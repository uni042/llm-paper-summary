---
authors:
- Fangyuan Xu
- Tanya Goyal
- Eunsol Choi
canonical_id: DOI:10.18653/v1/2025.acl-long.1211
code: https://github.com/carriex/refreshkv
doi: 10.18653/v1/2025.acl-long.1211
list_summary: 完全KVを保持したまま通常は小さな部分KVへ注意し、クエリ類似度低下時だけ完全注意して重要トークン集合を更新することで長文生成の固定削除失敗を避ける。
publication: ACL 2025
published: 2025-07
reference_main_sha: 56b868025d112b179597495c3ec0105adface8c2
source: https://aclanthology.org/2025.acl-long.1211/
sources:
- https://aclanthology.org/2025.acl-long.1211/
- https://aclanthology.org/2025.acl-long.1211.pdf
summary: RefreshKVは、KVキャッシュを一度だけ圧縮する方式が長文生成の途中で後から必要になる入力トークンを復元できない問題を扱う。完全KVキャッシュ自体は保持し、通常は上位Kトークンだけの部分キャッシュへ注意し、現在のクエリと直近の完全注意時クエリの類似度が下がった時だけ完全注意を実行して部分キャッシュを再構築する。16K文脈でLlama-3.1-8BのArxiv PPLをSnapKV 2.54から2.32へ改善しつつ時間6.77対6.33、HTML→TSVではH2O/SnapKVがF1=0の条件でRefreshKVが17を得る。
title: 'RefreshKV: Updating Small KV Cache During Long-form Generation'
topics:
- KV cache
- long-context inference
- sparse attention
- long-form generation
worker_completed_at: '2026-10-02T22:46:34+09:00'
worker_run_key: 20261002-2245-scheduled-chat-45
publication_type: 査読付き学術論文
publication_status: published
implementation: 実装形態の詳細は既存本文の手法・評価記述を参照。公式コード公開あり（https://github.com/carriex/refreshkv）。
implementation_status: official-code-available
last_checked: '2026-10-03'
references:
- canonical_id: arXiv:2307.11088
  arxiv_id: '2307.11088'
- canonical_id: arXiv:2407.02490
- canonical_id: arXiv:2211.10438
- canonical_id: arXiv:2305.13245
- canonical_id: arXiv:2306.14048
- canonical_id: arXiv:2401.18079
- canonical_id: arXiv:2406.02069
- canonical_id: arXiv:2307.08691
- canonical_id: arXiv:2408.03675
- canonical_id: arXiv:2310.01801
- canonical_id: arXiv:2406.10774
- canonical_id: arXiv:2402.02750
- canonical_id: arXiv:2309.17453
- canonical_id: arXiv:2404.14469
- canonical_id: arXiv:1904.10509
- canonical_id: arXiv:2007.14062
references_checked_at: '2026-10-03'
references_source: primary-pdf-reference-section
references_total: 1
last_audited: null
audit_version: 0
---

# RefreshKV: Updating Small KV Cache During Long-form Generation

> 完全KVを保持したまま通常は小さな部分KVへ注意し、クエリ類似度低下時だけ完全注意して重要トークン集合を更新することで長文生成の固定削除失敗を避ける。

## 概要

長文脈LLMではKVキャッシュが系列長に比例して増え、各デコード段の注意計算も過去トークン数に比例する。StreamingLLM、H2O、SnapKVなどは注意対象トークンを減らすが、入力側トークンを永久に捨てる方式では、長い出力の後半で初めて必要になる情報を取り戻せない。RefreshKVはこの「重要トークン集合が生成中に変わる」問題を直接扱う。

RefreshKVは完全KVキャッシュをメモリに保持するため、容量削減方式ではない。代わりに、通常ステップではK個の入力トークンからなる部分KVだけへ注意して計算時間を減らし、必要と判断したときだけ完全KVへ注意する。その完全注意で得た注意分布からtop-Kトークンを選び直し、部分KVを更新する。

16K入力の言語モデリングでは、Llama-3.1-8Bで完全注意がPPL
2.22/時間7.50、SnapKVが2.54/6.77なのに対し、RefreshKV(QC=10)は2.32/6.33となる。長文HTML→TSVではH2OとSnapKVがF1=0まで崩れる条件でRefreshKV(QC=5)はLlama-3.1-8Bで17、Qwen2-7Bで10を得る。速度だけでなく、生成が進むにつれて必要情報が変わる場合の品質保持が主な貢献である。

## 問題設定

一回だけのKV圧縮は、圧縮時点の注意パターンが将来も有効という仮定を置く。短い出力ならこの仮定が成立しやすいが、要約、HTML表変換、連鎖検索のように数百〜数千トークンを生成すると、現在の出力内容に応じて次に参照すべき入力位置が移動する。

論文のChain-of-key課題はこの失敗を明示する。前に生成したキーの末尾語が次に探すキーを決めるため、将来必要な入力トークンをプリフィル時点だけで固定できない。既存削除方式は2キーを超える有効連鎖をほぼ作れず、精度20未満になる。

## 手法

### 完全キャッシュと部分キャッシュの二重保持

