---
canonical_id: arXiv:2608.12435
arxiv_id: '2608.12435'
arxiv_categories:
  primary: cs.LG
  cross_list: []
title: 'MARCH: Scaling Recurrent Memory with Content-Routed State Anchors'
summary: MARCHは再帰モデルの累積状態を一定間隔で状態アンカーとして保存し、各アンカーの内容を反映した小次元の鍵で過去状態を選択的に読み出す。現在状態の再帰経路を維持したまま長距離記憶を拡張し、Gated DeltaNetを基底とする50Bトークン事前学習でLongBench平均を11.9から14.9へ改善した。アンカー間隔・密/Top-4経路に応じて記憶容量と速度を調整できる。
list_summary: 累積再帰状態を周期保存し、内容依存ルーティングで必要な過去状態だけを読み、固定サイズ再帰記憶の長距離検索を改善する。
authors:
- Ming Zhang
- Kaisen Yang
- Shu Yu
- Ermo Hua
- Ning Ding
- Xia Hu
- Bowen Zhou
- Chaochao Lu
- Youbang Sun
published: '2026-08-12'
publication: arXiv preprint
publication_type: preprint
publication_status: preprint
source: https://arxiv.org/html/2608.12435v1
sources:
- https://arxiv.org/html/2608.12435v1
- https://arxiv.org/abs/2608.12435
- https://arxiv.org/pdf/2608.12435
implementation: Gated DeltaNetの再帰更新を基盤に、累積状態を生成するproducerと履歴を融合読出しするreaderを実装し、密ルーティングとTop-4を比較した。一次論文から公式コードの確実な公開先は確認できなかった。
code: null
last_checked: '2026-10-08'
worker_completed_at: '2026-10-08T18:40:34+09:00'
worker_run_key: 20261008-1834-scheduled-chat-30/r01
last_audited: '2026-10-08'
audit_version: 2026-10-07-v1
references:
- canonical_id: arXiv:2607.25357
  arxiv_id: '2607.25357'
- canonical_id: OpenReview:LY3ukUANko
  openreview_id: LY3ukUANko
- canonical_id: arXiv:2304.09433
  arxiv_id: '2304.09433'
- canonical_id: DOI:10.18653/v1/2024.acl-long.172
  doi: 10.18653/v1/2024.acl-long.172
- canonical_id: DOI:10.18653/v1/2025.acl-long.183
  doi: 10.18653/v1/2025.acl-long.183
- canonical_id: arXiv:2602.24281
  arxiv_id: '2602.24281'
- canonical_id: arXiv:2501.00663
  arxiv_id: '2501.00663'
- canonical_id: arXiv:2004.05150
  arxiv_id: '2004.05150'
- canonical_id: arXiv:2412.09764
  arxiv_id: '2412.09764'
- canonical_id: DOI:10.1609/aaai.v34i05.6239
  doi: 10.1609/aaai.v34i05.6239
- canonical_id: arXiv:2509.24552
  arxiv_id: '2509.24552'
- canonical_id: arXiv:2607.07386
  arxiv_id: '2607.07386'
- canonical_id: DOI:10.18653/v1/2023.emnlp-main.232
  doi: 10.18653/v1/2023.emnlp-main.232
- canonical_id: arXiv:1904.10509
  arxiv_id: '1904.10509'
- canonical_id: OpenReview:Ua6zuk0WRH
  openreview_id: Ua6zuk0WRH
- canonical_id: OpenReview:Y8YVCOMEpz
  openreview_id: Y8YVCOMEpz
- canonical_id: arXiv:1803.05457
  arxiv_id: '1803.05457'
- canonical_id: arXiv:2205.14135
- canonical_id: arXiv:2307.08691
  openreview_id: mZn2Xyh9Ec
- canonical_id: arXiv:2509.15763
  arxiv_id: '2509.15763'
- canonical_id: arXiv:2502.13685
  arxiv_id: '2502.13685'
- canonical_id: DOI:10.18653/v1/n19-1246
  doi: 10.18653/v1/n19-1246
