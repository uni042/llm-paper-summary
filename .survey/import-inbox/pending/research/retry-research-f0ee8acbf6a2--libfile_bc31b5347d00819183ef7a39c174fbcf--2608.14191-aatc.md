---
canonical_id: "arXiv:2608.14191"
title: "KV Cache Compression Through the Lens of Transform Coding"
summary: "AATCはKV cache量子化誤差そのものではなくattention出力への歪みを最小化するbit配分を、white-noise量子化modelとtransform coding/rate-distortion理論から導く。Llama-3.1-8B-InstructとQwen-2.5-7B-Instructで約5.8倍圧縮時にnear-lossless accuracyを維持し、比較baselineはいずれかのtaskで劣化する。"
list_summary: "注意機構への影響をrate-distortion目的に直接組み込み、トークン/経路ごとのbit配分を最適化してKV キャッシュを約5.8倍圧縮する。"
authors: ["Hannah Laus","Claudio Mayrink Verdun","Hao Wang","Flavio du Pin Calmon","Felix Krahmer"]
published: "2026-08-14"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2608.14191"
sources: ["https://arxiv.org/abs/2608.14191"]
implementation: "Llama-3.1-8B-InstructとQwen-2.5-7B-InstructをLongBench、RULER、GSM8K、MMLU-Pro、MATH-500で評価。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2608.14191"
arxiv_categories: {primary: "cs.LG", cross_list: []}
worker_completed_at: "2026-10-06T12:06:00+09:00"
worker_run_key: "20261006-1130-scheduled-chat-30/r03"
last_audited: null
audit_version: 0
---
## 概要
KVキャッシュ（KV キャッシュ）の量子化は通常、保存したK/V テンソルの再構成誤差を小さくする。しかし同じテンソル誤差でも注意機構 スコアやvalue集約への影響はトークン・経路で異なる。Attention-Aware Transform Coding（AATC）は圧縮対象そのものではなく、最終注意機構への歪みをrate-distortion目的へ入れる。

## 手法
white-noise 量子化 モデルの下で注意機構-aware distortionを解析し、key由来とvalue由来の寄与が加法的に分解でき、さらにトークン/経路へfactorizeできることを示す。この構造により各成分へbitをどう配るかを独立したrate-distortion項として扱える。

calibration setから各成分の感度を推定し、transform codingとreverse water-fillingを用いて総bit budget内の配分を決める。uniform low-bit dtypeではなく、注意機構に強く効く成分へbitを重点配分する。

## 評価条件
|項目|条件|
|---|---|
|モデル|Llama-3.1-8B-Instruct、Qwen-2.5-7B-Instruct|
|タスク|LongBench、RULER、GSM8K、MMLU-Pro、MATH-500|
|対象|KV キャッシュ 量子化/compression|
|指標|compression ratio、タスク accuracy|

## 主要結果
約5.8倍のKV キャッシュ圧縮でnear-無損失 accuracyを維持する一方、各比較比較対象はいずれかの評価条件で明確な劣化を示す。長文脈だけでなくGSM8K/MATH-500等のreasoning タスクを含めて検証しているため、圧縮誤差のautoregressive影響も評価対象に入る。

## 既存研究との差・限界
テンソル reconstruction errorを代理指標にする既存量子化に対し、注意機構機構を通した下流 distortionを直接最適化する。理論はwhite-noise量子化近似に依存し、calibration 分布から大きく外れる入力で最適配分が維持される保証はない。また圧縮率・品質が中心で、専用カーネルによるエンドツーエンド スループット倍率は主要結果ではない。