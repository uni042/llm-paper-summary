# Continuous discovery policy

この文書は、探索専用Scheduled Chat workerが1回の実行枠で可能な限り探索を継続するための停止・継続条件の正本とする。既存の通常論文workerのdiscovery責務は変更しない。

## 基本原則

- **在庫水位は停止条件ではない**。target=50、low=25、critical=15は探索優先度を決めるための水位であり、探索専用workerが止まる理由にはしない。
- **固定ラウンド上限を設けない**。固定件数、固定batch数、固定round数で探索を打ち切らない。
- **空振り・全重複・低採用率は停止理由にしない**。その軸をいったん離れ、別の独立探索軸へ切り替える。
- **単一ソースの障害・rate limitは停止理由にしない**。利用可能な別ソース、別クエリ、別探索経路へ切り替える。
- 1論文の取得不能、1候補の判定不能、1回の重複競合、1回のGitHub write失敗はrun全体の終了理由にしない。
- GitHubへのcandidate投入が失敗しても、ChatGPT Library `/LLM-survey-outbox/pending/` へ完全なoffline job seedを耐久保存できるなら探索を継続する。

## 1回のrunでの探索ループ

各roundで `discovery-state.json` の直近統計を読み、重複率・採用率・直近の探索軸を確認する。そのうえで以下から未消化または再探索価値のある独立軸を選ぶ。

1. 新着論文探索
2. 収録済み重要論文のforward citation
3. 重要論文のbackward reference
4. DBMS / OS / storage / distributed systems / HPC / GPU runtime / networking等の隣接分野
5. 直近採用候補からの検索語・著者・実装・引用クラスタ拡張
6. offload / hierarchical memory / MoE / expert placement-cache-prefetch / KV cache / scheduling / disaggregation / inference framework等の重点テーマ
7. 直近で高採用率だった軸の近傍探索。ただし同一queryの機械的反復は禁止する。

1 roundが終わったら候補を耐久保存し、残り実行余力と未探索軸を再評価する。探索余力があり、有望な独立軸が残っている限り次roundへ進む。

## soft failure時の動作

以下はrun停止ではなく、その場で局所回復する。

- 検索結果0件: queryを広げる、時期・用語・関連分野を変える。
- 全重複: その軸の重複率を記録し、別軸へ移る。
- 低採用率: 採用率を記録し、別ソースまたは隣接軸へ移る。
- 一次資料が1件だけ読めない: その候補を保留し、他候補・他軸へ進む。
- 1つの検索サイト/APIが失敗・rate limit: 別ソースへ切り替える。
- GitHub SHA競合: 最新HEADを取り直し、再重複判定してから再試行する。
- GitHub write不可: Library fallbackが生きていればoffline seedとして保存して継続する。

## hard stop

探索専用workerがrunを終了してよいのは、原則として次のいずれかだけとする。

1. 正本repo/identity/queueを読めず、安全な重複判定そのものができない。
2. **GitHubとLibraryの両方へ耐久保存できない**ため、発見状態を失わずに継続できない。
3. Chat/connector/tool等の**実行上限**に到達し、そのrunで追加の探索を実行できない。
4. 軸変更、引用追跡、隣接分野、検索語拡張まで行ったうえで、**有望な独立探索軸を合理的に使い切った**。

単にcandidate_inventoryが50以上になった、1 roundが空だった、重複率が高かった、候補を数件投入できた、という理由では終了しない。

## 通常論文workerとの関係

このポリシーは探索専用workerの継続性を強化するものであり、通常論文workerのdiscoveryを置き換えない。通常workerは従来どおりresearch / audit / discoveryを行う。
