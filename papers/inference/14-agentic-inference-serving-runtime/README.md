# Agentic Inference / Serving Runtime

ツール呼出し、長寿命セッション、複数LLM・複数エージェントのワークフロー、長い待機時間と再入場を前提に、エージェント推論の資源・状態・GPU配置・KV再利用を最適化するシステム研究をまとめる。

## 分類境界

主要貢献がtool-usingまたはmulti-agent workflowの実行特性を利用した資源管理、状態管理、スケジューリング、配置、KV再利用、OS/runtime制御である研究を含め、単にagentを評価対象に使うだけの一般serving・一般KV手法は含めない。

### 含める研究

- ツール待機・再入場を含む長寿命agent session管理
- multi-agent／multi-LLM workflowのGPU配置・スケジューリング
- agent workflow固有のKV・OS・sandbox資源管理

### 含めない研究

- 独立requestだけを扱う一般LLM serving
- agentを単なるワークロードとして使うだけでagent固有機構を持たない研究

## 近傍系統

- [11-llm-serving-scheduling-disaggregation](../11-llm-serving-scheduling-disaggregation/)
- [07-kv-cache-optimization-compression](../07-kv-cache-optimization-compression/)
- [10-kv-cache-offload-recomputation](../10-kv-cache-offload-recomputation/)

