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
  3. Màu theo chiều sâu, vẽ sẵn trong hình (app sẽ bỏ bộ lọc làm mờ): lớp gần màu rõ, khối to, tối đa 2 tông, gần như không chi tiết; lớp giữa độ tươi khoảng 80%; lớp xa (bg-far) độ tươi khoảng 50%, sáng hơn khoảng 20%, nét 0,6.
  4. Màu dành cho đồ của game (đỏ tươi, vàng đậm, xanh dương đậm, tím đậm) không dùng thành mảng lớn trên nền, tối đa khoảng 5% khung.
  5. Đồ chơi lặp lại giữa các trang (cầu trượt, cây cầu, khung leo) dùng một hình duy nhất trong do-choi/.
- Lớp giữa nằm trong nhóm `class="bg-mid"`, lớp xa trong `class="bg-far"`, lớp gần không có class. Màu đã vẽ sẵn theo chiều sâu, app không cần lọc hay làm mờ thêm.
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
| `cong-vao-truong.svg` | Màn 0 mở đầu, cuối Màn 6 · cổng | 104 (vỉa hè), đường 117 | toàn cảnh: mọi trang. Đang thử màu: `thu-mau/cong-vao-truong-a.svg`, `-b.svg` | — |
| `xe-buyt.svg` | Màn 0 · xe buýt trường (đồ vật) | đáy hình | — | — |
| `vuon-truong.svg` | Màn 0 · vườn sau trường | 88 | toàn cảnh: trang đầu, ú òa, mảnh 1 | `BG.sgarden` |
| `vuon-truong-tron.svg` | Màn 0 · vườn sau trường, sân khấu (mới 21/10, màu kiểu A) | 88 | sân khấu: đếm cờ, cầu trượt, cây cầu, trốn tìm (cầu trượt, cây cầu, bụi cây do game đặt). Bản màu B: `thu-mau/vuon-truong-tron-b.svg` | — |
| `cong-vien.svg` | Màn 1 · công viên | 92 | toàn cảnh: mọi trang. Đang thử màu: `thu-mau/cong-vien-a.svg`, `-b.svg` | `BG.park` |
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
| `duong-toi-truong.svg` (+ `-chieu`, `-toi`) | Màn 6 · đường tới trường sáng/chiều/tối | 128 (vỉa hè gần), làn xe 104–128 | toàn cảnh | — |
| `cong-vien-chieu.svg` | Màn 6 · chiều Na đạp xe | 92 | toàn cảnh | — |
| `trang-sach.svg` | Màn 6 · trong cuốn sách | mặt ao 78 | toàn cảnh | — |
| `roi-ben.svg` | Màn 7 · rời bến | mặt sông 59 | toàn cảnh | — |
| `ra-khoi.svg` | Màn 7 · ra khơi | mặt biển 70 | toàn cảnh | — |
| `dao-bai-cat.svg` | Màn 7 · trên đảo: bãi cát | ≈ 98 | toàn cảnh | — |
| `dao-hai-dang.svg` | Màn 7 · trên đảo: hải đăng, cầu gỗ | ≈ 98 | toàn cảnh | — |
| `hang-kho-bau.svg` | Màn 7 · chỗ đặt rương | 112 | toàn cảnh | — |

## `thu-mau/` · thử màu theo chiều sâu (21/10, chờ chọn)
Cùng hình, hai cách làm nhạt lớp xa. Chọn xong thì bản được chọn thay vào file chính cùng tên, thư mục này xoá đi.
- **A** (`*-a.svg`): lớp xa nhạt về phía **trắng** (độ tươi 50%, sáng hơn 20%, nét 0,6); lớp giữa độ tươi 80%.
- **B** (`*-b.svg`): lớp xa nhạt về phía **màu trời** (độ tươi 50%, pha 30% màu trời, nét 0,6), như sương xa; lớp giữa độ tươi 80%, pha chút màu trời.
- Ở cổng trường, lớp gần đã làm gọn: tường kem + xanh ngọc (2 tông), khối tên trường một màu xanh ngọc (bỏ cụm đỏ vì đỏ dành cho đồ của game), bỏ sóng, hoa, chậu, kẻ gạch vỉa hè. Ở công viên bỏ cụm hoa ở lớp gần.

## `do-choi/` · đồ chơi sân trường thật, để game đặt riêng (đồ vật, đứng trên mặt đất)
| File | Gợi ý dùng |
|---|---|
| `nha-nam.svg` | ú òa (bạn ló ra từ cửa), in/on (mèo trong nhà nấm, trên mái) |
| `doi-co-ham.svg` | kẻ đường: leo thang lên đồi rồi chui ra hầm; trốn tìm; in/under |
| `cong-con-cua.svg` | kẻ đường: chui cổng cua → qua cầu khúc gỗ → chui ống; đếm khúc gỗ, gọi tên màu |
| `khung-leo.svg` | on/under, leo thang |
| `khung-hat.svg` | khung hạt đỏ trắng: đếm đến 5 (Unit 1), đến 10 (Unit 2) |

## `sau/` · địa danh, chưa dùng trong Unit 1
`buu-dien.svg`, `thao-cam-vien.svg` (cổng sắt), `nha-tho-duc-ba.svg`, `cho-ben-thanh.svg`, `metro.svg`, `pho-di-bo.svg` (nhìn về Bitexco).
