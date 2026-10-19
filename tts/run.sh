#!/bin/bash
# usage: run.sh SHARD (e.g. 2/5) SPEEDS (e.g. m,s,f)
set -e
cd "$(dirname "$0")"
M=/tmp/models; mkdir -p $M
pip install --break-system-packages -q kokoro-onnx soundfile sherpa-onnx soxr numpy >/dev/null 2>&1 || pip install -q kokoro-onnx soundfile sherpa-onnx soxr numpy
G=https://github.com
[ -f $M/kokoro-v1.0.onnx ] || curl -sL -o $M/kokoro-v1.0.onnx $G/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -f $M/voices-v1.0.bin ] || curl -sL -o $M/voices-v1.0.bin $G/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
[ -d $M/sherpa-onnx-whisper-base.en ] || (curl -sL -o $M/b.tar.bz2 $G/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-base.en.tar.bz2 && tar xjf $M/b.tar.bz2 -C $M && rm $M/b.tar.bz2)
sed -i "s#/home/claude/models/#$M/#g" kgen.py asr.py
python3 gen_en.py "$2" 1000000000 "$1"
# final format: mono 24 kHz MP3 40 kbit/s, one file per line
for d in clips/en-*; do for w in $d/*.wav; do ffmpeg -loglevel error -y -i "$w" -ac 1 -ar 24000 -c:a libmp3lame -b:a 40k "${w%.wav}.mp3" && rm "$w"; done; done
echo DONE
