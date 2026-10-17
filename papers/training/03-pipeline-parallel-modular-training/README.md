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
## 自動生成の論文一覧（3本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

該当なし。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-08 · [ZeroLock: Concurrent Memory-Efficient LLM Training via Modular Update Decoupling](2026-2608.07974-zerolock-concurrent-memory-efficient-llm-training-via-modular-update-decoupling.md)**  
  実装：[✓](https://anonymous.4open.science/r/unlock_trainer-105B) ・ リポジトリ内被引用：0  
  大規模言語モデルを連続した層群へ分割し、各段の予測分布に局所損失を与えることで段間の逆伝播依存を切る方式。三段の実機試験では、PipeDreamに対する最大段のピークメモリを26.5%削減し、標準条件の処理量を4.9%改善した。ただし、同一段の内部では通常の逆伝播を行い、推論高速化の手法ではない。

### 3年前（2023-11〜2024-10）

- **2023-11 · [Striped Attention: Faster Ring Attention for Causal Transformers](2023-2311.09431-striped-attention.md)**  
  実装：[✓](https://github.com/exists-forall/striped_attention) ・ リポジトリ内被引用：18  
  Ring 注意機構の連続分割を縞状のトークン配置へ変え、因果マスクで省略できる計算を全装置へ均等化して長文Transformer学習を高速化する厳密注意方式。

- **2024-05 · [NeMo-Aligner: Scalable Toolkit for Efficient Model Alignment](2024-2405.01481-nemo-aligner.md)**  
  実装：[✓](https://github.com/NVIDIA/NeMo-Aligner) ・ リポジトリ内被引用：7  
  整合学習の複数モデルを分散配置し、TensorRT-LLM生成・非同期通信・重み再配置を統合して、PPOを1000 GPU級まで拡張する学習基盤。
<!-- survey:auto:end -->
