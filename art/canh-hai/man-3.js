/* Màn 3 · Nhà Na · "Mèo con đội trống" (khoảng 6,5 giây)
   Xong trò bắt đồ chơi rơi: mèo con trên kệ nhìn cái rổ, lấy đà, nhảy vèo vào rổ, rổ lắc lục cục, trong rổ kêu "tùng",
   rồi mèo nhảy HẲN ra khỏi rổ, đáp xuống sàn cạnh rổ, đầu đội cái trống úp ngược (như cái xô), đứng nghiêng đầu cho bé nhìn rõ.
   CanhHai.man3(box, { meo: phần tử mèo (bắt buộc), ro: phần tử rổ (bắt buộc),
                       mu: svg làm mũ (mặc định cái trống của app ART.drum, bỏ dùi, úp ngược),
                       raDat: {x, b} chỗ mèo đáp (mặc định ngay cạnh rổ, phía giữa phòng), toRa: mèo to lên khi ra trước (1,35),
                       vanhRo: 0..1 (miệng rổ cách đỉnh rổ bao nhiêu phần chiều cao, mặc định .4 = ART.basket),
                       dauMeo: 0..1 (đỉnh đầu mèo, tính từ trên, mặc định .18 = CAT_SVG), …chung })
   Tiếng (am): 'meo' "[meo!]" ×2, 'bich' "[bịch]" ×2, 'luc-cuc' "[lục cục]", 'tung' "[tùng!]" (trống).
   Kết thúc: mèo đội trống ĐỨNG LẠI trên sàn cạnh rổ (bản sao mèo; mèo gốc đang ẩn; rổ đã trả lại). r.xoa() trả lại như cũ. */
