# MLX LM

MLX LMの主要な機能・性能更新を継続的に記録する集約ページ。Apple Silicon上のLLM実行、KV cache、MLA、投機的デコード（speculative decoding）、MTPなどを扱う。

未マージPRは正式releaseと明確に分け、**提案段階の性能値をstable機能として扱わない**。

## 現在できること

- **Apple Silicon上でのLLM推論**: Appleの統一memoryを使い、text generation、chat、streaming、batch generationを実行できる。CPUとGPUが同じphysical memoryを共有するため、GPU専用VRAMへweightを丸ごとcopyする構成とは異なり、大容量RAMをmodelとKVで共同利用できる。
- **Hugging Face modelの変換**: Hugging Face Hub等のcheckpointをMLX向けweight / configへ変換し、Apple GPUで実行しやすい形式へ持ち込める。既存open-weight modelをApple Siliconへ移す入口として使える。
- **weight量子化**: model weightを低bit化し、統一memory使用量とweight読出し量を減らせる。量子化済みmodelを保存・再配布できるため、毎回変換し直さずlocal inferenceへ使える。
- **KV / prompt cache管理**: rotating KV cacheで保持する過去token量へ上限を設けたり、prompt cacheを保存して共通prefixのprefill結果を再利用したりできる。長context時のmemory増加と再計算のどちらを優先するか調整できる。
- **prefillの分割実行**: 長いpromptを小さいstepへ分けてprefillし、一度に作るactivationやtemporary tensorのpeak memoryを抑えられる。統一memory容量は大きくてもbandwidthと一時memoryは有限なので、長文処理で重要になる。
- **LoRA fine-tuning**: base weightを固定し、小さいadapterだけ学習するLoRAを実行できる。full fine-tuningよりoptimizer stateとgradient memoryを大幅に減らし、Mac上で現実的な追加学習を行いやすい。
- **full-parameter fine-tuning**: model全parameterを更新するtrainingにも対応する。LoRAよりmemory要求は大きいが、Apple Siliconを推論専用ではなく研究用training環境としても利用できる。
- **量子化modelを使った追加学習**: 量子化済みbase modelとadapter trainingを組み合わせ、base weightのmemory footprintを抑えながらfine-tuningする構成を取れる。
- **distributed inference / training**: `mx.distributed`を使い、複数device / hostへ計算やparameterを分散できる。単一deviceの計算・memory制約を超える構成へ拡張できる一方、network / inter-device通信costが追加される。
- **Python API / CLI / server**: libraryとしてgeneration loopへ組み込む、CLIでlocal chatする、serverとして常駐させる、といった複数の使い方ができる。library APIとserver CLIでは公開されているcache / quantization optionが一致しない場合があるため、利用可能機能を区別して扱う必要がある。
- **投機的デコード関連の基盤**: modelのMTP headや外部draftを使って複数tokenをまとめて検証する経路を扱える。MLAやrecurrent architectureでは通常のTransformer KVと異なるcache処理が必要なため、multi-token attention経路やrollback対応が性能・対応範囲を左右する。
- **Apple Silicon向け研究・試作の位置づけ**: datacenter servingのmulti-tenant schedulerより、Mac上でopen-weight modelをload・量子化・fine-tune・serveまで一貫して試す用途に強い。

以下の更新履歴では、stable機能に加え、**MLA multi-token decode、KV cache量子化、recurrent state rollbackのように「Apple Silicon上で長contextや投機的デコードをどこまで実用化できるか」を変える未マージPR**をstableと分離して追跡する。

## 初期収録期間

2026-06-03〜2026-09-03

対象期間内に本一覧の基準を満たすstable releaseはない。以下は2026-09-07時点でも未マージのPRとして記録する。

## 注視すべきPR

### 2026-09-02 — #1817（Open）

**multi-token MLA decodeで、cache長と同時query数から高速なattention経路を自動選択する提案。**

MLA（Multi-head Latent Attention）はK/Vを低次元latentへ圧縮してcacheする。decodeで1 tokenだけ処理するときは、latentを完全なK/Vへ展開せず計算する**absorbed path**が効率的だが、複数tokenを一度に検証する投機的デコードでは、条件によってlatentを展開する**materialized path**の方が速くなる。

従来実装はmulti-token stepで常にcache全体を展開する側へ寄るため、長いcontextほどverify costが急増していた。このPRは、

- 現在のKV cache長
- 1 stepで同時処理するquery数
- modelのhead dimension

から両方式の分岐点を計算し、その時点で速い方を選ぶ。

GLM-4.7-Flash＋8K promptではdraft model付き生成が **2.8 → 14.7 tok/s**。cache 8,192のverify stepは **363.7 → 3.3 ms**。ただし同じarchitectureの重いdraft modelでは、target verifyが速くなってもdraft costを含めた全体が通常decodeを上回らない場合がある。[PR #1817](https://github.com/ml-explore/mlx-lm/pull/1817)

### 2026-08-29 — #1804（Open）

**MLX LM serverからKV cache量子化を設定できるようにする提案。**

library APIではKV cacheを低bit化できる一方、`mlx_lm.server`のCLIからは指定できなかった。このPRは、

- `--kv-bits`
- `--kv-group-size`
- `--quantized-kv-start`
- `--max-kv-size`

をserverへ公開し、長いcontextで線形に増えるKV memoryを抑えられるようにする。

対応していないcache layerがある場合は黙って一部だけ量子化せず、起動時に検出してerror終了する。現状、量子化KVを有効にするとbatched request pathは未対応のため、requestを1件ずつ処理する制約がある。独立した速度benchmarkはなし。[PR #1804](https://github.com/ml-explore/mlx-lm/pull/1804)

### 2026-09-02 — #1821（Draft / WIP）

**投機的デコードで巻き戻せるrecurrent state cacheを作る提案。**

通常のKV cacheはtoken単位に末尾を切り戻しやすいが、linear attentionやrecurrent modelが持つstateは「現在までを集約した1つの状態」になっており、draft tokenが拒否されたとき数token前へ戻しにくい。

現在の`ArraysCache`は最後のhidden stateだけを保持するため、投機的デコードやMTPで必要なrollbackができない。このPRの**RecurrentCache**は、短いdraft区間についてtokenごとのstateを時間方向に保持し、拒否されたtoken分だけ切り戻せるようにする。

代償として通常のKV cacheよりtokenあたりstateが大きく、長いprefix全体をcacheする用途にはmemory costが高い。PR自身もbatch generationはWIP、profiling未実施としている。[PR #1821](https://github.com/ml-explore/mlx-lm/pull/1821)

## 状態

2026-09-07確認時点で、#1817と#1804はOpen、#1821はOpenかつDraft。いずれもstable MLX LMへ入った機能としては扱わない。

[公式releases](https://github.com/ml-explore/mlx-lm/releases)で、本収録期間より前の最新stableはv0.31.3。

### 用語メモ

- **absorbed MLA**: 圧縮latentからattention結果を直接計算し、完全なK/V tensorへ展開しない経路。
- **materialized MLA**: 圧縮latentを一度通常のK/V表現へ展開してからattentionする経路。
- **verify step**: speculative decodingでdraft token列をtarget modelがまとめて検証するforward step。
- **rollback / trim**: draft tokenが拒否されたとき、cache stateを最後に確定したtoken位置まで巻き戻すこと。
