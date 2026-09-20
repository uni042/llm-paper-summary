<!-- survey:auto:start -->
## 自動生成の論文一覧（17本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-03 · [Sparse-dLLM: Accelerating Diffusion LLMs with Dynamic Cache Eviction](2025-2508.02558-sparse-dllm-dynamic-cache-eviction.md)**  
  実装：[✓](https://github.com/OpenMOSS/Sparse-dLLM) ・ リポジトリ内被引用：3  
  拡散型LLMの安定した注意重要度を利用した遅延双方向鍵値破棄で、長文脈推論を最大10倍高速化する。

- **2026-03 · [Low-Latency Edge LLM Handover via Joint KV Cache Transfer and Token Prefill](2026-2603.28018-edge-llm-handover-kv-transfer-prefill.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Edge LLM移動時にプリフィル再計算するprefix長と残余KVのbackhaul転送を共同最適化し、複数UEの最悪ハンドオーバ停止時間を最小化する。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Shared KV Caching for Replicated 27B Inference: Correctness Failures and Performance Boundaries](2026-2609.15021-shared-kv-caching-replicated-27b-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共有KVキャッシュのページ表現・CUDAストリーム順序・全容量ピン留めを段階検証し、レプリカ移動時だけ大きな長文プリフィル再利用効果が得られる境界を実測する。

- **2026-09 · [Grouped Value Attention: Efficient KV Caching via On-Demand Key Reconstruction](2026-2609.13285-grouped-value-attention-efficient-kv-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  値だけをKVキャッシュへ保存し、内容キーを値から再構成してクエリ側へ吸収することで、GQAに近い精度を保ちながら永続キャッシュを約45〜47%削減する注意機構。

- **2026-09 · [Contiguity, Not Importance: Budgeted Repair of Stale KV Caches After Document Edits](2026-2609.17983-contiguity-budgeted-repair-stale-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文書編集で古くなったKVは重要位置の散発再計算より編集直後を連続再計算する方が有効で、隣接依存なら13〜21倍高速にほぼ完全修復する。

- **2026-09 · [AgentKV: Phase-Aware KV Eviction for Agentic LLMs](2026-2609.14872-agentkv-phase-aware-kv-eviction-agentic-llms.md)**  
  実装：[✓](https://github.com/LiuTaowen-Tony/agentkv) ・ リポジトリ内被引用：0  
  思考・行動・ツール応答など段階別の問い合わせ履歴でKV重要度を評価し、エージェントの段階遷移で必要になる古い状態を残しつつ、物理ページ圧縮で最大1.80倍の出力スループットを得る。

- **2026-07 · [InferScale: GPU-Native KV Injection for Personalized LLM Serving](2026-2607.27090-inferscale-gpu-native-kv-injection.md)**  
  実装：[✓](https://github.com/saltsystemslab/InferScale) ・ リポジトリ内被引用：0  
  検索メモリのRoPE適用前KVをGPU上で再利用・位置再配置してvLLMへ直接注入し、k=50でTTFTを72〜79%削減する。

- **2026-07 · [GroupKV: Hierarchical KV Cache Management for Long-Context Diffusion LLM Inference](2026-2609.17573-groupkv-hierarchical-kv-cache-diffusion-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散型LLMの長文KVを連続グループ単位で疎選択し、層間予測先読みと古さ補正を組み合わせてCPU退避時の転送量と待ち時間を削減する。

- **2026-05 · [Dynamic-dLLM: Dynamic Cache-Budget and Adaptive Parallel Decoding for Training-Free Acceleration of Diffusion LLM](2026-2606.26120-dynamic-dllm-cache-budget-parallel-decoding.md)**  
  実装：[✓](https://github.com/TianyiWu233/DYNAMIC-DLLM) ・ リポジトリ内被引用：0  
  層別キャッシュ更新量とトークン別確定基準を動的化し、追加学習なしで最大4.48倍の拡散型LLM推論高速化を実現する。

### 2年前（2024-10〜2025-09）

- **2025-05 · [Fast-dLLM: Training-free Acceleration of Diffusion LLM by Enabling KV Cache and Parallel Decoding](2025-2505.22618-fast-dllm-kv-cache-parallel-decoding.md)**  
  実装：[✓](https://github.com/NVlabs/Fast-dLLM) ・ リポジトリ内被引用：10  
  ブロック単位の近似鍵・値キャッシュと確信度に基づく並列復号を組み合わせ、拡散型LLMを再学習なしで最大27.6倍高速化する。

- **2025-05 · [dLLM-Cache: Accelerating Diffusion Large Language Models with Adaptive Caching](2025-2506.06295-dllm-cache-adaptive-caching.md)**  
  実装：[✓](https://github.com/maomaocun/dLLM-cache) ・ リポジトリ内被引用：8  
  プロンプトの長間隔キャッシュとV類似度による応答トークン選択更新で、拡散LLM推論の再計算を学習なしに削減する。

- **2025-05 · [dKV-Cache: The Cache for Diffusion Language Models](2025-2505.15781-dkv-cache-delayed-kv-diffusion-language-models.md)**  
  実装：[✓](https://github.com/horseee/dKV-Cache) ・ リポジトリ内被引用：8  
  DLMの復号済みトークンK/Vを1ステップ遅延して再利用し、未確定位置だけを再計算することで、学習なしに2〜10倍級の推論高速化を実現する。

- **2025-09 · [d²Cache: Accelerating Diffusion-Based LLMs via Dual Adaptive Caching](2025-2509.23094-d2cache-dual-adaptive-caching-diffusion-llm.md)**  
  実装：[✓](https://github.com/Kamichanw/d2Cache) ・ リポジトリ内被引用：2  
  確定性事前分布と注意影響度で更新対象トークンを細粒度選択し、拡散LLMのKV再計算を削減しながら生成品質も改善する。

- **2025-03 · [Oaken: Fast and Efficient LLM Serving with Online-Offline Hybrid KV Cache Quantization](2025-2503.18599-oaken-hybrid-kv-cache-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  KV外れ値の境界だけをオフライン学習し、オンライン3群量子化と専用DMA量子化・メモリ管理器を共同設計して、大規模バッチのKV帯域・容量を同時に削減する。

### 3年前（2023-10〜2024-09）

- **2024-06 · [InfiniGen: Efficient Generative Inference of Large Language Models with Dynamic KV Cache Management](2024-2406.19707-infinigen-dynamic-kv-cache-management.md)**  
  実装：[✓](https://github.com/snu-comparch/InfiniGen) ・ リポジトリ内被引用：11  
  CPU側の全KVキャッシュから次レイヤーで重要なトークンだけを予測してGPUへ先読みし、長文オフロード推論のPCIe転送を削減して最大3.00倍高速化する。

- **2024-05 · [You Only Cache Once: Decoder-Decoder Architectures for Language Models](2024-2405.05254-yoco.md)**  
  実装：[✓](https://aka.ms/YOCO) ・ リポジトリ内被引用：3  
  自己デコーダが一度だけ生成した大域鍵値を後半の交差デコーダ全層で共有し、長文脈の鍵値メモリと事前充填時間を桁違いに削減する。

- **2024-05 · [Reducing Transformer Key-Value Cache Size with Cross-Layer Attention](2024-2405.12981-cross-layer-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  MQA/GQAのKV共有を層方向へ拡張し、隣接層でKV活性を再利用してKVキャッシュを追加で約2倍削減する注意アーキテクチャ。
<!-- survey:auto:end -->