- canonical_id: DOI:10.1002/spe.4380240306
  doi: 10.1002/spe.4380240306
- canonical_id: DOI:10.5281/zenodo.5371629
  doi: 10.5281/zenodo.5371629
- canonical_id: arXiv:2312.00752
  arxiv_id: '2312.00752'
- canonical_id: OpenReview:uYLFoz1vlAC
  openreview_id: uYLFoz1vlAC
- canonical_id: OpenReview:mOJgZWkXKW
  openreview_id: mOJgZWkXKW
- canonical_id: arXiv:2605.22791
  arxiv_id: '2605.22791'
- canonical_id: OpenReview:kIoBbc76Sy
  openreview_id: kIoBbc76Sy
- canonical_id: arXiv:2607.02980
  arxiv_id: '2607.02980'
- canonical_id: DOI:10.18653/v1/p17-1147
  doi: 10.18653/v1/p17-1147
- canonical_id: DOI:10.18653/v1/2024.emnlp-main.1124
  doi: 10.18653/v1/2024.emnlp-main.1124
- canonical_id: DOI:10.1162/tacl%5fa%5f00276
  doi: 10.1162/tacl%5fa%5f00276
- canonical_id: arXiv:1907.05242
  arxiv_id: '1907.05242'
- canonical_id: arXiv:2407.14207
  arxiv_id: '2407.14207'
- canonical_id: DOI:10.18653/v1/n19-1309
  doi: 10.18653/v1/n19-1309
- canonical_id: arXiv:2502.13189
  arxiv_id: '2502.13189'
- canonical_id: arXiv:2604.20920
  arxiv_id: '2604.20920'
- canonical_id: DOI:10.18653/v1/d18-1260
  doi: 10.18653/v1/d18-1260
- canonical_id: arXiv:2304.08467
- canonical_id: arXiv:2401.06104
  arxiv_id: '2401.06104'
- canonical_id: arXiv:2507.16577
  arxiv_id: '2507.16577'
- canonical_id: DOI:10.18653/v1/p16-1144
  doi: 10.18653/v1/p16-1144
- canonical_id: arXiv:2305.13048
  doi: 10.18653/v1/2023.findings-emnlp.936
- canonical_id: arXiv:2504.08934
  arxiv_id: '2504.08934'
- canonical_id: arXiv:2404.07904
  openreview_id: y6SqbJfCSk
- canonical_id: DOI:10.18653/v1/p18-2124
  doi: 10.18653/v1/p18-2124
- canonical_id: arXiv:2003.05997
  doi: 10.1162/tacl%5fa%5f00353
- canonical_id: DOI:10.1609/aaai.v34i05.6399
  doi: 10.1609/aaai.v34i05.6399
- canonical_id: arXiv:2102.11174
  arxiv_id: '2102.11174'
- canonical_id: arXiv:2502.10297
  arxiv_id: '2502.10297'
- canonical_id: arXiv:2404.02882
  arxiv_id: '2404.02882'
- canonical_id: arXiv:2307.08621
  arxiv_id: '2307.08621'
- canonical_id: DOI:10.18653/v1/n19-1421
  doi: 10.18653/v1/n19-1421
- canonical_id: arXiv:2406.10774
- canonical_id: arXiv:2506.15545
  arxiv_id: '2506.15545'
- canonical_id: arXiv:2606.10650
  arxiv_id: '2606.10650'
- canonical_id: arXiv:2402.18510
  arxiv_id: '2402.18510'
- canonical_id: DOI:10.1609/aaai.v35i16.17664
  doi: 10.1609/aaai.v35i16.17664
- canonical_id: arXiv:2412.06464
  openreview_id: r8H7xhYPwz
- canonical_id: arXiv:2502.11089
  doi: 10.18653/v1/2025.acl-long.1126
- canonical_id: arXiv:2007.14062
- canonical_id: DOI:10.18653/v1/p19-1472
  doi: 10.18653/v1/p19-1472
