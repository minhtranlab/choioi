/**
 * Chồi Ơi: Google Sheet backend (Google Apps Script web app)
 *
 * The Sheet gets these tabs (made by itself, or from the menu Chồi Ơi → Cài đặt / làm mới các bảng):
 *   Hướng dẫn     the admin guide (how to send the link, how parents register, how to read the tabs)
 *   Báo cáo       one row per child: level, days played, minutes in the last 7 days, % correct, skills to practise …
 *   Theo kỹ năng  one row per skill: how many children have it, are practising, have not started
 *   Accounts      one row per child: login, PIN hash, name, birth year, parent email, dates, and the full progress (JSON)
 *   Progress      one row per child and skill: status, tries, correct, last day, next review
 *
 * The app sends register / load / save (POST, text/plain JSON). The PIN itself never arrives, only its SHA-256 hash.
 * After 10 wrong PINs a login is locked for 15 minutes.
 */
const APP_URL = 'https://minhtranlab.github.io/choioi/';   // the link parents open (change it if the app lives elsewhere)
const ACC = 'Accounts', PROG = 'Progress', REP = 'Báo cáo', SKL = 'Theo kỹ năng', GUIDE = 'Hướng dẫn';
const ACC_H = ['login', 'pin_hash', 'child_name', 'birth_year', 'email', 'created', 'updated', 'lesson', 'level_name', 'pieces', 'levels_done', 'last_played', 'days_played', 'min_7d', 'review_due', 'fun_mix', 'fails', 'fail_time',
  'state_1', 'state_2', 'state_3', 'state_4', 'state_5', 'state_6', 'state_7', 'state_8'];
const PROG_H = ['login', 'child_name', 'skill_id', 'skill', 'status', 'tries', 'correct', 'last_day', 'next_review', 'updated'];
const COL = n => ACC_H.indexOf(n) + 1, CHUNK = 45000, NCHUNK = 8;
const STATUS_VI = { got_it: 'Đã vững', practising: 'Đang luyện', not_yet: 'Chưa học', spoken: 'Đã nói theo', assigned: 'Đã giao (ở nhà)' };

/* ---------------- web app ---------------- */
function doGet() { return out({ ok: true, app: 'choi-oi' }); }
function doPost(e) {
  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000);
    const d = JSON.parse(e.postData.contents);
    const res = handle(d);
    if (res.ok && (d.action === 'save' || d.action === 'register')) { try { updateReport(); } catch (x) {} }
    return out(res);
  } catch (err) {
    return out({ ok: false, error: String(err && err.message || err) });
  } finally { try { lock.releaseLock(); } catch (x) {} }
}
function out(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

function sheet(name, head) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let s = ss.getSheetByName(name);
  if (!s) { s = ss.insertSheet(name); if (head) { s.appendRow(head); s.setFrozenRows(1); s.getRange(1, 1, 1, head.length).setFontWeight('bold'); } }
  return s;
}
function findRow(s, login) {
  const n = s.getLastRow() - 1; if (n < 1) return 0;
  const v = s.getRange(2, 1, n, 1).getValues();
  for (let i = 0; i < v.length; i++) if (String(v[i][0]).toLowerCase() === login) return i + 2;
  return 0;
}
function chunks(str) { if (str.length > CHUNK * NCHUNK) throw new Error('toolarge'); const a = []; for (let i = 0; i < NCHUNK; i++) a.push(str.slice(i * CHUNK, (i + 1) * CHUNK)); return a; }
function metaRow(m) { return [m.lesson || 0, m.level || '', m.pieces || 0, m.done || 0, m.last || '', m.days || 0, m.min7 || 0, m.due || 0, m.mix || 0]; }

