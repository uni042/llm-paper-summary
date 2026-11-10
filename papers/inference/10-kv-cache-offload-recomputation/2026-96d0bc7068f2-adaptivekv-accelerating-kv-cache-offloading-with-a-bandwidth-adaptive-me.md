---
canonical_id: DOI:10.1145/3821219
title: 'AdaptiveKV: Accelerating KV Cache Offloading with a Bandwidth-Adaptive Memory Allocation Mechanism'
summary: AdaptiveKVはGPUから退避したKVキャッシュをDDRとCXLの複数NUMAメモリへ配置する比率を、GPU観測帯域に基づくランダムフォレストと差分進化で適応制御する。H100単体の制限帯域構成でOPT-1.3B/30BのTPP比スループット1.32～1.80倍、ShareGPT由来3,200要求で1.90倍、vLLMの3モデルで平均1.71倍を報告。ただしマルチGPUは主に帯域競合の模擬で、prefillや尾部遅延を主眼としない。
list_summary: GPU視点のDDR/CXL帯域を予測し、NUMA間KVページの配置比率を実行時に最適化する。
authors:
- Yibo Tang
- Lizhou Wu
- Yang Ou
- Sunfeng Gao
- Yanjing Wang
- Zicong Wang
- Xingyun Qi
- Jiaqing Xu
- Fangxu Lv
- Liquan Xiao
- Mingche Lai
published: '2026-07-10'
publication: ACM Transactions on Architecture and Code Optimization, 23(3)
publication_type: journal_article
publication_status: published
source: https://dl.acm.org/doi/10.1145/3821219
sources:
- https://dl.acm.org/doi/10.1145/3821219
- https://doi.org/10.1145/3821219
implementation: Linux NUMAメモリ管理上の軽量ランタイム。ランダムフォレストで帯域予測、差分進化で割当比率を決定し、vm.numa_tier_interleaveを周期更新。H100 80GB、2 CPUソケット、DDR/CXL構成でOPT-1.3B/30Bを実測。vLLMでQwen3-8B/Llama3-8B/Mistral-7Bも評価。公式コード公開を原著§1で確認。
code: https://github.com/TianheMICALab/AdaptiveKV
last_checked: '2026-10-30'
worker_id: scheduled-chat-00
scheduled_slot: '00'
worker_run_key: 20261030-2202-scheduled-chat-00/r01
worker_completed_at: '2026-10-30T22:15:00+09:00'
reference_main_sha: f62375f526e53e338a3ea74e689a900c4d224731
under16kb_reaudit_target_path: papers/inference/10-kv-cache-offload-recomputation/2026-96d0bc7068f2-adaptivekv-accelerating-kv-cache-offloading-with-a-bandwidth-adaptive-me.md
under16kb_reaudit_source_git_blob_sha: 71fd61aae1645a21c651c0c1fd2998b179dd9bbb
under16kb_reaudit_source_sha256: b567ecd24a6b929729be201f7e450f810d2dc44b6e3a93a7bdcdc5e8a9e40067
under16kb_reaudit_version: 2026-10-07-v1
under16kb_reaudit_passed: true
quality_self_review_passed: true
quality_self_review_version: PAPER-QUALITY-GUIDE-2026-10-07
last_audited: '2026-10-30'
audit_version: 1
references:
- canonical_id: arXiv:2403.02310
- canonical_id: arXiv:2207.00032
- canonical_id: DOI:10.1023/a:1010933404324
- canonical_id: DOI:10.1109/tevc.2010.2059031
- canonical_id: DOI:10.1109/micro61859.2024.00020
- canonical_id: DOI:10.5555/3691992.3691999
- canonical_id: arXiv:2502.07578
- canonical_id: arXiv:2403.11421
- canonical_id: DOI:10.1109/isca45697.2020.00083
- canonical_id: OpenReview:rqn2v1Ltgn0.
- canonical_id: arXiv:2310.06825
- canonical_id: DOI:10.1145/3695053.3731092
- canonical_id: DOI:10.1145/3600006.3613165
- canonical_id: DOI:10.1109/mm.2024.3358861
- canonical_id: arXiv:2406.19707
- canonical_id: DOI:10.1109/isca59077.2024.00036
- canonical_id: DOI:10.1145/3676641.3715987
- canonical_id: arXiv:2409.14317
- canonical_id: DOI:10.1145/3651890.3672274
- canonical_id: DOI:10.1145/3582016.3582063
- canonical_id: arXiv:2409.04992
- canonical_id: DOI:10.1109/hpca57654.2024.00078
- canonical_id: arXiv:2405.04437
- canonical_id: arXiv:2407.00079
- canonical_id: DOI:10.1145/3458817.3476205
- canonical_id: arXiv:2303.06865
- canonical_id: DOI:10.1145/3613424.3614256
- canonical_id: arXiv:2406.10774
- canonical_id: DOI:10.1145/3627703.3650061
- canonical_id: arXiv:2407.21783
- canonical_id: arXiv:2505.09388
- canonical_id: arXiv:2307.09288
- canonical_id: arXiv:2405.14209
- canonical_id: DOI:10.1145/3695794.3695809
- canonical_id: arXiv:2509.03377
- canonical_id: DOI:10.1109/sc41406.2024.00100
- canonical_id: arXiv:2511.20172
- canonical_id: DOI:10.5555/3691992.3692026
- canonical_id: arXiv:2205.01068
- canonical_id: arXiv:2401.09670
- canonical_id: DOI:10.1109/micro61859.2024.00111
references_checked_at: '2026-10-30'
references_source: crossref-deposited-reference-metadata
references_total: 61
---

