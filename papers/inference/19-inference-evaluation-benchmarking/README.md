<!-- survey:auto:start -->
## 自動生成の論文一覧（49本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2025-11 · [Latent Collaboration in Multi-Agent Systems](2025-2511.20639-latent-collaboration-in-multi-agent-systems.md)**  
  実装：[✓](https://github.com/Gen-Verse/LatentMAS) ・ リポジトリ内被引用：6  
  LatentMASはこの境界を変え、エージェントが最終層の隠れ状態を連続表現のまま自己回帰生成し、層ごとの鍵・値キャッシュ（KVキャッシュ）を共有作業メモリとして次のエージェントへ渡す。著者は既存モデルを追加学習しない訓練不要方式として設計し、入力埋め込みと最終層隠れ状態の分布の違いを補正する線形写像を組み込む。

- **2026-03 · [AIMER: Calibration-Free Task-Agnostic MoE Expert Pruning](2026-2603.18492-aimer-calibration-free-task-agnostic-moe-expert-pruning.md)**  
  実装：[✓](https://github.com/ZongfangLiu/AIMER) ・ リポジトリ内被引用：5  
  特にGPUメモリが限られる場合、未使用時間の長い専門家であっても保存・読込み費用がかかる。この方式は代表入力の分布に依存し、校正用入力の収集・推論・統計保存が必要となる。Qwen3-30Bの専門家50%削減ではコード評価平均がAIMERで0.361、REAPで0.046となった。

- **2025-12 · [Less Is More, but Where? Dynamic Token Compression via LLM-Guided Keyframe Prior](2025-2512.06866-less-is-more-but-where-dynamic-token-compression-via-llm-guided-keyframe.md)**  
  実装：[✓](https://github.com/yu-lin-li/DyToK) ・ リポジトリ内被引用：2  
  映像が長くなると入力トークン数が増え、自己注意と全結合層の計算費用、入力事前充填の遅延、メモリ消費が増える。既存の視覚トークン圧縮は、各フレームに同じ保持率を適用する場合が多い。

- **2026-04 · [NeuReasoner: Towards Explainable, Controllable, and Unified Reasoning via Mixture-of-Neurons](2026-2604.02972-neureasoner-towards-explainable-controllable-and-unified-reasoning-via-m.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  失敗を、単一推論段階内の計算・論理誤り、複数段階間で同じ考えを繰り返す停滞、問題の難易度に対して考え過ぎる過剰思考の三つに分類する。原著付録のA100実測では、監視と介入を加えた方式の実行時間が元モデルより増えている。

- **2026-04 · [MoEITS: A Green AI approach for simplifying MoE-LLMs](2026-2604.10603-moeits-a-green-ai-approach-for-simplifying-moe-llms.md)**  
  実装：[✓](https://github.com/luisbalru/MoEITS) ・ リポジトリ内被引用：1  
  一方、推論時に毎回使わないエキスパートも重みとして保持する必要があり、GPUやホスト側のメモリ容量、モデル配備コスト、エネルギー消費が大きくなる。方式は単純な利用頻度ベースの削除ではない。

- **2026-03 · [QMoP: Query Guided Mixture-of-Projector for Efficient Visual Token Compression](2026-2603.21232-qmop-query-guided-mixture-of-projector-for-efficient-visual-token-compre.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  QMoP（Query Guided Mixture-of-Projector）は、マルチモーダル大規模言語モデル（Multimodal Large Language モデル、MLLM）の画像トークン数を減らす際に、一つの固定圧縮法では画像と質問の組合せによって必要な情報を失うという問題を扱う。

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

- **2026-07 · [CORVUS: Context Optimization and Reduction Via Underlying Synchronization for LLM Coding Agents](2026-2607.22711-corvus-context-optimization-and-reduction-via-underlying-synchronization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  コード編集を行う大規模言語モデル（LLM）エージェントは、ファイル読込み、編集、試験、再読込みを何度も繰り返す。従来の追記専用履歴では、読込み時のファイル本文が道具の観測結果として永久に残り、後で同じファイルが変更されても古い本文は削除されない。エージェントがその古い記述を使って修正すると、適用位置の不一致や失敗が起こり、さらに再読込みと再試行を繰り返す。

- **2026-07 · [Benchmarking Confidential GPU Inference on NVIDIA H100 under Intel TDX](2026-2607.19353-benchmarking-confidential-gpu-inference-on-nvidia-h100-under-intel-tdx.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  原著はサービス指標の比較研究であり、GPU内部の暗号化処理、PCIe転送、HBM帯域、スケジューラのどれが何%の原因かまで分解したマイクロアーキテクチャ解析ではない。

- **2026-06 · [Benchmarking LLM Serving Systems for Agentic AI Workloads with XPerf](2026-2608.20370-xperf-benchmarking-llm-serving-agentic-ai-workloads.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント実行を呼出し依存グラフとして記録・再生し、8種類の実アプリでサービング負荷とハードウェア指標を再現可能に測る評価基盤を提示する。

- **2026-05 · [PARCEL: Pool-Anchored Resampling with Conditioned Elastic Queries for Efficient Vision-Language Understanding](2026-2605.30126-parcel-pool-anchored-resampling-with-conditioned-elastic-queries-for-eff.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PARCELは、視覚トークンの数を16、64、256など異なる予算へ縮めても、空間的な位置関係と画像の細部を両立して保つための、可変予算の視覚表現設計である。27種類の評価課題を横断した全体平均の性能保持率は、視覚トークン256個で95.6%、64個で95.3%、16個で88.3%と報告された。

- **2026-05 · [Linear Scaling Video VLMs for Long Video Understanding](2026-2605.31598-linear-scaling-video-vlms-for-long-video-understanding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い動画を視覚言語モデル（Vision-Language モデル; VLM）へ入力すると、映像から得られる視覚トークンが時間とともに増え、各フレームが過去の全フレームへ自己注意（self-注意機構）を計算する通常の実装では、全映像を処理する事前充填（プリフィル）の計算量がフレーム数 N に対して二次的に増える。

- **2026-05 · [Evading Visual Aphasia: Contrastive Adaptive Semantic Token Pruning for Vision-Language Models](2026-2605.09429-evading-visual-aphasia-contrastive-adaptive-semantic-token-pruning-for-v.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  たとえば、画像内で目立つ動物より周辺の店名看板を尋ねているのに、初期層の注意が動物へ集中した結果、看板のトークンが枝刈りされ、モデルが架空の店名を答える。LLaVA-v1.5-7Bで画像トークンを576個から128個へ77.8%削減した条件では、七つの評価セットを正規化した平均性能を98.64%保持し、遅延を167.50ミリ秒から77.94ミリ秒へ短縮した。

- **2026-05 · [EarlyTom: Early Token Compression Completes Fast Video Understanding](2026-2605.30010-earlytom-early-token-compression-completes-fast-video-understanding.md)**  
  実装：[✓](https://github.com/viridisGreen/EarlyTom) ・ リポジトリ内被引用：0  
  既存の圧縮方式の多くは、視覚符号化器が全トークンを処理し終えた後に間引く。単一NVIDIA A100上のLLaVA-OneVision-7Bでは、言語モデルへ入る視覚トークンを元の10%に保つ条件で、最初のトークンまでの時間（Time to First Token; TTFT）が889.9ミリ秒から336.2ミリ秒へ短縮し、約2.65倍の逆数比となる。

- **2026-04 · [Watt Counts: Energy-Aware Benchmark for Sustainable LLM Inference on Heterogeneous GPU Architectures](2026-2604.09048-watt-counts-energy-aware-benchmark-for-sustainable-llm-inference-on-hete.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  逆に常時待機する低負荷サーバでは、ピーク処理能力よりアイドル時の消費電力が支配的になり、別のGPUが有利になり得る。Watt Countsは、こうしたモデル、GPU、運用負荷の三者の相互作用を比較するための公開データセットと測定基盤を提案する。

- **2026-04 · [SMoES: Soft Modality-Guided Expert Specialization in MoE-VLMs](2026-2604.23996-smoes-soft-modality-guided-expert-specialization-in-moe-vlms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SMoES（Soft Modality-guided 専門家 Specialization）は、視覚・言語モデル（Vision-Language モデル, VLM）の専門家混合（Mixture of エキスパート, MoE）層で、画像由来トークンと文章由来トークンが各層でどの程度混合しているかを推定し、専門家の配置と学習を調整する方式である。

- **2026-04 · [Reasoning Language Model Inference Serving Unveiled: An Empirical Study](2025-2510.18672-reasoning-language-model-inference-serving-unveiled.md)**  
  実装：[✓](https://github.com/lqinfdim/RLMServing) ・ リポジトリ内被引用：0  
  推論大規模言語モデルは通常の言語モデルと異なり、キャッシュ使用量が大きく変動し、少数の遅い要求が処理全体を引き延ばす。著者らは評価枠組みASUとベンチマークASU-Perfを導入し、複数のサービング最適化がモデル規模や負荷によって効いたり逆効果になったりすることを、実機評価と到着負荷の再現で示す。

- **2026-04 · [EvoComp: Learning Visual Token Compression for Multimodal Large Language Models via Semantic-Guided Evolutionary Labeling](2026-2604.17087-evocomp-learning-visual-token-compression-for-multimodal-large-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル時の注意演算、鍵・値（KV）キャッシュ、入力列の読み込みが増え、初回応答の待ち時間が長くなる。EvoCompは、視覚トークンのうち質問への回答に必要なものだけを選び、下流LLMへ渡す系列長を減らす方式である。LLaVA-1.5-7Bでは576トークンを192に削減したとき、6ベンチマークの平均成績を元モデルの99.3%に保つ。

- **2026-04 · [Comparative Characterization of KV Cache Management Strategies for LLM Inference](2026-2604.05012-comparative-characterization-kv-cache-management-strategies-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  vLLM、H2O、InfiniGenをH100実機で比較し、GPUメモリを最大約70%減らすH2O、初期事実を保ちやすいInfiniGen、速度に優れるvLLMの条件別の使い分けを明らかにする。

- **2026-04 · [Beyond Accuracy: Unveiling Inefficiency Patterns in Tool-Integrated Reasoning](2026-2604.05404-beyond-accuracy-unveiling-inefficiency-patterns-in-tool-integrated-reaso.md)**  
  実装：[✓](https://github.com/sqs-ustc/tool-reasoning-framework-PTE) ・ リポジトリ内被引用：0  
  本論文は、推論と外部ツール利用を交互に行うツール統合推論（tool-integrated reasoning; TIR）の計算費用の測り方を提案する。

- **2026-03 · [Unified Spatiotemporal Token Compression for Video-LLMs at Ultra-Low Retention](2026-2603.21957-unified-spatiotemporal-token-compression-for-video-llms-at-ultra-low-ret.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既存の手法はフレーム内の空間圧縮とフレーム間の時間圧縮を順番に適用するものが多いが、保持率を5%以下まで下げると、先に決めた各段階の予算配分が適切でなくなり、質問に必要な短い出来事や小さな物体を落としやすい。

- **2026-03 · [Token Reduction via Local and Global Contexts Optimization for Efficient Video Large Language Models](2026-2603.01400-token-reduction-via-local-and-global-contexts-optimization-for-efficient.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AOT（local-global Anchor Optimal Transport）は、動画対応の大規模言語モデル（Video LLM）の入力に含まれる視覚トークンを、追加学習なしで削減する方式である。LLaVA-OneVision-7Bの無圧縮平均58.4に対し、視覚トークン10%保持のAOTは平均57.0で、元性能の97.6%を維持した。

- **2026-03 · [Spend Less, Reason Better: Budget-Aware Value Tree Search for LLM Agents](2026-2603.12634-spend-less-reason-better-budget-aware-value-tree-search-for-llm-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  実サービスではツール呼び出し回数、生成トークン数、API料金に上限があるため、単に推論を長くする方式は適さない。原著はgpt-oss-20bとQwen3-30B-A3B-Instruct-2507を用い、HotpotQA、2WikiMultihopQA、MuSiQue、Bamboogleで評価した。

- **2026-02 · [Parallel-Probe: Towards Efficient Parallel Thinking via 2D Probing](2026-2602.03845-parallel-probe-towards-efficient-parallel-thinking-via-2d-probing.md)**  
  実装：[✓](https://github.com/zhengkid/Parallel-Probe) ・ リポジトリ内被引用：0  
  多数派の答えが途中で既に確定していても、最後まで生成する方式では長い少数経路の完了待ちと総生成トークンが残る。論文の表1では、Qwen3-0.6Bの数学3ベンチマーク平均で、固定64経路の多数決に比べ正答率22.8%から23.3%へ変化しつつ、逐次トークン31.6千個から20.3千個、総トークン945.7千個から735.3千個へ減少した。

- **2026-02 · [On the Optimal Reasoning Length for RL-Trained Language Models](2026-2602.09591-on-the-optimal-reasoning-length-for-rl-trained-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長くすることで最頻回答が正解になる問題は増えるが、その正解周辺に個々の標本が集中しなくなるため、単発回答の成功率が下がり得る。

- **2026-01 · [L³: Large Lookup Layers](2026-2601.21461-l-large-lookup-layers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  このため、CPUに退避した専門家をGPUへ移す場合は、選択後の転送が計算の待ち時間になりやすい。推論速度はL³の配置に依存し、2.6B稼働モデルで最初のL³を第5層後に置くと、原著表2のバッチ1速度は密モデル776に対して772トークン/秒/系列だった。

- **2025-11 · [MemSearcher: Training LLMs to Reason, Search and Manage Memory via End-to-End Reinforcement Learning](2025-2511.02805-memsearcher-training-llms-to-reason-search-and-manage-memory-via-end-to-.md)**  
  実装：[✓](https://github.com/icip-cas/MemSearcher) ・ リポジトリ内被引用：0  
  検索エージェント（search agent）が外部検索を何度も行うと、思考、検索クエリ、検索結果を全て会話履歴に追記する従来のReAct方式では、ターンが増えるにつれて入力文脈が長くなる。検索エージェントの入力文脈はほぼ一定長で、論文の評価条件では4,000トークン未満を維持する。

### 2年前（2024-11〜2025-10）

- **2025-05 · [ServeGen: Workload Characterization and Generation of Large Language Model Serving in Production](2026-2505.09999-servegen-workload-characterization-and-generation-of-large-language-mode.md)**  
  実装：[✓](https://github.com/alibaba/ServeGen) ・ リポジトリ内被引用：21  
  4か月・12モデル・35.4億要求の本番記録から、到着率、バースト、入力・出力長、画像・音声・動画、推論過程の分布を分析する。顧客ごとの比較的安定した特性と時間変動する到着率を合成し、現実的な推論ベンチマークを作る。

- **2025-03 · [Stop Overthinking: A Survey on Efficient Reasoning for Large Language Models](2025-2503.16419-stop-overthinking-a-survey-on-efficient-reasoning-for-large-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  モデル自体に短い推論を学習させる方式、推論の出力軌跡を途中で圧縮・制御する方式、入力の難度や指示に応じて推論量を変える方式である。

- **2025-02 · [KernelBench: Can LLMs Write Efficient GPU Kernels?](2025-2502.10517-kernelbench-can-llms-write-efficient-gpu-kernels.md)**  
  実装：[✓](https://github.com/ScalingIntelligence/KernelBench) ・ リポジトリ内被引用：12  
  一般的なプログラム合成では単体試験に通ることを重視するが、GPUカーネルの実用性は入力形状、メモリ階層、並列実行、命令セットに左右される。正しくても遅い実装を成功とみなさないことが設計の中心にある。例えばDeepSeek-R1の fast1 は単一演算12%、複合演算36%、モデル全体2%である。

- **2024-11 · [Lynx: Enabling Efficient MoE Inference through Dynamic Batch-Aware Expert Selection](2024-2411.08982-lynx-enabling-efficient-moe-inference-through-dynamic-batch-aware-expert.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  演算の疎性が、専門家重みを高帯域メモリから読み出す量の削減につながらなくなる。Lynxはこの矛盾を、モデルの重みを恒久的に枝刈りするのでなく、現在のバッチのルーター出力を再配置することで緩和する。通常の同居配置で出力トークン間隔の中央値を1.09～1.30倍短縮し、精度変化を概ね1ポイント以内に抑える。

- **2025-01 · [LLaVA-Mini: Efficient Image and Video Large Multimodal Models with One Vision Token](2025-2501.03895-llava-mini-efficient-image-and-video-large-multimodal-models-with-one-vi.md)**  
  実装：[✓](https://github.com/ictnlp/LLaVA-Mini) ・ リポジトリ内被引用：11  
  画像を1枚だけ扱う場合でも自己注意と中間活性の負荷が増え、動画ではフレーム数にほぼ比例して言語モデルの文脈が膨らむ。別の学習可能なクエリを使った圧縮器が、言語モデルへ渡す視覚トークンを最少1個にする。

- **2025-07 · [LIMINAL: Exploring The Frontiers of LLM Decode Performance](2025-2507.14397-liminal-exploring-the-frontiers-of-llm-decode-performance.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  LIMINALは、自己回帰デコードの上限を、モデル側の演算・重み・キー・バリュー（Key-Value; KV）キャッシュ需要と、加速器側の演算性能・メモリ容量・帯域・集合通信性能へ分解する解析性能モデルである。

- **2025-02 · [Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach](2025-2502.05171-scaling-up-test-time-compute-with-latent-reasoning-a-recurrent-depth-app.md)**  
  実装：[✓](https://github.com/seal-rg/recurrent-pretraining) ・ リポジトリ内被引用：7  
  この研究は、推論時の計算量を思考連鎖（chain-of-thought; CoT）の出力トークン数ではなく、モデル内部の反復深さで増やす。入力を処理するprelude、共有されるrecurrent core、出力を作るcodaにTransformerを分け、coreを推論時に何回でも反復する。

- **2025-06 · [Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference](2025-2506.09501-understanding-and-mitigating-numerical-sources-of-nondeterminism-in-llm-inference.md)**  
  実装：[✓](https://github.com/nanomaoli/llm_reproducibility) ・ リポジトリ内被引用：6  
  「温度0の貪欲復号なら同じモデルは同じ答えを返す」という前提が、GPU数・GPU種類・バッチサイズによる浮動小数点演算順序の変化だけでも崩れることを系統的に示し、重みの保存精度と計算精度を分離するLayerCastで再現性を改善する研究。

- **2024-12 · [Don't Do RAG: When Cache-Augmented Generation is All You Need for Knowledge Tasks](2024-2412.15605-don-t-do-rag-when-cache-augmented-generation-is-all-you-need-for-knowled.md)**  
  実装：[✓](https://github.com/hhhuang/CAG) ・ リポジトリ内被引用：6  
  著者らはキャッシュ拡張生成（Cache-Augmented Generation、CAG）を提案する。Llama 3.1 8BをV100×8で評価した結果、SQuADとHotPotQAの多くの知識集合でCAGの回答品質は疎検索・密検索を用いるRAGと同等以上である。

- **2025-07 · [Collaborative Inference and Learning between Edge SLMs and Cloud LLMs: A Survey of Algorithms, Execution, and Open Challenges](2025-2507.16731-collaborative-inference-and-learning-between-edge-slms-and-cloud-llms-a-.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  端末で簡単な要求を処理し、必要な時だけクラウドを呼ぶ方式は自然だが、呼出し回数が増えれば往復遅延が支配的になる。

### 3年前（2023-11〜2024-10）

- **2024-01 · [BurstGPT: A Real-world Workload Dataset to Optimize LLM Serving Systems](2024-2401.17644-burstgpt-real-world-llm-serving-workload-dataset.md)**  
  実装：[✓](https://github.com/HPMLL/BurstGPT) ・ リポジトリ内被引用：41  
  Azure OpenAI GPTサービスの1031万件・213日分の実トレースと再生基盤BurstGPT-Perfを公開し、平均RPSだけを揃えた合成負荷では見えないバースト、会話間隔、応答長、失敗がサービング評価の結論を変えることを示す。

- **2024-03 · [The Unreasonable Ineffectiveness of the Deeper Layers](2024-2403.17887-the-unreasonable-ineffectiveness-of-the-deeper-layers.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  削除したい層数を決め、入力・出力間の角距離が最小の連続ブロックを選択し、実際に層を除去する。Llama-2系列の5-shot MMLUでは削除率45〜55%付近で急落するが、Qwen系列では約20%付近で急落する。

- **2024-01 · [Escape Sky-high Cost: Early-stopping Self-Consistency for Multi-step Reasoning](2024-2401.10480-escape-sky-high-cost-early-stopping-self-consistency-for-multi-step-reas.md)**  
  実装：[✓](https://github.com/Yiwei98/ESC) ・ リポジトリ内被引用：8  
  多段階推論では、単一の思考連鎖（Chain-of-Thought、CoT）だけで回答すると、途中の偶然の誤りがそのまま最終回答に伝わる。自己整合性（自己整合性、SC）は同一問題から複数の思考連鎖を独立に標本化し、最終回答を多数決してこの変動を抑える。しかしSCは難しい問題にも簡単な問題にも、事前に決めた最大標本数を一律に使う。

- **2024-02 · [A Comprehensive Evaluation of Quantization Strategies for Large Language Models](2024-2402.16775-a-comprehensive-evaluation-of-quantization-strategies-for-large-language.md)**  
  実装：[✓](https://github.com/cordercorder/quant_eval) ・ リポジトリ内被引用：7  
  本論文は、新しい量子化器を提案するものではなく、既存の量子化方式をモデル能力、指示追従・整合性、推論効率という異なる観点で測り直す比較実験である。論文のSpQR実装は低ビットの値域を模擬しながら高精度形式で重みを保持しており、品質の比較には使えても実メモリ削減を実証しない。

- **2024-04 · [Toward Inference-optimal Mixture-of-Expert Large Language Models](2024-2404.02852-toward-inference-optimal-mixture-of-expert-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  MoEのスケーリング則へ推論費用を組み込み、専門家数を増やした「損失最適」構成より、小さなMoEを多くのデータで学習する構成が配信費用まで含めて有利になる領域を示す。

- **2024-02 · [Benchmarking and Dissecting the Nvidia Hopper GPU Architecture](2024-2402.13499-benchmarking-and-dissecting-the-nvidia-hopper-gpu-architecture.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  Hopper世代のGPUは第4世代テンソル Core、8ビット浮動小数点（FP8）、ワープグループ行列積（wgmma）、動的計画法命令（DPX）、テンソルメモリアクセラレータ（TMA）、分散共有メモリ（DSM）を備える。しかし仕様表のピーク演算量や帯域だけでは、行列形状、オペランド配置、電力、精度変換、カーネル起動の費用を含む実性能は分からない。

### 4年前（2022-11〜2023-10）

- **2023-10 · [From Words to Watts: Benchmarking the Energy Costs of Large Language Model Inference](2023-2310.03003-from-words-to-watts-benchmarking-the-energy-costs-of-large-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  対象は初代LLaMAの7B、13B、65Bで、NVIDIA V100とA100、自然言語指示のAlpaca、算術問題のGSM8Kを用いる。この研究は新しい注意演算や復号アルゴリズムを提案するものではない。

- **2023-09 · [Large Language Model Routing with Benchmark Datasets](2023-2309.15789-large-language-model-routing-with-benchmark-datasets.md)**  
  実装：[✓](https://github.com/UMich-FATML/llm-routing) ・ リポジトリ内被引用：6  
  しかし実際のサービスでは、数学問題、法務文書、要約、常識質問など、タスクごとに得意なモデルが異なる。常に最も大きいモデルを呼ぶ方式は品質を得やすい反面、必要以上の推論計算を消費する。これらは品質と必要なモデル呼出し回数の評価であり、実際のGPU実行時間・請求金額の削減倍率を測定したものではない（原著§5、表1・2）。

### 5年前（2021-11〜2022-10）

- **2022-02 · [A Survey on Model Compression and Acceleration for Pretrained Language Models](2022-2202.07105-a-survey-on-model-compression-and-acceleration-for-pretrained-language-m.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  著者らは推論段階を対象に、重み共有、低ランク分解、枝刈り、量子化、知識蒸留、早期終了、トークン省略の七系統を比較する。

### 6年前（2020-11〜2021-10）

- **2021-10 · [Efficiently Modeling Long Sequences with Structured State Spaces](2021-2111.00396-efficiently-modeling-long-sequences-with-structured-state-spaces.md)**  
  実装：[✓](https://github.com/HazyResearch/state-spaces) ・ リポジトリ内被引用：46  
  自己注意（self-注意機構）は系列長Lに対して二次の注意行列を作るため、1万〜数万ステップの系列では計算・メモリ負荷が大きくなる。論文はLong Range Arena（LRA）の全課題で当時の最良水準を更新し、長さ16,384のPath-Xで88%正解率を達成した。
<!-- survey:auto:end -->
