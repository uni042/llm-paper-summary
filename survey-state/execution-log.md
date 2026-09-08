# Survey Execution Log

直近24時間の客観的な実行記録を保持する。

## 2026-09-08 10:00 JST
- planned slot: `2026-09-08 10:00 JST`
- run_id: `scheduled-20260908T100000+0900`
- workflow_version: `2`
- mode: `hourly-inference`
- status: `running`
- fixed research targets: `Pallas` (arXiv:2608.16477), `HeadInfer` (arXiv:2502.12574)
- fixed audit targets: `Fiddler` (arXiv:2402.07033), `Hydragen` (arXiv:2402.05099)
- checkpoint: target queue persisted before primary-source review

## 2026-09-08 08:58–09:11 JST
- planned slot: `2026-09-08 09:00 JST`
- run_id: `scheduled-20260908T090000+0900`
- workflow_version: `2`
- mode: `hourly-inference`
- status: `completed`
- research: assigned 2 / completed 2 / added 2 / updated 0 / already_recorded 0 / not_selected 0 / carried_over 0
- audit: assigned 2 / completed 2 / changed 2 / no_change 0 / carried_over 0
- pending_research at end: 1（独立新着確認で次回候補へ追加: Pallas, arXiv:2608.16477）
- pending_audit at end: 0
- batch size: research 2 / audit 2
- full_batch_streak: 1（今回開始時の固定対象は調査2/2・監査2/2を全件保存確認まで完了。実行中に新規発見したPallasは次回候補のため増加判定から除外）
- discovery: existing queue primary-source review + independent arXiv search
- validation: pass — recursive tree has 160 inference paper Markdown files including 6 moved stubs; identity registry has 154 active studies（144 arXiv + 10 other）, all arXiv IDs unique; Inference 154 / Training 19 / total 173; lineage counts KV Optimization 11 and KV Offload 21; required new-paper and audit metadata present
- rejected ledger: added 0 / updated 0
- added: `HeadWiseKV` (arXiv:2609.02029), `SwiftCache` (arXiv:2606.16135)
- audited: `DeepSpeed-FastGen` — arXiv v1、Microsoft DeepSpeed所属、公式code、Llama-2/A100・H100・A6000実機評価を確認。`MoE-Infinity` — arXiv v3、著者6名と所属、RTX A5000実機評価、公式codeを確認
- result commits: `ad6b6c43`, `6b88dd4f`
- checkpoint commit: `bf5ac824`
- error / bottleneck: none

## 2026-09-08 08:38–08:40 JST
- planned slot: `manual recovery of 08:00 morning slot`
- run_id: `manual-morning-20260908T083800+0900`
- workflow_version: `2`
- mode: `morning`
- status: `completed`
- research / audit: not applicable in morning mode; existing queues were not processed or reordered
- morning report cutoff: previous cutoff was unset; initial lower bound = 2026-09-07 08:38 JST (24 hours before start), current cutoff = 2026-09-08 08:38 JST
- paper aggregation: completed from repository change history for the initial 24-hour window
- framework updates: completed; llama.cpp Vulkan TQ1_0 execution support (b10831) and RMSNorm fusion expansion (b10833) recorded
- major LLM releases: completed; existing Qwen3.8-Flash-Next open-weight entry revalidated and expanded with official architecture / parameter / runtime details; no newer Qwen family release superseded Qwen3.8-Max-0902 in the family-latest table
- consistency check: pass — recursive tree contains 158 inference paper Markdown files including 6 moved stubs; identity registry has 152 active studies; training count remains 19; Other lineage remains 99-last; state files present
- pending_research remains 2; pending_audit remains 1
- batch size unchanged: research 2 / audit 2; full_batch_streak unchanged: 0
- rejected ledger: unchanged
- result commits: `14194947`, `791d5744`
- error / bottleneck: none

