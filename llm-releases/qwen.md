# Qwen系 LLMリリース

Qwenファミリーの主要な新規公開・一般提供モデルを、新しいものから順に記録する。

収録対象期間: **2026-03-04〜2026-09-08**

このページでは、API専用モデルと重み公開モデル（open-weight）を区別する。MoEでは総パラメータ数だけを見ると実行costを誤解しやすいため、公開されている場合は**1 tokenで実際に使う有効パラメータ数（active parameters）**も併記する。

| リリース日 | モデル | 簡単な説明 | 公式リンク |
|---|---|---|---|
| 2026-09-02 | Qwen3.8-Max-0902 | Qwen3.8-Maxの更新snapshot。software開発、長時間tool実行、複数toolをまたぐ処理、chart / document / image / video理解を強化したAPIモデル。基盤は2.4T級MoEで、最大1M-token contextとmultimodal入力を維持する。**0902 snapshot自体のopen-weight checkpointは確認されておらず、ローカル実行用weightの公開とは別扱い。** | https://www.qwencloud.com/models/qwen3.8-max-0902 |
| 2026-08-26 | Qwen3.8-Flash-Next | Qwen4へ向けた次世代architectureを先行採用したopen-weight multimodal MoE。非常に大きい総parameterを持ちながら、各tokenで選択するexpertを絞ってactive parametersを小さくし、dense modelより計算量を抑える設計。長contextとtext / visual入力を対象とする。 | https://qwen.ai/blog?id=qwen3.8-flash-next |
| 2026-08-02 | Qwen3.8-Max | Qwen3.8世代の最大級モデル。Max-classのweight公開も発表され、Qwen3.8-2.4T-A95Bなど大規模MoEへ展開。`2.4T-A95B`のような表記では、前半が総parameter規模、`A95B`がtokenあたり約95Bを有効化する構成を表す。 | https://qwen.ai/blog?id=qwen3.8 |
| 2026-04-21 | Qwen3.6-27B | 約27B parameterを毎token使用するdense model。MoEのように一部expertだけを選ぶ構造ではないため、同程度の総parameterを持つMoEより1 tokenあたりの演算量は大きくなりやすい一方、実行構造は単純。量子化すれば単一workstationでのローカル利用も検討できるサイズ帯。 | https://qwen.ai/blog?id=qwen3.6-27b |
| 2026-04-18 | Qwen3.6-Max-Preview | Qwen3.6世代の最大級APIモデルのpreview。複雑な推論、tool利用、長いmulti-step taskを主対象とする。preview提供であり、open-weight modelとは区別する。 | https://qwen.ai/blog?id=qwen3.6-max-preview |
| 2026-04-15 | Qwen3.6-35B-A3B | 総約35Bのweightを持つ一方、1 tokenでは約3B相当のexpertだけを使うopen-weight MoE。model file自体は35B級の保存容量を必要とするが、tokenごとの主なexpert演算量は約3B級まで抑える設計。 | https://qwen.ai/blog?id=qwen3.6-35b-a3b |

## Qwen3.8-Flash-Next 詳細

Qwen公式の2026-08-26公開版を2026-09-08に再確認した。**重み公開（open-weight）**のマルチモーダル混合エキスパート（Mixture of Experts; MoE）で、主モデル125Bに51BのN-gram embeddingを加え、1 tokenあたりの有効パラメータは6B。Gated DeltaNetとQwen Sparse Attentionを組み合わせ、長い履歴の全位置へ常に同じ計算をかけるのではなく、圧縮状態と重要部分の選択を使って長文脈のattention費用を抑える。

N-gram embeddingはhost memoryへ退避し、非同期先読み（asynchronous prefetch）でmodel計算と重ねられる設計。公式配布先はHugging FaceとModelScope。公式READMEではTransformers、llama.cpp（text / vision）、SGLang、vLLMでの実行手順が示されている。SGLang / vLLMの例は262,144 tokenで起動する設定だが、これはmodel自体の上限値と同義ではない。

- 公式repository: https://github.com/QwenLM/Qwen3.8-Flash-Next
- Hugging Face: https://huggingface.co/Qwen/Qwen3.8-Flash-Next
- ModelScope: https://www.modelscope.cn/organization/Qwen
- 公式blog: https://qwen.ai/blog?id=qwen3.8-flash-next

## 用語メモ

- **重み公開（open-weight）**: model weightをdownloadして自前hardwareで実行できる提供形態。source codeやtraining dataまで完全公開される「open source」とは同義ではない。
- **MoE（Mixture of Experts; エキスパート混合）**: 多数のFFN expertを持ち、各tokenではrouterがその一部だけを選んで実行するarchitecture。
- **総パラメータ数（total parameters）**: model file全体に含まれるparameter数。主に保存容量・RAM/VRAM容量へ効く。
- **有効パラメータ数（active parameters）**: 1 tokenのforwardで実際に使われるparameter数。MoEでは主に演算量の目安になる。
- **context length（文脈長）**: 1 requestでmodelが参照できる入力・履歴token数の上限。長くするとKV cache等のmemory使用量も増える。

重要なopen-weight MoEについては、公開情報がある範囲で総parameter数、active parameters、expert数、Top-k routing、context length、vision対応、license、Hugging Face / ModelScope / API、主要runtime対応状況、量子化時のmemory目安も記録する。

公式open-weight collection: https://huggingface.co/collections/Qwen/qwen38