- canonical_id: arXiv:2401.03462
  arxiv_id: '2401.03462'
- canonical_id: arXiv:2306.14048
- canonical_id: arXiv:2601.00671
  arxiv_id: '2601.00671'
- canonical_id: DOI:10.18653/v1/2025.acl-long.1245
  doi: 10.18653/v1/2025.acl-long.1245
references_checked_at: '2026-10-04'
references_source: arxiv-html-reference-section
references_total: 76
under16kb_reaudit_target_path: papers/inference/99-other-inference-systems/2026-2608.12435-march-scaling-recurrent-memory-with-content-routed-state-anchors.md
under16kb_reaudit_source_git_blob_sha: 4b2bf3503d0006db1e2eb8265e7d27986ebd706e
under16kb_reaudit_version: 2026-10-07-v1
under16kb_reaudit_passed: true
quality_self_review_passed: true
quality_self_review_version: 2026-10-08-semantic-v1
quality_body_chars: 5025
quality_method_chars: 1502
quality_eval_chars: 1354
quality_limitation_chars: 546
---

# MARCH: Scaling Recurrent Memory with Content-Routed State Anchors

## 概要

MARCHは、再帰型言語モデルの「過去を固定サイズの状態に圧縮するため、後から古い情報を取り出しにくい」という問題を、累積再帰状態の履歴保存と内容に基づく検索で緩和する構造である。通常の全注意機構は各トークンの鍵・値を保存して任意の過去へ直接アクセスできるが、推論のKVキャッシュは文脈長に比例して増える。Gated DeltaNetのような再帰モデルは一つの行列状態を逐次更新するため復号が軽い一方、後続トークンによる忘却・上書きで古い関連付けが弱くなる。

MARCHは再帰状態の更新式を変更せず、例えば512トークンごとにその時点までの累積状態を状態アンカーとして保存する。各アンカーには内容を反映した小さなルーティング鍵を結び付け、現在トークンが必要な過去状態を重み付きで読み出す。履歴を使わない選択肢も学習するため、通常の再帰経路を残したまま必要時だけ過去の状態を加える。全トークンのKVを保存するのではなく、過去の圧縮状態を時間方向に増やす中間的な設計である。

著者らはGated DeltaNetを基底として50Bトークン・16K文脈で事前学習し、常識推論、長文理解、文脈内検索、針探し検索を比較した。LongBenchの平均はGated DeltaNetの11.9から14.9、文脈内検索は20.5から23.3へ改善した。過去状態の読出しには追加費用があり、128KではTop-4の疎ルーティングが密なMARCHの学習処理量を2倍超に改善する。精度向上と計算費用の交換条件を含めて評価すべき研究である。

## 問題設定：固定状態の長距離記憶

全注意機構はトークンごとの鍵・値を記憶し、現在の問い合わせと過去の鍵の類似度から必要な値を取り出す。長い系列の学習では全トークン間の相互作用が二次的に増え、復号ではKVキャッシュが系列長とともに増加する。対照的に線形注意は、値ベクトルと鍵ベクトルの外積を行列状態S_tへ蓄積し、現在の問い合わせq_tに対してS_t q_tを計算する。状態のサイズは文脈長に依存しないが、古い情報と新しい情報が同じ行列へ重なる。

Gated DeltaNetは保持ゲートと差分更新を使い、以前の関連付けを適応的に書き換える。それでも履歴は単一の現在状態へ圧縮され、忘却された古い表現への直接の参照経路は存在しない。例えば長い文書の冒頭にあった特定のキーと値の対応を、末尾の質問で再び要求すると、途中の更新で対応が上書きされている可能性がある。単に状態次元を大きくすると毎トークンの更新費用が増えるため、容量拡張だけでは計算効率との両立が難しい。

MARCHは「毎トークン更新する現在状態」と「時々保存し必要なときに読む過去状態」を分離する。過去状態は各区間だけの独立メモリではなく、その区間の終端までの累積状態の複製である。これにより、その後の忘却で弱まった情報の以前の表現へ再アクセスできる。ただしアンカーの数は文脈長に応じて増えるため、固定メモリ再帰モデルの定数メモリ性をそのまま維持するものではない。

