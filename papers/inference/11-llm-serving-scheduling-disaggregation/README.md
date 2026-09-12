# LLM Serving / Scheduling / Disaggregation

複数requestを複数GPU / nodeで処理するLLM servingについて、request順、batch、prefill / decodeのGPU配分、KV再利用・転送、request移動などを調整し、latencyとresource効率を改善する研究をまとめる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（75本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2025-11 · [Continnum: Efficient and Robust Multi-Turn LLM Agent Scheduling with KV Cache Time-to-Live](2025-2511.02230-continuum-agent-kv-cache-ttl-scheduling.md)**  
  実装：[✓](https://github.com/Hanchenli/vllm-continuum) ・ リポジトリ内被引用：4  
  ツール呼出しを何度も挟むLLMエージェントでは、各ターン終了時にKVキャッシュを追い出すと、次ターンでプリフィルやCPUからの再読込みが必要になるだけでなく、GPUメモリを他要求へ渡した後に待ち行列へ戻るため、ターンごとの待ち時間が累積する。

- **2026-09 · [GreenLLM: SLO-Aware Dynamic Frequency Scaling for Energy-Efficient LLM Serving](2025-2508.16449-greenllm-slo-aware-dvfs-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  本論文は、LLM推論のプリフィルとデコードでは計算特性と許容遅延が異なるのに、既定GPU電力制御が両段階をほぼ一様に扱い、余分な高周波数動作とエネルギー消費を生む問題を扱う。GreenLLMは、入力長で要求を別キューへ振り分けて長いプロンプトによる先頭待ちを避け、プリフィルでは入力長・周波数・待ち行列負荷からSLO内でエネルギー最小のSM周波数を選ぶ。

- **2026-05 · [AlignedServe: Orchestrating Prefix-aware Batching to Build a High-throughput and Computing-efficient LLM Serving System](2026-2605.23389-alignedserve-prefix-aware-batching.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  AlignedServeは、LLMデコードでは同じバッチ内でも系列ごとにKVキャッシュ長が異なり、注意計算時間の長い少数要求が各反復の完了を支配してGPUに反復内の待ちを生む問題を扱う。プリフィル後の要求とKVキャッシュをCPU大容量メモリへいったん蓄え、接頭辞長が近い要求を動的な四分木から密度優先で選んでバッチ化することで、同一反復内の計算量を揃える。

- **2026-07 · [SmartGen: Seamless Disaggregated LLM Inference with Selective KV Cache Transfer](2026-2607.28150-smartgen-selective-kv-cache-transfer.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  SmartGenの狙いは、事前充填（プリフィル）と復号（デコード）を別ノードへ分離したときに生じる「最初のトークンは出たのに、KVキャッシュ（KV キャッシュ）の転送が終わらず2 トークン目が長く出てこない」停止時間を消すことである。通常は事前充填ノードが作ったKVを全量復号ノードへ転送するが、SmartGenはそれを3段階へ分ける。

- **2026-07 · [AugServe: Adaptive Request Scheduling for Augmented Large Language Model Inference Serving](2025-2512.04013-augserve-adaptive-request-scheduling-augmented-llm-inference-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  外部APIや検索、外部モデルを呼び出す拡張LLMでは、生成が途中で停止して外部応答を待ち、その後に同じ要求が再開する。このため通常の到着順スケジューリングでは、長い要求や停止中要求が後続の短い要求を塞ぎ、GPU上に残す・CPUへ退避する・破棄して再計算するというKVキャッシュ処理によって実行時メモリも大きく変動する。

- **2026-06 · [Geometry-Aware Online Scheduling for LLM Serving: From Theoretical Bound to System Practice](2026-2606.22327-geometry-aware-online-scheduling.md)**  
  実装：[✓](https://github.com/Aurora-Kl/Geometry-Aware-Online-Scheduling) ・ リポジトリ内被引用：1  
  SVFはリクエストを「何トークン残っているか」だけでなく、「その間にどれだけKV メモリを占有し続けるか」まで面積として数え、小さいメモリ-時間 体積から実行することで、メモリ-境界なLLM サービングのヘッド-of-line ブロッキングを減らす。

- **2026-06 · [CrossPool: Efficient Multi-LLM Serving for Cold MoE Models through KV-Cache and Weight Disaggregation](2026-2606.24506-crosspool-cold-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  CrossPoolは、複数の低頻度MoEモデルで「常に大きいFFN 重み」と「時々だけ大きくなるKV キャッシュ」を同じHBMへ押し込むのをやめ、重み用GPUとKV用GPUへ分けることで、モデルごとの余ったKV容量を1つの共有プールとして使えるようにする。

- **2026-05 · [RTP-LLM: High-Performance Alibaba LLM Inference Engine](2026-2605.29639-rtp-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Alibabaで実運用されているLLM推論基盤。単一の高速化手法ではなく、入力処理と逐次生成の分離、GPUから分散ストレージまでのKVキャッシュ階層、キャッシュを再利用しやすい要求振り分け、大規模モデルの高速読込、投機的復号、量子化、MoE・画像入力対応を一つの提供基盤へ統合し、実トラフィックを使って各機構の効果を評価する。

- **2026-03 · [MoEless: Efficient MoE LLM Serving via Serverless Computing](2026-2603.06350-moeless-serverless-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  分散MoE推論で一部のエキスパート（エキスパート）へトークンが集中すると、そのエキスパートを担当するGPUだけが遅れて全体の同期待ちを引き起こす。MoElessは、次の層で生じるエキスパート負荷を事前予測し、混雑するエキスパートだけを一時的に複製して複数GPUへ分散することで、この待ち時間を減らすシステムである。

- **2026-02 · [DualScale: Energy-Efficient Disaggregated LLM Serving via Phase-Aware Placement and DVFS](2026-2602.18755-biscale-phase-aware-placement-dvfs.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  プリフィルとデコードを別GPU群へ分離するLLM推論では、両段階の負荷特性が異なるため、単純な自動スケーリングや一律のGPU周波数制御ではサービス品質目標を守りつつ電力を下げにくい。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Topology-Aware Data Movement for Disaggregated GPU Inference](2026-2607.28633-topology-aware-data-movement.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィルとデコードを別GPU群へ分離するLLMサービングでは、プリフィルで生成したKVキャッシュをデコード側へ渡す転送が新たなボトルネックになる。TopKVは、GPU間の物理接続を検出し、NVLink、PCIe、RDMA、TCPから転送経路を選び、層ごとのKV転送を計算と重ねる。

- **2026-09 · [OUTLETS: Output-Length Prediction from Speculative Decoding Backbones](2026-2609.01068-outlets-output-length-prediction-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  OUTLETSは、投機的 デコード用のドラフト モデルを「先のトークンを当てる装置」だけでなく「この生成があと何トークン続きそうかを読む装置」としても使い、予測した残長でデコードのキュー順序とワーカー割当を改善する。

- **2026-09 · [Latency-Aware Orchestration for Multi-Agent LLM Workflows on Heterogeneous GPUs](2026-2609.03335-latency-aware-multi-agent-orchestration-heterogeneous-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数のLLMエージェントが依存関係を持って連携する処理では、次のモデル呼び出しが準備できてから配置を決めると、モデル読込み、GPUメモリ確保、異種GPUごとの実行時間差が待ち時間として表面化する。

- **2026-09 · [Energy-Efficient LLM Serving via Disaggregated Attention--FFN and Flexible Frequency Scaling](2026-2608.01891-aflex-attention-ffn-disaggregation-frequency-scaling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、LLMサービングのプリフィルとデコードを分けて周波数制御するだけでは、同じ段階の中でも注意機構と全結合ネットワーク（Feed-順伝播 Network; FFN）の周波数感度が大きく異なるため、不要なGPU電力を使う問題を扱う。

- **2026-09 · [Deadline-Aware Adaptive Prefill Chunking for Efficient Large Language Model Serving](2026-2609.07883-deadline-aware-adaptive-prefill-chunking.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  連続バッチ型LLMサービングでは、長い入力を一括プリフィルすると同じ反復にいるデコード要求の次トークンが遅れ、逆にプリフィルを小さく固定分割すると反復回数とカーネル起動費用が増えて初回応答が遅くなる。

- **2026-09 · [Analytical Resource Management for Fine-grained MoE Computation-Communication Overlap](2026-2609.07536-moe-overlap-resource-manager.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分散MoEでは、専門家の計算が終わった部分からGPU間通信を始めれば待ち時間を隠せるが、計算担当と通信担当は同じGPUの実行資源を取り合う。本研究は、入力長や専門家へのトークン偏りに応じて「通信へGPU資源をどれだけ予約するか」を起動直前に解析式で決め、固定配分のCOMETよりモデル全体のプリフィルを平均1.185倍高速化する。

- **2026-09 · [Adaptive Context Parallelism for Production LLM Serving](2026-2609.04774-vertumnus-adaptive-context-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Vertumnusは「長いリクエストには多くのGPU」という単純な閾値ルールではなく、プレフィックス キャッシュで実際に残った計算量、ワーカーの混雑、追加GPU時間をリクエストごとに比較しつつ、クラスタ全体のCP ワーカー構成そのものも数秒単位でsplit / 統合する。

- **2026-08 · [When Does Disaggregation Pay? Simulating Prefill--Decode--Attention--FFN Specialization for Agentic LLM Inference](2026-2608.03741-heteropanacea.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLM推論を一台・一種類のGPUでまとめて処理する代わりに、入力処理と逐次生成、さらに注意機構とFFNを最大4種類の計算機群へ分けたとき、通信コストを払ってでも速くなる条件をシミュレーションで調べた研究。各段に計算重視・メモリ帯域重視の異なるハードウェアを割り当てられる場合ほど4段分離が効き、同じGPUしか選べない環境では細かく分ける意味が小さくなる。

- **2026-08 · [Pallas: A Proactive KV Cache Migration Framework for LLM Inference in AI-RAN](2026-2608.16477-pallas-proactive-kv-cache-migration-ai-ran.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Pallasは、ハンドオーバー後にKV キャッシュを救出するのではなく、ハンドオーバー前の予測時間を使って「古い大部分は対象で再計算、これから増える部分だけ送信元からストリーム」し、切替時点にほぼ最新の推論状態を揃える。

- **2026-08 · [P-PAS: Prefill-Pressure Adaptive Scheduling for Long-Context LLM Serving](2026-2608.15171-p-pas-prefill-pressure-adaptive-scheduling.md)**  
  実装：[✓](https://github.com/TimoSaemann/ppas-vllm) ・ リポジトリ内被引用：0  
  P-PASは、chunked プリフィルのchunkを常に小さくも大きくもせず、「今デコードと競合しているか」に応じて1 iterationのトークン budgetを切り替える軽量なvLLM スケジューラ拡張である。

- **2026-08 · [OpScale: Operator-level Provisioning and Autoscaling for LLM Serving](2026-2608.13499-opscale-operator-level-autoscaling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル全体ではなく演算子単位で供給・配置・実行時伸縮を行い、負荷に応じて現在の律速演算子だけへGPU資源を追加するLLM配信基盤。

- **2026-08 · [From LLM Inference to Agentic Workloads: Characterization and Implications for Serving Systems](2026-2608.15127-agentsysbench.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AgentSysBenchは、エージェント型 アプリケーションをLLM 呼び出しだけでなく、ツール、サンドボックス、検索取得、永続 状態、通信を含む長時間実行として計測し、従来のLLM サービングの前提がどこで崩れるかを明らかにする。主眼は推論カーネル単体ではなく、エージェント 実行全体を対象にしたサービング designである。

- **2026-08 · [Cascade: Exploiting SLO-Aware latency budget for fair and high goodput LLM inference serving](2026-2608.06557-cascade-slo-aware-latency-budget-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  リクエストごとに「SLOまであと何秒の遅延を許容できるか」を残り遅延 budgetとして継続推定し、その同じbudgetでリクエストの実行順とHBM / CPU DRAM / NVMe間のKV キャッシュ復元・先読み・保持・再計算をまとめて決めることで、SLOを満たす処理量と長文脈 リクエストへの公平性を両立するサービング システム。

- **2026-07 · [Towards Load-Aware Prefill Deflection for Disaggregated LLM Serving](2026-2607.02043-kairos-load-aware-prefill-deflection.md)**  
  実装：[✓](https://github.com/sudokara/Kairos) ・ リポジトリ内被引用：0  
  Kairosは、プリフィル専用GPUが混んでいるときにリクエストをそこで待たせるのではなく、デコード GPUに残っている計算余力を借りてプリフィルまで実行する。

- **2026-07 · [Sangam: Efficiently Serving Diffusion LLMs with the AR Stack](2026-2607.04206-sangam-diffusion-llm-serving.md)**  
  実装：[✓](https://github.com/UT-InfraAI/sangam) ・ リポジトリ内被引用：0  
  Sangamは、双方向注意を使う拡散言語モデルでは通常の自己回帰LLMのようにKVキャッシュを固定できず、近似キャッシュを用いても重い再プリフィルとデコードが周期的に繰り返され、しかも再プリフィルをchunk化できないというサービング問題を扱う。

- **2026-07 · [Robust KV Cache Management for LLM Serving under Output Token Length Uncertainty](2026-2607.16892-robust-kv-cache-management-output-length-uncertainty.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  「何トークン生成されるか分からないリクエストへ、最初にKV キャッシュを何トークン分確保するか」を固定P90/P95の経験則ではなく、プリエンプションの損失と未使用HBMの損失から決め、その予約量をGPU構成・ルーティング・プレフィックス キャッシュと一緒に再最適化する制御-プレーン手法。

- **2026-07 · [Online Linear Programming for Multi-Objective Routing in LLM Serving](2026-2607.03948-online-linear-programming-multi-objective-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  「一番空いているワーカーへ送る」の代わりに、各ワーカーの将来のバッチ枠とKV キャッシュへ影価格（影 価格）を付け、リクエストを今入れる価値がその資源 コストを上回るかでルーティングする。目的関数の重みを変えるだけで、平均遅延・TTFT・末尾・スループットの優先順位を同じルーター内で切り替えられる。

- **2026-07 · [ELDR: Expert-Locality-Aware Decode Routing for PD-Disaggregated MoE Serving](2026-2607.00466-eldr-expert-locality-decode-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル・デコード分離（プリフィル-デコード disaggregation; PD分離）でMoEを提供すると、同じ要求数を持つデコードGPUでも、一つのバッチが呼び出す異なるエキスパート数によって重み読み込み量が変わり、遅延が揃わない。

- **2026-07 · [Akashic: A Low-Overhead LLM Inference Service with MemAttention](2026-2607.05708-akashic-memattention-memory-service.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Akashicは、長時間動作するLLMエージェントの履歴を毎回すべて再入力する代わりに、履歴を有界なメモリチャンクへ逐次圧縮し、意味的に関連する過去チャンクを必要時だけ再利用する推論サービスである。

- **2026-06 · [PersistentKV: Page-Aware Decode Scheduling for Long-Context LLM Serving on Commodity GPUs](2026-2606.26666-persistentkv.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い文脈の逐次生成では1回に1トークンしか計算しないため、少数要求だとGPUへ十分な仕事を出せない。PersistentKVは既存のページ化KVキャッシュを作り直さず、長い系列を複数区間へ分けて同時処理し、長さの違う要求が混ざる場合は実際に必要な区間だけを小さな作業キューへ詰める。

- **2026-06 · [Observation, Not Prediction: Conversation-Level Disaggregated Scheduling for Agentic Serving](2026-2606.01839-conserve-conversation-level-agentic-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ConServeは、エージェント（エージェント）の各ターンを別々に配置判断するのではなく、会話（会話）全体を1つの配置単位として扱う。最初の重いプロンプト処理だけを専用プリフィル（プリフィル）GPUで実行し、生成したKVキャッシュをデコード（デコード）GPUへ1回だけ移す。

- **2026-06 · [FlexNPU: Transparent NPU Virtualization for Dynamic LLM Prefill-Decode Co-location](2026-2606.04415-flexnpu-transparent-virtualization-dynamic-pd-colocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FlexNPUは、NPUをアプリケーションへ物理デバイスのまま見せる従来方式では、プリフィルとデコードの負荷変化に応じて実行順や資源配分を後から調整できない問題を扱う。AscendCL APIをユーザー空間で透過的に捕捉し、仮想ハンドルへ置き換えて各物理NPUのデーモンへ転送することで、モデル、AIフレームワーク、NPUドライバを変更せず実行制御点を作る。

- **2026-05 · [Towards Multi-Model LLM Schedulers: Empirical Insights into Offloading and Preemption](2026-2605.19593-multi-model-offloading-preemption-schedulers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数の大規模言語モデルを限られたGPUで切り替えて提供する際、各モデルをどれだけCPUへオフロードすべきか、実行中の要求を中断して別モデルへ切り替えるべきかを判断するための実測研究である。3種類の量子化モデルについてGPU配置層の割合を連続的に振り、別の3モデルについてプリエンプション時のKVキャッシュ退避、モデル解放、モデル再読込、KV復元を分解測定した。

- **2026-05 · [Towards Distributed Inference of LLMs on a P2P Network](2026-2606.17059-p2p-prefix-cache-aware-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この論文は、分散LLMサービングで接頭辞KVキャッシュが各ノードへ分散し、要求がキャッシュを持たないノードへ到着すると同じプリフィル計算を繰り返す問題に対し、中央ルータやKVテンソル転送を使わず要求側を移動させる分散ルーティングを提案する。各ノードは自分の接頭辞を正確な基数木で管理し、他ノードの基数木は定期的な全体スナップショット交換で近似的に保持する。

- **2026-05 · [Taming Request Imbalance: SLO-Aware Scheduling for Disaggregated LLM Inference](2026-2605.02329-taming-request-imbalance-slo-aware-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この論文の狙いは、長いリクエストを単純に後回しにすることではない。各リクエストがサービス水準目標（サービス レベル 目的: SLO）を破るまでにどれだけ時間の余裕を持っているかをスケジューラが使い、余裕のないリクエストを先に進めつつ、余裕のあるリクエストは短時間だけ待たせる。これによりプリフィル側の先頭待ちとデコード側の長文リクエストによる同期待ちを減らす。

- **2026-05 · [STAR: Decode-Phase Rescheduling for LLM Inference](2026-2510.13668-star-decode-phase-rescheduling-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル・デコード分離サービングでは、プリフィル終了時に要求をデコードGPUへ一度割り当てても、その後の生成長が大きく異なるため時間経過とともにデコード負荷が崩れる。STARは対象LLM最終層の最後のトークンの隠れ状態を4層MLPへ入力し、残り生成長を低追加費で継続予測する。

- **2026-05 · [Measurement-Driven Diagnosis and Mitigation of Host-CPU Co-location Interference in Single-GPU LLM Serving on a Multi-GPU Server](2026-2609.05425-cotail.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLM本体はGPUで計算していても、要求の受付・バッチ作成・GPUへの仕事投入はCPUが担当するため、同じサーバの空きCPUで別処理を動かすとLLMが大きく遅くなることがある。

- **2026-04 · [Blink: CPU-Free LLM Inference by Delegating the Serving Stack to GPU and SmartNIC](2026-2604.07609-blink-cpu-free-llm-inference-gpu-smartnic.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Blinkは、定常状態のLLM推論でCPUが毎トークン行っていたバッチ更新・スケジューリング・KVキャッシュ管理・GPU起動をGPU常駐制御へ移し、ネットワーク要求処理をSmartNICへ移す。SmartNICとGPUはGPUメモリ上の共有リングバッファを介して直接通信し、ホストCPUを推論のクリティカルパスから外す。

- **2026-03 · [PrefixWall: Mitigating Prefix Caching Side Channels in Shared LLM Systems](2026-2603.10726-cachesolidarity-prefix-cache-side-channel-defense.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PrefixWallは、複数利用者が同じLLM推論基盤を共有するとき、自動接頭辞キャッシュ（Automatic Prefix キャッシュ; APC）のヒット有無による初回トークン遅延の差から他人の入力を推測できる問題に対し、利用者全体を分離するのではなく、異なる利用者から再利用された接頭辞だけを危険境界として記録し…

- **2026-03 · [Multi-stage Flow Scheduling for LLM Serving](2026-2603.17456-multi-stage-flow-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分離型LLMサービングでは、初回トークンを返すまでに、再利用KVキャッシュの遠隔取得、テンソル・エキスパート・系列並列などの集団通信、プリフィルからデコードへのKV転送という複数段階の通信が発生する。

- **2026-03 · [Cost-Efficient Multimodal LLM Inference via Cross-Tier GPU Heterogeneity](2026-2603.12707-cost-efficient-multimodal-llm-inference-via-cross-tier-gpu-heterogeneity.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  画像符号化をRTX 4090、言語生成をA100へ分離し、KVキャッシュではなく数MB級の画像埋め込みだけをPCIe転送することで、異種GPUを使った低コストなマルチモーダルLLMサービングを実現する。

- **2026-03 · [CALVO: Improve Serving Efficiency for LLM Inferences with Intense Network Demands](2026-2603.21257-calvo-network-aware-kv-loading-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  遠隔KV読み込みを独立した非同期段階へ分離し、通信時間と計算時間を合わせた要求費用で順序付けすることで、長文脈の高キャッシュ再利用環境で平均最初のトークン時間を81.3%以上短縮し、期限達成率を最大61.67%改善する。

- **2026-02 · [Multi-Layer Scheduling for MoE-Based LLM Reasoning](2026-2602.21626-multi-layer-scheduling-moe-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  混合専門家モデル（Mixture of エキスパート; MoE）の推論サービングでは、要求をどのデータ並列エンジンへ送るか、各エンジン内でどの要求を先に処理するか、各専門家をどのGPUへ置くかが互いに影響する。

- **2026-02 · [Large-Scale LLM Inference with Heterogeneous Workloads: Prefill-Decode Contention and Asymptotically Optimal Control](2026-2602.02987-prefill-decode-contention-optimal-control.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模LLM推論では、入力処理であるプリフィルをGPUへ入れるほど新規要求をデコード段階へ送り込める一方、同じGPU上の逐次生成を遅くするという競合が生じる。

- **2025-10 · [From Principles to Practice: A Systematic Study of LLM Serving on Multi-core NPUs](2025-2510.05632-systematic-study-multicore-npu-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  マルチコアNPUでは、GPU向けに考えたLLMサービング方式をそのまま移すと、コア間通信、コアごとに分かれたSRAM、HBM帯域の不足によって計算資源が遊ぶ。

### 1年以上前

- **2023-09 · [Efficient Memory Management for Large Language Model Serving with PagedAttention](2023-2309.06180-vllm-pagedattention-efficient-memory-management.md)**  
  実装：[✓](https://github.com/vllm-project/vllm) ・ リポジトリ内被引用：193  
  vLLMは、要求ごとに大きな連続領域を予約していたKVキャッシュを固定長ブロックへ分解し、論理的な並びとGPU上の物理配置を分離する。必要なブロックだけ動的に割り当て、同じ接頭辞のKVを共有することで、限られたGPUメモリへより多くの要求を同時に載せる。

- **2022-07 · [Orca: A Distributed Serving System for Transformer-Based Generative Models](2022-osdi22-orca-iteration-level-scheduling-selective-batching.md)**  
  実装：✓ ・ リポジトリ内被引用：101  
  出力トークンを1個生成するたびにスケジューラへ制御を戻し、終わった要求を外して新着要求を追加する。さらに、長さの違う要求を同じバッチで処理できるよう、注意機構だけを要求ごとに分け、それ以外の演算はトークン単位でまとめて実行する分散LLMサービングシステム。

- **2024-01 · [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](2024-2401.09670-distserve-disaggregating-prefill-decoding-goodput.md)**  
  実装：[✓](https://github.com/LLMServe/DistServe) ・ リポジトリ内被引用：94  
  プリフィルとデコードを別GPU群へ分け、それぞれのGPU数・モデル分割方法・配置場所を、最初のトークンまでの時間とその後のトークン間隔の目標に合わせて別々に決めることで、両処理段階の干渉をなくす推論提供システム。

- **2023-11 · [Splitwise: Efficient Generative LLM Inference Using Phase Splitting](2023-2311.18677-splitwise-efficient-generative-llm-inference-phase-splitting.md)**  
  実装：[✓](https://github.com/Mutinifni/splitwise-sim) ・ リポジトリ内被引用：93  
  プリフィルとデコードを別の計算機群へ分け、それぞれに向くGPU世代・電力設定・台数を使い分けて、クラスタ全体のスループット・コスト・消費電力を改善するサービング設計。

- **2023-12 · [SGLang: Efficient Execution of Structured Language Model Programs](2023-2312.07104-sglang-efficient-execution-structured-language-model-programs.md)**  
  実装：[✓](https://github.com/sgl-project/sglang) ・ リポジトリ内被引用：86  
  複数のLLM呼び出しや条件分岐をランタイムが1つのプログラムとして理解し、共有接頭辞のKV再利用・並列実行・構造化出力生成をまとめて効率化する推論システム。

- **2024-03 · [Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve](2024-2403.02310-sarathi-serve-chunked-prefills-stall-free-scheduling.md)**  
  実装：[✓](https://github.com/microsoft/sarathi-serve) ・ リポジトリ内被引用：79  
  長いプリフィルを小さい分割片へ分け、毎回まず進行中要求のデコードトークンを処理し、残った総トークン枠へプリフィルを入れることで、新要求を受けながらデコードの長時間停止を防ぐ推論提供スケジューラ。

- **2024-07 · [Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot](2024-2407.00079-mooncake-kvcache-centric-disaggregated-architecture.md)**  
  実装：[✓](https://github.com/kvcache-ai/Mooncake) ・ リポジトリ内被引用：50  
  プリフィルとデコードを別GPU群へ分け、クラスタ内のCPU DRAM・SSDへ過去KVを保存して別ノードからも再利用できるようにし、KV取得時間・待ち行列待ち・残りプリフィル計算を比較してリクエストの実行先を決める大規模な推論提供システム。

- **2024-03 · [Cost-Efficient Large Language Model Serving for Multi-turn Conversations with CachedAttention](2024-2403.19708-cachedattention-multi-turn-conversation-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：41  
  複数ターン会話の過去KVを要求終了後もDRAM / SSDへ保存し、次ターンで使う層のKVを少し前からGPUへ戻すことで、履歴全体の再プリフィルと記憶装置待ちを減らす状態保持型推論提供手法。

- **2023-02 · [AlpaServe: Statistical Multiplexing with Model Parallelism for Deep Learning Serving](2023-2302.11665-alpaserve.md)**  
  実装：[✓](https://github.com/alpa-projects/mms) ・ リポジトリ内被引用：31  
  複数モデルへ届くリクエスト数が時間ごとに偏る環境で、モデルを複数GPUへ分割して置き、空いているGPUをモデル間で共有しやすくすることで、特定モデルだけ待ち行列が伸びるのを抑えるサービング配置手法。

- **2023-05 · [FastServe: Iteration-Level Preemptive Scheduling for Large Language Model Inference](2023-2305.05920-fastserve-iteration-level-preemptive-scheduling.md)**  
  実装：[✓](https://github.com/LLMServe/FastServe) ・ リポジトリ内被引用：30  
  出力トークンを1つ生成する区切りで要求（リクエスト）を一時停止・再開できるようにし、短い要求を優先しながらKVキャッシュ（KV キャッシュ）をCPUへ退避・先読みして待ち時間を減らすLLMサービングスケジューラ（serving スケジューラ）。

- **2024-06 · [Llumnix: Dynamic Scheduling for Large Language Model Serving](2024-2406.03243-llumnix-dynamic-scheduling-live-migration.md)**  
  実装：[✓](https://github.com/AlibabaPAI/llumnix) ・ リポジトリ内被引用：25  
  実行中要求のKVキャッシュを別モデル実行単位へ段階的に移し、GPU間の混雑差・メモリ不足・優先度変更・実行単位削減が起きた後でも要求配置を修正できる複数実行単位の推論提供スケジューラ。

- **2024-05 · [Preble: Efficient Distributed Prompt Scheduling for LLM Serving](2024-2407.00023-preble-efficient-distributed-prompt-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  同じプレフィックスのKVをすでに持つGPUへリクエストを送ればプリフィルを省ける一方、そのGPUだけ混むことがあるため、KV再利用で節約できる計算時間とGPUの混雑による待ち時間を比較してリクエストの送り先を決めるdistributed サービング スケジューラ。

- **2024-01 · [DeepSpeed-FastGen: High-throughput Text Generation for LLMs via MII and DeepSpeed-Inference](2024-2401.08671-deepspeed-fastgen-dynamic-splitfuse.md)**  
  実装：[✓](https://github.com/deepspeedai/DeepSpeed-MII) ・ リポジトリ内被引用：17  
  長いプロンプトを小さく分割し、短いプロンプト・プリフィル 分割片・デコード トークンを毎回ほぼ同じ総トークン数になるよう混ぜることで、長いプリフィルがデコードを止める時間を抑えつつGPUを効率よく使うLLM 提供処理 システム。

- **2024-06 · [MemServe: Context Caching for Disaggregated LLM Serving with Elastic Memory Pool](2024-2406.17565-memserve-context-caching-disaggregated-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  プリフィルとデコードを別実行単位へ分ける推論提供で、GPU / CPU上のKVキャッシュを実行単位横断で検索・共有・転送できる共通メモリプールを作り、過去接頭部の再利用と処理段階間KV移動を同じ仕組みで扱うシステム。

- **2023-12 · [Stateful Large Language Model Serving with Pensieve](2023-2312.05516-pensieve-stateful-large-language-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  複数往復会話の過去KVキャッシュをリクエスト終了後もGPU / CPUへ残し、次の往復で同じ履歴を再びプリフィルする計算を避ける状態保持型LLM提供処理システム。

- **2024-01 · [ServerlessLLM: Low-Latency Serverless Inference for Large Language Models](2024-2401.14351-serverlessllm-low-latency-serverless-inference.md)**  
  実装：[✓](https://github.com/ServerlessLLM/ServerlessLLM) ・ リポジトリ内被引用：14  
  要求到着時にモデルをGPUへ読み込むサーバーレス環境で、チェックポイントをGPU近くのSSD / DRAMへキャッシュし、高速読み込み器とモデル所在地を考慮した要求配置、生成途中要求の移動を組み合わせてモデル起動待ちを短縮するシステム。

- **2023-12 · [Fairness in Serving Large Language Models](2024-2401.00588-fairness-in-serving-large-language-models-vtc.md)**  
  実装：[✓](https://github.com/Ying1123/VTC-artifact) ・ リポジトリ内被引用：14  
  仮想 トークン Counter（VTC）は、要求数ではなくクライアントごとに実際に処理した入力・出力トークンをサービス量として数え、累積サービス量が少ないクライアントから新しい要求を実行バッチへ入れる。空きGPUを意図的に遊ばせず、公平性と高い利用率を両立することを狙う。

- **2024-08 · [Efficient LLM Scheduling by Learning to Rank](2024-2408.15792-efficient-llm-scheduling-learning-to-rank.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  最終的な出力トークン数を正確に当てる代わりに、プロンプトからどのリクエストが他より短く終わりそうかという順位だけを小型モデルで予測し、短そうなリクエストを先に処理して長いリクエストによるキュー待ちを減らすスケジューラ。

- **2024-05 · [Parrot: Efficient Serving of LLM-based Applications with Semantic Variable](2024-2405.19888-parrot-efficient-serving-llm-applications-semantic-variable.md)**  
  実装：[✓](https://github.com/microsoft/ParrotServe) ・ リポジトリ内被引用：12  
  複数LLM呼び出しから成るアプリケーションについて、どの呼び出しの出力を次の呼び出しが使うか、どのプロンプト部分を共有するかをバックエンドへ伝え、アプリケーション全体を見て並列実行・バッチ処理・接頭部 KV再利用を調整する推論提供システム。

- **2023-11 · [SpotServe: Serving Generative Large Language Models on Preemptible Instances](2023-2311.15566-spotserve-preemptible-instance-serving.md)**  
  実装：[✓](https://github.com/Hsword/SpotServe) ・ リポジトリ内被引用：12  
  安価だが突然利用できなくなるスポットGPU（spot GPU）の増減に合わせてモデルの分割方法を組み替え、既存の重み（重み）とKVキャッシュ（KV キャッシュ）をできるだけ再利用してLLMサービングを継続するシステム。

- **2024-02 · [INFERCEPT: Efficient Intercept Support for Augmented Large Language Model Inference](2024-2402.01869-infercept-intercept-aware-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  外部ツールや人間応答を待つ間に生成が中断される拡張LLMで、KVキャッシュをGPUに保持する、CPUへ退避する、破棄して再計算するという三つの選択肢を、GPUメモリの時間積で表した浪費量を基準に要求ごとに切り替える推論基盤。

- **2024-06 · [Queue Management for SLO-Oriented Large Language Model Serving](2024-2407.00047-qlm-queue-management-slo-oriented-llm-serving.md)**  
  実装：[✓](https://github.com/QLM-project/QLM) ・ リポジトリ内被引用：7  
  対話的 / バッチ要求や複数モデルを同じクラスタで扱うとき、各要求グループがあと何秒待てるかとモデルがどのGPUに載っているかを見て、待ち行列順序と実行先を組み替え、遅延目標を守れる要求数を増やすシステム。

- **2024-04 · [Andes: Defining and Enhancing Quality-of-Experience in LLM-Based Text Streaming Services](2024-2404.16283-andes-qoe-text-streaming-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  LLMのストリーミング応答を単純な生成速度ではなく、最初のトークンが早く届き、その後もユーザーが読む速度に間に合うようトークンが途切れず届くかで評価し、十分先まで生成済みの要求を一時停止して、今すぐGPU時間が必要な要求へ回す推論提供システム。

- **2025-07 · [Oneiros: KV Cache Optimization through Parameter Remapping for Multi-tenant LLM Serving](2025-2507.11507-oneiros-parameter-remapping-multitenant-serving.md)**  
  実装：[✓](https://github.com/UT-SysML/Oneiros/) ・ リポジトリ内被引用：3  
  Oneirosは、複数LLMを同じGPUで提供する環境でKVキャッシュ不足が起きたとき、頻繁に更新されるKVをCPUへ退避すると双方向転送と同期がデコードを止める問題を扱う。そこで実行中に不変なモデルパラメータの一部をCPUへ移し、空いたGPU物理ページをKVキャッシュへ転用するパラメータ再配置を導入する。

- **2025-04 · [Optimizing LLM Inference: Fluid-Guided Online Scheduling with Memory Constraints](2025-2504.11320-fluid-guided-online-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  この論文の中心は「GPU メモリが足りなくなってからリクエストを追い出す」のではなく、数十〜数百トークン先までデコードするとKV キャッシュがどのように増えるかを見越して、GPU内に残すリクエストの構成そのものを調整することである。

- **2025-01 · [Mell: Memory-Efficient Large Language Model Serving via Multi-GPU KV Cache Management](2025-2501.06709-mell-multi-gpu-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  複数GPUでLLMを提供すると、要求ごとの出力長が予測しにくくKVキャッシュが時間とともに成長するため、あるGPUだけが満杯になり別GPUには空きが残る。Mellは実行中要求をGPU間で移し、通信余力があるときはKV本体を転送し、演算余力があるときはトークンだけを転送して移行先で再プリフィルする適応型移行を行う。

- **2025-01 · [Locality-aware Fair Scheduling in LLM Serving](2025-2501.14312-locality-aware-fair-scheduling-dlpm.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  クライアントごとのGPU利用量を公平に保ちつつ、公平性が大きく崩れない範囲だけ実行順を入れ替えて、同じプレフィックスを持つリクエストを続けて処理しKV再利用を増やすスケジューラ。

- **2025-01 · [Hierarchical Autoscaling for Large Language Model Serving with Chiron](2025-2501.08090-chiron-hierarchical-autoscaling.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  対話型 リクエストの遅延目標を守りながら余ったGPU 容量をバッチ リクエストへ使うため、各GPUで同時処理するリクエスト数を素早く増減する制御と、クラスタ全体のGPU インスタンス数を遅い周期で増減する制御を分けたLLM 自動スケーラ。

- **2024-08 · [P/D-Serve: Serving Disaggregated Large Language Model at Scale](2024-2408.08147-pd-serve-disaggregated-llm-at-scale.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  P/D-Serveは、事前充填（プリフィル）と復号（デコード）を別インスタンスに分ける設計を、数万NPUの商用クラスタで運用したときに生じる制御面・ネットワーク面の問題まで含めて解くシステムである。中心は3点ある。

- **2025-09 · [Parallax: Efficient LLM Inference Service over Decentralized Environment](2025-2509.26182-parallax-decentralized-heterogeneous-serving.md)**  
  実装：[✓](https://github.com/GradientHQ/parallax) ・ リポジトリ内被引用：0  
  Parallaxは、地理的に離れた異種GPUを公衆ネットワーク越しに束ねる分散LLMサービングで、計算性能・VRAM容量・通信帯域の差が大きいため均等なモデル分割では最遅GPUや低速回線が全体を律速する問題を、二段階スケジューリングで解く。
<!-- survey:auto:end -->
