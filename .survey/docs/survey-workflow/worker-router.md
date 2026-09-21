# Worker router — workflow v10

この文書はScheduled Chat / Work系ワーカー（worker）の**唯一の実行手順正本**である。役割分岐（routing）、継続・停止、探索、研究、退避の判断を別文書から組み立て直してはならない。

ワーカーは実装リファレンス（implementation reference）や履歴互換資料（read-compatibility material）から手順を補完しない。必要な実装詳細は正規スクリプトが `[WORKER-GUIDE]`、`next_action`、`recovery_steps` として返す。実装リファレンスは保守・テスト用途に限定する。

**実行時の具体的な操作では、正規スクリプトが返す `[WORKER-GUIDE]` / `next_action` / `recovery_steps` を最優先する。** `[待機]` 中に依存する次操作へ進んだり、`[次]` を自己判断で飛ばしたり、`[手順エラー]` / `[正しい手順]` を無視して別経路へ迂回してはならない。機械案内とこの文書が矛盾した場合は、旧経路へ逃げず**そのrunでは機械案内に従って安全に処理し、矛盾の内容・採用した機械案内・影響を最終報告でユーザーへ相談事項として明記する。** ワーカーがその場で正本の意味を独自に上書きしない。

## 1. 開始時に読む状態

各実行（run）の開始時に最新 `main` HEADを取得し、同じHEADで次を読む。

- `.survey/work-queue/next-jobs.json`
- `.survey/work-queue/maintenance-cycle.json`
- `.survey/work-queue/discovery-state.json`
- 必要なら `.survey/work-queue/state.json`
- 出力品質が必要な場合は `.survey/templates/paper.md`

実際の起動時刻を1回取得し、`actual_invocation_start` として固定する。予定時刻や前回runの時刻を再利用しない。通常の時間枠は起動時刻から3600秒で、残り600秒以下では新しい独立作業を開始しない。残り180秒以下では耐久保存と安全な引き継ぎだけを行う。

## 2. 共通ルーター

毎時 `:00` と毎時 `:30` の論文ワーカーは、**同じ論文処理規約・同じ手順**を使う。スケジュール時刻による役割差は設けない。run開始時に最新 `next-jobs.json` から **Research/Audit の ready 全件数**を `candidate_inventory` として取得する。`claimable` ではなく、原則 `claiming.ready_research_audit`、それが無ければ `counts.research.ready + counts.audit.ready` を使う。このrun開始時の値を固定し、次の1条件だけで今回の論文作業モードを決める。

- **`candidate_inventory >= 50` → 読解（Research / Audit）**
- **`candidate_inventory < 50` → 探索（Discovery）**

**08:30 JSTの`:30`専用runだけ**は、この分岐より優先して第9節の日次更新・maintenance経路へ入る。通常runに「maintenance対象」という別条件は設けない。

モード決定後は、どちらのScheduled Chatから起動したかを一切条件分岐に使わない。探索なら第4節、読解なら第3節の共通手順をそのまま使う。`:00` 専用・`:30` 専用の探索手順、読解手順、overflow modeは作らない。

候補数は最新の耐久状態から毎run開始時に取得し、旧runや旧STATUSの推定値を再利用しない。候補数が境界ちょうど50件なら読解を選ぶ。**一度選んだモードはそのrunの終了まで固定する。** run中に候補数が50を跨いでも再ルーティングしない。次回runの開始時にあらためて最新候補数で判定する。

ノルマは維持する。

- **読解モード**: 今回の起動中に **Research / Audit 合計で成功完了を最低3件**作る。Research job 1件とAudit job 1件は、同じ論文に対するものでも**別々に1件ずつ**数える。Researchは一次資料全文→5スロット→preflight→不変submission→submission result成功→最新mainへの反映確認まで、Auditも対応する不変submission→成功result→最新mainへの反映確認までを1件の完了とする。`blocked` / `deferred` / `rejected` や提出しただけのpending状態はノルマへ数えない。3件は停止上限ではない。
- **探索モード**: 今回のrunで最低4つの**成功した正規schema v3 precheck**を完了させ、そのprecheckに対応するDiscovery submission/resultまで耐久反映する。**1つのprecheck `request_id` = 1ラウンド**と数える。同じprecheckから候補を複数submissionへ分割しても1ラウンドのままであり、逆に別の成功precheckなら同じprovider・同じ探索元でも別ラウンドとして数える。候補0件の成功precheckも、0件submission/resultまで正規経路を完了すれば1ラウンドに数える。4ラウンドは停止上限ではない。

