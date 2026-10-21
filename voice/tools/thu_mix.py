#!/usr/bin/env python3
"""Chơi hết 8 màn (nhanh) rồi chơi Fun Mix 3 lần (có trò thưởng), ghi lại mọi câu Chồi nói: python3 thu_mix.py SỐ_LẦN thu-mix.json"""
import asyncio,json,sys
from playwright.async_api import async_playwright
RUNS=int(sys.argv[1]); OUT=sys.argv[2]
POLLY=r"""pollyEcho=async function(word,vi){ const en=String(word).split(/(?<=[!?.])\s+/), vv=String(vi||word).split(/(?<=[!?.])\s+/); en.forEach((e,i)=>window.__sayLog.push([e, vv.length===en.length?vv[i]:(i?'':vv.join(' ')),0,'p'])) };"""
async def main():
    out=[]
    async with async_playwright() as p:
        br=await p.chromium.launch()
        for r in range(RUNS):
            pg=await br.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text[:200]) if m.type=='error' else None)
            await pg.goto('http://localhost:8765/index.html#auto'); await pg.wait_for_timeout(400)
            lang=['en','vi'][r%2]
            await pg.evaluate(f"""()=>{{ window.__sayLog=[]; window.__autoWrong={[0,0.4][r%2]}; {POLLY} window.__kid=[]; {{ const o=say; say=function(en,vi,opt){{ if(opt&&opt.kid) window.__kid.push([en,vi||'',opt.rate||0]); return o.apply(this,arguments) }} }}
              S.child={{name:'Bin',birthYear:2021}}; S.lang='{lang}'; S.lesson=0; save();
              window.__fin=false; (async()=>{{ for(let li=0;li<8;li++){{ try{{ await runSession(li) }}catch(e){{}} }} window.__sayLog=[]; window.__kid=[]; for(let k=0;k<3;k++){{ try{{ await viewMix() }}catch(e){{}} }} }})().then(()=>window.__fin=true,()=>window.__fin=true) }}""")
            for t in range(600):
                await pg.wait_for_timeout(1000)
                if await pg.evaluate("window.__fin"): break
            log=await pg.evaluate("window.__sayLog.concat(window.__kid.map(x=>[...x,'k']))"); await pg.close()
            print('mix run',r,lang,'lines',len(log),'t',t,errs[:1],flush=True)
            out+=[['chung']+e for e in log]
        await br.close()
    json.dump(out,open(OUT,'w'),ensure_ascii=False)
asyncio.run(main())
