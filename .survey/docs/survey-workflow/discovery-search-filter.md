# Discovery search-result filter

この文書はDiscovery検索結果をcandidate評価へ渡す前の取得時filter/collector契約を定義する。目的は、既収録・既投入論文や過去にcandidate評価で不採用となった論文が検索上位を占有しても、それらを再評価せず、より深い未収録・未評価結果まで到達することである。

## 正本

既収録・既投入論文の重複照合正本は最新default branchの `.survey/work-queue/discovery-identities/` とする。この照合面は `queue_worker.existing_candidate_keys()` から生成され、最終重複ゲートと同じ正規化済みidentity token集合を持つ。

candidate評価で不採用となった論文の除外正本は immutable Discovery submission の `rejected_candidates` とする。`.survey/scripts/build_discovery_rejection_ledger.py` がそれらを集約し、派生索引 `.survey/work-queue/discovery-rejections.json` を生成する。ledgerにはidentity token、最新の不採用理由、初回/最終不採用時刻、rejection count、axis、source submissionを保持する。

`.survey/scripts/discovery_search_filter.py` はこの2つの除外面を使う参照実装である。GitHubコード検索はnavigation補助に限り、コード検索で見つからないことを未収録判定の根拠にしない。

## workerへ渡す前のprefetch buffer

Discoveryの標準経路では、1ページごとの検索結果をcandidate評価workerへ返さない。`discovery_search_filter.collect_until_unseen(...)` がproviderのpage/cursor取得を内包し、既収録・既投入・過去の評価落ち・ページ間重複を除外した**未収録かつ未評価落ちの検索結果が10件たまるまで**複数ページを内部で取得・蓄積する。

標準閾値は `DEFAULT_PREFETCH_UNSEEN = 10` とする。10件はcandidate採用ノルマではなく、candidate評価へ一度に渡す前処理済み検索結果bufferの大きさである。10件のうち何件をcandidateへ採用するかは後段の品質評価で決める。

最後に取得したページで10件を超えた場合、そのページ内の未収録結果を切り捨てないため、workerへ返るbufferは10件より多くてもよい。providerが尽きた場合は10件未満でも、その時点までのbufferを返す。

## 検索結果取得時の必須処理

collectorが検索providerから1ページまたは1バッチを受け取るたび、relevance評価、priority付与、candidate選定より前に次を行う。

1. 結果ごとにcanonical ID、arXiv ID、DOI、OpenReview ID、URL、titleを取得できる範囲で抽出する。
2. `paper_identity.py` と同じ規則でidentity tokenへ正規化し、Discovery identity snapshotと照合する。
3. 既収録・既投入identityに一致する結果はcandidate評価bufferへ入れない。
4. `discovery-rejections.json` のidentity tokenにも照合し、過去にcandidate評価で不採用となった論文もcandidate評価bufferへ入れない。
5. どちらにも一致しない結果だけをcollector内部へ蓄積する。
6. 同一ページ内だけでなく、collectorが走査した複数ページ間でも同じprimary identityは1件へ畳み込む。
7. bufferが10件未満で `next_cursor` / page / offset が残るなら、collector自身が次ページを取得して処理を繰り返す。
8. bufferが10件以上になった時点、providerが尽きた時点、または明示的な安全上限へ達した時点でのみcollector結果をcallerへ返す。

identity snapshot、manifest、または存在するrejection ledgerが取得不能・不整合なら、検索結果を未収録と推定して通してはならない。正本再取得を試み、それでも照合不能なら既存のcontinuation/finalization gateへcanonical read failureとして渡す。

## candidate評価で不採用にした論文の記録

collectorからworkerへ渡された論文をcandidate評価した結果、submissionの `candidates` に採用しなかった論文は、重複・既収録として落としたものを除き、同じimmutable Discovery submissionのトップレベル `rejected_candidates` に記録する。

各entryには少なくとも最も強いidentity情報、title、取得できるならsource URL、および具体的な `rejection_reason` を含める。例:

```json
{
  "rejected_candidates": [
    {
      "canonical_id": "arXiv:2609.12345",
      "title": "Example Paper",
      "source_url": "https://arxiv.org/abs/2609.12345",
      "rejection_reason": "survey scopeには近いがsystem-level evaluationが不足"
    }
  ]
}
```

`rejected_candidates` は「今回採用しなかった」という事実をdurableに残すための欄であり、次回以降のretrieval-stage除外に使う。既収録重複やfilterで事前除外された論文はここへ再記録しない。

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

## 多段の重複・再評価防止

- 第1段階: collector内部で複数検索ページを走査し、既収録・既投入・過去の評価落ち・ページ間重複を除外して未収録/未評価落ち10件前後のbufferを作る。
- 第2段階: candidate採用時に最新default branchのidentity snapshotを再取得して照合する。
- 第3段階: immutable Discovery submission書き込み直前に再度最新HEADへ更新して照合する。
- candidate評価落ちは同じsubmissionの `rejected_candidates` に保存し、ledger更新後の次回検索から第1段階で除外する。

その後のActions最終重複ゲートも競合・同時投入に対する最終安全網として維持する。

## 観測値

collectorは少なくとも、検索した生結果数、既収録/既投入として除外した件数、rejection ledgerで除外した件数、ページ間重複除外数、workerへ返した未収録結果数、走査したページまたはcursor数、target到達有無、provider枯渇有無を返す。workerはcandidate評価後の採用件数と `rejected_candidates` 件数も記録する。これらは探索効率を診断するtelemetryであり、candidate採用件数ノルマにはしない。
