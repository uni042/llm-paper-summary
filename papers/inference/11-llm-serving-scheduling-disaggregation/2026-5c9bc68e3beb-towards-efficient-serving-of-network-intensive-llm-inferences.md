---
canonical_id: DOI:10.1145/3820441.3820479
doi: 10.1145/3820441.3820479
title: Towards Efficient Serving of Network-intensive LLM Inferences
summary: 分散KVキャッシュの読込み中に計算スケジューラが要求を止め、通信費用を無視して処理順を決める既存LLMエンジンの問題に対し、SanicはvLLM上で各キャッシュ移送段階に独立dispatcher/executorを置き、ネットワーク転送・PCIe転送・プリフィル計算をデータ依存関係に沿って非同期に重ねる。さらに、オフライン測定からリモートKV読込み時間とクエリ計算時間を別々に推定し、平均TTFT向けSJFとTTFT期限向けLSTFで要求を並べ替える。vLLM 0.9.1とLMCache 0.3.1を基礎に3.3K行を実装し、単一GPUノードと別のリモートCPUメモリノードを結ぶ400 Gbps RDMA環境で長文脈データセットを評価した。ICLを1.2 QPSで処理する条件では平均TTFTをvLLM-LMCache比で81.3%超短縮し、同QPSのTTFT SLO達成率は61.67%高かったと報告する。これは選定モデル・データ・単一サーバ構成でのシステム測定であり、著者らは相関したエージェント要求の協調と本番Mooncakeへの適用を将来課題に挙げる。
list_summary: 分散KV読込みを独立段階としてvLLMのプリフィル計算と非同期に重ね、読込み遅延も考慮したSJF/LSTFで要求を順序付けるSanicを実装。単一GPUノード・400 Gbps RDMA構成の長文脈評価で、ICL 1.2 QPS時にvLLM-LMCache比で平均TTFTを81.3%超短縮し、TTFT SLO達成率を61.67%改善したと報告する。
authors:
- Weiye Wang
- Chen Chen
- Junxue Zhang
- Zhusheng Wang
- Hui Yuan
- Zi-Ting Guan
- Xiaolong Zheng
- Qizhen Weng
- Yin Chen
- Minyi Guo
published: 2026-08
publication: The 10th Asia-Pacific Workshop on Networking (APNet ’26), Singapore, August 6–7, 2026
publication_type: ワークショップ論文
publication_status: APNet ’26 proceedingsに掲載。著者配布PDFにACM DOIと2026年8月のISBN情報を記載。
source: https://doi.org/10.1145/3820441.3820479
sources:
- https://doi.org/10.1145/3820441.3820479
- https://snowzjx.me/assets/sanic-apnet26.pdf
- https://conferences.sigcomm.org/events/apnet2026/accept.php
implementation: SanicをvLLM 0.9.1、LMCache 0.3.1上へ約3.3K行で実装。L3のMooncake StoreからL2のローカルCPU DRAMを経てL1のGPU HBMへKVを移し、L3→L2およびL2→L1読込み用dispatcher/executor、vLLMの計算スケジューラ、ZeroMQによるプロセス間通知を使用する。公式コードURLは一次資料で確認できない。
code: null
last_checked: '2026-10-04'
worker_completed_at: '2026-10-04T17:10:00+09:00'
worker_run_key: 20261004-1830-codex-local-r21
last_audited: null
audit_version: 0
references:
- canonical_id: arXiv:2502.15734
  doi: 10.48550/arxiv.2502.15734
- canonical_id: arXiv:2406.11612
  arxiv_id: '2406.11612'
  doi: 10.48550/arxiv.2406.11612
- canonical_id: DOI:10.1287/opre.33.5.1035
  doi: 10.1287/opre.33.5.1035
- canonical_id: DOI:10.1145/3731569.3764834
  doi: 10.1145/3731569.3764834
- canonical_id: DOI:10.1007/s11023-020-09548-1
  doi: 10.1007/s11023-020-09548-1
- canonical_id: DOI:10.1145/3575693.3575721
  doi: 10.1145/3575693.3575721
- canonical_id: DOI:10.1145/3611643.3617850
  doi: 10.1145/3611643.3617850
- canonical_id: arXiv:2407.02490
  doi: 10.52202/079017-1663
- canonical_id: DOI:10.1145/3600006.3613165
  doi: 10.1145/3600006.3613165
- canonical_id: DOI:10.18653/v1/2024.acl-long.859
  doi: 10.18653/v1/2024.acl-long.859
- canonical_id: DOI:10.1145/3604237.3626869
  doi: 10.1145/3604237.3626869
