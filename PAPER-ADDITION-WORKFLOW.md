# 論文探索・読解・GitHub登録

更新: 2026-10-10。正本はこのフォルダ、対象repoは `uni042/llm-paper-summary`。工程別の詳細は [PAPER-ADDITION-DETAILS.md](PAPER-ADDITION-DETAILS.md)、ローカル補助CLIは [AUTOMATION-TOOLS.md](AUTOMATION-TOOLS.md)。この手順は探索・読解・登録に必要な範囲に絞る。

## 探索モード

探索の最終成果は暫定screen archiveではなく、最新mainの .survey/import-inbox/pending/discovery/ へ渡す正規Discovery recordである。Discoveryでは一次資料のタイトル・要旨・書誌情報を確認して論文固有の根拠が得られれば最終分類でき、本文読解は必須ではない。本文確認・詳述はResearch段階で行う。provisional screen保存だけで完了・取り込み済みとはしない。

### 判定基準と証拠

- accept: LLM推論・実行基盤の高速化、レイテンシ/throughput、serving/scheduling、CPU-GPU offload/階層memory、KV cache、MoE推論、量子化/圧縮、speculative decoding/attention、GPU kernel/compiler/runtime、分散推論、edge inference、性能計測/benchmark/simulation、または直接関係する基盤技術へ具体的に寄与する候補。古典・汎用技術も対象技術への具体的な接続が確認できれば含める。
- borderline: 関連の糸口はあるが、システム効率への貢献・適用先・既存系統との接続が限定的または不明瞭なもの。単なる情報不足の代用分類にはしない。
- unrelated: LLMを使うだけの異分野応用、能力/生成品質評価、安全性・社会的影響、画像/音声等の独立応用、学習単独の高速化など、対象システム効率との具体的な接続が一次資料から確認できないもの。
- 新しさ、被引用数、venueは優先度には使えるが、関連性の証拠にしない。テンプレート理由は禁止し、各論文の提案機構・改善対象・適用先に結び付けて理由を書く。
- 安定ID（arXiv/DOI等）、一次資料の題名・要旨・書誌、研究対象、提案技術、改善対象を確認する。一次要旨を取得できない候補は、確認済みID・題名・一次URLと取得失敗理由を残してborderlineへ記録する。ID・題名自体が不確かなidentity_unresolvedは未解決として別管理し、正式分類件数へ含めない。
- 本文未読で一次要旨を読めたrecordでは body_check: "abstract_screen_only; body_not_read" を記録する。一次要旨を取得できず本文も読めなかったborderlineでは body_check: "source_unavailable; abstract_not_read; body_not_read" とし、確認済み書誌・一次URL・具体的取得失敗をreasonに残す。明白な対象外だけをタイトル段階で除外する場合は body_check: "title_screen_only; abstract_not_read; body_not_read" とし、理由も題名に示された明白な対象外に限定する。本文で見たような評価・機構を記述しない。
- linked_from / identity_tokens は確認済みの情報だけを記録する。未確認関連付け、安定ID、日時、実験結果を捏造しない。

### 候補選択と既存成果の再評価

- 作業前に最新main SHAを固定し、同一SHAのSTATUS.md、processor/precheck scripts、関連Actionsの実行設定、対象成果を確認する。GitHub側の古い手順書（worker-router、import-inbox README等）は参照しない。実行規約はこのローカル契約とユーザーの最新指示を使う。古いcloneやmain取得失敗から候補・重複・空queueを推定しない。
- 既存batchではR312〜R336の暫定screenを再評価する。items[] / results[] の両形式を読む。accept_for_readingは暫定推奨、identity_unresolvedは再照合、clear_out_of_scopeは根拠を確認して原則unrelatedとする。要旨証拠・原本・出典・履歴を保持し、汎用理由は一次要旨に戻って論文固有の根拠へ直す。
- 同一論文の統合ではcanonical ID、別名ID、identity tokens、題名を使い、衝突を未解決として明示する。既存paper、Research job、relevance台帳との重複は最新main側の正式precheckに委ねる。ローカル重複helperは同じ論文を二重にbatch投入しないために使い、正式採否の代用にしない。
- 新規探索は50候補を1担当者が1batchで扱う。rootは割当前に題名・要旨をざっと見て、明白な無関係だけ根拠付きunrelated_listに記録して担当から外す。系統との接点や対象技術への可能性が残る候補は広く残す。agentの結果とroot除外を同一batchへ統合し、rootが全件検証する。

### 正規Discovery JSONと段階投入

