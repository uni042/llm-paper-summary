---
canonical_id: arXiv:2403.09636
arxiv_id: '2403.09636'
doi: 10.48550/arxiv.2403.09636
last_audited: '2026-10-08'
audit_version: 2
title: 'Dynamic Memory Compression: Retrofitting LLMs for Accelerated Inference'
summary: 自己回帰推論で系列長・バッチサイズに比例して膨張するキー・値キャッシュを、各注意ヘッドが新しいKVを「追加するか直前エントリへ重み付き結合するか」オンライン判断する動的メモリ圧縮（Dynamic Memory Compression; DMC）へ置き換える。既存Llama 2を追加パラメータなしの短い継続事前学習で改造し、4倍圧縮までは下流性能をほぼ維持しながら、公開ICML版ではA100/H100上で約3.4〜3.7倍、更新版では高圧縮条件で最大7倍の生成スループット向上を報告する。
list_summary: 各注意ヘッドがKVを追加・結合するかを入力依存で学習するDMCをLlama 2へ後付けし、4倍KV圧縮まで品質をほぼ維持しつつ実機生成スループットを数倍に高める。
published: 2024-03-14
publication: ICML 2024
publication_type: conference
publication_status: Published
lineage: inference-systems
topics:
- LLM推論
- KVキャッシュ圧縮
- 動的圧縮
importance: Researchワークリストから精読
hardware_evaluation: Llama 2 7B/13B/70B、NVIDIA A100/H100で品質・KV圧縮率・最大バッチ・自己回帰生成スループットを評価
source: https://arxiv.org/abs/2403.09636
sources:
- https://arxiv.org/abs/2403.09636
- https://proceedings.mlr.press/v235/nawrot24a.html
implementation: 既存Llama 2を少量の継続事前学習でDMC化する。各ヘッドでKVの追加/直前要素への重み付き結合を学習し、推論時は標準KVキャッシュの代わりに可変長の圧縮キャッシュを保持する。公式実装・モデルはNVIDIA Megatron-LM内で公開。
arxiv_categories:
  primary: cs.CL
  cross_list: []
last_checked: 2026-09-28
authors:
- Nawrot, Piotr
- Łańcucki, Adrian
- Chochowski, Marcin
- Tarjan, David
- Ponti, Edoardo M.
code: https://github.com/NVIDIA/Megatron-LM/tree/DMC
implementation_status: official-code-available
references:
- canonical_id: arXiv:2305.13245
  doi: 10.18653/v1/2023.emnlp-main.298
- canonical_id: arXiv:2305.15805
- canonical_id: arXiv:1409.0473
  arxiv_id: '1409.0473'
- canonical_id: arXiv:2004.05150
  arxiv_id: '2004.05150'
- canonical_id: DOI:10.1609/aaai.v34i05.6239
  doi: 10.1609/aaai.v34i05.6239
- canonical_id: OpenReview:JroZRaRw7Eu
  openreview_id: JroZRaRw7Eu
- canonical_id: arXiv:1904.10509
- canonical_id: OpenReview:Ua6zuk0WRH
  openreview_id: Ua6zuk0WRH
- canonical_id: DOI:10.18653/v1/n19-1300
  doi: 10.18653/v1/n19-1300
- canonical_id: arXiv:2205.14135
- canonical_id: DOI:10.48550/arxiv.2405.04434
- canonical_id: OpenReview:COZDy0WYGg
  openreview_id: COZDy0WYGg
- canonical_id: arXiv:2310.01801
- canonical_id: arXiv:2312.00752
- canonical_id: OpenReview:d7KBjmI3GmQ
  openreview_id: d7KBjmI3GmQ
- canonical_id: OpenReview:rygGQyrFvH
  openreview_id: rygGQyrFvH
- canonical_id: arXiv:2401.18079
- canonical_id: DOI:10.1145/3600006.3613165
  doi: 10.1145/3600006.3613165
- canonical_id: OpenReview:Hyg0vbWC-
  openreview_id: Hyg0vbWC-
- canonical_id: arXiv:2305.17118
- canonical_id: arXiv:2402.02750
- canonical_id: arXiv:2304.08467
- canonical_id: DOI:10.1145/3458817.3476209
  doi: 10.1145/3458817.3476209
- canonical_id: arXiv:2211.05102
  doi: 10.48550/arxiv.2211.05102
- canonical_id: OpenReview:SylKikSYDH
  openreview_id: SylKikSYDH
