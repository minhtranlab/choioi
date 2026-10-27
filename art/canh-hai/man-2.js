/* Màn 2 · Vườn đêm · "Polly tập ngủ như dơi" (khoảng 8,5 giây)
   Xong trò đèn pin: Polly bay tới đậu trên cành cạnh con dơi đang ngủ treo ngược, thử treo ngược như dơi,
   chóng mặt (sao quay quanh đầu), lật lại đứng thẳng, ngáp "Tired! Tired!", rồi rúc đầu vào cánh ngủ kiểu vẹt.
   CanhHai.man2(box, { canh: {x,b,w} | phần tử cành (khung kit 200×40), doi: phần tử dơi (nếu cảnh đã có),
                       doiTai: 0..1 (chỗ dơi treo dọc cành, mặc định .58), dauTai: 0..1 (chỗ Polly đậu, .84), doiW, vaoTu, …chung })
   Không có cành / dơi thì cảnh tự vẽ (art/kit/do-vat/canh-cay, con-vat/doi-ngu-treo-nguoc).
   Tiếng (am): 'vut' "[vụt]" ×2, 'tired' "Tired! Tired!" (Polly; câu "Tired!" đã có bản ghi), 'ngu' "[khò… khò…]".
   Kết thúc: cành, dơi và Polly đang ngủ VẪN Ở LẠI (trang sau thay cả khung thì tự mất; muốn gỡ ngay: r.xoa()). */
