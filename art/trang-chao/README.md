# Trang chào (24/10) · ba thiết kế để Minh chọn

Đây là trang ba mẹ thấy khi mở link lần đầu. Hướng đã chốt ở `claude/chot-trang-chao-24-10.md`. Chỉ là thiết kế: chưa gắn vào `index.html`.

**Vòng 2 (24/10 trưa, góp ý của Minh):** chọn thiết kế A (bộ cả đội: Lam, Na, Ben, Polly, Chồi). Bỏ tấm bản đồ, vì bản đồ phải mở mới thấy. Đổi cảnh nền sang một trong các cảnh đẹp đã vẽ, Minh chọn một trong sáu cảnh. Bỏ B (đảo khối: chỉ là một phần của trò chơi, chưa đại diện) và C (xe buýt: nhiều thứ quá, hơi nhiễu).
Sửa chữ trong khung:
- "10 phút mỗi ngày cho bé 4–6 tuổi" xuống thành dòng nhỏ riêng, dưới "Toán · Khám phá · Tiếng Anh".
- Ghi chú dưới nút Chơi ngay chỉ còn: "Tiến độ của bé được lưu trong 7 ngày."

| File | Là gì |
|---|---|
| `xem-thu.html` | Trang xem thử cho Minh: khung chữ đã sửa (điện thoại, trước và sau khi bấm Đăng ký), rồi sáu cảnh nền, mỗi cảnh có iPad ngang 1180×820 và điện thoại dọc 390×844. Các khung bấm thử được |
| `a1.html` … `a6.html` | Từng cảnh, chạy riêng cả màn hình (thêm `?dk` vào cuối link để mở sẵn Đăng ký) |
| `anh/` | Ảnh chụp: `a1-ipad.png` … `a6-ipad.png`, `a1-dt.png` … `a6-dt.png`, và `a1-ipad-dang-ky.png`, `a1-dt-dang-ky.png` |

## Sáu cảnh nền (cả đội đứng ở cùng một chỗ trên mặt đất phía trước)
| | File | Cảnh | Lấy từ |
|---|---|---|---|
| 1 | `a1.html` | Bãi biển đảo hải đăng: bãi cát có cầu tàu, đồi xanh, hải đăng trên đỉnh | `dao-bai-cat-hai-dang` (Màn 7) |
| 2 | `a2.html` | Đảo hải đăng: đảo cát, đồi tròn, hải đăng đỏ trắng, cầu gỗ, cây dừa | `dao-hai-dang` (Màn 7) |
| 3 | `a3.html` | Đồi lên hải đăng: đồi xanh, đường mòn uốn lên hải đăng | `duong-len-hai-dang` (Màn 7) |
| 4 | `a4.html` | Bãi cát hàng dừa | `dao-bai-cat` (Màn 7) |
| 5 | `a5.html` | Công viên chiều ven sông, thành phố xa | `cong-vien-chieu` (Màn 6) |
| 6 | `a6.html` | Vườn nhà Na đêm trăng sao | `vuon-nha-na-dem` (Màn 2) |

Bố cục cả đội trong khung 200×140:
- Lam (chỉ tay) ở x 98 và Ben (vẫy) ở x 152, chân y 122.
- Na (vỗ tay) ở x 125, chân y 120.
- Chồi (nhún) ở x 180, chân y 132.
- Polly bay khoảng y 30, x 96–132 tuỳ cảnh, để không che hải đăng hay mặt trăng.

## Bố cục chung (giống nhau ở cả ba)
- Một khối `.tc` có `container: tc / size`. Bố cục đổi theo **container query**, nên cùng một đoạn HTML chạy được cả toàn màn hình lẫn trong khung xem thử.
- **Ngang (iPad):** tranh phủ cả màn hình (`preserveAspectRatio="xMidYMid slice"`). Khung chữ trắng mờ nằm bên trái: rộng `min(390px, 32cqw)`, cách mép trái `3cqw`. Các bạn đứng ở 65% bên phải nên chữ không che mặt.
- **Dọc (điện thoại):** tranh ở trên, cao `50cqh`, cắt quanh các bạn bằng hai biến: `--R` là tỉ lệ khung tranh, `--fx` là chỗ các bạn theo chiều ngang (0,685 cho cả sáu cảnh). Khung chữ là tấm trắng bên dưới, mép trên chồm lên tranh `3cqh`.
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
- Tiếng: chỉ phát sau lần chạm đầu (trình duyệt chặn tự phát), nên trang chào không có tiếng.

## Khi dựng vào app (chat U1)
- Lấy khối `.tc`, CSS và đoạn JS trong file của cảnh Minh chọn (`a1.html` … `a6.html`).
  - Nút **Chơi ngay** nối vào luồng chơi thử.
  - Nút **Tạo tài khoản** nối vào đăng ký (cột Zalo thay email, bỏ năm sinh).
  - Link **Đăng nhập** mở trang đăng nhập cũ.
- Hình trong trang là SVG nhúng sẵn, không cần tải thêm file. Riêng `#tc-stk` (bộ lọc sticker) đặt một lần trong trang.
