# Queue-based survey workflow v10

ワークフローv10（workflow v10）は、GitHub `main` を唯一の正本としてqueue・state・paper identityを管理し、Scheduled Chat / Work workerはDiscovery、一次資料全文取得、科学的判断、Audit判断、5-slot structured research record作成を担当する。

この文書はqueueとtransportの契約を定義する。実行順・停止判定・fallback選択は、`worker-router.md`、`always-on-worker.md`、`claim-serial-policy.md`、`fallback-routing.md`、`continuation-policy.json`、`backlog-resilience.md` を優先する。

## 1. Queue policy

- ready jobはpriority順に処理する。
- Research / Audit workerは未完了claimを同時に1件だけ持つ。
- 完全payloadをimmutable submissionまたはLibrary checkpointへ耐久保存したら、Actionsのterminal反映を同期的に待たず最新queue / claim stateを再取得する。
- actionable readyが尽きたらDiscoveryへ移る。
- Discovery submissionのcandidate数にアプリケーション上の固定上限を設けない。
- 固定の日次件数、固定batch数、固定Research/Audit比率、最低Research完了件数を設けない。
- fallback backlog、record bank枯渇、単一job失敗、Actions待ち、探索枯渇は正常run終了理由にしない。

GitHub上でreadyでも、完全payloadがGitHubへ耐久保存済み、またはChatGPT Libraryへcheckpoint済みなら、同じrunで再精読しない。

## 2. Ownership and Actions lanes

### Scheduled Chat / Work

- 文献探索（literature discovery）
- 一次資料取得と全文精読
- 科学的判断・監査判断
- 重複の事前確認
- 5-slot structured research record作成
- claim結果で予約されたrecord bankへの書込み
- attempt固有immutable descriptor作成
- GitHub write不能時のChatGPT Library checkpoint

### GitHub Actions

- structured record検証
- 決定論的Markdown生成
- paper公開・更新
- job/state遷移
- identity delta維持
- 重複抑止
- fallback replay
- 派生view、citation、maintenance

Actionsは`survey-claim-main`、`survey-submission-main`、`survey-background-main`に分離する。claim / submission fast laneはbackground laneの完了を同期障壁にしない。

## 3. Duplicate prevention

candidate提出前とResearch着手前に次を照合する。

1. `.survey/survey-state/paper-identity-index.json`
2. `.survey/survey-state/identity-deltas/**/*.json`
3. `papers/inference/**`、`papers/training/**`、`papers/survey/**`
4. `.survey/work-queue/jobs/*.json`
5. GitHub fallback-inbox/archiveと、確認可能なChatGPT Library pending

canonical ID / arXiv ID / DOI / OpenReview IDを優先し、最後にnormalized titleを使う。GitHub code searchだけで未登録判定をしない。

## 4. Research quality

一次資料本文を最後まで読む。全文取得不能ならcompletedとして送らずblocked/deferredとして扱う。抄録・検索断片から欠落情報を推測しない。

本文品質は `.survey/templates/paper.md` を正本とする。structured recordは内部メモではなく最終Markdownの原稿である。GitHubまたはLibraryへ耐久保存する前にActions側と同じvalidator基準でpreflightする。

## 5. Structured record banks

利用可能bankの正本は `.survey/work-queue/records/bank-registry.json`。各bankは次の5 slotを持つ。

- `metadata.json`
- `problem_method.json`
- `evaluation.json`
- `results.json`
- `positioning.json`

通常Research/Auditではclaim resultの `record_bank` が正本である。workerが別bankを選び直してはならない。`record_bank: null` かつ `record_bank_fallback: "library"` の場合はLibraryへ完全payloadをcheckpointする。

各slot envelopeは`schema_version`、`transport_version: 10`、`slot`、`attempt_id`、`job_id`、`data`を含む。

`metadata.json`では少なくとも正規識別子、題名、要約、著者、`published`、`publication`、`publication_type`、`publication_status`、`sources`、`implementation`、`code`、`last_checked`を保存する。一次論文のreference sectionも確認し、`references`、`references_checked_at`、`references_source`、`references_total`を保存する。

## 6. Immutable Research/Audit submission

新規Research/Auditでは固定 `.survey/work-queue/submissions/chat-inbox.json` を使わない。

1. claimで得た`attempt_id`と予約bankを使う。
2. `metadata → problem_method → evaluation → results → positioning`の順で5 slotを書く。
3. 各slotの実Git blob SHAを取得する。
4. 5 slotがすべて耐久保存された後だけattempt固有descriptorを作る。

Research descriptorは `.survey/work-queue/submissions/research/<attempt-id>.json`、Audit descriptorは `.survey/work-queue/submissions/audit/<attempt-id>.json` に保存する。既存paper更新時は`expected_blob_sha`を含める。

`survey-submission-fast`は未解決descriptorを安全にdrainし、複数descriptorを並列検証した後、正本状態への副作用を決定論的に統合する。同じattemptの再実行は同じresultへ冪等に収束する。

未解決descriptorが参照するbankはoccupiedである。matching success result、または安全な耐久状態が確認されるまで別attemptが上書きしてはならない。

