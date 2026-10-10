# Distributed / Heterogeneous MoE Training

MoEを多数GPUへ分散して学習すると、tokenごとに使うエキスパート（expert）が変わるため、通常のdense modelより**GPUごとの仕事量が偏りやすく、expertへtokenを送るGPU間通信も大きくなりやすい**。

この系統では、

- 人気expertを必要な数だけ複製する
- expertを別GPUへ移す
- attentionとexpertで異なる並列化を使う
- 新旧GPUへ得意な処理を分担させる
- paddingや重複token通信を減らす

といった方法で、**最も遅いGPUの待ち時間、GPU間通信量、GPUメモリ使用量を減らすMoE学習研究**をまとめる。

CPUやSSDへモデルを退避することが中心の研究は `01-training-offload-memory-systems/` に分類し、ここでは主にGPU間の配置・複製・通信・並列化を扱う。

<!-- survey:auto:start -->
## 自動生成の論文一覧（8本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

該当なし。

### 直近12か月・未被引用（2025-11〜2026-10）

該当なし。

### 2年前（2024-11〜2025-10）

- **2025-04 · [SYMI: Efficient Mixture-of-Experts Training via Model and Optimizer State Decoupling](2025-2504.19925-symi-efficient-mixture-of-experts-training-via-model-and-optimizer-state-decoupl.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  SYMIは、混合専門家（Mixture-of-Experts; MoE）モデルの学習中に、特定の専門家へトークンが集中しても、毎反復の専門家複製数を変更して負荷を吸収できる分散学習システムである。著者らはDeepSpeedを基盤に実装し、A100 80GBを16枚備えるAzureクラスタで評価した。

- **2025-04 · [MoE Parallel Folding: Heterogeneous Parallelism Mappings for Efficient Large-Scale MoE Model Training with Megatron Core](2025-2504.14960-moe-parallel-folding-heterogeneous-parallelism-mappings-for-efficient-large-scal.md)**  
  実装：[✓](https://github.com/NVIDIA/Megatron-LM) ・ リポジトリ内被引用：2  
  一方、大規模な分散学習では、専門家の重みを保持するためのGPUメモリ、トークンを担当専門家へ運ぶ全対全通信、注意機構のテンソル・文脈並列化が競合する。

- **2025-04 · [HeterMoE: Efficient Training of Mixture-of-Experts Models on Heterogeneous GPUs](2025-2504.03871-hetermoe-efficient-training-of-mixture-of-experts-models-on-heterogeneous-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  異なる世代のGPUを「一律に遅い／速い装置」とみなさず、注意計算と専門家計算の世代差を別々に測って配置するMoE学習システム。以下の速度値は学習処理率であり、生成時のトークン速度や推論待ち時間ではない。

- **2025-08 · [X-MoE: Enabling Scalable Training for Emerging Mixture-of-Experts Architectures on HPC Platforms](2025-2508.13337-x-moe-enabling-scalable-training-for-emerging-mixture-of-experts-architectures-o.md)**  
  実装：[✓](https://github.com/Supercomputing-System-AI-Lab/X-MoE) ・ リポジトリ内被引用：1  
  計算量を抑えながら専門家の組合せを増やせる反面、分配・回収するトークン活性値が増え、学習用GPUのメモリとノード間通信が律速になる。X-MoEはこの学習上の問題に対し、ゼロ埋めを排したトークン格納（PFT）、ノード間の重複回避分配（RBD）、MoE層専用の系列分割（SSMB）を統合する。

### 3年前（2023-11〜2024-10）

- **2024-04 · [Lancet: Accelerating Mixture-of-Experts Training via Whole Graph Computation-Communication Overlapping](2024-2404.19429-lancet.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  MoE学習の全対全通信をエキスパートだけでなく非MoE計算と重み勾配計算まで学習グラフ全体で重ね、最大1.3倍高速化する。

### 4年前（2022-11〜2023-10）

- **2023-04 · [FlexMoE: Scaling Large-scale Sparse Pre-trained Model Training via Dynamic Device Placement](2023-2304.03946-flexmoe-scaling-large-scale-sparse-pre-trained-model-training-via-dynamic-device.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  この疎な計算は理論上、パラメータを増やしても一トークン当たりの演算量を抑えられるが、複数のGPUに専門家を分散した学習ではトークンの偏りが大きな問題になる。FlexMoEはモデル側のトークン選択を変えず、同じ専門家の複製を複数GPUに配置し、実際の負荷に合わせて複製数と配置を調整する。

### 6年前（2020-11〜2021-10）

- **2021-09 · [Scalable and Efficient MoE Training for Multitask Multilingual Models](2021-2109.10465-scalable-efficient-moe-training.md)**  
  実装：[✓](https://github.com/microsoft/DeepSpeed) ・ リポジトリ内被引用：21  
  専門家並列とZeRO/CPUオフロード等の多次元並列を統合してMoEを3.5兆パラメータ超へ拡張し、ランダムトークン選択や専門家枝刈りで学習・推論効率も改善するDeepSpeed MoE。

### 7年前（2019-11〜2020-10）

- **2020-06 · [GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding](2020-2006.16668-gshard.md)**  
  実装：✓ ・ リポジトリ内被引用：196  
  疎な混合専門家モデルと自動SPMD分割を組み合わせ、少数の分割注釈だけで6000億パラメータ級Transformerを2048 TPUへ拡張し、4日で学習可能にした基礎システム。
<!-- survey:auto:end -->
