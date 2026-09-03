---
title: "D-LLM: A Token Adaptive Computing Resource Allocation Strategy for Large Language Models"
summary: "トークンの難度に応じて使用するTransformer層を動的に割り当て、LLMの計算量を細粒度に制御する方式。"
authors_affiliations: "一次資料記載の著者ら（NeurIPS 2024）"
published: "2024-12-15"
publication_status: "Published"
lineage: "Conditional computation"
topics: ["Dynamic depth","KV cache offload","Quality-cost"]
importance: "高"
hardware_evaluation: "実機"
source: "https://proceedings.neurips.cc/paper_files/paper/2024/hash/03469b1a66e351b18272be23baf3b809-Abstract-Conference.html"
code: "https://github.com/Jyk-122/D-LLM"
last_checked: "2026-09-02"
---

# D-LLM: A Token Adaptive Computing Resource Allocation Strategy for Large Language Models

> トークンの難度に応じて使用するTransformer層を動的に割り当て、LLMの計算量を細粒度に制御する方式。

## 概要
D-LLMの「動的」は文全体を一つの出口で止める意味ではなく、同一層であってもtokenごとに実行/skipが違うという意味である。そのため数学記号や難しい内容語は多層を使い、冗長な機能語は少層で処理する。Ωを学習時に指定するので、精度一定の単一モデルを作るより、端末ごとに計算予算を変えたモデルを同じ枠組みで生成できる。
D-LLMは、入力トークンごとにTransformer層を実行するかskipするかを決める動的推論パラダイムである。従来のLLMは簡単な語や問題にも一律に全層を割り当てるが、D-LLMはトークン難度に応じて計算資源を配分する。各層の前に小さなdynamic decision moduleを置き、hidden stateからskip/executeのカテゴリ確率を出力。ユーザーが目標acceleration rate Ωを指定できるため、端末・GPU性能に合わせて平均計算量を調整できる。Llama 2 7BとLlama 3 8B（各32層）をLoRAでfew-shot fine-tuningし、Alpaca/SAMSum、GSM8K/MaWPS、BoolQ/PIQA/SIQA/OBQA/MMLUの9ベンチマークで評価した。結論としてLlama 2では約55〜59%、Llama 3では約52〜55%のFLOPsで、LoRA full-depthと同等以上の精度を得る。さらにskipされたトークンのKVを捨てるevictionによりKVストレージを約45%削減する。条件計算をトークン単位に実装し、通常の層pruningより入力・問題ごとの適応性が高い点が新規性である。
## 手法のあらまし
hard decisionは順伝播時だけ使い、逆伝播ではGumbelノイズとsoft probabilityを通すため、skip/executeの離散選択をend-to-endで最適化できる。KV evictionを行わない設定は計算を節約しても、次tokenが参照できる文脈を残す必要から品質が落ちる。文頭m tokenを予約するのはこの長距離依存への安全策である。
層lへの入力x_lを2線形層＋活性化のdecision module g_lへ入れ、skip/execute確率を得る。argmaxでhardな二値b_lを作るが非微分なので、学習時はGumbel-Softmaxとstraight-through estimatorを使う。順伝播はx_\{l+1\}=b_skip x_l+b_exec f_l(x_l)で、実行しない層のattention/FFNを丸ごと省く。平均skip率ω_nと指定ΩのL1差をacceleration-ratio lossにし、通常のlanguage-model cross-entropyと重みαで合算する。事前学習から動的モデルを作れるほか、LoRAで既存Llamaに追加する。KV evictionでは、ある層でskipした過去トークンのK/Vをattention maskで後続queryから隠す。ただし文頭トークンは後続予測への寄与が大きく、最初のmトークンを常時保持する。本実験はm=2、最初の2層は安定化のためdecision対象外、最大文脈1024、decision hidden dimension 512。skipトークンを隠すことでKV容量もskip率に比例して減るが、文脈情報を失う危険があり、保持数を明示的に調整する。
## 評価
D-LLMの表はFLOPsをLlama 2 7B LoRA full-depth=1.00に正規化した平均値であり、壁時計ではない。従って0.55という値は理論計算量が約半分という意味で、decision moduleやmask生成の実装費用を別途考慮する必要がある。
Llama 2 7Bの表では、D-LLMのPPL/FLOPsはAlpaca 6.01/0.59、SAMSum 3.18/0.55、GSM8K accuracy 0.29/0.59、MaWPS 0.74/0.56、BoolQ 0.73/0.52、PIQA 0.84/0.52、SIQA 0.82/0.54、OBQA 0.80/0.53、MMLU 0.53/0.55（LoRA full-depth FLOPs=1.00）。比較対象MoD、Shortened-LLaMA（PPL/Taylor）、Ada-Inferはいずれも0.56〜0.90のFLOPsで、D-LLMは全9データセットで概ね最良または同等。Llama 3 8Bでも5データセット以上で55%未満の計算量でLoRAを上回る。MaWPS/OBQAでは40%/30% FLOPsでも100% FLOPs baselineを超える一方、SAMSumは計算量を増やしすぎると過学習でPPLが悪化。m=0,1,2,4,8を比べm=2が最良で、KV evictionなしでは精度が下がる。限界はdecision moduleとGumbel温度、α・Ωのデータ/端末依存、層ごと・tokenごとの不規則分岐がGPU実効速度を下げること。報告速度は主にFLOPs/KV容量で、壁時計での大規模バッチ実証は限定的である。浅いモデルや複雑な数学では過剰skipが誤りを増幅し、skip層のKVを捨てる積極策は長文文脈を損ねうる。
## 一次資料
- [論文](https://proceedings.neurips.cc/paper_files/paper/2024/hash/03469b1a66e351b18272be23baf3b809-Abstract-Conference.html)
- [公式コード](https://github.com/Jyk-122/D-LLM)
## 更新履歴
- 2026-09-02: 概要・手法・評価を一次資料に基づき拡充。

