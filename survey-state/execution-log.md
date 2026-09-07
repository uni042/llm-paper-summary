# Survey Execution Log

直近24時間の客観的な実行記録を保持する。

## 2026-09-08 03:02–03:06 JST
- mode: `hourly-inference`
- status: `partial`
- research: assigned 5 / completed 1 / added 1 / updated 0 / already_recorded 0 / not_selected 0 / carried_over 4
- audit: assigned 4 / completed 0 / changed 0 / no_change 0 / carried_over 4
- pending_research: 4
- pending_audit: 4
- batch size: research 5 / audit 5
- full_batch_streak: 0
- discovery: `arxiv-new`
- validation: pass for completed KVMem/index changes; unfinished research and audits retained in queue
- rejected ledger: added 0 / updated 0
- added: `KVMem: Virtualizing Million-Token Agent Workspaces on a Consumer GPU` (arXiv:2609.04852)
- carried over research: `OUTLETS`, `mzCache`, `AceSpec`, `Random Attention`
- carried over audit: `DistServe`, `Sarathi-Serve`, `SGLang`, `Pensieve`
- validation detail: Inference 145本 / Training 19本 / total 164本へ同期。KVMem pageはcanonical_id / last_verifiedを保持し、KV Offload lineage READMEへ一言説明付きで追加。Training配下は変更なし。
- commits: `8927008`, `8a43a3e`, `b647276`, `b0ede3e`, `00eac55`, `075674f`

## 2026-09-08 02:02–02:05 JST
- mode: `hourly-inference`
- status: `partial`
- research: assigned 5 / completed 5 / added 5 / updated 0 / already_recorded 0 / not_selected 0 / carried_over 0
- audit: assigned 5 / completed 1 / changed 1 / no_change 0 / carried_over 4
- pending_research: 0
- pending_audit: 4
- batch size: research 5 / audit 5
- full_batch_streak: 0
- discovery: `arxiv-search`
- validation: pass for completed research/index changes; unfinished audits retained in queue
- rejected ledger: added 0 / updated 0
- added: `SpecInfer`, `Medusa`, `EAGLE`, `Lookahead Decoding`, `REST`
- lineage update: `Speculative Decoding × MoE` を一般のspeculative decodingも含む `Speculative Decoding / MoE` へ拡張。6本→11本。
- audited: `Splitwise` — ISCA 2024書誌、公式artifact、evaluation typeを確認しcanonical/audit metadataを追加。
- carried over audit: `DistServe`, `Sarathi-Serve`, `SGLang`, `Pensieve`
- validation detail: Inference 144本 / Training 19本 / total 163本へ同期。新規5ページはcanonical_id / last_verifiedを保持し、lineage READMEは全entryに一言説明付き。Training配下は変更なし。
- commits: `8a270ac`, `8c93ebb`, `4daab3c`, `23351d1`, `4c735ea`, `0a6dfe0`, `e9cf37c`, `7c1f59c`, `d92147c`, `0fdf48c`, `6d588e2`, `338c1b6`, `055cc99`

## 2026-09-08 00:57 JST
- mode: `hourly-inference`
- status: `completed`
- research: assigned 1 / completed 1 / added 1 / updated 0 / already_recorded 0 / not_selected 0 / carried_over 0
- audit: assigned 3 / completed 3 / changed 1 / no_change 2 / carried_over 0
- pending_research: 0
- pending_audit: 0
- batch size: research 5 / audit 5
- full_batch_streak: 0
- discovery: `arxiv-new`
- validation: pass
- recovery: `rejected-papers.json` と `execution-log.md` が未作成だったため初期化。
- rejected ledger: added 0 / updated 0
- added: `Adaptive Context Parallelism for Production LLM Serving` (arXiv:2609.04774)
- audited: `ProMoE`, `Orca`, `Efficient Memory Management for Large Language Model Serving with PagedAttention`
- validation detail: Inference 139本 / Training 19本 / total 158本へ同期。Serving lineage 30本。一言説明付きentryを維持し、Training配下は変更なし。
- commits: `3f62197`, `6e7bb41`, `56f03e6`, `e9fe36f`, `f2216d9`
