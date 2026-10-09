<!-- survey:auto:start -->
## 自動生成の論文一覧（23本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2025-11 · [Latent Collaboration in Multi-Agent Systems](2025-2511.20639-latent-collaboration-in-multi-agent-systems.md)**  
  実装：[✓](https://github.com/Gen-Verse/LatentMAS) ・ リポジトリ内被引用：2  
  LatentMASはこの境界を変え、エージェントが最終層の隠れ状態を連続表現のまま自己回帰生成し、層ごとの鍵・値キャッシュ（KVキャッシュ）を共有作業メモリとして次のエージェントへ渡す。著者は既存モデルを追加学習しない訓練不要方式として設計し、入力埋め込みと最終層隠れ状態の分布の違いを補正する線形写像を組み込む。

- **2026-04 · [MoEITS: A Green AI approach for simplifying MoE-LLMs](2026-2604.10603-moeits-a-green-ai-approach-for-simplifying-moe-llms.md)**  
  実装：[✓](https://github.com/luisbalru/MoEITS) ・ リポジトリ内被引用：1  
  一方、推論時に毎回使わないエキスパートも重みとして保持する必要があり、GPUやホスト側のメモリ容量、モデル配備コスト、エネルギー消費が大きくなる。方式は単純な利用頻度ベースの削除ではない。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [PrefixBench-H100: Characterizing Prefix Reuse and Time-to-First-Token in H100 LLM Serving](2026-2609.19657-prefixbench-h100-prefix-reuse-ttft.md)**  
  実装：[✓](https://doi.org/10.5281/zenodo.21725505) ・ リポジトリ内被引用：0  
  単一H100 NVL上でvLLMとTensorRT-LLMへ同じ要求列を送り、接頭辞キャッシュそのものの効果、容量超過、要求スケジューリングの差を切り分ける実測ベンチマーク。

- **2026-09 · [Predict, Don't Iterate: Efficient Adaptive-Length Infilling for Diffusion Language Models](2026-2609.02108-predict-don-t-iterate-efficient-adaptive-length-infilling-for-diffusion-.md)**  
  実装：[✓](https://github.com/Hsu1023/PILL) ・ リポジトリ内被引用：0  
  PILLは、拡散言語モデル（diffusion language モデル）が文章やプログラムの既知の前半と後半の間を補完する課題（infilling）において、欠落部分の長さをあらかじめ固定しなければならない制約を扱う。既存の可変長方式は長さを反復探索したり生成途中に伸縮操作を挿入したりするため、推論回数が増える。

- **2026-08 · [Diagnose Before You Compress: Prediction-Independent Bottleneck Witness Refinement for LLM Serving Traces](2026-2608.00423-bottleneck-preserving-witnessing.md)**  
  実装：[✓](https://github.com/llmllmllm/BPW) ・ リポジトリ内被引用：0  
  スケジューリング・入力処理・生成・KVキャッシュの各ボトルネックを実機測定で独立確認し、四要素すべてに複数の証拠を残す小さなLLMサービング再生用トレースを選ぶ。

- **2026-06 · [Benchmarking LLM Serving Systems for Agentic AI Workloads with XPerf](2026-2608.20370-xperf-benchmarking-llm-serving-agentic-ai-workloads.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント実行を呼出し依存グラフとして記録・再生し、8種類の実アプリでサービング負荷とハードウェア指標を再現可能に測る評価基盤を提示する。

- **2026-04 · [Reasoning Language Model Inference Serving Unveiled: An Empirical Study](2025-2510.18672-reasoning-language-model-inference-serving-unveiled.md)**  
  実装：[✓](https://github.com/lqinfdim/RLMServing) ・ リポジトリ内被引用：0  
  推論大規模言語モデルは通常の言語モデルと異なり、キャッシュ使用量が大きく変動し、少数の遅い要求が処理全体を引き延ばす。著者らは評価枠組みASUとベンチマークASU-Perfを導入し、複数のサービング最適化がモデル規模や負荷によって効いたり逆効果になったりすることを、実機評価と到着負荷の再現で示す。

- **2026-04 · [Comparative Characterization of KV Cache Management Strategies for LLM Inference](2026-2604.05012-comparative-characterization-kv-cache-management-strategies-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  vLLM、H2O、InfiniGenをH100実機で比較し、GPUメモリを最大約70%減らすH2O、初期事実を保ちやすいInfiniGen、速度に優れるvLLMの条件別の使い分けを明らかにする。

### 2年前（2024-11〜2025-10）

- **2025-05 · [ServeGen: Workload Characterization and Generation of Large Language Model Serving in Production](2026-2505.09999-servegen-workload-characterization-and-generation-of-large-language-mode.md)**  
  実装：[✓](https://github.com/alibaba/ServeGen) ・ リポジトリ内被引用：17  
  4か月・12モデル・35.4億要求の本番記録から、到着率、バースト、入力・出力長、画像・音声・動画、推論過程の分布を分析する。顧客ごとの比較的安定した特性と時間変動する到着率を合成し、現実的な推論ベンチマークを作る。

- **2024-11 · [Lynx: Enabling Efficient MoE Inference through Dynamic Batch-Aware Expert Selection](2024-2411.08982-lynx-enabling-efficient-moe-inference-through-dynamic-batch-aware-expert.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  演算の疎性が、専門家重みを高帯域メモリから読み出す量の削減につながらなくなる。Lynxはこの矛盾を、モデルの重みを恒久的に枝刈りするのでなく、現在のバッチのルーター出力を再配置することで緩和する。通常の同居配置で出力トークン間隔の中央値を1.09～1.30倍短縮し、精度変化を概ね1ポイント以内に抑える。

- **2025-02 · [KernelBench: Can LLMs Write Efficient GPU Kernels?](2025-2502.10517-kernelbench-can-llms-write-efficient-gpu-kernels.md)**  
  実装：[✓](https://github.com/ScalingIntelligence/KernelBench) ・ リポジトリ内被引用：8  
  GPUカーネル最適化では「同じ出力を返すコードを書ける」だけでは不十分で、参照実装より実測で速くなければ意味がない。生成物は自動でコンパイル・正当性検証・時間測定されるため、一般的なコード ベンチマークより「GPU固有の性能工学」を直接評価する。

- **2025-07 · [LIMINAL: Exploring The Frontiers of LLM Decode Performance](2025-2507.14397-liminal-exploring-the-frontiers-of-llm-decode-performance.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  LIMINALは、自己回帰デコードの上限を、モデル側の演算・重み・キー・バリュー（Key-Value; KV）キャッシュ需要と、加速器側の演算性能・メモリ容量・帯域・集合通信性能へ分解する解析性能モデルである。

- **2025-06 · [Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference](2025-2506.09501-understanding-and-mitigating-numerical-sources-of-nondeterminism-in-llm-inference.md)**  
  実装：[✓](https://github.com/nanomaoli/llm_reproducibility) ・ リポジトリ内被引用：6  
  「温度0の貪欲復号なら同じモデルは同じ答えを返す」という前提が、GPU数・GPU種類・バッチサイズによる浮動小数点演算順序の変化だけでも崩れることを系統的に示し、重みの保存精度と計算精度を分離するLayerCastで再現性を改善する研究。

- **2024-12 · [Don't Do RAG: When Cache-Augmented Generation is All You Need for Knowledge Tasks](2024-2412.15605-don-t-do-rag-when-cache-augmented-generation-is-all-you-need-for-knowled.md)**  
  実装：[✓](https://github.com/hhhuang/CAG) ・ リポジトリ内被引用：5  
  著者らはキャッシュ拡張生成（Cache-Augmented Generation、CAG）を提案する。Llama 3.1 8BをV100×8で評価した結果、SQuADとHotPotQAの多くの知識集合でCAGの回答品質は疎検索・密検索を用いるRAGと同等以上である。

- **2025-02 · [Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach](2025-2502.05171-scaling-up-test-time-compute-with-latent-reasoning-a-recurrent-depth-app.md)**  
  実装：[✓](https://github.com/seal-rg/recurrent-pretraining) ・ リポジトリ内被引用：4  
  この研究は、推論時の計算量を思考連鎖（chain-of-thought; CoT）の出力トークン数ではなく、モデル内部の反復深さで増やす。入力を処理するprelude、共有されるrecurrent core、出力を作るcodaにTransformerを分け、coreを推論時に何回でも反復する。

- **2025-03 · [Stop Overthinking: A Survey on Efficient Reasoning for Large Language Models](2025-2503.16419-stop-overthinking-a-survey-on-efficient-reasoning-for-large-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  モデル自体に短い推論を学習させる方式、推論の出力軌跡を途中で圧縮・制御する方式、入力の難度や指示に応じて推論量を変える方式である。

### 3年前（2023-11〜2024-10）

- **2024-01 · [BurstGPT: A Real-world Workload Dataset to Optimize LLM Serving Systems](2024-2401.17644-burstgpt-real-world-llm-serving-workload-dataset.md)**  
  実装：[✓](https://github.com/HPMLL/BurstGPT) ・ リポジトリ内被引用：31  
  Azure OpenAI GPTサービスの1031万件・213日分の実トレースと再生基盤BurstGPT-Perfを公開し、平均RPSだけを揃えた合成負荷では見えないバースト、会話間隔、応答長、失敗がサービング評価の結論を変えることを示す。

- **2024-04 · [Toward Inference-optimal Mixture-of-Expert Large Language Models](2024-2404.02852-toward-inference-optimal-mixture-of-expert-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  MoEのスケーリング則へ推論費用を組み込み、専門家数を増やした「損失最適」構成より、小さなMoEを多くのデータで学習する構成が配信費用まで含めて有利になる領域を示す。

- **2024-02 · [A Comprehensive Evaluation of Quantization Strategies for Large Language Models](2024-2402.16775-a-comprehensive-evaluation-of-quantization-strategies-for-large-language.md)**  
  実装：[✓](https://github.com/cordercorder/quant_eval) ・ リポジトリ内被引用：5  
  量子化は重みや活性値を少ないビット数で表し、GPUメモリ容量とデータ転送量を減らす代表的なLLM圧縮手法である。結果として、4ビット量子化は多くの条件で非量子化モデルに近い下流性能を維持する。

- **2024-03 · [The Unreasonable Ineffectiveness of the Deeper Layers](2024-2403.17887-the-unreasonable-ineffectiveness-of-the-deeper-layers.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  枝刈り（枝刈り）方法自体は単純で、ある長さ n の連続層 ブロックについて、そのブロックへの入力表現と通過後表現の角距離（angular distance）を測る。

- **2024-01 · [Escape Sky-high Cost: Early-stopping Self-Consistency for Multi-step Reasoning](2024-2401.10480-escape-sky-high-cost-early-stopping-self-consistency-for-multi-step-reas.md)**  
  実装：[✓](https://github.com/Yiwei98/ESC) ・ リポジトリ内被引用：2  
  多段階推論では、単一の思考連鎖（Chain-of-Thought、CoT）だけで回答すると、途中の偶然の誤りがそのまま最終回答に伝わる。自己整合性（自己整合性、SC）は同一問題から複数の思考連鎖を独立に標本化し、最終回答を多数決してこの変動を抑える。しかしSCは難しい問題にも簡単な問題にも、事前に決めた最大標本数を一律に使う。

### 4年前（2022-11〜2023-10）

- **2023-10 · [From Words to Watts: Benchmarking the Energy Costs of Large Language Model Inference](2023-2310.03003-from-words-to-watts-benchmarking-the-energy-costs-of-large-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  対象は初代LLaMAの7B、13B、65Bで、NVIDIA V100とA100、自然言語指示のAlpaca、算術問題のGSM8Kを用いる。この研究は新しい注意演算や復号アルゴリズムを提案するものではない。

### 6年前（2020-11〜2021-10）

- **2021-10 · [Efficiently Modeling Long Sequences with Structured State Spaces](2021-2111.00396-efficiently-modeling-long-sequences-with-structured-state-spaces.md)**  
  実装：[✓](https://github.com/HazyResearch/state-spaces) ・ リポジトリ内被引用：23  
  自己注意（self-注意機構）は系列長Lに対して二次の注意行列を作るため、1万〜数万ステップの系列では計算・メモリ負荷が大きくなる。論文はLong Range Arena（LRA）の全課題で当時の最良水準を更新し、長さ16,384のPath-Xで88%正解率を達成した。
<!-- survey:auto:end -->
