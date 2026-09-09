---
canonical_id: "arXiv:2608.23658"
arxiv_id: "2608.23658"
title: "Elastic KV Cache for LLM Serving: A Working Reclamation Mechanism, and Why Chunked Prefill Already Closes the Gap"
summary: "vLLMは大きなprefillに備えて一時activation用GPUメモリを常時予約するため、decode中はその領域が遊ぶ。Elastic KV CacheはCUDA仮想メモリを使い、decode中だけその予約領域をKV cacheへ貸し、prefill直前に返す機構を実装する。しかし実験ではprefill chunkを小さくする単純設定でもほぼ同じTTFTでより多くKVを確保でき、複雑なelastic機構の実用上の優位を見つけられなかったというnegative resultが中心。"
source: "https://arxiv.org/abs/2608.23658"
last_audited: "2026-09-09"
audit_version: 1
---

# Elastic KV Cache for LLM Serving: A Working Reclamation Mechanism, and Why Chunked Prefill Already Closes the Gap

> vLLMは大きなprefillに備えて一時activation用GPUメモリを常時予約するため、decode中はその領域が遊ぶ。Elastic KV CacheはCUDA仮想メモリを使い、decode中だけその予約領域をKV cacheへ貸し、prefill直前に返す機構を実装する。しかし実験ではprefill chunkを小さくする単純設定でもほぼ同じTTFTでより多くKVを確保でき、複雑なelastic機構の実用上の優位を見つけられなかったというnegative resultが中心。

## 書誌情報

- **著者**: Sathishkumar Sivashanmugam
- **公開**: 2026-08-24, arXiv v1
- **種別**: プレプリント（preprint）
- **主題**: KVキャッシュ容量、入力処理（prefill）、CUDA仮想メモリ管理（CUDA Virtual Memory Management; VMM）、vLLM、メモリ再利用
- **実装**: userspace CUDA VMM、PyTorch pluggable allocator、KV block-pool gate、scheduler controllerとして実装。attention kernelやGPU driverのpatchは不要。

## 概要

この論文は、提案機構そのものよりも**「複雑な仕組みを作って正しく動かしたが、もっと単純な既存設定がほぼ同じ問題を解いていた」**というnegative resultが重要な研究である。

LLM servingではGPUメモリの大部分を、

- モデル重み
- KVキャッシュ（KV cache）
- 一時activation

が取り合う。

KVキャッシュを多く置けるほど、より多くのrequest・より長いcontextを同時にdecodeできる。一方、長い入力をprefillするときは巨大なactivationが一時的に必要になる。

vLLMは安全にprefillできるよう、起動時に最大級prefillで必要になるactivation領域を見積もり、その分を**常時KV poolから差し引いて予約**する。

問題は、decode-only時間にはその大きなactivation workspaceを使わないことである。chat servingでは長い時間decodeだけが続くため、「使っていない予約メモリをその間だけKV cacheへ貸せないか」という発想が自然に出る。

Elastic KV Cacheはこれを実際に実装する。

しかし著者が比較すると、vLLMの`max_num_batched_tokens`を小さくし、prefillを小さなchunkへ分割するだけでactivation peak自体を小さくできる。結果として、elasticに貸し借りするより**最初から小さいreserveにする方が簡単で、KV容量も大きく、TTFT悪化も約1%しかない**条件が見つかる。

したがって論文の結論は「Elastic KV Cacheを導入すべき」ではなく、「mechanismは成立するが、現在のvLLMではsimple chunked prefillが強いbaselineなので、elastic memory sharingが本当に必要なregimeは狭い」というものになる。

## 問題設定

### Prefillとdecodeでは必要メモリの種類が違う

入力処理（prefill）では、prompt中の多数tokenをまとめてTransformerへ通す。

このとき各layerで大きな行列演算を行うため、一時的な中間activationが増える。prompt chunkが大きいほどactivation peakも大きくなりやすい。

