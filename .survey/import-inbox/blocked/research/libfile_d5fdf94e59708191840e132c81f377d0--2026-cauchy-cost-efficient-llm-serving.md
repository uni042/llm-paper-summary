---
canonical_id: "DOI:10.1145/3772052.3772264"
title: "Cauchy: A Cost-Efficient LLM Serving System through Adaptive Heterogeneous Deployment"
authors: ["Menghao Zhang", "Li Li", "Chunming Hu", "Tianyu Wo", "Chengru Song", "Jin Ouyang"]
published: "2026-01-13"
summary: "Cauchyはプリフィルとデコードを同種GPUへ固定配置すると、計算律速/帯域律速の違いとGPU世代・価格差を活かせず資本効率が落ちる問題を扱う。異種GPU構成のプリフィル・デコード対をGPU Comboとして性能/価格で評価し、SLOを満たすCombo集合を選ぶ。Combo内では機会的schedule、Combo間ではgoodput重み付きround-robinを使い、負荷急増時はautoscalingする。実験では厳格なSLOを維持しつつTokens/USDを既存方式より最大38.3%改善する。"
list_summary: "プリフィル・デコードを異種GPUのGPU Comboへ適応配置し、階層scheduleとautoscalingでSLOを守りながらTokens/USDを最大38.3%改善するサービング基盤。"
source: "https://doi.org/10.1145/3772052.3772264"
worker_completed_at: "2026-10-03T05:58:00+09:00"
worker_run_key: "20261003-0545-scheduled-chat-45"
reference_main_sha: "e7d11a1ba6865891d8156766cef11ea559fddc97"
---

# Cauchy: A Cost-Efficient LLM Serving System through Adaptive Heterogeneous Deployment

## 概要
LLMサービングのプリフィルは長いpromptをまとめて処理するため計算律速になりやすく、デコードは1 tokenずつ重みとKVを読むためメモリ帯域律速になりやすい。それにもかかわらず、同じGPU型を両段階へ割り当てる構成では、GPU世代ごとの演算性能・メモリ帯域・価格差を使い切れない。

Cauchyはプリフィル用GPU構成とデコード用GPU構成の組を「GPU Combo」として扱い、各ComboのSLO内goodputと費用からTokens/USDを評価する。要求量を満たすCombo集合を選び、Combo内部とCombo間で別のschedulerを使い、負荷変動時はautoscalingする。

2025 ACM Symposium on Cloud Computing掲載版の評価では、既存の最先端baselineよりTokens/USD効率を最大38.3%改善しながら、設定したサービス水準目標（SLO）を維持する。

## 問題設定
高価なGPUが常に費用効率のよい選択とは限らない。プリフィルでは高い演算throughputが価値を持つ一方、デコードではメモリ帯域・容量と価格の比が重要になる。さらにtensor parallel数を変えると各段階の速度と1request当たり費用も変わる。

単一GPU型へ統一すると運用は簡単だが、プリフィル側に不要な帯域、デコード側に不要な演算能力へ支払う可能性がある。逆に異種GPUを無計画に混ぜると、遅い段階がbottleneckになりSLO違反が増える。

## 手法
### GPU Comboの性能・費用モデル
Cauchyは「プリフィルをGPU型A・並列度pで、デコードをGPU型B・並列度qで動かす」といった組を1 Comboとする。各ComboについてTTFT/TPOT等のSLOを満たせるgoodputと時間当たりGPU費用を見積もり、Tokens/USDを比較する。

この単位にすることで、プリフィルとデコードを別々に最安化して通信や段階bottleneckを無視するのではなく、1要求が両段階を通る全体費用として選択できる。

### Combo集合の配置
到着率を1 Comboで処理できない場合、Cauchyは複数Comboを配置する。単に最高性能Comboを複製せず、費用効率とgoodputを基に異種Comboを組み合わせ、SLOを満たす必要capacityを確保する。

負荷が変われば最適なCombo集合も変わるため、固定provisioningではなくautoscalingで構成を更新する。急増時にcapacity不足を放置してSLOを破るより、追加Comboを起動して費用効率を安定させる。

### 階層scheduler
Combo内部では、その時点の空き資源と要求特性を使う機会的scheduleでGPUを埋める。Combo間ではgoodput重み付きround-robinで要求を配り、処理能力の異なるComboへ同数要求を投げて遅い構成を飽和させることを避ける。

この二段構造により、globalには異種capacity比を守り、localには各Comboの瞬間的な空きを利用する。異種GPUを使うだけでなく、負荷分配まで異種性能へ合わせる点が重要である。

## 評価条件
|項目|内容|
|---|---|
|対象|オンラインLLMサービング|
|分離単位|prefill / decode|
|資源|性能・価格の異なる異種GPU|
|配置単位|GPU Combo（prefill構成 + decode構成）|
|QoS|goodput、TTFT/TPOT等のSLO|
|費用指標|Tokens/USD|
|比較|同種GPU中心の既存サービングbaseline|

## 主要結果
|条件・指標|結果|意味|
|---|---:|---|
|Tokens/USD|最大38.3%改善|異種GPUの段階別適性を費用へ変換|
|SLO|厳格条件を維持|安価GPU利用のために遅延制約を捨てていない|
|負荷変動|autoscalingで追従|固定Comboだけでなく需要変化を対象化|
|階層schedule|Combo能力差を考慮|異種構成間の過負荷を抑制|

## 既存研究との差
DistServe等の分離サービングはプリフィルとデコードを別資源へ置くことで干渉を減らすが、CauchyはさらにGPU型・並列度・価格の異質性を配置問題へ入れる。目標も単純throughput最大化ではなく、SLOを満たした上でのTokens/USDである。

異種GPU serving研究の中でも、個別requestを「最速GPUへ送る」だけではなく、prefill/decode対をComboとして事前評価し、Combo内/間の階層scheduleとautoscalingを一体化する。

## 限界
最大38.3%は評価したGPU価格・モデル・負荷・SLOに依存する。クラウド価格やGPU供給が変われば最適Comboも変わるため、固定した組を普遍的最適解として使えない。

プリフィル・デコード分離にはKV転送が必要で、network帯域やtopologyが弱い環境では異種配置の利得を通信費が相殺し得る。autoscalingにも起動時間があり、非常に短いburstでは追従が間に合わない可能性がある。

## 一次資料
- https://doi.org/10.1145/3772052.3772264