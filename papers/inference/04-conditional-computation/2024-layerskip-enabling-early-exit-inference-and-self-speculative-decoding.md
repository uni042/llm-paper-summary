---
canonical_id: ACL:2024.acl-long.681
arxiv_id: '2404.16710'
doi: 10.18653/v1/2024.acl-long.681
openreview_id: null
arxiv_categories:
  primary: cs.CL
  cross_list:
  - cs.AI
  - cs.LG
last_audited: '2026-09-10'
audit_version: 1
storage_targets: []
bottlenecks: []
hardware_details: null
quality_effect: null
evidence_locations: []
title: 'LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding'
summary: 学習時に途中layerからでもnext-token予測できるようmodelを訓練し、推論時は前半layerだけで数tokenを仮生成して、残りlayerでまとめて検証することで、別draft modelなしのspeculative decodingを行う。
list_summary: 'LayerSkipは同じLLMの前半層を下書き器、後半層を検証器に分け、追加モデルなしで自己投機的デコードを行う。学習で中間層の予測力を高め、検証済み結果だけを採用する。'
authors_affiliations: Meta AIほか（ACL 2024、著者詳細は一次資料参照）
published: '2024-08-12'
publication_status: Published
lineage: Conditional Computation
topics:
- Dynamic depth
- Speculative decoding
- Quality-cost
importance: 中
hardware_evaluation: 実機
source: https://aclanthology.org/2024.acl-long.681/
code: https://github.com/facebookresearch/LayerSkip
implementation: 公式実装・チェックポイントあり（facebookresearch/LayerSkip）
last_checked: '2026-09-11'
authors:
- Mostafa Elhoushi
- Akshat Shrivastava
- Diana Liskovich
- Basil Hosmer
- Bram Wasti
- Liangzhen Lai
- Anas Mahmoud
- Bilge Acun
- Saurabh Agarwal
- Ahmed Roman
- Ahmed A Aly
- Beidi Chen
- Carole-Jean Wu
publication: arXiv
publication_type: preprint
sources:
- https://aclanthology.org/2024.acl-long.681/
implementation_status: official-code-available
references:
- canonical_id: DOI:10.18653/v1/2020.emnlp-main.413
  doi: 10.18653/v1/2020.emnlp-main.413
- canonical_id: arXiv:2307.02628
- canonical_id: OpenReview:SylO2yStDr
  openreview_id: SylO2yStDr
- canonical_id: arXiv:2101.00027
  arxiv_id: '2101.00027'
- canonical_id: DOI:10.18653/v1/2022.emnlp-main.3
  doi: 10.18653/v1/2022.emnlp-main.3
- canonical_id: OpenReview:d7KBjmI3GmQ
  openreview_id: d7KBjmI3GmQ
- canonical_id: DOI:10.18653/v1/d17-1082
  doi: 10.18653/v1/d17-1082
- canonical_id: arXiv:2404.02258
  arxiv_id: '2404.02258'
- canonical_id: arXiv:2310.03003
  arxiv_id: '2310.03003'
  doi: 10.48550/arxiv.2310.03003
- canonical_id: DOI:10.18653/v1/d19-1454
  doi: 10.18653/v1/d19-1454
- canonical_id: OpenReview:uLYc4L3C81A
  openreview_id: uLYc4L3C81A
- canonical_id: DOI:10.1109/isocc53507.2021.9613933
  doi: 10.1109/isocc53507.2021.9613933
- canonical_id: DOI:10.18653/v1/2021.eacl-main.8
  doi: 10.18653/v1/2021.eacl-main.8
- canonical_id: DOI:10.18653/v1/p19-1472
  doi: 10.18653/v1/p19-1472
- canonical_id: arXiv:2311.15436
  arxiv_id: '2311.15436'
references_checked_at: '2026-09-11'
references_source: arxiv-html-reference-section
references_total: 69
---

# 層kip: Enabling Early Exit Inference and Self-Speculative デコード

> LayerSkipは同じLLMの前半層を下書き器、後半層を検証器に分け、追加モデルなしで自己投機的デコードを行う。学習で中間層の予測力を高め、検証済み結果だけを採用する。

