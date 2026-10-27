/* Màn 4 · Cửa hàng · "Polly tha nải chuối" (khoảng 9 giây)
   Xong trò xe đẩy: Polly cố tha cả một nải chuối to tới xe; nặng quá, vỗ cánh phành phạch, bay lên từng nấc
   (lên một chút lại tụt), tới trên xe thì thả "bịch" vào xe, đậu lên tay đẩy, nói "Big bananas! Big bananas!",
   rồi thở hổn hển, xong bay đi.
   CanhHai.man4(box, { xe: phần tử xe đẩy (bắt buộc),
                       xeTrong: {x, mieng, day, tayX, tayY} các tỉ lệ 0..1 trong khung xe (mặc định theo SHOPCART_SVG 120×90:
                                 lòng xe x .58, miệng y .25, đáy lòng y .64, tay đẩy (.1, .12)),
                       vaoTu, raTai, naiW (bề rộng nải chuối, % box; mặc định 1,35 × Polly),
                       moTrongXe (độ rõ phần nải chuối nằm dưới miệng xe, mặc định .4), …chung })
   Tiếng (am): 'vo-canh' "[phành phạch]", 'bich' "[bịch!]", 'big-bananas' "Big bananas! Big bananas!" (Polly; CHƯA CÓ BẢN GHI),
   'tho' "[hộc hộc]".
   Kết thúc: nải chuối NẰM LẠI trong xe (bản sao xe + hình nải chuối); Polly đã bay đi. r.xoa() trả lại như cũ. */
