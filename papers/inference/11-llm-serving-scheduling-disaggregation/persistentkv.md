---
canonical_id: "arXiv:2606.26666"
arxiv_id: "2606.26666"
title: "PersistentKV: Page-Aware Decode Scheduling for Long-Context LLM Serving on Commodity GPUs"
summary: "native paged KV layoutを維持したまま、長文decodeのsequence splitとragged batch向けcompact workqueueをrequest状態に応じてFlashInferと切り替え、RTX 3060でB1長文を1.403×、B8長文を1.044–1.080×高速化する。"
source: "https://arxiv.org/abs/2606.26666"
last_audited: null
audit_version: 0
---

# PersistentKV: Page-Aware Decode Scheduling for Long-Context LLM Serving on Commodity GPUs

## 書誌情報
- **著者**: Muhammad Ahmed
- **公開**: arXiv:2606.26666。v1 2026-06-25、v2 2026-07-01
- **種別**: workshop paper / arXiv preprint
- **対象**: long-context decode、paged KV cache、GQA、GPU scheduling
- **実装**: 論文はCUDA kernel、serving harness、calibration artifact、external trace入力経路を評価している。arXiv landing pageから独立した公式code repository URLは確認できず、公開artifactの所在は未確認。

## 問題設定
LLMのdecodeでは各requestが1 stepにつき1 query tokenしか生成しない一方、prefix全体のKV cacheをstreamするためarithmetic intensityが低い。特にconsumer GPU上のlow-active long-context servingでは、単一requestや少数requestだけではGPUへ十分な独立workを供給できない。

PagedAttention系のruntimeはKV cacheをpage tableで管理して断片化を抑え、FlashInferなどはnative paged decodeを高度に最適化している。しかし「最速の単一attention kernel」が必ずしも「request trace全体で最速のschedule」ではない。長いsequenceではsequence方向の並列性を追加したい一方、ragged batchではsequence長ごとのlaunchを増やすとhost/launch overheadが大きくなり、粗いbucketへまとめるとshort rowへ無駄なsplit workを割り当てる。

PersistentKVの主張は万能kernelではなく、**request状態に応じてFlashInferとPersistentKVのwork decompositionを切り替えるadaptive page-aware scheduling**である。

## 手法

### Native block-table GQA decode
KVをcontiguous tensorへrepackせず、serving runtimeのnative block tableを直接参照する。評価shapeは `Hq=32`, `Hkv=8`, `G=Hq/Hkv=4`, head dimension `d=128`。CTAを `(request, KV head, sequence split)` へ割り当て、同じKV headを共有する4 query headsを同一work assignment内で処理する。

attention loopは32-token tileを処理し、page accessorでlogical tokenからphysical pageを引き、FP32のonline-softmax stateを維持する。したがってsupplied KVに対するattention自体は近似・pruningではなくexactで、sequence split後のpartial softmax stateもmerge kernelで数学的に正しく結合する。

### Sequence splittingとrow-local bounds
B1などlow-active状態ではrequest×KV-headだけではCTA数が不足するため、sequenceを `S` 個のrangeへsplitして並列度を増やす。split数が多すぎればmerge overheadが増えるため、これは主要なoccupancy knobになる。

bucket長ではなく各rowの真の `seq_len` からtile数、split境界、prefetch sizeを決める。tileを1つも持たないsplitはneutral softmax stateを書いて早期returnし、不要なQ loadやshared-memory stagingを避ける。

### Compact workqueue
ragged B8でexact-length bucketを使うと、active sequence長の種類に応じて多数のCUDA launchが発生する。PersistentKVは `(row, KV head, split, begin, end)` のうち実際にnon-emptyなtaskだけをcompact queueへmaterializeし、1次元gridで実行する。partial stateはcompact slotへ保存し、2つ目のmerge kernelでrow-local segmented reductionを行う。

これにより一つのroute bucketを維持しつつ、short rowのempty splitを排除し、long rowにはsequence parallelismを残す。

### Calibrated cost model
各decode stepでFlashInfer、PersistentKV length-bucket、PersistentKV workqueueの推定costを比較する軽量roofline-style policyを使う。RTX 3060 artifactではstreaming bandwidth 331.2 GB/s、minimum occupancy 4 CTA/SM、launch overhead 8.19 µsをcalibrationから得る。

