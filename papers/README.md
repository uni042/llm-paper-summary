# 論文カタログ

収録論文: **387本**。

論文は **Inference（推論）**、**Training（学習）**、**Survey（サーベイ／レビュー）** の3系統に分け、その下を研究系統別に整理する。Training側は既存19本を保持したまま更新を凍結している。Survey側は個別の新規手法ではなく、複数研究を横断整理するsurvey / review論文を収録する。

各研究系統ディレクトリのREADMEにある論文一覧は、公開年月ベースの **直近12か月** → **それ以前でリポジトリ内の別論文から引用されている論文** → **その他** の順に、重複なしで自動分類する。一覧には公開年月、明示的な実装有無、リポジトリ内被引用数、一文要約を表示する。

## Inference / 推論 — 363本

- [Offload / Hierarchical Memory](inference/01-offload-hierarchical-memory/) — 36本 — model weightやMoE expertをCPU・peer GPU・SSD / Flash等へ置き、転送・計算を協調させてGPU memory不足を補う。
- [Adaptive Expert Computation / Compression](inference/02-adaptive-expert-computation-compression/) — 14本 — tokenやlayerごとに実行expert数を変えたりexpertを統合・代替したりして、MoEの計算・転送・容量を減らす。
- [Expert Prefetch](inference/03-expert-prefetch/) — 14本 — 将来使うexpertをrouting確定前に予測し、GPU cacheの保持や先読みを制御してweight転送待ち・転送量を減らす。
- [Conditional Computation](inference/04-conditional-computation/) — 9本 — layer skipping、early exit、token pruning等で入力に応じて不要なTransformer計算を実行しない。
- [Speculative Decoding / MoE](inference/05-speculative-decoding-moe/) — 17本 — draft候補を並列生成・検証して1回のtarget実行で複数tokenを確定し、MoEではexpert読込・検証costも抑える。
- [MoE Quantization / Compression](inference/06-moe-quantization-compression/) — 14本 — expert weightを低bit化・pruning・mixed precision等で小さくし、VRAM・bandwidth・計算量を削減する。
- [KV Cache Optimization / Compression](inference/07-kv-cache-optimization-compression/) — 26本 — KV cacheを圧縮・選別・動的配分・GPU内prefetchして、容量とmemory bandwidthの負荷を減らす。
- [Edge / On-device LLM Systems](inference/08-edge-on-device-llm-systems/) — 14本 — smartphoneや個人PCなど、memory・bandwidth・電力制約の厳しい端末でLLMを実行するsystem研究。
- [KV Cache Offload / Recomputation](inference/10-kv-cache-offload-recomputation/) — 61本 — KVをCPU・peer GPU・SSD等へ置き、必要な転送・attention実行場所・再計算を最適化する。
- [LLM Serving / Scheduling / Disaggregation](inference/11-llm-serving-scheduling-disaggregation/) — 108本 — request順、batch、prefill / decode分離、KV再利用・移動、GPU配置を調整してserving効率とlatencyを改善する。
- [Other Inference Systems](inference/99-other-inference-systems/) — 9本 — 推論効率化が主目的だが、まだ独立lineageを作るほど同種研究が集まっていない手法を置く。

→ [Inference一覧](inference/)

## Training / 学習 — 19本（凍結）

既存内容を参照用として保持するが、通常サーベイでは新規追加・監査・本文更新を行わない。

→ [Training一覧](training/)

## Survey / サーベイ — 5本

複数研究を横断的に整理するsurvey / review論文を独立して収録する。現時点では既存収録論文から高確度にsurvey / reviewと判定できるものはないため、カテゴリのみ先に作成している。

→ [Survey一覧](survey/)

<!-- survey:auto:start -->
推論：**363本** ／ 学習：**19本** ／ サーベイ：**5本**。 [推論一覧](inference/README.md) ／ [学習一覧](training/README.md) ／ [サーベイ一覧](survey/README.md) ／ [研究比較](inference/comparison.md)
<!-- survey:auto:end -->
