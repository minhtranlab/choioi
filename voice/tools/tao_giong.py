#!/usr/bin/env python3
"""Tạo giọng Chồi bằng máy (bản 3, 20/10/2026).

  Tiếng Anh : Kokoro-82M, giọng af_heart, tốc độ 0.70 (khoảng 120 từ/phút)
  Tiếng Việt: VieNeu-TTS v3 Turbo, giọng "Đoan Trang" (Bắc, tự nhiên, khoảng 3,4 tiếng/giây)
  Mỗi câu được tách thành từng câu nhỏ, đọc riêng, rồi ghép lại với khoảng nghỉ 0,6 giây.
  Không nâng giọng, không kéo giãn: tốc độ do mô hình đọc.
  Mỗi câu nhỏ được máy nghe lại (Whisper cho tiếng Anh, Zipformer cho tiếng Việt); bản nghe đúng nhất được giữ.

Chạy lại được: chỉ câu mới hoặc câu đã đổi (hoặc đổi giọng/tốc độ) mới được tạo lại.
Câu đã tạo nằm sẵn trong voice/<lang>-NN.mp3; tools/manifest-<lang>.json ghi câu nào là giọng mới.

  python3 voice/tools/tao_giong.py lines --parts chung,man0,man1 [--log thu-cau.json]
  python3 voice/tools/tao_giong.py make  --lang en,vi            # tạo câu còn thiếu (vào thư mục tạm)
  python3 voice/tools/tao_giong.py pack  --lang en,vi            # ghi voice/<lang>.json + voice/<lang>-NN.mp3
  python3 voice/tools/tao_giong.py page                          # voice/nghe-thu.html: nghe mọi câu giọng mới

App đọc voice/<lang>.json như cũ ({n, c:{hash:[bundle,offset,length]}}), nên không cần sửa index.html.
Các bundle cũ (giọng bản 2) giữ nguyên; giọng mới nằm ở các bundle phía sau.
"""
import argparse, collections, hashlib, io, json, os, re, subprocess, sys, time
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
VOICE = os.path.dirname(HERE)
MODELS = os.environ.get('CHOI_MODELS', os.path.expanduser('~/models'))
CACHE = os.environ.get('CHOI_CACHE', os.path.join(os.path.expanduser('~'), '.cache', 'choi-voice'))
CFG = json.load(open(os.path.join(HERE, 'config.json'), encoding='utf-8'))
MAXB = 900_000          # bytes per bundle
SR_OUT = 24000

# ---------------------------------------------------------------- keys (same as index.html vKey / vHash)
def vhash(s):
    h = 2166136261
    b = s.encode('utf-16-le')
    for i in range(0, len(b), 2):
        h ^= b[i] | (b[i + 1] << 8); h = (h * 16777619) & 0xffffffff
    d = '0123456789abcdefghijklmnopqrstuvwxyz'; o = ''
    while True:
        o = d[h % 36] + o; h //= 36
        if not h: return o
def vkey(t, slow=False):
    return ('~' if slow else '') + re.sub(r'\s+', ' ', str(t)).strip()

# ---------------------------------------------------------------- text the engine reads
def spoken(key, lang):
    """the app swaps the child's name for {N}; the recording leaves the name out (it can't know it)"""
    t = key.lstrip('~')
    t = re.sub(r',\s*\{N\}(?=[!?.,…]|$)', '', t)          # "Great job, {N}!" -> "Great job!"
    t = re.sub(r'\{N\},\s*', '', t)                        # "{N}, look!" -> "look!"
    if lang == 'vi':
        t = re.sub(r'\bHi hi\b', 'Hì hì', t)                 # a giggle, read as Vietnamese
        t = re.sub(r'\bChào\s*\{N\}', 'Chào con', t)
        t = t.replace('{N}', 'con')
    else:
        t = t.replace('{N}', 'friend')
    t = t.replace('’', "'").replace('“', '"').replace('”', '"')
    t = t.replace('…', '.').replace('"', '')
    if lang == 'en': t = t.replace('Chồi', 'Choy')
    t = re.sub(r'\s+', ' ', t).strip()
    if t and t[0].islower(): t = t[0].upper() + t[1:]
    return t
def sentences(t):
    return [s for s in re.split(r'(?<=[.!?])\s+', t.strip()) if s] or [t]

