# Worker router — workflow v10

この文書はScheduled Chat / Work系ワーカー（worker）の**唯一の実行手順正本**である。役割分岐（routing）、継続・停止、探索、研究、退避の判断を別文書から組み立て直してはならない。

実装詳細が必要な場合だけ `queue-v10.md` 等の実装リファレンス（implementation reference）を参照する。実装リファレンスと本書が競合する場合、ワーカーの行動は本書を優先する。

**実行中にリポジトリの正規スクリプトが `[WORKER-GUIDE]` を出した場合、ワーカーはそのガイドに従うこと。** `[待機]` 中に依存する次操作へ進んだり、`[次]` を自己判断で飛ばしたり、`[手順エラー]` / `[正しい手順]` を無視して別経路へ迂回してはならない。ガイドと機械可読resultの `next_action` / `recovery_steps` が併存する場合は、両方を満たす手順を実行する。

## 1. 開始時に読む状態

各実行（run）の開始時に最新 `main` HEADを取得し、同じHEADで次を読む。

- `.survey/work-queue/next-jobs.json`
- `.survey/work-queue/maintenance-cycle.json`
- `.survey/work-queue/discovery-state.json`
- 必要なら `.survey/work-queue/state.json`
- 出力品質が必要な場合は `.survey/templates/paper.md`

実際の起動時刻を1回取得し、`actual_invocation_start` として固定する。予定時刻や前回runの時刻を再利用しない。通常の時間枠は起動時刻から3600秒で、残り600秒以下では新しい独立作業を開始しない。残り180秒以下では耐久保存と安全な引き継ぎだけを行う。

## 2. 共通ルーター

毎時 `:00` と毎時 `:30` の論文ワーカーは、**同じタスク・同じ手順**を使う。スケジュール時刻による役割差は設けない。run開始時に最新状態から `candidate_inventory` を取得し、次の1条件だけで今回の論文作業モードを決める。

- **`candidate_inventory >= 50` → 探索（Discovery）**
- **`candidate_inventory < 50` → 読解（Research / Audit）**

maintenance対象または08:30 JSTの専用更新条件だけは、この分岐より優先して専用経路へ入る。

モード決定後は、どちらのScheduled Chatから起動したかを一切条件分岐に使わない。探索なら第4節、読解なら第3節の共通手順をそのまま使う。`:00` 専用・`:30` 専用の探索手順、読解手順、overflow modeは作らない。

候補数は最新の耐久状態から毎run取得し、旧runや旧STATUSの推定値を再利用しない。候補数が境界ちょうど50件なら探索を選ぶ。

ノルマは維持する。

- **読解モード**: 今回の起動中に新規論文を最低3本、一次資料全文→5スロット→preflight→不変submission→最新mainへの耐久反映まで完了させる。3本は停止上限ではない。
- **探索モード**: 最低4つの materially distinct なDiscovery roundを耐久保存する。4 roundは停止上限ではない。単一roundの0件・重複のみでは終了しない。

handoff guard、platform/context limit、GitHub正本の読取不能、GitHub/Library双方への耐久保存不能などのhard stopはノルマより優先する。件数を満たすために弱い候補を採用したり、読解品質を下げたりしない。
## 3. 読解（Research / Audit）の共通処理ループ

1. 最新queueと現在の担当確保状態（claim state）を取得する。
2. priority最上位の実行可能jobを**1件だけ**担当確保する。`max_jobs=1`。同一ワーカーが未完了claimを複数保持しない。
3. claim result待ちなら同じ `request_id` を保持する。別requestを発行して回避しない。次の安全な判断に結果が必要な場合だけ10秒の実時間間隔で同じ対象を再確認する。
4. claim resultの `record_bank` / `record_bank_fallback` をそのまま使う。ワーカーが別bankを選び直さない。
5. 一次資料本文を最後まで読み、抄録や検索断片から欠落情報を推測しない。
6. `metadata`、`problem_method`、`evaluation`、`results`、`positioning` の5スロットを完成させる。
7. Actionsと同じ基準で事前検査（preflight）する。
8. GitHubへ保存可能なら各スロットの実blob SHAを取得し、attempt固有の不変descriptorを `.survey/work-queue/submissions/research/` または `audit/` へ保存する。
9. GitHub書込みがrun全体で利用不能なら、完全な5スロットpayloadをChatGPT Library `/LLM-survey-outbox/pending/` へ1論文1envelopeで保存する。
10. 完全payloadが耐久保存されたら、前jobのGitHub Actions完了を同期障壁にせず最新queue / claim stateを取り直し、次の独立作業へ進む。

