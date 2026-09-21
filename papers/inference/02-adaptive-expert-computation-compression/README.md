# Adaptive Expert Computation / Compression

MoEで毎回同じ数のexpertを実行するのではなく、**token・layer・expertの重要度や実行コストに応じて、実際に使うexpert数やexpert構成を変える**研究をまとめる。簡単なtokenではexpert計算を減らし、重要なtokenやlayerには多くの計算を割り当てるほか、役割が似たexpertを統合したり、GPUにないexpertを似た常駐expertで代替したりして、品質低下を抑えながら計算量・転送量・モデル容量を減らす。

`Expert Prefetch` が「この先必要になるexpertを予測して早めにGPUへ用意する」ことを主眼とするのに対し、この系統は**そもそもどのexpertを何個実行するか、あるいはexpert構成そのものをどう小さくするか**が中心となる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（34本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2025-10 · [REAP the Experts: Why Pruning Prevails for One-Shot MoE compression](2025-2510.13999-reap-one-shot-moe-compression.md)**  
  実装：[✓](https://github.com/CerebrasResearch/reap) ・ リポジトリ内被引用：6  
  ルーターゲート値と活性ノルムを組み合わせ、生成性能への寄与が小さい専門家をone-shotで削除し、最大1T級MoEでも50%圧縮を高品質に実現する。

- **2025-11 · [Opportunistic Expert Activation: Batch-Aware Expert Routing for Faster Decode Without Retraining](2025-2511.02237-opportunistic-expert-activation.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  各トークンの必須上位専門家を確保した後、同じバッチですでにロードされる専門家へ追加相乗りする再学習不要ルーティングで、MoEデコード遅延を最大39%削減する。

- **2025-11 · [BuddyMoE: Exploiting Expert Redundancy to Accelerate Memory-Constrained Mixture-of-Experts Inference](2025-2511.10054-buddymoe-exploiting-expert-redundancy-to-accelerate-memory-constrained-mixture-o.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  BuddyMoEはルータの共活性統計から常駐専門家を代替候補に選び、GPUキャッシュミス時のCPU重み転送を省いて、品質低下との交換でMoE推論を高速化する。

- **2026-04 · [Alloc-MoE: Budget-Aware Expert Activation Allocation for Efficient Mixture-of-Experts Inference](2026-2604.08133-alloc-moe-budget-aware-expert-activation-allocation-for-efficient-mixture-of-exp.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Alloc-MoEは全層・全トークンの専門家実行回数を総予算として、層の重要度とルータ確信度に応じて配分し、固定Top-kより少ない計算で品質を保つ。

- **2026-02 · [SERE: Similarity-based Expert Re-routing for Efficient Batch Decoding in MoE Models](2026-2602.07616-sere-similarity-expert-rerouting.md)**  
  実装：[✓](https://github.com/JL-Cheng/SERE) ・ リポジトリ内被引用：2  
  バッチ内で重複して活性化するMoEエキスパートを類似する主要エキスパートへ動的に再ルーティングし、品質を保ちながら復号を最大2倍高速化する。

- **2026-05 · [ReMoE: Boosting Expert Reuse through Router Fine-Tuning in Memory-Constrained MoE LLM Inference](2026-2605.27081-remoe-router-finetuning-expert-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ReMoEはルータだけを追加学習し、直前トークンで使った専門家へ確率を寄せて再利用を増やし、端末MoEのキャッシュミスと低速階層からの重み再読込を減らす。

- **2026-04 · [Temporally Extended Mixture-of-Experts Models](2026-2604.20156-temporally-extended-moe-expert-persistence.md)**  
  実装：[✓](https://github.com/princeton-polaris-lab/temporal-moe) ・ リポジトリ内被引用：1  
  専門家集合を複数トークン維持する選択肢として学習し、gpt-oss-20bの切替率を50%以上から数%へ抑えてオフロード向けの時間的連続性を作る方式。

- **2025-11 · [Route Experts by Sequence, not by Token](2025-2511.06494-seqtopk-route-by-sequence.md)**  
  実装：[✓](https://github.com/Y-Research-SBU/SeqTopK) ・ リポジトリ内被引用：1  
  系列全体で同じ総エキスパート予算を保ちながら、容易なトークンから難しいトークンへ計算を再配分し、高スパースMoEの品質を改善するSeqTopKを提案。

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

- **2026-09 · [Distribution-Consistent Inference for Dynamic Sparse Mixture-of-Experts](2026-2609.09241-distribution-consistent-dynamic-sparse-moe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動的MoE推論で専門家数を減らすと出力分散と尺度が増える問題を特定し、層・次元ごとの平均と分散を学習時分布へ戻す軽量補正で、同じ専門家予算の精度を大幅に回復する。

- **2026-09 · [Beyond Retraining-Free MoE Compression: A Cost-Normalized Study of Post-Compression Adjustment](2026-2609.06076-post-compression-adjustment-cost-normalized.md)**  
  実装：[✓](https://github.com/AIDASLab/Post-Compression-Adjustment) ・ リポジトリ内被引用：0  
  圧縮済みMoEを小規模調整の初期値と再定義し、3000例・1エポックの全パラメータ微調整で平均37.3%の性能差を回復するコスト正規化研究。

- **2026-09 · [ACE: Adaptive Calibration-Free Expert Skipping for MoE-based LLMs](2026-2609.05228-ace.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ACEはルータ重みと専門家変換能力の事前統計を組み合わせ、Top-k内でも寄与の小さいスロットだけをトークン単位で省く。元重みとTop-1を保ち、追加学習なしでFFN計算を減らす。

- **2026-08 · [Share First, Route What Remains: A Unified Framework for Token-Adaptive MoE Computation](2026-2608.10392-share-first-route-what-remains.md)**  
  実装：[✓](https://github.com/existence0420/UniF-MoE) ・ リポジトリ内被引用：0  
  共有ブロックを先にトークン適応で選び、残余需要だけを可変数の専門家へ累積確率で回すUniF-MoEにより、精度を高めながら推論計算・遅延・メモリを削減する。

- **2026-08 · [Meta-Learning Where to Allocate Experts: Task-Conditioned Layer-Wise Compression for MoEs](2026-2608.26650-metanet-task-conditioned-layer-wise-expert-allocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  支援集合から層別エキスパート数と弱いルーティング補正を推定し、凍結DeepSeek-MoEで平均active エキスパートを最大62%削減するタスク条件付きMetaNet。

- **2026-08 · [ExFold: Unified Expert Folding for Training-Free MoE Prefill-Decode Acceleration](2026-2608.24938-exfold-training-free-expert-folding.md)**  
  実装：[✓](https://github.com/Time-Rune/ExFold-MoE) ・ リポジトリ内被引用：0  
  除外エキスパートの出力を保持エキスパートへスカラー射影して、事前充填と復号を共通機構で高速化する再学習不要のエキスパート Folding。

- **2026-07 · [TriRoute: Unified Learned Routing for Joint Adaptive Attention, Experts, and KV-Cache Allocation](2026-2607.06601-triroute-joint-adaptive-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意機構・MoE専門家・KVキャッシュ精度を単一制御器で共同配分し、同一計算・メモリ予算で独立最適化より品質と希少事例の頑健性を改善する。

- **2026-07 · [It Takes a MAESTRO To Prune Bad Experts](2026-2607.08601-maestro-expert-pruning.md)**  
  実装：[✓](https://github.com/parmanu-lcs2) ・ リポジトリ内被引用：0  
  自己回帰生成時の層間専門家遷移をマルコフ連鎖として集計し、定常分布が小さい専門家を構造的に削除してMoEの常駐メモリを縮小する。

- **2026-06 · [SHAPE: Coalition-Aware Expert Pruning for Sparse Mixture-of-Experts LLMs](2026-2606.09886-shape-coalition-aware-expert-pruning.md)**  
  実装：[✓](https://github.com/Alizen-1009/Shapley-Moe) ・ リポジトリ内被引用：0  
  Top-kで同時起動する専門家集合を協力ゲームとして評価し、Shapley風の貢献度と層別品質カバレッジで再学習なしの専門家枝刈りを行う。

- **2026-06 · [Beyond Uniform Experts: Cost-Aware Expert Execution for Efficient Multi-Device MoE Inference](2026-2606.29982-beyond-uniform-experts-cost-aware-expert-execution-for-efficient-multi-device-mo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CAEEはルータ寄与と転送・実行コストを見て、層全体を待たせる遅いデバイスの低寄与専門家を省き、その重みを実行済み専門家へ再配分して分散MoEを高速化する。

- **2026-05 · [dMoE: dLLMs with Learnable Block Experts](2026-2605.30876-dmoe-block-level-experts.md)**  
  実装：[✓](https://github.com/fscdc/dMoE) ・ リポジトリ内被引用：0  
  ブロック内のトークン別ルータ得点を集約して適応的な専門家候補集合を作り、MoE拡散LLMの固有専門家数と重み読出しを大幅に減らす。

- **2026-03 · [Expert Threshold Routing for Autoregressive Language Modeling with Dynamic Computation Allocation and Load Balancing](2026-2603.11535-expert-threshold-routing.md)**  
  実装：[✓](https://github.com/MasterGodzilla/Expert-Threshold-Routing) ・ リポジトリ内被引用：0  
  専門家ごとの得点分位点を指数移動平均で追跡し、未来トークンを参照せず可変数の専門家を起動して負荷均衡と動的計算を両立する。

- **2025-10 · [MoE-Prism: Model and System Support for Request-Level Compute Elasticity in MoE Serving](2025-2510.19366-moe-prism-elastic-services.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  専門家を4分割してtop-k動作点を4倍に増やし、予算別バッチングと分割CUDAグラフで要求ごとの計算予算をvLLM上で効率的に実行する。

### 2年前（2024-10〜2025-09）

- **2024-10 · [ExpertFlow: Efficient Mixture-of-Experts Inference via Predictive Expert Caching and Token Scheduling](2024-2410.17954-expertflow-efficient-mixture-of-experts-inference-via-predictive-expert-caching-.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  ExpertFlowは数層先の専門家利用を予測し、同じ経路のトークンをまとめ、層ごとのGPUキャッシュ容量も再配分してCPUからの重み転送待ちを隠す。

- **2024-10 · [MoE++: Accelerating Mixture-of-Experts Methods with Zero-Computation Experts](2024-2410.07348-moe-accelerating-mixture-of-experts-methods-with-zero-computation-experts.md)**  
  実装：[✓](https://github.com/SkyworkAI/MoE-plus-plus) ・ リポジトリ内被引用：6  
  MoE++は無計算・入力コピー・学習済み定数の軽量専門家を通常FFNと同じ候補に混ぜ、トークンごとに代替経路を選んでFFN計算を減らす。

- **2025-09 · [Elastic MoE: Unlocking the Inference-Time Scalability of Mixture-of-Experts](2025-2509.21892-elastic-moe-inference-time-scalability.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  学習時と異なる活性エキスパート数でも性能が崩れないよう、多様な共活性組合せと階層的ルーター順位を学習し、単一MoEを2〜3倍の推論予算範囲へ弾性化する。

- **2025-09 · [LongCat-Flash Technical Report](2025-2509.01322-longcat-flash-zero-computation-experts.md)**  
  実装：[✓](https://github.com/meituan-longcat/LongCat-Flash-Chat) ・ リポジトリ内被引用：3  
  ゼロ計算専門家でトークンごとの活性計算量を18.6B～31.3Bへ動的配分し、ScMoEで専門家通信を密計算へ重ね、560B MoEの学習・推論効率を高める。

- **2025-09 · [LExI: Layer-Adaptive Active Experts for Efficient MoE Model Inference](2025-2509.02753-lexi-layer-adaptive-active-experts-for-efficient-moe-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  LExIは層ごとのTop-k削減による出力変化を合成入力で測り、影響の小さい層の専門家数を減らして重要層へ予算を回し、固定Top-kの計算を減らす。

- **2025-09 · [MoE-PHDS: One MoE checkpoint for flexible runtime sparsity](2025-2509.23012-moe-phds-flexible-runtime-sparsity.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数top-kを混ぜたSFTと低kアンカーにより、一つのMoEチェックポイントを複数の実行時疎性へ対応させ、SLA・エネルギー要求に応じてkを直接切り替える。

### 3年前（2023-10〜2024-09）

- **2024-02 · [Not All Experts are Equal: Efficient Expert Pruning and Skipping for Mixture-of-Experts Large Language Models](2024-2402.14800-not-all-experts-are-equal-efficient-expert-pruning-and-skipping-for-mixture-of-e.md)**  
  実装：[✓](https://github.com/Lucky-Lance/Expert_Sparsity) ・ リポジトリ内被引用：40  
  本研究は校正データで冗長な専門家を恒久削除し、実行時はルータ寄与の小さい第2専門家をトークン単位で省いて、Mixtralの常駐メモリとFFN計算を減らす。

- **2023-10 · [Merge, Then Compress: Demystify Efficient SMoE with Hints from Its Routing Policy](2023-2310.01334-merge-then-compress-demystify-efficient-smoe-with-hints-from-its-routing-policy.md)**  
  実装：[✓](https://github.com/UNITES-Lab/MC-SMoE) ・ リポジトリ内被引用：19  
  MC-SMoEはルータ履歴で似た専門家を代表へ統合し、統合重みを低ランク成分と疎な残差へ圧縮して、専門家数とメモリ使用量を減らす。

- **2024-06 · [AdaMoE: Token-Adaptive Routing with Null Experts for Mixture-of-Experts Language Models](2024-2406.13233-adamoe-token-adaptive-routing-with-null-experts-for-mixture-of-experts-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  AdaMoEは計算しないnull専門家をTop-k候補に加え、簡単なトークンほどnullを選ばせて実FFN数を減らし、トークンごとの計算量を適応させる。

- **2024-02 · [XMoE: Sparse Models with Fine-grained and Adaptive Expert Selection](2024-2403.18926-xmoe-sparse-models-with-fine-grained-and-adaptive-expert-selection.md)**  
  実装：[✓](https://github.com/ysngki/XMoE) ・ リポジトリ内被引用：5  
  XMoEはFFNを細粒度専門家に分割し、ルータ確率の累積が閾値に達するまでトークンごとに選ぶ数を変えて、確信度に応じた計算量配分で固定Top-kの無駄を減らす。
<!-- survey:auto:end -->