handoff guard、platform/context limit、GitHub正本の読取不能、GitHub/Library双方への耐久保存不能などのhard stopはノルマより優先する。件数を満たすために弱い候補を採用したり、読解品質を下げたりしない。
## 2.1 正規スクリプトを直接実行できない環境のfast-lane transport

Scheduled Chat等でリポジトリ内Pythonを直接起動できないこと自体は、Research / Audit / Discoveryを停止する理由ではない。GitHubへのread/writeが可能なら、**requestファイルをmainへ耐久保存し、対応するGitHub Actions fast laneに正規スクリプトを実行させ、resultファイルを読む経路**を現行の正規transportとして使う。この経路はmanual state編集ではない。

Research / Auditのclaimは次の順で行う。

1. 最新main HEADとclaim stateを再取得し、同一workerの未完了claimがないことを確認する。
2. 一意な `request_id` を作り、`.survey/work-queue/claim-requests/<request_id>.json` をmainへcommitする。通常Scheduled Chatの最小requestは `schema_version: 1`、`request_id`、`worker_id`、`worker_kind: scheduled_chat`、`requested_at`、`max_jobs: 1`、`job_types: ["research", "audit"]` を持つ。
3. このpushで `.github/workflows/survey-claim-fast.yml` が起動し、最新main上で `claim_worker_with_banks.py` を実行する。ワーカー自身が `claims/*.json`、`jobs/*.json`、`state.json`、`next-jobs.json` を直接編集してclaimを再現してはならない。
4. 同じ `request_id` の `.survey/work-queue/claim-results/<request_id>.json` を所定間隔で再確認する。resultの `ok`、`assignments`、`attempt_id`、`claim_id`、`record_bank` / `record_bank_fallback`、`next_action` / `instructions` を正本として以後の処理を行う。
5. claim result待ちのためだけに別requestを発行しない。

**並列workerの扱い:** `max_jobs=1` と未完了claimの直列制約は**同一worker / 同一論理worker lineage内だけ**に適用する。`:00` worker、`:30` worker、その他の独立workerは、別 `worker_id` と別record bankで同時にResearch / Auditを進めてよい。他workerのactive claim、他workerのclaim request、またはclaim fast lane上で先行requestが処理中であることを理由に、このworkerのrunを停止・終了・handoffしてはならない。`.github/workflows/survey-claim-fast.yml` の `concurrency: survey-claim-main` は**claim割当commitの競合回避だけを直列化するもの**であり、論文精読そのものを全worker間で直列化するものではない。自分のrequestがfast lane待ちなら同じ `request_id` のresultを所定間隔で再確認し、割当後は返された別job / record bankで処理を続ける。他workerのclaimを自分の未完了claimとして扱わない。

Research / Auditの不変submissionも同様にfast laneを使える。

1. 5スロットをclaim result指定のrecord bankまたは現行fallbackへ完全保存し、必要な実blob SHAを確定する。
2. attempt固有descriptorを `.survey/work-queue/submissions/research/<unique>.json` または `audit/<unique>.json` にcommitする。status-only `blocked` / `deferred` / `rejected` も同じsubmission laneへ送る。
3. このpushで `.github/workflows/survey-submission-fast.yml` が起動し、最新main上で正規submission processorを実行する。
4. 同名の `.survey/work-queue/results/research/<unique>.json` または `audit/<unique>.json` を確認し、`ok`、終端status、`next_action` / `recovery_steps` に従う。pending中は同一descriptorを上書きせず、**同じ論文のresult確認・repair準備・canonical state確認だけを続け、次の論文へは進まない。**
5. **1 attemptにつきcompleted descriptorは1本だけ**とする。検証失敗後に同じ `job_id / attempt_id` の `repair1`、`repair2` 等を追加して修正しない。
6. failure resultが `content_validation`、またはjobが `repair_required=true` になった場合は、そのfailure resultがmainへ耐久保存されたことを確認した後、同じjobを `job_ids: [<job_id>]` で指定した新しいclaim requestを発行する。claim fast laneが旧claimを解放し、**新しいclaim_id / attempt_id** と回復済みrecord bankを返すので、指摘されたslotだけを一次資料に基づいて修正して新attemptのdescriptorを提出する。全文読解済み成果を捨てない。
7. failure resultが `retryable=true` の場合は、同じattemptの別descriptorを作らない。既存の同一descriptorをsubmission laneのbounded recoveryに任せ、同じresultを再確認する。`retryable=false` かつ `repair_required` でもないstate/transport guardは、返された回復指示に従う。

Discovery precheckも、ローカルCLIがない場合は `.survey/work-queue/discovery-precheck/requests/<request-id>.json` をmainへcommitし、`.github/workflows/discovery-precheck.yml` に `process_discovery_precheck.py` を実行させ、同名resultを読む。Discovery submissionは既存のqueue処理経路へ流し、Research jobやstateを手で生成しない。

