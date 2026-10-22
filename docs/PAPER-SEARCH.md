# 日本語論文解説検索

`build_paper_search.py` は既存の `survey.paper_views()` と citation graph から静的な全体・区分・系統検索を生成する。各HTMLはbuild時のscopeを固定し、family/lineageをURLパラメーターで変更できない。階層リンクとREADMEリンクから全体、推論・学習・サーベイ、個別系統の検索へ移動できる。

## 検索と表示

- タイトル、`summary` / `list_summary` を反映した日本語概要、frontmatterを除いた本文を検索する。HTMLタグ、HTMLコメント、Markdown link destination、bare URLは検索本文から除く。本文はbuild時にNFKCへ正規化し、入力のたびに数千本分の本文全体を再正規化しない。
- NFKCと小文字化を行い、空白区切りの複数語はAND、引用符で囲んだ語句はフレーズとして扱う。引用符内外の各語句もすべて一致する必要がある。
- 空検索はscope内の全件を表示する。おすすめ順は直近12か月内かつリポジトリ内被引用1件以上の注目論文、被引用数、一致回数、公開日、タイトルで安定順にする。引用数順と新しい順も選べる。検索語に一致しない論文はどのsortでも加えない。
- 公開年、注目のみ、実装情報ありのfilterは固定scope内で交差して絞る。「実装情報あり」は公開コードの有無を断定せず、解説に記載された実装・実装情報（未公開コードを含む）がある論文を示す。リポジトリ内被引用は収録論文の `references` から同一repositoryの対象を数えた値で、世界全体の被引用数ではない。
- URL queryには検索語、対象field、年、sort、checkboxを保存する。ページ自身のscopeはqueryから変更できない。
- 画面は一致件数、最大50件ずつの表示、本文一致の短い抜粋とhighlight、系統・公開時期・注目・実装・被引用を表示する。DOMへはtext nodeと`textContent`で出力する。

## BuildとGitHub Pages

通常のrepository rootで `python .survey/scripts/build_paper_search.py --repo-root . --out _site`、または`.survey`をrootにした場合も利用できる。`--site-base` と `--repo-url` で公開URLを変更できる。builderは指定out内のmanifest登録済みfileだけを更新・削除し、outがrepo自身・親・外部の場合は拒否する。

Pages workflowはmainの論文や検索source変更、手動実行、毎日のrefreshで検索をbuildしてdeployする。`GITHUB_TOKEN` によるpaper-import commitではpush workflowが再実行されないため、成功した `Library import processor` の `workflow_run` 完了も更新契機にする。毎日のrefreshは他のbot更新に対するfallbackである。pull requestではartifact buildのみでdeploy jobを実行しない。手動実行を別branchから行った場合もbuildだけで、main以外はdeployしない。

GitHub Pagesは `https://uni042.github.io/llm-paper-summary/` を既定URLとするが、この実装作業はPagesのsource/settingsを変更せず、サイトの公開も行っていない。公開にはrepositoryのPages sourceをGitHub Actionsへ設定する必要がある。

## Payload

各ページはその固定scopeの `papers.json.gz` だけをfetchする。gzip fileが配信側で既に展開された場合はsignatureで検知して再展開を避ける。gzip bytesならブラウザーの `DecompressionStream` で展開する。全体検索は収録全件を含むため初回fetchが最大であり、build結果は全scopeと全体scopeの未圧縮/圧縮byte数を表示する。日本語本文をscopeごとに保存する都合でlineage JSONにも重複があり、サイズは収録本数・本文量に比例する。
