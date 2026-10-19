import re
def vhash(s):
    h=2166136261
    for ch in s.encode('utf-16-le').decode('utf-16-le'):
        pass
    # JS charCodeAt iterates UTF-16 code units
    b=s.encode('utf-16-le'); 
    for i in range(0,len(b),2):
        h^=b[i]|(b[i+1]<<8); h=(h*16777619)&0xffffffff
    n=h; d='0123456789abcdefghijklmnopqrstuvwxyz'; o=''
    if n==0: return '0'
    while n: o=d[n%36]+o; n//=36
    return o
def vkey(t,slow=False,name=None):
    t=re.sub(r'\s+',' ',str(t)).strip()
    if name: t=re.sub(r'(^|[^\w])'+re.escape(name)+r'(?!\w)',r'\1{N}',t)
    return ('~' if slow else '')+t
