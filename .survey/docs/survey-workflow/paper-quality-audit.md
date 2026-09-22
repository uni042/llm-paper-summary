# Paper mechanical quality audit

`.survey/scripts/audit_paper_quality.py` は `papers/inference/**/*.md` を全件走査し、`.survey/templates/paper.md` のうち機械判定できる品質条件を一覧化する。

監査対象の判定はfrontmatterや`canonical_id`の正常性に依存させない。カテゴリ索引の`README.md`、横断比較表`comparison.md`、正規の移動先だけを示す`# Moved`ファイルだけを除外する。

この品質監査には、本文量・日本語率だけでなく、**一覧の一文解説が「何をした論文か」を失っていないか**、**単体ページの概要だけで代表結果が分かるか**も含める。

## 実行

```bash
mkdir -p audit-output
python .survey/scripts/audit_paper_quality.py \
  --markdown-out audit-output/paper-quality-audit.md \
  --json-out audit-output/paper-quality-audit.json \
  --no-fail-exit

python .survey/scripts/audit_list_summary_quality.py \
  --markdown-out audit-output/list-summary-quality-audit.md \
  --json-out audit-output/list-summary-quality-audit.json \
  --no-fail-exit

python .survey/scripts/audit_overview_results.py \
  --markdown-out audit-output/overview-result-quality-audit.md \
  --json-out audit-output/overview-result-quality-audit.json \
  --no-fail-exit
```

GitHub Actionsの `.github/workflows/paper-quality-audit.yml` も同じ監査を行い、結果はrepositoryへ固定保存せず7日間のworkflow artifactとして保持する。

## 品質基準の固定

論文品質の機械基準は、2026-09-12から2026-09-21の間に安定運用されていた `.survey/scripts/audit_paper_quality.py` の基準を固定基準とする。具体的には、UTF-8 4,500 bytes、説明文2,200文字、説明10段落、手法4段落、主要機構が3個以上ある場合は各2段落、日本語比率70%未満FAIL・80%未満WARN、裸の英語専門語0件、既存の構造化手法相当判定を維持する。品質計測の閾値・説明量・手法要件は当時の基準を固定する。例外として、`書誌情報` の著者名・所属などの英語メタデータが本文品質へ混入する挙動は誤計測バグとして扱い、品質計測から除外する。既存の一次資料、参考文献、References、更新履歴、監査メモの除外と合わせ、このバグ修正だけは固定基準に含める。

この固定基準は、repository-wide監査、`paper_quality_gate.py` を使うsubmission processor、`research_quality_preflight.py` の提出前preflightで共通利用する。提出前preflightは独自の機械閾値を持たず、同じ `audit_paper_quality.py` の既定値をそのまま使う。セルフレビューやexact blob照合は提出前に同じ品質を確認するための手順であり、新しい品質閾値を追加するものではない。

今後、品質基準そのものを自動的に強化・緩和・追加・削除しない。変更してよいのは、今回の`書誌情報`除外のような想定外挙動、解析バグ、移行・互換バグを直し、**本文品質に対する要求水準を変えない場合だけ**とする。基準変更が必要に見える場合は実装せず報告し、ユーザーの明示指示を待つ。

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

日本語文字率はfrontmatter、URL、コード、Markdownリンク先、見出し、表、書誌情報、一次資料、更新履歴などを除外して計算する。固有名詞やモデル名の影響を受けるため補助指標とし、用語規則は裸の英語専門語検出を主判定とする。

## 一文解説はワーカーが生成する

一覧の一文解説は、概要の自動短縮ではなく、**論文を精読したresearch workerが一覧専用に生成する独立成果物**とする。

workflow v10の構造化研究レコードでは `metadata.list_summary` に保存する。rendererはこれをタイトル直下の引用文 `> ...` とfrontmatterへそのまま出力する。新規レコードで `metadata.list_summary` が欠けている場合、rendererは公開処理を失敗させる。

一文解説の要件は次の通り。

1. 45〜180文字程度の一文とする。
2. 論文名や方式名を言い換えただけで終わらない。
3. 「何が問題か」だけで終わらず、**この論文が具体的に何をしたか**を必ず書く。
4. 手法論文なら、何を観測・予測・配置・移動・削減・切り替え・設計する方式なのかが分かるようにする。
5. サーベイ・分析・ベンチマーク論文なら、何を比較・整理・測定・分析して、何を明らかにしたのかを書く。
6. 代表結果を短く入れると理解が大きく改善する場合は結果も含めてよいが、詳細な数値は`## 概要`を優先する。
7. 論文未読者がその一文だけ読んでも、その論文の主な貢献を区別できることを最終基準とする。