一方、逐次生成（decode）では各requestにつき1stepで1token程度しか増えないため、prefillほど大きな一時activationは要らない。その代わり、多数requestの長い履歴を保持するKV cacheが大きくなる。

つまり理想的には、

- prefill時: activationへ多め
- decode時: KV cacheへ多め

とGPU memoryの用途を時間で変えたい。

### なぜvLLMは最初から全部KVへ使わないのか

もしdecode時の空きだけ見てKVを最大化すると、突然大きなprefill requestが来たときactivationを置く場所がなくなり、OOMになる。

そこでvLLMは起動時profilingで最大activation peakを見積もり、常にその余白を残す。

これは安全だが、decode-only期間には予約領域がidleになる。

論文のQwen2.5-7B / A100 40GB例では、prefill chunk sizeを2048から32768へ大きくするとKV capacityが約366K tokenから308K tokenへ減り、約3.1 GiB級のactivation reserveが生じる。

## 手法のあらまし

Elastic KV Cacheは、GPU上のKV bufferに**大きな連続仮想アドレス範囲**を最初から確保しておく。

その仮想範囲を、

- 常に物理メモリが割り当てられているbase部分
- decode中だけ追加で物理メモリを割り当てるelastic部分

に分ける。

attention kernelからは一つの連続KV bufferに見えるが、裏側ではelastic部分だけをmap/unmapできる。

schedulerは次のbatchがdecode-onlyならelastic memoryをcommitしてKV block poolを増やす。prefillが来る直前には、そのKV blockを使っているrequestがないことを確認してpoolから外し、物理memory mappingを解除してactivationへ返す。

この仕組み自体は正しく動作し、大きなprefill前にmemoryを返せばOOMを避けられる。

## 手法

### 1. CUDA VMM — 仮想アドレスと物理GPUメモリを分離する

通常の`cudaMalloc`では、あるpointerへ割り当てた物理メモリを途中から部分的に増減するのは扱いにくい。

CUDA Virtual Memory Management（VMM）はOSの仮想メモリに近く、まず大きな**仮想アドレス範囲**を予約し、その一部へ後から物理メモリhandleをmapできる。

Elastic KV Cacheは、各layerのKV領域について

```text
[ base KV | elastic KV ]
```

という連続virtual rangeを予約する。

base部分は常時mapし、elastic部分だけをdecode/prefill状態に応じて追加・解除する。

### 2. なぜkernelを変更しなくてよいのか

物理的にはelastic領域が存在したり消えたりするが、仮想アドレス上ではKV bufferの位置は変わらない。

attention kernelは従来どおり「このbase pointerからblock id分進んだ場所」にアクセスするだけでよい。

つまりmemory allocatorとscheduler側でelasticityを実現し、attention kernelへ特殊なpage faultや分岐を入れない**kernel-transparent**な設計である。

### 3. Commit — decode中に空きreserveをKVへ貸す

次のbatchがdecode-onlyだとschedulerが分かれば、elastic部分へ物理GPU memoryをmapする。

その後、新しく使えるKV block IDをblock poolへ追加する。

これで通常ならactivation reserveとして遊んでいた領域へ、追加requestのKVを格納できる。

### 4. Decommit — prefill前にKV blockを回収する

prefillが来る前にはelastic memoryをactivationへ返す必要がある。

しかしelastic KV blockをまだrequestが使っている状態でunmapすれば破壊的になる。

そこでcontrollerは、まずelastic blockを新規allocation対象から外し、既存使用分がなくなるまで**drain**する。その後物理mappingを解除する。

これによりattention kernelから見て無効なKV pointerを踏むことを防ぐ。

### 5. Schedulerが1step先を知ることを利用する

LLM schedulerは次batchを組む時点で、

- decode tokenだけを処理するのか
- 新しいprefillを含むのか

を知っている。

Elastic KV Cacheはこの情報を使い、decode-onlyならcommit、prefill直前ならdecommitする。

