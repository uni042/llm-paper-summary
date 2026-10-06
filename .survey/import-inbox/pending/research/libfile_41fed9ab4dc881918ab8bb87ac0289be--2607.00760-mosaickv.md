---
canonical_id: "arXiv:2607.00760"
title: "MosaicKV: Serving Long-Context LLM with Dynamic Two-D KV Cache Compression"
summary: "MosaicKVは長文脈KV cacheをsequence軸とchannel軸の両方でsegment単位に動的圧縮し、重要要素に応じて圧縮方式を変える。圧縮cache管理をGPU/CPUの余剰資源へ分散し、H800評価でmemoryを3倍削減、attention最大16倍、decode latency最大4.8倍、throughput最大7.3倍改善し、LongBench/RULER平均accuracy lossを1.76%に抑える。"
list_summary: "長文脈KVをtoken軸とchannel軸の2次元で適応圧縮し、圧縮管理もGPU/CPUへ分散してcache容量とattention計算を同時に削減する。"
authors: ["Sheng Qiang","Ruiwei Chen","Yinpeng Wu","Jinyu Gu","Zhichao Hua","Yubin Xia","Binyu Zang","Haibo Chen"]
published: "2026-07-01"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2607.00760"
sources: ["https://arxiv.org/abs/2607.00760"]
implementation: "複数LLMをNVIDIA H800上でlong-context serving評価し、attention、decode latency、throughput、memory、LongBench/RULER accuracyを測定。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2607.00760"
arxiv_categories: {primary: "cs.DC", cross_list: ["cs.LG"]}
worker_completed_at: "2026-10-06T12:03:00+09:00"
worker_run_key: "20261006-1130-scheduled-chat-30/r02"
---
## 概要
数十万～百万token級のlong-context servingではKVキャッシュ（KV cache）がGPU memoryを占有し、batch sizeとthroughputを制限する。従来方式はsequence軸のtoken pruningかchannel軸の量子化・低rank化のどちらか一方を主に圧縮する。MosaicKVは両軸を同時に圧縮するが、単純な二重圧縮で精度を落とさないようKV segmentごとに方式を変える。

## 手法
各KV vector内の重要度分布が不均一であることを利用し、cacheをsegmentへ分けて重要要素を識別する。segmentごとにsequence方向とchannel方向の圧縮率・方式を選び、一つのglobal patternを全cacheへ強制しない。

細粒度な2D圧縮はmetadata管理や復元costが増えるため、compressed KV cache managementを導入する。GPUとCPUの余っている計算・memory資源を使って圧縮cacheを維持し、attention kernelが圧縮表現を効率的に読むことで、memory削減を実際のdecode高速化へ変換する。

## 評価条件
|項目|条件|
|---|---|
|用途|extremely long-context LLM serving|
|hardware|NVIDIA H800|
|モデル|複数LLM|
|品質|LongBench、RULER|
|system指標|attention速度、decode latency、throughput、memory|

## 主要結果
非圧縮baselineに対しKV memoryを3倍削減し、attention計算を最大16倍高速化する。end-to-end寄りの指標ではdecode latencyを最大4.8倍短縮し、throughputを最大7.3倍高める。

LongBenchとRULERの平均accuracy lossは1.76%で、sequence/channelを同時に削る高圧縮でも品質低下を小さく抑える。cache容量削減だけでなくH800上のwall-clock serving指標まで測っている点が重要である。

## 既存研究との差・限界
token pruningだけ、またはchannel quantizationだけの一次元圧縮に対し、2Dをsegment単位で適応選択する。管理overheadを別system componentで吸収するmodel-system協調型である。最大倍率は非常に長いcontextで圧縮が効く条件の値で、短contextではmetadata/圧縮管理costにより利得が縮む可能性がある。CPU/GPU余剰資源を利用する設計なのでresource contentionが強いclusterでは再評価が必要である。