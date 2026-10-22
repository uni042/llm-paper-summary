const test = require('node:test');
const assert = require('node:assert/strict');
const { normalize, tokenize, filterAndRank, queryState, parsePayload, excerpt, highlightRanges } = require('../../web/paper-search/search.js');

test('normalizes fullwidth text and tokenizes quoted phrases as a single AND term', () => {
  assert.equal(normalize('ＫＶ ＣＡＣＨＥ'), 'kv cache');
  assert.deepEqual(tokenize('推論 "メモリ 帯域"'), ['推論', 'メモリ 帯域']);
});

test('filters only matching papers within fields and ranks attention first', () => {
  const papers = [
    { title: '注目論文', summary: 'KV cache', body: '', year: 2026, attention: true, citations: 1, implementation: null },
    { title: '別の論文', summary: 'KV cache', body: '日本語本文', year: 2025, attention: false, citations: 80, implementation: 'https://example.test' },
    { title: '不一致', summary: 'その他', body: '', year: 2026, attention: true, citations: 4, implementation: true },
  ];
  const ranked = filterAndRank(papers, { query: 'KV cache', field: 'summary' });
  assert.deepEqual(ranked.map((p) => p.title), ['注目論文', '別の論文']);
  assert.deepEqual(filterAndRank(papers, { query: '日本語本文', field: 'body' }).map((p) => p.title), ['別の論文']);
  assert.deepEqual(filterAndRank(papers, { query: 'KV cache', field: 'summary', year: '2025', implementation: true }).map((p) => p.title), ['別の論文']);
});

test('parses shareable URL state while rejecting unknown selectors', () => {
  assert.deepEqual(queryState('?q=hello&field=body&sort=newest&year=2026&attention=1'), {
    query: 'hello', field: 'body', year: '2026', sort: 'newest', attention: true, implementation: false,
  });
  assert.equal(queryState('?field=../../all&sort=remote').field, 'all');
});

test('searches a pre-normalized full text body without normalizing the corpus on each query', () => {
  const papers = [{ title: 'paper', summary: '', body: 'LLM CACHE', year: 2026, citations: 0 }];
  assert.equal(filterAndRank(papers, { query: 'ｌｌｍ cache', field: 'body', preNormalizedBody: true }).length, 1);
});

test('reads both raw and gzip payload bytes without double-decompressing', async () => {
  const zlib = require('node:zlib');
  const source = Buffer.from('{"scope":"all","papers":[]}');
  assert.deepEqual(await parsePayload(source), { scope: 'all', papers: [] });
  assert.deepEqual(await parsePayload(zlib.gzipSync(source)), { scope: 'all', papers: [] });
});

test('maps normalized matches back to original UTF-16 ranges for excerpts', () => {
  const halfWidth = `前${'x'.repeat(270)}ｶﾞ${'後'.repeat(270)}`;
  const halfWidthExcerpt = excerpt(halfWidth, 'ガ');
  assert.ok(halfWidthExcerpt.includes('ｶﾞ'));
  assert.ok(halfWidthExcerpt.length > 0);
  assert.equal(halfWidth.slice(...highlightRanges(halfWidth, 'ガ')[0]), 'ｶﾞ');

  const emojiText = `${'😀'.repeat(260)} query ${'後'.repeat(10)}`;
  const emojiExcerpt = excerpt(emojiText, 'query');
  assert.ok(emojiExcerpt.includes('query'));
  assert.ok(emojiExcerpt.includes('後'.repeat(10)));
  const emojiMatch = `${'😀'.repeat(260)}query`;
  assert.equal(emojiMatch.slice(...highlightRanges(emojiMatch, 'query')[0]), 'query');
  for (const character of emojiExcerpt) {
    const point = character.codePointAt(0);
    assert.ok(point < 0xd800 || point > 0xdfff, 'excerpt must not contain an unpaired surrogate');
  }

  const noMatch = excerpt('先頭'.repeat(200), '存在しない語');
  assert.ok(noMatch.startsWith('先頭'));
});

test('maps combining sequences and compatibility expansions to whole original graphemes', () => {
  assert.equal('e\u0301'.slice(...highlightRanges('e\u0301', 'é')[0]), 'e\u0301');
  assert.equal('ﬃ'.slice(...highlightRanges('ﬃ', 'fi')[0]), 'ﬃ');
});

test('completes initial UI render after reading scoped data', async () => {
  const searchUi = require('../../web/paper-search/search.js');
  class FakeElement {
    constructor(tag = 'div') { this.tagName = tag; this.children = []; this.listeners = {}; this.dataset = {}; this.value = ''; this.checked = false; this.hidden = false; this.textContent = ''; }
    appendChild(child) { this.children.push(child); return child; }
    replaceChildren(...children) { this.children = children; }
    addEventListener(type, callback) { this.listeners[type] = callback; }
  }
  const elements = new Map(['app', 'search-form', 'query', 'field', 'sort', 'year', 'attention', 'implementation', 'status', 'results', 'more'].map((id) => [id, new FakeElement(id)]));
  elements.get('app').dataset.scope = 'all';
  elements.get('field').value = 'all'; elements.get('sort').value = 'recommend';
  const original = { document: globalThis.document, location: globalThis.location, history: globalThis.history, fetch: globalThis.fetch };
  globalThis.document = { getElementById: (id) => elements.get(id), createElement: (tag) => new FakeElement(tag), createTextNode: (text) => Object.assign(new FakeElement('#text'), { textContent: text }) };
  globalThis.location = { search: '', pathname: '/' };
  globalThis.history = { replaceState() {} };
  globalThis.fetch = async () => ({ ok: true, arrayBuffer: async () => new TextEncoder().encode(JSON.stringify({ scope: 'all', body_normalization: 'NFKC', papers: [{ title: '論文', summary: '要約', summary_display: '短い要約', body: '本文', year: 2026, date: '2026-01', citations: 0, family: 'inference', lineage: 'example', attention: false, implementation: null, source_url: 'https://github.com/uni042/llm-paper-summary/blob/main/papers/inference/example/a.md' }] })).buffer });
  try {
    await searchUi.start();
    assert.match(elements.get('status').textContent, /1件中 1件/);
    assert.equal(elements.get('results').children.length, 1);
  } finally {
    globalThis.document = original.document; globalThis.location = original.location; globalThis.history = original.history; globalThis.fetch = original.fetch;
  }
});
