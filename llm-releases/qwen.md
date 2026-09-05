# Qwen系 LLMリリース

Qwenファミリーの主要な新規公開・一般提供モデルを、新しいものから順に記録する。

収録対象期間: **2026-03-04〜2026-09-05**

| リリース日 | モデル | 簡単な説明 | 公式リンク |
|---|---|---|---|
| 2026-09-02 | Qwen3.8-Max-0902 | Qwen3.8-Maxの重要snapshot。coding / cowork向けに追加post-trainingされ、複雑なengineering project、long-horizon autonomous development、multi-tool orchestration、chart / document / multimodal understandingを強化。2.4T級MoEを基盤とし、1M context、image / text / video入力、thinking modeとtool ecosystemを維持する。0902自体はAPI提供で、対応するopen-weight checkpointの公開は確認されていない。 | https://www.qwencloud.com/models/qwen3.8-max-0902 |
| 2026-08-26 | Qwen3.8-Flash-Next | Qwen4へ向けた次世代アーキテクチャを先行採用したopen-weightのmultimodal MoE。大規模総パラメータに対しactive parametersを抑え、高速推論と長文脈を狙う。 | https://qwen.ai/blog?id=qwen3.8-flash-next |
| 2026-08-02 | Qwen3.8-Max | Qwen3.8世代の最大級モデル。Max-class weightsのopen化も発表され、Qwen3.8-2.4T-A95Bなどの大規模MoE系へ展開した。 | https://qwen.ai/blog?id=qwen3.8 |
| 2026-04-21 | Qwen3.6-27B | 27B級denseモデルとして公開されたQwen3.6の中規模モデル。ローカル実行も視野に入るサイズ帯。 | https://qwen.ai/blog?id=qwen3.6-27b |
| 2026-04-18 | Qwen3.6-Max-Preview | Qwen3.6世代の最大級APIモデルのpreview。複雑な推論・agent用途を主眼とする。 | https://qwen.ai/blog?id=qwen3.6-max-preview |
| 2026-04-15 | Qwen3.6-35B-A3B | 総35B・active約3Bのopen-weight MoE。比較的小さいactive parametersで高い推論効率を狙う。 | https://qwen.ai/blog?id=qwen3.6-35b-a3b |

重要なopen-weight MoEについては、公開情報がある範囲で総パラメータ数、active parameters、expert数、top-k routing、context length、Vision対応、ライセンス、Hugging Face / ModelScope / API、主要runtime対応状況、量子化時のメモリ目安も記録する。

公式open-weight collection: https://huggingface.co/collections/Qwen/qwen38
