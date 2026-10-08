---
under16kb_reaudit_target_path: papers/inference/19-inference-evaluation-benchmarking/2026-2609.19657-prefixbench-h100-prefix-reuse-ttft.md
under16kb_reaudit_source_git_blob_sha: '11510c84f6032320d1f7831ec4dab1a2be923938'
under16kb_reaudit_version: '2026-10-07-v1'
under16kb_reaudit_passed: true
quality_body_chars: 6813
quality_method_chars: 1043
quality_eval_chars: 2895
quality_limitation_chars: 321
quality_self_review_passed: true
quality_self_review_version: '2026-10-07-v1'
worker_completed_at: '2026-10-08T17:39:39+09:00'
worker_run_key: 20261008-interactive-bottom-up-reaudit/prefixbench
worker_id: interactive-bottom-up
last_audited: '2026-10-08'
audit_version: 2
canonical_id: arXiv:2609.19657
arxiv_id: '2609.19657'
doi: 10.48550/arxiv.2609.19657
arxiv_categories:
  primary: cs.PF
  cross_list:
  - cs.LG
last_audited: '2026-09-27'
audit_version: 1
storage_targets:
- GPU HBM
- KV cache
bottlenecks:
- prefix-cache capacity
- request scheduling
- TTFT under burst
hardware_details: Single NVIDIA H100 NVL, 94 GB HBM3; Qwen2-7B-Instruct BF16 and Qwen2.5-32B-Instruct
quality_effect: At 8,192 shared-prefix tokens, reuse cuts p50 TTFT 5–6.5x while cache fits; under burst concurrency 32, TensorRT-LLM p50 TTFT is 319 ms vs vLLM 759 ms.
evidence_locations:
- Abstract
- Sections 3, 4, 5, 7
references:
- canonical_id: arXiv:2403.02310
- canonical_id: arXiv:2510.09665
  arxiv_id: '2510.09665'
- canonical_id: arXiv:2408.05499
- canonical_id: arXiv:2401.08671
  arxiv_id: '2401.08671'
- canonical_id: arXiv:2406.17565
  arxiv_id: '2406.17565'
- canonical_id: DOI:10.1145/3600006.3613165
- canonical_id: arXiv:2405.04532
- canonical_id: DOI:10.1145/3651890.3672274
- canonical_id: arXiv:2311.18677
- canonical_id: arXiv:2405.04437
- canonical_id: arXiv:2405.16444
- canonical_id: DOI:10.5555/3600237.3600268
- canonical_id: arXiv:2312.07104
- canonical_id: arXiv:2401.09670
- canonical_id: arXiv:2408.12757
references_checked_at: '2026-10-03'
references_source: arxiv-html-reference-section
references_total: 18
title: 'PrefixBench-H100: Characterizing Prefix Reuse and Time-to-First-Token in H100 LLM Serving'
summary: PrefixBench-H100は、単一のH100 NVL上でvLLMとTensorRT-LLMへ同じ要求列を送り、共有接頭辞の再利用効果とスケジューラ差を切り分ける測定枠組みである。Qwen2-7B-Instruct BF16等を用い、接頭辞長・接尾辞多様性・到着形態・並列度・出力長・キャッシュ設定を変えてTTFT、生成間隔、スループット、命中率、メモリを測る。キャッシュが容量内なら8,192トークン接頭辞の再利用でTTFTが5〜6.5倍短縮し、バースト並列度32ではTensorRT-LLMがvLLMより低いp50 TTFTを示す一方、固定到着では優劣が逆転する。
list_summary: 単一H100 NVLでvLLMとTensorRT-LLMを同一負荷比較し、接頭辞再利用が容量内でTTFTを5〜6.5倍減らす一方、バーストか固定到着かでランタイムの優劣が反転し、差の主因はキャッシュより上位のスケジューリングにあると示す。
authors:
- Omkar Shewale
- Deepak Kumar
- Divakar Kumar Yadav
authors_affiliations: Illinois Institute of Technology; University of Wisconsin–Milwaukee
published: '2026-09-17'
publication: arXiv preprint
publication_type: Preprint
publication_status: Preprint
lineage: LLM inference evaluation and benchmarking
topics:
- prefix caching
- serving runtime comparison
- H100
importance: キャッシュ方式の存在だけで実配信のTTFTを推定できず、到着形態・並列度・容量比・上位スケジューラの条件を揃えた測定が必要であることを示す。
hardware_evaluation: 単一H100 NVL 94GB HBM3、Qwen2-7B-Instruct BF16。追加の容量圧力実験でQwen2.5-32B-Instruct。
source: https://arxiv.org/abs/2609.19657
sources:
- https://arxiv.org/abs/2609.19657
- https://arxiv.org/html/2609.19657v1
code: https://doi.org/10.5281/zenodo.21725505
implementation: 測定コード、102個のJSON生データ、統合CSV、図、分析ノートブックを公開。
last_checked: '2026-10-08'
---

