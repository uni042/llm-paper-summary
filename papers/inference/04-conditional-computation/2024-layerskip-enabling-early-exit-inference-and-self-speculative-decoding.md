---
title: "LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding"
summary: "学習時のlayer dropoutとearly-exit損失により、同一モデルで早期終了とself-speculative decodingを可能にする手法。"
authors_affiliations: "Meta AIほか（ACL 2024、著者詳細は一次資料参照）"
published: "2024-08-12"
publication_status: "Published"
lineage: "Conditional computation"
topics: ["Dynamic depth","Speculative decoding","Quality-cost"]
importance: "中"
hardware_evaluation: "実機"
source: "https://aclanthology.org/2024.acl-long.681/"
code: "https://github.com/facebookresearch/LayerSkip"
last_checked: "2026-09-02"
---

# LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding

> 学習時のlayer dropoutとearly-exit損失により、同一モデルで早期終了とself-speculative decodingを可能にする手法。

## 概要
LayerSkipは、同じLLMの浅い層を**draft modelの代わり**に使い、残りの層でそのdraft tokenを検証する `self-speculative decoding` を成立させる学習レシピである。

通常のspeculative decodingでは別の小型draft modelを常駐させるため、重み・KV・メモリが追加で必要になる。LayerSkipは同一モデルの前半層をdraft、後半層をverifierとして使うので、別モデルを持たなくてよい。

ただし既存checkpointの中間層はそのままでは次token予測精度が低い。そこで学習時に `layer dropout` と `early-exit loss` を加え、中間層からでもLM headで予測しやすい表現を作る。

H100実機でtoken/sまで測定しており、taskにより約1.3〜2.16倍のspeedupを示す。単純な層skipではなく、**浅い推測を後段で検証するため品質を守りやすい**のが特徴である。

## 手法のあらまし

### 1. `Layer Dropout`：学習中にいろいろな深さのsubmodelを経験させる

学習時、Transformer層を確率的にskipする。

後段ほどdropout率を高くすることで、前半層だけでもある程度意味の通る表現を作れるようにする。

これはinference時の単純なlayer pruningとは違い、**同じ重みを複数のdepthで使えるよう事前に慣らす学習**である。

### 2. `Early-Exit Loss`：中間層から直接next-token予測を学習する

各中間層のhidden stateを、最終層と同じLM headへ通してcross-entropy lossを追加する。

出口ごとに別classifierを持つのではなく、**全出口が同じLM headを共有する**点が重要。

これにより中間層の表現を最終的な語彙logitへ直接読み出しやすくする。

### 3. `Self-Speculative Decoding`

推論時は出口層 `E` までで数tokenをdraft生成する。

その後、残りの `L-E` 層を使ってdraft token列をまとめて検証する。

- draftが正しい部分 → そのままaccept
- 最初の不一致 → full model側の予測で修正

という通常のspeculative decodingと同じ考え方だが、draftとtargetが**一つのmodelの前半／後半**に分かれている。

### 4. `Shared Weights / Shared KV`

別draft modelを持たないので、前半層のweightを二重に常駐させる必要がない。

またdraft時に作った前半層のactivation/KVをverificationでも再利用できる。

この共有が、外部draft model方式に対するmemory上の主な利点になる。

### 5. `Exit Layer E` と `Draft Length d`

速度を決める主な2パラメータ。

- `E`が浅すぎる → draft精度が下がりrejectが増える
- `E`が深すぎる → draft自体が重くなる
- `d`が短すぎる → parallel verificationの利得が小さい
- `d`が長すぎる → reject後の無駄計算が増える

つまり最適点は単なる「浅いほど速い」ではなく、acceptanceとのバランスで決まる。

### 6. 既存checkpointをそのまま使う方式ではない

LayerSkipの中間層がdraftとして強いのは、専用のlayer-dropout＋early-exit trainingをした結果である。

既存Llama checkpointへruntimeだけ追加して同じ結果が出るわけではない。

## 評価

### まず見るところ
- **結論:** 同じモデルの前半層をdraftへ使うことで、別draft modelなしのspeculative decodingを実現できる。
- **実速度:** **H100で実token/sを測定**し、1.3〜2倍超の改善を確認。
- **品質:** verifierが後半層で修正するため、early exit単独より品質を保ちやすい。
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

単に途中層のlogitをそのまま採用すると、浅い出口ほど品質が落ちる。

LayerSkipでは浅い出口を**確定出力ではなくdraft**として使い、残り層でverificationするため、speedupと品質の両立がしやすい。

### 速度を決めるもの

| 要因 | 影響 |
|---|---|
| Exit layerが浅い | draftは速いがacceptance低下 |
| Exit layerが深い | acceptance向上、draft cost増加 |
| Draft lengthが長い | parallelism増加、reject時の無駄も増加 |
| LayerSkip training | 中間層精度を上げacceptance改善 |

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
