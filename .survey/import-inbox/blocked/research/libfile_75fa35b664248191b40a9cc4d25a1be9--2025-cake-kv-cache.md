---
canonical_id: "OpenReview:EQgEMAD4kv"
identity_tokens: ["OpenReview:EQgEMAD4kv","arXiv:2503.12491"]
title: "CAKE: Cascading and Adaptive KV Cache Eviction with Layer Preferences"
authors: ["Ziran Qin","Yuchen Cao","Mingbao Lin","Wen Hu","Shixuan Fan","Ke Cheng","Weiyao Lin","Jianguo Li"]
published: "2025-01-22"
source: "https://openreview.net/forum?id=EQgEMAD4kv"
summary: "CAKEは長文脈推論のKVキャッシュ削除で全Transformer層へ同じ容量を配ると、層ごとに異なる注意の空間集中度・時間変動を無視する問題を扱う。注意統計から層別選好を算出して総容量を適応配分し、上位層へ向かうカスケード管理と、平均だけでなく時間方向の変動も見る削除指標で重要tokenを保持する。LongBench/NeedleBenchと複数モデルで、元KVの3.2%だけでも性能を維持する条件を示し、128K文脈ではFlashAttention-2の全cache比で復号遅延を10倍超高速化する。"
list_summary: "層ごとの注意集中度と時間変動からKV容量を適応配分し、カスケード削除と変動感知scoreで長文脈cacheを3.2%まで削減しつつ品質を保つ。"
worker_id: "scheduled-chat-45"
worker_completed_at: "2026-10-03T06:58:00+09:00"
worker_run_key: "20261003-0645-scheduled-chat-45"
reference_main_sha: "c6b4225a61c6c358d9faf707386cae9ba8d84ae1"
---

# CAKE: Cascading and Adaptive KV Cache Eviction with Layer Preferences

> 層ごとの注意集中度と時間変動からKV容量を適応配分し、カスケード削除と変動感知scoreで長文脈cacheを3.2%まで削減しつつ品質を保つ。

## 書誌

- 著者: Ziran Qin, Yuchen Cao, Mingbao Lin, Wen Hu, Shixuan Fan, Ke Cheng, Weiyao Lin, Jianguo Li
- ICLR 2025
- OpenReview: EQgEMAD4kv
- arXiv: 2503.12491
- 一次資料: https://openreview.net/forum?id=EQgEMAD4kv

## 概要

長文脈LLMの鍵値キャッシュ（KV cache）は系列長に比例して増え、復号では各stepで大量の過去KVを読む。H2OやSnapKV等の削除方式は重要tokenを残すが、層ごとに注意分布が違うにもかかわらず、固定または単純なcache budgetを配ると限られた容量を有効に使えない。

CAKE（Cascading and Adaptive KV cache Eviction）はこの配分を「cake slicing」と捉え、各層の注意がどれだけ特定tokenへ集中するかという空間特性と、重要tokenが時間とともにどれだけ入れ替わるかという時間特性を測る。層別選好に応じて総cache budgetを分け、各層では時間変動に強い削除指標でtokenを残す。

LongBenchとNeedleBench、Llama 2/3.1、Mistral、Qwen 2.5、Gemma等で評価し、極端な条件では元KVの3.2%だけで性能を維持する。128K token文脈ではFlashAttention-2の全cache復号より10倍超のlatency高速化を報告する。

## 問題設定

一様budgetでは、注意が少数tokenへ集中する層にも、多数tokenを必要とする層にも同じ容量を与える。前者ではcacheを余らせ、後者では重要tokenを捨てる可能性がある。

さらに「過去の平均attentionが高いtoken」を残すだけでは、普段は低attentionでも特定時点で急に重要になるtokenを落としやすい。長い生成ではattention patternが時間的に移動するため、平均値だけの重要度は将来の必要性を表しきれない。

## 手法

### 層別選好の測定

CAKEはprompt prefill時のattentionから、各層の空間的な集中度と時間的な変動を集約する。集中度が高い層は少数tokenへattentionが偏るため少ないcacheでも情報を保ちやすく、広く分散する層にはより多いbudgetが必要になる。

時間変動が大きい層では、現在重要なtoken集合が将来変わりやすい。この性質もbudget配分へ反映し、単一の固定ratioを全層へ適用しない。

### 選好優先適応配分

総KV budgetを固定したまま、層別scoreを温度parameterで変換して各層のcache sizeへ割り当てる。実装では二つの温度parameterをgrid searchし、モデルごとの層特性へ適応する。

出力は各Transformer層が保持できるtoken数であり、その後の削除処理はこの層別budget内で行われる。総メモリ上限は守りつつ、必要度の高い層へcacheを移す。

### カスケードcache管理

prefillからdecodeへ進む際、cacheを層ごとに独立な固定箱として扱うのではなく、選好に沿ってカスケード状に管理する。上流で残すべきtoken情報と各層の容量を対応させ、限られた総budgetを層間で整合させる。

この構造により、層別budget計算とtoken削除が別々に暴走せず、全体メモリ制約の中で一貫したcache状態を維持する。

### attention-shift耐性のある削除指標

token scoreではattentionの平均だけでなく変動も考慮する。平均attentionが低くても変動が大きいtokenは将来急に重要になる可能性があるため、単純な累積attention方式より残しやすくする。

論文実装では観測windowを用いてprefill時に統計を作り、decode時にcacheを更新する。これにより「過去に常に重要だったtoken」と「一時的に重要度が上がるtoken」の両方を扱う。

## 評価条件

| 項目 | 内容 |
|---|---|
| モデル | Llama 2/3.1、Mistral、Qwen 2.5、Gemma等 |
| ベンチマーク | LongBench、NeedleBench |
| 比較 | StreamingLLM、H2O、TOVA、SnapKV、PyramidKV等 |
| 長文脈 | 最大128K token条件を含む |
| 実装 | FlashAttention-2との組合せを評価 |
| 指標 | task性能、cache保持率、復号latency、peak memory |

## 主要結果

| 条件 | 結果 | 解釈 |
|---|---:|---|
| 極小cache条件 | 元KVの3.2%でも高い性能を維持 | 層間budget再配分が低容量で有効 |
| LongBench/NeedleBench | 多数のbudgetで既存削除法を上回る | 単純な一様配分より層選好が重要 |
| 128K文脈 + FlashAttention-2 | 全cache比で復号latency 10倍超高速化 | KV読出し削減が長文脈ほど効く |
| peak memory | 全cache比で大幅削減 | token保持数削減が容量へ直接反映 |
| 4bit KV量子化との併用 | 追加圧縮可能 | token削除とbit圧縮が直交的 |

## 既存研究との差

H2O等はtoken単位の重要度を主に扱い、PyramidKV等は層ごとのbudget差を導入する。CAKEは層配分の根拠として注意の空間集中と時間変動を同時に使い、さらにtoken削除score側にも時間的なattention shiftを入れる。

SnapKV等と競合するだけでなく、量子化や他のcache圧縮と組み合わせられる。削除するtoken数の最適化と、残したKVのbit表現最適化を分離できるためである。

## 限界

CAKEの適応単位は主に層であり、同一層内のattention headごとの異質性までは十分に扱わない。論文自身もhead-level配分を将来課題として挙げる。

またattention統計の観測、層別budget計算、削除更新の追加処理が必要である。10倍超のlatency改善は128Kという長文脈かつ強いcache削減条件であり、短文脈やcacheが十分大きい条件では利得は小さくなる。

## 一次資料

- https://openreview.net/forum?id=EQgEMAD4kv
- https://arxiv.org/abs/2503.12491