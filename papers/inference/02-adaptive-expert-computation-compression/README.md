# Adaptive Expert Computation / Compression

MoEで毎回同じ数のexpertを実行するのではなく、**token・layer・expertの重要度や実行コストに応じて、実際に使うexpert数やexpert構成を変える**研究をまとめる。簡単なtokenではexpert計算を減らし、重要なtokenやlayerには多くの計算を割り当てるほか、役割が似たexpertを統合したり、GPUにないexpertを似た常駐expertで代替したりして、品質低下を抑えながら計算量・転送量・モデル容量を減らす。

`Expert Prefetch` が「この先必要になるexpertを予測して早めにGPUへ用意する」ことを主眼とするのに対し、この系統は**そもそもどのexpertを何個実行するか、あるいはexpert構成そのものをどう小さくするか**が中心となる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（13本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-04 · [Alloc-MoE: Budget-Aware Expert Activation Allocation for Efficient Mixture-of-Experts Inference](2026-2604.08133-alloc-moe-budget-aware-expert-activation-allocation-for-efficient-mixture-of-exp.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  モデル全体で許すエキスパート実行回数を先に決め、その予算を影響の大きい層とルータ判断が曖昧なトークンへ多く配ることで、固定Top-kより少ない計算で品質を保つ。

- **2025-11 · [BuddyMoE: Exploiting Expert Redundancy to Accelerate Memory-Constrained Mixture-of-Experts Inference](2025-2511.10054-buddymoe-exploiting-expert-redundancy-to-accelerate-memory-constrained-mixture-o.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  必要なエキスパートがGPU キャッシュにない時、同じトークンで一緒に選ばれやすい常駐エキスパートを代わりに使い、CPUからエキスパート 重みを読むPCIe待ちを品質と引き換えに減らす。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Training-Free Halving of Activated Experts in Fine-Grained Mixture-of-Experts Models](2026-2609.04575-training-free-halving-activated-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  実行エキスパート数k1とルータ正規化分母の基準 集合 k2を分離し、細粒度 MoEでエキスパート 計算を減らしつつ訓練時のエキスパート-分岐 利得を保つ。Qwen3.6-35B-A3Bの8→4 エキスパートでMMLU低下を4.65ptから0.35ptへ縮小する。

- **2026-09 · [ACE: Adaptive Calibration-Free Expert Skipping for MoE-based LLMs](2026-2609.05228-ace.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  固定上位kルーティングで選ばれたエキスパートのうち実際の寄与が小さいスロットをトークンごとに省く、学習不要・チェックポイント保持型のMoE推論手法。

- **2026-06 · [Beyond Uniform Experts: Cost-Aware Expert Execution for Efficient Multi-Device MoE Inference](2026-2606.29982-beyond-uniform-experts-cost-aware-expert-execution-for-efficient-multi-device-mo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ルータ上の寄与が小さい一方で転送・実行に時間がかかり、特に全体処理を遅らせているdevice上のエキスパートを省き、その寄与を実行済みエキスパートへ振り分けてmulti-device MoEを高速化する。

- **2026-05 · [ReMoE: Boosting Expert Reuse through Router Fine-Tuning in Memory-Constrained MoE LLM Inference](2026-2605.27081-remoe-router-finetuning-expert-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  細粒度MoEを端末で動かすと、連続トークンが別々のエキスパートを選ぶたびに小さな高速キャッシュから重みが追い出され、CPU DRAMやNVMe SSDなど低速階層から再読込が必要になる。ReMoEは実行時キャッシュを複雑化する代わりに、既学習モデルのルータだけを追加学習し、直前に選んだエキスパートへ確率を寄せつつ元ルータからの逸脱をKL損失で抑える。

### 1年以上前

- **2024-02 · [Not All Experts are Equal: Efficient Expert Pruning and Skipping for Mixture-of-Experts Large Language Models](2024-2402.14800-not-all-experts-are-equal-efficient-expert-pruning-and-skipping-for-mixture-of-e.md)**  
  実装：[✓](https://github.com/Lucky-Lance/Expert_Sparsity) ・ リポジトリ内被引用：18  
  削除しても層出力があまり変わらないエキスパートをモデルから恒久的に除き、さらにトークンごとにルータ寄与が小さい第2エキスパートを省いて、メモリとFFN計算を減らす学習不要の手法。

- **2024-10 · [ExpertFlow: Efficient Mixture-of-Experts Inference via Predictive Expert Caching and Token Scheduling](2024-2410.17954-expertflow-efficient-mixture-of-experts-inference-via-predictive-expert-caching-.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  数層先で使うエキスパートを予測し、同じエキスパートを使いそうなトークンをまとめ、GPU キャッシュ容量も需要に応じて層間で動かすことで、CPUからエキスパートを読む待ち時間を減らすMoE推論システム。

- **2023-10 · [Merge, Then Compress: Demystify Efficient SMoE with Hints from Its Routing Policy](2023-2310.01334-merge-then-compress-demystify-efficient-smoe-with-hints-from-its-routing-policy.md)**  
  実装：[✓](https://github.com/UNITES-Lab/MC-SMoE) ・ リポジトリ内被引用：6  
  MC-SMoEは、MoEのルータがすでに持っている『どの専門家がよく使われ、どの専門家が似た入力を受けているか』という情報を、専門家圧縮にも使う研究である。まず似た専門家を代表専門家へ統合し、その後で統合済み重みをさらに低ランク + 疎に圧縮する。

- **2024-02 · [XMoE: Sparse Models with Fine-grained and Adaptive Expert Selection](2024-2403.18926-xmoe-sparse-models-with-fine-grained-and-adaptive-expert-selection.md)**  
  実装：[✓](https://github.com/ysngki/XMoE) ・ リポジトリ内被引用：3  
  ルータ確率を高い順に足し、合計が設定値に達するまでエキスパートを選ぶことで、ルータが確信しているトークンでは少数、判断が分散しているトークンでは多数のエキスパートを使う。

- **2025-09 · [LExI: Layer-Adaptive Active Experts for Efficient MoE Model Inference](2025-2509.02753-lexi-layer-adaptive-active-experts-for-efficient-moe-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  層ごとにTop-kを減らした時の出力変化を事前に測り、影響が小さい層ではエキスパート数を減らし、影響が大きい層へエキスパート実行予算を回すことで、固定Top-kより少ない計算で品質維持を狙う。

- **2024-06 · [AdaMoE: Token-Adaptive Routing with Null Experts for Mixture-of-Experts Language Models](2024-2406.13233-adamoe-token-adaptive-routing-with-null-experts-for-mixture-of-experts-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  計算を行わないnull エキスパートをルーティング候補へ加え、簡単なトークンではnullを多く選ばせることで、実際にFFN計算するエキスパート数をトークンごとに変えるMoE。

- **2024-10 · [MoE++: Accelerating Mixture-of-Experts Methods with Zero-Computation Experts](2024-2410.07348-moe-accelerating-mixture-of-experts-methods-with-zero-computation-experts.md)**  
  実装：[✓](https://github.com/SkyworkAI/MoE-plus-plus) ・ リポジトリ内被引用：0  
  通常のFFN エキスパートに加えて、何も出力しない・入力をそのまま返す・学習済み定数を返す軽量エキスパートをルーティング候補へ入れ、トークンに応じて実際のFFN計算数を減らすMoE。
<!-- survey:auto:end -->
