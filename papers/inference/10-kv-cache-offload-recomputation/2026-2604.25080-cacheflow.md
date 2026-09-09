---
canonical_id: "arXiv:2604.25080"
arxiv_id: "2604.25080"
title: "CacheFlow: Efficient LLM Serving with 3D-Parallel KV Cache Restoration"
summary: "以前処理した長いprefixのKVキャッシュがGPU外に退避されているとき、全部をI/Oで戻すか全部を再計算するかの二択にせず、prefixの一部はGPUで再計算し、別部分は外部メモリから読み戻して同時進行させる手法。さらにこの分担をトークン方向だけでなく層方向・複数GPU方向にも広げ、同じバッチ内の複数要求がGPU計算資源とI/O帯域を奪い合う状況までまとめてスケジュールする。"
source: "https://arxiv.org/abs/2604.25080"
last_audited: "2026-09-09"
audit_version: 1
---

# CacheFlow: Efficient LLM Serving with 3D-Parallel KV Cache Restoration

> 以前処理した長いprefixのKVキャッシュがGPU外に退避されているとき、全部をI/Oで戻すか全部を再計算するかの二択にせず、prefixの一部はGPUで再計算し、別部分は外部メモリから読み戻して同時進行させる手法。さらにこの分担をトークン方向だけでなく層方向・複数GPU方向にも広げ、同じバッチ内の複数要求がGPU計算資源とI/O帯域を奪い合う状況までまとめてスケジュールする。

## 書誌情報

- **著者**: Sean Nian, Jiahao Fang, Qilong Feng, Zhiyu Wu, Fan Lai
- **所属**: University of Illinois Urbana-Champaign, National University of Singapore
- **公開**: 2026-04-28, arXiv v1
- **種別**: プレプリント（preprint）
- **主題**: KVキャッシュ復元（KV cache restoration）、長文LLM提供、再計算とI/Oの重畳、複数GPU、バッチスケジューリング
- **実装**: vLLMとLMCacheを基盤に実装して評価。arXiv v1時点で独立した公式コードリポジトリは確認できない。

## 概要

CacheFlowが扱うのは、**「前に一度計算した長い文脈をもう一度使いたいが、そのKVキャッシュはGPUメモリから追い出されている」**という状況である。

LLMは入力処理（prefill）を行うと、各層・各トークンについて注意機構（attention）で使うKey/Valueを計算し、**KVキャッシュ（KV cache）**として保存する。同じprefixを後で再利用できれば、入力文を最初からモデルへ通す必要がない。

しかし長文のKVキャッシュは非常に大きい。多数ユーザー、RAG、長いchat、エージェント処理を同時に扱うとGPU HBMへ全部置いておけないため、CPUメモリや別のメモリ階層へ退避する。

その要求が再び来たとき、GPUでdecodeを始めるにはKVを復元しなければならない。基本的な方法は二つある。

1. **読み戻す**: 退避しておいたKVをI/OでGPUへ戻す。
2. **再計算する**: 元のtokenをもう一度prefillし、KVをGPUで作り直す。

読み戻しはGPU計算を節約できるが、ネットワークやPCIeなどのI/O帯域が遅いと待ち時間が長い。再計算はI/Oを使わないが、長いprefixほどattention計算が重くなる。

CacheFlowの発想は、どちらか一方を選ぶのではなく、**同じKV復元の中で両方を同時に進め、先に終わった側からprefixを埋めていく**ことである。

さらに、この並列化を

- トークン方向
- Transformer層方向
- 複数GPU方向

の3次元へ広げる。論文が「3D-parallel restoration」と呼ぶのはこのためである。

## 問題設定

### なぜKVを読み戻すだけでは遅いのか

例えば30Kトークンのprefixについて数GBのKVがCPU側にあるとする。GPUへ戻す時間は、ほぼ

`転送するKV量 ÷ 実効I/O帯域`

で決まる。

10 Gbps程度の経路なら、GPUの計算性能がどれだけ高くても、転送が終わるまでattentionを始められない。KV reuseのために保存したのに、復元I/Oが最初のトークンまでの時間を支配する。

この最初の出力までの時間を**最初のトークンまでの時間（Time To First Token; TTFT）**という。

### なぜ再計算だけでも遅いのか

KVを保存せず、prefix tokenから再prefillすればI/Oは要らない。

しかしTransformerのattentionでは後ろのtokenほど参照する過去tokenが多くなる。単純化すると、prefixの後半を再計算するほどattentionの仕事が増える。