# PrefixBench-H100: Characterizing Prefix Reuse and Time-to-First-Token in H100 LLM Serving

> 単一H100 NVL上でvLLMとTensorRT-LLMへ同じ要求列を送り、接頭辞キャッシュそのものの効果、容量超過、要求スケジューリングの差を切り分ける実測ベンチマーク。

## 概要

システム指示、検索拡張生成（Retrieval-Augmented Generation; RAG）のテンプレート、複数ターン会話では、複数要求の先頭に同じトークン列が繰り返し現れる。通常はその接頭辞を毎回プリフィルしてキー・バリュー（Key-Value; KV）キャッシュを作るが、接頭辞キャッシュ（prefix cache）を使えば、以前計算したKV状態を再利用して重複計算を避けられる。

ただし「同じ接頭辞がある」ことと「先頭トークン遅延（Time To First Token; TTFT）が大きく下がる」ことは同義ではない。再利用するKVがGPUメモリに収まるか、何要求が同時に来るか、要求をどの順序でバッチへ入れるかによって、キャッシュ命中後の待ち時間が変わる。キャッシュ方式だけを単独評価すると、実際にはスケジューラ由来の差をキャッシュ性能と誤認しやすい。

PrefixBench-H100は新しい接頭辞キャッシュ方式ではなく、単一NVIDIA H100 NVL 94GB上でvLLMとTensorRT-LLMへ同じ要求列を送り、接頭辞再利用、容量圧力、到着形態、並列度を系統的に変える測定枠組みである。基本はQwen2-7B-Instruct BF16、容量圧力ではQwen2.5-32B-Instructを使う。

8,192トークンの共有接頭辞がKV容量内に収まる並列度1では、vLLMのp50 TTFTが345.1msから53.0msへ短縮し、6.51倍の差になる。TensorRT-LLMでも306msから約50msへ短縮する。一方、バースト並列度32ではTensorRT-LLMが319ms、vLLMが759msであるのに対し、固定到着率16要求/秒ではp95の優劣が反転する。つまり、キャッシュが同程度に効いていても、上位スケジューリングの動作でランタイム比較の結論が変わる。

## 書誌情報

- 著者: Omkar Shewale、Deepak Kumar、Divakar Kumar Yadav。
- 公開: 2026年9月17日、arXiv:2609.19657。
- 基本ハードウェア: NVIDIA H100 NVL、94GB HBM3、単一GPU。
- 基本モデル: Qwen2-7B-Instruct、7.6Bパラメータ、BF16重み・BF16 KV、32K文脈。
- 容量圧力実験: Qwen2.5-32B-Instruct。
- 公開物: 測定コード、102個のJSON生データ、統合CSV、図、再分析ノートブック。

## 問題設定

接頭辞再利用では、過去要求のKVを見つけて利用できれば、そのトークン部分のプリフィル演算を省ける。接頭辞が長いほど省ける行列演算は増えるので、理想的にはTTFT短縮も大きくなる。しかし実サービングでは、再利用KVを保持するメモリ、検索・照合、要求の待ち行列、バッチ形成、デコード中要求との干渉が加わる。

