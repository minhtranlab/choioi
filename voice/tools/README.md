# Công cụ tạo giọng Chồi (bản 3)

Tạo giọng Chồi bằng máy, chạy lại được: chỉ câu mới, câu đã đổi, hoặc câu đổi giọng/tốc độ mới được tạo lại.

| | Tiếng Anh | Tiếng Việt |
|---|---|---|
| Mô hình | Kokoro-82M (Apache-2.0) | VieNeu-TTS v3 Turbo (Apache-2.0) |
| Giọng Chồi | `af_heart`, speed 0.70 (≈120 từ/phút) | `Đoan Trang` (Bắc, tự nhiên, ≈3,4 tiếng/giây) |
| Giọng các bạn nhỏ | xem mục "Giọng các bạn nhỏ" | xem mục "Giọng các bạn nhỏ" |

Cấu hình nằm trong `config.json`. Đổi giọng, tốc độ hoặc `gap` thì mọi câu sẽ được tạo lại ở lần `make` sau.

## Cách làm từng câu
1. Tên bé trong app được thay bằng `{N}`. Bản ghi bỏ tên đi: "Great job, {N}!" đọc thành "Great job!", "Chào {N}!" thành "Chào con!".
2. Câu được tách thành từng câu nhỏ (ở `.`, `!`, `?`). Mỗi câu nhỏ đọc riêng rồi ghép lại, giữa các câu nghỉ 0,6 giây.
3. Tốc độ do mô hình đọc, không kéo giãn hay nâng giọng sau khi đọc.
4. Kokoro đọc chậm hay chèn một tiếng "ơ" trước từ đầu câu. Vì vậy câu được đọc sau một từ mồi ("Okay.") rồi cắt bỏ từ mồi ở chỗ ngắt đầu tiên.
5. Máy nghe lại từng câu nhỏ (Whisper base.en cho tiếng Anh, Zipformer tiếng Việt). Bản nghe đúng chữ nhất được giữ. Câu nghe chưa thật đúng sẽ được in ra để người nghe lại.
6. Mọi câu được chỉnh cùng độ to, rồi lưu mp3 mono 24 kHz: tiếng Anh 48 kbit/s, tiếng Việt 32 kbit/s (`mp3_kbps` trong `config.json`, chốt 22/10).

## Chạy
Cần: Python 3.10+, `ffmpeg`, `pip install kokoro-onnx vieneu sherpa-onnx soundfile soxr numpy`, và các mô hình trong `~/models` (đổi bằng biến `CHOI_MODELS`):
- `kokoro-v1.0.onnx`, `voices-v1.0.bin`: github.com/thewh1teagle/kokoro-onnx/releases (model-files-v1.0)
- `sherpa-onnx-whisper-base.en`, `sherpa-onnx-zipformer-vi-2025-04-20`: github.com/k2-fsa/sherpa-onnx/releases (asr-models)
- `VieNeu-TTS-v3-Turbo` (huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo) và `MOSS-Audio-Tokenizer-Nano-ONNX` (huggingface.co/OpenMOSS-Team/MOSS-Audio-Tokenizer-Nano-ONNX). Tải bằng `snapshot_download(..., local_dir=...)` để được file thật, không phải symlink (onnxruntime ≥1.29 không đọc được symlink của cache).

```bash
cd voice/tools
python3 tao_giong.py lines --log thu-cau.json thu-mix.json so-thu.json   # danh sách câu (--parts chung,man0 để chỉ lấy vài phần)
python3 tao_giong.py make --lang en,vi      # tạo câu còn thiếu (thư mục tạm ~/.cache/choi-voice), theo thứ tự chung, Màn 0, Màn 1…
python3 tao_giong.py pack --lang en,vi      # thêm câu mới/đã sửa vào voice/en.json, voice/vi.json, trong các file mp3 mới ở cuối
python3 tao_giong.py page                   # voice/nghe-thu.html: nghe từng câu giọng mới
```

**Khi có câu mới hoặc câu sửa:** cập nhật `voice/pending-unit1.json`, chạy lại 4 lệnh trên. Chỉ câu mới/đã đổi được tạo; các file mp3 đã có trên GitHub giữ nguyên, câu mới nằm trong file mp3 mới ở cuối.

