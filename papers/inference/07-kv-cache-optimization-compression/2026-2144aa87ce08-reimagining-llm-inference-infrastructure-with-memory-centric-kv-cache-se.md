---
canonical_id: SemanticScholar:e3397bfa8a64c83dc88c08dcfab676c8255d6a1b
title: Reimagining LLM Inference Infrastructure with Memory-Centric KV Cache Servers
summary: KVキャッシュの容量・帯域が支配する長文脈LLM推論に対し、CXL接続メモリを独立したKVキャッシュサーバとして設計する構想を提示する。DDRx拡張、PNM、PIMを備える3段階の装置類型と、共有KV・GPUからの復号分離・メモリ装置内推論の3運用を提案する。DeepSeek-R1-671Bの32K生成を対象とした帯域律速の解析では、19基のH100と23基のPIM-DIMMの比較で理論スループット679対1607 token/sを試算する。ただし実機の端対端測定ではなく、GPU側CPU/スイッチ費用除外やPIM内部帯域とCXL外部帯域の違いに注意が必要である。
list_summary: CXL接続のKVキャッシュ専用メモリ階層とPNM/PIMへの復号移管を提案。DeepSeek-R1の解析で2.4倍の理論スループットを示すが、実機検証ではない。
authors:
- Khyati Kiyawat
- Kevin Skadron
published: '2026-06-28'
publication: 3rd Workshop on Hot Topics in System Infrastructure (HotInfra 2026), co-located with ISCA 2026
publication_type: workshop_paper
publication_status: published
source: https://hotinfra.org/2026/papers/hotinfra26-final59.pdf
sources:
- https://hotinfra.org/2026/papers/hotinfra26-final59.pdf
- https://hotinfra.org/2026/index.html
implementation: 提案するKVキャッシュサーバ全体の実装・実機評価は示されず、DeepSeek-R1-671Bの帯域、コスト、電力を仮定した解析モデルと装置構想を提示。既存Sangam、CENTなどの先行PIM研究を根拠として参照するが、本論文固有の実装測定ではない。
code: null
last_checked: '2026-10-28'
worker_id: scheduled-chat-30
scheduled_slot: '30'
worker_completed_at: '2026-10-28T06:32:19+09:00'
worker_run_key: 20261028-0632-scheduled-chat-30/r01
reference_main_sha: cd31d037746f0f7adeedfc11f7a0261bc7c08a31
quality_self_review_passed: true
quality_self_review_version: PAPER-QUALITY-GUIDE-2026-10-07
last_audited: null
audit_version: 0
references:
- canonical_id: arXiv:2407.00079
  arxiv_id: '2407.00079'
- canonical_id: arXiv:2512.18194
  arxiv_id: '2512.18194'
- canonical_id: arXiv:2511.12286
  arxiv_id: '2511.12286'
- canonical_id: arXiv:2311.18677
- canonical_id: arXiv:2501.12948
  arxiv_id: '2501.12948'
- canonical_id: arXiv:2403.00579
- canonical_id: arXiv:2312.07104
- canonical_id: arXiv:2510.09665
  arxiv_id: '2510.09665'
- canonical_id: DOI:10.1145/3600006.3613165
- canonical_id: DOI:10.1145/3620665.3640422
- canonical_id: arXiv:2412.15605
- canonical_id: arXiv:2511.20172
  arxiv_id: '2511.20172'
- canonical_id: arXiv:2511.00321
  arxiv_id: '2511.00321'
- canonical_id: arXiv:2509.03377
  arxiv_id: '2509.03377'
- canonical_id: arXiv:2504.17584
  arxiv_id: '2504.17584'
- canonical_id: arXiv:2401.09670
references_checked_at: '2026-10-27'
references_source: primary-pdf-reference-section
references_total: 28
---

# Reimagining LLM Inference Infrastructure with Memory-Centric KV Cache Servers：KVを中心に組み替えるLLM推論基盤

## 概要

本論文は、GPUを計算能力の大きさで増設する従来のLLMデータセンター設計が、長文脈・長い推論出力・複数エージェント間の接頭辞共有という負荷に必ずしも合致しないと論じる。重要なのは演算器の理論FLOPSだけではなく、復号時に繰り返し読む重みとKVキャッシュの容量、アクセス帯域、他の要求との共有可能性である。著者はKVキャッシュをGPU内の一時バッファではなく、計算装置から独立した第一級のメモリ資源として扱う「KV cache server」を提案する。