## 概要
層kipは、同じLLMの浅い層を**draft modelの代わり**に使い、残り層でそのdraft トークンを検証するself-speculative デコードを成立させる学習レシピである。

前半層を安価な下書き器、後半層を検証器として役割分担させるため、別モデルを用意せずに候補生成と正確な確認を一つのモデル内で行える。

通常のspeculative デコードでは別の小型draft modelを常駐させるため、重み・KV・メモリが追加で必要になる。層kipは同一modelの前半層をdraft、後半層をverifierとして使うので、別modelを持たなくてよい。

ただし既存チェックポイントの中間層は、そのままでは次トークン予測精度が低い。そこで学習時に、**一部層をランダムに飛ばす訓練**と、**途中層からも正解トークンを予測させる損失**を加え、中間層からでも言語モデル出力ヘッドで予測しやすい表現を作る。

H100実機でトークン/sまで測定しており、課題により約1.3〜2.16倍の高速化倍率を示す。単純な層スキップではなく、**浅い予測を後段で検証して誤りを修正するため品質を守りやすい**のが特徴である。

この検証は最終モデルの出力分布に従って下書きトークンを受理するため、単純な早期終了のように浅い層の誤りをそのまま確定させない。下書きが外れた位置では後段層の結果へ戻り、それ以降を改めて生成する。そのため速度は受理率に依存するが、受理されたトークンについては完全モデルで検証済みの経路を使える。層kipの品質保持は『浅い層が常に正しい』ことではなく、『浅い層を安い候補生成器として使い、間違いを後段で検出する』構造から生じる。

## 手法

### 1. 学習中にいろいろな深さのsubmodelを経験させる

学習時、Transformer 層を確率的にスキップする。

後段ほどドロップアウト率を高くすることで、前半層だけでもある程度次トークン予測に使える表現を作れるようにする。

これは推論時の単純な層枝刈りとは違い、**同じ重みを複数の深さで使えるよう事前に慣らす学習**である。

### 2. 中間層から直接next-トークン予測を学習する

各中間層の隠れ状態を、最終層と同じ言語モデル出力ヘッドへ通して交差エントロピー損失を追加する。

終了点ごとに別分類器を持つのではなく、**全終了点が同じ言語モデル出力ヘッドを共有する**。

これにより中間層の表現を語彙logitへ直接読み出しやすくする。

### 3. 前半層だけでdraftし、後半層でまとめて検証する

推論時は終了層 `E` までで数トークンを下書き生成する。

その後、残りの `L-E` 層を使って下書きトークン列をまとめて検証する。

- 下書きが正しい部分 → そのまま受理
- 最初の不一致 → 完全モデル側の予測で修正

という通常の投機的デコードと同じ考え方だが、下書き器と標的モデルが**一つのモデルの前半／後半**に分かれている。

### 4. 重みと前半層のKVを別draft model用に複製しなくてよい

別の下書きモデルを持たないので、前半層の重みを二重に常駐させる必要がない。

また下書き時に作った前半層の活性値/KVを検証でも再利用できる。

同一モデルを使う利点は、重みの共有だけではない。下書き段階で終了層まで計算済みの各トークンについて、検証時は同じ前半層をもう一度通さず、その中間表現から残りの層だけをまとめて実行できる。別の小型下書きモデルを使う方式では下書き側の計算結果を標的モデルの途中状態として直接再利用できないため、この共有計算が層kip固有の速度・メモリ利点になる。

この共有が、外部の下書きモデル方式に対するメモリ上の主な利点になる。

### 5. Exit 層 `E` とdraft トークン数 `d` のバランス

速度を決める主な2パラメータ。

- `E`が浅すぎる → 下書き精度が下がり否認が増える
- `E`が深すぎる → 下書き自体が重くなる
- `d`が短すぎる → まとめて検証する利得が小さい
- `d`が長すぎる → 途中で否認された時の無駄計算が増える

最適点は単なる「浅いほど速い」ではなく、下書き受理率とのバランスで決まる。

例えば終了層を浅くすると1個の下書きトークンを作る費用は小さくなるが、後段層で否認される割合が増えれば、まとめて作った後続下書きも無駄になる。逆に終了層を深くすると受理率は上がるが、下書き生成そのものが完全モデルに近い費用へ戻る。したがって最適な終了層と下書き長は、下書き1トークンの費用、受理される連続長、検証を一括実行する効率の積で決まる。

