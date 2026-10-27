/* Màn 5 · Công trường · "Mái nhà biết đi" (khoảng 8 giây)
   Mở đầu, lúc mái nhà tam giác còn nằm dưới đất: Polly bay xuống, chui vào dưới mái; cái mái tự đi lạch bạch
   (lòi ra hai chân vẹt), đi qua rồi đi lại. Cả đội ngạc nhiên "Oh!". Mái nhấc lên một bên, Polly thò ra:
   "Triangle! Triangle!" rồi bay đi; mái hạ xuống lại đúng chỗ cũ (để trò cần cẩu đặt mái chạy như cũ).
   CanhHai.man5(box, { mai: phần tử mái nhà (bắt buộc, đang nằm dưới đất), ban: [phần tử Lam, Na, Ben…],
                       doiMat(el, 'surprised' | null): đổi mặt một bạn (app: setKidFace); mặc định đổi hình kit <ten>-ngac-nhien
                       nếu phần tử có data-kit="lam|na|ben", diXa (% box mái đi, mặc định 9), vaoTu, raTai, …chung })
   Tiếng (am): 'lach-bach' "[lạch bạch]" ×2, 'oh' "Oh!" (cả đội), 'triangle' "Triangle! Triangle!" (Polly), 'cop' "[cộp]".
   Kết thúc: mái về đúng chỗ cũ (bản gốc hiện lại), mặt các bạn trở lại như trước, Polly đã bay đi. Không để lại gì. */
