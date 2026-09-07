# KTransformers

KTransformersの主要な機能・性能更新を継続的に記録する集約ページ。CPUとGPUへmodel計算を分担させる異種実行（heterogeneous execution）、MoE expertのCPU実行、full-parameter / LoRA fine-tuning、FP8学習などを扱う。

## 現在できること

- 1つのmodel operatorをCPUとGPUへ分ける異種実行により、GPUへ収まりきらない巨大LLM / MoEをCPU RAMと併用して推論できる。
- attentionなどGPU向きの計算をGPUへ残し、大容量を占めるMoE expertをCPUで低bit実行する構成を取れる。
- operator injectionにより、model全体を作り直さず特定layer / operatorだけをKTransformersのCPU / GPU実装へ差し替えられる。
- CPU側ではINT4等の低bit expert計算を使い、host memory帯域と容量を抑えながらMoEを実行できる。
- full-parameter SFTとLoRA SFTにもCPU/GPU異種配置を使い、VRAMだけでは難しい大規模modelの追加学習を行える。
- FP8 expert weightやCPU activation保持を組み合わせ、training時のhost RAM / VRAM peakを抑えられる。

以下の更新履歴は、主に**CPU expert実行、低bit表現、異種fine-tuning、activation配置**がどう拡張されたかを記録している。

## 初期収録期間

2026-06-03〜2026-09-03

## 要点

この期間のKTransformersは、**巨大MoE modelのexpertをCPU側でも実用速度で動かすこと**と、**CPU RAMとGPU VRAMを併用して大規模modelをfine-tuningすること**を強化している。

KTransformersでは、attentionなどGPUが得意な処理をGPUへ残し、容量を大量に使うMoE expertや一部stateをCPU側へ置く構成が中心になる。そのためGPU性能だけでなく、CPUの行列演算命令、system RAM容量・帯域、CPU↔GPU転送が性能を左右する。

## 主要更新

### 2026-07-23 — v0.6.4（released）

- **CPU/GPU異種full-parameter / LoRA SFT**: model全parameterを更新するfull fine-tuningと、低rank adapterだけ更新するLoRAの両方で、CPUとGPUへ計算・stateを分散できるようにした。

  **SFT（Supervised Fine-Tuning; 教師あり追加学習）**は、入力と望ましい回答のpairを使ってpretrained modelを追加学習する工程。full-parameter SFTでは元model重み全体を更新するため必要memoryが大きく、LoRAでは小さい追加matrixだけを学習するためmemoryを大幅に減らせる。

- **RAWINT4 CPU expert path**: MoE expert weightを4-bit integerのままCPU向けに詰めた形式で保持し、推論・学習時に毎回BF16などへ完全展開せずmatrix multiplyへ使う経路を追加。

  packed INT4でmemory trafficを減らし、AVX-VNNIやAMXなどCPUの低精度matrix命令へ合わせたblocked matrix multiplicationを使う。

  - **AVX-VNNI（Vector Neural Network Instructions）**: Intel/AMD x86 CPUで低精度dot productを高速化するvector命令群。
  - **AMX（Advanced Matrix Extensions）**: Intel CPUのtile型matrix演算命令。大きなmatrix multiplyをCPU上で高throughputに実行する。

- **報告性能**: 2×EPYC 9355＋2×RTX 5090でfull fine-tuning約400 tok/s、LoRA約600 tok/s。RTX 4090＋AMX対応CPUでは700 tok/s超を報告。

[release](https://github.com/kvcache-ai/ktransformers/releases/tag/v0.6.4)

### 2026-08-17 — v0.7.0（released）

- **Native FP8 LoRA SFT**: routed expertのweightをFP8 E4M3形式のまま読み、blockごとのscaleと組み合わせてLoRA学習へ使う。従来のように全expert weightをBF16へ展開してhost RAMへ置く必要を減らす。

  **FP8 E4M3**は8-bit浮動小数点形式の1つで、指数4 bit・仮数3 bitを使う。BF16より表現精度は低いが、1要素あたりmemoryを半分にでき、対応hardwareでは計算も高速化できる。

- **blockwise load**: expert全体を一度に高精度へ展開せず、必要なblockだけscaleと一緒に読み込んで計算する。これにより巨大MoEのhost memory peakを下げる。

- **host RAM削減**: 対象構成では約 **1.4 TB → 約800 GB**へ削減。

- **CPU activation retention**: forwardで作った活性値（activation）の一部をGPUへ保持せずCPU側に残し、backward時に必要になった段階で使うことでVRAM pressureを下げる。

[release](https://github.com/kvcache-ai/ktransformers/releases/tag/v0.7.0)

v0.6.3は主にmodel対応追加で、性能・memory architectureの本質的変更が少ないため本一覧では掲載対象外とした。

### 用語メモ

- **異種実行（heterogeneous execution）**: 1つのmodelをCPUとGPUへ分け、それぞれ得意な処理や保持しやすいstateを担当させる方式。
- **routed expert**: MoEのgateがtokenごとに選ぶexpert。全expertを毎token使うわけではない。
- **LoRA（Low-Rank Adaptation; 低rank追加学習）**: 元の大きなweightを固定し、小さい低rank matrixだけ学習するfine-tuning方式。
- **blockwise quantization**: weight全体で1つのscaleを使わず、小さいblockごとにscaleを持たせ、低bit化による誤差を抑える方式。
