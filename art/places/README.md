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
  2. Trang nào có trò chơi (kể cả ú òa) thì dùng bản `-tron`; toàn cảnh chỉ cho trang đầu và trang kể chuyện không có trò.
  2b. Vùng chơi (khung 200×140): x 25–175, y 60–135 không đồ vật, không mảng màu đậm, chỉ nền một màu (cùng lắm một dải sáng hơn). Dải y 105–140 không có chi tiết chính (chỗ thẻ lựa chọn). Mỗi cảnh ghi y của mặt đất trong README.
  3. ~~Màu theo chiều sâu: lớp xa độ tươi 50%, sáng hơn 20%, nét 0,6; lớp giữa 80%.~~ **Sửa 21/10 (chọn phương án C):** giữ màu như các cảnh đã chốt: lớp xa (`bg-far`) nhạt, nét mảnh như hiện nay; không tô lại theo thông số. App vẫn bỏ bộ lọc làm mờ.
  4. Màu dành cho đồ của game (đỏ tươi, vàng đậm, xanh dương đậm, tím đậm) không dùng thành mảng lớn trên nền, tối đa khoảng 5% khung.
  5. Đồ chơi lặp lại giữa các trang (cầu trượt, cây cầu, khung leo) dùng một hình duy nhất trong do-choi/.
- Lớp xa nằm trong nhóm `class="bg-far"`. App không lọc, không làm mờ thêm.
- Mọi cảnh có trời và nền trải rộng x −400…600, nên điện thoại ngang (khoảng 2,2:1) vẫn kín màn hình (đã kiểm tra 21/10; cầu qua kênh đã nối dài mặt cầu).
- Bãi cỏ cắt sọc đậm nhạt xen kẽ như sân bóng (dải rộng dần khi gần), để bé thấy ngay đây là cỏ và là mặt đất phẳng (21/10).
- Nét trang trí (đường gạch, đường kẻ) không bao giờ đè lên viền đen.
- **Lớp xa không bao giờ đè nét đen của lớp gần** (22/10): nhóm `bg-far` vẽ trước mọi thứ ở gần; chỗ nào đồ xa đứng chạm đường sàn hay đường chân trời thì vẽ lại đường đen đó sau lớp xa. Áp dụng cho mọi bản toàn cảnh và `-tron` (đã soát hết; chỉ `sieu-thi-tron` bị, đã sửa).
- Lớp gần vẽ đè lớp xa: viền mép cỏ (đường chân trời) nằm trên chân đồ xa (22/10).
- Cây to (thân nâu, tán tròn): nét đáy thân đậm bằng nét hai bên thân (22/10, đã sửa ở mọi nền có loại cây này).
- Không có mặt trời, không chữ, không số, không biển tên, không logo (riêng cổng sở thú có chữ ZOO). Không có mặt trẻ thật.
- Mỗi id trong SVG là duy nhất trên toàn bộ thư mục (tiền tố `p195-` + tên cảnh), nên gắn nhiều hình vào cùng một trang không bị trùng.
- Nhóm `tp tp-cloud` / `tp tp-tree` là mây và cây chạm được. Id trong SVG có tiền tố `p195-`.

## Unit 1 (đủ cả 8 màn, 20/10)
Cột **Mặt đất** là y (trong khung 200×140) nơi nhân vật đứng. Cột **Bản** ghi bản nào dùng ở trang nào; cảnh chưa có bản `-tron` thì tạm dùng toàn cảnh cho mọi trang.

