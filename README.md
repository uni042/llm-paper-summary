# LLM Inference and Training Systems Research Survey

LLM推論・学習システムに関する論文サーベイ、主要framework更新、新LLMリリースを整理したリポジトリです。

> このリポジトリの内容作成・要約・継続更新は、リポジトリ所有者の依頼に基づいてOpenAIのChatGPTが担当しています。生成AIによる整理を含むため、重要な判断では各ページの一次資料も確認してください。

## 構成

- [papers/](papers/) — 論文カタログ。まず推論／学習に分け、その下を研究系統別に整理
  - [Inference / 推論](papers/inference/) — 112本
  - [Training / 学習](papers/training/) — 17本
- [framework-updates/](framework-updates/) — 主要frameworkの重要な機能・性能更新
- [llm-releases/](llm-releases/) — 新LLMリリースの最新一覧とmodel family別履歴
- [templates/](templates/) — 追加時の記述テンプレート

## 論文の分類方針

論文は最終目的で分類します。推論高速化のために補助的な学習・蒸留・予測器trainingを使う場合も推論側に置きます。事前学習・fine-tuning・optimizer update・分散学習そのものの効率化を目的とする場合は学習側に置きます。

その下の研究系統は固定せず、独立した研究群が育った場合は適宜追加・分割・統合します。

## 記述方針

Transformer、MoE、KV cache、quantization、speculative decoding、tensor parallelismなど、LLM分野で広く使われる基礎用語は説明なしで使います。

一方で、**特定論文や狭い研究分野でしか通じにくい用語を、説明の前提としてそのまま使わない**ことを原則とします。論文固有の方式名や専門用語を残す場合は、最初の出現で「具体的に何をする仕組みか」を説明します。

例えば `goodput` とだけ書くのではなく「SLOを満たして処理できるrequest数」、`head-of-line blocking` とだけ書くのではなく「先頭の長いrequestが後続requestを待たせる状態」のように、**用語を知らなくても手法の動作と効果が分かる文章**を優先します。

この方針は一文要約だけでなく、概要、手法、評価、既存研究との差、限界、README、framework更新、LLM releaseページを含む全文章に適用します。

## 収録方針

研究・framework更新では、新しい実行方式、memory管理、routing、cache、offload、parallelism、quantization、kernel、明確な性能向上を扱います。単なるmodel対応、許可リスト追加、chat template、軽微な互換性変更、bug fixのみの更新は対象外です。

新LLMリリースは主要なmodel familyごとに整理し、原則として直近約半年の主要リリースを収録します。著名な系統で半年内に主要リリースがない場合は、その系統の最新モデル1件を残します。

情報源はarXiv、OpenReview、公式GitHub、公式release note、開発元の公式発表など一次資料を優先します。

## 論文ページ

各ページは一文要約、書誌情報、概要、手法、評価、限界、一次資料を含みます。weight offloadとKV cache offload、CPU DRAMと通常NVMe、peer GPU HBM、HBF、CXL、実機評価とsimulationを区別します。

現在の論文収録数: **129本**