(function () {
  'use strict';
  const CH = window.CanhHai;
  const INK = '#361D46', OL = `stroke="${INK}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"`;
  // cái trống của app (ART.drum) bỏ dùi, úp ngược: mặt trống ở dưới (đội lên đầu), thân đỏ ở trên
  const TRONG = `<svg viewBox="14 24 72 62" overflow="visible"><g transform="translate(0 110) scale(1 -1)"><path d="M18 40 V74 C18 82 82 82 82 74 V40" fill="#E8607E" ${OL}/><ellipse cx="50" cy="40" rx="32" ry="10" fill="#FFF3D6" ${OL}/><path d="M18 52 L34 76 L50 52 L66 76 L82 52" fill="none" stroke="#FCB515" stroke-width="3"/></g></svg>`;

  CH.man3 = (box, o = {}) => CH.chay(box, o, async C => {
    if (!o.meo || !o.ro) throw new Error('man3: cần o.meo và o.ro');
    const vanh = o.vanhRo ?? .4, dau = o.dauMeo ?? .18;
    const roSau = C.muon(o.ro, { z: 5 });                        // rổ (phía sau)
    const roTruoc = C.muon(o.ro, { z: 8 });                      // thân rổ phía trước: che phần mèo nằm trong rổ
    roTruoc.querySelector('.ch-q').style.clipPath = `inset(${vanh * 100}% 0 0 0)`;
    const m = C.muon(o.meo, { z: 6 });
    const mi = m.firstElementChild; mi.style.transformOrigin = '50% 100%';
    const hR = C.cao(roSau), hM = C.cao(m), mieng = roSau.b + hR * (1 - vanh);
    const veTrai = roSau.x < m.x;                                  // mèo nhảy sang trái?

    // 1. nhìn cái rổ, lấy đà
    await C.lam(m, [{ transform: 'rotate(0)' }, { transform: `rotate(${veTrai ? -14 : 14}deg)` }, { transform: 'rotate(0)' }], 600);
    await C.lam(m, [{ transform: 'scaleY(1)' }, { transform: 'scale(1.08,.8)' }], 260, { giu: true });
    // 2. nhảy vèo vào rổ
    C.am('meo', '[meo!]', m);
    const tren = { x: roSau.x, b: mieng + 4 }, dinh = { x: (m.x + roSau.x) / 2, b: Math.max(m.b, mieng) + 18 };
    mi.getAnimations().forEach(a => a.cancel());
    C.chay(mi, [{ transform: 'scale(.9,1.12) rotate(0)' }, { transform: `scale(1) rotate(${veTrai ? -20 : 20}deg)`, offset: .5 }, { transform: 'scale(1) rotate(0)' }], 760);
    await C.di(m, [{ x: dinh.x, b: dinh.b, o: .45 }, tren], 760, 'cubic-bezier(.3,.1,.5,1)');
    await C.di(m, { b: Math.max(roSau.b + 1, mieng - hM * .95) }, 220, 'ease-in');
    C.am('bich', '[bịch]', roSau);
    const nhun = [{ transform: 'scale(1,1)' }, { transform: 'scale(1.1,.86)' }, { transform: 'scale(.97,1.04)' }, { transform: 'scale(1)' }];
    C.chay(roSau.firstElementChild, nhun, 380); await C.lam(roTruoc, nhun, 380);
    // 3. rổ lắc lục cục, trong rổ kêu "tùng" (mèo vừa đội cái trống)
    C.am('luc-cuc', '[lục cục]', roSau);
    const lac = [{ transform: 'rotate(0)' }, { transform: 'rotate(-6deg)' }, { transform: 'rotate(5deg)' }, { transform: 'rotate(-4deg)' }, { transform: 'rotate(0)' }];
    for (const r of [roSau, roTruoc]) r.firstElementChild.style.transformOrigin = '50% 100%';
    C.chay(roSau.firstElementChild, lac, 800); await C.lam(roTruoc, lac, 800);
    C.am('tung', '[tùng!]', { x: roSau.x, b: mieng + 8 });
    C.chay(roSau.firstElementChild, nhun, 300); await C.lam(roTruoc, nhun, 300);
    await C.cho(150);
    // 4. nhảy hẳn ra khỏi rổ, đầu đội cái trống úp ngược
    const mu = document.createElement('div');
    mu.style.cssText = `position:absolute;left:10%;bottom:${(1 - dau) * 100 - 12}%;width:80%;transform:rotate(-6deg);transform-origin:50% 100%`;
    mu.innerHTML = o.mu || TRONG; m.querySelector('.ch-q').append(mu);
    m.style.zIndex = 9;                                            // ra trước thân rổ
    const sangPhai = o.raDat ? o.raDat.x > roSau.x : roSau.x <= 50;
    const dat = o.raDat || { x: roSau.x + (sangPhai ? 1 : -1) * (roSau.w / 2 + m.w * .9), b: roSau.b };
    C.am('meo', '[meo!]', { x: roSau.x, b: mieng + hM + 6 });
    m.style.transformOrigin = '50% 100%';                         // ra phía trước, to hơn một chút cho bé nhìn rõ
    C.chay(m, [{ scale: '1' }, { scale: String(o.toRa ?? 1.35) }], 780, { giu: true });
    C.chay(mi, [{ transform: 'rotate(0)' }, { transform: `rotate(${sangPhai ? 14 : -14}deg)`, offset: .5 }, { transform: 'rotate(0)' }], 780);
    await C.di(m, [{ x: roSau.x, b: mieng + hM * .2, o: .2 }, { x: (roSau.x + dat.x) / 2, b: mieng + hM * .9, o: .55 }, dat], 780, 'cubic-bezier(.3,.1,.5,1)');
    m.style.scale = String(o.toRa ?? 1.35);
    C.am('bich', '[bịch]', { x: dat.x, b: dat.b + hM * 1.6 });
    await C.lam(m, [{ transform: 'scale(1)' }, { transform: 'scale(1.12,.84)' }, { transform: 'scale(.96,1.06)' }, { transform: 'scale(1)' }], 320);
    roTruoc.tra(); roSau.tra();                                    // rổ xong việc: trả lại rổ gốc (đúng thứ tự ngược lúc mượn)
    // 5. đứng cho bé nhìn rõ: nghiêng đầu, cái trống lắc lư
    C.chay(mu, [{ transform: 'rotate(-6deg)' }, { transform: 'rotate(6deg)' }, { transform: 'rotate(-6deg)' }], 700, { lap: 2 });
    await C.lam(m, [{ transform: 'rotate(0)' }, { transform: 'rotate(-10deg)', offset: .25 }, { transform: 'rotate(-10deg)', offset: .45 }, { transform: 'rotate(9deg)', offset: .7 }, { transform: 'rotate(0)' }], 1300);
    await C.cho(500)
  });
})();
