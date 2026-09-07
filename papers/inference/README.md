# 推論システム研究

収録論文: **115本**。

推論・serving・decoding・実行時memory / I/O・on-device実行など、**modelを使って出力を生成する段階の効率化**を目的とする研究を収録する。

分類は手法内部の実装ではなく最終目的で決める。推論高速化のために予測器の学習、蒸留、追加学習、calibrationなどを使う場合も推論側に置く。

各系統READMEには、その研究系統の説明と、収録する全論文の一文説明を掲載する。Transformer、MoE、KV cacheなどLLMの基礎用語は説明なしで使うが、狭い分野や個別論文でしか通じにくい語は、それを知らなくても手法の動作が分かる文章に言い換える。正式名称を残す場合も、最初の出現で具体的な意味を説明する。

## 系統

- [Offload / Hierarchical Memory](01-offload-hierarchical-memory/) — 14本
  - GPUに収まらないmodel weightやMoE expertなどをCPU・別GPU・SSD・Flashへ置き、data転送とCPU / GPUの分担を工夫して必要VRAMとI/O待ちを減らす。
- [Adaptive Expert Computation / Compression](02-adaptive-expert-computation-compression/) — 10本
  - token・layer・expertの重要度やcostに応じて実行するexpert数や保持するexpertを変え、MoEの計算量・転送量・model容量を削減する。
- [Expert Prefetch](03-expert-prefetch/) — 12本
  - 次に使うexpertをrouting確定前に予測してGPUへ先読みし、CPU / storageからのweight転送を現在の計算と重ねて待ち時間を減らす。
- [Conditional Computation](04-conditional-computation/) — 8本
  - 入力やtokenの難しさに応じて使うlayer・token・終了位置を選び、不要なTransformer計算を最初から実行しない。
- [Speculative Decoding × MoE](05-speculative-decoding-moe/) — 6本
  - speculative decodingで増えるMoE expertの実行・weight転送・verification計算を、branch選択やexpert再利用・先読みで抑える。
- [MoE Quantization / Compression](06-moe-quantization-compression/) — 13本
  - expertごとの重要度・利用頻度・量子化への強さに合わせてbit幅やexpert数を調整し、memoryと計算量を減らす。
- [KV Cache Optimization / Compression](07-kv-cache-optimization-compression/) — 7本
  - KV cacheの不要部分を削る・圧縮する、必要量を動的に変える、GPU内部で先読みする、共有prefixへの重複したKV読み出しをまとめるなどして、memory使用量とaccess待ちを減らす。
- [Edge / On-device LLM Systems](08-edge-on-device-llm-systems/) — 5本
  - smartphoneや個人PCなどresourceが限られたdeviceで、CPU / GPU / NPU / memoryを分担させてLLMを実用速度で動かす。
- [Other Inference Systems](09-other-inference-systems/) — 3本
  - 推論効率化を主目的とするが、まだ独立系統を作るほど同種研究が集まっていない手法を一時的に収録する。
- [KV Cache Offload / Recomputation](10-kv-cache-offload-recomputation/) — 13本
  - KV cacheをCPU DRAM・別GPUのHBM・storageへ置く、attentionをKVの近くへ移す、転送するKVの一部を再計算する、またはSSD I/O制御をGPU側へ移すことで、local HBM使用量とdata transfer / I/O待ちを減らす。
- [LLM Serving / Scheduling / Disaggregation](11-llm-serving-scheduling-disaggregation/) — 24本
  - requestの実行順、batchの組み方、prefill / decodeへのGPU配分、共有prefixやconversation KVの再利用、requestのGPU間移動、GPU数の増減などを調整し、latency・SLOを満たせるrequest数・cost・公平性・利用者の待ち時間を改善する。
