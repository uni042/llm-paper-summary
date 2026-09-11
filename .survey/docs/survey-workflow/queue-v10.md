# Queue-based survey workflow v10

workflow v10は、GitHubを唯一の正本としてqueue/state/identityをGitHub Actions側で管理し、Scheduled Chatは探索、一次資料全文取得、科学的判断、監査判断、構造化research record作成を担当する。

この文書はqueueとtransportの契約だけを定義する。実行順・停止判定・fallback選択は重複定義せず、次を正本とする。

1. `worker-router.md`
2. `fallback-routing.md`
3. `continuation-policy.json`
4. `backlog-resilience.md`
5. `.survey/templates/paper.md`
6. `.survey/work-queue/records/bank-registry.json`

## 1. Queue policy

- ready jobはpriority順に処理する。
- job処理、blocked化、checkpoint後は最新queueを再取得する。
- actionable readyが尽きたらdiscoveryを行う。
- discovery候補は0〜5件。5件はノルマではない。
- research後、追加の一次資料確認が明確に必要な場合だけauditを生成する。
- 固定の日次件数、固定batch数、固定research/audit比率は設けない。
- 同一runでは実行環境が許す限り `discovery → research → 必要ならaudit → queue再取得` を継続する。
- fallback backlog、record bank exhaustion、単一job失敗はrun終了理由にしない。

GitHub上でreadyでも、完全payloadがChatGPT LibraryまたはGitHub fallback-inboxへcheckpoint済みなら、そのjobは再精読しない。checkpoint済みreadyだけがqueueを塞ぐ場合は `.survey/work-queue/transport/request-jobs.json` を使ってstatusを変更せずdiscovery補充を要求する。

Google Drive fallbackは廃止済みで、新規保存・replay・backlog判定には使わない。削除前実装は `archive/drive-fallback-before-removal-20260910` ブランチに保存している。

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
- duplicate suppression
- derived-view rebuild
- offline job seed materialization
- GitHub fallback-inboxの直列dispatch

Notionは使用しない。旧 `/LLM-survey-fallback/` はlegacy移行元であり、新規保存には使わない。

## 3. Duplicate prevention

候補提出前とresearch着手前に次を照合する。

1. `.survey/survey-state/paper-identity-index.json`
2. `.survey/survey-state/identity-deltas/**/*.json`
3. `papers/inference/**` と `papers/survey/**` の既収録論文
4. `.survey/work-queue/jobs/*.json`
5. ChatGPT Library / GitHub fallback-inbox上のseedとcheckpoint済みjob

canonical ID / arXiv ID / DOI / OpenReview IDを優先する。GitHub code searchだけで未登録判定をしない。Actions側の `.survey/scripts/dedupe_queue.py` も再確認する。

## 4. Research quality

一次資料本文を最後まで読む。全文取得不能ならcompletedにせずblocked/deferredとする。抄録・検索断片から欠落情報を推測しない。

本文品質は `.survey/templates/paper.md` を唯一の正本とする。新しい会話・実行環境では、同テンプレートが例示するMoE-Infinityの既存まとめも確認する。

構造化recordは内部メモではなく、人間向けMarkdownへ変換する原稿である。特に`problem_method`は、入力、観測状態、処理、出力、前後接続、なぜ効くか、追加コスト、失敗条件が追える量を書く。

GitHubへ送る前、またはLibraryへcheckpointする前にActions側と同じvalidator基準でpreflightする。基準未達recordは完成扱いにしない。

## 5. Structured record transport

利用可能なrecord bankは `.survey/work-queue/records/bank-registry.json` を正本とする。現在の通常構成はA〜Hで、各bankに次の5 slotを持つ。

- `metadata.json`
- `problem_method.json`
- `evaluation.json`
- `results.json`
- `positioning.json`

GitHubへ直接slotを書き始める前に、可能なら:

```bash
python .survey/scripts/select_record_bank.py --repo-root .
```

を使って`selected_bank`を取得する。見た目だけでbankを選ばない。

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

`metadata.json`では一覧・重複排除・監査を再現できるよう、正規識別子、題名、要約、著者、公開日`published`、公開先`publication`、公開種別`publication_type`、公開状態`publication_status`、一次資料`sources`、実装情報`implementation`、公式コード`code`、確認日`last_checked`を必須項目として保存する。公式コードを確認できない場合も`code`自体を省略せず`null`とし、未確認と実装なしを混同しない。arXiv論文は、その版のarXiv表示を正本として、主カテゴリと横断登録カテゴリを次の形で保存する。

```json
"arxiv_categories": {
  "primary": "cs.LG",
  "cross_list": ["cs.AI"]
}
```

`primary`と`cross_list`を混ぜない。カテゴリが1件だけなら`cross_list`は空配列とする。Markdown生成時にこれらのメタデータを捨てず、論文frontmatterへ引き継ぐ。

5 slotすべて反映後だけ `.survey/work-queue/submissions/chat-inbox.json` を更新する。inboxの`record_slots`は5件固定で、各slotのpathと実際のGit blob SHAを持つ。

