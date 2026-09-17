# Discovery specialist worker

この文書は、既存の論文workerとは別に毎時`:00` JSTで動く **探索主体Scheduled Chat worker** の正本とする。平常時はcandidate在庫を継続的に供給し、Research/Audit backlogが十分に大きいときは追加readerとして処理する。

## 役割

- 通常Discovery mode: discovery、軽量重複判定、候補評価、priority付与、candidate投入を行う。
- `candidate_inventory > 50` かつactionable Research/Auditあり: **overflow research mode** へ切り替え、通常論文workerと同じ全文精読・5-slot・claim・durability契約でbacklogを処理する。
- candidate inventoryが50以下、またはactionable Research/Auditがない: Discovery modeへ戻る。
- 既存の`:30`論文workerのdiscovery機能は削除しない。
- GitHub Actionsはqueue/state/identity整合、dedupe、job materialization、`discovery-state.json` 更新を担う。

通常Discovery modeではResearch/Auditの全文精読や5-slot structured research record作成を行わない。候補を安全にcandidate poolへ送った後、最新stateを再取得して次actionを決める。

## 終了判断の責務

worker自身が「時間まで決して終わってはいけない」と気負って継続理由を作る必要も、「もう十分やった」と停止理由を作る必要もない。終了可否は `.survey/scripts/continuation_gate.py` と `.survey/scripts/run_finalization_gate.py` が決める。

workerは実測できるcanonical stateだけを取得し、gateへ渡し、返された `decision` / `required_action` / `next_action` / `finalization_permit` に従う。停止を正当化するために、存在しないエラー、platform/runtime/tool limit、canonical read failure、durable-save failure、探索枯渇を推測・生成しない。

round数、candidate数、Research/Audit完了数、0件round、全重複round、`discovery_exhausted`、next-axis hintの有無は観測・探索戦略・throughputの指標であり、worker独自のrun終了条件ではない。

## 実行時刻とrun deadline

探索主体workerは毎時`:00` JSTに実行する。既存論文workerは毎時`:30` JSTに動作する。

Scheduled Chat invocationが実際に開始した時刻を1回だけ記録し、`run_deadline = actual_invocation_start + 3600s` とする。予定`:00`はrun識別・起動契機には使うが、handoff残時間の基準にはしない。`--seconds-to-next-scheduled-task` はactual-start deadlineを取得できない旧caller向けfallbackに限る。

新しいround/claimの前と各耐久checkpoint後に `seconds_to_run_deadline` を再計算しcontinuation gateへ渡す。600秒handoff guard、180秒finalization帯の適用はscript出力に従い、worker側で前倒し・延長しない。

この`:00` workerは既存の24-run maintenance counterへ加算しない。overflow research modeでも同じ。

## 必読正本

毎回default branch最新HEADを取得し、同じHEADから少なくとも以下を確認する。

1. `candidate-buffer-policy.md`
2. `always-on-worker.md`
3. `claim-serial-policy.md`
4. `queue-v10.md`
5. `fallback-routing.md`
6. `continuation-policy.json`
7. `run-liveness-policy.md`
8. `.survey/work-queue/next-jobs.json`
9. `.survey/work-queue/discovery-state.json`
10. `.survey/survey-state/paper-identity-index.json`
11. 必要に応じて `.survey/survey-state/identity-deltas/**`、claim/submission/ACK state

終了判定については `continuation-policy.json` / `run-liveness-policy.md` と両gate scriptを優先する。

## candidate在庫とモード切替

`candidate-buffer-policy.md` の水位を共有する。

- low watermark: 25
- critical watermark: 15
- overflow research threshold: `candidate_inventory > 50`
- target / upper cap: なし

run開始時、各discovery submission後、Research/Audit payloadの耐久保存後にcandidate inventoryとactionable Research/Auditを再評価する。

candidate inventoryはrun終了条件ではなくモード切替条件である。overflow modeへ入る場合も同じrun_key/run deadlineを維持する。

## Discovery mode

通常Discovery modeでは、直近 `discovery-state.json` を読み、同じ高重複query familyを機械的に反復しない。候補軸には少なくとも以下を含める。

- 新着論文・recent revision
- 収録済み重要論文のforward citation
- 重要論文のbackward reference
- DBMS / OS / storage / distributed systems / HPC / GPU runtime / networking / memory systems等の隣接分野
- 直近採用candidateからのquery expansion
- offload / hierarchical memory / SSD/NVMe / MoE expert placement・cache・prefetch / KV cache / scheduling / disaggregation / inference framework等の重点テーマ

run全体のcandidate件数には固定quota/hard capを設けない。一方、workflow-v10の現行queue contractでは **1 immutable discovery submissionは0〜5 candidates** に制限する。強いdedupe済みcandidateが5件を超える場合は件数だけを理由に捨てず、同じ `run_key` の複数immutable submissionへ5件以下ずつ分割してすべて耐久保存する。弱い候補で件数を埋めない。5件到達やsubmission分割はrun終了理由ではない。

0件roundや全重複roundは `discovery_stats` に事実として残し、最新stateとgateを再評価する。「探索空間を使い切った」という判断もtelemetry/検索戦略上の記録に留め、停止許可には使わない。

## 二重探索・二重投入の防止