## 手法

### 1. 累積再帰状態の周期チェックポイント

入力トークン列を一定長Cの区間に分け、各境界b_mの直後に共通の学習済みアンカートークンξ_mを挿入する。テキスト位置では従来どおりGated DeltaNetの状態S_tを更新し、境界に到達するとA^(m)=S_(b_m)を保存する。アンカー位置は状態を更新せず、直前に保存した状態を読むための補助位置として扱う。再帰の連続性を保ったまま、過去の状態の時間的な軌跡を記録する設計である。

アンカーは区間ごとに再初期化した状態ではない。m番目のアンカーは文脈の先頭からb_mまでを処理した累積状態であり、後の更新で失われた情報をその時点の表現として保持する。既定のC=512なら16K文脈で32個のアンカーが生まれる。Cを小さくすると時間解像度は高まるが、保存状態と検索候補が増える。Cを大きくすると費用は減るが、情報が変化した重要な区間の表現を取り逃す可能性がある。

### 2. 内容依存のルーティング鍵

各アンカー位置の正規化された隠れ表現u_mから、射影W_kによって小次元の鍵κ_mを作る。同じアンカー埋め込みを使っていても、アンカー位置は自分に対応する累積状態を読み、その結果が次の層の隠れ表現へ伝わる。このため、二層目以降の鍵は時刻の番号だけでなく、保存状態の内容を反映する。過去状態を選ぶ基準が単なる新しさや固定した時間尺度ではない点が本質である。

現在のテキスト位置tでは、隠れ表現x_tから別の射影W_Rでルーティング問い合わせρ_tを作り、因果的に見えるアンカーの鍵κ_mとの内積をスコアにする。将来のアンカーは候補に含めず、b_m<tを満たす履歴だけを参照する。さらに「過去状態を使わない」というnull選択肢を追加し、全候補にソフトマックスをかけて重みπ_(t,m)を求める。不要な履歴があるときにはnullが重みを引き受け、古い状態からの干渉を抑える。

### 3. 現在状態と履歴状態の残差融合

通常の再帰読出しはS_t q_tである。MARCHは、同じ状態読出し問い合わせq_tで各アンカーA^(m)を読み、その結果をπ_(t,m)で重み付けして加える。最終出力は現在状態の読出しに、過去アンカーの加重読出しを残差として足した形になる。nullの状態はゼロなので、履歴が不要なら通常の再帰出力を保持できる。ルーティング確率は言語モデルの出力へ直接影響するため、アンカー鍵と問い合わせは通常の言語モデリング損失で端から端まで学習できる。

この構造ではルーティング用の問い合わせρ_tと、保存された行列状態を読む問い合わせq_tの役割が異なる。前者はどの時点の累積状態が有用かを選び、後者はその状態の内容を読み出す。過去の個別トークンを再度全注意するのではなく、圧縮された過去の状態の間で選択する。全注意と単一状態再帰の中間の記憶表現であり、アンカーの間隔と選択数によって費用を調整できる。

### 4. 融合読出しとTop-4疎ルーティング

実装は、再帰更新とアンカー生成を行う生産段、履歴状態を読む読出し段に分かれる。読出し段は問い合わせトークンとアンカーをタイル化し、ルーティングスコア計算、オンラインソフトマックス、状態読出しの重み付き蓄積を融合する。これにより、全トークン×全アンカーの密な重み行列や、各アンカーの候補読出しを大きな中間テンソルとして高帯域メモリへ書き出さない。

長文脈でアンカーが多い場合は、各トークン・各ヘッドについて上位4個のアンカーだけを集約する疎方式も使う。Top-4は履歴読出し費用を減らすが、密な方式と全く同じ精度ではない。論文の消去実験では常識推論と文脈内検索では近い成績を維持する一方、針探し検索では精度が低下する。つまり疎化は無料の高速化ではなく、記憶検索の完全性との交換条件がある。

