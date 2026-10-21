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

Bảng tuyến xe buýt để trống (dải tối, không chữ, không số).

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
