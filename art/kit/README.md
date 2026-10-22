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

## `nhan-vat/` · đội bạn nhỏ (22/10, Minh đã duyệt)
Khác với `nguoi/`: các bạn vẽ **theo cỡ nhân vật của app**, không theo tỉ lệ 1 m ≈ 12 đơn vị. Nét và khung giống hình các bạn đang có trong app (`kidSVG`, `mascotSVG`, `pollySVG`), nên thay thẳng được.

Mỗi bạn một thư mục: `choi/`, `lam/`, `na/`, `ben/`, `polly/`. Tên file: `<bạn>-<tư thế>-phai.svg` và `-trai.svg` (bản lật ngang). Mọi tư thế của một bạn **cùng khung, cùng chỗ chân**, nên đổi tư thế chỉ cần đổi file, không dời chỗ.

| Bạn | Khung | Chân / đáy | Trang phục (màu riêng, giữ suốt app) | Đồ riêng (đeo, chỉ cầm khi dùng) |
|---|---|---|---|---|
| Chồi | 120×140 | đáy thân y 137 | mầm cây xanh như trong app | — |
| Lam | 200×260 | đế giày y 246 | áo thám hiểm xanh lá không tay (cổ áo, 2 túi), quần soóc kaki, mũ thám hiểm băng xanh lá, giày nâu | ống nhòm đeo dây trước ngực |
| Na | 200×260 | đế giày y 246 | váy yếm cam đỏ không tay, tóc đuôi ngựa buộc dây xanh, giày hồng | kính lúp đeo dây trên ngực |
| Ben | 200×260 | đế giày y 246 | áo xanh dương có tay, quần soóc kaki, kính tròn, giày trắng | túi nhỏ đeo chéo, bản đồ cuộn ló ra khỏi túi |
| Polly | 200×260 | chân y 252 | vẹt xanh lá, cánh xanh dương, mào đỏ | — |

**Tư thế của Chồi, Lam, Na, Ben** (13): `dung` đứng · `vay-chao` vẫy chào · `vo-tay-mo` vỗ tay, hai tay mở · `vo-tay-cham` vỗ tay, hai tay chạm · `chi-tay` chỉ tay sang phải (bản `-trai` chỉ sang trái) · `cam-do` hai tay ngang bụng để cầm đồ · `nhay` nhảy vui · `buon` buồn cúi đầu · `ngoi` ngồi · `ngu` nằm ngủ có chăn · `buoc-1`, `buoc-2` hai tư thế bước (mặt quay theo hướng đi; thay phiên là thành dáng đi) · `deo-huy-chuong` đeo huy chương vàng.

**Tư thế của Polly** (5): `dung` · `noi` (mở mỏ) · `bay-1`, `bay-2` (bay như hiệu ứng trong app: thân nhấc lên, chân co, chỉ cánh vỗ; `bay-2` cánh hất lên 28°) · `deo-huy-chuong`.

**Toạ độ để game đặt đồ** (khung của từng bạn):
- `cam-do` (Lam, Na, Ben): hai bàn tay ở (93, 188) và (107, 188); tâm đồ cầm khoảng (100, 182), đặt đồ trước người, cao không quá y 150 để không che mặt. Chồi: hai tay ở (53, 120) và (67, 120), tâm đồ khoảng (60, 116).
- `chi-tay`: đầu ngón tay ở (191, 150) (Chồi: (131, 94)).
- Huy chương: tâm huy chương Lam, Na, Ben (100, 188); Chồi (60, 122); Polly (100, 180).
- `ngu`: nằm ngang trong cùng khung, đầu ở bên trái (bản `-phai`).

## `do-vat/` · đồ vật (22/10)
Cùng luật chung: 1 m ≈ 12 đơn vị, chân chạm cạnh dưới, có `-phai` / `-trai`.

| Tên (thêm `-phai` / `-trai`) | Khung W×H | Ghi chú |
|---|---|---|
| `da-to-dau-x` | 64×30 | Màn 7 · trạm cuối của con cua: hòn đá to xám (x 3–46) và **dấu X đỏ vẽ trên cát ngay cạnh, tâm (56, 26)** (bản `-trai`: tâm (8, 26)) |
| `bang-go-mui-ten` | 26×28 | Màn 7 · bảng gỗ hình mũi tên cắm trên cát, dùng sau mỗi trạm ("đi lối này"); `-phai` mũi tên chỉ sang phải |
| `bang-go-hang` | 30×32 | Màn 7 · bảng gỗ cắm cạnh dấu X, vẽ một mũi tên đỏ và hình cái hang (không chữ) |
