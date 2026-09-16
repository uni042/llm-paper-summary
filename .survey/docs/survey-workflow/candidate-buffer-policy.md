# Candidate buffer policy

この文書は論文survey workerのcandidate供給・在庫水位・モード切替の正本とする。探索継続は `discovery-continuation-policy.md`、探索主体workerは `discovery-specialist-worker.md`、run終了判定は `continuation-policy.json` を優先する。

## 目的

DiscoveryをResearch開始前の一回限りの処理ではなく、独立したcandidate供給工程として扱う。弱い論文で件数を埋めず、価値のあるcandidateを継続的に蓄積し、Research/Auditはpriority順に全文精読する。

## 水位

重複排除後の未処理Research候補を `candidate_inventory` とする。

- `low_watermark = 25`
- `critical_watermark = 15`
- `overflow_research_threshold = 50`
- overflow切替条件: `candidate_inventory > 50` かつactionable Research/Auditあり
- target / upper hard cap: なし

これらは処理モードを選ぶ水位であり、runの正常終了条件ではない。candidate在庫が多いことも少ないことも、件数だけではrunを終了させない。

`candidate_inventory` 自体にhard capは設けない。candidate配列にも5件などの固定受入上限は設けない。強いcandidateが1 roundで12件、50件、100件得られた場合も、重複除外後の候補をすべて受け入れる。

## DiscoveryとResearchの分離

Discovery段階ではタイトル、abstract、書誌情報、一次資料の存在、identity重複、テーマ適合性、新規性の見込みを軽量評価する。Research段階で一次資料全文を取得・精読し、repository-qualityの5-slot structured research recordを作る。

Discoveryで得たabstractや検索snippetだけからResearch内容を推測しない。候補数を満たすために弱い論文を採用しない一方、固定件数上限へ強い候補を切り捨てない。

## 複数worker協調

candidate供給とResearch消化は2つのScheduled Chat workerが共有する。

1. **通常論文worker（毎時:30）**: Research/Auditを主担当とする。candidate在庫が25本未満、またはactionable Research/Auditが尽きた場合にDiscoveryも行う。
2. **探索主体worker（毎時:00）**: `candidate_inventory <= 50` またはactionable Research/AuditなしならDiscoveryを行う。`candidate_inventory > 50` かつactionable Research/Auditありなら **overflow research mode** に切り替え、追加readerとしてResearch/Auditへ加勢する。

両workerがResearchを行う場合、それぞれ固有の `worker_id` を使う。同一workerの未完了claimは1件だけだが、異なるworkerが別jobを同時にclaim・精読してよい。同一job排他とrecord bank予約はclaim-fastに任せる。

## Candidate identityと重複抑止

Discovery開始前とcandidate投入直前の2段階で最新HEADを確認し、次を照合する。

- paper identity index
- identity deltas
- 既収録paper
- 既存Research / Discovery job
- GitHub fallback inbox/archive
- 確認可能なChatGPT Library pending/offline seed

canonical ID / arXiv ID / DOI / OpenReview IDを優先し、最後にnormalized titleを使う。並行workerにより投入直前に既存化したcandidateは再送しない。残った競合はActions側dedupeで1件へ収束させる。

## Discovery state

`discovery-state.json` はGitHub Actionsを単一writerとする。Scheduled Chatは共有stateを直接更新せず、各Discovery submissionへ `discovery_stats` を添付する。

少なくとも次を記録する。

- `run_key`
- `round`
- `axis`
- `query_summary`
- `candidate_count`
- `duplicate_filtered_count`
- `duplicate_canonical_ids`
- `next_axis_hint`

`candidate_count` は検索結果の生hit数ではなく、テーマ適合性等を確認して実質的に評価した件数。`accepted_count` はActionsが最終dedupe後に確定する。統計値は観測用であり、quota（ノルマ）やrun終了判定に使わない。

## 探索経路

同じ検索式を機械的に繰り返さず、次を組み合わせる。

- 新着・recent revision
- forward citation
- backward reference
- DBMS / OS / storage / distributed systems / HPC / GPU runtime / networking / memory systems等の隣接分野
- 直近candidateからの検索語・著者・実装・citation cluster拡張
- offload / hierarchical memory / SSD/NVMe / MoE expert placement・cache・prefetch / KV cache / scheduling / disaggregation / inference framework等の重点テーマ

空round、全重複、高重複、低採用、既知軸の一巡はrun終了理由ではない。別軸を生成してDiscoveryを継続する。

## 優先順位

candidateにはResearch priorityを付ける。少なくとも重点テーマとの関連、新規性、既存収録との差分、実測評価、公式実装、引用関係上の重要性、SSD/NVMe・MoE・階層メモリ・serving基盤への研究価値を考慮する。candidate poolが大きくなっても単純FIFOだけで消化しない。

## Run内の制御

maintenance runと08:30 other-update runを除く通常workerでは、run開始時と各耐久保存後にcandidate inventoryを再評価する。

- `candidate_inventory > 50`: actionable Research/Auditがある間、通常論文workerと探索主体workerの双方をhigh-backlog research-only / overflow research modeにする。
- 25〜50: 通常論文workerはactionable Research/Auditがある間Research中心。探索主体workerはDiscoveryを継続する。
- 15〜24: Researchを進めつつDiscovery補充を積極化する。
- 0〜14: Discovery補充を優先し、複数探索経路から在庫回復を図る。

どの水位でも「1run最低3件」等のResearch件数ノルマは設けない。固定batch数も設けない。引き継ぎガード外で独立作業が可能なら処理を続ける。

現在の有望探索軸を使い切ったという判断も正常stop条件にしない。検索語、source、citation seed、隣接分野を再生成する。

## Candidate transport

Discovery submissionの `candidates` 配列にアプリケーション上の固定件数上限はない。そのroundで得られた強いcandidateをすべて保存する。

外部API・GitHub・Library等の実payloadサイズ制約により単一payloadが保存不能な場合のみ複数のimmutable submissionへ安全に分割してよい。この分割はtransport上の制約回避であり、総candidate数を削除・切り捨てる理由にはしない。

## GitHub write不能時

GitHub write不能でもChatGPT Library `/LLM-survey-outbox/pending/` へ保存可能ならworkerを止めない。Research/Auditは完全payloadをcheckpointし、Discoveryはcandidate seedを完全envelopeとして保存する。fallback envelopeにも `discovery_stats` を保持し、復旧後にActionsが通常submissionと同じ統計処理を行えるようにする。

## 通常終了

candidate bufferの水位、候補件数、Research完了件数、Discovery round数、探索枯渇は正常終了条件ではない。通常runの正常終了は実開始基準のrun-local handoff guardに従う。

## 08:30 reporting

08:30 JSTの報告では直近24時間の発見数・追加数・残candidate数を示す。在庫がlow watermark未満ならその旨を示す。target inventoryは設けないため `candidate_inventory / target_inventory` の比率表示は行わない。集計できない場合は推測値で埋めない。

Claims do not change candidate-buffer or discovery visibility. They hide only actively claimed ready Research/Audit jobs from `next-jobs.json`; Discovery remains visible under the existing priority-window policy.
