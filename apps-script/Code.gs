/**
 * Chồi Ơi: Google Sheet backend (Google Apps Script web app)
 *
 * Sheets it makes by itself:
 *   Accounts  one row per child: login, PIN hash, child's name, birth year, parent email, dates, level, and the
 *             full progress (JSON, split over the state_1 … state_8 cells)
 *   Progress  one row per child and skill: status (not_yet / practising / got_it …), tries, correct, last day, next review
 *
 * The app sends: register, load, save (POST, text/plain JSON). The PIN itself never arrives here, only its hash.
 * After 10 wrong PINs a login is locked for 15 minutes.
 */
const ACC = 'Accounts', PROG = 'Progress';
const ACC_H = ['login', 'pin_hash', 'child_name', 'birth_year', 'email', 'created', 'updated', 'lesson', 'pieces', 'levels_done', 'last_played', 'fails', 'fail_time',
  'state_1', 'state_2', 'state_3', 'state_4', 'state_5', 'state_6', 'state_7', 'state_8'];
const PROG_H = ['login', 'child_name', 'skill_id', 'skill', 'status', 'tries', 'correct', 'last_day', 'next_review', 'updated'];
const COL = n => ACC_H.indexOf(n) + 1, CHUNK = 45000, NCHUNK = 8;

function doGet() { return out({ ok: true, app: 'choi-oi' }); }
function doPost(e) {
  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000);
    const d = JSON.parse(e.postData.contents);
    return out(handle(d));
  } catch (err) {
    return out({ ok: false, error: String(err && err.message || err) });
  } finally { try { lock.releaseLock(); } catch (x) {} }
}
function out(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

function sheet(name, head) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let s = ss.getSheetByName(name);
  if (!s) { s = ss.insertSheet(name); s.appendRow(head); s.setFrozenRows(1); s.getRange(1, 1, 1, head.length).setFontWeight('bold'); }
  return s;
}
function findRow(s, login) {
  const n = s.getLastRow() - 1; if (n < 1) return 0;
  const v = s.getRange(2, 1, n, 1).getValues();
  for (let i = 0; i < v.length; i++) if (String(v[i][0]).toLowerCase() === login) return i + 2;
  return 0;
}
function chunks(str) { const a = []; for (let i = 0; i < NCHUNK; i++) a.push(str.slice(i * CHUNK, (i + 1) * CHUNK)); if (str.length > CHUNK * NCHUNK) throw new Error('toolarge'); return a; }

function handle(d) {
  const login = String(d.login || '').trim().toLowerCase();
  if (!/^[a-z0-9._-]{3,20}$/.test(login)) return { ok: false, error: 'login' };
  const s = sheet(ACC, ACC_H), now = new Date(), row = findRow(s, login);

  if (d.action === 'register') {
    if (row) return { ok: false, error: 'taken' };
    const st = JSON.stringify(d.state || {}), m = d.meta || {};
    s.appendRow([login, d.h, d.child || '', d.birthYear || '', d.email || '', now, now, m.lesson || 0, m.pieces || 0, m.done || 0, m.last || '', 0, ''].concat(chunks(st)));
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
    const st = JSON.stringify(d.state || {}), m = d.meta || {}, child = (d.state && d.state.child && d.state.child.name) || v[COL('child_name') - 1];
    s.getRange(row, COL('child_name')).setValue(child);
    s.getRange(row, COL('updated'), 1, 5).setValues([[now, m.lesson || 0, m.pieces || 0, m.done || 0, m.last || '']]);
    s.getRange(row, COL('state_1'), 1, NCHUNK).setValues([chunks(st)]);
    if (d.summary) writeProgress(login, child, d.summary);
    return { ok: true };
  }
  return { ok: false, error: 'action' };
}

/* the Progress sheet: this child's rows are replaced, everyone else's stay */
function writeProgress(login, child, summary) {
  const p = sheet(PROG, PROG_H), n = p.getLastRow() - 1, now = new Date();
  const keep = n > 0 ? p.getRange(2, 1, n, PROG_H.length).getValues().filter(r => String(r[0]).toLowerCase() !== login) : [];
  const mine = summary.map(x => [login, child, x.id, x.name, x.status, x.tries, x.correct, x.last, x.review, now]);
  const all = keep.concat(mine);
  if (n > 0) p.getRange(2, 1, n, PROG_H.length).clearContent();
  if (all.length) p.getRange(2, 1, all.length, PROG_H.length).setValues(all);
}