function handle(d) {
  const login = String(d.login || '').trim().toLowerCase();
  if (!/^[a-z0-9._-]{3,20}$/.test(login)) return { ok: false, error: 'login' };
  const s = sheet(ACC, ACC_H), now = new Date(), row = findRow(s, login);

  if (d.action === 'register') {
    if (row) return { ok: false, error: 'taken' };
    const st = JSON.stringify(d.state || {});
    s.appendRow([login, d.h, d.child || '', d.birthYear || '', d.email || '', now, now].concat(metaRow(d.meta || {}), [0, ''], chunks(st)));
    writeProgress(login, d.child || '', d.summary || []);
    return { ok: true };
  }
  if (!row) return { ok: false, error: 'nouser' };
  const v = s.getRange(row, 1, 1, ACC_H.length).getValues()[0];
  // too many wrong PINs: wait 15 minutes
  const fails = +v[COL('fails') - 1] || 0, ft = v[COL('fail_time') - 1];
  if (fails >= 10 && ft && now - new Date(ft) < 15 * 60 * 1000) return { ok: false, error: 'locked' };
  if (String(v[COL('pin_hash') - 1]) !== String(d.h)) {
    s.getRange(row, COL('fails'), 1, 2).setValues([[fails >= 10 ? 1 : fails + 1, now]]);
    return { ok: false, error: 'pin' };
  }
  if (fails) s.getRange(row, COL('fails'), 1, 2).setValues([[0, '']]);

  if (d.action === 'load') {
    const st = v.slice(COL('state_1') - 1, COL('state_1') - 1 + NCHUNK).join('');
    let state = null; try { state = st ? JSON.parse(st) : null; } catch (x) { state = null; }
    return { ok: true, state: state, child: v[COL('child_name') - 1], birthYear: v[COL('birth_year') - 1], email: v[COL('email') - 1] };
  }
  if (d.action === 'save') {
    const st = JSON.stringify(d.state || {}), child = (d.state && d.state.child && d.state.child.name) || v[COL('child_name') - 1];
    s.getRange(row, COL('child_name')).setValue(child);
    s.getRange(row, COL('updated'), 1, 10).setValues([[now].concat(metaRow(d.meta || {}))]);
    s.getRange(row, COL('state_1'), 1, NCHUNK).setValues([chunks(st)]);
    if (d.summary) writeProgress(login, child, d.summary);
    return { ok: true };
  }
  return { ok: false, error: 'action' };
}

/* the Progress tab: this child's rows are replaced, everyone else's stay */
function writeProgress(login, child, summary) {
  const p = sheet(PROG, PROG_H), n = p.getLastRow() - 1, now = new Date();
  const keep = n > 0 ? p.getRange(2, 1, n, PROG_H.length).getValues().filter(r => String(r[0]).toLowerCase() !== login) : [];
  const mine = summary.map(x => [login, child, x.id, x.name, x.status, x.tries, x.correct, x.last, x.review, now]);
  const all = keep.concat(mine);
  if (n > 0) p.getRange(2, 1, n, PROG_H.length).clearContent();
  if (all.length) p.getRange(2, 1, all.length, PROG_H.length).setValues(all);
}

/* ---------------- the report tabs (rebuilt after every save, or from the menu) ---------------- */
const REP_H = ['Tên bé', 'Tên đăng nhập', 'Năm sinh', 'Email ba mẹ', 'Ngày đăng ký', 'Chơi gần nhất', 'Số ngày đã chơi', 'Phút chơi 7 ngày qua', 'Đang học', 'Số màn đã xong (/8)', 'Mảnh bản đồ (/8)',
  'Kỹ năng đã vững', 'Đang luyện', 'Chưa học', 'Tỉ lệ đúng', 'Nên ôn thêm', 'Kỹ năng đến hạn ôn', 'Lần chơi Fun Mix'];
