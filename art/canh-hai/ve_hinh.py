#!/usr/bin/env python3
"""Vẽ các hình mới cho 6 cảnh hài (27/10) vào art/kit/.
Chạy lại: python3 art/canh-hai/ve_hinh.py  (ghi đè đúng các file này, không đụng file khác).
Mỗi hình có -phai và -trai (bản lật ngang), cùng nét (#3A1B49) và màu với kit."""
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'kit'))
INK = '#3A1B49'


def save(rel, w, h, inner):
    """ghi <rel>-phai.svg và <rel>-trai.svg (lật ngang cả hình, như các file kit khác)"""
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    head = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" overflow="visible">'
    open(p + '-phai.svg', 'w').write(head + inner + '</svg>')
    open(p + '-trai.svg', 'w').write(head + f'<g transform="translate({w} 0) scale(-1 1)">' + inner + '</g></svg>')
    print('ve', rel)


# ---------- Polly: các phần lấy đúng từ polly-dung (khung 200×260, chân y 252) ----------
S = f'stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"'
TAIL = f'<path d="M104 210 L92 252 L104 246 L112 256 L114 214Z" fill="#E8484F" {S}/>'
LEGS = f'<path d="M86 226 v12 M108 226 v12" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
BODY = f'<ellipse cx="100" cy="170" rx="44" ry="58" fill="#4ECF62" stroke="{INK}" stroke-width="4.5"/>'
WING = (f'<path d="M60 150 Q42 200 76 222 Q86 190 82 158Z" fill="#3683C4" {S}/>'
        '<path d="M62 186 l14 -2 M66 202 l12 -2" stroke="#2A5E96" stroke-width="3.8"/>')
BELLY = '<ellipse cx="104" cy="186" rx="24" ry="30" fill="#FFE07A" opacity=".9"/>'
HEAD = f'<circle cx="104" cy="98" r="46" fill="#4ECF62" stroke="{INK}" stroke-width="4.5"/>'
CREST = f'<path d="M88 56 q-4 -22 10 -30 q0 14 8 20 q4 -18 18 -18 q-6 14 -2 28" fill="#E8484F" {S}/>'
BEAK = f'<path d="M132 104 Q164 104 160 132 Q152 128 134 124Z" fill="#FBB516" {S}/>'
EYE = (f'<circle cx="116" cy="94" r="14" fill="#FFFFFF" stroke="{INK}" stroke-width="3.8"/>'
       f'<circle cx="118" cy="95" r="7" fill="{INK}"/><circle cx="120" cy="92" r="2.6" fill="#fff"/>')
CHEEK = '<ellipse cx="96" cy="118" rx="8" ry="5" fill="#F7A9B8"/>'
DROP = lambda x, y, s=1: (f'<path d="M{x} {y} q{-7*s:.1f} {11*s:.1f} 0 {16*s:.1f} q{7*s:.1f} {-5*s:.1f} 0 {-16*s:.1f}z" '
                          'fill="#BFE3FA" stroke="#3683C4" stroke-width="1.6"/>')

