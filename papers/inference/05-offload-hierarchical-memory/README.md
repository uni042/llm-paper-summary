<!-- survey:auto:start -->
## 自動生成の論文一覧（2本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-08 · [HBF Sucks? A Full-Stack Characterization of High-Bandwidth Flash for KV-Centric LLM Serving](2026-2608.11668-high-bandwidth-flash-kv-serving-characterization.md)**  
  実装：[✓](https://github.com/pku-lemonade/TokenSim) ・ リポジトリ内被引用：1  
  SSD型KV退避の保存先だけをHBFへ置換すると、近接メモリ減少・書込主体化・熱／耐久制約が利点を上回り、遅延が2〜5.5倍悪化することを本番トレースで示す。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [AutoUVM: Automated Prefetching Framework for LLMs under UVM Oversubscription](2026-2609.06172-autouvm-automated-prefetching-uvm-oversubscription.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PyTorch内部のテンソル意味情報をUVM先読みに持ち込み、必要テンソルだけを選択的にCPU→GPU移送して標準UVM比平均3.1倍高速化する。
<!-- survey:auto:end -->
