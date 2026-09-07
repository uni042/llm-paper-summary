# 推論システム研究

収録論文: **145本**。

推論・serving・decoding・実行時memory / I/O・on-device実行など、**modelを使って出力を生成する段階の効率化**を目的とする研究を収録する。

分類は手法内部の実装ではなく最終目的で決める。推論高速化のために予測器の学習、蒸留、追加学習、calibrationなどを使う場合も推論側に置く。

## 系統

- [Offload / Hierarchical Memory](01-offload-hierarchical-memory/) — 16本 — model weightやMoE expertをCPU・peer GPU・SSD / Flash等へ置き、転送・計算を協調させてGPU memory不足を補う。
- [Adaptive Expert Computation / Compression](02-adaptive-expert-computation-compression/) — 10本 — tokenやlayerごとに実行expert数を変えたりexpertを統合・代替したりして、MoEの計算・転送・容量を減らす。
- [Expert Prefetch](03-expert-prefetch/) — 13本 — 将来使うexpertをrouting確定前に予測してGPUへ先読みし、weight転送待ちを現在の計算へ隠す。
- [Conditional Computation](04-conditional-computation/) — 8本 — layer skipping、early exit、token pruning等で入力に応じて不要なTransformer計算を実行しない。
- [Speculative Decoding / MoE](05-speculative-decoding-moe/) — 11本 — draft候補を並列生成・検証して1回のtarget実行で複数tokenを確定し、MoEではexpert読込・検証costも抑える。
- [MoE Quantization / Compression](06-moe-quantization-compression/) — 13本 — expert weightを低bit化・pruning・mixed precision等で小さくし、VRAM・bandwidth・計算量を削減する。
- [KV Cache Optimization / Compression](07-kv-cache-optimization-compression/) — 9本 — KV cacheを圧縮・選別・動的配分・GPU内prefetchして、容量とmemory bandwidthの負荷を減らす。
- [Edge / On-device LLM Systems](08-edge-on-device-llm-systems/) — 6本 — smartphoneや個人PCなど、memory・bandwidth・電力制約の厳しい端末でLLMを実行するsystem研究。
- [KV Cache Offload / Recomputation](10-kv-cache-offload-recomputation/) — 20本 — KVをCPU・peer GPU・SSD等へ置き、必要な転送・attention実行場所・再計算を最適化する。
- [LLM Serving / Scheduling / Disaggregation](11-llm-serving-scheduling-disaggregation/) — 30本 — request順、batch、prefill / decode分離、KV再利用・移動、GPU配置を調整してserving効率とlatencyを改善する。
- [Other Inference Systems](99-other-inference-systems/) — 7本 — 推論効率化が主目的だが、まだ独立lineageを作るほど同種研究が集まっていない手法を置く。
