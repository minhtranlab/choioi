#!/usr/bin/env python3
"""Bé chạm liên tục (29/10): chơi Màn 0 (hoặc màn khác) ở TỐC ĐỘ THẬT, giọng ghi âm thật, với một bé chạm suốt, và báo câu nào của
Chồi bị cắt vì bé chạm.

Luật (29/10, chat chính, mục 131 tài liệu thiết kế): câu dẫn chuyện và câu lệnh của Chồi ("Here comes my school bus!") KHÔNG BAO GIỜ
bị cắt vì bé chạm. Bé chạm đồ vật lúc Chồi đang nói: vẫn có tiếng động nhưng nhỏ hơn; câu Chồi gọi tên đồ vật ("A taxi!") bỏ qua.
Bộ này:
  - mở app như máy mới, trang chào, gõ tên bé, bấm "Chơi ngay" thật; qua màn chờ tải giọng (giọng ghi âm thật);
  - sau màn chờ, app tự trả lời (AUTO) để màn đi tiếp, còn "bé" bấm chuột thật (sự kiện thật như ngón tay):
      trang phố Màn 0: bấm xe liên tục (mỗi ~0,45 giây), cả lúc Chồi nói "Here comes my school bus!";
      các trang khác: bấm các bạn và đồ vật trong tranh mỗi ~1,3 giây, ai đang nói cũng vậy;
  - ghi từng câu và từng đoạn tiếng phát: bắt đầu, lẽ ra hết lúc nào, có bị dừng sớm không, và có phải ngay sau một cú chạm thật.
Kết quả: số câu của Chồi bị cắt ngay sau cú chạm (phải là 0), số tên đồ vật bỏ qua lúc Chồi nói, độ to tiếng còi lúc Chồi nói.
Thoát mã 1 khi có câu của Chồi bị cắt vì bé chạm.
    python3 tools/test/be_cham_lien_tuc.py                 # Màn 0, Chromium, bé tên Na (~10 phút)
    python3 tools/test/be_cham_lien_tuc.py --levels 0,1 --browser webkit
Lưu ý: câu đếm ("One." "Two.") khi app tự chạm rất nhanh vẫn cắt nhau như trước; bộ này chỉ tính câu bị cắt ngay sau cú chạm thật."""
import argparse, json, os, random, socket, subprocess, sys, time
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap = argparse.ArgumentParser(description='Bé chạm liên tục: câu của Chồi không bị cắt vì bé chạm')
ap.add_argument('--name', default='Na'); ap.add_argument('--browser', default='chromium', choices=['chromium', 'webkit'])
ap.add_argument('--levels', default='0', help='vd. 0 hoặc 0,1'); ap.add_argument('--url', default=''); ap.add_argument('--out', default='')
A = ap.parse_args(); LEVELS = [int(x) for x in A.levels.split(',')]
OUT = A.out or os.path.join('/tmp', f'be-cham-{A.browser}-{A.name}.json')
srv = None
if A.url: APP = A.url
else:
    s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1'], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1); APP = f'http://127.0.0.1:{port}/index.html'
HOOK = r"""()=>{ if(window.__A) return; window.__A=[]; window.__T0=performance.now(); const now=()=>Math.round(performance.now()-window.__T0);
  const LOG=o=>{ o.t=now(); window.__A.push(o); return o };
  window.__TN=false; ['pointerdown','pointerup','click'].forEach(t=>addEventListener(t,e=>{ if(!e.isTrusted) return; window.__TN=true; setTimeout(()=>{ window.__TN=false },0) },true));
  const TN=()=>window.__TN;
  const osay=say; say=(en,vi,opt={})=>{ const V=isVi()&&!!vi; const r=LOG({ev:'say',text:V?vi:en,tapped:TN(),react:!!opt.react,tapName:!!opt.tapName,free:!!opt.free,sayn:SAYN});
    const p=osay(en,vi,opt); p.then(()=>{ r.end=now() },()=>{ r.end=now() }); return p };
  const oclip=vClip; vClip=async(set,text,slow,kid)=>{ const b=await oclip(set,text,slow,kid); if(b&&typeof b==='object') b.__text=text; return b };
  const P=AudioBufferSourceNode.prototype, ost=P.start, osp=P.stop;
  P.start=function(...a){ if(this.buffer&&this.buffer.__text){ const r=LOG({ev:'start',text:this.buffer.__text,dur:+(this.buffer.duration/this.playbackRate.value).toFixed(2)}); this.__rec=r } return ost.apply(this,a) };
  P.stop=function(...a){ if(this.__rec&&!this.__rec.stopped){ this.__rec.stopped=now(); this.__rec.byTap=TN() } return osp.apply(this,a) };
  const oh=honk; honk=k=>{ LOG({ev:'honk',kind:k,vol:typeof tapVol==='function'?tapVol():1,sayn:SAYN}); return oh(k) };
  const og=voiceGate; voiceGate=async li=>{ AUTO=false; SPEED=1; await og(li); LOG({ev:'gate',li,mode:VOICE.mode}); AUTO=true; SPEED=1 };
}"""
STATE = r"""()=>{ if(!RUN) return null; const gate=window.__A.some(a=>a.ev==='gate'); const street=document.querySelector('#card .sbox.street0'); const out={gate,street:!!street};
  if(street){ const asked=window.__A.some(a=>a.ev==='say'&&a.text==='Tap the school bus!'&&a.end);
    out.pts=asked?[]:[...street.querySelectorAll('.xe[data-kind]')].filter(e=>e.dataset.kind!=='schoolbus'&&getComputedStyle(e).visibility!=='hidden').map(e=>e.getBoundingClientRect()).filter(r=>r.width>20&&r.left>30&&r.right<innerWidth-30&&r.top>0).map(r=>[r.left+r.width/2,r.top+r.height*.6]) }
  else { const box=document.querySelector('#card .sbox,#card .spage'); out.pts=box?[...box.querySelectorAll('.skid,.actor.kid,.sthing,.tpolly')].filter(e=>!e.closest('.travelold')&&!e.closest('[data-live]')).map(e=>e.getBoundingClientRect()).filter(r=>r.width>10&&r.top>0&&r.bottom<innerHeight).map(r=>[r.left+r.width/2,r.top+r.height/2]):[] }
  return out }"""
