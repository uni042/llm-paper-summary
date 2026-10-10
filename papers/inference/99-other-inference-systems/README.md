# Other Inference Systems

推論効率化を主目的とするが、現時点では他の系統へ自然に入らず、**独立系統を作るほど同種研究がまだ集まっていない手法**を置く。ここに論文が増えて共通した問題設定・主要技術・評価軸が見えてきた場合は、新しい系統へ分割する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（392本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-01 · [DART: Diffusion-Inspired Speculative Decoding for Fast LLM Inference](2026-2601.19278-dart-diffusion-inspired-speculative-decoding-for-fast-llm-inference.md)**  
  実装：[✓](https://github.com/fvliang/DART) ・ リポジトリ内被引用：8  
  対象LLM特徴から未来ロジットを1回で並列予測しN-gram木刈り込みを行い、EAGLE3より平均約30%高い投機デコード高速化を得る。

- **2026-02 · [P-EAGLE: Parallel-Drafting EAGLE with Scalable Training](2026-2602.01469-p-eagle-parallel-drafting-eagle-with-scalable-training.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  投機的復号は軽いドラフトモデルが先に複数トークンを提案し、大きな対象モデルがまとめて検証することで、対象モデルの重みを読む回数を減らす。vLLMでの実測では、GPT-OSS 20B、120B、Qwen3-Coder 30Bに対し、自己回帰EAGLE-3比で代表的に1.10〜1.36倍の生成処理量改善を報告する。

- **2026-01 · [Double: Breaking the Acceleration Limit via Double Retrieval Speculative Parallelism](2026-2601.05524-double-breaking-the-acceleration-limit-via-double-retrieval-speculative-.md)**  
  実装：[✓](https://github.com/Sylvan820/Double1) ・ リポジトリ内被引用：7  
  Doubleは、並列投機的復号（Parallel 投機的復号; PSD）における二つの性能制約を同時に解く。この方式は、ドラフト用の追加学習を必要としない。原著の8基のNVIDIA A100 80GBによる実験では、LLaMA3.3-70BのHumanEvalで通常のターゲット推論に対して5.33倍、Qwen3-32Bでは2.84倍の実時間高速化を示す。

- **2026-07 · [FlashAccel: Leveraging High-Bandwidth Flash (HBF) for High-Throughput LLM Inference](2026-2607.10186-flashaccel-high-bandwidth-flash-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  HBM級帯域・大容量の高帯域フラッシュをGPUへ統合し、SRAM先読み、重み/KV専用配置、KVの選択的HBM複製、追記型永続管理を協調させて、モデル重みとKVキャッシュをフラッシュ上で直接高並列アクセスする推論アクセラレータ。

- **2026-03 · [PIMphony: Overcoming Bandwidth and Capacity Inefficiency in PIM-Based Long-Context LLM Inference System](2026-ff07d7af9733-pimphony-overcoming-bandwidth-and-capacity-inefficiency-in-pim-based-long-context-llm-inference-system.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  長文脈のLLMがトークンを一つずつ生成するとき、注意機構はこれまでの各トークンに対応する鍵・値キャッシュ（KV キャッシュ）を読み返す。動的PIMアクセス（動的 PIM Access; DPA）は生成中のトークン数に応じたループとアドレス変換を使い、KVキャッシュを実行時に1MB単位で追加する。

- **2026-01 · [Fast KVzip: Efficient and Accurate LLM Inference with Gated KV Eviction](2026-2601.17668-fast-kvzip-efficient-and-accurate-llm-inference-with-gated-kv-eviction.md)**  
  実装：[✓](https://github.com/Janghyun1230/FastKVzip) ・ リポジトリ内被引用：4  
  長文脈の言語モデルは、生成のたびに過去の鍵・値（KV）を参照するため、文脈が長くなるとキャッシュがGPUメモリを圧迫する。重要でないKVを削除する方法は容量を減らせるが、何を消すかを決めるために過去の注意を再計算すると、圧縮器自体の費用が大きくなる。

- **2025-12 · [Janus: Disaggregating Attention and Experts for Scalable MoE Inference](2025-2512.13525-janus-disaggregating-attention-and-experts-for-scalable-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  Janusは、大規模混合専門家モデル（Mixture-of-エキスパート; MoE）をモデル全体の1単位としてGPUへ置くのではなく、注意層とエキスパート層を別GPU プールへ分離し、両者を独立にprovision/規模変更するデコード向けserving システムである。

- **2026-06 · [TWLA: Achieving Ternary Weights and Low-Bit Activations for LLMs via Post-Training Quantization](2026-2606.13054-twla-achieving-ternary-weights-and-low-bit-activations-for-llms-via-post.md)**  
  実装：[✓](https://github.com/Kishon-zzx/TWLA) ・ リポジトリ内被引用：3  
  TWLA（Ternarized Weights and Low-bit Activations）は、学習済み大規模言語モデル（LLM）の重みを三値へ圧縮し、さらに活性値を平均4ビット級へ下げる事後学習量子化（Post-学習 量子化; PTQ）の研究である。ここではFP16の23.70トークン/秒に対しTWLAが86.35トークン/秒を示した。

- **2026-06 · [CAT-Q: Cost-efficient and Accurate Ternary Quantization for LLMs](2026-2606.26650-cat-q-cost-efficient-and-accurate-ternary-quantization-for-llms.md)**  
  実装：[✓](https://github.com/IntelChina-AI/BitTern) ・ リポジトリ内被引用：3  
  CAT-Q（コスト-efficient and Accurate Ternary Quantization）は、既存の高精度LLMを三値重み {−1, 0, +1}、すなわち約1.58-bitへ変換する学習後量子化（Post-学習 量子化; PTQ）方式である。三値化はFP16重みに比べて理論上10倍超の重みメモリ削減を可能にし、0状態による疎性も持つ。

- **2026-02 · [Fast KV Compaction via Attention Matching](2026-2602.16284-fast-kv-compaction-via-attention-matching.md)**  
  実装：[✓](https://github.com/adamzweiger/compaction) ・ リポジトリ内被引用：3  
  長文脈のKVキャッシュを、将来の問い合わせで元の注意挙動を再現する短い鍵・値・バイアスへ置き換える。参照問い合わせの生成、鍵選択、非負最小二乗による注意質量合わせ、値の最小二乗推定を組み合わせる。

- **2026-01 · [MELINOE: Fine-Tuning Enables Memory-Efficient Inference for Mixture-of-Experts Models](2026-2602.11192-melinoe-fine-tuning-enables-memory-efficient-inference-for-mixture-of-ex.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  MELINOEは、混合専門家モデル（MoE）の専門家重みをCPUへ退避する推論環境で、モデル自身の専門家選択を少数の再利用しやすい専門家へ寄せる手法である。著者らはOLMoE、Phi-3.5-MoE、Mixtral-8x7Bを対象に、H100、A100、RTX 4090のメモリ制限環境で評価した。

- **2026-01 · [Latent Space Communication via K-V Cache Alignment](2026-2601.06123-latent-space-communication-via-k-v-cache-alignment.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  モデル固有のKVキャッシュを、共有潜在空間への入出力変換器を介して交換する。単に同じ数値へ復元するのではなく、受信側が後続トークンを正しく予測できる状態を学ぶことで、異なる言語モデル間の内部状態共有を可能にする。

- **2026-06 · [Models Take Notes at Prefill: KV Cache Can Be Editable and Composable](2026-2606.17107-models-take-notes-at-prefill-kv-cache-can-be-editable-and-composable.md)**  
  実装：[✓](https://github.com/19PINE-AI/programmable-kv) ・ リポジトリ内被引用：2  
  プリフィル済みKVキャッシュを結論メモとして捉え、追記訂正による編集とRoPE再配置による部品合成で再プリフィルを回避する。

- **2026-05 · [An Efficient Hybrid Sparse Attention with CPU-GPU Parallelism for Long-Context Inference](2026-2605.07719-an-efficient-hybrid-sparse-attention-with-cpu-gpu-parallelism-for-long-context-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  CPU常駐KV向けに出力寄与ベース予算配分とCPU・GPU協調疎注意を統合し、長文復号を最大3.7倍高速化する。

- **2026-02 · [RelayCaching：協調LLMの生成KVキャッシュ再利用](2026-2603.13289-relaycaching-accelerating-llm-collaboration-via-decoding-kv-cache-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  前段エージェントのデコードKVを後段プリフィルへ渡し、位置補正と中間層・重要トークンだけの疎な再計算で80%以上を再利用し、TTFTを最大4.7倍短縮する。

- **2026-02 · [ICaRus: Identical Cache Reuse for Efficient Multi Model Inference](2026-2603.13281-icarus-identical-cache-reuse-for-efficient-multi-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  複数の専門言語モデルを順番に呼び出すエージェント型推論では、同じシステム指示、会話履歴、検索資料を何度も入力する。LLaMA-3.1-8Bを使うReAct型の8エージェント構成では、通常のモデル別KV方式に対して95パーセンタイル遅延（P95、遅い側5%に入る境界）を最大11.1倍短縮し、最大スループットを3.8倍に高めた。

- **2025-12 · [Kitsune: Enabling Dataflow Execution on GPUs with Spatial Pipelines](2025-2502.18403-kitsune-enabling-dataflow-execution-on-gpus-with-spatial-pipelines.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  カーネル境界で中間テンソルが高帯域メモリへ書き戻され、次のカーネルが再び読む。さらに、一般命令主体のCTAとテンソル演算主体のCTAを同じストリーミングマルチプロセッサ（SM）へ配置できるようグリッドスケジューラを拡張する。

- **2025-12 · [HiFC: High-efficiency Flash-based KV Cache Swapping for Scaling LLM Inference](2026-f52f99f3360a-hifc-high-efficiency-flash-based-kv-cache-swapping-for-scaling-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  GPUとNVMe SSDをGDSで直結し、pSLCと順次KVブロック配置でDRAMなしのKV交換を実現し、長文脈推論の性能を保ちながら容量費用を削減する。

- **2025-12 · [DEER: Draft with Diffusion, Verify with Autoregressive Models](2025-2512.15176-deer-draft-with-diffusion-verify-with-autoregressive-models.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  DEERは、投機的復号の候補生成器を、左から右へ逐次生成する小型自己回帰モデルから、複数位置をまとめて予測できる離散拡散言語モデル（discrete diffusion language モデル）へ置き換える方式である。

- **2025-11 · [FlexiCache: Leveraging Temporal Stability of Attention Heads for Efficient KV Cache Management](2025-2511.00868-flexicache-leveraging-temporal-stability-of-attention-heads-for-efficient-kv-cache-management.md)**  
  実装：[✓](https://github.com/NazmulTakbir/FlexiCache) ・ リポジトリ内被引用：2  
  重要KVページが時間的に入れ替わりやすい注意ヘッドだけ全KVをGPUへ残し、安定ヘッドは上位ページ以外をCPUへ退避・周期再昇格することで、精度を保ちながらGPUメモリを最大70%削減する。

- **2026-09 · [HBFlex: A Flexible Memory System for Bridging Fine-Grained LLM States and Coarse-Grained HBF Parallel Execution](2026-2609.18675-hbflex.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  全HBF構成でKV配置・書戻し・寿命認識GCを共同最適化し、FlashAccel比最大1.58倍、H3比最大3.30倍の平均スループット向上。

- **2026-08 · [FlashPrefill V2: Block-Sparse Prefill Attention for Long-Context LLM Serving](2026-2608.19758-flashprefill-v2-block-sparse-prefill-attention-for-long-context-llm-serving.md)**  
  実装：[✓](https://github.com/qhfan/FlashPrefillv2) ・ リポジトリ内被引用：1  
  平均補正付きブロック疎注意をHopper向けに再設計し、SGLangの長文事前充填を128Kで最大4.8倍高速化する。

- **2026-08 · [Bole: Efficient Tree Speculation for Hybrid-Attention Language Models](2026-2608.01651-bole-efficient-tree-speculation-for-hybrid-attention-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  再帰型線形注意の木検証を厳密閉形式で並列化し、因子化状態とhardware-aware予算をSGLangへ統合して最大4.72倍のデコード スループットを実現。

- **2026-06 · [RoPE-Aware Bit Allocation for KV-Cache Quantization](2026-2606.24033-rope-aware-bit-allocation-for-kv-cache-quantization.md)**  
  実装：[✓](https://github.com/JIA-Lab-research/blockgtq) ・ リポジトリ内被引用：1  
  回転位置埋め込みの周波数ブロックごとのエネルギーに応じて鍵キャッシュのビット幅を配分し、圧縮した鍵・値を直接読む融合注意計算で長文脈推論の容量とメモリ帯域を同時に削減する。

- **2026-05 · [SYMPHONY: Enabling Compute-Memory Disaggregation in LLM Serving Systems](2026-0fd53670e945-symphony-enabling-compute-memory-disaggregation-in-llm-serving-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  将来要求の助言信号でKVキャッシュを事前移動し、層優先度と協調HBM管理で不確実性を吸収して計算・メモリ分離を低遅延化する。

- **2026-05 · [Move the Query, Not the Cache: Characterizing Cross-Instance Latent Attention Redistribution Across GPU Fabrics](2026-2606.01502-move-the-query-not-the-cache-characterizing-cross-instance-latent-attention-redistribution-across-gpu-fabrics.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  約1KBの問い合わせを遠隔キャッシュへ送り注意計算する方式を実H100で測定し、約3msのキャッシュ再適応より数十µsの往復が有利となる条件を閉形式化する。

- **2026-05 · [How Far Can Disaggregation Go? A Design-Space Exploration of Attention-FFN Disaggregation for Efficient MoE LLM Serving](2026-2605.28302-how-far-can-disaggregation-go-a-design-space-exploration-of-attention-ffn-disaggregation-for-efficient-moe-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  注意とMoE-FFNの演算・通信を別GPU群へ分離する価値を、負荷・モデル・SLO・ネットワークを横断して設計空間探索する。

- **2026-03 · [ArcLight: A Lightweight LLM Inference Architecture for Many-Core CPUs](2026-2603.07770-arclight-a-lightweight-llm-inference-architecture-for-many-core-cpus.md)**  
  実装：[✓](https://github.com/OpenBMB/ArcLight) ・ リポジトリ内被引用：1  
  NUMAごとのメモリ配置、動的スレッド群、Scatter/Gather型テンソル並列を一体化し、多数コアCPUの遠隔メモリアクセス壁を避けて、192コアARM環境でllama.cpp比最大46%高い推論スループットを示す軽量CPU推論基盤。

- **2026-02 · [Out of the Memory Barrier: A Highly Memory Efficient Training System for LLMs with Million-Token Contexts](2026-2602.02108-out-of-the-memory-barrier-a-highly-memory-efficient-training-system-for-llms-with-million-token-contexts.md)**  
  実装：[✓](https://github.com/wenhaoli-xmu/OOMB) ・ リポジトリ内被引用：1  
  チャンク再計算・ページ化KV/勾配・非同期CPUオフロード・疎注意を統合し、Qwen2.5-7Bの4M文脈学習を単一H200で実現する。

- **2026-02 · [MoSE: Mixture of Slimmable Experts for Efficient and Adaptive Language Models](2026-2602.06154-mose-mixture-of-slimmable-experts-for-efficient-and-adaptive-language-mo.md)**  
  実装：[✓](https://github.com/tnurbek/mose) ・ リポジトリ内被引用：1  
  MoSEは、混合専門家モデル（Mixture-of-Experts; MoE）の「専門家を何個選ぶか」に加え、「選んだ各専門家を何割の中間幅で実行するか」を推論時に変える研究である。主指標は一トークン当たり浮動小数点演算量（FLOPs/トークン）と品質であり、実機処理率は補助的な検証である。

- **2026-02 · [Effective MoE-based LLM Compression by Exploiting Heterogeneous Inter-Group Experts Routing Frequency and Information Density](2026-2602.09316-effective-moe-based-llm-compression-by-exploiting-heterogeneous-inter-gr.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  RFID-MoEは、混合専門家（Mixture-of-Experts; MoE）型の大規模言語モデルを、事後学習の重み圧縮で小さくする研究である。論文はQwen3-235B-A22Bの総重み容量が8基のA100 40GB、合計320GBに収まらない例を挙げ、演算の疎性と保存容量の大きさが別問題であることを示す。

- **2026-01 · [Towards Compute-Aware In-Switch Computing for LLMs Tensor-Parallelism on Multi-GPU Systems](2026-161bea97e0de-towards-compute-aware-in-switch-computing-for-llms-tensor-parallelism-on-multi-gpu-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  NVLSの通信意味論をLLM計算カーネルの読み書き要求へ合わせ、スイッチ内要求マージ・GPU間TB協調・データフロー重畳でテンソル並列の通信待ちを削減する。

- **2026-01 · [ContiguousKV: Accelerating LLM Prefill with Granularity-Aligned KV Cache Management](2026-2601.13631-contiguouskv-accelerating-llm-prefill-with-granularity-aligned-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  KV 枝刈りとI/Oの粒度をContiguousChunkへ統一し、二段非同期プリフェッチでSSD KV読み込みを計算と重ねてRe-プリフィルを最大3.85倍高速化する。

- **2025-11 · [LUT-LLM: Efficient Large Language Model Inference with Memory-based Computations on FPGAs](2025-2511.06174-lut-llm-efficient-large-language-model-inference-with-memory-based-computations-on-fpgas.md)**  
  実装：[✓](https://github.com/LUT-FPGA/LUT-LLM) ・ リポジトリ内被引用：1  
  活性値・重み共同ベクトル量子化で線形層を2次元表引きへ変換し、AMD V80上のQwen3 1.7BでGPU比1.10〜3.29倍高速化を示す。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-10 · [TopK-Guided: Adaptive, Budget-Aware Activation Sparsity for Efficient LLM Inference](2026-2610.01763-topk-guided-adaptive-budget-aware-activation-sparsity-for-efficient-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  両手法はさらにTransformer層間へ一様な疎性予算を与え、疎化への耐性が異なる層を区別しない。論文のC4評価では、Llama-2-7BとLlama-3-8Bの目標疎性30%、50%、70%で、TopK-GuidedはTEALおよびWINAと比べperplexityと8課題平均正解率の両方で全条件最高だった。

- **2026-09 · [Where Should the KV Cache Live? Placement Policies Across GPU, CPU, and SSD for Long-Lived Sessions](2026-2609.16215-where-should-the-kv-cache-live-placement-policies-across-gpu-cpu-and-ssd-for-long-lived-sessions.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU・CPU・SSD間のKV配置政策を比較し、SSDの容量利得とワークロード別の最適配置・遅延境界を定量化する。

- **2026-09 · [Validating Hybrid-State Cache Recovery for GLM-5.3-Flash with vLLM and LMCache](2026-2609.15030-validating-hybrid-state-cache-recovery-for-glm-5-3-flash-with-vllm-and-lmcache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GLM-5.3-Flash＋vLLM＋LMCacheの完全キャッシュヒット境界ずれを厳密プレフィックス復旧で修正し、出力同一性を保ったCPUキャッシュ再ロードのTTFT短縮を実証。

- **2026-09 · [Unlocking Software-defined GPU Fabric Scheduling in the LLM Era](2026-a43ed4b300bf-unlocking-software-defined-gpu-fabric-scheduling-in-the-llm-era.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPUファブリック競合を監視・通信注入制御し、vLLM+MooncakeでPD KV転送を19.4–34.4%短縮する。

- **2026-09 · [Unlocking Lossless Speedups in LLMs via Discrete Diffusion](2026-2609.04010-unlocking-lossless-speedups-in-llms-via-discrete-diffusion.md)**  
  実装：[✓](https://github.com/ifm-ai/uno) ・ リポジトリ内被引用：0  
  元の自己回帰モデル分布を保ったまま追加した離散拡散重みで複数トークンを並列提案し、専用サンプラで正しく補正して、逐次デコードの重み読出し回数を減らす。

- **2026-09 · [The Inference Engineering Pareto Atlas: Which Optimizations Dominate the Cost, Quality, and Latency Frontier?](2026-2609.17863-inference-engineering-pareto-atlas.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  54実測点と校正シミュレータで推論最適化の組合せを品質・遅延・費用の同一Pareto面へ置き、制約別の支配構成を示す。

- **2026-09 · [Taming Bitwise Behavior in GPU Kernels with Tensor Core: Black-Box Reconstruction, Compiler Enforcement, and Static Verification](2026-2609.11356-taming-bitwise-behavior-gpu-tensor-core-kernels.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU縮約順序を記述子化し、非公開行列積のビット挙動復元、コンパイラでの平衡木強制、命令列の静的同値判定を接続して再現性と自動調整を両立する。

- **2026-09 · [SpliTEE: Improving LLM Inference on Trusted Hardware with Differentially Private GPU Outsourcing](2026-2609.15039-splitee-improving-llm-inference-on-trusted-hardware-with-differentially-private-gpu-outsourcing.md)**  
  実装：[✓](https://github.com/DPVault/SpliTEE) ・ リポジトリ内被引用：0  
  TEE内のLLM線形演算を差分プライバシーで保護してGPUへ委譲し、プロンプト漏洩を抑えつつCPU-only TDX推論を約2倍高速化する。

- **2026-09 · [SiliconBench: Speed, Memory, and Fidelity for LLM Serving on Unified-Memory Desktops](2026-2609.19169-siliconbench-speed-memory-and-fidelity-for-llm-serving-on-unified-memory-desktops.md)**  
  実装：[✓](https://github.com/WindChimeRan/SiliconBench) ・ リポジトリ内被引用：0  
  Apple Siliconの九推論基盤を速度・共有メモリ・忠実度・新モデル対応・複数機で横断監査し、vllm-metalの並行処理と遠隔直接メモリアクセスを使うテンソル並列の優位を示す。

- **2026-09 · [Shared-Prefix KV Reuse Across Standard LoRA Adapters: Quality and Serving Tradeoffs](2026-2609.17109-shared-prefix-kv-reuse-across-standard-lora-adapters-quality-and-serving-tradeoffs.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既学習の標準LoRA間で基盤モデル接頭辞KVを直接再利用し、8K暖機済み初回トークン時間約16倍と小さいが不確実な品質低下、物理共有未実装という実運用上の境界を測定する。

- **2026-09 · [Separating Stream Stability from Long-Term Recall in Language Models](2026-2609.07282-stream-stability-long-term-recall-threeh.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長時間生成の安定性・過去情報への因果アクセス・タスク効用をThreeHの3到達距離へ分離し、注意シンクの安定生成を長期記憶と誤認しない評価契約を示す。

- **2026-09 · [SemBridge: Compiling Consumer Observations into Cross-Stack Communication Plans](2026-2609.08231-sembridge-compiling-consumer-observations-into-cross-stack-communication-plans.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  異種CUDA/NCCL–CANN/HCCL境界で消費者が必要とする観測結果を型付き契約へコンパイルし、不要な全logit転送をトークン投影へ縮約して結果通信を99.97%以上削減する通信計画器。

- **2026-09 · [Scaling Post-Training Ternarisation to Qwen3-8B Capability Retention, Reproduction, Lossless Packing, and Packed Execution](2026-2609.09240-scaling-post-training-ternarisation-to-qwen3-8b-capability-retention-reproduction-lossless-packing-and-packed-execution.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Qwen3-8Bを適応的約1.64 bit/重みへ後量子化し、78.5%の補正済み能力保持、8.24 GiBの無損失packed artifact、RTX 5070上15.52 トークン/s・7.35 GiBの直接実行まで検証する。

- **2026-09 · [SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking](2026-2609.13141-sas-simple-attention-sparsification-via-end-to-end-optimization-of-context-ranking.md)**  
  実装：[✓](https://github.com/Tencent-Hunyuan/Simple-Attention-Sparsification) ・ リポジトリ内被引用：0  
  言語モデル損失を注意ソフトマックス内の連続ゲートへ直接流してコンテキスト順位を学習し、固定Top-K疎注意の精度と長文脈デコード効率を改善する。

- **2026-09 · [Sample-Guided Exact Top-K Selection for Long-Context Sparse Attention](2026-2609.08450-sample-guided-exact-topk-sparse-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HPC-Ops Top-Kは、標本で上位候補境界を予測し、全行の一回走査で十分性を証明、足りない時だけ回復して正確なK個を選び、長文疎注意の再走査を減らす。

- **2026-09 · [RoofLang: Enabling AI-Driven Architecting of LLM Inference Systems](2026-2609.12551-rooflang-ai-driven-llm-inference-architecting.md)**  
  実装：[✓](https://github.com/yzygitzh/rooflang) ・ リポジトリ内被引用：0  
  RoofLangはLLM推論を計算・ハードウェアグラフと意味保存変換で表し、実装非依存のシミュレーションを評価器としてAIに配置・並列化・通信構成を探索させる設計基盤である。

- **2026-09 · [RGSQ：リーマン幾何感度型量子化](2026-2609.25492-rgsq-riemannian-geometry-sensitive-quantization-for-large-vision-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の学習後量子化は、量子化前後の差をユークリッド距離で測り、各方向の誤差をほぼ等価に扱う。

- **2026-09 · [Quality-Constrained Routing over a Fixed Pool of Quantized Mixture-of-Experts Instances](2026-2609.12550-quality-constrained-routing-over-a-fixed-pool-of-quantized-mixture-of-experts-instances.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  固定常駐したW2・W3・W4量子化MoEインスタンス間で、入力時の脆弱性重み付きパープレキシティから要求別の量子化リスクを推定し、品質予算付き線形計画で高処理量側へ配分する要求ルーティング。

- **2026-09 · [Pull: Lazy Materialization of Working Memory for Stateful LLM Conversations](2026-2609.14773-pull-lazy-working-memory-materialization.md)**  
  実装：[✓](https://github.com/wulun811/kongmen-pull) ・ リポジトリ内被引用：0  
  長期対話を決定論的な索引で管理し、質問ごとに必要な原文ターンだけを可逆的に実体化して入力トークンを削減するセッションルータ。

- **2026-09 · [PolarKV: Tier Locally, Serve Globally–A KV Cache over Cloud Memory and Storage](2026-4820586f504d-polarkv-tier-locally-serve-globally-a-kv-cache-over-cloud-memory-and-storage.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分散メモリを帯域層、クラウドブロックストレージを容量層とし、対応シャードを同一VMへ共置してKVの階層移動をローカル化することで、クラウドのネットワーク帯域と費用の制約を抑えるKVキャッシュ基盤。

- **2026-09 · [Physically Partitioned KVCache Format for CPU–GPU Load Balancing in MoE Inference](2026-2609.14507-physically-partitioned-kvcache-format-for-cpu-gpu-load-balancing-in-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVを書込時にCPU計算用・GPU転送用の物理領域へ固定配置し、ルーフラインで系列を動的分担することで、単一GPUの長文MoE推論を高速化する。

- **2026-09 · [PELM: Power Efficient On-Device LLM Inference with Speculative Decoding and Dynamic Voltage Frequency Scaling](2026-2609.09662-pelm-speculative-decoding-dvfs.md)**  
  実装：[✓](https://github.com/imec-nu/PELM) ・ リポジトリ内被引用：0  
  DVFS・自己投機的デコード・可変検証深度を深層強化学習で共同制御し、端末LLMで最大23.1%高速化・52.4%エネルギー削減を達成する。

- **2026-09 · [Partition-Aware Scheduling for Mobile Heterogeneous Inference Co-Execution](2026-2609.14213-partition-aware-scheduling-for-mobile-heterogeneous-inference-co-execution.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  演算子のCPU-GPU分割とDAG上の実行順を共同最適化し、段階化・臨界度標本化・遅延予測による配備時反復探索でオフライン最適化に近いモバイル推論遅延を得る。

- **2026-09 · [Online Draft Co-Training for Speculative Decoding in Large-Scale, Long-Context RL Post-Training](2026-2609.07108-online-draft-co-training-for-speculative-decoding-in-large-scale-long-context-rl-post-training.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈RLで投機的復号のドラフトを方策と同時更新するため、分岐注意を文脈並列リングへ統合し、中間特徴をパイプライン外のTapChannelで輸送して、最大122B規模で学習品質を保ちつつ最大1.88倍の全体高速化を得る。

- **2026-09 · [OBC-Prune: Outcome-Based Calibration for Large Reasoning Model Pruning](2026-2609.17890-obc-prune-outcome-based-calibration-for-large-reasoning-model-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  正答・誤答の思考過程を同一問題で対にし、文ごとの因果的寄与で較正活性値を再重み付けすることで、一発枝刈り後の推論精度と停止挙動を改善する。

- **2026-09 · [MiX: Micro-Inverted-Scaling for End-to-End Low-Bit Vision-Language Model Acceleration](2026-2609.19683-mix-micro-inverted-scaling-for-end-to-end-low-bit-vision-language-model-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  VLMのマルチモーダル外れ値に対し、要素別指数＋共有仮数へマイクロスケーリングを反転し、4bit級の端から端までの量子化と乗算器不要のシフト加算PEを同時に実現する。

- **2026-09 · [MeshKV: A Network-on-Chip KV Cache Fabric for Scalable Transformer Decoding Accelerators](2026-2609.19207-meshkv-a-network-on-chip-kv-cache-fabric-for-scalable-transformer-decoding-accelerators.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  鍵値キャッシュをオンチップ網の分散流へ変換し、8×8 FPGA実装で通信量最大58%削減、鍵値帯域利用率2.1倍、生成処理量最大1.90倍を実測する。

- **2026-09 · [MCSched: Memory-Controller-Aware Scheduling for Embodied LLM Workloads on NVIDIA Jetson](2026-fd0d3fa4e564-mcsched-memory-controller-aware-scheduling-for-embodied-llm-workloads-on-nvidia-jetson.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Jetson統合メモリの隠れた帯域競合を監視し、締切危険時だけ背景LLMを一時停止してロボット処理を保護する軽量実行時スケジューラ。

- **2026-09 · [LeanStream: A Speculate-and-Refine Streaming Framework for Efficient on-Device LLM Inference](2026-2609.03079-leanstream-speculate-refine-on-device.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LeanStreamは、層内の部分残差から次層の重み優先度を更新し、重み読出し・GPU計算・キャッシュを非同期に重ねて、端末LLMのSSD待ちと予測ミスを減らす。

- **2026-09 · [LayerRoute: Adaptive Layer-Skipping with LoRA-Preserved Quality for Efficient LLM Inference](2026-2609.13682-layerroute-adaptive-layer-skipping-with-lora-preserved-quality-for-effic.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  同時にランク-8 LoRAを注意機構 射影へ入れ、層を飛ばすことで失われる表現能力をパラメータ-efficientに補償する。壁時計速度は全試行で改善し1.02〜1.06倍、平均1.04倍。

- **2026-09 · [Kalman Delta Networks: Uncertainty-aware Associative Memory](2026-2609.07816-kalman-delta-networks-associative-memory.md)**  
  実装：[✓](https://github.com/ngocbh/kalman-delta-networks) ・ リポジトリ内被引用：0  
  固定サイズの線形注意メモリに推定不確実性を持たせ、蓄積証拠に応じて上書き強度をカルマン利得から決めることで、長文脈検索と生成精度を改善する。

- **2026-09 · [JustFit: 200K-Token LLM Serving on a 24 GiB Laptop with Just-in-Time State Management](2026-2609.17475-justfit-200k-token-llm-serving-on-a-24-gib-laptop-with-just-in-time-state-management.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  圧縮キー・バリュー実行、部品常駐切替、状態保持遷移を統合し、24 GiB機で27B級モデルの約213K位置の単一要求を完走する推論実行系。

- **2026-09 · [IHS-LM: Intra-batch Hybrid Scheduling and Layer Migration for VLM Pipeline Inference Acceleration on Edge Devices](2026-9b405eddeda4-ihs-lm-intra-batch-hybrid-scheduling-and-layer-migration-for-vlm-pipeline-inference-acceleration-on-edge-devices.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KV容量連動のプリフィル/デコード混在スケジューリングと帯域感知型の境界層移行を統合し、異種Jetson上のVLM推論遅延を最大17.5%削減する。

- **2026-09 · [HoliBench: A Cross-Platform Benchmarking and Deployment Toolkit for Foundation Models in CPS-IoT Applications](2026-2609.12412-holibench-a-cross-platform-benchmarking-and-deployment-toolkit-for-foundation-models-in-cps-iot-applications.md)**  
  実装：[✓](https://github.com/beesfleas/HoliBench) ・ リポジトリ内被引用：0  
  20モデル×7デバイス×3量子化×8推論系を精度・遅延・電力・メモリで統一測定し、実測プロファイルから制約付き配備構成まで選ぶ基盤。

- **2026-09 · [GrowMTP: Can RL Grow Its Own Draft Head?](2026-2609.16648-growmtp-efficient-multi-token-prediction-via-progressive-growth.md)**  
  実装：[✓](https://growmtp.github.io/) ・ リポジトリ内被引用：0  
  強化学習ロールアウトの検証信号でドラフトヘッドをその場で育成し、事前ヘッドなしでも投機的デコードによる学習加速を実現する。

- **2026-09 · [GDN Tree-Scan: Served Tree Verification for Recurrent-Hybrid Language Models](2026-2609.23900-gdn-tree-scan-served-tree-verification-for-recurrent-hybrid-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  再帰状態を持つハイブリッドLLMの木型投機検証で、枝ごとのGDN状態を親子関係どおりに走査し、受理枝だけを永続化することで、Qwen3.6-27B-FP8のデコード処理量を27.0%改善する。

- **2026-09 · [FoldQuantVLA: Native Low-Bit Quantization of Vision-Language-Action Models via Consistent Folding](2026-2609.24433-foldquantvla-native-low-bit-quantization-of-vision-language-action-models-via-consistent-folding.md)**  
  実装：[✓](https://github.com/cair-vinuni/FoldQuantVLA) ・ リポジトリ内被引用：0  
  VLAの共有活性値変換を校正から重み丸め、TensorRT実行まで一貫させる学習後量子化を設計し、W4A4でOrin上の推論を浮動小数点TensorRT比1.20〜1.33倍に高速化した。

- **2026-09 · [FlexEE: Self-Speculative and KV-Compatible Early Exiting for Offloading-Aware LLM Inference](2026-2609.17008-flexee-self-speculative-and-kv-compatible-early-exiting-for-offloading-aware-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Top-K自己投機による軽量な早期退出と隠れ状態の持越しでKV整合性を保ち、重みオフロード時に後段層の計算と転送をまとめて省く。

- **2026-09 · [FlashGPU-sim: Enabling GPU Modeling for Modern Architectures and AI Workloads](2026-2609.15311-flashgpu-sim-enabling-gpu-modeling-for-modern-architectures-and-ai-workloads.md)**  
  実装：[✓](https://github.com/FlashGPU-Sim/FlashGPU-Sim) ・ リポジトリ内被引用：0  
  Hopper/Blackwellの非同期GPU機構とTriton AIカーネルを実行駆動で再現し、131構成でサイクル誤差5.24%、16スレッドで7.86倍高速化した現代GPUシミュレータ。

- **2026-09 · [Flash-dLLM: IO-Aware KV Caching and Parallel Decoding for Fast, Memory-Efficient Diffusion LLMs](2026-2609.26796-flash-dllm-io-aware-kv-caching-and-parallel-decoding-for-fast-memory-efficient-diffusion-llms.md)**  
  実装：[✓](https://github.com/VILA-Lab/Flash-dLLM) ・ リポジトリ内被引用：0  
  拡散言語モデルの鍵・値キャッシュ更新を融合注意へ統合し、同じモデルによる下書き・検証型並列復号を重ねることで、メモリ入出力と反復回数を同時に削減する。

- **2026-09 · [Fengshui: Demystifying Chiplet Ecosystem and Bespoke Neural Network Accelerator Codesign](2026-2609.10970-fengshui-chiplet-neural-accelerator-codesign.md)**  
  実装：[✓](https://github.com/CrucibleComputingGroup/fengshui) ・ リポジトリ内被引用：0  
  再利用可能な少数チップレット群そのものと演算子単位の専用アクセラレータ構成を共同探索し、計算データフロー・メモリ・並列方式・配置配線を演算子ごとに最適化してNREを抑えつつLLM推論のエネルギー効率を高める。

- **2026-09 · [FaultSense: Fault Localization in Large-Scale Mixture-of-Experts Model Serving Infrastructure](2026-a08c1f9c632d-faultsense-fault-localization-in-large-scale-mixture-of-experts-model-serving-infrastructure.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単一MoE層の選択可能プローブと二段階グループ検査で、特権監視なしにグレー障害GPU・通信経路をアプリ層から局所化し、診断プローブを約20倍削減する。

- **2026-09 · [ECOKV: Geometry-Aware KV Cache Eviction via Complementary Diversity Metrics](2026-2609.06663-ecokv-geometry-aware-kv-cache-eviction-via-complementary-diversity-metrics.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  コサイン類似度だけでは見落とすKV表現の大きさをユークリッド距離で補い、注意ヘッドごとの冗長度に応じて多様性と重要度を混合し、狭いKV予算で保持トークンを改善する方式。

- **2026-09 · [EAT: Expert Account Tracker for Efficient MoE Inference](2026-2609.33614-eat-expert-account-tracker-for-efficient-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は混合専門家モデル（Mixture-of-Experts、MoE）の推論時に、各トークンで何個の専門家ネットワークを実行するかを決める問題を扱う。固定個数選択（Top-K）では容易なトークンにも同じ数の専門家を割り当てる。

- **2026-09 · [Dynamic Semantic Compression for Efficient Latent-Space Inference in Large Language Models](2026-2609.15338-dynamic-semantic-compression-latent-space-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文を長さに応じて1〜3区間へ分割し、重要トークンを重み付けした潜在表現を生成・復号するDSEI。固定文圧縮より品質を改善し、トークン単位推論より系列長とメモリ負荷を削減する。

- **2026-09 · [Dissecting GPU Utilization for LLM Inference on Nvidia Hopper](2026-2609.12923-dissecting-gpu-utilization-llm-inference-hopper.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  H100上のLLM推論を8種類のNsight指標で分解し、デコードでは帯域待ちに加えGMMA m64固定断片の1.56～12.5%充填やwave損失が単一SM利用率に隠れることを示す。

- **2026-09 · [DeepSeek-V4-Flash on AMD gfx90a: Correctness Recovery and Inference Performance Engineering](2026-2609.15627-deepseek-v4-flash-on-amd-gfx90a-correctness-recovery-and-inference-performance-engineering.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MI250上のDeepSeek-V4-Flashで数値不具合を修復し、CDNA2向けカーネル・通信・事前充填最適化によりTP8復号をC64で1327.10トークン/秒まで実測した。

- **2026-09 · [D-Quant: Driftable Entropy Coding for KV Cache Quantization](2026-2609.19880-d-quant-driftable-entropy-coding-for-kv-cache-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  固定サイズ容器と長さ制約付きドリフトを組み合わせ、エントロピー符号化KVキャッシュを注意カーネル内で直接並列復号できる形にした低ビット量子化方式。

- **2026-09 · [CompKV: Compensation-Aware KV Selection for Long-Context LLM Inference](2026-2609.26300-compkv-compensation-aware-kv-selection-for-long-context-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  平均補償後に残る注意誤差を注意質量とブロック内得点分散の積で推定し、厳密に読む鍵・値ブロックを選ぶことで、長文脈の疎な注意計算の精度と中央処理装置退避効率を改善する。

- **2026-09 · [CEDAR: Error-Bounded Residual Routing for Efficient Long-Context Attention](2026-2609.07237-cedar-error-bounded-residual-routing-for-efficient-long-context-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  選外チャンクも要約経路で全域可視性を残し、鍵・値分散に基づく誤差上界で必要なチャンクだけ正確注意へ展開して、128Kで約3倍のカーネル高速化と品質回復を両立する疎注意方式。

- **2026-09 · [Breaking the 1.58-bit Barrier for Ternary LLMs](2026-2609.16338-breaking-the-1-58-bit-barrier-for-ternary-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  三値重みのゼロ偏りを利用するBITCOSで格納量を最小1.485ビット/重みまで下げ、専用CPU・Xe2復号で一要求デコードを最大1.27倍高速化する。

- **2026-09 · [BigMoMo: Efficient Inference of Large-Scale MoE with Speculative Decoding on Mobile Devices](2609.14643.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号の複数トークン窓でエキスパート再利用・フラッシュ連続読出し・NPU計算との移動重畳を行い、30B級MoEのスマホ推論を平均4.83倍高速化する。

- **2026-09 · [Beyond Scalar Sensitivity: Activation-Aware Mixed-Precision LLM Quantization with Cross-Layer Refinement](2026-2609.25916-beyond-scalar-sensitivity-activation-aware-mixed-precision-llm-quantizat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルを低メモリで推論するために重みを量子化する際、全ての行列へ同じビット幅を適用する必要はない。Llama-3-8Bで平均2.25ビット／重みの場合、既存のQ-PaletteのWikiText-2パープレキシティ47.20に対してCASAは22.41、6課題平均正解率34.0%に対して39.2%だった。

- **2026-09 · [AutoTuneBench: Trustworthy Measurement for Agent Auto-Tuning of LLM Serving Engines](2026-2609.18123-autotunebench-trustworthy-serving-engine-measurement.md)**  
  実装：[✓](https://github.com/li-ch/autotunebench) ・ リポジトリ内被引用：0  
  自動チューニングの測定規約を凍結コード・DB投入検証・不正隔離・事前登録比較・外部アンカーで強制し、エージェントが評価欠陥を最適化するのを防ぐ。

- **2026-09 · [Attention Routing Stabilizes Early: Working-Set Inference for Recurrent Language Models](2026-2609.27373-attention-routing-stabilizes-early-working-set-inference-for-recurrent-language-models.md)**  
  実装：[✓](https://github.com/tbn5pj/WISE_code) ・ リポジトリ内被引用：0  
  再帰型言語モデルは、同じネットワークブロックを何度も通して潜在表現を更新することで、固定パラメータ数のまま推論時計算量を増やせる。4K文脈では、後半20段の注意をネイティブFlashAttention比で1.758倍、探索段を含む32段の注意軌跡全体でも1.355倍高速化した。

- **2026-09 · [ASPIRE: Asynchronous Batched Self-Speculative Decoding for Long-Context LLM Inference](2026-2609.17943-aspire-asynchronous-batched-self-speculative-decoding.md)**  
  実装：[✓](https://github.com/Amir-zsh/ASPIRE) ・ リポジトリ内被引用：0  
  下書き・検証混在順伝播、要求別オンライン制御、下書き内の鍵値文脈更新により長文脈自己投機復号を最大4.58倍高速化する。

- **2026-08 · [TurboBus: Pooling PCIe Bandwidth for LLM Workloads via Scale-Up Fabrics](2026-2fe550669a96-turbobus-pooling-pcie-bandwidth-for-llm-workloads-via-scale-up-fabrics.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU間高速ファブリックを中継路として他GPUの空きPCIeリンクを借用し、モデル読込の初回トークン待ち時間を最大40%削減、鍵値退避推論を最大1.6倍高速化する。

- **2026-08 · [SSDi8: Accurate and Efficient 8-bit Quantization for State Space Duality](2026-2608.21952-ssdi8-accurate-and-efficient-8-bit-quantization-for-state-space-duality.md)**  
  実装：[✓](https://github.com/cau-hai-lab/SSDi8) ・ リポジトリ内被引用：0  
  Mamba-2の構造化状態空間双対の内部状態をINT8のまま受け渡すため、再帰計算の式を並べ替え、異なる軸の分布に合わせて量子化する方式を示す。

- **2026-08 · [SplitScaling: Adaptive Scaling for Disaggregated LLM Serving Against Traffic Bursts via DRL](2026-92b65c48d388-splitscaling-adaptive-scaling-for-disaggregated-llm-serving-against-traffic-bursts-via-drl.md)**  
  実装：[✓](https://github.com/Onlytonight/SplitScaling) ・ リポジトリ内被引用：0  
  プリフィル／デコード各プールを深層強化学習で独立伸縮し、新規ノードへ待機要求を即時再割当して、バースト負荷下でSLOを守りながら静的構成比25.2%の計算コストを削減する。

- **2026-08 · [RotaryQuant: Fitting 120B MoE Models on Consumer Hardware via Fused Compressed-Space Attention](2026-2608.08081-rotaryquant-fitting-120b-moe-models-on-consumer-hardware-via-fused-compressed-space-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み・3ビット鍵値キャッシュ・専門家退避を統合し、圧縮表現のまま注意計算して120B MoEを17.2GB、14.85トークン毎秒で実行する。

- **2026-08 · [ResiSpec：残差分布整形による複数候補投機サンプリング](2026-2608.24411-resispec-enhancing-multi-candidate-speculative-sampling-via-residual-distribution-shaping.md)**  
  実装：[✓](https://github.com/Czzzk/Resispec) ・ リポジトリ内被引用：0  
  複数候補方式は候補数を増やせば受理確率が上がるように見えるが、最初の候補が棄却されると対象分布からその候補確率を差し引いた残差分布へ移り、元のドラフト分布と急速にずれる。対象モデルの厳密な出力分布を変えず、既存の最先端複数候補方式に対して最大1.92倍の高速化を報告する。

- **2026-08 · [Performance Foundations of Parallel & Distributed Reasoning Language Models](2026-2608.27046-performance-foundations-of-parallel-distributed-reasoning-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RLM後学習を仕事量・深さ・メモリで形式化し、モデル内6種の並列化と配置・段階融合・非同期化を統一分類して、長い自己回帰生成が支配する分散RLの設計原理を整理する。

- **2026-08 · [OpRAG: A Resource-Deterministic Runtime for GPU-Backed Multi-Stage RAG Workflows](2026-2608.08340-oprag-resource-deterministic-rag-runtime.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RAG各段階を資源・通信付き演算子へ変換し、ゼロコピー通信とCPU/GPU重畳で復号外のオーケストレーション律速を削減する。

- **2026-08 · [MARCH: Scaling Recurrent Memory with Content-Routed State Anchors](2026-2608.12435-march-scaling-recurrent-memory-with-content-routed-state-anchors.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MARCHは、再帰型言語モデルの「過去を固定サイズの状態に圧縮するため、後から古い情報を取り出しにくい」という問題を、累積再帰状態の履歴保存と内容に基づく検索で緩和する構造である。過去状態の読出しには追加費用があり、128KではTop-4の疎ルーティングが密なMARCHの学習処理量を2倍超に改善する。

- **2026-08 · [M-LoRA: Efficient Serving for Concurrent LoRA Adapters with Memory-Aware Speculative Scheduler on Single GPU](2026-bbf40b71b5e2-m-lora-efficient-serving-for-concurrent-lora-adapters-with-memory-aware-speculative-scheduler-on-single-gpu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  要求ごとの生成長をモデル別LoRA予測器で見積もり、鍵値キャッシュとアダプタのピークメモリを同時制約する整数線形計画で、単一GPUの複数LoRA要求を高並行に割り当てるサービング方式。

- **2026-08 · [LLM4LLM: Bridging Kernel Benchmarks and Real Deployment via Closed-Loop Agentic Optimization](2026-2608.21836-llm4llm-bridging-kernel-benchmarks-and-real-deployment-via-closed-loop-agentic-optimization.md)**  
  実装：[✓](https://github.com/hzeng2000/LLM4LLM) ・ リポジトリ内被引用：0  
  実モデルを計測して段階別カーネルを探索し、モデル内検証まで閉ループ化してA100/H100で幾何平均3.91倍/6.98倍の端から端までの高速化を達成する。

- **2026-08 · [Learning how to Forget: Fine-tuning for Long-Context Sparse Attention](2026-2608.19920-learning-how-to-forget-fine-tuning-for-long-context-sparse-attention.md)**  
  実装：[✓](https://github.com/awslabs/keys_values) ・ リポジトリ内被引用：0  
  任意のKVキャッシュ方策を学習中に再現し、二重チェックポイントとKV差分符号化で推論級メモリの長文脈疎注意微調整を実現する。

- **2026-08 · [Launch-Bound and Substitutable: Why Three Inference Optimizations Fail to Pay Off in Mixture-of-Experts Models](2026-2608.26612-launch-bound-and-substitutable-moe-inference-optimizations.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoEの融合カーネル・4/8ビット量子化・グラフコンパイルを単体とE2Eで測定し、局所高速化が起動律速や品質へどう波及するかを分解して、置換可能な最適化の限界を明らかにする研究。

- **2026-08 · [Janus: Joint Prefill/Decode Disaggregation with KV-Cache-Aware Multi-Cloud Routing for Edge-Adjacent LLM Serving](2026-98d01325c44c-janus-joint-prefill-decode-disaggregation-with-kv-cache-aware-multi-cloud-routing-for-edge-adjacent-llm-serving.md)**  
  実装：[✓](https://github.com/arunakbofficial-tech/Janus) ・ リポジトリ内被引用：0  
  プリフィル/デコード配置とKV輸送方式を共同最適化し、異種マルチクラウドLLMサービングのTTFT・有効スループット・コストを同時改善する。

- **2026-08 · [HorizonServe: Coordinating Request Scheduling with GPU Sharing for Omni-Model Serving](2026-2608.01785-horizonserve-coordinating-request-scheduling-with-gpu-sharing-for-omni-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単一GPU上のオムニモデルで、締切余裕に基づく経路入場制御と帯域圧力に応じたSM配分を連携し、異種出力要求のSLO達成率を高めるサービング方式。

- **2026-08 · [H-Scale: Hessian-Guided Scale Refinement for NVFP4 Sub-Byte LLM Inference](2026-2608.28113-h-scale-hessian-guided-scale-refinement-for-nvfp4-sub-byte-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  H-Scaleは、NVIDIA Blackwell世代のGPUが直接扱える4ビット浮動小数点量子化形式（NVFP4）に対して、重みをどの4ビット値へ丸めるかではなく、16個の重みに共通して掛ける尺度をどう選ぶかに着目した学習後量子化（Post-学習 量子化; PTQ）の後処理である。

- **2026-08 · [FLINT: Efficiently Leveraging High Bandwidth Flash for Capacity-Scalable LLM Inference Acceleration](2026-2608.25062-flint-efficiently-leveraging-high-bandwidth-flash-for-capacity-scalable-llm-inference-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  高帯域フラッシュを巨大モデル重みの近接容量層として使い、動的読み出し結合・更新隔離・読み出し専用変換表で従来方式比六・二倍の復号処理量を実現する。

- **2026-08 · [FlashQuant：外れ値認識量子化の疎密融合GPU実行](2026-2608.15531-flashquant-sparse-dense-fusion-for-memory-efficient-outlier-aware-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  外れ値認識量子化では大半の重みを4ビットへ圧縮し、誤差を生みやすい少数の大振幅重みだけを高精度の疎行列として分離する。評価ではBF16のcuBLASに対して2.74〜4.18倍、最も強い非融合外れ値認識比較方式に対して最大1.53倍の高速化を報告する。

- **2026-08 · [FAMPWQ: Fisher Information-based Adaptive Mixed Precision Weight Quantization for Effective LLM Inference](2026-2608.24945-fampwq-fisher-information-based-adaptive-mixed-precision-weight-quantization-for-effective-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  実量子化ノイズでFisher情報の層別感度を測り、PPOで全体ビット予算を層へ配分して、3〜4bit域の品質劣化を一様量子化より抑える。

- **2026-08 · [EdgeXpert: An Edge Device for Memory-Efficient LLM Inference with Mixture-of-Experts and Speculative Decoding](2026-2608.05303-edgexpert-moe-speculative-decoding.md)**  
  実装：[✓](https://doi.org/10.5281/zenodo.21481269) ・ リポジトリ内被引用：0  
  MoEと投機的復号の併用で増える専門家外部メモリアクセスを、プリフィルの共有専門家再利用とデコードの深さ認識チャネル統合で直接削減するエッジ向け協調設計。

- **2026-08 · [Depth-adaptive Inference of Looped Language Models via Continuous Depth Batching](2026-2608.09444-depth-adaptive-inference-of-looped-language-models-via-continuous-depth-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  論文はCDBを端から端まで実装し、深度が不揃いになる鍵値キャッシュ（KV キャッシュ）、CPU側スケジューラとGPU側反復の同期、前段・後段をどの頻度で実行するかまで扱う。

- **2026-08 · [DeltaLog: Deferred Materialization of Recurrent States for Linear Attention Decoding](2026-2608.15533-deltalog-deferred-materialization-of-recurrent-states-for-linear-attention-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  線形注意の密な再帰状態を基底状態と有界な差分ログへ分解し、毎トークンの全状態書き戻しを周期的なマージへ遅延する。

- **2026-08 · [DASC: Decay-Aware State Compression for Hybrid Linear-Attention Serving](2026-2608.30386-dasc-decay-aware-state-compression-for-hybrid-linear-attention-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み由来の保持地平でKDA/GDN再帰状態を選別・ragged保存し、TP均衡化によりKimi-KDAで2.63倍のcheckpoint容量とTTFT 42.6%削減を実現する。

- **2026-08 · [Bounded-State Restoration: Decoupling Local Restore Capacity from External LLM State](2026-2608.17826-bounded-state-restoration-decoupling-local-restore-capacity-from-external-llm-state.md)**  
  実装：[✓](https://github.com/StarkLeeSunny/Flexkv-doublenode) ・ リポジトリ内被引用：0  
  外部KV状態の全ヒットを先に把握しつつ、復元はWチャンク窓だけを順次ステージングして解放することで、長大な外部状態とローカル復元メモリを分離する方式。

- **2026-08 · [Beyond Sparse Weights: When Is Attention Compressible?](2026-2608.21541-beyond-sparse-weights-when-is-attention-compressible.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  疎な注意マップだけではKV圧縮を正当化できないことを理論化し、値分散配分と末尾要約を厳密な物理予算で実装するCertKVを提案。

- **2026-08 · [AsymSpec: Efficient Cloud-Edge Speculative Decoding over Asymmetric Networks](2026-2608.04974-asymspec-efficient-cloud-edge-speculative-decoding-over-asymmetric-networks.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  非対称回線向けの証明付き段階補正と確認済み要求間パイプラインを組み合わせ、クラウド・エッジ投機的復号の通信待ちと無効先読みを削減する。

- **2026-08 · [ARCHead: Activation-Metric Residual Correction for Large Language Model Output Heads](2026-2608.02703-archead-activation-metric-residual-correction-for-large-language-model-output-heads.md)**  
  実装：[✓](https://github.com/suayptalha/archead) ・ リポジトリ内被引用：0  
  ARCHeadは、大規模言語モデル（LLM）の最終出力射影（language-modeling head; LM-head）に特化した学習後圧縮方式である。語彙数が大きいモデルでは、この例外だけで数百MBから1GB以上の重みを保持する。

- **2026-08 · [AFD-Ledger: Deployment Provisioning for Attention--FFN Disaggregation](2026-2608.04502-afd-ledger-deployment-provisioning-for-attention-ffn-disaggregation.md)**  
  実装：[✓](https://github.com/kvcache-ai/AFD-Ledger) ・ リポジトリ内被引用：0  
  AFDと同居配置を同一予算・TPOT SLOで独立最適化し、少数のハードウェア組だけを完全評価して最適配置を探索する分析プロビジョニング系。

- **2026-08 · [AdaMX：異質性を考慮した低ビット・マイクロスケーリング](2026-2608.03867-heterogeneity-aware-microscaling-for-efficient-low-bit-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  4ビットのMXFP4はブロック単位の共有尺度で低ビット推論を実現するが、すべてのブロックへ同じ要素形式と精度回復方式を適用するため、量子化しやすさの違いを十分に利用できない。3B〜70BモデルでMXFP4が失う精度のうち常識推論で83%、MMLUで82%を回復し、NVFP4に対してもそれぞれ43%、27%の損失を回復する。

- **2026-08 · [A Probabilistic Interpretation of KV Cache Eviction](2026-2608.28293-a-probabilistic-interpretation-of-kv-cache-eviction.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KV追放を期待値推定として定式化し、確率的追放＋復号時重要度補正で既存top-kのバイアスを抑えタスク間頑健性を高める。

- **2026-07 · [SelectInfer: Selective Neuron Loading and Computation for On-Device LLMs](2026-2607.18081-selectinfer-selective-neuron-loading-and-computation-for-on-device-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  オフラインで重要FFNニューロンを選別して必要分だけロードし、入力ごとの活性で計算対象も絞ることで、端末LLMのメモリ量と計算量を独立に調整する方式。

- **2026-07 · [LLMET: Enabling Cross-Layer Evaluation of Emerging M3D Memories for Energy-Efficient LLM Serving](2026-2607.26491-llmet-m3d-memory-energy-efficient-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMETは、LLMのタイル配置とメモリ階層転送を回路レベルのSRAM・M3D特性へ接続し、L2容量を増やす利益とアクセス費が釣り合う省エネ設計点を探索する。

- **2026-07 · [LaCache: Exact Caching and Precision-Adaptive Inference for Diffusion Large Language Models](2026-2607.16339-lacache-exact-caching-precision-adaptive-dllm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散型LLMの反復生成で不変なトークン状態とFlashAttention中間状態を無損失再利用し、第2層以降をFP8化して、既存の生成ステップ削減法と組み合わせ可能な推論高速化を実現する。

- **2026-07 · [I/o for LLM inference: a survey of storage and memory bottlenecks](2026-5e022a2789e7-i-o-for-llm-inference-a-survey-of-storage-and-memory-bottlenecks.md)**  
  実装：[✓](https://github.com/rch0wdhury/llm-io-profiler) ・ リポジトリ内被引用：0  
  LLMデコードのデータ移動を重み・KVキャッシュ・活性の三I/O流へ分解し、量子化からSSD/CXL/統合メモリまでをルーフライン上で統一して、最適化を積むと支配ボトルネックが移動することを定量化したサーベイ。

- **2026-07 · [From Expert Reduction to Behavioral Divergence: Tracing Numerical State through Sparse MoE Inference](2026-2607.28097-from-expert-reduction-to-behavioral-divergence-tracing-numerical-state-through-sparse-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  疎MoEの専門家加算順序だけで内部状態と生成文が分岐しうることを全順列・状態再構成で実証し、BF16項＋FP32累算を評価範囲の安定な互換契約として特定する。

- **2026-07 · [Enabling Spatially Fine-Grained DVFS in Neural Processing Units for Energy-Efficient LLM Serving](2026-2607.16473-enpu-component-level-dvfs-npu-llm-serving.md)**  
  実装：[✓](https://github.com/google-coral/coralnpu（ベースコア）。eNPUの改変実装・シミュレータの公開URLは一次資料に記載なし。) ・ リポジトリ内被引用：0  
  eNPUは、演算器・SRAM・HBM・接続を別電圧周波数領域に分け、非同期転送と演算子別計画をSLO余裕で切替えて、NPUサービングの非ボトルネック電力を落とす。

- **2026-07 · [DynaCalKV: Key-Value Cache Compression via Head Grouping and Adaptive Rank Allocation](2026-2607.24331-dynacalkv-key-value-cache-compression-via-head-grouping-and-adaptive-rank-allocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キー投影の注意ヘッドをCKA類似度で動的に群分けし、群ごとの情報量に応じて低ランク次元を配分することでReCalKVよりキー側パラメータを減らすが、GQAの長文脈では精度低下も確認する。

- **2026-07 · [CXL-CCL: Inter-Node Collective GPU-Communication Using a CXL Shared Memory Pool](2026-fab14a584908-cxl-ccl-inter-node-collective-gpu-communication-using-a-cxl-shared-memory-pool.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CXL共有メモリをノード間GPU集団通信の媒体として使い、データ配置・細粒度重畳・ドアベル同期でRDMA型通信に対する性能とコストを改善する。

- **2026-07 · [CTA-Pipelining: A Latency-Oriented Spatial Scaling Method for Multi-GPU Systems](2026-2607.07862-cta-pipelining-a-latency-oriented-spatial-scaling-method-for-multi-gpu-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CUTLASS、cuBLAS、NCCLを使いH200/B200最大8GPUで評価し、MLPを模した2層GEMMで最適化したマイクロバッチ方式より最大31.8%、テンソル並列（テンソル Parallelism; TP）より最大29.6%遅延を削減した。

- **2026-07 · [3DLS: A 3D Logic-Stacked Architecture for Disaggregated LLM Serving](2026-2607.01617-3dls-disaggregated-serving-interconnect.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル→デコードのKV転送とデコード側テンソル並列AllReduceを同じ横方向リンクで競合させず、KVだけを3D縦リンクへ物理分離するチップレット構成。等帯域条件でも最大1.49倍のスループットと60.2%の遅延削減を示す。

- **2026-06 · [Unified KV Pooling to Accelerate Long-Context LLM Serving](2026-2606.14779-unified-kv-pooling-to-accelerate-long-context-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数RAM/SSDを帯域幅比例の単一KVプールとして並列利用し、SPDK直アクセスでファイルシステムを迂回して長文脈KV再取得を高速化する。

- **2026-06 · [SMEPilot: Characterizing and Optimizing LLM Inference with Scalable Matrix Extensions](2026-2606.16332-smepilot-characterizing-and-optimizing-llm-inference-with-scalable-matrix-extensions.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CPU内のSMEと通常コアを共有帯域込みのルーフラインで使い分け、タイル分割・注意パイプライン・配置再利用によりLLM推論をllama.cpp比最大3.94倍高速化する。

- **2026-06 · [Omni-Flow: A Unified Workflow Orchestration and Distributed KV Cache Sharing Framework for Multimodal Inference](2026-2606.31093-omni-flow-a-unified-workflow-orchestration-and-distributed-kv-cache-sharing-framework-for-multimodal-inference.md)**  
  実装：[✓](https://github.com/meituan-longcat/omni-flow) ・ リポジトリ内被引用：0  
  マルチモーダル推論を制御・データ・計算の3層へ分離し、Python DSL、GPU/CPU/SSD分散KV、SGLang互換実行を統合する。LongCat-NextやHunyuanImage-3を同じ配信抽象へ載せる基盤。

- **2026-06 · [LiveServe: Interaction-Aware Serving for Real-Time Omni-Modal LLMs](2026-2606.22983-liveserve-interaction-aware-serving-for-real-time-omni-modal-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  音声対話の再生進捗・発話・割込みをスケジューリングとKV配置へ反映し、不要な先行生成を抑えながら次ターンのKVを発話中に先読みし、P90初回音声遅延と無駄計算を同時に減らす。

- **2026-06 · [Less is MoE: Trimming Experts in Domain-Specialist Language Models](2026-2606.05538-less-is-moe-trimming-experts-in-domain-specialist-language-models.md)**  
  実装：[✓](https://github.com/HectorHHZ/Less-is-MoE) ・ リポジトリ内被引用：0  
  Less is MoEは、混合専門家モデル（Mixture of エキスパート、MoE）を圧縮する際に専門家を丸ごと削ると、一般常識の選択式問題では性能が残っても数学推論やコード生成が崩壊する原因を分析し、専門家内部の順伝播ネットワーク（FFN）中間次元を削るFisher-MoEを提案する研究である。

- **2026-06 · [High-accuracy Low-Bit KV-Cache Quantization via Local Distribution Restoration](2026-2607.16248-high-accuracy-low-bit-kv-cache-quantization-via-local-distribution-restoration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  1ビットKVキャッシュを維持したまま、量子化で崩れた高確率候補の局所順位だけを検出・補正し、RULER精度を47.8%から83.2%へ回復するDGAP。

- **2026-06 · [HERALD: High-Throughput Block Diffusion LLM Serving via CPU-GPU Cooperative KV Cache Retrieval](2026-2606.21633-herald-high-throughput-block-diffusion-llm-serving-via-cpu-gpu-cooperative-kv-cache-retrieval.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ブロック拡散LLMのKV再利用性を利用し、CPUで1回選択した疎KVをGPUへ先読みしてデノイズと重畳し、5% KV予算で最大2.28倍の処理量を実現する。

- **2026-06 · [Execution-State Capsules: Graph-Bound Execution-State Checkpoint and Restore for Low-Latency, Small-Batch, On-Device Physical-AI Serving](2026-2606.20537-execution-state-capsules-graph-bound-execution-state-checkpoint-and-restore-for-low-latency-small-batch-on-device-physic.md)**  
  実装：[✓](https://github.com/flashrt-project/FlashRT) ・ リポジトリ内被引用：0  
  KVだけでなく再帰・畳み込み・複数トークン予測状態を丸ごと保存復元し、単一ストリーム再入場の初回応答を最大26.94倍高速化する実行状態カプセル。

- **2026-06 · [Dustin: Draft-Augmented Sparse Verification for Efficient Long-Context Generation with Speculative Decoding](2026-2606.24957-dustin-draft-augmented-sparse-verification-for-efficient-long-context-generation-with-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  対象側の過去注意とドラフト側の先読み注意を融合し、少数の意味検索ヘッドだけで検証用KVを選ぶことで、長文投機的デコードのKV読込を削減する。

- **2026-06 · [Characterizing Software Aging in GPU-Based LLM Serving Systems](2026-2606.11916-characterizing-software-aging-in-gpu-based-llm-serving-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  6種類のGPU LLMサービング構成を計216時間連続運転し、全構成でホスト側のメモリ経年劣化を検出。リーク率はvLLM V1単体+1.8KB/時からTriton+V0の+157KB/時まで大差があり、配置・ランタイム選択が長期信頼性を左右することを示す。

- **2026-06 · [BatchGen: An Architecture for Scalable and Efficient Batch Inference](2026-2606.21712-batchgen-an-architecture-for-scalable-and-efficient-batch-inference.md)**  
  実装：[✓](https://github.com/batchgen-project/batchgen) ・ リポジトリ内被引用：0  
  系列をイベント駆動コルーチン化して停止・結合・分割・移動を可能にし、MoEバッチ形成と長尾負荷分散を動的化して最大2.3倍の大規模高速化を示す。

- **2026-06 · [Attribution-Guided and Coverage-Maximized Pruning for Structural MoE Compression](2026-2606.18304-attribution-guided-and-coverage-maximized-pruning-for-structural-moe-com.md)**  
  実装：[✓](https://github.com/yifu-ding/MoE-Slimming) ・ リポジトリ内被引用：0  
  専門家を丸ごと削除する従来方式では、重要度が高いと判定された専門家の内部にも残る冗長チャネルを見逃し、逆に頻度の低い専門家を全削除すると一部の入力に必要な能力を失う。著者らはDeepSeekとQwenの複数の混合専門家モデルを対象に、構造的枝刈り（structural 枝刈り）50%単独と、25%枝刈りに4ビット量子化を重ねた構成を比較した。

- **2026-06 · [Above the Inner Loop: Exceeding Accelerate at LLM Prefill GEMM on the M1 AMX](2026-2606.25426-above-the-inner-loop-exceeding-accelerate-at-llm-prefill-gemm-on-the-m1-amx.md)**  
  実装：[✓](https://github.com/dbhan08/inferc) ・ リポジトリ内被引用：0  
  M1 AMXの内側ループがロード発行律速であることを切り分け、細粒度パネルで第2 AMXブロックを使い、重み事前パッキングを併用してllama.cppの128トークンfp32プリフィルを1.44倍高速化する。

- **2026-05 · [SpecSA: Bridging Speculative Decoding and Sparse Attention for Efficient LLM Inference](2026-2605.19893-specsa-sparse-speculative-verification.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的検証クエリが選ぶ重複KVブロックを一度だけ読み、厳密共有と近似共有、層間索引再利用、融合カーネルを比較して、長文脈の疎注意読出しを減らすシステム。

- **2026-05 · [Self-Orchestrating Language Models: Leveraging Semantic Dependence for Efficient Inference](2026-2609.14850-self-orchestrating-language-models-leveraging-semantic-dependence-for-ef.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  意味的に独立する文章断片や推論段階をモデルに印付けさせ、ランタイムが並列デコード、不要なKVページの解放、または拡散生成の並列順序に利用する三方式を示すMIT博士論文。各方式は別個に評価され、速度向上は課題・設定によって品質との交換条件がある。

- **2026-05 · [Lodestar：オンライン学習によるLLM推論リクエストルータ](2026-2606.00946-lodestar-an-online-learning-llm-inference-router.md)**  
  実装：[✓](https://github.com/gangmuk/Lodestar) ・ リポジトリ内被引用：0  
  公開クラウドの同種8基A30クラスタと、A30 8基＋V100 8基の異種クラスタで評価し、強い接頭辞・負荷認識ヒューリスティックに対して平均TTFTを平均1.41倍、P99 TTFTを1.47倍改善し、条件によって異種クラスタでは4倍超の改善を示す。

- **2026-05 · [Llamas on the Web: Memory-Efficient, Performance-Portable, and Multi-Precision LLM Inference with WebGPU](2026-2605.20706-llamaweb.md)**  
  実装：[✓](https://github.com/ggml-org/llama.cpp) ・ リポジトリ内被引用：0  
  LlamaWebは静的メモリ計画、端末適応型WebGPUカーネル、量子化対応をllama.cppへ統合し、ブラウザ推論のメモリ消費とデコード性能を改善する。

- **2026-05 · [Efficient MoE Inference on Single Consumer-grade GPU with Dynamic Expert Caching](2020-2026.00101-efficient-moe-inference-on-single-consumer-grade-gpu-with-dynamic-expert-caching.md)**  
  実装：[✓](https://github.com/rzhang772/SMOE) ・ リポジトリ内被引用：0  
  プリフィルの動的エキスパート配置とデコードのトークン-wise予測取得を組み合わせ、単一RTX 4090で671B級MoEを高速化するCPU/GPUハイブリッド基盤。

- **2026-05 · [Bandwidth-Aware LLM Inference on Heterogeneous Many-Core Supercomputers](2026-2605.25655-bandwidth-aware-llm-inference-on-heterogeneous-many-core-supercomputers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低帯域・分散オンチップ記憶のMT-3000向けに演算子、融合注意、三段パイプライン、混合並列を共同設計し、大規模LLM推論を実現。

- **2026-04 · [Unlocking the Edge deployment and ondevice acceleration of multi-LoRA enabled one-for-all foundational LLM](2026-2604.18655-ondevice-multilora-runtime.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  実行時LoRA入力・NPU向け最適化・並行生成・自己投機的復号を統合し、Galaxy S24/S25で多用途LLMを単一グラフ展開する。

- **2026-04 · [SpecFed: Accelerating Federated LLM Inference with Speculative Decoding and Compressed Transmission](2026-2604.25777-specfed-accelerating-federated-llm-inference-with-speculative-decoding-and-compressed-transmission.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  連合LLM投機的復号で上位K確率だけを送信し、2種の確率再構成と誤差上界により通信量を削減する方式。

- **2026-04 · [Serving Chain-structured Jobs with Large Memory Footprints with Application to Large Foundation Model Serving](2026-2604.14993-serving-chain-structured-jobs-with-large-memory-footprints-with-application-to-large-foundation-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分散パイプライン型の大規模言語モデル推論を、モデルブロック配置、鍵値キャッシュ容量配分、オンライン負荷分散からなるサーバ鎖構成問題として定式化し、実サービング評価で平均応答時間を六十三から七十七パーセント削減する。

- **2026-04 · [KV Cache Offloading for Context-Intensive Tasks](2026-2604.08426-kv-cache-offloading-for-context-intensive-tasks.md)**  
  実装：[✓](https://github.com/yandex-research/context-intensive-kv-offloading) ・ リポジトリ内被引用：0  
  文脈集約型課題でKV退避の選択誤差を分析し、低ビット量子化によるYAKVで精度とスループットを改善する。

- **2026-04 · [Fleet: Hierarchical Task-based Abstraction for Megakernels on Multi-Die GPUs](2026-2604.15379-fleet-multi-die-gpu-megakernel.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Fleetは複数ダイGPUにチップレット単位の作業階層を追加し、永続カーネル内で同一L2を共有するCUを協調スケジュールしてLLMデコードの重み再利用と同期局所性を高める。

- **2026-04 · [ELMoE-3D: Leveraging Intrinsic Elasticity of MoE for Hybrid-Bonding-Enabled Self-Speculative Decoding in On-Premises Serving](2026-2604.14626-elmoe-3d-hybrid-bonding-self-speculative-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HBメモリ上の頻出エキスパート上位ビットをキャッシュ兼自己ドラフトとして使い、MoEの投機的デコードと重み転送を一体最適化する3D積層HW-SW協調方式。

- **2026-03 · [The Missing Memory Hierarchy: Demand Paging for LLM Context Windows](2026-2603.09023-pichay-demand-paging-context-windows.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント文脈を仮想メモリとしてページングし、古いツール結果を追い出して再参照時に復元する透明プロキシ。139万追い出しで0.0254%フォルト率を報告。

- **2026-03 · [Serving Hybrid LLM Loads with SLO Guarantees Using CPU-GPU Attention Piggybacking](2026-2603.12831-serving-hybrid-llm-loads-with-slo-guarantees-using-cpu-gpu-attention-piggybacking.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CPUへ逃がした低優先度要求の注意計算を非同期化し、後続GPU密計算へ層単位で相乗りさせることで、SLOを守りながら低優先度スループットを最大9.85倍にする。

- **2026-02 · [Two-Stage Expert Offloading for Domain-Aware MoE Inference](2026-dacc3922b5b4-two-stage-expert-offloading-for-domain-aware-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  領域別プリフィル事前読込と時間・層間・領域局所性によるデコード先読みを組み合わせ、MoEのCPU退避でI/O待ち50%削減、投影TPOT 3.45倍高速化、全常駐比33%メモリ削減を狙う。

- **2026-02 · [StreamServe: Adaptive Speculative Flows for Low-Latency Disaggregated LLM Serving](2026-2604.09562-streamserve-adaptive-speculative-flows-for-low-latency-disaggregated-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分離型プリフィル・デコード上で、複数指標による要求ルーティングと実行時適応する投機深度を閉ループ連携し、4×A800評価でテンソル並列vLLM比の平均レイテンシ15.75倍短縮・平均スループット4.4倍を報告する。

- **2026-02 · [ReviveMoE: Fast Recovery for Hardware Failures in Large-Scale MoE LLM Inference Deployments](2026-2602.21140-revivemoe-fast-hardware-failure-recovery.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単一NPU障害時にサービング全体を再起動せず、要求状態・KVブロック表・MoE重み・通信領域・実行グラフを局所修復して大規模MoE推論を高速復旧する。

- **2026-01 · [RadixMLP -- Intra-batch Deduplication for Causal Transformers](2026-2601.15013-radixmlp-intra-batch-deduplication.md)**  
  実装：[✓](https://github.com/michaelfeil/radix-mlp) ・ リポジトリ内被引用：0  
  RadixMLPは、同一バッチに入った複数の系列が長い接頭辞を共有している場合、共有部分の多層パーセプトロン（MLP）、層正規化（LayerNorm）、線形射影、埋め込みなどを何度も実行する無駄を削減する方式である。

- **2026-01 · [PLA-Serve: A Prefill-Length-Aware LLM Serving System](2026-a30e37ff7d4b-pla-serve-a-prefill-length-aware-llm-serving-system.md)**  
  実装：[✓](https://github.com/Jianshu-She/LAPS) ・ リポジトリ内被引用：0  
  プリフィル長で短要求と長要求を別キュー・別実行モードへ分離し、待機窓、CUDA Graph形状クラスタリング、動的GPU割当で短要求の待ちと長要求の干渉を同時に抑える。

- **2026-01 · [LOOKAT: Lookup-Optimized Key-Attention for Memory-Efficient Transformers](2026-2601.10155-lookat-lookup-optimized-key-attention-for-memory-efficient-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LOOKATは、自己回帰Transformerの注意得点計算を、ベクトル検索における内積類似度検索として扱い、キーを圧縮したまま注意得点を計算する方式である。GPT-2の第1注意層で、64次元のキーを2個の1バイト符号へ圧縮すると、キー表現は128バイトから2バイトへ減り、キー単体の表現上の圧縮率は64倍となる。

- **2026-01 · [LLM KV Cache Storage Using CXL Memory](2026-4885970e907b-llm-kv-cache-storage-using-cxl-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  vLLMとLMCacheのKVキャッシュを4種類のCXLメモリへ退避して実機比較し、DRAM型・プール型CXLが長文脈でシステムDRAMに近い性能を保ち、122K入力でGPU VRAM比約9倍の要求スループットを示す。

- **2025-12 · [MatKV: Trading Compute for Flash Storage in LLM Inference](2025-2512.22195-matkv-trading-compute-for-flash-storage-in-llm-inference.md)**  
  実装：[✓](https://github.com/kunwooshin/MatKV) ・ リポジトリ内被引用：0  
  検索拡張生成（retrieval-augmented generation; RAG）では、検索された長い文書を要求ごとに大規模言語モデルへ再入力し、同じ文書のキー・値キャッシュ（KV キャッシュ）を何度も計算する。この方式は通常の接頭辞キャッシュ（prefix キャッシュ）とは性質が異なる。

- **2025-12 · [CHIME: Chiplet-based Heterogeneous Near-Memory Acceleration for Edge Multimodal LLM Inference](2026-2601.19908-chime-chiplet-near-memory-mllm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚入力で膨らむKVキャッシュと演算重みをDRAM・RRAMへ役割分担し、近メモリ実行と局所性を保つ演算融合で端末MLLM推論のデータ移動を抑える設計を示す。

- **2025-11 · [T-SAR: A Full-Stack Co-design for CPU-Only Ternary LLM Inference via In-Place SIMD ALU Reorganization](2025-2511.13676-t-sar-a-full-stack-co-design-for-cpu-only-ternary-llm-inference-via-in-p.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  T-SARは、重みを−1、0、+1の三値に制約した大規模言語モデル（LLM）を、専用の大きな行列演算器なしにCPUで高速実行するための、アルゴリズム・命令セット・マイクロアーキテクチャ・ソフトウェアの協調設計である。

- **2025-11 · [Scaling Graph Chain-of-Thought Reasoning: A Multi-Agent Framework with Efficient LLM Serving](2025-2511.01633-graph-cot-multi-agent-efficient-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Graph-CoTを分類・推論・行動・検索へ分業し、頂点単位KV再利用、優先度追い出し、検索と生成の重畳を組み合わせ、遅延最大90.3%減・スループット最大15.1倍を報告。

- **2025-11 · [Revisiting Disaggregated Large Language Model Serving for Performance and Energy Implications](2026-2601.08833-revisiting-disaggregated-large-language-model-serving-for-performance-and-energy-implications.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  公平な2-GPU基準と複数KV転送階層・DVFSでプリフィル/デコード分離を再評価し、性能・省電力の優位が条件依存であることを示す。

- **2025-11 · [GoCkpt: Gradient-Assisted Multi-Step overlapped Checkpointing for Efficient LLM Training](2025-2511.07035-gockpt-gradient-assisted-multi-step-overlapped-checkpointing-for-efficient-llm-training.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  チェックポイント転送を複数学習ステップへ分散し、低精度勾配でCPU側の版を一貫状態へ再構築することで、GPU停止を大幅に隠して学習スループットを最大約40%改善する。

### 2年前（2024-11〜2025-10）

- **2025-01 · [FlashInfer: Efficient and Customizable Attention Engine for LLM Inference Serving](2025-2501.01005-flashinfer-attention-engine-serving.md)**  
  実装：[✓](https://github.com/flashinfer-ai/flashinfer) ・ リポジトリ内被引用：98  
  多様なKV配置と注意派生形をブロック疎形式と実行時コンパイルで統一し、可変系列長を固定CTAへ動的に負荷均衡しながらCUDAグラフ互換性も保つ、LLMサービング向け高性能注意エンジン。

- **2024-12 · [Gated Delta Networks: Improving Mamba2 with Delta Rule](2024-2412.06464-gated-delta-networks-improving-mamba2-with-delta-rule.md)**  
  実装：[✓](https://github.com/NVlabs/GatedDeltaNet) ・ リポジトリ内被引用：25  
  本論文は、長文脈を固定容量の状態へ圧縮する線形再帰言語モデルが、記憶の保持と更新を両立しにくい問題を扱う。

- **2025-08 · [Dream 7B: Diffusion Large Language Models](2025-2508.15487-dream-7b-diffusion-large-language-models.md)**  
  実装：[✓](https://github.com/DreamLM/Dream) ・ リポジトリ内被引用：23  
  自己回帰モデルから初期化した70億拡散言語モデルで、系列全体の反復復元により計画課題と任意順生成を強化し、推論反復数で品質と速度を調整する。

- **2025-04 · [SpinQuant: LLM quantization with learned rotations](2025-2405.16406-spinquant-llm-quantization-with-learned-rotations.md)**  
  実装：[✓](https://github.com/facebookresearch/SpinQuant) ・ リポジトリ内被引用：23  
  外れ値が低ビット量子化の誤差を大きくする問題に対して、全精度の機能を保つ旋回行列を学習し、重み・活性値・KVキャッシュの量子化に合わせる。

- **2025-03 · [Block Diffusion: Interpolating Between Autoregressive and Diffusion Language Models](2025-2503.09573-block-diffusion-interpolating-between-autoregressive-and-diffusion-langu.md)**  
  実装：[✓](https://github.com/kuleshov-group/bd3lms) ・ リポジトリ内被引用：20  
  マスク率をデータに応じて区間制限する学習方式と、清浄系列・雑音系列を特殊注意で同時処理する実装を導入した。

- **2024-11 · [BatchLLM: Optimizing Large Batched LLM Inference with Global Prefix Sharing and Throughput-oriented Token Batching](2024-2412.03594-batchllm-optimizing-large-batched-llm-inference-with-global-prefix-shari.md)**  
  実装：[✓](https://github.com/microsoft/MixLLM/tree/batchllm_vllm_064) ・ リポジトリ内被引用：18  
  BatchLLMは、検索結果の説明文生成、広告文書の変換、推薦候補の採点など、数千件以上のプロンプトをまとめて処理する大規模言語モデル（LLM）の一括推論を対象とするシステムである。原著のMLSys 2026産業部門版は、NVIDIA A100とAMD MI200上で、vLLMやSGLangに対して1.3～10.8倍の端点処理率改善を報告する。

- **2025-04 · [JITServe: SLO-aware LLM Serving with Imprecise Request Information](2025-2504.20068-jitserve-slo-aware-llm-serving-with-imprecise-request-information.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  不確かな出力長と依存関係を逐次更新し、期限達成に必要な最小帯域で要求を選ぶことで、サービス有効処理量を1.4〜6.3倍へ改善する。

- **2025-02 · [Comet: Fine-grained Computation-communication Overlapping for Mixture-of-Experts](2025-2502.19811-comet-fine-grained-computation-communication-overlapping-for-mixture-of-experts.md)**  
  実装：[✓](https://github.com/bytedance/flux) ・ リポジトリ内被引用：15  
  Cometは、混合専門家モデル（Mixture-of-Experts; MoE）の専門家を複数GPUへ分散配置したときに生じる通信待ちを、専門家の行列計算と重ねて隠すための実行系である。著者らは8基のH800および8基のL20からなるGPU環境で、Mixtral-8×7B、Qwen2-MoE、Phi-3.5-MoEなどを評価した。

- **2025-09 · [Fast-dLLM v2: Efficient Block-Diffusion LLM](2025-2509.26328-fast-dllm-v2-block-diffusion-hierarchical-cache.md)**  
  実装：[✓](https://github.com/NVlabs/Fast-dLLM/tree/main/v2) ・ リポジトリ内被引用：12  
  自己回帰モデルをブロック拡散へ少量追加学習し、ブロック間KVキャッシュとブロック内DualCache、信頼度並列復号を階層化して品質を保ちながら生成を高速化する。

- **2025-10 · [Pie: A Programmable Serving System for Emerging LLM Applications](2025-2510.24051-pie-a-programmable-serving-system-for-emerging-llm-applications.md)**  
  実装：[✓](https://github.com/pie-project/pie) ・ リポジトリ内被引用：8  
  生成ループを細粒度APIへ分解し、Wasm inferletがKV・復号・入出力を直接制御しつつ適応一括処理でGPU効率を維持するプログラマブルLLMサービング基盤。

- **2025-05 · [FlashDLM: Accelerating Diffusion Language Model Inference via Efficient KV Caching and Guided Diffusion](2025-2505.21467-flashdlm-accelerating-diffusion-language-model-inference.md)**  
  実装：[✓](https://github.com/ZhanqiuHu/flash-dlm-experimental) ・ リポジトリ内被引用：8  
  FlashDLMは拡散言語モデル（Diffusion Language モデル; DLM）の遅さを、1回のノイズ除去で再計算し過ぎる問題と、何回ノイズ除去を繰り返すかという問題に分ける。FreeCacheは前者を、Guided Diffusionは後者を削り、二つを組み合わせて大きな端末間高速化を得る。

- **2025-04 · [KeyDiff: Key Similarity-Based KV Cache Eviction for Long-Context LLM Inference in Resource-Constrained Environments](2025-2504.15364-keydiff-key-similarity-based-kv-cache-eviction-for-long-context-llm-inference-in-resource-constrained-environments.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  注意重みではなくキーの幾何学的多様性を重要度代理として使う学習不要KV削除法で、ブロック長文処理でも厳密な容量上限を守りつつ、8K予算で約23%削減・LongBench差0.04%以下、既存削除法比で遅延最大30%短縮を示す。

- **2025-04 · [OmniKV: Dynamic Context Selection for Efficient Long-Context LLMs](2025-6264cfc484ad-omnikv-dynamic-context-selection-for-efficient-long-context-llms.md)**  
  実装：[✓](https://github.com/antgroup/OmniKV) ・ リポジトリ内被引用：7  
  OmniKVは、長文脈の大規模言語モデルで、鍵・値キャッシュ（KVキャッシュ）をGPUにすべて置くと容量不足になる一方、CPUに退避した全量を各層で読み直すと転送が律速になる問題を扱う。単一A100 80GB、128K文脈で退避なしの復号は毎秒21.0トークン、完全注意比1.68倍である。

- **2025-02 · [Cache-Craft: Managing Chunk-Caches for Efficient Retrieval-Augmented Generation](2025-2502.15734-cache-craft-managing-chunk-caches-for-efficient-retrieval-augmented-gene.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  文書自体が同じなのに、GPUはその文書の鍵・値（KV）を再計算することになる。Cache-Craftは再利用するかどうかの判定と、どれだけ再計算して修復するかの決定を分離する。実際のRAGワークロードでは、接頭辞キャッシュ比で冗長計算を51%減らし、連続バッチ下で処理率を1.6倍、エンドツーエンド応答遅延を約半分にしたと報告する。

- **2025-10 · [dInfer: An Efficient Inference Framework for Diffusion Language Models](2025-2510.08666-dinfer-an-efficient-inference-framework-for-diffusion-language-models.md)**  
  実装：[✓](https://github.com/inclusionAI/dInfer) ・ リポジトリ内被引用：6  
  拡散型LLM（dLLM）の反復的な雑音除去（denoising）・並列トークン確定・更新され続けるKVをモジュール化し、デコーダ/KV管理とGPU実行系を同時最適化するdInfer。

- **2025-06 · [Accelerating Diffusion Large Language Models with SlowFast Sampling: The Three Golden Principles](2025-2506.10848-accelerating-diffusion-large-language-models-with-slowfast-sampling-the-three-golden-principles.md)**  
  実装：[✓](https://github.com/LiangrunFlora/Slow-Fast-Sampling) ・ リポジトリ内被引用：6  
  単独の信頼度閾値だけではなく、連続区間の終端が最近の複数反復で安定したかを検査し、探索段階（Slow）から高速段階（Fast）へ切り替える。原著図2のGPQA・8-shot・生成長1024という特定条件では、LLaDAの通常復号が1.60トークン/秒、SlowFast単独が25.00トークン/秒で15.63倍となる。

- **2025-05 · [TokenWeave: Efficient Compute-Communication Overlap for Distributed LLM Inference](2025-2505.11329-tokenweave-efficient-compute-communication-overlap-for-distributed-llm-inference.md)**  
  実装：[✓](https://github.com/microsoft/tokenweave) ・ リポジトリ内被引用：6  
  GPU実行波を考慮した2分割とAllReduce–RMSNorm融合により、小さなテンソル並列バッチでも通信と計算を重ね、遅延とスループットを改善する。

- **2024-11 · [Context Parallelism for Scalable Million-Token Inference](2024-2411.01783-context-parallelism-for-scalable-million-token-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  本研究は、巨大な言語モデルの推論において、長い入力を処理する最初の一回の待ち時間を短縮する文脈並列（context parallelism）の実装を扱う。提案の中心は、リング状の通信で鍵・値を巡回させるpass-KVと、逆に問い合わせを巡回させるpass-Qを、推論段階と既存キャッシュの割合に応じて切り替えることである。

- **2025-05 · [ELIS: Efficient LLM Iterative Scheduling System with Response Length Predictor](2025-2505.09142-elis-efficient-llm-iterative-scheduling-system-with-response-length-predictor.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  応答長を50トークンごとに再予測して短い残作業を優先し、LLM servingの先頭待ちを減らすKubernetes/vLLMスケジューラ。

- **2025-03 · [MoE-Gen: High-Throughput MoE Inference on a Single GPU with Module-Based Batching](2025-2503.09716-moe-gen-module-based-batching.md)**  
  実装：[✓](https://github.com/EfficientMoE/MoE-Gen) ・ リポジトリ内被引用：4  
  MoEの注意機構とエキスパートを別々にバッチ化し、ホストメモリでトークンを蓄積して大バッチ化することで、単一GPUオフロード推論のGPU利用率とスループットを改善する。

- **2025-03 · [A Novel Hat-Shaped Device-Cloud Collaborative Inference Framework for Large Language Models](2025-2503.18989-a-novel-hat-shaped-device-cloud-collaborative-inference-framework-for-la.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  HATは、端末で利用する大規模言語モデルの応答速度と、入力・出力トークンをクラウドへ直接送らない配置を両立するための協調推論方式である。論文全体では比較方式に対して初回応答遅延41～54%、トークン間遅延41～77%の削減を報告する。

- **2025-02 · [TeleRAG: Efficient Retrieval-Augmented Generation Inference with Lookahead Retrieval](2025-2502.20969-telerag-efficient-retrieval-augmented-generation-inference-with-lookahead-retrieval.md)**  
  実装：[✓](https://github.com/uw-syfi/TeleRAG) ・ リポジトリ内被引用：4  
  RAGの前段生成から次のIVF検索クラスタを予測し、LLM生成とCPU→GPU先読みを重ねつつ外れクラスタをCPU検索で補完して、大規模索引をGPU常駐せず検索待ちを隠す。

- **2024-12 · [Multi-Bin Batching for Increasing LLM Inference Throughput](2024-2412.04504-multi-bin-batching-for-increasing-llm-inference-throughput.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  複数ビン バッチ化は、固定バッチ（静的バッチ化）で生成長の異なるリクエストを同じバッチへ入れたとき、短いリクエストが終了しても最長リクエストが終わるまで計算unitが解放されない遅延処理損失を、出力長に応じた事前分類で減らすスケジューラである。

- **2024-11 · [FFN-SkipLLM: A Hidden Gem for Autoregressive Decoding with Adaptive Feed Forward Skipping](2024-2404.03865-ffn-skipllm-a-hidden-gem-for-autoregressive-decoding-with-adaptive-feed-.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  将来トークンが参照するキャッシュに穴が生じるため、過去状態をコピーしたり鍵・値を再計算したりする追加対策が必要となる。提案法は各層の自己注意を維持し、FFNに入る状態とFFN残差更新後の状態のコサイン類似度（cosine similarity）から、中間層の冗長なFFNを検出する。

- **2025-08 · [Diffusion LLMs Can Do Faster-Than-AR Inference via Discrete Diffusion Forcing](2025-2508.09192-diffusion-llms-can-do-faster-than-ar-inference-via-discrete-diffusion-fo.md)**  
  実装：[✓](https://github.com/zhijie-group/Discrete-Diffusion-Forcing) ・ リポジトリ内被引用：3  
  離散拡散型の大規模言語モデル（diffusion LLM、dLLM）は、マスクされた複数トークンを一度の推論で同時に予測できる。しかし従来の双方向注意を使う拡散モデルでは、マスクの状態が反復ごとに変わるため、過去の鍵・値（KV）を自己回帰型モデルのように正確にキャッシュしにくい。確定済みのブロックのKVは変更されないため正確に再利用できる。

- **2025-06 · [TD-Pipe: Temporally-Disaggregated Pipeline Parallelism Architecture for High-Throughput LLM Inference](2025-2506.10470-td-pipe-temporally-disaggregated-pipeline-parallelism-architecture-for-h.md)**  
  実装：[✓](https://github.com/MLSysU/TD-Pipe) ・ リポジトリ内被引用：3  
  PCIeのみで接続されたGPUのパイプライン並列推論において、プリフィルとデコードを時間分離し、予測型KVメモリ管理と負荷移送で遊休時間を削減する。

- **2025-06 · [SwiftSpec: Ultra-Low Latency LLM Decoding by Scaling Asynchronous Speculative Decoding](2025-2506.11309-swiftspec-asynchronous-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  ドラフトGPU群と対象GPU群を分離して候補木生成と検証を同時実行し、検証済み接頭辞と未検証枝のKVを分けて再利用し、低バッチの同期・起動待ちを減らす投機的デコード。

- **2025-06 · [MNN-LLM: A Generic Inference Engine for Fast Large Language Model Deployment on Mobile Devices](2025-2506.10443-mnn-llm-mobile-inference-engine.md)**  
  実装：[✓](https://github.com/alibaba/MNN) ・ リポジトリ内被引用：3  
  DRAMとFlashの階層利用、役割別量子化、CPU/GPU別データ配置と負荷分散を統合し、スマートフォン上のLLM推論を高速・省メモリ化する。

- **2025-05 · [WINA: Weight Informed Neuron Activation for Accelerating Large Language Model Inference](2025-2505.19427-wina-weight-informed-neuron-activation-for-accelerating-large-language-m.md)**  
  実装：[✓](https://github.com/microsoft/wina) ・ リポジトリ内被引用：3  
  WINAは、既存の大規模言語モデル（LLM）を再学習せず、各層で計算に参加させる活性成分を選択する疎活性化方式である。代表例としてLlama-2-7Bの常識推論8課題平均では、65%の活性疎性でWINAが65.14、TEALが61.07、R-Sparseが59.37となった。

- **2025-02 · [M-ANT: Efficient Low-bit Group Quantization for LLMs via Mathematically Adaptive Numerical Type](2025-2502.18755-m-ant-efficient-low-bit-group-quantization-for-llms-via-mathematically-a.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  M-ANTは、LLMの細粒度グループ-wise量子化で「同じテンソル内でも64〜128要素程度の小グループごとに値分布が大きく違う」という問題へ、数値型そのものをグループごとに適応させる方式である。

- **2025-02 · [Accelerating LLM Inference with Lossless Speculative Decoding Algorithms for Heterogeneous Vocabularies](2025-2502.05202-accelerating-llm-inference-with-lossless-speculative-decoding-algorithms-for-heterogeneous-vocabularies.md)**  
  実装：[✓](https://github.com/keyboardAnt/hf-bench) ・ リポジトリ内被引用：3  
  対象モデルと提案モデルの語彙が異なっても損失なし投機的復号を可能にし、既製モデルの自由な組合せで自己回帰復号比最大2.8倍高速化する。

- **2024-12 · [Dynamic-LLaVA: Efficient Multimodal Large Language Models via Dynamic Vision-language Context Sparsification](2024-2412.00876-dynamic-llava-efficient-multimodal-large-language-models-via-dynamic-vis.md)**  
  実装：[✓](https://github.com/Osilly/dynamic_llava) ・ リポジトリ内被引用：3  
  動的-LLaVAは、マルチモーダル大規模言語モデル（マルチモーダル Large Language モデル; MLLM）の高速化を、画像トークンだけの削減ではなく「画像文脈と生成済み言語文脈の両方を、推論段階に応じて動的に疎化する」問題として扱う。予測は一度だけ行い、その保持/削除決定を後続層すべてで共有する。

- **2025-10 · [Patterns behind Chaos：大規模MoEのデータ移動予測](2025-2510.05497-patterns-behind-chaos-forecasting-data-movement-for-efficient-large-scale-moe-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  その知見を将来のウェハ級GPU設計へ適用すると四モデル平均6.6倍、既存GPU向けプリフィル認識型専門家配置ではMoE計算を最大1.25倍高速化した。

- **2025-10 · [INT v.s. FP: A Comprehensive Study of Fine-Grained Low-bit Quantization Formats](2025-2510.25602-int-v-s-fp-a-comprehensive-study-of-fine-grained-low-bit-quantization-fo.md)**  
  実装：[✓](https://github.com/ChenMnZ/INT_vs_FP) ・ リポジトリ内被引用：2  
  しかし、32要素や16要素ごとに独立した尺度を持つ細粒度量子化では、外れ値と典型値を同じ広い範囲へ押し込める必要が小さくなる。ハードウェアの評価は論理回路モデルによる推定であり、MXINT8のエネルギーがMXFP8の0.63倍という数値を、既存GPUの実測消費電力や推論速度と混同してはならない。

- **2025-09 · [SemShareKV: Efficient KVCache Sharing for Semantically Similar Prompts via Token-Level LSH Matching](2025-2509.24832-semsharekv-efficient-kvcache-sharing-for-semantically-similar-prompts-via-token-level-lsh-matching.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  意味的に近い別プロンプトをトークンLSHで対応付け、位置補正と層別再計算により完全一致なしでもKVを選択再利用する。

- **2025-09 · [RServe: Overlapping Encoding and Prefill for Efficient LMM Inference](2025-2509.24381-rserve-overlapping-encoding-and-prefill-for-efficient-lmm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  マルチモーダル入力の符号化が全件終わるまで言語モデルを待機させる依存を解消する。要求内では準備済み埋め込みだけを順にプリフィルへ渡し、要求間では処理可能トークンを複数要求から集めて分割パイプラインの空きを減らす。Qwen2.5-VLの評価で初回トークン遅延最大66%削減、入力トークン処理量最大109%増加を報告する。

- **2025-08 · [TinyServe: Query-Aware Cache Selection for Efficient LLM Serving](2025-2509.12211-tinyserve-query-aware-cache-selection.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  QueryごとにKVページの関連度を軽量メタデータで推定し、必要ページだけを融合CUDAカーネルで読むことで小型LLMサービングの復号とメモリ移動を削減する。

- **2025-08 · [PiKV: KV Cache Management System for Mixture of Experts](2025-2508.06526-pikv-kv-cache-management-for-mixture-of-experts.md)**  
  実装：[✓](https://github.com/NoakLiu/PiKV) ・ リポジトリ内被引用：2  
  混合専門家モデルのKVを専門家単位に分散し、選択・圧縮・保持判断を統合する設計。第3版本文には独立した実測評価節がない。

- **2025-08 · [MoE-Beyond: Learning-Based Expert Activation Prediction on Edge Devices](2025-2508.17137-moe-beyond-learning-based-expert-activation-prediction-on-edge-devices.md)**  
  実装：[✓](https://github.com/ngavhane/moe-beyond) ・ リポジトリ内被引用：2  
  トークン埋め込みと層IDから次のMoEエキスパートを予測する4層Transformerを学習し、10%容量のGPUキャッシュでMoE-Infinityの17%に対し約72%の適中率を示す。

- **2025-08 · [HAP: Hybrid Adaptive Parallelism for Efficient Mixture-of-Experts Inference](2025-2508.19373-hap-hybrid-adaptive-parallelism-for-efficient-mixture-of-experts-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  入力処理では多数トークンをまとめて計算するため通信量と演算量が大きいが、復号では1トークンずつ進むため重み読出しと専門家間の負荷不均衡が目立つ。各候補の遅延を演算・通信の実測から予測し、GPUメモリに収まる組合せだけを残す。

- **2025-07 · [BlockBPE: Parallel BPE Tokenization](2025-2507.11941-blockbpe-parallel-bpe-tokenization.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  BlockBPEは正規表現による事前分割を廃止し、Rustで入力をバイト列と特殊トークンへ分けた後、各文字列を一つのGPUスレッドブロックへ割り当てる。高バッチではtiktokenに対して最大2倍、HuggingFace Tokenizersに対して最大2.5倍の字句分割処理量を報告した。

- **2025-06 · [StoreLLM: Energy Efficient Large Language Model Inference with Permanently Pre-stored Attention Matrices](2026-d42c81b62392-storellm-energy-efficient-large-language-model-inference-with-permanently-pre-stored-attention-matrices.md)**  
  実装：[✓](https://github.com/StoreLLM/StoreLLM/) ・ リポジトリ内被引用：2  
  語彙トークンの注意行列を先に計算してSSDへ蓄え、頻出分だけDRAMへ置き、要求ごとに遅延を守りながら読出しか再計算かを選ぶ方式である。

- **2025-05 · [Speeding up Model Loading with fastsafetensors](2025-2505.23072-speeding-up-model-loading-with-fastsafetensors.md)**  
  実装：[✓](https://github.com/foundation-model-stack/fastsafetensors) ・ リポジトリ内被引用：2  
  fastsafetensorsは、safetensors形式の大規模モデルをストレージからGPUへロードする際、各テンソルをいったんホストメモリ上のPython/PyTorchオブジェクトとして逐次生成してからGPUへコピーする従来経路を改め、ファイル上の複数テンソルをまとめてGPUへ搬送し、GPU上でテンソル実体化・分割などの前処理を行うローダである。

- **2025-05 · [Llama-Nemotron: Efficient Reasoning Models](2025-2505.00949-llama-nemotron-efficient-reasoning-models.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Nano（80億）、Super（490億）、Ultra（2530億）の3規模を提供し、通常の会話と詳細な推論を同じモデルで切り替えられる。実測ではSuperが単一H100上、バッチ256の指定条件で元のLlama 3.3-70Bに対して5倍のスループットを報告し、Ultraは8枚のH100で元のLlama 3.1-405Bに対して1.71倍の遅延改善を得た。

- **2025-03 · [L1: Controlling How Long A Reasoning Model Thinks With Reinforcement Learning](2025-2503.04697-l1-controlling-how-long-a-reasoning-model-thinks-with-reinforcement-lear.md)**  
  実装：[✓](https://www.cmu-l3.github.io/l1) ・ リポジトリ内被引用：2  
  L1は、推論言語モデルの思考連鎖（chain-of-thought; CoT）の長さを、ユーザーがプロンプトで指定した計算予算へ合わせるための強化学習手法である。

- **2025-03 · [Collaborative Speculative Inference for Efficient LLM Inference Serving](2025-2503.10325-collaborative-speculative-inference-for-efficient-llm-inference-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  異種GPUへドラフト生成と検証を分離し、専門ドラフタ協調と動的パイプライン制御で投機推論の資源利用と受理率を改善する。

- **2025-01 · [MoE²: Optimizing Collaborative Inference for Edge Large Language Models](2025-2501.09410-moe-optimizing-collaborative-inference-for-edge-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  MoE²（Mixture-of-Edge-Experts）は、単一の大規模言語モデル内部に小さな専門家層を並べる方式ではなく、独立した端末・サーバーに配置された複数の大規模言語モデルそのものを専門家として扱う協調推論基盤である。

- **2024-12 · [HashEvict: A Pre-Attention KV Cache Eviction Strategy using Locality-Sensitive Hashing](2024-2412.16187-hashevict-a-pre-attention-kv-cache-eviction-strategy-using-locality-sensitive-hashing.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  問い合わせと鍵の短い局所性鋭敏型ハッシュ（LSH）間のハミング距離から注意度が低い候補を事前推定し、注意計算を実行する前に不要なKVキャッシュを動的に置換する。

- **2025-06 · [PecSched: Preemptive and Efficient Cluster Scheduling for LLM Inference](2024-2409.15104-csps-a-communication-efficient-sequence-parallelism-based-serving-system-for-transformer-based-models-with-long-prompts.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長入力事前計算を短入力事前計算で選択的に横取りし、事前計算・復号の分離同居と高速系列並列を組み合わせて、短入力の待ち時間と長入力の飢餓を両立して抑える。

- **2025-06 · [EQuARX: Efficient Quantized AllReduce in XLA for Distributed Machine Learning Acceleration](2025-2506.17615-equarx-quantized-allreduce-xla.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  AllReduce内でブロック量子化と逆量子化を通信へ重ね、TPU/XLAの集団通信量を削減する方式。int8でBF16 AllReduce比最大1.8倍、Gemma 3 27Bプリフィル最大1.28倍を示す。

- **2025-05 · [MorphServe: Efficient and Workload-Aware LLM Serving via Runtime Quantized Layer Swapping and KV Cache Resizing](2025-2506.02006-efficient-and-workload-aware-llm-serving-via-runtime-layer-swapping-and-kv-cache-resizing.md)**  
  実装：[✓](https://github.com/ds2-lab/MorphServe) ・ リポジトリ内被引用：1  
  負荷ピーク時だけ低影響層を低ビット版へ非同期交換し、空いたGPUメモリをKVキャッシュへ振り替えることで、平均SLO違反を92.45%削減しP95初回トークン遅延を2.2〜3.9倍改善する。

- **2025-04 · [Energy Considerations of Large Language Model Inference and Efficiency Optimizations](2025-2504.17674-energy-considerations-of-large-language-model-inference-and-efficiency-o.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LLM推論の電力量を、入力長・出力長・バッチ数・GPU・推論基盤・復号方式・モデル並列の組合せで実測し、実トラフィックの入出力長分布を区間化して総消費量を推定する。適切なソフトウェア最適化で未最適化PyTorch比最大73%削減できる一方、投機的復号や複数GPUは条件によって逆に電力量を増やす。

- **2025-02 · [TokenSkip: Controllable Chain-of-Thought Compression in LLMs](2025-2502.12067-tokenskip-controllable-chain-of-thought-compression-in-llms.md)**  
  実装：[✓](https://github.com/hemingkx/TokenSkip) ・ リポジトリ内被引用：1  
  思考連鎖（Chain-of-Thought、CoT）は、複雑な数学や論理の問題を段階的に解くことで大規模言語モデルの正答率を改善する。保持率を条件として複数の圧縮版を学習させ、推論時に指定した保持率に応じて短い思考列をモデル自身が直接生成するようにする。

- **2025-02 · [Chain of Draft: Thinking Faster by Writing Less](2025-2502.18600-chain-of-draft-thinking-faster-by-writing-less.md)**  
  実装：[✓](https://github.com/sileix/chain-of-draft) ・ リポジトリ内被引用：1  
  Chain of 下書き（CoD）は、推論連鎖（Chain-of-Thought; CoT）の冗長な自然言語を減らし、必要な中間計算だけを短いドラフトとして生成させるprompting方式である。

- **2024-12 · [IFMoE: An Inference Framework Design for Fine-grained MoE](2026-3190de0b4969-ifmoe-an-inference-framework-design-for-fine-grained-moe.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  共有部分をテンソル並列化して細粒度MoEの重複メモリを減らし、少数専門家で草稿生成した後に完全専門家設定でKVキャッシュを修整して復号を高速化する。

- **2024-11 · [DyCoke: Dynamic Compression of Tokens for Fast Video Large Language Models](2024-2411.15024-dycoke-dynamic-compression-of-tokens-for-fast-video-large-language-model.md)**  
  実装：[✓](https://github.com/KD-TAO/DyCoke) ・ リポジトリ内被引用：1  
  DyCokeは、動画大規模言語モデル（動画 大規模 言語 モデル; VLLM）が数十フレームを入力すると数万個の視覚トークンを生成し、プリフィルとデコードの注意計算およびKVキャッシュを膨張させる問題に対する、学習不要（学習-free）の二段階トークン圧縮法である。

- **2025-07 · [CateKV: On Sequential Consistency for Long-Context LLM Inference Acceleration](2026-2608.30295-catekv-on-sequential-consistency-for-long-context-llm-inference-acceleration.md)**  
  実装：[✓](https://github.com/haoyun-jiang/CateKV) ・ リポジトリ内被引用：0  
  プリフィルからデコードまで注意先が安定するヘッドだけKVを強く削減し、動的ヘッドは大半を保持するハイブリッドKVキャッシュで、精度を保ちながら長文推論のメモリ・デコード・バッチ性能を改善する。

- **2025-07 · [Accelerating Dense LLMs via L0-regularized Mixture-of-Experts](2026-2609.21672-accelerating-dense-llms-via-l0-regularized-mixture-of-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  L0-MoEは、既存の密（密）LLMを一からMoEとして再学習するのではなく、密 チェックポイントのフィードフォワードネットワーク（FFN）内部にある中間次元を、L0正則化（L0 正則化）でドメイン別に選択して複数の専門家（エキスパート）を作り、その後にルータを学習する軽量なMoE変換法である。

- **2025-05 · [Recursive Offloading for LLM Serving in Multi-tier Networks](2025-2505.16502-recursive-offloading-for-llm-serving-in-multi-tier-networks.md)**  
  実装：[✓](https://github.com/wuzhiyuan2000/RecServe) ・ リポジトリ内被引用：0  
  端末→エッジ→クラウドを信頼度で再帰的に上げ、履歴分位点から閾値を自動適応してCloudServe比50%以上の通信削減を狙う多層LLMサービング。

- **2025-04 · [SPIRe: Boosting LLM Inference Throughput with Speculative Decoding](2025-2504.06419-spire-throughput-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大バッチ投機的デコードの受理率とKV読出し量を実測し、浅くKVを制限したドラフトの性能モデルを構築して、重み読出しよりKV帯域が支配する条件の処理量を比較する研究。

- **2025-03 · [Reimagining Memory Access for LLM Inference: Compression-Aware Memory Controller Design](2025-2503.18869-reimagining-memory-access-for-llm-inference-compression-aware-memory-controller-design.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みとKVキャッシュをビットプレーン・チャネル単位に再配置して無損失圧縮を効かせ、動的量子化時は必要ビットだけを読むメモリ制御器で容量・帯域・エネルギーを同時に削減する。

- **2025-03 · [PIPO: Pipelined Offloading for Efficient Inference on Consumer Devices](2025-2504.03664-pipo-pipelined-offloading-for-efficient-inference-on-consumer-devices.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CPU/NVMeオフロードを計算・重み読込・KV読込/保存の細粒度タスクへ分解し、転送パイプラインとINT4 CUDAカーネルで6GB RTX 3060上のGPU利用率を90%超へ高める。

- **2025-02 · [AutoHete: An Automatic and Efficient Heterogeneous Training System for LLMs](2025-2503.01890-autohete-an-automatic-and-efficient-heterogeneous-training-system-for-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  活性値再計算・パラメータ退避・オプティマイザ退避を整数線形計画で共同選択し、反復をまたぐ優先度付き処理重畳でCPU/GPU待ちを減らす異種混在LLM学習方式。

### 3年前（2023-11〜2024-10）

- **2023-12 · [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](2023-2312.00752-mamba-selective-state-space-linear-time-inference.md)**  
  実装：[✓](https://github.com/state-spaces/mamba) ・ リポジトリ内被引用：73  
  入力依存の選択的状態空間層とGPU向け融合走査を統合し、注意機構なしでTransformer級品質と4〜5倍の生成スループットを両立する。

- **2024-07 · [FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](2024-2407.08608-flashattention-3-fast-and-accurate-attention-with-asynchrony-and-low-pre.md)**  
  実装：[✓](https://github.com/Dao-AILab/flash-attention) ・ リポジトリ内被引用：53  
  従来のFlashAttention系列は、注意重みの巨大な中間行列を高帯域メモリ（HBM）に書き戻さず、共有メモリとレジスタ内でタイルごとに処理することでメモリ転送を削減した。

- **2024-09 · [OLMoE: Open Mixture-of-Experts Language Models](2024-2409.02060-olmoe-open-mixture-of-experts-language-models.md)**  
  実装：[✓](https://github.com/allenai/OLMoE) ・ リポジトリ内被引用：46  
  混合専門家（Mixture-of-Experts; MoE）は総パラメータを増やしながら、各トークンで一部専門家だけを実行することで、密 モデルより計算量を抑えられる。

- **2024-03 · [QuaRot: Outlier-Free 4-Bit Inference in Rotated LLMs](2024-2404.00456-quarot-outlier-free-4-bit-inference-in-rotated-llms.md)**  
  実装：[✓](https://github.com/spcl/QuaRot) ・ リポジトリ内被引用：35  
  QuaRotは、大規模言語モデル（LLM）の4ビット推論を難しくする活性値の外れ値を、高精度の例外チャネルへ逃がすのではなく、モデルの関数を変えない直交回転（orthogonal rotation）で多数の次元へ分散する量子化手法である。

- **2024-04 · [RAGCache: Efficient Knowledge Caching for Retrieval-Augmented Generation](2024-2404.12457-ragcache-efficient-knowledge-caching-for-retrieval-augmented-generation.md)**  
  実装：✓ ・ リポジトリ内被引用：32  
  RAGCacheは、検索拡張生成（Retrieval-Augmented Generation; RAG）で同じ知識文書が何度も検索されることに着目し、その文書を言語モデルが処理したときの鍵・値キャッシュ（KVキャッシュ）を複数要求で再利用する推論提供システムである。

- **2023-11 · [FlashDecoding++: Faster Large Language Model Inference on GPUs](2023-2311.01282-flashdecoding-faster-large-language-model-inference-on-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：32  
  FlashDecoding++は、自己回帰型の大規模言語モデルで一語ずつ出力する復号段階を、GPUの演算資源とメモリ階層に合わせて高速化する推論エンジンである。論文が分離した三つの障害は、長い注意系列を分割したときの部分ソフトマックス結合同期、少数トークンを入力する細長い行列積のゼロ埋め、行列形状とGPUの種類を無視する固定実行方式である。

- **2024-04 · [Mixture-of-Depths: Dynamically allocating compute in transformer-based language models](2024-2404.02258-mixture-of-depths-dynamically-allocating-compute-in-transformer-based-la.md)**  
  実装：✓ ・ リポジトリ内被引用：30  
  Mixture-of-Depths（MoD）は、通常のTransformerがすべてのトークンをすべてのブロックで同じだけ処理する設計を変え、各層で「計算すべきトークン」だけを学習済みルータで選ぶ条件付き計算（conditional computation）方式である。

- **2024-02 · [QuIP#: Even Better LLM Quantization with Hadamard Incoherence and Lattice Codebooks](2024-2402.04396-quip-even-better-llm-quantization-with-hadamard-incoherence-and-lattice-.md)**  
  実装：[✓](https://github.com/Cornell-RelaxML/quip-sharp) ・ リポジトリ内被引用：30  
  QuIP#は4 ビット/重み以下、特に2〜3 ビットの極端な圧縮領域を対象とする重み専用の事後学習量子化（PTQ）である。Llama 2 70Bは2 ビットなら20GB未満へ収まり、proof-of-concept CUDA カーネルではRTX 4090上でpeak メモリ 帯域の50%超へ到達する。

- **2024-09 · [RetrievalAttention: Accelerating Long-Context LLM Inference via Vector Retrieval](2024-2409.10516-retrievalattention-accelerating-long-context-llm-inference-via-vector-re.md)**  
  実装：✓ ・ リポジトリ内被引用：29  
  RetrievalAttentionは、長文脈の大規模言語モデルが自己回帰復号で過去のすべての鍵値を走査する負担を、現在の質問に重要なトークンだけを動的に検索することで減らす手法である。しかし注意の質問と鍵は異なる重み行列で射影され、ベクトル分布がずれるため、一般的な索引をそのまま使うと高い再現率を得るために鍵の30～50%を走査しなければならない。

- **2024-04 · [Better & Faster Large Language Models via Multi-token Prediction](2024-2404.19737-better-faster-large-language-models-via-multi-token-prediction.md)**  
  実装：✓ ・ リポジトリ内被引用：28  
  一般的な自己回帰言語モデルは、各位置までの文脈から直後の一つのトークンを予測する。これに対して複数トークン予測（Multi-トークン Prediction; MTP）は、同じ位置の共有表現から、1個先だけでなく2個先、3個先、4個先など複数の未来トークンを別々の出力ヘッドで予測するよう学習する。この研究には二つの独立した成果がある。

- **2024-02 · [InfLLM: Training-Free Long-Context Extrapolation for LLMs with an Efficient Context Memory](2024-2402.04617-infllm-training-free-long-context-extrapolation-for-llms-with-an-efficie.md)**  
  実装：[✓](https://github.com/thunlp/InfLLM) ・ リポジトリ内被引用：26  
  InfLLMは、短い文脈長で事前学習された大規模言語モデル（LLM）を、重みの追加学習なしに非常に長い入力へ適用する方式である。

- **2024-07 · [PQCache: Product Quantization-based KVCache for Long Context LLM Inference](2024-2407.12820-pqcache-product-quantization-based-kvcache-for-long-context-llm-inferenc.md)**  
  実装：[✓](https://github.com/HugoZHL/PQCache) ・ リポジトリ内被引用：23  
  文脈が長くなるほどKVキャッシュは大きくなり、GPUメモリへ収まらない場合にはCPUメモリへの退避と転送が必要になる。Llama-3.1-8Bの128K文脈を用いたInfiniteBenchでは、過去トークンの1/10だけを選択する条件で平均スコア46.80を報告し、比較方式に対する改善は+4.60%である。

- **2024-04 · [SEER-MoE: Sparse Expert Efficiency through Regularization for Mixture-of-Experts](2024-2404.05089-seer-moe-sparse-expert-efficiency-through-regularization-for-mixture-of-.md)**  
  実装：✓ ・ リポジトリ内被引用：23  
  SEER-MoEは、事前学習済みMixture-of-エキスパート（MoE）を再学習せずそのままservingするのではなく、(1) ほとんど使われないエキスパートを物理的に削除してモデル メモリを減らし、(2) 各トークンで活性化するエキスパート数Top-(K)を2から1へ下げても品質が崩れにくいようQLoRAとルーティング 正則化で再適応する…

- **2024-02 · [Hydra: Sequentially-Dependent Draft Heads for Medusa Decoding](2024-2402.05109-hydra-sequentially-dependent-draft-heads-for-medusa-decoding.md)**  
  実装：[✓](https://github.com/zankner/Hydra) ・ リポジトリ内被引用：21  
  ハイドラは、メデューサ型の投機的復号（投機的 デコード）で使う複数の下書きヘッド（ドラフト ヘッド）を、互いに独立な将来-トークン predictorから逐次依存（逐次依存）なpredictorへ変える手法である。

- **2024-01 · [Extreme Compression of Large Language Models via Additive Quantization](2024-2401.06118-extreme-compression-of-large-language-models-via-additive-quantization.md)**  
  実装：[✓](https://github.com/Vahe1994/AQLM) ・ リポジトリ内被引用：20  
  加算量子化による言語モデル圧縮（AQLM）は、重みの極低ビット量子化における「小さいモデルを高精度で保持した方が、巨大モデルを2ビットにするより良い」という従来の精度対容量の関係を改善する研究である。Llama 2 7B・13B・70B、Mixtral 8×7B、Mistral 7Bを評価する。

- **2023-12 · [ASVD: Activation-aware Singular Value Decomposition for Compressing Large Language Models](2023-2312.05821-asvd-activation-aware-singular-value-decomposition-for-compressing-large.md)**  
  実装：[✓](https://github.com/hahnyuan/ASVD4LLM) ・ リポジトリ内被引用：20  
  活性認識特異値分解（活性値-考慮型 特異値分解; ASVD）は、学習済みLLMの線形 重みを再学習なしで低ランク化するpost-学習 圧縮である。LLaMA/LLaMA-2 7B〜13Bで10〜30%のモデル圧縮を示し、K/V 射影にも同じ低ランク構造を適用して中間の低次元活性値をキャッシュすることで、KV キャッシュを50%までほぼ品質低下なしに削減する。

- **2024-03 · [ShortGPT: Layers in Large Language Models are More Redundant Than You Expect](2024-2403.03853-shortgpt-layers-in-large-language-models-are-more-redundant-than-you-exp.md)**  
  実装：[✓](https://github.com/icip-cas/ShortGPT) ・ リポジトリ内被引用：18  
  本論文は、大規模言語モデルの全ての変換層が同程度に必要とは限らないという観察から、計算の一部を省略する二種類の方式を提案する。ACL 2025掲載版の代表例では、Llama2-13Bの40層から10層を対象とする条件で、多肢選択指標の平均値は58.49から53.57となり、元の約91.59%を維持した。

- **2024-02 · [Decoding Speculative Decoding](2024-2402.01528-decoding-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：17  
  350件超の投機的デコード実験からドラフト遅延と層深度を主要因と特定し、浅く広いドラフトモデルへ再設計して最大111%のスループット向上を示す。

- **2024-03 · [DéjàVu：KVキャッシュ・ストリーミングによる高速・耐障害LLM配信](2024-2403.01876-dejavu-kv-cache-streaming-for-fast-fault-tolerant-generative-llm-serving.md)**  
  実装：[✓](https://github.com/msr-fiddle/dejavu) ・ リポジトリ内被引用：16  
  また各マイクロバッチのKVキャッシュをGPUに保持し続けるとメモリを過剰確保し、障害時には失われたKV状態を再計算するため復旧が遅い。DéjàVuはこれらをKVキャッシュの高速な非同期転送という一つの機構で扱う。

- **2023-12 · [Gated Linear Attention Transformers with Hardware-Efficient Training](2024-2312.06635-gated-linear-attention-transformers-with-hardware-efficient-training.md)**  
  実装：[✓](https://github.com/sustcsonglin/flash-linear-attention) ・ リポジトリ内被引用：16  
  また再帰式を素朴にGPUへ実装すると、逐次依存や高帯域メモリへの状態書き込みが律速となる。著者らは二つの仕組みを提案する。

- **2024-06 · [A Survey on Mixture of Experts in Large Language Models](2024-2407.06204-a-survey-on-mixture-of-experts-in-large-language-models.md)**  
  実装：[✓](https://github.com/withinmiaov/A-Survey-on-Mixture-of-Experts-in-LLMs) ・ リポジトリ内被引用：15  
  全パラメータ数を大きくしても活性化する部分を限定できるが、実機では選択された専門家へのトークン転送、専門家ごとの負荷の偏り、GPU間の全対全通信、巨大な専門家重みの配置・退避が新たな律速になる。

- **2024-02 · [WKVQuant: Quantizing Weight and Key/Value Cache for Large Language Models Gains More](2024-2402.12065-wkvquant-quantizing-weight-and-key-value-cache-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  WKVQuantは、量子化対象を「重み・KVキャッシュ・一時活性化」に分解し、メモリ削減へ長時間効く重みとKVキャッシュだけを4ビット化し、一時活性化は高精度のまま残す事後量子化（post-学習 量子化; PTQ）方式である。

- **2024-02 · [The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits](2024-2402.17764-the-era-of-1-bit-llms-all-large-language-models-are-in-1-58-bits.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  狙いは、学習済みFP16/BF16モデルを後から近似する事後学習量子化ではなく、モデル自体を極低bit表現へ適応させ、品質を維持したまま重み転送・行列積・メモリ容量の支配項を小さくすることにある。

- **2024-02 · [Massive Activations in Large Language Models](2024-2402.17762-massive-activations-in-large-language-models.md)**  
  実装：[✓](https://github.com/locuslab/massive-activations) ・ リポジトリ内被引用：15  
  著者らは入力を変えたときの値の変動と、推論中に値を直接置換する介入実験から、巨大活性値が単なる数値的不安定さではなく、自己注意（self-注意機構）へ一定の加算成分を供給する暗黙のバイアス（implicit bias）として働くと結論付ける。

- **2024-04 · [Leave No Context Behind: Efficient Infinite Context Transformers with Infini-attention](2024-2404.07143-leave-no-context-behind-efficient-infinite-context-transformers-with-infini-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  Infini-注意機構は、入力文脈が数十万から100万トークンに達しても、過去の全トークンに対応する鍵・値（KV）を保存し続けずに情報を参照するための注意機構である。

- **2024-04 · [JetMoE: Reaching Llama2 Performance with 0.1M Dollars](2024-2404.07413-jetmoe-reaching-llama2-performance-with-0-1m-dollars.md)**  
  実装：[✓](https://github.com/myshell-ai/JetMoE) ・ リポジトリ内被引用：13  
  JetMoE-8Bは、混合専門家モデル（Mixture of エキスパート、MoE）の条件付き計算を順伝播ネットワーク（FFN）だけでなく自己注意機構へも拡張した、総パラメータ約80億の言語モデルである。論文はLlama2-7Bとの比較で推論演算量を約70%削減できると述べるが、これは実測の生成遅延が70%減るという意味ではない。

- **2024-10 · [ConServe: Fine-Grained GPU Harvesting for LLM Online and Offline Co-Serving](2024-2410.01228-conserve-fine-grained-gpu-harvesting-for-llm-online-and-offline-co-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  SLO予測付きトークン調整・層単位プリエンプション・増分KV退避で、オンライン遅延を守りながら遊休GPUをオフライン推論へ回す共同サービング方式。

- **2024-09 · [HybridFlow: A Flexible and Efficient RLHF Framework](2024-2409.19256-hybridflow-a-flexible-and-efficient-rlhf-framework.md)**  
  実装：[✓](https://github.com/volcengine/verl) ・ リポジトリ内被引用：12  
  HybridFlowは、人間フィードバックによる強化学習（Reinforcement Learning from Human Feedback: RLHF）を複数の大規模言語モデルからなる分散データフローとして扱い、その制御の柔軟性と学習処理率を両立するシステムである。

- **2024-01 · [Multi-Candidate Speculative Decoding](2024-2401.06706-multi-candidate-speculative-decoding.md)**  
  実装：[✓](https://github.com/NJUNLP/MCSD) ・ リポジトリ内被引用：12  
  標準方式では各深さに一つの候補しかない。したがって、研究の核は「候補幅による受理率向上」「分布保存の検証」「共有接頭辞による検証費用削減」の三点である。

- **2024-01 · [MoE-LLaVA: Mixture of Experts for Large Vision-Language Models](2024-2401.15947-moe-llava-mixture-of-experts-for-large-vision-language-models.md)**  
  実装：[✓](https://github.com/PKU-YuanGroup/MoE-LLaVA) ・ リポジトリ内被引用：12  
  単純に既学習LLMのFFNをMoEへ変えて視覚言語学習を始めると、モダリティ間の特徴分布差と専門家負荷の偏りにより学習が崩れやすい。そこで論文は三段階の分離学習（MoE-Tuning）を採用し、まず密なLVLMとして視覚と言語を整合・適応させ、その重みを専門家へ損失なく複製してから疎ルーティングを学ぶ。

- **2024-03 · [An Image is Worth 1/2 Tokens After Layer 2: Plug-and-Play Inference Acceleration for Large Vision-Language Models](2024-2403.06764-an-image-is-worth-1-2-tokens-after-layer-2-plug-and-play-inference-accel.md)**  
  実装：[✓](https://github.com/pkunlp-icler/FastV) ・ リポジトリ内被引用：11  
  LLaVA-1.5では一枚の336×336画像が576トークンになり、高解像度化や動画の複数フレーム処理では数千トークンへ増える。初期層では画像情報が広く注意される一方、深い層では少数のシステム指示や文章トークンへ注意が集中し、画像トークン一個当たりの注意効率が非常に低くなる。代表設定は二層後に視覚トークンの50%を削除する方式である。

- **2024-02 · [CLLMs: Consistency Large Language Models](2024-2403.00835-cllms-consistency-large-language-models.md)**  
  実装：[✓](https://github.com/hao-ai-lab/Consistency_LLM) ・ リポジトリ内被引用：11  
  整合性大規模言語モデル（Consistency Large Language Models; CLLMs）は、Jacobi型の並列復号で使う仮の複数トークン列から、自己回帰復号の最終固定点へ速く近づくよう既存LLMを追加学習する。固定点に対する大域整合性損失と通常の自己回帰損失を併用し、追加の小型草案モデルなしで生成を高速化する。

- **2024-01 · [Long Context Compression with Activation Beacon](2024-2401.03462-long-context-compression-with-activation-beacon.md)**  
  実装：[✓](https://github.com/FlagOpen/FlagEmbedding) ・ リポジトリ内被引用：11  
  活性値 Beaconは、文章そのものを短く書き換えるのではなく、Transformerの各層に生じる鍵・値活性を、追加したビーコントークンの活性へ直接圧縮する。圧縮率を8倍にした128K文脈の実験では、非圧縮で同じデータにより微調整した比較モデルに対し、推論時間を約半分、KVキャッシュを約8分の1にした。

- **2024-04 · [Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing](2024-2404.14618-hybrid-llm-cost-efficient-and-quality-aware-query-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  要求ごとの品質差を予測して小型LLMへの振り分け率を調整し、推論費を削減する。モデル間の品質差が大きいときは無品質低下での削減幅が限られる。

- **2024-08 · [Harder Task Needs More Experts: Dynamic Routing in MoE Models](unknown-7f27cb4187bc-harder-task-needs-more-experts-dynamic-routing-in-moe-models.md)**  
  実装：[✓](https://github.com/ZhenweiAn/Dynamic_MoE) ・ リポジトリ内被引用：9  
  HuangらのACL 2024論文は、ルータの専門家確率を高い順に累積し、閾値を超えた時点で専門家の追加を止める動的ルーティング（動的 ルーティング）を提案する。

- **2024-07 · [Mixture of A Million Experts](2024-2407.04153-mixture-of-a-million-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  混合専門家（Mixture of エキスパート、MoE）は多数の専門家のうち一部だけを活性化することで、総パラメータ容量と各トークンの計算を分離する。

- **2024-04 · [Characterizing Power Management Opportunities for LLMs in the Cloud](2024-ad611bbc0cdc-characterizing-power-management-opportunities-for-llms-in-the-cloud.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  この観測を使い、優先度別の二段階電力制御を行うPOLCAを提案する。著者らは本番トレースから生成した合成負荷を用いた離散事象シミュレーションで、既存の電力予算のままサーバーを30%多く配置しても、設定した遅延SLOを満たし、通常条件で電力ブレーキを起こさない結果を示した。

- **2024-06 · [Samba: Simple Hybrid State Space Models for Efficient Unlimited Context Language Modeling](2024-2406.07522-samba-simple-hybrid-state-space-models-for-efficient-unlimited-context-language-modeling.md)**  
  実装：[✓](https://github.com/microsoft/Samba) ・ リポジトリ内被引用：8  
  Sambaは、選択的状態空間モデル（Selective State Space モデル; SSM）で遠い過去を固定サイズ状態へ畳み込み、スライディング窓注意（Sliding Window 注意機構; SWA）で直近トークンを正確に参照する。

- **2023-11 · [LLaMA-VID: An Image is Worth 2 Tokens in Large Language Models](2023-2311.17043-llama-vid-an-image-is-worth-2-tokens-in-large-language-models.md)**  
  実装：[✓](https://github.com/dvlab-research/LLaMA-VID) ・ リポジトリ内被引用：8  
  LLaMA-VIDは、各フレームの情報を質問に応じて抽出する文脈トークンと画像内容を要約する内容トークンに分離する。ECCV 2024正式論文では、動画質問応答のMSVD-QAでVicuna-7B構成が正解率69.7%、MSRVTT-QAで57.7%、ActivityNet-QAで47.4%を記録した。

- **2024-04 · [Eagle and Finch: RWKV with Matrix-Valued States and Dynamic Recurrence](2024-2404.05892-eagle-and-finch-rwkv-with-matrix-valued-states-and-dynamic-recurrence.md)**  
  実装：[✓](https://github.com/RWKV/RWKV-LM) ・ リポジトリ内被引用：6  
  過去の鍵・値をトークン単位で保持する代わりに、複数ヘッドの固定サイズ行列状態を更新する。Eagleは行列状態とゲートを、Finchは内容依存の補間・時間減衰を導入し、長文脈での情報保持を改善する。

- **2024-03 · [LLaVA-PruMerge: Adaptive Token Reduction for Efficient Large Multimodal Models](2024-2403.15388-llava-prumerge-adaptive-token-reduction-for-efficient-large-multimodal-m.md)**  
  実装：[✓](https://github.com/42Shawn/LLaVA-PruMerge) ・ リポジトリ内被引用：6  
  LLaVA-PruMergeは、画像を大規模言語モデルへ渡す際の視覚トークン数を削減する方式である。LLaVA-1.5は336×336画素の画像から24×24個、すなわち576個の視覚トークンを生成する。

- **2024-01 · [Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models](2024-2401.04658-lightning-attention-2-a-free-lunch-for-handling-unlimited-sequence-lengt.md)**  
  実装：[✓](https://github.com/OpenNLPLab/lightning-attention) ・ リポジトリ内被引用：6  
  通常のソフトマックス注意は全トークン対を扱うため、系列長を n とすると計算量が二次に増える。Lightning 注意機構-2は因果線形注意をタイル内とタイル間へ分解する。

- **2023-12 · [Lookahead: An Inference Acceleration Framework for Large Language Model with Lossless Generation Accuracy](2023-2312.12728-lookahead-an-inference-acceleration-framework-for-large-language-model-w.md)**  
  実装：[✓](https://github.com/alipay/PainlessInferenceAcceleration) ・ リポジトリ内被引用：6  
  Lookaheadは、この空きを利用して過去の生成履歴から複数の継続候補を構成し、一回の対象モデル計算で複数トークンを確定する推論高速化方式である。

- **2023-11 · [Learning to Skip for Language Modeling](2023-2311.15436-learning-to-skip-for-language-modeling.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  モデルを深くすれば表現容量は増えるが、トークン当たりの行列演算と復号遅延も増える。提案するSkipLayerは各層を二値ルータで包み、トークンの現在の隠れ表現から「この層を実行する」か「入力をそのまま次層へ渡す」かを選ぶ。

- **2024-10 · [Minions: Accelerating Large Language Model Inference with Aggregated Speculative Execution](2024-2402.15678-minions-accelerating-large-language-model-inference-with-aggregated-speculative-execution.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  複数小型モデルの重み付き多数決、オンライン投機長調整、SSM/LLM非同期パイプラインを統合した投機的復号サービング。

- **2024-10 · [MatryoshkaKV: Adaptive KV Compression via Trainable Orthogonal Projection](2024-2410.14731-matryoshkakv-adaptive-kv-compression-via-trainable-orthogonal-projection.md)**  
  実装：[✓](https://github.com/The-kamisato/MatryoshkaKV-cache) ・ リポジトリ内被引用：5  
  MatryoshkaKVは、事前学習済み大規模言語モデル（LLM）の鍵値キャッシュ（KVキャッシュ）について、トークン数や注意ヘッド数を減らす代わりに各ヘッドが保存する特徴次元を縮小する方式である。単純な主成分分析（PCA）による次元削減は中程度の圧縮では有効だが、元のキャッシュ容量の半分以下にすると生成品質が急落する。

- **2024-06 · [Your Absorbing Discrete Diffusion Secretly Models the Conditional Distributions of Clean Data](2026-2406.03736-your-absorbing-discrete-diffusion-secretly-models-the-conditional-distri.md)**  
  実装：[✓](https://github.com/ML-GSAI/RADD) ・ リポジトリ内被引用：5  
  RADDは吸収型離散拡散の逆過程で必要な条件付き確率を時刻から切り離し、マスク配置が変わらないステップの推論を省略する。理論的な損失の等価性と、実際の生成時間・困惑度の双方を検証した研究。

- **2024-06 · [LLMCompass: Enabling Efficient Hardware Design for Large Language Model Inference](2024-6daecc086891-llmcompass-enabling-efficient-hardware-design-for-large-language-model-i.md)**  
  実装：[✓](https://github.com/PrincetonUniversity/LLMCompass) ・ リポジトリ内被引用：5  
  大規模言語モデルの推論アクセラレータを設計するとき、演算器数、オンチップメモリ容量、外部メモリ帯域、チップ面積、装置間接続、並列配置を変えるたびにRTL実装や実機試作を行うのは現実的ではない。実機検証ではNVIDIA A100、AMD MI210、Google TPUv3を使い、演算子遅延の平均誤差10.9%、LLM推論全体の平均遅延誤差4.1%を報告する。

- **2024-01 · [CaraServe: CPU-Assisted and Rank-Aware LoRA Serving for Generative LLM Inference](2024-2401.11240-caraserve-cpu-assisted-lora-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  LoRA読込中にCPUでプリフィル計算を先行し、ランク依存のバッチ遅延を予測してSLO違反が少ないサーバへ配分することで、多数アダプタ提供のコールドスタートを隠す。

- **2024-10 · [LightTransfer: Your Long-Context LLM is Secretly a Hybrid Model with Effortless Adaptation](2024-2410.13846-lighttransfer-your-long-context-llm-is-secretly-a-hybrid-model-with-effo.md)**  
  実装：[✓](https://github.com/sail-sg/LightTrans) ・ リポジトリ内被引用：4  
  キャッシュがGPUメモリを圧迫すると、同時に処理できる要求数が減り、長文脈の生成処理量も低下する。ある層では先頭の少数トークン（注意機構 sink）と直近の窓だけに注意が集中する。

- **2024-07 · [Learning to (Learn at Test Time): RNNs with Expressive Hidden States](2024-2407.04620-learning-to-learn-at-test-time-rnns-with-expressive-hidden-states.md)**  
  実装：[✓](https://github.com/test-time-training/ttt-lm-pytorch) ・ リポジトリ内被引用：4  
  本論文は、再帰型ニューラルネットワーク（Recurrent Neural Network、RNN）の隠れ状態を単なる固定長ベクトルではなく、小さな機械学習モデルの重みとして表現するテスト時訓練（Test-Time 学習、TTT）層を提案する。

- **2024-05 · [Boosting Multimodal Large Language Models with Visual Tokens Withdrawal for Rapid Inference](2024-2405.05803-boosting-multimodal-large-language-models-with-visual-tokens-withdrawal-.md)**  
  実装：[✓](https://github.com/lzhxmu/VTW) ・ リポジトリ内被引用：4  
  第一に、深い層では注意シンク（注意 sink）が強まり、576個の視覚トークン全体へ向く注意は約5%まで下がる一方、わずか35個のシステム トークンへ80%以上が集まる。

- **2024-04 · [HGRN2: Gated Linear RNNs with State Expansion](2024-2404.07904-hgrn2-gated-linear-rnns-with-state-expansion.md)**  
  実装：[✓](https://github.com/OpenNLPLab/HGRN2) ・ リポジトリ内被引用：4  
  これに対し、線形再帰モデルは固定サイズの状態へ履歴を圧縮して次のトークンを生成できるため、推論時の状態保存量を系列長に依存させない。

- **2024-03 · [PipeRAG: Fast Retrieval-Augmented Generation via Algorithm-System Co-design](2024-2403.05676-piperag-fast-retrieval-augmented-generation-via-algorithm-system-co-desi.md)**  
  実装：[✓](https://github.com/amazon-science/piperag) ・ リポジトリ内被引用：4  
  検索拡張生成（Retrieval-Augmented Generation、RAG）では、生成開始前に一度だけ外部情報を検索する方式に加え、生成文が伸びる途中でも検索を繰り返す方式がある。1024トークン生成の端から端の遅延では、同等以上の困惑度を維持しながらRETRO比最大2.6倍の短縮を示す。

- **2024-01 · [A Comprehensive Survey of Compression Algorithms for Language Models](2024-2401.15347-a-comprehensive-survey-of-compression-algorithms-for-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  枝刈り、量子化、知識蒸留、低ランク近似、パラメータ共有、効率的構造設計の六系統を、圧縮後の性能だけでなく、圧縮を実行するための学習・較正費用から比較するサーベイ。

- **2024-10 · [SplitLLM: Collaborative Inference of LLMs for Model Placement and Throughput Optimization](2024-2410.10759-splitllm-collaborative-inference-of-llms-for-model-placement-and-through.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  提案方式は、層ごとの端末推論時間、端末からサーバーへの上り転送時間、サーバーから端末への下り転送時間、サーバー資源消費量を測定し、モデルの順方向の依存関係を守りながら配置する。

- **2024-10 · [SparseVLM: Visual Token Sparsification for Efficient Vision-Language Model Inference](2024-2410.04417-sparsevlm-visual-token-sparsification-for-efficient-vision-language-mode.md)**  
  実装：[✓](https://github.com/Gumpest/SparseVLMs) ・ リポジトリ内被引用：3  
  SparseVLMは、視覚言語モデル（VLM）の入力画像から生じる大量の視覚トークンを、現在の質問に必要な情報をできるだけ残しながら削減する追加学習不要の方式である。

- **2024-09 · [Moshi: a speech-text foundation model for real-time dialogue](2024-2410.00037-moshi-a-speech-text-foundation-model-for-real-time-dialogue.md)**  
  実装：[✓](https://github.com/kyutai-labs/moshi) ・ リポジトリ内被引用：3  
  Moshiは、音声認識、テキストLLM、音声合成を順番に実行する音声対話システムを、入力音声を聞きながら出力音声を生成する全二重の音声言語モデルへ置き換える研究である。音声質問応答の零例評価では、MoshiがWeb Questions 26.6%、LLaMA Questions 62.3%、音声版TriviaQA 22.8%の正答率を示した。

- **2024-09 · [Discovering the Gems in Early Layers: Accelerating Long-Context LLMs with 1000x Input Token Reduction](2024-2409.17422-discovering-the-gems-in-early-layers-accelerating-long-context-llms-with.md)**  
  実装：[✓](https://github.com/SalesforceAIResearch/GemFilter) ・ リポジトリ内被引用：3  
  GemFilterは、長文脈LLMが回答に必要なトークン位置を最終層まで待たず、比較的早い層ですでに強く識別しているという観察を利用する、学習不要の入力圧縮法である。システム評価ではSnapKVとの比較で最大2.4倍の高速化と約30%のGPUメモリ削減を報告する。

- **2024-06 · [ProTrain: Efficient LLM Training via Memory-Aware Techniques](2024-2406.08334-protrain-efficient-llm-training-via-memory-aware-techniques.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  モデル状態と活性値の階層管理を費用モデルで自動調整し、限られたGPUメモリで学習容量とスループットを高める。

- **2024-06 · [Optimised Grouped-Query Attention Mechanism for Transformers](2024-2406.14963-optimised-grouped-query-attention-mechanism-for-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  既存の多頭注意（Multi-Head 注意機構、MHA）を、複数の質問ヘッドで鍵・値ヘッドを共有するグループ化質問注意（Grouped-Query 注意機構、GQA）へ変換すると、復号時に保存する鍵値キャッシュと鍵値投影のパラメータを減らせる。

- **2024-03 · [AI and Memory Wall](2024-2403.14123-ai-and-memory-wall.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  AI向け計算器の演算性能が急速に増える一方、DRAMやデバイス間通信の帯域は同じ速度で増えない。低バッチの自己回帰生成では重みの再読出しが支配的になり、FLOPsだけで推論性能を評価すると誤る。

- **2024-02 · [BlackMamba: Mixture of Experts for State-Space Models](2024-2402.01771-blackmamba-mixture-of-experts-for-state-space-models.md)**  
  実装：[✓](https://github.com/Zyphra/BlackMamba) ・ リポジトリ内被引用：3  
  選択的状態空間モデルの固定状態生成と、混合専門家層の疎な全結合計算を一つの言語モデルに組み込み、長系列生成・学習計算量・専門家の割当てを同時に評価した。

- **2023-12 · [Compressed Context Memory For Online Language Model Interaction](2023-2312.03414-compressed-context-memory-for-online-language-model-interaction.md)**  
  実装：[✓](https://github.com/snu-mllab/context-memory) ・ リポジトリ内被引用：3  
  オンライン対話、個人化推薦、複数課題の逐次学習では、要求を受けるたびに新しい文脈が追加される。Compressed Context メモリ（CCM）は、過去の鍵値キャッシュを、専用の圧縮トークンが生成する少数の鍵値へ繰り返し統合する。

- **2024-10 · [CoreInfer: Accelerating Large Language Model Inference with Semantics-Inspired Adaptive Sparse Activation](2024-2410.18311-coreinfer-accelerating-large-language-model-inference-with-semantics-ins.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  文の意味が安定している間は、生成トークンが変わっても必要なFFNニューロンの集合は大きく変わらない。プリフィル時に文単位の重要ニューロンを決めて生成中に固定し、トークンごとの予測器と頻繁な重み配置変更を避ける。

- **2024-06 · [Divergent Token Metrics: Measuring degradation to prune away LLM components -- and optimize quantization](2024-2311.01544-divergent-token-metrics-measuring-degradation-to-prune-away-llm-componen.md)**  
  実装：[✓](https://github.com/Aleph-Alpha/Divergent_Tokens) ・ リポジトリ内被引用：2  
  大規模言語モデルの圧縮では、重みを0にする枝刈りや、浮動小数点数を整数へ変換する量子化が、生成文をどの時点から変えてしまうかを把握する必要がある。この指標を使って行列ごとの枝刈り率を配分すると、Llama-2-13Bを全体75%疎化したとき、同じ平均疎化率の一様な大きさ基準の枝刈りより、WikiText2のPPLを13.512から8.101へ抑えられる。

- **2024-03 · [Decoding Compressed Trust: Scrutinizing the Trustworthiness of Efficient LLMs Under Compression](2024-2403.15447-decoding-compressed-trust-scrutinizing-the-trustworthiness-of-efficient-.md)**  
  実装：[✓](https://github.com/decoding-comp-trust/comp-trust) ・ リポジトリ内被引用：2  
  LLM圧縮の評価は、通常の質問応答や知識課題の性能を維持できるかに偏りがちである。評価の中心的な結果は、同程度に圧縮する場合は量子化が枝刈りより元モデルの信頼性を再現しやすいこと、4-bit量子化では一部軸が改善し得ること、3-bitでは通常性能に現れにくい深刻な回帰が生じることである。

- **2024-02 · [Training-Free Long-Context Scaling of Large Language Models](2024-2402.17463-training-free-long-context-scaling-of-large-language-models.md)**  
  実装：[✓](https://github.com/HKUNLP/ChunkLlama) ・ リポジトリ内被引用：2  
  二重チャンク注意（Dual Chunk 注意機構、以下DCA）は、回転位置埋め込み（Rotary Position Embedding、以下RoPE）を用いた大規模言語モデルが、事前学習時より長い系列で位置関係を見失う問題に対する推論時の注意計算の変更である。最後の比較は特定の閉形式4課題の平均であり、汎用能力の94%を意味しない。

- **2024-02 · [Accurate LoRA-Finetuning Quantization of LLMs via Information Retention](2024-2402.05445-accurate-lora-finetuning-quantization-of-llms-via-information-retention.md)**  
  実装：[✓](https://github.com/AI-Efficiency/IR-QLoRA) ・ リポジトリ内被引用：2  
  大規模言語モデルの重みを16ビットから4ビット以下へ縮めると、重みの保存量と推論時に必要な重み転送量を減らせる。量子化後の基盤重みを固定し、小さな低ランク適応行列だけを微調整するQLoRA系の方法でも、失われた情報を十分に取り戻せない場合がある。

- **2023-12 · [ZeroQuant(4+2): Redefining LLMs Quantization with a New FP6-Centric Strategy for Diverse Generative Tasks](2023-2312.08583-zeroquant-4-2-redefining-llms-quantization-with-a-new-fp6-centric-strate.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  大規模言語モデルの重みを4ビット整数へ量子化すると、重み容量とメモリ転送量を大きく減らせる。

- **2023-12 · [Understanding the Potential of FPGA-Based Spatial Acceleration for Large Language Model Inference](2023-2312.15159-understanding-the-potential-of-fpga-based-spatial-acceleration-for-large.md)**  
  実装：[✓](https://github.com/cornell-zhang/allo/tree/main/examples) ・ リポジトリ内被引用：2  
  大規模言語モデルの推論を再構成可能な論理回路（FPGA）へ載せる従来方式の多くは、同じ演算器を複数の演算子・層へ順番に割り当てる時間多重型である。AMD Alveo U280上のGPT-2では、同じFPGAのDFXに対してプリフィル2.16倍、復号1.10倍の高速化を報告する。

- **2023-12 · [LLMCompass: Enabling Efficient Hardware Design for Large Language Model Inference](2023-2312.03134-llmcompass-enabling-efficient-hardware-design-for-large-language-model-i.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  大規模言語モデル（Large Language モデル、LLM）の推論には、膨大な重みを保存するメモリ、行列演算器、注意計算のためのキャッシュ、複数装置間の通信が必要になる。新しいアクセラレータを設計する際、最高演算性能や最高メモリ帯域の仕様だけを比較しても、実際のモデルがどの程度速く動くかは分からない。

- **2023-11 · [Routing to the Expert: Efficient Reward-guided Ensemble of Large Language Models](2023-2311.08692-routing-to-the-expert-efficient-reward-guided-ensemble-of-large-language.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  本論文が解こうとする問題は、異なる得意分野を持つ既製の大規模言語モデル（LLM）を組み合わせる際、問い合わせごとに候補すべてを実行すると生成計算量が膨らむことである。一方、回答をすべて生成して報酬モデル（reward モデル）で順位付けする方式は品質の良い候補を後から選べるが、候補数に比例する生成費用を必要とする。

- **2024-10 · [PyramidDrop: Accelerating Your Large Vision-Language Models via Pyramid Visual Redundancy Reduction](2024-2410.17247-pyramiddrop-accelerating-your-large-vision-language-models-via-pyramid-v.md)**  
  実装：[✓](https://github.com/Cooperx521/PyramidDrop) ・ リポジトリ内被引用：1  
  大規模視覚言語モデル（Large Vision-Language モデル; LVLM）は、画像を数百から数千の画像トークンへ変換して、文章の質問と一緒に言語モデルへ入力する。画像解像度が上がると画像トークンが増え、注意計算と全結合層の演算量が大きくなる。複数の視覚言語ベンチマークで品質は概ね維持されるが、個別の高解像度課題では小さな低下もある。

- **2024-10 · [LongVU: Spatiotemporal Adaptive Compression for Long Video-Language Understanding](2024-2410.17434-longvu-spatiotemporal-adaptive-compression-for-long-video-language-under.md)**  
  実装：[✓](https://github.com/Vision-CAIR/LongVU) ・ リポジトリ内被引用：1  
  LongVUは、長時間動画を多模態大規模言語モデルへ入力するとき、視覚トークン数が文脈長を超える問題に対して、時間方向の冗長なフレーム削除、質問に応じた空間解像度の配分、フレーム間で重複する空間トークンの削除を段階的に組み合わせる方式である。

- **2024-09 · [LLaMA-Omni: Seamless Speech Interaction with Large Language Models](2024-2409.06666-llama-omni-seamless-speech-interaction-with-large-language-models.md)**  
  実装：[✓](https://github.com/ictnlp/LLaMA-Omni) ・ リポジトリ内被引用：1  
  LLaMA-Omniは、音声認識（automatic 音声 recognition; 音声認識）→大規模言語モデル（large 言語 モデル; LLM）→音声合成（テキスト-to-音声; 音声合成）を直列に接続するカスケード構成の遅延を避け、ユーザーの音声指示からテキスト応答と音声応答をほぼ同時に生成するエンドツーエンド音声対話モデルである。

- **2024-02 · [LongHeads: Multi-Head Attention is Secretly a Long Context Processor](2024-2402.10685-longheads-multi-head-attention-is-secretly-a-long-context-processor.md)**  
  実装：[✓](https://github.com/LuLuLuyi/LongHeads) ・ リポジトリ内被引用：1  
  LongHeadsは、事前学習時よりはるかに長い文章を既存の大規模言語モデルへ与える際、各注意頭が全文へ注意する必要はないという観察を利用した、追加学習不要の長文推論方式である。LLaMA-2-7Bを単一NVIDIA A100で評価し、32Kのパスキー検索でほぼ100%、CPUへKVキャッシュを退避した128K条件でも2K注意窓で100%を報告する。

- **2024-02 · [FlattenQuant: Breaking Through the Inference Compute-bound for Large Language Models with Per-tensor Quantization](2024-2402.17985-flattenquant-breaking-through-the-inference-compute-bound-for-large-lang.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  FlattenQuantは、大規模言語モデル（LLM）の推論で、重みだけを低ビット化しても行列演算が半精度のまま残るという問題を解く後学習量子化（post-学習 量子化; PTQ）方式である。難点は、LLMの活性値に他のチャネルより20〜100倍程度大きい外れ値チャネルが存在することだ。

- **2024-02 · [Efficient Prompt Caching via Embedding Similarity](2024-2402.01173-efficient-prompt-caching-via-embedding-similarity.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文は、言語モデルの生成済み応答そのものを再利用するプロンプトキャッシュの判定精度を改善する研究である。以前の質問に対する回答がキャッシュにあれば、新しい質問を言語モデルへ送らず、その回答を返すことができる。ただし、質問文の意味が近いことと、同じ回答で両方の質問に正しく答えられることは一致しない。

- **2024-01 · [Inferflow: an Efficient and Highly Configurable Inference Engine for Large Language Models](2024-2401.08294-inferflow-an-efficient-and-highly-configurable-inference-engine-for-larg.md)**  
  実装：[✓](https://github.com/inferflow/inferflow) ・ リポジトリ内被引用：1  
  Inferflowは、言語モデルの構造が頻繁に変化する状況で、モデルごとに推論エンジンのソースコードを書き足す負担を減らすことを主目的とした推論基盤である。この拡張性に加え、低ビット量子化と複数GPU分割による実行効率を追求する。

- **2024-09 · [DisDP: Disaggregating Compute, Network, and Storage for Model-Sharded Data-Parallel Training](2024-2409.00918-luwu-an-end-to-end-in-network-out-of-core-optimizer-for-100b-scale-model-in-network-data-parallel-training-on-distribute.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPUから通信とオプティマイザ状態をSmartNIC・SmartSwitch・単一パラメータサーバへ分離し、100B級モデル分割データ並列の干渉と容量制約を同時に減らす。

### 4年前（2022-11〜2023-10）

- **2023-07 · [FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](2023-2307.08691-flashattention-2.md)**  
  実装：[✓](https://github.com/Dao-AILab/flash-attention) ・ リポジトリ内被引用：217  
  初代FlashAttentionのオンライン・ソフトマックスとタイル分割を保ちつつ、行列積以外の演算とブロック・ワープ間の仕事分割を再設計し、A100で理論演算性能の最大73%と初代比約2倍の高速化を達成する。

- **2023-05 · [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](2023-2305.13245-gqa.md)**  
  実装：✓ ・ リポジトリ内被引用：166  
  標準の多頭注意（Multi-Head 注意機構; MHA）は各クエリ頭に独立した鍵頭と値頭を持つため、復号時には全KV頭のキャッシュを読み出す必要がある。

- **2022-11 · [SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models](2022-2211.10438-smoothquant-accurate-and-efficient-post-training-quantization-for-large-language-models.md)**  
  実装：[✓](https://github.com/mit-han-lab/smoothquant) ・ リポジトリ内被引用：159  
  活性値全体を単純に8ビットへ写すと、その少数の外れ値が量子化範囲を広げ、通常値へ割り当てられる段階数が減って精度が崩れる。OPT、BLOOM、GLM、MT-NLGなどで8ビット重み・8ビット活性値（W8A8）を実現し、精度低下をほぼ抑えながら最大1.56倍の推論高速化と2倍のメモリ削減を報告し、530Bモデルを単一ノードで提供可能にした。

- **2022-11 · [Efficiently Scaling Transformer Inference](2022-2211.05102-efficiently-scaling-transformer-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：128  
  TPU v4上の大規模Transformer推論を通信・メモリ・計算モデルから設計し、2D重み固定/重み収集の切替とバッチ分割MQAで540B級の低遅延・高MFU・長文脈を両立する。

- **2023-06 · [A Simple and Effective Pruning Approach for Large Language Models](2023-2306.11695-a-simple-and-effective-pruning-approach-for-large-language-models.md)**  
  実装：[✓](https://github.com/locuslab/wanda) ・ リポジトリ内被引用：71  
  Wanda（重みと活性による枝刈り、枝刈り by 重み and 活性値）は、大規模言語モデルの線形層を追加学習も残存重みの更新も行わず疎化する方法である。LLaMA-7Bを50%非構造疎化したとき、WikiTextの困惑度は単純大きさ枝刈り17.29、Wanda 7.26、SparseGPT 7.22であり、軽い処理でも品質を大幅に保てる。

- **2023-01 · [SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot](2023-2301.00774-sparsegpt-massive-language-models-can-be-accurately-pruned-in-one-shot.md)**  
  実装：[✓](https://github.com/IST-DASLab/sparsegpt) ・ リポジトリ内被引用：62  
  重みの絶対値が小さい順に削除する単純な枝刈りでは、巨大モデルであっても削除による層出力誤差が累積し、50%の疎化で性能が崩壊し得る。

- **2023-05 · [LLM-Pruner: On the Structural Pruning of Large Language Models](2023-2305.11627-llm-pruner-on-the-structural-pruning-of-large-language-models.md)**  
  実装：[✓](https://github.com/horseee/LLM-Pruner) ・ リポジトリ内被引用：52  
  LLM-Prunerは、大規模言語モデルのパラメータを実際に削除して小さい密行列モデルへ変換する構造枝刈り手法である。LLaMA-7B、Vicuna-7B、ChatGLM-6Bを評価し、LLaMA-7Bでは20%の構造削減でゼロショット七課題平均が63.25から56.82へ下がり、低ランク適応後60.07まで回復した。

- **2023-10 · [DistillSpec: Improving Speculative Decoding via Knowledge Distillation](2023-2310.08461-distillspec-improving-speculative-decoding-via-knowledge-distillation.md)**  
  実装：✓ ・ リポジトリ内被引用：50  
  ドラフト自身の生成データと課題別の分布間距離でターゲットとの整合を蒸留し、投機的デコードの候補受理率を上げる手法。

- **2023-08 · [OmniQuant: Omnidirectionally Calibrated Quantization for Large Language Models](2023-2308.13137-omniquant-omnidirectionally-calibrated-quantization-for-large-language-m.md)**  
  実装：[✓](https://github.com/OpenGVLab/OmniQuant) ・ リポジトリ内被引用：48  
  大規模言語モデルの重みを16ビットから4ビット、3ビット、2ビットへ縮めると、保存容量と重み転送量を大きく削減できる。一方、極低ビットでは重みや活性値の少数の外れ値が量子化範囲を広げ、重要な値の量子化刻みが粗くなって出力品質が崩れる。LLaMA-2 7B～70Bは128個の校正系列とA100 40GB 1基で1～16時間の処理が可能と報告される。

- **2023-10 · [Ring Attention with Blockwise Transformers for Near-Infinite Context](2023-2310.01889-ring-attention-blockwise-transformers.md)**  
  実装：[✓](https://github.com/lhao499/llm_large_context) ・ リポジトリ内被引用：44  
  キー・値ブロックをリング転送しながらブロック注意計算を重畳し、系列長に依存しない活性化メモリで最大文脈長をデバイス数に比例して拡張する分散注意方式。

- **2023-05 · [LLM-QAT: Data-Free Quantization Aware Training for Large Language Models](2023-2305.17888-llm-qat-data-free-quantization-aware-training-for-large-language-models.md)**  
  実装：[✓](https://github.com/facebookresearch/LLM-QAT) ・ リポジトリ内被引用：42  
  LLM-QATは、学習後量子化（Post-学習 量子化: PTQ）では精度が大きく低下する低ビット領域に対し、量子化誤差を学習中に経験させる量子化対応学習（Quantization-Aware 学習: QAT）を大規模言語モデルへ適用する研究である。

- **2023-05 · [RWKV: Reinventing RNNs for the Transformer Era](2023-2305.13048-rwkv-reinventing-rnns-for-the-transformer-era.md)**  
  実装：[✓](https://github.com/BlinkDL/RWKV-LM) ・ リポジトリ内被引用：38  
  RWKVの大きな特徴は、単に注意を近似して軽量化することではなく、同じ重みと演算を訓練時の並列形式と推論時の再帰形式の双方で扱うことである。論文自身も長文脈評価の一部で弱点を示し、指示の順序を変えるだけで下流評価が大きく改善する例を報告している。

- **2023-08 · [YaRN: Efficient Context Window Extension of Large Language Models](2023-2309.00071-yarn-efficient-context-window-extension-of-large-language-models.md)**  
  実装：[✓](https://github.com/jquesnelle/yarn) ・ リポジトリ内被引用：32  
  大規模言語モデルの回転位置埋め込み（Rotary Position Embedding、RoPE）は、クエリとキーを位置に応じた角度だけ回転し、両者の内積が相対位置を反映するように設計される。128Kまでのパスキー検索では7B・13Bとも平均正答率99.4%を報告する。

- **2023-07 · [Retentive Network: A Successor to Transformer for Large Language Models](2023-2307.08621-retentive-network-a-successor-to-transformer-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：32  
  RetNetは、指数減衰付き保持演算を並列・再帰・チャンク再帰の三形式で同じ重みのまま実行する。6.7Bモデルの8K入力ではTransformerのKVキャッシュ方式に対し復号8.4倍、メモリ約70%削減を報告し、学習の並列性と固定状態復号を両立する。

- **2023-10 · [Sheared LLaMA: Accelerating Language Model Pre-training via Structured Pruning](2023-2310.06694-sheared-llama-accelerating-language-model-pre-training-via-structured-pr.md)**  
  実装：[✓](https://github.com/princeton-nlp/LLM-Shearing) ・ リポジトリ内被引用：27  
  枝刈り直後に失われた能力は継続事前学習で回復するが、その際にも学習データを元の比率で使い続けず、領域別の損失回復状況に応じて再配分する。A100 80GB上の単一生成で、13億パラメータの均一形状は毎秒58トークン、非均一形状は51トークン、27億では43対37トークンであった。

- **2023-08 · [LM-Infinite: Zero-Shot Extreme Length Generalization for Large Language Models](2023-2308.16137-lm-infinite-zero-shot-extreme-length-generalization-for-large-language-m.md)**  
  実装：[✓](https://github.com/Glaciohound/LM-Infinite) ・ リポジトリ内被引用：27  
  この設計は全過去トークンへの密注意をやめるため計算量を系列長に対して線形へ落とし、同時に位置表現が未経験距離へ外挿されるのを防ぐ。論文は最大200M トークンまでパープレキシティを保つ極端長実験、Passkey 検索・Qasper、通常の長文生成、速度・メモリを評価し、元モデルに対してデコード約2.7倍高速、メモリ最大7.5倍削減を報告する。

- **2023-04 · [Learning to Compress Prompts with Gist Tokens](2023-2304.08467-learning-to-compress-prompts-with-gist-tokens.md)**  
  実装：[✓](https://github.com/jayelm/gisting) ・ リポジトリ内被引用：22  
  指示の鍵・値状態をそのままキャッシュすれば再計算は減るものの、保持する状態の長さは指示トークン数に比例する。Jesse Muらの研究は、指示の意味を短い要旨トークン（gist トークン）の内部状態へ集約し、後続の異なる入力に再利用する「要旨化（gisting）」を提案する。

- **2022-12 · [The case for 4-bit precision: k-bit Inference Scaling Laws](2022-2212.09720-the-case-for-4-bit-precision-k-bit-inference-scaling-laws.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  量子化では、1パラメータ当たりのビット数を下げるほど同じ重みメモリへ大きなモデルを置ける。

- **2023-07 · [LongNet: Scaling Transformers to 1,000,000,000 Tokens](2023-2307.02486-longnet-scaling-transformers-to-1-000-000-000-tokens.md)**  
  実装：[✓](https://aka.ms/LongNet) ・ リポジトリ内被引用：18  
  LongNetは、自己注意の計算量が系列長Nの二乗で増える問題を、拡張注意（dilated 注意機構）で解くTransformer変種である。

- **2023-05 · [FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance](2023-2305.05176-frugalgpt-how-to-use-large-language-models-while-reducing-cost-and-impro.md)**  
  実装：[✓](https://github.com/stanford-futuredata/FrugalGPT) ・ リポジトリ内被引用：17  
  FrugalGPTは、価格・正確さ・誤答の種類が異なる複数の大規模言語モデル（LLM）を、予算を超えずに組み合わせる推論時のサービス選択方式である。

- **2023-04 · [Outlier Suppression+: Accurate quantization of large language models by equivalent and optimal shifting and scaling](2023-2304.09145-outlier-suppression-accurate-quantization-of-large-language-models-by-eq.md)**  
  実装：[✓](https://github.com/ModelTC/Outlier_Suppression_Plus) ・ リポジトリ内被引用：17  
  Outlier Suppression+（OS+）は、大規模言語モデルの活性値に現れる極端な外れ値が、事後量子化（Post-学習 量子化: PTQ）の精度を悪化させる問題に対する方法である。

- **2023-10 · [LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression](2023-2310.06839-longllmlingua-accelerating-and-enhancing-llms-in-long-context-scenarios-.md)**  
  実装：[✓](https://aka.ms/LongLLMLingua) ・ リポジトリ内被引用：16  
  LongLLMLinguaは、長いプロンプトを単に一律に切り詰めるのではなく、「質問に対してどの文書・トークンが有用か」を小型言語モデルで推定し、重要部分へトークン予算を集中させる長文脈プロンプト圧縮法である。

- **2023-10 · [ReLU Strikes Back: Exploiting Activation Sparsity in Large Language Models](2024-2310.04564-relu-strikes-back-exploiting-activation-sparsity-in-large-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  さらに既存Falcon/LlamaをReLUへ変換するrelufication、正規化層の後にもReLUを追加する第二段階、複数トークンを跨いだ集約疎性（aggregated 疎性）を提案し、推論時の重み I/O削減へ接続する。

- **2023-10 · [Compressing Context to Enhance Inference Efficiency of Large Language Models](2023-2310.06201-compressing-context-to-enhance-inference-efficiency-of-large-language-mo.md)**  
  実装：[✓](https://github.com/liyucheng09/Selective_Context) ・ リポジトリ内被引用：15  
  長い文書や会話を大規模言語モデル（LLM）へ入力すると、初回入力処理と鍵・値キャッシュに多くの時間・メモリが必要になる。Selective Contextは、下流モデルの構造や重みを変更する代わりに、入力文脈に含まれる予測しやすい語句を事前に削り、残った自然言語テキストだけを渡す。

- **2022-12 · [Hungry Hungry Hippos: Towards Language Modeling with State Space Models](2022-2212.14052-hungry-hungry-hippos-towards-language-modeling-with-state-space-models.md)**  
  実装：[✓](https://github.com/HazyResearch/H3) ・ リポジトリ内被引用：15  
  本論文は、状態空間モデル（state space モデル; SSM）が長系列を効率的に処理できるにもかかわらず、言語モデリングでは注意機構（注意機構）を使う変換器（Transformer）に劣る理由を二つの観点から調べる。

- **2023-03 · [ZeroQuant-V2: Exploring Post-training Quantization in LLMs from Comprehensive Study to Low Rank Compensation](2023-2303.08302-zeroquant-v2-exploring-post-training-quantization-in-llms-from-comprehen.md)**  
  実装：[✓](https://github.com/microsoft/DeepSpeed) ・ リポジトリ内被引用：14  
  ZeroQuant-V2は、学習後量子化（post-学習 量子化; PTQ）を一つの新方式だけで評価するのではなく、OPTとBLOOMの125M〜176Bを横断して「重みだけ」「活性値だけ」「重み+活性値」、INT8/INT4、対称/非対称、丸め（round-to-nearest; RTN）、GPTQ…

- **2023-07 · [In-context Autoencoder for Context Compression in a Large Language Model](2023-2307.06945-in-context-autoencoder-for-context-compression-in-a-large-language-model.md)**  
  実装：[✓](https://github.com/getao/icae) ・ リポジトリ内被引用：13  
  本論文は、大規模言語モデル（LLM）の長い入力文脈を、同じモデルがそのまま利用できる短い連続表現へ学習圧縮する文脈内自己符号化器（In-context Autoencoder、ICAE）を提案する。

- **2023-07 · [Predictive Pipelined Decoding: A Compute-Latency Trade-off for Exact LLM Decoding](2023-2307.05908-predictive-pipelined-decoding-a-compute-latency-trade-off-for-exact-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  予測パイプライン復号（Predictive Pipelined Decoding; PPD）は、自己回帰大規模言語モデルの「現在トークンが最終層まで確定しないと次トークンの計算を開始できない」という逐次依存を、追加の計算資源で一部重畳する方式である。

- **2023-03 · [Resurrecting Recurrent Neural Networks for Long Sequences](2023-2303.06349-resurrecting-recurrent-neural-networks-for-long-sequences.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  連続時間状態空間モデルの特殊な離散化を出発点とせず、古典的な再帰型ニューラルネットワークを線形化・複素対角化・安定化・正規化することで、長距離依存の精度と並列学習速度を回復できることを、段階的な除去実験で示した研究。論文が測ったのは主として長系列ベンチマークの分類精度と学習速度であり、大規模言語モデルの実運用推論性能ではない。

- **2023-05 · [Unlimiformer: Long-Range Transformers with Unlimited Length Input](2023-2305.01625-unlimiformer-long-range-transformers-with-unlimited-length-input.md)**  
  実装：[✓](https://github.com/abertsch72/unlimiformer) ・ リポジトリ内被引用：8  
  文書が長いほど参照すべきキーと値の数が増え、推論時のメモリ使用量と注意計算が膨らむ。長文専用の注意構造へモデルを変更する方式は再事前学習や追加の位置埋め込み学習を要する場合がある。

- **2023-07 · [Skeleton-of-Thought: Prompting LLMs for Efficient Parallel Generation](2023-2307.15337-skeleton-of-thought-prompting-llms-for-efficient-parallel-generation.md)**  
  実装：[✓](https://github.com/imagination-research/sot) ・ リポジトリ内被引用：7  
  Skeleton-of-Thought（SoT）はモデル内部の注意カーネルを変えず、回答を「骨格作成」と「各項目の独立展開」に分解して、後半を並列実行する。高速化の源泉は総トークン数を必ず減らすことではなく、長い1本の逐次デコードを複数の短いデコードへ分け、クリティカルパスを短くする点にある。

- **2023-05 · [Let's Sample Step by Step: Adaptive-Consistency for Efficient Reasoning and Coding with LLMs](2023-2305.11860-let-s-sample-step-by-step-adaptive-consistency-for-efficient-reasoning-a.md)**  
  実装：[✓](https://sample-step-by-step.info) ・ リポジトリ内被引用：6  
  大規模言語モデル（LLM）で多段階推論の精度を上げる自己整合性（自己整合性）は、同じ質問に対して複数の思考連鎖を標本化し、最終回答を多数決する方式である。最大7.9倍の節約は個別条件の値であり、全条件平均ではない。

- **2023-04 · [Scaling Transformer to 1M tokens and beyond with RMT](2023-2304.11062-scaling-transformer-to-1m-tokens-and-beyond-with-rmt.md)**  
  実装：[✓](https://github.com/burtsev/RMT-experiments) ・ リポジトリ内被引用：6  
  再帰メモリトランスフォーマー（Recurrent メモリ トランスフォーマー; RMT）は、長い入力を固定長の区間（セグメント）へ分割し、少数の学習可能なメモリトークン（メモリ トークン）の状態だけを次の区間へ再帰的に渡すことで、事前学習済みトランスフォーマーの有効文脈を伸ばす。重要なのは、専用の外部メモリ読書き機構を追加しない点である。

- **2023-10 · [Sparse Universal Transformer](2023-2310.07096-sparse-universal-transformer.md)**  
  実装：[✓](https://github.com/shawntan/SUT) ・ リポジトリ内被引用：5  
  Sparse Universal Transformer（SUT）は、同じTransformerブロックを複数回反復するユニバーサルTransformer（Universal Transformer; UT）の長所を残しながら、反復計算を疎な専門家選択と動的停止で削減するモデルである。通常のTransformerは各層に別の重みを持つ。

- **2023-10 · [Compressing LLMs: The Truth is Rarely Pure and Never Simple](2023-2310.01382-compressing-llms-the-truth-is-rarely-pure-and-never-simple.md)**  
  実装：[✓](https://github.com/VITA-Group/llm-kick) ・ リポジトリ内被引用：5  
  困惑度（perplexity）がほぼ維持されても、圧縮モデルの事実知識や指示追従は失われ得る。知識をモデル内部から答える課題と、外部文脈を与える検索・要約を分けて評価することで、枝刈りと量子化の能力別の弱点を可視化する。

- **2023-07 · [Efficient Guided Generation for Large Language Models](2023-2307.09702-efficient-guided-generation-for-large-language-models.md)**  
  実装：[✓](https://github.com/dottxt-ai/outlines) ・ リポジトリ内被引用：5  
  従来方式は、各生成ステップで語彙中のN個のトークン文字列を照合し、現在の部分出力に続けてよいかを調べるため、制約判定が少なくとも語彙数に比例する。

- **2023-05 · [LoRAPrune: Structured Pruning Meets Low-Rank Parameter-Efficient Fine-Tuning](2023-2305.18403-loraprune-structured-pruning-meets-low-rank-parameter-efficient-fine-tun.md)**  
  実装：[✓](https://github.com/aim-uofa/LoRAPrune) ・ リポジトリ内被引用：5  
  LoRAPruneは、事前学習済み大規模言語モデルを配備しやすい小型の密モデルへ変えるために、低ランク適応（Low-Rank Adaptation、LoRA）と構造化枝刈り（structured 枝刈り）を一体化する方式である。

- **2023-09 · [Transformer-VQ: Linear-Time Transformers via Vector Quantization](2023-2309.16354-transformer-vq-linear-time-transformers-via-vector-quantization.md)**  
  実装：[✓](https://github.com/transformer-vq/transformer_vq) ・ リポジトリ内被引用：2  
  基本の着想は、過去の鍵ベクトルを学習可能なコードブックの少数の代表ベクトルへ量子化すると、異なるトークン位置でも同じコードを持つ鍵は同じ注意得点になる、という性質にある。TPU v3での訓練処理率は同規模の二次注意モデルと比べ、系列長8192で3倍超、32768で12倍超となり、131072トークンまで大きな処理率低下なく動作した。

- **2023-09 · [Pruning Large Language Models via Accuracy Predictor](2023-2309.09507-pruning-large-language-models-via-accuracy-predictor.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  大規模言語モデルの枝刈りを「どの重みを削るか」だけでなく「どの層を何割削るか」という探索問題として扱い、少数の実測品質から決定木型予測器を学習する。推論速度の測定ではなく、圧縮率とタスク品質の交換条件を改善する研究である。

- **2023-06 · [Block-State Transformers](2023-2306.09539-block-state-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  GPUで測った層単体の順方向計算は、ブロック再帰方式に対して単一頭BSTが6〜11倍速い。

- **2023-10 · [Look-Up mAI GeMM: Increasing AI GeMMs Performance by Nearly 2.5x via msGeMM](2023-2310.06178-look-up-mai-gemm-increasing-ai-gemms-performance-by-nearly-2-5x-via-msge.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  重みを4ビット整数へ量子化すれば、各重みが取れる値は16種類に限られる。約2.5倍という代表値を、現在のGPUにおける推論遅延やトークン生成速度の改善と解釈してはならない。

- **2023-10 · [A Dynamic LLM-Powered Agent Network for Task-Oriented Agent Collaboration](2023-2310.02170-a-dynamic-llm-powered-agent-network-for-task-oriented-agent-collaboratio.md)**  
  実装：[✓](https://github.com/SALT-NLP/DyLAN) ・ リポジトリ内被引用：1  
  複数の大規模言語モデル（large language モデル; LLM）エージェントを協調させる方式では、役割の異なる複数回答を相互評価できる一方、人数と通信構造を全タスクで固定すると、不要なモデル呼出しが増え、専門外のエージェントが有用な回答へ干渉する。

- **2023-07 · [Beyond Classical Attention: Quantum Attention for Scalable Computation](2023-2307.08045-beyond-classical-attention-quantum-attention-for-scalable-computation.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文は、長い入力系列に対する自己注意で全ての問い合わせと鍵の内積を計算する代わりに、閾値を超える少数の大きな内積だけを量子探索で発見する理論的な方法を提案する。

- **2023-02 · [With Shared Microexponents, A Little Shifting Goes a Long Way](2023-2302.08007-with-shared-microexponents-a-little-shifting-goes-a-long-way.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Rouhaniらは、ブロックデータ表現（Block Data Representation; BDR）という共通の設計枠を用意し、ブロックサイズ、尺度の階層、尺度を保存するビット数、各要素の仮数幅を変えて比較した。

### 5年前（2021-11〜2022-10）

- **2022-05 · [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](2022-2205.14135-flashattention.md)**  
  実装：[✓](https://github.com/HazyResearch/flash-attention) ・ リポジトリ内被引用：298  
  タイル化、オンラインsoftmax、逆伝播時再計算により二次元注意行列の高帯域メモリ往復を避ける厳密注意カーネル。

- **2022-06 · [DeepSpeed Inference: Enabling Efficient Inference of Transformer Models at Unprecedented Scale](2022-2207.00032-deepspeed-inference-enabling-efficient-inference-of-transformer-models-at-unprecedented-scale.md)**  
  実装：[✓](https://github.com/microsoft/DeepSpeed) ・ リポジトリ内被引用：94  
  単一の量子化方式や一種類の並列化を万能解とせず、GPU内実行向けのDeepSpeed Transformerと、CPU主記憶・NVMeを使うZeRO-Inferenceという二つの経路を組み合わせる。

- **2022-06 · [ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers](2022-2206.01861-zeroquant-efficient-and-affordable-post-training-quantization-for-large-.md)**  
  実装：[✓](https://github.com/microsoft/DeepSpeed) ・ リポジトリ内被引用：53  
  大規模言語モデルの量子化では、重みを16ビットから8ビットへ減らすだけでメモリ転送量は小さくなる。INT8では追加の学習や校正なしでBERT・GPT系の品質をほぼ保ち、NVIDIA A100上のBERT-baseで最大5.19倍、GPT-3 350Mで4.16倍の速度向上を示した。

- **2021-12 · [GLaM: Efficient Scaling of Language Models with Mixture-of-Experts](2021-2112.06905-glam-efficient-scaling-of-language-models-with-mixture-of-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：36  
  総パラメータ数と一トークンで実際に使用するパラメータ数を分離することで、巨大な容量を持ちながら密なモデルほどの計算を必要としない。最大構成GLaM（64B/64E）は総1.2兆パラメータを持つが、トークン当たり活性化するのは約96.6B、全体の約8%である。

- **2021-12 · [Self-attention Does Not Need O(n^2) Memory](2021-2112.05682-self-attention-does-not-need-o-n-2-memory.md)**  
  実装：[✓](https://github.com/google-research/google-research/tree/master/memory_efficient_attention) ・ リポジトリ内被引用：20  
  ソフトマックス注意の最大値、指数和、値の重み付き和を逐次更新し、全注意行列を実体化せず同じ数学的出力を得る。理論上の省メモリ算法と、TPU向けのチャンク並列実装、再計算を使った微分を示す。

- **2022-06 · [Long Range Language Modeling via Gated State Spaces](2022-2206.13947-long-range-language-modeling-via-gated-state-spaces.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  対象：自己回帰言語モデルの状態空間層をTPUで効率よく学習し、学習系列長を超える長距離依存を扱う研究。学習速度と推論速度の主張を分けて読む。一次論文は2022年7月2日改訂の第3版。

- **2022-02 · [Transformer Quality in Linear Time](2022-2202.10447-transformer-quality-in-linear-time.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  FLASHは、注意計算を系列長に対して線形に近づける方式が、理論計算量を減らしても実機で速くならず、強いTransformerを比較対象にすると品質が落ちるという問題に取り組む。

- **2021-12 · [LongT5: Efficient Text-To-Text Transformer for Long Sequences](2021-2112.07916-longt5-efficient-text-to-text-transformer-for-long-sequences.md)**  
  実装：[✓](https://github.com/google-research/longt5) ・ リポジトリ内被引用：7  
  T5のエンコーダを長文向けに置き換え、各層でブロック集約した大域トークンを一時的に作る注意機構を提案する。重要文生成による事前学習と組み合わせ、要約・質問応答で長い入力の情報を利用する。論文の主な評価はモデル品質と学習時の計算費用であり、デコード専用の推論サービング実験とは区別する。

- **2022-08 · [Unified Normalization for Accelerating and Stabilizing Transformers](2022-2208.01313-unified-normalization-for-accelerating-and-stabilizing-transformers.md)**  
  実装：[✓](https://github.com/hikvision-research/Unified-Normalization) ・ リポジトリ内被引用：2  
  UNはTransformerのoffline normalizationを、活性値/勾配統計の平滑化と適応型 outlier除去で安定化し、固定統計を線形層へ融合してSwin-Tで31.2% スループット向上を示す。

### 6年前（2020-11〜2021-10）

- **2021-01 · [I-BERT: Integer-only BERT Quantization](2021-2101.01321-i-bert-integer-only-bert-quantization.md)**  
  実装：[✓](https://github.com/kssteven418/i-bert) ・ リポジトリ内被引用：13  
  Transformerの重みと行列積を8ビット整数へ量子化しても、推論全体が整数だけで実行できるとは限らない。Tesla T4上の予備的な整数カーネル実装では、FP32比で2.4～4.0倍の推論高速化を報告する。

- **2021-09 · [Block Pruning For Faster Transformers](2021-2109.04838-block-pruning-for-faster-transformers.md)**  
  実装：[✓](https://github.com/huggingface/nn_pruning) ・ リポジトリ内被引用：7  
  Block Pruningは移動量に基づく枝刈り（movement 枝刈り）を重みブロック単位へ拡張し、フィードフォワード層の次元や注意ヘッドを構造的に除去できる形へ誘導する。

- **2021-02 · [Nyströmformer: A Nyström-Based Algorithm for Approximating Self-Attention](2021-2102.03902-nystr-mformer-a-nystr-m-based-algorithm-for-approximating-self-attention.md)**  
  実装：[✓](https://github.com/mlpen/Nystromformer) ・ リポジトリ内被引用：5  
  標準的な自己注意（self-注意機構）は、系列長nのすべてのトークン対の類似度を計算するため、n×nの注意行列を作る。系列が2倍になると注意行列の要素数は4倍となり、長い文書を扱うTransformerでは計算量とメモリ容量が問題になる。

- **2020-12 · [MiniLMv2: Multi-Head Self-Attention Relation Distillation for Compressing Pretrained Transformers](2020-2012.15828-minilmv2-multi-head-self-attention-relation-distillation-for-compressing.md)**  
  実装：[✓](https://github.com/microsoft/unilm/tree/master/minilm) ・ リポジトリ内被引用：5  
  教師と生徒の注意頭数を揃える制約を外し、Query・Key・Valueのトークン間関係を共通の「関係頭」で比較する。推論速度の改善は蒸留後の小型モデルによるもので、実行時に教師を参照する方式ではない。

### 7年前（2019-11〜2020-10）

- **2020-01 · [Reformer: The Efficient Transformer](2020-2001.04451-reformer-the-efficient-transformer.md)**  
  実装：[✓](https://github.com/google/trax/tree/master/trax/models/reformer) ・ リポジトリ内被引用：61  
  Reformerは、長系列Transformerで支配的になる二つの資源問題を別々の機構で解く。

- **2020-09 · [Rethinking Attention with Performers](2020-2009.14794-rethinking-attention-with-performers.md)**  
  実装：[✓](https://github.com/google-research/google-research/tree/master/performer) ・ リポジトリ内被引用：41  
  Performerは、通常の全ランクのソフトマックス注意を正の直交ランダム特徴で近似するFAVOR+を提案し、注意行列を明示的に保持しない線形時間・線形空間の実行を可能にする。

- **2020-09 · [TernaryBERT: Distillation-aware Ultra-low Bit BERT](2020-2009.12812-ternarybert-distillation-aware-ultra-low-bit-bert.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  TernaryBERTは、自然言語理解向けのBERTを極低ビットで実行可能な重み表現へ圧縮し、精度低下を知識蒸留（Knowledge Distillation）で抑える手法である。これにより重み2ビット・埋め込み2ビット・活性値8ビットの代表構成で、BERTの保存サイズを418MBから28MBへ減らす。

- **2020-05 · [GOBO: Quantizing Attention-Based NLP Models for Low Latency and Energy Efficient Inference](2020-2005.03842-gobo-quantizing-attention-based-nlp-models-for-low-latency-and-energy-ef.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  GOBOは、BERTなどの注意機構を使う自然言語処理モデルの重みを、学習後に大幅に圧縮する手法である。重みの約99.9%を少数の代表値への索引で表し、残る約0.1%の外れ値だけを元の32ビット浮動小数点のまま保持する。

- **2020-04 · [FastBERT: a Self-distilling BERT with Adaptive Inference Time](2020-2004.02178-fastbert-a-self-distilling-bert-with-adaptive-inference-time.md)**  
  実装：[✓](https://github.com/autoliuweijie/FastBERT) ・ リポジトリ内被引用：12  
  この設計は文章生成の各トークンを省略する方式ではなく、主に文章分類と文対照合に適用される。例えば中国語THUCNewsでは閾値0.1で分類精度96.71%を維持しつつ計算量が約6.05分の1、英語DBpediaでは同閾値で99.31%から99.28%への微小な低下と引き換えに約10.57分の1となる。

- **2020-04 · [DeeBERT: Dynamic Early Exiting for Accelerating BERT Inference](2020-2004.12993-deebert-dynamic-early-exiting-for-accelerating-bert-inference.md)**  
  実装：[✓](https://github.com/castorini/DeeBERT) ・ リポジトリ内被引用：12  
  DeeBERTは、BERT系の分類モデルで入力ごとに必要なTransformer層数が異なることを利用し、浅い層ですでに十分確信度の高い予測が得られた例を途中で返す動的早期終了（動的 early exiting）方式である。

- **2019-11 · [Blockwise Self-Attention for Long Document Understanding](2019-1911.02972-blockwise-self-attention-for-long-document-understanding.md)**  
  実装：[✓](https://github.com/xptree/BlockBERT) ・ リポジトリ内被引用：9  
  BlockBERTは、長い文書をBERT型の双方向符号化器へ入力するとき、通常の自己注意が系列長の二乗に比例する注意得点を作る問題を、ブロック単位で規則的に疎化した注意によって緩和する。単に遠方のトークンを切り捨てるのではなく、各注意ヘッドへ異なるブロック置換を割り当てることで、近傍情報を読むヘッドと離れたブロックを読むヘッドを共存させる。

- **2020-07 · [FTRANS: Energy-Efficient Acceleration of Transformers using FPGA](2020-2007.08563-ftrans-energy-efficient-acceleration-of-transformers-using-fpga.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  FTRANSは、Transformerの重み行列を拡張ブロック循環行列（enhanced block-circulant matrix; BCM）に置き換える構造化圧縮と、その圧縮表現を直接計算する再構成可能論理回路（field-programmable gate array; FPGA）の専用構成を同時設計した研究である。

- **2020-06 · [BERT Loses Patience: Fast and Robust Inference with Early Exit](2020-2006.04152-bert-loses-patience-fast-and-robust-inference-with-early-exit.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  浅い層で正しい分類がほぼ確定している入力にも後段層の計算を続けるため、不要な遅延が生じる。従来の早期終了方式は中間分類器の最大確率やエントロピーなど、一つの層での自信の強さを停止信号にすることが多かった。

- **2020-06 · [Dynamic Tensor Rematerialization](2020-2006.09616-dynamic-tensor-rematerialization.md)**  
  実装：[✓](https://github.com/uwsampl/dtr-prototype) ・ リポジトリ内被引用：2  
  活性チェックポイントは一部の活性だけを保存し、捨てた活性を逆伝播の必要時に再計算することで、メモリと演算量を交換する。

### 8年前（2018-11〜2019-10）

- **2019-04 · [Generating Long Sequences with Sparse Transformers](2019-1904.10509-generating-long-sequences-with-sparse-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：103  
  全結合の自己注意を局所窓と周期・固定要約位置へ因数分解して O(n√n) 化し、再計算と疎GPUカーネルを併用して数万〜100万要素の生成を可能にしたSparse Transformer。

- **2018-11 · [ブロック並列 Parallel Decoding for Deep Autoregressive Models](2018-1811.03115-blockwise-parallel-decoding-for-deep-autoregressive-models.md)**  
  実装：✓ ・ リポジトリ内被引用：30  
  ブロック並列 Parallel Decodingは、この逐次性そのものを完全に捨てるのではなく、複数の将来位置を一度に予測し、元の自己回帰スコアリングモデルで「通常の貪欲復号なら同じトークンを選んだか」を並列検証する。

- **2019-09 · [Reducing Transformer Depth on Demand with Structured Dropout](2019-1909.11556-reducing-transformer-depth-on-demand-with-structured-dropout.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  深いTransformerは学習時に層をすべて使用する前提で最適化されるため、学習後に連続した層を削ると、残った層が想定しない中間表現を受け取り品質が悪化する。深度ごとに新しいモデルを一から学習したり知識蒸留を繰り返したりする方法では、必要な配備構成が増えるほど学習費用が増える。深度削減は品質低下を完全に取り除くわけではない。

- **2019-05 · [Are Sixteen Heads Really Better than One?](2019-1905.10650-are-sixteen-heads-really-better-than-one.md)**  
  実装：[✓](https://github.com/pmichel31415/are-16-heads-really-better-than-1) ・ リポジトリ内被引用：21  
  Michelらは、学習済みの翻訳用TransformerとBERTの各注意ヘッドを無効化して、品質の変化、ヘッド重要度の推定、構造的な枝刈り後の推論速度を実験した。WMT14英仏翻訳のTransformerでは全ヘッドの約20%、MultiNLIに微調整したBERTでは約40%を重要度順に削っても顕著な品質低下が生じなかった。

- **2019-09 · [Q-BERT: Hessian Based Ultra Low Precision Quantization of BERT](2019-1909.05840-q-bert-hessian-based-ultra-low-precision-quantization-of-bert.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  Q-BERTは、BERTの各層へ同じビット数を割り当てる均一量子化ではなく、損失関数の二階微分から層ごとの誤差感度を推定し、敏感な層へ高い精度を残す混合精度量子化手法である。論文はSST-2、MNLI、CoNLL-03、SQuADの四課題で、重みの最大13倍圧縮、埋め込みと活性値の最大4倍圧縮を報告し、強圧縮でも性能低下を最大2.3%以内に抑えたと説明する。

- **2019-05 · [Analyzing Multi-Head Self-Attention: Specialized Heads Do the Heavy Lifting, the Rest Can Be Pruned](2019-1905.09418-analyzing-multi-head-self-attention-specialized-heads-do-the-heavy-lifti.md)**  
  実装：[✓](https://github.com/lena-voita/the-story-of-heads) ・ リポジトリ内被引用：19  
  本論文は、翻訳用Transformerの多頭注意機構において、各ヘッドの計算が同じだけ必要なのかを、予測への寄与と実際の削除耐性の両側面から調べた研究である。一方、これは2019年の機械翻訳Transformerにおける品質評価であり、現代の生成専用LLMで実際に同じ割合の実行時間や鍵・値キャッシュ容量を削減できると証明した結果ではない。

- **2019-05 · [Adaptive Attention Span in Transformers](2019-1905.07799-adaptive-attention-span-in-transformers.md)**  
  実装：[✓](https://github.com/facebookresearch/adaptive-span) ・ リポジトリ内被引用：11  
  自己回帰型Transformerの注意機構は、過去の一定幅のトークンを参照して次のトークンを予測する。

- **2019-04 · [Mask-Predict: Parallel Decoding of Conditional Masked Language Models](2019-1904.09324-mask-predict-parallel-decoding-of-conditional-masked-language-models.md)**  
  実装：[✓](https://github.com/facebookresearch/Mask-Predict) ・ リポジトリ内被引用：9  
  翻訳文の長さを最初に予測し、最初の反復では全位置を同時に予測する。2019年の機械翻訳実験では、WMT14英語→ドイツ語において基礎CMLMの10反復が27.03 BLEU、同等規模の自己回帰Transformerが27.74 BLEUとなった。

- **2019-10 · [Q8BERT: Quantized 8Bit BERT](2019-1910.06188-q8bert-quantized-8bit-bert.md)**  
  実装：[✓](https://github.com/NervanaSystems/nlp-architect) ・ リポジトリ内被引用：8  
  Q8BERTは、事前学習済みBERTを特定の自然言語処理課題へ微調整する段階で量子化誤差を模擬し、推論時の8ビット整数演算へ適応させる研究である。著者はBERTの重みの99%以上を占める埋め込み層と全結合層を8ビット整数へ対応させ、残りの数値的に敏感な演算は32ビット浮動小数点に残す。

### 9年前（2017-11〜2018-10）

- **2018-06 · [PipeDream: Generalized Pipeline Parallelism for DNN Training](2018-1806.03377-pipedream-generalized-pipeline-parallelism-for-dnn-training.md)**  
  実装：✓ ・ リポジトリ内被引用：29  
  DNNの連続層を複数GPUへ割り当て、異なるミニバッチの順伝播と逆伝播を交互に重ねる。層の計算・通信費用を測って段を自動分割し、順伝播時の重み版を逆伝播まで保持することで非同期実行の整合性を保つ。

- **2018-02 · [Deterministic Non-Autoregressive Neural Sequence Modeling by Iterative Refinement](2018-1802.06901-deterministic-non-autoregressive-neural-sequence-modeling-by-iterative-r.md)**  
  実装：[✓](https://github.com/nyu-dl/dl4mt-nonauto) ・ リポジトリ内被引用：7  
  本研究は、出力系列を左から右へ一語ずつ生成する自己回帰モデルの逐次依存を取り除き、系列全体を同時に予測した後、少数回の反復で文章を修正する決定論的な非自己回帰系列生成法を提案する。

### 10年前（2016-11〜2017-10）

- **2017-01 · [Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](2017-1701.06538-outrageously-large-neural-networks-the-sparsely-gated-mixture-of-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：155  
  本論文は、ニューラルネットワークの総パラメータ数を増やすと各入力での計算量も増えるという密なモデルの制約を、入力ごとに一部の専門家だけを実行する条件付き計算によって緩和した基礎研究である。モデルの総容量を大きくしても、活性化する専門家数を固定すれば入力一件あたりの専門家演算量はほぼ一定にできる。ただし専門家を増やすだけでは高速にならない。
<!-- survey:auto:end -->
