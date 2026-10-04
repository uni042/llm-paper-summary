---
canonical_id: "DOI:10.24963/ijcai.2026/657"
title: "DoMoE: Domain-Aware Semantic Expert Prediction for Efficient MoE Inference Under Expert Offloading"
summary: "DoMoEは、CPUへ退避したMoE expertをGPUへ先読みする際、全履歴tokenとの意味類似度検索を行う代わりに、domain別expert routing tableをoffline構築し、prefillで上位2 domainを選んでdecode時の検索空間を限定する。さらに予測頻度と先読み距離を、予測費用とmiss時expert load費用の和で最適化する。L40上のMixtral-8×7B、Phi-3.5-MoE、Qwen1.5-MoE、Qwen3-30B-A3Bで、意味検索型FMoE比の平均throughputを1.32倍、expert hit ratioを1.22倍にした。"
list_summary: "domain別routing tableでMoE expert予測の意味検索空間を絞り、複数層先予測の頻度も最適化して、expert offloadの先読み精度と検索費用を両立する。"
authors:
  - Yao Mu
  - Fahao Chen
  - Wenbin Zhu
  - Mengying Zhao
  - Zhaoyan Shen
  - Dongxiao Yu
published: "2026"
publication: "Proceedings of the Thirty-Fifth International Joint Conference on Artificial Intelligence (IJCAI-26)"
publication_type: "conference"
publication_status: "published"
source: "https://www.ijcai.org/proceedings/2026/657"
sources:
  - "https://www.ijcai.org/proceedings/2026/657"
  - "https://www.ijcai.org/proceedings/2026/0657.pdf"
implementation: "MoE-Infinityを基盤に約4K LoCを追加し、domain別routing table構築・domain matching・adaptive expert predictionを実装。単一NVIDIA L40 GPU、Xeon Platinum 8480+、1 TB host memoryで4種MoEを評価する。確認済み一次資料にはDoMoE専用の公式コードURLは記載されていない。"
code: null
last_checked: "2026-10-04"
worker_completed_at: "2026-10-04T09:58:00+09:00"
worker_run_key: "20261004-0930-scheduled-chat-30/r01"
---

# DoMoE: Domain-Aware Semantic Expert Prediction for Efficient MoE Inference Under Expert Offloading

## 概要

混合専門家モデル（Mixture-of-Experts; MoE）はtokenごとに少数のexpertだけを実行するため計算量は疎にできるが、全expertの重みをGPUへ常駐させると総parameter容量が問題になる。expert offloadは非活性expertをCPU memoryへ置き、必要になるexpertだけGPUへ移すが、routerが選択してから転送するとdecodeのcritical pathにI/O stallが入る。そこで将来使うexpertを予測して先読みする。

既存のtrajectory型予測は初期層のrouting履歴から後段を推測するため軽い反面、初期情報が弱くmissが連鎖しやすい。意味検索型は現在tokenと過去tokenのembeddingを比較できるため精度が上がるが、全履歴を検索すると予測そのものが重い。DoMoEは、同一domain内ではtokenの意味近傍とexpert選択がより再利用しやすいという観測を使い、検索対象をdomain別に分割する。

offlineでdomain別expert routing tableを構築し、token embeddingとexpert activation pathを保存する。onlineではprefill中にqueryをdomain prototypeへ照合して上位2 tableを選び、decode tokenはそのtable内だけで近傍検索する。さらに毎層予測せず、予測呼出し費用と先読み距離が伸びたときのmiss費用を同時に考えて予測layerを間引く。

単一NVIDIA L40上で4種MoEを評価し、意味検索型FMoE比で平均throughput 1.32倍、expert hit ratio 1.22倍を報告する。重要なのはhit ratio最大化だけが目的ではない点で、予測頻度を減らした完全構成ではhit ratioが2〜3%下がってもthroughputがさらに1.06〜1.12倍伸びる。

## 問題設定

MoE offloadでは、予測が外れると必要expertをCPUから同期的にロードするためstallが発生し、不要expertの先読みはPCIe転送とGPU cache容量を浪費する。したがって予測精度は重要だが、意味検索に長時間を使えば先読みで隠すはずのI/O時間を検索処理が食い潰す。

DoMoEの動機となる測定では、同一domainのtokenはembedding空間でまとまり、expert選択もdomainを跨ぐ場合より転用しやすい。またMixtral-8×7BとPhi-3.5-MoEでは隣接layer間の同一token embedding cosine similarityが平均0.96、peak 0.99超で、近いlayerなら毎層検索し直す冗長性がある。一方、距離が伸びると類似度が低下するため、無制限のmulti-layer-ahead予測はmissを増やす。

## 手法

### domain別expert routing table

profiling dataをdomainごとに分け、各tableへhistorical token embeddingとexpert activation pathを格納する。全domainを一つのglobal tableへ混ぜないため、同じtable容量でも現在queryと無関係なrouting履歴の割合を下げられる。各tableはembeddingをcluster化し、代表cluster centerをdomain prototypeとしてoffline生成する。

