# TGI

Text Generation Inference（TGI）の主要な機能・性能更新を継続的に記録する集約ページ。TGIはHugging Faceが提供していたLLM serving engineで、continuous batching、tensor parallelism、quantization、token streamingなどを統合していた。

## 現在できること

- **production向けHTTP serving**: archive前の最終世代では、LLMをserverとして常駐させ、HTTP経由でgeneration requestを受け付けられる。application processごとにmodelをloadする必要をなくし、複数clientから共有できる。
- **continuous batching**: requestを生成途中でもbatchへ出し入れし、短いrequestが終わったあとも残りのrequestと新着requestをまとめてGPUへ流せる。固定batchの終了待ちを減らし、GPU utilizationとthroughputを上げる。
- **token streaming**: response全体の生成完了を待たず、生成されたtokenを順次clientへ返せる。chat UIやinteractive applicationで体感latencyを下げられる。
- **request queueing / admission**: GPUが処理できる同時request数を超えた場合にqueueへ入れ、server全体でrequestを管理できる。client側でGPU memory状況を直接把握する必要を減らす。
- **tensor parallelism**: 1つのmodelのmatrix計算を複数GPUへ分割し、単一GPUに収まらないmodelや高いcompute throughputを扱える。GPU間通信が増えるため、高速linkがある構成ほど有利。
- **量子化model serving**: GPTQ / AWQ / bitsandbytes等の低bit modelを扱い、weight memoryとmemory bandwidthを削減できる。GPU枚数を減らしたり、同じGPUでより大きいmodelを動かしたりできる。
- **optimized attention**: release世代に応じてFlashAttention / PagedAttention系の実装を利用し、attention scoreの一時memoryやKV allocationの無駄を減らせる。
- **KV cache管理**: decode時に過去tokenのK/Vを再利用し、prompt全体を毎token再計算しない。paged系memory管理により、長さの異なるrequestを同時servingしやすくする。
- **prefix / prompt再利用系機能**: 共通prefixを持つrequestでprefill計算を再利用できる世代があり、長いsystem prompt等の重複計算を減らせる。
- **投機的デコード**: 対応releaseではdraft候補をtarget modelでまとめて検証し、1 tokenごとのtarget forward回数を減らす方式を利用できる。
- **metrics / observability**: throughput、queue、latency等を監視するためのmetricsを提供し、production serverとしてcapacityやSLOを観測できる。
- **OpenAI互換系interface**: 既存applicationから移行しやすいAPI形態を利用でき、Hugging Face ecosystemのmodelをserverへ載せる入口として使われていた。

ただし公式repositoryはarchive済みであり、ここでいう「現在できること」は**最終世代に実装済みの機能を既存環境で利用できる**という意味である。新しいmodel architecture、CUDA / ROCm世代、serving技術が継続的に追加されるframeworkとしては扱わない。

## 初期収録期間

2026-06-03〜2026-09-03

## 掲載対象となる更新なし

公式repositoryは **2026-03-21にarchive済み**で、対象期間内に新しいreleaseや本質的なruntime改善は確認できなかった。

そのため、このrepositoryではTGIを「現在も活発に機能追加されるframework」としては扱わず、**既存研究・既存serving stackを読む際の歴史的な参照先**として残す。

archiveは既存binaryや過去releaseが即座に使えなくなることを意味しないが、新しいmodel architectureやCUDA / hardware世代への継続対応は原則期待しにくい。

- [TGI releases](https://github.com/huggingface/text-generation-inference/releases)
