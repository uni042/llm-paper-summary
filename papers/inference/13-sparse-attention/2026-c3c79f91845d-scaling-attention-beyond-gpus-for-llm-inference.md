---
canonical_id: DOI:10.1145/3806645.3807596
title: Scaling Attention Beyond GPUs for LLM Inference
summary: Beyondは、長文脈LLMのKVキャッシュがGPU HBMを超えるとPCIe再転送が律速になる問題に対し、最近のKVはGPUで密注意、重要な古いKVはCPU DRAM上でhead別疎注意として並列処理し、log-sum-expで結果を融合するCPU–GPU協調attention runtimeである。
list_summary: GPU上のrecent KVとCPU上のsalient KVを並列注意機構し、PCIe転送を抑えて長文脈LLMをGPU容量外へ拡張する。
authors:
- Weishu Deng
- Yujie Yang
- Peiran Du
- Lingfeng Xiang
- Zhen Lin
- Chen Zhong
- Faraz Ahmed
- Lianjie Cao
- Puneet Sharma
- Song Jiang
- Hui Lu
- Jia Rao
published: 2026-07
publication: 35th ACM International Symposium on High-Performance Parallel and Distributed Computing (HPDC 2026)
publication_type: conference
publication_status: published
source: https://doi.org/10.1145/3806645.3807596
sources:
- https://doi.org/10.1145/3806645.3807596
- https://huilucs.github.io/pubs/hpdc2026.pdf
implementation: commodity GPUとCPU DRAMを使うdrop-in runtimeとして、KV offloadとCPU–GPU hybrid attentionを実装し、複数モデル・長文脈workloadで評価。今回確認した一次・著者資料から公式コードURLは特定できなかった。
code: null
last_checked: '2026-10-04'
worker_completed_at: '2026-10-04T07:10:00+09:00'
worker_run_key: 20261004-0700-scheduled-chat-00/r01
last_audited: null
audit_version: 0
references:
- canonical_id: arXiv:2308.14508
  arxiv_id: '2308.14508'
- canonical_id: arXiv:2004.05150
  arxiv_id: '2004.05150'
- canonical_id: arXiv:2204.06745
  arxiv_id: '2204.06745'
  doi: 10.18653/v1/2022.bigscience-1.9
- canonical_id: arXiv:2406.16937
  arxiv_id: '2406.16937'
- canonical_id: arXiv:2205.14135
  doi: 10.52202/068431-1189
- canonical_id: DOI:10.52202/075280-3100
  doi: 10.52202/075280-3100
- canonical_id: arXiv:2001.04451
  arxiv_id: '2001.04451'
- canonical_id: DOI:10.1145/3600006.3613165
  doi: 10.1145/3600006.3613165
- canonical_id: arXiv:2406.19707
- canonical_id: arXiv:2211.17192
- canonical_id: arXiv:2502.02770
  arxiv_id: '2502.02770'
- canonical_id: arXiv:2502.13189
  arxiv_id: '2502.13189'
- canonical_id: arXiv:2409.04992
  arxiv_id: '2409.04992'
- canonical_id: DOI:10.18653/v1/2020.emnlp-main.748
  doi: 10.18653/v1/2020.emnlp-main.748
- canonical_id: arXiv:2308.12950
  arxiv_id: '2308.12950'
- canonical_id: arXiv:2303.06865
- canonical_id: arXiv:2406.10774
  arxiv_id: '2406.10774'
- canonical_id: arXiv:2302.13971
  arxiv_id: '2302.13971'
- canonical_id: DOI:10.52202/068431-1800
  doi: 10.52202/068431-1800
- canonical_id: arXiv:1910.03771
  arxiv_id: '1910.03771'
- canonical_id: DOI:10.1109/icde60146.2024.00378
  doi: 10.1109/icde60146.2024.00378
- canonical_id: arXiv:2309.17453
  arxiv_id: '2309.17453'
- canonical_id: arXiv:2503.16428
  arxiv_id: '2503.16428'
- canonical_id: DOI:10.1145/3549937
  doi: 10.1145/3549937
- canonical_id: arXiv:2502.11089
  arxiv_id: '2502.11089'
- canonical_id: arXiv:2007.14062
- canonical_id: arXiv:2205.01068
  arxiv_id: '2205.01068'
- canonical_id: arXiv:2306.14048
  doi: 10.52202/075280-1506
- canonical_id: arXiv:2504.05897
  arxiv_id: '2504.05897'
  doi: 10.1109/dac63849.2025.11133274
references_checked_at: '2026-10-04'
references_source: crossref-deposited-reference-metadata
references_total: 33
---

