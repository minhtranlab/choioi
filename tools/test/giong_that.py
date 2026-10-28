#!/usr/bin/env python3
"""Kiểm giọng thật (28/10): chơi các màn với GIỌNG GHI ÂM THẬT, đi đúng đường phát như trên máy phụ huynh, và báo mọi câu "chỉ hiện chữ".

Vì sao: máy tự chơi nhanh (#fast, #auto, #time) không dùng giọng ghi âm, nên không bắt được câu im (28/10: bé tên Na thì nhiều câu
ở Màn 0 chỉ có chữ). Bộ này:
  - mở app như máy mới (không có gì trong bộ nhớ), trang chào, gõ tên bé, bấm "Chơi ngay" thật (cú chạm thật mở được âm thanh);
  - Màn 0 chạy qua màn chờ tải giọng (voiceGate → VOICE.mode 'rec'), các màn sau bé chạm trên bản đồ như thật;
  - sau màn chờ, app tự chạm (AUTO); có thể tua: SPEED (chờ và chuyển động ngắn lại) và vrate (tiếng phát nhanh hơn), nhưng mỗi câu
    vẫn đi đúng đường thật: tìm bản ghi (vEntry) → tải file (vBundle) → giải mã (decodeAudioData) → phát (AudioBufferSourceNode.start);
  - ghi từng câu hiện chữ và câu đó CÓ THẬT SỰ BẮT ĐẦU PHÁT không (bắt AudioBufferSourceNode.start của đúng câu đó).
Câu im được báo kèm lý do: chưa có bản ghi · file chưa tải kịp · âm thanh bị chặn · màn không ở chế độ giọng ghi âm.

CHẠY TRƯỚC MỖI LẦN ĐẨY (khoảng 25–35 phút cho 8 màn với tua mặc định):
    python3 tools/test/giong_that.py                     # 8 màn, Chromium, tiếng Anh, bé tên Na
    python3 tools/test/giong_that.py --lang vi
    python3 tools/test/giong_that.py --browser webkit --levels 0-1 --name Ben
Tên mặc định là Na (trùng tên một bạn trong đội): bắt được cả lỗi tên bé lẫn câu thiếu bản ghi.
Kết quả: in ra màn hình, ghi --out (JSON). Thoát mã 1 khi có câu im (để chặn việc đẩy).
Cần: pip install playwright; python3 -m playwright install chromium webkit."""
import argparse, json, os, socket, subprocess, sys, time
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap = argparse.ArgumentParser(description='Kiểm giọng thật: báo mọi câu chỉ hiện chữ')
ap.add_argument('--name', default='Na'); ap.add_argument('--browser', default='chromium', choices=['chromium', 'webkit'])
ap.add_argument('--levels', default='0-7', help='vd. 0-7, 0-1, 3'); ap.add_argument('--lang', default='en', choices=['en', 'vi'])
ap.add_argument('--speed', type=float, default=0.3, help='hệ số chờ của app (1 = thật)'); ap.add_argument('--vrate', type=float, default=2.5, help='tốc độ phát tiếng (1 = thật)')
ap.add_argument('--url', default='', help='địa chỉ app có sẵn; bỏ trống thì tự mở một máy chủ ở thư mục repo')
ap.add_argument('--out', default=''); ap.add_argument('--net', type=int, default=0, help='thêm độ trễ (ms) cho mỗi file giọng: mạng chậm')
A = ap.parse_args()
a, b = (A.levels.split('-') + [None])[:2]; LEVELS = list(range(int(a), int(b or a) + 1))
OUT = A.out or os.path.join('/tmp', f'giong-that-{A.browser}-{A.lang}-{A.name}.json')

srv = None
if A.url: APP = A.url
else:
    s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1); APP = f'http://127.0.0.1:{port}/index.html'