**重要:** 「ローカルPython/任意コマンド実行機能がない」は、GitHub read/writeと上記fast laneが利用可能な限り `platform_limit` / hard stopではない。fast lane自体がGitHub/API/認証/Actions障害で利用不能になった場合だけ、第6節の保存障害・退避と第7節の停止判定へ進む。

## 3. 読解（Research / Audit）の共通処理ループ

1. 最新queueと現在の担当確保状態（claim state）を取得する。
2. priority最上位の実行可能jobを**1件だけ**担当確保する。`max_jobs=1`。同一ワーカーが未完了claimを複数保持しない。ただし**Audit starvation防止をpriorityより優先する**。今回runの成功完了を3件ずつのブロックとして数え、ready Auditが存在するブロックでは少なくとも1件Auditを処理する。ブロック内で先に2件ともResearchを完了し、まだAuditを完了していない場合、3件目のclaim requestは `job_types: ["audit"]` に限定する。それ以外は `job_types: ["research", "audit"]` で通常priority順に選ぶ。
3. claim result待ちなら同じ `request_id` を保持する。別requestを発行して回避しない。次の安全な判断に結果が必要な場合だけ10秒の実時間間隔で同じ対象を再確認する。
4. claim resultの `record_bank` / `record_bank_fallback` をそのまま使う。ワーカーが別bankを選び直さない。
5. 一次資料本文を最後まで読み、抄録や検索断片から欠落情報を推測しない。
6. `metadata`、`problem_method`、`evaluation`、`results`、`positioning` の5スロットを完成させる。
7. Actionsと同じ基準で事前検査（preflight）する。
8. GitHubへ保存可能なら各スロットの実blob SHAを取得し、attempt固有の不変descriptorを `.survey/work-queue/submissions/research/` または `audit/` へ保存する。
9. GitHub書込みがrun全体で利用不能なら、完全な5スロットpayloadをChatGPT Library `/LLM-survey-outbox/pending/` へ1論文1envelopeで保存する。
10. 完全payloadまたはstatus-only descriptorを耐久保存して不変submissionを送った後は、**同じ論文のsubmission resultが `ok=true` の終端状態になり、最新 `main` に対応job / artifactまたはstatus反映を確認するまで次の論文へ進まない。** pending中は同じresultを再確認し、validation失敗なら同じ論文の正規repair経路を完了する。終端反映を確認して初めて最新queue / claim stateを取り直し、次の論文を1件だけclaimする。ノルマへ数えるのはそのうち成功完了したResearch / Auditだけである。

禁止事項:

- 固定 `submissions/chat-inbox.json` を生成・更新しない。
- 完成MarkdownをScheduled Chatから直接送らない。
- claim resultが返したbankを無視して別bankへ書かない。
- 1本処理したことだけをrun終了理由にしない。

**論文単位の処理は完全直列とする。** 1本について一次資料取得・全文読解・5スロット作成・検証・不変submissionまで行い、または取得不能等ならstatus-only submissionへ収束させ、そのsubmissionの `ok=true` 終端resultと最新main反映を確認する前に、次の論文をclaimしたり、次論文の一次資料・書誌・取得経路を先取りしたりしてはならない。待ち時間に行ってよいのは、同じ論文のrepair・result確認・canonical state確認、および次論文を取得しない範囲の独立した状態整合処理だけである。

### 3.1 実運用で確立した高スループット原則

以下は品質基準を緩める高速化ではなく、全文精読・検証・耐久保存を維持したまま重複作業を減らすための標準手順である。

