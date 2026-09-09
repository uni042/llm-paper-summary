# Paper mechanical quality audit

`.survey/scripts/audit_paper_quality.py` は `papers/inference/**/*.md` にある実体付きの論文要約を全件走査し、`.survey/templates/paper.md` のうち機械的に判定できる品質条件を一覧化する。論文要約はfrontmatterに空でない `canonical_id` を持つファイルと定義する。カテゴリ索引の `README.md`、横断比較表、正規の移動先だけを示す `# Moved` ファイルは論文要約ではないため対象外とする。移動先の実体ファイルは通常どおり監査する。

## 実行

```bash
python .survey/scripts/audit_paper_quality.py \
  --markdown-out .survey/reports/paper-quality-audit.md \
  --json-out .survey/reports/paper-quality-audit.json \
  --no-fail-exit
```

`--no-fail-exit` を外すと、FAILが1件以上ある場合に終了コード1を返すため、CIの品質ゲートとしても利用できる。

## 既定の機械判定

- UTF-8ファイルサイズ: 4,500 bytes以上
- 説明文: 2,200文字以上
- 説明段落: 10段落以上
- `## 手法` の説明段落: 4段落以上
- `## 手法` 内に主要機構が3個以上ある場合、各主要機構に2段落以上
- 説明文の日本語文字率: 50%以上をFAIL、50〜60%をWARN
- `request`, `placement`, `latency`, `offload`, `cache`, `throughput` など `TERM_RULES` に登録された英語専門語が本文へ裸で出た場合はFAIL

日本語文字率は、ひらがな・カタカナ・漢字の文字数を、日本語文字数と英字数の合計で割る。frontmatter、URL、コード、Markdownリンク先、見出し、表、一次資料、更新履歴などは除外する。正式名称を併記する `日本語（English term）` 形式は用語検査では違反扱いにしない。

日本語率は固有名詞やモデル名の影響を受けるため補助指標であり、用語ルールの主判定は裸の英語専門語検出とする。

## 出力

MarkdownにはFAIL/WARN論文を表で並べ、各論文について未達理由と、裸の英語専門語の出現回数・行番号を記録する。JSONには全論文の測定値を保存するため、後から閾値調整や修整順序の決定に利用できる。

## 閾値調整

既定値は初期の機械監査用であり、意味的な品質基準の正本は常に `.survey/templates/paper.md` とする。必要なら次の引数で変更できる。

```text
--min-bytes
--min-prose-chars
--min-paragraphs
--min-method-paragraphs
--min-component-paragraphs
--min-japanese-ratio
--warn-japanese-ratio
```

英語専門語の検出対象を増減する場合は、`audit_paper_quality.py` の `TERM_RULES` を更新する。モデル名、フレームワーク名、略語、単位、URLは原則として対象外とする。
