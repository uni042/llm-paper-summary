<!-- survey:auto:start -->
## 自動生成の論文一覧（115本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/19-inference-evaluation-benchmarking/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2025-11 · [Latent Collaboration in Multi-Agent Systems](2025-2511.20639-latent-collaboration-in-multi-agent-systems.md)**  
  実装：[✓](https://github.com/Gen-Verse/LatentMAS) ・ リポジトリ内被引用：10  
  LatentMASはこの境界を変え、エージェントが最終層の隠れ状態を連続表現のまま自己回帰生成し、層ごとの鍵・値キャッシュ（KVキャッシュ）を共有作業メモリとして次のエージェントへ渡す。著者は既存モデルを追加学習しない訓練不要方式として設計し、入力埋め込みと最終層隠れ状態の分布の違いを補正する線形写像を組み込む。

- **2026-03 · [AIMER: Calibration-Free Task-Agnostic MoE Expert Pruning](2026-2603.18492-aimer-calibration-free-task-agnostic-moe-expert-pruning.md)**  
  実装：[✓](https://github.com/ZongfangLiu/AIMER) ・ リポジトリ内被引用：8  
  特にGPUメモリが限られる場合、未使用時間の長い専門家であっても保存・読込み費用がかかる。この方式は代表入力の分布に依存し、校正用入力の収集・推論・統計保存が必要となる。Qwen3-30Bの専門家50%削減ではコード評価平均がAIMERで0.361、REAPで0.046となった。

- **2025-12 · [Less Is More, but Where? Dynamic Token Compression via LLM-Guided Keyframe Prior](2025-2512.06866-less-is-more-but-where-dynamic-token-compression-via-llm-guided-keyframe.md)**  
  実装：[✓](https://github.com/yu-lin-li/DyToK) ・ リポジトリ内被引用：5  
  映像が長くなると入力トークン数が増え、自己注意と全結合層の計算費用、入力事前充填の遅延、メモリ消費が増える。既存の視覚トークン圧縮は、各フレームに同じ保持率を適用する場合が多い。

- **2026-03 · [QMoP: Query Guided Mixture-of-Projector for Efficient Visual Token Compression](2026-2603.21232-qmop-query-guided-mixture-of-projector-for-efficient-visual-token-compre.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  QMoP（Query Guided Mixture-of-Projector）は、マルチモーダル大規模言語モデル（Multimodal Large Language モデル、MLLM）の画像トークン数を減らす際に、一つの固定圧縮法では画像と質問の組合せによって必要な情報を失うという問題を扱う。

- **2026-09 · [Predict, Don't Iterate: Efficient Adaptive-Length Infilling for Diffusion Language Models](2026-2609.02108-predict-don-t-iterate-efficient-adaptive-length-infilling-for-diffusion-.md)**  
  実装：[✓](https://github.com/Hsu1023/PILL) ・ リポジトリ内被引用：2  
  PILLは、拡散言語モデル（diffusion language モデル）が文章やプログラムの既知の前半と後半の間を補完する課題（infilling）において、欠落部分の長さをあらかじめ固定しなければならない制約を扱う。既存の可変長方式は長さを反復探索したり生成途中に伸縮操作を挿入したりするため、推論回数が増える。

- **2026-04 · [Watt Counts: Energy-Aware Benchmark for Sustainable LLM Inference on Heterogeneous GPU Architectures](2026-2604.09048-watt-counts-energy-aware-benchmark-for-sustainable-llm-inference-on-hete.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  逆に常時待機する低負荷サーバでは、ピーク処理能力よりアイドル時の消費電力が支配的になり、別のGPUが有利になり得る。Watt Countsは、こうしたモデル、GPU、運用負荷の三者の相互作用を比較するための公開データセットと測定基盤を提案する。

- **2025-11 · [Revisiting Disaggregated Large Language Model Serving for Performance and Energy Implications](2026-2601.08833-revisiting-disaggregated-large-language-model-serving-for-performance-and-energy-implications.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  公平な2-GPU基準と複数KV転送階層・DVFSでプリフィル/デコード分離を再評価し、性能・省電力の優位が条件依存であることを示す。

- **2026-06 · [NLL-Guided Full-Attention Layer Selection for Training-Free Sliding-Window Adaptation](2026-2606.27791-nll-guided-full-attention-layer-selection-for-training-free-sliding-wind.md)**  
  実装：[✓](https://gitlab.com/fars-a/nll-guided-swaa-layer-selection) ・ リポジトリ内被引用：1  
  長文脈LLMの事前充填（プリフィル）では、通常の全注意（full 注意機構; FA）の計算量が入力長に対して二乗で増える。36層のQwen3-4B-Thinking-2507とLongMemEval24kの評価では、9層（1/4）を全注意としたNLL-guidedが64.6%の正解率を得た。

- **2026-05 · [EarlyTom: Early Token Compression Completes Fast Video Understanding](2026-2605.30010-earlytom-early-token-compression-completes-fast-video-understanding.md)**  
  実装：[✓](https://github.com/viridisGreen/EarlyTom) ・ リポジトリ内被引用：1  
  既存の圧縮方式の多くは、視覚符号化器が全トークンを処理し終えた後に間引く。単一NVIDIA A100上のLLaVA-OneVision-7Bでは、言語モデルへ入る視覚トークンを元の10%に保つ条件で、最初のトークンまでの時間（Time to First Token; TTFT）が889.9ミリ秒から336.2ミリ秒へ短縮し、約2.65倍の逆数比となる。

- **2026-04 · [Reasoning Language Model Inference Serving Unveiled: An Empirical Study](2025-2510.18672-reasoning-language-model-inference-serving-unveiled.md)**  
  実装：[✓](https://github.com/lqinfdim/RLMServing) ・ リポジトリ内被引用：1  
  推論大規模言語モデルは通常の言語モデルと異なり、キャッシュ使用量が大きく変動し、少数の遅い要求が処理全体を引き延ばす。著者らは評価枠組みASUとベンチマークASU-Perfを導入し、複数のサービング最適化がモデル規模や負荷によって効いたり逆効果になったりすることを、実機評価と到着負荷の再現で示す。

- **2026-04 · [NeuReasoner: Towards Explainable, Controllable, and Unified Reasoning via Mixture-of-Neurons](2026-2604.02972-neureasoner-towards-explainable-controllable-and-unified-reasoning-via-m.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  失敗を、単一推論段階内の計算・論理誤り、複数段階間で同じ考えを繰り返す停滞、問題の難易度に対して考え過ぎる過剰思考の三つに分類する。原著付録のA100実測では、監視と介入を加えた方式の実行時間が元モデルより増えている。

- **2026-04 · [MoEITS: A Green AI approach for simplifying MoE-LLMs](2026-2604.10603-moeits-a-green-ai-approach-for-simplifying-moe-llms.md)**  
  実装：[✓](https://github.com/luisbalru/MoEITS) ・ リポジトリ内被引用：1  
  一方、推論時に毎回使わないエキスパートも重みとして保持する必要があり、GPUやホスト側のメモリ容量、モデル配備コスト、エネルギー消費が大きくなる。方式は単純な利用頻度ベースの削除ではない。

- **2026-03 · [Unified Spatiotemporal Token Compression for Video-LLMs at Ultra-Low Retention](2026-2603.21957-unified-spatiotemporal-token-compression-for-video-llms-at-ultra-low-ret.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  既存の手法はフレーム内の空間圧縮とフレーム間の時間圧縮を順番に適用するものが多いが、保持率を5%以下まで下げると、先に決めた各段階の予算配分が適切でなくなり、質問に必要な短い出来事や小さな物体を落としやすい。

- **2026-03 · [Token Reduction via Local and Global Contexts Optimization for Efficient Video Large Language Models](2026-2603.01400-token-reduction-via-local-and-global-contexts-optimization-for-efficient.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  AOT（local-global Anchor Optimal Transport）は、動画対応の大規模言語モデル（Video LLM）の入力に含まれる視覚トークンを、追加学習なしで削減する方式である。LLaVA-OneVision-7Bの無圧縮平均58.4に対し、視覚トークン10%保持のAOTは平均57.0で、元性能の97.6%を維持した。

- **2026-02 · [Parallel-Probe: Towards Efficient Parallel Thinking via 2D Probing](2026-2602.03845-parallel-probe-towards-efficient-parallel-thinking-via-2d-probing.md)**  
  実装：[✓](https://github.com/zhengkid/Parallel-Probe) ・ リポジトリ内被引用：1  
  多数派の答えが途中で既に確定していても、最後まで生成する方式では長い少数経路の完了待ちと総生成トークンが残る。論文の表1では、Qwen3-0.6Bの数学3ベンチマーク平均で、固定64経路の多数決に比べ正答率22.8%から23.3%へ変化しつつ、逐次トークン31.6千個から20.3千個、総トークン945.7千個から735.3千個へ減少した。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [The Inference Engineering Pareto Atlas: Which Optimizations Dominate the Cost, Quality, and Latency Frontier?](2026-2609.17863-inference-engineering-pareto-atlas.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  54実測点と校正シミュレータで推論最適化の組合せを品質・遅延・費用の同一Pareto面へ置き、制約別の支配構成を示す。

- **2026-09 · [SiliconBench: Speed, Memory, and Fidelity for LLM Serving on Unified-Memory Desktops](2026-2609.19169-siliconbench-speed-memory-and-fidelity-for-llm-serving-on-unified-memory-desktops.md)**  
  実装：[✓](https://github.com/WindChimeRan/SiliconBench) ・ リポジトリ内被引用：0  
  Apple Siliconの九推論基盤を速度・共有メモリ・忠実度・新モデル対応・複数機で横断監査し、vllm-metalの並行処理と遠隔直接メモリアクセスを使うテンソル並列の優位を示す。

- **2026-09 · [Separating Stream Stability from Long-Term Recall in Language Models](2026-2609.07282-stream-stability-long-term-recall-threeh.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長時間生成の安定性・過去情報への因果アクセス・タスク効用をThreeHの3到達距離へ分離し、注意シンクの安定生成を長期記憶と誤認しない評価契約を示す。

- **2026-09 · [PrefixBench-H100: Characterizing Prefix Reuse and Time-to-First-Token in H100 LLM Serving](2026-2609.19657-prefixbench-h100-prefix-reuse-ttft.md)**  
  実装：[✓](https://doi.org/10.5281/zenodo.21725505) ・ リポジトリ内被引用：0  
  単一H100 NVL上でvLLMとTensorRT-LLMへ同じ要求列を送り、接頭辞キャッシュそのものの効果、容量超過、要求スケジューリングの差を切り分ける実測ベンチマーク。

- **2026-09 · [MassAlloc Attention: Let Attention Allocate Its Own Compute](2026-2609.32712-massalloc-attention-let-attention-allocate-its-own-compute.md)**  
  実装：[✓](https://github.com/HKUSTDial/flash-sparse-attention) ・ リポジトリ内被引用：0  
  MassAlloc 注意機構（MALA）は、長文脈で計算負荷が大きくなる自己注意のうち、クエリとキーの内積スコアを求めた後の処理を削減する方式である。原著は8基のH100を用いた128K系列の注意演算子ベンチマークで、全注意（Full 注意機構; FullAttn）に対し順伝播の遅延を2.2倍、逆伝播を3.0倍、復号を1.6倍改善したと報告する。

- **2026-09 · [MaskCoFT: Masked Co-Adaptive Fine-Tuning for Memory-Efficient MoE Inference](2026-2609.34077-maskcoft-masked-co-adaptive-fine-tuning-for-memory-efficient-moe-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPUメモリが不足する場合は専門家をCPUへオフロードし、必要時にGPUへロードする。原著はMoE-OffloadingにおけるMixtral-8×7Bのデコード時間で、専門家ロードが86%、専門家計算が3%という分析を示す。

- **2026-09 · [KREX: Concurrent Kernel Benchmarking on Shared GPUs via Region-Granular Exclusivity](2026-2609.30057-krex-concurrent-kernel-benchmarking-on-shared-gpus-via-region-granular-e.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  実行時間のわずかな差が候補順位を変えるため、他の処理が同じGPUへ負荷をかけると測定が歪み、エージェントは遅い候補を良いものと誤認する。さらにGPUコンテキストを毎回作り直さず、長寿命のコンテキスト保持プロセスを再利用することで、GPU初期化時のノード全体の直列化を避ける。

- **2026-09 · [HoliBench: A Cross-Platform Benchmarking and Deployment Toolkit for Foundation Models in CPS-IoT Applications](2026-2609.12412-holibench-a-cross-platform-benchmarking-and-deployment-toolkit-for-foundation-models-in-cps-iot-applications.md)**  
  実装：[✓](https://github.com/beesfleas/HoliBench) ・ リポジトリ内被引用：0  
  20モデル×7デバイス×3量子化×8推論系を精度・遅延・電力・メモリで統一測定し、実測プロファイルから制約付き配備構成まで選ぶ基盤。

- **2026-09 · [GGUF-Metadata Prediction of Single-Sequence llama.cpp Throughput Across Three Systems](2026-2609.14864-gguf-metadata-prediction-of-single-sequence-llama-cpp-throughput-across-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ローカル大規模言語モデルを選ぶとき、GGUF形式の複数の量子化モデルを実際に読み込み、同じ入力長で速度を比較する作業は重い。

- **2026-09 · [From Inference Engine to Inference Control Plane: Connecting vLLM, llm-d, and the Evolution of Efficient Distributed LLM Serving](2026-2609.23130-from-inference-engine-to-inference-control-plane-connecting-vllm-llm-d-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLM推論最適化の単位が単一推論エンジンのバッチ処理・KV管理から、分散したGPU群のルーティング、KV転送、プリフィル/デコード分離、入場制御、拡縮と耐障害性を束ねる制御面へ移行していることを整理したシステム統合レビュー。

- **2026-09 · [FaultSense: Fault Localization in Large-Scale Mixture-of-Experts Model Serving Infrastructure](2026-a08c1f9c632d-faultsense-fault-localization-in-large-scale-mixture-of-experts-model-serving-infrastructure.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単一MoE層の選択可能プローブと二段階グループ検査で、特権監視なしにグレー障害GPU・通信経路をアプリ層から局所化し、診断プローブを約20倍削減する。

- **2026-09 · [Dissecting GPU Utilization for LLM Inference on Nvidia Hopper](2026-2609.12923-dissecting-gpu-utilization-llm-inference-hopper.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  H100上のLLM推論を8種類のNsight指標で分解し、デコードでは帯域待ちに加えGMMA m64固定断片の1.56～12.5%充填やwave損失が単一SM利用率に隠れることを示す。

- **2026-09 · [AutoTuneBench: Trustworthy Measurement for Agent Auto-Tuning of LLM Serving Engines](2026-2609.18123-autotunebench-trustworthy-serving-engine-measurement.md)**  
  実装：[✓](https://github.com/li-ch/autotunebench) ・ リポジトリ内被引用：0  
  自動チューニングの測定規約を凍結コード・DB投入検証・不正隔離・事前登録比較・外部アンカーで強制し、エージェントが評価欠陥を最適化するのを防ぐ。

- **2026-09 · [Accuracy is Not Enough: A Divergence-Based Approach to Evaluate Fidelity Loss in Quantized LLMs](2026-2609.07664-accuracy-is-not-enough-a-divergence-based-approach-to-evaluate-fidelity-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）を低ビット量子化して端末へ載せるとき、一般的には困惑度（perplexity）や選択式問題の正答率がどれだけ落ちるかを確認する。例えばLLaMA-3.1-8BのMMLUでは、Q4KとQ40の正答率はそれぞれ32.2%と32.1%でほぼ等しいのに、BF16に対するTVDは0.055と0.221で約4倍異なる。

- **2026-08 · [Thinking Hard, Not Smart: Reasoning Models Fail to Ration Test-Time Compute Across Questions](2026-2608.07968-thinking-hard-not-smart-reasoning-models-fail-to-ration-test-time-comput.md)**  
  実装：[✓](https://github.com/Fcr09/thinking-hard-not-smart) ・ リポジトリ内被引用：0  
  長い思考を許す推論言語モデルは、一問ごとの数学・コード問題で精度を高められる。しかし現実の計算資源は有限であり、複数の依頼を同時に処理する場合には「どの問題へ何トークン使うか」「いつ諦めて別の問題へ進むか」という別の判断が必要になる。この論文は新しい高速化カーネルや推論サービング基盤を提案するものではない。

- **2026-08 · [Sliding-window beats linear attention](2026-2608.28444-sliding-window-beats-linear-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  線形注意は固定サイズの再帰状態に集約することで、この増加を抑える。窓64・先頭シンク4の方式は、一般知識6課題平均で元モデルの99.0%を回復し、11の比較例のうち9例で元モデルを除く最高の平均値を得た。

- **2026-08 · [LowRankArena: A Standardized Evaluation Platform for SVD-Based LLM Compression](2026-2608.26389-lowrankarena-a-standardized-evaluation-platform-for-svd-based-llm-compre.md)**  
  実装：[✓](https://github.com/Zishan-Shao/lowrankarena) ・ リポジトリ内被引用：0  
  特異値分解（Singular Value Decomposition; SVD）を使う低ランク圧縮は、重み行列を二つの小さな行列の積に分解し、保存するパラメータと演算量を減らす。

- **2026-08 · [Launch-Bound and Substitutable: Why Three Inference Optimizations Fail to Pay Off in Mixture-of-Experts Models](2026-2608.26612-launch-bound-and-substitutable-moe-inference-optimizations.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoEの融合カーネル・4/8ビット量子化・グラフコンパイルを単体とE2Eで測定し、局所高速化が起動律速や品質へどう波及するかを分解して、置換可能な最適化の限界を明らかにする研究。

- **2026-08 · [Diagnose Before You Compress: Prediction-Independent Bottleneck Witness Refinement for LLM Serving Traces](2026-2608.00423-bottleneck-preserving-witnessing.md)**  
  実装：[✓](https://github.com/llmllmllm/BPW) ・ リポジトリ内被引用：0  
  スケジューリング・入力処理・生成・KVキャッシュの各ボトルネックを実機測定で独立確認し、四要素すべてに複数の証拠を残す小さなLLMサービング再生用トレースを選ぶ。

- **2026-08 · [Beyond Tokens: A Survey on Decoding Methods for Large Language and Vision-Language Models](2026-2608.14797-beyond-tokens-a-survey-on-decoding-methods-for-large-language-and-vision.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  対象はモデルの重みを更新する学習ではなく、既存モデルが出力した確率分布を、推論時にどのようなトークン列へ変換するかという復号（デコード）の設計である。表1の年代と分類は文献整理の結果であり、速度・品質の絶対値や改善倍率を示す統一ベンチマークではない。

- **2026-08 · [Beyond Accuracy: Auditing Spatial Provenance in Visual Token Pruning for OCR-Critical MLLM Inference](2026-2608.00077-beyond-accuracy-auditing-spatial-provenance-in-visual-token-pruning-for-.md)**  
  実装：[✓](https://github.com/SouthWinter/spatial-provenance-audit) ・ リポジトリ内被引用：0  
  視覚トークンを間引けば言語モデル側の事前計算（プリフィル）とその作業用メモリを削減できるが、単に「保持率30%で正答率がほぼ同じ」という評価には穴がある。さらにトークンを統合する手法については、統合出力の出自集合と、代表位置で局所的に追跡できる範囲を区別する。

- **2026-07 · [Rethinking the Generation Order of Block Diffusion Language Models](2026-2607.24306-rethinking-the-generation-order-of-block-diffusion-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ブロック内の位置は任意順で確定できるように見えるが、既存の並列サンプリング方式をそのまま移植すると、先の位置だけを確定して前方の未確定位置を残し、コードや推論の構造を壊す場合がある。

- **2026-07 · [From Static Inference to Dynamic Interaction: A Survey of Streaming Large Language Models](2026-73c7c240d868-from-static-inference-to-dynamic-interaction-a-survey-of-streaming-large.md)**  
  実装：[✓](https://github.com/EIT-NLP/Awesome-Streaming-LLMs) ・ リポジトリ内被引用：0  
  さらに同時入出力で生じる注意依存の競合、位置IDの衝突、読み書きタイミングの決定を、アーキテクチャと制御ポリシーの独立した設計軸として比較する。

- **2026-07 · [From Expert Reduction to Behavioral Divergence: Tracing Numerical State through Sparse MoE Inference](2026-2607.28097-from-expert-reduction-to-behavioral-divergence-tracing-numerical-state-through-sparse-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  疎MoEの専門家加算順序だけで内部状態と生成文が分岐しうることを全順列・状態再構成で実証し、BF16項＋FP32累算を評価範囲の安定な互換契約として特定する。

- **2026-07 · [CORVUS: Context Optimization and Reduction Via Underlying Synchronization for LLM Coding Agents](2026-2607.22711-corvus-context-optimization-and-reduction-via-underlying-synchronization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  コード編集を行う大規模言語モデル（LLM）エージェントは、ファイル読込み、編集、試験、再読込みを何度も繰り返す。従来の追記専用履歴では、読込み時のファイル本文が道具の観測結果として永久に残り、後で同じファイルが変更されても古い本文は削除されない。エージェントがその古い記述を使って修正すると、適用位置の不一致や失敗が起こり、さらに再読込みと再試行を繰り返す。

- **2026-07 · [Benchmarking Confidential GPU Inference on NVIDIA H100 under Intel TDX](2026-2607.19353-benchmarking-confidential-gpu-inference-on-nvidia-h100-under-intel-tdx.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  原著はサービス指標の比較研究であり、GPU内部の暗号化処理、PCIe転送、HBM帯域、スケジューラのどれが何%の原因かまで分解したマイクロアーキテクチャ解析ではない。

- **2026-06 · [Characterizing Software Aging in GPU-Based LLM Serving Systems](2026-2606.11916-characterizing-software-aging-in-gpu-based-llm-serving-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  6種類のGPU LLMサービング構成を計216時間連続運転し、全構成でホスト側のメモリ経年劣化を検出。リーク率はvLLM V1単体+1.8KB/時からTriton+V0の+157KB/時まで大差があり、配置・ランタイム選択が長期信頼性を左右することを示す。

- **2026-06 · [Beyond tokens: a unified framework for latent communication in LLM-based multi-agent systems](2026-2606.05711-beyond-tokens-a-unified-framework-for-latent-communication-in-llm-based-.md)**  
  実装：[✓](https://github.com/enochliu98/Awesome-Latent-Communication) ・ リポジトリ内被引用：0  
  2026年7月15日を調査打切りとして、2024～2026年の代表的な18研究を選び、送る情報の種類（WHAT）、送受信間の表現・層の整合（WHICH）、受信モデルへの統合方法（HOW）という3軸で比較する。

- **2026-06 · [Beyond Per-Token Pricing: A Concurrency-Aware Methodology for LLM Infrastructure Cost Estimation](2026-2606.11690-beyond-per-token-pricing-a-concurrency-aware-methodology-for-llm-infrast.md)**  
  実装：[✓](https://github.com/pChitral/vllm-cost-meter) ・ リポジトリ内被引用：0  
  本研究はこの差を、要求到着率を明示した費用測定問題として定式化する。ハードウェア、モデル構造、量子化精度、要求到着率、遅延目標を分け、同じGPUでも負荷によって費用がどの程度変わるかを実機で測る。H100 NVLの主実験では、3種類のモデルと2種類の精度の計6構成を7段階の要求率で測定し、同じ構成内で17.5～36.3倍の出力トークン単価差を観測した。

- **2026-06 · [Benchmarking LLM Serving Systems for Agentic AI Workloads with XPerf](2026-2608.20370-xperf-benchmarking-llm-serving-agentic-ai-workloads.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント実行を呼出し依存グラフとして記録・再生し、8種類の実アプリでサービング負荷とハードウェア指標を再現可能に測る評価基盤を提示する。

- **2026-06 · [AVIS: Adaptive Test-Time Scaling for Vision-Language Models](2026-2606.11576-avis-adaptive-test-time-scaling-for-vision-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚トークンを減らして浮いた計算を、難しい問いの追加推論へ回せれば、計算を減らしつつ精度を維持・改善できる可能性がある。推論探索量を制御するVisual Reasoning Scaling（VRS）では、視覚埋め込みから問題の解答可能性を予測し、自己整合性多数決の試行数Kを1、3、5、7から選ぶ。

- **2026-06 · [Agent Memory: Characterization and System Implications of Stateful Long-Horizon Workloads](2026-2606.06448-agent-memory-characterization-and-system-implications-of-stateful-long-h.md)**  
  実装：[✓](https://github.com/Tambe-Lab/agent-memory-profiling) ・ リポジトリ内被引用：0  
  本研究は、長期にわたり複数のセッションをまたいで稼働する大規模言語モデル（LLM）エージェントの「記憶」を、回答品質を高める機能としてだけでなく、計算・メモリ・入出力・スケジューリングの対象となる実行時システムとして捉え直す。後者は前者の約26.5倍である。

- **2026-05 · [Stop When Reasoning Converges: Semantic-Preserving Early Exit for Reasoning Models](2026-2605.17672-stop-when-reasoning-converges-semantic-preserving-early-exit-for-reasoni.md)**  
  実装：[✓](https://github.com/giovanni-vaccarino/PUMA) ・ リポジトリ内被引用：0  
  PUMAは、推論モデルが問題を解き終えた後も思考を繰り返す「過剰思考」を減らすための推論時早期終了方式である。

- **2026-05 · [PARCEL: Pool-Anchored Resampling with Conditioned Elastic Queries for Efficient Vision-Language Understanding](2026-2605.30126-parcel-pool-anchored-resampling-with-conditioned-elastic-queries-for-eff.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PARCELは、視覚トークンの数を16、64、256など異なる予算へ縮めても、空間的な位置関係と画像の細部を両立して保つための、可変予算の視覚表現設計である。27種類の評価課題を横断した全体平均の性能保持率は、視覚トークン256個で95.6%、64個で95.3%、16個で88.3%と報告された。

- **2026-05 · [Measuring Maximum Activations in Open Large Language Models](2026-2605.15572-measuring-maximum-activations-in-open-large-language-models.md)**  
  実装：[✓](https://github.com/clx1415926/Max_act_llm) ・ リポジトリ内被引用：0  
  低ビット推論では、活性値を少数の離散水準へ写すときに、値の最大絶対値が量子化尺度の決定を左右する。近い規模のMoEモデルは密モデルより14.0〜23.4倍低い極大値を示す。

- **2026-05 · [Linear Scaling Video VLMs for Long Video Understanding](2026-2605.31598-linear-scaling-video-vlms-for-long-video-understanding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い動画を視覚言語モデル（Vision-Language モデル; VLM）へ入力すると、映像から得られる視覚トークンが時間とともに増え、各フレームが過去の全フレームへ自己注意（self-注意機構）を計算する通常の実装では、全映像を処理する事前充填（プリフィル）の計算量がフレーム数 N に対して二次的に増える。

- **2026-05 · [Evading Visual Aphasia: Contrastive Adaptive Semantic Token Pruning for Vision-Language Models](2026-2605.09429-evading-visual-aphasia-contrastive-adaptive-semantic-token-pruning-for-v.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  たとえば、画像内で目立つ動物より周辺の店名看板を尋ねているのに、初期層の注意が動物へ集中した結果、看板のトークンが枝刈りされ、モデルが架空の店名を答える。LLaVA-v1.5-7Bで画像トークンを576個から128個へ77.8%削減した条件では、七つの評価セットを正規化した平均性能を98.64%保持し、遅延を167.50ミリ秒から77.94ミリ秒へ短縮した。

- **2026-04 · [SMoES: Soft Modality-Guided Expert Specialization in MoE-VLMs](2026-2604.23996-smoes-soft-modality-guided-expert-specialization-in-moe-vlms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SMoES（Soft Modality-guided 専門家 Specialization）は、視覚・言語モデル（Vision-Language モデル, VLM）の専門家混合（Mixture of エキスパート, MoE）層で、画像由来トークンと文章由来トークンが各層でどの程度混合しているかを推定し、専門家の配置と学習を調整する方式である。

- **2026-04 · [Quantized Transformers in Practice: Benchmarking Full- and Low-Precision LLMs across Two Processors](2026-f22ed3216fa9-quantized-transformers-in-practice-benchmarking-full-and-low-precision-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は新規の量子化アルゴリズムを提案するものではなく、既存の8ビット学習後量子化を一般的なノートPC向けGPUに適用した場合、モデルの収容可否、生成時間、生成文の一致度がどのように変化するかを実測する。著者の要旨はCPUオフロードの影響を受けた条件を除外した平均高速化を3.4倍と記すが、個別の表3は非常に不均一である。

- **2026-04 · [On the Quantization Robustness of Diffusion Language Models in Coding Benchmarks](2026-2604.20079-on-the-quantization-robustness-of-diffusion-language-models-in-coding-be.md)**  
  実装：[✓](https://github.com/zinichakraborty/Diffusion-LLM-Quantization-Robustness) ・ リポジトリ内被引用：0  
  推論用重みを低ビットで表す学習後量子化（post-学習 量子化; PTQ）はこの費用を減らす有力な方法だが、自己回帰型で得られた量子化の知見を拡散型へそのまま適用できるとは限らない。重要な留保として、混合精度実験は量子化を模擬しても重みを浮動小数点形式で保存する方式であり、低ビットの実物理容量削減を実測した結果ではない。

- **2026-04 · [KiToke: Distribution-Aware Token Compression for Video Large Language Models](2026-2604.03414-kitoke-distribution-aware-token-compression-for-video-large-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  特に保持率1%など極端な条件では、複雑な既存手法が一様ランダム抽出より低い精度になることもある。

- **2026-04 · [IWP: Token Pruning as Implicit Weight Pruning in Large Vision Language Models](2026-2604.00757-iwp-token-pruning-as-implicit-weight-pruning-in-large-vision-language-mo.md)**  
  実装：[✓](https://github.com/jhtwosun/IWP) ・ リポジトリ内被引用：0  
  視覚トークンを削る従来方式は、注意重みの大きいトークンを残す、埋込み表現が似たトークンをまとめるなどの経験的基準を使うことが多い。LLaVA-OneVision-7Bの88.9%削減条件では、全トークン時1.37秒から0.64秒へ実測レイテンシを短縮する一方、品質指標は95.9%から89.5%へ下がる。

- **2026-04 · [ID-Selection: Importance-Diversity Based Visual Token Selection for Efficient LVLM Inference](2026-2604.05601-id-selection-importance-diversity-based-visual-token-selection-for-effic.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  候補N個からT個を残す計算量は概ねO(NT)であり、TがNより十分小さい強い圧縮で実用的とされる。LLaVA-1.5-7Bでは576個の視覚トークンを16個へ削減しても、9課題の集計で元モデルの91.8%の性能を維持する。

- **2026-04 · [EvoComp: Learning Visual Token Compression for Multimodal Large Language Models via Semantic-Guided Evolutionary Labeling](2026-2604.17087-evocomp-learning-visual-token-compression-for-multimodal-large-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル時の注意演算、鍵・値（KV）キャッシュ、入力列の読み込みが増え、初回応答の待ち時間が長くなる。EvoCompは、視覚トークンのうち質問への回答に必要なものだけを選び、下流LLMへ渡す系列長を減らす方式である。LLaVA-1.5-7Bでは576トークンを192に削減したとき、6ベンチマークの平均成績を元モデルの99.3%に保つ。

- **2026-04 · [Efficient Multimodal Spatial Reasoning via Dynamic and Asymmetric Routing](2026-22e11514f14e-efficient-multimodal-spatial-reasoning-via-dynamic-and-asymmetric-routin.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  これにより複雑な空間関係を段階的に処理できるが、過去の中間トークンが自己回帰的に蓄積し、注意計算・KVキャッシュ・推論遅延を押し上げる。既存の固定率圧縮では、初期段階で必要な画像細部を落としたり、深い層ですでに冗長な視覚トークンを残したりする。

- **2026-04 · [Comparative Characterization of KV Cache Management Strategies for LLM Inference](2026-2604.05012-comparative-characterization-kv-cache-management-strategies-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  vLLM、H2O、InfiniGenをH100実機で比較し、GPUメモリを最大約70%減らすH2O、初期事実を保ちやすいInfiniGen、速度に優れるvLLMの条件別の使い分けを明らかにする。

- **2026-04 · [Caracal: Causal Architecture via Spectral Mixing](2026-2605.00292-caracal-causal-architecture-via-spectral-mixing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Caracalは、Transformerの全域注意（global 注意機構）を多頭フーリエ混合（Multi-Head Fourier、MHF）で置き換える言語モデルの設計である。ただし、論文の主要な高速化評価は文脈長を変えた訓練処理であり、一般的なLLM配信での1トークンずつの逐次生成が同率で高速化することを示したものではない。

- **2026-04 · [Beyond Accuracy: Unveiling Inefficiency Patterns in Tool-Integrated Reasoning](2026-2604.05404-beyond-accuracy-unveiling-inefficiency-patterns-in-tool-integrated-reaso.md)**  
  実装：[✓](https://github.com/sqs-ustc/tool-reasoning-framework-PTE) ・ リポジトリ内被引用：0  
  本論文は、推論と外部ツール利用を交互に行うツール統合推論（tool-integrated reasoning; TIR）の計算費用の測り方を提案する。

- **2026-03 · [Wattchmen: Watching the Wattchers -- High Fidelity, Flexible GPU Energy Modeling](2026-2603.26435-wattchmen-watching-the-wattchers-high-fidelity-flexible-gpu-energy-model.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  一方、従来の細粒度モデルは一部の命令だけを対象にするか、別のGPU・冷却条件への移植性が不足していた。これはLLM専用推論の速度を改善する方式ではなく、GPUを使う学習・推論・科学計算のエネルギーを分析し最適化箇所を見つける基盤である。

- **2026-03 · [Towards Efficient Large Vision-Language Models: A Comprehensive Survey on Inference Strategies](2026-2603.27960-towards-efficient-large-vision-language-models-a-comprehensive-survey-on.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Surendra PathakとBo Hanによる本サーベイは、大規模視覚言語モデル（LVLM）の推論を高速化・省メモリ化する既存研究を、①視覚トークン圧縮、②KVキャッシュ管理とサービング、③モデル構造と注意計算の最適化、④高度な復号戦略という四つの層に整理する。

- **2026-03 · [Spend Less, Reason Better: Budget-Aware Value Tree Search for LLM Agents](2026-2603.12634-spend-less-reason-better-budget-aware-value-tree-search-for-llm-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  実サービスではツール呼び出し回数、生成トークン数、API料金に上限があるため、単に推論を長くする方式は適さない。原著はgpt-oss-20bとQwen3-30B-A3B-Instruct-2507を用い、HotpotQA、2WikiMultihopQA、MuSiQue、Bamboogleで評価した。

- **2026-03 · [DyLLM: Efficient Diffusion LLM Inference via Saliency-based Token Selection and Partial Attention](2026-2603.08026-dyllm-efficient-diffusion-llm-inference-via-saliency-based-token-selecti.md)**  
  実装：[✓](https://github.com/scale-snu/DyLLM) ・ リポジトリ内被引用：0  
  マスク拡散型の言語モデルは、応答系列をマスクから始め、複数トークンを並列に埋めながら反復的に復号する。salient位置ではFFNを再計算し、注意も正確に更新する。DyLLMは速度だけでなく品質を維持する運用点を探す方式である。

- **2026-02 · [On the Optimal Reasoning Length for RL-Trained Language Models](2026-2602.09591-on-the-optimal-reasoning-length-for-rl-trained-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長くすることで最頻回答が正解になる問題は増えるが、その正解周辺に個々の標本が集中しなくなるため、単発回答の成功率が下がり得る。

- **2026-01 · [L³: Large Lookup Layers](2026-2601.21461-l-large-lookup-layers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  このため、CPUに退避した専門家をGPUへ移す場合は、選択後の転送が計算の待ち時間になりやすい。推論速度はL³の配置に依存し、2.6B稼働モデルで最初のL³を第5層後に置くと、原著表2のバッチ1速度は密モデル776に対して772トークン/秒/系列だった。

- **2025-11 · [TimeViper: A Hybrid Mamba-Transformer Vision-Language Model for Efficient Long Video Understanding](2025-2511.16595-timeviper-a-hybrid-mamba-transformer-vision-language-model-for-efficient.md)**  
  実装：[✓](https://github.com/xiaomi-research/timeviper) ・ リポジトリ内被引用：0  
  1時間の動画を毎秒1枚、1フレーム768トークンで表現すると約276万トークンになり、通常の全注意では処理費用とメモリが大きい。TimeViperは、状態空間モデル（State Space モデル; SSM）のMamba-2とTransformerの注意層を混ぜた基盤を使い、さらに言語モデルの途中で視覚トークンを圧縮する。

- **2025-11 · [OckBench: Measuring the Efficiency of LLM Reasoning](2025-2511.05722-ockbench-measuring-the-efficiency-of-llm-reasoning.md)**  
  実装：[✓](https://github.com/OckBench/OckBench) ・ リポジトリ内被引用：0  
  従来の正答率だけではこの差が見えず、ハードウェアの処理量だけではモデル自身がどれほど冗長に推論するかを分離できない。

- **2025-11 · [MemSearcher: Training LLMs to Reason, Search and Manage Memory via End-to-End Reinforcement Learning](2025-2511.02805-memsearcher-training-llms-to-reason-search-and-manage-memory-via-end-to-.md)**  
  実装：[✓](https://github.com/icip-cas/MemSearcher) ・ リポジトリ内被引用：0  
  検索エージェント（search agent）が外部検索を何度も行うと、思考、検索クエリ、検索結果を全て会話履歴に追記する従来のReAct方式では、ターンが増えるにつれて入力文脈が長くなる。検索エージェントの入力文脈はほぼ一定長で、論文の評価条件では4,000トークン未満を維持する。

- **2025-11 · [From Prompts to Power: Measuring the Energy Footprint of LLM Inference](2025-2511.05597-from-prompts-to-power-measuring-the-energy-footprint-of-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本サーベイとの接点は、LLM推論サービング（serving）の省エネルギー化、モデル・GPUの配置選択、バッチ処理、KVキャッシュ容量、量子化・実行方式の設計判断である。

- **2025-11 · [Analyzing and Modeling LLM Response Lengths with Extreme Value Theory: Anchoring Effects and Hybrid Distributions](2025-a08ef62fbe5d-analyzing-and-modeling-llm-response-lengths-with-extreme-value-theory-an.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  要求ごとの出力長がばらつくと、短い応答と非常に長い応答が混在し、GPUの連続バッチングやスケジューラの資源配分が難しくなる。

### 2年前（2024-11〜2025-10）

- **2025-05 · [ServeGen: Workload Characterization and Generation of Large Language Model Serving in Production](2026-2505.09999-servegen-workload-characterization-and-generation-of-large-language-mode.md)**  
  実装：[✓](https://github.com/alibaba/ServeGen) ・ リポジトリ内被引用：28  
  4か月・12モデル・35.4億要求の本番記録から、到着率、バースト、入力・出力長、画像・音声・動画、推論過程の分布を分析する。顧客ごとの比較的安定した特性と時間変動する到着率を合成し、現実的な推論ベンチマークを作る。

- **2025-01 · [LLaVA-Mini: Efficient Image and Video Large Multimodal Models with One Vision Token](2025-2501.03895-llava-mini-efficient-image-and-video-large-multimodal-models-with-one-vi.md)**  
  実装：[✓](https://github.com/ictnlp/LLaVA-Mini) ・ リポジトリ内被引用：26  
  画像を1枚だけ扱う場合でも自己注意と中間活性の負荷が増え、動画ではフレーム数にほぼ比例して言語モデルの文脈が膨らむ。別の学習可能なクエリを使った圧縮器が、言語モデルへ渡す視覚トークンを最少1個にする。

- **2025-03 · [Stop Overthinking: A Survey on Efficient Reasoning for Large Language Models](2025-2503.16419-stop-overthinking-a-survey-on-efficient-reasoning-for-large-language-mod.md)**  
  実装：[✓](https://github.com/Eclipsess/Awesome-Efficient-Reasoning-LLMs) ・ リポジトリ内被引用：23  
  本論文は、推論に特化した大規模言語モデルが長い思考連鎖（Chain-of-Thought; CoT）を生成することで正答率を高める一方、単純な質問にも冗長な検証や反復を行ってしまう「過剰思考」を減らす研究を整理したサーベイである。

- **2025-02 · [KernelBench: Can LLMs Write Efficient GPU Kernels?](2025-2502.10517-kernelbench-can-llms-write-efficient-gpu-kernels.md)**  
  実装：[✓](https://github.com/ScalingIntelligence/KernelBench) ・ リポジトリ内被引用：18  
  一般的なプログラム合成では単体試験に通ることを重視するが、GPUカーネルの実用性は入力形状、メモリ階層、並列実行、命令セットに左右される。正しくても遅い実装を成功とみなさないことが設計の中心にある。例えばDeepSeek-R1の fast1 は単一演算12%、複合演算36%、モデル全体2%である。

- **2025-02 · [Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach](2025-2502.05171-scaling-up-test-time-compute-with-latent-reasoning-a-recurrent-depth-app.md)**  
  実装：[✓](https://github.com/seal-rg/recurrent-pretraining) ・ リポジトリ内被引用：17  
  この研究は、推論時の計算量を思考連鎖（chain-of-thought; CoT）の出力トークン数ではなく、モデル内部の反復深さで増やす。入力を処理するprelude、共有されるrecurrent core、出力を作るcodaにTransformerを分け、coreを推論時に何回でも反復する。

- **2025-04 · [Energy Considerations of Large Language Model Inference and Efficiency Optimizations](2025-2504.17674-energy-considerations-of-large-language-model-inference-and-efficiency-o.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  LLM推論の電力量を、入力長・出力長・バッチ数・GPU・推論基盤・復号方式・モデル並列の組合せで実測し、実トラフィックの入出力長分布を区間化して総消費量を推定する。適切なソフトウェア最適化で未最適化PyTorch比最大73%削減できる一方、投機的復号や複数GPUは条件によって逆に電力量を増やす。

- **2024-11 · [Lynx: Enabling Efficient MoE Inference through Dynamic Batch-Aware Expert Selection](2024-2411.08982-lynx-enabling-efficient-moe-inference-through-dynamic-batch-aware-expert.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  演算の疎性が、専門家重みを高帯域メモリから読み出す量の削減につながらなくなる。Lynxはこの矛盾を、モデルの重みを恒久的に枝刈りするのでなく、現在のバッチのルーター出力を再配置することで緩和する。通常の同居配置で出力トークン間隔の中央値を1.09～1.30倍短縮し、精度変化を概ね1ポイント以内に抑える。

- **2024-12 · [Don't Do RAG: When Cache-Augmented Generation is All You Need for Knowledge Tasks](2024-2412.15605-don-t-do-rag-when-cache-augmented-generation-is-all-you-need-for-knowled.md)**  
  実装：[✓](https://github.com/hhhuang/CAG) ・ リポジトリ内被引用：14  
  著者らはキャッシュ拡張生成（Cache-Augmented Generation、CAG）を提案する。Llama 3.1 8BをV100×8で評価した結果、SQuADとHotPotQAの多くの知識集合でCAGの回答品質は疎検索・密検索を用いるRAGと同等以上である。

- **2025-07 · [LIMINAL: Exploring The Frontiers of LLM Decode Performance](2025-2507.14397-liminal-exploring-the-frontiers-of-llm-decode-performance.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  LIMINALは、自己回帰デコードの上限を、モデル側の演算・重み・キー・バリュー（Key-Value; KV）キャッシュ需要と、加速器側の演算性能・メモリ容量・帯域・集合通信性能へ分解する解析性能モデルである。

- **2025-06 · [Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference](2025-2506.09501-understanding-and-mitigating-numerical-sources-of-nondeterminism-in-llm-inference.md)**  
  実装：[✓](https://github.com/nanomaoli/llm_reproducibility) ・ リポジトリ内被引用：11  
  「温度0の貪欲復号なら同じモデルは同じ答えを返す」という前提が、GPU数・GPU種類・バッチサイズによる浮動小数点演算順序の変化だけでも崩れることを系統的に示し、重みの保存精度と計算精度を分離するLayerCastで再現性を改善する研究。

- **2025-10 · [Growing a Twig to Accelerate Large Vision-Language Models](2025-2503.14075-growing-a-twig-to-accelerate-large-vision-language-models.md)**  
  実装：[✓](https://github.com/MILVLG/twigvlm) ・ リポジトリ内被引用：7  
  初期の視覚トークン枝刈り方式は、入力処理（プリフィル）の計算量を減らす一方、初期層の注意得点が質問内容を十分反映しないため、削除してはいけない視覚トークンを捨てやすい。ICCV 2025論文の主結果では、LLaVA-1.5-7Bの平均視覚トークンを576から64へ減らした設定（88.9%削減）で、6課題の平均相対性能96.0%を維持した。

- **2025-07 · [Collaborative Inference and Learning between Edge SLMs and Cloud LLMs: A Survey of Algorithms, Execution, and Open Challenges](2025-2507.16731-collaborative-inference-and-learning-between-edge-slms-and-cloud-llms-a-.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  端末で簡単な要求を処理し、必要な時だけクラウドを呼ぶ方式は自然だが、呼出し回数が増えれば往復遅延が支配的になる。

- **2025-01 · [Resource-efficient Algorithms and Systems of Foundation Models: A Survey](2025-f103beecee83-resource-efficient-algorithms-and-systems-of-foundation-models-a-survey.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  Xu・Cai・Yin・Wang・Jin・Liuによる39ページの査読付きサーベイは、基盤モデルの「効率」を単一のモデル圧縮率やGPU演算速度として扱わず、モデル構造、学習・圧縮・推論アルゴリズム、実行システムという異なる介入点に分解する。

- **2025-09 · [Training Matryoshka Mixture-of-Experts for Elastic Inference-Time Expert Utilization](2025-2509.26520-training-matryoshka-mixture-of-experts-for-elastic-inference-time-expert.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  1T トークンをk=1で事前学習したcheckpointから、各方式でさらに80B トークンを継続学習する。

- **2025-06 · [Towards Efficient Multi-LLM Inference: Characterization and Analysis of LLM Routing and Hierarchical Techniques](2025-2506.06579-towards-efficient-multi-llm-inference-characterization-and-analysis-of-l.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  このサーベイは、複数の独立した大規模言語モデル（LLM）を一つのサービスで使い分ける際、どの要求をどのモデルへ送り、どの条件で上位モデルへ再実行するかを推論システムの最適化問題として整理する。本文中の最大98%費用削減などの値は引用した個別研究の結果であり、このサーベイの独立した再現実験ではない。

- **2024-12 · [A Survey of RWKV](2024-2412.14847-a-survey-of-rwkv.md)**  
  実装：[✓](https://github.com/MLGroupJLU/RWKV-Survey) ・ リポジトリ内被引用：2  
  RWKVは、過去の情報を固定形状の再帰状態へ畳み込むことで、生成時に全トークンのKVを保持しない設計を取る。

- **2025-02 · [Binary Neural Networks for Large Language Model: A Survey](2025-2502.19008-binary-neural-networks-for-large-language-model-a-survey.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  中心となるのは、BitNet、BitNet b1.58、BitNet a4.8、FBI-LLM、Bi-Mambaなど、重みの二値化・三値化を学習時から組み込む方式である。

- **2025-10 · [Higher-order Linear Attention](2025-2510.27258-higher-order-linear-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Higher-order Linear 注意機構（HLA）は、より高次の相互作用を、低次のモーメントと補正統計の組合せへ因数分解する。

- **2025-09 · [PLaMo 2 Technical Report](2025-2509.04897-plamo-2-technical-report.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PLaMo 2 Technical Reportは、Preferred Networksが開発した日本語向け大規模言語モデル系列のアーキテクチャ、学習・蒸留、長文脈対応、推論実装と量子化をまとめた技術報告である。推論側では、31BモデルのBF16重みが約63GB、KVキャッシュが約110KB/トークンであり、32K文脈だけで約3.6GBのKVを使う。

- **2025-09 · [Motivating Next-Gen Accelerators with Flexible N:M Activation Sparsity via Benchmarking Lightweight Post-Training Sparsification Approaches](2025-2509.22166-motivating-next-gen-accelerators-with-flexible-n-m-activation-sparsity-v.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  半構造化N:M疎性は、各M要素のうちN要素を残す制約を設ける。2:4、4:8、8:16、16:32はいずれも50%の要素をゼロ化するが、ブロックが大きいほど、どの要素を残すかの組合せが増える。したがって本研究は「半構造化活性疎性が現時点で実用上安全」と結論するより、将来ハードウェアの設計選択を促す精度とコストの基礎ベンチマークとして読むべきである。

- **2025-09 · [Efficient Fine-Grained GPU Performance Modeling for Distributed Deep Learning of LLM](2025-2509.22832-efficient-fine-grained-gpu-performance-modeling-for-distributed-deep-lea.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、こうした複雑さをブラックボックスの「モデルサイズから学習時間を推定する式」だけで扱うのではなく、演算・通信プリミティブの実測回帰器と、実行依存関係を反映した時間軸モデルを組み合わせることで、実際の学習反復時間を予測する手法を提案する。

- **2025-08 · [TPLA: Tensor Parallel Latent Attention for Efficient Disaggregated Prefill and Decode Inference](2025-2508.15881-tpla-tensor-parallel-latent-attention-for-efficient-disaggregated-prefil.md)**  
  実装：[✓](https://github.com/fxmeng/TransMLA) ・ リポジトリ内被引用：0  
  TPLA（テンソル-Parallel Latent 注意機構）は、DeepSeek系列などで使われるMulti-Head Latent 注意機構（MLA）のKVキャッシュをGPUごとに複製する問題を解消するテンソル parallel（TP）方式である。

- **2025-08 · [Meta-Metrics and Best Practices for System-Level Inference Performance Benchmarking](2025-2508.10251-meta-metrics-and-best-practices-for-system-level-inference-performance-b.md)**  
  実装：[✓](https://github.com/IBM/fmwork) ・ リポジトリ内被引用：0  
  入力トークン長、出力トークン長、同時実行数、重み精度、テンソル並列数、推論エンジン、スケジューラ設定を変えると、初回トークン遅延（TTFT）、トークン間遅延（ITL）、総スループット（THP）は異なる。

- **2025-05 · [Resource-Efficient Language Models: Quantization for Fast and Accessible Inference](2025-2505.08620-resource-efficient-language-models-quantization-for-fast-and-accessible-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、大規模言語モデルを一般利用者の限られた計算資源で動かすための後学習量子化を解説する文献レビューである。

- **2025-05 · [ResDecode: Accelerating Large Language Models Inference via Residual Decoding Heads](2025-098116cbc05e-resdecode-accelerating-large-language-models-inference-via-residual-deco.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号は、小さなドラフトモデルが複数の候補トークンを先に生成し、大きな対象モデルがまとめて検証することで、出力分布の整合性を保ちながら複数トークンを進める方式である。ドラフト候補の精度が低いと検証時に棄却が増え、速度改善が小さくなる。

- **2025-02 · [KVCrush: Key value cache size-reduction using similarity in head-behaviour](2025-2503.00022-kvcrush-key-value-cache-size-reduction-using-similarity-in-head-behaviou.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVCrushは、長文脈のLLM推論でKVキャッシュを縮小する際に、重要度の高いトークンだけを残す既存方式の弱点を補う手法である。平均KV削減率約4倍の条件でも精度低下を小さく抑えられる一方、すべての個別課題でFullKVに勝つわけではない。

### 3年前（2023-11〜2024-10）

- **2024-01 · [BurstGPT: A Real-world Workload Dataset to Optimize LLM Serving Systems](2024-2401.17644-burstgpt-real-world-llm-serving-workload-dataset.md)**  
  実装：[✓](https://github.com/HPMLL/BurstGPT) ・ リポジトリ内被引用：69  
  Azure OpenAI GPTサービスの1031万件・213日分の実トレースと再生基盤BurstGPT-Perfを公開し、平均RPSだけを揃えた合成負荷では見えないバースト、会話間隔、応答長、失敗がサービング評価の結論を変えることを示す。

- **2024-03 · [The Unreasonable Ineffectiveness of the Deeper Layers](2024-2403.17887-the-unreasonable-ineffectiveness-of-the-deeper-layers.md)**  
  実装：✓ ・ リポジトリ内被引用：39  
  削除したい層数を決め、入力・出力間の角距離が最小の連続ブロックを選択し、実際に層を除去する。Llama-2系列の5-shot MMLUでは削除率45〜55%付近で急落するが、Qwen系列では約20%付近で急落する。

- **2024-04 · [Characterizing Power Management Opportunities for LLMs in the Cloud](2024-ad611bbc0cdc-characterizing-power-management-opportunities-for-llms-in-the-cloud.md)**  
  実装：✓ ・ リポジトリ内被引用：28  
  この観測を使い、優先度別の二段階電力制御を行うPOLCAを提案する。著者らは本番トレースから生成した合成負荷を用いた離散事象シミュレーションで、既存の電力予算のままサーバーを30%多く配置しても、設定した遅延SLOを満たし、通常条件で電力ブレーキを起こさない結果を示した。

- **2024-02 · [A Comprehensive Evaluation of Quantization Strategies for Large Language Models](2024-2402.16775-a-comprehensive-evaluation-of-quantization-strategies-for-large-language.md)**  
  実装：[✓](https://github.com/cordercorder/quant_eval) ・ リポジトリ内被引用：14  
  本論文は、新しい量子化器を提案するものではなく、既存の量子化方式をモデル能力、指示追従・整合性、推論効率という異なる観点で測り直す比較実験である。論文のSpQR実装は低ビットの値域を模擬しながら高精度形式で重みを保持しており、品質の比較には使えても実メモリ削減を実証しない。

- **2024-01 · [Escape Sky-high Cost: Early-stopping Self-Consistency for Multi-step Reasoning](2024-2401.10480-escape-sky-high-cost-early-stopping-self-consistency-for-multi-step-reas.md)**  
  実装：[✓](https://github.com/Yiwei98/ESC) ・ リポジトリ内被引用：11  
  多段階推論では、単一の思考連鎖（Chain-of-Thought、CoT）だけで回答すると、途中の偶然の誤りがそのまま最終回答に伝わる。自己整合性（自己整合性、SC）は同一問題から複数の思考連鎖を独立に標本化し、最終回答を多数決してこの変動を抑える。しかしSCは難しい問題にも簡単な問題にも、事前に決めた最大標本数を一律に使う。

- **2024-02 · [Benchmarking and Dissecting the Nvidia Hopper GPU Architecture](2024-2402.13499-benchmarking-and-dissecting-the-nvidia-hopper-gpu-architecture.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  Hopper世代のGPUは第4世代テンソル Core、8ビット浮動小数点（FP8）、ワープグループ行列積（wgmma）、動的計画法命令（DPX）、テンソルメモリアクセラレータ（TMA）、分散共有メモリ（DSM）を備える。しかし仕様表のピーク演算量や帯域だけでは、行列形状、オペランド配置、電力、精度変換、カーネル起動の費用を含む実性能は分からない。

- **2024-06 · [Measuring and Improving the Energy Efficiency of Large Language Models Inference](2024-f40d5b5275ad-measuring-and-improving-the-energy-efficiency-of-large-language-models-i.md)**  
  実装：[✓](https://github.com/maufadel/EnergyMeter) ・ リポジトリ内被引用：8  
  著者らは推論をモデルパラメータ数だけで比較する慣習にも疑問を投げかけ、層の深さ、注意・フィードフォワードの並列化、バッチ数、量子化形式の実行実装を分けて検証した。

- **2024-04 · [Toward Inference-optimal Mixture-of-Expert Large Language Models](2024-2404.02852-toward-inference-optimal-mixture-of-expert-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  MoEのスケーリング則へ推論費用を組み込み、専門家数を増やした「損失最適」構成より、小さなMoEを多くのデータで学習する構成が配信費用まで含めて有利になる領域を示す。

- **2024-09 · [Art and Science of Quantizing Large-Scale Models: A Comprehensive Overview](2024-2409.11650-art-and-science-of-quantizing-large-scale-models-a-comprehensive-overvie.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、大規模モデルの量子化（量子化）を、重みと活性値の数値表現、学習後量子化（post-学習 量子化; PTQ）、量子化認識学習（量子化-aware 学習; QAT）、知識蒸留（knowledge distillation）、鍵・値キャッシュ（key-value キャッシュ; KV キャッシュ）の圧縮という複数の切り口から整理した概説論文である。

### 4年前（2022-11〜2023-10）

- **2023-10 · [From Words to Watts: Benchmarking the Energy Costs of Large Language Model Inference](2023-2310.03003-from-words-to-watts-benchmarking-the-energy-costs-of-large-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：28  
  対象は初代LLaMAの7B、13B、65Bで、NVIDIA V100とA100、自然言語指示のAlpaca、算術問題のGSM8Kを用いる。この研究は新しい注意演算や復号アルゴリズムを提案するものではない。

- **2023-09 · [Large Language Model Routing with Benchmark Datasets](2023-2309.15789-large-language-model-routing-with-benchmark-datasets.md)**  
  実装：[✓](https://github.com/UMich-FATML/llm-routing) ・ リポジトリ内被引用：11  
  しかし実際のサービスでは、数学問題、法務文書、要約、常識質問など、タスクごとに得意なモデルが異なる。常に最も大きいモデルを呼ぶ方式は品質を得やすい反面、必要以上の推論計算を消費する。これらは品質と必要なモデル呼出し回数の評価であり、実際のGPU実行時間・請求金額の削減倍率を測定したものではない（原著§5、表1・2）。

- **2023-05 · [A Quantitative Review on Language Model Efficiency Research](2023-2306.01768-a-quantitative-review-on-language-model-efficiency-research.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、新しい高速化アルゴリズムや推論カーネルを提案する研究ではなく、既存の効率的言語モデル研究が公開した評価表を出典とともに集め直し、論文間で比較できる範囲と比較できない範囲を調べるメタ分析である。

### 5年前（2021-11〜2022-10）

- **2022-02 · [A Survey on Model Compression and Acceleration for Pretrained Language Models](2022-2202.07105-a-survey-on-model-compression-and-acceleration-for-pretrained-language-m.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  著者らは推論段階を対象に、重み共有、低ランク分解、枝刈り、量子化、知識蒸留、早期終了、トークン省略の七系統を比較する。

- **2022-08 · [Momentum Transformer: Closing the Performance Gap Between Self-attention and Its Linearization](2022-2208.00579-momentum-transformer-closing-the-performance-gap-between-self-attention-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モーメンタム Transformerは、通常のソフトマックス注意を線形化した際に失われる表現力を、最適化アルゴリズムのモーメンタムに着想を得た状態更新で補おうとする研究である。だが、LRAの平均正答率は標準ソフトマックスの58.70%を下回る56.04%であり、翻訳の生成速度も標準ソフトマックスの方が大きい。

### 6年前（2020-11〜2021-10）

- **2021-10 · [Efficiently Modeling Long Sequences with Structured State Spaces](2021-2111.00396-efficiently-modeling-long-sequences-with-structured-state-spaces.md)**  
  実装：[✓](https://github.com/HazyResearch/state-spaces) ・ リポジトリ内被引用：111  
  自己注意（self-注意機構）は系列長Lに対して二次の注意行列を作るため、1万〜数万ステップの系列では計算・メモリ負荷が大きくなる。論文はLong Range Arena（LRA）の全課題で当時の最良水準を更新し、長さ16,384のPath-Xで88%正解率を達成した。
<!-- survey:auto:end -->
