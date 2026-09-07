# LLM Inference and Training Systems Research Survey

LLMの**推論・学習システム研究**を中心に、論文サーベイ、主要フレームワーク（framework）の重要更新、新しいLLMリリースを整理するリポジトリです。

単なる論文リンク集ではなく、各手法について「何をCPU / GPU / storageへ置くのか」「どの計算・通信を省くのか」「何と何を同時進行させるのか」「どのhardware条件で効果が出たのか」が、個別方式の名前を知らなくても追えることを目標にしています。

> このリポジトリの内容作成・要約・継続更新には、リポジトリ所有者の依頼に基づいてOpenAIのChatGPTを使用しています。生成AIによる整理を含むため、論文の数値・model仕様・release状態など重要な判断では、各ページに記載した一次資料も確認してください。

## リポジトリ構成

- [papers/](papers/) — **論文サーベイ**。最終目的を基準に推論 / 学習へ分け、その下を研究系統別に整理
  - [Inference / 推論](papers/inference/) — **123本**
  - [Training / 学習](papers/training/) — **19本**
- [framework-updates/](framework-updates/) — **実装側の更新追跡**。vLLM、llama.cpp、SGLang、DeepSpeed、ROCmなどで、性能・memory・offload・通信方式を実質的に変えるrelease / PRを記録
- [llm-releases/](llm-releases/) — **model公開の更新追跡**。主要model familyのAPI / open-weight releaseと、MoE構造、context length、multimodal対応などを整理
- [templates/](templates/) — 新しい論文・項目を追加するときの記述template

現在の論文収録数: **142本**（推論123本 + 学習19本）

## 3種類の情報を分けて扱う

### 1. 論文サーベイ

新しい推論・学習手法そのものを扱う。

例:

- GPUに収まらないweight / KV cacheをCPUやSSDへ退避する
- MoE expertを予測して先読みする
- KV cacheを圧縮する
- request schedulingやprefill / decode分離を改善する
- activationやoptimizer stateをCPU / storageへoffloadして学習memoryを減らす

### 2. フレームワーク更新

論文とは別に、既存runtimeへ実際に入った重要実装を追う。

たとえば、

- CUDA kernelを融合して中間memory accessを減らす
- KV cacheをGPU → CPU → diskの複数階層へ拡張する
- MoEのGPU間通信を高速化する
- 投機的デコード（speculative decoding）をruntimeへ統合する
- weight / activation / optimizer stateのoffloadを正式機能へ入れる

といった変更を対象にする。

### 3. LLMリリース

新しいmodelが出たこと自体を追う。