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

<!-- survey:auto:start -->
## 自動生成の論文一覧（1本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 直近12か月（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-08 | [ZeroLock: Concurrent Memory-Efficient LLM Training via Modular Update Decoupling](2026-2608.07974-zerolock-concurrent-memory-efficient-llm-training-via-modular-update-decoupling.md) | [✓](https://anonymous.4open.science/r/unlock_trainer-105B) | 0 | モデルを複数chunkへ分け、各chunkを局所目的関数で独立更新することで、下流chunkの逆伝播待ちと長時間のactivation保持をなくし、pipeline並列学習のbubble・memory・通信待ちを減らすBP-free fine-tuning system。 |

### 直近12か月より前・リポジトリ内で被引用

該当なし。

### その他

該当なし。
<!-- survey:auto:end -->
