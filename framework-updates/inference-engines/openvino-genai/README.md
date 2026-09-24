# OpenVINO GenAI

OpenVINO GenAIの主要な機能・性能更新を継続的に記録する集約ページ。Intel CPU / GPU向けLLM・生成model実行、投機的デコード（speculative decoding）、temporal cache、compile / link最適化などを扱う。

## 現在できること

- **Intel hardware上の生成AI推論**: Intel CPU / GPU / NPUでLLM、vision-language model、embedding / reranking、image / video generation等を実行できる。OpenVINO graphへ変換・compileしてhardware別に最適化するため、server CPUからclient deviceまで同じecosystemで扱える。
- **LLM generation pipeline**: tokenization、prefill、decode、KV cache更新、streamingをpipeline APIとしてまとめて扱える。application側で低level generation loopを全面的に自作せず、C++ / Pythonから組み込める。
- **continuous batching**: 複数requestを生成途中でもbatchへ出し入れし、request長が異なってもGPU / CPUを継続利用できる。1件ずつ直列に処理するよりthroughputを上げやすい。
- **KV cache管理**: 過去tokenのK/Vを保持し、decode時にprompt全体を再計算しない。長contextではKVが支配的なmemoryになるため、cache layoutとprecisionが同時request数を左右する。
- **prefix / prompt再利用**: 共通prefixがあるrequestで以前の計算結果を再利用し、system promptや長いdocument contextのprefill計算を減らせる。RAGやagent workloadで同じprefixを繰り返す場合に有効。
- **投機的デコード**: 小さいdraft model等で複数token候補を先に作り、target modelでまとめて検証できる。tree型候補も扱い、1本のdraft列が途中で外れたときでも別branchを受理できる可能性を残せる。
- **model圧縮 / 低精度実行**: OpenVINOのquantization / compression toolchainと組み合わせ、INT8 / INT4等のweightを利用できる。model memoryとmemory bandwidthを減らし、CPU / iGPU / NPUの限られたmemoryへ載せやすくする。
- **heterogeneous device deployment**: 同じmodelをCPU、GPU、NPU等へ展開し、deviceごとの得意なprecisionやoperatorへ合わせて実行できる。実際に1 pipeline内でどうdeviceを使い分けられるかはmodel / plugin対応に依存する。
- **VLM / embedding / reranking**: text generation以外に画像入力を含むmodelやretrieval向けencoder / rerankerを同じGenAI ecosystemで扱えるため、RAG pipeline全体をIntel hardware上へまとめやすい。
- **image / video generation**: diffusion / video generation pipelineも扱い、LLM以外の反復生成modelをlocal / server applicationへ組み込める。
- **temporal cache**: diffusion / video generationでは連続step間で変化の小さい中間featureを再利用し、毎step同じ計算を繰り返す量を減らせる。これはLLMのKV cacheとは異なり、反復denoising / video stepの計算省略に使う。
- **C++ / Python組込み**: native application、desktop application、server backendから同じpipelineを呼び出せる。Pythonの試作からC++製品へ移す場合にもAPI体系を揃えやすい。
- **compile / graph最適化**: OpenVINO compilerとlink-time最適化を使い、operator fusion、constant folding、dead code除去などを通してruntime overheadとmemory trafficを減らせる。
- **client / edge寄りの位置づけ**: 大規模GPU cluster向けserving schedulerというより、Intel hardwareへ生成AImodelを圧縮・compileして実アプリへ組み込むことに強みがある。

以下の更新履歴は、model追加ではなく、**decode回数、反復生成step、graph実行overhead、device memoryを実質的に変える主要機能**だけを記録する。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

### 2026-08-05 — 2026.3.0.0（released）

- **EAGLE系Dynamic Tree Search speculative decodingを正式releaseへ収録**: draft側が1本のtoken列だけでなく複数候補を木構造（tree）として作り、target modelがまとめて検証する方式。

  通常のspeculative decodingではdraft token列の途中が外れると後続候補も捨てやすい。tree形式なら複数branchを同時に用意できるため、target modelが受理できる経路を増やせる可能性がある。実装PR自体のmergeは収録期間前だが、製品releaseとして利用可能になったのがこのversion。[PR #3451](https://github.com/openvinotoolkit/openvino.genai/pull/3451)

- **TaylorSeer temporal cache**: LTXVideo生成で、時間step間で変化が小さく再利用できる中間計算をcacheし、毎step同じ計算をやり直さないようにする。

  **temporal cache（時間方向cache）**は、連続する生成stepで中間featureが近いことを利用し、一部stepの計算をskipする方式。LLMのKV cacheとは異なり、動画diffusion系の反復計算を減らすためのcacheである。LTXVideoでは既定有効化。比較可能な性能値はrelease noteに未掲載。[PR #3642](https://github.com/openvinotoolkit/openvino.genai/pull/3642)

- **LTO有効化**: GenAI objectをbuildするときにLTO（Link-Time Optimization; link時最適化）を有効化。

  個別source fileを別々に最適化するだけでなく、link時にmoduleをまたいで関数inline化や不要code除去を行えるようにする。公式性能値なし。[PR #3672](https://github.com/openvinotoolkit/openvino.genai/pull/3672)

2026.2.1.0は主に製品version更新・修正が中心のため、本質的な新しい性能機能としては掲載対象外とした。

[releases](https://github.com/openvinotoolkit/openvino.genai/releases)

### 用語メモ

- **Dynamic Tree Search**: draft候補を1列ではなく複数branchのtreeとして展開し、target modelで一括検証するspeculative decoding方式。
- **temporal cache**: 連続stepで似た中間結果を再利用し、生成modelの反復計算を省くcache。
- **LTO（Link-Time Optimization; link時最適化）**: compilerが複数object fileをまとめて見て、module横断で最適化する仕組み。
