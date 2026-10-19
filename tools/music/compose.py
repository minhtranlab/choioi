#!/usr/bin/env python3
"""Our own recordings of famous classical pieces (the music itself is public domain; these arrangements and recordings are ours).
Notes are written by hand below, turned into MIDI with mido, played by FluidSynth with the FluidR3 GM sound set (MIT licence),
then cut and normalised with ffmpeg.

usage: python3 tools/music/compose.py OUTDIR
Writes, for each piece: OUTDIR/<id>.mid, OUTDIR/<id>-box.mp3 (the Music box: the best-known part, ~20–35 s)
and the short clips the levels use (see CLIPS)."""
import sys, os, subprocess, re
import mido

SF2 = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
NOTE = {'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def pitch(n):
    m = re.fullmatch(r'([A-G])([#b]?)(-?\d)', n)
    p = NOTE[m.group(1)] + (1 if m.group(2)=='#' else -1 if m.group(2)=='b' else 0)
    return 12*(int(m.group(3))+1) + p
def seq(text, dflt=1.0):
    """'E4 E4:.5 r:1 |' → list of ([pitch], beats). '|' is only a bar line for reading."""
    out = []
    for tok in text.replace('|', ' ').split():
        n, _, d = tok.partition(':'); d = float(d) if d else dflt
        out.append(([] if n == 'r' else [pitch(n)], d))
    return out
def chords(text, dflt=1.0):
    """chords written as C4+E4+G4:2 (plus-joined)"""
    out = []
    for tok in text.replace('|', ' ').split():
        n, _, d = tok.partition(':'); d = float(d) if d else dflt
        out.append(([] if n == 'r' else [pitch(x) for x in n.split('+')], d))
    return out

TPB = 480
def build(parts, tempo, name, tempo_map=None):
    """parts: list of dict(prog, notes=[(pitches, beats)], vel, ch, legato, vel_fn)
    tempo_map: optional list of (beat, bpm) changes."""
    mid = mido.MidiFile(ticks_per_beat=TPB)
    meta = mido.MidiTrack(); mid.tracks.append(meta)
    meta.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo), time=0))
    if tempo_map:
        last = 0
        for beat, bpm in tempo_map:
            t = int(beat*TPB); meta.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm), time=t-last)); last = t
    for i, P in enumerate(parts):
        tr = mido.MidiTrack(); mid.tracks.append(tr); ch = P.get('ch', i if i < 9 else i+1)
        tr.append(mido.Message('program_change', program=P['prog'], channel=ch, time=0))
        if 'cc7' in P: tr.append(mido.Message('control_change', control=7, value=P['cc7'], channel=ch, time=0))
        tr.append(mido.Message('control_change', control=91, value=P.get('rev', 70), channel=ch, time=0))
        ev = []; t = 0.0
        for k, (ps, d) in enumerate(P['notes']):
            v = P['vel'](t, k) if callable(P.get('vel')) else P.get('vel', 80)
            dur = d*P.get('legato', .92)
            for p in ps: ev.append((t, 1, p, v)); ev.append((t+dur, 0, p, 0))
            t += d
        ev.sort(key=lambda e: (e[0], e[1]))
        last = 0
        for (tt, on, p, v) in ev:
            tick = int(round(tt*TPB))
            tr.append(mido.Message('note_on' if on else 'note_off', note=p, velocity=int(max(1, min(127, v))) if on else 0, channel=ch, time=tick-last)); last = tick
    mid.save(name)

def render(mid, wav, gain=.7):
    subprocess.run(['fluidsynth', '-ni', '-g', str(gain), '-r', '44100', '-o', 'synth.reverb.active=1', '-o', 'synth.reverb.room-size=0.55',
                    '-o', 'synth.reverb.level=0.55', '-o', 'synth.chorus.active=0', '-F', wav, SF2, mid], check=True, capture_output=True)
