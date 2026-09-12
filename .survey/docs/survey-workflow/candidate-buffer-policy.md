# Candidate buffer policy

この文書は論文survey workerの **candidate供給・discovery水位制御** の正本とする。既存の `queue-v10.md` にある「actionable readyが尽きたらdiscovery」という受動的な記述より、本書の水位制御を優先する。research品質、transport、fallback、maintenance、08:30 routing等は従来の正本に従う。

## 目的

research workerが候補枯渇で停止しないよう、discoveryをresearch開始の前処理ではなく独立した在庫補充工程として扱う。弱い論文で件数を埋めず、有望候補を先に広く集め、researchはその候補群から優先度順に全文精読する。

## 水位

重複排除後の未処理research候補を `candidate_inventory` とする。

- `target_inventory = 50`
- `low_watermark = 25`
- `critical_watermark = 15`

通常は50本前後の候補在庫を目標にする。25本未満になった時点でdiscovery補充をresearchと並行して加速し、15本未満では候補枯渇防止を優先してdiscovery比重をさらに上げる。0本になるまで待ってから探索を始めてはならない。

50本はhard capではない。50本を超えた場合も、低コストな新着確認・引用追跡等で高価値候補が見つかるならcandidate poolへ追加してよい。件数維持のために弱い候補を採用しない。

`candidate_inventory` はGitHub queueの未処理research候補、Library/GitHub fallback由来の未checkpoint spillover、candidate pool相当の未処理候補をcanonical ID / arXiv ID / DOI / normalized titleで重複排除して数える。blocked/deferredで現在research不能な論文は通常在庫に含めない。

## DiscoveryとResearchの分離

Discovery段階では原則として全文精読しない。タイトル、abstract、書誌情報、一次資料の存在、既収録identityとの重複、テーマ適合性、新規性の見込みを軽量評価し、「全文を読む価値がある候補」をcandidate poolへ積む。

Research段階で初めて一次資料全文を取得・精読し、repository-qualityの5-slot structured recordを作る。Discoveryで得たabstractや検索snippetだけからresearch内容を推測しない。

この分離により、1回のdiscoveryで1本だけ見つけて即researchする方式に固定せず、先に複数候補を蓄積できるようにする。

## 複数worker協調

candidate供給は2つのScheduled Chat workerが共有する。

1. **通常論文worker（毎時:30）**: research / auditに加えて、従来どおりdiscoveryも行う。
2. **探索専用worker（毎時:00）**: discovery、軽量候補評価、priority付与、candidate投入だけを行う。

探索専用workerの追加を理由に通常論文workerのdiscoveryを停止・縮小しない。両workerは同じ `candidate_inventory`、identity、queue、discovery stateを共有する。

二重投入を防ぐため、両workerとも探索開始前とcandidate投入直前に最新HEADを再確認し、canonical ID / arXiv ID / DOI / OpenReview ID / normalized titleで再重複判定する。片方が探索中にもう片方やActionsが同じ候補を先に登録した場合、後発workerはその候補を送らない。競合が残る場合も正本側のdedupeで1候補へ収束させる。

`discovery-state.json` 等の共有stateを書き換える場合は最新blob SHAを取得し、古いSHAで上書きしない。SHA競合は最新stateを再取得して該当更新だけ再評価する。

探索専用workerの毎時runは通常論文workerの24-run maintenance counterへ加算しない。探索専用workerの詳細契約は `discovery-specialist-worker.md` を正本とする。

## 探索経路

在庫補充では同じ検索語を反復せず、以下を独立した探索経路として組み合わせる。

1. **新着探索**: arXiv、OpenReview、会議等から重点テーマの新規論文を広めに拾う。
2. **被引用探索**: 収録済み重要論文を引用する新しい論文を追う。
3. **参考文献探索**: 重要論文のreferenceから未収録の基礎・過去研究を拾う。
4. **隣接分野探索**: DBMS、OS、storage、distributed systems、HPC、GPU runtime、networking等からLLM serving / inferenceへ接続する研究を探す。
5. **検索語自動拡張**: 直近で採用率が高かった候補のtitle / abstract / keywordから新しい検索語を抽出し、次の探索軸に使う。
6. **既存の重点テーマ探索**: offload / hierarchical memory / MoE / expert placement・cache・prefetch / KV cache / scheduling / disaggregation / inference framework等を継続する。

探索ラウンドごとに、取得候補数、重複除外数、新規候補数、candidate採用数、採用率、探索軸を記録する。高重複・低採用率の軸は直後に繰り返さず、別経路へ切り替える。採用率の高い探索語・探索経路は次回の候補生成へ再利用する。

## 優先順位

candidateにはresearch priorityを付ける。少なくとも以下を考慮する。

- repoの重点テーマとの関連度
- 手法・システムとしての新規性
- 既存収録論文との差分
- 実測評価・実装公開の有無
- SSD/NVMe、MoE、階層メモリ、serving基盤等への研究価値
- 新しさだけでなく、重要な基礎研究・引用関係上の価値

research workerは原則としてpriorityの高い候補から処理する。candidate poolが大きくなった場合もFIFOだけで消化しない。

## Run内の制御

maintenance runと08:30 other-update runを除くpaper workerでは、run開始時とjob処理後にcandidate_inventoryを再評価する。

- 25以上: priority順researchを主処理としつつ、低コストdiscoveryを許可する。
- 15〜24: researchを継続しながらdiscovery補充を積極化する。
- 0〜14: discovery補充を優先し、複数の探索経路を使って在庫回復を図る。見つかった高priority候補のresearchを同一runで進めてもよい。
- 50以上: researchを主処理とするが、高価値候補を逃さないため低コスト探索は停止必須としない。

固定件数・固定batch数は設けない。候補が0件の探索ラウンドがあっても別軸へ切り替える。プラットフォーム上限、耐久保存不能、または合理的に有望探索軸を使い切った場合のみそのrunのdiscoveryを終了する。

## GitHub write不能時

GitHub write不能でもLibrary `/LLM-survey-outbox/pending/` へoffline job seedを耐久保存できるなら、同じ水位方針でcandidateを補充する。candidate seedを保存した後は、必要に応じてpriority上位候補のresearchを同一runで進める。transport envelope、job ID、replayは `fallback-routing.md` と `continuation-policy.json` を正本とする。

探索専用workerはGitHub write不能時でもresearchへ進まず、candidate seedの耐久保存までに留める。

## 08:30 reporting

08:30 JSTの報告では従来の「直近24時間の発見数・追加数・残候補数」に加え、可能なら `candidate_inventory / target_inventory` を示す。在庫がlow watermark未満ならその旨を短く示す。集計できない場合は推測値で埋めない。
