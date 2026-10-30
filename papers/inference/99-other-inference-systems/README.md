# Other Inference Systems

推論効率化を主目的とするが、現時点では他の系統へ自然に入らず、**独立系統を作るほど同種研究がまだ集まっていない手法**を置く。ここに論文が増えて共通した問題設定・主要技術・評価軸が見えてきた場合は、新しい系統へ分割する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（848本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/99-other-inference-systems/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-02 · [Fast KV Compaction via Attention Matching](2026-2602.16284-fast-kv-compaction-via-attention-matching.md)**  
  実装：[✓](https://github.com/adamzweiger/compaction) ・ リポジトリ内被引用：13  
  長文脈のKVキャッシュを、将来の問い合わせで元の注意挙動を再現する短い鍵・値・バイアスへ置き換える。参照問い合わせの生成、鍵選択、非負最小二乗による注意質量合わせ、値の最小二乗推定を組み合わせる。

- **2026-01 · [Ministral 3](2026-2601.08584-ministral-3.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  著者らはこの方式を段階蒸留（Cascade Distillation）と呼ぶ。したがって「全評価項目で教師と同等」ではない。

- **2025-12 · [Recursive Language Models](2025-2512.24601-recursive-language-models.md)**  
  実装：[✓](https://github.com/alexzhang13/rlm) ・ リポジトリ内被引用：9  
  再帰型言語モデル（Recursive Language モデル; RLM）は、長い入力を大規模言語モデルの注意窓へ丸ごと入れる代わりに、持続的なプログラム実行環境の変数として保存し、モデル自身がコードを生成して入力の必要箇所を調査・分割・変換する推論方式である。

- **2026-07 · [Read As Human: Compressing Context via Parallelizable Close Reading and Skimming](2026-2602.01840-read-as-human-compressing-context-via-parallelizable-close-reading-and-s.md)**  
  実装：[✓](https://github.com/Twilightaaa/RAM) ・ リポジトリ内被引用：6  
  入力文脈圧縮には、不要な語を削る方式と、文章を連続ベクトルへ変換する方式がある。Qwen3-4Bでの4倍圧縮時、NaturalQAの完全一致率は66.59、2WikiMQAは50.39であり、8倍圧縮時にはそれぞれ61.09、40.24となる。

- **2026-07 · [FlashAccel: Leveraging High-Bandwidth Flash (HBF) for High-Throughput LLM Inference](2026-2607.10186-flashaccel-high-bandwidth-flash-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  HBM級帯域・大容量の高帯域フラッシュをGPUへ統合し、SRAM先読み、重み/KV専用配置、KVの選択的HBM複製、追記型永続管理を協調させて、モデル重みとKVキャッシュをフラッシュ上で直接高並列アクセスする推論アクセラレータ。

- **2026-02 · [QuantVLA: Scale-Calibrated Post-Training Quantization for Vision-Language-Action Models](2026-2602.20309-quantvla-scale-calibrated-post-training-quantization-for-vision-language.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  視覚・言語・行動モデル（vision-language-action モデル; VLA）は、画像と自然言語の指示を統合し、ロボットの連続した操作を生成する。

- **2026-02 · [RelayCaching：協調LLMの生成KVキャッシュ再利用](2026-2603.13289-relaycaching-accelerating-llm-collaboration-via-decoding-kv-cache-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  前段エージェントのデコードKVを後段プリフィルへ渡し、位置補正と中間層・重要トークンだけの疎な再計算で80%以上を再利用し、TTFTを最大4.7倍短縮する。

- **2026-01 · [SWE-Pruner: Self-Adaptive Context Pruning for Coding Agents](2026-2601.16746-swe-pruner-self-adaptive-context-pruning-for-coding-agents.md)**  
  実装：[✓](https://github.com/Ayanami1314/swe-pruner) ・ リポジトリ内被引用：5  
  コード編集エージェントは、問題を理解して修正するまでに何度もファイルを読み、検索し、テストを実行する。cat や grep が返した大量のコードや周辺行を、そのまま大規模言語モデル（LLM）へ渡すと、文脈窓を圧迫し、API料金と推論時間を増やす。しかも一度読み込んだ不要なコードは対話履歴に残り、次の推論でも繰り返し処理される。

- **2026-05 · [SYMPHONY: Enabling Compute-Memory Disaggregation in LLM Serving Systems](2026-0fd53670e945-symphony-enabling-compute-memory-disaggregation-in-llm-serving-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  将来要求の助言信号でKVキャッシュを事前移動し、層優先度と協調HBM管理で不確実性を吸収して計算・メモリ分離を低遅延化する。

- **2026-04 · [Why and When Visual Token Pruning Fails? A Study on Relevant Visual Information Shift in MLLMs Decoding](2026-2604.12358-why-and-when-visual-token-pruning-fails-a-study-on-relevant-visual-infor.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  そのうえで、生成中の注意分布が初期状態から変化した時だけ、退避しておいた視覚トークンを選び直す生成段階移動対応トークン削減（デコード-stage Shift-aware トークン 枝刈り; DSTP）を提案する。

- **2026-02 · [Is Retraining-Free Enough? The Necessity of Router Calibration for Efficient MoE Compression](2026-2603.02217-is-retraining-free-enough-the-necessity-of-router-calibration-for-effici.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  しかし推論時に呼ばれない専門家も含めて大量の重みを保持する必要があり、GPUメモリの制約が厳しい。専門家を削除、低ランク編集、統合する方式はこの常駐重みを減らせるが、圧縮後の性能が元モデルより大きく落ちることがある。

- **2026-02 · [FlashVID: Efficient Video Large Language Models via Training-free Tree-based Spatiotemporal Token Merging](2026-2602.08024-flashvid-efficient-video-large-language-models-via-training-free-tree-ba.md)**  
  実装：[✓](https://github.com/Fanziyang-v/FlashVID) ・ リポジトリ内被引用：4  
  入力フレームが増えるとトークン列が長くなり、注意機構だけでなく全結合層の計算、鍵値キャッシュ、初回応答までの時間が増える。LLaVA-OneVisionでは、視覚トークンを10%まで減らしても四つの主要評価群の平均点58.4から57.9へと小幅な低下にとどまり、元精度の99.1%を維持した。

- **2026-01 · [Native LLM and MLLM Inference at Scale on Apple Silicon](2026-2601.19139-native-llm-and-mllm-inference-at-scale-on-apple-silicon.md)**  
  実装：[✓](https://github.com/waybarrios/vllm-mlx) ・ リポジトリ内被引用：4  
  Apple SiliconはCPUとGPUが同じ物理メモリを利用する統合メモリ構成を持つため、一般的な独立GPU環境とはモデル重みや中間状態の管理条件が異なる。

- **2025-12 · [DEER: Draft with Diffusion, Verify with Autoregressive Models](2025-2512.15176-deer-draft-with-diffusion-verify-with-autoregressive-models.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  DEERは、投機的復号の候補生成器を、左から右へ逐次生成する小型自己回帰モデルから、複数位置をまとめて予測できる離散拡散言語モデル（discrete diffusion language モデル）へ置き換える方式である。

- **2026-06 · [Models Take Notes at Prefill: KV Cache Can Be Editable and Composable](2026-2606.17107-models-take-notes-at-prefill-kv-cache-can-be-editable-and-composable.md)**  
  実装：[✓](https://github.com/19PINE-AI/programmable-kv) ・ リポジトリ内被引用：3  
  プリフィル済みKVキャッシュを結論メモとして捉え、追記訂正による編集とRoPE再配置による部品合成で再プリフィルを回避する。

- **2026-06 · [MiniPIC: Flexible Position-Independent Caching in <100LOC](2026-2606.13126-minipic-flexible-position-independent-caching-in-100loc.md)**  
  実装：[✓](https://github.com/IBM/vllm) ・ リポジトリ内被引用：3  
  例えばシステム指示や文書の並び順が異なる二つの要求は、同じ文書の事前充填を繰り返すことになる。H100単体・2Wikiの12,576サンプルでは、文書の事前充填と最終要求を交互に投入する方式により48.01サンプル/秒を達成し、通常vLLMの32.21サンプル/秒に対して49%増加した。

- **2026-04 · [HAWK: Head Importance-Aware Visual Token Pruning in Multimodal Models](2026-2604.07812-hawk-head-importance-aware-visual-token-pruning-in-multimodal-models.md)**  
  実装：[✓](https://github.com/peppery77/HAWK) ・ リポジトリ内被引用：3  
  画像の解像度や動画のフレーム数が増えると、入力長、注意計算、キー・値キャッシュの負荷が増える。視覚トークンを削減する既存方式には、画像特徴の類似性や注意得点で残すトークンを選ぶものがあるが、注意ヘッドを単純平均すると、画像理解に重要なヘッドとそうでないヘッドを同等に扱ってしまう。

- **2026-04 · [DORA: A Scalable Asynchronous Reinforcement Learning System for Language Model Training](2026-2604.26256-dora-a-scalable-asynchronous-reinforcement-learning-system-for-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  DORAは、大規模言語モデル（Large Language モデル; LLM）の強化学習（Reinforcement Learning; RL）による後学習を、生成する応答の長さが大きく偏る状況でも効率よく進めるシステムである。

- **2026-03 · [The Model Knows Which Tokens Matter: Automatic Token Selection via Noise Gating](2026-2603.07135-the-model-knows-which-tokens-matter-automatic-token-selection-via-noise-.md)**  
  実装：[✓](https://github.com/MedHK23/AutoSelect) ・ リポジトリ内被引用：3  
  重要度の低いトークンを削除する既存手法は、注意重み、類似度、固定削減比などの代理指標を使うことが多く、最終回答に必要な情報を最適に残せるとは限らない。LLaVA-1.5-7Bの576視覚トークンを64個へ削減した条件で、10ベンチマークの平均性能維持率96.5%を報告する。

- **2026-03 · [AgilePruner: An Empirical Study of Attention and Diversity for Adaptive Visual Token Pruning in Large Vision-Language Models](2026-2603.01236-agilepruner-an-empirical-study-of-attention-and-diversity-for-adaptive-v.md)**  
  実装：[✓](https://github.com/cvsp-lab/AgilePruner) ・ リポジトリ内被引用：3  
  従来の注意重視方式は画像符号化器のクラス・トークンが強く注目する領域を残す。LLaVA-1.5-7B、TextVQA、RTX 4090の単一GPU評価で、64個を残す設定は576個を残す基準に対して推論計算量3.14→0.48兆FLOPs、1画像遅延172→115 ms、GPUメモリ13.60→13.30 GBとなった。

- **2026-02 · [Swordsman: Entropy-Driven Adaptive Block Partition for Efficient Diffusion Language Models](2026-2602.04399-swordsman-entropy-driven-adaptive-block-partition-for-efficient-diffusio.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  Swordsmanは、拡散言語モデル（Diffusion Language モデル、DLM）の生成速度と品質を改善するため、出力列を固定長で区切るブロック復号を、モデルの予測エントロピーに応じて動的に区切る方式へ変更する。

- **2026-02 · [SweetSpot: An Analytical Model for Predicting Energy Efficiency of LLM Inference](2026-2602.05695-sweetspot-an-analytical-model-for-predicting-energy-efficiency-of-llm-in.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  SweetSpotは、大規模言語モデル（LLM）の推論で、入力トークン数と生成トークン数が変化したときの出力1トークン当たり電力量を予測する解析モデルである。単に出力が短ければ省エネルギーとは限らない。一方、出力を長くし続けると逐次復号（デコード）で参照するキー・値キャッシュ（KV キャッシュ）が増え、各ステップの計算とメモリアクセスが増える。

- **2026-02 · [ICaRus: Identical Cache Reuse for Efficient Multi Model Inference](2026-2603.13281-icarus-identical-cache-reuse-for-efficient-multi-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  複数の専門言語モデルを順番に呼び出すエージェント型推論では、同じシステム指示、会話履歴、検索資料を何度も入力する。LLaMA-3.1-8Bを使うReAct型の8エージェント構成では、通常のモデル別KV方式に対して95パーセンタイル遅延（P95、遅い側5%に入る境界）を最大11.1倍短縮し、最大スループットを3.8倍に高めた。

- **2026-01 · [MELINOE: Fine-Tuning Enables Memory-Efficient Inference for Mixture-of-Experts Models](2026-2602.11192-melinoe-fine-tuning-enables-memory-efficient-inference-for-mixture-of-ex.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  MELINOEは、混合専門家モデル（MoE）の専門家重みをCPUへ退避する推論環境で、モデル自身の専門家選択を少数の再利用しやすい専門家へ寄せる手法である。著者らはOLMoE、Phi-3.5-MoE、Mixtral-8x7Bを対象に、H100、A100、RTX 4090のメモリ制限環境で評価した。

- **2026-01 · [Latent Space Communication via K-V Cache Alignment](2026-2601.06123-latent-space-communication-via-k-v-cache-alignment.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  モデル固有のKVキャッシュを、共有潜在空間への入出力変換器を介して交換する。単に同じ数値へ復元するのではなく、受信側が後続トークンを正しく予測できる状態を学ぶことで、異なる言語モデル間の内部状態共有を可能にする。

- **2025-12 · [UniQL: Unified Quantization and Low-rank Compression for Adaptive Edge LLMs](2025-2512.03383-uniql-unified-quantization-and-low-rank-compression-for-adaptive-edge-ll.md)**  
  実装：[✓](https://github.com/enyac-group/UniQL) ・ リポジトリ内被引用：3  
  端末上で大規模言語モデル（LLM）を実行する際には、モデルの重みだけでなく、実行時の一時領域やほかのアプリケーションが共有するメモリも考慮する必要がある。4ビット量子化だけで端末に収まるモデルを作れても、別のアプリケーションが起動して空きメモリが減れば、固定サイズの量子化モデルは実行不能になる。

- **2025-12 · [Trellis: Learning to Compress Key-Value Memory in Attention Models](2025-2512.23852-trellis-learning-to-compress-key-value-memory-in-attention-models.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  通常の自己注意では、生成済みの全トークンに対する鍵ベクトルと値ベクトルを保持し、次のトークンでそれらを参照する。提案は、鍵を圧縮して中間表現を得る第1段と、値を圧縮して出力を得る第2段からなる。

- **2025-11 · [A Comprehensive Study on Visual Token Redundancy for Discrete Diffusion-based Multimodal Large Language Models](2025-2511.15098-a-comprehensive-study-on-visual-token-redundancy-for-discrete-diffusion-.md)**  
  実装：[✓](https://github.com/Yrdal3910/dMLLM-Visual-Token-Redundancy-Analysis) ・ リポジトリ内被引用：3  
  本論文は、画像・動画を扱う離散拡散型マルチモーダル大規模言語モデル（discrete diffusion-based Multimodal Large Language Models、dMLLM）に、自己回帰型の視覚トークン枝刈りをそのまま移植しても期待通り高速化しない理由を実験的に分析する。

- **2026-08 · [VPP: Virtual Pipeline Parallelism for Efficient Chunked Prefill in Long-Context LLM Inference](2026-2608.26523-vpp-virtual-pipeline-parallelism-for-efficient-chunked-prefill-in-long-c.md)**  
  実装：[✓](https://github.com/RookieCoder-Camera/vllm-ascend/tree/vpp-dev) ・ リポジトリ内被引用：2  
  非同期通信と要求間詰め込みを追加し、16基のAscend 910C上で長文脈の処理量を動的方式比最大13.1%、混合要求で最大6.7%改善した。

- **2026-07 · [LightRot: A Light-Weighted Rotation Scheme and Architecture for Accurate Low-Bit Large Language Model Inference](2026-2607.27704-lightrot-a-light-weighted-rotation-scheme-and-architecture-for-accurate-.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  低ビットLLM推論では重みだけでなく、推論時に生成される入力活性（IA）とKVキャッシュを4ビットへ量子化したい。

- **2026-07 · [HunyuanOCR-1.5: Making Lightweight OCR VLMs Faster and Better](2026-2607.04884-hunyuanocr-1-5-making-lightweight-ocr-vlms-faster-and-better.md)**  
  実装：[✓](https://github.com/Tencent-Hunyuan/HunyuanOCR) ・ リポジトリ内被引用：2  
  原著の研究全体は、認識精度を改善するデータ構築・学習と、出力生成を高速化する推論機構の二本立てである。OmniDocBenchの単一要求評価で、同じHunyuanOCR-1.5の自己回帰復号と比較した平均ページ遅延は、Transformersで34.850秒から5.474秒、vLLMで3.032秒から1.408秒になった。

- **2026-06 · [Less is MoE: Trimming Experts in Domain-Specialist Language Models](2026-2606.05538-less-is-moe-trimming-experts-in-domain-specialist-language-models.md)**  
  実装：[✓](https://github.com/HectorHHZ/Less-is-MoE) ・ リポジトリ内被引用：2  
  Less is MoEは、混合専門家モデル（Mixture of エキスパート、MoE）を圧縮する際に専門家を丸ごと削ると、一般常識の選択式問題では性能が残っても数学推論やコード生成が崩壊する原因を分析し、専門家内部の順伝播ネットワーク（FFN）中間次元を削るFisher-MoEを提案する研究である。

- **2026-05 · [Beyond Surrogate Gradients: Fully Differentiable Token Pruning for Vision-Language Models](2026-2605.28051-beyond-surrogate-gradients-fully-differentiable-token-pruning-for-vision.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  DiffPruneは、視覚言語モデル（Vision-Language モデル、VLM）の入力画像を多数の視覚トークンへ展開した後、どのトークンだけを言語モデルへ渡すかを学習する方式である。一次論文のLLaVA-1.5-7B評価では、576個の視覚トークンから64個だけを保持する88.9%削減時、10課題の正規化平均性能が元モデルの96.5%となった。

- **2026-04 · [MiniCPM-o 4.5: Towards Real-Time Full-Duplex Omni-Modal Interaction](2026-2604.27393-minicpm-o-4-5-towards-real-time-full-duplex-omni-modal-interaction.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  従来の対話方式では、利用者の発話が終わってからモデルが考え、応答が終わるまで次の入力を十分反映できない。著者のRTX 4090測定では、vLLMのINT4条件で毎秒212.3トークン、初回トークン遅延0.58秒、使用メモリ11GBを報告する。

- **2026-04 · [LearnPruner: Rethinking Attention-based Token Pruning in Vision Language Models](2026-2604.23950-learnpruner-rethinking-attention-based-token-pruning-in-vision-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  LLaVA-v1.5では1画像576トークン、LLaVA-NeXTの高解像度入力では最大2,880トークンとなり、画像の背景や類似領域にも長い系列を割り当てる。LLaVA-v1.5-7Bの8課題では、視覚トークンを平均576個から32個へ削減しても、元モデルを100%とした平均相対性能94.8%を維持した。

- **2026-04 · [Cactus: Accelerating Auto-Regressive Decoding with Constrained Acceptance Speculative Sampling](2026-2604.04987-cactus-accelerating-auto-regressive-decoding-with-constrained-acceptance.md)**  
  実装：[✓](https://github.com/MANGA-UOFA/Cactus) ・ リポジトリ内被引用：2  
  検証器が毎トークンの計算を繰り返す必要を減らす一方、草案器が提案したトークンを確率的に棄却するため、草案器と検証器の分布が異なると効率が落ちる。Qwen3-14Bを検証器、0.6Bを草案器としたSpec-Benchの6種類の課題では、自己回帰生成に対する総合速度倍率がSpSの1.81倍からCactusの1.88倍へ改善した。

- **2026-03 · [Fine-Grained Post-Training Quantization for Large Vision Language Models with Quantization-Aware Integrated Gradients](2026-2603.17809-fine-grained-post-training-quantization-for-large-vision-language-models.md)**  
  実装：[✓](https://github.com/ucas-xiang/QIG) ・ リポジトリ内被引用：2  
  重みと活性値を低ビット化すればメモリ使用量を抑えられるが、量子化誤差の影響は画像と文章という二つのモダリティの間だけでなく、同じモダリティ内の各トークンや層によっても異なる。著者はこれを1.60%の改善と説明するが、表の数値としては1.60ポイントの上昇である。

- **2026-03 · [EvoPrune: Early-Stage Visual Token Pruning for Efficient MLLMs](2026-2603.03681-evoprune-early-stage-visual-token-pruning-for-efficient-mllms.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  多くの既存削減方式は、視覚符号化器が全トークンを処理した後に削減を行うため、後段の言語モデルの事前入力処理は軽くできても、視覚符号化器がすでに使った演算量は取り戻せない。

- **2026-02 · [Out of the Memory Barrier: A Highly Memory Efficient Training System for LLMs with Million-Token Contexts](2026-2602.02108-out-of-the-memory-barrier-a-highly-memory-efficient-training-system-for-llms-with-million-token-contexts.md)**  
  実装：[✓](https://github.com/wenhaoli-xmu/OOMB) ・ リポジトリ内被引用：2  
  チャンク再計算・ページ化KV/勾配・非同期CPUオフロード・疎注意を統合し、Qwen2.5-7Bの4M文脈学習を単一H200で実現する。

- **2026-02 · [OmniSIFT: Modality-Asymmetric Token Compression for Efficient Omni-modal Large Language Models](2026-2602.04804-omnisift-modality-asymmetric-token-compression-for-efficient-omni-modal-.md)**  
  実装：[✓](https://github.com/dingyue772/OmniSIFT) ・ リポジトリ内被引用：2  
  動画と音声を同時に受け取る統合マルチモーダル大規模言語モデルでは、視覚エンコーダと音声エンコーダが生成したトークンを時間順に並べ、言語モデルへ渡す。著者らは20秒のクリップでも2万を超える入力トークンが生じ得ることを問題設定に挙げる。

- **2026-02 · [HiFloat4 Format for Language Model Inference](2026-2602.11287-hifloat4-format-for-language-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  4ビット浮動小数点を使うとモデル容量とメモリ転送を削減できるが、4ビットの中で符号・指数・仮数をすべて表すと、精度と数値範囲の両立が難しい。そこで複数要素で尺度を共有するブロック浮動小数点（Block Floating-Point; BFP）を利用する。尺度が階層化されるため、外れ値が一部の要素だけにある場合も群全体の量子化刻みを粗くしすぎずに済む。

- **2026-02 · [HiDrop: Hierarchical Vision Token Reduction in MLLMs via Late Injection, Concave Pyramid Pruning, and Early Exit](2026-2602.23699-hidrop-hierarchical-vision-token-reduction-in-mllms-via-late-injection-c.md)**  
  実装：[✓](https://github.com/EIT-NLP/HiDrop) ・ リポジトリ内被引用：2  
  LLaVA型の画像言語モデルは、画像符号化器が出力した多数の視覚特徴を言語モデルの入力列へ結合する。この前提では、視覚情報の統合が実際に行われる層と計算資源を費やす層が一致しない。

- **2026-01 · [Residual Context Diffusion Language Models](2026-2601.22954-residual-context-diffusion-language-models.md)**  
  実装：[✓](https://github.com/yuezhouhu/residual-context-diffusion) ・ リポジトリ内被引用：2  
  マスク型拡散大規模言語モデル（dLLM）は、複数のトークン位置を同時に予測し、確信度が高い位置だけを確定しながら残りを反復更新する。SDAR-8Bでブロック長64のMATH500正答率は通常の逐次ノイズ除去（Sequential Denoising、SeqD）の64.20%から74.40%へ、AIME24は7.08%から18.75%へ改善する。

- **2025-12 · [More Than Bits: Multi-Envelope Double Binary Factorization for Extreme Quantization](2025-2512.24545-more-than-bits-multi-envelope-double-binary-factorization-for-extreme-qu.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  大規模言語モデルの重みを1～1.5ビットまで圧縮すると、各重みを独立に丸める方式では振幅の情報が著しく失われ、生成品質が低下する。

- **2025-12 · [Fairy2i: Training Complex LLMs from Real LLMs with All Parameters in {±1, ±i}](2025-2512.02901-fairy2i-training-complex-llms-from-real-llms-with-all-parameters-in-1-i.md)**  
  実装：[✓](https://github.com/PKULab1806/Fairy2i-W2) ・ リポジトリ内被引用：2  
  Fairy2iは、通常の実数値で学習済みのTransformerを、量子化前の出力を変えずに複素数の広義線形（widely-linear）表現へ変換する。実効2ビットのFairy2i-W2はC4検証集合の困惑度（Perplexity; PPL）7.85、ARC-Easyなど五つのゼロショット課題平均62.00%を示した。

- **2025-12 · [Bolmo: Byteifying the Next Generation of Language Models](2025-2512.15586-bolmo-byteifying-the-next-generation-of-language-models.md)**  
  実装：[✓](https://github.com/allenai/bolmo-core) ・ リポジトリ内被引用：2  
  本研究の中心課題は、強力なサブワード言語モデルをすべて一から学習し直さずに、文字の細部を直接扱えるバイト単位のモデルへ変えることである。推論速度は圧縮率に依存し、元モデルに近い4.4バイト/パッチではBolmoの方が遅い。

- **2025-12 · [AdmTree: Compressing Lengthy Context with Adaptive Semantic Trees](2025-2512.04550-admtree-compressing-lengthy-context-with-adaptive-semantic-trees.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  AdmTreeは、長い文書を大規模言語モデル（LLM）へ入力する際、入力トークンを短い潜在表現へ圧縮しつつ、局所的な事実と文書全体の意味を両立して保持する方式である。LongBenchの評価では、Llama-2-7Bを基盤にしたAdmTreeの平均得点は44.1で、活性値 Beaconの40.1を上回った。

- **2025-11 · [Nemotron-Flash: Towards Latency-Optimal Hybrid Small Language Models](2025-2511.18890-nemotron-flash-towards-latency-optimal-hybrid-small-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  GPUで1トークンずつ復号する際、層を何回順に通過するか、どの演算子が起動されるか、状態やKVをどれだけ転送するかが遅延を決める。Nemotron-Flashは、モデルの大きさよりも実際のGPU上での遅延制約を第一の設計目標とする。

- **2026-09 · [Tensor Decomposition of Transformer Key-Value Caches: Spectral Structure and Format Comparison](2026-2609.28029-tensor-decomposition-of-transformer-key-value-caches-spectral-structure-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  この研究は、自己回帰Transformerの鍵・値キャッシュ（key-value キャッシュ; KVキャッシュ）を、注意ヘッド・トークン・特徴・隣接層の四つの軸を持つテンソルとして扱い、どの軸が実際に低ランク圧縮できるのかを調べる。RoPE後の鍵を圧縮すると、RoPE前に圧縮する場合に比べて同じ保存量での再構成誤差が相対41〜64%増す。

- **2026-09 · [Online Draft Co-Training for Speculative Decoding in Large-Scale, Long-Context RL Post-Training](2026-2609.07108-online-draft-co-training-for-speculative-decoding-in-large-scale-long-context-rl-post-training.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長文脈RLで投機的復号のドラフトを方策と同時更新するため、分岐注意を文脈並列リングへ統合し、中間特徴をパイプライン外のTapChannelで輸送して、最大122B規模で学習品質を保ちつつ最大1.88倍の全体高速化を得る。

- **2026-08 · [H-Scale: Hessian-Guided Scale Refinement for NVFP4 Sub-Byte LLM Inference](2026-2608.28113-h-scale-hessian-guided-scale-refinement-for-nvfp4-sub-byte-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  H-Scaleは、NVIDIA Blackwell世代のGPUが直接扱える4ビット浮動小数点量子化形式（NVFP4）に対して、重みをどの4ビット値へ丸めるかではなく、16個の重みに共通して掛ける尺度をどう選ぶかに着目した学習後量子化（Post-学習 量子化; PTQ）の後処理である。

- **2026-08 · [Beyond Parallel Blindness: Information Floors and Model Gaps in Block Drafting](2026-2608.27339-beyond-parallel-blindness-information-floors-and-model-gaps-in-block-dra.md)**  
  実装：[✓](https://github.com/tie-pilot-qxw/specfloor) ・ リポジトリ内被引用：1  
  投機的復号では、小型の草案モデルが将来のトークンを提案し、元のターゲットモデルがそれを検証する。Qwen3-4B、7位置の草案では、完全並列方式の最終位置で情報下限が0.286に達する一方、直前の実トークン1個だけを見せるとこの下限の86〜100%が解消した。

- **2026-08 · [Archer: Adaptive Reuse of Cached Hidden States for Efficient Rollback in Diffusion Language Models](2026-2608.08086-archer-adaptive-reuse-of-cached-hidden-states-for-efficient-rollback-in-.md)**  
  実装：[✓](https://github.com/Hxnng/Archer) ・ リポジトリ内被引用：1  
  本研究は、拡散言語モデル（Diffusion Language モデル; DLM）が一度生成したトークンを後から置換・再マスクできる「巻き戻し（rollback）」を保持しながら、繰り返しの全系列再計算を減らす推論時のキャッシュ制御を扱う。ただし応答を再計算することと、元の全再計算方式と同じ出力分布・復号経路を保証することは異なる。

- **2026-07 · [WISERouter: LLM Routing with Workload Budget Constraint](2026-2607.23765-wiserouter-llm-routing-with-workload-budget-constraint.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  常に最高性能のモデルを呼ぶと料金が膨らむ一方、全問い合わせに固定額を課すと、容易な問い合わせで節約した予算を難しい問い合わせへ振り向けられない。過去のモデル応答をすべて持つWR-Offlineと、限られた応答だけを逐次観測するWR-Onlineの二方式がある。

- **2026-06 · [Memory is Reconstructed, Not Retrieved: Graph Memory for LLM Agents](2026-2606.06036-memory-is-reconstructed-not-retrieved-graph-memory-for-llm-agents.md)**  
  実装：[✓](https://github.com/Ji-shuo/MRAgent) ・ リポジトリ内被引用：1  
  MRAgent（メモリ Reasoning 構成 for LLM Agents）は、対話記憶を「手掛かり（Cue）・関連タグ（Tag）・記憶内容（Content）」の三者関係として整理し、LLMが現在までに得た証拠に応じて次の検索操作を選ぶ能動的な記憶再構成を提案する。

- **2026-06 · [Do Transformers Need Three Projections? Systematic Study of QKV Variants](2026-2606.04032-do-transformers-need-three-projections-systematic-study-of-qkv-variants.md)**  
  実装：[✓](https://github.com/anushamadan02/Do-Transformers-Need-3-Projections) ・ リポジトリ内被引用：1  
  標準的なTransformerの注意機構では、入力表現Xを三つの独立した行列で変換し、問い合わせ（Query; Q）、鍵（Key; K）、値（Value; V）を生成する。鍵と値を同一射影にすると、推論時にKだけを保持してVとしても再利用でき、標準的なQKVに比べてKVキャッシュを50%削減できる。

- **2026-06 · [Delay-Adaptive Speculation Control for Low-Latency Edge-Cloud LLM Inference](2026-2606.20591-delay-adaptive-speculation-control-for-low-latency-edge-cloud-llm-infere.md)**  
  実装：[✓](https://github.com/szpsunkk/UCB-SpecStop) ・ リポジトリ内被引用：1  
  本論文は、端末・クラウド分散推論（edge-cloud inference）で投機的復号（投機的復号）を行うとき、草稿モデルが一度に生成するトークン数を通信遅延に応じて決める問題を扱う。時間と採択数の「平均の比」を使う点が、各回の時間／採択数を単純平均する方式と異なる。

- **2026-06 · [AlphaQ: Calibration-Free Bit Allocation for Mixture-of-Experts Quantization](2026-2606.04980-alphaq-calibration-free-bit-allocation-for-mixture-of-experts-quantizati.md)**  
  実装：[✓](https://github.com/Superone77/AlphaQ) ・ リポジトリ内被引用：1  
  しかし、推論時に選択され得る専門家の重みをGPUまたは周辺メモリへ配置する必要があるため、活性化の疎性がそのまま重みの記憶容量削減につながるわけではない。専門家ごとに2、3、4ビットなど異なる量子化精度を与えれば容量を減らせるが、どの専門家を高精度で守るかが問題になる。

- **2026-05 · [Training-Inference Consistent Segmented Execution for Long-Context LLMs](2026-2605.11744-training-inference-consistent-segmented-execution-for-long-context-llms.md)**  
  実装：[✓](https://github.com/sxp11/Training-Inference-Consistent-Segmented-Execution) ・ リポジトリ内被引用：1  
  長文脈の大規模言語モデル（LLM）は、通常の全注意力（full self-注意機構）を使うと、入力が長くなるにつれて注意演算と中間状態の記憶費用が増大する。16K/32K事前充填でのGPUピークメモリは18.56/19.06GBで、全注意力の23.61/34.67GBより小さい。

- **2026-05 · [Test-Time Speculation](2026-2605.09329-test-time-speculation.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号（投機的復号）は、小さく高速なドラフトモデルに複数トークンの候補を作らせ、大きな対象モデルがまとめて検証することで、対象モデルの呼び出し回数を減らす方式である。原著の実験ではDFlashを基準に受理長が平均41%、最大72%改善し、EAGLE-3を基準に平均34%、最大67%改善した。

- **2026-05 · [Tensor Cache: Eviction-conditioned Associative Memory for Transformers](2026-2605.22884-tensor-cache-eviction-conditioned-associative-memory-for-transformers.md)**  
  実装：[✓](https://github.com/kswain98/tensor-cache) ・ リポジトリ内被引用：1  
  長文脈や同時要求数が増えるほどキャッシュの占有量が増え、GPUメモリ容量と帯域を圧迫する。学習可能なゲートでL1の局所注意出力とL2の読出しを融合することで、固定容量を保ちながら窓外の情報を予測へ戻す。

- **2026-05 · [Speculative Pipeline Decoding: Higher-Accuracy Drafting with Hidden Latency via Pipeline Parallelism](2026-2605.30852-speculative-pipeline-decoding-higher-accuracy-drafting-with-hidden-laten.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  通常の投機的復号では、小型ドラフトモデルが将来の複数トークンを先に作り、ターゲットLLMが一度に検証する。多数GPUを消費して単一系列の遅延を短縮する設計であり、1GPU当たりの演算効率や総クラスタ費用の改善とは区別する。

- **2026-05 · [Pruning and Distilling Mixture-of-Experts into Dense Language Models](2026-2605.28207-pruning-and-distilling-mixture-of-experts-into-dense-language-models.md)**  
  実装：[✓](https://github.com/krafton-ai/moe-to-dense) ・ リポジトリ内被引用：1  
  演算量は小さくても、すべての専門家をGPUメモリへ常駐させる場合の容量は大きい。CPUへ退避すれば容量制約を緩和できるが、専門家の転送が遅延や帯域を圧迫する。Qwen3-30B-A3Bから約3.3Bの密な生徒モデルを作った実験では、約4Bトークンの蒸留後に5課題の平均58.10%を達成した。

- **2026-05 · [Nearly Optimal Attention Coresets](2026-2605.05602-nearly-optimal-attention-coresets.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長文脈LLMのKVキャッシュを元の鍵・値対の部分集合へ縮約する際、全てのノルム有界な問い合わせに対して注意出力誤差をε以内に保つコアセットの存在上界と情報理論的下界を証明。計算可能な高速KV削除アルゴリズムや実モデルの品質・速度改善を実証する論文ではない。

- **2026-05 · [Multi-Stream LLMs: Unblocking Language Models with Parallel Streams of Thoughts, Inputs and Outputs](2026-2605.12460-multi-stream-llms-unblocking-language-models-with-parallel-streams-of-th.md)**  
  実装：[✓](https://github.com/seal-rg/streaming) ・ リポジトリ内被引用：1  
  Multi-Stream LLMsは、利用者、回答、内部思考、監査などの役割を独立したトークン列へ割り当て、一回の前向き計算で各列の次トークンを同時に生成するモデル形式を提案する。

- **2026-05 · [Move the Query, Not the Cache: Characterizing Cross-Instance Latent Attention Redistribution Across GPU Fabrics](2026-2606.01502-move-the-query-not-the-cache-characterizing-cross-instance-latent-attention-redistribution-across-gpu-fabrics.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  約1KBの問い合わせを遠隔キャッシュへ送り注意計算する方式を実H100で測定し、約3msのキャッシュ再適応より数十µsの往復が有利となる条件を閉形式化する。

- **2026-05 · [Locality-Aware Redundancy Pruning for LLM Depth Compression](2026-2605.27786-locality-aware-redundancy-pruning-for-llm-depth-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LoRP（Locality-Aware Redundancy Pruning）は、事前学習済み大規模言語モデルのTransformerブロックを、追加学習なしに削除する深さ枝刈り（depth 枝刈り）方式である。

- **2026-05 · [Full Attention Strikes Back: Transferring Full Attention into Sparse within Hundred Training Steps](2026-2605.16928-full-attention-strikes-back-transferring-full-attention-into-sparse-with.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長文脈の大規模言語モデル（Large Language モデル; LLM）は、すべてのトークンへ注意を計算する全注意（Full 注意機構）を使うと、系列長の増加に伴って注意計算とキー・値（Key-Value; KV）キャッシュの負荷が増える。著者は100万トークン文脈のプリフィルで最大9.36倍、復号で約2.01倍の速度向上を報告する。

- **2026-05 · [ConQuR: Corner Aligned Activation Quantization via Optimized Rotations for LLMs](2026-2605.10793-conqur-corner-aligned-activation-quantization-via-optimized-rotations-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  低ビット量子化では、重みだけでなく中間活性値を4ビットなどで表現できれば、行列積の計算・転送の効率化余地が増す。

- **2026-05 · [BubbleSpec: Turning Long-Tail Bubbles into Speculative Rollout Drafts for Synchronous Reinforcement Learning](2026-2605.08862-bubblespec-turning-long-tail-bubbles-into-speculative-rollout-drafts-for.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  従来の非同期化はこの待ちを減らせるが、生成時の方策と更新時の方策がずれるという別の問題を持ち込む。候補が誤っていても棄却サンプリングで目標分布へ戻すため、古い方策の出力を無条件に採用する方式とは異なる。通常のVerlと比べ、復号ステップ数は48.9～56.8%減、ロールアウト時間は30.0～45.2%減である。

- **2026-05 · [Beyond Position Bias: Shifting Context Compression from Position-Driven to Semantic-Driven](2026-2605.09463-beyond-position-bias-shifting-context-compression-from-position-driven-t.md)**  
  実装：[✓](https://anonymous.4open.science/r/seco-EE5E) ・ リポジトリ内被引用：1  
  本論文の対象は、長い文脈を少数の連続値の埋め込み（soft プロンプト）へ圧縮してから回答を生成する方式である。LLaMA-3.2-1B-Instructを用いた16倍圧縮・分布内6課題の平均完全一致率は、比較方式COMIの42.07に対してSeCoが53.52、平均F1は54.37に対して68.55であった。

- **2026-05 · [Attention Once Is All You Need: Efficient Streaming Inference with Stateful Transformers](2026-2605.13784-attention-once-is-all-you-need-efficient-streaming-inference-with-statef.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文は、金融時系列、センサ、ログのようにデータが継続的に追加され、利用者からの質問がときどき到着する用途に対し、質問の到着を待たずにデータを処理する状態保持型（Stateful）LLM推論を提案する。

- **2026-04 · [VFA: Relieving Vector Operations in Flash Attention with Global Maximum Pre-computation](2026-2604.12798-vfa-relieving-vector-operations-in-flash-attention-with-global-maximum-p.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  FlashAttentionは、巨大な注意行列をGPUの高帯域メモリへ書き出さず、クエリ・キー・値を小さなブロックに分割してオンチップメモリで処理する。VFA（Vector Relieved Flash 注意機構）はこの残った部分に焦点を当てる。要旨ではC16V32という計算器構成を基準にC8V32、C4V32、C4V16で約2倍の高速化を報告する。

- **2026-04 · [Tango: Taming Visual Signals for Efficient Video Large Language Models](2026-2604.09547-tango-taming-visual-signals-for-efficient-video-large-language-models.md)**  
  実装：[✓](https://github.com/xjtupanda/Tango) ・ リポジトリ内被引用：1  
  Tangoは、動画大規模言語モデル（Video LLM）へ渡す視覚トークンの数を削減する、学習不要の前処理方式である。LLaVA-OneVision-7Bの32フレーム評価では、視覚トークンを10%にしたとき元の4ベンチマーク平均性能の98.9%を保持し、実測推論速度は1.88倍となった。

- **2026-04 · [Structural Pruning of Large Vision Language Models: A Comprehensive Study on Pruning Dynamics, Recovery, and Data Efficiency](2026-2604.24380-structural-pruning-of-large-vision-language-models-a-comprehensive-study.md)**  
  実装：[✓](https://github.com/YiranHuangIrene/VLMCompression) ・ リポジトリ内被引用：1  
  本論文は新しい単一の枝刈りアルゴリズムを提案するというより、何を削るか、何を再学習するか、どれだけのデータを使うかの組合せを、異なる視覚言語モデルで統制して比較する研究である。

- **2026-04 · [Open-Loop Planning, Closed-Loop Verification: Speculative Verification for VLA](2026-2604.02965-open-loop-planning-closed-loop-verification-speculative-verification-for.md)**  
  実装：[✓](https://github.com/edsad122/SV-VLA) ・ リポジトリ内被引用：1  
  本論文は、計画は重いモデルで低頻度に実施し、計画が依然として妥当かの検査だけを軽いモデルで毎制御時刻に実施するSV-VLA（投機的 検証 for VLA Control）を提案する。

- **2026-04 · [MemoSight: Unifying Context Compression and Multi Token Prediction for Reasoning Acceleration](2026-2604.14889-memosight-unifying-context-compression-and-multi-token-prediction-for-re.md)**  
  実装：[✓](https://github.com/helldog-star/MemoSight) ・ リポジトリ内被引用：1  
  MemoSightは、長い思考連鎖（Chain-of-Thought; CoT）の鍵・値キャッシュ（KV キャッシュ）を減らす文脈圧縮と、次の複数トークンを予測する先読みを、一つの追加学習手順で実現する方式である。

- **2026-04 · [GSQ: Highly-Accurate Low-Precision Scalar Quantization for LLMs via Gumbel-Softmax Sampling](2026-2604.18556-gsq-highly-accurate-low-precision-scalar-quantization-for-llms-via-gumbe.md)**  
  実装：[✓](https://github.com/IST-DASLab/GSQ) ・ リポジトリ内被引用：1  
  大規模言語モデルを2～3ビット程度に圧縮すると、重みの転送量と常駐メモリを大幅に減らせる。Llama-3.1-8B/70Bの2ビット評価で従来スカラー量子化より高い精度を示し、Qwen3-8Bの既存GGUF K-Quantチェックポイントを同じ保存形式のまま改善する点が実用上重要である。

- **2026-04 · [Equifinality in Mixture of Experts: Routing Topology Does Not Determine Language Modeling Quality](2026-2604.14419-equifinality-in-mixture-of-experts-routing-topology-does-not-determine-l.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  著者は学習可能な重心ベクトルとの余弦類似度で専門家を選ぶ幾何学的ルータを作り、一段で多数の専門家を選ぶ方式、複数段で少数ずつ選び直す方式、段ごとの射影を変える方式などを比較した。

- **2026-04 · [Efficient Quantization of Mixture-of-Experts with Theoretical Generalization Guarantees](2026-2604.06515-efficient-quantization-of-mixture-of-experts-with-theoretical-generaliza.md)**  
  実装：[✓](https://github.com/nowazrabbani/moe_quantization) ・ リポジトリ内被引用：1  
  本研究は、混合専門家モデル（Mixture-of-Experts、MoE）の推論メモリを減らすため、全専門家を同じビット幅へ量子化する代わりに、専門家ごとに1〜3ビットなど異なる精度を割り当てる方式を提案する。Mixtral 8x7Bの8課題平均では、専門家平均2.5ビットの提案方式が68.38%、比較方式PMQが67.53%だった。

- **2026-04 · [ART: Attention Run-time Termination for Efficient Large Language Model Decoding](2026-2606.00024-art-attention-run-time-termination-for-efficient-large-language-model-de.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ART（注意機構 Run-time Termination）は、大規模言語モデルの復号中に、注意計算の累積出力が十分安定したと判断できた時点で残りのキー・値（key-value; KV）ブロックへのアクセスを止める方式である。

- **2026-04 · [A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression](2026-2604.19572-a-self-evolving-framework-for-efficient-terminal-agents-via-observationa.md)**  
  実装：[✓](https://github.com/multimodal-art-projection/TACO) ・ リポジトリ内被引用：1  
  TACO（Terminal Agent Compression）は、コマンド出力をエージェントの履歴へ入れる直前に圧縮する追加層である。MiniMax-M2.5によるTerminalBench 1.0では成功率42.30%→45.25%、総トークン29.74→23.43百万（21.2%減）である。

- **2026-03 · [SliderQuant: Accurate Post-Training Quantization for LLMs](2026-2603.25284-sliderquant-accurate-post-training-quantization-for-llms.md)**  
  実装：[✓](https://github.com/deep-optimization/SliderQuant) ・ リポジトリ内被引用：1  
  SliderQuantは、事前学習済みLLMを追加の大規模学習なしで低ビット化する事後量子化（PTQ）方式である。Llama2-7BのW4A4でWikiText2困惑度（PPL）はCBQの12.73に対し8.34、Qwen3-30B-A3BのW4A4ではOmniQuantのゼロショット平均50.11%に対し66.86%だった。

- **2026-03 · [Prune-then-Quantize or Quantize-then-Prune? Understanding the Impact of Compression Order in Joint Model Compression](2026-2603.18426-prune-then-quantize-or-quantize-then-prune-understanding-the-impact-of-c.md)**  
  実装：[✓](https://github.com/snudatalab/PQQP) ・ リポジトリ内被引用：1  
  本論文は、大規模言語モデル（LLM）を枝刈り（枝刈り）と量子化（量子化）の両方で圧縮する場合、どちらを先に適用すべきかを、圧縮率とモデル品質の関係から分析した研究である。枝刈り率5～30%、量子化4～8ビットを含む条件で、単独適用時の圧縮強度の差が大きいほど順序による品質差が大きくなる傾向を確認した。

- **2026-03 · [OneComp: One-Line Revolution for Generative AI Model Compression](2026-2603.28845-onecomp-one-line-revolution-for-generative-ai-model-compression.md)**  
  実装：[✓](https://github.com/FujitsuResearch/OneCompression) ・ リポジトリ内被引用：1  
  大規模言語モデル（Large Language モデル; LLM）の重み量子化では、同じ平均ビット幅でも層ごとの感度、較正用入力の分布、丸め誤差の伝播、量子化後の品質回復方法によって性能が大きく変わる。Llama-3-8BとQwen3系の実験では、感度に応じた混合ビット幅割当や誤差伝播補正が量子化後の困惑度を改善した。

- **2026-03 · [CSAttention: Centroid-Scoring Attention for Accelerating LLM Inference](2026-2604.08584-csattention-centroid-scoring-attention-for-accelerating-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長文脈の自己注意では、現在の問い合わせベクトルと過去の鍵ベクトルとの内積を計算し、対応する値を重み付き集約する。多くの鍵の寄与が小さいため、一部の鍵だけを使う疎注意で演算量と転送量を削減できる。しかし95%もの鍵を捨てる場合、実際に重要な鍵を取りこぼすと正答率が急落する。鍵の全件走査をオンラインで繰り返さない設計である。

- **2026-03 · [Compressing Language Models for Specialized Domains](2026-2502.18424-compressing-language-models-for-specialized-domains.md)**  
  実装：[✓](https://github.com/mlsw/domain-compression) ・ リポジトリ内被引用：1  
  言語モデルを量子化・剪定して配備コストを下げると、汎用ベンチマークの正解率が比較的よく残っていても、医療・法務などの専門領域の精度が大きく落ちる場合がある。

- **2026-03 · [BATQuant: Outlier-resilient MXFP4 Quantization via Learnable Block-wise Optimization](2026-2603.16590-batquant-outlier-resilient-mxfp4-quantization-via-learnable-block-wise-o.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデル（LLM）や画像言語モデル（MLLM）の重み・活性化を4ビットへ量子化すれば、メモリ帯域と計算資源の負担を軽くできる可能性がある。マルチモーダル5課題の総合回復率はBF16比96.43%で、同条件のFlatQuant94.79%、GPTQ94.64%を上回る。

- **2026-03 · [ASAP: Attention-Shift-Aware Pruning for Efficient LVLM Inference](2026-2603.14549-asap-attention-shift-aware-pruning-for-efficient-lvlm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ASAPはこの注意の位置偏り（注意機構 shift）を緩和するため、視覚トークン同士に限り、重要度の高い未来位置への注意を段階的に許可する。

- **2026-03 · [ArcLight: A Lightweight LLM Inference Architecture for Many-Core CPUs](2026-2603.07770-arclight-a-lightweight-llm-inference-architecture-for-many-core-cpus.md)**  
  実装：[✓](https://github.com/OpenBMB/ArcLight) ・ リポジトリ内被引用：1  
  NUMAごとのメモリ配置、動的スレッド群、Scatter/Gather型テンソル並列を一体化し、多数コアCPUの遠隔メモリアクセス壁を避けて、192コアARM環境でllama.cpp比最大46%高い推論スループットを示す軽量CPU推論基盤。

- **2026-02 · [T3D: Few-Step Diffusion Language Models via Trajectory Self-Distillation with Direct Discriminative Optimization](2026-2602.12262-t3d-few-step-diffusion-language-models-via-trajectory-self-distillation-.md)**  
  実装：[✓](https://github.com/Tyrion58/T3D) ・ リポジトリ内被引用：1  
  これに対しマスク拡散言語モデル（Masked Diffusion Language モデル、MDLM）は、複数位置のマスクを並列に予測し、繰り返し修正して文章を完成させる。動的復号を組み合わせた一部条件では、GSM8Kの正答率を10.8ポイント改善しながら処理量を1.45倍にする実測結果も報告されている。

- **2026-02 · [ScaleBITS: Scalable Bitwidth Search for Hardware-Aligned Mixed-Precision LLMs](2026-2602.17698-scalebits-scalable-bitwidth-search-for-hardware-aligned-mixed-precision-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデル（LLM）の重みを4ビット未満に量子化すると、同じ平均ビット数でも、どの重みを低精度にするかによって予測品質が大きく変わる。第三に、行列積のタイルと整合する64×128重みブロックへ整数ビット幅を割り当て、勾配に基づく一括更新と受理判定で全モデルの平均容量予算へ近づける。

- **2026-02 · [ReviveMoE: Fast Recovery for Hardware Failures in Large-Scale MoE LLM Inference Deployments](2026-2602.21140-revivemoe-fast-hardware-failure-recovery.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  単一NPU障害時にサービング全体を再起動せず、要求状態・KVブロック表・MoE重み・通信領域・実行グラフを局所修復して大規模MoE推論を高速復旧する。

- **2026-02 · [Reasoning with Latent Tokens in Diffusion Language Models](2026-2602.03769-reasoning-with-latent-tokens-in-diffusion-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  この研究の問いは、マスク型拡散言語モデルが複雑な制約充足問題で自己回帰モデルより良い成績を示す場合、その差が何によって生じるのか、というものである。通常の拡散生成では未確定の複数位置について同時に分布を計算するが、一回の反復で実際に確定する位置はその一部だけである。残りの位置の出力はその反復では捨てられる。研究の核は二つある。

- **2026-02 · [RAT+: Train Dense, Infer Sparse -- Recurrence Augmented Attention for Dilated Inference](2026-2602.18196-rat-train-dense-infer-sparse-recurrence-augmented-attention-for-dilated-.md)**  
  実装：[✓](https://github.com/wimh966/rat-plus) ・ リポジトリ内被引用：1  
  注意機構の推論コストを下げる方法には、局所窓だけを見る方式や、重要なトークンだけを選ぶ方式がある。D=16では密な注意に近い精度を保ち、D=64では常識推論の平均正解率が59.21%から57.46%へ下がる一方、時間混合部分の理論演算量とKV保存量を64分の1へ減らす。

- **2026-02 · [MoSE: Mixture of Slimmable Experts for Efficient and Adaptive Language Models](2026-2602.06154-mose-mixture-of-slimmable-experts-for-efficient-and-adaptive-language-mo.md)**  
  実装：[✓](https://github.com/tnurbek/mose) ・ リポジトリ内被引用：1  
  MoSEは、混合専門家モデル（Mixture-of-Experts; MoE）の「専門家を何個選ぶか」に加え、「選んだ各専門家を何割の中間幅で実行するか」を推論時に変える研究である。主指標は一トークン当たり浮動小数点演算量（FLOPs/トークン）と品質であり、実機処理率は補助的な検証である。

- **2026-02 · [Improving Sampling for Masked Diffusion Models via Information Gain](2026-2602.18176-improving-sampling-for-masked-diffusion-models-via-information-gain.md)**  
  実装：[✓](https://github.com/yks23/Information-Gain-Sampler) ・ リポジトリ内被引用：1  
  モデルの再学習を要しない復号時のアルゴリズムである。Dream-7B-Instructで数学・コード・計画の6課題を評価した原著表2では、復号率K=2の平均正解率が53.4%、K=1で62.0%となる。

- **2026-02 · [FlexRank: Nested Low-Rank Knowledge Decomposition for Adaptive Model Deployment](2026-2602.02680-flexrank-nested-low-rank-knowledge-decomposition-for-adaptive-model-depl.md)**  
  実装：[✓](https://github.com/RickZack/FlexRank) ・ リポジトリ内被引用：1  
  FlexRankは、一つの事前学習済みモデルから、計算・メモリ予算に応じて大きさの異なる複数の部分モデルを切り出すための低ランク分解・学習方式である。

- **2026-02 · [Effective MoE-based LLM Compression by Exploiting Heterogeneous Inter-Group Experts Routing Frequency and Information Density](2026-2602.09316-effective-moe-based-llm-compression-by-exploiting-heterogeneous-inter-gr.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  RFID-MoEは、混合専門家（Mixture-of-Experts; MoE）型の大規模言語モデルを、事後学習の重み圧縮で小さくする研究である。論文はQwen3-235B-A22Bの総重み容量が8基のA100 40GB、合計320GBに収まらない例を挙げ、演算の疎性と保存容量の大きさが別問題であることを示す。

- **2026-02 · [Data Distribution Matters: A Data-Centric Perspective on Context Compression for Large Language Model](2026-2602.01778-data-distribution-matters-a-data-centric-perspective-on-context-compress.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長文脈の大規模言語モデル（LLM）では、入力の全トークンをそのまま処理するより、先に少数の潜在表現へ圧縮して復元器へ渡す方法が考えられる。

- **2026-02 · [CoMoL: Efficient Mixture of LoRA Experts via Dynamic Core Space Merging](2026-2603.00573-comol-efficient-mixture-of-lora-experts-via-dynamic-core-space-merging.md)**  
  実装：[✓](https://github.com/DCDmllm/CoMoL) ・ リポジトリ内被引用：1  
  本論文は、低ランク適応（LoRA）を複数の専門家へ拡張する際に、専門家の数に比例して増える学習パラメータと計算量を抑えつつ、トークン単位の細かな経路選択を維持するCoMoLを提案する。

- **2026-01 · [Towards Compute-Aware In-Switch Computing for LLMs Tensor-Parallelism on Multi-GPU Systems](2026-161bea97e0de-towards-compute-aware-in-switch-computing-for-llms-tensor-parallelism-on-multi-gpu-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  NVLSの通信意味論をLLM計算カーネルの読み書き要求へ合わせ、スイッチ内要求マージ・GPU間TB協調・データフロー重畳でテンソル並列の通信待ちを削減する。

- **2026-01 · [The Perplexity Paradox: Why Code Compresses Better Than Math in LLM Prompts](2026-2602.15843-the-perplexity-paradox-why-code-compresses-better-than-math-in-llm-promp.md)**  
  実装：[✓](https://github.com/micoverde/taac-llm-compression) ・ リポジトリ内被引用：1  
  本研究は、大規模言語モデル（LLM）へ渡す入力文を短縮する際、言語モデルが予測しにくいトークンと、下流の課題を解くために残すべきトークンが一致するとは限らないという問題を扱う。関数署名再挿入では正答率が5.3%から39.3%へ34.0ポイント回復した。

- **2026-01 · [SyncThink: A Training-Free Strategy to Align Inference Termination with Reasoning Saturation](2026-2601.03649-syncthink-a-training-free-strategy-to-align-inference-termination-with-r.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  SyncThinkは、思考過程を明示的に生成する推論特化言語モデルに対し、追加学習なしで推論を早期終了させる復号制御方式である。

- **2026-01 · [SimpleMem: Efficient Lifelong Memory for LLM Agents](2026-2601.02553-simplemem-efficient-lifelong-memory-for-llm-agents.md)**  
  実装：[✓](https://github.com/aiming-lab/SimpleMem) ・ リポジトリ内被引用：1  
  SimpleMemは、書き込み時に記憶を整理して、質問時に必要な情報だけを引き出すことで、この二種類の費用を同時に抑えようとする方式である。原著のLoCoMo評価では、GPT-4.1-miniを基盤としたSimpleMemの平均F1が43.24、Mem0が34.20で、相対26.4%の改善となる。

- **2026-01 · [LOOKAT: Lookup-Optimized Key-Attention for Memory-Efficient Transformers](2026-2601.10155-lookat-lookup-optimized-key-attention-for-memory-efficient-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LOOKATは、自己回帰Transformerの注意得点計算を、ベクトル検索における内積類似度検索として扱い、キーを圧縮したまま注意得点を計算する方式である。GPT-2の第1注意層で、64次元のキーを2個の1バイト符号へ圧縮すると、キー表現は128バイトから2バイトへ減り、キー単体の表現上の圧縮率は64倍となる。

- **2026-01 · [Is Finer Better? The Limits of Microscaling Formats in Large Language Models](2026-2601.19026-is-finer-better-the-limits-of-microscaling-formats-in-large-language-mod.md)**  
  実装：[✓](https://github.com/iclr2016codeshare/microscaling) ・ リポジトリ内被引用：1  
  本論文は、大規模言語モデルの重みと活性を4ビット浮動小数点（FP4）へ圧縮する際、「量子化のブロックを小さくするほど精度が良くなる」という一般的な期待が破れる条件を明らかにした研究である。

- **2026-01 · [HeRo-Q: A General Framework for Stable Low-Bit Quantization via Hessian Conditioning](2026-2601.21626-hero-q-a-general-framework-for-stable-low-bit-quantization-via-hessian-c.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデル（LLM）の重みを2〜4ビットへ量子化すると、モデルをGPUメモリへ収めやすくなる。Llama-3.1-8BのW4A16条件では、NVIDIA A800上の生成処理量が113.1トークン/秒で、SpinQuantの112.8トークン/秒とほぼ同じである。

- **2026-01 · [Exploring Fine-Tuning for In-Context Retrieval and Efficient KV-Caching in Long-Context Language Models](2026-2601.18527-exploring-fine-tuning-for-in-context-retrieval-and-efficient-kv-caching-.md)**  
  実装：[✓](https://github.com/amazon-science/icr-kv-caching-long-context-llms) ・ リポジトリ内被引用：1  
  長文脈LLMの文脈長が数十万〜100万トークンに伸びても、大量の文書から正しい証拠を見つける能力が必ずしも高いとは限らない。検索拡張生成（Retrieval-Augmented Generation; RAG）は事前に関連文書を検索するため効率的だが、検索索引の構築・運用が必要である。HotpotQA単体では61.0→81.1と20.1ポイント改善した。

- **2026-01 · [Dynamic Thinking-Token Selection for Efficient Reasoning in Large Reasoning Models](2026-2601.18383-dynamic-thinking-token-selection-for-efficient-reasoning-in-large-reason.md)**  
  実装：[✓](https://github.com/Robin930/DynTS) ・ リポジトリ内被引用：1  
  DynTS（動的 Thinking-Token Selection）は、長い思考列を生成する大規模推論モデル（Large Reasoning モデル; LRM）で、最終回答に必要な思考トークンのキー・値キャッシュ（Key-Value キャッシュ; KVキャッシュ）を残し、その他を推論途中に削除する方式である。

- **2025-12 · [Script: Graph-Structured and Query-Conditioned Semantic Token Pruning for Multimodal Large Language Models](2025-2512.01949-script-graph-structured-and-query-conditioned-semantic-token-pruning-for.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  手法は、余弦類似度の二部グラフを用いて冗長な視覚トークンを削るグラフ構造化枝刈り（Graph-Structured Pruning; GSP）と、質問との関連性に加えて特徴の多様性を考慮する質問条件付き意味枝刈り（Query-Conditioned Semantic Pruning; QCSP）から成る。

- **2025-12 · [Rethinking Chain-of-Thought Reasoning for Videos](2025-2512.09616-rethinking-chain-of-thought-reasoning-for-videos.md)**  
  実装：[✓](https://github.com/LaVi-Lab/Rethink_CoT_Video) ・ リポジトリ内被引用：1  
  本論文は、長い人間風の思考列が動画理解に必須かを疑い、短い推論文、視覚トークン圧縮、強化学習による事後学習を組み合わせる代替構成を検証する。

- **2025-12 · [MatKV: Trading Compute for Flash Storage in LLM Inference](2025-2512.22195-matkv-trading-compute-for-flash-storage-in-llm-inference.md)**  
  実装：[✓](https://github.com/kunwooshin/MatKV) ・ リポジトリ内被引用：1  
  MatKVは、検索拡張生成（Retrieval-Augmented Generation、RAG）の質問ごとに同じ文書を何度もGPUで事前処理する無駄を、文書単位の鍵・値（KV）キャッシュをストレージへ永続化することで減らす方式である。

- **2025-12 · [LLMCache: Layer-Wise Caching Strategies for Accelerated Reuse in Transformer Inference](2025-2512.16843-llmcache-layer-wise-caching-strategies-for-accelerated-reuse-in-transfor.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LLMCacheは、入力文字列が完全一致しなくても意味的に似ていればTransformer内部の中間活性を再利用できると考え、各層の出力を入力の指紋とともに保存する推論方式である。

- **2025-12 · [Hybrid Token Compression for Vision-Language Models](2025-2512.08240-hybrid-token-compression-for-vision-language-models.md)**  
  実装：[✓](https://github.com/jushengzhang/HybridToken-VLM) ・ リポジトリ内被引用：1  
  一方、離散量子化した符号だけでは姿勢・質感・細部の変化が失われやすい。一次論文v2の7種類の画像理解評価では、無圧縮モデルを上限、学習しない1トークン圧縮を下限とする正規化性能保持率が87.2%であり、連続圧縮方式VoCo-LLaMAの81.0%を上回る。

- **2025-12 · [From Context to EDUs: Faithful and Structured Context Compression via Elementary Discourse Unit Decomposition](2025-2512.14244-from-context-to-edus-faithful-and-structured-context-compression-via-ele.md)**  
  実装：[✓](https://github.com/DeepLangAI/LingoEDU) ・ リポジトリ内被引用：1  
  LingoEDUは、長い文章を単純にトークン単位で間引くのではなく、まず原文の談話構造を木として抽出し、その木から質問に必要な範囲だけを選択して入力を短縮する、明示的な文脈圧縮方式である。著者は248文書を人手で構造注釈したStructBenchを公開し、木編集距離4.77、文書単位完全一致率49.60%を報告した。

- **2025-12 · [Asynchronous Reasoning: Training-Free Interactive Thinking LLMs](2025-2512.10931-asynchronous-reasoning-training-free-interactive-thinking-llms.md)**  
  実装：[✓](https://github.com/yandex-research/AsyncReasoning) ・ リポジトリ内被引用：1  
  推論時計算を増やすほど対話の即応性が下がるという問題である。二つの流れがそれぞれ通常の「入力→思考→回答」という順序で文脈を見ているように、鍵・値キャッシュ（KV キャッシュ）の論理的な並びを切り替える。

- **2025-11 · [Thinking with Drafts: Speculative Temporal Reasoning for Efficient Long Video Understanding](2025-2512.00805-thinking-with-drafts-speculative-temporal-reasoning-for-efficient-long-v.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長い動画の質問応答では、最初に少数のフレームを見て全体を把握し、必要な時間区間を細かく調べる「フレームを見ながら考える」方式が使われる。原著の観測では、動画トークンに対する注意スコアの90%以上が 10^-3 未満で、密に読み込んだフレームには冗長な情報が多い。

- **2025-11 · [Rotate, Clip, and Partition: Towards W2A4KV4 Quantization by Integrating Rotation and Learnable Non-uniform Quantizer](2025-2502.15779-rotate-clip-and-partition-towards-w2a4kv4-quantization-by-integrating-ro.md)**  
  実装：[✓](https://github.com/songsm921/RCP) ・ リポジトリ内被引用：1  
  重みを二ビット、活性値とキャッシュを四ビットにする極端な量子化では、単純な事後量子化や従来の量子化認識学習だけでは予測が崩れる場合がある。ピークメモリは13.48GBから2.55GBへ減り、約5.29倍の削減となる。

- **2025-11 · [Mitigating Sequential Dependencies: A Survey of Algorithms and Systems for Generation-Refinement Frameworks in Autoregressive Models](2025-d5b03c1b33e0-mitigating-sequential-dependencies-a-survey-of-algorithms-and-systems-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  対象は、草案トークンを安く先読みし、より高品質なターゲットモデルで検証する投機的復号だけでなく、複数位置を仮置きして反復修正するJacobi型方式や、検索・n-gramによる草案再利用まで含む。付録A1では公開実装を用い、単一NVIDIA A100 80GB、バッチ1、貪欲復号という条件で11方式を六課題比較した。

- **2025-11 · [DeCoRL: Decoupling Reasoning Chains via Parallel Sub-Step Generation and Cascaded Reinforcement for Interpretable and Scalable RLHF](2025-2511.19097-decorl-decoupling-reasoning-chains-via-parallel-sub-step-generation-and-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  DeCoRLは、長い推論手順を単一の大規模言語モデル（LLM）が順番に生成する代わりに、役割の異なる小さな推論モジュールへ分解して同時に実行し、出力を統合する枠組みである。著者はNVIDIA A100を使った10段階の推論問題で、逐次実行1,202ミリ秒に対してDeCoRLが316ミリ秒となり、約3.8倍高速化したと報告する。

- **2025-11 · [CLaRa: Bridging Retrieval and Generation with Continuous Latent Reasoning](2025-2511.18659-clara-bridging-retrieval-and-generation-with-continuous-latent-reasoning.md)**  
  実装：[✓](https://github.com/apple/ml-clara) ・ リポジトリ内被引用：1  
  CLaRa（Continuous Latent Reasoning）は、文書を少数の連続値メモリトークンへ圧縮し、その表現を文書検索と生成の双方に用いる。Mistral-7Bで16倍圧縮したSCPは、4質問応答課題の通常検索条件において平均CEM 38.96%を記録し、PISCOの37.83%を上回る。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-10 · [TopK-Guided: Adaptive, Budget-Aware Activation Sparsity for Efficient LLM Inference](2026-2610.01763-topk-guided-adaptive-budget-aware-activation-sparsity-for-efficient-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  両手法はさらにTransformer層間へ一様な疎性予算を与え、疎化への耐性が異なる層を区別しない。論文のC4評価では、Llama-2-7BとLlama-3-8Bの目標疎性30%、50%、70%で、TopK-GuidedはTEALおよびWINAと比べperplexityと8課題平均正解率の両方で全条件最高だった。

- **2026-10 · [The Devil Is in the Reconstruction Loss Scale: Rethinking Optimization in LLM Quantization](2026-2610.00983-the-devil-is-in-the-reconstruction-loss-scale-rethinking-optimization-in.md)**  
  実装：[✓](https://github.com/IntelChina-AI/RMSE) ・ リポジトリ内被引用：0  
  この論文は、学習済み大規模言語モデルを小さな校正データだけで低ビット化する学習後量子化（post-学習 量子化; PTQ）の最適化損失に焦点を当てる。

- **2026-10 · [Spend Bytes on Breadth: Precision–Count Trade-offs for Decode-Time KV Compression in Long Chain-of-Thought Reasoning](2026-2610.05685-spend-bytes-on-breadth-precision-count-trade-offs-for-decode-time-kv-com.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  古いデコード KVをKIVI形式で2、3、4ビット量子化し、直近128トークンはfp16に残す。3モデル、複数の数学・科学ベンチマーク、2予算の計18条件では、BreadthKVがfp16のSnapKV-D 追い出しより17条件で正答率が高く、16条件で95%信頼区間が0を除く。

- **2026-10 · [SEIS: Self-Evolving Inference Systems](2026-2610.04646-seis-self-evolving-inference-systems.md)**  
  実装：[✓](https://github.com/smth-fun/self-evolving-inference-system) ・ リポジトリ内被引用：0  
  個別のGPUカーネルだけを最適化するのではなく、モデル層、正規化、量子化、注意計算、KVキャッシュ、CPU側のスケジューラ、CUDAグラフ、トークン選択、投機的復号までを同じ目的関数のもとで改修する。中心実験では、Qwen3-0.6BをNVIDIA H100 80GBの単一GPUで、単一要求の貪欲復号として実行する。

- **2026-10 · [MOIRA: Mass-Oriented Indexing with Ragged Attention for Long-Context Decoding](2026-2610.04313-moira-mass-oriented-indexing-with-ragged-attention-for-long-context-deco.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  可変予算方式では選択後のページリストが不均一長となり、従来のFlashAttention-3（FA3）やFlashInferの分割スケジューラに余分なパディング、ブロック負荷偏り、CPUでの再計画が発生する。

- **2026-10 · [Decoupled Contrastive Decoding via Expert-Aligned Drafting](2026-2608.12913-decoupled-contrastive-decoding-via-expert-aligned-drafting.md)**  
  実装：[✓](https://github.com/chadlzx/dcd) ・ リポジトリ内被引用：0  
  重要なのは「対比分布を軽量器で近似すること」ではなく、ドラフト器を検証の正しさから分離することにある。

- **2026-09 · [XOR-Trellis: Ultra-Low-Complexity Dequantization and Curvature-Aware Hadamard-Free LLM Quantization](2026-2610.00432-xor-trellis-ultra-low-complexity-dequantization-and-curvature-aware-hada.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  2ビット前後まで重みを圧縮すると、重み転送量は小さくなる一方で、単純なスカラー量子化では量子化誤差が大きくなる。復元は約14個の2入力XORゲートと固定された4×4の小さな候補表で表現できる。

- **2026-09 · [Unlocking Lossless Speedups in LLMs via Discrete Diffusion](2026-2609.04010-unlocking-lossless-speedups-in-llms-via-discrete-diffusion.md)**  
  実装：[✓](https://github.com/ifm-ai/uno) ・ リポジトリ内被引用：0  
  元の自己回帰モデル分布を保ったまま追加した離散拡散重みで複数トークンを並列提案し、専用サンプラで正しく補正して、逐次デコードの重み読出し回数を減らす。

- **2026-09 · [Unleashing the Power of Equality Saturation for Tensor Program Superoptimization](2026-2609.12330-unleashing-the-power-of-equality-saturation-for-tensor-program-superopti.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  特定の注意機構パターンを手書きで登録するのではなく、softmaxの依存関係を修復しながらreductionを融合する規則から、online softmaxを含む融合カーネルを導くことができる。

- **2026-09 · [Toward Sustainable Distributed LLM Inference: A Systems Synthesis and Research Agenda for an Energy-, Carbon-, and Cache-Aware llm-d Control Plane](2026-2609.05565-toward-sustainable-distributed-llm-inference-a-systems-synthesis-and-res.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、LLM推論の省エネルギー化を単一のGPUカーネルや量子化手法に閉じず、分散サービングの制御面（control plane）が担う複合意思決定として再定義するシステムサーベイ兼研究課題提案である。原著の表にある2〜4倍の処理量等はPagedAttentionなど引用元の既存研究の数値であり、SICPを動かした結果ではない。

- **2026-09 · [ThinQuant: Scalable Rotation Learning for Weight and Activation Quantization of LLMs](2026-2609.36120-thinquant-scalable-rotation-learning-for-weight-and-activation-quantizat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低ビット量子化では、重みと活性の外れ値が量子化範囲を広げ、通常の小さい値に割り当てられる表現精度を低下させる。Llama-3-70BのW4A4KV4ではDartQuantのWikiText-2困惑度7.55に対して5.63へ改善し、校正時間は111分から11分57秒へ、保存データは960GiBから0.51GiBへ削減する。

- **2026-09 · [STEPQuant: When and Where Errors Matter in Delta-Rule Recurrent State Quantization](2026-2609.38169-stepquant-when-and-where-errors-matter-in-delta-rule-recurrent-state-qua.md)**  
  実装：[✓](https://github.com/Dreamer-Toby/STEPQuant) ・ リポジトリ内被引用：0  
  Gated DeltaNetやKimi Delta 注意機構の状態は通常FP32で保持され、要求ごとに持続するため、重みを4ビットへ圧縮した後は状態プールの容量がサービングの律速となり得る。

- **2026-09 · [StepPrune: Adaptive Sequential Visual Token Selection across Multimodal Large Language Models](2026-2609.13804-stepprune-adaptive-sequential-visual-token-selection-across-multimodal-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  多くの視覚言語モデルは、画像エンコーダが生成した数百〜数千個の視覚トークンをテキスト指示の前へ付けてLLMに入力する。これらの視覚prefixはプリフィルで全層を通るため、視覚側の冗長性が大きいと推論計算とKV容量の双方に負担をかける。StepPruneは視覚トークン保持を逐次的な意思決定問題として定義する。

- **2026-09 · [SpliTEE: Improving LLM Inference on Trusted Hardware with Differentially Private GPU Outsourcing](2026-2609.15039-splitee-improving-llm-inference-on-trusted-hardware-with-differentially-private-gpu-outsourcing.md)**  
  実装：[✓](https://github.com/DPVault/SpliTEE) ・ リポジトリ内被引用：0  
  TEE内のLLM線形演算を差分プライバシーで保護してGPUへ委譲し、プロンプト漏洩を抑えつつCPU-only TDX推論を約2倍高速化する。

- **2026-09 · [SMat-Attention: Structured Long-Context Sequence Modeling](2026-2609.36062-smat-attention-structured-long-context-sequence-modeling.md)**  
  実装：[✓](https://anonymous.4open.science/r/smat_attention/README.md) ・ リポジトリ内被引用：0  
  SMat-注意機構は、過去へのアクセスを「任意の過去トークン」か「全履歴を一つに要約」かの二択とせず、選択できる過去トークン集合の組合せ的な豊かさをVC次元dで制御する。実験では、Mamba-2やGated DeltaNetに学習可能なプロフィールと4つの要約読出しを追加し、複数キー検索で精度を改善した。

- **2026-09 · [Signed Rescue Routing: Harm-Aware Cascades for Efficient LLM Inference](2026-2609.07786-signed-rescue-routing-harm-aware-cascades-for-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（Large Language モデル; LLM）の多段推論では、全問い合わせを高価な大型モデルへ送る代わりに、まず小型モデルで回答し、難しいと判断したものだけ大型モデルへ送る。大型モデルの呼出し回数に予算があるとき、純利得が大きい問い合わせから優先して切り替える。

- **2026-09 · [SemBridge: Compiling Consumer Observations into Cross-Stack Communication Plans](2026-2609.08231-sembridge-compiling-consumer-observations-into-cross-stack-communication-plans.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  異種CUDA/NCCL–CANN/HCCL境界で消費者が必要とする観測結果を型付き契約へコンパイルし、不要な全logit転送をトークン投影へ縮約して結果通信を99.97%以上削減する通信計画器。

- **2026-09 · [Reciprocal Guidance: Orchestrating Draft and Verify Budgets for Advancing the Diffusion-AR Self-Speculation Frontier](2026-2609.34388-reciprocal-guidance-orchestrating-draft-and-verify-budgets-for-advancing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Reciprocal Guidance（RecGuide）は、拡散型ドラフトと自己回帰検証を同一の大規模言語モデルで実行する自己投機的復号に対し、同時実行負荷に応じて二つの制御方式を使い分ける推論ランタイムである。

- **2026-09 · [QuLoC: Photonic Quantum-Assisted Low-Rank LLM Compression](2026-2609.40146-quloc-photonic-quantum-assisted-low-rank-llm-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの線形射影行列を特異値分解（singular value decomposition; SVD）して小さな二つの行列へ置き換える低ランク圧縮は、重み数と行列演算量を削減できる。Qwen3.5-4Bの言語モデル部分のパラメータを20.05%減らした条件で、六つの下流課題の平均精度はSwift-SVDの49.24%から54.03%へ上昇した。

- **2026-09 · [Quantization Error Is Spectrally Flat: A Single Random Probe Is a Calibrated, Data-Free Sensitivity Estimator, with Application to Budget-Targeted Mixed-Precision Quantization at 400B Scale](2026-2609.33923-quantization-error-is-spectrally-flat-a-single-random-probe-is-a-calibra.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模LLMを低ビット量子化する際、すべての重みを同じビット幅にするより、精度劣化に敏感なテンソルを高ビット、耐性のあるテンソルを低ビットにした方が、同じ容量予算で品質を維持できる可能性がある。

- **2026-09 · [PQ-HSA: Reusing Product-Quantized Scores for Hybrid Sparse-Approximate Attention](2026-2609.33746-pq-hsa-reusing-product-quantized-scores-for-hybrid-sparse-approximate-at.md)**  
  実装：[✓](https://github.com/KunmingSHAO/pqhsa_release) ・ リポジトリ内被引用：0  
  PQ-HSAは、積量化（PQ）で圧縮したキーを全件走査して近似logitを求め、そのスコアを上位KVの選択だけでなく、非選択KVの背景寄与の推定にも使う。

- **2026-09 · [Post-Training Ternarization of Qwen3-4B: Capability, Effective Bit Budget, Storage Compression, and Deployment](2026-2609.01962-post-training-ternarization-of-qwen3-4b-capability-effective-bit-budget-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Qwen3-4Bの線形重み81.62%を既存の回転・残差三値化・誤差補償で事後変換し、対象重みの実効1.641ビット、保存容量8.29→3.96GiBを実証。圧縮、能力保持、実行速度を分離して検証する。

- **2026-09 · [One Distribution, Two Channels: Coverage-Calibrated KV Retention and Compensation](2026-2610.02235-one-distribution-two-channels-coverage-calibrated-kv-retention-and-compe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈推論ではKVキャッシュがメモリ容量と読み出し帯域を圧迫する。トークンを単純に重要度順で保持する方式では、重要度の高いトークンが互いに似ている場合に貴重な保持枠を浪費する。RULERでは90% KV圧縮時に最良比較方式を平均2.25ポイント、最大3.78ポイント上回り、複数回の再圧縮やLongBenchでも優位性を報告する。

- **2026-09 · [MoRA: MoE Pruning via Router Bias Learning and Expert Approximation](2026-2610.00367-mora-moe-pruning-via-router-bias-learning-and-expert-approximation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoRA（MoE Pruning via ルーティング Bias Learning and 専門家 Approximation）は、混合専門家（Mixture of エキスパート; MoE）型大規模言語モデルで、推論時に保持する専門家（専門家）の数を減らしながら、元モデルの生成品質をできるだけ保つ構造的な枝刈り方式である。

- **2026-09 · [Mid-Harness: Scaling Actions Between Model and Harness for Terminal Agents](2026-2609.39982-mid-harness-scaling-actions-between-model-and-harness-for-terminal-agent.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末エージェントは、言語モデルが提案したコマンドやファイル変更を実行環境へ送る。単一候補を実行する基準のPass@1は50.00%。

- **2026-09 · [LeanStream: A Speculate-and-Refine Streaming Framework for Efficient on-Device LLM Inference](2026-2609.03079-leanstream-speculate-refine-on-device.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LeanStreamは、層内の部分残差から次層の重み優先度を更新し、重み読出し・GPU計算・キャッシュを非同期に重ねて、端末LLMのSSD待ちと予測ミスを減らす。

- **2026-09 · [IHS-LM: Intra-batch Hybrid Scheduling and Layer Migration for VLM Pipeline Inference Acceleration on Edge Devices](2026-9b405eddeda4-ihs-lm-intra-batch-hybrid-scheduling-and-layer-migration-for-vlm-pipeline-inference-acceleration-on-edge-devices.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KV容量連動のプリフィル/デコード混在スケジューリングと帯域感知型の境界層移行を統合し、異種Jetson上のVLM推論遅延を最大17.5%削減する。

- **2026-09 · [HEAT: Faster Fully Homomorphic Inference via Approximations-Weights Co-Adaptation](2026-2609.01730-heat-faster-fully-homomorphic-inference-via-approximations-weights-co-ad.md)**  
  実装：[✓](https://github.com/gladia-research-group/heat) ・ リポジトリ内被引用：0  
  対象は通常のGPU推論全般ではなく、暗号文上で加算・乗算・回転を組み合わせてTransformerを評価する、非常に高コストなプライバシー保護推論である。ただし比較する平文モデルは各方式の「自分自身の平文版」であり、同一平文モデルへの忠実度を直接比較した値ではない。

- **2026-09 · [Green AI: Cost of LLM-Based Code Completion](2026-2609.33918-green-ai-cost-of-llm-based-code-completion.md)**  
  実装：[✓](https://doi.org/10.5281/zenodo.21971227) ・ リポジトリ内被引用：0  
  コード補完のためにLLMをローカル実行する場合、モデルの正答率や生成速度だけでなく、入力文脈を処理するためのGPUエネルギーと、出力を逐次生成するためのGPUエネルギーを分けて評価する必要がある。量子化モデル、とくにQ4は同一モデル系のFP16に比べて省エネルギーな傾向があり、品質とエネルギーのPareto前線へ頻繁に現れる。

- **2026-09 · [From Position Risks to Block Survival: Faster Generation for Diffusion Language Models](2026-2609.33390-from-position-risks-to-block-survival-faster-generation-for-diffusion-la.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデル（DLM）は複数の将来トークンを並列に提案できるため、自己回帰生成より少ないモデル評価回数で長い出力を作れる可能性がある。arXiv:2609.33390の原著ではI-DLM 8B/32Bを対象に、H200上の18条件で同規模I-DLM比の生成スループットを8Bで幾何平均22.7%、32Bで29.8%改善する。

- **2026-09 · [FoldAttention: Declared-Reference Softmax for Fast Decode and Deterministic Backward](2026-2609.33410-foldattention-declared-reference-softmax-for-fast-decode-and-determinist.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈の自己回帰デコードでは、次の一トークンを作るたびに伸び続けるKVキャッシュを参照する。後方計算では、CTAごとの部分勾配を共通整数格子へ丸めて加算することで、加算順序に依存しない決定的な勾配を得る。

- **2026-09 · [Fengshui: Demystifying Chiplet Ecosystem and Bespoke Neural Network Accelerator Codesign](2026-2609.10970-fengshui-chiplet-neural-accelerator-codesign.md)**  
  実装：[✓](https://github.com/CrucibleComputingGroup/fengshui) ・ リポジトリ内被引用：0  
  再利用可能な少数チップレット群そのものと演算子単位の専用アクセラレータ構成を共同探索し、計算データフロー・メモリ・並列方式・配置配線を演算子ごとに最適化してNREを抑えつつLLM推論のエネルギー効率を高める。

- **2026-09 · [Dynamic Semantic Compression for Efficient Latent-Space Inference in Large Language Models](2026-2609.15338-dynamic-semantic-compression-latent-space-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文を長さに応じて1〜3区間へ分割し、重要トークンを重み付けした潜在表現を生成・復号するDSEI。固定文圧縮より品質を改善し、トークン単位推論より系列長とメモリ負荷を削減する。

- **2026-09 · [Distance-KV: Exploiting Relative Distance for Efficient Long-Context Inference](2026-2609.32663-distance-kv-exploiting-relative-distance-for-efficient-long-context-infe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  復号時の注意演算は過去のKVを繰り返し参照するため、メモリ容量と帯域がボトルネックになる。既存の圧縮方式には、最近のトークンだけを残す方式、注意重みで重要トークンを選ぶ方式、層や注意ヘッドごとに異なる保持予算を割り当てる方式がある。

- **2026-09 · [DimPO: Dimensionality Reduction for Attention using Preference Optimization](2026-2609.32579-dimpo-dimensionality-reduction-for-attention-using-preference-optimizati.md)**  
  実装：[✓](https://github.com/lanzv/dimpo) ・ リポジトリ内被引用：0  
  DimPOは、大規模言語モデル（LLM）の注意計算におけるクエリとキーのベクトル次元を縮める際、元の注意重みを数値的に完全再現することと、モデルの下流課題性能を保つことは別の目的だと実証する研究である。提案は、事前学習済みモデルを追加学習し直す方式ではなく、各層に一つの小さな線形写像をオフラインで学習する方式である。

- **2026-09 · [Compression Beyond the Uncompressed: A Two-Stage Training Recipe for Soft Context Compression in RAG](2026-2609.05152-compression-beyond-the-uncompressed-a-two-stage-training-recipe-for-soft.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  soft context compressionは文書を短い連続embeddingへ置き換え、デコーダがそのembeddingから回答する方式である。教師の失敗を模倣せず、結果報酬から改善を探索する点が重要である。

- **2026-08 · [VoiceMem: Streaming Dual-Brain Memory for Real-Time Interaction](2026-2608.26005-voicemem-streaming-dual-brain-memory-for-real-time-interaction.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  VoiceMemは、音声対話システムの過去会話記憶を、応答を遅らせずに少数の関連記憶へ絞るための索引・更新・検索方式である。

- **2026-08 · [Unifying Depth and Width Pruning for LLMs via Binary Knapsack Optimization](2026-2608.12953-unifying-depth-and-width-pruning-for-llms-via-binary-knapsack-optimizati.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの構造化枝刈りは、注意ブロック、MLP、層、チャネルなど、行列の形状を維持できるまとまった単位を取り除く。

- **2026-08 · [TurboBus: Pooling PCIe Bandwidth for LLM Workloads via Scale-Up Fabrics](2026-2fe550669a96-turbobus-pooling-pcie-bandwidth-for-llm-workloads-via-scale-up-fabrics.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU間高速ファブリックを中継路として他GPUの空きPCIeリンクを借用し、モデル読込の初回トークン待ち時間を最大40%削減、鍵値退避推論を最大1.6倍高速化する。

- **2026-08 · [Training-Free Hashing-Based Attention via Binary Principal Components](2026-2608.04405-training-free-hashing-based-attention-via-binary-principal-components.md)**  
  実装：[✓](https://github.com/yudaohai666/BPC) ・ リポジトリ内被引用：0  
  入力が数万〜数十万トークンに伸びると、GPUの演算器よりもメモリ帯域が律速になりやすい。射影後の問い合わせを符号と7ビットの絶対値へ量子化し、XOR、AND、ビット個数計数とシフトで大量の鍵候補を走査する。長文脈・バッチ2の生成スループットはFlashAttention-2比で最大3.56倍、128K・バッチ16では5.04倍を報告する。

- **2026-08 · [TailSieve: Partial-Rollout-Guided Tail Routing for LLM Rollouts](2026-2608.22788-tailsieve-partial-rollout-guided-tail-routing-for-llm-rollouts.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TailSieveは、以前の部分生成で時間切れとなったプロンプト群を、追加の長さ予測モデルなしで長尾候補として選び、長尾専用プールと通常プールへ割り当てる。

- **2026-08 · [Speculative Probing: LLM Monitoring at Speculative-Decoding Cost](2026-2608.28099-speculative-probing-llm-monitoring-at-speculative-decoding-cost.md)**  
  実装：[✓](https://github.com/collinzrj/SpeculativeProbing) ・ リポジトリ内被引用：0  
  大規模言語モデルの推論サービスでは、回答を生成するだけでなく、危険な入力、指示の矛盾、推論の反復、品質の低下を実行中に検知したい場合がある。別の大規模分類モデルを動かせば高い精度が得られる可能性はあるが、モデルを追加で常駐させ、入力全体をもう一度処理する費用が発生する。ただしすべての条件でMULTIMAXより正確なわけではない。

- **2026-08 · [SoftWater: Class-Aware Rate Allocation for Softmax Quantization](2026-2608.12026-softwater-class-aware-rate-allocation-for-softmax-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の事後量子化では中間の線形層を2〜4ビットにしても、この最終出力層だけを16ビットで残すことが多い。例えばLlama-3.2-1Bの出力層は約2.63億パラメータ、モデル全体の21.3%であり、本体を低ビット化すると出力層の相対的な容量負担がさらに増える。

- **2026-08 · [S$^4$R: Selective Sampling, Subspaces, and Sparse Reconstruction for Compressed Long-Context KV Caching](2026-2608.00528-s-4-r-selective-sampling-subspaces-and-sparse-reconstruction-for-compres.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  S4R（Selective Sampling, Subspaces, and Sparse Reconstruction）は、長文脈言語モデルのキー・値（KV）キャッシュを低ランク係数として保持し、復号時には注意計算に重要な位置だけを元の次元へ戻す方式である。RULERで2.5倍圧縮時の平均は93.61、非圧縮93.97、xKV 93.47である。

- **2026-08 · [Router Sensitivity Under Lightweight Fine-Tuning Identifies Prunable Experts in Mixture-of-Experts Models](2026-2608.07890-router-sensitivity-under-lightweight-fine-tuning-identifies-prunable-exp.md)**  
  実装：[✓](https://github.com/ianKa1/MoE_pruning) ・ リポジトリ内被引用：0  
  混合専門家モデル（Mixture-of-Experts; MoE）は、各トークンで一部の専門家しか動かさないため演算量を抑えられるが、選択される可能性のある専門家の重み全体をメモリに保持する必要がある。専門家を丸ごと削除すればGPUメモリを減らせるものの、使用頻度や重みの大きさだけでは重要な専門家を誤って削除し、推論品質が急落することがある。

- **2026-08 · [Rollplex: Cross-Phase GPU Spatial Sharing for Vision Language Model Post-Training](2026-2608.14498-rollplex-cross-phase-gpu-spatial-sharing-for-vision-language-model-post-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案は単なるGPU上の並列カーネル起動ではない。一方、評価に使うH800は80GBである。

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

- **2026-08 · [Maia 200: A Software Defined Dataflow System for Large-scale AI Acceleration](2026-2608.24664-maia-200-a-software-defined-dataflow-system-for-large-scale-ai-accelerat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Maia 200はTSMC 3nmで製造した1400億超のトランジスタを持つSoCで、750Wの熱設計電力（TDP）の下、FP4で10,145 TFLOP/s、FP8で5,072 TFLOP/s、HBM3e帯域7 TiB/sを公称する。

- **2026-08 · [Maglev: Sliding Recurrent Memory](2026-2608.02870-maglev-sliding-recurrent-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  435M規模、学習43.52Bトークン、最大系列長2048という制御された比較で、最良のQ/P分離パラメータ、整合損失重みλ=1は、通常の局所窓Transformerに対してFineWeb-Edu検証のビット/バイト（BPB）を0.7413から0.7251へ低下させ、下流精度平均を54.1から56.4へ改善した。

- **2026-08 · [Learning What to Remember: Test-Time Training via Context Distillation](2026-2608.01672-learning-what-to-remember-test-time-training-via-context-distillation.md)**  
  実装：[✓](https://github.com/dangxingyu/ttcd) ・ リポジトリ内被引用：0  
  通常の全注意（full 注意機構）は長い履歴の情報を参照できる一方、長さに応じて注意計算と鍵・値（KV）キャッシュの費用が増える。760Mパラメータをゼロから学習したモデルのRULER針検索（6課題平均）では、32KトークンでIP-TTTの9.29%に対しIP-TTCDは21.96%。

- **2026-08 · [From Sweep to Seam: Interleaved Cross-Block Post-Training Quantization](2026-2608.09595-from-sweep-to-seam-interleaved-cross-block-post-training-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Interleaved Cross-Block Quantization（ICBQ）は、学習済みLLMの重みを極低ビットへ圧縮する際、隣接Transformerブロックを再構成する最適化窓をどの順序で訪れるかを変更する方式である。

- **2026-08 · [FLINT: Efficiently Leveraging High Bandwidth Flash for Capacity-Scalable LLM Inference Acceleration](2026-2608.25062-flint-efficiently-leveraging-high-bandwidth-flash-for-capacity-scalable-llm-inference-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  高帯域フラッシュを巨大モデル重みの近接容量層として使い、動的読み出し結合・更新隔離・読み出し専用変換表で従来方式比六・二倍の復号処理量を実現する。

- **2026-08 · [Dynamic Multi-Byte Prediction With Hierarchical Language Models](2026-2608.15454-dynamic-multi-byte-prediction-with-hierarchical-language-models.md)**  
  実装：[✓](https://github.com/skai-research/lca-multibyte) ・ リポジトリ内被引用：0  
  モデル内部の圧縮と、外部へ文字列を生成する速度の間にギャップが残る。外部FlexiTokensモデルで検証すると、検証器の出力を保ちながら2.1〜2.3倍の生成スループットが報告される。

- **2026-08 · [CubicQuant: Parametric Non-Uniform Codebooks for High-Throughput LLM Inference with 1-8-Bit Weights](2026-2608.06763-cubicquant-parametric-non-uniform-codebooks-for-high-throughput-llm-infe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究が扱うのは、大規模言語モデル（LLM）の重みをGPUメモリに置き、自己回帰復号の各段階で行列演算に供給する際の表現形式である。提案形式は、1〜8ビットの重み符号を連続したビット列へ保存し、重み群ごとに尺度 s と二つの形状係数 a,b を付加する。

- **2026-08 · [Budget-Aware LLM Quantization and Low-Rank Correction via Information-Guided Subspace Matrices](2026-b373673622df-budget-aware-llm-quantization-and-low-rank-correction-via-information-gu.md)**  
  実装：[✓](https://github.com/sinuofan/IJCAI2026-BALANCER) ・ リポジトリ内被引用：0  
  BALANCERは、限られた記憶容量で大規模言語モデル（LLM）を実行するため、各重み行列の量子化精度と低ランク補正の階数を全モデル共通のビット予算で割り当てる学習不要の圧縮方式である。

- **2026-08 · [Bounded-State Restoration: Decoupling Local Restore Capacity from External LLM State](2026-2608.17826-bounded-state-restoration-decoupling-local-restore-capacity-from-external-llm-state.md)**  
  実装：[✓](https://github.com/StarkLeeSunny/Flexkv-doublenode) ・ リポジトリ内被引用：0  
  外部KV状態の全ヒットを先に把握しつつ、復元はWチャンク窓だけを順次ステージングして解放することで、長大な外部状態とローカル復元メモリを分離する方式。

- **2026-08 · [Beyond Sparse Weights: When Is Attention Compressible?](2026-2608.21541-beyond-sparse-weights-when-is-attention-compressible.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  疎な注意マップだけではKV圧縮を正当化できないことを理論化し、値分散配分と末尾要約を厳密な物理予算で実装するCertKVを提案。

- **2026-08 · [Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory](2026-2608.07169-agent-memory-distillation-empowering-small-llm-agents-with-hierarchical-.md)**  
  実装：[✓](https://github.com/taeilkim2465/agentic_memory_distillation) ・ リポジトリ内被引用：0  
  提案手法AMD（Agent メモリ Distillation）は、教師が成功した道具呼び出し軌跡から、作業全体の戦略を示す作業手順記憶（Workflow メモリ）、実際の道具呼び出し列を示す部分作業記憶（Subtask メモリ）、個別関数の呼び方を示す関数記憶（Function メモリ）を別々に構築する。

- **2026-07 · [What to Keep, What to Forget: A Rate-Distortion View of Memory Compaction in LLMs and Agents](2026-2607.08032-what-to-keep-what-to-forget-a-rate-distortion-view-of-memory-compaction-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVキャッシュ、入力プロンプト、固定長内部状態、エージェント記憶の圧縮を率歪み最適化で統一し、7軸分類とCOMPACT-Benchを提案するサーベイ。RTX 4060・Qwen2.5-1.5Bの参照実験では、KV保持予算約25%未満でneedle検索がほぼ失敗し、反復要約の事実再現率0.33〜0.56に対して検索可能な原文アーカイブは約0.95だった。

- **2026-07 · [Variable Bit-width Quantization: Learning Per-Group Precision for 'Bigger-but-Smaller' Language Models](2026-2607.02893-variable-bit-width-quantization-learning-per-group-precision-for-bigger-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  量子化は重みの容量を減らすが、通常の方法では全重みに同じ4bitや2bitを割り当てる。Gumbel-Softmaxの連続緩和と交互最適化で精度選択を学習すると、グループの69%が1bitへ落ちる一方、最初のMLPブロックや頻出語彙の出力行は高い精度を要求する。

- **2026-07 · [Structured Redundancy Modeling for Efficient Visual Token Pruning in High-Resolution MLLMs](2026-2607.23046-structured-redundancy-modeling-for-efficient-visual-token-pruning-in-hig.md)**  
  実装：[✓](https://github.com/cvsp-lab/SFPruner) ・ リポジトリ内被引用：0  
  後段の言語モデルがそれらすべてを処理すると、注意演算とKVキャッシュの負担が増えるため、重要な視覚トークンだけを残す枝刈りが有効である。Qwen2.5-VL-7Bで平均512トークンを残す条件では、CDPrunerの選択時間112.4msに対し2.5msで、約110msを選択段階から削減する。

- **2026-07 · [ST-Veto: Spatio-Temporal Token Veto for Diffusion MLLMs via Taylor Prediction and Visual Grounding](2026-2607.17884-st-veto-spatio-temporal-token-veto-for-diffusion-mllms-via-taylor-predic.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者が提案する時空間トークン拒否（Spatio-Temporal Token Veto、ST-Veto）は、ある反復で確信度が高くても、その確信度の時間変化が不安定、あるいは画像への注意が弱い候補を一時的に拒否し、条件を満たす別の候補を先に確定させる。

- **2026-07 · [Skip-It? Theoretical Conditions for Layer Skipping in Vision–Language Models](2026-2509.25584-skip-it-theoretical-conditions-for-layer-skipping-in-vision-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の層スキップ手法は、経験的な層番号や余弦類似度などを用いて処理を省略していたが、表現が似ていることと出力品質が保たれることは同義ではない。

- **2026-07 · [SelectInfer: Selective Neuron Loading and Computation for On-Device LLMs](2026-2607.18081-selectinfer-selective-neuron-loading-and-computation-for-on-device-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  オフラインで重要FFNニューロンを選別して必要分だけロードし、入力ごとの活性で計算対象も絞ることで、端末LLMのメモリ量と計算量を独立に調整する方式。

- **2026-07 · [SAB-LVLM: Significance-Aware Binarization for Large Vision-Language Models](2026-2607.01876-sab-lvlm-significance-aware-binarization-for-large-vision-language-model.md)**  
  実装：[✓](https://github.com/LyuQi127/SAB_LVLM) ・ リポジトリ内被引用：0  
  SAB-LVLMは、画像と文章を扱う大規模視覚言語モデル（LVLM）を、重み約1bitの二値化へ圧縮する事後量子化（PTQ）方式である。Qwen2.5-VL-32B-InstructのMMStarは約1bitのARB-LLM48.48点からSAB-LVLM54.77点へ改善し、モデルメモリは10.28GBと報告される。

- **2026-07 · [Resting Neurons, Active Insights: Robustifying Activation Sparsity in LLMs via Spontaneity](2025-2512.12744-resting-neurons-active-insights-improving-input-sparsification-for-large.md)**  
  実装：[✓](https://github.com/hxu105/SPON) ・ リポジトリ内被引用：0  
  TEALなどの活性疎化方式は、小さい入力活性を閾値処理で零にして重み転送と積和を省く。実際にNVIDIA A6000でバッチ1の生成速度を測定し、50%疎化したLlama3-8Bは64.13 トークン/s、Mistral-7Bは71.84 トークン/sであり、TEALの64.28、71.25 トークン/sとほぼ同じだった。

- **2026-07 · [OmniScope: Modality-Decoupled Token Compression for Omnimodal Large Language Models](2026-2607.23193-omniscope-modality-decoupled-token-compression-for-omnimodal-large-langu.md)**  
  実装：[✓](https://github.com/MAC-AutoML/OmniScope) ・ リポジトリ内被引用：0  
  入力を処理する事前充填（プリフィル）では、そのトークン数が注意演算、GPUメモリ、遅延を増やす。既存の音声・映像圧縮には、音声で重要と判断した時間帯を映像側でも重視する方式がある。映像にはアンカー・差分時空間圧縮（Anchor-Delta Spatio-Temporal Compression、AD-STC）、音声には1秒区間内の類似トークン統合を用いる。

- **2026-07 · [Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers](2026-2607.15456-looped-latent-attention-cross-loop-kv-compression-for-looped-transformer.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ループ型Transformerは、同じTransformerブロックを何度も適用することで、モデルの深さに相当する反復計算を少ない重みで実現する。Ouro-1.4Bを用いた同一キャッシュ容量比較では、4倍圧縮のLLAはGSM8K厳密正解率0.800を記録し、教師の0.794とほぼ同等だった。

- **2026-07 · [LaCo: Layer-wise Compensation for Pruned Large Language Models](2026-00140e8efcf4-laco-layer-wise-compensation-for-pruned-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LaCo（層-wise Compensation）は、枝刈りによって一部の重みや層内構造を削除したLLMの性能を、元モデルの各層の隠れ状態へ順次近づける局所回帰で回復する方法である。

- **2026-07 · [Kairox: Adaptive GPU-CPU Hybrid LLM Inference via Online Neuron Balancing](2026-58b45f0ef5d5-kairox-adaptive-gpu-cpu-hybrid-llm-inference-via-online-neuron-balancing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  巨大な言語モデルでは重みをVRAMにすべて置けない場合、llama.cppの層単位オフロードではCPU側の層計算が直列経路の律速になりやすい。RTX 3080 Ti 12GBとRTX 4090 24GBを用いた実機で、活性化疎性を持つ複数の7B～66B級モデルを評価した。

- **2026-07 · [I/o for LLM inference: a survey of storage and memory bottlenecks](2026-5e022a2789e7-i-o-for-llm-inference-a-survey-of-storage-and-memory-bottlenecks.md)**  
  実装：[✓](https://github.com/rch0wdhury/llm-io-profiler) ・ リポジトリ内被引用：0  
  LLMデコードのデータ移動を重み・KVキャッシュ・活性の三I/O流へ分解し、量子化からSSD/CXL/統合メモリまでをルーフライン上で統一して、最適化を積むと支配ボトルネックが移動することを定量化したサーベイ。

- **2026-07 · [GyRot: Leveraging Hidden Synergy between Rotation and Fine-grained Group Quantization for Low-bit LLM Inference](2026-2607.27694-gyrot-leveraging-hidden-synergy-between-rotation-and-fine-grained-group-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GyRotは、重み・活性化を4ビットに圧縮したLLMを精度よく、しかも整数演算中心の専用回路で実行するためのアルゴリズムとハードウェアの共同設計である。回路性能は28nm・1GHz条件の合成・推定に基づき、Tender比の幾何平均で速度3.40倍、エネルギー効率3.64倍と報告する。

- **2026-07 · [FlashRT: Agent Harness for Guiding Agents to Deploy Real-Time Multimodal Applications](2026-2607.18171-flashrt-agent-harness-for-guiding-agents-to-deploy-real-time-multimodal-.md)**  
  実装：[✓](https://github.com/Infini-AI-Lab/FlashRT) ・ リポジトリ内被引用：0  
  単体モデルのカーネルを高速化するだけでは、どの段階をどのGPUへ配置し、いつ出力を小分けで次段へ渡し、どの段階の永続状態を共有できるかというアプリケーション全体の最適化は解けない。

- **2026-07 · [Enabling Spatially Fine-Grained DVFS in Neural Processing Units for Energy-Efficient LLM Serving](2026-2607.16473-enpu-component-level-dvfs-npu-llm-serving.md)**  
  実装：[✓](https://github.com/google-coral/coralnpu（ベースコア）。eNPUの改変実装・シミュレータの公開URLは一次資料に記載なし。) ・ リポジトリ内被引用：0  
  eNPUは、演算器・SRAM・HBM・接続を別電圧周波数領域に分け、非同期転送と演算子別計画をSLO余裕で切替えて、NPUサービングの非ボトルネック電力を落とす。

- **2026-07 · [CXL-CCL: Inter-Node Collective GPU-Communication Using a CXL Shared Memory Pool](2026-fab14a584908-cxl-ccl-inter-node-collective-gpu-communication-using-a-cxl-shared-memory-pool.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CXL共有メモリをノード間GPU集団通信の媒体として使い、データ配置・細粒度重畳・ドアベル同期でRDMA型通信に対する性能とコストを改善する。

- **2026-07 · [CRISP: Pre-LLM Yet Text-Driven Visual Token Pruning for Efficient LVLM Inference](2026-2607.16326-crisp-pre-llm-yet-text-driven-visual-token-pruning-for-efficient-lvlm-in.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  学習を追加せず、言語モデルの層内注意重みを取り出さないことが設計上の要点である。原著の表IではLLaVA-1.5-7Bの視覚トークンを576個から128個（77.8%削除）へ減らしても、報告された平均性能保持率は99.5%である。

- **2026-07 · [Constrained Decoding for Diffusion Language Models via Efficient Inference over Finite Automata](2026-2607.07026-constrained-decoding-for-diffusion-language-models-via-efficient-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DangとErmonは、生成時に課す制約を有限オートマトン（finite automaton）へ変換し、拡散モデルの各位置に対する予測分布とオートマトンの受理経路を結合する。制約を満たすかどうかを生成後に判定して捨てる拒否標本化とは異なり、無効な系列へ確率を割り当てない点が中心的な貢献である。

- **2026-07 · [COMPEL: Compensated Mixture-of-Experts Pruning with Expert-Layer distribution](2026-092a8a151f95-compel-compensated-mixture-of-experts-pruning-with-expert-layer-distribu.md)**  
  実装：[✓](https://github.com/seohee0925/COMPEL) ・ リポジトリ内被引用：0  
  COMPEL（Compensated Mixture-of-Experts Pruning with 専門家-層 distribution）は、混合専門家モデル（MoE）の全エキスパートを推論時に保持するメモリ負担を、モデルの各層で異なる冗長性を考慮して削減する剪定方式である。

- **2026-07 · [CoMem: Reusing Transformer Depth across Queries with Persistent Intermediate Residuals](2026-2607.28263-comem-reusing-transformer-depth-across-queries-with-persistent-intermedi.md)**  
  実装：[✓](https://github.com/liuhanzuo/Mixture-of-Memory) ・ リポジトリ内被引用：0  
  CoMemはTransformerのどこまでを文書単独で先払い計算するかを新たな制御変数とし、文書の中間残差（residual state）を永続保存して、問い合わせ時は上位層のみ再実行する方式である。

- **2026-07 · [Combating Textual Noise and Redundancy: Entropy-Aware Dense Visual Token Pruning](2026-2607.02484-combating-textual-noise-and-redundancy-entropy-aware-dense-visual-token-.md)**  
  実装：[✓](https://github.com/SJTU-DeepVisionLab/EADP) ・ リポジトリ内被引用：0  
  画像を含むVision-Language モデル（VLM）では、画像エンコーダが作る多数のパッチトークンがLLMの入力を長くし、事前充填の注意演算とメモリ転送を増やす。EADP（Entropy-Aware Dense Pruning）はこの二段階の失敗を分離する。

- **2026-07 · [CLIP Tricks You: Training-free Token Pruning for Efficient Pixel Grounding in Large Vision-Language Models](2026-2605.13178-clip-tricks-you-training-free-token-pruning-for-efficient-pixel-groundin.md)**  
  実装：[✓](https://github.com/sejong-rcv/LiteLVLM) ・ リポジトリ内被引用：0  
  一般的な画像理解向け視覚トークン枝刈りは、画像の全体表現への寄与や画像・テキストの高い類似度を手掛かりにトークンを残す。GLaMMの元の576視覚トークンを192に削減したとき、8評価分割平均の領域分割指標は75.5から68.1となり、元性能の90.3%を維持した。

- **2026-07 · [Capturing Token Tendencies for Training-Free Token Pruning in Multimodal Large Language Models](2026-2607.28341-capturing-token-tendencies-for-training-free-token-pruning-in-multimodal.md)**  
  実装：[✓](https://github.com/JieMaMagic/Trend-aware-Pruning) ・ リポジトリ内被引用：0  
  本論文は、多モーダル大規模言語モデル（Multimodal Large Language モデル、MLLM）の推論時に、画像由来の視覚トークンを削減する学習不要の手法を提案する。LLaVA-v1.5-7Bの実験では、初期保持288/576トークンの条件で平均相対性能98.89%を維持し、計算量を元の55.10%へ削減した。

- **2026-07 · [Beyond Activation Alignment: The Alignment-Diversity Tradeoff in Task-Aware LLM Quantization](2026-2607.00908-beyond-activation-alignment-the-alignment-diversity-tradeoff-in-task-awa.md)**  
  実装：[✓](https://github.com/WangFei-2019/TASA) ・ リポジトリ内被引用：0  
  TASA（Task-Aware Sensitivity Analysis）は、LLMの重みを低ビットへ圧縮するとき、どの層へ何ビット割り当てるかを単一の言語モデル損失だけで決めない方式である。LLaMA-3-8Bでは平均3.5ビットで7タスク平均68.9%、HQQ W4の68.1%とRTN W4の67.9%を上回るが、AWQ W4の69.4%は下回る。

- **2026-07 · [Back from the Future: Key-Value Cache Management by Counter-Causal Surprise](2026-2607.27600-back-from-the-future-key-value-cache-management-by-counter-causal-surpri.md)**  
  実装：[✓](https://github.com/metacognitionai/counter_causal) ・ リポジトリ内被引用：0  
  従来のスライディングウィンドウは古いトークンを機械的に捨て、H2Oなどのheavy-hitter方式は過去に多く注意されたトークンを残す。Qwen2.5-7B、RTX4090のキャッシュ更新1回では、KV長512で54msから7.9ms、4096で496msから52.6msとなり、更新処理単体で7～9倍速くなる。

- **2026-07 · [A Hippocampus for Linear Attention: An Exact Memory for What the Recurrent State Forgets](2026-2607.02303-a-hippocampus-for-linear-attention-an-exact-memory-for-what-the-recurren.md)**  
  実装：[✓](https://github.com/scale-lab-ai/HOLA) ・ リポジトリ内被引用：0  
  線形注意（Linear 注意機構）や状態空間モデル（State Space モデル; SSM）は、入力履歴を固定長の再帰状態へ要約するため、過去の全トークンに対応する鍵・値キャッシュ（Key-Value キャッシュ; KVキャッシュ）を保存する全注意と比べて、長文脈の記憶容量を一定に保ちやすい。

- **2026-07 · [3DLS: A 3D Logic-Stacked Architecture for Disaggregated LLM Serving](2026-2607.01617-3dls-disaggregated-serving-interconnect.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル→デコードのKV転送とデコード側テンソル並列AllReduceを同じ横方向リンクで競合させず、KVだけを3D縦リンクへ物理分離するチップレット構成。等帯域条件でも最大1.49倍のスループットと60.2%の遅延削減を示す。

- **2026-06 · [Understanding Evaluation Illusion in Diffusion Large Language Models](2026-2606.29228-understanding-evaluation-illusion-in-diffusion-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は新しい復号器の提案ではなく、既存の復号方式を同じ条件で比較するための評価方法論の研究である。結果は、少し異なるテンプレートを使うだけで方式間の優劣が逆転し、単一テンプレートで測った「品質を維持した高速化」が再現しない場合があるというものだった。

- **2026-06 · [TGV-KV: Text-Grounded KV Eviction for Vision-Language Models](2026-2606.03075-tgv-kv-text-grounded-kv-eviction-for-vision-language-models.md)**  
  実装：[✓](https://github.com/Danielement321/TGV-KV) ・ リポジトリ内被引用：0  
  TGV-KVは、画像と文章を同時に入力する視覚言語モデル（Vision-Language モデル; VLM）の鍵・値キャッシュ（Key-Value Cache; KVキャッシュ）を、文章の意味を優先して削減する手法である。

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

- **2026-06 · [ProbMoE: Differentiable Probabilistic Routing for Mixture-of-Experts](2026-2606.01509-probmoe-differentiable-probabilistic-routing-for-mixture-of-experts.md)**  
  実装：[✓](https://github.com/HengHugoZhao/ProbMoE) ・ リポジトリ内被引用：0  
  ProbMoEはMoEのtop-kルーティングを専門家部分集合の確率分布として定式化し、学習時に確率的に選択した専門家を実行しつつ、集合制約下の厳密な周辺確率を直通勾配の代理に使う。OLMoEのGSMでは従来45.94%に対し50.19%、Qwen1.5-MoEの翻訳では30.00に対し39.23。

- **2026-06 · [P-MTP: Efficient Document Parsing via Multi-Token Prediction with Progressive Depth Scaling](2026-2606.24447-p-mtp-efficient-document-parsing-via-multi-token-prediction-with-progres.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数トークン予測（MTP）を使って将来のトークンを軽量に先読みし、基盤モデルで検証してまとめて確定できれば、同じ意味内容をより少ない大規模推論回数で生成できる。最も大きい5.24倍という数値は、Qwen3-VL-2BでPubTabNetの表解析を行う際の単体復号遅延26.71→5.10の比である。

- **2026-06 · [Orchestra-o1: Omnimodal Agent Orchestration](2026-2606.13707-orchestra-o1-omnimodal-agent-orchestration.md)**  
  実装：[✓](https://github.com/zfkarl/Orchestra-o1) ・ リポジトリ内被引用：0  
  Orchestra-o1は、文字・画像・音声・動画が同時に含まれる複雑な質問を、主エージェント（MainAgent）が複数の部分課題へ分解し、専門の副エージェント（SubAgent）へ割り当てて実行する全モダリティ対応のエージェント統括（omnimodal agent orchestration）方式である。

- **2026-06 · [Omni-Flow: A Unified Workflow Orchestration and Distributed KV Cache Sharing Framework for Multimodal Inference](2026-2606.31093-omni-flow-a-unified-workflow-orchestration-and-distributed-kv-cache-sharing-framework-for-multimodal-inference.md)**  
  実装：[✓](https://github.com/meituan-longcat/omni-flow) ・ リポジトリ内被引用：0  
  マルチモーダル推論を制御・データ・計算の3層へ分離し、Python DSL、GPU/CPU/SSD分散KV、SGLang互換実行を統合する。LongCat-NextやHunyuanImage-3を同じ配信抽象へ載せる基盤。

- **2026-06 · [OffQ: Taming Structured Outliers in LLM Quantization by Offsetting](2026-2606.07116-offq-taming-structured-outliers-in-llm-quantization-by-offsetting.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低ビット量子化は、大規模言語モデル（LLM）の重み転送量と行列積の費用を削減する。一次論文の表1では、Llama 3-8BのWikiText困惑度が16ビットの6.1、比較方式ResQの7.1に対してOffQは6.98、8課題平均ゼロショット正解率はResQの63.91%に対して65.49%だった。

- **2026-06 · [Multi-Token Residual Prediction](2026-2605.18817-multi-token-residual-prediction.md)**  
  実装：[✓](https://github.com/heavyball-research/multi-token-residual-prediction) ・ リポジトリ内被引用：0  
  拡散言語モデルは、マスクされたトークン列を何度も予測し直して文章を生成する。品質を維持する静的ノイズ除去では、MRPが複数トークンを先行提案し、大型モデルが検証することで1.17〜1.40倍のスループット改善を得る。

- **2026-06 · [MS-Resampler: Multi-Scope Visual Resampling for Efficient Multimodal LLMs](2026-2606.31383-ms-resampler-multi-scope-visual-resampling-for-efficient-multimodal-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MS-Resamplerは、異なる空間窓を優先する複数の再標本化分枝を並列に配置し、局所・中域・大域の特徴を固定長のトークンへ融合する。LLaVA-1.5-7Bの576視覚トークンを144へ減らす条件では、原著Table 1の相対平均は未圧縮比101.15%である。

- **2026-06 · [MorphoQuant: Modality-Aware Quantization for Omni-modal Large Language Models](2026-2606.04349-morphoquant-modality-aware-quantization-for-omni-modal-large-language-mo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MorphoQuantは、画像・動画・音声を同時に扱う大規模言語モデルの活性値を4ビットに圧縮するとき、モダリティごとに異なる分布の形状が原因で精度が低下する問題を扱う。

- **2026-06 · [Mitigating Bias in Locally Constrained Decoding via Tractable Proposals](2026-2606.01926-mitigating-bias-in-locally-constrained-decoding-via-tractable-proposals.md)**  
  実装：[✓](https://github.com/MhDang/gelatwo) ・ リポジトリ内被引用：0  
  本論文は有限オートマトンをテンソル化し、残りトークン予算内に受理状態へ到達可能な語だけを許すGCDと、蒸留HMMで将来の有効な完了の確率を推定するP-GCDを提案。

- **2026-06 · [LoopMoE: Unifying Iterative Computation with Mixture-of-Experts for Language Modeling](2026-2606.04438-loopmoe-unifying-iterative-computation-with-mixture-of-experts-for-langu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常のMoEは、多数の専門家パラメータを保持しながら各トークンでは少数だけを選ぶことで、総容量と一回の計算量を分離する。しかし、反復による精度向上を単純な非反復モデルと比較すると、層数、総パラメータ、演算回数、専門家活性化数などが同時に変化し、何が改善を生んだのか分からなくなる。

- **2026-06 · [LatentSkill: From In-Context Textual Skills to In-Weight Latent Skills for LLM Agents](2026-2606.06087-latentskill-from-in-context-textual-skills-to-in-weight-latent-skills-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の文脈内スキル方式（In-context Skill）は、作業手順や道具の使用方法を自然言語でプロンプトへ挿入する。Qwen3-8Bを基盤としたALFWorldでは、文脈内スキル方式に対し既知課題の平均成功率が52.9%から74.3%、未知課題が56.0%から69.4%へ改善し、事前充填トークン数を約64%削減した。

- **2026-06 · [K-Forcing: Joint Next-K-Token Decoding via Push-Forward Language Modeling](2026-2606.10820-k-forcing-joint-next-k-token-decoding-via-push-forward-language-modeling.md)**  
  実装：[✓](https://github.com/alibaba-damo-academy/K-Forcing) ・ リポジトリ内被引用：0  
  推論エンジンのカーネルを高速化する研究ではなく、生成分布の表現とサンプリング方式を変える研究である。LM1BとOpenWebText（OWT）の約1億パラメータTransformerで、k=4の推論はAR比2.38〜3.47倍のスループットを報告した。

- **2026-06 · [Improving Visual Token Reduction via Rectifying Distortions for Efficient Multimodal LLM Inference](2026-2606.01711-improving-visual-token-reduction-via-rectifying-distortions-for-efficien.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚トークン削減（Visual Token Reduction; VTR）は不要なパッチを削除したり、似た特徴を統合したりして系列を短くする。LLaVA-1.5-7Bの8種類の画像理解課題で、視覚トークンを576個から64個へ減らすHoloVの平均保持率は92.2%だが、RESTOREを加えると96.5%になる。

- **2026-06 · [HyperQuant: A Rate-Distortion-Optimal Quantization Pipeline for Large Language and Diffusion Models](2026-2606.23406-hyperquant-a-rate-distortion-optimal-quantization-pipeline-for-large-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みの低ビット化とKVの低ビット化は別々の手法が発展してきたが、ビット幅を固定した符号化では、量子化後の符号分布が偏っていても同じ長さの符号を全要素へ割り当てるため、統計的な冗長性が残る。

- **2026-06 · [Execution-State Capsules: Graph-Bound Execution-State Checkpoint and Restore for Low-Latency, Small-Batch, On-Device Physical-AI Serving](2026-2606.20537-execution-state-capsules-graph-bound-execution-state-checkpoint-and-restore-for-low-latency-small-batch-on-device-physic.md)**  
  実装：[✓](https://github.com/flashrt-project/FlashRT) ・ リポジトリ内被引用：0  
  KVだけでなく再帰・畳み込み・複数トークン予測状態を丸ごと保存復元し、単一ストリーム再入場の初回応答を最大26.94倍高速化する実行状態カプセル。

- **2026-06 · [End-to-End Dynamic Sparsity for Resource-Adaptive LLM Inference](2026-2606.27743-end-to-end-dynamic-sparsity-for-resource-adaptive-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常のLLM推論は、入力が簡単か難しいか、サーバーのメモリや締切が変動するかにかかわらず、同じTransformer層と注意ヘッドを実行する。従来の動的スキップも入力のエントロピーなどから難易度を推測する方式が多く、現在のサービス側の予算を直接条件にしていない。

- **2026-06 · [End-to-End Context Compression at Scale](2026-2606.09659-end-to-end-context-compression-at-scale.md)**  
  実装：[✓](https://github.com/LeonLixyz/LCLM) ・ リポジトリ内被引用：0  
  LCLM（Latent Context Language モデル）は、長いテキストを先に小型encoderで短い連続ベクトル列へ変換し、その列を大きいdecoderへ渡すコンテキスト圧縮方式である。

- **2026-06 · [Dustin: Draft-Augmented Sparse Verification for Efficient Long-Context Generation with Speculative Decoding](2026-2606.24957-dustin-draft-augmented-sparse-verification-for-efficient-long-context-generation-with-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  対象側の過去注意とドラフト側の先読み注意を融合し、少数の意味検索ヘッドだけで検証用KVを選ぶことで、長文投機的デコードのKV読込を削減する。

- **2026-06 · [Do Value Vectors in Deep Layers Need Context from the Residual Stream?](2026-2606.02780-do-value-vectors-in-deep-layers-need-context-from-the-residual-stream.md)**  
  実装：[✓](https://github.com/RiddleHe/nanochat) ・ リポジトリ内被引用：0  
  通常の自己注意（self-注意機構）は、各層の残差ストリームから問い合わせベクトル（Query）、鍵ベクトル（Key）、値ベクトル（Value）を計算する。結果として、深い層では元のトークン自体の情報から作った値だけを用いる方が、標準の文脈依存値より良い検証損失を示した。

- **2026-06 · [Depth Exploration for LLM Decoding](2026-2606.29223-depth-exploration-for-llm-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この一択の難しさを著者らは「選択ボトルネック」と捉える。各深度区間を別のGPUへ割り当て、候補トークンとその先の計算を分岐させておき、最終深度の予測を基準に正しいトークンを確定する。提案は中間出口の予測精度を無条件に信じるのではなく、最終モデルの確定結果だけを外部へ出すため、通常の自己回帰生成との同一性を維持する設計である。

- **2026-06 · [Communication-Efficient Verifiable Attention for LLM Inference](2026-2606.16352-communication-efficient-verifiable-attention-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  VeriAttn（通信-efficient TEE-GPU 注意機構）は、注意の線形演算と非線形の指数関数をともにGPUで計算させ、TEEには結果の検証と最終的な正規化を担当させる。Intel TDX、16仮想CPU、128 GBホストメモリ、NVIDIA H20 96 GBの環境で、4種類の3B～14Bモデルを評価した。

- **2026-06 · [Cold Start Latency of Quantized Small Language Models on Serverless CPU Infrastructure](2026-9a95feba0c73-cold-start-latency-of-quantized-small-language-models-on-serverless-cpu-.md)**  
  実装：[✓](https://github.com/mingwho/slm-research) ・ リポジトリ内被引用：0  
  本論文は、アクセス頻度の低い小型言語モデル（Small Language モデル; SLM）を、要求が来たときだけ起動するサーバーレス基盤で提供する際の遅延を測る研究である。利用者の要求がないときに実行環境をゼロへ縮退させられる反面、次の要求時にはコンテナを起こし、量子化重みを読み込み、トークンを生成する必要がある。

- **2026-06 · [CLP: Collocation-Length Prediction for Zero-Loss Adaptive Multi-Token Inference](2026-2606.10935-clp-collocation-length-prediction-for-zero-loss-adaptive-multi-token-inf.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  残りの課題は、追加ヘッドが正しく予測できそうな連続トークン数を決めることである。追加ヘッドの学習は必要だが、独立した小型草稿モデルを毎回起動する方式ではない。Qwen2.5-1.5B-Instructの原著表IVでは、k=3のCLPが67.47トークン/秒、通常の貪欲復号比1.294倍、反復3-gram比率0.018となった。

- **2026-06 · [Cloud-Based Large Language Model Deployment: A Comparative Analysis of Serverless and Bring-Your-Own-Container Architectures](2026-a46fa3dc951e-cloud-based-large-language-model-deployment-a-comparative-analysis-of-se.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの運用者は、モデルを自らコンテナ化してGPUインスタンス上で動かす方式（Bring Your Own Container、以下BYOC）と、事業者が推論エンドポイントを管理するサーバーレスAPI方式を選ぶ必要がある。調査対象32モデルのうち管理型サーバーレスで利用できたのは11モデル（34.4%）、両クラウドに共通するのは2モデル（6.2%）。

- **2026-06 · [CHERRY: Compressed Hierarchical Experts with Recurrent Representational Yield](2026-2606.31796-cherry-compressed-hierarchical-experts-with-recurrent-representational-y.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  学習済みモデルの隣接層を平均してパラメータを圧縮し、同じ層を複数回使う再帰的深さ変換（Recurrent Depth Transformation; RDT）で有効深さを回復する。1B級の韓国語モデルで、重要トークン比率は平均15.3%。

- **2026-06 · [BitNet Text Embeddings](2026-2606.25674-bitnet-text-embeddings.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の量子化研究はモデル本体の低ビット化に偏りがちで、ベクトルの保存精度を下げると検索の類似度構造が崩れることもある。

- **2026-06 · [BatchGen: An Architecture for Scalable and Efficient Batch Inference](2026-2606.21712-batchgen-an-architecture-for-scalable-and-efficient-batch-inference.md)**  
  実装：[✓](https://github.com/batchgen-project/batchgen) ・ リポジトリ内被引用：0  
  系列をイベント駆動コルーチン化して停止・結合・分割・移動を可能にし、MoEバッチ形成と長尾負荷分散を動的化して最大2.3倍の大規模高速化を示す。

- **2026-06 · [Attribution-Guided and Coverage-Maximized Pruning for Structural MoE Compression](2026-2606.18304-attribution-guided-and-coverage-maximized-pruning-for-structural-moe-com.md)**  
  実装：[✓](https://github.com/yifu-ding/MoE-Slimming) ・ リポジトリ内被引用：0  
  専門家を丸ごと削除する従来方式では、重要度が高いと判定された専門家の内部にも残る冗長チャネルを見逃し、逆に頻度の低い専門家を全削除すると一部の入力に必要な能力を失う。著者らはDeepSeekとQwenの複数の混合専門家モデルを対象に、構造的枝刈り（structural 枝刈り）50%単独と、25%枝刈りに4ビット量子化を重ねた構成を比較した。

- **2026-06 · [AdaCodec: A Predictive Visual Code for Video MLLMs](2026-2606.02569-adacodec-a-predictive-visual-code-for-video-mllms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者らは再生用動画符号化の考え方を、動画の画素を忠実に再生するためではなく、言語モデルが必要とする視覚情報を少ないトークンで伝えるために再設計した。Qwen3-VL-8Bを基盤とする原著の11種類の動画理解評価では、比較可能な視覚トークン予算で各評価の基準方式を上回った。

- **2026-06 · [Above the Inner Loop: Exceeding Accelerate at LLM Prefill GEMM on the M1 AMX](2026-2606.25426-above-the-inner-loop-exceeding-accelerate-at-llm-prefill-gemm-on-the-m1-amx.md)**  
  実装：[✓](https://github.com/dbhan08/inferc) ・ リポジトリ内被引用：0  
  M1 AMXの内側ループがロード発行律速であることを切り分け、細粒度パネルで第2 AMXブロックを使い、重み事前パッキングを併用してllama.cppの128トークンfp32プリフィルを1.44倍高速化する。

- **2026-05 · [When Less is Enough: Efficient Inference via Collaborative Reasoning](2026-2605.01111-when-less-is-enough-efficient-inference-via-collaborative-reasoning.md)**  
  実装：[✓](https://github.com/fairytale9/llm_bottleneck) ・ リポジトリ内被引用：0  
  複雑な数学や科学の問題を解く推論モデルは、最終回答に到達する前に長い思考の連鎖を生成する。DUET（Dual-モデル Efficient Two-stage inference）は、高性能なモデルが「小モデルに渡すのに十分な推論信号」を生成し、軽量モデルが入力とその信号から最終回答を作る方式である。

- **2026-05 · [When Are Experts Misrouted? Counterfactual Routing Analysis in Mixture-of-Experts Language Models](2026-2605.07260-when-are-experts-misrouted-counterfactual-routing-analysis-in-mixture-of.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  混合専門家（Mixture-of-Experts; MoE）言語モデルは、各トークンについて多数の専門家ネットワークのうち少数だけを実行する。Qwen3-30B-A3Bでは、確信度の高いトークンは標準経路と最良候補の差がほぼないが、難しいトークンでは大きく乖離する。ただし、この論文は推論時に32個の候補を毎回試す高速化方式を提案したわけではない。

- **2026-05 · [VLMaxxing through FrameMogging: Training-Free Anti-Recomputation for Video Vision-Language Models](2026-2605.03351-vlmaxxing-through-framemogging-training-free-anti-recomputation-for-vide.md)**  
  実装：[✓](https://github.com/jfbastien/VLMaxxing) ・ リポジトリ内被引用：0  
  本研究は「再利用で何を省くか」と「どの時間を分母にするか」を分け、異なる三つの機構を評価する。Qwen2.5-VL-7B-Instruct-4bitで、同一動画の後続質問を14.90〜35.92倍高速化し、VideoMMEの93対では選択肢・正誤の変化を観測しなかった。

- **2026-05 · [Visual-Redundancy-Controlled Parallel Decoding for Diffusion-Based Multimodal Large Language Models](2026-2605.25820-visual-redundancy-controlled-parallel-decoding-for-diffusion-based-multi.md)**  
  実装：[✓](https://github.com/infiniteYuanyl/VRCD) ・ リポジトリ内被引用：0  
  マスク付き拡散言語モデル（masked diffusion language モデル）は、未確定の多数のトークン位置を一度に予測し、確信の高い一部を確定する処理を繰り返して文章を生成する。主要な結果は推論高速化ではなく品質改善である。

- **2026-05 · [Triplet-Block Diffusion RWKV](2026-2605.25969-triplet-block-diffusion-rwkv.md)**  
  実装：[✓](https://github.com/leonardodalinky/B3D-RWKV) ・ リポジトリ内被引用：0  
  この論文は、片方向にしか情報が流れない再帰型言語モデルを、内部構造を変更せずに双方向の拡散型生成へ転換する方法を扱う。自己回帰型Transformerは生成位置を順番に確定するため、1回の復号で出せるトークン数が限られる。離散拡散型言語モデルは複数位置を並列に修正できるが、通常はブロック内の未マスク位置を左右両方向から参照する。

- **2026-05 · [TileQ: Efficient Low-Rank Quantization of Mixture-of-Experts with 2D Tiling](2026-2605.09281-tileq-efficient-low-rank-quantization-of-mixture-of-experts-with-2d-tili.md)**  
  実装：[✓](https://anonymous.4open.science/r/TileQ-BE20) ・ リポジトリ内被引用：0  
  TileQは、混合専門家モデル（Mixture-of-Experts; MoE）の推論用重みを低ビット量子化する際、量子化誤差を修復する低ランク行列そのものが大量の専門家ごとに増殖する問題を扱う。

- **2026-05 · [Thinking as Compression: Your Reasoning Model is Secretly a Context Compressor](2026-2605.28713-thinking-as-compression-your-reasoning-model-is-secretly-a-context-compr.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の文脈圧縮は、入力文から重要そうなトークン・文書片を選ぶか、別のモデルで固定長の潜在表現へ符号化する。主要実験では、Qwen3-8Bの回答系で4倍圧縮制約下の平均F1が65.12、完全一致率（EM）が51.17、8倍ではF1 65.42・EM 51.79である。

- **2026-05 · [The Shape of Overthinking: Backtracking Bursts in Long Reasoning Traces](2026-2605.27965-the-shape-of-overthinking-backtracking-bursts-in-long-reasoning-traces.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  行単位に分割した推論文へ、別の注釈実行で「継続・停滞・後戻り・終了」の確信度を割り当て、後戻りの強度に閾値を設ける。固定2000語の打切りでは残存軌跡の正解率がAIME2024で10.0%、AIME2025で6.7%になるのに対し、接頭部分の後戻り特徴で選別すると73.5%・64.5%となり、それぞれ21.7%・27.0%の軌跡を終了対象にできる。

- **2026-05 · [The Path Matters: Learning a Token-Commitment Policy for Diffusion Language Models](2026-2605.24697-the-path-matters-learning-a-token-commitment-policy-for-diffusion-langua.md)**  
  実装：[✓](https://github.com/BobSun98/TraceLock) ・ リポジトリ内被引用：0  
  LLaDAのGSM8Kでは生成長256・窓64で最終正答率80.0%、HumanEvalのPass@1は37.2%で、信頼度方式の79.8%、36.0%をわずかに上回る。

- **2026-05 · [The Efficiency Frontier: A Unified Framework for Cost-Performance Optimization in LLM Context Management](2026-2605.23071-the-efficiency-frontier-a-unified-framework-for-cost-performance-optimiz.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全文投入、検索拡張、要約・圧縮などの文脈管理方式は、回答品質だけ、または入力トークン数だけを比較すると運用上の優劣が決めにくい。HotpotQAの5,000問をGPT-5.4 miniで評価した結果、再利用回数が1から100へ増えると、F1約0.78の運用点で有効トークン数が566から424へ約25%減る構成が選ばれた。

- **2026-05 · [SpecSA: Bridging Speculative Decoding and Sparse Attention for Efficient LLM Inference](2026-2605.19893-specsa-sparse-speculative-verification.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的検証クエリが選ぶ重複KVブロックを一度だけ読み、厳密共有と近似共有、層間索引再利用、融合カーネルを比較して、長文脈の疎注意読出しを減らすシステム。

- **2026-05 · [Semantic-Aware Intelligent Request Routing in Multi-Model LLM Backend Gateways](2026-5c886960494f-semantic-aware-intelligent-request-routing-in-multi-model-llm-backend-ga.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  APIRouterは異種LLMを接続するAPIゲートウェイで、要求の軽量特徴抽出、66MパラメータのDistilBERTによる難易度3分類、負荷・価格・品質を考慮する文脈付きバンディットの三段階でバックエンドを選択する。

- **2026-05 · [Self-Orchestrating Language Models: Leveraging Semantic Dependence for Efficient Inference](2026-2609.14850-self-orchestrating-language-models-leveraging-semantic-dependence-for-ef.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  意味的に独立する文章断片や推論段階をモデルに印付けさせ、ランタイムが並列デコード、不要なKVページの解放、または拡散生成の並列順序に利用する三方式を示すMIT博士論文。各方式は別個に評価され、速度向上は課題・設定によって品質との交換条件がある。

- **2026-05 · [Selective Latent Thinking: Adaptive Compression of LLM Reasoning Chains](2026-2605.25745-selective-latent-thinking-adaptive-compression-of-llm-reasoning-chains.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかし、文章で説明する思考の全トークンを自己回帰的に生成すると、推論遅延とKVキャッシュ使用量が増える。複数の思考トークンを連続した潜在ベクトルへ置き換える方式は生成数を減らせるが、数値、式、厳密な条件分岐などの情報まで圧縮すると、正答に必要な離散的な値が失われやすい。

- **2026-05 · [Search Your Block Floating Point Scales!](2026-2605.12464-search-your-block-floating-point-scales.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ScaleSearchは、ブロック浮動小数点（Block Floating Point、BFP）形式で低ビット量子化するとき、各ブロックに共通する尺度（Scale）を最適化する方法である。これらは異なる評価対象の数値であり、尺度探索だけで全ての改善が生じたと見なしてはならない。

- **2026-05 · [ScaleSweep: Accurate NVFP4 Post-Training Quantization of LLMs via Block Scale Initialization](2026-2606.07618-scalesweep-accurate-nvfp4-post-training-quantization-of-llms-via-block-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ScaleSweepは、NVIDIA Blackwell世代でハードウェア対応するNVFP4の重み・活性値・KVキャッシュ・query状態の量子化について、16要素ブロックのFP8スケールの選び方を改善する後学習量子化（PTQ）手法である。これはBF16比約93.9%の平均性能回復である。

- **2026-05 · [ProxyKV: Cross-Model Proxy Pruning for Efficient Long-Context LLM Inference](2026-2605.16360-proxykv-cross-model-proxy-pruning-for-efficient-long-context-llm-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ProxyKVは、長文脈LLMのKVキャッシュを圧縮するとき、どのトークンを残すかを高精度に決める計算を大型モデル自身にさせず、同じモデル系列の小型モデルへ委譲する方式である。Llama-3.1-8Bではdual-GPU構成で最大3.21倍のプレフィル高速化、同一GPU上でCUDA ストリームを共有する構成では約1.5倍を報告する。

- **2026-05 · [Probabilistic Tiny Recursive Model](2026-2605.19943-probabilistic-tiny-recursive-model.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  数独や格子型の制約充足問題で高い精度を示す一方、決定的な更新では誤った解の近傍へ収束し、再帰を増やしても抜け出せないことがある。推論時の追加計算を、再帰を長くする「深さ」だけでなく、並列に試す「幅」へ割り当てる方式である。

- **2026-05 · [PEEK: Context Map as an Orientation Cache for Long-Context LLM Agents](2026-2605.19932-peek-context-map-as-an-orientation-cache-for-long-context-llm-agents.md)**  
  実装：[✓](https://github.com/zhuohangu/peek) ・ リポジトリ内被引用：0  
  コンテキスト地図はエージェントのシステムプロンプトへ付与され、予算 B トークン以内に維持される。

- **2026-05 · [Parallel Prefix Verification for Speculative Generation](2026-2605.04263-parallel-prefix-verification-for-speculative-generation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかし従来の意味的投機方式では、節ごとに正誤を順番に判定するため、検証回数が新たな直列処理の負担となる。対象モデル単独に対する生成処理量はGPQAで1.25倍、GSM8Kで4.29倍となり、EAGLE-3併用では最大4.46倍を示した。

- **2026-05 · [OccamToken: Efficient VLM Inference with Training-Free and Budget-Adaptive Token Pruning](2026-2605.29657-occamtoken-efficient-vlm-inference-with-training-free-and-budget-adaptiv.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の視覚トークン枝刈り（visual トークン 枝刈り）は、注意重みや特徴ベクトルの類似度で重要度を付け、得点の高い上位K個を残す方式が多い。高解像度のLLaVA-NeXTでは、元の2,880個から平均40個まで減らしても元モデルの集約性能の93.8%を維持する。

- **2026-05 · [NCO: A Versatile Plug-in for Handling Negative Constraints in Decoding](2026-2605.10065-nco-a-versatile-plug-in-for-handling-negative-constraints-in-decoding.md)**  
  実装：[✓](https://github.com/hyundong98/NCO-Decoding) ・ リポジトリ内被引用：0  
  一般的な制約付き復号は「出力が指定文法に属する」正制約を扱うことが多い。NCO（Negative Constraint Optimization）は逆に、複数の禁止文字列または正規表現が生成結果のどの位置にも現れないことを要求する。ただしGUARDの評価は同手法全体ではなくトライ成分に限定される。

- **2026-05 · [NCCLZ: Compression-Enabled GPU Collectives with Decoupled Quantization and Entropy Coding](2026-2605.12396-ncclz-compression-enabled-gpu-collectives-with-decoupled-quantization-an.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPUの演算能力が向上しても、ノード間ネットワークの帯域が不足すると通信待ちが律速になる。通信前に量子化すればデータ量を減らせるものの、量子化だけでは記号の偏りを利用しきれず、さらに符号化・復号のGPU計算が通信時間を上回る場合もある。論文の要旨はNCCL比最大9.65倍、既存の圧縮集合通信ライブラリ比最大3.34倍と報告する。

- **2026-05 · [N-vium: Mixture-of-Exits Transformer for Accelerated Exact Generation](2026-2605.13190-n-vium-mixture-of-exits-transformer-for-accelerated-exact-generation.md)**  
  実装：[✓](https://github.com/ETH-DISCO/n-vium) ・ リポジトリ内被引用：0  
  N-viumは、自己回帰言語モデルの「次のトークンを確定する処理」と「将来の注意計算に必要な全層のKVキャッシュを作る処理」を切り離す推論方式である。

- **2026-05 · [Multi-Mixer Models: Flexible Sequence Modeling with Shared Representations](2026-2605.28769-multi-mixer-models-flexible-sequence-modeling-with-shared-representation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、自己注意（Self-注意機構）と線形再帰型の系列混合（Linear Recurrent Sequence Mixing）を、モデルの異なる層に固定配置するのではなく、同一層・同一系列の異なる区間で切り替えるOryxアーキテクチャを提案する。

- **2026-05 · [Mixture of Layers with Hybrid Attention: Parallel Thin Blocks for Sparse Transformer Compute](2026-2605.09516-mixture-of-layers-with-hybrid-attention-parallel-thin-blocks-for-sparse-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  標準的な専門家混合（Mixture of エキスパート; MoE）は各Transformer層の主にフィードフォワードネットワーク（FFN）を複数の専門家に分け、トークンごとに一部を使う。しかし注意計算と層の入出力は幅の広い一つのブロックのままであり、モデルの容量とトークン当たりの計算を別々に増減できる範囲は限られる。

- **2026-05 · [MeMo: Memory as a Model](2026-2605.15156-memo-memory-as-a-model.md)**  
  実装：[✓](https://github.com/arunv3rma/MeMo) ・ リポジトリ内被引用：0  
  従来の検索拡張生成（RAG）は質問ごとに検索索引から文書を取得するため、検索雑音、複数文書にまたがる関係の取りこぼし、長い引用文脈の投入が問題になる。MeMoは、知識を記憶する小型モデルと、推論・回答を担当する凍結モデルを分離する。

- **2026-05 · [MARR: Module-Adaptive Residual Reconstruction for Low-Bit Post-Training Quantization](2026-2605.17997-marr-module-adaptive-residual-reconstruction-for-low-bit-post-training-q.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MARR（Module-適応的 Residual Reconstruction）は、学習済みモデルを追加学習せず低ビットへ変換する学習後量子化（post-学習 量子化; PTQ）で、層をまたぐ量子化誤差の補正を強めすぎないための方法である。

- **2026-05 · [LoopQ: Quantization for Looped Language Models](2026-2605.16343-loopq-quantization-for-looped-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の事後量子化（PTQ）は同一重みに同じ変換行列と尺度を適用し続けるため、周回ごとに活性化の大きさ・方向が変わると丸め誤差やクリッピングが生じる。W4A4条件で4バックボーンの5課題平均正答率は静的PTQ最良比較方式に対して相対平均67.8%改善し、8つのバックボーン×データセット条件のPPL相対減少は下限代入による保守的平均75.2%と報告した。

- **2026-05 · [LocateAnything: Fast and High-Quality Vision-Language Grounding with Parallel Box Decoding](2026-2605.27365-locateanything-fast-and-high-quality-vision-language-grounding-with-para.md)**  
  実装：[✓](https://github.com/NVlabs/Eagle/tree/main/Embodied) ・ リポジトリ内被引用：0  
  各矩形を、四つの量子化座標と構造トークンからなる長さ6のブロックで表し、ブロック内部は同時に予測する。

- **2026-05 · [Llamas on the Web: Memory-Efficient, Performance-Portable, and Multi-Precision LLM Inference with WebGPU](2026-2605.20706-llamaweb.md)**  
  実装：[✓](https://github.com/ggml-org/llama.cpp) ・ リポジトリ内被引用：0  
  LlamaWebは静的メモリ計画、端末適応型WebGPUカーネル、量子化対応をllama.cppへ統合し、ブラウザ推論のメモリ消費とデコード性能を改善する。

- **2026-05 · [Layer-wise Token Compression for Efficient Document Reranking](2026-2605.20683-layer-wise-token-compression-for-efficient-document-reranking.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検索システムの再順位付け（reranking）では、初段のBM25や密ベクトル検索が返した文書候補を、より高価なTransformerで再評価する。Qwen3-0.6BのDL19段落再順位付けでは、28層中第8層から40%のトークンを残す設定でnDCG@10が無圧縮の約0.727と同水準のまま、QPSは5.35→6.69（25%増）となる。

- **2026-05 · [Layer Collapse in Diffusion Language Models](2026-2605.06366-layer-collapse-in-diffusion-language-models.md)**  
  実装：[✓](https://github.com/Conzel/super-outlier-dlm) ・ リポジトリ内被引用：0  
  本論文は、離散拡散型言語モデル（Diffusion Language モデル、DLM）と自己回帰型言語モデル（Autoregressive Language モデル、ARモデル）で、隠れ状態の層間類似性と圧縮耐性がどのように異なるかを調べた実証研究である。

- **2026-05 · [LASER: Loss-Aware Singular-value Decomposition and Rank Allocation for Efficient Low-Precision Vision-Language Models](2026-2606.00573-laser-loss-aware-singular-value-decomposition-and-rank-allocation-for-ef.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LASERは、視覚言語モデル（VLM）の自己注意のQ/K/V射影を低ランク化し、同時に低精度化を行う圧縮・推論実装である。

- **2026-05 · [Language Modeling with Hyperspherical Flows](2026-2605.11125-language-modeling-with-hyperspherical-flows.md)**  
  実装：[✓](https://github.com/jdeschena/s-flm) ・ リポジトリ内被引用：0  
  S-FLMは代わりに次元 d の単位超球面 S^{d-1} 上へトークンを配置し、雑音ベクトルから正しい単語埋め込みへ回転する経路を学習する。

- **2026-05 · [IO-SVD: Input-Output Whitened SVD for Adaptive-Rank LLM Compression](2026-2605.15626-io-svd-input-output-whitened-svd-for-adaptive-rank-llm-compression.md)**  
  実装：[✓](https://github.com/mint-vu/IO-SVD) ・ リポジトリ内被引用：0  
  特異値分解（Singular Value Decomposition; SVD）による学習後圧縮は、密な線形層の重み行列を低階数の二つの因子に分け、保存量と乗算量を減らす手法である。

- **2026-05 · [InfoQuant: Shaping Activation Distributions for Low-Bit LLM Quantization](2026-2605.26175-infoquant-shaping-activation-distributions-for-low-bit-llm-quantization.md)**  
  実装：[✓](https://github.com/LLIKKE/InfoQuant) ・ リポジトリ内被引用：0  
  InfoQuantは、LLMの低ビット事後量子化（post-学習 量子化; PTQ）における活性値の量子化誤差を、単純な外れ値除去ではなく、量子化器に入力する分布の形から最適化する方式である。

- **2026-05 · [HybridServe: Stall-Free Distributed Disaggregated LLM Inference with Hybrid KVCache Buffering](2026-1e016ba4edaa-hybridserve-stall-free-distributed-disaggregated-llm-inference-with-hybr.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来のPush方式は、事前入力が終わるとキャッシュを復号側へすぐ送るため、後の復号時にノード間転送を待ちにくい。2台のV100を用いた実機では、前段停止が大きい条件で最初のトークンまでの時間が最大1.76倍高速化し、処理量は最大1.57倍改善した。

- **2026-05 · [Hierarchical Mixture-of-Experts with Two-Stage Optimization](2026-2605.08292-hierarchical-mixture-of-experts-with-two-stage-optimization.md)**  
  実装：[✓](https://github.com/brain-lab-research/Hi-MoE) ・ リポジトリ内被引用：0  
  混合専門家モデル（Mixture-of-Experts、MoE）は、多数の専門家ネットワークを用意し、各トークンで少数だけ実行することで総パラメータ数と実行計算量を分離する。パープレキシティ（perplexity、PPL）は11検証領域の10領域で改善するが、下流課題の一部では悪化し、実測の生成トークン毎秒が40%改善したという意味ではない。

- **2026-05 · [GRIP-VLM: Group-Relative Importance Pruning for Efficient Vision-Language Models](2026-2605.13375-grip-vlm-group-relative-importance-pruning-for-efficient-vision-language.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GRIP-VLM（Group-Relative Importance Pruning for Efficient Vision-Language Models）は、視覚言語モデル（VLM）へ渡す大量の画像トークンを、入力ごと・層ごと・保持予算ごとに選び直す手法である。

- **2026-05 · [GQLA: Group-Query Latent Attention for Hardware-Adaptive Large Language Model Decoding](2026-2605.15250-gqla-group-query-latent-attention-for-hardware-adaptive-large-language-m.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  多頭潜在注意（Multi-head Latent 注意機構; MLA）は鍵と値を共通の低ランク潜在ベクトルへまとめ、過去文脈から読み出すバイト数を大きく削減する。論文の中心的な「H20で3.4倍」は、文脈長8192・BF16・公開ピーク性能を入力した屋根線モデルによる注意部分の理論的処理量であり、実GPUで測ったモデル全体のトークン生成速度ではない。

- **2026-05 · [Ghosted Layers: Unconstrained Activation Alignment for Recovering Layer-Pruned LLMs](2026-2605.15491-ghosted-layers-unconstrained-activation-alignment-for-recovering-layer-p.md)**  
  実装：[✓](https://github.com/daniel-eai/ghosted_layers_official_repository) ・ リポジトリ内被引用：0  
  大規模言語モデルの深さ方向の構造的枝刈りは、トランスフォーマーの復号層を丸ごと削除し、特殊な疎行列カーネルを必要とせずにモデルの演算と重みを減らせる。LLaMA-3.1-8Bで32層中7層をLLM-Streamlineにより削除した場合、9課題平均正答率は無補正の42.60%から60.01%へ回復する。

- **2026-05 · [Gated Subspace Inference for Transformer Acceleration](2026-2605.03109-gated-subspace-inference-for-transformer-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）のバッチサイズ1の逐次復号では、GPUの計算能力よりも重み行列を高帯域メモリ（HBM）から読む費用が律速になりやすい。Gated Subspace Inference（GSI）は、各層の活性化を低次元基底への射影と残差に分解し、残差が十分小さいトークンだけ、事前計算した低次元の重み像を使う方式である。

- **2026-05 · [Fre-Res: Frequency-Residual Video Token Compression for Efficient Video MLLMs](2026-2605.16366-fre-res-frequency-residual-video-token-compression-for-efficient-video-m.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動画対応マルチモーダルLLMにおいて、疎な高精細空間アンカーフレームと、フレーム間残差の時間方向DCT低周波成分を別経路で圧縮・統合するFre-Resを提案。Qwen2-VL-7Bの約2.1倍圧縮でNExT-QA 70.08、LongVideoBench 53.52、EgoSchema 63.58を達成。

- **2026-05 · [Enhancing Visual Token Representations for Video Large Language Models via Training-Free Spatial-Temporal Pooling and Gridding](2026-2605.22078-enhancing-visual-token-representations-for-video-large-language-models-v.md)**  
  実装：[✓](https://github.com/bingjunluo/ST-GridPool) ・ リポジトリ内被引用：0  
  階層的な時間区間のフレームを格子状に組み合わせ、区間末尾へ多時間尺度の要約を埋め込むPyramid Temporal Gridding（PTG）と、視覚特徴のL2ノルムを重みに使うNorm-based Spatial Pooling（NSP）を統合する。

- **2026-05 · [Efficient Diffusion LLMs via Temporal-Spatial Parallel Decoding and Confidence Extrapolation](2026-2605.30753-efficient-diffusion-llms-via-temporal-spatial-parallel-decoding-and-conf.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  自己回帰型モデルは基本的に次の一語を順番に生成するのに対し、マスク型dLLMは多数の未確定位置を同時に予測し、確信度の低い位置を再びマスクして次の反復で修正する。

- **2026-05 · [Efficient Cooperation-Aware Key and Value Management for LLM Inference](2026-3089a0084f72-efficient-cooperation-aware-key-and-value-management-for-llm-inference.md)**  
  実装：[✓](https://github.com/ZJU-DIVER/CoKV) ・ リポジトリ内被引用：0  
  得られたSSVは事前にモデルと検証データから計算し、実行時にはヘッド群別の保持トークン数やKV量子化ビット数の重みとして使う。Qwen3-32Bで平均128組のKVを保持する設定では、GSM8Kの正答率82.10%、MATH 46.17%を報告し、比較した圧縮方式を上回る。

- **2026-05 · [Dropping the Anchor: Statistical Context Summarization for Distributed Systems via Pulsar Attention](2026-2607.20457-dropping-the-anchor-statistical-context-summarization-for-distributed-sy.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既存のStar 注意機構は、系列を連続ブロックに分けて各GPUで並列符号化し、生成時には各GPUの注意結果を統合する。しかし、長い文書の後半を担当するGPUにも、文書の先頭しか参照できないアンカーを繰り返し処理させることになり、局所入力が本来のブロックの約2倍になる。

- **2026-05 · [Different Prompts, Different Ranks: Prompt-aware Dynamic Rank Selection for SVD-based LLM Compression](2026-2605.08568-different-prompts-different-ranks-prompt-aware-dynamic-rank-selection-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  特異値分解（SVD）による低ランク圧縮は、重み行列を小さい行列の積へ分解し、寄与の小さい成分を切り捨てる。

- **2026-05 · [DeferMem: Query-Time Evidence Distillation via Reinforcement Learning for Long-Term Agent Memory](2026-2605.22411-defermem-query-time-evidence-distillation-via-reinforcement-learning-for.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の記憶システムは、将来の質問が分からない時点で対話を要約・圧縮し、検索しやすい記憶単位を作る。原著v2の評価ではLongMemEval-Sの正答率が70.00%、LoCoMoで学習に使った唯一の会話conv-26を除いた正答率が89.93%だった。

- **2026-05 · [Concurrency without Model Changes: Future-based Asynchronous Function Calling for LLMs](2026-2605.15077-concurrency-without-model-changes-future-based-asynchronous-function-cal.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  一般的な同期方式では、モデルがツール呼出しを出力すると、その処理が完了するまで次の生成を止める。GPT-4oを用いたBFCL v4の検索ツール評価では、逐次同期呼出しと比べてタスク完了時間を1.26倍高速化した。

- **2026-05 · [Compute Where it Counts: Self Optimizing Language Models](2026-2605.10875-compute-where-it-counts-self-optimizing-language-models.md)**  
  実装：[✓](https://github.com/akhauriyash/SOL) ・ リポジトリ内被引用：0  
  Self-Optimizing Language Models（SOL）は、LLM推論の各トークンに同じ圧縮率・計算予算を与えるのではなく、トークンごとに計算の必要度が異なるという性質を利用して、どこで計算を節約し、どこで品質を守るかを小型制御器に学習させる方式である。

- **2026-05 · [Code Generation by Differential Test Time Scaling](2026-2605.20473-code-generation-by-differential-test-time-scaling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  コード生成の推論時計算量拡張（Test-Time Scaling、TTS）では、一つの問題に対して複数のコードを生成し、その中から正しい候補を選ぶ。従来の選択方式には、公開テストを実行するもの、別のLLMにテスト入力を生成させるもの、LLM評価器に候補を比較させるものがある。

- **2026-05 · [BlockBatch: Multi-Scale Consensus Decoding for Efficient Diffusion Language Model Inference](2026-2605.29233-blockbatch-multi-scale-consensus-decoding-for-efficient-diffusion-langua.md)**  
  実装：[✓](https://github.com/Laurence-Wu/BlockBatch) ・ リポジトリ内被引用：0  
  局所更新で古くなったKVキャッシュは定期的な全系列再計算で補正する。学習済みモデルの重みを変更しない推論時方式である。著者はLLaDA系2モデルとDream系1モデル、算数・数学・コード生成の4課題を用い、Fast-dLLMの二重キャッシュ方式と比較して、モデル呼出し回数（NFE）を平均26.6%削減し、実測生成時間を平均1.33倍高速化したと報告する。

- **2026-05 · [Bandwidth-Aware LLM Inference on Heterogeneous Many-Core Supercomputers](2026-2605.25655-bandwidth-aware-llm-inference-on-heterogeneous-many-core-supercomputers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低帯域・分散オンチップ記憶のMT-3000向けに演算子、融合注意、三段パイプライン、混合並列を共同設計し、大規模LLM推論を実現。

- **2026-05 · [AgentStop: Terminating Local AI Agents Early to Save Energy in Consumer Devices](2026-2605.15206-agentstop-terminating-local-ai-agents-early-to-save-energy-in-consumer-d.md)**  
  実装：[✓](https://github.com/brave-experiments/AgentStop) ・ リポジトリ内被引用：0  
  LLMエージェントは通常の一問一答と異なり、推論、検索、コード実行、失敗後の再試行を何度も繰り返す。これをクラウドではなく利用者の端末で動かすと、ネットワーク依存や外部へのデータ送信を減らせる一方、長時間のGPU稼働、発熱、電池消費が利用者に直接影響する。特に失敗する実行が長く続いた場合、最終的な課題成功に結び付かない電力が大量に消費される。

- **2026-05 · [Adaptive Inverted-Index Routing for Granular Mixtures-of-Experts](2026-2605.04952-adaptive-inverted-index-routing-for-granular-mixtures-of-experts.md)**  
  実装：[✓](https://anonymous.4open.science/r/adaptive_inverted_index_routing_code-D6FE/) ・ リポジトリ内被引用：0  
  本研究が解くのは、非常に多数の小さな専門家を使う混合専門家モデル（Mixture-of-Experts、MoE）で、専門家を選ぶルータ自身が高価になるという問題である。具体的には、入力トークンを最も近い符号語へ割り当て、その符号語に結び付いた専門家番号の候補表を取得する。著者は最大約10%の相対困惑度改善をPEERとの比較で報告する。

- **2026-05 · [A general tensor-structured compression scheme for efficient large language models](2026-2605.25344-a-general-tensor-structured-compression-scheme-for-efficient-large-langu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MixT（Mixture of Tensors）は、Transformer内の密な線形変換を、局所的なテンソル演算子を複数重ねた構造に置き換える方式である。

- **2026-04 · [Valve: Production Online-Offline Inference Colocation with Jointly-Bounded Preemption Latency and Rate](2026-2604.07874-valve-production-online-offline-inference-colocation-with-jointly-bounde.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Valveは、オンラインLLM推論のためにピーク需要へ合わせてGPUを確保すると、通常時に空き計算能力が大量に生じる問題を扱う。従来の同居方式では、オンライン要求が来たときにオフライン処理を止めるまで時間がかかるか、短い空き時間ごとに停止と再開を繰り返して干渉が増える。

- **2026-04 · [Unlocking the Edge deployment and ondevice acceleration of multi-LoRA enabled one-for-all foundational LLM](2026-2604.18655-ondevice-multilora-runtime.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  実行時LoRA入力・NPU向け最適化・並行生成・自己投機的復号を統合し、Galaxy S24/S25で多用途LLMを単一グラフ展開する。

- **2026-04 · [Two-dimensional early exit optimisation of LLM inference](2026-2604.18592-two-dimensional-early-exit-optimisation-of-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、大規模言語モデルを文書分類器として使う場合に、何層まで計算するかと入力文書の何文目まで読むかを同時に制御する二次元早期終了（two-dimensional early exit）を提案する。

- **2026-04 · [TRIMS: Trajectory-Ranked Instruction Masked Supervision for Diffusion Language Models](2026-2604.00666-trims-trajectory-ranked-instruction-masked-supervision-for-diffusion-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TRIMS（Trajectory-Ranked Instruction Masked Supervision）は、マスク拡散言語モデル（Masked Diffusion Language モデル; MDLM）の反復生成で、どのトークンを先に確定するかを学習中から誘導する方式である。

- **2026-04 · [Towards Joint Quantization and Token Pruning of Vision-Language Models](2026-2604.17320-towards-joint-quantization-and-token-pruning-of-vision-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は視覚言語モデル（VLM）の推論で、低ビット量子化と視覚トークン枝刈りを別々に設計すると品質が不安定になる問題を扱う。LLaVA-1.5-7B-hfで視覚トークンを最終30%まで削減した場合、6ベンチマークの完全精度モデルに対する平均性能保持率は95.65%だった。

- **2026-04 · [Towards Faster Language Model Inference Using Mixture-of-Experts Flow Matching](2026-2604.15009-towards-faster-language-model-inference-using-mixture-of-experts-flow-ma.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、通常の自己回帰（autoregressive; AR）生成が1トークンごとに逐次的な前向き計算を必要とする問題に対し、連続潜在空間上の流れ合わせ（flow matching）と混合専門家（mixture of エキスパート; MoE）を組み合わせる非自己回帰（non-autoregressive; NAR）モデルYANを提案する。

- **2026-04 · [Thinking Without Words: Efficient Latent Reasoning with Abstract Chain-of-Thought](2026-2604.22709-thinking-without-words-efficient-latent-reasoning-with-abstract-chain-of.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  自然言語CoTは数学や多段階推論の正答率を改善するが、途中の推論を文章として一語ずつ生成するため、長い回答までの待ち時間と生成トークン費用を増やす。推論内容を短縮する手法には、文章を途中で打ち切る方式、自然言語のCoTを段階的に内在化する方式、連続ベクトルの潜在思考を繰り返す方式などがある。

- **2026-04 · [The Recurrent Transformer: Greater Effective Depth and Efficient Decoding](2026-2604.21215-the-recurrent-transformer-greater-effective-depth-and-efficient-decoding.md)**  
  実装：[✓](https://github.com/geniucos/recurrent-transformer) ・ リポジトリ内被引用：0  
  通常の自己回帰Transformerでは、ある層のトークン位置$i$に対する鍵・値は、その層に入力された表現から計算される。重要なのは、固定サイズの再帰状態へ過去を押し込む方式ではないことだ。

- **2026-04 · [Tandem: Riding Together with Large and Small Language Models for Efficient Reasoning](2026-2604.23623-tandem-riding-together-with-large-and-small-language-models-for-efficien.md)**  
  実装：[✓](https://github.com/Applied-Machine-Learning-Lab/ACL2026_Tandem) ・ リポジトリ内被引用：0  
  Tandemは、推論型大規模言語モデルが難問を解く際に生成する長い思考列を、より安価な小型言語モデルへ部分的に委ねる協調推論方式である。

- **2026-04 · [Stability Implies Redundancy: Delta Attention Selective Halting for Efficient Long-Context Prefilling](2026-2604.18103-stability-implies-redundancy-delta-attention-selective-halting-for-effic.md)**  
  実装：[✓](https://github.com/verach3n/DASH) ・ リポジトリ内被引用：0  
  FlashAttentionは注意行列を外部メモリへ展開しないことで転送量を削減するが、入力トークンが多ければ必要な計算量自体は残る。DASH（Delta 注意機構 Selective Halting）は、各トークンの表現が層を進むにつれて更新されなくなる「意味的固定点」に着目する。

- **2026-04 · [SpecFed: Accelerating Federated LLM Inference with Speculative Decoding and Compressed Transmission](2026-2604.25777-specfed-accelerating-federated-llm-inference-with-speculative-decoding-and-compressed-transmission.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  連合LLM投機的復号で上位K確率だけを送信し、2種の確率再構成と誤差上界により通信量を削減する方式。

- **2026-04 · [Sink-Token-Aware Pruning for Fine-Grained Video Understanding in Efficient Video LLMs](2026-2604.20937-sink-token-aware-pruning-for-fine-grained-video-understanding-in-efficie.md)**  
  実装：[✓](https://github.com/rlqja1107/SToP) ・ リポジトリ内被引用：0  
  従来の枝刈りは視覚符号化器の注意重みを重要度の代用として使うが、注意が高い位置に意味情報が多いとは限らない。

- **2026-04 · [SimDiff: Depth Pruning via Similarity and Difference](2026-2604.19520-simdiff-depth-pruning-via-similarity-and-difference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SimDiffは、隣接層の隠れ状態について方向の違いと変化の大きさを別々に計算し、重み付きの重要度へ統合する。一次論文は25%剪定したLLaMA2-7Bで元モデルの10課題平均の91.44%を維持し、LLaMA3.1-8Bで12層を削った場合にA40上の生成スループット1.49倍を報告する。

- **2026-04 · [Serving Chain-structured Jobs with Large Memory Footprints with Application to Large Foundation Model Serving](2026-2604.14993-serving-chain-structured-jobs-with-large-memory-footprints-with-application-to-large-foundation-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分散パイプライン型の大規模言語モデル推論を、モデルブロック配置、鍵値キャッシュ容量配分、オンライン負荷分散からなるサーバ鎖構成問題として定式化し、実サービング評価で平均応答時間を六十三から七十七パーセント削減する。

- **2026-04 · [RouteLMT: Learned Sample Routing for Hybrid LLM Translation Deployment](2026-2604.22520-routelmt-learned-sample-routing-for-hybrid-llm-translation-deployment.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルを用いた翻訳では、高品質な大型モデルをすべての要求に適用すると推論費用と遅延が大きくなる。小型モデルで大半を処理し、必要な要求だけ大型モデルへ振り分ける混成配備（hybrid deployment）は、一定の品質を維持しながら大型モデルの利用率を抑えるための基本的な方式である。

- **2026-04 · [Residual-Mass Accounting for Partial-KV Decoding](2026-2604.05438-residual-mass-accounting-for-partial-kv-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  入力文脈が長いほど読み出すKVが増え、メモリ帯域が律速になりやすい。そこで一部の過去トークンだけを取得して正確な注意を計算する部分KV方式がある。Llama-3.2-3B-InstructのRULER、64k文脈、全体の1%を正確参照する設定では、選択のみのTop-Kの0.688に対し提案法は0.711、全注意は0.721だった。

- **2026-04 · [Reason Only When Needed: Efficient Generative Reward Modeling via Model-Internal Uncertainty](2026-2604.10072-reason-only-when-needed-efficient-generative-reward-modeling-via-model-i.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  難しい質問には段階的な思考連鎖（Chain-of-Thought、CoT）が有効だが、簡単な質問にも毎回長い思考を生成すると、回答に至るまでの生成トークン数と推論費用が増える。ただし最初の並列生成は無料ではなく、バッチやGPU配置を含む実システム全体で同じ節約率になるとは限らない。

- **2026-04 · [Prompt Compression in the Wild: Measuring Latency, Rate Adherence, and Quality for Faster LLM Inference](2026-2604.02985-prompt-compression-in-the-wild-measuring-latency-rate-adherence-and-qual.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  入力圧縮（プロンプト compression）は、情報価値の低い語や断片を削り、生成モデルに渡す入力を短くすることでこの費用を減らす。著者はLLMLingua-2の軽量な圧縮器を使えば、特定の長文入力・高圧縮条件で端から端までの遅延を最大約18%減らせると報告する。

- **2026-04 · [POINTS-Long: Adaptive Dual-Mode Visual Reasoning in MLLMs](2026-2604.11627-points-long-adaptive-dual-mode-visual-reasoning-in-mllms.md)**  
  実装：[✓](https://anakin-skywalker-joseph.github.io/POINTS-Long-Webpage) ・ リポジトリ内被引用：0  
  WangらはPOINTS-Longを提案し、高精細な視覚情報を使うFocusモードと、圧縮された視覚情報だけを使うStandbyモードを同じモデルに持たせる。64フレームの動画では、Standbyが1フレーム8〜32トークン、合計512〜2,048トークンだけを使い、原著Table 1の相対平均97.7〜99.7%を維持する。

- **2026-04 · [NI Sampling: Accelerating Discrete Diffusion Sampling by Token Order Optimization](2026-2604.18471-ni-sampling-accelerating-discrete-diffusion-sampling-by-token-order-opti.md)**  
  実装：[✓](https://github.com/imagination-research/NI-Sampling) ・ リポジトリ内被引用：0  
  そのため従来の全段階方式は一回のモデル実行で一位置だけを確定し、長さ512の出力では原則512回の推論が必要となる。ICLR 2026の論文に記載された単一GPU評価では、LLaDA-8B-InstructのMBPP、生成長512で全段階方式19.1トークン/秒に対し273.8トークン/秒（14.3倍）を報告する。

- **2026-04 · [MI-Pruner: Crossmodal Mutual Information-guided Token Pruner for Efficient MLLMs](2026-2604.03072-mi-pruner-crossmodal-mutual-information-guided-token-pruner-for-efficien.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意の吸い込み（注意機構 Sink）、位置偏り、複数注意ヘッドの役割差、画像全体で目立つ物体への偏りがある。さらに64トークンのPOPE効率測定では、質問関連性だけを使うλ=1の構成が77.06ms、13.93GBであり、VisPrunerの89.48ms、14.35GBより小さい。

- **2026-04 · [MCAP: Deployment-Time Layer Profiling for Memory-Constrained LLM Inference](2026-2604.21026-mcap-deployment-time-layer-profiling-for-memory-constrained-llm-inferenc.md)**  
  実装：[✓](https://github.com/genovationtech/nve) ・ リポジトリ内被引用：0  
  MCAP（Monte Carlo Activation Profiling）は、モデルを読み込む段階で少数の入力を使って層ごとの重要度を計測し、推論時の演算精度と重みの常駐先を同時に決める方式である。論文の代表例ではプロファイルは338バイトのJSONであり、初回計測は約60秒、同一アーキテクチャの再利用時は追加計測を省ける。

- **2026-04 · [MARS: Enabling Autoregressive Models Multi-Token Generation](2026-2604.07023-mars-enabling-autoregressive-models-multi-token-generation.md)**  
  実装：[✓](https://github.com/Xalp/MARS) ・ リポジトリ内被引用：0  
  MARS（Mask AutoRegreSsion）は、通常は1回の前向き計算で1トークンを生成する自己回帰（autoregressive; AR）言語モデルに、必要なときだけ複数トークンをまとめて出力する能力を追加する方式である。

- **2026-04 · [LLaDA2.0-Uni: Unifying Multimodal Understanding and Generation with Diffusion Large Language Model](2026-2604.20796-llada2-0-uni-unifying-multimodal-understanding-and-generation-with-diffu.md)**  
  実装：[✓](https://github.com/inclusionAI/LLaDA2.0-Uni) ・ リポジトリ内被引用：0  
  画像理解と画像生成を一つの基盤モデルで扱うには、画像を言語モデルへどう渡すかが大きな設計課題になる。SPRINTの最大1.6倍とデコーダの段数削減は異なる処理段階の話であり、単純に掛け算してエンドツーエンドの高速化率とみなしてはならない。

- **2026-04 · [LBLLM: Lightweight Binarization of Large Language Models via Three-Stage Distillation](2026-2604.19167-lbllm-lightweight-binarization-of-large-language-models-via-three-stage-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LBLLMは、既存の大規模言語モデルを極端な低ビット表現へ変換する際、重みと活性化を一度に量子化して学習すると誤差が増幅し、蒸留が不安定になる問題を扱う。LLaMA-2-7Bの同等ビット幅で、LBLLMのWikiText-2困惑度は9.18、C4困惑度は10.91、六つの常識推論課題の平均正答率は54.91%となった。

- **2026-04 · [Latent-Condensed Transformer for Efficient Long Context Modeling](2026-2604.12452-latent-condensed-transformer-for-efficient-long-context-modeling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  多頭潜在注意（multi-head latent 注意機構、MLA）はトークンごとのKVを低次元潜在へ圧縮するが、文脈の全トークンを保持し、注意計算も全長に対して行う。

- **2026-04 · [Integrated Electro-Optic Attention Nonlinearities for Transformers](2026-2604.09512-integrated-electro-optic-attention-nonlinearities-for-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この論文は、非線形関数をデジタル回路で近似する代わりに、光の干渉に伴う電圧と透過光強度の非線形関係を演算として利用する方式を提案する。

- **2026-04 · [Geometry-Guided 3D Visual Token Pruning for Video-Language Models](2026-2604.18260-geometry-guided-3d-visual-token-pruning-for-video-language-models.md)**  
  実装：[✓](https://github.com/homothetic/Geo3DPruner) ・ リポジトリ内被引用：0  
  動画言語モデル（Video Language モデル）は、動画フレームを多数の画像パッチに分割して言語モデルへ入力する。三次元場面理解では同じ机や椅子が異なるカメラ位置から繰り返し写るため、入力トークンが増えても新しい空間情報が比例して増えるとは限らない。比較対象FastVは81.0%、VisPrunerは84.9%である。

- **2026-04 · [GenericAgent: A Token-Efficient Self-Evolving LLM Agent via Contextual Information Density Maximization (V1.0)](2026-2604.17091-genericagent-a-token-efficient-self-evolving-llm-agent-via-contextual-in.md)**  
  実装：[✓](https://github.com/lsdefine/GenericAgent) ・ リポジトリ内被引用：0  
  GenericAgent（GA）は、この問題を単純な長文対応ではなく、限られた文脈内の意思決定に有効な情報密度を高めるシステム設計として扱う。論文は複数のエージェント基盤との比較を行い、5種類の長期タスクでGAとClaude コードがともに100%成功しながら、GAの総トークン数が188,829、比較方式が537,413だったと報告する。

- **2026-04 · [Faster LLM Inference via Sequential Monte Carlo](2026-2604.15672-faster-llm-inference-via-sequential-monte-carlo.md)**  
  実装：[✓](https://github.com/abdelfattah-lab/smcsd) ・ リポジトリ内被引用：0  
  本論文は、従来の投機的復号（投機的復号; SD）で候補トークンが最初に棄却されると、その後の候補まで捨てなければならない問題に対し、逐次モンテカルロ法（sequential Monte Carlo; SMC）を用いた近似的な復号方式SMC-SDを提案する。

- **2026-04 · [Expert Upcycling: Shifting the Compute-Efficient Frontier of Mixture-of-Experts](2026-2604.19835-expert-upcycling-shifting-the-compute-efficient-frontier-of-mixture-of-e.md)**  
  実装：[✓](https://github.com/amazon-science/expert-upcycling) ・ リポジトリ内被引用：0  
  混合専門家モデル（Mixture-of-Experts; MoE）は、各トークンが多数の専門家のうち一部だけを実行することで、総パラメータ数とトークン当たり演算量を切り離す。32専門家を64専門家へ増やした場合、50%の継続事前学習予算で13Bを最初から訓練する方式よりGPU時間を約32%節約し、検証損失を1.308から1.305へ下げた。

- **2026-04 · [ELMoE-3D: Leveraging Intrinsic Elasticity of MoE for Hybrid-Bonding-Enabled Self-Speculative Decoding in On-Premises Serving](2026-2604.14626-elmoe-3d-hybrid-bonding-self-speculative-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HBメモリ上の頻出エキスパート上位ビットをキャッシュ兼自己ドラフトとして使い、MoEの投機的デコードと重み転送を一体最適化する3D積層HW-SW協調方式。

- **2026-04 · [Efficient Test-Time Scaling via Temporal Reasoning Aggregation](2026-2604.17304-efficient-test-time-scaling-via-temporal-reasoning-aggregation.md)**  
  実装：[✓](https://github.com/qianfantianyuzhouzhou/TRACE) ・ リポジトリ内被引用：0  
  推論時の計算量を増やすと難問の正答率を改善できる場合があるが、すべての問題で長い思考を最後まで生成することが効率的とは限らない。答えが既に定まった後も思考を続ける「過剰思考」は、トークン数と応答待ち時間を増やす。一方、途中の回答の確信度が高くなった瞬間に止めると、まだ検討が十分でない誤答を確定する危険がある。正答率も完全には維持していない。

- **2026-04 · [DepCap: Adaptive Block-Wise Parallel Decoding for Efficient Diffusion LM Inference](2026-2604.15750-depcap-adaptive-block-wise-parallel-decoding-for-efficient-diffusion-lm-.md)**  
  実装：[✓](https://github.com/X-Xia0828/DepCap) ・ リポジトリ内被引用：0  
  DepCapは、拡散言語モデル（DLM）が文章をブロック単位で生成する際の二つの判断、すなわち「次のブロックをどこまで伸ばすか」と「そのブロック内のどの位置を同時に確定するか」を、異なる予測信号から決める学習不要の推論方式である。

- **2026-04 · [Coverage-Based Calibration for Post-Training Quantization via Weighted Set Cover over Outlier Channels](2026-2604.24008-coverage-based-calibration-for-post-training-quantization-via-weighted-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CoverCal（Coverage-Based Calibration）は、LLMをAWQやGPTQでINT4事後量子化（PTQ）する際、どのサンプルを較正データとして選ぶかを改善する方式である。LLaMA-3-8BのAWQ INT4・128較正サンプルでは、MMLU 5-shot正答率がrandom 63.1%からCoverCal 64.6%へ改善した。

- **2026-04 · [ClawVM: Harness-Managed Virtual Memory for Stateful Tool-Using LLM Agents](2026-2604.10352-clawvm-harness-managed-virtual-memory-for-stateful-tool-using-llm-agents.md)**  
  実装：[✓](https://github.com/mpi-dsg/clawvm) ・ リポジトリ内被引用：0  
  ClawVMは、長時間稼働し外部ツールを使うLLMエージェントで、プロンプト文脈を高速・小容量の作業メモリ、永続ファイルを低速・大容量の退避先とみなし、状態の常駐・縮退・書戻しをエージェント実行基盤（agent harness）に強制する仕組みである。

- **2026-04 · [CLASP: Class-Adaptive Layer Fusion and Dual-Stage Pruning for Multimodal Large Language Models](2026-2604.12767-clasp-class-adaptive-layer-fusion-and-dual-stage-pruning-for-multimodal-.md)**  
  実装：[✓](https://github.com/Yunkaidang/CLASP) ・ リポジトリ内被引用：0  
  CLASP（Class-適応的 層 融合 and Dual-Stage Pruning）は、画像・動画を入力するマルチモーダルLLM（MLLM）の視覚トークンを、ユーザーの質問の種類に応じて削減する方式である。

- **2026-04 · [Characterizing Vision-Language-Action Models across XPUs: Constraints and Acceleration for On-Robot Deployment](2026-2604.24447-characterizing-vision-language-action-models-across-xpus-constraints-and.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、視覚・言語・行動モデル（Vision-Language-Action、VLA）をロボットに搭載するときの「制御周期内に推論を終えられるか」「何ワット時・いくらで実行できるか」という推論システムの問題を扱う。

- **2026-04 · [BOSCH: Black-Box Binary Optimization for Short-Context Attention-Head Selection in LLMs](2026-2604.05942-bosch-black-box-binary-optimization-for-short-context-attention-head-sel.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全注意（full 注意機構）の鍵・値キャッシュ（KV キャッシュ）は生成文脈とともに増大する。Qwen3 1.7B/8B/14B/30B-A3Bの4モデル、SWA率25/50/75/87.5%を用いた原著表1・2では、BOSCHは多くの設定で層単位の単純な交互配置や静的ヘッド順位より高いNIAH/LongBenchスコアを保つ。

- **2026-04 · [Attention Editing: A Versatile Framework for Cross-Architecture Attention Conversion](2026-2604.05688-attention-editing-a-versatile-framework-for-cross-architecture-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（Large Language モデル; LLM）の長文脈推論では、過去トークンの鍵・値（Key-Value; KV）を保存するメモリと、その読出し帯域が制約となる。グループ化問い合わせ注意（Grouped Query 注意機構; GQA）はKVヘッドの共有によって容量を抑えるが、長い系列や多数の同時要求ではKVが増え続ける。

- **2026-04 · [AgentOpt v0.1 Technical Report: Client-Side Optimization for LLM-Based Agent](2026-2604.06296-agentopt-v0-1-technical-report-client-side-optimization-for-llm-based-ag.md)**  
  実装：[✓](https://agentoptimizer.github.io/agentopt/) ・ リポジトリ内被引用：0  
  AgentOptは、複数のLLM呼び出しから成るエージェントのモデル選択を、開発者側の品質・遅延・API費用の制約に従って最適化する基盤である。9種類のモデルを2役割へ割り当てれば81通りになる。

- **2026-04 · [AEGIS: Scaling Long-Sequence Homomorphic Encrypted Transformer Inference via Hybrid Parallelism on Multi-GPU Systems](2026-2604.03425-aegis-scaling-long-sequence-homomorphic-encrypted-transformer-inference-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AEGISは、完全準同型暗号（fully homomorphic encryption; FHE）で暗号化した入力を復号せずにTransformerへ通す際、複数GPUへ暗号文を分配する方法を最適化するシステムである。

- **2026-04 · [Adaptive Parallel Monte Carlo Tree Search for Efficient Test-time Compute Scaling](2026-2604.00510-adaptive-parallel-monte-carlo-tree-search-for-efficient-test-time-comput.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  成功候補を早期発見した場合に打ち切る「正の早期終了」は効果があるが、いくら探索しても十分な報酬に達しない要求には効かず、同時処理時の長い裾の遅延が残る。推論サーバーvLLMへ統合し、4基のNVIDIA H100でLlama-3.1-8B-InstructとQwen2.5-14B-Instructを評価した。

- **2026-04 · [Absorber LLM: Harnessing Causal Synchronization for Test-Time Training](2026-2604.20915-absorber-llm-harnessing-causal-synchronization-for-test-time-training.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈の大規模言語モデルでは、生成済み履歴を鍵値キャッシュ（KV キャッシュ）へ蓄積すると、復号のたびに参照する過去位置が増える。この方式は推論時学習（test-time 学習）と長文脈推論の接点にある。

- **2026-03 · [TIDE: Token-Informed Depth Execution for Per-Token Early Exit in LLM Inference](2026-2603.21365-tide-token-informed-depth-execution-for-per-token-early-exit-in-llm-infe.md)**  
  実装：[✓](https://github.com/RightNow-AI/TIDE) ・ リポジトリ内被引用：0  
  TIDE（Token-Informed Depth Execution）は、学習済み大規模言語モデル（LLM）の中間層における隠れ状態が最終層の表現へ近づいたかを、後付けの小規模な二値分類器で判定する方式である。元の言語モデルの重みを変更せず、約2,000件のWikiText-103文による較正をA100上で約170秒で実行できる点が実装上の特徴である。

- **2026-03 · [The Missing Memory Hierarchy: Demand Paging for LLM Context Windows](2026-2603.09023-pichay-demand-paging-context-windows.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント文脈を仮想メモリとしてページングし、古いツール結果を追い出して再参照時に復元する透明プロキシ。139万追い出しで0.0254%フォルト率を報告。

- **2026-03 · [TERMINATOR: Learning Optimal Exit Points for Early Stopping in Chain-of-Thought Reasoning](2026-2603.12529-terminator-learning-optimal-exit-points-for-early-stopping-in-chain-of-t.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複雑な問題では思考が必要だが、答えが既に得られた後にも検算、別解探索、方針変更を続けることがある。実行時には未来の最終解答を参照せず、モデル最終層の隠れ状態から終了の可能性を予測し、複数トークンの多数決を経て を挿入する。Qwen3-8BのMATH-500では思考圧縮率45.1%（約54.9%削減）で、正答率91.1%から90.7%とほぼ同水準を維持した。

- **2026-03 · [TAPS: Task Aware Proposal Distributions for Speculative Sampling](2026-2603.27027-taps-task-aware-proposal-distributions-for-speculative-sampling.md)**  
  実装：[✓](https://github.com/Moe-Zbeeb/TAPS) ・ リポジトリ内被引用：0  
  さらに、複数の専門草稿をどう使い分けるべきかを、重み平均、確信度に基づく経路選択、草稿木の統合検証の三方式で検討する。

- **2026-03 · [Slow-Fast Inference: Training-Free Inference Acceleration via Within-Sentence Support Stability](2026-2603.12038-slow-fast-inference-training-free-inference-acceleration-via-within-sent.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  選択器は密注意のlogitから得た証拠と、KVに保存されたキーnorm・位置情報から得たpriorを統合する。Qwen3-4B、Qwen3-30B-A3B、Qwen3-235B-A22Bの長文脈デコードで、密注意と比較した実測スループットは文脈長に応じて約1.6〜14.4倍に増える。

- **2026-03 · [SkipOPU: An FPGA-based Overlay Processor for Large Language Models with Dynamically Allocated Computation](2026-2603.14785-skipopu-an-fpga-based-overlay-processor-for-large-language-models-with-d.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、非線形処理の待機を隠す融合データフロー、浮動小数点活性値と4ビット整数重みを扱うDSP演算器の高密度実装、層をまたいで変化しないKVを保持するオンチップ履歴バッファを一体設計した。AMD Alveo U280上のLlama2-7Bで140.8トークン/秒、帯域効率86.7%を報告する。

- **2026-03 · [SERQ: Saliency-Aware Low-Rank Error Reconstruction for LLM Quantization](2026-2603.08185-serq-saliency-aware-low-rank-error-reconstruction-for-llm-quantization.md)**  
  実装：[✓](https://github.com/acalabys/SERQ) ・ リポジトリ内被引用：0  
  SERQ（Saliency-Aware Low-Rank Error Reconstruction for LLM Quantization）は、LLMの線形層で重みと活性値をともに低ビット化した際の誤差を、小さな追加行列で補う後学習量子化（PTQ）手法である。

- **2026-03 · [Quasar: Quantized Self-Speculative Acceleration for Rapid Inference via Memory-Efficient Verification](2026-2603.01399-quasar-quantized-self-speculative-acceleration-for-rapid-inference-via-m.md)**  
  実装：[✓](https://github.com/Tom-HG/Quasar) ・ リポジトリ内被引用：0  
  Quasar（量子化 自己投機的 Acceleration for Rapid Inference）は、投機的復号（投機的復号）の下書き側ではなく、目標モデルによる検証側を8ビット量子化する方式である。検証がメモリ帯域に制限される条件では、下書き側だけを改善しても総生成時間の短縮に限界がある。

- **2026-03 · [Prompt Compression in Production Task Orchestration: A Pre-Registered Randomized Trial](2026-2603.23525-prompt-compression-in-production-task-orchestration-a-pre-registered-ran.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  評価対象は新しい圧縮モデルの開発でもGPUカーネルの高速化でもなく、指示のどの部分をどれだけ残すかという圧縮方針の費用対効果である。

- **2026-03 · [Pooling Engram Conditional Memory in Large Language Models using CXL](2026-2603.10087-pooling-engram-conditional-memory-in-large-language-models-using-cxl.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  条件付き記憶は言語モデルの条件付き記憶を、通常のTransformer計算から分離した大規模なN-gram埋め込み表で保持する。

- **2026-03 · [Multi-Head Low-Rank Attention](2026-2603.02188-multi-head-low-rank-attention.md)**  
  実装：[✓](https://github.com/SongtaoLiu0823/MLRA) ・ リポジトリ内被引用：0  
  長文脈の自己回帰型言語モデルでは、次トークンを出すたびに過去トークンのキー・値（KV）キャッシュを高帯域メモリ（HBM）から演算器近傍へ読み込む。多頭潜在注意（Multi-Head Latent 注意機構; MLA）はKVを低次元の潜在状態へ圧縮することで転送量を減らすが、元のMLAでは潜在KVが一つの共有状態として保持される。

- **2026-03 · [Mixture of Chapters: Scaling Learnt Memory in Transformers](2026-2603.21096-mixture-of-chapters-scaling-learnt-memory-in-transformers.md)**  
  実装：[✓](https://github.com/Tasmay-Tibrewal/Memory) ・ リポジトリ内被引用：0  
  Mixture of Chapters（MoC）は、言語モデルが事前学習で獲得する知識を、通常の重みとは別の学習可能な潜在記憶として保持し、入力に必要な部分だけを交差注意（cross-注意機構）で取り出す設計である。元のmain原稿にあった主要な正負両方の結果を維持し、計算量の内訳、選択単位、実施済み実験と将来計画の区別を明確化した。

- **2026-03 · [MASQuant: Modality-Aware Smoothing Quantization for Multimodal Large Language Models](2026-2603.04800-masquant-modality-aware-smoothing-quantization-for-multimodal-large-lang.md)**  
  実装：[✓](https://github.com/alibaba/EfficientAI) ・ リポジトリ内被引用：0  
  通常の文章向け平滑化量子化は、チャネルごとに一つのスケールを決め、活性の外れ値を重み側へ移して低ビット表現の誤差を減らす。

- **2026-03 · [LooComp: Leverage Leave-One-Out Strategy to Encoder-only Transformer for Efficient Query-aware Context Compression](2026-2603.09222-loocomp-leverage-leave-one-out-strategy-to-encoder-only-transformer-for-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかし検索件数を増やすと、無関係な文章も入力され、事前充填の計算量、入力トークン費用、モデルの注意の分散が問題になる。生成型の圧縮器は文書を短い文章へ書き換えられるが、圧縮器自体がトークンを逐次生成するため遅延が大きくなる。

- **2026-03 · [Locally Coherent Parallel Decoding in Diffusion Language Models](2026-2603.20216-locally-coherent-parallel-decoding-in-diffusion-language-models.md)**  
  実装：[✓](https://github.com/IBM/coherent-diffusion-local-autoregression) ・ リポジトリ内被引用：0  
  マスク拡散型の言語モデル（DLM）は、未確定トークンを一度に複数予測して反復的に確定できる。Dream-Coder-Instruct-7BとQwen3-0.6Bの組合せでは、HumanEvalのコード抽出失敗率が、1反復に8トークン確定する条件で基準DLMの70%からCoDiLAの16%へ低下した。

- **2026-03 · [KVSlimmer: Theoretical Insights and Practical Optimizations for Asymmetric KV Merging](2026-2603.00907-kvslimmer-theoretical-insights-and-practical-optimizations-for-asymmetri.md)**  
  実装：[✓](https://github.com/lianjunl13-sudo/KVSlimmer) ・ リポジトリ内被引用：0  
  古いトークンを単に捨てる方式は将来必要になる情報を回復できないため、近接したトークンの表現を統合して残す方法が検討されている。A100上ではAsymKV比で平均実行時間28%削減、チャンク512のピークGPUメモリ約29%削減を報告する。

- **2026-03 · [InfoDensity: Rewarding Information-Dense Traces for Efficient Reasoning](2026-2603.17310-infodensity-rewarding-information-dense-traces-for-efficient-reasoning.md)**  
  実装：[✓](https://github.com/amao0o0/InfoDensity) ・ リポジトリ内被引用：0  
  そこで、後方からの最大値包絡（suffix-max envelope）によって軌跡全体の形を要約し、同一問題に対する複数生成の相対的な長さで補正する報酬を設計した。原著表2では、DeepSeek-R1-Distill-Qwen-1.5Bの4ベンチマーク平均正答率が36.5%から50.8%へ上がり、平均生成長は11.1千から7.5千トークンへ短縮した。

- **2026-03 · [HiCI: Hierarchical Construction-Integration for Long-Context Attention](2026-2603.20843-hici-hierarchical-construction-integration-for-long-context-attention.md)**  
  実装：[✓](https://github.com/zengxyyu/HiCI) ・ リポジトリ内被引用：0  
  HiCI（Hierarchical Construction–Integration）は、長文脈言語モデルの注意機構を、セグメント単位の局所表現の構築、局所表現からの全体文脈の統合、全体と局所の情報を各セグメントへ再配信する処理へ分解する研究である。

- **2026-03 · [Gumbel Distillation for Parallel Text Generation](2026-2603.22216-gumbel-distillation-for-parallel-text-generation.md)**  
  実装：[✓](https://github.com/hxixixh/gumbel-distill) ・ リポジトリ内被引用：0  
  自己回帰言語モデル（autoregressive language モデル）は、前のトークンを条件に次の一個を順番に予測するため、隣接する語の依存関係を扱いやすい。例えば「San Francisco」を同時に予測する場合、「San」を選んだ条件で「Francisco」を選ぶという自己回帰的な関係が明示されない。

- **2026-03 · [Graph Signal Processing Meets Mamba2: Adaptive Filter Bank via Delta Modulation](2026-2603.22333-graph-signal-processing-meets-mamba2-adaptive-filter-bank-via-delta-modu.md)**  
  実装：[✓](https://github.com/yehjin-shin/HADES) ・ リポジトリ内被引用：0  
  トークン列を線状グラフとみなし、状態空間モデルの再帰ヘッドを時変フィルタとして解釈するGraph Signal Processing（グラフ信号処理）の観点から設計する。

- **2026-03 · [GradMem: Learning to Write Context into Memory with Test-Time Gradient Descent](2026-2603.13875-gradmem-learning-to-write-context-into-memory-with-test-time-gradient-de.md)**  
  実装：[✓](https://github.com/yurakuratov/gradmem) ・ リポジトリ内被引用：0  
  長文脈の大規模言語モデル（LLM）では、過去の情報を再利用するために鍵・値キャッシュ（KV キャッシュ）を保持するのが一般的である。しかしキャッシュは通常、層数と文脈長に比例して増える。GradMemはこの記憶形成を、単なる順伝播による要約ではなく、推論時に小さな記憶ベクトルへ勾配降下を行う最適化問題として定義する。モデル本体の重みは推論時に更新しない。

- **2026-03 · [Frequency-Modulated Visual Restoration for Matryoshka Large Multimodal Models](2026-2603.11220-frequency-modulated-visual-restoration-for-matryoshka-large-multimodal-m.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FMVR（Frequency-Modulated Visual Restoration）は、削減済み視覚表現の平均値からの残差と最大値からの残差をそれぞれ学習可能な係数で変調し、目立つ特徴と埋もれた特徴の両方を補強する方式である。原著表3では36トークン時に初期入力処理時間が58.1から18.0ミリ秒へ短縮し、総メモリが21.6から13.8GBへ減少する。

- **2026-03 · [ETA-VLA: Efficient Token Adaptation via Temporal Fusion and Intra-LLM Sparsification for Vision-Language-Action Models](2026-2603.25766-eta-vla-efficient-token-adaptation-via-temporal-fusion-and-intra-llm-spa.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数カメラの過去画像を視覚言語行動モデル（Vision-Language-Action モデル; VLA）へ入力すると、フレーム数とカメラ数に比例して視覚トークンが増える。主題は車両の制御アルゴリズムそのものよりも、VLAにおける視覚系列の効率的な処理である。

- **2026-03 · [Efficient Training-Free Multi-Token Prediction via Embedding-Space Probing](2026-2603.17942-efficient-training-free-multi-token-prediction-via-embedding-space-probi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ESP（Embedding-Space Probing）は、通常は次トークンだけを学習した自己回帰LLMから、重みを変更せずに複数の将来トークン候補を取り出すための推論時手法である。

- **2026-03 · [DASH: Dynamic Audio-Driven Semantic Chunking for Efficient Omnimodal Token Compression](2026-2603.15685-dash-dynamic-audio-driven-semantic-chunking-for-efficient-omnimodal-toke.md)**  
  実装：[✓](https://github.com/laychou666/DASH) ・ リポジトリ内被引用：0  
  LLMへ渡す前の入力列が長くなると、プリフィル（プリフィル）の注意演算とKVキャッシュのメモリ消費が増える。DASH（動的 Audio-driven Semantic cHunking）は、音声埋め込みの隣接トークンの変化を意味境界の手掛かりにし、音声と映像を可変長の区間へ分ける学習不要の圧縮方式である。

- **2026-03 · [CRISP: Compressed Reasoning via Iterative Self-Policy Distillation](2026-2603.05433-crisp-compressed-reasoning-via-iterative-self-policy-distillation.md)**  
  実装：[✓](https://github.com/HJSang/CRISP_Reasoning_Compression) ・ リポジトリ内被引用：0  
  CRISP（Compressed Reasoning via Iterative Self-Policy Distillation）は、この余分な思考を生成後に切り落とすのではなく、モデルが自発的に短い推論を出すように学習する方式である。

- **2026-03 · [Consensus-Expert DynamicMoE: ARIMA-based Capacity Prediction with Adaptive Load Balancing for Sparse Models](2026-dbb1f579343b-consensus-expert-dynamicmoe-arima-based-capacity-prediction-with-adaptiv.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  主要実験では、Switch Transformer-base-8の9種類のGLUE評価指標を単純平均した値が、従来構成の80.5、共有専門家だけを導入した構成の81.0に対して、提案構成で81.6となる（原著表4。

- **2026-03 · [ConFu: Contemplate the Future for Better Speculative Sampling](2026-2603.08899-confu-contemplate-the-future-for-better-speculative-sampling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ConFu（Contemplate the Future）は、投機的復号で候補を提案する軽量ドラフトモデルに、ターゲットモデルが推測する将来の生成方向を補助情報として渡す方式である。

- **2026-03 · [Confidence-Calibrated Small-Large Language Model Collaboration for Cost-Efficient Reasoning](2026-2603.03752-confidence-calibrated-small-large-language-model-collaboration-for-cost-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、小型言語モデル（SLM）にまず問題を解かせ、答えへの自己申告確信度が低いときだけ大型言語モデル（LLM）へ委譲する二段推論方式COREAを提案する。大型モデル単独との比較で、領域外の数理問題では推定費用21.5%減・正答率1.7ポイント減、非数理問題では16.8%減・正答率1.7ポイント減となった。

- **2026-03 · [CLAG: Adaptive Memory Organization via Agent-Driven Clustering for Small Language Model Agents](2026-2603.15421-clag-adaptive-memory-organization-via-agent-driven-clustering-for-small-.md)**  
  実装：[✓](https://github.com/dmis-lab/CLAG) ・ リポジトリ内被引用：0  
  CLAGは、記憶を話題ごとのクラスタへ割り当てるエージェント主導のルーティング、割当先クラスタ内だけでリンク生成・要約更新を行う局所的進化、質問に関連するクラスタを先に選んでから個別記憶を検索する二段階検索の三つを結合する。原著付録Cによれば、200件のBioASQ質問で二段階検索が除外した記憶は平均8.02%にとどまる。

- **2026-03 · [Characterizing Performance-Energy Trade-offs of Large Language Models in Multi-Request Workflows](2026-2604.09611-characterizing-performance-energy-trade-offs-of-large-language-models-in.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  新しい推論カーネルの提案ではなく、既存の推論基盤をどの条件でどう設定すると効率が変わるかを調べる。A100 40GB上でLlama-2-7Bを使い、入力長、出力長、バッチサイズ、GPU電力上限を変える。

- **2026-03 · [Capability-Guided Compression: Toward Interpretability-Aware Budget Allocation for Large Language Models](2026-2603.16440-capability-guided-compression-toward-interpretability-aware-budget-alloc.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル圧縮では重みの絶対値、活性値、曲率や再構成誤差を基準に枝刈り・量子化の強さを選ぶ。従来のWanda重要度とのスピアマン順位相関は−0.054だったものの、ヘッド除去によるパープレキシティ悪化との相関は有意でなく、50%保持ではCGC-Lのパープレキシティ27.87が均一枝刈り27.57より悪化した。

- **2026-03 · [Bielik-Minitron-7B: Compressing Large Language Models via Structured Pruning and Knowledge Distillation for the Polish Language](2026-2603.11881-bielik-minitron-7b-compressing-large-language-models-via-structured-prun.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの重み容量と計算費用を下げる方法には、数値精度を落とす量子化と、モデル構造自体を小さくする枝刈りがある。パラメータ削減率は33.4%である。

- **2026-03 · [Attention-Based Sampler for Diffusion Language Models](2026-2604.08564-attention-based-sampler-for-diffusion-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、マスク拡散型大規模言語モデル（dLLM）の生成時に、どの位置のマスクを先に確定するかを注意行列から決める学習不要の復号法Attn-Samplerを提案する。

- **2026-02 · [Understanding and Exploiting Weight Update Sparsity for Communication-Efficient Distributed RL](2026-2602.03839-understanding-and-exploiting-weight-update-sparsity-for-communication-ef.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）の強化学習による後学習（reinforcement learning post-学習）では、重みを更新する学習器（trainer）と、現在の方策を用いて回答を生成する推論ワーカー（inference worker）が分離されることが多い。

- **2026-02 · [TraceNAS: Zero-shot LLM Pruning via Gradient Trace Correlation](2026-2602.02891-tracenas-zero-shot-llm-pruning-via-gradient-trace-correlation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TraceNASは、事前学習済み大規模言語モデル（Large Language モデル、LLM）から層と内部チャネルを削除する構造的枝刈り（structured 枝刈り）において、候補構造を逐一学習させずに選ぶための探索方式である。

- **2026-02 · [Test-Time Scaling with Diffusion Language Models via Reward-Guided Stitching](2026-2602.22871-test-time-scaling-with-diffusion-language-models-via-reward-guided-stitc.md)**  
  実装：[✓](https://github.com/roymiles/diffusion-stitching) ・ リポジトリ内被引用：0  
  本論文はこの無駄に着目し、拡散言語モデルの安価な並列探索から中間ステップを再利用する仕組みを提案する。さらにピークメモリはQwen PRM構成で約42.8GB、比較AR単体の約14.4GBより大きい。

- **2026-02 · [StreamServe: Adaptive Speculative Flows for Low-Latency Disaggregated LLM Serving](2026-2604.09562-streamserve-adaptive-speculative-flows-for-low-latency-disaggregated-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分離型プリフィル・デコード上で、複数指標による要求ルーティングと実行時適応する投機深度を閉ループ連携し、4×A800評価でテンソル並列vLLM比の平均レイテンシ15.75倍短縮・平均スループット4.4倍を報告する。

- **2026-02 · [Stateful Token Reduction for Long-Video Hybrid VLMs](2026-2603.00198-stateful-token-reduction-for-long-video-hybrid-vlms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い動画を扱う視覚言語モデルでは、各フレームを多数の視覚トークンへ変換して言語モデルへ入力するため、動画が長くなると事前充填（プリフィル）の計算量とメモリが増大する。著者はこの現象を「状態付き圧縮」と捉え、浅い層では多くのトークンを保持し、深い層へ進むほど段階的に削減する方式を設計した。

- **2026-02 · [SR-TTT Does Not Learn Retrieval: A Correction and Mechanistic Post-Mortem of Surprisal-Aware Residual Test-Time Training](2026-2603.06642-sr-ttt-does-not-learn-retrieval-a-correction-and-mechanistic-post-mortem.md)**  
  実装：[✓](https://github.com/swamynathanvp/Surprisal-Aware-Residual-Test-Time-Training) ・ リポジトリ内被引用：0  
  本論文は、推論時学習（Test-Time 学習; TTT）を用いた長文系列モデルへ、驚き度（surprisal）に応じて選別したトークンを厳密なキー・バリュー（KV）キャッシュへ残す SR-TTT の初版（v1）を訂正し、その失敗を機構ごとに実験で切り分けた研究である。

- **2026-02 · [SPQ: An Ensemble Technique for Large Language Model Compression](2026-2602.18420-spq-an-ensemble-technique-for-large-language-model-compression.md)**  
  実装：[✓](https://github.com/JiaminYao/spq-compression) ・ リポジトリ内被引用：0  
  SPQ（SVD–枝刈り–量子化）は、大規模言語モデル（LLM）の重みメモリを削減する際、単一の圧縮手段をすべての層に一律に適用するのではなく、注意層には特異値分解（Singular Value Decomposition; SVD）による低ランク近似、フィードフォワード層（MLP）には活性統計に基づく構造的剪定…

- **2026-02 · [SimpleTool: Parallel Decoding for Real-Time LLM Function Calling](2026-2603.00030-simpletool-parallel-decoding-for-real-time-llm-function-calling.md)**  
  実装：[✓](https://github.com/HaxxorCialtion/SimpleTool) ・ リポジトリ内被引用：0  
  SimpleToolは、大規模言語モデルによる関数呼出し（function calling）の待ち時間を減らすために、出力表現の圧縮と並列復号（parallel デコード）を一緒に設計した手法である。

- **2026-02 · [SALAAD: Sparse And Low-Rank Adaptation via ADMM for Large Language Model Inference](2026-2602.00942-salaad-sparse-and-low-rank-adaptation-via-admm-for-large-language-model-.md)**  
  実装：[✓](https://github.com/HaoMAFRLu/salaad) ・ リポジトリ内被引用：0  
  SALAADは、言語モデルの重みを疎成分と低ランク成分の和として表現できるように事前学習中から構造を誘導し、配置時には必要なメモリ予算に応じて同じ学習済みチェックポイントを縮小できる方式である。

- **2026-02 · [Quant Experts: Token-aware Adaptive Error Reconstruction with Mixture of Experts for Large Vision-Language Models Quantization](2026-2602.24059-quant-experts-token-aware-adaptive-error-reconstruction-with-mixture-of-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像・テキストを統合処理するVision-Language モデル（VLM）を低ビットで推論する際、量子化された重み行列と活性値の積には誤差が生じる。

- **2026-02 · [QTALE: Quantization-Robust Token-Adaptive Layer Execution for LLMs](2026-2602.10431-qtale-quantization-robust-token-adaptive-layer-execution-for-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの推論負荷を下げるには、重みを少ないビットで保持する量子化（量子化）と、トークンごとに不要なTransformer層を省く動的層実行（トークン-適応的 層 execution）が補完的である。

- **2026-02 · [Pruning as a Cooperative Game: Surrogate-Assisted Layer Contribution Estimation for Large Language Models](2026-2602.07804-pruning-as-a-cooperative-game-surrogate-assisted-layer-contribution-esti.md)**  
  実装：[✓](https://github.com/920927/Pruning_As_A_Cooperative_Game) ・ リポジトリ内被引用：0  
  本論文は、推論時に実行するTransformer層を丸ごと減らす深さ方向の構造化枝刈り（depth-wise structured 枝刈り）を対象とする。

- **2026-02 · [PRISM: Parametrically Refactoring Inference for Speculative Sampling Draft Models](2026-2602.01762-prism-parametrically-refactoring-inference-for-speculative-sampling-draf.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（投機的復号）は、小型の草稿モデルに将来のトークンを提案させ、対象の大規模言語モデルがまとめて検証することで、対象モデルの逐次呼出し回数を減らす。

- **2026-02 · [OTPrune: Distribution-Aligned Visual Token Pruning via Optimal Transport](2026-2602.20205-otprune-distribution-aligned-visual-token-pruning-via-optimal-transport.md)**  
  実装：[✓](https://github.com/xiwenc1/OTPrune) ・ リポジトリ内被引用：0  
  OTPruneは、画像と言語を組み合わせて推論する多モーダル大規模言語モデルにおいて、画像から得られる多数の視覚トークンを追加学習なしで削減する手法である。原著が証明する約63%の最悪時近似保証は代理目的の最大化に対するものであり、元のワッサースタイン距離や言語モデルの回答品質が63%保証されるという意味ではない。

- **2026-02 · [On the Limits of Layer Pruning for Generative Reasoning in Large Language Models](2026-2602.01997-on-the-limits-of-layer-pruning-for-generative-reasoning-in-large-languag.md)**  
  実装：[✓](https://github.com/safal312/on-the-limits-of-layer-pruning) ・ リポジトリ内被引用：0  
  本研究は大規模言語モデルの層を丸ごと削る深さ方向の枝刈り（層 枝刈り）が、分類課題と生成型推論課題で異なる品質低下を起こす原因を調べる。主な実験では、層の約25%を除去し、元モデルが生成した回答を教師にして再学習する。

- **2026-02 · [Neural Attention Search Linear: Towards Adaptive Token-Level Hybrid Attention Models](2026-2602.03681-neural-attention-search-linear-towards-adaptive-token-level-hybrid-atten.md)**  
  実装：[✓](https://github.com/automl/NeuralAttentionSearchLinear) ・ リポジトリ内被引用：0  
  NAtS-L（Neural 注意機構 Search Linear）は、従来の「ある層はソフトマックス注意、別の層は線形注意」という固定的な混成構成を、同じ層の中で入力トークン塊ごとに注意演算を選択する構成へ拡張した研究である。

- **2026-02 · [Near-Oracle KV Selection via Pre-hoc Sparsity for Long-Context Inference](2026-2602.08329-near-oracle-kv-selection-via-pre-hoc-sparsity-for-long-context-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈LLMの自己回帰復号では、生成トークンが増えるほど各層・各ヘッドが参照する過去のKey/Value（KV）キャッシュが増え、注意演算の読み出しと集約が高コストになる。従来の近似方式は過去の注意分布や代理スコアから重要KVを予測するため、変化したクエリに必要なトークンを落とす危険がある。

- **2026-02 · [MoBiQuant: Mixture-of-Bits Quantization for Token-Adaptive Any-Precision LLM](2026-2602.20191-mobiquant-mixture-of-bits-quantization-for-token-adaptive-any-precision-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（Large Language モデル; LLM）の推論における重み量子化は、GPUメモリ容量と重み読み出し帯域を節約する一方、ビット幅を下げるほど丸め誤差を増やす。

- **2026-02 · [Minimizing Response Latency in LLM-Based Agent Systems: A Comprehensive Survey](2026-34369c1e45a2-minimizing-response-latency-in-llm-based-agent-systems-a-comprehensive-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  計画のための追加生成、メモリ検索、外部API、ツール結果の統合、複数エージェント間のメッセージ、推論サーバのキュー待ちが逐次・並列に組み合わさるためである。

- **2026-02 · [MentorCollab: Large-to-Small Inference-Time Mentorship for Concise Reasoning in Language Models](2026-2602.05307-mentorcollab-large-to-small-inference-time-mentorship-for-concise-reason.md)**  
  実装：[✓](https://github.com/haojinw0027/Mentorcollab) ・ リポジトリ内被引用：0  
  大型推論モデルは複雑な問題を解ける反面、解答までの思考列が長く、生成トークンの費用が増える。大型モデルが出力するトークンを小型モデルへ逐次注入する従来の協調方式では、大型モデルの「考え直し」「前段階への後戻り」まで取り込んでしまい、小型モデルの簡潔さを損なう場合がある。メンター由来のトークンが最終生成列に占める割合は平均18.4%と記述される。

- **2026-02 · [LLM-CoOpt: A Co-Design and Optimization Framework for Efficient LLM Inference on Heterogeneous Platforms](2026-2602.09323-llm-coopt-a-co-design-and-optimization-framework-for-efficient-llm-infer.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLM-CoOptは、一般的なGPUとはメモリ階層や実行単位が異なる計算装置にvLLMを移植したときの推論効率を改善するシステム最適化である。本文第4.3節の5種類のLLaMA系GPTQモデルでは、生成処理量が5.72～12.13%増加し、推論遅延が4.82～6.75%短縮した。

- **2026-02 · [Learning Query-Aware Budget-Tier Routing for Runtime Agent Memory](2026-2602.06025-learning-query-aware-budget-tier-routing-for-runtime-agent-memory.md)**  
  実装：[✓](https://github.com/ViktorAxelsen/BudgetMem) ・ リポジトリ内被引用：0  
  従来の記憶方式は履歴全体を事前に要約・索引化することが多いが、将来どの質問が来るかを知らずに情報を圧縮するため、不要な部分へ計算を費やしたり、後で必要になる詳細を失ったりする。

- **2026-02 · [LATMiX: Learnable Affine Transformations for Microscaling Quantization of LLMs](2026-2602.17681-latmix-learnable-affine-transformations-for-microscaling-quantization-of.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LATMiXは、低ビット量子化で問題になる活性値の外れ値を、量子化する前の可逆な座標変換によって緩和する事後量子化手法である。Qwen3-4BのMXFP4では単純GPTQの7課題平均62.11%に対しLATMiX-LUは64.74%、MXINT4では55.09%に対し63.63%である。

- **2026-02 · [Improving the Trade-off Between Watermark Strength and Speculative Sampling Efficiency for Language Models](2026-2602.01428-improving-the-trade-off-between-watermark-strength-and-speculative-sampl.md)**  
  実装：[✓](https://github.com/hwq0726/watermark-tradeoff) ・ リポジトリ内被引用：0  
  一方、投機的サンプリングは小型のドラフトモデルが先読みした複数トークンを大型ターゲットモデルがまとめて検証し、受理できたトークンの分だけ逐次的な大型モデル呼び出しを減らす。ELI5とC4、LlamaおよびGemmaの二組のモデルで、1検証ステップ当たりの受理トークン数が通常投機的サンプリングとほぼ同じで、検出性能も改善することを確認した。

- **2026-02 · [HyLRA: Hybrid Layer Reuse Attention for Efficient Long-Context Inference](2026-2602.00777-hylra-hybrid-layer-reuse-attention-for-efficient-long-context-inference.md)**  
  実装：[✓](https://anonymous.4open.science/r/unified-cache-management-CF80/) ・ リポジトリ内被引用：0  
  HyLRA（Hybrid 層 Reuse 注意機構）は、長い入力を参照しながら一語ずつ生成する際に、各Transformer層が毎回すべての過去トークンへ注意を計算する費用を減らす手法である。系列長60Kの総合処理量は全注意比1.45倍だが、8Kでは0.93倍に低下する。

- **2026-02 · [Greedy Multi-Path Block Verification for Faster Decoding in Speculative Sampling](2026-2602.16961-greedy-multi-path-block-verification-for-faster-decoding-in-speculative-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の方式は、草稿の先頭付近に受理されにくいトークンがあると、その後の候補が正しくても利用できない。A100 80GB上のOPT-6.7B/350MおよびOPT-6.7B/125Mでは、草稿長L=8、経路数K=3により、K=1のBVに対してトークン当たり実時間を6条件平均13.34%削減した。

- **2026-02 · [Focus-Scan-Refine: From Human Visual Perception to Efficient Visual Token Pruning](2026-2602.05809-focus-scan-refine-from-human-visual-perception-to-efficient-visual-token.md)**  
  実装：[✓](https://github.com/ILOT-code/FSR) ・ リポジトリ内被引用：0  
  高解像度画像や複数フレームの動画ではトークン数が増え、事前充填の演算量、注意機構に必要な記憶量、鍵・値キャッシュ（KV キャッシュ）の容量が増加する。LLaVA-1.5-7Bで視覚トークンを576個から64個へ削減すると、9種類の評価を正規化した平均性能保持率は96.1%であり、比較対象のCDPrunerは95.7%、VisPrunerは93.5%だった。

- **2026-02 · [Every Bit Counts: A Theoretical Study of Precision–Expressivity Tradeoffs in Quantized Transformers](2026-2602.02707-every-bit-counts-a-theoretical-study-of-precision-expressivity-tradeoffs.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、Transformerの量子化が単に近似誤差を増やすだけなのか、それとも十分な学習を行っても表現できない関数を生むのかを問う理論研究である。補助実験では、2ヘッド・埋め込み次元4の単層モデルに合成等値判定を学習させ、長さ100の課題で学習後量子化した場合、INT12の平均正答率94.95%に対してINT4は58.72%となる。

- **2026-02 · [Evaluating the Impact of Post-Training Quantization on Reliable VQA with Multimodal LLMs](2026-2602.13289-evaluating-the-impact-of-post-training-quantization-on-reliable-vqa-with.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像と言語を入力するマルチモーダル大規模言語モデル（MLLM）では、モデルの重みを低ビット量子化することで端末配置を容易にできる。VQAv2上のIdefics3ではbf16の精度79.3に対し、int4 HQQが77.2、int4 MBQが78.1、int3 HQQが64.0、int3 MBQが71.2となる。

- **2026-02 · [EntropyPrune: Matrix Entropy Guided Visual Token Pruning for Multimodal Large Language Models](2026-2602.17196-entropyprune-matrix-entropy-guided-visual-token-pruning-for-multimodal-l.md)**  
  実装：[✓](https://github.com/YahongWang1/EntropyPrune) ・ リポジトリ内被引用：0  
  既存の視覚トークン枝刈り（visual トークン 枝刈り）は重要そうなトークンを残すが、どの層で削除するかを経験的に固定するものが多く、異なるモデル・画像で最適な位置が変わる理由を説明しにくい。

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

- **2026-02 · [AttnPO: Attention-Guided Process Supervision for Efficient Reasoning](2026-2602.09953-attnpo-attention-guided-process-supervision-for-efficient-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AttnPO（注意機構-guided Policy Optimization）は、モデルが最終回答を生成するときに過去の思考のどの部分へ注意しているかを、思考段階ごとの重要性の代理指標として使う。

- **2026-02 · [Astro: Activation-guided Structured Regularization for Outlier-Robust LLM Post-Training Quantization](2026-2602.07596-astro-activation-guided-structured-regularization-for-outlier-robust-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Astroは、LLMの重みのみの事後量子化（重み-only PTQ）において、外れ値に由来する精度低下を抑えるための量子化前処理である。

- **2026-02 · [AgentArk: Distilling Multi-Agent Intelligence into a Single LLM Agent](2026-2602.03955-agentark-distilling-multi-agent-intelligence-into-a-single-llm-agent.md)**  
  実装：[✓](https://github.com/AIFrontierLab/AgentArk) ・ リポジトリ内被引用：0  
  複数のLLMエージェントが同じ問題を検討し、相互に批判・訂正して最終回答を合意する方式は、単独モデルより複雑な推論を改善できることがある。Qwen3、Gemma3、Llama3系を含む120の実験で、単一モデルに比べた推論品質の改善と、学習信号の種類・学生モデルの規模・教師エージェント数の影響を分析する。

- **2026-02 · [ACL: Aligned Contrastive Learning Improves BERT and Multi-exit BERT Fine-tuning](2026-2602.03563-acl-aligned-contrastive-learning-improves-bert-and-multi-exit-bert-fine-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文のACLは整合対照学習（aligned contrastive learning）であり、分類モデルの交差エントロピー損失と教師あり対照学習損失が異なる方向へ重みを更新してしまう問題を扱う。しかし著者はRTE分類の予備実験で、両損失から得られる勾配のなす角度が約75〜105度に分布し、互いに逆向きの成分を持つバッチが存在することを観察した。

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

- **2026-01 · [Superlinear Multi-Step Attention](2026-2601.18401-superlinear-multi-step-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈LLMの標準的なcausal self-注意機構は、系列長をLとするとプリフィル・学習時の注意計算が概ねO(L²)、1トークンの逐次デコードでも過去L個のKVを読むためO(L)となる。

- **2026-01 · [Speculative Sampling with Reinforcement Learning](2026-2601.12212-speculative-sampling-with-reinforcement-learning.md)**  
  実装：[✓](https://github.com/wmd3i/ReSpS) ・ リポジトリ内被引用：0  
  Re-SpS（Reinforcement Learning for 投機的 Sampling）は、投機的復号（投機的復号）における草稿木（下書き木）の全体トークン上限、深さ、分岐展開数を、文脈に応じて強化学習で切り替える方式である。

- **2026-01 · [SimMerge: Learning to Select Merge Operators from Similarity Signals](2026-2601.09473-simmerge-learning-to-select-merge-operators-from-similarity-signals.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数の重みを一つのモデルへ統合するモデル結合（モデル merging）は、複数モデルを同時常駐させずに能力をまとめる方法だが、どの結合演算子を使うか、どのチェックポイントを選ぶか、どの順番で結合するかによって結果が大きく変わる。

- **2026-01 · [RPIQ: Residual-Projected Multi-Collaboration Closed-Loop and Single Instance Quantization for Visually Impaired Assistance](2026-2601.02888-rpiq-residual-projected-multi-collaboration-closed-loop-and-single-insta.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RPIQ（Residual-Projected Multi-Collaboration Closed-Loop and Single Instance Quantization）は、視覚障害者向け支援を動機として、大規模言語モデルと視覚言語モデルを少ないメモリで利用するために提案された重みの事後量子化（post-学習 量子化、PTQ）手法である。

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

- **2026-01 · [Power-based Partial Attention: Bridging Linear-Complexity and Full Attention](2026-2601.17334-power-based-partial-attention-bridging-linear-complexity-and-full-attent.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、完全注意の二次計算量と局所窓注意の線形計算量の中間を、べき指数 p によって連続的に構成する「べき乗型部分注意（Power-based Partial 注意機構; PPA）」を提案する。MATH500では p=0 の67.4%から p=0.75 の79.8%、p=0.875 の82.4%へ上昇し、全注意 p=1 の80.8%に並ぶ。

- **2026-01 · [PLA-Serve: A Prefill-Length-Aware LLM Serving System](2026-a30e37ff7d4b-pla-serve-a-prefill-length-aware-llm-serving-system.md)**  
  実装：[✓](https://github.com/Jianshu-She/LAPS) ・ リポジトリ内被引用：0  
  プリフィル長で短要求と長要求を別キュー・別実行モードへ分離し、待機窓、CUDA Graph形状クラスタリング、動的GPU割当で短要求の待ちと長要求の干渉を同時に抑える。

- **2026-01 · [Mosaic: Unlocking Long-Context Inference for Diffusion LLMs via Global Memory Planning and Dynamic Peak Taming](2026-2601.06562-mosaic-unlocking-long-context-inference-for-diffusion-llms-via-global-me.md)**  
  実装：[✓](https://github.com/flashserve/Mosaic) ・ リポジトリ内被引用：0  
  Mosaicは、拡散型大規模言語モデル（diffusion-based Large Language モデル; dLLM）の長文脈生成で生じる、鍵・値キャッシュではなく一時活性化が容量の限界になるという問題を解く推論基盤である。過去KVを長期保持する手法だけでは、この大きな一時メモリを削れない。

- **2026-01 · [ModeX: Evaluator-Free Best-of-N Selection for Open-Ended Generation](2026-2601.02535-modex-evaluator-free-best-of-n-selection-for-open-ended-generation.md)**  
  実装：[✓](https://github.com/deeplearning-wisc/ModeX) ・ リポジトリ内被引用：0  
  しかし従来は、正解と照合できる数学問題なら多数決が使える一方、自由記述の要約やプログラムでは文字列の一致が品質を表さない。別の大規模言語モデルを採点器として呼ぶ方式は、その採点器の推論費用と誤判定を持ち込む。

- **2026-01 · [Low-Rank Key Value Attention](2026-2601.11471-low-rank-key-value-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低ランク鍵・値注意（Low-Rank Key Value 注意機構; LRKV）は、Transformerの各注意ヘッドが別々に保存する鍵・値（key/value; KV）キャッシュの重複を減らすため、各層に一組の共有射影を持たせ、ヘッド固有の違いだけを低ランク残差で表す注意機構である。

- **2026-01 · [LLM KV Cache Storage Using CXL Memory](2026-4885970e907b-llm-kv-cache-storage-using-cxl-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  vLLMとLMCacheのKVキャッシュを4種類のCXLメモリへ退避して実機比較し、DRAM型・プール型CXLが長文脈でシステムDRAMに近い性能を保ち、122K入力でGPU VRAM比約9倍の要求スループットを示す。

- **2026-01 · [GlimpRouter: Efficient Collaborative Inference by Glimpsing One Token of Thoughts](2026-2601.05110-glimprouter-efficient-collaborative-inference-by-glimpsing-one-token-of-.md)**  
  実装：[✓](https://github.com/Zengwh02/GlimpRouter) ・ リポジトリ内被引用：0  
  大規模推論モデルは長い思考過程を生成するため、回答までの待ち時間と計算費用が大きい。トークン単位で常時切り替えると、判定とモデル切替が頻繁になりやすい。

- **2026-01 · [Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning](2026-2601.09708-fast-thinkact-efficient-vision-language-action-reasoning-via-verbalizabl.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Fast-ThinkActは、視覚・言語・行動モデル（Vision-Language-Action モデル、VLA）の推論に必要な長い文章形式の思考列を、少数の連続潜在表現へ圧縮する研究である。

- **2026-01 · [Fast Forward: Accelerating LLM Prefill with Predictive FFN Sparsity](2026-2602.00397-fast-forward-accelerating-llm-prefill-with-predictive-ffn-sparsity.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FastForwardは、大規模言語モデル（Large Language モデル; LLM）の入力一括処理（プリフィル）におけるフィードフォワード網（Feed-順伝播 Network; FFN）の演算を、入力文脈に応じてブロック単位で省く方式である。

- **2026-01 · [Elastic Spectral State Space Models for Train-Once Budgeted Inference](2026-2601.22488-elastic-spectral-state-space-models-for-train-once-budgeted-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  異なるGPUや端末で同じ系列モデルを提供する場合、計算予算ごとに別の小型モデルを学習する方法は、学習費用とモデル管理の両方を増やす。学習済みの幅・層数を後から単純に削っても、小型化された部分が単独で有効な予測器になるとは限らない。学習後は成分の接頭辞を物理的に切り出し、別の学習やチャネル選別を行わずに、複数のパラメータ数・実行予算に対応する。

- **2026-01 · [Efficient Paths and Dense Rewards: Probabilistic Flow Reasoning for Large Language Models](2026-2601.09260-efficient-paths-and-dense-rewards-probabilistic-flow-reasoning-for-large.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  標準的な思考の連鎖は、最終解答の正誤だけでは途中の推論ステップの有用性を直接測れず、冗長な言い換えや誤った分岐を含みやすい。CoT-Flowは、問題xと時点iまでの生成列sを持つ状態Iiにおいて、正解yの負の対数確率 D(Ii)=-log p(y\|Ii) を難しさと定義する。

- **2026-01 · [Can Vision-Language Models Handle Long-Context Code? An Empirical Study on Visual Compression](2026-2602.00746-can-vision-language-models-handle-long-context-code-an-empirical-study-o.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LongCodeOCRは、長大なプログラムの文脈を削除型のテキスト圧縮で短くする代わりに、コード全体を二次元画像へ描画し、視覚言語モデル（Vision-Language モデル; VLM）で読ませる方式である。

- **2026-01 · [Attention Needs to Focus: A Unified Perspective on Attention Allocation](2026-2601.00919-attention-needs-to-focus-a-unified-perspective-on-attention-allocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者らは前者を注意の過負荷、後者を注意の過少負荷と呼び、両者を注意重みの配分失敗として統一的に扱う。提案手法Lazy 注意機構は二つの機構からなる。340Mパラメータ・150億学習トークンの8課題平均は48.01%で、比較対象のGated DeltaNetの47.68%を上回る。

- **2026-01 · [ArcAligner: Adaptive Recursive Aligner for Compressed Context Embeddings in RAG](2026-2601.05038-arcaligner-adaptive-recursive-aligner-for-compressed-context-embeddings-.md)**  
  実装：[✓](https://github.com/liunian-Jay/ArcAligner) ・ リポジトリ内被引用：0  
  ArcAlignerは、検索拡張生成（Retrieval-Augmented Generation; RAG）で取得した長文書を、少数の連続ベクトルへ圧縮した後の「情報が残っていても生成モデルが読めない」という問題を扱う。約24倍の文脈圧縮条件で、HotpotQAのF1は34.92、同じ論文で比較したCOCOMの16倍圧縮は31.77となった。

- **2026-01 · [APB-V: Accelerating Long-Video Understanding via Sequence-Parallelism-aware Approximate Attention](2026-2601.21444-apb-v-accelerating-long-video-understanding-via-sequence-parallelism-awa.md)**  
  実装：[✓](https://github.com/thunlp/APB) ・ リポジトリ内被引用：0  
  入力を間引く方式では一瞬しか映らない文字・物体・順序の手掛かりを失いやすい。原著のQwen2.5VL-3B・64フレーム・1440p動画の条件では、APB-VはFlashAttention比12.72倍、ZigZagRing比1.70倍、先行APB比1.18倍の処理量を報告する。

- **2026-01 · [Adaptive Layer Selection for Layer-Wise Token Pruning in LLM Inference](2026-2601.07667-adaptive-layer-selection-for-layer-wise-token-pruning-in-llm-inference.md)**  
  実装：[✓](https://github.com/TANIGUCHIREI/ASL) ・ リポジトリ内被引用：0  
  ASL（適応的選別層）は、長い入力を処理するTransformerのどの層でトークンを間引くべきかを、実行時の注意分布から判断する方式である。

- **2025-12 · [Zero-Overhead Introspection for Adaptive Test-Time Compute](2025-2512.01457-zero-overhead-introspection-for-adaptive-test-time-compute.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  数学推論などでは、同じ質問に対して複数の回答候補を生成し、多数決（Majority Voting）や最良候補選択（Best-of-N）で正答率を高められる。しかし固定個数の候補を最後まで生成すると、既に正しい回答が得られそうな簡単な質問でも計算を浪費し、失敗しそうな長い推論系列が全体の応答時間を引き延ばす。外部の報酬モデルを推論時に追加で走らせる必要はない。

- **2025-12 · [You Only Need Your Transformer 25% of the Time: Meaning-First Execution for Eliminating Unnecessary Inference](2025-2601.00847-you-only-need-your-transformer-25-of-the-time-meaning-first-execution-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の量子化、枝刈り、KVキャッシュ最適化、投機的復号は、モデルを実行することを前提に一回当たりの計算費用を削減する。論文は、1,000件の要求を用いた主実験で781件（78.1%）のTransformer実行を回避し、残り219件について無条件実行と完全一致する出力を得たと報告する。

- **2025-12 · [XLM: A Python package for non-autoregressive language models](2025-2512.17065-xlm-a-python-package-for-non-autoregressive-language-models.md)**  
  実装：[✓](https://github.com/dhruvdcoder/xlm-core) ・ リポジトリ内被引用：0  
  これに対して、非自己回帰言語モデルにはマスク拡散、挿入型生成、編集型生成など複数の方式がある。

- **2025-12 · [SASQ: Static Activation Scaling for Quantization-Aware Training in Large Language Models](2025-2512.14481-sasq-static-activation-scaling-for-quantization-aware-training-in-large-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低ビット量子化はモデルのメモリ容量や演算費用を減らすが、推論時に活性値の最大値を観測してスケールを更新する動的量子化では、毎回のスケール計算やデータ変換が発生する。

- **2025-12 · [RouteRAG: Efficient Retrieval-Augmented Generation from Text and Graph via Reinforcement Learning](2025-2512.09487-routerag-efficient-retrieval-augmented-generation-from-text-and-graph-vi.md)**  
  実装：[✓](https://github.com/YucanGuo/RouteRAG) ・ リポジトリ内被引用：0  
  RouteRAGは、言語モデルが推論途中に外部知識を調べる際、通常の文書検索、知識グラフ検索、両者の混合検索を状況に応じて切り替える方策を強化学習で獲得する検索拡張生成方式である。

- **2025-12 · [Rethinking Output Alignment For 1-bit Post-Training Quantization of Large Language Models](2025-2512.21651-rethinking-output-alignment-for-1-bit-post-training-quantization-of-larg.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（Large Language モデル; LLM）を事後量子化（Post-学習 量子化; PTQ）で1ビットへ圧縮すると、重みをほぼ±1に制限するため、4ビットなどの量子化より精度劣化が大きい。

- **2025-12 · [RADAR: Accelerate Large Language Model Inference With RL-Based Dynamic Draft Trees](2025-2512.14069-radar-accelerate-large-language-model-inference-with-rl-based-dynamic-dr.md)**  
  実装：[✓](https://github.com/minaduki-sora/RADAR) ・ リポジトリ内被引用：0  
  大規模言語モデルの逐次生成を高速化する投機的復号（投機的復号）は、小さな草稿モデルが将来の候補トークンを作り、大きな対象モデルがまとめて検証する。木構造の草稿を使うEAGLE-3では候補の枝を増やすことで検証一回当たりの採用長を延ばせるが、草稿モデルの呼出し回数を固定すると、既に有望な枝が乏しい状態でも計算を続けてしまう。

- **2025-12 · [Post-Training Quantization of OpenPangu Models for Efficient Deployment on Atlas A2](2025-2512.23367-post-training-quantization-of-openpangu-models-for-efficient-deployment-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単なる量子化誤差の研究ではなく、Ascendの演算子テンプレートライブラリCATLASSへ、量子化された重み配置、逆量子化、行列積を組み込み、不要な形式変換を避ける実行経路を構築する点が推論基盤上の寄与である。実測の前処理（プリフィル）では、バッチ32のFP16遅延5419msがINT8で3611msへ減少し、1.50倍の高速化となる。

- **2025-12 · [Parallel Decoder Transformer: Planner-Conditioned Latent Coordination for Model-Intrinsic Parallel Generation](2025-2512.10054-parallel-decoder-transformer-planner-conditioned-latent-coordination-for.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Parallel Decoder Transformer（PDT）は、モデル自身に三つの持続的な自己回帰生成前線を持たせる構造を提案する。重要な品質境界：本稿が確認した2026年7月18日改訂v3は、設計、実装、学習計画、評価プロトコルを記した研究であり、学習済みモデルの品質改善や実機速度向上を報告していない。

- **2025-12 · [OptRot: Mitigating Weight Outliers via Data-Free Rotations for Post-Training Quantization](2025-2512.24124-optrot-mitigating-weight-outliers-via-data-free-rotations-for-post-train.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPTQによる低ビット重み量子化では、極端に大きい重みが量子化スケールを押し広げ、通常の重みの再現精度を損なう。

- **2025-12 · [Multiscale Aggregated Hierarchical Attention (MAHA): A Game-Theoretic and Optimization-Driven Approach to Efficient Contextual Modeling in Large Language Models](2025-2512.14925-multiscale-aggregated-hierarchical-attention-maha-a-game-theoretic-and-o.md)**  
  実装：[✓](https://github.com/canererden/MAHA-Project) ・ リポジトリ内被引用：0  
  MAHA（Multiscale Aggregated Hierarchical 注意機構）は、入力トークンを複数の解像度へ縮約し、それぞれの尺度で注意を計算した後、尺度ごとの出力を凸最適化またはゲーム理論に基づく重みで統合する注意機構である。

- **2025-12 · [Modality Inflation: Energy Characterization and Optimization Opportunities for MLLM Inference](2025-2512.22695-modality-inflation-energy-characterization-and-optimization-opportunitie.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像入力を追加すると、視覚符号化器（vision encoder）が必要になるだけでなく、符号化結果が多数の視覚トークンとして言語モデルへ渡される。モデルはおおむね7B～8Bの言語モデル本体を持つが、視覚符号化器と画像のトークン化方式が異なる。代表的な条件では、画像入力によるエネルギー上乗せは17～94%の範囲だったと報告する。

- **2025-12 · [MIDUS: Memory-Infused Depth Up-Scaling](2025-2512.13751-midus-memory-infused-depth-up-scaling.md)**  
  実装：[✓](https://github.com/MLAI-Yonsei/midus-hml) ・ リポジトリ内被引用：0  
  MIDUS（メモリ-Infused Depth Up-Scaling）は、既存の言語モデルの層数を増やすDepth Up-Scaling（DUS）の追加パラメータと計算を削減するモデル拡張方式である。

- **2025-12 · [Mesh-Attention: A New Communication-Efficient Distributed Attention with Improved Data Locality](2025-2512.20968-mesh-attention-a-new-communication-efficient-distributed-attention-with-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Mesh-注意機構は、数十万から100万トークンの系列に対して注意機構を多数のGPUへ分割する際、各GPUが受け取る問い合わせ（Q）と鍵・値（KV）の転送量を同時に抑える分散注意アルゴリズムである。

- **2025-12 · [Interleaved Latent Visual Reasoning with Selective Perceptual Modeling](2025-2512.05665-interleaved-latent-visual-reasoning-with-selective-perceptual-modeling.md)**  
  実装：[✓](https://github.com/XD111ds/ILVR) ・ リポジトリ内被引用：0  
  既存の方法には、画像を切り出す外部道具を繰り返し呼ぶもの、中間画像を新たに生成するもの、画像の特徴を短い潜在ベクトルへ圧縮するものがある。Qwen2.5-VL-7Bでの原著評価では、COMTの平均正答率60.8%、VSPの正答率81.5%を達成し、静的潜在方式Mirageの56.0%・76.0%を上回った。

- **2025-12 · [Glance2Gaze: Efficient Vision-Language Models from Glance Fusion to Gaze Compression](2025-5f0897915cbf-glance2gaze-efficient-vision-language-models-from-glance-fusion-to-gaze-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  高解像度画像や動画では視覚トークン数が大きくなり、言語モデルの注意計算、鍵・値キャッシュ（KV キャッシュ）、初回トークン生成までの遅延が増加する。Glance2Gazeは、最初に画像全体を眺めて必要な細部へ視線を絞るという着想を二つの計算機構へ具体化する。

- **2025-12 · [ELANA: A Simple Energy and Latency Analyzer for LLMs](2025-2512.09946-elana-a-simple-energy-and-latency-analyzer-for-llms.md)**  
  実装：[✓](https://github.com/enyac-group/Elana) ・ リポジトリ内被引用：0  
  本論文は新しい推論アルゴリズムの高速化倍率を主張するものではなく、計測方法と計測例を提示する研究である。

- **2025-12 · [Efficient-VLN: A Simple yet Strong Baseline for Efficient Vision-Language Navigation](2025-2512.10310-efficient-vln-a-simple-yet-strong-baseline-for-efficient-vision-language.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論の中核は、回転位置埋め込み（Rotary Position Embedding; RoPE）を適用する前のKVをフレームごとに保存し、次の行動では必要な過去フレームのKVだけを選択して連続した位置IDで再回転する仕組みである。

- **2025-12 · [DiRL: An Efficient Post-Training Framework for Diffusion Language Models](2025-2512.22234-dirl-an-efficient-post-training-framework-for-diffusion-language-models.md)**  
  実装：[✓](https://github.com/OpenMOSS/DiRL) ・ リポジトリ内被引用：0  
  提案はこの問題を、ブロック間は自己回帰的、ブロック内は並列的な拡散という構造で扱う。著者は、学習処理の遅延を約6分の1にし、学習・推論の統合によって全体処理量を約2.5倍改善したと報告する。

- **2025-12 · [Demystifying LLM-as-a-Judge: Analytically Tractable Model for Inference-Time Scaling](2025-2512.19905-demystifying-llm-as-a-judge-analytically-tractable-model-for-inference-t.md)**  
  実装：[✓](https://github.com/I-Halder/Demystifying-LLM-as-a-Judge-Analytically-Tractable-Model-for-Inference-Time-Scaling) ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）の推論時に複数の回答を生成し、別の評価モデル（LLM-as-a-Judge）が良い回答を選ぶ方式は、学習済みのモデル重みを変更せずに品質を改善する手段である。

- **2025-12 · [Can LLMs Predict Their Own Failures? Self-Awareness via Internal Circuits](2025-2512.20578-can-llms-predict-their-own-failures-self-awareness-via-internal-circuits.md)**  
  実装：[✓](https://github.com/Amirhosein-gh98/Gnosis) ・ リポジトリ内被引用：0  
  回答文中の自己申告の確信度も、誤った回答に対して高い確信を示す問題がある。提案方式は、生成モデル本体の重みを変更せず、生成中に現れる隠れ状態（Hidden States）と注意重み（注意機構 Maps）の時系列的な特徴を抽出する。これは判定器の時間比較であり、回答を生成する言語モデル全体が37倍または99倍速くなるという意味ではない。

- **2025-12 · [Block Sparse Flash Attention](2025-2512.07011-block-sparse-flash-attention.md)**  
  実装：[✓](https://github.com/Danielohayon/Block-Sparse-Flash-Attention) ・ リポジトリ内被引用：0  
  Block-Sparse FlashAttention（BSFA）は、長文脈Transformerのプリフィルで、FlashAttention-2のブロックごとのQuery–Key（QK）スコアを正確に計算した後、重要度が低いブロックに対するValue（V）の読み出しと注意重み×Value（PV）行列積を省くCUDAカーネルである。<。

- **2025-11 · [Test-Time Temporal Sampling for Efficient MLLM Video Understanding](2025-2511.17945-test-time-temporal-sampling-for-efficient-mllm-video-understanding.md)**  
  実装：[✓](https://github.com/kaibinwang3/T3S) ・ リポジトリ内被引用：0  
  一方、学習済みフレーム選択器や動画専用圧縮器は追加学習と前処理が必要で、既存のMLLMへそのまま組み込めるとは限らない。Qwen2.5-VL-7BでLongVideoBenchの正答率は59.2%から62.3%へ3.1ポイント改善し、論文が測る最初のトークンまでの遅延は2.04倍高速化した。

- **2025-11 · [T-SAR: A Full-Stack Co-design for CPU-Only Ternary LLM Inference via In-Place SIMD ALU Reorganization](2025-2511.13676-t-sar-a-full-stack-co-design-for-cpu-only-ternary-llm-inference-via-in-p.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  T-SARは、重みを−1、0、+1の三値に制約した大規模言語モデル（LLM）を、専用の大きな行列演算器なしにCPUで高速実行するための、アルゴリズム・命令セット・マイクロアーキテクチャ・ソフトウェアの協調設計である。

- **2025-11 · [Symbiosis: Multi-Adapter Inference and Fine-Tuning](2025-2507.03220-symbiosis-multi-adapter-inference-and-fine-tuning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Symbiosisは、基盤モデルの凍結層を共有サービスへ分離し、利用者固有の注意・アダプタ・状態を各clientに残す設計によって、推論と微調整を同じ仕組みで扱う。

- **2025-11 · [Streaming Tensor Programs: A Streaming Abstraction for Dynamic Parallelism](2025-2511.07776-streaming-tensor-programs-a-streaming-abstraction-for-dynamic-parallelis.md)**  
  実装：[✓](https://github.com/stanford-ppl/step_artifact) ・ リポジトリ内被引用：0  
  SDAは演算器とメモリをチップ上へ分散配置し、演算間を先入先出のストリームで接続する。著者はMixtral-8x7B、Qwen3-30B-A3BのMoE層と全モデル、AzureLLMInferenceDataset由来のKV長分布を用い、サイクル近似シミュレータで評価する。

- **2025-11 · [R2Q: Towards Robust 2-Bit Large Language Models via Residual Refinement Quantization](2025-2511.21736-r2q-towards-robust-2-bit-large-language-models-via-residual-refinement-q.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  R2Q（Residual Refinement Quantization）は、2ビットの重み量子化を1回の4値への丸めではなく、元重みを二値近似した後、その残差をさらに二値近似する2段階へ分解する方式である。2ビットで品質を完全に保てる方式ではなく、比較対象の崩壊が極端な条件で改善幅が大きく見える点を区別する必要がある。

- **2025-11 · [NeuroPath: Neurobiology-Inspired Path Tracking and Reflection for Semantically Coherent Retrieval](2025-2511.14096-neuropath-neurobiology-inspired-path-tracking-and-reflection-for-semanti.md)**  
  実装：[✓](https://github.com/KennyCaty/NeuroPath) ・ リポジトリ内被引用：0  
  知識グラフ（Knowledge Graph; KG）上の隣接性だけを重視する既存方式は、質問に答えるための関係の向きや意味を無視して文書を集める場合がある。原著の多段質問応答3データセットでは、主要なグラフ検索方式に比べて平均Recall@2を16.3%、Recall@5を13.5%改善したと報告する。

- **2025-11 · [Layer-Wise High-Impact Parameter Ratio Optimization in Post-Training Quantization for Large Language Models](2025-2511.17801-layer-wise-high-impact-parameter-ratio-optimization-in-post-training-qua.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、大規模言語モデルを2〜3ビット程度の重み精度に縮小するとき、少数の高感度な重みが量子化誤差を増幅する問題を扱う。

- **2025-11 · [DeepCoT: Deep Continual Transformers for Real-Time Inference on Data Streams](2025-2511.17693-deepcot-deep-continual-transformers-for-real-time-inference-on-data-stre.md)**  
  実装：[✓](https://github.com/Atamarado/deepcot) ・ リポジトリ内被引用：0  
  DeepCoT（Deep Continual Transformer）は、映像・音声・テキストのストリームを移動窓で逐次処理する際、深いTransformerエンコーダで繰り返される過去トークンの計算を減らす方式である。原著のオンライン行動検出では通常のTransformerに対して23.65倍の相対実行速度、音楽分類では37.24倍を報告する。

- **2025-11 · [BudgetMem: Training-Free Selective Memory for Cost-Efficient Long-Context Processing in Language Models](2025-2511.04919-budgetmem-training-free-selective-memory-for-cost-efficient-long-context.md)**  
  実装：[✓](https://github.com/Chandra-Alla/BudgetMem-paper) ・ リポジトリ内被引用：0  
  大規模言語モデル（Large Language モデル; LLM）の長文脈処理では、全入力をモデルへ投入すると注意計算・メモリ・料金が増える。トークン単位の圧縮器では、語句が断片的に残ることで検索に必要な語順や句のまとまりが失われる場合がある。既定の保持比率は30%であり、残した断片をBM25検索索引に格納する。

- **2025-11 · [Beyond Dynamic Quantization: An Efficient Static Hierarchical Mix-precision Framework for Near-Lossless LLM Compression](2025-84553b047243-beyond-dynamic-quantization-an-efficient-static-hierarchical-mix-precisi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの推論で重みと活性を低ビット化すると、転送するデータ量と行列積の計算負荷を減らせる。ただし少数の極端に大きな値（外れ値）に量子化範囲を合わせると、多数の通常値に割り当てられる表現段階が粗くなり、生成品質が損なわれる。主要な評価条件は、重みの80%を4ビット、20%を8ビット、活性を8ビットとするW4.8A8である。

### 2年前（2024-11〜2025-10）

- **2025-08 · [Dream 7B: Diffusion Large Language Models](2025-2508.15487-dream-7b-diffusion-large-language-models.md)**  
  実装：[✓](https://github.com/DreamLM/Dream) ・ リポジトリ内被引用：90  
  自己回帰モデルから初期化した70億拡散言語モデルで、系列全体の反復復元により計画課題と任意順生成を強化し、推論反復数で品質と速度を調整する。

- **2025-03 · [Block Diffusion: Interpolating Between Autoregressive and Diffusion Language Models](2025-2503.09573-block-diffusion-interpolating-between-autoregressive-and-diffusion-langu.md)**  
  実装：[✓](https://github.com/kuleshov-group/bd3lms) ・ リポジトリ内被引用：76  
  マスク率をデータに応じて区間制限する学習方式と、清浄系列・雑音系列を特殊注意で同時処理する実装を導入した。

- **2025-09 · [Fast-dLLM v2: Efficient Block-Diffusion LLM](2025-2509.26328-fast-dllm-v2-block-diffusion-hierarchical-cache.md)**  
  実装：[✓](https://github.com/NVlabs/Fast-dLLM/tree/main/v2) ・ リポジトリ内被引用：46  
  自己回帰モデルをブロック拡散へ少量追加学習し、ブロック間KVキャッシュとブロック内DualCache、信頼度並列復号を階層化して品質を保ちながら生成を高速化する。

- **2025-01 · [Titans: Learning to Memorize at Test Time](2025-2501.00663-titans-learning-to-memorize-at-test-time.md)**  
  実装：✓ ・ リポジトリ内被引用：37  
  長い系列を処理する言語モデルでは、直近の情報を精密に参照する短期記憶と、遠い過去から重要な情報を残す長期記憶の両立が難しい。一方、線形再帰型モデルは過去を小さな状態へ圧縮できるが、重要な出来事をどのように選択して長く保持するかに制約がある。

- **2025-03 · [L1: Controlling How Long A Reasoning Model Thinks With Reinforcement Learning](2025-2503.04697-l1-controlling-how-long-a-reasoning-model-thinks-with-reinforcement-lear.md)**  
  実装：[✓](https://github.com/cmu-l3/l1) ・ リポジトリ内被引用：33  
  長い思考は難問での正答率を上げ得るが、単純な問題に数千トークンを費やすと不要な逐次生成が増える。著者が提案する長さ制御方策最適化（Length Controlled Policy Optimization、LCPO）には二種類ある。指定長との平均偏差は数学課題で約3%である。

- **2024-12 · [Token-Budget-Aware LLM Reasoning](2024-2412.18547-token-budget-aware-llm-reasoning.md)**  
  実装：[✓](https://github.com/GeniusHTX/TALE) ・ リポジトリ内被引用：31  
  そこで問題ごとに適切な予算を推定する推論時方式TALE-EPと、適切な予算下の短い正答を学習させる事後学習方式TALE-PTを提案する。

- **2025-02 · [TokenSkip: Controllable Chain-of-Thought Compression in LLMs](2025-2502.12067-tokenskip-controllable-chain-of-thought-compression-in-llms.md)**  
  実装：[✓](https://github.com/hemingkx/TokenSkip) ・ リポジトリ内被引用：29  
  思考連鎖（Chain-of-Thought、CoT）は、複雑な数学や論理の問題を段階的に解くことで大規模言語モデルの正答率を改善する。保持率を条件として複数の圧縮版を学習させ、推論時に指定した保持率に応じて短い思考列をモデル自身が直接生成するようにする。

- **2025-08 · [Diffusion LLMs Can Do Faster-Than-AR Inference via Discrete Diffusion Forcing](2025-2508.09192-diffusion-llms-can-do-faster-than-ar-inference-via-discrete-diffusion-fo.md)**  
  実装：[✓](https://github.com/zhijie-group/Discrete-Diffusion-Forcing) ・ リポジトリ内被引用：27  
  離散拡散型の大規模言語モデル（diffusion LLM、dLLM）は、マスクされた複数トークンを一度の推論で同時に予測できる。しかし従来の双方向注意を使う拡散モデルでは、マスクの状態が反復ごとに変わるため、過去の鍵・値（KV）を自己回帰型モデルのように正確にキャッシュしにくい。確定済みのブロックのKVは変更されないため正確に再利用できる。

- **2025-03 · [Qwen2.5-Omni Technical Report](2025-2503.20215-qwen2-5-omni-technical-report.md)**  
  実装：[✓](https://github.com/QwenLM/Qwen2.5-Omni) ・ リポジトリ内被引用：27  
  従来の視覚言語モデルや音声言語モデルを単に接続すると、動画フレームと音声の時間対応が失われやすく、音声出力のために全文の生成完了を待つ設計では初回音声までの遅延が大きい。原著の7B級モデルは、音声・映像を混合するOmniBenchで平均56.13%を示し、比較表のGemini 1.5 Proの42.91%を上回った。

- **2025-02 · [Training Language Models to Reason Efficiently](2025-2502.04463-training-language-models-to-reason-efficiently.md)**  
  実装：[✓](https://github.com/Zanette-Labs/efficient-reasoning) ・ リポジトリ内被引用：26  
  長い思考過程を生成する推論モデルは、難しい問題で高い正答率を得られる一方、簡単な問題でも冗長な検討を続けることがある。本論文は、正答を優先したまま正解応答の長さに罰則を与えるオンライン強化学習を提案する。7Bの5タスク平均では、長さ罰則 $\alpha=0.2$ の場合、基準モデルに対して生成トークン数が51.58%、正答率が95.94%となった。

- **2024-12 · [C3oT: Generating Shorter Chain-of-Thought without Compromising Effectiveness](2024-2412.11664-c3ot-generating-shorter-chain-of-thought-without-compromising-effectiven.md)**  
  実装：✓ ・ リポジトリ内被引用：25  
  C3oT（Conditioned Compressed Chain-of-Thought）は、言語モデルが回答の前に生成する長い思考連鎖（Chain of Thought、CoT）を短くしながら、長い思考で獲得した推論能力を保持するための条件付き学習方式である。

- **2025-07 · [Step-3 is Large yet Affordable: Model-system Co-design for Cost-effective Decoding](2025-2507.19427-step-3-is-large-yet-affordable-model-system-co-design-for-cost-effective.md)**  
  実装：[✓](https://github.com/stepfun-ai/StepMesh) ・ リポジトリ内被引用：24  
  単純に総パラメータや活性パラメータを減らすのではなく、モデルの注意機構とサービング時のGPU配置を一緒に設計し、長い思考系列の復号費用を下げる。

- **2025-02 · [CoT-Valve: Length-Compressible Chain-of-Thought Tuning](2025-2502.09601-cot-valve-length-compressible-chain-of-thought-tuning.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  CoT-Valveは、推論モデルが簡単な問題にも長い思考連鎖（Chain of Thought、CoT）を生成してしまう無駄を減らし、同じ重みを基盤とするモデルで思考列の長さを柔軟に変える手法である。

- **2025-02 · [Chain of Draft: Thinking Faster by Writing Less](2025-2502.18600-chain-of-draft-thinking-faster-by-writing-less.md)**  
  実装：[✓](https://github.com/sileix/chain-of-draft) ・ リポジトリ内被引用：22  
  Chain of 下書き（CoD）は、推論連鎖（Chain-of-Thought; CoT）の冗長な自然言語を減らし、必要な中間計算だけを短いドラフトとして生成させるprompting方式である。

- **2024-12 · [Compressed Chain of Thought: Efficient Reasoning Through Dense Representations](2024-2412.13171-compressed-chain-of-thought-efficient-reasoning-through-dense-representa.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  本研究は、言語モデルの推論精度を高めるために長い自然言語の思考連鎖（Chain of Thought; CoT）を生成すると、回答前の自己回帰復号に多くの時間がかかる問題を扱う。自然言語の思考文を一度すべて生成してから圧縮する方式ではない。

- **2025-09 · [Qwen3-Omni Technical Report](2025-2509.17765-qwen3-omni-technical-report.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  Qwen3-Omniは、テキスト、画像、音声、動画の入力を統合し、テキスト応答と音声応答を生成する大規模多モーダルモデルである。原著の理論的な初回パケット遅延は、同時要求1件で音声入力234ms、動画を含む入力547msである。

- **2025-04 · [Reasoning Models Can Be Effective Without Thinking](2025-2504.09858-reasoning-models-can-be-effective-without-thinking.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  大規模推論モデルは、最終回答の前に長い思考列（chain of thought、CoT）を生成することで数学、プログラミング、定理証明の精度を高めている。形式定理証明では長い思考より3.3～3.7倍少ないトークンで同程度のpass@kを得る。

- **2025-10 · [dInfer: An Efficient Inference Framework for Diffusion Language Models](2025-2510.08666-dinfer-an-efficient-inference-framework-for-diffusion-language-models.md)**  
  実装：[✓](https://github.com/inclusionAI/dInfer) ・ リポジトリ内被引用：18  
  拡散型LLM（dLLM）の反復的な雑音除去（denoising）・並列トークン確定・更新され続けるKVをモジュール化し、デコーダ/KV管理とGPU実行系を同時最適化するdInfer。

- **2025-02 · [CODI: Compressing Chain-of-Thought into Continuous Space via Self-Distillation](2025-2502.21074-codi-compressing-chain-of-thought-into-continuous-space-via-self-distill.md)**  
  実装：[✓](https://github.com/zhenyi4/codi) ・ リポジトリ内被引用：17  
  CODI（Continuous Chain-of-Thought via Self-Distillation）は、推論過程を自然言語の単語列として毎回生成する費用を減らすため、明示的な思考連鎖（Chain-of-Thought; CoT）を少数の連続潜在状態へ移す学習方式である。

- **2024-12 · [ArkVale: Efficient Generative LLM Inference with Recallable Key-Value Eviction](2024-001c0516e00c-arkvale-efficient-generative-llm-inference-with-recallable-key-value-evi.md)**  
  実装：[✓](https://github.com/pku-liang/ArkVale) ・ リポジトリ内被引用：15  
  大規模言語モデル（Large Language モデル; LLM）が長い文章を扱うと、注意機構の鍵・値キャッシュ（Key-Value キャッシュ; KVキャッシュ）は入力文脈の長さと同時処理要求数に比例して増える。

- **2025-10 · [DeepSeek-OCR: Contexts Optical Compression](2025-2510.18234-deepseek-ocr-contexts-optical-compression.md)**  
  実装：[✓](https://github.com/deepseek-ai/DeepSeek-OCR) ・ リポジトリ内被引用：14  
  本研究は、長いテキストをそのまま多数の言語トークンとして処理する代わりに、文書を二次元の画像として扱い、少数の視覚トークンへ圧縮できるかを検証する。英語文書のFox評価では、画像化した元テキストの約10倍圧縮に相当する視覚トークン数でも文字復元精度がおおむね97%に達する。

- **2024-12 · [NVILA: Efficient Frontier Visual Language Models](2024-2412.04468-nvila-efficient-frontier-visual-language-models.md)**  
  実装：[✓](https://github.com/NVlabs/VILA) ・ リポジトリ内被引用：13  
  NVILAは解像度を先に上げて必要な情報を取り込み、その後に空間・時間方向の冗長性を圧縮する「拡大してから圧縮する（scale-then-compress）」設計を採用する。

- **2025-05 · [Llama-Nemotron: Efficient Reasoning Models](2025-2505.00949-llama-nemotron-efficient-reasoning-models.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  Nano（80億）、Super（490億）、Ultra（2530億）の3規模を提供し、通常の会話と詳細な推論を同じモデルで切り替えられる。実測ではSuperが単一H100上、バッチ256の指定条件で元のLlama 3.3-70Bに対して5倍のスループットを報告し、Ultraは8枚のH100で元のLlama 3.1-405Bに対して1.71倍の遅延改善を得た。

- **2025-08 · [Huawei Cloud Model-as-a-Service on the CloudMatrix384 SuperPod](2025-2508.02520-huawei-cloud-model-as-a-service-on-the-cloudmatrix384-superpod.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  xDeepServe（XDS）は、Huawei Cloudが大規模Mixture-of-Experts（MoE）モデルを提供するためのモデル-as-a-Service（MaaS）配信システムである。

- **2025-06 · [MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents](2025-2506.15841-mem1-learning-to-synergize-memory-and-reasoning-for-efficient-long-horiz.md)**  
  実装：[✓](https://github.com/MIT-MI/MEM1) ・ リポジトリ内被引用：9  
  従来の全履歴追記方式では、過去の検索結果が毎ターンのプロンプトへ残るため、文脈長に比例して鍵値キャッシュの容量が増え、注意計算や再入力の費用も高くなる。16目標の多段質問応答では、Qwen2.5-14B-Instructの完全一致数0.567に対しMEM1は1.97、ピークトークン数は3,840に対し1,040、推論時間は29.7秒に対し8.70秒だった。

- **2025-06 · [MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention](2025-2506.13585-minimax-m1-scaling-test-time-compute-efficiently-with-lightning-attentio.md)**  
  実装：[✓](https://github.com/MiniMax-AI/MiniMax-M1) ・ リポジトリ内被引用：7  
  MiniMax-M1は、推論時に長い思考過程を生成する大規模言語モデルで、生成トークンが増えるほど従来のSoftmax注意の計算・記憶費用が膨らむ問題に対処する。モデル全体は4560億パラメータ、トークンごとの活性化は459億パラメータの混合専門家モデル（Mixture of エキスパート、MoE）である。

- **2025-09 · [Learning to Parallel: Accelerating Diffusion Large Language Models via Learnable Parallel Decoding](2025-2509.25188-learning-to-parallel-accelerating-diffusion-large-language-models-via-le.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  これに対してマスク型拡散言語モデルは、あるブロック内の複数トークンを一度に予測し、まだ不確かな位置だけを再びマスクして次の反復で更新する。

- **2025-05 · [GMSA: Enhancing Context Compression via Group Merging and Layer Semantic Alignment](2025-2505.12215-gmsa-enhancing-context-compression-via-group-merging-and-layer-semantic-.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  GMSAは、原文を文字列として間引くのではなく、少数の連続表現トークン（soft トークン）へ変換する文脈圧縮方式である。NaturalQuestionsの4倍圧縮では完全一致（Exact Match、EM）が58.12%で、元文脈をそのまま与える条件の15.07%を上回った。

- **2025-04 · [PLD+: Accelerating LLM Inference by Leveraging Language Model Artifacts](2025-1e04c2f7fc65-pld-accelerating-llm-inference-by-leveraging-language-model-artifacts.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  PLD+（プロンプト Lookup Decoding+）は、入力文脈の一部がそのまま出力にも現れる場合に、過去の入力トークン列を将来の出力候補として再利用する投機的復号法である。例えばコード編集で改行やインデント、識別子が何度も現れると、従来のPLDが最長の局所的な文字列一致だけで候補を選ぶと、同じ記号が出る別の場所を誤選択し、検証に失敗する。

- **2025-08 · [Towards Efficient and Practical GPU Multitasking in the Era of LLM](2025-2508.08448-towards-efficient-and-practical-gpu-multitasking-in-the-era-of-llm.md)**  
  実装：[✓](https://github.com/ovg-project) ・ リポジトリ内被引用：5  
  この論文は、GPUの単独実行（Singletasking）から多重実行（Multitasking）への移行を主張する設計論・立場論文（Position Paper）である。本文の「10%まで下がる利用率」やGPU世代間の成長率は背景の参考値であり、提案法がGPU使用率を何ポイント改善したという実験結果ではない。

- **2025-01 · [Rope to Nope and Back Again: A New Hybrid Attention Strategy](2025-2501.18795-rope-to-nope-and-back-again-a-new-hybrid-attention-strategy.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  大規模言語モデル（large language モデル; LLM）で長い入力を処理すると、全トークン同士の注意（注意機構）計算は入力長Lの二乗に近い費用を要する。長文脈評価では256Kトークンでの検索・質問応答が改善し、局所層を増やすことで長文推論時のキー・値キャッシュ（key-value キャッシュ; KVキャッシュ）も減らせる。

- **2025-10 · [xLLM Technical Report](2025-2510.14686-xllm-technical-report.md)**  
  実装：[✓](https://github.com/jd-opensource/xllm) ・ リポジトリ内被引用：4  
  原著のDeepSeek-R1、プリフィル/デコード分離、入力2048／出力2048トークン、TPOT上限100msの表3では、MindIEが8476.44 トークン/s、xLLMが11351.58 トークン/sとなり、同じ制約下で約33.9%の改善を示した。

- **2025-02 · [LLM Bandit: Cost-Efficient LLM Generation via Preference-Conditioned Dynamic Routing](2025-2502.02743-llm-bandit-cost-efficient-llm-generation-via-preference-conditioned-dyna.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  安価なモデルだけを使えば費用を抑えられるが、難しい質問で誤答が増える。複数モデルを順番に呼び出すカスケード方式は品質を確認してから高価なモデルへ移れる一方、複数回の推論が必要になる。

- **2024-12 · [Flash Communication: Reducing Tensor Parallelization Bottleneck for Fast Large Language Model Inference](2024-2412.04964-flash-communication-reducing-tensor-parallelization-bottleneck-for-fast-.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  大規模モデルでは行列積の後に各GPUの部分結果を集約する必要があり、GPU間の接続帯域が低い環境では、この通信が前段入力処理（プリフィル）の主要な待ち時間になる。提案方式は、活性値を細粒度に量子化して転送量を削減し、リング型の逐次的な集約ではなく、全対全による分散集約とAll-Gatherによる結果配布を二段階で行う。

- **2025-10 · [Not All Bits Are Equal: Scale-Dependent Memory Optimization Strategies for Reasoning Models](2025-2510.10964-not-all-bits-are-equal-scale-dependent-memory-optimization-strategies-fo.md)**  
  実装：[✓](https://github.com/krafton-ai/not-all-bits-are-equal) ・ リポジトリ内被引用：3  
  長い思考列を出力する推論モデルでは、量子化してモデル重みを小さくすれば常に省メモリで高性能になる、という通常の指針が成立しない。原著のQwen3-4Bでは、4bit重みが2.49 GBであるのに対し、32kトークン相当のKVキャッシュは4.42 GBと約1.8倍に達する（原著§1）。

- **2025-10 · [Mixed-Precision Quantization for Language Models: Techniques and Prospects](2025-2510.16805-mixed-precision-quantization-for-language-models-techniques-and-prospect.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  量子化はモデル重み・活性・KVキャッシュの数値精度を下げてメモリ・帯域・演算費用を抑える。一方、平均2bitの一部方式ではPPLがFP16比55%以上悪化する。

- **2025-09 · [Efficient Pre-Training of LLMs via Topology-Aware Communication Alignment on More Than 9600 GPUs](2025-2509.15940-efficient-pre-training-of-llms-via-topology-aware-communication-alignmen.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  一般的なクラスタスケジューラが空きGPUを近い位置に詰めても、実際に頻繁に通信するDP/PPグループが別のスイッチ配下に分散すれば帯域競合と通信待ちが発生する。トレース駆動シミュレーションでは比較方式に対し通信グループの重み付き最大広がりを最大1.67倍改善し、実クラスタでは208 GPUで学習処理量5.7%、9600超GPUで10.6%改善した。

- **2025-06 · [MoE-GPS: Guidlines for Prediction Strategy for Dynamic Expert Duplication in MoE Load Balancing](2025-2506.07366-moe-gps-guidlines-for-prediction-strategy-for-dynamic-expert-duplication.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  MoE-GPSは、複数GPUに専門家を分散配置するMixture-of-Experts（MoE）モデルで、負荷分散のために人気専門家を複製するとき、どの程度細かくルーティング先を予測すべきかを選択する性能分析フレームワークである。MoE-GPSはこの交換条件をGPU計算・通信・予測費用へ分解し、システム全体の遅延が最小になる選択を示す。

- **2025-05 · [Let LRMs Break Free from Overthinking via Self-Braking Tuning](2025-2505.14604-let-lrms-break-free-from-overthinking-via-self-braking-tuning.md)**  
  実装：[✓](https://github.com/ZJU-REAL/Self-Braking-Tuning) ・ リポジトリ内被引用：3  
  従来の出力トークン予算や推論時の外部停止判定では、問題の難しさと必要な推論深度を一律に扱ったり、追加の判定機構が必要になったりする。

- **2025-03 · [Performance Aware LLM Load Balancer for Mixed Workloads](2025-e32383a452cd-performance-aware-llm-load-balancer-for-mixed-workloads.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  本研究の対象は、同じ大規模言語モデルを複数のGPUインスタンスで提供するとき、各要求をどのインスタンスへ送るかという負荷分散である。1インスタンス内のバッチ形成を改善する研究と異なり、要求がいったん不適切なインスタンスへ送られると、その内部のスケジューラだけでは混在負荷による干渉を解消しにくい。

- **2025-03 · [Key, Value, Compress: A Systematic Exploration of KV Cache Compression Techniques](2025-2503.11816-key-value-compress-a-systematic-exploration-of-kv-cache-compression-tech.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  長文脈の大規模言語モデルで問題になるキー・バリュー（KV）キャッシュの容量を減らす方式を、どの軸の冗長性を削るかという視点で整理する。したがって表4の2.87倍と1.86倍を並べて前者が後者より優れた方式と結論付けることはできない。

- **2025-02 · [BumbleBee: Secure Two-party Inference Framework for Large Transformers](2025-93b16acfd7b9-bumblebee-secure-two-party-inference-framework-for-large-transformers.md)**  
  実装：[✓](https://github.com/AntCPLab/OpenBumbleBee) ・ リポジトリ内被引用：3  
  入力とモデル重みをそれぞれ秘匿したままBERT、GPT-2、LLaMA-7B、ViTを実行し、従来方式に比べて実測の転送量と実行時間を改善する。

- **2024-12 · [WebLLM: A High-Performance In-Browser LLM Inference Engine](2024-2412.15803-webllm-a-high-performance-in-browser-llm-inference-engine.md)**  
  実装：[✓](https://github.com/mlc-ai/web-llm) ・ リポジトリ内被引用：3  
  新しい注意機構や学習アルゴリズムではなく、ブラウザで効率的な言語モデル実行を成立させるシステム統合が主要な貢献である。ブラウザ版はネイティブ版より遅いが、復号処理率の約71.2～79.6%を保持した。

- **2025-09 · [SINQ: Sinkhorn-Normalized Quantization for Calibration-Free Low-Precision LLM Weights](2025-2509.22944-sinq-sinkhorn-normalized-quantization-for-calibration-free-low-precision.md)**  
  実装：[✓](https://github.com/huawei-csl/SINQ) ・ リポジトリ内被引用：2  
  通常の4ビットあるいは3ビット重み量子化では、同じ量子化群に非常に大きな重みが混ざると、その外れ値に合わせて量子化刻みを広げる必要がある。これを「モデル全体が3.5倍高速になった」と解釈してはいけない。

- **2025-08 · [READER: Retrieval-Assisted Drafter for Efficient LLM Inference](2025-2508.09072-reader-retrieval-assisted-drafter-for-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  READERは、LLMの逐次トークン生成を高速化する投機的復号（投機的復号）のドラフト木へ、モデルが予測した候補と、過去のテキストや外部データから検索した候補を混ぜる方式である。

- **2025-05 · [Radio: Rate–Distortion Optimization for Large Language Model Compression](2025-2505.03031-radio-rate-distortion-optimization-for-large-language-model-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  RadioはLLM重みの事後量子化を、平均ビット数の制約下で元モデルとの出力歪みを最小化するレート・歪み最適化として定式化する。

- **2025-05 · [Cross-Attention Speculative Decoding](2025-2505.24544-cross-attention-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Beagle（Budget EAGLE）は、投機的復号の小型下書きモデルに単層のcross-注意機構 Transformerを採用し、EAGLE-v2のようなself-注意機構型下書きに近い速度を、単純な構造と少ないメモリで得る方式である。

- **2025-04 · [Hawkeye: Model Collaboration for Efficient Reasoning](2025-2504.00424-hawkeye-model-collaboration-for-efficient-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Hawkeyeは、推論用の大規模言語モデルが長い思考連鎖（Chain-of-Thought; CoT）を出力し続けることによる生成遅延と課金額を削減する研究である。重要なのは、二段階のモデル連携を推論時だけでなく事後学習の報酬設計にも組み込んでいることである。

- **2025-04 · [Activated LoRA: Fine-tuned LLMs for Intrinsics](2025-2504.12397-activated-lora-fine-tuned-llms-for-intrinsics.md)**  
  実装：[✓](https://github.com/tdoublep/vllm/tree/alora) ・ リポジトリ内被引用：2  
  しかし複数のLoRAを一つの長い会話やエージェント処理で切り替える場合、過去の文脈の鍵・値（Key-Value; KV）キャッシュは、アダプタが異なれば一般に同じにならない。vLLMを改造した7モデルの評価器呼び出し実験では、長い接頭辞に対して評価器単体の最大35倍高速化を報告する。

- **2025-03 · [RSQ: Learning from Important Tokens Leads to Better Quantized LLMs](2025-2503.01820-rsq-learning-from-important-tokens-leads-to-better-quantized-llms.md)**  
  実装：[✓](https://github.com/ylsung/rsq) ・ リポジトリ内被引用：2  
  GPTQなどの事後量子化（Post-学習 量子化; PTQ）は、元の重みを低ビットへ丸めるとき、少数の校正データで量子化前後の層出力を比較して誤差を補償する。2bit条件ではQuaRotの平均35.3%に対しRSQは40.6%となる。

- **2025-02 · [SPECTRE: An FFT-Based Efficient Drop-In Replacement to Self-Attention for Long Contexts](2025-2502.18394-spectre-an-fft-based-efficient-drop-in-replacement-to-self-attention-for.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  SPECTREは、系列長$n$に対して二乗で増える通常の自己注意（Self-注意機構）を、実数高速フーリエ変換（Real Fast Fourier Transform、RFFT）、内容適応の周波数ゲート、逆変換の組合せで置き換える方式である。

- **2025-02 · [Exploiting Sparsity for Long Context Inference: Million Token Contexts on Commodity GPUs](2025-2502.06766-exploiting-sparsity-for-long-context-inference-million-token-contexts-on.md)**  
  実装：[✓](https://github.com/ryansynk/topk-decoding) ・ リポジトリ内被引用：2  
  長文脈の推論では、モデル重みだけでなく過去のkey/valueを保持するKVキャッシュがGPUメモリを圧迫する。すべてのKVをCPUへオフロードしても、生成トークンごとに全量をGPUへ戻せばPCIe転送がボトルネックになる。特に重要なのは、100万トークン文脈のプリフィルを16GB級GPUだけで実行した研究ではないという点である。

- **2025-02 · [ETS: Efficient Tree Search for Inference-Time Scaling](2025-2502.13575-ets-efficient-tree-search-for-inference-time-scaling.md)**  
  実装：[✓](https://github.com/SqueezeAILab/ETS) ・ リポジトリ内被引用：2  
  ETS（Efficient Tree Search）は、LLMの推論時演算量拡大（inference-time scaling）で用いる木探索の費用を、単なるモデル呼出回数ではなく分岐間の鍵・値キャッシュ（KV キャッシュ）共有量に基づいて最適化する方式である。

- **2024-11 · [kNN Attention Demystified: A Theoretical Exploration for Scalable Transformers](2024-2411.04013-knn-attention-demystified-a-theoretical-exploration-for-scalable-transfo.md)**  
  実装：[✓](https://github.com/sansui-123/knn_attention) ・ リポジトリ内被引用：2  
  近傍探索によって各クエリに重要そうなk個のキーだけを選ぶ方式は経験的に用いられてきたが、何をどの精度で近似できるか、逆伝播で同様の効率化が可能かは自明ではない。

- **2025-10 · [Untangling Component Imbalance in Hybrid Linear Attention Conversion Methods](2025-2510.05901-untangling-component-imbalance-in-hybrid-linear-attention-conversion-met.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  事前学習済みTransformerの通常のsoftmax注意を線形注意（LA）へ置き換えれば、過去のキーと値を全トークン分保持せず、一定サイズの再帰状態へ集約できる。しかし注意機構を変更しただけでは元モデルの精度が下がるため、注意転写と追加微調整を行う。

- **2025-10 · [Scaling Laws Meet Model Architecture: Toward Inference-Efficient LLMs](2025-2510.18245-scaling-laws-meet-model-architecture-toward-inference-efficient-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデルの設計では、パラメータ数と学習トークン数を指定して学習損失を下げる方法が重視されてきた。

- **2025-10 · [Key and Value Weights Are Probably All You Need: On the Necessity of the Query, Key, Value weight Triplet in Self-Attention Transformers](2025-2510.23912-key-and-value-weights-are-probably-all-you-need-on-the-necessity-of-the-.md)**  
  実装：[✓](https://github.com/MarkoKarbevski/Wqkv_necessity) ・ リポジトリ内被引用：1  
  各射影が表現力に独立して必要なのかは、モデルのパラメータ数・学習時の最適化・推論時のメモリ使用量を考えるうえで重要である。理論の出発点は、注意機構が元の入力Xを直接見るのではなく、XWQ、XWK、XWVという射影後の値に依存する点である。これは非埋込パラメータ約8.3%削減であり、総モデルパラメータが25%減るわけではない。

- **2025-10 · [AsyncSpade: Efficient Test-Time Scaling with Asynchronous Sparse Decoding](2025-2510.07486-asyncspade-efficient-test-time-scaling-with-asynchronous-sparse-decoding.md)**  
  実装：[✓](https://github.com/UNITES-Lab/AsyncSpade) ・ リポジトリ内被引用：1  
  疎注意で参照トークン数を減らしても、現在のクエリを計算してから参照ページを選ぶ方式では、選別処理が注意計算の直前に直列化される。長文推論の性能を比較する際には、生成品質を維持したまま演算量を減らせるかと、実際のトークン生成遅延が短くなるかを分けて見る必要がある。

- **2025-10 · [ARMOR: High-Performance Semi-Structured Pruning via Adaptive Matrix Factorization](2025-2510.05528-armor-high-performance-semi-structured-pruning-via-adaptive-matrix-facto.md)**  
  実装：[✓](https://github.com/LawrenceRLiu/ARMOR) ・ リポジトリ内被引用：1  
  一方、どの4要素からも2要素を消すという硬い制約は、同じ50%剪定率の非構造化剪定よりも言語モデルの品質を大きく悪化させやすい。ARMORは、この損失をマスク選択だけで解決するのではなく、疎行列の前後へ小さい学習可能な線形変換を配置して重み表現を変える方式である。

- **2025-10 · [Activation Quantization of Vision Encoders Needs Prefixing Registers](2025-2510.04547-activation-quantization-of-vision-encoders-needs-prefixing-registers.md)**  
  実装：[✓](https://github.com/spbob0418/RegCache) ・ リポジトリ内被引用：1  
  しかし、CLIPやSigLIPなどの視覚Transformerでは、一部トークンの活性値が他より極端に大きくなり、活性値の量子化範囲を押し広げて精度を損なう。

- **2025-09 · [SpikingBrain: Spiking Brain-inspired Large Models](2025-2509.05276-spikingbrain-spiking-brain-inspired-large-models.md)**  
  実装：[✓](https://github.com/BICLab/SpikingBrain-7B) ・ リポジトリ内被引用：1  
  SpikingBrainは、標準Transformerの長文脈計算・KVキャッシュ負荷と、非NVIDIA GPUでの大規模学習の難しさを同時に扱う研究である。成果は一つの高速注意機構カーネルにとどまらない。

- **2025-09 · [PipelineRL: Faster On-policy Reinforcement Learning for Long Sequence Generation](2025-2509.19128-pipelinerl-faster-on-policy-reinforcement-learning-for-long-sequence-gen.md)**  
  実装：[✓](https://github.com/ServiceNow/pipelinerl) ・ リポジトリ内被引用：1  
  PipelineRLは、大規模言語モデルの長文推論を強化学習で訓練するときに、系列生成器と訓練器の並行実行および生成途中の重み更新（in-flight 重み update）を組み合わせるシステムである。

- **2025-09 · [LUQ: Layerwise Ultra-Low Bit Quantization for Multimodal Large Language Models](2025-2509.23729-luq-layerwise-ultra-low-bit-quantization-for-multimodal-large-language-m.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LUQ（Layerwise Ultra-Low Bit Quantization）は、視覚言語モデル（VLM/MLLM）の各Transformer層が低ビット量子化に耐える度合いは一様でないことに着目し、層の出力活性entropyが低い順に1bit系量子化へ切り替える方式である。

- **2025-09 · [HERO: Rethinking Visual Token Early Dropping in High-Resolution Large Vision-Language Models](2025-2509.13067-hero-rethinking-visual-token-early-dropping-in-high-resolution-large-vis.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  HEROは、高解像度画像を複数の局所タイルと全体サムネイルへ分割して処理するVision-Language モデル（VLM）向けに、LLMへ渡す前の視覚トークンを選別する追加学習不要の圧縮手法である。

- **2025-08 · [P/D-Device: Disaggregated Large Language Model between Cloud and Devices](2025-2508.09035-p-d-device-disaggregated-large-language-model-between-cloud-and-devices.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  クラウドのLLMサービングではプリフィルとデコードを別のインスタンスへ配置するP/D分離が普及している。著者のAscend NPUクラウド・Kirin SoC端末による4k～32k入力の実験では、端末が自分のプリフィルを完了するまでの平均時間が端末単独より60%短くなり、利用者にはそれより早いクラウドの第1トークン到着時点で応答を表示できる。

- **2025-08 · [DualSparse-MoE: Coordinating Tensor/Neuron-Level Sparsity with Expert Partition and Reconstruction](2025-2508.18376-dualsparse-moe-coordinating-tensor-neuron-level-sparsity-with-expert-par.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  DualSparse-MoEはこの二種類の疎性を同時に使い、重要なニューロンの計算を残しながら、影響の小さいトークン・専門家演算を省くシステムである。原著のSGLang/H20評価では、約25%のMoE演算省略に対しMixtral・OLMoE・DeepSeekの平均精度低下は0.08〜0.28ポイントにとどまる。

- **2025-08 · [DTRNet: Dynamic Token Routing Network to Reduce Quadratic Costs in Transformers](2025-2509.00925-dtrnet-dynamic-token-routing-network-to-reduce-quadratic-costs-in-transf.md)**  
  実装：[✓](https://github.com/Aman26Sharma/DTRNet) ・ リポジトリ内被引用：1  
  各層で学習済みルーティングがトークンごとにfull 注意機構経路と軽量な自己投影経路を選ぶ。FineWeb-Eduで事前学習した360Mモデルでは、DTRNet-BiLayerがdense SmolLM比FLOPs 0.84倍で平均ゼロショット精度44.36%、denseの44.23%とほぼ同等だった。

- **2025-08 · [Attention Debiasing for Token Pruning in Vision–Language Models](2025-2508.17807-attention-debiasing-for-token-pruning-in-vision-language-models.md)**  
  実装：[✓](https://github.com/intcomp/attention-bias) ・ リポジトリ内被引用：1  
  多くの視覚トークンが冗長なので、言語モデルの初期層で重要度の低いトークンを捨てれば、以後の注意機構やKV保持の負荷を下げられる。

- **2025-07 · [Squeeze10-LLM: Squeezing LLMs’ Weights by 10 Times via a Staged Mixed-Precision Quantization Method](2025-2507.18073-squeeze10-llm-squeezing-llms-weights-by-10-times-via-a-staged-mixed-prec.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  しかし均一に1～2bitへ量子化すると、外れ値や重要なチャネルの情報が失われ、出力活性が層を通るたびにずれていく。Squeeze10-LLMは、すべての重みをいきなり1bitにせず、まず4bitへ変換してから重要度を測定し、80%を1bit、残り20%を4bitで保存する段階的な重み専用post-学習 量子化（PTQ）を提案する。

- **2025-07 · [RAT: Bridging RNN Efficiency and Attention Accuracy via Chunk-based Sequence Modeling](2025-2507.04416-rat-bridging-rnn-efficiency-and-attention-accuracy-via-chunk-based-seque.md)**  
  実装：[✓](https://github.com/CLAIRE-Labo/RAT) ・ リポジトリ内被引用：1  
  全トークンに対するソフトマックス注意（softmax 注意機構）は、過去の任意の位置を直接参照できる一方、長文で注意演算量と鍵・値キャッシュ（KV キャッシュ）が増える。また、3072トークンの入力から1024トークンを生成する最大生成処理量では、1.3Bモデルで通常注意3152に対しRAT 31170トークン/秒、約10.2倍である。

- **2025-07 · [CCQ: Convolutional Code for Extreme Low-bit Quantization in LLMs](2025-2507.07145-ccq-convolutional-code-for-extreme-low-bit-quantization-in-llms.md)**  
  実装：[✓](https://github.com/PaddlePaddle/FastDeploy/tree/develop) ・ リポジトリ内被引用：1  
  2bit級の重み量子化では、単純な整数丸めでは表現可能な値が少なすぎて精度が大きく落ちる。原著Table 2ではDeepSeek-V3-0324の8bit版642GBに対し、CCQ 2.06bpw版は184GBで、GSM8K/C-Eval/MMLU平均が90.01から87.76へ低下する。

- **2025-06 · [SparseSSM: Efficient Selective Structured State Space Models Can Be Pruned in One-Shot](2025-2506.09613-sparsessm-efficient-selective-structured-state-space-models-can-be-prune.md)**  
  実装：[✓](https://github.com/CFinTech/SparseSSM) ・ リポジトリ内被引用：1  
  入力依存の離散化係数と、系列の全時刻で使い回す状態遷移パラメータが組み合わさるため、通常の線形層向け剪定手法を状態遷移重みにそのまま適用すると、削除してよい状態を見誤りやすい。正式版の要旨は、SSM重み50%を微調整なしで削除した際の品質低下が「限定的」であると説明する。

- **2025-06 · [Latent Multi-Head Attention for Small Language Models](2025-2506.09342-latent-multi-head-attention-for-small-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本研究は、大規模LLMで利用される多頭潜在注意（Multi-head Latent 注意機構、MLA）の低ランクKV表現が、数千万〜数億パラメータ規模の小型GPTでも有効かを調べる。

- **2025-06 · [BAQ: Efficient Bit Allocation Quantization for Large Language Models](2025-2506.05664-baq-efficient-bit-allocation-quantization-for-large-language-models.md)**  
  実装：[✓](https://github.com/CSU-ModelCompression/BAQ) ・ リポジトリ内被引用：1  
  BAQ（Bit Allocation Quantization）は、大規模言語モデルの事後量子化で各列に同じビット数を割り当てることの非効率を、逆ヘッセ行列に基づく感度係数から計算した列別ビット幅で改善する手法である。

- **2025-05 · [Semantic Caching of Contextual Summaries for Efficient Question-Answering with Language Models](2025-2505.11271-semantic-caching-of-contextual-summaries-for-efficient-question-answerin.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本研究は、文書検索とLLM呼出しを組み合わせる質問応答で、回答そのものでもKVキャッシュでもなく、質問に合わせて生成した中間の文書要約をキャッシュする方法を扱う。文書を検索した後に要約し、その要約と質問を使って回答する複数段階のワークフローでは、同じ文書に対して似た質問が繰り返される。

- **2025-05 · [NeUQI: Near-Optimal Uniform Quantization Parameter Initialization for Low-Bit LLMs](2025-2505.17595-neuqi-near-optimal-uniform-quantization-parameter-initialization-for-low.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  低ビットの言語モデルを作る際、重みを整数格子へ写す一様量子化は既存GPUの整数演算・メモリ削減と相性がよい。

- **2025-05 · [$\mu$-MoE: Test-Time Pruning as Micro-Grained Mixture-of-Experts](2025-2505.18451-mu-moe-test-time-pruning-as-micro-grained-mixture-of-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  μ-MoEは、モデルをあらかじめ一度だけ枝刈りするのではなく、実際に与えられたプロンプトをその場の校正データとして使い、線形層の重みのうち重要なものだけを有効化する方式である。

- **2025-04 · [AccLLM: Accelerating Long-Context LLM Inference Via Algorithm-Hardware Co-Design](2025-2505.03745-accllm-accelerating-long-context-llm-inference-via-algorithm-hardware-co.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデル（LLM）を資源制約の強い端末向けFPGAに載せるため、圧縮アルゴリズムと演算器・データフローを同時に設計する。主要な評価ではLlama-2-7Bを12.1GBのFP16モデルから1.53GBへ縮小し、Xilinx Alveo U280 FPGA上で164 トークン/s、33W、4.96 トークン/Jを報告した。

- **2025-03 · [Union of Experts: Adapting Hierarchical Routing to Equivalently Decomposed Transformer](2025-2503.02495-union-of-experts-adapting-hierarchical-routing-to-equivalently-decompose.md)**  
  実装：[✓](https://github.com/YujiaoYang-work/UoE) ・ リポジトリ内被引用：1  
  本論文は、Mixture-of-Experts（MoE）の疎活性化をMLPブロックだけに限定せず、注意ブロックとMLPブロックをともに、機能的に等価な部分計算から構成される専門家集合へ分解するUnion-of-Experts（UoE）を提案する。

- **2025-03 · [PromptDistill: Query-based Selective Token Retention in Intermediate Layers for Efficient Large Language Model Inference](2025-2503.23274-promptdistill-query-based-selective-token-retention-in-intermediate-laye.md)**  
  実装：[✓](https://github.com/declare-lab/PromptDistill) ・ リポジトリ内被引用：1  
  長文の入力を持つ大規模言語モデルでは、プロンプトの全位置を全Transformer層で処理すると、入力長に伴って注意計算と中間状態の保存量が増える。PromptDistillは、最初の数層だけ全位置を処理した後、入力の最後の位置のqueryと各位置のkeyから選んだ重要位置に計算を集中する。< の本文§2–3とTable 1–5を照合した。

- **2025-03 · [Multi-Cue Adaptive Visual Token Pruning for Large Vision-Language Models](2025-2503.08019-multi-cue-adaptive-visual-token-pruning-for-large-vision-language-models.md)**  
  実装：[✓](https://github.com/bzluan/AdaptPrune) ・ リポジトリ内被引用：1  
  画像を扱う大規模視覚言語モデル（LVLM）では、視覚エンコーダが作る数百から数千の画像パッチ表現が言語モデルへトークンとして挿入される。画像が高解像度になると、視覚トークンは言語側の自己注意やFFNにも流れ、プリフィル計算量、後続のKVキャッシュ容量、生成時の注意計算に影響する。画像トークンの一部を早い層で取り除けば、後続層の計算と記憶を減らせる。

- **2025-02 · [M2R2: Mixture of Multi-Rate Residuals for Efficient Transformer Inference](2025-2502.02040-m2r2-mixture-of-multi-rate-residuals-for-efficient-transformer-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  M2R2は、言語モデルの中間残差表現が最終層の残差表現へどれだけ早く近づくかを、追加の軽量な計算経路で制御する方式である。

- **2025-02 · [GATEKEEPER: Improving Model Cascades Through Confidence Tuning](2025-2502.19335-gatekeeper-improving-model-cascades-through-confidence-tuning.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GATEKEEPERは、軽量な小型モデルと高精度だが高価な大型モデルを組み合わせる二段推論カスケードに対して、小型モデルの確信度そのものを委譲判断に適した形へ学習し直す方式である。評価は正答率と委譲率の曲線を主軸としており、実サービング基盤におけるGPU処理量や末尾遅延の改善を直接測ったものではない。

- **2025-01 · [TreeKV: Smooth Key-Value Cache Compression with Tree Structures](2025-2501.04987-treekv-smooth-key-value-cache-compression-with-tree-structures.md)**  
  実装：[✓](https://github.com/ZiweiHe/TreeKV) ・ リポジトリ内被引用：1  
  過去KVの一部だけを残す方法は以前からあるが、単純な「先頭と末尾の固定窓」は中間の重要情報を落とし、注意重みが大きいものを全履歴から貪欲に選ぶ方式は特定領域へ保持位置が偏りやすい。

- **2025-01 · [RedundancyLens: Revealing and Exploiting Visual Token Processing Redundancy for Efficient Decoder-Only MLLMs](2025-2501.19036-redundancylens-revealing-and-exploiting-visual-token-processing-redundan.md)**  
  実装：[✓](https://github.com/L-Hugh/RedundancyLens) ・ リポジトリ内被引用：1  
  この構成は実装が単純で精度も高い一方、画像由来のトークン数が増えると、LLMのself-注意機構とFFNの両方で大量の演算が発生する。約半数の層へ演算削減を適用すると、FLOPs比が約71〜72%に下がり、元モデルに近い品質を維持する。

- **2025-01 · [DiscQuant: A Quantization Method for Neural Networks Inspired by Discrepancy Theory](2025-2501.06417-discquant-a-quantization-method-for-neural-networks-inspired-by-discrepa.md)**  
  実装：[✓](https://github.com/jerry-chee/DiscQuant) ・ リポジトリ内被引用：1  
  DiscQuantは、事前学習済みLLMの重みを低ビット化する際、量子化格子を設計した後の「各重みを上側と下側のどちらへ丸めるか」という問題を解く。原著の代表例では、Phi-3-mini-4k-instructを平均3.25ビットで量子化したGSM8kの正答率が、DiscQuant64%、GPTQ54%、RTN31%、無量子化84%である。

- **2024-11 · [CLOVER: Cross-Layer Orthogonal Vectors Pruning and Fine-Tuning](2024-2411.17426-clover-cross-layer-orthogonal-vectors-pruning-and-fine-tuning.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  重要度の小さい方向を剪定したり、特異値を学習対象にしたりすることで、既存モデルの構造を利用した圧縮と効率的な微調整を行う。

- **2024-11 · [AdaCM^2: On Understanding Extremely Long-Term Video with Adaptive Cross-Modality Memory Reduction](2024-2411.12593-adacm-2-on-understanding-extremely-long-term-video-with-adaptive-cross-m.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  AdaCM²は、長時間動画を言語モデルへ渡す際、すべてのフレームの視覚特徴を保存し続ける代わりに、テキスト質問と強く関連する視覚トークンだけを古いキャッシュから残す方式である。

- **2025-10 · [video-SALMONN S: Memory-Enhanced Streaming Audio-Visual LLM](2025-2510.11129-video-salmonn-s-memory-enhanced-streaming-audio-visual-llm.md)**  
  実装：[✓](https://github.com/bytedance/SALMONN/tree/video-salmonn-S) ・ リポジトリ内被引用：0  
  後者では将来の質問も動画長も未知であり、長時間の履歴を固定のGPUメモリ予算へ保持しなければならない。類似トークンをまとめるだけの方式は新しいフレームが来るたび古い細部を失い、数十分前に見た手順を問われる課題では精度が下がり得る。

- **2025-10 · [To Compress or Not? Pushing the Frontier of Lossless GenAI Model Weights Compression with Exponent Concentration](2025-2510.02676-to-compress-or-not-pushing-the-frontier-of-lossless-genai-model-weights-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FP8形式は、行列積を低精度で直接計算できるため、LLM推論時の重みメモリと演算費用を抑えられる。ECF8（Exponent-Concentrated FP8）は、この偏りを利用してFP8重みの値そのものは一切変えずに、保存時のビット数を減らす方式である。報告されたメモリ削減率は9.8〜26.9%、固定メモリ予算での処理率改善は11.3〜177.1%である。

- **2025-10 · [STaMP: Sequence Transformation and Mixed Precision for Low-Precision Activation Quantization](2025-2510.26771-stamp-sequence-transformation-and-mixed-precision-for-low-precision-acti.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  STaMP（Sequence Transformation and Mixed Precision）は、低ビット量子化の前に活性行列を系列方向へ直交変換し、情報が集中した少数の変換後トークンだけを8ビット、残りを4ビットで表現する方式である。

- **2025-10 · [Reasoning in the Dark: Interleaved Vision-Text Reasoning in Latent Space](2025-2510.12603-reasoning-in-the-dark-interleaved-vision-text-reasoning-in-latent-space.md)**  
  実装：[✓](https://github.com/ModalityDance/IVT-LR) ・ リポジトリ内被引用：0  
  視覚言語モデル（vision-language モデル; VLM）が図表や画像に基づいて多段階の推論をするとき、従来の思考の連鎖（chain of thought; CoT）方式は中間推論を自然言語トークンとして逐次生成する。

- **2025-10 · [PatternKV: Flattening KV Representation Expands Quantization Headroom](2025-2510.05176-patternkv-flattening-kv-representation-expands-quantization-headroom.md)**  
  実装：[✓](https://github.com/HCOOOH/PatternKV) ・ リポジトリ内被引用：0  
  KVキャッシュを保持することで過去トークンの注意計算を省ける一方、文脈長、同時リクエスト数、複数回答を生成する推論時スケーリングに比例してキャッシュが膨らむ。著者は複数モデル平均でFP16との差が0.08%と要約するが、これは個別モデルの全タスクで差がゼロという意味ではない。

- **2025-10 · [MossNet: Mixture of State-Space Experts is a Multi-Head Attention](2025-2510.26182-mossnet-mixture-of-state-space-experts-is-a-multi-head-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数の状態空間専門家の混合が線形化したmulti-head 注意機構の形に展開できることを示し、従来の単一状態のSSMより表現力を高める。8x200M+モデルは2.8兆トークン学習後、top-2（活性477M）で7課題平均53.5%、Qwen2.5-0.5Bの47.7%を上回るが、学習トークン数・モデル構造が異なる。

- **2025-10 · [MixReasoning: Switching Modes to Think](2025-2510.06052-mixreasoning-switching-modes-to-think.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MixReasoningは、問題全体を「考える／考えない」に二分するのではなく、一つの長い推論軌跡の中で難しい部分だけ詳細思考を行う方式である。Qwen3-8Bの4課題平均では、元モデルのpass@1 77.44、平均生成7027トークンに対し、MixReasoningはpass@1 78.29、5120トークン（約28%減）となる。

- **2025-10 · [HA-RAG: Hotness-Aware RAG Acceleration via Mixed Precision and Data Placement](2025-2510.20878-ha-rag-hotness-aware-rag-acceleration-via-mixed-precision-and-data-place.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HA-RAGは、検索拡張生成（RAG）で繰り返し参照される外部文書のKVキャッシュを、検索頻度に応じた数値形式とメモリ階層の組合せで管理する推論システムである。

- **2025-10 · [Exemplar-Derived Soft Prompts for Efficient and Effective Domain Adaptation](2025-2510.05363-exemplar-derived-soft-prompts-for-efficient-and-effective-domain-adaptat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案法MHA-ESPは、質問に関連する例示を検索し、質問と例示の埋め込みを多頭注意で集約して、基盤モデルの埋め込み次元に揃えた少数の仮想トークンを作る。原著がいう最大約10倍の計算量削減は入力例示のトークン処理に関する演算量比較であり、実際の生成速度が常に10倍になるという意味ではない。

- **2025-10 · [ELUTQ: Optimizing Quantization Accuracy under LUT-Based Computation for Edge LLMs](2025-2510.19482-elutq-optimizing-quantization-accuracy-under-lut-based-computation-for-e.md)**  
  実装：[✓](https://github.com/Nkniexin/ELUTQ) ・ リポジトリ内被引用：0  
  ELUTQは、LLMの重みを2〜3bitへ圧縮するときの量子化誤差と、量子化後の重みをCPU/GPUで実行するときの復号・乗算費用を一緒に扱うシステムである。

- **2025-10 · [Don't Run with Scissors: Pruning Breaks VLA Models but They Can Be Recovered](2025-2510.08464-don-t-run-with-scissors-pruning-breaks-vla-models-but-they-can-be-recove.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、2:4構造化剪定をVLAへ適用すると、一般的な言語モデルよりはるかに深刻な性能崩壊が起こることを示し、剪定で失われた重み成分を低ランク補正で部分的に復元するGLUESTICKを提案する。

- **2025-10 · [Direct Multi-Token Decoding](2025-2510.11958-direct-multi-token-decoding.md)**  
  実装：[✓](https://github.com/luoxuan-cs/Direct-Multitoken-Decoding) ・ リポジトリ内被引用：0  
  低バッチでは重みをGPUメモリから読み出す時間が支配的になりやすく、各層を毎トークン通ることが遅延の主要因になる。以下の数値はすべて原著の表を照合したものであり、未測定の大規模サービング性能や他の投機復号方式との優劣は主張しない。

- **2025-10 · [AttnCache: Accelerating Self-Attention Inference for LLM Prefill via Attention Cache](2025-2510.25979-attncache-accelerating-self-attention-inference-for-llm-prefill-via-atte.md)**  
  実装：[✓](https://github.com/PASAUCMerced/AttnCache) ・ リポジトリ内被引用：0  
  従って「注意計算全体をゼロにする」方式ではない。著者の実測はCPUで平均1.2倍のエンドツーエンド（E2E）高速化、自己注意部分で平均2倍、GPUでE2E平均1.6倍、注意部分で平均3倍を報告する。

- **2025-10 · [ARA: Adaptive Rank Allocation for Efficient Large Language Model SVD Compression](2025-2510.19389-ara-adaptive-rank-allocation-for-efficient-large-language-model-svd-comp.md)**  
  実装：[✓](https://github.com/compressionOrg/ARA) ・ リポジトリ内被引用：0  
  ARA（適応的 Rank Allocation）は、圧縮予算を複数の線形モジュールに配る学習可能なランク選択器である。特に「80% 残存比率」はパラメータの80%を残すという意味で、80%を削る意味ではない。

- **2025-10 · [APCE: Adaptive Progressive Context Expansion for Long Context Processing](2025-2510.12051-apce-adaptive-progressive-context-expansion-for-long-context-processing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  適応的 Progressive Context Expansion（APCE）は、長い入力を最初から全てTransformerへ通す代わりに、質問と意味的に近いchunkだけを選んでプリフィルし、生成が進むにつれて参照chunkを入れ替える方式である。

- **2025-10 · [Adaptive Dual Reasoner: Large Reasoning Models Can Think Efficiently by Hybrid Reasoning](2025-2510.10207-adaptive-dual-reasoner-large-reasoning-models-can-think-efficiently-by-h.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  適応的 Dual Reasoner（ADR）は、大規模推論モデルが簡単な計算でも長いChain-of-Thoughtを出力する「過剰思考」を抑えるため、推論途中の難しさに応じてeasy（簡潔な思考）とhard（深い思考）を切り替える方式である。

- **2025-09 · [Thinking-Free Policy Initialization Makes Distilled Reasoning Models More Effective and Efficient Reasoners](2025-2509.26226-thinking-free-policy-initialization-makes-distilled-reasoning-models-mor.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論モデルを検証可能報酬で強化学習するRLVR（Reinforcement Learning with Verifiable Rewards）では、正解が自動判定できる数学・コード課題を多数解かせ、rolloutごとの成否からpolicyを更新する。最大応答長を短く制限すれば安くなるが、途中の検証・再考を切り捨てることで、学習後の正答率が戻らない場合がある。

- **2025-09 · [TASP: Topology-aware Sequence Parallelism](2025-2509.26541-tasp-topology-aware-sequence-parallelism.md)**  
  実装：[✓](https://github.com/infinigence/HamiltonAttention) ・ リポジトリ内被引用：0  
  Ring 注意機構は、長いQ/K/V列を複数GPUへ分け、各GPUがローカルQを保持したままKVブロックをリングで順送りする。しかし8 GPUの全結合トポロジーで単一リングだけを使うと、各反復で利用できる方向付き通信リンクは全体の約1/7、すなわち14.3%にとどまる。

- **2025-09 · [Self-Aligned Reward: Towards Effective and Efficient Reasoners](2025-2509.05489-self-aligned-reward-towards-effective-and-efficient-reasoners.md)**  
  実装：[✓](https://github.com/amazon-science/Self-Aligned-Reward-Towards_Effective_and_Efficient_Reasoners) ・ リポジトリ内被引用：0  
  提案する自己整合報酬（Self-Aligned Reward; SAR）は、同じ回答 $a$ の困惑度を、質問 $q$ を与えた場合と与えない場合で計算する。例えばQwen3-1.7Bでは、GRPOの平均正答率53.37%、回答長762.8トークンに対して、SAR付きGRPOは54.13%、602.0トークンだった。

- **2025-09 · [SBVR: Summation of BitVector Representation for Efficient LLM Quantization](2025-2509.18172-sbvr-summation-of-bitvector-representation-for-efficient-llm-quantizatio.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの重みを4ビット程度へ圧縮する事後量子化では、表現可能な値を減らすことで重みの転送量を節約できる。ただしRTX 3090・バッチ1のTPOTはSBVR 10.24msに対しAWQ 8.61msで、速度の絶対首位ではない。

- **2025-09 · [Pyramid Token Pruning for High-Resolution Large Vision-Language Models via Region, Token, and Instruction-Guided Importance](2025-2509.15704-pyramid-token-pruning-for-high-resolution-large-vision-language-models-v.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Pyramid Token Pruning（PTP）は、追加学習なしで、画像全体に対するタイルの重要度、タイル内部のパッチ重要度、ユーザーの指示文に対するパッチ関連度を三段階で組み合わせる方式である。

- **2025-09 · [HiPO: Hybrid Policy Optimization for Dynamic Reasoning in LLMs](2025-2509.23967-hipo-hybrid-policy-optimization-for-dynamic-reasoning-in-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HiPO（Hybrid Policy Optimization）は、各入力に対して詳細推論を行うThink-onと直接回答するThink-offを選ぶ能力をモデル自体に学習させる方式である。

- **2025-09 · [Frame-Stacked Local Transformers For Efficient Multi-Codebook Speech Generation](2025-2509.19592-frame-stacked-local-transformers-for-efficient-multi-codebook-speech-gen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Koel-TTSとNanoCodecを使ったLibriTTS評価では、積層係数2で自己回帰型が従来の非積層・全コード並列方式の2.1倍、MaskGIT型が3.1倍の推論処理量を示した。

- **2025-09 · [Enhancing Linear Attention with Residual Learning](2025-2509.25223-enhancing-linear-attention-with-residual-learning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  線形注意機構は、履歴のkey/valueを固定サイズの状態行列に集約し、系列長に対して線形時間・一定の再帰状態メモリで生成できる。約1.5Bパラメータを100B トークンで学習した比較で、RDNはGated DeltaNet（GDN）のWikiText PPL 17.27から16.57へ、8課題平均正解率46.03%から47.20%へ改善した。

- **2025-09 · [Efficient Large Language Models with Zero-Shot Adjustable Acceleration](2025-2509.01190-efficient-large-language-models-with-zero-shot-adjustable-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究の狙いは、推論時にTransformerの層間を通過する隠れ活性の数を削減しながら、どの程度の削減を行うかを微調整後に変更できるようにすることである。GPT-2のIMDB分類では最大11倍の加速設定で正解率が92.40%から86.48%へ低下する。

- **2025-09 · [Effective Model Pruning: Measuring the Redundancy of Model Components](2025-2509.25606-effective-model-pruning-measuring-the-redundancy-of-model-components.md)**  
  実装：[✓](https://github.com/noMushroomw/Effective-model-pruning) ・ リポジトリ内被引用：0  
  ニューラルネットワークの枝刈りでは、重要度の低い重みや注意ヘッドを削除するためにMagnitude、Wanda、勾配感度などのスコアを用いる。例えばLLMで全層一律50%の非構造化枝刈りを指定すると、スコアの分布が集中している層と均一な層へ同じ予算を押し付ける。

- **2025-09 · [CompLLM: Compression for Long Context Q&A](2025-2509.19228-compllm-compression-for-long-context-q-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CompLLMは、LLMへ入力する長い文書を、短いセグメントごとに独立して連続ベクトルへ圧縮する方式である。標準設定は最大20入力トークンを10個のCEへ変換する2倍圧縮である。

- **2025-09 · [COMPACT: Common-token Optimized Model Pruning Across Channels and Tokens](2025-2509.06836-compact-common-token-optimized-model-pruning-across-channels-and-tokens.md)**  
  実装：[✓](https://github.com/ekwek1/COMPACT) ・ リポジトリ内被引用：0  
  COMPACTは、推論用の大規模言語モデルを圧縮するとき、Transformerの層数や隠れ次元を一律に削るのでなく、語彙表に結び付くパラメータとフィードフォワード網（FFN）の中間チャネルを別々に制御する手法である。

- **2025-09 · [ChunkLLM: A Lightweight Pluggable Framework for Accelerating LLMs Inference](2025-2510.02361-chunkllm-a-lightweight-pluggable-framework-for-accelerating-llms-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ChunkLLMは、既存Transformerのbackboneを固定したまま軽量なadapterを付加し、長文のどのchunkのKVを保持するかを学習する方式である。Qwen2.5-7BのLongBenchでは、通常モデルの平均44.13に対してChunkLLMは43.53、KV保持率は48.58%である。

- **2025-09 · [Amdahl's Law for LLMs: A Throughput-Centric Analysis of Extreme LLM Quantization](2025-d58c83365862-amdahl-s-law-for-llms-a-throughput-centric-analysis-of-extreme-llm-quant.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者はTransformerの演算を、極端な量子化で行列乗算を置換できる射影部分と、置換しにくい注意ヘッド内部に分ける。さらにAmdahl則で「改善できる部分が元の実行時間の何割か」を明示し、13種類のGPT・OPT・LLaMA構成を、クラウド向け256×256およびエッジ向け32×32のシストリック配列でサイクル精度解析した。

- **2025-08 · [SEPTQ: A Simple and Effective Post-Training Quantization Paradigm for Large Language Models](2025-2604.10091-septq-a-simple-and-effective-post-training-quantization-paradigm-for-lar.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SEPTQは、LLMの重み-only事後量子化（Post-学習 量子化; PTQ）を、(1) 重要重みの保存位置を静的・行列globalに決める、(2) 残りの重みを列ごとに量子化してHessian情報で誤差補償する、という2段階に整理した方式である。

- **2025-08 · [Rethinking 1-bit Optimization Leveraging Pre-trained Large Language Models](2025-2508.06974-rethinking-1-bit-optimization-leveraging-pre-trained-large-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、事前学習済みの言語モデルをそのまま極端な低ビット形式へ変換すると知識が破壊される問題に対し、BinaryLLMという段階的な一ビット化方式を提案する。原著はSmolLM、LLaMA3、LLaMA2などで評価し、三十億パラメータ規模ではゼロショット七課題平均57.0%を得た。

- **2025-08 · [GPT-OSS-20B: A Comprehensive Deployment-Centric Analysis of OpenAI's Open-Weight Mixture of Experts Model](2025-2508.16700-gpt-oss-20b-a-comprehensive-deployment-centric-analysis-of-openai-s-open.md)**  
  実装：[✓](https://github.com/deepdik/GPT-OSS-20B-analysis) ・ リポジトリ内被引用：0  
  MoEは全重みの一部だけを各トークンで活性化するため、演算量はDenseの同規模モデルより小さくなり得る。しかし、未活性のエキスパート重みがメモリから消えるわけではなく、ルーティング、メモリアクセス、KV保持、プリフィルの費用も発生する。GPUのCUDA allocatorピークメモリはそれぞれ43,461MB、63,650MB、66,459MB。

- **2025-08 · [GLASS: Global-Local Aggregation for Inference-time Sparsification of LLMs](2025-2508.14302-glass-global-local-aggregation-for-inference-time-sparsification-of-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  一方、GRIFFINなどの学習不要な方式は、プリフィル中に観測した活性から「生成中に使うニューロン」を決め、その固定マスクをデコードで再利用する。論文v2では、50% FFN疎化の長文生成でGRIFFINよりPPLを最大45.10%、Kullback–Leibler divergence（KLD）を最大25.73%減らした。

- **2025-08 · [AdaptInfer: Adaptive Token Pruning for Vision-Language Model Inference via Dynamical Text Guidance](2025-2508.06084-adaptinfer-adaptive-token-pruning-for-vision-language-model-inference-vi.md)**  
  実装：[✓](https://github.com/weiczh02/AdaptInfer-base) ・ リポジトリ内被引用：0  
  AdaptInferは、質問文のうち画像のどの部分を見るべきかを決める文章トークンが、Transformerの深さに応じて変わることを利用し、各枝刈り層で文章の重要度を再計算して画像トークンを選ぶ方式である。

- **2025-07 · [SpeLLM: Character-Level Multi-Head Decoding](2025-2507.16323-spellm-character-level-multi-head-decoding.md)**  
  実装：[✓](https://github.com/schwartz-lab-NLP/SpeLLM) ・ リポジトリ内被引用：0  
  SpeLLMは入力のBPE語彙を残したまま、出力の予測表現だけを文字単位に分離する。4つの公開モデルを変換した実験では、教師の上位5候補のいずれかと文字列が完全一致する割合が平均91.75%、AutoCorrectありでは94.93%となった。

- **2025-07 · [Smooth Reading: Bridging the Gap of Recurrent LLM to Self-Attention LLM on Long-Context Tasks](2025-2507.19353-smooth-reading-bridging-the-gap-of-recurrent-llm-to-self-attention-llm-o.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかし一度に大量の文書を読み込ませると、必要な情報が後続トークンによって上書き・圧縮され、長文質問応答や要約の精度が下がりやすい。主な評価ではSWA-3B-4k-SRがLongBenchで自己注意のQwen2.5-3Bの平均を3.61ポイント上回る。

- **2025-07 · [MGAA: Multi-Granular Adaptive Allocation fof Low-Rank Compression of LLMs](2025-2507.03294-mgaa-multi-granular-adaptive-allocation-fof-low-rank-compression-of-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MGAA（Multi-Granular 適応的 Allocation）は、LLMの重み行列を低ランク分解するときに、各行列へ同じ削減率を割り当てるのではなく、Transformerサブレイヤ間の重要度と同じサブレイヤ内の各行列が保持する情報量を別々に見積もる手法である。

- **2025-07 · [Investigating Structural Pruning and Recovery Techniques for Compressing Multimodal Large Language Models: An Empirical Study](2025-2507.20749-investigating-structural-pruning-and-recovery-techniques-for-compressing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  言語バックボーンの重みと演算が大きな割合を占めるため、モデルの一部を実際に削除できれば、量子化とは別の経路でメモリ・計算負担を下げられる。15%削減・回復なしのLLaVAでは幅方向の平均指標57.79、層方向46.09であり、元モデル62.28からの低下は幅方向の方が小さい。

- **2025-07 · [High-Layer Attention Pruning with Rescaling](2025-2507.01900-high-layer-attention-pruning-with-rescaling.md)**  
  実装：[✓](https://github.com/SongtaoLiu0823/HARP) ・ リポジトリ内被引用：0  
  下位層と上位層で同じ割合の注意を削ると、表現形成の早い段階にある重要なトークン間依存まで失われ、特に生成・推論課題で品質が大幅に悪化する。HARP（High-層 注意機構 枝刈り with Rescaling）は、高い層ほどトークン表現が類似し、注意によるトークンの識別が弱くなるという仮説を設計の出発点にする。

- **2025-07 · [CoRE: Enhancing Metacognition with Label-free Self-evaluation in LRMs](2025-2507.06087-core-enhancing-metacognition-with-label-free-self-evaluation-in-lrms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い推論を生成する言語モデルは、複雑な数学問題で有用な中間計算を積み重ねる一方、同じ検算や方針の見直しを繰り返し、答えが得られないまま出力を延ばす場合がある。正誤ラベルを集めて判定器を追加学習する方式ではなく、モデルが生成中に持つ隠れ状態を利用する。

- **2025-07 · [Characterizing State Space Model and Hybrid Language Model Performance with Long Context](2025-2507.12442-characterizing-state-space-model-and-hybrid-language-model-performance-w.md)**  
  実装：[✓](https://github.com/sapmitra/ssm-scope) ・ リポジトリ内被引用：0  
  近年はSSMと注意機構を組み合わせたHybridモデルも登場した。本論文は、RTX 4090（24GB）とJetson Orin Nano（8GB共有メモリ）を対象に、Transformer・SSM・Hybridの文脈長による性能逆転、メモリ上限、消費エネルギー、演算子別のボトルネックを計測したシステム特性評価である。

- **2025-07 · [CateKV: On Sequential Consistency for Long-Context LLM Inference Acceleration](2026-2608.30295-catekv-on-sequential-consistency-for-long-context-llm-inference-acceleration.md)**  
  実装：[✓](https://github.com/haoyun-jiang/CateKV) ・ リポジトリ内被引用：0  
  プリフィルからデコードまで注意先が安定するヘッドだけKVを強く削減し、動的ヘッドは大半を保持するハイブリッドKVキャッシュで、精度を保ちながら長文推論のメモリ・デコード・バッチ性能を改善する。

- **2025-07 · [Assigning Distinct Roles to Quantized and Low-Rank Matrices Toward Optimal Weight Decomposition](2025-2506.02077-assigning-distinct-roles-to-quantized-and-low-rank-matrices-toward-optim.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CALDERAなどの方式はWを量子化行列Qと低ランク行列積LRの和、すなわちW ≈ Q + LRで近似し、Qの量子化とLRの更新を交互に行う。一方、同じ条件のARC-Easy正答率は66.35%から65.49%へ下がり、すべての下流タスクを改善するわけではない。

- **2025-07 · [A Comprehensive Evaluation on Quantization Techniques for Large Language Models](2025-2507.17417-a-comprehensive-evaluation-on-quantization-techniques-for-large-language.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの量子化方式は、重み・活性値の精度だけでなく、外れ値をならす前処理、量子化後の誤差補償、対称・非対称、チャネル・グループ粒度、スケールの表現形式などを組み合わせている。さらにRTX 4090のINT4はプリフィルを約2倍高速化するが、バッチ1のデコードはBF16より遅い。

- **2025-06 · [Task-Related Token Compression in Multimodal Large Language Models from an Explainability Perspective](2025-2506.01097-task-related-token-compression-in-multimodal-large-language-models-from-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この研究は、画像や動画を扱うマルチモーダル大規模言語モデル（MLLM）で、ユーザーの指示に関係しない視覚トークンをLLM入力段階で取り除くための方式を提案する。

- **2025-06 · [SPECS: Faster Test-Time Scaling through Speculative Drafts and Dynamic Switching](2025-2506.15733-specs-faster-test-time-scaling-through-speculative-drafts-and-dynamic-sw.md)**  
  実装：[✓](https://github.com/mert-cemri/SPECS) ・ リポジトリ内被引用：0  
  第二に、最初は大型モデルで推論経路を確立し、途中報酬が十分高くなった時点で小型モデルへ切り替えることで、難しい初期推論と比較的容易な続きを分担する。原著v2のQwen2.5モデル対によるMATH500・ビーム幅8の評価では、大型モデルのみのビーム探索が正答率71.3%、平均13.6秒に対し、SPECSは79.5%、11.3秒であった。

- **2025-06 · [S4C: Speculative Sampling with Syntactic and Semantic Coherence for Efficient Inference of Large Language Models](2025-2506.14158-s4c-speculative-sampling-with-syntactic-and-semantic-coherence-for-effic.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  S4C（投機的 Sampling with Syntactic and Semantic Coherence）は、自己回帰型大規模言語モデルの逐次生成を高速化する投機的復号方式である。軽量なドラフト側で複数の将来トークンを予測し、元の大規模モデルがまとめて検証するという基本構造を維持しながら、ドラフト系列の作り方と検証時の候補木を変更する。

- **2025-06 · [Routing Mamba: Scaling State Space Models with Mixture-of-Experts Projection](2025-2506.18145-routing-mamba-scaling-state-space-models-with-mixture-of-experts-project.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者らは115Mから10B総パラメータまでの構成、Mamba、Mamba2、Gated DeltaNet、注意機構とのハイブリッドであるSambaを評価する。

- **2025-06 · [Principled SVD-based Delta Compression via Quantization Error Minimization](2025-2506.11087-principled-svd-based-delta-compression-via-quantization-error-minimizati.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PRINMIXは、同じ基盤LLMから多数の微調整済みモデルを提供する場面を想定し、各モデルに固有の差分重みΔWだけを圧縮する方式である。

- **2025-06 · [MoTE: Mixture of Ternary Experts for Memory-efficient Large Multimodal Models](2025-2506.14435-mote-mixture-of-ternary-experts-for-memory-efficient-large-multimodal-mo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoTE（Mixture of Ternary Experts）は、画像と言語を扱うマルチモーダル言語モデルを密な事前学習済みモデルからMoEへ拡張する際、既存のFFNを高精度の共有専門家として保持し、新たな経路選択専門家だけを三値の重みで学習する方式である。

- **2025-06 · [Hopscotch: Discovering and Skipping Redundancies in Language Models](2025-2506.03303-hopscotch-discovering-and-skipping-redundancies-in-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Hopscotchは、Transformerの注意ブロックを丸ごと除去しながら、残る層の出力を少数のスカラーで再調整する構造圧縮法である。Llama-3.1-8B-InstructとQwen2.5-7B-Instructで検証し、Llamaでは四つの注意ブロックを削除しても平均性能保持率98.65%、七つ削除した場合も97.08%と報告する。

- **2025-06 · [Fine-grained Token Allocation Via Operation Pruning for Efficient MLLMs](2025-2507.02909-fine-grained-token-allocation-via-operation-pruning-for-efficient-mllms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の視覚トークン枝刈りは、重要と判定した少数のトークンを残すが、どの層・どのモジュールも同じ数の視覚トークンを処理しがちである。LLaVA-NeXT-7Bの実験では、視覚トークンを一律に減らす比較方式より同一演算予算で精度を保ち、特定の強圧縮条件ではTFLOPs86%削減とプリフィル CUDA遅延83%削減を平均性能約1%低下で報告する。

- **2025-06 · [Don't Pay Attention](2025-2506.11305-don-t-pay-attention.md)**  
  実装：[✓](https://github.com/rimads/avey-dpa) ・ リポジトリ内被引用：0  
  本論文は、Transformerの自己注意とRNN系の再帰状態の双方を用いず、長い系列から関連部分だけを選択してトークン間の相互作用を計算する言語モデルAveyを提案する。一方、一般NLPのゼロショット平均精度は1.52BではTransformer++の52.54%に対してAveyは51.53%で、全面的な品質優位ではない。

- **2025-06 · [Attention2D: Communication Efficient Distributed Self-Attention Mechanism](2025-2503.15758-attention2d-communication-efficient-distributed-self-attention-mechanism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈の自己注意をGPU間で分割する際、Ring 注意機構などの従来の一次元コンテキスト並列では、各GPUが自分のクエリ部分を担当しても、全てのキー・バリュー（KV）を順に受け取る必要がある。A100を16枚または64枚使用したGPT-3型モデルの学習では、Ring 注意機構に対してNOがそれぞれ2.4倍以上・4倍以上の学習性能を示す。

- **2025-06 · [Advancing Decoding Strategies: Enhancements in Locally Typical Sampling for LLMs](2025-2506.05387-advancing-decoding-strategies-enhancements-in-locally-typical-sampling-f.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案する適応的 Semantic-Aware Typicality Sampling（ASTS）は、(1) 過去のエントロピー変動を用いた候補区間の適応化、(2) 意味的類似度・関連度・多様性の複合採点、(3) 報酬と反復ペナルティによる確率再重み付け、(4) 正規化と温度調整、という段階を組み合わせる。

- **2025-06 · [Accurate Sublayer Pruning for Large Language Models by Exploiting Latency and Tunability Information](2025-2506.03510-accurate-sublayer-pruning-for-large-language-models-by-exploiting-latenc.md)**  
  実装：[✓](https://github.com/snudm-starlab/SPRINT) ・ リポジトリ内被引用：0  
  しかし注意とMLPは遅延への寄与が違い、削除後に残った層を補正することで回復できる誤差も異なる。Llama-2/3系モデルで、同程度の推論高速化を達成する従来方式と比較し、ゼロショット常識推論の正答率を最大23.88パーセントポイント改善したと報告する。

- **2025-05 · [Understanding Differential Transformer Unchains Pretrained Self-Attentions](2025-2505.16333-understanding-differential-transformer-unchains-pretrained-self-attentio.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者らは、この方式の利点を単純な注意の疎化として説明できるかを検証し、負の寄与による表現力、注意頭部の冗長性低下、学習時の安定性という三つの要因を分析した。Llama-3.2-3Bの11課題平均は60.2から64.2へ4.0ポイント改善し、針検索の平均正答率は66.9%から78.3%へ11.4ポイント改善した。

- **2025-05 · [STAR: Stage-Wise Attention-Guided Token Reduction for Efficient Large Vision-Language Models Inference](2025-2505.12359-star-stage-wise-attention-guided-token-reduction-for-efficient-large-vis.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  STAR（Stage-Wise 注意機構-Guided Token Reduction）は、画像とテキストを扱う大規模Vision-Language モデル（LVLM）の推論で、視覚トークンを視覚エンコーダ直後とLLMデコーダ中間層の二段階で削る学習不要の手法である。

- **2025-05 · [Sparsified State-Space Models are Efficient Highway Networks](2025-2505.20698-sparsified-state-space-models-are-efficient-highway-networks.md)**  
  実装：[✓](https://github.com/woominsong/Simba) ・ リポジトリ内被引用：0  
  Simbaは、Mambaなどの状態空間モデル（SSM）で、入力系列のトークンを層が深くなるほど段階的に間引く推論時の疎化手法である。付録の8枚のRTX2080 Ti上のPyTorch実装では、Mamba-2.8Bの入力長3Kの推論時間5.819秒に対しSimbaは3.217秒で、約1.81倍の高速化である。

- **2025-05 · [Semantic Retention and Extreme Compression in LLMs: Can We Have Both?](2025-2505.07289-semantic-retention-and-extreme-compression-in-llms-can-we-have-both.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、学習済み大規模言語モデル（LLM）に対する重み剪定と量子化の組合せを、同じ理論圧縮率で比較した研究である。主な結果は、25%剪定と4ビット量子化の組合せが、理論圧縮率TCr=81.25%の条件で、3ビット量子化のみより平均約20%高い意味保持率を示すというものだ。

- **2025-05 · [PreMoE: Proactive Inference for Efficient Mixture-of-Experts](2025-2505.17639-premoe-proactive-inference-for-efficient-mixture-of-experts.md)**  
  実装：[✓](https://github.com/JarvisPei/PreMoe) ・ リポジトリ内被引用：0  
  Mixture-of-Experts（MoE）は1トークン当たり一部の専門家（専門家）だけを実行するが、通常のサービングでは全専門家の重みをGPU/NPUメモリに常駐させる必要がある。PreMoEは、利用する領域をあらかじめ決められるなら、その領域で重要な専門家だけを残した小型MoEを、元モデルのルータlogitから再学習なしで事前構築する方式である。

- **2025-05 · [Multilingual Brain Surgeon: Large Language Models Can be Compressed Leaving No Language Behind](2025-2404.04748-multilingual-brain-surgeon-large-language-models-can-be-compressed-leavi.md)**  
  実装：[✓](https://github.com/X-LANCE/MBS) ・ リポジトリ内被引用：0  
  Multilingual Brain Surgeon（MBS）は、LLMの重み量子化や枝刈りで使うキャリブレーションデータを英語だけから選ぶと、事前学習時に割合が小さい言語の品質が大きく悪化する問題を扱う。

- **2025-05 · [LCD: Advancing Extreme Low-Bit Clustering for Large Language Models via Knowledge Distillation](2025-2506.12038-lcd-advancing-extreme-low-bit-clustering-for-large-language-models-via-k.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LCDは密度に基づく重み代表値の初期化、ヘッセ対角近似による代表値更新、段階的・投機的な代表値数削減、層別活性平滑化を組み合わせる極低ビット量子化方式。A100上の報告速度改善はBERT-large最大6.2倍、LLaMA-2-7Bは4.7倍。

- **2025-05 · [Exploring Federated Pruning for Large Language Models](2025-2505.13547-exploring-federated-pruning-for-large-language-models.md)**  
  実装：[✓](https://github.com/Pengxin-Guo/FedPrLLM) ・ リポジトリ内被引用：0  
  LLMの重みを削ってメモリ使用量を減らす剪定（枝刈り）は、モデルの入力活性化を校正データで観測して「消しても影響の小さい重み」を選ぶことが多い。LLaMA 7Bの50%疎化では、WikiText2の困惑度（PPL）が密モデル5.67、全データを集める集中剪定7.25、FedPrLLM層one-shot 7.32、クライアント単独7.44となる。

- **2025-05 · [Efficient Large Language Model Inference with Neural Block Linearization](2025-2505.21077-efficient-large-language-model-inference-with-neural-block-linearization.md)**  
  実装：[✓](https://github.com/LIONS-EPFL/NBL) ・ リポジトリ内被引用：0  
  Neural Block Linearization（NBL）は、特定の注意層について「その入力から出力を線形写像でどの程度予測できるか」を測り、予測しやすい層だけを統計的に推定した線形層で代替する。

- **2025-05 · [EdgeMM: Multi-Core CPU with Heterogeneous AI-Extension and Activation-aware Weight Pruning for Multimodal LLMs at Edge](2025-2505.10782-edgemm-multi-core-cpu-with-heterogeneous-ai-extension-and-activation-awa.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エッジでマルチモーダルLLM（MLLM）を実行する際、画像などをトークンに変換するエンコーダ、入力トークンをまとめて処理するLLM プリフィル、出力トークンを逐次生成するデコードでは、計算とメモリの比率が大きく異なる。ただし、これらは実チップを製造して測定した数字ではなく、シミュレーション・実装設計評価に基づく比較である。

- **2025-04 · [Thanos: A Block-wise Pruning Algorithm for Efficient Large Language Model Compression](2025-2504.05346-thanos-a-block-wise-pruning-algorithm-for-efficient-large-language-model.md)**  
  実装：[✓](https://github.com/vectozavr/thanos) ・ リポジトリ内被引用：0  
  Thanosは、大規模言語モデル（LLM）の学習済み重みを、少数の校正データだけで剪定するpost-学習 枝刈り手法である。原著Table 2では、LLaMA-3 8Bを30%構造化剪定したWikiText-2困惑度（PPL）がSparseGPTの82.19、Thanos（外れ値行保護α=0.1）の36.61となる。

- **2025-04 · [Task-Circuit Quantization: Leveraging Knowledge Localization and Interpretability for Compression](2025-2504.07389-task-circuit-quantization-leveraging-knowledge-localization-and-interpre.md)**  
  実装：[✓](https://github.com/The-Inscrutable-X/TACQ) ・ リポジトリ内被引用：0  
  Task-Circuit Quantization（TACQ）は、学習済みLLMを2〜3ビットへ圧縮した際の性能崩壊を抑えるため、全ての重みを同じ精度で丸めるのではなく、タスクにとって重要で、かつ実際の量子化で大きな損失を引き起こしそうな重みだけを16ビットのまま残す学習後量子化方式である。

- **2025-04 · [Scaling Test-Time Inference with Policy-Optimized, Dynamic Retrieval-Augmented Generation via KV Caching and Decoding](2025-2504.01281-scaling-test-time-inference-with-policy-optimized-dynamic-retrieval-augm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、外部文書を参照する検索拡張生成（RAG）を、検索タイミング、検索結果への忠実性、推論時のメモリ消費の三つの観点から改善する。提案は、方策最適化PORAG、選択的検索ATLAS、KV圧縮CRITICという異なる段階の機構を接続するものである。

- **2025-04 · [Saliency-driven Dynamic Token Pruning for Large Language Models](2025-2504.04514-saliency-driven-dynamic-token-pruning-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVキャッシュを削減する方式は、生成段階のメモリと注意計算を減らす一方、既に全入力を処理した後でKVを捨てるだけではプリフィル計算を取り戻せない。

- **2025-04 · [Multi-Branch Self-Drafting for LLM Inference Acceleration](2025-2224e69b745c-multi-branch-self-drafting-for-llm-inference-acceleration.md)**  
  実装：[✓](https://github.com/ZipECHO/Self-Draft) ・ リポジトリ内被引用：0  
  重みをメモリから読み出す費用が大きい状況では、1回の順伝播で得られるトークン数を増やすことが有効である。コーパスから固定的なn-gram候補を検索する方式も、実際の対話・コード生成との分布ずれに弱い。

- **2025-04 · [Gradual Binary Search and Dimension Expansion: A general method for activation quantization in LLMs](2025-2504.13989-gradual-binary-search-and-dimension-expansion-a-general-method-for-activ.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの低ビット事後量子化では、活性値の外れ値が量子化範囲を占有し、3〜4ビットの小さい整数レンジに通常の値を十分に割り当てられない。Mistral 7B v0.1を重み・活性・KVとも3ビット化した実験では、QuaRot単独の6課題平均18.43%がGBS併用58.31%へ改善した。

- **2025-04 · [Entropy-Based Block Pruning for Efficient Large Language Models](2025-2504.03794-entropy-based-block-pruning-for-efficient-large-language-models.md)**  
  実装：[✓](https://github.com/SalesforceAIResearch/EntroDrop) ・ リポジトリ内被引用：0  
  Transformerの構造化剪定では、隣接する層や注意機構 blockの入出力のcosine similarityを冗長度の指標として使うことが多い。

- **2025-04 · [Enhancing Ultra-Low-Bit Quantization of Large Language Models Through Saliency-Aware Partial Retraining](2025-2504.13932-enhancing-ultra-low-bit-quantization-of-large-language-models-through-sa.md)**  
  実装：[✓](https://github.com/TokuyuSou/ULB-SAPR) ・ リポジトリ内被引用：0  
  CaoとArefは、事前学習済み大規模言語モデルの重みを2ビットへ圧縮するとき、既存のApiQが残す精度劣化を、小規模な部分再学習だけで軽減する手法を提案した。LLaMA-2-7Bのゼロショット常識推論5課題平均は、全精度64.85%、ApiQ 55.91%に対して、提案法の最良設定で56.88%となる。

- **2025-04 · [Empower Vision Applications with LoRA LMM](2025-2411.00915-empower-vision-applications-with-lora-lmm.md)**  
  実装：[✓](https://github.com/mi150/VaLoRA) ・ リポジトリ内被引用：0  
  オンラインでは入力形状に合うタイル構成を事前探索したATMMカーネルを使い、LoRAを基盤重みへ統合するモード、統合しないモード、両者を混ぜるdeLoRAモードを負荷に応じて選ぶ。

- **2025-04 · [An Empirical Study on Prompt Compression for Large Language Models](2025-2505.00019-an-empirical-study-on-prompt-compression-for-large-language-models.md)**  
  実装：[✓](https://github.com/3DAgentWorld/Toolkit-for-Prompt-Compression) ・ リポジトリ内被引用：0  
  本論文は、長いプロンプトを事前に短縮してLLMへ渡すテキスト入力の圧縮について、6種類の方式を同一の評価枠組みで比較する実証研究である。また、単一A6000 GPU上の圧縮器処理時間はSCRLの67ms/入力からKiSの2410ms/入力まで大きく異なる。

- **2025-03 · [Universality of Layer-Level Entropy-Weighted Quantization Beyond Model Architecture and Size](2025-2503.04704-universality-of-layer-level-entropy-weighted-quantization-beyond-model-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMを一律4bitに量子化すると、容量は大幅に減るが、精度に敏感な層も同じビット幅へ押し込まれる。原著は1.6B〜70B級の複数モデルを対象に、MMLUで元モデルから概ね0.5%以内の精度差を目標とし、最大18%のメモリ削減を報告する。

- **2025-03 · [Towards Extreme Pruning of LLMs with Plug-and-Play Mixed Sparsity](2025-2503.11164-towards-extreme-pruning-of-llms-with-plug-and-play-mixed-sparsity.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの重みを学習後に削減する際、既存のMagnitude、SparseGPT、Wandaなどは、重みを残す重要度の測り方を工夫してきた。その後、各層の疎度を遺伝的アルゴリズムに似た進化的探索で調整する。代表例はLLaMA-13B、WikiText、75%削減、ブロック幅M=4のWandaである。

- **2025-03 · [Radar: Fast Long-Context Decoding for Any Transformer](2025-2503.10571-radar-fast-long-context-decoding-for-any-transformer.md)**  
  実装：[✓](https://github.com/BorealisAI/radar-decoding) ・ リポジトリ内被引用：0  
  Radarは、事前学習済みTransformerの重みを再学習せずに、長い文脈の自己回帰復号を高速化する方式である。論文のPG-19とコード系列の実験では、A100 40GB、Llama-3.1-8BおよびMistral-7Bを用い、密注意に近い困惑度（差がおよそ0.2以下）を維持しながら、2倍超の高速化を報告する。

- **2025-03 · [QUAD: Quantization and Parameter-Efficient Tuning of LLM with Activation Decomposition](2025-2503.19353-quad-quantization-and-parameter-efficient-tuning-of-llm-with-activation-.md)**  
  実装：[✓](https://github.com/hyx1999/Quad) ・ リポジトリ内被引用：0  
  重みと活性をともに4bitへ量子化する方式は、GPUの低精度行列積を利用できる可能性がある。

- **2025-03 · [Local Information Matters: Inference Acceleration For Grounded Conversation Generation Models Through Adaptive Local-Aware Token Pruning](2025-2503.23959-local-information-matters-inference-acceleration-for-grounded-conversati.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案する適応的局所認識トークン剪定は、画像を複数の意味的にまとまった領域へ分け、領域ごとに保持するトークンを確保する。OMG-LLaVAでも同程度の削減条件で、検証集合のAPが24.1から26.2、領域の重なり率が58.0から61.0へ改善した。

- **2025-03 · [Cost-Optimal Grouped-Query Attention for Long-Context Modeling](2025-2503.09579-cost-optimal-grouped-query-attention-for-long-context-modeling.md)**  
  実装：[✓](https://github.com/THUNLP/cost-optimal-gqa) ・ リポジトリ内被引用：0  
  Grouped-Query 注意機構（GQA）は複数のquery headでKey/Valueを共有し、通常のMulti-Head 注意機構（MHA）よりKVキャッシュ容量と読み出し量を抑える。

- **2025-03 · [ClusComp: A Simple Paradigm for Model Compression and Efficient Finetuning](2025-2503.13089-cluscomp-a-simple-paradigm-for-model-compression-and-efficient-finetunin.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ClusCompは、言語モデルの重みを一様な低ビット数値へ丸める代わりに、似た値の短いベクトルをまとめて代表ベクトルへ置き換える圧縮法である。

- **2025-03 · [Attention Condensation via Sparsity Induced Regularized Training](2025-2503.01564-attention-condensation-via-sparsity-induced-regularized-training.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、Transformerの注意行列を推論時に疎化する際の品質劣化を、学習時に注意確率を少数の要素へ集中させておくことで抑える手法を提案する。理想マスクでの精度維持と、低コストのマスク予測器が同じ結果を達成できるかは別問題であり、Hyper-注意機構では正則化モデルの方が悪い条件も存在する。

- **2025-02 · [Round Attention: A Novel Round-Level Attention Mechanism to Accelerate LLM Inference](2025-2502.15294-round-attention-a-novel-round-level-attention-mechanism-to-accelerate-ll.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  対話型LLMを長期間利用すると、過去の質問・回答を含むKVキャッシュが増え、GPUメモリ容量とCPUからの転送帯域が推論の制約になる。通常のトークン単位KV圧縮や選択は、注意スコアを層ごとに評価したり、小さなKV片を何度も転送したりする費用を生む。

- **2025-02 · [LIFT: A Novel Framework for Enhancing Long-Context Understanding of LLMs via Long Input Fine-Tuning](2025-2502.14644-lift-a-novel-framework-for-enhancing-long-context-understanding-of-llms-.md)**  
  実装：[✓](https://github.com/MuLabPKU/LIFT) ・ リポジトリ内被引用：0  
  LIFT（Long Input 微調整）は、長い文書をそのままLLMの入力コンテキストへ入れる代わりに、文書から生成した質問・回答（QA）で短文脈モデルをテスト時に微調整し、文書の情報をモデルのパラメータへ内在化させる方式である。

- **2025-02 · [DeltaLLM: Compress LLMs with Low-Rank Deltas between Shared Weights](2025-2501.18596-deltallm-compress-llms-with-low-rank-deltas-between-shared-weights.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案は単なる重みの複製ではない。Phi-3.5由来のDeltaPhi 3.35Bは3.8Bから約12%のパラメータ削減で、原著Table 1の5課題平均が0.66から0.59となる。

- **2025-02 · [CopySpec: Accelerating LLMs with Speculative Copy-and-Paste](2025-2502.08923-copyspec-accelerating-llms-with-speculative-copy-and-paste.md)**  
  実装：[✓](https://github.com/RazvanDu/CopySpec) ・ リポジトリ内被引用：0  
  CopySpecは、言語モデルが生成しようとしている文章の一部が、すでに入力文脈や過去の応答に現れている場合に、その部分を再計算せずに候補として再利用する推論高速化手法である。

- **2025-02 · [Activation-aware Probe-Query: Effective Key-Value Retrieval for Long-Context LLMs Inference](2025-2502.13542-activation-aware-probe-query-effective-key-value-retrieval-for-long-cont.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ActQKVは、長文脈の履歴KVキャッシュから生成に必要な情報を取り出すため、検索用の代表Queryの作り方と各層で何件のKVを取り出すかを改良する学習不要の推論手法である。

- **2025-01 · [Softplus Attention with Re-weighting Boosts Length Extrapolation in Large Language Models](2025-2501.13428-softplus-attention-with-re-weighting-boosts-length-extrapolation-in-larg.md)**  
  実装：[✓](https://github.com/iminfine/freeattn) ・ リポジトリ内被引用：0  
  提案するLSSAR（Length Scaled Softplus 注意機構 with Re-weighting）は、第一段でquery/keyの長さ依存正規化とSoftplusを用いて数値的に安定した重みを作り、第二段で重みを中心化して小さい値を抑え、残る大きな値をべき乗で強調する。

- **2025-01 · [Rethinking Post-Training Quantization: Introducing a Statistical Pre-Calibration Approach](2025-2501.09107-rethinking-post-training-quantization-introducing-a-statistical-pre-cali.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、LLMの学習後量子化（PTQ）において、校正用の入力文を使わずに重要な重みを識別し、低ビット量子化での品質低下を抑える事前校正（pre-calibration）を提案する。LLaMA-7B、4ビット系の実験では、量子化時間が57秒でAWQの838秒、SpQRの10,901秒より短い。

- **2025-01 · [DReSS: Data-driven Regularized Structured Streamlining for Large Language Models](2025-2501.17905-dress-data-driven-regularized-structured-streamlining-for-large-language.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかし従来の「重要度を測ってチャネルを直接削除し、その後に回復微調整する」方式では、削除予定チャネルに残っていた有用な情報まで失われる。

- **2025-01 · [CURing Large Models: Compression via CUR Decomposition](2025-2501.04211-curing-large-models-compression-via-cur-decomposition.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの重みを圧縮する場合、ニューロンや層を削除する構造化剪定はパラメータ数を減らせるが、ネットワーク構造と残差経路の整合性を変更する必要がある。原著はLlama3.1-8Bで10層をrank 256で分解し、8.03Bパラメータを7.32Bに削減する処理を129.45秒で実行した。

- **2025-01 · [A Proximal Operator for Inducing 2:4-Sparsity](2025-2501.18015-a-proximal-operator-for-inducing-2-4-sparsity.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPUの2:4疎行列演算では4重み中2つをゼロにすることで、通常の非構造化疎性よりも実行時に利用しやすい規則性が得られる。

- **2024-12 · [Taming Sensitive Weights: Noise Perturbation Fine-tuning for Robust LLM Quantization](2024-2412.06858-taming-sensitive-weights-noise-perturbation-fine-tuning-for-robust-llm-q.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの低ビット重み量子化では、全重みを一律に丸めると少数の敏感な重みが出力品質を大きく悪化させる。RTX 4090でOPT-1.3Bの128トークン生成を測ると、FP16外れ値0.5%を保持したsqLLMの2.62秒に対し、外れ値を保持しないNPFT併用版は2.40秒であった。

- **2024-12 · [Sparse Checkpointing for Fast and Reliable MoE Training](2024-2412.15411-sparse-checkpointing-for-fast-and-reliable-moe-training.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  これらの最大値は比較方式・モデル・障害条件が異なるため、同一条件で「4×31×8倍」を掛け合わせられるわけではない。

- **2024-12 · [Mixture of Hidden-Dimensions Transformer](2024-2412.05644-mixture-of-hidden-dimensions-transformer.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意機構のQ/K/V/O投影とFFNのup/gate/down投影を同じ隠れ次元の選択に合わせて部分実行し、総パラメータ数を増やしても1トークン当たりに活性化するパラメータ数を抑える。LLaMA2型355Mの10指標平均は全活性42.7、MoHDの50%活性42.3、75%活性43.2だった。

- **2024-12 · [LSAQ: Layer-Specific Adaptive Quantization for Large Language Model Deployment](2024-2412.18135-lsaq-layer-specific-adaptive-quantization-for-large-language-model-deplo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LSAQ（層-Specific 適応的 量子化）は、GPUの利用可能メモリが異なるエッジ端末へLLMを配備するため、層ごとに重みの量子化ビット幅を変える方式である。Llama-3-8Bの平均5bit条件では、既存の層別量子化LWQに対して6課題zero-shot平均67.59→69.10%、WikiText-2のPPL7.386→7.331と小幅に改善した。

- **2024-12 · [GUIDE: A Global Unified Inference Engine for Deploying Large Language Models in Heterogeneous Environments](2024-2412.04788-guide-a-global-unified-inference-engine-for-deploying-large-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルを実運用に配置する際、同じモデルでもGPU、推論ランタイム、入力長、バッチ数、GPU分割方式が変わると、初トークン遅延（TTFT）、復号スループット、GPUメモリ使用量が大きく変化する。

- **2024-12 · [Continuous Speech Tokens Makes LLMs Robust Multi-Modality Learners](2024-2412.04917-continuous-speech-tokens-makes-llms-robust-multi-modality-learners.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  音声対話を言語モデルへ統合する際、文字列と同様に音声も離散トークンIDへ変換し、次のIDを分類する方式が広く用いられる。Mini-Omniの10.84に対しFlow-Omniは8.81で、絶対2.03ポイント、相対約18.7%の低下となる。

- **2024-12 · [Constrained Decoding with Speculative Lookaheads](2024-2412.10418-constrained-decoding-with-speculative-lookaheads.md)**  
  実装：[✓](https://github.com/amazon-science/CDSL-NAACL2025) ・ リポジトリ内被引用：0  
  本論文の対象は、指定語をすべて含む文章や有害な要求に対する無害な応答など、通常の次トークン尤度だけでは満たしにくい制約付き生成である。この方法は制約達成率が高い一方、次の1トークンを確定するために大量のモデル呼び出しを要する。評価器、タスク、ドラフトとターゲットの組合せを分離して読む必要がある。

- **2024-11 · [Shrinking the Giant: Quasi-Weightless Transformers for Low Energy Inference](2024-2411.01818-shrinking-the-giant-quasi-weightless-transformers-for-low-energy-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トランスフォーマーの多層パーセプトロン（多層パーセプトロン）は、注意機構とは別に各トークンの表現を変換する二つの大きな行列積を持つ。この研究の主要成果は、比較的小規模な視覚トランスフォーマーと文字生成モデルで予測品質を概ね維持しながら、専用再構成可能回路と専用集積回路の合成評価で推論エネルギーを減らした点にある。

- **2024-11 · [LoRAExit: Empowering Dynamic Modulation of LLMs in Resource-limited Settings using Low-rank Adapters](2024-af0fed60b919-loraexit-empowering-dynamic-modulation-of-llms-in-resource-limited-setti.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案は、共通の基盤重みを残したまま、出口ごとに独立した低階数適応器（Low-Rank Adaptation; LoRA）を配置する方式である。

- **2024-11 · [Interactions Across Blocks in Post-Training Quantization of Large Language Models](2024-2411.03934-interactions-across-blocks-in-post-training-quantization-of-large-langua.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、LLMの学習後量子化（PTQ）でよく使われる各Transformerブロックを独立に最適化する手法が、どこまで妥当かを実験的に検証する。

- **2024-11 · [freePruner: A Training-free Approach for Large Multimodal Model Acceleration](2024-2411.15446-freepruner-a-training-free-approach-for-large-multimodal-model-accelerat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  主目的は視覚トークンの数を減らしてLLM側の事前入力処理（プリフィル）を軽くすることで、視覚エンコーダそのものを低ビット化する手法ではない。LLaVA-1.5では視覚トークンを約50%へ減らして複数の画像質問応答指標を維持し、Video-LLaVAではさらに高い冗長性を利用した削減を報告する。

- **2024-11 · [Anchor Attention, Small Cache: Code Generation with Large Language Models](2024-2411.06680-anchor-attention-small-cache-code-generation-with-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  手法は、行単位のトークン-wise Anchor 注意機構（TAA）、位置情報をアンカー内へ保持するMulti-Head Positional Encoding（MHPE）、浅い層のアンカーKVを深い層へ直接参照させる層-wise Anchor 注意機構（LAA）からなる。

### 3年前（2023-11〜2024-10）

- **2024-02 · [InfLLM: Training-Free Long-Context Extrapolation for LLMs with an Efficient Context Memory](2024-2402.04617-infllm-training-free-long-context-extrapolation-for-llms-with-an-efficie.md)**  
  実装：[✓](https://github.com/thunlp/InfLLM) ・ リポジトリ内被引用：84  
  InfLLMは、短い文脈長で事前学習された大規模言語モデル（LLM）を、重みの追加学習なしに非常に長い入力へ適用する方式である。

- **2024-09 · [OLMoE: Open Mixture-of-Experts Language Models](2024-2409.02060-olmoe-open-mixture-of-experts-language-models.md)**  
  実装：[✓](https://github.com/allenai/OLMoE) ・ リポジトリ内被引用：81  
  混合専門家（Mixture-of-Experts; MoE）は総パラメータを増やしながら、各トークンで一部専門家だけを実行することで、密 モデルより計算量を抑えられる。

- **2024-08 · [Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters](2024-2408.03314-scaling-llm-test-time-compute-optimally-can-be-more-effective-than-scaling-model-parameters.md)**  
  実装：✓ ・ リポジトリ内被引用：73  
  本論文は、大規模言語モデル（LLM）の推論時に追加の計算予算を与える場合、その予算を何回の独立サンプリング、何段の探索、何回の逐次自己修正へ割り当てるべきかを分析する。さらに、小型モデルの推論時追加計算と、約14倍大きいモデルの事前学習を浮動小数点演算回数（FLOPs）で揃えて比較する。

- **2024-02 · [Massive Activations in Large Language Models](2024-2402.17762-massive-activations-in-large-language-models.md)**  
  実装：[✓](https://github.com/locuslab/massive-activations) ・ リポジトリ内被引用：51  
  著者らは入力を変えたときの値の変動と、推論中に値を直接置換する介入実験から、巨大活性値が単なる数値的不安定さではなく、自己注意（self-注意機構）へ一定の加算成分を供給する暗黙のバイアス（implicit bias）として働くと結論付ける。

- **2023-11 · [LLaMA-VID: An Image is Worth 2 Tokens in Large Language Models](2023-2311.17043-llama-vid-an-image-is-worth-2-tokens-in-large-language-models.md)**  
  実装：[✓](https://github.com/dvlab-research/LLaMA-VID) ・ リポジトリ内被引用：49  
  LLaMA-VIDは、各フレームの情報を質問に応じて抽出する文脈トークンと画像内容を要約する内容トークンに分離する。ECCV 2024正式論文では、動画質問応答のMSVD-QAでVicuna-7B構成が正解率69.7%、MSRVTT-QAで57.7%、ActivityNet-QAで47.4%を記録した。

- **2024-07 · [Learning to (Learn at Test Time): RNNs with Expressive Hidden States](2024-2407.04620-learning-to-learn-at-test-time-rnns-with-expressive-hidden-states.md)**  
  実装：[✓](https://github.com/test-time-training/ttt-lm-pytorch) ・ リポジトリ内被引用：39  
  本論文は、再帰型ニューラルネットワーク（Recurrent Neural Network、RNN）の隠れ状態を単なる固定長ベクトルではなく、小さな機械学習モデルの重みとして表現するテスト時訓練（Test-Time 学習、TTT）層を提案する。

- **2023-12 · [Zoology: Measuring and Improving Recall in Efficient Language Models](2023-2312.04927-zoology-measuring-and-improving-recall-in-efficient-language-models.md)**  
  実装：[✓](https://github.com/HazyResearch/zoology) ・ リポジトリ内被引用：36  
  Zoologyは注意、H3、Hyena、RWKVなどの系列混合器を共通条件で比較し、注意なしの方式がどのようなトークンで失敗するかを細かく測定した研究である。Pileの検証データで、以前の文脈に現れた二語連接の続きを再び予測する位置を「連想想起ヒット」として抽出すると、該当位置は全トークンの6.4%にすぎない。

- **2024-02 · [CLLMs: Consistency Large Language Models](2024-2403.00835-cllms-consistency-large-language-models.md)**  
  実装：[✓](https://github.com/hao-ai-lab/Consistency_LLM) ・ リポジトリ内被引用：33  
  整合性大規模言語モデル（Consistency Large Language Models; CLLMs）は、Jacobi型の並列復号で使う仮の複数トークン列から、自己回帰復号の最終固定点へ速く近づくよう既存LLMを追加学習する。固定点に対する大域整合性損失と通常の自己回帰損失を併用し、追加の小型草案モデルなしで生成を高速化する。

- **2024-06 · [A Survey on Mixture of Experts in Large Language Models](2024-2407.06204-a-survey-on-mixture-of-experts-in-large-language-models.md)**  
  実装：[✓](https://github.com/withinmiaov/A-Survey-on-Mixture-of-Experts-in-LLMs) ・ リポジトリ内被引用：31  
  全パラメータ数を大きくしても活性化する部分を限定できるが、実機では選択された専門家へのトークン転送、専門家ごとの負荷の偏り、GPU間の全対全通信、巨大な専門家重みの配置・退避が新たな律速になる。

- **2023-12 · [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](2023-c83594f6f821-gqa-training-generalized-multi-query-transformer-models-from-multi-head-.md)**  
  実装：✓ ・ リポジトリ内被引用：26  
  本論文は、既に学習済みの多頭注意（MHA）モデルを破棄せず、復号時に読み出すKey/Value（KV）ヘッド数を減らすためのチェックポイント変換と追加学習を提案する。著者らはMHAのKV投影重みをグループ内で平均して初期化し、元の事前学習手順の5%相当を追加実行する。

- **2024-06 · [Your Absorbing Discrete Diffusion Secretly Models the Conditional Distributions of Clean Data](2026-2406.03736-your-absorbing-discrete-diffusion-secretly-models-the-conditional-distri.md)**  
  実装：[✓](https://github.com/ML-GSAI/RADD) ・ リポジトリ内被引用：23  
  RADDは吸収型離散拡散の逆過程で必要な条件付き確率を時刻から切り離し、マスク配置が変わらないステップの推論を省略する。理論的な損失の等価性と、実際の生成時間・困惑度の双方を検証した研究。

- **2024-08 · [LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression](2024-33c68d74c3c9-llmlingua-2-data-distillation-for-efficient-and-faithful-task-agnostic-p.md)**  
  実装：[✓](https://aka.ms/LLMLingua-2) ・ リポジトリ内被引用：21  
  本手法は圧縮を単語の保持/削除の二値分類として定式化し、双方向encoderのXLM-RoBERTa-largeやmBERTに圧縮の目的を直接学習させる。V100-32GB上のMeetingBank遅延測定では、非圧縮エンドツーエンド14.9秒に対し、5倍圧縮時5.2秒（2.9倍高速）と報告する。

- **2024-05 · [xRAG: Extreme Context Compression for Retrieval-augmented Generation with One Token](2024-2405.13792-xrag-extreme-context-compression-for-retrieval-augmented-generation-with.md)**  
  実装：[✓](https://github.com/Hannibal046/xRAG) ・ リポジトリ内被引用：16  
  検索拡張生成（Retrieval-Augmented Generation、RAG）は、外部の文書から関連情報を検索し、その本文を言語モデルへ入力することで、学習時点に含まれない知識を利用する。

- **2024-04 · [JetMoE: Reaching Llama2 Performance with 0.1M Dollars](2024-2404.07413-jetmoe-reaching-llama2-performance-with-0-1m-dollars.md)**  
  実装：[✓](https://github.com/myshell-ai/JetMoE) ・ リポジトリ内被引用：16  
  JetMoE-8Bは、混合専門家モデル（Mixture of エキスパート、MoE）の条件付き計算を順伝播ネットワーク（FFN）だけでなく自己注意機構へも拡張した、総パラメータ約80億の言語モデルである。論文はLlama2-7Bとの比較で推論演算量を約70%削減できると述べるが、これは実測の生成遅延が70%減るという意味ではない。

- **2023-12 · [Honeybee: Locality-enhanced Projector for Multimodal LLM](2023-2312.06742-honeybee-locality-enhanced-projector-for-multimodal-llm.md)**  
  実装：[✓](https://github.com/kakaobrain/honeybee) ・ リポジトリ内被引用：16  
  線形投射器は画像の各位置をほぼ一対一でトークン化するため空間情報を保持しやすいが、解像度が上がると視覚トークン数が増え、言語モデルの計算とメモリを圧迫する。Honeybeeは、出力視覚トークン数を任意に選べることと、局所的な画像構造を保持することを同時に満たす投射器を設計した。

- **2024-09 · [Moshi: a speech-text foundation model for real-time dialogue](2024-2410.00037-moshi-a-speech-text-foundation-model-for-real-time-dialogue.md)**  
  実装：[✓](https://github.com/kyutai-labs/moshi) ・ リポジトリ内被引用：15  
  Moshiは、音声認識、テキストLLM、音声合成を順番に実行する音声対話システムを、入力音声を聞きながら出力音声を生成する全二重の音声言語モデルへ置き換える研究である。音声質問応答の零例評価では、MoshiがWeb Questions 26.6%、LLaMA Questions 62.3%、音声版TriviaQA 22.8%の正答率を示した。

- **2023-11 · [Routing to the Expert: Efficient Reward-guided Ensemble of Large Language Models](2023-2311.08692-routing-to-the-expert-efficient-reward-guided-ensemble-of-large-language.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  本論文が解こうとする問題は、異なる得意分野を持つ既製の大規模言語モデル（LLM）を組み合わせる際、問い合わせごとに候補すべてを実行すると生成計算量が膨らむことである。一方、回答をすべて生成して報酬モデル（reward モデル）で順位付けする方式は品質の良い候補を後から選べるが、候補数に比例する生成費用を必要とする。

- **2024-08 · [Mini-Omni: Language Models Can Hear, Talk While Thinking in Streaming](2024-2408.16725-mini-omni-language-models-can-hear-talk-while-thinking-in-streaming.md)**  
  実装：[✓](https://github.com/gpt-omni/mini-omni) ・ リポジトリ内被引用：12  
  Mini-Omniは、言語モデルの応答文を最後まで生成してから独立した音声合成器へ渡す従来の直列方式を避け、文字トークンと音声トークンを一つの自己回帰生成過程の中で並列に出力する音声対話モデルである。

- **2024-02 · [Training-Free Long-Context Scaling of Large Language Models](2024-2402.17463-training-free-long-context-scaling-of-large-language-models.md)**  
  実装：[✓](https://github.com/HKUNLP/ChunkLlama) ・ リポジトリ内被引用：11  
  二重チャンク注意（Dual Chunk 注意機構、以下DCA）は、回転位置埋め込み（Rotary Position Embedding、以下RoPE）を用いた大規模言語モデルが、事前学習時より長い系列で位置関係を見失う問題に対する推論時の注意計算の変更である。最後の比較は特定の閉形式4課題の平均であり、汎用能力の94%を意味しない。

- **2024-09 · [LLaMA-Omni: Seamless Speech Interaction with Large Language Models](2024-2409.06666-llama-omni-seamless-speech-interaction-with-large-language-models.md)**  
  実装：[✓](https://github.com/ictnlp/LLaMA-Omni) ・ リポジトリ内被引用：9  
  従来のカスケード方式では、音声認識が入力を文字起こしし、その文字列を大規模言語モデルへ渡し、生成されたテキストを音声合成器へ送る。

- **2024-04 · [LongVLM: Efficient Long Video Understanding via Large Language Models](2024-2404.03384-longvlm-efficient-long-video-understanding-via-large-language-models.md)**  
  実装：[✓](https://github.com/ziplab/LongVLM) ・ リポジトリ内被引用：9  
  LongVLMは、長時間動画を入力する視覚言語モデル（Vision-Language モデル; VLM）で、画像符号化器から出る大量の視覚トークンを短時間区間ごとに統合する。100フレームを224×224画素で符号化し、元のパッチ特徴が約25,600トークンになる設定で、10区間×30トークンと全体特徴5トークンの計305視覚トークンへまとめる。

- **2024-06 · [Hybrid SLM and LLM for Edge-Cloud Collaborative Inference](2024-7a6bf47fa469-hybrid-slm-and-llm-for-edge-cloud-collaborative-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  本研究は、端末側で短い草稿を作り、クラウド側で草稿中のトークンをまとめて検証することで、品質と計算費用の間の連続的な選択肢を作る。GSM8KではLlama-2-7B単独の正答率21.68%、70B単独53.07%に対し、対数閾値−0.5の協調方式は52.24%を達成した。

- **2024-04 · [MixLoRA: Enhancing Large Language Models Fine-Tuning with LoRA-based Mixture of Experts](2024-2404.15159-mixlora-enhancing-large-language-models-fine-tuning-with-lora-based-mixt.md)**  
  実装：[✓](https://github.com/TUDB-Labs/MixLoRA) ・ リポジトリ内被引用：8  
  大規模言語モデルを多くの下流タスクへ適応させるとき、全パラメータを更新する方式は学習用メモリと計算時間が大きい。著者の概要にある「約30%のトークン計算遅延削減」は、元のMixLoRA実装に対する最適化効果を指す総括値であり、通常LoRAより30%速いという意味ではない。

- **2024-01 · [A Comprehensive Survey of Compression Algorithms for Language Models](2024-2401.15347-a-comprehensive-survey-of-compression-algorithms-for-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  枝刈り、量子化、知識蒸留、低ランク近似、パラメータ共有、効率的構造設計の六系統を、圧縮後の性能だけでなく、圧縮を実行するための学習・較正費用から比較するサーベイ。

- **2024-03 · [Exploring Post-training Quantization in LLMs from Comprehensive Study to Low Rank Compensation](2024-8166d1af62df-exploring-post-training-quantization-in-llms-from-comprehensive-study-to.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  この論文は、大規模言語モデル（Large Language モデル; LLM）の学習後量子化（Post-学習 量子化; PTQ）について、「何ビットにするか」だけでなく、重みと活性化のどちらを量子化するか、どの範囲で尺度を共有するか、誤差をどの方法で補正するか、モデル系列と規模によって結果がどう変わるかを分離して調べる。

- **2024-03 · [AI and Memory Wall](2024-2403.14123-ai-and-memory-wall.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  AI向け計算器の演算性能が急速に増える一方、DRAMやデバイス間通信の帯域は同じ速度で増えない。低バッチの自己回帰生成では重みの再読出しが支配的になり、FLOPsだけで推論性能を評価すると誤る。

- **2024-02 · [A Survey on Transformer Compression](2024-2402.05964-a-survey-on-transformer-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  論文はTransformer圧縮を、構造を保つ圧縮（量子化・知識蒸留）と、構造を変える圧縮（枝刈り・効率的なモデル構造）という二つの上位観点で整理する。

- **2023-12 · [Understanding the Potential of FPGA-Based Spatial Acceleration for Large Language Model Inference](2023-2312.15159-understanding-the-potential-of-fpga-based-spatial-acceleration-for-large.md)**  
  実装：[✓](https://github.com/cornell-zhang/allo/tree/main/examples) ・ リポジトリ内被引用：7  
  大規模言語モデルの推論を再構成可能な論理回路（FPGA）へ載せる従来方式の多くは、同じ演算器を複数の演算子・層へ順番に割り当てる時間多重型である。AMD Alveo U280上のGPT-2では、同じFPGAのDFXに対してプリフィル2.16倍、復号1.10倍の高速化を報告する。

- **2024-06 · [DeciMamba: Exploring the Length Extrapolation Potential of Mamba](2024-2406.14528-decimamba-exploring-the-length-extrapolation-potential-of-mamba.md)**  
  実装：[✓](https://github.com/assafbk/DeciMamba) ・ リポジトリ内被引用：5  
  Mambaは選択的状態空間モデル（Selective State Space モデル; SSM）の一種で、注意機構のように系列長の二乗へ比例する全組合せを直接計算せず、再帰的な隠れ状態へ過去の情報を集約する。

- **2024-03 · [Decoding Compressed Trust: Scrutinizing the Trustworthiness of Efficient LLMs Under Compression](2024-2403.15447-decoding-compressed-trust-scrutinizing-the-trustworthiness-of-efficient-.md)**  
  実装：[✓](https://github.com/decoding-comp-trust/comp-trust) ・ リポジトリ内被引用：5  
  LLM圧縮の評価は、通常の質問応答や知識課題の性能を維持できるかに偏りがちである。評価の中心的な結果は、同程度に圧縮する場合は量子化が枝刈りより元モデルの信頼性を再現しやすいこと、4-bit量子化では一部軸が改善し得ること、3-bitでは通常性能に現れにくい深刻な回帰が生じることである。

- **2024-01 · [APAR: LLMs Can Do Auto-Parallel Auto-Regressive Decoding](2024-2401.06761-apar-llms-can-do-auto-parallel-auto-regressive-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  各トークンの生成にはモデル重みの読み込みと注意計算が必要で、単一要求ではGPUの演算器が十分使われない一方、多数要求では注意計算とKVキャッシュ容量が制約になる。重要なのは独立した段落を別々の生成系列として同時に進めることであり、単に次の複数トークンを予測して検証する投機的復号（投機的復号）とは異なる。

- **2024-05 · [A Comprehensive Survey of Accelerated Generation Techniques in Large Language Models](2024-2405.13019-a-comprehensive-survey-of-accelerated-generation-techniques-in-large-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  第一は小型モデルなどで先のトークンを予測し、大型の対象モデルが並列に検証する投機的復号（投機的復号）、第二は簡単なトークンで深いTransformer層の計算を省略する早期終了（early exiting）、第三は複数位置のトークンを同時に生成・更新する非自己回帰生成（non-autoregressive generation）である。

- **2024-04 · [Hierarchical Context Merging: Better Long Context Understanding for Pre-trained LLMs](2024-2404.10308-hierarchical-context-merging-better-long-context-understanding-for-pre-t.md)**  
  実装：[✓](https://github.com/alinlab/HOMER) ・ リポジトリ内被引用：4  
  HOMER（Hierarchical cOntext MERging）は、入力を小区間に分けて初期層を処理し、中間層へ進むにつれて隣接区間を統合する。ICLR 2024の原著では、Llama-2-13B-chatの32Kトークンにおけるパスキー検索正答率が80.4%、位置尺度変更方式との併用で86.0%だった。

- **2024-02 · [Small Models, Big Insights: Leveraging Slim Proxy Models To Decide When and What to Retrieve for LLMs](2024-2402.12052-small-models-big-insights-leveraging-slim-proxy-models-to-decide-when-an.md)**  
  実装：[✓](https://github.com/plageon/SlimPlm) ・ リポジトリ内被引用：4  
  従来の自己評価型方式は大型言語モデル自身に暫定回答や判断を作らせるため、検索要否を知る段階で高価な大型モデル推論が増える。

- **2024-02 · [LongHeads: Multi-Head Attention is Secretly a Long Context Processor](2024-2402.10685-longheads-multi-head-attention-is-secretly-a-long-context-processor.md)**  
  実装：[✓](https://github.com/LuLuLuyi/LongHeads) ・ リポジトリ内被引用：4  
  LongHeadsは、事前学習時よりはるかに長い文章を既存の大規模言語モデルへ与える際、各注意頭が全文へ注意する必要はないという観察を利用した、追加学習不要の長文推論方式である。LLaMA-2-7Bを単一NVIDIA A100で評価し、32Kのパスキー検索でほぼ100%、CPUへKVキャッシュを退避した128K条件でも2K注意窓で100%を報告する。

- **2024-02 · [Generative Representational Instruction Tuning](2024-2402.09906-generative-representational-instruction-tuning.md)**  
  実装：[✓](https://github.com/ContextualAI/gritlm) ・ リポジトリ内被引用：4  
  GRIT（Generative Representational Instruction Tuning）は、文章生成と文章埋込みを一つの大規模言語モデルで処理するための指示調整方式である。7BモデルのGritLM-7Bは、56データ集合からなるMTEBの平均66.8を示し、同じ基盤モデルから表現専用で訓練した比較版の66.8と同等だった。

- **2024-10 · [Scaling Laws for Mixed Quantization](2024-2410.06722-scaling-laws-for-mixed-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  低bitのLLM推論では、すべての重みや活性を同じ低精度へ変換するより、精度低下に敏感な部分を高精度で残す混合量子化が有効になる場合がある。

- **2024-10 · [Multi-Draft Speculative Sampling: Canonical Decomposition and Theoretical Limits](2024-2410.18234-multi-draft-speculative-sampling-canonical-decomposition-and-theoretical.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  ドラフトが提案したトークンを受理できれば大型モデルの逐次呼出し回数を減らせるが、分布の一致を保証するには棄却後の補正サンプリングが必要である。実験ではA100 80GB、ドラフトOPT-125M、ターゲットOPT-13Bを使い、XSUMとDollyなどで候補数・サンプリング温度・切り詰め量を変えて比較した。

- **2024-10 · [BitStack: Any-Size Compression of Large Language Models in Variable Memory Environments](2024-2410.23918-bitstack-any-size-compression-of-large-language-models-in-variable-memor.md)**  
  実装：[✓](https://github.com/xinghaow99/BitStack) ・ リポジトリ内被引用：3  
  BitStackは、LLMの重みを固定の2bit、3bit、4bitなどへ一度だけ量子化する代わりに、複数の小さな残差ブロックへ分解して優先順位を付け、使えるメモリ量に応じて必要なブロックだけを読み込む学習不要の圧縮方式である。

- **2023-12 · [DSFormer: Effective Compression of Text-Transformers by Dense-Sparse Weight Factorization](2023-2312.13211-dsformer-effective-compression-of-text-transformers-by-dense-sparse-weig.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  DSFormerは、事前学習済みTransformerの大きな線形変換行列を、密な基底行列と半構造化された疎な係数行列の積に置き換える圧縮手法である。原著Table 1のGLUE開発セットでは、BERT-baseの8タスク単純平均82.05に対して、DSFormerの2倍圧縮が83.13、2.8倍圧縮が81.85、3.57倍圧縮が79.80である。

- **2024-10 · [TesseraQ: Ultra Low-Bit LLM Post-Training Quantization with Block Reconstruction](2024-2410.19103-tesseraq-ultra-low-bit-llm-post-training-quantization-with-block-reconst.md)**  
  実装：[✓](https://github.com/Intelligent-Computing-Lab-Yale/TesseraQ) ・ リポジトリ内被引用：2  
  大規模言語モデルを2〜4bitに事後量子化すると、重みの容量を大幅に減らせるが、2bit付近では量子化誤差が大きくなり、困惑度や下流タスク精度が崩れやすい。Table 2では5つの常識推論タスクの平均正答率が50.52%から59.27%へ上がる。

- **2024-10 · [SIGMA: Secure GPT Inference with Function Secret Sharing](2024-c544a15b6867-sigma-secure-gpt-inference-with-function-secret-sharing.md)**  
  実装：[✓](https://github.com/mpc-msri/EzPC/tree/master/GPU-MPC/experiments/sigma) ・ リポジトリ内被引用：2  
  SIGMAは関数秘密分散（Function Secret Sharing; FSS）によって複雑な非線形演算を二者間で実現し、事前に作った暗号鍵を使ってオンライン時の通信を抑える。代表結果は、系列長128の二者間オンライン推論において、既存のGPU秘匿計算系CrypTenより12.2～19倍短い実行時間である。

- **2024-08 · [Inference Optimizations for Large Language Models: Effects, Challenges, and Practical Considerations](2024-2408.03130-inference-optimizations-for-large-language-models-effects-challenges-and.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Donisch、Schacht、Lanquillonの論文は、LLMの推論資源を削減する研究を、量子化、剪定、知識蒸留、アーキテクチャ最適化という四群に分けた文献レビューである。§III-Dで紹介する投機的復号の2〜3倍の遅延改善は参照論文に帰属する値であり、このレビューの独立した再現結果ではない。

- **2024-06 · [MoreauPruner: Robust Pruning of Large Language Models against Weight Perturbations](2024-2406.07017-moreaupruner-robust-pruning-of-large-language-models-against-weight-pert.md)**  
  実装：[✓](https://github.com/ShiningSord/MoreauPruner) ・ リポジトリ内被引用：2  
  LLaMA-13Bでは回復微調整後の7課題平均が元64.97に対しMoreauPruner-GSで64.94まで近づく。一方、LLaMA3-8Bでは元70.33に対し同方式の20%剪定後が65.37で、性能損失が残る。

- **2024-06 · [Divergent Token Metrics: Measuring degradation to prune away LLM components -- and optimize quantization](2024-2311.01544-divergent-token-metrics-measuring-degradation-to-prune-away-llm-componen.md)**  
  実装：[✓](https://github.com/Aleph-Alpha/Divergent_Tokens) ・ リポジトリ内被引用：2  
  大規模言語モデルの圧縮では、重みを0にする枝刈りや、浮動小数点数を整数へ変換する量子化が、生成文をどの時点から変えてしまうかを把握する必要がある。この指標を使って行列ごとの枝刈り率を配分すると、Llama-2-13Bを全体75%疎化したとき、同じ平均疎化率の一様な大きさ基準の枝刈りより、WikiText2のPPLを13.512から8.101へ抑えられる。

- **2024-05 · [STAT: Shrinking Transformers After Training](2024-2406.00061-stat-shrinking-transformers-after-training.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  STATは、学習済みTransformerを再学習せずに小さくするため、フィードフォワードネットワーク（FFN）のニューロンと自己注意ヘッドを構造ごと除去する事後剪定手法である。いずれもA6000 48GBを1枚使った剪定計算が約2時間半で、これはモデル圧縮の処理時間である。

- **2024-03 · [SynCode: LLM Generation with Grammar Augmentation](2024-2403.01632-syncode-llm-generation-with-grammar-augmentation.md)**  
  実装：[✓](https://github.com/structuredllm/syncode) ・ リポジトリ内被引用：2  
  SynCodeは、言語モデルがJSON、SQL、Python、Goなどの形式言語を生成する際に、文脈自由文法（CFG）を満たすトークンだけを次の候補として残す制約付き復号方式である。

- **2024-03 · [Repoformer: Selective Retrieval for Repository-Level Code Completion](2024-2403.10059-repoformer-selective-retrieval-for-repository-level-code-completion.md)**  
  実装：[✓](https://github.com/amazon-science/Repoformer) ・ リポジトリ内被引用：2  
  Repoformerは、ソースコードの現在のファイルだけでは分からない別ファイルの関数定義や呼出し関係を、必要な場合だけ検索するコード補完方式である。RepoEvalで複数のコード言語モデルを調べると、検索によって補完が改善した例は概ね20%以下、変わらない例が60%以上、悪化する例も約20%あった。

- **2024-03 · [Accurate Block Quantization in LLMs with Outliers](2024-2403.20137-accurate-block-quantization-in-llms-with-outliers.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  長文脈LLMのKVキャッシュは系列長に比例して大きくなるため、重み量子化とは別にKVの保存精度を下げる必要がある。

- **2024-02 · [Plato: Plan to Efficiently Decode for Large Language Model Inference](2024-2402.12280-plato-plan-to-efficiently-decode-for-large-language-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Platoは、長い回答を1トークンずつ逐次生成する代わりに、質問を意味的な小課題（node）へ分割し、その間の依存関係を有向非巡回グラフ（DAG）として表現することで、依存しない部分を並列生成するLLM推論システムである。

- **2023-12 · [Mini-GPTs: Efficient Large Language Models through Contextual Pruning](2023-2312.12682-mini-gpts-efficient-large-language-models-through-contextual-pruning.md)**  
  実装：[✓](https://github.com/tval2/contextual-pruning) ・ リポジトリ内被引用：2  
  Mini-GPTsは、汎用言語モデルが保持する知識や計算経路の全てを個別業務で必要とするわけではないという仮説から、用途に応じて不要なニューロンを取り除く研究である。削除後には分野別データで微調整し、困惑度の回復を試みる。

- **2024-10 · [Understanding the Difficulty of Low-Precision Post-Training Quantization for LLMs](2024-2410.14570-understanding-the-difficulty-of-low-precision-post-training-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LLMの重みを2〜4bitへ圧縮すると、GPUメモリ使用量を減らせる可能性がある一方、言語モデルの予測品質が大きく落ちることがある。

- **2024-10 · [Taipan: Efficient and Expressive State Space Language Models with Selective Attention](2024-2410.18572-taipan-efficient-and-expressive-state-space-language-models-with-selecti.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Taipanはこの弱点を、すべてのトークンへ全面的な注意を適用するのではなく、軽量な二値ゲートで選別したトークンの表現だけを補強することで緩和する。学習時には選択率が目標値15%へ近づく損失を加え、選別の離散性をStraight-Through Gumbel-Softmaxで扱う。

- **2024-10 · [Scaling Stick-Breaking Attention: An Efficient Implementation and In-depth Study](2024-2410.17980-scaling-stick-breaking-attention-an-efficient-implementation-and-in-dept.md)**  
  実装：[✓](https://github.com/shawntan/stickbreaking-attention) ・ リポジトリ内被引用：1  
  本論文は、通常のTransformerが採用する正規化指数関数（softmax）に基づく自己注意（self-注意機構）を、棒折り過程（stick-breaking process）で定義される別の注意重みへ置き換える研究である。

- **2024-10 · [LevAttention: Time, Space, and Streaming Efficient Algorithm for Heavy Attentions](2024-2410.05462-levattention-time-space-and-streaming-efficient-algorithm-for-heavy-atte.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  実験は画像分類用の視覚Transformer（ViT）であり、LLMのKVキャッシュ圧縮やGPU推論時間の改善を直接実証したものではない。

- **2024-10 · [ESPACE: Dimensionality Reduction of Activations for Model Compression](2024-2410.05437-espace-dimensionality-reduction-of-activations-for-model-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ESPACEはこの順序を逆転させ、入力活性化を較正済みの低次元空間へ射影してから元の重みで学習し、推論時だけ結合則で圧縮重みへ置き換える。GPT3、Llama2、Nemotron4の複数モデルで、20〜55%程度の圧縮に対するPPL、下流精度、GEMMレイテンシ、プリフィル TTFTを評価する。

- **2024-06 · [Recurrent Context Compression: Efficiently Expanding the Context Window of LLM](2024-2406.06110-recurrent-context-compression-efficiently-expanding-the-context-window-o.md)**  
  実装：[✓](https://github.com/WUHU-G/RCC_Transformer) ・ リポジトリ内被引用：1  
  通常のTransformerは、学習時の文脈窓を超えると品質が落ちやすいという別の問題もある。Recurrent Context Compression（RCC）は、長文を短い区間へ分割し、各区間の情報を少数の隠れベクトルへ圧縮して復号器に渡す方式である。主張する32倍圧縮時のBLEU-4約0.95は、特定の短文再構成タスクでの値である。

- **2024-05 · [Dependency-Aware Semi-Structured Sparsity of GLU Variants in Large Language Models](2024-2405.01943-dependency-aware-semi-structured-sparsity-of-glu-variants-in-large-langu.md)**  
  実装：[✓](https://github.com/guozhiyu/glu_dass) ・ リポジトリ内被引用：1  
  LLaMA2やMistralのMLPでは、入力をGate投影とUp投影に通し、活性化関数と要素積によって中間表現を作り、Down投影で元の隠れ次元へ戻す。通常の重み単位剪定は各線形層の入力活性と重みの大きさを見て独立にゼロ化するため、ある中間ニューロンのDown側の寄与を重視しても、その中間値を作るGate/Up側の重みが多く削られる可能性がある。

- **2024-02 · [Why Lift so Heavy? Slimming Large Language Models by Cutting Off the Layers](2024-2402.11700-why-lift-so-heavy-slimming-large-language-models-by-cutting-off-the-laye.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデル（LLM）は多数のTransformer層を積み重ねることで表現能力を獲得する。重要な限定条件は、すべて分類タスク向けに再微調整した後の結果である。

- **2024-01 · [With Greater Text Comes Greater Necessity: Inference-Time Training Helps Long Text Generation](2024-2401.11504-with-greater-text-comes-greater-necessity-inference-time-training-helps-.md)**  
  実装：[✓](https://github.com/TemporaryLoRA/Temp-LoRA) ・ リポジトリ内被引用：1  
  本論文が扱うのは、数十万トークン規模の小説生成や長編翻訳を、短い注意窓しか持たない言語モデルで継続するときに発生する「古い情報の消失」と「長い鍵・値キャッシュ（KVキャッシュ）の費用」の両立問題である。近い文脈は通常の注意機構で直接読み、古い情報は一時的に変化した重みを介して利用する。

- **2024-10 · [Two are better than one: Context window extension with multi-grained self-injection](2024-2410.19318-two-are-better-than-one-context-window-extension-with-multi-grained-self.md)**  
  実装：[✓](https://github.com/Clement25/SharedLLM) ・ リポジトリ内被引用：0  
  一方、単純に過去文脈を一様圧縮すると、質問に必要な細かい事実まで失われやすい。論文要旨の速度改善（ストリーミング型比約2倍、エンコーダ・デコーダ型比約3倍）は対象実装・装置での比較であり、一般的なLLM推論のトークン/s改善倍率と同一視しない。

- **2024-10 · [Quamba: A Post-Training Quantization Recipe for Selective State Space Models](2024-2410.13229-quamba-a-post-training-quantization-recipe-for-selective-state-space-mod.md)**  
  実装：[✓](https://github.com/enyac-group/Quamba) ・ リポジトリ内被引用：0  
  Mambaのような選択的状態空間モデル（SSM）は、注意機構のKVキャッシュを保持せず、固定サイズの再帰状態で長い系列を処理できる。2.8BのMambaではOrin Nano 8GBで生成1トークン当たりの遅延が103.56msから60.17msに減り、6種zero-shot平均精度は63.1%から62.2%へ低下した。

- **2024-10 · [Optimized Spatial Architecture Mapping Flow for Transformer Accelerators](2024-2410.07407-optimized-spatial-architecture-mapping-flow-for-transformer-accelerators.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SAMT（Spatial 構成 Mapping for Transformers）は、Transformer推論の行列演算をTPU型・NVDLA型などの空間アクセラレータへ割り当てる際に、演算子融合の選択とPE（processing element）上のデータフローを同時に最適化する探索フローである。

- **2024-10 · [FastAttention: Extend FlashAttention2 to NPUs and Low-resource GPUs](2024-2410.16663-fastattention-extend-flashattention2-to-npus-and-low-resource-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FlashAttentionは注意重み行列をGPUの外部メモリに全量書き出さず、タイル単位の行列積とオンラインsoftmaxによって中間データの移動を抑える。

- **2024-10 · [Efficiently Deploying LLMs with Controlled Risk](2024-2410.02173-efficiently-deploying-llms-with-controlled-risk.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの運用費用を下げるために、小型モデルで簡単な質問へ回答し、難しい質問だけを大型モデルへ渡す階層的ルーティングが利用される。しかし、従来の費用最適化型ルータは「自信がないときには回答しない」という選択的予測の運用要件を、ルーティングの設計変数として十分に扱っていなかった。

- **2024-10 · [Correlation-Aware Select and Merge Attention for Efficient Fine-Tuning and Context Length Extension](2024-2410.04211-correlation-aware-select-and-merge-attention-for-efficient-fine-tuning-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案する MS 注意機構（Merge-Selection 注意機構） は、すべてのトークン対の注意を計算せず、質問側と参照側のトークンを領域へ分割し、領域代表の関連度から重要なKV領域を選ぶ。

- **2024-10 · [COrAL: Order-Agnostic Language Modeling for Efficient Iterative Refinement](2024-2410.09675-coral-order-agnostic-language-modeling-for-efficient-iterative-refinemen.md)**  
  実装：[✓](https://github.com/YuxiXie/COrAL) ・ リポジトリ内被引用：0  
  COrAL（Context-Wise Order-Agnostic Language Modeling）は、短い局所window内だけで生成順序を柔軟にし、前方の複数トークン予測と既出トークンの後方再構成を同じdecoder-onlyモデルへ学習させる方式である。

- **2024-10 · [Approximately Aligned Decoding](2024-2410.01103-approximately-aligned-decoding.md)**  
  実装：[✓](https://github.com/amazon-science/Approximately-Aligned-Decoding) ・ リポジトリ内被引用：0  
  Approximately Aligned Decoding（AprAD）は、大規模言語モデルの生成途中で禁止文字、構文違反、存在しないAPIの呼び出しなどを検出したとき、生成済み接頭辞をどこまで残して再開するかを投機的サンプリング（投機的 sampling）の受理・棄却計算で決める方式である。

- **2024-09 · [Internalizing ASR with Implicit Chain of Thought for Efficient Speech-to-Speech Conversational LLM](2024-2409.17353-internalizing-asr-with-implicit-chain-of-thought-for-efficient-speech-to.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  音声入力から音声出力を生成する大規模言語モデルでは、音声を文字へ転写し、文字で回答を考え、再び音声へ変換する方式が使われる。RTX 3090を使った測定では、初回出力音声トークンの遅延が1.09秒から0.87秒へ低下した。

- **2024-09 · [Hyper-Compression: Model Compression via Hyperfunction](2024-2409.00592-hyper-compression-model-compression-via-hyperfunction.md)**  
  実装：[✓](https://github.com/Juntongkuki/Hyper-Compression) ・ リポジトリ内被引用：0  
  学習済み大規模言語モデルの重み容量を小さくする一般的な方法は、低ビット量子化、枝刈り、低ランク分解である。LLaMA2-7Bでは原著Table 5で保存容量12.50GB→4.80GB（2.60倍圧縮）、8課題の平均正答率65.88%→64.89%（0.99ポイント低下）を報告する。

- **2024-07 · [FlashNorm: Fast Normalization for Transformers](2024-2407.09577-flashnorm-fast-normalization-for-transformers.md)**  
  実装：[✓](https://github.com/OpenMachine-ai/transformer-tricks) ・ リポジトリ内被引用：0  
  RMSNormは多くのLLMで注意機構やFFNの直前に置かれ、活性ベクトルの二乗平均平方根で各要素を割り、学習済みスケールを掛ける。T4 GPUのnorm-then-project単体実験では、SmolLM2-135M相当の4096トークンで0.704msから0.468msへ、8192トークンで0.929msから0.599msへ短縮した。

- **2024-07 · [Efficient LLM Pruning with Global Token-Dependency Awareness and Hardware-Adapted Inference](2024-614ce03da14c-efficient-llm-pruning-with-global-token-dependency-awareness-and-hardwar.md)**  
  実装：[✓](https://github.com/oshindutta/TVAprune) ・ リポジトリ内被引用：0  
  TVA-Prune（トークン Dependency-aware Variational Adapted 枝刈り）は、LLMの注意ヘッド、FFNの中間次元、トークンの隠れ次元をまとめて削減する構造的枝刈り方式である。

- **2024-07 · [Compensate Quantization Errors+: Quantized Models Are Inquisitive Learners](2024-2407.15508-compensate-quantization-errors-quantized-models-are-inquisitive-learners.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Compensate Quantization Errors+（CQE+）は、学習済み大規模言語モデルの重みを2〜4ビットへ量子化する際、量子化の整数格子に適した重み分布へ調整する方法を提案する。

- **2024-07 · [Attention Is All You Need But You Don't Need All Of It For Inference of Large Language Models](2024-2407.15516-attention-is-all-you-need-but-you-don-t-need-all-of-it-for-inference-of-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TransformerベースのLLMでは、各層に注意機構サブレイヤとMLPサブレイヤがあり、推論時にもすべての層を通すのが通常である。主要な結果として、Llama2-13Bで後段注意機構の約33%を省くと、OpenLLMのARC、HellaSwag、TruthfulQA、MMLUの平均スコアは58.5から56.8へ低下する。

- **2024-07 · [Accelerating Large Language Model Inference with Self-Supervised Early Exits](2024-2407.21082-accelerating-large-language-model-inference-with-self-supervised-early-e.md)**  
  実装：[✓](https://anonymous.4open.science/r/BranchyLLM-B870) ・ リポジトリ内被引用：0  
  通常の自己回帰型言語モデルは、生成するトークンが簡単か難しいかにかかわらず、全層を通して次トークンの確率を計算する。提案は二段階である。Pythia-2.8Bの実験では、LayerSkipの最良固定設定のドラフト受理率53.6%に対して、DSSDは閾値0.9で88.8%を報告した。

- **2024-06 · [VTrans: Accelerating Transformer Compression with Variational Information Bottleneck based Pruning](2024-2406.05276-vtrans-accelerating-transformer-compression-with-variational-information.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来は残差接続などの整合性が難しく埋め込みを温存する方式が多かったが、埋め込みが全パラメータの相当部分を占める小・中規模モデルでは、そこを残すことが極端な圧縮の障害となる。「剪定を25倍高速化」は生成TPSが25倍になる意味ではない。

- **2024-06 · [VcLLM: Video Codecs are Secretly Tensor Codecs](2024-2407.00467-vcllm-video-codecs-are-secretly-tensor-codecs.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルのメモリと通信の問題は重みだけではない。既存のGPTQやAWQは主に重み、1-bit Adamや1-bit LAMBは主に学習勾配を対象にしており、各テンソル種別に異なる圧縮手法を組み合わせる必要がある。原著は重み約25GBとKV約7.2GBを4つのメモリ約8GBの装置へ分割し、長文脈推論を成立させる構成を示す。

- **2024-06 · [On Efficient Language and Vision Assistants for Visually-Situated Natural Language Understanding: What Matters in Reading and Reasoning](2024-2406.11823-on-efficient-language-and-vision-assistants-for-visually-situated-natura.md)**  
  実装：[✓](https://github.com/naver-ai/elva) ・ リポジトリ内被引用：0  
  本論文は、視覚と言語を組み合わせた助手（Vision-Language Assistant; VLA）が文書画像を理解する際の推論資源を削減しながら、画像中の文字を読み取る精度を維持するためのモデル設計を調べる。

- **2024-06 · [Compensate Quantization Errors: Make Weights Hierarchical to Compensate Each Other](2024-2406.16299-compensate-quantization-errors-make-weights-hierarchical-to-compensate-e.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの事後量子化（PTQ）は、学習済みの重みを低ビット整数へ丸めることでモデルのメモリ・帯域を減らす。

- **2024-05 · [Task-agnostic Distillation of Encoder-Decoder Language Models](2024-2305.12330-task-agnostic-distillation-of-encoder-decoder-language-models.md)**  
  実装：[✓](https://github.com/GeneZC/MiniEnD) ・ リポジトリ内被引用：0  
  提案法MiniEnDは、教師と学生の最終層の関係分布を整合する蒸留に、エンコーダとデコーダの接続を反映する損失を追加する。

- **2024-05 · [OpenBA-V2: Reaching 77.3% High Compression Ratio with Fast Multi-Stage Pruning](2024-2405.05957-openba-v2-reaching-77-3-high-compression-ratio-with-fast-multi-stage-pru.md)**  
  実装：[✓](https://github.com/OpenNLG/OpenBA-v2) ・ リポジトリ内被引用：0  
  OpenBA-V2は、中国語・英語を中心に学習したencoder-decoder型のOpenBA（15Bパラメータ）を、3.4Bへ縮小するための多段階圧縮・継続事前学習の研究である。元モデルから約77.3%のパラメータを削除しながら、層単位、行列の幅方向、語彙埋め込みという異なる削減対象を順番に処理する。

- **2024-05 · [Integer Scale: A Free Lunch for Faster Fine-grained Quantization of LLMs](2024-2405.14597-integer-scale-a-free-lunch-for-faster-fine-grained-quantization-of-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの重みを小さなグループに分けて量子化すると、グループごとに異なる量子化スケールを選べるため、粗い量子化より精度を維持しやすい。原著は最大1.85倍のFP16比エンドツーエンド速度改善、浮動小数点スケールの同等カーネル比最大1.83倍などを報告する。

- **2024-04 · [LongVQ: Long Sequence Modeling with Vector Quantization on Structured Memory](2024-2404.11163-longvq-long-sequence-modeling-with-vector-quantization-on-structured-mem.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LongVQは、SSMの構造化長期記憶とベクトル量子化されたKeyによる固定長の注意を組み合わせ、系列長に対して線形時間で動作するハイブリッドモデルである。

- **2024-03 · [QuantTune: Optimizing Model Quantization with Adaptive Outlier-Driven Fine Tuning](2024-2403.06497-quanttune-optimizing-model-quantization-with-adaptive-outlier-driven-fin.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  整数のビット幅を小さくすると、重みと活性を低精度で表現でき、メモリや演算資源を節約できる可能性がある。しかし通常の対称一様量子化では、一部の極端に大きい活性値に量子化の最大範囲を合わせると、同じビット数で表現する刻み幅が粗くなる。

- **2024-03 · [Outrageously Fast LLMs: Faster Inference and Fine-Tuning with Moefication and LoRA](2024-cdf8e588e197-outrageously-fast-llms-faster-inference-and-fine-tuning-with-moefication.md)**  
  実装：[✓](https://github.com/chiyotsai/MoEfication-with-LoRA) ・ リポジトリ内被引用：0  
  重要な結果は、モデル規模によって高速化の符号が逆転することである。著者の表4では、単一の画像処理用計算機ではなく、エヌビディアのRTX 3090で測った相対推論時間が、小型のT5-smallでは元の135.1%、T5-baseでは101.4%、T5-largeでは88.9%、T5-3Bでは71.1%となった。

- **2024-03 · [Efficient Encoder-Decoder Transformer Decoding for Decomposable Tasks](2024-2403.13112-efficient-encoder-decoder-transformer-decoding-for-decomposable-tasks.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来のプロンプト-in-Encoder（PIE）では、各項目の問いを入力文書と結合してencoderへ渡すため、入力を問いの数だけ再符号化し、cross-注意機構でも問いごとに異なるencoder表現を読み出す。

- **2024-02 · [User-LLM: Efficient LLM Contextualization with User Embeddings](2024-2402.13598-user-llm-efficient-llm-contextualization-with-user-embeddings.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  履歴を項目IDと属性IDの列として符号化し、小型の自己回帰型利用者エンコーダで密なベクトル列へ変換した後、LLMの中間層に交差注意（cross-注意機構）で取り込ませる。MovieLens 20M、Google Review、Amazon Reviewを用いた実験では、長い履歴を使うほど計算量削減が顕著になった。

- **2024-02 · [Unifying Linear-Time Attention via Latent Probabilistic Modelling](2024-2402.17512-unifying-linear-time-attention-via-latent-probabilistic-modelling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  標準Transformerの自己注意は、系列内の各トークンが過去の各トークンを参照するため、長い入力のプリフィルではトークン数の二乗に比例する注意計算を必要とする。生成時には過去のKey/ValueをKVキャッシュへ保持するため、文脈長とともにメモリ容量も増える。本論文は、線形注意を潜在変数を介した確率分布として解釈する。

- **2024-02 · [RepQuant: Towards Accurate Post-Training Quantization of Large Transformer Models via Scale Reparameterization](2024-2402.05628-repquant-towards-accurate-post-training-quantization-of-large-transforme.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  これらへ単一の量子化尺度や単純な2進対数量子化を直接適用すると、4ビット付近では重要な情報が失われやすい。

- **2024-01 · [Infini-gram: Scaling Unbounded n-gram Language Models to a Trillion Tokens](2024-2401.17377-infini-gram-scaling-unbounded-n-gram-language-models-to-a-trillion-token.md)**  
  実装：[✓](https://github.com/liujch1998/infini-gram) ・ リポジトリ内被引用：0  
  従来のn-gram方式は直前の数トークンしか参照しないため、長い固有表現や定型句を扱いにくかった。

- **2023-12 · [A Performance Evaluation of a Quantized Large Language Model on Various Smartphones](2023-2312.12472-a-performance-evaluation-of-a-quantized-large-language-model-on-various-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  対象はiPhone 14、14 Pro、14 Pro Max、15、15 Pro Maxの五機種で、llama.cppとGGUFを利用し、orcaminiv37Bを3bit small K-S量子化した約2.95GiBのモデルを使用する。

### 4年前（2022-11〜2023-10）

- **2022-11 · [Efficiently Scaling Transformer Inference](2022-2211.05102-efficiently-scaling-transformer-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：261  
  TPU v4上の大規模Transformer推論を通信・メモリ・計算モデルから設計し、2D重み固定/重み収集の切替とバッチ分割MQAで540B級の低遅延・高MFU・長文脈を両立する。

- **2023-06 · [A Simple and Effective Pruning Approach for Large Language Models](2023-2306.11695-a-simple-and-effective-pruning-approach-for-large-language-models.md)**  
  実装：[✓](https://github.com/locuslab/wanda) ・ リポジトリ内被引用：243  
  Wanda（重みと活性による枝刈り、枝刈り by 重み and 活性値）は、大規模言語モデルの線形層を追加学習も残存重みの更新も行わず疎化する方法である。LLaMA-7Bを50%非構造疎化したとき、WikiTextの困惑度は単純大きさ枝刈り17.29、Wanda 7.26、SparseGPT 7.22であり、軽い処理でも品質を大幅に保てる。

- **2023-08 · [YaRN: Efficient Context Window Extension of Large Language Models](2023-2309.00071-yarn-efficient-context-window-extension-of-large-language-models.md)**  
  実装：[✓](https://github.com/jquesnelle/yarn) ・ リポジトリ内被引用：113  
  大規模言語モデルの回転位置埋め込み（Rotary Position Embedding、RoPE）は、クエリとキーを位置に応じた角度だけ回転し、両者の内積が相対位置を反映するように設計される。128Kまでのパスキー検索では7B・13Bとも平均正答率99.4%を報告する。

- **2023-10 · [Ring Attention with Blockwise Transformers for Near-Infinite Context](2023-2310.01889-ring-attention-blockwise-transformers.md)**  
  実装：[✓](https://github.com/lhao499/llm_large_context) ・ リポジトリ内被引用：102  
  キー・値ブロックをリング転送しながらブロック注意計算を重畳し、系列長に依存しない活性化メモリで最大文脈長をデバイス数に比例して拡張する分散注意方式。

- **2023-04 · [Learning to Compress Prompts with Gist Tokens](2023-2304.08467-learning-to-compress-prompts-with-gist-tokens.md)**  
  実装：[✓](https://github.com/jayelm/gisting) ・ リポジトリ内被引用：84  
  指示の鍵・値状態をそのままキャッシュすれば再計算は減るものの、保持する状態の長さは指示トークン数に比例する。Jesse Muらの研究は、指示の意味を短い要旨トークン（gist トークン）の内部状態へ集約し、後続の異なる入力に再利用する「要旨化（gisting）」を提案する。

- **2023-07 · [In-context Autoencoder for Context Compression in a Large Language Model](2023-2307.06945-in-context-autoencoder-for-context-compression-in-a-large-language-model.md)**  
  実装：[✓](https://github.com/getao/icae) ・ リポジトリ内被引用：66  
  本論文は、大規模言語モデル（LLM）の長い入力文脈を、同じモデルがそのまま利用できる短い連続表現へ学習圧縮する文脈内自己符号化器（In-context Autoencoder、ICAE）を提案する。

- **2023-05 · [FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance](2023-2305.05176-frugalgpt-how-to-use-large-language-models-while-reducing-cost-and-impro.md)**  
  実装：[✓](https://github.com/stanford-futuredata/FrugalGPT) ・ リポジトリ内被引用：64  
  FrugalGPTは、価格・正確さ・誤答の種類が異なる複数の大規模言語モデル（LLM）を、予算を超えずに組み合わせる推論時のサービス選択方式である。

- **2023-07 · [Hyena Hierarchy: Towards Larger Convolutional Language Models](2023-2302.10866-hyena-hierarchy-towards-larger-convolutional-language-models.md)**  
  実装：[✓](https://github.com/HazyResearch/safari) ・ リポジトリ内被引用：47  
  従来の線形注意や疎注意はこの費用を減らせる一方、長距離の連想記憶や文脈内での規則適用に必要な表現能力が不足し、密な注意層を混ぜないと大規模モデルの品質に届かない場合があった。著者らは、注意機構が持つ三つの性質、すなわち入力に応じて演算内容が変わること、系列長に対してパラメータ数が線形に増えないこと、任意の過去位置を参照できることに注目した。

- **2023-06 · [MiniLLM: On-Policy Distillation of Large Language Models](2023-2306.08543-minillm-on-policy-distillation-of-large-language-models.md)**  
  実装：[✓](https://github.com/microsoft/LMOps/tree/main/minillm) ・ リポジトリ内被引用：41  
  MiniLLMは、大規模な教師言語モデルから小規模な学生言語モデルへ生成能力を移す知識蒸留（Knowledge Distillation; KD）の学習方式である。

- **2023-07 · [Skeleton-of-Thought: Prompting LLMs for Efficient Parallel Generation](2023-2307.15337-skeleton-of-thought-prompting-llms-for-efficient-parallel-generation.md)**  
  実装：[✓](https://github.com/imagination-research/sot) ・ リポジトリ内被引用：23  
  Skeleton-of-Thought（SoT）はモデル内部の注意カーネルを変えず、回答を「骨格作成」と「各項目の独立展開」に分解して、後半を並列実行する。高速化の源泉は総トークン数を必ず減らすことではなく、長い1本の逐次デコードを複数の短いデコードへ分け、クリティカルパスを短くする点にある。

- **2023-10 · [Compressing LLMs: The Truth is Rarely Pure and Never Simple](2023-2310.01382-compressing-llms-the-truth-is-rarely-pure-and-never-simple.md)**  
  実装：[✓](https://github.com/VITA-Group/llm-kick) ・ リポジトリ内被引用：21  
  困惑度（perplexity）がほぼ維持されても、圧縮モデルの事実知識や指示追従は失われ得る。知識をモデル内部から答える課題と、外部文脈を与える検索・要約を分けて評価することで、枝刈りと量子化の能力別の弱点を可視化する。

- **2023-07 · [When Not to Trust Language Models: Investigating Effectiveness of Parametric and Non-Parametric Memories](2023-2212.10511-when-not-to-trust-language-models-investigating-effectiveness-of-paramet.md)**  
  実装：[✓](https://github.com/AlexTMallen/adaptive-retrieval) ・ リポジトリ内被引用：16  
  著者らは、質問の対象実体のウィキペディア閲覧数を人気度の代理指標として、質問の関係種別ごとに閾値を学習し、閾値未満の質問だけ外部文書を検索する適応的検索（適応的 Retrieval）を提案した。PopQAで最良の組合せは正答率46.5%となり、どの常時検索・検索なしの構成よりも5.3ポイント高いと報告する。

- **2023-07 · [Efficient Guided Generation for Large Language Models](2023-2307.09702-efficient-guided-generation-for-large-language-models.md)**  
  実装：[✓](https://github.com/dottxt-ai/outlines) ・ リポジトリ内被引用：15  
  従来方式は、各生成ステップで語彙中のN個のトークン文字列を照合し、現在の部分出力に続けてよいかを調べるため、制約判定が少なくとも語彙数に比例する。

- **2023-05 · [Tabi: An Efficient Multi-Level Inference System for Large Language Models](2023-1685e89adb79-tabi-an-efficient-multi-level-inference-system-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  Tabiは、大型の言語モデルを用いた分類・回帰サービスで、すべての要求に同じ大きなモデルを実行する無駄を削減する推論システムである。サービスが例えば分類正答率95%以上という精度下限を指定すると、従来の推論基盤は平均精度が下限を超える単一モデルを選び、簡単な入力にも難しい入力にも同じ計算を行う。

- **2023-10 · [RECOMP: Improving Retrieval-Augmented LMs with Compression and Selective Augmentation](2023-2310.04408-recomp-improving-retrieval-augmented-lms-with-compression-and-selective-.md)**  
  実装：[✓](https://github.com/carriex/recomp) ・ リポジトリ内被引用：12  
  Xu、Shi、ChoiによるRECOMPは、検索拡張言語モデル（Retrieval-Augmented Language モデル、RALM）の推論時に、検索した文書をそのままモデルの文脈へ連結する方式を改める。原著は文脈トークン数を主要な効率指標とするため、文書量が5%になったという数値をGPU実行時間が20倍速くなったと読み替えてはならない。

- **2023-10 · [MatFormer: Nested Transformer for Elastic Inference](2023-2310.07707-matformer-nested-transformer-for-elastic-inference.md)**  
  実装：[✓](https://github.com/devvrit/matformer) ・ リポジトリ内被引用：12  
  大規模言語モデルを配備する際、同じ品質・遅延・計算資源の要求を持つ利用者ばかりとは限らない。モデルを後から枝刈りして調整する方法では、新しいサイズごとに再学習や調整を要することもある。

- **2023-10 · [GEMINI: Fast Failure Recovery in Distributed Training with In-Memory Checkpoints](2023-075d73797107-gemini-fast-failure-recovery-in-distributed-training-with-in-memory-chec.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  保存頻度を増やせば故障前に失う学習進捗は減るが、遠隔ストレージの集約帯域が不足すると保存そのものが長くなり、学習を妨げる。提案は単なる「メモリへ保存する」という発想ではない。

- **2023-10 · [A Dynamic LLM-Powered Agent Network for Task-Oriented Agent Collaboration](2023-2310.02170-a-dynamic-llm-powered-agent-network-for-task-oriented-agent-collaboratio.md)**  
  実装：[✓](https://github.com/SALT-NLP/DyLAN) ・ リポジトリ内被引用：6  
  複数の大規模言語モデルエージェントを協調させる方式では、担当する役割や通信順序を固定すると、問題によっては不得意なエージェントの発言が増え、余計なモデル呼出しと品質低下を招く。原著のHumanEvalコード生成評価では、単一実行の正答率73.2%に対してDyLANは82.9%、平均モデルAPI呼出し数は16.85回だった。

- **2022-11 · [Iron: Private Inference on Transformers](2022-0ed2662d9eee-iron-private-inference-on-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  この構成では、サーバーは入力内容を読めるため、医療文書や企業機密をそのまま送信したくない利用者には問題がある。Ironはこの二つの律速点に特化した手順を設計する。従来の行列・ベクトル積を行ごとに繰り返す方式と比較し、一般の行列形状で出力行数の平方根程度の通信削減を理論的に示す。

- **2023-10 · [Look-Up mAI GeMM: Increasing AI GeMMs Performance by Nearly 2.5x via msGeMM](2023-2310.06178-look-up-mai-gemm-increasing-ai-gemms-performance-by-nearly-2-5x-via-msge.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  重みを4ビット整数へ量子化すれば、各重みが取れる値は16種類に限られる。約2.5倍という代表値を、現在のGPUにおける推論遅延やトークン生成速度の改善と解釈してはならない。

- **2023-07 · [PUMA: Secure Inference of LLaMA-7B in Five Minutes](2023-2307.12533-puma-secure-inference-of-llama-7b-in-five-minutes.md)**  
  実装：[✓](https://github.com/secretflow/spu/tree/main/examples/python/ml/flax_llama7b) ・ リポジトリ内被引用：4  
  従来の高速化方式が必要としたモデルの再学習や構造変更を避け、既存の学習済み重みをほぼそのまま秘密計算へ持ち込むことを狙う。

- **2023-01 · [Alternating Updates for Efficient Transformers](2023-2301.13310-alternating-updates-for-efficient-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  AltUp（Alternating Updates）は、表現の幅と層内部の演算幅を分離し、幅Kdの状態を保持しながら各層で実際にTransformerを通すのはd次元の部分ブロック一つに限る方式である。NeurIPS 2023採択論文のT5実験では、同じ予測精度を持つ密なTransformerに対して最大87%の相対速度向上を報告する。

- **2023-07 · [A Survey of Techniques for Optimizing Transformer Inference](2023-2307.07982-a-survey-of-techniques-for-optimizing-transformer-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  本論文は、Transformer推論を軽量化・高速化する手法を、モデルを作り直す方法から演算器の設計まで横断的に整理した43ページの文献調査である。例えばCoFiは引用元研究で約95%の疎性と約10倍の高速化を報告し、HMC-TranはV100のテンソルコアを利用するBERT-baseの92%疎性で3.68倍を報告する。

- **2022-12 · [Linearizing Transformer with Key-Value Memory](2022-2203.12644-linearizing-transformer-with-key-value-memory.md)**  
  実装：[✓](https://github.com/jcyk/memsizer) ・ リポジトリ内被引用：2  
  MemSizerはこの問題を、既存モデルのKVキャッシュだけを圧縮するのではなく、注意層そのものを別の演算へ置換して解く。一方、同じ比較の生成速度は3165対1932トークン/秒、メモリは3.373対19.21GBである。

- **2023-07 · [Beyond Classical Attention: Quantum Attention for Scalable Computation](2023-2307.08045-beyond-classical-attention-quantum-attention-for-scalable-computation.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文は、長い入力系列に対する自己注意で全ての問い合わせと鍵の内積を計算する代わりに、閾値を超える少数の大きな内積だけを量子探索で発見する理論的な方法を提案する。

- **2023-06 · [Modular Transformers: Compressing Transformers into Modularized Layers for Flexible Efficient Inference](2023-2306.02379-modular-transformers-compressing-transformers-into-modularized-layers-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文の主題は、圧縮済みモデルを一種類だけ作るのではなく、一度の圧縮学習から異なる実行時予算に対応できる層構成を取り出すことである。

- **2023-05 · [SmartTrim: Adaptive Tokens and Attention Pruning for Efficient Vision-Language Models](2023-2305.15033-smarttrim-adaptive-tokens-and-attention-pruning-for-efficient-vision-lan.md)**  
  実装：[✓](https://github.com/kugwzk/SmartTrim) ・ リポジトリ内被引用：1  
  すべての入力に同じ割合でトークンを削る静的枝刈りは、簡単な入力では計算を無駄に残し、難しい入力では必要な情報まで失う可能性がある。METERのVQAでは、元モデルの77.43%・88.5 GFLOPsに対して、約2倍の計算量削減設定で77.13%・46.0 GFLOPsを報告する。

- **2023-05 · [Revisiting Offline Compression: Going Beyond Factorization-based Methods for Transformer Language Models](2023-2302.04045-revisiting-offline-compression-going-beyond-factorization-based-methods-.md)**  
  実装：[✓](https://github.com/MohammadrezaBanaei/auto-encoder-based-transformer-compression) ・ リポジトリ内被引用：1  
  本研究は、既に学習されたTransformerの重み行列を、事前学習モデル全体の再訓練や蒸留を行わずに小さくする「オフライン圧縮」を対象とする。

- **2023-07 · [Scaling In-Context Demonstrations with Structured Attention](2023-2307.02690-scaling-in-context-demonstrations-with-structured-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  例示数を増やせば精度が改善する可能性があるが、全ての例示を連結して密な自己注意を実行すると、系列長の二乗に比例する演算量とメモリが必要になる。SAICL（Structured 注意機構 for In-Context Learning）は、例示どうしの直接注意を取り除き、テスト入力を情報集約のハブにする。

- **2023-07 · [Efficient Latent Space Compression for Lightning-Fast Fine-Tuning and Inference of Transformer-Based Models](2023-400218b723db-efficient-latent-space-compression-for-lightning-fast-fine-tuning-and-in.md)**  
  実装：[✓](https://github.com/AlaFalaki/compressedBART) ・ リポジトリ内被引用：0  
  本論文は、既存のTransformer 符号化器が出力する各トークンの隠れ表現を、別途学習した自己符号化器（AE）で低次元に写像し、その低次元表現を入力として処理できる小型復号器を構築する手法を検討する。これは約2.2倍の速度、時間比で約54%の短縮に相当する。

- **2023-07 · [DPBERT: Efficient Inference for BERT based on Dynamic Planning](2023-2308.00108-dpbert-efficient-inference-for-bert-based-on-dynamic-planning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DPBERTは、BERT-baseの12個のTransformer層をすべて通すのではなく、入力ごとに実行すべき層の部分列を決めることで推論遅延を削減する。従来のearly exitでは、途中の層で最終分類を確定すると、それより上の層をまとめて省略する。そのため下位・中間層を残したまま上位だけを削る選択に限定される。

- **2023-07 · [CA-LoRA: Adapting Existing LoRA for Compressed LLMs to Enable Efficient Multi-Tasking on Personal Devices](2023-2307.07705-ca-lora-adapting-existing-lora-for-compressed-llms-to-enable-efficient-m.md)**  
  実装：[✓](https://github.com/thunlp/CA-LoRA) ・ リポジトリ内被引用：0  
  CA-LoRAは非圧縮LLM上で学習済みのLoRAを圧縮モデルへ移植する際、元LoRAを初期値として継承し、非線形低ランクの回復モジュールを加え、非圧縮モデル＋LoRAを教師として蒸留する。T5-3Bを量子化・枝刈り・MoEficationで5.61GBから0.94GBへ圧縮した実験では、RTEが通常LoRAの82.9%からCA-LoRAの84.3%へ改善。

- **2023-06 · [A Probabilistic Framework for Pruning Transformers Via a Finite Admixture of Keys](2023-dc4a5089a5f8-a-probabilistic-framework-for-pruning-transformers-via-a-finite-admixtur.md)**  
  実装：[✓](https://github.com/Fsoft-AIC/FiAKFormer) ・ リポジトリ内被引用：0  
  本研究は、Transformerの自己注意を確率的な混合モデルとして解釈し、学習可能なkeyの事前重みを使って冗長な注意スコアとkey/valueを枝刈りする方式「Finite Admixture of Keys（FiAK）」を提案する。

- **2023-05 · [Infor-Coef: Information Bottleneck-based Dynamic Token Downsampling for Compact and Efficient language model](2023-2305.12458-infor-coef-information-bottleneck-based-dynamic-token-downsampling-for-c.md)**  
  実装：[✓](https://github.com/twwwwx/Infor-Coef) ・ リポジトリ内被引用：0  
  Infor-Coefが扱うのは、BERTのモデル重みを固定比率で減らすだけでは、簡単な入力と難しい入力に同じ計算を割り当てるという問題である。BERT-base比で16.2倍という原著の代表値は、バッチ内最大長へpaddingしたときの推定FLOPs比である。

- **2023-02 · [Auto-Parallelizing Large Models with Rhino: A Systematic Approach on Production AI Platform](2023-2302.08141-auto-parallelizing-large-models-with-rhino-a-systematic-approach-on-prod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Rhinoは、単一デバイス向けに記述されたテンソル計算を、複数GPUへ自動分散する学習システムである。評価では、V100 32GBと100Gb RoCEのクラスタでGPTとGShard MoEを最大16GPUまで実行し、Alpa、Megatron/DeepSpeedと比較した。

- **2023-01 · [AttMemo: Accelerating Self-Attention with Memoization on Big Memory Systems](2023-2301.09262-attmemo-accelerating-self-attention-with-memoization-on-big-memory-syste.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Transformerの自己注意（self-注意機構）は、入力系列内のトークン間関係を行列として計算する。BERT、RoBERTa、DeBERTa、GPT-2（いずれも約1億パラメータ）を48コアのXeon CPUとDRAM/Optaneの合計最大1.6TBメモリで測定し、著者は平均22%、最大68%の推論速度向上を報告する。

- **2022-11 · [DBA: Efficient Transformer With Dynamic Bilinear Low-Rank Attention](2022-2211.16368-dba-efficient-transformer-with-dynamic-bilinear-low-rank-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DBA（動的 Bilinear Low-Rank 注意機構）は、通常のTransformer注意計算における系列長nと特徴次元dの二つの大きさを同時に小さくする方式である。長さ4,096のbyte-level text分類では通常Transformerに対する相対速度6.1倍、ピークメモリ比0.09を報告する。

- **2022-11 · [AAN+: Generalized Average Attention Network for Accelerating Neural Transformer](2022-ffa88b154f4f-aan-generalized-average-attention-network-for-accelerating-neural-transf.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AAN+は、履歴を位置別・内容別の正のスコアで加重平均したベクトルへ圧縮し、ゲートで現在トークンと混ぜる。WMT14英独翻訳では、通常TransformerのBLEU 27.59に対しNerは27.56とほぼ同等で、デコード速度は1.30倍、学習速度は1.02倍となる。

### 5年前（2021-11〜2022-10）

- **2022-06 · [DeepSpeed Inference: Enabling Efficient Inference of Transformer Models at Unprecedented Scale](2022-2207.00032-deepspeed-inference-enabling-efficient-inference-of-transformer-models-at-unprecedented-scale.md)**  
  実装：[✓](https://github.com/microsoft/DeepSpeed) ・ リポジトリ内被引用：174  
  単一の量子化方式や一種類の並列化を万能解とせず、GPU内実行向けのDeepSpeed Transformerと、CPU主記憶・NVMeを使うZeRO-Inferenceという二つの経路を組み合わせる。

- **2022-02 · [ST-MoE: Designing Stable and Transferable Sparse Expert Models](2022-2202.08906-st-moe-designing-stable-and-transferable-sparse-expert-models.md)**  
  実装：[✓](https://github.com/tensorflow/mesh/blob/master/mesh_tensorflow/transformer/moe.py) ・ リポジトリ内被引用：73  
  ST-MoEは専門家混合（Mixture-of-Experts、MoE）モデルを単に巨大化するのではなく、学習の発散を防ぎ、下流の多様な自然言語課題で密モデルを上回るための設計を検討する研究である。ただしこれはモデル全体をGPUメモリ12GBで動かせるという意味ではなく、専門家の重み配置と分散通信を含めた大規模学習システムの研究である。

- **2021-12 · [Self-attention Does Not Need O(n^2) Memory](2021-2112.05682-self-attention-does-not-need-o-n-2-memory.md)**  
  実装：[✓](https://github.com/google-research/google-research/tree/master/memory_efficient_attention) ・ リポジトリ内被引用：32  
  ソフトマックス注意の最大値、指数和、値の重み付き和を逐次更新し、全注意行列を実体化せず同じ数学的出力を得る。理論上の省メモリ算法と、TPU向けのチャンク並列実装、再計算を使った微分を示す。

- **2022-07 · [FNet: Mixing Tokens with Fourier Transforms](2022-2105.03824-fnet-mixing-tokens-with-fourier-transforms.md)**  
  実装：[✓](https://github.com/google-research/google-research/tree/master/f_net) ・ リポジトリ内被引用：17  
  標準的な変換器（Transformer）の自己注意（self-注意機構）は、入力系列内のトークン間の重みを入力内容に応じて計算する。特にこの論文の「学習80%高速化」は約1.8倍の処理速度を意味し、処理時間が80%減ったという意味ではない。

- **2022-02 · [Competition-Level Code Generation with AlphaCode](2022-2203.07814-competition-level-code-generation-with-alphacode.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  AlphaCodeは、自然言語で与えられた競技プログラミング問題から、正しい実行プログラムを見つけるための生成・探索・選別システムである。評価では2021年12月のCodeforcesの10大会を後から模擬し、各問題最大10提出という条件で、参加者中の順位が平均して上位54.3%に相当した。

- **2022-05 · [A Simple Hash-Based Early Exiting Approach For Language Understanding and Generation](2022-219d2c1fa7a8-a-simple-hash-based-early-exiting-approach-for-language-understanding-an.md)**  
  実装：[✓](https://github.com/txsun1997/HashEE) ・ リポジトリ内被引用：7  
  前者は回帰や生成へそのまま転用しにくく、後者は未知入力に対する難度予測が難しい。難度を精密に当てることより、似た語彙が学習時と推論時に同じ計算経路を通る一貫性を重視する設計である。

- **2022-04 · [Step-unrolled Denoising Autoencoders for Text Generation](2022-2112.06749-step-unrolled-denoising-autoencoders-for-text-generation.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  大規模言語モデルの典型的な自己回帰生成は、先行トークンが確定してから次トークンを計算する。注意演算の内部を高速化しても、長い出力を作るにはトークン数にほぼ比例した生成ステップが必要になる。最初はランダムなトークン列を用意し、各反復で全体の整合性を改善して最終文を得る。しかし生成中のモデルが自分で作った中間文は、人工的なランダム破損文と同じ分布ではない。

- **2022-08 · [Unified Normalization for Accelerating and Stabilizing Transformers](2022-2208.01313-unified-normalization-for-accelerating-and-stabilizing-transformers.md)**  
  実装：[✓](https://github.com/hikvision-research/Unified-Normalization) ・ リポジトリ内被引用：2  
  UNはTransformerのオフライン 正規化を、活性値/勾配統計の平滑化と適応型 外れ値除去で安定化し、固定統計を線形層へ融合してSwin-Tで31.2% スループット向上を示す。

- **2022-01 · [Latency Adjustable Transformer Encoder for Language Understanding](2022-2201.03327-latency-adjustable-transformer-encoder-for-language-understanding.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Transformerの推論では、すべての入力トークンに対して各層の注意機構とFFNを実行する。

- **2022-01 · [Fast Monte-Carlo Approximation of the Attention Mechanism](2022-2201.12854-fast-monte-carlo-approximation-of-the-attention-mechanism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Transformerの注意機構では、各入力位置が他の位置へどれだけ注意を向けるかを表す重みを計算し、その重みに基づいて値ベクトルを集約する。BERT、DistilBERT、Longformerに適用した実験では、GLUEの分類・類似度評価で精度をおおむね維持しつつ注意演算の計算量を大幅に減らせると報告する。

- **2021-12 · [DAP-BERT: Differentiable Architecture Pruning of BERT](2021-0028045aea9f-dap-bert-differentiable-architecture-pruning-of-bert.md)**  
  実装：[✓](https://github.com/OscarYau525/DAP-BERT) ・ リポジトリ内被引用：0  
  DAP-BERTは、既存のBERTモデルから、実行装置の演算制約に応じて不要な注意ヘッドとFeed-順伝播 Network（FFN）の中間次元を選択的に除去する、微分可能な構造化枝刈り方式である。

- **2021-11 · [SimpleTRON: Simple Transformer with O(N) Complexity](2021-2111.15588-simpletron-simple-transformer-with-o-n-complexity.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Transformerの標準自己注意は、系列長L、各ヘッド次元dに対してQKᵀのL×L行列を作り、その各行をsoftmax正規化してVと掛ける。これにより過去の各位置との類似度を直接計算できるが、系列長に対して時間・中間注意行列のサイズが二乗で増える。各ヘッドについて、標準のsoftmax(QKᵀ/√d)Vを、Q(KᵀV)/√Lに置き換える。

### 6年前（2020-11〜2021-10）

- **2021-04 · [Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM](2021-2104.04473-efficient-large-scale-language-model-training-on-gpu-clusters-using-mega.md)**  
  実装：[✓](https://github.com/NVIDIA/Megatron-LM) ・ リポジトリ内被引用：81  
  本論文は、巨大言語モデルの学習を数千基のGPUへ拡張するとき、メモリ容量、層内の集合通信、パイプラインの空泡、ノード間転送の重複が性能を制限する問題を扱う。パイプラインでは前向きと後向きを交互に処理する1F1Bを使い、さらに一つのGPUに複数の離れたモデル片を割り当てて空泡を短くする。

- **2021-02 · [Nyströmformer: A Nyström-Based Algorithm for Approximating Self-Attention](2021-2102.03902-nystr-mformer-a-nystr-m-based-algorithm-for-approximating-self-attention.md)**  
  実装：[✓](https://github.com/mlpen/Nystromformer) ・ リポジトリ内被引用：39  
  標準的な自己注意（self-注意機構）は、系列長nのすべてのトークン対の類似度を計算するため、n×nの注意行列を作る。系列が2倍になると注意行列の要素数は4倍となり、長い文書を扱うTransformerでは計算量とメモリ容量が問題になる。

- **2020-12 · [Fast Transformers with Clustered Attention](2020-2007.04825-fast-transformers-with-clustered-attention.md)**  
  実装：[✓](https://github.com/idiap/fast-transformers) ・ リポジトリ内被引用：21  
  本論文は、自己注意（self-注意機構）の各クエリがすべてのキーを参照するため、系列長Nに対して注意行列がN×Nになり、計算量と中間メモリが二乗で増える問題を扱う。NeurIPS 2020の正式版では、GTX 1080 Ti 11GB上の音声認識2データセットと、学習済みRoBERTaのGLUE・SQuADへの適用を評価した。

- **2021-10 · [8-bit Optimizers via Block-wise Quantization](2021-2110.02861-8-bit-optimizers-via-block-wise-quantization.md)**  
  実装：[✓](https://github.com/bitsandbytes-foundation/bitsandbytes) ・ リポジトリ内被引用：17  
  Dettmersらは、この状態を8ビットへ縮めても32ビット版に近い学習品質を維持する方式を提案した。原著表1では1.5Bパラメータ言語モデルで32ビットAdamと8ビットAdamの困惑度がともに9.0で、後者は8.5GBのGPUメモリを節約した。

- **2020-12 · [MiniLMv2: Multi-Head Self-Attention Relation Distillation for Compressing Pretrained Transformers](2020-2012.15828-minilmv2-multi-head-self-attention-relation-distillation-for-compressing.md)**  
  実装：[✓](https://github.com/microsoft/unilm/tree/master/minilm) ・ リポジトリ内被引用：15  
  教師と生徒の注意頭数を揃える制約を外し、Query・Key・Valueのトークン間関係を共通の「関係頭」で比較する。推論速度の改善は蒸留後の小型モデルによるもので、実行時に教師を参照する方式ではない。

- **2021-03 · [Softermax: Hardware/Software Co-Design of an Efficient Softmax for Transformers](2021-2103.09301-softermax-hardware-software-co-design-of-an-efficient-softmax-for-transf.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  Transformerの自己注意機構では、クエリとキーの積から得た各スコアをsoftmaxで正規化し、値ベクトルへの重みを生成する。原著のTSMC 7nm設計評価では、非正規化部の面積0.25倍・エネルギー0.10倍、正規化部の面積0.65倍・エネルギー0.39倍、MAC等を含む演算器全体の面積0.90倍・エネルギー0.43倍を報告する。

### 7年前（2019-11〜2020-10）

- **2020-02 · [Compressing Large-Scale Transformer-Based Models: A Case Study on BERT](2020-2002.11985-compressing-large-scale-transformer-based-models-a-case-study-on-bert.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  量子化で重みを小さくする方法、不要な重みや構造を削る方法、大きな教師モデルから小さな生徒モデルへ知識を移す方法など、圧縮の選択肢は多い。

- **2020-04 · [Lite Transformer with Long-Short Range Attention](2020-2004.11886-lite-transformer-with-long-short-range-attention.md)**  
  実装：[✓](https://github.com/mit-han-lab/lite-transformer) ・ リポジトリ内被引用：9  
  Lite Transformerは、短い文章を処理する翻訳・要約・言語モデルを、限られた計算予算の端末で実行するためのモデル構造を提案したICLR 2020論文である。

- **2020-07 · [FTRANS: Energy-Efficient Acceleration of Transformers using FPGA](2020-2007.08563-ftrans-energy-efficient-acceleration-of-transformers-using-fpga.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  FTRANSは、Transformerの重み行列を拡張ブロック循環行列（enhanced block-circulant matrix; BCM）に置き換える構造化圧縮と、その圧縮表現を直接計算する再構成可能論理回路（field-programmable gate array; FPGA）の専用構成を同時設計した研究である。

- **2020-06 · [Funnel-Transformer: Filtering out Sequential Redundancy for Efficient Language Processing](2020-2006.03236-funnel-transformer-filtering-out-sequential-redundancy-for-efficient-lan.md)**  
  実装：[✓](https://github.com/laiguokun/Funnel-Transformer) ・ リポジトリ内被引用：7  
  Funnel-Transformerは、すべての変換器層で入力トークン数と同じ長さの隠れ状態を維持することが、系列全体を一つの表現へ要約する分類・ランキング課題では冗長であるという着想から生まれた。これにより、出力長は短くしながら圧縮前の情報全体を参照できる。

- **2020-05 · [IntelliCode Compose: Code Generation using Transformer](2020-2005.08025-intellicode-compose-code-generation-using-transformer.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  IntelliCode Composeは、統合開発環境（IDE）で入力途中のプログラムから一行規模の補完候補を提示するクラウド型のコード生成システムである。ただし編集類似度は84.1%から78.0%へ下がる。

- **2019-11 · [Mask-Predict: Parallel Decoding of Conditional Masked Language Models](2019-0bc18ef37a7d-mask-predict-parallel-decoding-of-conditional-masked-language-models.md)**  
  実装：[✓](https://github.com/facebookresearch/Mask-Predict) ・ リポジトリ内被引用：7  
  翻訳文全体を毎回捨てる反復改良方式とは異なり、高信頼の語を固定して低信頼位置へ文脈を提供する点が中心的な設計である。

- **2020-06 · [Multi-Head Attention: Collaborate Instead of Concatenate](2020-2006.16362-multi-head-attention-collaborate-instead-of-concatenate.md)**  
  実装：[✓](https://github.com/epfml/collaborative-attention) ・ リポジトリ内被引用：6  
  標準的な多頭注意（Multi-Head 注意機構、MHA）は、複数の注意ヘッドに独立したクエリ射影とキー射影を与え、それぞれが計算した値を連結して出力する。単層のV100測定では設定次第で推論時間が2.28ミリ秒から1.75ミリ秒へ短縮した。

- **2020-06 · [$O(n)$ Connections are Expressive Enough: Universal Approximability of Sparse Transformers](2020-2006.04862-o-n-connections-are-expressive-enough-universal-approximability-of-spars.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  通常のTransformerの自己注意は、系列中の各トークンが他の全トークンを参照するため、系列長nに対して注意得点の組合せがnの二乗で増える。長文を処理する際に接続を減らす疎注意は計算量を減らす候補だが、接続を取り除くことでモデルが表現できる関数の種類まで狭まるのかは自明ではない。

- **2020-09 · [Efficient Sparse Collective Communication and its application to Accelerate Distributed Deep Learning](2020-e4ac6d84ba9c-efficient-sparse-collective-communication-and-its-application-to-acceler.md)**  
  実装：[✓](https://github.com/sands-lab/omnireduce) ・ リポジトリ内被引用：2  
  この集団通信（collective 通信）は計算機を増やすほど相対的に重くなり、特に多数の埋め込み表を持つモデルではゼロ要素の転送が無駄になる。各ワーカーが次の非ゼロブロックの位置を通知するため、集約器は全ワーカーの進行を調整し、誰も値を持たない領域を安全に飛ばせる。

- **2020-08 · [ConvBERT: Improving BERT with Span-based Dynamic Convolution](2020-2008.02496-convbert-improving-bert-with-span-based-dynamic-convolution.md)**  
  実装：[✓](https://github.com/yitu-opensource/ConvBert) ・ リポジトリ内被引用：0  
  BERTの多頭自己注意は、すべてのヘッドで全トークン対の関係を計算する。しかし自然言語では局所的な構文・語彙の結び付きが重要であり、実際に多くのヘッドの注意行列は対角線付近へ集中する。遠方トークンをほとんど参照しないヘッドでも、全系列の二次元注意行列を構築するのは計算上の無駄である。

### 8年前（2018-11〜2019-10）

- **2019-09 · [Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism](2019-1909.08053-megatron-lm-training-multi-billion-parameter-language-models-using-model.md)**  
  実装：[✓](https://github.com/NVIDIA/Megatron-LM) ・ リポジトリ内被引用：325  
  この論文の対象は、巨大な言語モデルの学習時に、モデル重み・勾配・最適化器状態が単一GPUのメモリに収まらない問題である。従来のモデル全体を別の言語や専用コンパイラで書き直す方法とは異なり、PyTorchの既存Transformer実装へ少数の集約通信を挿入する設計である。

- **2019-04 · [Generating Long Sequences with Sparse Transformers](2019-1904.10509-generating-long-sequences-with-sparse-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：257  
  全結合の自己注意を局所窓と周期・固定要約位置へ因数分解して O(n√n) 化し、再計算と疎GPUカーネルを併用して数万〜100万要素の生成を可能にしたSparse Transformer。

- **2018-11 · [Blockwise Parallel Decoding for Deep Autoregressive Models](2018-1811.03115-blockwise-parallel-decoding-for-deep-autoregressive-models.md)**  
  実装：[✓](https://github.com/tensorflow/tensor2tensor) ・ リポジトリ内被引用：126  
  計算器に並列能力があっても、この依存関係が生成遅延を制限する。最大 $k$ 個の候補を同時に提案し、基準モデルで候補列を並列採点して、基準モデルの貪欲選択と一致する先頭からの連続部分だけを採用する。後年の投機的復号（投機的復号）と同じく、安い予測の正しさを基準モデルで検証するという基本構造を明示した初期研究である。

- **2018-11 · [GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism](2018-1811.06965-gpipe-efficient-training-of-giant-neural-networks-using-pipeline-paralle.md)**  
  実装：[✓](https://github.com/tensorflow/lingvo/blob/master/lingvo/core/gpipe.py) ・ リポジトリ内被引用：85  
  GPipeは、単一のGPUやTPUに収まらないニューラルネットワークを、層の連続区間ごとに複数の装置へ分割して学習する方式である。実際に学習した557百万パラメータのAmoebaNetはImageNet-2012の上位1件正解率84.4%、60億パラメータ・128層の多言語Transformerは102言語対で個別の二言語モデルを上回った。

- **2019-09 · [Q-BERT: Hessian Based Ultra Low Precision Quantization of BERT](2019-1909.05840-q-bert-hessian-based-ultra-low-precision-quantization-of-bert.md)**  
  実装：✓ ・ リポジトリ内被引用：69  
  Q-BERTは、BERTの各層へ同じビット数を割り当てる均一量子化ではなく、損失関数の二階微分から層ごとの誤差感度を推定し、敏感な層へ高い精度を残す混合精度量子化手法である。論文はSST-2、MNLI、CoNLL-03、SQuADの四課題で、重みの最大13倍圧縮、埋め込みと活性値の最大4倍圧縮を報告し、強圧縮でも性能低下を最大2.3%以内に抑えたと説明する。

- **2019-05 · [Adaptive Attention Span in Transformers](2019-1905.07799-adaptive-attention-span-in-transformers.md)**  
  実装：[✓](https://github.com/facebookresearch/adaptive-span) ・ リポジトリ内被引用：33  
  自己回帰型Transformerの注意機構は、過去の一定幅のトークンを参照して次のトークンを予測する。

- **2019-10 · [Q8BERT: Quantized 8Bit BERT](2019-1910.06188-q8bert-quantized-8bit-bert.md)**  
  実装：[✓](https://github.com/NervanaSystems/nlp-architect) ・ リポジトリ内被引用：18  
  Q8BERTは、事前学習済みBERTを特定の自然言語処理課題へ微調整する段階で量子化誤差を模擬し、推論時の8ビット整数演算へ適応させる研究である。著者はBERTの重みの99%以上を占める埋め込み層と全結合層を8ビット整数へ対応させ、残りの数値的に敏感な演算は32ビット浮動小数点に残す。

- **2019-04 · [Mask-Predict: Parallel Decoding of Conditional Masked Language Models](2019-1904.09324-mask-predict-parallel-decoding-of-conditional-masked-language-models.md)**  
  実装：[✓](https://github.com/facebookresearch/Mask-Predict) ・ リポジトリ内被引用：16  
  翻訳文の長さを最初に予測し、最初の反復では全位置を同時に予測する。2019年の機械翻訳実験では、WMT14英語→ドイツ語において基礎CMLMの10反復が27.03 BLEU、同等規模の自己回帰Transformerが27.74 BLEUとなった。

- **2019-07 · [Large Memory Layers with Product Keys](2019-1907.05242-large-memory-layers-with-product-keys.md)**  
  実装：[✓](https://github.com/facebookresearch/XLM) ・ リポジトリ内被引用：13  
  本論文の積キー記憶層（Product Key メモリ; PKM）は、二つの部分キー集合の直積で巨大なキー集合を暗黙的に作り、各部分集合の上位候補だけを調べて全積キー集合に対する正確な上位選択を行う。検索結果に対応する少数の値ベクトルだけを読み出して加重和を計算するため、総パラメータ容量と活性計算量を分離できる。

- **2019-03 · [Supporting Very Large Models using Automatic Dataflow Graph Partitioning](2019-1807.08887-supporting-very-large-models-using-automatic-dataflow-graph-partitioning.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  Tofuは、単一のGPUのメモリ容量を超えるニューラルネットワークを、プログラムを書き換えず複数GPUで学習できるようにする自動モデル並列化システムである。

### 9年前（2017-11〜2018-10）

- **2018-06 · [PipeDream: Generalized Pipeline Parallelism for DNN Training](2018-1806.03377-pipedream-generalized-pipeline-parallelism-for-dnn-training.md)**  
  実装：✓ ・ リポジトリ内被引用：84  
  DNNの連続層を複数GPUへ割り当て、異なるミニバッチの順伝播と逆伝播を交互に重ねる。層の計算・通信費用を測って段を自動分割し、順伝播時の重み版を逆伝播まで保持することで非同期実行の整合性を保つ。

- **2018-02 · [Horovod: fast and easy distributed deep learning in TensorFlow](2018-1802.05799-horovod-fast-and-easy-distributed-deep-learning-in-tensorflow.md)**  
  実装：[✓](https://github.com/uber/horovod) ・ リポジトリ内被引用：20  
  GPU数を増やすと勾配転送と集約のために通信が集中し、著者らの128 GPU試験では、計算資源のほぼ半分を効率的に使えていなかった。提案の価値は通信アルゴリズムだけではない。

- **2018-02 · [Deterministic Non-Autoregressive Neural Sequence Modeling by Iterative Refinement](2018-1802.06901-deterministic-non-autoregressive-neural-sequence-modeling-by-iterative-r.md)**  
  実装：[✓](https://github.com/nyu-dl/dl4mt-nonauto) ・ リポジトリ内被引用：17  
  本研究は、出力系列を左から右へ一語ずつ生成する自己回帰モデルの逐次依存を取り除き、系列全体を同時に予測した後、少数回の反復で文章を修正する決定論的な非自己回帰系列生成法を提案する。

### 10年前（2016-11〜2017-10）

- **2017-01 · [Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](2017-1701.06538-outrageously-large-neural-networks-the-sparsely-gated-mixture-of-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：305  
  本論文は、ニューラルネットワークの総パラメータ数を増やすと各入力での計算量も増えるという密なモデルの制約を、入力ごとに一部の専門家だけを実行する条件付き計算によって緩和した基礎研究である。モデルの総容量を大きくしても、活性化する専門家数を固定すれば入力一件あたりの専門家演算量はほぼ一定にできる。ただし専門家を増やすだけでは高速にならない。

### 11年前（2015-11〜2016-10）

- **2016-06 · [Compression of Neural Machine Translation Models via Pruning](2016-1606.09274-compression-of-neural-machine-translation-models-via-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  この論文は、注意機構付きの長短期記憶（LSTM）を使うニューラル機械翻訳器について、どの重みを消せば翻訳品質を損なわずに保存パラメータを減らせるかを実験した2016年の研究である。種類非依存枝刈りでは、40%の重みを消しても再学習前の品質劣化は小さく、さらに80%を消した後に残存重みだけを4エポック再学習すると20.91 BLEUまで回復した。
<!-- survey:auto:end -->
