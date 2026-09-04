# LLM Inference and Training Systems Research Survey

LLM推論・学習システムに関する論文サーベイ、主要フレームワーク更新、新LLMリリースを整理したリポジトリです。

> このリポジトリの内容作成・要約・継続更新は、リポジトリ所有者の依頼に基づいてOpenAIのChatGPTが担当しています。生成AIによる整理を含むため、重要な判断では各ページの一次資料も確認してください。

## 構成

- [papers/](papers/) — 9つの研究系統で整理した論文ページ
  - オフロード／階層メモリ
  - Adaptive computation／cache-aware MoE
  - Expert prefetch
  - Conditional computation
  - Speculative decoding × MoE
  - Quantization × MoE × Offload
  - Quality-cost optimization
  - Edge／on-device MoE
  - その他システム研究
- [framework-updates/](framework-updates/) — 主要フレームワークの本質的な機能・性能更新
- [llm-releases/](llm-releases/) — 新LLMリリースの最新一覧と系統別履歴
- [templates/](templates/) — 追加時の記述テンプレート

## 収録方針

研究・フレームワーク更新では、新しいruntime mechanism、memory management、routing、cache、offload、parallelism、quantization、kernel、明確な性能向上を扱います。単なるモデル対応、allowlist、chat template、軽微な互換性変更、bug fixのみの更新は対象外です。

新LLMリリースは主要なmodel familyごとに整理し、原則として直近約半年の主要リリースを収録します。著名な系統で半年内に主要リリースがない場合は、その系統の最新モデル1件を残します。

情報源はarXiv、OpenReview、公式GitHub、公式リリースノート、開発元の公式発表など一次資料を優先します。

## 論文ページ

各ページは一文要約、書誌情報、概要、手法のあらまし、評価、限界、一次資料を含みます。weight offloadとKV cache offload、CPU DRAMと通常NVMe、HBF、CXL、実機評価とsimulationを区別します。

現在の論文収録数: **80本**
