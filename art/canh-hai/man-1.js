/* Màn 1 · Công viên · "Bong bóng vỡ trên mỏ" (khoảng 6,5 giây)
   Xong trò bong bóng có mặt: Polly bay ra mổ vỡ vài quả còn sót; quả cuối (to nhất) vỡ "bụp" ngay trên mỏ,
   bọt trắng dính đầy, Polly đứng hình, lắc đầu cho văng bọt, rồi bay đi.
   CanhHai.man1(box, { bongBong:[{x,b,w}…] (3 quả, quả cuối là quả to), bongBongSVG, vaoTu:{x,b}, raTai:{x,b}, …chung })
   Tiếng (am): 'bup' ×2 "[bụp]", 'bup-to' "[BỤP!]", 'lac' "[phì phì]".
   Kết thúc: không để lại gì (bong bóng vỡ hết, Polly bay khỏi khung). */
(function () {
  'use strict';
  const CH = window.CanhHai;
  const BONG = '<svg viewBox="0 0 40 40" overflow="visible"><circle cx="20" cy="20" r="18" fill="#DDF3FF" fill-opacity=".6" stroke="#3A1B49" stroke-width="2"/><path d="M9 15 q3 -7 11 -8" stroke="#fff" stroke-width="3.2" fill="none" stroke-linecap="round"/><circle cx="28" cy="28" r="2.6" fill="#fff" opacity=".85"/></svg>';

  CH.man1 = (box, o = {}) => CH.chay(box, o, async C => {
    const ds = o.bongBong || [{ x: 72, b: 46, w: 8 }, { x: 50, b: 56, w: 7 }, { x: 30, b: 42, w: 13 }];
    const bs = ds.map(q => {
      const s = C.hinh(o.bongBongSVG || BONG, { x: q.x, b: q.b, w: q.w, z: 5 });
      C.chay(s, [{ opacity: 0 }, { opacity: 1 }], 300);
      C.chay(s.firstElementChild, [{ transform: 'translateY(0)' }, { transform: 'translateY(-8%)' }], 900, { lap: Infinity, dir: 'alternate' });
      return s
    });
    const tam = s => ({ x: s.x, b: s.b + C.cao(s) / 2 });
    const vao = o.vaoTu || { x: 114, b: 70 };
    const p = C.polly({ x: vao.x, b: vao.b, lat: true, tu: 'bay' });

    // Polly bay tới, đầu mỏ chạm mép phải quả bóng
    const toi = async (s, t, sat = .42) => { const c = tam(s), d = C.neo(p, 162, 108, c.x + s.w * sat, c.b); await C.di(p, d, t) };
    const vo = s => {
      const c = tam(s); s.firstElementChild.getAnimations().forEach(a => a.cancel());
      C.chay(s, [{ transform: 'scale(1)', opacity: 1 }, { transform: 'scale(1.4)', opacity: 0 }], 160, { giu: true, ez: 'ease-out' });
      C.hat(c.x, c.b, { n: 8, mau: '#DDF3FF', co: 1.2 + s.w / 10, xa: s.w * .9, t: 450 });
      setTimeout(() => s.remove(), C.ms(200))
    };
    const mo = () => C.lam(p, [{ transform: 'none' }, { transform: 'translateX(-14%) rotate(-14deg)', offset: .5 }, { transform: 'none' }], 280);

    await C.cho(250);
    for (let i = 0; i < bs.length - 1; i++) {
      await toi(bs[i], i ? 700 : 950);
      const m = mo(); await C.cho(140); vo(bs[i]); C.am('bup', '[bụp]', tam(bs[i])); await m; await C.cho(120)
    }
    // quả cuối: to, vỡ ngay trên mỏ
    const big = bs[bs.length - 1];
    await toi(big, 800, .2);
    await C.cho(180);
    const m = mo(); await C.cho(140);
    vo(big); C.am('bup-to', '[BỤP!]', { x: big.x, b: tam(big).b + C.cao(big) * .7 }, { t: 1500 });
    const bot = p.lop(`<div style="position:absolute;inset:0;transform:scale(1.25);transform-origin:76% 45%">${CH.HINH['bot-mo-polly']}</div>`);
    C.chay(bot, [{ opacity: 0, transform: 'scale(.4)', transformOrigin: '80% 45%' }, { opacity: 1, transform: 'scale(1.1)', transformOrigin: '80% 45%', offset: .6 }, { opacity: 1, transform: 'scale(1)', transformOrigin: '80% 45%' }], 260);
    await m;
    // đứng hình: thôi vỗ cánh, tụt xuống một chút
    p.tu('dung'); await C.di(p, { b: p.b - 3 }, 380, 'ease-in'); await C.cho(260);
    p.tu('bay');
    // lắc đầu, bọt văng ra
    C.am('lac', '[phì phì]', p, { t: 1100 });
    const sh = C.lam(p, [{ transform: 'rotate(0)' }, { transform: 'rotate(14deg)' }, { transform: 'rotate(-14deg)' }, { transform: 'rotate(12deg)' }, { transform: 'rotate(-10deg)' }, { transform: 'rotate(0)' }], 850);
    await C.cho(200); let mm = C.mo(p); C.hat(mm.x, mm.b, { n: 6, co: 1.4, xa: 6 });
    await C.cho(380); mm = C.mo(p); C.hat(mm.x, mm.b, { n: 6, co: 1.2, xa: 6 });
    await sh;
    // bay đi (bọt vẫn còn dính trên mỏ)
    const ra = o.raTai || { x: -16, b: 96 };
    await C.di(p, ra, 1100, 'ease-in');
    p.remove()
  });
})();
