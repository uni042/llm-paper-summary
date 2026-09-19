# Queue-based survey workflow v10 — 実装リファレンス

ワークフロー v10（workflow v10）は、GitHub `main` を唯一の正本としてキュー（queue）・状態（state）・論文同一性（identity）を管理し、Scheduled Chat / Work workerは探索、一次資料全文取得、科学的判断、監査判断、5スロット構造化研究レコード（five-slot structured research record）作成を担当する。

この文書はキュー（queue）と転送（transport）の**内部実装契約**を定義する。Scheduled Chat / Work ワーカーの実行順・役割分岐・探索・停止判定・fallback選択の唯一の正本は `worker-router.md` であり、この文書を別のワーカー指示として解釈してはならない。

正規スクリプト実行時に stderr へ出る `[WORKER-GUIDE]` は `worker-router.md` に基づく実行時ガイドであり、ワーカーはこれに従う。実装リファレンスの記述を根拠に `[待機]`、`[次]`、`[正しい手順]` を飛ばしてはならない。

実装上の参照順位は次とする。

1. `worker-router.md` — ワーカー行動の正本
2. `continuation-policy.json` — 機械可読設定
3. 本書 — queue / transport内部契約
4. `.survey/templates/paper.md` — 研究レコード品質
5. `.survey/work-queue/records/bank-registry.json` — record bank定義

## 1. Queue policy

- ready jobはpriority順に処理する。
- Research / Audit workerは未完了claimを同時に1件だけ持つ。
- 完全payloadを不変提出（immutable submission）またはLibrary checkpointへ耐久保存したら、Actionsのterminal反映を同期的に待たず最新queue / claim stateを再取得する。
- actionable readyが尽きたらdiscoveryへ移る。
- discovery候補0〜5件は1 submissionの転送上限であり、run全体の上限ではない。
- research後に追加の一次資料確認が明確に必要な場合だけauditを生成する。
- 固定の日次件数、固定batch数、固定research/audit比率は設けない。
- fallback backlog、record bank枯渇、単一job失敗、Actions待ちはrun終了理由にしない。

GitHub上でreadyでも、完全payloadがGitHubへ耐久保存済み、またはChatGPT Libraryへcheckpoint済みなら、同じrunで再精読しない。

## 2. Ownership and Actions lanes

### Scheduled Chat / Work

- 文献探索（literature discovery）
- 一次資料取得と全文精読
- 科学的判断・監査判断
- 重複の事前確認
- 5スロット構造化研究レコード作成
- claim結果で予約されたrecord bankへの書込み
- attempt固有の不変descriptor作成
- GitHub write不能時のChatGPT Library checkpoint

### GitHub Actions

- 構造化record検証
- 決定論的Markdown生成
- paper公開・更新
- job/state遷移
- identity delta維持
- 重複抑止
- fallback replay
- 派生view、citation、maintenance

Actionsは3レーンに分離する。

- `survey-claim-main`: claim割当、record bank予約、軽量queue snapshot。
- `survey-submission-main`: Research/Auditの不変descriptor処理。
- `survey-background-main`: fallback、discovery/control submission、dedupe、blocked retry、citation、index、maintenance等。

claim / submission fast laneはbackground laneの完了を同期障壁にしない。

## 3. Duplicate prevention

候補提出前とresearch着手前に次を照合する。

1. `.survey/survey-state/paper-identity-index.json`
2. `.survey/survey-state/identity-deltas/**/*.json`
3. `papers/inference/**`、`papers/training/**`、`papers/survey/**`
4. `.survey/work-queue/jobs/*.json`
5. GitHub fallback-inbox/archiveと、確認可能なChatGPT Library pending

canonical ID / arXiv ID / DOI / OpenReview IDを優先し、最後にnormalized titleを使う。GitHub code searchだけで未登録判定をしない。

## 4. Research quality

一次資料本文を最後まで読む。全文取得不能ならcompletedとして送らず、blocked/deferredとして扱う。抄録・検索断片から欠落情報を推測しない。

本文品質は `.survey/templates/paper.md` を正本とする。構造化recordは内部メモではなく最終Markdownの原稿である。特に`problem_method`は、入力、観測状態、処理、出力、前後接続、なぜ効くか、追加コスト、失敗条件が追える量を書く。

GitHubまたはLibraryへ耐久保存する前に、Actions側と同じvalidator基準で事前検査（preflight）する。基準未達recordは完成扱いにしない。

## 5. Structured record banks

利用可能bankの正本は `.survey/work-queue/records/bank-registry.json`。通常はA〜Hで、各bankに次の5 slotを持つ。

- `metadata.json`
- `problem_method.json`
- `evaluation.json`
- `results.json`
- `positioning.json`

