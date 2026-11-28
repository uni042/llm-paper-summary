# Other Inference Systems

推論効率化を主目的とするが、現時点では他の系統へ自然に入らず、**独立系統を作るほど同種研究がまだ集まっていない手法**を置く。ここに論文が増えて共通した問題設定・主要技術・評価軸が見えてきた場合は、新しい系統へ分割する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（851本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/99-other-inference-systems/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-12〜2026-11**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-12〜2026-11）

- **2026-01 · [Ministral 3](2026-2601.08584-ministral-3.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  著者らはこの方式を段階蒸留（Cascade Distillation）と呼ぶ。したがって「全評価項目で教師と同等」ではない。

- **2026-01 · [Latent Space Communication via K-V Cache Alignment](2026-2601.06123-latent-space-communication-via-k-v-cache-alignment.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  モデル固有のKVキャッシュを、共有潜在空間への入出力変換器を介して交換する。単に同じ数値へ復元するのではなく、受信側が後続トークンを正しく予測できる状態を学ぶことで、異なる言語モデル間の内部状態共有を可能にする。

- **2025-12 · [Recursive Language Models](2025-2512.24601-recursive-language-models.md)**  
  実装：[✓](https://github.com/alexzhang13/rlm) ・ リポジトリ内被引用：11  
  再帰型言語モデル（Recursive Language モデル; RLM）は、長い入力を大規模言語モデルの注意窓へ丸ごと入れる代わりに、持続的なプログラム実行環境の変数として保存し、モデル自身がコードを生成して入力の必要箇所を調査・分割・変換する推論方式である。

- **2026-01 · [SWE-Pruner: Self-Adaptive Context Pruning for Coding Agents](2026-2601.16746-swe-pruner-self-adaptive-context-pruning-for-coding-agents.md)**  
  実装：[✓](https://github.com/Ayanami1314/swe-pruner) ・ リポジトリ内被引用：10  
  コード編集エージェントは、問題を理解して修正するまでに何度もファイルを読み、検索し、テストを実行する。cat や grep が返した大量のコードや周辺行を、そのまま大規模言語モデル（LLM）へ渡すと、文脈窓を圧迫し、API料金と推論時間を増やす。しかも一度読み込んだ不要なコードは対話履歴に残り、次の推論でも繰り返し処理される。

- **2026-07 · [Read As Human: Compressing Context via Parallelizable Close Reading and Skimming](2026-2602.01840-read-as-human-compressing-context-via-parallelizable-close-reading-and-s.md)**  
  実装：[✓](https://github.com/Twilightaaa/RAM) ・ リポジトリ内被引用：8  
  入力文脈圧縮には、不要な語を削る方式と、文章を連続ベクトルへ変換する方式がある。Qwen3-4Bでの4倍圧縮時、NaturalQAの完全一致率は66.59、2WikiMQAは50.39であり、8倍圧縮時にはそれぞれ61.09、40.24となる。

- **2026-02 · [ICaRus: Identical Cache Reuse for Efficient Multi Model Inference](2026-2603.13281-icarus-identical-cache-reuse-for-efficient-multi-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  複数の専門言語モデルを順番に呼び出すエージェント型推論では、同じシステム指示、会話履歴、検索資料を何度も入力する。LLaMA-3.1-8Bを使うReAct型の8エージェント構成では、通常のモデル別KV方式に対して95パーセンタイル遅延（P95、遅い側5%に入る境界）を最大11.1倍短縮し、最大スループットを3.8倍に高めた。

- **2026-04 · [MiniCPM-o 4.5: Towards Real-Time Full-Duplex Omni-Modal Interaction](2026-2604.27393-minicpm-o-4-5-towards-real-time-full-duplex-omni-modal-interaction.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  従来の対話方式では、利用者の発話が終わってからモデルが考え、応答が終わるまで次の入力を十分反映できない。著者のRTX 4090測定では、vLLMのINT4条件で毎秒212.3トークン、初回トークン遅延0.58秒、使用メモリ11GBを報告する。

- **2026-02 · [QuantVLA: Scale-Calibrated Post-Training Quantization for Vision-Language-Action Models](2026-2602.20309-quantvla-scale-calibrated-post-training-quantization-for-vision-language.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  視覚・言語・行動モデル（vision-language-action モデル; VLA）は、画像と自然言語の指示を統合し、ロボットの連続した操作を生成する。

- **2026-02 · [Is Retraining-Free Enough? The Necessity of Router Calibration for Efficient MoE Compression](2026-2603.02217-is-retraining-free-enough-the-necessity-of-router-calibration-for-effici.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  しかし推論時に呼ばれない専門家も含めて大量の重みを保持する必要があり、GPUメモリの制約が厳しい。専門家を削除、低ランク編集、統合する方式はこの常駐重みを減らせるが、圧縮後の性能が元モデルより大きく落ちることがある。

- **2026-05 · [Language Modeling with Hyperspherical Flows](2026-2605.11125-language-modeling-with-hyperspherical-flows.md)**  
  実装：[✓](https://github.com/jdeschena/s-flm) ・ リポジトリ内被引用：4  
  S-FLMは代わりに次元 d の単位超球面 S^{d-1} 上へトークンを配置し、雑音ベクトルから正しい単語埋め込みへ回転する経路を学習する。

- **2026-04 · [DORA: A Scalable Asynchronous Reinforcement Learning System for Language Model Training](2026-2604.26256-dora-a-scalable-asynchronous-reinforcement-learning-system-for-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  DORAは、大規模言語モデル（Large Language モデル; LLM）の強化学習（Reinforcement Learning; RL）による後学習を、生成する応答の長さが大きく偏る状況でも効率よく進めるシステムである。

- **2025-12 · [Trellis: Learning to Compress Key-Value Memory in Attention Models](2025-2512.23852-trellis-learning-to-compress-key-value-memory-in-attention-models.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  通常の自己注意では、生成済みの全トークンに対する鍵ベクトルと値ベクトルを保持し、次のトークンでそれらを参照する。提案は、鍵を圧縮して中間表現を得る第1段と、値を圧縮して出力を得る第2段からなる。

- **2026-07 · [LightRot: A Light-Weighted Rotation Scheme and Architecture for Accurate Low-Bit Large Language Model Inference](2026-2607.27704-lightrot-a-light-weighted-rotation-scheme-and-architecture-for-accurate-.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  低ビットLLM推論では重みだけでなく、推論時に生成される入力活性（IA）とKVキャッシュを4ビットへ量子化したい。

- **2026-06 · [Posterior Refinement: Fast Language Generation via Any-Order Flow Maps](2026-2606.24773-posterior-refinement-fast-language-generation-via-any-order-flow-maps.md)**  
  実装：[✓](https://github.com/MananAg007/posterior-refinement) ・ リポジトリ内被引用：3  
  フローマップにマスク型条件付けを入れて全体生成と事後確信度を両立させ、確信の低いトークンだけを再生成する反復で、関数評価を最大32分の1にしながら拡散系比較対象に並ぶ非自己回帰生成方式。

- **2026-06 · [End-to-End Context Compression at Scale](2026-2606.09659-end-to-end-context-compression-at-scale.md)**  
  実装：[✓](https://github.com/LeonLixyz/LCLM) ・ リポジトリ内被引用：3  
  LCLM（Latent Context Language モデル）は、長いテキストを先に小型encoderで短い連続ベクトル列へ変換し、その列を大きいdecoderへ渡すコンテキスト圧縮方式である。

- **2026-04 · [Efficient Test-Time Scaling via Temporal Reasoning Aggregation](2026-2604.17304-efficient-test-time-scaling-via-temporal-reasoning-aggregation.md)**  
  実装：[✓](https://github.com/qianfantianyuzhouzhou/TRACE) ・ リポジトリ内被引用：3  
  推論時の計算量を増やすと難問の正答率を改善できる場合があるが、すべての問題で長い思考を最後まで生成することが効率的とは限らない。答えが既に定まった後も思考を続ける「過剰思考」は、トークン数と応答待ち時間を増やす。一方、途中の回答の確信度が高くなった瞬間に止めると、まだ検討が十分でない誤答を確定する危険がある。正答率も完全には維持していない。

- **2026-01 · [Residual Context Diffusion Language Models](2026-2601.22954-residual-context-diffusion-language-models.md)**  
  実装：[✓](https://github.com/yuezhouhu/residual-context-diffusion) ・ リポジトリ内被引用：3  
  マスク型拡散大規模言語モデル（dLLM）は、複数のトークン位置を同時に予測し、確信度が高い位置だけを確定しながら残りを反復更新する。SDAR-8Bでブロック長64のMATH500正答率は通常の逐次ノイズ除去（Sequential Denoising、SeqD）の64.20%から74.40%へ、AIME24は7.08%から18.75%へ改善する。

- **2026-09 · [STEPQuant: When and Where Errors Matter in Delta-Rule Recurrent State Quantization](2026-2609.38169-stepquant-when-and-where-errors-matter-in-delta-rule-recurrent-state-qua.md)**  
  実装：[✓](https://github.com/Dreamer-Toby/STEPQuant) ・ リポジトリ内被引用：2  
  Gated DeltaNetやKimi Delta 注意機構の状態は通常FP32で保持され、要求ごとに持続するため、重みを4ビットへ圧縮した後は状態プールの容量がサービングの律速となり得る。

- **2026-07 · [Constrained Decoding for Diffusion Language Models via Efficient Inference over Finite Automata](2026-2607.07026-constrained-decoding-for-diffusion-language-models-via-efficient-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  DangとErmonは、生成時に課す制約を有限オートマトン（finite automaton）へ変換し、拡散モデルの各位置に対する予測分布とオートマトンの受理経路を結合する。制約を満たすかどうかを生成後に判定して捨てる拒否標本化とは異なり、無効な系列へ確率を割り当てない点が中心的な貢献である。

- **2026-06 · [Mitigating Bias in Locally Constrained Decoding via Tractable Proposals](2026-2606.01926-mitigating-bias-in-locally-constrained-decoding-via-tractable-proposals.md)**  
  実装：[✓](https://github.com/MhDang/gelatwo) ・ リポジトリ内被引用：2  
  本論文は有限オートマトンをテンソル化し、残りトークン予算内に受理状態へ到達可能な語だけを許すGCDと、蒸留HMMで将来の有効な完了の確率を推定するP-GCDを提案。

- **2026-06 · [Memory is Reconstructed, Not Retrieved: Graph Memory for LLM Agents](2026-2606.06036-memory-is-reconstructed-not-retrieved-graph-memory-for-llm-agents.md)**  
  実装：[✓](https://github.com/Ji-shuo/MRAgent) ・ リポジトリ内被引用：2  
  MRAgent（メモリ Reasoning 構成 for LLM Agents）は、対話記憶を「手掛かり（Cue）・関連タグ（Tag）・記憶内容（Content）」の三者関係として整理し、LLMが現在までに得た証拠に応じて次の検索操作を選ぶ能動的な記憶再構成を提案する。

- **2026-06 · [Do Transformers Need Three Projections? Systematic Study of QKV Variants](2026-2606.04032-do-transformers-need-three-projections-systematic-study-of-qkv-variants.md)**  
  実装：[✓](https://github.com/anushamadan02/Do-Transformers-Need-3-Projections) ・ リポジトリ内被引用：2  
  標準的なTransformerの注意機構では、入力表現Xを三つの独立した行列で変換し、問い合わせ（Query; Q）、鍵（Key; K）、値（Value; V）を生成する。鍵と値を同一射影にすると、推論時にKだけを保持してVとしても再利用でき、標準的なQKVに比べてKVキャッシュを50%削減できる。

- **2026-05 · [Probabilistic Tiny Recursive Model](2026-2605.19943-probabilistic-tiny-recursive-model.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  数独や格子型の制約充足問題で高い精度を示す一方、決定的な更新では誤った解の近傍へ収束し、再帰を増やしても抜け出せないことがある。推論時の追加計算を、再帰を長くする「深さ」だけでなく、並列に試す「幅」へ割り当てる方式である。

- **2026-05 · [Nearly Optimal Attention Coresets](2026-2605.05602-nearly-optimal-attention-coresets.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  長文脈LLMのKVキャッシュを元の鍵・値対の部分集合へ縮約する際、全てのノルム有界な問い合わせに対して注意出力誤差をε以内に保つコアセットの存在上界と情報理論的下界を証明。計算可能な高速KV削除アルゴリズムや実モデルの品質・速度改善を実証する論文ではない。

- **2026-05 · [Multi-Stream LLMs: Unblocking Language Models with Parallel Streams of Thoughts, Inputs and Outputs](2026-2605.12460-multi-stream-llms-unblocking-language-models-with-parallel-streams-of-th.md)**  
  実装：[✓](https://github.com/seal-rg/streaming) ・ リポジトリ内被引用：2  
  Multi-Stream LLMsは、利用者、回答、内部思考、監査などの役割を独立したトークン列へ割り当て、一回の前向き計算で各列の次トークンを同時に生成するモデル形式を提案する。

- **2026-05 · [BubbleSpec: Turning Long-Tail Bubbles into Speculative Rollout Drafts for Synchronous Reinforcement Learning](2026-2605.08862-bubblespec-turning-long-tail-bubbles-into-speculative-rollout-drafts-for.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  従来の非同期化はこの待ちを減らせるが、生成時の方策と更新時の方策がずれるという別の問題を持ち込む。候補が誤っていても棄却サンプリングで目標分布へ戻すため、古い方策の出力を無条件に採用する方式とは異なる。通常のVerlと比べ、復号ステップ数は48.9～56.8%減、ロールアウト時間は30.0～45.2%減である。

- **2026-05 · [AgentStop: Terminating Local AI Agents Early to Save Energy in Consumer Devices](2026-2605.15206-agentstop-terminating-local-ai-agents-early-to-save-energy-in-consumer-d.md)**  
  実装：[✓](https://github.com/brave-experiments/AgentStop) ・ リポジトリ内被引用：2  
  LLMエージェントは通常の一問一答と異なり、推論、検索、コード実行、失敗後の再試行を何度も繰り返す。これをクラウドではなく利用者の端末で動かすと、ネットワーク依存や外部へのデータ送信を減らせる一方、長時間のGPU稼働、発熱、電池消費が利用者に直接影響する。特に失敗する実行が長く続いた場合、最終的な課題成功に結び付かない電力が大量に消費される。

- **2026-04 · [Towards Joint Quantization and Token Pruning of Vision-Language Models](2026-2604.17320-towards-joint-quantization-and-token-pruning-of-vision-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  本論文は視覚言語モデル（VLM）の推論で、低ビット量子化と視覚トークン枝刈りを別々に設計すると品質が不安定になる問題を扱う。LLaVA-1.5-7B-hfで視覚トークンを最終30%まで削減した場合、6ベンチマークの完全精度モデルに対する平均性能保持率は95.65%だった。

- **2026-04 · [ELMoE-3D: Leveraging Intrinsic Elasticity of MoE for Hybrid-Bonding-Enabled Self-Speculative Decoding in On-Premises Serving](2026-2604.14626-elmoe-3d-hybrid-bonding-self-speculative-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  HBメモリ上の頻出エキスパート上位ビットをキャッシュ兼自己ドラフトとして使い、MoEの投機的デコードと重み転送を一体最適化する3D積層HW-SW協調方式。

- **2026-04 · [A Self-Evolving Framework for Efficient Terminal Agents via Observational Context Compression](2026-2604.19572-a-self-evolving-framework-for-efficient-terminal-agents-via-observationa.md)**  
  実装：[✓](https://github.com/multimodal-art-projection/TACO) ・ リポジトリ内被引用：2  
  TACO（Terminal Agent Compression）は、コマンド出力をエージェントの履歴へ入れる直前に圧縮する追加層である。MiniMax-M2.5によるTerminalBench 1.0では成功率42.30%→45.25%、総トークン29.74→23.43百万（21.2%減）である。

- **2026-03 · [SkipOPU: An FPGA-based Overlay Processor for Large Language Models with Dynamically Allocated Computation](2026-2603.14785-skipopu-an-fpga-based-overlay-processor-for-large-language-models-with-d.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  本研究は、非線形処理の待機を隠す融合データフロー、浮動小数点活性値と4ビット整数重みを扱うDSP演算器の高密度実装、層をまたいで変化しないKVを保持するオンチップ履歴バッファを一体設計した。AMD Alveo U280上のLlama2-7Bで140.8トークン/秒、帯域効率86.7%を報告する。

- **2026-03 · [Prune-then-Quantize or Quantize-then-Prune? Understanding the Impact of Compression Order in Joint Model Compression](2026-2603.18426-prune-then-quantize-or-quantize-then-prune-understanding-the-impact-of-c.md)**  
  実装：[✓](https://github.com/snudatalab/PQQP) ・ リポジトリ内被引用：2  
  本論文は、大規模言語モデル（LLM）を枝刈り（枝刈り）と量子化（量子化）の両方で圧縮する場合、どちらを先に適用すべきかを、圧縮率とモデル品質の関係から分析した研究である。枝刈り率5～30%、量子化4～8ビットを含む条件で、単独適用時の圧縮強度の差が大きいほど順序による品質差が大きくなる傾向を確認した。

- **2026-02 · [Understanding and Exploiting Weight Update Sparsity for Communication-Efficient Distributed RL](2026-2602.03839-understanding-and-exploiting-weight-update-sparsity-for-communication-ef.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  大規模言語モデル（LLM）の強化学習による後学習（reinforcement learning post-学習）では、重みを更新する学習器（trainer）と、現在の方策を用いて回答を生成する推論ワーカー（inference worker）が分離されることが多い。

- **2026-02 · [T3D: Few-Step Diffusion Language Models via Trajectory Self-Distillation with Direct Discriminative Optimization](2026-2602.12262-t3d-few-step-diffusion-language-models-via-trajectory-self-distillation-.md)**  
  実装：[✓](https://github.com/Tyrion58/T3D) ・ リポジトリ内被引用：2  
  これに対しマスク拡散言語モデル（Masked Diffusion Language モデル、MDLM）は、複数位置のマスクを並列に予測し、繰り返し修正して文章を完成させる。動的復号を組み合わせた一部条件では、GSM8Kの正答率を10.8ポイント改善しながら処理量を1.45倍にする実測結果も報告されている。

- **2026-02 · [SimpleTool: Parallel Decoding for Real-Time LLM Function Calling](2026-2603.00030-simpletool-parallel-decoding-for-real-time-llm-function-calling.md)**  
  実装：[✓](https://github.com/HaxxorCialtion/SimpleTool) ・ リポジトリ内被引用：2  
  SimpleToolは、大規模言語モデルによる関数呼出し（function calling）の待ち時間を減らすために、出力表現の圧縮と並列復号（parallel デコード）を一緒に設計した手法である。

- **2026-02 · [Reasoning with Latent Tokens in Diffusion Language Models](2026-2602.03769-reasoning-with-latent-tokens-in-diffusion-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  この研究の問いは、マスク型拡散言語モデルが複雑な制約充足問題で自己回帰モデルより良い成績を示す場合、その差が何によって生じるのか、というものである。通常の拡散生成では未確定の複数位置について同時に分布を計算するが、一回の反復で実際に確定する位置はその一部だけである。残りの位置の出力はその反復では捨てられる。研究の核は二つある。

- **2026-02 · [RAT+: Train Dense, Infer Sparse -- Recurrence Augmented Attention for Dilated Inference](2026-2602.18196-rat-train-dense-infer-sparse-recurrence-augmented-attention-for-dilated-.md)**  
  実装：[✓](https://github.com/wimh966/rat-plus) ・ リポジトリ内被引用：2  
  注意機構の推論コストを下げる方法には、局所窓だけを見る方式や、重要なトークンだけを選ぶ方式がある。D=16では密な注意に近い精度を保ち、D=64では常識推論の平均正解率が59.21%から57.46%へ下がる一方、時間混合部分の理論演算量とKV保存量を64分の1へ減らす。

- **2026-02 · [Out of the Memory Barrier: A Highly Memory Efficient Training System for LLMs with Million-Token Contexts](2026-2602.02108-out-of-the-memory-barrier-a-highly-memory-efficient-training-system-for-llms-with-million-token-contexts.md)**  
  実装：[✓](https://github.com/wenhaoli-xmu/OOMB) ・ リポジトリ内被引用：2  
  チャンク再計算・ページ化KV/勾配・非同期CPUオフロード・疎注意を統合し、Qwen2.5-7Bの4M文脈学習を単一H200で実現する。

- **2026-02 · [ATTS: Asynchronous Test-Time Scaling via Conformal Prediction](2026-2509.15148-atts-asynchronous-test-time-scaling-via-conformal-prediction.md)**  
  実装：[✓](https://github.com/menik1126/Asynchronous-Test-Time-Scaling) ・ リポジトリ内被引用：2  
  下書きと対象モデルの検証を適合予測の検定として組み直して非同期化し、拡大推論を最大五六・七倍速く、処理量を四・一四倍にし、精度の損失なく棄却率を制御したと報告した。

- **2026-01 · [SimpleMem: Efficient Lifelong Memory for LLM Agents](2026-2601.02553-simplemem-efficient-lifelong-memory-for-llm-agents.md)**  
  実装：[✓](https://github.com/aiming-lab/SimpleMem) ・ リポジトリ内被引用：2  
  SimpleMemは、書き込み時に記憶を整理して、質問時に必要な情報だけを引き出すことで、この二種類の費用を同時に抑えようとする方式である。原著のLoCoMo評価では、GPT-4.1-miniを基盤としたSimpleMemの平均F1が43.24、Mem0が34.20で、相対26.4%の改善となる。

- **2026-01 · [LOOKAT: Lookup-Optimized Key-Attention for Memory-Efficient Transformers](2026-2601.10155-lookat-lookup-optimized-key-attention-for-memory-efficient-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  LOOKATは、自己回帰Transformerの注意得点計算を、ベクトル検索における内積類似度検索として扱い、キーを圧縮したまま注意得点を計算する方式である。GPT-2の第1注意層で、64次元のキーを2個の1バイト符号へ圧縮すると、キー表現は128バイトから2バイトへ減り、キー単体の表現上の圧縮率は64倍となる。

- **2025-12 · [Zero-Overhead Introspection for Adaptive Test-Time Compute](2025-2512.01457-zero-overhead-introspection-for-adaptive-test-time-compute.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  数学推論などでは、同じ質問に対して複数の回答候補を生成し、多数決（Majority Voting）や最良候補選択（Best-of-N）で正答率を高められる。しかし固定個数の候補を最後まで生成すると、既に正しい回答が得られそうな簡単な質問でも計算を浪費し、失敗しそうな長い推論系列が全体の応答時間を引き延ばす。外部の報酬モデルを推論時に追加で走らせる必要はない。

- **2025-12 · [Hybrid Token Compression for Vision-Language Models](2025-2512.08240-hybrid-token-compression-for-vision-language-models.md)**  
  実装：[✓](https://github.com/jushengzhang/HybridToken-VLM) ・ リポジトリ内被引用：2  
  一方、離散量子化した符号だけでは姿勢・質感・細部の変化が失われやすい。一次論文v2の7種類の画像理解評価では、無圧縮モデルを上限、学習しない1トークン圧縮を下限とする正規化性能保持率が87.2%であり、連続圧縮方式VoCo-LLaMAの81.0%を上回る。

- **2025-12 · [Bolmo: Byteifying the Next Generation of Language Models](2025-2512.15586-bolmo-byteifying-the-next-generation-of-language-models.md)**  
  実装：[✓](https://github.com/allenai/bolmo-core) ・ リポジトリ内被引用：2  
  本研究の中心課題は、強力なサブワード言語モデルをすべて一から学習し直さずに、文字の細部を直接扱えるバイト単位のモデルへ変えることである。推論速度は圧縮率に依存し、元モデルに近い4.4バイト/パッチではBolmoの方が遅い。

- **2025-12 · [AdmTree: Compressing Lengthy Context with Adaptive Semantic Trees](2025-2512.04550-admtree-compressing-lengthy-context-with-adaptive-semantic-trees.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  AdmTreeは、長い文書を大規模言語モデル（LLM）へ入力する際、入力トークンを短い潜在表現へ圧縮しつつ、局所的な事実と文書全体の意味を両立して保持する方式である。LongBenchの評価では、Llama-2-7Bを基盤にしたAdmTreeの平均得点は44.1で、活性値 Beaconの40.1を上回った。

- **2026-11 · [The Sparsity Whisperer](2026-2608.06630-the-sparsity-whisperer.md)**  
  実装：[✓](https://github.com/Shavit-Lab/Whisper) ・ リポジトリ内被引用：1  
  枝刈りで守るべきものを活性値の大きさから入力対の出力差へ広げ、層単位・ニューロン単位・二階再構成の三方式で、高いスパース率ほどスパースジーピーティーやワンダに対する改善が広がることを示す。

- **2026-11 · [Perceive Once, Escalate on Demand: Handing Off Visual KV Memory from Small to Large VLMs](2026-2611.26902-perceive-once-escalate-on-demand-handing-off-visual-kv-memory-from-small.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  小さい視覚言語モデルのKVキャッシュを大きいモデルへ渡すとき、相手のキャッシュへの忠実な回帰ではなく相手自身の回答から写像を蒸留することで、履歴の再エンコードなしに大きいモデルの判断を引き出せることを示した、カスケードの受け渡し経路の研究。

- **2026-11 · [MOAI: Module-Optimizing Architecture for non-interactive secure transformer Inference](2026-2611.13641-moai-module-optimizing-architecture-for-non-interactive-secure-transform.md)**  
  実装：[✓](https://github.com/dtc2025ag/MOAI) ・ リポジトリ内被引用：1  
  準同型暗号による非対話型の安全なトランスフォーマー推論で、パッキング統一と回転なしの非線形評価とインターリーブバッチングにより回転を大幅に減らし、評価時間を52.8パーセント削減した研究。

- **2026-10 · [ParaTTT: Parallelizing Test-Time Training Layers with Deep Memories](2026-2610.38255-parattt-parallelizing-test-time-training-layers-with-deep-memories.md)**  
  実装：[✓](https://github.com/ntumm120/paraTTT) ・ リポジトリ内被引用：1  
  深い非線形メモリの勾配軌跡を3つのチャンク並列パスで反復精緻化し、テスト時学習層を誤差を揃えて32倍速く評価できるようにした並列化アルゴリズム。

- **2026-10 · [Multi-Token Prediction Done Right](2026-2610.38331-multi-token-prediction-done-right.md)**  
  実装：[✓](https://github.com/JaydenTeoh/Soft-MTP) ・ リポジトリ内被引用：1  
  複数トークン予測の交差エントロピー勾配を自己蒸留成分と低品質な残差へ厳密に分解し、勾配回収の工夫で残差だけを消す一行変更のSoft-MTPにより、全規模でパープレキシティ、投機的デコーディング、ゼロショット精度を無料で改善する学習法。

- **2026-10 · [How to Loop Your Transformer: Loop Scaling, Specialization, and Parallel Inference](2026-2610.40325-how-to-loop-your-transformer-loop-scaling-specialization-and-parallel-in.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ループする範囲、ループごとの低ランク特化、トークン間へ接続をずらす並列化を統一条件で比較し、制約ごとに最適なループ設計が異なることと、並列ループの品質を正規化で回復できることを示した研究。

- **2026-10 · [Gated Slot Attention-2: Two-Sided Associative Memory Correction in Linear Attention](2026-2610.02816-gated-slot-attention-2-two-sided-associative-memory-correction-in-linear.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  キー側はオジャ則、値側はデルタ則で、共有スロットを持つ2段階メモリの両側を誤差修正し、線形注意の想起性能を高めた回帰型アーキテクチャ。

- **2026-09 · [Tensor Decomposition of Transformer Key-Value Caches: Spectral Structure and Format Comparison](2026-2609.28029-tensor-decomposition-of-transformer-key-value-caches-spectral-structure-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  この研究は、自己回帰Transformerの鍵・値キャッシュ（key-value キャッシュ; KVキャッシュ）を、注意ヘッド・トークン・特徴・隣接層の四つの軸を持つテンソルとして扱い、どの軸が実際に低ランク圧縮できるのかを調べる。RoPE後の鍵を圧縮すると、RoPE前に圧縮する場合に比べて同じ保存量での再構成誤差が相対41〜64%増す。

- **2026-09 · [SMat-Attention: Structured Long-Context Sequence Modeling](2026-2609.36062-smat-attention-structured-long-context-sequence-modeling.md)**  
  実装：[✓](https://anonymous.4open.science/r/smat_attention/README.md) ・ リポジトリ内被引用：1  
  SMat-注意機構は、過去へのアクセスを「任意の過去トークン」か「全履歴を一つに要約」かの二択とせず、選択できる過去トークン集合の組合せ的な豊かさをVC次元dで制御する。実験では、Mamba-2やGated DeltaNetに学習可能なプロフィールと4つの要約読出しを追加し、複数キー検索で精度を改善した。

- **2026-09 · [Online Draft Co-Training for Speculative Decoding in Large-Scale, Long-Context RL Post-Training](2026-2609.07108-online-draft-co-training-for-speculative-decoding-in-large-scale-long-context-rl-post-training.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長文脈RLで投機的復号のドラフトを方策と同時更新するため、分岐注意を文脈並列リングへ統合し、中間特徴をパイプライン外のTapChannelで輸送して、最大122B規模で学習品質を保ちつつ最大1.88倍の全体高速化を得る。

- **2026-09 · [Low-Bit Recurrent States in Hybrid Language Models](2026-2609.30950-low-bit-recurrent-states-in-hybrid-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  再帰状態の量子化誤差が減衰率に応じて蓄積する点に着目し、グラミアン由来の持続重みと正規化範囲でビット幅を混合配分することで、較正なしに平均4ビットで過剰な負の対数尤度を最良の比較対象比3.3から27.9倍削減した。

- **2026-08 · [When Entropy Is Not Enough: Reclaiming Lost Semantics in LLM Output Length Prediction](2026-2608.15592-when-entropy-is-not-enough-reclaiming-lost-semantics-in-llm-output-lengt.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  プリフィル中の注意から意味の重みを取り出し位置バイアスを除いた上で、エントロピーによる不確かさの重みと融合して出力長分布を予測し、長さに応じたスケジューリングのパディングと待ちを減らす研究。

- **2026-08 · [Structured Memory for Edge Language Models: Persistent Context and Corpus Retrieval via O(1) SSM State Injection](2026-2608.02560-structured-memory-for-edge-language-models-persistent-context-and-corpus.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  文書を隠れ状態として事前に保存し質問時に初期状態へ注入することで、検索付き生成の入力処理を約27秒から6ミリ秒未満へ短縮し、質問応答の品質が文脈内検索とほぼ一致することを示した。

- **2026-08 · [OpRAG: A Resource-Deterministic Runtime for GPU-Backed Multi-Stage RAG Workflows](2026-2608.08340-oprag-resource-deterministic-rag-runtime.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  RAG各段階を資源・通信付き演算子へ変換し、ゼロコピー通信とCPU/GPU重畳で復号外のオーケストレーション律速を削減する。

- **2026-08 · [Multi-Image Visual Token Pruning in Large Visual Language Models](2026-2608.26806-multi-image-visual-token-pruning-in-large-visual-language-models.md)**  
  実装：[✓](https://github.com/zry13/AVTP) ・ リポジトリ内被引用：1  
  隠れ状態の変化で重要度を測り、モデルに合う層と画像ごとの保持率を適応させる学習不要の視覚トークン枝刈りで、多画像推論を精度を保ちながら2倍速くする。

- **2026-08 · [Learning What to Remember: Test-Time Training via Context Distillation](2026-2608.01672-learning-what-to-remember-test-time-training-via-context-distillation.md)**  
  実装：[✓](https://github.com/dangxingyu/ttcd) ・ リポジトリ内被引用：1  
  通常の全注意（full 注意機構）は長い履歴の情報を参照できる一方、長さに応じて注意計算と鍵・値（KV）キャッシュの費用が増える。760Mパラメータをゼロから学習したモデルのRULER針検索（6課題平均）では、32KトークンでIP-TTTの9.29%に対しIP-TTCDは21.96%。

- **2026-08 · [A Layer Importance Metric for Quantization Accounting for the Speed-Quality Trade-off in Autoregressive Models](2026-2608.26926-a-layer-importance-metric-for-quantization-accounting-for-the-speed-qual.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  量子化の情報保持をSQNRで、速度利得をルーフライン型の解析予測で測り、重み付きで統合する層重要度指標を提案し、再実行なしの速度予測が平均誤差約3.4パーセントで実測と合うことを示した。

- **2026-07 · [SWE-Pruner Pro: The Coder LLM Already Knows What to Prune](2026-2607.18213-swe-pruner-pro-the-coder-llm-already-knows-what-to-prune.md)**  
  実装：[✓](https://github.com/Ayanami1314/swe-pruner-pro) ・ リポジトリ内被引用：1  
  エージェント自身の隠れ状態から行単位の枝刈り信号を読み出す小さなヘッドで、別モデルなしにツール出力を削り、SWE-QA-Proでトークン39.4パーセント減と品質維持を両立する。

- **2026-07 · [CoMem: Reusing Transformer Depth across Queries with Persistent Intermediate Residuals](2026-2607.28263-comem-reusing-transformer-depth-across-queries-with-persistent-intermedi.md)**  
  実装：[✓](https://github.com/liuhanzuo/Mixture-of-Memory) ・ リポジトリ内被引用：1  
  CoMemはTransformerのどこまでを文書単独で先払い計算するかを新たな制御変数とし、文書の中間残差（residual state）を永続保存して、問い合わせ時は上位層のみ再実行する方式である。

- **2026-06 · [LoopMoE: Unifying Iterative Computation with Mixture-of-Experts for Language Modeling](2026-2606.04438-loopmoe-unifying-iterative-computation-with-mixture-of-experts-for-langu.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  通常のMoEは、多数の専門家パラメータを保持しながら各トークンでは少数だけを選ぶことで、総容量と一回の計算量を分離する。しかし、反復による精度向上を単純な非反復モデルと比較すると、層数、総パラメータ、演算回数、専門家活性化数などが同時に変化し、何が改善を生んだのか分からなくなる。

- **2026-06 · [Improving Visual Token Reduction via Rectifying Distortions for Efficient Multimodal LLM Inference](2026-2606.01711-improving-visual-token-reduction-via-rectifying-distortions-for-efficien.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  視覚トークン削減（Visual Token Reduction; VTR）は不要なパッチを削除したり、似た特徴を統合したりして系列を短くする。LLaVA-1.5-7Bの8種類の画像理解課題で、視覚トークンを576個から64個へ減らすHoloVの平均保持率は92.2%だが、RESTOREを加えると96.5%になる。

- **2026-06 · [Extreme Low-Bit Inference in Reasoning Models: Failure Modes and Targeted Recovery](2026-2606.02011-extreme-low-bit-inference-in-reasoning-models-failure-modes-and-targeted.md)**  
  実装：[✓](https://github.com/brain-lab-research/quantized-reasoning) ・ リポジトリ内被引用：1  
  2ビット推論の失敗を推論過程の崩れとして診断し、半精度の計画と繰り返し救済を崩れた領域だけへ入れることで、MATH-500の正解率を8Bで17.2から74.2パーセントへ、32Bで65.0から87.2パーセントへ回復させた。

- **2026-05 · [XtraMAC: An Efficient MAC Architecture for Mixed-Precision LLM Inference on FPGA](2026-2605.06052-xtramac-an-efficient-mac-architecture-for-mixed-precision-llm-inference-.md)**  
  実装：[✓](https://github.com/Xtra-Computing/XtraMAC) ・ リポジトリ内被引用：1  
  整数と浮動小数点の積和を仮数の整数積へ分解して乗算経路を全精度で共有し累積だけを精度別に分けることで、書き換え可能な回路上で計算密度一・四〜二・〇倍と演算当たり資源の二七〜五一パーセント削減を達成し、混合精度の推論負荷でエネルギー効率が最大一・九倍になったと報告した。

- **2026-05 · [Training-Inference Consistent Segmented Execution for Long-Context LLMs](2026-2605.11744-training-inference-consistent-segmented-execution-for-long-context-llms.md)**  
  実装：[✓](https://github.com/sxp11/Training-Inference-Consistent-Segmented-Execution) ・ リポジトリ内被引用：1  
  長文脈の大規模言語モデル（LLM）は、通常の全注意力（full self-注意機構）を使うと、入力が長くなるにつれて注意演算と中間状態の記憶費用が増大する。16K/32K事前充填でのGPUピークメモリは18.56/19.06GBで、全注意力の23.61/34.67GBより小さい。

- **2026-05 · [The Shape of Overthinking: Backtracking Bursts in Long Reasoning Traces](2026-2605.27965-the-shape-of-overthinking-backtracking-bursts-in-long-reasoning-traces.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  行単位に分割した推論文へ、別の注釈実行で「継続・停滞・後戻り・終了」の確信度を割り当て、後戻りの強度に閾値を設ける。固定2000語の打切りでは残存軌跡の正解率がAIME2024で10.0%、AIME2025で6.7%になるのに対し、接頭部分の後戻り特徴で選別すると73.5%・64.5%となり、それぞれ21.7%・27.0%の軌跡を終了対象にできる。

- **2026-05 · [The Path Matters: Learning a Token-Commitment Policy for Diffusion Language Models](2026-2605.24697-the-path-matters-learning-a-token-commitment-policy-for-diffusion-langua.md)**  
  実装：[✓](https://github.com/BobSun98/TraceLock) ・ リポジトリ内被引用：1  
  LLaDAのGSM8Kでは生成長256・窓64で最終正答率80.0%、HumanEvalのPass@1は37.2%で、信頼度方式の79.8%、36.0%をわずかに上回る。

- **2026-05 · [Tensor Cache: Eviction-conditioned Associative Memory for Transformers](2026-2605.22884-tensor-cache-eviction-conditioned-associative-memory-for-transformers.md)**  
  実装：[✓](https://github.com/kswain98/tensor-cache) ・ リポジトリ内被引用：1  
  長文脈や同時要求数が増えるほどキャッシュの占有量が増え、GPUメモリ容量と帯域を圧迫する。学習可能なゲートでL1の局所注意出力とL2の読出しを融合することで、固定容量を保ちながら窓外の情報を予測へ戻す。

- **2026-05 · [Pruning and Distilling Mixture-of-Experts into Dense Language Models](2026-2605.28207-pruning-and-distilling-mixture-of-experts-into-dense-language-models.md)**  
  実装：[✓](https://github.com/krafton-ai/moe-to-dense) ・ リポジトリ内被引用：1  
  演算量は小さくても、すべての専門家をGPUメモリへ常駐させる場合の容量は大きい。CPUへ退避すれば容量制約を緩和できるが、専門家の転送が遅延や帯域を圧迫する。Qwen3-30B-A3Bから約3.3Bの密な生徒モデルを作った実験では、約4Bトークンの蒸留後に5課題の平均58.10%を達成した。

- **2026-05 · [ConQuR: Corner Aligned Activation Quantization via Optimized Rotations for LLMs](2026-2605.10793-conqur-corner-aligned-activation-quantization-via-optimized-rotations-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  低ビット量子化では、重みだけでなく中間活性値を4ビットなどで表現できれば、行列積の計算・転送の効率化余地が増す。

- **2026-05 · [Code Generation by Differential Test Time Scaling](2026-2605.20473-code-generation-by-differential-test-time-scaling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  コード生成の推論時計算量拡張（Test-Time Scaling、TTS）では、一つの問題に対して複数のコードを生成し、その中から正しい候補を選ぶ。従来の選択方式には、公開テストを実行するもの、別のLLMにテスト入力を生成させるもの、LLM評価器に候補を比較させるものがある。

- **2026-05 · [Beyond Position Bias: Shifting Context Compression from Position-Driven to Semantic-Driven](2026-2605.09463-beyond-position-bias-shifting-context-compression-from-position-driven-t.md)**  
  実装：[✓](https://anonymous.4open.science/r/seco-EE5E) ・ リポジトリ内被引用：1  
  本論文の対象は、長い文脈を少数の連続値の埋め込み（soft プロンプト）へ圧縮してから回答を生成する方式である。LLaMA-3.2-1B-Instructを用いた16倍圧縮・分布内6課題の平均完全一致率は、比較方式COMIの42.07に対してSeCoが53.52、平均F1は54.37に対して68.55であった。

- **2026-04 · [When to Commit? Towards Variable-Size Self-Contained Blocks for Discrete Diffusion Language Models](2026-2604.23994-when-to-commit-towards-variable-size-self-contained-blocks-for-discrete-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  拡散言語モデルで、未来文脈の有無による予測の乖離を自己完結性として測り、意味的に完結した位置で可変長にブロックを確定する方式と訓練の整合で、土台モデルを最大10.36ポイント改善した。

- **2026-04 · [Tandem: Riding Together with Large and Small Language Models for Efficient Reasoning](2026-2604.23623-tandem-riding-together-with-large-and-small-language-models-for-efficien.md)**  
  実装：[✓](https://github.com/Applied-Machine-Learning-Lab/ACL2026_Tandem) ・ リポジトリ内被引用：1  
  Tandemは、推論型大規模言語モデルが難問を解く際に生成する長い思考列を、より安価な小型言語モデルへ部分的に委ねる協調推論方式である。

- **2026-04 · [Prompt Compression in the Wild: Measuring Latency, Rate Adherence, and Quality for Faster LLM Inference](2026-2604.02985-prompt-compression-in-the-wild-measuring-latency-rate-adherence-and-qual.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  入力圧縮（プロンプト compression）は、情報価値の低い語や断片を削り、生成モデルに渡す入力を短くすることでこの費用を減らす。著者はLLMLingua-2の軽量な圧縮器を使えば、特定の長文入力・高圧縮条件で端から端までの遅延を最大約18%減らせると報告する。

- **2026-04 · [Open-Loop Planning, Closed-Loop Verification: Speculative Verification for VLA](2026-2604.02965-open-loop-planning-closed-loop-verification-speculative-verification-for.md)**  
  実装：[✓](https://github.com/edsad122/SV-VLA) ・ リポジトリ内被引用：1  
  本論文は、計画は重いモデルで低頻度に実施し、計画が依然として妥当かの検査だけを軽いモデルで毎制御時刻に実施するSV-VLA（投機的 検証 for VLA Control）を提案する。

- **2026-04 · [MemoSight: Unifying Context Compression and Multi Token Prediction for Reasoning Acceleration](2026-2604.14889-memosight-unifying-context-compression-and-multi-token-prediction-for-re.md)**  
  実装：[✓](https://github.com/helldog-star/MemoSight) ・ リポジトリ内被引用：1  
  MemoSightは、長い思考連鎖（Chain-of-Thought; CoT）の鍵・値キャッシュ（KV キャッシュ）を減らす文脈圧縮と、次の複数トークンを予測する先読みを、一つの追加学習手順で実現する方式である。

- **2026-04 · [GenericAgent: A Token-Efficient Self-Evolving LLM Agent via Contextual Information Density Maximization (V1.0)](2026-2604.17091-genericagent-a-token-efficient-self-evolving-llm-agent-via-contextual-in.md)**  
  実装：[✓](https://github.com/lsdefine/GenericAgent) ・ リポジトリ内被引用：1  
  GenericAgent（GA）は、この問題を単純な長文対応ではなく、限られた文脈内の意思決定に有効な情報密度を高めるシステム設計として扱う。論文は複数のエージェント基盤との比較を行い、5種類の長期タスクでGAとClaude コードがともに100%成功しながら、GAの総トークン数が188,829、比較方式が537,413だったと報告する。

- **2026-04 · [Equifinality in Mixture of Experts: Routing Topology Does Not Determine Language Modeling Quality](2026-2604.14419-equifinality-in-mixture-of-experts-routing-topology-does-not-determine-l.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  著者は学習可能な重心ベクトルとの余弦類似度で専門家を選ぶ幾何学的ルータを作り、一段で多数の専門家を選ぶ方式、複数段で少数ずつ選び直す方式、段ごとの射影を変える方式などを比較した。

- **2026-04 · [Characterizing Vision-Language-Action Models across XPUs: Constraints and Acceleration for On-Robot Deployment](2026-2604.24447-characterizing-vision-language-action-models-across-xpus-constraints-and.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文は、視覚・言語・行動モデル（Vision-Language-Action、VLA）をロボットに搭載するときの「制御周期内に推論を終えられるか」「何ワット時・いくらで実行できるか」という推論システムの問題を扱う。

- **2026-04 · [AEGIS: Scaling Long-Sequence Homomorphic Encrypted Transformer Inference via Hybrid Parallelism on Multi-GPU Systems](2026-2604.03425-aegis-scaling-long-sequence-homomorphic-encrypted-transformer-inference-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  AEGISは、完全準同型暗号（fully homomorphic encryption; FHE）で暗号化した入力を復号せずにTransformerへ通す際、複数GPUへ暗号文を分配する方法を最適化するシステムである。

- **2026-03 · [TIDE: Token-Informed Depth Execution for Per-Token Early Exit in LLM Inference](2026-2603.21365-tide-token-informed-depth-execution-for-per-token-early-exit-in-llm-infe.md)**  
  実装：[✓](https://github.com/RightNow-AI/TIDE) ・ リポジトリ内被引用：1  
  TIDE（Token-Informed Depth Execution）は、学習済み大規模言語モデル（LLM）の中間層における隠れ状態が最終層の表現へ近づいたかを、後付けの小規模な二値分類器で判定する方式である。元の言語モデルの重みを変更せず、約2,000件のWikiText-103文による較正をA100上で約170秒で実行できる点が実装上の特徴である。

- **2026-03 · [Multi-Head Low-Rank Attention](2026-2603.02188-multi-head-low-rank-attention.md)**  
  実装：[✓](https://github.com/SongtaoLiu0823/MLRA) ・ リポジトリ内被引用：1  
  長文脈の自己回帰型言語モデルでは、次トークンを出すたびに過去トークンのキー・値（KV）キャッシュを高帯域メモリ（HBM）から演算器近傍へ読み込む。多頭潜在注意（Multi-Head Latent 注意機構; MLA）はKVを低次元の潜在状態へ圧縮することで転送量を減らすが、元のMLAでは潜在KVが一つの共有状態として保持される。

- **2026-03 · [Gumbel Distillation for Parallel Text Generation](2026-2603.22216-gumbel-distillation-for-parallel-text-generation.md)**  
  実装：[✓](https://github.com/hxixixh/gumbel-distill) ・ リポジトリ内被引用：1  
  自己回帰言語モデル（autoregressive language モデル）は、前のトークンを条件に次の一個を順番に予測するため、隣接する語の依存関係を扱いやすい。例えば「San Francisco」を同時に予測する場合、「San」を選んだ条件で「Francisco」を選ぶという自己回帰的な関係が明示されない。

- **2026-03 · [GradMem: Learning to Write Context into Memory with Test-Time Gradient Descent](2026-2603.13875-gradmem-learning-to-write-context-into-memory-with-test-time-gradient-de.md)**  
  実装：[✓](https://github.com/yurakuratov/gradmem) ・ リポジトリ内被引用：1  
  長文脈の大規模言語モデル（LLM）では、過去の情報を再利用するために鍵・値キャッシュ（KV キャッシュ）を保持するのが一般的である。しかしキャッシュは通常、層数と文脈長に比例して増える。GradMemはこの記憶形成を、単なる順伝播による要約ではなく、推論時に小さな記憶ベクトルへ勾配降下を行う最適化問題として定義する。モデル本体の重みは推論時に更新しない。

- **2026-03 · [Compressing Language Models for Specialized Domains](2026-2502.18424-compressing-language-models-for-specialized-domains.md)**  
  実装：[✓](https://github.com/mlsw/domain-compression) ・ リポジトリ内被引用：1  
  言語モデルを量子化・剪定して配備コストを下げると、汎用ベンチマークの正解率が比較的よく残っていても、医療・法務などの専門領域の精度が大きく落ちる場合がある。

- **2026-03 · [ArcLight: A Lightweight LLM Inference Architecture for Many-Core CPUs](2026-2603.07770-arclight-a-lightweight-llm-inference-architecture-for-many-core-cpus.md)**  
  実装：[✓](https://github.com/OpenBMB/ArcLight) ・ リポジトリ内被引用：1  
  NUMAごとのメモリ配置、動的スレッド群、Scatter/Gather型テンソル並列を一体化し、多数コアCPUの遠隔メモリアクセス壁を避けて、192コアARM環境でllama.cpp比最大46%高い推論スループットを示す軽量CPU推論基盤。

- **2026-03 · [AgentCollab: A Self-Evaluation-Driven Collaboration Paradigm for Efficient LLM Agents](2026-2603.26034-agentcollab-a-self-evaluation-driven-collaboration-paradigm-for-efficien.md)**  
  実装：[✓](https://github.com/SparkEngineAI/AgentFlashInfer) ・ リポジトリ内被引用：1  
  ステップごとにモデル自身が進捗を自己評価し、停滞時だけ大きいモデルへ一時的に制御を移す協調方式で、エージェントの正解率を大きいモデル並みに近づけつつ1.3から2.4倍の高速化を得た。

- **2026-03 · [3BASiL: An Algorithmic Framework for Sparse plus Low-Rank Compression of LLMs](2026-2603.01376-3basil-an-algorithmic-framework-for-sparse-plus-low-rank-compression-of-.md)**  
  実装：[✓](https://github.com/mazumder-lab/3BASiL) ・ リポジトリ内被引用：1  
  重みの疎＋低ランク分解を3ブロックの交互方向乗数法で同時最適化し、ブロック単位の出力整合で精緻化する一括圧縮で、困惑度の劣化を3割超縮め圧縮も2.5倍超高速化した。

- **2026-02 · [ThinkRouter: Efficient Reasoning via Routing Thinking between Latent and Discrete Spaces](2026-2602.11683-thinkrouter-efficient-reasoning-via-routing-thinking-between-latent-and-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  思考ステップごとにモデルの確信度を見て、低確信なら離散トークン、高確信なら潜在空間の柔らかい埋め込みへ振り分ける学習不要の方式で、正解率を最大19.70ポイント上げながら生成長も削った。

- **2026-02 · [SALAAD: Sparse And Low-Rank Adaptation via ADMM for Large Language Model Inference](2026-2602.00942-salaad-sparse-and-low-rank-adaptation-via-admm-for-large-language-model-.md)**  
  実装：[✓](https://github.com/HaoMAFRLu/salaad) ・ リポジトリ内被引用：1  
  SALAADは、言語モデルの重みを疎成分と低ランク成分の和として表現できるように事前学習中から構造を誘導し、配置時には必要なメモリ予算に応じて同じ学習済みチェックポイントを縮小できる方式である。

- **2026-02 · [ReviveMoE: Fast Recovery for Hardware Failures in Large-Scale MoE LLM Inference Deployments](2026-2602.21140-revivemoe-fast-hardware-failure-recovery.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  単一NPU障害時にサービング全体を再起動せず、要求状態・KVブロック表・MoE重み・通信領域・実行グラフを局所修復して大規模MoE推論を高速復旧する。

- **2026-02 · [Optimal Bayesian Stopping for Efficient Inference of Consistent LLM Answers](2026-2602.05395-optimal-bayesian-stopping-for-efficient-inference-of-consistent-llm-answ.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  自己整合性のサンプリング停止に分布形状の事前情報を入れた最適ベイズ停止を定式化し、最頻・第2位・その他の3区分を数える集約事後で漸近最適性が得られることを証明して、呼び出し回数を最大約5割削減する。

- **2026-02 · [On the Limits of Layer Pruning for Generative Reasoning in Large Language Models](2026-2602.01997-on-the-limits-of-layer-pruning-for-generative-reasoning-in-large-languag.md)**  
  実装：[✓](https://github.com/safal312/on-the-limits-of-layer-pruning) ・ リポジトリ内被引用：1  
  本研究は大規模言語モデルの層を丸ごと削る深さ方向の枝刈り（層 枝刈り）が、分類課題と生成型推論課題で異なる品質低下を起こす原因を調べる。主な実験では、層の約25%を除去し、元モデルが生成した回答を教師にして再学習する。

- **2026-02 · [Neural Attention Search Linear: Towards Adaptive Token-Level Hybrid Attention Models](2026-2602.03681-neural-attention-search-linear-towards-adaptive-token-level-hybrid-atten.md)**  
  実装：[✓](https://github.com/automl/NeuralAttentionSearchLinear) ・ リポジトリ内被引用：1  
  NAtS-L（Neural 注意機構 Search Linear）は、従来の「ある層はソフトマックス注意、別の層は線形注意」という固定的な混成構成を、同じ層の中で入力トークン塊ごとに注意演算を選択する構成へ拡張した研究である。

- **2026-02 · [Improving Sampling for Masked Diffusion Models via Information Gain](2026-2602.18176-improving-sampling-for-masked-diffusion-models-via-information-gain.md)**  
  実装：[✓](https://github.com/yks23/Information-Gain-Sampler) ・ リポジトリ内被引用：1  
  モデルの再学習を要しない復号時のアルゴリズムである。Dream-7B-Instructで数学・コード・計画の6課題を評価した原著表2では、復号率K=2の平均正解率が53.4%、K=1で62.0%となる。

- **2026-02 · [Data Distribution Matters: A Data-Centric Perspective on Context Compression for Large Language Model](2026-2602.01778-data-distribution-matters-a-data-centric-perspective-on-context-compress.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長文脈の大規模言語モデル（LLM）では、入力の全トークンをそのまま処理するより、先に少数の潜在表現へ圧縮して復元器へ渡す方法が考えられる。

- **2026-02 · [Conformal Thinking: Risk Control for Reasoning on a Compute Budget](2026-2602.03814-conformal-thinking-risk-control-for-reasoning-on-a-compute-budget.md)**  
  実装：[✓](https://github.com/xidulu/reasoning_risk_control/) ・ リポジトリ内被引用：1  
  Conformal Thinkingは、推論を伴う大規模言語モデル（reasoning LLM）の思考トークンを、精度への影響を制御しながら減らす停止規則を提案する。

- **2026-02 · [CoMoL: Efficient Mixture of LoRA Experts via Dynamic Core Space Merging](2026-2603.00573-comol-efficient-mixture-of-lora-experts-via-dynamic-core-space-merging.md)**  
  実装：[✓](https://github.com/DCDmllm/CoMoL) ・ リポジトリ内被引用：1  
  本論文は、低ランク適応（LoRA）を複数の専門家へ拡張する際に、専門家の数に比例して増える学習パラメータと計算量を抑えつつ、トークン単位の細かな経路選択を維持するCoMoLを提案する。

- **2026-01 · [Why Attention Patterns Exist: A Unifying Temporal Perspective Analysis](2026-2601.21709-why-attention-patterns-exist-a-unifying-temporal-perspective-analysis.md)**  
  実装：[✓](https://github.com/MIRALab-USTC/LLM-TAPPA) ・ リポジトリ内被引用：1  
  KVキャッシュ圧縮では検索型の不規則な注意が多い、自己類似度の低い層に多めのKV予算を配る。

- **2026-01 · [VTC-R1: Vision-Text Compression for Efficient Long-Context Reasoning](2026-2601.22069-vtc-r1-vision-text-compression-for-efficient-long-context-reasoning.md)**  
  実装：[✓](https://github.com/w-yibo/VTC-R1) ・ リポジトリ内被引用：1  
  本研究は、長い思考履歴を文字列として保持し続ける代わりに、既に生成した推論を画像へ描画して次の推論段階へ渡す視覚・テキスト圧縮（Vision-Text Compression; VTC）を提案する。約1億8100万のテキストトークンに相当する履歴を約5400万の視覚トークンとして表し、集計上3.4倍のトークン圧縮を得る。

- **2026-01 · [Towards Compute-Aware In-Switch Computing for LLMs Tensor-Parallelism on Multi-GPU Systems](2026-161bea97e0de-towards-compute-aware-in-switch-computing-for-llms-tensor-parallelism-on-multi-gpu-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  NVLSの通信意味論をLLM計算カーネルの読み書き要求へ合わせ、スイッチ内要求マージ・GPU間TB協調・データフロー重畳でテンソル並列の通信待ちを削減する。

- **2026-01 · [The Perplexity Paradox: Why Code Compresses Better Than Math in LLM Prompts](2026-2602.15843-the-perplexity-paradox-why-code-compresses-better-than-math-in-llm-promp.md)**  
  実装：[✓](https://github.com/micoverde/taac-llm-compression) ・ リポジトリ内被引用：1  
  本研究は、大規模言語モデル（LLM）へ渡す入力文を短縮する際、言語モデルが予測しにくいトークンと、下流の課題を解くために残すべきトークンが一致するとは限らないという問題を扱う。関数署名再挿入では正答率が5.3%から39.3%へ34.0ポイント回復した。

- **2026-01 · [Low-Rank Key Value Attention](2026-2601.11471-low-rank-key-value-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  低ランク鍵・値注意（Low-Rank Key Value 注意機構; LRKV）は、Transformerの各注意ヘッドが別々に保存する鍵・値（key/value; KV）キャッシュの重複を減らすため、各層に一組の共有射影を持たせ、ヘッド固有の違いだけを低ランク残差で表す注意機構である。

- **2026-01 · [Exploring Fine-Tuning for In-Context Retrieval and Efficient KV-Caching in Long-Context Language Models](2026-2601.18527-exploring-fine-tuning-for-in-context-retrieval-and-efficient-kv-caching-.md)**  
  実装：[✓](https://github.com/amazon-science/icr-kv-caching-long-context-llms) ・ リポジトリ内被引用：1  
  長文脈LLMの文脈長が数十万〜100万トークンに伸びても、大量の文書から正しい証拠を見つける能力が必ずしも高いとは限らない。検索拡張生成（Retrieval-Augmented Generation; RAG）は事前に関連文書を検索するため効率的だが、検索索引の構築・運用が必要である。HotpotQA単体では61.0→81.1と20.1ポイント改善した。

- **2026-01 · [ArcAligner: Adaptive Recursive Aligner for Compressed Context Embeddings in RAG](2026-2601.05038-arcaligner-adaptive-recursive-aligner-for-compressed-context-embeddings-.md)**  
  実装：[✓](https://github.com/liunian-Jay/ArcAligner) ・ リポジトリ内被引用：1  
  ArcAlignerは、検索拡張生成（Retrieval-Augmented Generation; RAG）で取得した長文書を、少数の連続ベクトルへ圧縮した後の「情報が残っていても生成モデルが読めない」という問題を扱う。約24倍の文脈圧縮条件で、HotpotQAのF1は34.92、同じ論文で比較したCOCOMの16倍圧縮は31.77となった。

- **2025-12 · [Rethinking Chain-of-Thought Reasoning for Videos](2025-2512.09616-rethinking-chain-of-thought-reasoning-for-videos.md)**  
  実装：[✓](https://github.com/LaVi-Lab/Rethink_CoT_Video) ・ リポジトリ内被引用：1  
  本論文は、長い人間風の思考列が動画理解に必須かを疑い、短い推論文、視覚トークン圧縮、強化学習による事後学習を組み合わせる代替構成を検証する。

- **2025-12 · [LLMCache: Layer-Wise Caching Strategies for Accelerated Reuse in Transformer Inference](2025-2512.16843-llmcache-layer-wise-caching-strategies-for-accelerated-reuse-in-transfor.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LLMCacheは、入力文字列が完全一致しなくても意味的に似ていればTransformer内部の中間活性を再利用できると考え、各層の出力を入力の指紋とともに保存する推論方式である。

- **2025-12 · [Interleaved Latent Visual Reasoning with Selective Perceptual Modeling](2025-2512.05665-interleaved-latent-visual-reasoning-with-selective-perceptual-modeling.md)**  
  実装：[✓](https://github.com/XD111ds/ILVR) ・ リポジトリ内被引用：1  
  既存の方法には、画像を切り出す外部道具を繰り返し呼ぶもの、中間画像を新たに生成するもの、画像の特徴を短い潜在ベクトルへ圧縮するものがある。Qwen2.5-VL-7Bでの原著評価では、COMTの平均正答率60.8%、VSPの正答率81.5%を達成し、静的潜在方式Mirageの56.0%・76.0%を上回った。

- **2025-12 · [HFS: Holistic Query-Aware Frame Selection for Efficient Video Understanding](2025-2512.11534-hfs-holistic-query-aware-frame-selection-for-efficient-video-understandi.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  質問の意図を潜在クエリとして抽出し、関連度・被覆・冗長性を束ねた集合目的と選択器・推論器の相互学習でフレーム集合そのものを最適化し、16フレームで従来の選択法を上回る精度と小さい追加遅延を両立した。

- **2025-12 · [From Context to EDUs: Faithful and Structured Context Compression via Elementary Discourse Unit Decomposition](2025-2512.14244-from-context-to-edus-faithful-and-structured-context-compression-via-ele.md)**  
  実装：[✓](https://github.com/DeepLangAI/LingoEDU) ・ リポジトリ内被引用：1  
  LingoEDUは、長い文章を単純にトークン単位で間引くのではなく、まず原文の談話構造を木として抽出し、その木から質問に必要な範囲だけを選択して入力を短縮する、明示的な文脈圧縮方式である。著者は248文書を人手で構造注釈したStructBenchを公開し、木編集距離4.77、文書単位完全一致率49.60%を報告した。

- **2025-12 · [DiRL: An Efficient Post-Training Framework for Diffusion Language Models](2025-2512.22234-dirl-an-efficient-post-training-framework-for-diffusion-language-models.md)**  
  実装：[✓](https://github.com/OpenMOSS/DiRL) ・ リポジトリ内被引用：1  
  提案はこの問題を、ブロック間は自己回帰的、ブロック内は並列的な拡散という構造で扱う。著者は、学習処理の遅延を約6分の1にし、学習・推論の統合によって全体処理量を約2.5倍改善したと報告する。

- **2025-12 · [Asynchronous Reasoning: Training-Free Interactive Thinking LLMs](2025-2512.10931-asynchronous-reasoning-training-free-interactive-thinking-llms.md)**  
  実装：[✓](https://github.com/yandex-research/AsyncReasoning) ・ リポジトリ内被引用：1  
  推論時計算を増やすほど対話の即応性が下がるという問題である。二つの流れがそれぞれ通常の「入力→思考→回答」という順序で文脈を見ているように、鍵・値キャッシュ（KV キャッシュ）の論理的な並びを切り替える。

### 直近12か月・未被引用（2025-12〜2026-11）

- **2026-11 · [Specification-Guided Generation for Large Language Models](2026-2610.41511-specification-guided-generation-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文法では表せない変数同士の論理の制約を、各割当ての前に可能な領域を計算して文法へ変換することで生成の構成により保証し、模型の呼び出しを却下標本化より大幅に減らし、後戻りで促しに合わない割当てを九十八件中九十二件から十三件へ減らしたと報告した。

- **2026-11 · [Shallow Encoding Emits Deep Memories](2026-2611.06084-shallow-encoding-emits-deep-memories.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ハイブリッドモデルの「深い記憶の書き込みは浅い層から出せる」「再帰状態はシンク＋低ランク」という二性質を使い、プリフィルの層数を最大63%まで削り再帰状態を2.0〜3.9倍小さくして、公式試験ほぼ無損失のままスループットを1.2〜1.4倍にするサービング手法SEED。

- **2026-11 · [Scout Before You Route: Predicting Task Success and Token Count from a Small LLM Prefill](2026-2611.09028-scout-before-you-route-predicting-task-success-and-token-count-from-a-sm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  凍結した小さいモデルのプリフィル活性値から候補ごとの成功確率と出力長を線形プローブで予測するルータを提案し、中央値価格付けに対して精度をそろえた支出を9データセット中8つで9.4%から33.0%削減した。

- **2026-11 · [Quantizing Recurrent Language Models Is Easier Than You Think](2026-2611.01864-quantizing-recurrent-language-models-is-easier-than-you-think.md)**  
  実装：[✓](https://github.com/camail-official/LoReS) ・ リポジトリ内被引用：0  
  リカレント言語モデルの量子化を状態外と状態内へ分け、減衰型リカレンスは外れ値が弱く量子化しやすいことと、バリュー軸グルーピング・減衰ベース混合精度・確率的丸めからなるLoReSで状態を8ビット化しても大規模ハイブリッドの精度がほぼ保たれることを示す研究。

- **2026-11 · [PURA: Video Token Pruning via Unified Spatiotemporal Redundancy Assessment](2026-2611.34521-pura-video-token-pruning-via-unified-spatiotemporal-redundancy-assessmen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各視覚トークンの空間参照と時間参照を表現誤差と重要度からなる1つの除去コストで競わせ、動画ごとに空間と時間の枝刈り配分を自動で決める学習不要の圧縮で、圧縮自体の時間を111.7倍短縮し保持率5パーセントでも比較対象の10パーセント時を上回る精度を保った動画トークン枝刈り。

- **2026-11 · [One Schedule Does Not Fit All: Adaptive Inference Schedules for Diffusion Language Models](2026-2611.25895-one-schedule-does-not-fit-all-adaptive-inference-schedules-for-diffusion.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  固定のノイズ除去スケジュールが最適でないことを示し、ペア校正と同時ブートストラップ限界で効用と退化ガードレールを一緒に認証して最安の候補だけを配備し、駄目なら完全スケジュールへ戻る配備ルールで、デノイザ評価回数をタスクにより1.33倍から8.0倍まで減らすことを認証した研究。

- **2026-11 · [Keep the Reasoning, Read the Image: On-Demand Visual KV for Multi-Turn Reasoning VLMs](2026-2611.23769-keep-the-reasoning-read-the-image-on-demand-visual-kv-for-multi-turn-rea.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い推論が画像のKVエントリを押し出す問題に対し、全視覚エントリをCPUメモリに退避して削除を防ぎ、各ステップで現在のクエリが必要とする分だけをテキストの低評価スロットと交換して読む、既存の保持方針へ被せる学習不要のオンデマンド読み出し方式。

- **2026-11 · [Isonomy: Isolating Every Request from Timing Side Channels at Nearly Full-Sharing Throughput in Multi-Instance LLM Prefill](2026-2611.27596-isonomy-isolating-every-request-from-timing-side-channels-at-nearly-full.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  接頭辞キャッシュのヒットが最初のトークンの到着時刻から漏れる問題に対し、キャッシュ自体は全体で共有したまま、共有グループ外のヒットだけを予測ゲートと仮想リクエスト実行の2方式で隠し、リクエスト単位の隔離でも無防備な共有の0.98のスループットを保つプリフィル防御。

- **2026-11 · [HiSA: Sparsifying the Hidden Dimension of RoPE Attention in LLMs](2026-2611.26363-hisa-sparsifying-the-hidden-dimension-of-rope-attention-in-llms.md)**  
  実装：[✓](https://github.com/ambroise-b/hisa) ・ リポジトリ内被引用：0  
  回転位置埋め込みの速い周波数ペアは遠距離で不要だという仮説から、角度予算を超えたペアのスコア部分だけを位置だけで静的に落とす隠れ次元疎化を提案し、内積の約3割の計算で検証損失を密な注意より下げ、KVキャッシュ削減とデコード高速化まで示した研究。

- **2026-11 · [HiCal: Offline Calibration for Hierarchical Scale Encoding in Accurate HiF4 Quantization](2026-2611.32624-hical-offline-calibration-for-hierarchical-scale-encoding-in-accurate-hi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HiF4の3階層スケール符号化の丸めバイアスと2つの拡張しきい値だけをオフライン校正で実分布に合わせ、ブロックごとの候補探索なしに量子化誤差を9.91〜23.50パーセント減らし、下流精度の平均も改善した軽量な量子化校正。

- **2026-11 · [GreenDynaMix: Thermal-Aware Dynamic Mixed-Precision MoE LLM Inference Systems](2026-2611.31737-greendynamix-thermal-aware-dynamic-mixed-precision-moe-llm-inference-sys.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DVFSのPID制御でGPU温度と老化を抑え、失うスループットをMoEエキスパートの動的混合精度で補い、高精度配分をルータ重みで決めることで、3種のプラットフォームで老化率を25〜33%下げつつスループット維持とPPL悪化0.9〜1.6%を両立した。

- **2026-11 · [FrontierReplay: Split-Free Exact Prefix Caching for Hybrid Language Models](2026-2611.26020-frontierreplay-split-free-exact-prefix-caching-for-hybrid-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ハイブリッドモデルでプリフィックス再利用が終わる位置はターンの境界など予測可能だと実測し、プリフィルを切断せず回帰層の入力ログから状態だけを再計算して正確なチェックポイントを作ることで、有効スループットを最大4.26倍にし初回トークン時間を最大89パーセント減らしたキャッシュ方式。

- **2026-11 · [flash-comm: Self-Synchronizing Collective Communication for LLM Decoding](2026-2611.06634-flash-comm-self-synchronizing-collective-communication-for-llm-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  データブロック自体に準備完了の証拠を持たせてGPU間バリアを定常状態から外す自己同期型の集合通信で、8台のB300でオールリデュース遅延の中央値を28.8パーセント減らし、デコードのTPOTを最大6.8パーセント下げた。

- **2026-11 · [Efficient and Robust Drafting with Multi-Token Prediction](2026-2611.25813-efficient-and-robust-drafting-with-multi-token-prediction.md)**  
  実装：[✓](https://github.com/google-research/gemma4-mtp-drafter-domain-adaptation) ・ リポジトリ内被引用：0  
  対象モデルの活性値とKVキャッシュを共有する単一の4層ドラフトヘッドで複数トークンを自己回帰的に予測し、プリフィルと全語彙射影の費用を削ることで、Gemma 4の31BでH100上3.14倍、スマートフォンのGPU上でE4Bが2.18倍の追加学習なし高速化を実測した複数トークン予測法。

- **2026-11 · [DiFiT: Distribution-Fidelity-guided Visual Token Pruning for Multimodal Large Language Models](2026-2611.15069-difit-distribution-fidelity-guided-visual-token-pruning-for-multimodal-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  枝刈りで答えが変わらなくても応答確率がずれる予測ドリフトを定量化し、全トークン版の応答分布に合わせる蒸留と複数予算のマスク学習で選択器だけを学習することで、視覚トークン10パーセント保持でも平均性能89.36パーセント保持とサンプリング反転の30.3パーセント削減を示した視覚トークン枝刈り。

- **2026-11 · [Cruella: A Unified Microscaling and Floating-Point Dot-Product Unit for LLM Inference on FPGAs](2026-2611.27323-cruella-a-unified-microscaling-and-floating-point-dot-product-unit-for-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MXFP4とBF16の両方の積を1つのDSP配列で実行する統一ドット積ユニットをFPGAへ実装し、別置き構成よりDSP23パーセントとLUT36パーセントを削減しながら、MXFP4重みによるデコード1.15から1.87倍を実機で示すハードウェア研究。

- **2026-11 · [Concise-9B: Removing the Slack from a Reasoning Model's Thinking](2026-2611.02278-concise-9b-removing-the-slack-from-a-reasoning-model-s-thinking.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  答えが固まった後の思考であるスラックを強制読み出しで測り、最短の正解サンプルで自己学習して除去する研究。未見8983問でトークンを0.66倍にし、正解率は同等範囲を維持する。

- **2026-11 · [CanopyKV: Remember beyond the Crop for Fast Active Visual Reasoning](2026-2611.24373-canopykv-remember-beyond-the-crop-for-fast-active-visual-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  能動的な視覚推論で、切り出しの親子関係から新しい視野で置き換わらない補完証拠を残し、履歴を固定して継続状態を守ることで、全量保持の約4分の1のKVキャッシュで正解率と課題完了速度をともに改善した学習不要のKV圧縮方式。

- **2026-10 · [YANchor-4B: Effective Long-Horizon Reasoning in O(N) Time with O(1) Memory](2026-2610.10118-yanchor-4b-effective-long-horizon-reasoning-in-o-n-time-with-o-1-memory.md)**  
  実装：[✓](https://github.com/RocoreMatrix/YANchor) ・ リポジトリ内被引用：0  
  回帰圧縮と局所注意に、重要度で残す検索可能な記憶アンカーを加え、生成時間は長さに比例しメモリは一定のまま、AIME平均82.93パーセントの長距離推論を実現する4B級モデル。

- **2026-10 · [Weighted State Souping for Efficient Long-Context Retrieval](2026-2610.25621-weighted-state-souping-for-efficient-long-context-retrieval.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キャッシュしたチャンク状態をクエリ依存の重みで合成する方式で、混み合った長文脈でも選択的検索を保ち、上位N件だけ使うスパース版では符号化コストを文脈長ほぼ非依存にする。

- **2026-10 · [V-CoLA: Vision Token Compression with Linear Attention](2026-2610.11251-v-cola-vision-token-compression-with-linear-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  線形注意の再帰状態への再構成のされ方から画像トークンの重要度を測り、重要度密度に応じた適応的マージで圧縮することで、ハイブリッド視覚言語モデルでトークン半減でも性能の99.5パーセントを保ちプリフィルを最大6.15倍速くする学習不要の圧縮法。

- **2026-10 · [UNREAL: Unifying Retrieval and Long-Context with a Single Model](2026-2610.08463-unreal-unifying-retrieval-and-long-context-with-a-single-model.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  凍結LLMの内部表現と学習した検索トークンだけで証拠チャンクを選び、外部検索モデルなしにコーパス検索と長文脈推論を一つの選択機構で統一する方式。

- **2026-10 · [The Physical Cost of Context: Quality-Constrained Resource Accounting for Coding Agents](2026-2610.34763-the-physical-cost-of-context-quality-constrained-resource-accounting-for.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文脈方針の評価を論理トークンから実行プリフィル・KV滞在・エネルギーへ直し、品質ゲートを通った方針だけを比べる会計手順で、先読みは呼出しとエネルギーを3割強減らす一方、履歴削除はトークンを減らしても実行量を6倍に増やすことを示す。

- **2026-10 · [TAP: Efficient Long-Horizon Agent Pruning via Trajectory-Anchored Recovery](2026-2610.09074-tap-efficient-long-horizon-agent-pruning-via-trajectory-anchored-recover.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  教師軌跡へ文脈を固定したオンポリシー蒸留と、その回復目的によるチャネル再評価を交互に回す反復プルーニングで、RL訓練エージェントのFFNを60〜80パーセント削ってもタスク成功率を大きく保ち、成功あたり費用を下げる枠組み。

- **2026-10 · [Static Bootstrap Placement for Encrypted Language Model Decoding](2026-2610.04912-static-bootstrap-placement-for-encrypted-language-model-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  一つの静的な配置規則で暗号化デコードのブートストラップ費用を文脈長の閉形式にし、トークン選択から書き戻しまで暗号の下でループ全体をサーバ側で回してクライアントをオフラインにする方式。

- **2026-10 · [Spectral-MoE: Heterogeneous Per-Layer Expert Utilization in Dense-to-MoE Conversion](2026-2610.19232-spectral-moe-heterogeneous-per-layer-expert-utilization-in-dense-to-moe-.md)**  
  実装：[✓](https://github.com/ZacharyBroveak/Spectral-MoE) ・ リポジトリ内被引用：0  
  密モデルから混合専門家モデルへの変換で、トークンあたり総予算を厳密に保ちながら層ごとのエキスパート使用数を静的またはトークン動的に学習して配分し直し、同じ使用率の一律配分より品質を改善する手法。

- **2026-10 · [Sparse Text Diffusion under Dual Budgets: Context Connectivity and Expert Activation](2026-2610.41487-sparse-text-diffusion-under-dual-budgets-context-connectivity-and-expert.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文章拡散の費用を注意の辺と専門家の活性化の二予算に分けて定式化し、報告された疎な専門家構成が要約の集計で ROUGE-1 四十四・四一と二つの比較対象を上回り十六キロトークンまで優位を保つ一方、費用の測定条件は未指定で主張の範囲が限られることを切り分けた。

- **2026-10 · [SEIS: Self-Evolving Inference Systems](2026-2610.04646-seis-self-evolving-inference-systems.md)**  
  実装：[✓](https://github.com/smth-fun/self-evolving-inference-system) ・ リポジトリ内被引用：0  
  個別のGPUカーネルだけを最適化するのではなく、モデル層、正規化、量子化、注意計算、KVキャッシュ、CPU側のスケジューラ、CUDAグラフ、トークン選択、投機的復号までを同じ目的関数のもとで改修する。中心実験では、Qwen3-0.6BをNVIDIA H100 80GBの単一GPUで、単一要求の貪欲復号として実行する。

- **2026-10 · [Revisiting Cauchy–Schwarz Norm Bounds for SDC Detection in LLM Inference](2026-2610.18557-revisiting-cauchy-schwarz-norm-bounds-for-sdc-detection-in-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  行列積出力のノルム上限だけでサイレントデータ破損を検出する方式を故障注入で再評価し、稠密モデルの線形層ではチェックサム方式の検出能力の99パーセントを検証費用87パーセント減で保ち、MoEルーターでは55パーセントに落ちることを示した研究。

- **2026-10 · [Prune Gradually, Adapt Sparsely: Efficient Pruning of Large Language Models at Extreme Sparsity](2026-2610.41968-prune-gradually-adapt-sparsely-efficient-pruning-of-large-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  疎化の上限を段階的に締め、各段階で小さな疎な差分だけを適応させて勾配を次の枝刈りへ使う方式で、六モデル・疎化率五〇から九〇パーセントの全条件で先行最良方式よりパープレキシティを下げ最大四二パーセント削減し、七十億の九割疎化を単一装置で保持状態五分の一・装置時間四九パーセント減で実行したと報告した。

- **2026-10 · [Parse Before You Execute: Efficient Spatial Reasoning with Executable Primitives](2026-2610.41389-parse-before-you-execute-efficient-spatial-reasoning-with-executable-pri.md)**  
  実装：[✓](https://github.com/Xiwei-web/PEPS) ・ リポジトリ内被引用：0  
  質問を座標系・対象・状態・指標の基本要素へ実行前に確定させ必要な分だけ道具で計算し検証で局所修復する枠組みで、三課題すべてで最良の正解率と、反復型方式より料金十五から二十三点五パーセント減と遅延三十二点三から三十八点二パーセント減を報告した。

- **2026-10 · [PAIR: Memory-Efficient and Fast Inference with Reading–Reasoning Fusion](2026-2610.16003-pair-memory-efficient-and-fast-inference-with-reading-reasoning-fusion.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  小さいReaderに全文脈を読ませ大きいReasonerには文脈を見せず、両者のロジットを固定重みで融合することで、大規模モデルの精度の89〜96%をKVメモリ約4分の1で保つ非対称な2モデル推論。

- **2026-10 · [PACE: Periodic and Channel-Aligned Encoding of Four-Bit Recurrent States](2026-2610.29545-pace-periodic-and-channel-aligned-encoding-of-four-bit-recurrent-states.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  再帰状態の4ビット量子化で、丸めを毎トークンから8トークンに1回へ減らし、スケールグループを大きな成分が集まる列方向へそろえ、誤差を長く保つヘッドだけ8ビットにすることで、8ビット手法に約3分の2のメモリで迫る精度を出す方式。

- **2026-10 · [Orthros: Phase-Aware Heterogeneous Attention for Efficient Transformers](2026-2610.13735-orthros-phase-aware-heterogeneous-attention-for-efficient-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  アテンションの使い分けを層ではなくプリフィルとデコードのフェーズへ移し、全トークンはスライディングウィンドウ、予測位置だけフルアテンションで処理することで、100万トークンのプリフィルを21.9倍速くしながら128Kの針探し検索をほぼ完璧に保つ統合モジュール。

- **2026-10 · [Next-Concept Modeling: Fast, Parallel Coarse-to-Fine Text Generation](2026-2610.14162-next-concept-modeling-fast-parallel-coarse-to-fine-text-generation.md)**  
  実装：[✓](https://github.com/HazyResearch/ncm) ・ リポジトリ内被引用：0  
  テキストを残差量子化の粗から細への離散コード階層へ符号化し、レベル単位で全コードを並列予測することで、拡散モデルより少ない関数評価と短い処理時間で並列生成する二段階の言語モデル。

- **2026-10 · [MX-Like Tensor Core for LLM Inference with NPU Integration via Hardware-Software Co-Design Exploration](2026-2610.26083-mx-like-tensor-core-for-llm-inference-with-npu-integration-via-hardware-.md)**  
  実装：[✓](https://github.com/KULeuven-MICAS/MX-Like-for-LLM-Inference) ・ リポジトリ内被引用：0  
  ブロック量子化のスケール形式と重み活性値の非対称精度からなる設計空間を、形式特化のデータパスとエヌピー統合で精度とシリコン両面から探索し、エフピー4域ではユーイー5エム3スケールが劣化を25.3パーセント減らしほぼ無償で得られること、高精度域ではスケールは無関係なことを示した研究。

- **2026-10 · [HyperThink: Text-to-Parameter Hypernetworks for Efficient Reasoning](2026-2610.03039-hyperthink-text-to-parameter-hypernetworks-for-efficient-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い思考トレースの逐次生成を、質問ごとにバイアス更新を予測するハイパーネットワークの1回の順伝播へ置き換え、ベクトル量子化で更新を離散パターンへ制約することで、非思考モードに近い遅延のまま思考モードの推論力を近似し、低遅延域の精度と遅延のトレードオフを改善した効率的推論の研究。

- **2026-10 · [Hybrid Computer Use: A Unified Programmatic, Semantic, and Visual Interface for General Agents](2026-2610.41432-hybrid-computer-use-a-unified-programmatic-semantic-and-visual-interface.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  計算機を使う代理人の対話面を視覚と意味と手続きの三経路で統一し、圧縮した意味の観測と一括の動作と入力直前の照合で、OSWorld 2.0 の最高の部分点と完全達成率を出し、入力トークンを五十七パーセント減らし費用を五十五パーセント下げたと報告した。

- **2026-10 · [FuseRAG: Fusing Structure and Evidence into Inference for Cost-Efficient Graph-based RAG](2026-2610.22818-fuserag-fusing-structure-and-evidence-into-inference-for-cost-efficient-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  グラフ証拠の直列化順序最適化がNP困難であることを示し、証拠を再利用可能な潜在メモリとしてデコーダ注意へ注入し、テキストには少数の事実アンカーだけを残すことで、品質を上げながらTTFTを最大2.7倍高速化するグラフ型RAGの枠組みFuseRAG。

- **2026-10 · [FIGFLEX: A Mixed-Precision FP-INT GEMM Accelerator Co-Designed with Low-Bit LLM Quantization](2026-2610.30480-figflex-a-mixed-precision-fp-int-gemm-accelerator-co-designed-with-low-b.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みのビット数が下がるほど計算が速くなる基数4のFP-INTデータパスと、GPTQの補償後誤差でビット配分を決める量子化器を協調設計し、低ビット化をメモリだけでなく計算の利得へ変えたアクセラレータ。

- **2026-10 · [Fast and Accurate: Improving Personalized LLM Performance by Semantic Concentration Inspired Workload Split between RAG and Fine-Tuning](2026-2610.15921-fast-and-accurate-improving-personalized-llm-performance-by-semantic-con.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  履歴の意味的集中度で中核をPEFTへ、周辺をRAGへ振り分け、推論時に中核クエリの検索を省く負荷分割。

- **2026-10 · [Echo: Error-Compensated 4-Bit Tensor-Parallel Communication for LLM Training and Inference](2026-2610.14277-echo-error-compensated-4-bit-tensor-parallel-communication-for-llm-train.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  テンソル並列のオールリデュースを4ビット化し、注入される丸め誤差を二つの時間スケールのフィードバックで打ち消して蓄積を有界に抑えることで、精度をほぼ保ちながら通信を最大2.09倍高速化する方式。

- **2026-10 · [Dynamic Routing as a New Dimension for Test-time Versatility of LLMs](2026-2610.04751-dynamic-routing-as-a-new-dimension-for-test-time-versatility-of-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層のスキップと繰り返しからなる実行プログラムを、課題のデモンストレーション数件への適合とモデル自身の信頼度による調停で推論時に選ぶ学習不要の方式を検証し、MMLUとARC-AGIで思考の連鎖と相補的な精度向上と、その潜在能力が事後学習で選択不能になる過程を明らかにした研究。

- **2026-10 · [Dual DeltaNet: Value-Side Memory Reorganization for Linear Attention](2026-2610.38578-dual-deltanet-value-side-memory-reorganization-for-linear-attention.md)**  
  実装：[✓](https://github.com/ReichtumQian/DualDeltaNet) ・ リポジトリ内被引用：0  
  線形注意の固定サイズ状態に対し、キー側の値補正に加えて値の特徴からアドレスを再編成する値側デルタ則を導入し、針探し想起を大きく改善しつつデコードの演算密度も上げる両面補正の再帰モデル。

- **2026-10 · [DiffuPlex: Accelerating Full-Duplex Spoken Dialog Models via Rolling Masked Diffusion](2026-2610.12214-diffuplex-accelerating-full-duplex-spoken-dialog-models-via-rolling-mask.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全二重音声対話で80ミリ秒ごとに必要だったバックボーン計算を、マスク付き未来予測で複数フレーム分まとめて行い、信頼できる接頭辞だけを再生しながらユーザー発話との不一致では未再生分だけを書き直すことで、対話の振る舞いを保ちながら実時間で1.46倍から1.59倍に高速化した研究。

- **2026-10 · [DecisionRank: On-Policy Distillation for Decision-Model Rerankers](2026-2610.42128-decisionrank-on-policy-distillation-for-decision-model-rerankers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  生徒の現在の順位を教師に教師強制で評価させ、残り候補への条件付き選好で先頭トークンスコアを直接直す項目空間オン方策蒸留により、小さい決断モデルが27B教師を超える順位品質と24.5倍の高速化を両立した。

- **2026-10 · [DConstrain: Compiling Context-Parameterized Transitions for Diffusion Language Model Constrained Decoding](2026-2610.30920-dconstrain-compiling-context-parameterized-transitions-for-diffusion-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルの制約付きデコードで、スタックとフィールド履歴を実行時パラメータとして残す遷移プログラムへスキーマをコンパイルし、プロパティの任意順序でも厳密な同時推論を可能にしてBFCL遅延を最大46.26倍削減する方式。

- **2026-10 · [Continue or Restart? The Limits of Early Failure Prediction in Coding Agents](2026-2610.35971-continue-or-restart-the-limits-of-early-failure-prediction-in-coding-age.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  147,002件の軌跡で、早期接頭辞は同一課題の試行を偶然並みにしか分けられないこと、学習型再起動の利得は試行選択ではなく課題間配分から来ること、予算内では継続が再起動を支配することを示した。

- **2026-10 · [Clock Diffusion: Efficient Semi-Autoregressive Continuous Diffusion Language Models](2026-2610.00894-clock-diffusion-efficient-semi-autoregressive-continuous-diffusion-langu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  位置依存のノイズスケジュールでトークンごとに拡散の時計をずらし、可変長生成とKVキャッシュを連続拡散言語モデルへ持ち込んだ半自己回帰型の枠組みで、拡散モデル最良のパープレキシティ19.5を達成する。

- **2026-10 · [CacheLink: Functional KV Transport for Zero-Prefill Cross-Model Context Handoff](2026-2610.15509-cachelink-functional-kv-transport-for-zero-prefill-cross-model-context-h.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVキャッシュの再構成誤差ではなく受け手の注意と予測の振る舞いを学習信号にして、別モデルへプリフィルなしで文脈を引き継ぐCacheLinkを提案し、4モデルペア全てで最良の平均性能と32Kで最大7.27倍の引き継ぎ高速化を示す研究。

- **2026-10 · [Breaking the Space Barrier and its Application to Language Model Inference](2026-2610.09139-breaking-the-space-barrier-and-its-application-to-language-model-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  制約付き復号の経路一意性という理論結果から、強制テキストの無償化と表なしマスクと並列検証を持つ推論エンジンを構成し、ノートPCで構造化出力を高速化する研究。

- **2026-10 · [Breaking Diffusion: Parallel Reasoning with Draft Refinement](2026-2610.26542-breaking-diffusion-parallel-reasoning-with-draft-refinement.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散の逆遷移を捨て、完全な下書きを並列に書き直し、トークン自身の証拠を割り引いたキャビティエネルギーで候補を採否する推論方式で、6MモデルがCountdown-5で44.4パーセント、Sudoku-Extremeで93.9パーセントを記録する。

- **2026-10 · [Balanced State Subspaces with Spectral Rank Allocation for Mamba-2 State Compression](2026-2610.36617-balanced-state-subspaces-with-spectral-rank-allocation-for-mamba-2-state.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Mamba-2の再帰状態を座標ではなくバランス部分空間で切り詰め、ランク予算をハンケルスペクトルで層ごとに配り直すことで、状態半減でもパープレキシティ増加0.3ポイントと検索性能の97パーセント保持を両立させた学習後圧縮。

- **2026-10 · [Augment the Cache, Replace the Activation: A 2x2 Study of Internal-State Sharing](2026-2610.22026-augment-the-cache-replace-the-activation-a-2x2-study-of-internal-state-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント間の内部状態共有は担い手と融合方法の組み合わせで決まり、KVキャッシュは増強、活性値は置換が正解という非対称な規則を、同一対照階段の2×2実験で示した研究。

- **2026-10 · [ApexQuant: Data-Free Elastic Quantization by Residual Re-Isotropization](2026-2610.07904-apexquant-data-free-elastic-quantization-by-residual-re-isotropization.md)**  
  実装：[✓](https://github.com/afristrup/ApexQuant) ・ リポジトリ内被引用：0  
  残差へ毎回新しい回転を掛けて再量子化を繰り返すデータフリー量子化で、誤差の幾何級数的減衰を理論で保証し、1つの成果物の接頭辞がそのまま低精度モデルになる弾力性を持つ。

- **2026-10 · [Accordion: Elastic-Depth Inference via Fixed-Prefix Layer Looping](2026-2610.32492-accordion-elastic-depth-inference-via-fixed-prefix-layer-looping.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  中間の層の窓の先頭側を繰り返す固定した5通りの深さを1組の重みで提供し、予算に応じて推論の計算量と品質を選べるようにした専門家の混合モデル。学習の各段階を通して深さの選択肢を保持する進め方まで含めて検証している。

- **2026-09 · [You Cannot Pick a Provider From the Price List: Market-Aware Routing for Open-Weight LLM Inference](2026-2609.37902-you-cannot-pick-a-provider-from-the-price-list-market-aware-routing-for-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  同じモデルでもプロバイダで品質・遅延・価格が大きく違うことをライブ計測で示し、価格ではなくタスク条件付きの実測で最安の健全なプロバイダを選ぶルーティングと、オンラインで実行可能性を認証するFACETを提案した研究。

- **2026-09 · [Why Is Video Still So Expensive? A Survey of Inference-Efficiency Mechanisms in Video and Audiovisual LLMs](2026-2609.10355-why-is-video-still-so-expensive-a-survey-of-inference-efficiency-mechani.md)**  
  実装：[✓](https://github.com/momentslab/awesome-efficient-videollm) ・ リポジトリ内被引用：0  
  動画言語モデルの高費用を、フレーム選択・符号器・接続部・言語モデル実行の4段階のどこで削るかで125件の効率化機構を分類し、条件のそろった比較だけを集約して、保持率25パーセント前後が精度維持の目安になることと、音声側と評価規約の空白を明らかにしたサーベイ。

- **2026-09 · [When to Retrieve, When to Stay: Uncertainty-Aware Temporal Evidence Allocation for Streaming Video-LLMs](2026-2609.37345-when-to-retrieve-when-to-stay-uncertainty-aware-temporal-evidence-alloca.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  軽量エンコーダの類似度分布のエントロピーで意味検索と新しさの配分を適応させ、対象Video-LLMの視覚符号化を選ばれた観測だけに限定することで、ストリーミング動画理解の視覚処理費用を半分以下にする学習不要の証拠配分。

- **2026-09 · [Train Overcomplete, Deploy Compact: Scaling Recovery Capacity for Structured LLM Pruning](2026-2609.06974-train-overcomplete-deploy-compact-scaling-recovery-capacity-for-structur.md)**  
  実装：[✓](https://github.com/mmai-laboratory/OverRep) ・ リポジトリ内被引用：0  
  枝刈りの回復段階だけを一時的に過完備化して大きな容量で学習し、配備時には代数的に畳み込んで小型構造へ戻すことで、推論時の追加費用なしに保持性能を最大8.4ポイント上げた構造化枝刈りの回復手法。

- **2026-09 · [Toward Sustainable Distributed LLM Inference: A Systems Synthesis and Research Agenda for an Energy-, Carbon-, and Cache-Aware llm-d Control Plane](2026-2609.05565-toward-sustainable-distributed-llm-inference-a-systems-synthesis-and-res.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、LLM推論の省エネルギー化を単一のGPUカーネルや量子化手法に閉じず、分散サービングの制御面（control plane）が担う複合意思決定として再定義するシステムサーベイ兼研究課題提案である。原著の表にある2〜4倍の処理量等はPagedAttentionなど引用元の既存研究の数値であり、SICPを動かした結果ではない。

- **2026-09 · [SpliTEE: Improving LLM Inference on Trusted Hardware with Differentially Private GPU Outsourcing](2026-2609.15039-splitee-improving-llm-inference-on-trusted-hardware-with-differentially-private-gpu-outsourcing.md)**  
  実装：[✓](https://github.com/DPVault/SpliTEE) ・ リポジトリ内被引用：0  
  TEE内のLLM線形演算を差分プライバシーで保護してGPUへ委譲し、プロンプト漏洩を抑えつつCPU-only TDX推論を約2倍高速化する。

- **2026-09 · [Speech Block Influence: Component-Specific Layer Scoring for Pruning Speech LLMs](2026-2609.29343-speech-block-influence-component-specific-layer-scoring-for-pruning-spee.md)**  
  実装：[✓](https://github.com/CU-0/sbi-speechllm-pruning) ・ リポジトリ内被引用：0  
  音声LLMの層枝刈りに向け、エンコーダはアダプタ出力への影響で、デコーダはテキストトークンだけの入出力類似度で採点する部品別スコアSBIを提案し、従来のブロック影響度より高い枝刈り率まで性能を保てることと、テキストのみ較正で代替できることを示した。

- **2026-09 · [Settle: Learning When to Stop Reasoning](2026-2609.38997-settle-learning-when-to-stop-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  完了トレースの答えの安定性から停止ラベルを作り、既存の推論終了トークンへ停止判断を二値監督と参照正則化で学習させることで、通常デコードのまま推論トークンを約4割削減する手法。

- **2026-09 · [SemBridge: Compiling Consumer Observations into Cross-Stack Communication Plans](2026-2609.08231-sembridge-compiling-consumer-observations-into-cross-stack-communication-plans.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  異種CUDA/NCCL–CANN/HCCL境界で消費者が必要とする観測結果を型付き契約へコンパイルし、不要な全logit転送をトークン投影へ縮約して結果通信を99.97%以上削減する通信計画器。

- **2026-09 · [Rank-Aware Speculative Sampling for Diffusion Draft Trees](2026-2610.02251-rank-aware-speculative-sampling-for-diffusion-draft-trees.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散ドラフト木の検証で、候補を平均変位に沿って順位付けし全変動距離を最小化する順位重みで選ぶことで、対象分布の厳密さを保ったまま受理確率と対象呼出し効率を上げる検証規則。

- **2026-09 · [Post-Training Ternarization of Qwen3-4B: Capability, Effective Bit Budget, Storage Compression, and Deployment](2026-2609.01962-post-training-ternarization-of-qwen3-4b-capability-effective-bit-budget-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Qwen3-4Bの線形重み81.62%を既存の回転・残差三値化・誤差補償で事後変換し、対象重みの実効1.641ビット、保存容量8.29→3.96GiBを実証。圧縮、能力保持、実行速度を分離して検証する。

- **2026-09 · [Mid-Harness: Scaling Actions Between Model and Harness for Terminal Agents](2026-2609.39982-mid-harness-scaling-actions-between-model-and-harness-for-terminal-agent.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末エージェントは、言語モデルが提案したコマンドやファイル変更を実行環境へ送る。単一候補を実行する基準のPass@1は50.00%。

- **2026-09 · [Maverick: Private and Verifiable LLM Inference Made Practical via Matrix-Vector Multiplication Delegation](2026-2609.10264-maverick-private-and-verifiable-llm-inference-made-practical-via-matrix-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  行列ベクトル積の委譲に、符号とスパースチャレンジによる情報理論的に健全な検証とLPN系マスクのプライバシーを組み合わせ、サーバ負担ほぼゼロで私的かつ検証可能なLLM推論を実現するMaverickの研究。

- **2026-09 · [Low-Discrepancy Dither for Quantized Recurrent State Caches](2026-2609.39185-low-discrepancy-dither-for-quantized-recurrent-state-caches.md)**  
  実装：[✓](https://github.com/nssprogrammer/ssm-dither) ・ リポジトリ内被引用：0  
  再帰状態キャッシュの丸め規則として、乱数の代わりに黄金比の低不一致列を使う決定論的ディザを提案し、確率的丸めよりKLダイバージェンスを主比較の全設定で11から49パーセント下げ、最近傍丸めが長生成で崩れる理由も理論と実測で示す。

- **2026-09 · [Less Uniform Discrete Diffusion is More Powerful and Scalable](2026-2609.35817-less-uniform-discrete-diffusion-is-more-powerful-and-scalable.md)**  
  実装：[✓](https://github.com/FMD-NEXT/LUDI) ・ リポジトリ内被引用：0  
  一様拡散の損失から一様化項を取り除いたLess Uniform損失とトークン単位の時刻埋め込みで、一様拡散言語モデルを7B規模の複雑な推論まで拡張可能にした枠組み。

- **2026-09 · [Layer-Aware Position Embeddings for Visual Token Pruning in Multimodal Large Language Models](2026-2609.23715-layer-aware-position-embeddings-for-visual-token-pruning-in-multimodal-l.md)**  
  実装：[✓](https://github.com/YahongWang1/LayerPos) ・ リポジトリ内被引用：0  
  枝刈り後の位置番号を全層一律にせず、中間のグラウンディング敏感層だけ元の番号を保ち他は詰め直すことで、CDPrunerで77.8パーセント削減しても元の性能の98.2パーセントを保持する。

- **2026-09 · [LatentHarness: Learning Latent Actions for Memory and Reasoning via Counterfactual Policy Distillation](2026-2609.39740-latentharness-learning-latent-actions-for-memory-and-reasoning-via-count.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ループ型潜在推論の各ステップで、計算継続・メモリ想起・トークン発行の3行動を方策に選ばせ、全行動の1ステップ分岐で得た反実仮想利得で方策と書込みゲートを教える方式により、長文脈推論の精度を上げながら計算量を全深さの約55パーセントへ下げた。

- **2026-09 · [Interaction Effects in Hybrid Compression of Small Language Models](2026-be7fa99be335-interaction-effects-in-hybrid-compression-of-small-language-models.md)**  
  実装：[✓](https://github.com/ihebbrl/slm-hybrid-compression) ・ リポジトリ内被引用：0  
  量子化と枝刈りの併用効果から単独効果の和を差し引く相互作用係数を導入し、併用の相互作用が疎性0.2から0.3で最大になり0.5で加算へ戻る非単調な振る舞いと、課題ごとの符号の違いを明らかにした分析研究。

- **2026-09 · [HEAT: Faster Fully Homomorphic Inference via Approximations-Weights Co-Adaptation](2026-2609.01730-heat-faster-fully-homomorphic-inference-via-approximations-weights-co-ad.md)**  
  実装：[✓](https://github.com/gladia-research-group/heat) ・ リポジトリ内被引用：0  
  対象は通常のGPU推論全般ではなく、暗号文上で加算・乗算・回転を組み合わせてTransformerを評価する、非常に高コストなプライバシー保護推論である。ただし比較する平文モデルは各方式の「自分自身の平文版」であり、同一平文モデルへの忠実度を直接比較した値ではない。

- **2026-09 · [HARISSA: Inference-Time Self-Checks for Efficient and Safe Local Language Model Deployment](2026-2609.38006-harissa-inference-time-self-checks-for-efficient-and-safe-local-language.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル状態と回答状態から正しさを予測するようモデルを微調整し、安い答え方から順に試して失敗予測を飛ばし、誤答の恐れが高い回答は人へ回すカスケードで、思考連鎖に近い正解率を2.7倍低い遅延で得たローカル配備の研究。

- **2026-09 · [Gumbel Straight Flow: Distilling Autoregressive Models into One-step Flow Maps](2026-2610.00497-gumbel-straight-flow-distilling-autoregressive-models-into-one-step-flow.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  自己回帰モデルのガンベル最大化サンプリングが作る交わらない直線のノイズとデータの経路を教師とし、フローマップへ蒸留することで、並列な一段階生成を行う言語モデル。

- **2026-09 · [GSM: Efficient Language Modeling with Shared Global State](2026-2609.33465-gsm-efficient-language-modeling-with-shared-global-state.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  履歴の選択と集約をエンコーダへ集中し、デコーダ全層が直近256位置の共有KV状態だけを読む構造で、履歴長に依らないデコーダ費用とキャッシュを実現しながら、強いスパース注意ベースラインと同等の性能と64K検索能力を保ったアーキテクチャ研究。

- **2026-09 · [GroupMask: Layer-Adaptive Group-wise Sparsity for Semi-Structured LLM Pruning](2026-2609.33977-groupmask-layer-adaptive-group-wise-sparsity-for-semi-structured-llm-pru.md)**  
  実装：[✓](https://github.com/ZhengaoLi/GroupMask) ・ リポジトリ内被引用：0  
  グループ単位で保持・削除する半構造化スパース化で、全層の選択子をハイパーネットワークが生成し予算正則化と自己蒸留で学習させ、N:Mでは効かなかった層適応配分がグループ粒度では効くことを示した枝刈り手法。

- **2026-09 · [Forward-Free LLM Depth Pruning via Weight Redundancy](2026-2609.09883-forward-free-llm-depth-pruning-via-weight-redundancy.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  較正データも順伝播も使わず、チェックポイントの重み同士の類似度（射影のCKAと相対スケール）から層間冗長性を推定して深さ枝刈りの除去ブロックを決めるWRPを提案し、活性値ベース方式に迫る精度を順伝播なしで達成した。

- **2026-09 · [FlexComp: One Model for Every Ratio in Context Compression](2026-2609.11192-flexcomp-one-model-for-every-ratio-in-context-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文脈圧縮の率を学習から切り離し、予算を入力ごとにサンプリングする学習で1モデルを任意率対応にし、信頼度カスケードか予算予測器で入力ごとに率を選ぶことで、精度をほぼ保って平均最大266倍の圧縮とKVキャッシュ半減を実現する。

- **2026-09 · [Fengshui: Demystifying Chiplet Ecosystem and Bespoke Neural Network Accelerator Codesign](2026-2609.10970-fengshui-chiplet-neural-accelerator-codesign.md)**  
  実装：[✓](https://github.com/CrucibleComputingGroup/fengshui) ・ リポジトリ内被引用：0  
  再利用可能な少数チップレット群そのものと演算子単位の専用アクセラレータ構成を共同探索し、計算データフロー・メモリ・並列方式・配置配線を演算子ごとに最適化してNREを抑えつつLLM推論のエネルギー効率を高める。

- **2026-09 · [Dynamic Semantic Compression for Efficient Latent-Space Inference in Large Language Models](2026-2609.15338-dynamic-semantic-compression-latent-space-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文を長さに応じて1〜3区間へ分割し、重要トークンを重み付けした潜在表現を生成・復号するDSEI。固定文圧縮より品質を改善し、トークン単位推論より系列長とメモリ負荷を削減する。

- **2026-09 · [DimPO: Dimensionality Reduction for Attention using Preference Optimization](2026-2609.32579-dimpo-dimensionality-reduction-for-attention-using-preference-optimizati.md)**  
  実装：[✓](https://github.com/lanzv/dimpo) ・ リポジトリ内被引用：0  
  DimPOは、大規模言語モデル（LLM）の注意計算におけるクエリとキーのベクトル次元を縮める際、元の注意重みを数値的に完全再現することと、モデルの下流課題性能を保つことは別の目的だと実証する研究である。提案は、事前学習済みモデルを追加学習し直す方式ではなく、各層に一つの小さな線形写像をオフラインで学習する方式である。

- **2026-09 · [DegreeSpar: Structured Degree Sparsity for Efficient Secure Transformer Inference](2026-2609.32204-degreespar-structured-degree-sparsity-for-efficient-secure-transformer-i.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  セキュアなトランスフォーマー推論の圧縮を、非線形多項式の次数という共通空間で構造化し、次数削減とトークン・次元の計算除去を一体で最適化して、精度を保ちながら基礎方式比2.29〜6.63倍の高速化を得る研究。

- **2026-09 · [CORAL: Co-Evolutionary Optimization of Routing and Adaptive Prompts for Cost-Efficient LLM Deployment](2026-ca88519757de-coral-co-evolutionary-optimization-of-routing-and-adaptive-prompts-for-c.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プロンプトとモデルの割当てを別々に最適化する従来法の限界を示し、プロンプト集団とルータ集団を多目的共進化で同時に育てることで、同一精度での推論コストを最大31.4パーセント削減した研究。

- **2026-09 · [Compression Beyond the Uncompressed: A Two-Stage Training Recipe for Soft Context Compression in RAG](2026-2609.05152-compression-beyond-the-uncompressed-a-two-stage-training-recipe-for-soft.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  soft context compressionは文書を短い連続embeddingへ置き換え、デコーダがそのembeddingから回答する方式である。教師の失敗を模倣せず、結果報酬から改善を探索する点が重要である。

- **2026-09 · [A Tilted Bowl Is Not a Slippery Slope: Compressing Looped Models](2026-2609.39277-a-tilted-bowl-is-not-a-slippery-slope-compressing-looped-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  圧縮したループ型モデルの崩壊は誤差の蓄積ではなく静定点のずれであり、押しと部屋で崩壊を予測でき、最後の数回の8ビットループで回復できることを示し、停止と仕上げの制御器で精度を最大15ポイント上げる研究。

- **2026-08 · [VoiceMem: Streaming Dual-Brain Memory for Real-Time Interaction](2026-2608.26005-voicemem-streaming-dual-brain-memory-for-real-time-interaction.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  VoiceMemは、音声対話システムの過去会話記憶を、応答を遅らせずに少数の関連記憶へ絞るための索引・更新・検索方式である。

- **2026-08 · [VLZip: Unified Visual and Textual Compression for Interleaved Long-Context Modeling](2026-2608.08630-vlzip-unified-visual-and-textual-compression-for-interleaved-long-contex.md)**  
  実装：[✓](https://github.com/ShareLab-SII/VLZip) ・ リポジトリ内被引用：0  
  画像とテキストの両方をチャンク単位で層別ソフトプレフィックスへ蒸留し全デコーダ層へ注入することで系列を25分の1級に縮め、学習120K・推論280K超を可能にする視覚言語モデルの統合圧縮方式。

- **2026-08 · [TurboBus: Pooling PCIe Bandwidth for LLM Workloads via Scale-Up Fabrics](2026-2fe550669a96-turbobus-pooling-pcie-bandwidth-for-llm-workloads-via-scale-up-fabrics.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU間高速ファブリックを中継路として他GPUの空きPCIeリンクを借用し、モデル読込の初回トークン待ち時間を最大40%削減、鍵値退避推論を最大1.6倍高速化する。

- **2026-08 · [The Parser Already Knows: Lightweight Bias Correction in Constrained Decoding](2026-2608.10137-the-parser-already-knows-lightweight-bias-correction-in-constrained-deco.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文法マスクが壊す分布のずれを、パーサ状態・レクサ状態・候補トークンから学習した軽量補正で戻し、ビットベクトル文法でマスク比最大113倍のKL改善をマスク並みの速さで得る研究。

- **2026-08 · [TailSieve: Partial-Rollout-Guided Tail Routing for LLM Rollouts](2026-2608.22788-tailsieve-partial-rollout-guided-tail-routing-for-llm-rollouts.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TailSieveは、以前の部分生成で時間切れとなったプロンプト群を、追加の長さ予測モデルなしで長尾候補として選び、長尾専用プールと通常プールへ割り当てる。

- **2026-08 · [StreamTTT: Reconciling Real-Time Perception and Long-Term Memory in Streaming VLMs](2026-2608.13416-streamttt-reconciling-real-time-perception-and-long-term-memory-in-strea.md)**  
  実装：[✓](https://github.com/zeyun-zhong/StreamTTT) ・ リポジトリ内被引用：0  
  長期履歴を注意の外の高速重みへ書き込み、注意は直近専用の短いスライディングKVキャッシュに絞る二重メモリで、ストリーミング視覚言語モデルの知覚と想起の競合を解く方式。

- **2026-08 · [Speculative Probing: LLM Monitoring at Speculative-Decoding Cost](2026-2608.28099-speculative-probing-llm-monitoring-at-speculative-decoding-cost.md)**  
  実装：[✓](https://github.com/collinzrj/SpeculativeProbing) ・ リポジトリ内被引用：0  
  大規模言語モデルの推論サービスでは、回答を生成するだけでなく、危険な入力、指示の矛盾、推論の反復、品質の低下を実行中に検知したい場合がある。別の大規模分類モデルを動かせば高い精度が得られる可能性はあるが、モデルを追加で常駐させ、入力全体をもう一度処理する費用が発生する。ただしすべての条件でMULTIMAXより正確なわけではない。

- **2026-08 · [Rollplex: Cross-Phase GPU Spatial Sharing for Vision Language Model Post-Training](2026-2608.14498-rollplex-cross-phase-gpu-spatial-sharing-for-vision-language-model-post-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案は単なるGPU上の並列カーネル起動ではない。一方、評価に使うH800は80GBである。

- **2026-08 · [Reflection Steering: Disentangling Reflection from Reasoning in Activation Space for Token-Efficient Inference](2026-2608.25542-reflection-steering-disentangling-reflection-from-reasoning-in-activatio.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  振り返りの方向を主成分分析と一般推論方向への直交化で純化し、安定する層だけに上限付きの射影除去を適用することで、学習なしに推論トークンを平均16.9パーセント減らし、数学課題では正解率をほぼ保った活性値制御の研究。

- **2026-08 · [ProxyFormer: A Dual-Stream Proxy Architecture for Ultra-Long Context and High-Resolution Generation](2026-2608.23463-proxyformer-a-dual-stream-proxy-architecture-for-ultra-long-context-and-.md)**  
  実装：[✓](https://github.com/simonFelix-Ai/proxy-former.git) ・ リポジトリ内被引用：0  
  ローカル特徴を層ごとにプロキシへ圧縮し、大域相互作用を短いプロキシ空間だけに閉じ込め、結果をローカル側へ戻す二重ストリーム構造で、注意とKVキャッシュの費用を圧縮率の二乗・比例で削りながら情報の可逆性を保つ構造を提案した。

- **2026-08 · [PI-Mem: Pushing Long-Context Reasoning to 3.6M Tokens with Parallel-Iterative Memory](2026-2608.03048-pi-mem-pushing-long-context-reasoning-to-3-6m-tokens-with-parallel-itera.md)**  
  実装：[✓](https://github.com/JetAstra/PI-Mem) ・ リポジトリ内被引用：0  
  全区間を共有メモリで並列に読み、証拠を選んで統合するターンを反復するメモリ方式で、360万トークンでもMemAgentより最大7.81ポイント高精度かつ最大6.1倍高速を記録する。

- **2026-08 · [Performance Foundations of Parallel & Distributed Reasoning Language Models](2026-2608.27046-performance-foundations-of-parallel-distributed-reasoning-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RLM後学習を仕事量・深さ・メモリで形式化し、モデル内6種の並列化と配置・段階融合・非同期化を統一分類して、長い自己回帰生成が支配する分散RLの設計原理を整理する。

- **2026-08 · [ParaTempo: Efficient Parallel Reasoning via Temporal Confidence](2026-2608.16425-paratempo-efficient-parallel-reasoning-via-temporal-confidence.md)**  
  実装：[✓](https://github.com/ScottZhang812/ParaTempo) ・ リポジトリ内被引用：0  
  各枝の中間答え分布を時間方向に平均した集中度で枝の収束を見極め、見込みの薄い枝を刈り、収束した枝を早期に終了させ、空いた計算を有望な枝のフォークへ回す、学習なしの非同期並列推論の制御方式。

- **2026-08 · [Not All Attention Heads Contribute to Critical Visual Token Selection: Head-Aware Pruning Matters More](2026-2608.25332-not-all-attention-heads-contribute-to-critical-visual-token-selection-he.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚トークンの重要度判定が少数の視覚ヘッドへ集中することを示し、骨格へ入る前の類似度削減と、浅い層は視覚ヘッドのみ・中間層は全ヘッドという段階的枝刈りを組み合わせ、88.9パーセント削減でも性能の95.9パーセント保持と1.62倍高速化を実現する。

- **2026-08 · [Maia 200: A Software Defined Dataflow System for Large-scale AI Acceleration](2026-2608.24664-maia-200-a-software-defined-dataflow-system-for-large-scale-ai-accelerat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Maia 200はTSMC 3nmで製造した1400億超のトランジスタを持つSoCで、750Wの熱設計電力（TDP）の下、FP4で10,145 TFLOP/s、FP8で5,072 TFLOP/s、HBM3e帯域7 TiB/sを公称する。

- **2026-08 · [Less can be More: Relieving RAG Bottlenecks via Evidence Frontloading and Pressure-Adaptive Budgeting](2026-2608.25115-less-can-be-more-relieving-rag-bottlenecks-via-evidence-frontloading-and.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  再順位付けと生成の間で律速が移動することを実測し、限界証拠被覆による証拠前倒しと待ち行列圧力に応じた予算削減を組み合わせ、HotpotQAでは半分の再順位付け件数で最終再現率を41.13から62.38へ上げた。

- **2026-08 · [Is Discrete Difficulty Sufficient? Leveraging Continuous Difficulty for Efficient Self-Consistency in LLMs](2026-2608.24590-is-discrete-difficulty-sufficient-leveraging-continuous-difficulty-for-e.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  出力エントロピーを最終トークン埋め込みから予測する線形プローブで問題の難しさを連続信号として推定し、自己整合性のサンプリング本数を問題ごとに比例配分することで、正解率をほぼ保ったままトークン消費を最大76.7パーセント削減した効率的なテスト時計算配分の研究。

- **2026-08 · [CForce: Boosting Parallel Decoding for dLLMs via Consistency Forcing](2026-2608.13925-cforce-boosting-parallel-decoding-for-dllms-via-consistency-forcing.md)**  
  実装：[✓](https://github.com/inclusionAI/dFactory) ・ リポジトリ内被引用：0  
  拡散言語モデルの自己軌跡上で初期段階の予測を後期段階へ信頼度適応型KLで合わせる自己蒸留により、編集可能なモデルでは並列度と精度を同時に上げ、並列復号の速度と品質の前線を押し広げる。

- **2026-08 · [Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory](2026-2608.07169-agent-memory-distillation-empowering-small-llm-agents-with-hierarchical-.md)**  
  実装：[✓](https://github.com/taeilkim2465/agentic_memory_distillation) ・ リポジトリ内被引用：0  
  提案手法AMD（Agent メモリ Distillation）は、教師が成功した道具呼び出し軌跡から、作業全体の戦略を示す作業手順記憶（Workflow メモリ）、実際の道具呼び出し列を示す部分作業記憶（Subtask メモリ）、個別関数の呼び方を示す関数記憶（Function メモリ）を別々に構築する。

- **2026-07 · [Your Reasoning Model Knows What Counts: Self-Guided Chain-of-Thought Pruning for Efficient Reasoning](2026-c187be9e4f6f-your-reasoning-model-knows-what-counts-self-guided-chain-of-thought-prun.md)**  
  実装：[✓](https://github.com/HammerScholar/SGP-CoT) ・ リポジトリ内被引用：0  
  推論モデルの冗長な思考を、外部監督ではなくモデル自身の尤度で測った答えへの影響と一貫性への影響で切り分け、不要な推論単位だけを外した選好学習で、長さを20〜50%削りながら正解率を保つ自己誘導型枝刈り方式。

- **2026-07 · [What to Keep, What to Forget: A Rate-Distortion View of Memory Compaction in LLMs and Agents](2026-2607.08032-what-to-keep-what-to-forget-a-rate-distortion-view-of-memory-compaction-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVキャッシュ、入力プロンプト、固定長内部状態、エージェント記憶の圧縮を率歪み最適化で統一し、7軸分類とCOMPACT-Benchを提案するサーベイ。RTX 4060・Qwen2.5-1.5Bの参照実験では、KV保持予算約25%未満でneedle検索がほぼ失敗し、反復要約の事実再現率0.33〜0.56に対して検索可能な原文アーカイブは約0.95だった。

- **2026-07 · [VDAR-Router: Adaptive LLMs Routing via Verbalized Query Difficulty Analysis Retrieval](2026-2607.18098-vdar-router-adaptive-llms-routing-via-verbalized-query-difficulty-analys.md)**  
  実装：[✓](https://github.com/NYCU-NLP-Lab/VDAR-Router) ・ リポジトリ内被引用：0  
  クエリ本文ではなく、必要な能力と難易度を言語化した分析文を検索キーにして似た難易度の過去事例を引き、その事例での性能と費用から報酬でモデルを選ぶ、学習不要の難易度認識型ルーティング。

- **2026-07 · [Token Reduction Is Not Cost Reduction](2026-2607.12161-token-reduction-is-not-cost-reduction.md)**  
  実装：[✓](https://github.com/PointFiveLabs/ai-efficiency-benchmark) ・ リポジトリ内被引用：0  
  コーディングエージェントの文脈削減を2908回の課金実行で対照測定し、費用の大半がプロンプトキャッシュであり、ツール出力を38パーセント削っても費用が6.8パーセント増えるなど、トークン削減と費用削減が切り離されることを示した実証研究。

- **2026-07 · [STEEL: Sparsity-Aware Fused Attention for Energy-Efficient Long-Sequence Inference on AMD's XDNA NPU](2026-2607.09385-steel-sparsity-aware-fused-attention-for-energy-efficient-long-sequence-.md)**  
  実装：[✓](https://github.com/amd/iron) ・ リポジトリ内被引用：0  
  FlashAttentionをデータフロー化して三段階パイプラインでニューラル処理装置へ載せ、因果マスクの疎性を意識した配置で負荷の偏りを均すSTEEL。CPU比でエネルギーを9.17分の1まで減らした。

- **2026-07 · [ST-Veto: Spatio-Temporal Token Veto for Diffusion MLLMs via Taylor Prediction and Visual Grounding](2026-2607.17884-st-veto-spatio-temporal-token-veto-for-diffusion-mllms-via-taylor-predic.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者が提案する時空間トークン拒否（Spatio-Temporal Token Veto、ST-Veto）は、ある反復で確信度が高くても、その確信度の時間変化が不安定、あるいは画像への注意が弱い候補を一時的に拒否し、条件を満たす別の候補を先に確定させる。

- **2026-07 · [SCOPE: Boosting LLM Efficiency with Scoped Position Encoding](2026-c67f95485dce-scope-boosting-llm-efficiency-with-scoped-position-encoding.md)**  
  実装：[✓](https://github.com/oncemoe/ScoPE) ・ リポジトリ内被引用：0  
  注意ヘッドごとに指数的に広がる振り返り範囲を与える構造的疎性を位置符号化そのものとして使う方式で、算術的な位置信号なしに長さ外挿と検索精度をRoPEより高め、長文脈プリフィルを約2倍速くする。

- **2026-07 · [RSCE: Training-Free Residual Stream Encoding for Persistent Context Amortization](2026-1cd332146598-rsce-training-free-residual-stream-encoding-for-persistent-context-amort.md)**  
  実装：[✓](https://anonymous.4open.science/r/RSCE-2E4C/) ・ リポジトリ内被引用：0  
  文書を残差ストリームの平均ベクトル1本へ圧縮して質問時に注入し、プリフィルを定数時間化する学習不要の方式で、99パーセント削減でも品質の6から8割を保つが、ベクトル単独では記憶想起を抑える干渉も見つけた。

- **2026-07 · [Reflex: Real-Time VLA Control through Streaming Inference](2026-2607.14695-reflex-real-time-vla-control-through-streaming-inference.md)**  
  実装：[✓](https://github.com/9yc/Reflex) ・ リポジトリ内被引用：0  
  フローマッチング型行動モデルの文脈を3領域へ分ける分割注意で正しいキャッシュ再利用を可能にし、非同期実行と組み合わせて推論2.58倍高速化と反応遅延の最大54パーセント削減を達成する。

- **2026-07 · [OS-Pruner: Pruning Chains-of-Thought of Reasoning Models via Optimal Stopping](2026-2607.11089-os-pruner-pruning-chains-of-thought-of-reasoning-models-via-optimal-stop.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  思考連鎖の打ち切りを最適停止問題として定式化し、凍結した基礎モデルへ小さな停止方策を差し込むことで、数学推論で生成長を20〜60パーセント減らしながら精度をほぼ保ち、固定しきい値の分類型早期終了より良い精度と効率の交換を示した研究。

- **2026-07 · [Omni-Prune: Query-Aware Unified Token Pruning for Efficient Omnimodal Large Language Models](2026-2607.23445-omni-prune-query-aware-unified-token-pruning-for-efficient-omnimodal-lar.md)**  
  実装：[✓](https://github.com/kimberlyii/Omni-Prune) ・ リポジトリ内被引用：0  
  音声の顕著さで時間窓を切り、エンコーダ注意と質問への関連度で音声と映像を統一採点し、対応ペアを一緒に残して代表トークンで補う学習不要の枝刈りで、全トークン性能の99パーセント台を保ちながらプリフィルを最大3.25倍速くする。

- **2026-07 · [Multi-Mask Diffusion Language Models for Few-Step Generation](2026-2607.19686-multi-mask-diffusion-language-models-for-few-step-generation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  マスクを複数化し各トークンに指定マスクを持たせることで終端のエントロピー潰れを解消し、離散状態のまま少ステップ生成向けの整合性蒸留を可能にする拡散言語モデルの枠組み。

- **2026-07 · [Look and Think: Efficient Multimodal Reasoning via Modality-Decoupled Compression](2026-ba3a8b36c1eb-look-and-think-efficient-multimodal-reasoning-via-modality-decoupled-com.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  マルチモーダル推論を画像を見るステップと文章で考えるステップへ分け、考える間は視覚トークンを文脈から外し、終わったステップを圧縮することで、精度をほぼ保ったまま文脈長を6割前後削る微調整型の効率化。

- **2026-07 · [Lightweight Haar Wavelet Subband Pruning for LLMs](2026-30f6425d9933-lightweight-haar-wavelet-subband-pruning-for-llms.md)**  
  実装：[✓](https://github.com/dellixx/HWSP) ・ リポジトリ内被引用：0  
  重みをハール変換して四つの周波数帯域へ分け、各帯域を同じ割合で切る較正不要の枝刈りで、低周波への偏りを防ぎ、70Bモデルでも単一GPUで3分の枝刈りと強い方式に拮抗する品質を両立する。

- **2026-07 · [LaCo: Layer-wise Compensation for Pruned Large Language Models](2026-00140e8efcf4-laco-layer-wise-compensation-for-pruned-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LaCo（層-wise Compensation）は、枝刈りによって一部の重みや層内構造を削除したLLMの性能を、元モデルの各層の隠れ状態へ順次近づける局所回帰で回復する方法である。

- **2026-07 · [I/o for LLM inference: a survey of storage and memory bottlenecks](2026-5e022a2789e7-i-o-for-llm-inference-a-survey-of-storage-and-memory-bottlenecks.md)**  
  実装：[✓](https://github.com/rch0wdhury/llm-io-profiler) ・ リポジトリ内被引用：0  
  LLMデコードのデータ移動を重み・KVキャッシュ・活性の三I/O流へ分解し、量子化からSSD/CXL/統合メモリまでをルーフライン上で統一して、最適化を積むと支配ボトルネックが移動することを定量化したサーベイ。

- **2026-07 · [HPD-Parsing: Hierarchical Parallel Document Parsing](2026-2607.18839-hpd-parsing-hierarchical-parallel-document-parsing.md)**  
  実装：[✓](https://github.com/PaddlePaddle/PaddleOCR) ・ リポジトリ内被引用：0  
  文書のレイアウト協調とブロック内容の局所性を使い、主分岐が内容分岐を動的に起こして共有プリフィックスKVを再利用する階層並列デコードと分岐内の複数トークン予測で、自己回帰の土台比3.06倍のスループットと統合型最高の解析精度を両立する文書解析モデル。

- **2026-07 · [Gleam: Adaptive Network-Efficient CUDA API Remoting for Cross-Device GPU Sharing over LANs](2026-2607.23115-gleam-adaptive-network-efficient-cuda-api-remoting-for-cross-device-gpu-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  構内ネットワーク越しのCUDAリモーティングで、重みのハッシュキャッシュ、呼出しの非同期化、競合を予測する割当て、文脈保護を組み合わせ、リモーティング効率1.4から24.2倍とスループット最大1.79倍を達成する。

- **2026-07 · [FlowHN: Adaptive Token Routing for Efficient Parallel Hybrid Networks](2026-9723e70ce878-flowhn-adaptive-token-routing-for-efficient-parallel-hybrid-networks.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意分枝と状態空間モデル分枝を並列に置き、トークンをFLOP費用に比例して決定的に振り分けて層ごとに回転させることで、学習型ルーティングのばらつきなしに負荷を均し、32K文脈で比較対象の約3倍のスループットと最高水準のMFUを出すハイブリッドアーキテクチャ。

- **2026-07 · [FlashRT: Agent Harness for Guiding Agents to Deploy Real-Time Multimodal Applications](2026-2607.18171-flashrt-agent-harness-for-guiding-agents-to-deploy-real-time-multimodal-.md)**  
  実装：[✓](https://github.com/Infini-AI-Lab/FlashRT) ・ リポジトリ内被引用：0  
  単体モデルのカーネルを高速化するだけでは、どの段階をどのGPUへ配置し、いつ出力を小分けで次段へ渡し、どの段階の永続状態を共有できるかというアプリケーション全体の最適化は解けない。

- **2026-07 · [Every Time I Hire a Linguist, Inference Costs Go Down: On Linguistic Rules as Effective Prompt Compressors](2026-2607.25335-every-time-i-hire-a-linguist-inference-costs-go-down-on-linguistic-rules.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークン採点にLMの順伝播を使う代わりに、語彙・統語・意味・談話の言語規則だけの圧縮器を進化探索で自動発見し、配備時はCPU処理だけでプロンプトを圧縮して推論費用を下げる研究。

- **2026-07 · [Enabling Spatially Fine-Grained DVFS in Neural Processing Units for Energy-Efficient LLM Serving](2026-2607.16473-enpu-component-level-dvfs-npu-llm-serving.md)**  
  実装：[✓](https://github.com/google-coral/coralnpu（ベースコア）。eNPUの改変実装・シミュレータの公開URLは一次資料に記載なし。) ・ リポジトリ内被引用：0  
  eNPUは、演算器・SRAM・HBM・接続を別電圧周波数領域に分け、非同期転送と演算子別計画をSLO余裕で切替えて、NPUサービングの非ボトルネック電力を落とす。

- **2026-07 · [Dual-Flow Transformers: Decoupling the Primary Prefill Path from Additional Decode Computation](2026-2608.12385-dual-flow-transformers-decoupling-the-primary-prefill-path-from-addition.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  主フローだけがプロンプトとKVを担い補助フローは続きだけを厚くする二流化で、検証損失の漸近値を2.9416から2.9013へ下げ、専門家の段階別配分を可能にする。

- **2026-07 · [CXL-CCL: Inter-Node Collective GPU-Communication Using a CXL Shared Memory Pool](2026-fab14a584908-cxl-ccl-inter-node-collective-gpu-communication-using-a-cxl-shared-memory-pool.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CXL共有メモリをノード間GPU集団通信の媒体として使い、データ配置・細粒度重畳・ドアベル同期でRDMA型通信に対する性能とコストを改善する。

- **2026-07 · [CLARO: Controlled Attribute-Driven Reasoning Optimization for Efficient Chain-of-Thought](2026-682e6def443e-claro-controlled-attribute-driven-reasoning-optimization-for-efficient-c.md)**  
  実装：[✓](https://github.com/odedsc/CLARO) ・ リポジトリ内被引用：0  
  思考連鎖の長さではなく、読みやすさ・数式密度・統語圧縮・低冗長さという言語構造の属性を正解条件付きの報酬で強化学習し、トークン予算内での精度を最大で相対63.6%改善する効率的推論方式CLAROと、その即効版である属性誘導プロンプト。

- **2026-07 · [An Efficient vLLM-Based Inference Pipeline for Unified Audio Understanding and Generation](2026-2607.02119-an-efficient-vllm-based-inference-pipeline-for-unified-audio-understandi.md)**  
  実装：[✓](https://github.com/whr-a/vllm/tree/opuslm) ・ リポジトリ内被引用：0  
  複数コードブックの音声トークン生成を主従分解でvLLMの単一ストリーム経路へ載せ、CFGの条件・無条件リクエストを対で同時スケジュールして、音声理解と生成を統合した高スループット推論パイプラインを実現する研究。

- **2026-07 · [Adaptive Depth Sparse Framework: Similarity-Driven Resource Allocation for Pre-Trained LLMs](2026-2607.21291-adaptive-depth-sparse-framework-similarity-driven-resource-allocation-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層の入出力の類似度から「表現をよく変える層ほど多くのトークンを残す」層別保持率を決め、軽量ルーターと密モデルへのアライメント学習で、学習済みLLMを再学習なしに深さ疎化するAdaDSFの提案。

- **2026-07 · [3DLS: A 3D Logic-Stacked Architecture for Disaggregated LLM Serving](2026-2607.01617-3dls-disaggregated-serving-interconnect.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル→デコードのKV転送とデコード側テンソル並列AllReduceを同じ横方向リンクで競合させず、KVだけを3D縦リンクへ物理分離するチップレット構成。等帯域条件でも最大1.49倍のスループットと60.2%の遅延削減を示す。

- **2026-06 · [When Attention Collapses: Stage-Aware Visual Token Pruning from Structure to Semantics](2026-2606.03569-when-attention-collapses-stage-aware-visual-token-pruning-from-structure.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意スコア頼みの視覚トークン枝刈りが高スコア領域へ崩壊する問題を定量化し、投入前の反発型サンプリングで多様性を確保してから中間層で指示関連性により絞る二段階の学習不要な枝刈りで、トークンを約9割減らしても性能をほぼ保つ。

- **2026-06 · [Video-Rate Streaming Stylization on a Vision-Aware MLLM-Conditioned Edit Diffusion: Asymmetric Batched Inference on a Distilled UNet + MLLM Text Encoder](2026-2606.05981-video-rate-streaming-stylization-on-a-vision-aware-mllm-conditioned-edit.md)**  
  実装：[✓](https://github.com/otanl/dreamlite-stream) ・ リポジトリ内被引用：0  
  蒸留で軽くなった拡散デノイザではなく重いMLLMテキストエンコーダが律速になる反転したボトルネックに対し、CUDAストリーム分離とバッチ非対称性、コンパイル可能な時間アダプタ再定式化、条件の周期再利用で消費者GPU上に動画レートのストリーミング様式化を実現する推論システムの研究。

- **2026-06 · [Towards Fast and Effective Long Video Understanding of Multimodal Large Language Models via Adaptive Quasi-Gaussian Sampling](2026-2606.24187-towards-fast-and-effective-long-video-understanding-of-multimodal-large-.md)**  
  実装：[✓](https://github.com/Zkayovo-xmu/AdaQ) ・ リポジトリ内被引用：0  
  類似度の分散で準ガウス分布の3シグマ区間を質問ごとに広げたり狭めたりしてフレームを柔らかく抽出する学習不要の方式で、少ないフレームで長編動画理解の正解率を上げた。

- **2026-06 · [SMEPilot: Characterizing and Optimizing LLM Inference with Scalable Matrix Extensions](2026-2606.16332-smepilot-characterizing-and-optimizing-llm-inference-with-scalable-matrix-extensions.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CPU内のSMEと通常コアを共有帯域込みのルーフラインで使い分け、タイル分割・注意パイプライン・配置再利用によりLLM推論をllama.cpp比最大3.94倍高速化する。

- **2026-06 · [Query-based Cross-Modal Projector Bolstering Mamba Multimodal LLM](2026-2606.04719-query-based-cross-modal-projector-bolstering-mamba-multimodal-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚言語モデルでは画像符号器が大量のパッチ特徴を生成し、それを言語モデルの入力トークンとして与える。Transformer型言語モデルでは長い入力が自己注意の計算量を増やす。問い合わせ型射影器とMamba言語モデルを学習・微調整したモデル構造そのものを比較している。

- **2026-06 · [ProbMoE: Differentiable Probabilistic Routing for Mixture-of-Experts](2026-2606.01509-probmoe-differentiable-probabilistic-routing-for-mixture-of-experts.md)**  
  実装：[✓](https://github.com/HengHugoZhao/ProbMoE) ・ リポジトリ内被引用：0  
  ProbMoEはMoEのtop-kルーティングを専門家部分集合の確率分布として定式化し、学習時に確率的に選択した専門家を実行しつつ、集合制約下の厳密な周辺確率を直通勾配の代理に使う。OLMoEのGSMでは従来45.94%に対し50.19%、Qwen1.5-MoEの翻訳では30.00に対し39.23。

- **2026-06 · [Perplexity-Spectrum Calibration for Post-Training Pruning of Large Language Models](2026-14c95b8b5d41-perplexity-spectrum-calibration-for-post-training-pruning-of-large-langu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  学習後枝刈りのキャリブレーション標本を、対象モデルのパープレキシティで測った難易度の中央値中心の窓から選ぶ方式。3つの7Bモデルと2つの枝刈り手法で、無作為抽出よりパープレキシティ悪化を20から26パーセント減らし、結果のばらつきも3.4から6.1倍小さくする。

- **2026-06 · [Orchestra-o1: Omnimodal Agent Orchestration](2026-2606.13707-orchestra-o1-omnimodal-agent-orchestration.md)**  
  実装：[✓](https://github.com/zfkarl/Orchestra-o1) ・ リポジトリ内被引用：0  
  Orchestra-o1は、文字・画像・音声・動画が同時に含まれる複雑な質問を、主エージェント（MainAgent）が複数の部分課題へ分解し、専門の副エージェント（SubAgent）へ割り当てて実行する全モダリティ対応のエージェント統括（omnimodal agent orchestration）方式である。

- **2026-06 · [OrCA: An Efficient Computing Architecture for Fault-Tolerant Large Language Model Inference via Outlier-Aware Recalculation](2026-1f137626e007-orca-an-efficient-computing-architecture-for-fault-tolerant-large-langua.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  故障注入で見つけた、出力へ効くのは1から2パーセントの外れ値だけという性質を使い、外れ値の計算だけを冗長に再計算して守る階層型アクセラレータで、同等の面積のまま耐えられるビット誤り率を従来方式の約10倍へ上げる。

- **2026-06 · [Omni-Flow: A Unified Workflow Orchestration and Distributed KV Cache Sharing Framework for Multimodal Inference](2026-2606.31093-omni-flow-a-unified-workflow-orchestration-and-distributed-kv-cache-sharing-framework-for-multimodal-inference.md)**  
  実装：[✓](https://github.com/meituan-longcat/omni-flow) ・ リポジトリ内被引用：0  
  マルチモーダル推論を制御・データ・計算の3層へ分離し、Python DSL、GPU/CPU/SSD分散KV、SGLang互換実行を統合する。LongCat-NextやHunyuanImage-3を同じ配信抽象へ載せる基盤。

- **2026-06 · [Not All Errors Are Equal: Consequence-Aware Reasoning Compute Allocation](2026-2606.04402-not-all-errors-are-equal-consequence-aware-reasoning-compute-allocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  失敗の損害の大きさを課題文から予測して計算量を配る結果重大さ基準の配分で、難易度基準より費用重み付き損失を最大30.7パーセント減らし、難易度基準が無作為より悪い理由まで示す配分研究。

- **2026-06 · [MS-Resampler: Multi-Scope Visual Resampling for Efficient Multimodal LLMs](2026-2606.31383-ms-resampler-multi-scope-visual-resampling-for-efficient-multimodal-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MS-Resamplerは、異なる空間窓を優先する複数の再標本化分枝を並列に配置し、局所・中域・大域の特徴を固定長のトークンへ融合する。LLaVA-1.5-7Bの576視覚トークンを144へ減らす条件では、原著Table 1の相対平均は未圧縮比101.15%である。

- **2026-06 · [MorphoQuant: Modality-Aware Quantization for Omni-modal Large Language Models](2026-2606.04349-morphoquant-modality-aware-quantization-for-omni-modal-large-language-mo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MorphoQuantは、画像・動画・音声を同時に扱う大規模言語モデルの活性値を4ビットに圧縮するとき、モダリティごとに異なる分布の形状が原因で精度が低下する問題を扱う。

- **2026-06 · [Massive Spikes in LLMs are Bias Vectors: Mechanistic Uncovering and Spike-Free Quantization](2026-2606.02288-massive-spikes-in-llms-are-bias-vectors-mechanistic-uncovering-and-spike.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  巨大スパイクの担い手が正規化後に定数ベクトルへ収束し注意シンクを駆動するという機構解明に基づき、スパイクを抑えて事前計算テンプレートで機能を戻すことで、4ビット量子化でも先行最良方式と同等の精度を保ち、視覚モデルへも一般化した学習後量子化の研究。

- **2026-06 · [LatentSkill: From In-Context Textual Skills to In-Weight Latent Skills for LLM Agents](2026-2606.06087-latentskill-from-in-context-textual-skills-to-in-weight-latent-skills-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の文脈内スキル方式（In-context Skill）は、作業手順や道具の使用方法を自然言語でプロンプトへ挿入する。Qwen3-8Bを基盤としたALFWorldでは、文脈内スキル方式に対し既知課題の平均成功率が52.9%から74.3%、未知課題が56.0%から69.4%へ改善し、事前充填トークン数を約64%削減した。

- **2026-06 · [K-Forcing: Joint Next-K-Token Decoding via Push-Forward Language Modeling](2026-2606.10820-k-forcing-joint-next-k-token-decoding-via-push-forward-language-modeling.md)**  
  実装：[✓](https://github.com/alibaba-damo-academy/K-Forcing) ・ リポジトリ内被引用：0  
  推論エンジンのカーネルを高速化する研究ではなく、生成分布の表現とサンプリング方式を変える研究である。LM1BとOpenWebText（OWT）の約1億パラメータTransformerで、k=4の推論はAR比2.38〜3.47倍のスループットを報告した。

- **2026-06 · [HMPO: Hybrid Median-length Policy Optimization for Chain-of-Thought Compression](2026-2606.01934-hmpo-hybrid-median-length-policy-optimization-for-chain-of-thought-compr.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  思考連鎖の圧縮を単一ステージの強化学習で実現するため、正解生成の長さの中央値を適応予算とし、余弦減衰のトークン報酬と正解優先の乗算型報酬を組み合わせ、9Bから122Bで精度をほぼ保ち19から46パーセントのトークン圧縮を示した研究。

- **2026-06 · [From Awareness to Adherence: Bridging the Context Gap in Spoken Dialogue Systems via Context-Aware Decoding](2026-2606.16472-from-awareness-to-adherence-bridging-the-context-gap-in-spoken-dialogue-.md)**  
  実装：[✓](https://github.com/saga1214/AudioCAD) ・ リポジトリ内被引用：0  
  音声対話モデル内部の注意から鍵となる過去ラウンドを抽出し、その文脈がある場合とない場合の出力差を増幅するデコードで、履歴を忘れていないのに守れない失敗を、追加学習なしに改善する方式。

- **2026-06 · [Execution-State Capsules: Graph-Bound Execution-State Checkpoint and Restore for Low-Latency, Small-Batch, On-Device Physical-AI Serving](2026-2606.20537-execution-state-capsules-graph-bound-execution-state-checkpoint-and-restore-for-low-latency-small-batch-on-device-physic.md)**  
  実装：[✓](https://github.com/flashrt-project/FlashRT) ・ リポジトリ内被引用：0  
  KVだけでなく再帰・畳み込み・複数トークン予測状態を丸ごと保存復元し、単一ストリーム再入場の初回応答を最大26.94倍高速化する実行状態カプセル。

- **2026-06 · [Efficient and Trainable Language Model Test-Time Scaling via Local Branch Routing](2026-2606.25354-efficient-and-trainable-language-model-test-time-scaling-via-local-branc.md)**  
  実装：[✓](https://github.com/roger-yt/Local-Branch-Routing) ・ リポジトリ内被引用：0  
  各トークンの確定前に候補を小さな先読み木として実際に前方計算し、候補後の隠れ状態を振り分け器が比べて1枝だけ残す局所分岐方式で、数学推論のPass@1とPass@32を離散生成・通常の強化学習・軟トークン分岐の全てより高めた。

- **2026-06 · [Do Value Vectors in Deep Layers Need Context from the Residual Stream?](2026-2606.02780-do-value-vectors-in-deep-layers-need-context-from-the-residual-stream.md)**  
  実装：[✓](https://github.com/RiddleHe/nanochat) ・ リポジトリ内被引用：0  
  通常の自己注意（self-注意機構）は、各層の残差ストリームから問い合わせベクトル（Query）、鍵ベクトル（Key）、値ベクトル（Value）を計算する。結果として、深い層では元のトークン自体の情報から作った値だけを用いる方が、標準の文脈依存値より良い検証損失を示した。

- **2026-06 · [CRePE: Convolution-aware Relative Importance in Post-training Pruning with Efficient Search](2026-2606.01544-crepe-convolution-aware-relative-importance-in-post-training-pruning-wit.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  相対重要度へ二次元近傍の項と適応係数を加えた学習後枝刈り。係数探索はジニ係数の代理指標で約11時間から約20分へ短縮し、多モデルで従来スコアより低いパープレキシティを一貫して示した。

- **2026-06 · [ConCise: Training-Free Conclusion-Chain State Compression for Cost-Efficient Multi-Step RAG Services](2026-2606.28361-concise-training-free-conclusion-chain-state-compression-for-cost-effici.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  多段階RAGで生テキストの蓄積を構造化結論の追加専用チェーンへ置き換え、融合生成と合わせて累積トークンの伸びを二乗から線形へ落とし、平均64.63%のトークン削減を得る学習不要の状態管理方式。

- **2026-06 · [Communication-Efficient Verifiable Attention for LLM Inference](2026-2606.16352-communication-efficient-verifiable-attention-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  VeriAttn（通信-efficient TEE-GPU 注意機構）は、注意の線形演算と非線形の指数関数をともにGPUで計算させ、TEEには結果の検証と最終的な正規化を担当させる。Intel TDX、16仮想CPU、128 GBホストメモリ、NVIDIA H20 96 GBの環境で、4種類の3B～14Bモデルを評価した。

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

- **2026-05 · [VocalNet-M2: Advancing Low-Latency Spoken Language Modeling via Integrated Multi-Codebook Tokenization and Multi-Token Prediction](2026-2511.10232-vocalnet-m2-advancing-low-latency-spoken-language-modeling-via-integrate.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  8コードブックの音声トークンを直接生成してフローマッチングを外し、複数トークン予測で局所依存を学ばせることで、最初の音声チャンク遅延を725ミリ秒級から348.86ミリ秒へ約半減した音声言語モデル。ただし音声品質はデータの量と質に強く依存する。

- **2026-05 · [VLMaxxing through FrameMogging: Training-Free Anti-Recomputation for Video Vision-Language Models](2026-2605.03351-vlmaxxing-through-framemogging-training-free-anti-recomputation-for-vide.md)**  
  実装：[✓](https://github.com/jfbastien/VLMaxxing) ・ リポジトリ内被引用：0  
  本研究は「再利用で何を省くか」と「どの時間を分母にするか」を分け、異なる三つの機構を評価する。Qwen2.5-VL-7B-Instruct-4bitで、同一動画の後続質問を14.90〜35.92倍高速化し、VideoMMEの93対では選択肢・正誤の変化を観測しなかった。

- **2026-05 · [Visual-Redundancy-Controlled Parallel Decoding for Diffusion-Based Multimodal Large Language Models](2026-2605.25820-visual-redundancy-controlled-parallel-decoding-for-diffusion-based-multi.md)**  
  実装：[✓](https://github.com/infiniteYuanyl/VRCD) ・ リポジトリ内被引用：0  
  マスク付き拡散言語モデル（masked diffusion language モデル）は、未確定の多数のトークン位置を一度に予測し、確信の高い一部を確定する処理を繰り返して文章を生成する。主要な結果は推論高速化ではなく品質改善である。

- **2026-05 · [Triplet-Block Diffusion RWKV](2026-2605.25969-triplet-block-diffusion-rwkv.md)**  
  実装：[✓](https://github.com/leonardodalinky/B3D-RWKV) ・ リポジトリ内被引用：0  
  この論文は、片方向にしか情報が流れない再帰型言語モデルを、内部構造を変更せずに双方向の拡散型生成へ転換する方法を扱う。自己回帰型Transformerは生成位置を順番に確定するため、1回の復号で出せるトークン数が限られる。離散拡散型言語モデルは複数位置を並列に修正できるが、通常はブロック内の未マスク位置を左右両方向から参照する。

- **2026-05 · [Thinking as Compression: Your Reasoning Model is Secretly a Context Compressor](2026-2605.28713-thinking-as-compression-your-reasoning-model-is-secretly-a-context-compr.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の文脈圧縮は、入力文から重要そうなトークン・文書片を選ぶか、別のモデルで固定長の潜在表現へ符号化する。主要実験では、Qwen3-8Bの回答系で4倍圧縮制約下の平均F1が65.12、完全一致率（EM）が51.17、8倍ではF1 65.42・EM 51.79である。

- **2026-05 · [The Efficiency Frontier: A Unified Framework for Cost-Performance Optimization in LLM Context Management](2026-2605.23071-the-efficiency-frontier-a-unified-framework-for-cost-performance-optimiz.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全文投入、検索拡張、要約・圧縮などの文脈管理方式は、回答品質だけ、または入力トークン数だけを比較すると運用上の優劣が決めにくい。HotpotQAの5,000問をGPT-5.4 miniで評価した結果、再利用回数が1から100へ増えると、F1約0.78の運用点で有効トークン数が566から424へ約25%減る構成が選ばれた。

- **2026-05 · [Self-Orchestrating Language Models: Leveraging Semantic Dependence for Efficient Inference](2026-2609.14850-self-orchestrating-language-models-leveraging-semantic-dependence-for-ef.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  意味的に独立する文章断片や推論段階をモデルに印付けさせ、ランタイムが並列デコード、不要なKVページの解放、または拡散生成の並列順序に利用する三方式を示すMIT博士論文。各方式は別個に評価され、速度向上は課題・設定によって品質との交換条件がある。

- **2026-05 · [Selective Latent Thinking: Adaptive Compression of LLM Reasoning Chains](2026-2605.25745-selective-latent-thinking-adaptive-compression-of-llm-reasoning-chains.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかし、文章で説明する思考の全トークンを自己回帰的に生成すると、推論遅延とKVキャッシュ使用量が増える。複数の思考トークンを連続した潜在ベクトルへ置き換える方式は生成数を減らせるが、数値、式、厳密な条件分岐などの情報まで圧縮すると、正答に必要な離散的な値が失われやすい。

- **2026-05 · [Remember to Forget: Gated Adaptive Positional Encoding](2026-2605.10414-remember-to-forget-gated-adaptive-positional-encoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  回転幾何を変えず、クエリ側の収縮ゲートで不要な遠方文脈を指数的に弱め、キー側のランドマーク保護で必要な遠方トークンを残す位置符号化で、八倍の文脈外挿とヤーン併用時の一万六千トークン検索の大幅な改善を示した。

- **2026-05 · [Predict-then-Diffuse: Adaptive Response Length for Compute-Budgeted Inference in Diffusion LLMs](2026-2605.04215-predict-then-diffuse-adaptive-response-length-for-compute-budgeted-infer.md)**  
  実装：[✓](https://github.com/mchl-labs/predict-then-diffuse) ・ リポジトリ内被引用：0  
  拡散型言語モデルの固定応答長を、推論前に軽量予測器で入力ごとに見積もって安全余裕を加えることで置き換え、埋め草計算を省いて既定推論比で計算量を99.34パーセント減らす枠組み。

- **2026-05 · [Positional LSH: Binary Block Matrix Approximation for Attention with Linear Biases](2026-2605.09472-positional-lsh-binary-block-matrix-approximation-for-attention-with-line.md)**  
  実装：[✓](https://github.com/DanielWolfsonTAU/positional_lsh) ・ リポジトリ内被引用：0  
  ALiBiのバイアス行列を、位置をハッシュするランダムビニングによる二値ブロックマスクの期待値として表し、保証付き近似とほぼ線形時間の長文脈注意への帰着を与える理論研究。

- **2026-05 · [PEEK: Context Map as an Orientation Cache for Long-Context LLM Agents](2026-2605.19932-peek-context-map-as-an-orientation-cache-for-long-context-llm-agents.md)**  
  実装：[✓](https://github.com/zhuohangu/peek) ・ リポジトリ内被引用：0  
  コンテキスト地図はエージェントのシステムプロンプトへ付与され、予算 B トークン以内に維持される。

- **2026-05 · [OmniMem: Perturbation-aware Memory Compression for Streaming Audio-Visual LLMs](2026-2606.07577-omnimem-perturbation-aware-memory-compression-for-streaming-audio-visual.md)**  
  実装：[✓](https://github.com/bytedance/SALMONN/tree/omni_mem) ・ リポジトリ内被引用：0  
  映像と音声のKVキャッシュを分けて層別・モダリティ別に予算を配り、注意重要度と冗長性を掛けたスコアで残すペアを選ぶことで、同一8K予算で長尺動画理解の正解率を比較対象より2から4ポイント高める圧縮方式。

- **2026-05 · [Nice Fold or Hero Call: Learning Budget-Efficient Thinking for Adaptive Reasoning](2026-2605.11625-nice-fold-or-hero-call-learning-budget-efficient-thinking-for-adaptive-r.md)**  
  実装：[✓](https://github.com/houqiii/BET) ・ リポジトリ内被引用：0  
  推論特化モデルは複雑な問題で長い思考系列を生成するが、長い思考が常に正答率を改善するわけではない。従来の一律な思考圧縮や問題難易度に応じた予算制御は、後者を十分に見分けられず、逆に「難しいが解ける」問題まで早期に切り上げてしまうことがある。

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

- **2026-05 · [LocateAnything: Fast and High-Quality Vision-Language Grounding with Parallel Box Decoding](2026-2605.27365-locateanything-fast-and-high-quality-vision-language-grounding-with-para.md)**  
  実装：[✓](https://github.com/NVlabs/Eagle/tree/main/Embodied) ・ リポジトリ内被引用：0  
  各矩形を、四つの量子化座標と構造トークンからなる長さ6のブロックで表し、ブロック内部は同時に予測する。

- **2026-05 · [Locality Matters for Training-Free Audio Token Compression in Audio-Language Models](2026-2605.25179-locality-matters-for-training-free-audio-token-compression-in-audio-lang.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  音声トークンを時間的に近い相手とだけ統合する学習不要の圧縮LTBMを、全域マッチングとの統制比較で検証し、局所性はキャプション生成では強い圧縮下で効くが選択式理解では全域集約が有利という、タスク依存の設計指針を示した研究。

- **2026-05 · [LLMForge: Multi-Backend Hardware-Aware Neural Architecture Search with Infinite-Head Attention for Edge Language Models](2026-2605.17653-llmforge-multi-backend-hardware-aware-neural-architecture-search-with-in.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ヘッド数と次元を層ごとに独立化した注意で探索空間を約400倍に広げ、代理モデルと複数費用モデルで基板ごとに異なる最適形を求める端末向け構造探索で、300M級で検証損失2.798とエネルギー40パーセント減を両立する方式。

- **2026-05 · [LLaVA-UHD v4: What Makes Efficient Visual Encoding in MLLMs?](2026-2605.08985-llava-uhd-v4-what-makes-efficient-visual-encoding-in-mllms.md)**  
  実装：[✓](https://github.com/THUMAI-Lab/LLaVA-UHD-v4) ・ リポジトリ内被引用：0  
  切り分け符号化が全体符号化を上回ることを示し、視覚符号器の浅い層に窓注意と重み再利用で初期化した圧縮部を入れて内部から四倍圧縮することで、視覚符号化の演算量を五五・七五パーセント減らしながら十六倍圧縮でも精度をほぼ保った。

- **2026-05 · [Layer-wise Token Compression for Efficient Document Reranking](2026-2605.20683-layer-wise-token-compression-for-efficient-document-reranking.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検索システムの再順位付け（reranking）では、初段のBM25や密ベクトル検索が返した文書候補を、より高価なTransformerで再評価する。Qwen3-0.6BのDL19段落再順位付けでは、28層中第8層から40%のトークンを残す設定でnDCG@10が無圧縮の約0.727と同水準のまま、QPSは5.35→6.69（25%増）となる。

- **2026-05 · [Layer Collapse in Diffusion Language Models](2026-2605.06366-layer-collapse-in-diffusion-language-models.md)**  
  実装：[✓](https://github.com/Conzel/super-outlier-dlm) ・ リポジトリ内被引用：0  
  本論文は、離散拡散型言語モデル（Diffusion Language モデル、DLM）と自己回帰型言語モデル（Autoregressive Language モデル、ARモデル）で、隠れ状態の層間類似性と圧縮耐性がどのように異なるかを調べた実証研究である。

- **2026-05 · [LatentRouter: Can We Choose the Right Multimodal Large Language Model Before Seeing Its Answer?](2026-2605.11301-latentrouter-can-we-choose-the-right-multimodal-large-language-model-bef.md)**  
  実装：[✓](https://github.com/LabRAI/LatentRouter) ・ リポジトリ内被引用：0  
  画像と質問から作るルーティングカプセルと、候補モデルの能力トークンを潜在空間で照合して各モデルの反実仮想的な品質を予測するルータで、MMR-BenchとVL-RouterBenchの性能志向と費用条件の全4条件で最良の非オラクル結果を出す。

- **2026-05 · [Latent Bridge: Feature Delta Prediction for Efficient Dual-System Vision-Language-Action Model Inference](2026-2605.02739-latent-bridge-feature-delta-prediction-for-efficient-dual-system-vision-.md)**  
  実装：[✓](https://github.com/1999Lyd/Latent-Bridge) ・ リポジトリ内被引用：0  
  視覚言語バックボーンの出力の変化量を小さな橋で予測して呼び出しを50から75パーセント省き、二系統型の行動モデルで成功率をほぼ保ったまま1.65から1.73倍へ高速化する。

- **2026-05 · [Latent Action Reparameterization for Efficient Agent Inference](2026-2605.18597-latent-action-reparameterization-for-efficient-agent-inference.md)**  
  実装：[✓](https://github.com/EZ-hwh/LAR) ・ リポジトリ内被引用：0  
  エージェントの軌跡から遷移等価な複数ステップ行動を潜在行動として学習し語彙化することで、行動トークンを最大で約27パーセント減らしながらタスク性能を維持または改善する、行動表現そのものの再設計。

- **2026-05 · [InfoQuant: Shaping Activation Distributions for Low-Bit LLM Quantization](2026-2605.26175-infoquant-shaping-activation-distributions-for-low-bit-llm-quantization.md)**  
  実装：[✓](https://github.com/LLIKKE/InfoQuant) ・ リポジトリ内被引用：0  
  InfoQuantは、LLMの低ビット事後量子化（post-学習 量子化; PTQ）における活性値の量子化誤差を、単純な外れ値除去ではなく、量子化器に入力する分布の形から最適化する方式である。

- **2026-05 · [HybridServe: Stall-Free Distributed Disaggregated LLM Inference with Hybrid KVCache Buffering](2026-1e016ba4edaa-hybridserve-stall-free-distributed-disaggregated-llm-inference-with-hybr.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来のPush方式は、事前入力が終わるとキャッシュを復号側へすぐ送るため、後の復号時にノード間転送を待ちにくい。2台のV100を用いた実機では、前段停止が大きい条件で最初のトークンまでの時間が最大1.76倍高速化し、処理量は最大1.57倍改善した。

- **2026-05 · [Hierarchical Mixture-of-Experts with Two-Stage Optimization](2026-2605.08292-hierarchical-mixture-of-experts-with-two-stage-optimization.md)**  
  実装：[✓](https://github.com/brain-lab-research/Hi-MoE) ・ リポジトリ内被引用：0  
  混合専門家モデル（Mixture-of-Experts、MoE）は、多数の専門家ネットワークを用意し、各トークンで少数だけ実行することで総パラメータ数と実行計算量を分離する。パープレキシティ（perplexity、PPL）は11検証領域の10領域で改善するが、下流課題の一部では悪化し、実測の生成トークン毎秒が40%改善したという意味ではない。

- **2026-05 · [GQLA: Group-Query Latent Attention for Hardware-Adaptive Large Language Model Decoding](2026-2605.15250-gqla-group-query-latent-attention-for-hardware-adaptive-large-language-m.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  多頭潜在注意（Multi-head Latent 注意機構; MLA）は鍵と値を共通の低ランク潜在ベクトルへまとめ、過去文脈から読み出すバイト数を大きく削減する。論文の中心的な「H20で3.4倍」は、文脈長8192・BF16・公開ピーク性能を入力した屋根線モデルによる注意部分の理論的処理量であり、実GPUで測ったモデル全体のトークン生成速度ではない。

- **2026-05 · [Focus on the Core: Empowering Diffusion Large Language Models by Self-Contrast](2026-2605.01373-focus-on-the-core-empowering-diffusion-large-language-models-by-self-con.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルのデコードを核トークンへ集中させる学習不要の手法。分布のステップ間変動から高情報密度トークンを自動検出し、再マスクした負例との自己コントラストで品質を上げ、収束検知による並列デコードでステップ数と遅延も削減する。

- **2026-05 · [Fixed-Point Masked Generative Modeling](2026-2605.31215-fixed-point-masked-generative-modeling.md)**  
  実装：[✓](https://github.com/andreamiele/fp-mgm/) ・ リポジトリ内被引用：0  
  デノイザー中央を重み共有の不動点ブロックへ置き換えて実効深さを可変にし、跨ステップ一貫性と三状態再利用を組み合わせ、パラメータと学習費用を減らしながら低予算生成の品質を上げるマスク生成方式。

- **2026-05 · [Exploiting Multicast for Accelerating Collective Communication](2026-2605.22428-exploiting-multicast-for-accelerating-collective-communication.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  宛先をパケットへ埋め込み中継ノードで複製する書き込み意味論MultiWriteで多対多集合通信の重複送信をなくし、Ascend NPUでAllGatherとAlltoAllの遅延を最大33パーセント減らす方式。

- **2026-05 · [Enhancing Visual Token Representations for Video Large Language Models via Training-Free Spatial-Temporal Pooling and Gridding](2026-2605.22078-enhancing-visual-token-representations-for-video-large-language-models-v.md)**  
  実装：[✓](https://github.com/bingjunluo/ST-GridPool) ・ リポジトリ内被引用：0  
  階層的な時間区間のフレームを格子状に組み合わせ、区間末尾へ多時間尺度の要約を埋め込むPyramid Temporal Gridding（PTG）と、視覚特徴のL2ノルムを重みに使うNorm-based Spatial Pooling（NSP）を統合する。

- **2026-05 · [ECM: Enhancing Compressibility of Quantized Vision Encoder and LLM for Large Vision-Language Models](2026-97023514dc43-ecm-enhancing-compressibility-of-quantized-vision-encoder-and-llm-for-la.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚エンコーダと言語モデルの両方を対象に、チャネル重要度で量子化粒度を変える適応粒度量子化と、視覚側のゼロ点除去と重みスケーリングで圧縮しやすさを高め、量子化済み重みへ可逆圧縮を重ねてメモリをFP16比で平均80.3パーセント減らす枠組み。

- **2026-05 · [DeferMem: Query-Time Evidence Distillation via Reinforcement Learning for Long-Term Agent Memory](2026-2605.22411-defermem-query-time-evidence-distillation-via-reinforcement-learning-for.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の記憶システムは、将来の質問が分からない時点で対話を要約・圧縮し、検索しやすい記憶単位を作る。原著v2の評価ではLongMemEval-Sの正答率が70.00%、LoCoMoで学習に使った唯一の会話conv-26を除いた正答率が89.93%だった。

- **2026-05 · [DC-Leap: Training-Free Acceleration of dLLMs via Draft-Guided Contiguous Leaping Decoding](2026-2607.20467-dc-leap-training-free-acceleration-of-dllms-via-draft-guided-contiguous-.md)**  
  実装：[✓](https://github.com/ffh-wyls/DC-Leap) ・ リポジトリ内被引用：0  
  拡散言語モデルの並列確定を左から連続した範囲だけに制限して依存誤差を抑え、窓外の高信頼予測を下書きとして右側文脈に使うことで、確定閾値を下げて長系列MBPPで53.19倍まで高速化する学習不要のデコード法。

- **2026-05 · [Compute Where it Counts: Self Optimizing Language Models](2026-2605.10875-compute-where-it-counts-self-optimizing-language-models.md)**  
  実装：[✓](https://github.com/akhauriyash/SOL) ・ リポジトリ内被引用：0  
  Self-Optimizing Language Models（SOL）は、LLM推論の各トークンに同じ圧縮率・計算予算を与えるのではなく、トークンごとに計算の必要度が異なるという性質を利用して、どこで計算を節約し、どこで品質を守るかを小型制御器に学習させる方式である。

- **2026-05 · [BitLM: Unlocking Multi-Token Language Generation with Bitwise Continuous Diffusion](2026-2605.11577-bitlm-unlocking-multi-token-language-generation-with-bitwise-continuous-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークンを18ビットの二進コードで表し、ブロック内は拡散ヘッドで複数トークンを共同にノイズ除去し、ブロック間は因果的注意を保つことで、語彙ソフトマックスを介さない複数トークン生成を実現する言語モデル。

- **2026-05 · [Bandwidth-Aware LLM Inference on Heterogeneous Many-Core Supercomputers](2026-2605.25655-bandwidth-aware-llm-inference-on-heterogeneous-many-core-supercomputers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低帯域・分散オンチップ記憶のMT-3000向けに演算子、融合注意、三段パイプライン、混合並列を共同設計し、大規模LLM推論を実現。

- **2026-05 · [Adaptive Inverted-Index Routing for Granular Mixtures-of-Experts](2026-2605.04952-adaptive-inverted-index-routing-for-granular-mixtures-of-experts.md)**  
  実装：[✓](https://anonymous.4open.science/r/adaptive_inverted_index_routing_code-D6FE/) ・ リポジトリ内被引用：0  
  本研究が解くのは、非常に多数の小さな専門家を使う混合専門家モデル（Mixture-of-Experts、MoE）で、専門家を選ぶルータ自身が高価になるという問題である。具体的には、入力トークンを最も近い符号語へ割り当て、その符号語に結び付いた専門家番号の候補表を取得する。著者は最大約10%の相対困惑度改善をPEERとの比較で報告する。

- **2026-04 · [VisPCO: Visual Token Pruning Configuration Optimization via Budget-Aware Pareto-Frontier Learning for Vision-Language Models](2026-2604.15188-vispco-visual-token-pruning-configuration-optimization-via-budget-aware-.md)**  
  実装：[✓](https://github.com/JHW5981/VisPCO) ・ リポジトリ内被引用：0  
  視覚トークン枝刈りの層ごとの比率設定を予算つきのパレート最適化として勾配で自動探索する枠組みで、予算半分の条件で無作為設定の平均から平均成績を約八ポイント回復し、経験的な最適曲線へほぼ一致する設定を約一時間で得たと報告した。

- **2026-04 · [TRIMS: Trajectory-Ranked Instruction Masked Supervision for Diffusion Language Models](2026-2604.00666-trims-trajectory-ranked-instruction-masked-supervision-for-diffusion-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TRIMS（Trajectory-Ranked Instruction Masked Supervision）は、マスク拡散言語モデル（Masked Diffusion Language モデル; MDLM）の反復生成で、どのトークンを先に確定するかを学習中から誘導する方式である。

- **2026-04 · [Towards Faster Language Model Inference Using Mixture-of-Experts Flow Matching](2026-2604.15009-towards-faster-language-model-inference-using-mixture-of-experts-flow-ma.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、通常の自己回帰（autoregressive; AR）生成が1トークンごとに逐次的な前向き計算を必要とする問題に対し、連続潜在空間上の流れ合わせ（flow matching）と混合専門家（mixture of エキスパート; MoE）を組み合わせる非自己回帰（non-autoregressive; NAR）モデルYANを提案する。

- **2026-04 · [Thinking Without Words: Efficient Latent Reasoning with Abstract Chain-of-Thought](2026-2604.22709-thinking-without-words-efficient-latent-reasoning-with-abstract-chain-of.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  自然言語CoTは数学や多段階推論の正答率を改善するが、途中の推論を文章として一語ずつ生成するため、長い回答までの待ち時間と生成トークン費用を増やす。推論内容を短縮する手法には、文章を途中で打ち切る方式、自然言語のCoTを段階的に内在化する方式、連続ベクトルの潜在思考を繰り返す方式などがある。

- **2026-04 · [The Recurrent Transformer: Greater Effective Depth and Efficient Decoding](2026-2604.21215-the-recurrent-transformer-greater-effective-depth-and-efficient-decoding.md)**  
  実装：[✓](https://github.com/geniucos/recurrent-transformer) ・ リポジトリ内被引用：0  
  通常の自己回帰Transformerでは、ある層のトークン位置$i$に対する鍵・値は、その層に入力された表現から計算される。重要なのは、固定サイズの再帰状態へ過去を押し込む方式ではないことだ。

- **2026-04 · [Technology solutions targeting the performance of gen-AI inference in resource constrained platforms](2026-2604.11128-technology-solutions-targeting-the-performance-of-gen-ai-inference-in-re.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末推論のメモリ圧迫に対し、高帯域ストレージと接合型SRAMチップレットを階層ルーフラインの解析モデルで評価し、帯域・遅延の要求条件とデータ配置の指針を示すハードウェア技術の分析。

- **2026-04 · [Stochastic Attention: Connectome-Inspired Randomized Routing for Expressive Linear-Time Attention](2026-2604.00754-stochastic-attention-connectome-inspired-randomized-routing-for-expressi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  窓注意の前後でトークン順序をランダムに入れ替えるだけのパラメータなし改良。固定窓が確率的な大域窓に変わり、同じ計算量で受容野が指数的に広がる。SWAとのゲート併用で局所性も保ち、学習なし適用でも全注意の品質へ近づく。

- **2026-04 · [SLaB: Sparse-Lowrank-Binary Decomposition for Efficient Large Language Models](2026-2604.04493-slab-sparse-lowrank-binary-decomposition-for-efficient-large-language-mo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みを疎行列とランク1低ランク掛ける二値行列の補償へ分解する、再学習不要のワンショット圧縮手法。高圧縮率でも枝刈りの品質低下を大きく抑える。

- **2026-04 · [Revisiting Auxiliary Losses for Conditional Depth Routing: An Empirical Study](2026-2604.17228-revisiting-auxiliary-losses-for-conditional-depth-routing-an-empirical-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  条件付き深さルーティングのゲート学習で、予測型の補助とオラクル型のスコア監督の相互作用を統制比較し、後続層がすべてfullという前提で作る教師ラベルは実行方策とずれて純粋に有害であり、外すと両ゲートとも改善してゲート間の差も消えることを示した実証研究。

- **2026-04 · [Residual-Mass Accounting for Partial-KV Decoding](2026-2604.05438-residual-mass-accounting-for-partial-kv-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  入力文脈が長いほど読み出すKVが増え、メモリ帯域が律速になりやすい。そこで一部の過去トークンだけを取得して正確な注意を計算する部分KV方式がある。Llama-3.2-3B-InstructのRULER、64k文脈、全体の1%を正確参照する設定では、選択のみのTop-Kの0.688に対し提案法は0.711、全注意は0.721だった。

- **2026-04 · [QuantClaw: Precision Where It Matters for OpenClaw](2026-2604.22577-quantclaw-precision-where-it-matters-for-openclaw.md)**  
  実装：[✓](https://github.com/SparkEngineAI/QuantClaw-plugin) ・ リポジトリ内被引用：0  
  エージェント課題ごとの量子化感度を実測して精度の経路表を作り、軽い課題は低精度、重い課題は高精度へ自動で振り分けることで、得点を保ちながら費用と遅延を2割前後削った精度経路プラグイン。

- **2026-04 · [PrunePrivyTune: Accelerating Language Models with Pruning and Differentially Private Fine-Tuning](2026-7c3882fcb8c1-pruneprivytune-accelerating-language-models-with-pruning-and-differentia.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全層ペアの隠れ状態コサイン類似度で冗長層を枝刈りし、DP-SGDとLoRAでプライバシーを保ちながら回復させる圧縮枠組みで、BERT-baseとGLUE 4タスクにおいてε=1でもSST-2精度92.31パーセントと未圧縮モデルに並び、抽出攻撃への耐性も合成データで検証した研究。

- **2026-04 · [POINTS-Long: Adaptive Dual-Mode Visual Reasoning in MLLMs](2026-2604.11627-points-long-adaptive-dual-mode-visual-reasoning-in-mllms.md)**  
  実装：[✓](https://anakin-skywalker-joseph.github.io/POINTS-Long-Webpage) ・ リポジトリ内被引用：0  
  WangらはPOINTS-Longを提案し、高精細な視覚情報を使うFocusモードと、圧縮された視覚情報だけを使うStandbyモードを同じモデルに持たせる。64フレームの動画では、Standbyが1フレーム8〜32トークン、合計512〜2,048トークンだけを使い、原著Table 1の相対平均97.7〜99.7%を維持する。

- **2026-04 · [Mixture of Heterogeneous Grouped Experts for Language Modeling](2026-2604.23108-mixture-of-heterogeneous-grouped-experts-for-language-modeling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大きさの異なる専門家グループと二段階ルーティングでトークンの難しさに計算量を合わせ、補助損失とGPU配置の工夫で負荷均衡を保ちながら、均一MoEより総パラメータ約20パーセント減で同等以上の性能を得るMoEアーキテクチャ。

- **2026-04 · [MIPT-SSM: Scaling Language Models with O(1) Inference Cache via Phase Transitions](2026-2604.07716-mipt-ssm-scaling-language-models-with-o-1-inference-cache-via-phase-tran.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  学習される測定率で波の相と粒子の相を切り替える状態空間モデルにより、系列長8192でTransformerの34,651MBに対し810MBのメモリで済み、AG Newsの精度は0.905でTransformerの0.736を上回った。

- **2026-04 · [MCAP: Deployment-Time Layer Profiling for Memory-Constrained LLM Inference](2026-2604.21026-mcap-deployment-time-layer-profiling-for-memory-constrained-llm-inferenc.md)**  
  実装：[✓](https://github.com/genovationtech/nve) ・ リポジトリ内被引用：0  
  MCAP（Monte Carlo Activation Profiling）は、モデルを読み込む段階で少数の入力を使って層ごとの重要度を計測し、推論時の演算精度と重みの常駐先を同時に決める方式である。論文の代表例ではプロファイルは338バイトのJSONであり、初回計測は約60秒、同一アーキテクチャの再利用時は追加計測を省ける。

- **2026-04 · [MARS: Enabling Autoregressive Models Multi-Token Generation](2026-2604.07023-mars-enabling-autoregressive-models-multi-token-generation.md)**  
  実装：[✓](https://github.com/Xalp/MARS) ・ リポジトリ内被引用：0  
  MARS（Mask AutoRegreSsion）は、通常は1回の前向き計算で1トークンを生成する自己回帰（autoregressive; AR）言語モデルに、必要なときだけ複数トークンをまとめて出力する能力を追加する方式である。

- **2026-04 · [Local-Splitter: A Measurement Study of Seven Tactics for Reducing Cloud LLM Token Usage on Coding-Agent Workloads](2026-2604.12301-local-splitter-a-measurement-study-of-seven-tactics-for-reducing-cloud-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  小型ローカルモデルを前段に置く7戦術を同一条件で測り、ローカル振り分けとプロンプト圧縮の組が編集・説明中心の作業でクラウドトークンを45から79パーセント減らす一方、最適な組は作業種別で変わることを示した測定研究。

- **2026-04 · [LLaDA2.0-Uni: Unifying Multimodal Understanding and Generation with Diffusion Large Language Model](2026-2604.20796-llada2-0-uni-unifying-multimodal-understanding-and-generation-with-diffu.md)**  
  実装：[✓](https://github.com/inclusionAI/LLaDA2.0-Uni) ・ リポジトリ内被引用：0  
  画像理解と画像生成を一つの基盤モデルで扱うには、画像を言語モデルへどう渡すかが大きな設計課題になる。SPRINTの最大1.6倍とデコーダの段数削減は異なる処理段階の話であり、単純に掛け算してエンドツーエンドの高速化率とみなしてはならない。

- **2026-04 · [Layer-wise heterogeneity-guided heterogeneous pruning: An LLM compression method](2026-2b611e85a822-layer-wise-heterogeneity-guided-heterogeneous-pruning-an-llm-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層ごとのフィッシャー重要度で感度を測り、層・チャネル・重みという三つの枝刈り粒度とスパース率を層ごとに割り当て、サロゲート関数で探索を高速化することで、精度と推論速度の調整可能な両立を狙う異種混合の枝刈り方式。

- **2026-04 · [Integrated Electro-Optic Attention Nonlinearities for Transformers](2026-2604.09512-integrated-electro-optic-attention-nonlinearities-for-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この論文は、非線形関数をデジタル回路で近似する代わりに、光の干渉に伴う電圧と透過光強度の非線形関係を演算として利用する方式を提案する。

- **2026-04 · [Folding Tensor and Sequence Parallelism for Memory-Efficient Transformers](2026-2604.26294-folding-tensor-and-sequence-parallelism-for-memory-efficient-transformer.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  テンソル並列と系列並列を一つの装置軸へ折り畳み、各装置が重みと系列の両方を分割保持することで、長文脈ほど効くメモリ削減とスループット改善を得る並列化方式。

- **2026-04 · [Expert Upcycling: Shifting the Compute-Efficient Frontier of Mixture-of-Experts](2026-2604.19835-expert-upcycling-shifting-the-compute-efficient-frontier-of-mixture-of-e.md)**  
  実装：[✓](https://github.com/amazon-science/expert-upcycling) ・ リポジトリ内被引用：0  
  混合専門家モデル（Mixture-of-Experts; MoE）は、各トークンが多数の専門家のうち一部だけを実行することで、総パラメータ数とトークン当たり演算量を切り離す。32専門家を64専門家へ増やした場合、50%の継続事前学習予算で13Bを最初から訓練する方式よりGPU時間を約32%節約し、検証損失を1.308から1.305へ下げた。

- **2026-04 · [Evolving LLMs from Next-Token Prediction to Multi-Token Prediction via Self-Distillation](2026-077aa1e5b2da-evolving-llms-from-next-token-prediction-to-multi-token-prediction-via-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  対象モデルを凍結し、その出力分布を1トークンずらして教師にする自己蒸留で軽量なマルチトークン予測モジュールを後付け学習する方式。Qwen3-8Bで受理長が従来のラベル学習の2.35から2.52へ上がり、学習量は対象モデルの事前学習の450分の1で済む。

- **2026-04 · [Efficient Test-Time Inference via Deterministic Exploration of Truncated Decoding Trees](2026-2604.20500-efficient-test-time-inference-via-deterministic-exploration-of-truncated.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  打ち切り標本のデコード木を復元標本せず相異なる葉として決定的に列挙し、共有プリフィックスの再利用と早期停止で、自己整合性より少ない新規トークンで高い多数決正解率とコード通過率を得るテスト時推論法。

- **2026-04 · [DiffuMask: Diffusion Language Model for Token-level Prompt Pruning](2026-2604.06627-diffumask-diffusion-language-model-for-token-level-prompt-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  階層的枝刈りで作った教師データを拡散言語モデルへ学習させ、トークン保持マスクを並列に予測することで、逐次枝刈りに10時間以上かかるプロンプト圧縮を約1分で終え、プロンプト長を最大80パーセント削減しながら精度を維持・改善したプロンプト圧縮の研究。

- **2026-04 · [Attention Editing: A Versatile Framework for Cross-Architecture Attention Conversion](2026-2604.05688-attention-editing-a-versatile-framework-for-cross-architecture-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（Large Language モデル; LLM）の長文脈推論では、過去トークンの鍵・値（Key-Value; KV）を保存するメモリと、その読出し帯域が制約となる。グループ化問い合わせ注意（Grouped Query 注意機構; GQA）はKVヘッドの共有によって容量を抑えるが、長い系列や多数の同時要求ではKVが増え続ける。

- **2026-04 · [AgentOpt v0.1 Technical Report: Client-Side Optimization for LLM-Based Agent](2026-2604.06296-agentopt-v0-1-technical-report-client-side-optimization-for-llm-based-ag.md)**  
  実装：[✓](https://agentoptimizer.github.io/agentopt/) ・ リポジトリ内被引用：0  
  AgentOptは、複数のLLM呼び出しから成るエージェントのモデル選択を、開発者側の品質・遅延・API費用の制約に従って最適化する基盤である。9種類のモデルを2役割へ割り当てれば81通りになる。

- **2026-04 · [Adaptive Head Budgeting for Efficient Multi-Head Attention](2026-2604.22583-adaptive-head-budgeting-for-efficient-multi-head-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  入力ごとに使う注意ヘッドの数と顔ぶれを学習して選び、分類課題で計算量を減らしながら正解率を維持または改善する、予算適応型の多ヘッド注意。

- **2026-04 · [Absorber LLM: Harnessing Causal Synchronization for Test-Time Training](2026-2604.20915-absorber-llm-harnessing-causal-synchronization-for-test-time-training.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈の大規模言語モデルでは、生成済み履歴を鍵値キャッシュ（KV キャッシュ）へ蓄積すると、復号のたびに参照する過去位置が増える。この方式は推論時学習（test-time 学習）と長文脈推論の接点にある。

- **2026-03 · [Why Smaller Is Slower? Dimensional Misalignment in Compressed LLMs](2026-2604.09595-why-smaller-is-slower-dimensional-misalignment-in-compressed-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  圧縮で生じる不規則な次元が実行基盤の整列条件を外してモデルを遅くする現象を三層で切り分け、同じ予算のまま全次元を整列した候補から動的計画法で選び直す後付けの枠組みで、前処理の遅延を最大約一・五倍の高速化まで回復したと報告した。

- **2026-03 · [Weight Clustering Reveals the Importance of Relative Rank in Large Language Models](2026-2603.17917-weight-clustering-reveals-the-importance-of-relative-rank-in-large-langu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み行列を16から64個の共有値へ置き換えるクラスタ化を分析道具にし、割当を固定して共有値だけを動かす摂動実験で、圧縮で守るべきは正確な値ではなく重みの相対順位と分散であることを4モデルで分離し、再学習なしの2から4倍の保存圧縮と併せて示した重み構造の分析研究。

- **2026-03 · [The 1/W Law: An Analytical Study of Context-Length Routing Topology and GPU Generation Gains for LLM Inference Energy Efficiency](2026-2603.17280-the-1-w-law-an-analytical-study-of-context-length-routing-topology-and-g.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文脈窓が2倍になるとワットあたりトークンが半分になる1/W則を解析的に導き、文脈長ルーティングがGPU世代交代より大きな省エネ手段であり、両者の利得が乗算で重なることを示す分析研究。

- **2026-03 · [SecDTD: Dynamic Token Drop for Secure Transformers Inference](2026-2603.13670-secdtd-dynamic-token-drop-for-secure-transformers-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  安全なTransformer推論向けに、ソフトマックス前スコア付けMCNと秘匿中央値選択OMSelでトークンドロップを前倒しし、暗号文で最も高いソフトマックスまで削って最大4.47倍の高速化を精度維持で示す。

- **2026-03 · [ReLope: KL-Regularized LoRA Probes for Multimodal LLM Routing](2026-2603.24787-relope-kl-regularized-lora-probes-for-multimodal-llm-routing.md)**  
  実装：[✓](https://github.com/Spinozaaa/ReLope) ・ リポジトリ内被引用：0  
  画像で弱まる隠れ状態の正解信号を、注意集約とKL正則化付きLoRAで作り直し、マルチモーダルモデルのルーティングAUCを標準プローブから平均4ポイント以上引き上げる。

- **2026-03 · [Prompt Compression in Production Task Orchestration: A Pre-Registered Randomized Trial](2026-2603.23525-prompt-compression-in-production-task-orchestration-a-pre-registered-ran.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  評価対象は新しい圧縮モデルの開発でもGPUカーネルの高速化でもなく、指示のどの部分をどれだけ残すかという圧縮方針の費用対効果である。

- **2026-03 · [Mixture of Chapters: Scaling Learnt Memory in Transformers](2026-2603.21096-mixture-of-chapters-scaling-learnt-memory-in-transformers.md)**  
  実装：[✓](https://github.com/Tasmay-Tibrewal/Memory) ・ リポジトリ内被引用：0  
  Mixture of Chapters（MoC）は、言語モデルが事前学習で獲得する知識を、通常の重みとは別の学習可能な潜在記憶として保持し、入力に必要な部分だけを交差注意（cross-注意機構）で取り出す設計である。元のmain原稿にあった主要な正負両方の結果を維持し、計算量の内訳、選択単位、実施済み実験と将来計画の区別を明確化した。

- **2026-03 · [MemBoost: A Memory-Boosted Framework for Cost-Aware LLM Inference](2026-2603.26557-memboost-a-memory-boosted-framework-for-cost-aware-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  過去の回答を意味検索で再利用し、不足時だけ大規模モデルへ委ねて、その回答をメモリへ書き戻す三層の提供枠組みで、繰り返しの多い模擬負荷で小さいモデルでもオラクル並み以上の正解率を保ちながら高価な呼び出しを減らす。

- **2026-03 · [MaskLoRA: Low-Rank Subspace-Induced Token Masking for Efficient and Faithful Language Models](2026-0acd4305ac8f-masklora-low-rank-subspace-induced-token-masking-for-efficient-and-faith.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LoRAが各トークンの表現を動かした大きさを重要度の物差しにして不要なトークンを推論から外し、予測の一致を保つ学習と組み合わせることで、根拠の忠実さを保ちながら推論を高速化するトークン選択の仕組み。

- **2026-03 · [LooComp: Leverage Leave-One-Out Strategy to Encoder-only Transformer for Efficient Query-aware Context Compression](2026-2603.09222-loocomp-leverage-leave-one-out-strategy-to-encoder-only-transformer-for-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかし検索件数を増やすと、無関係な文章も入力され、事前充填の計算量、入力トークン費用、モデルの注意の分散が問題になる。生成型の圧縮器は文書を短い文章へ書き換えられるが、圧縮器自体がトークンを逐次生成するため遅延が大きくなる。

- **2026-03 · [Large Language Model as Token Compressor and Decompressor](2026-2603.25340-large-language-model-as-token-compressor-and-decompressor.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既成の言語モデルをLoRAで適応させ、長文を離散・可変長のZトークンへ圧縮して復号も行う自動符号化で、内容に応じた配分により長文脈のメモリと遅延を大きく削った。

- **2026-03 · [InfoDensity: Rewarding Information-Dense Traces for Efficient Reasoning](2026-2603.17310-infodensity-rewarding-information-dense-traces-for-efficient-reasoning.md)**  
  実装：[✓](https://github.com/amao0o0/InfoDensity) ・ リポジトリ内被引用：0  
  そこで、後方からの最大値包絡（suffix-max envelope）によって軌跡全体の形を要約し、同一問題に対する複数生成の相対的な長さで補正する報酬を設計した。原著表2では、DeepSeek-R1-Distill-Qwen-1.5Bの4ベンチマーク平均正答率が36.5%から50.8%へ上がり、平均生成長は11.1千から7.5千トークンへ短縮した。

- **2026-03 · [HiCI: Hierarchical Construction-Integration for Long-Context Attention](2026-2603.20843-hici-hierarchical-construction-integration-for-long-context-attention.md)**  
  実装：[✓](https://github.com/zengxyyu/HiCI) ・ リポジトリ内被引用：0  
  HiCI（Hierarchical Construction–Integration）は、長文脈言語モデルの注意機構を、セグメント単位の局所表現の構築、局所表現からの全体文脈の統合、全体と局所の情報を各セグメントへ再配信する処理へ分解する研究である。

- **2026-03 · [Frequency-Modulated Visual Restoration for Matryoshka Large Multimodal Models](2026-2603.11220-frequency-modulated-visual-restoration-for-matryoshka-large-multimodal-m.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FMVR（Frequency-Modulated Visual Restoration）は、削減済み視覚表現の平均値からの残差と最大値からの残差をそれぞれ学習可能な係数で変調し、目立つ特徴と埋もれた特徴の両方を補強する方式である。原著表3では36トークン時に初期入力処理時間が58.1から18.0ミリ秒へ短縮し、総メモリが21.6から13.8GBへ減少する。

- **2026-03 · [FineRMoE: Dimension Expansion for Finer-Grained Expert with Its Upcycling Approach](2026-2603.13364-finermoe-dimension-expansion-for-finer-grained-expert-with-its-upcycling.md)**  
  実装：[✓](https://github.com/liaoning97/FineRMoE) ・ リポジトリ内被引用：0  
  専門家の細粒度化を中間次元から出力次元へ広げ、二段の疎な計算と単一ルータ、両次元で分割するアップサイクリングで、Qwen2.5由来の全規模で10課題平均首位と高い推論効率を得る専門家混合の構造。

- **2026-03 · [Density-aware Soft Context Compression with Semi-Dynamic Compression Ratio](2026-2603.25926-density-aware-soft-context-compression-with-semi-dynamic-compression-rat.md)**  
  実装：[✓](https://github.com/yuyijiong/semi-dynamic-context-compress) ・ リポジトリ内被引用：0  
  文脈の情報密度を予測して離散的な圧縮率へ量子化する半動的ソフト圧縮で、完全動的化の崩壊を避けながら固定比率より高い正解率と圧縮率の両立を示す文脈圧縮方式。

- **2026-03 · [CRISP: Compressed Reasoning via Iterative Self-Policy Distillation](2026-2603.05433-crisp-compressed-reasoning-via-iterative-self-policy-distillation.md)**  
  実装：[✓](https://github.com/HJSang/CRISP_Reasoning_Compression) ・ リポジトリ内被引用：0  
  CRISP（Compressed Reasoning via Iterative Self-Policy Distillation）は、この余分な思考を生成後に切り落とすのではなく、モデルが自発的に短い推論を出すように学習する方式である。

- **2026-03 · [Consensus-Expert DynamicMoE: ARIMA-based Capacity Prediction with Adaptive Load Balancing for Sparse Models](2026-dbb1f579343b-consensus-expert-dynamicmoe-arima-based-capacity-prediction-with-adaptiv.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  主要実験では、Switch Transformer-base-8の9種類のGLUE評価指標を単純平均した値が、従来構成の80.5、共有専門家だけを導入した構成の81.0に対して、提案構成で81.6となる（原著表4。

- **2026-03 · [CLAG: Adaptive Memory Organization via Agent-Driven Clustering for Small Language Model Agents](2026-2603.15421-clag-adaptive-memory-organization-via-agent-driven-clustering-for-small-.md)**  
  実装：[✓](https://github.com/dmis-lab/CLAG) ・ リポジトリ内被引用：0  
  CLAGは、記憶を話題ごとのクラスタへ割り当てるエージェント主導のルーティング、割当先クラスタ内だけでリンク生成・要約更新を行う局所的進化、質問に関連するクラスタを先に選んでから個別記憶を検索する二段階検索の三つを結合する。原著付録Cによれば、200件のBioASQ質問で二段階検索が除外した記憶は平均8.02%にとどまる。

- **2026-03 · [Capability-Guided Compression: Toward Interpretability-Aware Budget Allocation for Large Language Models](2026-2603.16440-capability-guided-compression-toward-interpretability-aware-budget-alloc.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル圧縮では重みの絶対値、活性値、曲率や再構成誤差を基準に枝刈り・量子化の強さを選ぶ。従来のWanda重要度とのスピアマン順位相関は−0.054だったものの、ヘッド除去によるパープレキシティ悪化との相関は有意でなく、50%保持ではCGC-Lのパープレキシティ27.87が均一枝刈り27.57より悪化した。

- **2026-03 · [Bielik-Q2-Sharp: A Comparative Study of Extreme 2-bit Quantization Methods for a Polish 11B Language Model](2026-2603.04162-bielik-q2-sharp-a-comparative-study-of-extreme-2-bit-quantization-method.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ポーランド語十一ビーモデルへ六つの二ビット量子化を共通ヘッセ行列で比較し、クイップシャープが既存のコミュニティ量子化と互角、キューティップがビット当たり最良、回転系は生成で崩壊し、四流派が似た精度へ収束して手法に依らない天井を示唆した。

- **2026-03 · [AutoScout: Structured Optimization for Automating ML System Configuration](2026-2603.11603-autoscout-structured-optimization-for-automating-ml-system-configuration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MLシステムの階層的な設定空間を、木探索による構造選択と座標探索による密パラメータ調整に分け、特徴量優先順位のトーナメントと多忠実度シミュレータで探索を安く回し、学習で専門家調整比最大3.0倍を達成する自動設定器。

- **2026-03 · [Adapting Methods for Domain-Specific Japanese Small LMs: Scale, Architecture, and Quantization](2026-2603.18037-adapting-methods-for-domain-specific-japanese-small-lms-scale-architectu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  日本語の専門分野向け小規模モデルの適応を、訓練規模の最適点、土台モデルの選択、適応後の量子化の安全性の三段階で検証し、最適規模は4千件、日本語の継続事前学習が決定的に効き、量子化の可否は注意の構造で決まることを示した。

- **2026-02 · [Unlocking Edge Fine-Tuning: A Sample-Efficient Language-Empowered Split Fine-Tuning Framework](2026-e0f5024d7632-unlocking-edge-fine-tuning-a-sample-efficient-language-empowered-split-f.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル分割と連合集約に、正解付き参照入力との二経路対比で重要な推論トークンを重く学ぶ損失を組み合わせ、各課題800件の学習で分割微調整の精度を大きく引き上げた端末向け微調整枠組み。

- **2026-02 · [Test-Time Scaling with Diffusion Language Models via Reward-Guided Stitching](2026-2602.22871-test-time-scaling-with-diffusion-language-models-via-reward-guided-stitc.md)**  
  実装：[✓](https://github.com/roymiles/diffusion-stitching) ・ リポジトリ内被引用：0  
  本論文はこの無駄に着目し、拡散言語モデルの安価な並列探索から中間ステップを再利用する仕組みを提案する。さらにピークメモリはQwen PRM構成で約42.8GB、比較AR単体の約14.4GBより大きい。

- **2026-02 · [Stable Adaptive Thinking via Advantage Shaping and Length-Aware Gradient Regulation](2026-2602.22556-stable-adaptive-thinking-via-advantage-shaping-and-length-aware-gradient.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  思考の要否を制御トークンで選ぶ適応思考を、正しい長思考を罰しないアドバンテージ整形と長さ配慮型の勾配調整で安定化し、Qwen2.5で正解率を上げながら生成トークンを約4割減らす二段階学習。

- **2026-02 · [SR-TTT Does Not Learn Retrieval: A Correction and Mechanistic Post-Mortem of Surprisal-Aware Residual Test-Time Training](2026-2603.06642-sr-ttt-does-not-learn-retrieval-a-correction-and-mechanistic-post-mortem.md)**  
  実装：[✓](https://github.com/swamynathanvp/Surprisal-Aware-Residual-Test-Time-Training) ・ リポジトリ内被引用：0  
  本論文は、推論時学習（Test-Time 学習; TTT）を用いた長文系列モデルへ、驚き度（surprisal）に応じて選別したトークンを厳密なキー・バリュー（KV）キャッシュへ残す SR-TTT の初版（v1）を訂正し、その失敗を機構ごとに実験で切り分けた研究である。

- **2026-02 · [SPQ: An Ensemble Technique for Large Language Model Compression](2026-2602.18420-spq-an-ensemble-technique-for-large-language-model-compression.md)**  
  実装：[✓](https://github.com/JiaminYao/spq-compression) ・ リポジトリ内被引用：0  
  SPQ（SVD–枝刈り–量子化）は、大規模言語モデル（LLM）の重みメモリを削減する際、単一の圧縮手段をすべての層に一律に適用するのではなく、注意層には特異値分解（Singular Value Decomposition; SVD）による低ランク近似、フィードフォワード層（MLP）には活性統計に基づく構造的剪定…

- **2026-02 · [Sparsity Induction for Accurate Post-Training Pruning of Large Language Models](2026-2602.21652-sparsity-induction-for-accurate-post-training-pruning-of-large-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  枝刈り前に等価なスケーリング変換とスペクトルノルム損失で重み分布と特徴をスパース化に適した形へ誘導し、推論時の追加費用なしにポストトレーニング枝刈りの精度を上げる前処理方式。

- **2026-02 · [Scaling State-Space Models on Multiple GPUs with Tensor Parallelism](2026-2602.21144-scaling-state-space-models-on-multiple-gpus-with-tensor-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  状態空間モデル向けにチャネル分割と状態キャッシュで同期を減らすテンソル並列設計。Mambaで4GPU時に最大4.0倍のスループットと4倍のプロンプト長を実現した。

- **2026-02 · [Phase transitions in large language model compression](2026-a4909aa5b9a7-phase-transitions-in-large-language-model-compression.md)**  
  実装：[✓](https://github.com/whucs21Mzy/Model-Phase-Transitions) ・ リポジトリ内被引用：0  
  LLMのモデルサイズを削減する方法には、重みを低ビットへ丸める量子化、重要度の低い構造や重みを削除する枝刈り、重み行列を小さい行列の積で近似する低ランク分解がある。代表例はLLaMA-2-7Bの3ビット量子化、35%の非構造的枝刈り、5%の低ランク分解を組み合わせた構成である。

- **2026-02 · [Parallel Track Transformers: Enabling Fast GPU Inference with Reduced Synchronization](2026-2602.07306-parallel-track-transformers-enabling-fast-gpu-inference-with-reduced-syn.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデルを複数トラックへ分けてGPUごとに独立実行し、一定層ごとにだけ同期することで同期回数を最大16倍減らし、30Bモデルで最初のトークンまでの時間を15から30パーセント短縮するアーキテクチャ。

- **2026-02 · [NLI: Non-uniform Linear Interpolation Approximation of Nonlinear Operators](2026-2602.02988-nli-non-uniform-linear-interpolation-approximation-of-nonlinear-operator.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  非線形関数の区間分割を動的計画法で最適化した非一様線形補間の参照表と、二段アドレス変換の専用ユニットで、精度をほぼ落とさず非線形演算を四倍超効率化する方式。

- **2026-02 · [Neural Paging: Learning Context Management Policies for Turing-Complete Agents](2026-2603.02228-neural-paging-learning-context-management-policies-for-turing-complete-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  コンテキスト管理をページング問題として定式化し、推論本体から切り離した学習型コントローラと感度の頑健性 bound を提案する理論論文で、検証は合成トレースに限られる。

- **2026-02 · [Minimizing Response Latency in LLM-Based Agent Systems: A Comprehensive Survey](2026-34369c1e45a2-minimizing-response-latency-in-llm-based-agent-systems-a-comprehensive-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  計画のための追加生成、メモリ検索、外部API、ツール結果の統合、複数エージェント間のメッセージ、推論サーバのキュー待ちが逐次・並列に組み合わさるためである。

- **2026-02 · [MeKi: Memory-based Expert Knowledge Injection for Efficient LLM Scaling](2026-2602.03359-meki-memory-based-expert-knowledge-injection-for-efficient-llm-scaling.md)**  
  実装：[✓](https://github.com/ningding-o/MeKi) ・ リポジトリ内被引用：0  
  知識を読み出し専用メモリの参照表へ逃がし、有効計算を増やさずに容量だけを広げる端末向けスケーリングで、一点七ビーが密な四ビー級の品質へ同速度のまま迫る方式。

- **2026-02 · [LQA: A Lightweight Quantized-Adaptive Framework for Vision-Language Models on the Edge](2026-2602.07849-lqa-a-lightweight-quantized-adaptive-framework-for-vision-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像・テキストで量子化器を分け敏感な層を高精度に残す量子化と、正負の特徴キャッシュで勾配なしに適応する仕組みを組み合わせ、端末向け視覚言語モデルの精度を保ちながらメモリを最大19.9倍削減する方式。

- **2026-02 · [LLM-CoOpt: A Co-Design and Optimization Framework for Efficient LLM Inference on Heterogeneous Platforms](2026-2602.09323-llm-coopt-a-co-design-and-optimization-framework-for-efficient-llm-infer.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLM-CoOptは、一般的なGPUとはメモリ階層や実行単位が異なる計算装置にvLLMを移植したときの推論効率を改善するシステム最適化である。本文第4.3節の5種類のLLaMA系GPTQモデルでは、生成処理量が5.72～12.13%増加し、推論遅延が4.82～6.75%短縮した。

- **2026-02 · [Krause Synchronization Transformers](2026-2602.11534-krause-synchronization-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  内積と全体正規化を、距離に基づく動径基底関数と局所近傍・上位k選択へ置き換え、多クラスタ同期を保ちながら注意の計算量を線形化し精度も上げるKrause注意の提案。

- **2026-02 · [Improving the Trade-off Between Watermark Strength and Speculative Sampling Efficiency for Language Models](2026-2602.01428-improving-the-trade-off-between-watermark-strength-and-speculative-sampl.md)**  
  実装：[✓](https://github.com/hwq0726/watermark-tradeoff) ・ リポジトリ内被引用：0  
  一方、投機的サンプリングは小型のドラフトモデルが先読みした複数トークンを大型ターゲットモデルがまとめて検証し、受理できたトークンの分だけ逐次的な大型モデル呼び出しを減らす。ELI5とC4、LlamaおよびGemmaの二組のモデルで、1検証ステップ当たりの受理トークン数が通常投機的サンプリングとほぼ同じで、検出性能も改善することを確認した。

- **2026-02 · [HyPER: Bridging Exploration and Exploitation for Scalable LLM Reasoning with Hypothesis Path Expansion and Reduction](2026-2602.06527-hyper-bridging-exploration-and-exploitation-for-scalable-llm-reasoning-w.md)**  
  実装：[✓](https://github.com/ShengxuanQiu/HyPER) ・ リポジトリ内被引用：0  
  経路プールの信頼度と多様さを64トークンごとに観測して分岐・短区間拡張・1トークン精錬を使い分ける学習なしの制御と、長さと信頼度による最終投票で、Qwen3-NextのAIME24正解率を自己整合の90.7%から97.3%へ上げ、トークン費用を正規化値0.61まで下げた。

- **2026-02 · [Greedy-Gnorm: A Gradient Matrix Norm-Based Alternative to Attention Entropy for Head Pruning](2026-2602.04491-greedy-gnorm-a-gradient-matrix-norm-based-alternative-to-attention-entro.md)**  
  実装：[✓](https://github.com/dionysus23334/Greedy-Gnorm) ・ リポジトリ内被引用：0  
  ヘッドを1つ削るたびにクエリ・キー・バリュー勾配行列のノルムの積で重要度を計算し直す貪欲なヘッド枝刈りで、静的な注意エントロピーより滑らかな精度低下を実現し、BERTの容量を22.52パーセント削減する。

- **2026-02 · [Every Bit Counts: A Theoretical Study of Precision–Expressivity Tradeoffs in Quantized Transformers](2026-2602.02707-every-bit-counts-a-theoretical-study-of-precision-expressivity-tradeoffs.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、Transformerの量子化が単に近似誤差を増やすだけなのか、それとも十分な学習を行っても表現できない関数を生むのかを問う理論研究である。補助実験では、2ヘッド・埋め込み次元4の単層モデルに合成等値判定を学習させ、長さ100の課題で学習後量子化した場合、INT12の平均正答率94.95%に対してINT4は58.72%となる。

- **2026-02 · [Evaluating the Impact of Post-Training Quantization on Reliable VQA with Multimodal LLMs](2026-2602.13289-evaluating-the-impact-of-post-training-quantization-on-reliable-vqa-with.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像と言語を入力するマルチモーダル大規模言語モデル（MLLM）では、モデルの重みを低ビット量子化することで端末配置を容易にできる。VQAv2上のIdefics3ではbf16の精度79.3に対し、int4 HQQが77.2、int4 MBQが78.1、int3 HQQが64.0、int3 MBQが71.2となる。

- **2026-02 · [Efficient Post-Training Pruning of Large Language Models with Statistical Correction](2026-2602.07375-efficient-post-training-pruning-of-large-language-models-with-statistica.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  一次統計だけで重要度を較正し、枝刈り後の信号エネルギーを閉形式で戻す軽量な学習後枝刈り。再構成型の重い計算なしに、Wanda等の精度を一貫して押し上げる。

- **2026-02 · [Efficient Encoder-Free Fourier-based 3D Large Multimodal Model](2026-2602.23153-efficient-encoder-free-fourier-based-3d-large-multimodal-model.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Fase3Dは、重い専用3Dエンコーダを使わず、浅い多層パーセプトロン（MLP）と幾何的なスーパーポイント（superpoint）集約、空間充填曲線（Space-Filling Curve、SFC）に基づく1次元整列、高速フーリエ変換（Fast Fourier Transform、FFT）による文脈混合、疎グラフを用いたトークン統合で…

- **2026-02 · [Does Your Reasoning Model Implicitly Know When to Stop Thinking?](2026-2602.08354-does-your-reasoning-model-implicitly-know-when-to-stop-thinking.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  そこで本論文は、モデルの確率分布に「適切な時点で終了する」兆候がすでに含まれているのかを調べ、その情報を取り出す生成方式と学習方式を設計する。

- **2026-02 · [Decoupled Reasoning with Implicit Fact Tokens (DRIFT): A Dual-Model Framework for Efficient Long-Context Inference](2026-2602.10021-decoupled-reasoning-with-implicit-fact-tokens-drift-a-dual-model-framewo.md)**  
  実装：[✓](https://github.com/Lancelot-Xie/DRIFT) ・ リポジトリ内被引用：0  
  軽量な知識モデルが長文書のチャンクをクエリ条件付きで潜在的な事実トークンへ圧縮し、大きな推論モデルは生文ではなく圧縮表現だけを読んで答えることで、32倍圧縮でもLongBench v2の精度を20.87パーセントから29.22パーセントへ上げ、256kトークン文書で平均7倍速くした二重モデルの長文脈推論。

- **2026-02 · [Confidence-Driven Multi-Scale Model Selection for Cost-Efficient Inference](2026-2602.22090-confidence-driven-multi-scale-model-selection-for-cost-efficient-inferen.md)**  
  実装：[✓](https://github.com/NYCU-NLP-Lab/ConfDrivenInference) ・ リポジトリ内被引用：0  
  小さいモデルの選択肢確率P(T)と隠れ状態から学習した正答可能性P(IK)で自信度を測り、不確かなクエリだけを大きいモデルへ引き上げることで、MMLUで最大モデル並みの精度を保ちながら計算量を最大で約44パーセント、GPT-4oのトークンを約60パーセント削減した多段階モデル選択の研究。

- **2026-02 · [BAPS: A Fine-Grained Low-Precision Scheme for Softmax in Attention via Block-Aware Precision reScaling](2026-2602.02071-baps-a-fine-grained-low-precision-scheme-for-softmax-in-attention-via-bl.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  近似した行最大値での引き算を専用コア側へ寄せて注意スコアの差を八ビットのまま転送し、外れたブロックだけ高精度でやり直すことで、長文脈の単語抽出で高精度構成の六十四・八パーセントに対し六十四・〇パーセントを保ち、単純な八ビット化の五十四・〇パーセントへの崩れを防いだ。

- **2026-02 · [AttnPO: Attention-Guided Process Supervision for Efficient Reasoning](2026-2602.09953-attnpo-attention-guided-process-supervision-for-efficient-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AttnPO（注意機構-guided Policy Optimization）は、モデルが最終回答を生成するときに過去の思考のどの部分へ注意しているかを、思考段階ごとの重要性の代理指標として使う。

- **2026-02 · [AllMem: A Memory-centric Recipe for Efficient Long-context Modeling](2026-2602.13680-allmem-a-memory-centric-recipe-for-efficient-long-context-modeling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  局所を見るスライディングウィンドウ注意と、過去を非線形メモリへオンライン学習で圧縮するテスト時学習メモリを並列に組み合わせ、窓の外の情報を固定サイズのメモリで担うことで、長文脈でも計算量とキャッシュを文脈長から切り離すハイブリッド構造。

- **2026-02 · [AgentArk: Distilling Multi-Agent Intelligence into a Single LLM Agent](2026-2602.03955-agentark-distilling-multi-agent-intelligence-into-a-single-llm-agent.md)**  
  実装：[✓](https://github.com/AIFrontierLab/AgentArk) ・ リポジトリ内被引用：0  
  複数のLLMエージェントが同じ問題を検討し、相互に批判・訂正して最終回答を合意する方式は、単独モデルより複雑な推論を改善できることがある。Qwen3、Gemma3、Llama3系を含む120の実験で、単一モデルに比べた推論品質の改善と、学習信号の種類・学生モデルの規模・教師エージェント数の影響を分析する。

- **2026-02 · [ACL: Aligned Contrastive Learning Improves BERT and Multi-exit BERT Fine-tuning](2026-2602.03563-acl-aligned-contrastive-learning-improves-bert-and-multi-exit-bert-fine-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文のACLは整合対照学習（aligned contrastive learning）であり、分類モデルの交差エントロピー損失と教師あり対照学習損失が異なる方向へ重みを更新してしまう問題を扱う。しかし著者はRTE分類の予備実験で、両損失から得られる勾配のなす角度が約75〜105度に分布し、互いに逆向きの成分を持つバッチが存在することを観察した。

- **2026-02 · [A Replicate-and-Quantize Strategy for Plug-and-Play Load Balancing of Sparse Mixture-of-Experts LLMs](2026-2602.19938-a-replicate-and-quantize-strategy-for-plug-and-play-load-balancing-of-sp.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  過負荷のエキスパートを低精度で複製し、重要度の低いエキスパートの量子化で予算を賄う、再学習不要のMoE負荷分散策。不均衡スコアを最大で約1.4倍分改善し精度をほぼ保つ。

- **2026-01 · [You Need Better Attention Priors](2026-2601.15380-you-need-better-attention-priors.md)**  
  実装：[✓](https://github.com/elonlit/goat) ・ リポジトリ内被引用：0  
  注意の一様な事前分布を、フーリエ級数の相対位置成分とキー専用シンク成分からなる学習可能な事前分布へ置き換え、密なバイアスなしにFlashAttention互換の1回の内積注意で長文脈外挿とメモリ削減を得る機構。

- **2026-01 · [When to Think Fast and Slow? AMOR: Adaptive Entropy Gate for Hybrid Models](2026-2602.13215-when-to-think-fast-and-slow-amor-adaptive-entropy-gate-for-hybrid-models.md)**  
  実装：[✓](https://github.com/HaoranZhengRaul/AMOR) ・ リポジトリ内被引用：0  
  AMOR（適応的 Metacognitive Output Router）は、Mamba2またはGated DeltaNetの再帰型言語モデルに、トークンごとに必要性を判定して実行する注意ブロックを追加する方式である。ゲートの発火率は学習中に約40%となり、発火しない位置では注意の問い合わせと出力計算を省略する。

- **2026-01 · [Towards Understanding Best Practices for Quantization of Vision-Language Models](2026-2601.15287-towards-understanding-best-practices-for-quantization-of-vision-language.md)**  
  実装：[✓](https://github.com/gautomdas/mmq) ・ リポジトリ内被引用：0  
  本論文は、視覚言語モデル（Vision-Language モデル; VLM）を低ビット化するとき、視覚符号化器（Vision Transformer; ViT）、視覚と言語の接続器、言語モデル（LLM）のどこを何ビットにするのが有利かを、複数のタスクと量子化方式で比較する実証研究である。

- **2026-01 · [SPRINT: Scalable Secure & Differentially Private Inference for Transformers](2026-6e8bb6985b9f-sprint-scalable-secure-differentially-private-inference-for-transformers.md)**  
  実装：[✓](https://github.com/SAP/sprint) ・ リポジトリ内被引用：0  
  差分プライバシー付き微調整と秘密計算推論を、MPCの近似を微調整へ織り込む設計、固定型LoRA、平文パラメータの活用、安定な非線形近似で統合し、精度差1ポイント未満で先行方式より最大1.6倍速い秘匿推論方式SPRINT。

- **2026-01 · [SimMerge: Learning to Select Merge Operators from Similarity Signals](2026-2601.09473-simmerge-learning-to-select-merge-operators-from-similarity-signals.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数の重みを一つのモデルへ統合するモデル結合（モデル merging）は、複数モデルを同時常駐させずに能力をまとめる方法だが、どの結合演算子を使うか、どのチェックポイントを選ぶか、どの順番で結合するかによって結果が大きく変わる。

- **2026-01 · [SecMoE: Communication-Efficient Secure MoE Inference via Select-Then-Compute](2026-2601.06790-secmoe-communication-efficient-secure-moe-inference-via-select-then-comp.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  専門家の重みを暗号化された選択で1つだけ取り出してから計算することで、選択結果をサーバへ漏らさずに疎性を保ち、秘密保持推論の通信を最大約29.8倍減らした安全な専門家混合推論の研究。

- **2026-01 · [Scalable Generative Game Engine: Breaking the Resolution Wall via Hardware-Algorithm Co-Design](2026-2602.00608-scalable-generative-game-engine-breaking-the-resolution-wall-via-hardwar.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  世界モデルとデコーダの律速の違いに合わせてアクセラレータ配分・演算子融合・潜在外挿を設計し、生成ゲームの解像度を720かける480へ引き上げて毎秒26.4フレームを達成する協調設計。

- **2026-01 · [Routing with Generated Data: Annotation-Free LLM Skill Estimation and Expert Selection](2026-2601.09692-routing-with-generated-data-annotation-free-llm-skill-estimation-and-exp.md)**  
  実装：[✓](https://github.com/tianyiniu/RoutingGenData) ・ リポジトリ内被引用：0  
  本論文は、課題の短い説明だけを使って生成モデルに質問・回答対を作らせる「生成データによる振分け（ルーティング with Generated Data; RGD）」を定式化し、その環境に適したCASCAL（Consensus-Aware Skill Clustering and Aggregation for LLMs）を提案する。

- **2026-01 · [ROMA: Real-time Omni-Multimodal Assistant with Interactive Streaming Understanding](2026-2601.10323-roma-real-time-omni-multimodal-assistant-with-interactive-streaming-unde.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ただし、これは継続的な入力処理の平均時間であり、発話内容の生成時間、ネットワーク遅延、音声合成、極端に長い履歴を含むシステム全体の最悪応答遅延ではない。YouCook2の実況開始時刻のF1は35.21で、比較するVideoLLM-onlineの18.82を上回る。

- **2026-01 · [Queueing-Aware Optimization of Reasoning Tokens for Accuracy-Latency Trade-offs in LLM Servers](2026-2601.10274-queueing-aware-optimization-of-reasoning-tokens-for-accuracy-latency-tra.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論トークン予算をタスク種別ごとに割り当てる問題をM/G/1待ち行列で定式化し、精度と平均システム時間の目的関数が強凹で最適配分が一意になることを示し、不動点反復と射影勾配法で解く、待ち行列を意識した予算最適化の理論研究。

- **2026-01 · [QA-Merging: Query-Adaptive Reasoning via Layer Selective Model Merging](2026-2601.03506-qa-merging-query-adaptive-reasoning-via-layer-selective-model-merging.md)**  
  実装：[✓](https://github.com/Zephyr-Zhong/QA-Merging) ・ リポジトリ内被引用：0  
  長い思考過程を出すモデルと短い思考過程を出すモデルについて、両者の隠れ状態が大きく分かれる層だけを特徴合わせで較正し、残りの層は閉形式の隠れ状態補正で済ませて統合することで、難しい問いには長く、簡単な問いには短く答える単一モデルを作る統合方式。

- **2026-01 · [OnePiece: A Large-Scale Distributed Inference System with RDMA for Complex AI-Generated Content (AIGC) Workflows](2026-2601.20655-onepiece-a-large-scale-distributed-inference-system-with-rdma-for-comple.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  生成コンテンツの多段階処理をマイクロサービスへ分解し、片側RDMAと二重リングバッファ、利用率に応じた動的再配置でGPU利用効率を狙う分散推論基盤。ただし定量評価の提示が乏しく効果量は未検証である。

- **2026-01 · [ModeX: Evaluator-Free Best-of-N Selection for Open-Ended Generation](2026-2601.02535-modex-evaluator-free-best-of-n-selection-for-open-ended-generation.md)**  
  実装：[✓](https://github.com/deeplearning-wisc/ModeX) ・ リポジトリ内被引用：0  
  しかし従来は、正解と照合できる数学問題なら多数決が使える一方、自由記述の要約やプログラムでは文字列の一致が品質を表さない。別の大規模言語モデルを採点器として呼ぶ方式は、その採点器の推論費用と誤判定を持ち込む。

- **2026-01 · [Mixture-of-Models: Unifying Heterogeneous Agents via N-Way Self-Evaluating Deliberation](2026-2601.16863-mixture-of-models-unifying-heterogeneous-agents-via-n-way-self-evaluatin.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  異種LLMの編成を合意状態が回帰する意味的回帰ネットワークとして実行する審議プロトコルNSEDを提案し、ブローカーによる制約付きチーム編成、自己投票を禁じる二次投票、疲労モデルによる最適停止を備え、小型モデルの編成でAIME 2025の84.0パーセントを示す。

- **2026-01 · [LAMP: Look-Ahead Mixed-Precision Inference of Large Language Models](2026-2601.21623-lamp-look-ahead-mixed-precision-inference-of-large-language-models.md)**  
  実装：[✓](https://github.com/sbudzinskiy/LAMP-LLM) ・ リポジトリ内被引用：0  
  行列積の直後に続く非線形演算が丸め誤差を増幅する度合いを先読みし、注意機構のキー・クエリ内積などのうち数値的に敏感なごく一部だけを高精度で再累算することで、GPT-2 XLの低精度推論誤差を最大2桁超削減する混合精度累算フレームワーク。

- **2026-01 · [FourierSampler: Unlocking Non-Autoregressive Potential in Diffusion Language Models via Frequency-Guided Generation](2026-2601.23182-fouriersampler-unlocking-non-autoregressive-potential-in-diffusion-langu.md)**  
  実装：[✓](https://github.com/ShirleYoung/FourierSampler) ・ リポジトリ内被引用：0  
  拡散言語モデルの隠れ状態で低周波が構造、高周波が詳細を担うという発見に基づき、周波数窓を滑らせて構造から詳細へ復号順序を誘導し、LLaDAとSDARで数学とコードの精度を一貫して上げる学習不要のサンプラー。

- **2026-01 · [Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning](2026-2601.09708-fast-thinkact-efficient-vision-language-action-reasoning-via-verbalizabl.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Fast-ThinkActは、視覚・言語・行動モデル（Vision-Language-Action モデル、VLA）の推論に必要な長い文章形式の思考列を、少数の連続潜在表現へ圧縮する研究である。

- **2026-01 · [FAQ: Mitigating Quantization Error via Regenerating Calibration Data with Family-Aware Quantization](2026-2601.11200-faq-mitigating-quantization-error-via-regenerating-calibration-data-with.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  同系統の大モデルに較正文を書き直させ、競合選択と正規化で整えた較正データで通常の量子化を行うことで、八十億級モデルで全精度との精度差を最大二八・五パーセント縮めたと報告した。

- **2026-01 · [EUGens: Efficient, Unified, and General Dense Layers](2026-2601.22563-eugens-efficient-unified-and-general-dense-layers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全結合層の入力と重みをランダム特徴で分離し内積だけで結ぶEUGenで推論を線形時間化し、Mip-NeRF 360で品質を保ったまま27パーセント高速化、ViTで推論パラメータ約30パーセント削減を実証した層置換の研究。

- **2026-01 · [Entropy-Tree: Tree-Based Decoding with Entropy-Guided Exploration](2026-2601.15296-entropy-tree-tree-based-decoding-with-entropy-guided-exploration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークンのエントロピーと注意による重要度で分岐位置を選び、接頭辞を共有する木で推論経路を探索するEntropy-Treeは、同じ葉数の独立サンプリングより高いpass@kと良い不確実性推定を多くの条件で示すデコード手法。

- **2026-01 · [Efficient Paths and Dense Rewards: Probabilistic Flow Reasoning for Large Language Models](2026-2601.09260-efficient-paths-and-dense-rewards-probabilistic-flow-reasoning-for-large.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  標準的な思考の連鎖は、最終解答の正誤だけでは途中の推論ステップの有用性を直接測れず、冗長な言い換えや誤った分岐を含みやすい。CoT-Flowは、問題xと時点iまでの生成列sを持つ状態Iiにおいて、正解yの負の対数確率 D(Ii)=-log p(y\|Ii) を難しさと定義する。

- **2026-01 · [Do Not Waste Your Rollouts: Recycling Search Experience for Efficient Test-Time Scaling](2026-2601.21684-do-not-waste-your-rollouts-recycling-search-experience-for-efficient-tes.md)**  
  実装：[✓](https://github.com/WangXinglin/RSE) ・ リポジトリ内被引用：0  
  捨てられていた推論軌跡から正と負の経験を蒸留して共有バンクに蓄え次ラウンドへ再利用し、同じ計算予算でテスト時探索の到達精度を上げる学習不要の再利用戦略。

- **2026-01 · [DIP: Dynamic In-Context Planner For Diffusion Language Models](2026-2601.03199-dip-dynamic-in-context-planner-for-diffusion-language-models.md)**  
  実装：[✓](https://github.com/wmd3i/DIP) ・ リポジトリ内被引用：0  
  拡散言語モデルのブロック境界で、平均検証信頼度が落ちたときだけ文脈内例を段階的に挿入し、固定プロンプト比で最大1.59倍高速化する学習不要の文脈最適化方式。

- **2026-01 · [Context Tokens are Anchors: Understanding the Repetition Curse in dMLLMs from an Information Flow Perspective](2026-2601.20520-context-tokens-are-anchors-understanding-the-repetition-curse-in-dmllms-.md)**  
  実装：[✓](https://github.com/ErikZ719/CoTA) ・ リポジトリ内被引用：0  
  拡散型マルチモーダルモデルでキャッシュが引き起こす反復現象を、文脈トークンがアンカーであるという情報フロー分析で説明し、注意強化とエントロピー誘導投票のCoTAで隣接反復率を大幅に減らした研究。

- **2026-01 · [Conditional Performance Guarantee for Large Reasoning Models](2026-2601.22790-conditional-performance-guarantee-for-large-reasoning-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論モデルと非思考モデルの振り分け保証を全体平均から集団単位へ細かくし、集団ごとに閾値を較正するG-PACと不確かさのクラスタリングで集団を学ぶC-PACで、集団ごとの性能損失を許容範囲に収めながら思考トークンを節約する統計的枠組み。

- **2026-01 · [Can Vision-Language Models Handle Long-Context Code? An Empirical Study on Visual Compression](2026-2602.00746-can-vision-language-models-handle-long-context-code-an-empirical-study-o.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LongCodeOCRは、長大なプログラムの文脈を削除型のテキスト圧縮で短くする代わりに、コード全体を二次元画像へ描画し、視覚言語モデル（Vision-Language モデル; VLM）で読ませる方式である。

- **2026-01 · [Beyond Model Scaling: Test-Time Intervention for Efficient Deep Reasoning](2026-2601.11252-beyond-model-scaling-test-time-intervention-for-efficient-deep-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論中の転換表現の位置で生成を止め、外部評価者の合理性・完全性フィードバックを差し込んで続行と終了を決める対話型推論。AIME24で8K窓のもと正解率を7.19ポイント上げながら推論長を81パーセント削減する。

- **2026-01 · [Attention Needs to Focus: A Unified Perspective on Attention Allocation](2026-2601.00919-attention-needs-to-focus-a-unified-perspective-on-attention-allocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者らは前者を注意の過負荷、後者を注意の過少負荷と呼び、両者を注意重みの配分失敗として統一的に扱う。提案手法Lazy 注意機構は二つの機構からなる。340Mパラメータ・150億学習トークンの8課題平均は48.01%で、比較対象のGated DeltaNetの47.68%を上回る。

- **2026-01 · [APB-V: Accelerating Long-Video Understanding via Sequence-Parallelism-aware Approximate Attention](2026-2601.21444-apb-v-accelerating-long-video-understanding-via-sequence-parallelism-awa.md)**  
  実装：[✓](https://github.com/thunlp/APB) ・ リポジトリ内被引用：0  
  入力を間引く方式では一瞬しか映らない文字・物体・順序の手掛かりを失いやすい。原著のQwen2.5VL-3B・64フレーム・1440p動画の条件では、APB-VはFlashAttention比12.72倍、ZigZagRing比1.70倍、先行APB比1.18倍の処理量を報告する。

- **2025-12 · [You Only Need Your Transformer 25% of the Time: Meaning-First Execution for Eliminating Unnecessary Inference](2025-2601.00847-you-only-need-your-transformer-25-of-the-time-meaning-first-execution-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の量子化、枝刈り、KVキャッシュ最適化、投機的復号は、モデルを実行することを前提に一回当たりの計算費用を削減する。論文は、1,000件の要求を用いた主実験で781件（78.1%）のTransformer実行を回避し、残り219件について無条件実行と完全一致する出力を得たと報告する。

- **2025-12 · [XLM: A Python package for non-autoregressive language models](2025-2512.17065-xlm-a-python-package-for-non-autoregressive-language-models.md)**  
  実装：[✓](https://github.com/dhruvdcoder/xlm-core) ・ リポジトリ内被引用：0  
  これに対して、非自己回帰言語モデルにはマスク拡散、挿入型生成、編集型生成など複数の方式がある。

- **2025-12 · [SparseSwaps: Tractable LLM Pruning Mask Refinement at Scale](2025-2512.10922-sparseswaps-tractable-llm-pruning-mask-refinement-at-scale.md)**  
  実装：[✓](https://github.com/ZIB-IOL/SparseSwaps) ・ リポジトリ内被引用：0  
  行単位の疎制約でマスク選択を行ごとに分離し、グラム行列で1件交換の正確な効果を定数時間評価して既存枝刈りマスクを単調改善し、層誤差を最大60パーセント減らす後付け改良法。

- **2025-12 · [SASQ: Static Activation Scaling for Quantization-Aware Training in Large Language Models](2025-2512.14481-sasq-static-activation-scaling-for-quantization-aware-training-in-large-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低ビット量子化はモデルのメモリ容量や演算費用を減らすが、推論時に活性値の最大値を観測してスケールを更新する動的量子化では、毎回のスケール計算やデータ変換が発生する。

- **2025-12 · [RouteRAG: Efficient Retrieval-Augmented Generation from Text and Graph via Reinforcement Learning](2025-2512.09487-routerag-efficient-retrieval-augmented-generation-from-text-and-graph-vi.md)**  
  実装：[✓](https://github.com/YucanGuo/RouteRAG) ・ リポジトリ内被引用：0  
  RouteRAGは、言語モデルが推論途中に外部知識を調べる際、通常の文書検索、知識グラフ検索、両者の混合検索を状況に応じて切り替える方策を強化学習で獲得する検索拡張生成方式である。

- **2025-12 · [Rhea: Role-aware Heuristic Episodic Attention for Conversational LLMs](2025-2512.06869-rhea-role-aware-heuristic-episodic-attention-for-conversational-llms.md)**  
  実装：[✓](https://github.com/ddInference/Rhea) ・ リポジトリ内被引用：0  
  会話履歴を指示メモリとエピソードメモリへ役割分離し、応答だけの潜在圧縮と類似度による粒度付き検索で文脈の汚染・希釈・ドリフトを抑え、Long-MT-Bench+の精度を6.32から7.36へ上げる多ターン対話の文脈管理。

- **2025-12 · [Post-Training Quantization of OpenPangu Models for Efficient Deployment on Atlas A2](2025-2512.23367-post-training-quantization-of-openpangu-models-for-efficient-deployment-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単なる量子化誤差の研究ではなく、Ascendの演算子テンプレートライブラリCATLASSへ、量子化された重み配置、逆量子化、行列積を組み込み、不要な形式変換を避ける実行経路を構築する点が推論基盤上の寄与である。実測の前処理（プリフィル）では、バッチ32のFP16遅延5419msがINT8で3611msへ減少し、1.50倍の高速化となる。

- **2025-12 · [Parallel Decoder Transformer: Planner-Conditioned Latent Coordination for Model-Intrinsic Parallel Generation](2025-2512.10054-parallel-decoder-transformer-planner-conditioned-latent-coordination-for.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Parallel Decoder Transformer（PDT）は、モデル自身に三つの持続的な自己回帰生成前線を持たせる構造を提案する。重要な品質境界：本稿が確認した2026年7月18日改訂v3は、設計、実装、学習計画、評価プロトコルを記した研究であり、学習済みモデルの品質改善や実機速度向上を報告していない。

- **2025-12 · [Multiscale Aggregated Hierarchical Attention (MAHA): A Game-Theoretic and Optimization-Driven Approach to Efficient Contextual Modeling in Large Language Models](2025-2512.14925-multiscale-aggregated-hierarchical-attention-maha-a-game-theoretic-and-o.md)**  
  実装：[✓](https://github.com/canererden/MAHA-Project) ・ リポジトリ内被引用：0  
  MAHA（Multiscale Aggregated Hierarchical 注意機構）は、入力トークンを複数の解像度へ縮約し、それぞれの尺度で注意を計算した後、尺度ごとの出力を凸最適化またはゲーム理論に基づく重みで統合する注意機構である。

- **2025-12 · [MIDUS: Memory-Infused Depth Up-Scaling](2025-2512.13751-midus-memory-infused-depth-up-scaling.md)**  
  実装：[✓](https://github.com/MLAI-Yonsei/midus-hml) ・ リポジトリ内被引用：0  
  MIDUS（メモリ-Infused Depth Up-Scaling）は、既存の言語モデルの層数を増やすDepth Up-Scaling（DUS）の追加パラメータと計算を削減するモデル拡張方式である。

- **2025-12 · [LangCompress: Language-Aware Compression of Large Language Models](2025-1015f01478e5-langcompress-language-aware-compression-of-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  対象言語の指示データをモデル自身に合成させ、頻度の高いキートークンだけへ語彙ヘッドを切り詰めることで、既存の枝刈りと量子化を低資源言語でも崩壊させずに効かせる言語適応型の圧縮枠組み。

- **2025-12 · [Hierarchical Sparse Plus Low Rank Compression of LLM](2025-2601.07839-hierarchical-sparse-plus-low-rank-compression-of-llm.md)**  
  実装：[✓](https://github.com/misterpawan/hi-solo-llm) ・ リポジトリ内被引用：0  
  大きな重みをスパースに取り出し、残差をRCM順序付けしてから対角は密・非対角は低ランクという階層因数分解（HSS）で近似する重み圧縮sHSSを提案し、LLaMA-7Bの注意射影で保存量最大1.7倍削減とスパース＋SVD系より良いパープレキシティを示す。

- **2025-12 · [FP2: A 2-bit Floating-Point Format for Edge-AI Inference and Fine-Tuning](2025-c5badaa23ebf-fp2-a-2-bit-floating-point-format-for-edge-ai-inference-and-fine-tuning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  隣接2値で符号と指数または仮数を共有し実効2ビットの浮動小数点形式を作り、積和をビット加算へ置き換えることで、FP4比47パーセントの容量削減と最大78パーセントの処理要素面積・電力削減を、精度低下1から2ポイント程度で両立させる形式と計算アーキテクチャ。

- **2025-12 · [Efficient-VLN: A Simple yet Strong Baseline for Efficient Vision-Language Navigation](2025-2512.10310-efficient-vln-a-simple-yet-strong-baseline-for-efficient-vision-language.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論の中核は、回転位置埋め込み（Rotary Position Embedding; RoPE）を適用する前のKVをフレームごとに保存し、次の行動では必要な過去フレームのKVだけを選択して連続した位置IDで再回転する仕組みである。

- **2025-12 · [Dynamic Rank Reinforcement Learning for Adaptive Low-Rank Multi-Head Self-Attention in Large Language Models](2025-2512.15973-dynamic-rank-reinforcement-learning-for-adaptive-low-rank-multi-head-sel.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意の低ランク近似のランクを、摂動上界の安全検査付き強化学習で入力と層ごとに動的に選び、長系列で演算量を4割減らしながら全ランクに近い精度を保つ。

- **2025-12 · [Demystifying LLM-as-a-Judge: Analytically Tractable Model for Inference-Time Scaling](2025-2512.19905-demystifying-llm-as-a-judge-analytically-tractable-model-for-inference-t.md)**  
  実装：[✓](https://github.com/I-Halder/Demystifying-LLM-as-a-Judge-Analytically-Tractable-Model-for-Inference-Time-Scaling) ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）の推論時に複数の回答を生成し、別の評価モデル（LLM-as-a-Judge）が良い回答を選ぶ方式は、学習済みのモデル重みを変更せずに品質を改善する手段である。

- **2025-12 · [D2Pruner: Debiased Importance and Structural Diversity for MLLM Token Pruning](2025-2512.19443-d2pruner-debiased-importance-and-structural-diversity-for-mllm-token-pru.md)**  
  実装：[✓](https://github.com/EvelynZhang-epiclab/D2Pruner) ・ リポジトリ内被引用：0  
  注意の位置バイアスを差し引いて重要度を直し、空間と意味のハイブリッドグラフ上で最大独立集合を選ぶことで、視覚トークンを90パーセント削っても局所化性能の85.7パーセントを保ち、プリフィルを最大5.09倍速くした学習不要のマルチモーダルモデル向けトークン枝刈り。

- **2025-12 · [Compass: Co-Exploration of Mapping and Hardware for Heterogeneous Multi-Chiplet Accelerators Targeting LLM Inference Service Workloads](2025-2512.06093-compass-co-exploration-of-mapping-and-hardware-for-heterogeneous-multi-c.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  混在するリクエスト種類と可変系列長の提供ワークロードを、マイクロバッチと層の二次元グラフ符号化で表し、系列長分布に合わせて遺伝的探索でチップレット配置を最適化することで、エネルギー遅延積を先行探索手法から平均約63パーセント削減するマッピング探索フレームワーク。

- **2025-12 · [Can LLMs Predict Their Own Failures? Self-Awareness via Internal Circuits](2025-2512.20578-can-llms-predict-their-own-failures-self-awareness-via-internal-circuits.md)**  
  実装：[✓](https://github.com/Amirhosein-gh98/Gnosis) ・ リポジトリ内被引用：0  
  回答文中の自己申告の確信度も、誤った回答に対して高い確信を示す問題がある。提案方式は、生成モデル本体の重みを変更せず、生成中に現れる隠れ状態（Hidden States）と注意重み（注意機構 Maps）の時系列的な特徴を抽出する。これは判定器の時間比較であり、回答を生成する言語モデル全体が37倍または99倍速くなるという意味ではない。

- **2025-12 · [BitStopper: An Efficient Transformer Attention Accelerator via Stage-fusion and Early Termination](2025-2512.06457-bitstopper-an-efficient-transformer-attention-accelerator-via-stage-fusi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キーを1ビットずつ読みながら部分スコアで不要トークンを早期に打ち切り、独立したスパース予測段を消した注意アクセラレータ。Sanger比2.03倍、SOFA比1.89倍の高速化を品質悪化ほぼなしで得る。

### 2年前（2024-12〜2025-11）

- **2025-08 · [Dream 7B: Diffusion Large Language Models](2025-2508.15487-dream-7b-diffusion-large-language-models.md)**  
  実装：[✓](https://github.com/DreamLM/Dream) ・ リポジトリ内被引用：158  
  自己回帰モデルから初期化した70億拡散言語モデルで、系列全体の反復復元により計画課題と任意順生成を強化し、推論反復数で品質と速度を調整する。

- **2025-03 · [Block Diffusion: Interpolating Between Autoregressive and Diffusion Language Models](2025-2503.09573-block-diffusion-interpolating-between-autoregressive-and-diffusion-langu.md)**  
  実装：[✓](https://github.com/kuleshov-group/bd3lms) ・ リポジトリ内被引用：129  
  マスク率をデータに応じて区間制限する学習方式と、清浄系列・雑音系列を特殊注意で同時処理する実装を導入した。

- **2025-03 · [L1: Controlling How Long A Reasoning Model Thinks With Reinforcement Learning](2025-2503.04697-l1-controlling-how-long-a-reasoning-model-thinks-with-reinforcement-lear.md)**  
  実装：[✓](https://github.com/cmu-l3/l1) ・ リポジトリ内被引用：65  
  長い思考は難問での正答率を上げ得るが、単純な問題に数千トークンを費やすと不要な逐次生成が増える。著者が提案する長さ制御方策最適化（Length Controlled Policy Optimization、LCPO）には二種類ある。指定長との平均偏差は数学課題で約3%である。

- **2025-09 · [Fast-dLLM v2: Efficient Block-Diffusion LLM](2025-2509.26328-fast-dllm-v2-block-diffusion-hierarchical-cache.md)**  
  実装：[✓](https://github.com/NVlabs/Fast-dLLM/tree/main/v2) ・ リポジトリ内被引用：58  
  自己回帰モデルをブロック拡散へ少量追加学習し、ブロック間KVキャッシュとブロック内DualCache、信頼度並列復号を階層化して品質を保ちながら生成を高速化する。

- **2025-01 · [Titans: Learning to Memorize at Test Time](2025-2501.00663-titans-learning-to-memorize-at-test-time.md)**  
  実装：✓ ・ リポジトリ内被引用：55  
  長い系列を処理する言語モデルでは、直近の情報を精密に参照する短期記憶と、遠い過去から重要な情報を残す長期記憶の両立が難しい。一方、線形再帰型モデルは過去を小さな状態へ圧縮できるが、重要な出来事をどのように選択して長く保持するかに制約がある。

- **2024-12 · [Token-Budget-Aware LLM Reasoning](2024-2412.18547-token-budget-aware-llm-reasoning.md)**  
  実装：[✓](https://github.com/GeniusHTX/TALE) ・ リポジトリ内被引用：53  
  そこで問題ごとに適切な予算を推定する推論時方式TALE-EPと、適切な予算下の短い正答を学習させる事後学習方式TALE-PTを提案する。

- **2025-02 · [TokenSkip: Controllable Chain-of-Thought Compression in LLMs](2025-2502.12067-tokenskip-controllable-chain-of-thought-compression-in-llms.md)**  
  実装：[✓](https://github.com/hemingkx/TokenSkip) ・ リポジトリ内被引用：51  
  思考連鎖（Chain-of-Thought、CoT）は、複雑な数学や論理の問題を段階的に解くことで大規模言語モデルの正答率を改善する。保持率を条件として複数の圧縮版を学習させ、推論時に指定した保持率に応じて短い思考列をモデル自身が直接生成するようにする。

- **2025-02 · [Chain of Draft: Thinking Faster by Writing Less](2025-2502.18600-chain-of-draft-thinking-faster-by-writing-less.md)**  
  実装：[✓](https://github.com/sileix/chain-of-draft) ・ リポジトリ内被引用：49  
  Chain of 下書き（CoD）は、推論連鎖（Chain-of-Thought; CoT）の冗長な自然言語を減らし、必要な中間計算だけを短いドラフトとして生成させるprompting方式である。

- **2025-02 · [Training Language Models to Reason Efficiently](2025-2502.04463-training-language-models-to-reason-efficiently.md)**  
  実装：[✓](https://github.com/Zanette-Labs/efficient-reasoning) ・ リポジトリ内被引用：44  
  長い思考過程を生成する推論モデルは、難しい問題で高い正答率を得られる一方、簡単な問題でも冗長な検討を続けることがある。本論文は、正答を優先したまま正解応答の長さに罰則を与えるオンライン強化学習を提案する。7Bの5タスク平均では、長さ罰則 $\alpha=0.2$ の場合、基準モデルに対して生成トークン数が51.58%、正答率が95.94%となった。

- **2025-03 · [Qwen2.5-Omni Technical Report](2025-2503.20215-qwen2-5-omni-technical-report.md)**  
  実装：[✓](https://github.com/QwenLM/Qwen2.5-Omni) ・ リポジトリ内被引用：42  
  従来の視覚言語モデルや音声言語モデルを単に接続すると、動画フレームと音声の時間対応が失われやすく、音声出力のために全文の生成完了を待つ設計では初回音声までの遅延が大きい。原著の7B級モデルは、音声・映像を混合するOmniBenchで平均56.13%を示し、比較表のGemini 1.5 Proの42.91%を上回った。

- **2025-02 · [CoT-Valve: Length-Compressible Chain-of-Thought Tuning](2025-2502.09601-cot-valve-length-compressible-chain-of-thought-tuning.md)**  
  実装：✓ ・ リポジトリ内被引用：37  
  CoT-Valveは、推論モデルが簡単な問題にも長い思考連鎖（Chain of Thought、CoT）を生成してしまう無駄を減らし、同じ重みを基盤とするモデルで思考列の長さを柔軟に変える手法である。

- **2024-12 · [C3oT: Generating Shorter Chain-of-Thought without Compromising Effectiveness](2024-2412.11664-c3ot-generating-shorter-chain-of-thought-without-compromising-effectiven.md)**  
  実装：✓ ・ リポジトリ内被引用：33  
  C3oT（Conditioned Compressed Chain-of-Thought）は、言語モデルが回答の前に生成する長い思考連鎖（Chain of Thought、CoT）を短くしながら、長い思考で獲得した推論能力を保持するための条件付き学習方式である。

- **2025-09 · [Qwen3-Omni Technical Report](2025-2509.17765-qwen3-omni-technical-report.md)**  
  実装：✓ ・ リポジトリ内被引用：32  
  Qwen3-Omniは、テキスト、画像、音声、動画の入力を統合し、テキスト応答と音声応答を生成する大規模多モーダルモデルである。原著の理論的な初回パケット遅延は、同時要求1件で音声入力234ms、動画を含む入力547msである。

- **2025-07 · [Step-3 is Large yet Affordable: Model-system Co-design for Cost-effective Decoding](2025-2507.19427-step-3-is-large-yet-affordable-model-system-co-design-for-cost-effective.md)**  
  実装：[✓](https://github.com/stepfun-ai/StepMesh) ・ リポジトリ内被引用：31  
  単純に総パラメータや活性パラメータを減らすのではなく、モデルの注意機構とサービング時のGPU配置を一緒に設計し、長い思考系列の復号費用を下げる。

- **2025-04 · [Reasoning Models Can Be Effective Without Thinking](2025-2504.09858-reasoning-models-can-be-effective-without-thinking.md)**  
  実装：✓ ・ リポジトリ内被引用：29  
  大規模推論モデルは、最終回答の前に長い思考列（chain of thought、CoT）を生成することで数学、プログラミング、定理証明の精度を高めている。形式定理証明では長い思考より3.3～3.7倍少ないトークンで同程度のpass@kを得る。

- **2024-12 · [Compressed Chain of Thought: Efficient Reasoning Through Dense Representations](2024-2412.13171-compressed-chain-of-thought-efficient-reasoning-through-dense-representa.md)**  
  実装：✓ ・ リポジトリ内被引用：27  
  本研究は、言語モデルの推論精度を高めるために長い自然言語の思考連鎖（Chain of Thought; CoT）を生成すると、回答前の自己回帰復号に多くの時間がかかる問題を扱う。自然言語の思考文を一度すべて生成してから圧縮する方式ではない。

- **2025-02 · [BumbleBee: Secure Two-party Inference Framework for Large Transformers](2025-93b16acfd7b9-bumblebee-secure-two-party-inference-framework-for-large-transformers.md)**  
  実装：[✓](https://github.com/AntCPLab/OpenBumbleBee) ・ リポジトリ内被引用：25  
  入力とモデル重みをそれぞれ秘匿したままBERT、GPT-2、LLaMA-7B、ViTを実行し、従来方式に比べて実測の転送量と実行時間を改善する。

- **2024-12 · [NVILA: Efficient Frontier Visual Language Models](2024-2412.04468-nvila-efficient-frontier-visual-language-models.md)**  
  実装：[✓](https://github.com/NVlabs/VILA) ・ リポジトリ内被引用：25  
  NVILAは解像度を先に上げて必要な情報を取り込み、その後に空間・時間方向の冗長性を圧縮する「拡大してから圧縮する（scale-then-compress）」設計を採用する。

- **2025-02 · [CODI: Compressing Chain-of-Thought into Continuous Space via Self-Distillation](2025-2502.21074-codi-compressing-chain-of-thought-into-continuous-space-via-self-distill.md)**  
  実装：[✓](https://github.com/zhenyi4/codi) ・ リポジトリ内被引用：23  
  CODI（Continuous Chain-of-Thought via Self-Distillation）は、推論過程を自然言語の単語列として毎回生成する費用を減らすため、明示的な思考連鎖（Chain-of-Thought; CoT）を少数の連続潜在状態へ移す学習方式である。

- **2025-06 · [MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents](2025-2506.15841-mem1-learning-to-synergize-memory-and-reasoning-for-efficient-long-horiz.md)**  
  実装：[✓](https://github.com/MIT-MI/MEM1) ・ リポジトリ内被引用：19  
  従来の全履歴追記方式では、過去の検索結果が毎ターンのプロンプトへ残るため、文脈長に比例して鍵値キャッシュの容量が増え、注意計算や再入力の費用も高くなる。16目標の多段質問応答では、Qwen2.5-14B-Instructの完全一致数0.567に対しMEM1は1.97、ピークトークン数は3,840に対し1,040、推論時間は29.7秒に対し8.70秒だった。

- **2025-10 · [DeepSeek-OCR: Contexts Optical Compression](2025-2510.18234-deepseek-ocr-contexts-optical-compression.md)**  
  実装：[✓](https://github.com/deepseek-ai/DeepSeek-OCR) ・ リポジトリ内被引用：18  
  本研究は、長いテキストをそのまま多数の言語トークンとして処理する代わりに、文書を二次元の画像として扱い、少数の視覚トークンへ圧縮できるかを検証する。英語文書のFox評価では、画像化した元テキストの約10倍圧縮に相当する視覚トークン数でも文字復元精度がおおむね97%に達する。

- **2025-05 · [Llama-Nemotron: Efficient Reasoning Models](2025-2505.00949-llama-nemotron-efficient-reasoning-models.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  Nano（80億）、Super（490億）、Ultra（2530億）の3規模を提供し、通常の会話と詳細な推論を同じモデルで切り替えられる。実測ではSuperが単一H100上、バッチ256の指定条件で元のLlama 3.3-70Bに対して5倍のスループットを報告し、Ultraは8枚のH100で元のLlama 3.1-405Bに対して1.71倍の遅延改善を得た。

- **2025-06 · [MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention](2025-2506.13585-minimax-m1-scaling-test-time-compute-efficiently-with-lightning-attentio.md)**  
  実装：[✓](https://github.com/MiniMax-AI/MiniMax-M1) ・ リポジトリ内被引用：10  
  MiniMax-M1は、推論時に長い思考過程を生成する大規模言語モデルで、生成トークンが増えるほど従来のSoftmax注意の計算・記憶費用が膨らむ問題に対処する。モデル全体は4560億パラメータ、トークンごとの活性化は459億パラメータの混合専門家モデル（Mixture of エキスパート、MoE）である。

- **2025-10 · [StreamingTOM: Streaming Token Compression for Efficient Video Understanding](2025-2510.18269-streamingtom-streaming-token-compression-for-efficient-video-understandi.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  未来フレームを使わず、隣接フレームとの変化と顕著さでフレームごとに五十トークンだけを言語モデルへ通し、残りを四ビットで蓄積して質問時に必要な分だけ復元することで、鍵値キャッシュを一五・七倍に圧縮しながら無学習方式で最良の精度を示した。

- **2025-05 · [Let LRMs Break Free from Overthinking via Self-Braking Tuning](2025-2505.14604-let-lrms-break-free-from-overthinking-via-self-braking-tuning.md)**  
  実装：[✓](https://github.com/ZJU-REAL/Self-Braking-Tuning) ・ リポジトリ内被引用：9  
  従来の出力トークン予算や推論時の外部停止判定では、問題の難しさと必要な推論深度を一律に扱ったり、追加の判定機構が必要になったりする。

- **2025-01 · [Rope to Nope and Back Again: A New Hybrid Attention Strategy](2025-2501.18795-rope-to-nope-and-back-again-a-new-hybrid-attention-strategy.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  大規模言語モデル（large language モデル; LLM）で長い入力を処理すると、全トークン同士の注意（注意機構）計算は入力長Lの二乗に近い費用を要する。長文脈評価では256Kトークンでの検索・質問応答が改善し、局所層を増やすことで長文推論時のキー・値キャッシュ（key-value キャッシュ; KVキャッシュ）も減らせる。

- **2024-12 · [WebLLM: A High-Performance In-Browser LLM Inference Engine](2024-2412.15803-webllm-a-high-performance-in-browser-llm-inference-engine.md)**  
  実装：[✓](https://github.com/mlc-ai/web-llm) ・ リポジトリ内被引用：7  
  新しい注意機構や学習アルゴリズムではなく、ブラウザで効率的な言語モデル実行を成立させるシステム統合が主要な貢献である。ブラウザ版はネイティブ版より遅いが、復号処理率の約71.2～79.6%を保持した。

- **2024-12 · [Flash Communication: Reducing Tensor Parallelization Bottleneck for Fast Large Language Model Inference](2024-2412.04964-flash-communication-reducing-tensor-parallelization-bottleneck-for-fast-.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  大規模モデルでは行列積の後に各GPUの部分結果を集約する必要があり、GPU間の接続帯域が低い環境では、この通信が前段入力処理（プリフィル）の主要な待ち時間になる。提案方式は、活性値を細粒度に量子化して転送量を削減し、リング型の逐次的な集約ではなく、全対全による分散集約とAll-Gatherによる結果配布を二段階で行う。

- **2025-05 · [GMSA: Enhancing Context Compression via Group Merging and Layer Semantic Alignment](2025-2505.12215-gmsa-enhancing-context-compression-via-group-merging-and-layer-semantic-.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  GMSAは、原文を文字列として間引くのではなく、少数の連続表現トークン（soft トークン）へ変換する文脈圧縮方式である。NaturalQuestionsの4倍圧縮では完全一致（Exact Match、EM）が58.12%で、元文脈をそのまま与える条件の15.07%を上回った。

- **2025-04 · [Activated LoRA: Fine-tuned LLMs for Intrinsics](2025-2504.12397-activated-lora-fine-tuned-llms-for-intrinsics.md)**  
  実装：[✓](https://github.com/tdoublep/vllm/tree/alora) ・ リポジトリ内被引用：6  
  しかし複数のLoRAを一つの長い会話やエージェント処理で切り替える場合、過去の文脈の鍵・値（Key-Value; KV）キャッシュは、アダプタが異なれば一般に同じにならない。vLLMを改造した7モデルの評価器呼び出し実験では、長い接頭辞に対して評価器単体の最大35倍高速化を報告する。

- **2025-02 · [CipherPrune: Efficient and Scalable Private Transformer Inference](2025-2502.16782-cipherprune-efficient-and-scalable-private-transformer-inference.md)**  
  実装：[✓](https://github.com/UCF-Lou-Lab-PET/cipher-prune-inference) ・ リポジトリ内被引用：6  
  暗号化されたまま重要度を計算して不要トークンを層ごとに段階的に捨て、低重要度トークンには低次多項式を割り当てることで、秘匿推論を入力128トークンで約6.1倍、512トークンで約10.6倍高速化した。

- **2025-08 · [Towards Efficient and Practical GPU Multitasking in the Era of LLM](2025-2508.08448-towards-efficient-and-practical-gpu-multitasking-in-the-era-of-llm.md)**  
  実装：[✓](https://github.com/ovg-project) ・ リポジトリ内被引用：5  
  この論文は、GPUの単独実行（Singletasking）から多重実行（Multitasking）への移行を主張する設計論・立場論文（Position Paper）である。本文の「10%まで下がる利用率」やGPU世代間の成長率は背景の参考値であり、提案法がGPU使用率を何ポイント改善したという実験結果ではない。

- **2025-08 · [Breaking the Layer Barrier: Remodeling Private Transformer Inference with Hybrid CKKS and MPC](2025-2508.19525-breaking-the-layer-barrier-remodeling-private-transformer-inference-with.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  層を演算子へ分解して隣り合う線形演算を境界を越えて融合し、近似数向け準同型暗号の安全な変換と回転の少ない行列積を組み合わせることで、秘匿推論の通信をボルト比で最大21倍、遅延を画像処理装置利用時13倍まで削減した。

- **2025-01 · [ProxSparse: Regularized Learning of Semi-Structured Sparsity Masks for Pretrained LLMs](2025-2502.00258-proxsparse-regularized-learning-of-semi-structured-sparsity-masks-for-pr.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  二値マスクの硬い制約を正則化へ緩和してマスクを全層横断で学習することで、ラマ二・七十億版のパープレキシティをワンダ比で約三十五パーセント改善した半構造化枝刈り手法。

- **2025-11 · [Nemotron-Flash: Towards Latency-Optimal Hybrid Small Language Models](2025-2511.18890-nemotron-flash-towards-latency-optimal-hybrid-small-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  GPUで1トークンずつ復号する際、層を何回順に通過するか、どの演算子が起動されるか、状態やKVをどれだけ転送するかが遅延を決める。Nemotron-Flashは、モデルの大きさよりも実際のGPU上での遅延制約を第一の設計目標とする。

- **2025-11 · [A Comprehensive Study on Visual Token Redundancy for Discrete Diffusion-based Multimodal Large Language Models](2025-2511.15098-a-comprehensive-study-on-visual-token-redundancy-for-discrete-diffusion-.md)**  
  実装：[✓](https://github.com/Yrdal3910/dMLLM-Visual-Token-Redundancy-Analysis) ・ リポジトリ内被引用：4  
  本論文は、画像・動画を扱う離散拡散型マルチモーダル大規模言語モデル（discrete diffusion-based Multimodal Large Language Models、dMLLM）に、自己回帰型の視覚トークン枝刈りをそのまま移植しても期待通り高速化しない理由を実験的に分析する。

- **2025-10 · [Mixed-Precision Quantization for Language Models: Techniques and Prospects](2025-2510.16805-mixed-precision-quantization-for-language-models-techniques-and-prospect.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  量子化はモデル重み・活性・KVキャッシュの数値精度を下げてメモリ・帯域・演算費用を抑える。一方、平均2bitの一部方式ではPPLがFP16比55%以上悪化する。

- **2025-09 · [Efficient Pre-Training of LLMs via Topology-Aware Communication Alignment on More Than 9600 GPUs](2025-2509.15940-efficient-pre-training-of-llms-via-topology-aware-communication-alignmen.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  一般的なクラスタスケジューラが空きGPUを近い位置に詰めても、実際に頻繁に通信するDP/PPグループが別のスイッチ配下に分散すれば帯域競合と通信待ちが発生する。トレース駆動シミュレーションでは比較方式に対し通信グループの重み付き最大広がりを最大1.67倍改善し、実クラスタでは208 GPUで学習処理量5.7%、9600超GPUで10.6%改善した。

- **2025-11 · [CLaRa: Bridging Retrieval and Generation with Continuous Latent Reasoning](2025-2511.18659-clara-bridging-retrieval-and-generation-with-continuous-latent-reasoning.md)**  
  実装：[✓](https://github.com/apple/ml-clara) ・ リポジトリ内被引用：3  
  CLaRa（Continuous Latent Reasoning）は、文書を少数の連続値メモリトークンへ圧縮し、その表現を文書検索と生成の双方に用いる。Mistral-7Bで16倍圧縮したSCPは、4質問応答課題の通常検索条件において平均CEM 38.96%を記録し、PISCOの37.83%を上回る。

- **2025-07 · [Activation Steering for Chain-of-Thought Compression](2025-2507.04742-activation-steering-for-chain-of-thought-compression.md)**  
  実装：[✓](https://github.com/ArminAzizi98/ASC) ・ リポジトリ内被引用：3  
  冗長な推論と簡潔な推論の活性の平均差を操舵ベクトルとして中間層へ注入し、分布のずれを距離予算で抑えながら思考連鎖を最大六七・四三パーセント短縮し、正解率を保って二・七三倍速くした。

- **2025-05 · [$\mu$-MoE: Test-Time Pruning as Micro-Grained Mixture-of-Experts](2025-2505.18451-mu-moe-test-time-pruning-as-micro-grained-mixture-of-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  μ-MoEは、モデルをあらかじめ一度だけ枝刈りするのではなく、実際に与えられたプロンプトをその場の校正データとして使い、線形層の重みのうち重要なものだけを有効化する方式である。

- **2025-04 · [Hawkeye: Model Collaboration for Efficient Reasoning](2025-2504.00424-hawkeye-model-collaboration-for-efficient-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  Hawkeyeは、推論用の大規模言語モデルが長い思考連鎖（Chain-of-Thought; CoT）を出力し続けることによる生成遅延と課金額を削減する研究である。重要なのは、二段階のモデル連携を推論時だけでなく事後学習の報酬設計にも組み込んでいることである。

- **2025-04 · [AccLLM: Accelerating Long-Context LLM Inference Via Algorithm-Hardware Co-Design](2025-2505.03745-accllm-accelerating-long-context-llm-inference-via-algorithm-hardware-co.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  大規模言語モデル（LLM）を資源制約の強い端末向けFPGAに載せるため、圧縮アルゴリズムと演算器・データフローを同時に設計する。主要な評価ではLlama-2-7Bを12.1GBのFP16モデルから1.53GBへ縮小し、Xilinx Alveo U280 FPGA上で164 トークン/s、33W、4.96 トークン/Jを報告した。

- **2025-03 · [Key, Value, Compress: A Systematic Exploration of KV Cache Compression Techniques](2025-2503.11816-key-value-compress-a-systematic-exploration-of-kv-cache-compression-tech.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  長文脈の大規模言語モデルで問題になるキー・バリュー（KV）キャッシュの容量を減らす方式を、どの軸の冗長性を削るかという視点で整理する。したがって表4の2.87倍と1.86倍を並べて前者が後者より優れた方式と結論付けることはできない。

- **2025-02 · [ETS: Efficient Tree Search for Inference-Time Scaling](2025-2502.13575-ets-efficient-tree-search-for-inference-time-scaling.md)**  
  実装：[✓](https://github.com/SqueezeAILab/ETS) ・ リポジトリ内被引用：3  
  ETS（Efficient Tree Search）は、LLMの推論時演算量拡大（inference-time scaling）で用いる木探索の費用を、単なるモデル呼出回数ではなく分岐間の鍵・値キャッシュ（KV キャッシュ）共有量に基づいて最適化する方式である。

- **2025-11 · [Thinking with Drafts: Speculative Temporal Reasoning for Efficient Long Video Understanding](2025-2512.00805-thinking-with-drafts-speculative-temporal-reasoning-for-efficient-long-v.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  長い動画の質問応答では、最初に少数のフレームを見て全体を把握し、必要な時間区間を細かく調べる「フレームを見ながら考える」方式が使われる。原著の観測では、動画トークンに対する注意スコアの90%以上が 10^-3 未満で、密に読み込んだフレームには冗長な情報が多い。

- **2025-11 · [Beyond Fixed-Length Calibration for Post-Training Compression of LLMs](2025-572d81dfcf74-beyond-fixed-length-calibration-for-post-training-compression-of-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  圧縮用の較正データの長さが手法ごとに効き方が違うことを四モデル六手法で示し、正規化された隠れ状態では最初のトークンが後続と反対向きになる観測から、その状態だけ先頭の一部を使う較正で、追加費用なしに圧縮後の品質を概ね改善する方式。

- **2025-10 · [video-SALMONN S: Memory-Enhanced Streaming Audio-Visual LLM](2025-2510.11129-video-salmonn-s-memory-enhanced-streaming-audio-visual-llm.md)**  
  実装：[✓](https://github.com/bytedance/SALMONN/tree/video-salmonn-S) ・ リポジトリ内被引用：2  
  後者では将来の質問も動画長も未知であり、長時間の履歴を固定のGPUメモリ予算へ保持しなければならない。類似トークンをまとめるだけの方式は新しいフレームが来るたび古い細部を失い、数十分前に見た手順を問われる課題では精度が下がり得る。

- **2025-10 · [ARMOR: High-Performance Semi-Structured Pruning via Adaptive Matrix Factorization](2025-2510.05528-armor-high-performance-semi-structured-pruning-via-adaptive-matrix-facto.md)**  
  実装：[✓](https://github.com/LawrenceRLiu/ARMOR) ・ リポジトリ内被引用：2  
  一方、どの4要素からも2要素を消すという硬い制約は、同じ50%剪定率の非構造化剪定よりも言語モデルの品質を大きく悪化させやすい。ARMORは、この損失をマスク選択だけで解決するのではなく、疎行列の前後へ小さい学習可能な線形変換を配置して重み表現を変える方式である。

- **2025-09 · [Ultra-Fast Language Generation via Discrete Diffusion Divergence Instruct](2025-2509.25035-ultra-fast-language-generation-via-discrete-diffusion-divergence-instruc.md)**  
  実装：[✓](https://github.com/haoyangzheng-ai/didi-instruct) ・ リポジトリ内被引用：2  
  拡散言語モデルの全雑音水準の分布を教師へ一致させる蒸留で少数ステップ生成を実現し、16回の評価で1024回の教師のパープレキシティを上回った方式。

- **2025-09 · [SpikingBrain: Spiking Brain-inspired Large Models](2025-2509.05276-spikingbrain-spiking-brain-inspired-large-models.md)**  
  実装：[✓](https://github.com/BICLab/SpikingBrain-7B) ・ リポジトリ内被引用：2  
  SpikingBrainは、標準Transformerの長文脈計算・KVキャッシュ負荷と、非NVIDIA GPUでの大規模学習の難しさを同時に扱う研究である。成果は一つの高速注意機構カーネルにとどまらない。

- **2025-09 · [PATCH: Learnable Tile-level Hybrid Sparsity for LLMs](2025-2509.23410-patch-learnable-tile-level-hybrid-sparsity-for-llms.md)**  
  実装：[✓](https://github.com/Paramathic/patch) ・ リポジトリ内被引用：2  
  重みをタイル単位で密か2:4疎かを学習して選び、疎性率を0から50パーセントで連続制御するハイブリッド疎性PATCH。LLaMA-2 7Bで密比最大1.38倍の実測高速化とMaskLLM超えの精度。

- **2025-06 · [Parallel Continuous Chain-of-Thought with Jacobi Iteration](2025-2506.18582-parallel-continuous-chain-of-thought-with-jacobi-iteration.md)**  
  実装：[✓](https://github.com/whyNLP/PCCoT) ・ リポジトリ内被引用：2  
  連続思考の逐次依存をヤコビ反復で並列化し、数学推論の正解率を保ったまま学習と推論の時間をほぼ半減させる。

- **2025-05 · [Semantic Caching of Contextual Summaries for Efficient Question-Answering with Language Models](2025-2505.11271-semantic-caching-of-contextual-summaries-for-efficient-question-answerin.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  本研究は、文書検索とLLM呼出しを組み合わせる質問応答で、回答そのものでもKVキャッシュでもなく、質問に合わせて生成した中間の文書要約をキャッシュする方法を扱う。文書を検索した後に要約し、その要約と質問を使って回答する複数段階のワークフローでは、同じ文書に対して似た質問が繰り返される。

- **2025-05 · [Prolonged Reasoning Is Not All You Need: Certainty-Based Adaptive Routing for Efficient LLM/MLLM Reasoning](2025-2505.15154-prolonged-reasoning-is-not-all-you-need-certainty-based-adaptive-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  まず短い答えを出してその困惑度を正誤二つの分布と比べ、危うい問だけ長い推論へ回す振り分けで、全推論より正解率を上げながらトークンを大幅に減らした。

- **2025-03 · [Towards Extreme Pruning of LLMs with Plug-and-Play Mixed Sparsity](2025-2503.11164-towards-extreme-pruning-of-llms-with-plug-and-play-mixed-sparsity.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  大規模言語モデルの重みを学習後に削減する際、既存のMagnitude、SparseGPT、Wandaなどは、重みを残す重要度の測り方を工夫してきた。その後、各層の疎度を遺伝的アルゴリズムに似た進化的探索で調整する。代表例はLLaMA-13B、WikiText、75%削減、ブロック幅M=4のWandaである。

- **2025-03 · [StreamMind: Unlocking Full Frame Rate Streaming Video Dialogue through Event-Gated Cognition](2025-2503.06220-streammind-unlocking-full-frame-rate-streaming-video-dialogue-through-ev.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  状態空間モデルによる定数費用の知覚と、言語モデルの浅い層を転用した認知ゲートで、毎秒100フレームのストリーミング動画へ能動的に応答する枠組み。

- **2025-02 · [SPECTRE: An FFT-Based Efficient Drop-In Replacement to Self-Attention for Long Contexts](2025-2502.18394-spectre-an-fft-based-efficient-drop-in-replacement-to-self-attention-for.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  SPECTREは、系列長$n$に対して二乗で増える通常の自己注意（Self-注意機構）を、実数高速フーリエ変換（Real Fast Fourier Transform、RFFT）、内容適応の周波数ゲート、逆変換の組合せで置き換える方式である。

- **2025-02 · [Prompt-based Depth Pruning of Large Language Models](2025-2502.04348-prompt-based-depth-pruning-of-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  ブロックの重要度が課題で違うことに着目し、候補の省略集合を課題尤度で作りプロンプトごとに軽量ルーターが選ぶ動的深さ枝刈りPuDDingで、約22パーセント削減でも静的枝刈りより正解率を上げつつ1.2倍台の生成高速化を得る。

- **2025-02 · [LLM Inference Acceleration via Efficient Operation Fusion](2025-2502.17728-llm-inference-acceleration-via-efficient-operation-fusion.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  レイヤー正規化とソフトマックスの分母集約を、後続の線形層との可換性を使って行列積の後へ繰り延べ、集約をSIMD側で並行実行して遅延を隠す代数等価な演算融合を提案し、自社アクセラレータCorsairでLlama 2/3の推論遅延を約20%削減したと報告する無損失の最適化。

- **2025-01 · [A Proximal Operator for Inducing 2:4-Sparsity](2025-2501.18015-a-proximal-operator-for-inducing-2-4-sparsity.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  GPUの2:4疎行列演算では4重み中2つをゼロにすることで、通常の非構造化疎性よりも実行時に利用しやすい規則性が得られる。

- **2025-11 · [T-SAR: A Full-Stack Co-design for CPU-Only Ternary LLM Inference via In-Place SIMD ALU Reorganization](2025-2511.13676-t-sar-a-full-stack-co-design-for-cpu-only-ternary-llm-inference-via-in-p.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  T-SARは、重みを−1、0、+1の三値に制約した大規模言語モデル（LLM）を、専用の大きな行列演算器なしにCPUで高速実行するための、アルゴリズム・命令セット・マイクロアーキテクチャ・ソフトウェアの協調設計である。

- **2025-11 · [NeuroPath: Neurobiology-Inspired Path Tracking and Reflection for Semantically Coherent Retrieval](2025-2511.14096-neuropath-neurobiology-inspired-path-tracking-and-reflection-for-semanti.md)**  
  実装：[✓](https://github.com/KennyCaty/NeuroPath) ・ リポジトリ内被引用：1  
  知識グラフ（Knowledge Graph; KG）上の隣接性だけを重視する既存方式は、質問に答えるための関係の向きや意味を無視して文書を集める場合がある。原著の多段質問応答3データセットでは、主要なグラフ検索方式に比べて平均Recall@2を16.3%、Recall@5を13.5%改善したと報告する。

- **2025-11 · [Mitigating Sequential Dependencies: A Survey of Algorithms and Systems for Generation-Refinement Frameworks in Autoregressive Models](2025-d5b03c1b33e0-mitigating-sequential-dependencies-a-survey-of-algorithms-and-systems-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  対象は、草案トークンを安く先読みし、より高品質なターゲットモデルで検証する投機的復号だけでなく、複数位置を仮置きして反復修正するJacobi型方式や、検索・n-gramによる草案再利用まで含む。付録A1では公開実装を用い、単一NVIDIA A100 80GB、バッチ1、貪欲復号という条件で11方式を六課題比較した。

- **2025-11 · [DeCoRL: Decoupling Reasoning Chains via Parallel Sub-Step Generation and Cascaded Reinforcement for Interpretable and Scalable RLHF](2025-2511.19097-decorl-decoupling-reasoning-chains-via-parallel-sub-step-generation-and-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  DeCoRLは、長い推論手順を単一の大規模言語モデル（LLM）が順番に生成する代わりに、役割の異なる小さな推論モジュールへ分解して同時に実行し、出力を統合する枠組みである。著者はNVIDIA A100を使った10段階の推論問題で、逐次実行1,202ミリ秒に対してDeCoRLが316ミリ秒となり、約3.8倍高速化したと報告する。

- **2025-10 · [Untangling Component Imbalance in Hybrid Linear Attention Conversion Methods](2025-2510.05901-untangling-component-imbalance-in-hybrid-linear-attention-conversion-met.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  事前学習済みTransformerの通常のsoftmax注意を線形注意（LA）へ置き換えれば、過去のキーと値を全トークン分保持せず、一定サイズの再帰状態へ集約できる。しかし注意機構を変更しただけでは元モデルの精度が下がるため、注意転写と追加微調整を行う。

- **2025-10 · [Scaling Laws Meet Model Architecture: Toward Inference-Efficient LLMs](2025-2510.18245-scaling-laws-meet-model-architecture-toward-inference-efficient-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデルの設計では、パラメータ数と学習トークン数を指定して学習損失を下げる方法が重視されてきた。

- **2025-10 · [Reasoning in the Dark: Interleaved Vision-Text Reasoning in Latent Space](2025-2510.12603-reasoning-in-the-dark-interleaved-vision-text-reasoning-in-latent-space.md)**  
  実装：[✓](https://github.com/ModalityDance/IVT-LR) ・ リポジトリ内被引用：1  
  視覚言語モデル（vision-language モデル; VLM）が図表や画像に基づいて多段階の推論をするとき、従来の思考の連鎖（chain of thought; CoT）方式は中間推論を自然言語トークンとして逐次生成する。

- **2025-10 · [Layer as Puzzle Pieces: Compressing Large Language Models through Layer Concatenation](2025-2510.15304-layer-as-puzzle-pieces-compressing-large-language-models-through-layer-c.md)**  
  実装：[✓](https://github.com/MPI-Lab/CoMe) ・ リポジトリ内被引用：1  
  隣接層の重要なチャネルをチャネル感度で選び出して連結し、1層に再構成するCoMeにより、層削除と重みの線形加算の両方の情報損失を避け、圧縮時の層対応を使った階層蒸留でLLaMA-2-7Bの30パーセント圧縮後も保持率82.98パーセントまで回復させた層圧縮の研究。

- **2025-10 · [Key and Value Weights Are Probably All You Need: On the Necessity of the Query, Key, Value weight Triplet in Self-Attention Transformers](2025-2510.23912-key-and-value-weights-are-probably-all-you-need-on-the-necessity-of-the-.md)**  
  実装：[✓](https://github.com/MarkoKarbevski/Wqkv_necessity) ・ リポジトリ内被引用：1  
  各射影が表現力に独立して必要なのかは、モデルのパラメータ数・学習時の最適化・推論時のメモリ使用量を考えるうえで重要である。理論の出発点は、注意機構が元の入力Xを直接見るのではなく、XWQ、XWK、XWVという射影後の値に依存する点である。これは非埋込パラメータ約8.3%削減であり、総モデルパラメータが25%減るわけではない。

- **2025-10 · [Direct Multi-Token Decoding](2025-2510.11958-direct-multi-token-decoding.md)**  
  実装：[✓](https://github.com/luoxuan-cs/Direct-Multitoken-Decoding) ・ リポジトリ内被引用：1  
  低バッチでは重みをGPUメモリから読み出す時間が支配的になりやすく、各層を毎トークン通ることが遅延の主要因になる。以下の数値はすべて原著の表を照合したものであり、未測定の大規模サービング性能や他の投機復号方式との優劣は主張しない。

- **2025-10 · [Activation Quantization of Vision Encoders Needs Prefixing Registers](2025-2510.04547-activation-quantization-of-vision-encoders-needs-prefixing-registers.md)**  
  実装：[✓](https://github.com/spbob0418/RegCache) ・ リポジトリ内被引用：1  
  しかし、CLIPやSigLIPなどの視覚Transformerでは、一部トークンの活性値が他より極端に大きくなり、活性値の量子化範囲を押し広げて精度を損なう。

- **2025-09 · [Toward Robust and Efficient ML-Based GPU Caching for Modern Inference](2025-2509.20979-toward-robust-and-efficient-ml-based-gpu-caching-for-modern-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  予測を盲信せず、正確なら最適へ近づき外れればLRUへ戻る保証を持つ学習拡張LRUと、そのGPUキャッシュ実装LCRで、尾遅延とスループットを改善しながら予測劣化への頑健さを示す研究。

- **2025-09 · [PipelineRL: Faster On-policy Reinforcement Learning for Long Sequence Generation](2025-2509.19128-pipelinerl-faster-on-policy-reinforcement-learning-for-long-sequence-gen.md)**  
  実装：[✓](https://github.com/ServiceNow/pipelinerl) ・ リポジトリ内被引用：1  
  PipelineRLは、大規模言語モデルの長文推論を強化学習で訓練するときに、系列生成器と訓練器の並行実行および生成途中の重み更新（in-flight 重み update）を組み合わせるシステムである。

- **2025-09 · [CompLLM: Compression for Long Context Q&A](2025-2509.19228-compllm-compression-for-long-context-q-a.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  CompLLMは、LLMへ入力する長い文書を、短いセグメントごとに独立して連続ベクトルへ圧縮する方式である。標準設定は最大20入力トークンを10個のCEへ変換する2倍圧縮である。

- **2025-08 · [Z-Pruner: Post-Training Pruning of Large Language Models for Efficiency without Retraining](2025-2508.15828-z-pruner-post-training-pruning-of-large-language-models-for-efficiency-w.md)**  
  実装：[✓](https://github.com/sazzadadib/Z-Pruner) ・ リポジトリ内被引用：1  
  重みの行・列正規化から作るゼットスコアの三乗とモデル族別の活性値スケーリングで重要度を決め、再学習も重み更新もなしに50%枝刈りして、大規模モデルで最低のパープレキシティと最速級の枝刈り時間を両立する学習後枝刈り。

- **2025-08 · [Not All Errors Are Created Equal: ASCoT Addresses Late-Stage Fragility in Efficient LLM Reasoning](2025-2508.05282-not-all-errors-are-created-equal-ascot-addresses-late-stage-fragility-in.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  誤り注入の実験で終盤の段の誤りほど最終答えを壊すことを示し、意味の薄いトークンの間引きと、位置で重み付けした危険度が高い段だけの二経路修正を組み合わせ、八十億規模モデルで生成トークンを約二割減らしつつ正解率の低下を一・一ポイントに抑えたと報告した。

- **2025-08 · [GM-Skip: Metric-Guided Transformer Block Skipping for Efficient Vision-Language Models](2025-2508.18227-gm-skip-metric-guided-transformer-block-skipping-for-efficient-vision-la.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  視覚言語モデルのTransformerブロックを、タスク指標を実測しながら落としても痛くないものから貪欲にスキップし、逆順削除で初期層を守ることで、分類精度を保ちながら推論遅延を下げるフレームワーク。

- **2025-08 · [DTRNet: Dynamic Token Routing Network to Reduce Quadratic Costs in Transformers](2025-2509.00925-dtrnet-dynamic-token-routing-network-to-reduce-quadratic-costs-in-transf.md)**  
  実装：[✓](https://github.com/Aman26Sharma/DTRNet) ・ リポジトリ内被引用：1  
  各層で学習済みルーティングがトークンごとにfull 注意機構経路と軽量な自己投影経路を選ぶ。FineWeb-Eduで事前学習した360Mモデルでは、DTRNet-BiLayerがdense SmolLM比FLOPs 0.84倍で平均ゼロショット精度44.36%、denseの44.23%とほぼ同等だった。

- **2025-07 · [RAT: Bridging RNN Efficiency and Attention Accuracy via Chunk-based Sequence Modeling](2025-2507.04416-rat-bridging-rnn-efficiency-and-attention-accuracy-via-chunk-based-seque.md)**  
  実装：[✓](https://github.com/CLAIRE-Labo/RAT) ・ リポジトリ内被引用：1  
  全トークンに対するソフトマックス注意（softmax 注意機構）は、過去の任意の位置を直接参照できる一方、長文で注意演算量と鍵・値キャッシュ（KV キャッシュ）が増える。また、3072トークンの入力から1024トークンを生成する最大生成処理量では、1.3Bモデルで通常注意3152に対しRAT 31170トークン/秒、約10.2倍である。

- **2025-07 · [Investigating Structural Pruning and Recovery Techniques for Compressing Multimodal Large Language Models: An Empirical Study](2025-2507.20749-investigating-structural-pruning-and-recovery-techniques-for-compressing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  言語バックボーンの重みと演算が大きな割合を占めるため、モデルの一部を実際に削除できれば、量子化とは別の経路でメモリ・計算負担を下げられる。15%削減・回復なしのLLaVAでは幅方向の平均指標57.79、層方向46.09であり、元モデル62.28からの低下は幅方向の方が小さい。

- **2025-07 · [IMPACT: Importance-Aware Activation Space Reconstruction](2025-2507.03828-impact-importance-aware-activation-space-reconstruction.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  活性値の次元ごとの重要度を勾配で測り、重要度で重み付けした活性値共分散行列の固有ベクトルを再構成基底とする低ランク圧縮で、従来法より最大48.6パーセント大きなサイズ削減を同精度で達成し、同精度ではスループット最大35パーセント増とメモリ最大41パーセント減を示した研究。

- **2025-06 · [SparseSSM: Efficient Selective Structured State Space Models Can Be Pruned in One-Shot](2025-2506.09613-sparsessm-efficient-selective-structured-state-space-models-can-be-prune.md)**  
  実装：[✓](https://github.com/CFinTech/SparseSSM) ・ リポジトリ内被引用：1  
  入力依存の離散化係数と、系列の全時刻で使い回す状態遷移パラメータが組み合わさるため、通常の線形層向け剪定手法を状態遷移重みにそのまま適用すると、削除してよい状態を見誤りやすい。正式版の要旨は、SSM重み50%を微調整なしで削除した際の品質低下が「限定的」であると説明する。

- **2025-06 · [ReCUT: Balancing Reasoning Length and Accuracy in LLMs via Stepwise Trails and Preference Optimization](2025-2506.10822-recut-balancing-reasoning-length-and-accuracy-in-llms-via-stepwise-trail.md)**  
  実装：[✓](https://github.com/NEUIR/ReCUT) ・ リポジトリ内被引用：1  
  段階ごとに長い続きと短い続きを試し報酬で一歩ずつ選ぶ探索で選好データを作り、正確さ重視と短さ重視の二モデルをパラメータ補間で統合することで、数学推論の平均トークンを約四二パーセント減らしながら正解率を四三・九から四五・七パーセントへ上げた。

- **2025-06 · [Latent Multi-Head Attention for Small Language Models](2025-2506.09342-latent-multi-head-attention-for-small-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本研究は、大規模LLMで利用される多頭潜在注意（Multi-head Latent 注意機構、MLA）の低ランクKV表現が、数千万〜数億パラメータ規模の小型GPTでも有効かを調べる。

- **2025-06 · [Graph-KV: Breaking Sequence via Injecting Structural Biases into Large Language Models](2025-2506.07334-graph-kv-breaking-sequence-via-injecting-structural-biases-into-large-la.md)**  
  実装：[✓](https://github.com/Graph-COM/GraphKV) ・ リポジトリ内被引用：1  
  テキスト片のKVをグラフの辺に沿ってだけ結び位置符号も出典と対象で分けて共有することで、平坦化の位置バイアスと二次計算を避け多段推論で逐次符号化を上回る。

- **2025-06 · [Efficient Reasoning Through Suppression of Self-Affirmation Reflections in Large Reasoning Models](2025-2506.12353-efficient-reasoning-through-suppression-of-self-affirmation-reflections-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  推論特化言語モデルが長い思考過程を生成する際、誤りを見つけて解き直す有用な反省と、既に正しい途中計算を繰り返し肯定するだけの冗長な反省が混在する。本研究は後者を自己確認型反省と呼び、反省文を開始する語の生成確率に偏りがあることを利用して、必要な推論をなるべく残しながら冗長な出力を減らす。ただし平均正解率は64.9%から64.2%へ0.7ポイント下がった。

- **2025-05 · [Hierarchical Document Refinement for Long-context Retrieval-augmented Generation](2025-2505.10413-hierarchical-document-refinement-for-long-context-retrieval-augmented-ge.md)**  
  実装：[✓](https://github.com/ignorejjj/LongRefiner) ・ リポジトリ内被引用：1  
  検索文書を階層木へ起こし直し、問いの情報範囲に応じた局所得点と全域得点で節点を選ぶ精錬器で、全文投入より約十分の一のトークンで七課題すべて最高精度を達成した。

- **2025-05 · [DINGO: Constrained Inference for Diffusion LLMs](2025-2505.23061-dingo-constrained-inference-for-diffusion-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  正規表現のオートマトン上で動的計画法を回し、ブロック並列予測でも分布を歪めずに確率最大の制約適合出力を厳密に求める、拡散言語モデル向けの制約付きデコード。

- **2025-04 · [Window Token Concatenation for Efficient Visual Large Language Models](2025-2504.04024-window-token-concatenation-for-efficient-visual-large-language-models.md)**  
  実装：[✓](https://github.com/JackYFL/WiCo) ・ リポジトリ内被引用：1  
  視覚エンコーダーの末尾層を微調整してウィンドウ内特徴を平滑化し、2次元ウィンドウ内の隣接視覚トークンを連結して4分の1へ減らすプロジェクターWiCoと、LLM後段層でトークンを補間復元して細粒度タスクの劣化を抑えるWiCo+を提案した研究。

- **2025-04 · [Thanos: A Block-wise Pruning Algorithm for Efficient Large Language Model Compression](2025-2504.05346-thanos-a-block-wise-pruning-algorithm-for-efficient-large-language-model.md)**  
  実装：[✓](https://github.com/vectozavr/thanos) ・ リポジトリ内被引用：1  
  Thanosは、大規模言語モデル（LLM）の学習済み重みを、少数の校正データだけで剪定するpost-学習 枝刈り手法である。原著Table 2では、LLaMA-3 8Bを30%構造化剪定したWikiText-2困惑度（PPL）がSparseGPTの82.19、Thanos（外れ値行保護α=0.1）の36.61となる。

- **2025-04 · [Empower Vision Applications with LoRA LMM](2025-2411.00915-empower-vision-applications-with-lora-lmm.md)**  
  実装：[✓](https://github.com/mi150/VaLoRA) ・ リポジトリ内被引用：1  
  オンラインでは入力形状に合うタイル構成を事前探索したATMMカーネルを使い、LoRAを基盤重みへ統合するモード、統合しないモード、両者を混ぜるdeLoRAモードを負荷に応じて選ぶ。

- **2025-04 · [An Empirical Study on Prompt Compression for Large Language Models](2025-2505.00019-an-empirical-study-on-prompt-compression-for-large-language-models.md)**  
  実装：[✓](https://github.com/3DAgentWorld/Toolkit-for-Prompt-Compression) ・ リポジトリ内被引用：1  
  本論文は、長いプロンプトを事前に短縮してLLMへ渡すテキスト入力の圧縮について、6種類の方式を同一の評価枠組みで比較する実証研究である。また、単一A6000 GPU上の圧縮器処理時間はSCRLの67ms/入力からKiSの2410ms/入力まで大きく異なる。

- **2025-03 · [Union of Experts: Adapting Hierarchical Routing to Equivalently Decomposed Transformer](2025-2503.02495-union-of-experts-adapting-hierarchical-routing-to-equivalently-decompose.md)**  
  実装：[✓](https://github.com/YujiaoYang-work/UoE) ・ リポジトリ内被引用：1  
  本論文は、Mixture-of-Experts（MoE）の疎活性化をMLPブロックだけに限定せず、注意ブロックとMLPブロックをともに、機能的に等価な部分計算から構成される専門家集合へ分解するUnion-of-Experts（UoE）を提案する。

- **2025-03 · [STADE: Standard Deviation as a Pruning Metric](2025-2503.22451-stade-standard-deviation-as-a-pruning-metric.md)**  
  実装：[✓](https://github.com/Coello-dev/STADE) ・ リポジトリ内被引用：1  
  枝刈り問題の理論解析から、入力が中心化されていない層ではWandaではなく活性の標準偏差を使う指標が最適になることを導いた研究。層ごとに指標を切り替えるSTADE-Wまで含め、理論の予測どおりに優劣が入れ替わることを実測で確認した。

- **2025-03 · [Cost-Optimal Grouped-Query Attention for Long-Context Modeling](2025-2503.09579-cost-optimal-grouped-query-attention-for-long-context-modeling.md)**  
  実装：[✓](https://github.com/THUNLP/cost-optimal-gqa) ・ リポジトリ内被引用：1  
  Grouped-Query 注意機構（GQA）は複数のquery headでKey/Valueを共有し、通常のMulti-Head 注意機構（MHA）よりKVキャッシュ容量と読み出し量を抑える。

- **2025-02 · [M2R2: Mixture of Multi-Rate Residuals for Efficient Transformer Inference](2025-2502.02040-m2r2-mixture-of-multi-rate-residuals-for-efficient-transformer-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  M2R2は、言語モデルの中間残差表現が最終層の残差表現へどれだけ早く近づくかを、追加の軽量な計算経路で制御する方式である。

- **2025-02 · [LIFT: A Novel Framework for Enhancing Long-Context Understanding of LLMs via Long Input Fine-Tuning](2025-2502.14644-lift-a-novel-framework-for-enhancing-long-context-understanding-of-llms-.md)**  
  実装：[✓](https://github.com/MuLabPKU/LIFT) ・ リポジトリ内被引用：1  
  LIFT（Long Input 微調整）は、長い文書をそのままLLMの入力コンテキストへ入れる代わりに、文書から生成した質問・回答（QA）で短文脈モデルをテスト時に微調整し、文書の情報をモデルのパラメータへ内在化させる方式である。

- **2025-02 · [DeltaLLM: Compress LLMs with Low-Rank Deltas between Shared Weights](2025-2501.18596-deltallm-compress-llms-with-low-rank-deltas-between-shared-weights.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  提案は単なる重みの複製ではない。Phi-3.5由来のDeltaPhi 3.35Bは3.8Bから約12%のパラメータ削減で、原著Table 1の5課題平均が0.66から0.59となる。

- **2025-11 · [Word Salad Chopper: Reasoning Models Waste A Ton Of Decoding Budget On Useless Repetitions, Self-Knowingly](2025-2511.00536-word-salad-chopper-reasoning-models-waste-a-ton-of-decoding-budget-on-us.md)**  
  実装：[✓](https://github.com/wenyaxie023/WordSaladChopper) ・ リポジトリ内被引用：0  
  推論モデルの無意味な反復を区切りトークンの隠れ状態で検出して切り取り再生成させる軽量部品で、生成長を最大57パーセント削り正解率をほぼ保つ。

- **2025-11 · [TwIST: Rigging the Lottery in Transformers with Independent Subnetwork Training](2025-2511.03983-twist-rigging-the-lottery-in-transformers-with-independent-subnetwork-tr.md)**  
  実装：[✓](https://anonymous.4open.science/r/twist2-373F) ・ リポジトリ内被引用：0  
  部分ネットワークの並行学習と定期的な集約・再抽選により、学習後の回復処理なしで取り出せる構造化枝刈り済みモデルを学習過程で作る分散学習の枠組みで、高い疎率で学習後枝刈りを上回った研究。

- **2025-11 · [Thinking While Speaking: Inference-Time Knowledge Transfer for Responsive and Intelligent Conversational Voice Agents](2025-2511.07397-thinking-while-speaking-inference-time-knowledge-transfer-for-responsive.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末の360Mモデルが即座に会話を進めながらクラウドの大規模モデルから流れ込む知識を途中で織り込むConvFillで、正解率を10パーセントから46から52パーセントへ上げつつ応答開始を200ミリ秒未満に保つ。

- **2025-11 · [Test-Time Temporal Sampling for Efficient MLLM Video Understanding](2025-2511.17945-test-time-temporal-sampling-for-efficient-mllm-video-understanding.md)**  
  実装：[✓](https://github.com/kaibinwang3/T3S) ・ リポジトリ内被引用：0  
  一方、学習済みフレーム選択器や動画専用圧縮器は追加学習と前処理が必要で、既存のMLLMへそのまま組み込めるとは限らない。Qwen2.5-VL-7BでLongVideoBenchの正答率は59.2%から62.3%へ3.1ポイント改善し、論文が測る最初のトークンまでの遅延は2.04倍高速化した。

- **2025-11 · [Streaming Tensor Programs: A Streaming Abstraction for Dynamic Parallelism](2025-2511.07776-streaming-tensor-programs-a-streaming-abstraction-for-dynamic-parallelis.md)**  
  実装：[✓](https://github.com/stanford-ppl/step_artifact) ・ リポジトリ内被引用：0  
  SDAは演算器とメモリをチップ上へ分散配置し、演算間を先入先出のストリームで接続する。著者はMixtral-8x7B、Qwen3-30B-A3BのMoE層と全モデル、AzureLLMInferenceDataset由来のKV長分布を用い、サイクル近似シミュレータで評価する。

- **2025-11 · [Revisiting Pruning vs Quantization for Small Language Models](2025-863c1324e5f3-revisiting-pruning-vs-quantization-for-small-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  小型言語モデル6種で枝刈り2方式と量子化2方式を7言語・7課題で統一比較し、同等圧縮率では量子化が忠実度と精度を大きく保ち、大規模モデルでの枝刈りの優劣関係が小型モデルでは逆転することを示した分析研究。

- **2025-11 · [Re-FORC: Adaptive Reward Prediction for Efficient Chain-of-Thought Reasoning](2025-2511.02130-re-forc-adaptive-reward-prediction-for-efficient-chain-of-thought-reason.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  追加の思考トークンに対する期待報酬の曲線を予測し、ギッティンズ指標で早期停止、モデル選択、テスト時スケーリングを統一的に決める計算配分手法。

- **2025-11 · [LAPA: Log-Domain Prediction-Driven Dynamic Sparsity Accelerator for Transformer Model](2025-2512.07855-lapa-log-domain-prediction-driven-dynamic-sparsity-accelerator-for-trans.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  QKV生成と注意の両段階へ動的スパース化を広げるクロスステージスパース化を、片側だけ対数変換するALOC、多ラウンド段階絞り込みのMRSA、ソート不要のDDFで低電力に予測し、28nm実装でSpatten比3.52倍のエネルギー効率を達成したTransformerアクセラレータの協調設計。

- **2025-11 · [HookMoE: A learnable performance compensation strategy of Mixture-of-Experts for LLM inference acceleration](2025-6f8f63691373-hookmoe-a-learnable-performance-compensation-strategy-of-mixture-of-expe.md)**  
  実装：[✓](https://github.com/KerwinKai/HookMoE) ・ リポジトリ内被引用：0  
  MoEの活性化エキスパートを半分以下へ減らす代わりに、感度の高い1層へ小さな学習可能モジュールを挿入して表現のずれを補い、512件の較正だけで精度低下の大半を回復させる事後補償の枠組み。

- **2025-11 · [Focused Chain-of-Thought: Efficient LLM Reasoning via Structured Input Information](2025-2511.22176-focused-chain-of-thought-efficient-llm-reasoning-via-structured-input-in.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  質問の事実だけを構造化コンテキストへ抽出してから解かせることで、精度を保ったまま推論の生成トークンを2から3倍減らす、学習不要の入力側プロンプト手法。

- **2025-11 · [FISTAPruner: Layer-wise Post-training Pruning for Large Language Models](2025-d3680518ecb7-fistapruner-layer-wise-post-training-pruning-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  枝刈りをL1正則化つき凸最適化として定式化しFISTAで解く学習なし枝刈り法で、層内の累積誤差の打ち消しと層単位の並列処理を備え、LLaMA-3-70Bを50パーセント疎にしてもゼロショット性能の98.6パーセントを保持する。

- **2025-11 · [DeepCoT: Deep Continual Transformers for Real-Time Inference on Data Streams](2025-2511.17693-deepcot-deep-continual-transformers-for-real-time-inference-on-data-stre.md)**  
  実装：[✓](https://github.com/Atamarado/deepcot) ・ リポジトリ内被引用：0  
  DeepCoT（Deep Continual Transformer）は、映像・音声・テキストのストリームを移動窓で逐次処理する際、深いTransformerエンコーダで繰り返される過去トークンの計算を減らす方式である。原著のオンライン行動検出では通常のTransformerに対して23.65倍の相対実行速度、音楽分類では37.24倍を報告する。

- **2025-11 · [Decoupled Multi-Predictor Optimization for Inference-Efficient Model Tuning](2025-2511.03245-decoupled-multi-predictor-optimization-for-inference-efficient-model-tun.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  早期終了の浅い層で衝突する基礎特徴と識別特徴を、バイパスモジュールと高次統計の予測器、二相の損失重みで分離し、約30パーセントの計算量で70パーセントを使う先行方式に並ぶ精度を出す微調整法。

- **2025-11 · [Concept than Document: Context Compression via AMR-based Conceptual Entropy](2025-2511.18832-concept-than-document-context-compression-via-amr-based-conceptual-entro.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検索文書をAMRグラフ化し、概念エントロピーとt検定で重要な概念だけを残して文脈を約50%に圧縮することで、PopQAで全バックボーンのAUCをバニラより改善した、意味構造を使うRAG文脈圧縮の研究。

- **2025-11 · [BudgetMem: Training-Free Selective Memory for Cost-Efficient Long-Context Processing in Language Models](2025-2511.04919-budgetmem-training-free-selective-memory-for-cost-efficient-long-context.md)**  
  実装：[✓](https://github.com/Chandra-Alla/BudgetMem-paper) ・ リポジトリ内被引用：0  
  大規模言語モデル（Large Language モデル; LLM）の長文脈処理では、全入力をモデルへ投入すると注意計算・メモリ・料金が増える。トークン単位の圧縮器では、語句が断片的に残ることで検索に必要な語順や句のまとまりが失われる場合がある。既定の保持比率は30%であり、残した断片をBM25検索索引に格納する。

- **2025-11 · [Behavior-Equivalent Token: Single-Token Replacement for Long Prompts in LLMs](2025-2511.23271-behavior-equivalent-token-single-token-replacement-for-long-prompts-in-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長いシステムプロンプトの内容を再構成学習で埋め込み、フルプロンプト付きモデルの出力分布を知識蒸留して振る舞いまで写した特殊トークン1個でプロンプトを置き換えることで、性能のおおむね98%を保ったままプリフィルをほぼ消し、TTFTを最大59%短縮するプロンプト圧縮。

- **2025-11 · [Automatic Pruning Discovery for Large Language Models](2025-2511.15390-automatic-pruning-discovery-for-large-language-models.md)**  
  実装：[✓](https://anonymous.4open.science/r/AutoPrune) ・ リポジトリ内被引用：0  
  LLM自身にグラフ駆動の思考連鎖で枝刈り式を発見させ、重み分布の歪度で層ごとの削り方を変える配分と組み合わせることで、60パーセント枝刈りでもLLaMA-1 13BのパープレキシティをWandaの8.56から7.63へ改善した自動枝刈り設計。

- **2025-10 · [Value-State Gated Attention for Mitigating Extreme-Token Phenomena in Transformers](2025-2510.09017-value-state-gated-attention-for-mitigating-extreme-token-phenomena-in-tr.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  アテンションシンクと値状態ドレインを生む相互強化サイクルを、値ベクトル自身から計算するゲートで勾配経路ごと断ち、活性値外れ値と量子化劣化を抑える注意機構の改変。

- **2025-10 · [STaMP: Sequence Transformation and Mixed Precision for Low-Precision Activation Quantization](2025-2510.26771-stamp-sequence-transformation-and-mixed-precision-for-low-precision-acti.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  STaMP（Sequence Transformation and Mixed Precision）は、低ビット量子化の前に活性行列を系列方向へ直交変換し、情報が集中した少数の変換後トークンだけを8ビット、残りを4ビットで表現する方式である。

- **2025-10 · [Rewiring Experts on the Fly: Continuous Rerouting for Better Online Adaptation in Mixture-of-Expert models](2025-2510.14853-rewiring-experts-on-the-fly-continuous-rerouting-for-better-online-adapt.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  専門家混合モデルのルータを、外部データなしで生成中の文脈そのものを使って繰り返し直し、コード生成で最大6.7ポイントの改善を外部参照を使う従来法より少ない計算で得るテスト時再ルーティング。

- **2025-10 · [ReSSFormer: A Recursive Sparse Structured Transformer for Scalable and Long-Context Reasoning](2025-2510.01585-ressformer-a-recursive-sparse-structured-transformer-for-scalable-and-lo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単一ブロックの再帰＋階層メモリ、スパース注意と専門家ルーティング、位置符号化なしの構造誘導を組み合わせたトランスフォーマーで、同等計算量のまま長文脈精度と構造汎化を上げるアーキテクチャ提案。

- **2025-10 · [MossNet: Mixture of State-Space Experts is a Multi-Head Attention](2025-2510.26182-mossnet-mixture-of-state-space-experts-is-a-multi-head-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数の状態空間専門家の混合が線形化したmulti-head 注意機構の形に展開できることを示し、従来の単一状態のSSMより表現力を高める。8x200M+モデルは2.8兆トークン学習後、top-2（活性477M）で7課題平均53.5%、Qwen2.5-0.5Bの47.7%を上回るが、学習トークン数・モデル構造が異なる。

- **2025-10 · [From Local to Global: Revisiting Structured Pruning Paradigms for Large Language Models](2025-2510.18030-from-local-to-global-revisiting-structured-pruning-paradigms-for-large-l.md)**  
  実装：[✓](https://github.com/uncc-efficient-ai/GISP) ・ リポジトリ内被引用：0  
  モデル全体の損失で測った重要度を注意ヘッドとMLPチャネルへ集約し、反復的に少しずつ削る大域的構造化枝刈りGISPにより、枝刈り率40〜50パーセントでもパープレキシティ崩壊を避け、タスク校正を下流精度へ直接結び付けられることを示した研究。

- **2025-10 · [Explore Briefly, Then Decide: Mitigating LLM Overthinking via Cumulative Entropy Regulation](2025-2510.02249-explore-briefly-then-decide-mitigating-llm-overthinking-via-cumulative-e.md)**  
  実装：[✓](https://github.com/AusertDream/CumulativeEntropyRegulation) ・ リポジトリ内被引用：0  
  トークンエントロピーの累積平均TECAで推論過程の探索量を測り、正解時にTECAが低い応答へ報酬を与えるCERと分節報酬機構をGRPOへ組み込み、考えすぎによる出力トークンの浪費を難易度適応的に抑える学習手法を提案した研究。

- **2025-10 · [Exemplar-Derived Soft Prompts for Efficient and Effective Domain Adaptation](2025-2510.05363-exemplar-derived-soft-prompts-for-efficient-and-effective-domain-adaptat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案法MHA-ESPは、質問に関連する例示を検索し、質問と例示の埋め込みを多頭注意で集約して、基盤モデルの埋め込み次元に揃えた少数の仮想トークンを作る。原著がいう最大約10倍の計算量削減は入力例示のトークン処理に関する演算量比較であり、実際の生成速度が常に10倍になるという意味ではない。

- **2025-10 · [Don't Run with Scissors: Pruning Breaks VLA Models but They Can Be Recovered](2025-2510.08464-don-t-run-with-scissors-pruning-breaks-vla-models-but-they-can-be-recove.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、2:4構造化剪定をVLAへ適用すると、一般的な言語モデルよりはるかに深刻な性能崩壊が起こることを示し、剪定で失われた重み成分を低ランク補正で部分的に復元するGLUESTICKを提案する。

- **2025-10 · [Deconstructing Attention: Investigating Design Principles for Effective Language Modeling](2025-2510.11602-deconstructing-attention-investigating-design-principles-for-effective-l.md)**  
  実装：[✓](https://github.com/HUIYINXUE/DeconAttn) ・ リポジトリ内被引用：0  
  標準Transformerの注意機構は、現在のトークンが過去のトークンから情報を集めるために、現在層のhidden stateからQ・K・Vを生成し、QK内積をsoftmaxで正規化してVを混合する。

- **2025-10 · [CoRoVA: Compressed Representations for Vector-Augmented Code Completion](2025-2510.19644-corova-compressed-representations-for-vector-augmented-code-completion.md)**  
  実装：[✓](https://anonymous.4open.science/r/CoRoVA) ・ リポジトリ内被引用：0  
  検索した別ファイル断片を1件1ベクトルへ圧縮して射影し、10トークンだけを入力へ足すことで、コード補完の品質を保ちながら最初のトークンまでの時間を20パーセントから38パーセント減らす方式。

- **2025-10 · [Computationally Efficient FPGA-based Large Language Model Inference for Real-Time Decision-Making in Robotic Systems](2025-5c6550db1690-computationally-efficient-fpga-based-large-language-model-inference-for-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLaMA 2-7Bをロボットへ搭載するため、グループ量子化と混合精度、注意の削減を、FPGAロジックとAIエンジンとCPUへ演算を割り振るヘテロジニアス実装と組み合わせ、Jetson AGX Orin比1.95倍のスループットと18ワット動作を実機で示した研究。

- **2025-10 · [Chopping Trees: Semantic Similarity Based Dynamic Pruning for Tree-of-Thought Reasoning](2025-2511.08595-chopping-trees-semantic-similarity-based-dynamic-pruning-for-tree-of-tho.md)**  
  実装：[✓](https://github.com/kimjoonghokim/SSDP) ・ リポジトリ内被引用：0  
  展開直後の子ノードを文埋め込みの類似度でまとめ、報酬最大の代表だけを残すオンライン意味的剪定で、木探索の探索ノードを85〜90パーセント減らし、DPTS比最大2.3倍の高速化と精度の概ね維持を両立した推論時探索の効率化。

- **2025-10 · [BRIEF-Pro: Universal Context Compression with Short-to-Long Synthesis for Fast and Accurate Multi-Hop Reasoning](2025-2510.13799-brief-pro-universal-context-compression-with-short-to-long-synthesis-for.md)**  
  実装：[✓](https://github.com/JasonForJoy/BRIEF) ・ リポジトリ内被引用：0  
  短い種データから長文脈の訓練データを合成し、質問に効く証拠だけを文数指定つきで要約する3B圧縮器BRIEF-Proにより、1万語超の検索文脈を32倍に圧縮しながら70B読み手のQA性能を既存圧縮より平均4.67パーセント高く保った文脈圧縮の研究。

- **2025-10 · [AttnCache: Accelerating Self-Attention Inference for LLM Prefill via Attention Cache](2025-2510.25979-attncache-accelerating-self-attention-inference-for-llm-prefill-via-atte.md)**  
  実装：[✓](https://github.com/PASAUCMerced/AttnCache) ・ リポジトリ内被引用：0  
  従って「注意計算全体をゼロにする」方式ではない。著者の実測はCPUで平均1.2倍のエンドツーエンド（E2E）高速化、自己注意部分で平均2倍、GPUでE2E平均1.6倍、注意部分で平均3倍を報告する。

- **2025-10 · [Adaptive Dual Reasoner: Large Reasoning Models Can Think Efficiently by Hybrid Reasoning](2025-2510.10207-adaptive-dual-reasoner-large-reasoning-models-can-think-efficiently-by-h.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  適応的 Dual Reasoner（ADR）は、大規模推論モデルが簡単な計算でも長いChain-of-Thoughtを出力する「過剰思考」を抑えるため、推論途中の難しさに応じてeasy（簡潔な思考）とhard（深い思考）を切り替える方式である。

- **2025-10 · [A Free Lunch in LLM Compression: Revisiting Retraining after Pruning](2025-2510.14444-a-free-lunch-in-llm-compression-revisiting-retraining-after-pruning.md)**  
  実装：[✓](https://github.com/ZIB-IOL/Free-Lunch-in-LLM-Compression) ・ リポジトリ内被引用：0  
  枝刈り後の適応を部分モデル単位の局所再構成で行う方法を最大72Bまで検証し、非線形部分を含む粒度では品質が粒度に依存しないフリーランチ領域と、行列単位だけが劣ること、再構成後に枝刈り基準の差が消えることを示した研究。

- **2025-09 · [Vocabulary Customization for Efficient Domain-Specific LLM Deployment](2025-2509.26124-vocabulary-customization-for-efficient-domain-specific-llm-deployment.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ドメイン固有トークンを語彙へ追加し、マージ操作の末尾追加によりトークン数が決して増えないことを保証しながら、入力系列を最大20パーセント短縮しスループットを20〜30パーセント高める語彙カスタマイズを、電子商取引の実務タスクで検証した研究。

- **2025-09 · [VeriLLM: A Lightweight Framework for Publicly Verifiable Decentralized Inference](2025-2509.24257-verillm-a-lightweight-framework-for-publicly-verifiable-decentralized-in.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分散推論の出力を誰でも検証できるよう、隠れ状態のMerkleコミットとVRFサンプリング再計算を組み合わせ、検証費用を推論の約1パーセントへ抑えつつ、正直な検証がナッシュ均衡になる報酬設計まで与えた検証プロトコル。

- **2025-09 · [UniPruning: Unifying Local Metric and Global Feedback for Scalable Sparse LLM Inference](2025-2510.03291-unipruning-unifying-local-metric-and-global-feedback-for-scalable-sparse.md)**  
  実装：[✓](https://github.com/RainbowQTT/UniPruning) ・ リポジトリ内被引用：0  
  重み更新なしで、層ごとの顕著性と鏡像降下による全体の予算再配分を統一し、非構造型と二対四を含む半構造型の両方で高スパーシティでも崩れにくい学習後枝刈りを実現する方式。

- **2025-09 · [Thinking-Free Policy Initialization Makes Distilled Reasoning Models More Effective and Efficient Reasoners](2025-2509.26226-thinking-free-policy-initialization-makes-distilled-reasoning-models-mor.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論モデルを検証可能報酬で強化学習するRLVR（Reinforcement Learning with Verifiable Rewards）では、正解が自動判定できる数学・コード課題を多数解かせ、rolloutごとの成否からpolicyを更新する。最大応答長を短く制限すれば安くなるが、途中の検証・再考を切り捨てることで、学習後の正答率が戻らない場合がある。

- **2025-09 · [Stop Before You Fail: Operational Capability Boundaries for Mitigating Unproductive Reasoning in Large Reasoning Models](2025-2509.24711-stop-before-you-fail-operational-capability-boundaries-for-mitigating-un.md)**  
  実装：[✓](https://github.com/qingjiesjtu/CapBound) ・ リポジトリ内被引用：0  
  解けない問題への長く非生産的な推論を減らすため、推論中の表現の軌跡と入力直後の隠れ状態という2つの早期信号を発見し、推論を打ち切って簡潔な方針だけを提示させるテスト時監視を提案した研究。

- **2025-09 · [Semantic Agreement Enables Efficient Open-Ended LLM Cascades](2025-2509.21837-semantic-agreement-enables-efficient-open-ended-llm-cascades.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数の小さいモデルの出力同士の意味的な一致を振り分け信号にし、学習なし・ブラックボックス対応のまま、大きいモデルの計算量の40パーセントで同等以上の品質と最大61パーセントの遅延削減を達成する自由生成向けカスケード。

- **2025-09 · [Self-Aligned Reward: Towards Effective and Efficient Reasoners](2025-2509.05489-self-aligned-reward-towards-effective-and-efficient-reasoners.md)**  
  実装：[✓](https://github.com/amazon-science/Self-Aligned-Reward-Towards_Effective_and_Efficient_Reasoners) ・ リポジトリ内被引用：0  
  提案する自己整合報酬（Self-Aligned Reward; SAR）は、同じ回答 $a$ の困惑度を、質問 $q$ を与えた場合と与えない場合で計算する。例えばQwen3-1.7Bでは、GRPOの平均正答率53.37%、回答長762.8トークンに対して、SAR付きGRPOは54.13%、602.0トークンだった。

- **2025-09 · [QWHA: Quantization-Aware Walsh-Hadamard Adaptation for Parameter-Efficient Fine-Tuning on Large Language Models](2025-2509.17428-qwha-quantization-aware-walsh-hadamard-adaptation-for-parameter-efficien.md)**  
  実装：[✓](https://github.com/vantaa89/qwha) ・ リポジトリ内被引用：0  
  量子化誤差の大きいチャネルへ係数予算を寄せて初期化するウォルシュ・アダマール変換型の疎アダプタで、低ビット量子化モデルの適応精度を低ランク型より高め、変換型の学習の遅さも単一変換と加減算だけの核で解消した方式。

- **2025-09 · [Lightweighting Large Models: A Review of Model Compression Techniques](2025-63d5bd54b66a-lightweighting-large-models-a-review-of-model-compression-techniques.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル圧縮を資源予算付きの最適化として定義し、枝刈り・量子化・知識蒸留・低ランク分解・パラメータ共有の5手法を圧縮率・性能保持・効率・難易度・構造変更の有無で比較し、キー・バリューキャッシュと視覚トークンという構造固有の律速まで整理したサーベイ。

- **2025-09 · [HiPO: Hybrid Policy Optimization for Dynamic Reasoning in LLMs](2025-2509.23967-hipo-hybrid-policy-optimization-for-dynamic-reasoning-in-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HiPO（Hybrid Policy Optimization）は、各入力に対して詳細推論を行うThink-onと直接回答するThink-offを選ぶ能力をモデル自体に学習させる方式である。

- **2025-09 · [FS-DFM: Fast and Accurate Long Text Generation with Few-Step Diffusion Language Models](2025-2509.20624-fs-dfm-fast-and-accurate-long-text-generation-with-few-step-diffusion-la.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ステップ数を条件として学習し、大きな1歩が多歩の合成と一致する一貫性と、区間積分した累積スカラーによる更新で、離散フローマッチングの生成を1024ステップから8ステップへ減らして同等のパープレキシティを保つ方式。

- **2025-09 · [Frame-Stacked Local Transformers For Efficient Multi-Codebook Speech Generation](2025-2509.19592-frame-stacked-local-transformers-for-efficient-multi-codebook-speech-gen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Koel-TTSとNanoCodecを使ったLibriTTS評価では、積層係数2で自己回帰型が従来の非積層・全コード並列方式の2.1倍、MaskGIT型が3.1倍の推論処理量を示した。

- **2025-09 · [ENSI: Efficient Non-Interactive Secure Inference for Large Language Models](2025-2509.09424-ensi-efficient-non-interactive-secure-inference-for-large-language-model.md)**  
  実装：[✓](https://github.com/sugarhh/ENSI) ・ リポジトリ内被引用：0  
  CKKSとBitNetの共同設計で、乗算なしの行列積、再学習不要のシグモイド注意、RMSNorm内蔵のブートストラップにより、非対話型の秘匿推論を高速化する枠組み。

- **2025-09 · [Effective Model Pruning: Measuring the Redundancy of Model Components](2025-2509.25606-effective-model-pruning-measuring-the-redundancy-of-model-components.md)**  
  実装：[✓](https://github.com/noMushroomw/Effective-model-pruning) ・ リポジトリ内被引用：0  
  ニューラルネットワークの枝刈りでは、重要度の低い重みや注意ヘッドを削除するためにMagnitude、Wanda、勾配感度などのスコアを用いる。例えばLLMで全層一律50%の非構造化枝刈りを指定すると、スコアの分布が集中している層と均一な層へ同じ予算を押し付ける。

- **2025-09 · [AxLLM: accelerator architecture for large language models with computation reuse capability](2025-2509.22512-axllm-accelerator-architecture-for-large-language-models-with-computatio.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  量子化で重みの値の種類が絞られる点を利用し、重み値ごとの乗算結果をキャッシュして再利用するアクセラレータAxLLMを提案し、再利用率87パーセント以上・平均1.7倍の高速化・消費電力約28パーセント減を、再学習なし・無損失で示した研究。

- **2025-09 · [AttnComp: Attention-Guided Adaptive Context Compression for Retrieval-Augmented Generation](2025-2509.17486-attncomp-attention-guided-adaptive-context-compression-for-retrieval-aug.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  中間層の注意で文書の関連度を測り、累積注意が閾値へ達するまでだけ文書を残す適応型圧縮で、検索拡張生成の正解率を無圧縮より上げながら入力を17倍に圧縮し遅延を半分にする方式。

- **2025-09 · [Amdahl's Law for LLMs: A Throughput-Centric Analysis of Extreme LLM Quantization](2025-d58c83365862-amdahl-s-law-for-llms-a-throughput-centric-analysis-of-extreme-llm-quant.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者はTransformerの演算を、極端な量子化で行列乗算を置換できる射影部分と、置換しにくい注意ヘッド内部に分ける。さらにAmdahl則で「改善できる部分が元の実行時間の何割か」を明示し、13種類のGPT・OPT・LLaMA構成を、クラウド向け256×256およびエッジ向け32×32のシストリック配列でサイクル精度解析した。

- **2025-09 · [Adaptive Overclocking: Dynamic Control of Thinking Path Length via Real-Time Reasoning Signals](2025-2509.17000-adaptive-overclocking-dynamic-control-of-thinking-path-length-via-real-t.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論進捗ベクトルへの介入強度を、問題の難しさによる初期化とトークンごとの予測エントロピーによる調整で動的に制御し、トークン上限1024のMath500でQwen-32Bの正解数を75件から102件へ増やした、推論時の考えすぎを抑える適応制御。

- **2025-08 · [Hardwired-Neurons Language Processing Units as General-Purpose Cognitive Substrates](2025-2508.16151-hardwired-neurons-language-processing-units-as-general-purpose-cognitive.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの重みを金属配線の形状として回路へ埋め込み、メモリアクセスを消すことで桁違いのスループットとエネルギー効率を狙う言語処理ユニットと、その製造を成立させる配線埋め込み方法の提案。

- **2025-08 · [GPT-OSS-20B: A Comprehensive Deployment-Centric Analysis of OpenAI's Open-Weight Mixture of Experts Model](2025-2508.16700-gpt-oss-20b-a-comprehensive-deployment-centric-analysis-of-openai-s-open.md)**  
  実装：[✓](https://github.com/deepdik/GPT-OSS-20B-analysis) ・ リポジトリ内被引用：0  
  MoEは全重みの一部だけを各トークンで活性化するため、演算量はDenseの同規模モデルより小さくなり得る。しかし、未活性のエキスパート重みがメモリから消えるわけではなく、ルーティング、メモリアクセス、KV保持、プリフィルの費用も発生する。GPUのCUDA allocatorピークメモリはそれぞれ43,461MB、63,650MB、66,459MB。

- **2025-08 · [Fast weight programming and linear transformers: from machine learning to neurobiology](2025-2508.08435-fast-weight-programming-and-linear-transformers-from-machine-learning-to.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  主要な根拠は原著の式(13)、(23)～(24)、表1、表2、および関連研究の分析であり、著者が新しいサービングシステムを実装して速度を測定した論文ではない。

- **2025-08 · [EGGS-PTP: An Expander-Graph Guided Structured Post-training Pruning Method for Large Language Models](2025-2508.09471-eggs-ptp-an-expander-graph-guided-structured-post-training-pruning-metho.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  線形層を二部グラフとみなし、対角選択で連結性を保証しながらN:M構造化枝刈りを行う学習後枝刈り手法。重要度保持とチャネル破損回避を両立し、全モデルで既存の構造化枝刈りを上回る。

- **2025-08 · [ChipChat: Low-Latency Cascaded Conversational Agent in MLX](2025-2509.00078-chipchat-low-latency-cascaded-conversational-agent-in-mlx.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  音声認識から音声合成まで全段をストリーミング化して段の待ちを重ね合わせ、MLX実装でMac Studio上に1秒未満の応答遅延と割り込み対応を持つ端末内音声対話エージェントを実現したシステム。

- **2025-07 · [The Case for Instance-Optimized LLMs in OLAP Databases](2025-2507.04967-the-case-for-instance-optimized-llms-in-olap-databases.md)**  
  実装：[✓](https://github.com/mpi-dsg/IOLM-DB) ・ リポジトリ内被引用：0  
  OLAPクエリごとに代表データで較正した量子化・疎化・構造的枝刈りで専用の軽量言語モデルを生成し、行単位の言語モデル呼び出しのスループットを最大3.31倍、フットプリントを最大76%削減するデータベース向け推論最適化の概念実証。

- **2025-07 · [SpeLLM: Character-Level Multi-Head Decoding](2025-2507.16323-spellm-character-level-multi-head-decoding.md)**  
  実装：[✓](https://github.com/schwartz-lab-NLP/SpeLLM) ・ リポジトリ内被引用：0  
  SpeLLMは入力のBPE語彙を残したまま、出力の予測表現だけを文字単位に分離する。4つの公開モデルを変換した実験では、教師の上位5候補のいずれかと文字列が完全一致する割合が平均91.75%、AutoCorrectありでは94.93%となった。

- **2025-07 · [Smooth Reading: Bridging the Gap of Recurrent LLM to Self-Attention LLM on Long-Context Tasks](2025-2507.19353-smooth-reading-bridging-the-gap-of-recurrent-llm-to-self-attention-llm-o.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかし一度に大量の文書を読み込ませると、必要な情報が後続トークンによって上書き・圧縮され、長文質問応答や要約の精度が下がりやすい。主な評価ではSWA-3B-4k-SRがLongBenchで自己注意のQwen2.5-3Bの平均を3.61ポイント上回る。

- **2025-07 · [Search-in-Context: Efficient Multi-Hop QA over Long Contexts via Monte Carlo Tree Search with Dynamic KV Retrieval](2025-a9c6d6258692-search-in-context-efficient-multi-hop-qa-over-long-contexts-via-monte-ca.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈の多段質問応答を、モンテカルロ木探索による段ごとの探索、段ごとに4千トークンぶんの重要KVを取り出す動的検索、自動ラベル学習の過程報酬モデルで解き、8Bモデルで70Bモデルの直接応答を上回るF1を示した枠組み。

- **2025-07 · [GeLaCo: An Evolutionary Approach to Layer Compression](2025-2507.10059-gelaco-an-evolutionary-approach-to-layer-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層崩壊の融合案を進化的に探索する圧縮手法。残差寄与の類似度とKLを適応度に、融合係数まで含めて最適化し、圧縮率と品質のパレート前線も推定する。Llama系で比較対象をほぼ一貫して上回る。

- **2025-07 · [DOTResize: Reducing LLM Width via Discrete Optimal Transport-based Neuron Merging](2025-2507.04517-dotresize-reducing-llm-width-via-discrete-optimal-transport-based-neuron.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  捨てるはずのニューロンの信号を、活性の近さに基づく最適輸送の写像で残すニューロンへ混ぜ込んでから幅を縮める、学習不要の幅圧縮。枝刈りの上乗せとしてパープレキシティと下流精度の損失を回復する。

- **2025-07 · [DistrAttention: An Efficient and Flexible Self-Attention Mechanism on Modern GPUs](2025-2507.17245-distrattention-an-efficient-and-flexible-self-attention-mechanism-on-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  埋め込み次元方向にQの似た列をグループ化し代表列とK行の合計で注意行列を近似することで、全トークンの文脈を保ったまま注意計算をフラッシュアテンション2比で最大37%高速化する近似注意機構。

- **2025-07 · [CoRE: Enhancing Metacognition with Label-free Self-evaluation in LRMs](2025-2507.06087-core-enhancing-metacognition-with-label-free-self-evaluation-in-lrms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い推論を生成する言語モデルは、複雑な数学問題で有用な中間計算を積み重ねる一方、同じ検算や方針の見直しを繰り返し、答えが得られないまま出力を延ばす場合がある。正誤ラベルを集めて判定器を追加学習する方式ではなく、モデルが生成中に持つ隠れ状態を利用する。

- **2025-07 · [Accurate and Efficient Fine-Tuning of Quantized Large Language Models Through Optimal Balance in Adaptation](2025-2407.17029-accurate-and-efficient-fine-tuning-of-quantized-large-language-models-th.md)**  
  実装：[✓](https://github.com/xiaocaigou/qbaraqahira) ・ リポジトリ内被引用：0  
  量子化モデルの低ランク適応が学習不足になる原因を、複雑な入出力と低いランクの不均衡と捉え、平均プーリングで入出力を圧縮してランクを広げることで釣り合いを取り、さらにブロック量子化へ合わせて4ビット推論モデルを直接作れるようにした方式。

- **2025-07 · [A Comprehensive Evaluation on Quantization Techniques for Large Language Models](2025-2507.17417-a-comprehensive-evaluation-on-quantization-techniques-for-large-language.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの量子化方式は、重み・活性値の精度だけでなく、外れ値をならす前処理、量子化後の誤差補償、対称・非対称、チャネル・グループ粒度、スケールの表現形式などを組み合わせている。さらにRTX 4090のINT4はプリフィルを約2倍高速化するが、バッチ1のデコードはBF16より遅い。

- **2025-06 · [Routing Mamba: Scaling State Space Models with Mixture-of-Experts Projection](2025-2506.18145-routing-mamba-scaling-state-space-models-with-mixture-of-experts-project.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者らは115Mから10B総パラメータまでの構成、Mamba、Mamba2、Gated DeltaNet、注意機構とのハイブリッドであるSambaを評価する。

- **2025-06 · [ReTern: Exploiting Natural Redundancy and Sign Transformations for Enhanced Fault Tolerance in Compute-in-Memory-Based Ternary LLMs](2025-2506.01140-retern-exploiting-natural-redundancy-and-sign-transformations-for-enhanc.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  三値LLMをコンピュート・イン・メモリへ載せる際のスタックアット故障に対し、ゼロ重みの冗長表現と列単位の符号反転を組み合わせ、再学習なしで故障による精度低下を大幅に抑える重みマッピング手法。

- **2025-06 · [MoTE: Mixture of Ternary Experts for Memory-efficient Large Multimodal Models](2025-2506.14435-mote-mixture-of-ternary-experts-for-memory-efficient-large-multimodal-mo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoTE（Mixture of Ternary Experts）は、画像と言語を扱うマルチモーダル言語モデルを密な事前学習済みモデルからMoEへ拡張する際、既存のFFNを高精度の共有専門家として保持し、新たな経路選択専門家だけを三値の重みで学習する方式である。

- **2025-06 · [Fast on the Easy, Deep on the Hard: Efficient Reasoning via Powered Length Penalty](2025-2506.10446-fast-on-the-easy-deep-on-the-hard-efficient-reasoning-via-powered-length.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  正解報酬へ長さのべき乗に反比例する項を加え、短い応答ほど長さ差が効き長い応答では効かない報酬にすることで、易しい問題のトークンを最大で約九割減らしつつ難しい問題の精度を保った。

- **2025-06 · [Fast ECoT: Efficient Embodied Chain-of-Thought via Thoughts Reuse](2025-2506.07639-fast-ecot-efficient-embodied-chain-of-thought-via-thoughts-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  具身推論の時間的局所性を使い、前ステップの思考の再利用と推論段階の並列生成と非同期実行で、ECoTの遅延を最大約7.5倍速くしながら成功率を保つFast ECoTを提案する。

- **2025-06 · [Don't Pay Attention](2025-2506.11305-don-t-pay-attention.md)**  
  実装：[✓](https://github.com/rimads/avey-dpa) ・ リポジトリ内被引用：0  
  本論文は、Transformerの自己注意とRNN系の再帰状態の双方を用いず、長い系列から関連部分だけを選択してトークン間の相互作用を計算する言語モデルAveyを提案する。一方、一般NLPのゼロショット平均精度は1.52BではTransformer++の52.54%に対してAveyは51.53%で、全面的な品質優位ではない。

- **2025-06 · [Context-Aware CodeLLM Eviction for AI-assisted Coding](2025-2506.18796-context-aware-codellm-eviction-for-ai-assisted-coding.md)**  
  実装：[✓](https://figshare.com/s/1a30559050bc43d5fefd) ・ リポジトリ内被引用：0  
  自前ホストのCodeLLMサービングで、最終利用時刻・再読み込み時間・将来需要・タスク重要度の4要素からエビクションスコアを計算して追い出し先を決めるCACEを提案し、LRU比でTTFT最大70%減・読み込みオーバーヘッド最大31%減を実機で示した研究。

- **2025-06 · [Attention2D: Communication Efficient Distributed Self-Attention Mechanism](2025-2503.15758-attention2d-communication-efficient-distributed-self-attention-mechanism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈の自己注意をGPU間で分割する際、Ring 注意機構などの従来の一次元コンテキスト並列では、各GPUが自分のクエリ部分を担当しても、全てのキー・バリュー（KV）を順に受け取る必要がある。A100を16枚または64枚使用したGPT-3型モデルの学習では、Ring 注意機構に対してNOがそれぞれ2.4倍以上・4倍以上の学習性能を示す。

- **2025-06 · [Advancing Decoding Strategies: Enhancements in Locally Typical Sampling for LLMs](2025-2506.05387-advancing-decoding-strategies-enhancements-in-locally-typical-sampling-f.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案する適応的 Semantic-Aware Typicality Sampling（ASTS）は、(1) 過去のエントロピー変動を用いた候補区間の適応化、(2) 意味的類似度・関連度・多様性の複合採点、(3) 報酬と反復ペナルティによる確率再重み付け、(4) 正規化と温度調整、という段階を組み合わせる。

- **2025-05 · [Understanding Differential Transformer Unchains Pretrained Self-Attentions](2025-2505.16333-understanding-differential-transformer-unchains-pretrained-self-attentio.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者らは、この方式の利点を単純な注意の疎化として説明できるかを検証し、負の寄与による表現力、注意頭部の冗長性低下、学習時の安定性という三つの要因を分析した。Llama-3.2-3Bの11課題平均は60.2から64.2へ4.0ポイント改善し、針検索の平均正答率は66.9%から78.3%へ11.4ポイント改善した。

- **2025-05 · [TRIM: Achieving Extreme Sparsity with Targeted Row-wise Iterative Metric-driven Pruning](2025-2505.16743-trim-achieving-extreme-sparsity-with-targeted-row-wise-iterative-metric-.md)**  
  実装：[✓](https://github.com/flobk/TRIM) ・ リポジトリ内被引用：0  
  ワンショット枝刈りの疎率を層内一律から出力次元ごとに変え、次元別品質（出力のコサイン類似度）に基づく反復調整で配分を最適化し、70〜80パーセントの極端な疎率でもパープレキシティの崩壊を抑えるTRIMを提案した研究。

- **2025-05 · [Towards ML System Extensibility](2025-af96f29ab97d-towards-ml-system-extensibility.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分散実行の固定化で失われる拡張性を、分散アクター・先行値・タスクの接口と解釈型・コンパイル型の二方式の併用で取り戻す構想を示し、Ray上の試作で推論と学習の双方でSPMD方式と同等の性能に届くことを示した位置づけ論文。

- **2025-05 · [SwiftPrune: Hessian-Free Weight Pruning for Large Language Models](2025-2501.16376-swiftprune-hessian-free-weight-pruning-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ヘッセ行列を寄与指標の近似で置き換え、指数加重移動平均で行ごとの並べ替えも省くことで、七十億級モデルの枝刈りを七・七三秒で終え、従来方式の平均十二・二九倍の高速化と疎性五十パーセントでの性能維持を両立したと報告した。

- **2025-05 · [Semantic Retention and Extreme Compression in LLMs: Can We Have Both?](2025-2505.07289-semantic-retention-and-extreme-compression-in-llms-can-we-have-both.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、学習済み大規模言語モデル（LLM）に対する重み剪定と量子化の組合せを、同じ理論圧縮率で比較した研究である。主な結果は、25%剪定と4ビット量子化の組合せが、理論圧縮率TCr=81.25%の条件で、3ビット量子化のみより平均約20%高い意味保持率を示すというものだ。

- **2025-05 · [Scaling Reasoning without Attention](2025-2505.22425-scaling-reasoning-without-attention.md)**  
  実装：[✓](https://github.com/inclusionAI/PromptCoT) ・ リポジトリ内被引用：0  
  KVキャッシュを持たないMamba-2の状態空間双対層だけで推論モデルを構成し、PromptCoTの合成データによる2段階カリキュラムで鍛えた研究。7Bで27B級の推論性能と、メモリ制限下で最大3.66倍のスループットを示した。

- **2025-05 · [QwenLong-CPRS: Towards ∞-LLMs with Dynamic Context Optimization](2025-2505.18092-qwenlong-cprs-towards-llms-with-dynamic-context-optimization.md)**  
  実装：[✓](https://github.com/Tongyi-Zhiwen/QwenLong-CPRS) ・ リポジトリ内被引用：0  
  生成モデルの前段で、自然言語の指示に沿って長文脈から必要なトークンだけを多粒度で残す圧縮モデルにより、プリフィル費用を下げながら長文脈性能を上げる方式。

- **2025-05 · [Multilingual Brain Surgeon: Large Language Models Can be Compressed Leaving No Language Behind](2025-2404.04748-multilingual-brain-surgeon-large-language-models-can-be-compressed-leavi.md)**  
  実装：[✓](https://github.com/X-LANCE/MBS) ・ リポジトリ内被引用：0  
  Multilingual Brain Surgeon（MBS）は、LLMの重み量子化や枝刈りで使うキャリブレーションデータを英語だけから選ぶと、事前学習時に割合が小さい言語の品質が大きく悪化する問題を扱う。

- **2025-05 · [Lossless Token Sequence Compression via Meta-Tokens](2025-2506.00307-lossless-token-sequence-compression-via-meta-tokens.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  繰り返すトークン部分列をプロンプト専用辞書付きのメタトークンへ置換する無損失なプロンプト圧縮で、木構造理解では27パーセント短縮しても精度低下が1ポイント未満にとどまる方式。

- **2025-05 · [LLM-MS: A Multi-Model LLM Search Engine](2025-fa0fa1f7bd52-llm-ms-a-multi-model-llm-search-engine.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数のオープンLLMへトークン予算を動的に配分する検索エンジンで、埋め込み類似度の採点で有望モデルへ生成を寄せて打ち切りを行うOUAと、UCB1バンディットで配分するMABにより、単体モデルより高い応答品質を少ないトークンで得る。

- **2025-05 · [First Finish Search: Efficient Test-Time Scaling in Large Language Models](2025-2505.18149-first-finish-search-efficient-test-time-scaling-in-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  並列生成した推論トレースのうち最初に完了した最も短いものを即座に返すFirst Finish Searchを提案し、DeepSeek-R1のAIME平均で正解率82.23%を、多数決より少ない総トークン31.1Kで達成した。

- **2025-05 · [Exploring Federated Pruning for Large Language Models](2025-2505.13547-exploring-federated-pruning-for-large-language-models.md)**  
  実装：[✓](https://github.com/Pengxin-Guo/FedPrLLM) ・ リポジトリ内被引用：0  
  LLMの重みを削ってメモリ使用量を減らす剪定（枝刈り）は、モデルの入力活性化を校正データで観測して「消しても影響の小さい重み」を選ぶことが多い。LLaMA 7Bの50%疎化では、WikiText2の困惑度（PPL）が密モデル5.67、全データを集める集中剪定7.25、FedPrLLM層one-shot 7.32、クライアント単独7.44となる。

- **2025-05 · [Efficient Large Language Model Inference with Neural Block Linearization](2025-2505.21077-efficient-large-language-model-inference-with-neural-block-linearization.md)**  
  実装：[✓](https://github.com/LIONS-EPFL/NBL) ・ リポジトリ内被引用：0  
  Neural Block Linearization（NBL）は、特定の注意層について「その入力から出力を線形写像でどの程度予測できるか」を測り、予測しやすい層だけを統計的に推定した線形層で代替する。

- **2025-05 · [Efficient Attention via Pre-Scoring: Prioritizing Informative Keys in Transformers](2025-2505.11040-efficient-attention-via-pre-scoring-prioritizing-informative-keys-in-tra.md)**  
  実装：[✓](https://github.com/Bruce-JiYuefeng/prescored-transformer) ・ リポジトリ内被引用：0  
  k平均・kメディアンのクラスタリングやレバレッジスコアで重要なキーを事前に選び、その部分集合だけへハイパーアテンションを適用することで、長文脈の困惑度を12から8.3へ改善する事前スコア付け機構。

- **2025-05 · [EdgeMM: Multi-Core CPU with Heterogeneous AI-Extension and Activation-aware Weight Pruning for Multimodal LLMs at Edge](2025-2505.10782-edgemm-multi-core-cpu-with-heterogeneous-ai-extension-and-activation-awa.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エッジでマルチモーダルLLM（MLLM）を実行する際、画像などをトークンに変換するエンコーダ、入力トークンをまとめて処理するLLM プリフィル、出力トークンを逐次生成するデコードでは、計算とメモリの比率が大きく異なる。ただし、これらは実チップを製造して測定した数字ではなく、シミュレーション・実装設計評価に基づく比較である。

- **2025-05 · [Analog Foundation Models](2025-2505.09663-analog-foundation-models.md)**  
  実装：[✓](https://github.com/IBM/analog-foundation-models) ・ リポジトリ内被引用：0  
  アナログインメモリ計算のノイズと低精度の入力量子化へ大規模言語モデルを頑健化する訓練法で、知識蒸留の後にノイズ注入と重みの切り捨てと静的量子化を組み合わせ、ハードウェア現実的なノイズ下でも16ビット精度との平均差をPhi-3-miniで3.7ポイントまで縮める方式。

- **2025-04 · [TAMP: Token-Adaptive Layerwise Pruning in Multimodal Large Language Models](2025-2504.09897-tamp-token-adaptive-layerwise-pruning-in-multimodal-large-language-model.md)**  
  実装：[✓](https://github.com/G-JWLee/TAMP) ・ リポジトリ内被引用：0  
  マルチモーダルモデルの枝刈りで、出力トークンの多様性が高い層ほど残すパラメータを増やし、注意スコアで選んだ代表入力トークンだけで重み重要度を計算することで、高スパーシティでも多モダリティ理解を保つ枠組みを提案した研究。

- **2025-04 · [Scaling Test-Time Inference with Policy-Optimized, Dynamic Retrieval-Augmented Generation via KV Caching and Decoding](2025-2504.01281-scaling-test-time-inference-with-policy-optimized-dynamic-retrieval-augm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、外部文書を参照する検索拡張生成（RAG）を、検索タイミング、検索結果への忠実性、推論時のメモリ消費の三つの観点から改善する。提案は、方策最適化PORAG、選択的検索ATLAS、KV圧縮CRITICという異なる段階の機構を接続するものである。

- **2025-04 · [LVLM_CSP: Accelerating Large Vision Language Models via Clustering, Scattering, and Pruning for Reasoning Segmentation](2025-2504.10854-lvlm-csp-accelerating-large-vision-language-models-via-clustering-scatte.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論セグメンテーション向けに、代表トークンでの粗推論→全トークンの再投入→[SEG]注意での大胆な枝刈りという学習不要の3段階で画像トークンを間引き、計算量65パーセント削減と精度実質維持を両立した手法。

- **2025-04 · [HERA: Hybrid Edge-cloud Resource Allocation for Cost-Efficient AI Agents](2025-2504.00434-hera-hybrid-edge-cloud-resource-allocation-for-cost-efficient-ai-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェントのサブタスク連鎖では振り分けが後続へ波及することに着目し、類似度予測・S-L距離・収束検出・サブタスク分解を階層化した振り分けで、サブタスクの約46パーセントをローカル小モデルへ逃がしてクラウド費用を19〜30パーセント削減する。

- **2025-04 · [Bi-directional Model Cascading with Proxy Confidence](2025-2504.19391-bi-directional-model-cascading-with-proxy-confidence.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデルカスケードの回送判断を、小モデルの中間層由来の自信と、大モデルを呼ばずに自信を予測する補助モデルの双方向で決める方式を提案し、LLaMA-2 13B→70Bで同等精度の回送率を最大42.5%削減した研究。

- **2025-03 · [Text Compression for Efficient Language Generation](2025-2503.11426-text-compression-for-efficient-language-generation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文を一つの埋め込みへ圧縮し、完了した文の埋め込みをキャッシュして生成する階層型モデルで、小規模領域で計算量最大約10倍と速度最大3倍の効率を得る一方、品質の代償も測る研究。

- **2025-03 · [IteRABRe: Iterative Recovery-Aided Block Reduction](2025-2503.06291-iterabre-iterative-recovery-aided-block-reduction.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMのブロックを類似度で1層ずつ落とし、そのたびに知識蒸留とLoRAで回復する反復を繰り返すことで、わずか250万トークンの回復データで約25%の層削減と性能保持を両立する圧縮手法。

- **2025-03 · [Efficient self-attention with smart pruning for sustainable large language models](2025-7e148a9b32f9-efficient-self-attention-with-smart-pruning-for-sustainable-large-langua.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  埋め込みと全結合層の重みを凍結とゼロ化で削り、自己注意のクエリとキーを行の同一化で、バリューを対角化で圧縮する枝刈り手法。GPT-2で全体約70%圧縮しながら分類精度の低下を約2.5ポイントに抑え、推論を2.5倍に高速化したと報告する。

- **2025-03 · [Attention Condensation via Sparsity Induced Regularized Training](2025-2503.01564-attention-condensation-via-sparsity-induced-regularized-training.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、Transformerの注意行列を推論時に疎化する際の品質劣化を、学習時に注意確率を少数の要素へ集中させておくことで抑える手法を提案する。理想マスクでの精度維持と、低コストのマスク予測器が同じ結果を達成できるかは別問題であり、Hyper-注意機構では正則化モデルの方が悪い条件も存在する。

- **2025-02 · [Streaming Looking Ahead with Token-level Self-reward](2025-2503.00029-streaming-looking-ahead-with-token-level-self-reward.md)**  
  実装：[✓](https://github.com/CognitiveKernel/SLA) ・ リポジトリ内被引用：0  
  方策モデル自身にトークン単位の自己報酬を持たせるReward Transformerと、先読みトークンを再利用するバランス木探索SLAで、外部報酬モデルなしの先読みデコードをストリーミング可能にし、凍結したLlama-3-8Bで貪欲デコードに対する勝率79.7パーセントを得た。

- **2025-02 · [StreamDCIM: A Tile-based Streaming Digital CIM Accelerator with Mixed-stationary Cross-forwarding Dataflow for Multimodal Transformer](2025-2502.05798-streamdcim-a-tile-based-streaming-digital-cim-accelerator-with-mixed-sta.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  マルチモーダルTransformer向けに、再構成可能なタイル単位デジタルCIMマクロ、混合定常クロスフォワーディング・データフロー、書き換えを計算と重ねる細粒度パイプラインを組み合わせ、ViLBERTで非ストリーミング比2.63倍・層単位ストリーミング比1.28倍の高速化を合成評価で示したCIMアクセラレータ。

- **2025-02 · [SHAFT: Secure, Handy, Accurate and Fast Transformer Inference](2025-14a507fe2936-shaft-secure-handy-accurate-and-fast-transformer-inference.md)**  
  実装：[✓](https://github.com/andeskyl/SHAFT) ・ リポジトリ内被引用：0  
  入力クリッピング付き常微分方程式による定数ラウンドのソフトマックスと、フーリエ級数近似のGELUで、秘密分散型のTransformer秘密推論を速く正確にし、Hugging Faceからそのまま持ち込めるようにした枠組みSHAFT。

- **2025-02 · [Online Pseudo-average Shifting Attention (PASA) for Robust Low-precision LLM Inference: Algorithms and Numerical Analysis](2025-2503.01873-online-pseudo-average-shifting-attention-pasa-for-robust-low-precision-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キーの擬似平均を行列積で引くオンライン処理と最大値の補正で、フラッシュアテンション全体を半精度化しても桁あふれしないようにする数値安定化手法。実モデルで注意スコアの値域を半精度の範囲へ戻した。

- **2025-02 · [HASSLE-free: A unified Framework for Sparse plus Low-Rank Matrix Decomposition for LLMs](2025-2502.00899-hassle-free-a-unified-framework-for-sparse-plus-low-rank-matrix-decompos.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みの疎＋低ランク分解について、層ごとの再構成誤差を緩和せず直接解く交互最小化の統一枠組みを提示し、従来法がその緩和であることを示して、Llama系でパープレキシティとゼロショット精度の両方を改善するワンショット圧縮。

- **2025-02 · [HAAN: A Holistic Approach for Accelerating Normalization Operations in Large Language Models](2025-2502.11832-haan-a-holistic-approach-for-accelerating-normalization-operations-in-la.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  深い層で標準偏差の逆数が対数領域で直線的に減る性質を使い、正規化統計の計算を飛ばして予測し、残りもサブサンプリングと量子化で軽くするアルゴリズムとFPGAアクセラレータの協調設計で、正規化の遅延と電力を大きく下げる。

- **2025-02 · [Exploring Model Invariance with Discrete Search for Ultra-Low-Bit Quantization](2025-2502.06844-exploring-model-invariance-with-discrete-search-for-ultra-low-bit-quanti.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  順列・スケーリング・回転の不変変換を活性値ガイドの離散探索で同時に探す量子化前処理InvarExploreで、OPT-13Bの2ビット量子化においてAWQのパープレキシティを35.89から26.26へ、推論精度を51.85から55.13へ改善した。

- **2025-02 · [Cicada: A Pipeline-Efficient Approach to Serverless Inference with Decoupled Management](2025-2502.20959-cicada-a-pipeline-efficient-approach-to-serverless-inference-with-decoup.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  サーバーレス推論のモデル読み込みパイプラインについて、層構築の無駄な初期化を1ビット化して省くMiniLoaderと、重み取得を層構築から切り離して順不同適用を可能にするWeightDecouplerで停止時間を潰し、PISeL比で遅延を平均61.59%削減し利用率をほぼ100%まで引き上げた方式。

- **2025-01 · [Softplus Attention with Re-weighting Boosts Length Extrapolation in Large Language Models](2025-2501.13428-softplus-attention-with-re-weighting-boosts-length-extrapolation-in-larg.md)**  
  実装：[✓](https://github.com/iminfine/freeattn) ・ リポジトリ内被引用：0  
  提案するLSSAR（Length Scaled Softplus 注意機構 with Re-weighting）は、第一段でquery/keyの長さ依存正規化とSoftplusを用いて数値的に安定した重みを作り、第二段で重みを中心化して小さい値を抑え、残る大きな値をべき乗で強調する。

- **2025-01 · [Practical Secure Inference Algorithm for a Fine-Tuned Large Language Model Based on Fully Homomorphic Encryption](2025-2501.01672-practical-secure-inference-algorithm-for-a-fine-tuned-large-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  基盤モデルはクライアント、LoRA行列だけはサーバーで暗号文計算する分割と、モデル抽出攻撃へ耐えるPrivate Linear 層により、ChatGLM2-6Bで1トークン1.61秒の秘匿推論を実現する方式。

- **2025-01 · [Deriving Coding-Specific Sub-Models from LLMs using Resource-Efficient Pruning](2025-2501.05248-deriving-coding-specific-sub-models-from-llms-using-resource-efficient-p.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Wandaの校正データを対象領域のものへ替えるだけで、再学習なしに領域・言語特化のサブモデルを切り出せることを示した研究。50%の非構造化枝刈りで、最良サブモデルは全領域で領域別校正から得られ、言語別サブモデルは自言語のHumanEvalで最も高い精度を保った。

- **2024-12 · [Sparse Checkpointing for Fast and Reliable MoE Training](2024-2412.15411-sparse-checkpointing-for-fast-and-reliable-moe-training.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  これらの最大値は比較方式・モデル・障害条件が異なるため、同一条件で「4×31×8倍」を掛け合わせられるわけではない。

- **2024-12 · [Mixture of Hidden-Dimensions Transformer](2024-2412.05644-mixture-of-hidden-dimensions-transformer.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意機構のQ/K/V/O投影とFFNのup/gate/down投影を同じ隠れ次元の選択に合わせて部分実行し、総パラメータ数を増やしても1トークン当たりに活性化するパラメータ数を抑える。LLaMA2型355Mの10指標平均は全活性42.7、MoHDの50%活性42.3、75%活性43.2だった。

- **2024-12 · [GUIDE: A Global Unified Inference Engine for Deploying Large Language Models in Heterogeneous Environments](2024-2412.04788-guide-a-global-unified-inference-engine-for-deploying-large-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルを実運用に配置する際、同じモデルでもGPU、推論ランタイム、入力長、バッチ数、GPU分割方式が変わると、初トークン遅延（TTFT）、復号スループット、GPUメモリ使用量が大きく変化する。

- **2024-12 · [Enhanced Computationally Efficient Long LoRA Inspired Perceiver Architectures for Auto-Regressive Language Modeling](2024-2412.06106-enhanced-computationally-efficient-long-lora-inspired-perceiver-architec.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PerceiverARの履歴情報が第1層で失われる弱点を、履歴を全層へ運ぶ3拡張と、セグメントを半分重ねて交差注意を行い受容野を層ごとに広げるLLPで改善し、注意計算を全注意の12%に抑えながらWikitext-103でPerceiverARの約5分の1の規模でより良いパープレキシティを達成した効率的注意アーキテクチャ研究。

- **2024-12 · [Continuous Speech Tokens Makes LLMs Robust Multi-Modality Learners](2024-2412.04917-continuous-speech-tokens-makes-llms-robust-multi-modality-learners.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  音声対話を言語モデルへ統合する際、文字列と同様に音声も離散トークンIDへ変換し、次のIDを分類する方式が広く用いられる。Mini-Omniの10.84に対しFlow-Omniは8.81で、絶対2.03ポイント、相対約18.7%の低下となる。

- **2024-12 · [Continual Low-Rank Scaled Dot-product Attention](2024-2412.03214-continual-low-rank-scaled-dot-product-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ストリーム処理の継続推論向けに、Continual Transformerの差分更新へNyström低ランク近似を組み込んだ注意を定式化し、ランドマークの更新版と固定版を提示して、音声分類で通常注意の最大1850倍の演算削減と競合する精度を両立させた効率的注意の研究。

- **2024-12 · [Constrained Decoding with Speculative Lookaheads](2024-2412.10418-constrained-decoding-with-speculative-lookaheads.md)**  
  実装：[✓](https://github.com/amazon-science/CDSL-NAACL2025) ・ リポジトリ内被引用：0  
  本論文の対象は、指定語をすべて含む文章や有害な要求に対する無害な応答など、通常の次トークン尤度だけでは満たしにくい制約付き生成である。この方法は制約達成率が高い一方、次の1トークンを確定するために大量のモデル呼び出しを要する。評価器、タスク、ドラフトとターゲットの組合せを分離して読む必要がある。

- **2024-12 · [BEExformer: A Fast Inferencing Binarized Transformer with Early Exits](2024-2412.05225-beexformer-a-fast-inferencing-binarized-transformer-with-early-exits.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  1ビット二値化学習と早期終了を初めて組み合わせたテキスト推論向けトランスフォーマーで、符号関数の2次近似と選択的学習・忘却の仕組みにより、サイズ21.30倍削減と計算量52.27%削減を精度維持と両立させた研究。

### 3年前（2023-12〜2024-11）

- **2024-08 · [Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters](2024-2408.03314-scaling-llm-test-time-compute-optimally-can-be-more-effective-than-scaling-model-parameters.md)**  
  実装：✓ ・ リポジトリ内被引用：112  
  本論文は、大規模言語モデル（LLM）の推論時に追加の計算予算を与える場合、その予算を何回の独立サンプリング、何段の探索、何回の逐次自己修正へ割り当てるべきかを分析する。さらに、小型モデルの推論時追加計算と、約14倍大きいモデルの事前学習を浮動小数点演算回数（FLOPs）で揃えて比較する。

- **2024-09 · [OLMoE: Open Mixture-of-Experts Language Models](2024-2409.02060-olmoe-open-mixture-of-experts-language-models.md)**  
  実装：[✓](https://github.com/allenai/OLMoE) ・ リポジトリ内被引用：110  
  混合専門家（Mixture-of-Experts; MoE）は総パラメータを増やしながら、各トークンで一部専門家だけを実行することで、密 モデルより計算量を抑えられる。

- **2024-02 · [Massive Activations in Large Language Models](2024-2402.17762-massive-activations-in-large-language-models.md)**  
  実装：[✓](https://github.com/locuslab/massive-activations) ・ リポジトリ内被引用：74  
  著者らは入力を変えたときの値の変動と、推論中に値を直接置換する介入実験から、巨大活性値が単なる数値的不安定さではなく、自己注意（self-注意機構）へ一定の加算成分を供給する暗黙のバイアス（implicit bias）として働くと結論付ける。

- **2024-07 · [Learning to (Learn at Test Time): RNNs with Expressive Hidden States](2024-2407.04620-learning-to-learn-at-test-time-rnns-with-expressive-hidden-states.md)**  
  実装：[✓](https://github.com/test-time-training/ttt-lm-pytorch) ・ リポジトリ内被引用：57  
  本論文は、再帰型ニューラルネットワーク（Recurrent Neural Network、RNN）の隠れ状態を単なる固定長ベクトルではなく、小さな機械学習モデルの重みとして表現するテスト時訓練（Test-Time 学習、TTT）層を提案する。

- **2023-12 · [Zoology: Measuring and Improving Recall in Efficient Language Models](2023-2312.04927-zoology-measuring-and-improving-recall-in-efficient-language-models.md)**  
  実装：[✓](https://github.com/HazyResearch/zoology) ・ リポジトリ内被引用：50  
  Zoologyは注意、H3、Hyena、RWKVなどの系列混合器を共通条件で比較し、注意なしの方式がどのようなトークンで失敗するかを細かく測定した研究である。Pileの検証データで、以前の文脈に現れた二語連接の続きを再び予測する位置を「連想想起ヒット」として抽出すると、該当位置は全トークンの6.4%にすぎない。

- **2024-06 · [Your Absorbing Discrete Diffusion Secretly Models the Conditional Distributions of Clean Data](2026-2406.03736-your-absorbing-discrete-diffusion-secretly-models-the-conditional-distri.md)**  
  実装：[✓](https://github.com/ML-GSAI/RADD) ・ リポジトリ内被引用：47  
  RADDは吸収型離散拡散の逆過程で必要な条件付き確率を時刻から切り離し、マスク配置が変わらないステップの推論を省略する。理論的な損失の等価性と、実際の生成時間・困惑度の双方を検証した研究。

- **2024-06 · [A Survey on Mixture of Experts in Large Language Models](2024-2407.06204-a-survey-on-mixture-of-experts-in-large-language-models.md)**  
  実装：[✓](https://github.com/withinmiaov/A-Survey-on-Mixture-of-Experts-in-LLMs) ・ リポジトリ内被引用：40  
  全パラメータ数を大きくしても活性化する部分を限定できるが、実機では選択された専門家へのトークン転送、専門家ごとの負荷の偏り、GPU間の全対全通信、巨大な専門家重みの配置・退避が新たな律速になる。

- **2023-12 · [Honeybee: Locality-enhanced Projector for Multimodal LLM](2023-2312.06742-honeybee-locality-enhanced-projector-for-multimodal-llm.md)**  
  実装：[✓](https://github.com/kakaobrain/honeybee) ・ リポジトリ内被引用：30  
  線形投射器は画像の各位置をほぼ一対一でトークン化するため空間情報を保持しやすいが、解像度が上がると視覚トークン数が増え、言語モデルの計算とメモリを圧迫する。Honeybeeは、出力視覚トークン数を任意に選べることと、局所的な画像構造を保持することを同時に満たす投射器を設計した。

- **2024-05 · [xRAG: Extreme Context Compression for Retrieval-augmented Generation with One Token](2024-2405.13792-xrag-extreme-context-compression-for-retrieval-augmented-generation-with.md)**  
  実装：[✓](https://github.com/Hannibal046/xRAG) ・ リポジトリ内被引用：29  
  検索拡張生成（Retrieval-Augmented Generation、RAG）は、外部の文書から関連情報を検索し、その本文を言語モデルへ入力することで、学習時点に含まれない知識を利用する。

- **2024-09 · [Moshi: a speech-text foundation model for real-time dialogue](2024-2410.00037-moshi-a-speech-text-foundation-model-for-real-time-dialogue.md)**  
  実装：[✓](https://github.com/kyutai-labs/moshi) ・ リポジトリ内被引用：26  
  Moshiは、音声認識、テキストLLM、音声合成を順番に実行する音声対話システムを、入力音声を聞きながら出力音声を生成する全二重の音声言語モデルへ置き換える研究である。音声質問応答の零例評価では、MoshiがWeb Questions 26.6%、LLaMA Questions 62.3%、音声版TriviaQA 22.8%の正答率を示した。

- **2024-04 · [LongVLM: Efficient Long Video Understanding via Large Language Models](2024-2404.03384-longvlm-efficient-long-video-understanding-via-large-language-models.md)**  
  実装：[✓](https://github.com/ziplab/LongVLM) ・ リポジトリ内被引用：17  
  LongVLMは、長時間動画を入力する視覚言語モデル（Vision-Language モデル; VLM）で、画像符号化器から出る大量の視覚トークンを短時間区間ごとに統合する。100フレームを224×224画素で符号化し、元のパッチ特徴が約25,600トークンになる設定で、10区間×30トークンと全体特徴5トークンの計305視覚トークンへまとめる。

- **2024-08 · [Mini-Omni: Language Models Can Hear, Talk While Thinking in Streaming](2024-2408.16725-mini-omni-language-models-can-hear-talk-while-thinking-in-streaming.md)**  
  実装：[✓](https://github.com/gpt-omni/mini-omni) ・ リポジトリ内被引用：16  
  Mini-Omniは、言語モデルの応答文を最後まで生成してから独立した音声合成器へ渡す従来の直列方式を避け、文字トークンと音声トークンを一つの自己回帰生成過程の中で並列に出力する音声対話モデルである。

- **2024-04 · [JetMoE: Reaching Llama2 Performance with 0.1M Dollars](2024-2404.07413-jetmoe-reaching-llama2-performance-with-0-1m-dollars.md)**  
  実装：[✓](https://github.com/myshell-ai/JetMoE) ・ リポジトリ内被引用：16  
  JetMoE-8Bは、混合専門家モデル（Mixture of エキスパート、MoE）の条件付き計算を順伝播ネットワーク（FFN）だけでなく自己注意機構へも拡張した、総パラメータ約80億の言語モデルである。論文はLlama2-7Bとの比較で推論演算量を約70%削減できると述べるが、これは実測の生成遅延が70%減るという意味ではない。

- **2023-12 · [Understanding the Potential of FPGA-Based Spatial Acceleration for Large Language Model Inference](2023-2312.15159-understanding-the-potential-of-fpga-based-spatial-acceleration-for-large.md)**  
  実装：[✓](https://github.com/cornell-zhang/allo/tree/main/examples) ・ リポジトリ内被引用：14  
  大規模言語モデルの推論を再構成可能な論理回路（FPGA）へ載せる従来方式の多くは、同じ演算器を複数の演算子・層へ順番に割り当てる時間多重型である。AMD Alveo U280上のGPT-2では、同じFPGAのDFXに対してプリフィル2.16倍、復号1.10倍の高速化を報告する。

- **2024-11 · [XGrammar: Flexible and Efficient Structured Generation Engine for Large Language Models](2024-2411.15100-xgrammar-flexible-and-efficient-structured-generation-engine-for-large-l.md)**  
  実装：[✓](https://github.com/mlc-ai/xgrammar) ・ リポジトリ内被引用：13  
  構造化生成の文法チェックを高速化するため、語彙を事前検査できるトークンと実行時検査が必要なトークンに分け、前者はマスクをキャッシュし、後者は永続スタックで処理し、文法計算をGPU推論と重ねるエンジン。既存ライブラリより最大で100倍以上速く、サービング全体ではほぼゼロの追加コストになった。

- **2024-09 · [LLaMA-Omni: Seamless Speech Interaction with Large Language Models](2024-2409.06666-llama-omni-seamless-speech-interaction-with-large-language-models.md)**  
  実装：[✓](https://github.com/ictnlp/LLaMA-Omni) ・ リポジトリ内被引用：13  
  従来のカスケード方式では、音声認識が入力を文字起こしし、その文字列を大規模言語モデルへ渡し、生成されたテキストを音声合成器へ送る。

- **2024-02 · [Training-Free Long-Context Scaling of Large Language Models](2024-2402.17463-training-free-long-context-scaling-of-large-language-models.md)**  
  実装：[✓](https://github.com/HKUNLP/ChunkLlama) ・ リポジトリ内被引用：13  
  二重チャンク注意（Dual Chunk 注意機構、以下DCA）は、回転位置埋め込み（Rotary Position Embedding、以下RoPE）を用いた大規模言語モデルが、事前学習時より長い系列で位置関係を見失う問題に対する推論時の注意計算の変更である。最後の比較は特定の閉形式4課題の平均であり、汎用能力の94%を意味しない。

- **2024-10 · [Fast Best-of-N Decoding via Speculative Rejection](2024-2410.20290-fast-best-of-n-decoding-via-speculative-rejection.md)**  
  実装：[✓](https://github.com/Zanette-Labs/SpeculativeRejection) ・ リポジトリ内被引用：11  
  部分応答の報酬が最終報酬と相関することを使い、生成途中で見込みの薄い応答を繰り返し打ち切ることで、Best-of-Nを単一GPUで16倍から32倍効率化する推論時アラインメント。

- **2024-02 · [A Survey on Transformer Compression](2024-2402.05964-a-survey-on-transformer-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  論文はTransformer圧縮を、構造を保つ圧縮（量子化・知識蒸留）と、構造を変える圧縮（枝刈り・効率的なモデル構造）という二つの上位観点で整理する。

- **2024-01 · [APAR: LLMs Can Do Auto-Parallel Auto-Regressive Decoding](2024-2401.06761-apar-llms-can-do-auto-parallel-auto-regressive-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  各トークンの生成にはモデル重みの読み込みと注意計算が必要で、単一要求ではGPUの演算器が十分使われない一方、多数要求では注意計算とKVキャッシュ容量が制約になる。重要なのは独立した段落を別々の生成系列として同時に進めることであり、単に次の複数トークンを予測して検証する投機的復号（投機的復号）とは異なる。

- **2024-10 · [SIGMA: Secure GPT Inference with Function Secret Sharing](2024-c544a15b6867-sigma-secure-gpt-inference-with-function-secret-sharing.md)**  
  実装：[✓](https://github.com/mpc-msri/EzPC/tree/master/GPU-MPC/experiments/sigma) ・ リポジトリ内被引用：10  
  SIGMAは関数秘密分散（Function Secret Sharing; FSS）によって複雑な非線形演算を二者間で実現し、事前に作った暗号鍵を使ってオンライン時の通信を抑える。代表結果は、系列長128の二者間オンライン推論において、既存のGPU秘匿計算系CrypTenより12.2～19倍短い実行時間である。

- **2024-03 · [AI and Memory Wall](2024-2403.14123-ai-and-memory-wall.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  AI向け計算器の演算性能が急速に増える一方、DRAMやデバイス間通信の帯域は同じ速度で増えない。低バッチの自己回帰生成では重みの再読出しが支配的になり、FLOPsだけで推論性能を評価すると誤る。

- **2024-04 · [MixLoRA: Enhancing Large Language Models Fine-Tuning with LoRA-based Mixture of Experts](2024-2404.15159-mixlora-enhancing-large-language-models-fine-tuning-with-lora-based-mixt.md)**  
  実装：[✓](https://github.com/TUDB-Labs/MixLoRA) ・ リポジトリ内被引用：9  
  大規模言語モデルを多くの下流タスクへ適応させるとき、全パラメータを更新する方式は学習用メモリと計算時間が大きい。著者の概要にある「約30%のトークン計算遅延削減」は、元のMixLoRA実装に対する最適化効果を指す総括値であり、通常LoRAより30%速いという意味ではない。

- **2024-01 · [A Comprehensive Survey of Compression Algorithms for Language Models](2024-2401.15347-a-comprehensive-survey-of-compression-algorithms-for-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  枝刈り、量子化、知識蒸留、低ランク近似、パラメータ共有、効率的構造設計の六系統を、圧縮後の性能だけでなく、圧縮を実行するための学習・較正費用から比較するサーベイ。

- **2024-03 · [SynCode: LLM Generation with Grammar Augmentation](2024-2403.01632-syncode-llm-generation-with-grammar-augmentation.md)**  
  実装：[✓](https://github.com/structuredllm/syncode) ・ リポジトリ内被引用：7  
  SynCodeは、言語モデルがJSON、SQL、Python、Goなどの形式言語を生成する際に、文脈自由文法（CFG）を満たすトークンだけを次の候補として残す制約付き復号方式である。

- **2024-06 · [DeciMamba: Exploring the Length Extrapolation Potential of Mamba](2024-2406.14528-decimamba-exploring-the-length-extrapolation-potential-of-mamba.md)**  
  実装：[✓](https://github.com/assafbk/DeciMamba) ・ リポジトリ内被引用：6  
  Mambaは選択的状態空間モデル（Selective State Space モデル; SSM）の一種で、注意機構のように系列長の二乗へ比例する全組合せを直接計算せず、再帰的な隠れ状態へ過去の情報を集約する。

- **2024-03 · [Decoding Compressed Trust: Scrutinizing the Trustworthiness of Efficient LLMs Under Compression](2024-2403.15447-decoding-compressed-trust-scrutinizing-the-trustworthiness-of-efficient-.md)**  
  実装：[✓](https://github.com/decoding-comp-trust/comp-trust) ・ リポジトリ内被引用：6  
  LLM圧縮の評価は、通常の質問応答や知識課題の性能を維持できるかに偏りがちである。評価の中心的な結果は、同程度に圧縮する場合は量子化が枝刈りより元モデルの信頼性を再現しやすいこと、4-bit量子化では一部軸が改善し得ること、3-bitでは通常性能に現れにくい深刻な回帰が生じることである。

- **2024-02 · [Generative Representational Instruction Tuning](2024-2402.09906-generative-representational-instruction-tuning.md)**  
  実装：[✓](https://github.com/ContextualAI/gritlm) ・ リポジトリ内被引用：6  
  GRIT（Generative Representational Instruction Tuning）は、文章生成と文章埋込みを一つの大規模言語モデルで処理するための指示調整方式である。7BモデルのGritLM-7Bは、56データ集合からなるMTEBの平均66.8を示し、同じ基盤モデルから表現専用で訓練した比較版の66.8と同等だった。

- **2024-05 · [A Comprehensive Survey of Accelerated Generation Techniques in Large Language Models](2024-2405.13019-a-comprehensive-survey-of-accelerated-generation-techniques-in-large-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  第一は小型モデルなどで先のトークンを予測し、大型の対象モデルが並列に検証する投機的復号（投機的復号）、第二は簡単なトークンで深いTransformer層の計算を省略する早期終了（early exiting）、第三は複数位置のトークンを同時に生成・更新する非自己回帰生成（non-autoregressive generation）である。

- **2024-02 · [Small Models, Big Insights: Leveraging Slim Proxy Models To Decide When and What to Retrieve for LLMs](2024-2402.12052-small-models-big-insights-leveraging-slim-proxy-models-to-decide-when-an.md)**  
  実装：[✓](https://github.com/plageon/SlimPlm) ・ リポジトリ内被引用：5  
  従来の自己評価型方式は大型言語モデル自身に暫定回答や判断を作らせるため、検索要否を知る段階で高価な大型モデル推論が増える。

- **2024-11 · [kNN Attention Demystified: A Theoretical Exploration for Scalable Transformers](2024-2411.04013-knn-attention-demystified-a-theoretical-exploration-for-scalable-transfo.md)**  
  実装：[✓](https://github.com/sansui-123/knn_attention) ・ リポジトリ内被引用：4  
  近傍探索によって各クエリに重要そうなk個のキーだけを選ぶ方式は経験的に用いられてきたが、何をどの精度で近似できるか、逆伝播で同様の効率化が可能かは自明ではない。

- **2024-03 · [Repoformer: Selective Retrieval for Repository-Level Code Completion](2024-2403.10059-repoformer-selective-retrieval-for-repository-level-code-completion.md)**  
  実装：[✓](https://github.com/amazon-science/Repoformer) ・ リポジトリ内被引用：4  
  Repoformerは、ソースコードの現在のファイルだけでは分からない別ファイルの関数定義や呼出し関係を、必要な場合だけ検索するコード補完方式である。RepoEvalで複数のコード言語モデルを調べると、検索によって補完が改善した例は概ね20%以下、変わらない例が60%以上、悪化する例も約20%あった。

- **2024-10 · [Rethinking Token Reduction for State Space Models](2024-2410.14725-rethinking-token-reduction-for-state-space-models.md)**  
  実装：[✓](https://github.com/wuyushuwys/ToR_SSM) ・ リポジトリ内被引用：3  
  Mamba向けに、隠れ状態由来の重要度でトークンを分類し枝刈りとマージを使い分ける学習後トークン削減を作り、演算2割減でも既存削減法より平均正解率を約9ポイント高く保つ。

- **2024-08 · [Inference Optimizations for Large Language Models: Effects, Challenges, and Practical Considerations](2024-2408.03130-inference-optimizations-for-large-language-models-effects-challenges-and.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  Donisch、Schacht、Lanquillonの論文は、LLMの推論資源を削減する研究を、量子化、剪定、知識蒸留、アーキテクチャ最適化という四群に分けた文献レビューである。§III-Dで紹介する投機的復号の2〜3倍の遅延改善は参照論文に帰属する値であり、このレビューの独立した再現結果ではない。

- **2024-02 · [Plato: Plan to Efficiently Decode for Large Language Model Inference](2024-2402.12280-plato-plan-to-efficiently-decode-for-large-language-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  Platoは、長い回答を1トークンずつ逐次生成する代わりに、質問を意味的な小課題（node）へ分割し、その間の依存関係を有向非巡回グラフ（DAG）として表現することで、依存しない部分を並列生成するLLM推論システムである。

- **2023-12 · [The Cost of Compression: Investigating the Impact of Compression on Parametric Knowledge in Language Models](2023-2312.00960-the-cost-of-compression-investigating-the-impact-of-compression-on-param.md)**  
  実装：[✓](https://github.com/NamburiSrinath/LLMCompression) ・ リポジトリ内被引用：3  
  枝刈りと量子化が重みに蓄えた事実知識へ与える影響を三系統のモデルで系統測定し、全体の同時枝刈りが最も有害で五割超の枝刈りで知識が急落すること、注意の量子化は比較的安全で最終層の構造的枝刈りが特に危険であることを示した。

- **2024-10 · [Scaling Laws for Mixed Quantization](2024-2410.06722-scaling-laws-for-mixed-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  低bitのLLM推論では、すべての重みや活性を同じ低精度へ変換するより、精度低下に敏感な部分を高精度で残す混合量子化が有効になる場合がある。

- **2024-10 · [LevAttention: Time, Space, and Streaming Efficient Algorithm for Heavy Attentions](2024-2410.05462-levattention-time-space-and-streaming-efficient-algorithm-for-heavy-atte.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  実験は画像分類用の視覚Transformer（ViT）であり、LLMのKVキャッシュ圧縮やGPU推論時間の改善を直接実証したものではない。

- **2024-06 · [Recurrent Context Compression: Efficiently Expanding the Context Window of LLM](2024-2406.06110-recurrent-context-compression-efficiently-expanding-the-context-window-o.md)**  
  実装：[✓](https://github.com/WUHU-G/RCC_Transformer) ・ リポジトリ内被引用：2  
  通常のTransformerは、学習時の文脈窓を超えると品質が落ちやすいという別の問題もある。Recurrent Context Compression（RCC）は、長文を短い区間へ分割し、各区間の情報を少数の隠れベクトルへ圧縮して復号器に渡す方式である。主張する32倍圧縮時のBLEU-4約0.95は、特定の短文再構成タスクでの値である。

- **2024-01 · [With Greater Text Comes Greater Necessity: Inference-Time Training Helps Long Text Generation](2024-2401.11504-with-greater-text-comes-greater-necessity-inference-time-training-helps-.md)**  
  実装：[✓](https://github.com/TemporaryLoRA/Temp-LoRA) ・ リポジトリ内被引用：2  
  本論文が扱うのは、数十万トークン規模の小説生成や長編翻訳を、短い注意窓しか持たない言語モデルで継続するときに発生する「古い情報の消失」と「長い鍵・値キャッシュ（KVキャッシュ）の費用」の両立問題である。近い文脈は通常の注意機構で直接読み、古い情報は一時的に変化した重みを介して利用する。

- **2024-11 · [CLOVER: Cross-Layer Orthogonal Vectors Pruning and Fine-Tuning](2024-2411.17426-clover-cross-layer-orthogonal-vectors-pruning-and-fine-tuning.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  重要度の小さい方向を剪定したり、特異値を学習対象にしたりすることで、既存モデルの構造を利用した圧縮と効率的な微調整を行う。

- **2024-10 · [Understanding the Difficulty of Low-Precision Post-Training Quantization for LLMs](2024-2410.14570-understanding-the-difficulty-of-low-precision-post-training-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LLMの重みを2〜4bitへ圧縮すると、GPUメモリ使用量を減らせる可能性がある一方、言語モデルの予測品質が大きく落ちることがある。

- **2024-10 · [Scaling Stick-Breaking Attention: An Efficient Implementation and In-depth Study](2024-2410.17980-scaling-stick-breaking-attention-an-efficient-implementation-and-in-dept.md)**  
  実装：[✓](https://github.com/shawntan/stickbreaking-attention) ・ リポジトリ内被引用：1  
  本論文は、通常のTransformerが採用する正規化指数関数（softmax）に基づく自己注意（self-注意機構）を、棒折り過程（stick-breaking process）で定義される別の注意重みへ置き換える研究である。

- **2024-10 · [Optimized Spatial Architecture Mapping Flow for Transformer Accelerators](2024-2410.07407-optimized-spatial-architecture-mapping-flow-for-transformer-accelerators.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  SAMT（Spatial 構成 Mapping for Transformers）は、Transformer推論の行列演算をTPU型・NVDLA型などの空間アクセラレータへ割り当てる際に、演算子融合の選択とPE（processing element）上のデータフローを同時に最適化する探索フローである。

- **2024-10 · [AERO: Entropy-Guided Framework for Private LLM Inference](2024-2410.13060-aero-entropy-guided-framework-for-private-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  注意エントロピーで非線形演算の役割を診断し、静的正規化とヘッド別エントロピー正則化で非線形を削っても学習が崩れないようにする、プライベート推論向けの設計枠組み。通信を3.4倍削減する。

- **2024-10 · [Addition is All You Need for Energy-efficient Language Models](2024-2410.00907-addition-is-all-you-need-for-energy-efficient-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  浮動小数点乗算の仮数部の積を落として定数で補い、乗算を1回の整数加算で近似する L-Mul を提案し、fp8 乗算より少ないゲート数で同等以上の精度を示すとともに、注意機構への学習なし置換で bf16 との平均差0.07パーセントに収まることを言語モデルで確認した研究。

- **2024-09 · [Parse Trees Guided LLM Prompt Compression](2024-2409.15395-parse-trees-guided-llm-prompt-compression.md)**  
  実装：[✓](https://github.com/LengendaryHippopotamus/PartPrompt) ・ リポジトリ内被引用：1  
  プロンプト圧縮を構文木と文書階層の大域木の枝刈りへ変換し、局所エントロピーと節点値調整で選ぶPartPromptを提案し、残存率20%のBBCnewsでBLEU 13.69と、生成型を含む比較対象の9.22から11.31を上回った。

- **2024-08 · [Kraken: Inherently Parallel Transformers For Efficient Multi-Device Inference](2024-2408.07802-kraken-inherently-parallel-transformers-for-efficient-multi-device-infer.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  層を分割する代わりに小さい副層を並列度ぶん並べて集約を層一回に減らし、その結果を次層の全結合部まで遅らせることで通信を注意計算に重ね、実機で最初のトークンまでの時間を標準構造より幾何平均三十五・六パーセント短縮したと報告した。

- **2024-06 · [How Can We Effectively Expand the Vocabulary of LLMs with 0.01GB of Target Language Text?](2024-2406.11477-how-can-we-effectively-expand-the-vocabulary-of-llms-with-0-01gb-of-targ.md)**  
  実装：[✓](https://github.com/gucci-j/lowres-cve) ・ リポジトリ内被引用：1  
  対象言語の文三万件だけで語彙を拡張する条件で初期化法と学習戦略を比較し、分解平均による初期化と上下二層ずつの学習の組合せが要約で最大四・五八倍の生成高速化と元モデル並みの生成性能を両立することを示した。分類と原言語の低下は学習なしの事後手法で回復する。

- **2024-05 · [Task-agnostic Distillation of Encoder-Decoder Language Models](2024-2305.12330-task-agnostic-distillation-of-encoder-decoder-language-models.md)**  
  実装：[✓](https://github.com/GeneZC/MiniEnD) ・ リポジトリ内被引用：1  
  提案法MiniEnDは、教師と学生の最終層の関係分布を整合する蒸留に、エンコーダとデコーダの接続を反映する損失を追加する。

- **2024-05 · [Ditto: Quantization-aware Secure Inference of Transformers upon MPC](2024-2405.05525-ditto-quantization-aware-secure-inference-of-transformers-upon-mpc.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  尺度を固定した静的量子化と環をまたぐ型変換手続きと知識蒸留を組み合わせ、量子化した秘匿推論を初めて実行可能にし、先行方式比で最大4.40倍の高速化を精度低下を抑えて達成した。

- **2024-03 · [QuantTune: Optimizing Model Quantization with Adaptive Outlier-Driven Fine Tuning](2024-2403.06497-quanttune-optimizing-model-quantization-with-adaptive-outlier-driven-fin.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  整数のビット幅を小さくすると、重みと活性を低精度で表現でき、メモリや演算資源を節約できる可能性がある。しかし通常の対称一様量子化では、一部の極端に大きい活性値に量子化の最大範囲を合わせると、同じビット数で表現する刻み幅が粗くなる。

- **2024-11 · [The Evolution of RWKV: Advancements in Efficient Language Modeling](2024-2411.02795-the-evolution-of-rwkv-advancements-in-efficient-language-modeling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、RWKV（Receptance Weighted Key Value）系列の設計原理と、2024年までの派生研究を整理した単著のレビューである。

- **2024-11 · [Shrinking the Giant: Quasi-Weightless Transformers for Low Energy Inference](2024-2411.01818-shrinking-the-giant-quasi-weightless-transformers-for-low-energy-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トランスフォーマーの多層パーセプトロン（多層パーセプトロン）は、注意機構とは別に各トークンの表現を変換する二つの大きな行列積を持つ。この研究の主要成果は、比較的小規模な視覚トランスフォーマーと文字生成モデルで予測品質を概ね維持しながら、専用再構成可能回路と専用集積回路の合成評価で推論エネルギーを減らした点にある。

- **2024-11 · [MemoryFormer: Minimize Transformer Computation by Removing Fully-Connected Layers](2024-2411.12992-memoryformer-minimize-transformer-computation-by-removing-fully-connecte.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全結合層を行列積からハッシュ表検索へ置き換えて注意以外の計算をほぼ消し、ブロック計算を約19パーセントまで減らしながらPythia同規模の平均正解率を上回る。

- **2024-11 · [Layer Pruning With Consensus: A Triple-Win Solution](2024-2411.14345-layer-pruning-with-consensus-a-triple-win-solution.md)**  
  実装：[✓](https://github.com/CarolinaTavaresDuarte/Consensus-Layer-Pruning/) ・ リポジトリ内被引用：0  
  複数の類似度指標の順位を合議して、除いても特徴表現が最も変わらない層を繰り返し削除する層枝刈りで、演算を最大78.8パーセント減らしながら精度と敵対的頑健性を保つ方式。

- **2024-11 · [Interactions Across Blocks in Post-Training Quantization of Large Language Models](2024-2411.03934-interactions-across-blocks-in-post-training-quantization-of-large-langua.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、LLMの学習後量子化（PTQ）でよく使われる各Transformerブロックを独立に最適化する手法が、どこまで妥当かを実験的に検証する。

- **2024-11 · [Anchor Attention, Small Cache: Code Generation with Large Language Models](2024-2411.06680-anchor-attention-small-cache-code-generation-with-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  手法は、行単位のトークン-wise Anchor 注意機構（TAA）、位置情報をアンカー内へ保持するMulti-Head Positional Encoding（MHPE）、浅い層のアンカーKVを深い層へ直接参照させる層-wise Anchor 注意機構（LAA）からなる。

- **2024-11 · [An exploration of the effect of quantisation on energy consumption and inference time of StarCoder2](2024-2411.12758-an-exploration-of-the-effect-of-quantisation-on-energy-consumption-and-i.md)**  
  実装：[✓](https://github.com/ana-oprescu/GreenLLMs) ・ リポジトリ内被引用：0  
  StarCoder2の量子化と枝刈りを実測し、bitsandbytes量子化はスループット低下のため消費エネルギーが19〜75パーセント増えること、末尾層の枝刈りはエネルギーを減らすが精度を大きく損なうことを示した測定研究。

- **2024-11 · [A Runtime-Adaptive Transformer Neural Network Accelerator on FPGAs](2024-2411.18148-a-runtime-adaptive-transformer-neural-network-accelerator-on-fpgas.md)**  
  実装：[✓](https://github.com/Kabir-Ehsan/Transformer_on_FPGA) ・ リポジトリ内被引用：0  
  トランスフォーマー全体を対象に、モジュール化した高水準合成設計とタイリング、実行時適応を組み合わせた稠密計算向けFPGAアクセラレータ。

- **2024-10 · [Two are better than one: Context window extension with multi-grained self-injection](2024-2410.19318-two-are-better-than-one-context-window-extension-with-multi-grained-self.md)**  
  実装：[✓](https://github.com/Clement25/SharedLLM) ・ リポジトリ内被引用：0  
  一方、単純に過去文脈を一様圧縮すると、質問に必要な細かい事実まで失われやすい。論文要旨の速度改善（ストリーミング型比約2倍、エンコーダ・デコーダ型比約3倍）は対象実装・装置での比較であり、一般的なLLM推論のトークン/s改善倍率と同一視しない。

- **2024-10 · [Flash Inference: Near Linear Time Inference for Long Convolution Sequence Models and Beyond](2024-2410.12982-flash-inference-near-linear-time-inference-for-long-convolution-sequence.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い畳み込みの推論を、寄与をタイルへまとめて高速フーリエ変換で処理することで二乗時間から準線形時間へ落とす厳密な推論法で、Hyenaで位置混合110倍、全体7.8倍の高速化を示す研究。

- **2024-10 · [COrAL: Order-Agnostic Language Modeling for Efficient Iterative Refinement](2024-2410.09675-coral-order-agnostic-language-modeling-for-efficient-iterative-refinemen.md)**  
  実装：[✓](https://github.com/YuxiXie/COrAL) ・ リポジトリ内被引用：0  
  COrAL（Context-Wise Order-Agnostic Language Modeling）は、短い局所window内だけで生成順序を柔軟にし、前方の複数トークン予測と既出トークンの後方再構成を同じdecoder-onlyモデルへ学習させる方式である。

- **2024-10 · [Approximately Aligned Decoding](2024-2410.01103-approximately-aligned-decoding.md)**  
  実装：[✓](https://github.com/amazon-science/Approximately-Aligned-Decoding) ・ リポジトリ内被引用：0  
  Approximately Aligned Decoding（AprAD）は、大規模言語モデルの生成途中で禁止文字、構文違反、存在しないAPIの呼び出しなどを検出したとき、生成済み接頭辞をどこまで残して再開するかを投機的サンプリング（投機的 sampling）の受理・棄却計算で決める方式である。

- **2024-09 · [Sorbet: A Neuromorphic Hardware-Compatible Transformer-Based Spiking Language Model](2024-2409.15298-sorbet-a-neuromorphic-hardware-compatible-transformer-based-spiking-lang.md)**  
  実装：[✓](https://github.com/Kaiwen-Tang/Sorbet) ・ リポジトリ内被引用：0  
  ソフトマックスと層正規化をビットシフト演算へ置き換え、重みを1ビット化することで、ニューロモルフィックハードウェアへ載せられる初のTransformer型スパイキング言語モデルを実現し、エネルギー試算でBERT比27.16倍の削減を示した研究。

- **2024-09 · [Internalizing ASR with Implicit Chain of Thought for Efficient Speech-to-Speech Conversational LLM](2024-2409.17353-internalizing-asr-with-implicit-chain-of-thought-for-efficient-speech-to.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  音声入力から音声出力を生成する大規模言語モデルでは、音声を文字へ転写し、文字で回答を考え、再び音声へ変換する方式が使われる。RTX 3090を使った測定では、初回出力音声トークンの遅延が1.09秒から0.87秒へ低下した。

- **2024-09 · [Deploying Open-Source Large Language Models: A performance Analysis](2024-2409.14887-deploying-open-source-large-language-models-a-performance-analysis.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  vLLMでMistral系とLLaMA-3 70BをV100とA100の複数構成で実測し、同時リクエスト数とプロンプト長に対する100トークン生成時間を7構成分表にまとめ、Mixtral 8x7BではA100 2枚で総計最大約700トークン毎秒、A100 2枚で70B級が実用になるという配備目安を示した計測研究。

- **2024-08 · [Writing in the Margins: Better Inference Pattern for Long Context Retrieval](2024-2408.14906-writing-in-the-margins-better-inference-pattern-for-long-context-retriev.md)**  
  実装：[✓](https://github.com/writer/writing-in-the-margins) ・ リポジトリ内被引用：0  
  チャンク化プリフィルの各区間で質問関連部分を欄外メモとして抽出・分類し、残したメモだけを文脈末尾へ集約して再提示することで、中盤忘却を抑えて長文脈の多段推論と集約を改善するKVキャッシュ対応の推論パターン。

- **2024-08 · [QUITO: Accelerating Long-Context Reasoning through Query-Guided Context Compression](2024-2408.00274-quito-accelerating-long-context-reasoning-through-query-guided-context-c.md)**  
  実装：[✓](https://github.com/Wenshansilvia/attention_compressor) ・ リポジトリ内被引用：0  
  質問への応答開始を示すトリガートークンの注意分布で文脈中の語の重要度を測り予算内で残す文脈圧縮QUITOを提案し、2倍圧縮のNaturalQuestionsで正解率58.9%と、パープレキシティ基準の比較対象38.7から53.2%を上回った。

- **2024-08 · [Practical Token Pruning for Foundation Models in Few-shot Conversational Virtual Assistant Systems](2024-2408.11799-practical-token-pruning-for-foundation-models-in-few-shot-conversational.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意スコアから測る重要度で早い層1か所だけトークンを間引く学習不要の枝刈りと、設定を全タスク共通化する適応法で、文埋め込みモデルの推論を20〜34パーセント速くする実運用の報告。

- **2024-06 · [VcLLM: Video Codecs are Secretly Tensor Codecs](2024-2407.00467-vcllm-video-codecs-are-secretly-tensor-codecs.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルのメモリと通信の問題は重みだけではない。既存のGPTQやAWQは主に重み、1-bit Adamや1-bit LAMBは主に学習勾配を対象にしており、各テンソル種別に異なる圧縮手法を組み合わせる必要がある。原著は重み約25GBとKV約7.2GBを4つのメモリ約8GBの装置へ分割し、長文脈推論を成立させる構成を示す。

- **2024-06 · [Retaining Key Information under High Compression Ratios: Query-Guided Compressor for LLMs](2024-2406.02376-retaining-key-information-under-high-compression-ratios-query-guided-com.md)**  
  実装：[✓](https://github.com/DeepLearnXMU/QGC) ・ リポジトリ内被引用：0  
  問い合わせと文書を一緒に符号化し、関連度で重み付けしたnグラムプーリングと見直し層で重要情報を残す文脈圧縮器で、高い圧縮率でも質問応答の精度を保ち、圧縮率とスループットを従来の文脈圧縮より大きく改善する方式。

- **2024-06 · [On Efficient Language and Vision Assistants for Visually-Situated Natural Language Understanding: What Matters in Reading and Reasoning](2024-2406.11823-on-efficient-language-and-vision-assistants-for-visually-situated-natura.md)**  
  実装：[✓](https://github.com/naver-ai/elva) ・ リポジトリ内被引用：0  
  本論文は、視覚と言語を組み合わせた助手（Vision-Language Assistant; VLA）が文書画像を理解する際の推論資源を削減しながら、画像中の文字を読み取る精度を維持するためのモデル設計を調べる。

- **2024-06 · [Decoding with Limited Teacher Supervision Requires Understanding When to Trust the Teacher](2024-2406.18002-decoding-with-limited-teacher-supervision-requires-understanding-when-to.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  教師の助けを冒頭数トークンに限る条件で、信頼の重みを事例ごとに予測し、生徒のエントロピーが中間帯のときだけ知識を注入することで、小さなモデルの生成品質を一貫して上げるデコード法。

- **2024-05 · [SelfCP: Compressing Over-Limit Prompt via the Frozen Large Language Model Itself](2024-2405.17052-selfcp-compressing-over-limit-prompt-via-the-frozen-large-language-model.md)**  
  実装：[✓](https://github.com/jungao1106/SelfCP) ・ リポジトリ内被引用：0  
  凍結した対象モデル自身に超過分だけを12倍のメモリトークンへ圧縮させ、残りは無加工で読ませることで、学習可能パラメータ17Mのまま長文プロンプトの品質と処理可能量を回復する圧縮方式。

- **2024-05 · [Language-Specific Pruning for Efficient Reduction of Large Language Models](2024-f34641a221bb-language-specific-pruning-for-efficient-reduction-of-large-language-mode.md)**  
  実装：[✓](https://github.com/mshamrai/language-specific-pruning) ・ リポジトリ内被引用：0  
  枝刈りの較正データの言語がウクライナ語評価のパープレキシティを大きく左右することを、SparseGPTとWandaの比較で示し、英語較正では2:4スパース化が崩壊する一方、ウクライナ語較正なら50パーセント削減とメモリ約41パーセント減を両立できることを示した研究。

- **2024-05 · [DynaMo: Accelerating Language Model Inference with Dynamic Multi-Token Sampling](2024-2405.00888-dynamo-accelerating-language-model-inference-with-dynamic-multi-token-sa.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既存モデルの重みを流用した軽い学習で複数トークンを同時予測し、共起重みマスキングと適応的閾値で同時分布を整え信頼度に応じて出す個数を動的に変えるDynaMoで、同等品質のまま2.57倍の生成高速化を得る。

- **2024-05 · [Distributed Inference Performance Optimization for LLMs on CPUs](2024-2407.00029-distributed-inference-performance-optimization-for-llms-on-cpus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CPUだけの分散推論で、トークンIDのブロードキャスト、層あたり1回の同期、計算と通信の間のゼロコピーの三つにより通信を削り、Xeon 4台で72Bモデルをトークンあたり140ミリ秒で生成する実践報告。

- **2024-05 · [Basis Selection: Low-Rank Decomposition of Pretrained Large Language Models for Target Applications](2024-2405.15877-basis-selection-low-rank-decomposition-of-pretrained-large-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み行列のSVD基底の重要度を対象用途のデータで再学習してから剪定し、新規基底で損失を補うことで、深い圧縮率でも精度を保つ用途特化型の低ランク圧縮。

- **2024-04 · [LongVQ: Long Sequence Modeling with Vector Quantization on Structured Memory](2024-2404.11163-longvq-long-sequence-modeling-with-vector-quantization-on-structured-mem.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LongVQは、SSMの構造化長期記憶とベクトル量子化されたKeyによる固定長の注意を組み合わせ、系列長に対して線形時間で動作するハイブリッドモデルである。

- **2024-04 · [Large Language Model Inference Acceleration Based on Hybrid Model Branch Prediction](2024-f00175abf388-large-language-model-inference-acceleration-based-on-hybrid-model-branch.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的サンプリングの検証待ちを、分岐予測で受理トークン数を先読みして小モデルの次ラウンド生成と大モデルの検証を重ねることで隠し、無損失のまま投機的サンプリングを上回る速度を出す方式。

- **2024-04 · [HLSTransform: Energy-Efficient Llama 2 Inference on FPGAs Via High Level Synthesis](2024-2405.00738-hlstransform-energy-efficient-llama-2-inference-on-fpgas-via-high-level-.md)**  
  実装：[✓](https://github.com/HLSTransform/submission) ・ リポジトリ内被引用：0  
  Llama 2系の小規模モデルを高位合成と8ビット量子化でFPGAへ実装し、トークンあたりエネルギーをCPU比12.75分の1、GPU比8.25分の1へ下げながら、CPUの2.46倍の速度を保った省電力推論の実証。

- **2024-04 · [CQIL: Inference Latency Optimization with Concurrent Computation of Quasi-Independent Layers](2024-2404.06709-cqil-inference-latency-optimization-with-concurrent-computation-of-quasi.md)**  
  実装：[✓](https://github.com/Photooon/CQIL) ・ リポジトリ内被引用：0  
  隣接層の入力が似ていることを使い、中間の層の群に入力を共有させて複数計算機で同時計算し、注意出力を群内で回すバイパスで損失を補う方式で、三百三十億パラメータのモデルの遅延を最大四十八・三パーセント削減し、課題の平均得点の低下を約二ポイントに抑えたと報告した。

- **2024-03 · [IM-Unpack: Training and Inference with Arbitrarily Low Precision Integers](2024-2403.07339-im-unpack-training-and-inference-with-arbitrarily-low-precision-integers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  整数化自体は無害で低ビットへの制限だけが外れ値で壊れることを切り分け、大きな整数を行や列の桁分解で低ビット化して元の行列積と厳密に一致させ、七十億級モデルの線形層で膨張率約一・二七倍に抑えたと報告した。

- **2024-03 · [Efficient Encoder-Decoder Transformer Decoding for Decomposable Tasks](2024-2403.13112-efficient-encoder-decoder-transformer-decoding-for-decomposable-tasks.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来のプロンプト-in-Encoder（PIE）では、各項目の問いを入力文書と結合してencoderへ渡すため、入力を問いの数だけ再符号化し、cross-注意機構でも問いごとに異なるencoder表現を読み出す。

- **2024-02 · [User-LLM: Efficient LLM Contextualization with User Embeddings](2024-2402.13598-user-llm-efficient-llm-contextualization-with-user-embeddings.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  履歴を項目IDと属性IDの列として符号化し、小型の自己回帰型利用者エンコーダで密なベクトル列へ変換した後、LLMの中間層に交差注意（cross-注意機構）で取り込ませる。MovieLens 20M、Google Review、Amazon Reviewを用いた実験では、長い履歴を使うほど計算量削減が顕著になった。

- **2024-02 · [Institutional Platform for Secure Self-Service Large Language Model Exploration](2024-2402.00913-institutional-platform-for-secure-self-service-large-language-model-expl.md)**  
  実装：[✓](https://github.com/innovationcore/llmfactory) ・ リポジトリ内被引用：0  
  機関内向けに、データ管理から学習ジョブ管理、LoRAXによるマルチアダプタ推論までをセルフサービス化し、孤立した計算資源をCrescoのエージェント網で暗号化・テナント分離つきに束ねる安全なLLM基盤の構築報告。

- **2024-01 · [Infini-gram: Scaling Unbounded n-gram Language Models to a Trillion Tokens](2024-2401.17377-infini-gram-scaling-unbounded-n-gram-language-models-to-a-trillion-token.md)**  
  実装：[✓](https://github.com/liujch1998/infini-gram) ・ リポジトリ内被引用：0  
  従来のn-gram方式は直前の数トークンしか参照しないため、長い固有表現や定型句を扱いにくかった。

- **2023-12 · [Rethinking Compression: Reduced Order Modelling of Latent Features in Large Language Models](2023-2312.07046-rethinking-compression-reduced-order-modelling-of-latent-features-in-lar.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各層の出力特徴の主成分だけを残して重みを2つの低ランク行列へ再パラメータ化する、学習不要・CPUのみで実行できるLLM圧縮法。LLaMA-7Bの80%圧縮で調整済み構造化枝刈りを上回る。

- **2023-12 · [A Performance Evaluation of a Quantized Large Language Model on Various Smartphones](2023-2312.12472-a-performance-evaluation-of-a-quantized-large-language-model-on-various-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  対象はiPhone 14、14 Pro、14 Pro Max、15、15 Pro Maxの五機種で、llama.cppとGGUFを利用し、orcaminiv37Bを3bit small K-S量子化した約2.95GiBのモデルを使用する。

### 4年前（2022-12〜2023-11）

- **2023-08 · [YaRN: Efficient Context Window Extension of Large Language Models](2023-2309.00071-yarn-efficient-context-window-extension-of-large-language-models.md)**  
  実装：[✓](https://github.com/jquesnelle/yarn) ・ リポジトリ内被引用：148  
  大規模言語モデルの回転位置埋め込み（Rotary Position Embedding、RoPE）は、クエリとキーを位置に応じた角度だけ回転し、両者の内積が相対位置を反映するように設計される。128Kまでのパスキー検索では7B・13Bとも平均正答率99.4%を報告する。

- **2023-10 · [Ring Attention with Blockwise Transformers for Near-Infinite Context](2023-2310.01889-ring-attention-blockwise-transformers.md)**  
  実装：[✓](https://github.com/lhao499/llm_large_context) ・ リポジトリ内被引用：132  
  キー・値ブロックをリング転送しながらブロック注意計算を重畳し、系列長に依存しない活性化メモリで最大文脈長をデバイス数に比例して拡張する分散注意方式。

- **2023-04 · [Learning to Compress Prompts with Gist Tokens](2023-2304.08467-learning-to-compress-prompts-with-gist-tokens.md)**  
  実装：[✓](https://github.com/jayelm/gisting) ・ リポジトリ内被引用：113  
  指示の鍵・値状態をそのままキャッシュすれば再計算は減るものの、保持する状態の長さは指示トークン数に比例する。Jesse Muらの研究は、指示の意味を短い要旨トークン（gist トークン）の内部状態へ集約し、後続の異なる入力に再利用する「要旨化（gisting）」を提案する。

- **2023-07 · [In-context Autoencoder for Context Compression in a Large Language Model](2023-2307.06945-in-context-autoencoder-for-context-compression-in-a-large-language-model.md)**  
  実装：[✓](https://github.com/getao/icae) ・ リポジトリ内被引用：94  
  本論文は、大規模言語モデル（LLM）の長い入力文脈を、同じモデルがそのまま利用できる短い連続表現へ学習圧縮する文脈内自己符号化器（In-context Autoencoder、ICAE）を提案する。

- **2023-11 · [LLaMA-VID: An Image is Worth 2 Tokens in Large Language Models](2023-2311.17043-llama-vid-an-image-is-worth-2-tokens-in-large-language-models.md)**  
  実装：[✓](https://github.com/dvlab-research/LLaMA-VID) ・ リポジトリ内被引用：64  
  LLaMA-VIDは、各フレームの情報を質問に応じて抽出する文脈トークンと画像内容を要約する内容トークンに分離する。ECCV 2024正式論文では、動画質問応答のMSVD-QAでVicuna-7B構成が正解率69.7%、MSRVTT-QAで57.7%、ActivityNet-QAで47.4%を記録した。

- **2023-07 · [Hyena Hierarchy: Towards Larger Convolutional Language Models](2023-2302.10866-hyena-hierarchy-towards-larger-convolutional-language-models.md)**  
  実装：[✓](https://github.com/HazyResearch/safari) ・ リポジトリ内被引用：56  
  従来の線形注意や疎注意はこの費用を減らせる一方、長距離の連想記憶や文脈内での規則適用に必要な表現能力が不足し、密な注意層を混ぜないと大規模モデルの品質に届かない場合があった。著者らは、注意機構が持つ三つの性質、すなわち入力に応じて演算内容が変わること、系列長に対してパラメータ数が線形に増えないこと、任意の過去位置を参照できることに注目した。

- **2023-06 · [MiniLLM: On-Policy Distillation of Large Language Models](2023-2306.08543-minillm-on-policy-distillation-of-large-language-models.md)**  
  実装：[✓](https://github.com/microsoft/LMOps/tree/main/minillm) ・ リポジトリ内被引用：52  
  MiniLLMは、大規模な教師言語モデルから小規模な学生言語モデルへ生成能力を移す知識蒸留（Knowledge Distillation; KD）の学習方式である。

- **2023-07 · [Skeleton-of-Thought: Prompting LLMs for Efficient Parallel Generation](2023-2307.15337-skeleton-of-thought-prompting-llms-for-efficient-parallel-generation.md)**  
  実装：[✓](https://github.com/imagination-research/sot) ・ リポジトリ内被引用：41  
  Skeleton-of-Thought（SoT）はモデル内部の注意カーネルを変えず、回答を「骨格作成」と「各項目の独立展開」に分解して、後半を並列実行する。高速化の源泉は総トークン数を必ず減らすことではなく、長い1本の逐次デコードを複数の短いデコードへ分け、クリティカルパスを短くする点にある。

- **2023-07 · [Efficient Guided Generation for Large Language Models](2023-2307.09702-efficient-guided-generation-for-large-language-models.md)**  
  実装：[✓](https://github.com/dottxt-ai/outlines) ・ リポジトリ内被引用：27  
  従来方式は、各生成ステップで語彙中のN個のトークン文字列を照合し、現在の部分出力に続けてよいかを調べるため、制約判定が少なくとも語彙数に比例する。

- **2023-07 · [When Not to Trust Language Models: Investigating Effectiveness of Parametric and Non-Parametric Memories](2023-2212.10511-when-not-to-trust-language-models-investigating-effectiveness-of-paramet.md)**  
  実装：[✓](https://github.com/AlexTMallen/adaptive-retrieval) ・ リポジトリ内被引用：24  
  著者らは、質問の対象実体のウィキペディア閲覧数を人気度の代理指標として、質問の関係種別ごとに閾値を学習し、閾値未満の質問だけ外部文書を検索する適応的検索（適応的 Retrieval）を提案した。PopQAで最良の組合せは正答率46.5%となり、どの常時検索・検索なしの構成よりも5.3ポイント高いと報告する。

- **2023-10 · [RECOMP: Improving Retrieval-Augmented LMs with Compression and Selective Augmentation](2023-2310.04408-recomp-improving-retrieval-augmented-lms-with-compression-and-selective-.md)**  
  実装：[✓](https://github.com/carriex/recomp) ・ リポジトリ内被引用：21  
  Xu、Shi、ChoiによるRECOMPは、検索拡張言語モデル（Retrieval-Augmented Language モデル、RALM）の推論時に、検索した文書をそのままモデルの文脈へ連結する方式を改める。原著は文脈トークン数を主要な効率指標とするため、文書量が5%になったという数値をGPU実行時間が20倍速くなったと読み替えてはならない。

- **2023-10 · [MatFormer: Nested Transformer for Elastic Inference](2023-2310.07707-matformer-nested-transformer-for-elastic-inference.md)**  
  実装：[✓](https://github.com/devvrit/matformer) ・ リポジトリ内被引用：19  
  大規模言語モデルを配備する際、同じ品質・遅延・計算資源の要求を持つ利用者ばかりとは限らない。モデルを後から枝刈りして調整する方法では、新しいサイズごとに再学習や調整を要することもある。

- **2023-07 · [PUMA: Secure Inference of LLaMA-7B in Five Minutes](2023-2307.12533-puma-secure-inference-of-llama-7b-in-five-minutes.md)**  
  実装：[✓](https://github.com/secretflow/spu/tree/main/examples/python/ml/flax_llama7b) ・ リポジトリ内被引用：19  
  従来の高速化方式が必要としたモデルの再学習や構造変更を避け、既存の学習済み重みをほぼそのまま秘密計算へ持ち込むことを狙う。

- **2023-10 · [A Dynamic LLM-Powered Agent Network for Task-Oriented Agent Collaboration](2023-2310.02170-a-dynamic-llm-powered-agent-network-for-task-oriented-agent-collaboratio.md)**  
  実装：[✓](https://github.com/SALT-NLP/DyLAN) ・ リポジトリ内被引用：13  
  複数の大規模言語モデルエージェントを協調させる方式では、担当する役割や通信順序を固定すると、問題によっては不得意なエージェントの発言が増え、余計なモデル呼出しと品質低下を招く。原著のHumanEvalコード生成評価では、単一実行の正答率73.2%に対してDyLANは82.9%、平均モデルAPI呼出し数は16.85回だった。

- **2023-10 · [GEMINI: Fast Failure Recovery in Distributed Training with In-Memory Checkpoints](2023-075d73797107-gemini-fast-failure-recovery-in-distributed-training-with-in-memory-chec.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  保存頻度を増やせば故障前に失う学習進捗は減るが、遠隔ストレージの集約帯域が不足すると保存そのものが長くなり、学習を妨げる。提案は単なる「メモリへ保存する」という発想ではない。

- **2023-07 · [A Survey of Techniques for Optimizing Transformer Inference](2023-2307.07982-a-survey-of-techniques-for-optimizing-transformer-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  本論文は、Transformer推論を軽量化・高速化する手法を、モデルを作り直す方法から演算器の設計まで横断的に整理した43ページの文献調査である。例えばCoFiは引用元研究で約95%の疎性と約10倍の高速化を報告し、HMC-TranはV100のテンソルコアを利用するBERT-baseの92%疎性で3.68倍を報告する。

- **2023-01 · [Alternating Updates for Efficient Transformers](2023-2301.13310-alternating-updates-for-efficient-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  AltUp（Alternating Updates）は、表現の幅と層内部の演算幅を分離し、幅Kdの状態を保持しながら各層で実際にTransformerを通すのはd次元の部分ブロック一つに限る方式である。NeurIPS 2023採択論文のT5実験では、同じ予測精度を持つ密なTransformerに対して最大87%の相対速度向上を報告する。

- **2023-10 · [Look-Up mAI GeMM: Increasing AI GeMMs Performance by Nearly 2.5x via msGeMM](2023-2310.06178-look-up-mai-gemm-increasing-ai-gemms-performance-by-nearly-2-5x-via-msge.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  重みを4ビット整数へ量子化すれば、各重みが取れる値は16種類に限られる。約2.5倍という代表値を、現在のGPUにおける推論遅延やトークン生成速度の改善と解釈してはならない。

- **2023-09 · [Softmax Bias Correction for Quantized Generative Models](2023-2309.01729-softmax-bias-correction-for-quantized-generative-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ソフトマックスを8ビット量子化すると小さな確率がゼロへ丸められて確率の合計が崩れることを突き止め、そのずれを校正データで測って量子化のオフセットへ吸収することで、追加計算なしに量子化ソフトマックスの精度を回復する方式。

- **2023-09 · [Poster: PipeLLM: Pipeline LLM Inference on Heterogeneous Devices with Sequence Slicing](2023-4587313dce71-poster-pipellm-pipeline-llm-inference-on-heterogeneous-devices-with-sequ.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  手元の異種機器へLLMの層を能力に応じて配分し、入力シーケンスをトークン方向へスライスしてパイプラインに流すことで、疎なリクエストでも並列化して推論を速くするPipeLLM。

- **2023-07 · [Beyond Classical Attention: Quantum Attention for Scalable Computation](2023-2307.08045-beyond-classical-attention-quantum-attention-for-scalable-computation.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文は、長い入力系列に対する自己注意で全ての問い合わせと鍵の内積を計算する代わりに、閾値を超える少数の大きな内積だけを量子探索で発見する理論的な方法を提案する。

- **2023-06 · [Modular Transformers: Compressing Transformers into Modularized Layers for Flexible Efficient Inference](2023-2306.02379-modular-transformers-compressing-transformers-into-modularized-layers-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文の主題は、圧縮済みモデルを一種類だけ作るのではなく、一度の圧縮学習から異なる実行時予算に対応できる層構成を取り出すことである。

- **2023-01 · [AttMemo: Accelerating Self-Attention with Memoization on Big Memory Systems](2023-2301.09262-attmemo-accelerating-self-attention-with-memoization-on-big-memory-syste.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Transformerの自己注意（self-注意機構）は、入力系列内のトークン間関係を行列として計算する。BERT、RoBERTa、DeBERTa、GPT-2（いずれも約1億パラメータ）を48コアのXeon CPUとDRAM/Optaneの合計最大1.6TBメモリで測定し、著者は平均22%、最大68%の推論速度向上を報告する。

- **2023-11 · [Tessel: Boosting Distributed Execution of Large DNN Models via Flexible Schedule Search](2023-2311.15269-tessel-boosting-distributed-execution-of-large-dnn-models-via-flexible-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  演算子配置を入力に、繰り返し部分であるリピーテンドの構築と前後の時間最適な補完という二段階探索で分散実行スケジュールを自動生成し、学習で最大5.5倍、推論でも遅延とスループットの改善を得るスケジュール探索システム。

- **2023-09 · [Understanding the Impact of Post-Training Quantization on Large Language Models](2023-2309.05210-understanding-the-impact-of-post-training-quantization-on-large-language.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  量子化方式ごとに温度・生成長・topkへの生成品質の感度を6,300生成で実測した分析。4ビット量子化は温度に敏感で、方式の優劣はモデル系列で逆転する。

- **2023-08 · [Transformer Compression via Subspace Projection](2023-2308.16475-transformer-compression-via-subspace-projection.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  特徴行列の特異値分解から作った射影でTransformer全体を低次元部分空間へ移し、隠れ次元を直接削る圧縮法で、圧縮率44パーセントでも精度低下を最大1.6パーセントに抑える。

- **2023-07 · [INT-FP-QSim: Mixed Precision and Formats For Large Language Models and Vision Transformers](2023-2307.03712-int-fp-qsim-mixed-precision-and-formats-for-large-language-models-and-vi.md)**  
  実装：[✓](https://github.com/lightmatter-ai/INT-FP-QSim) ・ リポジトリ内被引用：0  
  整数と浮動小数点の量子化を一つのシミュレータで比べられるようにし、重み4ビット条件の横断調査で、ベクトル単位の適応スケーリングが全体キャリブレーションより大幅に精度を保ち、低ビット浮動小数点は整数に対して明確な利点がないことを示す研究。

- **2023-07 · [Efficient Latent Space Compression for Lightning-Fast Fine-Tuning and Inference of Transformer-Based Models](2023-400218b723db-efficient-latent-space-compression-for-lightning-fast-fine-tuning-and-in.md)**  
  実装：[✓](https://github.com/AlaFalaki/compressedBART) ・ リポジトリ内被引用：0  
  本論文は、既存のTransformer 符号化器が出力する各トークンの隠れ表現を、別途学習した自己符号化器（AE）で低次元に写像し、その低次元表現を入力として処理できる小型復号器を構築する手法を検討する。これは約2.2倍の速度、時間比で約54%の短縮に相当する。

- **2023-07 · [CA-LoRA: Adapting Existing LoRA for Compressed LLMs to Enable Efficient Multi-Tasking on Personal Devices](2023-2307.07705-ca-lora-adapting-existing-lora-for-compressed-llms-to-enable-efficient-m.md)**  
  実装：[✓](https://github.com/thunlp/CA-LoRA) ・ リポジトリ内被引用：0  
  CA-LoRAは非圧縮LLM上で学習済みのLoRAを圧縮モデルへ移植する際、元LoRAを初期値として継承し、非線形低ランクの回復モジュールを加え、非圧縮モデル＋LoRAを教師として蒸留する。T5-3Bを量子化・枝刈り・MoEficationで5.61GBから0.94GBへ圧縮した実験では、RTEが通常LoRAの82.9%からCA-LoRAの84.3%へ改善。

- **2023-05 · [NeuralMatrix: Moving Entire Neural Networks to General Matrix Multiplication for Efficient Inference](2023-2305.14405-neuralmatrix-moving-entire-neural-networks-to-general-matrix-multiplicat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  非線形演算を区分線形近似と区間判定の行列積へ置き換え、ネットワーク全体を一般行列積だけで実行することで、単一のGEMM加速器でCNN・Transformer・GNNを専用ASIC級の電力効率で動かす枠組み。

- **2023-05 · [Infor-Coef: Information Bottleneck-based Dynamic Token Downsampling for Compact and Efficient language model](2023-2305.12458-infor-coef-information-bottleneck-based-dynamic-token-downsampling-for-c.md)**  
  実装：[✓](https://github.com/twwwwx/Infor-Coef) ・ リポジトリ内被引用：0  
  Infor-Coefが扱うのは、BERTのモデル重みを固定比率で減らすだけでは、簡単な入力と難しい入力に同じ計算を割り当てるという問題である。BERT-base比で16.2倍という原著の代表値は、バッチ内最大長へpaddingしたときの推定FLOPs比である。

- **2023-05 · [Flover: A Temporal Fusion Framework for Efficient Autoregressive Model Parallel Inference](2023-2305.13484-flover-a-temporal-fusion-framework-for-efficient-autoregressive-model-pa.md)**  
  実装：[✓](https://github.com/YJHMITWEB/Flover) ・ リポジトリ内被引用：0  
  到着したリクエストを単一推論ストリームのイテレーション境界で融合し、終了分の孤立メモリを移動量最小のシャッフルで詰めることで、ポアソン到着でFasterTransformer比最大11.2倍、出力長ばらつき条件で6.8倍を達成した自己回帰モデル向け推論枠組み。

- **2023-05 · [Finding the Pillars of Strength for Multi-Head Attention](2023-2305.14380-finding-the-pillars-of-strength-for-multi-head-attention.md)**  
  実装：[✓](https://github.com/SenticNet/GHA) ・ リポジトリ内被引用：0  
  多頭注意のヘッドをグループ内同質化とグループ間多様化の自己教師あり制約で分け、各グループの代表ヘッドだけを投票で残すことで、パラメータを32.1パーセント削りながら翻訳と要約で通常のTransformerを上回る注意機構の冗長性削減。

- **2023-05 · [Diffusion Language Models Generation Can Be Halted Early](2023-2305.10818-diffusion-language-models-generation-can-be-halted-early.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散言語モデルの生成途中で予測分布が収束する現象を観測し、エントロピー・KL・トークン切替の基準で適応的に生成を止めることで、DDLMで約40%、SSDで10〜15%の生成時間削減を品質低下なしに得た早期停止の研究。

- **2023-05 · [Cheaply Evaluating Inference Efficiency Metrics for Autoregressive Transformer APIs](2023-2305.02440-cheaply-evaluating-inference-efficiency-metrics-for-autoregressive-trans.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  APIの生の実行時間は提供者の最適化と負荷変動に汚染されるため、推論時間をプロンプト長と出力トークン数の線形和としてモデル化し、統一環境での「理想化実行時間」を少数クエリの回帰で推定して、モデル自体の効率と能力の交換関係を初めて比較した研究。

- **2023-04 · [To Asymmetry and Beyond: Structured Pruning of Sequence to Sequence Models for Improved Inference Efficiency](2023-2304.02721-to-asymmetry-and-beyond-structured-pruning-of-sequence-to-sequence-model.md)**  
  実装：[✓](https://github.com/spacemanidol/Efficient-Web-Scale-Absractive-Summarization) ・ リポジトリ内被引用：0  
  要約向け系列変換モデルで、精度はエンコーダ・遅延はデコーダが支配するという非対称性を測り、デコーダ中心の構造化プルーニングで約3倍の推論高速化をROUGE-2約1ポイント低下で達成した研究。

- **2023-02 · [DISCO: Distributed Inference with Sparse Communications](2023-2302.11180-disco-distributed-inference-with-sparse-communications.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層内並列の分散推論で送る特徴の選択を重みの重要度による疎化へ変換して学習し、ResNet-50の2ノード推論で通信量を5分の1にしながら4.7倍の高速化と同等精度を両立する枠組み。

- **2023-02 · [Auto-Parallelizing Large Models with Rhino: A Systematic Approach on Production AI Platform](2023-2302.08141-auto-parallelizing-large-models-with-rhino-a-systematic-approach-on-prod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Rhinoは、単一デバイス向けに記述されたテンソル計算を、複数GPUへ自動分散する学習システムである。評価では、V100 32GBと100Gb RoCEのクラスタでGPTとGShard MoEを最大16GPUまで実行し、Alpa、Megatron/DeepSpeedと比較した。

- **2023-01 · [Pre-computed memory or on-the-fly encoding? A hybrid approach to retrieval augmentation makes the most of your compute](2023-2301.10448-pre-computed-memory-or-on-the-fly-encoding-a-hybrid-approach-to-retrieva.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検索パッセージの符号化の大半を事前計算メモリへ寄せ、残りの層だけ質問条件付きでその場で仕上げるLUMENにより、FiD並みの質問応答品質をずっと少ない演算で得る。

### 5年前（2021-12〜2022-11）

- **2022-06 · [DeepSpeed Inference: Enabling Efficient Inference of Transformer Models at Unprecedented Scale](2022-2207.00032-deepspeed-inference-enabling-efficient-inference-of-transformer-models-at-unprecedented-scale.md)**  
  実装：[✓](https://github.com/microsoft/DeepSpeed) ・ リポジトリ内被引用：213  
  単一の量子化方式や一種類の並列化を万能解とせず、GPU内実行向けのDeepSpeed Transformerと、CPU主記憶・NVMeを使うZeRO-Inferenceという二つの経路を組み合わせる。

- **2022-02 · [ST-MoE: Designing Stable and Transferable Sparse Expert Models](2022-2202.08906-st-moe-designing-stable-and-transferable-sparse-expert-models.md)**  
  実装：[✓](https://github.com/tensorflow/mesh/blob/master/mesh_tensorflow/transformer/moe.py) ・ リポジトリ内被引用：78  
  ST-MoEは専門家混合（Mixture-of-Experts、MoE）モデルを単に巨大化するのではなく、学習の発散を防ぎ、下流の多様な自然言語課題で密モデルを上回るための設計を検討する研究である。ただしこれはモデル全体をGPUメモリ12GBで動かせるという意味ではなく、専門家の重み配置と分散通信を含めた大規模学習システムの研究である。

- **2021-12 · [Self-attention Does Not Need O(n^2) Memory](2021-2112.05682-self-attention-does-not-need-o-n-2-memory.md)**  
  実装：[✓](https://github.com/google-research/google-research/tree/master/memory_efficient_attention) ・ リポジトリ内被引用：42  
  ソフトマックス注意の最大値、指数和、値の重み付き和を逐次更新し、全注意行列を実体化せず同じ数学的出力を得る。理論上の省メモリ算法と、TPU向けのチャンク並列実装、再計算を使った微分を示す。

- **2022-11 · [Iron: Private Inference on Transformers](2022-0ed2662d9eee-iron-private-inference-on-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：25  
  この構成では、サーバーは入力内容を読めるため、医療文書や企業機密をそのまま送信したくない利用者には問題がある。Ironはこの二つの律速点に特化した手順を設計する。従来の行列・ベクトル積を行ごとに繰り返す方式と比較し、一般の行列形状で出力行数の平方根程度の通信削減を理論的に示す。

- **2022-07 · [FNet: Mixing Tokens with Fourier Transforms](2022-2105.03824-fnet-mixing-tokens-with-fourier-transforms.md)**  
  実装：[✓](https://github.com/google-research/google-research/tree/master/f_net) ・ リポジトリ内被引用：25  
  標準的な変換器（Transformer）の自己注意（self-注意機構）は、入力系列内のトークン間の重みを入力内容に応じて計算する。特にこの論文の「学習80%高速化」は約1.8倍の処理速度を意味し、処理時間が80%減ったという意味ではない。

- **2022-02 · [Competition-Level Code Generation with AlphaCode](2022-2203.07814-competition-level-code-generation-with-alphacode.md)**  
  実装：✓ ・ リポジトリ内被引用：24  
  AlphaCodeは、自然言語で与えられた競技プログラミング問題から、正しい実行プログラムを見つけるための生成・探索・選別システムである。評価では2021年12月のCodeforcesの10大会を後から模擬し、各問題最大10提出という条件で、参加者中の順位が平均して上位54.3%に相当した。

- **2022-04 · [Step-unrolled Denoising Autoencoders for Text Generation](2022-2112.06749-step-unrolled-denoising-autoencoders-for-text-generation.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  大規模言語モデルの典型的な自己回帰生成は、先行トークンが確定してから次トークンを計算する。注意演算の内部を高速化しても、長い出力を作るにはトークン数にほぼ比例した生成ステップが必要になる。最初はランダムなトークン列を用意し、各反復で全体の整合性を改善して最終文を得る。しかし生成中のモデルが自分で作った中間文は、人工的なランダム破損文と同じ分布ではない。

- **2022-08 · [Unified Normalization for Accelerating and Stabilizing Transformers](2022-2208.01313-unified-normalization-for-accelerating-and-stabilizing-transformers.md)**  
  実装：[✓](https://github.com/hikvision-research/Unified-Normalization) ・ リポジトリ内被引用：2  
  UNはTransformerのオフライン 正規化を、活性値/勾配統計の平滑化と適応型 外れ値除去で安定化し、固定統計を線形層へ融合してSwin-Tで31.2% スループット向上を示す。

- **2022-11 · [DBA: Efficient Transformer With Dynamic Bilinear Low-Rank Attention](2022-2211.16368-dba-efficient-transformer-with-dynamic-bilinear-low-rank-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  DBA（動的 Bilinear Low-Rank 注意機構）は、通常のTransformer注意計算における系列長nと特徴次元dの二つの大きさを同時に小さくする方式である。長さ4,096のbyte-level text分類では通常Transformerに対する相対速度6.1倍、ピークメモリ比0.09を報告する。

- **2022-10 · [QuaLA-MiniLM: a Quantized Length Adaptive MiniLM](2022-2210.17114-quala-minilm-a-quantized-length-adaptive-minilm.md)**  
  実装：[✓](https://github.com/intel/intel-extension-for-transformers/tree/main/examples/huggingface/pytorch/question-answering/dynamic) ・ リポジトリ内被引用：0  
  MiniLMv2の自己注意関係蒸留、層別トークン削減と復元、INT8事後量子化を統合し、SQuAD1.1の質問応答でBERT-base比8.8倍のCPU推論高速化をF1低下約0.90ポイントで達成した研究。

- **2022-09 · [SAMP: A Model Inference Toolkit of Post-Training Quantization for Text Processing via Self-Adaptive Mixed-Precision](2022-2209.09130-samp-a-model-inference-toolkit-of-post-training-quantization-for-text-pr.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意を浮動小数点に残し全結合だけを量子化するモードを含む混合精度の組み合わせを、精度劣化を考慮する配分アルゴリズムで自動推奨し、カーネル融合と合わせてBERT系テキスト処理の推論をFasterTransformer比最大1.15倍まで速くする学習後量子化のツールキット。

- **2022-03 · [DTQAtten: Leveraging Dynamic Token-based Quantization for Efficient Attention Architecture](2022-51ecca33c669-dtqatten-leveraging-dynamic-token-based-quantization-for-efficient-atten.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークン重要度に応じて0／4／8ビットへ動的に振り分ける混合精度量子化と、同精度トークンの並べ替えでストールを消す可変速シストリックアレイを一体設計し、精度を保ったまま注意計算を高速化する。

- **2022-01 · [Fast Monte-Carlo Approximation of the Attention Mechanism](2022-2201.12854-fast-monte-carlo-approximation-of-the-attention-mechanism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Transformerの注意機構では、各入力位置が他の位置へどれだけ注意を向けるかを表す重みを計算し、その重みに基づいて値ベクトルを集約する。BERT、DistilBERT、Longformerに適用した実験では、GLUEの分類・類似度評価で精度をおおむね維持しつつ注意演算の計算量を大幅に減らせると報告する。

- **2022-01 · [Continual Transformers: Redundancy-Free Attention for Online Inference](2022-2201.06268-continual-transformers-redundancy-free-attention-for-online-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  過去分の注意の部分結果をキャッシュして新しいトークンとの差分だけを更新する形へ注意計算を書き換え、出力と重みを完全に保ったままオンライン推論の1予測あたり演算を最大63倍削減した、無損失な継続型Transformerエンコーダ。

### 6年前（2020-12〜2021-11）

- **2021-04 · [Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM](2021-2104.04473-efficient-large-scale-language-model-training-on-gpu-clusters-using-mega.md)**  
  実装：[✓](https://github.com/NVIDIA/Megatron-LM) ・ リポジトリ内被引用：111  
  本論文は、巨大言語モデルの学習を数千基のGPUへ拡張するとき、メモリ容量、層内の集合通信、パイプラインの空泡、ノード間転送の重複が性能を制限する問題を扱う。パイプラインでは前向きと後向きを交互に処理する1F1Bを使い、さらに一つのGPUに複数の離れたモデル片を割り当てて空泡を短くする。

- **2021-10 · [8-bit Optimizers via Block-wise Quantization](2021-2110.02861-8-bit-optimizers-via-block-wise-quantization.md)**  
  実装：[✓](https://github.com/bitsandbytes-foundation/bitsandbytes) ・ リポジトリ内被引用：23  
  Dettmersらは、この状態を8ビットへ縮めても32ビット版に近い学習品質を維持する方式を提案した。原著表1では1.5Bパラメータ言語モデルで32ビットAdamと8ビットAdamの困惑度がともに9.0で、後者は8.5GBのGPUメモリを節約した。

- **2021-03 · [Softermax: Hardware/Software Co-Design of an Efficient Softmax for Transformers](2021-2103.09301-softermax-hardware-software-co-design-of-an-efficient-softmax-for-transf.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  Transformerの自己注意機構では、クエリとキーの積から得た各スコアをsoftmaxで正規化し、値ベクトルへの重みを生成する。原著のTSMC 7nm設計評価では、非正規化部の面積0.25倍・エネルギー0.10倍、正規化部の面積0.65倍・エネルギー0.39倍、MAC等を含む演算器全体の面積0.90倍・エネルギー0.43倍を報告する。

- **2020-12 · [MiniLMv2: Multi-Head Self-Attention Relation Distillation for Compressing Pretrained Transformers](2020-2012.15828-minilmv2-multi-head-self-attention-relation-distillation-for-compressing.md)**  
  実装：[✓](https://github.com/microsoft/unilm/tree/master/minilm) ・ リポジトリ内被引用：17  
  教師と生徒の注意頭数を揃える制約を外し、Query・Key・Valueのトークン間関係を共通の「関係頭」で比較する。推論速度の改善は蒸留後の小型モデルによるもので、実行時に教師を参照する方式ではない。

- **2021-11 · [SimpleTRON: Simple Transformer with O(N) Complexity](2021-2111.15588-simpletron-simple-transformer-with-o-n-complexity.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Transformerの標準自己注意は、系列長L、各ヘッド次元dに対してQKᵀのL×L行列を作り、その各行をsoftmax正規化してVと掛ける。これにより過去の各位置との類似度を直接計算できるが、系列長に対して時間・中間注意行列のサイズが二乗で増える。各ヘッドについて、標準のsoftmax(QKᵀ/√d)Vを、Q(KᵀV)/√Lに置き換える。

- **2021-05 · [EL-Attention: Memory Efficient Lossless Attention for Generation](2021-2105.04779-el-attention-memory-efficient-lossless-attention-for-generation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  クエリだけを広げキーとバリューは隠れ状態を共有してマルチヘッド注意と同一結果を返す無損失注意で、保存量を96分の1へ減らし生成を最大5.3倍速くする。

- **2021-04 · [TPrune](2021-a15e1294d14f-tprune.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Transformerの各行列の削れやすさをブロック単位のスパース学習で分析し、スケール不変な正則化による行単位枝刈りで、モバイル実機でBLEU低下なしの1.21倍から最大1.92倍の高速化を示す枝刈りパイプライン。

### 7年前（2019-12〜2020-11）

- **2020-07 · [FTRANS: Energy-Efficient Acceleration of Transformers using FPGA](2020-2007.08563-ftrans-energy-efficient-acceleration-of-transformers-using-fpga.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  FTRANSは、Transformerの重み行列を拡張ブロック循環行列（enhanced block-circulant matrix; BCM）に置き換える構造化圧縮と、その圧縮表現を直接計算する再構成可能論理回路（field-programmable gate array; FPGA）の専用構成を同時設計した研究である。

- **2020-02 · [Compressing Large-Scale Transformer-Based Models: A Case Study on BERT](2020-2002.11985-compressing-large-scale-transformer-based-models-a-case-study-on-bert.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  量子化で重みを小さくする方法、不要な重みや構造を削る方法、大きな教師モデルから小さな生徒モデルへ知識を移す方法など、圧縮の選択肢は多い。

- **2020-06 · [Funnel-Transformer: Filtering out Sequential Redundancy for Efficient Language Processing](2020-2006.03236-funnel-transformer-filtering-out-sequential-redundancy-for-efficient-lan.md)**  
  実装：[✓](https://github.com/laiguokun/Funnel-Transformer) ・ リポジトリ内被引用：12  
  Funnel-Transformerは、すべての変換器層で入力トークン数と同じ長さの隠れ状態を維持することが、系列全体を一つの表現へ要約する分類・ランキング課題では冗長であるという着想から生まれた。これにより、出力長は短くしながら圧縮前の情報全体を参照できる。

- **2020-04 · [Lite Transformer with Long-Short Range Attention](2020-2004.11886-lite-transformer-with-long-short-range-attention.md)**  
  実装：[✓](https://github.com/mit-han-lab/lite-transformer) ・ リポジトリ内被引用：12  
  Lite Transformerは、短い文章を処理する翻訳・要約・言語モデルを、限られた計算予算の端末で実行するためのモデル構造を提案したICLR 2020論文である。

- **2020-06 · [Multi-Head Attention: Collaborate Instead of Concatenate](2020-2006.16362-multi-head-attention-collaborate-instead-of-concatenate.md)**  
  実装：[✓](https://github.com/epfml/collaborative-attention) ・ リポジトリ内被引用：9  
  標準的な多頭注意（Multi-Head 注意機構、MHA）は、複数の注意ヘッドに独立したクエリ射影とキー射影を与え、それぞれが計算した値を連結して出力する。単層のV100測定では設定次第で推論時間が2.28ミリ秒から1.75ミリ秒へ短縮した。

- **2020-05 · [IntelliCode Compose: Code Generation using Transformer](2020-2005.08025-intellicode-compose-code-generation-using-transformer.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  IntelliCode Composeは、統合開発環境（IDE）で入力途中のプログラムから一行規模の補完候補を提示するクラウド型のコード生成システムである。ただし編集類似度は84.1%から78.0%へ下がる。

- **2020-06 · [$O(n)$ Connections are Expressive Enough: Universal Approximability of Sparse Transformers](2020-2006.04862-o-n-connections-are-expressive-enough-universal-approximability-of-spars.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  通常のTransformerの自己注意は、系列中の各トークンが他の全トークンを参照するため、系列長nに対して注意得点の組合せがnの二乗で増える。長文を処理する際に接続を減らす疎注意は計算量を減らす候補だが、接続を取り除くことでモデルが表現できる関数の種類まで狭まるのかは自明ではない。

- **2020-09 · [Efficient Sparse Collective Communication and its application to Accelerate Distributed Deep Learning](2020-e4ac6d84ba9c-efficient-sparse-collective-communication-and-its-application-to-acceler.md)**  
  実装：[✓](https://github.com/sands-lab/omnireduce) ・ リポジトリ内被引用：2  
  この集団通信（collective 通信）は計算機を増やすほど相対的に重くなり、特に多数の埋め込み表を持つモデルではゼロ要素の転送が無駄になる。各ワーカーが次の非ゼロブロックの位置を通知するため、集約器は全ワーカーの進行を調整し、誰も値を持たない領域を安全に飛ばせる。

- **2020-10 · [AxFormer: Accuracy-driven Approximation of Transformers for Faster, Smaller and more Accurate NLP Models](2020-2010.03688-axformer-accuracy-driven-approximation-of-transformers-for-faster-smalle.md)**  
  実装：[✓](https://github.com/amrnag/Specialized-Transformers) ・ リポジトリ内被引用：1  
  微調整済みTransformerについて、検証損失を実際に下げる要素だけを階層的に枝刈りし、効く層だけ注意を上位K件へ絞ることで、再学習なしに精度・速度・サイズを同時に改善するタスク特化型の近似計算フレームワーク。

- **2020-08 · [ConvBERT: Improving BERT with Span-based Dynamic Convolution](2020-2008.02496-convbert-improving-bert-with-span-based-dynamic-convolution.md)**  
  実装：[✓](https://github.com/yitu-opensource/ConvBert) ・ リポジトリ内被引用：0  
  BERTの多頭自己注意は、すべてのヘッドで全トークン対の関係を計算する。しかし自然言語では局所的な構文・語彙の結び付きが重要であり、実際に多くのヘッドの注意行列は対角線付近へ集中する。遠方トークンをほとんど参照しないヘッドでも、全系列の二次元注意行列を構築するのは計算上の無駄である。

### 8年前（2018-12〜2019-11）

- **2019-09 · [Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism](2019-1909.08053-megatron-lm-training-multi-billion-parameter-language-models-using-model.md)**  
  実装：[✓](https://github.com/NVIDIA/Megatron-LM) ・ リポジトリ内被引用：396  
  この論文の対象は、巨大な言語モデルの学習時に、モデル重み・勾配・最適化器状態が単一GPUのメモリに収まらない問題である。従来のモデル全体を別の言語や専用コンパイラで書き直す方法とは異なり、PyTorchの既存Transformer実装へ少数の集約通信を挿入する設計である。

- **2019-04 · [Mask-Predict: Parallel Decoding of Conditional Masked Language Models](2019-1904.09324-mask-predict-parallel-decoding-of-conditional-masked-language-models.md)**  
  実装：[✓](https://github.com/facebookresearch/Mask-Predict) ・ リポジトリ内被引用：20  
  翻訳文の長さを最初に予測し、最初の反復では全位置を同時に予測する。2019年の機械翻訳実験では、WMT14英語→ドイツ語において基礎CMLMの10反復が27.03 BLEU、同等規模の自己回帰Transformerが27.74 BLEUとなった。

- **2019-07 · [Large Memory Layers with Product Keys](2019-1907.05242-large-memory-layers-with-product-keys.md)**  
  実装：[✓](https://github.com/facebookresearch/XLM) ・ リポジトリ内被引用：15  
  本論文の積キー記憶層（Product Key メモリ; PKM）は、二つの部分キー集合の直積で巨大なキー集合を暗黙的に作り、各部分集合の上位候補だけを調べて全積キー集合に対する正確な上位選択を行う。検索結果に対応する少数の値ベクトルだけを読み出して加重和を計算するため、総パラメータ容量と活性計算量を分離できる。

- **2019-11 · [Mask-Predict: Parallel Decoding of Conditional Masked Language Models](2019-0bc18ef37a7d-mask-predict-parallel-decoding-of-conditional-masked-language-models.md)**  
  実装：[✓](https://github.com/facebookresearch/Mask-Predict) ・ リポジトリ内被引用：11  
  翻訳文全体を毎回捨てる反復改良方式とは異なり、高信頼の語を固定して低信頼位置へ文脈を提供する点が中心的な設計である。

- **2019-03 · [Supporting Very Large Models using Automatic Dataflow Graph Partitioning](2019-1807.08887-supporting-very-large-models-using-automatic-dataflow-graph-partitioning.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  Tofuは、単一のGPUのメモリ容量を超えるニューラルネットワークを、プログラムを書き換えず複数GPUで学習できるようにする自動モデル並列化システムである。

### 9年前（2017-12〜2018-11）

- **2018-11 · [GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism](2018-1811.06965-gpipe-efficient-training-of-giant-neural-networks-using-pipeline-paralle.md)**  
  実装：[✓](https://github.com/tensorflow/lingvo/blob/master/lingvo/core/gpipe.py) ・ リポジトリ内被引用：120  
  GPipeは、単一のGPUやTPUに収まらないニューラルネットワークを、層の連続区間ごとに複数の装置へ分割して学習する方式である。実際に学習した557百万パラメータのAmoebaNetはImageNet-2012の上位1件正解率84.4%、60億パラメータ・128層の多言語Transformerは102言語対で個別の二言語モデルを上回った。

- **2018-06 · [PipeDream: Generalized Pipeline Parallelism for DNN Training](2018-1806.03377-pipedream-generalized-pipeline-parallelism-for-dnn-training.md)**  
  実装：✓ ・ リポジトリ内被引用：97  
  DNNの連続層を複数GPUへ割り当て、異なるミニバッチの順伝播と逆伝播を交互に重ねる。層の計算・通信費用を測って段を自動分割し、順伝播時の重み版を逆伝播まで保持することで非同期実行の整合性を保つ。

- **2018-02 · [Horovod: fast and easy distributed deep learning in TensorFlow](2018-1802.05799-horovod-fast-and-easy-distributed-deep-learning-in-tensorflow.md)**  
  実装：[✓](https://github.com/uber/horovod) ・ リポジトリ内被引用：22  
  GPU数を増やすと勾配転送と集約のために通信が集中し、著者らの128 GPU試験では、計算資源のほぼ半分を効率的に使えていなかった。提案の価値は通信アルゴリズムだけではない。

- **2018-02 · [Deterministic Non-Autoregressive Neural Sequence Modeling by Iterative Refinement](2018-1802.06901-deterministic-non-autoregressive-neural-sequence-modeling-by-iterative-r.md)**  
  実装：[✓](https://github.com/nyu-dl/dl4mt-nonauto) ・ リポジトリ内被引用：19  
  本研究は、出力系列を左から右へ一語ずつ生成する自己回帰モデルの逐次依存を取り除き、系列全体を同時に予測した後、少数回の反復で文章を修正する決定論的な非自己回帰系列生成法を提案する。

### 10年前（2016-12〜2017-11）

- **2017-01 · [Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](2017-1701.06538-outrageously-large-neural-networks-the-sparsely-gated-mixture-of-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：395  
  本論文は、ニューラルネットワークの総パラメータ数を増やすと各入力での計算量も増えるという密なモデルの制約を、入力ごとに一部の専門家だけを実行する条件付き計算によって緩和した基礎研究である。モデルの総容量を大きくしても、活性化する専門家数を固定すれば入力一件あたりの専門家演算量はほぼ一定にできる。ただし専門家を増やすだけでは高速にならない。
<!-- survey:auto:end -->
