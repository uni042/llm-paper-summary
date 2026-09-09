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