1. **全文読解済み成果を捨てない。** 初回全文精読後はrecord bankと既存5スロットを再利用し、validation失敗時は指摘されたslotだけを一次資料に基づいて修復する。一次証拠が不足・変更していない限り、全文を最初から読み直さない。
2. **初回5スロットをvalidator下限ぎりぎりにしない。** 問題設定は「問題＋既存法で解けない理由」、method overviewは入力から出力までのend-to-end流れ、各componentは「入力・内部処理・出力・他componentとの接続」を十分に記述する。短すぎる説明によるrepair往復を減らす。
3. **一次資料は取得できた時に一度で必要範囲を読む。** 完全なarXiv HTMLが使えるなら優先し、必要ならPDF、OpenReview/会議公式、著者・プロジェクト公式コピーへ進む。同一資料を小分けに再取得せず、手法・評価・結果・ablation・限界・関連研究までまとめて確認する。
4. **1経路の取得失敗をwhole-run failureにしない。** materially distinctな公式経路を試し、なお全文取得不能ならstatus-only `blocked` を不変submissionとして耐久保存し、対応resultが `ok=true` の終端状態になって最新mainへ反映されたことを確認してから次の論文へ進む。status-only `blocked` / `deferred` / `rejected` は、Scheduled Chatが最小の不変JSON descriptorを `.survey/work-queue/submissions/research/` または `audit/` へ直接保存し、既存のsubmission laneに処理させる。ローカルPythonや保存前canonicalizerの実行を前提にしない。descriptorは `schema_version` / `transport_version` / `kind` / `attempt_id` / `job_id` / `claim_id` / `worker_id` / `status` / `reason` を基本とし、取得済みなら `retrieval_evidence` / `blocked_at` を加えてよい。`record_bank` / `paper_path` / `record_slots` / `expected_blob_sha` その他のrecord transport fieldはstatus-only descriptorへ混在させない。一時障害の `blocked` と、一次証拠で再試行不要と確定した `rejected` を混同しない。
5. **非同期待ちでも論文単位の直列性を崩さない。** claim/result/submissionの同じIDを保持して所定間隔で確認する。submission待ち中は次論文のclaim・一次資料取得・書誌確認へ進まず、同じ論文のrepair準備、identity/queue同期など次論文を取得しない作業だけを行う。未完了claimを増やしたり同一requestを重複発行しない。
6. **canonical stateを再利用する。** claim前・submission後・repair時に最新queue、identity、rejection ledger、result、record bankを使い、重複claim・重複探索・重複取得を避ける。Research / Audit claimは常に1件だけ保持し、成功完了またはstatus-only submissionの `ok=true` 終端resultと最新main反映を確認した後にだけ次へ進む。
7. **Research / Audit 合計3件ノルマは維持する。** `research_audit_completed_this_invocation < 3` の間は、hard stopまたはhandoff guardでない限り読解を継続する。成功resultと最新main反映を確認したResearchまたはAuditだけを1件として数え、同一論文のResearchとAuditも別jobとしてそれぞれ1件に数える。ready Auditが存在するなら3件ブロックごとに最低1件Auditを含める。3件到達は停止上限ではなく、600秒handoff guardに入るまで、または安全に実行可能な作業が尽きるまで同じモードで継続する。取得枠を節約するため、再取得より既存成果の局所修復を優先する。

## 4. 探索（Discovery）の共通入口

新規Discoveryは**固定ソース precheck schema v3** だけを使う。ワーカーが検索結果を数件だけ手でJSONへ詰め、schema v1/v2として投入してはならない。

requestは `.survey/work-queue/discovery-precheck/requests/<request-id>.json` に保存し、少なくとも次を含める。

```yaml
schema_version: 3
operation: precheck_discovery_candidates
provider: openalex | semantic_scholar | openalex_references | repository_references
source_url: <固定した検索/API URL>
collector_id: <同一探索軸の識別子>
run_key: <今回runの識別子>
axis: <探索軸>
target_unseen: 20
```

`target_unseen` の既定値は20。precheck側の `discovery_provider_adapter.py` と `collect_until_unseen()` が**同じ検索結果をページ送り**し、各ページで既収録・既候補・既却下・ページ間重複を除外する。ワーカーが2ページ目以降を個別に手作業で継ぎ足す必要はない。

評価に使ってよい候補は、schema v3 resultが `evaluation_allowed=true` として返した `allowed_records` だけである。precheck resultが未完了なら、旧schemaへ逃げずに同じ現行経路を完了させる。

### 4.1 探索方法

探索は**引用グラフ優先（citation-first）**とし、既存の収録論文に直接つながる2方向を主経路にする。どちらも同じschema v3 precheck、identity/rejection重複排除、固定ソースページ送りを使う。

1. **後方引用（backward reference）**: 収録済み論文が引用している論文を掘る。最初はリポジトリ全体の構造化 `references` を横断する `provider: repository_references`、`source_url: repository://structured-references`、原則 `target_unseen: 20` を使う。構造化メタデータが不足する系統では、種論文ごとの `openalex_references` または Semantic Scholar `/references` を補助的に使う。
2. **前方引用（forward citation）**: 収録済み論文を引用している後続研究を、系統ごとの種論文から最新順に掘る。OpenAlexの `cites:W...` または Semantic Scholar `/citations` を固定ソースにする。
3. **通常検索・新着検索**: 引用関係だけでは拾えない新系統・新用語を補完するフォールバック。OpenAlex / Semantic Scholar等の固定検索URLを使う。

