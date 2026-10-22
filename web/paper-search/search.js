(function (root) {
  "use strict";
  const LABELS = { title: "タイトル", summary: "概要", body: "本文" };

  function normalize(value) {
    return String(value || "").normalize("NFKC").toLocaleLowerCase("ja");
  }

  function tokenize(query) {
    const parts = String(query || "").replace(/[「」]/g, '"').replace(/[“”]/g, '"').match(/"([^"]+)"|([^\s]+)/g) || [];
    return parts.map((part) => normalize(part.replace(/^"|"$/g, "").trim())).filter(Boolean);
  }

  function hasLiteral(text, term) {
    const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    return new RegExp(escaped, "iu").test(String(text || ""));
  }

  function filterAndRank(papers, options) {
    const opts = Object.assign({ query: "", field: "all", year: "", attention: false, implementation: false, sort: "recommend" }, options || {});
    const tokens = tokenize(opts.query);
    const fields = opts.field === "all" ? ["title", "summary", "body"] : [opts.field];
    const matching = [];
    for (const paper of papers || []) {
      if (opts.year && String(paper.year || "") !== String(opts.year)) continue;
      if (opts.attention && !paper.attention) continue;
      if (opts.implementation && !paper.implementation) continue;
      const haystacks = Object.fromEntries(fields.map((field) => [field, field === "body" && opts.preNormalizedBody ? String(paper[field] || "") : normalize(paper[field])]));
      const has = (field, token) => field === "body" && opts.preNormalizedBody ? hasLiteral(haystacks[field], token) : haystacks[field].includes(token);
      if (!tokens.every((token) => fields.some((field) => has(field, token)))) continue;
      const matchedFields = tokens.length ? fields.filter((field) => tokens.some((token) => has(field, token))) : [];
      let score = 0;
      for (const token of tokens) for (const field of fields) {
        if (field === "body" && opts.preNormalizedBody) {
          const escaped = token.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
          const found = haystacks[field].match(new RegExp(escaped, "giu"));
          score += found ? found.length : 0;
        } else {
          let at = 0;
          while ((at = haystacks[field].indexOf(token, at)) >= 0) { score += 1; at += Math.max(1, token.length); }
        }
      }
      matching.push(Object.assign({}, paper, { matchedFields, score }));
    }
    matching.sort((a, b) => {
      if (opts.sort === "citations") return (b.citations || 0) - (a.citations || 0) || (b.year || 0) - (a.year || 0) || String(b.date).localeCompare(String(a.date)) || a.title.localeCompare(b.title, "ja");
      if (opts.sort === "newest") return (b.year || 0) - (a.year || 0) || String(b.date).localeCompare(String(a.date)) || (b.citations || 0) - (a.citations || 0) || a.title.localeCompare(b.title, "ja");
      return Number(b.attention) - Number(a.attention) || (b.citations || 0) - (a.citations || 0) || b.score - a.score || (b.year || 0) - (a.year || 0) || String(b.date).localeCompare(String(a.date)) || a.title.localeCompare(b.title, "ja");
    });
    return matching;
  }

  function queryState(search) {
    const params = new URLSearchParams(search || "");
    return { query: params.get("q") || "", field: ["all", "title", "summary", "body"].includes(params.get("field")) ? params.get("field") : "all", year: params.get("year") || "", sort: ["recommend", "citations", "newest"].includes(params.get("sort")) ? params.get("sort") : "recommend", attention: params.get("attention") === "1", implementation: params.get("implementation") === "1" };
  }

  function mappedNormalization(value) {
    const text = String(value || "");
    const segments = [];
    if (typeof Intl !== "undefined" && Intl.Segmenter) {
      for (const part of new Intl.Segmenter("ja", { granularity: "grapheme" }).segment(text)) segments.push({ text: part.segment, start: part.index });
    } else {
      // Keep combining marks and half-width voiced marks with their base even on older browsers.
      let offset = 0;
      for (const point of Array.from(text)) {
        if (segments.length && (/\p{M}/u.test(point) || point === "ﾞ" || point === "ﾟ")) segments[segments.length - 1].text += point;
        else segments.push({ text: point, start: offset });
        offset += point.length;
      }
    }
    const normalized = [], starts = [], ends = [];
    for (const segment of segments) {
      const part = normalize(segment.text);
      normalized.push(part);
      for (let i = 0; i < part.length; i++) {
        starts.push(segment.start);
        ends.push(segment.start + segment.text.length);
      }
    }
    return { text: normalized.join(""), starts, ends, source: text, segments };
  }

  function highlightRanges(text, query) {
    const mapped = mappedNormalization(text);
    const spans = [];
    for (const term of tokenize(query).sort((a, b) => b.length - a.length)) {
      let from = 0, at;
      while ((at = mapped.text.indexOf(term, from)) >= 0) {
        const start = mapped.starts[at], end = mapped.ends[at + term.length - 1];
        if (start !== undefined && end !== undefined) spans.push([start, end]);
        from = at + Math.max(1, term.length);
      }
    }
    spans.sort((a, b) => a[0] - b[0] || b[1] - a[1]);
    const merged = [];
    for (const span of spans) {
      const previous = merged[merged.length - 1];
      if (previous && span[0] < previous[1]) previous[1] = Math.max(previous[1], span[1]);
      else merged.push(span.slice());
    }
    return merged;
  }

  function addHighlight(parent, text, query) {
    const value = String(text || "");
    const spans = highlightRanges(value, query);
    let cursor = 0;
    for (const [start, end] of spans) {
      if (start < cursor) continue;
      if (start > cursor) parent.appendChild(document.createTextNode(value.slice(cursor, start)));
      const mark = document.createElement("mark"); mark.textContent = value.slice(start, end); parent.appendChild(mark); cursor = end;
    }
    if (cursor < value.length) parent.appendChild(document.createTextNode(value.slice(cursor)));
  }

  function excerpt(text, query, maxLength) {
    const value = String(text || "");
    const mapped = mappedNormalization(value);
    const first = tokenize(query).map((term) => mapped.text.indexOf(term)).filter((i) => i >= 0).sort((a, b) => a - b)[0];
    const size = maxLength || 240;
    if (value.length <= size) return value;
    const originalFirst = first === undefined ? 0 : mapped.starts[first];
    const targetStart = first === undefined ? 0 : Math.max(0, originalFirst - Math.floor(size / 3));
    const start = mapped.segments.reduce((chosen, segment) => segment.start <= targetStart ? segment.start : chosen, 0);
    const targetEnd = Math.min(value.length, start + size);
    let end = start;
    for (const segment of mapped.segments) {
      const segmentEnd = segment.start + segment.text.length;
      if (segmentEnd <= targetEnd) end = segmentEnd;
      else break;
    }
    if (end <= start) {
      const next = mapped.segments.find((segment) => segment.start >= start);
      if (next) end = next.start + next.text.length;
    }
    return (start ? "…" : "") + value.slice(start, end) + (end < value.length ? "…" : "");
  }

  async function parsePayload(arrayBuffer) {
    const bytes = new Uint8Array(arrayBuffer);
    let jsonBytes = arrayBuffer;
    if (bytes[0] === 0x1f && bytes[1] === 0x8b) {
      if (!("DecompressionStream" in globalThis)) throw new Error("このブラウザーはgzip検索データに対応していません。");
      const stream = new Blob([arrayBuffer]).stream().pipeThrough(new DecompressionStream("gzip"));
      jsonBytes = await new Response(stream).arrayBuffer();
    }
    return JSON.parse(new TextDecoder("utf-8").decode(jsonBytes));
  }

  function render(papers, state, limit) {
    const list = document.getElementById("results");
    const status = document.getElementById("status");
    const more = document.getElementById("more");
    list.replaceChildren();
    const shown = papers.slice(0, limit);
    for (const paper of shown) {
      const item = document.createElement("li"); item.className = "result";
      const title = document.createElement("h2"); const link = document.createElement("a"); link.href = paper.source_url; link.textContent = paper.title; title.appendChild(link); item.appendChild(title);
      const summary = document.createElement("p"); summary.className = "summary";
      const summaryText = state.query && paper.matchedFields.includes("summary") ? excerpt(paper.summary, state.query, 240) : (paper.summary_display || paper.summary);
      addHighlight(summary, summaryText, state.query); item.appendChild(summary);
      const matched = paper.matchedFields.length ? `${paper.matchedFields.map((field) => LABELS[field]).join("・")}一致` : "検索語なし";
      const meta = document.createElement("p"); meta.className = "meta"; meta.textContent = `${matched} · ${paper.family} / ${paper.lineage} · ${paper.date || "公開年不明"} · リポジトリ内被引用 ${paper.citations || 0}`; item.appendChild(meta);
      if (paper.attention) { const badge = document.createElement("span"); badge.className = "badge"; badge.textContent = "注目"; item.appendChild(badge); }
      if (paper.implementation) { const impl = document.createElement("p"); impl.className = "implementation"; impl.textContent = typeof paper.implementation === "string" ? `実装: ${paper.implementation}` : "実装あり"; item.appendChild(impl); }
      if (paper.matchedFields.includes("body") && state.field !== "title" && state.field !== "summary") {
        const body = document.createElement("p"); body.className = "excerpt"; addHighlight(body, excerpt(paper.body, state.query), state.query); item.appendChild(body);
      }
      list.appendChild(item);
    }
    status.textContent = papers.length ? `${papers.length}件中 ${shown.length}件を表示しています。` : "条件に一致する論文はありません。";
    more.hidden = papers.length <= shown.length;
  }

  async function start() {
    const app = document.getElementById("app"); if (!app) return;
    const form = document.getElementById("search-form");
    const controls = Object.fromEntries(["query", "field", "year", "sort", "attention", "implementation"].map((id) => [id, document.getElementById(id)]));
    const state = queryState(location.search);
    controls.query.value = state.query; controls.field.value = state.field; controls.sort.value = state.sort; controls.attention.checked = state.attention; controls.implementation.checked = state.implementation;
    let papers = [], matches = [], limit = 50, timer, bodyIsNormalized = false;
    try {
      const response = await fetch("papers.json.gz", { credentials: "same-origin" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const compressed = await response.arrayBuffer();
      const data = await parsePayload(compressed);
      if (!data || data.scope !== (app.dataset.scope || "all") || !Array.isArray(data.papers)) throw new Error("検索データのscopeが一致しません。");
      papers = data.papers;
      bodyIsNormalized = data.body_normalization === "NFKC";
      for (const year of Array.from(new Set(papers.map((paper) => paper.year).filter(Boolean))).sort((a, b) => b - a)) {
        const option = document.createElement("option"); option.value = String(year); option.textContent = `${year}年`; controls.year.appendChild(option);
      }
      controls.year.value = state.year;
    } catch (error) {
      document.getElementById("status").textContent = `検索データを読み込めませんでした: ${error.message}`; return;
    }
    function updateUrl() {
      const params = new URLSearchParams();
      if (state.query) params.set("q", state.query); if (state.field !== "all") params.set("field", state.field);
      if (state.year) params.set("year", state.year); if (state.sort !== "recommend") params.set("sort", state.sort);
      if (state.attention) params.set("attention", "1"); if (state.implementation) params.set("implementation", "1");
      const queryString = params.toString();
      history.replaceState(null, "", `${location.pathname}${queryString ? `?${queryString}` : ""}`);
    }
    function run() { matches = filterAndRank(papers, Object.assign({}, state, { preNormalizedBody: bodyIsNormalized })); limit = 50; render(matches, state, limit); updateUrl(); }
    function sync() { state.query = controls.query.value; state.field = controls.field.value; state.year = controls.year.value; state.sort = controls.sort.value; state.attention = controls.attention.checked; state.implementation = controls.implementation.checked; }
    form.addEventListener("submit", (event) => { event.preventDefault(); sync(); run(); });
    form.addEventListener("input", () => { sync(); clearTimeout(timer); timer = setTimeout(run, 220); });
    document.getElementById("more").addEventListener("click", () => { limit += 50; render(matches, state, limit); });
    run();
  }

  const api = { normalize, tokenize, filterAndRank, queryState, excerpt, highlightRanges, parsePayload, start };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (root && root.document) root.addEventListener("DOMContentLoaded", start);
})(typeof globalThis !== "undefined" ? globalThis : this);
