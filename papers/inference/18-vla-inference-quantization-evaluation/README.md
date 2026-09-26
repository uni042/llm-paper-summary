# Pipeline-Native CPU Inference

CPU向け単一トークン推論で、Transformerの層間依存構造、重み配置、実行スケジュールを共同設計する研究を収録する。標準モデルのまま行う量子化やカーネル高速化とは異なり、推論時のデータ移動順序を変えるためにモデル構造そのものを設計する研究を扱う。

## 収録論文

- [Pipeline-Native Transformers: Co-Designing Model Architecture and CPU Inference for Bandwidth-Efficient Autoregressive Decode](2026-2608.23841-pipeline-native-transformers.md) — 層間依存を緩めたモデルとCPUタイル型ストリーミングランタイムを共同設計する。
