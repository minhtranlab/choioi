/* Cảnh hài Unit 1 (27/10) · phần chung cho 6 cảnh (man-1.js … man-6.js).
   Không dùng thư viện ngoài: chỉ Web Animations API (el.animate) và một ít CSS.
   Cách gọi một cảnh: const r = await CanhHai.man1(box, {…});  box là khung cảnh (trong app là .sbox, tỉ lệ 200/140).
   Mọi vị trí tính bằng % của box, giống kidAt(): x = tâm theo chiều ngang, b = đáy tính từ dưới lên, w = bề rộng.
   Tuỳ chọn chung cho mọi cảnh:
     speed   hệ số thời gian (1 = bình thường, 2 = chậm gấp đôi; trong app truyền SPEED)
     signal  AbortSignal: huỷ giữa chừng (bấm lại) → dọn sạch, Promise vẫn resolve
     am(key, chu, ai)  gọi ở mỗi chỗ có tiếng động / câu nói (app phát tiếng ở đây; ai = ai nói, vd. 'Lam'); xem bảng trong README
     chu     true: hiện chữ nhỏ "[bụp]", "Triangle! Triangle!" (mặc định: true khi không có am)
     giamChuyenDong  true/false: ép bật/tắt; mặc định theo máy (prefers-reduced-motion) → bật thì bỏ qua cảnh
   Promise trả về { xong:true, xoa() } (xoa() gỡ mọi thứ cảnh còn để lại), hoặc { boQua:true } khi máy bật giảm chuyển động. */
