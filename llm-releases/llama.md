# Llama系 LLMリリース

Meta Llamaファミリーの主要な重み公開（open-weight）モデルを記録する。

> **2026-03-04〜2026-09-04の直近半年には新しいLlama本体の主要リリースを確認できなかったため、系統を一覧から消さない目的で、その時点の最新主要リリース1件のみ掲載する。**

| リリース日 | モデル | 簡単な説明 | 公式リンク |
|---|---|---|---|
| 2025-04-05 | Llama 4 Scout / Llama 4 Maverick | MetaのLlama本体として初めてnative multimodalとMoE（Mixture of Experts; エキスパート混合）を採用した世代。Scoutは約17B active / 16 experts、最大10M-token context、Maverickは約17B active / 128 experts。weightをdownloadできるopen-weight提供。 | https://ai.meta.com/blog/llama-4-multimodal-intelligence/ |

## モデル構造の読み方

- **約17B active**: 1 tokenのforwardで主に実行されるparameter規模。model全体の総parameter数とは別。
- **16 / 128 experts**: MoE layerが持つexpert総数。各tokenで全expertを同時実行するわけではなく、routerが一部を選択する。
- **10M-token context**: 1 requestで参照可能な非常に長いtoken履歴の上限。実際に長contextを使うにはKV cache容量・runtime対応・hardware memoryも必要。
- **native multimodal**: textとimage等をarchitecture / training段階から統合して扱う設計。
- **重み公開（open-weight）**: model weightを自前環境へdownloadできる提供形態。training dataや全sourceの公開を意味する「open source」とは区別する。

MoE modelのローカル実行ではactive parameterだけでなく、**全expert weightを保持するRAM / VRAM / storage容量**も別に確認する必要がある。
