# Trang chào (24/10) · ba thiết kế để Minh chọn

Đây là trang ba mẹ thấy khi mở link lần đầu. Hướng đã chốt ở `claude/chot-trang-chao-24-10.md`. Chỉ là thiết kế: chưa gắn vào `index.html`.

**Vòng 2 (24/10 trưa, góp ý của Minh):** chọn thiết kế A (bộ cả đội: Lam, Na, Ben, Polly, Chồi). Bỏ tấm bản đồ, vì bản đồ phải mở mới thấy. Đổi cảnh nền sang một trong các cảnh đẹp đã vẽ, Minh chọn một trong sáu cảnh. Bỏ B (đảo khối: chỉ là một phần của trò chơi, chưa đại diện) và C (xe buýt: nhiều thứ quá, hơi nhiễu).
Sửa chữ trong khung:
- "10 phút mỗi ngày cho bé 4–6 tuổi" xuống thành dòng nhỏ riêng, dưới "Toán · Khám phá · Tiếng Anh".
- Ghi chú dưới nút Chơi ngay chỉ còn: "Tiến độ của bé được lưu trong 7 ngày."

**Các vòng:**
- Vòng 1: ba thiết kế A, B, C. Minh chọn A (cả đội).
- Vòng 2: sáu cảnh nền. Công viên chiều được 7 điểm, cao nhất.
- Vòng 3: bốn phương án công viên chiều, Minh chấm như sau.

| Phương án | Điểm |
|---|---|
| Thả diều | 7 |
| **Đèn ông sao** | **8** (thích màu trời) |
| Bóng bay | 6 |
| Sông Sài Gòn | 6 (cầu đâm vào toà nhà; thuyền hay) |

**Bản cuối (24/10, 12:58, chờ Minh duyệt lần cuối)** là `trang-chao.html`, nền `places/cong-vien-chieu.svg`:
- Dải trời chiều tím hồng của bản đèn ông sao, mây hồng.
- Cửa sổ các toà nhà lên đèn.
- Thuyền buồm nhỏ trên sông (x 164–176, giữa hai cột đèn), chỉ dập dềnh tại chỗ; thêm một thuyền nữa ở x 44, sau khung chữ.
- Đàn chim nhỏ.
- Polly bay bên phải (x 162), tránh toà nhà cao Landmark.
- Không có cầu, không có đèn ông sao, không có dây đèn.

**BẢN CUỐI, Minh chọn (24/10, 13:33): `trang-chao.html`**
- Vòng 5: Minh chọn **trời xanh ban ngày** và **du thuyền**, trong năm màu trời và ba loại thuyền.
- Nền là `places/cong-vien-chieu.svg`, đổi thành ban ngày: dải trời xanh thay cho nền cam, mây trắng.
- Du thuyền trắng hai tầng có cờ đỏ, trên sông ở x 150–174 (giữa hai cột đèn), chỉ dập dềnh tại chỗ.
- Đàn chim nhỏ. Toà Landmark và các toà nhà giữ nguyên.
- Polly bay ngay trên Ben và Chồi (x 176, y 60), trong lớp cả đội.
- Không có cầu, không có đèn, không có bản đồ.

| File | Là gì |
|---|---|
| `trang-chao.html` | Bản cuối chạy riêng cả màn hình (hai lớp, xem mục *Hai lớp*); thêm `?dk` vào cuối link để mở sẵn Đăng ký |
| `nen.svg` | Lớp nền, vùng an toàn là viewBox |
| `ca-doi.svg` | Lớp cả đội, nền trong suốt, đáy khung là mặt đất |
| `xem-thu.html` | Trang xem thử: bản cuối ở iPad ngang 1180×820 và điện thoại dọc 390×844, trước và sau khi bấm Đăng ký |
| `anh/` | Ảnh chụp kiểm 9 cỡ màn hình: `kiem-<rộng>x<cao>.png` và `kiem-<rộng>x<cao>-dang-ky.png` |

Cả đội trong khung 200×140:
- Lam (chỉ tay) ở x 98 và Ben (vẫy) ở x 152, chân y 122.
- Na (vỗ tay) ở x 125, chân y 120.
- Chồi (vẫy) ở x 180, chân y 132.
- Polly bay ở x 176, y 60 (hạ thấp từ 24/10 chiều, khi tách hai lớp).

