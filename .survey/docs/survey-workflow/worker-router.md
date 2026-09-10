# Chat worker router — workflow v10

予定されたScheduled Chat workerは1つだけ。通常runは実行時刻で次のどちらか一方を選ぶ。ただし24-run maintenance gateが最優先で、maintenance runでは通常workerを実行しない。

- maintenance gateで24回目 → full GC + repository-wide consistency checkだけを要求して終了
- 08:30 JST → その他更新worker
- それ以外の毎時 :30 → 論文worker

毎回default branch最新HEADを取得し、このrouter、[README.md](README.md)、[queue-v10.md](queue-v10.md)、[continuation-policy.json](continuation-policy.json)、[fallback-routing.md](fallback-routing.md)、[backlog-resilience.md](backlog-resilience.md)、[suggestion-box.md](suggestion-box.md)、`.survey/work-queue/next-jobs.json`、`.survey/work-queue/maintenance-cycle.json`、`.survey/work-queue/discovery-state.json` を同じHEADから読む。必要に応じて `.survey/work-queue/records/bank-registry.json` を読む。

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

### discoveryの重複回避と再探索

探索開始前に、repo内の既収録論文から可能な範囲で識別集合を作る。最低限、arXiv ID、DOI、正規化タイトルを既収録ID集合として扱う。検索結果は全文取得や詳細評価の前にこの集合で先行フィルタし、既収録候補を除外する。

- 検索ソース側で完全除外できない場合は、まず軽量に広めの候補集合を取得し、ローカル重複除去後の未収録候補だけを詳細評価する。
- arXiv ID / DOIが一致するものは重複とする。IDがなくてもタイトル正規化で同一と判断できるものは重複扱いにしてよい。
- 重複判定のためだけに本文精読は行わない。

1回の探索ラウンドで候補が全て重複または有力な未収録候補が0件だった場合、それ自体をdiscovery終了理由にしない。同一run内で探索軸を変更して再探索する。

推奨ラウンド:

1. 通常の重点テーマ検索。
2. 検索語・表現を変更した同テーマ再検索。
3. 引用・被引用、関連実装、隣接技術語を使った展開検索。
4. 隣接テーマへの拡張検索。

同じ検索戦略・ほぼ同じクエリを反復しない。固定ラウンド数で機械的に埋める必要はないが、少なくとも通常検索が重複だけで終わった場合は1段以上探索軸を変えて再探索する。プラットフォーム上限、保存不能、または有望領域を合理的に使い切った場合のみそのrunのdiscoveryを終了する。

各ラウンド終了時に `.survey/work-queue/discovery-state.json` を更新し、探索軸、検索概要、取得候補数、重複除外数、未収録候補数、採用数、重複率、次回推奨探索軸を記録する。高重複の探索軸は直後のrunで機械的に再使用せず、別軸を優先する。

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

さらに08:30 runでは [suggestion-box.md](suggestion-box.md) に従い、ChatGPT Library `/LLM-survey-suggestion-box/pending/` の未報告提案を確認する。pendingが0件なら目安箱について余分な通知は出さない。pendingがある場合は実質重複をまとめ、重要度の高い順に「観測された問題・提案・期待効果・リスク」をユーザーへ簡潔に報告する。目安箱の提案を08:30 worker自身の判断で自動実装しない。ユーザーへの報告を生成した後に限り、報告済みファイルを `/LLM-survey-suggestion-box/reported/` へ移す。移動失敗時はpendingに残し、未報告のまま失うことを避ける。

## 8. 作業中の改善知見

maintenance runを除く通常workerは、実作業中に具体的な摩擦、失敗、重複作業、無駄、復旧コスト、品質低下リスクを観測し、具体的で実行可能な改善案を得た場合だけ [suggestion-box.md](suggestion-box.md) に従ってLibrary `/LLM-survey-suggestion-box/pending/` へ1提案1ファイルで保存する。提案を作るための追加探索や件数ノルマは設けない。既存pending・最近のreportedと実質重複する案は追加しない。重大障害は目安箱へ送って先送りせず、通常の問題報告・修復経路を使う。

目安箱への保存はbest-effortの観測処理であり、失敗してもresearch、queue、fallback checkpoint、GitHub publicationを止めない。成果保存を常に目安箱より優先する。目安箱はresearch record、queue、fallback、run ledgerの代替にしない。

## 9. 通知

予定タスク本文に通知条件が指定されている場合はそちらを優先する。問題報告はrun終了命令ではない。Stop Gateが`CONTINUE`なら、必要な通知を行った後も処理可能な範囲でjobを続ける。
