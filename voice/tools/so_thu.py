#!/usr/bin/env python3
"""Liệt kê mọi câu cho thú ăn ở sở thú (mỗi loài × mỗi món: thích / không ăn), lấy thẳng từ dữ liệu của app.
   python3 so_thu.py so-thu.json   (cần python3 -m http.server 8765 ở thư mục gốc repo)"""
import asyncio, json, sys
from playwright.async_api import async_playwright
JS = r"""()=>{ const P=[];
 for(const t of Object.keys(ZA)){ const D=ZA[t], short=cap(D.vi.replace(/^(chú|bạn) /,''));
   for(const f of Object.keys(ZFOOD)){
     if(D.eats.includes(f)) P.push(['chung',`Yum! ${zPl(t)} love ${ZFOOD[f].en}.`,`Ngon quá! ${short} thích ${ZFOOD[f].vi}.`,0,'']);
     else P.push(['chung',`${zPl(t)} don’t eat ${ZFOOD[f].en}. Try another one!`,`${short} không ăn ${ZFOOD[f].vi} đâu. Thử món khác nhé!`,0,'']) } }
 return P }"""
async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(); pg = await br.new_page()
        await pg.goto('http://localhost:8765/index.html#auto'); await pg.wait_for_timeout(500)
        P = await pg.evaluate(JS); await br.close()
    json.dump(P, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=0); print(len(P), 'câu')
asyncio.run(main())
