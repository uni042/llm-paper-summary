# LLM Inference and Training Systems Research Survey

LLMの**推論システム研究**を中心に、論文サーベイ、主要フレームワーク（framework）の重要更新、新しいLLMリリースを整理するリポジトリです。Training論文は既存内容を参照用として保持し、通常更新は凍結しています。

単なる論文リンク集ではなく、各手法について「何をCPU / GPU / storageへ置くのか」「どの計算・通信を省くのか」「何と何を同時進行させるのか」「どのhardware条件で効果が出たのか」が、個別方式の名前を知らなくても追えることを目標にしています。

> このリポジトリの内容作成・要約・継続更新には、リポジトリ所有者の依頼に基づいてOpenAIのChatGPTを使用しています。生成AIによる整理を含むため、論文の数値・model仕様・release状態など重要な判断では、各ページに記載した一次資料も確認してください。

[進捗](.survey/reports/metadata-coverage-latest.json) ／ [研究の横断比較](papers/inference/comparison.md) ／ [運用手順](.survey/docs/survey-workflow/README.md) ／ [全体点検](.survey/reports/consistency-latest.json)

## リポジトリ構成

- [papers/](papers/) — **論文サーベイ**
  - [Inference / 推論](papers/inference/) — **285本**
  - [Training / 学習](papers/training/) — **19本（凍結）**
  - [Survey / サーベイ](papers/survey/) — **4本**
- [framework-updates/](framework-updates/) — 主要runtime / frameworkの重要機能更新
- [llm-releases/](llm-releases/) — 主要model familyのrelease情報
- [.survey/](.survey/) — 運用手順・状態・補助スクリプト・テスト・templateなどの管理用領域

現在の論文収録数: **308本**（推論285本 + 学習19本 + サーベイ4本）

## 運用対象

通常の論文探索は、推論・serving・decoding・runtime・実行時memory / I/O・on-device inferenceの効率化を最終目的とする研究を対象にします。学習を内部手段として利用していても最終目的が推論効率化ならInferenceへ収録します。

Framework更新とLLMリリースは論文サーベイとは別に整理します。

<!-- survey:auto:start -->
推論：**285本** ／ 学習：**19本** ／ サーベイ：**4本**。 [推論一覧](papers/inference/README.md) ／ [学習一覧](papers/training/README.md) ／ [サーベイ一覧](papers/survey/README.md) ／ [研究比較](papers/inference/comparison.md)
<!-- survey:auto:end -->
