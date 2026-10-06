---
canonical_id: "arXiv:2601.07891"
title: "KVzap: Fast, Adaptive, and Faithful KV Cache Pruning"
summary: "KVzapはKVzipの重要度推定を高速なinput-adaptive近似へ置換し、prefillとdecodeの両方でKV cacheを選択的にpruneする。Qwen3-8B/32BとLlama-3.1-8B-Instructの長文脈・reasoning taskで、精度低下をほぼ出さず2–4倍のKV圧縮を達成し、KVpressへ実装されている。"
list_summary: "入力ごとにKV重要度を高速推定してprefill/decode中の不要cacheをpruneし、長文脈LLMで2–4倍のKV圧縮を狙う。"
authors: ["Simon Jegou","Maximilian Jeblick"]
published: "2026-01-12"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2601.07891"
sources: ["https://arxiv.org/abs/2601.07891"]
implementation: "Qwen3-8B/32B、Llama-3.1-8B-Instructでlong-context/reasoning taskを評価。NVIDIA KVpressに公式実装・model公開。"
code: "https://github.com/NVIDIA/kvpress"
last_checked: "2026-10-06"
arxiv_id: "2601.07891"
arxiv_categories: {primary: "cs.LG", cross_list: ["cs.AI","cs.CL"]}
worker_completed_at: "2026-10-06T10:51:00+09:00"
worker_run_key: "20261006-1030-scheduled-chat-30/r01"
---
## 概要
長文脈Transformerでは、各層が過去tokenのkey/valueを保持するKV cacheがsequence lengthとbatchに比例して増える。既存pruningは圧縮率を上げるほど精度を落とすか、重要度計算が重く、主要inference engineへ入れにくい。KVzapは高品質だが重いKVzipの重要度推定を高速に近似し、入力ごとに残すKVを変える。

## 手法
KVzapは固定位置や一律budgetだけで削るのではなく、現在の入力からKV entryの重要度を推定するinput-adaptive方式である。prefillだけでなくdecode中にも適用でき、不要と判断した過去KVを削って以後のattentionが読むcache量を減らす。

設計上の狙いは、圧縮判断そのものの計算を軽くし、pruningで減るmemory trafficを選別overheadが食い潰さないようにすることにある。実装はNVIDIAのKVpressへ公開され、複数modelに同一枠組みを適用する。

## 評価条件
|項目|条件|
|---|---|
|モデル|Qwen3-8B、Qwen3-32B、Llama-3.1-8B-Instruct|
|task|long-context、reasoning benchmark|
|比較|KVzipおよびKVpress leaderboardのpruning方式|
|指標|KV compression、task accuracy、pruning品質|

## 主要結果
2–4倍のKV cache圧縮を、評価taskでnegligibleなaccuracy lossに抑えて達成し、KVpress leaderboardでstate-of-the-art性能を報告する。32Bを含む複数規模で同じ方向の結果を示すため、単一小型modelだけの現象ではない。

## 既存研究との差
KVzipの高品質な重要度推定をそのまま使うのではなく、実推論へ載せやすい高速近似へ変える。H2Oや固定budget型のような一律heuristicより入力適応性を持ち、prefillとdecodeの双方を対象にする。

## 限界
2–4倍はcache容量の圧縮率であり、end-to-end latencyやthroughputが同じ倍率で改善することを意味しない。pruningが効く度合いはattention patternとtaskに依存し、極端な圧縮では重要tokenを落とすriskが残る。