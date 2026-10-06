---
canonical_id: "arXiv:2607.29591"
title: "ResKV: Reconstructing Omitted Attention Contributions for Fixed-Budget KV Cache Compression"
summary: "ResKVは固定KV予算を正確なmain cacheと、削除tokenのattention寄与を近似するresidual cacheへ分割する。residual entryは代表key/valueとpopulation countを持ち、mainと同一softmaxへ参加して分子・分母の両方の失われたmassを復元する。construction時のvalidation proxyとdecode時のdynamic gateでresidual量を適応させ、LongBenchの32/32、RULERの63/64表示条件で同一KV予算の基準を改善し、長文脈decode throughputとpeak memoryを維持する。"
list_summary: "削除KVを捨てず、代表key/valueと個数から残差注意機構 massを固定予算内で再構成し、main キャッシュと同じsoftmaxへ戻す。"
authors: ['Yuhang Zhan', 'Lisi Chen', 'Shuo Shang']
published: "2026-07-31"
publication: "arXiv"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2607.29591"
sources: ["https://arxiv.org/abs/2607.29591"]
implementation: "一次資料本文に基づき提案手法と評価を整理。 確認した一次資料から公式コードURLは特定できなかった。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2607.29591"
arxiv_categories:
  primary: "cs.CL"
  cross_list: []
worker_completed_at: "2026-10-06T19:30:00+09:00"
worker_run_key: "20261006-1900-scheduled-chat-00/r01"
reference_main_sha: "174b4002a423363e19f2224834cbb596437d38d6"
last_audited: null
audit_version: 0
---

## 概要

KVキャッシュ圧縮の追い出し方式は重要トークンだけを残すため高速だが、削除トークン群が持つ注意機構分子とsoftmax分母への総寄与を完全に失う。merge方式は情報を残せる一方、保持すべき正確なkey/valueへ削除情報を混ぜ、鋭い検索 peakを壊す可能性がある。

ResKVは固定予算をmain キャッシュとresidual キャッシュへ分ける。mainは選択トークンを元のkey/valueのまま保持し、residualは削除集合をcluster化した代表key/valueとpopulation countで表す。デコード時には両者を同じsoftmaxへ入れ、削除側の分子・分母massを近似的に復元する。LongBenchでは表示された32/32条件、RULERでは63/64条件で同予算比較対象を改善する。

## 問題設定

注意機構出力はsoftmax重み付きvalue和であり、トークン削除はvalueの分子寄与だけでなく正規化分母も消す。個々の注意機構が小さくても多数のトークンを削れば総massは無視できない。逆にそれらを重要トークンへmergeすると、後で一点検索したいexact メモリを変形してしまう。

## 手法

### main + residual予算

総slot数bをmain mとresidual rに分ける。mainはimportance スコアとrecent windowから選んだトークンをexactに保持し、残り集合Eだけをresidualへ要約するため、総persistent slot数は増えない。

### residual entry

削除トークンをkey空間でcluster化し、各clusterについて平均key、平均value、要素数cを保存する。問い合わせとの代表key logitへlog(c)を足すことで、そのclusterに含まれた複数トークンのsoftmax massを近似する。

### shared-softmax

residualは注意機構後の補正値として足すのではなく、main トークンと同じsoftmax分母へ参加する。これにより削除側のvalue寄与とnormalization massを同時に復元する。

### 適応制御

プリフィル後、validation 問い合わせで全体-キャッシュ 注意機構 出力との再構成誤差を測り、層/KV ヘッドごとにresidual予算rを選ぶ。residualがpure-mainより改善しない場合はr=0へ戻す。デコード時にはmain 注意機構が鋭い問い合わせでresidualを弱め、広い注意機構で強める動的 ゲートを使う。

## 評価条件

| 項目 | 内容 |
|---|---|
| ベンチマーク | LongBench、RULER |
| 設定 | 問い合わせ-aware / 問い合わせ-agnostic |
| 比較 | 追い出し・merge系KV圧縮比較対象 |
| 予算 | 同一retained KV slot budget |
| 指標 | タスク品質、peak メモリ、long-文脈 デコード スループット、再構成誤差 |

## 主要結果

同じKV予算でLongBenchの32/32表示構成、RULERの63/64表示構成を改善し、特に厳しいキャッシュ budgetや分散した文脈証拠を必要とするタスクで効果が大きい。residual slotはmain slotを置換するためpersistent キャッシュ footprintを増やさず、論文では追加メモリ オーバーヘッドが小さく長文脈スループットも安定すると報告する。

## 既存研究との差

H2O等の離散 追い出しは削除側を完全に失い、CaM/KVMerger等は削除情報を保持entryへ混ぜる。ResKVはexact mainを変更せず、削除側を独立residualとして同一softmaxへ戻す点が異なる。RESA等のpost-hoc補正とも、キャッシュ-常駐 entryとして分母まで復元する点が異なる。

## 限界

residualは将来問い合わせを知らない状態でkey-space clusterを作るため完全復元ではない。cluster構築とvalidation 代理指標のプリフィル後処理も追加コストになる。RULERでも1/64表示条件では比較対象改善にならず、すべてのタスクで無条件に優位ではない。

## 一次資料

- https://arxiv.org/abs/2607.29591