- 1ファイルは20 record以下。各ファイルは schema_version: 2, artifact_type: "discovery_run", worker_id, 一意な run_key, reference_main_sha, record_count, records[] を持ち、record_count == records.length を検証する。分類済みaccept/unrelated/borderlineを同じrunへ入れられる。未解決は正式分類recordへ混ぜない。
- recordには classification、確認済みcanonical_idとidentity_tokens、title、論文固有のreason、source_url、正しいbody_check、実際の確認時刻 first_checked_at / last_checked_at、確認済み関係だけのlinked_fromを含める。未解決候補は別管理し、分類件数へ含めない。
- 最新mainでdestination pathが存在しないことを確認し、一意な新規名で .survey/import-inbox/pending/discovery/ にcreate-only投入する。Contents APIまたは承認済みuploaderを使い、送信後に完全readbackし原本bytes/hash一致を確認する。不一致・曖昧な結果を成功扱いせず、同じ内容を再送しない。
- GitHub connectorのUTF-8 text入力には、`stage_upload.py emit` が出すbase64を厳密に復号し、UTF-8 decode/encodeの往復でbytes一致を確認した文字列を渡す。Contents API create後は固定commitを指定してbase64 readbackし、connectorが付ける行折返し（ASCII空白・TAB・CR/LF）だけを除いてstage emitのbase64と比較する。文字列差だけで成功扱いせず、base64のbytes一致を確認する。JSONの再serializationやpayload内容の正規化はしない。PowerShellの`Get-Content -Raw`出力を直接connectorへ渡す経路では末尾改行が追加された実例があるため避ける。
- まず20件以下の1ファイルだけ投入し、pendingからwaiting/処理済みへの移動、receipt、blocked、precheck結果と除外理由、新規Research job、STATUS候補数を追跡する。正常なreceiptと昇格経路を確認した後、残りを段階投入する。重複・既収録・既候補は失敗にせず、precheck内訳で報告する。
- 先行ファイルの公式受け入れ（receipt、submission、期待するResearch job、STATUS反映）の完了を待つ間も、待機が続く限り次の50候補batchをローカルで連続探索する。各batchの一次資料根拠・最終分類・取得不能borderline・identity_unresolvedを保存し、root検証後に分類済み成果をまとめる。先行batchの公式gateが完了するまでは後続artifactをGitHubへ送らず、waiting queueを膨らませない。gate完了後は蓄積分を正式手順で段階投入し、次の待機中も探索を再開する。探索は使用枠のcheckpoint境界とprojectのbatch契約を守る。
- survey-orchestrator.yml と library-import.yml の正規Actionsへ任せる。precheck result/request、Discovery submission、Research job、relevance台帳、STATUSを手作業で生成せず、正式routeを迂回しない。受付済みはResearch job化や最終paper収録と区別する。
- 実行時は、最初のlibrary-import runがpending→waitingとprecheck requestを作成して正常終了し、公式precheck gate後の継続runがsubmission・receipt・Research jobを完了する場合がある。最初のrun終了だけで停滞と判断せず、Actionsの自動継続を追跡する。receipt名は`<run_key>--<payload_sha256>--<run_key>.json`のようにhash付きになることがあるため、`<run_key>.json`だけを問い合わせず、pending時の正確なhash付きbasenameをresults/discoveryで照合する。手動でprecheck・submission・job・receiptを作らない。
- 受け入れ経路が明らかに停止した場合は、Actionsのrun/job状態・最終更新時刻・直近commitを確認して根拠をcheckpointし、6.1 Sol（reasoning low）へ最小限の再現情報と関連実装を渡して原因切り分けと範囲を絞った修繕を依頼する。修繕後はrootが差分と作用範囲を確認し、関連するfocused checkを実行してから正規経路を再開する。単に長時間実行中という表示だけでは停止と判定せず、既存の実行上限・過去の通常所要時間と比較する。
- 各batchでDiscovery schema検査/root検査、exact readback後にmain SHA、件数、receipt結果をcheckpointする。screen結果・一次要旨証拠・判定履歴は保持する。削除できるのは完全readback済みのupload artifact copyだけで、唯一の証跡を削除しない。
- **成功確認済みの実行例（2026-10-10）**: `codex-backfill-r492-b35-p05` は `stage_upload.py stage/emit` のUTF-8 bytesをContents APIでcreate-only登録し、作成commit固定のbase64 readbackをstage emitと照合した。通常のimporterが生成したreceiptは `imported`、source SHA-256 `ff8cd26f0c554a60f30272659ffa2479b6b76f3f7b8e0c710f5dabfb1b0acb2b`、19 records、18 accept/submit、provider gap 0。4件の正規submissionでResearch job 18件を確認し、STATUS候補数は親mainの1,034から1,052へ増加した。この実績は送信成功だけでなく、下流receipt・job・STATUSまで追跡できた例である。原稿・stage manifestは `reports/20261010-main-0a9fb-worklist-5000/codex-backfill-r492-b35-p05.json` と `reports/20261010-staged-codex-backfill-r492-b35-p05-d240/`、receiptは `repository/.survey/import-inbox/results/discovery/codex-backfill-r492-b35-p05--ff8cd26f0c554a60f30272659ffa2479b6b76f3f7b8e0c710f5dabfb1b0acb2b--codex-backfill-r492-b35-p05.json` を参照する。これは同じ正規routeの実証記録であり、後続batchのreadback・precheck・Research job・receipt確認を省略する根拠にはしない。
- `tools/validate_abstract_screen.py` は旧provisional-screen形式専用であり、正規 `discovery_run` を検証しない。旧screen enumや本文確認前提がabstract-only Discovery契約と衝突した場合、そのvalidatorのFAILをDiscovery JSONへ無理に適合させず、根拠を偽らずにcanonical schema・全件identity/disposition・本文未読表記・取得不能borderline・未解決分離をroot検査し、診断をscreen証跡へ残す。validatorの移行・統合は別の明示タスクで扱う。