新queryのprefillで得たtoken embeddingもcluster化し、query center集合と各domain prototype集合の最大cosine similarityをdomain scoreにする。上位2 domain tableだけをdecode用に選ぶ。1 domainへ強制決定せず、score差が小さい曖昧な場合は2 tableを併用するため、global fallbackを常用せず検索範囲を限定する。

### 意味近傍からのexpert予測とprefetch

decode tokenごとに選択済みdomain table内で意味的に近いhistorical tokenを検索し、そのactivation pathをsimilarity-weighted votingで集約してexpert候補をrank付けする。prefetcherは予測expertをCPUからGPUへ実行前に転送し、実routerが必要としたexpertが未prefetchならon-demand loadして正しさを維持する。

この機構は予測missで計算結果を近似するのではなく、miss時に同期loadへ戻る。そのためモデル品質を直接変えない代わりに、miss率が高いと性能利得が消える。

### adaptive expert prediction

毎層意味検索すると累積予測費用が大きいため、DoMoEは一回の予測を複数後続layerへ使う。layer `l` で予測するかを二値変数 `x_l` とし、最後の予測layerからの距離 `d(l)` に応じた経験的misprediction probabilityを使う。目的関数は各layerの予測呼出し費用 `c_pred x_l` と、miss確率×expert load費用 `p_d(l) c_load` の総和である。

厳密なinteger programをonlineで毎回解くのではなく、この費用構造からsampling-based strategyで予測layer集合を選ぶ。短いhorizonはhit率を上げるが検索回数が増え、長いhorizonは検索を償却するがmissが増える、という交換条件をsystem latencyへ直接落としている。

## 評価条件

|項目|条件|
|---|---|
|GPU|NVIDIA L40 1基|
|CPU / host memory|Intel Xeon Platinum 8480+ / 1 TB|
|モデル|Mixtral-8×7B、Phi-3.5-MoE、Qwen1.5-MoE、Qwen3-30B-A3B|
|active / total expert|2/8、2/16、4/60、8/128|
|workload|DISC-Law、Banking77、PsyDTCorpus、Agentic Coding CoT、PRM800K|
|profiling / test|各datasetの先頭70% / 残り30%|
|比較|MoE-Infinity、意味検索型FMoE再実装|
|実装|MoE-Infinity + 約4K LoC|
|指標|tokens/s、expert hit ratio、CPU footprint|

## 主要結果

|条件|指標|比較|DoMoE|読み取れること|
|---|---|---|---|---|
|全model/workload平均|throughput|FMoE|1.32×|検索範囲削減と予測間引きがend-to-endへ効く|
|全model/workload平均|expert hit ratio|FMoE|1.22×|domain別履歴がrouting signal密度を高める|
|Mixtral, mixed|throughput|MoE-Infinity 0.60 / FMoE 0.85 token/s|1.21 token/s|domain混在でもglobal履歴より高い|
|Phi-3.5, DISC-Law|throughput|1.03 / 1.67 token/s|2.32 token/s|意味検索費用削減が大きい条件|
|Qwen3-30B-A3B, mixed|hit ratio|MoE-Infinity 36% / FMoE 50%|67%|128 expertでも予測精度を維持|
|ablation: Tableのみ|throughput|Trajectory|Mixtral 1.78×、Phi 2.02×、Qwen1.5 1.65×|主利得はdomain table|
|adaptive追加|throughput|Tableのみ|1.07× / 1.12× / 1.06×|hit率2〜3%低下でも検索費用減が勝つ|
|table 100→3000|hit ratio|Mixtral|43.8%→69.9%|table拡大は予測精度を上げる|
|table 2000→3000|throughput|peak比|約7〜8%低下|大tableではsimilarity search費用が利得を相殺|

CPU footprintはFMoEと同等で、Mixtral 25.2 MB、Phi 25.95 MB、Qwen1.5 24.21 MB、Qwen3 25.56 MBと報告される。つまりdomain分割は追加の大容量metadataを積む方式ではなく、同程度の履歴容量をより関連度の高いentryへ使う。

## 既存研究との差

MoE-Infinityはearly-layer trajectoryを利用するため検索は軽いが、後段expertとの相関が弱い。FMoEはsemantic similarityで精度を改善するが、domainを区別しない履歴repositoryを頻繁に検索する。DoMoEはFMoE型のsemantic signalを残しつつ、domain prototypeで検索集合を先に絞り、さらにlayer間embedding類似性を使って検索呼出し自体を間引く。

expert cacheのeviction policyそのものを主に変える方式ではなく、「どのexpertをいつ先読みするか」の予測側を最適化する点が中心である。

## 限界

評価は単一L40 serverであり、複数GPU expert parallelismや同時多数requestでのcache競合は主対象ではない。論文もfuture workとしてlimited GPU memory下のconcurrent servingへの拡張を挙げる。

domain tableは70% profiling splitから作られており、未観測domainや急な分布変化ではprototype matchingとhistorical routingの有効性が低下し得る。tableを増やせばhit率は上がるが、3000 entryではthroughputがpeakから7〜8%落ちるため、履歴量を増やせば単調に速くなるわけではない。

## 一次資料

- https://www.ijcai.org/proceedings/2026/657
- https://www.ijcai.org/proceedings/2026/0657.pdf