# ---------------------------------------------------------------- checking by ear (a recognizer)
NUM = {'0':'zero','1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine','10':'ten'}
UK = {'bên': 'ben', 'bèn': 'ben', 'poly': 'polly', 'pô': 'polly', 'lamb': 'lam', 'nah': 'na', 'whoa': 'whoosh', 'nhá': 'nhé', 'kĩ': 'kỹ', 'colour': 'color', 'colours': 'colors', 'favourite': 'favorite', 'mum': 'mom', 'grey': 'gray', 'okay': 'ok'}
def words(t):
    t = t.lower().replace('’', "'")
    t = re.sub(r"\b(\d+)\b", lambda m: NUM.get(m.group(1), m.group(1)), t)
    return [UK.get(w, w) for w in re.findall(r"[a-zà-ỹđ']+", t)]
def lev(a, b):
    p = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        c = [i]
        for j in range(1, len(b) + 1): c.append(min(p[j] + 1, c[j - 1] + 1, p[j - 1] + (a[i - 1] != b[j - 1])))
        p = c
    return p[-1]
STRAY = {'ok', 'k', 'yes', 'so', 'hmm', 'a', 'uh', 'and', 'i', 'oh', 'um'}
ONO = {'vù', 'vèo', 'brừm', 'grừ', 'bụp', 'bùm', 'tõm', 'whoosh', 'grrr', 'brrm', 'vroom', 'pop', 'boing', 'ồ', 'oa', 'hì', 'hihi', 'ha'}   # sounds: a recognizer can't judge them
def score(expected, heard):
    """share of words heard right; a stray word before the first one (the carrier, an "uh") costs extra"""
    a, b = [w for w in words(expected) if w not in ONO], words(heard)
    if not a: return 1.0
    if words(expected) and words(expected)[0] in ONO and b and b[0] not in a: b = b[1:]
    if not a: return 1.0
    sc = 1 - lev(a, b) / len(a)
    if b and b[0] != a[0] and b[0] in STRAY: sc -= 0.3
    return sc
_asr = {}
def transcribe(a, sr, lang, which=None):
    """which: None = main recognizer; 'w' = Whisper small (second opinion for Vietnamese)"""
    import sherpa_onnx, soxr
    if sr != 16000: a = soxr.resample(a, sr, 16000)
    a = np.concatenate([np.zeros(3200, np.float32), a.astype(np.float32), np.zeros(4800, np.float32)])   # recognizers need a little silence around
    if which == 'w':
        if 'w' not in _asr:
            d = f'{MODELS}/sherpa-onnx-whisper-small/'
            _asr['w'] = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d + 'small-encoder.int8.onnx', decoder=d + 'small-decoder.int8.onnx', tokens=d + 'small-tokens.txt', language='vi', task='transcribe', num_threads=2)
        r = _asr['w']; s = r.create_stream(); s.accept_waveform(16000, a); r.decode_stream(s); return s.result.text.strip()
    if lang not in _asr:
        if lang == 'en':
            d = f'{MODELS}/sherpa-onnx-whisper-base.en/'
            _asr[lang] = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d + 'base.en-encoder.int8.onnx', decoder=d + 'base.en-decoder.int8.onnx', tokens=d + 'base.en-tokens.txt', language='en', task='transcribe', num_threads=2)
        else:
            d = f'{MODELS}/sherpa-onnx-zipformer-vi-2025-04-20/'
            _asr[lang] = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=d + 'encoder-epoch-12-avg-8.onnx', decoder=d + 'decoder-epoch-12-avg-8.onnx', joiner=d + 'joiner-epoch-12-avg-8.onnx', tokens=d + 'tokens.txt', num_threads=2)
    r = _asr[lang]; s = r.create_stream(); s.accept_waveform(16000, a.astype(np.float32)); r.decode_stream(s)
    return s.result.text.strip()

# ---------------------------------------------------------------- audio helpers
def trim(a, sr, th=0.008):
    idx = np.where(np.abs(a) > th)[0]
    if not len(idx): return a
    s = max(0, idx[0] - int(.02 * sr)); e = min(len(a), idx[-1] + int(.08 * sr)); a = a[s:e].astype(np.float32).copy()
    f = int(.008 * sr); a[:f] *= np.linspace(0, 1, f); g = int(.03 * sr); a[-g:] *= np.linspace(1, 0, g)
    return a
def to_sr(a, sr):
    if sr == SR_OUT: return a
    import soxr; return soxr.resample(a, sr, SR_OUT).astype(np.float32)
def loud(a, target=-18.0):
    """same loudness for every clip (RMS of the voiced part), peak kept under -1 dBFS"""
    v = a[np.abs(a) > 0.01]
    if not len(v): return a
    g = 10 ** ((target - 20 * np.log10(np.sqrt(np.mean(v ** 2)) + 1e-9)) / 20)
    a = a * g; pk = np.abs(a).max()
    return a * (0.89 / pk) if pk > 0.89 else a