## 2026-09-08 07:56–08:07 JST
- planned slot: `manual hourly test (07:00 hour)`
- run_id: `manual-20260908T075610+0900`
- workflow_version: `2`
- mode: `hourly-inference`
- status: `completed`
- research: assigned 2 / completed 2 / added 2 / updated 0 / already_recorded 0 / not_selected 0 / carried_over 0
- audit: assigned 2 / completed 2 / changed 2 / no_change 0 / carried_over 0
- pending_research at end: 2（独立新着確認で次回候補へ追加: HeadWiseKV, SwiftCache）
- pending_audit at end: 1（今回未着手の既存queue: DeepSpeed-FastGen）
- batch size: research 2 / audit 2
- full_batch_streak: 0（未着手queueが残るため増加条件外）
- discovery: `arxiv-search` + independent new-source quick scan
- newly queued after identity check: `HeadWiseKV` (arXiv:2609.02029), `SwiftCache` (arXiv:2606.16135)
- validation: pass for identities/counts/README/audit metadata — identity registry 152 active / Inference 152 / Training 19 / total 171。新規2 IDは各1 active lineage、Serving 35本、一言説明付き。Training配下変更なし。
- rejected ledger: added 0 / updated 0
- result commits: `dfcfe937`, `95196398`, `b73bfe48`, `7a75357c`, `fd69d347`, `52a92598`, `ef4532ae`, `63430eaf`, `50668a90`, `0c0fd17c`
- added: `Geometry-Aware Online Scheduling for LLM Serving: From Theoretical Bound to System Practice` (arXiv:2606.22327), `Online Linear Programming for Multi-Objective Routing in LLM Serving` (arXiv:2607.03948)
- audited: `SpotServe` — ASPLOS 2024、公式artifact、主要評価値、canonical/audit metadataを確認。`ServerlessLLM` — OSDI 2024最終版、著者所属、公式code、canonical/audit metadataを確認。
- save note: content processing completed, but this manual test used multiple Contents API commits instead of the runbook-preferred Git Data API batched result commits. A temporary test marker was created and immediately removed before survey data changes; no final repository file remains from it.
- error / bottleneck: no research/audit interruption; save batching deviated from preferred workflow in this manual test.

## 2026-09-08 07:43–07:53 JST
- planned slot: `manual hourly test (07:00 hour)`
- run_id: `manual-20260908T074337+0900`
- workflow_version: `2`
- mode: `hourly-inference`
- status: `completed`
- research: assigned 2 / completed 2 / added 2 / updated 0 / already_recorded 0 / not_selected 0 / carried_over 0
- audit: assigned 2 / completed 2 / changed 2 / no_change 0 / carried_over 0
- pending_research at end: 2（今回未着手の既存queue）
- pending_audit at end: 3（今回未着手の既存queue）
- batch size: research 2 / audit 2
- full_batch_streak: 0（queueに未着手作業が残るため増加条件外）
- discovery: `arxiv-search` + independent new-source quick scan; 今回の固定対象を増やす追加候補は登録なし
- validation: pass — identity registry 150 active / Inference 150 / Training 19 / total 169。新規2 IDは各1 active lineage、README件数・一言説明を同期、Training配下変更なし。
- recovery / migration: Workflow v2へ初回移行し、pending queueを保持したまま research/audit batch sizeを5/5→2/2、streakを0としてcheckpoint。
- rejected ledger: added 0 / updated 0
- added: `An Interpretable Latency Model for Speculative Decoding in LLM Serving` (arXiv:2605.15051), `Cache-Resident LLM Inference in GB-Scale Last-Level Caches` (arXiv:2606.25353)
- audited: `AlpaServe` — OSDI 2023最終版・著者所属・公式code・canonical/audit metadataを確認。`FastServe` — NSDI 2026最終版・公式code・canonical/audit metadataを確認し、arXiv prepublicationと最終版のheadline評価値を分離。
- result commits: `46981baa`, `e34b112f`
- checkpoint commit: `256a1097`
- error / bottleneck: none observed in this manual run

