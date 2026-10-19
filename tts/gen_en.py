"""Generate every English line in 3 speeds with Kokoro af_heart, checked by a recognizer. Cached per line."""
import json,os,re,sys,time,numpy as np,soundfile as sf
import kgen
from asr import transcribe
from qa import score
from vh import vhash
VOICE='af_heart'; LANG='en-us'
SPEEDS={'s':(0.62,0.75),'m':(0.70,0.60),'f':(0.84,0.45)}
VI=re.compile(r'[ăâđêôơưàáảãạèéẻẽẹìíỉĩịòóỏõọùúủũụỳýỷỹỵ]',re.I)
def tts_text(key):
    t=key.lstrip('~')
    t=re.sub(r',\s*\{N\}','',t); t=re.sub(r'\{N\},?\s*','',t)
    t=t.replace('’',"'").replace('Chồi','Choy').replace('…','.')
    return t.strip()
def todo():
    L=json.load(open('lines.json'))
    return [o for o in L if o['lang']=='en' and not VI.search(o['key']) and o['key'] not in ('aria-label',)]
def sentence_best(s,speed):
    cands=[]
    for how in ('carrier','carrier2','plain'):
        if how=='carrier': a,sr=kgen.sentence(s,VOICE,speed,LANG)
        elif how=='carrier2':
            old=kgen.CARRIER; kgen.CARRIER='Yes!'; kgen._cl.clear(); a,sr=kgen.sentence(s,VOICE,speed,LANG); kgen.CARRIER=old; kgen._cl.clear()
        else: a,sr=kgen.plain(s,VOICE,speed,LANG)
        if a is None or len(a)<sr*0.12: continue
        h=transcribe(a,sr,'en'); sc=score(s,h); cands.append((sc,how,a,h))
        if sc>=0.999: break
    cands.sort(key=lambda c:-c[0])
    return cands[0] if cands else (0,'none',np.zeros(2400,dtype=np.float32),'')
def gen(o,spd):
    key=o['key']; slow=key.startswith('~'); speed,gap=SPEEDS[spd]
    if slow: speed*=0.85
    text=tts_text(key); parts=[]; info=[]
    ss=kgen.sents(text) or [text]
    for s in ss:
        sc,how,a,h=sentence_best(s,speed); info.append([round(sc,2),how,h]); parts+=[a,np.zeros(int(gap*24000),dtype=np.float32)]
    return np.concatenate(parts[:-1]),info
if __name__=='__main__':
    spds=sys.argv[1].split(',') if len(sys.argv)>1 else ['m','s','f']
    lim=int(sys.argv[2]) if len(sys.argv)>2 else 10**9
    sh=sys.argv[3] if len(sys.argv)>3 else '0/1'; si,sn=map(int,sh.split('/'))
    T=[o for o in todo() if int(vhash(o['key']),36)%sn==si]; t0=time.time(); n=0
    for spd in spds:
        d=f'clips/en-{spd}'; os.makedirs(d,exist_ok=True)
        for o in T[:lim]:
            h=vhash(o['key']); p=f'{d}/{h}.wav'
            if os.path.exists(p): continue
            a,info=gen(o,spd); sf.write(p,a,24000)
            json.dump({'key':o['key'],'info':info},open(f'{d}/{h}.json','w'),ensure_ascii=False)
            n+=1
            if n%25==0: print(spd,n,round(time.time()-t0),'s',flush=True)
    print('done',n,round(time.time()-t0))
