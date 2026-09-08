# Identity deltas

`paper-identity-index.json`（索引形式3）へまだcompactされていない、小さい識別変更を置く。

- 1研究1差分。
- 必須属性は `schema_version`, `canonical_id`, `path`, `identifiers`。
- 論理索引は **未compact差分を先に、形式3スナップショットを後に**参照する。
- 同じ識別子が別canonical IDへ向く差分は保存しない。
- 完全checkoutが使える保守時に `python scripts/identity_delta.py validate` と `compact` を実行する。
- compactは論文の精読・監査件数を増やさず、論文frontmatterから形式3を再生成した後に適用済み差分を削除する。

通常の論文保存で巨大な `paper-identity-index.json` 全体を取得・全置換する必要はない。