# 1. Polly treo ngược: cả thân lật dọc (mỏ vẫn quay phải), chân bám cành ở trên (móng ở y 12–20, x 86 và 108)
tail_up = f'<g transform="rotate(-28 109 212)">{TAIL}</g>'
flip = f'<g transform="translate(0 262) scale(1 -1)">{tail_up}{BODY}{WING}{BELLY}{HEAD}{CREST}{BEAK}</g>'
legs_up = (f'<path d="M86 34 V18 M108 34 V18" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
           f'<path d="M79 22 q1 -9 8 -8 q6 1 6 9 M101 22 q1 -9 8 -8 q6 1 6 9" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
eye_up = (f'<circle cx="116" cy="168" r="14" fill="#FFFFFF" stroke="{INK}" stroke-width="3.8"/>'
          f'<circle cx="118" cy="168" r="7" fill="{INK}"/><circle cx="120" cy="165" r="2.6" fill="#fff"/>'
          '<ellipse cx="96" cy="146" rx="8" ry="5" fill="#F7A9B8"/>')
save('nhan-vat/polly/polly-treo-nguoc', 200, 260, legs_up + flip + eye_up)

# 2. Polly rúc đầu ngủ: thân phồng lên, đầu quay ra sau, mỏ vùi vào cánh, mắt nhắm
ngu = (TAIL + LEGS
       + f'<ellipse cx="100" cy="172" rx="47" ry="56" fill="#4ECF62" stroke="{INK}" stroke-width="4.5"/>' + BELLY
       + f'<circle cx="94" cy="108" r="44" fill="#4ECF62" stroke="{INK}" stroke-width="4.5"/>'
       + f'<path d="M72 74 q-18 -16 -10 -34 q8 12 16 14 q-4 -18 8 -26 q2 14 10 22" fill="#E8484F" {S}/>'
       + f'<path d="M64 112 Q40 112 44 136 Q54 132 66 128Z" fill="#FBB516" {S}/>'          # mỏ quay ra sau, chúi xuống cánh
       + f'<path d="M58 118 Q30 150 50 200 Q66 226 80 224 Q92 190 90 156 Q86 128 58 118Z" fill="#3683C4" {S}/>'  # cánh khép lên che mỏ
       + '<path d="M58 160 l16 -2 M60 178 l16 -2 M64 196 l14 -2" stroke="#2A5E96" stroke-width="3.8"/>'
       + f'<path d="M92 104 q9 8 18 0" fill="none" stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/>'  # mắt nhắm
       + '<ellipse cx="106" cy="122" rx="8" ry="5" fill="#F7A9B8"/>')
save('nhan-vat/polly/polly-ngu', 200, 260, ngu)

# 3. Polly tha nải chuối (hai hình vỗ cánh như bay-1 / bay-2): chân duỗi xuống quặp, mắt nhắm tịt vì gắng sức, giọt mồ hôi
#    chỗ chân quặp: (100, 246) trong khung → đặt cuống nải chuối ở đó
def tha(f2):
    wing = f'<g transform="rotate(-28 77 157)">{WING}</g>' if f2 else WING
    legs = (f'<path d="M90 222 L94 248 M110 222 L106 248" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M86 254 q8 6 14 -2 M100 254 q8 6 14 -2" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    face = (f'<path d="M108 86 L124 94 L108 102" fill="none" stroke="{INK}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>'
            '<ellipse cx="96" cy="118" rx="10" ry="6.5" fill="#F28A9A" opacity=".85"/>'
            f'<path d="M136 116 h20" stroke="{INK}" stroke-width="3"/>')
    g = f'<g transform="translate(0 -10)">{TAIL}{legs}{BODY}{wing}{BELLY}{HEAD}{CREST}{BEAK}{face}</g>'
    return g + DROP(150, 44) + DROP(162, 64, .8)
save('nhan-vat/polly/polly-tha-1', 200, 260, tha(False))
save('nhan-vat/polly/polly-tha-2', 200, 260, tha(True))

# 4. Polly thở hổn hển (hai hình: mỏ há to / há vừa), mắt lờ đờ, cánh xệ, mồ hôi
def tho(wide):
    lower = ('M134 122 Q156 134 150 150 Q140 146 132 130Z' if wide else 'M134 120 Q154 124 152 140 Q142 138 132 128Z')
    beak = (f'<path d="{lower}" fill="#E59A12" {S}/>'
            + ('<ellipse cx="144" cy="128" rx="7" ry="4" fill="#F28A9A"/>' if wide else '')
            + f'<path d="M132 98 Q166 92 164 120 Q154 116 134 116Z" fill="#FBB516" {S}/>')
    eye = (f'<circle cx="116" cy="96" r="13" fill="#FFFFFF" stroke="{INK}" stroke-width="3.8"/>'
           f'<circle cx="118" cy="100" r="6.5" fill="{INK}"/>'
           f'<path d="M102 96 A14 14 0 0 1 130 96 Z" fill="#4ECF62" stroke="{INK}" stroke-width="3.8" stroke-linejoin="round"/>')
    wing = f'<g transform="rotate(14 80 156)">{WING}</g>'
    return (TAIL + LEGS + BODY + wing + BELLY + HEAD + CREST + beak + eye + CHEEK
            + DROP(150, 40) + DROP(70, 60, .8) + DROP(164, 66, .7))
save('nhan-vat/polly/polly-tho-1', 200, 260, tho(True))
save('nhan-vat/polly/polly-tho-2', 200, 260, tho(False))

# 5. Hai chân Polly đang bước (chỉ có chân, cùng khung Polly): thò ra dưới mái nhà ở Màn 5
def chan(k):
    a, b = ((80, 116) if k == 1 else (90, 106))
    la, lb = ((-4, 0) if k == 1 else (0, -4))
    def foot(x, lift):
        y = 250 + lift
        return (f'<path d="M{x} 204 L{x} {y}" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
                f'<path d="M{x-14} {y+3} L{x} {y} L{x+14} {y+3} M{x} {y} L{x+4} {y+8}" fill="none" stroke="{INK}" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>')
    return foot(a, la) + foot(b, lb)
save('nhan-vat/polly/polly-chan-1', 200, 260, chan(1))
save('nhan-vat/polly/polly-chan-2', 200, 260, chan(2))

# 6. Bọt trên mỏ: lớp phủ cùng khung Polly (200×260), đặt chồng đúng lên Polly (dung / noi)
foam = [(150, 112, 16), (166, 124, 12), (138, 126, 13), (156, 138, 10), (132, 104, 10), (170, 102, 9), (148, 92, 9),
        (124, 62, 10), (140, 72, 7), (108, 56, 6), (180, 86, 5), (120, 140, 6), (176, 142, 5)]
bot = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" stroke="{INK}" stroke-width="2.4"/>' for x, y, r in foam)
bot += ''.join(f'<circle cx="{x-r*.35:.1f}" cy="{y-r*.35:.1f}" r="{r*.28:.1f}" fill="#BFE3FA"/>' for x, y, r in foam if r >= 6)
save('do-vat/bot-mo-polly', 200, 260, bot)

# ---------- con vật ----------
# 7. Dơi ngủ treo ngược: chân bám ở trên (50, 4), cánh quấn quanh người, đầu ở dưới, tai chĩa xuống, mắt nhắm
BAT, BAT_D, BAT_H = '#5A4A7A', '#3F325C', '#7E6CA3'
doi = (f'<path d="M42 16 V6 M58 16 V6" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>'
       f'<path d="M36 8 q2 -8 7 -6 M64 8 q-2 -8 -7 -6" fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>'
       f'<path d="M34 128 L26 146 L46 134Z M66 128 L74 146 L54 134Z" fill="{BAT_H}" stroke="{INK}" stroke-width="3.6" stroke-linejoin="round"/>'
       '<path d="M33 134 L30 141 L39 136Z M67 134 L70 141 L61 136Z" fill="#F7A9B8"/>'
       f'<path d="M38 14 Q12 40 16 80 Q20 104 50 108 Q80 104 84 80 Q88 40 62 14Z" fill="{BAT}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
       f'<path d="M50 20 V102 M34 32 Q28 64 36 98 M66 32 Q72 64 64 98" fill="none" stroke="{BAT_D}" stroke-width="2.6" stroke-linecap="round"/>'
       f'<path d="M16 80 q8 -6 16 0 q8 -6 18 0 q10 -6 18 0 q8 -6 16 0" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
       f'<circle cx="50" cy="114" r="22" fill="{BAT_H}" stroke="{INK}" stroke-width="4"/>'
       f'<path d="M37 118 q6 6 12 0 M51 118 q6 6 12 0" fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>'
       f'<path d="M45 105 q5 -5 10 0" fill="none" stroke="{INK}" stroke-width="2.8" stroke-linecap="round"/>'
       '<circle cx="36" cy="108" r="4" fill="#F7A9B8" opacity=".8"/><circle cx="64" cy="108" r="4" fill="#F7A9B8" opacity=".8"/>')
save('con-vat/doi-ngu-treo-nguoc', 100, 146, doi)

# ---------- đồ vật ----------
# 8. Cành cây vươn ngang từ bên trái (để dơi và Polly treo, đậu): mặt trên y ≈ 14, mặt dưới (chỗ bám treo) y ≈ 24
canh = (f'<path d="M-6 10 Q60 8 120 14 Q160 16 198 13 L198 19 Q160 24 120 25 Q60 26 -6 32Z" fill="#8A5A36" stroke="{INK}" stroke-width="3.6" stroke-linejoin="round"/>'
        '<path d="M14 20 q20 -3 40 0 M84 19 q16 -2 30 0" stroke="#6E4528" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
        f'<path d="M150 17 q6 -10 18 -13" fill="none" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>'
        + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="11" ry="6" transform="rotate({a} {x} {y})" fill="#58B592" stroke="{INK}" stroke-width="2.6"/>'
                  for x, y, a in [(34, 2, -20), (96, 4, 18), (172, -2, -30), (196, 10, 20), (6, 36, 25)]))
