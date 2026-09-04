# Hugging Face Transformers

Hugging Face Transformersの主要な機能・性能更新を継続的に記録する集約ページです。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

- **2026-07-15 — v5.14.0（released）**: StaticCache利用時のSDPA prefillをFlashAttention kernelへdispatch。Llama 3.1 8B／8,192-token入力で0.735→0.280秒、512-tokenでは約10%改善。[PR #47094](https://github.com/huggingface/transformers/pull/47094)
- **2026-08-10 — v5.15.0（released）**: target／draft分布を混合して受理率を高めるtraining-freeのstatic ensemble speculative decodingを追加。PRが引用する評価では受理率約65→78%、ROUGE-L低下0.5 point以内。Transformers独自benchmarkではない。[PR #45979](https://github.com/huggingface/transformers/pull/45979)

v5.16.0のcache関連は修正・変更取り消しが中心のため除外した。