def mp3(wav, out, start=0.0, dur=None, fade_in=0.05, fade_out=1.2):
    """cut, fade, and bring the loudest moment to -1.5 dB (keeps the quiet and loud parts: the Surprise needs its surprise)"""
    cut = ['-ss', str(start)] + (['-t', str(dur)] if dur else [])
    r = subprocess.run(['ffmpeg', '-hide_banner'] + cut + ['-i', wav, '-af', 'volumedetect', '-f', 'null', '-'], capture_output=True, text=True)
    peak = float(re.search(r'max_volume: (-?[\d.]+) dB', r.stderr).group(1))
    af = f'afade=t=in:st=0:d={fade_in}' + (f',afade=t=out:st={max(0,dur-fade_out)}:d={fade_out}' if dur else '') + f',volume={-1.5-peak:.2f}dB'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + cut + ['-i', wav, '-af', af, '-ac', '1', '-ar', '44100', '-b:a', '80k', out], check=True)
def length(wav):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav], capture_output=True, text=True); return float(r.stdout)

# ======================= the pieces =======================
P = {}

# --- Beethoven: Ode to Joy (Symphony No. 9, finale theme), D major, 4/4 ---
ode_mel = seq('''F#4 F#4 G4 A4 | A4 G4 F#4 E4 | D4 D4 E4 F#4 | F#4:1.5 E4:.5 E4:2 |
F#4 F#4 G4 A4 | A4 G4 F#4 E4 | D4 D4 E4 F#4 | E4:1.5 D4:.5 D4:2 |
E4 E4 F#4 D4 | E4 F#4:.5 G4:.5 F#4 D4 | E4 F#4:.5 G4:.5 F#4 E4 | D4 E4 A3:2 |
F#4 F#4 G4 A4 | A4 G4 F#4 E4 | D4 D4 E4 F#4 | E4:1.5 D4:.5 D4:2''')
ode_ch = chords('''D3+F#3+A3:4 | A2+E3+A3+C#4:4 | D3+F#3+A3:4 | A2+E3+A3+C#4:4 |
D3+F#3+A3:4 | A2+E3+A3+C#4:4 | D3+F#3+A3:4 | A2+E3+A3+C#4:2 D3+F#3+A3:2 |
A2+E3+A3+C#4:4 | D3+F#3+A3:2 A2+E3+A3+C#4:2 | A2+E3+A3+C#4:2 D3+F#3+A3:2 | D3+F#3+A3:2 A2+E3+G3+C#4:2 |
D3+F#3+A3:4 | A2+E3+A3+C#4:4 | D3+F#3+A3:4 | A2+E3+A3+C#4:2 D3+F#3+A3:2''')
ode_bass = [([ps[0]-12], 1.0) for (ps, d) in ode_ch for _ in range(int(d))]
P['ode'] = dict(tempo=118, parts=[
    dict(prog=73, notes=ode_mel, vel=96, legato=.95),                     # flute
    dict(prog=40, notes=[([p+12 for p in ps], d) for ps, d in ode_mel], vel=58, legato=.97),   # violin an octave up, soft
    dict(prog=48, notes=ode_ch, vel=56, legato=1.0),                      # strings
    dict(prog=45, notes=ode_bass, vel=74, legato=.5),                     # pizzicato bass
    dict(prog=9, notes=[(ps, d) if k % 2 == 0 else ([], d) for k, (ps, d) in enumerate([([x+24 for x in ps], d) for ps, d in ode_mel])], vel=40, legato=.6)])  # a little glockenspiel sparkle

# --- Mozart: Eine kleine Nachtmusik (K. 525, I), G major, the opening ---
nm1 = '''G4:1 r:.5 D4:.5 G4:1 r:.5 D4:.5 | G4:.5 D4:.5 G4:.5 B4:.5 D5:2 | C5:1 r:.5 A4:.5 C5:1 r:.5 A4:.5 | C5:.5 A4:.5 F#4:.5 A4:.5 D4:2 |'''
nm_end = '''G4:.5 B4:.5 D5:.5 B4:.5 G4:.5 B4:.5 D5:.5 G5:.5 | F#5:.5 D5:.5 A4:.5 F#4:.5 D4:1 r:1 | G4:.5 B4:.5 D5:.5 G5:.5 F#5:.5 A5:.5 C6:.5 A5:.5 | G5:1 D5:1 B4:1 G4:1 | G4:3 r:1'''
nm_mel = seq(nm1 + nm1 + nm_end)
nm_ch = chords('''G2+G3:2 G2+D3+B3:2 | G2+D3+B3:2 G2+D3+B3:2 | D3+F#3+C4:2 D3+F#3+A3:2 | D3+F#3+C4:2 D2+D3:2 |
G2+G3:2 G2+D3+B3:2 | G2+D3+B3:2 G2+D3+B3:2 | D3+F#3+C4:2 D3+F#3+A3:2 | D3+F#3+C4:2 D2+D3:2 |
G2+D3+B3:2 G2+D3+B3:2 | D3+F#3+A3:2 D3+A3+C4:2 | G2+D3+B3:2 D3+F#3+C4:2 | G2+D3+B3:2 D3+F#3+A3:2 | G2+D3+B3+G4:3 r:1''')
P['nacht'] = dict(tempo=132, parts=[
    dict(prog=40, notes=nm_mel, vel=100, legato=.8),                      # violins
    dict(prog=40, notes=[([p-12 for p in ps], d) for ps, d in nm_mel], vel=70, legato=.8),
    dict(prog=48, notes=nm_ch, vel=60, legato=.5),
    dict(prog=43, notes=[([ps[0]], d) for ps, d in nm_ch if ps] , vel=72, legato=.6)])   # cello/bass line

