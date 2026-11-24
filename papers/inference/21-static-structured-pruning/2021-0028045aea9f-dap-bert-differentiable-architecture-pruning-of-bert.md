---
canonical_id: DOI:10.1007/978-3-030-92185-9_30
doi: 10.1007/978-3-030-92185-9_30
title: 'DAP-BERT: Differentiable Architecture Pruning of BERT'
authors:
- Chung-Yiu Yau
- Haoli Bai
- Irwin King
- Michael R. Lyu
published: 2021-12
publication: ICONIP 2021, Lecture Notes in Computer Science 13108, pp. 367–378
publication_type: conference-paper
publication_status: peer-reviewed-published
source: https://oscaryau525.github.io/uploads/DAP_BERT.pdf
sources:
- https://oscaryau525.github.io/uploads/DAP_BERT.pdf
- https://doi.org/10.1007/978-3-030-92185-9_30
implementation: 既存BERT-base/TinyBERTをsuper-graphとし、注意headとFFN中間次元の微分可能ゲートを探索、FLOPs制約を漸進的に適用し、剪定後に二段階蒸留でfine-tuning。Intel Xeon E5-2620 2.00GHz・4コアでbatch32/最大系列128のCPU推論時間を測定。公式コード公開。
code: https://github.com/OscarYau525/DAP-BERT
summary: 既存BERTの注意headとFFN中間次元に連続ゲートを付け、FLOPs目標を徐々に縮めながら蒸留損失とともに最適化する構造化枝刈り。勾配消失と振動を抑える上位10%勾配の符号更新、元重み復元後の二段階蒸留が特徴。BERT-baseのGLUE平均78.6を保つFLOPs 22.3B→11.4BでCPU実測7.28→3.72秒、より小さい3.0Bでは1.36秒・平均76.4。TinyBERT4追加剪定の27.6倍は元のBERT-base比でありTinyBERT4単体比では約2.38倍。
list_summary: BERTの注意head/FFN幅を微分可能探索で剪定し、CPUのbatch32推論をBERT-base 7.28→1.36秒へ短縮。27.6倍の比較基準は元BERT-base。
last_checked: '2026-10-28'
worker_id: scheduled-chat-00
scheduled_slot: '00'
worker_run_key: 20261028-2202-scheduled-chat-00/r01
worker_completed_at: '2026-10-28T22:07:38+09:00'
reference_main_sha: 3579a9852e533caf20392a0585a93a01fb033067
quality_self_review_passed: true
quality_self_review_version: PAPER-QUALITY-GUIDE-2026-10-07
last_audited: null
audit_version: 0
references:
- canonical_id: arXiv:2109.15082
  arxiv_id: '2109.15082'
- canonical_id: arXiv:2003.07577
  arxiv_id: '2003.07577'
- canonical_id: arXiv:1907.11692
  arxiv_id: '1907.11692'
- canonical_id: arXiv:1910.06360
  arxiv_id: '1910.06360'
- canonical_id: arXiv:1905.10650
- canonical_id: arXiv:1909.05840
- canonical_id: arXiv:1908.08962
  arxiv_id: '1908.08962'
- canonical_id: arXiv:2009.12812
references_checked_at: '2026-10-28'
references_source: primary-pdf-reference-section
references_total: 35
---

# BERTの注意ヘッドとFFN幅を段階的に削るDAP-BERT：CPU実測と蒸留費用を含む検討

## 概要

DAP-BERTは、既存のBERTモデルから、実行装置の演算制約に応じて不要な注意ヘッドとFeed-Forward Network（FFN）の中間次元を選択的に除去する、微分可能な構造化枝刈り方式である。元のBERTを構造探索のsuper-graphとして使い、各ヘッドとFFNの各中間次元に学習可能な連続ゲートを設ける。推論のFLOPsを目標へ近づける制約と、元モデルの出力を模倣する知識蒸留損失を組み合わせて、ヘッド数と中間幅を層ごとに探索する。探索後は閾値により実際に枝を取り除き、元モデルの重みを残った構造へ復元してから二段階の知識蒸留で性能を回復する。

