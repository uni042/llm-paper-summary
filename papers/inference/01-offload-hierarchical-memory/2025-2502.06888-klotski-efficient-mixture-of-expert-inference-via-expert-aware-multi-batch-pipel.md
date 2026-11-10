---
canonical_id: arXiv:2502.06888
arxiv_id: '2502.06888'
last_audited: '2026-10-08'
audit_version: 2
storage_targets: []
bottlenecks: []
hardware_details: null
quality_effect: null
evidence_locations: []
title: 'Klotski: Efficient Mixture-of-Expert Inference via Expert-Aware Multi-Batch Pipeline'
summary: 複数batchで共通して使われるexpertを先にGPUで計算し、その計算中にまだGPUにないexpertをCPU RAM / SSDから読み込むことで、巨大MoEのI/O待ちを隠す単一GPU向け推論system。
list_summary: 'Klotskiは複数バッチで共通する専門家を先に計算し、その間にCPU RAMやSSDから次の専門家を読み込んで巨大MoEのI/O待ちを隠す。'
authors_affiliations: Zhiyuan Fang, Yuegui Huang, Zicong Hong, Yufeng Lyu, Wuhui Chen, Yue Yu, Fan Yu, Zibin Zheng（SYSU/HKUST/Huawei/Peng Cheng Laboratory）
published: '2025-02-09'
publication_status: Published
lineage: オフロード／階層メモリ
topics:
- CPU offload
- SSD／NVMe offload
- Expert cache
- Expert prefetch
- Quantization
- Quality-cost
- Edge／on-device
importance: 高
hardware_evaluation: 実機
source: https://arxiv.org/abs/2502.06888
code: https://openi.pcl.ac.cn/fangzhy/Klotski
last_checked: '2026-09-11'
doi: null
openreview_id: null
arxiv_categories:
  primary: cs.LG
  cross_list:
  - cs.AI
authors:
- Zhiyuan Fang
- Yuegui Huang
- Zicong Hong
- Yufeng Lyu
- Wuhui Chen
- Yue Yu
- Fan Yu
- Zibin Zheng
publication: arXiv:2502.06888v1
publication_type: Preprint
sources:
- https://arxiv.org/abs/2502.06888
- https://arxiv.org/html/2502.06888v1
- https://openi.pcl.ac.cn/fangzhy/Klotski
implementation: 公式実装あり（https://openi.pcl.ac.cn/fangzhy/Klotski）。
implementation_status: official-code-available
references:
- canonical_id: arXiv:2303.08774
  arxiv_id: '2303.08774'
- canonical_id: arXiv:2401.06066
  arxiv_id: '2401.06066'
- canonical_id: arXiv:2405.04434
  arxiv_id: '2405.04434'
- canonical_id: arXiv:1810.04805
  arxiv_id: '1810.04805'
- canonical_id: arXiv:2310.18859
  arxiv_id: '2310.18859'
- canonical_id: arXiv:2312.17238
  arxiv_id: '2312.17238'
- canonical_id: arXiv:2210.17323
  arxiv_id: '2210.17323'
- canonical_id: arXiv:2401.08671
  arxiv_id: '2401.08671'
- canonical_id: arXiv:2308.12066
- canonical_id: arXiv:2401.04088
  arxiv_id: '2401.04088'
- canonical_id: arXiv:2402.07033
  arxiv_id: '2402.07033'
- canonical_id: arXiv:2310.02410
  arxiv_id: '2310.02410'
- canonical_id: arXiv:2006.16668
  arxiv_id: '2006.16668'
- canonical_id: arXiv:2401.15947
  arxiv_id: '2401.15947'
- canonical_id: arXiv:1609.07843
  arxiv_id: '1609.07843'
- canonical_id: arXiv:2104.07857
- canonical_id: arXiv:1701.06538
  arxiv_id: '1701.06538'
- canonical_id: arXiv:2303.06865
- canonical_id: arXiv:2312.11805
  arxiv_id: '2312.11805'
