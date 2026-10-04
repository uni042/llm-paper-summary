---
canonical_id: "DOI:10.1145/3620665.3640366"
arxiv_id: null
doi: "10.1145/3620665.3640366"
openreview_id: null
arxiv_categories:
  primary: null
  cross_list: []
last_audited: null
audit_version: 0
storage_targets:
  - "papers/inference/99-other-inference-systems/2024-d5ec11366816-pytorch-2-faster-machine-learning-through-dynamic-python-bytecode-transformation-and-graph-compilation.md"
bottlenecks:
  - Python実行とカーネル起動のオーバーヘッド
  - 演算をまたぐメモリ転送
hardware_details: "評価はNVIDIA A100 GPUとIntel Xeon 8275CL CPU。別途TorchDynamo捕捉オーバーヘッドをNVIDIA V100 GPUで測定。"
quality_effect: "数値的に等価なコンパイル実行を意図する。精度品質のベンチマークではなく、実行速度とモデル捕捉範囲を評価。"
evidence_locations:
  - "Abstract; Sections 1, 3-6; Tables 1-4; Artifact Appendix A"
references:
  - {arxiv_id: "1903.01855"}
  - {arxiv_id: "1605.02688"}
  - {doi: "10.1145/2628071.2628092"}
  - {arxiv_id: "2207.04296"}
  - {arxiv_id: "1410.0759"}
  - {doi: "10.1145/3315508.3329973"}
  - {arxiv_id: "2102.13267"}
  - {arxiv_id: "2205.13603"}
  - {doi: "10.1145/3079856.3080246"}
  - {doi: "10.1145/2939672.2945397"}
  - {doi: "10.1080/00401706.1962.10490022"}

  - {doi: "10.1109/CGO51591.2021.9370308"}
  - {arxiv_id: "1802.04730"}
references_checked_at: "2026-10-04"
references_source: "Primary paper, References section, pp. 16-18"
references_total: 60
title: "PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation"
summary: "PyTorchの即時実行はPythonの柔軟性を保つ一方、演算単位の実行では複数演算をまたぐ融合やスケジューリングを適用しにくい。本論文は、実行直前にPythonバイトコードを解析してPyTorch演算列をFXグラフとして取り出すTorchDynamoと、そのグラフをGPU向けTritonまたはCPU向けC++へ変換するTorchInductorを示す。Pythonへ戻るグラフ分割を許すため既存プログラムの挙動や動的制御を保ちやすく、コンパイラを使えない処理も実行できる。NVIDIA A100上の180超の実モデル群を含む評価で、TorchInductorはPyTorch即時実行に対し推論で幾何平均2.27倍、学習で1.41倍の高速化を報告し、六つの他バックエンドと比較された。"
list_summary: "Pythonの柔軟な即時実行を維持したまま、実行時に演算グラフを捕捉してTritonやC++へコンパイルするPyTorch 2の仕組みを示し、実モデルの推論・学習で速度と捕捉範囲を比較する。"
authors:
  - "Jason Ansel"
  - "Edward Yang"
  - "Horace He"
  - "Natalia Gimelshein"
  - "Animesh Jain"
  - "Michael Voznesensky"
  - "Bin Bao"
  - "Peter Bell"
  - "David Berard"
  - "Evgeni Burovski"
  - "Geeta Chauhan"
  - "Anjali Chourdia"
  - "Will Constable"
  - "Alban Desmaison"
  - "Zachary DeVito"
  - "Elias Ellison"
  - "Will Feng"
  - "Jiong Gong"
  - "Michael Gschwind"
  - "Brian Hirsh"
  - "Sherlock Huang"
  - "Kshiteej Kalambarkar"
  - "Laurent Kirsch"
  - "Michael Lazos"
  - "Mario Lezcano"
  - "Yanbo Liang"
  - "Jason Liang"
  - "Yinghai Lu"
  - "CK Luk"
  - "Bert Maher"
  - "Yunjie Pan"
  - "Christian Puhrsch"
  - "Matthias Reso"
  - "Mark Saroufim"
  - "Marcos Yukio Siraichi"
  - "Helen Suk"
  - "Michael Suo"
  - "Phil Tillet"
  - "Eikan Wang"
  - "Xiaodong Wang"
  - "William Wen"
  - "Shunting Zhang"
  - "Xu Zhao"
  - "Keren Zhou"
  - "Richard Zou"
  - "Ajit Mathews"
  - "Gregory Chanan"
  - "Peng Wu"
  - "Soumith Chintala"
