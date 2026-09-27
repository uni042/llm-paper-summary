Warning: truncated output (original token count: 45494)
Total output lines: 712

# Worker router — workflow v10.22

この文書はScheduled Chat / Work系ワーカー（worker）の**唯一の実行手順正本**である。役割分岐（routing）、継続・停止、探索、研究、退避の判断を別文書から組み立て直してはならない。

ワーカーは実装リファレンス（implementation reference）や履歴互換資料（read-compatibility material）から手順を補完しない。必要な実装詳細は正規スクリプトが `[WORKER-GUIDE]`、`next_action`、`recovery_steps` として返す。実装リファレンスは保守・テスト用途に限定する。

**実行時の具体的な操作では、正規スクリプトが返す `[WORKER-GUIDE]` / `next_action` / `recovery_steps` を最優先する。** `[待機]` 中に依存する次操作へ進んだり、`[次]` を自己判断で飛ばしたり、`[手順エラー]` / `[正しい手順]` を無視して別経路へ迂回してはならない。機械案内とこの文書が矛盾した場合は、旧経路へ逃げず**そのrunでは機械案内に従って安全に処理し、矛盾の内容・採用した機械案内・影響を最終報告でユーザーへ相談事項として明記する。** ワーカーがその場で正本の意味を独自に上書きしない。

## 0.1 通常チャットからのLibrary成果取り込み経路

Scheduled Chat / WorkワーカーがGitHub本文書込みを拒否された場合、完成した論文解説または探索結果をChatGPT Libraryへ耐久退避してよい。退避ファイルには少なくとも対象identity、対象系統、参照main SHA、想定GitHub配置先、完成状態を持たせる。

ユーザーが通常チャットからLibrary退避成果のGitHub反映を明示指示した場合、その通常チャットは**取り込み専用の臨時反映者**として扱う。この操作はScheduled worker runのclaim・ノルマ・run-stateを再実行するものではなく、Libraryに既に完成保存された成果を最新mainへ移送するための独立経路である。

取り込み時は次の順序だけを使う。

1. Libraryからユーザーが指定した成果、または「未反映の任意の論文／探索結果」として指定された成果を取得する。
2. 最新mainを読み、同じmain上の本routerと対象フォーマット／配置規則を確認する。
3. Library成果のidentityと想定配置先を確認し、現在の正規配置と異なる場合は最新main側を優先して正規化する。**対象pathだけを見る前に、canonical_id / arXiv ID / DOI / OpenReview IDを使ってrepository全体の既収録paper identityを照合する。** 通常チャット取り込みでは `.survey/scripts/resolve_paper_identity.py` をstable identity付きで実行し、`status=represented` なら返された `paper_path` をupdate対象とする。`status=not_found` の場合だけ新規create候補として扱う。同一identityが別pathに存在する場合は新規createせず、その既存paperを現在のcanonical配置として統合/updateする。identity indexが一時的に古い場合でもresolverは `papers/**` 実体から再構築するため、実体照合を省略しない。
4. repository全体のidentity照合後、確定した対象pathを最新mainで取得する。未存在ならcreate、既存なら現在blob SHAを取得して内容を統合したうえでupdateする。古いLibrary記録のSHAをwrite前提に使わない。**同じcanonical identityの第二ファイルを作成してから後で重複解消する運用は禁止する。**
5. write後に同じpathをmainから再取得し、反映内容とcommitを確認する。
6. 論文本文を通常チャット経路から追加した場合、paper push後の正規reconciliationが実論文MarkdownとResearch jobをstable identity / declared paper_pathで照合する。既に本文が表現済みの `ready` Research jobは、通常Research完了を偽装せず `status=superseded` / `superseded_reason=paper_already_represented` として終端化する。派生 `next-jobs` とworker worklistも論文実体を再照合し、reconciliation commitが一時的に遅れても既収録論文を未処理として再提示しない。
7. 論文frontmatterの `references` は既存の構造化reference poolへ自動供給される。引用論文を通常チャット取り込み時に直接Research job化せず、Discoveryの重複除外・対象判定を通してから候補化する。引用情報が未記録の論文は通常のResearch/Auditメタデータ整備で補完し、取り込み経路だけで推測生成しない。
8. 論文本文、探索結果、候補リストのいずれもこの経路で取り込める。ただし、探索結果は現在のDiscovery正規フォーマット／配置先へ変換し、claim・reservation・submission等の制御ファイルを「取り込み済みに見せる」目的では生成しない。
9. GitHub writeが拒否された場合は回避せず、Library原本を残して失敗段階を報告する。Scheduled Task自体の有効状態・schedule・通知設定は変更しない。

この経路では、ユーザーが「保存したものをGitHubへ上げて」「Libraryの未反映分を反映して」「この論文／探索結果を入れて」等と明示したことを、その成果をmainへ反映するwrite承認として扱う。対象が曖昧な場合だけLibraryの未反映成果を列挙して選択を求める。

## 1. 開始時に読む状態

各実行（run）の開始時に最新 `main` HEADを取得し、同じHEADで次を読む。

- `.survey/work-queue/hot-dispatch.json`（存在する場合。ゼロ待ち開始用の再構築可能index）
- `scheduled-chat-00`: `.survey/work-queue/worker-worklist-00.json`（Research / Audit最大200件・Discovery最大500件の専用index）と `.survey/work-queue/WORKLIST-00.md`
- `scheduled-chat-30`: `.survey/work-queue/worker-worklist-30.json`（Research / Audit最大200件・Discovery最大500件の専用index）と `.survey/work-queue/WORKLIST-30.md`
- `.survey/work-queue/next-jobs.json`
- `.survey/work-queue/maintenance-cycle.json`
- `.survey/work-queue/discovery-state.json`
- 必要なら `.survey/work-queue/state.json`
- 出力品質が必要な場合は `.survey/templates/paper.md`

実際の起動時刻を1回取得し、`actual_invocation_start` として固定する。予定時刻や前回runの時刻を再利用しない。**タイムゾーン情報を必ず保持し、JSTの壁時計を `Z` / `+00:00` として偽装しない。** `actual_invocation_start` は今回runの成果件数・identity・履歴境界を決めるために使うが、通常runの終了時刻・開始禁止窓・handoff時刻の算出には使わない。`next_scheduled_task_at` / `seconds_to_next_scheduled_task` / `seconds_to_run_deadline` 等の旧時間fieldがsnapshotに残る場合も**観測・互換用テレメトリに限定し、作業開始禁止・最終化・handoff・stop permitの根拠にしてはならない。通常runは次のScheduled Task時刻や起動後経過時間だけでは終了しない。**

### 1.1 run identity と scheduled slot

通常のScheduled Chat論文ワーカーは、実行ごとに名前を作り直さず**固定worker identity**を使う。

- 毎時 `:00`: `worker_id = scheduled-chat-00`, `scheduled_slot = 00`
- 毎時 `:30`: `worker_id = scheduled-chat-30`, `scheduled_slot = 30`
- 08:30専用run: `worker_id = scheduled-chat-30`, `scheduled_slot = 0830`

これに加えて、単発・臨時ワーカーは **`worker-N`（Nは0〜999999の数字）** を正式identityとして使用できる。単発ワーカーは `scheduled_slot = adhoc` とし、claim / 共有preload FIFO / Research-Audit品質preflight / immutable submission / run-stateの同じ正規経路へ参加する。`worker-N` を `:00` / `:30` / `0830` と偽装してはならず、08:30 maintenanceも担当しない。同時稼働する単発ワーカー同士では異なるNを使い、同一Nを再利用する場合はそのworkerの未完了claimを引き継ぐものとして扱う。

`worker_kind` は固定Scheduled Chatと `worker-N` の両方でtransport互換上 `scheduled_chat` とする。claim request、Library checkpoint marker、fallback envelope、run-state request、最終報告でこのidentityを一貫して使う。別名・時刻埋め込み名・共通名 `scheduled-chat-llm-survey` を新規runで生成しない。これにより各worker lineageを分離し、互いのactive claimを自分のclaimとして扱わない。

各runに一意な `run_key` を1つ作り、Discovery、run-state snapshot、最終報告まで同じ値を使う。`worker-N` も必ずrun-state requestを作り、固定2workerと同じ継続判定を使用する。

また、実際の起動時刻とは別に**予定実行枠（scheduled slot）**を開始時に確定してrun中固定する。`:00` workerは `HH:00`、`:30` workerは `HH:30` の予定枠を使う。08:30専用runの判定は実際の起動時計ではなく予定実行枠で行う。たとえば08:34に遅延起動しても予定枠が08:30なら第9節へ入り、09:30枠が08:59に早期起動した等の異常でも08:30専用runとは扱わない。

## 2. 共通ルーター

毎時 `:00` と毎時 `:30` の論文ワーカーは、**同じ論文処理規約・同じ手順**を使う。スケジュール時刻による役割差は設けない。run開始時に最新 `next-jobs.json` から **Research/Audit の ready 全件数**を `candidate_inventory` として取得する。`claimable` ではなく、原則 `claiming.ready_research_audit`、それが無ければ `counts.research.ready + counts.audit.ready` を使う。このrun開始時の値を固定し、まず次の基本閾値で今回の論文作業モードを決める。

- **`candidate_inventory >= RESEARCH_DISCOVERY_THRESHOLD` → 読解（Research / Audit）**
- **`candidate_inventory < RESEARCH_DISCOVERY_THRESHOLD` → 探索（Discovery）**

ただし、Research在庫が閾値近傍で長時間維持されることでDiscoveryが永久に後回しになることを防ぐため、`.survey/scripts/claim_window_policy.py` の**探索鮮度オーバーライド**を基本閾値より優先する。現在は、最後に耐久完了したDiscoveryから **2時間以上**経過し、かつ `candidate_inventory <= 360`（288件の基本閾値 + 6 worker × 12件の1 window）なら、その新規runをDiscoveryへ送る。直近Discovery完了時刻を直接確認できない場合はこのオーバーライドを推測適用せず、基本閾値だけを使う。360件を超える大きなResearch backlogではResearchを優先する。

**この件数閾値は今回runでどちらを優先して処理するかを選ぶルーティング規則であり、Research / Discoveryどちらかのバンク・preload・direct-take機構を無効化する能力ゲートではない。** 二重用途バンクでは両レーンの在庫を同時に維持し、件数が閾値の上下どちらにあっても仕組み側はResearchとDiscoveryの両方を利用可能な状態に保つ。選ばれなかったレーンはそのrunで通常処理しないだけで、在庫生成・preload維持・次runからの利用を止めない。

閾値は `.survey/scripts/claim_window_policy.py` の正規policyから導出する。現在は、**各workerの論理在庫12件 × 容量設計上の同時worker基準6 × 4 = 288件**である。この6は在庫量・閾値を決める**容量サイジング基準であって参加worker数の上限ではない**。`worker-N` は6を超えても正規参加でき、共有poolを利用する。worker数・在庫幅の設計値を変更するときは閾値だけを別に手修正せず、同policyから連動させる。

**08:30 JSTの`:30`専用runだけ**は、この分岐より優先して第9節の日次更新・maintenance経路へ入る。通常runに「maintenance対象」という別条件は設けない。

モード決定後は、どちらのScheduled Chatから起動したかを一切条件分岐に使わない。探索なら第4節、読解なら第3節の共通手順をそのまま使う。`:00` 専用・`:30` 専用の探索手順、読解手順、overflow modeは作らない。

候補数は最新の耐久状態から毎run開始時に取得し、旧runや旧STATUSの推定値を再利用しない。候補数が現在の境界ちょうど288件なら、探索鮮度オーバーライドが発火しない限り読解を選ぶ。探索鮮度は耐久保存されたDiscovery完了時刻からrun開始時点までを計算し、`hot-dispatch.json` の `discovery_age_seconds` / `discovery_refresh_due` はこの判定の観測面である。**一度選んだモードはそのrunの終了まで固定する。** run中に候補数や探索鮮度が境界を跨いでも再ルーティングしない。次回runの開始時にあらためて最新状態で判定する。Discovery freshness runは既存Research claimを破棄・解放する操作ではなく、そのrunでDiscoveryを優先するだけである。

runノルマの正規値は `.survey/scripts/worker_quota_policy.py` に一元化する。現在はResearch / Audit成功5件、Discovery成功8ラウンドである。Audit starvation防止の3件ブロックも同policyに置くが、これは**作業配分の公平性規則でありrun完了ノルマではない**。