# AdaptiveKV：DDR/CXLへのKV配置をGPU帯域から適応的に決める

## 概要

大規模言語モデルの推論では、生成済みトークンの鍵・値（KV）キャッシュがGPUのHBMを圧迫する。KVをCPU側のDDRメモリへ退避すると容量を拡張できるが、複数GPUが同じホストメモリを読むと帯域が競合し、デコードが転送待ちになる。Compute Express Link（CXL）メモリを追加すれば転送経路と容量を増やせるものの、CXLの実効帯域は機器、NUMA配置、転送量、GPU負荷によって変動する。固定比率でDDRとCXLへページを配置しても、常に帯域を最大化できるわけではない。

AdaptiveKVは、GPU側から見たDDR/CXL転送帯域を測定し、ランダムフォレストによる帯域予測と差分進化による割当探索を組み合わせて、KVページのNUMA間配置比率を動的に更新する。単一H100を用いた制限帯域の評価でOPT-1.3B/30BのTPP比スループットを1.32～1.80倍へ、ShareGPT由来の連続3,200要求では1.90倍へ改善した。vLLMを用いたQwen3-8B、Llama3-8B、Mistral-7Bの実験でも平均1.71倍を報告する。ただし大部分の実推論評価は単一GPU上で帯域競合を模擬したものであり、実マルチGPUの直接測定と混同してはならない。

## 問題設定：容量ではなく転送帯域が律速になる

GPU内にKVが収まる間は、HBMの高速アクセスで注意計算を続けられる。KVをホスト側へ移すと、生成時に必要な履歴をPCIe経由で取り戻すため、HBM容量の不足は解消しても転送待ちが増える。CPUのメモリ階層を最適化する既存のTiered Page Placement（TPP）は、CPU側のアクセス遅延を中心に判断するため、GPUからの大量連続転送で最も速い配置を必ずしも選ばない。

CXLはDDRと別の接続経路を通じて帯域を提供できるが、単体でDDRより遅い場合もある。固定の1:1配置は、両者の帯域が似ている時には合理的でも、CXL機器が低速な時にはかえって悪化する。さらに同時実行中のGPUやCPUアプリケーションが帯域を使うと、各経路の実効帯域が時々刻々変わる。著者はGPU側の帯域プロファイルを調べ、転送量を一つの階層へ集中させるより複数経路を並行利用した方が速くなる条件を観測した。

## 手法

### 1. GPUメモリの「巻貝」モデル

原著§4.1は、GPUのL1/L2/HBMと、ホストのローカルDDR、リモートDDR、直接接続CXL、スイッチ経由CXLを一つの階層モデルとして整理する。ホスト側の各NUMAノードは異なるメモリ制御器や接続経路を持ち、同時にGPUへデータを供給できる。単一ノードの公称帯域ではなく、GPUから実際に読み出した時の総転送時間と実効帯域を対象とする。

このモデルでは、各ノードへ割り当てるKVページの量が変わると、転送帯域は単純な線形比例をしない。少しCXLへ逃がすだけでDDRの競合が減り総帯域が上がる場合も、CXLの遅さが支配的になって性能が落ちる場合もある。したがって割当比率を公称帯域の比率に固定せず、現在の転送規模と負荷を入力として決める必要がある。

### 2. ランダムフォレストによる帯域予測

