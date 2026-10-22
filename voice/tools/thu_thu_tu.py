#!/usr/bin/env python3
"""Cho app tự chơi từng màn và ghi lại THỨ TỰ câu nói trong mỗi lần chơi (để đóng gói giọng theo thứ tự nói):
python3 thu_thu_tu.py 0,1,2,3,4,5,6,7 thu-thu-tu.json   (cần python3 -m http.server 8765 ở thư mục gốc repo)
Mỗi màn chơi 8 lần: lần đầu (có giới thiệu), sai ít / sai nhiều, tiếng Anh / tiếng Việt, chơi lại."""
import asyncio,json,sys
from playwright.async_api import async_playwright
LEVELS=[int(x) for x in sys.argv[1].split(',')]; OUT=sys.argv[2]
RUNS=[dict(lang='en',wrong=0,first=True,replay=False),dict(lang='vi',wrong=0.35,first=True,replay=False),
      dict(lang='en',wrong=0.7,first=False,replay=False),dict(lang='vi',wrong=0.15,first=False,replay=True),
      dict(lang='en',wrong=0.5,first=False,replay=False),dict(lang='vi',wrong=0.7,first=False,replay=False),
      dict(lang='en',wrong=0.25,first=True,replay=True),dict(lang='vi',wrong=0.9,first=False,replay=False)]
HOOK=r"""()=>{ window.__seq=[];
  pollyEcho=async function(word,vi){ const en=String(word).split(/(?<=[!?.])\s+/), vv=String(vi||word).split(/(?<=[!?.])\s+/); en.forEach((e,i)=>window.__seq.push([e, vv.length===en.length?vv[i]:(i?'':vv.join(' ')),0,'p'])) };
  const o=say; say=function(en,vi,opt){ opt=opt||{}; window.__seq.push([en,vi||'',opt.rate||0, opt.kid?'k:'+opt.kid:(opt.polly?'p':'')]); return o.apply(this,arguments) } }"""
async def one(br,li,c):
    pg=await br.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto('http://localhost:8765/index.html#auto'); await pg.wait_for_timeout(400)
    await pg.evaluate(HOOK)
    await pg.evaluate(f"""()=>{{ window.__autoWrong={c['wrong']}; S.child={{name:'Bin',birthYear:2021}}; S.lang='{c['lang']}'; S.lesson=Math.max(S.lesson||0,{li}); S.done=S.done||{{}};
      for(let i=0;i<{li};i++) S.done[i]=1; if({str(c['replay']).lower()}) S.done[{li}]=1; if({str(c['first']).lower()}) S.introSeen={{}}; save();
      window.__fin=false; runSession({li}).then(()=>window.__fin=true,()=>window.__fin=true) }}""")
    for t in range(300):
        await pg.wait_for_timeout(1000)
        if await pg.evaluate("window.__fin"): break
    seq=await pg.evaluate("window.__seq"); await pg.close(); return seq,t,errs
async def main():
    out=[]
    async with async_playwright() as p:
        br=await p.chromium.launch()
        for li in LEVELS:
            for c in RUNS:
                seq,t,errs=await one(br,li,c)
                print(f'li{li} {c} lines={len(seq)} t={t}s errs={errs[:2]}',flush=True)
                out.append(dict(li=li,**c,seq=seq)); json.dump(out,open(OUT,'w'),ensure_ascii=False)
        await br.close()
asyncio.run(main())
