# Mistral系 LLMリリース

Mistral AIの主要な汎用・coding向けLLMを新しい順に記録する。初回バックフィル対象期間: **2026-03-04〜2026-09-04**。

Mistral系はAPI提供だけでなく重み公開（open-weight）も多いため、**context length、multimodal対応、license、ローカル実行可能性**を分けて記録する。

| リリース日 | モデル | 簡単な説明 | 公式リンク |
|---|---|---|---|
| 2026-04-28 | Mistral Medium 3.5 | codingやtool利用を伴うエージェント用途（agentic use）を重視したmultimodalモデル。最大256K-token contextを持ち、weightも公開されるためAPIだけでなく自前環境での実行対象にできる。 | https://docs.mistral.ai/models/mistral-medium-3-5-26-04 |
| 2026-03-16 | Mistral Small 4 | 通常指示応答（instruct）、推論（reasoning）、multimodal理解、agentic codingを1 modelへ統合した小型側モデル。Apache 2.0 licenseのopen modelとして公開され、再配布・改変条件が比較的明確。 | https://mistral.ai/news/mistral-small-4/ |

## 用語メモ

- **重み公開（open-weight）**: model weightをdownloadできる提供形態。license条件はmodelごとに別途確認する。
- **Apache 2.0**: commercial use、改変、再配布を広く認める代表的なpermissive software license。model weightへ適用される場合も、付随条件やmodel cardを併せて確認する。
- **256K-token context**: 最大約26万tokenを1 requestの文脈として扱える仕様。長context時のKV cache memoryや実速度はruntime・hardwareに依存する。
- **エージェント型coding（agentic coding）**: code生成だけでなく、repository探索、file編集、test実行、error確認、修正を複数step繰り返すsoftware development task。

「frontier-class」のような比較的曖昧な宣伝表現だけで性能を判断せず、必要に応じて個別benchmark・license・runtime対応を別途確認する。
