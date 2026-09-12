# Queue-based survey workflow v10

workflow v10は、GitHub mainを唯一の正本としてqueue / state / identityをGitHub Actions側で管理し、Scheduled Chatは探索、一次資料全文取得、科学的判断、監査判断、構造化research record作成を担当する。

本書は **queueとstructured transportの契約** を定義する。別事項の正本は重複定義しない。

- 時刻routing / maintenance: `worker-router.md`
- 通常runの継続・Actions待ち・可視queue: `always-on-worker.md`
- candidate水位: `candidate-buffer-policy.md`
- discovery継続・停止: `discovery-continuation-policy.md` / `discovery-exhaustive-run-policy.md`
- fallback / replay: `fallback-routing.md`
- run全体のSTOP判定: `continuation-policy.json`
- backlog耐性: `backlog-resilience.md`
- 本文品質: `.survey/templates/paper.md`
- record bank構成: `.survey/work-queue/records/bank-registry.json`

## 1. Queue policy

- ready jobはpriority順に処理する。
- `.survey/work-queue/next-jobs.json` は優先スナップショットであり、全ready job一覧ではない。countsに表示外readyがある場合は `.survey/work-queue/jobs/*.json` を確認する。
- job処理、blocked化、checkpoint後は最新queue/backlogを再取得する。
- candidate水位がlow/critical watermark未満なら、readyが残っていても `candidate-buffer-policy.md` に従ってdiscovery補充を並行する。
- actionable readyがなく、spilloverもなければdiscoveryする。
- 1 discovery submissionのcandidateは0〜5件。5件はノルマでもrun全体の上限でもない。
- research後、追加の一次資料確認が明確に必要な場合だけauditを生成する。
- 固定の日次件数、固定research/audit件数、固定discovery round数、固定batch数は設けない。
- fallback backlog、record bank exhaustion、単一job失敗、Actions反映待ちはrun終了理由にしない。

GitHub上でreadyでも、完全payloadがChatGPT LibraryまたはGitHub fallback-inbox/archiveへ耐久checkpoint済みなら、そのjobは再精読しない。通常runの継続は `always-on-worker.md` を正本とする。

Google Drive fallback、Notion、旧 `/LLM-survey-fallback/` は新規保存・replay・backlog判定に使わない。

## 2. Ownership

### Scheduled Chat

- literature discovery
- primary-source retrieval
- full-text reading
- scientific judgment
- formal audit judgment
- duplicate pre-check
- structured research record authoring
- normal GitHub transport
- GitHub write不能時のChatGPT Library checkpoint
- Library pendingのGitHub immutable intakeへの回収

### GitHub Actions

- structured record validation
- deterministic Markdown rendering
- paper publication/update
- job/state transition
- identity delta maintenance
- final duplicate suppression
- `discovery-state.json` の単一writer
- derived-view rebuild
- offline job seed materialization
- GitHub fallback-inboxの直列dispatch

Scheduled Chatからpaper / queue / state / identity / README / `discovery-state.json` を直接更新しない。

## 3. Duplicate prevention

候補提出前とresearch着手前に、可能な範囲で次を照合する。

1. `.survey/survey-state/paper-identity-index.json`
2. `.survey/survey-state/identity-deltas/**/*.json`
3. `papers/inference/**` と `papers/survey/**` の既収録論文
4. `.survey/work-queue/jobs/*.json`
5. ChatGPT Library / GitHub fallback-inbox/archive上のseed・checkpoint済みjob

canonical ID / arXiv ID / DOI / OpenReview IDを優先し、最後にnormalized titleを使う。GitHub code searchだけで未登録判定しない。Actions側のdedupeを最終防衛線とするが、意図的な重複jobは作らない。

## 4. Research quality

一次資料本文を最後まで読む。全文取得不能ならcompletedにせず、対象jobだけblocked/deferredとする。抄録・検索断片から欠落情報を推測しない。