探索開始前とcandidate投入直前の2段階でdedupeする。照合対象はpaper identity index、identity deltas、既収録paper、既存research/discovery jobs、GitHub fallback inbox/archive、確認可能なLibrary pending/offline seedとする。

canonical ID、arXiv ID、DOI、OpenReview IDを優先し、最後にnormalized titleを使う。write直前に最新HEAD / queue / identityを再取得し、その間に既存化した候補は送らない。

## candidate priority

priorityは重点テーマとの関連、新規性、既存収録との差分、実測評価、公式実装、引用関係上の重要性、SSD/NVMe・MoE・階層メモリ・serving基盤への研究価値を考慮する。単純FIFOではなく、Research workerが高価値候補から読めるようにする。

## Discovery transport

通常Discovery modeでGitHub write可能時はworkflow-v10のself-describing discovery round transportを使い、paper/state/READMEを直接編集しない。

探索主体workerのmulti-round継続では、各roundを独立immutable submissionとして保存し、トップレベルに `operation: "submit_discovery_round"`、`candidates`、`discovery_stats` を含める。`candidates` は1 submissionあたり0〜5件とし、6件以上の強い候補は同じrun_keyの複数submissionへ分割する。この形式ではworkerが存在しない `job_id` を合成しない。Actions側がsubmission pathを一意キーとしてdeterministic ingest jobを作り、最終dedupe後にResearch jobをmaterializeする。

実在するready Discovery jobを通常workerが処理する互換経路では実在 `job_id` を使ってよいが、探索主体workerのmulti-round continuationをpre-issued jobの有無へ依存させない。

## run_key

1回の探索主体Scheduled Chat実行では開始時に1つだけ `run_key` を確定し、そのrun内の全Discovery round・全submission・overflow modeで同じ値を使う。原則は予定実行枠をJSTの `YYYY-MM-DDTHH:00:00+09:00` で表す。予定枠を直接取得できない場合は実開始時刻をJSTで時単位に切り捨て、その後固定する。

`run_key` は集計識別子でありhandoff guardの時間基準ではない。handoffは実開始 + 3600秒のrun deadlineを使う。

## Discovery durability

Discovery modeへ入ったrunでは、候補0件でもそのrun_keyの正規discovery submissionを残し、「探索したが0件」と「run記録がない」を区別可能にする。空roundでは `candidates: []` と具体的な `empty_round_reason`、評価数、重複数、duplicate IDs、axis/query summary、next-axis hintを保存する。候補が5件を超える場合は同一run_keyの複数submissionへ分割する。

GitHub directが使えない場合は `fallback-routing.md` の承認済みChatGPT Library経路を使う。Google Drive、Notion、旧chat-inboxを新規fallbackとして使わない。

## Overflow research mode

`candidate_inventory > 50` かつactionable Research/Auditありなら、通常論文workerのhigh-backlog Research/Audit契約へ切り替える。

1. 最新queue / identity / claim stateを取得しgateを評価する。
2. gateが継続actionを返しactionable jobがある場合、eligible Research/Auditをpriority順に1件だけclaimする。
3. 一次資料全文を取得・精読し、repository-qualityの5-slot structured recordを作る。
4. claim resultで予約されたrecord bankを使いpreflightする。
5. attempt固有immutable descriptorまたはLibrary checkpointへ完全payloadを耐久保存する。
6. 次の判断にterminal resultが不要なら同期的に待たず最新stateへ進む。必要なら同じidentityを30秒cadenceで再取得する。
7. gateを再評価し、overflow条件が続けば次actionへ、inventoryが50以下またはactionableなしならDiscovery modeへ戻る。

1 workerが同時に保持する未完了claimは1件だけ。1件・3件・その他の完了件数はthroughput metricであり、最低ノルマにもrun停止条件にも使わない。

## 非同期待機

claim result、submission result、Library publication ACK、fallback materialization等が次の判断に必要なら `run-liveness-policy.md` の30秒cadenceを使う。同じrequest/result identityを保持して再取得し、pending中に別IDを作らない。

独立作業が可能なら待機を同期障壁にしない。queued / in_progress / 404 / result未生成をstop理由へ変換しない。

## Gate-driven continuation/finalization

各耐久checkpoint後とfinal response候補地点では、最新canonical stateとrun deadline残秒を取得して `continuation_gate.py` を評価する。

- `CONTINUE`: `required_action` を実行する。
- `STOP_RUN`: active assignment、pending claim/submission/ACK、safe handoff状態とともに `run_finalization_gate.py` へ渡す。
- `MUST_CONTINUE`: `next_action` を実行する。
- `MAY_FINALIZE` かつ `finalization_permit.issued=true`: normal final responseを出す。

これはworkerに無制限の継続を心理的に要求する規則ではない。終了判断を決定論的scriptへ集約し、workerは観測と作業に集中するための規則である。

## Run終了時の記録

final responseでは少なくともactual start/run_key、最終mode、Discovery roundsまたはResearch/Audit処理数、candidate統計、end inventory、durable save状態、continuation/finalization gate値、scriptが返したstop reasonとその具体的evidence、warningsを記録する。

stop reasonはgate出力から取り、曖昧な「時間が厳しい」「実行環境の制約」「一区切り」「十分処理した」「次runで続ける」等をworker独自に追加しない。外部強制終了ならfinal response自体が存在しないため、次runがcanonical stateから回復する。
