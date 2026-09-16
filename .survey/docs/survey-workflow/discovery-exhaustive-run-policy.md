# Discovery exhaustive-run policy

この文書は毎時`:00` JSTの探索主体Scheduled Chat workerが1回のrunをどう使うかを定める。役割分離は `discovery-specialist-worker.md`、candidate水位とoverflow切替は `candidate-buffer-policy.md`、最終継続判定は `continuation-policy.json` と `.survey/scripts/continuation_gate.py` を正本とする。

## Run-local time window

Scheduled Chat invocationの実開始時刻を1回だけ固定し、`run_deadline = actual_start + 3600 seconds` とする。予定`:00`は起動・集計識別に使うだけで、通常のhandoff時間計算には使わない。

- run deadlineまで600秒以下: 新しい独立作業を開始しない。現在までの成果を耐久保存し、安全なhandoffを行う。
- run deadlineまで180秒以下: 未保存成果、claim、継続情報の最低限の着地だけを行う。
- 600秒より多く残る: 件数・在庫・探索枯渇を理由に正常終了せず、次の独立作業へ進む。

## 固定件数を使わない

Discoveryには次の固定上限・下限を設けない。

- round数の上限・最低round数
- candidate総数の上限・最低candidate数
- 1 submissionのcandidate数上限
- submission数の上限・最低submission数
- overflow research modeの最低Research完了件数

5本、3件、4 roundなどの過去の値はrun終了・受入拒否・処理保証の判定に使わない。件数はすべて観測値（telemetry）である。

## Discovery mode loop

引き継ぎガード外では次を繰り返す。

1. 最新HEAD、identity、queue、existing jobs、`discovery-state.json`、candidate在庫を確認する。
2. `candidate_inventory > 50` かつactionable Research/AuditありならOverflow research modeへ移る。
3. 直近roundと重複しない探索軸を選ぶ。既知軸が枯れた場合は、引用・関連実装・隣接分野・既存candidateから新しい軸を生成する。
4. title、abstract、書誌情報、一次資料の存在、テーマ適合性を軽量評価する。
5. canonical ID / arXiv ID / DOI / OpenReview ID / normalized titleで重複除外する。
6. そのroundで得られた強いcandidateを **件数で切り捨てず** `submit_discovery_round` へ保存する。
7. `discovery_stats` にrun_key、round、axis、query summary、candidate数、重複数、next-axis hintを残す。
8. 最新stateを再取得し、handoff guard外なら次の探索軸またはOverflow research modeへ進む。

空round、全重複round、低採用率round、`next_axis_hint` 不在は停止条件ではない。それらは次軸を再生成するための入力である。

## Candidate受入

queue/backendのアプリケーションレベルではcandidate配列の固定件数上限を設けない。12件、50件、100件の強候補を含むroundも受け入れる。

外部transportの実際のpayload制約に当たった場合は、安全な複数submissionへ分割してよいが、総candidateを削除・切り捨ててはならない。分割はtransport上の実務対応であり、探索件数上限ではない。

## Overflow research mode loop

Overflow research modeでは新規discoveryを一時停止し、通常論文workerと同じResearch/Audit契約に従う。

1. 最新queue / claim state / checkpointed jobを確認する。
2. eligibleなResearch/Auditをpriority順に1件だけclaimする。
3. 一次資料全文を精読し、5-slot structured research recordを作る。
4. preflight後、immutable descriptorまたはLibrary checkpointへ完全payloadを耐久保存する。
5. terminal反映を同期障壁にせず、最新stateを取り直す。
6. handoff guard外でactionable Research/Auditが残る限り次jobへ進む。
7. candidate在庫が50以下、またはactionable Research/AuditなしならDiscovery modeへ戻る。

「1run最低3件」等のノルマは設けない。完了件数は停止条件でも継続条件でもなく、時間と安全な耐久保存だけがrun終了を支配する。

## 探索空間の扱い

「探索空間を使い切った」はrun正常終了理由にしない。現在のquery family、source、既知のaxis集合が枯れていても、引き継ぎガード外では次のように探索空間を再生成する。

- 新着・recent revisionの別検索語
- forward / backward citationの別seed
- 収録済み重要論文からの関連研究・実装
- DBMS / OS / storage / distributed systems / HPC / GPU runtime / networking / memory systems等の隣接分野
- 直近candidateからの著者・keyword・citation cluster拡張
- offload / hierarchical memory / SSD/NVMe / MoE / KV cache / scheduling / disaggregation / inference framework等の重点テーマの組合せ変更

したがって探索枯渇は観測・診断情報として記録してよいが、正常 `STOP_RUN` を発行しない。

## 正常終了条件

通常runを正常終了してよいのは、原則として次だけである。

1. 実開始時刻 + 3600秒のrun deadlineまで600秒以下となり、handoff guardが成立した。
2. 現在の論理成果がGitHubまたは承認済みLibrary fallbackへ耐久保存されている。
3. 未完了claimが安全に着地している、または安全なhandoff情報が残っている。

正本read不能、GitHub/Library双方のdurability failure、platform/tool hard limitなどは **異常blocker** であり、正常成功のfinalization理由ではない。回復可能なら回復して継続し、回復不能なら異常として残す。

## 非停止条件

以下は単独でも複数同時でも正常stop条件ではない。

- 1件または多数のcandidateを送った
- 1件または多数のsubmissionを保存した
- 1件または多数のDiscovery/Research/Auditを完了した
- candidate inventoryが多い／少ない
- 1つ以上の探索軸が0件、全重複、低採用、または枯渇
- 既知探索軸を一巡した
- Actions materialization待ち
- record bankや表示上のnext jobsが一時的に空
- 予定`:00`が近いがrun-local deadlineには余裕がある

## Run終了時の記録

handoff guardで終了する場合、今回のrunで完了したsubmission / checkpoint、未完了claimの状態、次に試す探索軸またはResearch/Audit候補を耐久状態へ残す。件数目標を達成したという理由だけの終了記録は作らない。