**通常・定期Discoveryでは、同じrun_keyの中で後方引用と前方引用を少なくとも1回ずつ試すまで通常検索へ進まない。** 一方、後方引用側の候補山が残っていても前方引用を止めない。原則として後方引用1バッファを分類・投入したら前方引用refreshへ進み、その後は `discovery_stats.search_windows` の未収録率・採用率・重複率を見て、実績の良い種論文／方向を優先する。これにより古い参考文献の巨大な山を掘りつつ、新しく既存研究を引用し始めた論文も取りこぼしにくくする。

前方引用・後方引用のどちらも、同じ固定結果集合のページ送りは `collect_until_unseen()` に任せる。ワーカーが上位数件だけを手作業で抜き、重複が多いから別クエリに変えることは禁止する。原則 `target_unseen: 20` まで既収録・既候補・既却下・ページ間重複を飛ばしてから軽量評価する。

**明示ユーザー指定探索（explicit user-directed discovery）の例外**: ユーザーが現在の会話で探索軸・対象系統・引用方向などを明示して個別探索を依頼した場合、その依頼に限って上記の自動実行順を上書きしてよい。これは通常・定期Discoveryの方針変更ではなく、ユーザー指定軸を即時に調べるための限定例外である。候補投入は必ずschema v3固定ソース事前検査（fixed-source precheck）→identity/rejection重複排除→通常Discovery submission→queue workerの一本道を通し、precheck自体を省略してはならない。submissionには `discovery_stats.trigger: explicit_user_request` と、非空の `user_directed_request.request_id` / `user_directed_request.summary` を付ける。自律・Scheduled workerはこの印を自己生成して通常優先順位を回避してはならない。

#### 4.1.1 structured-reference curation の進め方

この経路は、収録済み論文の `references` を横断して候補集合を作り、同じ候補を指す収録論文数 `relation_count` が多い順に少しずつ評価する。1回に全候補を掃除しようとせず、通常の `target_unseen: 20` の1バッファを処理する。**候補集合は空になるまで継続して掘るが、前方引用refreshをブロックしない。各runで後方引用を処理したら前方引用も実行し、その後は探索実績に応じて配分する。**

- 候補生成は `.survey/scripts/reference_pool.py` を正本とする。既収録論文に加え、`.survey/work-queue/reference-curation/unrelated-papers.json` と `.survey/work-queue/reference-curation/borderline-papers.json` の登録済み候補を通常時は除外する。
- **明確にサーベイ対象外**と判断した候補は、次の候補へ進む前に `.survey/scripts/reference_relevance_ledger.py mark-unrelated` で無関係台帳へ永続保存する。同じ論文を後続runで再判定しない。
- **関連性・重要性・得られそうな知見が微妙で、現時点ではResearchへ送る価値が弱い候補**は `.survey/scripts/reference_relevance_ledger.py mark-borderline` で微妙台帳へ保存する。微妙台帳も通常の `repository_references` 探索ではデフォルト除外し、同じ候補を毎回評価し直さない。
- 微妙台帳は永久除外ではない。後で明示的に再検討する場合だけ `reference_pool.py --include-borderline` を使って再び候補へ含めてよい。通常runでは使わない。
- 関連ありの候補は一次資料でtitle/abstract/書誌を補完してから、当該schema v3 precheck result / receiptを参照する通常のDiscovery submissionへ送る。canonical IDだけをtitle代わりにして提出しない。
- この経路からResearch jobを直接生成しない。Candidate投入以降は4.3〜4.4の一本道へ合流する。

### 4.1.2 系統限定の最新被引用探索（lineage-scoped forward-citation refresh）

特定の系統ページにある収録済み論文を**種論文（seed papers）**として、その論文を引用する後続研究から最新の有力候補を拾う方法。既存論文の引用先を掘るstructured-reference curationとは逆方向なので、直近数か月の新手法を拾うのに向く。通常runでも後方引用と並ぶ主経路として使い、`repository_references` の枯渇を待たない。ユーザーが「この系統を引用する最新論文を探して」のように明示した場合は、上記の明示ユーザー指定探索として対象系統を即時実行してよい。

効率化の標準手順:

