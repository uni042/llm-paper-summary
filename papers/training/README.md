# 学習システム研究

収録論文: **16本**。

事前学習、fine-tuning、分散学習、optimizer / activation / parameterのmemory管理など、**modelを学習・更新する工程そのものの効率化**を目的とする研究を収録する。

推論用手法の内部で予測器や補助modelを学習するだけのものはここには置かず、最終目的が推論なら `inference/` に分類する。

各系統READMEには、その研究系統の説明と、収録する全論文の一文説明を掲載する。Transformer、MoE、optimizer stateなどLLM学習で広く使われる基礎用語は説明なしで使うが、狭い分野や個別論文でしか通じにくい語は、それを知らなくても「何を移す・分ける・省く・重ねる手法か」が分かる表現にする。

## 系統

- [Training Offload / Memory Systems](01-training-offload-memory-systems/) — 11本
  - activation、optimizer state、parameterなどをCPU / SSDへ退避し、data転送やoptimizer更新をGPU計算と重ねて、限られたGPU memoryで大規模学習を行う。
- [Distributed / Heterogeneous MoE Training](02-distributed-heterogeneous-moe-training/) — 5本
  - expertの配置・複製・GPU間通信・parallelism・GPU性能差を調整し、多数または性能の異なるGPU上でMoE trainingを効率化する。
