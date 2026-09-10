# 研究サーベイ運用手順

現在の正本は **workflow v10（structured-record transport + queue + multi-outbox fallback）**。Scheduled Chat workerは毎回default branch最新HEADを取得し、同じHEADの [worker-router.md](worker-router.md)、[queue-v10.md](queue-v10.md)、[continuation-policy.json](continuation-policy.json)、[fallback-routing.md](fallback-routing.md)、`.survey/work-queue/next-jobs.json` を読む。

## 設計原則

- **Chat研究worker**: 一次資料探索、全文精読、科学的判断、正式監査、構造化research record作成。
- **GitHub Actions worker**: record検証、Markdownレンダリング、paper反映、job/state遷移、identity delta、派生view更新、通常job生成、fallback直列dispatch。
- GitHub repositoryを唯一の正本とする。
- Google DriveとChatGPT Libraryは一時配送outboxであり、研究・paper・queueの正本にはしない。
- Notionは使用しない。旧 `/LLM-survey-fallback/` はlegacy移行元であり、新規保存には使わない。
- 固定の日次件数、固定research/audit比率、固定バッチ数は使わない。
- 08:30 JSTだけその他更新worker、それ以外の毎時:30は論文workerを実行し、同じ枠で両方を処理しない。
- 1本終わったこと、pending増加、record bank枯渇、単一配送経路の障害をrun停止理由にしない。
- 停止判定は [continuation-policy.json](continuation-policy.json) と `.survey/scripts/continuation_gate.py` を正本とする。

## 論文品質

論文本文の品質正本は [paper template](../../templates/paper.md)。新しい実行環境では [MoE-Infinity のまとめ](../../../papers/inference/01-offload-hierarchical-memory/2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md) も確認する。

構造化recordは内部メモではなく、最終Markdownへ変換される本文原稿である。特に `problem_method` は、各主要機構について入力、観測状態、処理、出力、前後の接続、なぜ効くか、追加コスト、失敗条件まで読者が追える文章量を持たせる。

## 論文ファイル命名

- arXiv論文: `papers/inference/<lineage>/YYYY-YYMM.NNNNN-<slug>.md`
- arXiv IDなし: `YYYY-<stable-key>-<slug>.md` または既存互換の `YYYY-<slug>.md`
- 年・識別子を欠く題名スラッグ単独の新規ファイルは作らない。
- `paper_path` は一次資料から識別子と発表年を確認してから確定する。
- auditでは既存pathを原則維持する。

## v10 structured transport

research/auditでは完成MarkdownをChatからGitHubへ送らない。固定record bankの5 JSON slotへ構造化recordを書き、Actions側で最終Markdownを生成する。

利用可能bankの正本は `.survey/work-queue/records/bank-registry.json`。現在はA〜Hを事前作成している。

各bankのslot:

- `metadata.json`
- `problem_method.json`
- `evaluation.json`
- `results.json`
- `positioning.json`

GitHubへ直接slotを書き始める前に、可能なら:

```bash
python .survey/scripts/select_record_bank.py --repo-root .
```

を実行し、`selected_bank`を使う。見た目だけでbankの再利用可否を推測しない。

## 通常の論文worker

1. 最新HEADのrouter、queue、continuation policy、fallback policy、next-jobs、paper templateを読む。
2. Drive pending、Library pending、GitHub fallback-inboxを可能な範囲で確認し、`checkpointed_job_ids` とoffline seed由来の未処理候補を把握する。
3. GitHub readyからcheckpoint済みjobを除外し、actionable research/audit/discoveryをpriority順に処理する。
4. research/auditは一次資料全文を読み、5-slot recordを作成して品質検査する。
5. GitHub writeが正常なら選択bankへ5 slot→`chat-inbox.json`の順に反映し、Actions resultと最新queueで完了確認する。
6. 直接反映できない場合は [fallback-routing.md](fallback-routing.md) に従い、完全logical payloadをDriveまたはLibraryの生きているoutboxへ1 envelopeで保存する。元jobはGitHub上では未完了のままにする。
7. 完成・blocked・checkpoint後は最新queueとbacklog indexを取り直し、次の独立作業へ進む。
8. checkpoint済みreadyだけでqueueが塞がれているがGitHub writeは復旧している場合、`.survey/work-queue/transport/request-jobs.json` でそれらをstatus変更せず一時除外し、discoveryを追加発行する。
9. GitHub writeがrun-wideで停止していても、fallbackが書き込み可能ならoffline job seedを保存して新規discovery→researchを続ける。
10. 固定件数・固定バッチ数は設けない。終了前にStop Gateを評価する。

## GitHub write不能中のspillover

GitHub writeが使えずactionable readyを処理し終えた場合でも研究を止めない。候補0〜5件を探索し、`.survey/work-queue/transport/offline-job-seed.json` を書くtransport envelopeとしてDriveまたはLibraryへ耐久保存する。

candidate keyから将来のresearch job IDを決定論的に計算するため、GitHub jobがまだ存在しなくても同じrunでその候補を精読できる。完成した5-slot research payloadも同じjob IDでoutboxへ保存する。

復旧時にseedとresearchが別outboxへ分散しても問題ない。research envelopeは対応jobがGitHubに実体化するまでGitHub fallback-inboxでdependency待ちする。

## multi-outbox recovery

外部outboxから固定record bankや`chat-inbox.json`へ直接replayしない。DriveとLibraryの両方が復旧した場合も、まず各envelopeを次へ送る。

`.survey/work-queue/fallback-inbox/<envelope-id>.json`

- Drive pendingは `.github/workflows/drive-outbox-import.yml` / `.survey/scripts/import_drive_outbox_v4.py` がintakeする。
- Library pendingはScheduled ChatがGitHub write可能なrunでintakeする。
- `.survey/scripts/dispatch_fallback_inbox.py` がsurvey-helperの共通concurrency group内でeligible envelopeを1件ずつ固定transportへ展開する。
- 処理済みenvelopeは `.survey/work-queue/fallback-archive/` に残り、Drive/Library間のglobal dedupe ledgerになる。

同じ`id`のpayloadが複数outboxに存在しても、GitHub fallback-inbox/archiveの同一内容を確認できれば再展開せずsource copyをprocessedにできる。内容不一致ならID衝突としてfailedへ隔離し、上書きしない。

外部outboxの`processed`は「GitHub immutable intakeへの受領済み」を意味し、paper publication完了とは区別する。publication完了はActions result + latest queueで判定する。

## fallback保存先

### Google Drive

`/Google Drive/llm-paper-summary-outbox/pending/`

`GOOGLE_SERVICE_ACCOUNT_JSON` が未設定の間はImporterがidleでも、pending保存自体は有効な耐久checkpointである。設定・復旧後に順次GitHub intakeへ送る。

### ChatGPT Library

`/LLM-survey-outbox/pending/`

Library pendingはScheduled Chatが回収する。GitHub intake成功後にだけ`processed`へ移す。不正payloadは`failed`へ隔離する。

詳細は [fallback-routing.md](fallback-routing.md)、[drive-outbox.md](drive-outbox.md)、[backlog-resilience.md](backlog-resilience.md)。

## 08:30 JST

08:30だけは論文queueに触れず、[worker-router.md](worker-router.md) のその他更新workerに従う。フレームワーク更新と新規LLM公開を確認し、既存の固定 `update-payload.json` + `update-inbox.json` transportを使う。直接反映できない場合は同じmulti-outbox fallback policyを適用し、復旧時もGitHub immutable intakeを経由する。
