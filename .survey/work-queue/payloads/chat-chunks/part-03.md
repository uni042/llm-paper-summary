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