完全に予測不能な将来を当てるのではなく、**schedulerがすでに持っている次step情報**でmemory stateを切り替える。

### 6. Static overcommitが危険であることを実証する

「decodeで使えるなら、reserveを最初からKVへ足しておけばいい」とすると、prefillが来た瞬間OOMになる。

論文ではreserve全量をstaticにKVへ足すとKV capacityが約314K→370K tokenへ増える一方、62K-token prefill burstで約2.3 GiBのactivationが必要になりOOMする。

Dynamic toggleならprefill前にelastic部分を数msでdecommitし、このburstを完走する。

したがってmechanismの正しさ自体は確認されている。

## ここからが論文の重要なnegative result

### 7. Prefill chunkを小さくすると、そもそもreserveが小さくなる

vLLMは長いpromptを一度に全部prefillせず、小さなchunkへ分けて処理できる。

例えば32K tokenを一度に処理するより、8Kずつ4回に分ければ、1回に必要なactivation peakは小さくなる。

activation reserveも小さくできるので、起動時からより多くGPU memoryをKV cacheへ割り当てられる。

この方法はVMM commit/decommit、block draining、controller logicを追加しない。単なるscheduler parameterである。

### 8. 「小さいchunkはTTFTを大きく悪化させる」という前提を実測する

chunkを小さくすればprefill kernelの起動回数は増え、background decodeと交互実行する回数も増えるため、TTFTが悪化しそうに見える。

ところが実測では8192-token chunkと32768-token chunkのmedian TTFT差は約1%しかなかった。

理由として論文は、prefillがcompute-boundで総FLOPs自体は大きく変わらず、background decodeが使うtoken budgetも小さいため、chunk間へdecodeを挟むhead-of-line penaltyが想定ほど大きくないことを挙げる。

## 評価

### まず見るところ

- **mechanism**: CUDA VMMでactivation reserveをKVへ安全に貸し借りできることは実証。
- **切替cost**: 3.09 GiB / 28 layersでdecommit 3.8 ms、recommit 23.8 ms。
- **安全性**: static overcommitは長いprefillでOOM、dynamic toggleは完走。
- **しかし**: chunk 8192の方がElastic 32768よりKV capacityが大きく、median TTFT差も約1%。
- **結論**: 評価範囲ではElasticがsimple chunk reductionを上回る構成を見つけられない。
- **価値**: working mechanismと同じくらい、複雑なoptimizationが不要だったことを示すnegative resultが重要。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### 環境

- NVIDIA A100-SXM4 40GB
- Qwen2.5-7B-Instruct FP16
- vLLM 0.23.0
- `gpu_memory_utilization=0.9`
- `max_model_len=32768`

### VMM toggle cost

3.09 GiB / 28 layersのlive controllerで

- decommit: **3.8 ms**
- recommit: **23.8 ms**

### Static overcommitとの比較

reserve全量をKVへ固定追加するとcapacityは約314K→370K tokenへ増えるが、62K-token prefill burstで約2.3 GiB activationが必要になりOOM。

Dynamic Elasticはprefill直前に約4.4 msでdecommitし同burstを完走する。

### 決定的なTTFT/KV比較

40 background decode sequences中へ約25K-token promptを6本投入する。

| Mode | median TTFT | max TTFT | KV capacity |
|---|---:|---:|---:|
| chunk 8192 | 4.97 s | 6.07 s | 375K |
| chunk 32768 | 4.91 s | 5.79 s | 314K |
| Elastic 32768 | 4.90 s | 5.76 s | 364K |

Elastic 32768はlarge chunkのlatencyを保ちながらKVを増やすが、small chunk 8192は**より多い375K capacity**を持ち、median TTFTは約1%しか遅くない。

### Decode-only時間は本当に長い

workload別のdecode-only比率は

- chat: **95〜97%**
- bursty: **72〜97%**
- long-context: **90〜99.8%**

で、時間貸しできる期間自体は十分ある。

