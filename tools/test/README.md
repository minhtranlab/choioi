# Kiểm tra trước khi đẩy

## Kiểm giọng thật: `giong_that.py` (bắt buộc trước mỗi lần đẩy, từ 28/10)

Chơi các màn với **giọng ghi âm thật**, đi đúng đường phát như trên máy phụ huynh, và báo mọi câu **chỉ hiện chữ, không có tiếng**.

Máy tự chơi nhanh (`#fast`, `#auto`, `#time`) không dùng giọng ghi âm, nên không bắt được câu im. Ví dụ ngày 28/10: bé tên Na thì nhiều câu ở Màn 0 chỉ có chữ, máy tự chơi nhanh vẫn báo "không lỗi".

```bash
python3 tools/test/giong_that.py                                   # 8 màn, Chromium, tiếng Anh, bé tên Na (~25–35 phút)
python3 tools/test/giong_that.py --lang vi --name Ben              # tiếng Việt
python3 tools/test/giong_that.py --browser webkit --levels 0-1     # WebKit (bộ máy của Safari), Màn 0–1
python3 tools/test/giong_that.py --speed 1 --vrate 1 --levels 0    # tốc độ thật hoàn toàn
```

**Cách chạy:**
- Mở app như máy mới (bộ nhớ trống), vào trang chào, gõ tên bé, bấm **Chơi ngay** thật. Cú chạm thật mới mở được âm thanh, như trên máy thật.
- Mỗi màn qua màn chờ tải giọng (`voiceGate`), nên chạy ở chế độ giọng ghi âm (`VOICE.mode 'rec'`). Các màn sau, bé chạm trên bản đồ.
- Sau màn chờ, app tự chạm.
- **Tua** cho nhanh: `--speed` (chờ và chuyển động ngắn lại, mặc định 0,3) và `--vrate` (tiếng phát nhanh hơn, mặc định 2,5).
- Mỗi câu vẫn đi đúng đường thật: tìm bản ghi → tải file → giải mã → phát.

**Một câu tính là có tiếng** khi tiếng của đúng câu đó thật sự bắt đầu phát (bắt `AudioBufferSourceNode.start`).

**Câu im được báo kèm lý do:**
- chưa có bản ghi;
- file giọng chưa tải kịp;
- âm thanh bị chặn;
- màn không ở chế độ giọng ghi âm.

**Kết quả:**
- In ra màn hình và ghi file JSON (`--out`).
- Thoát với mã 1 khi có câu im.

**Tên mặc định là Na**, trùng tên một bạn trong đội, nên bắt được cả lỗi tên bé lẫn câu thiếu bản ghi.

**Câu nào thật sự chưa có bản ghi** thì đưa vào `voice/pending-unit1.json` cho chat Giọng.

**Cần:** `pip install playwright` và `python3 -m playwright install chromium webkit`.

## Bé chạm liên tục: `be_cham_lien_tuc.py` (29/10)

Chơi Màn 0 ở **tốc độ thật**, giọng ghi âm thật, với một bé chạm suốt (bấm chuột thật, như ngón tay). Báo câu nào của Chồi bị cắt vì bé chạm.

Luật (mục 131 tài liệu thiết kế): câu dẫn chuyện và câu lệnh của Chồi không bao giờ bị cắt vì bé chạm. Bé chạm đồ vật khi Chồi đang nói thì vẫn có tiếng động nhưng nhỏ hơn. Câu Chồi gọi tên đồ vật ("A taxi!") thì bỏ qua.

```bash
python3 tools/test/be_cham_lien_tuc.py                       # Màn 0, Chromium, bé tên Na (~10 phút)
python3 tools/test/be_cham_lien_tuc.py --browser webkit      # WebKit (bộ máy của Safari, iPad)
python3 tools/test/be_cham_lien_tuc.py --levels 0,1
```

**Cách chạy:**
- Mở app như máy mới, gõ tên bé, bấm **Chơi ngay**, qua màn chờ tải giọng.
- App tự trả lời để màn đi tiếp.
- "Bé" bấm thật:
  - ở trang phố: bấm xe mỗi ~0,45 giây, cả lúc Chồi nói "Here comes my school bus!";
  - ở các trang khác: bấm các bạn, đồ vật trong tranh mỗi ~1,3 giây.

**Kết quả:**
- Số câu của Chồi bị cắt ngay sau cú chạm của bé (phải là 0).
- Số tên đồ vật bị bỏ qua lúc Chồi đang nói.
- Độ to tiếng còi lúc Chồi nói.
- Thoát mã 1 khi có câu của Chồi bị cắt vì bé chạm.

**Chạy khi** sửa phần tiếng (`say`), phần chạm, hoặc trang phố.