function updateReport() {
  const ss = SpreadsheetApp.getActiveSpreadsheet(), acc = sheet(ACC, ACC_H), prog = sheet(PROG, PROG_H);
  const na = acc.getLastRow() - 1, np = prog.getLastRow() - 1;
  const A = na > 0 ? acc.getRange(2, 1, na, COL('fail_time')).getValues() : [], P = np > 0 ? prog.getRange(2, 1, np, PROG_H.length).getValues() : [];
  const byLogin = {}; P.forEach(r => { (byLogin[String(r[0]).toLowerCase()] = byLogin[String(r[0]).toLowerCase()] || []).push(r); });
  const today = new Date(), wk = new Date(today.getTime() - 7 * 864e5), fmt = d => d ? Utilities.formatDate(new Date(d), ss.getSpreadsheetTimeZone(), 'yyyy-MM-dd') : '';
  const rows = A.map(a => {
    const L = String(a[0]).toLowerCase(), sk = byLogin[L] || [], st = x => sk.filter(r => r[4] === x).length;
    const tries = sk.reduce((t, r) => t + (+r[5] || 0), 0), ok = sk.reduce((t, r) => t + (+r[6] || 0), 0);
    const weak = sk.filter(r => +r[5] >= 2).map(r => ({ n: r[3], acc: (+r[6] || 0) / (+r[5] || 1) })).filter(x => x.acc < .75).sort((x, y) => x.acc - y.acc).slice(0, 3).map(x => x.n + ' (' + Math.round(x.acc * 100) + '%)').join('; ');
    return [a[COL('child_name') - 1], L, a[COL('birth_year') - 1], a[COL('email') - 1], fmt(a[COL('created') - 1]), a[COL('last_played') - 1], a[COL('days_played') - 1], a[COL('min_7d') - 1], a[COL('level_name') - 1],
      a[COL('levels_done') - 1], a[COL('pieces') - 1], st('got_it'), st('practising'), st('not_yet'), tries ? Math.round(ok / tries * 100) + '%' : '', weak, a[COL('review_due') - 1], a[COL('fun_mix') - 1]];
  }).sort((x, y) => String(y[5]).localeCompare(String(x[5])));
  // the summary at the top
  const active = rows.filter(r => r[5] && new Date(r[5]) >= wk).length, avgDone = rows.length ? (rows.reduce((t, r) => t + (+r[9] || 0), 0) / rows.length).toFixed(1) : '0';
  const allT = P.reduce((t, r) => t + (+r[5] || 0), 0), allOk = P.reduce((t, r) => t + (+r[6] || 0), 0);
  const r = sheet(REP); r.clear();
  r.getRange(1, 1, 1, 2).setValues([['BÁO CÁO CHỒI ƠI', 'Cập nhật: ' + Utilities.formatDate(today, ss.getSpreadsheetTimeZone(), 'yyyy-MM-dd HH:mm')]]).setFontWeight('bold');
  r.getRange(2, 1, 4, 2).setValues([['Số bé đã đăng ký', rows.length], ['Bé chơi trong 7 ngày qua', active], ['Trung bình số màn đã xong (/8)', avgDone], ['Tỉ lệ đúng chung', allT ? Math.round(allOk / allT * 100) + '%' : '']]);
  r.getRange(7, 1, 1, REP_H.length).setValues([REP_H]).setFontWeight('bold').setBackground('#FFE9A8');
  if (rows.length) r.getRange(8, 1, rows.length, REP_H.length).setValues(rows);
  r.setFrozenRows(7);
  // per skill: how many children have it
  const sm = {}; P.forEach(p => { const k = p[2]; const o = sm[k] = sm[k] || { id: k, name: p[3], got_it: 0, practising: 0, not_yet: 0, other: 0, t: 0, ok: 0 }; if (o[p[4]] != null) o[p[4]]++; else o.other++; o.t += +p[5] || 0; o.ok += +p[6] || 0; });
  const S = sheet(SKL); S.clear();
  const SH = ['Mã kỹ năng', 'Kỹ năng', 'Số bé đã vững', 'Đang luyện', 'Chưa học', 'Khác (nói theo / ở nhà)', 'Tổng lượt', 'Tỉ lệ đúng'];
  S.getRange(1, 1, 1, SH.length).setValues([SH]).setFontWeight('bold').setBackground('#C9F2D9'); S.setFrozenRows(1);
  const srows = Object.keys(sm).sort().map(k => { const o = sm[k]; return [o.id, o.name, o.got_it, o.practising, o.not_yet, o.other, o.t, o.t ? Math.round(o.ok / o.t * 100) + '%' : '']; });
  if (srows.length) S.getRange(2, 1, srows.length, SH.length).setValues(srows);
}

