---
canonical_id: DOI:10.18653/v1/2023.emnlp-main.298
title: 'GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints'
authors:
- Joshua Ainslie
- James Lee-Thorp
- Michiel de Jong
- Yury Zemlyanskiy
- Federico Lebrón
- Sumit Sanghai
published: 2023-12
publication: EMNLP 2023, pp.4895–4901
publication_type: conference-paper
publication_status: EMNLP 2023採録（公式ACL Anthology）
summary: 多頭注意の既存チェックポイントのK/V投影行列をグループ内平均で統合し、元の事前学習計算量の約5%で追加学習してGQAへ変換する方式。T5.1.1 XXLではGQA-8がMHAに近い品質を維持しながら、平均推論時間1.51秒から0.28秒へ短縮した。ただしTPUv4でのencoder-decoder評価でありdecoder-onlyの直接実証ではない。
list_summary: 既存MHAチェックポイントを平均プーリング＋5%追加学習でGQAへ変換。T5 XXLでMHA近傍の品質とMQA近傍の速度を両立。
source: https://aclanthology.org/2023.emnlp-main.298.pdf
sources:
- https://aclanthology.org/2023.emnlp-main.298.pdf
- https://aclanthology.org/2023.emnlp-main.298/
implementation: JAX/Flaxformer上のT5.1.1 encoder-decoderをTPUv3で追加学習し、TPUv4で評価。論文はFlaxformerを参照するが、本方式専用の著者公式コードリポジトリは一次資料から特定できなかった。
code: null
last_checked: '2026-10-28'
worker_id: scheduled-chat-45
scheduled_slot: '45'
worker_run_key: 20261028-1445-scheduled-chat-45/r01
worker_completed_at: '2026-10-28T14:53:44+09:00'
reference_main_sha: 8015a9b98227c6258dc11bd5909527fcda841f95
quality_self_review_passed: true
quality_self_review_version: PAPER-QUALITY-GUIDE-2026-10-07
last_audited: null
audit_version: 0
references:
- canonical_id: arXiv:2212.08153
  arxiv_id: '2212.08153'
- canonical_id: arXiv:2210.17323
- canonical_id: DOI:10.48550/arxiv.2302.01318
- canonical_id: arXiv:2208.07339
- canonical_id: arXiv:2211.17192
- canonical_id: arXiv:1911.02150
references_checked_at: '2026-10-28'
references_source: primary-pdf-reference-section
references_total: 1
---

# GQA：既存MHAモデルを少量の追加学習でKV共有へ変換する

## 概要

Grouped-Query Attention（GQA）は、Transformerの注意ヘッドごとに別々のKey/Value（K/V）を保存するMulti-Head Attention（MHA）と、全Queryヘッドが単一K/Vヘッドを共有するMulti-Query Attention（MQA）の中間に位置する方式である。MHAでは復号時に各層の過去K/Vを全ヘッド分読み出すため、長い系列や複数要求でメモリ帯域と容量が律速になる。MQAはこれを大幅に削減するが、K/Vを一組に集約することでモデル品質が低下し得る。GQAはQueryヘッドをGグループに分け、各グループ内でK/Vを共有することで、容量・帯域と表現能力を調整できる。

本論文はGQA構造だけでなく、既存MHAチェックポイントを捨てずに変換するuptraining手順も示す。各グループのK/V投影行列を元のヘッドの平均で初期化し、元の事前学習の約5%だけ追加学習する。T5.1.1 XXLの実験では、GQA-8の平均推論時間0.28秒/サンプルに対しMHA-XXLは1.51秒、MQA-XXLは0.24秒だった。品質はMHAに近い一方、速度はMQAに近い。ただし原著の測定はTPUv4上のencoder-decoderモデルであり、今日のdecoder-onlyモデルやGPUカーネルに同じ倍率をそのまま適用できない。

## 問題設定と先行研究との差

