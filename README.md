# Chồi Ơi — app đồng hành lớp Chồi (bản thử)

App chơi tại nhà cho bé 4–5 tuổi, Chương 1 "Me and My Feelings" (Fun Academy), theo giáo trình lớp Chồi (Toán, Khám phá thế giới, Tiếng Anh).

**Admin: xem [ADMIN.md](ADMIN.md)**: cài Google Sheet, link và tin nhắn mẫu gửi phụ huynh, cách đăng ký, đọc báo cáo, đặt lại PIN, xử lý sự cố.

- Mở `index.html` qua GitHub Pages (hoặc bất kỳ máy chủ web tĩnh nào). Không cần cài đặt.
- `voice/`: giọng Chồi ghi âm sẵn (tiếng Anh: Kokoro "sky"; tiếng Việt: Piper "vais1000"). Thiếu file thì app tự dùng giọng của máy.
- `music/`: nhạc cho trò nghe nhạc đoán cảm xúc.
- Trang ba mẹ: nhấn giữ nút Progress hoặc Settings 1 giây.

## Tài khoản và lưu tiến độ
- Lần đầu mở app: trang chào (tranh cả đội ở công viên ven sông). **Chơi ngay** (ô Tên bé: chơi thử, chỉ lưu trên máy, vào Màn 0 luôn), **Đăng ký** (tên đăng nhập, tên bé, mã PIN 4 số, số Zalo ba mẹ; không hỏi năm sinh, email), hoặc **Đã có tài khoản? Đăng nhập**. Lần mở sau vào thẳng bản đồ; Settings → Đăng xuất thì hiện lại trang chào.
- Tiến độ luôn lưu trên máy, và được gửi lên Google Sheet nếu app có địa chỉ máy chủ (Apps Script). Đăng nhập ở máy khác thì tiến độ được tải về.
- Mã PIN không được gửi đi: app chỉ gửi mã băm SHA-256. Sai PIN 10 lần thì tài khoản bị khoá 15 phút.

### Cài Google Sheet (làm một lần)
1. Tạo một Google Sheet mới → Tiện ích mở rộng → Apps Script, dán toàn bộ `apps-script/Code.gs`.
2. Triển khai → Tùy chọn triển khai mới → loại "Ứng dụng web"; Thực thi với tư cách: Tôi; Người có quyền truy cập: Bất kỳ ai → Triển khai.
3. Lấy địa chỉ kết thúc bằng `/exec`, nhập vào app ở Settings → Tài khoản (hoặc mục "Máy chủ" trên trang đăng ký). Có thể đặt sẵn trong `index.html` ở dòng `const SYNC_URL_DEFAULT=''`.
4. Chạy hàm `setupSheets` một lần: Sheet có các bảng **Hướng dẫn**, **Báo cáo** (mỗi bé một dòng, số liệu chung ở trên), **Theo kỹ năng**, **Accounts**, **Progress**, và menu **Chồi Ơi** (cập nhật báo cáo, đặt lại PIN). Chi tiết trong ADMIN.md.

## Đưa lên GitHub Pages
1. Settings → Pages → Build and deployment → Source: "Deploy from a branch" → Branch: `main`, thư mục `/ (root)` → Save.
2. Sau 1–2 phút, link sẽ là `https://<tên-tài-khoản>.github.io/<tên-repo>/`.
