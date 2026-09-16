<!-- survey:auto:start -->
## 自動生成の論文一覧（2本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-01 · [RAPID-Serve: Resource-efficient and Accelerated P/D Intra-GPU Disaggregation](2026-2601.11822-rapid-serve-intra-gpu-pd-disaggregation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  同一GPU内でプリフィル/デコードを非lockstep並行実行し、共有KVとCU maskingでSLOと利用率を両立、MI300X実機で有効スループット平均4.9倍を報告。

- **2025-11 · [DOPD: A Dynamic PD-Disaggregation Architecture for Maximizing Goodput in LLM Inference Serving](2025-2511.20982-dopd-dynamic-pd-disaggregation.md)**  
  実装：[✓](https://github.com/liao4s/DOPD) ・ リポジトリ内被引用：0  
  負荷予測と解析的な最適P/D比でプリフィル/デコード instanceを動的再構成し、8x H100実機で有効スループット最大1.5倍・SLO達成99.4%を報告。
<!-- survey:auto:end -->
