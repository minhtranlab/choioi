import re
NUM={'0':'zero','1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine','10':'ten'}
def words(t):
    t=t.lower().replace('’',"'")
    t=re.sub(r"\b(\d+)\b",lambda m:NUM.get(m.group(1),m.group(1)),t)
    return re.findall(r"[a-zà-ỹđ']+",t)
def lev(a,b):
    p=list(range(len(b)+1))
    for i in range(1,len(a)+1):
        c=[i]
        for j in range(1,len(b)+1): c.append(min(p[j]+1,c[j-1]+1,p[j-1]+(a[i-1]!=b[j-1])))
        p=c
    return p[-1]
def score(expected,heard):
    a,b=words(expected),words(heard)
    if not a: return 1.0
    return 1-lev(a,b)/max(len(a),1)