# Scaling Attention Beyond GPUs for LLM Inference

## 概要
Beyondは、長文脈・多要求の大規模言語モデル（LLM）推論でキー・値キャッシュ（KV cache）がGPUの高帯域メモリ（HBM）を超えたとき、CPU DRAMを単なる退避先として使うのではなく、CPU側のメモリ帯域と演算能力も注意計算へ参加させるCPU–GPU協調ランタイムである。最近のKVはGPU上で密注意（dense attention）、古いが重要なKVはCPU上でヘッド別の疎注意（sparse attention）として並列計算し、両側の部分出力を対数和指数（log-sum-exp; LSE）で数値的に正しく融合する。

狙いは、CPUへオフロードしたKV本体をPCIeでGPUへ戻す経路を避けることにある。CPUからGPUへ送るのは各ヘッドの小さな注意出力とLSE統計だけで、CPU DRAMとGPU HBMの帯域を復号時に同時利用する。FlexGen上の評価では、BeyondはFlexGenとH2Oに対して最大5.6倍、2.1倍の生成高速化を示し、OPT-66Bの4096 CPU-resident KV・バッチ10の単一注意層では再ロード→GPU計算より約11倍高速だった。

## 問題設定
自己回帰復号では、1個または少数の問い合わせ（query）が巨大な過去KVへアクセスするため演算密度が低く、メモリ帯域律速になりやすい。GPU HBMに全KVが収まる間は問題が小さいが、長文脈やバッチ増加で容量を超えると、ホストDRAMからPCIe越しにKVを再ロードする必要がある。PCIe 4.0 x16は実用上最大約32GB/sで、A6000のGDDR6 768GB/sやCPU DRAMの数百GB/sより大幅に狭い。

単純な疎注意はGPUへ置くKVを減らせるが、固定Top-Kではヘッドごとの注意分布差を無視する。論文のOPT-6.7B解析では、同一層でも累積注意重み99%を得るのに必要なKV割合がヘッドごとに約10%から約80%まで変わった。全ヘッド同じKへ揃えると、あるヘッドでは重要KVを失い、別ヘッドでは不要KVを保持する。

## 手法
### 1. recent KVとcontextual KVの階層配置
GPUには直近のスライディング窓のKVを保持し、ここへ通常の密注意を適用する。古いKVはCPU DRAMへオフロードするが、その中から文脈上重要な位置だけをヘッド単位で残し、CPU側の疎注意対象にする。

オフロード時の重要度は直前の注意重みを利用し、各ヘッドの累積注意分布に応じて閾値 (eta) から保持数を決める。固定個数Top-Kではなく、注意が集中したヘッドは少数、分散したヘッドは多めに保持できる。論文の実験では (eta=0.5) の代表分布で選択KVが累積注意重み90%以上を覆う。

### 2. append時だけの再評価
通常の連続復号ではCPUへ落としたKVの文脈重要度を毎ステップ再評価せず、同一セッション中は保持集合を再利用する。新しいプロンプトが追加されるappendでは意味的文脈が変わるため、CPUの非同期スレッドでオフロード済みKVを再評価し、重要集合を更新する。

この設計は毎トークンの高価な再スコアを避ける一方、文脈が変わる境界では古い重要度を固定し続けない。CPU側の疎集合が追加で占めるメモリは実験上、CPUにある総KVキャッシュの平均10%未満だった。

### 3. CPUのヘッド粒度疎注意
選択されたKVを注意ヘッドごとに連続配置し、複数CPUスレッドへ分配する。各スレッドは1ヘッド相当の疎注意を計算し、結果をピン留めメモリへ格納する。バッチが大きいと「バッチ×ヘッド数」だけタスクが増えてCPUスレッドを過剰購読するため、隣接ヘッドを一つのCPUタスクへまとめる。

CPUはGPUよりFP16演算性能が大幅に低いが、復号注意はメモリ帯域律速であり、さらにCPU側では疎化済みKVだけを読むため、条件によってGPUと並行して実用速度で処理できる。

### 4. LSEによる厳密な部分softmax融合
GPU側recent集合とCPU側contextual集合は別々にsoftmaxを計算するため、部分出力をそのまま足すと「全KVへ一度softmaxした結果」と一致しない。Beyondは各集合のLSEを保持し、二つの正規化定数を共通スケールへ変換して部分出力を重み付き結合する。

CPUからGPUへ送るのはKV本体ではなく、各ヘッドの部分注意出力 (O_{cpu}) とスカラーLSEだけである。ゼロコピー（zero-copy）されたピン留めメモリを介してGPU側結果へin-placeで融合するため、PCIe転送量をKV再ロードより桁違いに小さくできる。