特に容量が重要である。7Bモデルを94GB HBM3へ載せる条件では比較的大きなKV作業集合を保持できるため、接頭辞キャッシュの命中率が安定しやすい。その結果だけを見ると「長い共有接頭辞は常に再利用できる」と見えてしまう。より大きい32Bモデルや制限したKV領域では追い出しが始まり、同じ再利用パターンでも利得が崩れる。

もう一つは要求到着である。並列度1の逐次負荷なら、キャッシュ済み要求はすぐGPUへ入れやすい。しかし32件が一斉に到着すると、キャッシュ計算を省いても実行スロットを待つ。逆に一定レートで流入する負荷では、スケジューラの公平性や連続バッチの作り方が支配的になる。本研究はこの「キャッシュ命中」と「上位の要求制御」を分けて測る。

## 手法

### 1. 同じJSONL要求列を両ランタイムへ与える

OpenAI互換の要求生成器を使い、vLLMとTensorRT-LLMへ同じ入力列・同じ到着条件を与える。ランタイムごとに異なるデータセットやプロンプトを使わず、比較軸を接頭辞長、接尾辞多様性、到着パターン、並列度、出力長、キャッシュ設定へ限定する。

キャッシュ有効・無効を同じ要求列で比較することで、モデルや入力の違いではなく「再利用できたプリフィル計算」の寄与を直接見る。接頭辞長0も入れるため、キャッシュ機構を有効にしただけの固定オーバーヘッドも確認できる。

### 2. TTFTだけでなく生成・メモリ・命中率を同時に測る

主指標はTTFTだが、トークン間遅延（Inter-Token Latency; ITL）、エンドツーエンド遅延、スループット、キャッシュ命中統計、GPUメモリ使用量も記録する。接頭辞再利用は主にプリフィルを省くためTTFTへ強く効く一方、生成開始後のITLへ同じ倍率で効くとは限らない。

これにより、「TTFTは下がったが生成スループットは変わらない」「命中率は同じだが待ち行列だけ違う」といった原因分離ができる。単一の平均遅延だけでランタイムを評価しないことがベンチマークの目的である。

### 3. バーストと固定到着を分ける

逐次要求、同時に多数要求を投げるバースト、一定RPSで流す固定到着を分けて測る。バーストでは瞬間的なキュー処理とバッチ形成、固定到着では継続的な定常処理能力が表れやすい。

実際に並列度32のバーストではTensorRT-LLMのp50 TTFTがvLLMより低い一方、16要求/秒の固定到着ではp95の優劣が逆転する。したがって、片方の到着形態だけで「どちらのランタイムが速い」と一般化しない。

### 4. 32Bモデルでキャッシュ容量境界を意図的に作る

Qwen2-7BではH100 NVL 94GBにKVが収まりやすいため、Qwen2.5-32B-Instructも使って実効KV容量に対する作業集合比を増やす。容量内、境界付近、大幅超過という領域を作り、追い出しによって命中率とTTFTがどう崩れるかを見る。

13.2倍の過剰割当条件では命中率が5.6%まで落ち、再利用が十分効く条件に対してTTFTが15.7倍悪化する。これはキャッシュアルゴリズムの有無より「再利用したい集合が実際に保持容量へ収まるか」が第一条件であることを示す。

## 評価

### 評価条件

| 項目 | 基本条件 |
|---|---|
| GPU | NVIDIA H100 NVL ×1、94GB HBM3 |
| 基本モデル | Qwen2-7B-Instruct、約7.6B |
| 容量圧力モデル | Qwen2.5-32B-Instruct |
| 数値形式 | BF16重み、BF16 KV |
| 文脈上限 | 32K |
| ランタイム | vLLM、TensorRT-LLM |
| 接頭辞長 | 0〜8,192トークン |
| 到着形態 | 逐次、バースト、固定到着率 |
| 主指標 | TTFT p50/p95、ITL、E2E遅延、スループット、キャッシュ命中、GPUメモリ |
| 再現物 | 102 JSON traces、統合CSV、図、分析ノートブック |

### 代表的な結果

