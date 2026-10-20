# Music in Chồi Ơi

Every music file here is **our own recording**: the notes of famous classical pieces (all public domain) were written by hand in
`tools/music/compose.py`, turned into MIDI, and played by FluidSynth with the **FluidR3 GM** instrument set
(© Frank Wen, released under the **MIT licence**). No outside recording is used, so there is no licence to check for the recordings.

To make them again: `apt install fluidsynth fluid-soundfont-gm`, `pip install mido`, then `python3 tools/music/compose.py music`.

**Loudness (20/10):** every clip is brought to the same loudness (EBU R128, about −17 LUFS) with a limiter, so the clips sound about
as loud as each other. Nobody has to turn the volume up for a quiet piece and then get a fright at a loud part.

| File | Piece | Used for |
|---|---|---|
| `ode-box.mp3`, `nacht-box.mp3`, `lullaby-box.mp3`, `mountain-box.mp3`, `moonlight-box.mp3`, `fifth-box.mp3` | the best-known part of each piece (20–38 s) | the Music box (a piece opens there once the child has heard it in a level) |
| `feel-excited.mp3` | Mozart, Eine kleine Nachtmusik | excited (Màn 2 lanterns) |
| `feel-sad.mp3` | Beethoven, Moonlight Sonata | sad (Màn 2 lanterns: the other lantern) |
| `feel-tired.mp3` | Brahms, Lullaby | tired (Màn 3 music box) |
| `lullaby-box.mp3` | Brahms, Lullaby | under Ben's bedtime (Màn 2) |
| `feel-scared.mp3` | Grieg, In the Hall of the Mountain King | scared, in a playful way (Màn 3 music box) |
| `feel-angry.mp3` | Beethoven, Symphony No. 5 | angry |
| `feel-happy.mp3` | Beethoven, Ode to Joy (Symphony No. 9) | music that sounds happy. Ode to Joy is kept for the treasure chest at the end of Màn 7 (it opens in the Music box there) |
| `surprise-box.mp3`, `feel-surprised.mp3` | Haydn, Symphony No. 94 "Surprise" | not used now (it sounds more startling than surprised); kept for Unit 2 (hearing: loud and quiet) |
