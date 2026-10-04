---
canonical_id: "arXiv:2607.17181"
title: "Talaria: Session-Aware Serverless Serving of Hundred-Billion-Parameter LLMs"
summary: "Talariaはtool-using agentの複数LLM呼出しを独立requestではなくsessionとして扱い、model residency、KV locality、instance pressureを統合したrouting、soft reservation、session-prefill、host-restorable KV、device-to-device weight stagingを組み合わせる。100B超3モデル・30 SWE-Bench sessionの単一TP=8 server replayでp50 session completion timeを1000秒から189秒、p95を2296秒から867秒へ短縮する。"
list_summary: "agent sessionのmodel/KV localityをsoft reservationとslot内prefillで維持し、100B級multi-model servingのsession完了時間を短縮する。"
authors: ["Utopia Meng","Unicornt Zhao","Derek Li","Goalen Gao","Frank Du"]
published: "2026-07-19"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2607.17181"
sources: ["https://arxiv.org/abs/2607.17181"]
implementation: "単一TP=8 server上で100B超3モデルをround-based multiplexingし、SWE-Bench由来30 model-session・960 callsをfixed replay。routerは別の2-worker TP=4 testbedでも評価。公式コードURLは確認できなかった。"
code: null
last_checked: "2026-10-04"
arxiv_id: "2607.17181"
arxiv_categories: {primary: "cs.DC", cross_list: ["cs.AI"]}
worker_completed_at: "2026-10-04T07:23:00+09:00"
worker_run_key: "20261004-0700-scheduled-chat-00/r02"
---
# Talaria: Session-Aware Serverless Serving of Hundred-Billion-Parameter LLMs

## 概要
serverless multi-model servingは通常request単位で負荷分散するが、agentはtool callを挟みながら同じLLMへ何度も戻り、長いKV prefixを再利用する。別instanceへrouteされるとmodel weightとKV localityを失い、同じinstanceでもround-based model multiplexingの次slotまで待つ。Talariaはsession continuityをplacementとadmissionの共通単位にする。

## 手法
routerはmodel residency、KV locality、instance pressureを合わせてplacementを順位付けする。sessionがtool処理へ出た後も戻る可能性をsoft reservationとしてadmission budgetへ計上し、GPUを完全にpinせずreturn affinityを残す。Session-Prefill（SP）はactive model slotが閉じる前にbudget内のcontinuationを割り込みadmitし、次round待ちを避ける。

instance側はHBM addressを安定させ、hostから復元可能なKV registryを維持する。model switch時にはdevice-to-device（D2D）weight stagingを使い、次modelのweightを準備する。これらはrouterだけでは実現できないsession localityを実行基盤側で支える。

## 評価条件
|項目|条件|
|---|---|
|end-to-end|単一TP=8 server、8 GPU|
|モデル|100B超3モデル（Qwen3-235B等）|
|workload|SWE-Bench由来30 model-session、960 calls|
|比較|同一round schedulerでSP/HKVR/D2Dを無効化したRound-only|
|router別評価|2-worker TP=4 testbed|
|指標|session completion time、TTFT、ablation|

## 主要結果
Round-only比でp50 session completion time（SCT）は1000秒から189秒へ5.3倍、p95は2296秒から867秒へ2.6倍改善し、30 session中29件が改善した。p50 TTFTは13.44秒から0.55秒へ低下する。逆ablationではSPの寄与が最大で、SPを外すとp50 SCTは189秒から623秒へ悪化する。host KV restorationを外すと486秒、D2D stagingを外すと194秒で、後者は中央値よりtail改善への寄与が大きい。

## 既存研究との差
request単位のload-aware routingやmodel round schedulingに対し、Talariaはtool gapをまたぐsessionの「次に戻ってくる可能性」を資源予約へ組み込む。KVを永久pinせずsoft reservationにするため、session localityとmulti-tenant利用率を両立しようとする。

## 限界
100B級のend-to-end結果は単一serverで、cluster-scale placementは別の小型testbedで評価されており、両者を同時に測ったものではない。pool membershipはstaticで、soft reservationの未使用率も残る。prefill/decode完全分離clusterへSPを拡張するにはcross-tier KV ownership調整が必要である。

## 一次資料
- https://arxiv.org/abs/2607.17181