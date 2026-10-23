# Đồ vật đời thực (dùng chung cho mọi unit)

Do chat **[App] Bối cảnh & hình vẽ** vẽ. Nét sticker như app; **giữ màu và dáng thật để bé nhận ra, không logo, không tên hãng, không chữ đọc được**.
Mỗi file là một SVG riêng, `viewBox="0 0 W H"`, **bánh xe / chân đứng chạm đúng cạnh dưới** của khung, nên game đặt `y = mặt đất − H × tỉ lệ` là đứng đúng trên đường.

## `xe/` · xe ngoài đường TP.HCM (21/10)
Tất cả vẽ **cùng một tỉ lệ thật: 1 m ≈ 12 đơn vị**. Game nhân một hệ số chung (ví dụ 0,5 khi đặt trên đường của cảnh 200×140) là các xe to nhỏ đúng với nhau.
Mỗi xe có hai file: `-phai.svg` (đầu xe quay sang phải, chạy từ trái sang phải) và `-trai.svg` (bản lật). Xe Việt Nam đi bên phải: làn gần người xem chạy sang phải, làn xa chạy sang trái.

| Tên | Khung W×H | Ghi chú |
|---|---|---|
| `xe-om-xanh` | 26×24 | xe số, người lái mũ áo xanh lá |
| `xe-om-xanh-cho-khach` | 28×25 | xe tay ga, chở khách đội mũ xanh dự phòng |
| `xe-om-xanh-thung` | 30×24 | xe số, thùng hàng sau xe (giao hàng) |
| `xe-om-vang` | 26×24 | như trên, mũ áo vàng |
| `xe-om-vang-cho-khach` | 28×25 | |
| `xe-om-vang-thung` | 30×24 | |
| `taxi-xanh-ngoc` | 46×22 | xe điện nhỏ, cao, mũi ngắn (giống xe thật trong ảnh) |
| `taxi-xanh-ngoc-suv` | 52×23 | SUV nhỏ, mui đen, thanh giá nóc (để đổi cho đỡ lặp) |
| `xe-buyt-xanh-duong` | 134×40 | xe buýt thành phố, khoảng 11 m |
| `xe-buyt-dien-xanh-la` | 98×36 | xe buýt điện xanh lá, khoảng 8 m |
| `xe-dua-don` | 90×42 | xe đưa đón học sinh màu vàng (bản đã duyệt, thu 75% cho khớp tỉ lệ, cỡ xe mầm non khoảng 7,5 m) |
| `o-to-con-trang` | 56×18 | ô tô con gia đình kiểu sedan màu trắng, khoảng 4,6 m (22/10) |
| `o-to-gia-dinh-bac` | 56×21 | ô tô 7 chỗ màu bạc, mui cao, thanh giá nóc, khoảng 4,7 m (22/10) |
| `o-to-nho-cam` | 44×18 | ô tô nhỏ (hatchback) màu cam san hô, khoảng 3,7 m (22/10) |
| `xe-may-thuong` | 26×24 | xe số thường, người lái áo xanh dương, mũ bảo hiểm trắng, không thùng hàng (22/10) |
| `xe-may-me-cho-be` | 28×25 | xe tay ga xanh nhạt, mẹ áo hồng mũ xanh nhạt, bé ngồi sau áo cam đội mũ bảo hiểm hồng (22/10) |
| `xe-dap` | 22×24 | xe đạp xanh dương, người đạp áo trắng, mũ bảo hiểm cam (22/10) |

Bảng tuyến xe buýt để trống (dải tối, không chữ, không số).

**Xe đưa đón cửa mở, bác tài vẫy tay** (vòng 4, 23/10, cho mở đầu Màn 0 mới: bé chạm xe thì cửa mở, bác tài vẫy): `xe-dua-don-mo-phai.svg` / `-trai.svg` (90×42, cùng khung, cùng chỗ bánh với `xe-dua-don`; cửa mở là khe tối có bậc lên, hai cánh gập sang hai bên, x 73,5–82,5, y 19,5–35 trong khung bản `-phai`; một bác tài nhỏ sau kính lái giơ tay vẫy) và `xe-dua-don-can-mo.svg` / `-mo-trai.svg` (240×136, cùng khung với `xe-dua-don-can`; **cửa mở x 188–216, y 66–118, bậc y 111–118**; bác tài giơ tay trái vẫy, bàn tay ở (209, 33)). Đổi file là mở cửa. Ô tô gia đình không có đèn taxi, không chữ, không logo; màu khác hẳn taxi xanh ngọc.

