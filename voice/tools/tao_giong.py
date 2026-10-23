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
KEYPFX = re.compile(r'^@(?:[A-Za-z]+:)?')   # "@câu" (bạn nhỏ chung, cũ) hoặc "@Lam:câu" (đúng bạn đó)
SYL_KEEP = {'bye-bye', 'ding-dong', 'kee-ow', 'đô-mi-nô', 'roly-poly', 'heave-ho'}   # real words with hyphens, read as one word
def syllables(m):
    """a clapping drill (ba-na-na, ap - pull): each sound said on its own, with a small pause between"""
    w = m.group(0)
    if re.sub(r'\s+', '', w).lower() in SYL_KEEP: return w
    if re.sub(r'\s+', '', w).lower() == 'is-land': return 'Eye, land' if w[0].isupper() else 'eye, land'   # said "eye-land", not "is"
    return ', '.join(x.strip() for x in w.split('-'))
def spoken(key, lang):
    """the app swaps the child's name for {N}; the recording leaves the name out (it can't know it)"""
    t = KEYPFX.sub('', key).lstrip('~')
    t = re.sub(r'[\wÀ-ỹ]+(?:\s*-\s*[\wÀ-ỹ]+)+', syllables, t)
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
    if t.lower() == 'ap': t = 'App'   # the first sound of apple on its own: "Ap" comes out 0.2 s, almost nothing (Minh, 22/10)
    t = re.sub(r'\s+', ' ', t).strip()
    if t and t[0].islower(): t = t[0].upper() + t[1:]
    return t
# English words in a Vietnamese-mode line (Minh, 22/10: phương án B): read by Chồi's English voice (af_heart), the rest by VieNeu
EN_WORDS = {'cat', 'fish', 'star', 'buh', 'loon', 'pre', 'zent', 'ap', 'pull', 'egg', 'tus', 'but', 'ter', 'fly', 'land', 'nut', 'banana',
            'apple', 'mango', 'lotus', 'butterfly', 'island', 'coconut'}
EN_ALONE = {'ba', 'na', 'co', 'lo', 'go', 'man', 'is'}     # also Vietnamese-looking: English only as a slow syllable on its own ("~ba")
VI_SYL = {'hoa', 'sen', 'con'}                             # Vietnamese clapping syllables written without marks
SPAN = re.compile(r'"([^"]*[A-Za-z][^"]*)"|\b([A-Za-z]+(?:\s*-\s*[A-Za-z]+)+)\b|\b([A-Za-z]+)\b')
# the English words of a Vietnamese line, as chat U1 writes them in pending-unit1.json ("tiengAnhTrongCauViet"), kept by key
HINTS_PATH = os.path.join(HERE, 'tieng-anh-trong-cau-viet.json')
HINTS = json.load(open(HINTS_PATH, encoding='utf-8')) if os.path.exists(HINTS_PATH) else {}
def vi_spans(raw, phrases=None):
    """[(lang, text)] for one sentence of a Vietnamese line; with phrases (chat U1's list) only those are English"""
    out, i = [], 0
    rx = re.compile('|'.join(r'(?<![\wÀ-ỹ])' + re.escape(x) + r'(?![\wÀ-ỹ])' for x in sorted(phrases, key=len, reverse=True)), re.I) if phrases else SPAN
    for m in rx.finditer(raw):
        q, drill, w = m.groups() if not phrases else (None, None, None)
        en = bool(phrases) or (q is not None and not re.search(r'[À-ỹđĐ]', q)) or \
             (drill is not None and not all(x.strip().lower() in VI_SYL for x in drill.split('-'))) or \
             (w is not None and w.lower() in EN_WORDS)
        if not en: continue
        if raw[i:m.start()].strip(' :,'): out.append(('vi', raw[i:m.start()].strip()))
        tail = re.match(r'[!?.…]*', raw[m.end():]).group(0)
        out.append(('en', (q if q is not None else m.group(0)) + tail)); i = m.end() + len(tail)
    if raw[i:].strip(' .,:'): out.append(('vi', raw[i:].strip()))
    return out or [('vi', raw)]
def mixed(key, lang, who):
    """a Vietnamese line of Chồi's with English words in it"""
    if lang != 'vi' or who != 'chồi': return False
    t = KEYPFX.sub('', key)
    if t.startswith('~') and t[1:].lower() in EN_ALONE: return True
    return any(l == 'en' for s in sentences(t.lstrip('~')) for l, _ in vi_spans(s, HINTS.get(key)))
