/* Màn 5 · Công trường · "Mái nhà biết đi" (khoảng 7 giây)
   Đầu trang, mái nhà tam giác nằm sẵn dưới đất; Polly đã trốn sẵn bên dưới (bé không thấy Polly chui vào).
   Cái mái tự nhấc lên, lòi ra hai chân vẹt, đi lạch bạch qua rồi đi lại. Cả đội mặt rất ngạc nhiên, mỗi bạn "Oh!".
   Mái nhấc lên một bên, lộ ra Polly: "Triangle! Triangle!", Polly bay đi, mái hạ xuống "cộp" đúng chỗ cũ.
   Sau đó app cho cần cẩu nhấc mái lên, trò cũ chạy tiếp.
   CanhHai.man5(box, { mai: phần tử mái nhà (bắt buộc, đang nằm dưới đất), ban: [phần tử Lam, Na, Ben…],
                       doiMat(el, 'surprised' | null): đổi mặt một bạn (app: setKidFace); mặc định đổi hình kit <ten>-ngac-nhien
                       nếu phần tử có data-kit="lam|na|ben", diXa (% box mái đi, mặc định 8), raTai, …chung })
   Tiếng (am): 'lach-bach' "[lạch bạch]" ×2, 'oh' "Oh!" mỗi bạn một lần (am nhận thêm tên bạn: 'Lam', 'Na', 'Ben';
   CHƯA CÓ BẢN GHI), 'triangle' "Triangle! Triangle!" (Polly; đã có bản ghi "Triangle!"), 'cop' "[cộp]".
   Kết thúc: mái về đúng chỗ cũ (bản gốc hiện lại), mặt các bạn trở lại như trước, Polly đã bay đi. Không để lại gì. */
