# Chat worker router — workflow v10

予定されたScheduled Chat workerは**1つだけ**。通常runは実行時刻で次のどちらか一方を選び、同じ枠で両方を処理しない。ただし、後述する24-run maintenance gateが最優先であり、maintenance runでは通常workerを実行しない。

- **maintenance gateで24回目** → full GC + repository-wide consistency checkだけを要求して終了
- **08:30 JST** → その他更新worker
- **それ以外の毎時 :30** → 論文worker

毎回default branch最新HEADを取得し、このrouter、[README.md](README.md)、[queue-v10.md](queue-v10.md)、[continuation-policy.json](continuation-policy.json)、[fallback-routing.md](fallback-routing.md)、`.survey/work-queue/next-jobs.json`、`.survey/work-queue/maintenance-cycle.json` を同じHEADから読む。必要に応じて [drive-outbox.md](drive-outbox.md)、[backlog-resilience.md](backlog-resilience.md)、`.survey/work-queue/records/bank-registry.json` を読む。

一時配送について古い文書と矛盾する場合は、**このrouter → fallback-routing.md → continuation-policy.json → backlog-resilience.md → drive-outbox.md → queue-v10.md** の順で新しい記述を優先する。Notionと旧 `/LLM-survey-fallback/` は新規保存先に使わない。

## 0. 24-run maintenance gate

通常の時刻routingより先に `.survey/work-queue/maintenance-cycle.json` を処理する。

1. 現在のScheduled Chat実行枠をJSTで一意な `run_key`（例 `2026-09-10T18:30:00+09:00`）として決める。
2. `last_counted_run_key` が同じなら二重加算しない。同じrunの再試行として現在のcounterをそのまま使う。
3. 新しいrunなら `total_runs_counted += 1`、`runs_since_maintenance += 1`、`last_counted_run_key = run_key` として、最新blob SHAを再取得したうえでstateを更新する。
4. `runs_since_maintenance < cadence_runs`（現在24）なら通常routingへ進む。
5. `runs_since_maintenance >= cadence_runs` になったrunはmaintenance runとする。その更新で `runs_since_maintenance = 0`、`maintenance_sequence += 1`、`maintenance_pending = true`、`last_maintenance_requested_at = 現在時刻` とする。
6. maintenance runでは**論文worker、その他更新worker、fallback replay、discovery、research、auditを一切実行しない**。state更新によって `.github/workflows/maintenance.yml` を起動し、GitHub Actions側の `.survey/scripts/full_gc.py` → `.survey/scripts/check_repository.py` に full GC と repository-wide consistency check を任せ、そのrunは終了する。
7. maintenance workflowは結果を `.survey/reports/full-gc-latest.json` と `.survey/reports/consistency-latest.json` に保存し、`maintenance_pending = false`、最終status、削除件数、完了時刻をstateへ戻す。
8. maintenance workflowの失敗・遅延で `maintenance_pending = true` が残っていても、後続のScheduled Chat run全体を停止しない。新しいrunはcounterを通常どおり数え、同じmaintenance sequenceを再発行しない。問題は通知対象として扱う。

full GCは保守対象だけを削除する。論文Markdown、docs、scripts、workflow、`next-jobs.json`、queue state、record banks、fallback inbox/archive、現在参照中のjobは削除禁止。terminal jobや旧runtime artifactも保持期間を満たし、かつlive stateから参照されていない場合だけ削除する。

## 1. run全体を止める条件

個別jobの失敗、単一transportの失敗、Drive pending増加、Library pending増加、GitHub fallback-inbox増加、record bank枯渇はrun停止理由ではない。

run終了前に必ず `continuation-policy.json` を評価し、可能なら `.survey/scripts/continuation_gate.py` を使う。

少なくとも次を確認する。

1. GitHub readは可能か。
2. 未反映の完成成果がGitHub / Drive / Libraryのいずれかへ耐久保存済みか、または保存可能か。
3. GitHub readyのほか、fallback spillover候補を含めて独立作業が残るか。
4. readyが実質空でも、fallbackへoffline job seedを保存して新規discoveryを安全に継続できるか。
5. プラットフォーム上限に達していないか。