save('do-vat/canh-cay', 200, 40, canh)

# 9. Nải chuối to (đồ cận): cuống ở trên (60, 6), Polly quặp ở đó; các quả xoè xuống dưới
BAN = 'M20 26 C18 60 42 84 82 74 C86 72 84 66 80 66 C50 70 34 52 30 26 C30 20 20 20 20 26Z'
def qua(a, col, mirror):
    t = f'translate(60 6) {"scale(-1 1) " if mirror else ""}rotate({a}) translate(-25 -20)'
    return (f'<g transform="{t}"><path d="{BAN}" fill="{col}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
            '<path d="M34 40 C38 56 50 64 66 66" fill="none" stroke="#E0A92E" stroke-width="2.6" stroke-linecap="round"/>'
            '<path d="M78 66 l6 2 -2 6z" fill="#6E4528"/></g>')
nai = (''.join(qua(a, c, True) for a, c in [(-2, '#FCC93A'), (20, '#FFD84A'), (40, '#FFE066')])
       + ''.join(qua(a, c, False) for a, c in [(-2, '#FFD84A'), (20, '#FCC93A'), (40, '#FFE066')])
       + f'<path d="M52 10 L56 -6 L66 -6 L68 10 Q60 14 52 10Z" fill="#9B6A45" stroke="{INK}" stroke-width="3.2" stroke-linejoin="round"/>')
