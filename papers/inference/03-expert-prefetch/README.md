# Expert Prefetch

MoEで次に使われるexpertを**routing結果が確定する前に予測して先にGPUへ読み込む**ことで、CPU / storageからの重み転送待ちを隠す研究をまとめる。予測器、過去のrouting履歴、前のlayerの状態などを使って将来のexpert需要を見積もり、現在の計算と次の転送を重ねるのが基本形となる。

一部の手法はexpertを小さく分けたり、予測したexpertをそのまま使うなどして、予測ミス時の追加I/Oまで減らす。将来需要の予測をcache保持判断に使い、必ずしも先読み転送しない方式も含む。最終目的が推論高速化であるため、予測器自体に学習が必要でもこの系統に分類する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（14本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。「リポジトリ内被引用」は収録済み別論文の本文・メタデータから arXiv ID / DOI の明示参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 直近12か月（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-09 | [Cache-Aware Joint Router Adaptation for Memory-Efficient MoE Inference](2026-2609.04895-cache-aware-joint-router-adaptation.md) | ✓ | 0 | MoEの実行expertを決めるnative Top-Kと、GPUにどのexpert weightを残すかというcache管理を分離し、cache側をmodel内の軽量routerで学習する。Temporal Routerは同じlayerで次tokenにも使われそうなresident expertを残すだけなので余計なprefetch trafficを出さない。Spatio-Temporal Routerはさらに次layer到達前のhidden stateから需要を予測し、上限R個だけnon-resident expertを先読みする。Qwen3では最強の評価対象prefetch baseline比でexpert-weight trafficを4.6〜53.3%削減。 |
| 2026-08 | [SPICE: Speculative Prefetching with Low-Rank Expert Surrogates and Heterogeneous Orchestration for MoE Inference Acceleration](2026-2608.21240-spice-speculative-prefetching-low-rank-expert-surrogates-heterogeneous-orchestration.md) | [✓](https://anonymous.4open.science/r/SPICE) | 0 | 数layer先で使うMoE expertを予測してCPU DRAMからGPUへ先読みし、予測外れのうち重要度が低いexpertは常駐shared expert＋小型補正で近似し、正確な計算が必要な残りはPCIe混雑に応じてCPU実行かGPUへのweight転送へ振り分けることで、expert待ちを減らす。 |
| 2026-06 | [SpecPrefetch: Parameter-Efficient Expert Prefetching for Sparse MoE Foundation Models](2026-2607.24787-specprefetch-parameter-efficient-expert-prefetching-for-sparse-moe-foundation-mo.md) | [✓](https://github.com/wei390/SpecPrefetch) | 0 | 小型predictorで次layerのexpertを必要そうな順に並べ、対象layerへ到達するまでの残り時間と実測storage帯域から『間に合う数』だけを先読みして、実行時にexpertが準備済みである割合を高める。 |
| 2026-03 | [Speculating Experts Accelerates Inference for Mixture-of-Experts](2026-2603.19289-speculating-experts-accelerates-inference-for-mixture-of-experts.md) | [✓](https://github.com/axonn-ai/yalis/tree/offload_prefetch) | 0 | 現在layerのhidden stateから次layerで使うexpertを予測し、weight転送だけでなくexpert FFN計算まで先に実行する。native routerと一致すれば先行結果を再利用し、外れれば正しいexpertを読み直して再計算するlossless方式。 |
| 2026-03 | [FIRM-MoE: Fine-Grained Expert Decomposition for Resource-Adaptive MoE Inference](2026-firm-moe-fine-grained-expert-decomposition-for-resource-adaptive-moe-inference.md) | ✓ | 0 | expert weightを複数の小さな行列単位へ分け、複数の前layerが共通して必要と予測したexpert部分を優先して先読みし、VRAMとPCIe帯域に合わせて先読み量を変えるMoE推論方式。 |
| 2026-03 | [CommitMoE: Efficient Fallback-Free MoE Inference with Offloading Under GPU Memory Constraints](2026-commitmoe-efficient-fallback-free-moe-inference-with-offloading-under-gpu-memory.md) | ✓ | 0 | 次layerで使うexpertを予測してGPUへ先読みし、予測が外れても正しいexpertを読み直さず、準備済みexpertをそのまま使うことでoffload待ちをなくす近似MoE方式。 |
| 2026-03 | [CasMoE: A Cascaded Framework for Efficient MoE Inference on Resource-constrained Devices](2026-casmoe-a-cascaded-framework-for-efficient-moe-inference-on-resource-constrained-.md) | ✓ | 0 | 過去に似たpromptがあればその時のexpert利用履歴を再利用し、似た履歴がなければ学習済みpredictorで全layerのexpert候補を予測して、CPUからGPUへの先読みを早く始める。 |
| 2025-12 | [OD-MoE: On-Demand Expert Loading for Cacheless Edge-Distributed MoE Inference](2025-2512.03927-od-moe-on-demand-expert-loading-for-cacheless-edge-distributed-moe-inference.md) | ✓ | 0 | 常設expert cacheを持たず、軽量化した別modelで数layer先のexpertを予測し、複数worker GPUへ必要expertだけを実行直前に読み込む。予測が外れた場合はnative routerの正しいexpertを追加ロードする分散edge MoE方式。 |

### 直近12か月より前・リポジトリ内で被引用

該当なし。

### その他

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2025-09 | [LayerScope: Predictive Cross-Layer Scheduling for Efficient Multi-Batch MoE Inference on Legacy Servers](2025-2509.23638-layerscope-predictive-cross-layer-scheduling-for-efficient-multi-batch-moe-infer.md) | ✓ | 0 | layerごとの小型予測器で将来使うexpertを見積もり、CPU→GPU先読み・必要時転送・CPUでのexpert実行を同じ計画で調整して、複数batchがPCIe帯域を奪い合う時の待ち時間を減らす。 |
| 2025-02 | [Fate: Fast Edge Inference of Mixture-of-Experts Models via Cross-Layer Gate](2025-2502.12224-fate-fast-edge-inference-of-mixture-of-experts-models-via-cross-layer-gate.md) | ✓ | 0 | 現在layerのrouter入力から次layerで使うexpertを予測し、浅いlayerには多めのexpertをGPUへ置き、深いlayerは先読みで補う。さらに利用頻度の低いexpertだけを強く量子化してedge環境の転送待ちとmemory使用量を減らす。 |
| 2024-12 | [DAOP: Data-Aware Offloading and Predictive Pre-Calculation for Efficient MoE Inference](2024-2501.10375-daop-data-aware-offloading-and-predictive-pre-calculation-for-efficient-moe-infe.md) | [✓](https://github.com/ecolab-nus/DAOP) | 0 | prefillでそのrequestがよく使うexpertを把握してGPU配置を調整し、decodeでは次layerでCPU側expertが必要かを1 block早く予測してCPU計算を先に始めることで、単一GPUのMoE推論を高速化する。 |
| 2024-10 | [ProMoE: Fast MoE-based LLM Serving using Proactive Caching](2024-2410.22134-promoe-fast-moe-based-llm-serving-using-proactive-caching.md) | [✓](https://github.com/promoe-opensource/promoe) | 0 | CPU DRAMへ退避したMoE expertを、必要になってから読むのではなく数layer先のroutingを軽量predictorで予測してGPUへ先読みする。予測の正しさだけでなく『実際に使う時刻までに何割転送できたか』もGoodPredで評価し、expertを3 chunkへ分けた転送、native gate直後の誤予測中断、GPUに到着済みexpertから先に実行する順序変更を組み合わせてPCIe待ちをcritical pathから外すlossless serving system。 |
| 2023-10 | [SiDA-MoE: Sparsity-Inspired Data-Aware Serving for Efficient and Scalable Large Mixture-of-Experts Models](2023-2310.18859-sida-moe-sparsity-inspired-data-aware-serving-for-efficient-and-scalable-large-m.md) | [✓](https://github.com/timlee0212/SiDA-MoE) | 0 | 小型LSTMで各tokenが使うexpertを先に予測し、予測したexpertだけをCPUからGPUへ読み込む。予測結果そのものをroutingに使うため、外れると元modelと異なるexpertを実行し得る近似方式。 |
| 2023-08 | [Pre-gated MoE: An Algorithm-System Co-Design for Fast and Scalable Mixture-of-Expert Inference](2023-2308.12066-pre-gated-moe-an-algorithm-system-co-design-for-fast-and-scalable-mixture-of-exp.md) | [✓](https://github.com/ranggihwang/Pregated_MoE) | 0 | 次layerのrouting判定を1 block前で行い、必要expertを早めに確定してCPU→GPU転送を現在blockの計算と重ねることで、expert weight待ちを減らすMoE offload方式。 |
<!-- survey:auto:end -->
