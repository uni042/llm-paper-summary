# Speculative Decoding / MoE

Speculative decodingで1回のtarget LLM実行から複数tokenを確定し、逐次decodeのweight読出し・latencyを減らす研究をまとめる。draft model、追加head、feature予測、retrieval、Jacobi iterationなどの候補生成方式と、tree verificationを含む。

MoEではさらに、検証するtokenやbranchが増えるほど呼び出すexpert数や重み転送量も増えやすいため、受理されそうなdraftだけを選ぶ、必要expertを先読みする、GPU常駐expertを優先する等の研究も含める。

<!-- survey:auto:start -->
## 自動生成の論文一覧（17本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2025-11 · [MoE-SpeQ: Speculative Quantized Decoding with Proactive Expert Prefetching and Offloading for Mixture-of-Experts](2025-2511.14102-moe-speq-speculative-quantized-decoding-with-proactive-expert-prefetching-and-of.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  MoE-SpeQは、対象MoEの4ビット版を下書きにして候補トークンと専門家経路を先に予測し、必要重みを検証前に読み込み、圧縮カーネルで転送と計算の待ちを減らす。

- **2025-10 · [SP-MoE: Speculative Decoding and Prefetching for Accelerating MoE-based Model Inference](2025-2510.10302-sp-moe-speculative-decoding-and-prefetching-for-accelerating-moe-based-model-inf.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  SP-MoEは、下書き生成中に対象MoEが次に使う専門家を予測し、CPUからGPUへ重みを非同期先読みして、検証時の専門家転送待ちを隠す。

- **2026-02 · [MoE-Spec: Expert Budgeting for Efficient Speculative Decoding](2026-2602.16052-moe-spec-expert-budgeting-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  MoE-Specは、候補木全体のルータ確率を層ごとに合算して専門家を予算B個へ絞り、各枝をその集合内で再選択して、木の拡大による検証重み読出しを抑える。

- **2026-02 · [MoE-SpAc: Efficient MoE Inference Based on Speculative Activation Utility in Heterogeneous Edge Scenarios](2026-2603.09983-moe-spac-efficient-moe-inference-based-on-speculative-activation-utility-in-hete.md)**  
  実装：[✓](https://github.com/lshAlgorithm/MoE-SpAc) ・ リポジトリ内被引用：2  
  MoE-SpAcは、投機的復号で先に見える専門家需要を集計し、VRAMに残す専門家・先読みする重み・CPUで計算する専門家を制約付きで同時に配置して、端末の転送待ちを減らす。

- **2026-07 · [Less Experts, Faster Decoding: Cost-Aware Speculative Decoding for Mixture-of-Experts](2026-2607.12696-less-experts-faster-decoding-cost-aware-speculative-decoding-for-mixture-of-expe.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  EcoSpecは、各下書き枝の受理確率と新規専門家数を比較し、既に使う重みを再利用できる枝を優先して、MoE検証のHBM読み出しと実行量を減らす。

- **2026-05 · [Making Every Verified Token Count: Adaptive Verification for MoE Speculative Decoding](2026-2605.00342-making-every-verified-token-count-adaptive-verification-for-moe-speculative-deco.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  適応的検証は、下書き木の各枝の受理見込みと追加される専門家・検証時間を測り、費用対効果の低い枝を捨てて、MoEの検証計算と重み読出しを減らす。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Osprey: Target-agnostic Pre-training Makes Stronger Drafters in Speculative Decoding](2026-2609.09338-osprey-target-agnostic-pretraining-speculative-decoding.md)**  
  実装：[✓](https://github.com/LeanModels/Osprey) ・ リポジトリ内被引用：0  
  Ospreyは、汎用ウェブで事前学習した浅いドラフト骨格を複数ターゲットへ転用し、ターゲット固有蒸留の初期値を改善して分野外でも受理トークンを増やし、検証回数を減らす。

- **2026-08 · [Vision Is Not Overhead: One-Pass Block Drafting for Lossless Speculative Decoding in Vision-Language Models](2026-2609.00355-glance-vlm-speculative-decoding.md)**  
  実装：[✓](https://github.com/js-lee-AI/GLANCE。実運用比較はSGLang) ・ リポジトリ内被引用：0  
  GLANCEは、VLMの視覚・言語融合状態から未来トークン塊を1回で下書きし、幅広い候補木を対象モデルで一括検証して、画像根拠付き生成の逐次下書き処理を減らす。

- **2026-08 · [AcceptMoE: Commitment-Weighted Self-Sizing Verifier Expert Sets for Efficient MoE Speculative Decoding](2026-2608.02989-acceptmoe-commitment-weighted-self-sizing-verifier-expert-sets-for-efficient-moe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AcceptMoEは、下書き枝の受理見込みとルータ寄与を重み付けし、層ごとの検証専門家集合を縮めて、オフロード時のホストからGPUへの転送量を削る近似方式。

- **2026-07 · [DraftExpert: Expansion-Aware Self-Speculative Decoding for End-Device MoE Inference](2026-2607.24434-draftexpert-expansion-aware-self-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DraftExpertは、各MoE層に小型の常駐専門家を追加して候補を作り、専門家展開量を予測した枝打ちと非同期先読みを行い、端末の専門家搬送待ちを減らす。

- **2026-05 · [SPECTRE: Hybrid Ordinary-Parallel Speculative Serving for Resource-Efficient LLM Inference](2026-2605.08151-spectre-hybrid-ordinary-parallel-speculative-serving.md)**  
  実装：[✓](https://github.com/sgl-project/sglang/pull/22272) ・ リポジトリ内被引用：0  
  SPECTREは、余った小型モデルGPUを遠隔下書き器として大型モデルの検証に再利用し、下書きと検証を直列・並列の間で切り替えて、通信待ちとロールバックを抑える。

- **2026-05 · [An Interpretable Latency Model for Speculative Decoding in LLM Serving](2026-2605.15051-interpretable-latency-model-speculative-decoding-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号の遅延モデルは、Littleの法則で実効バッチを推定し、下書き・検証の固定費と負荷依存費を分けて測定して、要求率に応じた下書き長の選択境界を明らかにする。

### 1年以上前

- **2024-01 · [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](2024-2401.10774-medusa-multiple-decoding-heads.md)**  
  実装：[✓](https://github.com/FasterDecoding/Medusa) ・ リポジトリ内被引用：24  
  Medusaは、対象LLMの隠れ状態に未来位置ごとの小型予測ヘッドを追加し、上位候補を木構造へまとめて一括検証することで、別ドラフトモデルを置かず対象モデルの逐次呼出しを減らす。

- **2024-01 · [EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](2024-2401.15077-eagle-feature-speculative-sampling.md)**  
  実装：[✓](https://github.com/SafeAILab/EAGLE) ・ リポジトリ内被引用：23  
  EAGLEは、対象LLMの上位層特徴量と直前に標本化したトークンを小型デコーダへ与えて未来特徴量を予測し、元の言語モデル出力ヘッドと木構造検証で重み読出し回数を減らす。

- **2023-05 · [SpecInfer: Accelerating Generative Large Language Model Serving with Tree-based Speculative Inference and Verification](2023-2305.09781-specinfer-tree-speculative-inference.md)**  
  実装：[✓](https://github.com/flexflow/FlexFlow) ・ リポジトリ内被引用：17  
  SpecInferは、小型モデル群が先に作る複数候補を共通接頭辞の木へまとめ、対象LLMを1回で木構造検証することで、逐次デコードの対象重み読出しとGPU間通信を減らし、複数トークンを確定する。

- **2024-02 · [Break the Sequential Dependency of LLM Inference Using Lookahead Decoding](2024-2402.02057-lookahead-decoding.md)**  
  実装：[✓](https://github.com/hao-ai-lab/LookaheadDecoding) ・ リポジトリ内被引用：7  
  先読みデコードは、対象LLMを未来位置へ並列反復して途中の正しい短いトークン列を蓄積し、現在接頭辞に合う候補を一括検証して、追加モデルなしに逐次ステップとメモリ帯域待ちを減らす。

- **2023-11 · [REST: Retrieval-Based Speculative Decoding](2023-2311.08252-rest-retrieval-speculative-decoding.md)**  
  実装：[✓](https://github.com/FasterDecoding/REST) ・ リポジトリ内被引用：3  
  RESTは、現在文脈末尾と一致する過去トークン列を接尾辞索引から検索し、その続き候補を木構造へ集約して対象LLMで一括検証し、ドラフトモデルなしで反復的なコードの対象重み読出しを減らす。
<!-- survey:auto:end -->
