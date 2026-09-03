---
title: "DiffSkip: Differential Layer Skipping in Large Language Models"
summary: "隣接層の表現差分を指標に冗長な層を選択的に飛ばし、品質劣化を抑えてLLM推論を高速化する方式。"
authors_affiliations: "一次資料記載の著者ら（Findings of ACL 2025）"
published: "2025-07-27"
publication_status: "Published"
lineage: "Conditional computation"
topics: ["Dynamic depth","Quality-cost","Edge／on-device"]
importance: "高"
hardware_evaluation: "実機"
source: "https://aclanthology.org/2025.findings-acl.377/"
code: ""
last_checked: "2026-09-02"
---

# DiffSkip: Differential Layer Skipping in Large Language Models

> 隣接層の表現差分を指標に冗長な層を選択的に飛ばし、品質劣化を抑えてLLM推論を高速化する方式。

## 概要
DiffSkipは層を恒久的に削除するpruningではなく、元のFFNを残してtoken単位のrouterで実行を選ぶ。よって同じcheckpointが入力に応じて異なる深度を使い、single-tokenベンチマークと長い生成タスクで挙動を変えられる。routerとadapterだけを訓練するため、全重みを更新する再学習より負担が小さい。
DiffSkipは、事前学習済みdecoder-only LLMがtokenごとに動的深度を持つことを、self-attentionの層入力・出力差から学習するFFN block skipping法である。固定して最後のk層を落とすearly exitや、系列全体で同じ層を落とすsequence routerは、GSM8K/BBH/XSumのような多token生成で一度の誤りが次tokenへ伝播しやすい。DiffSkipは軽量routerを後半層にだけ置き、各tokenが各FFNをskip/retainする確率を出す。Llama-3-8B-Instructを3 epoch、Tulu-v2 326k対話、8×NVIDIA A100で約7時間だけ効率的fine-tuningし、LLM本体を凍結する。4 FFN skipでは単一token平均99.0%（基準比、MMLU/HellaSwag/Winogrande）、多token97.4%、8 skipでも各96.6%/86.0%を保持する。大モデルほど冗長性が高く、Llama-2-13Bは平均9.1 FFN skip可能だが、GPU上decodeの実速度はI/Oで制限され、prefill中心の利得に留まる点を率直に示した。
## 手法のあらまし
routerは後半層にのみ配置し、初期層の文脈形成を壊さない。gateのskip penaltyは期待skip数をkへ近づけるが、学習データにない難問では過剰skipが起こる。adapterを同じFFN位置に置くことで、skip後の表現を元モデルのlatent spaceへ戻し、次層のattentionとLM headで利用できるようにする。
まず各FFN blockの入力/出力差を調べ、差が小さい（変換が不要）tokenにskip余地があると仮定する。routerはhidden dimension dに対しbottleneck d/16のMLP、FFN側は元intermediateの1/16の小型adapter/projectionを持ち、SparseMixerでgateを学習する。attentionは維持し、後半16層にだけrouterを配置。lossは通常のLM loss＋skip数を目標kへ寄せる期待値L2 penaltyで、αを変え4/8 skipのモデルを作る。tokenごとのgateは連続生成中にも更新されるので、copyなど簡単なtokenは薄く、計算・推論tokenは深くする。比較baselineはEarlyExit、ShortGPT（cosine input-output）、LaCo（隣接層merge）、MindSkip（系列router）で、全てFFNだけをk個skipするよう揃えた。元モデルとadapterの表現ずれを抑えるためadapterを省くablationも行った。
## 評価
Llama-3-8B基準（MMLU/HellaSwag/Winogrande/GSM8K/BBH/XSum=67.3/70.6/74.4/67.9/52.4/12.2）。4 FFN skipでDiffSkipは66.3/73.2/74.3/64.8/50.2/12.3、retain99.0%。8 skipでは62.4/68.7/74.2/57.8/44.6/10.7、retain91.3%。4 skip時のmulti-token retain97.4%に対しEarlyExit55.0%、ShortGPT50.0%、LaCo91.5%、MindSkip53.7%。8 skipではbaseline群48.0/44.8/65.3/47.9%に落ちるのに対しDiffSkip91.3%。別モデルではLlama-3.2-3Bが平均3.1 skip、Llama-2-7B4.3、Llama-2-13B9.1で、3Bは1.7 skipだけでもHellaSwag70.6→68.3と敏感。Tulu-v2に数学が少ないためGSM8KでLlama-3-8B 67.9→57.2（8 skip）と劣化し、数学強化データでは改善。adapterなしは平均retain23.2%、linear adapter85.8%、weightなし95.0%で、MLP/重み付けが重要。8×A6000、batch8、出力5 tokenのthroughputは小幅改善に留まり、連続decodeで速度向上なし。理由は各batchがFFN/adapter双方をfetchし、router・I/O overheadがFLOPs削減を相殺するためである。限界はprefill依存、batch不均一、training data不足、k固定の別モデル適応、specialized kernel未対応。
## 一次資料
- [論文](https://aclanthology.org/2025.findings-acl.377/)
## 更新履歴
- 2026-09-02: 概要・手法・評価を一次資料に基づき拡充。

