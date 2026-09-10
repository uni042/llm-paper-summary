# 研究サーベイ運用手順

現在の正本は **workflow v10（structured-record transport + queue + multi-outbox fallback）**。Scheduled Chat workerは毎回default branch最新HEADを取得し、同じHEADの [worker-router.md](worker-router.md)、[queue-v10.md](queue-v10.md)、[continuation-policy.json](continuation-policy.json)、[fallback-routing.md](fallback-routing.md)、`.survey/work-queue/next-jobs.json` を読む。

## 設計原則

- **Chat研究worker**: 一次資料探索、全文精読、科学的判断、正式監査、構造化research record作成。
- **GitHub Actions worker**: record検証、Markdownレンダリング、paper反映、job/state遷移、identity delta、派生view更新、通常job生成。
- GitHub repositoryを唯一の正本とする。
- Google DriveとChatGPT Libraryは一時配送outboxであり、研究・paper・queueの正本にはしない。
- Notionは使用しない。
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

GitHubへ直接slotを書き始める前に、可能なら次を実行する。

```bash
python .survey/scripts/select_record_bank.py --repo-root .
```

`selected_bank` を使い、見た目だけでbankの再利用可否を推測しない。完全payloadが外部outboxへ耐久保存済みなら、そのbankは成果の唯一コピーではないため後続研究を拘束しない。

## 通常の論文worker

1. 最新HEADのrouter、queue、continuation policy、fallback policy、next-jobs、paper templateを読む。
2. Drive pendingとLibrary pendingを可能な範囲で確認し、`checkpointed_job_ids` とoffline seed由来の未処理候補を一時的に把握する。
3. GitHub readyからcheckpoint済みjobを除外し、実行可能なresearch/audit/discoveryをpriority順に処理する。
4. research/auditは一次資料全文を読み、5-slot recordを作成して品質検査する。
5. GitHub writeが正常なら選択bankへ5 slot→`chat-inbox.json`の順に反映し、Actions resultと最新queueで完了確認する。
6. 直接反映できない場合は [fallback-routing.md](fallback-routing.md) に従い、完全logical payloadをDriveまたはLibraryの生きているoutboxへ1 envelopeで保存する。元jobはGitHub上では未完了のままにする。
7. 完成・blocked・checkpoint後は最新queueとbacklog indexを取り直し、次の独立作業へ進む。
8. GitHub readyがcheckpoint済みjobだけで塞がれているがGitHub writeは復旧している場合、`.survey/work-queue/transport/request-jobs.json` でcheckpoint済みjobを一時除外してdiscoveryを追加発行できる。
9. GitHub writeがrun-wideで停止している場合でも、fallbackが書き込み可能ならoffline job seedを保存して新規discovery→researchを続ける。
10. 固定件数・固定バッチ数は設けない。終了前にStop Gateを評価する。

## GitHub write不能中のspillover

GitHub writeが使えず、既存の実行可能readyを処理し終えた場合でも研究を止めない。候補0〜5件を探索し、`.survey/work-queue/transport/offline-job-seed.json` を書くtransport envelopeとしてDriveまたはLibraryへ耐久保存する。

candidate keyから将来のresearch job IDを決定論的に計算するため、GitHub jobがまだ存在しなくても同じrunでその候補を精読できる。完成した5-slot research payloadも同じjob IDでoutboxへ保存する。

GitHub復旧後は `.survey/scripts/apply_offline_job_seed.py` がseedからcanonical ready jobを生成する。Drive importerおよびLibrary replayはresearch payloadのjobがGitHubに実体化するまでそのpayloadをpendingに残す。

これにより、GitHub write障害が長時間続いても次の流れを繰り返せる。

```text
GitHub read
   │
   ├─ actionable ready ── research ──┐
   │                                 │
   └─ readyなし ─ discovery ─ seed ─┤
                                     ▼
                         Drive または Library outbox
                                     │
                         GitHub write復旧後に再投入
                                     │
                                     ▼
                         GitHub Actions → paper/queue
```

## fallbackの所有権

### Google Drive

保存先: `/Google Drive/llm-paper-summary-outbox/pending/`

Drive pendingは `.github/workflows/drive-outbox-import.yml` が回収する。`GOOGLE_SERVICE_ACCOUNT_JSON` が未設定の間はImporterがidleでも、pending保存自体は有効な耐久チェックポイントである。認証設定後に順次排出する。

### ChatGPT Library

保存先: `/LLM-survey-outbox/pending/`

Library pendingはScheduled Chat自身が回収する。GitHub writeが利用可能なrunで依存を満たす最古のpayloadから再投入し、GitHub側で反映完了を確認してから`processed`へ移す。

Drive pendingをChatから手動二重投入しない。Library pendingをDrive importerは処理しない。各payloadは最初に保存成功したoutboxが排出責任を持つ。

詳細は [fallback-routing.md](fallback-routing.md)、[drive-outbox.md](drive-outbox.md)、[backlog-resilience.md](backlog-resilience.md)。

## 08:30 JST

08:30だけは論文queueに触れず、[worker-router.md](worker-router.md) のその他更新workerに従う。フレームワーク更新と新規LLM公開を確認し、既存の固定 `update-payload.json` + `update-inbox.json` transportを使う。直接反映できない場合は同じmulti-outbox fallback policyを適用する。