| 条件 | vLLM | TensorRT-LLM | 解釈 |
|---|---:|---:|---|
| 8,192共有接頭辞、並列度1、キャッシュ無効 | p50 TTFT 345.1ms | 306ms | 長いプリフィルを毎回計算 |
| 同条件、接頭辞再利用 | p50 TTFT 53.0ms | 58.2ms | vLLMで6.51倍、TensorRT-LLMで5.26倍短縮 |
| バースト並列度32 | p50 TTFT 759ms | 319ms | 同時到着時はTensorRT-LLM側の上位スケジューリングが有利 |
| 固定到着16要求/秒 | p95で順位反転 | p95で順位反転 | バースト結果だけでは定常負荷の優劣を予測できない |
| 32B、KV作業集合13.2倍超過 | 命中率5.6%、TTFT 15.7倍悪化 | 容量圧力評価 | キャッシュ容量を超えると再利用利得自体が崩れる |

8,192トークンで得られた5〜6.5倍のTTFT短縮は、共有接頭辞が長く、かつ再利用状態が容量内に残る条件での結果である。接頭辞0では再利用有無の差はほぼなく、キャッシュを有効化しただけで速度が出るわけではない。

バースト32でTensorRT-LLMが優位でも、固定到着で順位が変わることから、ランタイム差を接頭辞キャッシュ実装だけに帰属できない。命中後の要求をいつGPUへ入れるか、連続バッチへどう組み込むかがTTFT分布を変える。

### 評価から分かる三つの運転領域

1. **容量内・低並列**: 接頭辞再利用の純粋な計算省略がTTFTへ現れやすい。
2. **容量内・高並列**: 命中率が高くてもスケジューリング待ちが支配し、ランタイム差が大きくなる。
3. **容量超過**: そもそも再利用状態が残らず、キャッシュ命中率が崩れてプリフィル再計算へ戻る。

この三領域を分けずに平均TTFTだけ比較すると、「キャッシュ方式」「スケジューラ」「容量」のどれが原因か分からない。PrefixBench-H100はこの原因分離を主眼にしている。

### 一次資料との再照合：再利用の有効性を分離する

arXiv初版の第4.1節・表1は、8192トークンの共通接頭辞を持つ逐次要求40件で、先頭要求によってキャッシュを温めた後の中央値を報告する。vLLMの先頭トークン到達時間は、キャッシュ無効時345.1ミリ秒から有効時53.0ミリ秒へ変化して6.51倍短縮する。TensorRT-LLMは306.1ミリ秒から58.2ミリ秒で5.26倍となる。一方、共通接頭辞0トークンの条件ではvLLMが25.1対25.2ミリ秒、TensorRT-LLMが23.7対23.9ミリ秒で、キャッシュ機能そのものが魔法のように固定費を減らすわけではない。この組合せにより、先頭トークン遅延の大幅な短縮が、再計算を省略できる長い接頭辞に依存することを確かめられる。

### 到着形態と遅延分布：中央値と95パーセンタイルを混同しない

第4.2節の一斉到着実験は、4096トークンの共通接頭辞を4種類持つ要求を100件流し、同時実行数を1から32まで増やす。並列度1ではvLLMが42ミリ秒、TensorRT-LLMが52ミリ秒と前者が速い。一方、並列度32の中央値はvLLM759ミリ秒に対してTensorRT-LLM319ミリ秒となり、順位が逆転する。ただし同条件の95パーセンタイルはvLLM約1.30秒、TensorRT-LLM約1.58秒で、中央値と高遅延側で異なる順位になる。単一の代表値だけで一方を常に高速と判断してはならない。

キャッシュ命中割合はこの一斉到着でも約83～85%を維持し、順位逆転を単純なキャッシュ命中率差で説明できない。vLLMについては待機時間計測器があり、並列度32では平均待機154ミリ秒へ増えることが確認される。ただし比較対象のTensorRT-LLMには同等の待機時間計測器がないため、両者の遅延差をスケジューラの単一原因へ完全に因果分解できたわけではない。スケジューリングの説明は、命中率が似ているという消去法と観測可能な待機時間から支持される推論である。