| File | Dùng ở | Mặt đất (y) | Bản → trang | Thay cho |
|---|---|---|---|---|
| `lop-hoc.svg` | Màn 0 · trong lớp (bản đồ trên kệ trái, y ≈ 38–50) | 96 | toàn cảnh: mọi trang | `BG.classroom` |
| `lop-hoc-tron.svg` | Màn 0 · lớp học, sân khấu: bỏ kệ nhà, bàn ghế; giữ cửa sổ, đồng hồ, tủ ở hai mép (21/10) | 96 | sân khấu | — |
| `san-truong.svg` | Màn 0 · sân trường | 92 | toàn cảnh: mọi trang | `BG.school` |
| `san-truong-tron.svg` | Màn 0 · sân trường, sân khấu: hàng rào cây dời ra mép phải (21/10) | 92 | sân khấu: ba chuyện cảm xúc, giúp bạn | — |
| `cong-vao-truong.svg` | Màn 0 mở đầu, cuối Màn 6 · cổng | 104 (vỉa hè), đường 117 | toàn cảnh: trang đầu, trang kể chuyện | — |
| `cong-vao-truong-tron.svg` | như trên, sân khấu (21/10) | 104 (vỉa hè trơn tới đáy, không có đường) | sân khấu: mọi trang có đồ của game. Cổng giữ nguyên thiết kế (biển tên, sóng, hoa, chậu), chỉ dịu đi một chút | — |
| `cong-vao-truong-tron-xe.svg` | Màn 0 · nền trò xếp bạn lên xe buýt (tối 21/10): cổng dịu riêng. Không cây, không bụi; tường rào kem trơn, mép trên xanh rất nhạt (không sóng đỏ xanh, không biển tên, không chậu hoa); cổng lùi xa và nhạt, dời sang trái (khe cổng x 14–52, trụ cổng x 14 và 52), trường phía sau rất nhạt. Chỗ xe đỗ (x 66–194, y 34–106, đúng `.cbus .busbody`) chỉ có tường trơn và trời, nên xe vàng nổi | 104 (vỉa hè trơn tới đáy) | sân khấu: xếp bạn lên xe buýt | — |
| `duong-quanh-truong.svg` (+ `-tron`) | Màn 0 · đường nhựa vòng quanh trường tới cổng sau của vườn (22/10). Tường trường bên trái (tới x 112), hàng rào gỗ trắng của vườn bên phải, **cổng nhỏ: hai trụ gỗ x 156 và 183, mái đỏ, khe cổng x 162–182**, một cánh cổng mở; lối nhỏ sáng màu từ cổng ra đường. Bản `-tron` bỏ hoa và một cây | vỉa hè 100–106; **đường 106–130 (bánh xe y 122)**; cỏ gần 130–140 | xe buýt chạy dọc đường; **xe đỗ ở cổng vườn: xe-dua-don cỡ 90×42 (hệ số 1), đáy bánh y 122, mép trái x 66, mũi xe x 156 ngay cạnh trụ cổng**; các bạn xuống xe đi vào khe cổng | — |
| `xe-buyt.svg` | Màn 0 · xe buýt trường (đồ vật) | đáy hình | — | — |
| `vuon-truong.svg` | Màn 0 · vườn sau trường. **21/10: chân trời lên y 62, cỏ cắt sọc**; nhà nấm, khung leo, đồi cỏ dời lên theo; hố cát giữ đúng chỗ cũ (y ≈ 108–132) | 62 | toàn cảnh: trang đầu, mảnh 1 | `BG.sgarden` |
| `vuon-truong-tron.svg` | Màn 0 · vườn sau trường, sân khấu. **Tối 21/10 (chơi thử lần 2): chân trời hạ xuống y 86** (cỏ ít hơn, trời và hàng rào nhiều hơn); bỏ nhà nấm; đồ xa nhạt đứng trên chân trời ở hai bên: khung gỗ leo (x 20–64, cao tới y 62), góc hộp cát có xẻng và xô (x 116–180, cao tới y 66); cây to ở hai mép. Không có hồ. 22/10: viền mép cỏ (y 86) vẽ đè lên chân đồ xa | 86 | sân khấu: đếm cờ, cầu trượt (quả bóng rơi), trốn tìm trong bụi, **ú òa**. Cầu trượt `do-choi/cau-truot-*.svg`, dốc cỏ `do-choi/doc-co.svg`, bụi cây đặt thẳng trên cỏ. Trang kẻ cây cầu dùng `vuon-truong-tron-ho.svg` | — |
| `vuon-truong-tron-ho.svg` | Màn 0 · trang kẻ cây cầu (tối 21/10; 22/10 viền mép cỏ đè lên chân đồ xa): như `vuon-truong-tron` (chân trời y 86) thêm một hồ nhỏ bờ uốn lượn, viền đá sỏi, 7 lá sen, 3 hoa súng; hồ x 44–158, y 92–140 (khoảng 30% phần cỏ). **Hai bờ để đặt hai chân cầu ở y 128,8: bờ trái x 56–64, bờ phải x 136–144** (đúng chỗ `do-choi/cay-cau.svg` đang đặt: tâm x 100, rộng 92, đáy y 128,8, tức `BRIDGE_AT={x:50,b:8,w:46}`; chân cầu ở x 58,5–62,9 và 137,1–141,5). Bên phải hồ (x 160–200, y 112–140) là cỏ trơn cho bụi cây có dấu X (game vẽ, đang ở x 176); bên trái hồ, chỗ Ben đứng (x 30–56, y 130) là cỏ | 86; chân cầu 128,8 | sân khấu: kẻ đường qua cây cầu | — |
| `cong-vien.svg` | Màn 1 · công viên | 92 | toàn cảnh: mọi trang | `BG.park` |
| `cong-vien-tron.svg` | Màn 1 · công viên, sân khấu: bỏ cây cọ và đèn ở giữa, bỏ hoa (21/10) | 92 | sân khấu: diều, bong bóng, vịt, bóng bay | — |
| `cong-vien-duong.svg` | Màn 1 · đường ven công viên (cạnh Landmark 81), nơi xe chạy qua (21/10) | vỉa hè gần 132, làn xa 106–119, làn gần 119–132 | toàn cảnh: mọi trang có xe chạy | — |
| `vuon-nha-na-chieu.svg` | Màn 2 · phần 1, hoàng hôn | ≈ 92 | toàn cảnh: mọi trang | `BG.dusk` |
| `vuon-nha-na-chieu-tron.svg` | Màn 2 · vườn chiều, sân khấu (21/10, sửa tối 21/10): bỏ nhà Na, cây to và cây nhỏ; chỉ còn tường rào thấp có chậu cây, thành phố xa, một bụi cây thấp ở mỗi mép (ngoài x 25–175) | ≈ 92 | sân khấu: mặt trời lặn, đom đóm | — |
| `vuon-nha-na-dem.svg` | Màn 2 · phần 2–9, ban đêm | ≈ 92 | toàn cảnh: trang kể chuyện, đèn lồng, bão, trốn tìm, đèn pin | `BG.night` |
| `vuon-nha-na-dem-tron.svg` | Màn 2 · vườn đêm, sân khấu (21/10, sửa tối 21/10): bỏ nhà Na, cây to và cây nhỏ; như bản chiều, thêm trăng sao | ≈ 92 | sân khấu: đèn lồng, bão, trốn tìm, đèn pin, túi ngủ, gõ trống | — |
| `vuon-nha-na-dem-can-ban.svg` | Màn 2 · cận: mèo con tìm chỗ khô (in/on/under). Tường rào thấp có chậu cây, một bụi cây ở mỗi mép (21/10; tối 21/10 bỏ góc nhà Na: đứng cạnh cái bàn cỡ mèo, góc nhà trông to bằng cái bàn) | 104 | cận: trò mèo, bàn, hộp (bàn, hộp, mèo do game vẽ). Nền không còn vật gì có cỡ cố định (nhà, cửa) để so, nên bàn và hộp ở cỡ nào cũng đúng; chỉ cần bàn cao hơn mèo đứng khoảng 1,3–2 lần và hộp vừa mèo ngồi lọt | — |
| `vuon-nha-na-dem-can-la.svg` | Màn 2 · cận: bọ rùa đậu trên lá. Cành từ mép trái, một chiếc lá to nằm ngang (chỗ đậu, y ≈ 58–96), vườn tối xa phía sau (21/10) | — | cận: trò bọ rùa (bọ rùa do game vẽ) | — |
| `vuon-nha-na-dem-truoc-leu.svg` | Màn 2 · cận: trước lều. Lều cam to ở mép trái, dây đèn nhỏ trên cao (21/10) | 112 | cận: trò gõ trống (trống do game vẽ) | — |
| `phong-na.svg` | Màn 3 · phòng Na | 92 | toàn cảnh: trang đầu, trang kể chuyện | phòng Na |
| `phong-na-tron.svg` | Màn 3 · phòng Na, sân khấu (21/10): cửa sổ, tranh, đồng hồ, máy lạnh đều trên y 58; thời khoá biểu ra mép phải; tường và sàn dưới trơn | 92 | sân khấu: gấu, bút màu, dọn đồ, hộp nhạc, mèo trốn, bắt đồ chơi | — |
| `phong-na-can-ban.svg` | Màn 3 · cận: mặt bàn thấp của Na (gỗ trơn từ y 62), tường hồng, một tranh trên cao (21/10) | 62 (mặt bàn) | cận: đô-mi-nô (quân do game vẽ) | — |
| `phong-na-can-but.svg` | Màn 3 · cận: mặt bàn học của Na (gỗ sáng từ y 66), bảng ghim có 2 tranh góc phải trên (21/10) | 66 (mặt bàn) | cận: bút màu và cốc | — |
| `phong-na-can-san.svg` | Màn 3 · cận: sát sàn phòng Na (từ y 69), góc giường mép trái, kệ đồ chơi mép phải (21/10) | 69 | cận: dọn đồ chơi nhỏ | — |
| `phong-na-toi.svg` | Màn 6 · buổi tối chọn sách | 92 | toàn cảnh | — |
| `phong-na-toi-tron.svg` | Màn 6 · phòng Na buổi tối, sân khấu (21/10) | 92 | sân khấu: chọn sách | — |
| `phong-na-dem.svg` | Màn 6 · Na đi ngủ, "morning or night?" | 92 | toàn cảnh | — |
| `phong-na-dem-tron.svg` | Màn 6 · phòng Na ban đêm, sân khấu (21/10) | 92 | sân khấu: Na đi ngủ | — |
| `sieu-thi.svg` | Màn 4 · cửa hàng | 98 | toàn cảnh: trang đầu, trang kể chuyện | `BG.shop` |
| `sieu-thi-tron.svg` | Màn 4 · cửa hàng, sân khấu (21/10, bản B): cùng tường, sàn, biển treo; quầy trái cây mép trái, kệ nước mép phải; hai kệ đồ chơi nhỏ rất nhạt ở x 34–64 và 134–164; giữa x 64–134 trống (chỗ tấm bản đồ). 22/10: kệ xa vẽ trước, đường sàn đen liền một mạch, không bị kệ xa đè | 98 | sân khấu: mọi trang có đồ của game | — |
| `sieu-thi-can-ghe.svg` | Màn 4 · cận: ghế gỗ dài (mặt ghế y 84, x 18–182), biển quả treo trên, quầy quả ở mép trái (21/10) | 84 (mặt ghế), sàn 98 | cận: quả, giỏ quả có số trên ghế dài | — |
| `cong-truong-xay.svg` | Màn 5 · công trường. Tối 21/10: cánh tay cần cẩu xa dài tới x 180, xe con và dây móc ở x 174 treo thẳng từ cánh tay; bỏ đám mây ở đầu cánh tay | 98 | toàn cảnh: mọi trang | — |
| `cong-truong-xay-tron.svg` | Màn 5 · công trường, sân khấu: bỏ cọc giao thông, chồng gạch (21/10); cần cẩu sửa như bản toàn cảnh (tối 21/10) | 98 | sân khấu: cần cẩu, bác thợ, tháp, xe tải | — |
| `cong-truong-can-cua-so.svg` | Màn 5 · cận: bức tường nhà mới, **lỗ vuông x 44–78, y 40–74; lỗ tròn tâm (150, 57), r 17** (21/10) | 112 | cận: cửa sổ Lam và Na cầm bay vào lỗ | — |
| `cong-truong-can-nha-xe.svg` | Màn 5 · cận: nhà để xe của Ben, tường gạch có 4 chỗ trống viền nét đứt: **22/10: tường rộng ra (x 24–176), cửa cuốn dài thành hình chữ nhật nằm ngang rõ ràng: x 56–132, y 80–116 (76 × 36, vừa một ô tô); cửa sổ x 142–164, y 70–92; đèn tâm (40, 78), r 8; mái tam giác (24,60) (100,26) (176,60)** | 116 | cận: ghép hình nhà để xe | — |
| `phong-nha-moi.svg` | Màn 5 · trong ngôi nhà mới xây | 92 | toàn cảnh | — |
| `phong-nha-moi-tron.svg` | Màn 5 · phòng nhà mới, sân khấu: bỏ thùng sơn, con lăn, thùng các-tông (21/10) | 92 | sân khấu: lắp tấm gỗ thành khung cửa | — |
| `nha-na-bo-doc.svg` | Màn 6 · mở đầu, xếp tranh một ngày | 128 (tầng dưới), 90 (tầng trên) | toàn cảnh | — |
| `the-tranh/mot-ngay-sang.svg`, `-chieu.svg`, `-toi.svg` | Màn 6 · ba thẻ tranh để xếp một ngày (khung 120×90, góc bo, có viền): sáng = bàn ăn có khăn kẻ, bát cháo bốc hơi, nải chuối, cốc sữa bên cửa sổ có mặt trời mọc (vẽ lại 21/10); chiều = công viên nắng chiều có lối đạp xe; tối = cửa sổ có trăng và cái giường nhìn ngang (đầu giường cao, gối, chăn kẻ sọc) (vẽ lại 21/10). Na do game vẽ (21/10) | — | thẻ | — |
| `bep.svg` | Màn 6 · bữa sáng | 96 | toàn cảnh | — |
| `bep-tron.svg` | Màn 6 · bếp, sân khấu: quầy bếp ngắn lại về mép trái, bỏ nồi cơm, đĩa quả (21/10) | 96 | sân khấu: bữa sáng, vỗ tay ba-na-na | — |
| `doc-cau-qua-kenh.svg` | Màn 6 · kẻ đường xuống dốc tới trường. 22/10: cầu sắt đơn giản hình thang: hai dốc thẳng, mặt cầu phẳng ở giữa, dốc dừng ngay chỗ chạm cỏ (chân trái x −14, chân phải x 214); bỏ vòm và các thanh dưới cầu, bỏ đoạn phẳng kéo dài hai bên. Lan can trắng nằm trong nhóm `<g class="bridge-rail">` để game lấy ra đặt trước Na. 22/10 chiều: đường đi bộ lát gạch dọc bờ gần, từ mép trái tới chân dốc trái (y 108,6–117); dốc phải đổ xuống **ngay cổng trường** (hai trụ x 200 và 230, vòm xanh ngọc ở trên, không biển tên), tường trường chạy tiếp sang phải từ x 226. Na đi: lối bộ (y 112) → dốc trái → mặt cầu (y 85) → dốc phải → khe cổng x 205–225, y 112 | mặt cầu 85 (giữa, x 46–154) → 112 (hai chân) | toàn cảnh | — |
| `duong-toi-truong.svg` (+ `-chieu`, `-toi`) | Màn 6 · đường tới trường sáng/chiều/tối. **21/10: bỏ xe ôm vẽ sẵn** (xe lấy từ `art/props/xe/`), vỉa hè gần trơn | 128 (vỉa hè gần), làn xe 104–128 (xa 104–116, gần 116–128) | toàn cảnh: trang đầu, kẻ đường tới trường | — |
| `duong-toi-truong-tron.svg` (+ `-chieu-tron`, `-toi-tron`) | như trên, sân khấu (21/10): không đèn giao thông, không vạch qua đường, không tường cổng ở giữa, cây chỉ ở hai mép | như trên | sân khấu: ếch qua đường, xếp tranh sáng/chiều/tối, mọi trang có xe chạy | — |
| `cong-vien-chieu.svg` | Màn 6 · chiều Na đạp xe | 92 | toàn cảnh | — |
| `cong-vien-chieu-tron.svg` | Màn 6 · công viên chiều, sân khấu (21/10) | 92 | sân khấu: Na đạp xe | — |
| `trang-sach.svg` | Màn 6 · trong cuốn sách | mặt ao 78 | toàn cảnh | — |
| `roi-ben.svg` | Màn 7 · rời bến | mặt sông 59 | toàn cảnh | — |
| `roi-ben-tron.svg` | Màn 7 · rời bến, sân khấu: bỏ phà, phao, lục bình giữa, vệt sóng (21/10) | mặt sông 59 | sân khấu: thuyền, câu hỏi trên thuyền | — |
| `ra-khoi.svg` | Màn 7 · ra khơi | mặt biển 70 | toàn cảnh | — |
| `ra-khoi-can.svg` | Màn 7 · cận: mặt nước sát mạn thuyền, mép thuyền gỗ ở đáy khung (y ≈ 128), đảo nhỏ ở chân trời (21/10) | mặt biển 56 | cận: cá heo (cá heo do game vẽ) | — |
| `dao-bai-cat.svg` | Màn 7 · trên đảo: bãi cát | ≈ 98 | toàn cảnh | — |
| `dao-bai-cat-tron.svg` | Màn 7 · bãi cát, sân khấu: bỏ đá, vỏ sò (21/10) | ≈ 98 | sân khấu: sao biển, cua, vỏ sò, dừa, lâu đài cát | — |
| `dao-hai-dang.svg` | Màn 7 · trên đảo: hải đăng, cầu gỗ | ≈ 98 | toàn cảnh | — |
| `dao-hai-dang-tron.svg` | Màn 7 · hải đăng, sân khấu: bỏ cầu gỗ (21/10) | ≈ 98 | sân khấu: khoá hải đăng | — |
| `hang-kho-bau.svg` | Màn 7 · chỗ đặt rương | 112 | toàn cảnh | — |
| `dao-bai-cat-hai-dang.svg` (+ `-tron`) | Màn 7 · thuyền cập bãi cát; hải đăng cùng hòn đảo (22/10): bãi cát phía trước, đồi xanh nhô lên ngay từ bãi ở bên phải, **hải đăng trên đỉnh đồi (chân tháp, cửa ở (186, 54))**, đường mòn sáng màu nối từ bãi cát **(110, 112)** lên tới cửa hải đăng. Biển ở trái phía sau. Bản `-tron` bỏ một cây dừa, vỏ sò | cát ≈ 100; chân đồi 104 | toàn cảnh / sân khấu: thuyền cập bến ở bên trái (mép nước y ≈ 98) | — |
| `duong-len-hai-dang.svg` | Màn 7 · cảnh xa đi lên hải đăng (22/10): đồi xanh, đường mòn có đá viền, hải đăng to ở trên. **Các điểm của đường (đi theo thứ tự): (8, 134) → (88, 118) → (56, 104) → (126, 92) → (104, 80) → (158, 68)**; cửa hải đăng ở (160, 68) | theo đường mòn | các bạn đi theo đường lên tới cửa | — |
| `hai-dang-cat-doc.svg` | Màn 7 · hải đăng cắt dọc, kiểu nhà Na (22/10). **Cửa 1 (tầng trệt, tường trái): x 67–74, y 107–128.** Cầu thang 1: từ (86, 128) lên (116, 102) (sàn tầng giữa y 98). Cầu thang 2: từ (116, 98) lên (88, 72) (sàn tầng trên y 68). **Cửa 2 (tầng trên, tường phải, ra ban công): x 126–133, y 49–68** — chỉ để xem, game mở cửa rồi sang cảnh nhìn từ cửa sổ. Phòng đèn trên đỉnh | đất 128; tầng giữa 98; tầng trên 68 | các bạn đi cầu thang lên cửa thứ hai | — |
| `nhin-tu-cua-so.svg` | Màn 7 · nhìn từ cửa sổ hải đăng xuống bãi biển (22/10): khung cửa vòm gỗ, ngoài là biển, bãi cát, vách đá có cửa hang ở bên phải. **Hòn đá to: tâm (111, 90), x 94–130, y 76–102; dấu X đỏ cạnh đá: tâm (120, 110); cửa hang: x 136–162, y 88–112.** Dấu chân trên cát từ trái tới | — | cảnh nhìn (game có thể nhấp nháy dấu X) | — |
| `cua-hang.svg` | Màn 7 · cửa hang ở cuối bãi biển (22/10), trước khi lật thẻ: vách đá bên phải, **miệng hang x 118–194 (lòng tối x 130–182), chân ở y 100**, một lối cát sáng dẫn vào hang. Cây dừa ở mép trái | cát 100 | đi vào hang → lật thẻ → rương (`hang-kho-bau`) | — |

