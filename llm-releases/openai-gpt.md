# OpenAI GPT系 LLMリリース

OpenAI GPT系の主要モデルを新しい順に記録する。初回バックフィル対象期間: **2026-03-04〜2026-09-04**。

このページでは、model名だけでなく、**APIでのmodel ID、主な用途、最大文脈長（context length）、出力上限、一般用途か高計算量用途か**を公開情報の範囲で記録する。

| リリース日 | モデル | 簡単な説明 | 公式リンク |
|---|---|---|---|
| 2026-09-03 | GPT-6 Astra | GPT-6世代の上位モデルとして、computer use、browser操作、software engineering、cybersecurity、science、professional workなどtoolを伴う長いtaskを重点強化。API model IDは`gpt-6-astra`。最大1,050,000-token context、最大128,000-token outputとして記録。 | https://openai.com/index/gpt-6-astra/ |
| 2026-07-09 | GPT-5.6 Sol / Terra / Luna | GPT-5.6世代のmodel群。Solは高能力側、Terraは性能・latency・costのbalance、Lunaは高速・低cost側という役割分担で、coding、knowledge work、science、エージェント型処理（agentic work）を対象とする。 | https://openai.com/index/gpt-5-6/ |
| 2026-04-23 | GPT-5.5 / GPT-5.5 Pro | 複雑な実務、agentic coding、online research、文書・spreadsheet作成、tool useを重点にした世代。Proはより多い計算量を使う高難度task向けvariantとして区別する。API提供は4月24日開始として記録。 | https://openai.com/index/introducing-gpt-5-5/ |

## 読み方

- **API model ID**: applicationからAPIを呼ぶ際に指定する識別子。ChatGPT上の表示名やproduct内のmode名と完全に一致するとは限らない。
- **文脈長（context length）**: 1 requestでmodelが参照できる入力・履歴のtoken量。大きいほど長文を扱えるが、実際のlatency・costは入力長に応じて増える。
- **最大出力（max output）**: 1 responseで生成できるtoken数の上限。context length全体とは別の制約。
- **エージェント型処理（agentic work）**: browser、terminal、file、外部API等を複数step使い、途中結果を見ながら計画を更新するtask。
- **Pro variant**: 通常variantより多い推論計算を許容する代わりに、latencyや利用costが大きくなる高難度task向けmodel / modeを指す場合がある。

OpenAIのChatGPT product上のmodel名称・利用上限と、APIのmodel ID・料金・context仕様は別々に変更されることがあるため、この一覧では可能な限りAPI / model releaseとしての情報を記録する。
