# Phi系 LLMリリース

Microsoft Phiファミリーの主要リリースを新しい順に記録する。初回バックフィル対象期間: **2026-03-04〜2026-09-04**。

Phi系は比較的小さいparameter規模でreasoningや端末・ローカル利用を狙うmodelが多いため、**parameter数、重み公開（open-weight）、multimodal対応、重点task**を中心に記録する。

| リリース日 | モデル | 簡単な説明 | 公式リンク |
|---|---|---|---|
| 2026-03-04 | Phi-4-reasoning-vision-15B | 約15B parameterの重み公開（open-weight）multimodal reasoning model。math / science reasoning、UIやscreenの視覚理解、imageとtextを組み合わせるvision-language taskを重点対象とする。巨大frontier modelより小さいため、量子化や対応runtimeを使えばローカル実行を検討しやすい規模。 | https://www.microsoft.com/en-us/research/blog/phi-4-reasoning-vision-and-the-lessons-of-training-a-multimodal-reasoning-model/ |

## 用語メモ

- **15B parameters**: 約150億parameter規模。実際のmodel file / VRAM量はBF16、FP8、INT4など保存precisionで大きく変わる。
- **multimodal reasoning（マルチモーダル推論）**: image中の文字・図・UI等を読み取り、text情報と組み合わせて複数stepの推論を行うこと。
- **vision-language task（視覚言語task）**: image説明、OCR後の推論、chart / diagram理解、screen UI理解など視覚とtextをまたぐtask。
- **重み公開（open-weight）**: model weightをdownloadして自前環境で実行できる提供形態。

ローカル用途ではparameter数だけでなく、vision encoderを含む実model容量、KV cache、画像入力時のmemory peakも確認する。