プリフィル後、全入力トークンのKVを完全キャッシュCfとして残す。同時に、直近の完全注意で重要だった上位K入力トークンを部分キャッシュCpへ入れる。部分注意ステップではCpと生成済み局所トークンだけを読み、長い入力全体へのメモリアクセスと注意演算を避ける。

この設計はH2O等と異なり、Cfからトークンを永久削除しない。したがってGPUメモリ容量は完全注意方式と同程度必要だが、デコードの大半で読み出すKV量を減らせる。

### クエリ類似度による更新判定

固定Nステップごとに完全注意すると、タスクによって更新が多すぎたり少なすぎたりする。RefreshKVは一定のクエリ確認間隔QCごとに、現在のクエリベクトルと直近の完全注意ステップのクエリを層ごとに比較する。

コサイン類似度が閾値を下回れば注意パターンが変わった可能性が高いとして完全注意を起動する。Llama-3.1-8Bの主設定では類似度閾値0.85、Qwen2-7Bでは0.95を用いる。完全注意の頻度を内容変化へ適応させるため、同程度の時間で固定間隔より品質を上げられる。

### 完全注意による部分KV再構築

完全注意ステップではCf全体を読み、現在トークンの注意スコアから上位K入力トークンを再選択する。論文の16K実験ではK=2048である。新しく生成されたKVも完全キャッシュへ反映し、以後の部分注意は更新済みCpを使う。

構成要素除去では、Llama-3.1-8BのArxivでRefreshKVがPPL
2.32なのに対し、更新なしでは2.50となり、HTML→TSVはF1
16から0へ落ちる。一方「完全注意の出力を使わない」変種でも2.32/F1
16を保つため、改善源は時折フル文脈で直接生成することより、部分キャッシュを再選択することにある。

## 評価

### 代表条件

  -----------------------------------------------------------------------------------------------------
  項目                                内容
  ----------------------------------- -----------------------------------------------------------------
  モデル                              Llama-3.1-8B、Qwen2-7B。Chain-of-keyでは70B/72Bも使用

  文脈                                言語モデル評価16K、下流は10K〜128K級

  部分KV                              K=2048（主要言語モデル実験）

  比較                                完全注意、StreamingLLM、H2O、SnapKV

  タスク                              Arxiv/Book
                                      PPL、RULER、QMSum、GovReport、NovelSumm、HTML→TSV、Chain-of-key

  時間測定                            A100、生成条件に応じたデコード時間
  -----------------------------------------------------------------------------------------------------

### 主要結果

  ----------------------------------------------------------------------------------------------
  条件                  完全注意      SnapKV/H2O等       RefreshKV 読み取り
  -------------- --------------- ----------------- --------------- -----------------------------
  Llama-3.1-8B              2.22       SnapKV 2.54       QC10 2.32 圧縮品質を大幅回復
  Arxiv 16K PPL                                                    

  同 Book PPL               7.07       SnapKV 7.78       QC10 7.41 長文生成でも乖離を抑制

  同 時間                   7.50       SnapKV 6.77       QC10 6.33 比較可能以上の速度

  HTML→TSV F1                 33  H2O 0 / SnapKV 0          QC5 17 完全注意性能の約52%を回復

  Qwen2-7B                    24  H2O 0 / SnapKV 0          QC5 10 約42%を回復
  HTML→TSV                                                         

  Chain-of-key             56/83   eviction系2〜13       QC5 25/24 2キー超の有効連鎖を生成可能
  ----------------------------------------------------------------------------------------------

動的更新と固定更新の比較では、Llama-3.1-8Bで固定stride=10がHTML精度17、動的QC=5が30で、時間はいずれも1.40。GovReportも32.30対32.56で動的方式が同程度時間で上回る。Qwen2-7Bでも同様に動的更新が品質を改善する条件が多い。

## 既存研究との差

StreamingLLMは局所窓とsink token、H2Oは累積注意のheavy
hitter、SnapKVはプリフィル時の重要位置を使う。これらは削除した入力KVを後から戻せない。RefreshKVは完全KVを残し、計算対象だけを動的に小さくする。

したがってRefreshKVは「KVメモリ容量を減らす圧縮」と「完全注意」の中間に位置する。容量制約が主問題なら不利だが、十分なメモリがあり注意読み出し・計算を減らしたい長文生成では、永久削除による品質崩壊を避けられる。

## 限界・実装状況

完全KVを保持するため、KVキャッシュ容量は削減しない。非常に長い文脈でHBM容量そのものがボトルネックなら、オフロード等を別途組み合わせる必要がある。完全注意ステップは高価なので、類似度閾値を厳しくすると品質は上がる一方で速度利得が縮む。

論文は継続事前学習も検討し、8K/16KでPPLをさらに改善するが、基本のRefreshKVは既存モデルへ推論時だけ適用できる。継続学習結果と無学習の推論結果を混同しない必要がある。

## 一次資料

-   https://aclanthology.org/2025.acl-long.1211/
-   https://aclanthology.org/2025.acl-long.1211.pdf
-   https://github.com/carriex/refreshkv