- canonical_id: arXiv:2405.19888
- canonical_id: DOI:10.1145/321738.321743
  doi: 10.1145/321738.321743
- canonical_id: arXiv:2404.16283
- canonical_id: DOI:10.1145/3651890.3672274
  doi: 10.1145/3651890.3672274
- canonical_id: DOI:10.2139/ssrn.5179390
  doi: 10.2139/ssrn.5179390
- canonical_id: arXiv:2407.00079
- canonical_id: arXiv:2503.24047
  arxiv_id: '2503.24047'
- canonical_id: DOI:10.1109/5.476077
  doi: 10.1109/5.476077
- canonical_id: arXiv:2302.13971
  arxiv_id: '2302.13971'
- canonical_id: DOI:10.52202/079017-2000
  doi: 10.52202/079017-2000
- canonical_id: arXiv:2401.09670
- canonical_id: DOI:10.18653/v1/2025.acl-long.1245
  doi: 10.18653/v1/2025.acl-long.1245
references_checked_at: '2026-10-04'
references_source: crossref-deposited-reference-metadata
references_total: 31
---

# Towards Efficient Serving of Network-intensive LLM Inferences

## 概要

長い共通コンテキストを持つ要求では、過去に計算した接頭辞のKVキャッシュを別サーバから再利用することでプリフィル再計算を減らせる。しかし、キャッシュが遠隔サーバにあるとネットワーク転送・ローカルCPUメモリ・PCIe転送を経てGPUへ載るまで計算を開始できない。Wangらは、この読込みをLLMエンジンの計算スケジューラが従属的に制御し、処理順もKV転送遅延を知らずに決めることが、長文脈・高キャッシュ命中のservingで資源遊休と待ち時間を生むと指摘する。

SanicはvLLMに非同期のKV読込みdispatcher/executorを加え、リモートDRAM→ローカルDRAM→GPU HBMの各段階をデータの準備と宛先容量の確保に応じて自律的に進める。別のオフライン・プロファイルで推定する読込み時間とプリフィル計算時間を合算したサービス費用を、平均TTFT向けSJFまたは期限遵守向けLSTFの要求優先度に使う。実機構成を用いた評価では、読込みが単一リクエストのTTFTの90%超になるケース、ICLを1.2 QPSで処理するときの平均TTFT 81.3%超の短縮、同条件でのSLO達成率61.67%向上などを報告する。

## 書誌情報