# --- Haydn: "Surprise" Symphony (No. 94, II), C major: the quiet tune, quieter again… then the loud chord ---
hy = '''C4:.5 C4:.5 E4:.5 E4:.5 | G4:.5 G4:.5 E4:1 | F4:.5 F4:.5 D4:.5 D4:.5 | B3:.5 B3:.5 G3:1 |
C4:.5 C4:.5 E4:.5 E4:.5 | G4:.5 G4:.5 C5:1 | A4:.5 A4:.5 F#4:.5 F#4:.5 | G4:1 r:1 |'''
hy_ch = '''C3+G3:2 | C3+E3+G3:2 | G2+D3+F3:2 | G2+D3+F3:2 | C3+G3:2 | C3+E3+G3:2 | D3+F#3+C4:2 | G2+D3+B3:1 r:1 |'''
hy_mel = seq(hy + hy + 'C4:.5 C4:.5 E4:.5 E4:.5 | G4:.5 G4:.5 E4:1 | F4:.5 F4:.5 D4:.5 D4:.5 | B3:.5 D4:.5 G4:1 | C4:2 |')
hy_chd = chords(hy_ch + hy_ch + 'C3+G3:2 | C3+E3+G3:2 | G2+D3+F3:2 | G2+D3+B3:2 | C3+E3+G3:2 |')
N1 = len(seq(hy))
def hy_vel(t, k, base=72):
    return base if k < N1 else (base*.38)          # the repeat is very quiet …
BANG = 2*16.0 - 1.0                                  # … and on the last beat of the quiet repeat: the surprise
P['surprise'] = dict(tempo=74, parts=[
    dict(prog=48, notes=hy_mel, vel=lambda t, k: (40 if 16 <= t < 32 else 74), legato=.55),
    dict(prog=45, notes=[([p-12 for p in ps], d) for ps, d in hy_chd], vel=lambda t, k: (24 if 16 <= t < 32 else 56), legato=.45),
    dict(prog=48, notes=[([], BANG), ([pitch(x) for x in 'G2 D3 G3 B3 D4 G4 B4'.split()], 1.0)], vel=127, legato=.95),   # the loud chord, all the strings
    dict(prog=60, notes=[([], BANG), ([pitch('G3'), pitch('D4'), pitch('G4')], 1.0)], vel=120, legato=.9),                 # horns
    dict(prog=47, notes=[([], BANG), ([pitch('G2')], .25), ([pitch('G2')], .25), ([pitch('G2')], .5)], vel=127, legato=.9)])  # timpani

# --- Brahms: Lullaby (Wiegenlied, Op. 49 No. 4), C major, 3/4 ---
br = seq('''r:2 E4:.5 E4:.5 | G4:2 E4:.5 E4:.5 | G4:2 E4:.5 G4:.5 | C5:1 B4:1.5 A4:.5 | A4:1 G4:1 D4:.5 E4:.5 |
F4:1 D4:1 D4:.5 E4:.5 | F4:2 D4:.5 F4:.5 | B4:.5 A4:.5 G4:1 B4:1 | C5:2 C4:.5 C4:.5 |
C5:2 A4:.5 F4:.5 | G4:2 E4:.5 C4:.5 | F4:1 G4:1 A4:1 | G4:2 C4:.5 C4:.5 |
C5:2 A4:.5 F4:.5 | G4:2 E4:.5 C4:.5 | F4:1 E4:1 D4:1 | C4:3''')
br_ch = chords('''r:3 | C3+G3+E4:3 | C3+G3+E4:3 | G2+F3+B3:3 | G2+F3+B3:3 |
G2+F3+B3:3 | G2+D3+F3+B3:3 | G2+F3+B3:3 | C3+G3+E4:3 |
F2+F3+A3:3 | C3+G3+E4:3 | F2+C3+A3:3 | C3+G3+E4:3 |
F2+F3+A3:3 | C3+G3+E4:3 | G2+F3+B3:3 | C3+G3+E4:3''')
br_harp = []
for ps, d in br_ch:
    if not ps: br_harp.append(([], d)); continue
    arp = sorted(ps); br_harp += [([arp[0]], 1.0), ([arp[1]], 1.0), ([arp[-1]], 1.0)]