6K程度なら再計算が比較的安くても、30K、100Kと伸びると、GPU計算時間が急速に増える。

つまり、

- I/Oが遅い環境 → 再計算した方がよい部分がある
- 長いprefix後半 → 再計算が高いのでKVを読んだ方がよい

という交差が生じる。

### 既存hybrid方式だけでは何が足りないのか

「request Aは全部読み戻す、request Bは全部再計算する」という要求単位の選択では粒度が粗い。

一つの長いrequestの中でも、先頭tokenは再計算が比較的安く、後半tokenは高い。層ごとにも復元を分けられる。複数GPUでpipeline parallelismを使うなら、それぞれのGPUは別のmodel shardを持つため、同時に復元できる余地がある。

CacheFlowは、この内部並列性をまとめて利用する。

## 手法のあらまし

最も直感的なのはtoken-wise方式である。

長いcached prefixを小さなchunkへ分け、**先頭側からGPU再計算を進めるpointer**と、**末尾側からKV読出しを進めるpointer**を同時に動かす。

```text
prefix:
|----|----|----|----|----|----|----|----|
 ↑compute →                   ← I/O ↑
```

先頭側は再計算が比較的安い。末尾側は再計算するとattention costが大きいので、保存KVを読む価値が高い。両pointerが出会えば全prefixのKV復元が終わる。

短いsequenceでは、このtoken方向分割だけでは十分な重畳時間が取れないため、layer方向にも分ける。さらにpipeline parallelismではGPUごとに必要KVを独立復元できるよう、stage境界のhidden activationも保存する。

最後に複数requestが同時復元するときは、各requestが勝手にcompute/I/Oを使わず、global schedulerがどのrequestへI/O帯域を与えるかを決める。

## 手法

### 1. Token-wise restoration — prefixの前半を再計算、後半を読み戻す

CacheFlowはcached prefixを通常512-token程度のchunkへ分割する。

前から進むcompute pointerは、元tokenをGPUでprefillしてKVを作る。後ろから進むI/O pointerは、退避先から保存済みKVをGPUへ読み戻す。

この二つは同時に進む。

なぜ逆方向なのかが重要である。

prefixの先頭chunkを再計算するときはattention対象が短い。一方、prefix末尾のchunkを再計算すると、それ以前の長い文脈すべてへattentionする必要があるため高価になる。

したがって、

- **前半**: 再計算向き
- **後半**: I/O復元向き

という非対称性がある。

単純な「半分再計算・半分load」ではなく、computeとI/Oの進行速度に応じて境界が決まるため、どちらか一方が早く終わって遊ぶ時間を減らせる。

### 2. 再計算とI/Oを重ねるとはどういうことか

GPUがprefix先頭をprefillしている間、I/O engineは別のKV chunkをGPUメモリへ転送する。

二つが完全に別資源なら、例えば

- 再計算だけ: 300 ms
- I/Oだけ: 400 ms

を順番にやれば700 ms掛かるが、同時に走らせれば理想的には長い方の400 ms付近へ近づけられる。

実際にはPCIe、memory bandwidth、CUDA実行などで競合するため完全には重ならない。それでもGPU利用率とI/O利用率を同時に高く保つことがCacheFlowの狙いである。

### 3. Layer-wise restoration — 短いsequenceでは層方向に並列化する

token方向の利点は、prefixが十分長いほど大きい。短いprefixではchunk数が少なく、computeとI/Oを長時間重ねる余地がない。

そこでCacheFlowは別方式として、Transformerの**層方向（layer-wise）**にも分割する。

概念的には、

- GPU計算: layer 0側から必要KVを再計算
- I/O: 最終layer側から保存KVを読み戻す

と進める。

token方向と同様、両側から仕事を進めて出会わせる。

どちらが有利かはprefix長・GPU速度・I/O帯域に依存するため、offline profilingで**交差長（crossover length）**を測り、短いsequenceではlayer-wise、長いsequenceではtoken-wiseを選ぶ。

### 4. Multi-GPU restoration — pipeline stageを順番待ちさせない

Pipeline Parallelism（PP）では、モデルの層を複数GPUへ分ける。

通常の再計算では、GPU 1が前半層を計算し、そのhidden activationをGPU 2へ渡し、GPU 2が後半層を計算するという依存がある。KV restorationでもこの依存をそのまま辿ると、後段GPUは前段が終わるまで待つ。

