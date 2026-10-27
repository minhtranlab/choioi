# Cảnh hài Unit 1 (27/10) · bản mẫu animation

Sáu cảnh hài ngắn đã chốt ở `claude/chot-canh-hai-unit1-27-10.md`. Do chat **[App] Cảnh hài** làm. Chưa gắn vào `index.html` (chat U1 gắn sau).

- Xem thử: mở `xem-thu.html` (một file, chạy riêng). 6 nút Màn 1–6, bấm là chạy, bấm lại là chạy lại; công tắc **Chậm (x0,5)**; công tắc **Thử "giảm chuyển động"**. Chưa có tiếng: chỗ có tiếng hiện chữ nhỏ.
- Luật đã giữ: bé chỉ xem; mỗi cảnh 5,6–9 giây; diễn ngay trong cảnh đang có; không làm mẫu việc nguy hiểm; Polly chỉ nói đúng từ đang dạy ("Triangle!", "Ba-na-na!", "Tired!"); không thu giọng mới, trừ "Oh!" (xem bảng tiếng).

## File

| File | Là gì |
|---|---|
| `canh-hai-chung.js` | phần chung: hẹn giờ, chuyển động (Web Animations), Polly có mọi tư thế, chữ tiếng động, mượn phần tử có sẵn, dọn dẹp. Không thư viện ngoài |
| `canh-hai-hinh.js` | `CanhHai.HINH`: các hình kit cảnh dùng. **Tự sinh** từ `art/kit/` bởi `dong_goi.py`, đừng sửa tay |
| `man-1.js` … `man-6.js` | mỗi cảnh một khối JS tự chứa (CSS riêng tự chèn một lần) |
| `xem-thu.mau.html` | khung trang xem thử; `dong_goi.py` nhúng JS, nền và hình vào thành `xem-thu.html` |
| `ve_hinh.py` | vẽ lại các hình mới trong `art/kit/` (xem `art/kit/README.md`, mục *Cảnh hài*) |
| `dong_goi.py` | chạy `python3 art/canh-hai/dong_goi.py` sau khi sửa hình hay cảnh (cần node; chỉ đọc `index.html` để lấy vài hình dựng sân khấu xem thử) |

Gắn vào app cần 3 file theo thứ tự: `canh-hai-chung.js`, `canh-hai-hinh.js`, rồi `man-N.js` của các màn dùng.

## Cách gọi (chung cho cả 6 cảnh)

```js
const r = await CanhHai.man3(box, { meo, ro, speed: SPEED, am: amCanhHai });
// r.xong: chạy xong · r.boQua: máy bật giảm chuyển động, cảnh không chạy · r.xoa(): gỡ những gì cảnh còn để lại
```

- `box`: khung cảnh đang có (trong app là `.sbox` / `.popfield` / `rfield`). Vị trí đều tính theo **% của box** như `kidAt()`: `x` là tâm, `b` là đáy tính từ dưới, `w` là bề rộng.
- `speed`: hệ số thời gian, truyền `SPEED` của app (1 = bình thường, 2 = chậm x0,5).
- `am(key, chu)`: được gọi ở mỗi chỗ có tiếng động hay câu nói; app phát tiếng ở đây (bảng dưới). Có `am` thì mặc định **không** hiện chữ; muốn hiện thêm chữ thì truyền `chu: true`.
- `signal`: `AbortSignal` để huỷ giữa chừng (bé bấm Tiếp, đổi trang). Huỷ thì cảnh tự dọn sạch, Promise vẫn trả về.
- **Giảm chuyển động:** máy bật `prefers-reduced-motion` thì cảnh không chạy, trả về ngay `{boQua:true}`, app đi tiếp. Ép bằng `giamChuyenDong: true/false` (trang xem thử ép `false` để Minh xem được cả khi máy bật; công tắc "Thử giảm chuyển động" ép `true`).
- Chế độ `#fast` / `#auto` của app: nên bỏ qua cảnh (`giamChuyenDong: FAST`), vì `SPEED` 0,04 làm cảnh chớp qua.
- Phần tử app truyền vào (mèo, rổ, xe, mái nhà) được **mượn**: cảnh đặt một bản sao đúng chỗ để tự chuyển động, bản gốc ẩn tạm. Cảnh xong thì trả lại, trừ khi bảng dưới ghi "để lại".
- Hình của cảnh nằm ở z-index 5–8 (`.skid` là 2, `.tpolly` là 6). Muốn viền sticker trắng như các bạn trong app, thêm CSS: `.sbox .ch-sp:not(.ch-muon) .ch-q{filter:<như .stk>}`.
- **Chỉ một Polly trên màn:** nếu trang đang có Polly đứng (`.tpolly`, `.actor.polly`), ẩn đi trong lúc cảnh chạy (giống `pollyEcho`).