`CONTINUE` で独立作業がある場合、問題報告だけ出して終了してはならない。

## 2. run開始時の回復とbacklog index

GitHub readが可能なら最新queue/identityに加え、次を可能な範囲で読む。

- Google Drive: `/Google Drive/llm-paper-summary-outbox/pending/`
- ChatGPT Library: `/LLM-survey-outbox/pending/`
- GitHub intake: `.survey/work-queue/fallback-inbox/*.json`
- GitHub archive: `.survey/work-queue/fallback-archive/*.json`

一時的に次を作る。

- `checkpointed_job_ids`: research/auditの完全payloadがoutboxまたはGitHub fallback-inboxへ耐久保存済みのjob
- `spillover_candidates`: offline job seedに含まれ、まだ完成payloadがcheckpointされていない候補

GitHub上で`ready`でも`checkpointed_job_ids`にあるjobは再精読しない。GitHub statusはActionsが反映するまで未完了のまま維持する。

### replay所有権

- **Drive pending** → `.github/workflows/drive-outbox-import.yml` がGitHub immutable intakeへ送る。Scheduled Chatは手動二重投入しない。
- **Library pending** → Scheduled ChatがGitHub write可能なrunで `.survey/work-queue/fallback-inbox/<id>.json` へ送る。固定record bankや`chat-inbox.json`へ直接replayしない。
- **GitHub fallback-inbox** → `.survey/scripts/dispatch_fallback_inbox.py` を呼ぶsurvey-helperだけが固定transportへ展開する。

Library pendingをGitHub intakeへ送る前に、同じ`id`のinbox/archiveを確認する。内容一致なら再writeせずLibrary側をprocessedへ移してよい。内容不一致ならID衝突としてfailedへ隔離する。

## 3. GitHub write失敗の診断

GitHub writeが失敗したら `continuation-policy.json` の手順を唯一の正本とする。

1. 失敗対象の最新blob SHA / repo状態を再取得し、その対象だけ1回再試行する。
2. まだ失敗する場合、そのrun最初のwrite失敗に限り `.survey/work-queue/transport/health-probe.json` を1回更新する。
3. probe成功 → `target_or_payload_specific`。影響payloadだけfallbackへ保存し、他のGitHub writeは継続可。
4. probe失敗 → `run_wide_github_write_unavailable`。そのrunでは以後GitHub writeを繰り返さず、完成成果とoffline seedをfallbackへ保存しながら研究を続ける。

fallbackは [fallback-routing.md](fallback-routing.md) に従い、Driveを先に試し、Driveが利用不能ならLibraryへ切り替える。同一runで経路全体が利用不能と判定済みなら各jobで同じ失敗を繰り返さない。

## 4. 論文worker

正本: [queue-v10.md](queue-v10.md)、[paper template](../../templates/paper.md)、`.survey/work-queue/next-jobs.json`。

research / auditに着手する前に `.survey/templates/paper.md` を読む。新しい会話・実行環境ではテンプレートが例示する [MoE-Infinity のまとめ](../../../papers/inference/01-offload-hierarchical-memory/2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md) も確認する。

Chatは探索、一次資料全文取得、全文精読、科学的判断、監査判断、構造化research record作成を担当する。完成Markdownは作成・送信しない。

### 実行順

1. GitHub readyから`checkpointed_job_ids`を除いた**actionable ready**をpriority順に処理する。
2. actionable readyがなければ、fallback seed由来の未処理`spillover_candidates`をpriority順に処理する。
3. それもなければdiscoveryを行う。
4. job完了、blocked化、checkpoint後はGitHub queueとbacklog indexを再取得し、再び1へ戻る。
5. 固定件数・固定バッチ数・「1本終わったら終了」は設けない。

### GitHub write可能時にcheckpoint済みreadyがqueueを塞ぐ場合