def sentences(t):
    return [s for s in re.split(r'(?<=[.!?])\s+', t.strip()) if s] or [t]

# ---------------------------------------------------------------- checking by ear (a recognizer)
NUM = {'0':'zero','1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine','10':'ten'}
UK = {'he': 'hee', 'sweet': 'sweets', 'bên': 'ben', 'bèn': 'ben', 'poly': 'polly', 'pô': 'polly', 'lamb': 'lam', 'nah': 'na', 'whoa': 'whoosh', 'nhá': 'nhé', 'kĩ': 'kỹ', 'colour': 'color', 'colours': 'colors', 'favourite': 'favorite', 'mum': 'mom', 'grey': 'gray', 'okay': 'ok', 'ireland': 'island'}
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
ONO = {'vù', 'vèo', 'brừm', 'grừ', 'bụp', 'bùm', 'tõm', 'whoosh', 'grrr', 'brrm', 'vroom', 'pop', 'boing', 'ồ', 'oa', 'hì', 'hihi', 'ha', 'wheee', 'vèo'}   # sounds: a recognizer can't judge them
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

def shift_voice(a, sr, formant=1.0, pitch=1.0):
    """a child's voice from an adult one: smaller vocal tract (formant scale) and higher pitch, set apart
    (two rubberband passes: the first moves pitch and formants together, the second moves pitch only)"""
    import tempfile
    f = []
    if formant != 1.0: f.append(f'rubberband=pitch={formant}:formant=shifted:pitchq=quality')
    if abs(pitch / formant - 1) > 1e-6: f.append(f'rubberband=pitch={pitch / formant}:formant=preserved:pitchq=quality')
    if not f: return a
    with tempfile.TemporaryDirectory() as d:
        sf.write(d + '/i.wav', a, sr); subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', d + '/i.wav', '-af', ','.join(f), d + '/o.wav'], check=True)
        b, _ = sf.read(d + '/o.wav', dtype='float32')
    return b
class KokoroKid:
    """a child's English voice: Kokoro at normal speed (no carrier word, so no "uh"), then made a child's voice"""
    def __init__(self): self.K = engine('kokoro').K
    def candidates(self, s, c, speed):
        for sp in (speed, speed * 0.95, speed * 1.05, speed * 0.9):
            a, sr = self.K.create(s, voice=c['voice'], speed=sp, lang=c.get('lang', 'en-us'))
            yield trim(shift_voice(trim(a, sr, th=0.012), sr, c.get('formant', 1), c.get('pitch', 1)), sr, th=0.012), sr
class VieNeuClone:
    """a child's Vietnamese voice: VieNeu reads in the voice of a short reference clip (kid-ref/)"""
    def __init__(self): self.V = engine('vieneu').V
    def candidates(self, s, c, speed, tries=6):
        n = len(re.findall(r'\w+', s)); ref = os.path.join(HERE, c['voice'])
        for _ in range(tries):
            a = trim(np.asarray(self.V.infer(s, ref_audio=ref, denoise=False), dtype=np.float32), 48000, th=0.012)
            if len(a) / 48000 > 1.0 + n * 0.5: continue
            yield a, 48000
ENG = {}
def engine(name):
    if name not in ENG: ENG[name] = {'kokoro': KokoroEN, 'vieneu': VieNeuVI, 'kokoro_kid': KokoroKid, 'vieneu_clone': VieNeuClone}[name]()
    return ENG[name]

# ---------------------------------------------------------------- lines
def sig(lang, who, key=None):
    c = CFG[lang][who]; extra = ''.join(f"|{k}{c[k]}" for k in ('formant', 'pitch', 'gap') if k in c)
    if key is not None and mixed(key, lang, who): extra += f"|en:{CFG['en']['chồi']['voice']}"   # its English words in Chồi's English voice
    return f"{c['engine']}|{c['voice']}|{c.get('speed', 1)}|gap{CFG['gap']}|v{CFG['version']}" + extra
