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
## 自動生成の論文一覧（81本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/14-agentic-inference-serving-runtime/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-02 · [ThunderAgent: A Simple, Fast and Program-Aware Agentic Inference System](2026-2602.13692-thunderagent-a-simple-fast-and-program-aware-agentic-inference-system.md)**  
  実装：[✓](https://github.com/ThunderAgent-org/ThunderAgent) ・ リポジトリ内被引用：21  
  エージェントの推論・ツール実行を独立要求ではなく永続プログラムとして追跡し、KVキャッシュの一時停止・復帰、GPU間移動、ツール環境の先行準備と回収を協調させ、配信スループットを最大3.58倍改善する。

- **2026-06 · [CacheWise: Understanding Workloads and Optimizing KVCache Management for Efficiently Serving LLM Coding Agents](2026-2606.16824-cachewise-understanding-workloads-and-optimizing-kvcache-management-for-efficiently-serving-llm-coding-agents.md)**  
  実装：[✓](https://github.com/cachewise-project/cachewise-coding-traces) ・ リポジトリ内被引用：9  
  実コーディングエージェントの接頭辞局所性とツール待ち時間を利用し、接頭辞優先スケジューリングと予測型KV追い出しでセッション完了を最大3.5倍改善。

- **2026-05 · [Idleness is Relative: Exploiting Tool-Call Idle Windows for Offloading in Agentic Systems with MORI](2026-2606.00866-mori.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  MORIはエージェントの直近の推論・ツール待機時間から相対アイドル度を求め、KVキャッシュをGPUとCPU DRAMへ容量適応的に配置して、高負荷時のスループットと応答性を改善する。

- **2026-03 · [Efficient LLM Serving for Agentic Workflows: A Data Systems Perspective](2026-2603.16104-efficient-llm-serving-agentic-workflows-helium.md)**  
  実装：[✓](https://github.com/mlsys-io/helium_demo) ・ リポジトリ内被引用：7  
  エージェントワークフローを問い合わせ計画として解析し、共通部分削除、結果・KVの先行キャッシュ、接頭辞構造を見た費用認識スケジューリングを統合して、KVFlow比最大1.56倍、複合Tradingで最大1.34倍高速化する。

- **2025-11 · [Sherlock: Reliable and Efficient Agentic Workflow Execution](2025-2511.00330-sherlock-reliable-and-efficient-agentic-workflow-execution.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  反実仮想故障注入で脆弱節点へだけ検証器を置き、検証中に後続処理を投機実行して必要時だけ巻き戻すSherlock。平均精度+18.3%、検証費用-26.0%、検証完了時間最大-48.7%。

- **2026-07 · [Agentic Coding in the Wild: Characterizing GitHub Copilot Traces at Production Scale](2026-2608.00101-agentic-coding-production-scale-characterization.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  1350万GitHub Copilotセッションを解析し、直列的なLLM↔ツール連鎖、入力偏重、KVキャッシュの境界崩壊、長いターン間遊休を定量化してエージェント向け資源管理の設計根拠を示す。

- **2025-12 · [Optimizing Agentic Language Model Inference via Speculative Tool Calls](2025-2512.15834-optimizing-agentic-language-model-inference-via-speculative-tool-calls.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  ツール呼出しを「LLMが確定してから実行する」直列経路から外し、小型モデルが次の呼出しを先読みして外部処理を本体生成と重ねる。クライアント側だけでも6〜21%の時間短縮を報告し、ツールが短い条件では推論エンジン統合がさらに2〜3%を削る。

- **2026-05 · [Agentic AI Workload Characteristics](2026-2605.26297-agentic-ai-workload-characteristics.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  ReAct型エージェントを追跡し、高い文脈再利用により実行がデコード支配となる一方、長寿命KV状態・再入場・ツール失敗が主要なシステム負荷になることを実測した研究。

- **2026-04 · [KAIROS: Stateful, Context-Aware Power-Efficient Agentic Inference Serving](2026-2604.16682-kairos-stateful-context-aware-power-efficient-agentic-inference-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  エージェントの文脈成長を見てGPU周波数・同時実行数・配置を共同制御し、スラッシングを避けながら単一インスタンス平均27%、複数インスタンス46.3%の電力を削減する。

- **2026-01 · [Nalar: Workflow-Aware Management of Agentic Applications](2026-2601.05109-nalar-workflow-aware-management-of-agentic-applications.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  複数の言語モデルエージェントが計画、検索、コード生成、試験などを繰り返す処理では、一つの利用者要求が多段階の作業へ分かれ、途中結果によって分岐や再試行が発生する。個々の言語モデルの生成速度だけを改善しても、外部ツールの待機、複数エージェントの依存関係、GPUメモリに残る鍵・値キャッシュ、資源の偏りによって、要求全体の終了時間が長くなる。

- **2026-05 · [Leyline: KV Cache Directives for Agentic Inference](2026-2606.01065-leyline-kv-cache-directives-for-agentic-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  従来のKVキャッシュ管理は、プロンプト到着後は末尾へトークンが追加され続けるチャット型負荷を暗黙に前提とする。そのため完全一致する接頭辞を再利用する接頭辞キャッシュや、古いKVを前から追い出す方式が成立する。

- **2026-05 · [Irminsul: MLA-Native Position-Independent Caching for Agentic LLM Serving](2026-2605.05696-irminsul-mla-native-position-independent-caching-for-agentic-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  Irminsulは、複数ターンのエージェント型LLMサービングで、トークン内容は同じなのにプロンプト内の位置が変わるためKVキャッシュを再利用できない問題を扱う。システム変数、検索文書、ツール出力、会話の圧縮結果が途中に挿入されると、残りの大部分が以前と同じ内容でも、最初の不一致以降は再計算になる。

- **2025-11 · [Aragog: Just-in-Time Model Routing for Scalable Serving of Agentic Workflows](2025-2511.20975-aragog-just-in-time-model-routing-for-scalable-serving-of-agentic-workfl.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  エージェント型ワークフローは、生成、批評、修正、ツール呼び出し、結果統合などを有向非巡回グラフ（Directed Acyclic Graph; DAG）で結んだ実行系列である。

- **2026-03 · [AVO: Agentic Variation Operators for Autonomous Evolutionary Search](2026-2603.24517-avo-agentic-variation-operators-for-autonomous-evolutionary-search.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  AVOは進化的プログラム探索の変異演算子を固定的なLLM生成呼出しから、過去の実装、ハードウェア資料、実行・性能測定へ自律的にアクセスしてコードの修正・検証を反復するエージェントへ置き換える。NVIDIA B200上のBF16注意カーネルを7日間自律改善し、40の成功版を記録。

- **2026-02 · [AgentCgroup: Understanding and Controlling OS Resources of AI Agents](2026-2602.09345-agentcgroup-understanding-and-controlling-os-resources-of-ai-agents.md)**  
  実装：[✓](https://github.com/eunomia-bpf/agentcgroup) ・ リポジトリ内被引用：2  
  AIエージェント144課題のOS資源変動を測定し、OS処理55〜60%、メモリピーク最大15.4倍を確認。ツール呼出し単位cgroupとeBPF制御で競合時の生存率100%と高優先度P95割当遅延29%削減を示す。

- **2026-08 · [Adaptive KV Retention for LLM Agents at Human-Approval Timescales](2026-2608.30830-adaptive-kv-retention-for-llm-agents-at-human-approval-timescales.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  人間承認で長時間停止するエージェントのKVをHBM・CPU DRAM・破棄の三段階で管理し、各選択をGPU機会費用へ換算して負荷に応じた保持期限を決める。

- **2026-07 · [Rethinking AI Cloud Infrastructure for Agentic Serving Systems with the Aries Experimentation Framework](2026-2607.29069-rethinking-ai-cloud-infrastructure-for-agentic-serving-systems-with-the-aries-experimentation-framework.md)**  
  実装：[✓](https://github.com/hyscale-lab/aries) ・ リポジトリ内被引用：1  
  AriesはLLM推論、ハーネス、状態付きツールを一つのエージェント軌跡として計測し、ツール待ち、長期文脈、サンドボックスの瞬間的な資源需要を同じタスク進捗へ結び付ける実験基盤である。

- **2026-05 · [GraphFlow: A Graph-Based Workflow Management for Efficient LLM-Agent Serving](2026-2605.22566-graphflow-agent-workflow-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  共有操作グラフからエージェント手順を動的生成し、操作単位の差分KV状態で約4倍のメモリ削減を狙うエージェント・サービング基盤。

- **2026-04 · [Scepsy: Serving Agentic Workflows Using Aggregate LLM Pipelines](2026-2604.15186-scepsy-serving-agentic-workflows-using-aggregate-llm-pipelines.md)**  
  実装：[✓](https://github.com/anon/Scepsy) ・ リポジトリ内被引用：1  
  LLMごとの安定した相対負荷を集約パイプライン化し、GPU分数・テンソル並列・複製数・配置を共同探索して任意の複数LLMエージェント処理を効率化する。

- **2026-03 · [SpecEyes: Accelerating Agentic Multimodal LLMs via Speculative Perception and Planning](2026-2603.23483-speceyes-accelerating-agentic-multimodal-llms-via-speculative-perception.md)**  
  実装：[✓](https://github.com/MAC-AutoML/SpecEyes) ・ リポジトリ内被引用：1  
  本研究は、画像を一度だけ入力して答える通常の視覚言語モデルではなく、画像の拡大、切り出し、追加観察などの視覚ツールを複数回呼び出すエージェント型マルチモーダル大規模言語モデルの応答遅延を対象とする。提案方式SpecEyesは、ツールを必要としない質問を早期に見つけ、軽量な視覚言語モデルの回答をそのまま返す。

- **2026-03 · [Orla: A Library for Serving LLM-Based Multi-Agent Systems](2026-2603.13605-orla-a-library-for-serving-llm-based-multi-agent-systems.md)**  
  実装：[✓](https://github.com/dorcha-inc/orla) ・ リポジトリ内被引用：1  
  分類段階をQwen3-4B、重い段階をQwen3-8Bへ割り当てた異種構成は、単一Qwen3-8Bの比較対象に対し壁時計時間38%、平均完了時間60%、推定推論費用35%を削減した。

- **2025-11 · [Tree Training: Accelerating Agentic LLMs Training via Shared Prefix Reuse](2025-2511.00413-tree-training-accelerating-agentic-llms-training-via-shared-prefix-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  エージェント型大規模言語モデルの学習軌跡が共有接頭辞を持つ木になることを利用し、各枝を独立学習する際の順伝播・逆伝播の重複を除く。深さ優先直列化、木に沿った注意・状態伝播、枝数に応じた損失重み付け、微分可能な分割境界を組み合わせ、学習目的を保ちながら計算を一度にする。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [Speculative Macro Commit for Faster Tool-Using Agents](2026-2609.03236-speculative-macro-commit-for-faster-tool-using-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ドラフトモデルが隔離環境でツール操作列を先行実行し、権威モデルが先頭操作を確認したマクロだけ後続操作と観測をまとめて確定して、大型モデル呼出しとツール待ちを減らす。

- **2026-09 · [SARA: SLO-Aware Resource Allocation for Disaggregated Agentic LLM Services](2026-2609.26763-sara.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの分離型推論では、入力をまとめて処理する事前充填（プリフィル）、生成された鍵・値キャッシュ（KV キャッシュ）の転送、出力を逐次生成する復号（デコード）を別々の装置群へ配置する。原著の要旨は段階別SLO予測の平均誤差5%未満、同じ配備費用で既存比較方式より平均26.6%高い有効処理率を報告する。

- **2026-09 · [RR-Evict: Fine-Grained Prefix Cache Eviction beyond LRU for Agentic LLM Serving](2026-2609.32278-rr-evict-fine-grained-prefix-cache-eviction-beyond-lru-for-agentic-llm-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の最近最少使用方式（Least Recently Used、LRU）では、同じエージェントのキャッシュ木に属するノードの最近使用時刻がほぼ同時に更新され、削除対象が特定のエージェントに偏る。

- **2026-09 · [Pull: Lazy Materialization of Working Memory for Stateful LLM Conversations](2026-2609.14773-pull-lazy-working-memory-materialization.md)**  
  実装：[✓](https://github.com/wulun811/kongmen-pull) ・ リポジトリ内被引用：0  
  長期対話を決定論的な索引で管理し、質問ごとに必要な原文ターンだけを可逆的に実体化して入力トークンを削減するセッションルータ。

- **2026-09 · [PipeSwift: Revisiting Pipeline Parallelism for Large-Scale Completion-Oriented Agentic LLM Serving](2026-2609.16491-pipeswift-pipeline-parallel-agentic-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント推論のJCTをプリフィルとデコードの均衡問題として捉え直し、JCT指向スケジューリングとMTP統合パイプライン並列で64基H800上の360B級MoE処理を高速化する。

- **2026-09 · [PackServe: SLO-Aware Request Scheduling for Agentic LLM Serving at Scale](2026-2609.33224-packserve-slo-aware-request-scheduling-for-agentic-llm-serving-at-scale.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PackServeは、エージェント型大規模言語モデル（LLM）の複数要求をGPU推論インスタンスへ振り分けるゲートウェイ型スケジューラである。64台のNVIDIA H20を使った再生実験では、比較方式より13.0～24.6%少ない稼働GPU時間で評価したTPOT目標を満たした。

- **2026-09 · [Memory Compression for High-Fanout Agent Sandboxes](2026-2609.11294-agentzip-memory-compression-high-fanout-agent-sandboxes.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AgentZipは共有テンプレートと兄弟サンドボックスの類似性を使ってページを圧縮し、LLM応答待ちに圧縮、再利用前に復元先読みする。16並列ロールアウトでサンドボックス所有メモリを88.55%削減した。

- **2026-09 · [LIMBO: Lifelong Inference-Time Memory and Budget Optimization for LLM Agents](2026-2609.14138-limbo-lifelong-inference-time-memory-and-budget-optimization-for-llm-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  経験再生方式と生成予算を軽量な文脈付きバンディットでタスクごとにオンライン選択し、生涯学習エージェントの精度を保ちながら推論コストを削減する。

- **2026-09 · [From Monolithic Blending to Agentic Orchestration: Dynamic Response for Conversational Assistants at Scale](2026-2609.05758-from-monolithic-blending-to-agentic-orchestration-dynamic-response-for-c.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、月間数百万件の会話を扱う宿泊予約サービスの顧客支援において、回答方針の選択と文章の生成を一つの大規模言語モデルに任せる方式から、二つのモデルと型付きツールで役割を分ける方式への移行を報告する。対象は11言語、全体応答時間の90パーセンタイルを10秒以内に抑える本番システムである。

- **2026-09 · [End-to-End Latency-Minimizing and Load-Balanced Request Scheduling for Edge LLM Inference in Agentic AI Services](2026-2609.17193-end-to-end-latency-minimizing-and-load-balanced-request-scheduling-for-edge-llm-inference-in-agentic-ai-services.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キー・バリューの量と滞在時間、リアプノフ長期制約、遅延報酬再配分を組み合わせ、分散エッジ推論の遅延と負荷分散を同時最適化する割当方式。

- **2026-09 · [DynBranch: Speculative Subgraph Reuse for Dynamic Agentic LLM Serving](2026-2609.31047-dynbranch-speculative-subgraph-reuse-for-dynamic-agentic-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DynBranchは、エージェント型大規模言語モデルの推論基盤で生じる分岐解決障壁（branch-resolution barrier）を短縮するサービング方式である。4枚のH200 NVLでQwen3-32Bを提供する評価では、4種類のエージェント処理の各条件で、外部比較方式のうち最良のものに対して低負荷時の平均遅延を14～32%削減した。

- **2026-09 · [DeepEdu-v1: Efficient and Scalable Agentic LLMs for Vietnamese Education](2026-2609.31568-deepedu-v1-efficient-and-scalable-agentic-llms-for-vietnamese-education.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  教育アプリケーション論文という題名だが、SCRはLLM推論基盤へ独立に適用できる方式であり、本サーベイではこちらを中心に扱う。

- **2026-09 · [BIO-MEMART: Biometric-Aware KV Cache Memory for Multi-User LLM Agents](2026-2609.08566-bio-memart-biometric-aware-kv-cache-memory-for-multi-user-llm-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共有KVキャッシュ記憶を意味類似度だけで検索せず、生体認証で所有者候補を先に絞ってからMemArtの検索・KV再利用を行う物理ユーザー認可層。

- **2026-09 · [Attuner: Recomputation-Free Agentic Context KV Reuse](2026-2609.36722-attuner-recomputation-free-agentic-context-kv-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェントがスキルの説明、検索した文書、過去の記憶をリクエストごとに組み立てると、同じ資料を何度もプリフィルすることになる。再計算を減らす代わりに、複数資料から正しい証拠を選ぶ能力が落ちる問題がある。学習済みQuery更新を投影重みに統合するため、推論時にFull teacherや保存済み資料KVの再計算は不要である。

- **2026-08 · [TideRL: Boosting Agentic RL Goodput with Readiness-Aware Scheduling](2026-2608.10402-tiderl-boosting-agentic-rl-goodput-with-readiness-aware-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TideRLは、言語モデルを外部環境と何度も対話させて強化学習する際、GPUを稼働させるだけでは学習の進捗が増えないという問題を扱う。さらに一つの課題が終了するまでのターン数は予測しにくい。

- **2026-08 · [Read Less, Solve More: Token-Efficient Sparse Reading for AI Agents](2026-2608.22237-read-less-solve-more-token-efficient-sparse-reading-for-ai-agents.md)**  
  実装：[✓](https://github.com/Zedong-Liu/SparseReadingOfficial) ・ リポジトリ内被引用：0  
  これにより入力処理の計算費用と遅延が増えるだけでなく、重要な根拠が埋もれて道具選択や停止判断を誤る場合がある。全文を読むべき表計算や小さいファイルへ無理に適用すると、逆にトークン量が大きく増える例も確認しており、読解判定器はこの負の条件を避けるための主要機構である。

- **2026-08 · [AsymSpec: Context-Asymmetric Speculative Decoding for Agentic LLMs](2026-2608.26004-asymspec-context-asymmetric-speculative-decoding-for-agentic-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  軽量ドラフターだけが完全文脈を読み、完全/圧縮文脈のロジット差δと文脈発散連動の受理ゲートで、圧縮文脈しか見ない大規模検証器の精度を回復する非対称推測復号。

- **2026-08 · [AOSpec: Action and Observation Co-Speculation for Low-Latency Agent Serving](2026-2608.00881-aospec-action-and-observation-co-speculation-for-low-latency-agent-servi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単純な投機的生成はモデル内部のトークン列を先読みするが、エージェント全体の遅延ではモデル外の実行時間が残る。同じ記録済み軌跡を再生する評価で、通常の逐次実行に比べた平均総遅延削減率は11.8〜32.5%、10ms/トークン条件のp99遅延削減率は42.8%である。

- **2026-07 · [Scalable LLM Agent Tool Access in the Cloud](2026-2607.15593-scalable-llm-agent-tool-access-in-the-cloud.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、LLMエージェントが数百から数千の外部操作を利用する際に、ツール定義を全件プロンプトへ詰め込む方式と、各ツールのMCPサーバへ個別接続する方式の両方が規模の壁に直面することを扱う。

- **2026-07 · [Compute Globally, Materialize Locally: The Memory Contract of Sparse Event-KV](2026-2607.23693-compute-globally-materialize-locally-the-memory-contract-of-sparse-event-kv.md)**  
  実装：[✓](https://github.com/oklen/Compute-Globally-Materialize-Locally) ・ リポジトリ内被引用：0  
  長い会話を続けるエージェントでは、過去の発話やツール結果を一度モデルに読み込ませ、各イベントのKV行を再利用する設計が考えられる。一方、意図的な値非明示の計算指示イベントを追加すると、同じモデルの追随回復率は6%から51%へ増えるが、二値以外の大きな値は保持しにくい。

- **2026-06 · [Towards Direct Latent-Space Synthesis for Parallel Branches in LLM-Agent Workflows](2026-2606.14672-towards-direct-latent-space-synthesis-for-parallel-branches-in-llm-agent-workflows.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  並列エージェントの生成済みKVを位置再符号化・キャッシュ写像・合成器LoRAで直接統合し、再プリフィルを省いて9課題中7課題で品質を維持・改善しつつ最初のトークンまでを2.5〜11倍高速化する。

- **2026-06 · [Toward Scalable LLM-Based Multi-Agent Collaboration: A Dynamic Task Graph Approach with Asynchronous Parallel Execution](2026-80a8722a219c-toward-scalable-llm-based-multi-agent-collaboration-a-dynamic-task-graph.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  意味選別型文脈管理（Semantic-Aware Context Management システム; SACMS）は受信者に関係する文脈のみを配送し、適応型ワークフロー管理器（適応的 Workflow Manager; AWM）が観測負荷を使って優先順位・割当を調整する。

- **2026-06 · [SwarmX: Agentic Scheduling for Low-Latency Agentic Systems](2026-2606.21401-swarmx-agentic-scheduling-for-low-latency-agentic-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単純なラウンドロビンや平均実行時間に基づく割当では、長い要求が特定のキューに集中し、遅延の裾が悪化しやすい。SwarmXは、プロンプトの意味、対象モデル、装置、実行時状態を組み合わせ、要求の推論時間と後続モデル呼び出し数の確率分布を予測するスケジューラである。

- **2026-06 · [Streaming Communication in Multi-Agent Reasoning](2026-2606.05158-streaming-communication-in-multi-agent-reasoning.md)**  
  実装：[✓](https://github.com/EnVision-Research/StreamMA) ・ リポジトリ内被引用：0  
  従来の逐次転送（Serial）は、各エージェントが全推論段階を終えた後に回答全文を渡すため、処理経路が深くなるほど待ち時間が積み上がる。全文を受け取る方式では後期の誤りまで強く条件付けられるが、段階別転送では下流が信頼できる初期部分から独自の推論を始められる。

- **2026-06 · [Libra: Efficient Resource Management for Agentic RL Post-Training](2026-2606.03077-libra-efficient-resource-management-for-agentic-rl-post-training.md)**  
  実装：[✓](https://github.com/NetX-lab/Libra) ・ リポジトリ内被引用：0  
  Libraは、ツール呼び出しを伴う大規模言語モデル（LLM）の強化学習後学習において、軌跡生成（Rollout）と勾配更新（学習）の双方を対象とする資源管理システムである。原著の最大改善はパイプライン処理能力4.2倍、報酬収束までの実時間2.7倍であり、初版の3.0倍・2.5倍と混同してはならない。

- **2026-05 · [Stateful Inference for Low-Latency Multi-Agent Tool Calling](2026-2605.26289-stateful-inference-for-low-latency-multi-agent-tool-calling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、複数のエージェントが道具呼出し（tool calling）を繰り返す大規模言語モデル（LLM）推論で、各ターンの会話履歴がほぼ前ターンの接頭辞になっている点を利用する推論サーバー設計を提案する。

- **2026-05 · [MemReread: Enhancing Agentic Long-Context Reasoning via Memory-Guided Rereading](2026-2605.10268-memreread-enhancing-agentic-long-context-reasoning-via-memory-guided-rer.md)**  
  実装：[✓](https://github.com/iiGray/MemReread) ・ リポジトリ内被引用：0  
  MemRereadは、長い文書を固定容量の作業メモリへ逐次要約するエージェントに、不足した証拠を後から原文で再読する処理を加える研究である。履歴メモリを検索する方式でも、捨てられた情報が履歴に保存されていなければ検索対象にならない。

- **2026-05 · [Energy per Successful Goal: Goal-Level Energy Accounting for Agentic AI Systems](2026-2605.22883-energy-per-successful-goal-goal-level-energy-accounting-for-agentic-ai-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかしエージェント型のシステムでは、利用者の一つの目的を達成するまでに計画の生成、道具の呼び出し、途中結果の検査、失敗後の再試行、最終回答の生成など、複数回の推論が連鎖する。x86の対応した目標集合でOOIは4.34倍、GraceのCPUとGPUを含めたローカル測定では7.63倍となった。

- **2026-05 · [Compiling Agentic Workflows into LLM Weights: Near-Frontier Quality at Two Orders of Magnitude Less Cost](2026-2605.22502-compiling-agentic-workflows-into-llm-weights-near-frontier-quality-at-tw.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この論文が扱うのは、複雑な業務フローチャートに従う対話型エージェントを、毎回外部の制御プログラムから指示される大規模言語モデルとして実装する必要があるのか、という問題である。別の構成としてフローチャート全体を毎回のシステム入力に含める方法もあるが、手順が長くなるほど入力トークンが増える。

- **2026-04 · [Recursive Multi-Agent Systems](2026-2604.25917-recursive-multi-agent-systems.md)**  
  実装：[✓](https://github.com/RecursiveMAS/RecursiveMAS) ・ リポジトリ内被引用：0  
  通常の複数エージェントシステムでは、計画役が文章を生成し、批評役がその文章を読み、解答役が批評を受け取る。文章媒介型の同じ再帰的協調構造（Recursive-TextMAS）に対し、再帰1、2、3ラウンドで平均推論実行時間の相対改善が1.2、1.9、2.4倍へ広がり、外部トークン使用量は34.6%、65.5%、75.6%少なくなると報告する。

- **2026-04 · [Networking-Aware Energy Efficiency in Agentic AI Inference: A Survey](2026-2604.07857-networking-aware-energy-efficiency-in-agentic-ai-inference-a-survey.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、エージェント型人工知能（Agentic AI）の推論時エネルギーを、単一のLLM呼び出しではなく、知覚・推論・行動（Perception–Reasoning–Action）の循環と、端末・エッジ・クラウド間の通信まで含めて分析するサーベイである。著者は計算・メモリ・通信を別々に数え、これらを跨いだ共同設計の必要性を論じる。

- **2026-04 · [MARS: Efficient, Adaptive Co-Scheduling for Heterogeneous Agentic Systems](2026-2604.26963-mars-efficient-adaptive-co-scheduling-for-heterogeneous-agentic-systems.md)**  
  実装：[✓](https://github.com/Afterglow231/MARS_preview) ・ リポジトリ内被引用：0  
  MARSは、複数の大規模言語モデル（LLM）エージェントが同じホストで稼働する際、モデル推論のGPU時間だけでなく、ツール呼び出しで消費されるCPU時間と鍵・値キャッシュ（KV キャッシュ）の保持費用まで同時に制御するサービング方式である。

- **2026-04 · [Hive: A Multi-Agent Infrastructure for Algorithm- and Task-Level Scaling](2026-2604.17353-hive-a-multi-agent-infrastructure-for-algorithm-and-task-level-scaling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  一方、複数エージェントが交互に動く場合は、頻繁に再開する重要エージェントの鍵・値キャッシュ（KVキャッシュ）を残し、まれに呼ばれるエージェントのキャッシュを先に退避する方が有利なことがある。

- **2026-04 · [EvolveRouter: Co-Evolving Routing and Prompt for Multi-Agent Question Answering](2026-2604.05149-evolverouter-co-evolving-routing-and-prompt-for-multi-agent-question-ans.md)**  
  実装：[✓](https://github.com/J-Huang01/EvolveRouter) ・ リポジトリ内被引用：0  
  あるモデルが低い正答率を示す原因は、モデル本体の能力不足だけでなく、与えられた役割指示の不適合にもある。逆に、すべてのエージェントを毎回呼び出す方式は、回答の質が低い参加者まで計算し、応答の待ち時間と呼出費用を増やす。

- **2026-04 · [CascadeDebate: Multi-Agent Deliberation for Cost-Aware LLM Cascades](2026-2604.12262-cascadedebate-multi-agent-deliberation-for-cost-aware-llm-cascades.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、問い合わせを小型LLMから大型LLMへ段階的に委譲するカスケード（cascade）に、必要なときだけ複数エージェントの討論（multi-agent deliberation）を挿入するCascadeDebateを提案する。Llama-3.2のMedQAでは標準カスケード68.20%に対し提案法86.44%を報告する。

- **2026-03 · [CUCo: An Agentic Framework for Compute and Communication Co-design](2026-2603.02376-cuco-an-agentic-framework-for-compute-and-communication-co-design.md)**  
  実装：[✓](https://anonymous.4open.science/r/CUCo-06EC/) ・ リポジトリ内被引用：0  
  既存の分散処理では、行列積や注意計算を高速化する担当と、NCCL通信を高速化する担当が分離されやすい。続いて性能探索の低速経路（slow-path）で、コンパイル・数値照合・実機ベンチマークを通した候補だけを残し、進化的な探索で転送と計算の重なり方を改善する。

- **2026-02 · [Search More, Think Less: Rethinking Long-Horizon Agentic Search for Efficiency and Generalization](2026-2602.22675-search-more-think-less-rethinking-long-horizon-agentic-search-for-effici.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重要なのはモデル内部の注意計算を高速化することではなく、モデルが外部情報を収集するための逐次対話回数と検索の依存鎖を減らす点にある。Qwen3-30B-A3B-Instruct-2507を基盤として学習したSMTL-300は、BrowseComp 48.6%、GAIA 75.7%、XBench-DeepSearch 82.0%を報告する。

- **2026-02 · [LatentMem: Customizing Latent Memory for Multi-Agent Systems](2026-2602.03036-latentmem-customizing-latent-memory-for-multi-agent-systems.md)**  
  実装：[✓](https://github.com/KANABOON1/LatentMem) ・ リポジトリ内被引用：0  
  しかし全エージェントへ同じ履歴や要約を渡すと、役割に無関係な情報が増え、似た指示を共有することで同じ誤りを繰り返す危険がある。これらは同一実験内の比較であり、別のエージェント基盤やGPUで同じ改善が得られる保証ではない。

- **2026-02 · [ClawMobile: Rethinking Smartphone-Native Agentic Systems](2026-2602.22942-clawmobile-rethinking-smartphone-native-agentic-systems.md)**  
  実装：[✓](https://github.com/ClawMobile/ClawMobile) ・ リポジトリ内被引用：0  
  一般的な画面操作型エージェントは、画面を解釈してタップや入力を決めるが、アプリ起動の遅延、画面遷移の非同期性、同じ場所に現れる別の操作対象などにより、言語モデルの計画が正しくても操作が失敗し得る。ClawMobileは、上位の計画と端末制御を分離し、構造化された端末命令を優先して使い、必要な場合だけ画面解釈型のエージェントへ処理を渡す。

- **2026-02 · [AgenticOCR: Parsing Only What You Need for Efficient Retrieval-Augmented Generation](2026-2602.24134-agenticocr-parsing-only-what-you-need-for-efficient-retrieval-augmented-.md)**  
  実装：[✓](https://github.com/OpenDataLab/AgenticOCR) ・ リポジトリ内被引用：0  
  AgenticOCRは、画像を含む長いPDF文書から回答を生成する検索拡張生成（Retrieval-Augmented Generation、RAG）において、検索されたページを丸ごと大規模な生成モデルへ渡す代わりに、質問に必要な領域を選んで拡大・回転・文字認識する方式である。

- **2026-01 · [Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents](2026-2601.01885-agentic-memory-learning-unified-long-term-and-short-term-memory-manageme.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長時間動作するLLMエージェントには、会話や作業をまたいで残す長期記憶（Long-Term メモリ; LTM）と、現在のプロンプト内で参照する短期記憶（Short-Term メモリ; STM）がある。従来は、長期記憶の追加・更新を外部の記憶管理器に任せ、短期文脈の検索・要約は一定間隔や文脈長しきい値で動かすことが多かった。

- **2025-12 · [Transcending Cost-Quality Tradeoff in Agent Serving via Session-Awareness](2025-d84a0fae3606-transcending-cost-quality-tradeoff-in-agent-serving-via-session-awarenes.md)**  
  実装：[✓](https://github.com/robinren03/agserve) ・ リポジトリ内被引用：0  
  従来の単純な接頭辞一致キャッシュや最近使用順の退避では、この特徴を活かしにくい。NeurIPS 2025の実機評価では、AWエージェントでGPT-4oと近い品質を16.5%の費用で達成し、同一費用の費用・品質曲線に対して1.8倍の品質を報告する。

- **2025-11 · [Scaling Graph Chain-of-Thought Reasoning: A Multi-Agent Framework with Efficient LLM Serving](2025-2511.01633-graph-cot-multi-agent-efficient-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Graph-CoTを分類・推論・行動・検索へ分業し、頂点単位KV再利用、優先度追い出し、検索と生成の重畳を組み合わせ、遅延最大90.3%減・スループット最大15.1倍を報告。

- **2025-11 · [O-Mem: Omni Memory System for Personalized, Long Horizon, Self-Evolving Agents](2025-2511.13593-o-mem-omni-memory-system-for-personalized-long-horizon-self-evolving-age.md)**  
  実装：[✓](https://github.com/OPPO-PersonalAI/O-Mem) ・ リポジトリ内被引用：0  
  過去の対話を意味的に近い断片へまとめ、質問に近い断片だけ検索する従来方式にも問題がある。主な結果は、長期対話ベンチマークLoCoMoのGPT-4.1条件でF1がLangMemの48.72から51.67へ、人物記憶のPERSONAMEMでA-Memの59.42から62.99へ改善したことである。

- **2025-11 · [AccelOpt: A Self-Improving LLM Agentic System for AI Accelerator Kernel Optimization](2025-2511.15915-accelopt-a-self-improving-llm-agentic-system-for-ai-accelerator-kernel-o.md)**  
  実装：[✓](https://github.com/zhang677/AccelOpt) ・ リポジトリ内被引用：0  
  機械学習演算カーネルの実行速度は、同じ演算を表すコードでも、タイル形状、メモリ配置、命令選択、演算融合、パイプラインの設計によって大きく変わる。理論ピークに対する平均達成率は、Trainium 1で49%から61%、Trainium 2で45%から59%へ改善した。

### 2年前（2024-11〜2025-10）

- **2025-07 · [KVFlow: Efficient Prefix Caching for Accelerating LLM-Based Multi-Agent Workflows](2025-2507.07400-kvflow.md)**  
  実装：✓ ・ リポジトリ内被引用：51  
  エージェント実行グラフから将来再利用を予測してKV追出しとCPU→GPU先読みを制御し、SGLang HiCache比最大2.19倍高速化。

- **2025-02 · [A-Mem: Agentic Memory for LLM Agents](2025-2502.12110-a-mem-agentic-memory-for-llm-agents.md)**  
  実装：[✓](https://github.com/WujiangXu/A-mem-sys) ・ リポジトリ内被引用：35  
  従来の記憶システムでは、いつ保存し、どの形式で整理し、どの条件で取り出すかを開発者が固定する場合が多い。NeurIPS 2025正式掲載論文では、長期会話の質問応答データで六つの基盤モデルを評価し、特に時間推論や複数会話をまたぐ質問で改善を示した。

- **2025-04 · [Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory](2025-2504.19413-mem0-building-production-ready-ai-agents-with-scalable-long-term-memory.md)**  
  実装：[✓](https://mem0.ai/research) ・ リポジトリ内被引用：31  
  Mem0は、長期にわたり対話を続ける大規模言語モデル（LLM）エージェントに対し、毎回の質問で過去の全会話を読み直す代わりに、今後も必要になる事実だけを抽出・統合・検索する外部記憶基盤を提案する。

- **2025-06 · [The Cost of Dynamic Reasoning: Demystifying AI Agents and Test-Time Scaling from an AI Infrastructure Perspective](2025-2506.04301-cost-dynamic-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  この構造は能力を上げる一方、通常の単一ターン推論を前提に設計されたGPUサービングでは、長い逐次依存、外部ツール待ち、繰り返しプリフィル、可変長生成を生み、平均利用率だけでは実コストを捉えにくい。代表結果では、HotpotQAやMATHのCPU・外部ツール待ちが実行時間の最大54.5%を占める条件があり、LLM実行中も復号がGPU時間の74.1%を占める。

- **2025-01 · [Zep: A Temporal Knowledge Graph Architecture for Agent Memory](2025-2501.13956-zep-a-temporal-knowledge-graph-architecture-for-agent-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  長期エージェントの記憶を、単なる「過去文書の検索」ではなく「時間とともに変わる事実の履歴」として扱う。LongMemEvalsではgpt-4oの全履歴投入60.2%に対して71.2%へ精度を上げつつ、平均文脈長を115k→1.6kトークン、応答遅延を28.9→2.58秒へ削減した。

- **2025-09 · [Batch Query Processing and Optimization for Agentic Workflows](2025-2509.02121-batch-query-processing-and-optimization-for-agentic-workflows.md)**  
  実装：[✓](https://anonymous.4open.science/r/Halo_Demo-BC86/) ・ リポジトリ内被引用：10  
  Haloは「LLM呼出しを1件ずつ速くする」のではなく、同時に走るエージェントワークフロー全体を実行計画として扱う。最新版v2では、同一ツール要求の統合とCPU-GPU協調を加え、強いエージェント基盤に対してバッチ推論最大3.6倍、オンライン処理量最大2.58倍を報告する。

- **2025-05 · [HEXGEN-FLOW: Optimizing LLM Inference Request Scheduling for Agentic Text-to-SQL](2025-2505.05286-hexgen-flow-optimizing-llm-inference-request-scheduling-for-agentic-text.md)**  
  実装：[✓](https://github.com/Relaxed-System-Lab/Hexgen-Flow) ・ リポジトリ内被引用：10  
  本研究は、一つの利用者問い合わせが約20回の大規模言語モデル（LLM）呼び出しを誘発するエージェント型Text-to-SQL処理に対し、問い合わせ全体の応答期限を守る推論スケジューラを設計する。

- **2025-10 · [Speculative Actions: A Lossless Framework for Faster Agentic Systems](2025-2510.04371-speculative-actions-a-lossless-framework-for-faster-agentic-systems.md)**  
  実装：[✓](https://github.com/naimengye/speculative-action) ・ リポジトリ内被引用：9  
  本研究は、LLMを使うエージェント（agentic systems）が環境へ問い合わせを行うたびに待機し、その結果を見てから次の操作を決めるという逐次的なツール呼び出しの待ち時間を短縮する。通常の投機的復号（投機的復号）は、小型モデルが次のトークンを予測し、対象モデルがそれを検証することで生成を高速化する。

- **2025-10 · [FlowMesh: A Service Fabric for Composable LLM Workflows](2025-2510.26913-flowmesh-a-service-fabric-for-composable-llm-workflows.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  LLMワークフローをDAG演算子へ分解し、完全一致の重複排除・実行互換バッチ化・異種GPU配置・無状態ワーカーを一体化して、金銭コスト1.8〜3.8倍、エネルギー1.3〜2.0倍の改善を示す。

- **2025-09 · [ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory](2025-2509.25140-reasoningbank-scaling-agent-self-evolving-with-reasoning-memory.md)**  
  実装：[✓](https://github.com/google-research/reasoning-bank) ・ リポジトリ内被引用：5  
  長期間にわたってウェブ操作やソフトウェア修正を行う大規模言語モデル（LLM）エージェントは、過去に成功した手順を別の課題で再発見したり、既に失敗した操作を繰り返したりする。過去の実行軌跡を丸ごと検索する方式では、現在の課題に関係ない画面遷移や局所的な操作が混ざる。

- **2025-06 · [Agent.xpu: Efficient Scheduling of Agentic LLM Workloads on Heterogeneous SoC](2025-2506.24045-agent-xpu-efficient-scheduling-of-agentic-llm-workloads-on-heterogeneous.md)**  
  実装：[✓](https://github.com/xinming-wei/LLM.xpu) ・ リポジトリ内被引用：5  
  Agent.xpuは、個人端末で複数の言語モデル利用エージェントを同時に動かす際、中央処理装置、統合画像処理装置、ニューラル処理装置を協調させる推論実行基盤である。

- **2025-09 · [Dynamic Speculative Agent Planning](2025-2509.01920-dynamic-speculative-agent-planning.md)**  
  実装：[✓](https://github.com/guanyilin428/Dynamic-Speculative-Planning) ・ リポジトリ内被引用：4  
  動的 投機的 Planning（DSP）は、大規模言語モデル（LLM）を用いたエージェントが一連の計画・操作を逐次生成する際、弱い近似エージェントが未来の複数ステップを先読みし、強い対象エージェントが並列に検証することで全体の完了時間を短縮する方式である。

- **2025-10 · [Staircase Streaming for Low-Latency Multi-Agent Inference](2025-2510.05059-staircase-streaming-for-low-latency-multi-agent-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  前段の提案者が最初の8トークン程度を生成した時点で集約者を起動し、後続の生成と集約を重ねる。提案者の全出力を待たないため、MoAでTTFTを10.6秒から0.47秒、MADで6.70秒から0.45秒へ削減する条件がある。

- **2025-09 · [Nova: Real-Time Agentic Vision-Language Model Serving with Adaptive Cross-Stage Parallelization](2025-2509.21301-nova-real-time-agentic-vision-language-model-serving-with-adaptive-cross.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Novaは、画面画像を見て操作命令を生成する視覚言語エージェント（Vision-Language モデル agent、VLMエージェント）を、単一のGPUで低遅延に提供する推論基盤である。さらに、画像符号器の全重みをGPUへ常駐させず、CPUメモリから層ごとに先読みする。
<!-- survey:auto:end -->
