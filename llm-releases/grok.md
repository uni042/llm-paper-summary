# Grok系 LLMリリース

xAI / SpaceXAI Grokファミリーの主要リリースを新しい順に記録する。初回バックフィル対象期間: **2026-03-04〜2026-09-04**。

Grok系では、単純な「最新flagship」という表現だけでなく、**長時間agent、coding、visual / interactive task、最大文脈長（context length）**のどこが更新されたかを記録する。

| リリース日 | モデル | 簡単な説明 | 公式リンク |
|---|---|---|---|
| 2026-08-12 | Grok 4.6 | 長時間動くエージェント（long-running agents）、coding、visual / interactive workを重点強化した上位モデル。最大500K-token contextを持ち、単発chatより複数stepのtool利用・長い作業履歴を扱う用途を重視。 | https://x.ai/news/grok-4-6 |
| 2026-07-16 | Grok 4.5 | coding、エージェント型タスク（agentic tasks）、knowledge workを中心に更新したGrok 4系モデル。code生成だけでなくtool利用や複数step executionを含むtaskを重点対象とする。 | https://x.ai/news/grok-4-5 |

## 用語メモ

- **flagship model（最上位モデル）**: model family内で最大能力を重視する上位系列。通常、低cost / low-latency系列とは別の位置づけ。
- **長時間エージェント（long-running agent）**: browser、terminal、file等のtoolを多数step使い、途中結果から計画を修正しながら長くtaskを継続するsystem。
- **500K-token context**: 1 requestで最大約50万tokenの入力・履歴を参照できる仕様。実際のlatency・cost・memory使用量は入力長に応じて増える。
- **interactive / visual work（対話的・視覚作業）**: imageやUI等を見ながら、操作と確認を繰り返すtask。

API提供範囲、料金、具体的なtool接続、weight公開の有無はmodel能力とは別項目なので、必要に応じて個別に追記する。
