# 学習システム研究

収録論文: **16本**。

事前学習、fine-tuning、分散学習、optimizer / activation / tensor memory管理など、**モデルを学習・更新する工程そのものの効率化**を目的とする研究を収録する。

推論用手法の内部で予測器や補助modelを学習するだけのものはここには置かず、最終目的が推論なら `inference/` に分類する。

各系統READMEには、その研究系統の説明と、収録する全論文の一文説明を掲載する。一文説明ではLLMの基礎知識は前提としつつ、個別分野でしか通じにくい用語は「何をして何を改善するか」が分かる表現へ言い換える。

## 系統

- [Training Offload / Memory Systems](01-training-offload-memory-systems/) — 11本
  - activation、optimizer state、parameterなどをCPU / SSDへ退避し、転送・更新をGPU計算と重ねて限られたGPU memoryで大規模学習を行う。
- [Distributed / Heterogeneous MoE Training](02-distributed-heterogeneous-moe-training/) — 5本
  - expert配置・複製・通信・parallelism・GPU性能差を調整し、多数または異種GPU上でMoE trainingを効率化する。
