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

**Thêm cho Lam và Ben:** `khieng-1`, `khieng-2` (22/10 tối) · khiêng rương: dáng bước đi như `buoc-1`/`buoc-2`, mặt quay theo hướng đi, hai tay đưa ra trước ngang bụng để đỡ vật; **hai bàn tay ở (144, 190) và (158, 188)** (bản `-phai`; bản `-trai` lật: (56, 190), (42, 188)). Rương đặt giữa hai bạn, cạnh trên rương khoảng y 184 của khung.

**Thêm cho Ben:** `ben-ngu-tui-ngu` · Ben ngủ trong túi ngủ xanh lá (22/10, thay cảnh xoay người + tấm chăn cũ): nằm dưới đất, đầu nằm nghiêng trong mũ trùm (đỉnh đầu về bên trái), túi kéo tới cằm, zzz. Cùng khung 200×260, đáy y 246; túi trống là `do-vat/tui-ngu`.

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
| `huy-chuong-vang` | 40×58 | Kho báu · một huy chương vàng có dây đỏ đeo cổ (vòng dây ở trên, đĩa vàng có ngôi sao, tâm đĩa (20, 44)). Cùng kiểu với huy chương trong tư thế `deo-huy-chuong` của các bạn, nên bay tới cổ bạn nào thì đổi sang tư thế đó. **Đồ cận, không theo tỉ lệ 12 đơn vị/m** |
| `chia-khoa-vang` | 52×22 | Kho báu · chìa khoá vàng (vòng tròn bên trái, răng chìa bên phải). Đồ cận |
| `ruong-kho-bau-dong` | 64×48 | Kho báu · rương gỗ đóng, đai vàng, ổ khoá giữa (lỗ khoá ở (32, 24)). Đồ cận |
| `ruong-kho-bau-mo` | 64×60 | Kho báu · rương mở: nắp lật ra sau, ánh vàng, **5 huy chương vàng** và chìa khoá vàng nằm trên. Đồ cận; đáy ở cạnh dưới giống rương đóng, nên đổi file là mở rương |
| `da-nho` | 34×16 | Màn 7 · tảng đá nhỏ trên bãi cát, có ít cát vun quanh chân (23/10). **Đỉnh đá phẳng y 3, x 10–24, tâm đỉnh (17, 3)**: con cua đứng ở đó (trò "on the rock") |
| `o-khoa-so` | 120×170 | Hải đăng · ổ khoá số (vòng 4): quai xám, thân vàng, **ô kem để game đặt chấm (1–5): x 20–100, y 76–138**; lỗ khoá nhỏ ở (60, 148). Gợi ý chỗ chấm: 1 chấm (60, 107); 2–5 chấm ở các góc (40, 92), (80, 122), (40, 122), (80, 92), r 7. Vẽ to được tới ô đứng cao gần bằng hải đăng |
| `o-khoa-hinh` | 120×170 | Hải đăng · ổ khoá có **lỗ hình chữ nhật: x 36–84, y 92–124** (lỗ tối, viền vàng sẫm). Cùng thân với ổ khoá số |
| `chia-khoa-trong` | 160×70 | Hải đăng · chìa khoá vàng có **đầu chìa để trống: đĩa kem tâm (36, 35), bán kính 23** (bản `-trai`: tâm (124, 35)); game đặt số hoặc hình (chữ nhật, vuông, tam giác…) vào đó. Mỗi đáp án là một chìa |
| `sao-bien` | 44×42 | Màn 7 · con sao biển (22/10, vẽ lại): con vật biển màu cam, năm cánh tròn mập, gai sần (chấm sáng), mặt cười dễ thương. Nằm phẳng trên cát. Đồ cận |
| `tui-ngu` | 200×260 | Màn 2 · túi ngủ xanh lá còn trống, nằm dưới đất, mũ trùm ở bên trái. Cùng khung, cùng đáy (y 246) với tư thế của các bạn, nên đặt chồng đúng chỗ `ben-ngu-tui-ngu` |

