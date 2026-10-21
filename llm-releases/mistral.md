# Mistral系 LLMリリース

Mistral AIの主要な汎用・coding向けLLMを新しい順に記録する。初回バックフィル対象期間: **2026-03-04〜2026-09-04**。

Mistral系はAPI提供だけでなく重み公開（open-weight）も多いため、**context length、multimodal対応、license、ローカル実行可能性**を分けて記録する。

| リリース日 | モデル | 簡単な説明 | 公式リンク |
|---|---|---|---|
| 2026-10-20 | Voxtral 3 音声モデル群 | Small / Mini Transcribe 3（Miniは4B）、Realtime Transcribe 3、Speech / Mini TTS 3とvoice-agent SDK。Transcribeは50以上の言語、話者分離、文脈語彙補正に対応。Realtimeは公式発表で35言語以上・500ms未満を掲げる一方、モデル資料の設定範囲は80〜2400msで、固定遅延ではない。API公開previewと導入相談が案内されるが、一般配布weight・licenseは未確認。音声認識/合成の系列であり汎用text LLMではない。 | [発表](https://mistral.ai/news/voxtral-3/) · [Small Transcribe](https://docs.mistral.ai/models/voxtral-small-transcribe-3-0) · [Mini Transcribe](https://docs.mistral.ai/models/voxtral-mini-transcribe-3-0) · [Realtime](https://docs.mistral.ai/models/voxtral-mini-transcribe-realtime-3-0) · [Mini TTS](https://docs.mistral.ai/models/voxtral-mini-tts-3-0) |
| 2026-10-06 | Mistral Large 4 | 約1.05T total / 52B activeのnative multimodal flagship（2026-10-12公式情報再照合）。APIのpublic previewが利用可能で、model weightsは10月末公開予定のためopen-weight配布済みとは扱わない。coding、agentic workflows、multimodal understandingを重点化。 | https://mistral.ai/news/mistral-large-4/ |
| 2026-04-28 | Mistral Medium 3.5 | codingやtool利用を伴うエージェント用途（agentic use）を重視したmultimodalモデル。最大256K-token contextを持ち、weightも公開されるためAPIだけでなく自前環境での実行対象にできる。 | https://docs.mistral.ai/models/mistral-medium-3-5-26-04 |
| 2026-03-16 | Mistral Small 4 | 通常指示応答（instruct）、推論（reasoning）、multimodal理解、agentic codingを1 modelへ統合した小型側モデル。Apache 2.0 licenseのopen modelとして公開され、再配布・改変条件が比較的明確。 | https://mistral.ai/news/mistral-small-4/ |

## 用語メモ

- **重み公開（open-weight）**: model weightをdownloadできる提供形態。license条件はmodelごとに別途確認する。
- **Apache 2.0**: commercial use、改変、再配布を広く認める代表的なpermissive software license。model weightへ適用される場合も、付随条件やmodel cardを併せて確認する。
- **256K-token context**: 最大約26万tokenを1 requestの文脈として扱える仕様。長context時のKV cache memoryや実速度はruntime・hardwareに依存する。
- **エージェント型coding（agentic coding）**: code生成だけでなく、repository探索、file編集、test実行、error確認、修正を複数step繰り返すsoftware development task。

「frontier-class」のような比較的曖昧な宣伝表現だけで性能を判断せず、必要に応じて個別benchmark・license・runtime対応を別途確認する。
