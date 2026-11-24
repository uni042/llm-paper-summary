---
canonical_id: DOI:10.1145/3832810.3832886
doi: 10.1145/3832810.3832886
title: 'IHS-LM: Intra-batch Hybrid Scheduling and Layer Migration for VLM Pipeline Inference Acceleration on Edge Devices'
summary: IHS-LMは、異種エッジ端末上でVLMをパイプライン並列推論するときに生じる二種類の不均衡を同時に扱う。バッチ内ではKVキャッシュ空き容量と待機・デコードトークン量からプリフィル/デコード比を動的に調整し、段間では帯域変動を滑動窓で検知して事前複製した境界層の実行担当を切り替える。5台のNVIDIA Jetson実機でQwen2.5-VL-32BとYi-VL-34Bを評価し、Sarathi-Serve+DynaPipeの組合せに対して平均推論遅延を最大17.5%削減しつつ精度を維持した。
list_summary: KV容量連動のプリフィル/デコード混在スケジューリングと帯域感知型の境界層移行を統合し、異種Jetson上のVLM推論遅延を最大17.5%削減する。
authors:
- Yun Li
- Tianfu Pang
- Zhiyu Cai
- Zhenxiang Pan
- Yingchi Mao
- Jie Wu
authors_affiliations: Hohai University; China Telecom Cloud Computing Research Institute; Temple University
published: '2026-09-28'
publication: 55th International Conference on Parallel Processing (ICPP 2026)
publication_type: 国際会議論文
publication_status: Published / ICPP 2026
lineage: edge VLM inference / pipeline parallelism / hybrid batching / dynamic layer migration
topics:
- VLM推論
- エッジ推論
- パイプライン並列
- 混在バッチ
- 動的層移行
importance: メモリ制約のある異種エッジで、要求レベルのバッチ構成とネットワーク変動に起因する段間不均衡を別々に最適化せず、閉ループで共同適応させる実システム研究。
hardware_evaluation: AGX Orin 64GB×1、Orin NX 16GB×2、Orin Nano 8GB×2。1台のOrin NXをcoordinator、残り4台を推論パイプラインとして使用。
quality_effect: モデル重みや構造を変更せず、Qwen2.5-VL-32BとYi-VL-34Bで精度をほぼ維持。追加メモリは境界候補層の冗長常駐により増える。
references_checked_at: '2026-09-23'
references_source: primary manuscript
references_total: 36
source: https://doi.org/10.1145/3832810.3832886
sources:
- https://cis.temple.edu/~wu/research/publications/Publication_files/ICPP%202026-IHS-LM%20Intra-batch%20Hybrid%20Scheduling%20and%20Layer%20Migration%20for%20VLM%20Pipeline%20Inference%20Acceleration%20on%20Edge%20Devices.pdf
- https://doi.org/10.1145/3832810.3832886
implementation: PyTorchとNVIDIA JetPack 6.2上の実装。中央coordinatorと4台の推論workerを用い、Linux TCで動的帯域変動を再現して評価。
last_checked: '2026-09-23'
code: null
references: []
last_audited: null
audit_version: 0
---

# IHS-LM: Intra-batch Hybrid Scheduling and Layer Migration for VLM Pipeline Inference Acceleration on Edge Devices

> KV容量連動のプリフィル/デコード混在スケジューリングと帯域感知型の境界層移行を統合し、異種Jetson上のVLM推論遅延を最大17.5%削減する。
## 書誌情報
- **著者**: Yun Li, Tianfu Pang, Zhiyu Cai, Zhenxiang Pan, Yingchi Mao, Jie Wu
- **著者・所属**: Hohai University; China Telecom Cloud Computing Research Institute; Temple University
- **公開**: 55th International Conference on Parallel Processing (ICPP 2026)
- **種別**: 国際会議論文
- **対象**: VLM推論、エッジ推論、パイプライン並列、混在バッチ、動的層移行
- **実装**: PyTorchとNVIDIA JetPack 6.2上の実装。中央coordinatorと4台の推論workerを用い、Linux TCで動的帯域変動を再現して評価。
## 概要
IHS-LMは、異種エッジ端末上でVLMをパイプライン並列推論するときに生じる二種類の不均衡を同時に扱う。バッチ内ではKVキャッシュ空き容量と待機・デコードトークン量からプリフィル/デコード比を動的に調整し、段間では帯域変動を滑動窓で検知して事前複製した境界層の実行担当を切り替える。5台のNVIDIA Jetson実機でQwen2.5-VL-32BとYi-VL-34Bを評価し、Sarathi-Serve+DynaPipeの組合せに対して平均推論遅延を最大17.5%削減しつつ精度を維持した。

