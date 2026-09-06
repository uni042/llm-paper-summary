# 推論システム研究

収録論文: **106本**。

推論・serving・decoding・実行時memory / I/O・on-device実行など、**モデルを使って出力を生成する段階の効率化**を目的とする研究を収録する。

分類は手法内部の実装ではなく最終目的で決める。推論高速化のために予測器の学習、蒸留、追加学習、calibrationなどを使う場合も推論側に置く。

各系統READMEには、その研究系統の説明と、収録する全論文の一文説明を掲載する。一文説明ではLLMの基礎知識は前提としつつ、個別分野でしか通じにくい用語は「何をして何を改善するか」が分かる表現へ言い換える。

## 系統

- [Offload / Hierarchical Memory](01-offload-hierarchical-memory/) — 14本
  - GPUに収まらないmodel weight / expertなどをCPU・peer GPU・SSD・Flashへ置き、転送・協調計算・near-data処理を最適化してmemory容量とI/O待ちを減らす。
- [Adaptive Expert Computation / Compression](02-adaptive-expert-computation-compression/) — 10本
  - token・layer・expertの重要度やcostに応じて、実行するexpert数やexpert自体を変え、MoEの計算量・転送量・model容量を削減する。
- [Expert Prefetch](03-expert-prefetch/) — 12本
  - 将来使うexpertをrouting確定前に予測してGPUへ先読みし、CPU / storageからのweight転送を現在の計算と重ねる。
- [Conditional Computation](04-conditional-computation/) — 8本
  - 入力やtokenの難しさに応じてlayer、token、終了位置を選び、不要なTransformer計算を最初から実行しない。
- [Speculative Decoding × MoE](05-speculative-decoding-moe/) — 6本
  - speculative decodingで増えるMoEのexpert実行・weight転送・verification costを、branch選択やexpert再利用・先読みで抑える。
- [MoE Quantization / Compression](06-moe-quantization-compression/) — 13本
  - expertごとの重要度・利用頻度・量子化耐性に合わせてbit幅やexpert数を調整し、memoryと計算量を減らす。
- [KV Cache Optimization / Compression](07-kv-cache-optimization-compression/) — 7本
  - KV cacheを削除・圧縮・動的budgetingで小さくする、HBM→L2 prefetchでGPU内部のaccess待ちを隠す、またはshared prefixへの重複KV readをまとめて減らす。
- [Edge / On-device LLM Systems](08-edge-on-device-llm-systems/) — 4本
  - smartphoneや個人PCなど制約の強いdeviceで、CPU / GPU / NPU / memoryを協調させてLLMを実用速度で動かす。
- [Other Inference Systems](09-other-inference-systems/) — 2本
  - 推論効率化を主目的とするが、まだ独立系統を作るほど同種研究が集まっていない手法を一時的に収録する。
- [KV Cache Offload / Recomputation](10-kv-cache-offload-recomputation/) — 12本
  - KV cacheをCPU DRAM・peer GPU HBM・storageへ置く、attentionをKVの近くへ移す、またはKV転送を部分再計算・dynamic placementへ置き換えてlocal HBM容量とdata movementを抑える。
- [LLM Serving / Scheduling / Disaggregation](11-llm-serving-scheduling-disaggregation/) — 18本
  - batching・token-budget / chunked-prefill scheduling・SLO-aware queueing・fairness・prefix-locality-aware fairness・application-aware scheduling・stateful session reuse・P/D分離・request migration・serverless startup・global KV共有・elastic resource管理を組み合わせ、servingのlatency / SLO / goodput / costを改善する。
