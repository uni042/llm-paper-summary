# Chat worker router — workflow v10

予定されたScheduled Chat workerは1つだけ。通常runは実行時刻で次のどちらか一方を選ぶ。ただし24-run maintenance gateが最優先で、maintenance runでは通常workerを実行しない。

- maintenance gateで24回目 → full GC + repository-wide consistency checkだけを要求して終了
- 08:30 JST → その他更新worker
- それ以外の毎時 :30 → 論文worker

毎回default branch最新HEADを取得し、このrouter、[README.md](README.md)、[queue-v10.md](queue-v10.md)、[continuation-policy.json](continuation-policy.json)、[fallback-routing.md](fallback-routing.md)、[backlog-resilience.md](backlog-resilience.md)、`.survey/work-queue/next-jobs.json`、`.survey/work-queue/maintenance-cycle.json` を同じHEADから読む。必要に応じて `.survey/work-queue/records/bank-registry.json` を読む。

一時配送について古い文書と矛盾する場合は **このrouter → fallback-routing.md → continuation-policy.json → backlog-resilience.md → queue-v10.md** の順で優先する。Google Drive fallback、Notion、旧 `/LLM-survey-fallback/` は新規保存先に使わない。Drive実装の保存版は `archive/drive-fallback-before-removal-20260910` ブランチにある。

## 0. 24-run maintenance gate

通常の時刻routingより先に `.survey/work-queue/maintenance-cycle.json` を処理する。

1. 現在のScheduled Chat実行枠をJSTで一意な `run_key` として決める。
2. `last_counted_run_key` が同じなら二重加算しない。
3. 新しいrunなら `total_runs_counted += 1`、`runs_since_maintenance += 1`、`last_counted_run_key = run_key` としてstateを更新する。
4. `runs_since_maintenance < cadence_runs`（現在24）なら通常routingへ進む。
5. `runs_since_maintenance >= cadence_runs` になったrunはmaintenance runとし、同じ更新で `runs_since_maintenance = 0`、`maintenance_sequence += 1`、`maintenance_pending = true`、`last_maintenance_requested_at` を設定する。
6. maintenance runでは論文worker、その他更新worker、fallback replay、discovery、research、auditを実行しない。`.github/workflows/maintenance.yml` により `.survey/scripts/full_gc.py` → `.survey/scripts/check_repository.py` を実行し、そのrunは終了する。
7. workflowは結果を `.survey/reports/full-gc-latest.json` と `.survey/reports/consistency-latest.json` に保存し、maintenance stateを更新する。
8. maintenance失敗・遅延でpendingが残っても、後続run全体は止めず問題として扱う。

full GCは論文Markdown、docs、scripts、workflow、`next-jobs.json`、queue state、record banks、fallback inbox/archive、現在参照中jobを削除しない。terminal jobや旧runtime artifactは保持期間を満たしlive参照がない場合だけ削除する。

## 1. run全体を止める条件

個別jobの失敗、単一payloadの失敗、Library pending増加、GitHub fallback-inbox増加、record bank枯渇はrun停止理由ではない。

run終了前に `continuation-policy.json` を評価し、可能なら `.survey/scripts/continuation_gate.py` を使う。

少なくとも次を確認する。

1. GitHub readは可能か。
2. 未反映の完成成果をGitHubまたはLibraryへ耐久保存済みか、保存可能か。
3. GitHub ready、Library fallback spillover、GitHub intakeを含めて独立作業が残るか。
4. readyが空でもLibraryへoffline job seedを保存して新規discoveryを安全に継続できるか。
5. プラットフォーム上限に達していないか。

`CONTINUE` で独立作業がある場合、問題報告だけ出して終了してはならない。

## 2. run開始時の回復とbacklog index

GitHub readが可能なら最新queue/identityに加え、可能な範囲で次を読む。

- ChatGPT Library: `/LLM-survey-outbox/pending/`
- GitHub intake: `.survey/work-queue/fallback-inbox/*.json`
- GitHub archive: `.survey/work-queue/fallback-archive/*.json`

一時的に次を作る。

- `checkpointed_job_ids`: 完全research/audit payloadがLibraryまたはGitHub fallback-inboxへ耐久保存済みのjob
- `spillover_candidates`: offline job seedに含まれ、まだ完成payloadがcheckpointされていない候補

GitHub上で`ready`でもcheckpoint済みjobは再精読しない。GitHub statusはActionsが反映するまで未完了のまま維持する。

### replay所有権

- Library pending → Scheduled ChatがGitHub write可能なrunで `.survey/work-queue/fallback-inbox/<id>.json` へ送る。固定record bankや`chat-inbox.json`へ直接replayしない。
- GitHub fallback-inbox → `.survey/scripts/dispatch_fallback_inbox.py` を呼ぶsurvey-helperだけが固定transportへ展開する。