- `lines` giữ mọi câu đã có giọng mới (`manifest-<lang>.json`), thêm câu trong `voice/pending-unit1.json` (các phần trong `--parts`, bỏ trống là tất cả), và mọi câu trong các file `--log`.
- `thu_cau.py` cho app tự chơi các màn trong trình duyệt không đầu và ghi lại mọi câu Chồi nói, để không sót câu nào không có trong `pending-unit1.json` (vd. "See you next time!"): `python3 thu_cau.py 8 0,1,2,3 thu-cau.json` (cần `python3 -m http.server 8765` ở thư mục gốc repo và `pip install playwright`). Kết quả đã chạy cho cả 8 màn: `thu-cau.json` (có cả câu của các bạn nhỏ, cờ `k`). `thu_mix.py` chơi hết 8 màn rồi chơi Fun Mix 3 lần (có trò thưởng): `thu-mix.json`.
- `so_thu.py` liệt kê mọi câu cho thú ăn ở sở thú (8 loài × 7 món), lấy từ dữ liệu của app: `so-thu.json`.
- `pack` mặc định chỉ thêm, không ghi đè file mp3 cũ: câu mới hoặc câu đã sửa nằm trong file mới ở cuối, mỗi file chỉ chứa câu của một nhóm, và số file được nối vào cuối nhóm đó trong khoá `p`. `pack --compact` ghi lại toàn bộ theo cấu trúc ở mục dưới (chạy lần đầu 22/10; chạy lại khi đã sửa nhiều lời, để bỏ các đoạn câu cũ đã bị thay).
- `thu_thu_tu.py` cho app tự chơi 8 màn × 8 lần và ghi lại thứ tự câu nói (`thu-thu-tu.json`); `pack` dùng file này để xếp câu theo thứ tự nói và chia nhóm. Có màn mới hoặc đổi nhiều lời thì chạy lại trước `pack --compact`.
- `make --redo '<mẫu>'` tạo lại những câu khớp mẫu (vd. khi đổi cách đọc câu vỗ tay), rồi `pack` thay bản cũ.
- `pack` chỉ đóng gói clip đang chờ trong `~/.cache/choi-voice/<lang>/`; clip đã đóng gói chuyển sang `…/packed/`.

## Cấu trúc file giọng (đóng gói theo màn, 22/10)
`voice/en.json`, `voice/vi.json`: `{"n": số file, "c": {hash: [file, vị trí byte, độ dài]}, "p": {nhóm: [các file, theo thứ tự]}, "h": [dấu vân tay từng file]}`. File mp3: `voice/en-00.mp3` … (2 chữ số, quá 99 thì 3 chữ số).

Mỗi nhóm là các file liền nhau, mỗi file khoảng 400 KB. Trong nhóm, câu xếp theo thứ tự được nói (lấy từ 64 lần app tự chơi). Ai cũng tải được mọi câu: câu nào nằm ở file chưa tải thì app tải file đó khi cần.

| Nhóm (`p`) | Gồm | EN (48 kbit/s) | VI (32 kbit/s) |
|---|---|---|---|
| `chung` | câu dùng ở từ 2 màn trở lên (khen, nhắc, đếm, Polly và bạn nhỏ nói ở nhiều màn), câu bạn nhỏ không gặp trong lần tự chơi (vd. khi bé chạm vào bạn ấy) | 3 file, 1,10 MB | 2 file, 0,54 MB |
| `man0` … `man7` | câu chỉ màn đó dùng (kể cả câu Polly, bạn nhỏ chỉ có ở màn đó). **File đầu = đầu màn** | 5–11 file/màn, 1,7–4,1 MB | 3–6 file/màn, 1,0–2,3 MB |
| `sothu` | phần cuối mỗi màn: thành phố, sở thú, cho thú ăn (từ câu "This is your city!") | 6 file, 2,23 MB | 4 file, 1,32 MB |
| `ngoai` | câu 64 lần tự chơi không gặp: giảng lại khi bé sai nhiều, Fun Mix, My Games, hộp nhạc… | 7 file, 2,57 MB | 4 file, 1,44 MB |
| `cu` | giọng cũ chưa được thay (khoảng 1.300 đoạn) và giọng bạn nhỏ chung cũ (`@câu`). **Không tải trước**; chỉ tải khi một câu cần tới | 12 file, 11,5 MB | 10 file, 9,3 MB |

- Giọng bản 3 (không tính `cu`): EN 29,3 MB, VI 15,9 MB. Tất cả file giọng: EN 43,4 → 40,8 MB, VI 35,2 → 25,2 MB.
- `chung` + file đầu của màn chứa ít nhất 70–170 giây giọng Chồi đầu màn (EN 19–58 câu, VI 41–101 câu). Trong lúc bé chơi phần đó, 4G chậm (1,6 Mbit/s) tải xong một file 400 KB trong khoảng 2 giây.
- `h`: dấu vân tay nội dung từng file (8 ký tự). App ghép vào đường dẫn (`?v=`), nên file nào đổi thì máy bé tải lại đúng file đó, file không đổi giữ trong máy.
- **Nhóm `cu`:** chưa xoá vì nhiều câu trong app ghép từ chữ lúc chạy (vd. `Look, it’s a ${w}.`), không thể biết chắc đoạn cũ nào không còn dùng. Khi đã thử đủ thành phố, My Games, hộp nhạc, Cài đặt mà không gặp câu giọng cũ nào, có thể bỏ cả nhóm này.

