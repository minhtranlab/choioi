# Thư viện đồ vẽ dùng chung (`art/kit/`)

Bước đầu của thư viện đồ vẽ dùng chung cho mọi unit (22/10). Do chat **[App] Bối cảnh & hình vẽ** vẽ. Game lấy từng món đặt lên nền.

## Luật chung
- **Tỉ lệ thật: 1 m ≈ 12 đơn vị**, giống xe trong `art/props/xe/`. Game nhân cùng một hệ số cho cả xe lẫn người (ví dụ 0,9 cho vỉa hè xa trên `duong-toi-truong`), nên to nhỏ luôn đúng với nhau.
- Mỗi file là một SVG riêng, `viewBox="0 0 W H"`, **chân chạm đúng cạnh dưới** của khung. Muốn đứng trên mặt đất ở y = g thì đặt đáy hình ở g.
- Mỗi món có hai file: `-phai.svg` (mặt quay sang phải, đi từ trái sang phải) và `-trai.svg` (bản lật ngang).
- Cùng nét viền (#3A1B49) và bảng màu với các hình khác của app. Không chữ, không số, không logo, không phù hiệu, không mặt người thật.
- Mỗi id trong SVG là duy nhất trên toàn bộ `art/` (tiền tố `p195-` + tên file), nên gắn nhiều hình vào cùng một trang không bị trùng.

## `nguoi/` · người đi bộ trên vỉa hè
Tất cả đang bước đi (một chân trước, một chân sau, tay đánh ngược chân).

| Tên (thêm `-phai` / `-trai`) | Khung W×H | Ghi chú |
|---|---|---|
| `nguoi-di-bo-dat-be` | 24×20 | người lớn (khoảng 1,6 m) dắt tay một bé (khoảng 1 m); chuyển từ `art/props/nguoi/` sang đây (22/10) |
| `ba-cu-chong-gay` | 15×19 | bà cụ hơi còng, tóc bạc búi, áo tím nhạt, chống gậy, bước ngắn (khoảng 1,5 m) |
| `hoc-sinh-deo-cap` | 13×16 | bạn học sinh áo trắng, quần xanh đậm, khăn quàng đỏ nhỏ, đeo cặp cam sau lưng (khoảng 1,3 m) |
| `nguoi-doi-non-la` | 15×23 | người đội nón lá, áo xanh nhạt (khoảng 1,6 m; khung cao hơn vì chóp nón) |
| `nguoi-xach-gio-di-cho` | 15×20 | người đi chợ xách giỏ nhựa hồng có rau và đuôi cá thò ra (khoảng 1,6 m) |