Library pendingをGitHub intakeへ送る前に同じ`id`のinbox/archiveを確認する。内容一致なら再writeせずLibrary側をprocessedへ移してよい。内容不一致ならID衝突としてfailedへ隔離する。

## 3. GitHub write失敗の診断

1. 失敗対象の最新blob SHA / repo状態を再取得し、その対象だけ1回再試行する。
2. まだ失敗する場合、そのrun最初のwrite失敗に限り `.survey/work-queue/transport/health-probe.json` を1回更新する。
3. probe成功 → `target_or_payload_specific`。影響payloadだけLibraryへcheckpointし、他のGitHub writeを継続する。
4. probe失敗 → `run_wide_github_write_unavailable`。そのrunでは以後GitHub writeを繰り返さず、完成成果とoffline seedをLibraryへ保存しながら研究を続ける。

GitHub direct writeもLibrary保存もできない場合だけ、未checkpoint成果を増やす前にSTOP_RUNする。

## 4. 論文worker

正本: [queue-v10.md](queue-v10.md)、[paper template](../../templates/paper.md)、`.survey/work-queue/next-jobs.json`。

research / auditに着手する前に `.survey/templates/paper.md` を読む。新しい会話・実行環境ではテンプレートが例示するMoE-Infinityのまとめも確認する。

Chatは探索、一次資料全文取得、全文精読、科学的判断、監査判断、構造化research record作成を担当する。完成Markdownは作成・送信しない。

実行順:

1. GitHub readyから`checkpointed_job_ids`を除いたactionable readyをpriority順に処理。
2. actionable readyがなければLibrary seed由来の`spillover_candidates`をpriority順に処理。
3. それもなければdiscovery。
4. job完了、blocked化、checkpoint後はqueue/backlogを再取得して1へ戻る。
5. 固定件数・固定バッチ数・「1本終わったら終了」は設けない。

checkpoint済みreadyだけがqueueを塞ぐ場合は `.survey/work-queue/transport/request-jobs.json` の `ensure_discovery_excluding_checkpointed` を使って新規discovery jobを発行してよい。元job statusは変更しない。

### GitHub write不能中のoffline discovery

GitHub writeがrun-wideで停止していてもLibraryへ保存可能なら探索を止めない。

1. identity、既存GitHub jobs、Library pending、GitHub fallback-inboxと重複確認。
2. 候補0〜5件を選ぶ。弱い候補で埋めない。
3. `.survey/work-queue/transport/offline-job-seed.json` を書くenvelopeをLibraryへ保存。
4. candidateのresearch job IDを決定論的に計算。
5. seed保存後、GitHub job実体化を待たず全文精読してよい。
6. 完成research recordを同じjob IDの5-slot + inbox envelopeとしてLibraryへ保存。
7. 次の候補または次のdiscoveryへ進む。

job ID規則は [fallback-routing.md](fallback-routing.md) を正本とする。

## 5. record bankと品質

利用可能bankは `.survey/work-queue/records/bank-registry.json` を正本とする。GitHubへ直接slotを書き始める前に、可能なら:

```bash
python .survey/scripts/select_record_bank.py --repo-root .
```

を使う。

A〜Hすべてがdirty/使用中でも、Libraryへ完全payloadを保存できれば研究を止めない。fallback backlogはbank数を研究容量上限にしない。

structured recordはrendererが後で内容を補う前提で短縮しない。完成扱いにする直前にActions側と同じvalidator基準でpreflightし、5 slotの必須項目・最低説明量・日本語率・用語規則を確認する。基準未達ならそのrunで該当slotを補強する。Actions validation failureは該当jobだけrepair対象とし、独立jobを止めない。

## 6. fallback envelopeと復旧

Libraryは `schema_version: 1` envelopeを使う。research/auditでは1論文につき1 envelopeに5 slot + `chat-inbox.json` を完全に含める。完成Markdownは保存しない。

offline seedも同じenvelopeの`writes`で `.survey/work-queue/transport/offline-job-seed.json` を配送する。

fallback保存成功はGitHub publication成功ではないが、耐久checkpointとして後続研究へ進んでよい。復旧時はLibraryから固定transportへ直接戻さずGitHub immutable intakeを経由する。

## 7. その他更新worker（08:30専用）

対象は以下だけ。

1. `framework-updates/**`
2. `llm-releases/**`

論文queueには触れない。既存の固定 `.survey/update-worker/update-payload.json` と `.survey/update-worker/update-inbox.json` を使う。

GitHub write失敗時は同じhealth probeを使い、更新payloadをLibraryへ耐久保存できればScheduled task自体を停止・無効化・再作成しない。復旧時はGitHub immutable intakeを経由する。

## 8. 通知

予定タスク本文に通知条件が指定されている場合はそちらを優先する。問題報告はrun終了命令ではない。Stop Gateが`CONTINUE`なら、必要な通知を行った後も処理可能な範囲でjobを続ける。