IHS-LMの新規性は、異なる時間尺度の二つの不均衡を一つの閉ループへ統合した点にある。バッチごとにはIntra-バッチ Hybrid スケジューラ（IHS）が待機プリフィル量、実行中デコード量、全worker中で最小のKVキャッシュ空き率からトークンquotaを決め、デコードを優先しながらプリフィルをパイプライン深度に合わせて分散する。より粗い時間尺度では帯域-Aware Model 層 Migration（BAMLM）が各stageの計算＋通信遅延を滑動窓で平滑化し、平均stage遅延に比例する閾値を超えた持続的不均衡だけを検出する。移行対象の境界層はオフラインに隣接端末へ冗長配置しておき、オンラインでは重みを転送せずactivate/freezeの論理切替だけで計算境界を動かす。これによりKV容量に起因するバッチ内skewと帯域変動に起因するstage間skewを補完的に抑える。
## 問題設定
30B級VLMを単一のエッジ端末へ載せるのはGPUメモリ上困難で、クラウドへ送れば遅延とプライバシーの問題が生じるため、複数端末へモデル層を分割するパイプライン並列が有力になる。しかし推論には計算律速のプリフィルとメモリ帯域律速のデコードが混在し、従来の静的バッチやiteration-level batching、chunked プリフィルは、待機中トークン量と各端末のKVキャッシュ残量を同時に見てプリフィル/デコード比を調整しない。このためmicro-バッチごとの仕事量がずれてパイプライン bubbleが生じる。さらにエッジのリンク帯域は時間変動し、オフラインで均衡させた層分割も実行中に崩れる。DynaPipeは主に計算時間差を見てパイプライン末尾側の移行を扱い、LinguaLinkedはオフライン分割への依存が強いため、帯域変動に起因する段間不均衡を即応的に解消しにくい。重いVLM層を実行中に物理転送すれば、その転送自体が新たな遅延になる点も従来方式の制約である。
## 新規性
IHS-LMの新規性は、異なる時間尺度の二つの不均衡を一つの閉ループへ統合した点にある。バッチごとにはIntra-バッチ Hybrid スケジューラ（IHS）が待機プリフィル量、実行中デコード量、全worker中で最小のKVキャッシュ空き率からトークンquotaを決め、デコードを優先しながらプリフィルをパイプライン深度に合わせて分散する。より粗い時間尺度では帯域-Aware Model 層 Migration（BAMLM）が各stageの計算＋通信遅延を滑動窓で平滑化し、平均stage遅延に比例する閾値を超えた持続的不均衡だけを検出する。移行対象の境界層はオフラインに隣接端末へ冗長配置しておき、オンラインでは重みを転送せずactivate/freezeの論理切替だけで計算境界を動かす。これによりKV容量に起因するバッチ内skewと帯域変動に起因するstage間skewを補完的に抑える。
## 手法
### 手法のあらまし
システムは中央coordinatorとN台のworkerから成る。要求到着時、coordinatorのIHSは各workerのKVキャッシュ空き率の最小値をグローバル安全指標とし、待機プリフィルトークン数と目標処理step数から負荷側quota、KV空き率と安全水位から資源側quotaを作る。デコードは実行中queueから1 iterationの上限まで先に確保しパイプライン深度で均等化し、残りトークン budgetへプリフィルを詰める。KV空き率が安全水位を下回ると新規プリフィルを止め、継続デコード用の余裕を守る。生成したmixed micro-バッチを各workerが順次実行する一方、local monitorは計算・通信を含むstage 遅延を収集する。