- canonical_id: DOI:10.1609/aaai.v34i05.6399
  doi: 10.1609/aaai.v34i05.6399
- canonical_id: arXiv:1911.02150
  arxiv_id: '1911.02150'
- canonical_id: arXiv:2307.09288
  arxiv_id: '2307.09288'
- canonical_id: arXiv:2012.09852
  doi: 10.1109/hpca51647.2021.00018
- canonical_id: arXiv:2306.14048
references_checked_at: '2026-10-03'
references_source: arxiv-html-reference-section
references_total: 42
under16kb_reaudit_target_path: papers/inference/07-kv-cache-optimization-compression/2024-2403.09636-dynamic-memory-compression-retrofitting-llms-for-accelerated-inference.md
under16kb_reaudit_source_git_blob_sha: 'b8892625d32eebbe7cb45b1bd8af3deb9eaf0e81'
under16kb_reaudit_version: '2026-10-07-v1'
under16kb_reaudit_passed: true
quality_self_review_passed: true
quality_self_review_version: '2026-10-07-v1'
worker_run_key: 'interactive-20261008-bottom-up-reaudit-dmc'
worker_completed_at: '2026-10-08T07:32:15+09:00'

---

# Dynamic Memory Compression: Retrofitting LLMs for Accelerated Inference

> 動的メモリ圧縮（Dynamic Memory Compression; DMC）は、過去トークンを「残す／捨てる」の二択にせず、各注意ヘッドが新しいキー・値（Key-Value; KV）を新規スロットへ追加するか、直前のスロットへ重み付きで結合するかを学習する。これにより、内容・層・ヘッドごとに必要な時間解像度を変えながらKVキャッシュをオンライン圧縮する。

## 概要

Transformerの自己回帰生成では、一度計算した過去トークンのキーと値をKVキャッシュへ保存し、次トークンの注意計算で再利用する。再計算を避けられる反面、キャッシュ容量は系列長と同時処理要求数に比例する。長文脈や大バッチでは重みよりKVが高帯域メモリ（High Bandwidth Memory; HBM）を圧迫し、バッチを増やせないためGPUの行列演算器を十分に埋められない。

既存の追い出し方式は「重要でない過去KVを削除する」ため、後でその情報が必要になっても取り戻せない。グループ化クエリ注意（Grouped-Query Attention; GQA）はKVヘッド数を固定比率で減らすので実装しやすいが、全層・全入力へ同じ圧縮構造を課す。DMCはここを、**トークンごと・ヘッドごと・層ごとの学習済み結合判断**に変える。

Llama 2 7B/13B/70Bを短い継続事前学習でDMC化し、追加パラメータを増やさずに圧縮挙動を獲得する。4倍圧縮までは元モデルに近い下流性能を保ち、H2O/TOVAのような追い出し方式や学習済みGQAより高圧縮域で品質を保ちやすい。圧縮によって同じGPUメモリへより大きなバッチを載せられるため、自己回帰生成の実スループットも上がる。

## 背景と問題設定

### KVキャッシュ容量は「1要求の長さ」と「同時要求数」の積で増える

デコードでは各新トークンのクエリが過去KVを読む。全履歴を残せば品質面では安全だが、要求が長くなるほどキャッシュが増える。配信ではさらにバッチ数が掛かるため、HBM容量不足によってバッチ拡大が止まり、計算能力が余っていてもスループットが頭打ちになる。

単純なKV追い出しは容量を直接減らせるが、一度削除したトークンは後続注意から完全に消える。これは「大半の過去情報を後で再利用する」課題で不利になる。DMCの着眼点は、複数トークンの情報を一つのKVスロットへ**統合して残す**ことである。

### 必要な圧縮率はヘッド・層で同じではない

局所パターンを見るヘッド、長距離依存を保持するヘッド、上位層で抽象化された意味表現を扱うヘッドでは、連続するトークンを同じ粒度で保存する必要はない。DMCはグローバルな目標圧縮率だけを与え、実際にどのヘッド・どの位置で結合するかはモデルに学習させる。

## 手法

### 1. 各時刻で「追加」か「直前KVへの結合」かを決める

各注意ヘッドは新しいトークン (t) のKVを得たとき、判断変数 (alpha_t) により二つの動作を選ぶ。