CacheFlowはpipeline stage境界の**hidden activation**も保存しておく。

そうすると各GPUは、前段を最初から再実行しなくても、自分のstage開始地点のactivationから自分のmodel shard用KVを復元できる。

これにより複数GPUがそれぞれ

- 自分のstageで再計算する
- 自分のKVをI/Oで読む

処理を同時に進められる。

これが3Dの3軸目、GPU方向の並列化である。

### 5. なぜhidden activationを追加保存する価値があるのか

KVだけ保存するより、stage境界activationも保存すればstorage量は増える。

しかしその代わり、GPU間の逐次依存を切り、複数GPUを復元段階から並列稼働させられる。

つまりCacheFlowは、**少し追加状態を保存することで将来の復元並列性を買う**設計である。

これは「何をキャッシュするか」を単純な再利用率だけでなく、後の復元critical pathまで考えて決める例でもある。

### 6. Batch-aware scheduler — 複数requestがI/Oを奪い合うときの優先順位

実際のservingでは、一つのrequestだけを復元するとは限らない。

複数requestが同時に戻ってくると、

- GPU compute
- I/O bandwidth

という二つの有限資源を共有する。

各requestが独立に「自分の後半KVをloadする」と決めると、I/Oが混雑し、結果として全requestのTTFTが悪化する場合がある。

CacheFlowのbatch-aware schedulerは、各requestのcompute pointerとI/O pointerをglobalに管理する。

特に、**これから再計算すると高価になる長いprefix部分**へI/Oを優先する。短い・安い部分はGPUで再計算させ、I/O帯域は「再計算で代替しにくい部分」へ回す。

したがってschedulerの役割は単なる公平配分ではなく、computeとI/Oの**機会費用**を比較して帯域を割り当てることである。

### 7. 3D-parallelの意味

論文の「3D」は、データ並列・テンソル並列のような一般的3D parallelism名称ではない。KV restorationを次の3軸へ分解する意味で使われる。

| 軸 | 並列化するもの | 目的 |
|---|---|---|
| Token | prefixの前後chunk | 再計算とI/Oを同時進行 |
| Layer | Transformer前後層 | 短いsequenceでも重畳余地を作る |
| GPU | pipeline stages | 複数GPUの復元を独立化 |

その上にbatch-aware schedulingがあり、複数request間のresource sharingを調整する。

## 評価

### まず見るところ

- **結論**: KV復元を全部load・全部recomputeの二択にせず、computeとI/Oを同時に使うことでTTFTを10〜62%削減。
- **長文ほど効く**: 6K→30Kでbaselineとの差が1.1倍→1.7倍へ拡大。
- **資源利用**: 復元中にGPU平均88%、I/O平均78%を同時利用。
- **multi-GPU**: GPU軸最適化を外すと0.21→0.29秒、38%悪化。
- **品質**: KV圧縮・pruningは行わず、保存KVまたは再計算KVを使うため直接のモデル品質trade-offはない。
- **注意**: 公式コード公開は確認できず、NVIDIA GPUと10〜80 Gbpsの評価範囲に依存する。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### モデルとworkload

- Qwen3-8B
- Llama-3.1-8B
- Qwen3-30B-A3B

workloadはLMSYS-Chat、WildChat、SWE-Bench。

### Hardware

- NVIDIA L40S 46GB
- NVIDIA A100 40GB
- NVIDIA H100 80GB

I/O帯域は10 / 40 / 80 Gbpsを評価し、defaultは10 Gbps。

比較対象はvLLM、SGLang HiCache、LMCache v0.3.1、Cake。

### TTFT改善

既存方式比でTTFTを**10〜62%削減**し、条件によって**1.1〜1.7倍**改善する。

prefix長を6Kから30Kへ伸ばすとvLLM/SGLangとの差は**1.1倍→1.7倍**へ広がる。

これは長文ほど「後半を再計算するcost」が高くなり、compute/loadを適切に分担する価値が増えるためである。

### GPUとI/Oを同時に使えているか

KV復元中の平均利用率は

- GPU: **88%**
- I/O: **78%**

を報告する。

LMCacheはGPU利用が約10%で、load待ち中心。vLLMはGPU約91%を使うがI/Oはほぼ使わず、再計算中心になる。

CacheFlowは両方を同時に使う中間点を狙っている。

### Multi-GPUの寄与

multi-GPU最適化を外すと平均復元latencyは

