/**
 * 研究所英文複習器：獨立版的 Google Drive 同步中繼站。
 *
 * 進度存成 Drive 裡的快照檔 grad-english-progress-<時間戳>.json，每次寫入就建一份新的、把舊的丟進垃圾桶。
 * Claude 版透過 Google Drive 連接器讀寫同樣的檔案，用同一套合併規則：
 * 同一張卡保留複習次數 (n) 多的那筆，每日作答量取較大值，作文紀錄依 id 聯集。
 *
 * 部署：用存放進度檔的那個 Google 帳號，部署為網頁應用程式，
 * 「執行身分：我」、「誰可以存取：任何人」。KEY 是通關碼，跟網址一起貼到獨立版的同步設定。
 */
const KEY = '__SYNC_KEY__';
const PREFIX = 'grad-english-progress-';
const NAME = /^grad-english-progress-(\d+)\.json$/;

function doGet(e) {
  if (e.parameter.key !== KEY) return out_({ ok: false, error: 'bad_key' });
  return out_({ ok: true, doc: latest_().doc });
}

// body: {key, doc} → merges doc into the latest snapshot, writes a new one if anything changed, returns the merged doc
function doPost(e) {
  let body;
  try { body = JSON.parse(e.postData.contents); } catch (err) { return out_({ ok: false, error: 'bad_json' }); }
  if (body.key !== KEY) return out_({ ok: false, error: 'bad_key' });
  const lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    const cur = latest_();
    const merged = JSON.parse(JSON.stringify(cur.doc));
    const changed = merge_(merged, body.doc || {});
    if (changed || !cur.files.length) write_(merged, cur.files);
    return out_({ ok: true, doc: merged, wrote: changed || !cur.files.length });
  } finally {
    lock.releaseLock();
  }
}

function latest_() {
  const it = DriveApp.searchFiles("title contains '" + PREFIX + "' and trashed = false");
  const files = [];
  while (it.hasNext()) {
    const f = it.next();
    const m = NAME.exec(f.getName());
    if (m) files.push({ file: f, ts: Number(m[1]) });
  }
  files.sort((a, b) => b.ts - a.ts);
  let doc = empty_();
  for (const f of files) {
    try { doc = JSON.parse(f.file.getBlob().getDataAsString('UTF-8')); break; } catch (err) { /* skip a damaged snapshot */ }
  }
  return { doc: doc, files: files.map(f => f.file) };
}

function write_(doc, olds) {
  doc.app = 'grad-english-review';
  doc.version = 1;
  doc.updatedAt = Date.now();
  DriveApp.createFile(PREFIX + doc.updatedAt + '.json', JSON.stringify(doc), 'application/json');
  olds.forEach(f => f.setTrashed(true));
}

function empty_() {
  return { app: 'grad-english-review', version: 1, srs: { cards: {}, log: {} }, essays: [] };
}

// Same rules as mergeProgress() in index.html. Mutates dst, returns true if dst changed.
function merge_(dst, src) {
  let changed = false;
  dst.srs = dst.srs || {};
  dst.srs.cards = dst.srs.cards || {};
  dst.srs.log = dst.srs.log || {};
  dst.essays = dst.essays || [];
  const cards = (src.srs && src.srs.cards) || {};
  Object.keys(cards).forEach(k => {
    const c = cards[k], d = dst.srs.cards[k];
    if (!d || (c.n || 0) > (d.n || 0) || ((c.n || 0) === (d.n || 0) && (c.due || 0) > (d.due || 0))) {
      if (JSON.stringify(c) !== JSON.stringify(d)) { dst.srs.cards[k] = c; changed = true; }
    }
  });
  const log = (src.srs && src.srs.log) || {};
  Object.keys(log).forEach(k => {
    if ((log[k] || 0) > (dst.srs.log[k] || 0)) { dst.srs.log[k] = log[k]; changed = true; }
  });
  const ids = {};
  dst.essays.forEach(x => { ids[x.id] = true; });
  (src.essays || []).forEach(x => {
    if (x && x.id && !ids[x.id]) { dst.essays.push(x); ids[x.id] = true; changed = true; }
  });
  return changed;
}

function out_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