- **読解モード**: 今回の起動中に **Research / Audit 合計で成功完了を最低5件**作る。Research job 1件とAudit job 1件は、同じ論文に対するものでも**別々に1件ずつ**数える。Researchは一次資料全文→5スロット→ワーカー自身のセルフレビュー→exact blob preflight合格→不変submission→submission result成功→最新mainへの反映確認まで、Auditも同じ提出前ゲート→不変submission→成功result→最新mainへの反映確認までを1件の完了とする。`blocked` / `deferred` / `rejected` や提出しただけのpending状態はノルマへ数えない。5件は停止上限ではない。最低5件を達成した後も、継続可能なResearch / Auditがある限り機械案内は `CLAIM_NEXT_RESEARCH_AUDIT` を返し、既確保standbyの昇格またはclaim windowの補充を行って同じ読解モードを継続する。**時刻・次回予定枠・run経過時間だけを理由に新規Research/Auditを止めない。** 曖昧な `CONTINUE_WORK` を最低件数達成後の停止・待機理由として扱わない。
- **探索モード**: 今回のrunで最低8つの**成功した正規schema v3 precheck**を完了させ、そのprecheckに対応するDiscovery submission/resultまで耐久反映する。**1つのprecheck `request_id` = 1ラウンド**と数える。同じprecheckから候補を複数submissionへ分割しても1ラウンドのままであり、逆に別の成功precheckなら同じprovider・同じ探索元でも別ラウンドとして数える。候補0件の成功precheckも、0件submission/resultまで正規経路を完了すれば1ラウンドに数える。8ラウンドは停止上限ではない。

handoff guard、platform/context limit、GitHub正本の読取不能などのhard stopはノルマより優先する。ただし、**Research / Auditの内容書込みだけがplatform safetyで拒否され、claim/direct-take等の制御系GitHub writeとGitHub readが生きている場合はrun-wide hard stopへ昇格しない。** 第2.1節の `volatile pending durability` 規則で内容完成とGitHub耐久反映を分離し、既確保standbyの読解を継続する。件数を満たすために弱い候補を採用したり、読解品質を下げたりしない。
### 2.0 Library-first専用ワークリスト

**固定Scheduled Chat (`scheduled-chat-00` / `scheduled-chat-30`) がタスク本文で `Library-first（GitHub read-only）` を指定されている通常runでは、この節のタスクローカル方針を第2節のGitHub書込み型worker向けroute/quotaより優先する。** 現行値は、開始時未処理候補在庫が **500件を超える場合は読解**、**500件以下なら探索**、読解の最低ノルマは **新規完成10件**である。探索の最低ノルマは、まず候補ごとに **GitHub と ChatGPT Library の両方を照合**し、既収録paper、既存Discovery成果、既存relevance ledger（unrelated / borderline）、active claim、Library保存済みの完成成果・探索判定、同run内重複のいずれにも該当しない **未処理の新規Discovery候補40件** を確定することから始める。その40件すべてについて一次資料本文を可能な範囲で確認し、`accept`（収録候補）、`unrelated`（無関係）、`borderline`（微妙・既定除外だが再検討可能）のいずれかへ最終判定して耐久保存する。40件の母数へ入れた後に既処理・重複だと判明した候補は母数から外して別候補を補充する。本文取得不能で判定未完了の候補も40件へ数えず補充する。acceptだけを40件集めるために基準を緩めず、本文を読んだ結果unrelated/borderlineなら正しくその分類へ保存する。run中に在庫数が境界を跨いでもモードは固定する。第2節の `288件 / Research-Audit 5件 / Discovery 8ラウンド` はGitHub書込み型の正規claim/submission経路用であり、Library-first read-only runのノルマ判定には使わない。

現在の `:00` / `:30` Scheduled Chatが**Library-first運用**を指示されている場合は、workerごとに分離した専用indexを対象選択の第一入口として使う。

- `scheduled-chat-00`: `.survey/work-queue/worker-worklist-00.json` / 人間向け `.survey/work-queue/WORKLIST-00.md`
- `scheduled-chat-30`: `.survey/work-queue/worker-worklist-30.json` / 人間向け `.survey/work-queue/WORKLIST-30.md`

各専用ページは、Research / Audit候補を最大200件、リスト入り判定待ちDiscovery候補を最大500件持つ。Research / Auditの提示数は現行200件を維持し、Discoveryだけを500件へ拡張する。生成時に同一の正規候補列を決定的なround-robinで二分し、十分な候補在庫がある限り`:00`と`:30`の割当は重複させない。**「共有ページの先頭／末尾」という概念は使わない。** 各workerは自分専用のResearch / Audit最大200件、Discovery最大500件だけを処理候補として扱う。

worklistはjob / claim / paper実体 / relevance ledgerから再構築されるindexであり、それらの正本を置き換えない。Library-first runでは処理直前に最新mainの正本状態を再確認し、すでに処理済み・active claim済み・対象外となった行をskipする。同じpaper identityまたは探索candidate identityの完成成果がChatGPT Libraryへすでに耐久保存され、GitHub反映待ちになっている場合もskipして同じ専用ページの次候補へ進む。

**Library-first Discoveryのaccept判定は、`:00` / `:30` の両workerで同じ厳格基準を使う。** worklist行、タイトル、要旨だけではacceptしてはならない。候補の一次資料本文を可能な範囲で読み、少なくとも次を確認してから収録候補とする。

- 現行サーベイの対象範囲へ直接入ること。LLM推論・配信・学習システム、メモリ階層、MoE、並列化、量子化、KV管理、投機、カーネル／ランタイム、評価基盤等への実質的な寄与が必要で、単なるモデル発表・一般応用・評価だけの論文は原則除外する。
- 既存収録論文と実質同一の寄与でないこと。新しい手法、システム設計、測定知見、理論、再現可能な比較軸のいずれかで、一覧へ独立して残す価値があること。
- 本文中の手法・実装・評価を読み、タイトルや要旨の強い表現だけでなく、実際に何を変更し、何を比較し、どの条件で有効かを確認できること。
- サーベイの主対象から外れる境界論文は、将来のResearch件数を埋める目的でacceptしない。関連性が間接的、既存研究の再説明に近い、またはシステム上の新規知見が乏しい場合はrejectする。
- accept時の一文要約は本文確認後に書き、本文から確認できた固有の寄与または代表的結果を含める。要旨の言い換えだけを収録理由にしない。

本文全文へアクセスできず、収録適否を十分に判断できない候補はacceptへ数えず、取得不能としてskipまたは保留し、次候補へ進む。Discoveryの最低ノルマを満たすために判定基準を緩めない。

**本文確認後の判定はGitHub正規relevance手順と同じ3分類で保存する。**
- `accept`: サーベイへ収録する価値があり、後続Research候補として残す。
- `unrelated`: 現行サーベイの対象外。GitHubの `mark_unrelated` と同じ意味で、原則として恒久除外する。
- `borderline`: 関連性または期待されるサーベイ価値が微妙。GitHubの `mark_borderline` と同じ意味で、既定では探索から除外するが明示的な再検討は可能とする。

Library-firstではGitHubのrelevance ledgerへwriteしない代わりに、各worker専用のLibrary relevance ledgerへ追記する。競合を避けるため `:00` と `:30` は別ファイルを使い、少なくとも次を正規化して保持する。
- `/LLM-paper-summary-library-first/discovery-relevance/scheduled-chat-00-unrelated-papers.json`
- `/LLM-paper-summary-library-first/discovery-relevance/scheduled-chat-00-borderline-papers.json`
- `/LLM-paper-summary-library-first/discovery-relevance/scheduled-chat-30-unrelated-papers.json`
- `/LLM-paper-summary-library-first/discovery-relevance/scheduled-chat-30-borderline-papers.json`

各recordはGitHubの `reference_relevance_ledger.py` に合わせ、`classification`, `canonical_id`, `identity_tokens`, `title`, `reason`, `first_checked_at`, `last_checked_at`, `linked_from` を保持し、取得できる場合は `source_url` も残す。同じcanonical identityは新規行を増やさず既存recordを更新する。unrelatedとborderlineの両方に同じidentityを残さず、最新判定側だけを有効とする。判定理由は「無関係」「微妙」だけで済ませず、本文を読んで確認した具体的な対象外理由、既存収録との差不足、システム寄与不足などを短く記録する。

accept候補は従来どおりDiscovery成果ファイルへ保存し、unrelated/borderlineは上記relevance ledgerへ保存する。探索runの最低40件は、GitHub＋Library照合で未処理と確認済みの新規Discovery候補だけを母集団にし、その各候補について3分類いずれかのLibrary耐久保存と保存後再取得確認が完了したidentityだけを数える。選定時、本文確認直前、保存直前の少なくとも3段階でidentityを再照合し、途中で既処理と判明したものはノルマから除外して補充する。relevance ledger更新に失敗した判定はノルマへ数えず、Library自体へ保存できない場合は今回runの判定記録JSON/MarkdownをScheduled Chatへ添付して成果を失わない。

専用worklistが欠損・古い・該当レーン空の場合だけ既存の正規job/reference poolから直接選ぶ。その場合も可能な限りもう一方の固定Scheduled workerが処理中・Library保存済みのidentityを避ける。claim、重複排除、relevance判定、submissionなどGitHub正規経路を使うrunでは、それぞれの正規安全規則を省略しない。Library-first runでは完成内容をGitHub本文へ直接反映せず、タスク本文で指定されたLibrary保存規則を優先する。

**Library-first の Research / Audit 完成成果でも、正規テンプレート `.survey/templates/paper.md` の要約契約を省略しない。** 1論文1ファイルの同一Markdown内に、少なくとも frontmatter の `summary`、`list_summary`、および本文の `## 概要` をすべて含める。別の要約専用ファイルへ分割しない。`summary` は手順書・テンプレートに従って論文全体を説明する単体ページ用の要約材料としてワーカー自身が一次資料から作成し、空欄のまま完成扱いにしない。`list_summary` は一覧専用の45〜180文字程度の独立した一文解説とし、`summary` や `## 概要` の機械的な切り出し・短縮で代用しない。`## 概要` は代表結果を含め、何が問題で、何を変え、どの条件で何が改善したかが単独で分かる内容にする。Library保存直前のセルフレビューでは、この3要素が同一ファイルに存在し内容が役割どおりであることを確認する。

### 2.0.1 ゼロ待ちhot dispatch（Research / Discovery共通）

通常runでは、`.survey/work-queue/hot-dispatch.json` が存在し、`direct_start_allowed=true` なら、**Actions resultを待ってから最初の内容作業を始めてはならない。** このindexは共有Research preload FIFOとDiscovery PRECHECKED preloadを1 readで公開する再構築可能な加速面である。`candidate_inventory` / `research_discovery_threshold` / `suggested_work_mode` を今回runの開始値として固定し、同時に通常のrun-state requestをmainへ保存するが、そのrequestには次の4項目も付けて**run-state Actionsは非同期の整合確認へ回す**。

- `candidate_inventory_at_start: <hot-dispatch candidate_inventory>`
- `work_mode_at_start: research | discovery`
- `research_discovery_threshold: <hot-dispatch research_discovery_threshold>`
- `hot_dispatch_generated_at: <hot-dispatch generated_at>`

run-state側はこの4項目の形式・policy整合性を検証し、最初の正規snapshotがまだ無いrunでは `route_source=hot_dispatch_direct_start` として同じrouteを固定する。`suggested_work_mode` は基本閾値と探索鮮度オーバーライドを同じ正規policyから適用した結果であり、`candidate_inventory` と閾値はdirect-takeの技術的可否判定には使わない。hot-dispatchはResearch / Discoveryの両レーンを同時に公開し、`direct_start_allowed` は**今回選択済みレーンに準備済みpacketが存在するか**だけで決める。閾値からの距離・ガード帯を理由にdirect startを禁止しない。選択済みレーンに準備済みpacketが無い場合だけ従来どおりrun-state resultを待って開始する。08:30 maintenanceは常にhot dispatch対象外である。

**Research / Audit:** まず `research_resume.<worker_id>[]` を確認する。同一workerのactive未提出claimが載っている場合は、**新しいtake/claim/resultを待たず最古のforegroundを即時再開する。** `work_start_allowed=true` なら一次資料取得・全文読解を直ちに継続してよい。`record_write_allowed=false` の場合でも読解開始は止めず、同時に通常のrun-state requestを耐久保存してclaim fast pathの正規canonicalization/record-bank回復を走らせる。run-state resultの `auto_resume_recovery.foreground` または更新後の同じ `research_resume.<worker_id>[]` で `record_write_allowed=true` と正規routeが確定してから5スロットへ書く。resume packetは既存claimの再開専用であり、create-only takeを発行せず、別workerのpacketを取得しない。