原著Table 1ではBERT-baseのFLOPsを22.3Bから11.4Bへ削減してもGLUEテスト8タスクの平均得点78.6を維持した。Table 2ではIntel Xeon E5-2620 2.00GHz・4コア、batch32・最大系列長128のCPU条件で推論時間が7.28秒から3.72秒へ短縮した。さらにFLOPsを3.0Bへ下げるとGLUE平均76.4、CPU推論1.36秒で、元のBERT-base比5.4倍速となる。ただし、論文が述べる最大27.6倍は**元のBERT-baseと、TinyBERT4を追加剪定したモデルとの比較**であり、TinyBERT4単独から27.6倍高速化したという意味ではない。原著の研究対象は双方向BERTの分類タスクで、自己回帰LLMのトークン生成速度は測っていない。

## 問題設定：FLOPs制約下でのモデル構造探索

一般的な枝刈りでは重みの絶対値や勾配の大きさを指標として、不要と見なした部分を削除する。しかし、重み単位の非構造化枝刈りではCPUでの行列演算が必ずしも小さくならない。BERTの推論で実効的に演算量を下げるには、注意ヘッド単位またはFFNの隠れ次元単位で削り、残った行列の幅を物理的に縮めることが重要となる。一方、ネットワーク全体を一からニューラルアーキテクチャ探索する方式は計算費用が大きい。DAPは既に下流タスク向けに調整したBERTを出発点にし、既存構造の部分集合から選ぶことで探索範囲を限定する。

この方式の制約は、実行装置ごとに許容される計算量 $F_{target}$ が異なる点である。端末の演算予算を満たしながら元のBERTのタスク精度をなるべく維持するため、ヘッド数とFFNの中間幅を層別に選ぶ。モデル全体の層数を自由に変更したり、Transformer以外の演算セルを生成したりする探索ではない。構造化枝刈りの対象はMHAとFFNであり、埋め込みや全ての演算が同じ比率で縮むわけでもない。

## 手法

### 1. MHAとFFNの学習可能な構造ゲート

BERTの各層のマルチヘッド注意では、各ヘッドの出力 $H_i$ に対し学習可能なスカラー $\alpha_i^m$ を割り当て、$\sigma(\alpha_i^m)$ を掛けてから連結・出力投影を行う（原著式(1)、(2)）。シグモイド値がゼロに近づいたヘッドは寄与が小さくなるため、探索後に対応するQuery/Key/Value投影と出力投影の列・行を削除できる。単にヘッドの出力をゼロでマスクしたまま実行するのではなく、行列の形状そのものを縮小することがCPUでの実測速度改善につながる。

FFNには中間表現の各次元に $\alpha_j^f$ を割り当てる。第一線形層と活性化関数の出力に対角ゲート $\mathrm{Diag}(\sigma(\alpha^f))$ を掛け、第二線形層へ渡す（原著式(3)）。ゲートの小さい次元を除去すると、第一線形層の出力幅と第二線形層の入力幅が同時に減る。注意ヘッド数とFFN幅をそれぞれ層別に選べるため、全層一律に幅を半分にする方式より細かく演算予算を配分できる。

### 2. FLOPsの期待値と制約損失

各ヘッドとFFN次元に対応するゲート値から、選択される構造の期待FLOPs $E[F(\alpha)]$ を計算する。原著式(6)では層・ヘッド・中間次元について、ゲート値に対応する単位演算量を掛けて合計する。これを目標値と比較し、許容幅 $\delta$ を超えたときだけ対数型のペナルティを与える（式(5)）。目標より大きければ縮小を促し、小さすぎれば容量を戻す方向へ誘導する。性能だけを最適化してモデルが大きく残ることと、サイズだけを最小化して性能を失うことの両方を抑える構成である。