authors_affiliations: "Meta、OpenAI、Quansight、Intel、University of Michigan。"
published: "2024-04"
publication: "Proceedings of the 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 2 (ASPLOS '24), pp. 929-947"
publication_type: "会議論文"
publication_status: "査読済み・会議採録"
lineage: "PyTorch 2 torch.compileの設計と評価を報告する論文。"
topics:
  - "LLM推論"
  - "Transformer推論"
  - "機械学習コンパイラ"
  - "演算融合"
importance: "柔軟なPythonプログラムを部分グラフ単位でコンパイルし、推論性能を高める実運用フレームワークの実装・広範評価を提示する。"
hardware_evaluation: "NVIDIA A100 GPUでTorchBench、HuggingFace、TIMMの実モデルを評価。CPU評価にはIntel Xeon 8275CLを使用。捕捉コスト比較はNVIDIA V100で実施。"
source: "https://doi.org/10.1145/3620665.3640366"
sources:
  - "https://pytorch.org/assets/pytorch2-2.pdf"
code: "https://github.com/pytorch/pytorch"
implementation: "torch.compileはPyTorch 2に収録。TorchDynamoがPythonフレーム評価フックでバイトコードを解析し、TorchInductorがGPUではTriton、CPUではC++/OpenMPを生成する。"
last_checked: "2026-10-04"
worker_completed_at: "2026-10-04T15:19:36+09:00"
worker_run_key: "20261004-1830-codex-local-r19"
---

# PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation

> Pythonの即時実行の柔軟性を残して演算グラフを実行時に取り出し、TritonやC++へコンパイルする仕組みを設計・評価した。

## 概要

PyTorchの即時実行では、Pythonコードが演算を一つずつ呼び出すため、隣接演算をまとめる融合や全体を見たスケジューリングが難しい。一方、プログラム全体を固定グラフに変換する従来方式は、Pythonの分岐、データ構造、外部ライブラリを扱いにくく、モデルによっては未対応処理で失敗する。本論文は、実行直前のPythonバイトコードを解析してPyTorch演算列を抽出するTorchDynamoと、抽出したグラフをGPUまたはCPU向けコードへ変換するTorchInductorをPyTorch 2へ導入した。

実機評価では、NVIDIA A100上でTorchBench、HuggingFace、TIMMから180超の実モデルを用い、CPUとGPU、推論と学習、複数の精度設定を比較した。論文の要約値では即時実行に対する推論の幾何平均高速化は2.27倍、学習は1.41倍で、六つの他コンパイラを上回った。個別条件を見ると、A100上のHuggingFace float16推論45モデルでは1.91倍である。したがって2.27倍は全体の要約値であり、各LLMや各サービスが同じ倍率で速くなることを意味しない。

## 書誌情報