active resumeが無い場合は次に `research_recovery_resume.<worker_id>[]` を確認する。これは、同一job・同一旧attempt・同一旧claim reservationで5スロットが整合し、少なくとも1スロットに作業内容があり、immutable submissionがまだ無いまま旧claimだけが失効して共有poolへ戻ったケース専用である。該当packetがあれば、**worker自身は recovery packet の `take_path` へdirect takeを書かない。** 通常どおり今回runのrun-state requestを耐久保存（すでに同一identityで保存済みなら再利用）すると、同じrun-state workflow内の `auto_claim_from_run_state.py` が `research_recovery_resume.<worker_id>[0]` を検出し、対象 `job_id` に固定した一意な `auto-recovery-claim-*` requestを自動生成してclaim fast pathを実行する。これが同jobの `expired-same-job` recoveryを行い、保存済み5スロットを新claim/new attemptへretagする。run-state resultの `auto_recovery_claim.status=allocated` と、その後の `research_resume.<worker_id>[0]` / claim resultで正規record routeが確定し `record_write_allowed=true` になるまでは旧record bankを直接書き換えない。旧bank内容の読取と一次資料の再確認は自動canonicalizationと並行してよい。**このrecoveryでは worker-side direct-take write の失敗をhard stopにしない。direct-takeファイル作成自体が正規手順ではないためである。** 共有poolの通常claim refillも同じ未完了recordの元workerを優先するため、claim windowが埋まっている場合は既存foreground/standbyを壊して13件目を追加せず、次のrefill slotでこのrecovery jobを先に戻す。固定Scheduled Chat (`scheduled-chat-00` / `scheduled-chat-30`) の未完了recordは他workerの通常FIFO/direct takeから除外し、元workerへの再開アフィニティを保持する。

同一workerのactive resume/recovery resume packetが無い場合だけ、`research[]` の最古packetから、`take_path=.survey/work-queue/direct-takes/research/<claim_id>.json` を**存在しない場合だけcreate**する。payloadは最低限 `schema_version:1`, `operation:direct_take_research`, packetの `claim_id/job_id/attempt_id`, 一意な `request_id`, `worker_id`, `scheduled_slot`, `run_key`, `actual_invocation_start`, UTC `requested_at`, `claim_window`, 上記4つのdirect-route値を持つ。create成功が排他的な担当確保であり、**その瞬間からpacket内 `job` の一次資料取得・全文読解を開始してよい。** createが既存ファイル競合なら同じindexの次packetへ進み、Actionsを待たない。claim laneは後段でpool claimを正規worker claimへ変換し、同じworkerのwindowを既定12件まで補充し、hot record bankを確保する。**Survey claim fast laneとrun-state derivationは別々のActions concurrency groupを使い、run-state処理待ちをdirect take canonicalizationの待ち行列へ混ぜない。両laneが同時にmainへ書く場合はforce pushせず、push race時に最新mainから正規再計算して収束させる。** 5スロットへ書き始める前には `direct-take-results/research/<claim_id>.json` が `status=ready_for_submission` / `record_write_allowed=true` になったこと、または対応canonical claim resultで同一 `job_id/claim_id/attempt_id` とrecord routeが確定したことを確認する。**読解開始はこれを待たない。**

**pending claim rescue:** 誤って通常claim requestを先に発行した、またはfallback初回claimがまだresult待ちであっても、同一workerに本文foregroundが無く、hot-dispatchの未取得 `research[]` packetが残っているなら、そのpending requestを待機理由にしない。run-state / continuation gateは `CLAIM_NEXT_RESEARCH_AUDIT` と具体的な `next_work_packet.kind=research_direct_take` を返し、workerは**別の通常claim requestを追加せず**そのpacketをcreate-only direct takeして直ちに全文読解を始める。既存pending requestのidentityは保持して追跡する。claim fast laneはdirect takeを通常request allocationより先に正規化するため、後から処理される既存requestは同一workerの残りclaim windowをstandbyで埋める方向へ収束する。**時刻によるdirect take禁止は設けない。**

**Discovery:** 正規selector方向に対応する `discovery.<direction>[]` の最古packetについて、packetの `take_path=.survey/work-queue/discovery-preload/claims/<preload_id>.json` を**存在しない場合だけcreate**する。payloadは `schema_version:1`, packetの `preload_id/discovery_bank/discovery_slot_path/preload_result_path`, `worker_id`, `run_key`, 一意な `request_id`, `claimed_at`, 90分後の `lease_expires_at`, `direct_take:true`, `scheduled_slot`, `actual_invocation_start`, 上記direct-route値を持つ。create成功が排他的なpreload担当確保であり、**直ちにpacketの `preload_result_path` にある20件を軽量評価し始めてよい。** さらに供給側はこの最初のdirect takeを検出した時点で、同じ `worker_id / run_key` のDiscovery in-flightが正規上限3本へ届くまで、候補を実際に持つPRECHECKED packetを最大2本追加で**自動予約**し、それぞれのrun固有schema v3 precheck requestも同じforeground laneでmaterializeする。追加予約は `auto_frontier=true` と元packetの `frontier_parent_preload_id` を持ち、別workerへ再配布しない。したがってworkerが最初のprecheckの `queued` / `in_progress` を観測してから「次を始めるか」を判断する必要はなく、**待機状態へ到達する前に最大3ラウンド分の作業フロンティアが供給済みになる**。hot-dispatchの `discovery_start_frontier` は開始時点で即読める追加cached候補を最大2packet公開し、direct-take resultの `reserved_frontier` は実際に同runへ予約された後続packetを示す。既に正式precheck済みのcached候補は軽量評価を進めてよいが、各roundのsubmissionは必ずそのround固有の正式precheck result / receiptを待ち、preloadで先に評価した候補のうち正式 `allowed_records` から外れたものは捨てる。直接開始・frontier先行評価は品質ゲートを省略せず、**候補を読む時間と正式precheck待ちを重ねるだけ**である。create競合なら同方向の次packetへ進む。frontier上限3は供給在庫の上限であり、3ラウンドを同時submissionする許可ではない。

hot-dispatch packetに `direct_take_contract` がある場合は、worker自身がdirect-take schemaを文章から再構成してはならない。 `direct_take_contract.path` をcreate-only対象とし、`payload_base` をそのまま基礎payloadとして、`required_runtime_fields` に列挙された今回run固有値だけを補完する。時刻fieldはoffset-awareで生成し、Discoveryの `lease_expires_at` はcontractの `lease_seconds` から計算する。**`direct_take_contract` が有効なのに「現行schemaをまだ確認できていない」「payload形式に自信がない」を理由にrunを終了・handoffしてはならない。** contractと正規化実装が矛盾してcreateが実際に拒否された場合だけ、具体的なtransport/protocol failureとして正規回復へ進む。

hot-dispatchが欠落・破損、create競合を全packetで失敗、またはdirect-take正規化がrecovery_requiredになった場合は従来経路へfallbackする。ただし**Discoveryを選択済みで初回の後方引用PRECHECKED packetが0件でも、hot-dispatchの `discovery_fallback` / `fallback_start_allowed=true` があればrun-state resultを待ってはならない。** 同じ `run_key / worker_id / scheduled_slot / actual_invocation_start` を持つrun固有schema v3 precheck requestを、その固定 `provider / source_url / axis` から即時作成し、通常のrun-state requestは並行して耐久保存する。さらに `discovery_start_frontier` が非空なら、後方引用fallback requestを耐久保存した直後にそのPRECHECKED packet群から利用可能なものを順にcreate-only claimし、cached候補の軽量評価を開始する（旧互換の `discovery_start_lookahead` はfrontier先頭を示す補助面として残す）。これにより初回formal precheckがまだpendingでも実内容作業を持てる。`zero_wait_start_allowed` は非同期経路を即開始できること、`zero_wait_content_start_allowed` はcached候補を直ちに評価できることを区別する。lookahead自身もrun固有formal precheckが `ok=true / evaluation_allowed=true` になるまでsubmission禁止であり、in-flight上限3・古いresultのrecovery/evaluation優先規則を維持する。precheck laneはこのidentityからrun-stateを自動回復・更新するため、初回run-state resultは内容作業開始の同期障壁ではない。hot-dispatchは正本状態を置き換えず、submission可否は従来どおりcanonical claim / formal precheck / quality preflight / immutable resultが決める。

## 2.1 正規スクリプトを直接実行できない環境のfast-lane transport

Scheduled Chat等でリポジトリ内Pythonを直接起動できないこと自体は、Research / Audit / Discoveryを停止する理由ではない。GitHubへのread/writeが可能なら、**requestファイルをmainへ耐久保存し、対応するGitHub Actions fast laneに正規スクリプトを実行させ、resultファイルを読む経路**を現行の正規transportとして使う。この経路はmanual state編集ではない。

**GitHubのファイル作成・更新API/connectorを利用できる場合、それ自体をGitHub write可能と判定する。** ローカルshell、Python実行、`git push`、Actionsのmanual dispatch専用toolが無いことを、claim / run-state / preflight / submissionのwrite不能理由にしてはならない。新規request・direct-take・immutable descriptor等は、正規pathへGitHubのcreate-file相当操作でJSONを作成することで耐久化でき、そのcommitに反応するActions fast laneへ後段処理を委譲する。既存ファイルの更新が必要な段階では、直前に最新HEADと対象blob SHAを再取得してupdate-file相当操作を使う。

**このGitHub connector直結方式をScheduled Chatの既定・継続transportとする。** 今後の保守・リファクタリングでも、通常のGitHub file create/update → GitHub Actions fast lane → result読取、という責務分離を維持する。Scheduled Chat専用Issue relay、別inbox、独自bridge、低レベルGit object経路などの新しい搬送方式を、単発のplatform safety拒否や一時的なwrite失敗だけを理由に正規経路へ追加・置換してはならない。transport方式そのものを変更する必要がある場合は、まず過去に成功した同じGitHub connector経路の実績と現在の失敗条件を比較し、既存のLibrary fallback / status-only退避 / Actions側回復で処理できないことを確認する。**明示的なユーザー指示がない限り、正規transportの変更ではなく既存経路の修復を優先する。**

この規則は08:30専用runにも適用する。08:30のupdate / maintenanceで既存制御ファイルを更新する場合も、Scheduled Chatから通常のGitHub update-file相当操作を使い、直前に最新 `main` HEAD と対象blob SHAを再取得する。新規request等を作る場合は通常のcreate-file相当操作を使う。Scheduled Chat固有の別transportを設けない。

**Research / Auditの5スロット更新だけは、connector側で既存ファイルupdateがplatformから拒否された場合に低レベルGit ref更新へエスカレートしない。** 5スロット内容が完成しセルフレビュー済みなら、`.survey/work-queue/fallback-inbox/<unique-id>.json` へ **`record_bundle_mode: "quality_preflight_v1"`** のcreate-only record bundleを1個作る。bundleはrootに `origin: "claimed_worker"`, `kind`, `job_id`, `claim_id`, `worker_id`, `attempt_id`, `depends_on_job_ids`, `paper_path`, 完全なrun identity、`self_review`、必要なら `expected_blob_sha` を持ち、`writes` には同一bank由来の5スロットJSONをすべて含める。このpushでSurvey helperがbundleを安全なrecord bankへ展開し、同じcommitで通常の `research_quality_preflight` requestを生成する。以後は既存のpreflight PASS→自動descriptor→submission fast laneへ戻る。**create-only bundleが成功した時点で対象固有のupdate拒否は回復済みであり、`platform_context_limit` を申告してrunを終了してはならない。**

**内容を含むslot updateと `quality_preflight_v1` bundle createの両方がplatform安全検査で拒否された場合も、run-wide障害へ昇格する前にその1論文だけを退避する。** 最新mainでjobが同じ `job_id/kind` の非終端、claimが同じ `claim_id/attempt_id/worker_id` であることを再確認し、`.survey/work-queue/submissions/<kind>/<attempt_id>.json` に **内容を含まない最小status-only `blocked` descriptor** をcreate-onlyで保存する。descriptorは `schema_version:1`, `transport_version:10`, `kind`, `attempt_id`, `job_id`, `claim_id`, `worker_id`, `status:"blocked"`, `reason:"platform_content_write_rejected_after_bundle_fallback"` だけを基本とし、record slot本文・`paper_path`・`record_bank`・`record_slots`・`expected_blob_sha` を入れない。create成功をその論文の耐久退避完了とみなし、submission fast laneのresultを同期障壁にせず次のstandbyへ進む。Research/Auditともblocked retry対象とし、既存の7日cooldown後に再試行する。**このstatus-only descriptorが保存できた場合は `platform_context_limit` / run-wide write障害を申告してはならない。**