## Quyết định 21/10 (trang "Chọn phương án hình")
- Màu: **C**, giữ như hiện tại (luật 3 đã sửa theo). Thư mục `thu-mau/` đã xoá.
- Vườn trường: chân trời lên **y 62**, cỏ cắt sọc; bản sân khấu **không hố cát**.
- Mái kính chữ A giữ rõ (không nhạt theo lớp xa). Cổng trường giữ thiết kế cũ, kể cả cụm đỏ trên biển tên.
- Cầu trượt và cây cầu vẽ một lần trong `do-choi/`.
- Xe: xem `art/props/README.md`.
- Vòng 2 (21/10 chiều): đồng ý vườn trường mới, đường tới trường + bản sân khấu, đường ven công viên, taxi, xe chở hàng, cầu trượt và cây cầu. Cổng trường bản sân khấu sửa lại: giữ nguyên thiết kế cổng, chỉ dịu màu một chút (cổng là chỗ ai cũng nhận ra).

## `ban-do/` · bản đồ kho báu 8 mảnh (22/10)
Cùng khung với bản đồ đang có trong app (`viewBox="0 0 220 150"`, 8 ô 48×58 bắt đầu từ x 14, y 14, `MAP_CELLS` như cũ: hàng trên trái → phải là mảnh 1–4, hàng dưới phải → trái là mảnh 5–8), nên thay thẳng cho `islandArt()`; cắt từng mảnh bằng `mapJag(k)` như hiện nay.

