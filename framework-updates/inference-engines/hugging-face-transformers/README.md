# Hugging Face Transformers

Hugging Face Transformersの主要な機能・性能更新を継続的に記録する集約ページ。model実装、KV cache、attention backend、投機的デコード（speculative decoding）など、一般的な推論経路へ影響する変更を扱う。

## 現在できること

- text、vision、audio、multimodalを含む多数のTransformer系modelを共通APIでloadし、inference・fine-tuning・generationへ使える。
- generation APIでsampling、beam search、constraint付き生成、streaming、assistant modelを使うspeculative decodingなど複数のdecoding方式を扱える。
- Dynamic / Static / Sliding Windowなど複数のKV cache実装を選び、compileしやすさ、memory量、長context向け挙動を調整できる。
- SDPA、FlashAttention等のattention backendをmodel側から選択し、hardwareに応じた高速kernelを利用できる。
- bitsandbytes、GPTQ、AWQ、FP8等の量子化ecosystemと連携し、低bit modelをload・推論できる。
- Trainer / PEFT等の周辺libraryと組み合わせ、full fine-tuning、LoRA、分散学習へつなげられる。

以下の更新履歴は、この広い機能群のうち**KV cacheを使うprefill高速化とspeculative decoding**の最近の主要変更だけを記録している。model追加や互換修正は対象外とする。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

### 2026-07-15 — v5.14.0（released）

- **StaticCache利用時のSDPA prefillをFlashAttention kernelへdispatch**: 固定サイズのKV cacheであるStaticCacheを使う場合でも、prompt全体を処理するprefill phaseでFlashAttention系kernelを選べるようにした。

  **SDPA（Scaled Dot-Product Attention）**は標準的なattention計算API、**FlashAttention**はattention score全体をVRAMへ展開せずblock単位で処理し、memory trafficと一時memoryを減らす高速実装である。

  Llama 3.1 8Bでは、8,192-token入力のprefillが **0.735 → 0.280秒**。512-token入力でも約 **10%改善**。[PR #47094](https://github.com/huggingface/transformers/pull/47094)

### 2026-08-10 — v5.15.0（released）

- **static ensemble speculative decoding**: draft modelだけの確率分布で候補tokenを作るのではなく、本体model（target）とdraftの分布を固定比率で混合して候補を作る投機的デコードを追加。

  投機的デコードでは、小さいdraft modelが複数token候補を先に生成し、大きなtarget modelがまとめて検証する。候補が多く受理されるほど、target modelを呼ぶ回数を減らせる。

  この方式は追加学習を必要とせず、PRが引用する評価では受理率が約 **65% → 78%**へ上昇し、ROUGE-L低下は0.5 point以内。ただしこれはTransformers project自身の独立benchmarkではなく、PRで参照された評価値として扱う。[PR #45979](https://github.com/huggingface/transformers/pull/45979)

v5.16.0のcache関連変更は、既存挙動の修正や変更取り消しが中心で、独立した新しい性能機能としては本一覧から除外した。

### 用語メモ

- **prefill**: 入力prompt全体をまとめて処理し、最初のKV cacheを作る段階。
- **decode**: prefill後、過去KVを再利用しながら1 tokenずつ生成する段階。
- **StaticCache**: 最大長などに合わせてKV保存領域を先に固定確保するcache。shapeが安定するためcompile / graph最適化と相性がよい。
- **acceptance rate（受理率）**: draftが提案したtokenのうちtarget modelがそのまま採用できた割合。高いほど投機的デコードの利得が大きくなりやすい。