**最小status-only `blocked` descriptorのcreate自体もplatform safetyで拒否された場合は、その論文をrun-wide障害へ昇格させない。** ここでは通常経路を同じpayloadで再試行せず、`hot-dispatch.json` の `platform_content_write_recovery.on_status_only_write_rejected` が返す**第2経路**へ直ちに切り替える。第2経路は固定workerごとに事前作成済みの `.survey/work-queue/transport/worker-control/<worker_id>.json` を使い、**既存GitHub file updateだけ**で完結する。 shell、Python、manual Actions dispatch、低レベルGit ref操作、**新しいrun-state requestのcreateを要求しない**。対象ファイルの最新blob SHAと現在の `seq` を取り直し、`seq` を1増やしたうえで、契約の `worker_control_payload_base` にその `seq` だけを補って**既存ファイルを1回update**する。payloadには論文本文・title・`job_id`・`claim_id`・`attempt_id` を書かない。`foreground_guard` はhot-dispatchが対象foreground identityから生成済みのSHA-256であり、workerは再計算・改変しない。

このworker-control updateを受けたrun-state Actionsは、最新canonical claim stateからそのworkerのResearch/Audit foregroundを自分で解決し、`foreground_guard` が一致する場合だけ対象jobを `blocked` にしてclaimをreleaseし、7日cooldownを設定する。結果は `.survey/work-queue/transport/worker-control-results/<worker_id>-<seq>.json` に耐久保存される。`status=quarantined` / `next_action=CONTINUE_NEXT_RESEARCH_AUDIT` を確認したら、その論文を成功件数には数えず最古standbyへ直ちに進む。`foreground_guard_mismatch` の場合は古い命令を別論文へ適用せず、最新hot-dispatchを読み直す。**status-only createが1回拒否されたら、同じcreateを連打せずこのupdate-only第2経路を試す。**

**worker-control update自体もplatform safetyで拒否された場合だけ、第3経路として従来のhealth-probe update-only quarantineへ進む。** `on_worker_control_write_rejected` の契約を使い、`.survey/work-queue/transport/health-probe.json` の最新blob SHAを取り直して1回updateする。この第3経路では一意な `probe_id` と現在run identity、およびcanonical identityを明示した最小 `write_blocked_job` を使う。probe成功ならrun-wide障害ではない。worker-controlまたはhealth-probeのどちらかでquarantineが成功した場合、run-state requestのcreateは追加要求せず次のResearch/Auditへ進む。health-probe updateまで拒否された場合でも、**GitHub readとclaim/direct-take等の制御系writeがこのrunで成功しているなら、Research / Audit全体のtransport障害とは扱わない。** そのattemptだけを **`volatile pending durability`** として内容完成済み・GitHub耐久反映待ちに分離し、同じ内容writeやquarantine writeをこのrunで繰り返さない。

`volatile pending durability` に入れる条件は、(1) 一次資料全文の読解と5スロット相当の完成、(2) セルフレビュー完了、(3) 通常slot/bundle/status-only/worker-control/health-probeの正規回復を各1回まで実試行してplatform safety拒否を観測、(4) GitHub readまたは同runの制御系write成功実績があること、の全てである。これはResearch/Auditの**内容完成（content completion）**を表すだけで、成功件数・preflight PASS・immutable submission・耐久完了（durable completion）には数えない。

この状態ではcanonical foregroundを成功扱い・release済み扱いに捏造しない。**また、`volatile pending durability` を次回Scheduled Taskの再反映対象にしない。次回runは前runのcontent-write再試行に時間を使わず、新しいResearch / Audit作業を優先する。未反映の完成内容は最終報告のattempt別handoffとして残し、ユーザーが後から通常チャットでまとめてGitHub反映を指示する運用とする。通常チャットで反映済みになっていた場合はcanonical stateを確認してhandoffを解消し、再送しない。** 一方、**既に同一workerへ正規claim済みのstandbyがあるなら、最古standbyをread-ahead対象として一次資料取得・全文読解・5スロット相当の作成・セルフレビューまで進めてよい。** foreground昇格やrecord route確定を要するGitHub書込み、preflight、submissionは行わず、内容完成だけを先行する。これにより1本のcontent-write拒否でrunの残り時間を捨てない。既確保standbyが無い場合は、制御系writeが生きていることを実測できるときだけ通常のclaim/direct-take経路でstandbyを補充してよい。制御系writeまで拒否された場合は新規claimを増やさず、既確保分のread-aheadに限定する。

`volatile pending durability` の成果は、run終了時のScheduled Chat最終報告に機械可読なhandoffとして残す。各attemptについて最低限 `kind/job_id/claim_id/attempt_id/worker_id/run_key/source identity/5スロット完成内容/self_review/failed_operation/last_successful_operation/recovery_attempts/observed_error/next_action` を保持する。**次回同じScheduled Chatは、このhandoffの内容writeを自動再試行しない。** canonical identityとGitHub側の反映有無だけを確認し、通常チャット等ですでに反映済みならhandoffを解消する。未反映ならhandoffを維持したまま新しい作業へ進み、同じattemptの再読・slot/bundle再送にrun時間を使わない。ユーザーが通常チャットで一括反映を指示した場合にのみ、その時点の最新main・claim/attempt identity・record routeを確認して耐久反映する。canonical identityが変わっていれば古いhandoffを別attemptへ流用しない。

Libraryは一次PDFキャッシュや、Libraryへ直接保存できる正規経路が実際に利用可能な場合だけ補助耐久先として使う。**作業コンテナに生成したファイルをLibraryへmaterialize/uploadできない環境では、それ自体を追加fallbackとして要求しない。** Library境界の不一致だけを理由にrunを終了せず、上記volatile handoffとread-aheadへ進む。

この分離後、run-wide hard stopへ昇格できるのは、GitHub正本のread不能、claim/direct-takeを含む制御系transportも実際に拒否され既確保standbyも無い、または残り時間/取得上限/安全なidentity維持不能などにより内容作業そのものを継続できない場合である。

`transport_unrecoverable` / `durable_transports_unavailable` を申告してhandoffする前に、**今回必要な正規pathへの実writeを少なくとも1回は実際に試す。** write操作を一度も試していない、または「直接スクリプトを実行できない」ことしか確認していない状態はtransport障害ではない。create-only pathで既存ファイル競合が返った場合もwrite不能ではなく排他取得競合なので、routerが定める次packet/同一identity確認へ進む。

### 2.2 main writeのcommit集約

Scheduled ChatからGitHubへ直接耐久保存する場合、**同一論文・同一論理段階で、途中にActions起動や別workerからの可視化を必要としない複数ファイル更新は1回のcommitへ集約する。** 特にResearch / Auditの5スロットは、内容が完成してセルフレビュー可能になった時点でまとめて保存し、metadata / method / evaluation / results / positioningを1ファイルずつ別commitにしてmainを進めない。ローカルGit等で通常のatomic commitが利用できる場合は複数ファイルを1commitへまとめてよい。一方、connector環境で低レベルのtree/commit/ref操作が必要になる場合は、それを多重updateの回避策として使わず、前節の **`quality_preflight_v1` create-only record bundle** を優先する。特にplatformが通常updateを拒否した後に低レベルref更新を繰り返してはならない。

ただし、次の**耐久境界はまとめて潰さない**。claim request、Research quality preflight request、immutable submission、run-state requestなど、commit自体がActions起動・正規結果生成・handoff identity確定のトリガーになる境界は、それぞれ必要な順序を守って独立に耐久化する。`completed-submission request` は合格済みpreflight resultからGitHub側のpublication pipelineが自動生成する監査用の耐久記録であり、Scheduled Chatが追加writeする独立境界にはしない。preflight resultはdescriptor生成より前にmainへ耐久反映し、別attempt、別論文、別workerのpayloadを無関係に1commitへ束ねない。

GitHub transportが1ファイル単位のwriteしか提供しない場合は、存在しない原子更新を捏造せず、その環境で可能な最小commit数に留める。commit集約のために品質チェック・preflight・submission順序を変更してはならない。

### 2.3 一次資料取得回数の節約と再利用

Web/PDF取得のplatform上限はrunを途中終了させる実害があるため、Research / Auditでは**一次資料の全文読解要件を維持したまま、外部取得回数を可能な限り減らす。** 取得回数を節約するために抄録・検索断片・二次資料だけでResearchを完成させてはならない。

- claim後、同じ論文について既に利用可能な**一次PDF全文**がChatGPT Library等の耐久ファイル領域に存在するかをcanonical ID / arXiv ID / DOI / titleで確認できる場合は、Webへ再取得しに行く前にそれを再利用する。論文identityが一致し、欠落ページのない一次資料であることを確認する。
- 一次PDFをWebから取得する必要がある場合は、抄録ページ→HTML各節→PDF各ページのような細切れ取得を常用せず、まず**完全な一次PDFを1回でダウンロードする経路**を試す。完全な一次PDFのダウンロードに成功し、Libraryへの保存が利用可能なら、**そのPDFをLibrary側の一時キャッシュへ保存してから読解を継続することを原則必須とする。** Web上のPDFをページ単位で何度も取り直しながら読む経路を、Library保存可能なのに選んではならない。全文取得後の5スロット作成、preflight修復、submission failure修復、次runでのactive claim再開でも同じLibraryコピーを再利用し、同一版のPDFをWebから再取得しない。
- Libraryへ保存する一次PDFには、少なくともcanonical IDまたはarXiv ID/DOI、一次資料URL、取得時刻、判別可能なら版番号を対応付け、別論文・別版を誤再利用しない。二次資料や検索断片を一次PDFキャッシュとして保存しない。
- **完全な一次PDFそのものをダウンロードできない場合だけ、従来の取得方法へフォールバックする。** 具体的には、公式/著者公開HTML、arXiv HTML、PDFの必要ページ範囲取得など、利用可能な一次資料経路を少数回の範囲取得で最後まで読む。このフォールバックでも既に取得済みの節・ページを不必要に取り直さず、同一内容を複数providerから重複取得しない。PDFダウンロード不能を理由に抄録や二次資料だけでResearchを完成させてはならない。
- **Library上の一次PDFは恒久保存しない。** active claim、preflight修復、submission/repair待ち、handoff後の再開などで同一PDFを再利用する必要がある間だけ一時キャッシュとして保持する。その論文について成功result＋main反映が確定した、または `blocked` / `deferred` / `rejected` 等の終端状態が耐久反映され、未完了repair・再提出・handoff再開で当該PDFを使う必要がなくなった時点で、そのrun中に保存したLibrary PDFを削除する。削除前に別workerや未完了attemptが同じPDF identityを再利用中でないことを確認する。
- PDF/HTMLの同じ内容を複数providerから重複取得しない。現在の一次経路が実際に不完全・取得不能・破損・版不一致の場合だけ代替経路へ切り替える。
- 修復ループでは、品質検査が要求する箇所だけを既取得の全文から再確認し、論文全体をWebから取り直さない。
- Discovery中は候補identityと採否判断に全文PDFが不要なら取得しない。Research/Auditとしてclaimされた時点で初めて全文取得する。
- 取得節約によって出典確認、全文読解、一次資料優先、品質基準を弱めてはならない。必要な一次情報がキャッシュにもWebにも無い場合は推測せず、正規のblocked/deferred経路を使う。
- **単一論文の一次資料全文を取得できないことはrun-level hard stopではない。** foregroundで正規取得経路と利用可能な代替一次資料経路を試しても全文を確保できない場合、そのattemptを同じ `attempt_id` のstatus-only immutable descriptorとして `.survey/work-queue/submissions/<kind>/<attempt_id>.json` へ `blocked`（一時的・再試行価値がある場合は `deferred`）で耐久化する。理由と実際に試した一次資料経路を `reason` / `retrieval_evidence` に残し、推測で5スロットを作らない。descriptorがmainへ耐久保存された時点でそのclaimは次foreground選択から外れるので、**同じrunの最古standbyを直ちに開始する。submission result待ちを同期障壁にせず、成功数にも数えない。** `research_resume.<worker_id>[]` が `status_only_submission_path` / `status_only_descriptor_base` / `source_unavailable_next_action` を返している場合はそれを正本テンプレートとして使う。

**ノルマを達成したrunの最終報告には、取得上限を避けるために実際に使った工夫を短く記載する。** 例: 「Library上の既取得PDFを再利用」「PDFを1回だけ取得して修復でも再利用」「同一論文の再ダウンロードを回避」「Discoveryで不要な全文取得を省略」。取得回数や再利用回数を正確に数えられる場合は併記し、計測できない場合は推測値を作らず、実施した工夫だけを報告する。ノルマ未達時も取得上限が原因または近因なら、どの取得が上限に寄与したかを障害診断へ残す。

Research / Auditのclaimは次の順で行う。

### 2.4 Research / Auditの可変claim window（foreground 1 + standby N）

#### 二重用途バンク（dual-purpose bank）上の共有paper preload FIFO