| File | Nội dung |
|---|---|
| `ban-do.svg` | Cả tấm bản đồ: biển xanh, đất liền cho mảnh 1–7 (1 trường học, 2 công viên, 3 khu vườn, 4 nhà Na, 5 cửa hàng, 6 công trường, 7 một ngày của Na), **Đảo Kho Báu (mảnh 8, ô dưới cùng bên trái) là đảo riêng, có biển bao quanh tách khỏi đất liền**; trên đảo có cây dừa, hải đăng nhỏ, rương và dấu X đỏ. Một chiếc thuyền nhỏ ở eo biển giữa đất liền và đảo. Không có đường chấm đỏ. |
| `duong-1.svg` … `duong-7.svg` | Đường chấm đỏ từng đoạn, cùng khung 220×150: `duong-k` đi từ tâm mảnh k tới tâm mảnh k+1 (`duong-7` từ mảnh 7 qua thuyền ra đảo). Khi bé có mảnh mới nhất là n, đặt chồng `duong-1` … `duong-(n-1)`; không vẽ trước tới mảnh chưa có. |

Tâm các mảnh (điểm đầu, cuối của đường): 1 (38, 43), 2 (86, 43), 3 (134, 43), 4 (182, 43), 5 (182, 101), 6 (134, 101), 7 (86, 101), 8 (37, 108).

