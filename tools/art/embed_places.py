#!/usr/bin/env python3
"""Put the approved place backgrounds (art/places/*.svg, made by the [App] Bối cảnh chat) into index.html.

The app is one file, and BG.* are plain functions that return an SVG string, so each picture is copied into a
`PLACE` table between the two markers below (whitespace squeezed, nothing else changed). Run this again whenever a file
in art/places/ changes:  python3 tools/art/embed_places.py
Only the files listed in USED are copied (the ones a level uses now); add a name when a level starts using it."""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
USED = ['lop-hoc', 'san-truong', 'vuon-truong', 'cong-vien', 'vuon-nha-na-chieu', 'vuon-nha-na-dem', 'phong-na', 'sieu-thi', 'cong-truong-xay', 'phong-nha-moi']
# things taken out of a picture for the app (asked after a play-test), without changing the file in art/places/
TRIM = {'cong-truong-xay': [r'<path d="M146 10 V30"[^>]*/>', r'<rect x="142" y="30" width="8" height="5"[^>]*/>']}   # name -> [regex, ...] cut out (each must match once). The far crane's own hook: the game hangs its own (Màn 5)
A, B = '/* PLACES:BEGIN (made by tools/art/embed_places.py from art/places/, do not edit by hand) */', '/* PLACES:END */'
parts = []
for name in USED:
    s = open(os.path.join(ROOT, 'art', 'places', name + '.svg'), encoding='utf-8').read().strip()
    s = re.sub(r'<\?xml[^>]*\?>', '', s); s = re.sub(r'<!--.*?-->', '', s, flags=re.S); s = re.sub(r'\s*\n\s*', ' ', s)
    s = s.replace(' xmlns="http://www.w3.org/2000/svg"', '', 1)
    for pat in TRIM.get(name, []):
        s, n = re.subn(pat, '', s); assert n == 1, (name, pat)
    assert '`' not in s and '${' not in s, name
    parts.append(f"'{name}':`{s}`")
block = A + '\nconst PLACE={\n' + ',\n'.join(parts) + '\n};\n' + B
p = os.path.join(ROOT, 'index.html'); h = open(p, encoding='utf-8').read()
if A in h:
    i = h.index(A); j = h.index(B, i) + len(B); h = h[:i] + block + h[j:]
else:   # first time: right before the BG table
    k = h.index('const BG={'); h = h[:k] + block + '\n' + h[k:]
open(p, 'w', encoding='utf-8').write(h)
print('places:', ', '.join(USED), '|', sum(len(x) for x in parts) // 1024, 'KB')
