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
## 自動生成の論文一覧（6本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/23-model-routing-cascades/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-12〜2026-11**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-12〜2026-11）

該当なし。

### 直近12か月・未被引用（2025-12〜2026-11）

該当なし。

### 2年前（2024-12〜2025-11）

- **2025-07 · [R-Stitch: Dynamic Trajectory Stitching for Efficient Reasoning](2025-2507.17307-r-stitch-dynamic-trajectory-stitching-for-efficient-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  R-Stitchは、長い思考過程（Chain-of-Thought、CoT）を生成する際、小型言語モデル（SLM）が確信を持って生成できる部分は小型側に任せ、難しいトークンだけ大型言語モデル（LLM）へ移す方式である。

- **2025-08 · [Cost-Aware Contrastive Routing for LLMs](2025-2508.12491-cost-aware-contrastive-routing-for-llms.md)**  
  実装：[✓](https://github.com/rezashkv/cscr) ・ リポジトリ内被引用：0  
  CSCR（コスト-Spectrum Contrastive Router）は、質問の特徴と候補モデルの能力を同じベクトル空間へ配置し、正答できるモデルを費用帯ごとに区別する対照学習を行うことで、この選択を軽い近傍検索へ置き換える。

### 3年前（2023-12〜2024-11）

- **2024-04 · [Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing](2024-2404.14618-hybrid-llm-cost-efficient-and-quality-aware-query-routing.md)**  
  実装：[✓](https://github.com/m365-core/hybrid_llm_routing) ・ リポジトリ内被引用：49  
  同じ大規模言語モデル（LLM）を全要求へ使うと、単純な質問にも高価な推論計算を割り当てる。小型Llama-2 7B／大型Llama-2 13Bの組合せでは、検証集合で品質低下を1%以下にするしきい値を選んだ確率的ルータが、テスト集合で96.80%の要求を小型へ送ったが、品質低下は1.42%となった。

- **2024-04 · [Language Model Cascades: Token-level uncertainty and beyond](2024-2404.10136-language-model-cascades-token-level-uncertainty-and-beyond.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  本論文は、入力ごとに必要な推論計算量を変える「モデル段階実行」（モデル cascade）の委譲規則を、生成言語モデルに合わせて設計する研究である。

- **2024-02 · [Large Language Model Cascades with Mixture of Thought Representations for Cost-efficient Reasoning](2024-2310.03094-large-language-model-cascades-with-mixture-of-thought-representations-fo.md)**  
  実装：[✓](https://github.com/MurongYue/LLM_MoT_cascade) ・ リポジトリ内被引用：11  
  強力な言語モデルをすべての要求へ使用すると、簡単な算数問題にも難しい因果推論にも同じ高価なAPIを呼ぶことになる。一方、安価なモデルだけに切り替えると難問で正答率が落ちる。

### 6年前（2020-12〜2021-11）

- **2020-12 · [CascadeBERT: Accelerating Inference of Pre-trained Language Models via Calibrated Complete Models Cascade](2020-2012.14682-cascadebert-accelerating-inference-of-pre-trained-language-models-via-ca.md)**  
  実装：[✓](https://github.com/lancopku/CascadeBERT) ・ リポジトリ内被引用：12  
  提案するCascadeBERTは、単一モデルの途中で終了する代わりに、小型でも事前学習を完了した独立モデルを最初に走らせる。6つのGLUE分類課題で、BERT-baseを基準に実行層数を約4分の1へ減らす条件では、論文の課題平均はCascadeBERTが78.3、動的早期終了DeeBERTが67.8であり、差は10.5点、相対的には約15.5%である。
<!-- survey:auto:end -->