## 7. Normal save protocol

通常の直列ループは次である。

`1件claim → 全文精読 → 5-slot record → preflight → immutable descriptor/Library checkpoint → 最新queue/claim state → 次の1件claim`

- descriptorをGitHubへ耐久保存した時点でworker内では送信済みとみなす。
- submission-fastのterminal反映を待たない。
- matching resultは後で確認する。
- descriptorが失敗resultになっても、失敗状態が解決されるまで同attempt/bankの所有関係を壊さない。
- 前jobの完全payloadが未保存のまま次jobをclaimしない。

## 8. Discovery submission

探索主体workerのmulti-round Discoveryは、pre-issued Discovery jobに依存しない自己記述型round submission（self-describing round submission）を正規経路とする。

各roundは `.survey/work-queue/submissions/*.json` に独立したimmutable fileとして保存し、少なくとも次を含める。

- `operation: "submit_discovery_round"`
- `candidates`: **固定件数上限なし**
- `discovery_stats.run_key`
- `discovery_stats.round`
- `discovery_stats.axis`

この形式では `job_id` を付けない。workerが存在しない `job-discovery-specialist-*` 等を合成してはならない。`queue_worker.py` はsubmission pathからdeterministicな内部Discovery ingest jobを作り、candidateを最終dedupeし、採用候補だけをworkflow v10 Research jobへmaterializeする。

candidate数は1、5、12、50、100など任意でよい。quality基準を満たすcandidateを固定件数へ切り詰めない。外部API/GitHub/Libraryの実payloadサイズ制約で単一fileが保存不能な場合だけ複数immutable submissionへ分割し、総candidateを失わない。

通常workerが実在するready Discovery jobを処理する従来形式は互換として維持する。legacy synthetic/unknown `job_id` を持つself-describing roundは `recover_discovery_submissions.py` がdeterministic ingest経路へ収束させる。Research/Auditのunknown job IDはDiscovery救済へ流さない。

`.survey/scripts/queue_worker.py` は新規Research/Audit jobを最初からworkflow v10 `structured_record_v10`契約で作る。過去のroot-level完成Markdown submissionは履歴互換としてのみ読む。

## 9. Library fallback

GitHub direct write不能時の正本は `fallback-routing.md`。外部fallbackはChatGPT Library `/LLM-survey-outbox/pending/<id>.json` とする。

Research/Audit fallbackは1論文につき1 envelopeへroot-level `kind`、`job_id`、`claim_id`、`worker_id`、`attempt_id`、`depends_on_job_ids`、`paper_path`と完全な5 record slotを含める。

Libraryから復旧したenvelopeは `.survey/work-queue/fallback-inbox/<envelope-id>.json` へimmutable envelopeとして送り、`replay_record_fallback.py` が安全なbankへslotをmaterializeし、attempt固有descriptorへ変換する。

## 10. Offline Discovery

GitHub write不能中でもLibraryが書けるならDiscoveryを止めない。offline discovery seedのcandidate配列にも固定件数上限を設けない。そのroundで得られた強いcandidateをすべて完全envelopeとして保存する。

Library/APIの実payloadサイズ上限に当たる場合は複数seed envelopeへ分割してよいが、総candidateを切り捨てない。seed保存後はjob実体化を同期的に待たず、同じrunで候補をResearchへ進めて完全Research fallbackを保存してよい。

## 11. Transport integrity

- Scheduled Chatからpaper/state/README/identity/queueを直接編集しない。
- fallback envelopeから`papers/**`やworkflow/scriptを直接書かない。
- immutable descriptorは作成後に書き換えない。修正は新attemptで行う。
- completionはimmutable result + latest queueで確認する。
- 同一payloadの再処理は同attempt/resultへ冪等に収束させる。
- pending/replay失敗、bank枯渇、1本処理完了、Actions待ち、candidate数、探索枯渇は正常run終了理由にしない。

## 12. Paper family routing

Research開始時点で保存先をInference / Training / Surveyから明示判定する。Surveyは既存研究群の分類・比較・体系化が主目的、Inferenceは推論・serving・decoding・KV cache・offload・MoE実行等、Trainingは学習・fine-tuning・optimizer・学習時offload等を主とする。Surveyを `papers/inference/**` へ保存しない。

## 13. Claim transport

claim requestは `.survey/work-queue/claim-requests/` のJSONとして送る。`survey-claim-fast` は同じ直列化区間でjob ownershipとrecord bankを確定する。

- default `max_jobs = 1`
- default lease = 90分（5400秒）
- eligible = ready Research/Auditのみ
- expired claimは履歴として残るがactiveではない
- heartbeatは同じrequest/workerで新しいUTC `requested_at`を使う
- claim resultの`record_bank` / `record_bank_fallback`をworkerが上書きしない
- Library checkpoint済みjobは`checkpointed_jobs`で同workerの再精読対象から外せる

`max_jobs = 1` はcandidate受入上限ではなく、同一workerの未完了Research/Audit claimを直列化する安全不変条件である。詳細は `claim-serial-policy.md` を正本とする。