P['lullaby'] = dict(tempo=80, parts=[
    dict(prog=10, notes=br, vel=92, legato=.98),            # music box
    dict(prog=8, notes=br, vel=36, legato=.9),              # celesta, very soft, for a warm double
    dict(prog=46, notes=br_harp, vel=54, legato=1.0),       # harp
    dict(prog=49, notes=br_ch, vel=34, legato=1.0)])        # soft strings

# --- Grieg: In the Hall of the Mountain King (Peer Gynt), B minor: sneaky, then faster and faster ---
mk = '''B3:.5 C#4:.5 D4:.5 E4:.5 F#4:.5 D4:.5 F#4:1 | F4:.5 C#4:.5 F4:1 E4:.5 C4:.5 E4:1 |
B3:.5 C#4:.5 D4:.5 E4:.5 F#4:.5 D4:.5 F#4:.5 B4:.5 | A4:.5 F#4:.5 D4:.5 F#4:.5 A4:2 |'''
mk_hi = mk.replace('B3', 'B4').replace('C#4', 'C#5').replace('D4', 'D5').replace('E4', 'E5').replace('F#4', 'F#5').replace('F4', 'F5').replace('C4', 'C5').replace('B4:.5 |', 'B5:.5 |').replace('A4', 'A5')
mk_mel = seq(mk + mk + mk_hi + mk_hi + 'B4:1 r:1 B3:2')
mk_mel = [(ps, d) for ps, d in mk_mel]
mk_bass = seq(' '.join(['B2:1 F#2:1 B2:1 F#2:1 | B2:1 F#2:1 B2:1 F#2:1 | B2:1 F#2:1 B2:1 F#2:1 | B2:1 F#2:1 B2:1 F#2:1 |']*4) + ' B1:2 r:2')
nb = 16*4
tempo_map = [(0, 96), (16, 104), (32, 118), (40, 128), (48, 142), (56, 158), (60, 170)]
P['mountain'] = dict(tempo=96, tempo_map=tempo_map, parts=[
    dict(prog=45, notes=mk_mel, vel=lambda t, k: 60 + t*0.9, legato=.5),          # pizzicato strings, louder and louder
    dict(prog=70, notes=mk_mel, vel=lambda t, k: (52 if t < 16 else 0 if t < 32 else 70), legato=.6),   # bassoon first, then again at the end
    dict(prog=48, notes=[(ps, d) if t >= 32 else ([], d) for (ps, d), t in zip(mk_mel, [sum(x[1] for x in mk_mel[:i]) for i in range(len(mk_mel))])], vel=lambda t, k: 50 + (t-32)*1.6, legato=.55),
    dict(prog=43, notes=mk_bass, vel=lambda t, k: 50 + t*0.8, legato=.4),
    dict(prog=47, notes=[([], 48.0)] + [([pitch('B1')], 1.0), ([pitch('F#2')], 1.0)]*8 + [([pitch('B1')], 2.0)], vel=110, legato=.5)])

