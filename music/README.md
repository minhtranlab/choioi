# Music in Chồi Ơi

Every music file here is **our own recording**: the notes of famous classical pieces (all public domain) were written by hand in
`tools/music/compose.py`, turned into MIDI, and played by FluidSynth with the **FluidR3 GM** instrument set
(© Frank Wen, released under the **MIT licence**). No outside recording is used, so there is no licence to check for the recordings.

To make them again: `apt install fluidsynth fluid-soundfont-gm`, `pip install mido`, then `python3 tools/music/compose.py music`.

| File | Piece | Used for |
|---|---|---|
| `map-ode.mp3` | Beethoven, Ode to Joy (Symphony No. 9) | the map piece flying into the map, every level |
| `ode-box.mp3`, `nacht-box.mp3`, `surprise-box.mp3`, `lullaby-box.mp3`, `mountain-box.mp3`, `fifth-box.mp3`, `moonlight-box.mp3` | the best-known part of each piece (20–38 s) | the Music box |
| `feel-happy.mp3` | Ode to Joy | music that sounds happy |
| `feel-excited.mp3` | Mozart, Eine kleine Nachtmusik | excited (Màn 2 lanterns) |
| `feel-surprised.mp3` | Haydn, Symphony No. 94 "Surprise", the loud chord | surprised (Màn 2 lanterns) |
| `feel-tired.mp3` | Brahms, Lullaby | tired (Màn 2 bedtime, Màn 3 music box) |
| `feel-scared.mp3` | Grieg, In the Hall of the Mountain King | scared, in a playful way (Màn 3 music box) |
| `feel-angry.mp3` | Beethoven, Symphony No. 5 | angry |
| `feel-sad.mp3` | Beethoven, Moonlight Sonata | sad |