ただし最初から最終FLOPs目標を固定すると、探索の初期にゲートが一気に閉じ、重要なヘッドを誤って落とす可能性がある。そこで原著式(8)は、初期の元モデルFLOPs $F_{original}$ から最終 $F_{target}$ へ、探索ステップ $t/T$ に従い指数的に目標を縮める $F_{curr}(t)$ を導入する。枝刈り圧力を徐々に強くするため、モデルが各段階で表現を再配置する時間を確保できる。

### 3. ゲート勾配の消失と振動への対策

シグモイドゲートが0または1へ飽和すると、通常の勾配更新では $\alpha$ の勾配が小さくなり、探索が進まない。原著はsignSGDで勾配の符号を使うことで更新の大きさを確保する。ただしsignSGDをそのまま全ゲートへ適用すると、更新が振動して最終FLOPsへ早期に到達し、十分に良い構造を選べない。そこで、各ステップで勾配絶対値が大きい**上位10%の構造パラメータだけ**符号更新し、残りは更新しない（原著式(7)）。これをrectified gradient updateと呼ぶ。

この上位10%は、推論時に残すヘッドの割合ではない。探索中に更新する構造ゲートの割合である。Figure 2とFigure 3は、通常SGDでは目標FLOPsに届かず、signSGD単独では振動する一方、rectified updateと漸進的FLOPs制約を併用すると滑らかに目標へ到達する様子を示している。これらは最終精度の差を説明する構成要素除去の根拠となる。

### 4. 探索の教師信号と剪定後の回復

探索損失は元のBERTのロジット $z_t$ と探索モデルのロジット $z_s$ のクロスエントロピー、およびFLOPs制約損失の和 $L_{search}=L_{ce}+\lambda L_{cost}$ である（原著式(9)）。教師のsoft labelを使うことで、正解クラスだけでは表現しきれない元モデルの予測分布を構造探索へ伝える。探索中はモデル重み $w$ とゲート $\alpha$ を同時更新するが、最終モデルには探索中の重みをそのまま継承しない。

Algorithm 1では、ゲートが閾値 $\tau$ を超えるヘッド・次元を残して枝刈りした後、**残存構造の重みを元のBERTから復元**する。著者らは探索中に更新した重みをそのままfine-tuningすると性能が下がることを確認したため、探索で得た構造だけを採用する。次に二段階の蒸留を実施する。第一段階は各層の注意マップとFFN出力の平均二乗誤差を最小化し、第二段階は予測ロジットの蒸留を行う（原著式(10)）。この処理によって剪定後の精度を回復するが、蒸留とfine-tuningは追加学習コストである。オフラインで単純にヘッドを落とすだけの無学習手法ではない。

### 5. 実装と探索手順

既にGLUEタスク向けにfine-tuningされたBERT-baseまたはTinyBERTを初期super-graphとし、全ゲートが残るように $\alpha_i=5$ で初期化する。閾値は $\tau=0.99$。小規模データセットでは探索10 epoch・fine-tuning10 epoch、大規模データセットでは探索1 epoch以下・fine-tuning3 epochを設定し、Adamの学習率は $5\times10^{-5}$ とする。小規模GLUEのRTE、MRPC、STS-B、CoLAではデータ拡張も利用する。探索の後に元重みの復元と蒸留を行うため、完成したモデルの推論時には連続ゲートを計算し続ける必要はない。

## 評価条件と測定対象

| 項目 | 原著の条件 |
|---|---|
| モデル | BERT-base（12層）、TinyBERT6、TinyBERT4。事前に下流タスク向けに調整されたモデルを利用 |
| 品質評価 | GLUE testのMNLI-m、QQP、QNLI、SST-2、CoLA、STS-B、MRPC、RTE。各指標はタスクごとに異なる |
| 予算 | FLOPs目標を変化。Table 1のBERT-baseは22.3B、11.4B、7.1B、3.0B |
| 速度測定 | **Intel Xeon E5-2620 2.00GHz、4コアCPU**。batch32、最大系列長128で1バッチの推論時間を測定（Table 2） |
| 蒸留 | 探索中のlogit蒸留、剪定後の中間表現蒸留と予測蒸留。タスク別のfine-tuningを含む |
| 非評価 | GPUでの実測tok/s、LLM decoder-onlyの逐次生成、KVキャッシュ、長文脈、バッチ1の遅延 |