### Tensor parallelismでopportunityが薄まる

activation reserve比率は例として

- 7B TP1: **16%**
- 32B TP4: **7.7%**
- 7B TP4: **2.7%**

へ低下する。

TPでmodelを分割すると1 GPUあたりのactivation reserveの相対価値が小さくなり、elasticityの利益も減る。

</details>

## 主要結果の読み方

この論文は「動的memory reclamationは失敗した」という単純な話ではない。

技術的には、

- kernelを変えず
- CUDA VMMだけで
- decode中はKV capacityを増やし
- prefill前に安全に回収し
- CUDA graphやprefix cachingと共存する

mechanismを作れている。

しかしsystem研究では、**機構が動くことと、それが最善の設計であることは別**である。

Elastic KV Cacheが解こうとした問題は「large prefillに備えたreserveがdecode中に遊ぶ」ことだった。ところがprefill chunkを小さくすればreserve自体を小さくできる。

そのsimple baselineがほぼlatency penaltyなしでより多くKVを確保できたため、少なくとも評価環境では複雑な貸し借りmechanismを導入する理由が弱くなった。

このnegative resultは重要で、今後似たmemory sharing機構を提案する研究は、**chunked prefillのような既存parameter tuningを強いbaselineとして比較すべき**ことを示す。

## 品質への影響

KV内容やattention計算は変更しない。

論文はtoggle前後でbit-identical generationを確認しており、mechanism自体にmodel品質trade-offはない。

riskは品質ではなく、memory回収タイミングを誤って使用中blockをunmapするようなsystem correctness側にあるため、block drainとpool gateが重要になる。

## 既存研究との差

- **vAttention**: driver patchを使ったUVM demand paging等でKV memoryを仮想化する。Elastic KV Cacheはuserspace CUDA VMMでactivation reserveとKV poolを時間共有する。
- **Jenga等のKV sizing**: 固定memory budget内でKV allocationを調整する。Elasticは同じ物理memoryの用途をprefill/decode phaseで切り替える。
- **Chunked prefill**: 本来はserving fairness/latency等のためのscheduler機構だが、activation peak削減というmemory効果が強く、Elasticの直接baselineになる。

## 限界

- 主評価はA100 40GB、Qwen2.5-7B、vLLM 0.23.0中心。
- H100/B200、別model、別serving engineではactivation/KV比率が異なり結論が変わり得る。
- memory-bound prefillではsmall chunkの性能penaltyが大きくなり、Elasticが有利になる可能性が残る。
- Tensor parallelismでreserve比率が小さくなり、elastic opportunityも縮小する。
- VMM remap costやfragmentation特性はGPU/driver世代に依存する。
- 論文の評価範囲ではsimple chunk reductionを上回るregimeを発見できていないため、production導入を支持する性能証拠は弱い。

## 一般的な実装上の含意

この研究から最も一般化しやすい教訓は、**新しい動的mechanismを作る前に、静的parameterを変えるだけで同じ資源不足を解消できないか確認する**ことである。

LLM servingのmemory問題では、

1. 本当に使われていないmemoryがあるか
2. そのreserveがなぜ必要なのか
3. workload parameterを変えればreserve自体を減らせないか
4. dynamic reclamationの切替costはいくらか
5. simple baselineよりcapacity / latency / reliabilityで明確に勝つか

を順に見るべきである。

またnegative resultを残す価値も大きい。機構が正しく動くところまで実装したうえで「現状では不要」と示せば、後続研究が同じ複雑化を繰り返すのを防げる。

## 一次資料

- arXiv: https://arxiv.org/abs/2608.23658
- PDF: https://arxiv.org/pdf/2608.23658

## 更新履歴

- 2026-09-09: MoE-Infinity基準に合わせて全面改稿。prefill activation reserve、CUDA VMM、commit/decommit、安全なdrain、chunked prefillとの比較、negative resultの意味を論文未読者向けに説明。