## Sáu cảnh

| Màn | Gọi | Dài (x1) | Cần truyền | Tiếng (`am` key → gợi ý trong app) | Cuối cảnh |
|---|---|---|---|---|---|
| 1 Công viên · bong bóng vỡ trên mỏ | `CanhHai.man1(box, o)` | 6,6 s | không bắt buộc. `bongBong:[{x,b,w}…]` 3 quả (quả cuối to), mặc định (72,46,8) (50,56,7) (30,42,13) | `bup` ×2 → `SFX.pop()` · `bup-to` → `SFX.pop()` to hơn hoặc `noise(.12,.5)` · `lac` "[phì phì]" → `noise(.2,.15,0,2500)` | không để lại gì |
| 2 Vườn đêm · Polly tập ngủ như dơi | `CanhHai.man2(box, o)` | 9,0 s | `canh` (phần tử cành kit `do-vat/canh-cay`, hoặc `{x,b,w}`), `doi` (phần tử dơi; không có thì cảnh tự vẽ), `doiTai` .58, `dauTai` .84 | `vut` ×2 → `tone(700,.12,'sine',.08,0,300)` · `tired` → Polly nói "Tired!" hai lần (`say('Tired!','Mệt!',{polly:true})` ×2, câu đã có bản ghi) · `ngu` "[khò… khò…]" → `noise` nhỏ hoặc bỏ | để lại cành, dơi, Polly đang ngủ |
| 3 Nhà Na · mèo đội mũ đồ chơi | `CanhHai.man3(box, o)` | 5,6 s | **bắt buộc** `meo` (`.kcat`), `ro` (`.tbasket`); `vanhRo` .4, `dauMeo` .18 (đúng `ART.basket`, `CAT_SVG`), `mu` svg mũ (mặc định vịt `ART.duck`) | `meo` → tiếng mèo nhỏ (tone trượt lên) · `bich` → `SFX.soft()` · `luc-cuc` → `noise(.3,.1,0,600)` · `chit` (vịt cao su) → `tone(1400,.08,'square',.05)` | để lại mèo đội mũ thò đầu trong rổ |
| 4 Cửa hàng · Polly tha nải chuối | `CanhHai.man4(box, o)` | 8,4 s | **bắt buộc** `xe` (`.cart`); `xeTrong` = tỉ lệ trong khung xe: lòng `x` .58, `mieng` .25, `day` .64, tay đẩy `tayX` .1 `tayY` .12 (theo `SHOPCART_SVG`; xe của `shopCart` vẽ khác thì chỉnh) | `vo-canh` → `noise` ngắn lặp · `bich` → `SFX.soft()` + `tone(120,.15)` · `tho` "[hộc hộc]" → hai `noise(.15,.1)` | để lại nải chuối trong xe |
| 5 Công trường · mái nhà biết đi | `CanhHai.man5(box, o)` | 9,0 s | **bắt buộc** `mai` (`.s5roof`, đang nằm dưới đất); `ban` [Lam, Na…]; `doiMat(el,f)` → trong app: `setKidFace(el, el.dataset.who, f||'happy')` | `lach-bach` ×2 → `tone` ngắn xen kẽ · `oh` "Oh!" → **chưa có bản ghi** (cần chat Giọng thu "@Lam:Oh!", "@Na:Oh!", "@Ben:Oh!" hoặc "@Oh!" giọng kid; tạm thời bỏ hoặc dùng `tone`) · `triangle` → Polly nói "Triangle!" hai lần (đã có bản ghi) · `cop` → `SFX.soft()` + `noise(.1,.3,0,400)` | mái về đúng chỗ cũ, mặt các bạn như cũ |
| 6 Một ngày · mũ vỏ chuối | `CanhHai.man6(box, o)` | 6,5 s | `vo:{x,b,w}` chỗ vỏ chuối (mặc định 30, 46, 7 = chỗ đĩa chuối `.c6food`), `thung` (phần tử thùng rác kit `do-vat/thung-rac`, hoặc `{x,b,w}` để cảnh tự vẽ), `na` (phần tử Na, nhún theo) | `banana` → Polly nói "Ba-na-na!" (đã có bản ghi) · `cach` ×2 → `tone(900,.05,'square',.05)` | để lại thùng rác (nếu cảnh tự vẽ) |