`.survey/scripts/assemble_research_record.py` がrecordを検証し、`.survey/scripts/render_paper.py` がrunner内でMarkdownを生成する。Scheduled Chatは完成Markdownを直接送らない。

## 6. Normal save protocol

1. job用の一意な`attempt_id`を決める。
2. bank selectorで使用bankを決める。
3. `metadata → problem_method → evaluation → results → positioning`の順で、各ファイルを最新blob SHA付きでupdateする。
4. 途中write失敗時は`continuation-policy.json`のretry/health-probe規則に従う。
5. 5 slot成功後だけ固定`chat-inbox.json`をupdateする。
6. Actions resultと最新queueでterminalを確認する。
7. 完全payloadをLibraryへ耐久保存済みなら、そのbankは未送信論文の保存キューとして保持し続けない。

## 7. Discovery / blocked / deferred / rejected

長いartifactは不要。GitHub write可能なら既存の固定transportだけを使い、queue/state/paper/READMEをScheduled Chatから直接編集しない。

個別論文の全文取得不能や依存不足は対象jobだけblocked/deferredとし、次の独立作業へ進む。

## 8. Library fallback

GitHub writeを完了できない場合の正本は `fallback-routing.md`。

保存先はChatGPT Libraryのみ:

`/LLM-survey-outbox/pending/<id>.json`

Libraryへ完全payloadまたはoffline job seedを耐久保存できれば研究を続ける。

共通envelope:

```json
{
  "schema_version": 1,
  "id": "unique-safe-id",
  "kind": "research",
  "job_id": "job-research-...",
  "attempt_id": "attempt-...",
  "depends_on_job_ids": ["job-research-..."],
  "writes": [
    {"path": ".survey/work-queue/records/chat-record/metadata.json", "content": "{...}\n"},
    {"path": ".survey/work-queue/submissions/chat-inbox.json", "content": "{...}\n"}
  ]
}
```

research/auditでは1論文につき1 envelopeに5 slot + `chat-inbox.json`をまとめる。1論文を複数fragmentへ分割しない。完成Markdownはfallbackへ保存しない。

## 9. Recovery path

Libraryから固定record bankへ直接replayしない。Scheduled Chatは復旧したLibrary sourceをまず:

`.survey/work-queue/fallback-inbox/<envelope-id>.json`

へ不変envelopeとして送る。

同じ`id`がGitHub fallback-inbox/archiveにあり内容も同一なら再writeせずLibrary側をprocessedにできる。内容不一致なら衝突としてfailedへ隔離する。

`.survey/scripts/dispatch_fallback_inbox.py` がsurvey-helperの共通concurrency group内で1 run最大1件を固定transportへ展開する。job未実体化やchat transport busyはdependency待ちとしてinboxに残し、failedにしない。

## 10. Offline discovery

GitHub write不能中にactionable readyが尽きてもLibraryが書けるなら探索を続ける。

候補0〜5件を `.survey/work-queue/transport/offline-job-seed.json` に格納するenvelopeとしてLibraryへ保存する。候補のresearch job IDは`fallback-routing.md`の決定論的規則で計算する。

seed保存後はjob実体化を待たず同じrunで候補を精読し、完成research envelopeもLibraryへ保存してよい。復旧時はseedがjobを実体化するまでresearch envelopeをdependency待ちにする。

## 11. Transport integrity

- Scheduled Chatからpaper/state/README/identity/queueを直接updateしない。
- fallback envelopeから`papers/**`やworkflow/scriptを直接書かない。
- completionはActions result + latest queueで検証する。
- 同一payloadの重複copyは同じenvelope IDで冪等に収束させる。
- pending/replay失敗、bank exhaustion、1本処理完了をrun終了理由にしない。

## 12. Paper family routing

research開始時点で、論文を **Inference / Training / Survey** のどこへ保存するかを明示的に判定する。`paper_path` はこの判定と一致させる。

- **Survey / サーベイ**: 主目的が複数の既存研究・方式・システムを横断整理し、分類、比較、体系化、研究課題整理を行うsurvey / review / systematic review / tutorial-style overview。新規の中心的システム手法そのものを提案する原著論文は、関連研究節が広くてもSurveyへ入れない。
- **Inference / 推論**: 新規手法・システム・アルゴリズムの主目的が推論、serving、decoding、KV cache、offload、MoE実行、on-device実行などの推論効率化である原著論文。
- **Training / 学習**: 学習・fine-tuning・optimizer・activation/parameter/optimizer-state offloadなど学習段階の効率化が主目的。ただし通常サーベイではTraining側の新規追加は凍結方針を優先し、明示的な指示がない限り新規収録しない。

Surveyと判定した論文を `papers/inference/**` へ保存してはならない。保存先は `papers/survey/<survey-lineage>/<filename>.md` とする。適切なsurvey lineageがまだなければ、対象範囲に沿った下位ディレクトリを新設してよい。

判定が曖昧な場合は、タイトルに `survey` や `review` が含まれるかではなく、**論文の主たる貢献が新規システム提案か、既存研究群の体系化か**で決める。原著論文とsurveyを兼ねる場合、主要な評価・新規性が独自手法にあるならInference側を優先する。