通常のMHAではH個のQueryヘッドに対してH個のK/Vヘッドがあり、各生成トークンは過去のH組のK/Vを読む。復号が帯域律速なら、K/Vを読み込むバイト数を減らすことは計算量の削減以上に効く場合がある。ShazeerのMQAはQueryヘッドを保ったままK/Vを1組へ減らすため、理想化するとKVキャッシュ容量と読み出し帯域をH分の1にできる。ただし一組のK/Vに多様な注意パターンを集約するため、元のMHAと同じ精度を常に保てるわけではない。

本研究は既存MHAを新たに一から学習し直すことなく、複数K/Vグループを残して変換する。GQA-1はMQA、GQA-HはMHAと等価で、Gを増やすほどK/V表現力と保存量が増える。既存チェックポイントを平均プーリングで初期化するため、ゼロから学習する方式より小さい追加学習予算で速度・品質の中間点を探せる。重要なのは、この方式が注意行列の数学的な近似だけではなく、K/V投影パラメータそのものを再編成して再学習することにある。

## 手法

### 1. K/V投影行列の平均によるチェックポイント変換

元のMHAでH個のQueryヘッドとH個のK/Vヘッドを持つとする。GQA-GではH個のQueryヘッドをG個のグループへ分け、同じグループのQueryは一つのKeyヘッドと一つのValueヘッドを共有する。変換では、元の各グループに含まれるK/V投影行列を要素ごとに平均し、新しい共有投影行列として使う。例えばH=64、G=8ならQuery8ヘッドごとにK/V一組となり、K/Vキャッシュの主要要素数はMHAの8分の1となる。これはモデルの全メモリが8分の1になるという意味ではなく、重み・一時領域・その他のバッファは別に必要である。

著者は平均プーリング、各グループから一つの既存ヘッドを選ぶ初期化、ランダム初期化を比較し、平均プーリングが最も良い結果を得た。既存のK/Vヘッドの情報を平均で保存するため、変換直後の出力分布が大きく崩れにくい。Query側は元の複数ヘッドを保持し、共有K/Vへの対応を変更する。したがって単純なKVキャッシュ圧縮ではなく、モデルの重みと注意演算の構造を変更する作業である。

### 2. 事前学習レシピを用いる追加学習

チェックポイントを変換しただけでは共有による表現力の損失が残るため、元の事前学習データと最適化レシピを使い、元の事前学習ステップ数の割合αだけ追加学習する。主実験はα=0.05、すなわち元の約5%であり、T5 XXLでは約600 TPUv3チップ日を要した。これは「学習コストが無料」という意味ではない。元モデルを一から学習し直す費用より少ないという比較である。

論文のFigure 5ではMQAは変換直後に品質低下が大きく、追加学習で回復する一方、GQAは変換直後でも比較的良い性能を示す。αを10%まで増やしても改善幅は逓減する。したがって既存モデルの派生チェックポイントを作る場合、どのグループ数と追加学習量が費用対効果に優れるかを実験で選べる。学習前の変換と学習後の推論を分けて評価する必要がある。

### 3. encoder-decoderモデルでの適用範囲

原著ではT5.1.1のデコーダ自己注意とクロス注意にGQA/MQAを適用し、エンコーダ自己注意には適用しない。エンコーダ側は入力系列を並列処理でき、復号時に過去KVを逐次読み直すデコーダほど帯域律速にならないためである。大規模モデルを複数デバイスへ分割すると、単一KVヘッドのMQAでは各デバイスへ同じK/Vを複製する無駄が生じ得る。GQAは複数KVグループを持つため、並列分割とメモリ削減の折衷点を選びやすい。

## 評価条件と主要結果