## Gợi ý chèn vào app (cho chat U1)

Dòng là của `index.html` ngày 27/10 (commit `9f1bb2c`). Không đổi luồng trò: chỉ thêm một `await` trước khi trang đi tiếp.

1. **Màn 1** · `EP[1]` dòng 10466 `reviewIt(…bubbleFaces())`. Trong `bubbleFaces` (7874), sau `await popStream(…)`: chạy `man1` trên khung `.popfield` cuối cùng (vẫn là công viên có chú bán bóng). Bong bóng sót của app đã mờ đi (`.away`), cảnh tự vẽ 3 quả mới, không có mặt (bong bóng trơn).
2. **Màn 2** · `flashlightGame` (6700), `EP[2]` dòng 10483. **Thêm từ đầu trang:** cành kit `canh-cay` chìa ra từ tán cây ở chỗ `tree` (khoảng x 56, b 50, w 34) và con dơi kit `doi-ngu-treo-nguoc` treo dưới cành, để đèn pin soi thấy dơi trong lúc chơi. Chạy `man2(box,{canh, doi})` sau dòng 6749 (`dark.classList.add('off'); confetti()`), trước câu cuối.
3. **Màn 3** · `toyCatch` (6754), `EP[3]` dòng 10497 (có `kitten:true`). Chạy `man3(field,{meo: .kcat, ro: .tbasket})` sau dòng 6808 (`confetti()`), trước khi hàm trả về.
4. **Màn 4** · `shopCart` (6816), `EP[4]` dòng 10508. Chạy `man4(field,{xe: .cart})` sau dòng 6854 (`confetti()`). Kiểm lại `xeTrong` với hình xe của trang này.
5. **Màn 5** · `siteArrive` (8696), trang đầu Màn 5 (`EP[5]` dòng 10512). **Khác với chốt:** trong app mái nhà treo sẵn ở cần cẩu (bottom 70%) chứ không nằm dưới đất. Đề xuất: lúc mở trang đặt mái `.s5roof` dưới đất (bottom khoảng 3%, dây cần cẩu ẩn), chạy `man5(box,{mai, ban:[Lam, Na], doiMat})`, xong thì móc cần cẩu hạ xuống nhấc mái lên chỗ 70% (một bước nhỏ mới), rồi trò chạy như cũ. Trang này chỉ có Lam và Na (Ben không có): "cả đội" là hai bạn đó. **Minh duyệt hướng này trước khi U1 gắn.**
6. **Màn 6** · `bananaClap` (9157), `EP[6]` dòng 10526. **Thêm từ đầu trang:** thùng rác kit `thung-rac` ở góc bếp (khoảng x 87, b 4, w 9). Cuối trò, trước `confetti(); nextPage(box)` (dòng 9191): ẩn đĩa chuối `.c6food` (Na đã ăn), chạy `man6(box,{vo:{x:30,b:46,w:7}, thung, na})`.

## Ghi chú cho Minh
- **Màn 2:** Polly treo ngược trên cành chỉ một lát rồi chóng mặt, lật lại ngay và chọn ngủ kiểu vẹt. Bé thấy treo ngược làm Polly chóng mặt; nếu Minh vẫn ngại bé bắt chước, có thể bỏ đoạn treo ngược, giữ đoạn ngáp và rúc đầu ngủ (cảnh còn khoảng 5 giây).
- **Màn 3:** mèo nhảy từ kệ vào rổ. Nếu Minh ngại bé bắt chước trèo kệ, cho mèo bắt đầu từ sàn cạnh rổ (chỉ đổi chỗ mèo, cảnh tự tính đường nhảy).
- **Màn 5:** cần Minh chọn cách đặt mái dưới đất lúc đầu (mục 5 ở trên).
