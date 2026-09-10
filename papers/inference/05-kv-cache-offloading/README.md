<!-- survey:auto:start -->
## 自動生成の論文一覧（2本）

| 論文 | 一文要約 |
|---|---|
| [Interface-Aware KV Cache Quantization for Dense On-Chip NVM in Long-Context LLM Decoding](2026-2609.05764-interface-aware-kv-quantization-nvm.md) | 長文脈LLMのデコードでは、過去トークンのKVキャッシュ全体を各段階で読み出すため、演算量よりメモリ帯域とデータ移動が律速になりやすい。著者らは、KVキャッシュを高密度なオンチップ不揮発メモリ（Non-Volatile メモリ; NVM）へ置く場合、GPU向け量子化の補助情報や疎な外れ値表現が新たな面積・読み出しエネルギー負担になる点に着目する。提案方式はランダム化Hadamard回転とベクトル単位正規化で各座標の値域をそろえ、キー用と値用に固定した4ビット符号帳を全トークンで共有する。各ベクトルにはノルム1個だけを補助情報として残し、NVMの読み出し比較器へ符号帳の閾値を固定設定することで、トークンごとの変換器再設定や群単位のスケール読み出しを不要にする。注意計算そのものはデジタル回路で行い、アナログ交差配列は固定回転だけに限定する。3B〜14Bモデルと最大32K文脈の評価で、KIVIやKVQuantよりソフトウェア上の精度は一部低い一方、同じNVM基盤上のKV読み出しエネルギーを3.1〜3.6倍削減し、KIVI比で補助情報量を8分の1にする。 |
| [Scalable Processing-Near-Memory for 1M-Token LLM Inference: CXL-Enabled KV-Cache Management Beyond GPU Limits](2025-2511.00321-cxl-pnm-kv-cache.md) | 100万トークン級の長文脈推論では、完全なKVキャッシュをCXL拡張メモリへ退避しても、動的選択されたページをGPUへ呼び戻す通信が文脈長とともに増え、GPU側KV容量がバッチ数を制限する。著者らはCXL Type 3メモリに処理近傍メモリ（Processing-Near-メモリ; PNM）アクセラレータを統合し、ページ要約、重要度推定、Top-K選択、注意計算をKVの置かれたLPDDR5X近傍で実行するPNM-KVを提案する。さらに全結合層はGPUのテンソル並列、注意はPNMのデータ並列とし、文脈長に依存しない活性値だけを交換する。GPUの遊休計算も使うPnG-KVでは、時間的に安定して重要な一部KVだけをGPUに保持してGPUとPNMで注意を分担する。Llama 3.1の8B/70B/405B、128K〜1M文脈を対象とした実装・シミュレーション評価で、最大21.9倍のスループット、最大60倍低いトークン当たりエネルギー、最大7.3倍のコスト効率を報告する。 |
<!-- survey:auto:end -->
