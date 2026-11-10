# Liquid AI LFM3 / d1

Liquid AIが2026-10-27に公開した、用途別のopen-weight LFM3 familyをまとめる。公式発表は6つの派生モデルを示し、共通基盤のLFM3-1.7B-Baseを加えると少なくとも7系統のcheckpointがある。

| 公開日 | モデル | 主な用途・仕様 | 提供形態・注意 |
|---|---|---|---|
| 2026-10-27 | LFM3-1.7B-Base | 共通基盤となるtext model | open-weight。各checkpointの配布形式を個別確認 |
| 2026-10-27 | LFM3-1.7B | text・tool use・構造化出力。1.73B parameters、24 layers、128K語彙、事前学習22T tokens | LFM Open License v1.0。4bit版のweight footprintは約1GBとの公式説明 |
| 2026-10-27 | LFM3-VL-2B | 画像・動画対応 | モダリティと実行対応をcheckpointごとに確認 |
| 2026-10-27 | LFM3-Audio-2B | 音声用途 | checkpoint固有の音声入出力条件を確認 |
| 2026-10-27 | LFM3-Omni-2B | 音声・画像・動画を統合 | 配布形式とruntime対応はvariantごとに確認 |
| 2026-10-27 | d1-2B | 判断・agent用途 | Ollama v0.40.12はこのreleaseでApple hardware対応と案内 |
| 2026-10-27 | d1-omni-2B | 音声付き判断・agent用途 | モダリティ別のruntime対応を確認 |

## LFM3-1.7Bの構造

text版は13層のgated short convolution、5層のsliding-window attention（window 256 tokens）、6層のglobal attentionを組み合わせるtri-hybrid architecture。model全体のcontext lengthは256K tokensで、SWAの256-token windowとは別の値である。最大contextでの実行可能性や必要RAM/VRAMはKV cacheとruntime設定に依存する。

公式のLFM Open License v1.0を適用する。Apache-2.0やMITと読み替えない。4bit text checkpointの約1GBはweight footprintであり、長contextを動かすための総メモリ量ではない。

## 評価と実行互換性

Liquid AIはWebArena-Verifiedで38.42を報告し、比較としてLFM2.5-2.6Bの3.02を示す。著者評価はbenchmark構成・agent harnessに依存し、独立再現や全タスクでの優位を意味しない。Q4_0 GGUFを用いた著者のedge比較はRyzen AI Max+ 395、Apple M5 Max、iPhone 17 Proで行われたもので、RTX 4070 SUPERの性能へ外挿できない。

公式model cardはTransformers利用を案内する。GGUFはLFM3対応のllama.cpp buildが必要。FP8のSGLang対応は確認時点でPR審査中であり、現行stable release全般で使えるとは限らない。Ollama v0.40.12はLFM3およびd1 2BのApple hardware対応を告知し、Linux/Windows対応は今後としている。

## 一次資料

- [Liquid AI公式発表](https://www.liquid.ai/blog/lfm3)
- [Liquid AI Hugging Face記事](https://huggingface.co/blog/LiquidAI/lfm3)
- [LFM3-1.7B model card](https://huggingface.co/LiquidAI/LFM3-1.7B)
- [LFM3-1.7B-Base model card](https://huggingface.co/LiquidAI/LFM3-1.7B-Base)
- [LFM3 GGUF model card](https://huggingface.co/LiquidAI/LFM3-1.7B-GGUF)
- [LFM3 FP8 model card](https://huggingface.co/LiquidAI/LFM3-1.7B-FP8)
