# Adaptive Expert Computation / Compression

MoEで毎回同じ数のexpertを実行するのではなく、**token・layer・expertの重要度や実行コストに応じて、実際に使うexpert数やexpert構成を変える**研究をまとめる。簡単なtokenではexpert計算を減らし、重要なtokenやlayerには多くの計算を割り当てるほか、役割が似たexpertを統合したり、GPUにないexpertを似た常駐expertで代替したりして、品質低下を抑えながら計算量・転送量・モデル容量を減らす。

`Expert Prefetch` が「この先必要になるexpertを予測して早めにGPUへ用意する」ことを主眼とするのに対し、この系統は**そもそもどのexpertを何個実行するか、あるいはexpert構成そのものをどう小さくするか**が中心となる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（100本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2025-10 · [REAP the Experts: Why Pruning Prevails for One-Shot MoE compression](2025-2510.13999-reap-one-shot-moe-compression.md)**  
  実装：[✓](https://github.com/CerebrasResearch/reap) ・ リポジトリ内被引用：15  
  ルーターゲート値と活性ノルムを組み合わせ、生成性能への寄与が小さい専門家をone-shotで削除し、最大1T級MoEでも50%圧縮を高品質に実現する。

- **2025-11 · [Opportunistic Expert Activation: Batch-Aware Expert Routing for Faster Decode Without Retraining](2025-2511.02237-opportunistic-expert-activation.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  各トークンの必須上位専門家を確保した後、同じバッチですでにロードされる専門家へ追加相乗りする再学習不要ルーティングで、MoEデコード遅延を最大39%削減する。

- **2025-11 · [MoDES: Accelerating Mixture-of-Experts Multimodal Large Language Models via Dynamic Expert Skipping](2025-2511.15690-modes-dynamic-expert-skipping.md)**  
  実装：[✓](https://github.com/ModelTC/MoDES) ・ リポジトリ内被引用：5  
  層重要度のKL較正と画像・テキスト別閾値で、重要なエキスパートだけを残し、高省略率でもマルチモーダル性能を保つ学習不要の動的エキスパート省略法。

- **2026-02 · [XShare: Collaborative in-Batch Expert Sharing for Faster MoE Inference](2026-2602.07265-xshare-inbatch-expert-sharing.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  バッチ全体のルーター得点を集約して専門家集合を動的共有し、再学習なしで専門家混合推論の活性数・GPU負荷・投機デコード性能を改善する。

- **2025-10 · [MergeMoE: Efficient Compression of MoE Models via Expert Output Merging](2025-2510.14436-mergemoe-output-merging.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  エキスパート統合を出力近似問題として行列表現し、使用頻度重みの理論最適性と最小二乗による内部圧縮行列を組み合わせて、同圧縮率の既存統合法を改善する。

- **2026-06 · [DTop-p MoE: Sparsity-Controlled Dynamic Top-p MoE for Foundation Model Pre-training](2025-2512.13996-dtop-p-dynamic-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  比例積分制御でTop-p閾値を動かして平均専門家数を予算へ追従させ、層別正規化でトークン・深さごとに計算を再配分する事前学習MoE。

- **2026-04 · [REAM: Merging Improves Pruning of Experts in LLMs](2026-2604.04356-ream-router-weighted-expert-merging.md)**  
  実装：[✓](https://github.com/SamsungSAILMontreal/ream) ・ リポジトリ内被引用：3  
  重要専門家を代表として保護し、低重要度専門家をルータ・活性依存の類似度で統合するMoE圧縮。校正データ構成による選択式／生成性能のトレードオフも分析する。

- **2026-04 · [Alloc-MoE: Budget-Aware Expert Activation Allocation for Efficient Mixture-of-Experts Inference](2026-2604.08133-alloc-moe-budget-aware-expert-activation-allocation-for-efficient-mixture-of-exp.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  Alloc-MoEは全層・全トークンの専門家実行回数を総予算として、層の重要度とルータ確信度に応じて配分し、固定Top-kより少ない計算で品質を保つ。

- **2026-02 · [Unveiling Super Experts in Mixture-of-Experts Large Language Models](2025-2507.23279-super-experts-pruning-sensitivity.md)**  
  実装：[✓](https://github.com/ZunhaiSu/Super-Experts-Profilling) ・ リポジトリ内被引用：3  
  全専門家の0.5%未満しかないスーパー専門家が巨大活性と注意シンクの起点であり、Qwen3-30B-A3Bでは6144個中わずか3個を削るだけで推論課題平均が69.37から4.02へ崩壊することを示す。

- **2025-11 · [BuddyMoE: Exploiting Expert Redundancy to Accelerate Memory-Constrained Mixture-of-Experts Inference](2025-2511.10054-buddymoe-exploiting-expert-redundancy-to-accelerate-memory-constrained-mixture-o.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  BuddyMoEはルータの共活性統計から常駐専門家を代替候補に選び、GPUキャッシュミス時のCPU重み転送を省いて、品質低下との交換でMoE推論を高速化する。

- **2026-05 · [ReMoE: Boosting Expert Reuse through Router Fine-Tuning in Memory-Constrained MoE LLM Inference](2026-2605.27081-remoe-router-finetuning-expert-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  ReMoEはルータだけを追加学習し、直前トークンで使った専門家へ確率を寄せて再利用を増やし、端末MoEのキャッシュミスと低速階層からの重み再読込を減らす。

- **2026-05 · [Post-Trained MoE Can Skip Half Experts via Self-Distillation](2026-2605.18643-zeda-post-trained-dynamic-expert-skipping.md)**  
  実装：[✓](https://github.com/TsinghuaC3I/ZEDA) ・ リポジトリ内被引用：2  
  ゼロ出力専門家の挿入と二段階自己蒸留で既存MoEを動的化し、専門家計算を半減しつつ約1.2倍高速化する後処理法ZEDA。

- **2026-04 · [Temporally Extended Mixture-of-Experts Models](2026-2604.20156-temporally-extended-moe-expert-persistence.md)**  
  実装：[✓](https://github.com/princeton-polaris-lab/temporal-moe) ・ リポジトリ内被引用：2  
  専門家集合を複数トークン維持する選択肢として学習し、gpt-oss-20bの切替率を50%以上から数%へ抑えてオフロード向けの時間的連続性を作る方式。

- **2026-04 · [Does a Global Perspective Help Prune Sparse MoEs Elegantly?](2026-2604.06542-global-perspective-moe-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  層間で異なる専門家冗長性を全体最適化し、エントロピー制約付き貪欲統合で枝刈り予算を非一様配分して同一圧縮率の精度保持を改善する。

- **2026-02 · [SERE: Similarity-based Expert Re-routing for Efficient Batch Decoding in MoE Models](2026-2602.07616-sere-similarity-expert-rerouting.md)**  
  実装：[✓](https://github.com/JL-Cheng/SERE) ・ リポジトリ内被引用：2  
  バッチ内で重複して活性化するMoEエキスパートを類似する主要エキスパートへ動的に再ルーティングし、品質を保ちながら復号を最大2倍高速化する。

- **2026-01 · [Dynamic Expert Sharing: Decoupling Memory from Parallelism in Mixture-of-Experts Diffusion LLMs](2026-2602.00879-dynamic-expert-sharing.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  並列dLLMのトークン群で専門家コア集合を共有し、MoEのユニーク重み転送を約55%削減しつつ相対精度99.5%を維持、MoE層遅延を最大38%短縮する。

- **2025-12 · [MoE Pathfinder: Trajectory-driven Expert Pruning](2025-2512.18425-moe-pathfinder-trajectory-pruning.md)**  
  実装：[✓](https://github.com/xicyang/MoE-Pruning) ・ リポジトリ内被引用：2  
  MoEを層横断の重み付き専門家グラフとして扱い、再構成誤差・ルーティング・活性値を統合した大域経路計画で層ごとに非一様なエキスパート 枝刈りを決める。

- **2025-11 · [Route Experts by Sequence, not by Token](2025-2511.06494-seqtopk-route-by-sequence.md)**  
  実装：[✓](https://github.com/Y-Research-SBU/SeqTopK) ・ リポジトリ内被引用：2  
  系列全体で同じ総エキスパート予算を保ちながら、容易なトークンから難しいトークンへ計算を再配分し、高スパースMoEの品質を改善するSeqTopKを提案。

- **2026-06 · [Sticky Routing: Training MoE Models for Memory-Efficient Inference](2026-2607.08780-sticky-routing-memory-efficient-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  混合専門家（Mixture-of-Experts; MoE）モデルは各トークンで一部の専門家だけを活性化するため演算量を抑えられる一方、端末側では全専門家重みを高速メモリへ常駐できないことがある。隣接トークンが別々の専門家を選ぶと、低速な主記憶やストレージから重みを繰り返し入れ替える必要が生じ、疎な計算という利点がメモリ転送で相殺される。

- **2026-05 · [SlimQwen: Exploring the Pruning and Distillation in Large MoE Model Pre-training](2026-2605.08738-slimqwen-pruning-distillation.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Qwen3-Next 80A3Bを深さ・幅・専門家の段階的剪定と多トークン蒸留で23A2Bへ約4倍圧縮し、剪定初期化と段階的圧縮の優位性を示す。

- **2026-05 · [EMO: Pretraining Mixture of Experts for Emergent Modularity](2026-2605.06663-emo-emergent-modularity.md)**  
  実装：[✓](https://github.com/allenai/EMO) ・ リポジトリ内被引用：1  
  文書単位の共有専門家プール制約を事前学習へ導入し、領域ラベルなしで意味的モジュールを形成して少数専門家だけの領域別推論を可能にする。

- **2026-05 · [dMoE: dLLMs with Learnable Block Experts](2026-2605.30876-dmoe-block-level-experts.md)**  
  実装：[✓](https://github.com/fscdc/dMoE) ・ リポジトリ内被引用：1  
  ブロック内のトークン別ルータ得点を集約して適応的な専門家候補集合を作り、MoE拡散LLMの固有専門家数と重み読出しを大幅に減らす。

- **2026-03 · [SiftMoE: Similarity-Aware Energy-Efficient Expert Selection for Wireless Distributed MoE Inference](2026-2603.23888-siftmoe-similarity-aware-expert-selection.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  エキスパートの機能類似度から置換・スキップ時の誤差上界を求め、無線路状態・遅延・精度制約を同時に扱う最適化で、分散MoE推論の通信エネルギーをTop-K系手法より削減する。

- **2026-03 · [Expert Threshold Routing for Autoregressive Language Modeling with Dynamic Computation Allocation and Load Balancing](2026-2603.11535-expert-threshold-routing.md)**  
  実装：[✓](https://github.com/MasterGodzilla/Expert-Threshold-Routing) ・ リポジトリ内被引用：1  
  専門家ごとの得点分位点を指数移動平均で追跡し、未来トークンを参照せず可変数の専門家を起動して負荷均衡と動的計算を両立する。

- **2026-02 · [Certain Head, Uncertain Tail: Expert-Sample for Test-Time Scaling in Fine-Grained MoE](2026-2602.02443-expert-sample-test-time-scaling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  細粒度MoEの高確信専門家を固定し低確信尾部だけを確率的に選ぶことで、単発品質を崩しにくいまま複数推論経路の多様性とpass@nを高める。

- **2026-01 · [Improving MoE Compute Efficiency by Composing Weight and Data Sparsity](2026-2601.15370-composing-weight-data-sparsity.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ヌル専門家をトークン選択型MoEへ組み込み、因果性を保ったまま情報量に応じて実専門家数を変え、同一期待計算量で損失・下流性能の効率前線を改善する。

- **2025-10 · [Expert Merging in Sparse Mixture of Experts with Nash Bargaining](2025-2510.16138-namex-nash-expert-merging.md)**  
  実装：[✓](https://github.com/anh147/NAMEx) ・ リポジトリ内被引用：1  
  専門家差分をナッシュ交渉で重み付けして統合し、複素運動量で層間伝播を加速することで、言語・画像・14〜16B級MoEで既存統合を上回る。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Training-Free Halving of Activated Experts in Fine-Grained Mixture-of-Experts Models](2026-2609.04575-training-free-halving-activated-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は実行する専門家数k1とルータ正規化集合k2を分離し、k2を保ったままk1だけ半減して、細粒度MoEの計算削減とルータ利得を両立する学習不要手法。

- **2026-09 · [Residual Sparsification via Output Importance for Compressing Mixture-of-Experts LLMs](2026-2609.00575-parser-residual-sparsification-output-importance.md)**  
  実装：[✓](https://github.com/OSSS-KU/PARSER) ・ リポジトリ内被引用：0  
  MoE残差疎化の選択基準を行列誤差から専門家出力への影響へ変更し、層内全専門家で低影響な隠れ次元を選んで削ることで、同等メモリ削減時の精度低下を抑える。

- **2026-09 · [PCoMoE: Shifting MoE Inference from Monolithic Expert Selection to Fine-Grained Path Composition](2026-2609.01024-pcomoe-fine-grained-path-composition.md)**  
  実装：[✓](https://github.com/gzyyy0/PCoMoE) ・ リポジトリ内被引用：0  
  MoE専門家を展開側と射影側へ分け、異なる専門家の内部部品を適合度に基づき組み合わせ、共通の展開計算を複数経路で再利用することで、専門家単位の削減より細粒度に計算を減らす方式。

- **2026-09 · [MoEP: Compact and efficient sparsity with modular expert paths](2026-moep-modular-expert-paths.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  固定総パラメータ予算のまま縮小次元の並列Transformerブロックをトークン単位で選ぶ層レベル疎経路を導入し、小規模では一部改善を得る一方、1B規模では密モデルより遅くメモリも増える限界まで実測した。

- **2026-09 · [GeMoE: Gating Entropy is All You Need for Uncertainty-aware Adaptive Routing in MoE-based Large Vision-Language Models](2026-2606.26287-gemoe-gating-entropy-adaptive-routing.md)**  
  実装：[✓](https://github.com/caichaoxiang/GeMoE) ・ リポジトリ内被引用：0  
  ゲート分布のエントロピーを不確実性指標として各トークンの専門家数を予測し、固定Top-kに近い品質を保ちながら専門家活性化と実測推論時間を削減する動的MoEルーティング。

- **2026-09 · [Distribution-Consistent Inference for Dynamic Sparse Mixture-of-Experts](2026-2609.09241-distribution-consistent-dynamic-sparse-moe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動的MoE推論で専門家数を減らすと出力分散と尺度が増える問題を特定し、層・次元ごとの平均と分散を学習時分布へ戻す軽量補正で、同じ専門家予算の精度を大幅に回復する。

- **2026-09 · [Beyond Retraining-Free MoE Compression: A Cost-Normalized Study of Post-Compression Adjustment](2026-2609.06076-post-compression-adjustment-cost-normalized.md)**  
  実装：[✓](https://github.com/AIDASLab/Post-Compression-Adjustment) ・ リポジトリ内被引用：0  
  圧縮済みMoEを小規模調整の初期値と再定義し、3000例・1エポックの全パラメータ微調整で平均37.3%の性能差を回復するコスト正規化研究。

- **2026-09 · [ACE: Adaptive Calibration-Free Expert Skipping for MoE-based LLMs](2026-2609.05228-ace.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ACEはルータ重みと専門家変換能力の事前統計を組み合わせ、Top-k内でも寄与の小さいスロットだけをトークン単位で省く。元重みとTop-1を保ち、追加学習なしでFFN計算を減らす。

- **2026-08 · [UniMoMo: Expert Merging-Based MoE Acceleration for Large Recommendation Models](2026-2608.08627-unimomo-expert-merging.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推薦向け混合エキスパートの機能的類似度と経路利用量を同じ校正データから推定し、重要なエキスパートを保護しつつグラフ粗視化で配備時の専門家数を削減する事後圧縮。

- **2026-08 · [TuringLLM: Efficiently Scaling Foundation Models Toward Physical AI](2026-2608.30567-turingllm-dynamic-topk.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  平均約8エキスパートの計算予算を保ったままトークンごとに動的top-kを変え、分位点追跡で負荷分散し、プリフィル容量制約で長文MoE実行を規則化する20B-A2Bモデル。

- **2026-08 · [Share First, Route What Remains: A Unified Framework for Token-Adaptive MoE Computation](2026-2608.10392-share-first-route-what-remains.md)**  
  実装：[✓](https://github.com/existence0420/UniF-MoE) ・ リポジトリ内被引用：0  
  共有ブロックを先にトークン適応で選び、残余需要だけを可変数の専門家へ累積確率で回すUniF-MoEにより、精度を高めながら推論計算・遅延・メモリを削減する。

- **2026-08 · [Shape Mutating Expert Compression: LorExperts and BTExperts](2026-2608.07814-lorexperts-btexperts-shape-mutating-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共活性クラスタごとに完全精度代表を残し他専門家を整列済み低ランク補正化、ルータを維持したまま約50%圧縮するLorExpertsと計算共有用BTExperts。

- **2026-08 · [REFLEX: Rethinking MoE Inference as Refinement-Aware Compute Allocation in Diffusion Language Models](2026-2608.01784-reflex-refinement-aware-compute-allocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルの各位置の洗練状態に応じて専門家数を再配分し、既定ルータの順位を保ったまま平均約15%の専門家計算を削減しつつ品質を維持・改善する。

- **2026-08 · [Meta-Learning Where to Allocate Experts: Task-Conditioned Layer-Wise Compression for MoEs](2026-2608.26650-metanet-task-conditioned-layer-wise-expert-allocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  支援集合から層別エキスパート数と弱いルーティング補正を推定し、凍結DeepSeek-MoEで平均active エキスパートを最大62%削減するタスク条件付きMetaNet。

- **2026-08 · [ExFold: Unified Expert Folding for Training-Free MoE Prefill-Decode Acceleration](2026-2608.24938-exfold-training-free-expert-folding.md)**  
  実装：[✓](https://github.com/Time-Rune/ExFold-MoE) ・ リポジトリ内被引用：0  
  除外エキスパートの出力を保持エキスパートへスカラー射影して、事前充填と復号を共通機構で高速化する再学習不要のエキスパート Folding。

- **2026-08 · [Beyond Global Routing Aggregation: Phase-Aware Expert Merging for MoE Vision-Language Models](2026-2608.04454-phase-aware-expert-merging.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像・質問・回答のフェーズ別ルーティング役割を保持してMoE-VLMエキスパートを学習不要で統合するRoleMerge。

- **2026-07 · [TriRoute: Unified Learned Routing for Joint Adaptive Attention, Experts, and KV-Cache Allocation](2026-2607.06601-triroute-joint-adaptive-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意機構・MoE専門家・KVキャッシュ精度を単一制御器で共同配分し、同一計算・メモリ予算で独立最適化より品質と希少事例の頑健性を改善する。

- **2026-07 · [TENP: Trapezoidal Expert Neuron Pruning For Mixture-of-Experts](2026-2606.09885-tenp-trapezoidal-expert-neuron-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重要専門家と元ルーティングを残しつつ、浅層ほど強く専門家内部ニューロンを構造剪定する台形型MoE圧縮。

- **2026-07 · [It Takes a MAESTRO To Prune Bad Experts](2026-2607.08601-maestro-expert-pruning.md)**  
  実装：[✓](https://github.com/parmanu-lcs2) ・ リポジトリ内被引用：0  
  自己回帰生成時の層間専門家遷移をマルコフ連鎖として集計し、定常分布が小さい専門家を構造的に削除してMoEの常駐メモリを縮小する。

- **2026-06 · [SHAPE: Coalition-Aware Expert Pruning for Sparse Mixture-of-Experts LLMs](2026-2606.09886-shape-coalition-aware-expert-pruning.md)**  
  実装：[✓](https://github.com/Alizen-1009/Shapley-Moe) ・ リポジトリ内被引用：0  
  Top-kで同時起動する専門家集合を協力ゲームとして評価し、Shapley風の貢献度と層別品質カバレッジで再学習なしの専門家枝刈りを行う。

- **2026-06 · [From Observation to Intervention: A Causal Audit of Expert Importance in Mixture-of-Experts Models](2026-2606.10703-causal-audit-expert-importance.md)**  
  実装：[✓](https://github.com/callmeloui/observational_metrics) ・ リポジトリ内被引用：0  
  3種の高冗長MoEで観測的なルーティング統計と専門家除去の因果効果を直接照合し、60条件すべてで重要度予測が成立せず、既存剪定の成功は主に初期層の冗長性で説明できると示した。

- **2026-06 · [Depth-Aware Sensitivity Analysis of Mixture-of-Experts Models via Magnitude-Based Expert Masking](2026-2608.13565-depth-aware-moe-sensitivity.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Qwen3.6-35B-A3Bを実測し、MoE専門家削減は全層一律ではなく後段、とくに35-39層へ集中させる方が品質を保てることを500件の保持検証まで示す。

- **2026-06 · [Beyond Uniform Experts: Cost-Aware Expert Execution for Efficient Multi-Device MoE Inference](2026-2606.29982-beyond-uniform-experts-cost-aware-expert-execution-for-efficient-multi-device-mo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CAEEはルータ寄与と転送・実行コストを見て、層全体を待たせる遅いデバイスの低寄与専門家を省き、その重みを実行済み専門家へ再配分して分散MoEを高速化する。

- **2026-05 · [Uncovering Intra-expert Activation Sparsity for Efficient Mixture-of-Expert Model Execution](2026-2605.08575-intra-expert-activation-sparsity.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既存MoEのエキスパート内活性値 sparsityをvLLMへ統合し、再学習なしでMoE 層最大2.5倍・エンドツーエンド最大1.2倍を実現する。

- **2026-05 · [HodgeCover: Higher-Order Topological Coverage Drives Compression of Sparse Mixture-of-Experts](2026-2605.13997-hodgecover-topological-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  専門家ペアだけでは見えない三つ組の統合障害をホッジ調和成分として抽出し、重要な辺・三角形を被覆するよう生存専門家を選ぶ学習不要MoE圧縮。

- **2026-05 · [Extracting Small Translation Specialists from LLMs by Aggressively Pruning Experts](2026-2605.28042-translation-specialist-expert-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  翻訳時のルーティング質量と層別言語特化度から専門家を選び、GPT-OSS-20Bの専門家50%を再学習なし、75%を短い回復学習付きで削除しつつ翻訳品質と実VRAMを大きく維持・削減する。

- **2026-05 · [DECO: Sparse Mixture-of-Experts with Dense-Comparable Performance on End-Side Devices](2026-2605.10933-deco-end-side-sparse-moe.md)**  
  実装：[✓](https://github.com/thunlp/DECO) ・ リポジトリ内被引用：0  
  総パラメータ数と学習量を密モデルと揃えたまま、ReLUルーティングとNormSiLUで専門家活性を約20%に抑え、Jetson AGX Orinで密推論比2.93倍のデコード速度を示す端末向けMoE設計。

- **2026-05 · [BitsMoE: Efficient Spectral Energy-Guided Bit Allocation for MoE LLM Quantization](2026-2606.00079-bitsmoe-spectral-bit-allocation.md)**  
  実装：[✓](https://github.com/zjiayu064/BitsMoE) ・ リポジトリ内被引用：0  
  共有スペクトル基底をFP16保持し、専門家固有成分へ活性・スペクトルエネルギー依存でビットを整数最適配分する超低ビットMoE量子化。

- **2026-05 · [BEAM: Binary Expert Activation Masking for Dynamic Routing in MoE](2026-2605.14438-beam-binary-expert-activation-masking.md)**  
  実装：[✓](https://github.com/Time-Rune/BEAM) ・ リポジトリ内被引用：0  
  固定Top-K候補を学習二値マスクでトークンごとに削り、vLLM CUDA実装で実際の専門家計算を省略する動的MoEルーティング。

- **2026-03 · [LightMoE: Reducing Mixture-of-Experts Redundancy through Expert Replacing](2026-2603.12645-lightmoe-expert-replacing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  枝刈りは知識を不可逆に捨て、統合は異なる専門性を平均化しやすい。OLMoE-1B-7B-SFTを5種類の下流課題で評価した結果、30%圧縮では非圧縮モデルへのLoRA微調整とほぼ同等の平均性能を維持し、50%圧縮では同じ学習予算の既存圧縮法を平均5.6%、単純置換を3.8%上回った。

- **2026-02 · [VersatileFFN: Achieving Parameter Efficiency in LLMs via Adaptive Wide-and-Deep Reuse](2025-2512.14531-versatileffn-adaptive-wide-deep-reuse.md)**  
  実装：[✓](https://github.com/huawei-noah/noah-research/tree/master/VersatileFFN) ・ リポジトリ内被引用：0  
  同一FFNを仮想専門家として幅方向に分割し、難しいトークンには深さ方向に再帰利用することで、追加パラメータをほぼ増やさず計算量を適応配分し、1.21Bで8タスク平均60.47%を達成する。

- **2026-02 · [OmniMoE: An Efficient MoE by Orchestrating Atomic Experts at Scale](2026-2602.05711-omnimoe-atomic-experts.md)**  
  実装：[✓](https://github.com/HKUSTDial/omni-moe) ・ リポジトリ内被引用：0  
  ベクトル単位Atomic エキスパート、直積ルータ、専門家中心スケジューリングを統合し、PEER比10.9倍高速で7ベンチ平均50.9%を達成する細粒度MoE。

- **2026-01 · [LatentMoE: Toward Optimal Accuracy per FLOP and Parameter in Mixture of Experts](2026-2601.18089-latentmoe-accuracy-per-flop-parameter.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoEエキスパートを低次元潜在空間で計算し、削減した帯域・通信コストを総エキスパート数と活性エキスパート数の拡大へ再投資して、計算量当たり精度とパラメータ当たり精度を同時に改善する設計。

- **2026-01 · [ConceptMoE: Adaptive Token-to-Concept Compression for Implicit Compute Allocation](2026-2601.21420-conceptmoe-token-concept-compression.md)**  
  実装：[✓](https://github.com/ZihaoHuang-notabot/ConceptMoE) ・ リポジトリ内被引用：0  
  意味類似トークンを概念へ適応圧縮し、同一パラメータ・同一平均演算量下で節約計算を専門家混合モデルへ再配分して性能と長文脈推論効率を同時改善する。

- **2025-11 · [AnyExperts: On-Demand Expert Allocation for Multimodal Language Models with Mixture of Expert](2025-2511.18314-anyexperts-on-demand-expert-allocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークン重要度から実専門家と仮想専門家の可変スロットを割り当て、固定Top-Kより細粒度にマルチモーダルMoEの計算予算を配分する。

- **2025-10 · [MoE-Prism: Model and System Support for Request-Level Compute Elasticity in MoE Serving](2025-2510.19366-moe-prism-elastic-services.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  専門家を4分割してtop-k動作点を4倍に増やし、予算別バッチングと分割CUDAグラフで要求ごとの計算予算をvLLM上で効率的に実行する。

- **2025-10 · [GatePro: Parameter-Free Expert Selection Optimization for Mixture-of-Experts Models](2025-2510.13079-gatepro-parameter-free-expert-selection.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ゲート重みが最も似る専門家同士をトークンごとに局所競争させ、追加パラメータなしで冗長な同時活性化を抑えて専門家多様性とモデル品質を改善する。

### 2年前（2024-10〜2025-09）

- **2024-10 · [MoE-Pruner: Pruning Mixture-of-Experts Large Language Model using the Hints from Its Router](2024-2410.12013-moe-pruner-router-hints.md)**  
  実装：✓ ・ リポジトリ内被引用：28  
  重み・入力活性・ルータ重みを組み合わせたMoE専用重要度でエキスパート 重みをone-shot枝刈りし、エキスパート-wise蒸留で50%疎性でも元性能の約99%まで回復する。

- **2024-10 · [MoE++: Accelerating Mixture-of-Experts Methods with Zero-Computation Experts](2024-2410.07348-moe-accelerating-mixture-of-experts-methods-with-zero-computation-experts.md)**  
  実装：[✓](https://github.com/SkyworkAI/MoE-plus-plus) ・ リポジトリ内被引用：22  
  MoE++は無計算・入力コピー・学習済み定数の軽量専門家を通常FFNと同じ候補に混ぜ、トークンごとに代替経路を選んでFFN計算を減らす。

- **2024-10 · [ExpertFlow: Efficient Mixture-of-Experts Inference via Predictive Expert Caching and Token Scheduling](2024-2410.17954-expertflow-efficient-mixture-of-experts-inference-via-predictive-expert-caching-.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  ExpertFlowは数層先の専門家利用を予測し、同じ経路のトークンをまとめ、層ごとのGPUキャッシュ容量も再配分してCPUからの重み転送待ちを隠す。

- **2024-10 · [Retraining-Free Merging of Sparse MoE via Hierarchical Clustering](2024-2410.08589-hc-smoe-retraining-free-merging.md)**  
  実装：[✓](https://github.com/wazenmai/HC-SMoE) ・ リポジトリ内被引用：13  
  専門家の平均出力を用いる階層的クラスタリングと頻度重み付き統合により、再学習なしでQwen/Mixtralの専門家を最大50%削減しつつ比較手法より高い性能保持を示す。

- **2025-06 · [Sub-MoE: Efficient Mixture-of-Expert LLMs Compression via Subspace Expert Merging](2025-2506.23266-sub-moe-subspace-expert-merging.md)**  
  実装：[✓](https://github.com/siruihan2024/Sub-MoE) ・ リポジトリ内被引用：11  
  機能類似度クラスタリングと共有部分空間SVDでMoE専門家を整列し、活性頻度重み付きV統合でパラメータ衝突を抑える学習不要の専門家統合。

- **2025-09 · [LongCat-Flash Technical Report](2025-2509.01322-longcat-flash-zero-computation-experts.md)**  
  実装：[✓](https://github.com/meituan-longcat/LongCat-Flash-Chat) ・ リポジトリ内被引用：8  
  ゼロ計算専門家でトークンごとの活性計算量を18.6B～31.3Bへ動的配分し、ScMoEで専門家通信を密計算へ重ね、560B MoEの学習・推論効率を高める。

- **2025-04 · [Finding Fantastic Experts in MoEs: A Unified Study for Expert Dropping Strategies and Observations](2025-2504.05586-finding-fantastic-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  MoEエキスパート重要度を4視点・16指標で比較し、反復再評価＋軽量微調整なら50%以上削減でも性能を保ちやすく、指示追従能力の回復が鍵と示す。

- **2025-09 · [LExI: Layer-Adaptive Active Experts for Efficient MoE Model Inference](2025-2509.02753-lexi-layer-adaptive-active-experts-for-efficient-moe-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  LExIは層ごとのTop-k削減による出力変化を合成入力で測り、影響の小さい層の専門家数を減らして重要層へ予算を回し、固定Top-kの計算を減らす。

- **2025-09 · [Elastic MoE: Unlocking the Inference-Time Scalability of Mixture-of-Experts](2025-2509.21892-elastic-moe-inference-time-scalability.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  学習時と異なる活性エキスパート数でも性能が崩れないよう、多様な共活性組合せと階層的ルーター順位を学習し、単一MoEを2〜3倍の推論予算範囲へ弾性化する。

- **2025-09 · [DiEP: Adaptive Mixture-of-Experts Compression through Differentiable Expert Pruning](2025-2509.16105-diep-differentiable-expert-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  層ごとに異なるエキスパート冗長性を微分可能な探索で学習し、重要度に応じた非一様プルーニングでMoEの推論コストを削減する。

- **2025-05 · [Faster MoE LLM Inference for Extremely Large Models](2025-2505.03531-faster-moe-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  細粒度MoEで活性専門家数と総専門家数を別々に削減して実測し、活性専門家スキップは負荷依存で高速化できる一方、総専門家枝刈りは品質損失が大きいという実用境界を示す。

- **2025-09 · [Dropping Experts, Recombining Neurons: Retraining-Free Pruning for Sparse Mixture-of-Experts LLMs](2025-2509.10377-dern-dropping-experts-recombining-neurons.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  低重要度エキスパートを削除後、内部ニューロンをセグメントとして互換な残存エキスパートへ再配置・クラスタ統合し、再学習なしで知識を回収するMoE圧縮法。

- **2025-08 · [MoBE: Mixture-of-Basis-Experts for Compressing MoE-based LLMs](2025-2508.05257-mobe-mixture-of-basis-experts.md)**  
  実装：[✓](https://github.com/inclusionAI/MoBE) ・ リポジトリ内被引用：2  
  エキスパート固有の小行列と層共有basis行列の組合せでup/gate重みを再構成し、巨大MoEをdata-freeに24〜30%圧縮しながら性能低下を1〜2%程度へ抑える。

- **2025-08 · [Grove MoE: Towards Efficient and Superior MoE LLMs with Adjugate Experts](2025-2508.07785-grove-moe-heterogeneous-experts.md)**  
  実装：[✓](https://github.com/inclusionAI/GroveMoE) ・ リポジトリ内被引用：2  
  専門家群ごとに小型の随伴専門家を共有して通常の上位k個ルーティングのまま計算量を動的化し、33B総パラメータ・3.14〜3.28B活性のGroveMoEを構築する。

- **2025-05 · [Mixture of Lookup Experts](2025-2503.15798-mixture-of-lookup-experts.md)**  
  実装：[✓](https://github.com/JieShibo/MoLE) ・ リポジトリ内被引用：2  
  学習時エキスパート入力を語彙埋め込みへ固定して推論前にFFN出力を検索表化し、巨大エキスパート重みではなく小さな出力ベクトルだけをストレージから読むことでMoEのVRAMと転送遅延を削減する。

- **2025-04 · [Cluster-Driven Expert Pruning for Mixture-of-Experts Large Language Models](2025-2504.07807-cluster-driven-expert-pruning.md)**  
  実装：[✓](https://github.com/Fighoture/MoE_unsupervised_pruning) ・ リポジトリ内被引用：2  
  MoE内の似たエキスパートを層ごとにクラスタ化し、層横断の冗長性も見ながらクラスタ単位で枝刈り・統合して、20%圧縮時の性能低下を既存方式より抑える。

- **2025-09 · [Ban&Pick: Enhancing Performance and Efficiency of MoE-LLMs via Smarter Routing](2025-2509.06346-ban-pick-smarter-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  重要専門家をKL影響度でPickし、層・トークン感度に応じて冗長専門家をBanする学習不要のMoE推論時ルーティング補正。

- **2025-02 · [Analytical FFN-to-MoE Restructuring via Activation Pattern Analysis](2025-2502.04416-analytical-ffn-to-moe-restructuring.md)**  
  実装：[✓](https://github.com/JarvisPei/CMoE) ・ リポジトリ内被引用：1  
  ニューロン活性統計から共有・経路選択エキスパートと経路選択器を解析的に構築し、数分の変換と少量微調整で既存の密モデルまたはMoEへ階層的な疎計算を後付けする。

- **2025-09 · [MoE-PHDS: One MoE checkpoint for flexible runtime sparsity](2025-2509.23012-moe-phds-flexible-runtime-sparsity.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数top-kを混ぜたSFTと低kアンカーにより、一つのMoEチェックポイントを複数の実行時疎性へ対応させ、SLA・エネルギー要求に応じてkを直接切り替える。

- **2025-09 · [HEAPr: Hessian-based Efficient Atomic Expert Pruning in Output Space](2025-2509.22299-heapr-atomic-expert-pruning.md)**  
  実装：[✓](https://github.com/LLIKKE/HEAPr) ・ リポジトリ内被引用：0  
  MoE エキスパートをatomic エキスパートへ分解し、出力空間の二次情報で全層を大域順位付けして剪定することで、20〜25%程度の圧縮を多くのモデルでほぼ無損失に実現する。

- **2025-09 · [FURINA: Free from Unmergeable Router via LINear Aggregation of mixed experts](2025-2509.14900-furina-router-free-linear-expert-aggregation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  離散ルータを出力ノルムによる自己ルーティングへ置換し、学習時はMoE-LoRAの容量を使いながら推論前に全エキスパートを単一LoRA・基盤重みへ完全統合する方式。

- **2025-09 · [Faster, Smaller, and Smarter: Task-Aware Expert Merging for Online MoE Inference](2025-2509.19781-task-aware-expert-merging-online.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  タスクタグなしのオンラインMoEでタスク分布を文脈に連続な専門家統合重みを木構造ニューラルバンディットで探索し、単一統合専門家により推論時間とメモリを削減する。

- **2025-09 · [Dynamic Experts Search: Enhancing Reasoning in Mixture-of-Experts LLMs at Test Time](2025-2509.22572-dynamic-experts-search.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoEの活性化エキスパート数をTTSの探索軸に加え、推論軌跡ごとに構成を継承して同程度の計算量で推論多様性と正解率を高める。

- **2025-09 · [Breaking the MoE LLM Trilemma: Dynamic Expert Clustering with Structured Compression](2025-2510.02345-dynamic-expert-clustering-structured-compression.md)**  
  実装：[✓](https://github.com/szdtzpj/Breaking_the_moe_trilemma) ・ リポジトリ内被引用：0  
  パラメータ＋活性類似度で専門家を動的再編し、共有基底＋低ランク残差、階層ルーティング、INT4残差、NVMeオフロードを共同設計するMoE構造圧縮。

### 3年前（2023-10〜2024-09）

- **2024-02 · [Not All Experts are Equal: Efficient Expert Pruning and Skipping for Mixture-of-Experts Large Language Models](2024-2402.14800-not-all-experts-are-equal-efficient-expert-pruning-and-skipping-for-mixture-of-e.md)**  
  実装：[✓](https://github.com/Lucky-Lance/Expert_Sparsity) ・ リポジトリ内被引用：73  
  本研究は校正データで冗長な専門家を恒久削除し、実行時はルータ寄与の小さい第2専門家をトークン単位で省いて、Mixtralの常駐メモリとFFN計算を減らす。

- **2023-10 · [Merge, Then Compress: Demystify Efficient SMoE with Hints from Its Routing Policy](2023-2310.01334-merge-then-compress-demystify-efficient-smoe-with-hints-from-its-routing-policy.md)**  
  実装：[✓](https://github.com/UNITES-Lab/MC-SMoE) ・ リポジトリ内被引用：47  
  MC-SMoEはルータ履歴で似た専門家を代表へ統合し、統合重みを低ランク成分と疎な残差へ圧縮して、専門家数とメモリ使用量を減らす。

- **2024-06 · [AdaMoE: Token-Adaptive Routing with Null Experts for Mixture-of-Experts Language Models](2024-2406.13233-adamoe-token-adaptive-routing-with-null-experts-for-mixture-of-experts-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  AdaMoEは計算しないnull専門家をTop-k候補に加え、簡単なトークンほどnullを選ばせて実FFN数を減らし、トークンごとの計算量を適応させる。

- **2024-02 · [XMoE: Sparse Models with Fine-grained and Adaptive Expert Selection](2024-2403.18926-xmoe-sparse-models-with-fine-grained-and-adaptive-expert-selection.md)**  
  実装：[✓](https://github.com/ysngki/XMoE) ・ リポジトリ内被引用：12  
  XMoEはFFNを細粒度専門家に分割し、ルータ確率の累積が閾値に達するまでトークンごとに選ぶ数を変えて、確信度に応じた計算量配分で固定Top-kの無駄を減らす。

- **2024-07 · [Diversifying the Expert Knowledge for Task-Agnostic Pruning in Sparse Mixture-of-Experts](2024-2407.09590-task-agnostic-expert-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  共有入力上の専門家知識類似度で冗長専門家をグループ化し、専門家とルータを同時統合することで、タスク非依存にMoEのメモリと推論時間を削減する。

### 4年前（2022-10〜2023-09）

- **2023-07 · [Memory-efficient NLLB-200: Language-specific Expert Pruning of a Massively Multilingual Machine Translation Model](2022-2212.09811-nllb-language-specific-expert-pruning.md)**  
  実装：[✓](https://github.com/naver/nllb-pruning) ・ リポジトリ内被引用：10  
  翻訳時ゲート統計で言語別に重要な専門家を選び、NLLB-200の専門家を最大80%枝刈りして単一32GB GPU推論を可能にする方式。

- **2023-06 · [Soft Merging of Experts with Adaptive Routing](2023-2306.03745-smear-soft-merging-adaptive-routing.md)**  
  実装：[✓](https://github.com/r-three/smear) ・ リポジトリ内被引用：6  
  経路選択確率でエキスパート重みを入力ごとに合成して離散選択を消し、標準的な誤差逆伝播のまま適応的な専門化と単一エキスパート相当の活性計算を両立する。

- **2023-03 · [Sparse MoE as the New Dropout: Scaling Dense and Self-Slimmable Transformers](2023-2303.01610-smoe-dropout-self-slimmable.md)**  
  実装：[✓](https://github.com/VITA-Group/Random-MoE-as-Dropout) ・ リポジトリ内被引用：6  
  固定ランダム経路選択器と学習中の活性エキスパート数漸増により、1回の事前学習から推論資源に応じて容量を可変化できる自己スリム化SMoEを作る。

### 5年前（2021-10〜2022-09）

- **2022-01 · [DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale](2022-2201.05596-deepspeed-moe-inference-compression.md)**  
  実装：[✓](https://github.com/microsoft/DeepSpeed) ・ リポジトリ内被引用：41  
  PR-MoE/MoSでMoEサイズを最大3.7倍縮小し、多次元並列・通信・融合カーネルを統合してPyTorch比最大7.3倍、同等品質dense比最大4.5倍高速な推論を実現。

- **2022-06 · [Task-Specific Expert Pruning for Sparse Mixture-of-Experts](2022-2206.00277-task-specific-expert-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：33  
  下流タスク微調整中のゲート寄与から専門家を段階的に1つまで削り、混合専門家事前学習の利得をほぼ保った密モデルへ変換する方式。

- **2022-02 · [Mixture-of-Experts with Expert Choice Routing](2022-2202.09368-expert-choice-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：25  
  専門家側が固定容量ぶんの上位トークンを選ぶことで完全な負荷均衡とトークンごとの可変計算量を同時に実現するMoEルーティング。

- **2022-05 · [MoEfication: Transformer Feed-forward Layers are Mixtures of Experts](2021-2110.01786-moefication.md)**  
  実装：[✓](https://github.com/thunlp/MoEfication) ・ リポジトリ内被引用：10  
  密なTransformerのフィードフォワード層を共活性化するニューロン単位で専門家化し、入力ごとに一部だけを実行する疎推論方式。
<!-- survey:auto:end -->