禁止事項:

- 固定 `submissions/chat-inbox.json` を生成・更新しない。
- 完成MarkdownをScheduled Chatから直接送らない。
- claim resultが返したbankを無視して別bankへ書かない。
- 1本処理したことだけをrun終了理由にしない。

### 3.1 実運用で確立した高スループット原則

以下は品質基準を緩める高速化ではなく、全文精読・検証・耐久保存を維持したまま重複作業を減らすための標準手順である。

1. **全文読解済み成果を捨てない。** 初回全文精読後はrecord bankと既存5スロットを再利用し、validation失敗時は指摘されたslotだけを一次資料に基づいて修復する。一次証拠が不足・変更していない限り、全文を最初から読み直さない。
2. **初回5スロットをvalidator下限ぎりぎりにしない。** 問題設定は「問題＋既存法で解けない理由」、method overviewは入力から出力までのend-to-end流れ、各componentは「入力・内部処理・出力・他componentとの接続」を十分に記述する。短すぎる説明によるrepair往復を減らす。
3. **一次資料は取得できた時に一度で必要範囲を読む。** 完全なarXiv HTMLが使えるなら優先し、必要ならPDF、OpenReview/会議公式、著者・プロジェクト公式コピーへ進む。同一資料を小分けに再取得せず、手法・評価・結果・ablation・限界・関連研究までまとめて確認する。
4. **1経路の取得失敗をwhole-run failureにしない。** materially distinctな公式経路を試し、なお全文取得不能ならstatus-only `blocked` を耐久保存して次の独立jobへ進む。`blocked` descriptorは `schema_version` / `transport_version` / `kind` / `attempt_id` / `job_id` / `claim_id` / `worker_id` / `status` / `reason` / `retrieval_evidence` / `blocked_at` だけを持つ状態専用transportとし、`record_bank`、`paper_path`、`record_slots`、`expected_blob_sha` その他のrecord transport fieldを絶対に混在させない。一時障害の `blocked` と、一次証拠で再試行不要と確定した `rejected` を混同しない。
5. **非同期待ちを不要な同期障壁にしない。** claim/result/submissionの同じIDを保持して所定間隔で確認し、待ち時間には次候補の一次資料経路確認、identity/queue同期、既読slot整理などclaim競合を起こさない準備を行う。未完了claimを増やしたり同一requestを重複発行しない。
6. **canonical stateを再利用する。** claim前・submission後・repair時に最新queue、identity、rejection ledger、result、record bankを使い、重複claim・重複探索・重複取得を避ける。Research claimは常に1件だけ保持し、完了またはstatus-only耐久保存後に次へ進む。
7. **読解3本ノルマは維持する。** `papers_added_this_invocation < 3` の間は、hard stopまたはhandoff guardでない限り読解を継続する。3本到達は停止上限ではなく、continuation/finalization gateが継続を要求するなら次のResearch / Auditへ進む。取得枠を節約するため、再取得より既存成果の局所修復を優先する。

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
- この経路からResearch jobを直接生成しない。Candidate投入以降は4.2〜4.3の一本道へ合流する。

### 4.1.2 系統限定の最新被引用探索（lineage-scoped forward-citation refresh）

特定の系統ページにある収録済み論文を**種論文（seed papers）**として、その論文を引用する後続研究から最新の有力候補を拾う方法。既存論文の引用先を掘るstructured-reference curationとは逆方向なので、直近数か月の新手法を拾うのに向く。通常runでも後方引用と並ぶ主経路として使い、`repository_references` の枯渇を待たない。ユーザーが「この系統を引用する最新論文を探して」のように明示した場合は、上記の明示ユーザー指定探索として対象系統を即時実行してよい。

効率化の標準手順:

