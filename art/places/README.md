# Bối cảnh thật (TP.HCM), vẽ lại theo nét sticker của app

Do chat **[App] Bối cảnh & hình vẽ** vẽ và duyệt với chị Minh. Gắn vào app bằng `python3 tools/art/embed_places.py`
(chỉ các tên trong `USED` của script được chép vào `index.html`; màn nào bắt đầu dùng cảnh mới thì thêm tên vào đó).
Cảnh nào sửa thì thay file **cùng tên**, nên bên app chỉ cần chạy lại script.

## Luật vẽ chung
- Hình nền ngang, cùng khung với `BG.*`: `viewBox="0 0 200 140" preserveAspectRatio="xMidYMax meet" overflow="visible"`; trời và nền kéo dài x −400…600.
- Chỉ là **nền**. Đồ bé chạm vào (lều, đèn lồng, giường, bàn, xe đẩy, quả, cần cẩu, ngôi nhà, rương, cây cao, ao, mặt trời…) do game vẽ chồng lên.
- **Chỗ nhân vật đứng (sàn, nền đất) để một màu trơn**: không thảm, không đường kẻ gạch, không vệt bánh xe (20/10). Riêng sân cỏ có một dải cỏ sáng hơn dẫn vào sảnh.
- Nền không giành mắt bé: lớp xa (`class="bg-far"`) nhạt, nét mảnh; không làm mờ thêm. Ở siêu thị chỉ kệ và đồ trên kệ được làm nhạt (bộ lọc `p195-mute`), phòng giữ nguyên.
- Nét trang trí (đường gạch, đường kẻ) không bao giờ đè lên viền đen.
- Không có mặt trời, không chữ, không số, không biển tên, không logo (riêng cổng sở thú có chữ ZOO). Không có mặt trẻ thật.
- Mỗi id trong SVG là duy nhất trên toàn bộ thư mục (tiền tố `p195-` + tên cảnh), nên gắn nhiều hình vào cùng một trang không bị trùng.
- Nhóm `tp tp-cloud` / `tp tp-tree` là mây và cây chạm được. Id trong SVG có tiền tố `p195-`.

## Unit 1 (đủ cả 8 màn, 20/10)
| File | Dùng ở | Thay cho |
|---|---|---|
| `lop-hoc.svg` | Màn 0 · trong lớp (bản đồ trên kệ trái, y ≈ 38–50) | `BG.classroom` |
| `san-truong.svg` | Màn 0 · sân trường: cỏ nhân tạo, mái kính chữ A, sảnh cột xanh, cây sứ | `BG.school` |
| `cong-vao-truong.svg` | Màn 0 mở đầu (đến trường), cuối Màn 6 · cổng, sân trường phía sau | — |
| `xe-buyt.svg` | Màn 0 · xe buýt trường (đồ vật 120×72) | — |
| `vuon-truong.svg` | Màn 0 · vườn sau trường: khung leo, nhà nấm, đồi cỏ có hầm, hàng rào trắng | `BG.sgarden` |
| `cong-vien.svg` | Màn 1 · công viên (chỉ cỏ) | `BG.park` |
| `vuon-nha-na-chieu.svg` | Màn 2 · phần 1, hoàng hôn (mặt trời của game lặn sau dãy nhà) | `BG.dusk` |
| `vuon-nha-na-dem.svg` | Màn 2 · phần 2–9, ban đêm | `BG.night` |
| `phong-na.svg` | Màn 3 · phòng Na | phòng Na |
| `phong-na-toi.svg` | Màn 6 · buổi tối chọn sách | — |
| `phong-na-dem.svg` | Màn 6 · Na đi ngủ, "morning or night?" (tắt đèn, trăng, ánh trăng trên sàn) | — |
| `sieu-thi.svg` | Màn 4 · cửa hàng (đã dịu màu) | `BG.shop` |
| `cong-truong-xay.svg` | Màn 5 · công trường | — |
| `phong-nha-moi.svg` | Màn 5 · trong ngôi nhà mới xây (cửa sổ lớn nhìn ra công trường) | — |
| `nha-na-bo-doc.svg` | Màn 6 · mở đầu và xếp tranh một ngày: bếp tầng dưới (sáng), sân trước (chiều), phòng ngủ tầng trên giống phòng Na (tối) | — |
| `bep.svg` | Màn 6 · bữa sáng | — |
| `doc-cau-qua-kenh.svg` | Màn 6 · kẻ đường xuống dốc tới trường (cầu qua kênh, trường ở bên phải) | — |
| `duong-toi-truong.svg` | Màn 6 · đường tới trường, buổi sáng | — |
| `duong-toi-truong-chieu.svg` / `duong-toi-truong-toi.svg` | Màn 6 · cùng con đường buổi chiều và buổi tối (sáng/chiều/tối, trò Ếch qua đường) | — |
| `cong-vien-chieu.svg` | Màn 6 · chiều Na tự đạp xe | — |
| `trang-sach.svg` | Màn 6 · trong cuốn sách: ếch nhảy theo tiếng (lá sen, ếch do game vẽ) | — |
| `roi-ben.svg` | Màn 7 · mở đầu, đi thuyền trên sông Sài Gòn | — |
| `ra-khoi.svg` | Màn 7 · ra khơi, thấy đảo phía trước | — |
| `dao-bai-cat.svg` | Màn 7 · trên đảo: bãi cát, dừa, đá | — |
| `dao-hai-dang.svg` | Màn 7 · trên đảo: đồi có hải đăng, cầu gỗ | — |
| `hang-kho-bau.svg` | Màn 7 · chỗ đặt rương (rương do game vẽ) | — |

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
