---
canonical_id: "DOI:10.1145/3731569.3764843"
title: "KTransformers: Unleashing the Full Potential of CPU/GPU Hybrid Inference for MoE Models"
authors: ["Hongtao Chen","Weiyu Xie","Boxin Zhang","Jingqi Tang","Jiahao Wang","Jianwei Dong","Shaoyuan Chen","Ziwei Yuan","Chen Lin","Chengyu Qiu","Yuening Zhu","Qingliang Ou","Jiaqi Liao","Xianglin Chen","Zhiyuan Ai","Yongwei Wu","Mingxing Zhang"]
published: 2025-10-12
publication_status: "SOSP 2025"
summary: "KTransformersは巨大な混合専門家（MoE）モデルを少数GPUで動かすCPU/GPU混成推論で、CPU演算性能不足と同期待ちを解く。AMX/AVX-512専用カーネル、単一CUDA Graphを用いる非同期CPU-GPU実行、NUMAを考慮した重み配置を組み合わせ、さらに一部expert出力を次層へ遅延注入するExpert DeferralでCPUとGPUを重畳する。既存方式比でプリフィル4.62〜19.74倍、デコード1.25〜4.09倍、Expert Deferral込みではデコード最大4.90倍を示し、追加高速化時の平均精度低下を0.5%以内に抑える。"
list_summary: "巨大MoEのrouted expertをCPUで高速実行し、非同期CPU-GPUスケジューリングとExpert Deferralで同期待ちを隠して少数GPU推論を高速化する。"
source: "https://doi.org/10.1145/3731569.3764843"
worker_completed_at: "2026-09-30T17:06:39+09:00"
worker_run_key: "20260930-1700-scheduled-chat-00"
reference_main_sha: "d2dffadff91fadaa048ba44ad3dd399c7b9794c0"
---

# KTransformers: Unleashing the Full Potential of CPU/GPU Hybrid Inference for MoE Models

## 概要
巨大な混合専門家モデルは総パラメータ数が大きい一方、各tokenで使う専門家は少数である。この疎性は、注意や共有専門家をGPUに置き、多数のrouted expertを大容量CPUメモリへ置く混成推論と相性がよい。しかし単純なオフロードではCPU側の小さな行列演算が遅く、MoE層の結果を待つ間GPUが停止するため、PCIe転送だけでなくCPU計算と同期が律速になる。

KTransformersは重みを毎token転送する方式ではなく、専門家をCPU DRAMへ常駐させてCPUで直接計算する。そのためにIntel AMXとAVX-512へ合わせたMoEカーネル、NUMA配置、CPU/GPU非同期実行、CUDA Graphを組み合わせる。さらにExpert Deferralでは一部専門家の結果を次層まで遅らせ、次層のGPU注意計算と並行してCPU専門家を実行する。完全精度構成で既存方式比プリフィル4.62〜19.74倍、デコード1.25〜4.09倍を達成する。

## 問題設定
DeepSeek-V3/R1のような671B級MoEでは全expert重みを単一GPUへ置けないが、1 tokenが選ぶexpertは一部だけである。CPUメモリは容量単価が低く、AMXを持つ近年のXeonは行列演算も可能なので、routed expertをCPUに置く構成が現実的になる。

ただしデコードでは各expertに届くtoken数が少なく、行列×ベクトルに近い低算術強度になる。大きな行列向けAMXだけでは起動・タイル処理の固定費が目立つ。またTransformerの通常順序ではMoE出力が次の注意層の入力になるため、CPU expertが終わるまでGPUが待つ。KTransformersは「CPUを速くする」と「依存関係を緩めて待たせない」を分けて処理する。

## 手法

### AMX/AVX-512適応カーネル
プリフィルのようにexpertあたりtoken数が多い場合はAMXのタイル行列演算を使い、重みレイアウトと量子化形式をAMXへ合わせる。デコードのようにexpertあたり4 token以下の低算術強度では、軽量なAVX-512カーネルへ切り替える。両カーネルが同じ重み配置を使えるよう設計し、切替のための再配置を避ける。

MoEのgate/up/down射影も個別小演算として起動せず、依存しない処理をまとめた融合演算へ変える。これによりCPUスレッド同期と小GEMM起動の固定費を減らす。論文のマイクロベンチマークでは各種最適化が1.69〜4.30倍の改善を示す。

### NUMAを意識した配置
多ソケットCPUでは遠隔NUMAメモリからexpert重みを読むと帯域が落ちる。KTransformersはexpert重みを計算スレッドに近いNUMA nodeへ配置し、CPU側のメモリ帯域を使い切る。巨大MoEではCPU計算より重み読出しが支配する条件もあるため、単純なスレッド数増加ではなくデータ配置まで制御する。

