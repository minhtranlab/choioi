# Chồi Ơi · Hướng dẫn cho admin

Tài liệu này để admin (Fun Academy) mở lại sau một thời gian là nhớ ngay: app gồm những gì, gửi gì cho phụ huynh, phụ huynh đăng ký thế nào, xem kết quả của các bé ở đâu, và gặp sự cố thì làm gì.

---

## 1. App gồm những gì

| Thành phần | Ở đâu | Dùng để làm gì |
|---|---|---|
| **App cho bé** | `https://minhtranlab.github.io/choioi/` (GitHub Pages của repo này) | Link gửi cho phụ huynh. Bé chơi trên iPad / điện thoại / máy tính. |
| **Mã nguồn** | Repo `github.com/minhtranlab/choioi` | `index.html` (toàn bộ app), `voice/` (giọng Chồi), `music/`, `apps-script/Code.gs` (máy chủ Google Sheet). |
| **Google Sheet** | Trong Google Drive của admin | Lưu tài khoản và tiến độ của mọi bé; có sẵn các bảng báo cáo. |
| **Apps Script** | Gắn vào Google Sheet (Tiện ích mở rộng → Apps Script) | Nhận dữ liệu từ app, ghi vào Sheet, trả tiến độ khi bé đăng nhập ở máy khác. |

Tiến độ luôn được lưu trên máy của bé trước, vài giây sau mới gửi lên Sheet. Mất mạng thì bé vẫn chơi được; có mạng lại thì app tự gửi.

---

## 2. Cài Google Sheet (chỉ làm một lần)

1. Vào Google Drive → **Mới → Google Trang tính**. Đặt tên, ví dụ "Chồi Ơi · Học sinh".
2. Trong Sheet: **Tiện ích mở rộng → Apps Script**. Xoá hết mã có sẵn, dán toàn bộ nội dung `apps-script/Code.gs`, bấm **Lưu**.
3. Ở thanh trên cùng của Apps Script chọn hàm **`setupSheets`** → **Chạy**. Lần đầu Google hỏi quyền: chọn tài khoản → *Nâng cao* → *Đi tới … (không an toàn)* → **Cho phép**. Đây là mã của chính mình nên cho phép được.
   Sau bước này Sheet có các bảng **Hướng dẫn, Báo cáo, Theo kỹ năng, Accounts, Progress**. Tải lại Sheet sẽ thấy menu **Chồi Ơi**.
4. **Triển khai → Tùy chọn triển khai mới** → bánh răng → **Ứng dụng web**.
   - *Thực thi với tư cách*: **Tôi**
   - *Người có quyền truy cập*: **Bất kỳ ai**
   - Bấm **Triển khai**, sao chép **URL ứng dụng web** (kết thúc bằng `/exec`).
5. Đưa địa chỉ `/exec` vào app. Có hai cách:
   - **Nên làm:** gửi địa chỉ cho Claude (hoặc tự sửa `index.html`, dòng `const SYNC_URL_DEFAULT=''`, dán địa chỉ vào giữa hai dấu nháy), rồi đẩy lên GitHub. Từ đó máy nào mở app cũng tự kết nối.
   - Tạm thời: trên từng máy, vào **Settings → Tài khoản → Địa chỉ Google Sheet**, dán địa chỉ.
6. Kiểm tra: mở link app, đăng ký thử một bé, chơi một chút, quay lại Sheet. Bảng **Accounts** có một dòng mới, **Báo cáo** có tên bé.

> **Lưu ý khi sửa mã Apps Script sau này:** vào **Triển khai → Quản lý các bản triển khai** → bút chì → *Phiên bản*: **Phiên bản mới** → **Triển khai**. Làm như vậy địa chỉ `/exec` giữ nguyên.
> Nếu bấm *Tùy chọn triển khai mới* thì sẽ có địa chỉ khác, và các máy đang dùng địa chỉ cũ không gửi được nữa.

---

## 3. Gửi app cho phụ huynh

Chỉ gửi **link app**. **Không** gửi link Google Sheet (trong Sheet có email của mọi người).

### Tin nhắn mẫu (sao chép rồi gửi)