**通常Research/Auditではclaim resultの `record_bank` が正本である。workerが `select_record_bank.py` で別bankを選び直してはならない。**

- `record_bank: "a"` 等が返った場合、そのbankだけへ書く。
- `record_bank: null` かつ `record_bank_fallback: "library"` の場合、GitHub上で独自に別bankを確保せずLibraryへ完全payloadをcheckpointする。
- `select_record_bank.py` は診断、fallback replay、保守用途のbank状態確認に使う。

各slot envelope:

```json
{
  "schema_version": 1,
  "transport_version": 10,
  "slot": "metadata",
  "attempt_id": "attempt-unique",
  "job_id": "job-...",
  "data": {}
}
```

slot上限、必須field、文章量、日本語優先ルールは `.survey/scripts/assemble_research_record.py` と `.survey/templates/paper.md` を正本とする。

`metadata.json`では少なくとも正規識別子、題名、要約、著者、`published`、`publication`、`publication_type`、`publication_status`、`sources`、`implementation`、`code`、`last_checked`を保存する。一次論文のreference sectionも確認し、`references`、`references_checked_at`、`references_source`、`references_total`を保存する。

## 6. Immutable Research/Audit submission

新規の通常Research/Auditでは固定 `.survey/work-queue/submissions/chat-inbox.json` を使わない。

1. claimで得た`attempt_id`と予約bankを使う。
2. `metadata → problem_method → evaluation → results → positioning`の順で5 slotを書く。
3. 各slotの実際のGit blob SHAを取得する。
4. 5 slotがすべて耐久保存された後だけattempt固有descriptorを作る。

- Research: `.survey/work-queue/submissions/research/<attempt-id>.json`
- Audit: `.survey/work-queue/submissions/audit/<attempt-id>.json`

例:

```json
{
  "schema_version": 1,
  "transport_version": 10,
  "kind": "research",
  "attempt_id": "attempt-...",
  "job_id": "job-research-...",
  "claim_id": "claim-...",
  "worker_id": "scheduled-chat-...",
  "record_bank": "a",
  "paper_path": "papers/inference/.../paper.md",
  "record_slots": [
    {"slot": "metadata", "path": ".survey/work-queue/records/chat-record/metadata.json", "blob_sha": "..."},
    {"slot": "problem_method", "path": ".survey/work-queue/records/chat-record/problem_method.json", "blob_sha": "..."},
    {"slot": "evaluation", "path": ".survey/work-queue/records/chat-record/evaluation.json", "blob_sha": "..."},
    {"slot": "results", "path": ".survey/work-queue/records/chat-record/results.json", "blob_sha": "..."},
    {"slot": "positioning", "path": ".survey/work-queue/records/chat-record/positioning.json", "blob_sha": "..."}
  ]
}
```

既存paperを更新する場合は`expected_blob_sha`を含める。

`survey-submission-fast`は未解決descriptorを安全にdrainし、現在の実装では複数descriptorを並列検証した後、正本状態への副作用を決定論的に統合する。同じattemptの再実行は同じresultへ冪等に収束する。

result:

- `.survey/work-queue/results/research/<attempt-id>.json`
- `.survey/work-queue/results/audit/<attempt-id>.json`

未解決descriptorが参照するbankはoccupiedである。matching success result、または安全な耐久状態が確認されるまで別attemptが上書きしてはならない。

## 7. Normal save protocol

通常の直列ループ:

`1件claim → 全文精読 → 5-slot record → preflight → immutable descriptor/Library checkpoint → 最新queue/claim state → 次の1件claim`

- descriptorをGitHubへ耐久保存した時点でworker内では送信済みとみなす。
- submission-fastのterminal反映を待たない。
- matching resultは後で確認する。
- descriptorが失敗resultになっても、失敗状態が解決されるまで同attempt/bankの所有関係を壊さない。
- 前jobの完全payloadが未保存のまま次jobをclaimしない。

## 8. Discovery and compatibility submissions

> ここにある互換記述はバックエンドの履歴読込専用であり、新規ワーカーが選択できる経路ではない。新規Discovery requestは `worker-router.md` に従いschema v3 fixed-source precheckだけを使う。

Discovery、discovery統計、checkpoint-aware job request、offline seed等の軽量control transportはbackground laneで処理できる。

探索主体workerのmulti-round Discoveryは、pre-issued Discovery jobに依存しない **self-describing round submission** を正規経路とする。各roundは `.survey/work-queue/submissions/*.json` に独立したimmutable fileとして保存し、少なくとも次を含める。

- `operation: "submit_discovery_round"`
- `candidates`: 0〜5件
- `discovery_stats.run_key`
- `discovery_stats.round`
- `discovery_stats.axis`