**0.21秒 → 0.29秒**

へ38%増加する。

GPU軸を使わない2D版だけでもvLLMより24%高速だが、3軸目が追加改善を与える。

### I/O帯域が速くても意味はあるか

H100で40 / 80 Gbps条件でも、それぞれ**1.7倍 / 1.5倍**改善を報告する。

I/Oが高速になるほど全部loadの競争力が上がるため、80 Gbpsでは相対利得がやや小さくなる。

### 大きなMoEと複数GPU

Qwen3-30B-A3B、10 Gbps条件で

- 2×L40S: **1.6倍**
- 2×A100: **1.5倍**

改善。

batch size 2 / 4 / 8では**1.6〜2.6倍**の改善を報告する。

</details>

## 主要結果の読み方

CacheFlowの本質は、新しい圧縮方式ではなく**resource overlap**にある。

KVを保存しておくと「再計算しなくてよい」という利点があるが、保存場所がGPU外なら復元I/Oが必要になる。逆に再計算はI/Oを避けられるがGPUを使う。

この二つは別resourceを使うので、どちらか一方を遊ばせるより同時に働かせた方がよい。

ただし単純に50/50へ分けるのではなく、token位置によって再計算costが違い、sequence長によってlayer-wiseとの優劣が変わり、multi-GPUでは依存関係があり、batch内では帯域競合もある。

そのためCacheFlowは「hybrid restoration」を単なる比率調整ではなく、**token / layer / GPU / requestの依存関係を持つスケジューリング問題**として扱っている。

## 品質への影響

KVを量子化、圧縮、token pruningする方式ではない。

一部KVは保存済みのexact KVを読み、一部は元tokenから通常のprefillで再計算する。したがって設計そのものがモデル意味論を近似するわけではなく、直接的な生成品質低下は導入しない。

## 既存研究との差

- **LMCache / HiCache**: KVをGPU外へ保存・復元するmemory hierarchyが主眼。CacheFlowは復元時にGPU再計算も同時利用する。
- **Cake**: compute/load hybridをtoken方向で行う考え方に近い。CacheFlowはlayer軸とmulti-GPU軸まで広げ、batch内resource contentionも統合する。
- **HCache**: hidden stateを使う復元と関連する。CacheFlowでは特にpipeline stage境界activationを保存し、GPUごとの独立復元へ使う。
- **Mooncake等のdisaggregated KV transfer**: KVを高速に移動する仕組みとは補完的。CacheFlowは「転送帯域が有限なとき、どこを転送しどこを計算するか」を決める。

## 限界

- 評価はNVIDIA L40S/A100/H100と10〜80 GbpsのI/O条件が中心で、別accelerator・storage階層への一般化は未検証。
- multi-GPUの理想的なscaleは均等partitionや十分な独立性を仮定し、実機ではstage imbalanceで弱まる。
- hidden activationを追加保存するため、KV-only cachingよりcache容量が増える。
- computeとI/Oが実際にはmemory bandwidth等を共有する場合、理想的なoverlapは得られない。
- workloadによってcached prefix lengthやbatch構成が変わるため、最適なtoken/layer分担も変化する。
- 公式コードリポジトリはarXiv v1時点で確認できない。

## 一般的な実装上の含意

階層memoryを使うLLM systemでは、cache miss時の復元を「I/O処理」だけとして設計しない方がよい。

データを戻す間にGPUが空いているなら、GPUで一部を再計算することで復元critical pathを短くできる。逆にGPUが忙しくI/Oが空いているなら、保存データを多く読む方がよい。

したがって一般には、

1. **再計算cost**
2. **I/O cost**
3. **両者をどれだけ重ねられるか**
4. **位置によってcostが変わるか**
5. **複数request/GPUでresource contentionがあるか**

を同時に見るべきである。

この考え方はKVだけでなく、MoE expert、activation checkpoint、SSD-backed weightなどにも応用できる。**「保存するか再計算するか」ではなく、「どの部分をどちらに任せ、どう同時実行するか」**が重要になる。

## 一次資料

- arXiv: https://arxiv.org/abs/2604.25080
- HTML: https://arxiv.org/html/2604.25080v1

## 更新履歴

- 2026-09-09: MoE-Infinity基準に合わせて全面改稿。KV restorationの意味、loadとrecomputeのtrade-off、token-wise / layer-wise / multi-GPUの3軸、batch-aware schedulingを論文未読者向けに説明。