## 2026-09-08 05:58 JST
- mode: `hourly-inference`
- status: `partial`
- research: assigned 5 / completed 1 / added 1 / updated 0 / already_recorded 0 / not_selected 0 / carried_over 4
- audit: assigned 0 / completed 0 / changed 0 / no_change 0 / carried_over 0
- pending_research: 4
- pending_audit: 0
- batch size: research 5 / audit 5
- full_batch_streak: 0
- discovery: `arxiv-search`
- validation: pass for completed SPECTRE page/index/count changes; remaining research candidates retained in queue
- rejected ledger: added 0 / updated 0
- added: `SPECTRE: Hybrid Ordinary-Parallel Speculative Serving for Resource-Efficient LLM Inference` (arXiv:2605.08151)
- carried over research: `An Interpretable Latency Model for Speculative Decoding in LLM Serving`, `Cache-Resident LLM Inference in GB-Scale Last-Level Caches`, `Geometry-Aware Online Scheduling for LLM Serving`, `Online Linear Programming for Multi-Objective Routing in LLM Serving`
- validation detail: Inference 149本 / Training 19本 / total 168本へ同期。Speculative Decoding / MoEは12本。SPECTRE pageはcanonical_id / last_verified / verified_arxiv_versionを保持し、lineage READMEへ一言説明付きで追加。Training配下は変更なし。
- commits: `c550c45`, `0173687`, `8312aa5`, `bc0d3b2`, `7ea5864`, `aab3e3f`

## 2026-09-08 04:59–05:00 JST
- mode: `hourly-inference`
- status: `completed`
- research: assigned 3 / completed 3 / added 3 / updated 0 / already_recorded 0 / not_selected 0 / carried_over 0
- audit: assigned 4 / completed 4 / changed 4 / no_change 0 / carried_over 0
- pending_research: 0
- pending_audit: 0
- batch size: research 5 / audit 5
- full_batch_streak: 0
- discovery: `arxiv-new`
- validation: repaired — 前回途中だったOUTLETSのServing indexと、AceSpec / Random Attentionを含むtop-level件数を同期。Inference 148本 / Training 19本 / total 167本。影響したlineage READMEは一言説明付きentryを維持。
- recovery: 前回すでに作成済みだった `OUTLETS` / `AceSpec` / `Random Attention` のpaper pageを再作成せず、欠けていたindex/count/stateだけを補完。
- rejected ledger: added 0 / updated 0
- added: `OUTLETS`, `AceSpec`, `Random Attention`
- audited: `DistServe`, `Sarathi-Serve`, `SGLang`, `Pensieve` — canonical identityとaudit metadataを追加し、一次資料・publication / code状態・評価形態を再確認。
- commits: `90d4eb1`, `2cddd30`, `6fdff10`, `fca1948`, `710340e`, `d507478`, `5d59127`, `98a9303`, `2713eeb`

## 2026-09-08 03:59 JST
- mode: `hourly-inference`
- status: `partial`
- research: assigned 4 / completed 1 / added 0 / updated 0 / already_recorded 1 / not_selected 0 / carried_over 3
- audit: assigned 4 / completed 0 / changed 0 / no_change 0 / carried_over 4
- pending_research: 3
- pending_audit: 4
- batch size: research 5 / audit 5
- full_batch_streak: 0
- discovery: `arxiv-new`
- validation: partial — research pages for OUTLETS / AceSpec / Random Attention were created and AceSpec / Random Attention lineage indexes were updated, but top-level count synchronization and OUTLETS serving index remain for recovery before these three are marked complete
- recovery: `mzCache` was found already recorded in the Edge lineage and was therefore not duplicated
- rejected ledger: added 0 / updated 0
- already recorded: `mzCache: On-Device LLM Memory Management under Multitasking`
- staged additions awaiting index completion: `OUTLETS`, `AceSpec`, `Random Attention`
- carried over audit: `DistServe`, `Sarathi-Serve`, `SGLang`, `Pensieve`
- commits: `3e2bfff`, `632a497`, `ec4824c`, `8b6b5d5`, `cfb3829`

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
- validation detail: Inference 139本 / Training 19本 / total 158本へ同期。Serving lineage 30本。一言説明付きentryを維持し、Training配下変更なし。
- commits: `3f62197`, `6e7bb41`, `56f03e6`, `e9fe36f`, `f2216d9`