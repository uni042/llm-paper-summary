# TGI

Text Generation Inference（TGI）の主要な機能・性能更新を継続的に記録する集約ページ。TGIはHugging Faceが提供していたLLM serving engineで、continuous batching、tensor parallelism、quantization、token streamingなどを統合していた。

## 初期収録期間

2026-06-03〜2026-09-03

## 掲載対象となる更新なし

公式repositoryは **2026-03-21にarchive済み**で、対象期間内に新しいreleaseや本質的なruntime改善は確認できなかった。

そのため、このrepositoryではTGIを「現在も活発に機能追加されるframework」としては扱わず、**既存研究・既存serving stackを読む際の歴史的な参照先**として残す。

archiveは既存binaryや過去releaseが即座に使えなくなることを意味しないが、新しいmodel architectureやCUDA / hardware世代への継続対応は原則期待しにくい。

- [TGI releases](https://github.com/huggingface/text-generation-inference/releases)
