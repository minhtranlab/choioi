import re,numpy as np
from kokoro_onnx import Kokoro
from split import segments
K=Kokoro('/home/claude/models/kokoro-v1.0.onnx','/home/claude/models/voices-v1.0.bin')
CARRIER="Okay."
_cl={}
def carrier_len(voice,speed,lang):
    k=(voice if isinstance(voice,str) else id(voice),speed,lang)
    if k not in _cl:
        a,sr=K.create(CARRIER,voice=voice,speed=speed,lang=lang); s=segments(a,sr); _cl[k]=s[-1][1]/sr if s else len(a)/sr
    return _cl[k]
def trim(a,sr,th=0.008):
    idx=np.where(np.abs(a)>th)[0]
    if not len(idx): return a
    s=max(0,idx[0]-int(.02*sr)); e=min(len(a),idx[-1]+int(.08*sr)); a=a[s:e].copy()
    f=int(.008*sr); a[:f]*=np.linspace(0,1,f); g=int(.03*sr); a[-g:]*=np.linspace(1,0,g); return a
def sentence(s,voice,speed,lang):
    """one sentence, without the stray sound Kokoro adds before the first word when slowed down"""
    a,sr=K.create(CARRIER+" "+s,voice=voice,speed=speed,lang=lang)
    cl=carrier_len(voice,speed,lang)
    # first silence that starts after ~80% of the carrier
    hop=int(sr*.01); env=np.array([np.sqrt(np.mean(a[i:i+hop]**2)) for i in range(0,len(a)-hop,hop)])
    thr=max(env.max()*0.02,1e-4); quiet=env<thr
    lo=int(cl*0.45*100); hi=min(len(env),int(cl*1.6*100)+10)
    runs=[];i=lo
    while i<hi:
        if quiet[i]:
            j=i
            while j<len(env) and quiet[j]: j+=1
            runs.append((j-i,i,j)); i=j
        else: i+=1
    runs=[r for r in runs if r[0]>=5]
    if not runs: return None,sr
    _,i0,j=runs[0]
    return trim(a[max(0,j*hop-int(.03*sr)):],sr),sr
def sents(t): return [s for s in re.split(r'(?<=[.!?…])\s+',t.strip()) if s]
def line(text,voice,speed,lang,gap=.6):
    parts=[];sr=24000
    for s in sents(text):
        a,sr=sentence(s,voice,speed,lang)
        if a is None: return None,sr
        parts+= [a,np.zeros(int(gap*sr),dtype=np.float32)]
    return np.concatenate(parts[:-1]),sr

from asr import transcribe
from qa import score
def plain(s,voice,speed,lang):
    a,sr=K.create(s,voice=voice,speed=speed,lang=lang); return trim(a,sr),sr
def best_sentence(s,voice,speed,lang,lang_asr='en'):
    """try a few ways, keep the one the recognizer hears exactly as written"""
    cands=[]
    for how in ('carrier','plain','carrier2'):
        if how=='carrier': a,sr=sentence(s,voice,speed,lang)
        elif how=='plain': a,sr=plain(s,voice,speed,lang)
        else:
            global CARRIER; old=CARRIER; CARRIER="Yes!"; _cl.clear(); a,sr=sentence(s,voice,speed,lang); CARRIER=old; _cl.clear()
        if a is None: continue
        h=transcribe(a,sr,lang_asr); sc=score(s,h); cands.append((sc,how,a,h))
        if sc>=1: break
    cands.sort(key=lambda c:-c[0]); return cands[0] if cands else (0,'none',None,'')
def best_line(text,voice,speed,lang,gap=.6):
    parts=[];info=[];sr=24000
    for s in sents(text):
        sc,how,a,h=best_sentence(s,voice,speed,lang)
        info.append((round(sc,2),how,h)); parts+=[a,np.zeros(int(gap*sr),dtype=np.float32)]
    return np.concatenate(parts[:-1]),sr,info