- **著者**: Weiye Wang、Chen Chen（責任著者）、Junxue Zhang、Zhusheng Wang、Hui Yuan、Zi-Ting Guan、Xiaolong Zheng、Qizhen Weng、Yin Chen、Minyi Guo。
- **一次資料に記載された所属**: Shanghai Jiao Tong University、University of Science and Technology of China、Huawei、Institute of Artificial Intelligence (TeleAI), China Telecom。
- **出版**: The 10th Asia-Pacific Workshop on Networking (APNet ’26)、Singapore、2026年8月6–7日。PDFは7ページ、ACM DOI 10.1145/3820441.3820479、ACM ISBN 979-8-4007-2664-4/26/08を記載する。
- **実装状況**: vLLM 0.9.1、LMCache 0.3.1上の3.3K行のSanic実装。著者PDFにGitHub等のコードURLは記載されていないため、公開実装は確認できない。
- **一次資料**: [DOI](https://doi.org/10.1145/3820441.3820479)、[著者配布PDF](https://snowzjx.me/assets/sanic-apnet26.pdf)、[APNet ’26 accepted papers](https://conferences.sigcomm.org/events/apnet2026/accept.php)。

## 問題設定と律速

本論文が主に扱うのはプリフィル段階のTTFTである。共有プレフィックスが再利用できると、長い静的コンテキストのKVを再計算せずに済む一方、要求に必要なKVブロックをGPUへ搬入する時間が支配的になる。論文は、LooGLEをLlama-3.1-8Bで処理し分散KV poolと400 Gbps接続を使う経験測定で、KV読込み時間がTTFTの90%を超える場合があると報告する（§1）。

図1の既存vLLM＋LMCacheの流れでは、要求はFIFO待ち行列に入り、計算スケジューラが読込みと実行を一括して進める。まずKVを遠隔DRAM（L3）からノード内CPU DRAM（L2）、さらにGPU HBM（L1）へ送り、必要量がそろってからGPUプリフィルを始める。遠隔通信待ちの間、別要求が利用できるはずのネットワーク・PCIe・GPU資源も制御上すぐ再利用できず、異なる資源段階に空きが生じる。加えて、FIFOや計算トークン数だけを見るSJFでは、KV読込みが長い要求を先に実行して平均TTFTを悪化させることがある（§2.3、図3–4）。

論文中の二要求例では、先着R1が読込み0.361秒・計算0.019秒、R2が読込み0.199秒・計算0.025秒を要する。FIFOまたは計算時間のみのSJFはR1を先に選び、例の平均TTFTは0.49秒となるが、読込みと計算を合わせたSJFでR2を先にすると0.41秒となる（§2.3.2）。これは二要求の説明例であり、集約ベンチマーク値ではない。

## 手法

### L3→L2→L1の非同期ステージ制御

SanicはvLLM スケジューラ、コンテキスト管理、優先度推定器に加え、L3→L2とL2→L1の読込み段階それぞれにdispatcherとexecutorを置く（図5、§3.1）。dispatcherは優先度の高い要求に属する転送可能ブロックがあり、宛先メモリが確保されている間、対応executorに読込みを発行する。あるブロックの転送完了は上流側executorへ通知し、ブロック単位に段階を重ねる。要求で必要なKVブロックがL1にそろうとプリフィルを開始するため、一要求の全キャッシュ搬入が終わるまでGPUを待たせない。

容量依存を保ったままパイプラインを止めないため、下流の読込みdispatcherは高位メモリの確保を先行して要求する。具体的にはL3→L2転送を発行するときに、L2→L1段階へGPUメモリ領域の確保も依頼し、L2読込み完了後のPCIe転送を待ち行列化できるようにする。先行確保はGPUメモリを余分に予約しうるが、容量が足りなければ反応的な確保方式へ退化する（§3.1脚注2）。

入力は遠隔KVブロック、下流段階の空きメモリ、要求優先度、ブロック依存関係であり、出力は段階ごとに重なって進むL3→L2→L1読込みと、全必要KV到着後に始まるGPUプリフィルである。転送と計算の接続はブロック到着信号と先行メモリ確保で作る。この構成は通信量そのものを圧縮するのではなく、段階ごとの自律実行により他要求との重ね合わせと資源再利用を可能にする。

### 読込み費用を考慮した要求順序

Sanicはオフラインのシステム・プロファイリングで、コンテキスト長からKV読込み時間 `T_load`、クエリ長から計算時間 `T_comp` を推定する二要素の線形性能モデルを作る（§3.2、図6）。ここで読込み時間はデータ量・ネットワーク等に依存する独立費用として計上される。論文はモデル係数をサービング時に再学習する方法や、未評価のハードウェアへ移植した誤差値は示していない。

- **平均TTFT**: 推定プリフィル費用（読込みと計算）に基づくShortest-Job-First (SJF) で要求を順序付ける。
- **TTFT SLO達成率**: 各要求の期限 `DDL` から `T_load` と `T_comp` を差し引いて slack `LST = DDL − T_load − T_comp` を求め、値が小さい要求を先にするLeast-Slack-Time-First (LSTF) を使う。

## 評価条件と結果

### 実験環境と比較対象

SanicはvLLM 0.9.1、LMCache 0.3.1をベースに約3.3K行で実装され、遠隔L3はMooncake Store、スケジューラ processとworker processの通知にはZeroMQを使う（§4.1）。評価は単一GPUノード（80 GB GPU、CPU DRAM 128 GB）と遠隔CPUノード（DRAM 512 GB）を400 Gbps RDMAで接続した構成で行う。モデルはLlama-3.1-8B-InstructとQwen2.5-14B-Instruct-1M。長文脈データセットはLooGLE、ICL、Codeで、到着時刻は各データセットから与えられないためPoisson分布でシミュレートする。Table 1の規模は、LooGLE 120要求（平均コンテキスト28.1K、平均クエリ28 トークン）、ICL 120要求（28.3K、61 トークン）、Code 100要求（38.3K、209 トークン）である。

基準はvLLM-LMCacheと、スケジューリング最適化を外してFIFOを使うSanic variant。比較の公平性のため、論文は基準側にも読込み帯域を使うMooncake `batch_get_into`、L2→L1向け複数CUDA ストリームなど二つの性能修正を施し、vLLM-LMCacheが一度にプリフィルする要求を一件に制限している（§4.1脚注3）。したがって掲載値は、未調整の標準構成との差ではなく、論文で説明された強化済みの基準との差である。

### エンドツーエンド指標

| 実験・指標 | 論文が明記する結果 | 条件と比較 |
|---|---|---|
| 平均TTFT | ICLでSanicが平均TTFTを81.3%超削減 | 1.2 QPS。vLLM-LMCacheおよびSanic + FIFOとの比較（§4.2、図7）。 |
| TTFT SLO達成率 | SanicのSLO達成率が61.67%高い | 要求ごとに干渉なし条件のTTFTへ2×/4×/8×を一様に掛けてSLO deadlineを設定。1.2 QPSでvLLM-LMCache比（§4.2、図8）。論文の “higher” を百分率ポイント差とは読み替えない。 |

### ポリシー比較と感度

- **費用モデル**: コンテキストトークン数だけを費用とするSJF-PTは、図9の比較で推定優先度を誤り、FIFOよりTTFTが悪くなる場合がある。ここではキャッシュ hit ratioを25%、50%、75%、100%から要求ごとに無作為割当する。読込み時間と計算時間を分離したモデルを使う必要性を示すmicro-ベンチマークである（§4.3）。
- **SLOスケジューリング**: 図10ではLSTFのSLO達成率が73%、サービス費用を使わないEarliest Deadline First (EDF) が58%（§4.3）。本文は図の条件を数値本文で詳述していないため、独立したエンドツーエンド headline値ではなくポリシー比較値として扱う。
- **キャッシュ hit ratio**: 25%、50%、75%、100%を手動設定した感度分析で、Sanicの平均TTFTはhit ratioの増加に伴い単調に改善すると本文は説明する。図11の各棒の値は本文で列挙されていないため、数値を読み取って補わない（§4.3）。

## 既存研究との差と関係

本論文は、既存のKV再利用基盤を置き換える新しいキャッシュ storageや圧縮形式ではなく、読み込んで使う過程の制御と順序付けを主対象にする。サーベイ既収録の [Mooncake（arXiv:2407.00079）](https://github.com/uni042/llm-paper-summary/blob/main/papers/inference/11-llm-serving-scheduling-disaggregation/2024-2407.00079-mooncake-kvキャッシュ-centric-disaggregated-architecture.md) は、分散DRAM等へprefix KVを蓄積・再利用するKV-centric serving architectureであり、SanicはMooncake StoreをL3 backendとして使う。Sanicの貢献は、その共有KVをL2/L1へ搬入する段階を計算と独立させ、読込み費用を要求スケジューラへ渡す点で補完的である。

同じく既収録の [CacheGen（DOI:10.1145/3651890.3672274）](https://github.com/uni042/llm-paper-summary/blob/main/papers/inference/10-kv-キャッシュ-offload-recomputation/2024-2310.07240-キャッシュgen.md) はKV表現を圧縮・ストリーミングしネットワーク転送量を減らす。Sanicは本文でKV payloadの圧縮を提案せず、転送を別段階として重ねて費用モデルへ含める。したがって転送量削減と段階協調・スケジューリングは異なる設計軸で、併用可能性はあるものの本論文は併用を評価していない。

## 限界と適用条件

論文には独立したLimitations節はなく、Conclusionで将来課題を述べる。著者らは、相関したKV読込みタスクを含むagentic AI workflowの協調スケジューリング、Mooncakeのような本番推論システムでの要求 ルーティング改善・network collision緩和への拡張を予定として挙げる（§5）。本研究はそれらの協調・ルーティング自体を評価したものではない。

評価条件から読み取れる適用範囲上の注意は以下である（条件からの推論であり、著者の明示的な限界主張とは区別する）。実験トポロジは一つのGPUノードと一つのremote CPU DRAM node、単一の400 Gbps linkであり、複数GPUサーバをまたぐ本番規模のネットワーク競合は実測していない。要求到着はPoissonシミュレーションで、データセットは三つの長文脈ワークロードに限られる。費用推定はオフライン計測に依存するため、ネットワーク状態・backend・modelが変わる構成へ係数を適用する精度は本文から確認できない。L1の先行確保はGPU メモリを一時予約し、容量に余裕がないと読込みをパイプライン化できる範囲が限られる（§3.1脚注2）。

## 一次資料

- Weiye Wang et al., “Towards Efficient Serving of Network-intensive LLM Inferences,” APNet ’26, 2026. [DOI](https://doi.org/10.1145/3820441.3820479) / [著者配布全文PDF](https://snowzjx.me/assets/sanic-apnet26.pdf)
- [APNet ’26 accepted papers](https://conferences.sigcomm.org/events/apnet2026/accept.php) は採録と掲載著者を確認する補助一次資料。公式DOIページはこの確認時点でブラウザ読取りが403となったため、全文と書誌は著者配布論文PDFを確認した。