PersistentKVへpromotionするにはB8で推定1.05×、B4では1.50×のmarginを要求する。さらに `G=4` 以外と16K未満のshort contextはFlashInferへgateする。B1 long-contextはlength-bucket split、supported B8 long-contextはworkqueue、B4はdefaultでFlashInferを選ぶ。
## 評価条件
- **GPU**: NVIDIA RTX 3060 12 GB、28 SM
- **Software**: CUDA 12.1、PyTorch 2.5.1
- **Attention shape**: FP16、`Hq=32`, `Hkv=8`, `G=4`, `d=128`
- **Page size**: 16。main serving tracesではhole fraction 0、isolated native-paged benchmarkでは50% holes
- **Primary baseline**: FlashInfer 0.2.5
- **Isolated comparison**: vLLM 0.6.4.post1、TensorRT-LLM 0.8 MMHA、repack + PyTorch SDPA
- **Correctness**: FlashInfer出力に対し `max |e| < 2e-3`, `mean |e| < 3e-4`
- **Timing**: CUDA-event timingと、Python planning・metadata construction・launch・synchronizationを含むsynchronized wall timingを併記
- **Trace**: bucketed、homogeneous、bimodal、uniform、Zipf。main結果はsynthetic trace。外部CSV/JSON trace入力も実装し、redistributable mixed fixtureで確認
- **Calibration**: seed 20260622でpolicy/split operating pointを固定し、20260623–20260627の5 held-out seedsで評価

## 主要結果

### 単一native-paged kernelではFlashInferが最速
B1 isolated attentionではPersistentKV自体がFlashInferを上回るわけではない。8K / 32K / 64KでFlashInferは **0.1201 / 0.4404 / 0.8686 ms**、PersistentKV auto-splitは **0.1255 / 0.4597 / 0.9069 ms**。PersistentKVはそれぞれ約1.044–1.045×遅い。一方、同じ環境のvLLM PagedAttentionよりは低latencyだった。

したがってmain resultはkernel単体の優位性ではなく、low-active/ragged servingでの**work assignment**の改善として解釈する必要がある。

### B1 long-context
Bucketed B1ではPersistentKV bucket、split 32を選択し、5 held-out seeds平均でFlashInfer比:
- CUDA decode-token throughput: **1.471±0.037×**
- synchronized wall throughput: **1.403±0.065×**

sequence方向へworkを分割してlow occupancyを改善した効果が最も大きいregimeである。

### B8 long-context
compact workqueueを使うB8ではwall throughputが:
- bimodal: **1.080±0.050×**
- uniform: **1.044±0.022×**
- Zipf: **1.068±0.028×**

となり、平均改善幅は**1.044–1.080×**。B1ほど大きくないが、異なる長さのrequestが混在するtraceでも5 seedsでpositiveだった。

### B4境界とGQA gate
B4 workqueueのsplit sweepでは最良mean wall ratioでも **1.005×**、seedごとは **0.964–1.026×**で安定した勝ちにならなかった。このためdefault policyはB4をFlashInferへrouteし、regressionを避ける。

同様にsmall B8 sweepで `G=1` と `G=8` はPersistentKVへ送らずFlashInferへgateし、`G=4`のみPersistentKV workqueueを使う。これはsystem-levelにはno-regressionだが、PersistentKV kernelそのものがG=1/8で高速化したことを意味しない。

### Raggednessとlaunch fan-out
held-out bimodal B8でexact-length bucketsは**16.00 launches/step**、compact workqueueは**2.00 launches/step**。merge trafficも **4.06→2.54 MB/step**、merge launchesは **8.00→1.00**へ減る。workqueueはragged batchでsequence splitを残しながらroute数増加を抑えることが主要効果。

### Attention + MLP proxy
synthetic Llama-style gated MLP tailをattention後へ追加したproxyでも、B8 bimodal 5 seedsでwall decode-token throughputは **1.105±0.061×**。ただしこれはfull LLM serverでもfull transformer stackでもない。