第4.6節の固定到着実験では1秒に16要求の条件で、vLLMの95パーセンタイルは22ミリ秒、TensorRT-LLMでは203ミリ秒となり、約9.2倍の差に逆転する。これは200件のテンプレート型検索拡張生成要求を等間隔で送った結果で、実サービスの到着時刻が独立に揺らぐ確率的な流入は再現していない。そのため、本番運用では同時到着の極端な負荷と一定間隔で流れる負荷の双方を測り、高遅延側の分布まで比較する必要がある。

### 設定変更と容量圧力を独立に確かめる

第4.4節ではTensorRT-LLMのキャッシュブロック長を32、64、128トークンと変更しても、実験したPyTorch実行系では速度差が概ね計測ばらつきの範囲に収まる。これはブロック寸法の一般的な最適値を発見した結果ではなく、当該GPU、実装版、要求形状において既定設定から変更する利得を確認できなかったという否定的な実験結果である。

第4.8節の容量制限実験は、同じ7Bモデルでも使用可能なKVキャッシュ容量を56,320トークンに制限している。128種類の接頭辞が競合する条件では、制限前に両実装で約68.2%だった再利用率が制限後には約3.6%へ落ちる。vLLMの中央値も52ミリ秒から318ミリ秒、TensorRT-LLMでは67ミリ秒から303ミリ秒へ悪化するため、モデル規模だけでなく「同時に使いたい接頭辞の総KV量と保持可能容量の比」が再利用の成否を決めることを裏づける。さらに第4.9節のMistral-7B確認でも、並列度32の中央値はvLLM553.8ミリ秒、TensorRT-LLM265.0ミリ秒で同じ傾向が維持される。ただし複数GPU、異なる量子化幅、分散キャッシュへそのまま外挿できない。

## 既存研究との差

接頭辞キャッシュ研究は、共有接頭辞の照合方法、KVブロック配置、キャッシュ置換などの新機構を提案する。本論文は新キャッシュを追加せず、既存のvLLMとTensorRT-LLMを同じH100・同じモデル・同じ要求列で動かし、実際にどの条件で差が出るかを測る。

また、単純な「cache on/off」だけでなく、要求到着と容量圧力を独立に動かす。これにより、命中率が同程度なのにTTFTが違う領域をスケジューラ問題として、命中率自体が崩れる領域を容量問題として切り分ける。

## 限界

- 単一H100 NVLの結果であり、複数GPU、テンソル並列、プリフィル・デコード分離では追加の通信・配置要因が入る。
- 基本比較はQwen2-7B、容量圧力はQwen2.5-32Bであり、70B級やMoEモデルのKV/重み比率は異なる。
- BF16固定なので、FP8重みや量子化KVを使った場合の容量境界は変わる。
- ランタイムのバージョン更新でスケジューラや接頭辞キャッシュ実装が変われば、絶対値・順位も変わり得る。
- 合成要求列とチャット/RAG型要求を使うが、全ての本番到着分布を代表するわけではない。
- 5〜6.5倍という代表値は長い共有接頭辞が実際に再利用できる条件であり、共有率が低いサービスへそのまま適用できない。

## 実運用への含意

接頭辞キャッシュを導入するときは、平均共有接頭辞長だけでなく、同時に生きているユニーク接頭辞の総KV量を測る必要がある。容量内ならプリフィル削減が効くが、容量を越えた瞬間に追い出しが増えるため、平均メモリ使用量だけでは危険である。

ランタイム比較では少なくとも「逐次」「バースト」「定常到着」を分けるべきである。特に利用者向けサービスではp50だけでなくp95/p99 TTFTを見ないと、短時間キューが作る裾遅延を見落とす。PrefixBench-H100の結果は、キャッシュ機能の有無よりも、その上にある要求制御まで含めて測る必要性を示す。

## 一次資料

- arXiv: https://arxiv.org/abs/2609.19657
- 再現用アーティファクト: DOI 10.5281/zenodo.21725505

## 修正履歴

- 2026-09-28: 現行の論文品質ガイドに合わせ、接頭辞キャッシュ→容量→スケジューラの因果関係、4つの測定軸、H100/Qwen評価条件、TTFT・命中率の代表結果表、三つの運転領域、既存研究との差と実運用上の含意を追加した。
