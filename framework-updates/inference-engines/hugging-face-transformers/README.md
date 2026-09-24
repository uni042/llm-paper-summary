# Hugging Face Transformers

Hugging Face Transformersの主要な機能・性能更新を継続的に記録する集約ページ。model実装、KV cache、attention backend、投機的デコード（speculative decoding）など、一般的な推論経路へ影響する変更を扱う。

## 現在できること

- **多数architectureを共通APIで扱う**: text、vision、audio、multimodalを含む多数のTransformer系modelを`AutoModel` / task-specific class等からloadし、inference・generation・fine-tuningへ使える。modelごとの細かな実装差を共通interfaceへ寄せるため、新しいarchitectureを試す基盤として使われる。
- **複数のgeneration方式**: greedy、sampling、beam search、top-k / top-p、temperature、constraint付き生成、streamingなどをgeneration APIから選べる。用途に応じて決定的生成、探索、確率的生成を切り替えられる。
- **投機的デコード**: assistant / draft modelで複数token候補を先に生成し、target modelでまとめて検証できる。候補受理率が高ければtarget modelのforward回数を減らし、品質を基本的にtarget model側へ保ったままdecode latencyを下げられる。
- **複数種類のKV cache**: Dynamic、Static、Sliding Window等のcache実装を選び、memory使用量、最大context、compileしやすさを調整できる。StaticCacheのようにshapeを固定するとcompile / graph最適化を適用しやすい一方、最大長分の領域を先に確保するcostがある。
- **attention backend切替**: PyTorch SDPA、FlashAttention等のbackendを選び、hardwareやsequence長に合うkernelを使える。model codeを大きく書き換えず、attention scoreの中間memoryやHBM trafficを削減できる。
- **量子化ecosystemとの連携**: bitsandbytes、GPTQ、AWQ、FP8等の量子化backendと連携して低bit weightをloadできる。model memoryを減らして小さいGPUへ載せたり、weight読出し量を抑えてdecodeを高速化したりできるが、方式ごとに対応hardware・精度・kernelが異なる。
- **device map / offload**: Accelerate等と連携し、layerごとに複数GPU、CPU DRAM、diskへweightを配置できる。単一GPUを超えるmodelをloadできる代わりに、CPU / storageからの転送がlatencyへ影響する。
- **fine-tuningとadapter連携**: Trainer、PEFT等と組み合わせ、full fine-tuning、LoRA、QLoRAなどへつなげられる。Transformers自身はmodel定義とtraining / generation interfaceの中心を担い、distributed trainingやparameter-efficient trainingは周辺libraryと統合して使う。
- **multimodal preprocessingから生成まで**: tokenizer、image processor、audio processor、processor統合を通じて、text以外の入力をmodel形式へ変換してgenerationまで接続できる。LLM単体だけでなくVLMやspeech-language modelの標準実行層としても使える。
- **compile / optimized kernelとの接続点**: `torch.compile`や固定shape cache、optimized attentionを組み合わせ、Python / dynamic shape由来のoverheadを減らせる。Transformersはserving schedulerそのものより、上位runtimeが利用するmodel implementation層として重要。

以下の更新履歴は、この広い機能群のうち**model対応追加ではなく、既存modelの一般的なKV cache・attention・decoding経路そのものを変える更新**を中心に記録する。

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