本文品質は `.survey/templates/paper.md`、監査詳細は `paper-quality-audit.md` を正本とする。構造化recordは内部メモではなく、人間向けMarkdownへ変換する原稿であり、rendererが内容を補う前提で短縮しない。

新規v10 recordでは `metadata.list_summary` を精読workerが一覧専用短文として独立生成する。`## 概要`の機械的短縮で代用しない。GitHubへ送る前、またはLibraryへcheckpointする前にActions側と同じvalidator基準でpreflightする。

## 5. Structured record transport

利用可能なrecord bankは `.survey/work-queue/records/bank-registry.json` を正本とする。通常構成はA〜Hで、各bankに次の5 slotを持つ。

- `metadata.json`
- `problem_method.json`
- `evaluation.json`
- `results.json`
- `positioning.json`

GitHubへ直接slotを書き始める前に、可能なら:

```bash
python .survey/scripts/select_record_bank.py --repo-root .
```

を使って`selected_bank`を取得する。selectorはcanonical `.survey/work-queue/jobs/*.json` のready状態まで確認するため、`next-jobs.json`の表示だけを見てbankを再利用しない。

各slot envelopeの基本形:

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

`metadata.json`には一覧・重複排除・監査を再現するため、正規識別子、題名、`summary`、`list_summary`、著者、公開日`published`、公開先`publication`、公開種別`publication_type`、公開状態`publication_status`、一次資料`sources`、実装情報`implementation`、公式コード`code`、確認日`last_checked`を保持する。公式コードを確認できない場合も`code`自体を省略せず`null`とし、未確認と実装なしを混同しない。

arXiv論文は主カテゴリと横断登録カテゴリを分ける。

```json
"arxiv_categories": {
  "primary": "cs.LG",
  "cross_list": ["cs.AI"]
}
```

一次論文のreference sectionを確認し、正規化した`references`、`references_checked_at`、`references_source`、`references_total`を保存する。本文中の単なる関連言及をreferenceとして数えない。reference section確認済みで識別可能IDが0件なら`references: []`を明示する。

5 slotすべてを書き終えた後だけ `.survey/work-queue/submissions/chat-inbox.json` を更新する。inboxの`record_slots`は5件固定で、各slot pathと実際のGit blob SHAを持つ。

`.survey/scripts/assemble_research_record.py` がrecordを検証・組み立て、`.survey/scripts/render_paper.py` がrunner内でMarkdownを生成する。Scheduled Chatは完成Markdownを直接送らない。内部の`queue_worker.py`はv9互換インターフェースを残すが、`normalize_v10_jobs.py`とassemblerを介したActions内部の互換層であり、Scheduled Chat向けのv9契約ではない。

## 6. Normal save protocol

1. job用の一意な`attempt_id`を決める。
2. bank selectorで安全なbankを選ぶ。
3. `metadata → problem_method → evaluation → results → positioning`の順で、各slotを最新blob SHA付きで更新する。
4. 途中write失敗時は`continuation-policy.json`のretry / health-probe規則に従う。
5. 5 slot成功後だけ固定`chat-inbox.json`を更新する。
6. 完全payloadをGitHubへ送信済みなら、Actions terminal反映を次の独立job開始の同期障壁にしない。ただし後でActions result + latest queueによりterminalを確認する。
7. 完全payloadをLibraryへ耐久保存済みなら、そのbankを未送信論文の永続キューとして保持し続けない。

## 7. Discovery / blocked / deferred / rejected

Discoveryは軽量候補評価、Researchは全文精読として分離する。discoveryの継続・停止はdiscovery各正本に従う。

GitHub write可能なら既存の固定transportだけを使い、queue/state/paper/READMEをScheduled Chatから直接編集しない。個別論文の全文取得不能や依存不足は対象jobだけblocked/deferredとし、次の独立作業へ進む。

## 8. Library fallback

GitHub writeを完了できない場合の正本は `fallback-routing.md`。新規保存先はChatGPT Libraryのみ:

`/LLM-survey-outbox/pending/<id>.json`

Libraryへ完全payloadまたはoffline job seedを耐久保存できれば研究を続ける。

research/auditでは1論文につき1 envelopeに5 slot + `chat-inbox.json`をまとめる。例としてbank Aを使う場合は `.survey/work-queue/records/chat-record/*.json` を含むが、**このbank指定はimmutable envelope作成時のstaging参照であり、replay時の固定予約ではない**。dispatcherはreplay時点で安全なbankへ一時再配置できる。完成Markdownはfallbackへ保存しない。

## 9. Recovery path

Libraryから固定record bankへ直接replayしない。Scheduled ChatはLibrary sourceをまず:

`.survey/work-queue/fallback-inbox/<envelope-id>.json`

へ不変envelopeとして送る。

同じ`id`がGitHub fallback-inbox/archiveにあり内容も同一なら再writeせずLibrary側をprocessedにできる。内容不一致なら衝突としてfailedへ隔離する。

`.survey/scripts/dispatch_fallback_inbox.py` がsurvey-helperの共通concurrency group内で1 Actions run最大1件を展開する。research/audit envelopeは `.survey/scripts/fallback_transport.py` のbank選択を通し、作成時のbankが現在occupiedなら安全なfree/reusable bankへ一時remapする。安全なbankがなければfailedにせずdependency/deferredとしてinboxに残す。job未実体化やchat transport busyも同様に待機する。

## 10. Offline discovery

GitHub write不能中にactionable readyが尽きてもLibraryが書けるなら探索を続ける。

1 submissionの候補0〜5件を `.survey/work-queue/transport/offline-job-seed.json` に格納するenvelopeとしてLibraryへ保存する。5件はbatch上限だけであり、run全体の探索上限ではない。候補のresearch job IDは`fallback-routing.md`の決定論的規則で計算する。

通常論文workerはseed保存後、job実体化を待たず同じrunで候補を精読し、完成research envelopeもLibraryへ保存してよい。探索専用workerはresearchへ進まない。復旧時はseedがjobを実体化するまでresearch envelopeをdependency待ちにする。

## 11. Transport integrity

- Scheduled Chatからpaper/state/README/identity/queue/`discovery-state.json`を直接更新しない。
- fallback envelopeから`papers/**`やworkflow/scriptを直接書かない。
- completionはActions result + latest queueで検証する。
- 同一payloadの重複copyは同じenvelope IDで冪等に収束させる。
- pending/replay失敗、bank exhaustion、1本処理完了、5 candidate送信、Actions待ちをrun終了理由にしない。

## 12. Paper family routing

research開始時点で、論文を **Inference / Training / Survey** のどこへ保存するかを明示的に判定し、`paper_path`を一致させる。

- **Survey / サーベイ**: 主目的が複数の既存研究・方式・システムを横断整理し、分類、比較、体系化、研究課題整理を行うsurvey / review / systematic review / tutorial-style overview。新規の中心的システム手法そのものを提案する原著論文はSurveyへ入れない。
- **Inference / 推論**: 新規手法・システム・アルゴリズムの主目的が推論、serving、decoding、KV cache、offload、MoE実行、on-device実行などの推論効率化である原著論文。
- **Training / 学習**: 学習・fine-tuning・optimizer・activation/parameter/optimizer-state offloadなど学習段階の効率化が主目的。ただし通常サーベイではTraining側の新規追加は凍結方針を優先し、明示的な指示がない限り新規収録しない。

Surveyと判定した論文を `papers/inference/**` へ保存しない。保存先は `papers/survey/<survey-lineage>/<filename>.md` とする。判定が曖昧な場合はタイトル文字列ではなく、論文の主たる貢献が新規システム提案か既存研究群の体系化かで決める。原著論文とsurveyを兼ねる場合、主要な評価・新規性が独自手法にあるならInference側を優先する。