## 評価条件
実装は約1.5K行のPython、PyTorch 2.4 + CUDA 12.4、改造FlashInfer 0.1.6である。CPU側疎注意はtorch.jitと多重スレッドで最適化する。評価ハードウェアは、2×Intel Xeon Gold 6430 + 512GB DDR5 + 8×A6000、同CPU + 512GB DDR5 + A100/RTX 4090、2×Intel 8470 + 1TB DDR5 + 2×H100の三系統で、いずれもPCIe 5.0を使用する。

モデルはLlama、GPT-NeoX、OPTを複数サイズで使用する。FlexGen統合ではFlexGen、H2O、InfiniGenと比較し、H2O/InfiniGenは20% KVを使うTop-K疎注意、Beyondは5%をGPUに残して残りをCPU側で処理する。Hugging Face統合では、全KVをHBMに保持できる密注意と、GPU容量を制限したBeyondを比較する。品質はパープレキシティ（perplexity）とLongBenchで測る。

## 主要結果
単一注意層では、CPUに置くKVが512程度と小さい場合は「CPU→GPU再ロード後にGPU注意」の方が速い条件がある。CPU疎注意を起動・融合する固定費が転送節約を上回るためである。一方、CPU-resident KVとバッチが増えるほどBeyondが有利になり、OPT-66B・4096 KV・バッチ10では再ロード方式より約11倍高速になった。これは「常にCPU計算が速い」のではなく、PCIeで大量KVを動かさない効果が規模とともに強くなることを示す。

FlexGenで入力1920トークン、出力128トークンを生成した評価では、Beyondは全バッチでFlexGenとH2Oを上回り、最大5.6倍、2.1倍の高速化を報告した。InfiniGenは速度がBeyondに近いが、予測用のrehearsal attentionバッファが大きく、OPT-66B/A6000ではバッチ15を超えるとメモリ不足になる一方、Beyondはより大きなバッチまで処理できた。

Hugging Face上でバッチ15・4096生成トークンを処理すると、BeyondはKVと注意計算をCPUへ逃がすことで、Lotus-12BやLlama-13Bを密注意より少ないGPU数で最後まで処理できる。長いコンテキストほどCPUとGPUの合計メモリ帯域を利用できるため、GPUを減らしても復号速度の低下が比較的小さい。

品質面では、OPT-6.7Bの密注意PPL 19.12に対し、GPU KV比0.25・(eta=0.75)で19.02、OPT-30Bでは密16.78に対しGPU比0.5・(eta=1.0)で16.75など、同等か僅かに良い条件もあった。ただしLlama2-13Bでは密227.2に対し構成によって225〜341まで変動し、閾値・モデルによって品質低下が起こる。LongBenchではStreamingLLMより多くのタスクで良好だった。

CPUスレッド構成の除去実験では、1タスク2スレッド、合計40〜80スレッド付近が良く、それ以上は過剰購読で性能が落ちた。さらに単一要求で16,384トークンまで生成し、GPU側KVを4096に制限した試験ではメモリ不足なく動作し、末尾でも約3〜4 token/sを維持したが、CPUスケジューリングと負荷不均衡によるTBT外れ値も観測された。

## 既存研究との差
通常のKVオフロードはCPUを容量拡張として使い、注意を実行するたび必要KVをGPUへ戻す。Beyondは「KVがある場所で注意を計算する」ため、CPUを演算主体としても利用する。H2O等のGPU側疎注意と比べても、固定Top-Kではなくヘッドごとの累積注意分布から保持量を変える点、CPU・GPU部分softmaxをLSEで統合する点が異なる。

## 限界
利得はCPU DRAM帯域、コア数、PCIe、GPU HBM帯域の比率に強く依存する。小さいオフロード量やバッチではCPU起動・融合費が勝ち、再ロード方式より遅い。CPU側注意は不規則なヘッド粒度処理なので、多スレッド負荷分散が悪いとTBTのばらつきも生じる。

疎化は完全な密注意ではなく、(eta)を大きくしてCPU側KVを減らすほど速度は上がる一方、モデルによってパープレキシティが悪化する。著者はNVLink-C2C環境でも協調帯域の利点を示すが、最適なCPU/GPU分担はPCIe世代・共有メモリ構成ごとに再調整が必要である。

## 一次資料
- https://doi.org/10.1145/3806645.3807596
- https://huilucs.github.io/pubs/hpdc2026.pdf
