# Discovery search-result filter

この文書はDiscovery検索結果をcandidate評価へ渡す前の取得時フィルター契約を定義する。目的は、既収録・既投入論文が検索ランキング上位を占有しても、その論文をcandidateとして再評価せず、同じ検索軸のより深い未収録結果まで到達することである。

## 正本

重複照合の正本は最新default branchの `.survey/work-queue/discovery-identities/` とする。この照合面は `queue_worker.existing_candidate_keys()` から生成され、最終重複ゲートと同じ正規化済みidentity token集合を持つ。

`.survey/scripts/discovery_search_filter.py` はこの契約の参照実装である。GitHubコード検索（code search）はnavigation補助に限り、コード検索で見つからないことを未収録判定の根拠にしない。

## workerへ渡す前のprefetch buffer

Discoveryの標準経路では、1ページごとの検索結果をcandidate評価workerへ返さない。`discovery_search_filter.collect_until_unseen(...)` がproviderのpage/cursor取得を内包し、既収録・既投入・ページ間重複を除外した**未収録検索結果が10件たまるまで**複数ページを内部で取得・蓄積する。

標準閾値は `DEFAULT_PREFETCH_UNSEEN = 10` とする。10件はcandidate採用ノルマではなく、candidate評価へ一度に渡す前処理済み検索結果bufferの大きさである。10件のうち何件をcandidateへ採用するかは後段の品質評価で決める。

最後に取得したページで10件を超えた場合、そのページ内の未収録結果を切り捨てないため、workerへ返るbufferは10件より多くてもよい。providerが尽きた場合は10件未満でも、その時点までの未収録bufferを返す。

## 検索結果取得時の必須処理

collectorが検索providerから1ページまたは1バッチを受け取るたび、relevance評価、priority付与、candidate選定より前に次を行う。

1. 結果ごとにcanonical ID、arXiv ID、DOI、OpenReview ID、URL、titleを取得できる範囲で抽出する。
2. `paper_identity.py` と同じ規則でidentity tokenへ正規化し、対応するDiscovery identity shardと照合する。
3. snapshotに存在する結果はその場で除外し、candidate評価bufferへ入れない。
4. snapshotに存在しない結果だけを未収録検索結果としてcollector内へ蓄積する。
5. 同一ページ内だけでなく、collectorが走査した複数ページ間でも同じprimary identityは1件へ畳み込む。
6. 未収録bufferが10件未満で `next_cursor` / page / offset が残るなら、collector自身が次ページを取得して処理を繰り返す。
7. 未収録bufferが10件以上になった時点、providerが尽きた時点、または明示的な安全上限へ達した時点でのみcollector結果をcallerへ返す。

snapshotまたはmanifestが取得不能・不整合なら、検索結果を未収録と推定して通してはならない。正本再取得を試み、それでも照合不能なら既存のcontinuation/finalization gateへcanonical read failureとして渡す。

## provider adapter契約

`collect_until_unseen(fetch_page, ...)` の `fetch_page(cursor)` は、検索provider固有のpage/cursor/offset処理を隠蔽し、少なくとも次の形を返す。

```json
{
  "records": [
    {"arxiv_id": "2609.12345", "title": "..."}
  ],
  "next_cursor": "opaque-next-cursor-or-null"
}
```

collectorより上位のcandidate評価workerは中間ページ単位のcandidate選別を行わず、collectorが返した最終bufferだけを評価対象にする。

providerがページング、cursor、offset等を公開しない場合は、provider adapter側が期間・arXiv月・引用方向・隣接キーワード等の検索窓をずらし、未走査集合を次cursor相当としてcollectorへ供給してよい。同一queryの単純再実行はpagination扱いにしない。

## 三段階の重複防止

取得時collectorを追加しても後段の安全網は削除しない。

- 第1段階: collector内部で複数検索ページを走査し、既収録・既投入・ページ間重複を除外して未収録10件前後のbufferを作る。
- 第2段階: candidate採用時に最新default branchのsnapshotを再取得して照合する。
- 第3段階: immutable Discovery submission書き込み直前に再度最新HEADへ更新して照合する。

その後のActions最終重複ゲートも競合・同時投入に対する最終安全網として維持する。

## 観測値

collectorは少なくとも、検索した生結果数、取得時に既収録として除外した件数、ページ間重複除外数、workerへ返した未収録結果数、走査したページまたはcursor数、target到達有無、provider枯渇有無を返す。これらは探索効率を診断するtelemetryであり、candidate採用件数ノルマにはしない。