### 非同期CPU-GPUスケジューリング
GPU側の注意・共有expertとCPU側routed expertを独立taskとして発行し、可能な範囲で同時実行する。デコード全体を単一CUDA Graphへ入れ、CUDA上のspinningを利用して動的な形状やCPU完了通知を扱う。層・batchごとに多数のGraphを持つ方式よりVRAM固定費を抑え、kernel launchと同期を減らす。この機構だけでもデコードで最大1.23倍の追加改善を報告する。

### Expert Deferral
通常は第k層の全expert出力を足してから第k+1層へ進む。Expert Deferralはrouted expertをimmediate群とdeferred群へ分け、immediate群だけをその場で反映し、deferred群の出力は一層遅れて加える。これによりCPUがdeferred expertを計算している間にGPUは次層の注意等を開始できる。

DeepSeek-V3の代表構成では各層8 routed expertのうち5を即時、3を遅延させる。一般則としてCPUを飽和させる最小数だけ遅延し、少なくとも2 expertを即時に残してモデル安定性を守る。これは厳密な元モデル計算順を変える近似であるため、速度と精度の交換条件を伴う。

## 評価条件

|項目|内容|
|---|---|
|対象モデル|DeepSeek-V3/R1級、DeepSeek-V2、Qwen系MoE等|
|代表最大規模|671B級MoE|
|比較|Fiddler、llama.cpp等のCPU/GPU混成推論|
|CPU機構|Intel AMX、AVX-512、NUMA最適化|
|GPU機構|CUDA Graph、非同期CPU-GPU実行|
|精度形式|BF16/FP16に加えINT4/INT8構成|
|評価|prefill token/s、decode token/s、CPU/GPU利用率、精度|

## 主要結果

|条件|比較|結果|意味|
|---|---|---|---|
|完全精度構成|既存混成方式|prefill 4.62〜19.74倍|CPU MoEカーネル最適化が長いpromptで効く|
|完全精度構成|既存混成方式|decode 1.25〜4.09倍|低算術強度カーネルと非同期化が効く|
|Expert Deferral追加|最適化済みKTransformers|throughput最大1.45倍|層間依存を緩める余地が残る|
|DeepSeek-V3例|Deferral前後|CPU利用率 約74%→100%、GPU 約28%→37%|CPU/GPU待ち時間を重畳へ変換|
|Deferral込み総括|既存方式|decode最大4.90倍|カーネル高速化と実行順変更が累積|
|品質|Deferralなし/あり|平均accuracy低下0.5%以内|近似実行順の品質費用を限定|

DeepSeek-V3の一条件では最適化後も5.87 token/s程度でCPU側が律速となり、ここからExpert Deferralを導入する動機になっている。したがってDeferralは最初から全構成へ必要なのではなく、カーネルと非同期化を適用した後にもCPU待ちが残る大規模MoEで効果が大きい。

## 既存研究との差
重みオフロード方式は必要なexpertをGPUへ転送して実行するが、PCIe帯域と転送待ちが問題になる。KTransformersはrouted expertをCPUに常駐させCPUで直接計算し、GPUは高帯域が必要な注意・共有部分へ集中させる。

llama.cpp等のCPU/GPU分割に対しては、MoEの疎性を前提にexpert専用カーネル、NUMA配置、非同期実行を統合する。さらにExpert Deferralは単なる配置最適化ではなくTransformerの残差構造を利用して計算順を変え、CPUとGPUの依存待ちそのものを減らす。

## 限界
最高性能はAMXを備えた近年のIntel CPU、十分なDRAM帯域、特定の量子化形式に依存する。AVX-512 fallbackはあるが、CPU命令セットやNUMA構成が異なれば論文の倍率はそのまま得られない。高同時実行ではGPUへexpertを置く通常サービングの方が有利になる場合もあり、本方式は特にローカル・低並列の巨大MoEを主対象とする。

Expert Deferralは元モデルと完全同値ではない。遅延expert数を増やすほど重畳余地は増えるが精度低下リスクも増えるため、最低2 expertを即時に残す等のヒューリスティックが必要である。平均0.5%以内という品質結果は評価したベンチマークと設定に対する値である。

## 一次資料
- https://doi.org/10.1145/3731569.3764843
- https://madsys.cs.tsinghua.edu.cn/publication/ktransformers-unleashing-the-full-potential-of-cpu/gpu-hybrid-inference-for-moe-models/SOSP25-chen.pdf