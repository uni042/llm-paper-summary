# Conditional Computation

入力やtokenの難しさに応じて、**実行するlayer数、処理するtoken数、終了位置などを変え、不要な計算を最初から行わない**研究をまとめる。全tokenが全layerを必ず通る通常の実行を崩し、layer skipping、early exit、token pruningなどで計算量を減らす。

MoEのexpert数を変えるAdaptive Expert Computationとは対象が異なり、この系統では主にTransformer本体の実行深度や処理対象tokenを動的に変える。

<!-- survey:auto:start -->
## 自動生成の論文一覧（254本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/04-conditional-computation/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-12〜2026-11**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-12〜2026-11）

- **2026-02 · [FlashVID: Efficient Video Large Language Models via Training-free Tree-based Spatiotemporal Token Merging](2026-2602.08024-flashvid-efficient-video-large-language-models-via-training-free-tree-ba.md)**  
  実装：[✓](https://github.com/Fanziyang-v/FlashVID) ・ リポジトリ内被引用：13  
  入力フレームが増えるとトークン列が長くなり、注意機構だけでなく全結合層の計算、鍵値キャッシュ、初回応答までの時間が増える。LLaVA-OneVisionでは、視覚トークンを10%まで減らしても四つの主要評価群の平均点58.4から57.9へと小幅な低下にとどまり、元精度の99.1%を維持した。

- **2026-02 · [HiDrop: Hierarchical Vision Token Reduction in MLLMs via Late Injection, Concave Pyramid Pruning, and Early Exit](2026-2602.23699-hidrop-hierarchical-vision-token-reduction-in-mllms-via-late-injection-c.md)**  
  実装：[✓](https://github.com/EIT-NLP/HiDrop) ・ リポジトリ内被引用：12  
  LLaVA型の画像言語モデルは、画像符号化器が出力した多数の視覚特徴を言語モデルの入力列へ結合する。この前提では、視覚情報の統合が実際に行われる層と計算資源を費やす層が一致しない。

- **2026-02 · [OmniSIFT: Modality-Asymmetric Token Compression for Efficient Omni-modal Large Language Models](2026-2602.04804-omnisift-modality-asymmetric-token-compression-for-efficient-omni-modal-.md)**  
  実装：[✓](https://github.com/dingyue772/OmniSIFT) ・ リポジトリ内被引用：11  
  動画と音声を同時に受け取る統合マルチモーダル大規模言語モデルでは、視覚エンコーダと音声エンコーダが生成したトークンを時間順に並べ、言語モデルへ渡す。著者らは20秒のクリップでも2万を超える入力トークンが生じ得ることを問題設定に挙げる。

- **2026-02 · [ApET: Approximation-Error Guided Token Compression for Efficient VLMs](2026-2602.19870-apet-approximation-error-guided-token-compression-for-efficient-vlms.md)**  
  実装：[✓](https://github.com/MaQianKun0/ApET) ・ リポジトリ内被引用：9  
  視覚トークンの重要度を注意ではなく線形再構成の誤差で測って圧縮する学習不要の方式で、約9割のトークン削減でも性能をほぼ保ち、高速注意カーネルとも併用できる。

- **2026-04 · [Why and When Visual Token Pruning Fails? A Study on Relevant Visual Information Shift in MLLMs Decoding](2026-2604.12358-why-and-when-visual-token-pruning-fails-a-study-on-relevant-visual-infor.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  そのうえで、生成中の注意分布が初期状態から変化した時だけ、退避しておいた視覚トークンを選び直す生成段階移動対応トークン削減（デコード-stage Shift-aware トークン 枝刈り; DSTP）を提案する。

- **2026-03 · [AgilePruner: An Empirical Study of Attention and Diversity for Adaptive Visual Token Pruning in Large Vision-Language Models](2026-2603.01236-agilepruner-an-empirical-study-of-attention-and-diversity-for-adaptive-v.md)**  
  実装：[✓](https://github.com/cvsp-lab/AgilePruner) ・ リポジトリ内被引用：7  
  従来の注意重視方式は画像符号化器のクラス・トークンが強く注目する領域を残す。LLaVA-1.5-7B、TextVQA、RTX 4090の単一GPU評価で、64個を残す設定は576個を残す基準に対して推論計算量3.14→0.48兆FLOPs、1画像遅延172→115 ms、GPUメモリ13.60→13.30 GBとなった。

- **2026-04 · [LearnPruner: Rethinking Attention-based Token Pruning in Vision Language Models](2026-2604.23950-learnpruner-rethinking-attention-based-token-pruning-in-vision-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  LLaVA-v1.5では1画像576トークン、LLaVA-NeXTの高解像度入力では最大2,880トークンとなり、画像の背景や類似領域にも長い系列を割り当てる。LLaVA-v1.5-7Bの8課題では、視覚トークンを平均576個から32個へ削減しても、元モデルを100%とした平均相対性能94.8%を維持した。

- **2026-03 · [DASH: Dynamic Audio-Driven Semantic Chunking for Efficient Omnimodal Token Compression](2026-2603.15685-dash-dynamic-audio-driven-semantic-chunking-for-efficient-omnimodal-toke.md)**  
  実装：[✓](https://github.com/laychou666/DASH) ・ リポジトリ内被引用：5  
  LLMへ渡す前の入力列が長くなると、プリフィル（プリフィル）の注意演算とKVキャッシュのメモリ消費が増える。DASH（動的 Audio-driven Semantic cHunking）は、音声埋め込みの隣接トークンの変化を意味境界の手掛かりにし、音声と映像を可変長の区間へ分ける学習不要の圧縮方式である。

- **2026-08 · [Depth-adaptive Inference of Looped Language Models via Continuous Depth Batching](2026-2608.09444-depth-adaptive-inference-of-looped-language-models-via-continuous-depth-.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  論文はCDBを端から端まで実装し、深度が不揃いになる鍵値キャッシュ（KV キャッシュ）、CPU側スケジューラとGPU側反復の同期、前段・後段をどの頻度で実行するかまで扱う。

- **2026-04 · [HAWK: Head Importance-Aware Visual Token Pruning in Multimodal Models](2026-2604.07812-hawk-head-importance-aware-visual-token-pruning-in-multimodal-models.md)**  
  実装：[✓](https://github.com/peppery77/HAWK) ・ リポジトリ内被引用：4  
  画像の解像度や動画のフレーム数が増えると、入力長、注意計算、キー・値キャッシュの負荷が増える。視覚トークンを削減する既存方式には、画像特徴の類似性や注意得点で残すトークンを選ぶものがあるが、注意ヘッドを単純平均すると、画像理解に重要なヘッドとそうでないヘッドを同等に扱ってしまう。

- **2026-03 · [The Model Knows Which Tokens Matter: Automatic Token Selection via Noise Gating](2026-2603.07135-the-model-knows-which-tokens-matter-automatic-token-selection-via-noise-.md)**  
  実装：[✓](https://github.com/MedHK23/AutoSelect) ・ リポジトリ内被引用：4  
  重要度の低いトークンを削除する既存手法は、注意重み、類似度、固定削減比などの代理指標を使うことが多く、最終回答に必要な情報を最適に残せるとは限らない。LLaVA-1.5-7Bの576視覚トークンを64個へ削減した条件で、10ベンチマークの平均性能維持率96.5%を報告する。

- **2026-02 · [EntropyPrune: Matrix Entropy Guided Visual Token Pruning for Multimodal Large Language Models](2026-2602.17196-entropyprune-matrix-entropy-guided-visual-token-pruning-for-multimodal-l.md)**  
  実装：[✓](https://github.com/YahongWang1/EntropyPrune) ・ リポジトリ内被引用：4  
  既存の視覚トークン枝刈り（visual トークン 枝刈り）は重要そうなトークンを残すが、どの層で削除するかを経験的に固定するものが多く、異なるモデル・画像で最適な位置が変わる理由を説明しにくい。

- **2026-05 · [Beyond Surrogate Gradients: Fully Differentiable Token Pruning for Vision-Language Models](2026-2605.28051-beyond-surrogate-gradients-fully-differentiable-token-pruning-for-vision.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  DiffPruneは、視覚言語モデル（Vision-Language モデル、VLM）の入力画像を多数の視覚トークンへ展開した後、どのトークンだけを言語モデルへ渡すかを学習する方式である。一次論文のLLaVA-1.5-7B評価では、576個の視覚トークンから64個だけを保持する88.9%削減時、10課題の正規化平均性能が元モデルの96.5%となった。

- **2026-04 · [PixelPrune: Pixel-Level Adaptive Visual Token Reduction via Predictive Coding](2026-2604.00886-pixelprune-pixel-level-adaptive-visual-token-reduction-via-predictive-co.md)**  
  実装：[✓](https://github.com/OPPO-Mente-Lab/PixelPrune) ・ リポジトリ内被引用：3  
  画素の重複を予測符号化で検出し、視覚符号器へ入れる前に重複ブロックを落とす学習不要の方式で、文書では精度をほぼ保ちながら推論を最大4.2倍速くした。

- **2026-03 · [TERMINATOR: Learning Optimal Exit Points for Early Stopping in Chain-of-Thought Reasoning](2026-2603.12529-terminator-learning-optimal-exit-points-for-early-stopping-in-chain-of-t.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  複雑な問題では思考が必要だが、答えが既に得られた後にも検算、別解探索、方針変更を続けることがある。実行時には未来の最終解答を参照せず、モデル最終層の隠れ状態から終了の可能性を予測し、複数トークンの多数決を経て を挿入する。Qwen3-8BのMATH-500では思考圧縮率45.1%（約54.9%削減）で、正答率91.1%から90.7%とほぼ同水準を維持した。

- **2026-03 · [EvoPrune: Early-Stage Visual Token Pruning for Efficient MLLMs](2026-2603.03681-evoprune-early-stage-visual-token-pruning-for-efficient-mllms.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  多くの既存削減方式は、視覚符号化器が全トークンを処理した後に削減を行うため、後段の言語モデルの事前入力処理は軽くできても、視覚符号化器がすでに使った演算量は取り戻せない。

- **2026-02 · [OTPrune: Distribution-Aligned Visual Token Pruning via Optimal Transport](2026-2602.20205-otprune-distribution-aligned-visual-token-pruning-via-optimal-transport.md)**  
  実装：[✓](https://github.com/xiwenc1/OTPrune) ・ リポジトリ内被引用：3  
  OTPruneは、画像と言語を組み合わせて推論する多モーダル大規模言語モデルにおいて、画像から得られる多数の視覚トークンを追加学習なしで削減する手法である。原著が証明する約63%の最悪時近似保証は代理目的の最大化に対するものであり、元のワッサースタイン距離や言語モデルの回答品質が63%保証されるという意味ではない。

- **2026-07 · [CRISP: Pre-LLM Yet Text-Driven Visual Token Pruning for Efficient LVLM Inference](2026-2607.16326-crisp-pre-llm-yet-text-driven-visual-token-pruning-for-efficient-lvlm-in.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  学習を追加せず、言語モデルの層内注意重みを取り出さないことが設計上の要点である。原著の表IではLLaVA-1.5-7Bの視覚トークンを576個から128個（77.8%削除）へ減らしても、報告された平均性能保持率は99.5%である。

- **2026-07 · [Combating Textual Noise and Redundancy: Entropy-Aware Dense Visual Token Pruning](2026-2607.02484-combating-textual-noise-and-redundancy-entropy-aware-dense-visual-token-.md)**  
  実装：[✓](https://github.com/SJTU-DeepVisionLab/EADP) ・ リポジトリ内被引用：2  
  画像を含むVision-Language モデル（VLM）では、画像エンコーダが作る多数のパッチトークンがLLMの入力を長くし、事前充填の注意演算とメモリ転送を増やす。EADP（Entropy-Aware Dense Pruning）はこの二段階の失敗を分離する。

- **2026-06 · [Accelerating Multimodal Large Language Models with Prior-Corrected Token Reduction](2026-2606.24156-accelerating-multimodal-large-language-models-with-prior-corrected-token.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  指示なしでも生じるモデル由来の注意の偏りを空トークンで測って割り引き、指示が追加で運ぶ情報の多い視覚トークンだけを残す学習不要の削減方式で、厳しい予算でも精度を保ちながら推論を高速化した。

- **2026-04 · [Stability Implies Redundancy: Delta Attention Selective Halting for Efficient Long-Context Prefilling](2026-2604.18103-stability-implies-redundancy-delta-attention-selective-halting-for-effic.md)**  
  実装：[✓](https://github.com/verach3n/DASH) ・ リポジトリ内被引用：2  
  FlashAttentionは注意行列を外部メモリへ展開しないことで転送量を削減するが、入力トークンが多ければ必要な計算量自体は残る。DASH（Delta 注意機構 Selective Halting）は、各トークンの表現が層を進むにつれて更新されなくなる「意味的固定点」に着目する。

- **2026-04 · [QAPruner: Quantization-Aware Vision Token Pruning for Multimodal Large Language Models](2026-2604.02816-qapruner-quantization-aware-vision-token-pruning-for-multimodal-large-la.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  視覚トークンの量子化のされにくさを群単位の模擬誤差と外れ値強度で測り、意味的な重要度と混ぜて残すトークンを選ぶことで、低ビット量子化と枝刈りを併用しても正解率が落ちにくい方式を示した。

- **2026-04 · [MI-Pruner: Crossmodal Mutual Information-guided Token Pruner for Efficient MLLMs](2026-2604.03072-mi-pruner-crossmodal-mutual-information-guided-token-pruner-for-efficien.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  注意の吸い込み（注意機構 Sink）、位置偏り、複数注意ヘッドの役割差、画像全体で目立つ物体への偏りがある。さらに64トークンのPOPE効率測定では、質問関連性だけを使うλ=1の構成が77.06ms、13.93GBであり、VisPrunerの89.48ms、14.35GBより小さい。

- **2026-04 · [HieraVid: Hierarchical Token Pruning for Fast Video Large Language Models](2026-2604.01881-hieravid-hierarchical-token-pruning-for-fast-video-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  動画の区間分割と静的トークンの統合、区間ごとの予算配分と多様性を最大化する選択、層の深さに応じた段階的な削減を組み合わせ、視覚トークンを10パーセントまで減らしても性能の9割以上を保つ階層型の枝刈り方式を示した。

- **2026-02 · [Stateful Token Reduction for Long-Video Hybrid VLMs](2026-2603.00198-stateful-token-reduction-for-long-video-hybrid-vlms.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  長い動画を扱う視覚言語モデルでは、各フレームを多数の視覚トークンへ変換して言語モデルへ入力するため、動画が長くなると事前充填（プリフィル）の計算量とメモリが増大する。著者はこの現象を「状態付き圧縮」と捉え、浅い層では多くのトークンを保持し、深い層へ進むほど段階的に削減する方式を設計した。

- **2026-02 · [DUET-VLM: Dual stage Unified Efficient Token reduction for VLM Training and Inference](2026-2602.18846-duet-vlm-dual-stage-unified-efficient-token-reduction-for-vlm-training-a.md)**  
  実装：[✓](https://github.com/AMD-AGI/DUET-VLM) ・ リポジトリ内被引用：2  
  視覚側の局所クラスタ集約と、言語側のテキスト誘導の段階的ドロップを組み合わせた二段の視覚トークン削減。67パーセント削減でも精度の99パーセント前後を保ち、学習時間も3割減らす。

- **2025-12 · [Towards Lossless Ultimate Vision Token Compression for VLMs](2025-2512.09010-towards-lossless-ultimate-vision-token-compression-for-vlms.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  視覚符号器では空間軸に沿う反復統合で、言語モデル側では周波数の低域通過で視覚トークンを最終層まで段階的に消す学習不要の圧縮により、約2倍の高速化とほぼ無劣化の精度を両立した。

- **2026-10 · [TopK-Guided: Adaptive, Budget-Aware Activation Sparsity for Efficient LLM Inference](2026-2610.01763-topk-guided-adaptive-budget-aware-activation-sparsity-for-efficient-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  両手法はさらにTransformer層間へ一様な疎性予算を与え、疎化への耐性が異なる層を区別しない。論文のC4評価では、Llama-2-7BとLlama-3-8Bの目標疎性30%、50%、70%で、TopK-GuidedはTEALおよびWINAと比べperplexityと8課題平均正解率の両方で全条件最高だった。

- **2026-09 · [ShallowStream: Index Shallow then Answer Deep for Streaming Video Understanding](2026-2609.02780-shallowstream-index-shallow-then-answer-deep-for-streaming-video-underst.md)**  
  実装：[✓](https://github.com/CURRENTF/ShallowStream) ・ リポジトリ内被引用：1  
  流入フレームは浅い層だけで処理してKVを履歴索引とし、質問時だけ浅い層の注意で証拠を選んで全層計算することで、ストリーミング動画理解のプリフィル遅延を最大52.1倍下げる深さ分離方式。

- **2026-09 · [LayerRoute: Adaptive Layer-Skipping with LoRA-Preserved Quality for Efficient LLM Inference](2026-2609.13682-layerroute-adaptive-layer-skipping-with-lora-preserved-quality-for-effic.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  同時にランク-8 LoRAを注意機構 射影へ入れ、層を飛ばすことで失われる表現能力をパラメータ-efficientに補償する。壁時計速度は全試行で改善し1.02〜1.06倍、平均1.04倍。

- **2026-08 · [RoRA: Role-Oriented Regional Allocation for Visual Token Pruning in MLLMs](2026-2608.07088-rora-role-oriented-regional-allocation-for-visual-token-pruning-in-mllms.md)**  
  実装：[✓](https://github.com/LukieLuu/RoRA) ・ リポジトリ内被引用：1  
  高解像度画像や複数画像では、画像に由来するトークンが入力系列の多くを占め、事前計算（プリフィル）の演算、注意機構のキー・バリュー（KV）キャッシュ、応答開始までの時間を増加させる。LLaVA-1.5-7Bの視覚576トークンを64個へ減らす条件（88.9%削減）では、九つの評価課題の正規化平均が非削減時の96.5%に相当した。

- **2026-08 · [OmniPack: Unified Token Compression for Efficient Omni-modal Large Language Models](2026-2608.03812-omnipack-unified-token-compression-for-efficient-omni-modal-large-langua.md)**  
  実装：[✓](https://github.com/RowanSu/OmniPack) ・ リポジトリ内被引用：1  
  全モーダルモデル向けに、モデル前段の構造的圧縮とモデル内段の質問条件付き圧縮を統一した学習不要の2段トークン圧縮で、計算量を約6分の1にしながら性能の98パーセントを保った。

- **2026-08 · [DiffPrune: Differentiable Information Throttling for Token Pruning in Vision-Language Models](2026-2608.01985-diffprune-differentiable-information-throttling-for-token-pruning-in-vis.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  視覚言語モデル（Vision-Language モデル; VLM）では、画像エンコーダが数百〜数千の視覚トークンを生成する。言語モデルへ渡す視覚トークンを減らせば事前処理（プリフィル）の計算量と遅延を削減できるが、「どのトークンを残すか」を学習する段階で問題が生じる。この演算子不一致が重要度学習を不安定にする。

- **2026-08 · [Batch-wise Adaptive Pruning: Periodic Neuron Activation-Aware Weight Pruning for Language Reasoning Model](2026-2608.14003-batch-wise-adaptive-pruning-periodic-neuron-activation-aware-weight-prun.md)**  
  実装：[✓](https://github.com/matsuolab/batch-wise-prune) ・ リポジトリ内被引用：1  
  バッチ共有マスクで崩れる閾値型の適応枝刈りを、周期的なtop-k選択と重要度を蓄積する活性化メモリで置き換え、バッチ4・スパース率50パーセントでTEALを39.7ポイント上回り1.40倍の高速化を得る学習不要の枝刈り。

- **2026-07 · [Spectral Heat Flow for Conservative Token Condensation in Vision-Language Models](2026-2607.10640-spectral-heat-flow-for-conservative-token-condensation-in-vision-languag.md)**  
  実装：[✓](https://github.com/Lzy-dot/SpecFlow) ・ リポジトリ内被引用：1  
  特徴類似グラフ上の熱拡散で重要度を領域単位に平滑化し、四分木の領域配分と捨てる側のシンク凝縮で被覆と統計を守る学習不要の視覚トークン圧縮で、約9割削減でも性能の約96パーセントを保った。

- **2026-07 · [OmniDelta: Skill-Driven Budget Allocation for Token Compression in OmniLLMs](2026-2607.25669-omnidelta-skill-driven-budget-allocation-for-token-compression-in-omnill.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  総保持量を変えずに、質問と技能プールの類似度で音声と映像の間の予算を移し、複雑さと冗長さで時刻方向の予算を組み替える階層的配分により、全モダリティモデルのトークン圧縮の精度と効率の釣り合いを改善した研究である。

- **2026-07 · [CLIP Tricks You: Training-free Token Pruning for Efficient Pixel Grounding in Large Vision-Language Models](2026-2605.13178-clip-tricks-you-training-free-token-pruning-for-efficient-pixel-groundin.md)**  
  実装：[✓](https://github.com/sejong-rcv/LiteLVLM) ・ リポジトリ内被引用：1  
  一般的な画像理解向け視覚トークン枝刈りは、画像の全体表現への寄与や画像・テキストの高い類似度を手掛かりにトークンを残す。GLaMMの元の576視覚トークンを192に削減したとき、8評価分割平均の領域分割指標は75.5から68.1となり、元性能の90.3%を維持した。

- **2026-06 · [Stepwise Token Selection for Efficient Multimodal Large Language Models](2026-2606.16067-stepwise-token-selection-for-efficient-multimodal-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  視覚トークンを既選択分を条件に1個ずつ選び、学習した終了動作で個数も決める逐次選択方式で、固定比率の枝刈りを全削減水準で上回り、約9割削減でも精度の94.6パーセントを保った。

- **2026-06 · [Skip a Layer or Loop It? Learning Program-of-Layers in LLMs](2026-2606.06574-skip-a-layer-or-loop-it-learning-program-of-layers-in-llms.md)**  
  実装：[✓](https://github.com/tianyi-lab/PoLar) ・ リポジトリ内被引用：1  
  本論文は、学習済みの各層を関数とみなし、その呼出し順と回数を入力に応じて変える「層プログラム（Program-of-Layers; PoLar）」を提案する。Qwen1.5-MoE-A2.7B-Chatの24層を対象にした実測では、予測器・埋め込み器・候補探索を含む追加費用は合計3.05ミリ秒、通常の全層実行の0.8%だった。

- **2026-05 · [Gated Subspace Inference for Transformer Acceleration](2026-2605.03109-gated-subspace-inference-for-transformer-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデル（LLM）のバッチサイズ1の逐次復号では、GPUの計算能力よりも重み行列を高帯域メモリ（HBM）から読む費用が律速になりやすい。Gated Subspace Inference（GSI）は、各層の活性化を低次元基底への射影と残差に分解し、残差が十分小さいトークンだけ、事前計算した低次元の重み像を使う方式である。

- **2026-05 · [EchoPrune: Interpreting Redundancy as Temporal Echoes for Efficient VideoLLMs](2026-2605.10050-echoprune-interpreting-redundancy-as-temporal-echoes-for-efficient-video.md)**  
  実装：[✓](https://github.com/renaissanceee/EchoPrune) ・ リポジトリ内被引用：1  
  直前フレームから再構成できるトークンを時間的な反響として冗長とみなし、質問関連度と再構成誤差の差で一度に間引くことで、同じ予算で最大20倍のフレームを見て精度と速度を両方上げた学習不要の枝刈り方式。

- **2026-05 · [DynaTok: Temporally Adaptive and Positional Bias-Aware Token Compression for Video-LLMs](2026-2605.19322-dynatok-temporally-adaptive-and-positional-bias-aware-token-compression-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  時間メモリで新しいフレームへ予算を厚くし、空間メモリで過去に選んだ領域との重なりを避ける二段配分により、視覚トークンを約9割削っても動画質問応答の精度を基準の95パーセント超に保った。

- **2026-05 · [Different Prompts, Different Ranks: Prompt-aware Dynamic Rank Selection for SVD-based LLM Compression](2026-2605.08568-different-prompts-different-ranks-prompt-aware-dynamic-rank-selection-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  特異値分解（SVD）による低ランク圧縮は、重み行列を小さい行列の積へ分解し、寄与の小さい成分を切り捨てる。

- **2026-05 · [AQuaUI: Visual Token Reduction for GUI Agents with Adaptive Quadtrees](2026-2605.19260-aquaui-visual-token-reduction-for-gui-agents-with-adaptive-quadtrees.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  画面の情報密度に合わせて四分木で割り、各葉に代表トークンを一つ残す学習なしの削減を提案し、320億級モデルでトークン29.52パーセント減と性能の99.06パーセント保持、最大13.22パーセントの高速化を示した。

- **2026-04 · [Tango: Taming Visual Signals for Efficient Video Large Language Models](2026-2604.09547-tango-taming-visual-signals-for-efficient-video-large-language-models.md)**  
  実装：[✓](https://github.com/xjtupanda/Tango) ・ リポジトリ内被引用：1  
  Tangoは、動画大規模言語モデル（Video LLM）へ渡す視覚トークンの数を削減する、学習不要の前処理方式である。LLaVA-OneVision-7Bの32フレーム評価では、視覚トークンを10%にしたとき元の4ベンチマーク平均性能の98.9%を保持し、実測推論速度は1.88倍となった。

- **2026-04 · [RCP: Representation Consistency Pruner for Mitigating Distribution Shift in Large Vision-Language Models](2026-2604.04972-rcp-representation-consistency-pruner-for-mitigating-distribution-shift-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  累積マスクの枝刈りと、捨てたトークンの要約による遅延修復と統計一致の修復損失を組み合わせ、視覚トークン88.9パーセント削減とFLOPs 85.7パーセント削減を精度低下約5パーセントで達成した。

- **2026-04 · [Geometry-Guided 3D Visual Token Pruning for Video-Language Models](2026-2604.18260-geometry-guided-3d-visual-token-pruning-for-video-language-models.md)**  
  実装：[✓](https://github.com/homothetic/Geo3DPruner) ・ リポジトリ内被引用：1  
  動画言語モデル（Video Language モデル）は、動画フレームを多数の画像パッチに分割して言語モデルへ入力する。三次元場面理解では同じ机や椅子が異なるカメラ位置から繰り返し写るため、入力トークンが増えても新しい空間情報が比例して増えるとは限らない。比較対象FastVは81.0%、VisPrunerは84.9%である。

- **2026-03 · [SeGPruner: Semantic-Geometric Visual Token Pruner for 3D Question Answering](2026-2603.29437-segpruner-semantic-geometric-visual-token-pruner-for-3d-question-answeri.md)**  
  実装：[✓](https://github.com/intcomp/SegPruner) ・ リポジトリ内被引用：1  
  顕著性で物体の証拠を確保し、3次元幾何の多様性で空間の広がりを補う二段の視覚トークン削減で、トークン予算91パーセント削減と遅延86パーセント削減を3次元質問応答の精度を保ちながら達成した。

- **2026-03 · [ResPrune: Text-Conditioned Subspace Reconstruction for Visual Token Pruning in Large Vision-Language Models](2026-2603.21105-resprune-text-conditioned-subspace-reconstruction-for-visual-token-pruni.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  選んだ視覚トークンの部分空間で説明できない残差が最大のトークンを貪欲に足し、指示文の名詞との類似度で重み付けする学習不要の枝刈りで、トークンの77.8パーセント削減でも性能の99.3パーセントを保持した。

- **2026-03 · [Keeping the Evidence Chain: Semantic Evidence Allocation for Training-Free Token Pruning in Video Temporal Grounding](2026-2603.05663-keeping-the-evidence-chain-semantic-evidence-allocation-for-training-fre.md)**  
  実装：[✓](https://github.com/JiaqiLi404/SemVID) ・ リポジトリ内被引用：1  
  動画の時刻特定向けに、フレーム別予算配分と物体・運動・文脈の3役割の選択で証拠の連鎖を残す学習不要の枝刈りを行い、トークン12.5パーセントで精度の95.4パーセント保持と入力処理5.8倍高速化を両立した。

- **2026-03 · [ForestPrune: High-ratio Visual Token Compression for Video Multimodal Large Language Models via Spatial-Temporal Forest Modeling](2026-2603.22911-forestprune-high-ratio-visual-token-compression-for-video-multimodal-lar.md)**  
  実装：[✓](https://github.com/luminousllsa/ForestPrune) ・ リポジトリ内被引用：1  
  全フレームの視覚トークンを意味・位置・時刻で木に結び、深い木の根と幹を残して葉から削る学習不要の方式で、トークン90パーセント削減でも平均精度の95.8パーセントを保持した。

- **2026-03 · [ASAP: Attention-Shift-Aware Pruning for Efficient LVLM Inference](2026-2603.14549-asap-attention-shift-aware-pruning-for-efficient-lvlm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ASAPはこの注意の位置偏り（注意機構 shift）を緩和するため、視覚トークン同士に限り、重要度の高い未来位置への注意を段階的に許可する。

- **2026-02 · [WiSparse: Boosting LLM Inference Efficiency with Weight-Aware Mixed Activation Sparsity](2026-2602.14452-wisparse-boosting-llm-inference-efficiency-with-weight-aware-mixed-activ.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデル（LLM）の推論では、各層の線形射影が多数の乗算と重み読出を必要とする。WiSparseは、活性と重みの両方からチャネル重要度を推定し、モデル全体の疎性率をブロック・層の二段階で割り当てる学習不要の活性疎化（学習不要 活性値 sparsity）方式である。

- **2026-02 · [POP: Prefill-Only Pruning for Efficient Large Model Inference](2026-2602.03295-pop-prefill-only-pruning-for-efficient-large-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  プリフィルでのみ深い層を飛ばしデコードでは全層を使う段階別枝刈りで、生成精度をほぼ保ったままプリフィルを最大1.37倍高速化した。

- **2026-02 · [Focus-Scan-Refine: From Human Visual Perception to Efficient Visual Token Pruning](2026-2602.05809-focus-scan-refine-from-human-visual-perception-to-efficient-visual-token.md)**  
  実装：[✓](https://github.com/ILOT-code/FSR) ・ リポジトリ内被引用：1  
  高解像度画像や複数フレームの動画ではトークン数が増え、事前充填の演算量、注意機構に必要な記憶量、鍵・値キャッシュ（KV キャッシュ）の容量が増加する。LLaVA-1.5-7Bで視覚トークンを576個から64個へ削減すると、9種類の評価を正規化した平均性能保持率は96.1%であり、比較対象のCDPrunerは95.7%、VisPrunerは93.5%だった。

- **2026-02 · [CLAA: Cross-Layer Attention Aggregation for Accelerating LLM Prefill](2026-2602.16054-claa-cross-layer-attention-aggregation-for-accelerating-llm-prefill.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  CLAA（Cross-層 注意機構 Aggregation）は、層ごとに重要度順位が大きく変わるという現象を先に検証し、選別層の直前の複数層の重要度を各トークンについて最大値で集約する。

- **2026-01 · [SyncThink: A Training-Free Strategy to Align Inference Termination with Reasoning Saturation](2026-2601.03649-syncthink-a-training-free-strategy-to-align-inference-termination-with-r.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  SyncThinkは、思考過程を明示的に生成する推論特化言語モデルに対し、追加学習なしで推論を早期終了させる復号制御方式である。

- **2026-01 · [Fast Forward: Accelerating LLM Prefill with Predictive FFN Sparsity](2026-2602.00397-fast-forward-accelerating-llm-prefill-with-predictive-ffn-sparsity.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  FastForwardは、大規模言語モデル（Large Language モデル; LLM）の入力一括処理（プリフィル）におけるフィードフォワード網（Feed-順伝播 Network; FFN）の演算を、入力文脈に応じてブロック単位で省く方式である。

- **2025-12 · [Script: Graph-Structured and Query-Conditioned Semantic Token Pruning for Multimodal Large Language Models](2025-2512.01949-script-graph-structured-and-query-conditioned-semantic-token-pruning-for.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  手法は、余弦類似度の二部グラフを用いて冗長な視覚トークンを削るグラフ構造化枝刈り（Graph-Structured Pruning; GSP）と、質問との関連性に加えて特徴の多様性を考慮する質問条件付き意味枝刈り（Query-Conditioned Semantic Pruning; QCSP）から成る。

### 直近12か月・未被引用（2025-12〜2026-11）

- **2026-10 · [Vision Token Pruning via Query-Vision Interaction Decomposition](2026-2610.33215-vision-token-pruning-via-query-vision-interaction-decomposition.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  クエリと視覚の相互作用行列の低ランク構造を使い、上位の特異方向へ参加するトークンを残す学習なしの枝刈りQViDで、強い圧縮ほど既存手法より精度を保った研究。

- **2026-10 · [VETO: Video Efficient Token Optimization for Vision Language Models](2026-2610.01785-veto-video-efficient-token-optimization-for-vision-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動画の視覚トークンを、フレーム内の意味的統合の後にフレーム間の冗長統合を行う二軸の階層圧縮で減らし、EgoSchemaで精度を保ったまま遅延を4割下げ、保持率10パーセントでも単軸方式を上回るプラグイン。

- **2026-10 · [TokenGate: Adapting LLMs for Fast and Memory-Efficient Prefill with Learned Token Pruning](2026-2610.26754-tokengate-adapting-llms-for-fast-and-memory-efficient-prefill-with-learn.md)**  
  実装：[✓](https://github.com/tokengate-models/TokenGate) ・ リポジトリ内被引用：0  
  中間層に学習可能な採点ゲートを差し込み、重要トークンだけを上層へ通す枝刈りを端から端まで学習することで、精度を保ったまま入力処理を最大11.3倍高速化しピークメモリを最大3.4倍下げた。

- **2026-10 · [ThinkJev: One Thought, Every Budget for Calibrated Typed Decisions](2026-2610.37732-thinkjev-one-thought-every-budget-for-calibrated-typed-decisions.md)**  
  実装：[✓](https://github.com/ding-xiaolu/ThinkJev) ・ リポジトリ内被引用：0  
  一つのハイブリッド思考モデルの回答スロットを、空の思考と実思考の後で同じキャッシュ済みプロンプトから読み、直接回答には誤り率の統計保証を付け、残りは確信度が立つ時点で思考を止める、学習なしの二系統カスケード。

- **2026-10 · [Same Beliefs, Different Policies: Learning Reusable Representations for Early Stopping in LLM Reasoning](2026-2610.30450-same-beliefs-different-policies-learning-reusable-representations-for-ea.md)**  
  実装：[✓](https://github.com/EdisonNi-hku/BELT) ・ リポジトリ内被引用：0  
  凍結した推論モデルの隠れ状態から正答見込みの4つの信念を価格非依存に学習し、その上に線形の停止方策を当てはめることで、価格変更に再学習なしで追随しながら生成トークンを4割から5割減らす早期停止方式。

- **2026-10 · [Rescuing Your Pruning: Rethinking Visual Token Pruning and Post-Training Recovery in MLLMs](2026-2610.33688-rescuing-your-pruning-rethinking-visual-token-pruning-and-post-training-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  枝刈りの規則を固定したまま圧縮状態で事後学習することで精度低下の大半を回復できることを示し、回復の内訳を分解したうえで、どの段階でトークンを削るべきかという共同圧縮の配分指針を実測で与える研究。

- **2026-10 · [LRCC: Generalizing Low-Rank Compression with Conditional Computation](2026-2610.08858-lrcc-generalizing-low-rank-compression-with-conditional-computation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  入れ子状の低ランクパスをブロック単位のルーターでトークンごとに選ばせ、同じ有効パラメータ予算で静的低ランク圧縮よりLlama-2-7Bの下流平均正解率を最大7.6ポイント上げる条件付き圧縮。

- **2026-10 · [Hierarchical and Query-Aware Visual Token Pruning for High-Resolution LVLMs](2026-2610.24102-hierarchical-and-query-aware-visual-token-pruning-for-high-resolution-lv.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  サムネイルの多様さで画像ごとの予算を動かし、質問との類似度でクロップへ配分し、共有空間で測った偏り除去済みの質問スコアと視覚的顕著性を融合して視覚トークンを選ぶ学習不要の階層型枝刈りで、保持率25パーセントで未枝刈り比98.0パーセントの性能と2.0倍のスループットを得た。

- **2026-10 · [From Patching to Pruning Visual Computation in Vision Language Models](2026-2610.03389-from-patching-to-pruning-visual-computation-in-vision-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  活性パッチングの診断を推論へ転用し、視覚トークンの射影を中立な代理活性へ置換できる安全な層を検証で特定して、トークンを消さずに視覚計算の55パーセントを削減する方式。

- **2026-10 · [FlashGaze: Training-Free Multi-Scale Patch Pruning For Efficient Video Understanding](2026-2610.04225-flashgaze-training-free-multi-scale-patch-pruning-for-efficient-video-un.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画素差を情報損失の代理にし、四分木の動的計画法でパッチの削除と統合と保持を予算内で決めることで、符号化の前に動画の冗長性を削りプリフィルを最大17倍速くする学習不要の方式。

- **2026-10 · [Don't Ask the LLM: Visual Token Pruning with Spectral Structure and Semantic Relevance](2026-2610.38303-don-t-ask-the-llm-visual-token-pruning-with-spectral-structure-and-seman.md)**  
  実装：[✓](https://github.com/sejong-rcv/ST-Pruner) ・ リポジトリ内被引用：0  
  LLMへ入る前に、視覚特徴の低ランク構造への寄与を示すスペクトル顕著性と反転したパッチ・テキスト類似度を乗算融合して視覚トークンを選ぶ学習不要の枝刈り方式で、トークンを約9分の1に減らしても性能の95パーセント超を保ち3.2倍速くする。

- **2026-10 · [DIPrune: Task-Aware Token Pruning with Dual Importance for Efficient Multimodal Language Models](2026-2610.08341-diprune-task-aware-token-pruning-with-dual-importance-for-efficient-mult.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚トークンの重要度を、層内の意味整列と層間の順位上昇という二つの順位スコアで判定し、浅層の慣性に埋もれる新興トークンを救いながら学習不要で枝刈りする方式。

- **2026-10 · [Content-Aware Adaptive Token Pruning for Video-Language Models](2026-2608.03112-content-aware-adaptive-token-pruning-for-video-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚トークンの相関の固有値の減衰率から動画ごとの冗長度を測って保持率を動画ごとに決める学習不要の枝刈りで、平均保持率10パーセントでも固定保持率より動画説明の正解率を7.48ポイント高く保ち、言語モデルの演算量を約95.5パーセント減らす。

- **2026-10 · [Channel Selection for Mixture-of-Experts Decoding Needs No Calibration Data](2026-2610.37386-channel-selection-for-mixture-of-experts-decoding-needs-no-calibration-d.md)**  
  実装：[✓](https://github.com/AidenGeunGeun/calibration-free-moe) ・ リポジトリ内被引用：0  
  MoEデコードのチャネル選択では較正しきい値は読み出し量も精度も保証しないことを示し、上位k件への置き換えと、重みだけから作る三値スケッチと低ランク回復を持つ読み手で、読み出し17.8パーセントでも精度の98.1パーセントを保つ。

- **2026-10 · [CausalPrune: Counterfactual Causal Token Pruning for Efficient Large Vision-Language Models](2026-2611.00058-causalprune-counterfactual-causal-token-pruning-for-efficient-large-visi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚トークンの重要度を相関ではなく介入の効果で測り、一次近似と層ごとの媒介分解で段階的に枝刈りすることで、強い削減でも性能を保ち計算量を約11倍減らす視覚言語モデルの枝刈り。

- **2026-10 · [Bifocal: Training-Free Mixed Granularity Visual Token Pruning for Multimodal LLMs](2026-2610.18399-bifocal-training-free-mixed-granularity-visual-token-pruning-for-multimo.md)**  
  実装：[✓](https://github.com/EIT-NLP/Bifocal) ・ リポジトリ内被引用：0  
  視覚トークンの枝刈りで細粒度課題が崩れる問題に対し、質問焦点と画像自体の証拠へ別予算を配る混合粒度の学習不要な2段階枝刈りで、全能力群で未圧縮比90パーセント超を保った。

- **2026-10 · [Adaptive Stopping of Streamed Reasoning for Language Model Agents](2026-2610.27981-adaptive-stopping-of-streamed-reasoning-for-language-model-agents.md)**  
  実装：[✓](https://jh2525.github.io/StreamStop/) ・ リポジトリ内被引用：0  
  推論テキストの接頭辞だけを読み、全推論の行動と一致する時点を学習した軽量ヘッドで生成を打ち切る停止方針で、成功率をほぼ保ったままエージェントの推論トークンを最大で約半分に減らした。

- **2026-09 · [StepPrune: Adaptive Sequential Visual Token Selection across Multimodal Large Language Models](2026-2609.13804-stepprune-adaptive-sequential-visual-token-selection-across-multimodal-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  多くの視覚言語モデルは、画像エンコーダが生成した数百〜数千個の視覚トークンをテキスト指示の前へ付けてLLMに入力する。これらの視覚prefixはプリフィルで全層を通るため、視覚側の冗長性が大きいと推論計算とKV容量の双方に負担をかける。StepPruneは視覚トークン保持を逐次的な意思決定問題として定義する。

- **2026-09 · [SinkPruner: Sink-Free Visual Token Pruning for Multimodal Large Language Models](2026-2609.01004-sinkpruner-sink-free-visual-token-pruning-for-multimodal-large-language-.md)**  
  実装：[✓](https://github.com/LaVi-Lab/SinkPruner) ・ リポジトリ内被引用：0  
  注意を欺く高ノルム外れ値を先に取り除いて1個へ集約し、その後にテキスト誘導で絞る学習不要の視覚トークン枝刈りで、約9割削減でもLLaVA-1.5の性能の96.5パーセントを保った。

- **2026-09 · [S$^2$Prune: Spatially Structured Visual Token Pruning for Multimodal Large Language Models](2026-2609.01224-s-2-prune-spatially-structured-visual-token-pruning-for-multimodal-large.md)**  
  実装：[✓](https://github.com/yuanyuanjia71-spec/S2Prune) ・ リポジトリ内被引用：0  
  各画像領域への最低保証で空間被覆を固定し、残り予算を局所構造の豊かな領域へ配って代表トークンを選ぶ学習不要の視覚トークン枝刈りで、576個中32個でも元性能の79.3パーセントを保持した。

- **2026-09 · [GleanVID: Complementary Token Selection for Efficient Video Large Language Models](2026-2609.37042-gleanvid-complementary-token-selection-for-efficient-video-large-languag.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  時間的新しさでフレームへ予算を配り、局所代表性と既存選択に対する部分空間の補完性でトークンを選ぶことで、視覚トークン25パーセントで性能の98.6パーセントを保つ動画モデル向け圧縮方式。

- **2026-09 · [From Token Importance to Conditional Removability: Rethinking Visual Token Pruning in Multimodal Large Language Models](2026-2609.26484-from-token-importance-to-conditional-removability-rethinking-visual-toke.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  その観測に基づきCoRePruneを提案する。Qwen3.5-9Bで元の1024視覚トークンを最終128に削減した条件では、7指標をdense基準で正規化した平均相対性能90.3%を保持した。

- **2026-09 · [FlexEE: Self-Speculative and KV-Compatible Early Exiting for Offloading-Aware LLM Inference](2026-2609.17008-flexee-self-speculative-and-kv-compatible-early-exiting-for-offloading-aware-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Top-K自己投機による軽量な早期退出と隠れ状態の持越しでKV整合性を保ち、重みオフロード時に後段層の計算と転送をまとめて省く。

- **2026-09 · [Do Dynamic Routers Need Memory? HeRo: History-Aware Routing for Efficient LLM Inference](2026-2609.08189-hero-history-aware-routing-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各層の局所状態だけでなく過去のゲート選択と残差変化を線形注意メモリへ蓄積し、Llama 3.1-8Bで26.87%のパラメータ計算を回避しつつ密モデル比100.24%の性能を保つ動的FFNルーティング。

- **2026-09 · [Beyond One-Size-Fits-All: Sample-Adaptive Strategy Routing for Vision Token Pruning in MLLMs](2026-2609.10346-beyond-one-size-fits-all-sample-adaptive-strategy-routing-for-vision-tok.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  VIP-Routerは画像と質問ごとにFastV、VisionZip、PruMerge+、DART、無圧縮Fullから最適なvisual-トークン 枝刈り方針を選ぶ軽量ルータ。枝刈り-sensitiveなVTC-Bench Group Aでは5保持率平均accuracy 40.35%→51.19%、utility 30.88→37.68。

- **2026-08 · [HAP: Head-Adaptive Visual Token Pruning via Cross-Modal Alignment](2026-2608.23921-hap-head-adaptive-visual-token-pruning-via-cross-modal-alignment.md)**  
  実装：[✓](https://github.com/baokou-fw2/HAP) ・ リポジトリ内被引用：0  
  視覚トークン枝刈りで全ヘッド一様平均が抱える雑音混入を、ヘッドごとのプロンプト整合度PAQで重み付けする二段集約へ置き換え、LLaVA-1.5-7Bでトークン5.6パーセント保持でも相対性能99.1パーセントと2.82倍の高速化を両立させる学習不要の枝刈り。

- **2026-08 · [E2S-Pruner: Progressive Two-Stage Evidence Fusion for Visual Token Pruning in Vision-Language Models](2026-2608.23253-e2s-pruner-progressive-two-stage-evidence-fusion-for-visual-token-prunin.md)**  
  実装：[✓](https://github.com/taoyu-qian/E2S-Pruner.git) ・ リポジトリ内被引用：0  
  注意ヘッドと層の証拠をデンプスター・シェーファー理論で信頼度付きに融合し空間的な偏りも抑える視覚トークン枝刈りで、LLaVA-1.5-7Bの平均128トークン時に性能保持率96.8パーセントとスループット1.96倍を達成した。

- **2026-08 · [CoverPrune: Coverage-Driven Token Pruning for 3D VLMs via Optimal Transport](2026-2608.13226-coverprune-coverage-driven-token-pruning-for-3d-vlms-via-optimal-transpo.md)**  
  実装：[✓](https://github.com/Brucess/CoverPrune) ・ リポジトリ内被引用：0  
  3次元視覚言語モデルの視覚トークン枝刈りを多様性最大化から視覚的証拠の被覆保存へ転換し、特徴・空間・時間のコストと情報量容量を持つ最適輸送と貪欲近似で、保持率5%でも崩れにくい学習不要の枝刈りを実現する研究。

- **2026-08 · [Allocation Before Ranking: Decoupled Token Compression for OmniLLMs](2026-2608.01665-allocation-before-ranking-decoupled-token-compression-for-omnillms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  一つの得点に容量配分と選択を兼ねさせる共有順位付けの欠陥を分解で示し、予算を先に明示してからモダリティ内で正規化して選ぶ学習なしの圧縮で、25パーセント保持でも全トークン性能の98.7パーセントを保った方式。

- **2026-07 · [Structured Redundancy Modeling for Efficient Visual Token Pruning in High-Resolution MLLMs](2026-2607.23046-structured-redundancy-modeling-for-efficient-visual-token-pruning-in-hig.md)**  
  実装：[✓](https://github.com/cvsp-lab/SFPruner) ・ リポジトリ内被引用：0  
  後段の言語モデルがそれらすべてを処理すると、注意演算とKVキャッシュの負担が増えるため、重要な視覚トークンだけを残す枝刈りが有効である。Qwen2.5-VL-7Bで平均512トークンを残す条件では、CDPrunerの選択時間112.4msに対し2.5msで、約110msを選択段階から削減する。

- **2026-07 · [Skip-It? Theoretical Conditions for Layer Skipping in Vision–Language Models](2026-2509.25584-skip-it-theoretical-conditions-for-layer-skipping-in-vision-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の層スキップ手法は、経験的な層番号や余弦類似度などを用いて処理を省略していたが、表現が似ていることと出力品質が保たれることは同義ではない。

- **2026-07 · [SepPrune: A Separator-based Pruning Framework for Efficient Multimodal Large Language Models](2026-2607.25818-sepprune-a-separator-based-pruning-framework-for-efficient-multimodal-la.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SepPruneはVLMの画像トークン直後に置かれるmodality separatorを単一queryとして用い、視覚トークンのkeyとの内積から重要度を線形時間で推定してLLM プリフィル前に削減する学習不要手法。

- **2026-07 · [SelectInfer: Selective Neuron Loading and Computation for On-Device LLMs](2026-2607.18081-selectinfer-selective-neuron-loading-and-computation-for-on-device-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  オフラインで重要FFNニューロンを選別して必要分だけロードし、入力ごとの活性で計算対象も絞ることで、端末LLMのメモリ量と計算量を独立に調整する方式。

- **2026-07 · [Resting Neurons, Active Insights: Robustifying Activation Sparsity in LLMs via Spontaneity](2025-2512.12744-resting-neurons-active-insights-improving-input-sparsification-for-large.md)**  
  実装：[✓](https://github.com/hxu105/SPON) ・ リポジトリ内被引用：0  
  TEALなどの活性疎化方式は、小さい入力活性を閾値処理で零にして重み転送と積和を省く。実際にNVIDIA A6000でバッチ1の生成速度を測定し、50%疎化したLlama3-8Bは64.13 トークン/s、Mistral-7Bは71.84 トークン/sであり、TEALの64.28、71.25 トークン/sとほぼ同じだった。

- **2026-07 · [Per-Token Fixed-Point Convergence in Depth-Recurrent Transformers](2026-2607.14427-per-token-fixed-point-convergence-in-depth-recurrent-transformers.md)**  
  実装：[✓](https://github.com/jlognn/depth-recurrent-convergence) ・ リポジトリ内被引用：0  
  深さ再帰型トランスフォーマーの再帰状態がトークンごとに異なる深さで不動点へ収束することを直接測定し、収束を読み取る学習不要の終了規則が一様深さの品質を平均深さ38パーセント減で達成した研究。

- **2026-07 · [PCA: Persistence-Aware Compression and Aggregation for Fast Video Large Language Models](2026-2607.22726-pca-persistence-aware-compression-and-aggregation-for-fast-video-large-l.md)**  
  実装：[✓](https://github.com/Heisenberg10110/PCA) ・ リポジトリ内被引用：0  
  符号化前にフレーム間類似度で間引き、残ったフレームへ過去フレームを減衰集約して動きを補う学習不要の前処理で、動画LLMの総FLOPsを約半分以下へ減らしながら精度をほぼ保つ。

- **2026-07 · [OmniScope: Modality-Decoupled Token Compression for Omnimodal Large Language Models](2026-2607.23193-omniscope-modality-decoupled-token-compression-for-omnimodal-large-langu.md)**  
  実装：[✓](https://github.com/MAC-AutoML/OmniScope) ・ リポジトリ内被引用：0  
  入力を処理する事前充填（プリフィル）では、そのトークン数が注意演算、GPUメモリ、遅延を増やす。既存の音声・映像圧縮には、音声で重要と判断した時間帯を映像側でも重視する方式がある。映像にはアンカー・差分時空間圧縮（Anchor-Delta Spatio-Temporal Compression、AD-STC）、音声には1秒区間内の類似トークン統合を用いる。

- **2026-07 · [OmniFocus: Query-Guided Modality-Balanced Token Compression for Omni-Modal Large Language Models](2026-2607.03050-omnifocus-query-guided-modality-balanced-token-compression-for-omni-moda.md)**  
  実装：[✓](https://github.com/icip-cas/OmniFocus) ・ リポジトリ内被引用：0  
  質問との類似度を映像と音声で独立に測って区間予算を配り、連関と顕著性の二重得点でトークンを選ぶ学習不要の圧縮で、保持率25パーセントでも正解率を保ちプリフィルを1.38倍にした。

- **2026-07 · [Capturing Token Tendencies for Training-Free Token Pruning in Multimodal Large Language Models](2026-2607.28341-capturing-token-tendencies-for-training-free-token-pruning-in-multimodal.md)**  
  実装：[✓](https://github.com/JieMaMagic/Trend-aware-Pruning) ・ リポジトリ内被引用：0  
  本論文は、多モーダル大規模言語モデル（Multimodal Large Language モデル、MLLM）の推論時に、画像由来の視覚トークンを削減する学習不要の手法を提案する。LLaVA-v1.5-7Bの実験では、初期保持288/576トークンの条件で平均相対性能98.89%を維持し、計算量を元の55.10%へ削減した。

- **2026-06 · [Stop When Further Reasoning Won't Help: Attention-State Adaptive Generation in Reasoning Models](2026-2606.15070-stop-when-further-reasoning-won-t-help-attention-state-adaptive-generati.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  中間答えの確信度と注意エントロピーの低下を合わせて推論の収束を見極める早期終了と介入の方式で、推論モデルの正解率を上げながら生成トークンを約4割減らした。

- **2026-06 · [One Layer's Trash is Another Layer's Treasure: Adaptive Layer-wise Visual Token Selection in LVLMs](2026-2606.14277-one-layer-s-trash-is-another-layer-s-treasure-adaptive-layer-wise-visual.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚トークンを捨てず層ごとに飛ばす適応型の選択方式で、各層が低ランク近似の注意で必要な領域だけを処理し、89パーセント圧縮でも元の精度の96.7パーセントを保った。

- **2026-06 · [Moving Beyond Diversity: Visual Token Pruning as Subspace Reconstruction for Efficient VLMs](2026-2606.18681-moving-beyond-diversity-visual-token-pruning-as-subspace-reconstruction-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚トークンの枝刈りを、大きさの情報を含めて元の特徴空間を近似する列部分集合選択として解き直し、関連度の低いトークンを優遇する反関連度と組み合わせることで、94パーセント削減でも基準性能の約95パーセントを保つ方式である。

- **2026-06 · [Fast Enough to Act: Spatio-Temporal Visual Token Merging for Low-Latency Robotic VLMs and VLAs](2026-2606.29350-fast-enough-to-act-spatio-temporal-visual-token-merging-for-low-latency-.md)**  
  実装：[✓](https://github.com/Junzhou-Chen/ST_Merge) ・ リポジトリ内被引用：0  
  視覚符号化器の浅い層で、時刻と位置を意識した多キュー照合により冗長な視覚トークンを統合し、重心で位置符号を直すことで、ロボット向け視覚言語モデルの推論を動画で約2倍、行動方策の高解像度入力で8.3倍速くした。

- **2026-06 · [End-to-End Dynamic Sparsity for Resource-Adaptive LLM Inference](2026-2606.27743-end-to-end-dynamic-sparsity-for-resource-adaptive-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常のLLM推論は、入力が簡単か難しいか、サーバーのメモリや締切が変動するかにかかわらず、同じTransformer層と注意ヘッドを実行する。従来の動的スキップも入力のエントロピーなどから難易度を推測する方式が多く、現在のサービス側の予算を直接条件にしていない。

- **2026-06 · [AVOC: Enhancing Hour-Level Audio-Video Understanding in Omni-Modal LLMs via Retrieval-Inspired Token Compression](2026-2606.24286-avoc-enhancing-hour-level-audio-video-understanding-in-omni-modal-llms-v.md)**  
  実装：[✓](https://github.com/YJCX330/AVOC) ・ リポジトリ内被引用：0  
  圧縮を検索問題として捉え、関連性・重要性・多様性の3基準でトークンを選ぶ学習型モジュールにより、長尺音声映像の正解率で次点を4.9から5.5ポイント上回った。

- **2026-05 · [VideoRouter: Query-Adaptive Dual Routing for Efficient Long-Video Understanding](2026-2605.05848-videorouter-query-adaptive-dual-routing-for-efficient-long-video-underst.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  VideoRouterは、固定の視覚トークン予算を「広く浅く」か「重要な場面へ厚く」かに配分する方式を質問ごとに決める。

- **2026-05 · [OccamToken: Efficient VLM Inference with Training-Free and Budget-Adaptive Token Pruning](2026-2605.29657-occamtoken-efficient-vlm-inference-with-training-free-and-budget-adaptiv.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の視覚トークン枝刈り（visual トークン 枝刈り）は、注意重みや特徴ベクトルの類似度で重要度を付け、得点の高い上位K個を残す方式が多い。高解像度のLLaVA-NeXTでは、元の2,880個から平均40個まで減らしても元モデルの集約性能の93.8%を維持する。

- **2026-05 · [LRCP: Low-Rank Compressibility Guided Visual Token Pruning for Efficient LVLMs](2026-2605.15621-lrcp-low-rank-compressibility-guided-visual-token-pruning-for-efficient-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚トークンの低ランク構造を主成分分析で捉え、支配的部分空間で説明できない射影残差の大きいトークンを残して他を統合することで、学習なしに視覚トークンを約9割削っても性能をほぼ保つ枝刈り方式。

- **2026-05 · [GRIP-VLM: Group-Relative Importance Pruning for Efficient Vision-Language Models](2026-2605.13375-grip-vlm-group-relative-importance-pruning-for-efficient-vision-language.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GRIP-VLM（Group-Relative Importance Pruning for Efficient Vision-Language Models）は、視覚言語モデル（VLM）へ渡す大量の画像トークンを、入力ごと・層ごと・保持予算ごとに選び直す手法である。

- **2026-05 · [Fre-Res: Frequency-Residual Video Token Compression for Efficient Video MLLMs](2026-2605.16366-fre-res-frequency-residual-video-token-compression-for-efficient-video-m.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動画対応マルチモーダルLLMにおいて、疎な高精細空間アンカーフレームと、フレーム間残差の時間方向DCT低周波成分を別経路で圧縮・統合するFre-Resを提案。Qwen2-VL-7Bの約2.1倍圧縮でNExT-QA 70.08、LongVideoBench 53.52、EgoSchema 63.58を達成。

- **2026-05 · [Focus-then-Context: Subject-Centric Progressive Visual Token Reduction for Vision-Language Models](2026-2605.20950-focus-then-context-subject-centric-progressive-visual-token-reduction-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SPprunerは視覚言語モデルの推論時に、質問と一致する画像領域だけでなく目立つ被写体とその周囲の構造情報を残す二段階の視覚トークン間引き方式である。

- **2026-05 · [EventPrune: Cascaded Event-Assisted Token Pruning for Efficient First-Person Dynamic Spatial Reasoning](2026-2605.19506-eventprune-cascaded-event-assisted-token-pruning-for-efficient-first-per.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  イベントカメラの動き信号で場面の固定とトークンの濾過と注意の補正を段階的に行う学習なし削減を提案し、2割の保持で全トークンを上回る精度と1.89倍の高速化、演算量52パーセント減を示した。

- **2026-05 · [ERASE: Eliminating Redundant Visual Tokens via Adaptive Two-Stage Token Pruning](2026-2605.09982-erase-eliminating-redundant-visual-tokens-via-adaptive-two-stage-token-p.md)**  
  実装：[✓](https://github.com/Tuna-Luna/ERASE) ・ リポジトリ内被引用：0  
  生画像の辺とエントロピーで画像ごとに保持率を決める第一段階と、浅い層では視覚手がかりを加え深い層では指示への関連だけで削る第二段階を組み合わせ、保持率二十五パーセントで元の精度の九十五点七〇パーセントを保った。

- **2026-04 · [When Is Thinking Enough? Early Exit via Sufficiency Assessment for Efficient Reasoning](2026-2604.06787-when-is-thinking-enough-early-exit-via-sufficiency-assessment-for-effici.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  内省信号の出現時だけモデル自身に思考の十分性を採点させて早期終了する学習不要の方式で、Qwen3で推論長を約3割削りながら正解率をほぼ維持した。

- **2026-04 · [Two-dimensional early exit optimisation of LLM inference](2026-2604.18592-two-dimensional-early-exit-optimisation-of-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、大規模言語モデルを文書分類器として使う場合に、何層まで計算するかと入力文書の何文目まで読むかを同時に制御する二次元早期終了（two-dimensional early exit）を提案する。

- **2026-04 · [ST-Prune: Training-Free Spatio-Temporal Token Pruning for Vision-Language Models in Autonomous Driving](2026-2604.19145-st-prune-training-free-spatio-temporal-token-pruning-for-vision-language.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動きと新しさを入れた時間剪定と、隣接視点との重なりを罰する空間剪定を二段に組み合わせ、学習なしでトークンを九割減らしても位置特定を含む運転課題の性能をほぼ保った時空間剪定の枠組み。

- **2026-04 · [Sink-Token-Aware Pruning for Fine-Grained Video Understanding in Efficient Video LLMs](2026-2604.20937-sink-token-aware-pruning-for-fine-grained-video-understanding-in-efficie.md)**  
  実装：[✓](https://github.com/rlqja1107/SToP) ・ リポジトリ内被引用：0  
  従来の枝刈りは視覚符号化器の注意重みを重要度の代用として使うが、注意が高い位置に意味情報が多いとは限らない。

- **2026-04 · [Reason Only When Needed: Efficient Generative Reward Modeling via Model-Internal Uncertainty](2026-2604.10072-reason-only-when-needed-efficient-generative-reward-modeling-via-model-i.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  難しい質問には段階的な思考連鎖（Chain-of-Thought、CoT）が有効だが、簡単な質問にも毎回長い思考を生成すると、回答に至るまでの生成トークン数と推論費用が増える。ただし最初の並列生成は無料ではなく、バッチやGPU配置を含む実システム全体で同じ節約率になるとは限らない。

- **2026-04 · [HeadRouter: Dynamic Head-Weight Routing for Task-Adaptive Audio Token Pruning in Large Audio Language Models](2026-2604.23717-headrouter-dynamic-head-weight-routing-for-task-adaptive-audio-token-pru.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  音声トークン枝刈りで全ヘッド平均をやめ、ヘッド選択性のばらつきから入力の意味系・音響系の度合いを推定してヘッド重みを動的に混合する学習不要の方式を提案し、30パーセント削除でも未圧縮を上回る品質を示した研究。

- **2026-04 · [DocPrune: Efficient Document Question Answering via Background, Question, and Comprehension-aware Token Pruning](2026-2604.22281-docprune-efficient-document-question-answering-via-background-question-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  背景・質問との無関係さ・モデルの理解度という三つの手掛かりで文書の視覚トークンを段階的に落とす学習不要の方式で、処理速度を約3倍にしながら精度も上げた。

- **2026-04 · [CLASP: Class-Adaptive Layer Fusion and Dual-Stage Pruning for Multimodal Large Language Models](2026-2604.12767-clasp-class-adaptive-layer-fusion-and-dual-stage-pruning-for-multimodal-.md)**  
  実装：[✓](https://github.com/Yunkaidang/CLASP) ・ リポジトリ内被引用：0  
  CLASP（Class-適応的 層 融合 and Dual-Stage Pruning）は、画像・動画を入力するマルチモーダルLLM（MLLM）の視覚トークンを、ユーザーの質問の種類に応じて削減する方式である。

- **2026-04 · [Beyond Attention Scores: SVD-Based Vision Token Pruning for Efficient Vision-Language Models](2026-2604.11530-beyond-attention-scores-svd-based-vision-token-pruning-for-efficient-vis.md)**  
  実装：[✓](https://github.com/anoncvlab/svdPrune) ・ リポジトリ内被引用：0  
  視覚トークンの重要度を注意スコアではなく特異値分解のレバレッジスコアで測り、支配的分散を担うトークンだけを残す学習不要の枝刈りで、32トークンや16トークンの極端な予算でも先行手法を上回る保持性能を示す。

- **2026-03 · [ReDiPrune: Relevance-Diversity Pre-Projection Token Pruning for Efficient Multimodal LLMs](2026-2603.24680-rediprune-relevance-diversity-pre-projection-token-pruning-for-efficient.md)**  
  実装：[✓](https://github.com/UA-CVML/ReDiPrune) ・ リポジトリ内被引用：0  
  射影の前の視覚特徴の上で、質問への関連と最大最小の多様性を組み合わせた得点でトークンを貪欲に選ぶ学習なしの間引きにより、動画では保持率一五パーセントで未間引きを二・〇ポイント上回る精度を保ちながら計算量を約六分の一へ減らし、画像でも保持率一〇パーセントで最良級の精度を維持した。

- **2026-03 · [ForensicZip: More Tokens are Better but Not Necessary in Forensic Vision-Language Models](2026-2603.12208-forensiczip-more-tokens-are-better-but-not-necessary-in-forensic-vision-.md)**  
  実装：[✓](https://github.com/laiyingxin2/ForensicZip) ・ リポジトリ内被引用：0  
  隣接フレーム間の対応をダミーノード付き生死最適輸送で解いて出現と消滅の費用を異常得点とし、高周波応答と掛けて改ざん証拠のトークンだけを残すことで、保持率十パーセントで二点九七倍高速化と計算量九十パーセント超削減をしながら検出性能を保った。

- **2026-03 · [ETA-VLA: Efficient Token Adaptation via Temporal Fusion and Intra-LLM Sparsification for Vision-Language-Action Models](2026-2603.25766-eta-vla-efficient-token-adaptation-via-temporal-fusion-and-intra-llm-spa.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数カメラの過去画像を視覚言語行動モデル（Vision-Language-Action モデル; VLA）へ入力すると、フレーム数とカメラ数に比例して視覚トークンが増える。主題は車両の制御アルゴリズムそのものよりも、VLAにおける視覚系列の効率的な処理である。

- **2026-03 · [Dynamic Token Compression for Efficient Video Understanding through Reinforcement Learning](2026-2603.26365-dynamic-token-compression-for-efficient-video-understanding-through-rein.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  フレーム間残差を驚きの信号として使う軽量な方策網に、品質と疎さの報酬による強化学習と疑似動画から実動画への段階的学習でトークンの残し方を学ばせ、強い圧縮でも無圧縮並み以上の品質と16倍の入力処理高速化を得た。

- **2026-03 · [Balancing Saliency and Coverage: Semantic Prominence-Aware Budgeting for Visual Token Compression in VLMs](2026-2603.14892-balancing-saliency-and-coverage-semantic-prominence-aware-budgeting-for-.md)**  
  実装：[✓](https://github.com/jayaylee/PromPrune) ・ リポジトリ内被引用：0  
  特異値のスペクトルエントロピーで画像ごとの意味の広がりを測り、固定予算を顕著さと被覆へ振り分けて二段で選ぶことで、エルラバネクスト七ビーで計算量八十八パーセント削減と入力処理二十二パーセント高速化をしながら元の精度の九十七点五パーセントを保った。

- **2026-02 · [SwiftVLM: Efficient Vision-Language Model Inference via Cross-Layer Token Bypass](2026-2602.03134-swiftvlm-efficient-vision-language-model-inference-via-cross-layer-token.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  落選した視覚トークンを捨てずに迂回させ、次の枝刈り層で表現を補正して再評価する学習不要の枝刈りで、トークンを3分の1に減らしても位置特定の精度を無枝刈りの約87パーセントに保った。

- **2026-02 · [QTALE: Quantization-Robust Token-Adaptive Layer Execution for LLMs](2026-2602.10431-qtale-quantization-robust-token-adaptive-layer-execution-for-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの推論負荷を下げるには、重みを少ないビットで保持する量子化（量子化）と、トークンごとに不要なTransformer層を省く動的層実行（トークン-適応的 層 execution）が補完的である。

- **2026-02 · [POP: Online Structural Pruning Enables Efficient Inference of Large Foundation Models](2026-2602.06822-pop-online-structural-pruning-enables-efficient-inference-of-large-found.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  入力処理でチャネルを保持・候補・削除へ三分割し、生成中は候補の中だけでマスクを作り直す学習なしの動的構造枝刈りで、Llama2-7Bを密比1.14倍（削減20%）から1.38倍（削減40%）へ速くし、追加計算は全結合の2.85%、事前準備はゼロを実現した。

- **2026-02 · [DySL-VLA: Efficient Vision-Language-Action Model Inference via Dynamic-Static Layer-Skipping for Robot Manipulation](2026-2602.22896-dysl-vla-efficient-vision-language-action-model-inference-via-dynamic-st.md)**  
  実装：[✓](https://github.com/PKU-SEC-Lab/DYSL_VLA) ・ リポジトリ内被引用：0  
  DySL-VLAは、視覚言語行動モデル（Vision-Language-Action モデル; VLA）の大規模言語モデル（Large Language モデル; LLM）基盤に対し、必要な層だけを実行してロボット制御の推論遅延を削減する方式である。

- **2026-02 · [ConsensusDrop: Fusing Visual and Cross-Modal Saliency for Efficient Vision Language Models](2026-2602.00946-consensusdrop-fusing-visual-and-cross-modal-saliency-for-efficient-visio.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ConsensusDropは、言語モデルに入る前に質問依存の画像顕著性を近似して取得し、視覚エンコーダ由来の顕著性と統合する。原著Table 1では、LLaVA-1.5-7Bの視覚トークン576個を32個へ削減したとき、九つの画像ベンチマークの集計精度が基準モデルの90.5%となり、TTFTは106.4msから60.0ms（1.77倍）へ短縮された。

- **2026-01 · [Triage: Hierarchical Visual Budgeting for Efficient Video Reasoning in Vision-Language Models](2026-2601.22959-triage-hierarchical-visual-budgeting-for-efficient-video-reasoning-in-vi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  フレーム選択の重要度をトークン配分へ引き継ぐ階層的な視覚予算配分で、動画推論のトークンを学習なしに削る。保持率を半分にしても精度はむしろ上がる条件がある。

- **2026-01 · [Efficient Token Pruning for LLaDA-V](2026-2601.20168-efficient-token-pruning-for-llada-v.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散型の視覚言語モデルLLaDA-Vでは意味の集約が中層から深層で遅れて起きることを注意の実測で示し、最初の拡散ステップの中深層で視覚トークンを間引くことで、計算量を最大63パーセント減らしながら平均で相対性能95パーセント台を保つ枝刈り法。

- **2026-01 · [ChunkWise LoRA: Adaptive Sequence Partitioning for Memory-Efficient Low-Rank Adaptation and Accelerated LLM Inference](2026-2601.21109-chunkwise-lora-adaptive-sequence-partitioning-for-memory-efficient-low-r.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低ランク適応（LoRA）は、事前学習済みの重みを固定し、少数の低ランク行列を追加学習することで、モデルの更新費用を抑える。原著表Iでは、LLaMA-7Bを用いた比較で、通常のモデルが22.5ms/トークン、ピークGPUメモリ14.6GBに対し、提案方式は14.9ms/トークン、9.1GBを報告する。

- **2026-01 · [CAPA: Contribution-Aware Pruning and FFN Approximation for Efficient Large Vision-Language Models](2026-2602.00247-capa-contribution-aware-pruning-and-ffn-approximation-for-efficient-larg.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意確率に値ベクトルの大きさを掛けた注意寄与で視覚トークンを選び直し、中間層のほぼ線形な全結合変換を要素ごとのスケーリングへ置き換えることで、視覚トークン25パーセント保持でも精度を保ち理論計算量を78パーセント減らす二重の効率化。

- **2025-12 · [Token Expand-Merge: Training-Free Token Compression for Vision-Language-Action Models](2025-2512.09927-token-expand-merge-training-free-token-compression-for-vision-language-a.md)**  
  実装：[✓](https://github.com/Jasper-aaa/TEAM-VLA) ・ リポジトリ内被引用：0  
  疎な言語・画像類似度を密度で広げて前景を復元する前段の枝刈りと、行動に応答するトークンへ残りを畳み込む中間層マージを組み合わせ、学習なしでLIBEROの成功率を保ちながら遅延を約1.5倍速くする視覚・言語・行動モデル向け圧縮。

- **2025-12 · [StreamingAssistant: Efficient Visual Token Pruning for Accelerating Online Video Understanding](2025-2512.12560-streamingassistant-efficient-visual-token-pruning-for-accelerating-onlin.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  隣接トークンとの類似度で空間冗長性を測り、市松マスクで安全に並列枝刈りする動画向けトークン削減方式で、9割超のトークンを落としても精度をほぼ保った。

- **2025-12 · [Mixture of Attention Schemes (MoAS): Learning to Route Between MHA, GQA, and MQA](2025-2512.20650-mixture-of-attention-schemes-moas-learning-to-route-between-mha-gqa-and-.md)**  
  実装：[✓](https://github.com/Esmail-ibraheem/Mixture-of-Attention-Schemes-MoAS) ・ リポジトリ内被引用：0  
  標準の多頭注意（Multi-Head 注意機構; MHA）は各問い合わせ頭に独立したキー・バリュー（Key-Value; KV）頭を持ち、表現力が高い一方、生成時のKVキャッシュが大きくなる。これは条件付き計算の可能性を示す探索的結果であって、LLM推論の実用的高速化を実証した結果ではない。

- **2025-12 · [Glance2Gaze: Efficient Vision-Language Models from Glance Fusion to Gaze Compression](2025-5f0897915cbf-glance2gaze-efficient-vision-language-models-from-glance-fusion-to-gaze-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  高解像度画像や動画では視覚トークン数が大きくなり、言語モデルの注意計算、鍵・値キャッシュ（KV キャッシュ）、初回トークン生成までの遅延が増加する。Glance2Gazeは、最初に画像全体を眺めて必要な細部へ視線を絞るという着想を二つの計算機構へ具体化する。

### 2年前（2024-12〜2025-11）

- **2025-03 · [DivPrune: Diversity-based Visual Token Pruning for Large Multimodal Models](2025-2503.02175-divprune-diversity-based-visual-token-pruning-for-large-multimodal-model.md)**  
  実装：[✓](https://github.com/vbdi/divprune) ・ リポジトリ内被引用：109  
  提案方式は、情報量が高そうな個々のトークンを選ぶのではなく、選んだトークン同士が似過ぎないようにすることで、短い視覚列に異なる意味的領域を残そうとする。提案された距離選択を、言語モデルの最初の層より前、または途中層の視覚対応隠れ状態へ挿入できるが、主要な実験で最も良好だったのは最初の層の前に削減する構成である。

- **2025-02 · [Stop Looking for Important Tokens in Multimodal Language Models: Duplication Matters More](2025-2502.11494-stop-looking-for-important-tokens-in-multimodal-language-models-duplicat.md)**  
  実装：[✓](https://github.com/ZichenWen1/DART) ・ リポジトリ内被引用：81  
  従来は注意重みを使って重要そうなトークンを残す方式が多かった。LLaVA-Next-7Bの画像トークンを2880から320へ削減した条件では、総推論時間が36分16秒から18分13秒、事前充填時間が22分51秒から7分38秒へ短縮し、鍵値キャッシュは1512.1MBから168.0MBへ減少した。

- **2025-04 · [Dynamic Early Exit in Reasoning Models](2025-2504.15895-dynamic-early-exit-in-reasoning-models.md)**  
  実装：[✓](https://github.com/iie-ycx/DEER) ・ リポジトリ内被引用：67  
  DEERは推論途中で最終回答を試し、自己評価の確信度が高ければ思考連鎖を終了し、低ければ元地点から続行する。追加学習なしで過剰な再検討を減らす。

- **2025-06 · [Beyond Attention or Similarity: Maximizing Conditional Diversity for Token Pruning in MLLMs](2025-2506.10967-beyond-attention-or-similarity-maximizing-conditional-diversity-for-toke.md)**  
  実装：[✓](https://github.com/Theia-4869/CDPruner) ・ リポジトリ内被引用：47  
  本論文は、質問に必要な画像情報を残しながら視覚トークンを減らすCDPrunerを提案する。LLaVA-1.5-7Bで視覚トークン576個から128個へ減らすと、10種類の評価指標の平均相対性能は99.0%である。

- **2024-12 · [Dynamic-LLaVA: Efficient Multimodal Large Language Models via Dynamic Vision-language Context Sparsification](2024-2412.00876-dynamic-llava-efficient-multimodal-large-language-models-via-dynamic-vis.md)**  
  実装：[✓](https://github.com/Osilly/dynamic_llava) ・ リポジトリ内被引用：27  
  動的-LLaVAは、マルチモーダル大規模言語モデル（マルチモーダル Large Language モデル; MLLM）の高速化を、画像トークンだけの削減ではなく「画像文脈と生成済み言語文脈の両方を、推論段階に応じて動的に疎化する」問題として扱う。予測は一度だけ行い、その保持/削除決定を後続層すべてで共有する。

- **2025-05 · [AdaptThink: Reasoning Models Can Learn When to Think](2025-2505.13417-adaptthink-reasoning-models-can-learn-when-to-think.md)**  
  実装：[✓](https://github.com/THU-KEG/AdaptThink) ・ リポジトリ内被引用：25  
  AdaptThinkは、問題ごとに「思考あり（Thinking）」と「思考なし（NoThinking）」のどちらで回答するかをモデル自身が選択できるよう、強化学習（Reinforcement Learning; RL）で訓練する方式である。

- **2025-04 · [Reasoning Models Know When They're Right: Probing Hidden States for Self-Verification](2025-2504.05419-reasoning-models-know-when-they-re-right-probing-hidden-states-for-self-.md)**  
  実装：✓ ・ リポジトリ内被引用：25  
  長い思考連鎖（Chain of Thought; CoT）を生成する推論モデルは、最初に正解へ到達しても別の推論経路を探索し、同じ問題を何度も検証することがある。オンラインで検証器を挿入したサービングシステムの最初のトークン遅延、処理率、VRAM消費、GPU時間を直接測定した結果ではない。

- **2024-12 · [D-LLM: A Token Adaptive Computing Resource Allocation Strategy for Large Language Models](2024-d-llm-a-token-adaptive-computing-resource-allocation-strategy-for-large-language.md)**  
  実装：[✓](https://github.com/Jyk-122/D-LLM) ・ リポジトリ内被引用：15  
  D-LLMは、大規模言語モデルのすべてのトークンに同じ層数の計算を行う必要はないという観点から、各トークン・各Transformer層でその層を実行するか省略するかを学習する動的深度方式である。代表的な設定では、完全な層を実行するLoRA基準の約52～59%の浮動小数点演算量で、多くの課題の品質を維持した。

- **2025-03 · [Adaptive Layer-skipping in Pre-trained LLMs](2025-2503.23798-adaptive-layer-skipping-in-pre-trained-llms.md)**  
  実装：[✓](https://github.com/luoxuan-cs/Flexidepth) ・ リポジトリ内被引用：12  
  FlexiDepthは、すでに学習された大規模言語モデルの重みを変更せず、出力トークンごとに必要な層の計算量を変える手法である。原著のLlama-3-8B-Instruct（32層）では、平均8層を省いても6つの評価課題における平均性能保持率が100.7%となり、固定層省略方式より高い品質を示す。

- **2025-05 · [WINA: Weight Informed Neuron Activation for Accelerating Large Language Model Inference](2025-2505.19427-wina-weight-informed-neuron-activation-for-accelerating-large-language-m.md)**  
  実装：[✓](https://github.com/microsoft/wina) ・ リポジトリ内被引用：8  
  WINAは、既存の大規模言語モデル（LLM）を再学習せず、各層で計算に参加させる活性成分を選択する疎活性化方式である。代表例としてLlama-2-7Bの常識推論8課題平均では、65%の活性疎性でWINAが65.14、TEALが61.07、R-Sparseが59.37となった。

- **2025-10 · [VisionSelector: End-to-End Learnable Visual Token Compression for Efficient Multimodal LLMs](2025-2510.16598-visionselector-end-to-end-learnable-visual-token-compression-for-efficie.md)**  
  実装：[✓](https://github.com/JulietChoo/VisionSelector) ・ リポジトリ内被引用：7  
  言語モデル側はそれらを文章トークンとともに入力として処理するため、画像の情報量が増えるほど初期入力計算（プリフィル）の時間と中間状態のメモリが増える。視覚トークンを一部だけ残せば高速になるが、単純に注意スコアが大きい位置を選ぶと、内容上重要でない先頭トークンへ注意が集中する「注意の吸い込み（注意機構 sink）」や、文字・図表の細部が欠落する問題が起きる。

- **2025-03 · [AdaReTaKe: Adaptive Redundancy Reduction to Perceive Longer for Video-language Understanding](2025-2503.12559-adaretake-adaptive-redundancy-reduction-to-perceive-longer-for-video-lan.md)**  
  実装：[✓](https://github.com/SCZwangxiao/video-FlexReduc) ・ リポジトリ内被引用：7  
  動画を長くするほど事前充填で扱う系列が増え、言語モデルの鍵・値キャッシュ（KVキャッシュ）がGPUメモリを圧迫する。すべてのフレームを同じ割合で圧縮すると、静止区間へ不要な容量を割り当てる一方、質問に必要な短い場面の情報を失う。これは処理可能な動画情報量と理解精度の結果であり、トークン生成速度が同倍率で向上するという主張ではない。

- **2025-07 · [DiffSkip: Differential Layer Skipping in Large Language Models](2025-diffskip-differential-layer-skipping-in-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  大規模言語モデルは、次の単語を推測するたびに、難しい計算を要する単語にも文脈からほぼ写すだけの単語にも同じ数の変換層を適用する。DiffSkipは、トークンと層の組ごとに、後続のフィードフォワードネットワーク（FFN）を実行するか、軽量な補正器で代替するかを判断する手法である。

- **2025-01 · [Instruction-Following Pruning for Large Language Models](2025-2501.02086-instruction-following-pruning-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  指示追従枝刈り（Instruction-Following Pruning、IFPruning）は、利用者の指示文から小型の疎性予測器が必要なフィードフォワード層（FFN）の中間次元を選び、その指示に対する応答の復号中は同じ部分ネットワークを固定して実行する手法である。

- **2025-10 · [Learning to Inference Adaptively for Multimodal Large Language Models](2025-2503.10905-learning-to-inference-adaptively-for-multimodal-large-language-models.md)**  
  実装：[✓](https://github.com/zhuoyan-xu/AdaLLaVA) ・ リポジトリ内被引用：4  
  一般的な軽量化方式では、視覚トークン削除数や層構成が推論開始前に固定され、要求ごとの計算予算や画像・質問の難しさに合わせて変更できない。LLaVA-1.5の7B構成で層単位版を60%予算にすると、論文のMME計測ではプリフィル計算量が8.6兆から5.1兆浮動小数点演算へ、時間が81msから49msへ減り、VQAv2正解率は78.5から75.0へ下がる。

- **2025-08 · [AdaptInfer: Adaptive Token Pruning for Vision-Language Model Inference via Dynamical Text Guidance](2025-2508.06084-adaptinfer-adaptive-token-pruning-for-vision-language-model-inference-vi.md)**  
  実装：[✓](https://github.com/weiczh02/AdaptInfer-base) ・ リポジトリ内被引用：4  
  AdaptInferは、質問文のうち画像のどの部分を見るべきかを決める文章トークンが、Transformerの深さに応じて変わることを利用し、各枝刈り層で文章の重要度を再計算して画像トークンを選ぶ方式である。

- **2025-07 · [La RoSA: Enhancing LLM Efficiency via Layerwise Rotated Sparse Activation](2025-2507.01299-la-rosa-enhancing-llm-efficiency-via-layerwise-rotated-sparse-activation.md)**  
  実装：[✓](https://github.com/alibaba/EfficientAI) ・ リポジトリ内被引用：4  
  重みの量子化や枝刈りとは別に、入力活性の多くをゼロにできれば、ゼロに対応する重み列を読み込まずに済む。論文の代表例では、LLaMA2-7Bのモデル全体の活性疎性40%で困惑度の悪化が5.47から5.64への0.17にとどまり、7種のゼロ例示タスクの平均得点は66.69から66.15への0.54ポイント低下である。

- **2025-03 · [Lifting the Veil on Visual Information Flow in MLLMs: Unlocking Pathways to Faster Inference](2025-2503.13108-lifting-the-veil-on-visual-information-flow-in-mllms-unlocking-pathways-.md)**  
  実装：[✓](https://github.com/ustc-hyin/HiMAP) ・ リポジトリ内被引用：4  
  画像トークンの視覚情報フローが浅い層では指示トークンへの注入、深い層では画像トークン同士の集約へ転換することを突き止め、層ごとに違う重要度基準で二段階に画像トークンを落とすHiMAPで計算量を約65%以上減らすマルチモーダル推論の高速化。

- **2025-05 · [Why 1 + 1 < 1 in Visual Token Pruning: Beyond Naive Integration via Multi-Objective Balanced Covering](2025-2505.10118-why-1-1-1-in-visual-token-pruning-beyond-naive-integration-via-multi-obj.md)**  
  実装：[✓](https://github.com/YChenL/MoB) ・ リポジトリ内被引用：3  
  視覚トークン枝刈りの2つの目的が予算を取り合うことを理論で示し、残す予算の配分として解く学習不要の方式で、トークンを約9分の1に減らしても性能の96.4パーセント保持を示した。

- **2025-05 · [ToDRE: Effective Visual Token Pruning via Token Diversity and Task Relevance](2025-2505.18757-todre-effective-visual-token-pruning-via-token-diversity-and-task-releva.md)**  
  実装：[✓](https://github.com/Yrdal3910/ToDRE) ・ リポジトリ内被引用：3  
  既存の削減方式は、視覚トークン同士の類似度か、テキストと視覚の注意スコアのどちらか一方を重複の指標として使うことが多い。

- **2025-09 · [HERO: Rethinking Visual Token Early Dropping in High-Resolution Large Vision-Language Models](2025-2509.13067-hero-rethinking-visual-token-early-dropping-in-high-resolution-large-vis.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  HEROは、高解像度画像を複数の局所タイルと全体サムネイルへ分割して処理するVision-Language モデル（VLM）向けに、LLMへ渡す前の視覚トークンを選別する追加学習不要の圧縮手法である。

- **2025-08 · [ILRe: Intermediate Layer Retrieval for Context Compression in Causal Language Models](2025-2508.17892-ilre-intermediate-layer-retrieval-for-context-compression-in-causal-lang.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Intermediate 層 Retrieval（ILRe）は、長大な入力を全層へそのまま通す代わりに、選択した中間デコーダ層までの処理で原文から重要トークンを選び直し、短いプロンプトとして再投入する文脈圧縮方式である。

- **2025-08 · [Attention Debiasing for Token Pruning in Vision–Language Models](2025-2508.17807-attention-debiasing-for-token-pruning-in-vision-language-models.md)**  
  実装：[✓](https://github.com/intcomp/attention-bias) ・ リポジトリ内被引用：2  
  多くの視覚トークンが冗長なので、言語モデルの初期層で重要度の低いトークンを捨てれば、以後の注意機構やKV保持の負荷を下げられる。

- **2025-03 · [PromptDistill: Query-based Selective Token Retention in Intermediate Layers for Efficient Large Language Model Inference](2025-2503.23274-promptdistill-query-based-selective-token-retention-in-intermediate-laye.md)**  
  実装：[✓](https://github.com/declare-lab/PromptDistill) ・ リポジトリ内被引用：2  
  長文の入力を持つ大規模言語モデルでは、プロンプトの全位置を全Transformer層で処理すると、入力長に伴って注意計算と中間状態の保存量が増える。PromptDistillは、最初の数層だけ全位置を処理した後、入力の最後の位置のqueryと各位置のkeyから選んだ重要位置に計算を集中する。< の本文§2–3とTable 1–5を照合した。

- **2025-03 · [Position-Aware Depth Decay Decoding (D³): Boosting Large Language Model Inference Efficiency](2025-2503.08524-position-aware-depth-decay-decoding-boosting-large-language-model-inference-effi.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  位置考慮型深さ減衰復号（Position-Aware 深度減衰 デコード; D³）は、大規模言語モデルの自己回帰生成で、出力トークンの位置に応じて実行するTransformer層数を減らす方式である。

- **2025-03 · [Multi-Cue Adaptive Visual Token Pruning for Large Vision-Language Models](2025-2503.08019-multi-cue-adaptive-visual-token-pruning-for-large-vision-language-models.md)**  
  実装：[✓](https://github.com/bzluan/AdaptPrune) ・ リポジトリ内被引用：2  
  画像を扱う大規模視覚言語モデル（LVLM）では、視覚エンコーダが作る数百から数千の画像パッチ表現が言語モデルへトークンとして挿入される。画像が高解像度になると、視覚トークンは言語側の自己注意やFFNにも流れ、プリフィル計算量、後続のKVキャッシュ容量、生成時の注意計算に影響する。画像トークンの一部を早い層で取り除けば、後続層の計算と記憶を減らせる。

- **2025-02 · [Infinite Retrieval: Attention Enhanced LLMs in Long-Context Processing](2025-2502.12962-infinite-retrieval-attention-enhanced-llms-in-long-context-processing.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  単純な窓移動では古い区間を忘れ、KVキャッシュ圧縮では過去情報の一部を固定された埋め込み表現として保存するため、質問に必要な文を失うことがある。

- **2025-01 · [RedundancyLens: Revealing and Exploiting Visual Token Processing Redundancy for Efficient Decoder-Only MLLMs](2025-2501.19036-redundancylens-revealing-and-exploiting-visual-token-processing-redundan.md)**  
  実装：[✓](https://github.com/L-Hugh/RedundancyLens) ・ リポジトリ内被引用：2  
  この構成は実装が単純で精度も高い一方、画像由来のトークン数が増えると、LLMのself-注意機構とFFNの両方で大量の演算が発生する。約半数の層へ演算削減を適用すると、FLOPs比が約71〜72%に下がり、元モデルに近い品質を維持する。

- **2025-11 · [Conv-Basis: A New Paradigm for Efficient Attention Inference and Gradient Computation in Transformers](2025-a7d4659aa00f-conv-basis-a-new-paradigm-for-efficient-attention-inference-and-gradient.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  提案方式は、相対位置差に沿った対角線状の反復パターンを「畳み込み基底（conv basis）」として表し、各基底に対応する畳み込みとVの積を高速フーリエ変換（Fast Fourier Transform; FFT）で計算する。

- **2025-10 · [MixReasoning: Switching Modes to Think](2025-2510.06052-mixreasoning-switching-modes-to-think.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  MixReasoningは、問題全体を「考える／考えない」に二分するのではなく、一つの長い推論軌跡の中で難しい部分だけ詳細思考を行う方式である。Qwen3-8Bの4課題平均では、元モデルのpass@1 77.44、平均生成7027トークンに対し、MixReasoningはpass@1 78.29、5120トークン（約28%減）となる。

- **2025-07 · [SimLens for Early Exit in Large Language Models: Eliciting Accurate Latent Predictions with One More Token](2025-2507.17618-simlens-for-early-exit-in-large-language-models-eliciting-accurate-laten.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  中間層で開始トークンと候補回答トークンの2個だけを残して上位層へ通す学習不要の読み出しと、それを蒸留した線形監視器によるエントロピー早期終了で、単一トークン決定課題の推論を速くする方式。

- **2025-06 · [FREE: Fast and Robust Vision Language Models with Early Exits](2025-2506.06884-free-fast-and-robust-vision-language-models-with-early-exits.md)**  
  実装：[✓](https://github.com/Div290/FREE) ・ リポジトリ内被引用：1  
  視覚言語モデルの途中層に、最終層の分類器を共有し敵対的学習で最終層の表現をまねる早期終了口を付け、簡単なトークンを浅い層で確定させることで、NoCapsで品質を保ったまま1.51倍の高速化を示した。

- **2025-05 · [Scalable LLM Reasoning Acceleration with Low-rank Distillation](2025-2505.07861-scalable-llm-reasoning-acceleration-with-low-rank-distillation.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Capreseは、大規模言語モデルのフィードフォワードネットワーク（FFN）を疎化したとき、長い数学的推論で顕著になる精度低下を、小さな低ランク補正で回復する手法である。

- **2025-05 · [Beyond Hard and Soft: Hybrid Context Compression for Balancing Local and Global Information Retention](2025-2505.15774-beyond-hard-and-soft-hybrid-context-compression-for-balancing-local-and-.md)**  
  実装：[✓](https://github.com/Xnhyacinth/HyCo2) ・ リポジトリ内被引用：1  
  HyCo2（Hybrid Context Compression）は、長文脈の検索拡張生成（Retrieval-Augmented Generation; RAG）で、必要な情報を保持しながら入力トークン数を減らす圧縮方式である。デフォルトでは16個の潜在クエリと、原文トークンの上位10%を保持する設定である。

- **2025-04 · [Saliency-driven Dynamic Token Pruning for Large Language Models](2025-2504.04514-saliency-driven-dynamic-token-pruning-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  KVキャッシュを削減する方式は、生成段階のメモリと注意計算を減らす一方、既に全入力を処理した後でKVを捨てるだけではプリフィル計算を取り戻せない。

- **2025-03 · [Local Information Matters: Inference Acceleration For Grounded Conversation Generation Models Through Adaptive Local-Aware Token Pruning](2025-2503.23959-local-information-matters-inference-acceleration-for-grounded-conversati.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  提案する適応的局所認識トークン剪定は、画像を複数の意味的にまとまった領域へ分け、領域ごとに保持するトークンを確保する。OMG-LLaVAでも同程度の削減条件で、検証集合のAPが24.1から26.2、領域の重なり率が58.0から61.0へ改善した。

- **2025-10 · [LiteStage: Latency-aware Layer Skipping for Multi-stage Reasoning](2025-2510.14211-litestage-latency-aware-layer-skipping-for-multi-stage-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LiteStageは、複雑な質問を短い複数段階に分けて解く小型言語モデルについて、各段階に同じ数の層スキップを適用するのではなく、段階ごとの正答率と実際の推論遅延を測定してスキップ予算を配分する手法である。

- **2025-10 · [FLoC: Facility Location-Based Efficient Visual Token Compression for Long Video Understanding](2025-2511.00141-floc-facility-location-based-efficient-visual-token-compression-for-long.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FLoCは、長時間動画から抽出した大量の視覚トークンを、指定されたトークン数の予算内で代表性と多様性の両方を保つ部分集合へ圧縮する方式である。

- **2025-10 · [APCE: Adaptive Progressive Context Expansion for Long Context Processing](2025-2510.12051-apce-adaptive-progressive-context-expansion-for-long-context-processing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  適応的 Progressive Context Expansion（APCE）は、長い入力を最初から全てTransformerへ通す代わりに、質問と意味的に近いchunkだけを選んでプリフィルし、生成が進むにつれて参照chunkを入れ替える方式である。

- **2025-09 · [Pyramid Token Pruning for High-Resolution Large Vision-Language Models via Region, Token, and Instruction-Guided Importance](2025-2509.15704-pyramid-token-pruning-for-high-resolution-large-vision-language-models-v.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Pyramid Token Pruning（PTP）は、追加学習なしで、画像全体に対するタイルの重要度、タイル内部のパッチ重要度、ユーザーの指示文に対するパッチ関連度を三段階で組み合わせる方式である。

- **2025-09 · [EfficientUICoder: Efficient MLLM-based UI Code Generation via Input and Output Token Compression](2025-2509.12159-efficientuicoder-efficient-mllm-based-ui-code-generation-via-input-and-o.md)**  
  実装：[✓](https://github.com/WebPAI/EfficientUICoder) ・ リポジトリ内被引用：0  
  本研究は、ウェブ画面の画像を入力してHTMLとCSSを生成するUI-to-コードの推論費用を、画像側とコード側の両方から削減する方式である。

- **2025-09 · [Efficient Large Language Models with Zero-Shot Adjustable Acceleration](2025-2509.01190-efficient-large-language-models-with-zero-shot-adjustable-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究の狙いは、推論時にTransformerの層間を通過する隠れ活性の数を削減しながら、どの程度の削減を行うかを微調整後に変更できるようにすることである。GPT-2のIMDB分類では最大11倍の加速設定で正解率が92.40%から86.48%へ低下する。

- **2025-08 · [GLASS: Global-Local Aggregation for Inference-time Sparsification of LLMs](2025-2508.14302-glass-global-local-aggregation-for-inference-time-sparsification-of-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  一方、GRIFFINなどの学習不要な方式は、プリフィル中に観測した活性から「生成中に使うニューロン」を決め、その固定マスクをデコードで再利用する。論文v2では、50% FFN疎化の長文生成でGRIFFINよりPPLを最大45.10%、Kullback–Leibler divergence（KLD）を最大25.73%減らした。

- **2025-06 · [Task-Related Token Compression in Multimodal Large Language Models from an Explainability Perspective](2025-2506.01097-task-related-token-compression-in-multimodal-large-language-models-from-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この研究は、画像や動画を扱うマルチモーダル大規模言語モデル（MLLM）で、ユーザーの指示に関係しない視覚トークンをLLM入力段階で取り除くための方式を提案する。

- **2025-06 · [Fine-grained Token Allocation Via Operation Pruning for Efficient MLLMs](2025-2507.02909-fine-grained-token-allocation-via-operation-pruning-for-efficient-mllms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の視覚トークン枝刈りは、重要と判定した少数のトークンを残すが、どの層・どのモジュールも同じ数の視覚トークンを処理しがちである。LLaVA-NeXT-7Bの実験では、視覚トークンを一律に減らす比較方式より同一演算予算で精度を保ち、特定の強圧縮条件ではTFLOPs86%削減とプリフィル CUDA遅延83%削減を平均性能約1%低下で報告する。

- **2025-05 · [STAR: Stage-Wise Attention-Guided Token Reduction for Efficient Large Vision-Language Models Inference](2025-2505.12359-star-stage-wise-attention-guided-token-reduction-for-efficient-large-vis.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  STAR（Stage-Wise 注意機構-Guided Token Reduction）は、画像とテキストを扱う大規模Vision-Language モデル（LVLM）の推論で、視覚トークンを視覚エンコーダ直後とLLMデコーダ中間層の二段階で削る学習不要の手法である。

- **2025-05 · [Sparsified State-Space Models are Efficient Highway Networks](2025-2505.20698-sparsified-state-space-models-are-efficient-highway-networks.md)**  
  実装：[✓](https://github.com/woominsong/Simba) ・ リポジトリ内被引用：0  
  Simbaは、Mambaなどの状態空間モデル（SSM）で、入力系列のトークンを層が深くなるほど段階的に間引く推論時の疎化手法である。付録の8枚のRTX2080 Ti上のPyTorch実装では、Mamba-2.8Bの入力長3Kの推論時間5.819秒に対しSimbaは3.217秒で、約1.81倍の高速化である。

- **2025-04 · [DYNAMAX: Dynamic computing for Transformers and Mamba based architectures](2025-2504.20922-dynamax-dynamic-computing-for-transformers-and-mamba-based-architectures.md)**  
  実装：[✓](https://github.com/Xigm/DYNAMAX) ・ リポジトリ内被引用：0  
  デコーダのみTransformerとMambaの後半層に早期終了分類器を付け、状態を持てるMambaブロック型分類器と上位候補を許す蒸留学習で、層の枝刈りより精度を保ちながらトークンごとの計算を動的に打ち切る枠組み。

- **2024-12 · [COSEE: Consistency-Oriented Signal-Based Early Exiting via Calibrated Sample Weighting Mechanism](2024-2412.13236-cosee-consistency-oriented-signal-based-early-exiting-via-calibrated-sam.md)**  
  実装：[✓](https://github.com/He-Jianing/COSEE) ・ リポジトリ内被引用：0  
  学習時に複数の閾値で終了過程を模擬し、サンプルが終了しやすい層の近くの分類器へ損失の重みを寄せることで、高速化率を推論時に変えられるまま学習と推論の一致を取る早期終了の学習枠組み。

### 3年前（2023-12〜2024-11）

- **2024-03 · [An Image is Worth 1/2 Tokens After Layer 2: Plug-and-Play Inference Acceleration for Large Vision-Language Models](2024-2403.06764-an-image-is-worth-1-2-tokens-after-layer-2-plug-and-play-inference-accel.md)**  
  実装：[✓](https://github.com/pkunlp-icler/FastV) ・ リポジトリ内被引用：281  
  LLaVA-1.5では一枚の336×336画像が576トークンになり、高解像度化や動画の複数フレーム処理では数千トークンへ増える。初期層では画像情報が広く注意される一方、深い層では少数のシステム指示や文章トークンへ注意が集中し、画像トークン一個当たりの注意効率が非常に低くなる。代表設定は二層後に視覚トークンの50%を削除する方式である。

- **2024-10 · [SparseVLM: Visual Token Sparsification for Efficient Vision-Language Model Inference](2024-2410.04417-sparsevlm-visual-token-sparsification-for-efficient-vision-language-mode.md)**  
  実装：[✓](https://github.com/Gumpest/SparseVLMs) ・ リポジトリ内被引用：181  
  SparseVLMは、視覚言語モデル（VLM）の入力画像から生じる大量の視覚トークンを、現在の質問に必要な情報をできるだけ残しながら削減する追加学習不要の方式である。

- **2024-03 · [LLaVA-PruMerge: Adaptive Token Reduction for Efficient Large Multimodal Models](2024-2403.15388-llava-prumerge-adaptive-token-reduction-for-efficient-large-multimodal-m.md)**  
  実装：[✓](https://github.com/42Shawn/LLaVA-PruMerge) ・ リポジトリ内被引用：179  
  LLaVA-PruMergeは、画像を大規模言語モデルへ渡す際の視覚トークン数を削減する方式である。LLaVA-1.5は336×336画素の画像から24×24個、すなわち576個の視覚トークンを生成する。

- **2024-08 · [LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding](2024-layerskip-enabling-early-exit-inference-and-self-speculative-decoding.md)**  
  実装：[✓](https://github.com/facebookresearch/LayerSkip) ・ リポジトリ内被引用：174  
  LayerSkipは、大規模言語モデルの全ての層を毎トークン実行する代わりに、浅い層から次トークンを予測できるよう学習し、その予測を同じモデルの残りの層で検証する方式である。下書きモデルの生成結果を大きなモデルで一括検証することで生成時間を短縮できるが、二つのモデルの重みや鍵・値キャッシュを管理する必要がある。

- **2024-10 · [PyramidDrop: Accelerating Your Large Vision-Language Models via Pyramid Visual Redundancy Reduction](2024-2410.17247-pyramiddrop-accelerating-your-large-vision-language-models-via-pyramid-v.md)**  
  実装：[✓](https://github.com/Cooperx521/PyramidDrop) ・ リポジトリ内被引用：132  
  大規模視覚言語モデル（Large Vision-Language モデル; LVLM）は、画像を数百から数千の画像トークンへ変換して、文章の質問と一緒に言語モデルへ入力する。画像解像度が上がると画像トークンが増え、注意計算と全結合層の演算量が大きくなる。複数の視覚言語ベンチマークで品質は概ね維持されるが、個別の高解像度課題では小さな低下もある。

- **2024-04 · [Mixture-of-Depths: Dynamically allocating compute in transformer-based language models](2024-2404.02258-mixture-of-depths-dynamically-allocating-compute-in-transformer-based-la.md)**  
  実装：✓ ・ リポジトリ内被引用：86  
  そのため、簡単な予測位置も難しい予測位置も同じ計算を受ける。方式の要点は、処理するトークンの「個数」kを事前に固定し、「どのトークンか」だけを学習済みルータが動的に選ぶ点にある。論文の代表構成では系列長2048に対し、一つおきの層で上位256トークン、すなわち12.5%だけを自己注意とMLPへ通す。

- **2024-11 · [DyCoke: Dynamic Compression of Tokens for Fast Video Large Language Models](2024-2411.15024-dycoke-dynamic-compression-of-tokens-for-fast-video-large-language-model.md)**  
  実装：[✓](https://github.com/KD-TAO/DyCoke) ・ リポジトリ内被引用：65  
  DyCokeは、動画を入力とする大規模言語モデルが多数のフレームを視覚トークンへ変換する際に生じる、注意計算と鍵・値（KV）キャッシュの増大を抑える学習不要の圧縮方式である。原著のLLaVA-OneVision 7Bによる32フレーム評価では、基準方式の一例当たり遅延2.30秒・メモリ34GBに対し、DyCokeは1.49秒・24GBとなった。

- **2024-05 · [Boosting Multimodal Large Language Models with Visual Tokens Withdrawal for Rapid Inference](2024-2405.05803-boosting-multimodal-large-language-models-with-visual-tokens-withdrawal-.md)**  
  実装：[✓](https://github.com/lzhxmu/VTW) ・ リポジトリ内被引用：61  
  例えばLLaVAでは336×336画像を576個の視覚トークンに変換し、システム指示、ユーザー質問、生成済みのテキストトークンとともにデコーダへ流す。

- **2024-10 · [LongVU: Spatiotemporal Adaptive Compression for Long Video-Language Understanding](2024-2410.17434-longvu-spatiotemporal-adaptive-compression-for-long-video-language-under.md)**  
  実装：[✓](https://github.com/Vision-CAIR/LongVU) ・ リポジトリ内被引用：56  
  LongVUは、長時間動画を多模態大規模言語モデルへ入力するとき、視覚トークン数が文脈長を超える問題に対して、時間方向の冗長なフレーム削除、質問に応じた空間解像度の配分、フレーム間で重複する空間トークンの削除を段階的に組み合わせる方式である。

- **2024-08 · [LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression](2024-33c68d74c3c9-llmlingua-2-data-distillation-for-efficient-and-faithful-task-agnostic-p.md)**  
  実装：[✓](https://aka.ms/LLMLingua-2) ・ リポジトリ内被引用：52  
  本手法は圧縮を単語の保持/削除の二値分類として定式化し、双方向encoderのXLM-RoBERTa-largeやmBERTに圧縮の目的を直接学習させる。V100-32GB上のMeetingBank遅延測定では、非圧縮エンドツーエンド14.9秒に対し、5倍圧縮時5.2秒（2.9倍高速）と報告する。

- **2024-06 · [D2O: Dynamic Discriminative Operations for Efficient Long-Context Inference of Large Language Models](2024-2406.13035-d2o-dynamic-discriminative-operations-for-efficient-long-context-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：47  
  全層へ同じKVキャッシュ量を与えず、プリフィル時の注意密度から浅い層へ大きく、深い層へ小さく予算を配る。さらに追い出し候補を永久削除せず、保持トークンとの類似度を再判定して情報を重み付き統合する。学習なしで長文品質を保ちつつ、フルKVキャッシュ比で最大3.04倍のスループットを示す。

- **2024-08 · [Training-Free Activation Sparsity in Large Language Models](2024-2408.14690-training-free-activation-sparsity-in-large-language-models.md)**  
  実装：[✓](https://github.com/FasterDecoding/TEAL) ・ リポジトリ内被引用：44  
  隠れ状態の小振幅成分を層別にゼロ化し、対応重みチャネルを読まない専用カーネルで、追加学習なしに40〜50%のモデル全体活性疎性と最大1.8倍のデコード高速化を実現する。

- **2024-07 · [LazyLLM: Dynamic Token Pruning for Efficient Long Context LLM Inference](2024-2407.14057-lazyllm-dynamic-token-pruning-for-efficient-long-context-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：40  
  LazyLLMは、長い入力文のすべてのトークンを全変換層で計算する慣行を改め、現在予測しようとしている次のトークンに重要な入力部分だけを深い層へ進める推論時の計算削減法である。

- **2024-06 · [Turbo Sparse: Achieving LLM SOTA Performance with Minimal Activated Parameters](2024-2406.05955-turbo-sparse-achieving-llm-sota-performance-with-minimal-activated-parameters.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  SwiGLUのゲート側だけでなくup射影側にもReLUを掛ける二重ReLU（dReLU）へ置換し、継続事前学習で性能を回復する。Mistral-7BはFFNの約90%、Mixtral-47Bは専門家ルーティング込みで約97%を非活性化し、PowerInfer系の疎実行で2〜5倍のデコード高速化を報告する。

- **2024-03 · [Not All Layers of LLMs Are Necessary During Inference](2024-2403.02181-not-all-layers-of-llms-are-necessary-during-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  本論文は、デコーダ専用大規模言語モデルの各入力を必ず最終層まで通すことによる過剰計算を、入力単位の早期終了で減らすAdaInferを提案する。原著第3版の主評価では、Llama 2の7B・13BとOPT-13Bで層削減率は課題により約9〜43%、平均17.8%となる。

- **2024-09 · [Discovering the Gems in Early Layers: Accelerating Long-Context LLMs with 1000x Input Token Reduction](2024-2409.17422-discovering-the-gems-in-early-layers-accelerating-long-context-llms-with.md)**  
  実装：[✓](https://github.com/SalesforceAIResearch/GemFilter) ・ リポジトリ内被引用：18  
  GemFilterは、長い入力文脈を持つ大規模言語モデル（LLM）の推論を高速化するため、回答に関係する入力トークンをモデルの比較的早い層で選び、その短い部分列だけを全層で再処理する手法である。

- **2024-11 · [FFN-SkipLLM: A Hidden Gem for Autoregressive Decoding with Adaptive Feed Forward Skipping](2024-2404.03865-ffn-skipllm-a-hidden-gem-for-autoregressive-decoding-with-adaptive-feed-.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  将来トークンが参照するキャッシュに穴が生じるため、過去状態をコピーしたり鍵・値を再計算したりする追加対策が必要となる。提案法は各層の自己注意を維持し、FFNに入る状態とFFN残差更新後の状態のコサイン類似度（cosine similarity）から、中間層の冗長なFFNを検出する。

- **2024-09 · [Oryx MLLM: On-Demand Spatial-Temporal Understanding at Arbitrary Resolution](2024-2409.12961-oryx-mllm-on-demand-spatial-temporal-understanding-at-arbitrary-resoluti.md)**  
  実装：[✓](https://github.com/Oryx-mllm/Oryx) ・ リポジトリ内被引用：11  
  主要な設計要素は、入力画像の縦横比と解像度を維持して視覚特徴を抽出するOryxViTと、画像・短動画・長動画の用途に応じて視覚トークン数を1倍から最大16倍まで圧縮する動的圧縮器（動的 compressor）である。

- **2024-11 · [Accelerating Multimodal Large Language Models by Searching Optimal Vision Token Reduction](2024-2412.00556-accelerating-multimodal-large-language-models-by-searching-optimal-visio.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  この観察に「深い層で必要になる重要トークンは浅い層でも必要である」という仮定を加え、層別の保持率を浅い側から決める貪欲探索（Greedy Search、G-Search）を提案する。

- **2024-04 · [Accelerating Inference in Large Language Models with a Unified Layer Skipping Strategy](2024-2404.06954-accelerating-inference-in-large-language-models-with-a-unified-layer-ski.md)**  
  実装：[✓](https://github.com/Adaxry/Unified_Layer_Skipping) ・ リポジトリ内被引用：9  
  大規模言語モデル（LLM）の自動回帰生成では、次トークンを作るたびに多数のTransformer層を通る。したがって、論文は無劣化の高速化ではなく、実行層数・生成処理量・翻訳や要約の品質の交換関係を改善する方式を提案している。

- **2024-11 · [SparseInfer: Training-free Prediction of Activation Sparsity for Fast LLM Inference](2024-2411.12692-sparseinfer-training-free-prediction-of-activation-sparsity-for-fast-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  大規模言語モデルの逐次生成では、要求ごとの同時処理数が小さいと、フィードフォワード網の大きな重み行列をGPUメモリから読み出す費用が律速になる。入力によってゼロになる中間活性を事前に予測できれば、その活性に対応する行の重み読込みと行列ベクトル積を省略できる。しかし、一般的なLLaMAの滑らかな活性化関数であるSiLUでは、負の値も厳密にはゼロになりにくい。

- **2024-05 · [VideoTree: Adaptive Tree-based Video Representation for LLM Reasoning on Long Videos](2024-2405.19209-videotree-adaptive-tree-based-video-representation-for-llm-reasoning-on-.md)**  
  実装：[✓](https://github.com/Ziyang412/VideoTree) ・ リポジトリ内被引用：7  
  高関連クラスタだけを再分割して細部を調べるため、動画全体を均一に密な説明文へ変換する方式より、不要なフレーム説明や冗長な言語入力を減らせる。原著の主な根拠は、EgoSchema検証部分集合で66.2%の正答率、LLoVi-bestの61.2%に対して20.1秒対24.8秒という比較である。

- **2024-04 · [Hierarchical Context Merging: Better Long Context Understanding for Pre-trained LLMs](2024-2404.10308-hierarchical-context-merging-better-long-context-understanding-for-pre-t.md)**  
  実装：[✓](https://github.com/alinlab/HOMER) ・ リポジトリ内被引用：7  
  HOMER（Hierarchical cOntext MERging）は、入力を小区間に分けて初期層を処理し、中間層へ進むにつれて隣接区間を統合する。ICLR 2024の原著では、Llama-2-13B-chatの32Kトークンにおけるパスキー検索正答率が80.4%、位置尺度変更方式との併用で86.0%だった。

- **2024-11 · [ShowUI: One Vision-Language-Action Model for GUI Visual Agent](2024-2411.17465-showui-one-vision-language-action-model-for-gui-visual-agent.md)**  
  実装：[✓](https://github.com/showlab/ShowUI) ・ リポジトリ内被引用：6  
  一方、画像を粗く統合してしまうと、クリック対象の小さな部品の座標を失いやすい。Qwen2-VL-2Bを基盤に、25.6万件の指示データで学習したモデルは、ScreenSpotのゼロショット画面要素特定で75.1%を報告した。

- **2024-10 · [MoH: Multi-Head Attention as Mixture-of-Head Attention](2024-2410.11842-moh-mixture-of-head-attention.md)**  
  実装：[✓](https://github.com/SkyworkAI/MoH) ・ リポジトリ内被引用：6  
  注意ヘッドを共有ヘッドとTop-Kルーティングヘッドに分け、トークンごとに必要なヘッドだけ使うMoH。LLaMA3-8Bで75%利用・14評価平均64.0%を達成。

- **2024-02 · [HiRE: High Recall Approximate Top-k Estimation for Efficient LLM Inference](2024-2402.09360-hire-high-recall-approximate-top-k-estimation-for-efficient-llm-inferenc.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  HiRE（High Recall Approximate Top-k Estimation）は、自己回帰型の大規模言語モデル（LLM）で次トークンを生成するとき、必要な重み行・列を入力に応じて少数だけ読み込む方式である。

- **2024-10 · [CoreInfer: Accelerating Large Language Model Inference with Semantics-Inspired Adaptive Sparse Activation](2024-2410.18311-coreinfer-accelerating-large-language-model-inference-with-semantics-ins.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  文の意味が安定している間は、生成トークンが変わっても必要なFFNニューロンの集合は大きく変わらない。プリフィル時に文単位の重要ニューロンを決めて生成中に固定し、トークンごとの予測器と頻繁な重み配置変更を避ける。

- **2024-06 · [DEED: Dynamic Early Exit on Decoder for Accelerating Encoder-Decoder Transformer Models](2024-2311.08623-deed-dynamic-early-exit-on-decoder-for-accelerating-encoder-decoder-tran.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  浅い層の表現を深い層の状態としてそのままコピーする従来の停止・コピー方式は、層間の意味表現の違いを無視して精度を損なう。正式版のT5-large・SQuADでは、総遅延が221.9msから57.6ms（約74.0%短縮）、F1が92.1から91.6となった。

- **2024-11 · [AdaCM^2: On Understanding Extremely Long-Term Video with Adaptive Cross-Modality Memory Reduction](2024-2411.12593-adacm-2-on-understanding-extremely-long-term-video-with-adaptive-cross-m.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  AdaCM²は、長時間動画を言語モデルへ渡す際、すべてのフレームの視覚特徴を保存し続ける代わりに、テキスト質問と強く関連する視覚トークンだけを古いキャッシュから残す方式である。

- **2024-10 · [FiRST: Finetuning Router-Selective Transformers for Input-Adaptive Latency Reduction](2024-2410.12513-first-finetuning-router-selective-transformers-for-input-adaptive-latenc.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  FiRST（Finetuning Router-Selective Transformers）は、入力系列によって必要なTransformer層が異なるという観察に基づき、各層の前へ軽量ルータを挿入して推論時に通過層を選択する方式である。

- **2024-02 · [EE-Tuning: An Economical yet Scalable Solution for Tuning Early-Exit Large Language Models](2024-2402.00518-ee-tuning-an-economical-yet-scalable-solution-for-tuning-early-exit-larg.md)**  
  実装：[✓](https://github.com/pan-x-c/EE-LLM) ・ リポジトリ内被引用：2  
  EE-Tuningは、既存の大規模言語モデル（Large Language モデル; LLM）を、全パラメータの再学習なしに早期終了（early exit）できるモデルへ変換する手法である。論文本文では13Bの追加学習を4基のA800 GPUで約5時間、ピークGPUメモリ約20GB、70Bを約30時間、ピーク約78GBと報告する。

- **2024-11 · [freePruner: A Training-free Approach for Large Multimodal Model Acceleration](2024-2411.15446-freepruner-a-training-free-approach-for-large-multimodal-model-accelerat.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  主目的は視覚トークンの数を減らしてLLM側の事前入力処理（プリフィル）を軽くすることで、視覚エンコーダそのものを低ビット化する手法ではない。LLaVA-1.5では視覚トークンを約50%へ減らして複数の画像質問応答指標を維持し、Video-LLaVAではさらに高い冗長性を利用した削減を報告する。

- **2024-07 · [Turbo: Informativity-Driven Acceleration Plug-In for Vision-Language Large Models](2024-2407.11717-turbo-informativity-driven-acceleration-plug-in-for-vision-language-larg.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  相互冗長度と意味的価値を合わせた情報度で視覚と言語のトークンを並べ替え、冗長なものを統合する再学習不要の差し込みで、視覚言語モデルを理解課題で約2倍、生成課題で約1.6倍速くする方式。

- **2024-07 · [FlexAttention for Efficient High-Resolution Vision-Language Models](2024-2407.20228-flexattention-for-efficient-high-resolution-vision-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  高解像度画像の注意マップから重要領域の高解像度トークンだけを約1割選んで階層型自己注意へ入れることで、V BenchやTextVQAの精度を上げながら計算量を約3割から4割減らす視覚言語モデルの効率化。

- **2024-11 · [LoRAExit: Empowering Dynamic Modulation of LLMs in Resource-limited Settings using Low-rank Adapters](2024-af0fed60b919-loraexit-empowering-dynamic-modulation-of-llms-in-resource-limited-setti.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案は、共通の基盤重みを残したまま、出口ごとに独立した低階数適応器（Low-Rank Adaptation; LoRA）を配置する方式である。

- **2024-10 · [MoDification: Mixture of Depths Made Easy](2024-2410.14268-modification-mixture-of-depths-made-easy.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoDificationは、既存の大規模言語モデル（Large Language モデル; LLM）を、各トークンに必要な層の計算だけを実行する深さの混合（Mixture of Depths; MoD）方式へ変換する研究である。

- **2024-10 · [From Reading to Compressing: Exploring the Multi-document Reader for Prompt Compression](2024-2410.04139-from-reading-to-compressing-exploring-the-multi-document-reader-for-prom.md)**  
  実装：[✓](https://github.com) ・ リポジトリ内被引用：0  
  複数文書リーダーのクロス注意を重要度としてチャンクと文の二段でプロンプトを間引く圧縮法で、疑似ラベルなしに全体文脈を捉え、5倍から6倍の圧縮で精度首位と最速級の圧縮速度を両立する方式。

- **2024-07 · [An Adaptive Language-Agnostic Pruning Method for Greener Language Models for Code](2024-2407.04147-an-adaptive-language-agnostic-pruning-method-for-greener-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各層の注意スコアの分布から外れたトークンをフィードフォワード直前で適応的に落とす枝刈りで、コード向けモデルの演算を約半分にしつつ予測性能の98パーセント超を保つ方式。

- **2024-05 · [Switchable Decision: Dynamic Neural Generation Networks](2024-2405.04513-switchable-decision-dynamic-neural-generation-networks.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  問題設定。事前学習したTransformerを軽量化する一般的な方法は、枝刈り、量子化、知識蒸留などによって固定された小型モデルを作る。

- **2024-01 · [When Neural Code Completion Models Size up the Situation: Attaining Cheaper and Faster Completion through Dynamic Model Inference](2024-2401.09964-when-neural-code-completion-models-size-up-the-situation-attaining-cheap.md)**  
  実装：[✓](https://github.com/v587su/SEC) ・ リポジトリ内被引用：0  
  中間層で十分なトークンは早期に出し、予測できない補完は丸ごと打ち切る二判断の動的推論で、コード補完を平均11.2パーセント速くし無駄な提案も減らす方式。

- **2024-01 · [Dynamic Layer Skipping for Large Language Models on Natural Language Understanding Tasks and Machine Translation Using Reinforcement Learning](2024-b333410eff96-dynamic-layer-skipping-for-large-language-models-on-natural-language-und.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各層並列のアダプター型コントローラーが強化学習で次の層を飛ばすか決める動的レイヤースキッピングで、静的スキップより高い品質を保ち、機械翻訳では全層モデルをも上回る。

### 4年前（2022-12〜2023-11）

- **2023-10 · [LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression](2023-2310.06839-longllmlingua-accelerating-and-enhancing-llms-in-long-context-scenarios-.md)**  
  実装：[✓](https://aka.ms/LongLLMLingua) ・ リポジトリ内被引用：96  
  LongLLMLinguaは、長いプロンプトを単に一律に切り詰めるのではなく、「質問に対してどの文書・トークンが有用か」を小型言語モデルで推定し、重要部分へトークン予算を集中させる長文脈プロンプト圧縮法である。

- **2023-10 · [Compressing Context to Enhance Inference Efficiency of Large Language Models](2023-2310.06201-compressing-context-to-enhance-inference-efficiency-of-large-language-mo.md)**  
  実装：[✓](https://github.com/liyucheng09/Selective_Context) ・ リポジトリ内被引用：81  
  長い文書や会話を大規模言語モデル（LLM）へ入力すると、初回入力処理と鍵・値キャッシュに多くの時間・メモリが必要になる。Selective Contextは、下流モデルの構造や重みを変更する代わりに、入力文脈に含まれる予測しやすい語句を事前に削り、残った自然言語テキストだけを渡す。

- **2023-10 · [ReLU Strikes Back: Exploiting Activation Sparsity in Large Language Models](2024-2310.04564-relu-strikes-back-exploiting-activation-sparsity-in-large-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：44  
  大規模言語モデルは推論時に膨大な重みを読み出す。特に小さなバッチでの一トークンずつの生成では、演算器のピーク性能より高帯域メモリからの重み移動が制約になることが多い。滑らかな活性化関数であるSiLUやGELUは、負の入力でも通常は厳密なゼロを出さないため、出力が小さくても対応する重みの読み出しを機械的に省略しにくい。

- **2023-07 · [SkipDecode: Autoregressive Skip Decoding with Batching and Caching for Efficient LLM Inference](2023-2307.02628-skipdecode-autoregressive-skip-decoding-with-batching-and-caching-for-efficient-.md)**  
  実装：✓ ・ リポジトリ内被引用：40  
  トークンごとに途中で処理を終了する早期終了（early exit）は計算を減らせるが、従来の方式をそのまま実際の配信へ持ち込むと、二つの問題が生じる。原著は2023年のプレプリントで、OPT-1.3BとOPT-6.7Bを使い、構造化情報からの文章生成、短文要約、ニュース要約で目標2～5倍の高速化設定を比較した。

- **2023-07 · [MovieChat: From Dense Token to Sparse Memory for Long Video Understanding](2023-2307.16449-moviechat-from-dense-token-to-sparse-memory-for-long-video-understanding.md)**  
  実装：[✓](https://github.com/rese1f/MovieChat) ・ リポジトリ内被引用：32  
  MovieChatは、固定長の短期記憶を逐次更新し、古いフレームを類似度に応じて統合した長期記憶へ送ることで、この問題を扱う。原著図1は、224×224画素のフレームを標本抽出なしで処理する視覚側の条件で、24GB GPU上で10,000フレーム超を扱えると報告する。

- **2023-05 · [Let's Sample Step by Step: Adaptive-Consistency for Efficient Reasoning and Coding with LLMs](2023-2305.11860-let-s-sample-step-by-step-adaptive-consistency-for-efficient-reasoning-a.md)**  
  実装：[✓](https://sample-step-by-step.info) ・ リポジトリ内被引用：21  
  大規模言語モデル（LLM）で多段階推論の精度を上げる自己整合性（自己整合性）は、同じ質問に対して複数の思考連鎖を標本化し、最終回答を多数決する方式である。最大7.9倍の節約は個別条件の値であり、全条件平均ではない。

- **2023-03 · [CoLT5: Faster Long-Range Transformers with Conditional Computation](2023-2303.09752-colt5-faster-long-range-transformers-with-conditional-computation.md)**  
  実装：✓ ・ リポジトリ内被引用：21  
  軽量経路を全トークン、高容量の注意・MLPを学習ルータが選ぶ少数トークンだけへ適用し、16k入力でLongT5比35〜75%の学習高速化・50〜100%の推論高速化を示す。

- **2023-10 · [Sparse Universal Transformer](2023-2310.07096-sparse-universal-transformer.md)**  
  実装：[✓](https://github.com/shawntan/SUT) ・ リポジトリ内被引用：11  
  Sparse Universal Transformer（SUT）は、同じTransformerブロックを複数回反復するユニバーサルTransformer（Universal Transformer; UT）の長所を残しながら、反復計算を疎な専門家選択と動的停止で削減するモデルである。通常のTransformerは各層に別の重みを持つ。

- **2023-11 · [Learning to Skip for Language Modeling](2023-2311.15436-learning-to-skip-for-language-modeling.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  モデルを深くすれば表現容量は増えるが、トークン当たりの行列演算と復号遅延も増える。提案するSkipLayerは各層を二値ルータで包み、トークンの現在の隠れ表現から「この層を実行する」か「入力をそのまま次層へ渡す」かを選ぶ。

- **2023-05 · [SmartTrim: Adaptive Tokens and Attention Pruning for Efficient Vision-Language Models](2023-2305.15033-smarttrim-adaptive-tokens-and-attention-pruning-for-efficient-vision-lan.md)**  
  実装：[✓](https://github.com/kugwzk/SmartTrim) ・ リポジトリ内被引用：1  
  すべての入力に同じ割合でトークンを削る静的枝刈りは、簡単な入力では計算を無駄に残し、難しい入力では必要な情報まで失う可能性がある。METERのVQAでは、元モデルの77.43%・88.5 GFLOPsに対して、約2倍の計算量削減設定で77.13%・46.0 GFLOPsを報告する。

- **2023-07 · [DPBERT: Efficient Inference for BERT based on Dynamic Planning](2023-2308.00108-dpbert-efficient-inference-for-bert-based-on-dynamic-planning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DPBERTは、BERT-baseの12個のTransformer層をすべて通すのではなく、入力ごとに実行すべき層の部分列を決めることで推論遅延を削減する。従来のearly exitでは、途中の層で最終分類を確定すると、それより上の層をまとめて省略する。そのため下位・中間層を残したまま上位だけを削る選択に限定される。

### 5年前（2021-12〜2022-11）

- **2022-08 · [Learned Token Pruning for Transformers](2022-2107.00910-learned-token-pruning-for-transformers.md)**  
  実装：[✓](https://github.com/kssteven418/LTP) ・ リポジトリ内被引用：38  
  この論文の対象は、入力文の全トークンを全Transformer層で処理するために生じる推論計算量である。一次資料としてKDD 2022の原論文に加え、筆頭著者が2023年に公表した同方式の31ページの学位論文（UC Berkeley EECS-2023-119）の方法・評価・議論を参照した。

- **2022-05 · [A Simple Hash-Based Early Exiting Approach For Language Understanding and Generation](2022-219d2c1fa7a8-a-simple-hash-based-early-exiting-approach-for-language-understanding-an.md)**  
  実装：[✓](https://github.com/txsun1997/HashEE) ・ リポジトリ内被引用：8  
  前者は回帰や生成へそのまま転用しにくく、後者は未知入力に対する難度予測が難しい。難度を精密に当てることより、似た語彙が学習時と推論時に同じ計算経路を通る一貫性を重視する設計である。

- **2022-03 · [Transformer Feed-Forward Layers Build Predictions by Promoting Concepts in the Vocabulary Space](2022-2203.14680-transformer-feed-forward-layers-build-predictions-by-promoting-concepts-.md)**  
  実装：[✓](https://github.com/aviclu/ffn-values) ・ リポジトリ内被引用：8  
  Transformerの順伝播層（feed-順伝播 network、FFN）は、自己注意層で得た表現を更新するが、どのような内部操作が次トークンの予測を形作るかは分かりにくい。本論文は、FFNが出力するベクトルを、個々の値ベクトルに入力依存の係数を掛けた小さな加算成分の和として分解し、各成分が語彙中のどのトークンを押し上げるかを調べる。

- **2022-03 · [Pyramid-BERT: Reducing Complexity via Successive Core-set based Token Selection](2022-2203.14380-pyramid-bert-reducing-complexity-via-successive-core-set-based-token-sel.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  提案するPyramid-BERTは、各エンコーダ層の間で代表的なトークン表現の部分集合を選び、層が深くなるにつれて系列長を減らす。BERT-baseを用いたGLUEの開発集合では、推論時間を約3倍高速化する系列長構成で、原型の平均81.5に対して提案手法の最良設定が80.0を記録した。

- **2022-01 · [Latency Adjustable Transformer Encoder for Language Understanding](2022-2201.03327-latency-adjustable-transformer-encoder-for-language-understanding.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Transformerの推論では、すべての入力トークンに対して各層の注意機構とFFNを実行する。

- **2021-12 · [Block-Skim: Efficient Question Answering for Transformer](2021-2112.08560-block-skim-efficient-question-answering-for-transformer.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  注意重みから答えに関係するブロックだけを残し無関係な本文を下位層で早期に捨てることで、質問応答の精度を上げながらBERTを約3倍速くする早期スキミング。

- **2022-10 · [Accelerating Inference for Pretrained Language Models by Unified Multi-Perspective Early Exiting](2022-0f876c37e0b4-accelerating-inference-for-pretrained-language-models-by-unified-multi-p.md)**  
  実装：[✓](https://github.com/JunKong5/MPEE) ・ リポジトリ内被引用：0  
  層を抜ける縦の早期終了に、クラスアテンションで情報量の少ないトークンを融合トークンへ畳む横の早期終了を組み合わせ、分類器メモリと重み付き自己蒸留で浅い分類器の弱さを補って、GLUEで最大4.4倍のFLOPs削減を得る統合方式。

### 6年前（2020-12〜2021-11）

- **2021-04 · [BERxiT: Early Exiting for BERT with Better Fine-Tuning and Extension to Regression](2021-3c0f54f14532-berxit-early-exiting-for-bert-with-better-fine-tuning-and-extension-to-r.md)**  
  実装：[✓](https://github.com/castorini/berxit) ・ リポジトリ内被引用：21  
  従来の早期終了では、最後の層で良い予測を得ることと、中間層でも十分に良い予測を得ることの学習目標が競合しやすい。BERxiTはこの二つを別々の機構で解決する。例えばBERTBASEのSST-2試験集合では、交互微調整によって元モデルの得点の98%を保ちながら実行層数を65%減らす条件があり、より強い早期終了では96%の得点に対して79%の層削減を得る。

- **2021-06 · [TR-BERT: Dynamic Token Reduction for Accelerating BERT Inference](2021-00c8b8f9f90e-tr-bert-dynamic-token-reduction-for-accelerating-bert-inference.md)**  
  実装：[✓](https://github.com/thunlp/TR-BERT) ・ リポジトリ内被引用：13  
  選択しなかったトークンの表現はその層で凍結し、最終予測時には終了時の表現を回収する。表2の代表条件では、SQuAD 2.0でBERTのF1 77.12に対しTR-BERT12は75.66、演算回数の比で2.08倍の削減である。

- **2021-10 · [Magic Pyramid: Accelerating Inference with Early Exiting and Token Pruning](2021-2111.00230-magic-pyramid-accelerating-inference-with-early-exiting-and-token-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  文章分類器BERTの推論で、後続層へ運ぶトークン数を減らす枝刈りと、十分に確信できた入力の層処理を途中終了する機構を組み合わせる。入力長により得意条件が異なる二つの削減方法を重ね、五つの分類課題で演算量と精度の交換条件を評価した研究。表に示す4.95倍や8.25倍は浮動小数点演算量から計算した削減倍率であり、GPUの実時間高速化をそのまま意味しない。

### 7年前（2019-12〜2020-11）

- **2020-04 · [DeeBERT: Dynamic Early Exiting for Accelerating BERT Inference](2020-2004.12993-deebert-dynamic-early-exiting-for-accelerating-bert-inference.md)**  
  実装：[✓](https://github.com/castorini/DeeBERT) ・ リポジトリ内被引用：75  
  DeeBERTは、BERT系の分類モデルで入力ごとに必要なTransformer層数が異なることを利用し、浅い層ですでに十分確信度の高い予測が得られた例を途中で返す動的早期終了（動的 early exiting）方式である。

- **2020-06 · [BERT Loses Patience: Fast and Robust Inference with Early Exit](2020-2006.04152-bert-loses-patience-fast-and-robust-inference-with-early-exit.md)**  
  実装：✓ ・ リポジトリ内被引用：54  
  浅い層で正しい分類がほぼ確定している入力にも後段層の計算を続けるため、不要な遅延が生じる。従来の早期終了方式は中間分類器の最大確率やエントロピーなど、一つの層での自信の強さを停止信号にすることが多かった。

- **2020-04 · [FastBERT: a Self-distilling BERT with Adaptive Inference Time](2020-2004.02178-fastbert-a-self-distilling-bert-with-adaptive-inference-time.md)**  
  実装：[✓](https://github.com/autoliuweijie/FastBERT) ・ リポジトリ内被引用：52  
  この設計は文章生成の各トークンを省略する方式ではなく、主に文章分類と文対照合に適用される。例えば中国語THUCNewsでは閾値0.1で分類精度96.71%を維持しつつ計算量が約6.05分の1、英語DBpediaでは同閾値で99.31%から99.28%への微小な低下と引き換えに約10.57分の1となる。

- **2020-01 · [PoWER-BERT: Accelerating BERT Inference via Progressive Word-vector Elimination](2020-2001.08950-power-bert-accelerating-bert-inference-via-progressive-word-vector-elimi.md)**  
  実装：[✓](https://github.com/IBM/PoWER-BERT) ・ リポジトリ内被引用：31  
  方式は二つの判断を分離する。原著のK80 GPU、Keras、バッチ128（RACEのみ32）の評価では、BERTBASE比で各課題2.0～4.5倍の推論時間短縮を報告する。
<!-- survey:auto:end -->