- canonical_id: arXiv:1910.03771
  arxiv_id: '1910.03771'
- canonical_id: arXiv:2309.17453
  arxiv_id: '2309.17453'
- canonical_id: arXiv:2401.08092
  arxiv_id: '2401.08092'
- canonical_id: arXiv:2403.01164
- canonical_id: arXiv:2402.01739
  arxiv_id: '2402.01739'
- canonical_id: arXiv:2401.14361
  arxiv_id: '2401.14361'
- canonical_id: arXiv:2205.01068
  arxiv_id: '2205.01068'
references_checked_at: '2026-09-11'
references_source: arxiv-html-reference-section
references_total: 47
under16kb_reaudit_target_path: papers/inference/01-offload-hierarchical-memory/2025-2502.06888-klotski-efficient-mixture-of-expert-inference-via-expert-aware-multi-batch-pipel.md
under16kb_reaudit_source_git_blob_sha: '926692c5631c2b729e1268f1273d8742f0528389'
under16kb_reaudit_version: '2026-10-07-v1'
under16kb_reaudit_passed: true
quality_self_review_passed: true
quality_self_review_version: '2026-10-07-v1'
worker_run_key: 'interactive-20261008-bottom-up-reaudit-klotski'

worker_completed_at: '2026-10-08T07:27:27+09:00'
---

# Klotski: Efficient Mixture-of-Expert Inference via Expert-Aware Multi-Batch Pipeline

> Klotskiは複数バッチで共通する専門家を先に計算し、その間にCPU RAMやSSDから次の専門家を読み込んで巨大MoEのI/O待ちを隠す。

## 概要
Klotskiは、GPU VRAMにエキスパート重みが収まらないMoEで、**複数バッチを同時に流してGPU計算時間を長くし、その間にCPU RAM / SSDから次エキスパートを読む**ことでGPUがI/Oを待つ時間を減らす推論engineである。

Dense LLMならバッチを増やすほど重み再利用が効きやすいが、MoEではバッチを増やすと選ばれるエキスパートの種類も増え、単純な複数バッチ化だけではI/O量も増える。Klotskiはこの問題に対し、複数バッチで共通して多く使われるエキスパートを先にGPUで計算し、その計算時間を**まだGPUにないエキスパートの先読み時間**として使う。

RTX 3090環境では実際のSSD（約1 GB/s読み出し）まで含めて評価しており、CPU DRAMだけのオフロードより階層が深い。

実RTX 3090＋2TB SSD（read約1 GB/s）でMixtral-8x22B（入力512・出力32、バッチ4〜64）を測定し、最大スループットはFlexGen比2.23倍（Accelerate比85.12倍など）を示した。これはSSD→RAM→GPUのパイプラインを含む比較であり、4-bit量子化やsparse 注意機構を有効にした場合の品質差は別に扱う必要がある。

## 手法のあらまし

Klotskiの主要な仕組みは、複数バッチをまとめて扱うこと、SSD→CPU→GPUの二段先読み、よく使われそうなエキスパートの予測、エキスパートの実行順変更である。

### 1. 複数batchを一つの実行単位として扱う

Klotskiはバッチを単純に大きくするのではなく、複数のバッチをまとめた **バッチ グループ** をパイプライン単位として扱う。

バッチ グループ内のバッチ数を`n`とすると、`n`を増やすほどGPU計算時間が長くなり、その裏で重み I/Oを隠しやすくなる。

一方で、

- 選ばれるエキスパート数が増えて読む重みも増える
- KVキャッシュが増える
- VRAM使用量が増える

ため、`n`は大きければよいわけではない。

実行前の測定結果を使うplannerは各層の計算時間とI/O時間を見て、**GPUがI/Oを待つ時間をほぼ隠せる最小の`n`**を選ぶ。

### 2. CPU RAMが十分な場合：1段先のweightをprefetchする

