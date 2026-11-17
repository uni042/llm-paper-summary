# Recursive Flint

Recursive Flint 40B-A2.5Bは、Recursiveが公開するコード作成と段階的なtool利用を想定したopen-weightモデルである。

## 構成

- **公開確認**: 2026-10-21 UTC。Ollama v0.40.8の正式リリースで配布対応が確認できる。公式モデルカードはApache-2.0ライセンスとBF16 checkpoint、SGLangでの配信手順を案内する。
- **規模**: 総39.8B、tokenごとの有効約2.5BのMoE Transformer。49層（dense 2層、MoE 47層）で、各MoE層は256専門家から6つと共有専門家を選ぶ。
- **注意機構**: 35層は512履歴tokenのsliding-window attention、14層はfull attention。設定上の最大contextは262,144 token。
- **開発者報告の評価**: Terminal-Bench 2.1で54.9%、SWE-bench Verifiedで74.2%。実行環境と評価手順に依存する値として扱う。

## 配布と実行上の制約

公式のBF16 checkpointは約80GB。公式SGLang手順の例は単一B300またはH200であり、Ollama v0.40.8のFlint対応はmacOS限定と案内される。Windows 11 / RTX 4070 SUPER 12GBでの正式なOllama対応や実行性能、12GB内に収まる量子化配布物は確認できていない。これらの記載は、一般的なconsumer GPUで動作することを意味しない。

## Ripple-65B Preview（2026-11-04）

同じRicursive Intelligence（旧表記Recursive）から、同社初の汎用公開モデルとしてRipple-65B Previewが公開された。

- **規模・構造**: 65B dense Transformer（80層、d_model 5,120）。MoEではなくdenseで、12T tokensで事前学習。最大contextは1,048,576 tokensと案内される。
- **ライセンス・配布**: Apache-2.0。BF16 instruct checkpoint（約129.6GB）とNVFP4版（実験的、約57.2GB、単体DGX Spark向けスクリプト同梱）、投機的デコード用DFlash2 draft（4.04B）をHugging Faceで公開。hosted提供はTogether AI、GMI Cloud、OpenRouter、Fireworks（$0.20 / $0.60、各100万token）。
- **開発者報告の評価**: Terminal-Bench 2.1で80.52（著者報告値。実行環境と評価手順に依存し、独立検証ではない）。65B denseでもBF16で約130GB級のcheckpointであり、consumer GPU単体での実行を意味しない。
- 一次資料: [Ricursive公式発表](https://www.ricursive.com/ripple) / [Ripple-65B-Preview model card](https://huggingface.co/ricursiveAI/Ripple-65B-Preview)

## 一次資料

- [Recursive Flint model card](https://huggingface.co/RecursiveSI/flint)
- [Ollama v0.40.8 release](https://github.com/ollama/ollama/releases/tag/v0.40.8)
