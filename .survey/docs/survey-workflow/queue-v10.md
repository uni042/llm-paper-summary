# Queue-based survey workflow v10

workflow v10は、GitHubを唯一の正本としてqueue/state/identityをGitHub Actions側で管理し、Scheduled Chatは探索、一次資料全文取得、科学的判断、監査判断、構造化research record作成を担当する。

この文書はqueueとtransportの契約を定義する。実行順・停止判定・fallback選択は重複定義せず、次を正本とする。

1. `worker-router.md`
2. `always-on-worker.md`
3. `claim-serial-policy.md`
4. `fallback-routing.md`
5. `continuation-policy.json`
6. `backlog-resilience.md`
7. `.survey/templates/paper.md`
8. `.survey/work-queue/records/bank-registry.json`

## 1. Queue policy

- ready jobはpriority順に処理する。
- job処理、blocked化、checkpoint後は最新queueを再取得する。
- actionable readyが尽きたらdiscoveryを行う。
- discovery候補0〜5件は1 submissionのtransport上限であり、run全体の上限ではない。
- research後、追加の一次資料確認が明確に必要な場合だけauditを生成する。
- 固定の日次件数、固定batch数、固定research/audit比率は設けない。
- fallback backlog、record bank exhaustion、単一job失敗、Actions terminal待ちはrun終了理由にしない。

GitHub上でreadyでも、完全payloadがGitHubのimmutable submissionとして耐久保存済み、またはChatGPT Libraryへcheckpoint済みなら、そのjobは同じrunで再精読しない。

Google Drive fallbackは廃止済み。新規fallbackはChatGPT Libraryのみを使う。

## 2. Ownership and lanes

### Scheduled Chat / Work

- literature discovery
- primary-source retrieval
- full-text reading
- scientific judgment
- formal audit judgment
- duplicate pre-check
- structured research record authoring
- record slot / immutable descriptor transport
- GitHub write不能時のChatGPT Library checkpoint

### GitHub Actions

- structured record validation
- deterministic Markdown rendering
- paper publication/update
- job/state transition
- identity delta maintenance
- duplicate suppression
- derived-view rebuild
- fallback replay

GitHub Actionsは次の3レーンに分離する。

- `survey-claim-main`: claim割当と軽量`next-jobs.json`更新だけを行う高速レーン。
- `survey-submission-main`: 明示的に送られたimmutable research/audit descriptorだけを処理する高速レーン。
- `survey-background-main`: fallback、dedupe、blocked retry、maintenance、citation、index等の重い処理を行うbackgroundレーン。

claimとimmutable submissionはbackgroundの完了を待たない。

## 3. Duplicate prevention

候補提出前とresearch着手前に次を照合する。

1. `.survey/survey-state/paper-identity-index.json`
2. `.survey/survey-state/identity-deltas/**/*.json`
3. `papers/inference/**` と `papers/survey/**` の既収録論文
4. `.survey/work-queue/jobs/*.json`
5. ChatGPT Library / GitHub fallback-inbox上のseedとcheckpoint済みjob

canonical ID / arXiv ID / DOI / OpenReview IDを優先する。GitHub code searchだけで未登録判定をしない。

## 4. Research quality

一次資料本文を最後まで読む。全文取得不能ならcompletedとして送らず、blocked/deferredとして扱う。抄録・検索断片から欠落情報を推測しない。

本文品質は `.survey/templates/paper.md` を正本とする。構造化recordは内部メモではなく、人間向けMarkdownへ変換する原稿である。特に`problem_method`は、入力、観測状態、処理、出力、前後接続、なぜ効くか、追加コスト、失敗条件が追える量を書く。

GitHubへ送る前、またはLibraryへcheckpointする前にActions側と同じvalidator基準でpreflightする。基準未達recordは完成扱いにしない。

## 5. Structured record banks

利用可能なrecord bankは `.survey/work-queue/records/bank-registry.json` を正本とする。通常構成はA〜Hで、各bankに次の5 slotを持つ。

