import numpy as np
def segments(a,sr,min_gap=.12,th_db=-38):
    hop=int(sr*.01); n=len(a)//hop
    e=np.array([np.sqrt(np.mean(a[i*hop:(i+1)*hop]**2)+1e-12) for i in range(n)])
    db=20*np.log10(e/ (e.max()+1e-9)); voiced=db>th_db
    segs=[];start=None;gap=0
    for i,v in enumerate(voiced):
        if v:
            if start is None: start=i
            gap=0;end=i
        elif start is not None:
            gap+=1
            if gap*0.01>=min_gap: segs.append((start,end)); start=None
    if start is not None: segs.append((start,end))
    return [(max(0,s*hop-int(.03*sr)),min(len(a),(e_+1)*hop+int(.05*sr))) for s,e_ in segs]
