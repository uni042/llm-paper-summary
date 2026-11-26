# Cost-Aware Model Routing and Cascaded Inference

推論時に独立して実行できる複数の言語モデルの計算を、要求、生成途中の不確実性、品質、費用、利用者の選好に応じて選択または段階化し、品質と推論費用の関係を制御するルーティング／カスケード研究をまとめる。

## 分類境界

入力ごとの品質・費用・難度・不確実性・選好に基づいて、独立して実行できる言語モデルから一つを選ぶ、または小型モデルの結果に応じて強いモデルへ段階的に引き継ぐ方式を含める。生成中のtoken/trajectory単位のモデル切替と、分類入力に対する独立encoder model間の完全モデルcascadeも、同じ要求内でモデル選択を行い品質対計算量を変える場合に含める。単一モデル内のlayer/token early exitやpruning、draft/target検証、複数要求間のreplica・queue・GPU配置、tool/agent workflow、MoE内部expert選択、全候補モデルを毎回実行して回答を集約する品質only ensemble、費用または計算量の選択を評価しない同費用モデルの品質順位付けは除く。

### 含める研究

- 要求単位で独立した言語モデルを選ぶquality/cost-aware router
- 小型モデルの応答品質や不確実性を使い完全モデル間を段階的に委譲するcascade
- 生成tokenまたはtrajectoryの途中で独立モデル間の生成主体を切り替える方式
- 完全encoder model間の入力単位cascadeでquality-efficiencyを変える方式
- routerのcalibration、学習、model-skill推定、cost-quality frontierの評価

### 含めない研究

- 同じmodel内の層・token・early-exit条件付き計算（04）
- draft tokenをtarget modelで検証するspeculative decoding（05）
- 複数request、replica、GPU、queue、KV cache間の配信・配置（11）
- tool呼出しやagent workflowを主対象とする実行制御（14）
- 単一MoE model内のexpert routing
- 全modelを実行して回答をaggregate/rerankする品質only ensemble
- 同費用候補の品質順位だけを最適化し、model計算の選択費用を扱わない方式

## 近傍系統

- [04-conditional-computation](../04-conditional-computation/)
- [05-speculative-decoding-moe](../05-speculative-decoding-moe/)
- [11-llm-serving-scheduling-disaggregation](../11-llm-serving-scheduling-disaggregation/)

この系統は複数論文からなる明確な近傍クラスタとしてDiscoveryの昇格ゲートを通過した。単一論文だけを理由に細分化せず、上記の分類境界を維持する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（30本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/23-model-routing-cascades/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-12〜2026-11**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-12〜2026-11）