1. **系統全体を種集合にする。** READMEだけでなく、その系統ディレクトリ内の収録論文の正規識別子（canonical ID）を列挙する。最初は、引用が十分蓄積している代表論文・基礎論文から始める。1本で十分な新規候補が出る場合、全種論文を同時に走査しない。
2. **最新順を保証できる固定ソースを優先する。** OpenAlexでWork IDを解決できる場合は `/works?filter=cites:W...&sort=publication_date:desc` を固定 `source_url` とし、必要なら公開日範囲も付ける。Semantic Scholarを使う場合は対象論文の `/citations` エンドポイントを固定ソースにする。検索語だけの類似検索に置き換えない。
3. **schema v3事前検査（precheck）へ渡す。** 原則 `target_unseen: 20`。同一固定ソースのページ送りは `collect_until_unseen()` に任せ、既収録・既候補・既却下・ページ間重複を自動除外する。引用件数が大きい種論文でも、ワーカーが先頭数件だけ手で抜かない。
4. **新しいものから軽量評価する。** `allowed_records` を公開日降順で見て、対象系統への直接性を確認する。「種論文を引用している」だけでは採用理由にせず、既存系統をどの軸で更新するか（例: expert数の適応配分、expert pruning/merging、圧縮後回復、実測serving改善）をreasonに書く。
5. **1 submissionは強い候補だけ0〜5件。** 5件を埋めるための弱い候補は入れない。候補化後は4.2〜4.3の通常経路へ合流し、Research jobを直接生成しない。
6. **次の種論文へ進む条件を明確にする。** 1本の種論文から十分な強候補が得られたら、そのsubmissionを先に耐久保存する。続行時は同じ種論文を再度precheckしてidentity snapshotにより既候補を飛ばすか、別の種論文へ移る。複数種で同じ後続論文が出てもshared identityで重複除外させる。
7. **探索効率を記録する。** `discovery_stats.search_windows` に種論文、引用方向 `forward`、取得件数、未収録件数、評価件数、採用件数を残す。後続runでは採用率の高かった種論文を優先し、0件が続く種論文を毎回先頭から調べ直さない。

この方法が特に有効なのは、既存系統が2024〜2025年の代表論文を含み、2026年の新手法がその代表論文を関連研究として引用し始めている場合である。単純なキーワード検索より、対象系統との接続根拠を保ったまま最新研究へ追従しやすい。

### 4.2 探索ノルマ

探索モードでは、hard stopまたはhandoff guardがない限り、**最低4つの materially distinct なDiscovery round**を耐久保存する。4 roundは停止上限ではない。1 round完了、0件、重複のみ、単一provider障害、単一探索軸の飽和は終了理由にしない。4 round到達後も有望な次軸がある場合は継続する。

### 4.2 Candidate投入

Discoveryは軽量評価だけを行う。title、abstract、書誌、一次資料の存在、テーマ適合性、新規性の見込みを確認し、全文精読はResearchへ送る。

**Candidate priorityには、テーマ適合性・重要性だけでなく「新しさ」と「主要な査読会議・学会への採択実績」も加味する。** これらはResearchの読む順を決めるための補助点であり、テーマとの直接性や研究上の重要性を逆転させるほど過大に重み付けしない。

- **新しさ（recency）**: 公開・採択時期が新しい候補を加点する目安として、直近6か月は `+4`、6〜12か月は `+3`、12〜24か月は `+1`、それ以前は `+0` とする。基礎的重要論文は古さだけで減点・除外しない。
- **主要会議・学会採択（major-venue acceptance）**: NeurIPS / ICML / ICLR / MLSys / OSDI / SOSP / NSDI / USENIX ATC / EuroSys / ASPLOS / ISCA / MICRO / HPCA 等、その分野で主要とみなされる査読付き会議・学会への採択が既知なら `+3` を目安に加点する。その他の信頼できる査読付きvenueへの採択が既知なら `+1` を目安とする。venue名だけで機械的に判断せず、対象分野との対応を優先する。
- **情報不明時**: 採択状況・venueが不明なら `+0` とし、推測しない。arXivのみであること自体を減点理由にはしない。
- **追加ネットアクセス禁止**: 新しさや採択状況の採点だけを目的として追加のWeb/APIアクセスを発生させない。schema v3 precheck、既に取得したOpenAlex / Semantic Scholar / arXiv / OpenReview /会議公式等の結果、既存metadata、一次資料中の書誌情報に含まれている範囲だけを使う。既存取得情報にない場合は未確認のまま `+0` とする。
- candidateの `reason` には、priorityを押し上げた主要因が新しさ・主要venue採択である場合、その事実を短く残す。採択が確認できないものを「採択済み」と書かない。
1回のDiscovery submissionへ送るcandidateは0〜5件。**5件はrun上限ではなく1 submissionの上限**である。

Discoveryのmulti-round submissionは、どちらのwork mixから探索を選んだ場合でも自己記述型（self-describing）を使い、存在しないDiscovery `job_id` を合成しない。candidate投入前に最新HEAD / identity / queueを再確認する。

### 4.3 Discovery submissionからResearchへの一本道

Discovery後半は次の順序を正規経路とする。途中を手作業で代替してはならない。