HOOK = r"""()=>{ if(window.__A) return;
  window.__A=[]; window.__T0=performance.now(); const now=()=>Math.round(performance.now()-window.__T0);
  const LOG=o=>{ o.t=now(); window.__A.push(o); return o };
  const osay=say; say=(en,vi,opt={})=>{ const V=isVi()&&!!vi; const rec=LOG({ev:'say',text:V?vi:en,kid:opt.kid===undefined?null:opt.kid,polly:!!opt.polly,lesson:RUN&&RUN.lesson,step:RUN&&RUN.step,mode:VOICE.mode,ctx:AC?AC.state:'none'});
    const n=(window.__briefSkipped||[]).length; const p=osay(en,vi,opt); if((window.__briefSkipped||[]).length>n) rec.skipped=true;
    p.then(()=>{ rec.end=now() },()=>{ rec.end=now(); rec.aborted=true }); return p };
  const oclip=vClip; vClip=async(set,text,slow,kid)=>{ const t1=now(); let r; try{ r=await oclip(set,text,slow,kid) }catch(e){ r='throw' }
    LOG({ev:'clip',text,res:r===null?'null':typeof r==='string'?r:'buffer',ms:now()-t1,ctx:AC?AC.state:'none'}); if(r&&typeof r==='object') r.__text=text; return r };
  const P=AudioBufferSourceNode.prototype, ost=P.start;
  P.start=function(...a){ if(this.buffer&&this.buffer.__text) LOG({ev:'start',text:this.buffer.__text,ctx:this.context.state}); return ost.apply(this,a) };
  // the voice gate as on a parent's device (AUTO off: test runs skip it); after it the app taps by itself
  const og=voiceGate; voiceGate=async li=>{ AUTO=false; SPEED=1; await og(li); LOG({ev:'gate',li,mode:VOICE.mode}); AUTO=true; SPEED=window.__SPEED; window.__vrate=window.__VRATE };
}"""
WHY = {'null': 'chưa có bản ghi', 'fail': 'file giọng chưa tải kịp / không giải mã được', 'throw': 'lỗi khi tìm bản ghi', 'no-clip': 'không phát (âm thanh bị chặn hoặc bị bỏ)'}
res = {'app': APP, 'browser': A.browser, 'name': A.name, 'lang': A.lang, 'speed': A.speed, 'vrate': A.vrate, 'levels': [], 'errors': []}
code = 0
try:
    with sync_playwright() as p:
        br = (p.webkit if A.browser == 'webkit' else p.chromium).launch()
        ctx = br.new_context(viewport={'width': 1180, 'height': 820})
        if A.net:
            def slow(route, request): time.sleep(A.net / 1000); route.continue_()
            ctx.route('**/voice/*.mp3*', slow)
        pg = ctx.new_page(); pg.on('pageerror', lambda e: res['errors'].append(str(e)))
        pg.goto(APP); pg.wait_for_timeout(1500)
        if LEVELS[0] > 0:   # start later: the levels before are done (a child coming back), then from the map
            pg.evaluate(f"()=>{{ S.child={{name:{json.dumps(A.name)}}}; S.lang='{A.lang}'; S.consentMic=false; S.limitMin=0; S.done=Object.fromEntries([...Array({LEVELS[0]}).keys()].map(i=>[i,1])); S.lesson={LEVELS[0]}; saveLocal(); location.reload() }}")
            pg.wait_for_timeout(2000)
        pg.evaluate(f"()=>{{ window.__SPEED={A.speed}; window.__VRATE={A.vrate} }}"); pg.evaluate(HOOK)
        if LEVELS[0] == 0:
            if A.lang == 'vi': pg.evaluate("()=>{ S.lang='vi'; saveLocal() }")
            pg.evaluate("()=>{ S.consentMic=false; S.limitMin=0 }")   # no play-time reminder in the middle of the test
            pg.fill('#p-ten', A.name); pg.click('.tc-play')
        for i, li in enumerate(LEVELS):
            if not (i == 0 and li == 0):
                pg.wait_for_selector(f'#pathmap .node[data-i="{li}"]', timeout=60000); pg.wait_for_timeout(1200)
                bb = pg.locator(f'#pathmap .node[data-i="{li}"]').bounding_box(); pg.mouse.click(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2)
            t0 = time.time(); n0 = pg.evaluate("()=>window.__A.length")
            pg.wait_for_function("()=>!!RUN", timeout=30000)
            while pg.evaluate("()=>!!RUN"):
                if time.time() - t0 > 3600: res['errors'].append(f'Màn {li}: quá 60 phút'); break
                time.sleep(1)
            L = pg.evaluate(f"()=>window.__A.slice({n0})")
            says = [e for e in L if e['ev'] == 'say' and not e.get('skipped')]
            starts = [e for e in L if e['ev'] == 'start']; clips = [e for e in L if e['ev'] == 'clip']
            silent = []
            for s in says:
                t1 = s.get('end', s['t'] + 120000)
                if any(x['text'] == s['text'] and s['t'] - 50 <= x['t'] <= t1 + 50 for x in starts): continue
                if s['mode'] != 'rec':
                    silent.append({'text': s['text'], 'kid': s['kid'], 'why': f"màn không ở chế độ giọng ghi âm ({s['mode']})", 'step': s['step']}); continue
                cl = [x for x in clips if x['text'] == s['text'] and s['t'] - 50 <= x['t'] <= t1 + 50]
                why = WHY.get(cl[0]['res'], cl[0]['res']) if cl and cl[0]['res'] != 'buffer' else WHY['no-clip']
                if s.get('aborted') and cl and cl[0]['res'] == 'buffer': continue   # the level stopped right then: not a silent line
                silent.append({'text': s['text'], 'kid': s['kid'], 'why': why, 'step': s['step'], 'ctx': s['ctx']})
            lv = {'level': li, 'secs': round(time.time() - t0), 'lines': len(says), 'silent': silent}
            res['levels'].append(lv)
            print(f"Màn {li}: {len(says)} câu, {len(silent)} câu chỉ hiện chữ ({lv['secs']} s)", flush=True)
            for s in silent: print(f"   IM  [{s['why']}] {s['text']}" + (f"  ({s['kid']})" if s['kid'] else ''), flush=True)
        br.close()
finally:
    if srv: srv.terminate()
total = sum(len(l['silent']) for l in res['levels'])
res['silentTotal'] = total
json.dump(res, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(f"\nTổng: {sum(l['lines'] for l in res['levels'])} câu, {total} câu chỉ hiện chữ. Lỗi trang: {res['errors'][:3]}. Chi tiết: {OUT}")
sys.exit(1 if total or res['errors'] else 0)
