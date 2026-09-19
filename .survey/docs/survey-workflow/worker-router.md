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

## 2. 役割分岐

通常論文ワーカーは毎時 `:30`、探索主体ワーカーは毎時 `:00` を基本とする。08:30 JSTはフレームワーク・LLM更新専用である。

通常論文ワーカーでは、研究・監査・探索より先にmaintenance状態を確認する。

1. `maintenance_pending = true` または24回周期のmaintenance対象 → maintenance専用。
2. 08:30 JST → その他更新専用。
3. 毎時 `:00` の探索主体ワーカー → 下記の在庫水位で探索または overflow research mode。
4. それ以外の通常論文ワーカー → Research / Auditを優先し、必要に応じてDiscoveryを補充。

探索主体ワーカーの切替条件:

- **`candidate_inventory > 50`** かつ実行可能なResearch/Auditあり → **overflow research mode**。通常論文ワーカーと同じ研究処理へ入る。
- 50以下、または実行可能なResearch/Auditなし → Discovery mode。

通常論文ワーカーの候補水位:

- `candidate_inventory > 50`: Research / Auditのみを優先。
- 25〜50: Research / Auditを優先し、新規Discoveryを行わない。
- 15〜24: Researchを進めながらDiscovery補充を積極化。
- 0〜14: 枯渇防止のためDiscovery比重を上げる。
- 実行可能なResearch/Auditが0: Discoveryへ進む。

件数維持のために弱い候補を採用しない。

## 3. Research / Audit の唯一の処理ループ

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

## 4. Discovery の唯一の入口

新規Discoveryは**固定ソース precheck schema v3** だけを使う。ワーカーが検索結果を数件だけ手でJSONへ詰め、schema v1/v2として投入してはならない。

requestは `.survey/work-queue/discovery-precheck/requests/<request-id>.json` に保存し、少なくとも次を含める。

```yaml
schema_version: 3
operation: precheck_discovery_candidates
provider: openalex | semantic_scholar | openalex_references
source_url: <固定した検索/API URL>
collector_id: <同一探索軸の識別子>
run_key: <今回runの識別子>
axis: <探索軸>
target_unseen: 20
```

`target_unseen` の既定値は20。precheck側の `discovery_provider_adapter.py` と `collect_until_unseen()` が**同じ検索結果をページ送り**し、各ページで既収録・既候補・既却下・ページ間重複を除外する。ワーカーが2ページ目以降を個別に手作業で継ぎ足す必要はない。

評価に使ってよい候補は、schema v3 resultが `evaluation_allowed=true` として返した `allowed_records` だけである。precheck resultが未完了なら、旧schemaへ逃げずに同じ現行経路を完了させる。

### 4.1 探索方法

次の3経路はすべて同じschema v3 precheckを通す。

1. 通常検索・新着検索: OpenAlex / Semantic Scholar等の固定検索URL。
2. backward reference（収録論文が引用している論文）: `openalex_references` 等、参照先を列挙できる固定ソース。
3. forward citation（収録論文を引用している論文）: OpenAlex等の被引用検索を固定ソースとして指定。

OpenAlexで直接ページ送り・引用関係を取得できる場合はOpenAlexを優先してよい。提供元を変える場合は別探索軸として記録する。

### 4.2 Candidate投入

Discoveryは軽量評価だけを行う。title、abstract、書誌、一次資料の存在、テーマ適合性、新規性の見込みを確認し、全文精読はResearchへ送る。

1回のDiscovery submissionへ送るcandidateは0〜5件。**5件はrun上限ではなく1 submissionの上限**である。

探索主体ワーカーのmulti-round submissionは自己記述型（self-describing）を使い、存在しないDiscovery `job_id` を合成しない。candidate投入前に最新HEAD / identity / queueを再確認する。

1探索軸が0件、全重複、低採用率、単一provider障害でも、それだけでrunを終わらせない。通常検索、forward citation、backward reference、隣接分野、query family、providerを切り替える。ただし `candidate_inventory > 50` へ達した場合はoverflow research modeへ切り替える。

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

08:30 JSTの更新workerは `framework-updates/**`、`llm-releases/**` と必要な `.survey/update-worker/**` だけを扱う。同じrunでResearch / Audit / Discoveryを行わない。

maintenance runは `.github/workflows/maintenance.yml` に委譲し、GC、index再構築、品質・メタデータ監査、整合性確認を直列実行する。探索主体ワーカーの `:00` runは通常論文ワーカーの24-run maintenance counterへ加算しない。