Các vòng trước:
1. Ba thiết kế: A cả đội quanh bản đồ, B thành phố đảo khối, C xe buýt. Minh chọn A, bỏ bản đồ.
2. Sáu cảnh nền: công viên chiều cao nhất, 7 điểm.
3. Bốn phương án công viên chiều: đèn ông sao 8 điểm, thích màu trời; thuyền của bản sông Sài Gòn hay.
4. Ghép thuyền buồm, bỏ cầu và đèn, Polly sang phải.
5. Chọn trời xanh và du thuyền.

## Hai lớp (24/10 chiều, sửa lỗi cắt nhân vật trên màn rộng mà thấp)
Lỗi cũ: cả tranh là một khối phủ kín màn hình (`slice`). Trên màn rộng mà thấp như cửa sổ Mac 1524×830, khối này bị xén mất chân các bạn và đỉnh cột đèn, còn Chồi ra sát mép. Nay tranh tách thành hai lớp.

**1. Lớp nền · `nen.svg`**
- Có trời, toà Landmark, sông, du thuyền, công viên, chim. Không có nhân vật.
- `viewBox="12 26 184 78"` chính là **vùng an toàn**, phần luôn phải thấy: đỉnh Landmark, các toà nhà, sông có du thuyền, các cột đèn, mép cỏ.
- Dùng `preserveAspectRatio="xMidYMid meet"` và phủ kín màn hình. Vùng an toàn luôn hiện trọn, phần thừa của màn hình hiện tranh vẽ dư ra ngoài:
  - trời kéo lên tới y −600;
  - cỏ tràn xuống tới y 600;
  - hai bên vẽ từ x −400 tới 600.
- Vì vậy màn có tỉ lệ nào cũng kín, không có dải trống.
- Mép cỏ (chân trời gần) ở y 92.

**2. Lớp cả đội · `ca-doi.svg`**
- Có Lam, Na, Ben, Chồi, Polly, giữ dáng cũ. Nền trong suốt, bộ lọc sticker `#tc-stk` nằm sẵn trong file.
- `viewBox="78 38 120 98"` ôm sát cả nhóm, tỉ lệ 1,2245.
- **Điểm neo:** cạnh dưới khung (y 136) là mặt đất.
  - Chân Chồi ở y 132, cách đáy 4 đơn vị.
  - Chân Lam và Ben ở y 122, Na ở y 120, tức khoảng 14% chiều cao khung tính từ đáy.
- Polly bay ngay trên Ben và Chồi (tâm x 176, y 60), nằm trong khung. Trước đây Polly bay cao hơn; nay hạ xuống để khung ôm gọn.

**3. Cách đặt trong `trang-chao.html`** (CSS container query trên `.tc`)
- **Màn ngang:**
  - nền phủ kín;
  - khung chữ bên trái, rộng `--pw = min(390px, 32cqw)`, cách mép trái 3cqw;
  - lớp cả đội cách đáy 3cqh, nằm giữa vùng bên phải khung chữ (bắt đầu sau khung chữ 2cqw, chừa 3cqw ở mép phải);
  - cỡ cả đội: rộng `min(vùng còn trống, 70cqh × 1,2245)`. Màn thấp thì nhóm tự thu nhỏ theo chiều cao, cao tối đa 70% màn hình.
- **Màn dọc:**
  - tranh nền ở nửa trên, cao `--ah = 50cqh` (34cqh khi đang Đăng ký);
  - khung chữ là tấm trắng bắt đầu ở `ah − 3cqh`;
  - lớp cả đội đứng ngay trên mép tấm trắng (cách 1cqh), giữa màn hình, rộng `min(90cqw, (ah − 9cqh) × 1,2245)`.
- Kết quả: cả nhóm luôn nằm trọn trong màn hình và không bao giờ nằm dưới khung chữ. Chồi và Polly không ra ngoài mép.