### Xe đưa đón, bản cận (trò xếp bạn lên xe, Màn 0, tối 21/10)
`xe-dua-don-can.svg` (đầu xe quay phải) và `xe-dua-don-can-trai.svg` (bản lật). Khung **240×136**, bánh chạm cạnh dưới. Cùng dáng và màu với `xe-dua-don` (vàng, mui tròn, mũi dốc, sọc hồng và xanh, cửa lên xuống dưới kính lái), vẽ to, **không theo tỉ lệ 12 đơn vị/m** (đây là cảnh cận). Bác tài ngồi sau kính lái, hai tay cầm vô lăng, tóc ngắn, áo xanh nhạt, không chữ, không logo.

4 cửa sổ khách để trống (kính xanh rất nhạt, lưng ghế xanh lộ ở đáy, một vệt sáng nhỏ ở góc trên trái). Toạ độ trong khung 240×136 (x, y, rộng, cao):

| Cửa sổ | `xe-dua-don-can.svg` (quay phải) | `xe-dua-don-can-trai.svg` (quay trái) |
|---|---|---|
| 1 (đuôi xe) | 18, 24, 36, 42 | 186, 24, 36, 42 |
| 2 | 60, 24, 36, 42 | 144, 24, 36, 42 |
| 3 | 102, 24, 36, 42 | 102, 24, 36, 42 |
| 4 (sau bác tài) | 144, 24, 36, 42 | 60, 24, 36, 42 |

Mặt bạn đặt giữa ô, tâm khoảng y 42 (lưng ghế chiếm 10 đơn vị dưới đáy ô, từ y 56), đường kính mặt tới khoảng 30. Kính lái (bác tài) ở x 186–220, y 24–60 bản quay phải (x 20–54 bản quay trái), không dùng để đặt bạn.

## `nguoi/` · người (tối 21/10)
Vẽ theo nét các bạn nhỏ trong app (`kidSVG`): viền #3A1B49 dày 4,5, đầu tròn to, tay là nét dày, quay mặt ra phía người xem. Khung **200×340**, chân chạm y 326 (bạn nhỏ: khung 200×260, chân y 246, cùng khoảng trống 14 ở dưới). **Cùng tỉ lệ với các bạn:** đặt cùng bề rộng (w %) và cùng đáy (b %) như bạn nhỏ trên cùng trang (ví dụ `duong-toi-truong`), chú sẽ cao hơn bạn khoảng 1,3 lần.

**Chú công an giao thông** (trò ếch qua đường, Màn 6): đồng phục vàng (áo vàng, quần vàng đậm), mũ kê-pi vàng có vành tối, găng tay trắng, còi bạc trên dây trắng, gậy chỉ đường trắng có khoang đỏ. Mặt cười. Không phù hiệu, không số, không chữ.

| File | Tư thế | Ghi chú |
|---|---|---|
| `cong-an-giao-thong.svg` | ra hiệu dừng, thổi còi | tay giơ thẳng lên, lòng bàn tay ra trước (mọi xe dừng); còi ở miệng, má phồng; gậy cầm xuôi ở tay kia |
| `cong-an-giao-thong-khen.svg` | giơ ngón cái khen | cười to; gậy cầm xuôi ở tay kia; còi treo ở túi áo |
| `cong-an-giao-thong-dat-tay.svg` | dắt tay | một tay đưa thấp, mở ra để nắm tay ếch: **bàn tay ở khoảng x 186, y 296** của khung (gần mép phải, cao bằng con ếch); tay kia giơ gậy chéo lên chỉ đường |
| `cong-an-giao-thong-buoc-chan-trai.svg` | đi bộ, chân trái bước trước (22/10) | **mặt quay sang phải** (nhìn nghiêng ba phần tư), tay đánh ngược chân, gậy ở tay phải; cùng khung 200×340, đế giày ở y 328 như 3 tư thế kia. Đi sang trái thì app lật ngang |
| `cong-an-giao-thong-buoc-chan-phai.svg` | đi bộ, chân phải bước trước (22/10) | như trên; thay phiên hai file này là thành dáng đi |

Ba file cùng khung, cùng chỗ đứng: đổi file là đổi tư thế, không cần dời vị trí. Muốn quay sang phía kia thì lật ngang (`scale(-1,1)`).

**Người đi bộ** đã chuyển sang thư viện dùng chung `art/kit/nguoi/` (22/10), xem `art/kit/README.md`.