CPU RAMへモデル全体を保持できる場合は、GPUが層 `i`を計算している間に層 `i+1`で必要になるテンソルをCPU→GPUへプリフェッチする。

これは、片方のバッファを計算に使っている間にもう片方へ次データを用意する方式に近い。ただしMoEでは全エキスパートを読むのではなく、後述のエキスパート利用予測を使って優先順位を付ける。

### 3. CPU RAMも足りない場合：SSD→RAM→GPUを二段階で先読みする

CPU RAMには固定で`L` 層分程度の重みを保持し、同時に二つのプリフェッチを走らせる。論文ではこれを **two-levelプリフェッチ** と呼ぶ。

- GPU側：CPU RAMから近い将来の層を読む
- CPU側：SSDからさらに先の層をRAMへ読む

イメージとしては、GPUが`i+1`用重みをRAMから受け取っている間に、CPUがSSDから`i+L`用重みを先回りして読む。

これによりGPUが低速SSDを直接待つことを避け、**SSD → CPU RAM → GPU VRAM** の二段パイプラインを形成する。

### 4. 複数batchで多く使われそうなexpertだけ先に読む

複数バッチでは選ばれるエキスパート数が増えるため、全候補をプリフェッチすると帯域を使い切ってしまう。

そこでKlotskiは事前にエキスパート同士の利用関係を集計し、直前層のルーティング履歴から現在層で多く使われそうなエキスパートを予測する。

論文の主設定ではpath length `l=1`、つまり**直前層のエキスパート選択だけ**を主な予測信号に使う。

複数バッチのルーティング傾向を集約し、「バッチ グループ全体で多く使われそうなエキスパート」を先に読むことで、少数トークンしか使わないエキスパートのI/Oを後回しにする。

### 5. GPUにすでにあるexpertから先に計算する

通常のルーティング順どおりに計算するのではなく、Klotskiは**GPUにすでにあるエキスパートを先に計算**する。

その計算中に、まだGPUにないエキスパートをCPU / SSDからtransferする。

つまり実行順を、

`routing順` ではなく `I/Oを隠しやすい順`

へ並べ替える。

エキスパート 出力は最終的に元のトークン位置へ戻すため、計算順変更自体はモデル qualityを変えない。

### 6. WeightとKVの転送を別々に進める

実装では少なくとも次の4本のCUDAストリームを用途別に使う。

| Stream | 役割 |
|---|---|
| Weight プリフェッチ | 次重みをCPU→GPUへ読む |
| Expert transfer | gate確定後の必要専門家を補う |
| KV プリフェッチ | 次micro/バッチ用KVを用意 |
| KV save | 計算済みKVを保存 |

重みとKVを同じcopy queueに詰めず、依存しないI/Oを同時進行させる。

### 7. 量子化とsparse attentionは別の追加最適化

Klotskiは4-bit HQQで重み transfer量を減らす構成や、StreamingLLM型のsparse 注意機構で複数バッチ時のKVキャッシュを抑える構成も評価する。

ただしこれらはパイプラインそのものとは別の最適化である。

- HQQ → 重みを低bit化して転送バイト数を減らす
- sparse 注意機構 → 保持するKV容量を減らす
- Klotskiパイプライン → I/O待ちをGPU計算と同時進行させる

と役割を分けて読む必要がある。

## 評価

### まず見るところ
- **結論:** 複数バッチで共通して使われるエキスパートの計算をI/O待ちを隠す時間として使うと、CPU RAMだけでなく実SSDまで含むオフロードでも巨大MoEを単一GPUで動かせる。
- **実速度:** Mixtral-8x22BをRTX 3090で1.3トークン/s超、H800で約53トークン/sまで引き上げる構成要素比較を示す。
- **品質:** パイプライン/キャッシュ/プリフェッチ自体は無損失。4-bit量子化やsparse 注意機構を有効化した場合は別のquality trade-offがある。
- **メモリ・I/O:** **RTX 3090環境では実SSD 1 GB/sを使用**し、SSD→RAM→GPUの二段プリフェッチを評価。
- **注意点:** バッチ グループを増やすとKVキャッシュが膨らむため、I/Oを隠せる時間とVRAM消費のtrade-offが強い。

