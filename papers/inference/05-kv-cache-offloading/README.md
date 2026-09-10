<!-- survey:auto:start -->
## 自動生成の論文一覧（1本）

| 論文 | 一文要約 |
|---|---|
| [Scalable Processing-Near-Memory for 1M-Token LLM Inference: CXL-Enabled KV-Cache Management Beyond GPU Limits](2025-2511.00321-cxl-pnm-kv-cache.md) | 100万トークン級の長文脈推論では、完全なKVキャッシュをCXL拡張メモリへ退避しても、動的選択されたページをGPUへ呼び戻す通信が文脈長とともに増え、GPU側KV容量がバッチ数を制限する。著者らはCXL Type 3メモリに処理近傍メモリ（Processing-Near-メモリ; PNM）アクセラレータを統合し、ページ要約、重要度推定、Top-K選択、注意計算をKVの置かれたLPDDR5X近傍で実行するPNM-KVを提案する。さらに全結合層はGPUのテンソル並列、注意はPNMのデータ並列とし、文脈長に依存しない活性値だけを交換する。GPUの遊休計算も使うPnG-KVでは、時間的に安定して重要な一部KVだけをGPUに保持してGPUとPNMで注意を分担する。Llama 3.1の8B/70B/405B、128K〜1M文脈を対象とした実装・シミュレーション評価で、最大21.9倍のスループット、最大60倍低いトークン当たりエネルギー、最大7.3倍のコスト効率を報告する。 |
<!-- survey:auto:end -->