### 進捗・使用枠

毎batchと定期報告で、対象report数、候補総数、一意数、accept/borderline/unrelated/未解決、Discovery JSON化数、GitHub投入数、receipt/imported/waiting/blocked、precheck除外内訳、新規Research job数、STATUS候補数（前後）、未処理数を分けて報告する。探索accept率は accept / 正式分類済み件数を分子・分母付きで示し、最終採用・Research job昇格率と混同しない。HTTP 404の空一覧と接続障害を区別し、未確認の取り込み・採用を主張しない。

作業開始時、約5分ごと、主要工程の区切りで使用枠を確認する。reset creditは明示的に許可された閾値以下でのみ使う。5時間枠20%以下では新しい工程を始めず、安全にcheckpointして最新reset後への再開を調整する。週次境界は最新のユーザー指示を適用する。

## 作業順

候補選定・補充は [PAPER-SELECTION-FLOW.md](PAPER-SELECTION-FLOW.md) に従う。探索候補は50件を1 batchとして扱い、rootがローカルpaper/draft/report/batchとの重複を除き、題名・要旨のquick skimで明白な対象外だけを根拠付き`unrelated_list`に先行記録する。残りを1人の担当へ順番に渡し、事前除外分も同じbatch resultへ統合してGitHubへ登録する。GitHubのpending/waiting/blocked件数とmain SHAは各batch後に記録し、累計処理数と一緒にユーザーへ報告するが、待機列の増減を次batch開始条件にしない。作業者は常に1人とし、screening時にGitHub側状態を候補ごとに照合せず、最終precheck/importへ任せる。

探索の採用閾値は広く取る。既存の論文系統（既存paperからのlinked/related paper family）に加わる可能性がそこそこある候補は、本文評価の完成度や効果の強さが未確定でもscreeningで落とさずDiscoveryの`accept`として読解ゲートへ送る。特にLLM推論の計算量・メモリ・レイテンシ・スループット・KV cache・quantization・offload・servingを直接改善する具体的手法、または既存論文系統との妥当なつながりが要旨上うかがえるものを広く残す。これは探索候補として読解へ通す判定であり、最終収録や有効性の承認ではない。読解担当は一次本文の手法・実験・限界と系統とのつながりを確認し、明確に対象外なら`unrelated`、関係が弱い/本文取得不能/解決困難なら理由付き`borderline`へ最終分類する。要旨だけで技術的成功を断定しない。保留だけの最終状態を残さない。

候補の`linked_from_lineages`は関連性を検討する材料であり、Discoveryで本文読解を必須にしない。一次要旨の技術内容と適用先から最終分類し、接点が残るものを広くaccept側へ残す。一次要旨を取得できない場合は、確認済みID・題名・一次URLと取得失敗理由を保持してborderlineにする。identity自体が不確かな場合は未解決として別管理する。本文での最終収録判断はResearch段階で行う。

50件batchを担当へ渡す前に、rootが候補一覧の題名・要旨をざっと確認する。対象との接点が明らかにない候補だけを事前に`unrelated_list`へ記録し、一次要旨など判定根拠を短く残して、担当への一次資料確認依頼から外す。既存論文系統との接点、推論効率への具体的な寄与、または少しでも関連可能性が残る候補は外さず担当へ渡す。事前除外した候補も元の50件batch結果へ統合し、root validatorを通したうえで、他の分類済み結果とともにGitHubのDiscovery artifactへ登録する。候補を未記録のまま捨てない。

決定的で反復可能な機械作業（ローカル重複照合、候補選別、schema/件数確認、集計、file/hash確認、定型packet生成）は、手作業の繰り返しより再利用可能なread-onlyまたは安全な補助scriptを優先する。論文のscope適合性、証拠の十分さ、曖昧さの dispositionなど意味判断が必要な工程はLLMが担当する。scriptの出力は該当する受け入れ条件に沿って確認し、GitHub/API・削除・外部状態変更を含む作用は既存の明示的な承認境界を維持する。新規scriptは [AUTOMATION-TOOLS.md](AUTOMATION-TOOLS.md) に用途と制約を記録する。

直接依頼のCodexは [CODEX-PAPER-ROUTE.md](CODEX-PAPER-ROUTE.md) とローカル詳細契約を使う。GitHub側のrouter、README、workflow手順書を実行時にfetch/readしない。必要な実行条件はCodex専用execution_contract、品質項目はローカル詳細契約と論文templateに揃える。GitHubは最新状態・原稿・監査code/config等の入力データ取得と許可された保存のために使い、手順書読取へのfallbackはしない。