> Chào anh/chị, Fun Academy gửi app **"Chồi Ơi"** để bé lớp Chồi chơi và học ở nhà (Toán, Khám phá thế giới, Tiếng Anh), đi cùng chương trình ở lớp.
>
> 1. Mở link: **https://minhtranlab.github.io/choioi/**
>    Trên iPad / iPhone: bấm nút Chia sẻ → **Thêm vào MH chính** để mở như một app.
> 2. Chọn **Đăng ký**, điền tên bé, năm sinh, **tên đăng nhập** (chữ thường không dấu, ví dụ `bin2021`), **mã PIN 4 số** và email của anh/chị.
> 3. Ghi nhớ tên đăng nhập và PIN để mở trên máy khác: chọn **Đăng nhập** là tiến độ của bé tự tải về.
>
> Mỗi ngày bé chơi khoảng 10–15 phút là đủ. Trang dành cho ba mẹ (xem tiến độ, đổi ngôn ngữ, bật micro): nhấn giữ nút **Progress** hoặc **Settings** khoảng 1 giây. Cần hỗ trợ, anh/chị nhắn lại cho Fun Academy nhé.

---

## 4. Đăng ký hoạt động thế nào

- **Phụ huynh tự đăng ký** ngay trong app. Admin không cần làm gì, không cần duyệt. Tài khoản xuất hiện trong Sheet ngay khi đăng ký xong.
- **Admin đăng ký hộ** (khi phụ huynh nhờ):
  1. Mở link app, chọn Đăng ký, điền thông tin của bé.
  2. Vào **Settings → Đăng xuất** để máy của admin không giữ tài khoản của bé.
  3. Gửi **tên đăng nhập + PIN** cho phụ huynh. Phụ huynh mở link, chọn **Đăng nhập**.
- **Chơi thử** (nút "Chơi thử, không cần tài khoản"): tiến độ chỉ lưu trên máy đó, Sheet không biết gì. Sau này vào **Settings → Tạo tài khoản để lưu tiến độ** thì phần đã chơi được giữ và gửi lên.
- **Mỗi tài khoản là một bé.** Nhà có hai bé thì đăng ký hai tên đăng nhập; email có thể trùng.
- **Tên đăng nhập không đổi được** sau khi tạo. Tên bé thì đổi được trong Settings.

---

## 5. Xem kết quả của các bé

Mở Google Sheet. Báo cáo tự cập nhật mỗi khi một bé chơi. Muốn làm mới ngay: menu **Chồi Ơi → Cập nhật báo cáo**.

| Bảng | Có gì |
|---|---|
| **Báo cáo** | Phía trên là số liệu chung: số bé đã đăng ký, số bé chơi trong 7 ngày qua, trung bình số màn đã xong, tỉ lệ đúng chung. Bên dưới mỗi bé một dòng: đang học màn nào, số màn đã xong (/8), mảnh bản đồ, số ngày đã chơi, phút chơi 7 ngày qua, số kỹ năng đã vững / đang luyện / chưa học, tỉ lệ đúng, **kỹ năng nên ôn thêm** (dưới 75%, yếu nhất trước), số kỹ năng đến hạn ôn, số lần chơi Fun Mix. Sắp xếp: bé chơi gần đây nhất ở trên. |
| **Theo kỹ năng** | Mỗi kỹ năng một dòng: bao nhiêu bé đã vững, đang luyện, chưa học, tổng lượt, tỉ lệ đúng. Dùng để biết phần nào các bé hay vấp, cần dạy thêm ở lớp. |
| **Accounts** | Dữ liệu tài khoản. **Đừng sửa tay** cột `pin_hash` và `state_1 … state_8` (toàn bộ tiến độ của bé). |
| **Progress** | Chi tiết từng bé × từng kỹ năng. |
| **Hướng dẫn** | Bản tóm tắt của tài liệu này, nằm ngay trong Sheet. |

**Trạng thái kỹ năng:** `got_it` = đã vững (ít nhất 4 lượt và đúng từ 80% trở lên, trong 2 ngày khác nhau), `practising` = đang luyện, `not_yet` = chưa học, `spoken` = đã nói theo (kỹ năng nói), `assigned` = đã giao làm ở nhà.

**Ôn tập (Fun Mix):** mỗi kỹ năng có lịch ôn 3 → 7 → 21 ngày. Bé làm đúng vào ngày ôn thì kỹ năng lên bậc; làm sai thì kỹ năng quay về "ôn ngay". Cột *Kỹ năng đến hạn ôn* đếm số kỹ năng đã tới ngày ôn.

---

## 6. Việc thường gặp