<!-- survey:auto:start -->
## 自動生成の論文一覧（24本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-02 · [ThunderAgent: A Simple, Fast and Program-Aware Agentic Inference System](2026-2602.13692-thunderagent-a-simple-fast-and-program-aware-agentic-inference-system.md)**  
  実装：[✓](https://github.com/ThunderAgent-org/ThunderAgent) ・ リポジトリ内被引用：11  
  エージェントの推論・ツール実行を独立要求ではなく永続プログラムとして追跡し、KVキャッシュの一時停止・復帰、GPU間移動、ツール環境の先行準備と回収を協調させ、配信スループットを最大3.58倍改善する。

- **2026-06 · [CacheWise: Understanding Workloads and Optimizing KVCache Management for Efficiently Serving LLM Coding Agents](2026-2606.16824-cachewise-understanding-workloads-and-optimizing-kvcache-management-for-efficiently-serving-llm-coding-agents.md)**  
  実装：[✓](https://github.com/cachewise-project/cachewise-coding-traces) ・ リポジトリ内被引用：4  
  実コーディングエージェントの接頭辞局所性とツール待ち時間を利用し、接頭辞優先スケジューリングと予測型KV追い出しでセッション完了を最大3.5倍改善。

- **2026-07 · [Agentic Coding in the Wild: Characterizing GitHub Copilot Traces at Production Scale](2026-2608.00101-agentic-coding-production-scale-characterization.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  1350万GitHub Copilotセッションを解析し、直列的なLLM↔ツール連鎖、入力偏重、KVキャッシュの境界崩壊、長いターン間遊休を定量化してエージェント向け資源管理の設計根拠を示す。

- **2026-05 · [Idleness is Relative: Exploiting Tool-Call Idle Windows for Offloading in Agentic Systems with MORI](2026-2606.00866-mori.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  MORIはエージェントの直近の推論・ツール待機時間から相対アイドル度を求め、KVキャッシュをGPUとCPU DRAMへ容量適応的に配置して、高負荷時のスループットと応答性を改善する。

- **2026-03 · [Efficient LLM Serving for Agentic Workflows: A Data Systems Perspective](2026-2603.16104-efficient-llm-serving-agentic-workflows-helium.md)**  
  実装：[✓](https://github.com/mlsys-io/helium_demo) ・ リポジトリ内被引用：3  
  エージェントワークフローを問い合わせ計画として解析し、共通部分削除、結果・KVの先行キャッシュ、接頭辞構造を見た費用認識スケジューリングを統合して、KVFlow比最大1.56倍、複合Tradingで最大1.34倍高速化する。

- **2026-05 · [Agentic AI Workload Characteristics](2026-2605.26297-agentic-ai-workload-characteristics.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  ReAct型エージェントを追跡し、高い文脈再利用により実行がデコード支配となる一方、長寿命KV状態・再入場・ツール失敗が主要なシステム負荷になることを実測した研究。

- **2026-02 · [AgentCgroup: Understanding and Controlling OS Resources of AI Agents](2026-2602.09345-agentcgroup-understanding-and-controlling-os-resources-of-ai-agents.md)**  
  実装：[✓](https://github.com/eunomia-bpf/agentcgroup) ・ リポジトリ内被引用：2  
  AIエージェント144課題のOS資源変動を測定し、OS処理55〜60%、メモリピーク最大15.4倍を確認。ツール呼出し単位cgroupとeBPF制御で競合時の生存率100%と高優先度P95割当遅延29%削減を示す。

- **2026-08 · [Adaptive KV Retention for LLM Agents at Human-Approval Timescales](2026-2608.30830-adaptive-kv-retention-for-llm-agents-at-human-approval-timescales.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  人間承認で長時間停止するエージェントのKVをHBM・CPU DRAM・破棄の三段階で管理し、各選択をGPU機会費用へ換算して負荷に応じた保持期限を決める。

- **2026-07 · [Rethinking AI Cloud Infrastructure for Agentic Serving Systems with the Aries Experimentation Framework](2026-2607.29069-rethinking-ai-cloud-infrastructure-for-agentic-serving-systems-with-the-aries-experimentation-framework.md)**  
  実装：[✓](https://github.com/hyscale-lab/aries) ・ リポジトリ内被引用：1  
  AriesはLLM推論、ハーネス、状態付きツールを一つのエージェント軌跡として計測し、ツール待ち、長期文脈、サンドボックスの瞬間的な資源需要を同じタスク進捗へ結び付ける実験基盤である。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Speculative Macro Commit for Faster Tool-Using Agents](2026-2609.03236-speculative-macro-commit-for-faster-tool-using-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ドラフトモデルが隔離環境でツール操作列を先行実行し、権威モデルが先頭操作を確認したマクロだけ後続操作と観測をまとめて確定して、大型モデル呼出しとツール待ちを減らす。

- **2026-09 · [SARA: SLO-Aware Resource Allocation for Disaggregated Agentic LLM Services](2026-2609.26763-sara.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SARAは、プリフィルとデコードを分離する大規模言語モデル推論で、ハードウェアの列挙や経験的な割当だけに頼らず、サービス水準目標（Service-Level Objective; SLO）を満たすための必要資源量を数理モデルから直接求める資源配分方式である。

- **2026-09 · [PipeSwift: Revisiting Pipeline Parallelism for Large-Scale Completion-Oriented Agentic LLM Serving](2026-2609.16491-pipeswift-pipeline-parallel-agentic-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント推論のJCTをプリフィルとデコードの均衡問題として捉え直し、JCT指向スケジューリングとMTP統合パイプライン並列で64基H800上の360B級MoE処理を高速化する。

- **2026-09 · [Memory Compression for High-Fanout Agent Sandboxes](2026-2609.11294-agentzip-memory-compression-high-fanout-agent-sandboxes.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AgentZipは共有テンプレートと兄弟サンドボックスの類似性を使ってページを圧縮し、LLM応答待ちに圧縮、再利用前に復元先読みする。16並列ロールアウトでサンドボックス所有メモリを88.55%削減した。

- **2026-09 · [LIMBO: Lifelong Inference-Time Memory and Budget Optimization for LLM Agents](2026-2609.14138-limbo-lifelong-inference-time-memory-and-budget-optimization-for-llm-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  経験再生方式と生成予算を軽量な文脈付きバンディットでタスクごとにオンライン選択し、生涯学習エージェントの精度を保ちながら推論コストを削減する。

- **2026-09 · [End-to-End Latency-Minimizing and Load-Balanced Request Scheduling for Edge LLM Inference in Agentic AI Services](2026-2609.17193-end-to-end-latency-minimizing-and-load-balanced-request-scheduling-for-edge-llm-inference-in-agentic-ai-services.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キー・バリューの量と滞在時間、リアプノフ長期制約、遅延報酬再配分を組み合わせ、分散エッジ推論の遅延と負荷分散を同時最適化する割当方式。

- **2026-09 · [BIO-MEMART: Biometric-Aware KV Cache Memory for Multi-User LLM Agents](2026-2609.08566-bio-memart-biometric-aware-kv-cache-memory-for-multi-user-llm-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共有KVキャッシュ記憶を意味類似度だけで検索せず、生体認証で所有者候補を先に絞ってからMemArtの検索・KV再利用を行う物理ユーザー認可層。

- **2026-08 · [AsymSpec: Context-Asymmetric Speculative Decoding for Agentic LLMs](2026-2608.26004-asymspec-context-asymmetric-speculative-decoding-for-agentic-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  軽量ドラフターだけが完全文脈を読み、完全/圧縮文脈のロジット差δと文脈発散連動の受理ゲートで、圧縮文脈しか見ない大規模検証器の精度を回復する非対称推測復号。

- **2026-07 · [Compute Globally, Materialize Locally: The Memory Contract of Sparse Event-KV](2026-2607.23693-compute-globally-materialize-locally-the-memory-contract-of-sparse-event-kv.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  疎なイベントKV管理は「残したイベントが、生成元の観測を捨てても役に立つ」と暗黙に仮定する。本論文は、配信トークンと位置を完全に同一にしたドナー対で、事前計算時の元値だけを変え、下流KVが見えない元値を保持する意味的具現化を確認した。

- **2026-06 · [Towards Direct Latent-Space Synthesis for Parallel Branches in LLM-Agent Workflows](2026-2606.14672-towards-direct-latent-space-synthesis-for-parallel-branches-in-llm-agent-workflows.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  並列エージェントの生成済みKVを位置再符号化・キャッシュ写像・合成器LoRAで直接統合し、再プリフィルを省いて9課題中7課題で品質を維持・改善しつつ最初のトークンまでを2.5〜11倍高速化する。

- **2026-05 · [GraphFlow: A Graph-Based Workflow Management for Efficient LLM-Agent Serving](2026-2605.22566-graphflow-agent-workflow-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共有操作グラフからエージェント手順を動的生成し、操作単位の差分KV状態で約4倍のメモリ削減を狙うエージェント・サービング基盤。

- **2026-05 · [2026-2606.01065-leyline-kv-cache-directives-for-agentic-inference](2026-2606.01065-leyline-kv-cache-directives-for-agentic-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来のKVキャッシュ管理は、プロンプト到着後は末尾へトークンが追加され続けるチャット型負荷を暗黙に前提とする。そのため完全一致する接頭辞を再利用する接頭辞キャッシュや、古いKVを前から追い出す方式が成立する。

- **2026-04 · [Scepsy: Serving Agentic Workflows Using Aggregate LLM Pipelines](2026-2604.15186-scepsy-serving-agentic-workflows-using-aggregate-llm-pipelines.md)**  
  実装：[✓](https://github.com/anon/Scepsy) ・ リポジトリ内被引用：0  
  LLMごとの安定した相対負荷を集約パイプライン化し、GPU分数・テンソル並列・複製数・配置を共同探索して任意の複数LLMエージェント処理を効率化する。

### 2年前（2024-10〜2025-09）

- **2025-07 · [KVFlow: Efficient Prefix Caching for Accelerating LLM-Based Multi-Agent Workflows](2025-2507.07400-kvflow.md)**  
  実装：✓ ・ リポジトリ内被引用：25  
  エージェント実行グラフから将来再利用を予測してKV追出しとCPU→GPU先読みを制御し、SGLang HiCache比最大2.19倍高速化。

- **2025-06 · [The Cost of Dynamic Reasoning: Demystifying AI Agents and Test-Time Scaling from an AI Infrastructure Perspective](2025-2506.04301-cost-dynamic-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  この構造は能力を上げる一方、通常の単一ターン推論を前提に設計されたGPUサービングでは、長い逐次依存、外部ツール待ち、繰り返しプリフィル、可変長生成を生み、平均利用率だけでは実コストを捉えにくい。代表結果では、HotpotQAやMATHのCPU・外部ツール待ちが実行時間の最大54.5%を占める条件があり、LLM実行中も復号がGPU時間の74.1%を占める。
<!-- survey:auto:end -->
