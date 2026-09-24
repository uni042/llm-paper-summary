---
canonical_id: DOI:10.1145/3838177.3841731
doi: 10.1145/3838177.3841731
title: Unlocking Software-defined GPU Fabric Scheduling in the LLM Era
summary: GPUWeaverは、大規模言語モデル推論でPCIe・NVLink・GPUDirect RDMAが共有資源を競合する問題を、アプリケーション目標とファブリック信号を結ぶ閉ループ通信スケジューリングとして扱う。著者らはDGX-H100と2サーバRDMA環境で、NVLink転送がHBMアクセスを、GPUDirect RDMAがCPU-GPU転送を方向依存かつ非対称に阻害することを実測した。そこで高優先通信が性能目標を外した場合に背景通信の注入を抑える制御層を提案する。vLLMとMooncakeを統合したQwen3-8Bケースでは、プリフィル-デコード間KV転送時間を19.4–34.4%、平均初回トークン待ち時間を2.4–6.1%短縮し、階層メモリのデータ移動と分離推論通信を共同管理する必要性を示す。
list_summary: GPUファブリック競合を監視・通信注入制御し、vLLM+MooncakeでPD KV転送を19.4–34.4%短縮する。
authors:
- Danyang Chen
- Yufeng Gu
- Yibo Huang
- Chengxuan Pei
- Peichun Hua
- Yang Zhou
- Yunming Xiao
authors_affiliations: The Chinese University of Hong Kong, Shenzhen; University of Michigan; University of California, Davis
published: '2026-09-17'
publication: APSys 2026
publication_type: 査読付きワークショップ論文
publication_status: Published at APSys 2026
lineage: LLM serving / GPU fabric scheduling / KV-cache offload / disaggregated inference
topics:
- GPUファブリック
- PCIe競合
- NVLink競合
- KVキャッシュオフロード
- 分離推論
importance: オフロードやプリフィル-デコード分離で増える通信を単なる帯域利用ではなく、暗黙のハードウェア優先度を含む共有資源スケジューリング問題として明示化する。
hardware_evaluation: DGX-H100でHBM/NVLink競合を評価し、2サーバRDMA構成でPCIe競合を評価。統合ケースは論理2サーバ・各1GPU。
quality_effect: モデル品質を変更する手法ではなく通信スケジューリング。評価指標は帯域、転送時間、TTFTで、生成品質への近似は導入しない。
references_checked_at: '2026-09-21'
references_source: primary manuscript
references_total: 47
source: https://doi.org/10.1145/3838177.3841731
sources:
- https://yunmingxiao.github.io/publication/26apsys-gpuweaver/apsys26-gpuweaver.pdf
- https://doi.org/10.1145/3838177.3841731
implementation: GPUWeaverの予備プロトタイプをvLLM+Mooncakeへ統合し、監視信号とオフロード遅延注入を用いる。
last_checked: '2026-09-21'
code: null
references: []
last_audited: null
audit_version: 0
---

# Unlocking Software-defined GPU Fabric Scheduling in the LLM Era

> GPUファブリック競合を監視・通信注入制御し、vLLM+MooncakeでPD KV転送を19.4–34.4%短縮する。
## 書誌情報
- **著者**: Danyang Chen, Yufeng Gu, Yibo Huang, Chengxuan Pei, Peichun Hua, Yang Zhou, Yunming Xiao
- **著者・所属**: The Chinese University of Hong Kong, Shenzhen; University of Michigan; University of California, Davis
- **公開**: APSys 2026
- **種別**: 査読付きワークショップ論文
- **対象**: GPUファブリック、PCIe競合、NVLink競合、KVキャッシュオフロード、分離推論
- **実装**: GPUWeaverの予備プロトタイプをvLLM+Mooncakeへ統合し、監視信号とオフロード遅延注入を用いる。
## 概要
GPUWeaverは、大規模言語モデル推論でPCIe・NVLink・GPUDirect RDMAが共有資源を競合する問題を、アプリケーション目標とファブリック信号を結ぶ閉ループ通信スケジューリングとして扱う。著者らはDGX-H100と2サーバRDMA環境で、NVLink転送がHBMアクセスを、GPUDirect RDMAがCPU-GPU転送を方向依存かつ非対称に阻害することを実測した。そこで高優先通信が性能目標を外した場合に背景通信の注入を抑える制御層を提案する。vLLMとMooncakeを統合したQwen3-8Bケースでは、プリフィル-デコード間KV転送時間を19.4–34.4%、平均初回トークン待ち時間を2.4–6.1%短縮し、階層メモリのデータ移動と分離推論通信を共同管理する必要性を示す。