**Gợi ý cho app (chat U1):**
1. Màn chờ: chỉ chờ `p.chung` và `p['man'+li][0]`. Các file sau của màn tải nối tiếp trong lúc bé chơi, theo thứ tự trong `p`.
2. Tải ngầm theo thứ tự: phần còn lại của màn đang chơi, rồi `sothu`, rồi file đầu của màn kế tiếp. `ngoai` tải khi vào Fun Mix / My Games / hộp nhạc, hoặc sau cùng. Không tải trước `cu`.
3. Câu nằm ở file chưa tải: tải ngay file đó (app hiện đã làm vậy, chờ 1,5 giây rồi hiện chữ).

## Phần trong index.html (đã làm 21/10, commit 186183a; chat U1 sửa lại 22/10, commit 1c80eaf)
1. **Tải trước theo màn, có màn chờ.** Màn có `I.p['chung']` và `I.p['man'+li]`: app chờ các file đó trước khi vào màn (màn chờ có trò chạm bong bóng), rồi tải ngầm màn kế tiếp. Giọng đã tải được giữ trong máy (Cache Storage, theo `h`).
2. **Không lẫn giọng máy.** Câu thiếu bản ghi hoặc chưa tải kịp chỉ hiện chữ; không bao giờ đọc cả màn bằng giọng máy (bỏ từ 22/10).
3. **Giọng bạn nhỏ.** App tìm khoá `"@" + khoá câu` (hash của chuỗi đó) cho câu của Lam, Na, Ben trước; có thì phát nguyên tốc độ, chưa có thì dùng bản của Chồi nâng 1.12. Polly giữ 1.32. Khi ghi giọng `kid`, `pack` cần ghi câu đó dưới khoá có `@`.
4. **Tốc độ Chậm / Vừa / Nhanh (hoãn 22/10, chưa có bộ nào).** App đọc `voice/<lang>-s.json` với `voice/<lang>-s-NN.mp3` (Chậm), `voice/<lang>-f.json` với `voice/<lang>-f-NN.mp3` (Nhanh), cùng định dạng `en.json` (có khoá `p`); Vừa là bộ hiện có. Nghỉ sau câu 800 / 650 / 520 ms. Dòng chọn tốc độ trong Cài đặt chỉ hiện khi có đủ bộ Chậm và Nhanh.

## Giọng các bạn nhỏ (chốt 22/10)
- Mỗi người nói một giọng riêng, khoá `"@" + tên + ":" + câu` (`@Lam:Yes!`, `@Na:Ừ.`, `@Bac:…`). Danh sách câu: `cau-ban-nho.json`, tạo bằng `ban_nho.py`: câu chung `ANY` ghi cho cả ba bạn; câu riêng `OWN` ghi cho đúng người đó; câu sở thú lấy từ dữ liệu app. Thêm câu mới cho bạn nhỏ thì sửa `ban_nho.py`, chạy lại, rồi `lines` → `make` → `pack`.
- Tiếng Anh (`kokoro_kid`): Kokoro đọc ở tốc độ thường, không có từ mồi. Sau đó thu nhỏ khoang giọng (`formant`) và nâng cao độ (`pitch`) thành giọng trẻ 5 tuổi. Lam: `af_river` 1.15 / 1.45; Na: `af_sky` 1.15 / 1.55; Ben: `bf_isabella` (Anh-Anh) 1.12 / 1.25.
- Tiếng Việt (`vieneu_clone`): VieNeu đọc theo giọng mẫu trẻ con trong `kid-ref/` (mẫu làm từ giọng VieNeu Hải Đăng, Trúc Ly, Minh Đức đổi khoang giọng và cao độ). Giọng ra do mô hình đọc, không xử lý sau.
- Câu của bạn nhỏ được đọc liền một hơi khi máy nghe đủ rõ; nếu không thì đọc từng câu nhỏ, nghỉ 0,4 giây.
- Bác lái cần cẩu (`Bac`): Kokoro `am_michael`, VieNeu `Hải Đăng`.
- App cần sửa để tìm các khoá này: xem `claude/prompt-chat-chinh-giong-ban-nho.md` trong Project.
