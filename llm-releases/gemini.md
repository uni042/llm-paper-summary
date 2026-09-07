# Gemini系 LLMリリース

Google Geminiファミリーの主要リリースを新しい順に記録する。初回バックフィル対象期間: **2026-03-04〜2026-09-05**。

このページでは、単に「性能強化」と書くのではなく、**どの入力形式を扱えるか、最大文脈長（context length）、一般API提供か限定提供か、主な用途が何か**を優先して記述する。

| リリース日 | モデル | 簡単な説明 | 公式リンク |
|---|---|---|---|
| 2026-09-02 | Gemini 3.8 Flash | software engineering、エージェント型タスク（agentic tasks）、複数段階推論を3.7 Flashから強化した高速・汎用モデル。text / image / audio / video入力に対応し、最大1M-token入力文脈と64K-token出力を持つ。Gemini API等で一般利用できるproduction向けモデル。 | https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/ |
| 2026-09-02 | Gemini 3.8 Flash Cyber | Gemini 3.8 Flash系の基盤能力を、脆弱性探索（vulnerability discovery）や自動patch作成などcybersecurity用途へ調整した限定提供モデル。一般用途モデルではなく、Fairwind Program経由のtrusted defender向け提供として区別する。 | https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/ |
| 2026-08-13 | Gemini 3.7 Flash | codingとtoolを組み合わせるエージェント型workflowを中心に3.6 Flashから更新したFlash系モデル。Flash系は最大性能だけでなく、latency・cost・throughputとのbalanceを重視する位置づけ。 | https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/ |
| 2026-07-21 | Gemini 3.6 Flash | coding、knowledge work、multimodal処理とtoken効率を改善した汎用Flashモデル。大量requestを低latencyで処理するworkhorse用途を想定する。 | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/ |
| 2026-07-21 | Gemini 3.5 Flash-Lite | 3.5世代の低latency・低cost側モデル。高価な上位modelを毎request使わずに済むよう、分類・抽出・軽量tool利用など大量処理向けの位置づけ。 | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/ |
| 2026-05-19 | Gemini 3.5 Flash | Gemini 3.5世代のFlashモデル。推論だけでなくtool executionを含むエージェント型処理を統合した世代として公開。 | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/ |
| 2026-05-19 | Gemini Omni Flash | text・image・audio・videoを同じmodel familyで扱うmultimodalモデル。単に複数形式を入力できるだけでなく、異なるmodalをまたいだ理解・生成を狙うGemini Omni系の第一弾。 | https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/ |

## 用語メモ

- **Flash**: Gemini系で、最高性能だけでなくlatency・throughput・API costを重視する高速モデル系列。
- **Flash-Lite**: Flashよりさらに低cost・高throughput側へ寄せた系列。
- **マルチモーダル（multimodal）**: text以外にimage、audio、video等を同じmodelへ入力し、複数形式を横断して処理できること。
- **エージェント型タスク（agentic tasks）**: 1回回答して終わるのではなく、計画、tool呼び出し、結果確認、再試行を複数stepにわたって行うtask。
- **一般提供（general availability / production-ready）** と **限定提供**: API利用者全般が使えるmodelと、特定program・審査対象だけが使えるmodelを区別する。
