# Công cụ tạo giọng Chồi (bản 3)

Tạo giọng Chồi bằng máy, chạy lại được: chỉ câu mới, câu đã đổi, hoặc câu đổi giọng/tốc độ mới được tạo lại.

| | Tiếng Anh | Tiếng Việt |
|---|---|---|
| Mô hình | Kokoro-82M (Apache-2.0) | VieNeu-TTS v3 Turbo (Apache-2.0) |
| Giọng Chồi | `af_heart`, speed 0.70 (≈120 từ/phút) | `Đoan Trang` (Bắc, tự nhiên, ≈3,4 tiếng/giây) |
| Giọng bạn nhỏ (`kid`) | `af_sky`, 0.85 | `Trúc Ly` |

Cấu hình nằm trong `config.json`. Đổi giọng, tốc độ hoặc `gap` thì mọi câu sẽ được tạo lại ở lần `make` sau.

## Cách làm từng câu
1. Tên bé trong app được thay bằng `{N}`. Bản ghi bỏ tên đi: "Great job, {N}!" đọc thành "Great job!", "Chào {N}!" thành "Chào con!".
2. Câu được tách thành từng câu nhỏ (ở `.`, `!`, `?`). Mỗi câu nhỏ đọc riêng rồi ghép lại, giữa các câu nghỉ 0,6 giây.
3. Tốc độ do mô hình đọc, không kéo giãn hay nâng giọng sau khi đọc.
4. Kokoro đọc chậm hay chèn một tiếng "ơ" trước từ đầu câu. Vì vậy câu được đọc sau một từ mồi ("Okay.") rồi cắt bỏ từ mồi ở chỗ ngắt đầu tiên.
5. Máy nghe lại từng câu nhỏ (Whisper base.en cho tiếng Anh, Zipformer tiếng Việt). Bản nghe đúng chữ nhất được giữ. Câu nghe chưa thật đúng sẽ được in ra để người nghe lại.
6. Mọi câu được chỉnh cùng độ to, rồi lưu mp3 mono 24 kHz 48 kbit/s.

## Chạy
Cần: Python 3.10+, `ffmpeg`, `pip install kokoro-onnx vieneu sherpa-onnx soundfile soxr numpy`, và các mô hình trong `~/models` (đổi bằng biến `CHOI_MODELS`):
- `kokoro-v1.0.onnx`, `voices-v1.0.bin`: github.com/thewh1teagle/kokoro-onnx/releases (model-files-v1.0)
- `sherpa-onnx-whisper-base.en`, `sherpa-onnx-zipformer-vi-2025-04-20`: github.com/k2-fsa/sherpa-onnx/releases (asr-models)
- `VieNeu-TTS-v3-Turbo` (huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo) và `MOSS-Audio-Tokenizer-Nano-ONNX` (huggingface.co/OpenMOSS-Team/MOSS-Audio-Tokenizer-Nano-ONNX). Tải bằng `snapshot_download(..., local_dir=...)` để được file thật, không phải symlink (onnxruntime ≥1.29 không đọc được symlink của cache).

```bash
cd voice/tools
python3 tao_giong.py lines --parts chung,man0,man1,man2,man3 --log thu-cau-man0123.json so-thu.json   # danh sách câu (bỏ --parts = mọi phần)
python3 tao_giong.py make --lang en,vi      # tạo câu còn thiếu (thư mục tạm ~/.cache/choi-voice), theo thứ tự chung, Màn 0, Màn 1…
python3 tao_giong.py pack --lang en,vi      # thêm câu mới vào voice/en.json, voice/vi.json và các file mp3 mới ở cuối
python3 tao_giong.py page                   # voice/nghe-thu.html: nghe từng câu giọng mới
```

**Khi có câu mới hoặc câu sửa:** cập nhật `voice/pending-unit1.json`, chạy lại 4 lệnh trên. Chỉ câu mới/đã đổi được tạo; các file mp3 đã có trên GitHub giữ nguyên, câu mới nằm trong file mp3 mới ở cuối.

- `lines` giữ mọi câu đã có giọng mới (`manifest-<lang>.json`), thêm câu trong `voice/pending-unit1.json` (các phần trong `--parts`, bỏ trống là tất cả), và mọi câu trong các file `--log`.
- `thu_cau.py` cho app tự chơi các màn trong trình duyệt không đầu và ghi lại mọi câu Chồi nói, để không sót câu nào không có trong `pending-unit1.json` (vd. "See you next time!"): `python3 thu_cau.py 8 0,1,2,3 thu-cau.json` (cần `python3 -m http.server 8765` ở thư mục gốc repo và `pip install playwright`). Kết quả đã chạy cho Màn 0–3: `thu-cau-man0123.json`.
- `so_thu.py` liệt kê mọi câu cho thú ăn ở sở thú (8 loài × 7 món), lấy từ dữ liệu của app: `so-thu.json`.
- `pack` mặc định chỉ thêm, không ghi đè file mp3 cũ. `pack --compact` ghi lại toàn bộ: câu giọng mới xếp trước theo phần (chung, Màn 0, Màn 1…, để bé mới mở app tải màn đầu trước), rồi tới câu giọng cũ chưa được thay. Nên chạy một lần khi đã xong cả 8 màn (đỡ phải tải những đoạn giọng cũ đã bị thay).
- `en.json`/`vi.json` có thêm khoá `p` (phần → các file mp3 của phần đó), để app tải trước đúng file của màn sắp chơi. App bản hiện tại bỏ qua khoá này.
- Màn chưa làm giọng mới (hiện là Màn 4–7) vẫn dùng giọng cũ (bản 2).

## Phần trong index.html (đã làm 21/10, commit 186183a)
1. **Tải trước theo màn, có màn chờ.** Màn có `I.p['chung']` và `I.p['man'+li]`: app chờ đủ các file đó trước khi vào màn (màn chờ có Chồi nhún và thanh tiến độ), rồi tải phần còn lại ngầm, màn sắp chơi trước.
2. **Không lẫn giọng máy giữa màn.** Trong màn đó, câu thiếu bản ghi chỉ hiện chữ (`console.warn`); không tải được giọng thì cả màn đọc bằng giọng máy. Màn chưa có trong `p` giữ cách cũ.
3. **Giọng bạn nhỏ.** App tìm khoá `"@" + khoá câu` (hash của chuỗi đó) cho câu của Lam, Na, Ben trước; có thì phát nguyên tốc độ, chưa có thì dùng bản của Chồi nâng 1.12. Polly giữ 1.32. Khi ghi giọng `kid`, `pack` cần ghi câu đó dưới khoá có `@`.
4. **Tốc độ Chậm / Vừa / Nhanh.** App đọc `voice/<lang>-s.json` với `voice/<lang>-s-NN.mp3` (Chậm), `voice/<lang>-f.json` với `voice/<lang>-f-NN.mp3` (Nhanh), cùng định dạng `en.json` (có khoá `p`); Vừa là bộ hiện có. Nghỉ sau câu 800 / 650 / 520 ms. Dòng chọn tốc độ trong Cài đặt chỉ hiện khi có đủ bộ Chậm và Nhanh.
