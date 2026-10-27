/* Màn 6 · Một ngày · "Mũ vỏ chuối" (khoảng 7 giây)
   Bữa sáng ba-na-na: Na ăn chuối xong, Polly bay xuống nhặt vỏ chuối, đội lên đầu làm mũ: "Ba-na-na!" (nhún ba cái
   theo ba tiếng), rồi bay tới thùng rác trong bếp, nắp mở "cạch", thả vỏ vào, nắp đóng "cạch", bay đi.
   CanhHai.man6(box, { vo: {x, b, w} chỗ vỏ chuối nằm (mặc định trên quầy, chỗ đĩa chuối của app: x 30, b 46, w 7),
                       thung: phần tử thùng rác có <g class="nap"> (art/kit/do-vat/thung-rac) | {x, b, w} để cảnh tự vẽ,
                       na: phần tử Na (nhún theo), vaoTu, raTai, …chung })
   Tiếng (am): 'banana' "Ba-na-na!" (Polly; câu đã có bản ghi), 'cach' "[cạch]" ×2.
   Kết thúc: vỏ chuối đã vào thùng, Polly bay đi; thùng rác (nếu cảnh tự vẽ) VẪN Ở LẠI. r.xoa() gỡ. */
(function () {
  'use strict';
  const CH = window.CanhHai;

  CH.man6 = (box, o = {}) => CH.chay(box, o, async C => {
    const vq = o.vo || { x: 30, b: 46, w: 7 };
    const v = C.hinh('vo-chuoi', { x: vq.x, b: vq.b, w: vq.w, z: 6 });
    C.chay(v, [{ opacity: 0 }, { opacity: 1 }], 250);
    let t;
    if (o.thung && o.thung.nodeType) t = C.muon(o.thung, { z: 6 });
    else { const q = o.thung || { x: 88, b: 3, w: 9 }; t = C.hinh('thung-rac', { x: q.x, b: q.b, w: q.w, z: 6 }) }
    const nap = t.querySelector('g.nap'); if (nap) { nap.style.transformBox = 'view-box'; nap.style.transformOrigin = '6px 22px' }
    const hT = C.cao(t);

    // 1. Polly bay xuống, đáp cạnh vỏ chuối
    const vao = o.vaoTu || { x: 112, b: 88 };
    const p = C.polly({ x: vao.x, b: vao.b, lat: true, tu: 'bay' });
    const dat = C.neo(p, 97, 250, v.x + v.w * .5 + 5, v.b);
    await C.di(p, [{ x: (vao.x + dat.x) / 2, b: dat.b + 20 }, { x: dat.x, b: dat.b + 3 }], 1000);
    p.tu('dung'); C.dat(p, dat.x, dat.b);
    p.firstElementChild.style.transformOrigin = '50% 100%';
    await C.lam(p, [{ transform: 'rotate(0)' }, { transform: 'rotate(-16deg)', offset: .4 }, { transform: 'rotate(-16deg)', offset: .7 }, { transform: 'rotate(0)' }], 650);
    // 2. hất vỏ chuối lên, rơi đúng lên đầu thành cái mũ
    const dau = C.diem(p, 104, 34);
    const hv = C.cao(v);
    await C.di(v, [{ x: (v.x + dau.x) / 2, b: dau.b + hv * 1.4, o: .55 }, { x: dau.x, b: dau.b - hv * .25 }], 520, 'ease-out');
    v.remove();
    const mu = p.lop(`<div style="position:absolute;left:28%;top:-5%;width:48%;transform:rotate(-8deg)">${CH.HINH['vo-chuoi']}</div>`);
    C.chay(mu, [{ transform: 'translateY(-4%)' }, { transform: 'translateY(1%)' }, { transform: 'translateY(0)' }], 220);
    await C.cho(200);
    // 3. "Ba-na-na!" nhún ba cái
    p.tu('noi'); C.am('banana', 'Ba-na-na!', p, { loi: true, t: 1500 });
    if (o.na) C.chay(o.na, [{ transform: 'translateY(0)' }, { transform: 'translateY(-6%)' }, { transform: 'translateY(0)' }], 300, { lap: 3, tre: 60 });
    for (let i = 0; i < 3; i++) await C.lam(p, [{ transform: 'translateY(0) scale(1)' }, { transform: 'translateY(-12%) scale(.96,1.05)' }, { transform: 'translateY(0) scale(1.05,.94)', offset: .85 }, { transform: 'translateY(0) scale(1)' }], 320);
    await C.cho(150);
    // 4. bay tới thùng rác, nắp mở, thả vỏ vào, nắp đóng
    p.tu('bay'); C.quay(p, t.x < p.x);
    const tren = { x: t.x, b: t.b + hT + 4 };
    await C.di(p, [{ x: (p.x + tren.x) / 2, b: Math.max(p.b, tren.b) + 12 }, tren], 950);
    if (nap) await C.an(nap, [{ transform: 'rotate(0)' }, { transform: 'rotate(-80deg)' }], 220, { giu: true, ez: 'ease-out' });
    C.am('cach', '[cạch]', t);
    await C.cho(150);
    const r = C.rect(mu.firstElementChild); mu.remove();
    const roi = C.hinh('vo-chuoi', { x: r.x, b: r.b, w: r.w, z: 5 });
    C.chay(roi.firstElementChild, [{ transform: 'rotate(-8deg)' }, { transform: 'rotate(20deg)' }], 320, { giu: true });
    C.di(p, { b: p.b + 5 }, 300, 'ease-out').catch(() => {});
    await C.di(roi, { x: t.x, b: t.b + hT * .25 }, 320, 'ease-in');
    roi.remove();
    await C.cho(120);
    if (nap) await C.an(nap, [{ transform: 'rotate(-80deg)' }, { transform: 'rotate(0)' }], 170, { giu: true, ez: 'ease-in' });
    C.am('cach', '[cạch]', t);
    C.lam(t, [{ transform: 'scale(1)' }, { transform: 'scale(1.04,.95)' }, { transform: 'scale(1)' }], 200).catch(() => {});
    // 5. bay đi
    const ra = o.raTai || { x: 116, b: 96 };
    C.quay(p, ra.x < p.x);
    await C.di(p, ra, 900, 'ease-in');
    p.remove();
    if (t.tra) t.tra()
  });
})();
