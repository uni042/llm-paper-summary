# LLM Inference and Training Systems Research Survey

LLMの**推論・学習システム研究**を中心に、論文サーベイ、主要フレームワーク（framework）の重要更新、新しいLLMリリースを整理するリポジトリです。

単なる論文リンク集ではなく、各手法について「何をCPU / GPU / storageへ置くのか」「どの計算・通信を省くのか」「何と何を同時進行させるのか」「どのhardware条件で効果が出たのか」が、個別方式の名前を知らなくても追えることを目標にしています。

> このリポジトリの内容作成・要約・継続更新には、リポジトリ所有者の依頼に基づいてOpenAIのChatGPTを使用しています。生成AIによる整理を含むため、論文の数値・model仕様・release状態など重要な判断では、各ページに記載した一次資料も確認してください。

## リポジトリ構成

- [papers/](papers/) — **論文サーベイ**。最終目的を基準に推論 / 学習へ分け、その下を研究系統別に整理
  - [Inference / 推論](papers/inference/) — **113本**
  - [Training / 学習](papers/training/) — **17本**
- [framework-updates/](framework-updates/) — **実装側の更新追跡**。vLLM、llama.cpp、SGLang、DeepSpeed、ROCmなどで、性能・memory・offload・通信方式を実質的に変えるrelease / PRを記録
- [llm-releases/](llm-releases/) — **model公開の更新追跡**。主要model familyのAPI / open-weight releaseと、MoE構造、context length、multimodal対応などを整理
- [templates/](templates/) — 新しい論文・項目を追加するときの記述template

現在の論文収録数: **130本**（推論113本 + 学習17本）

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

API専用modelと重み公開（open-weight）modelを区別し、MoEでは総パラメータ数（total parameters）と1 tokenで使う有効パラメータ数（active parameters）を混同しないように記録する。

## 論文の分類方針

論文は**内部で何を使っているかではなく、最終目的**で分類する。

- 推論を速くするために予測器の学習、蒸留（distillation）、追加学習、calibrationなどを使う → `papers/inference/`
- 事前学習（pre-training）、追加学習（fine-tuning）、optimizer update、分散学習そのものを高速化・省memory化する → `papers/training/`

その下の研究系統は固定しない。同種研究が増えて独立した流れになった場合は、系統を追加・分割・統合する。

## 記述方針

### 基本方針: 方式名を知らなくても処理内容が分かる文章にする

Transformer、MoE、KV cacheのようなLLMの基礎概念は使用するが、**特定論文・特定runtime・狭い研究分野でしか通じない名称だけを説明の前提にしない**。

論文固有の方式名や専門用語を残す場合は、最初の出現で「具体的に何をする仕組みか」を説明する。

たとえば、

- `goodput` → **設定したlatency目標（SLO）を守りながら処理できたrequest数 / throughput**
- `head-of-line blocking` → **queue先頭の長いrequestが後続requestまで待たせる状態**
- `zero-copy` → **CPU / GPU間でdataを別bufferへ複製せず、同じmemoryを直接参照する方式**
- `fusion` → **別々なら中間結果を書き出す複数処理を1 kernelへまとめる方式**

のように、用語そのものより**処理・原因・効果**を優先する。

この方針は一文要約だけでなく、概要、手法、評価、既存研究との差、限界、各系統README、framework更新、LLM releaseページにも適用する。

## 収録方針

### 論文・framework更新

以下のように実行方式やresource使用を実質的に変えるものを扱う。

- memory管理 / cache
- CPU・GPU・SSDへのoffload
- routing / expert配置
- parallelism / disaggregation
- quantization
- speculative decoding
- GPU kernel / communication
- 明確な性能・capacity改善

単なるmodel対応追加、allowlist、chat template、軽微な互換性変更、bug fixだけの更新は原則として対象外とする。

### LLM release

主要model familyごとに、原則として直近約半年の主要releaseを記録する。著名な系統で半年内に主要releaseがない場合は、その系統の直近主要modelを1件だけ期間外として残す。

API提供、重み公開（open-weight）、preview / beta / experimentalは区別する。

## 一次資料

情報源はarXiv、OpenReview、conference proceedings、公式GitHub、公式release note、model providerの公式発表・model cardなど**一次資料を優先**する。

特に以下は同じ数値として扱わない。

- 実機測定とsimulation
- GPU HBM、CPU DRAM、別GPU memory、通常NVMe SSD、network / remote storage
- weight offloadとKV cache offload
- kernel単体benchmarkとend-to-end throughput
- preprint / Open PRと正式release
- open-weightとopen source

## 論文ページの標準構成

各論文ページは原則として、

- 一文要約
- 書誌情報
- 概要 / 問題設定
- 手法
- 評価条件と主要結果
- 既存研究との差
- 限界
- 一般的な実装上の含意
- 一次資料

を含む。

数値だけを並べず、**何と比較した値か、どのhardware条件か、kernel単体かend-to-endか**まで追える形を優先する。