<details>
<summary>評価条件・詳細な数値を開く</summary>

### 実機環境

| 環境 | GPU | CPU / RAM | PCIe | SSD |
|---|---|---|---|---|
| Environment 1 | RTX 3090 24 GB | Xeon Gold 5318Y / 256 GB | Gen4 x16 | 2 TB、read約1 GB/s |
| Environment 2 | H800 80 GB | Xeon Platinum 8470 / 800 GB | Gen5 x16 | 1 TB、主結果ではRAM十分 |

Environment 1が、一般的なGPU + CPU RAM + SSD階層に近い実測条件。

### 評価model

| Model | 総パラメータ規模 | Precision |
|---|---:|---|
| Mixtral-8x7B | 約46.7B | BF16 / 必要に応じた量子化 |
| Mixtral-8x22B | 約141B | BF16 / 必要に応じた量子化 |

主条件は入力 512、出力 32、バッチ 4〜64。

### 比較対象

| Baseline | 特徴 |
|---|---|
| Hugging Face Accelerate | 一般的オフロード |
| DeepSpeed-FastGen | 推論提供 ランタイム |
| FlexGen | 複数バッチ階層オフロード |
| MoE-Infinity | ルーティング履歴を使う専門家 キャッシュ |
| Fiddler | CPU/GPU 専門家 execution切替 |

### 最大処理量改善

| 比較対象 | 最大高速化倍率 |
|---|---:|
| Accelerate | **85.12倍** |
| FastGen | **15.45倍** |
| FlexGen | **2.23倍** |
| MoE-Infinity | **19.06倍** |
| Fiddler | **9.53倍** |

非常に大きな倍率は、一部比較対象が巨大22B MoEのSSD / low-メモリ条件でほぼI/Oを待ち続けていることも含む。通常のGPU-常駐推論に対する85倍高速化という意味ではない。

### RTX 3090 / Mixtral-8x22Bでの構成要素ごとの効果

| 構成 | 処理量 |
|---|---:|
| 単純なパイプライン | 0.01 トークン/s |
| + 複数バッチ | 0.97 |
| + 利用専門家予測プリフェッチ | 1.127 |
| + 専門家順序調整 | **1.325** |
| + Quantization | **1.366** |

最大の改善は複数バッチ化で、**GPU計算を長くしてSSD / CPU I/Oを隠す時間を作ること**がまず重要だと分かる。その後エキスパート予測と実行順序が上積みする。

### H800 / Mixtral-8x22Bでの構成要素ごとの効果

| 構成 | 処理量 |
|---|---:|
| 単純なパイプライン | 1.149 トークン/s |
| + 複数バッチ | 34.07 |
| + 利用専門家予測プリフェッチ | 44.17 |
| + 専門家順序調整 | 52.85 |
| + Quantization | **53.125** |

H800ではCPU RAMが十分でdiskが主ボトルネックではないため、主にCPU↔GPUパイプラインとエキスパートを考慮した実行順の効果を見る結果になる。

### 専門家予測精度

論文では複数の予測指標を報告する。

| 指標 | 値 |
|---|---:|
| Layer内で必要専門家を先読み候補のどこかに含めた率 | 100% |
| Single 系列平均 | 42.24% |
| 優先して先読みする専門家の選択精度 | 58.89% |

`100%`だけを見ると完全予測に見えるが、これは広い候補集合のどこかに必要エキスパートを含めた指標である。実際に優先プリフェッチするエキスパートの精度は約59%であり、指標を分けて読む必要がある。

### GPUメモリ削減

| 条件 | Memory削減 |
|---|---:|
| ほぼ全テンソル オフロード | 94.1%以上 |
| 3090級の実用設定 | 約74.5%削減と報告 |