`.survey/scripts/list_summary.py` は、タイトル直下のワーカー生成文を最優先で使用する。まだ専用短文を持たない既存論文に限り、`## 概要`から意味的に圧縮する旧互換フォールバックを使う。このフォールバックは移行用であり、新規論文の正規生成経路には使わない。

## 概要に代表結果を必ず含める

単体ページの`## 概要`は、背景・提案内容だけでなく、**その論文を読んだとき最初に覚えるべき代表結果を少なくとも1つ**含める。

優先順位は次の通り。

1. 論文のabstract、結論、主要結果節などで最も強くアピールしている定量結果。
2. それが明確でない場合、論文中で最も象徴的な定量結果。
3. サーベイ、分析研究、定量値が主役でない研究では、最も重要な定性的発見。

数値だけを置かず、**何の指標が、どの条件で、何と比べて、どう変わったか**を同じ文で分かるようにする。カーネル単体値とエンドツーエンド値、シミュレーションと実機値などは混同しない。

`.survey/scripts/audit_overview_results.py` は`## 概要`だけを抜き出し、代表結果の存在を監査する。既存ページの修整期間中はGitHub Actionsから`--no-fail-exit`でレポートのみ生成する。全既存ページの差し替えが完了して基準未達が0件になった後は、この監査を必須チェックへ昇格できる。

## 構造化研究レコードからの再発防止

workflow v10の研究レコードは `results.overview` と `results.key_results` を保持する。Markdown rendererはこれらを捨てず、単体ページの`## 概要`へ代表結果を反映する。

`results.key_results`を書くときは、**先頭要素をその論文の代表結果（headline result）として扱う**。複数の数値がある場合、単に論文中で最初に出た数値ではなく、abstract・結論・主要評価で最も強く主張されている結果を先頭に置く。`results.overview`には、その数値の実用上の意味と、条件によって利得が変わる理由を短くまとめる。

`metadata.summary` は単体ページの説明材料、`metadata.list_summary` は一覧専用短文として役割を分離する。長いsummaryを機械的に切ってlist summaryへ代用しない。

## 公開前セルフチェックとexact blob preflight

Research / Auditの新規completed publicationは、submission processorへ渡す前に2段階の提出前検査を必須とする。

1. **ワーカー自身の意味品質セルフレビュー**: 一次資料との整合、推測の混入、概要・一覧文の固有性、代表結果、end-to-end手法、評価条件・baseline、結果の条件と解釈、限界・既存研究との差を5スロット上で読み返す。不十分な項目はrecord bankへ確定保存する前に直す。
2. **exact blob preflight**: セルフレビュー済み5スロットをrecord bankへ保存した後、`.survey/work-queue/research-preflight/requests/` から `research_quality_preflight.py` を実行する。ここでは `assemble_research_record.py` の構造化validation、正規renderer、`paper_quality_gate.py` の機械品質基準をsubmission processorと同じ順で適用する。

preflightがFAILならcompleted-submission requestは作らない。resultの全指摘をslotへ戻して修正し、新しいpreflight requestで再検査する。PASS/WARNで `preflight_passed=true` になったresultだけをcompleted requestの `preflight_result` から参照できる。

合格resultには、その時点のvalidated descriptor全体のSHA-256 fingerprintと5スロットのGit blob SHAを保存する。completed descriptor builderは現在のdescriptorを再構築してfingerprintを照合するため、**preflight合格後に1文字でもslotが変われば古い合格resultは使えない**。この場合は再preflightが必要になる。

submission processor側のquality gateは削除せず、防御的な二重検査として残す。通常運用では品質不足をsubmission failureにしてからrepairするのではなく、提出前preflightで修正してから公開へ進める。

## 回帰試験

```bash
python -m unittest discover -s .survey/tests -p 'test_*quality.py'
python -m unittest discover -s .survey/tests -p 'test_render_paper_metadata.py'
```

意味的な品質基準の正本は常に `.survey/templates/paper.md` と本運用文書。上記の固定基準は、想定外挙動・解析バグ・移行/互換バグの修正、またはユーザーの明示指示がある場合を除いて変更しない。バグ修正時も基準の意味を変えず、repository-wide監査・提出前preflight・submission processorの3経路が同じ基準を使うことを既存回帰試験で確認する。