設計の中心はCXL接続メモリの3種類の類型である。単なる大容量DDRx拡張、メモリ近傍処理（PNM）付き、メモリ内処理（PIM）とPNMを備えた装置を、要求のprefill・decode比率に応じて使い分ける。DeepSeek-R1-671Bの32Kトークン生成に対する解析では、19基のH100 GPU構成の679 token/sに対し、23基のPIM-DIMM構成を1607 token/sと試算する。しかしこの値は**仮定した内部メモリ帯域に基づくモデル計算**であり、KVキャッシュサーバを構築して測定したスループットではない。GPU側の費用計上範囲やCXLリンク帯域との非対称性も、実用化判断では不可欠である。

## 問題設定：演算性能よりもKV容量・帯域が先に詰まる

自動回帰生成は、長い入力を一度処理するprefillと、既存KVを参照しながら1トークンずつ出すdecodeとで資源特性が異なる。著者はdecodeの演算強度を約0.5 ops/byteと記述し、H100の計算能力を使い切る条件から大きく離れていると論じる。論文中のLLaMA-3-70Bの例では128K文脈のKVが要求当たり34GB、モデル重みが約140GBとされ、80GB HBMのH100単体では収まらない。これはGPUメモリを増やすためにGPU演算器も追加購入する非効率を示す。

同時要求が増えるとKV容量は系列長とバッチの積にほぼ比例して伸びる。Figure 1はDeepSeek-R1-Distill-Qwen-14Bを対象に、1Kから32Kの系列長とバッチ1から64の組み合わせでメモリ要求が増える様子を示す。32K、バッチ32では合計228GBとされ、単一のH100 80GBを超える。これらの数値は異なるモデル例を用いて問題の二面性を説明するものであり、70Bの34GBと14Bの228GBを同一構成の値として比較してはならない。

KV再利用の機会も大きい。著者は先行する運用研究から50～90%のKV再利用率、複数エージェントでは75～95%という報告を引用する。これらは**本論文が新たに実測した再利用率ではない**。共通システムプロンプトのKVを要求ごとにGPU HBMへ複製するより、共有メモリへ一度だけ置き、必要なGPUやメモリ演算装置が参照できる仕組みが重要になる。

## 手法：KV cache serverの装置・通信・運用

### 1. 三つのCXL接続メモリ類型

**類型I：CXL DDRx expander** は計算器を持たない容量拡張装置である。GPUやCPUで作成したKVをCXL接続の共有プールに置き、複数のdecode側から再利用する。入力は生成済みKVとアクセス要求、処理は共有アドレス空間での保持・参照、出力はGPU側が再利用できるKVデータとなる。複数GPUに同じ接頭辞KVを複製する容量を抑えるが、復号演算自体はGPUに残り、CXL転送帯域・遅延が新しいボトルネックになり得る。

**類型II：CXL + PNM** はメモリ装置の制御器や近傍演算器に、トークン選択、オーケストレーション、メモリ帯域律速処理の一部を移す。類型Iと違って、KVを読むためだけにGPUやCPUへ全データを往復させる必要を減らす余地がある。ただし何をPNMへ移せるかは演算器の機能に依存し、論文は単一の固定されたPNM実装や全モデル対応の実行環境を提供していない。

**類型III：CXL + PNM + PIM** はメモリバンク内の高い内部帯域を使い、GEMV、平坦化GEMM、注意計算、場合によっては生成処理全体をメモリ側で実行する構想である。CPU/GPUからKVを引き出すのでなく、重み・KVに近い位置で演算することで、decode時のデータ移動を減らす。著者は既存のSangamやCENTを関連する構成例として引用するが、それらの測定結果は本論文の新規サーバ実測と同義ではない。

### 2. 三つの運用シナリオ

**共有KV + GPU decode**：prefill GPUがシステムプロンプトのKVを一度生成し、類型Iのプールへ書く。複数のdecode GPUがCXL経由で同じKVを読む。RAGや複数ターン対話など、共通接頭辞が長くGPU側のバッチが十分大きい用途を想定する。利得はKVの重複保持回避であり、GPU側のdecode計算が消えるわけではない。