- 著者: Jason Ansel, Edward Yang, Horace He, Natalia Gimelshein, Animesh Jain, Michael Voznesensky, Bin Bao, Peter Bell, David Berard, Evgeni Burovski, Geeta Chauhan, Anjali Chourdia, Will Constable, Alban Desmaison, Zachary DeVito, Elias Ellison, Will Feng, Jiong Gong, Michael Gschwind, Brian Hirsh, Sherlock Huang, Kshiteej Kalambarkar, Laurent Kirsch, Michael Lazos, Mario Lezcano, Yanbo Liang, Jason Liang, Yinghai Lu, CK Luk, Bert Maher, Yunjie Pan, Christian Puhrsch, Matthias Reso, Mark Saroufim, Marcos Yukio Siraichi, Helen Suk, Michael Suo, Phil Tillet, Eikan Wang, Xiaodong Wang, William Wen, Shunting Zhang, Xu Zhao, Keren Zhou, Richard Zou, Ajit Mathews, Gregory Chanan, Peng Wu, Soumith Chintala
- 公開: ASPLOS '24、2024年4月27日〜5月1日、La Jolla
- DOI: [10.1145/3620665.3640366](https://doi.org/10.1145/3620665.3640366)
- 実装: [PyTorch](https://github.com/pytorch/pytorch)に含まれる`torch.compile`

## 問題設定

即時実行は、通常のPythonとしてモデルを書き、標準的なデバッグ手段を使える。その反面、実行系が一度に見る範囲は個々の演算に狭まり、複数演算をまたいだ融合などの最適化を適用しづらい。固定グラフを事前に作る方法では、Pythonの任意の制御フロー、辞書やリスト、独自クラス、NumPy呼出し、例外などをすべてグラフへ写す必要があり、書き方を制限する。

推論では、演算ごとのカーネル起動や中間テンソルの読み書きが、特に小さな演算の連なりで無駄になる。コンパイラが複数演算をまとめればその転送を減らせるが、全コードをグラフ化する前提では、グラフ表現できない処理を含む実際のモデルへ適用しにくい。本論文が狙うのは、グラフで表現できる部分だけを最適化し、残りは通常のPython実行へ戻せる境界である。

## 手法のあらまし

TorchDynamoはCPythonのフレーム評価APIを使い、関数が動く直前にバイトコードを読み替える。Tensor演算を見つけると、その演算をFXグラフへ記録し、形状や型などコンパイル時に必要な情報を追跡する。Pythonの値や制御フローについては、実行時に成立する条件をガードとして記録する。グラフ化できない操作に出会った場合はそこでグラフを閉じてPythonへ戻り、後続の演算で新しいグラフを作る。

TorchInductorは受け取ったグラフをループ中心の中間表現へ下げ、演算を並べ替え、インライン化し、融合する。GPU向けにはTriton、CPU向けにはC++/OpenMPを出力し、カーネルを生成する。実行時の入力形状が変わればガード条件を確認し、成立しない場合には再コンパイルなどへ移る。これにより利用者は即時実行のコードを書き続けつつ、対応区間に限ってコンパイル最適化を得られる。

## 手法

### 1. TorchDynamo — 実行直前にPythonのフレームを解析

TorchDynamoはCPythonのフレーム評価フックを利用するため、ソースコード全体を別言語で解析するのではなく、実際に実行されるバイトコードを対象にする。これにより関数呼出し、分岐、クロージャなどPythonの実行意味に沿って処理できる。テンソル演算はグラフノードとして記録し、各値が定数、テンソル、辞書、リスト、ユーザー定義オブジェクトのどれかを追跡する。

グラフの前提となるPython値やテンソル形状が変わる可能性にはガードを付ける。再実行時に条件が同じなら生成済みコードを使い、異なる場合はその特殊化が安全かを再評価する。データ依存の値をPython分岐が読むなど、静的に判断できない場面ではそこでグラフを分ける。完全なグラフ化に失敗したモデルを丸ごと拒否する代わりに、グラフ区間とPython区間を混在させられる。

### 2. TorchInductor — 中間表現から融合カーネルを生成

TorchInductorはFXグラフをループや添字計算を表す中間表現へ変換する。高水準演算をプリミティブな処理へ分解し、データの読み書きや計算の順序を決めた後、近接した点ごとの演算、縮約、scatterなどをまとめる。GPUではTritonコード、CPUではC++/OpenMPコードを生成する。柔軟な中間表現により、新しい演算の低水準化やバックエンド拡張を実装しやすくしている。

大きな速度向上の主因は、複数の小さな演算を一つのカーネルに融合して、中間値のメモリ往復を省くことだった。HuggingFace float16のA100評価では全最適化時の幾何平均が1.91倍で、融合を無効にすると1.68倍、インライン化を無効にすると1.58倍へ下がった。両方を無効にした場合は0.80倍となり、演算分解で生じた小さな処理群を再結合できないと、即時実行より遅くなるケースがある。

### 3. 動的形状とグラフ分割 — 入力変化と未対応処理を扱う

入力形状が毎回異なるモデルでは、静的形状しか扱えないコンパイラは形状の組合せごとに再コンパイルする。本方式は形状を記号として扱い、0や1など特殊値に限って具体値へ特化する方針をとる。実行中に得た制約を使って形状式を簡約し、ガードが不要と分かれば削る。これにより動的入力を許しながら、コンパイル時の形状推論コストを抑える。

テンソル値からPython boolや数値を作り、その値で分岐する処理は実行結果が分かるまでグラフ化できない。TorchDynamoはその境界でグラフを切り、通常のPythonで処理した後に再度捕捉できる。論文の評価では、TorchBenchの多くで単一の全体グラフを取得し、分割が必要な場合も数百演算規模のグラフを保てた。主な分割原因はNumPyなど外部ライブラリ、`.tolist()`のようなPython型変換、データ依存分岐だった。

### 1回の推論で起きる処理

この流れは、Pythonコード全体を前もって固定グラフへ書き換えるものではない。実行中にコンパイル可能なテンソル演算を見つけ、その区間だけを機械語へ変換するので、未対応操作と動的制御を含む既存プログラムにも適用できる。


1. モデル関数のPythonフレームに入るとTorchDynamoがバイトコードを解析する。
2. テンソル演算の入力、演算、出力をFXグラフへ記録し、型や形状の前提にガードを付ける。
3. グラフ外の処理やデータ依存の制御へ達したらグラフを閉じ、該当処理をPythonで実行する。
4. TorchInductorが各グラフをループ中間表現へ変換し、演算の融合・配置・コード生成を行う。
5. GPUまたはCPU向けカーネルを実行し、Python区間と結果をつないでモデル出力を返す。

この仕組みでは、ガード条件が外れたときに別の特殊化やグラフ再取得が必要になり、初回コンパイルの費用も生じる。論文の性能比較はウォームアップを除いた定常状態を測るため、初回起動時間や頻繁な形状変化が多いサービスへの効果は別途測る必要がある。

## 評価

### 結論

TorchDynamoの捕捉は定常状態の即時実行に対して小さな追加コストに収まり、TorchInductorは推論・学習の実モデル群で他のバックエンドより高い幾何平均性能を示した。特にカーネル融合とインライン化が重要で、メモリ往復と細かなカーネル起動を減らす効果が大きい。一方、どのバックエンドもすべてのモデルと設定に対応するわけではなく、性能はモデル、形状、GPU/CPU、精度に依存する。

### 評価環境

| 項目 | 設定 |
|---|---|
| ハードウェア | A100 GPU。別実験の捕捉コストはV100 GPU。CPU評価環境にXeon 8275CLを含む |
| モデル | TorchBench 74件、HuggingFace 45〜46件、TIMM 60〜62件（有効数は設定により差） |
| 実行系 | PyTorch eager、TorchDynamo + TorchInductor、TorchDynamo + 他バックエンド |
| 条件 | 推論・学習、float32・float16、GPU・CPU。表3は動作したモデルのみの幾何平均 |

### 主な性能結果

| 条件 | 比較対象 | 提案手法 | 結果 |
|---|---:|---:|---|
| A100・HuggingFace・float16推論、45モデル | eager 1.00倍 | TorchInductor 1.91倍 | 幾何平均1.91倍 |
| A100・TorchBench・float16推論、74モデル | eager 1.00倍 | TorchInductor 2.59倍 | 幾何平均2.59倍 |
| A100・HuggingFace・float16学習、45モデル | eager 1.00倍 | TorchInductor 1.45倍 | 幾何平均1.45倍 |
| V100・TorchBench・捕捉コスト | eager同一カーネル | TorchDynamo 5% | 即時実行時間の5%未満 |

論文要約の2.27倍（推論）と1.41倍（学習）は180超の実モデルを含む複数スイート・設定をまとめた報告値である。個別スイートでは上表のように差があり、たとえばHuggingFace float16推論は1.91倍だった。A100上のHuggingFace推論で融合とインライン化を両方切ると0.80倍に落ちるため、性能は「コンパイルしたか」だけではなく、バックエンドが演算群を再結合できたかで変わる。

### 評価上の制約

- 大半のモデルは研究・実アプリ由来のベンチマークモデルであり、長時間の本番LLMサービングや複数利用者の待ち行列性能は測定していない。
- 表3の幾何平均は各バックエンドで動作したモデルを対象とする。未対応モデルの取り扱いは比較に影響し、TVM/Hidetなどは多数の構成でモデルを実行できなかった。
- アーティファクト付録はPyTorch 2.1向けの再現手順を記載し、本文中でも後続バージョンで速度と対応範囲が改善したと注記する。環境やCUDA版により細部は変わり得る。

## 既存研究との差

記録再生式の`torch.jit.trace`は実例入力の経路に特化するため、Python制御フローを取り逃して誤った捕捉になることがある。ソース解析方式はPython意味論全体を再現しにくく、遅延評価方式は捕捉待ちと実行の追加コストを持つ。TorchDynamoは実行中のバイトコードと実際のPython意味論を扱い、コンパイラ適用可能な範囲だけをグラフ化するため、従来の全体成功か全体失敗かという二択を緩める。

TorchInductorの独自性は、グラフを受けるだけでなく、Pythonで拡張可能なループ中間表現とTriton/C++出力を組み合わせ、PyTorchの演算分解後に必要な融合を実施した点にある。評価では同じTorchDynamoグラフを六つの別バックエンドへ渡しているため、フロントエンドの捕捉品質とバックエンドの生成性能を分けて比較している。

## 限界・実装状況

- `torch.compile`としてPyTorch 2に公開され、論文のアーティファクト付録はPyTorch本体のベンチマークコードから再現する方法を示す。
- グラフ化にはPython値、形状、演算の扱いに関するガードが必要であり、未対応操作やデータ依存分岐はグラフ分割を招く。
- 速度向上は評価モデルと実行条件に依存する。本論文は推論エンジンのスケジューリング、KVキャッシュ管理、サービング負荷の最適化を提案していない。
- アーティファクト付録は新しいPyTorch版の方が本論文より対応範囲・速度が改善していると記す。論文数値は2024年当時の測定として読む必要がある。

## 一般的な実装上の含意

コンパイラをモデル作成者に新しい静的なプログラミング方式として強制しなくても、実行時に安全な区間を捕捉し、難しい区間を既存ランタイムへ戻せば導入障壁を下げられる。推論時のボトルネックが小演算間のメモリ往復や起動回数なら、融合とインライン化の寄与をアブレーションで確認し、グラフ分割箇所を実ワークロードで調べることが有効である。

## 引用関係

本論文は即時実行フレームワーク、Pythonバイトコード解析、グラフ捕捉、機械学習コンパイラを背景としている。比較対象にはTorchScript、LazyTensor、Torch/XLA、ONNXランタイム、TVM、Hidet、nvFuser、NNCなどを含む。

## 一次資料

- Jason Ansel et al., “PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation,” ASPLOS '24, pp. 929-947, 2024.
- [論文PDF](https://pytorch.org/assets/pytorch2-2.pdf)
- [DOI](https://doi.org/10.1145/3620665.3640366)
