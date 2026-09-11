# Conditional Computation

入力やtokenの難しさに応じて、**実行するlayer数、処理するtoken数、終了位置などを変え、不要な計算を最初から行わない**研究をまとめる。全tokenが全layerを必ず通る通常の実行を崩し、layer skipping、early exit、token pruningなどで計算量を減らす。

MoEのexpert数を変えるAdaptive Expert Computationとは対象が異なり、この系統では主にTransformer本体の実行深度や処理対象tokenを動的に変える。

<!-- survey:auto:start -->
## 自動生成の論文一覧（8本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

該当なし。

### 1年以上前

- **2024-08 · [LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding](2024-layerskip-enabling-early-exit-inference-and-self-speculative-decoding.md)**  
  実装：[✓](https://github.com/facebookresearch/LayerSkip) ・ リポジトリ内被引用：7  
  学習時に途中層からでもnext-トークン予測できるようモデルを訓練し、推論時は前半層だけで数トークンを仮生成して、残り層でまとめて検証することで、別下書きモデルなしの投機的 デコードを行う。

- **2024-07 · [LazyLLM: Dynamic Token Pruning for Efficient Long Context LLM Inference](2024-2407.14057-lazyllm-dynamic-token-pruning-for-efficient-long-context-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  長文入力で現在の生成に重要なトークンだけを後続層へ通し、外したトークンもhidden stateを別キャッシュへ保存して後で必要になれば途中層から復帰できるようにすることで、主にプリフィル計算を減らす。

- **2023-07 · [SkipDecode: Autoregressive Skip Decoding with Batching and Caching for Efficient LLM Inference](2023-2307.02628-skipdecode-autoregressive-skip-decoding-with-batching-and-caching-for-efficient-.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  生成が後ろへ進むほど実行するTransformer層数を段階的に減らし、同じ生成位置ではバッチ全体で同じ深度を使うことで、バッチ処理とKVキャッシュを壊さずデコード計算を減らす。

- **2025-07 · [DiffSkip: Differential Layer Skipping in Large Language Models](2025-diffskip-differential-layer-skipping-in-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークンごとにFFN前後のhidden state差を見て、表現をほとんど変えないFFNを小さなadapterへ置き換え、固定層削除より品質を保ちながら計算量を減らす。

- **2025-04 · [Dynamic Early Exit in Reasoning Models](2025-2504.15895-dynamic-early-exit-in-reasoning-models.md)**  
  実装：[✓](https://github.com/iie-ycx/DEER) ・ リポジトリ内被引用：0  
  推論途中で一度最終回答を試しに生成し、その答えのトークン確率が十分高ければ思考連鎖を終了、低ければ試行回答を捨てて元の地点から推論を続ける追加学習不要の手法。

- **2025-03 · [Position-Aware Depth Decay Decoding: Boosting Large Language Model Inference Efficiency](2025-2503.08524-position-aware-depth-decay-decoding-boosting-large-language-model-inference-effi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  生成後半ほど実行する層数を減らすが、最初と最後の層は常に残し、中間層だけを段階的にskipすることで、KV キャッシュを保ちながらデコード計算を減らす学習不要手法。

- **2025-03 · [Adaptive Layer-skipping in Pre-trained LLMs](2025-2503.23798-adaptive-layer-skipping-in-pre-trained-llms.md)**  
  実装：[✓](https://github.com/luoxuan-cs/Flexidepth) ・ リポジトリ内被引用：0  
  トークンごと・層ごとに通常の注意機構+FFNを実行するか小型adapterだけで済ませるかを選び、skipしたトークンのKVは残すことで文脈を保ちながら計算量を減らす。

- **2024-12 · [D-LLM: A Token Adaptive Computing Resource Allocation Strategy for Large Language Models](2024-d-llm-a-token-adaptive-computing-resource-allocation-strategy-for-large-language.md)**  
  実装：[✓](https://github.com/Jyk-122/D-LLM) ・ リポジトリ内被引用：0  
  各トークン・各層で「この層を実行するか」を小型moduleが判断し、skipしたトークンのKVも後続注意機構から外すことで、計算量とKV使用量をトークンごとに変える。
<!-- survey:auto:end -->
