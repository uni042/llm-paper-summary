---
title: "EAC-MoE: Expert-Selection Aware Compressor for Mixture-of-Experts Large Language Models"
summary: "量子化後のexpert-shiftをTopK-MSEで校正し、入力系列のexpert頻度に応じた動的pruningを組み合わせてMoEを圧縮する。"
authors_affiliations: "Yuanteng Chen, Yuantian Shao, Peisong Wang, Jian Cheng／Chinese Academy of Sciences, UCAS, Nanjing University of Science and Technology, AIRIA, [Maicro.ai](http://Maicro.ai)"
published: "2025-08-03"
publication_status: "Published"
lineage: "Quantization × MoE × Offload"
topics: ["Quantization","Dynamic Top-k","Quality-cost","Edge／on-device"]
importance: "高"
hardware_evaluation: "実機"
source: "https://aclanthology.org/2025.acl-long.633/"
code: ""
last_checked: "2026-09-03"
---

# EAC-MoE: Expert-Selection Aware Compressor for Mixture-of-Experts Large Language Models

> 量子化後のexpert-shiftをTopK-MSEで校正し、入力系列のexpert頻度に応じた動的pruningを組み合わせてMoEを圧縮する。

## 概要
EAC-MoEはMoE型LLMへquantization（量子化）とexpert pruning（専門家削減）を同時適用する圧縮手法である。MoEはtokenごとのactive parameterは少ないが、全expert重みを保持する総memoryは大きい。また低bit化の誤差はexpert出力だけでなく後続router入力へ伝わり、元モデルと違うexpertが選ばれるexpert-shiftを起こす。EAC-MoEはこれを主要な品質劣化源と捉え、Quantization with Expert-Selection Calibration（QESC）で量子化前後のTop-k選択を揃える。さらに入力sequenceによってexpert頻度が異なることを利用し、現在のprefillでほぼ使われないexpertをPruning based on Expert-Selection Frequency（PESF）により動的に省く。量子化でmodel weight memoryを、pruningでactive computeを減らす二段構成である。登録済みPTQ benchmark、MC-MoE、Not All Experts Are Equalを引用し、同じbit予算でrouting挙動まで校正する後続研究である。Mixtral、Phi、DeepSeek、QwenをRTX 3090で実測する。CPU／SSDからのoffloadは提案せず、低bit化によりGPUへ収める研究で、KV cache offload、HBF、CXLは対象外。
## 手法のあらまし
QESCはGPTQ系weight-only quantizationを基礎に、Transformer／MoE layerを順に校正する。通常のMSEは全出力誤差を均等に扱うが、TopK-MSEはrouter上位に入るexpertとその出力を重く扱い、量子化後も元のexpert rankingを維持させる。Mixtral分析ではFPかつshiftなしPPL 3.84に対し、FPでもshiftを許すと4.17、量子化のみ4.21、量子化＋shiftで4.65となり、routing変化が独立の損失要因である。PESFはprefill中のexpert selection frequencyをsequence単位で集計し、頻度threshold以下のexpertを実行集合から除く。タスクごとに頻出expertが違うため、model-globalな静的pruningより入力適応性がある。QESC後にPESFを適用し、低bit weightと小さいactive expert集合を組み合わせる。ただしfrequencyを得るにはsequence内の複数tokenが必要で、1 tokenずつ進むdecodeへそのまま適用できない。適応粒度はsequence／prefillで、tokenごとの必要K予測ではない。
## 評価
Mixtral-8x7B、Phi-3.5-MoE、DeepSeek-MoE-16B、Qwen1.5-MoE-A2.7BをWikiText2と8 zero-shot tasksで評価し、RTX 3090実機でmemory／speedを測る。Mixtralはmemoryを4.92倍削減して3090へ収め、量子化＋pruningで1.68倍高速化、平均accuracy lossを1%未満に抑えた。2.06-bitでMC-MoEのPPL 5.51、accuracy 62.56、1.80倍に対し、EAC-MoEは5.14、65.90、1.82倍。2.56-bitではPPL 4.58対4.74、accuracy 68.60対68.65、speed 1.74対1.71倍である。DeepSeek 2.06-bitではGPTQ 54.88、PMQ 54.79に対し57.05、Qwenでは57.76／57.79に対し59.52。PESF約30% pruning時のMixtralはfull precision 72.64に対し72.19だが、攻撃的設定では58.22まで低下し、明確なquality–compute trade-offがある。実機評価でsimulation-onlyではないが、decode適用、大規模671B、offload trafficは未評価。公式codeは確認できない。
## 引用関係
登録済みの [Examining Post-Training Quantization for Mixture-of-Experts: A Benchmark](2024-2406.08155-examining-post-training-quantization-for-mixture-of-experts-a-benchmark.md)、[Mixture Compressor for Mixture-of-Experts LLMs Gains More](2024-2410.06270-mixture-compressor-for-mixture-of-experts-llms-gains-more.md)、[Not All Experts are Equal: Efficient Expert Pruning and Skipping for Mixture-of-Experts Large Language Models](../02-adaptive-computation-cache-aware-moe/2024-2402.14800-not-all-experts-are-equal-efficient-expert-pruning-and-skipping-for-mixture-of-e.md) を引用する。
## 一次資料
- [ACL Anthology](https://aclanthology.org/2025.acl-long.633/)
- [arXiv](https://arxiv.org/abs/2508.01625)