- `metadata.json`
- `problem_method.json`
- `evaluation.json`
- `results.json`
- `positioning.json`

GitHubへslotを書き始める前に可能なら次を使う。

```bash
python .survey/scripts/select_record_bank.py --repo-root .
```

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

`metadata.json`では少なくとも正規識別子、題名、要約、著者、`published`、`publication`、`publication_type`、`publication_status`、`sources`、`implementation`、`code`、`last_checked`を保存する。公式コードが確認できない場合も`code: null`を明示する。

arXiv論文は主カテゴリと横断登録カテゴリを分離する。

```json
"arxiv_categories": {
  "primary": "cs.LG",
  "cross_list": ["cs.AI"]
}
```

一次論文のreference sectionも確認し、正規化した`references`、`references_checked_at`、`references_source`、`references_total`を保存する。

## 6. Immutable research/audit submission

新規の通常Research/Audit完了payloadでは、固定 `.survey/work-queue/submissions/chat-inbox.json` を更新しない。

5 slotをすべてGitHubへ書き、その実際のGit blob SHAを取得した後、attempt固有のimmutable descriptorを1個だけ作る。

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

既存paperを更新する場合は`expected_blob_sha`も入れる。

`survey-submission-fast`はtriggerになったdescriptorだけを処理する。過去のsubmission全件を走査して処理してはならない。同じdescriptorの再実行はimmutable resultへ冪等に収束する。

resultは次に保存される。

- `.survey/work-queue/results/research/<attempt-id>.json`
- `.survey/work-queue/results/audit/<attempt-id>.json`

未解決descriptorが現在のattemptを参照しているbankはoccupiedであり、別workerが上書きしてはならない。matching resultが作成されるとそのbankは再利用可能になる。

## 7. Normal save protocol

1. claimから得た`attempt_id`を使う。
2. bank selectorで空きbankを1つ選ぶ。
3. `metadata → problem_method → evaluation → results → positioning`の順でslotを書く。
4. 各slotの最新Git blob SHAを取得する。
5. 5 slot成功後だけ、attempt固有immutable descriptorを新規作成する。
6. descriptorがGitHubへ耐久保存できた時点で、そのjobはworker内では送信済みとみなす。
7. **submission-fastのterminal反映を待たず**、最新queue/claim stateを再取得して次の1件をclaimする。
8. matching resultは後で確認する。失敗してもdescriptorとslotは残るため再処理できる。

1 workerが同時に保持する未完了claimは1件だけ。次jobの先取りclaimは禁止するが、前jobのimmutable descriptorを耐久保存した後はActions terminal待ちをしない。

## 8. Discovery / blocked / deferred / rejected

Discoveryや軽量なblocked/deferred transportは従来のroot-level submission経路を利用できる。immutable descriptor fast laneは、主に5-slotを伴うResearch/Auditの完全payload用である。

個別論文の全文取得不能や依存不足は対象jobだけblocked/deferredとし、次の独立作業へ進む。

Scheduled Chatからpaper/state/README/identity/queueを直接編集しない。

## 9. Library fallback and legacy compatibility

GitHub direct writeを完了できない場合の正本は `fallback-routing.md`。保存先はChatGPT Libraryのみ:

`/LLM-survey-outbox/pending/<id>.json`

Libraryへ完全payloadまたはoffline job seedを耐久保存できれば研究を続ける。

移行期間中、既存のLibrary / GitHub fallback envelopeは固定`chat-inbox.json`を含むlegacy replay形式のまま処理してよい。background helperが互換経路を担当する。**新しい通常GitHub Research/Audit送信ではlegacy `chat-inbox.json`を使わない。**

research/audit fallbackは1論文につき1 envelopeに必要な5 slotとsubmission情報をまとめ、1論文を複数fragmentへ分割しない。完成Markdownはfallbackへ保存しない。

Libraryから復旧したenvelopeはまず:

`.survey/work-queue/fallback-inbox/<envelope-id>.json`