### 6. 既存checkpointをそのまま使う方式ではない

層kipの中間層がdraftとして強いのは、専用の層-dropout＋early-exit trainingをした結果である。

既存Llama checkpointへ実行時だけ追加して同じ結果が出るわけではない。

学習時の層ドロップアウト（層 dropout）は複数の深さで残る層を使う経験を与え、途中終了損失（early-exit loss）は各中間表現を同じ語彙出力へ読み出せるようにする。前者だけでは浅い表現が次トークン予測へ十分整列する保証がなく、後者だけでは後半層を抜いた経路に本体が慣れない。二つを組み合わせることで、前半層を独立した下書き器として使える状態を作る。

以上の整理は、提案手法の動作原理と前提条件を保ったまま、一次資料の記述を要約したものである。

## 評価

### まず見るところ
- **結論:** 同じmodelの前半層をdraftへ使うことで、別draft modelなしのspeculative デコードを実現できる。
- **実速度:** **H100で実トークン/sを測定**し、1.3〜2倍超の改善を確認。
- **品質:** verifierが後半層で修正するため、early exit単独より品質を保ちやすい。
- **メモリ:** 別draft modelの重み/KVが不要。
- **注意点:** 専用学習とexit depth / draft lengthの調整が必要。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### 評価環境

| 項目 | 設定 |
|---|---|
| GPU | NVIDIA H100 |
| Models | Llama 2 7B / 13B、scratch 1.5B / 7B |
| Tasks | CNN/DailyMail, XSUM, HumanEval, TOPv2 |
| 主指標 | トークン/s, acceptance rate, ROUGE / task score |

### Llama 2 7B：代表結果

| Task | 設定 | 品質 | Acceptance | 高速化倍率 |
|---|---|---:|---:|---:|
| CNN/DM | E=8, d=12 | ROUGE-2 0.078 vs 0.079 | 68.9% | **1.86×** |
| XSUM | tuned | ROUGE-2 0.073維持 | — | 1.54× |
| HumanEval | tuned | score 0.042 | — | 1.83× |

CNN/DMでは62.7 トークン/sから127.9 トークン/sまで上がる。

### Llama 2 13B

| Task | 高速化倍率 |
|---|---:|
| CNN/DM | 1.81× |
| XSUM | 1.34× |
| HumanEval | 1.66× |

### scratch trainingの代表値

| Model | CNN/DM 高速化倍率 |
|---|---:|
| 1.5B | 1.76× |
| 7B | **2.16×** |

論文全体ではコードで最大約1.82倍、TOPv2で約2.0倍も報告する。

### Early exit単独との違い

単に途中層のlogitをそのまま確定出力へ使うと、浅いexitほど品質が落ちる。

層kipでは浅いexitを**確定出力ではなくdraft**として使い、残り層でverificationするため、高速化倍率と品質の両立がしやすい。

### 速度を決めるもの

| 要因 | 影響 |
|---|---|
| Exit 層が浅い | draftは速いがacceptance低下 |
| Exit 層が深い | acceptance向上、draft cost増加 |
| Draft lengthが長い | まとめて検証できるトークン数が増えるが、reject時の無駄も増加 |
| 層kip training | 中間層精度を上げacceptance改善 |

### 制約

- 専用の継続事前学習／fine-tuningが必要。
- exit 層とdraft lengthはmodel/task依存。
- acceptanceが低いtaskでは高速化倍率が縮む。
- 追加training costまで含めたtotal cost比較ではない。

</details>

## 一次資料
- [論文](https://aclanthology.org/2024.acl-long.681/)
- [公式コード](https://github.com/facebookresearch/LayerSkip)
## 更新履歴
- 2026-09-02: 概要・手法・評価を一次資料に基づき拡充。
- 2026-09-04: 層 Dropout / Early-Exit Loss / self-speculationを補足し、実トークン/s評価を表形式へ整理。
- 2026-09-07: 層 dropout / early-exit loss / shared 重み / acceptance等を、draft生成と検証の具体的な流れへ平易化。