`.survey/work-queue/transport/request-jobs.json` を更新してよい。

```json
{
  "schema_version": 1,
  "operation": "ensure_discovery_excluding_checkpointed",
  "request_id": "request-unique",
  "checkpointed_job_ids": ["job-research-..."]
}
```

Actions側 `.survey/scripts/apply_transport_requests.py` は指定jobをstatus変更せず一時的に実行不能として除外し、他にactionable readyが無ければ新しいdiscovery jobを追加する。

### GitHub write不能中のoffline discovery

GitHub writeがrun-wideで停止していても、DriveまたはLibraryへ保存可能なら新規探索を止めない。

1. identity正本、既存GitHub jobs、両outbox、GitHub fallback-inboxのseed/payloadと重複確認する。
2. 候補0〜5件を選ぶ。弱い候補で埋めない。
3. `.survey/work-queue/transport/offline-job-seed.json` を書くenvelopeを生きているfallbackへ保存する。
4. 各候補のresearch job IDを決定論的に計算する。
5. seed保存後、GitHub job実体化を待たず同じrunで候補を全文精読してよい。
6. 完成したresearch recordを同じjob IDの5-slot + inbox envelopeとしてfallbackへ保存する。
7. 次の候補、または次のdiscoveryへ進む。

job ID規則は [fallback-routing.md](fallback-routing.md) を正本とする。

## 5. record bankと品質

利用可能bankは `.survey/work-queue/records/bank-registry.json` を正本とする。GitHubへ直接slotを書き始める前に、可能なら:

```bash
python .survey/scripts/select_record_bank.py --repo-root .
```

を使い`selected_bank`を採用する。見た目だけでbank空きを推測しない。

A〜Hすべてがdirty/使用中でも、DriveまたはLibraryへ完全payloadを保存できれば研究を止めない。fallback backlogはbank数を研究容量上限にしない。

構造化recordはrendererが後で内容を補う前提で短縮しない。`problem_method`は主要機構ごとに入力、観測、処理、出力、前後接続、なぜ効くか、追加コスト、失敗条件を説明する。

GitHubへslotを書き始める前、またはfallbackへ完成payloadを保存する前に `.survey/templates/paper.md` に対する最終品質チェックを行う。基準未達recordは完成扱いにせず、そのrunで補強する。

## 6. fallback envelopeと復旧

DriveとLibraryは同じ`schema_version: 1` envelope形式を使う。research/auditでは1論文につき1 envelope、5 slot + `chat-inbox.json` を完全に含める。完成Markdownを保存しない。

offline seedも同じenvelopeの`writes`で `.survey/work-queue/transport/offline-job-seed.json` を配送する。

fallback保存成功はGitHub publication成功ではない。ただし耐久checkpointとして後続研究へ進んでよい。

復旧時は外部outboxから固定transportへ直接戻さず、まずGitHub immutable intakeへ送る。この二段階化によりDriveとLibraryが同時復旧しても固定bank/inboxの上書き競合を起こさない。

## 7. その他更新worker（08:30専用）

対象は以下だけ。

1. `framework-updates/**` — LLM推論・serving・runtime等の本質的更新
2. `llm-releases/**` — 新規LLMの正式公開・一般提供・主要更新

論文queueには触れない。既存の固定 `.survey/update-worker/update-payload.json` と `.survey/update-worker/update-inbox.json` を使う。

GitHub write失敗時は同じhealth probeとmulti-outbox fallbackを使う。更新payloadをDriveまたはLibraryへ耐久保存できればScheduled task自体を停止・無効化・再作成しない。復旧時は更新payloadもGitHub immutable intakeを経由し、survey-helperの直列dispatcherが `.survey/update-worker/**` へ展開する。

## 8. 通知

予定タスク本文に通知条件が指定されている場合はそちらを優先する。問題報告はrun終了命令ではない。Stop Gateが`CONTINUE`なら、必要な通知を行った後も処理可能な範囲でjobを続ける。