/* ---------------- the menu in the Sheet ---------------- */
function onOpen() {
  SpreadsheetApp.getUi().createMenu('Chồi Ơi')
    .addItem('Cài đặt / làm mới các bảng', 'setupSheets')
    .addItem('Cập nhật báo cáo', 'updateReport')
    .addItem('Đặt lại mã PIN cho một bé', 'resetPin')
    .addToUi();
}
function setupSheets() { sheet(ACC, ACC_H); sheet(PROG, PROG_H); writeGuide(); updateReport();
  const ss = SpreadsheetApp.getActiveSpreadsheet(); [GUIDE, REP, SKL, ACC, PROG].forEach((n, i) => { const s = ss.getSheetByName(n); if (s) { ss.setActiveSheet(s); ss.moveActiveSheet(i + 1); } }); ss.setActiveSheet(ss.getSheetByName(GUIDE)); }
function sha256hex(str) { return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, str, Utilities.Charset.UTF_8).map(b => ('0' + (b & 255).toString(16)).slice(-2)).join(''); }
function resetPin() {
  const ui = SpreadsheetApp.getUi();
  const a = ui.prompt('Đặt lại mã PIN', 'Tên đăng nhập của bé:', ui.ButtonSet.OK_CANCEL); if (a.getSelectedButton() !== ui.Button.OK) return;
  const login = a.getResponseText().trim().toLowerCase(); const s = sheet(ACC, ACC_H), row = findRow(s, login);
  if (!row) { ui.alert('Không tìm thấy tên đăng nhập "' + login + '".'); return; }
  const b = ui.prompt('Đặt lại mã PIN', 'Mã PIN mới (4 chữ số) cho "' + login + '":', ui.ButtonSet.OK_CANCEL); if (b.getSelectedButton() !== ui.Button.OK) return;
  const pin = b.getResponseText().trim(); if (!/^\d{4}$/.test(pin)) { ui.alert('Mã PIN phải gồm đúng 4 chữ số.'); return; }
  s.getRange(row, COL('pin_hash')).setValue(sha256hex('choi-oi:' + login + ':' + pin)); s.getRange(row, COL('fails'), 1, 2).setValues([[0, '']]);
  ui.alert('Đã đổi mã PIN của "' + login + '". Gửi PIN mới cho phụ huynh. Trên máy đang đăng nhập, phụ huynh đăng xuất rồi đăng nhập lại bằng PIN mới.');
}