原著§4.2は、線形回帰、サポートベクター回帰、ニューラルネットワークなどと比較し、非線形な帯域変動を低費用で近似する方法としてランダムフォレスト（RF）を選ぶ。CPU-GPU間の帯域を事前にプロファイルして学習し、実行中に観測した転送量と実効帯域から各ノードの転送時間を予測する。予測器はCPU上で動き、GPU推論と非同期に実行する。

原著Table 1では、5本の木を用いるRFは決定係数R²=0.996、予測時間4.32ms、モデル容量38KBである。100本の木ではR²=0.998へ改善するが、予測時間54.14ms、容量1,740KBへ増える。わずかな精度改善に対して費用が大きくなるため、軽量な5本構成に実務上の意味がある。同一機器でバッチや系列長が変わっても予測器を全面再学習する必要はないが、CXL機器などハードウェアが変わると再プロファイルが必要になる。

### 3. 差分進化で配置比率を探索

帯域予測器は非線形で微分可能ではないため、著者は差分進化（Differential Evolution、DE）を使ってNUMAノードごとの割当比率を探索する。各ノードへ配置するKV容量をx_i、予測帯域をb_i(x_i)とし、ノードごとの転送時間の最大値とばらつきを小さくする比率を求める。目的は「最も遅いノードが全体の完了を引き延ばす」状態を避けることである。

原著§6.2では30世代、個体数10のDEを8 CPUコアで動かし、平均420msと報告する。RF予測と探索を合わせた更新処理は0.5秒未満で、各バッチの推論後に非同期で実行するためGPU側の実行と重ねられる。ただし、単一の極短要求で毎回更新を待つなら無視できない費用であり、非同期に隠せるという評価条件を外して一般化してはならない。

### 4. 動的NUMAインターリーブ

DEが決めた割当比率を、LinuxのNUMAメモリ管理に反映する。原著Algorithm 1では次のページを割り当てるたびに乱数閾値を生成し、比率に応じた確率で配置先ノードを選ぶ。たとえば4:3:2:1という比率なら、4ノードへのページ割当確率は40%、30%、20%、10%となる。固定順でページを配置すると先頭のノードに転送が集中しやすいため、ランダム化して負荷を分散する。

実装はLinuxの既存NUMA機構を利用し、`vm.numa_tier_interleave`を実行時に更新する薄いランタイム層である。新しいアプリケーションAPIや注意演算の近似を導入せず、KVの内容を変更しない。GPU転送に必要なページ固定はCUDA側で扱い、AdaptiveKVはその処理を変更しない。追加費用は帯域プロファイル、RF予測、DE探索、ページ配置の制御である。

## 評価条件

| 項目 | 原著の実験条件 | 解釈上の注意 |
|---|---|---|
| 主ハードウェア | NVIDIA H100 80GB、2 CPUソケット、DDR/CXLのNUMA構成 | 実推論は主に単一GPU |
| モデル | OPT-1.3B、OPT-30B | モデルサイズの異なる2例 |
| 基準方式 | TPP、固定比率のNUMAインターリーブ | TPPを基準に倍率を報告 |
| 基本要求 | 入力512、出力32トークン | 出力比率が小さくprefill寄り |
| 連続負荷 | ShareGPTから選んだ3,200要求を100バッチへ集約 | 入出力長を実トレースに合わせる |
| vLLM実験 | Qwen3-8B、Llama3-8B、Mistral-7B、バッチ8 | vLLMとの組合せを評価 |
| 競合模擬 | CPU側Mess負荷とDDR4チャネル＋CXL、単一H100 | 実マルチGPUではない |
| 適用境界 | FPGAのCXLメモリエミュレータで帯域・遅延を変化 | 特定構成の閾値であり普遍定数ではない |

## 主要結果

### 1. 配置比率の予測と基本推論

| 条件 | 比較 | AdaptiveKVの結果 | 根拠 |
|---|---|---|---|
| RF 5本 | 帯域予測 | R²=0.996、4.32ms、38KB | Table 1 |
| RF 100本 | 帯域予測 | R²=0.998、54.14ms、1,740KB | Table 1 |
| DE探索 | CPU 8コア | 平均420ms、非同期更新 | §6.2 |
| 転送時間のノード間ばらつき | 固定配置比率 | 62～91%削減 | Fig.13 |
| OPT-1.3B/30Bの基本負荷 | TPP | スループット1.32～1.80倍 | Fig.14～15 |
| 同上 | 固定インターリーブ | 追加3～47%改善 | Fig.14～15 |