1. **系統全体を種集合にする。** READMEだけでなく、その系統ディレクトリ内の収録論文の正規識別子（canonical ID）を列挙する。最初は、引用が十分蓄積している代表論文・基礎論文から始める。1本で十分な新規候補が出る場合、全種論文を同時に走査しない。
2. **最新順を保証できる固定ソースを優先する。** OpenAlexでWork IDを解決できる場合は `/works?filter=cites:W...&sort=publication_date:desc` を固定 `source_url` とし、必要なら公開日範囲も付ける。Semantic Scholarを使う場合は対象論文の `/citations` エンドポイントを固定ソースにする。検索語だけの類似検索に置き換えない。
3. **schema v3事前検査（precheck）へ渡す。** 原則 `target_unseen: 20`。同一固定ソースのページ送りは `collect_until_unseen()` に任せ、既収録・既候補・既却下・ページ間重複を自動除外する。引用件数が大きい種論文でも、ワーカーが先頭数件だけ手で抜かない。
4. **新しいものから軽量評価する。** `allowed_records` を公開日降順で見て、対象系統への直接性を確認する。「種論文を引用している」だけでは採用理由にせず、既存系統をどの軸で更新するか（例: expert数の適応配分、expert pruning/merging、圧縮後回復、実測serving改善）をreasonに書く。
5. **1 submissionは強い候補だけ0〜5件。** 5件を埋めるための弱い候補は入れない。候補化後は4.3〜4.4の通常経路へ合流し、Research jobを直接生成しない。
6. **次の種論文へ進む条件を明確にする。** 1本の種論文から十分な強候補が得られたら、そのsubmissionを先に耐久保存する。続行時は同じ種論文を再度precheckしてidentity snapshotにより既候補を飛ばすか、別の種論文へ移る。複数種で同じ後続論文が出てもshared identityで重複除外させる。
7. **探索効率を記録する。** `discovery_stats.search_windows` に種論文、引用方向 `forward`、取得件数、未収録件数、評価件数、採用件数を残す。後続runでは採用率の高かった種論文を優先し、0件が続く種論文を毎回先頭から調べ直さない。

この方法が特に有効なのは、既存系統が2024〜2025年の代表論文を含み、2026年の新手法がその代表論文を関連研究として引用し始めている場合である。単純なキーワード検索より、対象系統との接続根拠を保ったまま最新研究へ追従しやすい。

### 4.2 探索ノルマ

探索モードでは、hard stopまたはhandoff guardがない限り、**今回のrunで成功した正規schema v3 precheckを合計4回**完了させ、それぞれをDiscovery submission/resultまで耐久反映する。ラウンドIDはprecheckの `request_id` とし、カウントはrun開始時に0から始める。1 precheckから強候補が6件以上出て `5 + 残り` の複数submissionに分割しても**1ラウンド**である。別precheckが成功すれば、同じprovider・同じ固定ソースでも別ラウンドとして数える。候補0件でも成功precheckと0件submission/resultまで完了すれば1ラウンドである。失敗・pendingのprecheckは数えない。4ラウンドは停止上限ではなく、600秒handoff guardに入るまで、または正規経路で安全に実行可能な探索が尽きるまで探索を続ける。

### 4.3 Candidate投入

Discoveryは軽量評価だけを行う。title、abstract、書誌、一次資料の存在、テーマ適合性、新規性の見込みを確認し、全文精読はResearchへ送る。

**Candidate priorityは0〜100点とし、基礎評価はワーカー判断を残しつつ、既存系統との関連・新しさ・venueが実際に読む順を動かす重みを持つようにする。** 推奨計算は `priority = min(100, base + lineage + recency + venue)` とする。

- **base: 0〜55点** — テーマ適合性、技術的重要性、得られる知見、実装・評価の有用性をまとめてワーカーが判断する。ここは固定チェックリストで機械化しない。
- **既存系統への関連度（lineage）: 0〜20点** — 既収録論文の直接引用・被引用、明確な後継/改良/比較対象で既存系統を直接更新する候補は `+20`、同一サブテーマに明確な差分を加える候補は `+10`、広いテーマ一致だけなら `+0` を目安とする。
- **新しさ（recency）: 0〜15点** — 直近6か月 `+15`、6〜12か月 `+10`、12〜24か月 `+5`、それ以前 `+0`。基礎的重要論文は古さだけで除外しない。
- **査読venue: 0〜10点** — NeurIPS / ICML / ICLR / MLSys / OSDI / SOSP / NSDI / USENIX ATC / EuroSys / ASPLOS / ISCA / MICRO / HPCA 等、対象分野の主要査読venueへの採択が既知なら `+10`、その他の信頼できる査読付きvenueは `+4`、不明またはarXivのみなら `+0`。推測しない。
- **Research投入下限**: 現行queueの正規実装に合わせ `priority >= 40` をCandidate→Research投入の下限とする。ただし40点を満たすためにbaseを水増ししない。弱い候補はborderline/unrelatedへ送る。
- **追加ネットアクセス禁止**: priority採点だけを目的として追加のWeb/APIアクセスを発生させない。precheckや既取得metadata、一次資料中に既にある情報だけを使い、不明項目は0点とする。
- candidateの `reason` には、lineage / recency / venueのうちpriorityを大きく押し上げた要因を短く残す。可能なら `priority_breakdown` に `base` / `lineage` / `recency` / `venue` / `total` を残す。

