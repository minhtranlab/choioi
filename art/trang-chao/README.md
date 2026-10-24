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

**Vòng 5 (24/10, 13:21, Minh):** chọn màu trời và loại thuyền. Các trang thử nằm trong `chon/`.
- Màu trời, cùng thuyền buồm:
  - `troi-tim.html`: chiều tím hồng, màu đang dùng;
  - `troi-cam.html`: hoàng hôn cam vàng;
  - `troi-hong.html`: hồng phấn;
  - `troi-lam.html`: chạng vạng xanh;
  - `troi-xanh.html`: trời xanh ban ngày.
- Thuyền, cùng trời tím: `thuyen-buom.html`, `thuyen-du.html` (du thuyền), `thuyen-cont.html` (tàu container).
- Ảnh chụp: `anh/<tên>-ipad.png`, `anh/<tên>-dt.png`.
- Ghép được bất kỳ màu trời nào với bất kỳ thuyền nào (`sceneParkFinal(trời, thuyền)` trong script vẽ). Khi Minh chọn xong, `trang-chao.html` sẽ được làm lại theo lựa chọn.

| File | Là gì |
|---|---|
| `xem-thu.html` | Trang xem thử: bản cuối ở iPad ngang 1180×820 và điện thoại dọc 390×844, trước và sau khi bấm Đăng ký |
| `trang-chao.html` | Bản cuối chạy riêng cả màn hình; thêm `?dk` vào cuối link để mở sẵn Đăng ký |
| `anh/` | `ipad.png`, `ipad-dang-ky.png`, `dt.png`, `dt-dang-ky.png` |

Cả đội trong khung 200×140:
- Lam (chỉ tay) ở x 98 và Ben (vẫy) ở x 152, chân y 122.
- Na (vỗ tay) ở x 125, chân y 120.
- Chồi (vẫy) ở x 180, chân y 132.
- Polly bay ở x 162, khoảng y 30.

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
- `.tc-boat`: thuyền dập dềnh tại chỗ (không đi lại).
- Tiếng: chỉ phát sau lần chạm đầu (trình duyệt chặn tự phát), nên trang chào không có tiếng.

## Khi dựng vào app (chat U1)
- Lấy khối `.tc`, CSS và đoạn JS trong file của cảnh Minh chọn (`trang-chao.html`).
  - Nút **Chơi ngay** nối vào luồng chơi thử.
  - Nút **Tạo tài khoản** nối vào đăng ký (cột Zalo thay email, bỏ năm sinh).
  - Link **Đăng nhập** mở trang đăng nhập cũ.
- Hình trong trang là SVG nhúng sẵn, không cần tải thêm file. Riêng `#tc-stk` (bộ lọc sticker) đặt một lần trong trang.
