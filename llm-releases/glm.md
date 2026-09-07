# GLM系 LLMリリース

Z.AI / Zhipu AIのGLMファミリー主要リリースを新しい順に記録する。初回バックフィル対象期間: **2026-03-04〜2026-09-04**。

GLM系では長文脈・agent用途の説明に加え、MoEモデルでは**総パラメータ数（total parameters）と有効パラメータ数（active parameters）**を分けて記録する。

| リリース日 | モデル | 簡単な説明 | 公式リンク |
|---|---|---|---|
| 2026-08-26 | GLM-5.3-Flash | GLM-5系初のnative multimodal Flashモデル。総約320B / tokenあたり約18B activeのMoE。通常attentionだけでなくsparse / linear attentionを組み合わせ、長contextで全過去tokenへ毎回dense attentionするcostとKV cache増加を抑える設計。 | https://autoclaw.z.ai/blog/model/glm-5.3-flash/ |
| 2026-08 | GLM-5.3 | 大規模software engineering、large codebase、長時間エージェント処理（long-horizon agentic work）向けのflagship更新。複数file・tool・stepをまたぐtaskを主用途として記録。 | https://autoclaw.z.ai/models/ |
| 2026-06 | GLM-5.2 | 最大1M-token contextを備え、大規模project、長文document、複数stageのdevelopment taskを重視したflagship更新。長contextは入力可能量を示す値であり、実際のmemory / latencyは利用するruntimeやcache方式にも依存する。 | https://autoclaw.z.ai/models/ |
| 2026-04-07 | GLM-5.1 | 長時間taskで、計画（planning）→実行（execution）→結果を見た修正（iterative refinement）を繰り返す能力を重点強化したGLM-5世代更新。 | https://docs.z.ai/release-notes/new-released |
| 2026-03-15 | GLM-5-Turbo | 多数stepを伴うagent workflowを高throughputで処理することを重視したTurbo系列。最高性能だけでなく、latency・cost・安定した連続実行とのbalanceを取る位置づけ。 | https://docs.z.ai/release-notes/new-released |

## 用語メモ

- **native multimodal**: 後付けの別vision modelだけに頼らず、model architecture / training段階からtextとimage等の複数modalを統合して扱うこと。
- **sparse attention（疎attention）**: 過去tokenすべてではなく重要な一部だけへattentionし、長文時の計算量を削減する方式。
- **linear attention（線形attention）**: 標準attentionの二次的に増えやすい計算を避け、sequence lengthに対してより緩やかに増えるstate /計算へ変換する方式群。
- **Flash / Turbo**: 一般にflagship最大性能より、latency・throughput・cost efficiencyを重視する系列名として使われる。
