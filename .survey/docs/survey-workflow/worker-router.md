# Chat worker router — workflow v10

予定されたScheduled Chat workerは**1つだけ**。実行時刻で次のどちらか一方を選び、同じ枠で両方を処理しない。

- **08:30 JST** → その他更新worker
- **それ以外の毎時 :30** → 論文worker

毎回default branch最新HEADを取得し、このrouter、[README.md](README.md)、[queue-v10.md](queue-v10.md)、[continuation-policy.json](continuation-policy.json)、[fallback-routing.md](fallback-routing.md)、`.survey/work-queue/next-jobs.json` を同じHEADから読む。必要に応じて [drive-outbox.md](drive-outbox.md)、[backlog-resilience.md](backlog-resilience.md)、`.survey/work-queue/records/bank-registry.json` を読む。

一時配送について古い文書と矛盾する場合は、**このrouter → fallback-routing.md → continuation-policy.json → backlog-resilience.md → drive-outbox.md** の新しい記述を優先する。Notionは使用しない。

## 1. run全体を止める条件

個別jobの失敗、単一transportの失敗、Drive pending増加、Library pending増加、record bank枯渇はrun停止理由ではない。

run終了前に必ず `continuation-policy.json` を評価し、可能なら次を使う。

```bash
python .survey/scripts/continuation_gate.py ...
```

少なくとも次を確認する。

1. GitHub readは可能か。
2. 未反映の完成成果がGitHub / Drive / Libraryのいずれかへ耐久保存済みか、または保存可能か。
3. GitHub readyのほか、fallback上のspillover候補を含めて独立作業が残るか。
4. readyが実質空でも、fallbackへoffline job seedを保存して新規discoveryを安全に継続できるか。
5. プラットフォーム上限に達していないか。

`CONTINUE` で独立作業がある場合、問題報告だけ出して終了してはならない。

## 2. run開始時の回復とbacklog index

GitHub readが可能なら最新queue/identityを取得する。可能な範囲で次のoutboxも読む。

- Google Drive: `/Google Drive/llm-paper-summary-outbox/pending/`
- ChatGPT Library: `/LLM-survey-outbox/pending/`

そこから一時的に次を作る。

- `checkpointed_job_ids`: research/auditの完全payloadがoutboxへ耐久保存済みのjob
- `spillover_candidates`: offline job seedに含まれ、まだ完成payloadがcheckpointされていない候補

GitHub上で`ready`でも`checkpointed_job_ids`にあるjobは再精読しない。GitHub statusはActionsが反映するまで未完了のまま維持する。

### replay所有権

- **Drive pending** → `.github/workflows/drive-outbox-import.yml` だけが再投入する。Scheduled Chatは二重投入しない。
- **Library pending** → Scheduled Chatだけが再投入する。GitHub writeが利用可能なrunで依存を満たす最古のpayloadから処理し、GitHub側の成功確認後だけ`processed`へ移す。

Library replayで対応jobがまだGitHubに存在しないresearch/audit payloadはfailedにせずdependency待ちとしてpendingに残す。offline seedが先に反映されると `.survey/scripts/apply_offline_job_seed.py` がjobを実体化する。

## 3. GitHub write失敗の診断

GitHub writeが失敗したら `continuation-policy.json` の手順を唯一の正本とする。

1. 失敗対象の最新blob SHA / repo状態を再取得し、その対象だけ1回再試行する。
2. まだ失敗する場合、そのrun最初のwrite失敗に限り `.survey/work-queue/transport/health-probe.json` を1回更新する。
3. probe成功 → `target_or_payload_specific`。影響payloadだけfallbackへ保存し、他のGitHub writeは継続可。
4. probe失敗 → `run_wide_github_write_unavailable`。そのrunでは以後GitHub writeを繰り返さず、完成成果とoffline seedをfallbackへ保存しながら研究を続ける。

fallbackは [fallback-routing.md](fallback-routing.md) に従い、Driveを先に試し、Driveが利用不能ならLibraryへ切り替える。同一runで経路全体が利用不能と判定済みなら各jobで同じ失敗を繰り返さない。