## 評価：実験設定・定量結果・消去実験

### 学習条件と比較対象

| 項目 | 一次論文の条件 | 注意点 |
|---|---|---|
| 学習データ | Long-Data-Collectionsの50Bトークン | 大規模商用モデルの学習ではない |
| 学習文脈 | 16Kトークン | 32Kの針探しは長さ外挿 |
| モデル | 21層、隠れ次元1536 | 主要比較で構成を合わせる |
| Gated DeltaNet | 約793Mパラメータ | 主な再帰比較対象 |
| Transformer | 21層693M、24層778M | 深さ合わせと規模合わせ |
| MARCH | ルーティング次元64、アンカー間隔512 | 既定構成 |
| 学習 | 全モデル同じ50B、16K、最適化設定 | 比較の統制条件 |
| ベンチマーク | 常識推論8件、LongBench12件、文脈内検索6件、RULER針探し | 課題別に指標が異なる |

比較対象は通常のGated DeltaNet、対数線形注意を付加したGated DeltaNet、全注意Transformerの二構成である。50Bトークンを同じ16K文脈で学習したため、記憶構造の違いを比較しやすい。ただしTransformerの21層版は再帰モデルよりパラメータが少なく、24層版で規模を近づけている。長文脈での優劣を述べるときは、学習時の16Kを超える32K評価が長さ外挿であることも区別する必要がある。

### 常識推論と長文理解

| 指標 | Gated DeltaNet | 対数線形版 | MARCH | 読み取り |
|---|---:|---:|---:|---|
| 常識推論8件平均 | 40.1 | 40.0 | 41.5 | 再帰モデル内で改善 |
| OpenBookQA | 30.0 | 30.4 | 32.8 | 通常版比+2.8ポイント |
| LongBench12件平均 | 11.9 | 12.5 | 14.9 | 通常版比相対約25%改善 |
| 2WikiMultihopQA | 8.7 | 8.2 | 11.5 | 複数文書の検索 |
| MuSiQue | 2.1 | 3.3 | 4.8 | 強い再帰基準比約45%増 |
| QMSum | 11.3 | 13.2 | 17.4 | 強い再帰基準比約32%増 |
| 文脈内検索6件平均 | 19.2 | 20.5 | 23.3 | 強い再帰基準比相対約14%改善 |

MARCHは常識推論8件の平均で41.5となり、通常Gated DeltaNetの40.1、対数線形版の40.0を上回った。LongBenchでも通常版の11.9から14.9へ改善したが、24層Transformerの平均15.4には届いていない。すべての全注意モデルを超えたわけではない。改善は複数文書質問応答、要約、少数例学習など複数の課題に及び、単一の針探しだけに最適化した結果ではない。

文脈内検索の平均は20.5から23.3へ上昇し、SQuADでは強い再帰基準比約8%、TriviaQAでは約23%の相対改善を報告する。ただし同じ表では24層Transformerが33.2であり、圧縮状態の履歴参照を追加してもトークン単位の全注意との精度差は残る。MARCHの主張は再帰モデルの記憶能力を改善することであり、全注意をあらゆる課題で凌駕することではない。

### 針探し・長さ外挿・学習効率

RULERの針探しでは、4K、8K、16K、32Kの長さで単一・複数のキー値検索を試した。24の課題・長さ組合せのうち、MARCHは強い再帰基準に19件で勝ち、残る5件で同点だった。32Kは学習文脈16Kの外側であり、6課題すべてでMARCHが最良だった。単一針の一部では完全正解を維持したが、残る課題は非ゼロの成績という水準であり、すべて100%の検索精度ではない。

128Kの学習処理では、Top-4疎ルーティングは密なMARCHの2倍超の処理量を示し、主要な混合演算の実行時間をおよそ一桁短縮した。FlashAttention-2より高い処理量を示す条件もあるが、過去状態を追加読出ししない通常のGated DeltaNetは依然として速い。したがって再帰モデルの計算効率を完全に保持したまま無料で記憶を拡張するわけではない。

