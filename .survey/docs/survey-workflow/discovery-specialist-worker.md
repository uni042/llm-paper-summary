# Discovery specialist worker

この文書は、毎時`:00` JSTに動く探索主体のScheduled Chat workerの正本とする。通常は探索（discovery）を行い、候補在庫が多くResearch/Auditが処理可能な場合は追加readerとしてresearchを消化する。

## 最重要原則

通常runの正常終了は **時間だけ** で決める。実際のScheduled Chat invocation開始時刻を1回だけ固定し、`run_deadline = actual_start + 3600 seconds` とする。`run_deadline` まで600秒以下になった引き継ぎガード（handoff guard）のみが、通常の `STOP_RUN` / 正常finalizeを許可する。

以下は件数にかかわらず正常終了条件にしない。

- discovery round数
- candidate数
- submission数
- Research/Audit完了数
- candidate在庫数
- 空round、全重複round、低採用率round
- 現在の探索軸やquery familyが枯れたという判断
- `next_axis_hint` が空であること
- 1件または複数件のjob完了

最低round数、最低candidate数、最低submission数、最低Research件数は設けない。件数はすべて観測値（telemetry）であり、ノルマ（quota）でも終了許可でもない。

## 候補受入は無制限

探索workerとqueue側のcandidate受入には、5件などのアプリケーション上の固定上限を設けない。1 roundで強い候補が12件、50件、100件見つかった場合も、重複除外・品質判定後の候補をすべて1つの `submit_discovery_round` に含めてよい。

候補が多いことを理由に弱い候補を混ぜない一方、固定件数へ切り詰めてもならない。品質基準を満たす候補はすべて受け入れ、最終的な重複抑止はGitHub Actions側で行う。

## 同一run内の継続

1 discovery round / 1 submissionの耐久保存は中間checkpointであり、run完了ではない。各round後に最新HEAD、queue、identity、`discovery-state.json`、candidate inventoryを再取得し、引き継ぎガード外なら次の独立作業へ進む。

Discovery modeでは、現在の探索軸が空・全重複・低採用・枯渇状態でもrunを終了しない。検索語、source、引用方向、隣接分野、関連実装などを変えて探索空間を再生成する。現在の候補集合を使い切ったことは「runで仕事がなくなった」ことを意味しない。

予定`:00`までの残り時間は、実開始基準のrun deadlineを確定できない古いcaller向けの互換フォールバック（compatibility fallback）に限る。予定境界が近くてもrun-local deadlineに余裕があれば継続する。

## candidate在庫とモード切替

`candidate-buffer-policy.md` の水位を共有する。

- low watermark: 25
- critical watermark: 15
- overflow research threshold: `candidate_inventory > 50`
- target / upper cap: なし

`candidate_inventory > 50` かつactionable Research/Auditがある場合はoverflow research modeへ切り替える。これはrun終了ではなく処理モードの変更である。candidate在庫が50以下へ戻る、またはactionable Research/AuditがなくなればDiscovery modeへ戻る。

## Overflow research mode

overflow research modeでは通常論文workerと同じResearch/Audit契約を使う。

1. `checkpointed_job_ids` を除いたactionable readyからpriority順に1件だけclaimする。
2. 一次資料全文を取得・精読し、repository-qualityの5-slot structured research recordを作る。
3. preflight後、immutable descriptorまたはLibrary checkpointへ完全payloadを耐久保存する。
4. terminal反映を同期障壁にせず、最新HEAD / queue / claim stateを再取得する。
5. 引き継ぎガード外でactionable workが残る限り次の1件へ進む。
6. candidate在庫が50以下、またはactionable Research/AuditなしならDiscovery modeへ戻る。

1runあたり「最低3件」などの件数ノルマは設けない。1件でも100件でも、時間と耐久保存が許す限り処理を続ける。同一workerが同時に保持する未完了claimは1件だけとする。

## 探索経路

直前の高重複軸を機械的に繰り返さず、少なくとも次から探索軸を選び直す。

- 新着・recent revision
- 収録済み重要論文のforward citation
- 重要論文のbackward reference
- DBMS / OS / storage / distributed systems / HPC / GPU runtime / networking / memory systems等の隣接分野
- 直近採用候補からの検索語・著者・実装・引用クラスタ拡張
- offload / hierarchical memory / SSD/NVMe / MoE expert placement・cache・prefetch / KV cache / scheduling / disaggregation / inference framework等の重点テーマ

探索軸の候補リスト自体も固定集合とみなさない。既知軸が一巡した場合は、収録済み論文・直近candidate・引用グラフ・隣接分野から新しい軸を生成する。

## 二重探索・二重投入の防止

探索開始前とcandidate投入直前の2段階で重複判定する。paper identity index、identity deltas、既収録paper、既存research/discovery jobs、GitHub fallback inbox/archive、可能な範囲のLibrary pending/offline seedを照合する。

同一性判定はcanonical ID、arXiv ID、DOI、OpenReview IDを優先し、最後にnormalized titleを使う。write直前に最新HEAD / identity / queueを再取得し、その間に既存化した候補は送らない。

## transport

GitHub write可能時はworkflow v10の自己記述型探索round transport（self-describing discovery round transport）を使う。各roundは独立したimmutable submissionとして、トップレベルに `operation: "submit_discovery_round"`、`candidates`、`discovery_stats` を含める。この形式ではworker側でsynthetic `job_id` を作らない。

`candidates` 配列に固定件数上限はない。候補数が多い場合も分割必須とはせず、そのroundで得られた強い候補を完全に保持する。transport/backendの実際の外部制約で単一payloadが保存不能な場合だけ、安全な複数immutable submissionへ分割してよい。その場合も総候補数を切り捨ててはならない。

1回の探索主体Scheduled Chat実行では開始時に1つだけ `run_key` を確定し、そのrun内の全roundで同じ値を使う。`run_key` は集計用であり、handoff時間は実開始時刻 + 3600秒で別に管理する。

`discovery_stats` には探索軸、query概要、candidate数、Scheduled Chat側で除外した重複数、重複ID、次回推奨軸を残す。`accepted_count` はActionsが最終dedupe後に確定する。

GitHub write不能時は `fallback-routing.md` に従い、ChatGPT Library `/LLM-survey-outbox/pending/` へ完全envelopeを耐久保存する。

## 異常blocker

正本read不能、GitHub/Library双方で耐久保存不能、platform/tool hard limitなどは通常成功の終了理由ではない。これらは異常blockerとして記録し、回復可能なら回復して継続する。回復不能でも「正常に仕事を使い切った」とは扱わない。

## 終了監査

終了直前に `continuation-policy.json` と `.survey/scripts/continuation_gate.py` を評価する。通常runで正常finalizeしてよいのは、run-local handoff guardが成立し、必要な成果が耐久保存され、未完了claimの安全な着地ができた場合だけである。

探索枯渇、round数、candidate数、submission数、Research完了数、在庫状態によって正常finalizeしてはならない。

## 通知

通常成功時はユーザーへ通知しない。正本が読めない、成果をGitHub/Libraryのどちらにも耐久保存できない、または継続不能な異常blockerが残る場合だけ問題として通知する。
