# Bối cảnh thật (TP.HCM), vẽ lại theo nét sticker của app

Do chat **[App] Bối cảnh & hình vẽ** vẽ và duyệt với chị Minh. Gắn vào app bằng `python3 tools/art/embed_places.py`
(chỉ các tên trong `USED` của script được chép vào `index.html`; màn nào bắt đầu dùng cảnh mới thì thêm tên vào đó).
Cảnh nào sửa thì thay file **cùng tên**, nên bên app chỉ cần chạy lại script.

## Luật vẽ chung
- Hình nền ngang, cùng khung với `BG.*`: `viewBox="0 0 200 140" preserveAspectRatio="xMidYMax meet" overflow="visible"`; trời và nền kéo dài x −400…600.
- Chỉ là **nền**. Đồ bé chạm vào (lều, đèn lồng, giường, bàn, xe đẩy, quả, cần cẩu, ngôi nhà, rương, cây cao, ao, mặt trời…) do game vẽ chồng lên.
- **Chỗ nhân vật đứng (sàn, nền đất) để một màu trơn**: không thảm, không đường kẻ gạch, không vệt bánh xe (20/10). Riêng sân cỏ có một dải cỏ sáng hơn dẫn vào sảnh.
- **Luật chung cho hình nền (đã duyệt 21/10):**
  1. Ba loại bản, cùng góc nhìn, cùng bảng màu, cùng đường chân trời:
     - `<ten>.svg` = toàn cảnh: trang đầu, giới thiệu nhân vật, trang kể chuyện không có trò.
     - `<ten>-tron.svg` = sân khấu: mọi trang có đồ của game. Giữ trời, mây, lớp xa, hàng rào, cây chung chung ở hai mép; vùng chơi để trơn.
     - `<ten>-can-<vat>.svg` = cận: trò có đồ nhỏ. Góc gần, tối đa 3 thứ trên nền.
  2. Vùng chơi (khung 200×140): x 25–175, y 60–135 không đồ vật, không mảng màu đậm, chỉ nền một màu (cùng lắm một dải sáng hơn). Dải y 105–140 không có chi tiết chính (chỗ thẻ lựa chọn). Mỗi cảnh ghi y của mặt đất trong README.
  3. ~~Màu theo chiều sâu: lớp xa độ tươi 50%, sáng hơn 20%, nét 0,6; lớp giữa 80%.~~ **Sửa 21/10 (chọn phương án C):** giữ màu như các cảnh đã chốt: lớp xa (`bg-far`) nhạt, nét mảnh như hiện nay; không tô lại theo thông số. App vẫn bỏ bộ lọc làm mờ.
  4. Màu dành cho đồ của game (đỏ tươi, vàng đậm, xanh dương đậm, tím đậm) không dùng thành mảng lớn trên nền, tối đa khoảng 5% khung.
  5. Đồ chơi lặp lại giữa các trang (cầu trượt, cây cầu, khung leo) dùng một hình duy nhất trong do-choi/.
- Lớp xa nằm trong nhóm `class="bg-far"`. App không lọc, không làm mờ thêm.
- Bãi cỏ cắt sọc đậm nhạt xen kẽ như sân bóng (dải rộng dần khi gần), để bé thấy ngay đây là cỏ và là mặt đất phẳng (21/10).
- Nét trang trí (đường gạch, đường kẻ) không bao giờ đè lên viền đen.
- Không có mặt trời, không chữ, không số, không biển tên, không logo (riêng cổng sở thú có chữ ZOO). Không có mặt trẻ thật.
- Mỗi id trong SVG là duy nhất trên toàn bộ thư mục (tiền tố `p195-` + tên cảnh), nên gắn nhiều hình vào cùng một trang không bị trùng.
- Nhóm `tp tp-cloud` / `tp tp-tree` là mây và cây chạm được. Id trong SVG có tiền tố `p195-`.

## Unit 1 (đủ cả 8 màn, 20/10)
Cột **Mặt đất** là y (trong khung 200×140) nơi nhân vật đứng. Cột **Bản** ghi bản nào dùng ở trang nào; cảnh chưa có bản `-tron` thì tạm dùng toàn cảnh cho mọi trang.

