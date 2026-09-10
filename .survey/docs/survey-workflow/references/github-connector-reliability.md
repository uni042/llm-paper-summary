# Scheduled task / GitHub connector reliability references

workflow v10のtransport設計判断を再現するための参照資料。GitHub Issuesは利用者による再現報告であり、OpenAI公式仕様ではない。仕様判断は公式資料を優先し、Issuesはfailure modeの実例として扱う。

## OpenAI official

### Agent mode / scheduled tasks

- https://help.openai.com/en/articles/10291617-what-is-agent-mode

Scheduled taskとconnected app、外部データ変更時の承認などを確認するための一次資料。

### Apps in ChatGPT

- https://help.openai.com/en/articles/11487775-connectors-in-chatgpt

接続アプリのpermission、action approval、workspace/app側権限との関係を確認するための一次資料。

## Public reproduction / bug reports

- https://github.com/openai/codex/issues/42687 — connector authority/tool namespaceが途中で失われる例。
- https://github.com/openai/codex/issues/37330 — reconnect後もcreate-fileが403になる例。
- https://github.com/openai/codex/issues/38146 — user権限とconnector App権限が一致しない例。
- https://github.com/openai/codex/issues/39018 — endpoint単位で403になる例。
- https://github.com/openai/codex/issues/41863 — capability surfaceが操作ごとに非対称な例。
- https://github.com/openai/codex/issues/40729 — access変更後にGitHub toolsが失われる例。
- https://github.com/openai/codex/issues/21387 — connector writeだけ403になる例。

## workflow v10への反映

1. 1回のread成功だけで、そのrun中のGitHub write能力が継続すると仮定しない。
2. write失敗時は対象の最新SHAを再取得して対象単位で再試行し、必要ならhealth probeでfailure scopeを判定する。
3. GitHub write不能はresearch failureと分離する。
4. direct write不能でもChatGPT Library `/LLM-survey-outbox/pending/` に完全logical payloadを耐久保存できれば研究を継続する。
5. Libraryからの復旧はGitHub immutable fallback intakeを経由し、固定record bankへ直接replayしない。
6. 成功判定はwrite試行そのものではなくActions resultと最新queueで行う。
7. 構造化transportはpayload size、validation、partial retry、idempotencyを改善するために使う。

仕様やfailure modeが変わった場合だけこの文書を更新する。