(function () {
  'use strict';
  const CH = window.CanhHai = window.CanhHai || {};
  CH.HINH = CH.HINH || {};
  const HUY = CH.HUY = { huy: true };

  CH.giamChuyenDong = () => !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
  CH.css = (id, text) => { if (document.getElementById(id)) return; const s = document.createElement('style'); s.id = id; s.textContent = text; document.head.append(s) };

  CH.css('ch-chung', `
.ch-sp{position:absolute;translate:-50% 0;pointer-events:none;z-index:6;line-height:0}
.ch-sp>.ch-in{position:relative;transform-origin:50% 100%}
.ch-q{position:relative}.ch-q.lat{transform:scaleX(-1)}
.ch-sp svg{display:block;width:100%;height:auto;overflow:visible}
.ch-pose>i{display:none}.ch-pose>i.on{display:block}
.ch-lop{position:absolute;inset:0}.ch-lop>svg{position:absolute;left:0;top:0}
.ch-bay .ch-pose>i.on{display:none}
.ch-bay .ch-pose>i.f1,.ch-bay .ch-pose>i.f2{display:block}
.ch-bay .ch-pose>i.f2{position:absolute;left:0;top:0;width:100%}
.ch-bay .ch-pose>i.f1{animation:chVoA var(--ch-vo,.3s) steps(1) infinite}
.ch-bay .ch-pose>i.f2{animation:chVoB var(--ch-vo,.3s) steps(1) infinite}
@keyframes chVoA{0%{visibility:visible}50%{visibility:hidden}}
@keyframes chVoB{0%{visibility:hidden}50%{visibility:visible}}
.ch-bay .ch-lop.theo-bay{transform:translateY(-3.846%)}
.ch-chu{position:absolute;z-index:30;translate:-50% 0;background:#fff;color:#361D46;font:900 clamp(10px,4cqh,18px)/1.15 Nunito,system-ui,sans-serif;padding:.22em .6em;border-radius:999px;border:2px solid #361D46;white-space:nowrap;pointer-events:none;box-shadow:0 2px 0 rgba(54,29,70,.25)}
.ch-chu.loi{background:#FFF3C4}
.ch-hat{position:absolute;pointer-events:none;z-index:9;border-radius:50%}
`);

  /** một lần chạy cảnh: hẹn giờ, chuyển động, hình tạm, dọn dẹp */
  function ctx(box, o) {
    const C = { box, o, sp: Math.max(.05, +o.speed || 1), anims: [], timers: [], rejs: [], els: [], back: [], dead: false };
    C.chu = o.chu != null ? !!o.chu : !o.am;
    const sig = o.signal;
    const stop = () => { if (C.dead) return; C.dead = true; C.timers.forEach(clearTimeout); C.rejs.forEach(r => r(HUY)); C.anims.forEach(a => { try { a.cancel() } catch (e) {} }) };
    if (sig) { if (sig.aborted) stop(); else sig.addEventListener('abort', stop, { once: true }) }
    C.stop = stop;
    C.ms = t => t * C.sp;
    C.cho = t => new Promise((res, rej) => { if (C.dead) return rej(HUY); C.rejs.push(rej); C.timers.push(setTimeout(res, C.ms(t))) });
    /** chạy một chuyển động trên el; chờ xong. giu: giữ trạng thái cuối */
    C.an = (el, kf, t, { ez = 'ease-in-out', giu = false, lap = 1, tre = 0, dir } = {}) => {
      if (C.dead) return Promise.reject(HUY);
      const a = el.animate(kf, { duration: C.ms(t), easing: ez, fill: giu ? 'forwards' : 'none', iterations: lap, delay: C.ms(tre), direction: dir });
      C.anims.push(a); return a.finished.catch(() => { throw HUY })
    };
    C.chay = (el, kf, t, opt) => { C.an(el, kf, t, opt).catch(() => {}) };   // chạy mà không chờ
    /** khung box (px) */
    C.R = () => box.getBoundingClientRect();
    /** vị trí một phần tử trong box, theo %: x tâm, b đáy, w rộng, h cao */
    C.rect = el => { const r = C.R(), q = el.getBoundingClientRect(); return { x: (q.left + q.width / 2 - r.left) / r.width * 100, b: (r.bottom - q.bottom) / r.height * 100, w: q.width / r.width * 100, h: q.height / r.height * 100 } };
    /** một hình (svg hoặc tên trong CanhHai.HINH) đặt vào box; W×H là khung svg */
    C.hinh = (art, { x = 50, b = 0, w = 10, z = 6, lat = false, cls = '' } = {}) => {
      const svg = CH.HINH[art] || art;
      const s = document.createElement('div'); s.className = 'ch-sp ' + cls;
      s.innerHTML = `<div class="ch-in"><div class="ch-q${lat ? ' lat' : ''}">${svg}</div></div>`;
      const vb = (svg.match(/viewBox="([^"]+)"/) || [, '0 0 100 100'])[1].split(/[\s,]+/).map(Number);
      s.W = vb[2]; s.H = vb[3]; s.w = w; s.lat = lat;
      C.dat(s, x, b); s.style.width = w + '%'; s.style.zIndex = z;
      box.append(s); C.els.push(s); return s
    };
    C.dat = (s, x, b) => { s.x = x; s.b = b; s.style.left = x + '%'; s.style.bottom = b + '%' };
    /** cao của hình s theo % box */
    C.cao = s => s.w * (s.H / s.W) * (C.R().width / C.R().height);
    /** đặt sao cho điểm (ax, ay) trong khung svg của s nằm ở (tx, tb) của box; trả {x, b} */
    C.neo = (s, ax, ay, tx, tb) => { const axx = s.lat ? s.W - ax : ax; return { x: tx - (axx / s.W - .5) * s.w, b: tb - (1 - ay / s.H) * C.cao(s) } };
    /** điểm (ax, ay) của khung svg s đang ở đâu trong box (%) */
    C.diem = (s, ax, ay) => { const axx = s.lat ? s.W - ax : ax; return { x: s.x + (axx / s.W - .5) * s.w, b: s.b + (1 - ay / s.H) * C.cao(s) } };
    /** di chuyển theo một hay nhiều điểm {x, b}; chờ xong */
    C.di = async (s, pts, t, ez = 'ease-in-out') => {
      pts = Array.isArray(pts) ? pts : [pts];
      const kf = [{ left: s.x + '%', bottom: s.b + '%' }, ...pts.map(p => ({ left: (p.x ?? s.x) + '%', bottom: (p.b ?? s.b) + '%', ...(p.o != null ? { offset: p.o } : {}) }))];
      const end = pts[pts.length - 1];
      await C.an(s, kf, t, { ez, giu: true });
      C.dat(s, end.x ?? s.x, end.b ?? s.b); C.anims.filter(a => a.effect && a.effect.target === s).forEach(a => { if (a.playState === 'finished') a.cancel() })
    };
    /** chuyển động trong (xoay, nhún, lắc) của hình s; không dời chỗ */
    C.lam = (s, kf, t, opt) => C.an(s.firstElementChild, kf, t, opt);
    /** lật mặt hình s (quay trái / phải) */
    C.quay = (s, lat) => { s.lat = lat; s.querySelector('.ch-q').classList.toggle('lat', lat) };
    /** tiếng động / câu nói: báo cho app (o.am), và hiện chữ nhỏ nếu cần. at: hình hoặc {x, b} */
    C.am = (key, chu, at, { loi = false, t = 1300, ai } = {}) => {
      try { o.am && o.am(key, chu, ai) } catch (e) {}
      if (!C.chu || C.dead) return;
      let x = 50, b = 70;
      if (at && at.nodeType) { const r = C.rect(at); x = r.x; b = r.b + r.h + 2 } else if (at) { x = at.x; b = at.b }
      const c = document.createElement('div'); c.className = 'ch-chu' + (loi ? ' loi' : ''); c.textContent = chu;
      c.style.left = Math.max(10, Math.min(90, x)) + '%'; c.style.bottom = Math.min(90, b) + '%';
      box.append(c); C.els.push(c);
      const cw = c.getBoundingClientRect().width / C.R().width * 100;   // chữ không tràn ra ngoài khung
      c.style.left = Math.max(cw / 2 + 1, Math.min(99 - cw / 2, x)) + '%';
      c.animate([{ opacity: 0, transform: 'scale(.6)' }, { opacity: 1, transform: 'scale(1.08)', offset: .15 }, { opacity: 1, transform: 'scale(1)', offset: .3 }, { opacity: 1, offset: .8 }, { opacity: 0 }], { duration: C.ms(t) }).finished.then(() => c.remove(), () => c.remove())
    };
    /** mượn một phần tử có sẵn trong cảnh (rổ, mái nhà, mèo…): một bản sao đặt đúng chỗ để cảnh tự chuyển động; bản gốc ẩn tạm */
    C.muon = (el, { z = 6 } = {}) => {
      const r = C.rect(el), cl = el.cloneNode(true);
      cl.removeAttribute('id'); cl.querySelectorAll('[id]').forEach(n => n.removeAttribute('id'));
      cl.style.cssText += ';position:relative;left:auto;right:auto;top:auto;bottom:auto;inset:auto;translate:none;transform:none;rotate:none;scale:none;width:100%;height:auto;margin:0;animation:none;transition:none;visibility:visible;opacity:1';
      const s = document.createElement('div'); s.className = 'ch-sp ch-muon';
      const inn = document.createElement('div'); inn.className = 'ch-in'; const q = document.createElement('div'); q.className = 'ch-q'; q.append(cl); inn.append(q); s.append(inn);
      s.W = 100; s.H = 100 * r.h / r.w * (C.R().height / C.R().width); s.w = r.w; s.lat = false;
      C.dat(s, r.x, r.b); s.style.width = r.w + '%'; s.style.zIndex = z;
      box.append(s); C.els.push(s);
      const was = el.style.visibility; el.style.visibility = 'hidden'; C.back.push(() => { el.style.visibility = was });
      s.goc = el; s.tra = () => { el.style.visibility = was; s.remove() };
      return s
    };
    /** Polly: một hình có mọi tư thế cần (tu = 'dung', 'noi', 'bay' (vỗ cánh), 'treo-nguoc', 'ngu', 'tha', 'tho-1'…) */
    C.polly = ({ x = 50, b = 50, w = 11, z = 7, lat = true, tu = 'bay', voMs = 300 } = {}) => {
      const P = n => CH.HINH['polly-' + n] || '';
      const poses = ['dung', 'noi', 'treo-nguoc', 'ngu', 'tho-1', 'tho-2'];
      const s = C.hinh(`<div class="ch-pose">${poses.map(p => `<i data-p="${p}">${P(p)}</i>`).join('')}<i class="f1">${P('bay-1')}</i><i class="f2">${P('bay-2')}</i></div>`, { x, b, w, z, lat, cls: 'ch-polly' });
      s.W = 200; s.H = 260;
      s.tu = n => {
        s._tu = n; const pose = s.querySelector('.ch-pose');
        s.classList.toggle('ch-bay', n === 'bay' || n === 'tha');
        if (n === 'tha') { pose.querySelector('.f1').innerHTML = P('tha-1'); pose.querySelector('.f2').innerHTML = P('tha-2') }
        else if (n === 'bay') { pose.querySelector('.f1').innerHTML = P('bay-1'); pose.querySelector('.f2').innerHTML = P('bay-2') }
        pose.querySelectorAll('i[data-p]').forEach(i => i.classList.toggle('on', i.dataset.p === n))
      };
      s.vo = msV => s.style.setProperty('--ch-vo', C.ms(msV) + 'ms');
      /** một lớp phủ cùng khung Polly (bọt trên mỏ, vỏ chuối đội đầu…); theoBay: dời lên theo thân khi bay */
      s.lop = (html, { theoBay = true, cls = '' } = {}) => { const l = document.createElement('div'); l.className = 'ch-lop ' + (theoBay ? 'theo-bay ' : '') + cls; l.innerHTML = html; s.querySelector('.ch-q').append(l); return l };
      s.vo(voMs); s.tu(tu);
      return s
    };
    /** mỏ Polly (đầu mỏ, khung 200×260): đứng (162, 118); bay cao hơn 10 */
    C.mo = p => C.diem(p, 162, p._tu === 'bay' || p._tu === 'tha' ? 108 : 118);
    /** vài hạt nhỏ bắn ra từ (x, b) (bọt, bụi): màu, số hạt, cỡ (% box) */
    C.hat = (x, b, { n = 7, mau = '#fff', vien = '#361D46', co = 1.6, xa = 7, t = 600 } = {}) => {
      const r = C.R();
      for (let i = 0; i < n; i++) {
        const d = document.createElement('i'); d.className = 'ch-hat';
        const sz = co * (0.6 + Math.random() * .8) * r.width / 100;
        d.style.cssText = `left:${x}%;bottom:${b}%;width:${sz}px;height:${sz}px;background:${mau};border:${vien ? `1.5px solid ${vien}` : 'none'};translate:-50% 50%`;
        box.append(d); C.els.push(d);
        const a = (i / n) * Math.PI * 2 + Math.random() * .6, dx = Math.cos(a) * xa * r.width / 100, dy = -Math.sin(a) * xa * r.width / 100;
        d.animate([{ transform: 'translate(0,0) scale(1)', opacity: 1 }, { transform: `translate(${dx}px,${dy}px) scale(.4)`, opacity: 0 }], { duration: C.ms(t), easing: 'cubic-bezier(.2,.7,.4,1)', fill: 'forwards' }).finished.then(() => d.remove(), () => d.remove())
      }
    };
    /** dọn: gỡ mọi hình tạm, trả lại phần tử đã mượn */
    C.xoa = () => { C.stop(); C.els.forEach(e => e.remove()); C.els = []; C.back.reverse().forEach(f => f()); C.back = [] };
    return C
  }

  /** chạy một cảnh: bỏ qua khi giảm chuyển động; dọn sạch khi bị huỷ */
  CH.chay = async (box, o = {}, fn) => {
    const giam = o.giamChuyenDong != null ? !!o.giamChuyenDong : CH.giamChuyenDong();
    if (!box || giam) return { boQua: true, xoa() {} };
    const C = ctx(box, o);
    try { await fn(C) }
    catch (e) { if (e !== HUY) { C.xoa(); throw e } C.xoa(); return { huy: true, xoa() {} } }
    const xoa = () => C.xoa();
    if (o.donCuoi) xoa();
    return { xong: true, xoa }
  };
})();