# ---------------------------------------------------------------- engines
class KokoroEN:
    """Kokoro slows down by itself (speed < 1), but then it often puts a little "uh" before the first word.
    So each sentence is read after a short carrier word ("Okay.") that is cut away at the first pause."""
    def __init__(self):
        from kokoro_onnx import Kokoro
        self.K = Kokoro(f'{MODELS}/kokoro-v1.0.onnx', f'{MODELS}/voices-v1.0.bin'); self.cl = {}
    def _carrier_len(self, carrier, voice, speed):
        k = (carrier, voice, speed)
        if k not in self.cl:
            a, sr = self.K.create(carrier, voice=voice, speed=speed, lang='en-us'); self.cl[k] = len(trim(a, sr)) / sr
        return self.cl[k]
    def _after_carrier(self, s, voice, speed, carrier):
        a, sr = self.K.create(carrier + ' ' + s, voice=voice, speed=speed, lang='en-us')
        cl = self._carrier_len(carrier, voice, speed); hop = int(sr * .01)
        env = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a) - hop, hop)])
        quiet = env < max(env.max() * 0.02, 1e-4); lo = int(cl * 0.45 * 100); hi = min(len(env), int(cl * 1.6 * 100) + 10); i = lo
        while i < hi:
            if quiet[i]:
                j = i
                while j < len(env) and quiet[j]: j += 1
                if j - i >= 5: return trim(a[max(0, j * hop - int(.03 * sr)):], sr), sr
                i = j
            else: i += 1
        return None, sr
    def candidates(self, s, voice, speed):
        """the first one the recognizer hears exactly is kept, so the later ones are only made when needed"""
        for c, sp in (('Okay.', speed), ('Yes!', speed), ('So.', speed), ('Okay.', speed * 1.04), ('Hmm.', speed * 0.97)):
            a, sr = self._after_carrier(s, voice, sp, c)
            if a is not None and len(a) > sr * 0.12: yield a, sr
        for sp in (speed, speed * 1.08):
            a, sr = self.K.create(s, voice=voice, speed=sp, lang='en-us'); yield trim(a, sr), sr

class VieNeuVI:
    """VieNeu-TTS v3 Turbo on CPU (ONNX). Its speed comes from the voice itself, so a calm voice is chosen."""
    def __init__(self):
        import vieneu._v3_turbo_engine.onnx_runtime_lite as L
        orig = L.OnnxV3LiteEngine.__init__
        def init(self_, *a, **k):
            k.setdefault('codec_dir', f'{MODELS}/MOSS-Audio-Tokenizer-Nano-ONNX'); return orig(self_, *a, **k)
        L.OnnxV3LiteEngine.__init__ = init
        from vieneu import Vieneu
        self.V = Vieneu(backbone_repo=f'{MODELS}/VieNeu-TTS-v3-Turbo', onnx_dir=f'{MODELS}/VieNeu-TTS-v3-Turbo/onnx_update', threads=2)
    def candidates(self, s, voice, speed, tries=4):
        n = len(re.findall(r'\w+', s))
        for _ in range(tries + (4 if n <= 3 else 0)):   # short words go wrong more often: more tries
            a = np.asarray(self.V.infer(s, voice=voice), dtype=np.float32); sr = 48000; a = trim(a, sr)
            if len(a) / sr > 1.2 + n * 0.55: continue          # it went on talking: try again
            yield a, sr

ENG = {}
def engine(name):
    if name not in ENG: ENG[name] = {'kokoro': KokoroEN, 'vieneu': VieNeuVI}[name]()
    return ENG[name]

# ---------------------------------------------------------------- lines
def sig(lang, who):
    c = CFG[lang][who]; return f"{c['engine']}|{c['voice']}|{c.get('speed', 1)}|gap{CFG['gap']}|v{CFG['version']}"