## `do-choi/` · đồ chơi sân trường, để game đặt riêng (đồ vật, đứng trên mặt đất; tỉ lệ khoảng 32 đơn vị = 1 m)
| File | Gợi ý dùng |
|---|---|
| `nha-nam.svg` | ú òa (bạn ló ra từ cửa), in/on (mèo trong nhà nấm, trên mái) |
| `doi-co-ham.svg` | kẻ đường: leo thang lên đồi rồi chui ra hầm; trốn tìm; in/under |
| `cong-con-cua.svg` | kẻ đường: chui cổng cua → qua cầu khúc gỗ → chui ống; đếm khúc gỗ, gọi tên màu |
| `khung-leo.svg` | on/under, leo thang |
| `khung-hat.svg` | khung hạt đỏ trắng: đếm đến 5 (Unit 1), đến 10 (Unit 2) |
| `cau-truot-phai.svg` / `cau-truot-trai.svg` | cầu trượt (thang bên trái, máng trượt sang phải / bản lật): Ben trượt xuống, kẻ đường dọc |
| `cay-cau.svg` | cây cầu gỗ nhỏ: qua cầu, kẻ đường ngang (trang này dùng nền `vuon-truong-tron-ho.svg`, chân cầu đứng trên hai bờ hồ) |
| `doc-co.svg` | dốc cỏ thấp (tối 21/10), khung **80×22**, cao ở trái, thoải dần xuống đất ở phải: đỉnh dốc x 12, y 4; chân dốc x 80, y 22 (đáy khung là mặt đất). Đặt dưới đầu bục cầu trượt để quả bóng rơi xuống đỉnh dốc rồi lăn về phía trước. Cùng tỉ lệ với cầu trượt (32 đơn vị = 1 m), nên dùng cùng hệ số: với cầu trượt đang ở `SLIDE_AT={x:44,b:8,w:44}`, chỗ thả bóng (sx 41) ở x 74 của cảnh, đặt dốc `sceneThing(PROP['doc-co'], 47.3, 8, 29.3)` (x là tâm: mép trái x 65,2 của cảnh, rộng 58,7; đỉnh dốc ngay dưới chỗ thả bóng, ở x 74, y 115,6; chân dốc x 123,9, y 128,8) |

## `sau/` · địa danh, chưa dùng trong Unit 1
`buu-dien.svg`, `thao-cam-vien.svg` (cổng sắt), `nha-tho-duc-ba.svg`, `cho-ben-thanh.svg`, `metro.svg`, `pho-di-bo.svg` (nhìn về Bitexco).
