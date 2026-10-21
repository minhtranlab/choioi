#!/usr/bin/env python3
"""Put the approved place backgrounds (art/places/*.svg, made by the [App] Bối cảnh chat) into index.html.

The app is one file, and BG.* are plain functions that return an SVG string, so each picture is copied into a
`PLACE` table between the two markers below (whitespace squeezed, nothing else changed). Run this again whenever a file
in art/places/ changes:  python3 tools/art/embed_places.py
Only the files listed in USED are copied (the ones a level uses now); add a name when a level starts using it."""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
USED = ['lop-hoc', 'san-truong', 'vuon-truong', 'cong-vien', 'vuon-nha-na-chieu', 'vuon-nha-na-dem', 'phong-na', 'sieu-thi', 'cong-truong-xay', 'phong-nha-moi',
        'nha-na-bo-doc', 'bep', 'doc-cau-qua-kenh', 'duong-toi-truong', 'duong-toi-truong-toi', 'cong-vien-chieu', 'phong-na-toi', 'phong-na-dem', 'trang-sach', 'cong-vao-truong',
        'roi-ben', 'ra-khoi', 'dao-bai-cat', 'dao-hai-dang', 'hang-kho-bau',
        # 21/10: the stage versions (-tron: the play area left plain, for the pages with things to play) and the road by the park
        'vuon-truong-tron', 'cong-vao-truong-tron', 'duong-toi-truong-tron', 'duong-toi-truong-toi-tron', 'cong-vien-duong',
        # 21/10 (b): every stage version (-tron) and close-up (-can-) of Unit 1 (art/places/README.md, table "Bản → trang")
        'san-truong-tron', 'cong-vien-tron', 'vuon-nha-na-chieu-tron', 'vuon-nha-na-dem-tron', 'phong-na-tron', 'sieu-thi-tron', 'cong-truong-xay-tron',
        'phong-nha-moi-tron', 'bep-tron', 'cong-vien-chieu-tron', 'phong-na-toi-tron', 'phong-na-dem-tron', 'roi-ben-tron', 'dao-bai-cat-tron', 'dao-hai-dang-tron',
        'vuon-nha-na-dem-can-ban', 'vuon-nha-na-dem-can-la', 'vuon-nha-na-dem-truoc-leu', 'phong-na-can-ban', 'phong-na-can-but', 'phong-na-can-san',
        'sieu-thi-can-ghe', 'cong-truong-can-cua-so', 'cong-truong-can-nha-xe', 'ra-khoi-can', 'vuon-truong-tron-ho', 'cong-vao-truong-tron-xe']
# things a game puts on a background, drawn once and used on every page (art/places/do-choi/, art/props/): copied into PROP, keyed by file name
PROPS = ['places/do-choi/cau-truot-phai', 'places/do-choi/cay-cau'] + [f'props/xe/{n}-{d}' for n in ('xe-om-xanh', 'xe-om-vang', 'xe-om-xanh-cho-khach', 'xe-om-vang-cho-khach',
         'xe-om-xanh-thung', 'xe-om-vang-thung', 'taxi-xanh-ngoc', 'taxi-xanh-ngoc-suv', 'xe-buyt-xanh-duong', 'xe-buyt-dien-xanh-la', 'xe-dua-don') for d in ('phai', 'trai')]
PROPS += ['props/xe/xe-dua-don-can', 'props/xe/xe-dua-don-can-trai']
PROPS += ['places/do-choi/doc-co'] + [f'props/nguoi/cong-an-giao-thong{t}' for t in ('', '-khen', '-dat-tay')]   # 21/10 (lần 2): the slope under the slide; the traffic police officer (frog crossing)   # Màn 0: the close-up school bus for the seating game (240×136, 4 windows for faces)
PROPS += [f'places/the-tranh/mot-ngay-{t}' for t in ('sang', 'chieu', 'toi')]   # Màn 6: the three day cards (120×90); the game draws Na on them
# things taken out of a picture for the app (asked after a play-test), without changing the file in art/places/
TRIM = {**{n: [r'<rect x="170.6" y="9.2"[^>]*/>', r'<path d="M173.6 12.4 V31"[^>]*/>', r'<path d="M173.6 31 v2.4[^"]*"[^>]*/>'] for n in ('cong-truong-xay', 'cong-truong-xay-tron')},   # the game draws the trolley-less hook that swings
        # the boat's wake (Màn 7): the game draws the team's boat from the side, with its own foam behind it
        **{n: [r'<path d="M64 140 Q90 122 106 104 M150 140 Q128 122 116 104"[^>]*/>'] for n in ('roi-ben', 'ra-khoi')},
        # two tiny shells on the beach (Màn 7): the games put their own shells, starfish and shapes on the sand
        'dao-bai-cat': [r'<path d="M60 126 q4 -6 8 0z"[^>]*/>', r'<path d="M120 120 l3 -5 3 5z"[^>]*/>']}   # name -> [regex, ...] cut out (each must match once). The far crane's own hook: the game hangs its own (Màn 5)
A, B = '/* PLACES:BEGIN (made by tools/art/embed_places.py from art/places/, do not edit by hand) */', '/* PLACES:END */'
def clean(path, name):
    s = open(path, encoding='utf-8').read().strip()
    s = re.sub(r'<\?xml[^>]*\?>', '', s); s = re.sub(r'<!--.*?-->', '', s, flags=re.S); s = re.sub(r'\s*\n\s*', ' ', s)
    s = s.replace(' xmlns="http://www.w3.org/2000/svg"', '', 1)
    for pat in TRIM.get(name, []):
        s, n = re.subn(pat, '', s); assert n == 1, (name, pat)
    assert '`' not in s and '${' not in s, name
    return s
parts = [f"'{n}':`{clean(os.path.join(ROOT, 'art', 'places', n + '.svg'), n)}`" for n in USED]
props = [f"'{os.path.basename(n)}':`{clean(os.path.join(ROOT, 'art', n + '.svg'), n)}`" for n in PROPS]
block = A + '\nconst PLACE={\n' + ',\n'.join(parts) + '\n};\nconst PROP={\n' + ',\n'.join(props) + '\n};\n' + B
p = os.path.join(ROOT, 'index.html'); h = open(p, encoding='utf-8').read()
if A in h:
    i = h.index(A); j = h.index(B, i) + len(B); h = h[:i] + block + h[j:]
else:   # first time: right before the BG table
    k = h.index('const BG={'); h = h[:k] + block + '\n' + h[k:]
open(p, 'w', encoding='utf-8').write(h)
print('places:', ', '.join(USED), '|', sum(len(x) for x in parts) // 1024, 'KB; props:', len(props), sum(len(x) for x in props) // 1024, 'KB')