1回のDiscovery submissionへ送るcandidateは0〜5件。**5件はrun上限でもround上限でもなく、1 submissionの上限**である。1回のprecheckで評価後に強候補が6件以上残った場合は、同じprecheck result / receiptを参照した複数submissionへ `5 + 残り` で分割し、強候補をすべてCandidate化する。複数submissionに分けても探索ラウンド数は1のままとする。分割時は全submissionの `discovery_stats` に同じ `run_key` / `round` / `axis` を持たせ、`round_submission_index` を1始まり、`round_submission_count` を総分割数として記録する。単一submissionなら両方1としてよい。

Discoveryのmulti-round submissionは、どちらのwork mixから探索を選んだ場合でも自己記述型（self-describing）を使い、存在しないDiscovery `job_id` を合成しない。candidate投入前に最新HEAD / identity / queueを再確認する。

### 4.4 Discovery submissionからResearchへの一本道

Discovery後半は次の順序を正規経路とする。途中を手作業で代替してはならない。

1. `process_discovery_precheck.py` のschema v3 resultが `READY_FOR_EVALUATION` / `evaluation_allowed=true` になったことを確認する。
2. `allowed_records` だけを軽量評価し、候補0〜5件を `operation: submit_discovery_round` の不変submissionとして `.survey/work-queue/submissions/<unique>.json` に保存する。submissionは対応するprecheck result path / receiptを参照する。
3. `queue_worker.py` にsubmission処理を任せる。workerはResearch job IDを合成したり、`jobs/*.json` / `state.json` を直接書き換えたりしない。
4. 同名の `.survey/work-queue/results/<unique>.json` を確認し、`ok=true`、`research_jobs_added`、`final_duplicate_filtered_count`、`next_action` を読む。
5. `refresh_queue_snapshot.py` または `queue_worker.py` が更新した `.survey/work-queue/next-jobs.json` を確認する。
6. ready Research/Audit が現れても、**今回runがDiscoveryならclaimしない。** `next-jobs.json` への反映だけ確認し、run開始時に固定したDiscoveryを続ける。Research / Auditのclaimは、次回run開始時の `candidate_inventory >= 50` 判定で読解モードになった場合に `claim_worker_with_banks.py` から1件だけ取得する。
7. `research_jobs_added=0` でもrun終了理由にしない。最終重複排除や低優先度除外を確認し、必要なら別探索軸をschema v3 precheckから開始する。

失敗submissionの回収には `recover_discovery_submissions.py` を使う。回収後は `refresh_queue_snapshot.py` → `next-jobs.json` でcanonical stateを確認する。ただし**このrunが探索モードならResearchへ切り替えず、run開始時に固定した探索モードを維持する。** Research jobのclaimは次回以降、読解モードで行う。失敗済みsubmissionを上書きしたり、synthetic `job_id` を作って回避してはならない。

引用優先runでは、後方引用の候補山が残っていても前方引用へ進む。逆に前方引用が0件でも後方引用の山は継続する。**通常検索へ進めるのは、同じrun_keyで後方引用と前方引用の両方を試した後だけ**とし、通常検索は引用グラフで空く領域を埋める用途に限定する。単一provider障害は「0件」とみなさず、同じ引用方向の別providerまたは別種論文を試す。1 Discovery roundが耐久保存まで完了したら、**今回runの探索モードを維持したまま**次の探索軸を選ぶ。候補在庫を再取得してもrun中のモード変更には使わず、次回runの開始判定用状態としてのみ扱う。

## 5. 重複排除

candidate提出前とResearch着手前に、正規識別子（canonical ID）、arXiv ID、DOI、OpenReview ID、正規化題名（normalized title）の順で照合する。

Discovery precheckではidentity snapshotとrejection ledgerを使う。GitHub code searchだけで「未収録」と判断しない。

## 6. 保存障害と退避

耐久経路は次の2つだけ。

1. GitHub direct write
2. ChatGPT Library `/LLM-survey-outbox/pending/`

Google Drive、Notion、旧 `/LLM-survey-fallback/` は使わない。

GitHub write失敗時:

1. 対象の最新blob SHA / repo状態を取り直し、その対象だけ1回再試行。
2. まだ失敗する場合、そのrun最初のwrite失敗に限り `.survey/work-queue/transport/health-probe.json` を1回更新。
3. probe成功 → 対象固有障害。影響payloadだけLibraryへcheckpointし、他のGitHub writeは継続。
4. probe失敗 → run-wide障害。そのrunではGitHub writeを繰り返さない。Research / Audit中なら現在の1論文だけをLibraryへcheckpointし、GitHub上の成功resultと最新main反映を確認できないため**次の論文へ進まない**。Discovery中も正規precheck/result要件を飛ばして新ラウンドを捏造せず、既に得た成果だけをLibraryへ耐久保存する。
5. GitHub direct writeとLibrary保存の両方が不能な場合だけ、未保存成果を増やす前に停止。

