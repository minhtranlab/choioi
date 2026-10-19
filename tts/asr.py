import sherpa_onnx,soundfile as sf,numpy as np,sys
M='/home/claude/models/'
_r={}
def rec(lang):
    if lang in _r: return _r[lang]
    if lang=='en':
        d=M+'sherpa-onnx-whisper-base.en/'
        r=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d+'base.en-encoder.int8.onnx',decoder=d+'base.en-decoder.int8.onnx',tokens=d+'base.en-tokens.txt',language='en',task='transcribe',num_threads=2)
    else:
        d=M+'sherpa-onnx-zipformer-vi-2025-04-20/'
        r=sherpa_onnx.OfflineRecognizer.from_transducer(encoder=d+'encoder-epoch-12-avg-8.onnx',decoder=d+'decoder-epoch-12-avg-8.onnx',joiner=d+'joiner-epoch-12-avg-8.onnx',tokens=d+'tokens.txt',num_threads=2)
    _r[lang]=r; return r
def transcribe(a,sr,lang):
    import soxr
    if sr!=16000: a=soxr.resample(a,sr,16000); sr=16000
    r=rec(lang); s=r.create_stream(); s.accept_waveform(sr,a.astype(np.float32)); r.decode_stream(s); return s.result.text.strip()
if __name__=='__main__':
    for f in sys.argv[2:]:
        a,sr=sf.read(f,dtype='float32'); 
        if a.ndim>1: a=a.mean(1)
        print(f,'|',transcribe(a,sr,sys.argv[1]))
