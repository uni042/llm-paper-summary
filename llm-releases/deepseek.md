# DeepSeek系 LLMリリース

DeepSeekファミリーの主要リリースを新しい順に記録する。初回バックフィル対象期間: **2026-03-04〜2026-09-04**。

このページでは、正式提供（production）、公開beta、実験版（experimental）を区別し、同じV4名称でも提供段階が異なることが分かるようにする。

| リリース日 | モデル | 簡単な説明 | 公式リンク |
|---|---|---|---|
| 2026-10-17 | DeepSeek-V4.1-Flash-1017 | 公式変更履歴でWeb / app / APIの提供更新とHugging Face / ModelScopeのcheckpoint案内を確認。API指定名は従来どおり`deepseek-flash`だが、新snapshotへ移るため出力再現性と費用見積を再確認する。公式公表比較ではTerminal-Bench 4.0が31.2→42.3、DeepSWE v1.1が74.2→77.0など。ただしbenchmark設定は各前回値と同一条件とは限らず、端から端のtokens/s改善は未提示。| [公式更新履歴](https://api-docs.deepseek.com/zh-cn/updates/) / [1017発表](https://api-docs.deepseek.com/news/news261017/) / [公式重み](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017) |
| 2026-09-10 | DeepSeek-V4.1-Flash | 総552B parameterのMoE。新しい非対称Causal Encoder-Decoder構造で入力時8B、出力時16B parameterをactiveにする。前世代比でKV cacheのHBM要求を1/4、SSD保存量を1/8とし、native multimodal対応。DeepSeek APIの`deepseek-flash`として一般提供され、open-weightも公開。 | https://deepseek.com/en/news/deepseek-v4-1-flash/ |
| 2026-08-21 | DeepSeek-V4-Flash-Vision-Exp | V4-Flash系のtext能力へimage入力を統合した**実験版（experimental）multimodal model**。正式production modelではなく、vision統合を試験する位置づけとして区別する。 | https://api-docs.deepseek.com/news/news260821/ |
| 2026-08-13 | DeepSeek-V4-Pro | V4世代の上位production model。複数stepでtoolを使うエージェント能力（agent capability）と、taskに応じて推論量を調整するreasoning-effort controlを強化。App / Web / APIで一般提供。 | https://api-docs.deepseek.com/news/news260813/ |
| 2026-07-31 | DeepSeek-V4-Flash | V4-Flashの公開beta（public beta）。V4-Proより高速・低cost側を狙いながら、codingやtoolを使うagent taskを対象とし、Responses APIにも対応。 | https://api-docs.deepseek.com/updates/ |
| 2026-04-24 | DeepSeek-V4-Pro / V4-Flash | DeepSeek V4世代のAPI提供開始。従来の`deepseek-chat` / `deepseek-reasoner`を利用していたapplicationが、新世代modelへ移行する節目として記録。 | https://api-docs.deepseek.com/updates/ |

## API機能の更新

2026-10-17、公式発表でSearch APIとFetch APIの一般公開を告知。発表本文の料金は各endpoint 1,000回あたり0.75米ドルとされ、特定Harnessのserver-side tool経由は2026-10-31 16:00 UTCまで無料の案内がある。利用時には現行の公式料金ページで条件を再確認する。これはLLM重みや推論tokens/sの更新と別のAPI機能変更である。一次資料: https://api-docs.deepseek.com/news/news261017/。

## 用語メモ

- **正式提供（production / general availability）**: 継続利用を想定した正式serviceとして提供される段階。
- **公開beta（public beta）**: 一般利用できるが、仕様・性能・API挙動が正式版までに変わる可能性がある段階。
- **実験版（experimental）**: 新architectureやmodalを試験する段階で、production用途と分けて扱うmodel。
- **推論量制御（reasoning effort control）**: task難度や利用者設定に応じて、回答前に使う内部計算量を調整する仕組み。
- **Responses API**: 単純なtext completionだけでなく、tool useやmulti-step outputを統合して扱うAPI形式。

API modelの公開と重み公開（open-weight）は別なので、weight downloadが確認できた場合は個別に明記する。
