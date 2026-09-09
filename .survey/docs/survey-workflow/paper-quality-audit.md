# Paper mechanical quality audit

`.survey/scripts/audit_paper_quality.py` は `papers/inference/**/*.md` を全件走査し、`.survey/templates/paper.md` のうち機械的に判定できる品質条件を一覧化する。

監査対象の判定は **frontmatter や `canonical_id` の正常性に依存させない**。メタデータが壊れている論文ほど監査対象から消える、という循環的な見逃しを避けるためである。`papers/inference` 配下の Markdown は原則として監査し、カテゴリ索引の `README.md`、横断比較表 `comparison.md`、正規の移動先だけを示す `# Moved` ファイルだけを除外する。`# Moved` は frontmatter が残っていても除外する。

今後、横断比較表など論文要約ではない Markdown を同じディレクトリへ追加する場合は、`canonical_id` の有無で暗黙に除外せず、`is_paper_summary()` に明示的な除外規則と回帰試験を追加する。

## 実行

```bash
python .survey/scripts/audit_paper_quality.py \
  --markdown-out .survey/reports/paper-quality-audit.md \
  --json-out .survey/reports/paper-quality-audit.json \
  --no-fail-exit
```

`--no-fail-exit` を外すと、FAIL が1件以上ある場合に終了コード1を返すため、継続的インテグレーション（CI）の品質ゲートとしても利用できる。

GitHub Actions の `.github/workflows/paper-quality-audit.yml` では、回帰試験を実行した後、`--no-fail-exit` 付きで全件監査を行い、Markdown / JSON の監査結果を7日間の成果物として保存する。論文本文またはチェッカー関連ファイルが更新されると再実行する。

## 既定の機械判定

- UTF-8ファイルサイズ: 4,500 bytes以上
- 説明文: 2,200文字以上
- 説明段落: 10段落以上
- 明示的な手法節の説明段落: 4段落以上
- 明示的な手法節内に主要機構が3個以上ある場合、各主要機構に2段落以上
- 説明文の日本語文字率: `.survey/scripts/japanese_style.py` と同じ既定値を使用
  - 70%未満: FAIL
  - 70〜80%: WARN
- `request`, `placement`, `latency`, `offload`, `cache`, `throughput` など、日本語・カタカナへ置き換えられる英語専門語が本文へ裸で出た場合はFAIL

手法節は現行テンプレートの `## 手法` だけでなく、既存要約で使われている `## 手法のあらまし`、`## 手法：...`、`## 提案手法`、`## 手法1: ...` のような番号付き見出しも同じ節として認識する。見出し名だけが古いという理由で、十分な手法本文を「手法なし」と誤判定しない。

さらに、HeadInferやLMCacheのように、1つの `## 手法` 配下へまとめず、機構ごとに独立したH2で詳しく説明している長文要約もある。この場合は以下をすべて満たす場合に限り **構造化手法相当（structured-equivalent）** と判定し、「手法説明不足」にはしない。

- 説明文4,000文字以上
- 説明段落20段落以上
- 背景・問題・評価・結果・限界・参考資料などを除いた、機構説明になり得るH2が3個以上

このフォールバックは、短い要約を救済するためのものではない。通常の最低説明量より十分に長く、複数の機構別節を持つ文書だけを対象とする。短い要約で明示的な手法節も構造化手法相当もない場合はFAILのままとする。

日本語文字率は、ひらがな・カタカナ・漢字の文字数を、日本語文字数と英字数の合計で割る。frontmatter、URL、コード、Markdownリンク先、見出し、表、一次資料、更新履歴などは除外する。正式名称を併記する `日本語（English term）` 形式は、`japanese_style.py` の共通規則に従って扱う。

日本語率は固有名詞やモデル名の影響を受けるため補助指標であり、用語ルールの主判定は裸の英語専門語検出とする。

## 出力

MarkdownにはFAIL/WARN論文と未達理由を記録する。裸の英語専門語については出現回数・行番号も記録する。JSONには全監査対象の測定値と判定基準を保存するため、後から閾値調整や修整順序の決定に利用できる。

JSONの `schema_version` は4。各論文には `method_detection` として `explicit` / `structured-equivalent` / `missing` を保存し、対象判定規則と構造化手法相当の閾値も `criteria` に記録する。

## 回帰試験

```bash
python -m unittest discover -s .survey/tests -p 'test_audit_paper_quality.py'
```

最低限、次を固定する。

- `README.md` と `comparison.md` は監査しない
- `# Moved` は frontmatter の有無にかかわらず監査しない
- `canonical_id` が欠けた実論文も監査する
- frontmatter 自体がない実論文も監査する
- `## 手法のあらまし`、`## 手法1: ...` など旧・番号付き見出しでも手法段落を正しく数える
- 十分長い機構別H2構成は構造化手法相当として認識する
- 短い要約は構造化手法相当として誤合格させない

## 閾値調整

既定値は機械監査用であり、意味的な品質基準の正本は常に `.survey/templates/paper.md` とする。必要なら次の引数で変更できる。

```text
--min-bytes
--min-prose-chars
--min-paragraphs
--min-method-paragraphs
--min-component-paragraphs
--min-japanese-ratio
--warn-japanese-ratio
```

英語専門語の検出対象や例外を増減する場合は、`.survey/scripts/japanese_style.py` の共通用語規則を更新する。モデル名、フレームワーク名、略語、単位、URLは原則として対象外とする。