**Scheduled Task自体を一時停止・無効化してはならない。** GitHub/API/Actions/Library障害、今回runのhard stop、ノルマ未達、その他の一時障害があっても、Scheduled Chat / automationのenabled状態は維持する。停止とは今回runの安全終了だけを意味し、将来runのスケジュール停止を意味しない。

Research/AuditのLibrary fallbackは1論文1envelopeで、root-level identityと完全5スロットを持たせる。復旧は `.survey/work-queue/fallback-inbox/<id>.json` から現行immutable submissionへ収束させる。

過去形式を読み込む互換コードが内部に存在しても、ワーカーが旧形式を新規生成してはならない。

## 7. 待機・継続・終了

継続判断には `.survey/scripts/continuation_gate.py`、最終化判断には `.survey/scripts/run_finalization_gate.py` を使う。

- claim/resultやsubmission/resultが次の安全な判断に必要なら、同一targetを10秒実時間間隔で再確認する。
- Research / Audit のsubmission result待ちは**次論文へ進むための同期障壁**である。成功resultと最新main反映を確認するまで次の論文をclaim・取得しない。待ち時間には同一論文のrepair準備や次論文を取得しない状態整合作業だけを行う。
- candidate在庫、Library pending、fallback backlog、record bank枯渇、単一job失敗、1本完了、単一探索軸0件だけをrun終了理由にしない。
- final responseはfinalization gateが許可した場合だけ行う。
- 600秒handoff guardに入ったら新規独立作業を開始せず、現在成果を耐久保存して引き継ぐ。

## 8. 誤経路に入った場合

実行可能スクリプトが標準エラー出力（stderr）へ出す `[WORKER-GUIDE]` は、そのコマンド実行中の**必須行動指示**である。ワーカーは表示された順番に従い、ガイドが明示した完了条件を満たす前に次段へ進まない。

- `[待機]`: 完了またはエラー案内が出るまで、その処理に依存する次操作を開始しない。処理中に別の同目的スクリプトへ切り替えない。
- `[完了]` と `[次]`: 正常終了後の後続手順。記載されたスクリプト、結果ファイル、進行条件を順番どおり確認する。結果ファイルの `next_action` / `instructions` がある場合は併せて従う。
- `[手順エラー]` と `[正しい手順]`: その場で別経路へ迂回せず、示された復旧手順で同じ現行入口へ戻る。旧schema・manual手順・直接state編集で回避しない。
- JSON等の機械可読出力はstdout、ワーカー向け案内はstderrで分離される。案内をJSON本文として扱わない。

検証処理が `next_action` または `recovery_steps` を返した場合、それがその実行時点の復帰手順の最優先指示である。この文書と矛盾して見える場合も機械案内に従い、矛盾を隠さず最終報告の相談事項へ残す。

ワーカーは次を行う。

1. 最新HEADと対象stateを再取得する。
2. エラーが示した現行入口へ戻る。
3. 同一payloadの二重投入を避ける。
4. 旧schema、旧manual workflow、固定 `chat-inbox.json`、旧fallbackへ迂回しない。

「エラーになったので別の古い経路を試す」は禁止する。

## 9. 08:30更新とmaintenance

毎時 `:30` のScheduled Chatから起動したworkerのうち、**08:30 JSTのrunだけ**を日次更新・maintenance専用runとする。このrunではResearch / Audit / Discoveryを行わない。

実行順序は固定する。

1. 先に `framework-updates/**`、`llm-releases/**` と必要な `.survey/update-worker/**` の非論文更新を確認し、必要な変更を最新 `main` へ耐久反映する。
2. 非論文更新の保存が完了した後、**runの最後の独立作業としてmaintenanceを実行する。**
3. maintenanceは `.survey/work-queue/maintenance-cycle.json` の `maintenance_pending=true` を耐久反映して `.github/workflows/maintenance.yml` を起動し、GC、index再構築、品質・メタデータ監査、整合性確認を直列実行させる。
4. maintenance workflowの結果を確認し、可能なら完了後の最新 `main` と `maintenance-cycle.json` を再取得して、`maintenance_pending=false` と結果状態が耐久反映されたことまで確認する。
5. 最終報告には非論文更新点に加え、maintenanceの起動・完了状態、GC/監査/整合性確認の結果、最終main SHAを含める。

maintenance実行の責任は08:30 JSTの `:30` workerに集約する。通常runでは定期maintenanceを発火させず、旧run-countカウンタも実行条件に使わない。