### アンカー間隔とルーティングの消去実験

| 設定 | アンカー数（16K） | 8K針探し平均 | 16K針探し平均 | 解釈 |
|---|---:|---:|---:|---|
| C=256 | 64 | 49.25 | 44.83 | 密だが費用増 |
| C=512 | 32 | 54.96 | 39.46 | 論文の既定 |
| C=1024 | 16 | 43.21 | 33.54 | 粗い時間解像度 |
| C=2048 | 8 | 39.83 | 27.96 | 記憶が粗すぎる |

アンカー間隔を短くすると候補が増え、検索精度が改善する場合があるが、必ず単調に改善するわけではない。C=256は16K針探しでC=512を上回る一方、8KではC=512の方が高い。推論時だけCを変える実験では、C=256がSQuADやSWDEで有利な条件もある。木構造で状態数を対数個へ抑えるFenwick方式は費用を減らせるが、検索精度は大きく下がる。したがってアンカー数と精度の関係は用途に依存する。

ルーティング次元を64から192へ増やすと一部の文脈内検索が改善する一方、常識推論や針探しの平均は低下した。Top-4では常識推論41.38、文脈内検索23.17と密方式の41.48、23.31に近いが、16K針探しは39.46から31.21へ下がる。null選択肢を削除すると常識推論、LongBench、検索、針探しのすべての集計が悪化した。不要な履歴を読まない分岐が精度面でも有効である。

## 既存研究との差

Gated DeltaNetは状態の書込み規則を工夫して干渉を抑えるが、現在状態一つに全履歴を圧縮する。MARCHは書込み規則を変えず、以前の累積状態を保存して読み出し先を増やす。Log-Linear Attentionのような階層的な状態保存とは異なり、各アンカーに内容を反映した鍵を付け、現在の問い合わせとの関連度で選ぶ。全注意の疎化はトークンやブロックのKVを選ぶのに対し、MARCHは圧縮された再帰状態の履歴を選ぶ点で検索単位が異なる。

全注意の長距離検索能力を、固定状態の軽い復号に近づけるための中間的な設計である。ただし各アンカーは過去の累積状態を保存するため、文脈長に応じたメモリ増加を許す。トークン単位のKV保存と比べれば粗い圧縮履歴だが、通常の再帰モデルの定数状態メモリよりは大きい。速度・メモリ・検索精度の交換条件を持つ方式として位置付けられる。

## 限界と適用範囲

固定間隔でアンカーを保存するため、状態がほとんど変化しない区間では冗長な複製が生まれ、重要な情報が急変する区間では保存密度が足りない可能性がある。著者ら自身も状態の新規性や更新量に応じた適応的なアンカー配置、冗長なアンカーの統合・破棄を今後の課題に挙げる。現在の実装は単一の同質なアンカー集合を使い、短期記憶と長期記憶を別々に特化させる仕組みではない。

保存したアンカーは各層の累積行列状態であり、アンカー数が増えるほど記憶容量と読出し候補が増える。Top-4による疎化は高速化できるが、針探し精度を落とす。密な方式も履歴読出しを伴うため、通常のGated DeltaNetより遅い条件がある。全注意と比べた優位は入力長、学習規模、実装、ハードウェアで変わる。

評価モデルは約7〜8億パラメータ級で、50Bトークン・16K文脈の学術的な学習条件である。より大規模なモデル、異なる言語、極端に長い文脈、分散サービングで同じ精度と速度の交換条件が成立するかは検証されていない。LongBench平均14.9は24層Transformerの15.4を下回り、文脈内検索23.3もTransformerの33.2より低い。長距離記憶を改善したことと、全注意の精度を全面的に代替したことを区別する必要がある。

## 一次資料

- 著者論文HTML: https://arxiv.org/html/2608.12435v1
- 書誌・公開日: https://arxiv.org/abs/2608.12435
- 著者論文PDF: https://arxiv.org/pdf/2608.12435