| 項目 | 原著の実験条件 |
|---|---|
| アーキテクチャ | T5.1.1 encoder-decoder、LargeとXXL |
| 実装・学習 | JAX、Flax、Flaxformer、Adafactor。元の事前学習データとスケジュールで追加学習 |
| 追加学習 | 主実験α=5%、T5 XXLで約600 TPUv3チップ日 |
| 推論時間 | TPUv4、8チップ、各チップ最大バッチ32、モデル別に並列化を最適化 |
| 評価課題 | CNN/DailyMail、arXiv、PubMed、MediaSum、Multi-News、WMT14 En-De、TriviaQA |
| 出力 | 要約はROUGE-1、翻訳はBLEU、質問応答はF1。推論はgreedy |
| 系列長 | CNN/DailyMail・WMT入力512/出力256、その他の要約入力2048/出力512、TriviaQA入力2048/出力32 |

| モデル（原著Table 1） | 平均推論時間/サンプル | 平均ROUGE-1 | WMT BLEU | TriviaQA F1 |
|---|---:|---:|---:|---:|
| MHA-Large | 0.37秒 | 46.0 | 27.7 | 78.2 |
| MHA-XXL | 1.51秒 | 47.2 | 28.4 | 81.9 |
| MQA-XXL（5%追加学習） | 0.24秒 | 46.6 | 28.5 | 81.3 |
| GQA-8-XXL（5%追加学習） | 0.28秒 | 47.1 | 28.4 | 81.6 |

MHA-XXLと比べたGQA-8の時間比は1.51/0.28≒5.39倍である。一方、MQA-XXLと比べると0.28/0.24≒1.17倍の時間を要する。平均ROUGE-1はMHA-XXLの47.2に対してGQA-8が47.1と近い。これは個々の要約タスクの品質が完全一致するという意味ではない。原著のTable 1ではMediaSumがMHA-XXL 36.4に対しGQA-8 36.3、MultiNewsが46.9に対し47.2と、課題ごとに大小関係が変わる。

### 追加学習・グループ数・初期化の感度

Figure 4では平均プーリングが、単一ヘッドの選択やランダム初期化より良い。Figure 5では追加学習を0から5%へ増やすとMQA/GQAとも品質が改善するが、10%では改善が逓減する。Figure 6ではGを1（MQA）から8へ増やす速度費用は比較的小さい一方、MHAに近い64グループへ増やすと時間が増える。8グループは原著が選んだ実用的な中間点であり、あらゆるモデル・ハードウェアで最適という保証はない。

MHA-XXLの1.51秒とGQAの0.28秒という大差は、TPU上の実装と対象系列長に結びつく。元のデコーダ専用モデルでのGPU実測ではなく、重みをロードする帯域、デコーダのKV量、クロス注意の実装、バッチ形状で結果は変わる。KVヘッドを減らすことで理想的なキャッシュ容量は減るが、モデル全体のパラメータ容量や実行時間が同じ比率で減るわけではない。

## 限界・既存研究との差

本論文は既存MHAを少量の追加学習でGQA/MQAへ変換する手順を示し、初期化・グループ数・追加学習量の感度を評価した点が特徴である。MQA単独より品質の落ちにくい中間点を示すが、追加学習に約600 TPUv3チップ日が必要で、無償の推論時最適化ではない。著者はROUGEが要約品質のすべてを測れないこと、同じ計算量でゼロからGQAを学習したモデルとの直接比較がないこと、実験がencoder-decoderに限られることを明示している。decoder-only LLMではK/V共有の効果がさらに大きい可能性を述べるが、当該論文で直接実証したわけではない。

GQAはモデルのK/Vヘッド構造そのものを変えるため、既存のMHAチェックポイントへ推論時の設定変更だけで適用できるとは限らない。変換済み重みと対応するattentionカーネルが必要である。現代のGPU上での実際のTTFT、TPOT、長文脈・高並列サービングの性能は、原著のTPU測定から推測せず、別途検証すべきである。

## 一次資料

- Ainslie et al., *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*, EMNLP 2023, pp.4895–4901, https://aclanthology.org/2023.emnlp-main.298.pdf
- ACL Anthology書誌：https://aclanthology.org/2023.emnlp-main.298/
- 照合箇所：§2（変換とGQA）、§3 Table 1、Figure 3～6（品質、時間、感度）、Limitations（対象範囲と評価の制約）。
