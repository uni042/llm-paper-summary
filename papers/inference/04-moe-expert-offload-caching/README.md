<!-- survey:auto:start -->
## 自動生成の論文一覧（1本）

| 論文 | 一文要約 |
|---|---|
| [Moebius: Serving Mixture-of-Expert Models with Seamless Runtime Parallelism Switch](2026-2606.26607-moebius-runtime-parallelism-switch.md) | MoE推論では低い同時実行数ではテンソル並列が低遅延、高い同時実行数ではエキスパート並列が高スループットになるため、バースト型オンライン要求や強化学習ロールアウトでは一つの実行中に最適構成が入れ替わる。Moebiusはモデルを再起動せず、実行中要求を落とさずに両構成を切り替える。固定アドレスの統一GPUメモリ、エキスパート重みとページ化KVを宛先へ直接書く融合転送カーネル、両構成のCUDAグラフ・通信状態常駐を組み合わせ、8×H200上のQwen3-235B-A22Bで切替215〜434ms、追加メモリ2.4%、強化学習ロールアウト1.16〜1.25倍高速化を示す。 |
<!-- survey:auto:end -->