メモリを減らすほどI/O量は増えるため、スループットとセットで評価する必要がある。

### Large batch

バッチ 128でもFlexGenより約15%高いスループットを報告する。ただしバッチ グループを増やすとKVキャッシュが増加し、Fiddler / MoE-Infinityは22Bでbatch16付近が上限になった条件もある。

### 評価上の制約

- SSD性能はEnvironment 1の約1 GB/sに依存する。
- Environment 2はCPU RAMが十分で、disk I/O評価とは性質が違う。
- エキスパート利用関係の表は事前に作る必要がある。
- ルーティング patternが変わるとエキスパート予測が外れ得る。
- バッチ グループを大きくするとKVキャッシュ OOMが起こる。
- HQQ / sparse 注意機構を使う場合、パイプラインとは別の品質影響がある。
- 実装はPyTorch + Hugging Face + FlexGen上の研究prototypeで、version差に注意が必要。

</details>

### 階層記憶でのボトルネックと速度評価の読み方

Klotskiの評価では、重みをGPUに全量置けない大規模MoEで、どの程度の時間をCPUメモリや補助記憶からの専門家転送に費やすかが重要である。特にRTX 3090環境では実際の読み出し速度が約毎秒一ギガバイトのSSDを使用しており、CPUメモリだけを使う理想的な退避とは条件が異なる。複数の要求をまとめて処理することにより、共通して必要な専門家を再利用でき、GPU演算を行っている時間へ次の層の読み込みを重ねられる。一方で要求を増やし過ぎるとキー・値キャッシュが増え、GPUに残せる専門家数が減るため、単純にバッチ数を最大化すればよいという結果ではない。

Mixtral-8x22BのRTX 3090での構成要素除去実験では、単純なパイプラインだけの場合に毎秒〇・〇一トークンだったものが、複数バッチの処理を加えると毎秒〇・九七トークンになる。その後、専門家の先読み予測を加えると一・一二七、処理順序を並べ替えると一・三二五、量子化も加えると一・三六六になる。基礎の単純な実行からの改善の大半は、バッチ処理で転送の待機時間を隠すことによる。量子化の追加が全体改善の中心だと解釈してはいけない。また量子化後の品質は完全な高精度重みと同じとは限らないため、パイプライン部分の品質保持と量子化の品質損失は別に扱う。

H800環境では同じ巨大MoEに対し、単純なパイプラインの毎秒一・一四九トークンから、複数バッチ化後の三四・〇七、先読み後の四四・一七、専門家順序最適化後の五二・八五まで上昇する。GPU容量やホストメモリ容量が異なるため、これらの値はRTX 3090と同条件の速度比較ではない。評価の「最大八五倍」など非常に大きな倍率は、比較対象がストレージ入出力待ちで極端に遅い条件を含む。完全GPU常駐のモデルに対して数十倍速いという意味ではなく、多階層の重み移動を要する状況でこそ有効という証拠である。従って利用者の環境への移植にはPCIe帯域、SSD転送速度、ホストメモリ量、KVキャッシュ容量の各制約を別々に再測定すべきである。

## 引用経路
FreeTokenの参考文献[91]から抽出。

## 一次資料
- [論文](https://arxiv.org/abs/2502.06888)
- [公式コード](https://openi.pcl.ac.cn/fangzhy/Klotski)

## 登録履歴
- 2026-09-07: hot/coldエキスパート、I/O バブル、two-levelプリフェッチ、エキスパート-aware execution、ablation、cover等を具体的な実行順・データ転送へ言い換え。
- 2026-09-02: 登録済み論文の参考文献調査から新規登録。
- 2026-09-04: バッチ グループ / two-levelプリフェッチ / エキスパート-aware execution order等を補足し、詳細評価を表形式へ整理。

- 2026-10-08: 一次資料を照合し、末尾起点の再監査に基づく評価条件、比較群、限界の日本語説明を増補。