へ不変envelopeとして送る。同じ`id`がarchive等にあり内容も同一なら再writeしない。内容不一致は衝突として隔離する。

background helperのfallback replay失敗・待機はclaim-fastやsubmission-fastをブロックしない。

## 10. Offline discovery

GitHub write不能中にactionable readyが尽きてもLibraryが書けるなら探索を続ける。

候補0〜5件を `.survey/work-queue/transport/offline-job-seed.json` に格納するenvelopeとしてLibraryへ保存する。候補のresearch job IDは`fallback-routing.md`の決定論的規則で計算する。

seed保存後はjob実体化を待たず同じrunで候補を精読し、完成research envelopeもLibraryへ保存してよい。復旧時はseedがjobを実体化するまでresearch envelopeをdependency待ちにする。

## 11. Transport integrity

- Scheduled Chatからpaper/state/README/identity/queueを直接updateしない。
- fallback envelopeから`papers/**`やworkflow/scriptを直接書かない。
- immutable descriptorは作成後に内容を書き換えない。修正が必要なら新attemptを使う。
- completionはimmutable result + latest queueで検証する。
- 同一payloadの再処理は同じattempt/resultへ冪等に収束させる。
- pending/replay失敗、bank exhaustion、1本処理完了、Actions待ちはrun終了理由にしない。

## 12. Paper family routing

research開始時点で、論文を **Inference / Training / Survey** のどこへ保存するかを明示的に判定する。`paper_path` はこの判定と一致させる。

- **Survey / サーベイ**: 主目的が複数の既存研究・方式・システムを横断整理し、分類、比較、体系化、研究課題整理を行うsurvey / review / systematic review / tutorial-style overview。
- **Inference / 推論**: 新規手法・システム・アルゴリズムの主目的が推論、serving、decoding、KV cache、offload、MoE実行、on-device実行などの推論効率化である原著論文。
- **Training / 学習**: 学習・fine-tuning・optimizer・activation/parameter/optimizer-state offloadなど学習段階の効率化が主目的。ただし通常サーベイではTraining側の新規追加凍結方針を優先する。

Surveyと判定した論文を `papers/inference/**` へ保存してはならない。保存先は `papers/survey/<survey-lineage>/<filename>.md` とする。

判定が曖昧な場合は、タイトルの`survey` / `review`ではなく、主たる貢献が新規システム提案か既存研究群の体系化かで決める。

## 13. Claim transport

Claim requests are immutable JSON files in `.survey/work-queue/claim-requests/`; `survey-claim-fast` writes one result and one current claim per assigned job.

- default `max_jobs` = 1
- default lease = **90 minutes (5400 seconds)**
- eligible = ready research/audit jobs only
- expired claim files remain on disk as durable history, but are no longer active and do not block a new assignment
- leaseを延長する場合は同じrequest/workerを新しいUTC `requested_at`でheartbeat更新する
- 期限切れ後にworkerがまだ成果をGitHub/Libraryへ耐久保存していない場合は旧claimで新規送信せず、fresh claimを取得し直す
- claimがactiveなのは、`expires_at`が未来で、かつ`released_at`と`lease_invalidated_at`のどちらも存在しない場合だけ。claimファイルは監査履歴として残す。
- immutable Research/Audit resultは、同じjob/attemptに対する`ok: true`だけを成功確定として扱う。`ok: false`はdescriptorを未解決のまま残し、再処理可能とする。
- reusable `chat-inbox.json` resultも、同じjob/attemptに対する`ok: true`だけをsettledとして扱う。失敗resultやattempt不一致resultはpreflight前に再利用しない。
- legacy root-level submissionを`queue_worker.py`で処理する経路は一回限りのprocessing receiptであり、対応resultが存在すれば同じroot submissionを再処理しない。Research/Auditのretryable transportにはimmutable descriptor fast laneを使う。

claim result待ち中に別requestを重ねず、完全payloadの耐久保存後は新しいrequest IDで次jobを1件だけ取得する。