2026-10-05に専用generatorの19件focused test、identity3件・claim2件の回帰、外側brief/identity補助6件、および取得時最新mainでのCLI生成/checkが成功。実データの手順文書read禁止検証と正式状態不変も確認した。[検証記録](reports/20261005-codex-route-final.md)を参照。GitHubへのコード公開・Actions実行は未実施で、現在はローカル隔離checkoutを使う。

ローカルResearchは [RESEARCH-BATCH-FLOW.md](RESEARCH-BATCH-FLOW.md) の小batchを通常経路とする。rootが候補と監査環境をまとめて確定し、1担当へ通常3本（少なくとも2本）を1回の契約で渡して既存agentを再利用する。人数を埋めるために1人1本へ分割しない。残り1本・長大論文・取得blocker・使用枠不足だけは理由付きで個別に切り分ける。完成分の随時返却と一括機械監査を組み合わせ、一次読解と意味reviewは論文別に維持する。Scheduled ChatのLibrary契約はこのCodex専用経路の対象外。

1. Git状態と5時間/週次使用枠を確認し、既存のdirty成果を保持する。最新main SHAを固定し、同じSHAのSTATUS・正規候補・identity・job/claim/inbox状態をCodex packetへまとめる。手順はこのローカル契約とexecution_contractを使い、GitHub手順書は読まない。未取得・404・古いcloneを「候補なし」と解釈しない。
2. 同じSHAのSTATUS「収録候補論文数」が600超ならResearch、600以下ならDiscovery。指標の欠落・取得不能は理由付きDiscoveryとし、別の実効値を推測しない。packetは完全な正規poolから候補windowを生成し、候補ID・一次資料URL・参照元と未解決点/final dispositionを保持する。手動で旧worklistを使うfallbackでは全ページを確認する。保存済み候補はID/hashで照合し、既処理分の再取得を避ける。
3. Discoveryは一次資料の題名・要旨・書誌と安定IDを確認し、論文固有の根拠でaccept/borderline/unrelatedへ最終分類する。本文読解は必須にしない。要旨上、LLM推論・実行基盤への具体的な寄与や既存系統との接点がある候補は広くaccept側へ残し、Researchの本文読解へ送る。本文未読は`abstract_screen_only; body_not_read`、明白な題名除外のみは`title_screen_only; abstract_not_read; body_not_read`と記録する。一次要旨取得不能は確認済みID・題名・一次URLと取得失敗理由付きborderlineへ記録する。identity自体が不確かな場合は未解決として別管理し、正式分類・候補数へ含めない。borderlineは境界的な関連性または取得不能の理由を明記する。Research担当は一次本文の該当節・評価・限界を確認して最終収録を判断する。未確認の機構・評価・書誌を補わない。
4. 成果を1回分のimmutable Research MarkdownまたはDiscovery JSONに完成させる。Discoveryはschema_version 2、artifact_type `discovery_run`、一意なrun_key、参照main SHA、全recordの最終分類と根拠を含める。手順は [詳細](PAPER-ADDITION-DETAILS.md) を参照。
   R312〜R336のbackfillでは`results[]`と`items[]`を再評価し、一次要旨とidentityを確認した正式分類だけを1 artifact最大20件で送る。旧`tools/watch_discovery_uploads.py prepare`は本文確認前提・取得不能のborderline変換を含むため、この新契約の変換には使用しない。暫定acceptを機械的に正式acceptへ変換せず、identity未解決を別台帳に残す。取得不能のborderlineは確認済みidentityと取得失敗理由を保持する。ready artifactは不変とし、source/result hashと判定証拠を保持する。
5. upload用artifactをUTF-8 BOMなし・LFへ正規化し、再監査後の原本SHAを確定する。PowerShellのテキスト出力末尾が本文へ混入しないよう原本bytesを保ってGitHub Contents APIで `.survey/import-inbox/pending/research/` または `pending/discovery/` に新規登録する。名前はrun_keyと原本SHAから一意にする。同じpathの異なる内容を上書きしない。既存ファイルの有無を先に確認する。
   backfillでは接続済みGitHub connectorのContents APIを使い、検査済み原本をcreate-onlyで送る。旧watcherの自動変換や監視を併用して同じ候補を二重投入しない。credentialをscript・引数・logへ保存しない。
6. 最新mainへ戻って同pathを読戻し、原本bytes/SHAと一致することを確認する。pendingが消えていれば同名waiting/blocked/retainedを確認し、最後に対応result receiptの `source_sha256` と比較する。一致するGitHub上の耐久コピーを確認した時点を `HANDOFF_VERIFIED` とする。内容不一致・不明writeは保持して読み直し、確認前に再送しない。
   `HANDOFF_VERIFIED`をstateへ永続記録した後、upload artifact本体のローカルcopyを削除し、manifestからpending項目を外してverified receipt metadataだけ残す。削除はworkspace内のready directoryにあるhash一致copyに限定する。state/hashが矛盾するcopy、未確認・失敗・曖昧な送信は削除しない。screen input/result、本文読解根拠、監査・進捗記録は成果証拠として保持し、upload staging folderを空に保つ。