- **追加**: 新しいKVを独立したキャッシュ要素として末尾に追加する。
- **結合**: 新しいKVを直前のキャッシュ要素へ重み付き平均で取り込み、キャッシュ長を増やさない。

結合時には重要度重み (omega_t) を使い、以前の累積重みと現在トークンの寄与を合わせる。したがって単純な「最後のKVで上書き」ではなく、複数トークンの情報を一つの代表KVへ蓄積する。

### 2. 追加パラメータを増やさず既存のクエリ・キー成分を判断に使う

DMCは別のルータネットワークを追加せず、既存のクエリ（query）とキー（key）の成分から追加/結合の判断と重みを作る。これによりモデルサイズを増やさず、通常の注意計算と同じ層内で圧縮判断を実行できる。

重要なのは、圧縮率が固定ではない点である。同じ4倍という全体目標でも、ある層・ヘッドは細かく残し、別のヘッドは長い区間をまとめる。論文の解析では、学習が進むにつれて高層から圧縮が始まり、目標圧縮率を上げると低層にも圧縮が広がる。

### 3. 離散判断を継続事前学習で獲得する

「追加する／結合する」は離散判断なので、そのままでは勾配で学習しにくい。学習中はガンベル・シグモイド（Gumbel-Sigmoid）による連続緩和を使い、言語モデリング損失に目標圧縮率へ近づける圧縮損失を加える。

開始時はほぼ通常KVキャッシュとして動かし、学習の進行とともに目標圧縮率を1倍から2倍、4倍などへ徐々に上げる。この「元モデルの挙動から連続的に圧縮モデルへ移す」手順により、既存Llama 2をゼロから学習し直さずDMCへ改造する。

著者らの公開説明では、目標圧縮率に応じて元の事前学習データ量の約2〜8%を使う。完全な学習し直しより軽いが、推論時だけ差し込める訓練不要手法ではない。

### 4. 推論時は圧縮済みKVだけを後続トークンへ渡す

学習後は各トークンで追加/結合を決め、圧縮された可変長キャッシュを更新する。後続注意はこの圧縮キャッシュだけを読むため、論理的な「圧縮率」が実際のHBM使用量と読み出し量へつながる。

圧縮で空いたHBMへバッチを増やせると、デコード時の小さな行列演算をまとめて実行でき、GPU利用率が上がる。DMCの大きなスループット利得は、1要求あたりの注意だけを高速化した結果ではなく、**メモリ節約 → 最大バッチ拡大 → GPU利用率向上**まで含む効果である。

## 評価

### 代表的な評価条件

| 項目 | 条件 |
|---|---|
| モデル | Llama 2 7B / 13B / 70B |
| 圧縮率 | 主に2倍・4倍、更新版では6倍・8倍も評価 |
| 品質 | 常識QA、MMLU、HumanEvalなど |
| 比較対象 | 元Llama 2、学習済みGQA、H2O、TOVA |
| 実機 | NVIDIA A100 / H100 |
| 性能指標 | KV容量、最大バッチサイズ、自己回帰生成スループット |
| 学習 | 元モデルからの継続事前学習。追加パラメータなし |
| 併用 | GQAとDMCを重ね、圧縮率を乗算する構成も評価 |

### 代表的な評価結果

| 条件・指標 | 結果 | 解釈 |
|---|---:|---|
| DMC 4倍 | 元モデルに近い下流性能を維持 | 4分の1規模のKVでも主要品質を保てる範囲を確認 |
| DMC 4倍、7B/13B | A100/H100で生成スループットが約 **3.4〜3.7倍** | KV削減でより大きなバッチを載せられる効果が実時間へ反映 |
| 高圧縮条件（更新版） | H100で最大 **7倍**のスループット向上を報告 | 最大値は高い圧縮率とメモリ制約下のバッチ拡大を含む |
| DMC対H2O/TOVA | 高圧縮率で品質劣化が小さい | 削除ではなく学習した結合で情報を残す利点 |
| GQA + DMC | 例: 既に8倍GQA相当のLlama 2 70BへDMC 2倍を重ね、合計16倍相当 | KVヘッド共有と時間方向の結合は独立軸として併用可能 |
| 圧縮分布 | 上位層ほど強く圧縮する傾向、絶対位置への固定依存は小さい | 一律周期ではなく層・内容依存の圧縮を学習している |