(function () {
  'use strict';
  const CH = window.CanhHai;
  CH.css('ch-man2', `
.ch-sao{position:absolute;z-index:9;pointer-events:none;translate:-50% 50%;width:9%;aspect-ratio:1}
.ch-sao>i{position:absolute;inset:0;animation:chSaoQuay var(--t,900ms) linear infinite}
.ch-sao>i::before{content:'';position:absolute;left:42%;top:-8%;width:22%;aspect-ratio:1;background:#FFD21F;clip-path:polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%)}
@keyframes chSaoQuay{to{transform:rotate(360deg)}}
.ch-z{position:absolute;z-index:9;pointer-events:none;font:900 clamp(10px,5cqh,22px)/1 Nunito,system-ui,sans-serif;color:#C9B4F0;-webkit-text-stroke:1px #3A1B49}
`);

  CH.man2 = (box, o = {}) => CH.chay(box, o, async C => {
    // cành: tự vẽ hoặc đo phần tử có sẵn (coi như khung kit 200×40: mặt trên y 14, mặt dưới y 24)
    let cs;
    if (o.canh && o.canh.nodeType) { const r = C.rect(o.canh); cs = { x: r.x, b: r.b, w: r.w, W: 200, H: 40, lat: false } }
    else { const q = o.canh || { x: 60, b: 58, w: 40 }; cs = C.hinh('canh-cay', { x: q.x, b: q.b, w: q.w, z: 5 }) }
    const treo = C.diem(cs, 200 * (o.doiTai ?? .58), 23);
    if (!o.doi) { const d = C.hinh('doi-ngu-treo-nguoc', { w: o.doiW || 6, z: 5 }); const n = C.neo(d, 50, 5, treo.x, treo.b); C.dat(d, n.x, n.b);
      d.firstElementChild.style.transformOrigin = '50% 3%'; C.chay(d.firstElementChild, [{ transform: 'rotate(-3deg)' }, { transform: 'rotate(3deg)' }], 1400, { lap: Infinity, dir: 'alternate' }) }

    const vao = o.vaoTu || { x: 114, b: 82 };
    const p = C.polly({ x: vao.x, b: vao.b, lat: true, tu: 'bay' });
    const tren = C.diem(cs, 200 * (o.dauTai ?? .84), 14), duoi = C.diem(cs, 200 * (o.dauTai ?? .84), 23);
    const inn = p.firstElementChild;

    // 1. bay tới, đậu trên cành cạnh dơi
    const dau = C.neo(p, 97, 241, tren.x, tren.b);
    await C.di(p, [{ x: (vao.x + dau.x) / 2, b: dau.b + 14 }, { x: dau.x, b: dau.b + 3 }], 1200);
    p.tu('dung'); C.dat(p, dau.x, dau.b);
    await C.lam(p, [{ transform: 'scaleY(1)' }, { transform: 'scaleY(.9)' }, { transform: 'scaleY(1)' }], 220);
    // 2. nhìn con dơi, nghiêng đầu
    inn.style.transformOrigin = '50% 100%';
    await C.lam(p, [{ transform: 'rotate(0)' }, { transform: 'rotate(-12deg)', offset: .3 }, { transform: 'rotate(-12deg)', offset: .7 }, { transform: 'rotate(0)' }], 900);
    // 3. lật xuống treo ngược như dơi
    C.am('vut', '[vụt]', p);
    await C.lam(p, [{ transform: 'scaleY(1)' }, { transform: 'scaleY(.05)' }], 150, { giu: true, ez: 'ease-in' });
    p.tu('treo-nguoc'); const ng = C.neo(p, 97, 20, duoi.x, duoi.b); C.dat(p, ng.x, ng.b);
    inn.getAnimations().forEach(a => a.cancel()); inn.style.transformOrigin = '50% 4%';
    await C.lam(p, [{ transform: 'scaleY(.05)' }, { transform: 'scaleY(1.06)' }, { transform: 'scaleY(1)' }], 260, { ez: 'ease-out' });
    // đung đưa, chóng mặt: sao quay quanh đầu (đầu đang ở dưới)
    const sao = document.createElement('div'); sao.className = 'ch-sao'; sao.innerHTML = '<i></i><i style="animation-delay:-300ms"></i><i style="animation-delay:-600ms"></i>';
    sao.style.setProperty('--t', C.ms(900) + 'ms'); box.append(sao); C.els.push(sao);
    const datSao = () => { const h = C.diem(p, 104, p._tu === 'treo-nguoc' ? 170 : 92); sao.style.left = h.x + '%'; sao.style.bottom = h.b + '%' };
    datSao(); C.chay(sao, [{ opacity: 0 }, { opacity: 1 }], 300);
    await C.lam(p, [{ transform: 'rotate(0)' }, { transform: 'rotate(12deg)' }, { transform: 'rotate(-12deg)' }, { transform: 'rotate(9deg)' }, { transform: 'rotate(-6deg)' }, { transform: 'rotate(0)' }], 1500);
    // 4. lật lại đứng thẳng, loạng choạng
    C.am('vut', '[vụt]', p);
    await C.lam(p, [{ transform: 'scaleY(1)' }, { transform: 'scaleY(.05)' }], 150, { giu: true, ez: 'ease-in' });
    p.tu('dung'); C.dat(p, dau.x, dau.b); datSao();
    inn.getAnimations().forEach(a => a.cancel()); inn.style.transformOrigin = '50% 96%';
    await C.lam(p, [{ transform: 'scaleY(.05)' }, { transform: 'scaleY(1)' }], 200, { ez: 'ease-out' });
    await C.lam(p, [{ transform: 'rotate(0)' }, { transform: 'rotate(-13deg)' }, { transform: 'rotate(11deg)' }, { transform: 'rotate(-7deg)' }, { transform: 'rotate(4deg)' }, { transform: 'rotate(0)' }], 1000);
    C.an(sao, [{ opacity: 1 }, { opacity: 0 }], 400, { giu: true }).catch(() => {});
    // 5. ngáp "Tired! Tired!"
    p.tu('noi'); C.am('tired', 'Tired! Tired!', p, { loi: true, t: 1400 });
    await C.lam(p, [{ transform: 'scale(1)' }, { transform: 'scale(1.05,.96)', offset: .5 }, { transform: 'scale(1)' }], 900);
    // 6. rúc đầu vào cánh ngủ (vẹt ngủ đứng, không treo ngược)
    p.tu('ngu');
    await C.lam(p, [{ transform: 'scaleY(1)' }, { transform: 'scaleY(.93)' }, { transform: 'scaleY(.97)' }], 500, { giu: true });
    C.am('ngu', '[khò… khò…]', p, { t: 1600 });
    const head = C.diem(p, 120, 70);
    for (let i = 0; i < 3; i++) {
      const z = document.createElement('b'); z.className = 'ch-z'; z.textContent = 'z'; z.style.left = head.x + '%'; z.style.bottom = head.b + '%';
      box.append(z); C.els.push(z);
      C.chay(z, [{ opacity: 0, transform: 'translate(0,0) scale(.6)' }, { opacity: 1, offset: .25 }, { opacity: 0, transform: 'translate(120%,-180%) scale(1.2)' }], 1300, { tre: i * 420, giu: true })
    }
    await C.cho(1900)
  });
})();