GPUWeaverの新規性は、GPUファブリック利用をアプリケーションから独立した副作用ではなく明示的なスケジューリング問題として定式化し、通信フローごとの性能目標とハードウェア観測値を閉ループで結ぶ点にある。論文はまずHBMアクセス対NVLink、GPUDirect RDMA対ホスト-device転送の競合を制御実験で分解し、暗黙の優先度を定量化する。その上で、RDMAのQoSやrate limit、CUDA転送のストリーム priority、chunking、launch gating、yieldなど既存ソフトウェアから操作可能なノブを統一制御面に載せ、重要フローが目標を外したときだけ背景通信を抑える。

代表結果として、H2D帯域低下はconcurrent GDR write + H2DでGDR writeなしに対して25.82→5.23 GiB/s（79.8%低下）。PCIe共有区間でGDR writeがH2Dより強いサービス優先を持つ。
## 問題設定
大規模言語モデル推論では、KVキャッシュのCPU退避、プリフィルとデコードの分離、GPU間並列化、計算と通信の重畳によって、PCIe、NVLink、RDMAを同時に利用する場面が増えている。しかし既存のランタイムはGPUファブリックをbest-effortな黒箱として扱い、通信を重ねれば隠蔽できるという前提を置きやすい。実際にはNVLink用DMAとSMのHBMアクセスがL2やメモリ制御器を共有し、GPUDirect RDMAとCPU-GPU転送も同じPCIe区間を通る。しかも仲裁は方向と通信種別によって非対称で、重要なKV転送より背景オフロードが資源を奪う場合がある。従来のジョブ内部スケジューリングや粗い通信停止だけでは、複数LLMタスクのSLOと共有ファブリックの状態を対応付けて制御できない。
## 新規性
GPUWeaverの新規性は、GPUファブリック利用をアプリケーションから独立した副作用ではなく明示的なスケジューリング問題として定式化し、通信フローごとの性能目標とハードウェア観測値を閉ループで結ぶ点にある。論文はまずHBMアクセス対NVLink、GPUDirect RDMA対ホスト-device転送の競合を制御実験で分解し、暗黙の優先度を定量化する。その上で、RDMAのQoSやrate limit、CUDA転送のストリーム priority、chunking、launch gating、yieldなど既存ソフトウェアから操作可能なノブを統一制御面に載せ、重要フローが目標を外したときだけ背景通信を抑える。
## 手法
### 手法のあらまし
GPUWeaverは大規模言語モデルアプリケーションと通信ライブラリの間に位置する軽量ランタイムである。アプリケーションはRDMA転送、collective、ホスト-device copyなどをフローとして登録し、優先度や遅延・帯域目標を付与する。ランタイムはNVML/DCGMのPCIe・NVLinkカウンタ、NICスループット、キュー深さ、GPUメモリ帯域などの基盤信号と、要求遅延、段階遅延、転送遅延、フローbacklogなどのアプリ信号を監視する。共有ファブリックが飽和し、高優先フローが目標を満たさない場合は次の制御窓でそのフローの帯域予算を増やし、背景フローの注入をpacingする。逆に高優先フローが健全なら背景側へ帯域を戻す。RDMAではservice level、NIC QoS、rate limitingを使い、CUDAが直接帯域制御を提供しないホスト-device転送ではストリーム priority、launch gating、chunked copy、cooperative yieldを組み合わせる。vLLM+Mooncakeケースではプリフィル-デコード間のGPUDirect RDMA KV転送を高優先、GPUからCPUへのprefix KV オフロードを背景フローとし、PD handoff窓の間だけオフロード delayを調整する。前ラウンドのPCIe帯域、RDMA帯域、初回トークン待ち時間、オフロード backlogから次ラウンドの遅延または帯域分割を選び、重要通信の完了を早める。

