# Recursive Flint

Recursive Flint 40B-A2.5Bは、Recursiveが公開するコード作成と段階的なtool利用を想定したopen-weightモデルである。

## 構成

- **公開確認**: 2026-10-21 UTC。Ollama v0.40.8の正式リリースで配布対応が確認できる。公式モデルカードはApache-2.0ライセンスとBF16 checkpoint、SGLangでの配信手順を案内する。
- **規模**: 総39.8B、tokenごとの有効約2.5BのMoE Transformer。49層（dense 2層、MoE 47層）で、各MoE層は256専門家から6つと共有専門家を選ぶ。
- **注意機構**: 35層は512履歴tokenのsliding-window attention、14層はfull attention。設定上の最大contextは262,144 token。
- **開発者報告の評価**: Terminal-Bench 2.1で54.9%、SWE-bench Verifiedで74.2%。実行環境と評価手順に依存する値として扱う。

## 配布と実行上の制約

公式のBF16 checkpointは約80GB。公式SGLang手順の例は単一B300またはH200であり、Ollama v0.40.8のFlint対応はmacOS限定と案内される。Windows 11 / RTX 4070 SUPER 12GBでの正式なOllama対応や実行性能、12GB内に収まる量子化配布物は確認できていない。これらの記載は、一般的なconsumer GPUで動作することを意味しない。

## 一次資料

- [Recursive Flint model card](https://huggingface.co/RecursiveSI/flint)
- [Ollama v0.40.8 release](https://github.com/ollama/ollama/releases/tag/v0.40.8)
