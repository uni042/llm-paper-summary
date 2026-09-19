<!-- survey:auto:start -->
## 自動生成の論文一覧（16本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2025-11 · [DuetServe: Harmonizing Prefill and Decode for LLM Serving via Adaptive GPU Multiplexing](2025-2511.04791-duetserve-adaptive-gpu-multiplexing.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  TBT違反が予測される時だけ単一GPUのSMをプリフィル/デコードへ動的分割し、集約方式のスループットと分離方式のisolationを両立する。

- **2026-02 · [BOute: Cost-Efficient LLM Serving with Heterogeneous LLMs and GPUs via Multi-Objective Bayesian Optimization](2026-2602.10729-boute-heterogeneous-model-gpu-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  問い合わせごとのモデル振り分けと異種GPU上のモデル配置・並列化を多目的ベイズ最適化で同時に探索し、品質制約下の遅延と運用費を削減する。

- **2026-04 · [Cascadia: An Efficient Cascade Serving System for Large Language Models](2025-2506.04203-cascadia-cascade-serving-routing-deployment.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  モデルカスケードの経路選択、GPU資源配分、並列構成を二段階最適化で共同設計し、品質維持下で遅延SLOと処理性能を改善する。

- **2026-09 · [Astrolabe: Balancing Load in LLM Serving with Randomized Prediction-Guided Scheduling](2025-2508.03611-block-predictive-load-balancing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  出力長予測とインスタンス局所シミュレーションを2択無作為配送へ統合し、KV移送なしでLLMクラスタの負荷分散を改善する。

- **2026-04 · [RouterWise: Joint Resource Allocation and Routing for Latency-Aware Multi-Model LLM Serving](2026-2604.10907-routerwise-resource-allocation-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GPU割当とプロンプト振り分けを構成別遅延モデルと双対価格で共同最適化し、同一クラスタでも配備構成がSLO下の達成品質を最大87%変えることを示す。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Token Latency Fairness: Performance Isolation for Multi-Tenant LLM Serving](2026-2609.18112-fairinference-token-latency-fairness-multitenant.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分離実行比δ以内のトークン遅延を保証するdeadline スケジューラとKV予約を統合し、高需要テナント下のp99 遅延 isolationを実現する。

- **2026-06 · [HW-Router: Hardware-Aware Routing for Scalable Multi-LLM Serving](2026-2608.14575-hw-router-hardware-aware-multi-llm-serving.md)**  
  実装：[✓](https://github.com/UCF-ML-Research/HW-Router) ・ リポジトリ内被引用：0  
  実時間のキュー・KVキャッシュ・TTFT/TPOTを遅延予測へ統合し、複数LLMルーティングのSLOとGPU負荷均衡を改善する。

- **2026-05 · [Tackling the Data-Parallel Load Balancing Bottleneck in LLM Serving: Practical Online Routing at Scale](2026-2605.06113-balanceroute-data-parallel-online-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  同期障壁を持つデータ並列デコードで、各ワーカーの安全余裕をFスコアで評価して新規要求を割り当て、KV負荷の偏りと障壁待ちを抑えるオンラインルータBalanceRouteを提案する。

- **2026-05 · [Optimus: Elastic Decoding for Efficient Diffusion LLM Serving](2026-2605.24832-optimus-elastic-decoding-diffusion-llm-serving.md)**  
  実装：[✓](https://github.com/dubcyfor3/Optimus) ・ リポジトリ内被引用：0  
  拡散LLMのブロックを再学習なしでチャンク化し、GPU飽和と有効トークン率を見ながら復号粒度を動的変更して負荷変動へ追従する。

- **2026-01 · [RAPID-Serve: Resource-efficient and Accelerated P/D Intra-GPU Disaggregation](2026-2601.11822-rapid-serve-intra-gpu-pd-disaggregation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  同一GPU内でプリフィル/デコードを非lockstep並行実行し、共有KVとCU maskingでSLOと利用率を両立、MI300X実機で有効スループット平均4.9倍を報告。

- **2025-11 · [DOPD: A Dynamic PD-Disaggregation Architecture for Maximizing Goodput in LLM Inference Serving](2025-2511.20982-dopd-dynamic-pd-disaggregation.md)**  
  実装：[✓](https://github.com/liao4s/DOPD) ・ リポジトリ内被引用：0  
  負荷予測と解析的な最適P/D比でプリフィル/デコード instanceを動的再構成し、8x H100実機で有効スループット最大1.5倍・SLO達成99.4%を報告。

### 2年前（2024-10〜2025-09）

- **2025-05 · [Prism: Unleashing GPU Sharing for Cost-Efficient Multi-LLM Serving](2025-2505.04021-prism-gpu-sharing-multi-llm-serving.md)**  
  実装：[✓](https://github.com/ovg-project/kvcached) ・ リポジトリ内被引用：15  
  GPU物理メモリをモデル横断で動的再配分し、空間共有と時間共有を負荷に応じて切り替える多モデル提供基盤。

- **2025-04 · [SLOs-Serve: Optimized Serving of Multi-SLO LLMs](2025-2504.08784-slos-serve-multi-slo-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  段階別SLOを動的計画法で扱い、チャンク化プリフィル・投機的デコード・入場制御・レプリカルーティングを統合してGPU当たり容量を平均2.2倍改善する。

- **2025-01 · [AdaServe: Accelerating Multi-SLO LLM Serving with SLO-Customized Speculative Decoding](2025-2501.12162-adaserve-multi-slo-speculative-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  GPU検証予算を各リクエストのSLO達成用トークンへ優先配分し、残余をスループット向上へ回す投機的デコード配信で、SLO違反を最大4.3倍削減する。

- **2025-07 · [Nexus: Proactive Intra-GPU Disaggregation of Prefill and Decode in LLM Serving](2025-2507.06608-nexus-proactive-intra-gpu-disaggregation.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  同一GPU内でプリフィル/デコードをproactiveにSM分割し、計算飽和とメモリ帯域競合をモデル化してvLLM比最大2.2倍スループット・20倍TTFT改善を達成する。

- **2025-04 · [semi-PD: Towards Efficient LLM Serving via Phase-Wise Disaggregated Computation and Unified Storage](2025-2504.19867-semi-pd-phase-wise-disaggregated-unified-storage.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  入力処理と逐次生成の計算をSM単位で分離しつつ高帯域メモリを共有し、完全分離方式のKV転送と保存容量の偏りを除いてエンドツーエンド遅延を最大2.58倍改善する。
<!-- survey:auto:end -->
