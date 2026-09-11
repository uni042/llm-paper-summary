# メタデータ補完作業の完了記録（2026-09-11）

## 状態

全論文のfrontmatterメタデータ補完は完了済み。通常の論文サーベイを優先してよく、この作業を再開タスクとして扱わない。

必須項目と判定条件の正本は `.survey/scripts/audit_metadata_coverage.py`、最新の実測状態は `.survey/reports/metadata-coverage-latest.json` とする。論文追加により本数は変動するため、この文書中の本数ではなく最新レポートを参照する。

2026-09-11の完了検証時点では、推論276本、学習19本、サーベイ4本の合計299本が必須項目をすべて充足し、未完了0件だった。同じworking treeで単体テスト15件が成功し、repository-wide consistency checkも findings 0 で通過した。

## 今後の運用

新規論文はstructured recordからMarkdownを生成する段階で必須メタデータを保持し、通常のvalidatorと監査で欠損を防ぐ。既存・新規を問わず確認したい場合は次を実行する。

```bash
python .survey/scripts/audit_metadata_coverage.py \
  --repo-root . \
  --json-out .survey/reports/metadata-coverage-latest.json \
  --strict
```

必要に応じて `.survey/scripts/backfill_paper_metadata.py` を使えるが、既存の非空値は上書きしない。`code` は公式URLを確認できた場合だけ記録し、確認できない場合はキーを残して `null` とする。`implementation` は実装形態、公開の有無、確認範囲を区別して記録する。

arXiv論文は `arxiv_categories.primary` と `arxiv_categories.cross_list` を分離して保存する。学習論文のfrontmatterを意図的に変更した場合は `.survey/survey-state/frozen-training.json` の基準ハッシュも明示的に更新する。

サーベイ論文も識別子索引、重複排除、品質監査の対象とする。
