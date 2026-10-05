<!-- survey:auto:start -->
## 自動生成の論文一覧（17本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-05 · [ServeGen: Workload Characterization and Generation of Large Language Model Serving in Production](2026-2505.09999-servegen-workload-characterization-and-generation-of-large-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  提案するServeGenは負荷全体へ単一分布を当てず、顧客ごとに到着過程と入出力データ分布をモデル化して最後に合成する。

- **2025-11 · [Latent Collaboration in Multi-Agent Systems](2025-2511.20639-latent-collaboration-in-multi-agent-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  従来の複数LLMエージェントは、各エージェントが推論結果をテキストへデコードし、次のエージェントがそのテキストをtokenizeして再びプリフィルする。LatentMASはこの離散テキスト境界を外し、エージェント内部の連続表現を直接共有する。次のエージェントはその表現を再エンコードせず受け取る。

- **2026-04 · [MoEITS: A Green AI approach for simplifying MoE-LLMs](2026-2604.10603-moeits-a-green-ai-approach-for-simplifying-moe-llms.md)**  
  実装：[✓](https://github.com/luisbalru/MoEITS) ・ リポジトリ内被引用：1  
  一方、推論時に毎回使わないエキスパートも重みとして保持する必要があり、GPUやホスト側のメモリ容量、モデル配備コスト、エネルギー消費が大きくなる。方式は単純な利用頻度ベースの削除ではない。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [PrefixBench-H100: Characterizing Prefix Reuse and Time-to-First-Token in H100 LLM Serving](2026-2609.19657-prefixbench-h100-prefix-reuse-ttft.md)**  
  実装：[✓](https://doi.org/10.5281/zenodo.21725505) ・ リポジトリ内被引用：0  
  単一H100 NVL上でvLLMとTensorRT-LLMへ同じ要求列を送り、接頭辞キャッシュそのものの効果、容量超過、要求スケジューリングの差を切り分ける実測ベンチマーク。

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

- **2024-11 · [Lynx: Enabling Efficient MoE Inference through Dynamic Batch-Aware Expert Selection](2024-2411.08982-lynx-enabling-efficient-moe-inference-through-dynamic-batch-aware-expert.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  MoEは各トークンが少数専門家だけを通るため、密モデルより少ない計算でモデル容量を増やせる。しかしサービングでは複数要求の復号トークンを同一バッチへまとめる。個々のトークンの選択専門家が異なると、バッチ全体の和集合はほぼ全専門家へ広がり、結局すべての専門家重みをGPUメモリから読む。計算疎性がメモリ帯域削減へつながらないことがLYNXの出発点である。

- **2025-07 · [LIMINAL: Exploring The Frontiers of LLM Decode Performance](2025-2507.14397-liminal-exploring-the-frontiers-of-llm-decode-performance.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  LIMINALは、自己回帰デコードの上限を、モデル側の演算・重み・キー・バリュー（Key-Value; KV）キャッシュ需要と、加速器側の演算性能・メモリ容量・帯域・集合通信性能へ分解する解析性能モデルである。

- **2025-06 · [Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference](2025-2506.09501-understanding-and-mitigating-numerical-sources-of-nondeterminism-in-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  「温度0の貪欲復号なら同じモデルは同じ答えを返す」という前提が、GPU数・GPU種類・バッチサイズによる浮動小数点演算順序の変化だけでも崩れることを系統的に示し、重みの保存精度と計算精度を分離するLayerCastで再現性を改善する研究。

- **2025-03 · [Stop Overthinking: A Survey on Efficient Reasoning for Large Language Models](2025-2503.16419-stop-overthinking-a-survey-on-efficient-reasoning-for-large-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  単に小型モデル化する研究だけでなく、推論中に思考長を動的に減らす方式や、プロンプト側から必要計算量を制御する方式まで同じ地図に置く。

- **2025-02 · [Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach](2025-2502.05171-scaling-up-test-time-compute-with-latent-reasoning-a-recurrent-depth-app.md)**  
  実装：[✓](https://github.com/seal-rg/recurrent-pretraining) ・ リポジトリ内被引用：3  
  この研究は、推論時の計算量を思考連鎖（chain-of-thought; CoT）の出力トークン数ではなく、モデル内部の反復深さで増やす。入力を処理するprelude、共有されるrecurrent core、出力を作るcodaにTransformerを分け、coreを推論時に何回でも反復する。

- **2024-12 · [Don't Do RAG: When Cache-Augmented Generation is All You Need for Knowledge Tasks](2024-2412.15605-don-t-do-rag-when-cache-augmented-generation-is-all-you-need-for-knowled.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  キャッシュ拡張生成（CAG）は、知識集合が限定され長文脈へ収まる場合、検索拡張生成（RAG）の実時間検索を省き、知識文書を事前にプリフィルしてKVキャッシュを保持する。質問時はこのキャッシュを再利用して検索待ちと検索誤りを除き、複数QAベンチマークでRAGと同等以上の品質と低遅延を示す。

### 3年前（2023-11〜2024-10）

- **2024-01 · [BurstGPT: A Real-world Workload Dataset to Optimize LLM Serving Systems](2024-2401.17644-burstgpt-real-world-llm-serving-workload-dataset.md)**  
  実装：[✓](https://github.com/HPMLL/BurstGPT) ・ リポジトリ内被引用：30  
  Azure OpenAI GPTサービスの1031万件・213日分の実トレースと再生基盤BurstGPT-Perfを公開し、平均RPSだけを揃えた合成負荷では見えないバースト、会話間隔、応答長、失敗がサービング評価の結論を変えることを示す。

- **2024-04 · [Toward Inference-optimal Mixture-of-Expert Large Language Models](2024-2404.02852-toward-inference-optimal-mixture-of-expert-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  MoEのスケーリング則へ推論費用を組み込み、専門家数を増やした「損失最適」構成より、小さなMoEを多くのデータで学習する構成が配信費用まで含めて有利になる領域を示す。

### 4年前（2022-11〜2023-10）

- **2023-10 · [From Words to Watts: Benchmarking the Energy Costs of Large Language Model Inference](2023-2310.03003-from-words-to-watts-benchmarking-the-energy-costs-of-large-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  本論文は新しい高速化方式を提案するのではなく、LLaMA 7B/13B/65Bを実機で動かし、スループットとGPUエネルギーを同時に測ることで、推論構成の交換条件を明らかにする。V100 32GBでは最低8枚、A100 80GBでは最低4枚が必要で、V100では8/16/32分割まで拡張する。
<!-- survey:auto:end -->