BAMLMのSliding Window 帯域 Sensingはリンクjitterが大きいほど窓を広げて一時的な揺らぎを除去し、coordinatorは最大stage 遅延と最小stage 遅延の差が平均stage 遅延に比例する動的閾値を超え、かつcooldownを経過した場合だけ移行を起動する。境界ごとにGPU空きメモリから候補層数を決め、隣接2端末へ候補層を事前複製する。オンラインでは全境界の候補層割当を同時に探索し、offline profilingした層計算時間と直近通信遅延から予測stage 遅延 rangeを最小化する割当を選ぶ。実際の移行は重み転送ではなく候補層のactivate/freezeで行うため、動的帯域に追従しながら移行通信を抑える。

### KV容量連動のIntra-バッチ Hybrid スケジューラ
IHSはプリフィルとデコードを固定比率で混ぜず、待機プリフィルトークン数、実行中デコードトークン数、全workerのうち最も逼迫したKVキャッシュ空き率を毎iteration参照する。プリフィル quotaには負荷消化速度とKV安全水位の双方を反映し、デコード quotaをパイプライン深度に合わせて均等化した後、残ったトークン budgetへプリフィルを入れる。

KV空き率が安全水位0.1を下回ると新規プリフィルを一時停止してデコードの継続領域を確保する。デコード-firstで総トークン budgetを守りつつ、プリフィルとデコードをパイプライン深度に応じてmicro-バッチへ均等配分するため、長いプリフィルによるデコード 待ちと特定micro-バッチの過大化を同時に抑え、パイプライン bubbleを減らす。

### 帯域感知型BAMLMと滑動窓監視
各workerはstageの計算時間と次stageへの活性値通信時間を計測し、帯域jitterの強さに応じて5〜20 バッチの滑動窓長を適応させる。coordinatorは平滑化したstage 遅延の最大値と最小値の差を不均衡指標とし、全stage平均遅延の15%を基準とする動的閾値を超えた持続的skewだけを移行対象にする。

短い窓は通常時の変化追従性を保ち、jitterが閾値を超えると窓を拡張して一時的な揺らぎを平均化する。移行後は30 バッチのcooldownを置き、旧観測値が窓に残っている間の反復移行を防ぐ。これにより通信帯域の瞬間ノイズではなく、実際にslowest stageを作る持続的な帯域劣化だけを層 migrationへ接続する。

### 事前複製境界層によるFine-Grained Model 層 Migration
初期分割では各端末メモリの85%を基本モデル配置に使い、残りを弾性領域として隣接stage境界の候補層を双方へ冗長常駐させる。オンラインでは各境界でどちらの端末が何層担当するかを変数とし、offline profilingした層計算コストと現在の通信遅延から全stageの予測遅延幅を最小化する組合せを求める。

候補重みはすでに両端末に存在するため、移行時はstraggler側で対象層をfreezeし隣接側でactivateする論理ルーティングだけで計算境界を移せる。全境界を同時に最適化することで一箇所のオフロードが別stageへボトルネックを移すことも避ける。大容量重みのオンライン転送を消す代償として、候補層の冗長常駐分だけピークGPUメモリが増える。

### 全体のデータ／制御の流れ
要求ごとの高速制御はIHS、持続的な環境変化への低頻度制御はBAMLMが担当する二時間尺度設計である。IHSがmicro-バッチ内のプリフィル/デコード負荷を揃えても、リンク劣化でstage間バランスは崩れ得るためBAMLMが計算境界を調整する。