| Việc | Cách làm |
|---|---|
| Phụ huynh **quên PIN** | Sheet → menu **Chồi Ơi → Đặt lại mã PIN cho một bé** → nhập tên đăng nhập và PIN mới → gửi PIN mới cho phụ huynh. Admin không xem được PIN cũ (Sheet chỉ lưu mã băm). |
| **Nhập sai PIN quá nhiều** | Sai 10 lần thì tài khoản khoá 15 phút. Đợi 15 phút, hoặc đặt lại PIN (mở khoá ngay). |
| Phụ huynh **quên tên đăng nhập** | Tìm theo email hoặc tên bé trong bảng **Báo cáo** / **Accounts**. |
| **Xoá một bé** | Xoá dòng của bé ở **Accounts** và các dòng của bé ở **Progress**, rồi menu **Chồi Ơi → Cập nhật báo cáo**. |
| **"Chơi thử" bị mất tiến độ** | "Chơi thử" chỉ lưu tiến độ trên máy đó. Safari có thể xoá dữ liệu của trang không được mở trong 7 ngày (trừ khi đã Thêm vào MH chính). Dặn phụ huynh tạo tài khoản (**Settings → Tạo tài khoản để lưu tiến độ**), hoặc Thêm vào MH chính. |
| **Đổi máy / cài lại** | Mở link → **Đăng nhập** → tên đăng nhập + PIN. Riêng các đoạn ghi âm giọng bé chỉ nằm trên máy cũ. |
| **Sheet không có dữ liệu mới** | (1) App đã có địa chỉ `/exec` chưa: Settings → Tài khoản. (2) Bản triển khai có để *Bất kỳ ai* không. (3) Có lỡ tạo bản triển khai mới (địa chỉ đổi) không. (4) Mở link app trên GitHub Pages, không mở trong claude.ai: trang xem trước của claude.ai có thể chặn kết nối tới Google. |
| **Màn chờ khi mở lần đầu** | Trước mỗi bài, app chỉ chờ phần giọng đầu bài (tiếng Anh khoảng 2 MB, tiếng Việt khoảng 1,6 MB): Wi-Fi gần như ngay, 4G chậm khoảng 5–8 giây. Màn chờ có thanh báo "Đang tải giọng nói của bài" kèm bóng bay, và trò chạm bong bóng. Phần còn lại tải trong lúc bé chơi. Giọng đã tải được giữ trong máy, mở lại không tải lại. Không cần dặn phụ huynh trước. |
| **Có câu chỉ hiện chữ, không có tiếng** | App không bao giờ đọc cả bài bằng giọng máy. Câu nào chưa tải kịp (mạng rất yếu hoặc mất mạng giữa chừng) thì hiện chữ, app vẫn tải tiếp, các câu sau có tiếng khi tải xong. Bật Wi-Fi hoặc chờ mạng ổn rồi chơi tiếp. |
| **Mở trong Zalo không có tiếng / mất tiến độ** | Dặn phụ huynh mở bằng Safari/Chrome (trong Zalo: "…" → "Mở bằng trình duyệt"), rồi **Thêm vào MH chính**. |

---

## 7. Cập nhật app

1. Sửa và kiểm tra app (cùng Claude trong project "3 - App Tích hợp").
2. Đẩy `index.html`, `voice/`, `music/` mới lên repo này (nhánh `main`). GitHub Pages tự cập nhật sau 1–2 phút.
3. Nếu `apps-script/Code.gs` thay đổi: dán lại vào Apps Script → Lưu → **Quản lý các bản triển khai → Phiên bản mới** (giữ địa chỉ cũ) → chạy `setupSheets` một lần để làm mới bảng Hướng dẫn và Báo cáo.

**Bật GitHub Pages (nếu chưa bật):** repo → Settings → Pages → Source: *Deploy from a branch* → Branch: `main`, thư mục `/ (root)` → Save.

---

## 8. Quyền riêng tư

- Phụ huynh chỉ cần link app; không ai ngoài admin có quyền mở Google Sheet.
- PIN không bao giờ được gửi đi; app chỉ gửi mã băm SHA-256.
- Ai biết địa chỉ `/exec` cũng chỉ đăng ký được tài khoản mới hoặc mở tài khoản mà họ biết tên đăng nhập **và** PIN.
- Ghi âm giọng bé (khi bé nói vào micro) chỉ lưu trên máy của bé, không gửi lên Sheet.
