# Discovery search-result filter

この文書はDiscovery検索結果をcandidate評価へ渡す前の取得時フィルター契約を定義する。目的は、既収録・既投入論文が検索ランキング上位を占有しても、その論文をcandidateとして再評価せず、同じ検索軸のより深い未収録結果まで到達することである。

## 正本

重複照合の正本は最新default branchの `.survey/work-queue/discovery-identities/` とする。この照合面は `queue_worker.existing_candidate_keys()` から生成され、最終重複ゲートと同じ正規化済みidentity token集合を持つ。

`.survey/scripts/discovery_search_filter.py` はこの契約の参照実装である。GitHubコード検索（code search）はnavigation補助に限り、コード検索で見つからないことを未収録判定の根拠にしない。

## 検索結果取得時の必須処理

検索providerから1ページまたは1バッチを受け取るたび、relevance評価、priority付与、candidate選定より前に次を行う。

1. 結果ごとにcanonical ID、arXiv ID、DOI、OpenReview ID、URL、titleを取得できる範囲で抽出する。
2. `paper_identity.py` と同じ規則でidentity tokenへ正規化し、対応するDiscovery identity shardと照合する。
3. snapshotに存在する結果はその場で除外し、candidate評価へ渡さない。
4. snapshotに存在しない結果だけを未収録検索結果として蓄積する。
5. 同一バッチ内で同じprimary identityが重複した場合も1件へ畳み込む。

snapshotまたはmanifestが取得不能・不整合なら、検索結果を未収録と推定して通してはならない。正本再取得を試み、それでも照合不能なら既存のcontinuation/finalization gateへcanonical read failureとして渡す。

## 次ページ・次cursorへの継続

検索providerがページング、cursor、offset等を提供し、現在の探索軸で十分な未収録結果をまだ確認できていない場合は、既収録結果を候補数へ数えずに次ページ・次cursorを取得する。

たとえば上位20件のうち18件がsnapshotで既収録なら、その18件をcandidateとして再評価せず、未収録2件だけを保持して次ページへ進む。検索上位が既収録論文で埋まっていることを、その探索軸の枯渇とみなしてはならない。

provider側のページ・cursorが尽きた場合は、既収録論文を再投入して件数を埋めず、`discovery-state.json` と探索方針に従って別の独立探索軸へ切り替える。

ここで使う「十分な未収録結果」は検索の深掘り判断のための作業上の目安であり、runのcandidate件数ノルマや停止条件ではない。品質基準を満たす候補が少なければ少ないままでよく、件数を埋めるために弱い論文や既収録論文を採用してはならない。

## 三段階の重複防止

取得時フィルターを追加しても後段の安全網は削除しない。

- 第1段階: 各検索ページ・バッチの取得直後にsnapshotで既収録結果を除外する。
- 第2段階: candidate採用時に最新default branchのsnapshotを再取得して照合する。
- 第3段階: immutable Discovery submission書き込み直前に再度最新HEADへ更新して照合する。

その後のActions最終重複ゲートも競合・同時投入に対する最終安全網として維持する。

## 観測値

workerは少なくとも、検索した生結果数、取得時に既収録として除外した件数、実際にcandidate評価へ渡した未収録結果数、走査したページまたはcursor数をrun内で把握する。これらは探索効率を診断するtelemetryであり、単独ではrun停止条件にしない。