逆にBAMLMだけでは要求長やKV残量の変化によるバッチ内skewを解消できない。coordinatorが両方を統合し、workerのKV状態・stage 遅延・事前profiling結果を使って、トークン flowと層 配置を別粒度で連続的に適応させる。
## 評価条件
- **ハードウェア**: 5台のNVIDIA Jetson実機。AGX Orin 64GB×1、Orin NX 16GB×2、Orin Nano 8GB×2をswitch接続し、Orin NX 1台をcoordinator専用、残るAGX Orin 1台・Orin NX 1台・Orin Nano 2台を4-stage パイプラインとして用いる。Linux TCで100Mbpsから50〜85Mbpsへの帯域劣化を人工的に与える。
- **ソフトウェア**: NVIDIA JetPack 6.2 SDK、PyTorch、FP16重み。VLMはQwen2.5-VL-32BとYi-VL-34B。IHSのKstep=8、Bmax=2048、Bmin=32、KV安全水位0.1。BAMLMはwindow 5〜20、jitter閾値0.1、window係数2、imbalance係数gamma=0.15、cooldown 30 バッチ、基本メモリ割当率0.85、バッファ 512MB。
IHSはQwen2.5-VL-32B、100MbpsでPoisson到着率1〜5 req/sを与え、Sarathi-Serve等とTTFT、TPOT、平均推論遅延を比較する。BAMLMは帯域を85/70/50Mbpsへ変化させgamma感度を調べ、100Mbps開始後50 iterationで中間linkを約50Mbpsへ落とす動的条件でDynaPipe、LinguaLinkedと比較する。統合評価はSarathi-Serve+DynaPipeを比較対象とし、IHSなし、BAMLMなしのablationを含め、GYU-DETとVizWiz-VQAで平均遅延、精度、ピークGPUメモリを測定する。
データセットは11,123画像・6欠陥カテゴリのGYU-DETと31,173 image-question pairのVizWiz-VQA。モデルは30B超のQwen2.5-VL-32BとYi-VL-34B。実機エッジclusterと帯域変動を評価する一方、Jetson系列以外、より大規模なnode数、WANの複雑なloss/jitter、異なるVLM構造やhybrid parallelismへの一般化は直接検証していない。
## 主要結果
IHS-LMは高負荷時のバッチ内skewと帯域変動時のstage間skewを別モジュールで抑え、統合時にSarathi-Serve+DynaPipeの比較対象より平均推論遅延を最大17.5%削減した。Qwen2.5-VL-32BではGYU/VizWizで328/342 ms/トークン、Yi-VL-34Bでは352/361 ms/トークンとなり、いずれも比較対象と各単独ablationを上回る。IHS単体は到着率5 req/sでTTFTを24.3秒から18.9秒へ下げ、TPOTを約20%削減する。BAMLMは50Mbpsへ劣化した条件でQwen2.5-VL-32Bを341 ms/トークン、Yi-VL-34Bを367 ms/トークンまで改善するが、候補層の冗長常駐によりGPUメモリは増加する。

- 統合平均推論遅延 / 最大17.5%削減 (比較対象: Sarathi-Serve + DynaPipe; 条件: 高負荷・異種帯域、GYU-DET/VizWiz-VQA、Qwen2.5-VL-32B/Yi-VL-34B) — バッチ内とstage間の二種類の不均衡を同時に扱う効果を示す。

- Qwen2.5-VL-32B AIL / 328 ms/トークン (GYU), 342 ms/トークン (VizWiz) (比較対象: 376 / 392 ms/トークン; 条件: full IHS-LM) — IHSなし341/356、BAMLMなし358/371よりも統合構成が速い。

- Yi-VL-34B AIL / 352 ms/トークン (GYU), 361 ms/トークン (VizWiz) (比較対象: 427 / 434 ms/トークン; 条件: full IHS-LM) — 両データセットで最小遅延。

- 高負荷TTFT / 18.9 s (比較対象: Sarathi-Serve 24.3 s; 条件: Qwen2.5-VL-32B, 100Mbps, Poisson 5 req/s) — KV容量とトークン backlogを用いるIHSがプリフィルによるデコード阻害を抑える。

- BAMLM 50Mbps AIL / 341 ms/トークン (Qwen2.5-VL-32B), 367 ms/トークン (Yi-VL-34B) (比較対象: DynaPipe 376/427、LinguaLinked 365/396 ms/トークン (GYU); 条件: 100Mbpsから約50Mbpsへ中間linkを劣化) — 帯域感知と細粒度境界層切替が通信由来のstage imbalanceに有効。

