# StepFun系 LLMリリース

StepFunが公開する主要モデルを記録する。公開日、checkpointが実際に確認できる日、配備資料の検証範囲を区別する。

| 日付 | モデル | 構成・配備 | 公式資料 |
|---|---|---|---|
| 2026-09-20 | Step 5 Preview | 総600B / 有効27Bの疎MoE、最大1M context。仕様表はtext・image入力を記載するが、説明本文のvideo記述とは不一致があるためvideo対応は未確定として扱う。公式BF16 repoは約1.21TB。vLLM、SGLang、Transformersの配備例がある。FP8構成例はB300×4またはH200×8、BF16はB300×8またはH200×16。BF16変換・生成の全工程は公式カードで未検証と注記される。| [公式BF16重み](https://huggingface.co/stepfun-ai/Step-5-Preview-BF16) / [commit履歴](https://huggingface.co/stepfun-ai/Step-5-Preview-BF16/commits/main) / [license](https://huggingface.co/stepfun-ai/Step-5-Preview/blob/main/LICENSE.txt) |

## 公開日とライセンス

2026-10-15に公式model cardの更新を確認したが、同じrepoのcommit履歴にはBF16重みのアップロードが2026-09-20に記録されている。したがって10月15日を重み初回公開日と断定しない。ライセンスはStepFun Model License 1.0。Apache-2.0そのものではなく、製品機器への商用搭載や一定条件のModel as a Service（MaaS）では追加契約が必要となる場合がある。帰属表示の対象・閾値を全出力へ無条件に適用される義務と読み替えず、利用前に公式条文を確認する。

この規模の重みは12GB VRAMのPCで実行できる対象ではない。長context時の実用性もGPU memory、KV cache、runtime並列構成に依存する。
