---
canonical_id: "arXiv:2606.23581"
title: "Kamera: Unified Position-Invariant Multimodal KV Cache for Training-Free Reuse"
summary: "Kameraはmultimodal agentが同じ画像・動画chunkを別位置で再利用する際、RoPE位置差をexact re-rotationし、失われるcross-chunk conditioningだけをrank-m低ランクpatchで補うtraining-free KV再利用方式である。MLA/GQA/MHAを統一的に扱い、rank約32でmulti-hop精度を回復し、SGLang kernelでbf16丸め誤差水準までre-prefill KVを再構成する。"
list_summary: "マルチモーダル KVをposition-free canonical キャッシュとして保存し、位置はRoPE再回転、文脈依存差分は低ランクpatchで復元してreorder・slide・再取得時の再プリフィルを避ける。"
authors: ["Bole Ma","Jan Eitzinger","Harald Koestler","Gerhard Wellein"]
published: "2026-06-22"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2606.23581"
sources: ["https://arxiv.org/abs/2606.23581"]
implementation: "Qwen2.5-VL、Qwen3-VL、Kimi-VL等6 backbone、MLA/GQA/MHAで評価し、SGLang paged-attention/KV poolへproduction kernelを統合。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2606.23581"
arxiv_categories: {primary: "cs.DC", cross_list: ["cs.AI","cs.CV"]}
worker_completed_at: "2026-10-06T16:55:00+09:00"
worker_run_key: "20261006-1630-scheduled-chat-30/r01"
last_audited: null
audit_version: 0
---
## 概要
マルチモーダル agentは同じvideo frame、UI screenshot、document pageを文脈 windowの移動や再推論で何度も見る。しかし接頭辞/radix キャッシュは同じleading 接頭辞・同じ位置でしか命中せず、chunkが別offsetへ移るとLLM プリフィルをやり直す。KameraはKVをcontentとpositionへ分離し、位置変更を代数的なRoPE再回転、文脈依存の差だけを低ランクpatchで補う。

## 問題設定
chunk Bを単独プリフィルしたKV(B|∅)と、antecedent Aの後でプリフィルしたKV(B|A)は異なる。独立キャッシュを単純連結すると、問い合わせがBを読む読み出し自体はsoftmax 状態 mergeで回復できるが、BがAから吸収したcross-chunk conditioningが消える。

この差Δ=KV(B|A)-KV(B|∅)はトークン方向にはdiffuseで、理想条件でも約50% トークンを再計算しないと十分回復しない。一方feature方向にはlow-ランクで、出力に効くenergyは少数方向へ集中し、主にdeep 層に現れる。したがってトークン 枝刈りよりfeature-space patchが適する。

## 手法
canonical storeにはposition-freeなKV(B|∅)を置く。再利用位置がδだけずれた場合、keyのRoPE 局面だけをR(δ)でexactに再回転する。valueやMLA 潜在表現などposition-free contentはbyte-identicalに再利用する。

conditioning patchはcompile時に一度だけconditioned 順伝播を行い、Δを計算してtop-m SVD factor U_m V_m^Tとして保存する。serve時は順伝播なしでcanonical KVへ低ランクGEMM patchを加える。ランクは概ね8～16で効果が立ち上がり、32付近でplateauする。

この分解をMLA、GQA、MHAへ共通化する。GQA/MHAではkeyをre-rotateしてK/Vをpatchし、MLAではposition-free cKVを保持してdecoupled k_ropeだけを回転する。

window操作では、reorderは同じcached setの順序変更へ一つのorbit patchを再利用し、sliding-window survivorはrotationだけで移動、追い出し chunkの再取得だけ新しいantecedentに対応するpatchを加える。

## 評価条件
|項目|内容|
|---|---|
|基盤モデル|Qwen2.5-VL、Qwen3-VL、Kimi-VL等6種|
|注意機構|GQA、deepstack GQA、MLA、MHA|
|タスク|MM-NIAH、two-page doc-QA、multi-hop video等|
|ランタイム|SGLang paged 注意機構 / KV プール|
|比較|blind 再利用、re-プリフィル、トークン-recompute型キャッシュ 再利用|

## 主要結果
two-page タスクではblind 再利用でsingle-hop accuracyは0.57のままだが、multi-hopはMLAで0.41→0.28、GQAで0.28→0.15へ低下する。Kameraのランク-m patchはこのcross-chunk bindingを回復し、トークン-recompute方式がmulti-hop answer flipの平均約20%しか戻せない条件で約97%を回復する。

SGLang実装ではre-プリフィル KVをbf16 rounding内に再構成し、residual next-トークン KLは約1e-3。patchは標準KV pageの約2%規模の例があり、同じchunkが約9回再利用されるとcompile時順伝播 コストを償却する。

## 既存研究との差
position-independent キャッシュが位置だけを補正するのに対し、Kameraは失われるconditioningを明示的に測定・補正する。CacheBlend/EPIC等のトークン再計算はトークン軸のsparsityを仮定するが、KameraはΔがfeature軸low-ランクである観測を使う。

## 限界
patch作成にはantecedentごとに一度conditioned 順伝播が必要で、再利用回数が少ないと償却できない。利得は同じvisual chunkが繰り返されるマルチモーダル agentで大きく、毎回完全に新規contentなら小さい。deep-層だけpatchする省メモリ版の最適深さはモデル依存である。