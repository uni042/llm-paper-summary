# Claude系 LLMリリース

Anthropic Claudeファミリーの主要リリースを新しい順に記録する。初回バックフィル対象期間: **2026-03-04〜2026-09-04**。

Claude系はmodel名だけでは用途差が分かりにくいため、このページでは**どの程度長いtaskを想定するか、coding・専門知識・研究など何へ重点を置くか**を中心に記述する。

| リリース日 | モデル | 簡単な説明 | 公式リンク |
|---|---|---|---|
| 2026-09-01 | Claude Fable 5.1 / Claude Mythos 5.1 | 5.1世代の上位モデル群。coding、knowledge work、科学研究など長いmulti-step taskを重点更新。Mythos 5.1は特にcybersecurity / biologyなど専門領域を重視する位置づけ。 | https://www.anthropic.com/news |
| 2026-07-24 | Claude Opus 5 | 長時間動くエージェント（long-running agents）、software development、専門的なknowledge workを主対象とするOpus系上位モデル。単発回答より、複数file・tool・stepをまたぐ仕事を想定する。 | https://www.anthropic.com/news/claude-opus-5 |
| 2026-06-30 | Claude Sonnet 5 | planning、browser / terminal tool use、長時間の自律実行を強化したSonnet系。Opusよりcost / latencyとのbalanceを取りながら、codingやtool-based workflowへ使う位置づけ。 | https://www.anthropic.com/news/claude-sonnet-5 |
| 2026-06-09 | Claude Fable 5 / Claude Mythos 5 | Anthropicの上位研究・専門用途モデル群。Fableは幅広い高度業務、Mythosはcybersecurity / biologyなど一部専門領域を重点対象とする。一般的な高速モデル系列とは用途を分けて見る必要がある。 | https://www.anthropic.com/system-cards |

## 用語メモ

- **長時間エージェント（long-running agent）**: 1回のpromptだけで終わらず、file編集、terminal、browser、外部toolなどを使いながら多数stepを継続する処理。
- **knowledge work（知識労働）**: 調査、分析、文書作成、企画、software設計など、情報を統合して成果物を作る業務。
- **system card（システムカード）**: modelの能力評価、安全性評価、制約、提供条件などをmodel提供者が整理した技術資料。

model family内の優劣は単純なbenchmark順位だけで決めず、API cost、latency、tool対応、提供範囲なども分けて記録する。
