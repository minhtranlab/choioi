# Trang chào (24/10) · ba thiết kế để Minh chọn

Đây là trang ba mẹ thấy khi mở link lần đầu. Hướng đã chốt ở `claude/chot-trang-chao-24-10.md`. Chỉ là thiết kế: chưa gắn vào `index.html`.

**Vòng 2 (24/10 trưa, góp ý của Minh):** chọn thiết kế A (bộ cả đội: Lam, Na, Ben, Polly, Chồi). Bỏ tấm bản đồ, vì bản đồ phải mở mới thấy. Đổi cảnh nền sang một trong các cảnh đẹp đã vẽ, Minh chọn một trong sáu cảnh. Bỏ B (đảo khối: chỉ là một phần của trò chơi, chưa đại diện) và C (xe buýt: nhiều thứ quá, hơi nhiễu).
Sửa chữ trong khung:
- "10 phút mỗi ngày cho bé 4–6 tuổi" xuống thành dòng nhỏ riêng, dưới "Toán · Khám phá · Tiếng Anh".
- Ghi chú dưới nút Chơi ngay chỉ còn: "Tiến độ của bé được lưu trong 7 ngày."

**Vòng 3 (24/10, 12:44):** Minh chấm sáu cảnh nền như sau.

| Cảnh | Điểm |
|---|---|
| Bãi biển đảo hải đăng | 6 |
| Đảo hải đăng | 6 |
| Đồi lên hải đăng | 5 |
| Bãi cát hàng dừa | 5 |
| **Công viên chiều** | **7** (cần thêm chi tiết cho hấp dẫn) |
| Vườn nhà Na đêm trăng | 6 |

Khung chữ: Minh đồng ý. Ở vòng này, công viên chiều được phát triển thành bốn phương án. Chồi đổi sang dáng vẫy tay, vì dáng nhảy có hai vạch dưới chân trông như hai cục.

| File | Là gì |
|---|---|
| `xem-thu.html` | Trang xem thử: khung chữ (điện thoại, trước và sau khi bấm Đăng ký), rồi bốn phương án công viên chiều, mỗi phương án có iPad ngang 1180×820 và điện thoại dọc 390×844 |
| `cv1.html` | **Thả diều:** trời hoàng hôn hồng cam, ba con diều, đàn chim nhỏ |
| `cv2.html` | **Đèn ông sao:** chiều tím, dây đèn màu giăng ngang trời, cửa sổ toà nhà lên đèn, Polly mang đèn ông sao, đốm sáng lấp lánh |
| `cv3.html` | **Bóng bay và bong bóng:** Chồi cầm chùm bóng bay, bong bóng xà phòng bay lơ lửng |
| `cv4.html` | **Sông Sài Gòn:** cầu dây văng xa xa, thuyền buồm trên sông, cửa sổ lên đèn, đàn chim |
| `anh/` | Ảnh chụp `cv1-ipad.png` … `cv4-ipad.png`, `cv1-dt.png` … `cv4-dt.png`, `cv1-ipad-dang-ky.png`, `cv1-dt-dang-ky.png` |

Mỗi file chạy riêng cả màn hình; thêm `?dk` vào cuối link để mở sẵn Đăng ký. Nền là `places/cong-vien-chieu.svg`: dải trời hoàng hôn thay cho nền trời một màu, các chi tiết thêm vẽ chồng lên. Không có mặt trời, không có chữ.

Cả đội đứng ở cùng một chỗ trong khung 200×140:
- Lam (chỉ tay) ở x 98 và Ben (vẫy) ở x 152, chân y 122.
- Na (vỗ tay) ở x 125, chân y 120.
- Chồi (vẫy) ở x 180, chân y 132.
- Polly bay khoảng y 30.

## Bố cục chung (giống nhau ở cả ba)
- Một khối `.tc` có `container: tc / size`. Bố cục đổi theo **container query**, nên cùng một đoạn HTML chạy được cả toàn màn hình lẫn trong khung xem thử.
- **Ngang (iPad):** tranh phủ cả màn hình (`preserveAspectRatio="xMidYMid slice"`). Khung chữ trắng mờ nằm bên trái: rộng `min(390px, 32cqw)`, cách mép trái `3cqw`. Các bạn đứng ở 65% bên phải nên chữ không che mặt.
- **Dọc (điện thoại):** tranh ở trên, cao `50cqh`, cắt quanh các bạn bằng hai biến: `--R` là tỉ lệ khung tranh, `--fx` là chỗ các bạn theo chiều ngang (0,685 cho mọi phương án). Khung chữ là tấm trắng bên dưới, mép trên chồm lên tranh `3cqh`.
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
- `.tc-kite`: diều đung đưa. `.tc-bob`: bóng bay, bong bóng lơ lửng. `.tc-star`, `.tc-glow`: đèn lấp lánh. `.tc-boat`: thuyền nhấp nhô.
- Tiếng: chỉ phát sau lần chạm đầu (trình duyệt chặn tự phát), nên trang chào không có tiếng.

## Khi dựng vào app (chat U1)
- Lấy khối `.tc`, CSS và đoạn JS trong file của cảnh Minh chọn (`cv1.html` … `cv4.html`).
  - Nút **Chơi ngay** nối vào luồng chơi thử.
  - Nút **Tạo tài khoản** nối vào đăng ký (cột Zalo thay email, bỏ năm sinh).
  - Link **Đăng nhập** mở trang đăng nhập cũ.
- Hình trong trang là SVG nhúng sẵn, không cần tải thêm file. Riêng `#tc-stk` (bộ lọc sticker) đặt một lần trong trang.