## 主要結果

### FLOPs・パラメータ数・GLUE品質（原著Table 1）

| モデル | FLOPs（B） | パラメータ（M） | GLUE test平均 | CoLA | RTE |
|---|---:|---:|---:|---:|---:|
| BERT-base | 22.3 | 109.5 | 78.6 | 55.3 | 65.5 |
| BERT-base + DAP-50% | 11.4 | 66.6 | 78.6 | 53.0 | 66.0 |
| BERT-base + DAP-30% | 7.1 | 51.6 | 77.7 | 49.9 | 65.2 |
| BERT-base + DAP-10% | 3.0 | 33.6 | 76.4 | 45.7 | 63.6 |
| TinyBERT6 | 11.1 | 67.0 | 79.0 | 51.1 | 70.0 |
| TinyBERT6 + DAP-30% | 3.6 | 37.1 | 77.2 | 46.1 | 63.6 |
| TinyBERT4 | 1.2 | 14.5 | 76.5 | 44.1 | 66.6 |
| TinyBERT4 + DAP-30% | 0.4 | 11.1 | 74.0 | 40.7 | 60.8 |

BERT-baseのFLOPsがほぼ半分の11.4Bになっても8タスク平均は78.6を保つ。ただしCoLAは55.3から53.0へ下がるため、「全タスクで劣化なし」という意味ではない。FLOPsを3.0Bまで縮めると平均は76.4となり2.2ポイント低下する。TinyBERT4の追加剪定では平均76.5から74.0へ低下し、RTEは66.6から60.8へ5.8ポイント下がる。元モデルが小さいほど同程度の圧縮で品質を落としやすい点が重要である。

### CPU実測時間と比較基準（原著Table 2）

| モデル | 1バッチ時間（秒） | BERT-base比の実測高速化 | 直前の同系ベース比 |
|---|---:|---:|---:|
| BERT-base | 7.28 | 1.0倍 | — |
| BERT-base + DAP-50% | 3.72 | 2.0倍 | BERT-base比約1.96倍 |
| BERT-base + DAP-30% | 2.49 | 2.9倍 | BERT-base比約2.92倍 |
| BERT-base + DAP-10% | 1.36 | 5.4倍 | BERT-base比約5.35倍 |
| TinyBERT6 | 3.69 | 2.0倍 | — |
| TinyBERT6 + DAP-30% | 1.22 | 6.0倍 | TinyBERT6比約3.02倍 |
| TinyBERT4 | 0.62 | 11.8倍 | — |
| TinyBERT4 + DAP-30% | 0.26 | 27.6倍 | **TinyBERT4比約2.38倍** |

ここでの27.6倍は7.28/0.26であり、比較対象はBERT-baseである。TinyBERT4の追加枝刈り固有の高速化は0.62/0.26≈2.38倍にとどまる。原著はFLOPs理論比とCPU実測比も区別しており、BERT-baseからDAP-10%への理論FLOPs比は22.3/3.0≈7.43倍、実測は約5.35倍。実行時には枝刈り後も残る演算やCPUの実装上の固定費があるため、FLOPsの減少率がそのまま速度倍率にはならない。

### 既存圧縮方式との比較（原著Table 3・4）

GLUE testではDAP-BERT12-10%がFLOPs 3.0B、パラメータ33.0M、平均76.4。MobileBERT-tinyはFLOPs 3.1B、パラメータ15.1M、平均76.4である。**同程度のFLOPsと平均品質でもDAPの方がパラメータ数は多い**。したがってメモリ容量の優位はこの比較からは導けない。DAP-BERT4-30%はFLOPs0.40B、パラメータ11.1M、平均74.0で、BERT-miniのFLOPs0.87B、11.1M、平均65.4より高いが、学習・蒸留条件の完全一致を意味しない。

