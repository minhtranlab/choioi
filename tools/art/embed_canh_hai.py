#!/usr/bin/env python3
"""Put the comedy scenes of Unit 1 (art/canh-hai, chat [App] Cảnh hài) into index.html, as one <script> right before the app's script.
Run again after art/canh-hai changes:  python3 tools/art/embed_canh_hai.py
The block is marked CANH-HAI:START / CANH-HAI:END and is replaced as a whole."""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APP = os.path.join(ROOT, 'index.html')
SRC = os.path.join(ROOT, 'art', 'canh-hai')
FILES = ['canh-hai-chung.js', 'canh-hai-hinh.js'] + [f'man-{i}.js' for i in range(1, 7)]
parts = []
for f in FILES:
    t = open(os.path.join(SRC, f), encoding='utf-8').read()
    if '</script' in t.lower():
        sys.exit(f'{f}: contains </script')
    parts.append(f'/* ---- art/canh-hai/{f} ---- */\n' + t.strip() + '\n')
block = ('<script>/* CANH-HAI:START · the comedy scenes of Unit 1 (art/canh-hai, chat [App] Cảnh hài; Minh approved 8640864).\n'
         '   Made by tools/art/embed_canh_hai.py: do not edit here, edit art/canh-hai and run it again. */\n'
         + '\n'.join(parts) + '/* CANH-HAI:END */</script>\n')
s = open(APP, encoding='utf-8').read()
m = re.search(r'<script>/\* CANH-HAI:START.*?/\* CANH-HAI:END \*/</script>\n', s, re.S)
if m:
    s = s[:m.start()] + block + s[m.end():]
else:
    i = s.index('\n<script>\n')   # the app's own script
    s = s[:i + 1] + block + s[i + 1:]
open(APP, 'w', encoding='utf-8').write(s)
print('embedded', len(block), 'chars from', len(FILES), 'files')