(function () {
  'use strict';
  const CH = window.CanhHai;

  CH.man4 = (box, o = {}) => CH.chay(box, o, async C => {
    if (!o.xe) throw new Error('man4: cần o.xe');
    const T = Object.assign({ x: .58, mieng: .25, day: .64, tayX: .1, tayY: .12 }, o.xeTrong || {});
    const xe = C.muon(o.xe, { z: 6 }); xe.firstElementChild.style.transformOrigin = '50% 100%';
    const hX = C.cao(xe), trai = xe.x - xe.w / 2;
    const longX = trai + T.x * xe.w, mieng = xe.b + (1 - T.mieng) * hX, day = xe.b + (1 - T.day) * hX;
    const tay = { x: trai + T.tayX * xe.w, b: xe.b + (1 - T.tayY) * hX };

    const W = 11, vao = o.vaoTu || { x: 116, b: 14 };
    const p = C.polly({ x: vao.x, b: vao.b, w: W, lat: true, tu: 'tha', voMs: 130 });
    // nải chuối treo dưới chân Polly (cuống ở chỗ chân quặp (100, 244) của khung Polly)
    const naiTi = (o.naiW || W * 1.35) / W;
    const nai = p.lop(`<div style="position:absolute;left:${50 - naiTi * 50}%;top:91.5%;width:${naiTi * 100}%">${CH.HINH['nai-chuoi-to']}</div>`, { theoBay: false });
    const hP = C.cao(p), hN = naiTi * W * (102 / 126) * (C.R().width / C.R().height);
    const duoiNai = () => p.b - (hN - (hP * .085));                 // đáy nải chuối (% box)
    const bTheo = dn => dn + (hN - hP * .085);                      // Polly ở đâu để đáy nải ở dn

    // 1. lết vào sát mặt đất, nặng trĩu, chập chờn
    C.am('vo-canh', '[phành phạch]', { x: 80, b: 40 });
    const xToi = longX + 20, b0 = bTheo(4);
    await C.di(p, [{ x: (vao.x + xToi) / 2, b: b0 + 3, o: .3 }, { x: (vao.x + xToi) / 2 - 6, b: b0, o: .55 }, { x: xToi + 4, b: b0 + 3, o: .8 }, { x: xToi, b: b0 }], 1500);
    // 2. bay lên từng nấc: lên một chút, tụt lại một ít
    const bDich = bTheo(mieng + 3), nac = 3, buoc = (bDich - b0) / nac;
    for (let i = 1; i <= nac; i++) {
      C.lam(p, [{ transform: 'rotate(0)' }, { transform: 'rotate(6deg)' }, { transform: 'rotate(-4deg)' }, { transform: 'rotate(0)' }], 400).catch(() => {});
      await C.di(p, { b: b0 + buoc * i + 3 }, 380, 'ease-out');
      await C.di(p, { b: b0 + buoc * i - (i < nac ? 1.5 : 0) }, 220, 'ease-in')
    }
    if (C.dead) return;
    // 3. kéo sang, tới ngay trên lòng xe
    await C.di(p, { x: longX }, 650);
    await C.cho(150);
    // 4. thả "bịch"
    const r = C.rect(nai.firstElementChild);
    nai.remove();
    const n = C.hinh('nai-chuoi-to', { x: r.x, b: r.b, w: r.w, z: 7 });
    p.tu('bay'); p.vo(300);
    C.di(p, { b: p.b + 9 }, 380, 'ease-out').catch(() => {});
    await C.di(n, { b: day }, 300, 'ease-in');
    C.am('bich', '[bịch!]', xe);
    // nằm trong lòng xe: phần dưới miệng xe mờ đi (như nhìn qua lưới xe), phần nhô lên trên miệng xe rõ.
    // (Không đặt nải chuối sau xe: viền sticker trắng của xe làm lòng xe đục, che mất nải chuối.)
    const cut = Math.max(0, Math.min(1, (mieng - day) / C.cao(n)));
    const tren = C.hinh('nai-chuoi-to', { x: n.x, b: n.b, w: n.w, z: 7 });
    tren.style.clipPath = `inset(-30% -30% ${cut * 100}% -30%)`;
    n.style.clipPath = `inset(${(1 - cut) * 100}% -30% -30% -30%)`; n.style.opacity = o.moTrongXe ?? .4;
    const nhun = [{ transform: 'scale(1)' }, { transform: 'scale(1.06,.9)' }, { transform: 'scale(1)' }];
    C.chay(n.firstElementChild, nhun, 300); C.chay(tren.firstElementChild, nhun, 300);
    await C.lam(xe, [{ transform: 'scale(1)' }, { transform: 'scale(1.05,.9)' }, { transform: 'scale(.98,1.03)' }, { transform: 'scale(1)' }], 380);
    // 5. đậu lên tay đẩy, nói "Big bananas! Big bananas!", rồi thở hổn hển
    C.quay(p, false);
    const dau = C.neo(p, 97, 241, tay.x, tay.b);
    await C.di(p, [{ x: (p.x + dau.x) / 2, b: Math.max(p.b, dau.b) + 6 }, { x: dau.x, b: dau.b + 2 }], 600);
    p.tu('noi'); C.dat(p, dau.x, dau.b);
    p.firstElementChild.style.transformOrigin = '50% 100%';
    C.am('big-bananas', 'Big bananas! Big bananas!', p, { loi: true, t: 1700 });
    await C.lam(p, [{ transform: 'rotate(0)' }, { transform: 'rotate(10deg)' }, { transform: 'rotate(0)' }, { transform: 'rotate(10deg)' }, { transform: 'rotate(0)' }], 1500);
    C.am('tho', '[hộc hộc]', p, { t: 1300 });
    for (let i = 0; i < 4; i++) {
      p.tu(i % 2 ? 'tho-2' : 'tho-1');
      await C.lam(p, [{ transform: 'scale(1)' }, { transform: i % 2 ? 'scale(.97,1.02)' : 'scale(1.04,.95)' }], 260, { giu: true })
    }
    p.firstElementChild.getAnimations().forEach(a => a.cancel());
    // 6. bay đi
    p.tu('bay');
    const ra = o.raTai || { x: -16, b: 92 };
    C.quay(p, ra.x < p.x);
    await C.di(p, ra, 900, 'ease-in');
    p.remove()
  });
})();
