/* Màn 3 · Nhà Na · "Mèo con đội mũ đồ chơi" (khoảng 6 giây)
   Xong trò bắt đồ chơi rơi: mèo con trên kệ nhìn cái rổ, lấy đà, nhảy vèo vào rổ, rổ lắc lục cục,
   rồi mèo thò đầu ra, đội một món đồ chơi vừa rơi (vịt cao su) làm mũ, nghiêng đầu.
   CanhHai.man3(box, { meo: phần tử mèo (bắt buộc), ro: phần tử rổ (bắt buộc), mu: svg đồ chơi làm mũ (mặc định vịt của app),
                       vanhRo: 0..1 (miệng rổ cách đỉnh rổ bao nhiêu phần chiều cao, mặc định .4 = ART.basket),
                       dauMeo: 0..1 (đỉnh đầu mèo, tính từ trên, mặc định .18 = CAT_SVG), …chung })
   Tiếng (am): 'meo' "[meo!]", 'bich' "[bịch]", 'luc-cuc' "[lục cục]", 'chit' "[chít!]" (vịt cao su).
   Kết thúc: mèo đội mũ VẪN THÒ ĐẦU trong rổ (bản sao của mèo và rổ; mèo, rổ gốc đang ẩn). r.xoa() trả lại như cũ. */
(function () {
  'use strict';
  const CH = window.CanhHai;
  const INK = '#361D46', OL = `stroke="${INK}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"`;
  const VIT = `<svg viewBox="0 0 64 64"><path d="M10 38 C10 52 24 58 36 56 C50 54 56 44 54 36 C46 40 40 38 36 32 L24 34 C18 32 12 32 10 38Z" fill="#FCB515" ${OL}/><circle cx="40" cy="22" r="11" fill="#FCB515" ${OL}/><path d="M50 22 l10 3 -10 3z" fill="#F28C38" ${OL}/><circle cx="43" cy="19" r="2.2" fill="${INK}"/></svg>`;

  CH.man3 = (box, o = {}) => CH.chay(box, o, async C => {
    if (!o.meo || !o.ro) throw new Error('man3: cần o.meo và o.ro');
    const vanh = o.vanhRo ?? .4, dau = o.dauMeo ?? .18;
    const roSau = C.muon(o.ro, { z: 5 });                        // rổ (phía sau)
    const roTruoc = C.muon(o.ro, { z: 8 });                      // thân rổ phía trước: che phần mèo nằm trong rổ
    roTruoc.querySelector('.ch-q').style.clipPath = `inset(${vanh * 100}% 0 0 0)`;
    const m = C.muon(o.meo, { z: 6 });
    const mi = m.firstElementChild; mi.style.transformOrigin = '50% 100%';
    const hR = C.cao(roSau), hM = C.cao(m), mieng = roSau.b + hR * (1 - vanh);

    // 1. nhìn cái rổ, lấy đà
    await C.lam(m, [{ transform: 'rotate(0)' }, { transform: `rotate(${roSau.x < m.x ? -14 : 14}deg)` }, { transform: 'rotate(0)' }], 600);
    await C.lam(m, [{ transform: 'scaleY(1)' }, { transform: 'scale(1.08,.8)' }], 260, { giu: true });
    // 2. nhảy vèo vào rổ
    C.am('meo', '[meo!]', m);
    const tren = { x: roSau.x, b: mieng + 4 }, dinh = { x: (m.x + roSau.x) / 2, b: Math.max(m.b, mieng) + 18 };
    mi.getAnimations().forEach(a => a.cancel());
    C.chay(mi, [{ transform: 'scale(.9,1.12) rotate(0)' }, { transform: `scale(1) rotate(${roSau.x < m.x ? -20 : 20}deg)`, offset: .5 }, { transform: 'scale(1) rotate(0)' }], 760);
    await C.di(m, [{ x: dinh.x, b: dinh.b, o: .45 }, tren], 760, 'cubic-bezier(.3,.1,.5,1)');
    const day = Math.max(roSau.b + 1, mieng - hM * .95);
    await C.di(m, { b: day }, 220, 'ease-in');
    C.am('bich', '[bịch]', roSau);
    const nhun = [{ transform: 'scale(1,1)' }, { transform: 'scale(1.1,.86)' }, { transform: 'scale(.97,1.04)' }, { transform: 'scale(1)' }];
    C.chay(roSau.firstElementChild, nhun, 380); await C.lam(roTruoc, nhun, 380);
    // 3. rổ lắc lục cục (mèo đang lục bên trong)
    C.am('luc-cuc', '[lục cục]', roSau);
    const lac = [{ transform: 'rotate(0)' }, { transform: 'rotate(-6deg)' }, { transform: 'rotate(5deg)' }, { transform: 'rotate(-4deg)' }, { transform: 'rotate(0)' }];
    for (const r of [roSau, roTruoc]) r.firstElementChild.style.transformOrigin = '50% 100%';
    C.chay(roSau.firstElementChild, lac, 800); await C.lam(roTruoc, lac, 800);
    await C.cho(250);
    // 4. thò đầu ra, đội món đồ chơi làm mũ
    const mu = document.createElement('div');
    mu.style.cssText = `position:absolute;left:4%;bottom:${(1 - dau) * 100 - 8}%;width:92%;transform:rotate(-12deg);transform-origin:50% 100%`;
    mu.innerHTML = o.mu || VIT; m.querySelector('.ch-q').append(mu);
    C.am('chit', '[chít!]', { x: roSau.x, b: mieng + hM * .8 + 6 });
    await C.di(m, { b: mieng - hM * .4 }, 340, 'cubic-bezier(.3,1.6,.5,1)');
    await C.lam(m, [{ transform: 'rotate(0)' }, { transform: 'rotate(-12deg)' }, { transform: 'rotate(-12deg)', offset: .4 }, { transform: 'rotate(10deg)', offset: .7 }, { transform: 'rotate(0)' }], 1300);
    C.chay(mu, [{ transform: 'rotate(-12deg)' }, { transform: 'rotate(-4deg)' }, { transform: 'rotate(-12deg)' }], 600, { lap: 2 });
    await C.cho(600)
  });
})();