def lines_path(): return os.path.join(HERE, 'lines.json')
def cmd_lines(a):
    """what to record: every line already in the new voice (kept), the parts of voice/pending-unit1.json,
    and every line the app said in a test run (--log)"""
    pend = json.load(open(os.path.join(VOICE, 'pending-unit1.json'), encoding='utf-8'))
    parts = a.parts.split(',') if a.parts else None; out = collections.OrderedDict()
    def add(lang, text, slow, who, part, key=None):
        # a kid's line (Lam, Na, Ben) is keyed "@" + the line, in the kid's own voice; the app falls back to Chồi's recording
        k = key or (('@' if who == 'kid' else '') + vkey(text, slow)); h = vhash(k)
        out.setdefault((lang, h), {'lang': lang, 'key': k, 'who': who, 'part': part})
    for lang in ('en', 'vi'):                         # lines made before stay (the pending list drops them once they have the new voice)
        for h, m in manifest(lang)['c'].items(): add(lang, None, None, m['who'], m['part'], key=m['k'])
    for x in pend:
        if parts and x['part'] not in parts: continue
        who = x.get('who') or 'chồi'   # a friend's line (Lam, Na, Ben): in that friend's own voice, keyed "@Lam:" + the line
        for lang in ('en', 'vi'):
            add(lang, None, None, who, x['part'], key=(f'@{who}:' if who != 'chồi' else '') + vkey(x[lang], x.get('slow')))
        if x.get('tiengAnhTrongCauViet'): HINTS[vkey(x['vi'], x.get('slow'))] = x['tiengAnhTrongCauViet']
    json.dump(HINTS, open(HINTS_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    kp = os.path.join(HERE, 'cau-ban-nho.json')   # each child's own voice: "@Lam:" + the line (ban_nho.py)
    if os.path.exists(kp):
        for x in json.load(open(kp, encoding='utf-8')):
            for lang in ('en', 'vi'):
                add(lang, None, None, x['who'], 'chung', key=f"@{x['who']}:" + vkey(x[lang]))
    for f in (a.log or []):
        for li, en, vi, rate, *rest in json.load(open(f, encoding='utf-8')):
            if a.name:   # the test child's name -> {N}, as the app does
                nm = re.compile(r'(^|[^\w])' + re.escape(a.name) + r'(?!\w)'); en = nm.sub(r'\1{N}', en); vi = nm.sub(r'\1{N}', vi)
            who = 'kid' if rest and rest[0] == 'k' else 'chồi'; slow = bool(rate) and rate < .65; part = li if isinstance(li, str) else f'man{li}'
            if en: add('en', en, slow, who, part)
            if vi: add('vi', vi, slow, who, part)
            if who == 'kid':                          # and Chồi's version too, for an app that has no kid voice yet
                if en: add('en', en, slow, 'chồi', part)
                if vi: add('vi', vi, slow, 'chồi', part)
    VI = re.compile(r'[ăâđêôơưàáảãạèéẻẽẹìíỉĩịòóỏõọùúủũụỳýỷỹỵằắẳẵặầấẩẫậềếểễệồốổỗộờớởỡợừứửữự]', re.I)
    # an English line with Vietnamese words in it (other than Chồi) is only the subtitle of a Vietnamese-mode line: never spoken
    L = [o for o in out.values() if spoken(o['key'], o['lang']) and not (o['lang'] == 'en' and VI.search(o['key'].replace('Chồi', '')))]
    json.dump(L, open(lines_path(), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('lines', sorted(collections.Counter((o['lang'], o['part']) for o in L).items()))

# ---------------------------------------------------------------- make (synthesize what is missing)
def manifest(lang):
    p = os.path.join(HERE, f'manifest-{lang}.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'c': {}}
def cache_path(lang, h, s): return os.path.join(CACHE, lang, hashlib.sha1((s + h).encode()).hexdigest()[:16] + '.wav')
def pick_best(e, c, s, lang, speed, whole):
    best = None
    for a, sr in (e.candidates(s, c, speed) if whole else e.candidates(s, c['voice'], speed)):
        heard = transcribe(a, sr, lang); sc = score(s, heard)
        if lang == 'vi' and sc < 0.999:
            h2 = transcribe(a, sr, lang, 'w'); s2 = score(s, h2)
            if s2 > sc: sc, heard = s2, 'W: ' + h2
        if best is None or sc > best[0]: best = (sc, to_sr(a, sr), heard)
        if sc >= 0.999: break
    return best
def make_line(o):
    lang, c = o['lang'], CFG[o['lang']][o['who']]; e = engine(c['engine']); text = spoken(o['key'], lang)
    speed = c.get('speed', 1) * (0.85 if KEYPFX.sub('', o['key']).startswith('~') else 1)
    whole = c['engine'] in ('kokoro_kid', 'vieneu_clone')   # these take the whole config
    parts, info = [], []
    if mixed(o['key'], lang, o['who']): return make_mixed(o, speed)
    groups = sentences(text)
    if whole and len(groups) > 1:   # a child says the line in one breath when it comes out clear; else sentence by sentence
        b = pick_best(e, c, text, lang, speed, whole)
        if b and b[0] >= 0.8: return loud(b[1]), [[round(b[0], 2), text, b[2]]]
    for s in groups:
        best = None
        for a, sr in (e.candidates(s, c, speed) if whole else e.candidates(s, c['voice'], speed)):
            if lang == 'vi' and re.search(r'"[A-Za-z][^"]*"', s):   # English words inside a Vietnamese line: the recognizer can't judge it
                best = (1.0, to_sr(a, sr), '(có tiếng Anh, không kiểm)'); break
            heard = transcribe(a, sr, lang); sc = score(s, heard)
            if lang == 'vi' and sc < 0.999:   # Vietnamese: two recognizers, the one that hears it right counts
                h2 = transcribe(a, sr, lang, 'w'); s2 = score(s, h2)
                if s2 > sc: sc, heard = s2, 'W: ' + h2
            if best is None or sc > best[0]: best = (sc, to_sr(a, sr), heard)
            if sc >= 0.999: break
        if best is None: raise RuntimeError('no audio for ' + s)
        info.append([round(best[0], 2), s, best[2]]); parts += [best[1], np.zeros(int(c.get('gap', CFG['gap']) * SR_OUT), np.float32)]
    return loud(np.concatenate(parts[:-1])), info
def make_mixed(o, slow_speed):
    """Vietnamese sentence parts by VieNeu, English words by Kokoro af_heart (Chồi's English voice), 0.15 s apart inside a sentence"""
    t = KEYPFX.sub('', o['key']); slow = t.startswith('~'); t = t.lstrip('~')
    ce, cv = CFG['en']['chồi'], CFG['vi']['chồi']; sp_en = ce.get('speed', 1) * (0.85 if slow else 1)
    if t.lower() in EN_ALONE: sents = [[('en', t)]]
    else: sents = [vi_spans(x, HINTS.get(o['key'])) for x in sentences(t)]
    parts, info = [], []
    for k, segs in enumerate(sents):
        for j, (l, x) in enumerate(segs):
            txt = spoken(x, l)
            if j and l == 'vi' and txt[:1].isupper() and not x[:1].isupper(): txt = txt[0].lower() + txt[1:]
            e, c, sp = (engine('kokoro'), ce, sp_en) if l == 'en' else (engine('vieneu'), cv, cv.get('speed', 1))
            b = pick_best(e, c, txt, l, sp, False)
            if b is None: raise RuntimeError('no audio for ' + txt)
            info.append([round(b[0], 2), f'{l}: {txt}', b[2]]); parts += [loud(b[1]), np.zeros(int(0.15 * SR_OUT), np.float32)]
        parts[-1] = np.zeros(int(CFG['gap'] * SR_OUT), np.float32)
    return loud(np.concatenate(parts[:-1])), info
def cmd_make(a):
    L = json.load(open(lines_path(), encoding='utf-8'))
    redo = re.compile(a.redo) if a.redo else None
    for lang in a.lang.split(','):
        M = manifest(lang); todo = []
        for o in L:
            if o['lang'] != lang: continue
            h = vhash(o['key']); s = sig(lang, o['who'], o['key'])
            if redo and redo.search(o['key']): todo.append(o); continue   # made again on purpose (the way of reading it changed)
            if M['c'].get(h, {}).get('s') == s and M['c'][h].get('k') == o['key']: continue   # already in the bundles
            if os.path.exists(cache_path(lang, h, s)): continue
            todo.append(o)
        todo.sort(key=lambda o: ORDER.get(o['part'], 99))   # common lines and the first levels first
        print(lang, 'to make', len(todo), flush=True); t0 = time.time(); low = []
        for i, o in enumerate(todo):
            h = vhash(o['key']); s = sig(lang, o['who'], o['key']); p = cache_path(lang, h, s); os.makedirs(os.path.dirname(p), exist_ok=True)
            au, info = make_line(o); sf.write(p, au, SR_OUT)
            json.dump({'key': o['key'], 'who': o['who'], 'info': info}, open(p[:-4] + '.json', 'w', encoding='utf-8'), ensure_ascii=False)
            if min(x[0] for x in info) < 0.8: low.append((o['key'], info))
            if (i + 1) % 10 == 0: print(lang, i + 1, '/', len(todo), round(time.time() - t0), 's', flush=True)
        print(lang, 'made', len(todo), 'in', round(time.time() - t0), 's; heard less well:', len(low))
        for k, info in low[:40]: print('  ?', k, '|', ' / '.join(x[2] for x in info))

# ---------------------------------------------------------------- pack (write the files the app reads)
def kbps(lang):
    k = CFG.get('mp3_kbps', 48); return int(k.get(lang, 48) if isinstance(k, dict) else k)
def mp3(path, lang):
    return subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(SR_OUT), '-c:a', 'libmp3lame', '-b:a', f'{kbps(lang)}k', '-f', 'mp3', '-'], capture_output=True, check=True).stdout
ORDER = {p: i for i, p in enumerate(['chung'] + [f'man{i}' for i in range(8)])}

# ---------------------------------------------------------------- pack (the files the app reads)
# Gói theo nhóm (khoá p trong en.json / vi.json), mỗi nhóm là các file mp3 liền nhau, theo thứ tự câu được nói:
#   chung   câu dùng ở từ 2 màn trở lên (khen, nhắc, Polly và các bạn nhỏ nói ở nhiều màn), câu bạn nhỏ khi bé chạm vào bạn ấy
#   man0 … man7   câu chỉ màn đó dùng (kể cả câu Polly, câu bạn nhỏ chỉ có ở màn đó), theo thứ tự nói (file đầu = đầu màn)
#   sothu   phần cuối mỗi màn: thành phố, sở thú, cho thú ăn (Chồi và các bạn nhỏ)
#   ngoai   câu các lần máy tự chơi 8 màn không gặp: câu ít gặp (giảng lại khi bé sai nhiều…), Fun Mix, My Games, hộp nhạc…
#   cu      giọng cũ chưa được thay, và giọng bạn nhỏ chung cũ (@câu): không tải trước, chỉ tải khi cần
LEVELS = [f'man{i}' for i in range(8)]
GROUPS = ['chung'] + LEVELS + ['sothu', 'ngoai', 'cu']
MAXB = 400_000           # bytes per file: a level's first file holds its first minutes
MAXB_CU = 1_000_000
TAIL = 'This is your city!'   # a level's last part (the city and the zoo) starts with this line
def usage(lang):
    """from thu-thu-tu.json (thu_thu_tu.py): {hash: {level: earliest place in a run, 0..1}} for the lines said before the
    city/zoo part at the end of a level, {hash: earliest place} for the lines said only there, and the hashes Polly said"""
    U, T, polly = collections.defaultdict(dict), {}, set()
    p = os.path.join(HERE, 'thu-thu-tu.json')
    if not os.path.exists(p): return U, T, polly
    nm = re.compile(r'(^|[^\w])Bin(?!\w)')
    for run in json.load(open(p, encoding='utf-8')):
        seq = run['seq']; n = max(len(seq), 1); lv = f"man{run['li']}"
        tail = next((i for i, x in enumerate(seq) if x[0].startswith(TAIL)), n)
        for i, (en, vi, rate, flag) in enumerate(seq):
            t = en if lang == 'en' else vi
            if not t: continue
            k = vkey(nm.sub(r'\1{N}', t), bool(rate) and rate < .65)
            if flag.startswith('k:'): k = f'@{flag[2:]}:' + k
            h = vhash(k)
            if i < tail: U[h][lv] = min(U[h].get(lv, 9), i / n)
            else: T[h] = min(T.get(h, 9), (i - tail) / max(n - tail, 1))
            if flag == 'p': polly.add(h)
    return U, T, polly
def layout(lang, M):
    """group -> its lines (hashes), in the order they are said"""
    U, T, polly = usage(lang)
    zoo = {vkey(x[1] if lang == 'en' else x[2]) for x in json.load(open(os.path.join(HERE, 'so-thu.json'), encoding='utf-8'))}
    kp = os.path.join(HERE, 'cau-ban-nho.json')
    if os.path.exists(kp): zoo |= {vkey(x[lang]) for x in json.load(open(kp, encoding='utf-8')) if x.get('zoo')}
    OLD = collections.defaultdict(set); nm = re.compile(r'(^|[^\w])Bin(?!\w)')
    for li, en, vi, rate, *_ in json.load(open(os.path.join(HERE, 'thu-cau.json'), encoding='utf-8')):
        t = en if lang == 'en' else vi
        if t: OLD[vhash(vkey(nm.sub(r'\1{N}', t), bool(rate) and rate < .65))].add(f'man{li}')
    G = {g: [] for g in GROUPS}; seen = {}
    for idx, (h, m) in enumerate(M.items()):
        k = m['k']; kid = bool(re.match(r'^@[A-Za-z]+:', k)); text = KEYPFX.sub('', k)
        if k.startswith('@') and not kid: g = 'cu'                     # the old shared kid voice: never asked for now
        elif not U.get(h) and (h in T or text in zoo): g = 'sothu'; seen[h] = (0, T.get(h, 9))
        elif U.get(h):
            lv = U[h]
            g = 'chung' if len(lv) > 1 else next(iter(lv))           # one level only (Polly's and the friends' lines too): with that level
            seen[h] = min((LEVELS.index(l), x) for l, x in lv.items()) if g == 'chung' else (0, lv[g])
        elif kid: g = 'chung'
        elif h in OLD: g = next(iter(OLD[h])) if len(OLD[h]) == 1 else 'chung'   # met only in the older test runs (thu-cau.json)
        elif m.get('part') in LEVELS: g = m['part']                   # not met in the test runs: after the lines that were
        else: g = 'ngoai'
        G[g].append((seen.get(h, (99, 9)), idx, h))
    return {g: [h for _, _, h in sorted(v)] for g, v in G.items()}, U, T
def wav_for(lang, h, s):
    p = cache_path(lang, h, s); q = os.path.join(os.path.dirname(p), 'packed', os.path.basename(p))
    return p if os.path.exists(p) else (q if os.path.exists(q) else None)
def cmd_pack(a):
    """Write the files the app reads. By default only new or changed lines are added, in new mp3 files at the end
    (the files already on GitHub stay as they are), each new file holding one group. --compact rewrites every file,
    group by group in the order the lines are said, and re-encodes every new-voice line at mp3_kbps (config.json, per language)."""
    L = json.load(open(lines_path(), encoding='utf-8'))
    for lang in a.lang.split(','):
        ip = os.path.join(VOICE, f'{lang}.json'); I = json.load(open(ip)); M = manifest(lang); cache = {}
        def clip(h):
            b, off, ln = I['c'][h]
            if b not in cache: cache[b] = open(os.path.join(VOICE, f'{lang}-{b:02d}.mp3'), 'rb').read()
            return cache[b][off:off + ln]
        newM, fresh, missing, done = collections.OrderedDict(), {}, 0, []
        for o in sorted((o for o in L if o['lang'] == lang), key=lambda o: ORDER.get(o['part'], 99)):
            h = vhash(o['key']); s = sig(lang, o['who'], o['key']); p = cache_path(lang, h, s)
            ok = M['c'].get(h, {}).get('s') == s and M['c'][h].get('k') == o['key'] and h in I['c']
            if os.path.exists(p): fresh[h] = p; done.append(p)                # made since the last pack (new, changed, or redone)
            elif not ok: missing += 1; print('  missing (run make):', lang, o['key']); continue
            newM[h] = {'k': o['key'], 's': s, 'part': o['part'], 'who': o['who']}
        G, U, T = layout(lang, newM)
        old = [h for h in I['c'] if h not in newM]                          # older voice, still not remade
        if a.compact:
            def data(h):
                w = fresh.get(h) or wav_for(lang, h, newM[h]['s'])
                if not w: print('  no wav, kept the packed clip:', lang, newM[h]['k'])
                return mp3(w, lang) if w else clip(h)
            plan = [(g, [(h, data(h)) for h in G[g]]) for g in GROUPS if g != 'cu']
            plan.append(('cu', [(h, data(h)) for h in G['cu']] + [(h, clip(h)) for h in old]))
            start = 0; I['c'] = {}; I['p'] = {}
        else:
            plan = [(g, [(h, mp3(fresh[h], lang)) for h in G[g] if h in fresh]) for g in GROUPS]
            start = I['n']; I.setdefault('p', {})
        bufs, pos = [], {}
        for g, items in plan:
            if not items: continue
            buf, cap = b'', (MAXB_CU if g == 'cu' else MAXB); files = []
            for h, d in items:
                if buf and len(buf) + len(d) > cap: bufs.append(buf); files.append(start + len(bufs) - 1); buf = b''
                pos[h] = [start + len(bufs), len(buf), len(d)]; buf += d
            bufs.append(buf); files.append(start + len(bufs) - 1)
            I['p'][g] = I['p'].get(g, []) + files
        if a.compact:
            for f in os.listdir(VOICE):
                if re.fullmatch(rf'{lang}-\d+\.mp3', f): os.remove(os.path.join(VOICE, f))
        I['c'].update(pos)
        for i, d in enumerate(bufs): open(os.path.join(VOICE, f'{lang}-{start + i:02d}.mp3'), 'wb').write(d)
        I['n'] = start + len(bufs)
        I['p'] = {g: I['p'][g] for g in GROUPS if I['p'].get(g)}
        if not a.compact:   # a group's files in the order their lines are said (its first file stays first: the start of the level)
            for g, fs in I['p'].items():
                rank = {}
                for i, h in enumerate(G[g]):
                    f = I['c'][h][0] if h in I['c'] else None
                    if f in fs: rank[f] = min(rank.get(f, i), i)
                I['p'][g] = fs[:1] + sorted(fs[1:], key=lambda f: rank.get(f, 1e9))
        for g in GROUPS:
            for h in G[g]: newM[h]['g'] = g
        # h: a short fingerprint of each file's bytes (the app asks for voice/en-07.mp3?v=<h>, so a file changed on GitHub is fetched again)
        I['h'] = [hashlib.sha1(open(os.path.join(VOICE, f'{lang}-{b:02d}.mp3'), 'rb').read()).hexdigest()[:8] for b in range(I['n'])]
        json.dump({'n': I['n'], 'c': I['c'], 'p': I['p'], 'h': I['h']}, open(ip, 'w'), separators=(',', ':'))
        json.dump({'c': newM}, open(os.path.join(HERE, f'manifest-{lang}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        for p in done:   # packed: keep a copy aside, so the next pack doesn't add it again
            d = os.path.join(os.path.dirname(p), 'packed'); os.makedirs(d, exist_ok=True)
            for ext in ('.wav', '.json'):
                if os.path.exists(p[:-4] + ext): os.replace(p[:-4] + ext, os.path.join(d, os.path.basename(p)[:-4] + ext))
        size = lambda fs: sum(os.path.getsize(os.path.join(VOICE, f'{lang}-{b:02d}.mp3')) for b in fs)
        print(lang, f'{kbps(lang)}k' if a.compact else '', 'new-voice lines', len(newM), '(new now', len(fresh), ') files', I['n'], 'written', len(bufs),
              'all MB', round(size(range(I['n'])) / 1e6, 1), 'missing', missing)
        for g, fs in I['p'].items(): print(f'   {g:6s} files {fs[0]:>2}–{fs[-1]:<2} ({len(fs):>2})  {size(fs) / 1e6:5.2f} MB  first file {size(fs[:1]) / 1e3:4.0f} KB')
        heard = set(U) | set(T); heard_old = [h for h in heard if h not in newM and h in I['c']]; none = [h for h in heard if h not in I['c']]
        print('   test runs: lines still in the old voice', len(heard_old), '· lines with no recording', len(none))

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
    p = sp.add_parser('lines'); p.add_argument('--parts', default='', help='e.g. chung,man0 (empty = all)'); p.add_argument('--log', nargs='*'); p.add_argument('--name', default='Bin', help='the child name used in the test run')
    p = sp.add_parser('make'); p.add_argument('--lang', default='en,vi'); p.add_argument('--redo', default='', help='regex: make these lines again even if they exist')
    p = sp.add_parser('pack'); p.add_argument('--lang', default='en,vi'); p.add_argument('--compact', action='store_true')
    sp.add_parser('page')
    a = ap.parse_args(); {'lines': cmd_lines, 'make': cmd_make, 'pack': cmd_pack, 'page': cmd_page}[a.cmd](a)
