<!-- survey:auto:start -->
## 自動生成の論文一覧（6本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-02 · [DualPath: Breaking the Storage Bandwidth Bottleneck in Agentic LLM Inference](2026-2602.21548-dualpath-storage-bandwidth-agentic-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  プリフィル側だけに集中していたKVキャッシュのストレージ読出しをデコード側NICにも分散し、RDMA転送と負荷認識スケジューリングでエージェント型LLM推論のストレージ帯域ボトルネックを緩和する。

- **2025-10 · [Scalable Processing-Near-Memory for 1M-Token LLM Inference: CXL-Enabled KV-Cache Management Beyond GPU Limits](2025-2511.00321-cxl-pnm-kv-cache.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  CXL-PNMはKVをGPUへ呼び戻さず、CXLメモリ近傍でページ要約・重要度選択・注意を計算する。PnG-KVはGPUも注意を分担し、長文脈のKV転送とGPU容量制約を減らす。

- **2026-06 · [SAC: Disaggregated KV Cache System for Sparse Attention LLMs with CXL](2026-2606.19746-sac-sparse-attention-cxl-disaggregated-kv.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  疎注意で実際に使うtop-k KVだけをCXL共有メモリから層ごとに直接読み込み、RDMAの接頭辞全量転送とローカルKV常駐をなくして長文高並行デコードを高速化する。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Interface-Aware KV Cache Quantization for Dense On-Chip NVM in Long-Context LLM Decoding](2026-2609.05764-interface-aware-kv-quantization-nvm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は固定Hadamard回転・正規化・4ビット符号帳でKVをオンチップNVM向けに量子化し、補助情報と読み出し再構成を減らして長文脈KVの面積・エネルギーを抑える。

- **2026-09 · [Composable CXL Memory as a Kubernetes-Native Shared Memory for LLM Serving](2026-2609.10790-composable-cxl-memory-kubernetes-native-shared-memory-llm-serving.md)**  
  実装：[✓](https://github.com/Seagate) ・ リポジトリ内被引用：0  
  共有CXLメモリをKubernetesの動的資源として割り当て、複数ノードから同じKVキャッシュを再利用して長い接頭辞の初動遅延を5.5〜36.6倍短縮する実現可能性研究。

### 2年前（2024-10〜2025-09）

- **2025-07 · [HGCA: Hybrid GPU-CPU Attention for Long Context LLM Inference](2025-2507.03153-hgca-hybrid-gpu-cpu-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  HGCAは最近のKVをGPUで密注意、古いKVをCPUでヘッド別の疎注意にし、部分出力だけを統合してPCIeでKV全量を戻す待ちを減らす。
<!-- survey:auto:end -->