A〜AFの32個のcanonical bankは、**Research preload / Discovery preload / Research-Audit hot stagingの3面を同時に持つ二重用途バンク**として扱う。各bankには従来の5つのResearch/Audit record slotに加えて、再構築可能な `research-preload.json` と独立した `discovery-preload.json` を置く。3面は互いに上書きせず、同じbankが読解用在庫と探索用在庫を同時に保持できる。**Research在庫とDiscovery在庫の維持はcandidate件数や今回runの選択モードから独立させ、片方の件数条件を理由にもう片方のpreloadを停止・空化しない。**

Research / Auditの事前装填はworkerごとの固定本数ではなく、全Scheduled Chat / worker-Nで共有するFIFO poolを使う。claim stateを正本とし、`research-preload.json` はその派生インデックスである。共有pool目標は `claim_window_policy.py` から導出し、現在は **12件/worker × 6 worker × 2セット = 144件**（workerへadopt済みを含む）。各Research claimは `pool_order` をcanonical bank順へround-robinして `stock_bank` / `stock_lane=research` を持ち、通常144件なら32bankすべてへ4〜5件ずつ読解用在庫を分散する。cold Research stockは5 record slotを予約しないため、全bankへ読解用在庫を置いてもhot staging容量は先食いしない。

- 共有poolのclaimは特定workerに固定しない。Scheduled Chat requestが来た時点で、そのrequestのjob type / 明示job_id条件を満たす最古のpool claimから不足window分をadoptする。
- 通常はhot-dispatchのcreate-only `direct-takes/research/<claim_id>.json` を先に置き、そのmarkerを**Actions前の排他的予約**として扱う。共有poolの通常allocatorはmarker済みclaimをadopt対象から除外するため、同時・不規則なworkerでも同一claim / jobを2 workerへ渡さない。claim fast laneはmarkerを後段で正規claimへ変換し、既存のsurvey-claim-main concurrencyとpush-race再計算でcanonical stateを確定する。adopt後も `stock_bank` は維持する。record slotを使うのはhot sliceだけで、hot化時はまず同じ `stock_bank` の5スロットを使い、そこが他Research stagingで使用中の場合だけ別のfree/reusable bankへ退避する。
- pool内の順番はpool_orderで固定する。一度装填済みの論文を後から到着した高priority論文で追い越させない。新しい補充論文は常にpool末尾へ追加する。
- workerへadoptした後は、そのworker内のpipeline_orderの末尾へ接続する。したがって既存standbyを飛び越さず、foreground終…15494 tokens truncated…帳へ反映し、`.survey/work-queue/reference-curation/results/<request_id>.json` を返す。push起動に加えて周期回収も行い、未result requestを再処理する。valid requestのresult未生成・Actions queued/in_progressは**待機理由でもrun終了理由でもない**。他候補評価、正式precheck回収、submission準備など今回runの実作業を継続し、作業の区切りでresultを回収する。resultが `ok=false` / `FIX_REFERENCE_RELEVANCE_REQUEST` の場合も、その失敗request/resultは不変証跡として残し、修正版を新しい `request_id` で作る一方、他候補の評価は止めない。processor内部の一時的I/O/競合失敗はresultを確定させず周期回収へ残し、1件のpoison requestで他の分類を停止させない。
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
7. **探索効率を記録する。** 前方引用roundでは `discovery_stats.seed_canonical_id` に実際に使った種論文のcanonical IDを必ず残し、`discovery_stats.search_windows` に種論文、引用方向 `forward`、取得件数、未収録件数、評価件数、採用件数を残す。後続runでは `select_discovery_direction.py` がこの耐久履歴を使って採用率の高かった種論文を優先し、0件が続く種論文を毎回先頭から調べ直さない。repository-wide後方引用のように単一seedを持たないroundでは `seed_canonical_id` を省略してよい。

この方法が特に有効なのは、既存系統が2024〜2025年の代表論文を含み、2026年の新手法がその代表論文を関連研究として引用し始めている場合である。単純なキーワード検索より、対象系統との接続根拠を保ったまま最新研究へ追従しやすい。

### 4.2 探索ノルマ

探索モードでは、正規hard stopがない限り、**今回のrunで成功した正規schema v3 precheckを合計8回**完了させ、それぞれをDiscovery submission/resultまで耐久反映する。ラウンドIDはprecheckの `request_id` とし、カウントはrun開始時に0から始める。1 precheckから強候補が6件以上出て `5 + 残り` の複数submissionに分割しても**1ラウンド**である。別precheckが成功すれば、同じprovider・同じ固定ソースでも別ラウンドとして数える。候補0件でも成功precheckと0件submission/resultまで完了すれば1ラウンドである。失敗・pendingのprecheckは数えない。8ラウンドは停止上限ではない。**時刻・次予定枠・run経過時間によるDiscovery開始禁止窓は設けず、selectorが返す次方向・次windowで探索を続ける。探索枯渇という通常終了条件も設けない。** 単一provider・単一seed・単一検索軸、あるいは前方/後方引用の一時的0件は終了理由にせず、selectorの次手へ進む。

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

1回のDiscovery submissionへ送るcandidateは0〜5件。**5件はrun上限でもround上限でもなく、1 submissionの上限**である。1回のprecheckで評価後に強候補が6件以上残った場合は、同じprecheck result / receiptを参照した複数submissionへ `5 + 残り` で分割し、強候補をすべてCandidate化する。複数submissionに分けても探索ラウンド数は1のままとする。**ただし分割した全submissionについて対応resultが `ok=true` で耐久反映されるまで、そのprecheck roundを成功ラウンドとして数えない。** 一部だけ成功・残りpending/失敗の状態はラウンド未完了である。分割時は全submissionの `discovery_stats` に同じ `run_key` / `round` / `axis` を持たせ、`round_submission_index` を1始まり、`round_submission_count` を総分割数として記録する。単一submissionなら両方1としてよい。

Discoveryのmulti-round submissionは、どちらのwork mixから探索を選んだ場合でも自己記述型（self-describing）を使い、存在しないDiscovery `job_id` を合成しない。candidate投入前に最新HEAD / identity / queueを再確認する。

### 4.3.1 新しい研究系統の昇格ルート

既存の正規系統へ無理に押し込むと研究上の差分が失われる**明確な近傍クラスタ**をDiscoveryで確認した場合、candidateに `lineage_proposal` を付けて正規の系統昇格ゲートへ送ってよい。未知のディレクトリをワーカーが直接作ってはならない。

新設は次をすべて満たす場合だけ提案する。

- `confidence: high`。
- `neighbor_lineages` に既存の正規系統を1〜3個指定し、`distinctness_reason` で近傍系統では表現できない理由を具体化する。
- `boundary_rule`、`scope_includes`、`scope_excludes` を明記し、別workerでも同じ境界で分類できるようにする。
- `supporting_papers` を4本以上指定し、正規IDで検証できること。そのうち少なくとも2本は既収録論文とする。
- 単一論文、1〜2本の派生研究、単なる実装差では新設しない。
- 1 Discovery roundで新設できる系統は最大1個とする。

提案は `slug_tail`、`title`、`description`、`distinctness_reason`、`boundary_rule`、`scope_includes`、`scope_excludes`、`neighbor_lineages`、`confidence`、`supporting_papers` を持つ。`queue_worker.py` は `.survey/scripts/lineage_proposal.py` で検査し、PASSなら空いている2桁番号を自動採番して `.survey/config/promoted-inference-lineages.json` へ正規登録し、`papers/inference/<new-lineage>/README.md` を作成してcandidateを新系統へ送る。

条件未達は探索失敗ではない。`.survey/work-queue/lineage-proposals/` に `deferred` と理由を保存し、candidate自体は既存系統または `99-other-inference-systems` へ通常どおり流す。**既存系統の説明を少し広げれば十分な場合は新設せず、複数論文が同じ主要機構を共有し、近傍系統との境界を再現可能に書ける場合は `99-other` に溜め続けず昇格ルートを使う。**

### 4.4 Discovery submissionからResearchへの一本道

Discovery後半は次の順序を正規経路とする。途中を手作業で代替してはならない。

1. `process_discovery_precheck.py` のschema v3 resultが `READY_FOR_EVALUATION` / `evaluation_allowed=true` になったことを確認する。
2. `allowed_records` だけを軽量評価し、候補0〜5件を `operation: submit_discovery_round` の不変submissionとして `.survey/work-queue/submissions/<unique>.json` に保存する。submissionは対応するprecheck result path / receiptを参照する。
3. `queue_worker.py` にsubmission処理を任せる。workerはResearch job IDを合成したり、`jobs/*.json` / `state.json` を直接書き換えたりしない。
4. 同名の `.survey/work-queue/results/<unique>.json` を確認し、`ok=true`、`research_jobs_added`、`final_duplicate_filtered_count`、`next_action` を読む。
5. `refresh_queue_snapshot.py` または `queue_worker.py` が更新した `.survey/work-queue/next-jobs.json` を確認する。
6. ready Research/Audit が現れても、**今回runがDiscoveryならclaimしない。** `next-jobs.json` への反映だけ確認し、run開始時に固定したDiscoveryを続ける。Research / Auditのclaimは、次回run開始時の `candidate_inventory >= RESEARCH_DISCOVERY_THRESHOLD` 判定で読解モードになった場合に `claim_worker_with_banks.py` から1件だけ取得する。
7. `research_jobs_added=0` でもrun終了理由にしない。最終重複排除や低優先度除外を確認し、必要なら別探索軸をschema v3 precheckから開始する。

失敗submissionの回収には `recover_discovery_submissions.py` を使う。回収後は `refresh_queue_snapshot.py` → `next-jobs.json` でcanonical stateを確認する。ただし**このrunが探索モードならResearchへ切り替えず、run開始時に固定した探索モードを維持する。** Research jobのclaimは次回以降、読解モードで行う。失敗済みsubmissionを上書きしたり、synthetic `job_id` を作って回避してはならない。

引用優先runでは、後方引用の候補山が残っていても前方引用へ進む。逆に前方引用が0件でも後方引用の山は継続する。**通常検索へ進めるのは、同じrun_keyで後方引用と前方引用の両方を試した後だけ**とし、通常検索は引用グラフで空く領域を埋める用途に限定する。単一provider障害は「0件」とみなさず、同じ引用方向の別providerまたは別種論文を試す。1 Discovery roundが耐久保存まで完了したら、**今回runの探索モードを維持したまま**次の探索軸を選ぶ。次方向の決定は原則 `.survey/scripts/select_discovery_direction.py` の出力を使い、ワーカーが「なんとなく次を選ぶ」ことは禁止する。selectorは同一runで未実施の後方引用→前方引用をまず埋め、その後は過去の `accepted_count`、`novel_candidate_count`、重複率、連続0件を使ってproductiveな引用方向を優先し、同点なら直前と反対方向を選ぶ。通常検索は同一runで後方・前方の両方が耐久記録済みの場合だけ候補になる。種論文についても過去search windowにseed identityがあれば同じyield規則を使い、履歴がないseed間ではcanonical ID昇順を決定的fallbackとする。候補在庫を再取得してもrun中のモード変更には使わず、次回runの開始判定用状態としてのみ扱う。

## 5. 重複排除

candidate提出前とResearch着手前に、正規識別子（canonical ID）、arXiv ID、DOI、OpenReview ID、正規化題名（normalized title）の順で照合する。

Discovery precheckではidentity snapshotとrejection ledgerを使う。GitHub code searchだけで「未収録」と判断しない。

## 6. 保存障害と退避

耐久経路は次の2つだけ。

1. GitHub direct write
2. ChatGPT Library `/LLM-survey-outbox/pending/`

Google Drive、Notion、旧 `/LLM-survey-fallback/` は使わない。

**record bankだけが枯渇し、GitHub read/write自体は利用可能な場合はrun-wide write障害ではない。** claim resultが `record_bank_fallback: library` を返したら、その論文の完全5-slot Research/Audit envelopeをLibrary `/LLM-survey-outbox/pending/` とcheckpoint markerへ保存する。GitHub writeが使えるなら同一run中にexact envelopeを `.survey/work-queue/fallback-inbox/` へimmutableに搬送し、`dispatch_fallback_inbox.py` / `drain_fallback_recovery.py` → immutable submission → result →最新main反映の正規publication経路へ流す。bank枯渇を理由に再精読やrun停止を行わない。成功件数へ数えるのはLibrary保存時点ではなく、canonical publication result `ok=true` と最新main反映を確認した時点だけである。

GitHub write失敗時:

1. 対象の最新blob SHA / repo状態を取り直し、その対象だけ1回再試行。
2. **Research / Auditの5スロット既存ファイルupdateが再び拒否された場合**は、低レベルtree/ref更新を試さず、完全5スロット＋セルフレビューを1つの `quality_preflight_v1` record bundleとして `.survey/work-queue/fallback-inbox/<unique-id>.json` へcreate-onlyで保存する。これが成功すれば対象固有障害は回復済みで、Actions側の展開→通常preflight→submissionを監視しつつrunを継続する。
3. **slot updateとrecord bundle createの両方がplatform安全検査で拒否された場合**は、上記の最小status-only `blocked` descriptorをcreate-onlyで1回保存する。保存成功ならその論文だけを7日cooldownへ退避し、submission resultを待たず最古standbyをforegroundへ昇格する。
4. **status-only descriptor createが拒否された場合は同じcreateを再試行しない。** hot-dispatchの `on_status_only_write_rejected` に従い、事前作成済み `worker-control/<worker_id>.json` の最新blob SHAと `seq` を取得し、`seq+1` と既定payloadだけで既存ファイルを1回updateする。job/claim/attempt identityは送らず、hot-dispatch提供の `foreground_guard` だけを使う。
5. worker-control resultが `quarantined` → run-wide障害ではない。claim releaseとblocked化はActions側で完了済みなので即座に次standbyへ進む。`foreground_guard_mismatch` → 最新hot-dispatchを読み直し、古い命令を別foregroundへ適用しない。
6. **worker-control update自体がplatform safetyで拒否された場合だけ** `on_worker_control_write_rejected` のhealth-probe update-only経路を1回使う。probe成功なら対象jobのblocked化・claim release結果を読み、次standbyへ進む。
7. health-probe updateまで失敗し、かつstatus-only/control write・Libraryを含む正規fallbackを尽くしても現在runの必須操作を耐久化できない → run-wide障害。そのrunではGitHub writeを繰り返さない。`transport_unrecoverable` / `durable_transports_unavailable` / `platform_context_limit` をrun-stateへ渡す場合は `transport_health_probe_attempted:true`、`transport_health_probe_succeeded:false` を必須とする。
8. GitHub direct writeとLibrary保存の両方が不能な場合だけ、未保存成果を増やす前に停止。

**`platform_context_limit` はrun-wideのplatform拒否に限定する。** 対象固有のslot updateやrecord bundleだけが拒否された一方で、status-only descriptor、worker-control update、GitHub read、Library保存、またはhealth probe updateが利用できる状態はrun-wide limitではない。run-stateへ `platform_context_limit` を申告する場合は、通常の証拠に加えて `runtime_condition_scope: "run_wide"`、**`runtime_condition_fallback_exhausted: true`**、`transport_health_probe_attempted:true`、`transport_health_probe_succeeded:false` を必須とする。このflagは、対象固有status-only退避とhealth probeを含む上記fallbackを実際に試しても現在runの必須tool callを耐久化できなかった場合だけtrueにする。health probeが成功したrunでは `platform_context_limit` を申告せず、対象論文のquarantineまたは次のstandbyへ進む。

**Scheduled Task自体を一時停止・無効化してはならない。** GitHub/API/Actions/Library障害、今回runのhard stop、ノルマ未達、その他の一時障害があっても、Scheduled Chat / automationのenabled状態は維持する。停止とは今回runの安全終了だけを意味し、将来runのスケジュール停止を意味しない。

Research/AuditのLibrary fallbackは1論文1envelopeで、root-level identityと完全5スロットを持たせる。復旧は `.survey/work-queue/fallback-inbox/<id>.json` から現行immutable submissionへ収束させる。

過去形式を読み込む互換コードが内部に存在しても、ワーカーが旧形式を新規生成してはならない。

## 7. 待機・継続・終了

### 7.0 非同期結果待ちの待機ミクロタスク

claim result、Research quality preflight、submission result、Discovery precheck/submission result、またはclaim可能jobの再出現待ちなど、**依存結果が未確定で本処理を直ちに進められない場合も、固定時間のsleepや定周期pollingだけを行ってはならない。** Scheduled Chatが「やることなし」と判断してrunを早期終了することを避けるため、依存結果がpendingの間は次の**待機ミクロタスクを1件だけ実行し、その完了直後に同じ耐久target/resultまたは最新queueを再確認する。** resultがまだpendingなら次のミクロタスクを1件実行して再確認する。このサイクル自体をrun終了理由にしない。

待機ミクロタスクは、現在のclaim/result identityを壊さず、途中で即座に本処理へ戻れる小さい作業に限定し、原則として次の優先順を使う。

1. **同一workerの非同期transport監査**: 未解決submission、retryable / repair待ち、active claim整合、対象Actions run/job/step、descriptor/result対応を確認する。
2. **直近完成論文の軽量生成物チェック**: Markdownの明白な自動置換破壊、source/code URL欠落、canonical ID/arXiv ID、必須見出し、正式英語名の破壊など、生成・変換バグだけをread中心に確認する。品質閾値・説明量・採否基準を変更してはならない。
3. **一時PDFキャッシュ掃除**: 成功result＋main反映済み、またはblocked/deferred/rejectedの終端が耐久反映済みで、別worker/未完了attemptが再利用していないLibrary一次PDFだけを削除する。
4. **キューの軽量健全性確認**: result済みclaim残留、descriptor済みactive表示、孤児request、同一canonical IDの明白な二重claim等をread-onlyで確認する。異常を見つけた場合だけ既存の正規repairへ渡し、待ち時間を理由に新しいrepair scriptやmanual state編集を作らない。
5. **現在論文の証拠整理**: すでに取得済み一次資料から代表結果、評価条件、限界、実装情報の根拠位置を整理する。依存preflight/resultが返る前に5スロットや公開paperを勝手に変更しない。

待機ミクロタスクの制約は次のとおり。

- **新しい論文claim、未claim論文の先読み、新しいDiscovery round、新規外部PDF取得、大規模refactorは行わない。**
- 新しい外部取得を増やさず、原則としてGitHub/Libraryの既取得状態だけで完結させる。
- 1件ごとに中断可能な粒度にする。長引く場合は途中状態を増やさず、そのタスクを打ち切って依存resultを再確認する。
- 待機ミクロタスクは時間残量で禁止しない。依存resultがpendingの間はread-only監査・安全なcache cleanup等の小作業を行い、各ミクロタスク直後に同じtargetを再確認する。時間を理由に内容作業・ミクロタスクを打ち切らない。
- 実行可能なミクロタスクを一通り確認済みでも、それ自体をrun終了理由にしない。同一targetの状態を再確認し、pendingなら安全なread-only確認を繰り返すか、既存の正規回復へ従う。
- resultが生成された時点でミクロタスクよりresult処理を優先し、`next_action` / `recovery_steps` にただちに戻る。

### 7.0.1 ゼロアイドル不変条件

通常の作業時間帯では、**非同期request/result待ちだけが残ってworkerに実行可能作業が0件になる状態を許容しない。** hot-dispatchのPRECHECKED packet、同一runの次Discovery固定ソースprecheck、Research/Audit standby、または第7.0節の有限ミクロタスクの少なくとも1つを常に次作業として持つ。特にDiscoveryは、PRECHECKED在庫が0でも固定ソースfallbackを即時開始し、前ラウンド成功時の自動advanceも同方向bankが無ければ同じrecovery transaction内で固定ソースprecheckまで実行する。

`idle_gap_forbidden=true` / hot-dispatchの `idle_gap_guard.passive_wait_forbidden=true` は、`Actionsが処理中なので何もせず終了`、`resultがまだ無いので最終応答`、`次の定期回収を待つ` を禁止する機械指示である。待ち対象が存在する場合も、そのtargetを保持したまま独立に進められる準備済み作業を先に実行する。**準備済み作業も固定ソースfallbackもミクロタスクも本当に生成できない状態は運用上の在庫欠損として最終報告へ記録するが、それ自体を通常終了許可にはしない。**

### 7.1 hard stopの機械判定

hard stopは曖昧な「安全そうでない」「難しい」「時間がかかる」では立てない。通常runでhard stopとして許可するのは次の機械的事実だけである。

- 通常runでは**予定時刻・次Scheduled Task・起動後経過時間をhard stopに含めない。** hard stopとして許可するのは、GitHub canonical stateをreadできず回復不能、GitHub/Library双方への耐久保存不能、実測したplatform/context取得上限、または正規transport/API/認証障害を規定回数回復しても継続不能な場合だけである。
- GitHubのcanonical stateをreadできず、同じrunで復旧確認もできない。
- 保存対象についてGitHub direct writeとLibrary耐久保存の両方が利用不能。
- platform/context上限が実際に発生し、継続するtool callまたは出力がプラットフォームから拒否された。
- 正規transportが要求するGitHub Actions/API/認証が利用不能で、Libraryを含む代替耐久経路でも現在成果を安全に引き継げない。

単一provider失敗、**単一論文の一次資料全文取得失敗**、validation failure、record bank枯渇、claim/submission result pending、候補0件、Library backlog、単に次手が分かりにくいことはhard stopではない。これらは正規回復・別provider・status-only・Library route・同一target待機・次の独立作業へ進む。特に一次資料取得失敗を `platform_context_limit` / `global_dependency` へ読み替えてrun全体を終了してはならない。

`continuation_gate.py` / `run_finalization_gate.py` へ停止系入力を渡す場合も、この列挙に対応する観測事実がある時だけtrueにする。ワーカー独自の解釈で `platform_limit` / `global_dependency` / `discovery_exhausted` を立てない。

### 7.2 run-state fast lane

run-stateは **request駆動snapshotとsubmission駆動の自動snapshotを同じ正規result schemaで扱う。** run開始時・runtime_condition申告時・自動導出不能時は従来どおりrequest fast laneを使う。一方、Research / Auditのsubmission処理で同一run identityと固定routeを安全に特定できる場合は、submission処理直後にGitHub側で正規snapshotを生成し、workerによる追加run-state request writeを省略してよい。自動snapshotもcontinuation gate / finalization gateを必ず通り、resultが存在すること自体でgateを迂回してはならない。

**run開始時の初回claim連結:** request駆動snapshotがResearch / Auditを選び、`CLAIM_NEXT_RESEARCH_AUDIT` かつ同一runにclaim transport・active assignment・submissionがまだ無い場合、run-state laneは同じserialized claim domain内で `auto_claim_from_run_state.py` → `claim_fast_path.py` を続けて実行し、初回claim request・bank予約・claim result・claim後の自動run-state snapshotを**同じmain commit**に耐久反映してよい。これによりworkerがrun-state resultを読んでから別のclaim Actionsを起動する往復を省く。run-state laneとstandalone claim laneはともに `concurrency: survey-claim-main` を使い、claim ownershipの競合回避を維持する。対象はrun開始時の**初回claim request自動生成だけ**であり、既存claim transportが1件でもあるrun、carry-over active claim、08:30 maintenance、Discoveryでは自動生成しない。**時間残量による除外はしない。** 以後のclaim window補充requestは通常のclaim経路を使う。

通常のScheduled Chatは、継続判断用の多数のbooleanを手作業で組み立てない。`.survey/work-queue/run-state/requests/<request-id>.json` に次の最小requestを耐久保存し、`.github/workflows/survey-run-state.yml` に `.survey/scripts/derive_worker_run_state.py` を実行させる。 **各再判定snapshotでは新しい一意な `request_id` を使う。** 同じrun内では `run_key` / `worker_id` / `scheduled_slot` / `actual_invocation_start` を維持するが、resultが既に存在するrequest IDを再利用して最新状態を得ようとしてはならない。既存resultは不変snapshotである。requestが存在してresultだけ未生成の場合は新requestを作らず、同じrequest IDのresultを待って定期回収に任せる。

```yaml
schema_version: 1
request_id: <filename stemと一致>
run_key: <今回runで固定した値>
worker_id: scheduled-chat-00 | scheduled-chat-30
scheduled_slot: "00" | "30" | "0830"
actual_invocation_start: <offset-aware timestamp>
runtime_condition: none
# hot-dispatch direct startを使った場合だけ追加:
# candidate_inventory_at_start: <hot-dispatch candidate_inventory>
# work_mode_at_start: research | discovery
# research_discovery_threshold: <hot-dispatch threshold>
# hot_dispatch_generated_at: <hot-dispatch generated_at>
# runtime障害を申告する場合だけ追加:
# runtime_condition_confirmed: true
# runtime_condition_attempts: 2
# runtime_condition_detail: <観測した障害と回復試行>
# platform_context_limit の場合だけ必須:
# runtime_condition_event: platform_tool_call_rejected
# runtime_condition_scope: run_wide
# runtime_condition_fallback_exhausted: true
# transport_health_probe_attempted: true
# transport_health_probe_succeeded: false
```

