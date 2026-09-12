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

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-08 · [ZeroLock: Concurrent Memory-Efficient LLM Training via Modular Update Decoupling](2026-2608.07974-zerolock-concurrent-memory-efficient-llm-training-via-modular-update-decoupling.md)**  
  実装：[✓](https://anonymous.4open.science/r/unlock_trainer-105B) ・ リポジトリ内被引用：0  
  モデルを複数チャンクへ分け、各チャンクを局所目的関数で独立更新して下流の逆伝播待ちと下流更新中の長時間の活性値保持を減らし、パイプライン並列のメモリ・通信・バブルを減らす微調整方式。

### 1年以上前

該当なし。
<!-- survey:auto:end -->