この形式では `job_id` を付けない。workerが存在しない `job-discovery-specialist-*` 等を合成してはならない。`queue_worker.py` はsubmission pathからdeterministicな内部Discovery ingest jobを作り、candidateを最終dedupeし、採用候補だけをworkflow v10のResearch jobへmaterializeする。内部ingest jobはworker-facing Discovery laneとは分離されるため、同一runの次roundは新しいDiscovery jobのmaterializeを待たず送信できる。

通常workerが実在するready Discovery jobを処理する従来形式は互換として維持する。さらに、過去にself-describing roundがsynthetic/unknown `job_id` またはterminal Discovery jobを参照して失敗済みの場合、`recover_discovery_submissions.py` は同じdeterministic ingest経路へ安全に収束させる。`discovery_stats` を持たないlegacy候補payloadは、元の実在terminal Discovery jobが確認できる場合に限り旧recovery経路で救済する。Research/Auditのunknown job IDはDiscovery救済へ流さず拒否する。

`.survey/scripts/queue_worker.py` は新規Research/Audit jobを最初からworkflow v10の`structured_record_v10`契約で作る。後段でv9 jobをv10へ書き換える正規化処理は現行経路に存在しない。

過去に作られたroot-levelの「完成Markdownを返す」Research/Audit submissionは履歴互換として読み込めるが、**新規workerがその形式を生成してはならない。**

## 9. Library fallback and legacy read compatibility

> legacy read compatibilityは既存履歴の救済専用である。新規ワーカーは旧形式を生成しない。

GitHub direct write不能時の正本は `worker-router.md`。外部fallbackはChatGPT Libraryのみ:

`/LLM-survey-outbox/pending/<id>.json`

新規Research/Audit fallbackは、1論文につき1 envelopeへ次を含める。

- root-levelの`kind`、`job_id`、`claim_id`、`worker_id`、`attempt_id`、`depends_on_job_ids`、`paper_path`
- 完全な5 record slot

新規fallbackは固定`chat-inbox.json`を含めない。

Libraryから復旧したenvelopeはまず `.survey/work-queue/fallback-inbox/<envelope-id>.json` へ不変envelopeとして送る。Research/Audit bundleは `.survey/scripts/replay_record_fallback.py` が安全なbankへslotをmaterializeし、attempt固有のimmutable descriptorへ変換する。replayでも固定`chat-inbox.json`を再生成しない。

2026-09-14以前に保存済みの「5 slot + `chat-inbox.json`」bundleは、既存pending救済のため**読込互換だけ**残す。legacy chat payloadから不足するmetadataを読み出した後は、同じ現行descriptor経路へ収束させる。

## 10. Offline discovery

GitHub write不能中でもLibraryが書けるなら探索を止めない。候補0〜5件をoffline seed envelopeとしてLibraryへ保存できる。

seed保存後はjob実体化を同期的に待たず、同じrunで候補を精読して完全Research fallbackを保存してよい。復旧時にcanonical jobが未実体化ならResearch envelopeはdependency待ちとする。

## 11. Transport integrity

- Scheduled Chatからpaper/state/README/identity/queueを直接編集しない。
- fallback envelopeから`papers/**`やworkflow/scriptを直接書かない。
- immutable descriptorは作成後に書き換えない。修正は新attemptで行う。
- completionはimmutable result + latest queueで確認する。
- 同一payloadの再処理は同attempt/resultへ冪等に収束させる。
- pending/replay失敗、bank枯渇、1本処理完了、Actions待ちはrun終了理由にしない。

## 12. Paper family routing

research開始時点で保存先を **Inference / Training / Survey** から明示判定する。

- **Survey / サーベイ**: 既存研究群の分類、比較、体系化、課題整理が主目的。
- **Inference / 推論**: 推論、serving、decoding、KV cache、offload、MoE実行、on-device等の新規手法・システム。
- **Training / 学習**: 学習、fine-tuning、optimizer、学習時offload等。ただし通常サーベイではTraining新規追加凍結方針を優先する。

Surveyを `papers/inference/**` へ保存してはならない。判定はタイトル語ではなく主たる貢献で決める。

## 13. Claim transport

claim requestは `.survey/work-queue/claim-requests/` のJSONとして送る。`survey-claim-fast` は同じ直列化区間でjob ownershipとrecord bankを確定する。

- default `max_jobs` = 1
- default lease = 90分（5400秒）
- eligible = ready Research/Auditのみ
- expired claimは履歴として残るがactiveではない
- heartbeatは同じrequest/workerで新しいUTC `requested_at`を使う
- claim resultの`record_bank` / `record_bank_fallback`をworkerが上書きしない
- Library checkpoint済みjobは`checkpointed_jobs`で同workerの再精読対象から外せる

詳細は `worker-router.md` を正本とする。