### 競合診断と根因分解
著者らは単なるエンドツーエンド低下だけを見るのではなく、HBMアクセスとNVLink転送、GPUDirect RDMAとホスト-device copyをそれぞれisolated実行とconcurrent実行で比較する。HBM/NVLinkでは128MBから4GBまで両方のサイズを独立に掃引し、どちらの処理時間が長いかで重畳時間と帯域低下がどう変わるかを測る。PCIeではGDR writeとH2D、GDR readとD2Hを方向別に分離し、共有GPU側PCIe区間でどちらが優先されるかを確認する。これにより、総帯域不足ではなくL2、メモリ制御器、PCIe仲裁領域に起因する暗黙優先度を制御対象として抽出する。

### 閉ループ通信スケジューラ
ランタイムはファブリック混雑を示す基盤信号と、どのアプリケーションフローが実際に遅れているかを示す進捗信号を同時に監視する。高優先フローが遅延または帯域目標を外し、かつ共有資源が飽和している場合だけ次の制御窓で帯域予算を高優先側へ寄せる。高優先フローが健全になれば背景backlogを消化するため帯域を戻す。方策自体は固定分割、閾値規則、学習制御器のいずれでもよく、GPUWeaverはフローごとの帯域予算またはpacing決定を受け取れる共通制御層として設計される。重要フローを常時最大優先に固定せず、性能目標が満たされている期間は背景処理へ資源を返すため、保護と総利用率の両立を狙える。アプリ信号と基盤信号を併用することで、単にリンクが混雑しただけなのか、実際にSLOへ影響しているのかを区別して不要な抑制を避ける。

### ソフトウェア可視制御ノブ
ハードウェアの仲裁規則を変更できないため、GPUWeaverは共有ファブリックへ要求を投入する手前で注入率を制御する。RDMAではservice level、NIC QoS、rate limitingを使い、ホスト-device転送ではCUDA ストリーム priority、launch gating、転送の小分割、協調的yieldを組み合わせる。バックエンドごとに具体機構は異なるが、すべてのノブを『各フローが共有PCIe/NVLinkへどれだけ積極的に要求を入れるか』という共通量へ写像することで、アプリケーション目標に沿った優先制御を可能にする。

### KVキャッシュオフロード統合ケース
vLLMとMooncakeを統合したケースでは、プリフィル workerが生成したKVをデコード workerへGPUDirect RDMAで送りながら、prefix KVをCPUへ退避する。両者が同じGPU側PCIe資源を使うため、GPUWeaverはPD信号で保護窓を開き、遅延-criticalなKV転送が不足すると背景オフロードへより大きいdelayを入れる。KV転送が健全ならオフロードへ帯域を返す。実トレース由来のリクエスト shapeと1.2〜9.4GBのKV量を使い、自然重畳する既定方策と比較することで、オフロードを少し遅らせる方が全体TTFTを改善できることを示す。

### 全体のデータ／制御の流れ
設計全体は、アプリケーション意図の登録、ファブリックと進捗の観測、競合根因の判定、フロー別通信注入制御という循環で構成される。重要なのはPCIeやNVLinkのハードウェア仲裁そのものを書き換えるのではなく、既存通信ライブラリの上で投入タイミングと帯域を調整し、階層メモリの背景データ移動と分離推論のcritical pathを協調させる点である。
## 評価条件
- **ハードウェア**: HBM/NVLink競合はDGX-H100上の2 GPUで評価。PCIe競合は2サーバ構成で、Server AのGPUとRNIC、Server BからのGDR read/writeを用いる。統合ケースはプリフィル/デコードを論理2サーバ・各1 GPUとして評価する。
- **ソフトウェア**: CUDAのcudaMemcpyPeerAsync、cudaMemcpyAsync、GPUDirect RDMA、NVML/DCGM監視を利用。統合ケースはvLLM + Mooncake、Qwen3-8B、Codex/SWE-bench Proの実トレース由来リクエスト shape。
HBM/NVLinkは128MB〜4GBの6×6サイズ格子でisolated HBM、isolated NVLink、concurrentを比較し帯域低下率を測る。PCIeはGDR write+H2D、GDR read+D2Hの方向別競合を測定。統合ケースではKV総量1.2〜9.4GBの複数リクエスト shapeでdefault overlapとGPUWeaverを比較し、前ラウンドのRDMA帯域とTTFTを用いて候補PCIe配分を選ぶ。
短い8ページのAPSys論文で、GPUWeaverは予備プロトタイプ。統合評価はQwen3-8B、vLLM+Mooncake、限定された2サーバ相当構成とCodex由来shapeが中心で、NVLink/HBM側へのエンドツーエンド制御適用は将来課題。
## 主要結果
実測ではHBMとNVLinkの同時実行でHBM帯域が典型的に約20%低下し、PCIeではGDR writeがH2D帯域を79.8%、GDR readがD2H帯域を53.9%低下させる強い非対称性を確認した。GPUWeaverをvLLM+Mooncakeへ統合すると、1.2〜9.4GBのKV条件でPD KV転送時間を19.4–34.4%、平均TTFTを2.4–6.1%短縮した。