hot-dispatch direct startではrun-state requestを**内容作業開始前に耐久保存するがresultは待たない**。上記4項目がpolicyと整合する場合、run-stateはその開始時routeを正規snapshotへ固定する。従来経路ではresultを待ってから開始する。`runtime_condition` は通常 `none`。repoから導出できない実際のplatform/transport事象が起きた場合だけ、`github_read_unavailable` / `durable_transports_unavailable` / `platform_context_limit` / `transport_unrecoverable` のいずれかを使う。**単発のAPI/認証/ネットワーク失敗をruntime hard stopへ昇格させない。** retriableなread/transport事象は待機ミクロタスク等の別作業を1件以上挟んだ正規回復を最低2回試し、それでも同じ条件が継続した場合だけ `runtime_condition_confirmed=true`、`runtime_condition_attempts>=2`、短い `runtime_condition_detail` をrequestへ付ける。`platform_context_limit` は実際にplatformから**run-wideに必要なtool callまたはoutputを拒否された事実**がある場合に限り、`runtime_condition_confirmed=true`、`runtime_condition_attempts>=1`、非空の `runtime_condition_detail` に加えて **`runtime_condition_event=platform_tool_call_rejected`、`runtime_condition_scope=run_wide`、`runtime_condition_fallback_exhausted=true`、`transport_health_probe_attempted=true`、`transport_health_probe_succeeded=false`** を持つ場合だけ有効とする。対象固有のupdate拒否は前節のrecord bundle→status-only blocked退避→worker-control update-only隔離→health probeの順に正規fallbackを先に試す。probe成功時またはこの構造化証拠が無い `platform_context_limit` はrun-state側で `none` に降格する。単一論文のPDF/HTML/DOI/provider取得失敗はこのeventではなくstatus-only終端対象である。**`handoff_guard` は時間から導出しない。** 証拠不足のruntime_conditionはrun-state側で `none` に降格する。

同名の `.survey/work-queue/run-state/results/<request-id>.json` が返す `candidate_inventory`、run開始時に固定された `work_mode`、claim/submission pending、成功完了数、Discovery round数、**Discovery precheck pending / evaluation pending / submission pending / recovery required**、`gate.decision` / `gate.required_action` を継続判断の正本とする。 **ただしワーカーが次に実行する操作はトップレベルの `next_action` を正本とする。これは `run_finalization_gate.py` の `next_action` から導出し、前段の継続判定は `continuation_next_action` として診断用に残す。** `run_termination_allowed=false` の間はrunを終了・通常handoff扱いにせず、`next_work_packet` が非nullならそこに示された具体的なjob / claim / precheck result / preload / recovery targetを**次の操作として直ちに処理する**。進捗報告はしてよいが、それをrun終了の代替にしない。

**耐久stop permit:** 通常の論文workerは `finalization_permit_issued=true` だけでは終了してはならない。run-state snapshot内の `stop_permit.issued=true` かつ `run_termination_allowed=true` を終了の機械的証明とする。**`stop_permit.category=time_window` は廃止し、`next_scheduled_task_at` / `seconds_to_next_scheduled_task` / `seconds_to_run_deadline` は終了判断に使用しない。** stop permitは、(1) platform/toolの取得上限・出力上限を構造化証拠付きで実測した場合、(2) GitHub read / durable transport等が正規回復を所定回数試しても継続不能と確認された場合、に限って発行する。08:30 maintenanceはmaintenance完了を別カテゴリとして許可する。ノルマ達成、1件/1round完了、pending result、Actions実行中、候補0件、一区切り、次回再開可能、時刻接近という理由では `stop_permit` を発行しない。`continuation_contract.must_consume_next_work_packet=true` のsnapshotでは、現在の耐久境界の直後に `next_work_packet` を消費し、終了判断を挟まない。

**ゼロ空白継続契約:** 正常runで `run_termination_allowed=false` の場合、run-stateは可能な限り `next_work_packet` を具体化する。Research/Auditではforeground job/claim、次claim用hot-dispatch、Discoveryでは評価待ちprecheck result、lookahead preload、次direct take/fallback precheck、recovery targetのいずれかを返す。Discoveryではroundがsubmission resultまで耐久完了した時点で、そのprecheck identityをin-flight frontierから即時解放し、submission recovery transactionが空いた枠を再補充する。これにより上限3本の先行フロンティアを可能な限り維持し、完了後に次roundを探し始める空白を作らない。ワーカーは現在の耐久境界を完了した直後に再度「続けるか」を自由判断せず、このpacketへ連続して移る。packetを具体化できないactionだけは既存の待機ミクロタスク/正規回復へ進み、単に分かりにくいことを終了理由にしない。**時間残量はpacket生成・消費の条件に使わない。** foreground Discovery precheckに有効な `worker_id` / `run_key` / `scheduled_slot` / `actual_invocation_start` が存在するのに同runのrun-state requestが無い場合、Discovery precheck laneはそのidentityから決定的な回復requestを自動生成し、precheck resultと同じpublish transactionでrun-stateを導出する。この回復は既に開始済みのDiscovery modeを保持し、後から増減したcandidate inventoryでResearchへ再ルーティングしない。回復時の `candidate_inventory` は回復時観測値であり、`candidate_inventory_at_start_exact=false` として明示する。さらにDiscovery submission recovery側もlinked precheck identityから同じ回復を試してからauto-advanceするため、worker側のrun-state write漏れだけを理由に継続制御を失わない。`pipeline_ahead_count` が出力される場合は観測用テレメトリであり、Research / Auditの新規claim上限には使わない。run-state lane自体も**10分周期で未result requestを定期回収**し、push競合は最新mainから最大12回再導出し、各再試行は上限付きバックオフ＋ジッタで衝突位相をずらす。同一 `run_key` の最初の成功snapshotが `candidate_inventory` / `work_mode` を固定し、後続snapshotはそれを再利用する。ワーカーは結果と矛盾するbooleanを別途推測して `continuation_gate.py` を呼ばない。

**増分状態とsnapshot世代:** `.survey/work-queue/run-state/cache/<worker_id>.json` と `fact-clock.json` は高速化用の再構築可能index/cacheであり、immutable descriptor/result、claim state、queue state等のcanonical durable factsを置き換えない。cache欠落・破損・fact世代不一致ではcanonical factsから再構築し、maintenanceでも全履歴とのreconcileを行う。cache更新はmonotonic generationで管理し、古いgenerationを新しい状態として採用しない。`:00` と `:30` はworker_id別cacheで分離する。current invocation成功件数は従来どおり**resultの `processed_at >= actual_invocation_start`**だけを数え、claim時刻では数えない。carry-over unresolved attempt、前run由来pending result、retryable repairはcurrent run cacheにも残す。

**自動snapshotの鮮度:** 同一 `run_key` のsnapshotが複数ある場合、routeの固定値は最初の成功snapshotを維持し、現在状態の読取には同一run identityで最大の `snapshot_generation`、同世代なら新しい `processed_at` を優先する。`.survey/work-queue/run-state/latest/<worker_id>.json` はこの検索を短縮するpointerであり、それ自体を継続判断の正本にしない。pointerの `actual_invocation_start` / generationが対象runより古い場合は使わない。

**hot queue退避:** settled transportは `.survey/work-queue/archive/transport/**` へ段階的に退避する。対象はidentity確認済みcompleted-submission request、十分に古くdescriptor化済みのpassing preflight request/result、十分に古いsettled run-state request/result、全assignment終端確認済みの古いclaim request/resultに限定する。unresolved、pending、retryable、repair_required、active claim、handoff再開に必要なidentityは退避しない。immutable Research/Audit descriptor/resultはこのcompactorでは移動しない。archive失敗は論文処理を停止させずmaintenanceで再試行する。canonical再構築はarchive済み旧履歴もread compatibilityとして読める。

`gate.hard_stop` が返る場合はその値も正本とし、ワーカーが停止理由を再分類しない。主な `required_action` は次のように解釈する。

- `CLAIM_NEXT_RESEARCH_AUDIT`: Research / Auditの実行在庫を前へ進める。既確保standbyがあれば最古standbyをforegroundへ昇格し、windowが低水位なら正規claim requestでstandbyを補充する。1回のclaim requestが複数assignmentを返しても、本文処理するforegroundは1件だけである。
- `CONTINUE_ASSIGNED_WORK`: すでにactiveな同一workerの担当を継続し、新規claimを作らない。
- `WAIT_FOR_READY_RESEARCH_AUDIT`: claim可能jobが0件なので空claimを発行せず、第7.0節の待機ミクロタスクを1件処理してから最新queue/run-stateを再確認する。Discoveryへ切り替えない。
- `MONITOR_CLAIM_FAST_LANE`: claim requestから60秒未満で、かつ上記pending claim rescueに使える準備済みResearch/Audit packetが無い場合の監視フェーズ。同じrequestを起動したSurvey claim fast laneのActions run/job/step、同一workerの未解決submission・retryable repair・active claim整合を確認し、待機ミクロタスクを1件処理してから最新main/resultを再確認する。準備済みpacketが出現したら監視を前景にせず `CLAIM_NEXT_RESEARCH_AUDIT` のdirect takeへ移る。別の通常claim requestは発行しない。
- `WAIT_FOR_CLAIM_RESULT`: 60秒以上pendingのclaimを同一identityのまま追跡する。Actions失敗/cancelなら正規回復、処理中なら待機ミクロタスクを1件処理して再確認する。pendingだけを理由にrunを終了しない。
- `MONITOR_SUBMISSION_RESULTS`: claimableな独立Research/Auditが無くsubmission resultだけがpendingのときに、待機ミクロタスクを1件処理するたびに既存の未確定submission resultを回収し `next_action` / `recovery_steps` に従う。時間窓を理由にこのactionへ入らない。
- `WAIT_FOR_DISCOVERY_PRECHECK_RESULT` / `WAIT_FOR_DISCOVERY_SUBMISSION_RESULT`: 開始済みDiscovery roundとして、第7.0節の待機ミクロタスクを1件処理するたびに同一identityを再確認する。時間残量による打切りはしない。
- `CONTINUE_DISCOVERY_ROUND`: 成功済みprecheckの評価・submissionなど、すでに開始済みのroundを完了する。
- `RECOVER_DISCOVERY_SUBMISSION`: precheck/submissionの失敗を正規recovery_stepsで回収し、同じroundを終端まで進める。
- `DISCOVER_AGAIN`: 時間残量に関係なく新しいDiscovery roundへ進む。run-stateの `discovery_selector.next_direction` を正本とする。**今回runの初回roundでは、run-state fast laneが同方向PRECHECKED preloadを自動adoptしてrun固有precheckまで同一commitで完了していれば、返された `auto_initial_discovery` / 正式precheck resultを使って直ちに評価へ進み、同じprecheck requestを作り直さない。第2round以降も、直前roundのsubmission recovery fast laneが次のPRECHECKED preloadを確保した場合は、同じrecovery transaction内でrun固有schema v3 precheckまで完了させ、周期precheck回収を待たず正式resultから評価へ進む。** 自動高速化されていない場合だけ、同方向の `discovery_preload` が返っていれば従来どおりその事前装填窓をrun固有schema v3 requestとしてadoptする。利用可能preloadが無ければ固定ソースprecheckへ即時フォールバックし、preload待ちで停止しない。**通常検索（normal）のforeground schema-v3 precheckでSemantic Scholarのrate limit、provider fetch failure、または非対応search endpointにより `FIX_REQUEST` となった場合は、その失敗request/resultを不変証跡として残したまま、同じrun・同じ検索queryをOpenAlexの固定 `/works?search=...` result setへ写した新しいschema-v3 requestを正規provider failoverとして自動生成し、同じprecheck workflow内で処理する。citation request、preload seed、手選別recordsはこのfailover対象にしない。failover成功resultのみ評価へ進め、元のfailed precheckを成功roundとして数えない。**
- `RUN_0830_MAINTENANCE`: 08:30専用runの非論文更新→maintenanceを続行する。通常論文処理へ入らない。
- `FINALIZE`: `run_finalization_gate.py` で最終化許可を確認してから終了する。