## `cay/` · cây (23/10)
Cùng luật chung (1 m ≈ 12 đơn vị, chân chạm cạnh dưới, có `-phai` / `-trai`). Dùng trên đảo khối của thành phố nên vẽ kiểu khối như `dao-khoi/` (từ vòng 4).

| Tên (thêm `-phai` / `-trai`) | Khung W×H | Ghi chú |
|---|---|---|
| `bui-cay` | 40×24 | bụi cây, đáy chạm cạnh dưới. Sở thú: chạm bụi cây, Polly nói "A bush!". **Vòng 4 (23/10): vẽ lại kiểu khối như đảo (ba khối tròn có mặt sáng, mặt tối, bóng dưới chân, không nét viền)**, cùng tên, cùng khung |

## `dao-khoi/` · đồ trên đảo khối của thành phố (vòng 4, 23/10)
Kiểu khối như đảo và cây hình nón: **khối đặc, không nét viền đen**, sáng từ trên bên trái (mặt trái, mặt trên sáng; mặt phải, mặt dưới sẫm), bóng mờ dưới chân. **Giữ đúng `viewBox` app đang dùng cho từng món**, nên thay thẳng hình cũ. Đồ trên đảo vẽ theo một hướng nhìn cố định nên không có `-trai`. Các bạn, thú, đồ ăn vẫn là sticker (có viền trắng).

| File | viewBox | Ghi chú |
|---|---|---|
| `cau-truot.svg` | 0 0 130 120 | cầu trượt: thang xanh bên phải, bục vàng (mặt trên x 86–126, y 12–22), máng hồng từ đỉnh (khoảng (92, 26)) cong xuống chân trái (khoảng (8, 112)) |
| `xich-du.svg` | 0 0 130 110 | xích đu: khung chữ A đỏ hai bên, xà ngang trên (y 6–18), dây nâu, ghế vàng (mặt ghế y 68–73, x 48–84); điểm treo (65, 14) |
| `bap-benh.svg` | 0 0 130 70 | bập bênh: trụ tam giác tím, tấm ván xanh (mặt trên y 34, x 6–126), hai tay nắm vàng ở x 14 và 114; điểm tựa (65, 38) |
| `qua-bong.svg` | 0 0 40 40 | quả bóng cam, tâm (20, 19), bán kính 16 |
| `cay-tron.svg` | 0 0 90 130 | cây tán tròn: thân nâu (gốc (45, 124)), tán ba khối tròn |
| `cay-sao.svg` | -6 -10 132 190 | cây sao của Chồi ở quảng trường: thân, tán khối to, **12 ngôi sao `class="sao"`, `data-k` 1–12**, đúng 12 chỗ cũ của app; trong file tất cả đều chưa sáng (#7FCCA4), game tô vàng (#FFD21F) n ngôi đầu |
| `cau-truot-lam.svg` | 0 0 130 120 | cầu trượt có **Lam ngồi ở đỉnh máng**, trong nhóm `<g class="tp-slide">` (Lam: tư thế `ngoi`, quay trái, x 74, y −16, rộng 34) để game cho Lam trượt xuống |
| `xich-du-na.svg` | 0 0 130 110 | xích đu có **Na ngồi trên ghế**; nhóm `<g class="tp-swing">` gồm dây, ghế, Na, đung đưa quanh (65, 14) |
| `bap-benh-ben-lam.svg` | 0 0 130 70 | bập bênh có **Ben (trái) và Lam (phải) ngồi hai đầu**; nhóm `<g class="tp-saw">` gồm tấm ván và hai bạn, lên xuống quanh (65, 38) |

Các bạn trên đồ chơi là sticker (tư thế `ngoi` của `nhan-vat/`, viền trắng bằng bộ lọc riêng trong từng file, id `p195-<tên file>-stk`).

