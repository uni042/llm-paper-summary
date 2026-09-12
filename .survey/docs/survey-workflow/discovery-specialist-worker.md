# Discovery specialist worker

この文書は、既存の論文workerとは別に毎時実行する **探索専用Scheduled Chat worker** の正本とする。目的はcandidate在庫を継続的に積み上げることであり、既存の論文workerからdiscovery責務を取り上げない。

## 役割

- 探索専用worker: discovery、軽量重複判定、候補評価、priority付与、candidate投入だけを担当する。
- 既存の論文worker: 従来どおりresearch / audit / discoveryを行う。探索機能を削除・停止しない。
- GitHub Actions: queue/state/identityの最終整合、重複抑止、job materializationを担当する。

探索専用workerはresearch、audit、5-slot structured research record作成、論文Markdown生成を行わない。候補発見後に全文精読へ進まず、candidate poolへ安全に投入して次の探索軸へ進む。

## 実行時刻

探索専用workerは毎時 `:00` JSTに実行する。既存の論文workerは従来どおり毎時 `:30` JSTで動作する。30分ずらすことで、両者が同じqueue/stateを書き換える時間的競合を減らす。

探索専用workerは既存の24-run maintenance counterへ加算しない。maintenance gateは既存の論文worker側の正本に従う。

## 必読正本

毎回default branch最新HEADを取得し、同じHEADから最低限以下を読む。

1. `candidate-buffer-policy.md`
2. `queue-v10.md`
3. `fallback-routing.md`
4. `continuation-policy.json`
5. `.survey/work-queue/next-jobs.json`
6. `.survey/work-queue/discovery-state.json`
7. `.survey/survey-state/paper-identity-index.json`
8. 必要に応じて `.survey/survey-state/identity-deltas/**` と既存job

この文書と他文書が競合する場合、探索専用workerの役割分離については本書、candidate水位と探索経路については `candidate-buffer-policy.md`、transportについては `fallback-routing.md` / `continuation-policy.json` を優先する。

## candidate在庫

`candidate-buffer-policy.md` の水位を共有する。

- target: 50
- low watermark: 25
- critical watermark: 15

探索専用workerは在庫が50以上でも停止必須ではない。低コスト探索で高価値候補が見つかる場合は追加してよい。ただし在庫数を満たすために弱い候補を採用しない。

## 探索経路

各runでは直近の `discovery-state.json` を読み、直前の高重複軸を機械的に繰り返さない。候補経路は少なくとも以下から選ぶ。

- 新着論文
- 収録済み重要論文の被引用
- 重要論文の参考文献
- DBMS / OS / storage / distributed systems / HPC / GPU runtime / networking等の隣接分野
- 直近採用候補からの検索語拡張
- offload / hierarchical memory / MoE / expert cache・placement・prefetch / KV cache / scheduling / disaggregation / inference framework等の重点テーマ

固定件数で埋めない。1軸が0件または全重複なら別軸へ切り替える。

## 二重探索・二重投入の防止

探索開始前とcandidate投入直前の **2段階** で重複判定する。

照合対象:

1. paper identity index
2. identity deltas
3. 既収録paper
4. 既存research / discovery jobs
5. GitHub fallback inbox/archive
6. 可能な範囲でLibrary pending/offline seed

同一性判定はcanonical ID、arXiv ID、DOI、OpenReview IDを優先し、最後にnormalized titleを使う。

探索開始後に既存workerやActionsが同じ候補を先に投入する可能性があるため、write直前に最新HEAD / queue / identityを再取得する。そこで既存化していた候補は送らない。

両workerが同じ論文を同時に発見した場合も、同じcanonical IDから同一candidateとして扱い、Actions側の重複抑止で1件へ収束させる。重複候補を別jobとして意図的に作らない。

## candidate priority

priorityは少なくとも以下を考慮する。

- 重点テーマとの関連度
- 新規性と既存収録との差分
- 実測評価の有無
- 公式実装・コード公開の有無
- 引用関係上の重要度
- SSD/NVMe、MoE、階層メモリ、serving基盤への研究価値

単純FIFOではなく、research workerが価値の高い候補から読めるようpriorityを付ける。

## transport

GitHub write可能時は既存workflow v10のdiscovery transportを使い、paper/state/READMEを直接編集しない。

GitHub write不能時は `fallback-routing.md` に従い、ChatGPT Library `/LLM-survey-outbox/pending/` へoffline job seedを完全envelopeとして耐久保存する。完成Markdownやresearch recordを作らない。

同一payloadの重複保存を避け、復旧時は既存のimmutable intake経路に従う。

## discovery-state

各runで可能な範囲で探索軸、query概要、取得候補数、重複数、新規候補数、採用数、採用率、次回推奨軸を記録する。複数workerが同じ `discovery-state.json` を更新する場合は、write直前に最新SHAを再取得して競合を避ける。SHA競合時に古いstateで上書きしない。

## 通知

通常成功時はユーザーへ通知しない。GitHubとLibraryの両方へ候補状態を耐久保存できない、継続的な重複競合でcandidate投入不能、または正本が読めず安全に探索できない場合だけ問題として通知する。