(function () {
  'use strict';
  const CH = window.CanhHai;
  const TEN = { lam: 'Lam', na: 'Na', ben: 'Ben', choi: 'Chồi' };

  CH.man5 = (box, o = {}) => CH.chay(box, o, async C => {
    if (!o.mai) throw new Error('man5: cần o.mai');
    const m = C.muon(o.mai, { z: 8 }), mi = m.firstElementChild;
    const dat0 = { x: m.x, b: m.b }, hM = C.cao(m);
    const ban = o.ban || [];
    const tenOf = el => el.dataset.who || TEN[el.dataset.kit] || '';
    const doiMat = o.doiMat || ((el, f) => {
      const k = el.dataset.kit, sv = el.querySelector('.ch-kit') || el; if (!k) return;
      if (f) { if (sv._was == null) { sv._was = sv.innerHTML; C.back.push(() => { if (sv._was != null) { sv.innerHTML = sv._was; sv._was = null } }) } sv.innerHTML = CH.HINH[k + '-ngac-nhien'] }
      else if (sv._was != null) { sv.innerHTML = sv._was; sv._was = null }
    });
    // Polly trốn sẵn dưới mái: có mặt nhưng ẩn, đứng giữa mái
    const p = C.polly({ x: m.x, b: m.b, lat: false, tu: 'dung', z: 6 });
    p.style.visibility = 'hidden';

    await C.cho(400);
    // 1. cái mái nhúc nhích, rồi tự nhấc lên, lòi hai chân vẹt
    await C.lam(m, [{ transform: 'rotate(0)' }, { transform: 'rotate(-2deg)' }, { transform: 'rotate(2deg)' }, { transform: 'rotate(0)' }], 300);
    await C.cho(200);
    const nhac = Math.max(3, hM * .22);
    await C.di(m, { b: dat0.b + nhac }, 220, 'ease-out');
    const chan = C.hinh('polly-chan-1', { w: p.w * 2.4, z: 7 });
    const datChan = () => { const n = C.neo(chan, 98, 252, m.x, dat0.b); C.dat(chan, n.x, n.b) };
    datChan();
    C.chay(chan, [{ opacity: 0 }, { opacity: 1 }], 120);
    let k = 0; const buoc = setInterval(() => { k++; chan.querySelector('.ch-q').innerHTML = CH.HINH[k % 2 ? 'polly-chan-2' : 'polly-chan-1'] }, C.ms(170));
    C.timers.push(buoc); C.back.push(() => clearInterval(buoc));
    // 2. đi lạch bạch sang một bên rồi đi lại
    const xa = o.diXa ?? 8;
    const di = async (dx) => {
      C.am('lach-bach', '[lạch bạch]', { x: m.x, b: dat0.b + hM + 6 });
      const lac = C.lam(m, [{ transform: 'rotate(0) translateY(0)' }, { transform: 'rotate(-4deg) translateY(-6%)' }, { transform: 'rotate(0) translateY(0)' }, { transform: 'rotate(4deg) translateY(-6%)' }, { transform: 'rotate(0) translateY(0)' }], 560, { lap: 2 });
      const lacA = C.anims[C.anims.length - 1];   // bước đi theo thời gian của chính chuyển động lắc lư: app tạm dừng (Pause) thì mái cũng đứng yên
      const tg = m.x + dx, x0 = m.x, dur = C.ms(1120);
      const theo = () => { if (C.dead) return; const t = lacA && lacA.currentTime != null ? +lacA.currentTime : dur; const f = Math.min(1, t / dur); C.dat(m, x0 + (tg - x0) * f, m.b); datChan(); if (f < 1) requestAnimationFrame(theo) };
      requestAnimationFrame(theo); await lac; C.dat(m, tg, m.b); datChan()
    };
    const ve = ban.length && C.rect(ban[0]).x < m.x ? -1 : 1;     // đi về phía các bạn trước
    const diDau = di(ve * xa);
    // 3. cả đội mặt rất ngạc nhiên, mỗi bạn "Oh!"
    await C.cho(450);
    for (const el of ban) {
      doiMat(el, 'surprised');
      C.chay(el, [{ transform: 'translateY(0)' }, { transform: 'translateY(-8%)' }, { transform: 'translateY(0)' }], 340);
      C.am('oh', 'Oh!', el, { loi: true, ai: tenOf(el), t: 1100 });
      await C.cho(260)
    }
    await diDau;
    await di(-ve * xa);
    clearInterval(buoc);
    // 4. mái nhấc lên một bên, lộ ra Polly: "Triangle! Triangle!"
    mi.style.transformOrigin = '2% 100%';
    const mo = C.lam(m, [{ transform: 'rotate(0)' }, { transform: 'rotate(-20deg)' }], 320, { giu: true, ez: 'ease-out' });
    C.chay(chan, [{ opacity: 1 }, { opacity: 0 }], 150, { giu: true });
    C.dat(p, C.neo(p, 97, 250, m.x + m.w * .3, dat0.b).x, dat0.b);
    p.tu('noi'); p.style.visibility = '';
    C.chay(p, [{ opacity: 0 }, { opacity: 1 }], 150);
    await mo;
    const ngoai = C.neo(p, 97, 250, m.x + m.w / 2 + 3, dat0.b);
    await C.di(p, ngoai, 260, 'cubic-bezier(.3,1.5,.5,1)');
    chan.remove();
    C.am('triangle', 'Triangle! Triangle!', p, { loi: true, t: 1600 });
    p.firstElementChild.style.transformOrigin = '50% 100%';
    await C.lam(p, [{ transform: 'rotate(0)' }, { transform: 'rotate(8deg)' }, { transform: 'rotate(0)' }, { transform: 'rotate(8deg)' }, { transform: 'rotate(0)' }], 1100);
    // 5. Polly bay đi, mái hạ xuống "cộp"
    p.tu('bay'); const ra = o.raTai || { x: 116, b: 92 };
    C.di(p, ra, 900, 'ease-in').then(() => p.remove(), () => {});
    await C.cho(250);
    mi.getAnimations().forEach(a => a.cancel());
    await C.lam(m, [{ transform: 'rotate(-20deg)' }, { transform: 'rotate(0)' }], 200, { ez: 'ease-in' });
    await C.di(m, { b: dat0.b }, 120, 'ease-in');
    C.am('cop', '[cộp]', m);
    C.hat(m.x - m.w * .45, dat0.b + 1, { n: 4, mau: '#D9C7A8', vien: '', co: 1.6, xa: 4 });
    C.hat(m.x + m.w * .45, dat0.b + 1, { n: 4, mau: '#D9C7A8', vien: '', co: 1.6, xa: 4 });
    await C.lam(m, [{ transform: 'scale(1)' }, { transform: 'scale(1.03,.92)' }, { transform: 'scale(1)' }], 220);
    await C.cho(600);
    ban.forEach(el => doiMat(el, null));
    m.tra();
    await C.cho(300)
  });
})();
