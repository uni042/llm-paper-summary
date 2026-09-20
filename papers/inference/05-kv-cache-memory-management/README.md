<!-- survey:auto:start -->
## 自動生成の論文一覧（8本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-07 · [C²KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference](2026-2607.17715-c2kv-compressed-composable-kv-cache-reuse.md)**  
  実装：[✓](https://github.com/s7a9/C2KV) ・ リポジトリ内被引用：1  
  文書ごとに位置非依存で直接連結できる圧縮KVを学習抽出し、非prefix再利用のプリフィル削減とKV保存・転送・デコード帯域削減を同時に狙う。

- **2025-12 · [MEPIC: Memory Efficient Position Independent Caching for LLM Serving](2025-2512.16822-mepic-position-independent-chunk-kv-sharing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  位置非依存KVをページ境界へ正規配置し、最初の1ブロックだけ再計算、RoPEを注意時に融合することで、同一チャンクのHBMページを要求間共有し、既存PICよりHBM重複と再計算を大幅に減らす。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-08 · [More GPUs or a Smaller Cache? Tensor Parallelism versus KV Compression for Memory-Bound LLM Serving](2026-2608.23962-tensor-parallelism-versus-kv-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像処理装置追加と鍵値圧縮を百万トークン当たり費用で直接比較し、重みが単一装置へ収まる範囲では圧縮が一・二〜二倍安いことを示す。

- **2026-07 · [VarRate: Training-Free Variable-Rate KV Cache Compression for Long-Context LLMs](2026-2607.15498-varrate-training-free-variable-rate-kv-cache-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークンを削除せず、注意顕著度に応じて各トークンの低ランク表現へ可変容量を配る学習不要KV圧縮で、20%メモリ予算でもLongBench平均を非圧縮から0.8点以内に保ち、再利用時の不可逆削除崩壊を抑える。

- **2026-04 · [DASH-KV: Accelerating Long-Context LLM Inference via Asymmetric KV Cache Hashing](2026-2604.19351-dash-kv-asymmetric-hashing-long-context.md)**  
  実装：[✓](https://github.com/Zhihan-Zh/DASH-KV) ・ リポジトリ内被引用：0  
  注意の全キー内積を学習済み非対称ハッシュ検索へ置換し、重要トークンだけ完全精度へ戻すことで、長文脈の計算量を線形化しつつLongBench品質をFull 注意機構近傍に維持する。

### 2年前（2024-10〜2025-09）

- **2025-07 · [Krul: Efficient State Restoration for Multi-turn Conversations with Dynamic Cross-layer KV Sharing](2025-2507.08045-krul-dynamic-cross-layer-kv-restoration.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  対話ごとの注意類似度から層間の鍵・値共有を動的選択し、注意類似度計算を中央処理装置と画像処理装置へ分担、圧縮後の再計算とロードを層間パイプラインで重畳してマルチターン状態復元を高速・省容量化する。

### 3年前（2023-10〜2024-09）

- **2024-07 · [vTensor: Flexible Virtual Tensor Management for Efficient LLM Serving](2024-2407.15309-vtensor-virtual-memory-management.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  CUDA仮想メモリ管理でKVの物理配置を通常テンソル風の連続仮想アドレスから切り離し、ページ化注意専用カーネルを不要にして、vLLM比平均1.86倍高速化しつつA100で平均57GBを他用途へ解放するメモリ管理方式。

### 4年前（2022-10〜2023-09）

- **2023-09 · [Efficient Streaming Language Models with Attention Sinks](2023-2309.17453-streamingllm.md)**  
  実装：[✓](https://github.com/mit-han-lab/streaming-llm) ・ リポジトリ内被引用：84  
  先頭数トークンを注意シンクとして固定保持し、直近トークンだけをローリングKVキャッシュに残すことで、再学習なしに一定メモリで400万トークン超のストリーミング生成を安定化する。
<!-- survey:auto:end -->
