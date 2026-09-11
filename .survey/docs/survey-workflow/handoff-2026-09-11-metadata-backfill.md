# メタデータ補完作業の引き継ぎ（2026-09-11）

## 最優先

全論文のfrontmatterメタデータ補完を、本文の内容修整より先に完了する。

必須項目と判定条件は `.survey/scripts/audit_metadata_coverage.py` を正本とする。再開時は最初に次を実行する。

```bash
python .survey/scripts/audit_metadata_coverage.py \
  --repo-root . \
  --json-out .survey/reports/metadata-coverage-latest.json
```

## 中断時点

- 推論: 269本中192本が必須項目を充足、77本が未完了。
- 学習: 19本中18本が充足。ZeRO-Infinityのみ著者とarXiv分類が未完了。
- サーベイ: 3本中3本が充足。
- 01〜06系統、10系統は一括補完済み。
- 07〜09系統は中断により未完了が多い。
- 11系統と99系統は大半を補完済みだが、公開日が未記録の論文が一部残る。

数値は中断時点のスナップショットであり、必ず最新レポートを再生成してから残件を割り振る。

## 再開順

1. `metadata-coverage-latest.json` の `incomplete` を系統別にLunaへ分割する。
2. 07〜09系統の残件を優先する。
3. 11・99系統の少数残件を処理する。
4. 学習のZeRO-Infinityを補完する。
5. 全件完了後に `survey.py build`、単体テスト、品質監査、整合性検査を実行する。
6. 学習論文のfrontmatter変更後は `.survey/survey-state/frozen-training.json` の基準ハッシュを意図的に更新する。

## 注意事項

- arXiv分類は `arxiv_categories.primary` と `arxiv_categories.cross_list` を分け、arXiv表示をそのまま保存する。
- `code`は公式URLを確認できた場合だけ記録する。確認できない場合はキーを残して`null`とする。
- `implementation`には、実装形態、公開の有無、確認範囲を区別して書く。
- メタデータ補完だけの回では本文、監査済み日、監査版数を不用意に変更しない。
- 総説論文も識別子索引、重複排除、品質監査へ含める修正が入っている。
