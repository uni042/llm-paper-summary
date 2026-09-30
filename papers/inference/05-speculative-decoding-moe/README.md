# Speculative Decoding / MoE

Speculative decodingで1回のtarget LLM実行から複数tokenを確定し、逐次decodeのweight読出し・latencyを減らす研究をまとめる。draft model、追加head、feature予測、retrieval、Jacobi iterationなどの候補生成方式と、tree verificationを含む。

MoEではさらに、検証するtokenやbranchが増えるほど呼び出すexpert数や重み転送量も増えやすいため、受理されそうなdraftだけを選ぶ、必要expertを先読みする、GPU常駐expertを優先する等の研究も含める。

<!-- survey:auto:start -->
## 自動生成の論文一覧（93本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-02 · [DFlash: Block Diffusion for Flash Speculative Decoding](2026-2602.06036-dflash-block-diffusion-for-flash-speculative-decoding.md)**  
  実装：[✓](https://github.com/z-lab/dflash) ・ リポジトリ内被引用：14  
  target hidden featuresで条件付けしたblock-diffusion drafterが候補列を1回で並列生成し、投機下書き自身の逐次待ちを除くDFlash。

- **2025-11 · [MoE-SpeQ: Speculative Quantized Decoding with Proactive Expert Prefetching and Offloading for Mixture-of-Experts](2025-2511.14102-moe-speq-speculative-quantized-decoding-with-proactive-expert-prefetching-and-of.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  MoE-SpeQは、対象MoEの4ビット版を下書きにして候補トークンと専門家経路を先に予測し、必要重みを検証前に読み込み、圧縮カーネルで転送と計算の待ちを減らす。

- **2026-07 · [DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation](2026-2607.05147-dspark-confidence-scheduled-speculative-decoding.md)**  
  実装：[✓](https://github.com/deepseek-ai/DeepSpec) ・ リポジトリ内被引用：8  
  並列ドラフトの後半受理率低下を軽量な逐次ヘッドで抑え、較正した接頭辞生存確率と実機処理能力から検証長を負荷適応で配分し、実トラフィックで同等処理能力時のユーザー当たり生成速度を57〜85%改善する。

- **2026-02 · [MoE-Spec: Expert Budgeting for Efficient Speculative Decoding](2026-2602.16052-moe-spec-expert-budgeting-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  MoE-Specは、候補木全体のルータ確率を層ごとに合算して専門家を予算B個へ絞り、各枝をその集合内で再選択して、木の拡大による検証重み読出しを抑える。

- **2026-05 · [Domino: Decoupling Causal Modeling from Autoregressive Drafting in Speculative Decoding](2026-2605.29707-domino-speculative-decoding.md)**  
  実装：[✓](https://github.com/jianuo-huang/Domino) ・ リポジトリ内被引用：6  
  並列ドラフトが弱めるトークン間の依存を、軽量GRUと低ランク補正で戻す投機的デコード方式。Qwen3評価では受理長と生成速度を改善したが、要旨の最大5.8倍は本文表の条件と対応づけられない。

- **2026-01 · [TALON: Confidence-Aware Speculative Decoding with Adaptive Token Trees](2026-2601.07353-talon-confidence-aware-speculative-decoding-with-adaptive-draft-length.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  投機木の形をあらかじめ「幅10・深さ8」のように固定すると、簡単な箇所では深さが足りず、難しい箇所では大量の枝を作って捨てる。TALONは総ノード数だけを固定し、ドラフトモデルの確信度に応じて予算を深さと幅へその場で配分する。

- **2025-12 · [Speculative Decoding: Performance or Illusion?](2026-2601.11580-speculative-decoding-performance-or-illusion.md)**  
  実装：[✓](https://github.com/orgs/SpecDecode-Bench/repositories) ・ リポジトリ内被引用：5  
  実運用向けvLLMで主要投機的復号を横断評価し、検証支配・バッチ依存・受理変動と理論上限との差を定量化。

- **2026-06 · [DFlare: Scaling Up Draft Capacity for Block Diffusion Speculative Decoding](2026-2606.02091-dflare.md)**  
  実装：[✓](https://github.com/Tencent/AngelSlim) ・ リポジトリ内被引用：4  
  ブロック拡散ドラフトの各層へ異なる標的層混合を注入し、ドラフト深さ・標的知識・学習データを拡張して受理長と実時間高速化を伸ばす。

- **2026-05 · [ECHO: Elastic Speculative Decoding with Sparse Gating for High-Concurrency Scenarios](2026-2604.09603-echo.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  高同時実行時の投機的デコードを固定検証予算の配分問題として扱い、信頼度の高い深さだけで候補木を伸縮し、バッチ内要求間で予算を再配分するSGLang統合方式。

- **2026-04 · [Self-Speculative Decoding for On-device MoE Acceleration](2025-self-speculative-decoding-for-on-device-moe-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  少数の経路選択専門家だけで同じMoE自身をドラフト化し、GPUを専門家キャッシュとして生成・検証間で再利用することで、CPU退避を伴う端末MoE復号を最大3.72倍高速化する。

- **2026-02 · [MoE-SpAc: Efficient MoE Inference Based on Speculative Activation Utility in Heterogeneous Edge Scenarios](2026-2603.09983-moe-spac-efficient-moe-inference-based-on-speculative-activation-utility-in-hete.md)**  
  実装：[✓](https://github.com/lshAlgorithm/MoE-SpAc) ・ リポジトリ内被引用：4  
  MoE-SpAcは、投機的復号で先に見える専門家需要を集計し、VRAMに残す専門家・先読みする重み・CPUで計算する専門家を制約付きで同時に配置して、端末の転送待ちを減らす。

- **2025-11 · [DSD: A Distributed Speculative Decoding Solution for Edge-Cloud Agile Large Model Serving](2025-2511.21669-dsd-distributed-edge-cloud-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  端末側下書きモデルとクラウド側目標モデルによる分散投機的復号をDSD-Simでモデル化し、学習型の適応窓制御で投機窓幅を調整して処理量を最大9.7%向上する。

- **2026-05 · [Draft Less, Retrieve More: Hybrid Tree Construction for Speculative Decoding](2026-2605.20104-draft-less-retrieve-more-hybrid-tree-construction-for-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  動的剪定は投機木を速くするが、剪定した枝の中に本来受理できる候補があれば平均受理長が落ちる。Graftは剪定で空いた候補枠を捨てず、対象モデルの過去検証から得た安価な検索候補で「接ぎ木」する。対象モデルが一度に検証するノード総数は増やさず、ドラフト計算だけを安い検索へ置換する。

- **2026-05 · [D-PACE: Dynamic Position-Aware Cross-Entropy for Parallel Speculative Drafting](2026-2605.18810-d-pace.md)**  
  実装：[✓](https://github.com/Lucas-TY/D-PACE) ・ リポジトリ内被引用：3  
  並列投機ドラフタで、受理接頭辞長への位置別寄与から交差エントロピー重みを毎例動的に計算し、固定位置減衰より受理長と実測高速化を改善する。

- **2026-04 · [Accelerating Speculative Decoding with Block Diffusion Draft Trees](2026-2604.12989-accelerating-speculative-decoding-with-block-diffusion-draft-trees.md)**  
  実装：[✓](https://github.com/liranringel/ddtree) ・ リポジトリ内被引用：3  
  DFlashが1回で得た位置別確率分布から高確率な複数接頭辞をDDTreeとして組み、1回の対象モデル検証で複数経路を試して単一路径投機より受理長と速度を高める。

- **2026-07 · [AngelSpec: Towards Real-World High Performance Inference with Speculative Decoding](2026-2607.25852-angelspec.md)**  
  実装：[✓](https://github.com/Tencent/AngelSpec) ・ リポジトリ内被引用：2  
  会話には短い多トークン予測、コード・数学には並列草稿DFlyを使い分け、実行時負荷に応じて検証深度も動的調整する推測デコード基盤。

- **2026-05 · [PipeSD: An Efficient Cloud-Edge Collaborative Pipeline Inference Framework with Speculative Decoding](2026-2605.13319-pipesd.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  投機的復号は小型モデルが複数トークンを先に提案し、大型モデルがまとめて検証することで自己回帰生成を高速化する。

- **2026-05 · [Draft-OPD: On-Policy Distillation for Speculative Draft Models](2026-2605.29343-draft-opd.md)**  
  実装：[✓](https://github.com/haodilei/Draft-OPD) ・ リポジトリ内被引用：2  
  投機的復号の検証で露出したドラフト誤り位置から提案を再生し、教師分布でオンポリシー蒸留することで受理長と無損失推論速度を高める。

- **2026-03 · [Speculative Speculative Decoding](2026-2603.03251-speculative-speculative-decoding.md)**  
  実装：[✓](https://github.com/tanishqkumar/ssd) ・ リポジトリ内被引用：2  
  検証中に受理長と補正トークンを複数予測し、その各結果に続く次ラウンドのドラフトを別GPUで先行生成することで、投機的デコードに残るドラフト待ちを隠す方式。

- **2026-01 · [WISP: Waste- and Interference-Suppressed Distributed Speculative LLM Serving at the Edge via Dynamic Drafting and SLO-Aware Batching](2026-2601.11652-wisp-distributed-speculative-serving-edge.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  WISPは、エッジで最初の棄却位置を予測して下書きを止め、サーバーでSLO余裕と検証時間から異種要求をバッチ分離し、無駄計算と干渉を減らす。

- **2026-08 · [S2-MoE: Enabling Efficient Self-Speculative Decoding for Mixture-of-Experts on Edge Devices](2026-2608.15018-s2-moe-self-speculative-decoding-edge.md)**  
  実装：[✓](https://github.com/angerybob/S2-MoE) ・ リポジトリ内被引用：1  
  エッジ向けMoEで、専門家再利用を考慮した投機展開・ゲーティング・文脈共有を組み合わせ、専門家読み出しを抑えながら自己投機的復号を高速化する。

- **2026-07 · [SpecExtend: A Drop-in Enhancement for Speculative Decoding of Long Sequences](2026-specextend.md)**  
  実装：[✓](https://github.com/jycha98/SpecExtend) ・ リポジトリ内被引用：1  
  対象モデルの注意重みでドラフト側KVキャッシュの重要文脈を動的選択し、再学習なしで長文の投機的復号を高速化する拡張。

- **2026-07 · [Less Experts, Faster Decoding: Cost-Aware Speculative Decoding for Mixture-of-Experts](2026-2607.12696-less-experts-faster-decoding-cost-aware-speculative-decoding-for-mixture-of-expe.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  EcoSpecは、各下書き枝の受理確率と新規専門家数を比較し、既に使う重みを再利用できる枝を優先して、MoE検証のHBM読み出しと実行量を減らす。

- **2026-07 · [D-cut: Adaptive Verification Depth Pruning for Batched Speculative Decoding](2026-2607.14647-d-cut-adaptive-verification-depth-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号は小さなドラフト器が複数トークンを先に提案し、大きな対象モデルがまとめて検証することで逐次実行回数を減らす。高並行条件では長ドラフト基準の自己回帰復号比平均高速化率1.26倍を1.65倍へ引き上げ、30個のモデル・課題組合せ中29個で改善した。

- **2026-05 · [SPECTRE: Hybrid Ordinary-Parallel Speculative Serving for Resource-Efficient LLM Inference](2026-2605.08151-spectre-hybrid-ordinary-parallel-speculative-serving.md)**  
  実装：[✓](https://github.com/sgl-project/sglang/pull/22272) ・ リポジトリ内被引用：1  
  SPECTREは、余った小型モデルGPUを遠隔下書き器として大型モデルの検証に再利用し、下書きと検証を直列・並列の間で切り替えて、通信待ちとロールバックを抑える。

- **2026-05 · [Making Every Verified Token Count: Adaptive Verification for MoE Speculative Decoding](2026-2605.00342-making-every-verified-token-count-adaptive-verification-for-moe-speculative-deco.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  適応的検証は、下書き木の各枝の受理見込みと追加される専門家・検証時間を測り、費用対効果の低い枝を捨てて、MoEの検証計算と重み読出しを減らす。

- **2026-03 · [A Pipelined Collaborative Speculative Decoding Framework for Efficient Edge-Cloud LLM Inference](2026-2603.19133-picospec-edge-cloud-pipelined-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  端末の候補生成とクラウド検証を非同期に重ね、棄却用確率分布を疎圧縮してネットワーク往復を隠すことで、端末・クラウド協調推論を最大2.9倍高速化する。

- **2026-02 · [SPEED-Bench: A Unified and Diverse Benchmark for Speculative Decoding](2026-2604.09557-speed-bench-speculative-decoding-benchmark.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的復号を意味多様性・入力長・エントロピー・並列度の軸で統一評価し、合成入力の平均23%過大評価やバッチ依存の最適ドラフト長など、従来ベンチマークの順位偏りを明らかにする。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [Osprey: Target-agnostic Pre-training Makes Stronger Drafters in Speculative Decoding](2026-2609.09338-osprey-target-agnostic-pretraining-speculative-decoding.md)**  
  実装：[✓](https://github.com/LeanModels/Osprey) ・ リポジトリ内被引用：0  
  Ospreyは、汎用ウェブで事前学習した浅いドラフト骨格を複数ターゲットへ転用し、ターゲット固有蒸留の初期値を改善して分野外でも受理トークンを増やし、検証回数を減らす。

- **2026-09 · [NebulaSD: Many-for-Many Speculative Decoding](2026-2609.29364-nebulasd.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  NebulaSDは、投機的復号（投機的復号）のドラフト生成と対象モデル検証を固定した一対一の組から切り離し、M個のドラフトワーカーとN個の対象ワーカーを独立した共有資源プールとして運用する推論システムである。物理分離方式比で50.4%、同居方式比で72.6%高く、時間重み付きストリーミングマルチプロセッサ活動率も約29〜30%から47.3%へ上昇した。

- **2026-09 · [LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers](2026-2609.17184-loopspec-pipelined-self-speculative-looped-transformers.md)**  
  実装：[✓](https://github.com/kaist-flexml-lab/loopspec) ・ リポジトリ内被引用：0  
  ループ型Transformerの中間再帰状態を投機提案に使い、未来ドラフトと現在検証をパイプライン化して最大6.83倍高速化する。

- **2026-09 · [How Lossless Is Lossless Speculative Decoding? The Role of Numerical Precision in Orthrus](2026-2609.15504-orthrus-numerical-precision-losslessness.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Orthrusの無損失投機的復号を独立再現し、BF16では生成軌跡の完全一致が43〜45%に留まる一方、FP32では1,190件すべて一致することを示した再現・評価研究。

- **2026-09 · [ECHO: Early-layer Collaborative Hierarchical Orchestration with Bonus Logits in Speculative Decoding](2026-2609.17241-echo-early-layer-collaborative-hierarchical-orchestration-with-bonus-logits-in-speculative-decoding.md)**  
  実装：[✓](https://github.com/whucs21Mzy/ECHO) ・ リポジトリ内被引用：0  
  対象モデルの前半層を高頻度の候補木探索、後半層を低頻度の厳密検証へ分け、中間状態再利用と補助ロジットで候補を更新し、追加ドラフトモデルなしで2.4〜2.9倍級の生成高速化を報告する。

- **2026-09 · [DFlow: Enabling Verifier Information Flow in Block Diffusion Speculative Decoding](2026-2609.06498-dflow-verifier-information-flow-block-diffusion.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検証済みだが棄却された後続位置の対象モデル中間表現を次の投機生成回へ再利用し、対象モデルの追加計算なしでブロック拡散型投機的復号の平均受理長を約10〜13%改善する。

- **2026-09 · [Carryover Drafting: Recycling Rejected States for Speculative Decoding](2026-2609.14717-carryover-drafting-recycling-rejected-states.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検証済みだが棄却されたターゲット隠れ状態を次回ドラフトの一時KV文脈へ再利用し、追加投影器なしで受理長を6.5〜14.7%改善する。

- **2026-08 · [Vision Is Not Overhead: One-Pass Block Drafting for Lossless Speculative Decoding in Vision-Language Models](2026-2609.00355-glance-vlm-speculative-decoding.md)**  
  実装：[✓](https://github.com/js-lee-AI/GLANCE。実運用比較はSGLang) ・ リポジトリ内被引用：0  
  GLANCEは、VLMの視覚・言語融合状態から未来トークン塊を1回で下書きし、幅広い候補木を対象モデルで一括検証して、画像根拠付き生成の逐次下書き処理を減らす。

- **2026-08 · [MemSpec: Memory-Aware Runtime for Adaptive Draft Scheduling in Speculative Decoding on Edge Devices](2026-2608.10362-memspec-memory-aware-adaptive-draft-scheduling-edge.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MemSpecは、入力と生成履歴から有望なドラフトを予測し、上位モデルを常駐集合へ先読みして、エッジ端末のSSD読み込み待ちを隠し適応投機を高速化する。

- **2026-08 · [AcceptMoE: Commitment-Weighted Self-Sizing Verifier Expert Sets for Efficient MoE Speculative Decoding](2026-2608.02989-acceptmoe-commitment-weighted-self-sizing-verifier-expert-sets-for-efficient-moe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AcceptMoEは、下書き枝の受理見込みとルータ寄与を重み付けし、層ごとの検証専門家集合を縮めて、オフロード時のホストからGPUへの転送量を削る近似方式。

- **2026-07 · [DraftExpert: Expansion-Aware Self-Speculative Decoding for End-Device MoE Inference](2026-2607.24434-draftexpert-expansion-aware-self-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DraftExpertは、各MoE層に小型の常駐専門家を追加して候補を作り、専門家展開量を予測した枝打ちと非同期先読みを行い、端末の専門家搬送待ちを減らす。

- **2026-07 · [AdaptiveSD A Stability-Aware, Runtime-Adaptive Speculative Decoding Framework with Multi-Policy Orchestration for CPU-Constrained LLM Inference](2026-2607.03876-adaptivesd-runtime-adaptive-cpu-constrained.md)**  
  実装：[✓](https://github.com/sadrasa97/adaptive-speculate-decoding) ・ リポジトリ内被引用：0  
  CPU資源・受理率・遅延・KV圧力を監視し、投機深度を閉ループ制御して資源飽和と遅延変動を抑える適応投機デコード。

- **2026-05 · [An Interpretable Latency Model for Speculative Decoding in LLM Serving](2026-2605.15051-interpretable-latency-model-speculative-decoding-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号の遅延モデルは、Littleの法則で実効バッチを推定し、下書き・検証の固定費と負荷依存費を分けて測定して、要求率に応じた下書き長の選択境界を明らかにする。

- **2026-04 · [NanoSpec: Accelerating Speculative Decoding using Minimalist In-Context Vocabularies](2026-2605.26444-microspec-lightweight-in-context-vocabularies.md)**  
  実装：[✓](https://github.com/csAugust/NanoSpec) ・ リポジトリ内被引用：0  
  文脈と直近候補から毎ステップ3000未満の動的ドラフト語彙を作り、必要なLMヘッド重みを非同期収集して射影計算を削減する投機的デコード最適化。EAGLE-2のドラフト時間を平均51.6%削減する。

- **2026-04 · [FASER: Fine-Grained Phase Management for Speculative Decoding in Dynamic LLM Serving](2026-2604.20503-faser-fine-grained-phase-management.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動的負荷下の投機的デコードを、リクエスト別投機長、検証途中の棄却枝刈り、ドラフトと検証のフロンティア単位重畳で細粒度化し、vLLM上で最大53%のスループット向上と最大1.92倍の遅延改善を示す。

- **2026-02 · [When RL Meets Adaptive Speculative Training: A Unified Training-Serving System](2026-2602.06932-aurora-adaptive-speculator-training-serving.md)**  
  実装：[✓](https://github.com/togethercomputer/aurora) ・ リポジトリ内被引用：0  
  実配信の採用・棄却トレースからドラフトモデルを非同期更新し、停止なしで重みを差し替える閉ループ型の投機的復号により、初日配備と分布変化への継続適応を実現する。

- **2026-02 · [Vegas: Self-Speculative Decoding with Verification-Guided Sparse Attention](2026-2602.07223-specattn-sparse-attention-self-speculative-decoding.md)**  
  実装：[✓](https://github.com/platformxlab/vegas) ・ リポジトリ内被引用：0  
  検証で得た注意ロジットを次の疎な候補生成へ再利用し、鍵値選択の追加走査を抑えながら損失なし自己投機復号を高速化する。

### 2年前（2024-11〜2025-10）

- **2025-03 · [EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test](2025-2503.01840-eagle-3.md)**  
  実装：[✓](https://github.com/SafeAILab/EAGLE) ・ リポジトリ内被引用：44  
  特徴回帰制約を外して直接トークン予測し、訓練時に自己生成入力を再投入することでドラフト学習のデータ規模拡大を有効化したEAGLE系投機的復号。

- **2025-04 · [MagicDec: Breaking the Latency-Throughput Tradeoff for Long Context Generation with Speculative Decoding](2025-2408.11049-magicdec-breaking-the-latency-throughput-tradeoff-for-long-context-gener.md)**  
  実装：— ・ リポジトリ内被引用：11  
  投機的復号は小さなドラフトが複数トークンを提案し、大きな対象モデルが一括検証することで対象モデル呼出し回数を減らす。Llama-3.1-8Bでは8枚H100、10万トークン級の長文脈で最大2.51倍を報告する。

- **2025-10 · [SP-MoE: Speculative Decoding and Prefetching for Accelerating MoE-based Model Inference](2025-2510.10302-sp-moe-speculative-decoding-and-prefetching-for-accelerating-moe-based-model-inf.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  SP-MoEは、下書き生成中に対象MoEが次に使う専門家を予測し、CPUからGPUへ重みを非同期先読みして、検証時の専門家転送待ちを隠す。

- **2025-09 · [DiffuSpec: Unlocking Diffusion Language Models for Speculative Decoding](2025-2510.02358-diffuspec-unlocking-diffusion-language-models-for-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  拡散言語モデルで複数トークンを一括提案し、因果整合経路探索と適応ドラフト長制御でQwen2.5-32Bの投機的復号を平均3.08倍高速化する。

- **2025-06 · [Utility-Driven Speculative Decoding for Mixture-of-Experts](2025-2506.20675-cascade.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  MoEでは投機長が増やす専門家読出し費用まで含めた効用を実測し、投機の無効化とK選択を動的に行って最悪減速を5%へ抑える。

- **2025-05 · [MoESD: Unveil Speculative Decoding's Potential for Accelerating Sparse MoE](2025-2505.19645-moesd-unveiling-speculative-decodings-potential-for-accelerating-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  MoESDは新しい投機アルゴリズムを提案するというより、「混合専門家（Mixture of エキスパート; MoE）モデルでは投機的復号（投機的復号; SD）が本当に不利なのか」を実行効率から再分析する。

- **2025-07 · [TETRIS: Optimal Draft Token Selection for Batch Speculative Decoding](2025-2502.15197-tetris-optimal-draft-token-selection-for-batch-speculative-decoding.md)**  
  実装：[✓](https://github.com/ZhaoxuanWu/Tetris) ・ リポジトリ内被引用：4  
  投機的復号（投機的復号; SD）で速いドラフトモデルが多めの候補を作り、遅い対象モデルが並列検証する構造はそのままに、対象モデルへ送る候補を要求ごとではなくバッチ全体で選び直す。各要求の連続候補について「そこまで全部受理される確率」を計算し、限られた検証容量 (C) を確率の高い前方トークンへ配る。

- **2025-04 · [PARD: Accelerating LLM Inference with Low-Cost PARallel Draft Model Adaptation](2025-2504.18583-pard-accelerating-llm-inference-with-low-cost-parallel-draft-model-adaptation.md)**  
  実装：[✓](https://github.com/AMD-AIG-AIMA/PARD) ・ リポジトリ内被引用：4  
  小型AR 下書きをmask-トークン型の並列下書きへ変換し、KV整合性を保つConditional Dropで学習費を抑えつつモデル family内で再利用するPARD。

- **2025-09 · [Set Block Decoding is a Language Model Inference Accelerator](2025-2509.04185-set-block-decoding-is-a-language-model-inference-accelerator.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  次トークン予測とマスク位置予測を同一Transformerへ統合し、未来ブロックの非連続位置をEB-Samplerで並列確定するSBD。8Bモデルで品質を概ね維持しながら前向き計算回数を約3〜5倍削減し、H100屋根線モデルで実時間化の可能性を分析する。

- **2025-05 · [Fast and Cost-effective Speculative Edge-Cloud Decoding with Early Exits](2025-2505.21594-fast-and-cost-effective-speculative-edge-cloud-decoding-with-early-exits.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  Cloud targetの早期出口から暫定トークンを返し、edge 下書きを最終検証と並行して先行生成することで待ち時間を隠し、Jetson Nano＋A100でpre-drafting単体最大11%級の追加改善を示す。

- **2025-04 · [Speculative Diffusion Decoding: Accelerating Language Generation through Diffusion](2025-speculative-diffusion-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  自己回帰型の下書き器を離散拡散型へ置換し、候補列の生成と目標モデルによる検証の双方を並列化して投機的復号を高速化する方式。

- **2025-03 · [ML-SpecQD: Multi-Level Speculative Decoding with Quantized Drafts](2025-2503.13565-ml-specqd-multi-level-speculative-decoding-quantized-drafts.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  BF16対象の直接MXFP4版を第一段ドラフトにし、その生成を小型ドラフトで再び投機して、専用ドラフト学習なしに最大2.72倍高速化する。

- **2025-09 · [SpecVLM: Fast Speculative Decoding in Vision-Language Models](2025-2509.11815-specvlm-fast-speculative-decoding-in-vision-language-models.md)**  
  実装：— ・ リポジトリ内被引用：2  
  SpecVLMはこのVLM固有の律速へ、EAGLE-2型のEagleVLM、弾力的視覚圧縮器、オンラインlogit蒸留を組み合わせる。対象モデルによる最終検証は維持するため、投機部分は対象分布を変えない。

- **2025-09 · [Communication-Efficient Collaborative LLM Inference via Distributed Speculative Decoding](2025-2509.04576-communication-efficient-distributed-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  分散投機的デコードの上り通信を語彙全体分布から上位K疎ロジットへ圧縮し、出力分布を維持したまま通信量と最適ドラフト長を共同最適化する。

- **2025-07 · [Quantize-Sample-and-Verify: LLM Acceleration via Adaptive Edge-Cloud Speculative Decoding](2025-2507.00605-quantize-sample-and-verify-llm-acceleration-via-adaptive-edge-cloud-spec.md)**  
  実装：— ・ リポジトリ内被引用：2  
  Q-SVは、量子化された確率情報からサンプルしてもクラウド側の目標分布を厳密に保存する量子化・サンプル戦略と、通信状態・意味的不確実性に応じてドラフト長と量子化精度を同時調整する制御を組み合わせる。

- **2025-05 · [Scaling Laws for Speculative Decoding](2025-2505.07858-scaling-laws-for-speculative-decoding.md)**  
  実装：— ・ リポジトリ内被引用：2  
  この則でScyllaを設計し、Llama 2/3とQwen2.5でEAGLE2より高い受理性能を示し、産業向け推論エンジンではEAGLE2比2倍の復号スループットを報告する。

- **2024-11 · [Draft Model Knows When to Stop: A Self-Verification Length Policy for Speculative Decoding](2024-2411.18462-draft-model-knows-when-to-stop-a-self-verification-length-policy-for-spe.md)**  
  実装：— ・ リポジトリ内被引用：2  
  固定長でドラフトすると、簡単な区間では短すぎて一括検証の機会を失い、難しい区間では長すぎて後半が棄却され、無駄なドラフト計算が増える。低エントロピーならドラフトを続け、高エントロピーになった位置で検証へ切り替える。

- **2024-11 · [A Theoretical Perspective for Speculative Decoding Algorithm](2024-2411.00841-a-theoretical-perspective-for-speculative-decoding-algorithm.md)**  
  実装：— ・ リポジトリ内被引用：2  
  投機的復号は小型ドラフトモデルが複数トークンを提案し、大型対象モデルが一括検証することで自己回帰step数を減らす。

- **2025-05 · [SpecMemo: Speculative Decoding is in Your Pocket](2025-2506.01986-specmemo-memory-aware-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的デコードの候補木・KVキャッシュ・デコードヘッドをGPUメモリ予算に合わせて自動調整し、Titan RTXで生成メモリ65%削減・スループット96%維持、8×MI250のLlama-2-70Bでは通常分散復号比2倍を示す。

- **2024-12 · [Dovetail: A CPU/GPU Heterogeneous Speculative Decoding for LLM inference](2024-2412.18934-dovetail-cpu-gpu-heterogeneous-speculative-decoding.md)**  
  実装：[✓](https://github.com/ddInference/Dovetail) ・ リポジトリ内被引用：1  
  ターゲットLLMをCPU、深くした小型ドラフトをGPUへ分離し、候補数削減・動的ゲート融合・複数Transformerブロックで低VRAM環境の投機的デコードを高速化する。

- **2025-03 · [SPIN: Accelerating Large Language Model Inference with Heterogeneous Speculative Models](2025-2503.15921-spin-heterogeneous-speculative-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  要求難度に応じて異種の小型下書きモデルを選択し、検証バッチのゼロ埋めを要求分解で減らし、下書き生成と標的検証を小バッチ単位で重ねて投機的デコードを高速化する。

### 3年前（2023-11〜2024-10）

- **2024-01 · [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](2024-2401.10774-medusa-multiple-decoding-heads.md)**  
  実装：[✓](https://github.com/FasterDecoding/Medusa) ・ リポジトリ内被引用：95  
  Medusaは、対象LLMの隠れ状態に未来位置ごとの小型予測ヘッドを追加し、上位候補を木構造へまとめて一括検証することで、別ドラフトモデルを置かず対象モデルの逐次呼出しを減らす。

- **2024-01 · [EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](2024-2401.15077-eagle-feature-speculative-sampling.md)**  
  実装：[✓](https://github.com/SafeAILab/EAGLE) ・ リポジトリ内被引用：75  
  EAGLEは、対象LLMの上位層特徴量と直前に標本化したトークンを小型デコーダへ与えて未来特徴量を予測し、元の言語モデル出力ヘッドと木構造検証で重み読出し回数を減らす。

- **2024-02 · [Break the Sequential Dependency of LLM Inference Using Lookahead Decoding](2024-2402.02057-lookahead-decoding.md)**  
  実装：[✓](https://github.com/hao-ai-lab/LookaheadDecoding) ・ リポジトリ内被引用：32  
  先読みデコードは、対象LLMを未来位置へ並列反復して途中の正しい短いトークン列を蓄積し、現在接頭辞に合う候補を一括検証して、追加モデルなしに逐次ステップとメモリ帯域待ちを減らす。

- **2024-06 · [EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees](2024-2406.16858-eagle-2.md)**  
  実装：✓ ・ リポジトリ内被引用：25  
  EAGLE-2は、投機的復号（投機的復号）で使う候補木を固定形状から文脈適応型へ変える方式である。元のEAGLEは軽量ドラフトモデルで複数候補を作り、大規模な対象モデルが一括検証することで自己回帰復号を高速化するが、候補木の形を事前に固定すると、簡単な文脈にも難しい文脈にも同じ計算予算を配ってしまう。

- **2024-07 · [Online Speculative Decoding](2023-2310.07177-online-speculative-decoding.md)**  
  実装：[✓](https://github.com/LiuXiaoxuanPKU/OSD) ・ リポジトリ内被引用：23  
  投機的復号で得られる目標モデルの確率分布を教師信号として下書きモデルをオンライン更新し、問い合わせ分布の変化に追従して受理率と推論速度を高める方式。

- **2023-11 · [REST: Retrieval-Based Speculative Decoding](2023-2311.08252-rest-retrieval-speculative-decoding.md)**  
  実装：[✓](https://github.com/FasterDecoding/REST) ・ リポジトリ内被引用：14  
  RESTは、現在文脈末尾と一致する過去トークン列を接尾辞索引から検索し、その続き候補を木構造へ集約して対象LLMで一括検証し、ドラフトモデルなしで反復的なコードの対象重み読出しを減らす。

- **2024-04 · [TriForce: Lossless Acceleration of Long Sequence Generation with Hierarchical Speculative Decoding](2024-2404.11912-triforce-lossless-acceleration-of-long-sequence-generation-with-hierarch.md)**  
  実装：— ・ リポジトリ内被引用：13  
  文脈が128K以上になるとKV読出しがメモリ帯域を圧迫し、GPU演算器が十分使われない。KVを削除・量子化する方式は帯域を減らせる一方、最終出力を変える可能性がある。

- **2024-03 · [Block Verification Accelerates Speculative Decoding](2024-2403.10444-block-verification-accelerates-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  投機的復号の候補接頭辞をブロック単位で共同検証し、出力分布を変えず期待生成量を理論最適化。PaLM-2評価で標準検証よりブロック効率平均8.30%、実時間平均6.49%改善する。

- **2024-06 · [SpecExec: Massively Parallel Speculative Decoding for Interactive LLM Inference on Consumer Devices](2024-2406.02532-specexec-massively-parallel-speculative-decoding-for-interactive-llm-inference-on-consumer-devices.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  RAMオフロードでは「対象モデルを1トークン通す時間」と「数百〜数千トークンをまとめて通す時間」の差が小さくなる。SpecExecはその余剰バッチ幅で将来分布を事前計算し、70B級モデルを消費者GPUでも数トークン/sで対話可能にする。

- **2024-06 · [OPT-Tree: Speculative Decoding with Adaptive Draft Tree Structure](2024-2406.17276-opt-tree-speculative-decoding-with-adaptive-draft-tree-structure.md)**  
  実装：[✓](https://github.com/Jikai0Wang/OPT-Tree) ・ リポジトリ内被引用：5  
  木型投機的復号では、候補数が同じでも「一本道に深く使うか」「複数枝へ広く使うか」で受理トークン数が変わる。OPT-Treeはその形を手作業で固定せず、ドラフト確率から期待受理長を計算し、入力ごとに価値の高い候補だけで木を組み直す。

- **2024-05 · [Dynamic Speculation Lookahead Accelerates Speculative Decoding of Large Language Models](2024-2405.04304-dynamic-speculation-lookahead-accelerates-speculative-decoding-of-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  DISCOは投機的復号（投機的復号; SD）の先読み長（Speculation Lookahead; SL）をラウンドごとに変える。次トークンが簡単な区間では長くドラフトし、難しく拒否されやすい区間では早く対象モデル検証へ移ることで、「固定kでは長過ぎるか短過ぎる」という問題を避ける。

- **2024-04 · [Kangaroo: Lossless Self-Speculative Decoding via Double Early Exiting](2024-2404.18911-kangaroo-lossless-self-speculative-decoding-via-double-early-exiting.md)**  
  実装：[✓](https://github.com/Equationliu/Kangaroo) ・ リポジトリ内被引用：5  
  Kangarooは別のドラフトモデルを持たず、対象LLMの浅い前半層を自己ドラフトとして使う。浅い表現を補正する小型アダプタと、低確信度になった時点でドラフト生成自体を打ち切る「二重の早期終了」により、追加パラメータと無駄なドラフト計算を同時に抑える。

- **2024-01 · [SpecBranch: Speculative Decoding via Hybrid Drafting and Rollback-Aware Branch Parallelism](2025-2506.01979-specbranch-speculative-decoding-via-hybrid-drafting-and-rollback-aware-branching.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  SpecBranchは投機的復号（投機的復号; SD）の「ドラフト→対象モデル検証→却下ならやり直し」という直列依存を、分岐予測に似た並列枝で隠す。単一の長い候補列へ賭けず、却下されそうな位置から複数候補を先回りして生成し、対象モデルが一方を拒否しても別枝へ継続できるようにする。

- **2024-08 · [Learning Harmonized Representations for Speculative Sampling](2024-2408.15766-learning-harmonized-representations-for-speculative-sampling.md)**  
  実装：[✓](https://github.com/HArmonizedSS/HASS) ・ リポジトリ内被引用：4  
  EAGLE系ドラフトの学習時／復号時の文脈差と蒸留目的のずれをTop-K蒸留＋multi-step context alignmentで揃えるHASS。

- **2023-12 · [Cascade Speculative Drafting for Even Faster LLM Inference](2023-2312.11462-cascade-speculative-drafting-for-even-faster-llm-inference.md)**  
  実装：[✓](https://github.com/lfsszd/CS-Drafting) ・ リポジトリ内被引用：4  
  下書きモデル自身をさらに投機するVertical Cascadeと、後方トークンほど小さい下書きへ切替えるHorizontal Cascadeで投機的復号の下書き費用を削る。

- **2024-10 · [DySpec: Faster Speculative Decoding with Dynamic Token Tree Structure](2024-2410.11744-dyspec-faster-speculative-decoding-with-dynamic-token-tree-structure.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  ドラフト確率を対象モデルの受理確率の代理にして投機木を実行時に動的構築し、限られた検証予算を高確率枝へ集中して固定木より長い受理系列と低遅延を狙う。

- **2024-02 · [Generation Meets Verification: Accelerating Large Language Model Inference with Smart Parallel Auto-Correct Decoding](2024-2402.11809-generation-meets-verification-accelerating-large-language-models-with-speculative-decoding.md)**  
  実装：[✓](https://github.com/cteant/SPACE) ・ リポジトリ内被引用：3  
  SPACE（Smart Parallel Auto-Correct デコード）は、通常は1位置しか予測しない自己回帰LLMを半自己回帰教師あり微調整で「複数位置を同時予測できるモデル」へ変え、候補生成と検証を1回のモデル呼出しに同居させる。HumanEval-Xで出力品質を保ちながら2.7〜4.0倍の推論高速化を報告する。

- **2024-10 · [AdaEDL: Early Draft Stopping for Speculative Decoding of Large Language Models via an Entropy-based Lower Bound on Token Acceptance Probability](2024-2410.18351-adaedl-early-draft-stopping-for-speculative-decoding-of-large-language-m.md)**  
  実装：— ・ リポジトリ内被引用：2  
  ドラフト分布のエントロピーから受理確率下限を推定し、投機的復号のドラフトを早期停止して無駄な小型モデル計算を削減する学習不要方式。

- **2024-05 · [Nearest Neighbor Speculative Decoding for LLM Generation and Attribution](2024-2405.19325-nearest-neighbor-speculative-decoding-for-llm-generation-and-attribution.md)**  
  実装：— ・ リポジトリ内被引用：2  
  k近傍言語モデル（kNN-LM）は、生成中の隠れ状態に近い外部コーパス中のトークンを検索し、その近傍分布とLLMの分布を混ぜることで、モデル重みにない事実を生成へ反映できる。しかし毎トークン検索と分布構築を行うため遅く、検索された実文書の連続spanをそのまま活用しにくい。

- **2024-04 · [BASS: Batched Attention-optimized Speculative Sampling](2024-2404.15778-bass.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  系列ごとに異なる投機受理長を保ったまま注意計算をバッチ化し、動的ドラフト長調整で複数応答の遅延とGPU利用率を改善する方式。

### 4年前（2022-11〜2023-10）

- **2023-02 · [Accelerating Large Language Model Decoding with Speculative Sampling](2023-2302.01318-speculative-sampling.md)**  
  実装：✓ ・ リポジトリ内被引用：101  
  小型モデルの複数候補を大型モデルで並列検証し、出力分布を変えず700億パラメータモデルのデコードを最大約2.5倍高速化。

- **2022-11 · [Fast Inference from Transformers via Speculative Decoding](2022-2211.17192-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：100  
  軽量モデルの複数トークン提案を対象モデルで並列検証し、出力分布を変えずに直列復号回数を削減する投機的復号の基礎研究。

- **2023-05 · [SpecInfer: Accelerating Generative Large Language Model Serving with Tree-based Speculative Inference and Verification](2023-2305.09781-specinfer-tree-speculative-inference.md)**  
  実装：[✓](https://github.com/flexflow/FlexFlow) ・ リポジトリ内被引用：63  
  SpecInferは、小型モデル群が先に作る複数候補を共通接頭辞の木へまとめ、対象LLMを1回で木構造検証することで、逐次デコードの対象重み読出しとGPU間通信を減らし、複数トークンを確定する。

- **2023-09 · [Draft & Verify: Lossless Large Language Model Acceleration via Self-Speculative Decoding](2023-2309.08168-draft-verify.md)**  
  実装：[✓](https://openreview.net/attachment?id=ACC2nQYzPYS&name=software) ・ リポジトリ内被引用：22  
  元モデルの中間層を一時的に飛ばして下書きを生成し、完全モデルで一括検証することで、追加下書きモデルなしに最大約2倍の損失なしデコード高速化を実現する。

- **2023-08 · [Accelerating LLM Inference with Staged Speculative Decoding](2023-2308.04623-accelerating-llm-inference-with-staged-speculative-decoding.md)**  
  実装：— ・ リポジトリ内被引用：16  
  小バッチの自己回帰デコードでは、1トークン生成のたびにモデル重みをGPUへ供給する必要がある一方、行列演算のバッチが小さいため演算器を使い切れない。標準的な投機的復号は小さなドラフトモデルが複数トークンを先読みし、大きな対象モデル（論文ではoracleと呼ぶ）が一括検証することで、重み読み出し1回あたりの確定トークン数を増やす。

- **2023-10 · [SPEED: Speculative Pipelined Execution for Efficient Decoding](2023-2310.12072-speed-speculative-pipelined-execution-for-efficient-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  周期パラメータ共有モデルの早い層から将来トークンを予測して同じ共有層へ並行投入し、重み読出しを償却することで、浅いT5に近い遅延のまま深いモデルの精度を得る。

- **2023-02 · [Speculative Decoding with Big Little Decoder](2023-2302.07863-speculative-decoding-with-big-little-decoder.md)**  
  実装：[✓](https://github.com/kssteven418/BigLittleDecoder) ・ リポジトリ内被引用：3  
  Big Little Decoder（BiLD）は、小型モデルに自己回帰生成を任せ、予測が難しいときだけ大型モデルへフォールバックする。大型モデルは小型モデルが直前まで作った区間をまとめて評価し、不一致が大きい位置までロールバックして修正する。mT5/T5の翻訳・要約でNVIDIA T4上最大2.12倍高速化する。
<!-- survey:auto:end -->