**4. Chụp kiểm** (`anh/kiem-<rộng>x<cao>.png` và `-dang-ky.png`)
- Đã chụp 9 cỡ, mỗi cỡ cả trước và sau khi bấm Đăng ký: 1524×830, 1366×768, 1440×900, 1920×1080, 1280×600, iPad ngang 1180×820, iPad dọc 820×1180, điện thoại dọc 390×844, điện thoại ngang 844×390.
- Ở cả 18 ảnh, khung lớp cả đội nằm trọn trong màn hình và không chạm khung chữ (đo bằng toạ độ trên trang).
- Ở 844×390, khung chữ cao hơn màn hình nên cuộn bên trong khung.

## Bố cục chung (giống nhau ở cả ba)
- Một khối `.tc` có `container: tc / size`. Bố cục đổi theo **container query**, nên cùng một đoạn HTML chạy được cả toàn màn hình lẫn trong khung xem thử.
- **Ngang (iPad):** tranh phủ cả màn hình (`preserveAspectRatio="xMidYMid slice"`). Khung chữ trắng mờ nằm bên trái: rộng `min(390px, 32cqw)`, cách mép trái `3cqw`. Các bạn đứng ở 65% bên phải nên chữ không che mặt.
- **Dọc (điện thoại):** tranh ở trên, cao `50cqh`, cắt quanh các bạn bằng hai biến: `--R` là tỉ lệ khung tranh, `--fx` là chỗ các bạn theo chiều ngang (0,685). Khung chữ là tấm trắng bên dưới, mép trên chồm lên tranh `3cqh`.
- Thứ tự trong khung chữ:
  1. "Chồi Ơi", dòng "Toán · Khám phá · Tiếng Anh", dòng nhỏ "10 phút mỗi ngày cho bé 4–6 tuổi".
  2. Ô **Tên bé** và nút vàng to **Chơi ngay**.
  3. Ghi chú nhỏ "Tiến độ của bé được lưu trong 7 ngày."
  4. "hoặc", rồi nút phụ **Đăng ký** (viền xanh).
  5. Dòng nhỏ "Đã có tài khoản? Đăng nhập".
- **Trạng thái Đăng ký:** thêm class `dk` vào `.tc`.
  - Phần chơi thử (`.tc-try`) ẩn đi. Hiện "← Chơi thử, không cần tài khoản", tiêu đề "Tạo tài khoản" và các ô (`.tc-dk`):
    - Tên đăng nhập;
    - Tên bé;
    - Mã PIN 4 số (4 ô, tự nhảy ô);
    - Số Zalo ba mẹ.
  - Nút xanh **Tạo tài khoản**.
  - Không có năm sinh, không có email.
  - Trên điện thoại, tranh thu lại còn `34cqh` để đủ chỗ cho các ô; tranh vẫn thấy cả các bạn.
- Màu, chữ theo app: Nunito, mực `#361D46`, nút chính vàng `#FCB515`, nút xanh `#58B592`, nút phụ viền `#2A8060`.

## Chuyển động (đã làm sẵn bằng CSS, tắt khi máy bật giảm chuyển động)
- `.tc-choi`: Chồi nhún (nén xuống rồi bật lên), 1,8 giây một lần.
- `.tc-polly`: Polly bay lượn nhẹ. Hai hình `polly-bay-1` và `polly-bay-2` thay nhau 0,25 giây một lần, nên trông như vỗ cánh.
- `.tc-cloud`: mây trôi qua lại rất chậm.
- `.tc-boat`: du thuyền dập dềnh tại chỗ (không đi lại).
- Tiếng: chỉ phát sau lần chạm đầu (trình duyệt chặn tự phát), nên trang chào không có tiếng.

## Khi dựng vào app (chat U1)
- Lấy khối `.tc`, CSS và đoạn JS trong file của cảnh Minh chọn (`trang-chao.html`).
  - Nút **Chơi ngay** nối vào luồng chơi thử.
  - Nút **Tạo tài khoản** nối vào đăng ký (cột Zalo thay email, bỏ năm sinh).
  - Link **Đăng nhập** mở trang đăng nhập cũ.
- Hình trong trang là SVG nhúng sẵn, không cần tải thêm file. Riêng `#tc-stk` (bộ lọc sticker) đặt một lần trong trang.
