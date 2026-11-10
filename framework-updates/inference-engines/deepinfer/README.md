# DeepSeek DeepInfer

DeepInferはDeepSeek-V4.1-Flash向けに公開されたDeepSeekのoffline inference runtime。2026-10-20の一般公開を確認した。公式GitHub repositoryの作成は2026-10-16 UTCで、確認時点ではタグ付き正式releaseはない。

## 対応構成

現在の公開READMEで示される対象はDeepSeek-V4.1-Flash、NVIDIA SM100 GPUまたはHuawei Ascend 950 NPU、Linuxである。Python 3.12、GCC 13以降を要求し、NVIDIA経路はCUDA 13を必要とする。

## 実行方式

FlashMLA、DeepGEMM、DeepEP、DeepSelect、TileLang等を組み合わせる。Attention DP / CP、MoE EP / EPLB、DSparkと信頼度ベースのverification、SWAのbounded replay、非同期scheduling、batch構成に依存しない決定的sampling、structured outputを含む。

## 適用範囲と比較上の注意

公開版はoffline inferenceが中心で、完全なproduction serving stackではない。公式READMEはKV cache system、prefill / decode disaggregation、DP replica間のload balancerが公開版に含まれないと説明しているため、repository名だけからvLLMやSGLangの完全な代替と扱わない。

Apache-2.0で公開される。公式benchmarkのprefill条件（4×SM100）とdecode条件（64×SM100）は規模が異なるため、相互の直接比較や単一GPU性能への外挿はできない。Windows / RTX 4070 SUPERは記載された対応構成に含まれない。

## 一次資料

- [DeepInfer repository](https://github.com/deepseek-ai/DeepInfer)
- [DeepInfer README](https://github.com/deepseek-ai/DeepInfer/blob/main/README.md)
