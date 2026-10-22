#!/usr/bin/env python3
"""Liệt kê câu của các bạn nhỏ (Lam, Na, Ben) và bác lái cần cẩu, ghi vào cau-ban-nho.json.
Câu chung (bạn nào nói cũng được) được ghi cho cả ba bạn; câu riêng ghi cho đúng bạn đó.
Câu sở thú lấy thẳng từ dữ liệu app (cần python3 -m http.server 8765 ở thư mục gốc repo):  python3 ban_nho.py"""
import asyncio, json
from playwright.async_api import async_playwright
KIDS = ['Lam', 'Na', 'Ben']
ANY = [  # friendSays(...) trong index.html: bạn nào nói tuỳ cảnh
 ('Yes!', 'Ừ!'), ('Yes.', 'Ừ.'), ('I feel happy!', 'Tớ thấy vui!'), ('I feel sad.', 'Tớ thấy buồn.'),
 ('I feel excited!', 'Tớ thấy háo hức quá!'), ('I feel proud!', 'Tớ thấy tự hào!'), ('I feel proud!', 'Mình thấy tự hào!'),
 ('Oh! Butterflies!', 'Ồ! Bươm bướm!'), ('Oh! Sweets!', 'Ồ! Kẹo!'), ('Let’s play a drum game!', 'Mình chơi trò gõ trống nhé!'),
 ('Mmm! Slurp!', 'Ngon quá! Sụp sụp!')]
OWN = {  # câu của đúng một bạn
 'Lam': [('Hi! I’m Lam!', 'Chào bạn! Mình là Lam!'), ('I want to catch one!', 'Tớ muốn bắt một con!')],
 'Na':  [('Hi! I’m Na!', 'Chào bạn! Mình là Na!'), ('They look like tiny stars!', 'Trông như những ngôi sao tí hon!')],
 'Ben': [('Hi! I’m Ben!', 'Chào bạn! Mình là Ben!'), ('Look! A firefly is on my nose!', 'Nhìn này! Một chú đom đóm đậu trên mũi tớ!')],
 'Bac': [('I’m busy building this tower. Help me finish it, then I can bring the hook down!', 'Bác đang bận xây cái tháp này. Con giúp bác xây xong, rồi bác hạ móc xuống cho nhé!')]}
JS = r"""()=>{ const P=[];
 for(const f of Object.keys(ZFOOD)){ const F=ZFOOD[f];
   if(KID_FOOD.includes(f)) P.push([`Yum! I love ${F.en}! Thank you!`,`Ngon quá! Tớ thích ${F.vi} lắm! Cảm ơn bạn!`]);
   else { const a=ZA[FOOD_FOR[f]]; P.push([`Hee hee! ${cap(F.en)}? I’m not a ${a.en}!`,`Hi hi! ${cap(F.vi)} á? Tớ đâu phải ${a.vi.replace(/^(chú|bạn) /,'')}!`]) } }
 return P }"""
async def zoo():
    async with async_playwright() as p:
        br = await p.chromium.launch(); pg = await br.new_page()
        await pg.goto('http://localhost:8765/index.html#auto'); await pg.wait_for_timeout(500)
        P = await pg.evaluate(JS); await br.close(); return P
out = []
for en, vi, z in [(e, v, 0) for e, v in ANY] + [(e, v, 1) for e, v in asyncio.run(zoo())]:
    for k in KIDS: out.append({'who': k, 'en': en, 'vi': vi, **({'zoo': 1} if z else {})})   # zoo: câu ở sở thú (đóng gói vào nhóm sothu)
for k, L in OWN.items():
    for en, vi in L: out.append({'who': k, 'en': en, 'vi': vi})
json.dump(out, open('cau-ban-nho.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(out), 'câu (đã nhân theo từng bạn)')