**GPU prefill + PNM/PIM decode**：GPUが最初のprefillを行い、生成したKVを共有メモリへ格納する。その後の低バッチ・長出力decodeを類型II/IIIのメモリ側へ移し、GPUを別要求に解放する。ここでの主要な選択軸は、GPUの演算器を遊ばせたままメモリを読み続けるより、メモリ内の比較的単純な演算器を利用した方がよいかである。GPUからPIMへの移行コスト、初期prefillの償却、対応演算の網羅性は実装時に評価が必要となる。

**CXL装置内の端対端推論**：接頭辞KVが既に計算されている、あるいは新規prefillがほとんど不要な場合、類型IIIが増分prefillも含めて推論を実行する。GPUは最初のprefill後に解放できる。これは「CXLメモリならどのLLMもGPU不要」という一般的主張ではなく、PIMが必要な演算を実装し、メモリ内で重み・KVへアクセスできる構成を仮定する。

### 3. 階層オーケストレーションとメモリ間ファブリック

CPUは依存関係の境界で全体を調整し、独立タスクの割当・実行をCXL Fabric Managerまたはメモリ装置側の局所制御器へ委譲する。単純なDDRx拡張ではCPUに多くの制御が残り、PNM/PIMを備える装置ほど内部処理を自己完結できる。複数エージェントの共通プロンプトKVは共有プール、個別の会話KVは各装置のローカル領域に置くという分離も提案する。

さらに、GPUを経由しないメモリ装置同士の直接転送ファブリックを構想する。これはCXL接続、メモリ内演算、GPU間NVLink/UALinkなどを組み合わせた将来設計であり、すべてが現時点の汎用CXL実装で実現・性能確認済みという意味ではない。KV共有の効果はアクセス権管理、同一接頭辞の同定、装置間通信遅延、キャッシュ失効といった未解決の運用要素にも左右される。

## 評価条件：DeepSeek-R1-671Bの解析モデル

| 項目 | 論文の条件・仮定 |
|---|---|
| 対象モデル | DeepSeek-R1-671B、1トークン当たり活性パラメータ37B、61層、MLA潜在次元512 |
| ワークロード | 32Kトークンの長い生成、平均KV参照位置16K、定常decode中心 |
| 数値形式 | 重み・KVはBF16相当の2 bytes/element |
| GPU構成 | H100 SXM5 80GB ×19、合計HBM 1520GB |
| メモリ構成 | 64GB PIM-DIMM ×23、CXLスイッチ2台、CPU1台、合計1472GB |
| 演算律速の近似 | 活性重み読出し約74GB/token + MLA KV約1.02GB/token = 約75GB/token |
| 帯域利用率 | GPU/PIMとも有効利用率η=0.80と仮定 |
| PIM内部帯域 | 1 DIMM当たり6.55TB/s、23 DIMM合計150.7TB/s（CXLリンク帯域とは異なる） |
| 費用仮定 | PIM-DIMM $12/GB、H100レンタル$3/時間、電力$0.12/kWh、PUE 1.4 |
| 測定形態 | 実機ベンチマークではなく帯域・価格・電力を仮定した解析モデル |

モデルはトークン当たりの重み読出し74GBとMLA KV読出し1.02GBを加え、約75GB/tokenとする。理論スループットは `η × 集約内部帯域 / トークン当たり読出し量` で求める。PIMの集約帯域150.7TB/sは各DIMMの内部バンク帯域の合計であり、外部CXLネットワークが150.7TB/sを運べるとする実測値ではない。この区別が本稿の最重要な解釈条件である。

## 主要結果：解析上の速度・費用・電力

| 指標 | GPU構成（19×H100） | KVサーバ構成（23×PIM-DIMM） | 読み方 |
|---|---:|---:|---|
| 集約帯域 | 63.7 TB/s | 150.7 TB/s | PIM側は内部バンク帯域、2.4倍の計算上の差 |
| decodeスループット | 679 token/s | 1,607 token/s | 同じη=0.8を置いた帯域律速推定、2.4倍 |
| 購入費用 | $570,000 | $27,664 | 20.6分の1、GPU側CPU・NVスイッチ費用を除外 |
| 運用費 | $59.23/h | $3.53/h | 16.8分の1、PIM側レンタル料をCapEx比例で推計 |
| PUE込み消費電力 | 18.6 kW | 1.49 kW | 12.5分の1、装置仕様に基づく推定 |
| Tokens/Watt | 0.051 | 1.507 | 29.5倍、実機測定の電力効率ではない |
| 100万トークン当たり費用 | $24.24 | $0.61 | 39.7分の1、上記費用・速度仮定から算出 |

