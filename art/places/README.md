# Bối cảnh thật (TP.HCM), vẽ lại theo nét sticker của app

Mỗi file là một hình nền ngang, cùng khung với `BG.*` trong `index.html`:
`viewBox="0 0 200 140" preserveAspectRatio="xMidYMax meet" overflow="visible"`.
Trời và nền kéo dài từ x −400 đến 600, nên khung 16:9 nào cũng kín.

Đây chỉ là **nền**. Đồ bé chạm vào (lều, đèn lồng, xe đẩy, quả, cây cao, ao, mặt trời…) vẫn do game vẽ chồng lên.
Trên hình không có chữ, số, biển tên hay logo. Không có mặt trẻ thật.

| File | Dùng ở | Thay cho |
|---|---|---|
| `lop-hoc.svg` | Màn 0 · trong lớp (bản đồ treo trên kệ trái, y ≈ 38–50) | `BG.classroom` |
| `san-truong.svg` | Màn 0 · sân trường | `BG.school` |
| `cong-vao-truong.svg` | Màn 0 · cổng trường (sân phía sau, cổng phía trước) | — |
| `xe-buyt.svg` | Màn 0 · xe buýt trường | — |
| `vuon-truong.svg` | Màn 0 · vườn trường | `BG.sgarden` |
| `cong-vien.svg` | Màn 1 · công viên (chỉ cỏ; cây cao và ao vẫn do game vẽ) | `BG.park` |
| `vuon-nha-na-chieu.svg` | Màn 2 · phần 1, hoàng hôn (mặt trời của game lặn sau dãy nhà) | `BG.dusk` |
| `vuon-nha-na-dem.svg` | Màn 2 · phần 2–9, ban đêm | `BG.night` |
| `sieu-thi.svg` | Màn 4 · cửa hàng | `BG.shop` |
| `duong-toi-truong.svg` | Màn 6 · đường từ nhà tới cổng trường | — |

Ghi chú khi gắn vào app:
- Nhóm `class="tp tp-cloud"` và `class="tp tp-tree"` là mây và cây chạm được, giống `BG` hiện tại.
- Nhóm `class="bg-far"` là lớp xa (nhạt, nét mảnh). Không làm mờ thêm.
- Không có mặt trời trong nền; game tự vẽ.
- Id trong `clipPath` đều có tiền tố `p195-` để không trùng khi nhiều SVG cùng nằm trong trang.

Nguồn vẽ: thư mục làm việc của chat [App] Bối cảnh & hình vẽ. Cảnh nào sửa thì thay file cùng tên.
