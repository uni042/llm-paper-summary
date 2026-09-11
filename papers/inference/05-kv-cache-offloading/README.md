<!-- survey:auto:start -->
## 自動生成の論文一覧（3本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2025-10 | [Scalable Processing-Near-Memory for 1M-Token LLM Inference: CXL-Enabled KV-Cache Management Beyond GPU Limits](2025-2511.00321-cxl-pnm-kv-cache.md) | ✓ | 2 | 100万トークン級の長文脈推論では、完全なKVキャッシュをCXL拡張メモリへ退避しても、動的選択されたページをGPUへ呼び戻す通信が文脈長とともに増え、GPU側KV容量がバッチ数を制限する。 |

### 直近12か月・未被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-09 | [Interface-Aware KV Cache Quantization for Dense On-Chip NVM in Long-Context LLM Decoding](2026-2609.05764-interface-aware-kv-quantization-nvm.md) | ✓ | 0 | 長文脈LLMのデコードでは、過去トークンのKVキャッシュ全体を各段階で読み出すため、演算量よりメモリ帯域とデータ移動が律速になりやすい。 |

### 1年以上前

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2025-07 | [HGCA: Hybrid GPU-CPU Attention for Long Context LLM Inference](2025-2507.03153-hgca-hybrid-gpu-cpu-attention.md) | ✓ | 2 | 長文LLM推論でKVキャッシュがGPUメモリを超えると、CPUへ退避したKVを注意計算のたびにPCIe経由でGPUへ戻す方式は転送待ちがボトルネックになる。 |
<!-- survey:auto:end -->
