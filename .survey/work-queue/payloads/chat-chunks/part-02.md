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