Table 1の数字は非常に大きいが、**速度・コスト・エネルギーを独立に実測した結果ではない**。同じ帯域律速式、想定価格、想定電力から派生した値が多く、前提を変えると同時に変わる。とりわけGPU構成の費用からCPU・NVスイッチを除く一方、KVサーバ側にはCPU・CXLスイッチを計上しているため、両者の費用範囲は完全には対称でない。またGPUの$3/hを起点に、PIM側のクラウドレンタル価格を購入費用比例で推定しており、市場の実料金ではない。

32K出力の定常decodeでは初期prefillを長い生成で償却できると仮定する。短い回答、初回起動、KVが共有されないワークロードではprefill・転送・スケジューリングの相対費用が大きくなり、この表の倍率をそのまま使えない。PIM内部帯域を使うためには重み・KVの配置と演算が同じ装置内で完結する必要があり、GPUへの頻繁な往復がある構成ならCXL転送が制約になる。

## 既存研究との差

vLLM、SGLang、LMCache、Mooncakeは主としてソフトウェア側でKVの配置、再利用、退避、分散転送を管理する。本論文はそれらを置き換える単一のキャッシュアルゴリズムではなく、ソフトウェアが管理するKVの背後に**独立したCXLメモリサーバ階層を設ける**というハードウェア基盤の提案である。TraCTやBelugaなどのCXLベースKV退避方式はGPUで演算を続けるのに対し、類型II/IIIは演算の一部または全部をメモリ近傍へ移す。

NeuPIMs、CENT、SangamなどのPIM系研究はメモリ内演算やGPUを使わない生成の実装可能性を示してきた。本稿は特定PIMチップのカーネル最適化ではなく、DDRx共有プールからPIM推論までを一つの装置スペクトラムとして整理し、prefill/decode分離とエージェント共有の運用モードを対応付けた点に位置付けがある。逆に、その統合制御・キャッシュ一貫性・セキュリティ・マルチテナント隔離の実装を完成させたわけではない。

## 限界と研究上の位置付け

本論文は4ページのワークショップ構想・解析論文であり、KVサーバ全体を実装したプロトタイプのTTFT、TPOT、P99遅延、同時要求数、ネットワーク転送量、CXLリンク飽和、キャッシュヒット率を実測していない。Table 1はハードウェア仮定と解析式の妥当性を検討するための見積もりであり、既存GPUサービスとの実証済み性能差として引用してはならない。原著が引用する先行システムの測定値も、本稿独自の測定と区別する。

MLAを用いるDeepSeek-R1のKVがMHAより小さいことは、KV専用サーバの優位を無条件に保証しない。重み読出し74GB/tokenが大きい解析条件では、PIMの内部帯域を利用できることが主要な利得の源泉である。KVのみをCXL外部リンクからGPUへ移動する類型Iでは同じスループットを実現できると示されていない。対象モデルのMoE専門家配置、expert通信、実際の活性パラメータのメモリ再利用、GPUカーネル効率もモデル式の精緻化が必要である。

今後の検証には、共有接頭辞の書込みと読み出しの同時負荷、複数ホストのCXL帯域争奪、KV一貫性・アクセス制御、GPU↔PIM間の移行、PIM上でのGEMM/GEMV実装、クラウド運用価格の実測が必要となる。長文脈・高再利用・decode中心の負荷では有望な設計仮説だが、短文・低再利用・prefill中心の負荷に同じ経済性を外挿できない。推論基盤の調査では「CXLメモリ階層の設計提案と解析評価」として収録し、「既存GPUに対する実機2.4倍高速化」とは分類しない。

## 一次資料

- Khyati Kiyawat and Kevin Skadron, *Reimagining LLM Inference Infrastructure with Memory-Centric KV Cache Servers*, HotInfra 2026, June 28, 2026. https://hotinfra.org/2026/papers/hotinfra26-final59.pdf （Figure 1・2、§2の3類型、§3の式とTable 1、§4の関連研究、限界を照合）
- 会議の公式プログラム: https://hotinfra.org/2026/index.html