# --- Beethoven: Symphony No. 5, the opening ---
b5 = seq('''r:.5 G4:.5 G4:.5 G4:.5 | Eb4:4 | r:.5 F4:.5 F4:.5 F4:.5 | D4:4 |
r:.5 G4:.5 G4:.5 G4:.5 | Eb4:.5 Ab4:.5 Ab4:.5 Ab4:.5 | G4:.5 Eb5:.5 Eb5:.5 Eb5:.5 | C5:3 r:1 |
r:.5 G4:.5 G4:.5 G4:.5 | D4:.5 Ab4:.5 Ab4:.5 Ab4:.5 | G4:.5 F5:.5 F5:.5 F5:.5 | D5:3 r:1''')
P['fifth'] = dict(tempo=108, parts=[
    dict(prog=48, notes=b5, vel=118, legato=.85),
    dict(prog=48, notes=[([p-12 for p in ps], d) for ps, d in b5], vel=110, legato=.85),
    dict(prog=42, notes=[([p-24 for p in ps], d) for ps, d in b5], vel=100, legato=.85),
    dict(prog=60, notes=[(ps, d) for ps, d in b5], vel=70, legato=.8)])

# --- Beethoven: "Moonlight" Sonata (I), C-sharp minor: the rocking triplets, and the tune coming in ---
tri = lambda a, b, c, n: [([pitch(a)], 1/3), ([pitch(b)], 1/3), ([pitch(c)], 1/3)]*n
ml_r = (tri('G#3','C#4','E4',4) + tri('G#3','C#4','E4',4) + tri('A3','C#4','E4',2) + tri('A3','D4','F#4',2)
        + tri('G#3','C4','F#4',1) + tri('G#3','C#4','E4',1) + tri('G#3','C#4','D#4',1) + tri('F#3','C4','D#4',1)
        + tri('E3','G#3','C#4',3) + tri('G#3','C#4','E4',1)
        + tri('G#3','C#4','E4',4) + tri('G#3','C#4','E4',2) + tri('A3','C#4','F#4',2)
        + tri('G#3','C#4','E4',2) + tri('G#3','B3','E4',2) + tri('G#3','C#4','E4',4))
ml_l = chords('C#2+C#3:4 | B1+B2:4 | A1+A2:2 F#1+F#2:2 | G#1+G#2:4 | C#2+C#3:4 | C#2+C#3:4 | C#2+C#3:2 A1+A2:2 | G#1+G#2:2 E2+E3:2 | C#2+C#3:4')
ml_m = seq('r:16 r:3 G#4:.75 G#4:.25 | G#4:3 G#4:.75 G#4:.25 | G#4:2 A4:2 | G#4:2 F#4:2 | E4:4')
P['moonlight'] = dict(tempo=56, parts=[
    dict(prog=0, notes=ml_r, vel=48, legato=1.0),
    dict(prog=0, notes=ml_l, vel=62, legato=1.0),
    dict(prog=0, notes=ml_m, vel=78, legato=.98)])

# ======================= what the app uses =======================
# Music box: (start, length) of the best-known part. Clips: name → (piece, start, length) for the levels.
BOX = {'ode': (0, 33.5), 'nacht': (0, 25), 'surprise': (0, 31), 'lullaby': (1.3, 38), 'mountain': (0, 33), 'fifth': (0, 20), 'moonlight': (0, 34)}
CLIPS = {
    'map-ode': ('ode', 0, 8.6),             # the map piece flies into the map
    'feel-happy': ('ode', 0, 8.6),
    'feel-excited': ('nacht', 0, 8.2),
    'feel-surprised': ('surprise', 17.6, 9.6),   # the quiet tune … and the loud chord
    'feel-tired': ('lullaby', 1.4, 9.0),
    'feel-scared': ('mountain', 0, 9.0),
    'feel-angry': ('fifth', 0, 8.0),
    'feel-sad': ('moonlight', 0, 9.0),
}
if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '.'; os.makedirs(out, exist_ok=True); tmp = os.path.join(out, '_wav'); os.makedirs(tmp, exist_ok=True)
    only = sys.argv[2:]
    for k, d in P.items():
        if only and k not in only: continue
        mid = os.path.join(tmp, k + '.mid'); wav = os.path.join(tmp, k + '.wav')
        build(d['parts'], d['tempo'], mid, d.get('tempo_map')); render(mid, wav)
        st, ln = BOX[k]; ln = min(ln, length(wav) - st); mp3(wav, os.path.join(out, f'{k}-box.mp3'), st, ln, fade_out=1.5)
        print(k, 'rendered', round(length(wav), 1), 's')
    for name, (k, st, ln) in CLIPS.items():
        if only and k not in only: continue
        mp3(os.path.join(tmp, k + '.wav'), os.path.join(out, name + '.mp3'), st, ln, fade_out=.9)
    print('done')
