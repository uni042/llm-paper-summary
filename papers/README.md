# 論文カタログ

収録論文: **124本**。

論文はまず最終目的で **Inference（推論）** と **Training（学習）** に分け、その下を研究系統別に整理する。各系統READMEには、**その系統が何を効率化する研究群かという説明**と、**収録する全論文の一文説明**を掲載する。

一文説明ではTransformer、MoE、KV cache、quantization、speculative decodingなどLLMの基礎知識は説明なしで使う。一方、特定論文・狭い研究領域でしか通じにくい名称はそのまま並べず、できるだけ「何をどう変えて、何を減らす・改善するのか」が分かる表現へ言い換える。

## Inference / 推論 — 108本

- [Offload / Hierarchical Memory](inference/01-offload-hierarchical-memory/) — 14本
  - GPUに収まらないmodel weight / expertなどをCPU・peer GPU・SSD・Flashへ置き、転送・協調計算・near-data処理を最適化してmemory容量とI/O待ちを減らす。
- [Adaptive Expert Computation / Compression](inference/02-adaptive-expert-computation-compression/) — 10本
  - token・layer・expertの重要度やcostに応じて、実行するexpert数やexpert自体を変え、MoEの計算量・転送量・model容量を削減する。
- [Expert Prefetch](inference/03-expert-prefetch/) — 12本
  - 将来使うexpertをrouting確定前に予測してGPUへ先読みし、CPU / storageからのweight転送を現在の計算と重ねる。
- [Conditional Computation](inference/04-conditional-computation/) — 8本
  - 入力やtokenの難しさに応じてlayer、token、終了位置を選び、不要なTransformer計算を実行しない。
- [Speculative Decoding × MoE](inference/05-speculative-decoding-moe/) — 6本
  - speculative decodingで増えるMoEのexpert実行・weight転送・verification costを、branch選択やexpert再利用・先読みで抑える。
- [MoE Quantization / Compression](inference/06-moe-quantization-compression/) — 13本
  - expertごとの重要度・利用頻度・量子化耐性に合わせてbit幅やexpert数を調整し、memoryと計算量を減らす。
- [KV Cache Optimization / Compression](inference/07-kv-cache-optimization-compression/) — 7本
  - KV cacheを削除・圧縮・動的budgetingで小さくする、HBM→L2 prefetchでGPU内部のaccess待ちを隠す、またはshared prefixへの重複KV readをまとめて減らす。
- [Edge / On-device LLM Systems](inference/08-edge-on-device-llm-systems/) — 4本
  - smartphoneや個人PCなど制約の強いdeviceで、CPU / GPU / NPU / memoryを協調させてLLMを実行する。
- [Other Inference Systems](inference/09-other-inference-systems/) — 2本
  - 推論効率化を主目的とするが、まだ独立系統を作るほど同種研究が集まっていない手法を一時的に収録する。
- [KV Cache Offload / Recomputation](inference/10-kv-cache-offload-recomputation/) — 12本
  - KV cacheをCPU DRAM・peer GPU HBM・storageへ置く、attentionをKVの近くへ移す、またはKV転送を部分再計算・dynamic placementへ置き換えてlocal HBM容量とdata movementを抑える。
- [LLM Serving / Scheduling / Disaggregation](inference/11-llm-serving-scheduling-disaggregation/) — 20本
  - batching・token-budget / chunked-prefill scheduling・predictive job-size scheduling・SLO-aware queueing・fairness・prefix-locality-aware routing / fairness・application-aware scheduling・stateful session reuse・P/D分離・request migration・serverless startup・global KV共有・elastic resource管理を組み合わせ、servingのlatency / SLO / goodput / costを改善する。

→ [Inference一覧](inference/)

## Training / 学習 — 16本

- [Training Offload / Memory Systems](training/01-training-offload-memory-systems/) — 11本
  - activation、optimizer state、parameterなどをCPU / SSDへ退避し、転送・更新をGPU計算と重ねて限られたGPU memoryで大規模学習を行う。
- [Distributed / Heterogeneous MoE Training](training/02-distributed-heterogeneous-moe-training/) — 5本
  - expert配置・複製・通信・parallelism・GPU性能差を調整し、多数または異種GPU上でMoE trainingを効率化する。

→ [Training一覧](training/)

## 分類ルール

分類は「手法の中で何を使うか」ではなく、**最終的に何を効率化する研究か**で決める。

- 推論・serving・decodingを高速化するために、予測器の学習、蒸留、追加学習、calibrationなどを使う場合 → `inference/`
- 事前学習、fine-tuning、optimizer update、分散学習そのものを効率化する場合 → `training/`
- 学習・推論の両方へ適用できる場合 → 論文の主目的、主要評価、主要metricを優先して分類する

研究系統は固定しない。独立した問題設定・主要技術・評価軸を持つ論文群が増えた場合は、適宜新しい系統を追加・分割・統合する。
