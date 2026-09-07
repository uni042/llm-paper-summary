# Pipeline-Parallel / Modular Training Systems

大規模modelを複数stageへ分割して学習すると、stage間のforward / backward依存、microbatchの実行順、activation lifetime、通信、故障時の巻き戻し方がtraining throughputとmemoryを大きく左右する。

この系統では、

- model layerを複数stageへ分割する
- stage間のforward / backward待ちを減らす
- microbatch scheduleを組み替えてpipeline bubbleを減らす
- local objectiveなどでstage間のgradient dependency自体を弱める・切る
- activation保持時間やcross-stage gradient通信を減らす
- stage単位checkpoint / replayでfailure recoveryを軽くする

といった方法で、**pipeline-parallel trainingのGPU idle time、activation memory、stage間通信、recovery costを減らす研究**をまとめる。

CPU DRAMやSSD/NVMeへparameter・optimizer state・activationを退避することが中心なら `01-training-offload-memory-systems/`、MoE expertのGPU配置・複製・all-to-all通信が中心なら `02-distributed-heterogeneous-moe-training/` に分類する。

## 収録論文

収録論文: 1本。公開日が新しい順。

- 2026-08-08 — [ZeroLock: Concurrent Memory-Efficient LLM Training via Modular Update Decoupling](2026-2608.07974-zerolock-concurrent-memory-efficient-llm-training-via-modular-update-decoupling.md)
  - 各model chunkにlocal objectiveを持たせてchunk間のbackward dependencyを切り、forward hidden stateをlocal backwardより先に次stageへ渡す。下流backward待ちのactivation保持とcross-stage gradient通信を減らし、stage単位checkpointで局所復旧も可能にする。