save('do-vat/nai-chuoi-to', 126, 102, f'<g transform="translate(3 6)">{nai}</g>')

# 10. Vỏ chuối (đứng, cuống trên (40, 4)): bốn vạt rủ xuống; đội lên đầu Polly thành cái mũ
vo = (f'<path d="M36 6 L38 -6 L46 -5 L44 7Z" fill="#9B6A45" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
      f'<path d="M44 16 Q66 26 72 50 Q66 56 60 50 Q56 32 40 22Z" fill="#FFF1B0" stroke="{INK}" stroke-width="3.2" stroke-linejoin="round"/>'
      f'<path d="M36 16 Q12 28 6 52 Q12 58 18 52 Q24 32 42 22Z" fill="#FFD84A" stroke="{INK}" stroke-width="3.2" stroke-linejoin="round"/>'
      f'<path d="M44 18 Q64 30 70 56 Q64 62 58 56 Q54 36 38 24Z" fill="#FCC93A" stroke="{INK}" stroke-width="3.2" stroke-linejoin="round"/>'
      f'<path d="M36 20 Q28 42 34 62 Q40 68 46 62 Q46 40 44 20Z" fill="#FFD84A" stroke="{INK}" stroke-width="3.2" stroke-linejoin="round"/>'
      f'<path d="M26 10 Q40 0 54 10 Q52 22 40 24 Q28 22 26 10Z" fill="#FFD84A" stroke="{INK}" stroke-width="3.2" stroke-linejoin="round"/>'
      '<path d="M8 50 l4 4 M66 54 l-4 4 M36 62 l4 3" stroke="#6E4528" stroke-width="3" stroke-linecap="round"/>')
save('do-vat/vo-chuoi', 80, 76, f'<g transform="translate(0 6)">{vo}</g>')

