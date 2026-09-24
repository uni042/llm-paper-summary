# Gemma系 LLMリリース

Google Gemmaファミリーの主要リリースを新しい順に記録する。初回バックフィル対象期間: **2026-03-04〜2026-09-04**。

Gemmaは重み公開（open-weight）モデル群なので、API専用modelとは異なり自前hardwareへdownloadして実行できる。dense modelとMoE modelが混在するため、model名のparameter表記が何を意味するかを分けて読む。

| リリース日 | モデル | 簡単な説明 | 公式リンク |
|---|---|---|---|
| 2026-06-03 | Gemma 4 12B Unified | Gemma 4世代の12B級Unifiedモデル。複数用途・入力形式を1つのmodel familyへまとめる後続releaseとして追加。12B級は大規模MoEより総weight量が小さく、量子化すればローカルGPU / unified-memory machineでも比較的扱いやすいサイズ帯。 | https://ai.google.dev/gemma/docs/releases |
| 2026-04-16 | Gemma 4 MTP | E2B、E4B、31B、26B-A4B向けにMTP（Multi-Token Prediction; 複数token予測）headを持つvariantを追加。通常の次1 token予測に加えて複数token先の候補を作り、対応runtimeでは投機的デコードへ利用できる。 | https://ai.google.dev/gemma/docs/releases |
| 2026-03-31 | Gemma 4 | E2B、E4B、31B、26B-A4Bを含むGemma 4世代。毎tokenほぼ全weightを使うdense modelと、一部expertだけを使うMoEを同じfamilyに含むopen-weightリリース。 | https://ai.google.dev/gemma/docs/releases |

## モデル名の読み方

- **12B / 31B**: おおむねmodel全体のparameter規模を示すdense系表記。
- **26B-A4B**: 総parameterは約26Bだが、MoE routingによって1 tokenあたり約4B相当をactiveにする構成を示す表記。
- **E2B / E4B**: Gemma family内のexpert構成・規模を表す名称。具体的なtotal / active parameterは各model cardの記載を優先する。

## 用語メモ

- **MTP（Multi-Token Prediction; 複数token予測）**: 1回のforwardで次tokenだけでなく、その先の複数位置の候補も予測する仕組み。対応runtimeではdraft生成へ利用してdecodeを高速化できる。
- **dense model（密model）**: 基本的に各tokenで同じ主要FFN weight全体を使うmodel。
- **MoE（Mixture of Experts; エキスパート混合）**: 多数expertのうちtokenごとに一部だけを選んで実行するmodel。
- **Unified**: 複数用途・modal・機能を別modelへ分けず、1つのmodel / architectureへ統合する位置づけを示す名称として使われる。
