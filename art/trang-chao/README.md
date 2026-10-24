# Trang chào (24/10) · ba thiết kế để Minh chọn

Đây là trang ba mẹ thấy khi mở link lần đầu. Hướng đã chốt ở `claude/chot-trang-chao-24-10.md`. Chỉ là thiết kế: chưa gắn vào `index.html`.

| File | Là gì |
|---|---|
| `xem-thu.html` | Trang xem thử cho Minh: cả ba thiết kế, mỗi cái có khung iPad ngang 1180×820 và điện thoại dọc 390×844, trước và sau khi bấm **Đăng ký**. Các khung bấm thử được |
| `a.html` | Thiết kế **A · Bản đồ kho báu**, chạy riêng cả màn hình (thêm `?dk` vào cuối link để mở sẵn trạng thái Đăng ký) |
| `b.html` | Thiết kế **B · Thành phố đảo khối** |
| `c.html` | Thiết kế **C · Xe buýt tới trường** |
| `anh/` | Ảnh chụp: `<a/b/c>-ipad.png`, `-ipad-dang-ky.png`, `-dt.png` (điện thoại), `-dt-dang-ky.png` |

## Ba ý
- **A · Bản đồ kho báu:** Lam, Na, Ben quanh tấm bản đồ 8 mảnh trải trên cỏ; Chồi nhún nhảy bên cạnh; Polly bay về phía Đảo Kho Báu ở xa (đảo có dấu X: đây là X duy nhất, đúng luật một dấu X). Ý: phiêu lưu, mỗi ngày một mảnh bản đồ.
- **B · Thành phố đảo khối:** nhìn từ trên cao theo đúng kiểu đảo khối của app (code đảo, cầu, cây lấy từ `isoIsland`, `isoBridge`, `isoTree`; thú lấy từ `zAnimal`). Có các đảo: sở thú, sân chơi, cây sao của Chồi (12 sao sáng), trường, bãi biển có hải đăng. Cả đội đứng ở đảo giữa. Ý: một thế giới lớn dần cùng bé.
- **C · Xe buýt tới trường:** xe cận cảnh `xe-dua-don-can-mo` đỗ trước cổng trường (`cong-vao-truong-tron`). Bốn ô cửa sổ, mỗi ô một bạn: Ben, Na, Lam và Chồi ngồi sát bác tài. Bác tài vẫy, Polly bay trên xe. Ý: đi học vui, gần đời thật.

Tranh ghép từ `art/kit/` và `art/places/`, đúng kiểu vẽ của app. Các bạn là sticker: viền trắng và bóng tím mờ, bộ lọc `#tc-stk`.

## Bố cục chung (giống nhau ở cả ba)
- Một khối `.tc` có `container: tc / size`. Bố cục đổi theo **container query**, nên cùng một đoạn HTML chạy được cả toàn màn hình lẫn trong khung xem thử.
- **Ngang (iPad):** tranh phủ cả màn hình (`preserveAspectRatio="xMidYMid slice"`). Khung chữ trắng mờ nằm bên trái: rộng `min(390px, 32cqw)`, cách mép trái `3cqw`. Các bạn đứng ở 65% bên phải nên chữ không che mặt.
- **Dọc (điện thoại):** tranh ở trên, cao `50cqh`, cắt quanh các bạn bằng hai biến: `--R` là tỉ lệ khung tranh, `--fx` là chỗ các bạn theo chiều ngang (A 0,68 · B 0,62 · C 0,66). Khung chữ là tấm trắng bên dưới, mép trên chồm lên tranh `3cqh`.
- Thứ tự trong khung chữ:
  1. "Chồi Ơi" và dòng cho ba mẹ.
  2. Ô **Tên bé** và nút vàng to **Chơi ngay**.
  3. Ghi chú nhỏ "Chơi thử lưu trên máy này. Không mở 7 ngày có thể mất. Tạo tài khoản để giữ tiến độ."
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
- B: `.tc-star`, 12 ngôi sao trên cây sao lấp lánh so le.
- C: `.tc-bus`, xe rung rất nhẹ như đang nổ máy.
- Tiếng: chỉ phát sau lần chạm đầu (trình duyệt chặn tự phát), nên trang chào không có tiếng.

## Khi dựng vào app (chat U1)
- Lấy khối `.tc`, CSS và đoạn JS trong file của thiết kế đã chọn (`a.html`, `b.html` hoặc `c.html`).
  - Nút **Chơi ngay** nối vào luồng chơi thử.
  - Nút **Tạo tài khoản** nối vào đăng ký (cột Zalo thay email, bỏ năm sinh).
  - Link **Đăng nhập** mở trang đăng nhập cũ.
- Hình trong trang là SVG nhúng sẵn, không cần tải thêm file. Riêng `#tc-stk` (bộ lọc sticker) đặt một lần trong trang.