def lines_path(): return os.path.join(HERE, 'lines.json')
def cmd_lines(a):
    """what to record: the parts of voice/pending-unit1.json, plus every line the app said in a test run (--log)"""
    pend = json.load(open(os.path.join(VOICE, 'pending-unit1.json'), encoding='utf-8'))
    parts = a.parts.split(','); out = collections.OrderedDict()
    def add(lang, text, slow, who, part):
        k = vkey(text, slow); h = vhash(k); o = out.setdefault((lang, h), {'lang': lang, 'key': k, 'who': who, 'part': part})
        if who == 'chồi': o['who'] = 'chồi'           # said by Chồi anywhere: Chồi's voice
    for x in pend:
        if x['part'] not in parts: continue
        add('en', x['en'], x.get('slow'), 'chồi', x['part']); add('vi', x['vi'], x.get('slow'), 'chồi', x['part'])
    for f in (a.log or []):
        for li, en, vi, rate, *rest in json.load(open(f, encoding='utf-8')):
            if a.name:   # the test child's name -> {N}, as the app does
                nm = re.compile(r'(^|[^\w])' + re.escape(a.name) + r'(?!\w)'); en = nm.sub(r'\1{N}', en); vi = nm.sub(r'\1{N}', vi)
            who = 'kid' if rest and rest[0] == 'k' else 'chồi'; slow = bool(rate) and rate < .65; part = f'man{li}'
            if en: add('en', en, slow, who, part)
            if vi: add('vi', vi, slow, who, part)
    L = [o for o in out.values() if spoken(o['key'], o['lang'])]
    json.dump(L, open(lines_path(), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('lines', collections.Counter((o['lang'], o['part']) for o in L))

# ---------------------------------------------------------------- make (synthesize what is missing)
def manifest(lang):
    p = os.path.join(HERE, f'manifest-{lang}.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'first': None, 'c': {}}
def cache_path(lang, h, s): return os.path.join(CACHE, lang, hashlib.sha1((s + h).encode()).hexdigest()[:16] + '.wav')
def make_line(o):
    lang, c = o['lang'], CFG[o['lang']][o['who']]; e = engine(c['engine']); text = spoken(o['key'], lang)
    speed = c.get('speed', 1) * (0.85 if o['key'].startswith('~') else 1)
    parts, info = [], []
    for s in sentences(text):
        best = None
        for a, sr in e.candidates(s, c['voice'], speed):
            if lang == 'vi' and re.search(r'"[A-Za-z][^"]*"', s):   # English words inside a Vietnamese line: the recognizer can't judge it
                best = (1.0, to_sr(a, sr), '(có tiếng Anh, không kiểm)'); break
            heard = transcribe(a, sr, lang); sc = score(s, heard)
            if lang == 'vi' and sc < 0.999:   # Vietnamese: two recognizers, the one that hears it right counts
                h2 = transcribe(a, sr, lang, 'w'); s2 = score(s, h2)
                if s2 > sc: sc, heard = s2, 'W: ' + h2
            if best is None or sc > best[0]: best = (sc, to_sr(a, sr), heard)
            if sc >= 0.999: break
        if best is None: raise RuntimeError('no audio for ' + s)
        info.append([round(best[0], 2), s, best[2]]); parts += [best[1], np.zeros(int(CFG['gap'] * SR_OUT), np.float32)]
    return loud(np.concatenate(parts[:-1])), info
def cmd_make(a):
    L = json.load(open(lines_path(), encoding='utf-8'))
    for lang in a.lang.split(','):
        M = manifest(lang); todo = []
        for o in L:
            if o['lang'] != lang: continue
            h = vhash(o['key']); s = sig(lang, o['who'])
            if M['c'].get(h, {}).get('s') == s and M['c'][h].get('k') == o['key']: continue   # already in the bundles
            if os.path.exists(cache_path(lang, h, s)): continue
            todo.append(o)
        print(lang, 'to make', len(todo), flush=True); t0 = time.time(); low = []
        for i, o in enumerate(todo):
            h = vhash(o['key']); s = sig(lang, o['who']); p = cache_path(lang, h, s); os.makedirs(os.path.dirname(p), exist_ok=True)
            au, info = make_line(o); sf.write(p, au, SR_OUT)
            json.dump({'key': o['key'], 'who': o['who'], 'info': info}, open(p[:-4] + '.json', 'w', encoding='utf-8'), ensure_ascii=False)
            if min(x[0] for x in info) < 0.8: low.append((o['key'], info))
            if (i + 1) % 10 == 0: print(lang, i + 1, '/', len(todo), round(time.time() - t0), 's', flush=True)
        print(lang, 'made', len(todo), 'in', round(time.time() - t0), 's; heard less well:', len(low))
        for k, info in low[:40]: print('  ?', k, '|', ' / '.join(x[2] for x in info))

# ---------------------------------------------------------------- pack (write the files the app reads)
def mp3(path):
    return subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(SR_OUT), '-c:a', 'libmp3lame', '-b:a', '48k', '-f', 'mp3', '-'], capture_output=True, check=True).stdout
def cmd_pack(a):
    L = json.load(open(lines_path(), encoding='utf-8'))
    for lang in a.lang.split(','):
        ip = os.path.join(VOICE, f'{lang}.json'); I = json.load(open(ip)); M = manifest(lang)
        first = M['first'] if M['first'] is not None else I['n']           # bundles before this one are the older voice, never touched
        oldb = {}
        def bundle(b):
            if b not in oldb: oldb[b] = open(os.path.join(VOICE, f'{lang}-{b:02d}.mp3'), 'rb').read()
            return oldb[b]
        clips = collections.OrderedDict(); newM = {}
        order = {p: i for i, p in enumerate(['chung'] + [f'man{i}' for i in range(8)])}
        for o in sorted((o for o in L if o['lang'] == lang), key=lambda o: order.get(o['part'], 99)):
            h = vhash(o['key']); s = sig(lang, o['who']); p = cache_path(lang, h, s)
            if os.path.exists(p): data = mp3(p)
            elif M['c'].get(h, {}).get('s') == s and M['c'][h].get('k') == o['key'] and h in I['c'] and I['c'][h][0] >= first:
                b, off, ln = I['c'][h]; data = bundle(b)[off:off + ln]
            else: print('  missing (run make):', lang, o['key']); continue
            old = M['c'].get(h, {}).get('old') or (I['c'][h] if h in I['c'] and I['c'][h][0] < first else None)
            clips[h] = data; newM[h] = {'k': o['key'], 's': s, 'part': o['part'], 'who': o['who'], **({'old': old} if old else {})}
        # lines that were in the new voice but are no longer wanted go back to their older recording (or away)
        for h, m in M['c'].items():
            if h not in newM:
                if m.get('old'): I['c'][h] = m['old']
                else: I['c'].pop(h, None)
        for b in range(first, I['n']):
            f = os.path.join(VOICE, f'{lang}-{b:02d}.mp3')
            if os.path.exists(f): oldb.setdefault(b, open(f, 'rb').read())
        bufs, buf = [], b''
        for h, data in clips.items():
            if buf and len(buf) + len(data) > MAXB: bufs.append(buf); buf = b''
            I['c'][h] = [first + len(bufs), len(buf), len(data)]; buf += data
        if buf: bufs.append(buf)
        parts = collections.defaultdict(set)
        for h, m in newM.items(): parts[m['part']].add(I['c'][h][0])
        I['p'] = {k: sorted(v) for k, v in parts.items()}   # part -> its mp3 files (to fetch a level's voice first)
        for b in range(first, max(I['n'], first + len(bufs))):
            f = os.path.join(VOICE, f'{lang}-{b:02d}.mp3')
            if os.path.exists(f): os.remove(f)
        for i, data in enumerate(bufs): open(os.path.join(VOICE, f'{lang}-{first + i:02d}.mp3'), 'wb').write(data)
        I['n'] = first + len(bufs)
        json.dump(I, open(ip, 'w'), separators=(',', ':'))
        json.dump({'first': first, 'c': newM}, open(os.path.join(HERE, f'manifest-{lang}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        print(lang, 'new-voice lines', len(clips), 'bundles', f'{first}..{I["n"] - 1}', 'MB', round(sum(map(len, bufs)) / 1e6, 1))

# ---------------------------------------------------------------- listening page
def cmd_page(a):
    rows = {}
    for lang in ('en', 'vi'):
        M = manifest(lang)
        for h, m in M['c'].items(): rows.setdefault(m['part'], []).append([lang, h, m['k'], m['who']])
    tpl = open(os.path.join(HERE, 'nghe-thu.tpl.html'), encoding='utf-8').read()
    open(os.path.join(VOICE, 'nghe-thu.html'), 'w', encoding='utf-8').write(tpl.replace('/*ROWS*/null', json.dumps(rows, ensure_ascii=False)))
    print('voice/nghe-thu.html', {k: len(v) for k, v in rows.items()})

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd', required=True)
    p = sp.add_parser('lines'); p.add_argument('--parts', default='chung,man0,man1'); p.add_argument('--log', nargs='*'); p.add_argument('--name', default='Bin', help='the child name used in the test run')
    p = sp.add_parser('make'); p.add_argument('--lang', default='en,vi')
    p = sp.add_parser('pack'); p.add_argument('--lang', default='en,vi')
    sp.add_parser('page')
    a = ap.parse_args(); {'lines': cmd_lines, 'make': cmd_make, 'pack': cmd_pack, 'page': cmd_page}[a.cmd](a)