固定インターリーブ自体もTPPより1.13～1.63倍速いが、AdaptiveKVは負荷に応じて比率を変えることでさらに改善する。デコード段階が主な利得源であり、OPT-30B・三NUMA・バッチ32では、デコード時間がTPP比41%、固定インターリーブ比4%短縮された（Fig.18）。prefillの計算時間はこの方式の主な改善対象ではない。

### 2. 実トレースと既存サービングへの組込み

| 評価 | 基準 | 固定インターリーブ | AdaptiveKV | 解釈 |
|---|---|---|---|---|
| ShareGPT 3,200要求 | TPP | 1.65倍 | **1.90倍** | 100バッチの総処理時間 |
| vLLMの3モデル平均 | TPP相当の基準 | 1.33倍 | **1.71倍** | Qwen3-8B/Llama3-8B/Mistral-7B |
| CPU側の帯域競合模擬 | TPP | ― | **1.73倍** | 4 DDRチャネル＋CXL、単一H100 |

ShareGPTの3,200要求は系列長で並べて選び、100バッチへ分割して処理した（Fig.19）。入力512・出力32という短い基本実験より、出力トークンが多い実負荷の方がKV転送の占める割合が増えるため、最大1.90倍の利得が出る。vLLMでMistral-7Bの改善がやや小さいのは、Sliding Window Attentionによりホストから読み戻すKV量が少ないためと説明される。

### 3. CXLの帯域と遅延の感度

原著§6.6ではFPGAメモリエミュレータを使い、CXLの遅延と帯域を別々に変える。OPT-1.3B・128バッチの条件で遅延を450～750nsへ変えても推論スループットへの影響は小さい。一方、帯域を増やすと固定インターリーブとAdaptiveKVの両方が改善する。CXL帯域が7.5GB/sを下回ると固定インターリーブはTPPより遅くなる条件があるが、AdaptiveKVは配置比率を下げて悪化を避ける。

著者は5%以上の推論高速化を「意味のある改善」の基準とし、CXL/DDR帯域比が8%以上ならその基準に達することを示す（Fig.23）。8%は特定のFPGA模擬条件における閾値であり、異なるGPU数・DDR世代・CXL構成・ワークロードにそのまま適用できる普遍的な規則ではない。帯域が極端に低いCXLを無理に併用せず、DDR優先へ戻す判断も必要になる。

## 既存研究との差

TPPなどの一般的な階層メモリ管理はCPU視点のアクセス遅延やページ温度を重視する。固定NUMAインターリーブはDDRとCXLを併用するが、実行中の転送量と競合の変化に追従できない。AdaptiveKVはGPU視点の帯域曲線を予測し、複数ノードの転送時間が揃うよう配置比率を動的に更新する。KVを圧縮・破棄するのではなく、同じKVをどのホストメモリへ置くかを変える方式である。原著はvLLMとの組合せを示し、注意計算の実装とは独立した最適化であることを検証している。

## 限界と適用上の注意

実際の推論実験は単一H100と帯域を制限したホスト構成が中心であり、複数GPUが同時にKVを退避する本番環境を直接再現したわけではない。CPU側の負荷発生器による競合模擬は有用だが、GPU間の通信や同時実行の詳細までは含まれない。モデル・NUMAトポロジー・CXL機器が変われば帯域の再プロファイルが必要になる。FPGAエミュレータも複雑な実機の動的遅延特性を完全には再現しない。

この方式はKV転送が支配的なデコードで有利だが、計算律速のprefillや学習、細かな不規則アクセス、尾部遅延を最優先するサービングには直接適さないと原著§6.6が明記する。最大1.90倍は平均的なスループットの結果であり、すべての要求のP95/P99遅延が同じ倍率で改善するという意味ではない。予測器とDEの更新は非同期で隠す前提であり、極短要求で同期実行すれば費用が顕在化し得る。

## 一次資料と公式実装

- [ACM正式全文](https://dl.acm.org/doi/10.1145/3821219)：§3のGPU帯域観測、§4のRF/DE/動的インターリーブ、§6のTable 1、Fig.13～23、§6.6の適用境界を照合。
- [DOI正式書誌](https://doi.org/10.1145/3821219)：ACM Transactions on Architecture and Code Optimization、2026年。
- [著者らの公式実装](https://github.com/TianheMICALab/AdaptiveKV)：原著§1に公開URLを明記。既存原稿の`code: null`を修正。