(function () {
  'use strict';
  const CH = window.CanhHai;

  CH.man5 = (box, o = {}) => CH.chay(box, o, async C => {
    if (!o.mai) throw new Error('man5: cần o.mai');
    const m = C.muon(o.mai, { z: 8 }), mi = m.firstElementChild;
    const dat0 = { x: m.x, b: m.b }, hM = C.cao(m);
    const ban = o.ban || [];
    const doiMat = o.doiMat || ((el, f) => {
      const k = el.dataset.kit, sv = el.querySelector('.ch-kit') || el; if (!k) return;
      if (f) { if (sv._was == null) { sv._was = sv.innerHTML; C.back.push(() => { if (sv._was != null) { sv.innerHTML = sv._was; sv._was = null } }) } sv.innerHTML = CH.HINH[k + '-ngac-nhien'] }
      else if (sv._was != null) { sv.innerHTML = sv._was; sv._was = null }
    });

    // 1. Polly bay xuống, đáp bên phải cái mái
    const vao = o.vaoTu || { x: 114, b: 66 };
    const p = C.polly({ x: vao.x, b: vao.b, lat: true, tu: 'bay', z: 6 });
    const dat = C.neo(p, 97, 250, m.x + m.w / 2 + 6, m.b);
    await C.di(p, [{ x: (vao.x + dat.x) / 2 + 4, b: dat.b + 16 }, { x: dat.x, b: dat.b + 3 }], 1000);
    p.tu('dung'); C.dat(p, dat.x, dat.b);
    // nhìn cái mái, nghiêng đầu
    await C.lam(p, [{ transform: 'rotate(0)' }, { transform: 'rotate(-10deg)', offset: .3 }, { transform: 'rotate(-10deg)', offset: .7 }, { transform: 'rotate(0)' }], 700);
    // 2. nhảy lò cò tới mép mái rồi chui vào dưới
    const sat = m.x + m.w * .36;
    await C.di(p, [{ x: (p.x + sat) / 2, b: p.b + 4 }, { x: (p.x + sat) / 2 - 1, b: p.b }, { x: sat + 1, b: p.b + 3 }, { x: sat, b: p.b }], 520);
    await C.lam(p, [{ transform: 'translateX(0) scale(1)', opacity: 1 }, { transform: 'translateX(-70%) scale(.5,.3)', opacity: 0 }], 260, { giu: true, ez: 'ease-in' });
    p.style.visibility = 'hidden';
    C.lam(m, [{ transform: 'translateY(0)' }, { transform: 'translateY(-14%)' }, { transform: 'translateY(0)' }], 220).catch(() => {});
    await C.cho(350);
    // 3. mái nhấc lên, lòi hai chân vẹt, đi lạch bạch sang trái rồi quay lại
    const nhac = Math.max(3, hM * .22);
    await C.di(m, { b: dat0.b + nhac }, 220, 'ease-out');
    const chan = C.hinh('polly-chan-1', { w: p.w * 2.4, z: 7 });
    const datChan = () => { const n = C.neo(chan, 98, 252, m.x, dat0.b); C.dat(chan, n.x, n.b) };
    datChan();
    let k = 0; const buoc = setInterval(() => { k++; chan.querySelector('.ch-q').innerHTML = CH.HINH[k % 2 ? 'polly-chan-2' : 'polly-chan-1'] }, C.ms(170));
    C.timers.push(buoc); C.back.push(() => clearInterval(buoc));
    const xa = o.diXa ?? 9;
    const di = async (dx) => {
      C.am('lach-bach', '[lạch bạch]', { x: m.x, b: dat0.b + hM + 6 });
      const lac = C.lam(m, [{ transform: 'rotate(0) translateY(0)' }, { transform: 'rotate(-4deg) translateY(-6%)' }, { transform: 'rotate(0) translateY(0)' }, { transform: 'rotate(4deg) translateY(-6%)' }, { transform: 'rotate(0) translateY(0)' }], 560, { lap: 2 });
      const tg = m.x + dx, x0 = m.x, t0 = performance.now(), dur = C.ms(1120);
      const theo = () => { if (C.dead) return; const f = Math.min(1, (performance.now() - t0) / dur); C.dat(m, x0 + (tg - x0) * f, m.b); datChan(); if (f < 1) requestAnimationFrame(theo) };
      requestAnimationFrame(theo); await lac; C.dat(m, tg, m.b); datChan()
    };
    await di(-xa);
    // cả đội ngạc nhiên
    ban.forEach((el, i) => { doiMat(el, 'surprised'); C.chay(el, [{ transform: 'translateY(0)' }, { transform: 'translateY(-7%)' }, { transform: 'translateY(0)' }], 340, { tre: i * 70 }) });
    if (ban.length) C.am('oh', 'Oh!', ban[Math.floor((ban.length - 1) / 2)], { loi: true });
    await C.cho(120);
    await di(xa);
    clearInterval(buoc); chan.remove();
    // 4. mái nhấc một bên, Polly thò ra: "Triangle! Triangle!"
    mi.style.transformOrigin = '2% 100%';
    await C.lam(m, [{ transform: 'rotate(0)' }, { transform: 'rotate(-17deg)' }], 300, { giu: true, ez: 'ease-out' });
    p.firstElementChild.getAnimations().forEach(a => a.cancel());
    C.quay(p, false); p.tu('noi'); p.style.visibility = '';
    const ngoai = C.neo(p, 97, 250, m.x + m.w / 2 + 3, dat0.b), trong = { x: ngoai.x - 7, b: ngoai.b };
    C.dat(p, trong.x, trong.b);
    await C.di(p, ngoai, 260, 'cubic-bezier(.3,1.5,.5,1)');
    C.am('triangle', 'Triangle! Triangle!', p, { loi: true, t: 1600 });
    p.firstElementChild.style.transformOrigin = '50% 100%';
    await C.lam(p, [{ transform: 'rotate(0)' }, { transform: 'rotate(8deg)' }, { transform: 'rotate(0)' }, { transform: 'rotate(8deg)' }, { transform: 'rotate(0)' }], 1100);
    // 5. Polly bay đi, mái hạ xuống "cộp"
    p.tu('bay'); const ra = o.raTai || { x: 116, b: 92 };
    C.di(p, ra, 900, 'ease-in').then(() => p.remove(), () => {});
    await C.cho(250);
    mi.getAnimations().forEach(a => a.cancel());
    await C.lam(m, [{ transform: 'rotate(-17deg)' }, { transform: 'rotate(0)' }], 200, { ez: 'ease-in' });
    await C.di(m, { b: dat0.b }, 120, 'ease-in');
    C.am('cop', '[cộp]', m);
    C.hat(m.x - m.w * .45, dat0.b + 1, { n: 4, mau: '#D9C7A8', vien: '', co: 1.6, xa: 4 });
    C.hat(m.x + m.w * .45, dat0.b + 1, { n: 4, mau: '#D9C7A8', vien: '', co: 1.6, xa: 4 });
    await C.lam(m, [{ transform: 'scale(1)' }, { transform: 'scale(1.03,.92)' }, { transform: 'scale(1)' }], 220);
    await C.cho(600);
    ban.forEach(el => doiMat(el, null));
    m.tra();
    await C.cho(400)
  });
})();