7. Discovery/Researchの下流処理結果を別に確認する依頼では、main上のresult・論文実体・STATUSを照合する。handoff、processor取込、candidate/paperへの最終収録を同じ完了状態として扱わない。
8. 整理対象は今回の許可範囲に限る。原本とGitHub上の耐久コピーのhash一致を確認後、正確なupload artifact copyだけを削除する。verified metadataは送信履歴として残す。screen input/resultと読解根拠は再監査可能性のため残す。未完・保留・hash不一致は理由とともに保持する。

## 最終記録と使用枠あたりの処理効率

- 作業開始後は少なくとも5分ごと、およびbatch・探索windowなどの主要区切りで、開始からの累計進捗をユーザーへ報告する。要旨screen完了数、候補探索・identity照合数、分類読解完了数、一次本文まで確認した数を別々に数え、今回増えた件数と累計を示す。未確認と重複は完了数に混ぜず、一次資料取得不能は要旨確認完了数から分けて数えつつ理由付き`borderline`へ記録する。identity自体が不確かな未解決は別台帳で追跡し、機械的に正式分類へ変換しない。候補提示、読解、handoff、processor取込、最終収録も別状態で報告する。
- 作業開始時、約5分ごと、主要工程の区切りで取得した5時間枠・週次枠の`usedPercent`と`resetsAt`を、時刻・run_keyとともに作業記録へ残す。自然resetをまたいだ場合は別windowとして集計し、前後の差を混ぜない。
- 1 runごとに、探索した候補数、一次本文を実際に確認して分類した候補数、全文読解を終えた論文数、品質監査PASS数、送信済み数、`HANDOFF_VERIFIED`数、processorの`imported`数、最終paper実体確認数、および重複・対象外・保留・失敗数を分けて記録する。候補提出、全文読解、送信、最終取込は別の成果として数える。
- 各探索batchと定期進捗報告では、`accept_for_reading`（または同等の探索通過判定）件数 ÷ 判定済み候補件数の割合を、分子・分母・対象batchとともに示す。これは読解候補への通過率であり、最終収録率とは分ける。最終収録率を併記するときは、GitHub STATUSの耐久保存された収録件数を処理済み件数で割った値と明記する。
- 最終報告では、window別に枠使用率の増分（percentage points）を示し、探索済み候補数・一次本文確認数・全文読解完了数・`imported`数をそれぞれその増分で割った値を参考効率として併記する。複数windowをまとめる場合は各windowの分子と使用率増分を先に合算する。
- 5時間枠はアカウント共有であり、他taskの利用分を切り分けられない。したがってこの比率は観測されたアカウント枠の増分に対する参考値と明記し、task固有のtoken消費、節約率、因果的な生産性と断定しない。`resetsAt`から実経過時間を推測して使用量に換算しない。
- 詳細は `reports/` のrun別記録へ保存し、最終報告ではpaper / candidateの状態と集計式、対象window、測定不能な範囲を簡潔に説明する。

## 変えない品質・安全条件

