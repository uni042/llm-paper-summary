# OpenVINO GenAI

OpenVINO GenAIの主要な機能・性能更新を継続的に記録する集約ページ。Intel CPU / GPU向けLLM・生成model実行、投機的デコード（speculative decoding）、temporal cache、compile / link最適化などを扱う。

## 現在できること

- Intel CPU / GPU / NPU上でLLM、vision-language model、embedding / reranking、画像・動画生成などの生成AIpipelineを実行できる。
- LLM generationではKV cache、continuous batching、streaming、prefix / prompt再利用等を使い、複数requestや長contextを効率化できる。
- speculative decodingを利用し、小さいdraftまたはtree状の候補をtarget modelでまとめて検証してdecode回数を減らせる。
- OpenVINOのmodel変換・低精度最適化と組み合わせ、INT8 / INT4等の圧縮modelをIntel hardwareへ展開できる。
- C++ / Python APIからpipelineとして組み込み、local applicationやserver backendに利用できる。
- diffusion / video系ではstep間の中間結果を再利用するcacheも扱い、LLM以外の生成modelの反復計算も削減できる。

以下の更新履歴は、model追加ではなく、**speculative decoding、temporal cache、compile / link最適化**など実行方式を変える主要機能だけを記録している。

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
