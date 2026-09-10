# Paper mechanical quality audit

`.survey/scripts/audit_paper_quality.py` は `papers/inference/**/*.md` を全件走査し、`.survey/templates/paper.md` のうち機械判定できる品質条件を一覧化する。

監査対象の判定はfrontmatterや`canonical_id`の正常性に依存させない。カテゴリ索引の`README.md`、横断比較表`comparison.md`、正規の移動先だけを示す`# Moved`ファイルだけを除外する。

## 実行

```bash
mkdir -p audit-output
python .survey/scripts/audit_paper_quality.py \
  --markdown-out audit-output/paper-quality-audit.md \
  --json-out audit-output/paper-quality-audit.json \
  --no-fail-exit
```

GitHub Actionsの `.github/workflows/paper-quality-audit.yml` も同じ監査を行い、結果はrepositoryへ固定保存せず7日間のworkflow artifactとして保持する。

## 既定の機械判定

- UTF-8ファイルサイズ: 4,500 bytes以上
- 説明文: 2,200文字以上
- 説明段落: 10段落以上
- 明示的な手法節の説明段落: 4段落以上
- 手法節内に主要機構が3個以上ある場合、各主要機構に2段落以上
- 説明文の日本語文字率: `.survey/scripts/japanese_style.py` の共通規則
  - 70%未満: FAIL
  - 70〜80%: WARN
- 日本語・カタカナへ自然に置換できる裸の英語専門語はFAIL

手法節は `## 手法` だけでなく、`## 手法のあらまし`、`## 提案手法`、`## 手法1: ...` など既存の互換見出しも認識する。

1つの手法節へまとめず機構ごとのH2で説明する長文要約は、十分な説明量と複数の機構節を持つ場合に限り **構造化手法相当（structured-equivalent）** と判定する。この救済規則で短い要約を合格させない。

日本語文字率はfrontmatter、URL、コード、Markdownリンク先、見出し、表、一次資料、更新履歴などを除外して計算する。固有名詞やモデル名の影響を受けるため補助指標とし、用語規則は裸の英語専門語検出を主判定とする。

## 回帰試験

```bash
python -m unittest discover -s .survey/tests -p 'test_audit_paper_quality.py'
```

意味的な品質基準の正本は常に `.survey/templates/paper.md`。機械閾値や英語専門語規則を変更する場合は、checkerと回帰試験を同時に更新する。
