# Adaptive Expert Computation / Compression

MoEで毎回同じ数のexpertを実行するのではなく、**token・layer・expertの重要度や実行コストに応じて、実際に使うexpert数やexpert構成を変える**研究をまとめる。簡単なtokenではexpert計算を減らし、重要なtokenやlayerには多くの計算を割り当てるほか、役割が似たexpertを統合したり、GPUにないexpertを似た常駐expertで代替したりして、品質低下を抑えながら計算量・転送量・モデル容量を減らす。

`Expert Prefetch` が「この先必要になるexpertを予測して早めにGPUへ用意する」ことを主眼とするのに対し、この系統は**そもそもどのexpertを何個実行するか、あるいはexpert構成そのものをどう小さくするか**が中心となる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（14本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-04 · [Alloc-MoE: Budget-Aware Expert Activation Allocation for Efficient Mixture-of-Experts Inference](2026-2604.08133-alloc-moe-budget-aware-expert-activation-allocation-for-efficient-mixture-of-exp.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Alloc-MoEは全層・全トークンの専門家実行回数を総予算として、層の重要度とルータ確信度に応じて配分し、固定Top-kより少ない計算で品質を保つ。

- **2025-11 · [BuddyMoE: Exploiting Expert Redundancy to Accelerate Memory-Constrained Mixture-of-Experts Inference](2025-2511.10054-buddymoe-exploiting-expert-redundancy-to-accelerate-memory-constrained-mixture-o.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  BuddyMoEはルータの共活性統計から常駐専門家を代替候補に選び、GPUキャッシュミス時のCPU重み転送を省いて、品質低下との交換でMoE推論を高速化する。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Training-Free Halving of Activated Experts in Fine-Grained Mixture-of-Experts Models](2026-2609.04575-training-free-halving-activated-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は実行する専門家数k1とルータ正規化集合k2を分離し、k2を保ったままk1だけ半減して、細粒度MoEの計算削減とルータ利得を両立する学習不要手法。

- **2026-09 · [Distribution-Consistent Inference for Dynamic Sparse Mixture-of-Experts](2026-2609.09241-distribution-consistent-dynamic-sparse-moe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動的MoE推論で専門家数を減らすと出力分散と尺度が増える問題を特定し、層・次元ごとの平均と分散を学習時分布へ戻す軽量補正で、同じ専門家予算の精度を大幅に回復する。

- **2026-09 · [ACE: Adaptive Calibration-Free Expert Skipping for MoE-based LLMs](2026-2609.05228-ace.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ACEはルータ重みと専門家変換能力の事前統計を組み合わせ、Top-k内でも寄与の小さいスロットだけをトークン単位で省く。元重みとTop-1を保ち、追加学習なしでFFN計算を減らす。

- **2026-06 · [Beyond Uniform Experts: Cost-Aware Expert Execution for Efficient Multi-Device MoE Inference](2026-2606.29982-beyond-uniform-experts-cost-aware-expert-execution-for-efficient-multi-device-mo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CAEEはルータ寄与と転送・実行コストを見て、層全体を待たせる遅いデバイスの低寄与専門家を省き、その重みを実行済み専門家へ再配分して分散MoEを高速化する。

- **2026-05 · [ReMoE: Boosting Expert Reuse through Router Fine-Tuning in Memory-Constrained MoE LLM Inference](2026-2605.27081-remoe-router-finetuning-expert-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ReMoEはルータだけを追加学習し、直前トークンで使った専門家へ確率を寄せて再利用を増やし、端末MoEのキャッシュミスと低速階層からの重み再読込を減らす。

### 2年前（2024-10〜2025-09）

- **2024-10 · [ExpertFlow: Efficient Mixture-of-Experts Inference via Predictive Expert Caching and Token Scheduling](2024-2410.17954-expertflow-efficient-mixture-of-experts-inference-via-predictive-expert-caching-.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  ExpertFlowは数層先の専門家利用を予測し、同じ経路のトークンをまとめ、層ごとのGPUキャッシュ容量も再配分してCPUからの重み転送待ちを隠す。

- **2025-09 · [LExI: Layer-Adaptive Active Experts for Efficient MoE Model Inference](2025-2509.02753-lexi-layer-adaptive-active-experts-for-efficient-moe-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  LExIは層ごとのTop-k削減による出力変化を合成入力で測り、影響の小さい層の専門家数を減らして重要層へ予算を回し、固定Top-kの計算を減らす。

- **2024-10 · [MoE++: Accelerating Mixture-of-Experts Methods with Zero-Computation Experts](2024-2410.07348-moe-accelerating-mixture-of-experts-methods-with-zero-computation-experts.md)**  
  実装：[✓](https://github.com/SkyworkAI/MoE-plus-plus) ・ リポジトリ内被引用：0  
  MoE++は無計算・入力コピー・学習済み定数の軽量専門家を通常FFNと同じ候補に混ぜ、トークンごとに代替経路を選んでFFN計算を減らす。

### 3年前（2023-10〜2024-09）

- **2024-02 · [Not All Experts are Equal: Efficient Expert Pruning and Skipping for Mixture-of-Experts Large Language Models](2024-2402.14800-not-all-experts-are-equal-efficient-expert-pruning-and-skipping-for-mixture-of-e.md)**  
  実装：[✓](https://github.com/Lucky-Lance/Expert_Sparsity) ・ リポジトリ内被引用：20  
  本研究は校正データで冗長な専門家を恒久削除し、実行時はルータ寄与の小さい第2専門家をトークン単位で省いて、Mixtralの常駐メモリとFFN計算を減らす。

- **2023-10 · [Merge, Then Compress: Demystify Efficient SMoE with Hints from Its Routing Policy](2023-2310.01334-merge-then-compress-demystify-efficient-smoe-with-hints-from-its-routing-policy.md)**  
  実装：[✓](https://github.com/UNITES-Lab/MC-SMoE) ・ リポジトリ内被引用：7  
  MC-SMoEはルータ履歴で似た専門家を代表へ統合し、統合重みを低ランク成分と疎な残差へ圧縮して、専門家数とメモリ使用量を減らす。

- **2024-02 · [XMoE: Sparse Models with Fine-grained and Adaptive Expert Selection](2024-2403.18926-xmoe-sparse-models-with-fine-grained-and-adaptive-expert-selection.md)**  
  実装：[✓](https://github.com/ysngki/XMoE) ・ リポジトリ内被引用：3  
  XMoEはFFNを細粒度専門家に分割し、ルータ確率の累積が閾値に達するまでトークンごとに選ぶ数を変えて、確信度に応じた計算量配分で固定Top-kの無駄を減らす。

- **2024-06 · [AdaMoE: Token-Adaptive Routing with Null Experts for Mixture-of-Experts Language Models](2024-2406.13233-adamoe-token-adaptive-routing-with-null-experts-for-mixture-of-experts-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  AdaMoEは計算しないnull専門家をTop-k候補に加え、簡単なトークンほどnullを選ばせて実FFN数を減らし、トークンごとの計算量を適応させる。
<!-- survey:auto:end -->
