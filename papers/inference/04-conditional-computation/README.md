# Conditional Computation

入力やtokenの難しさに応じて、**実行するlayer数、処理するtoken数、終了位置などを変え、不要な計算を最初から行わない**研究をまとめる。全tokenが全layerを必ず通る通常の実行を崩し、layer skipping、early exit、token pruningなどで計算量を減らす。

MoEのexpert数を変えるAdaptive Expert Computationとは対象が異なり、この系統では主にTransformer本体の実行深度や処理対象tokenを動的に変える。

<!-- survey:auto:start -->
## 自動生成の論文一覧（41本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/04-conditional-computation/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

該当なし。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [Do Dynamic Routers Need Memory? HeRo: History-Aware Routing for Efficient LLM Inference](2026-2609.08189-hero-history-aware-routing-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各層の局所状態だけでなく過去のゲート選択と残差変化を線形注意メモリへ蓄積し、Llama 3.1-8Bで26.87%のパラメータ計算を回避しつつ密モデル比100.24%の性能を保つ動的FFNルーティング。

- **2026-05 · [VideoRouter: Query-Adaptive Dual Routing for Efficient Long-Video Understanding](2026-2605.05848-videorouter-query-adaptive-dual-routing-for-efficient-long-video-underst.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  VideoRouterは、固定の視覚トークン予算を「広く浅く」か「重要な場面へ厚く」かに配分する方式を質問ごとに決める。

- **2026-01 · [ChunkWise LoRA: Adaptive Sequence Partitioning for Memory-Efficient Low-Rank Adaptation and Accelerated LLM Inference](2026-2601.21109-chunkwise-lora-adaptive-sequence-partitioning-for-memory-efficient-low-r.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低ランク適応（LoRA）は、事前学習済みの重みを固定し、少数の低ランク行列を追加学習することで、モデルの更新費用を抑える。原著表Iでは、LLaMA-7Bを用いた比較で、通常のモデルが22.5ms/トークン、ピークGPUメモリ14.6GBに対し、提案方式は14.9ms/トークン、9.1GBを報告する。

- **2025-12 · [Mixture of Attention Schemes (MoAS): Learning to Route Between MHA, GQA, and MQA](2025-2512.20650-mixture-of-attention-schemes-moas-learning-to-route-between-mha-gqa-and-.md)**  
  実装：[✓](https://github.com/Esmail-ibraheem/Mixture-of-Attention-Schemes-MoAS) ・ リポジトリ内被引用：0  
  標準の多頭注意（Multi-Head 注意機構; MHA）は各問い合わせ頭に独立したキー・バリュー（Key-Value; KV）頭を持ち、表現力が高い一方、生成時のKVキャッシュが大きくなる。これは条件付き計算の可能性を示す探索的結果であって、LLM推論の実用的高速化を実証した結果ではない。

- **2025-11 · [Conv-Basis: A New Paradigm for Efficient Attention Inference and Gradient Computation in Transformers](2025-a7d4659aa00f-conv-basis-a-new-paradigm-for-efficient-attention-inference-and-gradient.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案方式は、相対位置差に沿った対角線状の反復パターンを「畳み込み基底（conv basis）」として表し、各基底に対応する畳み込みとVの積を高速フーリエ変換（Fast Fourier Transform; FFT）で計算する。

### 2年前（2024-11〜2025-10）

- **2025-04 · [Dynamic Early Exit in Reasoning Models](2025-2504.15895-dynamic-early-exit-in-reasoning-models.md)**  
  実装：[✓](https://github.com/iie-ycx/DEER) ・ リポジトリ内被引用：21  
  DEERは推論途中で最終回答を試し、自己評価の確信度が高ければ思考連鎖を終了し、低ければ元地点から続行する。追加学習なしで過剰な再検討を減らす。

- **2024-12 · [D-LLM: A Token Adaptive Computing Resource Allocation Strategy for Large Language Models](2024-d-llm-a-token-adaptive-computing-resource-allocation-strategy-for-large-language.md)**  
  実装：[✓](https://github.com/Jyk-122/D-LLM) ・ リポジトリ内被引用：7  
  D-LLMは、大規模言語モデルのすべてのトークンに同じ層数の計算を行う必要はないという観点から、各トークン・各Transformer層でその層を実行するか省略するかを学習する動的深度方式である。代表的な設定では、完全な層を実行するLoRA基準の約52～59%の浮動小数点演算量で、多くの課題の品質を維持した。

- **2025-07 · [DiffSkip: Differential Layer Skipping in Large Language Models](2025-diffskip-differential-layer-skipping-in-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  大規模言語モデルは、次の単語を推測するたびに、難しい計算を要する単語にも文脈からほぼ写すだけの単語にも同じ数の変換層を適用する。DiffSkipは、トークンと層の組ごとに、後続のフィードフォワードネットワーク（FFN）を実行するか、軽量な補正器で代替するかを判断する手法である。

- **2025-03 · [Adaptive Layer-skipping in Pre-trained LLMs](2025-2503.23798-adaptive-layer-skipping-in-pre-trained-llms.md)**  
  実装：[✓](https://github.com/luoxuan-cs/Flexidepth) ・ リポジトリ内被引用：4  
  FlexiDepthは、すでに学習された大規模言語モデルの重みを変更せず、出力トークンごとに必要な層の計算量を変える手法である。原著のLlama-3-8B-Instruct（32層）では、平均8層を省いても6つの評価課題における平均性能保持率が100.7%となり、固定層省略方式より高い品質を示す。

- **2024-11 · [SparseInfer: Training-free Prediction of Activation Sparsity for Fast LLM Inference](2024-2411.12692-sparseinfer-training-free-prediction-of-activation-sparsity-for-fast-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  大規模言語モデルの逐次生成では、要求ごとの同時処理数が小さいと、フィードフォワード網の大きな重み行列をGPUメモリから読み出す費用が律速になる。入力によってゼロになる中間活性を事前に予測できれば、その活性に対応する行の重み読込みと行列ベクトル積を省略できる。しかし、一般的なLLaMAの滑らかな活性化関数であるSiLUでは、負の値も厳密にはゼロになりにくい。

- **2025-08 · [ILRe: Intermediate Layer Retrieval for Context Compression in Causal Language Models](2025-2508.17892-ilre-intermediate-layer-retrieval-for-context-compression-in-causal-lang.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Intermediate 層 Retrieval（ILRe）は、長大な入力を全層へそのまま通す代わりに、選択した中間デコーダ層までの処理で原文から重要トークンを選び直し、短いプロンプトとして再投入する文脈圧縮方式である。

- **2025-05 · [Beyond Hard and Soft: Hybrid Context Compression for Balancing Local and Global Information Retention](2025-2505.15774-beyond-hard-and-soft-hybrid-context-compression-for-balancing-local-and-.md)**  
  実装：[✓](https://github.com/Xnhyacinth/HyCo2) ・ リポジトリ内被引用：1  
  HyCo2（Hybrid Context Compression）は、長文脈の検索拡張生成（Retrieval-Augmented Generation; RAG）で、必要な情報を保持しながら入力トークン数を減らす圧縮方式である。デフォルトでは16個の潜在クエリと、原文トークンの上位10%を保持する設定である。

- **2025-03 · [Position-Aware Depth Decay Decoding (D³): Boosting Large Language Model Inference Efficiency](2025-2503.08524-position-aware-depth-decay-decoding-boosting-large-language-model-inference-effi.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  位置考慮型深さ減衰復号（Position-Aware 深度減衰 デコード; D³）は、大規模言語モデルの自己回帰生成で、出力トークンの位置に応じて実行するTransformer層数を減らす方式である。

- **2025-02 · [Infinite Retrieval: Attention Enhanced LLMs in Long-Context Processing](2025-2502.12962-infinite-retrieval-attention-enhanced-llms-in-long-context-processing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単純な窓移動では古い区間を忘れ、KVキャッシュ圧縮では過去情報の一部を固定された埋め込み表現として保存するため、質問に必要な文を失うことがある。

### 3年前（2023-11〜2024-10）

- **2024-08 · [LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding](2024-layerskip-enabling-early-exit-inference-and-self-speculative-decoding.md)**  
  実装：[✓](https://github.com/facebookresearch/LayerSkip) ・ リポジトリ内被引用：112  
  LayerSkipは、大規模言語モデルの全ての層を毎トークン実行する代わりに、浅い層から次トークンを予測できるよう学習し、その予測を同じモデルの残りの層で検証する方式である。下書きモデルの生成結果を大きなモデルで一括検証することで生成時間を短縮できるが、二つのモデルの重みや鍵・値キャッシュを管理する必要がある。

- **2024-06 · [D2O: Dynamic Discriminative Operations for Efficient Long-Context Inference of Large Language Models](2024-2406.13035-d2o-dynamic-discriminative-operations-for-efficient-long-context-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：34  
  全層へ同じKVキャッシュ量を与えず、プリフィル時の注意密度から浅い層へ大きく、深い層へ小さく予算を配る。さらに追い出し候補を永久削除せず、保持トークンとの類似度を再判定して情報を重み付き統合する。学習なしで長文品質を保ちつつ、フルKVキャッシュ比で最大3.04倍のスループットを示す。

- **2024-07 · [LazyLLM: Dynamic Token Pruning for Efficient Long Context LLM Inference](2024-2407.14057-lazyllm-dynamic-token-pruning-for-efficient-long-context-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：29  
  LazyLLMは、長い入力文のすべてのトークンを全変換層で計算する慣行を改め、現在予測しようとしている次のトークンに重要な入力部分だけを深い層へ進める推論時の計算削減法である。

- **2024-08 · [Training-Free Activation Sparsity in Large Language Models](2024-2408.14690-training-free-activation-sparsity-in-large-language-models.md)**  
  実装：[✓](https://github.com/FasterDecoding/TEAL) ・ リポジトリ内被引用：20  
  隠れ状態の小振幅成分を層別にゼロ化し、対応重みチャネルを読まない専用カーネルで、追加学習なしに40〜50%のモデル全体活性疎性と最大1.8倍のデコード高速化を実現する。

- **2024-06 · [Turbo Sparse: Achieving LLM SOTA Performance with Minimal Activated Parameters](2024-2406.05955-turbo-sparse-achieving-llm-sota-performance-with-minimal-activated-parameters.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  SwiGLUのゲート側だけでなくup射影側にもReLUを掛ける二重ReLU（dReLU）へ置換し、継続事前学習で性能を回復する。Mistral-7BはFFNの約90%、Mixtral-47Bは専門家ルーティング込みで約97%を非活性化し、PowerInfer系の疎実行で2〜5倍のデコード高速化を報告する。

- **2024-03 · [Not All Layers of LLMs Are Necessary During Inference](2024-2403.02181-not-all-layers-of-llms-are-necessary-during-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  本論文は、デコーダ専用大規模言語モデルの各入力を必ず最終層まで通すことによる過剰計算を、入力単位の早期終了で減らすAdaInferを提案する。原著第3版の主評価では、Llama 2の7B・13BとOPT-13Bで層削減率は課題により約9〜43%、平均17.8%となる。

- **2023-11 · [Learning to Skip for Language Modeling](2023-2311.15436-learning-to-skip-for-language-modeling.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  モデルを深くすれば表現容量は増えるが、トークン当たりの行列演算と復号遅延も増える。提案するSkipLayerは各層を二値ルータで包み、トークンの現在の隠れ表現から「この層を実行する」か「入力をそのまま次層へ渡す」かを選ぶ。

- **2024-10 · [MoH: Multi-Head Attention as Mixture-of-Head Attention](2024-2410.11842-moh-mixture-of-head-attention.md)**  
  実装：[✓](https://github.com/SkyworkAI/MoH) ・ リポジトリ内被引用：6  
  注意ヘッドを共有ヘッドとTop-Kルーティングヘッドに分け、トークンごとに必要なヘッドだけ使うMoH。LLaMA3-8Bで75%利用・14評価平均64.0%を達成。

- **2024-06 · [DEED: Dynamic Early Exit on Decoder for Accelerating Encoder-Decoder Transformer Models](2024-2311.08623-deed-dynamic-early-exit-on-decoder-for-accelerating-encoder-decoder-tran.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  浅い層の表現を深い層の状態としてそのままコピーする従来の停止・コピー方式は、層間の意味表現の違いを無視して精度を損なう。正式版のT5-large・SQuADでは、総遅延が221.9msから57.6ms（約74.0%短縮）、F1が92.1から91.6となった。

- **2024-10 · [MoDification: Mixture of Depths Made Easy](2024-2410.14268-modification-mixture-of-depths-made-easy.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoDificationは、既存の大規模言語モデル（Large Language モデル; LLM）を、各トークンに必要な層の計算だけを実行する深さの混合（Mixture of Depths; MoD）方式へ変換する研究である。

- **2024-05 · [Switchable Decision: Dynamic Neural Generation Networks](2024-2405.04513-switchable-decision-dynamic-neural-generation-networks.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  問題設定。事前学習したTransformerを軽量化する一般的な方法は、枝刈り、量子化、知識蒸留などによって固定された小型モデルを作る。

### 4年前（2022-11〜2023-10）

- **2023-10 · [LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression](2023-2310.06839-longllmlingua-accelerating-and-enhancing-llms-in-long-context-scenarios-.md)**  
  実装：[✓](https://aka.ms/LongLLMLingua) ・ リポジトリ内被引用：59  
  LongLLMLinguaは、長いプロンプトを単に一律に切り詰めるのではなく、「質問に対してどの文書・トークンが有用か」を小型言語モデルで推定し、重要部分へトークン予算を集中させる長文脈プロンプト圧縮法である。

- **2023-10 · [Compressing Context to Enhance Inference Efficiency of Large Language Models](2023-2310.06201-compressing-context-to-enhance-inference-efficiency-of-large-language-mo.md)**  
  実装：[✓](https://github.com/liyucheng09/Selective_Context) ・ リポジトリ内被引用：54  
  長い文書や会話を大規模言語モデル（LLM）へ入力すると、初回入力処理と鍵・値キャッシュに多くの時間・メモリが必要になる。Selective Contextは、下流モデルの構造や重みを変更する代わりに、入力文脈に含まれる予測しやすい語句を事前に削り、残った自然言語テキストだけを渡す。

- **2023-07 · [SkipDecode: Autoregressive Skip Decoding with Batching and Caching for Efficient LLM Inference](2023-2307.02628-skipdecode-autoregressive-skip-decoding-with-batching-and-caching-for-efficient-.md)**  
  実装：✓ ・ リポジトリ内被引用：32  
  トークンごとに途中で処理を終了する早期終了（early exit）は計算を減らせるが、従来の方式をそのまま実際の配信へ持ち込むと、二つの問題が生じる。原著は2023年のプレプリントで、OPT-1.3BとOPT-6.7Bを使い、構造化情報からの文章生成、短文要約、ニュース要約で目標2～5倍の高速化設定を比較した。

- **2023-10 · [ReLU Strikes Back: Exploiting Activation Sparsity in Large Language Models](2024-2310.04564-relu-strikes-back-exploiting-activation-sparsity-in-large-language-model.md)**  
  実装：✓ ・ リポジトリ内被引用：24  
  大規模言語モデルは推論時に膨大な重みを読み出す。特に小さなバッチでの一トークンずつの生成では、演算器のピーク性能より高帯域メモリからの重み移動が制約になることが多い。滑らかな活性化関数であるSiLUやGELUは、負の入力でも通常は厳密なゼロを出さないため、出力が小さくても対応する重みの読み出しを機械的に省略しにくい。

- **2023-07 · [MovieChat: From Dense Token to Sparse Memory for Long Video Understanding](2023-2307.16449-moviechat-from-dense-token-to-sparse-memory-for-long-video-understanding.md)**  
  実装：[✓](https://github.com/rese1f/MovieChat) ・ リポジトリ内被引用：14  
  MovieChatは、固定長の短期記憶を逐次更新し、古いフレームを類似度に応じて統合した長期記憶へ送ることで、この問題を扱う。原著図1は、224×224画素のフレームを標本抽出なしで処理する視覚側の条件で、24GB GPU上で10,000フレーム超を扱えると報告する。

- **2023-05 · [Let's Sample Step by Step: Adaptive-Consistency for Efficient Reasoning and Coding with LLMs](2023-2305.11860-let-s-sample-step-by-step-adaptive-consistency-for-efficient-reasoning-a.md)**  
  実装：[✓](https://sample-step-by-step.info) ・ リポジトリ内被引用：13  
  大規模言語モデル（LLM）で多段階推論の精度を上げる自己整合性（自己整合性）は、同じ質問に対して複数の思考連鎖を標本化し、最終回答を多数決する方式である。最大7.9倍の節約は個別条件の値であり、全条件平均ではない。

- **2023-03 · [CoLT5: Faster Long-Range Transformers with Conditional Computation](2023-2303.09752-colt5-faster-long-range-transformers-with-conditional-computation.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  軽量経路を全トークン、高容量の注意・MLPを学習ルータが選ぶ少数トークンだけへ適用し、16k入力でLongT5比35〜75%の学習高速化・50〜100%の推論高速化を示す。

- **2023-10 · [Sparse Universal Transformer](2023-2310.07096-sparse-universal-transformer.md)**  
  実装：[✓](https://github.com/shawntan/SUT) ・ リポジトリ内被引用：9  
  Sparse Universal Transformer（SUT）は、同じTransformerブロックを複数回反復するユニバーサルTransformer（Universal Transformer; UT）の長所を残しながら、反復計算を疎な専門家選択と動的停止で削減するモデルである。通常のTransformerは各層に別の重みを持つ。

### 5年前（2021-11〜2022-10）

- **2022-08 · [Learned Token Pruning for Transformers](2022-2107.00910-learned-token-pruning-for-transformers.md)**  
  実装：[✓](https://github.com/kssteven418/LTP) ・ リポジトリ内被引用：14  
  この論文の対象は、入力文の全トークンを全Transformer層で処理するために生じる推論計算量である。一次資料としてKDD 2022の原論文に加え、筆頭著者が2023年に公表した同方式の31ページの学位論文（UC Berkeley EECS-2023-119）の方法・評価・議論を参照した。

- **2022-03 · [Transformer Feed-Forward Layers Build Predictions by Promoting Concepts in the Vocabulary Space](2022-2203.14680-transformer-feed-forward-layers-build-predictions-by-promoting-concepts-.md)**  
  実装：[✓](https://github.com/aviclu/ffn-values) ・ リポジトリ内被引用：5  
  Transformerの順伝播層（feed-順伝播 network、FFN）は、自己注意層で得た表現を更新するが、どのような内部操作が次トークンの予測を形作るかは分かりにくい。本論文は、FFNが出力するベクトルを、個々の値ベクトルに入力依存の係数を掛けた小さな加算成分の和として分解し、各成分が語彙中のどのトークンを押し上げるかを調べる。

- **2022-03 · [Pyramid-BERT: Reducing Complexity via Successive Core-set based Token Selection](2022-2203.14380-pyramid-bert-reducing-complexity-via-successive-core-set-based-token-sel.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案するPyramid-BERTは、各エンコーダ層の間で代表的なトークン表現の部分集合を選び、層が深くなるにつれて系列長を減らす。BERT-baseを用いたGLUEの開発集合では、推論時間を約3倍高速化する系列長構成で、原型の平均81.5に対して提案手法の最良設定が80.0を記録した。

### 6年前（2020-11〜2021-10）

- **2021-10 · [Magic Pyramid: Accelerating Inference with Early Exiting and Token Pruning](2021-2111.00230-magic-pyramid-accelerating-inference-with-early-exiting-and-token-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  文章分類器BERTの推論で、後続層へ運ぶトークン数を減らす枝刈りと、十分に確信できた入力の層処理を途中終了する機構を組み合わせる。入力長により得意条件が異なる二つの削減方法を重ね、五つの分類課題で演算量と精度の交換条件を評価した研究。表に示す4.95倍や8.25倍は浮動小数点演算量から計算した削減倍率であり、GPUの実時間高速化をそのまま意味しない。

### 7年前（2019-11〜2020-10）

- **2020-04 · [DeeBERT: Dynamic Early Exiting for Accelerating BERT Inference](2020-2004.12993-deebert-dynamic-early-exiting-for-accelerating-bert-inference.md)**  
  実装：[✓](https://github.com/castorini/DeeBERT) ・ リポジトリ内被引用：43  
  DeeBERTは、BERT系の分類モデルで入力ごとに必要なTransformer層数が異なることを利用し、浅い層ですでに十分確信度の高い予測が得られた例を途中で返す動的早期終了（動的 early exiting）方式である。

- **2020-06 · [BERT Loses Patience: Fast and Robust Inference with Early Exit](2020-2006.04152-bert-loses-patience-fast-and-robust-inference-with-early-exit.md)**  
  実装：✓ ・ リポジトリ内被引用：34  
  浅い層で正しい分類がほぼ確定している入力にも後段層の計算を続けるため、不要な遅延が生じる。従来の早期終了方式は中間分類器の最大確率やエントロピーなど、一つの層での自信の強さを停止信号にすることが多かった。

- **2020-04 · [FastBERT: a Self-distilling BERT with Adaptive Inference Time](2020-2004.02178-fastbert-a-self-distilling-bert-with-adaptive-inference-time.md)**  
  実装：[✓](https://github.com/autoliuweijie/FastBERT) ・ リポジトリ内被引用：33  
  この設計は文章生成の各トークンを省略する方式ではなく、主に文章分類と文対照合に適用される。例えば中国語THUCNewsでは閾値0.1で分類精度96.71%を維持しつつ計算量が約6.05分の1、英語DBpediaでは同閾値で99.31%から99.28%への微小な低下と引き換えに約10.57分の1となる。

- **2020-01 · [PoWER-BERT: Accelerating BERT Inference via Progressive Word-vector Elimination](2020-2001.08950-power-bert-accelerating-bert-inference-via-progressive-word-vector-elimi.md)**  
  実装：[✓](https://github.com/IBM/PoWER-BERT) ・ リポジトリ内被引用：12  
  方式は二つの判断を分離する。原著のK80 GPU、Keras、バッチ128（RACEのみ32）の評価では、BERTBASE比で各課題2.0～4.5倍の推論時間短縮を報告する。
<!-- survey:auto:end -->