Driveだけ失敗してもLibraryが使えれば続行する。Libraryだけ失敗してもDriveが使えれば続行する。

## 4. 論文worker

正本: [queue-v10.md](queue-v10.md)、[paper template](../../templates/paper.md)、`.survey/work-queue/next-jobs.json`。

research / auditに着手する前に `.survey/templates/paper.md` を読む。新しい会話・実行環境ではテンプレートが例示する [MoE-Infinity のまとめ](../../../papers/inference/01-offload-hierarchical-memory/2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md) も確認する。

Chatは探索、一次資料全文取得、全文精読、科学的判断、監査判断、構造化research record作成を担当する。完成Markdownは作成・送信しない。

### 実行順

1. GitHub readyから`checkpointed_job_ids`を除いた**実行可能ready**をpriority順に処理する。
2. 実行可能readyがなければ、fallback seed由来の未処理`spillover_candidates`をpriority順に処理する。
3. それもなければdiscoveryを行う。
4. job完了、blocked化、checkpoint後はGitHub queueとbacklog indexを再取得し、再び1へ戻る。
5. 固定件数・固定バッチ数・「1本終わったら終了」は設けない。

### GitHub write可能時にcheckpoint済みreadyがqueueを塞ぐ場合

`.survey/work-queue/transport/request-jobs.json` を更新してよい。形式:

```json
{
  "schema_version": 1,
  "operation": "ensure_discovery_excluding_checkpointed",
  "request_id": "request-unique",
  "checkpointed_job_ids": ["job-research-..."]
}
```

Actions側 `.survey/scripts/apply_transport_requests.py` は、指定jobを**status変更せず一時的に実行不能として除外**し、他に実行可能readyが無ければ新しいdiscovery jobを追加する。

### GitHub write不能中のoffline discovery

GitHub writeがrun-wideで停止していても、DriveまたはLibraryへ保存可能なら新規探索を止めない。

1. identity正本、既存GitHub jobs、両outboxのseed/payloadと重複確認する。
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

A〜Hすべてがdirty/使用中でも、DriveまたはLibraryへ完全payloadを保存できれば研究を止めない。fallback backlogはbankを占有しない。

構造化recordはrendererが後で内容を補う前提で短縮しない。`problem_method`は主要機構ごとに入力、観測、処理、出力、前後接続、なぜ効くか、追加コスト、失敗条件を説明する。

GitHubへslotを書き始める前、またはfallbackへ完成payloadを保存する前に `.survey/templates/paper.md` に対する最終品質チェックを行う。基準未達recordは完成扱いにせず、そのrunで補強する。

## 6. fallback envelope

DriveとLibraryは同じ`schema_version: 1` envelope形式を使う。research/auditでは1論文につき1 envelope、5 slot + `chat-inbox.json` を完全に含める。完成Markdownを保存しない。

offline seedも同じenvelopeの`writes`で `.survey/work-queue/transport/offline-job-seed.json` を配送する。

保存成功はGitHub publication成功ではない。元jobは未完了のまま。ただし耐久checkpointとして後続研究へ進んでよい。

## 7. その他更新worker（08:30専用）

対象は以下だけ。

1. `framework-updates/**` — LLM推論・serving・runtime等の本質的更新
2. `llm-releases/**` — 新規LLMの正式公開・一般提供・主要更新

論文queueには触れない。既存の固定 `.survey/update-worker/update-payload.json` と `.survey/update-worker/update-inbox.json` を使う。

GitHub write失敗時は同じhealth probeとmulti-outbox fallbackを使う。更新payloadをDriveまたはLibraryへ耐久保存できればScheduled task自体を停止・無効化・再作成しない。

## 8. 通知

予定タスク本文に通知条件が指定されている場合はそちらを優先する。問題報告はrun終了命令ではない。Stop Gateが`CONTINUE`なら、必要な通知を行った後も処理可能な範囲でjobを続ける。