random.seed(29); res = {'app': APP, 'browser': A.browser, 'name': A.name, 'levels': LEVELS, 'errors': [], 'taps': 0}; code = 0
try:
    with sync_playwright() as p:
        br = (p.webkit if A.browser == 'webkit' else p.chromium).launch(); ctx = br.new_context(viewport={'width': 1180, 'height': 820})
        pg = ctx.new_page(); pg.on('pageerror', lambda e: res['errors'].append(str(e)))
        pg.goto(APP); pg.wait_for_timeout(1500); pg.evaluate(HOOK); pg.evaluate("()=>{ S.limitMin=0; S.consentMic=false }")
        pg.fill('#p-ten', A.name); pg.click('.tc-play')
        for i, li in enumerate(LEVELS):
            if i:
                pg.evaluate("()=>{ S.limitMin=0; S.consentMic=false; saveLocal() }"); pg.wait_for_selector(f'#pathmap .node[data-i="{li}"]', timeout=30000); pg.wait_for_timeout(1200)
                b = pg.locator(f'#pathmap .node[data-i="{li}"]').bounding_box(); pg.mouse.click(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2)
            t0 = time.time(); pg.wait_for_function("()=>!!RUN", timeout=20000); last = 0
            while True:
                st = pg.evaluate(STATE)
                if not st: break
                if time.time() - t0 > 1800: res['errors'].append(f'Màn {li}: quá 30 phút'); break
                if st['gate'] and st['pts'] and time.time() - last > (0.45 if st['street'] else 1.3):
                    x, y = random.choice(st['pts']); pg.mouse.click(x, y); res['taps'] += 1; last = time.time()
                time.sleep(0.08)
        res['log'] = pg.evaluate("()=>window.__A"); ctx.close(); br.close()
finally:
    if srv: srv.terminate()
L = res.get('log', []); says = [e for e in L if e['ev'] == 'say']; starts = [e for e in L if e['ev'] == 'start']
cut = []
for s in starts:
    if s.get('stopped') and s['stopped'] < s['t'] + s['dur'] * 1000 - 120:
        sy = [x for x in says if x['text'] == s['text'] and x['t'] <= s['t'] + 50]; sy = sy[-1] if sy else {}
        if sy.get('tapName') or sy.get('react') or sy.get('free') or sy.get('tapped'): continue   # not Chồi's telling or asking
        cut.append({'text': s['text'], 'played': round((s['stopped'] - s['t']) / 1000, 2), 'of': s['dur'], 'byTap': bool(s.get('byTap'))})
names = [x for x in says if x.get('tapName')]
left_out = [x for x in names if not any(st['text'] == x['text'] and x['t'] - 50 <= st['t'] <= x['t'] + 3000 for st in starts)]
honks = [e for e in L if e['ev'] == 'honk']; talking = [h for h in honks if h['sayn']]
res.update(cut=cut, names=len(names), namesLeftOut=len(left_out), honks=len(honks), honksWhileTalking=len(talking), honkVolWhileTalking=sorted(set(h['vol'] for h in talking)))
json.dump(res, open(OUT, 'w'), ensure_ascii=False, indent=0)
byTap = [c for c in cut if c['byTap']]
print(f"{A.browser}, bé tên {A.name}, Màn {A.levels}: {len(says)} câu, bé chạm {res['taps']} lần; lỗi trang: {res['errors'][:2] or 'không'}")
print(f"  câu của Chồi bị cắt ngay sau cú chạm của bé: {len(byTap)}" + ''.join(f"\n    CẮT: {c['text']!r} ({c['played']}/{c['of']} giây)" for c in byTap))
print(f"  câu của Chồi dừng sớm vì lý do khác (câu sau của app, đếm khi app tự chạm nhanh): {len(cut) - len(byTap)}")
print(f"  tên đồ vật khi bé chạm: {len(names)} lần, bỏ qua lúc Chồi đang nói: {len(left_out)}")
print(f"  tiếng còi: {len(honks)} lần, lúc Chồi đang nói {len(talking)} lần, độ to {res['honkVolWhileTalking']}")
print(f"  (chi tiết: {OUT})")
if byTap or res['errors']: code = 1
sys.exit(code)