外部mixed trace fixtureではadaptive workqueue routeがwall throughput **1.212×**を示すが、production trafficの代替ではない。
## Hardware counterとablation
短いB8 bimodal G=4 traceのNsight Computeでは、FlashInfer decodeに対してPersistentKV decodeはSM throughput指標 **9.55→17.21**、memory-throughput指標 **62.72→74.48**。ただしprofiler replayを使ったshort traceであり、main 5-seed wall speedupの直接測定ではない。

CUDA graph replayはB4のtwo-kernel decode+merge overheadを解消できなかった。最終split CTAがatomic counterで完了検出してmergeまで行うfused variantも正しいがRTX 3060では遅く、saved launchよりatomic/in-kernel merge costが大きかった。このnegative resultからもB4をFlashInferへ戻すpolicyが妥当とされる。

## 既存研究との差
PagedAttention/vLLMはKV cache allocationとpaging、FlashInferは高速native-paged attention kernelを中心に扱う。PersistentKVはKV量を減らすのではなく、**native page layout上のdecode workをrequest/KV-head/sequence-splitへどう割り当てるか**をserving stateに応じて変える。

H2O等のKV eviction/pruningとは補完的で、PersistentKVは与えられたKVに対してdense exact attentionを維持する。Sarathi/Sarathi-Serveがprefill/decodeの混在scheduleを扱うのに対し、本研究はdecode内部のpage-aware work decompositionに焦点を絞る。

特に重要なのは、FlashInferを全面置換しない設計である。isolated kernelやB4、未校正GQA shapeでは強いbaselineをそのまま使い、PersistentKVが有利とcalibrationされたlong-context regimeだけ新routeへ送る。

## 品質への影響
KV compression、token pruning、近似attentionは使わない。split-local online-softmaxを数学的にmergeするため、対象attention演算はexactである。serving tableの最大誤差は報告上 **6.104e-5**で、設定したFlashInfer-equivalence toleranceを満たす。

したがってmodel quality trade-offを狙う方式ではないが、full model generation品質をtask benchmarkで評価した研究でもない。正しさの中心はkernel output equivalenceである。

## 限界
- main評価は**RTX 3060 1機種**。A100、L4/L40S、H100等での再calibration/再現は未実施。
- B8改善は4–8%程度と比較的小さく、hardware/runtime更新で閾値が変わる可能性が高い。
- main traceはsynthetic。external fixtureはあるがproduction serving logではない。
- harnessはdecode loopであり、admission control、prefill/decode interference、sampling、network、CPU queue、full transformer stack、実際のKV allocator pressureを含まない。
- model-level評価もattention + 1 synthetic MLP tailのproxyに留まる。
- physical page allocationはseeded synthetic permutationで、production allocatorのeviction/reuse/locality特性は再現しない。
- PersistentKVのpositive resultは現在 `G=4` に限定され、G=1/8はFlashInferへのfallbackでno-regressionを達成しているだけ。
- baseline versionはFlashInfer 0.2.5、vLLM 0.6.4.post1、TensorRT-LLM 0.8であり、将来/current stack全般への優位性は主張できない。

## 実装状態
論文v2はCUDA kernel、serving harness、calibration JSON、CSV/JSON trace path、Nsight captureなどのartifactを明示し、CLI ablation flagも記述している。ただしarXivのCode/Data欄および本文から独立した公式GitHub repository URLを確認できなかったため、公開コードの入手先は**未確認**とする。論文中でartifactが存在することと、第三者が公開repositoryから取得できることは区別する。

## 研究上の位置づけ
consumer GPUでlong-context LLMをservingするとき、最適化対象を「attention kernelの計算式」だけでなく「1 decode stepでGPUへ露出するwork量とlaunch構造」まで広げた点が有用。特に、最速baselineをfallbackとして保持しながら狭い勝ちregimeをcalibrated routerで利用する設計は、異なるGPUやruntimeへ展開する際にも現実的なsystem design patternである。

一方で現時点のevidenceはworkshop-levelで、production integrationと複数hardwareでの検証が次の主要課題となる。

## 一次資料
- https://arxiv.org/abs/2606.26666
- https://arxiv.org/pdf/2606.26666v2