# 11. Thùng rác đạp chân trong bếp (đồ cận): nắp là nhóm <g class="nap">, bản lề ở (6, 22) → xoay quanh điểm đó để mở
thung = (f'<path d="M10 26 L14 82 Q14 86 18 86 H50 Q54 86 54 82 L58 26Z" fill="#7FCBA8" stroke="{INK}" stroke-width="3.6" stroke-linejoin="round"/>'
         '<path d="M14 38 H54" stroke="#58B592" stroke-width="3"/><path d="M26 50 V74 M34 50 V74 M42 50 V74" stroke="#5FAE8C" stroke-width="2.6" stroke-linecap="round"/>'
         f'<rect x="38" y="84" width="16" height="6" rx="2" fill="#B9C3CC" stroke="{INK}" stroke-width="2.8"/>'
         f'<g class="nap"><path d="M6 20 Q34 6 62 20 L62 26 H6Z" fill="#58B592" stroke="{INK}" stroke-width="3.6" stroke-linejoin="round"/>'
         f'<path d="M28 13 Q34 9 40 13" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/></g>')
save('do-vat/thung-rac', 64, 92, thung)

# 11b. Bàn ăn nhỏ trong bếp (Màn 6, vòng 3): mặt bàn gỗ, hai chân. **Mặt bàn y 6** (đồ đặt lên bàn có đáy ở y 6). Đồ cận
ban = (f'<path d="M12 14 V60 M108 14 V60" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>'
       '<path d="M12 14 V60 M108 14 V60" stroke="#C98A52" stroke-width="6" stroke-linecap="round"/>'
       f'<path d="M10 16 H110 V24 H10Z" fill="#B5733E" stroke="{INK}" stroke-width="3.2" stroke-linejoin="round"/>'
       f'<rect x="2" y="5" width="116" height="11" rx="4" fill="#E9AE76" stroke="{INK}" stroke-width="3.6"/>'
       '<path d="M10 9 H70" stroke="#F6CFA0" stroke-width="2.4" stroke-linecap="round"/>')
save('do-vat/ban-an', 120, 64, ban)

# ---------- 12. mặt ngạc nhiên của Lam, Na, Ben: thân đứng, hai tay giơ lên cạnh má, mặt "surprised" giống hệt app (kidFace) ----------
CK_EY = {'lam': 102, 'na': 104, 'ben': 104}
def surprised(ey):
    my = ey + 16
    return (f'<path d="M70 {ey-17} q10 -8 20 -2 M110 {ey-19} q10 -6 20 2" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/>'
            f'<circle cx="80" cy="{ey}" r="9" fill="{INK}"/><circle cx="120" cy="{ey}" r="9" fill="{INK}"/>'
            f'<circle cx="83" cy="{ey-4}" r="3.2" fill="#fff"/><circle cx="123" cy="{ey-4}" r="3.2" fill="#fff"/>'
            f'<ellipse cx="100" cy="{my+8}" rx="8" ry="10" fill="{INK}"/>')
for who, ey in CK_EY.items():
    src = open(os.path.join(ROOT, 'nhan-vat', who, f'{who}-dung-phai.svg')).read()
    inner = re.sub(r'^<svg[^>]*>', '', src).replace('</svg>', '')
    inner = inner.replace('M76 158 Q64 176 64 194', 'M76 160 Q54 162 50 142').replace('M124 158 Q136 176 136 194', 'M124 160 Q146 162 150 142')
    inner = inner.replace('<circle cx="64" cy="198"', '<circle cx="50" cy="138"').replace('<circle cx="136" cy="198"', '<circle cx="150" cy="138"')
    n = 0
    def face(m):
        global n
        return m.group(1) + surprised(ey)
    inner, k = re.subn(r'(<g transform="translate\(0 0\)">)<ellipse cx="80" cy="\d+" rx="7" ry="9".*?stroke-linecap="round"/>', face, inner, flags=re.S)
    assert k == 1, who
    save(f'nhan-vat/{who}/{who}-ngac-nhien', 200, 260, inner)
