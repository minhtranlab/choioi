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
python3 tao_giong.py lines --parts chung,man0,man1 --log thu-cau-man01.json   # danh sách câu
python3 tao_giong.py make --lang en,vi                                  # tạo câu còn thiếu (thư mục tạm ~/.cache/choi-voice)
python3 tao_giong.py pack --lang en,vi                                  # ghi voice/en.json, voice/vi.json, voice/<lang>-NN.mp3
python3 tao_giong.py page                                               # voice/nghe-thu.html
```

- `lines` lấy câu từ `voice/pending-unit1.json` (các phần trong `--parts`). Nếu có `--log`, lấy thêm mọi câu app đã nói trong lần chạy thử, để cả màn chỉ một giọng.
- `thu_cau.py` cho app tự chơi các màn trong trình duyệt không đầu và ghi lại mọi câu Chồi nói: `python3 thu_cau.py 24 0,1 thu-cau.json` (cần `python3 -m http.server 8765` ở thư mục gốc repo và `pip install playwright`).
- `pack` không đụng các file giọng cũ (bản 2, `voice/<lang>-00.mp3` đến `-24.mp3` hoặc `-19.mp3`). Giọng mới nằm ở các file phía sau, số đầu tiên ghi trong `manifest-<lang>.json` (`first`). Câu đã có giọng mới trỏ sang file mới; câu bị bỏ khỏi danh sách trỏ về bản cũ.
- `en.json`/`vi.json` có thêm khoá `p` (phần → các file mp3 của phần đó), để app tải trước đúng file của màn sắp chơi. App bản hiện tại bỏ qua khoá này.

## Việc cần sửa trong index.html (chưa làm, để chat Cấu trúc màn làm)
1. **Tải trước theo màn, có màn chờ.** Hiện `voiceLoad` tải lần lượt mọi file từ `-00`, nên file giọng mới (ở cuối) về sau cùng, còn `runSession` chỉ chờ 15 giây. Nên dùng `I.p['chung']` và `I.p['man'+li]`: chờ đủ các file đó trước khi vào màn (màn chờ vui, có thanh tiến độ), rồi tải phần còn lại ngầm.
2. **Không lẫn giọng máy giữa màn.** Hiện câu không có bản ghi sẽ đọc bằng giọng máy. Nên: câu thiếu thì chỉ hiện chữ (và ghi `console.warn`); chỉ khi cả bộ giọng không tải được thì cả màn đọc bằng giọng máy.
3. **Giọng bạn nhỏ.** `opt.kid` đang tăng `playbackRate` lên 1.12 (nâng giọng). Nếu ghi giọng bạn nhỏ riêng (khoá `@…` trong `config.json` → `kid`), bỏ 1.12. Polly giữ 1.32 vì là con vẹt.
4. **Tốc độ Chậm / Vừa / Nhanh trong Settings.** Công cụ tạo được 3 bộ (speed 0.62 / 0.70 / 0.84 cho tiếng Anh). App cần: `S.vspeed`, đọc `voice/<lang>-<s|m|f>.json`, và khoảng nghỉ sau câu (`GAP`) 800 / 650 / 520 ms theo tốc độ. Có sẵn bản sửa mẫu (tải giọng theo màn, màn chờ, nút tốc độ) trong `index-v3.patch` để tham khảo.
