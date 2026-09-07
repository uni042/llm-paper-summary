# 論文カタログ

収録論文: **141本**。

論文はまず最終目的で **Inference（推論）** と **Training（学習）** に分け、その下を研究系統別に整理する。各系統READMEには、**その系統が何を効率化する研究群かという説明**と、**収録する全論文の一文説明**を掲載する。

Transformer、MoE、KV cache、quantization、speculative decodingなどLLMの基礎知識は説明なしで使う。一方、特定論文・狭い研究領域でしか通じにくい名称や略語は、それだけで説明を終えない。最初に出す時点で「何をどう変える仕組みか」を説明し、できるだけ**何の計算・転送・memory使用量・待ち時間を減らすのか**が分かる表現にする。この方針は一文説明だけでなく各論文本文にも適用する。

## Inference / 推論 — 122本

- [Offload / Hierarchical Memory](inference/01-offload-hierarchical-memory/) — 14本
- [Adaptive Expert Computation / Compression](inference/02-adaptive-expert-computation-compression/) — 10本
- [Expert Prefetch](inference/03-expert-prefetch/) — 13本
- [Conditional Computation](inference/04-conditional-computation/) — 8本
- [Speculative Decoding × MoE](inference/05-speculative-decoding-moe/) — 6本
- [MoE Quantization / Compression](inference/06-moe-quantization-compression/) — 13本
- [KV Cache Optimization / Compression](inference/07-kv-cache-optimization-compression/) — 7本
- [Edge / On-device LLM Systems](inference/08-edge-on-device-llm-systems/) — 5本
- [KV Cache Offload / Recomputation](inference/10-kv-cache-offload-recomputation/) — 18本
  - KV cacheをCPU DRAM・別GPU HBM・storageへ置く、CPU上のKVから必要subsetだけを検索する、attentionをKVの近くへ移す、CPU attentionを前倒しする、再計算へ置き換える、複数SSDの並列I/Oを使う、またはHBM/DRAM/SSDを協調管理してlocal HBM容量と転送・計算待ちを減らす。
- [LLM Serving / Scheduling / Disaggregation](inference/11-llm-serving-scheduling-disaggregation/) — 25本
- [Other Inference Systems](inference/99-other-inference-systems/) — 3本

→ [Inference一覧](inference/)

## Training / 学習 — 19本

- [Training Offload / Memory Systems](training/01-training-offload-memory-systems/) — 13本
  - activation、optimizer state、parameterなどをCPU / SSDへ退避する方式に加え、CPU DRAMを状態の正本としてGPUへ必要な層だけを流す方式も扱う。転送・更新をGPU計算と重ね、限られたGPU memoryで大規模学習を行う。
- [Distributed / Heterogeneous MoE Training](training/02-distributed-heterogeneous-moe-training/) — 5本
  - expertの配置・複製・GPU間通信・parallelism・GPU性能差を調整し、多数または異種GPU上でMoE trainingを効率化する。
- [Pipeline-Parallel / Modular Training Systems](training/03-pipeline-parallel-modular-training/) — 1本
  - modelをstageへ分割したtrainingで、実行順、stage間dependency、activation lifetime、通信、checkpoint / replayを変え、pipeline bubble・memory・待ち時間・recovery costを減らす。

→ [Training一覧](training/)

## 分類ルール

分類は「手法の中で何を使うか」ではなく、**最終的に何を効率化する研究か**で決める。

- 推論・serving・decodingを高速化するために、予測器の学習、蒸留、追加学習、calibrationなどを使う場合 → `inference/`
- 事前学習、fine-tuning、optimizer update、分散学習そのものを効率化する場合 → `training/`
- 学習・推論の両方へ適用できる場合 → 論文の主目的、主要評価、主要metricを優先して分類する

研究系統は固定しない。独立した問題設定・主要技術・評価軸を持つ論文群が増えた場合は、適宜新しい系統を追加・分割・統合する。
