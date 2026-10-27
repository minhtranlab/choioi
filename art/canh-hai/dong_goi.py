#!/usr/bin/env python3
"""Đóng gói cảnh hài (27/10).
  1. canh-hai-hinh.js : CanhHai.HINH = mọi hình kit mà 6 cảnh dùng (lấy thẳng từ art/kit/, bản -phai).
  2. xem-thu.html     : trang xem thử chạy riêng một file (nhúng JS, nền art/places, vài hình của app để dựng sân khấu).
Chạy: python3 art/canh-hai/dong_goi.py   (cần node để lấy hình của app từ index.html; chỉ đọc, không sửa index.html)"""
import os, json, subprocess, re

D = os.path.dirname(os.path.abspath(__file__))
ART = os.path.dirname(D)
REPO = os.path.dirname(ART)
KIT = os.path.join(ART, 'kit')

HINH = {
    # Polly (có sẵn) và tư thế mới
    **{f'polly-{p}': f'nhan-vat/polly/polly-{p}-phai.svg' for p in
       ['dung', 'noi', 'bay-1', 'bay-2', 'treo-nguoc', 'ngu', 'tha-1', 'tha-2', 'tho-1', 'tho-2', 'chan-1', 'chan-2']},
    # các bạn: đứng (có sẵn) và ngạc nhiên (mới)
    **{f'{k}-{p}': f'nhan-vat/{k}/{k}-{p}-phai.svg' for k in ['lam', 'na', 'ben'] for p in ['dung', 'ngac-nhien']},
    'bot-mo-polly': 'do-vat/bot-mo-polly-phai.svg',
    'doi-ngu-treo-nguoc': 'con-vat/doi-ngu-treo-nguoc-phai.svg',
    'canh-cay': 'do-vat/canh-cay-phai.svg',
    'nai-chuoi-to': 'do-vat/nai-chuoi-to-phai.svg',
    'vo-chuoi': 'do-vat/vo-chuoi-phai.svg',
    'thung-rac': 'do-vat/thung-rac-phai.svg',
    'ban-an': 'do-vat/ban-an-phai.svg',
}
JS = ['canh-hai-chung.js', 'canh-hai-hinh.js'] + [f'man-{i}.js' for i in range(1, 7)]
NEN = ['cong-vien-tron', 'vuon-nha-na-dem-tron', 'phong-na-tron', 'sieu-thi-tron', 'cong-truong-xay-tron', 'bep-tron']

# hình của app (chỉ để dựng sân khấu xem thử; trong app các thứ này đã có sẵn trên trang)
LAY_APP = r"""
const fs=require('fs'); const s=fs.readFileSync(process.argv[1],'utf8');
const INK='#361D46', OL=`stroke="${INK}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"`;
const L=s.split('\n');
const line=(pre)=>{ const l=L.find(x=>x.trimStart().startsWith(pre)); if(!l) throw new Error('khong thay '+pre); return l.trimStart().slice(pre.length).replace(/[;,]\s*(\/\/.*|\/\*.*)?$/,'') };
const ev=src=>eval('('+src+')');
const catG=ev(line('function catG').replace(/^/,'function catG'));
const out={
  cat:`<svg viewBox="-16 -40 32 42" overflow="visible">${catG(0,0,1)}</svg>`,
  basket:ev(line('basket:()=>`<svg viewBox="0 0 100 80">').replace(/^/,'()=>`<svg viewBox="0 0 100 80">'))(),
  cart:ev(line('const SHOPCART_SVG='))(),
  roof:ev(line('const ROOF5_SVG='))(),
  house:ev(line('const HOUSE5_SVG='))(),
  tree:ev(line('const TREE_ART='))(),
  shelf:ev(line('const WSHELF_BOXES_SVG='))(),
};
process.stdout.write(JSON.stringify(out));
"""


def svg(rel):
    t = open(os.path.join(KIT, rel)).read().strip()
    return re.sub(r'\s+xmlns="[^"]+"', '', t, count=1)


def main():
    hinh = {k: svg(v) for k, v in HINH.items()}
    open(os.path.join(D, 'canh-hai-hinh.js'), 'w').write(
        '/* Hình kit cho 6 cảnh hài: TỰ SINH bởi dong_goi.py từ art/kit/ (đừng sửa tay). */\n'
        '(window.CanhHai = window.CanhHai || {}).HINH = Object.assign(window.CanhHai.HINH || {}, '
        + json.dumps(hinh, ensure_ascii=False, indent=0) + ');\n')
    app = subprocess.run(['node', '-e', LAY_APP, os.path.join(REPO, 'index.html')], capture_output=True, text=True, check=True).stdout
    nen = {n: open(os.path.join(ART, 'places', n + '.svg')).read().strip() for n in NEN}
    js = '\n'.join(open(os.path.join(D, f)).read() for f in JS)
    mau = open(os.path.join(D, 'xem-thu.mau.html')).read()
    html = mau.replace('/*@JS*/', js.replace('</script', '<\\/script')).replace('/*@NEN*/{}', json.dumps(nen, ensure_ascii=False)).replace('/*@APP*/{}', app)
    open(os.path.join(D, 'xem-thu.html'), 'w').write(html)
    print('canh-hai-hinh.js', len(json.dumps(hinh)) // 1024, 'KB · xem-thu.html', len(html) // 1024, 'KB')


if __name__ == '__main__':
    main()