公開ICML 2024版の要旨は4倍DMCで約3.7倍の最大スループットを中心に報告している。一方、後の更新版・NVIDIA公開説明では8倍圧縮まで広げ、H100で最大7倍を報告する。したがって「DMCは常に7倍速い」とまとめるのは不正確で、圧縮率・モデル・GPU・最大バッチ条件を併記する必要がある。

### 公開版の倍率差と学習コスト（再監査補足）

DMCは、キー・値キャッシュの各トークンを単純に破棄する方式とは異なる。モデルは新しいトークンの状態を保存するか、それまでの記憶と重み付きで結合するかを学習し、層や注意ヘッドによって圧縮率を変える。したがって一度だけ使われる重要な情報は保持し、冗長な系列の状態は少ないメモリにまとめるという適応が可能である。一方、この判断を既存の事前学習済みモデルへ持ち込むには継続事前学習を必要とし、事前準備が不要な削除型キャッシュ管理とは比較条件が異なる。

数値の版差が重要である。ICML 2024で公開された正式採録版は、Llama 2の七十億・百三十億・七百億級を対象とし、最大四倍のキャッシュ圧縮で下流性能を維持しながら、H100で最大約三・七倍の生成スループット向上を報告する。後の更新稿ではより高い圧縮率を試し、最大七倍の処理量改善を掲げている。七倍は正式採録版の四倍圧縮・三・七倍改善と同一の設定ではない。圧縮率や同時処理数が大きくなれば、メモリ容量の利得が高速化として出やすいが、利用できるGPUメモリに十分余裕がある小バッチでは効果が縮む。

継続学習の規模も「追加パラメータがゼロ」という点だけでは評価できない。著者の分析では、二倍の圧縮へ適応させる際に元の事前学習データの約二％、四倍では約四％を使う設定がある。モデルの重みを一切更新せずその場で圧縮できる方式ではなく、小さいとはいえ継続学習の計算費が存在する。また既存のグループ化クエリ注意と時間方向の圧縮を併用する場合、両者は異なる冗長性を削るため、元から共有したヘッド数と時間方向の削減率を明示する必要がある。最終モデルの品質は常識推論、MMLU、コード生成で測定し、処理量改善と混同しない。

## 既存研究との差

GQAはKVヘッド数をアーキテクチャとして固定的に減らす。H2OやTOVAはキャッシュ上の一部トークンを追い出す。DMCは**時間方向に隣接するKVを学習して結合**し、圧縮位置と圧縮率をヘッド・層ごとに変える。

さらにGQAとは排他的ではない。GQAが「ヘッド方向」、DMCが主に「系列方向」を圧縮するため、両者を組み合わせて容量削減を重ねられる。この点は単一の置換方式より配備設計上重要である。

## 限界・実装状況

DMCは訓練不要のキャッシュ管理ではなく、既存モデルを継続事前学習する必要がある。元モデルの学習データまたは近い分布のデータを用意できない場合、同じ品質維持を期待できるとは限らない。

また、結合は情報を不可逆に圧縮する。4倍までは主要評価で品質を保つが、さらに圧縮率を上げるとタスク依存の劣化が現れる。長文検索や非常に細かな位置情報を必要とする課題で、同じ動作点が最適とは限らない。

性能倍率もHBM容量制約に強く依存する。既に小バッチで計算律速になっている条件では、KVを減らしても最大バッチを増やす必要がなく、3〜7倍級のスループット向上にはつながらない。

公式実装とモデルはNVIDIA Megatron-LMのDMCブランチで公開されている。したがって論文はアルゴリズム提案だけでなく、既存大規模モデルを実際に改造して実機性能まで測定した研究である。

## 一次資料

- arXiv: https://arxiv.org/abs/2403.09636
- ICML 2024: https://proceedings.mlr.press/v235/nawrot24a.html
- 公式実装: https://github.com/NVIDIA/Megatron-LM/tree/DMC

## 修整履歴

- 2026-09-28（修整済み）: 現行品質ガイドに合わせ、汎用的な推論最適化テンプレート文を削除。KVの追加/重み付き結合、ヘッド・層ごとの動的圧縮、ガンベル・シグモイドによる継続事前学習、圧縮から最大バッチ拡大へ至る因果関係を具体化し、Llama 2 7B/13B/70B、A100/H100、4倍圧縮で約3.4〜3.7倍、更新版高圧縮条件で最大7倍、GQA併用を評価表へ整理した。

- 2026-10-08: 再監査として採録版/原著の比較条件と評価解釈、適用限界を追記した。