- **2026-01 · [GlimpRouter: Efficient Collaborative Inference by Glimpsing One Token of Thoughts](2026-2601.05110-glimprouter-efficient-collaborative-inference-by-glimpsing-one-token-of-.md)**  
  実装：[✓](https://github.com/Zengwh02/GlimpRouter) ・ リポジトリ内被引用：3  
  大規模推論モデルは長い思考過程を生成するため、回答までの待ち時間と計算費用が大きい。トークン単位で常時切り替えると、判定とモデル切替が頻繁になりやすい。

- **2026-07 · [WISERouter: LLM Routing with Workload Budget Constraint](2026-2607.23765-wiserouter-llm-routing-with-workload-budget-constraint.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  常に最高性能のモデルを呼ぶと料金が膨らむ一方、全問い合わせに固定額を課すと、容易な問い合わせで節約した予算を難しい問い合わせへ振り向けられない。過去のモデル応答をすべて持つWR-Offlineと、限られた応答だけを逐次観測するWR-Onlineの二方式がある。

- **2026-04 · [Task-Aware LLM Routing with Multi-Level Task-Profile-Guided Data Synthesis for Cold-Start Scenarios](2026-2604.09377-task-aware-llm-routing-with-multi-level-task-profile-guided-data-synthes.md)**  
  実装：[✓](https://github.com/less-and-less-bugs/ColdStartLLMRouter) ・ リポジトリ内被引用：2  
  ドメイン内学習データがないコールドスタートでもLLMルーティングを可能にするため、階層タスク分類から質問応答データを合成して学習し、潜在タスクタイプ変数と分類由来の事前分布による正則化で回帰型ルーターの汎化を高めた研究。

- **2026-03 · [Robust Batch-Level Query Routing for Large Language Models under Cost and Capacity Constraints](2026-2603.26796-robust-batch-level-query-routing-for-large-language-models-under-cost-an.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  バッチ全体の割当てを整数線形計画で解いて費用と容量を直接守る経路選択の枠組みで、敵対的なバッチ構成では問い単位の方式より最大24パーセント高い精度を示した。

### 直近12か月・未被引用（2025-12〜2026-11）

- **2026-10 · [Whose Turn Is It? Context-Guided Model Routing for Stateful Agents](2026-2610.19292-whose-turn-is-it-context-guided-model-routing-for-stateful-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  状態を持つエージェントのターン単位ルーティングを比較し、履歴を見ることが同じ振り分け率で成功率を3.3ポイント上げることと、切替の費用が方向で非対称であり下方の切替だけが短期間で元を取ることを示した分析研究。

- **2026-09 · [Signed Rescue Routing: Harm-Aware Cascades for Efficient LLM Inference](2026-2609.07786-signed-rescue-routing-harm-aware-cascades-for-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（Large Language モデル; LLM）の多段推論では、全問い合わせを高価な大型モデルへ送る代わりに、まず小型モデルで回答し、難しいと判断したものだけ大型モデルへ送る。大型モデルの呼出し回数に予算があるとき、純利得が大きい問い合わせから優先して切り替える。

- **2026-09 · [Pretrain Once, Route Anywhere: Towards a Foundation Model for LLM Routing](2026-2609.37362-pretrain-once-route-anywhere-towards-a-foundation-model-for-llm-routing.md)**  
  実装：[✓](https://github.com/LAMDA-Model-Reuse/RouteFM) ・ リポジトリ内被引用：0  
  候補モデルを少数の行動観測から作る匿名の能力プロファイルで表し、異種環境をまたぐエピソード型事前学習で凍結まま適応できる基盤ルータを作り、未見のMMR-Benchで候補あたり8観測で最強比較対象を2.23ポイント上回る。

- **2026-07 · [Optimal Model Activation Policies for Inference Networks of Large Language Models](2026-2609.15992-optimal-model-activation-policies-for-inference-networks-of-large-langua.md)**  
  実装：[✓](https://github.com/anonym-conf/inf-nets) ・ リポジトリ内被引用：0  
  安いモデルを先に呼び確信度がしきい値未満のときだけ高いモデルへ委ねる方策が、直列の専門家モデル構成では最適であることを証明し、分類と生成で費用削減を実証する推論ネットワークの理論研究。

- **2026-05 · [Semantic-Aware Intelligent Request Routing in Multi-Model LLM Backend Gateways](2026-5c886960494f-semantic-aware-intelligent-request-routing-in-multi-model-llm-backend-ga.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  APIRouterは異種LLMを接続するAPIゲートウェイで、要求の軽量特徴抽出、66MパラメータのDistilBERTによる難易度3分類、負荷・価格・品質を考慮する文脈付きバンディットの三段階でバックエンドを選択する。

- **2026-05 · [Policy-Guided Stepwise Model Routing for Cost-Effective Reasoning](2026-2605.06116-policy-guided-stepwise-model-routing-for-cost-effective-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  思考連鎖の中間状態ごとに小型モデル継続か大型モデルへの昇格かを決める段階的ルーティングを制約つき決定問題として定式化し、小型制御ポリシーの強化学習と閾値較正を同時に行うことで、過程報酬モデルなしに精度とコストのトレードオフを改善した研究。

- **2026-04 · [RouteLMT: Learned Sample Routing for Hybrid LLM Translation Deployment](2026-2604.22520-routelmt-learned-sample-routing-for-hybrid-llm-translation-deployment.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルを用いた翻訳では、高品質な大型モデルをすべての要求に適用すると推論費用と遅延が大きくなる。小型モデルで大半を処理し、必要な要求だけ大型モデルへ振り分ける混成配備（hybrid deployment）は、一定の品質を維持しながら大型モデルの利用率を抑えるための基本的な方式である。

- **2026-04 · [RankGuide: Tensor-Rank-Guided Routing and Steering for Efficient Reasoning](2026-2604.16694-rankguide-tensor-rank-guided-routing-and-steering-for-efficient-reasonin.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  隠れ状態のテンソルランクの崩壊を小さい推論モデルの失敗信号として使い、過信型の誤りを大きいモデルへ回し、高ランク校正だけで作ったステアリングベクトルで再検証を減らす協調推論の枠組み。

- **2026-03 · [Confidence-Calibrated Small-Large Language Model Collaboration for Cost-Efficient Reasoning](2026-2603.03752-confidence-calibrated-small-large-language-model-collaboration-for-cost-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、小型言語モデル（SLM）にまず問題を解かせ、答えへの自己申告確信度が低いときだけ大型言語モデル（LLM）へ委譲する二段推論方式COREAを提案する。大型モデル単独との比較で、領域外の数理問題では推定費用21.5%減・正答率1.7ポイント減、非数理問題では16.8%減・正答率1.7ポイント減となった。

- **2026-02 · [MentorCollab: Large-to-Small Inference-Time Mentorship for Concise Reasoning in Language Models](2026-2602.05307-mentorcollab-large-to-small-inference-time-mentorship-for-concise-reason.md)**  
  実装：[✓](https://github.com/haojinw0027/Mentorcollab) ・ リポジトリ内被引用：0  
  大型推論モデルは複雑な問題を解ける反面、解答までの思考列が長く、生成トークンの費用が増える。大型モデルが出力するトークンを小型モデルへ逐次注入する従来の協調方式では、大型モデルの「考え直し」「前段階への後戻り」まで取り込んでしまい、小型モデルの簡潔さを損なう場合がある。メンター由来のトークンが最終生成列に占める割合は平均18.4%と記述される。

### 2年前（2024-12〜2025-11）

- **2025-02 · [LLM Bandit: Cost-Efficient LLM Generation via Preference-Conditioned Dynamic Routing](2025-2502.02743-llm-bandit-cost-efficient-llm-generation-via-preference-conditioned-dyna.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  安価なモデルだけを使えば費用を抑えられるが、難しい質問で誤答が増える。複数モデルを順番に呼び出すカスケード方式は品質を確認してから高価なモデルへ移れる一方、複数回の推論が必要になる。

- **2025-08 · [Cost-Aware Contrastive Routing for LLMs](2025-2508.12491-cost-aware-contrastive-routing-for-llms.md)**  
  実装：[✓](https://github.com/rezashkv/cscr) ・ リポジトリ内被引用：4  
  CSCR（コスト-Spectrum Contrastive Router）は、質問の特徴と候補モデルの能力を同じベクトル空間へ配置し、正答できるモデルを費用帯ごとに区別する対照学習を行うことで、この選択を軽い近傍検索へ置き換える。

- **2025-07 · [R-Stitch: Dynamic Trajectory Stitching for Efficient Reasoning](2025-2507.17307-r-stitch-dynamic-trajectory-stitching-for-efficient-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  R-Stitchは、長い思考過程（Chain-of-Thought、CoT）を生成する際、小型言語モデル（SLM）が確信を持って生成できる部分は小型側に任せ、難しいトークンだけ大型言語モデル（LLM）へ移す方式である。

- **2025-11 · [Confidence-Guided Stepwise Model Routing for Cost-Efficient Reasoning](2025-2511.06190-confidence-guided-stepwise-model-routing-for-cost-efficient-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  外部の判定模型を使わず、小さい模型のロジット最大値から段ごとの確信度を測り、混合正規分布の事後確率で次の段を小さい模型に任せるか大きい模型へ回すかを決める段単位の振り分けで、難関数学課題では大きい模型だけより正解率が二割上がり計算量が四八パーセント減ったと報告した。

- **2025-09 · [IPR: Intelligent Prompt Routing with User-Controlled Quality-Cost Trade-offs](2025-2509.06274-ipr-intelligent-prompt-routing-with-user-controlled-quality-cost-trade-o.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  入力文だけから各候補モデルの応答品質を連続値で予測し、利用者が許容度で決める閾値以上の候補から最も安いものを選ぶ振り分けで、クロード系列で最強モデルと品質同等を保ちながら費用を四十三・九パーセント削減し、新モデル追加も凍結した符号器への軽い適合だけで済むようにしたと報告した。

- **2025-06 · [SPECS: Faster Test-Time Scaling through Speculative Drafts and Dynamic Switching](2025-2506.15733-specs-faster-test-time-scaling-through-speculative-drafts-and-dynamic-sw.md)**  
  実装：[✓](https://github.com/mert-cemri/SPECS) ・ リポジトリ内被引用：1  
  第二に、最初は大型モデルで推論経路を確立し、途中報酬が十分高くなった時点で小型モデルへ切り替えることで、難しい初期推論と比較的容易な続きを分担する。原著v2のQwen2.5モデル対によるMATH500・ビーム幅8の評価では、大型モデルのみのビーム探索が正答率71.3%、平均13.6秒に対し、SPECSは79.5%、11.3秒であった。

- **2025-02 · [GATEKEEPER: Improving Model Cascades Through Confidence Tuning](2025-2502.19335-gatekeeper-improving-model-cascades-through-confidence-tuning.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GATEKEEPERは、軽量な小型モデルと高精度だが高価な大型モデルを組み合わせる二段推論カスケードに対して、小型モデルの確信度そのものを委譲判断に適した形へ学習し直す方式である。評価は正答率と委譲率の曲線を主軸としており、実サービング基盤におけるGPU処理量や末尾遅延の改善を直接測ったものではない。

### 3年前（2023-12〜2024-11）

- **2024-04 · [Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing](2024-2404.14618-hybrid-llm-cost-efficient-and-quality-aware-query-routing.md)**  
  実装：[✓](https://github.com/m365-core/hybrid_llm_routing) ・ リポジトリ内被引用：89  
  同じ大規模言語モデル（LLM）を全要求へ使うと、単純な質問にも高価な推論計算を割り当てる。小型Llama-2 7B／大型Llama-2 13Bの組合せでは、検証集合で品質低下を1%以下にするしきい値を選んだ確率的ルータが、テスト集合で96.80%の要求を小型へ送ったが、品質低下は1.42%となった。

- **2024-02 · [Large Language Model Cascades with Mixture of Thought Representations for Cost-efficient Reasoning](2024-2310.03094-large-language-model-cascades-with-mixture-of-thought-representations-fo.md)**  
  実装：[✓](https://github.com/MurongYue/LLM_MoT_cascade) ・ リポジトリ内被引用：26  
  強力な言語モデルをすべての要求へ使用すると、簡単な算数問題にも難しい因果推論にも同じ高価なAPIを呼ぶことになる。一方、安価なモデルだけに切り替えると難問で正答率が落ちる。

- **2024-04 · [Language Model Cascades: Token-level uncertainty and beyond](2024-2404.10136-language-model-cascades-token-level-uncertainty-and-beyond.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  本論文は、入力ごとに必要な推論計算量を変える「モデル段階実行」（モデル cascade）の委譲規則を、生成言語モデルに合わせて設計する研究である。

- **2024-10 · [Efficiently Deploying LLMs with Controlled Risk](2024-2410.02173-efficiently-deploying-llms-with-controlled-risk.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの運用費用を下げるために、小型モデルで簡単な質問へ回答し、難しい質問だけを大型モデルへ渡す階層的ルーティングが利用される。しかし、従来の費用最適化型ルータは「自信がないときには回答しない」という選択的予測の運用要件を、ルーティングの設計変数として十分に扱っていなかった。

### 4年前（2022-12〜2023-11）

- **2023-05 · [FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance](2023-2305.05176-frugalgpt-how-to-use-large-language-models-while-reducing-cost-and-impro.md)**  
  実装：[✓](https://github.com/stanford-futuredata/FrugalGPT) ・ リポジトリ内被引用：131  
  FrugalGPTは、価格・正確さ・誤答の種類が異なる複数の大規模言語モデル（LLM）を、予算を超えずに組み合わせる推論時のサービス選択方式である。

- **2023-11 · [Routing to the Expert: Efficient Reward-guided Ensemble of Large Language Models](2023-2311.08692-routing-to-the-expert-efficient-reward-guided-ensemble-of-large-language.md)**  
  実装：✓ ・ リポジトリ内被引用：28  
  本論文が解こうとする問題は、異なる得意分野を持つ既製の大規模言語モデル（LLM）を組み合わせる際、問い合わせごとに候補すべてを実行すると生成計算量が膨らむことである。一方、回答をすべて生成して報酬モデル（reward モデル）で順位付けする方式は品質の良い候補を後から選べるが、候補数に比例する生成費用を必要とする。

- **2023-05 · [Tabi: An Efficient Multi-Level Inference System for Large Language Models](2023-1685e89adb79-tabi-an-efficient-multi-level-inference-system-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  Tabiは、大型の言語モデルを用いた分類・回帰サービスで、すべての要求に同じ大きなモデルを実行する無駄を削減する推論システムである。サービスが例えば分類正答率95%以上という精度下限を指定すると、従来の推論基盤は平均精度が下限を超える単一モデルを選び、簡単な入力にも難しい入力にも同じ計算を行う。

### 5年前（2021-12〜2022-11）

- **2022-03 · [E-LANG: Energy-Based Joint Inferencing of Super and Swift Language Models](2022-2203.00748-e-lang-energy-based-joint-inferencing-of-super-and-swift-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大きなSuperと小さなSwiftを、Swiftの自由エネルギーで入力ごとに振り分ける動的推論で、再学習なしにT5で最大3.3倍、BERTで3.2倍の計算量削減とSuper同等以上の精度を両立する方式。

### 6年前（2020-12〜2021-11）

- **2020-12 · [CascadeBERT: Accelerating Inference of Pre-trained Language Models via Calibrated Complete Models Cascade](2020-2012.14682-cascadebert-accelerating-inference-of-pre-trained-language-models-via-ca.md)**  
  実装：[✓](https://github.com/lancopku/CascadeBERT) ・ リポジトリ内被引用：15  
  提案するCascadeBERTは、単一モデルの途中で終了する代わりに、小型でも事前学習を完了した独立モデルを最初に走らせる。6つのGLUE分類課題で、BERT-baseを基準に実行層数を約4分の1へ減らす条件では、論文の課題平均はCascadeBERTが78.3、動的早期終了DeeBERTが67.8であり、差は10.5点、相対的には約15.5%である。
<!-- survey:auto:end -->