### 負の結果・境界条件
- BAMLMは候補境界層を隣接端末へ冗長常駐させるため、Qwen2.5-VL-32Bでは比較対象約84.8〜84.6GBに対しIHS-LM約89.5〜89.3GB、Yi-VL-34Bでは87.1〜87.2GBに対し約89.9〜89.8GBへピークGPUメモリが増える。gamma=0.05では軽微な帯域変動にも反応して不要な移行が増え、gamma=0.20では50Mbps級の劣化でも移行が発火せずbubbleが蓄積するため、閾値選択に感度がある。

### 結果の読み方
性能向上は単なる層再配置だけではなく、IHSが短時間のリクエスト/トークン変動を、BAMLMがより長い時間尺度のlink変動を処理する役割分担から生じる。ablationでどちらか一方を外すと遅延が悪化するため、二つの制御ループは補完的である。一方、物理重み転送を避ける代わりに冗長メモリを予約するため、速度とGPU容量の明確なtrade-offがある。
## 品質への影響
モデル重み・architectureを変更しないため精度は概ね維持される。Qwen2.5-VL-32Bのfull IHS-LMはGYU/VizWizで75.2/76.1%、Yi-VL-34Bは77.5/78.3%。比較対象との差は小さく、主な代償は品質低下ではなく冗長層によるメモリ増加である。
## 既存研究との差
FasterTransformerはバッチ完了待ちの静的方式、Orcaはiteration単位でリクエストを出入りさせるが、プリフィル/デコードの資源差をKV残量まで含めて調整しない。Sarathi-Serveはchunked プリフィルでデコード 待ちを抑えるが、IHSはさらにpending トークン分布とパイプライン全体の最小KV空き率からプリフィル quotaを動的に変える。LinguaLinkedはheterogeneous edge向け分散配置を行うもののoffline partitionへの依存が強く、DynaPipeは計算時間差中心の動的層 assignmentで帯域非対称性を直接扱わない。BAMLMはstageの通信を含む実測遅延から帯域由来のskewを検知し、隣接境界層を事前複製して論理切替するため、オンライン重み転送を避けながら全stage境界を同時調整する点が異なる。
## 限界
評価は5台のNVIDIA Jetson系列、4-stage推論パイプライン、2種類の30B級VLMと2データセットに限定される。Linux TCで再現した帯域劣化は実ネットワークのpacket loss、複数link同時変動、長時間の非定常jitterを完全には表さない。BAMLMは候補境界層を隣接端末へ事前複製できるだけの余剰GPUメモリを必要とし、メモリが極端に逼迫した端末では移行自由度が小さくなる。全境界の候補割当探索は事前メモリ制約で枝刈りされるが、node数や候補層数が大きい場合の制御計算scalabilityは広く評価されていない。gamma、window、cooldown等の設定も環境依存性があり、論文自身も今後の課題としてhybrid parallelismとより動的なnetwork条件での適応型 partitioningを挙げる。
## 実装状態
ICPP 2026採録の11ページ論文。NVIDIA JetPack 6.2とPyTorch上で実装し、5台のJetson実機clusterで評価されている。論文本文から公開code repositoryは確認できず、今回の一次資料は共著者Jie WuのTemple University公開PDF。
## 研究上の位置づけ
LLM/VLMのedge serving研究の中で、IHS-LMはモデルをCPU/SSDへオフロードする系統というより、複数の小型GPU端末にパイプライン partitionした後の動的スケジューラと配置を扱う。特にKV キャッシュ occupancyをバッチ admissionへ直接使う点はserving スケジューラ系、帯域変動を見て層 boundaryを動かす点はheterogeneous/distributed inference系に接続する。候補層の冗長常駐で重み migrationをcontrol-plane操作へ変換する発想は、動的再構成の通信costをメモリ reservationへ置き換える設計として重要であり、将来のedge MoEやhybrid parallelismにも応用可能な位置付けである。
## 一次資料
- https://cis.temple.edu/~wu/research/publications/Publication_files/ICPP%202026-IHS-LM%20Intra-batch%20Hybrid%20Scheduling%20and%20Layer%20Migration%20for%20VLM%20Pipeline%20Inference%20Acceleration%20on%20Edge%20Devices.pdf
- https://doi.org/10.1145/3832810.3832886