- 対象範囲と除外条件は [詳細](PAPER-ADDITION-DETAILS.md) に従う。一次資料、paper固有の機構・評価・限界、identity alias確認を省略しない。
- GitHubの最新mainが正本。ローカルcloneや検索結果だけで重複や不存在を断定しない。
- create-only upload、固定SHAのreadback、hash一致を維持する。Contents API成功応答だけでは保存確認としない。
- 既存paperの修正は新規uploadと混ぜず、依頼された対象・目的・差分に限定する。
- quotaは開始、約5分ごと、agent起動前、主要境界で確認する。5時間枠の残量20%以下では安全にcheckpointし、同chat heartbeatで自然回復後に再開する。週次残量1%以下になったらcheckpointし、ユーザーが明示したreset credit使用指示に従って利用可能な既存creditを1回使用する。 reset toolがUsage設定の「Allow Codex to use resets」無効で拒否された場合はcreditを消費したと扱わず、ユーザーへ設定変更を依頼する。直後に使用枠と残creditを再確認し、週次残量40%以上になるまで不足時だけ繰り返す。40%以上で停止する。creditがなくなった、利用条件を確認できない、または使用が拒否された場合は停止して報告する。
- 5時間枠の回復待ちで未完了作業を継続する場合は、[使用枠回復待ちと同じtaskの再開](#使用枠回復待ちと同じtaskの再開)に従い、作業地点を保存して同じchatへ一度だけ再開予約する。
- 未実施のGitHub write、workflow起動、最終収録確認を完了済みと報告しない。

## 使用枠回復待ちと同じtaskの再開

5時間枠の残量が20%以下、または週次枠の残量が1%以下になったら、新しい工程へ進まず、実行中の原子的な作業を安全な区切りまで終えてから記録する。5時間枠回復待ちを挟んで同じ依頼を続ける場合、Codexの `automation_update` heartbeatを使って同じchatを一度だけ起こす。週次残量1%以下では、明示されたユーザー指示の範囲で既存reset creditを使い、週次残量40%以上になった時点で終了する。

1. 使用枠を再取得し、UTC時刻・5時間/週次の`usedPercent`と`resetsAt`、正本project・branch・dirty file、実施済み検証、未完了事項、正確な再開地点をcheckpointへ記録する。未完了agentを安全に区切り、同一fileの競合編集がないことを確認する。
2. 最新の5時間`resetsAt`より後の未来時刻を選ぶ。`automation_update`の`create`で `kind="heartbeat"`, `destination="thread"`, 現在のchatの`targetThreadId`, `status="ACTIVE"`を指定し、その時刻に一度だけ実行するRRULEを渡す。BackKeep Launcher taskで実際に再開まで確認できた形式は `RRULE:FREQ=DAILY;BYHOUR=3;BYMINUTE=0;BYSECOND=0;COUNT=1`（アプリのローカル時刻、例では3:00）だった。実作業では時刻を最新reset後へ合わせる。過去の`DTSTART`やすでに過ぎた時刻はfuture runを作らず失敗するため使わない。
3. promptには同じtask・同じcheckpointからの再開、起床直後の枠・規約・worktree・agent状態の再確認、5時間残量20%超の場合のみ通常作業を続行する条件を含める。週次残量1%以下では新規作業を始めずcheckpointし、ユーザーの明示済み指示に沿うreset creditの扱いを判断する。予約promptからcredit消費を自動化せず、使用直前に利用可能数・週次残量・ユーザー指示を確認する。作成応答後に同じautomationを`view`し、ACTIVEで未来の実行予定があることを確認する。view結果に予定日時が表示されない場合は確認済みと扱わず、制約を報告する。
4. 起床後に使用枠と保存地点を再確認する。5時間残量が20%を超えていれば、不要になった一回限りのheartbeatを削除して続行する。未回復なら新規予約を重複作成せず、同じautomationを最新の回復時刻より後へ更新する。週次残量1%以下では安全にcheckpointし、明示済み指示の範囲で利用可能なcreditを1回ずつ使用する。各使用後に枠と残creditを取り直し、週次残量40%以上で終了する。利用可能creditがない場合、使用が拒否された場合、または根拠が不明な場合は停止して報告する。
5. ローカルfileを使うdesktop taskは、予約時刻にPCとCodex desktop appを利用可能な状態にする。電源断・アプリ停止中の実行は保証されない。予約機構が利用不可、次回時刻が不明、または`view`で成立を確認できない場合は自動再開を主張せず、checkpointを残して制約を報告する。

このone-shot heartbeatの作成後に同じchatへ戻り、枠回復・作業再開まで成功した実例はBackKeep Launcher taskの2026-10-03の実行履歴で確認した。desktop scheduled taskはローカルprojectを使う場合、PCとappを起動しておく必要がある。 [Codex scheduled tasks](https://learn.chatgpt.com/docs/automations?surface=app)

## 作業ファイル

- `repository/`: 最新main読取・監査用clone
- `drafts/`: 成果原本
- `briefs/`: agent契約
- `reports/`: 候補別証拠・run記録
- `tools/`: この作業のローカル補助CLI

過去の検証記録は `reports/` と `archive/` に保持する。履歴資料の旧手順は現行作業手順として扱わない。

## 単純作業をまとめる補助工程

- 複数原稿の正規化・hash計算・unique path組立は `tools/stage_upload.py stage` で元原稿と別copyへまとめる。本文を含まないmanifestで確認し、正規化copyを監査・reviewする。送信時は `emit` のbase64を復元し、UTF-8 decode/encodeの往復でbytes一致を確かめた文字列だけをContents APIへ渡す。create-only前に最新mainで宛先404を確認し、作成後は固定commitのbase64 readbackをstage emitのbase64と照合する（ASCII空白・TAB・CR/LFの行折返しだけ除去）。JSON再serializationや内容正規化はしない。詳細は [UPLOAD-STAGING.md](UPLOAD-STAGING.md)。2026-10-10にB45-p01/p02/p03すべてでこの方法のcreate-only upload、固定commit exact readback、公式receipt/precheck/submission/Research job/STATUSのterminal gatesを確認した。実例とhash・part別証拠は [B45 upload記録](reports/20261010-main-be057-worklist-5000/b45-upload-record.md)。p03を含む3 partすべてがterminal gateを通過してから次batchへ進む。成功応答やwaitingだけをimport完了と扱わず、各partのreceipt・precheck・submission・Research job・STATUSを確認する。処理効率・節約率は未計測。
- **2026-10-10 B50/B51 p03の完全通過例**: 原稿SHA-256 08ebded08f4fb5ea53b822778a3c3beaa306909ff52cfe4bde869d3a878a82fa、create-only commit 8e4f29f3a978054a7ef03e9e78837597e9ba38de。uploadからprecheck resultまで10分36秒、imported receiptまで23分19秒、STATUS再生まで25分49秒だった。receiptは20 records（9 accept / 11 relevance）、provider gap 0、precheckは9/9 allowed・duplicate / unresolved 0、通常Actionsのsubmission 2件は5+4件・最終duplicate 0・Research job 9件がすべてready。receipt後のSTATUS再生commitは37bb99bbb77a7f8498b26eaefd51900c1ca5462f。実際の経過は成果直結の証拠であり、短縮効果とはみなさない。source hash付きreceipt、precheck、submission結果、ID別Research job状態、直後のSTATUS反映まで揃ったため、後続partへ進む正規受け入れ例として記録する。
- 不変な原稿の再監査は `audit_drafts.py --reuse` の原本hash・監査コード・設定・環境fingerprintの条件を満たす場合だけ再利用する。正規化でhashが変われば再監査する。
- 先行する調査根拠は [効率調査記録](reports/20261004-processing-efficiency.md) に保持する。権限エラーの再試行抑制は未反映の提案で、定期ワーカー設定は変更していない。
- 固定SHA共有と小batchの実行契約は上記Research batchフローへ具体化した。`research-batch-run.example.json`を実際のcandidate packetとsnapshotへ置換して`generate_briefs.py`に渡す。根拠のないjob/claim確認や旧cloneへのfallbackを省略の代わりに使わない。権限エラー対策と定期ワーカー設定は未変更。

- 2026-10-08にGitHub接続障害を切り分け、通常sandboxのDNS失敗に対して、接続済みGitHub connectorと承認審査を通した `require_escalated` の公開repo読取・fetchが成功することを確認した。接続失敗時は [Codex接続復旧手順](CODEX-PAPER-ROUTE.md#github接続が拒否される場合) を使う。これは上記の旧「権限エラー対策未変更」を接続手順について更新するもので、定期ワーカー設定・global sandbox設定・upload契約は変更しない。
- **2026-10-10の待機並行screen検証**: B63 p02 (20 records)のContents API create-onlyから19分16秒後、source SHA一致のimported receipt (6 accept / 14 relevance / provider gap 0)を確認した。6件precheckは全件allowed・unresolved 0、正規submission 2件は5+1、重複0、生成したResearch jobs 6件はすべてready、直後STATUSは候補1119・整合性異常0。受け入れ待機中にB69/B70を順番にローカルscreenし、76 delegated candidatesの一次資料判定と成果物stageを進め、後続uploadは先行gate完了まで保留した。取得不能abstract 1件/3件も確認済みID・題名・一次URL・失敗理由付きborderlineで保持した。待機中のローカル探索継続が実行可能なことを確認したが、この1回からupload待ち時間の短縮効果は主張しない。


- **2026-10-10 B63 p03正規importの追加検証**: Contents API create-only commit `d7c45c0ed1d63bc40c327ba32041c8bf1bfa6334` のartifact SHA `5f96ebc3b9c895f682c78a432e48f95dd99179faff750e920a5ec486f12d0d12` は固定commit readback一致済み。receiptは14:28:13Zに同一source SHAで `imported`（10 records、1 accept/submit、9 relevance、provider gap 0）。正式precheckは1件allowed・duplicate/unresolved 0、submission `ok=true`・1 submitted、ID対応Research jobは `ready`、同時刻更新STATUSは候補1,120・整合性異常0。create commit時刻14:15:35Zからreceiptまで12分38秒の観測。Actions runの最終終了状態確認とは分け、receipt/job/STATUSのdurable evidenceを受け入れ根拠にする。証拠は `reports/20261010-main-57470d7-worklist-5000/upload-record.md`。単一実行の所要時間で一般の待機短縮を主張せず、後続ファイルは同じ全gateを個別に確認する。
- **2026-10-10 B71 p01 second verified serial-import example**: Part payload SHA-256 `4f36509b7fbdadab06e50f41e15acb8a66f82dba99860736e278e9ca71ce98cc`, 18,947 bytes; create-only Contents API commit `86b09afbdf1cf26407b7e2ad5aedb3b965b15adf`. Fixed-commit readback matched staged bytes and base64 exactly. At main `bb7b8d8664a5d2d441860bfee16a2004ddfa4706`, receipt was `imported` at 14:50:25Z for 20 records (1 accept + 19 relevance), source SHA exact, provider gap 0. Official precheck allowed the one exact candidate with unresolved 0; submission succeeded with 1 submitted, final duplicates 0; the linked Research job was `ready`. STATUS at 23:51 JST showed 1,121 candidates and zero consistency anomalies. Observed create-to-receipt duration was 17m12s; record as a single observation, not a general wait-time reduction. The following part was not sent until these terminal gates were verified.

- **2026-10-10 B71 p02 terminal example**: Contents API create-only + fixed-commit exact-byte readback succeeded; imported receipt source SHA matched (20 records, 5 accept / 15 relevance, provider gap 0), official precheck allowed exactly 5 IDs with 0 unresolved, submission succeeded with 5 submitted / 0 duplicate, all 5 matching Research jobs became `ready`, and regenerated STATUS reported 1,126 candidates / 0 consistency anomalies. Observed create-to-receipt duration was 7m52s for this artifact only; do not generalize it as a wait-time improvement.

- **2026-10-10 B72 p02 status-run example**: After create-only Contents API upload and fixed-commit exact-byte readback, the official precheck gate processed the unsettled request and resumed dedicated Discovery intake. Its receipt matched the source SHA (20 records, 1 accept / 19 relevance, provider gap 0); formal precheck allowed the single exact ID with unresolved/duplicate filters 0; submission created one Research job, which was `ready`. The status dashboard regenerated successfully at main `64ee9e4012913b60ca6561f6b3e33fbe9e620908`, increasing candidate and ready job counts 1,131→1,132 with anomalies 0 and `consistency: passed`. This confirms the official precheck → intake resume → receipt → candidate precheck → submission → Research job → STATUS sequence; evidence and hashes are in `reports/20261010-main-57470d7-worklist-5000/upload-record.md`.

- **転送時の改行保持**: `Get-Content -Raw` のPowerShell標準出力をContents APIの本文へ直結しない。2026-10-10のB71 p03でstage原本末尾LFの後へCRLFが2 byte追加され、importは成功したもののstage SHAとreceipt SHAが一致しなかった。`stage_upload.py emit` のbase64を呼出元で厳密にUTF-8文字列へ復元してContents APIへ渡し、固定commit readbackのbytes/SHAがstage manifestと一致するまで次のpartをHANDOFF_VERIFIEDにしない。

## STATUS再生成のpush競合からの復旧（2026-10-11確認）

- 正規import/precheck/submission/Research jobが成功しても、別の`status-dashboard.yml` publishがpush競合で失敗した場合は、直ちにDiscoveryの失敗とは扱わず、最新main上のreceipt・precheck・submission・候補別Research jobを先に照合する。
- runが終了し、別のdashboard runが動いておらず、失敗理由がretry上限までの`fetch first`競合であれば、最新mainへの公式`workflow_dispatch`を1回だけ実行できる。先のrunがactiveの間は重ねてdispatchしない。再度競合失敗したら連続再実行せず、書込競合を監査して復旧方針を決める。
- 受け入れ完了はrun成功だけで判定せず、最新mainのSTATUS生成時刻、候補/job件数の増分、該当job状態、整合性異常0、`consistency: passed`をreadbackで確かめる。これらを確認してから次のpartを送る。
- 実例: B72 p01の5件はreceipt/precheck/submission後に全Research jobがreadyだった一方、最初のSTATUS publishは4回のpush競合で失敗した。最新main `9a3557a74`への公式dispatchは成功し、main `2b73edad1`でSTATUSが00:45 JSTに更新、未claim job 1,126→1,131、整合性異常0、consistency passedを確認した。履歴は`reports/20261010-main-57470d7-worklist-5000/upload-record.md`。

## 2026-10-10 B72 p03 end-to-end accepted example

- Local stage SHA-256 `31f542ab5359b4514a1d0509b1a653958597274025c057905e4f7fbfe0d4eef8` (10 records, 2 accept / 8 relevance) was registered create-only at `.survey/import-inbox/pending/discovery/` through Contents API. Fixed-commit `51d19b30622eb206ec5a2d0ba73c6e7d723ba1dc` base64 readback matched `stage_upload.py emit` exactly after removing connector line-folding whitespace; the Git blob SHA was `c88ccd4a1e87903be617fcfd10062ddeebea051f`.
- The official durable receipt matched the payload source SHA and recorded `imported`, 10 records, 2 accept / 8 relevance, provider gap 0. Candidate precheck `libimp-191ecf28271c34ae-pre01` was `ok=true` / `READY_FOR_EVALUATION`, allowed both exact IDs (`arXiv:2511.19575`, `arXiv:2606.04719`), and had unresolved/duplicate/rejection filters 0. Official submission result `libimp-191ecf28271c34ae-pre01-sub01` was `ok=true`, submitted 2, final duplicates 0; both matching Research jobs became `ready`.
- Dashboard run `38075196815` completed successfully. At latest main `2020a4dd9a232c2455a8b16d2e249ccf80134d86`, regenerated `STATUS.md` at 2026-10-11 03:33 JST reported candidate papers and ready Research jobs rising 1,132→1,134, consistency anomalies 0, `consistency: passed`, and `metadata: passed`. This is terminal acceptance evidence; downstream files may proceed after their own latest-main audit and all the same per-artifact gates.
- Detailed paths and timestamps are in `reports/20261010-main-57470d7-worklist-5000/upload-record.md`.
