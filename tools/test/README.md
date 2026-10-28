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