- H2D帯域低下 / 25.82→5.23 GiB/s（79.8%低下） (比較対象: GDR writeなし; 条件: concurrent GDR write + H2D) — PCIe共有区間でGDR writeがH2Dより強いサービス優先を持つ。

- D2H帯域低下 / 25.12→11.57 GiB/s（53.9%低下） (比較対象: GDR readなし; 条件: concurrent GDR read + D2H) — 逆方向でも強い競合がある。

- GDR read低下 / 約41.5% (比較対象: isolated GDR read; 条件: background D2H、message size 8KB以上) — 方向依存でD2HがGDR readを大きく抑える。

- PD KV transfer flow time / 19.4–34.4%短縮 (比較対象: default overlap; 条件: vLLM+Mooncake, Qwen3-8B, KV 1.2–9.4GB) — 背景オフロードをpacingして遅延-critical RDMAを保護できる。

- 平均TTFT / 2.4–6.1%短縮 (比較対象: default overlap; 条件: 同上) — PD KV転送はTTFT経路の一部なのでエンドツーエンド改善は転送改善より小さい。

### 負の結果・境界条件
- NVLinkは同時HBMアクセス下でも条件によって低下が0–1%程度に留まり、HBM側がより大きく犠牲になる暗黙優先度が観測された。GPUWeaverの現在のpolicyは単純でcontrol actionも粗く、NVLink/HBM競合に対する統合エンドツーエンド制御は未評価。

### 結果の読み方
主要な知見は、GPUファブリック競合が単なる総帯域不足ではなく、方向・トラフィック種別ごとの暗黙優先度を持つ点である。したがってLLM ランタイムは通信を無条件に重畳するより、SLO重要度に応じて注入を制御した方がよい。
## 品質への影響
生成品質の近似は導入しない。性能改善は通信スケジューリングによるもので、品質評価ではなくTTFT・転送時間・帯域を測定する。
## 既存研究との差
CruxやCentauri等が主に訓練・ジョブ内部の計算通信重畳をスケジュールするのに対し、GPUWeaverは複数LLMタスクが共有するPCIe/NVLink/RDMAの注入自体をアプリSLOと結び付ける。既存KVオフロードやPD分離は通信を重畳できることを前提にしがちだが、本研究はその重畳が共有ファブリック上で逆効果になり得ることを実測し、背景オフロードを意図的に遅らせてcritical KV transferを保護する。
## 限界
GPUWeaverは予備的なランタイムで、現行policyは前ラウンド信号に基づく単純な帯域配分・オフロード delay制御である。エンドツーエンド評価はvLLM+Mooncake、Qwen3-8B、限定されたリクエスト shapeと2サーバ相当構成に集中し、大規模クラスタ、多数フロー、異なるGPU世代での一般性は未確認。NVLink/HBM競合は詳細にcharacterizeするが、その経路への統合GPUWeaver制御は将来課題。
## 実装状態
APSys 2026の8ページ論文。vLLM+Mooncakeへ統合した予備プロトタイプを実機評価しているが、論文中に独立した公開コードURLは示されていない。著者公開PDFは利用可能。
## 研究上の位置づけ
LLM階層メモリ研究に対して、CPU/SSDへ状態を移す『配置』だけでなく、その移動がPD転送やGPU間通信と共有するファブリックの仲裁を管理対象にする点が重要。オフロード量を増やすほどPCIe競合が顕在化するため、階層メモリ容量最適化と通信QoSを共同設計する系統へ接続する。
## 一次資料
- https://yunmingxiao.github.io/publication/26apsys-gpuweaver/apsys26-gpuweaver.pdf
- https://doi.org/10.1145/3838177.3841731