1. `process_discovery_precheck.py` のschema v3 resultが `READY_FOR_EVALUATION` / `evaluation_allowed=true` になったことを確認する。
2. `allowed_records` だけを軽量評価し、候補0〜5件を `operation: submit_discovery_round` の不変submissionとして `.survey/work-queue/submissions/<unique>.json` に保存する。submissionは対応するprecheck result path / receiptを参照する。
3. `queue_worker.py` にsubmission処理を任せる。workerはResearch job IDを合成したり、`jobs/*.json` / `state.json` を直接書き換えたりしない。
4. 同名の `.survey/work-queue/results/<unique>.json` を確認し、`ok=true`、`research_jobs_added`、`final_duplicate_filtered_count`、`next_action` を読む。
5. `refresh_queue_snapshot.py` または `queue_worker.py` が更新した `.survey/work-queue/next-jobs.json` を確認する。
6. ready Research/Audit が現れたら `claim_worker_with_banks.py` の正規claim経路で**1件だけ**取得する。割当て後はclaim resultが指定したrecord bankを使い、Research処理へ進む。
7. `research_jobs_added=0` でもrun終了理由にしない。最終重複排除や低優先度除外を確認し、必要なら別探索軸をschema v3 precheckから開始する。

失敗submissionの回収には `recover_discovery_submissions.py` を使う。回収後は `refresh_queue_snapshot.py` → `next-jobs.json` → `claim_worker_with_banks.py` の順へ戻る。失敗済みsubmissionを上書きしたり、synthetic `job_id` を作って回避してはならない。

引用優先runでは、後方引用の候補山が残っていても前方引用へ進む。逆に前方引用が0件でも後方引用の山は継続する。**通常検索へ進めるのは、同じrun_keyで後方引用と前方引用の両方を試した後だけ**とし、通常検索は引用グラフで空く領域を埋める用途に限定する。単一provider障害は「0件」とみなさず、同じ引用方向の別providerまたは別種論文を試す。1 Discovery roundが耐久保存まで完了したら共通ルーターへ戻り、work mixと最新状態から次の作業種別を再選択する。

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
4. probe失敗 → run-wide障害。そのrunではGitHub writeを繰り返さず、Libraryへ耐久保存して作業継続。
5. GitHub direct writeとLibrary保存の両方が不能な場合だけ、未保存成果を増やす前に停止。

Research/AuditのLibrary fallbackは1論文1envelopeで、root-level identityと完全5スロットを持たせる。復旧は `.survey/work-queue/fallback-inbox/<id>.json` から現行immutable submissionへ収束させる。

過去形式を読み込む互換コードが内部に存在しても、ワーカーが旧形式を新規生成してはならない。

## 7. 待機・継続・終了

継続判断には `.survey/scripts/continuation_gate.py`、最終化判断には `.survey/scripts/run_finalization_gate.py` を使う。

- claim/resultやsubmission/resultが次の安全な判断に必要なら、同一targetを10秒実時間間隔で再確認する。
- 結果待ち中でも独立作業が安全にできる場合は、それを先に処理し、待機を不要な同期障壁にしない。
- candidate在庫、Library pending、fallback backlog、record bank枯渇、単一job失敗、1本完了、単一探索軸0件だけをrun終了理由にしない。
- final responseはfinalization gateが許可した場合だけ行う。
- 600秒handoff guardに入ったら新規独立作業を開始せず、現在成果を耐久保存して引き継ぐ。

## 8. 誤経路に入った場合

実行可能スクリプトが標準エラー出力（stderr）へ出す `[WORKER-GUIDE]` は、そのコマンド実行中の**必須行動指示**である。ワーカーは表示された順番に従い、ガイドが明示した完了条件を満たす前に次段へ進まない。

- `[待機]`: 完了またはエラー案内が出るまで、その処理に依存する次操作を開始しない。処理中に別の同目的スクリプトへ切り替えない。
- `[完了]` と `[次]`: 正常終了後の後続手順。記載されたスクリプト、結果ファイル、進行条件を順番どおり確認する。結果ファイルの `next_action` / `instructions` がある場合は併せて従う。
- `[手順エラー]` と `[正しい手順]`: その場で別経路へ迂回せず、示された復旧手順で同じ現行入口へ戻る。旧schema・manual手順・直接state編集で回避しない。
- JSON等の機械可読出力はstdout、ワーカー向け案内はstderrで分離される。案内をJSON本文として扱わない。

検証処理が `next_action` または `recovery_steps` を返した場合、それが復帰手順の正本である。

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
