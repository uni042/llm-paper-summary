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