開発セットのTable 4ではDAP-BERT12-10%の平均80.9に対しDistilBERT6は79.6、NAS-BERT10は75.5。ただしGLUE testのTable 3とdevelopmentのTable 4を混ぜて優劣を比較してはならない。特にMobileBERT-tinyのパラメータ数とDAP-BERT12のパラメータ数の差は、FLOPs最小化とモデルサイズ最小化が別目的であることを示す。

### アブレーションと負の結果

原著Figure 2・3では、通常のSGDだけではゲートが飽和して十分な枝刈りに至らず、signSGD単独では構造ゲートが振動する。漸進的FLOPs制約だけでも目標に安定収束せず、上位10%勾配の符号更新と漸進的制約を組み合わせることで構造探索が安定する。Figure 3の右図では正解のhard labelより教師モデルのsoft labelを使った探索の方が良い構造を選びやすいと報告している。したがって単なるL1重み枝刈りでも、単なる微分可能ゲートでもない。

一方、最終性能を維持するためには探索・元重み復元・二段階蒸留という複数工程が必要である。小データセットでは探索とfine-tuningを各10 epoch実行するため、モデルの配備前処理が無料ではない。さらにTinyBERT4を0.4B FLOPsまで縮めるとCoLAが44.1→40.7、RTEが66.6→60.8へ低下する。モデルが小さくなるほど品質の安全余裕が減る点は、圧縮率だけを追求する場合の失敗条件である。

## 既存研究との差分とLLM推論サーベイでの位置づけ

重みの大きさを使う単純な枝刈りと違い、DAP-BERTは実際にCPUの行列演算を縮小できる注意ヘッドとFFN中間次元を単位として選ぶ。NAS-BERTやAdaBERTのように新しいアーキテクチャを広く探索するのではなく、学習済みBERTの部分構造を探索し、モデルの事前学習を繰り返さない。さらにFLOPs予算を探索目的へ直接入れるため、対象端末の演算制約に合わせた構造を得られる。ただし端末ごとの実測遅延を直接最適化するのではなく、FLOPsを代理指標にしている点に留意する。

LLM推論最適化という観点では、構造化枝刈りがCPU実測のレイテンシを改善する具体例として有用である。しかし評価はBERTの分類・自然言語理解タスクであり、decoder-only LLMにおけるKVキャッシュの削減、長文脈注意、逐次デコード時のメモリ帯域、GPUのバッチ1性能、推論サーバの同時処理能力については実証していない。Transformer一般へ方法を転用できる可能性と、現代の生成LLMで検証済みであることを混同しない。

## 限界・再現性

推論速度は特定のIntel Xeon CPU・4コア・batch32・最大128トークンでの測定に限られる。CPUの短文分類における1バッチ時間を、GPU上のprefill/decode速度や長文脈の生成トークン/秒に読み替えることはできない。FLOPsの目標達成もモデルの実測メモリ使用量や電力消費の制約達成と同義ではない。Table 1の平均得点は異なるGLUE指標の単純平均であり、ある個別タスクの精度維持を保証しない。

検索時の重みと最終モデルの重みを区別する必要があり、原著Algorithm 1は探索中の重みを破棄して元重みから復元する。これは品質改善に有効だが、蒸留工程とタスクデータが必要になる。既存のBERTを対象とするため、MoEのexpertルーティングやLLMの巨大なembedding、GQA/MQAのKVヘッド設計を自動的に扱うわけではない。公式コードは公開されているものの、他ハードウェアでの速度・品質は別途再評価が必要である。

## 一次資料

- Yau et al., *DAP-BERT: Differentiable Architecture Pruning of BERT*, ICONIP 2021, LNCS 13108, 367–378, DOI:10.1007/978-3-030-92185-9_30。著者公開PDF全12頁、式(1)〜(10)、Algorithm 1、Table 1〜4、Figure 2・3を照合: https://oscaryau525.github.io/uploads/DAP_BERT.pdf
- 出版社DOI: https://doi.org/10.1007/978-3-030-92185-9_30
- 著者公式コード: https://github.com/OscarYau525/DAP-BERT
