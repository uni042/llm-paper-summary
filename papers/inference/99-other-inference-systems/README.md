# Other Inference Systems

推論効率化を主目的とするが、現時点では他の系統へ自然に入らず、**独立系統を作るほど同種研究がまだ集まっていない手法**を置く。ここに論文が増えて共通した問題設定・主要技術・評価軸が見えてきた場合は、新しい系統へ分割する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（786本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-01 · [DART: Diffusion-Inspired Speculative Decoding for Fast LLM Inference](2026-2601.19278-dart-diffusion-inspired-speculative-decoding-for-fast-llm-inference.md)**  
  実装：[✓](https://github.com/fvliang/DART) ・ リポジトリ内被引用：13  
  対象LLM特徴から未来ロジットを1回で並列予測しN-gram木刈り込みを行い、EAGLE3より平均約30%高い投機デコード高速化を得る。

- **2026-02 · [Fast KV Compaction via Attention Matching](2026-2602.16284-fast-kv-compaction-via-attention-matching.md)**  
  実装：[✓](https://github.com/adamzweiger/compaction) ・ リポジトリ内被引用：9  
  長文脈のKVキャッシュを、将来の問い合わせで元の注意挙動を再現する短い鍵・値・バイアスへ置き換える。参照問い合わせの生成、鍵選択、非負最小二乗による注意質量合わせ、値の最小二乗推定を組み合わせる。

- **2026-01 · [Double: Breaking the Acceleration Limit via Double Retrieval Speculative Parallelism](2026-2601.05524-double-breaking-the-acceleration-limit-via-double-retrieval-speculative-.md)**  
  実装：[✓](https://github.com/Sylvan820/Double1) ・ リポジトリ内被引用：8  
  Doubleは、並列投機的復号（Parallel 投機的復号; PSD）における二つの性能制約を同時に解く。この方式は、ドラフト用の追加学習を必要としない。原著の8基のNVIDIA A100 80GBによる実験では、LLaMA3.3-70BのHumanEvalで通常のターゲット推論に対して5.33倍、Qwen3-32Bでは2.84倍の実時間高速化を示す。

- **2026-02 · [P-EAGLE: Parallel-Drafting EAGLE with Scalable Training](2026-2602.01469-p-eagle-parallel-drafting-eagle-with-scalable-training.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  投機的復号は軽いドラフトモデルが先に複数トークンを提案し、大きな対象モデルがまとめて検証することで、対象モデルの重みを読む回数を減らす。vLLMでの実測では、GPT-OSS 20B、120B、Qwen3-Coder 30Bに対し、自己回帰EAGLE-3比で代表的に1.10〜1.36倍の生成処理量改善を報告する。

- **2026-01 · [Fast KVzip: Efficient and Accurate LLM Inference with Gated KV Eviction](2026-2601.17668-fast-kvzip-efficient-and-accurate-llm-inference-with-gated-kv-eviction.md)**  
  実装：[✓](https://github.com/Janghyun1230/FastKVzip) ・ リポジトリ内被引用：7  
  長文脈の言語モデルは、生成のたびに過去の鍵・値（KV）を参照するため、文脈が長くなるとキャッシュがGPUメモリを圧迫する。重要でないKVを削除する方法は容量を減らせるが、何を消すかを決めるために過去の注意を再計算すると、圧縮器自体の費用が大きくなる。

- **2025-12 · [Recursive Language Models](2025-2512.24601-recursive-language-models.md)**  
  実装：[✓](https://github.com/alexzhang13/rlm) ・ リポジトリ内被引用：6  
  再帰型言語モデル（Recursive Language モデル; RLM）は、長い入力を大規模言語モデルの注意窓へ丸ごと入れる代わりに、持続的なプログラム実行環境の変数として保存し、モデル自身がコードを生成して入力の必要箇所を調査・分割・変換する推論方式である。

- **2026-07 · [FlashAccel: Leveraging High-Bandwidth Flash (HBF) for High-Throughput LLM Inference](2026-2607.10186-flashaccel-high-bandwidth-flash-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  HBM級帯域・大容量の高帯域フラッシュをGPUへ統合し、SRAM先読み、重み/KV専用配置、KVの選択的HBM複製、追記型永続管理を協調させて、モデル重みとKVキャッシュをフラッシュ上で直接高並列アクセスする推論アクセラレータ。

- **2026-01 · [Ministral 3](2026-2601.08584-ministral-3.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  著者らはこの方式を段階蒸留（Cascade Distillation）と呼ぶ。したがって「全評価項目で教師と同等」ではない。

- **2026-06 · [CAT-Q: Cost-efficient and Accurate Ternary Quantization for LLMs](2026-2606.26650-cat-q-cost-efficient-and-accurate-ternary-quantization-for-llms.md)**  
  実装：[✓](https://github.com/IntelChina-AI/BitTern) ・ リポジトリ内被引用：4  
  CAT-Qは、高精度で事前学習された大規模言語モデル（LLM）を、重みが負一・零・正一の三値しか取らない形式へ変換する学習後量子化（Post-学習 量子化; PTQ）方式である。235Bモデルの三値化にはA100 80GBを8枚使って最大60時間を要する。

- **2026-03 · [PIMphony: Overcoming Bandwidth and Capacity Inefficiency in PIM-Based Long-Context LLM Inference System](2026-ff07d7af9733-pimphony-overcoming-bandwidth-and-capacity-inefficiency-in-pim-based-long-context-llm-inference-system.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  長文脈のLLMがトークンを一つずつ生成するとき、注意機構はこれまでの各トークンに対応する鍵・値キャッシュ（KV キャッシュ）を読み返す。動的PIMアクセス（動的 PIM Access; DPA）は生成中のトークン数に応じたループとアドレス変換を使い、KVキャッシュを実行時に1MB単位で追加する。

- **2026-02 · [RelayCaching：協調LLMの生成KVキャッシュ再利用](2026-2603.13289-relaycaching-accelerating-llm-collaboration-via-decoding-kv-cache-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  前段エージェントのデコードKVを後段プリフィルへ渡し、位置補正と中間層・重要トークンだけの疎な再計算で80%以上を再利用し、TTFTを最大4.7倍短縮する。

- **2025-12 · [JANUS: Disaggregating Attention and Experts for Scalable MoE Inference](2025-2512.13525-janus-disaggregating-attention-and-experts-for-scalable-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  JANUSは、専門家混合（Mixture-of-Experts、MoE）モデルのオンライン推論を、注意機構と専門家層を別々のGPU群へ配置して独立に伸縮するシステムである。

- **2026-06 · [TWLA: Achieving Ternary Weights and Low-Bit Activations for LLMs via Post-Training Quantization](2026-2606.13054-twla-achieving-ternary-weights-and-low-bit-activations-for-llms-via-post.md)**  
  実装：[✓](https://github.com/Kishon-zzx/TWLA) ・ リポジトリ内被引用：3  
  TWLA（Ternarized Weights and Low-bit Activations）は、学習済み大規模言語モデル（LLM）の重みを三値へ圧縮し、さらに活性値を平均4ビット級へ下げる事後学習量子化（Post-学習 量子化; PTQ）の研究である。ここではFP16の23.70トークン/秒に対しTWLAが86.35トークン/秒を示した。

- **2026-04 · [DORA: A Scalable Asynchronous Reinforcement Learning System for Language Model Training](2026-2604.26256-dora-a-scalable-asynchronous-reinforcement-learning-system-for-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  DORAは、大規模言語モデル（Large Language モデル; LLM）の強化学習（Reinforcement Learning; RL）による後学習を、生成する応答の長さが大きく偏る状況でも効率よく進めるシステムである。

- **2026-02 · [QuantVLA: Scale-Calibrated Post-Training Quantization for Vision-Language-Action Models](2026-2602.20309-quantvla-scale-calibrated-post-training-quantization-for-vision-language.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  視覚・言語・行動モデル（vision-language-action モデル; VLA）は、画像と自然言語の指示を統合し、ロボットの連続した操作を生成する。

- **2026-02 · [ICaRus: Identical Cache Reuse for Efficient Multi Model Inference](2026-2603.13281-icarus-identical-cache-reuse-for-efficient-multi-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  複数の専門言語モデルを順番に呼び出すエージェント型推論では、同じシステム指示、会話履歴、検索資料を何度も入力する。LLaMA-3.1-8Bを使うReAct型の8エージェント構成では、通常のモデル別KV方式に対して95パーセンタイル遅延（P95、遅い側5%に入る境界）を最大11.1倍短縮し、最大スループットを3.8倍に高めた。

- **2026-01 · [SWE-Pruner: Self-Adaptive Context Pruning for Coding Agents](2026-2601.16746-swe-pruner-self-adaptive-context-pruning-for-coding-agents.md)**  
  実装：[✓](https://github.com/Ayanami1314/swe-pruner) ・ リポジトリ内被引用：3  
  コード編集エージェントは、問題を理解して修正するまでに何度もファイルを読み、検索し、テストを実行する。cat や grep が返した大量のコードや周辺行を、そのまま大規模言語モデル（LLM）へ渡すと、文脈窓を圧迫し、API料金と推論時間を増やす。しかも一度読み込んだ不要なコードは対話履歴に残り、次の推論でも繰り返し処理される。

- **2026-01 · [Native LLM and MLLM Inference at Scale on Apple Silicon](2026-2601.19139-native-llm-and-mllm-inference-at-scale-on-apple-silicon.md)**  
  実装：[✓](https://github.com/waybarrios/vllm-mlx) ・ リポジトリ内被引用：3  
  Apple SiliconはCPUとGPUが同じ物理メモリを利用する統合メモリ構成を持つため、一般的な独立GPU環境とはモデル重みや中間状態の管理条件が異なる。

- **2026-01 · [MELINOE: Fine-Tuning Enables Memory-Efficient Inference for Mixture-of-Experts Models](2026-2602.11192-melinoe-fine-tuning-enables-memory-efficient-inference-for-mixture-of-ex.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  MELINOEは、混合専門家モデル（MoE）の専門家重みをCPUへ退避する推論環境で、モデル自身の専門家選択を少数の再利用しやすい専門家へ寄せる手法である。著者らはOLMoE、Phi-3.5-MoE、Mixtral-8x7Bを対象に、H100、A100、RTX 4090のメモリ制限環境で評価した。

- **2026-01 · [Latent Space Communication via K-V Cache Alignment](2026-2601.06123-latent-space-communication-via-k-v-cache-alignment.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  モデル固有のKVキャッシュを、共有潜在空間への入出力変換器を介して交換する。単に同じ数値へ復元するのではなく、受信側が後続トークンを正しく予測できる状態を学ぶことで、異なる言語モデル間の内部状態共有を可能にする。

- **2025-12 · [Trellis: Learning to Compress Key-Value Memory in Attention Models](2025-2512.23852-trellis-learning-to-compress-key-value-memory-in-attention-models.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  通常の自己注意では、生成済みの全トークンに対する鍵ベクトルと値ベクトルを保持し、次のトークンでそれらを参照する。提案は、鍵を圧縮して中間表現を得る第1段と、値を圧縮して出力を得る第2段からなる。

- **2025-11 · [DartQuant: Efficient Rotational Distribution Calibration for LLM Quantization](2025-2511.04063-dartquant-efficient-rotational-distribution-calibration-for-llm-quantiza.md)**  
  実装：[✓](https://github.com/CAS-CLab/DartQuant) ・ リポジトリ内被引用：3  
  DartQuantは、大規模言語モデル（LLM）の低ビット量子化で問題になる活性値の外れ値を、直交回転行列の校正によって緩和する方法である。時間比は約47倍、メモリ比は約10倍である。

- **2026-07 · [Trees from Marginals: Autoregressive drafting with factorized priors](2026-2607.06763-trees-from-marginals-autoregressive-drafting-with-factorized-priors.md)**  
  実装：[✓](https://github.com/trymirai/sglang) ・ リポジトリ内被引用：2  
  Trees from Marginals（DFlash-TfM）は、未来の複数トークンを並列に予測する周辺分布型の下書き器DFlashと、直前に選択した下書きトークンに条件付ける小型自己回帰器Weaverを接続した投機的復号方式である。

- **2026-07 · [Read As Human: Compressing Context via Parallelizable Close Reading and Skimming](2026-2602.01840-read-as-human-compressing-context-via-parallelizable-close-reading-and-s.md)**  
  実装：[✓](https://github.com/Twilightaaa/RAM) ・ リポジトリ内被引用：2  
  入力文脈圧縮には、不要な語を削る方式と、文章を連続ベクトルへ変換する方式がある。Qwen3-4Bでの4倍圧縮時、NaturalQAの完全一致率は66.59、2WikiMQAは50.39であり、8倍圧縮時にはそれぞれ61.09、40.24となる。

- **2026-06 · [Models Take Notes at Prefill: KV Cache Can Be Editable and Composable](2026-2606.17107-models-take-notes-at-prefill-kv-cache-can-be-editable-and-composable.md)**  
  実装：[✓](https://github.com/19PINE-AI/programmable-kv) ・ リポジトリ内被引用：2  
  プリフィル済みKVキャッシュを結論メモとして捉え、追記訂正による編集とRoPE再配置による部品合成で再プリフィルを回避する。

- **2026-06 · [MiniPIC: Flexible Position-Independent Caching in <100LOC](2026-2606.13126-minipic-flexible-position-independent-caching-in-100loc.md)**  
  実装：[✓](https://github.com/IBM/vllm) ・ リポジトリ内被引用：2  
  例えばシステム指示や文書の並び順が異なる二つの要求は、同じ文書の事前充填を繰り返すことになる。H100単体・2Wikiの12,576サンプルでは、文書の事前充填と最終要求を交互に投入する方式により48.01サンプル/秒を達成し、通常vLLMの32.21サンプル/秒に対して49%増加した。

- **2026-05 · [SYMPHONY: Enabling Compute-Memory Disaggregation in LLM Serving Systems](2026-0fd53670e945-symphony-enabling-compute-memory-disaggregation-in-llm-serving-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  将来要求の助言信号でKVキャッシュを事前移動し、層優先度と協調HBM管理で不確実性を吸収して計算・メモリ分離を低遅延化する。

- **2026-05 · [An Efficient Hybrid Sparse Attention with CPU-GPU Parallelism for Long-Context Inference](2026-2605.07719-an-efficient-hybrid-sparse-attention-with-cpu-gpu-parallelism-for-long-context-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  CPU常駐KV向けに出力寄与ベース予算配分とCPU・GPU協調疎注意を統合し、長文復号を最大3.7倍高速化する。

- **2026-03 · [DAPD: Dependency-Aware Parallel Decoding via Attention for Diffusion LLMs](2026-2603.12996-dapd-dependency-aware-parallel-decoding-via-attention-for-diffusion-llms.md)**  
  実装：[✓](https://github.com/quasar529/DAPD) ・ リポジトリ内被引用：2  
  またLLaDAの主表では比較方式とDAPDのブロック構成が異なるため、速度差の全てを位置選択アルゴリズム単独の効果とみなせない。

- **2026-02 · [FlashVID: Efficient Video Large Language Models via Training-free Tree-based Spatiotemporal Token Merging](2026-2602.08024-flashvid-efficient-video-large-language-models-via-training-free-tree-ba.md)**  
  実装：[✓](https://github.com/Fanziyang-v/FlashVID) ・ リポジトリ内被引用：2  
  入力フレームが増えるとトークン列が長くなり、注意機構だけでなく全結合層の計算、鍵値キャッシュ、初回応答までの時間が増える。LLaVA-OneVisionでは、視覚トークンを10%まで減らしても四つの主要評価群の平均点58.4から57.9へと小幅な低下にとどまり、元精度の99.1%を維持した。

- **2025-12 · [Kitsune: Enabling Dataflow Execution on GPUs with Spatial Pipelines](2025-2502.18403-kitsune-enabling-dataflow-execution-on-gpus-with-spatial-pipelines.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  カーネル境界で中間テンソルが高帯域メモリへ書き戻され、次のカーネルが再び読む。さらに、一般命令主体のCTAとテンソル演算主体のCTAを同じストリーミングマルチプロセッサ（SM）へ配置できるようグリッドスケジューラを拡張する。

- **2025-12 · [HiFC: High-efficiency Flash-based KV Cache Swapping for Scaling LLM Inference](2026-f52f99f3360a-hifc-high-efficiency-flash-based-kv-cache-swapping-for-scaling-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  GPUとNVMe SSDをGDSで直結し、pSLCと順次KVブロック配置でDRAMなしのKV交換を実現し、長文脈推論の性能を保ちながら容量費用を削減する。

- **2025-12 · [DEER: Draft with Diffusion, Verify with Autoregressive Models](2025-2512.15176-deer-draft-with-diffusion-verify-with-autoregressive-models.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  DEERは、投機的復号の候補生成器を、左から右へ逐次生成する小型自己回帰モデルから、複数位置をまとめて予測できる離散拡散言語モデル（discrete diffusion language モデル）へ置き換える方式である。

- **2025-12 · [AdmTree: Compressing Lengthy Context with Adaptive Semantic Trees](2025-2512.04550-admtree-compressing-lengthy-context-with-adaptive-semantic-trees.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  AdmTreeは、長い文書を大規模言語モデル（LLM）へ入力する際、入力トークンを短い潜在表現へ圧縮しつつ、局所的な事実と文書全体の意味を両立して保持する方式である。LongBenchの評価では、Llama-2-7Bを基盤にしたAdmTreeの平均得点は44.1で、活性値 Beaconの40.1を上回った。

- **2025-11 · [From Bits to Rounds: Parallel Decoding with Exploration for Diffusion Language Models](2025-2511.21103-from-bits-to-rounds-parallel-decoding-with-exploration-for-diffusion-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  通常の自己回帰モデルとは異なり、左から一語ずつ確定する必要がないため、並列復号によって生成の反復回数を減らせる可能性がある。実験ではGSM8K、MATH、HumanEval、MMLU-Proを対象に、同程度の正答率で必要なモデル順伝播回数を26〜61%削減する代表結果を示す。

- **2025-11 · [FlexiCache: Leveraging Temporal Stability of Attention Heads for Efficient KV Cache Management](2025-2511.00868-flexicache-leveraging-temporal-stability-of-attention-heads-for-efficient-kv-cache-management.md)**  
  実装：[✓](https://github.com/NazmulTakbir/FlexiCache) ・ リポジトリ内被引用：2  
  重要KVページが時間的に入れ替わりやすい注意ヘッドだけ全KVをGPUへ残し、安定ヘッドは上位ページ以外をCPUへ退避・周期再昇格することで、精度を保ちながらGPUメモリを最大70%削減する。

- **2026-09 · [HBFlex: A Flexible Memory System for Bridging Fine-Grained LLM States and Coarse-Grained HBF Parallel Execution](2026-2609.18675-hbflex.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  全HBF構成でKV配置・書戻し・寿命認識GCを共同最適化し、FlashAccel比最大1.58倍、H3比最大3.30倍の平均スループット向上。

- **2026-08 · [The Ingestion Tax: Adopting File-Backed Weights in Tensor Frameworks](2026-2608.12114-the-ingestion-tax-adopting-file-backed-weights-in-tensor-frameworks.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  統合メモリのApple Silicon、CPU–GPU間の一貫性接続を持つGH200、共有主記憶を使うAMD APUなどで問題になる。この三条件が揃うと、Apple M5 Maxの単一トークン用int8行列・ベクトル積では、標準的なテンソル生成経路の53〜82 GB/sに対して、公開APIを用いた直接採用が516 GB/sを記録する。

- **2026-08 · [SSDi8: Accurate and Efficient 8-bit Quantization for State Space Duality](2026-2608.21952-ssdi8-accurate-and-efficient-8-bit-quantization-for-state-space-duality.md)**  
  実装：[✓](https://github.com/cau-hai-lab/SSDi8) ・ リポジトリ内被引用：1  
  Mamba-2の構造化状態空間双対の内部状態をINT8のまま受け渡すため、再帰計算の式を並べ替え、異なる軸の分布に合わせて量子化する方式を示す。

- **2026-08 · [FlashPrefill V2: Block-Sparse Prefill Attention for Long-Context LLM Serving](2026-2608.19758-flashprefill-v2-block-sparse-prefill-attention-for-long-context-llm-serving.md)**  
  実装：[✓](https://github.com/qhfan/FlashPrefillv2) ・ リポジトリ内被引用：1  
  平均補正付きブロック疎注意をHopper向けに再設計し、SGLangの長文事前充填を128Kで最大4.8倍高速化する。

- **2026-08 · [Bole: Efficient Tree Speculation for Hybrid-Attention Language Models](2026-2608.01651-bole-efficient-tree-speculation-for-hybrid-attention-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  再帰型線形注意の木検証を厳密閉形式で並列化し、因子化状態とhardware-aware予算をSGLangへ統合して最大4.72倍のデコード スループットを実現。

- **2026-08 · [Attend to Your Own Thoughts: Breaking the Barrier for Post-Training Quantization of Reasoning LLMs through the Lens of 1.58-Bit Quantization](2026-2608.01078-attend-to-your-own-thoughts-breaking-the-barrier-for-post-training-quant.md)**  
  実装：[✓](https://github.com/IntelChina-AI/BitTern) ・ リポジトリ内被引用：1  
  大規模言語モデルの推論では重みの転送量と記憶容量が実行費用を決める重要な要因である。16ビットの重みを4ビットへ圧縮すれば容量を減らせるが、さらに1.58ビット相当の三値表現へ落とすと、数学の途中計算やコード生成など、複数段階の推論を必要とする課題の精度が大きく失われる。

- **2026-07 · [KronQ: LLM Quantization via Kronecker-Factored Hessian](2026-2607.07964-kronq-llm-quantization-via-kronecker-factored-hessian.md)**  
  実装：[✓](https://github.com/Intelligent-Computing-Lab-Panda/KronQ) ・ リポジトリ内被引用：1  
  大規模言語モデル（large language モデル; LLM）の重みを16ビットから4ビット、3ビット、2ビットへ縮小すると、メモリ占有と重み読出し帯域を削減できる。一方、単純な丸めでは、重要なチャネルの誤差が後段へ蓄積し、特に2ビット量子化で生成品質が崩れる。

- **2026-06 · [RoPE-Aware Bit Allocation for KV-Cache Quantization](2026-2606.24033-rope-aware-bit-allocation-for-kv-cache-quantization.md)**  
  実装：[✓](https://github.com/JIA-Lab-research/blockgtq) ・ リポジトリ内被引用：1  
  回転位置埋め込みの周波数ブロックごとのエネルギーに応じて鍵キャッシュのビット幅を配分し、圧縮した鍵・値を直接読む融合注意計算で長文脈推論の容量とメモリ帯域を同時に削減する。

- **2026-06 · [Memory is Reconstructed, Not Retrieved: Graph Memory for LLM Agents](2026-2606.06036-memory-is-reconstructed-not-retrieved-graph-memory-for-llm-agents.md)**  
  実装：[✓](https://github.com/Ji-shuo/MRAgent) ・ リポジトリ内被引用：1  
  MRAgent（メモリ Reasoning 構成 for LLM Agents）は、対話記憶を「手掛かり（Cue）・関連タグ（Tag）・記憶内容（Content）」の三者関係として整理し、LLMが現在までに得た証拠に応じて次の検索操作を選ぶ能動的な記憶再構成を提案する。

- **2026-06 · [Less is MoE: Trimming Experts in Domain-Specialist Language Models](2026-2606.05538-less-is-moe-trimming-experts-in-domain-specialist-language-models.md)**  
  実装：[✓](https://github.com/HectorHHZ/Less-is-MoE) ・ リポジトリ内被引用：1  
  Less is MoEは、混合専門家モデル（Mixture of エキスパート、MoE）を圧縮する際に専門家を丸ごと削ると、一般常識の選択式問題では性能が残っても数学推論やコード生成が崩壊する原因を分析し、専門家内部の順伝播ネットワーク（FFN）中間次元を削るFisher-MoEを提案する研究である。

- **2026-06 · [Do Transformers Need Three Projections? Systematic Study of QKV Variants](2026-2606.04032-do-transformers-need-three-projections-systematic-study-of-qkv-variants.md)**  
  実装：[✓](https://github.com/anushamadan02/Do-Transformers-Need-3-Projections) ・ リポジトリ内被引用：1  
  標準的なTransformerの注意機構では、入力表現Xを三つの独立した行列で変換し、問い合わせ（Query; Q）、鍵（Key; K）、値（Value; V）を生成する。鍵と値を同一射影にすると、推論時にKだけを保持してVとしても再利用でき、標準的なQKVに比べてKVキャッシュを50%削減できる。

- **2026-05 · [Test-Time Speculation](2026-2605.09329-test-time-speculation.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号（投機的復号）は、小さく高速なドラフトモデルに複数トークンの候補を作らせ、大きな対象モデルがまとめて検証することで、対象モデルの呼び出し回数を減らす方式である。原著の実験ではDFlashを基準に受理長が平均41%、最大72%改善し、EAGLE-3を基準に平均34%、最大67%改善した。

- **2026-05 · [Move the Query, Not the Cache: Characterizing Cross-Instance Latent Attention Redistribution Across GPU Fabrics](2026-2606.01502-move-the-query-not-the-cache-characterizing-cross-instance-latent-attention-redistribution-across-gpu-fabrics.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  約1KBの問い合わせを遠隔キャッシュへ送り注意計算する方式を実H100で測定し、約3msのキャッシュ再適応より数十µsの往復が有利となる条件を閉形式化する。

- **2026-05 · [How Far Can Disaggregation Go? A Design-Space Exploration of Attention-FFN Disaggregation for Efficient MoE LLM Serving](2026-2605.28302-how-far-can-disaggregation-go-a-design-space-exploration-of-attention-ffn-disaggregation-for-efficient-moe-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  注意とMoE-FFNの演算・通信を別GPU群へ分離する価値を、負荷・モデル・SLO・ネットワークを横断して設計空間探索する。

- **2026-05 · [ConQuR: Corner Aligned Activation Quantization via Optimized Rotations for LLMs](2026-2605.10793-conqur-corner-aligned-activation-quantization-via-optimized-rotations-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  低ビット量子化では、重みだけでなく中間活性値を4ビットなどで表現できれば、行列積の計算・転送の効率化余地が増す。

- **2026-05 · [BubbleSpec: Turning Long-Tail Bubbles into Speculative Rollout Drafts for Synchronous Reinforcement Learning](2026-2605.08862-bubblespec-turning-long-tail-bubbles-into-speculative-rollout-drafts-for.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  従来の非同期化はこの待ちを減らせるが、生成時の方策と更新時の方策がずれるという別の問題を持ち込む。候補が誤っていても棄却サンプリングで目標分布へ戻すため、古い方策の出力を無条件に採用する方式とは異なる。通常のVerlと比べ、復号ステップ数は48.9～56.8%減、ロールアウト時間は30.0～45.2%減である。

- **2026-05 · [Attention Once Is All You Need: Efficient Streaming Inference with Stateful Transformers](2026-2605.13784-attention-once-is-all-you-need-efficient-streaming-inference-with-statef.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文は、金融時系列、センサ、ログのようにデータが継続的に追加され、利用者からの質問がときどき到着する用途に対し、質問の到着を待たずにデータを処理する状態保持型（Stateful）LLM推論を提案する。

- **2026-04 · [Why and When Visual Token Pruning Fails? A Study on Relevant Visual Information Shift in MLLMs Decoding](2026-2604.12358-why-and-when-visual-token-pruning-fails-a-study-on-relevant-visual-infor.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  そのうえで、生成中の注意分布が初期状態から変化した時だけ、退避しておいた視覚トークンを選び直す生成段階移動対応トークン削減（デコード-stage Shift-aware トークン 枝刈り; DSTP）を提案する。

- **2026-04 · [Stochastic KV Routing: Enabling Adaptive Depth-Wise Cache Sharing](2026-2604.22782-stochastic-kv-routing-enabling-adaptive-depth-wise-cache-sharing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  既存の削減手法の多くは「どの時刻のトークンを捨てるか」に着目するが、本研究は「どの層が独自のKVを持つ必要があるか」を問い直す。

- **2026-04 · [MiniCPM-o 4.5: Towards Real-Time Full-Duplex Omni-Modal Interaction](2026-2604.27393-minicpm-o-4-5-towards-real-time-full-duplex-omni-modal-interaction.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  従来の対話方式では、利用者の発話が終わってからモデルが考え、応答が終わるまで次の入力を十分反映できない。著者のRTX 4090測定では、vLLMのINT4条件で毎秒212.3トークン、初回トークン遅延0.58秒、使用メモリ11GBを報告する。

- **2026-04 · [HAWK: Head Importance-Aware Visual Token Pruning in Multimodal Models](2026-2604.07812-hawk-head-importance-aware-visual-token-pruning-in-multimodal-models.md)**  
  実装：[✓](https://github.com/peppery77/HAWK) ・ リポジトリ内被引用：1  
  画像の解像度や動画のフレーム数が増えると、入力長、注意計算、キー・値キャッシュの負荷が増える。視覚トークンを削減する既存方式には、画像特徴の類似性や注意得点で残すトークンを選ぶものがあるが、注意ヘッドを単純平均すると、画像理解に重要なヘッドとそうでないヘッドを同等に扱ってしまう。

- **2026-03 · [SLO-Aware Compute Resource Allocation for Prefill-Decode Disaggregated LLM Inference](2026-2603.04716-slo-aware-compute-resource-allocation-for-prefill-decode-disaggregated-l.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LLM推論の事前処理（プリフィル）と逐次生成（デコード）を分離した配備で、要求総トークン量、入力・出力長、初回トークン遅延TTFT、生成トークン間隔TPOTから必要なP/Dインスタンス数を求める方法。

- **2026-03 · [BATQuant: Outlier-resilient MXFP4 Quantization via Learnable Block-wise Optimization](2026-2603.16590-batquant-outlier-resilient-mxfp4-quantization-via-learnable-block-wise-o.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデル（LLM）や画像言語モデル（MLLM）の重み・活性化を4ビットへ量子化すれば、メモリ帯域と計算資源の負担を軽くできる可能性がある。マルチモーダル5課題の総合回復率はBF16比96.43%で、同条件のFlatQuant94.79%、GPTQ94.64%を上回る。

- **2026-03 · [ArcLight: A Lightweight LLM Inference Architecture for Many-Core CPUs](2026-2603.07770-arclight-a-lightweight-llm-inference-architecture-for-many-core-cpus.md)**  
  実装：[✓](https://github.com/OpenBMB/ArcLight) ・ リポジトリ内被引用：1  
  NUMAごとのメモリ配置、動的スレッド群、Scatter/Gather型テンソル並列を一体化し、多数コアCPUの遠隔メモリアクセス壁を避けて、192コアARM環境でllama.cpp比最大46%高い推論スループットを示す軽量CPU推論基盤。

- **2026-03 · [AgilePruner: An Empirical Study of Attention and Diversity for Adaptive Visual Token Pruning in Large Vision-Language Models](2026-2603.01236-agilepruner-an-empirical-study-of-attention-and-diversity-for-adaptive-v.md)**  
  実装：[✓](https://github.com/cvsp-lab/AgilePruner) ・ リポジトリ内被引用：1  
  従来の注意重視方式は画像符号化器のクラス・トークンが強く注目する領域を残す。LLaVA-1.5-7B、TextVQA、RTX 4090の単一GPU評価で、64個を残す設定は576個を残す基準に対して推論計算量3.14→0.48兆FLOPs、1画像遅延172→115 ms、GPUメモリ13.60→13.30 GBとなった。

- **2026-02 · [ScaleBITS: Scalable Bitwidth Search for Hardware-Aligned Mixed-Precision LLMs](2026-2602.17698-scalebits-scalable-bitwidth-search-for-hardware-aligned-mixed-precision-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデル（LLM）の重みを4ビット未満に量子化すると、同じ平均ビット数でも、どの重みを低精度にするかによって予測品質が大きく変わる。第三に、行列積のタイルと整合する64×128重みブロックへ整数ビット幅を割り当て、勾配に基づく一括更新と受理判定で全モデルの平均容量予算へ近づける。

- **2026-02 · [RAT+: Train Dense, Infer Sparse -- Recurrence Augmented Attention for Dilated Inference](2026-2602.18196-rat-train-dense-infer-sparse-recurrence-augmented-attention-for-dilated-.md)**  
  実装：[✓](https://github.com/wimh966/rat-plus) ・ リポジトリ内被引用：1  
  注意機構の推論コストを下げる方法には、局所窓だけを見る方式や、重要なトークンだけを選ぶ方式がある。D=16では密な注意に近い精度を保ち、D=64では常識推論の平均正解率が59.21%から57.46%へ下がる一方、時間混合部分の理論演算量とKV保存量を64分の1へ減らす。

- **2026-02 · [Out of the Memory Barrier: A Highly Memory Efficient Training System for LLMs with Million-Token Contexts](2026-2602.02108-out-of-the-memory-barrier-a-highly-memory-efficient-training-system-for-llms-with-million-token-contexts.md)**  
  実装：[✓](https://github.com/wenhaoli-xmu/OOMB) ・ リポジトリ内被引用：1  
  チャンク再計算・ページ化KV/勾配・非同期CPUオフロード・疎注意を統合し、Qwen2.5-7Bの4M文脈学習を単一H200で実現する。

- **2026-02 · [OmniSIFT: Modality-Asymmetric Token Compression for Efficient Omni-modal Large Language Models](2026-2602.04804-omnisift-modality-asymmetric-token-compression-for-efficient-omni-modal-.md)**  
  実装：[✓](https://github.com/dingyue772/OmniSIFT) ・ リポジトリ内被引用：1  
  動画と音声を同時に受け取る統合マルチモーダル大規模言語モデルでは、視覚エンコーダと音声エンコーダが生成したトークンを時間順に並べ、言語モデルへ渡す。著者らは20秒のクリップでも2万を超える入力トークンが生じ得ることを問題設定に挙げる。

- **2026-02 · [MoSE: Mixture of Slimmable Experts for Efficient and Adaptive Language Models](2026-2602.06154-mose-mixture-of-slimmable-experts-for-efficient-and-adaptive-language-mo.md)**  
  実装：[✓](https://github.com/tnurbek/mose) ・ リポジトリ内被引用：1  
  MoSEは、混合専門家モデル（Mixture-of-Experts; MoE）の「専門家を何個選ぶか」に加え、「選んだ各専門家を何割の中間幅で実行するか」を推論時に変える研究である。主指標は一トークン当たり浮動小数点演算量（FLOPs/トークン）と品質であり、実機処理率は補助的な検証である。

- **2026-02 · [Is Retraining-Free Enough? The Necessity of Router Calibration for Efficient MoE Compression](2026-2603.02217-is-retraining-free-enough-the-necessity-of-router-calibration-for-effici.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  しかし推論時に呼ばれない専門家も含めて大量の重みを保持する必要があり、GPUメモリの制約が厳しい。専門家を削除、低ランク編集、統合する方式はこの常駐重みを減らせるが、圧縮後の性能が元モデルより大きく落ちることがある。

- **2026-02 · [Improving Sampling for Masked Diffusion Models via Information Gain](2026-2602.18176-improving-sampling-for-masked-diffusion-models-via-information-gain.md)**  
  実装：[✓](https://github.com/yks23/Information-Gain-Sampler) ・ リポジトリ内被引用：1  
  モデルの再学習を要しない復号時のアルゴリズムである。Dream-7B-Instructで数学・コード・計画の6課題を評価した原著表2では、復号率K=2の平均正解率が53.4%、K=1で62.0%となる。

- **2026-02 · [HiFloat4 Format for Language Model Inference](2026-2602.11287-hifloat4-format-for-language-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  4ビット浮動小数点を使うとモデル容量とメモリ転送を削減できるが、4ビットの中で符号・指数・仮数をすべて表すと、精度と数値範囲の両立が難しい。そこで複数要素で尺度を共有するブロック浮動小数点（Block Floating-Point; BFP）を利用する。尺度が階層化されるため、外れ値が一部の要素だけにある場合も群全体の量子化刻みを粗くしすぎずに済む。

- **2026-02 · [FlexRank: Nested Low-Rank Knowledge Decomposition for Adaptive Model Deployment](2026-2602.02680-flexrank-nested-low-rank-knowledge-decomposition-for-adaptive-model-depl.md)**  
  実装：[✓](https://github.com/RickZack/FlexRank) ・ リポジトリ内被引用：1  
  FlexRankは、一つの事前学習済みモデルから、計算・メモリ予算に応じて大きさの異なる複数の部分モデルを切り出すための低ランク分解・学習方式である。

- **2026-02 · [Effective MoE-based LLM Compression by Exploiting Heterogeneous Inter-Group Experts Routing Frequency and Information Density](2026-2602.09316-effective-moe-based-llm-compression-by-exploiting-heterogeneous-inter-gr.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  RFID-MoEは、混合専門家（Mixture-of-Experts; MoE）型の大規模言語モデルを、事後学習の重み圧縮で小さくする研究である。論文はQwen3-235B-A22Bの総重み容量が8基のA100 40GB、合計320GBに収まらない例を挙げ、演算の疎性と保存容量の大きさが別問題であることを示す。

- **2026-02 · [Data Distribution Matters: A Data-Centric Perspective on Context Compression for Large Language Model](2026-2602.01778-data-distribution-matters-a-data-centric-perspective-on-context-compress.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長文脈の大規模言語モデル（LLM）では、入力の全トークンをそのまま処理するより、先に少数の潜在表現へ圧縮して復元器へ渡す方法が考えられる。

- **2026-01 · [Towards Compute-Aware In-Switch Computing for LLMs Tensor-Parallelism on Multi-GPU Systems](2026-161bea97e0de-towards-compute-aware-in-switch-computing-for-llms-tensor-parallelism-on-multi-gpu-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  NVLSの通信意味論をLLM計算カーネルの読み書き要求へ合わせ、スイッチ内要求マージ・GPU間TB協調・データフロー重畳でテンソル並列の通信待ちを削減する。

- **2026-01 · [The Perplexity Paradox: Why Code Compresses Better Than Math in LLM Prompts](2026-2602.15843-the-perplexity-paradox-why-code-compresses-better-than-math-in-llm-promp.md)**  
  実装：[✓](https://github.com/micoverde/taac-llm-compression) ・ リポジトリ内被引用：1  
  本研究は、大規模言語モデル（LLM）へ渡す入力文を短縮する際、言語モデルが予測しにくいトークンと、下流の課題を解くために残すべきトークンが一致するとは限らないという問題を扱う。関数署名再挿入では正答率が5.3%から39.3%へ34.0ポイント回復した。

- **2026-01 · [SyncThink: A Training-Free Strategy to Align Inference Termination with Reasoning Saturation](2026-2601.03649-syncthink-a-training-free-strategy-to-align-inference-termination-with-r.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  SyncThinkは、思考過程を明示的に生成する推論特化言語モデルに対し、追加学習なしで推論を早期終了させる復号制御方式である。

- **2026-01 · [SONIC: Segmented Optimized Nexus for Information Compression in Key-Value Caching](2026-2601.21927-sonic-segmented-optimized-nexus-for-information-compression-in-key-value.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  多ターンの対話では、過去のユーザー発話とモデル応答が蓄積するたびに鍵値キャッシュが増え、メモリ使用量と新しいトークンの注意計算が重くなる。SONICは対話のターン境界を利用し、過去の各メッセージを少数の学習可能なNexusトークンへ集約する方式である。

- **2026-01 · [SimpleMem: Efficient Lifelong Memory for LLM Agents](2026-2601.02553-simplemem-efficient-lifelong-memory-for-llm-agents.md)**  
  実装：[✓](https://github.com/aiming-lab/SimpleMem) ・ リポジトリ内被引用：1  
  SimpleMemは、書き込み時に記憶を整理して、質問時に必要な情報だけを引き出すことで、この二種類の費用を同時に抑えようとする方式である。原著のLoCoMo評価では、GPT-4.1-miniを基盤としたSimpleMemの平均F1が43.24、Mem0が34.20で、相対26.4%の改善となる。

- **2026-01 · [Residual Context Diffusion Language Models](2026-2601.22954-residual-context-diffusion-language-models.md)**  
  実装：[✓](https://github.com/yuezhouhu/residual-context-diffusion) ・ リポジトリ内被引用：1  
  マスク型拡散大規模言語モデル（dLLM）は、複数のトークン位置を同時に予測し、確信度が高い位置だけを確定しながら残りを反復更新する。SDAR-8Bでブロック長64のMATH500正答率は通常の逐次ノイズ除去（Sequential Denoising、SeqD）の64.20%から74.40%へ、AIME24は7.08%から18.75%へ改善する。

- **2026-01 · [Exploring Fine-Tuning for In-Context Retrieval and Efficient KV-Caching in Long-Context Language Models](2026-2601.18527-exploring-fine-tuning-for-in-context-retrieval-and-efficient-kv-caching-.md)**  
  実装：[✓](https://github.com/amazon-science/icr-kv-caching-long-context-llms) ・ リポジトリ内被引用：1  
  長文脈LLMの文脈長が数十万〜100万トークンに伸びても、大量の文書から正しい証拠を見つける能力が必ずしも高いとは限らない。検索拡張生成（Retrieval-Augmented Generation; RAG）は事前に関連文書を検索するため効率的だが、検索索引の構築・運用が必要である。HotpotQA単体では61.0→81.1と20.1ポイント改善した。

- **2026-01 · [Dynamic Thinking-Token Selection for Efficient Reasoning in Large Reasoning Models](2026-2601.18383-dynamic-thinking-token-selection-for-efficient-reasoning-in-large-reason.md)**  
  実装：[✓](https://github.com/Robin930/DynTS) ・ リポジトリ内被引用：1  
  DynTS（動的 Thinking-Token Selection）は、長い思考列を生成する大規模推論モデル（Large Reasoning モデル; LRM）で、最終回答に必要な思考トークンのキー・値キャッシュ（Key-Value キャッシュ; KVキャッシュ）を残し、その他を推論途中に削除する方式である。

- **2026-01 · [ContiguousKV: Accelerating LLM Prefill with Granularity-Aligned KV Cache Management](2026-2601.13631-contiguouskv-accelerating-llm-prefill-with-granularity-aligned-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  KV 枝刈りとI/Oの粒度をContiguousChunkへ統一し、二段非同期プリフェッチでSSD KV読み込みを計算と重ねてRe-プリフィルを最大3.85倍高速化する。

- **2025-12 · [More Than Bits: Multi-Envelope Double Binary Factorization for Extreme Quantization](2025-2512.24545-more-than-bits-multi-envelope-double-binary-factorization-for-extreme-qu.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデルの重みを1～1.5ビットまで圧縮すると、各重みを独立に丸める方式では振幅の情報が著しく失われ、生成品質が低下する。

- **2025-12 · [LoPA: Scaling dLLM Inference via Lookahead Parallel Decoding](2025-2512.16229-lopa-scaling-dllm-inference-via-lookahead-parallel-decoding.md)**  
  実装：[✓](https://github.com/SJTU-DENG-Lab/LoPA) ・ リポジトリ内被引用：1  
  しかし実際には、確信度が閾値を超える位置だけを確定する方式では、難しい位置が残ってしまい、1回当たり1〜3トークン程度しか進まない場合が多い。

- **2025-12 · [Learning Unmasking Policies for Diffusion Language Models](2025-2512.09106-learning-unmasking-policies-for-diffusion-language-models.md)**  
  実装：[✓](https://github.com/apple/ml-rl-dllm) ・ リポジトリ内被引用：1  
  拡散言語モデル（diffusion language モデル）は、左から右へ一語ずつ出力する自己回帰型モデルと異なり、未確定位置をマスクした系列全体を繰り返し予測し、複数位置を同じ前向き計算で確定できる。

- **2025-12 · [Hybrid Token Compression for Vision-Language Models](2025-2512.08240-hybrid-token-compression-for-vision-language-models.md)**  
  実装：[✓](https://github.com/jushengzhang/HybridToken-VLM) ・ リポジトリ内被引用：1  
  一方、離散量子化した符号だけでは姿勢・質感・細部の変化が失われやすい。一次論文v2の7種類の画像理解評価では、無圧縮モデルを上限、学習しない1トークン圧縮を下限とする正規化性能保持率が87.2%であり、連続圧縮方式VoCo-LLaMAの81.0%を上回る。

- **2025-11 · [Thinking with Drafts: Speculative Temporal Reasoning for Efficient Long Video Understanding](2025-2512.00805-thinking-with-drafts-speculative-temporal-reasoning-for-efficient-long-v.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長い動画の質問応答では、最初に少数のフレームを見て全体を把握し、必要な時間区間を細かく調べる「フレームを見ながら考える」方式が使われる。原著の観測では、動画トークンに対する注意スコアの90%以上が 10^-3 未満で、密に読み込んだフレームには冗長な情報が多い。

- **2025-11 · [Revisiting Disaggregated Large Language Model Serving for Performance and Energy Implications](2026-2601.08833-revisiting-disaggregated-large-language-model-serving-for-performance-and-energy-implications.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  公平な2-GPU基準と複数KV転送階層・DVFSでプリフィル/デコード分離を再評価し、性能・省電力の優位が条件依存であることを示す。

- **2025-11 · [Nemotron-Flash: Towards Latency-Optimal Hybrid Small Language Models](2025-2511.18890-nemotron-flash-towards-latency-optimal-hybrid-small-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GPUで1トークンずつ復号する際、層を何回順に通過するか、どの演算子が起動されるか、状態やKVをどれだけ転送するかが遅延を決める。Nemotron-Flashは、モデルの大きさよりも実際のGPU上での遅延制約を第一の設計目標とする。

- **2025-11 · [LUT-LLM: Efficient Large Language Model Inference with Memory-based Computations on FPGAs](2025-2511.06174-lut-llm-efficient-large-language-model-inference-with-memory-based-computations-on-fpgas.md)**  
  実装：[✓](https://github.com/LUT-FPGA/LUT-LLM) ・ リポジトリ内被引用：1  
  活性値・重み共同ベクトル量子化で線形層を2次元表引きへ変換し、AMD V80上のQwen3 1.7BでGPU比1.10〜3.29倍高速化を示す。

- **2025-11 · [DiffuMamba: High-Throughput Diffusion LMs with Mamba Backbone](2025-2511.15927-diffumamba-high-throughput-diffusion-lms-with-mamba-backbone.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  しかし拡散Transformerは各ステップで系列全体の注意を再計算し、系列長Lが長くなると注意演算の二乗計算量と中間状態の読み書きが負担になる。一方、過去ブロックの状態を再利用する方式では純Mamba版が2.3倍、混合版が1.9倍と報告され、倍率は復号方式ごとに異なる。

- **2025-11 · [DeCoRL: Decoupling Reasoning Chains via Parallel Sub-Step Generation and Cascaded Reinforcement for Interpretable and Scalable RLHF](2025-2511.19097-decorl-decoupling-reasoning-chains-via-parallel-sub-step-generation-and-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  DeCoRLは、長い推論手順を単一の大規模言語モデル（LLM）が順番に生成する代わりに、役割の異なる小さな推論モジュールへ分解して同時に実行し、出力を統合する枠組みである。著者はNVIDIA A100を使った10段階の推論問題で、逐次実行1,202ミリ秒に対してDeCoRLが316ミリ秒となり、約3.8倍高速化したと報告する。

- **2025-11 · [Beyond Confidence: Adaptive and Coherent Decoding for Diffusion Language Models](2025-2512.02044-beyond-confidence-adaptive-and-coherent-decoding-for-diffusion-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文は、整合的文脈復号（coherent contextual デコード; CCD）を提案する。ステップ数の比は3.48倍で、得点差は3.91ポイントである。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-10 · [TopK-Guided: Adaptive, Budget-Aware Activation Sparsity for Efficient LLM Inference](2026-2610.01763-topk-guided-adaptive-budget-aware-activation-sparsity-for-efficient-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  両手法はさらにTransformer層間へ一様な疎性予算を与え、疎化への耐性が異なる層を区別しない。論文のC4評価では、Llama-2-7BとLlama-3-8Bの目標疎性30%、50%、70%で、TopK-GuidedはTEALおよびWINAと比べperplexityと8課題平均正解率の両方で全条件最高だった。

- **2026-09 · [Why Does Post-Training Quantization Work?](2026-2609.11716-why-does-post-training-quantization-work.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）の重みを学習後に4ビットへ量子化すると、各線形層の重みが元の値からずれる。Qwen3-32Bの第1〜48層では、この相互作用がブロック更新誤差の二乗ノルムの累積寄与の50.2%を相殺した。

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

- **2026-09 · [Tensor Decomposition of Transformer Key-Value Caches: Spectral Structure and Format Comparison](2026-2609.28029-tensor-decomposition-of-transformer-key-value-caches-spectral-structure-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この研究は、自己回帰Transformerの鍵・値キャッシュ（key-value キャッシュ; KVキャッシュ）を、注意ヘッド・トークン・特徴・隣接層の四つの軸を持つテンソルとして扱い、どの軸が実際に低ランク圧縮できるのかを調べる。RoPE後の鍵を圧縮すると、RoPE前に圧縮する場合に比べて同じ保存量での再構成誤差が相対41〜64%増す。

- **2026-09 · [Taming Bitwise Behavior in GPU Kernels with Tensor Core: Black-Box Reconstruction, Compiler Enforcement, and Static Verification](2026-2609.11356-taming-bitwise-behavior-gpu-tensor-core-kernels.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU縮約順序を記述子化し、非公開行列積のビット挙動復元、コンパイラでの平衡木強制、命令列の静的同値判定を接続して再現性と自動調整を両立する。

- **2026-09 · [SpliTEE: Improving LLM Inference on Trusted Hardware with Differentially Private GPU Outsourcing](2026-2609.15039-splitee-improving-llm-inference-on-trusted-hardware-with-differentially-private-gpu-outsourcing.md)**  
  実装：[✓](https://github.com/DPVault/SpliTEE) ・ リポジトリ内被引用：0  
  TEE内のLLM線形演算を差分プライバシーで保護してGPUへ委譲し、プロンプト漏洩を抑えつつCPU-only TDX推論を約2倍高速化する。

- **2026-09 · [SiliconBench: Speed, Memory, and Fidelity for LLM Serving on Unified-Memory Desktops](2026-2609.19169-siliconbench-speed-memory-and-fidelity-for-llm-serving-on-unified-memory-desktops.md)**  
  実装：[✓](https://github.com/WindChimeRan/SiliconBench) ・ リポジトリ内被引用：0  
  Apple Siliconの九推論基盤を速度・共有メモリ・忠実度・新モデル対応・複数機で横断監査し、vllm-metalの並行処理と遠隔直接メモリアクセスを使うテンソル並列の優位を示す。

- **2026-09 · [Signed Rescue Routing: Harm-Aware Cascades for Efficient LLM Inference](2026-2609.07786-signed-rescue-routing-harm-aware-cascades-for-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（Large Language モデル; LLM）の多段推論では、全問い合わせを高価な大型モデルへ送る代わりに、まず小型モデルで回答し、難しいと判断したものだけ大型モデルへ送る。大型モデルの呼出し回数に予算があるとき、純利得が大きい問い合わせから優先して切り替える。

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

- **2026-09 · [RGSQ: Riemannian Geometry-Sensitive Quantization for Large Vision-Language Models](2026-2609.25492-rgsq-riemannian-geometry-sensitive-quantization-for-large-vision-language-models.md)**  
  実装：[✓](https://github.com/RL-MIND/RGSQ) ・ リポジトリ内被引用：0  
  重みの学習後量子化（Post-学習 量子化; PTQ）は配備時のメモリ占有と転送帯域を減らせるが、視覚トークンと言語トークンの分布が異なるため、単一言語モデル向けの量子化手順をそのまま適用すると品質が崩れやすい。LLaVA-OneVision-7BのW4A8で、A800一枚における校正時間は2.1時間、ピークメモリは38GBである。

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

- **2026-09 · [KBBQ: A Predictive Noise Law and the Limits of Spectrum Flattening in FP4 Quantization](2026-2609.08135-kbbq-a-predictive-noise-law-and-the-limits-of-spectrum-flattening-in-fp4.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みと活性化をともに4ビットに落とす量子化（W4A4）では、表現範囲を共有するブロック内の外れ値と丸め誤差がモデル精度を損なう。4つの基盤モデルと2種類の4ビット浮動小数点形式を用いた8組の実験で、単純丸めにKBBQを組み合わせる方式は、同じ設定の完全平坦化方式WUSHを7組で上回った。

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

- **2026-09 · [Accuracy is Not Enough: A Divergence-Based Approach to Evaluate Fidelity Loss in Quantized LLMs](2026-2609.07664-accuracy-is-not-enough-a-divergence-based-approach-to-evaluate-fidelity-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）を限られたGPUメモリやローカルPCで実行するために、重みの事後量子化（Post-学習 量子化; PTQ）が使われる。LLaMA-3.1-8BのMMLUでは、Q4Kの正解率32.2%、TVD0.055に対し、Q40は正解率32.1%、TVD0.221である。

- **2026-08 · [VoiceMem: Streaming Dual-Brain Memory for Real-Time Interaction](2026-2608.26005-voicemem-streaming-dual-brain-memory-for-real-time-interaction.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  VoiceMemは、音声対話システムの過去会話記憶を、応答を遅らせずに少数の関連記憶へ絞るための索引・更新・検索方式である。

- **2026-08 · [TurboBus: Pooling PCIe Bandwidth for LLM Workloads via Scale-Up Fabrics](2026-2fe550669a96-turbobus-pooling-pcie-bandwidth-for-llm-workloads-via-scale-up-fabrics.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU間高速ファブリックを中継路として他GPUの空きPCIeリンクを借用し、モデル読込の初回トークン待ち時間を最大40%削減、鍵値退避推論を最大1.6倍高速化する。

- **2026-08 · [TailSieve: Partial-Rollout-Guided Tail Routing for LLM Rollouts](2026-2608.22788-tailsieve-partial-rollout-guided-tail-routing-for-llm-rollouts.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TailSieveは、以前の部分生成で時間切れとなったプロンプト群を、追加の長さ予測モデルなしで長尾候補として選び、長尾専用プールと通常プールへ割り当てる。

- **2026-08 · [SplitScaling: Adaptive Scaling for Disaggregated LLM Serving Against Traffic Bursts via DRL](2026-92b65c48d388-splitscaling-adaptive-scaling-for-disaggregated-llm-serving-against-traffic-bursts-via-drl.md)**  
  実装：[✓](https://github.com/Onlytonight/SplitScaling) ・ リポジトリ内被引用：0  
  プリフィル／デコード各プールを深層強化学習で独立伸縮し、新規ノードへ待機要求を即時再割当して、バースト負荷下でSLOを守りながら静的構成比25.2%の計算コストを削減する。

- **2026-08 · [SoftWater: Class-Aware Rate Allocation for Softmax Quantization](2026-2608.12026-softwater-class-aware-rate-allocation-for-softmax-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の事後量子化では中間の線形層を2〜4ビットにしても、この最終出力層だけを16ビットで残すことが多い。例えばLlama-3.2-1Bの出力層は約2.63億パラメータ、モデル全体の21.3%であり、本体を低ビット化すると出力層の相対的な容量負担がさらに増える。

- **2026-08 · [Sliding-window beats linear attention](2026-2608.28444-sliding-window-beats-linear-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  線形注意は固定サイズの再帰状態に集約することで、この増加を抑える。窓64・先頭シンク4の方式は、一般知識6課題平均で元モデルの99.0%を回復し、11の比較例のうち9例で元モデルを除く最高の平均値を得た。

- **2026-08 · [RotaryQuant: Fitting 120B MoE Models on Consumer Hardware via Fused Compressed-Space Attention](2026-2608.08081-rotaryquant-fitting-120b-moe-models-on-consumer-hardware-via-fused-compressed-space-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み・3ビット鍵値キャッシュ・専門家退避を統合し、圧縮表現のまま注意計算して120B MoEを17.2GB、14.85トークン毎秒で実行する。

- **2026-08 · [RoRA: Role-Oriented Regional Allocation for Visual Token Pruning in MLLMs](2026-2608.07088-rora-role-oriented-regional-allocation-for-visual-token-pruning-in-mllms.md)**  
  実装：[✓](https://github.com/LukieLuu/RoRA) ・ リポジトリ内被引用：0  
  高解像度画像や複数画像では、画像に由来するトークンが入力系列の多くを占め、事前計算（プリフィル）の演算、注意機構のキー・バリュー（KV）キャッシュ、応答開始までの時間を増加させる。LLaVA-1.5-7Bの視覚576トークンを64個へ減らす条件（88.9%削減）では、九つの評価課題の正規化平均が非削減時の96.5%に相当した。

- **2026-08 · [ResiSpec：残差分布整形による複数候補投機サンプリング](2026-2608.24411-resispec-enhancing-multi-candidate-speculative-sampling-via-residual-distribution-shaping.md)**  
  実装：[✓](https://github.com/Czzzk/Resispec) ・ リポジトリ内被引用：0  
  複数候補方式は候補数を増やせば受理確率が上がるように見えるが、最初の候補が棄却されると対象分布からその候補確率を差し引いた残差分布へ移り、元のドラフト分布と急速にずれる。対象モデルの厳密な出力分布を変えず、既存の最先端複数候補方式に対して最大1.92倍の高速化を報告する。

- **2026-08 · [RAC: Reference-Aware Activation Compression for Communication-Efficient Split LLM Inference](2026-2608.04991-rac-reference-aware-activation-compression-for-communication-efficient-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末からクラウドへ送る境界活性と、クラウドから端末へ返す境界活性を、そのまま低ビット量子化するのではなく、送受信側で共有可能な参照状態との差分として符号化する。原著が評価した3モデルと9種類のモデル・回線条件では、無圧縮との比較で平均初回トークン時間（TTFT）の比が1.24～2.72倍、平均出力トークン時間（TPOT）の比が1.01～2.79倍である。

- **2026-08 · [PRQuant: Permutation Residual Quantization for Low-Overhead Inference](2026-2609.22106-prquant-permutation-residual-quantization-for-low-overhead-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PRQuantは、言語モデルの線形層を重み・活性値とも4ビット相当で実行する際、少数の外れ値経路が精度を左右する問題を扱う。特に微小尺度浮動小数点4ビット形式（MXFP4）では小ブロックが共通尺度を持ち、ブロック内の一部の大きな値に尺度を合わせると、それ以外の値の量子化刻みが粗くなる。

- **2026-08 · [Performance Foundations of Parallel & Distributed Reasoning Language Models](2026-2608.27046-performance-foundations-of-parallel-distributed-reasoning-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RLM後学習を仕事量・深さ・メモリで形式化し、モデル内6種の並列化と配置・段階融合・非同期化を統一分類して、長い自己回帰生成が支配する分散RLの設計原理を整理する。

- **2026-08 · [OpRAG: A Resource-Deterministic Runtime for GPU-Backed Multi-Stage RAG Workflows](2026-2608.08340-oprag-resource-deterministic-rag-runtime.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RAG各段階を資源・通信付き演算子へ変換し、ゼロコピー通信とCPU/GPU重畳で復号外のオーケストレーション律速を削減する。

- **2026-08 · [OoO-Spec: Out-of-Order Semantic Speculation for Fast Tool Calling](2026-2608.00814-ooo-spec-out-of-order-semantic-speculation-for-fast-tool-calling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  OoO-Specは、この未解決の部分を文字列上の位置に到達する前に、意味的なスロットとして並列予測する方式である。

- **2026-08 · [MARCH: Scaling Recurrent Memory with Content-Routed State Anchors](2026-2608.12435-march-scaling-recurrent-memory-with-content-routed-state-anchors.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MARCHは、再帰型言語モデルの「過去を固定サイズの状態に圧縮するため、後から古い情報を取り出しにくい」という問題を、累積再帰状態の履歴保存と内容に基づく検索で緩和する構造である。過去状態の読出しには追加費用があり、128KではTop-4の疎ルーティングが密なMARCHの学習処理量を2倍超に改善する。

- **2026-08 · [MAPLE: MoE Adaptive Plug-and-play Layer-wise Expert allocation](2026-2608.15299-maple-moe-adaptive-plug-and-play-layer-wise-expert-allocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層によって専門家数を減らしたときの精度劣化が異なるにもかかわらず、一律に削ると重要な層の計算能力まで失う。DeepSeek-MoE-16B、DeepSeek-V2-Lite、Moonlight-16B-A3B、OLMoE-1B-7Bの4モデルを、ルーティング対象専門家の総活性数を元の75%とする条件で評価した。

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

- **2026-08 · [FlashQuant: Sparse-Dense Fusion for Memory-Efficient Outlier-Aware LLM Inference](2026-2608.15531-flashquant-sparse-dense-fusion-for-memory-efficient-outlier-aware-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FlashQuantは、大規模言語モデルの重み4ビット・活性値16ビット量子化（W4A16）で生じる「低精度の密行列積と、高精度で残した少数の外れ値による疎行列積を別々に実行する」という問題を、GPUカーネルの内部構造から解決する研究である。BF16のcuBLASに対するカーネル高速化は2.74〜4.18倍だが、これは4ビット量子化の効果も含む。

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

- **2026-08 · [DARTree: Speculative Diffusion Decoding with Autoregressive Draft Trees](2026-2608.13524-dartree-speculative-diffusion-decoding-with-autoregressive-draft-trees.md)**  
  実装：[✓](https://github.com/VILA-Lab/DARTree) ・ リポジトリ内被引用：0  
  投機的復号では軽量な提案器が複数の候補トークンを作り、大きな目標モデルがまとめて検証する。Qwen3-4B、温度0、GSM8Kでは平均受理長12.97トークン、同一環境で測定した通常自己回帰復号に対して9.73倍の復号速度向上を報告する。

- **2026-08 · [Bounded-State Restoration: Decoupling Local Restore Capacity from External LLM State](2026-2608.17826-bounded-state-restoration-decoupling-local-restore-capacity-from-external-llm-state.md)**  
  実装：[✓](https://github.com/StarkLeeSunny/Flexkv-doublenode) ・ リポジトリ内被引用：0  
  外部KV状態の全ヒットを先に把握しつつ、復元はWチャンク窓だけを順次ステージングして解放することで、長大な外部状態とローカル復元メモリを分離する方式。

- **2026-08 · [Beyond Sparse Weights: When Is Attention Compressible?](2026-2608.21541-beyond-sparse-weights-when-is-attention-compressible.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  疎な注意マップだけではKV圧縮を正当化できないことを理論化し、値分散配分と末尾要約を厳密な物理予算で実装するCertKVを提案。

- **2026-08 · [AsymSpec: Efficient Cloud-Edge Speculative Decoding over Asymmetric Networks](2026-2608.04974-asymspec-efficient-cloud-edge-speculative-decoding-over-asymmetric-networks.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  非対称回線向けの証明付き段階補正と確認済み要求間パイプラインを組み合わせ、クラウド・エッジ投機的復号の通信待ちと無効先読みを削減する。

- **2026-08 · [Archer: Adaptive Reuse of Cached Hidden States for Efficient Rollback in Diffusion Language Models](2026-2608.08086-archer-adaptive-reuse-of-cached-hidden-states-for-efficient-rollback-in-.md)**  
  実装：[✓](https://github.com/Hxnng/Archer) ・ リポジトリ内被引用：0  
  本研究は、拡散言語モデル（Diffusion Language モデル; DLM）が一度生成したトークンを後から置換・再マスクできる「巻き戻し（rollback）」を保持しながら、繰り返しの全系列再計算を減らす推論時のキャッシュ制御を扱う。ただし応答を再計算することと、元の全再計算方式と同じ出力分布・復号経路を保証することは異なる。

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

- **2026-07 · [WISERouter: LLM Routing with Workload Budget Constraint](2026-2607.23765-wiserouter-llm-routing-with-workload-budget-constraint.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  常に最高性能のモデルを呼ぶと料金が膨らむ一方、全問い合わせに固定額を課すと、容易な問い合わせで節約した予算を難しい問い合わせへ振り向けられない。過去のモデル応答をすべて持つWR-Offlineと、限られた応答だけを逐次観測するWR-Onlineの二方式がある。

- **2026-07 · [SelectInfer: Selective Neuron Loading and Computation for On-Device LLMs](2026-2607.18081-selectinfer-selective-neuron-loading-and-computation-for-on-device-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  オフラインで重要FFNニューロンを選別して必要分だけロードし、入力ごとの活性で計算対象も絞ることで、端末LLMのメモリ量と計算量を独立に調整する方式。

- **2026-07 · [LLMET: Enabling Cross-Layer Evaluation of Emerging M3D Memories for Energy-Efficient LLM Serving](2026-2607.26491-llmet-m3d-memory-energy-efficient-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMETは、LLMのタイル配置とメモリ階層転送を回路レベルのSRAM・M3D特性へ接続し、L2容量を増やす利益とアクセス費が釣り合う省エネ設計点を探索する。

- **2026-07 · [LaCo: Layer-wise Compensation for Pruned Large Language Models](2026-00140e8efcf4-laco-layer-wise-compensation-for-pruned-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LaCo（層-wise Compensation）は、枝刈りによって一部の重みや層内構造を削除したLLMの性能を、元モデルの各層の隠れ状態へ順次近づける局所回帰で回復する方法である。

- **2026-07 · [LaCache: Exact Caching and Precision-Adaptive Inference for Diffusion Large Language Models](2026-2607.16339-lacache-exact-caching-precision-adaptive-dllm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散型LLMの反復生成で不変なトークン状態とFlashAttention中間状態を無損失再利用し、第2層以降をFP8化して、既存の生成ステップ削減法と組み合わせ可能な推論高速化を実現する。

- **2026-07 · [I/o for LLM inference: a survey of storage and memory bottlenecks](2026-5e022a2789e7-i-o-for-llm-inference-a-survey-of-storage-and-memory-bottlenecks.md)**  
  実装：[✓](https://github.com/rch0wdhury/llm-io-profiler) ・ リポジトリ内被引用：0  
  LLMデコードのデータ移動を重み・KVキャッシュ・活性の三I/O流へ分解し、量子化からSSD/CXL/統合メモリまでをルーフライン上で統一して、最適化を積むと支配ボトルネックが移動することを定量化したサーベイ。

- **2026-07 · [HunyuanOCR-1.5: Making Lightweight OCR VLMs Faster and Better](2026-2607.04884-hunyuanocr-1-5-making-lightweight-ocr-vlms-faster-and-better.md)**  
  実装：[✓](https://github.com/Tencent-Hunyuan/HunyuanOCR) ・ リポジトリ内被引用：0  
  原著の研究全体は、認識精度を改善するデータ構築・学習と、出力生成を高速化する推論機構の二本立てである。OmniDocBenchの単一要求評価で、同じHunyuanOCR-1.5の自己回帰復号と比較した平均ページ遅延は、Transformersで34.850秒から5.474秒、vLLMで3.032秒から1.408秒になった。

- **2026-07 · [Half the Experts, All the Code: One-Shot Domain Pruning of Mixture-of-Experts LLMs for Coding](2026-2607.16721-half-the-experts-all-the-code-one-shot-domain-pruning-of-mixture-of-expe.md)**  
  実装：[✓](https://github.com/anik-jha/moep) ・ リポジトリ内被引用：0  
  Qwen3.6-35B-A3Bでは、専門家を各層50%保持するREAP方式によって総パラメータ数を36.0Bから19.0Bに減らし、HumanEval+の単発正答率（pass@1）は0.890から0.896となった。

- **2026-07 · [From Expert Reduction to Behavioral Divergence: Tracing Numerical State through Sparse MoE Inference](2026-2607.28097-from-expert-reduction-to-behavioral-divergence-tracing-numerical-state-through-sparse-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  疎MoEの専門家加算順序だけで内部状態と生成文が分岐しうることを全順列・状態再構成で実証し、BF16項＋FP32累算を評価範囲の安定な互換契約として特定する。

- **2026-07 · [Every Microsecond Matters: Achieving Near Speed-of-Light Latency in GPU Collectives](2026-2607.16100-every-microsecond-matters-achieving-near-speed-of-light-latency-in-gpu-c.md)**  
  実装：[✓](https://github.com/ss16118/low-latency-nccl) ・ リポジトリ内被引用：0  
  本研究は、GPU間の集合通信（collective 通信）を大きなメッセージの帯域幅ではなく、短いメッセージの待ち時間を中心に最適化する。そこで、データ転送と到着通知を一体化するLL方式、受信領域の特殊値で到着を判定するsentinel方式、双方向通信と二重バッファによる暗黙の順序制御、NVLinkの原子的加算を使うLL128方式を設計した。

- **2026-07 · [Enabling Spatially Fine-Grained DVFS in Neural Processing Units for Energy-Efficient LLM Serving](2026-2607.16473-enpu-component-level-dvfs-npu-llm-serving.md)**  
  実装：[✓](https://github.com/google-coral/coralnpu（ベースコア）。eNPUの改変実装・シミュレータの公開URLは一次資料に記載なし。) ・ リポジトリ内被引用：0  
  eNPUは、演算器・SRAM・HBM・接続を別電圧周波数領域に分け、非同期転送と演算子別計画をSLO余裕で切替えて、NPUサービングの非ボトルネック電力を落とす。

- **2026-07 · [DynaCalKV: Key-Value Cache Compression via Head Grouping and Adaptive Rank Allocation](2026-2607.24331-dynacalkv-key-value-cache-compression-via-head-grouping-and-adaptive-rank-allocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キー投影の注意ヘッドをCKA類似度で動的に群分けし、群ごとの情報量に応じて低ランク次元を配分することでReCalKVよりキー側パラメータを減らすが、GQAの長文脈では精度低下も確認する。

- **2026-07 · [DeLS-Spec: Decoupled Long-Short Contexts for Parallel Speculative Drafting](2026-2607.07409-dels-spec-decoupled-long-short-contexts-for-parallel-speculative-draftin.md)**  
  実装：[✓](https://github.com/dt-3t/DeLS-Spec) ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、軽量なドラフトモデルで複数の候補トークンを先に生成し、目標モデルの一度の前向き計算で並列検証することで自己回帰生成の逐次呼出しを減らす。Qwen3-4Bの温度0、8ベンチマーク平均では、DFlashの自己回帰比復号高速化4.63倍・平均受理長6.04から、DeLS-Specは4.82倍・6.35へ改善した。

- **2026-07 · [CXL-CCL: Inter-Node Collective GPU-Communication Using a CXL Shared Memory Pool](2026-fab14a584908-cxl-ccl-inter-node-collective-gpu-communication-using-a-cxl-shared-memory-pool.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CXL共有メモリをノード間GPU集団通信の媒体として使い、データ配置・細粒度重畳・ドアベル同期でRDMA型通信に対する性能とコストを改善する。

- **2026-07 · [CTA-Pipelining: A Latency-Oriented Spatial Scaling Method for Multi-GPU Systems](2026-2607.07862-cta-pipelining-a-latency-oriented-spatial-scaling-method-for-multi-gpu-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  協調スレッド配列（Cooperative Thread Array、以下CTA）ごとの依存関係を追跡し、GPU間の共有メモリ空間に配置した待ち行列で後段CTAを起動する方式がCTA-Pipeliningである。

- **2026-07 · [CRISP: Pre-LLM Yet Text-Driven Visual Token Pruning for Efficient LVLM Inference](2026-2607.16326-crisp-pre-llm-yet-text-driven-visual-token-pruning-for-efficient-lvlm-in.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  学習を追加せず、言語モデルの層内注意重みを取り出さないことが設計上の要点である。原著の表IではLLaVA-1.5-7Bの視覚トークンを576個から128個（77.8%削除）へ減らしても、報告された平均性能保持率は99.5%である。

- **2026-07 · [Constrained Decoding for Diffusion Language Models via Efficient Inference over Finite Automata](2026-2607.07026-constrained-decoding-for-diffusion-language-models-via-efficient-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DangとErmonは、生成時に課す制約を有限オートマトン（finite automaton）へ変換し、拡散モデルの各位置に対する予測分布とオートマトンの受理経路を結合する。制約を満たすかどうかを生成後に判定して捨てる拒否標本化とは異なり、無効な系列へ確率を割り当てない点が中心的な貢献である。

- **2026-07 · [A Hippocampus for Linear Attention: An Exact Memory for What the Recurrent State Forgets](2026-2607.02303-a-hippocampus-for-linear-attention-an-exact-memory-for-what-the-recurren.md)**  
  実装：[✓](https://github.com/scale-lab-ai/HOLA) ・ リポジトリ内被引用：0  
  線形注意（Linear 注意機構）や状態空間モデル（State Space モデル; SSM）は、入力履歴を固定長の再帰状態へ要約するため、過去の全トークンに対応する鍵・値キャッシュ（Key-Value キャッシュ; KVキャッシュ）を保存する全注意と比べて、長文脈の記憶容量を一定に保ちやすい。

- **2026-07 · [3DLS: A 3D Logic-Stacked Architecture for Disaggregated LLM Serving](2026-2607.01617-3dls-disaggregated-serving-interconnect.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル→デコードのKV転送とデコード側テンソル並列AllReduceを同じ横方向リンクで競合させず、KVだけを3D縦リンクへ物理分離するチップレット構成。等帯域条件でも最大1.49倍のスループットと60.2%の遅延削減を示す。

- **2026-06 · [Unified KV Pooling to Accelerate Long-Context LLM Serving](2026-2606.14779-unified-kv-pooling-to-accelerate-long-context-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数RAM/SSDを帯域幅比例の単一KVプールとして並列利用し、SPDK直アクセスでファイルシステムを迂回して長文脈KV再取得を高速化する。

- **2026-06 · [TGV-KV: Text-Grounded KV Eviction for Vision-Language Models](2026-2606.03075-tgv-kv-text-grounded-kv-eviction-for-vision-language-models.md)**  
  実装：[✓](https://github.com/Danielement321/TGV-KV) ・ リポジトリ内被引用：0  
  TGV-KVは、画像と文章を同時に入力する視覚言語モデル（Vision-Language モデル; VLM）の鍵・値キャッシュ（Key-Value Cache; KVキャッシュ）を、文章の意味を優先して削減する手法である。

- **2026-06 · [Teaching Diffusion to Speculate Left-to-Right](2026-2606.11552-teaching-diffusion-to-speculate-left-to-right.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、軽い生成器が複数の候補トークンを先に出し、大きな対象モデルが候補列を一度の並列計算で検証することで、対象モデルを逐次実行する回数を減らす。

- **2026-06 · [SMEPilot: Characterizing and Optimizing LLM Inference with Scalable Matrix Extensions](2026-2606.16332-smepilot-characterizing-and-optimizing-llm-inference-with-scalable-matrix-extensions.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CPU内のSMEと通常コアを共有帯域込みのルーフラインで使い分け、タイル分割・注意パイプライン・配置再利用によりLLM推論をllama.cpp比最大3.94倍高速化する。

- **2026-06 · [Skip a Layer or Loop It? Learning Program-of-Layers in LLMs](2026-2606.06574-skip-a-layer-or-loop-it-learning-program-of-layers-in-llms.md)**  
  実装：[✓](https://github.com/tianyi-lab/PoLar) ・ リポジトリ内被引用：0  
  本論文は、学習済みの各層を関数とみなし、その呼出し順と回数を入力に応じて変える「層プログラム（Program-of-Layers; PoLar）」を提案する。Qwen1.5-MoE-A2.7B-Chatの24層を対象にした実測では、予測器・埋め込み器・候補探索を含む追加費用は合計3.05ミリ秒、通常の全層実行の0.8%だった。

- **2026-06 · [Query-based Cross-Modal Projector Bolstering Mamba Multimodal LLM](2026-2606.04719-query-based-cross-modal-projector-bolstering-mamba-multimodal-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚言語モデルでは画像符号器が大量のパッチ特徴を生成し、それを言語モデルの入力トークンとして与える。Transformer型言語モデルでは長い入力が自己注意の計算量を増やす。問い合わせ型射影器とMamba言語モデルを学習・微調整したモデル構造そのものを比較している。

- **2026-06 · [ProtoKV: Streaming Video Understanding under Delayed Query with Summary-State Memory](2026-2606.26762-protokv-streaming-video-understanding-under-delayed-query-with-summary-s.md)**  
  実装：[✓](https://github.com/kaist-ina/ProtoKV) ・ リポジトリ内被引用：0  
  視覚言語モデル（Vision-Language モデル; VLM）は新しいフレームを取り込むたびに注意機構のキー・値（Key/Value; KV）キャッシュを増やす。主実験のLLaVA-OV-7Bでは、RVS-Egoの正答率が固定窓方式55.7%、オンラインのトークン保持方式InfiniPot-V 57.8%、ProtoKV 58.6%となる。

- **2026-06 · [Omni-Flow: A Unified Workflow Orchestration and Distributed KV Cache Sharing Framework for Multimodal Inference](2026-2606.31093-omni-flow-a-unified-workflow-orchestration-and-distributed-kv-cache-sharing-framework-for-multimodal-inference.md)**  
  実装：[✓](https://github.com/meituan-longcat/omni-flow) ・ リポジトリ内被引用：0  
  マルチモーダル推論を制御・データ・計算の3層へ分離し、Python DSL、GPU/CPU/SSD分散KV、SGLang互換実行を統合する。LongCat-NextやHunyuanImage-3を同じ配信抽象へ載せる基盤。

- **2026-06 · [Multi-Bitwidth Quantization for LLMs Using Additive Codebooks](2026-2606.12876-multi-bitwidth-quantization-for-llms-using-additive-codebooks.md)**  
  実装：[✓](https://anonymous.4open.science/r/DropbyDrop2026/) ・ リポジトリ内被引用：0  
  大規模言語モデルを異なる記憶容量の機器へ展開するとき、通常の学習後量子化（post-学習 量子化、PTQ）は3ビット、4ビット、5ビットといった精度ごとに別の圧縮モデルを作る必要がある。

- **2026-06 · [Mitigating Bias in Locally Constrained Decoding via Tractable Proposals](2026-2606.01926-mitigating-bias-in-locally-constrained-decoding-via-tractable-proposals.md)**  
  実装：[✓](https://github.com/MhDang/gelatwo) ・ リポジトリ内被引用：0  
  本論文は有限オートマトンをテンソル化し、残りトークン予算内に受理状態へ到達可能な語だけを許すGCDと、蒸留HMMで将来の有効な完了の確率を推定するP-GCDを提案。

- **2026-06 · [LoopMoE: Unifying Iterative Computation with Mixture-of-Experts for Language Modeling](2026-2606.04438-loopmoe-unifying-iterative-computation-with-mixture-of-experts-for-langu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常のMoEは、多数の専門家パラメータを保持しながら各トークンでは少数だけを選ぶことで、総容量と一回の計算量を分離する。しかし、反復による精度向上を単純な非反復モデルと比較すると、層数、総パラメータ、演算回数、専門家活性化数などが同時に変化し、何が改善を生んだのか分からなくなる。

- **2026-06 · [LiveServe: Interaction-Aware Serving for Real-Time Omni-Modal LLMs](2026-2606.22983-liveserve-interaction-aware-serving-for-real-time-omni-modal-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  音声対話の再生進捗・発話・割込みをスケジューリングとKV配置へ反映し、不要な先行生成を抑えながら次ターンのKVを発話中に先読みし、P90初回音声遅延と無駄計算を同時に減らす。

- **2026-06 · [LatentSkill: From In-Context Textual Skills to In-Weight Latent Skills for LLM Agents](2026-2606.06087-latentskill-from-in-context-textual-skills-to-in-weight-latent-skills-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の文脈内スキル方式（In-context Skill）は、作業手順や道具の使用方法を自然言語でプロンプトへ挿入する。Qwen3-8Bを基盤としたALFWorldでは、文脈内スキル方式に対し既知課題の平均成功率が52.9%から74.3%、未知課題が56.0%から69.4%へ改善し、事前充填トークン数を約64%削減した。

- **2026-06 · [Improving Visual Token Reduction via Rectifying Distortions for Efficient Multimodal LLM Inference](2026-2606.01711-improving-visual-token-reduction-via-rectifying-distortions-for-efficien.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚トークン削減（Visual Token Reduction; VTR）は不要なパッチを削除したり、似た特徴を統合したりして系列を短くする。LLaVA-1.5-7Bの8種類の画像理解課題で、視覚トークンを576個から64個へ減らすHoloVの平均保持率は92.2%だが、RESTOREを加えると96.5%になる。

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

- **2026-06 · [Beyond Per-Token Pricing: A Concurrency-Aware Methodology for LLM Infrastructure Cost Estimation](2026-2606.11690-beyond-per-token-pricing-a-concurrency-aware-methodology-for-llm-infrast.md)**  
  実装：[✓](https://github.com/pChitral/vllm-cost-meter) ・ リポジトリ内被引用：0  
  本研究はこの差を、要求到着率を明示した費用測定問題として定式化する。ハードウェア、モデル構造、量子化精度、要求到着率、遅延目標を分け、同じGPUでも負荷によって費用がどの程度変わるかを実機で測る。H100 NVLの主実験では、3種類のモデルと2種類の精度の計6構成を7段階の要求率で測定し、同じ構成内で17.5～36.3倍の出力トークン単価差を観測した。

- **2026-06 · [BatchGen: An Architecture for Scalable and Efficient Batch Inference](2026-2606.21712-batchgen-an-architecture-for-scalable-and-efficient-batch-inference.md)**  
  実装：[✓](https://github.com/batchgen-project/batchgen) ・ リポジトリ内被引用：0  
  系列をイベント駆動コルーチン化して停止・結合・分割・移動を可能にし、MoEバッチ形成と長尾負荷分散を動的化して最大2.3倍の大規模高速化を示す。

- **2026-06 · [Attribution-Guided and Coverage-Maximized Pruning for Structural MoE Compression](2026-2606.18304-attribution-guided-and-coverage-maximized-pruning-for-structural-moe-com.md)**  
  実装：[✓](https://github.com/yifu-ding/MoE-Slimming) ・ リポジトリ内被引用：0  
  専門家を丸ごと削除する従来方式では、重要度が高いと判定された専門家の内部にも残る冗長チャネルを見逃し、逆に頻度の低い専門家を全削除すると一部の入力に必要な能力を失う。著者らはDeepSeekとQwenの複数の混合専門家モデルを対象に、構造的枝刈り（structural 枝刈り）50%単独と、25%枝刈りに4ビット量子化を重ねた構成を比較した。

- **2026-06 · [AlphaQ: Calibration-Free Bit Allocation for Mixture-of-Experts Quantization](2026-2606.04980-alphaq-calibration-free-bit-allocation-for-mixture-of-experts-quantizati.md)**  
  実装：[✓](https://github.com/Superone77/AlphaQ) ・ リポジトリ内被引用：0  
  しかし、推論時に選択され得る専門家の重みをGPUまたは周辺メモリへ配置する必要があるため、活性化の疎性がそのまま重みの記憶容量削減につながるわけではない。専門家ごとに2、3、4ビットなど異なる量子化精度を与えれば容量を減らせるが、どの専門家を高精度で守るかが問題になる。

- **2026-06 · [Agent Memory: Characterization and System Implications of Stateful Long-Horizon Workloads](2026-2606.06448-agent-memory-characterization-and-system-implications-of-stateful-long-h.md)**  
  実装：[✓](https://github.com/Tambe-Lab/agent-memory-profiling) ・ リポジトリ内被引用：0  
  本研究は、長期にわたり複数のセッションをまたいで稼働する大規模言語モデル（LLM）エージェントの「記憶」を、回答品質を高める機能としてだけでなく、計算・メモリ・入出力・スケジューリングの対象となる実行時システムとして捉え直す。後者は前者の約26.5倍である。

- **2026-06 · [AdaCodec: A Predictive Visual Code for Video MLLMs](2026-2606.02569-adacodec-a-predictive-visual-code-for-video-mllms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者らは再生用動画符号化の考え方を、動画の画素を忠実に再生するためではなく、言語モデルが必要とする視覚情報を少ないトークンで伝えるために再設計した。Qwen3-VL-8Bを基盤とする原著の11種類の動画理解評価では、比較可能な視覚トークン予算で各評価の基準方式を上回った。

- **2026-06 · [Above the Inner Loop: Exceeding Accelerate at LLM Prefill GEMM on the M1 AMX](2026-2606.25426-above-the-inner-loop-exceeding-accelerate-at-llm-prefill-gemm-on-the-m1-amx.md)**  
  実装：[✓](https://github.com/dbhan08/inferc) ・ リポジトリ内被引用：0  
  M1 AMXの内側ループがロード発行律速であることを切り分け、細粒度パネルで第2 AMXブロックを使い、重み事前パッキングを併用してllama.cppの128トークンfp32プリフィルを1.44倍高速化する。

- **2026-05 · [When Are Experts Misrouted? Counterfactual Routing Analysis in Mixture-of-Experts Language Models](2026-2605.07260-when-are-experts-misrouted-counterfactual-routing-analysis-in-mixture-of.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  混合専門家（Mixture-of-Experts; MoE）言語モデルは、各トークンについて多数の専門家ネットワークのうち少数だけを実行する。Qwen3-30B-A3Bでは、確信度の高いトークンは標準経路と最良候補の差がほぼないが、難しいトークンでは大きく乖離する。ただし、この論文は推論時に32個の候補を毎回試す高速化方式を提案したわけではない。

- **2026-05 · [Visual-Redundancy-Controlled Parallel Decoding for Diffusion-Based Multimodal Large Language Models](2026-2605.25820-visual-redundancy-controlled-parallel-decoding-for-diffusion-based-multi.md)**  
  実装：[✓](https://github.com/infiniteYuanyl/VRCD) ・ リポジトリ内被引用：0  
  マスク付き拡散言語モデル（masked diffusion language モデル）は、未確定の多数のトークン位置を一度に予測し、確信の高い一部を確定する処理を繰り返して文章を生成する。主要な結果は推論高速化ではなく品質改善である。

- **2026-05 · [Triplet-Block Diffusion RWKV](2026-2605.25969-triplet-block-diffusion-rwkv.md)**  
  実装：[✓](https://github.com/leonardodalinky/B3D-RWKV) ・ リポジトリ内被引用：0  
  この論文は、片方向にしか情報が流れない再帰型言語モデルを、内部構造を変更せずに双方向の拡散型生成へ転換する方法を扱う。自己回帰型Transformerは生成位置を順番に確定するため、1回の復号で出せるトークン数が限られる。離散拡散型言語モデルは複数位置を並列に修正できるが、通常はブロック内の未マスク位置を左右両方向から参照する。

- **2026-05 · [Training-Inference Consistent Segmented Execution for Long-Context LLMs](2026-2605.11744-training-inference-consistent-segmented-execution-for-long-context-llms.md)**  
  実装：[✓](https://github.com/sxp11/Training-Inference-Consistent-Segmented-Execution) ・ リポジトリ内被引用：0  
  長文脈の大規模言語モデル（LLM）は、通常の全注意力（full self-注意機構）を使うと、入力が長くなるにつれて注意演算と中間状態の記憶費用が増大する。16K/32K事前充填でのGPUピークメモリは18.56/19.06GBで、全注意力の23.61/34.67GBより小さい。

- **2026-05 · [The Quantization Benefits of Residual-Free Transformers](2026-2605.25880-the-quantization-benefits-of-residual-free-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、Transformerの量子化を難しくする活性値の外れ値が、量子化器の選択だけでなくモデルの残差接続（Residual Connection）という構造に起因し得ることを示す。

- **2026-05 · [The Path Matters: Learning a Token-Commitment Policy for Diffusion Language Models](2026-2605.24697-the-path-matters-learning-a-token-commitment-policy-for-diffusion-langua.md)**  
  実装：[✓](https://github.com/BobSun98/TraceLock) ・ リポジトリ内被引用：0  
  LLaDAのGSM8Kでは生成長256・窓64で最終正答率80.0%、HumanEvalのPass@1は37.2%で、信頼度方式の79.8%、36.0%をわずかに上回る。

- **2026-05 · [The Efficiency Frontier: A Unified Framework for Cost-Performance Optimization in LLM Context Management](2026-2605.23071-the-efficiency-frontier-a-unified-framework-for-cost-performance-optimiz.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全文投入、検索拡張、要約・圧縮などの文脈管理方式は、回答品質だけ、または入力トークン数だけを比較すると運用上の優劣が決めにくい。HotpotQAの5,000問をGPT-5.4 miniで評価した結果、再利用回数が1から100へ増えると、F1約0.78の運用点で有効トークン数が566から424へ約25%減る構成が選ばれた。

- **2026-05 · [Tensor Cache: Eviction-conditioned Associative Memory for Transformers](2026-2605.22884-tensor-cache-eviction-conditioned-associative-memory-for-transformers.md)**  
  実装：[✓](https://github.com/kswain98/tensor-cache) ・ リポジトリ内被引用：0  
  長文脈や同時要求数が増えるほどキャッシュの占有量が増え、GPUメモリ容量と帯域を圧迫する。学習可能なゲートでL1の局所注意出力とL2の読出しを融合することで、固定容量を保ちながら窓外の情報を予測へ戻す。

- **2026-05 · [SpecSA: Bridging Speculative Decoding and Sparse Attention for Efficient LLM Inference](2026-2605.19893-specsa-sparse-speculative-verification.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的検証クエリが選ぶ重複KVブロックを一度だけ読み、厳密共有と近似共有、層間索引再利用、融合カーネルを比較して、長文脈の疎注意読出しを減らすシステム。

- **2026-05 · [Self-Orchestrating Language Models: Leveraging Semantic Dependence for Efficient Inference](2026-2609.14850-self-orchestrating-language-models-leveraging-semantic-dependence-for-ef.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  意味的に独立する文章断片や推論段階をモデルに印付けさせ、ランタイムが並列デコード、不要なKVページの解放、または拡散生成の並列順序に利用する三方式を示すMIT博士論文。各方式は別個に評価され、速度向上は課題・設定によって品質との交換条件がある。

- **2026-05 · [Selective Latent Thinking: Adaptive Compression of LLM Reasoning Chains](2026-2605.25745-selective-latent-thinking-adaptive-compression-of-llm-reasoning-chains.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかし、文章で説明する思考の全トークンを自己回帰的に生成すると、推論遅延とKVキャッシュ使用量が増える。複数の思考トークンを連続した潜在ベクトルへ置き換える方式は生成数を減らせるが、数値、式、厳密な条件分岐などの情報まで圧縮すると、正答に必要な離散的な値が失われやすい。

- **2026-05 · [Search Your Block Floating Point Scales!](2026-2605.12464-search-your-block-floating-point-scales.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ScaleSearchは、ブロック浮動小数点（Block Floating Point、BFP）形式で低ビット量子化するとき、各ブロックに共通する尺度（Scale）を最適化する方法である。これらは異なる評価対象の数値であり、尺度探索だけで全ての改善が生じたと見なしてはならない。

- **2026-05 · [QAM-W: Joint 2D Codebook Quantization for LLM Weights via Hadamard Rotation and Activation-Aware Scaling](2026-2605.26339-qam-w-joint-2d-codebook-quantization-for-llm-weights-via-hadamard-rotati.md)**  
  実装：[✓](https://github.com/white07S/qam-w) ・ リポジトリ内被引用：0  
  通常のスカラー学習後量子化（scalar post-学習 量子化）は各重みをほぼ独立に離散値へ丸める。TinyLlama-1.1B、Qwen2.5-3B、Mistral-7Bの主比較では5.5ビット相当のQAM-WでWikiText-2のパープレキシティー（PPL）がBF16比+0.4%、+0.3%、+0.1%に留まる。

- **2026-05 · [Pruning and Distilling Mixture-of-Experts into Dense Language Models](2026-2605.28207-pruning-and-distilling-mixture-of-experts-into-dense-language-models.md)**  
  実装：[✓](https://github.com/krafton-ai/moe-to-dense) ・ リポジトリ内被引用：0  
  演算量は小さくても、すべての専門家をGPUメモリへ常駐させる場合の容量は大きい。CPUへ退避すれば容量制約を緩和できるが、専門家の転送が遅延や帯域を圧迫する。Qwen3-30B-A3Bから約3.3Bの密な生徒モデルを作った実験では、約4Bトークンの蒸留後に5課題の平均58.10%を達成した。

- **2026-05 · [Probabilistic Tiny Recursive Model](2026-2605.19943-probabilistic-tiny-recursive-model.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  数独や格子型の制約充足問題で高い精度を示す一方、決定的な更新では誤った解の近傍へ収束し、再帰を増やしても抜け出せないことがある。推論時の追加計算を、再帰を長くする「深さ」だけでなく、並列に試す「幅」へ割り当てる方式である。

- **2026-05 · [PEEK: Context Map as an Orientation Cache for Long-Context LLM Agents](2026-2605.19932-peek-context-map-as-an-orientation-cache-for-long-context-llm-agents.md)**  
  実装：[✓](https://github.com/zhuohangu/peek) ・ リポジトリ内被引用：0  
  コンテキスト地図はエージェントのシステムプロンプトへ付与され、予算 B トークン以内に維持される。

- **2026-05 · [OSAQ: Outlier Self-Absorption for Accurate Low-bit LLM Quantization](2026-2605.04738-osaq-outlier-self-absorption-for-accurate-low-bit-llm-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、大規模言語モデル（Large Language モデル, LLM）の学習後量子化（Post-学習 量子化, PTQ）で、重みの少数の外れ値が量子化刻みを粗くする問題を扱う。これは約42.4%のPPL低下だが、元のFP16モデルのPPL5.47には遠い。

- **2026-05 · [OccamToken: Efficient VLM Inference with Training-Free and Budget-Adaptive Token Pruning](2026-2605.29657-occamtoken-efficient-vlm-inference-with-training-free-and-budget-adaptiv.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の視覚トークン枝刈り（visual トークン 枝刈り）は、注意重みや特徴ベクトルの類似度で重要度を付け、得点の高い上位K個を残す方式が多い。高解像度のLLaVA-NeXTでは、元の2,880個から平均40個まで減らしても元モデルの集約性能の93.8%を維持する。

- **2026-05 · [Nearly Optimal Attention Coresets](2026-2605.05602-nearly-optimal-attention-coresets.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈LLMのKVキャッシュを元の鍵・値対の部分集合へ縮約する際、全てのノルム有界な問い合わせに対して注意出力誤差をε以内に保つコアセットの存在上界と情報理論的下界を証明。計算可能な高速KV削除アルゴリズムや実モデルの品質・速度改善を実証する論文ではない。

- **2026-05 · [Multi-Stream LLMs: Unblocking Language Models with Parallel Streams of Thoughts, Inputs and Outputs](2026-2605.12460-multi-stream-llms-unblocking-language-models-with-parallel-streams-of-th.md)**  
  実装：[✓](https://github.com/seal-rg/streaming) ・ リポジトリ内被引用：0  
  Multi-Stream LLMsは、利用者、回答、内部思考、監査などの役割を独立したトークン列へ割り当て、一回の前向き計算で各列の次トークンを同時に生成するモデル形式を提案する。

- **2026-05 · [MixFP4: Enhancing NVFP4 with Adaptive FP4/INT4 Block Representations](2026-2605.31035-mixfp4-enhancing-nvfp4-with-adaptive-fp4-int4-block-representations.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MixFP4は、4ビット浮動小数点（FP4）量子化で生じる精度低下を、同じ4ビットの中で表現方式を切り替えて緩和する研究である。テンソル Core相当の合成回路では面積3.1%、電力1.5%増に収まる。

- **2026-05 · [Lodestar：オンライン学習によるLLM推論リクエストルータ](2026-2606.00946-lodestar-an-online-learning-llm-inference-router.md)**  
  実装：[✓](https://github.com/gangmuk/Lodestar) ・ リポジトリ内被引用：0  
  公開クラウドの同種8基A30クラスタと、A30 8基＋V100 8基の異種クラスタで評価し、強い接頭辞・負荷認識ヒューリスティックに対して平均TTFTを平均1.41倍、P99 TTFTを1.47倍改善し、条件によって異種クラスタでは4倍超の改善を示す。

- **2026-05 · [LocateAnything: Fast and High-Quality Vision-Language Grounding with Parallel Box Decoding](2026-2605.27365-locateanything-fast-and-high-quality-vision-language-grounding-with-para.md)**  
  実装：[✓](https://github.com/NVlabs/Eagle/tree/main/Embodied) ・ リポジトリ内被引用：0  
  各矩形を、四つの量子化座標と構造トークンからなる長さ6のブロックで表し、ブロック内部は同時に予測する。

- **2026-05 · [Llamas on the Web: Memory-Efficient, Performance-Portable, and Multi-Precision LLM Inference with WebGPU](2026-2605.20706-llamaweb.md)**  
  実装：[✓](https://github.com/ggml-org/llama.cpp) ・ リポジトリ内被引用：0  
  LlamaWebは静的メモリ計画、端末適応型WebGPUカーネル、量子化対応をllama.cppへ統合し、ブラウザ推論のメモリ消費とデコード性能を改善する。

- **2026-05 · [Layer-wise Token Compression for Efficient Document Reranking](2026-2605.20683-layer-wise-token-compression-for-efficient-document-reranking.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検索システムの再順位付け（reranking）では、初段のBM25や密ベクトル検索が返した文書候補を、より高価なTransformerで再評価する。Qwen3-0.6BのDL19段落再順位付けでは、28層中第8層から40%のトークンを残す設定でnDCG@10が無圧縮の約0.727と同水準のまま、QPSは5.35→6.69（25%増）となる。

- **2026-05 · [Language Modeling with Hyperspherical Flows](2026-2605.11125-language-modeling-with-hyperspherical-flows.md)**  
  実装：[✓](https://github.com/jdeschena/s-flm) ・ リポジトリ内被引用：0  
  S-FLMは代わりに次元 d の単位超球面 S^{d-1} 上へトークンを配置し、雑音ベクトルから正しい単語埋め込みへ回転する経路を学習する。

- **2026-05 · [Influence-Inspired Spectral Rotations for Extreme Low-Bit LLM Quantization](2026-2605.25203-influence-inspired-spectral-rotations-for-extreme-low-bit-llm-quantizati.md)**  
  実装：[✓](https://github.com/gogipav14/spectral-llm) ・ リポジトリ内被引用：0  
  この論文は、LLMの重みを極端に少ないビット数へ丸めるとき、同じ量子化グループ内でも出力に強く影響する方向を優先して精度を残す方法を検討する。ただし4ビットではQwen2.5-1.5BのPPLが9.65から9.71となり、評価ノイズの範囲で改善が見られない。

- **2026-05 · [GQLA: Group-Query Latent Attention for Hardware-Adaptive Large Language Model Decoding](2026-2605.15250-gqla-group-query-latent-attention-for-hardware-adaptive-large-language-m.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  多頭潜在注意（Multi-head Latent 注意機構; MLA）は鍵と値を共通の低ランク潜在ベクトルへまとめ、過去文脈から読み出すバイト数を大きく削減する。論文の中心的な「H20で3.4倍」は、文脈長8192・BF16・公開ピーク性能を入力した屋根線モデルによる注意部分の理論的処理量であり、実GPUで測ったモデル全体のトークン生成速度ではない。

- **2026-05 · [Ghosted Layers: Unconstrained Activation Alignment for Recovering Layer-Pruned LLMs](2026-2605.15491-ghosted-layers-unconstrained-activation-alignment-for-recovering-layer-p.md)**  
  実装：[✓](https://github.com/daniel-eai/ghosted_layers_official_repository) ・ リポジトリ内被引用：0  
  大規模言語モデルの深さ方向の構造的枝刈りは、トランスフォーマーの復号層を丸ごと削除し、特殊な疎行列カーネルを必要とせずにモデルの演算と重みを減らせる。LLaMA-3.1-8Bで32層中7層をLLM-Streamlineにより削除した場合、9課題平均正答率は無補正の42.60%から60.01%へ回復する。

- **2026-05 · [Gated Subspace Inference for Transformer Acceleration](2026-2605.03109-gated-subspace-inference-for-transformer-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）のバッチサイズ1の逐次復号では、GPUの計算能力よりも重み行列を高帯域メモリ（HBM）から読む費用が律速になりやすい。Gated Subspace Inference（GSI）は、各層の活性化を低次元基底への射影と残差に分解し、残差が十分小さいトークンだけ、事前計算した低次元の重み像を使う方式である。

- **2026-05 · [Full Attention Strikes Back: Transferring Full Attention into Sparse within Hundred Training Steps](2026-2605.16928-full-attention-strikes-back-transferring-full-attention-into-sparse-with.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈の大規模言語モデル（Large Language モデル; LLM）は、すべてのトークンへ注意を計算する全注意（Full 注意機構）を使うと、系列長の増加に伴って注意計算とキー・値（Key-Value; KV）キャッシュの負荷が増える。著者は100万トークン文脈のプリフィルで最大9.36倍、復号で約2.01倍の速度向上を報告する。

- **2026-05 · [Enhancing Visual Token Representations for Video Large Language Models via Training-Free Spatial-Temporal Pooling and Gridding](2026-2605.22078-enhancing-visual-token-representations-for-video-large-language-models-v.md)**  
  実装：[✓](https://github.com/bingjunluo/ST-GridPool) ・ リポジトリ内被引用：0  
  階層的な時間区間のフレームを格子状に組み合わせ、区間末尾へ多時間尺度の要約を埋め込むPyramid Temporal Gridding（PTG）と、視覚特徴のL2ノルムを重みに使うNorm-based Spatial Pooling（NSP）を統合する。

- **2026-05 · [Efficient MoE Inference on Single Consumer-grade GPU with Dynamic Expert Caching](2020-2026.00101-efficient-moe-inference-on-single-consumer-grade-gpu-with-dynamic-expert-caching.md)**  
  実装：[✓](https://github.com/rzhang772/SMOE) ・ リポジトリ内被引用：0  
  プリフィルの動的エキスパート配置とデコードのトークン-wise予測取得を組み合わせ、単一RTX 4090で671B級MoEを高速化するCPU/GPUハイブリッド基盤。

- **2026-05 · [Efficient Diffusion LLMs via Temporal-Spatial Parallel Decoding and Confidence Extrapolation](2026-2605.30753-efficient-diffusion-llms-via-temporal-spatial-parallel-decoding-and-conf.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  自己回帰型モデルは基本的に次の一語を順番に生成するのに対し、マスク型dLLMは多数の未確定位置を同時に予測し、確信度の低い位置を再びマスクして次の反復で修正する。

- **2026-05 · [EdgeRazor: A Lightweight Framework for Large Language Models via Mixed-Precision Quantization-Aware Distillation](2026-2605.04062-edgerazor-a-lightweight-framework-for-large-language-models-via-mixed-pr.md)**  
  実装：[✓](https://github.com/zhangsq-nju/EdgeRazor) ・ リポジトリ内被引用：0  
  対象は単なる事後量子化ではなく、量子化した生徒モデルを教師モデルで監督して再学習する混合精度量子化対応蒸留（Mixed-Precision Quantization-Aware Distillation; MPQAD）である。

- **2026-05 · [DREAM-R: Multimodal Speculative Reasoning with RL-Based Refined Drafting, Precise Verification, and Fully Parallel Execution](2026-2605.28678-dream-r-multimodal-speculative-reasoning-with-rl-based-refined-drafting-.md)**  
  実装：[✓](https://github.com/HuYunhai-Alex/DREAM-R) ・ リポジトリ内被引用：0  
  生成の各ステップで大きな目標モデルを実行すると、この長い推論部分が待ち時間を支配する。目標モデルの品質を必ず数学的に保存する厳密なトークン投機復号とは異なり、推論ステップの意味的妥当性を判定する近似的な方式であることが重要である。

- **2026-05 · [Don't Read Everything: A Curvature-Conditioned Query for Linear Attention](2026-2606.01294-don-t-read-everything-a-curvature-conditioned-query-for-linear-attention.md)**  
  実装：[✓](https://github.com/ledong0110/ccq) ・ リポジトリ内被引用：0  
  線形注意（Linear 注意機構）は、通常のsoftmax注意のように過去トークン全体との注意行列を毎回計算する代わりに、過去の鍵・値の情報を固定サイズの再帰状態へ蓄積する。

- **2026-05 · [DeferMem: Query-Time Evidence Distillation via Reinforcement Learning for Long-Term Agent Memory](2026-2605.22411-defermem-query-time-evidence-distillation-via-reinforcement-learning-for.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の記憶システムは、将来の質問が分からない時点で対話を要約・圧縮し、検索しやすい記憶単位を作る。原著v2の評価ではLongMemEval-Sの正答率が70.00%、LoCoMoで学習に使った唯一の会話conv-26を除いた正答率が89.93%だった。

- **2026-05 · [ConMoE: Expert-Pool Consolidation via Prototype Reassignment for MoE Compression](2026-2605.29350-conmoe-expert-pool-consolidation-via-prototype-reassignment-for-moe-comp.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ConMoEは、混合専門家モデル（Mixture-of-Experts; MoE）の推論に必要な専門家重みを、学習後の追加学習なしで縮小するための方式である。

- **2026-05 · [Concurrency without Model Changes: Future-based Asynchronous Function Calling for LLMs](2026-2605.15077-concurrency-without-model-changes-future-based-asynchronous-function-cal.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  一般的な同期方式では、モデルがツール呼出しを出力すると、その処理が完了するまで次の生成を止める。GPT-4oを用いたBFCL v4の検索ツール評価では、逐次同期呼出しと比べてタスク完了時間を1.26倍高速化した。

- **2026-05 · [Blurry Window Attention](2026-2606.09862-blurry-window-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Blurry Window 注意機構（BLA）は、長い系列の全トークンに注意を向ける通常の自己注意の代わりに、有限サイズの状態から過去の鍵・値情報を補間して読み出す注意機構である。規則学習課題RegBenchでは、比較した線形注意系の中でBLAとSWAが状態量の増加に応じて精度を改善し、BLAは小さな状態でも優位な条件があった。

- **2026-05 · [Beyond Position Bias: Shifting Context Compression from Position-Driven to Semantic-Driven](2026-2605.09463-beyond-position-bias-shifting-context-compression-from-position-driven-t.md)**  
  実装：[✓](https://anonymous.4open.science/r/seco-EE5E) ・ リポジトリ内被引用：0  
  本論文の対象は、長い文脈を少数の連続値の埋め込み（soft プロンプト）へ圧縮してから回答を生成する方式である。LLaMA-3.2-1B-Instructを用いた16倍圧縮・分布内6課題の平均完全一致率は、比較方式COMIの42.07に対してSeCoが53.52、平均F1は54.37に対して68.55であった。

- **2026-05 · [Bandwidth-Aware LLM Inference on Heterogeneous Many-Core Supercomputers](2026-2605.25655-bandwidth-aware-llm-inference-on-heterogeneous-many-core-supercomputers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低帯域・分散オンチップ記憶のMT-3000向けに演算子、融合注意、三段パイプライン、混合並列を共同設計し、大規模LLM推論を実現。

- **2026-05 · [AgentStop: Terminating Local AI Agents Early to Save Energy in Consumer Devices](2026-2605.15206-agentstop-terminating-local-ai-agents-early-to-save-energy-in-consumer-d.md)**  
  実装：[✓](https://github.com/brave-experiments/AgentStop) ・ リポジトリ内被引用：0  
  LLMエージェントは通常の一問一答と異なり、推論、検索、コード実行、失敗後の再試行を何度も繰り返す。これをクラウドではなく利用者の端末で動かすと、ネットワーク依存や外部へのデータ送信を減らせる一方、長時間のGPU稼働、発熱、電池消費が利用者に直接影響する。特に失敗する実行が長く続いた場合、最終的な課題成功に結び付かない電力が大量に消費される。

- **2026-04 · [VFA: Relieving Vector Operations in Flash Attention with Global Maximum Pre-computation](2026-2604.12798-vfa-relieving-vector-operations-in-flash-attention-with-global-maximum-p.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FlashAttentionは、巨大な注意行列をGPUの高帯域メモリへ書き出さず、クエリ・キー・値を小さなブロックに分割してオンチップメモリで処理する。VFA（Vector Relieved Flash 注意機構）はこの残った部分に焦点を当てる。要旨ではC16V32という計算器構成を基準にC8V32、C4V32、C4V16で約2倍の高速化を報告する。

- **2026-04 · [Unlocking the Edge deployment and ondevice acceleration of multi-LoRA enabled one-for-all foundational LLM](2026-2604.18655-ondevice-multilora-runtime.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  実行時LoRA入力・NPU向け最適化・並行生成・自己投機的復号を統合し、Galaxy S24/S25で多用途LLMを単一グラフ展開する。

- **2026-04 · [Thinking Without Words: Efficient Latent Reasoning with Abstract Chain-of-Thought](2026-2604.22709-thinking-without-words-efficient-latent-reasoning-with-abstract-chain-of.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  自然言語CoTは数学や多段階推論の正答率を改善するが、途中の推論を文章として一語ずつ生成するため、長い回答までの待ち時間と生成トークン費用を増やす。推論内容を短縮する手法には、文章を途中で打ち切る方式、自然言語のCoTを段階的に内在化する方式、連続ベクトルの潜在思考を繰り返す方式などがある。

- **2026-04 · [The Recurrent Transformer: Greater Effective Depth and Efficient Decoding](2026-2604.21215-the-recurrent-transformer-greater-effective-depth-and-efficient-decoding.md)**  
  実装：[✓](https://github.com/geniucos/recurrent-transformer) ・ リポジトリ内被引用：0  
  通常の自己回帰Transformerでは、ある層のトークン位置$i$に対する鍵・値は、その層に入力された表現から計算される。重要なのは、固定サイズの再帰状態へ過去を押し込む方式ではないことだ。

- **2026-04 · [Tandem: Riding Together with Large and Small Language Models for Efficient Reasoning](2026-2604.23623-tandem-riding-together-with-large-and-small-language-models-for-efficien.md)**  
  実装：[✓](https://github.com/Applied-Machine-Learning-Lab/ACL2026_Tandem) ・ リポジトリ内被引用：0  
  Tandemは、推論型大規模言語モデルが難問を解く際に生成する長い思考列を、より安価な小型言語モデルへ部分的に委ねる協調推論方式である。

- **2026-04 · [Structural Pruning of Large Vision Language Models: A Comprehensive Study on Pruning Dynamics, Recovery, and Data Efficiency](2026-2604.24380-structural-pruning-of-large-vision-language-models-a-comprehensive-study.md)**  
  実装：[✓](https://github.com/YiranHuangIrene/VLMCompression) ・ リポジトリ内被引用：0  
  本論文は新しい単一の枝刈りアルゴリズムを提案するというより、何を削るか、何を再学習するか、どれだけのデータを使うかの組合せを、異なる視覚言語モデルで統制して比較する研究である。

- **2026-04 · [SpikingBrain2.0: Brain-Inspired Foundation Models for Efficient Long-Context and Cross-Platform Inference](2026-2604.22575-spikingbrain2-0-brain-inspired-foundation-models-for-efficient-long-cont.md)**  
  実装：[✓](https://github.com/BICLab/SpikingBrain2.0) ・ リポジトリ内被引用：0  
  長い文章を扱う大規模言語モデルでは、全注意（Full 注意機構; FA）を用いると、事前充填（プリフィル）時の注意計算が系列長に対して二次的に増える。

- **2026-04 · [SpecFed: Accelerating Federated LLM Inference with Speculative Decoding and Compressed Transmission](2026-2604.25777-specfed-accelerating-federated-llm-inference-with-speculative-decoding-and-compressed-transmission.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  連合LLM投機的復号で上位K確率だけを送信し、2種の確率再構成と誤差上界により通信量を削減する方式。

- **2026-04 · [Sink-Token-Aware Pruning for Fine-Grained Video Understanding in Efficient Video LLMs](2026-2604.20937-sink-token-aware-pruning-for-fine-grained-video-understanding-in-efficie.md)**  
  実装：[✓](https://github.com/rlqja1107/SToP) ・ リポジトリ内被引用：0  
  従来の枝刈りは視覚符号化器の注意重みを重要度の代用として使うが、注意が高い位置に意味情報が多いとは限らない。

- **2026-04 · [Serving Chain-structured Jobs with Large Memory Footprints with Application to Large Foundation Model Serving](2026-2604.14993-serving-chain-structured-jobs-with-large-memory-footprints-with-application-to-large-foundation-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分散パイプライン型の大規模言語モデル推論を、モデルブロック配置、鍵値キャッシュ容量配分、オンライン負荷分散からなるサーバ鎖構成問題として定式化し、実サービング評価で平均応答時間を六十三から七十七パーセント削減する。

- **2026-04 · [RouteLMT: Learned Sample Routing for Hybrid LLM Translation Deployment](2026-2604.22520-routelmt-learned-sample-routing-for-hybrid-llm-translation-deployment.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルを用いた翻訳では、高品質な大型モデルをすべての要求に適用すると推論費用と遅延が大きくなる。小型モデルで大半を処理し、必要な要求だけ大型モデルへ振り分ける混成配備（hybrid deployment）は、一定の品質を維持しながら大型モデルの利用率を抑えるための基本的な方式である。

- **2026-04 · [Rethinking Residual Errors in Compensation-based LLM Quantization](2026-2604.07955-rethinking-residual-errors-in-compensation-based-llm-quantization.md)**  
  実装：[✓](https://github.com/list0830/ResComp) ・ リポジトリ内被引用：0  
  GPTQなどの学習後量子化（Post-学習 量子化; PTQ）は、線形層の重みを一列ずつ低ビット化し、量子化によって失われる出力を残りの未量子化重みの更新で補償する。Llama3.1-8B-InstructのGPTAQではゼロショット6課題平均70.3%→72.3%となった。

- **2026-04 · [Reason Only When Needed: Efficient Generative Reward Modeling via Model-Internal Uncertainty](2026-2604.10072-reason-only-when-needed-efficient-generative-reward-modeling-via-model-i.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  難しい質問には段階的な思考連鎖（Chain-of-Thought、CoT）が有効だが、簡単な質問にも毎回長い思考を生成すると、回答に至るまでの生成トークン数と推論費用が増える。ただし最初の並列生成は無料ではなく、バッチやGPU配置を含む実システム全体で同じ節約率になるとは限らない。

- **2026-04 · [Prompt Compression in the Wild: Measuring Latency, Rate Adherence, and Quality for Faster LLM Inference](2026-2604.02985-prompt-compression-in-the-wild-measuring-latency-rate-adherence-and-qual.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  入力圧縮（プロンプト compression）は、情報価値の低い語や断片を削り、生成モデルに渡す入力を短くすることでこの費用を減らす。著者はLLMLingua-2の軽量な圧縮器を使えば、特定の長文入力・高圧縮条件で端から端までの遅延を最大約18%減らせると報告する。

- **2026-04 · [Open-Loop Planning, Closed-Loop Verification: Speculative Verification for VLA](2026-2604.02965-open-loop-planning-closed-loop-verification-speculative-verification-for.md)**  
  実装：[✓](https://github.com/edsad122/SV-VLA) ・ リポジトリ内被引用：0  
  本論文は、計画は重いモデルで低頻度に実施し、計画が依然として妥当かの検査だけを軽いモデルで毎制御時刻に実施するSV-VLA（投機的 検証 for VLA Control）を提案する。

- **2026-04 · [NI Sampling: Accelerating Discrete Diffusion Sampling by Token Order Optimization](2026-2604.18471-ni-sampling-accelerating-discrete-diffusion-sampling-by-token-order-opti.md)**  
  実装：[✓](https://github.com/imagination-research/NI-Sampling) ・ リポジトリ内被引用：0  
  そのため従来の全段階方式は一回のモデル実行で一位置だけを確定し、長さ512の出力では原則512回の推論が必要となる。ICLR 2026の論文に記載された単一GPU評価では、LLaDA-8B-InstructのMBPP、生成長512で全段階方式19.1トークン/秒に対し273.8トークン/秒（14.3倍）を報告する。

- **2026-04 · [MI-Pruner: Crossmodal Mutual Information-guided Token Pruner for Efficient MLLMs](2026-2604.03072-mi-pruner-crossmodal-mutual-information-guided-token-pruner-for-efficien.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意の吸い込み（注意機構 Sink）、位置偏り、複数注意ヘッドの役割差、画像全体で目立つ物体への偏りがある。さらに64トークンのPOPE効率測定では、質問関連性だけを使うλ=1の構成が77.06ms、13.93GBであり、VisPrunerの89.48ms、14.35GBより小さい。

- **2026-04 · [LearnPruner: Rethinking Attention-based Token Pruning in Vision Language Models](2026-2604.23950-learnpruner-rethinking-attention-based-token-pruning-in-vision-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLaVA-v1.5では1画像576トークン、LLaVA-NeXTの高解像度入力では最大2,880トークンとなり、画像の背景や類似領域にも長い系列を割り当てる。LLaVA-v1.5-7Bの8課題では、視覚トークンを平均576個から32個へ削減しても、元モデルを100%とした平均相対性能94.8%を維持した。

- **2026-04 · [KV Cache Offloading for Context-Intensive Tasks](2026-2604.08426-kv-cache-offloading-for-context-intensive-tasks.md)**  
  実装：[✓](https://github.com/yandex-research/context-intensive-kv-offloading) ・ リポジトリ内被引用：0  
  文脈集約型課題でKV退避の選択誤差を分析し、低ビット量子化によるYAKVで精度とスループットを改善する。

- **2026-04 · [GSQ: Highly-Accurate Low-Precision Scalar Quantization for LLMs via Gumbel-Softmax Sampling](2026-2604.18556-gsq-highly-accurate-low-precision-scalar-quantization-for-llms-via-gumbe.md)**  
  実装：[✓](https://github.com/IST-DASLab/GSQ) ・ リポジトリ内被引用：0  
  大規模言語モデルを2～3ビット程度に圧縮すると、重みの転送量と常駐メモリを大幅に減らせる。Llama-3.1-8B/70Bの2ビット評価で従来スカラー量子化より高い精度を示し、Qwen3-8Bの既存GGUF K-Quantチェックポイントを同じ保存形式のまま改善する点が実用上重要である。

- **2026-04 · [GRASPrune: Global Gating for Budgeted Structured Pruning of Large Language Models](2026-2604.19398-grasprune-global-gating-for-budgeted-structured-pruning-of-large-languag.md)**  
  実装：[✓](https://github.com/ZiY-Wang/GRASPrune) ・ リポジトリ内被引用：0  
  本論文は、大規模言語モデル（LLM）の推論時に重みメモリと鍵・値キャッシュ（KV キャッシュ）がともに大きな資源を消費する点を背景に、フィードフォワードネットワーク（Feed-順伝播 Network; FFN）の中間チャネルと、注意機構のKVヘッド群を一つの予算で選ぶ構造化枝刈り（structured 枝刈り）を提案する。

- **2026-04 · [Geometry-Guided 3D Visual Token Pruning for Video-Language Models](2026-2604.18260-geometry-guided-3d-visual-token-pruning-for-video-language-models.md)**  
  実装：[✓](https://github.com/homothetic/Geo3DPruner) ・ リポジトリ内被引用：0  
  動画言語モデル（Video Language モデル）は、動画フレームを多数の画像パッチに分割して言語モデルへ入力する。三次元場面理解では同じ机や椅子が異なるカメラ位置から繰り返し写るため、入力トークンが増えても新しい空間情報が比例して増えるとは限らない。比較対象FastVは81.0%、VisPrunerは84.9%である。

- **2026-04 · [GenericAgent: A Token-Efficient Self-Evolving LLM Agent via Contextual Information Density Maximization (V1.0)](2026-2604.17091-genericagent-a-token-efficient-self-evolving-llm-agent-via-contextual-in.md)**  
  実装：[✓](https://github.com/lsdefine/GenericAgent) ・ リポジトリ内被引用：0  
  GenericAgent（GA）は、この問題を単純な長文対応ではなく、限られた文脈内の意思決定に有効な情報密度を高めるシステム設計として扱う。論文は複数のエージェント基盤との比較を行い、5種類の長期タスクでGAとClaude コードがともに100%成功しながら、GAの総トークン数が188,829、比較方式が537,413だったと報告する。

- **2026-04 · [Fleet: Hierarchical Task-based Abstraction for Megakernels on Multi-Die GPUs](2026-2604.15379-fleet-multi-die-gpu-megakernel.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Fleetは複数ダイGPUにチップレット単位の作業階層を追加し、永続カーネル内で同一L2を共有するCUを協調スケジュールしてLLMデコードの重み再利用と同期局所性を高める。

- **2026-04 · [ELMoE-3D: Leveraging Intrinsic Elasticity of MoE for Hybrid-Bonding-Enabled Self-Speculative Decoding in On-Premises Serving](2026-2604.14626-elmoe-3d-hybrid-bonding-self-speculative-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HBメモリ上の頻出エキスパート上位ビットをキャッシュ兼自己ドラフトとして使い、MoEの投機的デコードと重み転送を一体最適化する3D積層HW-SW協調方式。

- **2026-04 · [Efficient Test-Time Scaling via Temporal Reasoning Aggregation](2026-2604.17304-efficient-test-time-scaling-via-temporal-reasoning-aggregation.md)**  
  実装：[✓](https://github.com/qianfantianyuzhouzhou/TRACE) ・ リポジトリ内被引用：0  
  推論時の計算量を増やすと難問の正答率を改善できる場合があるが、すべての問題で長い思考を最後まで生成することが効率的とは限らない。答えが既に定まった後も思考を続ける「過剰思考」は、トークン数と応答待ち時間を増やす。一方、途中の回答の確信度が高くなった瞬間に止めると、まだ検討が十分でない誤答を確定する危険がある。正答率も完全には維持していない。

- **2026-04 · [Efficient Quantization of Mixture-of-Experts with Theoretical Generalization Guarantees](2026-2604.06515-efficient-quantization-of-mixture-of-experts-with-theoretical-generaliza.md)**  
  実装：[✓](https://github.com/nowazrabbani/moe_quantization) ・ リポジトリ内被引用：0  
  本研究は、混合専門家モデル（Mixture-of-Experts、MoE）の推論メモリを減らすため、全専門家を同じビット幅へ量子化する代わりに、専門家ごとに1〜3ビットなど異なる精度を割り当てる方式を提案する。Mixtral 8x7Bの8課題平均では、専門家平均2.5ビットの提案方式が68.38%、比較方式PMQが67.53%だった。

- **2026-04 · [ClawVM: Harness-Managed Virtual Memory for Stateful Tool-Using LLM Agents](2026-2604.10352-clawvm-harness-managed-virtual-memory-for-stateful-tool-using-llm-agents.md)**  
  実装：[✓](https://github.com/mpi-dsg/clawvm) ・ リポジトリ内被引用：0  
  ClawVMは、長時間稼働し外部ツールを使うLLMエージェントで、プロンプト文脈を高速・小容量の作業メモリ、永続ファイルを低速・大容量の退避先とみなし、状態の常駐・縮退・書戻しをエージェント実行基盤（agent harness）に強制する仕組みである。

- **2026-04 · [Characterizing Vision-Language-Action Models across XPUs: Constraints and Acceleration for On-Robot Deployment](2026-2604.24447-characterizing-vision-language-action-models-across-xpus-constraints-and.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、視覚・言語・行動モデル（Vision-Language-Action、VLA）をロボットに搭載するときの「制御周期内に推論を終えられるか」「何ワット時・いくらで実行できるか」という推論システムの問題を扱う。

- **2026-04 · [Cactus: Accelerating Auto-Regressive Decoding with Constrained Acceptance Speculative Sampling](2026-2604.04987-cactus-accelerating-auto-regressive-decoding-with-constrained-acceptance.md)**  
  実装：[✓](https://github.com/MANGA-UOFA/Cactus) ・ リポジトリ内被引用：0  
  検証器が毎トークンの計算を繰り返す必要を減らす一方、草案器が提案したトークンを確率的に棄却するため、草案器と検証器の分布が異なると効率が落ちる。Qwen3-14Bを検証器、0.6Bを草案器としたSpec-Benchの6種類の課題では、自己回帰生成に対する総合速度倍率がSpSの1.81倍からCactusの1.88倍へ改善した。

- **2026-04 · [Attention Editing: A Versatile Framework for Cross-Architecture Attention Conversion](2026-2604.05688-attention-editing-a-versatile-framework-for-cross-architecture-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（Large Language モデル; LLM）の長文脈推論では、過去トークンの鍵・値（Key-Value; KV）を保存するメモリと、その読出し帯域が制約となる。グループ化問い合わせ注意（Grouped Query 注意機構; GQA）はKVヘッドの共有によって容量を抑えるが、長い系列や多数の同時要求ではKVが増え続ける。

- **2026-04 · [AEGIS: Scaling Long-Sequence Homomorphic Encrypted Transformer Inference via Hybrid Parallelism on Multi-GPU Systems](2026-2604.03425-aegis-scaling-long-sequence-homomorphic-encrypted-transformer-inference-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AEGISは、完全準同型暗号（fully homomorphic encryption; FHE）で暗号化した入力を復号せずにTransformerへ通す際、複数GPUへ暗号文を分配する方法を最適化するシステムである。

- **2026-04 · [Adaptive Parallel Monte Carlo Tree Search for Efficient Test-time Compute Scaling](2026-2604.00510-adaptive-parallel-monte-carlo-tree-search-for-efficient-test-time-comput.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  成功候補を早期発見した場合に打ち切る「正の早期終了」は効果があるが、いくら探索しても十分な報酬に達しない要求には効かず、同時処理時の長い裾の遅延が残る。推論サーバーvLLMへ統合し、4基のNVIDIA H100でLlama-3.1-8B-InstructとQwen2.5-14B-Instructを評価した。

- **2026-04 · [A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression](2026-2604.19572-a-self-evolving-framework-for-efficient-terminal-agents-via-observationa.md)**  
  実装：[✓](https://github.com/multimodal-art-projection/TACO) ・ リポジトリ内被引用：0  
  TACO（Terminal Agent Compression）は、コマンド出力をエージェントの履歴へ入れる直前に圧縮する追加層である。MiniMax-M2.5によるTerminalBench 1.0では成功率42.30%→45.25%、総トークン29.74→23.43百万（21.2%減）である。

- **2026-03 · [The Model Knows Which Tokens Matter: Automatic Token Selection via Noise Gating](2026-2603.07135-the-model-knows-which-tokens-matter-automatic-token-selection-via-noise-.md)**  
  実装：[✓](https://github.com/MedHK23/AutoSelect) ・ リポジトリ内被引用：0  
  重要度の低いトークンを削除する既存手法は、注意重み、類似度、固定削減比などの代理指標を使うことが多く、最終回答に必要な情報を最適に残せるとは限らない。LLaVA-1.5-7Bの576視覚トークンを64個へ削減した条件で、10ベンチマークの平均性能維持率96.5%を報告する。

- **2026-03 · [The Missing Memory Hierarchy: Demand Paging for LLM Context Windows](2026-2603.09023-pichay-demand-paging-context-windows.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント文脈を仮想メモリとしてページングし、古いツール結果を追い出して再参照時に復元する透明プロキシ。139万追い出しで0.0254%フォルト率を報告。

- **2026-03 · [TERMINATOR: Learning Optimal Exit Points for Early Stopping in Chain-of-Thought Reasoning](2026-2603.12529-terminator-learning-optimal-exit-points-for-early-stopping-in-chain-of-t.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複雑な問題では思考が必要だが、答えが既に得られた後にも検算、別解探索、方針変更を続けることがある。実行時には未来の最終解答を参照せず、モデル最終層の隠れ状態から終了の可能性を予測し、複数トークンの多数決を経て を挿入する。Qwen3-8BのMATH-500では思考圧縮率45.1%（約54.9%削減）で、正答率91.1%から90.7%とほぼ同水準を維持した。

- **2026-03 · [SkipOPU: An FPGA-based Overlay Processor for Large Language Models with Dynamically Allocated Computation](2026-2603.14785-skipopu-an-fpga-based-overlay-processor-for-large-language-models-with-d.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、非線形処理の待機を隠す融合データフロー、浮動小数点活性値と4ビット整数重みを扱うDSP演算器の高密度実装、層をまたいで変化しないKVを保持するオンチップ履歴バッファを一体設計した。AMD Alveo U280上のLlama2-7Bで140.8トークン/秒、帯域効率86.7%を報告する。

- **2026-03 · [Serving Hybrid LLM Loads with SLO Guarantees Using CPU-GPU Attention Piggybacking](2026-2603.12831-serving-hybrid-llm-loads-with-slo-guarantees-using-cpu-gpu-attention-piggybacking.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CPUへ逃がした低優先度要求の注意計算を非同期化し、後続GPU密計算へ層単位で相乗りさせることで、SLOを守りながら低優先度スループットを最大9.85倍にする。

- **2026-03 · [Prune-then-Quantize or Quantize-then-Prune? Understanding the Impact of Compression Order in Joint Model Compression](2026-2603.18426-prune-then-quantize-or-quantize-then-prune-understanding-the-impact-of-c.md)**  
  実装：[✓](https://github.com/snudatalab/PQQP) ・ リポジトリ内被引用：0  
  本論文は、大規模言語モデル（LLM）を枝刈り（枝刈り）と量子化（量子化）の両方で圧縮する場合、どちらを先に適用すべきかを、圧縮率とモデル品質の関係から分析した研究である。枝刈り率5～30%、量子化4～8ビットを含む条件で、単独適用時の圧縮強度の差が大きいほど順序による品質差が大きくなる傾向を確認した。

- **2026-03 · [Prompt Compression in Production Task Orchestration: A Pre-Registered Randomized Trial](2026-2603.23525-prompt-compression-in-production-task-orchestration-a-pre-registered-ran.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  評価対象は新しい圧縮モデルの開発でもGPUカーネルの高速化でもなく、指示のどの部分をどれだけ残すかという圧縮方針の費用対効果である。

- **2026-03 · [Pooling Engram Conditional Memory in Large Language Models using CXL](2026-2603.10087-pooling-engram-conditional-memory-in-large-language-models-using-cxl.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  条件付き記憶は言語モデルの条件付き記憶を、通常のTransformer計算から分離した大規模なN-gram埋め込み表で保持する。

- **2026-03 · [OneComp: One-Line Revolution for Generative AI Model Compression](2026-2603.28845-onecomp-one-line-revolution-for-generative-ai-model-compression.md)**  
  実装：[✓](https://github.com/FujitsuResearch/OneCompression) ・ リポジトリ内被引用：0  
  大規模言語モデル（Large Language モデル; LLM）の重み量子化では、同じ平均ビット幅でも層ごとの感度、較正用入力の分布、丸め誤差の伝播、量子化後の品質回復方法によって性能が大きく変わる。Llama-3-8BとQwen3系の実験では、感度に応じた混合ビット幅割当や誤差伝播補正が量子化後の困惑度を改善した。

- **2026-03 · [M²RNN: Non-Linear RNNs with Matrix-Valued States for Scalable Language Modeling](2026-2603.14360-m-rnn-non-linear-rnns-with-matrix-valued-states-for-scalable-language-mo.md)**  
  実装：[✓](https://github.com/open-lm-engine/lm-engine) ・ リポジトリ内被引用：0  
  線形注意やMamba-2、Gated DeltaNetなどの再帰型方式は固定サイズの状態へ過去を畳み込み、生成時のメモリを一定に保ちやすい。

- **2026-03 · [Mixture of Chapters: Scaling Learnt Memory in Transformers](2026-2603.21096-mixture-of-chapters-scaling-learnt-memory-in-transformers.md)**  
  実装：[✓](https://github.com/Tasmay-Tibrewal/Memory) ・ リポジトリ内被引用：0  
  Mixture of Chapters（MoC）は、言語モデルが事前学習で獲得する知識を、通常の重みとは別の学習可能な潜在記憶として保持し、入力に必要な部分だけを交差注意（cross-注意機構）で取り出す設計である。元のmain原稿にあった主要な正負両方の結果を維持し、計算量の内訳、選択単位、実施済み実験と将来計画の区別を明確化した。

- **2026-03 · [LooComp: Leverage Leave-One-Out Strategy to Encoder-only Transformer for Efficient Query-aware Context Compression](2026-2603.09222-loocomp-leverage-leave-one-out-strategy-to-encoder-only-transformer-for-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかし検索件数を増やすと、無関係な文章も入力され、事前充填の計算量、入力トークン費用、モデルの注意の分散が問題になる。生成型の圧縮器は文書を短い文章へ書き換えられるが、圧縮器自体がトークンを逐次生成するため遅延が大きくなる。

- **2026-03 · [InfoDensity: Rewarding Information-Dense Traces for Efficient Reasoning](2026-2603.17310-infodensity-rewarding-information-dense-traces-for-efficient-reasoning.md)**  
  実装：[✓](https://github.com/amao0o0/InfoDensity) ・ リポジトリ内被引用：0  
  そこで、後方からの最大値包絡（suffix-max envelope）によって軌跡全体の形を要約し、同一問題に対する複数生成の相対的な長さで補正する報酬を設計した。原著表2では、DeepSeek-R1-Distill-Qwen-1.5Bの4ベンチマーク平均正答率が36.5%から50.8%へ上がり、平均生成長は11.1千から7.5千トークンへ短縮した。

- **2026-03 · [HiCI: Hierarchical Construction-Integration for Long-Context Attention](2026-2603.20843-hici-hierarchical-construction-integration-for-long-context-attention.md)**  
  実装：[✓](https://github.com/zengxyyu/HiCI) ・ リポジトリ内被引用：0  
  HiCI（Hierarchical Construction–Integration）は、長文脈言語モデルの注意機構を、セグメント単位の局所表現の構築、局所表現からの全体文脈の統合、全体と局所の情報を各セグメントへ再配信する処理へ分解する研究である。

- **2026-03 · [Gumbel Distillation for Parallel Text Generation](2026-2603.22216-gumbel-distillation-for-parallel-text-generation.md)**  
  実装：[✓](https://github.com/hxixixh/gumbel-distill) ・ リポジトリ内被引用：0  
  自己回帰言語モデル（autoregressive language モデル）は、前のトークンを条件に次の一個を順番に予測するため、隣接する語の依存関係を扱いやすい。例えば「San Francisco」を同時に予測する場合、「San」を選んだ条件で「Francisco」を選ぶという自己回帰的な関係が明示されない。

- **2026-03 · [GradMem: Learning to Write Context into Memory with Test-Time Gradient Descent](2026-2603.13875-gradmem-learning-to-write-context-into-memory-with-test-time-gradient-de.md)**  
  実装：[✓](https://github.com/yurakuratov/gradmem) ・ リポジトリ内被引用：0  
  長文脈の大規模言語モデル（LLM）では、過去の情報を再利用するために鍵・値キャッシュ（KV キャッシュ）を保持するのが一般的である。しかしキャッシュは通常、層数と文脈長に比例して増える。GradMemはこの記憶形成を、単なる順伝播による要約ではなく、推論時に小さな記憶ベクトルへ勾配降下を行う最適化問題として定義する。モデル本体の重みは推論時に更新しない。

- **2026-03 · [Fine-Grained Post-Training Quantization for Large Vision Language Models with Quantization-Aware Integrated Gradients](2026-2603.17809-fine-grained-post-training-quantization-for-large-vision-language-models.md)**  
  実装：[✓](https://github.com/ucas-xiang/QIG) ・ リポジトリ内被引用：0  
  重みと活性値を低ビット化すればメモリ使用量を抑えられるが、量子化誤差の影響は画像と文章という二つのモダリティの間だけでなく、同じモダリティ内の各トークンや層によっても異なる。著者はこれを1.60%の改善と説明するが、表の数値としては1.60ポイントの上昇である。

- **2026-03 · [EvoPrune: Early-Stage Visual Token Pruning for Efficient MLLMs](2026-2603.03681-evoprune-early-stage-visual-token-pruning-for-efficient-mllms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  多くの既存削減方式は、視覚符号化器が全トークンを処理した後に削減を行うため、後段の言語モデルの事前入力処理は軽くできても、視覚符号化器がすでに使った演算量は取り戻せない。

- **2026-03 · [EntropyCache: Decoded Token Entropy Guided KV Caching for Diffusion Language Models](2026-2603.18489-entropycache-decoded-token-entropy-guided-kv-caching-for-diffusion-langu.md)**  
  実装：[✓](https://github.com/mscheong01/EntropyCache) ・ リポジトリ内被引用：0  
  自己回帰型言語モデルの因果注意では、過去トークンの鍵・値（Key–Value; KV）表現は後続トークンの追加で変わらないため、過去KVを厳密に再利用できる。これに対して離散拡散言語モデル（discrete Diffusion Language モデル; dLLM）は双方向注意を使い、マスクされたトークンが一つ確定するだけで他の全位置の表現が変わり得る。

- **2026-03 · [DASH: Dynamic Audio-Driven Semantic Chunking for Efficient Omnimodal Token Compression](2026-2603.15685-dash-dynamic-audio-driven-semantic-chunking-for-efficient-omnimodal-toke.md)**  
  実装：[✓](https://github.com/laychou666/DASH) ・ リポジトリ内被引用：0  
  LLMへ渡す前の入力列が長くなると、プリフィル（プリフィル）の注意演算とKVキャッシュのメモリ消費が増える。DASH（動的 Audio-driven Semantic cHunking）は、音声埋め込みの隣接トークンの変化を意味境界の手掛かりにし、音声と映像を可変長の区間へ分ける学習不要の圧縮方式である。

- **2026-03 · [CSAttention: Centroid-Scoring Attention for Accelerating LLM Inference](2026-2604.08584-csattention-centroid-scoring-attention-for-accelerating-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈の自己注意では、現在の問い合わせベクトルと過去の鍵ベクトルとの内積を計算し、対応する値を重み付き集約する。多くの鍵の寄与が小さいため、一部の鍵だけを使う疎注意で演算量と転送量を削減できる。しかし95%もの鍵を捨てる場合、実際に重要な鍵を取りこぼすと正答率が急落する。鍵の全件走査をオンラインで繰り返さない設計である。

- **2026-03 · [CRISP: Compressed Reasoning via Iterative Self-Policy Distillation](2026-2603.05433-crisp-compressed-reasoning-via-iterative-self-policy-distillation.md)**  
  実装：[✓](https://github.com/HJSang/CRISP_Reasoning_Compression) ・ リポジトリ内被引用：0  
  CRISP（Compressed Reasoning via Iterative Self-Policy Distillation）は、この余分な思考を生成後に切り落とすのではなく、モデルが自発的に短い推論を出すように学習する方式である。

- **2026-03 · [Confidence-Calibrated Small-Large Language Model Collaboration for Cost-Efficient Reasoning](2026-2603.03752-confidence-calibrated-small-large-language-model-collaboration-for-cost-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、小型言語モデル（SLM）にまず問題を解かせ、答えへの自己申告確信度が低いときだけ大型言語モデル（LLM）へ委譲する二段推論方式COREAを提案する。大型モデル単独との比較で、領域外の数理問題では推定費用21.5%減・正答率1.7ポイント減、非数理問題では16.8%減・正答率1.7ポイント減となった。

- **2026-03 · [CLAG: Adaptive Memory Organization via Agent-Driven Clustering for Small Language Model Agents](2026-2603.15421-clag-adaptive-memory-organization-via-agent-driven-clustering-for-small-.md)**  
  実装：[✓](https://github.com/dmis-lab/CLAG) ・ リポジトリ内被引用：0  
  CLAGは、記憶を話題ごとのクラスタへ割り当てるエージェント主導のルーティング、割当先クラスタ内だけでリンク生成・要約更新を行う局所的進化、質問に関連するクラスタを先に選んでから個別記憶を検索する二段階検索の三つを結合する。原著付録Cによれば、200件のBioASQ質問で二段階検索が除外した記憶は平均8.02%にとどまる。

- **2026-03 · [Characterizing Performance-Energy Trade-offs of Large Language Models in Multi-Request Workflows](2026-2604.09611-characterizing-performance-energy-trade-offs-of-large-language-models-in.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  新しい推論カーネルの提案ではなく、既存の推論基盤をどの条件でどう設定すると効率が変わるかを調べる。A100 40GB上でLlama-2-7Bを使い、入力長、出力長、バッチサイズ、GPU電力上限を変える。

- **2026-03 · [Bielik-Minitron-7B: Compressing Large Language Models via Structured Pruning and Knowledge Distillation for the Polish Language](2026-2603.11881-bielik-minitron-7b-compressing-large-language-models-via-structured-prun.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの重み容量と計算費用を下げる方法には、数値精度を落とす量子化と、モデル構造自体を小さくする枝刈りがある。パラメータ削減率は33.4%である。

- **2026-03 · [Attention-Based Sampler for Diffusion Language Models](2026-2604.08564-attention-based-sampler-for-diffusion-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、マスク拡散型大規模言語モデル（dLLM）の生成時に、どの位置のマスクを先に確定するかを注意行列から決める学習不要の復号法Attn-Samplerを提案する。

- **2026-03 · [ASAP: Attention-Shift-Aware Pruning for Efficient LVLM Inference](2026-2603.14549-asap-attention-shift-aware-pruning-for-efficient-lvlm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ASAPはこの注意の位置偏り（注意機構 shift）を緩和するため、視覚トークン同士に限り、重要度の高い未来位置への注意を段階的に許可する。

- **2026-02 · [Understanding and Exploiting Weight Update Sparsity for Communication-Efficient Distributed RL](2026-2602.03839-understanding-and-exploiting-weight-update-sparsity-for-communication-ef.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）の強化学習による後学習（reinforcement learning post-学習）では、重みを更新する学習器（trainer）と、現在の方策を用いて回答を生成する推論ワーカー（inference worker）が分離されることが多い。

- **2026-02 · [Two-Stage Expert Offloading for Domain-Aware MoE Inference](2026-dacc3922b5b4-two-stage-expert-offloading-for-domain-aware-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  領域別プリフィル事前読込と時間・層間・領域局所性によるデコード先読みを組み合わせ、MoEのCPU退避でI/O待ち50%削減、投影TPOT 3.45倍高速化、全常駐比33%メモリ削減を狙う。

- **2026-02 · [T3D: Few-Step Diffusion Language Models via Trajectory Self-Distillation with Direct Discriminative Optimization](2026-2602.12262-t3d-few-step-diffusion-language-models-via-trajectory-self-distillation-.md)**  
  実装：[✓](https://github.com/Tyrion58/T3D) ・ リポジトリ内被引用：0  
  これに対しマスク拡散言語モデル（Masked Diffusion Language モデル、MDLM）は、複数位置のマスクを並列に予測し、繰り返し修正して文章を完成させる。動的復号を組み合わせた一部条件では、GSM8Kの正答率を10.8ポイント改善しながら処理量を1.45倍にする実測結果も報告されている。

- **2026-02 · [Swordsman: Entropy-Driven Adaptive Block Partition for Efficient Diffusion Language Models](2026-2602.04399-swordsman-entropy-driven-adaptive-block-partition-for-efficient-diffusio.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Swordsmanは、拡散言語モデル（Diffusion Language モデル、DLM）の生成速度と品質を改善するため、出力列を固定長で区切るブロック復号を、モデルの予測エントロピーに応じて動的に区切る方式へ変更する。

- **2026-02 · [SweetSpot: An Analytical Model for Predicting Energy Efficiency of LLM Inference](2026-2602.05695-sweetspot-an-analytical-model-for-predicting-energy-efficiency-of-llm-in.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SweetSpotは、大規模言語モデル（LLM）の推論で、入力トークン数と生成トークン数が変化したときの出力1トークン当たり電力量を予測する解析モデルである。単に出力が短ければ省エネルギーとは限らない。一方、出力を長くし続けると逐次復号（デコード）で参照するキー・値キャッシュ（KV キャッシュ）が増え、各ステップの計算とメモリアクセスが増える。

- **2026-02 · [StreamServe: Adaptive Speculative Flows for Low-Latency Disaggregated LLM Serving](2026-2604.09562-streamserve-adaptive-speculative-flows-for-low-latency-disaggregated-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分離型プリフィル・デコード上で、複数指標による要求ルーティングと実行時適応する投機深度を閉ループ連携し、4×A800評価でテンソル並列vLLM比の平均レイテンシ15.75倍短縮・平均スループット4.4倍を報告する。

- **2026-02 · [SimpleTool: Parallel Decoding for Real-Time LLM Function Calling](2026-2603.00030-simpletool-parallel-decoding-for-real-time-llm-function-calling.md)**  
  実装：[✓](https://github.com/HaxxorCialtion/SimpleTool) ・ リポジトリ内被引用：0  
  SimpleToolは、大規模言語モデルによる関数呼出し（function calling）の待ち時間を減らすために、出力表現の圧縮と並列復号（parallel デコード）を一緒に設計した手法である。

- **2026-02 · [SALAAD: Sparse And Low-Rank Adaptation via ADMM for Large Language Model Inference](2026-2602.00942-salaad-sparse-and-low-rank-adaptation-via-admm-for-large-language-model-.md)**  
  実装：[✓](https://github.com/HaoMAFRLu/salaad) ・ リポジトリ内被引用：0  
  SALAADは、言語モデルの重みを疎成分と低ランク成分の和として表現できるように事前学習中から構造を誘導し、配置時には必要なメモリ予算に応じて同じ学習済みチェックポイントを縮小できる方式である。

- **2026-02 · [ReviveMoE: Fast Recovery for Hardware Failures in Large-Scale MoE LLM Inference Deployments](2026-2602.21140-revivemoe-fast-hardware-failure-recovery.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単一NPU障害時にサービング全体を再起動せず、要求状態・KVブロック表・MoE重み・通信領域・実行グラフを局所修復して大規模MoE推論を高速復旧する。

- **2026-02 · [Pruning as a Cooperative Game: Surrogate-Assisted Layer Contribution Estimation for Large Language Models](2026-2602.07804-pruning-as-a-cooperative-game-surrogate-assisted-layer-contribution-esti.md)**  
  実装：[✓](https://github.com/920927/Pruning_As_A_Cooperative_Game) ・ リポジトリ内被引用：0  
  本論文は、推論時に実行するTransformer層を丸ごと減らす深さ方向の構造化枝刈り（depth-wise structured 枝刈り）を対象とする。

- **2026-02 · [Prism: Efficient Test-Time Scaling via Hierarchical Search and Self-Verification for Discrete Diffusion Language Models](2026-2602.01842-prism-efficient-test-time-scaling-via-hierarchical-search-and-self-verif.md)**  
  実装：[✓](https://github.com/viiika/Prism) ・ リポジトリ内被引用：0  
  Prismは、階層的軌跡探索（Hierarchical Trajectory Search; HTS）、部分再マスクによる局所分岐（Local Branching via Partial Remasking）、自己検証フィードバック（Self-Verified Feedback; SVF）を統合する。

- **2026-02 · [OTPrune: Distribution-Aligned Visual Token Pruning via Optimal Transport](2026-2602.20205-otprune-distribution-aligned-visual-token-pruning-via-optimal-transport.md)**  
  実装：[✓](https://github.com/xiwenc1/OTPrune) ・ リポジトリ内被引用：0  
  OTPruneは、画像と言語を組み合わせて推論する多モーダル大規模言語モデルにおいて、画像から得られる多数の視覚トークンを追加学習なしで削減する手法である。原著が証明する約63%の最悪時近似保証は代理目的の最大化に対するものであり、元のワッサースタイン距離や言語モデルの回答品質が63%保証されるという意味ではない。

- **2026-02 · [Online Vector Quantized Attention](2026-2602.03922-online-vector-quantized-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  オンラインベクトル量子化注意（Online Vector Quantized 注意機構、OVQ-注意機構）は、長い系列の情報を比較的大きな固定上限の記憶状態へ圧縮しながら、自己注意（self-注意機構）の長距離検索能力に近づける系列混合層である。

- **2026-02 · [On the Limits of Layer Pruning for Generative Reasoning in Large Language Models](2026-2602.01997-on-the-limits-of-layer-pruning-for-generative-reasoning-in-large-languag.md)**  
  実装：[✓](https://github.com/safal312/on-the-limits-of-layer-pruning) ・ リポジトリ内被引用：0  
  本研究は大規模言語モデルの層を丸ごと削る深さ方向の枝刈り（層 枝刈り）が、分類課題と生成型推論課題で異なる品質低下を起こす原因を調べる。主な実験では、層の約25%を除去し、元モデルが生成した回答を教師にして再学習する。

- **2026-02 · [Neural Attention Search Linear: Towards Adaptive Token-Level Hybrid Attention Models](2026-2602.03681-neural-attention-search-linear-towards-adaptive-token-level-hybrid-atten.md)**  
  実装：[✓](https://github.com/automl/NeuralAttentionSearchLinear) ・ リポジトリ内被引用：0  
  NAtS-L（Neural 注意機構 Search Linear）は、従来の「ある層はソフトマックス注意、別の層は線形注意」という固定的な混成構成を、同じ層の中で入力トークン塊ごとに注意演算を選択する構成へ拡張した研究である。

- **2026-02 · [Learning Query-Aware Budget-Tier Routing for Runtime Agent Memory](2026-2602.06025-learning-query-aware-budget-tier-routing-for-runtime-agent-memory.md)**  
  実装：[✓](https://github.com/ViktorAxelsen/BudgetMem) ・ リポジトリ内被引用：0  
  従来の記憶方式は履歴全体を事前に要約・索引化することが多いが、将来どの質問が来るかを知らずに情報を圧縮するため、不要な部分へ計算を費やしたり、後で必要になる詳細を失ったりする。

- **2026-02 · [HiDrop: Hierarchical Vision Token Reduction in MLLMs via Late Injection, Concave Pyramid Pruning, and Early Exit](2026-2602.23699-hidrop-hierarchical-vision-token-reduction-in-mllms-via-late-injection-c.md)**  
  実装：[✓](https://github.com/EIT-NLP/HiDrop) ・ リポジトリ内被引用：0  
  LLaVA型の画像言語モデルは、画像符号化器が出力した多数の視覚特徴を言語モデルの入力列へ結合する。この前提では、視覚情報の統合が実際に行われる層と計算資源を費やす層が一致しない。

- **2026-02 · [Focus-Scan-Refine: From Human Visual Perception to Efficient Visual Token Pruning](2026-2602.05809-focus-scan-refine-from-human-visual-perception-to-efficient-visual-token.md)**  
  実装：[✓](https://github.com/ILOT-code/FSR) ・ リポジトリ内被引用：0  
  高解像度画像や複数フレームの動画ではトークン数が増え、事前充填の演算量、注意機構に必要な記憶量、鍵・値キャッシュ（KV キャッシュ）の容量が増加する。LLaVA-1.5-7Bで視覚トークンを576個から64個へ削減すると、9種類の評価を正規化した平均性能保持率は96.1%であり、比較対象のCDPrunerは95.7%、VisPrunerは93.5%だった。

- **2026-02 · [Efficient Encoder-Free Fourier-based 3D Large Multimodal Model](2026-2602.23153-efficient-encoder-free-fourier-based-3d-large-multimodal-model.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Fase3Dは、重い専用3Dエンコーダを使わず、浅い多層パーセプトロン（MLP）と幾何的なスーパーポイント（superpoint）集約、空間充填曲線（Space-Filling Curve、SFC）に基づく1次元整列、高速フーリエ変換（Fast Fourier Transform、FFT）による文脈混合、疎グラフを用いたトークン統合で…

- **2026-02 · [DySL-VLA: Efficient Vision-Language-Action Model Inference via Dynamic-Static Layer-Skipping for Robot Manipulation](2026-2602.22896-dysl-vla-efficient-vision-language-action-model-inference-via-dynamic-st.md)**  
  実装：[✓](https://github.com/PKU-SEC-Lab/DYSL_VLA) ・ リポジトリ内被引用：0  
  DySL-VLAは、視覚言語行動モデル（Vision-Language-Action モデル; VLA）の大規模言語モデル（Large Language モデル; LLM）基盤に対し、必要な層だけを実行してロボット制御の推論遅延を削減する方式である。

- **2026-02 · [Does Your Reasoning Model Implicitly Know When to Stop Thinking?](2026-2602.08354-does-your-reasoning-model-implicitly-know-when-to-stop-thinking.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  そこで本論文は、モデルの確率分布に「適切な時点で終了する」兆候がすでに含まれているのかを調べ、その情報を取り出す生成方式と学習方式を設計する。

- **2026-02 · [Conformal Thinking: Risk Control for Reasoning on a Compute Budget](2026-2602.03814-conformal-thinking-risk-control-for-reasoning-on-a-compute-budget.md)**  
  実装：[✓](https://github.com/xidulu/reasoning_risk_control/) ・ リポジトリ内被引用：0  
  Conformal Thinkingは、推論を伴う大規模言語モデル（reasoning LLM）の思考トークンを、精度への影響を制御しながら減らす停止規則を提案する。

- **2026-02 · [CoMoL: Efficient Mixture of LoRA Experts via Dynamic Core Space Merging](2026-2603.00573-comol-efficient-mixture-of-lora-experts-via-dynamic-core-space-merging.md)**  
  実装：[✓](https://github.com/DCDmllm/CoMoL) ・ リポジトリ内被引用：0  
  本論文は、低ランク適応（LoRA）を複数の専門家へ拡張する際に、専門家の数に比例して増える学習パラメータと計算量を抑えつつ、トークン単位の細かな経路選択を維持するCoMoLを提案する。

- **2026-02 · [AttnPO: Attention-Guided Process Supervision for Efficient Reasoning](2026-2602.09953-attnpo-attention-guided-process-supervision-for-efficient-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AttnPO（注意機構-guided Policy Optimization）は、モデルが最終回答を生成するときに過去の思考のどの部分へ注意しているかを、思考段階ごとの重要性の代理指標として使う。

- **2026-02 · [AgentArk: Distilling Multi-Agent Intelligence into a Single LLM Agent](2026-2602.03955-agentark-distilling-multi-agent-intelligence-into-a-single-llm-agent.md)**  
  実装：[✓](https://github.com/AIFrontierLab/AgentArk) ・ リポジトリ内被引用：0  
  複数のLLMエージェントが同じ問題を検討し、相互に批判・訂正して最終回答を合意する方式は、単独モデルより複雑な推論を改善できることがある。Qwen3、Gemma3、Llama3系を含む120の実験で、単一モデルに比べた推論品質の改善と、学習信号の種類・学生モデルの規模・教師エージェント数の影響を分析する。

- **2026-01 · [Why Attention Patterns Exist: A Unifying Temporal Perspective Analysis](2026-2601.21709-why-attention-patterns-exist-a-unifying-temporal-perspective-analysis.md)**  
  実装：[✓](https://github.com/MIRALab-USTC/LLM-TAPPA) ・ リポジトリ内被引用：0  
  KVキャッシュ圧縮では検索型の不規則な注意が多い、自己類似度の低い層に多めのKV予算を配る。

- **2026-01 · [When to Think Fast and Slow? AMOR: Adaptive Entropy Gate for Hybrid Models](2026-2602.13215-when-to-think-fast-and-slow-amor-adaptive-entropy-gate-for-hybrid-models.md)**  
  実装：[✓](https://github.com/HaoranZhengRaul/AMOR) ・ リポジトリ内被引用：0  
  AMOR（適応的 Metacognitive Output Router）は、Mamba2またはGated DeltaNetの再帰型言語モデルに、トークンごとに必要性を判定して実行する注意ブロックを追加する方式である。ゲートの発火率は学習中に約40%となり、発火しない位置では注意の問い合わせと出力計算を省略する。

- **2026-01 · [VTC-R1: Vision-Text Compression for Efficient Long-Context Reasoning](2026-2601.22069-vtc-r1-vision-text-compression-for-efficient-long-context-reasoning.md)**  
  実装：[✓](https://github.com/w-yibo/VTC-R1) ・ リポジトリ内被引用：0  
  本研究は、長い思考履歴を文字列として保持し続ける代わりに、既に生成した推論を画像へ描画して次の推論段階へ渡す視覚・テキスト圧縮（Vision-Text Compression; VTC）を提案する。約1億8100万のテキストトークンに相当する履歴を約5400万の視覚トークンとして表し、集計上3.4倍のトークン圧縮を得る。

- **2026-01 · [Towards Understanding Best Practices for Quantization of Vision-Language Models](2026-2601.15287-towards-understanding-best-practices-for-quantization-of-vision-language.md)**  
  実装：[✓](https://github.com/gautomdas/mmq) ・ リポジトリ内被引用：0  
  本論文は、視覚言語モデル（Vision-Language モデル; VLM）を低ビット化するとき、視覚符号化器（Vision Transformer; ViT）、視覚と言語の接続器、言語モデル（LLM）のどこを何ビットにするのが有利かを、複数のタスクと量子化方式で比較する実証研究である。

- **2026-01 · [Singular Proxies for Adaptive Caching in Diffusion Language Models](2026-2602.02544-singular-proxies-for-adaptive-caching-in-diffusion-language-models.md)**  
  実装：[✓](https://github.com/wenhao728/spa-cache) ・ リポジトリ内被引用：0  
  自己注意（self-注意機構）が双方向であるため、ある位置のトークンを更新すると別の位置の隠れ状態にも影響が及び、自己回帰型モデルのように過去の鍵・値（KV）を常に固定したまま再利用することはできない。LLaDA-8BのMBPPでは通常復号5.75トークン/秒に対し46.12トークン/秒（8.0倍）で、正解率は39.20から39.00へ変化した。

- **2026-01 · [Routing with Generated Data: Annotation-Free LLM Skill Estimation and Expert Selection](2026-2601.09692-routing-with-generated-data-annotation-free-llm-skill-estimation-and-exp.md)**  
  実装：[✓](https://github.com/tianyiniu/RoutingGenData) ・ リポジトリ内被引用：0  
  本論文は、課題の短い説明だけを使って生成モデルに質問・回答対を作らせる「生成データによる振分け（ルーティング with Generated Data; RGD）」を定式化し、その環境に適したCASCAL（Consensus-Aware Skill Clustering and Aggregation for LLMs）を提案する。

- **2026-01 · [ROMA: Real-time Omni-Multimodal Assistant with Interactive Streaming Understanding](2026-2601.10323-roma-real-time-omni-multimodal-assistant-with-interactive-streaming-unde.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ただし、これは継続的な入力処理の平均時間であり、発話内容の生成時間、ネットワーク遅延、音声合成、極端に長い履歴を含むシステム全体の最悪応答遅延ではない。YouCook2の実況開始時刻のF1は35.21で、比較するVideoLLM-onlineの18.82を上回る。

- **2026-01 · [Randomization Boosts KV Caching, Learning Balances Query Load: A Joint Perspective](2026-2601.18999-randomization-boosts-kv-caching-learning-balances-query-load-a-joint-per.md)**  
  実装：[✓](https://github.com/fzwark/KVRouting) ・ リポジトリ内被引用：0  
  複数の大規模言語モデル（Large Language モデル, LLM）ワーカーが同じモデルを提供する場合、各ワーカーは過去の問い合わせの鍵・値キャッシュ（KV キャッシュ）を保持し、後続問い合わせが同じ接頭辞を持てば再計算を省ける。本論文は、この局所的なキャッシュ削除と全体的な振分けを一つのオンライン問題としてモデル化し、二つのアルゴリズムを提案する。

- **2026-01 · [RadixMLP -- Intra-batch Deduplication for Causal Transformers](2026-2601.15013-radixmlp-intra-batch-deduplication.md)**  
  実装：[✓](https://github.com/michaelfeil/radix-mlp) ・ リポジトリ内被引用：0  
  RadixMLPは、同一バッチに入った複数の系列が長い接頭辞を共有している場合、共有部分の多層パーセプトロン（MLP）、層正規化（LayerNorm）、線形射影、埋め込みなどを何度も実行する無駄を削減する方式である。

- **2026-01 · [PLA-Serve: A Prefill-Length-Aware LLM Serving System](2026-a30e37ff7d4b-pla-serve-a-prefill-length-aware-llm-serving-system.md)**  
  実装：[✓](https://github.com/Jianshu-She/LAPS) ・ リポジトリ内被引用：0  
  プリフィル長で短要求と長要求を別キュー・別実行モードへ分離し、待機窓、CUDA Graph形状クラスタリング、動的GPU割当で短要求の待ちと長要求の干渉を同時に抑える。

- **2026-01 · [ModeX: Evaluator-Free Best-of-N Selection for Open-Ended Generation](2026-2601.02535-modex-evaluator-free-best-of-n-selection-for-open-ended-generation.md)**  
  実装：[✓](https://github.com/deeplearning-wisc/ModeX) ・ リポジトリ内被引用：0  
  しかし従来は、正解と照合できる数学問題なら多数決が使える一方、自由記述の要約やプログラムでは文字列の一致が品質を表さない。別の大規模言語モデルを採点器として呼ぶ方式は、その採点器の推論費用と誤判定を持ち込む。

- **2026-01 · [MHLA: Restoring Expressivity of Linear Attention via Token-Level Multi-Head](2026-2601.07832-mhla-restoring-expressivity-of-linear-attention-via-token-level-multi-he.md)**  
  実装：[✓](https://github.com/DAGroup-PKU/MHLA) ・ リポジトリ内被引用：0  
  MHLA（Multi-Head Linear 注意機構）は、系列長に対して計算量が線形に増える注意機構を維持しながら、従来の線形注意（linear 注意機構）で失われるトークン間の選択性を回復する構造である。DeiT-TのImageNet-1K正答率は通常の線形注意69.8%からMHLA75.8%へ、通常のソフトマックス注意72.2%も上回った。

- **2026-01 · [Low-Rank Key Value Attention](2026-2601.11471-low-rank-key-value-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低ランク鍵・値注意（Low-Rank Key Value 注意機構; LRKV）は、Transformerの各注意ヘッドが別々に保存する鍵・値（key/value; KV）キャッシュの重複を減らすため、各層に一組の共有射影を持たせ、ヘッド固有の違いだけを低ランク残差で表す注意機構である。

- **2026-01 · [LOOKAT: Lookup-Optimized Key-Attention for Memory-Efficient Transformers](2026-2601.10155-lookat-lookup-optimized-key-attention-for-memory-efficient-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LOOKATは、自己回帰Transformerの注意得点計算を、ベクトル検索における内積類似度検索として扱い、キーを圧縮したまま注意得点を計算する方式である。GPT-2の第1注意層で、64次元のキーを2個の1バイト符号へ圧縮すると、キー表現は128バイトから2バイトへ減り、キー単体の表現上の圧縮率は64倍となる。

- **2026-01 · [LLM KV Cache Storage Using CXL Memory](2026-4885970e907b-llm-kv-cache-storage-using-cxl-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  vLLMとLMCacheのKVキャッシュを4種類のCXLメモリへ退避して実機比較し、DRAM型・プール型CXLが長文脈でシステムDRAMに近い性能を保ち、122K入力でGPU VRAM比約9倍の要求スループットを示す。

- **2026-01 · [JuDi: Revisiting Judge Decoding from First Principles via Training-Free Distributional Divergence](2026-2601.04766-judi-revisiting-judge-decoding-from-first-principles-via-training-free-d.md)**  
  実装：[✓](https://github.com/sunshy-1/JuDi) ・ リポジトリ内被引用：0  
  著者らは学習済み判定器の「重要トークン」スコアが、二つのモデルのカルバック・ライブラー発散（Kullback–Leibler divergence; KL発散）と相関することを確認し、KL値が閾値を下回る候補を受理する学習不要の方式JuDiを提案する。

- **2026-01 · [Iterative Structured Pruning for Large Language Models with Multi-Domain Calibration](2026-2601.02674-iterative-structured-pruning-for-large-language-models-with-multi-domain.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は大規模言語モデル（LLM）の構造化枝刈り（structured 枝刈り）で、削除すべきチャネルの選択をより正確にするため、多領域の較正データと反復的な重要度の再計算を組み合わせる。Qwen2.5-32Bを50%構造化枝刈りした6課題ゼロショット評価では、FLAPの平均36.59点に対して提案法は46.65点となる。

- **2026-01 · [Is Finer Better? The Limits of Microscaling Formats in Large Language Models](2026-2601.19026-is-finer-better-the-limits-of-microscaling-formats-in-large-language-mod.md)**  
  実装：[✓](https://github.com/iclr2016codeshare/microscaling) ・ リポジトリ内被引用：0  
  本論文は、大規模言語モデルの重みと活性を4ビット浮動小数点（FP4）へ圧縮する際、「量子化のブロックを小さくするほど精度が良くなる」という一般的な期待が破れる条件を明らかにした研究である。

- **2026-01 · [GlimpRouter: Efficient Collaborative Inference by Glimpsing One Token of Thoughts](2026-2601.05110-glimprouter-efficient-collaborative-inference-by-glimpsing-one-token-of-.md)**  
  実装：[✓](https://github.com/Zengwh02/GlimpRouter) ・ リポジトリ内被引用：0  
  大規模推論モデルは長い思考過程を生成するため、回答までの待ち時間と計算費用が大きい。トークン単位で常時切り替えると、判定とモデル切替が頻繁になりやすい。

- **2026-01 · [Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning](2026-2601.09708-fast-thinkact-efficient-vision-language-action-reasoning-via-verbalizabl.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Fast-ThinkActは、視覚・言語・行動モデル（Vision-Language-Action モデル、VLA）の推論に必要な長い文章形式の思考列を、少数の連続潜在表現へ圧縮する研究である。

- **2026-01 · [Fast Forward: Accelerating LLM Prefill with Predictive FFN Sparsity](2026-2602.00397-fast-forward-accelerating-llm-prefill-with-predictive-ffn-sparsity.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FastForwardは、大規模言語モデル（Large Language モデル; LLM）の入力一括処理（プリフィル）におけるフィードフォワード網（Feed-順伝播 Network; FFN）の演算を、入力文脈に応じてブロック単位で省く方式である。

- **2026-01 · [Efficient Paths and Dense Rewards: Probabilistic Flow Reasoning for Large Language Models](2026-2601.09260-efficient-paths-and-dense-rewards-probabilistic-flow-reasoning-for-large.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  標準的な思考の連鎖は、最終解答の正誤だけでは途中の推論ステップの有用性を直接測れず、冗長な言い換えや誤った分岐を含みやすい。CoT-Flowは、問題xと時点iまでの生成列sを持つ状態Iiにおいて、正解yの負の対数確率 D(Ii)=-log p(y\|Ii) を難しさと定義する。

- **2026-01 · [ConfSpec: Efficient Step-Level Speculative Reasoning via Confidence-Gated Verification](2026-2602.18447-confspec-efficient-step-level-speculative-reasoning-via-confidence-gated.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  小型の草稿モデルが作った途中の推論を大型の対象モデルで検証する既存方式は、単語列が異なっていても意味が同じである推論を扱える一方、すべてのステップを高価な検証器へ送ると加速効果が弱くなる。論文の表2では、DeepSeek-R1-Distill 1.5B/32B構成で5課題平均の高速化が1.68倍、平均正答率が対象モデル81.99%に対して81.51%である。

- **2026-01 · [ArcAligner: Adaptive Recursive Aligner for Compressed Context Embeddings in RAG](2026-2601.05038-arcaligner-adaptive-recursive-aligner-for-compressed-context-embeddings-.md)**  
  実装：[✓](https://github.com/liunian-Jay/ArcAligner) ・ リポジトリ内被引用：0  
  ArcAlignerは、検索拡張生成（Retrieval-Augmented Generation; RAG）で取得した長文書を、少数の連続ベクトルへ圧縮した後の「情報が残っていても生成モデルが読めない」という問題を扱う。約24倍の文脈圧縮条件で、HotpotQAのF1は34.92、同じ論文で比較したCOCOMの16倍圧縮は31.77となった。

- **2025-12 · [Zero-Overhead Introspection for Adaptive Test-Time Compute](2025-2512.01457-zero-overhead-introspection-for-adaptive-test-time-compute.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  数学推論などでは、同じ質問に対して複数の回答候補を生成し、多数決（Majority Voting）や最良候補選択（Best-of-N）で正答率を高められる。しかし固定個数の候補を最後まで生成すると、既に正しい回答が得られそうな簡単な質問でも計算を浪費し、失敗しそうな長い推論系列が全体の応答時間を引き延ばす。外部の報酬モデルを推論時に追加で走らせる必要はない。

- **2025-12 · [You Only Need Your Transformer 25% of the Time: Meaning-First Execution for Eliminating Unnecessary Inference](2025-2601.00847-you-only-need-your-transformer-25-of-the-time-meaning-first-execution-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の量子化、枝刈り、KVキャッシュ最適化、投機的復号は、モデルを実行することを前提に一回当たりの計算費用を削減する。論文は、1,000件の要求を用いた主実験で781件（78.1%）のTransformer実行を回避し、残り219件について無条件実行と完全一致する出力を得たと報告する。

- **2025-12 · [XLM: A Python package for non-autoregressive language models](2025-2512.17065-xlm-a-python-package-for-non-autoregressive-language-models.md)**  
  実装：[✓](https://github.com/dhruvdcoder/xlm-core) ・ リポジトリ内被引用：0  
  これに対して、非自己回帰言語モデルにはマスク拡散、挿入型生成、編集型生成など複数の方式がある。

- **2025-12 · [UniQL: Unified Quantization and Low-rank Compression for Adaptive Edge LLMs](2025-2512.03383-uniql-unified-quantization-and-low-rank-compression-for-adaptive-edge-ll.md)**  
  実装：[✓](https://github.com/enyac-group/UniQL) ・ リポジトリ内被引用：0  
  端末上で大規模言語モデル（LLM）を実行する際には、モデルの重みだけでなく、実行時の一時領域やほかのアプリケーションが共有するメモリも考慮する必要がある。4ビット量子化だけで端末に収まるモデルを作れても、別のアプリケーションが起動して空きメモリが減れば、固定サイズの量子化モデルは実行不能になる。

- **2025-12 · [Script: Graph-Structured and Query-Conditioned Semantic Token Pruning for Multimodal Large Language Models](2025-2512.01949-script-graph-structured-and-query-conditioned-semantic-token-pruning-for.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  手法は、余弦類似度の二部グラフを用いて冗長な視覚トークンを削るグラフ構造化枝刈り（Graph-Structured Pruning; GSP）と、質問との関連性に加えて特徴の多様性を考慮する質問条件付き意味枝刈り（Query-Conditioned Semantic Pruning; QCSP）から成る。

- **2025-12 · [RouteRAG: Efficient Retrieval-Augmented Generation from Text and Graph via Reinforcement Learning](2025-2512.09487-routerag-efficient-retrieval-augmented-generation-from-text-and-graph-vi.md)**  
  実装：[✓](https://github.com/YucanGuo/RouteRAG) ・ リポジトリ内被引用：0  
  RouteRAGは、言語モデルが推論途中に外部知識を調べる際、通常の文書検索、知識グラフ検索、両者の混合検索を状況に応じて切り替える方策を強化学習で獲得する検索拡張生成方式である。

- **2025-12 · [Post-Training Quantization of OpenPangu Models for Efficient Deployment on Atlas A2](2025-2512.23367-post-training-quantization-of-openpangu-models-for-efficient-deployment-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単なる量子化誤差の研究ではなく、Ascendの演算子テンプレートライブラリCATLASSへ、量子化された重み配置、逆量子化、行列積を組み込み、不要な形式変換を避ける実行経路を構築する点が推論基盤上の寄与である。実測の前処理（プリフィル）では、バッチ32のFP16遅延5419msがINT8で3611msへ減少し、1.50倍の高速化となる。

- **2025-12 · [Parallel Token Prediction for Language Models](2025-2512.21323-parallel-token-prediction-for-language-models.md)**  
  実装：[✓](https://github.com/mandt-lab/ptp) ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は小さなモデルに先読みさせて大きなモデルでまとめて検証するが、草案モデル自身が1トークンずつ順次生成する費用は残る。Vicuna-7Bを教師として学習したPTPは、RTX A6000単体でSpecBenchの6種類の文章生成課題において、通常の自己回帰生成比で平均2.40倍の実時間高速化を報告した。

- **2025-12 · [Mesh-Attention: A New Communication-Efficient Distributed Attention with Improved Data Locality](2025-2512.20968-mesh-attention-a-new-communication-efficient-distributed-attention-with-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Mesh-注意機構は、数十万から100万トークンの系列に対して注意機構を多数のGPUへ分割する際、各GPUが受け取る問い合わせ（Q）と鍵・値（KV）の転送量を同時に抑える分散注意アルゴリズムである。

- **2025-12 · [MatKV: Trading Compute for Flash Storage in LLM Inference](2025-2512.22195-matkv-trading-compute-for-flash-storage-in-llm-inference.md)**  
  実装：[✓](https://github.com/kunwooshin/MatKV) ・ リポジトリ内被引用：0  
  MatKVは、検索拡張生成（Retrieval-Augmented Generation、RAG）の質問ごとに同じ文書を何度もGPUで事前処理する無駄を、文書単位の鍵・値（KV）キャッシュをストレージへ永続化することで減らす方式である。

- **2025-12 · [LLMCache: Layer-Wise Caching Strategies for Accelerated Reuse in Transformer Inference](2025-2512.16843-llmcache-layer-wise-caching-strategies-for-accelerated-reuse-in-transfor.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMCacheは、入力文字列が完全一致しなくても意味的に似ていればTransformer内部の中間活性を再利用できると考え、各層の出力を入力の指紋とともに保存する推論方式である。

- **2025-12 · [From Context to EDUs: Faithful and Structured Context Compression via Elementary Discourse Unit Decomposition](2025-2512.14244-from-context-to-edus-faithful-and-structured-context-compression-via-ele.md)**  
  実装：[✓](https://github.com/DeepLangAI/LingoEDU) ・ リポジトリ内被引用：0  
  LingoEDUは、長い文章を単純にトークン単位で間引くのではなく、まず原文の談話構造を木として抽出し、その木から質問に必要な範囲だけを選択して入力を短縮する、明示的な文脈圧縮方式である。著者は248文書を人手で構造注釈したStructBenchを公開し、木編集距離4.77、文書単位完全一致率49.60%を報告した。

- **2025-12 · [Fairy2i: Training Complex LLMs from Real LLMs with All Parameters in {±1, ±i}](2025-2512.02901-fairy2i-training-complex-llms-from-real-llms-with-all-parameters-in-1-i.md)**  
  実装：[✓](https://github.com/PKULab1806/Fairy2i-W2) ・ リポジトリ内被引用：0  
  Fairy2iは、通常の実数値で学習済みのTransformerを、量子化前の出力を変えずに複素数の広義線形（widely-linear）表現へ変換する。実効2ビットのFairy2i-W2はC4検証集合の困惑度（Perplexity; PPL）7.85、ARC-Easyなど五つのゼロショット課題平均62.00%を示した。

- **2025-12 · [DiRL: An Efficient Post-Training Framework for Diffusion Language Models](2025-2512.22234-dirl-an-efficient-post-training-framework-for-diffusion-language-models.md)**  
  実装：[✓](https://github.com/OpenMOSS/DiRL) ・ リポジトリ内被引用：0  
  提案はこの問題を、ブロック間は自己回帰的、ブロック内は並列的な拡散という構造で扱う。著者は、学習処理の遅延を約6分の1にし、学習・推論の統合によって全体処理量を約2.5倍改善したと報告する。

- **2025-12 · [CHIME: Chiplet-based Heterogeneous Near-Memory Acceleration for Edge Multimodal LLM Inference](2026-2601.19908-chime-chiplet-near-memory-mllm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚入力で膨らむKVキャッシュと演算重みをDRAM・RRAMへ役割分担し、近メモリ実行と局所性を保つ演算融合で端末MLLM推論のデータ移動を抑える設計を示す。

- **2025-12 · [Can LLMs Predict Their Own Failures? Self-Awareness via Internal Circuits](2025-2512.20578-can-llms-predict-their-own-failures-self-awareness-via-internal-circuits.md)**  
  実装：[✓](https://github.com/Amirhosein-gh98/Gnosis) ・ リポジトリ内被引用：0  
  回答文中の自己申告の確信度も、誤った回答に対して高い確信を示す問題がある。提案方式は、生成モデル本体の重みを変更せず、生成中に現れる隠れ状態（Hidden States）と注意重み（注意機構 Maps）の時系列的な特徴を抽出する。これは判定器の時間比較であり、回答を生成する言語モデル全体が37倍または99倍速くなるという意味ではない。

- **2025-12 · [Asynchronous Reasoning: Training-Free Interactive Thinking LLMs](2025-2512.10931-asynchronous-reasoning-training-free-interactive-thinking-llms.md)**  
  実装：[✓](https://github.com/yandex-research/AsyncReasoning) ・ リポジトリ内被引用：0  
  推論時計算を増やすほど対話の即応性が下がるという問題である。二つの流れがそれぞれ通常の「入力→思考→回答」という順序で文脈を見ているように、鍵・値キャッシュ（KV キャッシュ）の論理的な並びを切り替える。

- **2025-11 · [T-SAR: A Full-Stack Co-design for CPU-Only Ternary LLM Inference via In-Place SIMD ALU Reorganization](2025-2511.13676-t-sar-a-full-stack-co-design-for-cpu-only-ternary-llm-inference-via-in-p.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  T-SARは、重みを−1、0、+1の三値に制約した大規模言語モデル（LLM）を、専用の大きな行列演算器なしにCPUで高速実行するための、アルゴリズム・命令セット・マイクロアーキテクチャ・ソフトウェアの協調設計である。

- **2025-11 · [SpecQuant: Spectral Decomposition and Adaptive Truncation for Ultra-Low-Bit LLMs Quantization](2025-2511.11663-specquant-spectral-decomposition-and-adaptive-truncation-for-ultra-low-b.md)**  
  実装：[✓](https://github.com/Kishon-zzx/SpecQuant) ・ リポジトリ内被引用：0  
  本研究は、大規模言語モデル（LLM）の重みと活性を同時に4ビット程度へ圧縮するときに生じる、外れ値による量子化誤差を低減する手法を扱う。

- **2025-11 · [Seer Self-Consistency: Advance Budget Estimation for Adaptive Test-Time Scaling](2025-2511.09345-seer-self-consistency-advance-budget-estimation-for-adaptive-test-time-s.md)**  
  実装：[✓](https://github.com/noforit/SeerSC) ・ リポジトリ内被引用：0  
  複数の推論経路を生成して最頻回答を選ぶ自己整合（自己整合性; SC）は、数学問題などで単一路線の思考連鎖より正解率を上げられる。各問題へ一律に $N$ 経路を割り当てると、容易な問題へも大量のトークンを使う。

- **2025-11 · [Scaling Graph Chain-of-Thought Reasoning: A Multi-Agent Framework with Efficient LLM Serving](2025-2511.01633-graph-cot-multi-agent-efficient-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Graph-CoTを分類・推論・行動・検索へ分業し、頂点単位KV再利用、優先度追い出し、検索と生成の重畳を組み合わせ、遅延最大90.3%減・スループット最大15.1倍を報告。

- **2025-11 · [Optimal Self-Consistency for Efficient Reasoning with Large Language Models](2025-2511.12309-optimal-self-consistency-for-efficient-reasoning-with-large-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかし、全問題へ同じ回数だけ生成を繰り返すと、少数の試行で答えが安定する簡単な問題にも計算を使い続け、回答が割れる難しい問題に十分な予算を残せない。固定回数の生成、回答の信頼度に応じて停止する方式、問題間で生成回数を再配分する方式の違いを整理し、予算が少ない段階で有効な方法と、予算が大きい段階で有効な方法を組み合わせるBlend-ASCを提案する。

- **2025-11 · [OckBench: Measuring the Efficiency of LLM Reasoning](2025-2511.05722-ockbench-measuring-the-efficiency-of-llm-reasoning.md)**  
  実装：[✓](https://github.com/OckBench/OckBench) ・ リポジトリ内被引用：0  
  従来の正答率だけではこの差が見えず、ハードウェアの処理量だけではモデル自身がどれほど冗長に推論するかを分離できない。

- **2025-11 · [NEZHA: A Zero-sacrifice and Hyperspeed Decoding Architecture for Generative Recommendations](2025-2511.18793-nezha-a-zero-sacrifice-and-hyperspeed-decoding-architecture-for-generati.md)**  
  実装：[✓](https://github.com/Applied-Machine-Learning-Lab/WWW2026_NEZHA) ・ リポジトリ内被引用：0  
  候補を広く集めるために多数のビームを保持して逐次復号すると、出力は3トークン程度でも主モデルを何度も呼び出すため遅延が大きい。外部ドラフトモデルを必要とせず、識別子の位置を表すプレースホルダーと、選択した前トークンを反映する状態遷移によって、意味識別子の順序依存性を維持する。

- **2025-11 · [NeuroPath: Neurobiology-Inspired Path Tracking and Reflection for Semantically Coherent Retrieval](2025-2511.14096-neuropath-neurobiology-inspired-path-tracking-and-reflection-for-semanti.md)**  
  実装：[✓](https://github.com/KennyCaty/NeuroPath) ・ リポジトリ内被引用：0  
  知識グラフ（Knowledge Graph; KG）上の隣接性だけを重視する既存方式は、質問に答えるための関係の向きや意味を無視して文書を集める場合がある。原著の多段質問応答3データセットでは、主要なグラフ検索方式に比べて平均Recall@2を16.3%、Recall@5を13.5%改善したと報告する。

- **2025-11 · [INTERLACE: Interleaved Layer Pruning and Efficient Adaptation in Large Vision-Language Models](2025-2511.19676-interlace-interleaved-layer-pruning-and-efficient-adaptation-in-large-vi.md)**  
  実装：[✓](https://github.com/pmadinei/Interlace) ・ リポジトリ内被引用：0  
  3層組は重複しないよう選択し、同じ層が複数の役割を持たないようにする。原著の表1では、Qwen3-VL-8Bの言語デコーダ層を25%削除し、FineVisionの1%を1エポック微調整すると、12課題平均の元モデルに対する性能保持率は86.1%だった。

- **2025-11 · [GoCkpt: Gradient-Assisted Multi-Step overlapped Checkpointing for Efficient LLM Training](2025-2511.07035-gockpt-gradient-assisted-multi-step-overlapped-checkpointing-for-efficient-llm-training.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  チェックポイント転送を複数学習ステップへ分散し、低精度勾配でCPU側の版を一貫状態へ再構築することで、GPU停止を大幅に隠して学習スループットを最大約40%改善する。

- **2025-11 · [Global Resolution: Optimal Multi-Draft Speculative Sampling via Convex Minimization](2025-2511.15898-global-resolution-optimal-multi-draft-speculative-sampling-via-convex-mi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Global Resolutionは、複数の草案トークンを同じ次トークン位置に提示する投機的サンプリングに対し、目標モデルの出力分布からの逸脱を制御しながら、草案のいずれかを受理できる確率を最大化する検証規則を計算する研究である。語彙数をVとすると候補n組の数はVのn乗であり、n=2でも通常の大語彙では汎用ソルバーで解けない。

- **2025-11 · [From Prompts to Power: Measuring the Energy Footprint of LLM Inference](2025-2511.05597-from-prompts-to-power-measuring-the-energy-footprint-of-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本サーベイとの接点は、LLM推論サービング（serving）の省エネルギー化、モデル・GPUの配置選択、バッチ処理、KVキャッシュ容量、量子化・実行方式の設計判断である。

- **2025-11 · [Federated Attention: A Distributed Paradigm for Collaborative LLM Inference over Edge Networks](2025-2511.02647-federated-attention-a-distributed-paradigm-for-collaborative-llm-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Federated 注意機構（FedAttn）は、この協調推論を注意機構の段階で分散する方式として提案された。

- **2025-11 · [Fast and Expressive Multi-Byte Prediction with Probabilistic Circuits](2025-2511.11346-fast-and-expressive-multi-byte-prediction-with-probabilistic-circuits.md)**  
  実装：[✓](https://github.com/april-tools/mtpc) ・ リポジトリ内被引用：0  
  本論文は、バイト単位の大規模言語モデルで複数の将来バイトを同時に予測する際、予測位置間の依存関係と候補生成の遅延を同時に制御する確率回路方式MtPCを提案する。

- **2025-11 · [CLaRa: Bridging Retrieval and Generation with Continuous Latent Reasoning](2025-2511.18659-clara-bridging-retrieval-and-generation-with-continuous-latent-reasoning.md)**  
  実装：[✓](https://github.com/apple/ml-clara) ・ リポジトリ内被引用：0  
  CLaRa（Continuous Latent Reasoning）は、文書を少数の連続値メモリトークンへ圧縮し、その表現を文書検索と生成の双方に用いる。Mistral-7Bで16倍圧縮したSCPは、4質問応答課題の通常検索条件において平均CEM 38.96%を記録し、PISCOの37.83%を上回る。

- **2025-11 · [C3PO: Optimized Large Language Model Cascades with Probabilistic Cost Constraints for Reasoning](2025-2511.07396-c3po-optimized-large-language-model-cascades-with-probabilistic-cost-con.md)**  
  実装：[✓](https://github.com/AntonValk/C3PO-LLM) ・ リポジトリ内被引用：0  
  すべての質問を最も高価なモデルへ送るのではなく、小型モデルが容易な質問へ回答し、難しい質問だけを高性能モデルへ順に送る方式をカスケード推論（cascaded inference）という。

- **2025-11 · [Adaptive Layer-Wise Transformations for Post-Training Quantization of Large Language Models](2025-2511.17809-adaptive-layer-wise-transformations-for-post-training-quantization-of-la.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの事後量子化（post-学習 量子化、PTQ）では、重みと活性値を低ビット整数へ丸める際、少数の外れ値に量子化範囲が引きずられて通常値の分解能が不足する。

### 2年前（2024-11〜2025-10）

- **2025-01 · [FlashInfer: Efficient and Customizable Attention Engine for LLM Inference Serving](2025-2501.01005-flashinfer-attention-engine-serving.md)**  
  実装：[✓](https://github.com/flashinfer-ai/flashinfer) ・ リポジトリ内被引用：120  
  多様なKV配置と注意派生形をブロック疎形式と実行時コンパイルで統一し、可変系列長を固定CTAへ動的に負荷均衡しながらCUDAグラフ互換性も保つ、LLMサービング向け高性能注意エンジン。

- **2025-04 · [SpinQuant: LLM quantization with learned rotations](2025-2405.16406-spinquant-llm-quantization-with-learned-rotations.md)**  
  実装：[✓](https://github.com/facebookresearch/SpinQuant) ・ リポジトリ内被引用：73  
  外れ値が低ビット量子化の誤差を大きくする問題に対して、全精度の機能を保つ旋回行列を学習し、重み・活性値・KVキャッシュの量子化に合わせる。

- **2024-12 · [Gated Delta Networks: Improving Mamba2 with Delta Rule](2024-2412.06464-gated-delta-networks-improving-mamba2-with-delta-rule.md)**  
  実装：[✓](https://github.com/NVlabs/GatedDeltaNet) ・ リポジトリ内被引用：59  
  本論文は、長文脈を固定容量の状態へ圧縮する線形再帰言語モデルが、記憶の保持と更新を両立しにくい問題を扱う。

- **2025-08 · [Dream 7B: Diffusion Large Language Models](2025-2508.15487-dream-7b-diffusion-large-language-models.md)**  
  実装：[✓](https://github.com/DreamLM/Dream) ・ リポジトリ内被引用：55  
  自己回帰モデルから初期化した70億拡散言語モデルで、系列全体の反復復元により計画課題と任意順生成を強化し、推論反復数で品質と速度を調整する。

- **2025-03 · [Block Diffusion: Interpolating Between Autoregressive and Diffusion Language Models](2025-2503.09573-block-diffusion-interpolating-between-autoregressive-and-diffusion-langu.md)**  
  実装：[✓](https://github.com/kuleshov-group/bd3lms) ・ リポジトリ内被引用：50  
  マスク率をデータに応じて区間制限する学習方式と、清浄系列・雑音系列を特殊注意で同時処理する実装を導入した。

- **2025-09 · [Fast-dLLM v2: Efficient Block-Diffusion LLM](2025-2509.26328-fast-dllm-v2-block-diffusion-hierarchical-cache.md)**  
  実装：[✓](https://github.com/NVlabs/Fast-dLLM/tree/main/v2) ・ リポジトリ内被引用：32  
  自己回帰モデルをブロック拡散へ少量追加学習し、ブロック間KVキャッシュとブロック内DualCache、信頼度並列復号を階層化して品質を保ちながら生成を高速化する。

- **2025-03 · [DivPrune: Diversity-based Visual Token Pruning for Large Multimodal Models](2025-2503.02175-divprune-diversity-based-visual-token-pruning-for-large-multimodal-model.md)**  
  実装：[✓](https://github.com/vbdi/divprune) ・ リポジトリ内被引用：25  
  提案方式は、情報量が高そうな個々のトークンを選ぶのではなく、選んだトークン同士が似過ぎないようにすることで、短い視覚列に異なる意味的領域を残そうとする。提案された距離選択を、言語モデルの最初の層より前、または途中層の視覚対応隠れ状態へ挿入できるが、主要な実験で最も良好だったのは最初の層の前に削減する構成である。

- **2025-07 · [Step-3 is Large yet Affordable: Model-system Co-design for Cost-effective Decoding](2025-2507.19427-step-3-is-large-yet-affordable-model-system-co-design-for-cost-effective.md)**  
  実装：[✓](https://github.com/stepfun-ai/StepMesh) ・ リポジトリ内被引用：20  
  単純に総パラメータや活性パラメータを減らすのではなく、モデルの注意機構とサービング時のGPU配置を一緒に設計し、長い思考系列の復号費用を下げる。

- **2025-02 · [Stop Looking for Important Tokens in Multimodal Language Models: Duplication Matters More](2025-2502.11494-stop-looking-for-important-tokens-in-multimodal-language-models-duplicat.md)**  
  実装：[✓](https://github.com/ZichenWen1/DART) ・ リポジトリ内被引用：20  
  従来は注意重みを使って重要そうなトークンを残す方式が多かった。LLaVA-Next-7Bの画像トークンを2880から320へ削減した条件では、総推論時間が36分16秒から18分13秒、事前充填時間が22分51秒から7分38秒へ短縮し、鍵値キャッシュは1512.1MBから168.0MBへ減少した。

- **2024-11 · [BatchLLM: Optimizing Large Batched LLM Inference with Global Prefix Sharing and Throughput-oriented Token Batching](2024-2412.03594-batchllm-optimizing-large-batched-llm-inference-with-global-prefix-shari.md)**  
  実装：[✓](https://github.com/microsoft/MixLLM/tree/batchllm_vllm_064) ・ リポジトリ内被引用：20  
  BatchLLMは、検索結果の説明文生成、広告文書の変換、推薦候補の採点など、数千件以上のプロンプトをまとめて処理する大規模言語モデル（LLM）の一括推論を対象とするシステムである。原著のMLSys 2026産業部門版は、NVIDIA A100とAMD MI200上で、vLLMやSGLangに対して1.3～10.8倍の端点処理率改善を報告する。

- **2025-04 · [JITServe: SLO-aware LLM Serving with Imprecise Request Information](2025-2504.20068-jitserve-slo-aware-llm-serving-with-imprecise-request-information.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  不確かな出力長と依存関係を逐次更新し、期限達成に必要な最小帯域で要求を選ぶことで、サービス有効処理量を1.4〜6.3倍へ改善する。

- **2025-03 · [Qwen2.5-Omni Technical Report](2025-2503.20215-qwen2-5-omni-technical-report.md)**  
  実装：[✓](https://github.com/QwenLM/Qwen2.5-Omni) ・ リポジトリ内被引用：18  
  従来の視覚言語モデルや音声言語モデルを単に接続すると、動画フレームと音声の時間対応が失われやすく、音声出力のために全文の生成完了を待つ設計では初回音声までの遅延が大きい。原著の7B級モデルは、音声・映像を混合するOmniBenchで平均56.13%を示し、比較表のGemini 1.5 Proの42.91%を上回った。

- **2025-02 · [Comet: Fine-grained Computation-communication Overlapping for Mixture-of-Experts](2025-2502.19811-comet-fine-grained-computation-communication-overlapping-for-mixture-of-experts.md)**  
  実装：[✓](https://github.com/bytedance/flux) ・ リポジトリ内被引用：18  
  Cometは、混合専門家モデル（Mixture-of-Experts; MoE）の専門家を複数GPUへ分散配置したときに生じる通信待ちを、専門家の行列計算と重ねて隠すための実行系である。著者らは8基のH800および8基のL20からなるGPU環境で、Mixtral-8×7B、Qwen2-MoE、Phi-3.5-MoEなどを評価した。

- **2024-12 · [Token-Budget-Aware LLM Reasoning](2024-2412.18547-token-budget-aware-llm-reasoning.md)**  
  実装：[✓](https://github.com/GeniusHTX/TALE) ・ リポジトリ内被引用：18  
  そこで問題ごとに適切な予算を推定する推論時方式TALE-EPと、適切な予算下の短い正答を学習させる事後学習方式TALE-PTを提案する。

- **2024-11 · [DyCoke: Dynamic Compression of Tokens for Fast Video Large Language Models](2024-2411.15024-dycoke-dynamic-compression-of-tokens-for-fast-video-large-language-model.md)**  
  実装：[✓](https://github.com/KD-TAO/DyCoke) ・ リポジトリ内被引用：18  
  DyCokeは、動画を入力とする大規模言語モデルが多数のフレームを視覚トークンへ変換する際に生じる、注意計算と鍵・値（KV）キャッシュの増大を抑える学習不要の圧縮方式である。原著のLLaVA-OneVision 7Bによる32フレーム評価では、基準方式の一例当たり遅延2.30秒・メモリ34GBに対し、DyCokeは1.49秒・24GBとなった。

- **2025-08 · [Diffusion LLMs Can Do Faster-Than-AR Inference via Discrete Diffusion Forcing](2025-2508.09192-diffusion-llms-can-do-faster-than-ar-inference-via-discrete-diffusion-fo.md)**  
  実装：[✓](https://github.com/zhijie-group/Discrete-Diffusion-Forcing) ・ リポジトリ内被引用：16  
  離散拡散型の大規模言語モデル（diffusion LLM、dLLM）は、マスクされた複数トークンを一度の推論で同時に予測できる。しかし従来の双方向注意を使う拡散モデルでは、マスクの状態が反復ごとに変わるため、過去の鍵・値（KV）を自己回帰型モデルのように正確にキャッシュしにくい。確定済みのブロックのKVは変更されないため正確に再利用できる。

- **2025-01 · [Titans: Learning to Memorize at Test Time](2025-2501.00663-titans-learning-to-memorize-at-test-time.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  長い系列を処理する言語モデルでは、直近の情報を精密に参照する短期記憶と、遠い過去から重要な情報を残す長期記憶の両立が難しい。一方、線形再帰型モデルは過去を小さな状態へ圧縮できるが、重要な出来事をどのように選択して長く保持するかに制約がある。

- **2025-07 · [Your LLM Knows the Future: Uncovering Its Multi-Token Prediction Potential](2025-2507.11851-your-llm-knows-the-future-uncovering-its-multi-token-prediction-potentia.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  長い出力ではモデルの実行回数が多くなり、復号の逐次性が遅延の原因になる。提案方式は、入力末尾へ複数のマスク位置を追加し、同一の接頭辞から未来のトークンを予測させる。ただしこの数値は受理トークン数を生成反復数で割った指標であり、壁時計時間で5.35倍高速になったという実測ではない。

- **2025-04 · [KeyDiff: Key Similarity-Based KV Cache Eviction for Long-Context LLM Inference in Resource-Constrained Environments](2025-2504.15364-keydiff-key-similarity-based-kv-cache-eviction-for-long-context-llm-inference-in-resource-constrained-environments.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  注意重みではなくキーの幾何学的多様性を重要度代理として使う学習不要KV削除法で、ブロック長文処理でも厳密な容量上限を守りつつ、8K予算で約23%削減・LongBench差0.04%以下、既存削除法比で遅延最大30%短縮を示す。

- **2025-02 · [TokenSkip: Controllable Chain-of-Thought Compression in LLMs](2025-2502.12067-tokenskip-controllable-chain-of-thought-compression-in-llms.md)**  
  実装：[✓](https://github.com/hemingkx/TokenSkip) ・ リポジトリ内被引用：15  
  思考連鎖（Chain-of-Thought、CoT）は、複雑な数学や論理の問題を段階的に解くことで大規模言語モデルの正答率を改善する。保持率を条件として複数の圧縮版を学習させ、推論時に指定した保持率に応じて短い思考列をモデル自身が直接生成するようにする。

- **2025-05 · [FlashDLM: Accelerating Diffusion Language Model Inference via Efficient KV Caching and Guided Diffusion](2025-2505.21467-flashdlm-accelerating-diffusion-language-model-inference.md)**  
  実装：[✓](https://github.com/ZhanqiuHu/flash-dlm-experimental) ・ リポジトリ内被引用：14  
  FlashDLMは拡散言語モデル（Diffusion Language モデル; DLM）の遅さを、1回のノイズ除去で再計算し過ぎる問題と、何回ノイズ除去を繰り返すかという問題に分ける。FreeCacheは前者を、Guided Diffusionは後者を削り、二つを組み合わせて大きな端末間高速化を得る。

- **2025-03 · [L1: Controlling How Long A Reasoning Model Thinks With Reinforcement Learning](2025-2503.04697-l1-controlling-how-long-a-reasoning-model-thinks-with-reinforcement-lear.md)**  
  実装：[✓](https://github.com/cmu-l3/l1) ・ リポジトリ内被引用：14  
  長い思考は難問での正答率を上げ得るが、単純な問題に数千トークンを費やすと不要な逐次生成が増える。著者が提案する長さ制御方策最適化（Length Controlled Policy Optimization、LCPO）には二種類ある。指定長との平均偏差は数学課題で約3%である。

- **2025-02 · [Training Language Models to Reason Efficiently](2025-2502.04463-training-language-models-to-reason-efficiently.md)**  
  実装：[✓](https://github.com/Zanette-Labs/efficient-reasoning) ・ リポジトリ内被引用：14  
  長い思考過程を生成する推論モデルは、難しい問題で高い正答率を得られる一方、簡単な問題でも冗長な検討を続けることがある。本論文は、正答を優先したまま正解応答の長さに罰則を与えるオンライン強化学習を提案する。7Bの5タスク平均では、長さ罰則 $\alpha=0.2$ の場合、基準モデルに対して生成トークン数が51.58%、正答率が95.94%となった。

- **2024-12 · [C3oT: Generating Shorter Chain-of-Thought without Compromising Effectiveness](2024-2412.11664-c3ot-generating-shorter-chain-of-thought-without-compromising-effectiven.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  C3oT（Conditioned Compressed Chain-of-Thought）は、言語モデルが回答の前に生成する長い思考連鎖（Chain of Thought、CoT）を短くしながら、長い思考で獲得した推論能力を保持するための条件付き学習方式である。

- **2024-12 · [Compressed Chain of Thought: Efficient Reasoning Through Dense Representations](2024-2412.13171-compressed-chain-of-thought-efficient-reasoning-through-dense-representa.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  本研究は、言語モデルの推論精度を高めるために長い自然言語の思考連鎖（Chain of Thought; CoT）を生成すると、回答前の自己回帰復号に多くの時間がかかる問題を扱う。自然言語の思考文を一度すべて生成してから圧縮する方式ではない。

- **2025-10 · [Pie: A Programmable Serving System for Emerging LLM Applications](2025-2510.24051-pie-a-programmable-serving-system-for-emerging-llm-applications.md)**  
  実装：[✓](https://github.com/pie-project/pie) ・ リポジトリ内被引用：12  
  生成ループを細粒度APIへ分解し、Wasm inferletがKV・復号・入出力を直接制御しつつ適応一括処理でGPU効率を維持するプログラマブルLLMサービング基盤。

- **2025-09 · [Qwen3-Omni Technical Report](2025-2509.17765-qwen3-omni-technical-report.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  Qwen3-Omniは、テキスト、画像、音声、動画の入力を統合し、テキスト応答と音声応答を生成する大規模多モーダルモデルである。原著の理論的な初回パケット遅延は、同時要求1件で音声入力234ms、動画を含む入力547msである。

- **2025-06 · [Accelerating Diffusion Large Language Models with SlowFast Sampling: The Three Golden Principles](2025-2506.10848-accelerating-diffusion-large-language-models-with-slowfast-sampling-the-three-golden-principles.md)**  
  実装：[✓](https://github.com/LiangrunFlora/Slow-Fast-Sampling) ・ リポジトリ内被引用：11  
  単独の信頼度閾値だけではなく、連続区間の終端が最近の複数反復で安定したかを検査し、探索段階（Slow）から高速段階（Fast）へ切り替える。原著図2のGPQA・8-shot・生成長1024という特定条件では、LLaDAの通常復号が1.60トークン/秒、SlowFast単独が25.00トークン/秒で15.63倍となる。

- **2025-04 · [OmniKV: Dynamic Context Selection for Efficient Long-Context LLMs](2025-6264cfc484ad-omnikv-dynamic-context-selection-for-efficient-long-context-llms.md)**  
  実装：[✓](https://github.com/antgroup/OmniKV) ・ リポジトリ内被引用：11  
  OmniKVは、長文脈の大規模言語モデルで、鍵・値キャッシュ（KVキャッシュ）をGPUにすべて置くと容量不足になる一方、CPUに退避した全量を各層で読み直すと転送が律速になる問題を扱う。単一A100 80GB、128K文脈で退避なしの復号は毎秒21.0トークン、完全注意比1.68倍である。

- **2025-02 · [Chain of Draft: Thinking Faster by Writing Less](2025-2502.18600-chain-of-draft-thinking-faster-by-writing-less.md)**  
  実装：[✓](https://github.com/sileix/chain-of-draft) ・ リポジトリ内被引用：11  
  Chain of 下書き（CoD）は、推論連鎖（Chain-of-Thought; CoT）の冗長な自然言語を減らし、必要な中間計算だけを短いドラフトとして生成させるprompting方式である。

- **2025-10 · [dInfer: An Efficient Inference Framework for Diffusion Language Models](2025-2510.08666-dinfer-an-efficient-inference-framework-for-diffusion-language-models.md)**  
  実装：[✓](https://github.com/inclusionAI/dInfer) ・ リポジトリ内被引用：10  
  拡散型LLM（dLLM）の反復的な雑音除去（denoising）・並列トークン確定・更新され続けるKVをモジュール化し、デコーダ/KV管理とGPU実行系を同時最適化するdInfer。

- **2025-04 · [Reasoning Models Can Be Effective Without Thinking](2025-2504.09858-reasoning-models-can-be-effective-without-thinking.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  大規模推論モデルは、最終回答の前に長い思考列（chain of thought、CoT）を生成することで数学、プログラミング、定理証明の精度を高めている。形式定理証明では長い思考より3.3～3.7倍少ないトークンで同程度のpass@kを得る。

- **2025-02 · [Cache-Craft: Managing Chunk-Caches for Efficient Retrieval-Augmented Generation](2025-2502.15734-cache-craft-managing-chunk-caches-for-efficient-retrieval-augmented-gene.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  文書自体が同じなのに、GPUはその文書の鍵・値（KV）を再計算することになる。Cache-Craftは再利用するかどうかの判定と、どれだけ再計算して修復するかの決定を分離する。実際のRAGワークロードでは、接頭辞キャッシュ比で冗長計算を51%減らし、連続バッチ下で処理率を1.6倍、エンドツーエンド応答遅延を約半分にしたと報告する。

- **2025-02 · [CoT-Valve: Length-Compressible Chain-of-Thought Tuning](2025-2502.09601-cot-valve-length-compressible-chain-of-thought-tuning.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  CoT-Valveは、推論モデルが簡単な問題にも長い思考連鎖（Chain of Thought、CoT）を生成してしまう無駄を減らし、同じ重みを基盤とするモデルで思考列の長さを柔軟に変える手法である。

- **2025-01 · [Judge Decoding: Faster Speculative Sampling Requires Going Beyond Model Alignment](2025-2501.19309-judge-decoding-faster-speculative-sampling-requires-going-beyond-model-a.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  Llama-3.1-8Bをドラフト、Llama-3.1-405Bを目標にした実験では、平均受理長が標準方式の6.3から19.7トークンへ伸び、最適化されたgpt-fast上で129.3トークン/秒に達した。

- **2024-12 · [Dynamic-LLaVA: Efficient Multimodal Large Language Models via Dynamic Vision-language Context Sparsification](2024-2412.00876-dynamic-llava-efficient-multimodal-large-language-models-via-dynamic-vis.md)**  
  実装：[✓](https://github.com/Osilly/dynamic_llava) ・ リポジトリ内被引用：9  
  動的-LLaVAは、マルチモーダル大規模言語モデル（マルチモーダル Large Language モデル; MLLM）の高速化を、画像トークンだけの削減ではなく「画像文脈と生成済み言語文脈の両方を、推論段階に応じて動的に疎化する」問題として扱う。予測は一度だけ行い、その保持/削除決定を後続層すべてで共有する。

- **2024-11 · [Context Parallelism for Scalable Million-Token Inference](2024-2411.01783-context-parallelism-for-scalable-million-token-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  本研究は、巨大な言語モデルの推論において、長い入力を処理する最初の一回の待ち時間を短縮する文脈並列（context parallelism）の実装を扱う。提案の中心は、リング状の通信で鍵・値を巡回させるpass-KVと、逆に問い合わせを巡回させるpass-Qを、推論段階と既存キャッシュの割合に応じて切り替えることである。

- **2025-02 · [CODI: Compressing Chain-of-Thought into Continuous Space via Self-Distillation](2025-2502.21074-codi-compressing-chain-of-thought-into-continuous-space-via-self-distill.md)**  
  実装：[✓](https://github.com/zhenyi4/codi) ・ リポジトリ内被引用：8  
  CODI（Continuous Chain-of-Thought via Self-Distillation）は、推論過程を自然言語の単語列として毎回生成する費用を減らすため、明示的な思考連鎖（Chain-of-Thought; CoT）を少数の連続潜在状態へ移す学習方式である。

- **2025-05 · [TokenWeave: Efficient Compute-Communication Overlap for Distributed LLM Inference](2025-2505.11329-tokenweave-efficient-compute-communication-overlap-for-distributed-llm-inference.md)**  
  実装：[✓](https://github.com/microsoft/tokenweave) ・ リポジトリ内被引用：7  
  GPU実行波を考慮した2分割とAllReduce–RMSNorm融合により、小さなテンソル並列バッチでも通信と計算を重ね、遅延とスループットを改善する。

- **2025-05 · [AdaptThink: Reasoning Models Can Learn When to Think](2025-2505.13417-adaptthink-reasoning-models-can-learn-when-to-think.md)**  
  実装：[✓](https://github.com/THU-KEG/AdaptThink) ・ リポジトリ内被引用：7  
  AdaptThinkは、問題ごとに「思考あり（Thinking）」と「思考なし（NoThinking）」のどちらで回答するかをモデル自身が選択できるよう、強化学習（Reinforcement Learning; RL）で訓練する方式である。

- **2025-04 · [Energy Considerations of Large Language Model Inference and Efficiency Optimizations](2025-2504.17674-energy-considerations-of-large-language-model-inference-and-efficiency-o.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  LLM推論の電力量を、入力長・出力長・バッチ数・GPU・推論基盤・復号方式・モデル並列の組合せで実測し、実トラフィックの入出力長分布を区間化して総消費量を推定する。適切なソフトウェア最適化で未最適化PyTorch比最大73%削減できる一方、投機的復号や複数GPUは条件によって逆に電力量を増やす。

- **2025-02 · [M-ANT: Efficient Low-bit Group Quantization for LLMs via Mathematically Adaptive Numerical Type](2025-2502.18755-m-ant-efficient-low-bit-group-quantization-for-llms-via-mathematically-a.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  一般的なINT4量子化は整数演算に向くが、各値の分布が一様でないと量子化誤差が大きくなる。専用アクセラレータのシミュレーションでは、先行するLLMアクセラレータに対して平均2.99倍、最大4.46倍の高速化と、平均2.81倍、最大4.10倍のエネルギー削減を報告する。

- **2025-10 · [DeepSeek-OCR: Contexts Optical Compression](2025-2510.18234-deepseek-ocr-contexts-optical-compression.md)**  
  実装：[✓](https://github.com/deepseek-ai/DeepSeek-OCR) ・ リポジトリ内被引用：6  
  本研究は、長いテキストをそのまま多数の言語トークンとして処理する代わりに、文書を二次元の画像として扱い、少数の視覚トークンへ圧縮できるかを検証する。英語文書のFox評価では、画像化した元テキストの約10倍圧縮に相当する視覚トークン数でも文字復元精度がおおむね97%に達する。

- **2025-06 · [SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics](2025-2506.01844-smolvla-a-vision-language-action-model-for-affordable-and-efficient-robo.md)**  
  実装：[✓](https://github.com/huggingface/lerobot) ・ リポジトリ内被引用：6  
  中核は、SmolVLM-2を使う視覚言語部の上位層を省略し、1画像の視覚トークンを64個に抑え、行動専門家（action 専門家）に交差注意と自己注意を交互に配置する設計である。実機のPick-Placeでは同期推論の平均完了時間13.75秒に対し、非同期推論は9.70秒、固定時間内の成功した物体移動数は9個から19個へ増えた。

- **2025-06 · [MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention](2025-2506.13585-minimax-m1-scaling-test-time-compute-efficiently-with-lightning-attentio.md)**  
  実装：[✓](https://github.com/MiniMax-AI/MiniMax-M1) ・ リポジトリ内被引用：6  
  MiniMax-M1は、推論時に長い思考過程を生成する大規模言語モデルで、生成トークンが増えるほど従来のSoftmax注意の計算・記憶費用が膨らむ問題に対処する。モデル全体は4560億パラメータ、トークンごとの活性化は459億パラメータの混合専門家モデル（Mixture of エキスパート、MoE）である。

- **2025-06 · [Beyond Attention or Similarity: Maximizing Conditional Diversity for Token Pruning in MLLMs](2025-2506.10967-beyond-attention-or-similarity-maximizing-conditional-diversity-for-toke.md)**  
  実装：[✓](https://github.com/Theia-4869/CDPruner) ・ リポジトリ内被引用：6  
  本論文は、質問に必要な画像情報を残しながら視覚トークンを減らすCDPrunerを提案する。LLaVA-1.5-7Bで視覚トークン576個から128個へ減らすと、10種類の評価指標の平均相対性能は99.0%である。

- **2025-05 · [Llama-Nemotron: Efficient Reasoning Models](2025-2505.00949-llama-nemotron-efficient-reasoning-models.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  Nano（80億）、Super（490億）、Ultra（2530億）の3規模を提供し、通常の会話と詳細な推論を同じモデルで切り替えられる。実測ではSuperが単一H100上、バッチ256の指定条件で元のLlama 3.3-70Bに対して5倍のスループットを報告し、Ultraは8枚のH100で元のLlama 3.1-405Bに対して1.71倍の遅延改善を得た。

- **2025-04 · [Reasoning Models Know When They're Right: Probing Hidden States for Self-Verification](2025-2504.05419-reasoning-models-know-when-they-re-right-probing-hidden-states-for-self-.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  長い思考連鎖（Chain of Thought; CoT）を生成する推論モデルは、最初に正解へ到達しても別の推論経路を探索し、同じ問題を何度も検証することがある。オンラインで検証器を挿入したサービングシステムの最初のトークン遅延、処理率、VRAM消費、GPU時間を直接測定した結果ではない。

- **2025-02 · [TeleRAG: Efficient Retrieval-Augmented Generation Inference with Lookahead Retrieval](2025-2502.20969-telerag-efficient-retrieval-augmented-generation-inference-with-lookahead-retrieval.md)**  
  実装：[✓](https://github.com/uw-syfi/TeleRAG) ・ リポジトリ内被引用：6  
  RAGの前段生成から次のIVF検索クラスタを予測し、LLM生成とCPU→GPU先読みを重ねつつ外れクラスタをCPU検索で補完して、大規模索引をGPU常駐せず検索待ちを隠す。

- **2024-12 · [NVILA: Efficient Frontier Visual Language Models](2024-2412.04468-nvila-efficient-frontier-visual-language-models.md)**  
  実装：[✓](https://github.com/NVlabs/VILA) ・ リポジトリ内被引用：6  
  NVILAは解像度を先に上げて必要な情報を取り込み、その後に空間・時間方向の冗長性を圧縮する「拡大してから圧縮する（scale-then-compress）」設計を採用する。

- **2024-11 · [ZipNN: Lossless Compression for AI Models](2024-2411.05239-zipnn-lossless-compression-for-ai-models.md)**  
  実装：[✓](https://github.com/zipnn/zipnn) ・ リポジトリ内被引用：6  
  ZipNNは、モデルの重みを変更せずに保存・転送時のバイト数を減らし、展開すると元の重みビット列を完全に復元する可逆圧縮（無損失 compression）である。論文表IIIのLlama 3.1（BF16）では、Zstd単体の圧縮後サイズが原寸の77.7%なのに対してZipNNは66.4%。

- **2025-10 · [INT v.s. FP: A Comprehensive Study of Fine-Grained Low-bit Quantization Formats](2025-2510.25602-int-v-s-fp-a-comprehensive-study-of-fine-grained-low-bit-quantization-fo.md)**  
  実装：[✓](https://github.com/ChenMnZ/INT_vs_FP) ・ リポジトリ内被引用：5  
  しかし、32要素や16要素ごとに独立した尺度を持つ細粒度量子化では、外れ値と典型値を同じ広い範囲へ押し込める必要が小さくなる。ハードウェアの評価は論理回路モデルによる推定であり、MXINT8のエネルギーがMXFP8の0.63倍という数値を、既存GPUの実測消費電力や推論速度と混同してはならない。

- **2025-06 · [MNN-LLM: A Generic Inference Engine for Fast Large Language Model Deployment on Mobile Devices](2025-2506.10443-mnn-llm-mobile-inference-engine.md)**  
  実装：[✓](https://github.com/alibaba/MNN) ・ リポジトリ内被引用：5  
  DRAMとFlashの階層利用、役割別量子化、CPU/GPU別データ配置と負荷分散を統合し、スマートフォン上のLLM推論を高速・省メモリ化する。

- **2025-06 · [MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents](2025-2506.15841-mem1-learning-to-synergize-memory-and-reasoning-for-efficient-long-horiz.md)**  
  実装：[✓](https://github.com/MIT-MI/MEM1) ・ リポジトリ内被引用：5  
  従来の全履歴追記方式では、過去の検索結果が毎ターンのプロンプトへ残るため、文脈長に比例して鍵値キャッシュの容量が増え、注意計算や再入力の費用も高くなる。16目標の多段質問応答では、Qwen2.5-14B-Instructの完全一致数0.567に対しMEM1は1.97、ピークトークン数は3,840に対し1,040、推論時間は29.7秒に対し8.70秒だった。

- **2025-02 · [Accelerating LLM Inference with Lossless Speculative Decoding Algorithms for Heterogeneous Vocabularies](2025-2502.05202-accelerating-llm-inference-with-lossless-speculative-decoding-algorithms-for-heterogeneous-vocabularies.md)**  
  実装：[✓](https://github.com/keyboardAnt/hf-bench) ・ リポジトリ内被引用：5  
  対象モデルと提案モデルの語彙が異なっても損失なし投機的復号を可能にし、既製モデルの自由な組合せで自己回帰復号比最大2.8倍高速化する。

- **2024-11 · [FFN-SkipLLM: A Hidden Gem for Autoregressive Decoding with Adaptive Feed Forward Skipping](2024-2404.03865-ffn-skipllm-a-hidden-gem-for-autoregressive-decoding-with-adaptive-feed-.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  将来トークンが参照するキャッシュに穴が生じるため、過去状態をコピーしたり鍵・値を再計算したりする追加対策が必要となる。提案法は各層の自己注意を維持し、FFNに入る状態とFFN残差更新後の状態のコサイン類似度（cosine similarity）から、中間層の冗長なFFNを検出する。

- **2025-09 · [ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory](2025-2509.25140-reasoningbank-scaling-agent-self-evolving-with-reasoning-memory.md)**  
  実装：[✓](https://github.com/google-research/reasoning-bank) ・ リポジトリ内被引用：4  
  長期間にわたってウェブ操作やソフトウェア修正を行う大規模言語モデル（LLM）エージェントは、過去に成功した手順を別の課題で再発見したり、既に失敗した操作を繰り返したりする。過去の実行軌跡を丸ごと検索する方式では、現在の課題に関係ない画面遷移や局所的な操作が混ざる。

- **2025-05 · [ELIS: Efficient LLM Iterative Scheduling System with Response Length Predictor](2025-2505.09142-elis-efficient-llm-iterative-scheduling-system-with-response-length-predictor.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  応答長を50トークンごとに再予測して短い残作業を優先し、LLM servingの先頭待ちを減らすKubernetes/vLLMスケジューラ。

- **2025-04 · [HIGGS: Pushing the Limits of Large Language Model Quantization via the Linearity Theorem](2025-2411.17525-higgs-pushing-the-limits-of-large-language-model-quantization-via-the-li.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  HIGGSは、LLMの各重み行列を別々に量子化するとき、どの誤差指標を最小化すればモデル全体の予測品質を守れるのかを理論と実験の両面から扱う。GPU実装面では、RTX 4090でLlama-3.1-8Bの4ビットHIGGSをFLUTEカーネルで実行すると、バッチ1で139トークン/秒、FP16は57トークン/秒だった。

- **2025-03 · [MoE-Gen: High-Throughput MoE Inference on a Single GPU with Module-Based Batching](2025-2503.09716-moe-gen-module-based-batching.md)**  
  実装：[✓](https://github.com/EfficientMoE/MoE-Gen) ・ リポジトリ内被引用：4  
  MoEの注意機構とエキスパートを別々にバッチ化し、ホストメモリでトークンを蓄積して大バッチ化することで、単一GPUオフロード推論のGPU利用率とスループットを改善する。

- **2025-03 · [Collaborative Speculative Inference for Efficient LLM Inference Serving](2025-2503.10325-collaborative-speculative-inference-for-efficient-llm-inference-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  異種GPUへドラフト生成と検証を分離し、専門ドラフタ協調と動的パイプライン制御で投機推論の資源利用と受理率を改善する。

- **2025-03 · [A Novel Hat-Shaped Device-Cloud Collaborative Inference Framework for Large Language Models](2025-2503.18989-a-novel-hat-shaped-device-cloud-collaborative-inference-framework-for-la.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  HATは、端末で利用する大規模言語モデルの応答速度と、入力・出力トークンをクラウドへ直接送らない配置を両立するための協調推論方式である。論文全体では比較方式に対して初回応答遅延41～54%、トークン間遅延41～77%の削減を報告する。

- **2024-12 · [Multi-Bin Batching for Increasing LLM Inference Throughput](2024-2412.04504-multi-bin-batching-for-increasing-llm-inference-throughput.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  しかし固定バッチ方式では、バッチに含まれる要求のうち最も長い生成が終わるまで、そのバッチ全体が実行資源を占有する。2026年改訂版の実測では、単一A100 80GB上のllama.cppでDollyワークロードを処理し、推定長8ビンが固定バッチの273.53生成トークン/秒から684.02生成トークン/秒へ改善する。

- **2025-09 · [SemShareKV: Efficient KVCache Sharing for Semantically Similar Prompts via Token-Level LSH Matching](2025-2509.24832-semsharekv-efficient-kvcache-sharing-for-semantically-similar-prompts-via-token-level-lsh-matching.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  意味的に近い別プロンプトをトークンLSHで対応付け、位置補正と層別再計算により完全一致なしでもKVを選択再利用する。

- **2025-06 · [TD-Pipe: Temporally-Disaggregated Pipeline Parallelism Architecture for High-Throughput LLM Inference](2025-2506.10470-td-pipe-temporally-disaggregated-pipeline-parallelism-architecture-for-h.md)**  
  実装：[✓](https://github.com/MLSysU/TD-Pipe) ・ リポジトリ内被引用：3  
  PCIeのみで接続されたGPUのパイプライン並列推論において、プリフィルとデコードを時間分離し、予測型KVメモリ管理と負荷移送で遊休時間を削減する。

- **2025-06 · [SwiftSpec: Ultra-Low Latency LLM Decoding by Scaling Asynchronous Speculative Decoding](2025-2506.11309-swiftspec-asynchronous-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  ドラフトGPU群と対象GPU群を分離して候補木生成と検証を同時実行し、検証済み接頭辞と未検証枝のKVを分けて再利用し、低バッチの同期・起動待ちを減らす投機的デコード。

- **2025-05 · [WINA: Weight Informed Neuron Activation for Accelerating Large Language Model Inference](2025-2505.19427-wina-weight-informed-neuron-activation-for-accelerating-large-language-m.md)**  
  実装：[✓](https://github.com/microsoft/wina) ・ リポジトリ内被引用：3  
  WINAは、既存の大規模言語モデル（LLM）を再学習せず、各層で計算に参加させる活性成分を選択する疎活性化方式である。代表例としてLlama-2-7Bの常識推論8課題平均では、65%の活性疎性でWINAが65.14、TEALが61.07、R-Sparseが59.37となった。

- **2025-01 · [MoE²: Optimizing Collaborative Inference for Edge Large Language Models](2025-2501.09410-moe-optimizing-collaborative-inference-for-edge-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  MoE²（Mixture-of-Edge-Experts）は、単一の大規模言語モデル内部に小さな専門家層を並べる方式ではなく、独立した端末・サーバーに配置された複数の大規模言語モデルそのものを専門家として扱う協調推論基盤である。

- **2025-01 · [Cache Me If You Must: Adaptive Key-Value Quantization for Large Language Models](2025-2501.19392-cache-me-if-you-must-adaptive-key-value-quantization-for-large-language-.md)**  
  実装：[✓](https://github.com/goodevening13/aquakv) ・ リポジトリ内被引用：3  
  長文脈の大規模言語モデル（LLM）では、生成済みトークンの注意機構に使う鍵・値（KV）を各層に保存する。原著の例では、131,072トークンを保持するLlama 3.2 3Bの16ビットKVは約15 GiB、Llama 3.1 70Bでは約42.9 GB（論文の導入部における十進表記）を占める。

- **2024-12 · [METIS: Fast Quality-Aware RAG Systems with Configuration Adaptation](2024-2412.10543-metis-fast-quality-aware-rag-systems-with-configuration-adaptation.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  検索数を増やすと根拠が集まりやすい反面、入力長が増え、最初のトークン生成までの処理やGPUメモリ占有が大きくなる。METISは、質問ごとに必要な検索件数、文章片の統合方法、中間要約長を変えることと、同時にGPUで処理する要求を選ぶことを、一つの制御器で行う。

- **2024-12 · [HashEvict: A Pre-Attention KV Cache Eviction Strategy using Locality-Sensitive Hashing](2024-2412.16187-hashevict-a-pre-attention-kv-cache-eviction-strategy-using-locality-sensitive-hashing.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  問い合わせと鍵の短い局所性鋭敏型ハッシュ（LSH）間のハミング距離から注意度が低い候補を事前推定し、注意計算を実行する前に不要なKVキャッシュを動的に置換する。

- **2025-10 · [Patterns behind Chaos：大規模MoEのデータ移動予測](2025-2510.05497-patterns-behind-chaos-forecasting-data-movement-for-efficient-large-scale-moe-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  その知見を将来のウェハ級GPU設計へ適用すると四モデル平均6.6倍、既存GPU向けプリフィル認識型専門家配置ではMoE計算を最大1.25倍高速化した。

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

- **2025-05 · [MorphServe: Efficient and Workload-Aware LLM Serving via Runtime Quantized Layer Swapping and KV Cache Resizing](2025-2506.02006-efficient-and-workload-aware-llm-serving-via-runtime-layer-swapping-and-kv-cache-resizing.md)**  
  実装：[✓](https://github.com/ds2-lab/MorphServe) ・ リポジトリ内被引用：2  
  負荷ピーク時だけ低影響層を低ビット版へ非同期交換し、空いたGPUメモリをKVキャッシュへ振り替えることで、平均SLO違反を92.45%削減しP95初回トークン遅延を2.2〜3.9倍改善する。

- **2025-06 · [PecSched: Preemptive and Efficient Cluster Scheduling for LLM Inference](2024-2409.15104-csps-a-communication-efficient-sequence-parallelism-based-serving-system-for-transformer-based-models-with-long-prompts.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長入力事前計算を短入力事前計算で選択的に横取りし、事前計算・復号の分離同居と高速系列並列を組み合わせて、短入力の待ち時間と長入力の飢餓を両立して抑える。

- **2025-06 · [EQuARX: Efficient Quantized AllReduce in XLA for Distributed Machine Learning Acceleration](2025-2506.17615-equarx-quantized-allreduce-xla.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  AllReduce内でブロック量子化と逆量子化を通信へ重ね、TPU/XLAの集団通信量を削減する方式。int8でBF16 AllReduce比最大1.8倍、Gemma 3 27Bプリフィル最大1.28倍を示す。

- **2025-05 · [GMSA: Enhancing Context Compression via Group Merging and Layer Semantic Alignment](2025-2505.12215-gmsa-enhancing-context-compression-via-group-merging-and-layer-semantic-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GMSAは、原文を文字列として間引くのではなく、少数の連続表現トークン（soft トークン）へ変換する文脈圧縮方式である。NaturalQuestionsの4倍圧縮では完全一致（Exact Match、EM）が58.12%で、元文脈をそのまま与える条件の15.07%を上回った。

- **2025-03 · [AdaReTaKe: Adaptive Redundancy Reduction to Perceive Longer for Video-language Understanding](2025-2503.12559-adaretake-adaptive-redundancy-reduction-to-perceive-longer-for-video-lan.md)**  
  実装：[✓](https://github.com/SCZwangxiao/video-FlexReduc) ・ リポジトリ内被引用：1  
  動画を長くするほど事前充填で扱う系列が増え、言語モデルの鍵・値キャッシュ（KVキャッシュ）がGPUメモリを圧迫する。すべてのフレームを同じ割合で圧縮すると、静止区間へ不要な容量を割り当てる一方、質問に必要な短い場面の情報を失う。これは処理可能な動画情報量と理解精度の結果であり、トークン生成速度が同倍率で向上するという主張ではない。

- **2024-12 · [IFMoE: An Inference Framework Design for Fine-grained MoE](2026-3190de0b4969-ifmoe-an-inference-framework-design-for-fine-grained-moe.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  共有部分をテンソル並列化して細粒度MoEの重複メモリを減らし、少数専門家で草稿生成した後に完全専門家設定でKVキャッシュを修整して復号を高速化する。

- **2025-08 · [Cost-Aware Contrastive Routing for LLMs](2025-2508.12491-cost-aware-contrastive-routing-for-llms.md)**  
  実装：[✓](https://github.com/rezashkv/cscr) ・ リポジトリ内被引用：0  
  CSCR（コスト-Spectrum Contrastive Router）は、質問の特徴と候補モデルの能力を同じベクトル空間へ配置し、正答できるモデルを費用帯ごとに区別する対照学習を行うことで、この選択を軽い近傍検索へ置き換える。

- **2025-07 · [La RoSA: Enhancing LLM Efficiency via Layerwise Rotated Sparse Activation](2025-2507.01299-la-rosa-enhancing-llm-efficiency-via-layerwise-rotated-sparse-activation.md)**  
  実装：[✓](https://github.com/alibaba/EfficientAI) ・ リポジトリ内被引用：0  
  重みの量子化や枝刈りとは別に、入力活性の多くをゼロにできれば、ゼロに対応する重み列を読み込まずに済む。論文の代表例では、LLaMA2-7Bのモデル全体の活性疎性40%で困惑度の悪化が5.47から5.64への0.17にとどまり、7種のゼロ例示タスクの平均得点は66.69から66.15への0.54ポイント低下である。

- **2025-07 · [CateKV: On Sequential Consistency for Long-Context LLM Inference Acceleration](2026-2608.30295-catekv-on-sequential-consistency-for-long-context-llm-inference-acceleration.md)**  
  実装：[✓](https://github.com/haoyun-jiang/CateKV) ・ リポジトリ内被引用：0  
  プリフィルからデコードまで注意先が安定するヘッドだけKVを強く削減し、動的ヘッドは大半を保持するハイブリッドKVキャッシュで、精度を保ちながら長文推論のメモリ・デコード・バッチ性能を改善する。

- **2025-07 · [Accelerating Dense LLMs via L0-regularized Mixture-of-Experts](2026-2609.21672-accelerating-dense-llms-via-l0-regularized-mixture-of-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既存の密な大規模言語モデル（LLM）を高速化するには、量子化・枝刈り・知識蒸留が使われるが、強い圧縮では能力低下が生じやすい。MMLU、GSM8K、HumanEval、BBHの4課題平均はほぼ維持され、推論速度は2.0〜2.5倍となる。

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

- **2025-02 · [BumbleBee: Secure Two-party Inference Framework for Large Transformers](2025-93b16acfd7b9-bumblebee-secure-two-party-inference-framework-for-large-transformers.md)**  
  実装：[✓](https://github.com/AntCPLab/OpenBumbleBee) ・ リポジトリ内被引用：0  
  入力とモデル重みをそれぞれ秘匿したままBERT、GPT-2、LLaMA-7B、ViTを実行し、従来方式に比べて実測の転送量と実行時間を改善する。

- **2025-02 · [AutoHete: An Automatic and Efficient Heterogeneous Training System for LLMs](2025-2503.01890-autohete-an-automatic-and-efficient-heterogeneous-training-system-for-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  活性値再計算・パラメータ退避・オプティマイザ退避を整数線形計画で共同選択し、反復をまたぐ優先度付き処理重畳でCPU/GPU待ちを減らす異種混在LLM学習方式。

- **2025-01 · [Instruction-Following Pruning for Large Language Models](2025-2501.02086-instruction-following-pruning-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  指示追従枝刈り（Instruction-Following Pruning、IFPruning）は、利用者の指示文から小型の疎性予測器が必要なフィードフォワード層（FFN）の中間次元を選び、その指示に対する応答の復号中は同じ部分ネットワークを固定して実行する手法である。

- **2024-11 · [ShowUI: One Vision-Language-Action Model for GUI Visual Agent](2024-2411.17465-showui-one-vision-language-action-model-for-gui-visual-agent.md)**  
  実装：[✓](https://github.com/showlab/ShowUI) ・ リポジトリ内被引用：0  
  一方、画像を粗く統合してしまうと、クリック対象の小さな部品の座標を失いやすい。Qwen2-VL-2Bを基盤に、25.6万件の指示データで学習したモデルは、ScreenSpotのゼロショット画面要素特定で75.1%を報告した。

### 3年前（2023-11〜2024-10）

- **2023-12 · [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](2023-2312.00752-mamba-selective-state-space-linear-time-inference.md)**  
  実装：[✓](https://github.com/state-spaces/mamba) ・ リポジトリ内被引用：137  
  入力依存の選択的状態空間層とGPU向け融合走査を統合し、注意機構なしでTransformer級品質と4〜5倍の生成スループットを両立する。

- **2024-03 · [QuaRot: Outlier-Free 4-Bit Inference in Rotated LLMs](2024-2404.00456-quarot-outlier-free-4-bit-inference-in-rotated-llms.md)**  
  実装：[✓](https://github.com/spcl/QuaRot) ・ リポジトリ内被引用：92  
  QuaRotは、大規模言語モデル（LLM）の4ビット推論を難しくする活性値の外れ値を、高精度の例外チャネルへ逃がすのではなく、モデルの関数を変えない直交回転（orthogonal rotation）で多数の次元へ分散する量子化手法である。

- **2024-07 · [FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](2024-2407.08608-flashattention-3-fast-and-accurate-attention-with-asynchrony-and-low-pre.md)**  
  実装：[✓](https://github.com/Dao-AILab/flash-attention) ・ リポジトリ内被引用：83  
  従来のFlashAttention系列は、注意重みの巨大な中間行列を高帯域メモリ（HBM）に書き戻さず、共有メモリとレジスタ内でタイルごとに処理することでメモリ転送を削減した。

- **2024-02 · [QuIP#: Even Better LLM Quantization with Hadamard Incoherence and Lattice Codebooks](2024-2402.04396-quip-even-better-llm-quantization-with-hadamard-incoherence-and-lattice-.md)**  
  実装：[✓](https://github.com/Cornell-RelaxML/quip-sharp) ・ リポジトリ内被引用：73  
  QuIP#は、学習済みの大規模言語モデルを再学習せずに2〜4ビット/重みへ圧縮する事後学習量子化（Post-学習 量子化、PTQ）である。試作推論実装はRTX 4090上で70Bの2ビット重みを32.74トークン/秒で生成し、実効メモリ帯域利用率56.84%を記録した（表5）。

- **2024-03 · [An Image is Worth 1/2 Tokens After Layer 2: Plug-and-Play Inference Acceleration for Large Vision-Language Models](2024-2403.06764-an-image-is-worth-1-2-tokens-after-layer-2-plug-and-play-inference-accel.md)**  
  実装：[✓](https://github.com/pkunlp-icler/FastV) ・ リポジトリ内被引用：62  
  LLaVA-1.5では一枚の336×336画像が576トークンになり、高解像度化や動画の複数フレーム処理では数千トークンへ増える。初期層では画像情報が広く注意される一方、深い層では少数のシステム指示や文章トークンへ注意が集中し、画像トークン一個当たりの注意効率が非常に低くなる。代表設定は二層後に視覚トークンの50%を削除する方式である。

- **2024-09 · [OLMoE: Open Mixture-of-Experts Language Models](2024-2409.02060-olmoe-open-mixture-of-experts-language-models.md)**  
  実装：[✓](https://github.com/allenai/OLMoE) ・ リポジトリ内被引用：55  
  混合専門家（Mixture-of-Experts; MoE）は総パラメータを増やしながら、各トークンで一部専門家だけを実行することで、密 モデルより計算量を抑えられる。

- **2024-04 · [Better & Faster Large Language Models via Multi-token Prediction](2024-2404.19737-better-faster-large-language-models-via-multi-token-prediction.md)**  
  実装：✓ ・ リポジトリ内被引用：51  
  一般的な自己回帰言語モデルは、各位置までの文脈から直後の一つのトークンを予測する。これに対して複数トークン予測（Multi-トークン Prediction; MTP）は、同じ位置の共有表現から、1個先だけでなく2個先、3個先、4個先など複数の未来トークンを別々の出力ヘッドで予測するよう学習する。この研究には二つの独立した成果がある。

- **2023-12 · [Gated Linear Attention Transformers with Hardware-Efficient Training](2024-2312.06635-gated-linear-attention-transformers-with-hardware-efficient-training.md)**  
  実装：[✓](https://github.com/sustcsonglin/flash-linear-attention) ・ リポジトリ内被引用：48  
  また再帰式を素朴にGPUへ実装すると、逐次依存や高帯域メモリへの状態書き込みが律速となる。著者らは二つの仕組みを提案する。

- **2024-02 · [Hydra: Sequentially-Dependent Draft Heads for Medusa Decoding](2024-2402.05109-hydra-sequentially-dependent-draft-heads-for-medusa-decoding.md)**  
  実装：[✓](https://github.com/zankner/Hydra) ・ リポジトリ内被引用：45  
  投機的復号（投機的復号）は、安価な下書きモデルが複数の将来トークンを予測し、元の大きな言語モデルが候補をまとめて検証することで、1回の高価な順伝播で複数トークンを確定させる。単一要求のVicuna 7B/13B/33Bで通常の自己回帰生成に対しそれぞれ2.70/2.50/2.53倍、Medusaに対し1.27/1.27/1.31倍の処理率を報告する。

- **2024-09 · [RetrievalAttention: Accelerating Long-Context LLM Inference via Vector Retrieval](2024-2409.10516-retrievalattention-accelerating-long-context-llm-inference-via-vector-re.md)**  
  実装：✓ ・ リポジトリ内被引用：44  
  RetrievalAttentionは、長文脈の大規模言語モデルが自己回帰復号で過去のすべての鍵値を走査する負担を、現在の質問に重要なトークンだけを動的に検索することで減らす手法である。しかし注意の質問と鍵は異なる重み行列で射影され、ベクトル分布がずれるため、一般的な索引をそのまま使うと高い再現率を得るために鍵の30～50%を走査しなければならない。

- **2024-03 · [LLaVA-PruMerge: Adaptive Token Reduction for Efficient Large Multimodal Models](2024-2403.15388-llava-prumerge-adaptive-token-reduction-for-efficient-large-multimodal-m.md)**  
  実装：[✓](https://github.com/42Shawn/LLaVA-PruMerge) ・ リポジトリ内被引用：43  
  LLaVA-PruMergeは、画像を大規模言語モデルへ渡す際の視覚トークン数を削減する方式である。LLaVA-1.5は336×336画素の画像から24×24個、すなわち576個の視覚トークンを生成する。

- **2024-01 · [Extreme Compression of Large Language Models via Additive Quantization](2024-2401.06118-extreme-compression-of-large-language-models-via-additive-quantization.md)**  
  実装：[✓](https://github.com/Vahe1994/AQLM) ・ リポジトリ内被引用：42  
  加算量子化による言語モデル圧縮（AQLM）は、重みの極低ビット量子化における「小さいモデルを高精度で保持した方が、巨大モデルを2ビットにするより良い」という従来の精度対容量の関係を改善する研究である。Llama 2 7B・13B・70B、Mixtral 8×7B、Mistral 7Bを評価する。

- **2024-04 · [RAGCache: Efficient Knowledge Caching for Retrieval-Augmented Generation](2024-2404.12457-ragcache-efficient-knowledge-caching-for-retrieval-augmented-generation.md)**  
  実装：✓ ・ リポジトリ内被引用：41  
  RAGCacheは、検索拡張生成（Retrieval-Augmented Generation; RAG）で同じ知識文書が何度も検索されることに着目し、その文書を言語モデルが処理したときの鍵・値キャッシュ（KVキャッシュ）を複数要求で再利用する推論提供システムである。

- **2024-02 · [InfLLM: Training-Free Long-Context Extrapolation for LLMs with an Efficient Context Memory](2024-2402.04617-infllm-training-free-long-context-extrapolation-for-llms-with-an-efficie.md)**  
  実装：[✓](https://github.com/thunlp/InfLLM) ・ リポジトリ内被引用：41  
  InfLLMは、短い文脈長で事前学習された大規模言語モデル（LLM）を、重みの追加学習なしに非常に長い入力へ適用する方式である。

- **2024-10 · [SparseVLM: Visual Token Sparsification for Efficient Vision-Language Model Inference](2024-2410.04417-sparsevlm-visual-token-sparsification-for-efficient-vision-language-mode.md)**  
  実装：[✓](https://github.com/Gumpest/SparseVLMs) ・ リポジトリ内被引用：40  
  SparseVLMは、視覚言語モデル（VLM）の入力画像から生じる大量の視覚トークンを、現在の質問に必要な情報をできるだけ残しながら削減する追加学習不要の方式である。

- **2024-04 · [Mixture-of-Depths: Dynamically allocating compute in transformer-based language models](2024-2404.02258-mixture-of-depths-dynamically-allocating-compute-in-transformer-based-la.md)**  
  実装：✓ ・ リポジトリ内被引用：40  
  そのため、簡単な予測位置も難しい予測位置も同じ計算を受ける。方式の要点は、処理するトークンの「個数」kを事前に固定し、「どのトークンか」だけを学習済みルータが動的に選ぶ点にある。論文の代表構成では系列長2048に対し、一つおきの層で上位256トークン、すなわち12.5%だけを自己注意とMLPへ通す。

- **2023-11 · [FlashDecoding++: Faster Large Language Model Inference on GPUs](2023-2311.01282-flashdecoding-faster-large-language-model-inference-on-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：38  
  FlashDecoding++は、自己回帰型の大規模言語モデルで一語ずつ出力する復号段階を、GPUの演算資源とメモリ階層に合わせて高速化する推論エンジンである。論文が分離した三つの障害は、長い注意系列を分割したときの部分ソフトマックス結合同期、少数トークンを入力する細長い行列積のゼロ埋め、行列形状とGPUの種類を無視する固定実行方式である。

- **2024-07 · [PQCache: Product Quantization-based KVCache for Long Context LLM Inference](2024-2407.12820-pqcache-product-quantization-based-kvcache-for-long-context-llm-inferenc.md)**  
  実装：[✓](https://github.com/HugoZHL/PQCache) ・ リポジトリ内被引用：36  
  文脈が長くなるほどKVキャッシュは大きくなり、GPUメモリへ収まらない場合にはCPUメモリへの退避と転送が必要になる。Llama-3.1-8Bの128K文脈を用いたInfiniteBenchでは、過去トークンの1/10だけを選択する条件で平均スコア46.80を報告し、比較方式に対する改善は+4.60%である。

- **2024-10 · [PyramidDrop: Accelerating Your Large Vision-Language Models via Pyramid Visual Redundancy Reduction](2024-2410.17247-pyramiddrop-accelerating-your-large-vision-language-models-via-pyramid-v.md)**  
  実装：[✓](https://github.com/Cooperx521/PyramidDrop) ・ リポジトリ内被引用：32  
  大規模視覚言語モデル（Large Vision-Language モデル; LVLM）は、画像を数百から数千の画像トークンへ変換して、文章の質問と一緒に言語モデルへ入力する。画像解像度が上がると画像トークンが増え、注意計算と全結合層の演算量が大きくなる。複数の視覚言語ベンチマークで品質は概ね維持されるが、個別の高解像度課題では小さな低下もある。

- **2024-03 · [ShortGPT: Layers in Large Language Models are More Redundant Than You Expect](2024-2403.03853-shortgpt-layers-in-large-language-models-are-more-redundant-than-you-exp.md)**  
  実装：[✓](https://github.com/icip-cas/ShortGPT) ・ リポジトリ内被引用：32  
  本論文は、大規模言語モデルの全ての変換層が同程度に必要とは限らないという観察から、計算の一部を省略する二種類の方式を提案する。ACL 2025掲載版の代表例では、Llama2-13Bの40層から10層を対象とする条件で、多肢選択指標の平均値は58.49から53.57となり、元の約91.59%を維持した。

- **2024-04 · [Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing](2024-2404.14618-hybrid-llm-cost-efficient-and-quality-aware-query-routing.md)**  
  実装：[✓](https://github.com/m365-core/hybrid_llm_routing) ・ リポジトリ内被引用：31  
  同じ大規模言語モデル（LLM）を全要求へ使うと、単純な質問にも高価な推論計算を割り当てる。小型Llama-2 7B／大型Llama-2 13Bの組合せでは、検証集合で品質低下を1%以下にするしきい値を選んだ確率的ルータが、テスト集合で96.80%の要求を小型へ送ったが、品質低下は1.42%となった。

- **2024-09 · [HybridFlow: A Flexible and Efficient RLHF Framework](2024-2409.19256-hybridflow-a-flexible-and-efficient-rlhf-framework.md)**  
  実装：[✓](https://github.com/volcengine/verl) ・ リポジトリ内被引用：30  
  HybridFlowは、人間フィードバックによる強化学習（Reinforcement Learning from Human Feedback: RLHF）を複数の大規模言語モデルからなる分散データフローとして扱い、その制御の柔軟性と学習処理率を両立するシステムである。

- **2024-02 · [Decoding Speculative Decoding](2024-2402.01528-decoding-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：30  
  350件超の投機的デコード実験からドラフト遅延と層深度を主要因と特定し、浅く広いドラフトモデルへ再設計して最大111%のスループット向上を示す。

- **2023-12 · [ASVD: Activation-aware Singular Value Decomposition for Compressing Large Language Models](2023-2312.05821-asvd-activation-aware-singular-value-decomposition-for-compressing-large.md)**  
  実装：[✓](https://github.com/hahnyuan/ASVD4LLM) ・ リポジトリ内被引用：30  
  活性値認識型特異値分解（活性値-aware Singular Value Decomposition、ASVD）は、大規模言語モデル（LLM）の線形重みを追加学習なしで低ランク行列へ置き換える圧縮方式である。LLaMA-7BとLLaMA-2-7B/13Bで重み容量を10～30%削減する実験を行い、活性値を考慮しないSVDより大幅に良い困惑度を報告する。

- **2023-11 · [LLaMA-VID: An Image is Worth 2 Tokens in Large Language Models](2023-2311.17043-llama-vid-an-image-is-worth-2-tokens-in-large-language-models.md)**  
  実装：[✓](https://github.com/dvlab-research/LLaMA-VID) ・ リポジトリ内被引用：30  
  LLaMA-VIDは、各フレームの情報を質問に応じて抽出する文脈トークンと画像内容を要約する内容トークンに分離する。ECCV 2024正式論文では、動画質問応答のMSVD-QAでVicuna-7B構成が正解率69.7%、MSRVTT-QAで57.7%、ActivityNet-QAで47.4%を記録した。

- **2024-02 · [WKVQuant: Quantizing Weight and Key/Value Cache for Large Language Models Gains More](2024-2402.12065-wkvquant-quantizing-weight-and-key-value-cache-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：29  
  WKVQuantは、大規模言語モデルの推論時に使うメモリを、モデル重み、鍵・値キャッシュ、一時活性化の三種類に分け、容量を長く占有する重みと鍵・値キャッシュだけを低ビット化する事後量子化（post-学習 量子化; PTQ）方式である。重みのみの量子化は比較的精度を維持しやすいが、長文脈・大バッチで増える鍵・値キャッシュを圧縮しない。

- **2024-02 · [Massive Activations in Large Language Models](2024-2402.17762-massive-activations-in-large-language-models.md)**  
  実装：[✓](https://github.com/locuslab/massive-activations) ・ リポジトリ内被引用：28  
  著者らは入力を変えたときの値の変動と、推論中に値を直接置換する介入実験から、巨大活性値が単なる数値的不安定さではなく、自己注意（self-注意機構）へ一定の加算成分を供給する暗黙のバイアス（implicit bias）として働くと結論付ける。

- **2024-02 · [The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits](2024-2402.17764-the-era-of-1-bit-llms-all-large-language-models-are-in-1-58-bits.md)**  
  実装：✓ ・ リポジトリ内被引用：27  
  狙いは、学習済みFP16/BF16モデルを後から近似する事後学習量子化ではなく、モデル自体を極低bit表現へ適応させ、品質を維持したまま重み転送・行列積・メモリ容量の支配項を小さくすることにある。

- **2024-04 · [SEER-MoE: Sparse Expert Efficiency through Regularization for Mixture-of-Experts](2024-2404.05089-seer-moe-sparse-expert-efficiency-through-regularization-for-mixture-of-.md)**  
  実装：✓ ・ リポジトリ内被引用：24  
  SEER-MoEは、事前学習済みの混合専門家モデル（Mixture of エキスパート、MoE）のメモリ消費とトークン当たりの演算量を、別々の制約として削減する方式である。Mixtral 8×7Bは通常各トークンを二つの専門家へ送り、専門家部分の演算は推論全体の約55%を占める。

- **2024-02 · [Griffin: Mixing Gated Linear Recurrences with Local Attention for Efficient Language Models](2024-2402.19427-griffin-mixing-gated-linear-recurrences-with-local-attention-for-efficie.md)**  
  実装：✓ ・ リポジトリ内被引用：24  
  Griffinは、自己回帰言語モデルの推論において、文脈が伸びるたびに増える鍵・値キャッシュ（KVキャッシュ）の読み出し費用を抑えるため、固定長の再帰状態と有限窓の注意機構を組み合わせたモデル構造である。

- **2024-06 · [Samba: Simple Hybrid State Space Models for Efficient Unlimited Context Language Modeling](2024-2406.07522-samba-simple-hybrid-state-space-models-for-efficient-unlimited-context-language-modeling.md)**  
  実装：[✓](https://github.com/microsoft/Samba) ・ リポジトリ内被引用：21  
  Sambaは、選択的状態空間モデル（Selective State Space モデル; SSM）で遠い過去を固定サイズ状態へ畳み込み、スライディング窓注意（Sliding Window 注意機構; SWA）で直近トークンを正確に参照する。

- **2024-04 · [Leave No Context Behind: Efficient Infinite Context Transformers with Infini-attention](2024-2404.07143-leave-no-context-behind-efficient-infinite-context-transformers-with-infini-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：21  
  Infini-注意機構は、入力文脈が数十万から100万トークンに達しても、過去の全トークンに対応する鍵・値（KV）を保存し続けずに情報を参照するための注意機構である。

- **2024-09 · [No Request Left Behind: Tackling Heterogeneity in Long-Context LLM Inference with Medha](2024-2409.17264-no-request-left-behind-tackling-heterogeneity-in-long-context-llm-infere.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  これはオペレーティングシステムでいう隊列詰まり（convoy effect）に相当し、GPUが高い総計算量を処理していても利用者の初回応答待ち時間が極端に悪化する。非割込みの長文推論配信基盤と比べて、ある混合負荷ではスループット5.7倍、初回トークン遅延の中央値30分の1、上位側の遅延174分の1という大きな差を報告する。

- **2024-06 · [A Survey on Mixture of Experts in Large Language Models](2024-2407.06204-a-survey-on-mixture-of-experts-in-large-language-models.md)**  
  実装：[✓](https://github.com/withinmiaov/A-Survey-on-Mixture-of-Experts-in-LLMs) ・ リポジトリ内被引用：19  
  全パラメータ数を大きくしても活性化する部分を限定できるが、実機では選択された専門家へのトークン転送、専門家ごとの負荷の偏り、GPU間の全対全通信、巨大な専門家重みの配置・退避が新たな律速になる。

- **2024-01 · [Long Context Compression with Activation Beacon](2024-2401.03462-long-context-compression-with-activation-beacon.md)**  
  実装：[✓](https://github.com/FlagOpen/FlagEmbedding) ・ リポジトリ内被引用：19  
  活性値 Beaconは、文章そのものを短く書き換えるのではなく、Transformerの各層に生じる鍵・値活性を、追加したビーコントークンの活性へ直接圧縮する。圧縮率を8倍にした128K文脈の実験では、非圧縮で同じデータにより微調整した比較モデルに対し、推論時間を約半分、KVキャッシュを約8分の1にした。

- **2024-10 · [LongVU: Spatiotemporal Adaptive Compression for Long Video-Language Understanding](2024-2410.17434-longvu-spatiotemporal-adaptive-compression-for-long-video-language-under.md)**  
  実装：[✓](https://github.com/Vision-CAIR/LongVU) ・ リポジトリ内被引用：17  
  LongVUは、長時間動画を多模態大規模言語モデルへ入力するとき、視覚トークン数が文脈長を超える問題に対して、時間方向の冗長なフレーム削除、質問に応じた空間解像度の配分、フレーム間で重複する空間トークンの削除を段階的に組み合わせる方式である。

- **2024-07 · [Learning to (Learn at Test Time): RNNs with Expressive Hidden States](2024-2407.04620-learning-to-learn-at-test-time-rnns-with-expressive-hidden-states.md)**  
  実装：[✓](https://github.com/test-time-training/ttt-lm-pytorch) ・ リポジトリ内被引用：17  
  本論文は、再帰型ニューラルネットワーク（Recurrent Neural Network、RNN）の隠れ状態を単なる固定長ベクトルではなく、小さな機械学習モデルの重みとして表現するテスト時訓練（Test-Time 学習、TTT）層を提案する。

- **2024-01 · [Multi-Candidate Speculative Decoding](2024-2401.06706-multi-candidate-speculative-decoding.md)**  
  実装：[✓](https://github.com/NJUNLP/MCSD) ・ リポジトリ内被引用：17  
  標準方式では各深さに一つの候補しかない。したがって、研究の核は「候補幅による受理率向上」「分布保存の検証」「共有接頭辞による検証費用削減」の三点である。

- **2024-01 · [MoE-LLaVA: Mixture of Experts for Large Vision-Language Models](2024-2401.15947-moe-llava-mixture-of-experts-for-large-vision-language-models.md)**  
  実装：[✓](https://github.com/PKU-YuanGroup/MoE-LLaVA) ・ リポジトリ内被引用：17  
  混合専門家（mixture of エキスパート、MoE）は、複数の専門家を持ちながらトークンごとに少数だけ活性化することで、総パラメータ数と一度の計算に使うパラメータ数を切り離せる。

- **2024-03 · [DéjàVu：KVキャッシュ・ストリーミングによる高速・耐障害LLM配信](2024-2403.01876-dejavu-kv-cache-streaming-for-fast-fault-tolerant-generative-llm-serving.md)**  
  実装：[✓](https://github.com/msr-fiddle/dejavu) ・ リポジトリ内被引用：16  
  また各マイクロバッチのKVキャッシュをGPUに保持し続けるとメモリを過剰確保し、障害時には失われたKV状態を再計算するため復旧が遅い。DéjàVuはこれらをKVキャッシュの高速な非同期転送という一つの機構で扱う。

- **2024-02 · [CLLMs: Consistency Large Language Models](2024-2403.00835-cllms-consistency-large-language-models.md)**  
  実装：[✓](https://github.com/hao-ai-lab/Consistency_LLM) ・ リポジトリ内被引用：16  
  整合性大規模言語モデル（Consistency Large Language Models; CLLMs）は、Jacobi型の並列復号で使う仮の複数トークン列から、自己回帰復号の最終固定点へ速く近づくよう既存LLMを追加学習する。固定点に対する大域整合性損失と通常の自己回帰損失を併用し、追加の小型草案モデルなしで生成を高速化する。

- **2024-06 · [Your Absorbing Discrete Diffusion Secretly Models the Conditional Distributions of Clean Data](2026-2406.03736-your-absorbing-discrete-diffusion-secretly-models-the-conditional-distri.md)**  
  実装：[✓](https://github.com/ML-GSAI/RADD) ・ リポジトリ内被引用：15  
  RADDは吸収型離散拡散の逆過程で必要な条件付き確率を時刻から切り離し、マスク配置が変わらないステップの推論を省略する。理論的な損失の等価性と、実際の生成時間・困惑度の双方を検証した研究。

- **2024-04 · [Eagle and Finch: RWKV with Matrix-Valued States and Dynamic Recurrence](2024-2404.05892-eagle-and-finch-rwkv-with-matrix-valued-states-and-dynamic-recurrence.md)**  
  実装：[✓](https://github.com/RWKV/RWKV-LM) ・ リポジトリ内被引用：15  
  過去の鍵・値をトークン単位で保持する代わりに、複数ヘッドの固定サイズ行列状態を更新する。Eagleは行列状態とゲートを、Finchは内容依存の補間・時間減衰を導入し、長文脈での情報保持を改善する。

- **2024-04 · [Characterizing Power Management Opportunities for LLMs in the Cloud](2024-ad611bbc0cdc-characterizing-power-management-opportunities-for-llms-in-the-cloud.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  この観測を使い、優先度別の二段階電力制御を行うPOLCAを提案する。著者らは本番トレースから生成した合成負荷を用いた離散事象シミュレーションで、既存の電力予算のままサーバーを30%多く配置しても、設定した遅延SLOを満たし、通常条件で電力ブレーキを起こさない結果を示した。

- **2023-12 · [Zoology: Measuring and Improving Recall in Efficient Language Models](2023-2312.04927-zoology-measuring-and-improving-recall-in-efficient-language-models.md)**  
  実装：[✓](https://github.com/HazyResearch/zoology) ・ リポジトリ内被引用：15  
  Zoologyは注意、H3、Hyena、RWKVなどの系列混合器を共通条件で比較し、注意なしの方式がどのようなトークンで失敗するかを細かく測定した研究である。Pileの検証データで、以前の文脈に現れた二語連接の続きを再び予測する位置を「連想想起ヒット」として抽出すると、該当位置は全トークンの6.4%にすぎない。

- **2024-10 · [ConServe: Fine-Grained GPU Harvesting for LLM Online and Offline Co-Serving](2024-2410.01228-conserve-fine-grained-gpu-harvesting-for-llm-online-and-offline-co-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  SLO予測付きトークン調整・層単位プリエンプション・増分KV退避で、オンライン遅延を守りながら遊休GPUをオフライン推論へ回す共同サービング方式。

- **2024-04 · [JetMoE: Reaching Llama2 Performance with 0.1M Dollars](2024-2404.07413-jetmoe-reaching-llama2-performance-with-0-1m-dollars.md)**  
  実装：[✓](https://github.com/myshell-ai/JetMoE) ・ リポジトリ内被引用：13  
  JetMoE-8Bは、混合専門家モデル（Mixture of エキスパート、MoE）の条件付き計算を順伝播ネットワーク（FFN）だけでなく自己注意機構へも拡張した、総パラメータ約80億の言語モデルである。論文はLlama2-7Bとの比較で推論演算量を約70%削減できると述べるが、これは実測の生成遅延が70%減るという意味ではない。

- **2023-12 · [Lookahead: An Inference Acceleration Framework for Large Language Model with Lossless Generation Accuracy](2023-2312.12728-lookahead-an-inference-acceleration-framework-for-large-language-model-w.md)**  
  実装：[✓](https://github.com/alipay/PainlessInferenceAcceleration) ・ リポジトリ内被引用：12  
  Lookaheadは、この空きを利用して過去の生成履歴から複数の継続候補を構成し、一回の対象モデル計算で複数トークンを確定する推論高速化方式である。

- **2024-04 · [HGRN2: Gated Linear RNNs with State Expansion](2024-2404.07904-hgrn2-gated-linear-rnns-with-state-expansion.md)**  
  実装：[✓](https://github.com/OpenNLPLab/HGRN2) ・ リポジトリ内被引用：11  
  これに対し、線形再帰モデルは固定サイズの状態へ履歴を圧縮して次のトークンを生成できるため、推論時の状態保存量を系列長に依存させない。

- **2024-02 · [OneBit: Towards Extremely Low-bit Large Language Models](2024-2402.11295-onebit-towards-extremely-low-bit-large-language-models.md)**  
  実装：[✓](https://github.com/xuyuzhuang11/OneBit) ・ リポジトリ内被引用：11  
  OneBitは、学習済み大規模言語モデル（LLM）の重みを極端に低いビット数で保存する際に生じる精度劣化を、線形層の表現形式そのものを変更することで緩和する研究である。査読版の表3では、LLaMA-7Bの重み保存量が13.5 GBから1.3 GBへ、LLaMA-13Bでは26.0 GBから2.2 GBへ減る。

- **2024-10 · [MatryoshkaKV: Adaptive KV Compression via Trainable Orthogonal Projection](2024-2410.14731-matryoshkakv-adaptive-kv-compression-via-trainable-orthogonal-projection.md)**  
  実装：[✓](https://github.com/The-kamisato/MatryoshkaKV-cache) ・ リポジトリ内被引用：10  
  MatryoshkaKVは、事前学習済み大規模言語モデル（LLM）の鍵値キャッシュ（KVキャッシュ）について、トークン数や注意ヘッド数を減らす代わりに各ヘッドが保存する特徴次元を縮小する方式である。単純な主成分分析（PCA）による次元削減は中程度の圧縮では有効だが、元のキャッシュ容量の半分以下にすると生成品質が急落する。

- **2024-05 · [Boosting Multimodal Large Language Models with Visual Tokens Withdrawal for Rapid Inference](2024-2405.05803-boosting-multimodal-large-language-models-with-visual-tokens-withdrawal-.md)**  
  実装：[✓](https://github.com/lzhxmu/VTW) ・ リポジトリ内被引用：10  
  例えばLLaVAでは336×336画像を576個の視覚トークンに変換し、システム指示、ユーザー質問、生成済みのテキストトークンとともにデコーダへ流す。

- **2023-12 · [LLMCompass: Enabling Efficient Hardware Design for Large Language Model Inference](2023-2312.03134-llmcompass-enabling-efficient-hardware-design-for-large-language-model-i.md)**  
  実装：[✓](https://github.com/PrincetonUniversity/LLMCompass) ・ リポジトリ内被引用：10  
  大規模言語モデル（Large Language モデル、LLM）の推論には、膨大な重みを保存するメモリ、行列演算器、注意計算のためのキャッシュ、複数装置間の通信が必要になる。新しいアクセラレータを設計する際、最高演算性能や最高メモリ帯域の仕様だけを比較しても、実際のモデルがどの程度速く動くかは分からない。

- **2024-09 · [Moshi: a speech-text foundation model for real-time dialogue](2024-2410.00037-moshi-a-speech-text-foundation-model-for-real-time-dialogue.md)**  
  実装：[✓](https://github.com/kyutai-labs/moshi) ・ リポジトリ内被引用：9  
  Moshiは、音声認識、テキストLLM、音声合成を順番に実行する音声対話システムを、入力音声を聞きながら出力音声を生成する全二重の音声言語モデルへ置き換える研究である。音声質問応答の零例評価では、MoshiがWeb Questions 26.6%、LLaMA Questions 62.3%、音声版TriviaQA 22.8%の正答率を示した。

- **2024-08 · [Harder Task Needs More Experts: Dynamic Routing in MoE Models](unknown-7f27cb4187bc-harder-task-needs-more-experts-dynamic-routing-in-moe-models.md)**  
  実装：[✓](https://github.com/ZhenweiAn/Dynamic_MoE) ・ リポジトリ内被引用：9  
  HuangらのACL 2024論文は、ルータの専門家確率を高い順に累積し、閾値を超えた時点で専門家の追加を止める動的ルーティング（動的 ルーティング）を提案する。

- **2024-07 · [Mixture of A Million Experts](2024-2407.04153-mixture-of-a-million-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  混合専門家（Mixture of エキスパート、MoE）は多数の専門家のうち一部だけを活性化することで、総パラメータ容量と各トークンの計算を分離する。

- **2023-11 · [Routing to the Expert: Efficient Reward-guided Ensemble of Large Language Models](2023-2311.08692-routing-to-the-expert-efficient-reward-guided-ensemble-of-large-language.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  本論文が解こうとする問題は、異なる得意分野を持つ既製の大規模言語モデル（LLM）を組み合わせる際、問い合わせごとに候補すべてを実行すると生成計算量が膨らむことである。一方、回答をすべて生成して報酬モデル（reward モデル）で順位付けする方式は品質の良い候補を後から選べるが、候補数に比例する生成費用を必要とする。

- **2023-11 · [Learning to Skip for Language Modeling](2023-2311.15436-learning-to-skip-for-language-modeling.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  モデルを深くすれば表現容量は増えるが、トークン当たりの行列演算と復号遅延も増える。提案するSkipLayerは各層を二値ルータで包み、トークンの現在の隠れ表現から「この層を実行する」か「入力をそのまま次層へ渡す」かを選ぶ。

- **2024-08 · [Mini-Omni: Language Models Can Hear, Talk While Thinking in Streaming](2024-2408.16725-mini-omni-language-models-can-hear-talk-while-thinking-in-streaming.md)**  
  実装：[✓](https://github.com/gpt-omni/mini-omni) ・ リポジトリ内被引用：8  
  Mini-Omniは、言語モデルの応答文を最後まで生成してから独立した音声合成器へ渡す従来の直列方式を避け、文字トークンと音声トークンを一つの自己回帰生成過程の中で並列に出力する音声対話モデルである。

- **2024-05 · [xRAG: Extreme Context Compression for Retrieval-augmented Generation with One Token](2024-2405.13792-xrag-extreme-context-compression-for-retrieval-augmented-generation-with.md)**  
  実装：[✓](https://github.com/Hannibal046/xRAG) ・ リポジトリ内被引用：8  
  検索拡張生成（Retrieval-Augmented Generation、RAG）は、外部の文書から関連情報を検索し、その本文を言語モデルへ入力することで、学習時点に含まれない知識を利用する。

- **2024-03 · [Optimizing LLM Queries in Relational Data Analytics Workloads](2024-2403.05821-optimizing-llm-queries-in-relational-data-analytics-workloads.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  理論上の最適解を探す最適接頭辞ヒット再帰（Optimal Prefix Hit Recursion、OPHR）は組合せ爆発を起こすため、実用方式として貪欲群再帰（Greedy Group Recursion、GGR）を設計する。

- **2024-01 · [Lightning Attention-2: A Free Lunch for Handling Unlimited Sequence Lengths in Large Language Models](2024-2401.04658-lightning-attention-2-a-free-lunch-for-handling-unlimited-sequence-lengt.md)**  
  実装：[✓](https://github.com/OpenNLPLab/lightning-attention) ・ リポジトリ内被引用：8  
  一覧用要約：Lightning 注意機構-2は因果線形注意を現在のタイル内と過去タイルからの寄与に分解し、タイル内を因果マスク付き通常行列積、タイル間を固定サイズの累積KV状態による右積で計算する。前向き・逆向きの両方をTritonで入出力認識型に実装し、長系列でも学習速度と作業メモリを安定させる。

- **2024-10 · [Minions: Accelerating Large Language Model Inference with Aggregated Speculative Execution](2024-2402.15678-minions-accelerating-large-language-model-inference-with-aggregated-speculative-execution.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  複数小型モデルの重み付き多数決、オンライン投機長調整、SSM/LLM非同期パイプラインを統合した投機的復号サービング。

- **2024-04 · [Language Model Cascades: Token-level uncertainty and beyond](2024-2404.10136-language-model-cascades-token-level-uncertainty-and-beyond.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  本論文は、入力ごとに必要な推論計算量を変える「モデル段階実行」（モデル cascade）の委譲規則を、生成言語モデルに合わせて設計する研究である。

- **2024-09 · [Discovering the Gems in Early Layers: Accelerating Long-Context LLMs with 1000x Input Token Reduction](2024-2409.17422-discovering-the-gems-in-early-layers-accelerating-long-context-llms-with.md)**  
  実装：[✓](https://github.com/SalesforceAIResearch/GemFilter) ・ リポジトリ内被引用：6  
  GemFilterは、長い入力文脈を持つ大規模言語モデル（LLM）の推論を高速化するため、回答に関係する入力トークンをモデルの比較的早い層で選び、その短い部分列だけを全層で再処理する手法である。

- **2024-04 · [MixLoRA: Enhancing Large Language Models Fine-Tuning with LoRA-based Mixture of Experts](2024-2404.15159-mixlora-enhancing-large-language-models-fine-tuning-with-lora-based-mixt.md)**  
  実装：[✓](https://github.com/TUDB-Labs/MixLoRA) ・ リポジトリ内被引用：6  
  大規模言語モデルを多くの下流タスクへ適応させるとき、全パラメータを更新する方式は学習用メモリと計算時間が大きい。著者の概要にある「約30%のトークン計算遅延削減」は、元のMixLoRA実装に対する最適化効果を指す総括値であり、通常LoRAより30%速いという意味ではない。

- **2024-03 · [Scattered Mixture-of-Experts Implementation](2024-2403.08245-scattered-mixture-of-experts-implementation.md)**  
  実装：[✓](https://github.com/shawntan/scattermoe) ・ リポジトリ内被引用：6  
  特にバッチが大きい学習や複数要求の推論では、中間のトークン表現を何度も高帯域メモリへ書き戻すことが問題になる。ScatterMoEは専門家へ割り当てたトークンを実体の配列として並べ替える代わりに、専門家順の索引を並べ替え、カーネルが入力の必要な位置を直接読み込む。

- **2024-03 · [PipeRAG: Fast Retrieval-Augmented Generation via Algorithm-System Co-design](2024-2403.05676-piperag-fast-retrieval-augmented-generation-via-algorithm-system-co-desi.md)**  
  実装：[✓](https://github.com/amazon-science/piperag) ・ リポジトリ内被引用：6  
  検索拡張生成（Retrieval-Augmented Generation、RAG）では、生成開始前に一度だけ外部情報を検索する方式に加え、生成文が伸びる途中でも検索を繰り返す方式がある。1024トークン生成の端から端の遅延では、同等以上の困惑度を維持しながらRETRO比最大2.6倍の短縮を示す。

- **2023-12 · [Compressed Context Memory For Online Language Model Interaction](2023-2312.03414-compressed-context-memory-for-online-language-model-interaction.md)**  
  実装：[✓](https://github.com/snu-mllab/context-memory) ・ リポジトリ内被引用：6  
  オンライン対話、個人化推薦、複数課題の逐次学習では、要求を受けるたびに新しい文脈が追加される。Compressed Context メモリ（CCM）は、過去の鍵値キャッシュを、専用の圧縮トークンが生成する少数の鍵値へ繰り返し統合する。

- **2024-10 · [LightTransfer: Your Long-Context LLM is Secretly a Hybrid Model with Effortless Adaptation](2024-2410.13846-lighttransfer-your-long-context-llm-is-secretly-a-hybrid-model-with-effo.md)**  
  実装：[✓](https://github.com/sail-sg/LightTrans) ・ リポジトリ内被引用：5  
  キャッシュがGPUメモリを圧迫すると、同時に処理できる要求数が減り、長文脈の生成処理量も低下する。ある層では先頭の少数トークン（注意機構 sink）と直近の窓だけに注意が集中する。

- **2024-04 · [Mitigating the Impact of Outlier Channels for Language Model Quantization with Activation Regularization](2024-2404.03605-mitigating-the-impact-of-outlier-channels-for-language-model-quantizatio.md)**  
  実装：[✓](https://github.com/aninrusimha/qat-pretrain) ・ リポジトリ内被引用：5  
  本研究は、言語モデルの重みと活性値の両方を4ビット整数にするW4A4量子化を、事前学習の段階から成立させる方法を調べる。300Mモデルを後からQAT微調整した試験では、基準に対しパープレキシティが16%悪化したという負の結果が重要である。

- **2024-04 · [Lossless Acceleration of Large Language Model via Adaptive N-gram Parallel Decoding](2024-2404.08698-lossless-acceleration-of-large-language-model-via-adaptive-n-gram-parall.md)**  
  実装：[✓](https://github.com/oujieww/ANPD) ・ リポジトリ内被引用：5  
  適応的N-gram並列復号（適応的 N-gram Parallel Decoding; ANPD）は、大規模言語モデル（LLM）を自己回帰で1トークンずつ実行する代わりに、安価なN-gram表で数トークンの候補を先に作り、元のLLMでまとめて検証する手法である。

- **2024-02 · [Training-Free Long-Context Scaling of Large Language Models](2024-2402.17463-training-free-long-context-scaling-of-large-language-models.md)**  
  実装：[✓](https://github.com/HKUNLP/ChunkLlama) ・ リポジトリ内被引用：5  
  二重チャンク注意（Dual Chunk 注意機構、以下DCA）は、回転位置埋め込み（Rotary Position Embedding、以下RoPE）を用いた大規模言語モデルが、事前学習時より長い系列で位置関係を見失う問題に対する推論時の注意計算の変更である。最後の比較は特定の閉形式4課題の平均であり、汎用能力の94%を意味しない。

- **2024-02 · [Large Language Model Cascades with Mixture of Thought Representations for Cost-efficient Reasoning](2024-2310.03094-large-language-model-cascades-with-mixture-of-thought-representations-fo.md)**  
  実装：[✓](https://github.com/MurongYue/LLM_MoT_cascade) ・ リポジトリ内被引用：5  
  強力な言語モデルをすべての要求へ使用すると、簡単な算数問題にも難しい因果推論にも同じ高価なAPIを呼ぶことになる。一方、安価なモデルだけに切り替えると難問で正答率が落ちる。

- **2024-01 · [CaraServe: CPU-Assisted and Rank-Aware LoRA Serving for Generative LLM Inference](2024-2401.11240-caraserve-cpu-assisted-lora-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  LoRA読込中にCPUでプリフィル計算を先行し、ランク依存のバッチ遅延を予測してSLO違反が少ないサーバへ配分することで、多数アダプタ提供のコールドスタートを隠す。

- **2023-12 · [Honeybee: Locality-enhanced Projector for Multimodal LLM](2023-2312.06742-honeybee-locality-enhanced-projector-for-multimodal-llm.md)**  
  実装：[✓](https://github.com/kakaobrain/honeybee) ・ リポジトリ内被引用：5  
  線形投射器は画像の各位置をほぼ一対一でトークン化するため空間情報を保持しやすいが、解像度が上がると視覚トークン数が増え、言語モデルの計算とメモリを圧迫する。Honeybeeは、出力視覚トークン数を任意に選べることと、局所的な画像構造を保持することを同時に満たす投射器を設計した。

- **2023-12 · [Fluctuation-based Adaptive Structured Pruning for Large Language Models](2023-2312.11983-fluctuation-based-adaptive-structured-pruning-for-large-language-models.md)**  
  実装：[✓](https://github.com/CASIA-IVA-Lab/FLAP) ・ リポジトリ内被引用：5  
  FLAP（FLuctuation-based 適応的 Structured Pruning）は、大規模言語モデル（LLM）の重みを再学習せずに構造化枝刈りする手法である。

- **2024-09 · [Oryx MLLM: On-Demand Spatial-Temporal Understanding at Arbitrary Resolution](2024-2409.12961-oryx-mllm-on-demand-spatial-temporal-understanding-at-arbitrary-resoluti.md)**  
  実装：[✓](https://github.com/Oryx-mllm/Oryx) ・ リポジトリ内被引用：4  
  主要な設計要素は、入力画像の縦横比と解像度を維持して視覚特徴を抽出するOryxViTと、画像・短動画・長動画の用途に応じて視覚トークン数を1倍から最大16倍まで圧縮する動的圧縮器（動的 compressor）である。

- **2024-09 · [LLaMA-Omni: Seamless Speech Interaction with Large Language Models](2024-2409.06666-llama-omni-seamless-speech-interaction-with-large-language-models.md)**  
  実装：[✓](https://github.com/ictnlp/LLaMA-Omni) ・ リポジトリ内被引用：4  
  従来のカスケード方式では、音声認識が入力を文字起こしし、その文字列を大規模言語モデルへ渡し、生成されたテキストを音声合成器へ送る。

- **2024-06 · [Measuring and Improving the Energy Efficiency of Large Language Models Inference](2024-f40d5b5275ad-measuring-and-improving-the-energy-efficiency-of-large-language-models-i.md)**  
  実装：[✓](https://github.com/maufadel/EnergyMeter) ・ リポジトリ内被引用：4  
  著者らは推論をモデルパラメータ数だけで比較する慣習にも疑問を投げかけ、層の深さ、注意・フィードフォワードの並列化、バッチ数、量子化形式の実行実装を分けて検証した。

- **2024-04 · [ALTO: An Efficient Network Orchestrator for Compound AI Systems](2024-01aa9dc12834-alto-an-efficient-network-orchestrator-for-compound-ai-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  ALTO（Automatic Language Token Orchestrator）は、言語モデルの生成結果を複数の検索・再順位付け・追加生成段へ渡す複合AIシステムの実行基盤である。論文の実機評価では、応答遅延4秒を目標とする条件で、非逐次転送の比較方式より最大3倍の要求到着負荷を処理し、低負荷での99パーセンタイル遅延を1.8分の1にした。

- **2024-03 · [AI and Memory Wall](2024-2403.14123-ai-and-memory-wall.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  AI向け計算器の演算性能が急速に増える一方、DRAMやデバイス間通信の帯域は同じ速度で増えない。低バッチの自己回帰生成では重みの再読出しが支配的になり、FLOPsだけで推論性能を評価すると誤る。

- **2024-02 · [LQER: Low-Rank Quantization Error Reconstruction for LLMs](2024-2402.02446-lqer-low-rank-quantization-error-reconstruction-for-llms.md)**  
  実装：[✓](https://github.com/ChengZhang-98/lqer) ・ リポジトリ内被引用：4  
  大規模言語モデルの重みを4ビットへ圧縮しても、実行時に半精度へ逆量子化してから行列積を計算するなら、重みの保存容量削減がそのまま演算器の省資源化につながるとは限らない。

- **2024-02 · [Accurate LoRA-Finetuning Quantization of LLMs via Information Retention](2024-2402.05445-accurate-lora-finetuning-quantization-of-llms-via-information-retention.md)**  
  実装：[✓](https://github.com/AI-Efficiency/IR-QLoRA) ・ リポジトリ内被引用：4  
  大規模言語モデルの重みを16ビットから4ビット以下へ縮めると、重みの保存量と推論時に必要な重み転送量を減らせる。量子化後の基盤重みを固定し、小さな低ランク適応行列だけを微調整するQLoRA系の方法でも、失われた情報を十分に取り戻せない場合がある。

- **2024-01 · [APAR: LLMs Can Do Auto-Parallel Auto-Regressive Decoding](2024-2401.06761-apar-llms-can-do-auto-parallel-auto-regressive-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  各トークンの生成にはモデル重みの読み込みと注意計算が必要で、単一要求ではGPUの演算器が十分使われない一方、多数要求では注意計算とKVキャッシュ容量が制約になる。重要なのは独立した段落を別々の生成系列として同時に進めることであり、単に次の複数トークンを予測して検証する投機的復号（投機的復号）とは異なる。

- **2024-01 · [A Comprehensive Survey of Compression Algorithms for Language Models](2024-2401.15347-a-comprehensive-survey-of-compression-algorithms-for-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  枝刈り、量子化、知識蒸留、低ランク近似、パラメータ共有、効率的構造設計の六系統を、圧縮後の性能だけでなく、圧縮を実行するための学習・較正費用から比較するサーベイ。

- **2023-11 · [GateLoop: Fully Data-Controlled Linear Recurrence for Sequence Modeling](2023-2311.01927-gateloop-fully-data-controlled-linear-recurrence-for-sequence-modeling.md)**  
  実装：[✓](https://github.com/tobiaskatsch/GatedLinearRNN) ・ リポジトリ内被引用：4  
  一方、状態空間モデルや線形再帰モデルは、過去を有限の隠れ状態へ圧縮して逐次更新できるが、保持・忘却の速度を固定の状態遷移係数に依存させる方式では、入力内容に応じて重要な情報だけを残す操作が難しい。

- **2024-10 · [SplitLLM: Collaborative Inference of LLMs for Model Placement and Throughput Optimization](2024-2410.10759-splitllm-collaborative-inference-of-llms-for-model-placement-and-through.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  提案方式は、層ごとの端末推論時間、端末からサーバーへの上り転送時間、サーバーから端末への下り転送時間、サーバー資源消費量を測定し、モデルの順方向の依存関係を守りながら配置する。

- **2024-10 · [CoreInfer: Accelerating Large Language Model Inference with Semantics-Inspired Adaptive Sparse Activation](2024-2410.18311-coreinfer-accelerating-large-language-model-inference-with-semantics-ins.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  文の意味が安定している間は、生成トークンが変わっても必要なFFNニューロンの集合は大きく変わらない。プリフィル時に文単位の重要ニューロンを決めて生成中に固定し、トークンごとの予測器と頻繁な重み配置変更を避ける。

- **2024-06 · [ProTrain: Efficient LLM Training via Memory-Aware Techniques](2024-2406.08334-protrain-efficient-llm-training-via-memory-aware-techniques.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  モデル状態と活性値の階層管理を費用モデルで自動調整し、限られたGPUメモリで学習容量とスループットを高める。

- **2024-06 · [Optimised Grouped-Query Attention Mechanism for Transformers](2024-2406.14963-optimised-grouped-query-attention-mechanism-for-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  既存の多頭注意（Multi-Head 注意機構、MHA）を、複数の質問ヘッドで鍵・値ヘッドを共有するグループ化質問注意（Grouped-Query 注意機構、GQA）へ変換すると、復号時に保存する鍵値キャッシュと鍵値投影のパラメータを減らせる。

- **2024-05 · [I-LLM: Efficient Integer-Only Inference for Fully-Quantized Low-Bit Large Language Models](2024-2405.17849-i-llm-efficient-integer-only-inference-for-fully-quantized-low-bit-large.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  I-LLMは、LLMの重みと活性値を低ビットへ量子化するだけでなく、注意機構のSoftmax、ゲート付き活性化のSwiGLU、RMSNormなどの非線形演算も整数演算へ置き換える学習後量子化（PTQ）方式である。

- **2024-04 · [LongVLM: Efficient Long Video Understanding via Large Language Models](2024-2404.03384-longvlm-efficient-long-video-understanding-via-large-language-models.md)**  
  実装：[✓](https://github.com/ziplab/LongVLM) ・ リポジトリ内被引用：3  
  LongVLMは、長時間動画を入力する視覚言語モデル（Vision-Language モデル; VLM）で、画像符号化器から出る大量の視覚トークンを短時間区間ごとに統合する。100フレームを224×224画素で符号化し、元のパッチ特徴が約25,600トークンになる設定で、10区間×30トークンと全体特徴5トークンの計305視覚トークンへまとめる。

- **2024-02 · [Small Models, Big Insights: Leveraging Slim Proxy Models To Decide When and What to Retrieve for LLMs](2024-2402.12052-small-models-big-insights-leveraging-slim-proxy-models-to-decide-when-an.md)**  
  実装：[✓](https://github.com/plageon/SlimPlm) ・ リポジトリ内被引用：3  
  従来の自己評価型方式は大型言語モデル自身に暫定回答や判断を作らせるため、検索要否を知る段階で高価な大型モデル推論が増える。

- **2024-02 · [BlackMamba: Mixture of Experts for State-Space Models](2024-2402.01771-blackmamba-mixture-of-experts-for-state-space-models.md)**  
  実装：[✓](https://github.com/Zyphra/BlackMamba) ・ リポジトリ内被引用：3  
  選択的状態空間モデルの固定状態生成と、混合専門家層の疎な全結合計算を一つの言語モデルに組み込み、長系列生成・学習計算量・専門家の割当てを同時に評価した。

- **2023-12 · [Understanding the Potential of FPGA-Based Spatial Acceleration for Large Language Model Inference](2023-2312.15159-understanding-the-potential-of-fpga-based-spatial-acceleration-for-large.md)**  
  実装：[✓](https://github.com/cornell-zhang/allo/tree/main/examples) ・ リポジトリ内被引用：3  
  大規模言語モデルの推論を再構成可能な論理回路（FPGA）へ載せる従来方式の多くは、同じ演算器を複数の演算子・層へ順番に割り当てる時間多重型である。AMD Alveo U280上のGPT-2では、同じFPGAのDFXに対してプリフィル2.16倍、復号1.10倍の高速化を報告する。

- **2024-06 · [Divergent Token Metrics: Measuring degradation to prune away LLM components -- and optimize quantization](2024-2311.01544-divergent-token-metrics-measuring-degradation-to-prune-away-llm-componen.md)**  
  実装：[✓](https://github.com/Aleph-Alpha/Divergent_Tokens) ・ リポジトリ内被引用：2  
  大規模言語モデルの圧縮では、重みを0にする枝刈りや、浮動小数点数を整数へ変換する量子化が、生成文をどの時点から変えてしまうかを把握する必要がある。この指標を使って行列ごとの枝刈り率を配分すると、Llama-2-13Bを全体75%疎化したとき、同じ平均疎化率の一様な大きさ基準の枝刈りより、WikiText2のPPLを13.512から8.101へ抑えられる。

- **2024-06 · [DeciMamba: Exploring the Length Extrapolation Potential of Mamba](2024-2406.14528-decimamba-exploring-the-length-extrapolation-potential-of-mamba.md)**  
  実装：[✓](https://github.com/assafbk/DeciMamba) ・ リポジトリ内被引用：2  
  Mambaは選択的状態空間モデル（Selective State Space モデル; SSM）の一種で、注意機構のように系列長の二乗へ比例する全組合せを直接計算せず、再帰的な隠れ状態へ過去の情報を集約する。

- **2024-05 · [Post Training Quantization of Large Language Models with Microscaling Formats](2024-2405.07135-post-training-quantization-of-large-language-models-with-microscaling-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  本論文は、大規模言語モデル（LLM）の事後量子化（post-学習 量子化, PTQ）で広く使われるSmoothQuant、活性認識重み量子化（AWQ）、勾配不要の重み誤差補償（GPTQ）を、ブロックごとに尺度を共有する微小尺度（microscaling, MX）形式へ拡張し、三方式の組合せと適用順序を体系的に評価した研究である。

- **2024-03 · [SynCode: LLM Generation with Grammar Augmentation](2024-2403.01632-syncode-llm-generation-with-grammar-augmentation.md)**  
  実装：[✓](https://github.com/structuredllm/syncode) ・ リポジトリ内被引用：2  
  SynCodeは、言語モデルがJSON、SQL、Python、Goなどの形式言語を生成する際に、文脈自由文法（CFG）を満たすトークンだけを次の候補として残す制約付き復号方式である。

- **2024-03 · [Decoding Compressed Trust: Scrutinizing the Trustworthiness of Efficient LLMs Under Compression](2024-2403.15447-decoding-compressed-trust-scrutinizing-the-trustworthiness-of-efficient-.md)**  
  実装：[✓](https://github.com/decoding-comp-trust/comp-trust) ・ リポジトリ内被引用：2  
  LLM圧縮の評価は、通常の質問応答や知識課題の性能を維持できるかに偏りがちである。評価の中心的な結果は、同程度に圧縮する場合は量子化が枝刈りより元モデルの信頼性を再現しやすいこと、4-bit量子化では一部軸が改善し得ること、3-bitでは通常性能に現れにくい深刻な回帰が生じることである。

- **2024-03 · [Cobra: Extending Mamba to Multi-Modal Large Language Model for Efficient Inference](2024-2403.14520-cobra-extending-mamba-to-multi-modal-large-language-model-for-efficient-.md)**  
  実装：[✓](https://github.com/h-zhao1997/cobra) ・ リポジトリ内被引用：2  
  提案の中心は、既存のMamba言語モデルへ視覚情報を接続する設計と学習方法を評価した点にある。単一のNVIDIA A100 PCIe 80GBで、画像1枚と同じ質問を入力し256トークンを生成する実験では、Cobra-3.5Bが1.54秒・166.47トークン/秒、MobileVLM v2-3Bが5.17秒・49.50トークン/秒である。

- **2024-02 · [LongHeads: Multi-Head Attention is Secretly a Long Context Processor](2024-2402.10685-longheads-multi-head-attention-is-secretly-a-long-context-processor.md)**  
  実装：[✓](https://github.com/LuLuLuyi/LongHeads) ・ リポジトリ内被引用：2  
  LongHeadsは、事前学習時よりはるかに長い文章を既存の大規模言語モデルへ与える際、各注意頭が全文へ注意する必要はないという観察を利用した、追加学習不要の長文推論方式である。LLaMA-2-7Bを単一NVIDIA A100で評価し、32Kのパスキー検索でほぼ100%、CPUへKVキャッシュを退避した128K条件でも2K注意窓で100%を報告する。

- **2024-02 · [Efficient Prompt Caching via Embedding Similarity](2024-2402.01173-efficient-prompt-caching-via-embedding-similarity.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  本論文は、言語モデルの生成済み応答そのものを再利用するプロンプトキャッシュの判定精度を改善する研究である。以前の質問に対する回答がキャッシュにあれば、新しい質問を言語モデルへ送らず、その回答を返すことができる。ただし、質問文の意味が近いことと、同じ回答で両方の質問に正しく答えられることは一致しない。

- **2023-12 · [ZeroQuant(4+2): Redefining LLMs Quantization with a New FP6-Centric Strategy for Diverse Generative Tasks](2023-2312.08583-zeroquant-4-2-redefining-llms-quantization-with-a-new-fp6-centric-strate.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  4ビット整数量子化（INT4）が自由生成課題で不安定になる条件を測り、6ビット浮動小数点（FP6）の品質を、4+2ビットの格納・復号方式と指数バイアスの事前変換によって既存GPU上で利用する研究。

- **2023-11 · [One Pass Streaming Algorithm for Super Long Token Attention Approximation in Sublinear Space](2023-2311.14652-one-pass-streaming-algorithm-for-super-long-token-attention-approximatio.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  長大な文脈を扱う注意機構では、問い合わせ、鍵、値の各行列から計算される注意重みが系列長に伴って大きくなる。主結果は実験的な高速化ではなく、厳密な入力条件の下での確率的な誤差・空間・復元時間の保証である。

- **2024-08 · [Fortify the Shortest Stave in Attention: Enhancing Context Awareness of Large Language Models for Effective Tool Use](2024-2312.04455-fortify-the-shortest-stave-in-attention-enhancing-context-awareness-of-l.md)**  
  実装：[✓](https://github.com/Fiorina1212/Attention-buckets) ・ リポジトリ内被引用：1  
  提案方式注意機構 Bucketsは、学習済みモデルの重みを変更せず、同じ入力文脈を複数の分岐へ複製し、それぞれ異なるRoPE基数を適用する。

- **2024-08 · [Context-Aware Assistant Selection for Improved Inference Acceleration with Large Language Models](2024-2408.08470-context-aware-assistant-selection-for-improved-inference-acceleration-wi.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号（投機的復号）は小さなドラフトモデルが複数トークンを先読みし、大きな対象モデルがまとめて検証することで逐次生成の遅延を削減する。

- **2024-04 · [Hierarchical Context Merging: Better Long Context Understanding for Pre-trained LLMs](2024-2404.10308-hierarchical-context-merging-better-long-context-understanding-for-pre-t.md)**  
  実装：[✓](https://github.com/alinlab/HOMER) ・ リポジトリ内被引用：1  
  HOMER（Hierarchical cOntext MERging）は、入力を小区間に分けて初期層を処理し、中間層へ進むにつれて隣接区間を統合する。ICLR 2024の原著では、Llama-2-13B-chatの32Kトークンにおけるパスキー検索正答率が80.4%、位置尺度変更方式との併用で86.0%だった。

- **2024-03 · [Repoformer: Selective Retrieval for Repository-Level Code Completion](2024-2403.10059-repoformer-selective-retrieval-for-repository-level-code-completion.md)**  
  実装：[✓](https://github.com/amazon-science/Repoformer) ・ リポジトリ内被引用：1  
  Repoformerは、ソースコードの現在のファイルだけでは分からない別ファイルの関数定義や呼出し関係を、必要な場合だけ検索するコード補完方式である。RepoEvalで複数のコード言語モデルを調べると、検索によって補完が改善した例は概ね20%以下、変わらない例が60%以上、悪化する例も約20%あった。

- **2024-02 · [Guiding LLMs The Right Way: Fast, Non-Invasive Constrained Generation](2024-2403.06988-guiding-llms-the-right-way-fast-non-invasive-constrained-generation.md)**  
  実装：[✓](https://github.com/eth-sri/domino) ・ リポジトリ内被引用：1  
  制約付き復号（constrained デコード）は、各生成段階で許される次トークンを文法で絞り、出力の構文的な妥当性を保証する。これが単なる書式上の違いにとどまらず、推論問題の正解率を損なうことを本論文は実験で示した。提案するDOMINOは、文法を解釈する字句解析器（scanner）と構文解析器（parser）を分ける。

- **2024-02 · [Generative Representational Instruction Tuning](2024-2402.09906-generative-representational-instruction-tuning.md)**  
  実装：[✓](https://github.com/ContextualAI/gritlm) ・ リポジトリ内被引用：1  
  GRIT（Generative Representational Instruction Tuning）は、文章生成と文章埋込みを一つの大規模言語モデルで処理するための指示調整方式である。7BモデルのGritLM-7Bは、56データ集合からなるMTEBの平均66.8を示し、同じ基盤モデルから表現専用で訓練した比較版の66.8と同等だった。

- **2024-02 · [FlattenQuant: Breaking Through the Inference Compute-bound for Large Language Models with Per-tensor Quantization](2024-2402.17985-flattenquant-breaking-through-the-inference-compute-bound-for-large-lang.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  FlattenQuantは、大規模言語モデル（LLM）の推論で、重みだけを低ビット化しても行列演算が半精度のまま残るという問題を解く後学習量子化（post-学習 量子化; PTQ）方式である。難点は、LLMの活性値に他のチャネルより20〜100倍程度大きい外れ値チャネルが存在することだ。

- **2024-01 · [Inferflow: an Efficient and Highly Configurable Inference Engine for Large Language Models](2024-2401.08294-inferflow-an-efficient-and-highly-configurable-inference-engine-for-larg.md)**  
  実装：[✓](https://github.com/inferflow/inferflow) ・ リポジトリ内被引用：1  
  Inferflowは、言語モデルの構造が頻繁に変化する状況で、モデルごとに推論エンジンのソースコードを書き足す負担を減らすことを主目的とした推論基盤である。この拡張性に加え、低ビット量子化と複数GPU分割による実行効率を追求する。

- **2023-11 · [Linear Log-Normal Attention with Unbiased Concentration](2023-2311.13541-linear-log-normal-attention-with-unbiased-concentration.md)**  
  実装：[✓](https://github.com/ynahshan/linear-lognormal-attention) ・ リポジトリ内被引用：1  
  本研究が扱う問題は、系列長が伸びると通常の自己注意（self-注意機構）のスコア行列が二次的に増大する一方、その行列を単に線形化した方式では言語理解の精度が落ちやすいことである。系列長4096での学習反復時間は標準方式6.8秒に対しLLN単独3.2秒、メモリは32.1GBに対し7.5GBだった。

- **2024-10 · [SIGMA: Secure GPT Inference with Function Secret Sharing](2024-c544a15b6867-sigma-secure-gpt-inference-with-function-secret-sharing.md)**  
  実装：[✓](https://github.com/mpc-msri/EzPC/tree/master/GPU-MPC/experiments/sigma) ・ リポジトリ内被引用：0  
  SIGMAは関数秘密分散（Function Secret Sharing; FSS）によって複雑な非線形演算を二者間で実現し、事前に作った暗号鍵を使ってオンライン時の通信を抑える。代表結果は、系列長128の二者間オンライン推論において、既存のGPU秘匿計算系CrypTenより12.2～19倍短い実行時間である。

- **2024-10 · [Scaling Stick-Breaking Attention: An Efficient Implementation and In-depth Study](2024-2410.17980-scaling-stick-breaking-attention-an-efficient-implementation-and-in-dept.md)**  
  実装：[✓](https://github.com/shawntan/stickbreaking-attention) ・ リポジトリ内被引用：0  
  本論文は、通常のTransformerが採用する正規化指数関数（softmax）に基づく自己注意（self-注意機構）を、棒折り過程（stick-breaking process）で定義される別の注意重みへ置き換える研究である。

- **2024-09 · [DisDP: Disaggregating Compute, Network, and Storage for Model-Sharded Data-Parallel Training](2024-2409.00918-luwu-an-end-to-end-in-network-out-of-core-optimizer-for-100b-scale-model-in-network-data-parallel-training-on-distribute.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPUから通信とオプティマイザ状態をSmartNIC・SmartSwitch・単一パラメータサーバへ分離し、100B級モデル分割データ並列の干渉と容量制約を同時に減らす。

- **2024-06 · [Adam-mini: Use Fewer Learning Rates To Gain More](2024-2406.16793-adam-mini-use-fewer-learning-rates-to-gain-more.md)**  
  実装：[✓](https://github.com/zyushun/Adam-mini) ・ リポジトリ内被引用：0  
  大規模言語モデルの事前学習や追加学習では、モデル重みだけでなく勾配とオプティマイザ（optimizer）の内部状態がGPUメモリを消費する。CPUへのオフロードや分散シャーディングは容量不足を緩和できる一方、転送・同期の追加費用が発生する。

- **2024-05 · [VideoTree: Adaptive Tree-based Video Representation for LLM Reasoning on Long Videos](2024-2405.19209-videotree-adaptive-tree-based-video-representation-for-llm-reasoning-on-.md)**  
  実装：[✓](https://github.com/Ziyang412/VideoTree) ・ リポジトリ内被引用：0  
  高関連クラスタだけを再分割して細部を調べるため、動画全体を均一に密な説明文へ変換する方式より、不要なフレーム説明や冗長な言語入力を減らせる。原著の主な根拠は、EgoSchema検証部分集合で66.2%の正答率、LLoVi-bestの61.2%に対して20.1秒対24.8秒という比較である。

- **2024-02 · [User-LLM: Efficient LLM Contextualization with User Embeddings](2024-2402.13598-user-llm-efficient-llm-contextualization-with-user-embeddings.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  履歴を項目IDと属性IDの列として符号化し、小型の自己回帰型利用者エンコーダで密なベクトル列へ変換した後、LLMの中間層に交差注意（cross-注意機構）で取り込ませる。MovieLens 20M、Google Review、Amazon Reviewを用いた実験では、長い履歴を使うほど計算量削減が顕著になった。

- **2024-02 · [SparseLLM: Towards Global Pruning for Pre-trained Language Models](2024-2402.17946-sparsellm-towards-global-pruning-for-pre-trained-language-models.md)**  
  実装：[✓](https://github.com/BaiTheBest/SparseLLM) ・ リポジトリ内被引用：0  
  大規模言語モデルの重みを間引く非構造化枝刈りは、モデルの保存容量と演算の理論上の非ゼロ要素数を減らせる。原著のOPT-1.3B、WikiText2、重みの80%を疎化した条件では、SparseGPTの困惑度69.67に対しSparseLLMは58.92である。

- **2024-01 · [With Greater Text Comes Greater Necessity: Inference-Time Training Helps Long Text Generation](2024-2401.11504-with-greater-text-comes-greater-necessity-inference-time-training-helps-.md)**  
  実装：[✓](https://github.com/TemporaryLoRA/Temp-LoRA) ・ リポジトリ内被引用：0  
  本論文が扱うのは、数十万トークン規模の小説生成や長編翻訳を、短い注意窓しか持たない言語モデルで継続するときに発生する「古い情報の消失」と「長い鍵・値キャッシュ（KVキャッシュ）の費用」の両立問題である。近い文脈は通常の注意機構で直接読み、古い情報は一時的に変化した重みを介して利用する。

- **2024-01 · [Infini-gram: Scaling Unbounded n-gram Language Models to a Trillion Tokens](2024-2401.17377-infini-gram-scaling-unbounded-n-gram-language-models-to-a-trillion-token.md)**  
  実装：[✓](https://github.com/liujch1998/infini-gram) ・ リポジトリ内被引用：0  
  従来のn-gram方式は直前の数トークンしか参照しないため、長い固有表現や定型句を扱いにくかった。

### 4年前（2022-11〜2023-10）

- **2023-07 · [FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](2023-2307.08691-flashattention-2.md)**  
  実装：[✓](https://github.com/Dao-AILab/flash-attention) ・ リポジトリ内被引用：316  
  初代FlashAttentionのオンライン・ソフトマックスとタイル分割を保ちつつ、行列積以外の演算とブロック・ワープ間の仕事分割を再設計し、A100で理論演算性能の最大73%と初代比約2倍の高速化を達成する。

- **2022-11 · [SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models](2022-2211.10438-smoothquant-accurate-and-efficient-post-training-quantization-for-large-language-models.md)**  
  実装：[✓](https://github.com/mit-han-lab/smoothquant) ・ リポジトリ内被引用：272  
  活性値全体を単純に8ビットへ写すと、その少数の外れ値が量子化範囲を広げ、通常値へ割り当てられる段階数が減って精度が崩れる。OPT、BLOOM、GLM、MT-NLGなどで8ビット重み・8ビット活性値（W8A8）を実現し、精度低下をほぼ抑えながら最大1.56倍の推論高速化と2倍のメモリ削減を報告し、530Bモデルを単一ノードで提供可能にした。

- **2023-05 · [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](2023-2305.13245-gqa.md)**  
  実装：✓ ・ リポジトリ内被引用：247  
  標準の多頭注意（Multi-Head 注意機構; MHA）は各クエリ頭に独立した鍵頭と値頭を持つため、復号時には全KV頭のキャッシュを読み出す必要がある。

- **2022-11 · [Efficiently Scaling Transformer Inference](2022-2211.05102-efficiently-scaling-transformer-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：171  
  TPU v4上の大規模Transformer推論を通信・メモリ・計算モデルから設計し、2D重み固定/重み収集の切替とバッチ分割MQAで540B級の低遅延・高MFU・長文脈を両立する。

- **2023-01 · [SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot](2023-2301.00774-sparsegpt-massive-language-models-can-be-accurately-pruned-in-one-shot.md)**  
  実装：[✓](https://github.com/IST-DASLab/sparsegpt) ・ リポジトリ内被引用：125  
  重みの絶対値が小さい順に削除する単純な枝刈りでは、巨大モデルであっても削除による層出力誤差が累積し、50%の疎化で性能が崩壊し得る。

- **2023-06 · [A Simple and Effective Pruning Approach for Large Language Models](2023-2306.11695-a-simple-and-effective-pruning-approach-for-large-language-models.md)**  
  実装：[✓](https://github.com/locuslab/wanda) ・ リポジトリ内被引用：121  
  Wanda（重みと活性による枝刈り、枝刈り by 重み and 活性値）は、大規模言語モデルの線形層を追加学習も残存重みの更新も行わず疎化する方法である。LLaMA-7Bを50%非構造疎化したとき、WikiTextの困惑度は単純大きさ枝刈り17.29、Wanda 7.26、SparseGPT 7.22であり、軽い処理でも品質を大幅に保てる。

- **2023-08 · [OmniQuant: Omnidirectionally Calibrated Quantization for Large Language Models](2023-2308.13137-omniquant-omnidirectionally-calibrated-quantization-for-large-language-m.md)**  
  実装：[✓](https://github.com/OpenGVLab/OmniQuant) ・ リポジトリ内被引用：99  
  大規模言語モデルの重みを16ビットから4ビット、3ビット、2ビットへ縮めると、保存容量と重み転送量を大きく削減できる。一方、極低ビットでは重みや活性値の少数の外れ値が量子化範囲を広げ、重要な値の量子化刻みが粗くなって出力品質が崩れる。LLaMA-2 7B～70Bは128個の校正系列とA100 40GB 1基で1～16時間の処理が可能と報告される。

- **2023-05 · [LLM-Pruner: On the Structural Pruning of Large Language Models](2023-2305.11627-llm-pruner-on-the-structural-pruning-of-large-language-models.md)**  
  実装：[✓](https://github.com/horseee/LLM-Pruner) ・ リポジトリ内被引用：97  
  LLM-Prunerは、大規模言語モデルのパラメータを実際に削除して小さい密行列モデルへ変換する構造枝刈り手法である。LLaMA-7B、Vicuna-7B、ChatGLM-6Bを評価し、LLaMA-7Bでは20%の構造削減でゼロショット七課題平均が63.25から56.82へ下がり、低ランク適応後60.07まで回復した。

- **2023-10 · [DistillSpec: Improving Speculative Decoding via Knowledge Distillation](2023-2310.08461-distillspec-improving-speculative-decoding-via-knowledge-distillation.md)**  
  実装：✓ ・ リポジトリ内被引用：81  
  ドラフト自身の生成データと課題別の分布間距離でターゲットとの整合を蒸留し、投機的デコードの候補受理率を上げる手法。

- **2023-05 · [LLM-QAT: Data-Free Quantization Aware Training for Large Language Models](2023-2305.17888-llm-qat-data-free-quantization-aware-training-for-large-language-models.md)**  
  実装：[✓](https://github.com/facebookresearch/LLM-QAT) ・ リポジトリ内被引用：74  
  LLM-QATは、学習後量子化（Post-学習 量子化: PTQ）では精度が大きく低下する低ビット領域に対し、量子化誤差を学習中に経験させる量子化対応学習（Quantization-Aware 学習: QAT）を大規模言語モデルへ適用する研究である。

- **2023-05 · [RWKV: Reinventing RNNs for the Transformer Era](2023-2305.13048-rwkv-reinventing-rnns-for-the-transformer-era.md)**  
  実装：[✓](https://github.com/BlinkDL/RWKV-LM) ・ リポジトリ内被引用：71  
  RWKVの大きな特徴は、単に注意を近似して軽量化することではなく、同じ重みと演算を訓練時の並列形式と推論時の再帰形式の双方で扱うことである。論文自身も長文脈評価の一部で弱点を示し、指示の順序を変えるだけで下流評価が大きく改善する例を報告している。

- **2023-10 · [Ring Attention with Blockwise Transformers for Near-Infinite Context](2023-2310.01889-ring-attention-blockwise-transformers.md)**  
  実装：[✓](https://github.com/lhao499/llm_large_context) ・ リポジトリ内被引用：62  
  キー・値ブロックをリング転送しながらブロック注意計算を重畳し、系列長に依存しない活性化メモリで最大文脈長をデバイス数に比例して拡張する分散注意方式。

- **2023-07 · [Retentive Network: A Successor to Transformer for Large Language Models](2023-2307.08621-retentive-network-a-successor-to-transformer-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：60  
  RetNetは、指数減衰付き保持演算を並列・再帰・チャンク再帰の三形式で同じ重みのまま実行する。6.7Bモデルの8K入力ではTransformerのKVキャッシュ方式に対し復号8.4倍、メモリ約70%削減を報告し、学習の並列性と固定状態復号を両立する。

- **2023-08 · [YaRN: Efficient Context Window Extension of Large Language Models](2023-2309.00071-yarn-efficient-context-window-extension-of-large-language-models.md)**  
  実装：[✓](https://github.com/jquesnelle/yarn) ・ リポジトリ内被引用：57  
  大規模言語モデルの回転位置埋め込み（Rotary Position Embedding、RoPE）は、クエリとキーを位置に応じた角度だけ回転し、両者の内積が相対位置を反映するように設計される。128Kまでのパスキー検索では7B・13Bとも平均正答率99.4%を報告する。

- **2023-04 · [Learning to Compress Prompts with Gist Tokens](2023-2304.08467-learning-to-compress-prompts-with-gist-tokens.md)**  
  実装：[✓](https://github.com/jayelm/gisting) ・ リポジトリ内被引用：52  
  指示の鍵・値状態をそのままキャッシュすれば再計算は減るものの、保持する状態の長さは指示トークン数に比例する。Jesse Muらの研究は、指示の意味を短い要旨トークン（gist トークン）の内部状態へ集約し、後続の異なる入力に再利用する「要旨化（gisting）」を提案する。

- **2023-10 · [Sheared LLaMA: Accelerating Language Model Pre-training via Structured Pruning](2023-2310.06694-sheared-llama-accelerating-language-model-pre-training-via-structured-pr.md)**  
  実装：[✓](https://github.com/princeton-nlp/LLM-Shearing) ・ リポジトリ内被引用：46  
  枝刈り直後に失われた能力は継続事前学習で回復するが、その際にも学習データを元の比率で使い続けず、領域別の損失回復状況に応じて再配分する。A100 80GB上の単一生成で、13億パラメータの均一形状は毎秒58トークン、非均一形状は51トークン、27億では43対37トークンであった。

- **2023-07 · [In-context Autoencoder for Context Compression in a Large Language Model](2023-2307.06945-in-context-autoencoder-for-context-compression-in-a-large-language-model.md)**  
  実装：[✓](https://github.com/getao/icae) ・ リポジトリ内被引用：42  
  本論文は、大規模言語モデル（LLM）の長い入力文脈を、同じモデルがそのまま利用できる短い連続表現へ学習圧縮する文脈内自己符号化器（In-context Autoencoder、ICAE）を提案する。

- **2022-12 · [The case for 4-bit precision: k-bit Inference Scaling Laws](2022-2212.09720-the-case-for-4-bit-precision-k-bit-inference-scaling-laws.md)**  
  実装：✓ ・ リポジトリ内被引用：40  
  量子化では、1パラメータ当たりのビット数を下げるほど同じ重みメモリへ大きなモデルを置ける。

- **2023-10 · [LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression](2023-2310.06839-longllmlingua-accelerating-and-enhancing-llms-in-long-context-scenarios-.md)**  
  実装：[✓](https://aka.ms/LongLLMLingua) ・ リポジトリ内被引用：39  
  LongLLMLinguaは、長いプロンプトを単に一律に切り詰めるのではなく、「質問に対してどの文書・トークンが有用か」を小型言語モデルで推定し、重要部分へトークン予算を集中させる長文脈プロンプト圧縮法である。

- **2023-05 · [FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance](2023-2305.05176-frugalgpt-how-to-use-large-language-models-while-reducing-cost-and-impro.md)**  
  実装：[✓](https://github.com/stanford-futuredata/FrugalGPT) ・ リポジトリ内被引用：39  
  FrugalGPTは、価格・正確さ・誤答の種類が異なる複数の大規模言語モデル（LLM）を、予算を超えずに組み合わせる推論時のサービス選択方式である。

- **2023-08 · [LM-Infinite: Zero-Shot Extreme Length Generalization for Large Language Models](2023-2308.16137-lm-infinite-zero-shot-extreme-length-generalization-for-large-language-m.md)**  
  実装：[✓](https://github.com/Glaciohound/LM-Infinite) ・ リポジトリ内被引用：38  
  LM-Infiniteは、短い系列で学習した大規模言語モデルを追加学習なしで長文脈へ外挿するため、推論時の注意範囲と位置距離の扱いだけを変更する方式である。論文は元の完全注意に対してデコードを約2.7倍高速化し、GPUメモリを最大7.5倍削減したと報告する。

- **2023-10 · [Compressing Context to Enhance Inference Efficiency of Large Language Models](2023-2310.06201-compressing-context-to-enhance-inference-efficiency-of-large-language-mo.md)**  
  実装：[✓](https://github.com/liyucheng09/Selective_Context) ・ リポジトリ内被引用：37  
  長い文書や会話を大規模言語モデル（LLM）へ入力すると、初回入力処理と鍵・値キャッシュに多くの時間・メモリが必要になる。Selective Contextは、下流モデルの構造や重みを変更する代わりに、入力文脈に含まれる予測しやすい語句を事前に削り、残った自然言語テキストだけを渡す。

- **2022-12 · [Hungry Hungry Hippos: Towards Language Modeling with State Space Models](2022-2212.14052-hungry-hungry-hippos-towards-language-modeling-with-state-space-models.md)**  
  実装：[✓](https://github.com/HazyResearch/H3) ・ リポジトリ内被引用：32  
  本論文は、状態空間モデル（state space モデル; SSM）が長系列を効率的に処理できるにもかかわらず、言語モデリングでは注意機構（注意機構）を使う変換器（Transformer）に劣る理由を二つの観点から調べる。

- **2023-05 · [Landmark Attention: Random-Access Infinite Context Length for Transformers](2023-2305.16300-landmark-attention-random-access-infinite-context-length-for-transformer.md)**  
  実装：[✓](https://github.com/epfml/landmark-attention) ・ リポジトリ内被引用：28  
  目印注意（Landmark 注意機構）は、長い文章を一定長のブロックに分け、それぞれの末尾へ特別な目印トークンを挿入し、注意機構そのものに「どの過去ブロックを読み戻すべきか」を学習させる方式である。また、LLaMA-7Bを長さ512の文脈で15,000ステップ微調整した実験では、32Kを超える入力から埋め込んだ合言葉を検索できることを示した。

- **2023-06 · [MiniLLM: On-Policy Distillation of Large Language Models](2023-2306.08543-minillm-on-policy-distillation-of-large-language-models.md)**  
  実装：[✓](https://github.com/microsoft/LMOps/tree/main/minillm) ・ リポジトリ内被引用：27  
  MiniLLMは、大規模な教師言語モデルから小規模な学生言語モデルへ生成能力を移す知識蒸留（Knowledge Distillation; KD）の学習方式である。

- **2023-07 · [LongNet: Scaling Transformers to 1,000,000,000 Tokens](2023-2307.02486-longnet-scaling-transformers-to-1-000-000-000-tokens.md)**  
  実装：[✓](https://aka.ms/LongNet) ・ リポジトリ内被引用：26  
  LongNetは、自己注意の計算量が系列長Nの二乗で増える問題を、拡張注意（dilated 注意機構）で解くTransformer変種である。

- **2023-04 · [Outlier Suppression+: Accurate quantization of large language models by equivalent and optimal shifting and scaling](2023-2304.09145-outlier-suppression-accurate-quantization-of-large-language-models-by-eq.md)**  
  実装：[✓](https://github.com/ModelTC/Outlier_Suppression_Plus) ・ リポジトリ内被引用：25  
  Outlier Suppression+（OS+）は、大規模言語モデルの活性値に現れる極端な外れ値が、事後量子化（Post-学習 量子化: PTQ）の精度を悪化させる問題に対する方法である。

- **2023-10 · [ReLU Strikes Back: Exploiting Activation Sparsity in Large Language Models](2024-2310.04564-relu-strikes-back-exploiting-activation-sparsity-in-large-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  大規模言語モデルは推論時に膨大な重みを読み出す。特に小さなバッチでの一トークンずつの生成では、演算器のピーク性能より高帯域メモリからの重み移動が制約になることが多い。滑らかな活性化関数であるSiLUやGELUは、負の入力でも通常は厳密なゼロを出さないため、出力が小さくても対応する重みの読み出しを機械的に省略しにくい。

- **2023-07 · [Hyena Hierarchy: Towards Larger Convolutional Language Models](2023-2302.10866-hyena-hierarchy-towards-larger-convolutional-language-models.md)**  
  実装：[✓](https://github.com/HazyResearch/safari) ・ リポジトリ内被引用：20  
  従来の線形注意や疎注意はこの費用を減らせる一方、長距離の連想記憶や文脈内での規則適用に必要な表現能力が不足し、密な注意層を混ぜないと大規模モデルの品質に届かない場合があった。著者らは、注意機構が持つ三つの性質、すなわち入力に応じて演算内容が変わること、系列長に対してパラメータ数が線形に増えないこと、任意の過去位置を参照できることに注目した。

- **2023-03 · [Resurrecting Recurrent Neural Networks for Long Sequences](2023-2303.06349-resurrecting-recurrent-neural-networks-for-long-sequences.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  連続時間状態空間モデルの特殊な離散化を出発点とせず、古典的な再帰型ニューラルネットワークを線形化・複素対角化・安定化・正規化することで、長距離依存の精度と並列学習速度を回復できることを、段階的な除去実験で示した研究。論文が測ったのは主として長系列ベンチマークの分類精度と学習速度であり、大規模言語モデルの実運用推論性能ではない。

- **2023-03 · [ZeroQuant-V2: Exploring Post-training Quantization in LLMs from Comprehensive Study to Low Rank Compensation](2023-2303.08302-zeroquant-v2-exploring-post-training-quantization-in-llms-from-comprehen.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  ZeroQuant-V2は、大規模言語モデルの学習後量子化（Post-学習 量子化、PTQ）を、特定の一手法の成功例だけで評価するのではなく、量子化対象、数値精度、粒度、モデル系列、最適化方式を組み合わせて調べた研究である。元の16ビットモデルは10.33なので、この設定では測定上ほぼ同等となる。

- **2023-07 · [Predictive Pipelined Decoding: A Compute-Latency Trade-off for Exact LLM Decoding](2023-2307.05908-predictive-pipelined-decoding-a-compute-latency-trade-off-for-exact-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  予測パイプライン復号（Predictive Pipelined Decoding; PPD）は、自己回帰型の大規模言語モデルが次のトークンを確定するまで、その次のトークンの計算を開始できないという逐次依存を緩める方式である。

- **2023-07 · [Skeleton-of-Thought: Prompting LLMs for Efficient Parallel Generation](2023-2307.15337-skeleton-of-thought-prompting-llms-for-efficient-parallel-generation.md)**  
  実装：[✓](https://github.com/imagination-research/sot) ・ リポジトリ内被引用：13  
  Skeleton-of-Thought（SoT）はモデル内部の注意カーネルを変えず、回答を「骨格作成」と「各項目の独立展開」に分解して、後半を並列実行する。高速化の源泉は総トークン数を必ず減らすことではなく、長い1本の逐次デコードを複数の短いデコードへ分け、クリティカルパスを短くする点にある。

- **2023-07 · [When Not to Trust Language Models: Investigating Effectiveness of Parametric and Non-Parametric Memories](2023-2212.10511-when-not-to-trust-language-models-investigating-effectiveness-of-paramet.md)**  
  実装：[✓](https://github.com/AlexTMallen/adaptive-retrieval) ・ リポジトリ内被引用：12  
  著者らは、質問の対象実体のウィキペディア閲覧数を人気度の代理指標として、質問の関係種別ごとに閾値を学習し、閾値未満の質問だけ外部文書を検索する適応的検索（適応的 Retrieval）を提案した。PopQAで最良の組合せは正答率46.5%となり、どの常時検索・検索なしの構成よりも5.3ポイント高いと報告する。

- **2023-05 · [Let's Sample Step by Step: Adaptive-Consistency for Efficient Reasoning and Coding with LLMs](2023-2305.11860-let-s-sample-step-by-step-adaptive-consistency-for-efficient-reasoning-a.md)**  
  実装：[✓](https://sample-step-by-step.info) ・ リポジトリ内被引用：12  
  大規模言語モデル（LLM）で多段階推論の精度を上げる自己整合性（自己整合性）は、同じ質問に対して複数の思考連鎖を標本化し、最終回答を多数決する方式である。最大7.9倍の節約は個別条件の値であり、全条件平均ではない。

- **2023-10 · [Merging Experts into One: Improving Computational Efficiency of Mixture of Experts](2023-2310.09832-merging-experts-into-one-improving-computational-efficiency-of-mixture-o.md)**  
  実装：[✓](https://github.com/Shwai-He/MEO) ・ リポジトリ内被引用：10  
  混合専門家（Mixture of エキスパート; MoE）モデルは、入力ごとに一部の専門家だけを選んで計算することで、全パラメータを常に実行する密モデルより計算費用を抑える。

- **2023-07 · [MovieChat: From Dense Token to Sparse Memory for Long Video Understanding](2023-2307.16449-moviechat-from-dense-token-to-sparse-memory-for-long-video-understanding.md)**  
  実装：[✓](https://github.com/rese1f/MovieChat) ・ リポジトリ内被引用：10  
  MovieChatは、固定長の短期記憶を逐次更新し、古いフレームを類似度に応じて統合した長期記憶へ送ることで、この問題を扱う。原著図1は、224×224画素のフレームを標本抽出なしで処理する視覚側の条件で、24GB GPU上で10,000フレーム超を扱えると報告する。

- **2023-07 · [Efficient Guided Generation for Large Language Models](2023-2307.09702-efficient-guided-generation-for-large-language-models.md)**  
  実装：[✓](https://github.com/dottxt-ai/outlines) ・ リポジトリ内被引用：10  
  従来方式は、各生成ステップで語彙中のN個のトークン文字列を照合し、現在の部分出力に続けてよいかを調べるため、制約判定が少なくとも語彙数に比例する。

- **2023-05 · [Unlimiformer: Long-Range Transformers with Unlimited Length Input](2023-2305.01625-unlimiformer-long-range-transformers-with-unlimited-length-input.md)**  
  実装：[✓](https://github.com/abertsch72/unlimiformer) ・ リポジトリ内被引用：9  
  文書が長いほど参照すべきキーと値の数が増え、推論時のメモリ使用量と注意計算が膨らむ。長文専用の注意構造へモデルを変更する方式は再事前学習や追加の位置埋め込み学習を要する場合がある。

- **2023-04 · [Scaling Transformer to 1M tokens and beyond with RMT](2023-2304.11062-scaling-transformer-to-1m-tokens-and-beyond-with-rmt.md)**  
  実装：[✓](https://github.com/booydar/t5-experiments/tree/aaai24) ・ リポジトリ内被引用：9  
  再帰メモリトランスフォーマー（Recurrent メモリ Transformer; RMT）は、長い入力を固定長の区間に分け、直前の区間から受け取った少数のメモリトークンを次の区間に引き渡す方式である。自然言語の実験は、主に履歴区間の追加によってパープレキシティ（perplexity、正解系列の予測の難しさを表す指標）が改善するかを測っている。

- **2023-05 · [Memory-Efficient Fine-Tuning of Compressed Large Language Models via sub-4-bit Integer Quantization](2023-2305.14152-memory-efficient-fine-tuning-of-compressed-large-language-models-via-sub.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  提案するPEQA（パラメータ-Efficient and 量子化-aware Adaptation）は、事前学習済みの重みを3～4ビットなどの整数表現へ量子化した後、整数値を凍結し、量子化尺度だけを学習する。

- **2023-10 · [Sparse Universal Transformer](2023-2310.07096-sparse-universal-transformer.md)**  
  実装：[✓](https://github.com/shawntan/SUT) ・ リポジトリ内被引用：7  
  Sparse Universal Transformer（SUT）は、同じTransformerブロックを複数回反復するユニバーサルTransformer（Universal Transformer; UT）の長所を残しながら、反復計算を疎な専門家選択と動的停止で削減するモデルである。通常のTransformerは各層に別の重みを持つ。

- **2023-10 · [Adaptive Gating in Mixture-of-Experts based Language Models](2023-2310.07188-adaptive-gating-in-mixture-of-experts-based-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  混合専門家モデル（Mixture of エキスパート、MoE）では、各トークンをルータが選んだ少数の専門家に渡し、専門家の出力を統合する。BERT、FSMT、BART、GPT-2、DialoGPTを使う6課題の比較では、固定top-2学習と比べて学習時間を短縮し、推論時の品質は概ね維持した。

- **2023-05 · [Tabi: An Efficient Multi-Level Inference System for Large Language Models](2023-1685e89adb79-tabi-an-efficient-multi-level-inference-system-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  Tabiは、文章分類や回帰の要求をすべて同じ大型モデルへ送る既存推論サービスの過剰計算を減らすため、要求ごとに必要なモデル容量を動的に決める方式である。

- **2023-05 · [LoRAPrune: Structured Pruning Meets Low-Rank Parameter-Efficient Fine-Tuning](2023-2305.18403-loraprune-structured-pruning-meets-low-rank-parameter-efficient-fine-tun.md)**  
  実装：[✓](https://github.com/aim-uofa/LoRAPrune) ・ リポジトリ内被引用：7  
  LoRAPruneは、事前学習済み大規模言語モデルを配備しやすい小型の密モデルへ変えるために、低ランク適応（Low-Rank Adaptation、LoRA）と構造化枝刈り（structured 枝刈り）を一体化する方式である。

- **2023-10 · [RECOMP: Improving Retrieval-Augmented LMs with Compression and Selective Augmentation](2023-2310.04408-recomp-improving-retrieval-augmented-lms-with-compression-and-selective-.md)**  
  実装：[✓](https://github.com/carriex/recomp) ・ リポジトリ内被引用：6  
  Xu、Shi、ChoiによるRECOMPは、検索拡張言語モデル（Retrieval-Augmented Language モデル、RALM）の推論時に、検索した文書をそのままモデルの文脈へ連結する方式を改める。原著は文脈トークン数を主要な効率指標とするため、文書量が5%になったという数値をGPU実行時間が20倍速くなったと読み替えてはならない。

- **2023-02 · [With Shared Microexponents, A Little Shifting Goes a Long Way](2023-2302.08007-with-shared-microexponents-a-little-shifting-goes-a-long-way.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  Rouhaniらは、ブロックデータ表現（Block Data Representation; BDR）という共通の設計枠を用意し、ブロックサイズ、尺度の階層、尺度を保存するビット数、各要素の仮数幅を変えて比較した。

- **2023-10 · [MatFormer: Nested Transformer for Elastic Inference](2023-2310.07707-matformer-nested-transformer-for-elastic-inference.md)**  
  実装：[✓](https://github.com/devvrit/matformer) ・ リポジトリ内被引用：5  
  大規模言語モデルを配備する際、同じ品質・遅延・計算資源の要求を持つ利用者ばかりとは限らない。モデルを後から枝刈りして調整する方法では、新しいサイズごとに再学習や調整を要することもある。

- **2023-10 · [Compressing LLMs: The Truth is Rarely Pure and Never Simple](2023-2310.01382-compressing-llms-the-truth-is-rarely-pure-and-never-simple.md)**  
  実装：[✓](https://github.com/VITA-Group/llm-kick) ・ リポジトリ内被引用：5  
  困惑度（perplexity）がほぼ維持されても、圧縮モデルの事実知識や指示追従は失われ得る。知識をモデル内部から答える課題と、外部文脈を与える検索・要約を分けて評価することで、枝刈りと量子化の能力別の弱点を可視化する。

- **2023-10 · [GEMINI: Fast Failure Recovery in Distributed Training with In-Memory Checkpoints](2023-075d73797107-gemini-fast-failure-recovery-in-distributed-training-with-in-memory-chec.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  保存頻度を増やせば故障前に失う学習進捗は減るが、遠隔ストレージの集約帯域が不足すると保存そのものが長くなり、学習を妨げる。提案は単なる「メモリへ保存する」という発想ではない。

- **2023-09 · [Transformer-VQ: Linear-Time Transformers via Vector Quantization](2023-2309.16354-transformer-vq-linear-time-transformers-via-vector-quantization.md)**  
  実装：[✓](https://github.com/transformer-vq/transformer_vq) ・ リポジトリ内被引用：4  
  基本の着想は、過去の鍵ベクトルを学習可能なコードブックの少数の代表ベクトルへ量子化すると、異なるトークン位置でも同じコードを持つ鍵は同じ注意得点になる、という性質にある。TPU v3での訓練処理率は同規模の二次注意モデルと比べ、系列長8192で3倍超、32768で12倍超となり、131072トークンまで大きな処理率低下なく動作した。

- **2022-11 · [Iron: Private Inference on Transformers](2022-0ed2662d9eee-iron-private-inference-on-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  この構成では、サーバーは入力内容を読めるため、医療文書や企業機密をそのまま送信したくない利用者には問題がある。Ironはこの二つの律速点に特化した手順を設計する。従来の行列・ベクトル積を行ごとに繰り返す方式と比較し、一般の行列形状で出力行数の平方根程度の通信削減を理論的に示す。

- **2023-10 · [Look-Up mAI GeMM: Increasing AI GeMMs Performance by Nearly 2.5x via msGeMM](2023-2310.06178-look-up-mai-gemm-increasing-ai-gemms-performance-by-nearly-2-5x-via-msge.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  重みを4ビット整数へ量子化すれば、各重みが取れる値は16種類に限られる。約2.5倍という代表値を、現在のGPUにおける推論遅延やトークン生成速度の改善と解釈してはならない。

- **2023-10 · [Compresso: Structured Pruning with Collaborative Prompting Learns Compact Large Language Models](2023-2310.05015-compresso-structured-pruning-with-collaborative-prompting-learns-compact.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Compressoは、大規模言語モデルの注意ヘッド、中間層のチャネル、隠れ次元をまとめて削除する構造化枝刈りの手法である。評価の中心はモデル規模と正答率であり、実機のトークン毎秒や消費電力の改善倍率は示されていない。

- **2023-10 · [A Dynamic LLM-Powered Agent Network for Task-Oriented Agent Collaboration](2023-2310.02170-a-dynamic-llm-powered-agent-network-for-task-oriented-agent-collaboratio.md)**  
  実装：[✓](https://github.com/SALT-NLP/DyLAN) ・ リポジトリ内被引用：2  
  複数の大規模言語モデルエージェントを協調させる方式では、担当する役割や通信順序を固定すると、問題によっては不得意なエージェントの発言が増え、余計なモデル呼出しと品質低下を招く。原著のHumanEvalコード生成評価では、単一実行の正答率73.2%に対してDyLANは82.9%、平均モデルAPI呼出し数は16.85回だった。

- **2023-09 · [Pruning Large Language Models via Accuracy Predictor](2023-2309.09507-pruning-large-language-models-via-accuracy-predictor.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  大規模言語モデルの枝刈りを「どの重みを削るか」だけでなく「どの層を何割削るか」という探索問題として扱い、少数の実測品質から決定木型予測器を学習する。推論速度の測定ではなく、圧縮率とタスク品質の交換条件を改善する研究である。

- **2023-06 · [Block-State Transformers](2023-2306.09539-block-state-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  GPUで測った層単体の順方向計算は、ブロック再帰方式に対して単一頭BSTが6〜11倍速い。

- **2023-06 · [Augmenting Language Models with Long-Term Memory](2023-2306.07174-augmenting-language-models-with-long-term-memory.md)**  
  実装：[✓](https://github.com/Victorwz/LongMem) ・ リポジトリ内被引用：2  
  過去のキー・値（KV）を外部バンクへ保持して必要な箇所だけ取り出す方式は有望だが、モデルを学習しながら記憶を書き込むと、古いモデルが生成した記憶表現と現在のモデルの表現が食い違う問題が生じる。

- **2023-10 · [Dual Grained Quantization: Efficient Fine-Grained Quantization for LLM](2023-2310.04836-dual-grained-quantization-efficient-fine-grained-quantization-for-llm.md)**  
  実装：[✓](https://github.com/ilur98/DGQ) ・ リポジトリ内被引用：1  
  しかし、重みを小さなグループ単位で4ビット量子化すると、グループごとに尺度が異なるため、整数の行列積を区切って浮動小数点で部分和を結合する必要が生じる。原著はLLaMA、LLaMA 2、OPTなどで困惑度とゼロショット推論精度を評価し、単一A100 80GBでの実行時間・メモリ使用量を測定した。

- **2023-07 · [PUMA: Secure Inference of LLaMA-7B in Five Minutes](2023-2307.12533-puma-secure-inference-of-llama-7b-in-five-minutes.md)**  
  実装：[✓](https://github.com/secretflow/spu/tree/main/examples/python/ml/flax_llama7b) ・ リポジトリ内被引用：1  
  従来の高速化方式が必要としたモデルの再学習や構造変更を避け、既存の学習済み重みをほぼそのまま秘密計算へ持ち込むことを狙う。

- **2023-07 · [Beyond Classical Attention: Quantum Attention for Scalable Computation](2023-2307.08045-beyond-classical-attention-quantum-attention-for-scalable-computation.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文は、長い入力系列に対する自己注意で全ての問い合わせと鍵の内積を計算する代わりに、閾値を超える少数の大きな内積だけを量子探索で発見する理論的な方法を提案する。

- **2023-07 · [A Survey of Techniques for Optimizing Transformer Inference](2023-2307.07982-a-survey-of-techniques-for-optimizing-transformer-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、Transformer推論を軽量化・高速化する手法を、モデルを作り直す方法から演算器の設計まで横断的に整理した43ページの文献調査である。例えばCoFiは引用元研究で約95%の疎性と約10倍の高速化を報告し、HMC-TranはV100のテンソルコアを利用するBERT-baseの92%疎性で3.68倍を報告する。

- **2023-02 · [SpikeGPT: Generative Pre-trained Language Model with Spiking Neural Networks](2023-2302.13939-spikegpt-generative-pre-trained-language-model-with-spiking-neural-netwo.md)**  
  実装：[✓](https://github.com/ridgerchu/SpikeGPT) ・ リポジトリ内被引用：0  
  従来のスパイク型ネットワークは画像分類などでは有効だったが、語彙数が大きく長距離依存を必要とする言語生成では、二値活性による情報の欠落と訓練の不安定性が課題だった。SpikeGPTは再帰的な言語モデルRWKVのトークン混合をスパイク型ニューロンと組み合わせ、時系列の情報を内部状態へ蓄積することで、二値発火を用いながら自己回帰的な文章生成を行う。

### 5年前（2021-11〜2022-10）

- **2022-05 · [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](2022-2205.14135-flashattention.md)**  
  実装：[✓](https://github.com/HazyResearch/flash-attention) ・ リポジトリ内被引用：433  
  タイル化、オンラインsoftmax、逆伝播時再計算により二次元注意行列の高帯域メモリ往復を避ける厳密注意カーネル。

- **2022-06 · [DeepSpeed Inference: Enabling Efficient Inference of Transformer Models at Unprecedented Scale](2022-2207.00032-deepspeed-inference-enabling-efficient-inference-of-transformer-models-at-unprecedented-scale.md)**  
  実装：[✓](https://github.com/microsoft/DeepSpeed) ・ リポジトリ内被引用：117  
  単一の量子化方式や一種類の並列化を万能解とせず、GPU内実行向けのDeepSpeed Transformerと、CPU主記憶・NVMeを使うZeRO-Inferenceという二つの経路を組み合わせる。

- **2022-06 · [ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers](2022-2206.01861-zeroquant-efficient-and-affordable-post-training-quantization-for-large-.md)**  
  実装：[✓](https://github.com/microsoft/DeepSpeed) ・ リポジトリ内被引用：88  
  大規模言語モデルの量子化では、重みを16ビットから8ビットへ減らすだけでメモリ転送量は小さくなる。INT8では追加の学習や校正なしでBERT・GPT系の品質をほぼ保ち、NVIDIA A100上のBERT-baseで最大5.19倍、GPT-3 350Mで4.16倍の速度向上を示した。

- **2022-02 · [ST-MoE: Designing Stable and Transferable Sparse Expert Models](2022-2202.08906-st-moe-designing-stable-and-transferable-sparse-expert-models.md)**  
  実装：[✓](https://github.com/tensorflow/mesh/blob/master/mesh_tensorflow/transformer/moe.py) ・ リポジトリ内被引用：60  
  ST-MoEは専門家混合（Mixture-of-Experts、MoE）モデルを単に巨大化するのではなく、学習の発散を防ぎ、下流の多様な自然言語課題で密モデルを上回るための設計を検討する研究である。ただしこれはモデル全体をGPUメモリ12GBで動かせるという意味ではなく、専門家の重み配置と分散通信を含めた大規模学習システムの研究である。

- **2021-12 · [GLaM: Efficient Scaling of Language Models with Mixture-of-Experts](2021-2112.06905-glam-efficient-scaling-of-language-models-with-mixture-of-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：56  
  総パラメータ数と一トークンで実際に使用するパラメータ数を分離することで、巨大な容量を持ちながら密なモデルほどの計算を必要としない。最大構成GLaM（64B/64E）は総1.2兆パラメータを持つが、トークン当たり活性化するのは約96.6B、全体の約8%である。

- **2021-12 · [Self-attention Does Not Need O(n^2) Memory](2021-2112.05682-self-attention-does-not-need-o-n-2-memory.md)**  
  実装：[✓](https://github.com/google-research/google-research/tree/master/memory_efficient_attention) ・ リポジトリ内被引用：23  
  ソフトマックス注意の最大値、指数和、値の重み付き和を逐次更新し、全注意行列を実体化せず同じ数学的出力を得る。理論上の省メモリ算法と、TPU向けのチャンク並列実装、再計算を使った微分を示す。

- **2022-02 · [Transformer Quality in Linear Time](2022-2202.10447-transformer-quality-in-linear-time.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  FLASHは、注意計算を系列長に対して線形に近づける方式が、理論計算量を減らしても実機で速くならず、強いTransformerを比較対象にすると品質が落ちるという問題に取り組む。

- **2022-06 · [Long Range Language Modeling via Gated State Spaces](2022-2206.13947-long-range-language-modeling-via-gated-state-spaces.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  対象：自己回帰言語モデルの状態空間層をTPUで効率よく学習し、学習系列長を超える長距離依存を扱う研究。学習速度と推論速度の主張を分けて読む。一次論文は2022年7月2日改訂の第3版。

- **2022-04 · [Structured Pruning Learns Compact and Accurate Models](2022-2204.00408-structured-pruning-learns-compact-and-accurate-models.md)**  
  実装：[✓](https://github.com/princeton-nlp/CoFiPruning) ・ リポジトリ内被引用：13  
  一方、あらかじめ小型の学生モデルを定めて知識蒸留する方式は、推論しやすい構造を得られるが、大量の未ラベル文章で一般蒸留を行う費用が大きい。MNLIの約95%剪定条件ではBERT-base比12.1倍の推論高速化と精度80.6を報告し、QNLIでも12.1倍・86.1を報告する。

- **2021-12 · [LongT5: Efficient Text-To-Text Transformer for Long Sequences](2021-2112.07916-longt5-efficient-text-to-text-transformer-for-long-sequences.md)**  
  実装：[✓](https://github.com/google-research/longt5) ・ リポジトリ内被引用：12  
  T5のエンコーダを長文向けに置き換え、各層でブロック集約した大域トークンを一時的に作る注意機構を提案する。重要文生成による事前学習と組み合わせ、要約・質問応答で長い入力の情報を利用する。論文の主な評価はモデル品質と学習時の計算費用であり、デコード専用の推論サービング実験とは区別する。

- **2022-02 · [cosFormer: Rethinking Softmax in Attention](2022-2202.08791-cosformer-rethinking-softmax-in-attention.md)**  
  実装：[✓](https://github.com/OpenNLPLab/cosFormer) ・ リポジトリ内被引用：11  
  cosFormerはソフトマックスの関数形をそのまま近似するのでなく、注意係数が非負であることと、関連性の高い位置へ重みを集中させることを抽出して設計する。

- **2022-04 · [A Fast Post-Training Pruning Framework for Transformers](2022-2204.09656-a-fast-post-training-pruning-framework-for-transformers.md)**  
  実装：[✓](https://github.com/WoosukKwon/retraining-free-pruning) ・ リポジトリ内被引用：9  
  Transformerの計算量と推論遅延を減らすために、不要な注意頭や順伝播層のフィルタを削る構造化枝刈りが使われる。品質低下を1%以内に抑えながら、BERT Baseでは元の演算量の60〜70%程度まで、DistilBERTでは条件により50%まで減らした。

- **2022-07 · [FNet: Mixing Tokens with Fourier Transforms](2022-2105.03824-fnet-mixing-tokens-with-fourier-transforms.md)**  
  実装：[✓](https://github.com/google-research/google-research/tree/master/f_net) ・ リポジトリ内被引用：7  
  標準的な変換器（Transformer）の自己注意（self-注意機構）は、入力系列内のトークン間の重みを入力内容に応じて計算する。特にこの論文の「学習80%高速化」は約1.8倍の処理速度を意味し、処理時間が80%減ったという意味ではない。

- **2022-08 · [Learned Token Pruning for Transformers](2022-2107.00910-learned-token-pruning-for-transformers.md)**  
  実装：[✓](https://github.com/kssteven418/LTP) ・ リポジトリ内被引用：5  
  この論文の対象は、入力文の全トークンを全Transformer層で処理するために生じる推論計算量である。一次資料としてKDD 2022の原論文に加え、筆頭著者が2023年に公表した同方式の31ページの学位論文（UC Berkeley EECS-2023-119）の方法・評価・議論を参照した。

- **2021-11 · [Memory-efficient Transformers via Top-k Attention](2021-c7730f7e7292-memory-efficient-transformers-via-top-k-attention.md)**  
  実装：[✓](https://github.com/ag1988/top_k_attention) ・ リポジトリ内被引用：3  
  既存の効率的注意には、ハッシュや局所窓で計算する組合せを制限する方式と、注意関数自体を近似する線形注意がある。

- **2022-08 · [Unified Normalization for Accelerating and Stabilizing Transformers](2022-2208.01313-unified-normalization-for-accelerating-and-stabilizing-transformers.md)**  
  実装：[✓](https://github.com/hikvision-research/Unified-Normalization) ・ リポジトリ内被引用：2  
  UNはTransformerのoffline normalizationを、活性値/勾配統計の平滑化と適応型 outlier除去で安定化し、固定統計を線形層へ融合してSwin-Tで31.2% スループット向上を示す。

- **2022-02 · [Competition-Level Code Generation with AlphaCode](2022-2203.07814-competition-level-code-generation-with-alphacode.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  AlphaCodeは、自然言語で与えられた競技プログラミング問題から、正しい実行プログラムを見つけるための生成・探索・選別システムである。評価では2021年12月のCodeforcesの10大会を後から模擬し、各問題最大10提出という条件で、参加者中の順位が平均して上位54.3%に相当した。

- **2022-03 · [Transformer Feed-Forward Layers Build Predictions by Promoting Concepts in the Vocabulary Space](2022-2203.14680-transformer-feed-forward-layers-build-predictions-by-promoting-concepts-.md)**  
  実装：[✓](https://github.com/aviclu/ffn-values) ・ リポジトリ内被引用：1  
  Transformerの順伝播層（feed-順伝播 network、FFN）は、自己注意層で得た表現を更新するが、どのような内部操作が次トークンの予測を形作るかは分かりにくい。本論文は、FFNが出力するベクトルを、個々の値ベクトルに入力依存の係数を掛けた小さな加算成分の和として分解し、各成分が語彙中のどのトークンを押し上げるかを調べる。

- **2022-02 · [Flowformer: Linearizing Transformers with Conservation Flows](2022-2202.06258-flowformer-linearizing-transformers-with-conservation-flows.md)**  
  実装：[✓](https://github.com/thuml/Flowformer) ・ リポジトリ内被引用：0  
  Flowformerは、自己注意（Self-注意機構）の計算量を系列長に対して線形に抑えつつ、通常のsoftmax注意が持つ「重要な位置を選んで重みを集中させる」性質を残そうとする研究である。

### 6年前（2020-11〜2021-10）

- **2021-01 · [I-BERT: Integer-only BERT Quantization](2021-2101.01321-i-bert-integer-only-bert-quantization.md)**  
  実装：[✓](https://github.com/kssteven418/i-bert) ・ リポジトリ内被引用：25  
  Transformerの重みと行列積を8ビット整数へ量子化しても、推論全体が整数だけで実行できるとは限らない。Tesla T4上の予備的な整数カーネル実装では、FP32比で2.4～4.0倍の推論高速化を報告する。

- **2021-04 · [Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM](2021-2104.04473-efficient-large-scale-language-model-training-on-gpu-clusters-using-mega.md)**  
  実装：[✓](https://github.com/NVIDIA/Megatron-LM) ・ リポジトリ内被引用：23  
  本論文は、巨大言語モデルの学習を数千基のGPUへ拡張するとき、メモリ容量、層内の集合通信、パイプラインの空泡、ノード間転送の重複が性能を制限する問題を扱う。パイプラインでは前向きと後向きを交互に処理する1F1Bを使い、さらに一つのGPUに複数の離れたモデル片を割り当てて空泡を短くする。

- **2021-09 · [Block Pruning For Faster Transformers](2021-2109.04838-block-pruning-for-faster-transformers.md)**  
  実装：[✓](https://github.com/huggingface/nn_pruning) ・ リポジトリ内被引用：17  
  Block Pruningは移動量に基づく枝刈り（movement 枝刈り）を重みブロック単位へ拡張し、フィードフォワード層の次元や注意ヘッドを構造的に除去できる形へ誘導する。

- **2021-02 · [Nyströmformer: A Nyström-Based Algorithm for Approximating Self-Attention](2021-2102.03902-nystr-mformer-a-nystr-m-based-algorithm-for-approximating-self-attention.md)**  
  実装：[✓](https://github.com/mlpen/Nystromformer) ・ リポジトリ内被引用：16  
  標準的な自己注意（self-注意機構）は、系列長nのすべてのトークン対の類似度を計算するため、n×nの注意行列を作る。系列が2倍になると注意行列の要素数は4倍となり、長い文書を扱うTransformerでは計算量とメモリ容量が問題になる。

- **2020-12 · [Fast Transformers with Clustered Attention](2020-2007.04825-fast-transformers-with-clustered-attention.md)**  
  実装：[✓](https://github.com/idiap/fast-transformers) ・ リポジトリ内被引用：11  
  本論文は、自己注意（self-注意機構）の各クエリがすべてのキーを参照するため、系列長Nに対して注意行列がN×Nになり、計算量と中間メモリが二乗で増える問題を扱う。NeurIPS 2020の正式版では、GTX 1080 Ti 11GB上の音声認識2データセットと、学習済みRoBERTaのGLUE・SQuADへの適用を評価した。

- **2021-10 · [8-bit Optimizers via Block-wise Quantization](2021-2110.02861-8-bit-optimizers-via-block-wise-quantization.md)**  
  実装：[✓](https://github.com/bitsandbytes-foundation/bitsandbytes) ・ リポジトリ内被引用：9  
  Dettmersらは、この状態を8ビットへ縮めても32ビット版に近い学習品質を維持する方式を提案した。原著表1では1.5Bパラメータ言語モデルで32ビットAdamと8ビットAdamの困惑度がともに9.0で、後者は8.5GBのGPUメモリを節約した。

- **2020-12 · [MiniLMv2: Multi-Head Self-Attention Relation Distillation for Compressing Pretrained Transformers](2020-2012.15828-minilmv2-multi-head-self-attention-relation-distillation-for-compressing.md)**  
  実装：[✓](https://github.com/microsoft/unilm/tree/master/minilm) ・ リポジトリ内被引用：9  
  教師と生徒の注意頭数を揃える制約を外し、Query・Key・Valueのトークン間関係を共通の「関係頭」で比較する。推論速度の改善は蒸留後の小型モデルによるもので、実行時に教師を参照する方式ではない。

- **2020-11 · [EdgeBERT: Sentence-Level Energy Optimizations for Latency-Aware Multi-Task NLP Inference](2020-2011.14203-edgebert-sentence-level-energy-optimizations-for-latency-aware-multi-tas.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  EdgeBERTは、資源制約の厳しい端末上で、自然言語分類を決められた応答時間内に実行しながら消費エネルギーを最小化するための、アルゴリズムと回路の共同設計である。これらは別々の比較であり、同一実行条件の速度改善倍率でも、LLMのトークン生成性能でもない（原著要旨、§8.2）。

- **2021-04 · [BERxiT: Early Exiting for BERT with Better Fine-Tuning and Extension to Regression](2021-3c0f54f14532-berxit-early-exiting-for-bert-with-better-fine-tuning-and-extension-to-r.md)**  
  実装：[✓](https://github.com/castorini/berxit) ・ リポジトリ内被引用：5  
  従来の早期終了では、最後の層で良い予測を得ることと、中間層でも十分に良い予測を得ることの学習目標が競合しやすい。BERxiTはこの二つを別々の機構で解決する。例えばBERTBASEのSST-2試験集合では、交互微調整によって元モデルの得点の98%を保ちながら実行層数を65%減らす条件があり、より強い早期終了では96%の得点に対して79%の層削減を得る。

- **2020-12 · [CascadeBERT: Accelerating Inference of Pre-trained Language Models via Calibrated Complete Models Cascade](2020-2012.14682-cascadebert-accelerating-inference-of-pre-trained-language-models-via-ca.md)**  
  実装：[✓](https://github.com/lancopku/CascadeBERT) ・ リポジトリ内被引用：5  
  提案するCascadeBERTは、単一モデルの途中で終了する代わりに、小型でも事前学習を完了した独立モデルを最初に走らせる。6つのGLUE分類課題で、BERT-baseを基準に実行層数を約4分の1へ減らす条件では、論文の課題平均はCascadeBERTが78.3、動的早期終了DeeBERTが67.8であり、差は10.5点、相対的には約15.5%である。

- **2021-06 · [TR-BERT: Dynamic Token Reduction for Accelerating BERT Inference](2021-00c8b8f9f90e-tr-bert-dynamic-token-reduction-for-accelerating-bert-inference.md)**  
  実装：[✓](https://github.com/thunlp/TR-BERT) ・ リポジトリ内被引用：4  
  選択しなかったトークンの表現はその層で凍結し、最終予測時には終了時の表現を回収する。表2の代表条件では、SQuAD 2.0でBERTのF1 77.12に対しTR-BERT12は75.66、演算回数の比で2.08倍の削減である。

- **2021-06 · [LightSeq: A High Performance Inference Library for Transformers](2021-439132b7c6e4-lightseq-a-high-performance-inference-library-for-transformers.md)**  
  実装：[✓](https://github.com/bytedance/lightseq) ・ リポジトリ内被引用：3  
  一方、推論の律速が行列積そのものではなく周辺処理へ移るというシステム上の問題を、具体的なカーネル構成と実測で説明した基礎的な実装研究である。

- **2021-03 · [Softermax: Hardware/Software Co-Design of an Efficient Softmax for Transformers](2021-2103.09301-softermax-hardware-software-co-design-of-an-efficient-softmax-for-transf.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  Transformerの自己注意機構では、クエリとキーの積から得た各スコアをsoftmaxで正規化し、値ベクトルへの重みを生成する。原著のTSMC 7nm設計評価では、非正規化部の面積0.25倍・エネルギー0.10倍、正規化部の面積0.65倍・エネルギー0.39倍、MAC等を含む演算器全体の面積0.90倍・エネルギー0.43倍を報告する。

- **2021-02 · [Accelerated Sparse Neural Training: A Provable and Efficient Method to Find N:M Transposable Masks](2021-2102.08124-accelerated-sparse-neural-training-a-provable-and-efficient-method-to-fi.md)**  
  実装：[✓](https://github.com/papers-submission/structured_transposable_masks) ・ リポジトリ内被引用：3  
  本研究は、この非対称性を解消する転置可能細粒度疎マスク（transposable fine-grained sparsity mask）を提案する。論文が示す「2倍」は主として疎テンソルコアの適用可能な行列積の範囲の比較であり、全学習時間の2倍高速化を実測したものと読み替えない。

- **2021-05 · [Poolingformer: Long Document Modeling with Pooling Attention](2021-2105.04371-poolingformer-long-document-modeling-with-pooling-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、長文を処理する変換器（Transformer）の自己注意を、近い単語を精密に参照する第一段と、遠い単語を圧縮して参照する第二段に分ける「Poolingformer」を提案する。

### 7年前（2019-11〜2020-10）

- **2020-01 · [Reformer: The Efficient Transformer](2020-2001.04451-reformer-the-efficient-transformer.md)**  
  実装：[✓](https://github.com/google/trax/tree/master/trax/models/reformer) ・ リポジトリ内被引用：108  
  第一の制約は、全トークン対の内積を求める標準自己注意が系列長の二乗に比例する計算を要することである。

- **2020-09 · [Rethinking Attention with Performers](2020-2009.14794-rethinking-attention-with-performers.md)**  
  実装：[✓](https://github.com/google-research/google-research/tree/master/performer) ・ リポジトリ内被引用：86  
  Performerは、通常の全ランクのソフトマックス注意を正の直交ランダム特徴で近似するFAVOR+を提案し、注意行列を明示的に保持しない線形時間・線形空間の実行を可能にする。

- **2020-04 · [DeeBERT: Dynamic Early Exiting for Accelerating BERT Inference](2020-2004.12993-deebert-dynamic-early-exiting-for-accelerating-bert-inference.md)**  
  実装：[✓](https://github.com/castorini/DeeBERT) ・ リポジトリ内被引用：27  
  DeeBERTは、BERT系の分類モデルで入力ごとに必要なTransformer層数が異なることを利用し、浅い層ですでに十分確信度の高い予測が得られた例を途中で返す動的早期終了（動的 early exiting）方式である。

- **2020-05 · [GOBO: Quantizing Attention-Based NLP Models for Low Latency and Energy Efficient Inference](2020-2005.03842-gobo-quantizing-attention-based-nlp-models-for-low-latency-and-energy-ef.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  GOBOは、BERTなどの注意機構を使う自然言語処理モデルの重みを、学習後に大幅に圧縮する手法である。重みの約99.9%を少数の代表値への索引で表し、残る約0.1%の外れ値だけを元の32ビット浮動小数点のまま保持する。

- **2019-11 · [Blockwise Self-Attention for Long Document Understanding](2019-1911.02972-blockwise-self-attention-for-long-document-understanding.md)**  
  実装：[✓](https://github.com/xptree/BlockBERT) ・ リポジトリ内被引用：22  
  BlockBERTは、長い文書をBERT型の双方向符号化器へ入力するとき、通常の自己注意が系列長の二乗に比例する注意得点を作る問題を、ブロック単位で規則的に疎化した注意によって緩和する。単に遠方のトークンを切り捨てるのではなく、各注意ヘッドへ異なるブロック置換を割り当てることで、近傍情報を読むヘッドと離れたブロックを読むヘッドを共存させる。

- **2020-09 · [TernaryBERT: Distillation-aware Ultra-low Bit BERT](2020-2009.12812-ternarybert-distillation-aware-ultra-low-bit-bert.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  TernaryBERTは、自然言語理解向けのBERTを極低ビットで実行可能な重み表現へ圧縮し、精度低下を知識蒸留（Knowledge Distillation）で抑える手法である。これにより重み2ビット・埋め込み2ビット・活性値8ビットの代表構成で、BERTの保存サイズを418MBから28MBへ減らす。

- **2020-04 · [FastBERT: a Self-distilling BERT with Adaptive Inference Time](2020-2004.02178-fastbert-a-self-distilling-bert-with-adaptive-inference-time.md)**  
  実装：[✓](https://github.com/autoliuweijie/FastBERT) ・ リポジトリ内被引用：20  
  この設計は文章生成の各トークンを省略する方式ではなく、主に文章分類と文対照合に適用される。例えば中国語THUCNewsでは閾値0.1で分類精度96.71%を維持しつつ計算量が約6.05分の1、英語DBpediaでは同閾値で99.31%から99.28%への微小な低下と引き換えに約10.57分の1となる。

- **2020-06 · [BERT Loses Patience: Fast and Robust Inference with Early Exit](2020-2006.04152-bert-loses-patience-fast-and-robust-inference-with-early-exit.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  浅い層で正しい分類がほぼ確定している入力にも後段層の計算を続けるため、不要な遅延が生じる。従来の早期終了方式は中間分類器の最大確率やエントロピーなど、一つの層での自信の強さを停止信号にすることが多かった。

- **2020-04 · [Training with Quantization Noise for Extreme Model Compression](2020-2004.07320-training-with-quantization-noise-for-extreme-model-compression.md)**  
  実装：[✓](https://github.com/pytorch/fairseq/tree/master/examples/quant_noise) ・ リポジトリ内被引用：18  
  学習済みモデルの重みを低ビットや積量子化で保存すると、推論時の重み容量を減らせるが、各層で生じた量子化誤差が次層の入力へ蓄積し、精度が急激に落ちることがある。ICLR 2021の原著では、16層Transformerの942MBを反復積量子化で38MBへ圧縮した場合、量子化雑音なしのテスト困惑度25.2に対して20.7へ改善した。

- **2020-02 · [Compressing BERT: Studying the Effects of Weight Pruning on Transfer Learning](2020-2002.08307-compressing-bert-studying-the-effects-of-weight-pruning-on-transfer-lear.md)**  
  実装：[✓](https://github.com/mitchellgordon95/bert-prune) ・ リポジトリ内被引用：10  
  対象はBERT-Baseの非構造化重み枝刈りである。主結果は、30～40%程度の重みを削除しても下流性能がほぼ変わらない一方、40～60%では事前学習で獲得した情報の消失が、70%以上ではそれに加えて残存ネットワークの表現容量制約が効くという三つの領域である。

- **2020-07 · [HAT: Hardware-Aware Transformers for Efficient Natural Language Processing](2020-2005.14187-hat-hardware-aware-transformers-for-efficient-natural-language-processin.md)**  
  実装：[✓](https://github.com/mit-han-lab/hardware-aware-transformers) ・ リポジトリ内被引用：8  
  Transformerの推論速度を改善するため、パラメータ数や浮動小数点演算回数（FLOPs）を減らすことは一般的だが、演算量が同じモデルでも機器によって実測遅延は大きく異なる。HAT（Hardware-Aware Transformers）はこの差を設計時に扱う。

- **2020-04 · [On the Effect of Dropping Layers of Pre-trained Transformer Models](2020-2004.03844-on-the-effect-of-dropping-layers-of-pre-trained-transformer-models.md)**  
  実装：[✓](https://github.com/hsajjad/transformers/) ・ リポジトリ内被引用：8  
  事前学習済みBERT系モデルの上位層を削除して推論時間を約半減し、モデル・タスクごとの精度低下と下位層の重要性を比較した構造的圧縮研究。

- **2020-04 · [Lite Transformer with Long-Short Range Attention](2020-2004.11886-lite-transformer-with-long-short-range-attention.md)**  
  実装：[✓](https://github.com/mit-han-lab/lite-transformer) ・ リポジトリ内被引用：7  
  Lite Transformerは、短い文章を処理する翻訳・要約・言語モデルを、限られた計算予算の端末で実行するためのモデル構造を提案したICLR 2020論文である。

- **2020-07 · [FTRANS: Energy-Efficient Acceleration of Transformers using FPGA](2020-2007.08563-ftrans-energy-efficient-acceleration-of-transformers-using-fpga.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  FTRANSは、Transformerの重み行列を拡張ブロック循環行列（enhanced block-circulant matrix; BCM）に置き換える構造化圧縮と、その圧縮表現を直接計算する再構成可能論理回路（field-programmable gate array; FPGA）の専用構成を同時設計した研究である。

- **2020-02 · [Compressing Large-Scale Transformer-Based Models: A Case Study on BERT](2020-2002.11985-compressing-large-scale-transformer-based-models-a-case-study-on-bert.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  量子化で重みを小さくする方法、不要な重みや構造を削る方法、大きな教師モデルから小さな生徒モデルへ知識を移す方法など、圧縮の選択肢は多い。

- **2020-05 · [IntelliCode Compose: Code Generation using Transformer](2020-2005.08025-intellicode-compose-code-generation-using-transformer.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  IntelliCode Composeは、統合開発環境（IDE）で入力途中のプログラムから一行規模の補完候補を提示するクラウド型のコード生成システムである。ただし編集類似度は84.1%から78.0%へ下がる。

- **2020-01 · [PoWER-BERT: Accelerating BERT Inference via Progressive Word-vector Elimination](2020-2001.08950-power-bert-accelerating-bert-inference-via-progressive-word-vector-elimi.md)**  
  実装：[✓](https://github.com/IBM/PoWER-BERT) ・ リポジトリ内被引用：4  
  方式は二つの判断を分離する。原著のK80 GPU、Keras、バッチ128（RACEのみ32）の評価では、BERTBASE比で各課題2.0～4.5倍の推論時間短縮を報告する。

- **2020-06 · [Multi-Head Attention: Collaborate Instead of Concatenate](2020-2006.16362-multi-head-attention-collaborate-instead-of-concatenate.md)**  
  実装：[✓](https://github.com/epfml/collaborative-attention) ・ リポジトリ内被引用：3  
  標準的な多頭注意（Multi-Head 注意機構、MHA）は、複数の注意ヘッドに独立したクエリ射影とキー射影を与え、それぞれが計算した値を連結して出力する。単層のV100測定では設定次第で推論時間が2.28ミリ秒から1.75ミリ秒へ短縮した。

- **2020-06 · [Dynamic Tensor Rematerialization](2020-2006.09616-dynamic-tensor-rematerialization.md)**  
  実装：[✓](https://github.com/uwsampl/dtr-prototype) ・ リポジトリ内被引用：3  
  活性チェックポイントは一部の活性だけを保存し、捨てた活性を逆伝播の必要時に再計算することで、メモリと演算量を交換する。

- **2020-06 · [Funnel-Transformer: Filtering out Sequential Redundancy for Efficient Language Processing](2020-2006.03236-funnel-transformer-filtering-out-sequential-redundancy-for-efficient-lan.md)**  
  実装：[✓](https://github.com/laiguokun/Funnel-Transformer) ・ リポジトリ内被引用：2  
  Funnel-Transformerは、すべての変換器層で入力トークン数と同じ長さの隠れ状態を維持することが、系列全体を一つの表現へ要約する分類・ランキング課題では冗長であるという着想から生まれた。これにより、出力長は短くしながら圧縮前の情報全体を参照できる。

- **2019-11 · [Mask-Predict: Parallel Decoding of Conditional Masked Language Models](2019-0bc18ef37a7d-mask-predict-parallel-decoding-of-conditional-masked-language-models.md)**  
  実装：[✓](https://github.com/facebookresearch/Mask-Predict) ・ リポジトリ内被引用：2  
  翻訳文全体を毎回捨てる反復改良方式とは異なり、高信頼の語を固定して低信頼位置へ文脈を提供する点が中心的な設計である。

- **2020-08 · [ConvBERT: Improving BERT with Span-based Dynamic Convolution](2020-2008.02496-convbert-improving-bert-with-span-based-dynamic-convolution.md)**  
  実装：[✓](https://github.com/yitu-opensource/ConvBert) ・ リポジトリ内被引用：0  
  BERTの多頭自己注意は、すべてのヘッドで全トークン対の関係を計算する。しかし自然言語では局所的な構文・語彙の結び付きが重要であり、実際に多くのヘッドの注意行列は対角線付近へ集中する。遠方トークンをほとんど参照しないヘッドでも、全系列の二次元注意行列を構築するのは計算上の無駄である。

- **2020-06 · [$O(n)$ Connections are Expressive Enough: Universal Approximability of Sparse Transformers](2020-2006.04862-o-n-connections-are-expressive-enough-universal-approximability-of-spars.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常のTransformerの自己注意は、系列中の各トークンが他の全トークンを参照するため、系列長nに対して注意得点の組合せがnの二乗で増える。長文を処理する際に接続を減らす疎注意は計算量を減らす候補だが、接続を取り除くことでモデルが表現できる関数の種類まで狭まるのかは自明ではない。

### 8年前（2018-11〜2019-10）

- **2019-09 · [Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism](2019-1909.08053-megatron-lm-training-multi-billion-parameter-language-models-using-model.md)**  
  実装：[✓](https://github.com/NVIDIA/Megatron-LM) ・ リポジトリ内被引用：228  
  この論文の対象は、巨大な言語モデルの学習時に、モデル重み・勾配・最適化器状態が単一GPUのメモリに収まらない問題である。従来のモデル全体を別の言語や専用コンパイラで書き直す方法とは異なり、PyTorchの既存Transformer実装へ少数の集約通信を挿入する設計である。

- **2019-04 · [Generating Long Sequences with Sparse Transformers](2019-1904.10509-generating-long-sequences-with-sparse-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：158  
  全結合の自己注意を局所窓と周期・固定要約位置へ因数分解して O(n√n) 化し、再計算と疎GPUカーネルを併用して数万〜100万要素の生成を可能にしたSparse Transformer。

- **2018-11 · [Blockwise Parallel Decoding for Deep Autoregressive Models](2018-1811.03115-blockwise-parallel-decoding-for-deep-autoregressive-models.md)**  
  実装：[✓](https://github.com/tensorflow/tensor2tensor) ・ リポジトリ内被引用：62  
  深層自己回帰モデルの生成では、次のトークンが確定して初めてその次の条件付き分布を計算できる。注意計算を多数の位置で同時実行できる変換器（Transformer）でも、通常の貪欲復号（greedy デコード）は生成長に比例した逐次呼び出しを必要とする。厳密一致を要求する限り、元モデルの貪欲復号と同じ出力を維持できる。

- **2019-05 · [Are Sixteen Heads Really Better than One?](2019-1905.10650-are-sixteen-heads-really-better-than-one.md)**  
  実装：[✓](https://github.com/pmichel31415/are-16-heads-really-better-than-1) ・ リポジトリ内被引用：45  
  Michelらは、学習済みの翻訳用TransformerとBERTの各注意ヘッドを無効化して、品質の変化、ヘッド重要度の推定、構造的な枝刈り後の推論速度を実験した。WMT14英仏翻訳のTransformerでは全ヘッドの約20%、MultiNLIに微調整したBERTでは約40%を重要度順に削っても顕著な品質低下が生じなかった。

- **2019-09 · [Q-BERT: Hessian Based Ultra Low Precision Quantization of BERT](2019-1909.05840-q-bert-hessian-based-ultra-low-precision-quantization-of-bert.md)**  
  実装：✓ ・ リポジトリ内被引用：44  
  Q-BERTは、BERTの各層へ同じビット数を割り当てる均一量子化ではなく、損失関数の二階微分から層ごとの誤差感度を推定し、敏感な層へ高い精度を残す混合精度量子化手法である。論文はSST-2、MNLI、CoNLL-03、SQuADの四課題で、重みの最大13倍圧縮、埋め込みと活性値の最大4倍圧縮を報告し、強圧縮でも性能低下を最大2.3%以内に抑えたと説明する。

- **2019-09 · [Reducing Transformer Depth on Demand with Structured Dropout](2019-1909.11556-reducing-transformer-depth-on-demand-with-structured-dropout.md)**  
  実装：✓ ・ リポジトリ内被引用：41  
  深いTransformerは学習時に層をすべて使用する前提で最適化されるため、学習後に連続した層を削ると、残った層が想定しない中間表現を受け取り品質が悪化する。深度ごとに新しいモデルを一から学習したり知識蒸留を繰り返したりする方法では、必要な配備構成が増えるほど学習費用が増える。深度削減は品質低下を完全に取り除くわけではない。

- **2019-05 · [Analyzing Multi-Head Self-Attention: Specialized Heads Do the Heavy Lifting, the Rest Can Be Pruned](2019-1905.09418-analyzing-multi-head-self-attention-specialized-heads-do-the-heavy-lifti.md)**  
  実装：[✓](https://github.com/lena-voita/the-story-of-heads) ・ リポジトリ内被引用：41  
  本論文は、翻訳用Transformerの多頭注意機構において、各ヘッドの計算が同じだけ必要なのかを、予測への寄与と実際の削除耐性の両側面から調べた研究である。一方、これは2019年の機械翻訳Transformerにおける品質評価であり、現代の生成専用LLMで実際に同じ割合の実行時間や鍵・値キャッシュ容量を削減できると証明した結果ではない。

- **2018-11 · [GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism](2018-1811.06965-gpipe-efficient-training-of-giant-neural-networks-using-pipeline-paralle.md)**  
  実装：[✓](https://github.com/tensorflow/lingvo/blob/master/lingvo/core/gpipe.py) ・ リポジトリ内被引用：35  
  GPipeは、単一のGPUやTPUに収まらないニューラルネットワークを、層の連続区間ごとに複数の装置へ分割して学習する方式である。実際に学習した557百万パラメータのAmoebaNetはImageNet-2012の上位1件正解率84.4%、60億パラメータ・128層の多言語Transformerは102言語対で個別の二言語モデルを上回った。

- **2019-05 · [Adaptive Attention Span in Transformers](2019-1905.07799-adaptive-attention-span-in-transformers.md)**  
  実装：[✓](https://github.com/facebookresearch/adaptive-span) ・ リポジトリ内被引用：24  
  自己回帰型Transformerの注意機構は、過去の一定幅のトークンを参照して次のトークンを予測する。

- **2019-10 · [Q8BERT: Quantized 8Bit BERT](2019-1910.06188-q8bert-quantized-8bit-bert.md)**  
  実装：[✓](https://github.com/NervanaSystems/nlp-architect) ・ リポジトリ内被引用：15  
  Q8BERTは、事前学習済みBERTを特定の自然言語処理課題へ微調整する段階で量子化誤差を模擬し、推論時の8ビット整数演算へ適応させる研究である。著者はBERTの重みの99%以上を占める埋め込み層と全結合層を8ビット整数へ対応させ、残りの数値的に敏感な演算は32ビット浮動小数点に残す。

- **2019-04 · [Mask-Predict: Parallel Decoding of Conditional Masked Language Models](2019-1904.09324-mask-predict-parallel-decoding-of-conditional-masked-language-models.md)**  
  実装：[✓](https://github.com/facebookresearch/Mask-Predict) ・ リポジトリ内被引用：10  
  翻訳文の長さを最初に予測し、最初の反復では全位置を同時に予測する。2019年の機械翻訳実験では、WMT14英語→ドイツ語において基礎CMLMの10反復が27.03 BLEU、同等規模の自己回帰Transformerが27.74 BLEUとなった。

- **2019-07 · [Large Memory Layers with Product Keys](2019-1907.05242-large-memory-layers-with-product-keys.md)**  
  実装：[✓](https://github.com/facebookresearch/XLM) ・ リポジトリ内被引用：4  
  本論文の積キー記憶層（Product Key メモリ; PKM）は、二つの部分キー集合の直積で巨大なキー集合を暗黙的に作り、各部分集合の上位候補だけを調べて全積キー集合に対する正確な上位選択を行う。検索結果に対応する少数の値ベクトルだけを読み出して加重和を計算するため、総パラメータ容量と活性計算量を分離できる。

- **2019-03 · [Supporting Very Large Models using Automatic Dataflow Graph Partitioning](2019-1807.08887-supporting-very-large-models-using-automatic-dataflow-graph-partitioning.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Tofuは、単一のGPUのメモリ容量を超えるニューラルネットワークを、プログラムを書き換えず複数GPUで学習できるようにする自動モデル並列化システムである。

### 9年前（2017-11〜2018-10）

- **2018-06 · [PipeDream: Generalized Pipeline Parallelism for DNN Training](2018-1806.03377-pipedream-generalized-pipeline-parallelism-for-dnn-training.md)**  
  実装：✓ ・ リポジトリ内被引用：55  
  DNNの連続層を複数GPUへ割り当て、異なるミニバッチの順伝播と逆伝播を交互に重ねる。層の計算・通信費用を測って段を自動分割し、順伝播時の重み版を逆伝播まで保持することで非同期実行の整合性を保つ。

- **2018-02 · [Horovod: fast and easy distributed deep learning in TensorFlow](2018-1802.05799-horovod-fast-and-easy-distributed-deep-learning-in-tensorflow.md)**  
  実装：[✓](https://github.com/uber/horovod) ・ リポジトリ内被引用：13  
  GPU数を増やすと勾配転送と集約のために通信が集中し、著者らの128 GPU試験では、計算資源のほぼ半分を効率的に使えていなかった。提案の価値は通信アルゴリズムだけではない。

- **2018-02 · [Deterministic Non-Autoregressive Neural Sequence Modeling by Iterative Refinement](2018-1802.06901-deterministic-non-autoregressive-neural-sequence-modeling-by-iterative-r.md)**  
  実装：[✓](https://github.com/nyu-dl/dl4mt-nonauto) ・ リポジトリ内被引用：10  
  本研究は、出力系列を左から右へ一語ずつ生成する自己回帰モデルの逐次依存を取り除き、系列全体を同時に予測した後、少数回の反復で文章を修正する決定論的な非自己回帰系列生成法を提案する。

### 10年前（2016-11〜2017-10）

- **2017-01 · [Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](2017-1701.06538-outrageously-large-neural-networks-the-sparsely-gated-mixture-of-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：202  
  本論文は、ニューラルネットワークの総パラメータ数を増やすと各入力での計算量も増えるという密なモデルの制約を、入力ごとに一部の専門家だけを実行する条件付き計算によって緩和した基礎研究である。モデルの総容量を大きくしても、活性化する専門家数を固定すれば入力一件あたりの専門家演算量はほぼ一定にできる。ただし専門家を増やすだけでは高速にならない。

### 11年前（2015-11〜2016-10）

- **2016-06 · [Compression of Neural Machine Translation Models via Pruning](2016-1606.09274-compression-of-neural-machine-translation-models-via-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  この論文は、注意機構付きの長短期記憶（LSTM）を使うニューラル機械翻訳器について、どの重みを消せば翻訳品質を損なわずに保存パラメータを減らせるかを実験した2016年の研究である。種類非依存枝刈りでは、40%の重みを消しても再学習前の品質劣化は小さく、さらに80%を消した後に残存重みだけを4エポック再学習すると20.91 BLEUまで回復した。
<!-- survey:auto:end -->