/* ---------------- the guide tab ---------------- */
function writeGuide() {
  const g = sheet(GUIDE); g.clear();
  const L = [
    ['HƯỚNG DẪN CHO ADMIN · CHỒI ƠI', ''],
    ['', ''],
    ['1. Link gửi phụ huynh', APP_URL],
    ['', 'Phụ huynh mở link trên iPad / điện thoại. Trên iPad: nút Chia sẻ → "Thêm vào MH chính" để mở như một app.'],
    ['', ''],
    ['2. Đăng ký', 'Phụ huynh TỰ đăng ký ngay trong app (admin không phải làm gì): Đăng ký → tên bé, năm sinh, tên đăng nhập, mã PIN 4 số, email.'],
    ['', 'Admin muốn tạo hộ: mở link, đăng ký bằng thông tin của bé, vào Settings → Đăng xuất, rồi gửi tên đăng nhập + PIN cho phụ huynh.'],
    ['', 'Chơi thử: không cần tài khoản, chỉ lưu trên máy đó; sau này vào Settings → "Tạo tài khoản để lưu tiến độ" thì tiến độ được giữ.'],
    ['', 'Máy khác (hoặc cài lại): mở link → Đăng nhập → tên đăng nhập + PIN → tiến độ tự tải về.'],
    ['', ''],
    ['3. Tin nhắn mẫu gửi phụ huynh', 'Chào anh/chị, Fun Academy gửi app "Chồi Ơi" để bé lớp Chồi chơi và học ở nhà (Toán, Khám phá thế giới, Tiếng Anh).'],
    ['', '1) Mở link: ' + APP_URL + ' (trên iPad: Chia sẻ → Thêm vào MH chính).'],
    ['', '2) Chọn "Đăng ký", điền tên bé, năm sinh, tên đăng nhập (chữ thường không dấu, ví dụ bin2021), mã PIN 4 số và email.'],
    ['', '3) Ghi nhớ tên đăng nhập và PIN để mở trên máy khác. Mỗi ngày bé chơi khoảng 10–15 phút là đủ.'],
    ['', 'Trang ba mẹ: nhấn giữ nút Progress hoặc Settings 1 giây. Cần hỗ trợ, anh/chị nhắn lại cho Fun Academy nhé.'],
    ['', ''],
    ['4. Các bảng', ''],
    ['Báo cáo', 'Mỗi bé một dòng: đang học màn nào, số màn đã xong, số ngày đã chơi, phút chơi 7 ngày qua, tỉ lệ đúng, kỹ năng nên ôn thêm (dưới 75%), số kỹ năng đến hạn ôn. Phía trên có số liệu chung.'],
    ['Theo kỹ năng', 'Mỗi kỹ năng một dòng: bao nhiêu bé đã vững / đang luyện / chưa học, tỉ lệ đúng chung. Dùng để biết phần nào các bé hay vấp.'],
    ['Accounts', 'Dữ liệu tài khoản (đừng sửa tay cột pin_hash và state_1 … state_8). Muốn xoá một bé: xoá cả dòng ở đây và các dòng của bé ở Progress.'],
    ['Progress', 'Chi tiết từng bé × từng kỹ năng. Trạng thái: got_it = đã vững, practising = đang luyện, not_yet = chưa học, spoken = đã nói theo, assigned = đã giao làm ở nhà.'],
    ['', 'Báo cáo tự cập nhật mỗi khi một bé chơi xong. Muốn làm mới ngay: menu Chồi Ơi → Cập nhật báo cáo.'],
    ['', ''],
    ['5. Quên mã PIN', 'Menu Chồi Ơi → Đặt lại mã PIN cho một bé → nhập tên đăng nhập và PIN mới → gửi PIN mới cho phụ huynh. Admin không xem được PIN cũ (chỉ lưu mã băm).'],
    ['', 'Sai PIN 10 lần thì tài khoản bị khoá 15 phút; đặt lại PIN cũng mở khoá ngay.'],
    ['', ''],
    ['6. Khi sửa mã Apps Script', 'Triển khai → Quản lý các bản triển khai → bút chì (Chỉnh sửa) → Phiên bản: "Phiên bản mới" → Triển khai. Làm như vậy địa chỉ /exec giữ nguyên.'],
    ['', 'Đừng bấm "Tùy chọn triển khai mới" (sẽ ra địa chỉ khác, app cũ không gửi được nữa).'],
    ['', ''],
    ['7. Lưu ý', 'Không chia sẻ Google Sheet này cho phụ huynh (có email của mọi người). Phụ huynh chỉ cần link app.'],
    ['', 'Tiến độ luôn lưu trên máy của bé trước, rồi mới gửi lên Sheet vài giây sau; mất mạng thì app vẫn chơi được và gửi lại sau.'],
    ['', 'Mã nguồn và hướng dẫn đầy đủ: github.com/minhtranlab/choioi (file ADMIN.md).']];
  g.getRange(1, 1, L.length, 2).setValues(L);
  g.getRange(1, 1).setFontWeight('bold').setFontSize(14);
  g.getRange(1, 1, L.length, 1).setFontWeight('bold');
  g.setColumnWidth(1, 210); g.setColumnWidth(2, 900); g.getRange(1, 2, L.length, 1).setWrap(true);
}
