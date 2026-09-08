---
canonical_id: "ACL:2024.acl-long.681"
last_audited: null
audit_version: 0
storage_targets: []
bottlenecks: []
hardware_details: null
quality_effect: null
evidence_locations: []
title: "LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding"
summary: "学習時に途中layerからでもnext-token予測できるようmodelを訓練し、推論時は前半layerだけで数tokenを仮生成して、残りlayerでまとめて検証することで、別draft modelなしのspeculative decodingを行う。"
authors_affiliations: "Meta AIほか（ACL 2024、著者詳細は一次資料参照）"
published: "2024-08-12"
publication_status: "Published"
lineage: "Conditional Computation"
topics: ["Dynamic depth","Speculative decoding","Quality-cost"]
importance: "中"
hardware_evaluation: "実機"
source: "https://aclanthology.org/2024.acl-long.681/"
code: "https://github.com/facebookresearch/LayerSkip"
last_checked: "2026-09-02"
---

# LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding

> 学習時に途中layerからでもnext-token予測できるようmodelを訓練し、推論時は前半layerだけで数tokenを仮生成して、残りlayerでまとめて検証することで、別draft modelなしのspeculative decodingを行う。

## 概要
LayerSkipは、同じLLMの浅いlayerを**draft modelの代わり**に使い、残りlayerでそのdraft tokenを検証するself-speculative decodingを成立させる学習レシピである。

通常のspeculative decodingでは別の小型draft modelを常駐させるため、weight・KV・memoryが追加で必要になる。LayerSkipは同一modelの前半layerをdraft、後半layerをverifierとして使うので、別modelを持たなくてよい。

ただし既存checkpointの中間layerは、そのままではnext-token予測精度が低い。そこで学習時に、**一部layerをランダムに飛ばす訓練**と、**途中layerからも正解tokenを予測させるloss**を加え、中間layerからでもLM headで予測しやすい表現を作る。

H100実機でtoken/sまで測定しており、taskにより約1.3〜2.16倍のspeedupを示す。単純なlayer skipではなく、**浅い予測を後段で検証して誤りを修正するため品質を守りやすい**のが特徴である。

## 手法のあらまし

### 1. 学習中にいろいろな深さのsubmodelを経験させる

学習時、Transformer layerを確率的にskipする。

後段ほどdropout率を高くすることで、前半layerだけでもある程度next-token予測に使える表現を作れるようにする。

これは推論時の単純なlayer pruningとは違い、**同じweightを複数のdepthで使えるよう事前に慣らす学習**である。

### 2. 中間layerから直接next-token予測を学習する

各中間layerのhidden stateを、最終layerと同じLM headへ通してcross-entropy lossを追加する。

exitごとに別classifierを持つのではなく、**全exitが同じLM headを共有する**。

これにより中間layerの表現を語彙logitへ直接読み出しやすくする。

### 3. 前半layerだけでdraftし、後半layerでまとめて検証する

推論時はexit layer `E` までで数tokenをdraft生成する。

その後、残りの `L-E` layerを使ってdraft token列をまとめて検証する。

- draftが正しい部分 → そのままaccept
- 最初の不一致 → full model側の予測で修正

という通常のspeculative decodingと同じ考え方だが、draftとtargetが**一つのmodelの前半／後半**に分かれている。

### 4. Weightと前半layerのKVを別draft model用に複製しなくてよい

別draft modelを持たないので、前半layerのweightを二重に常駐させる必要がない。

またdraft時に作った前半layerのactivation/KVをverificationでも再利用できる。

この共有が、外部draft model方式に対するmemory上の主な利点になる。

### 5. Exit layer `E` とdraft token数 `d` のバランス

速度を決める主な2parameter。

- `E`が浅すぎる → draft精度が下がりrejectが増える
- `E`が深すぎる → draft自体が重くなる
- `d`が短すぎる → まとめてverificationする利得が小さい
- `d`が長すぎる → 途中でrejectされた時の無駄計算が増える

最適点は単なる「浅いほど速い」ではなく、draft acceptanceとのバランスで決まる。

### 6. 既存checkpointをそのまま使う方式ではない

LayerSkipの中間layerがdraftとして強いのは、専用のlayer-dropout＋early-exit trainingをした結果である。

既存Llama checkpointへruntimeだけ追加して同じ結果が出るわけではない。

## 評価

### まず見るところ
- **結論:** 同じmodelの前半layerをdraftへ使うことで、別draft modelなしのspeculative decodingを実現できる。
- **実速度:** **H100で実token/sを測定**し、1.3〜2倍超の改善を確認。
- **品質:** verifierが後半layerで修正するため、early exit単独より品質を保ちやすい。
- **メモリ:** 別draft modelのweight/KVが不要。
- **注意点:** 専用学習とexit depth / draft lengthの調整が必要。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### 評価環境

| 項目 | 設定 |
|---|---|
| GPU | NVIDIA H100 |
| Models | Llama 2 7B / 13B、scratch 1.5B / 7B |
| Tasks | CNN/DailyMail, XSUM, HumanEval, TOPv2 |
| 主指標 | token/s, acceptance rate, ROUGE / task score |

### Llama 2 7B：代表結果

| Task | 設定 | 品質 | Acceptance | Speedup |
|---|---|---:|---:|---:|
| CNN/DM | E=8, d=12 | ROUGE-2 0.078 vs 0.079 | 68.9% | **1.86×** |
| XSUM | tuned | ROUGE-2 0.073維持 | — | 1.54× |
| HumanEval | tuned | score 0.042 | — | 1.83× |

CNN/DMでは62.7 token/sから127.9 token/sまで上がる。

### Llama 2 13B

| Task | Speedup |
|---|---:|
| CNN/DM | 1.81× |
| XSUM | 1.34× |
| HumanEval | 1.66× |

### scratch trainingの代表値

| Model | CNN/DM speedup |
|---|---:|
| 1.5B | 1.76× |
| 7B | **2.16×** |

論文全体ではコードで最大約1.82倍、TOPv2で約2.0倍も報告する。

### Early exit単独との違い

単に途中layerのlogitをそのまま確定出力へ使うと、浅いexitほど品質が落ちる。

LayerSkipでは浅いexitを**確定出力ではなくdraft**として使い、残りlayerでverificationするため、speedupと品質の両立がしやすい。

### 速度を決めるもの

| 要因 | 影響 |
|---|---|
| Exit layerが浅い | draftは速いがacceptance低下 |
| Exit layerが深い | acceptance向上、draft cost増加 |
| Draft lengthが長い | まとめて検証できるtoken数が増えるが、reject時の無駄も増加 |
| LayerSkip training | 中間layer精度を上げacceptance改善 |

### 制約

- 専用の継続事前学習／fine-tuningが必要。
- exit layerとdraft lengthはmodel/task依存。
- acceptanceが低いtaskではspeedupが縮む。
- 追加training costまで含めたtotal cost比較ではない。

</details>

## 一次資料
- [論文](https://aclanthology.org/2024.acl-long.681/)
- [公式コード](https://github.com/facebookresearch/LayerSkip)
## 更新履歴
- 2026-09-02: 概要・手法・評価を一次資料に基づき拡充。
- 2026-09-04: Layer Dropout / Early-Exit Loss / self-speculationを補足し、実token/s評価を表形式へ整理。
- 2026-09-07: layer dropout / early-exit loss / shared weights / acceptance等を、draft生成と検証の具体的な流れへ平易化。
