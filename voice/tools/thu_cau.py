#!/usr/bin/env python3
"""Cho app tự chơi một số màn (trình duyệt không đầu) và ghi lại mọi câu Chồi nói: python3 thu_cau.py SỐ_LẦN 0,1 thu-cau.json"""
import asyncio,json,sys
from playwright.async_api import async_playwright
RUNS=int(sys.argv[1]); LEVELS=[int(x) for x in sys.argv[2].split(',')]; OUT=sys.argv[3]
POLLY=r"""pollyEcho=async function(word,vi){ const en=String(word).split(/(?<=[!?.])\s+/), vv=String(vi||word).split(/(?<=[!?.])\s+/); en.forEach((e,i)=>window.__sayLog.push([e, vv.length===en.length?vv[i]:(i?'':vv.join(' ')),0,'p'])) };"""
async def one(br,li,wrong,lang,replay,first):
    pg=await br.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto('http://localhost:8765/index.html#auto'); await pg.wait_for_timeout(400)
    await pg.evaluate(f"""()=>{{ window.__sayLog=[]; window.__autoWrong={wrong}; {POLLY}
      S.child={{name:'Bin',birthYear:2021}}; S.lang='{lang}'; S.lesson=Math.max(S.lesson||0,{li}); S.done=S.done||{{}};
      for(let i=0;i<{li};i++) S.done[i]=1; if({'true' if replay else 'false'}) S.done[{li}]=1; if({'true' if first else 'false'}) S.introSeen={{}}; save();
      window.__fin=false; runSession({li}).then(()=>window.__fin=true,()=>window.__fin=true) }}""")
    for t in range(240):
        await pg.wait_for_timeout(1000)
        if await pg.evaluate("window.__fin"): break
    log=await pg.evaluate("window.__sayLog"); await pg.close(); return log,t,errs
async def main():
    out=[]
    async with async_playwright() as p:
        br=await p.chromium.launch()
        for r in range(RUNS):
            for li in LEVELS:
                wrong=[0,0.35,0.7,0.15][r%4]; lang=['en','vi'][r%2]; replay=(r%3==2); first=(r%5==0)
                log,t,errs=await one(br,li,wrong,lang,replay,first)
                print(f'run{r} li{li} w{wrong} {lang} replay{replay} lines={len(log)} t={t}s errs={errs[:2]}',flush=True)
                out+=[[li]+e for e in log]
            json.dump(out,open(OUT,'w'),ensure_ascii=False)
        await br.close()
asyncio.run(main())