継続判断の内部実装は `.survey/scripts/continuation_gate.py`、最終化判断は `.survey/scripts/run_finalization_gate.py` を使う。Scheduled Chatからは原則run-state fast laneの導出結果を経由する。run-state導出は同じcanonical factsを使って `run_finalization_gate.py` も評価し、`finalization_gate` と `finalization_permit_issued` をsnapshotへ耐久保存する。これらは**作業継続・停止の判断専用**であり、ユーザーへの報告可否を制御しない。run-stateは最終応答を禁止するfieldやdirectiveを持たない。Research / Auditでは**各提出直後と各claim前**にcontinuation gateを再実行し、新着submission resultも同時に回収する。提出直後はまず同一submission commitで生成された `.survey/work-queue/run-state/latest/<worker_id>.json` を確認し、`run_key` / `scheduled_slot` / `actual_invocation_start` が今回runと一致し、そのpointerが示す正規resultのidentityとgenerationも一致するなら、そのresultを使って追加run-state request writeを省略する。自動resultが無い、identity不一致、cache再構築要求、またはruntime_conditionを申告する必要がある場合だけ従来の一意なrun-state request fast laneへfallbackする。`submission_result_pending=true` でも、継続可能なResearch / Auditがあれば `required_action=CLAIM_NEXT_RESEARCH_AUDIT` を返し、standby昇格またはclaim window補充へ進む。`pipeline_ahead_count` は未確定submission後に積まれた提出数の観測値として保持してよいが、claim可否の閾値には使わない。claim可能jobが0件なら `WAIT_FOR_READY_RESEARCH_AUDIT` を使う。**時間fieldはcontinuation/finalization actionの選択に使わない。** 終端確認時はそのjobの終端statusを `--last-terminal-job-status`、今回runの成功完了数を `--research-audit-completed-this-invocation` として渡す。

`run_finalization_gate.py` にも今回runの `--work-mode` と最低条件カウンタを必ず渡す。run-state resultの `gate.hard_stop` をそのまま `--hard-stop` の正本とし、ワーカーが独自に再分類しない。Research / Auditで成功完了5件未達、またはDiscoveryで8 round未達の通常runは、仮に誤って `STOP_RUN` が渡されてもfinalization gateが拒否する。hard stop + safe handoffだけはこの最低条件より優先する。pending resultを含むsafe handoffでは、request/submission identity、期待result path、現在のpending状態、次の正規操作が耐久保存済みの場合だけ `handoff_safe=true` とする。

- claim/resultやsubmission/resultが次の安全な判断に必要なら、**最初にresult未生成を見ただけで終了・handoffしてはならない。** まず同一targetを保持したまま、正規workflow / fast lane / materializerがそのresultを即時生成・公開できる経路を1回だけ確認・実行し、第7.0節の待機ミクロタスクを1件処理して直後に再確認する。必要result以外に直ちに行える安全な内容作業が無い場合は、最大30秒の単発猶予待ちを1回だけ入れてから最新mainと同じresult pathをもう一度確認してよい。30秒後もpendingなら待機ミクロタスク・別の安全なforeground/standby作業・正規回復へ戻り、同じ短時間sleepを繰り返さない。claim result待ちではActions run/job/step確認と同一worker transport監査を優先する。Research / Auditモードで最新queue上のclaim可能jobが0件なら、空のclaim requestを連打せず待機ミクロタスクを1件処理して最新queueを再確認する。run中にDiscoveryへ切り替えない。**時刻接近を理由にpendingをhandoffして終了しない。**
- Research / Audit のsubmission result待ちは**foreground進行やclaim window補充の同期障壁にしない**。N提出後は既確保standbyのN+1、N+2、N+3…を順番にforegroundへ昇格し、各論文を1件ずつ直列に処理・耐久提出し続ける。standbyが低水位なら正規policyで非同期補充する。未確定resultは並行監視し、failureが見えた時点で `recovery_steps` に従って耐久回復へ流す。foreground処理中、claimable job 0件、または正規hard stop以外の理由でsubmission pendingを読解停止条件にしない。**時間窓も停止条件にしない。**
- candidate在庫、Library pending、fallback backlog、record bank枯渇、単一job失敗、status-only終端、1本完了、単一探索軸0件だけをrun終了理由にしない。
- **`run_termination_allowed=false` のsnapshotを観測した状態で通常handoff・run終了へ進んではならない。** `next_work_packet` が存在する場合、そのpacketを消費することが次の必須操作であり、「耐久保存できた」「一区切り」「次回再開可能」「次の予定時刻が近い」は終了理由にならない。
- **終了理由の整合性チェック:** 最終報告で通常run終了を宣言する場合、直前に確認した同一runの最新snapshotで `stop_permit.issued=true`、`run_termination_allowed=true`、かつcategoryが `observed_acquisition_limit` / transport・read系hard stop等の**非時間理由**であることを確認する。`time_window`、`seconds_to_next_scheduled_task`、`seconds_to_run_deadline`、`next_scheduled_task_at` は終了根拠として認めない。条件を満たさない場合は報告して終了せず、snapshotの `next_action` / `next_work_packet` へ戻る。
- **通常runは、次の2系統以外を理由に終了してはならない。** (1) 正規回復を試しても継続不能または安全に継続できない具体的な問題が発生した場合、(2) PDF・一次資料・Web/provider・Library等の**取得上限が実際に観測され**、必要な取得をそれ以上継続できない場合。**終了時刻・次回予定時刻・run経過時間は終了理由に含めない。** ノルマ達成、1本/1round完了、候補0件、submission/precheck/result pending、Actions進行中、単一provider失敗、単一論文の取得失敗、待機が発生したこと、次手が分かりにくいこと、通常処理が一区切り付いたことは、それ単独では終了理由にしない。取得上限は推測で立てず、実際の上限・拒否・quota/cap到達を観測した場合だけ使う。
- `finalization_gate` / `finalization_permit_issued` は停止判断には使用してよいが、**報告許可として扱わない。終了すると決めたrunは、終了理由が問題・取得上限のどちらであっても、Scheduled Chatへ必ず最終報告を残してから終了する。** hard stop、safe handoff、取得上限を含め、報告を省略して終了してはならない。**時間切れ接近は通常runの終了理由として報告しない。** 最終報告には少なくとも選択モード、今回の処理件数/round数、耐久反映、未完了事項、終了理由、確認できた最終main SHAを含める。`volatile pending durability` がある場合は、**成功件数とは別に `content_completed` と `durable_completed` を分けて報告し、次回再利用できるattempt別handoffを省略しない。** 最終mainを再取得できない問題で終了する場合は、最後に確認できたSHAと再取得不能であることを明記する。
- **通常runに時間ベースの開始禁止窓・最終handoff窓は設けない。** 新規独立作業、開始済みResearch/Audit、Discovery round、非同期result回収は、正規hard stopまたは実測取得上限が発生するまで継続する。

### 7.3 実行環境・transport障害の診断記録

Scheduled Chatで操作不能・platform limit・transport障害を理由に継続不能またはhandoffする場合、単に「操作できない」「GitHub操作を継続できない」と記録してはならない。**失敗した具体的な操作を、再現可能な粒度で必ず記録する。** 通常チャットとScheduled Chatでは利用可能なtool/transportが異なり得るため、リポジトリ回帰と実行環境差を切り分けられる情報を残す。

最低限、次をrun-stateの `runtime_condition_detail`、耐久handoff、最終報告のうち保存可能な箇所へ記録する。

- 失敗した段階（例: HEAD読取、worker-router読取、claim request write、Actions確認、result読取、record bank write、completed-submission request write、submission result確認）。
- **実際に試した操作/transport**（GitHub read、GitHub write、Actions read、Library write等）。利用可能なtool名を推測で列挙せず、実際に呼び出した操作だけを記録する。
- 対象repository/path/request_id/attempt_id等のidentity。秘密情報・認証情報は記録しない。
- 観測したエラー種別と、可能なら短いerror message / status。エラーが返る前にplatform側でtool call自体を拒否した場合はその事実を明記する。
- 正規回復として何を何回試したか、その結果。
- **直前まで成功していた操作**。たとえばHEADとworker-routerのreadは成功したがwriteだけ失敗した場合、それを明示する。
- 「未試行」「利用不能」「試行して失敗」を区別する。利用可能な正規transportを試していない状態で `transport_unrecoverable` と結論しない。
- **GitHub readが成功しており、ファイル作成・更新API/connectorが利用可能なら、GitHub writeは未試行扱いにしない。** 必要なrequest/direct-take等の正規pathへ実際のcreate/updateを試し、その具体的な失敗を観測して初めてwrite障害候補とする。shell/Python/CLIが無いことはwrite失敗の証拠ではない。

GitHub read/writeの一部だけが失敗した場合は、第6節のprobeと正規回復を行い、read成功をwrite成功と同一視しない。逆にwrite失敗をGitHub全体のread不能とも扱わない。Scheduled Chat固有の能力差が疑われる場合も、観測事実だけを記録し、リポジトリ変更が原因だと推測してhard stopにしない。

hard stop / safe handoffに入る場合の最終報告には、少なくとも **`failed_operation`、`last_successful_operation`、`recovery_attempts`、`observed_error`** に相当する4情報を人間が読める形で含める。これらを特定できない場合は「不明」と明記し、曖昧な一般文へ置き換えない。

## 8. 誤経路に入った場合

実行可能スクリプトが標準エラー出力（stderr）へ出す `[WORKER-GUIDE]` は、そのコマンド実行中の**必須行動指示**である。ワーカーは表示された順番に従い、ガイドが明示した完了条件を満たす前に次段へ進まない。

- `[待機]`: 完了またはエラー案内が出るまで、その処理に依存する次操作を開始しない。処理中に別の同目的スクリプトへ切り替えない。
- `[完了]` と `[次]`: 正常終了後の後続手順。記載されたスクリプト、結果ファイル、進行条件を順番どおり確認する。結果ファイルの `next_action` / `instructions` がある場合は併せて従う。
- `[手順エラー]` と `[正しい手順]`: その場で別経路へ迂回せず、示された復旧手順で同じ現行入口へ戻る。旧schema・manual手順・直接state編集で回避しない。
- JSON等の機械可読出力はstdout、ワーカー向け案内はstderrで分離される。案内をJSON本文として扱わない。

検証処理が `next_action` または `recovery_steps` を返した場合、それがその実行時点の復帰手順の最優先指示である。この文書と矛盾して見える場合も機械案内に従い、矛盾を隠さず最終報告の相談事項へ残す。**ただし保守・監査による実装変更は、稼働中のactive claim / immutable submission / result readerが使う現行schema・入口・読取契約を壊してはならない。破壊的変更が必要ならactive処理が収束するまで延期し、移行期間は後方互換読取を維持する。**

ワーカーは次を行う。

1. 最新HEADと対象stateを再取得する。
2. エラーが示した現行入口へ戻る。
3. 同一payloadの二重投入を避ける。
4. 旧schema、旧manual workflow、固定 `chat-inbox.json`、旧fallbackへ迂回しない。

「エラーになったので別の古い経路を試す」は禁止する。

## 9. 08:30更新とmaintenance

毎時 `:30` のScheduled Chatから起動したworkerのうち、**08:30 JSTのrunだけ**を日次更新・maintenance専用runとする。このrunではResearch / Audit / Discoveryを行わない。

実行順序は固定する。

1. 先に `framework-updates/**`、`llm-releases/**` の前回確認日時を読み、前回以降の一次資料（公式release / PR / documentation / model provider公式発表）を確認する。単なるmodel allowlist、軽微bugfix等は各READMEの掲載方針に従い除外する。
2. 更新があれば、最新blob SHAを基準に一意な `attempt_id` を持つ `.survey/update-worker/update-payload.json` と `update-inbox.json` を作る。`.github/workflows/update-helper.yml` / `.survey/scripts/update_worker.py` の正規入口で反映し、`.survey/update-worker/result.json` の同じ `attempt_id` で `ok=true` を確認する。更新が0件でも「確認済み」を最終報告へ残す。固定update inbox/payloadを過去attemptのまま再実行しない。
3. update result確認後に最新mainを再取得し、対象READMEの最終確認日と反映内容が一致することを確認する。ここまでを「非論文更新完了」とする。
4. 非論文更新の保存が完了した後、**runの最後の独立作業としてmaintenanceを実行する。**
5. maintenanceは `.survey/work-queue/maintenance-cycle.json` の `maintenance_pending=true` を耐久反映して `.github/workflows/maintenance.yml` を起動し、GC、index再構築、品質・メタデータ監査、整合性確認を直列実行させる。
6. maintenance workflowの結果を確認し、完了後の最新 `main` と `maintenance-cycle.json` を再取得して、`maintenance_pending=false`、かつ `last_maintenance_completed_at >= actual_invocation_start` が耐久反映されたことまでを今回08:30 runの完了条件とする。run-state fast laneはこの条件を満たす前は `RUN_0830_MAINTENANCE` を返し、完了後だけ最終化を許可する。workflowがhard stopで確認不能なら、その事実と未完了状態をhandoffしScheduled Task自体は止めない。未完了08:30 maintenanceの回収責任は次の`:45` STATUS異常修復に置き、通常の`:00`/`:30`論文runはmaintenanceを再発火しない。
7. 最終報告には非論文更新点（0件なら0件と明記）に加え、update result、maintenanceの起動・完了状態、GC/監査/整合性確認の結果、最終main SHAを含める。

maintenance実行の責任は08:30 JSTの `:30` workerに集約する。通常runでは定期maintenanceを発火させず、旧run-countカウンタも実行条件に使わない。
