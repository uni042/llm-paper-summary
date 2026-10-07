---
canonical_id: "arXiv:2606.26875"
title: "Information-Aware KV Cache Compression for Long Reasoning"
summary: "InfoKVは直近attentionだけでは長い推論で将来重要になるtokenを捉えにくい問題に対し、予測entropyと層間表現変化をattention scoreへ統合してKV保持tokenを選ぶ。Llama-3.1/3.2のLongReasonとDeepSeek-R1-Distillの長いdecodeで既存attention型圧縮を上回り、20%程度のcache予算でも長距離情報保持を改善する。"
list_summary: "予測entropyと層間表現変化をattentionへ統合し、近傍で目立たなくても将来の長い推論へ影響するtokenをKV cacheに残す。"
authors: ["Jushi Kai","Zhuiri Xiao","Alexandra Birch","Zhouhan Lin"]
published: "2026-06-25"
publication: "arXiv"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2606.26875"
sources: ["https://arxiv.org/abs/2606.26875"]
implementation: "Llama-3.1-8B-Instruct、Llama-3.2-3B-Instruct、DeepSeek-R1-Distill-Qwen-7B/Llama-8BでLongReason、IFEval、AIME 2024、LiveCodeBenchを評価。一次資料から公式code URLは確認できなかった。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2606.26875"
arxiv_categories: {primary: "cs.CL", cross_list: []}
reference_main_sha: "7755cc2d70dde454ac2743f6c86772df469b9478"
worker_completed_at: "2026-10-06T18:48:00+09:00"
worker_run_key: "20261006-1830-scheduled-chat-30/r01"
---
## 概要
KVキャッシュ圧縮では、直近queryから大きなattentionを受けた過去tokenを残す方式が一般的である。しかし長い思考連鎖では、現在は参照されていなくても数千token後の推論で再び重要になる情報がある。InfoKVはこの「将来への影響」をForward Influenceで分析し、attentionが主に近距離依存を拾う一方、予測時の不確実性が高いtokenは遠い将来まで強い影響を持つことを示す。

提案法は予測entropy、層ごとの表現変化、attentionを組み合わせ、各層で保持すべきKV tokenを選ぶ。Llama-3.1/3.2の長文prefillとDeepSeek-R1-Distillの最大32768-token decodeを評価し、attentionだけのSnapKV、PyramidKV、Expected Attention、RPCより一貫して高い品質を示す。

## 問題設定
SnapKV系は最近の観測windowから過去tokenへのattentionを集計するため、直近文脈との関連性には強い。しかし推論状態が長時間で変化すると、今は低attentionでも後から必要になる前提・中間結論を落とし得る。InfoKVはtoken削除前後の将来予測分布のKL divergenceを平均したForward Influenceを定義し、このずれを直接調べる。

最初の2048 tokenを圧縮し将来128-token chunkへの影響を追う分析では、attention上位tokenの影響は距離とともに急減するのに対し、高entropy tokenは14K規模の遠距離でも強い影響を示す。そこで「最近参照されたか」と「そのtokenが情報量を持つか」を補完的な信号として扱う。

## 手法
### 予測entropy
token生成時の語彙分布からentropy Hを計算する。全語彙の低確率tailはノイズになりやすいため、上位k候補だけで計算するTop-k Restricted Entropyを使う。実験ではk=256が安定して良く、全語彙entropyより高い性能を示した。

### 層間表現変化
層lのhidden stateと最終層hidden stateのcosine distance Dを計算し、E_i^(l)=D_i^(l) H_i とする。早い層ですでに最終表現へ近いtokenより、層を通じて表現が大きく変わるtokenへ高い情報scoreを与える。最終層でscoreがゼロにならないようbias τを加え、τ=1を既定値とする。

### attentionとの統合
各層の最終scoreは S_i^(l)=α A_i^(l)+(1-α)Softmax(E^(l))_i とし、上位tokenだけKVへ残す。α=1は純attentionへ退化し、実験ではα=0.9が最も良かった。entropyを強くしすぎても短距離依存を失うため、両者の混合が必要である。

### decode時運用
長いdecodeでは1024 token生成ごとにKV圧縮を起動する。これは一度prefillを圧縮して終わる方式と違い、増え続ける思考tokenにも同じ重要度判定を繰り返す。追加費用はentropy・表現距離・score計算であり、保持率を下げるほど後続attentionとKV memoryが減る。

## 評価条件
|項目|内容|
|---|---|
|prefillモデル|Llama-3.1-8B-Instruct、Llama-3.2-3B-Instruct|
|decodeモデル|DeepSeek-R1-Distill-Qwen-7B、DeepSeek-R1-Distill-Llama-8B|
|prefill benchmark|LongReason、16K/32K/64K|
|decode benchmark|IFEval、AIME 2024、LiveCodeBench|
|decode上限|32768 tokens、1024 tokenごとに圧縮|
|比較|SnapKV、PyramidKV、Expected Attention、RPC、Full cache|

## 主要結果
Llama-3.1-8B-InstructのLongReasonでは40% cacheでInfoKVの平均accuracyはCoT 52.53%、直接回答48.88%で、SnapKVの51.09%/47.15%、PyramidKVの50.76%/46.25%、Expected Attentionの51.13%/46.81%を上回る。20% cacheでも49.79%/46.89%で各attention型baselineより高い。

Llama-3.2-3B-Instructでも40% cacheのCoT平均43.95%でSnapKV 43.03%、PyramidKV 42.86%、Expected Attention 43.11%を上回る。長decodeではDeepSeek-R1-Distill両系列でRPCよりIFEval、AIME、LiveCodeBenchを改善し、Llama-8BのIFEvalでは保持率25%と12.5%がfull cacheを上回る条件もある。

ablationではtop-256 entropy、τ=1、α=0.9が最も安定して良い。α=1の純attentionよりentropy混合が改善し、entropy側へ寄せすぎると逆に悪化するため、長距離情報と局所関連性の両方が必要だと分かる。

## 既存研究との差
SnapKV/PyramidKVは最近のattentionから重要度を推定し、Expected Attentionは将来query分布を推定する。InfoKVはattention予測だけでなく、token生成時の情報量と層をまたぐ表現進化を独立信号として加える。RPCのようなdecode中の反復圧縮にも同じ情報scoreを適用できる。

## 限界
entropyと層間hidden stateを得る追加処理が必要で、純attention score再利用より管理費用が増える。評価は特定のLlama/DeepSeek-R1-Distill系列と長推論benchmarkに限られ、実測tokens/sやGPU memory削減量そのものは主評価ではない。保持率を極端に下げる場合は重要tokenの誤削除リスクが残る。