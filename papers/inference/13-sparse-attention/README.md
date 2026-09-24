# Sparse Attention

長文脈LLMで全KVへ密に注意を計算せず、重要token・block・page・routeだけを選択してattention演算量とメモリ帯域を減らす疎注意方式をまとめる。

## 分類境界

主要貢献がattention対象token/block/pageの選択、疎なquery-key接続、top-k/route型attention計算削減である論文を含め、KVの圧縮・退避・量子化だけでattention接続を疎化しない研究は含めない。

### 含める研究

- token/block/page選択型の疎attention
- top-k・threshold・route型attention
- 長文脈向けattention計算削減

### 含めない研究

- KV cache圧縮だけを主題とする研究
- KV offloadだけでattention自体は密な研究

## 近傍系統

- [07-kv-cache-optimization-compression](../07-kv-cache-optimization-compression/)
- [11-llm-serving-scheduling-disaggregation](../11-llm-serving-scheduling-disaggregation/)

<!-- survey:auto:start -->
## 自動生成の論文一覧（6本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-07 · [DELTA: Dynamic Layer-Aware Token Attention for Efficient Long-Context Reasoning](2026-delta.md)**  
  実装：[✓](https://github.com/hoenza/DELTA) ・ リポジトリ内被引用：1  
  少数の更新層で重要KVページを動的に選び、後続層がその集合を再利用することで、完全なKV保持と推論精度を維持しつつ長文デコードを高速化する疎注意方式。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [RouteRelay: Event-Triggered Cross-Layer Route Reuse for Efficient Dynamic Sparse Attention](2026-2609.07306-routerelay-cross-layer-route-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動的疎注意の前層経路IDを監視候補付きで再利用し、変化した行だけ再ルーティングして経路スコア計算を約38～52%へ削減するが、現CPU実装は未融合処理で逆に低速。

### 2年前（2024-10〜2025-09）

- **2024-10 · [SeerAttention: Learning Intrinsic Sparse Attention in Your LLMs](2024-2410.13276-seerattention.md)**  
  実装：[✓](https://github.com/microsoft/SeerAttention) ・ リポジトリ内被引用：11  
  Q/Kからブロック単位の重要度を学習する軽量ゲートとブロック疎FlashAttentionを組み合わせ、長文プリフィルの注意計算を動的に削減する。

- **2025-02 · [MoBA: Mixture of Block Attention for Long-Context LLMs](2025-2502.13189-moba.md)**  
  実装：[✓](https://github.com/MoonshotAI/MoBA) ・ リポジトリ内被引用：9  
  MoBAは各問い合わせが関連KVブロックを動的選択するMoE型疎注意で、1M文脈の品質を完全注意に近く保ちつつ注意層前処理を最大6.5倍高速化する。

### 3年前（2023-10〜2024-09）

- **2024-06 · [Quest: Query-Aware Sparsity for Efficient Long-Context LLM Inference](2024-2406.10774-quest.md)**  
  実装：[✓](https://github.com/mit-han-lab/Quest) ・ リポジトリ内被引用：47  
  KVページのキー最小・最大値と現在クエリから重要度上界を推定し、上位ページだけを読むことで全KVを保持したまま長文脈注意の帯域を削減し最大7.03倍高速化。

- **2024-07 · [MInference 1.0: Accelerating Pre-filling for Long-Context LLMs via Dynamic Sparse Attention](2024-2407.02490-minference.md)**  
  実装：[✓](https://github.com/microsoft/MInference) ・ リポジトリ内被引用：24  
  注意ヘッドを3種の疎パターンへ割り当て、入力ごとの重要位置を動的推定して長文脈プリフィルを専用GPUカーネルで高速化する。
<!-- survey:auto:end -->