| File | Dùng ở | Mặt đất (y) | Bản → trang | Thay cho |
|---|---|---|---|---|
| `lop-hoc.svg` | Màn 0 · trong lớp (bản đồ trên kệ trái, y ≈ 38–50) | 96 | toàn cảnh: mọi trang | `BG.classroom` |
| `san-truong.svg` | Màn 0 · sân trường | 92 | toàn cảnh: mọi trang | `BG.school` |
| `cong-vao-truong.svg` | Màn 0 mở đầu, cuối Màn 6 · cổng | 104 (vỉa hè), đường 117 | toàn cảnh: trang đầu, trang kể chuyện | — |
| `cong-vao-truong-tron.svg` | như trên, sân khấu (21/10) | 104 (vỉa hè trơn tới đáy, không có đường) | sân khấu: mọi trang có đồ của game. Tường trơn kem + xanh ngọc, không biển tên | — |
| `xe-buyt.svg` | Màn 0 · xe buýt trường (đồ vật) | đáy hình | — | — |
| `vuon-truong.svg` | Màn 0 · vườn sau trường. **21/10: chân trời lên y 62, cỏ cắt sọc**; nhà nấm, khung leo, đồi cỏ dời lên theo; hố cát giữ đúng chỗ cũ (y ≈ 108–132) | 62 | toàn cảnh: trang đầu, ú òa, mảnh 1 | `BG.sgarden` |
| `vuon-truong-tron.svg` | Màn 0 · vườn sau trường, sân khấu (21/10) | 62 | sân khấu: đếm cờ, cầu trượt, cây cầu, trốn tìm. Không hố cát: cầu trượt `do-choi/cau-truot-*.svg`, cây cầu `do-choi/cay-cau.svg`, bụi cây đặt thẳng trên cỏ | — |
| `cong-vien.svg` | Màn 1 · công viên | 92 | toàn cảnh: mọi trang | `BG.park` |
| `vuon-nha-na-chieu.svg` | Màn 2 · phần 1, hoàng hôn | ≈ 92 | toàn cảnh: mọi trang | `BG.dusk` |
| `vuon-nha-na-dem.svg` | Màn 2 · phần 2–9, ban đêm | ≈ 92 | toàn cảnh: mọi trang | `BG.night` |
| `phong-na.svg` | Màn 3 · phòng Na | 92 | toàn cảnh: mọi trang | phòng Na |
| `phong-na-toi.svg` | Màn 6 · buổi tối chọn sách | 92 | toàn cảnh | — |
| `phong-na-dem.svg` | Màn 6 · Na đi ngủ, "morning or night?" | 92 | toàn cảnh | — |
| `sieu-thi.svg` | Màn 4 · cửa hàng | 98 | toàn cảnh: mọi trang | `BG.shop` |
| `cong-truong-xay.svg` | Màn 5 · công trường | 98 | toàn cảnh: mọi trang | — |
| `phong-nha-moi.svg` | Màn 5 · trong ngôi nhà mới xây | 92 | toàn cảnh | — |
| `nha-na-bo-doc.svg` | Màn 6 · mở đầu, xếp tranh một ngày | 128 (tầng dưới), 90 (tầng trên) | toàn cảnh | — |
| `bep.svg` | Màn 6 · bữa sáng | 96 | toàn cảnh | — |
| `doc-cau-qua-kenh.svg` | Màn 6 · kẻ đường xuống dốc tới trường | mặt cầu 85 (giữa) → 112 (hai đầu) | toàn cảnh | — |
| `duong-toi-truong.svg` (+ `-chieu`, `-toi`) | Màn 6 · đường tới trường sáng/chiều/tối. **21/10: bỏ xe ôm vẽ sẵn** (xe lấy từ `art/props/xe/`), vỉa hè gần trơn | 128 (vỉa hè gần), làn xe 104–128 (xa 104–116, gần 116–128) | toàn cảnh: trang đầu, kẻ đường tới trường | — |
| `duong-toi-truong-tron.svg` (+ `-chieu-tron`, `-toi-tron`) | như trên, sân khấu (21/10): không đèn giao thông, không vạch qua đường, không tường cổng ở giữa, cây chỉ ở hai mép | như trên | sân khấu: ếch qua đường, xếp tranh sáng/chiều/tối, mọi trang có xe chạy | — |
| `cong-vien-chieu.svg` | Màn 6 · chiều Na đạp xe | 92 | toàn cảnh | — |
| `trang-sach.svg` | Màn 6 · trong cuốn sách | mặt ao 78 | toàn cảnh | — |
| `roi-ben.svg` | Màn 7 · rời bến | mặt sông 59 | toàn cảnh | — |
| `ra-khoi.svg` | Màn 7 · ra khơi | mặt biển 70 | toàn cảnh | — |
| `dao-bai-cat.svg` | Màn 7 · trên đảo: bãi cát | ≈ 98 | toàn cảnh | — |
| `dao-hai-dang.svg` | Màn 7 · trên đảo: hải đăng, cầu gỗ | ≈ 98 | toàn cảnh | — |
| `hang-kho-bau.svg` | Màn 7 · chỗ đặt rương | 112 | toàn cảnh | — |

## Quyết định 21/10 (trang "Chọn phương án hình")
- Màu: **C**, giữ như hiện tại (luật 3 đã sửa theo). Thư mục `thu-mau/` đã xoá.
- Vườn trường: chân trời lên **y 62**, cỏ cắt sọc; bản sân khấu **không hố cát**.
- Mái kính chữ A giữ rõ (không nhạt theo lớp xa). Cổng trường giữ thiết kế cũ, kể cả cụm đỏ trên biển tên.
- Cầu trượt và cây cầu vẽ một lần trong `do-choi/`.
- Xe: xem `art/props/README.md`.

## `do-choi/` · đồ chơi sân trường, để game đặt riêng (đồ vật, đứng trên mặt đất; tỉ lệ khoảng 32 đơn vị = 1 m)
| File | Gợi ý dùng |
|---|---|
| `nha-nam.svg` | ú òa (bạn ló ra từ cửa), in/on (mèo trong nhà nấm, trên mái) |
| `doi-co-ham.svg` | kẻ đường: leo thang lên đồi rồi chui ra hầm; trốn tìm; in/under |
| `cong-con-cua.svg` | kẻ đường: chui cổng cua → qua cầu khúc gỗ → chui ống; đếm khúc gỗ, gọi tên màu |
| `khung-leo.svg` | on/under, leo thang |
| `khung-hat.svg` | khung hạt đỏ trắng: đếm đến 5 (Unit 1), đến 10 (Unit 2) |
| `cau-truot-phai.svg` / `cau-truot-trai.svg` | cầu trượt (thang bên trái, máng trượt sang phải / bản lật): Ben trượt xuống, kẻ đường dọc |
| `cay-cau.svg` | cây cầu gỗ nhỏ: qua cầu, kẻ đường ngang |

## `sau/` · địa danh, chưa dùng trong Unit 1
`buu-dien.svg`, `thao-cam-vien.svg` (cổng sắt), `nha-tho-duc-ba.svg`, `cho-ben-thanh.svg`, `metro.svg`, `pho-di-bo.svg` (nhìn về Bitexco).
