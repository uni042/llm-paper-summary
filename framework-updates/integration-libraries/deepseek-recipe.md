# DeepSeek Recipe

DeepSeek RecipeはDeepSeek V4 / V4.1向けのAPI互換・prompt変換ライブラリで、独立した推論engineではない。公式GitHub repositoryにsourceとREADMEが公開され、repository metadata上の最終更新日は2026-10-19 UTC。

## 役割

Rust libraryとPython bindingsを提供する。Messages、Chat Completions、Responses APIの入力を内部Conversation形式へ正規化し、DeepSeek V4 / V4.1用のpromptとtoken IDへ変換する。生成結果からreasoning、tool calls、JSON schema等をAPI responseへ戻す。

model推論、tool実行、HTTP転送は利用側が用意する。DeepSeek Recipe単体をserving runtimeとして扱わない。

## 安全上の注意

公式READMEによると、外部画像URLを取得する`ReqwestImageFetcher`は既定で宛先を制限しない。非信頼入力のURLを受けるserviceでは`DestinationFilter`を適用する。

MIT license。

## 一次資料

- [DeepSeek Recipe repository](https://github.com/deepseek-ai/deepseek-recipe)
