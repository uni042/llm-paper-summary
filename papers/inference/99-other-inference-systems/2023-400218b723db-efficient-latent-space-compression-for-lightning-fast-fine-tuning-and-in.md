---
canonical_id: DOI:10.3390/make5030045
title: Efficient Latent Space Compression for Lightning-Fast Fine-Tuning and Inference of Transformer-Based Models
authors:
- Ala Alam Falaki
- Robin Gras
published: '2023-07-30'
publication: Machine Learning and Knowledge Extraction 5(3), 847–867 (2023)
publication_type: journal-paper
publication_status: 査読誌掲載（MDPI原著HTMLを照合）
summary: 事前学習済みencoderの出力を6層の線形autoencoderで圧縮し、decoderの隠れ次元を減らすseq2seqモデル圧縮。BART-baseでdecoder約96M→40M、要約推論時間5時間9分→2時間20分、ROUGE-1相対約4.5%低下。翻訳では推論改善が約9%、分類では改善なしという負の結果も報告。
list_summary: encoder出力の潜在次元をautoencoderで圧縮しBART decoderを小型化。要約は約2.2倍高速化、分類では利得なし。
source: https://www.mdpi.com/2504-4990/5/3/45
sources:
- https://www.mdpi.com/2504-4990/5/3/45
- https://doi.org/10.3390/make5030045
implementation: BART-baseのencoderと事前学習済みautoencoderを凍結し、小型decoderを学習。V100 32GBで要約、翻訳、分類を評価。著者コードはhttps://github.com/AlaFalaki/compressedBART。
code: https://github.com/AlaFalaki/compressedBART
last_checked: '2026-10-28'
worker_id: scheduled-chat-45
scheduled_slot: '45'
worker_run_key: 20261028-1445-scheduled-chat-45/r01
worker_completed_at: '2026-10-28T14:54:59+09:00'
reference_main_sha: 8015a9b98227c6258dc11bd5909527fcda841f95
quality_self_review_passed: true
quality_self_review_version: PAPER-QUALITY-GUIDE-2026-10-07
last_audited: null
audit_version: 0
---

# 潜在表現の次元圧縮によるBARTの軽量化：学習と推論の費用・品質交換

## 概要

本研究はTransformerの各層を単純に削るのではなく、encoderが生成する隠れ表現をautoencoderで低次元へ写像し、その小さい次元に合わせてdecoderを再設計する。encoder-decoder構造では、encoder出力の隠れ次元がdecoderの内部表現やクロス注意へ影響する。著者は事前学習済みencoderを凍結し、別途学習したautoencoderの圧縮部分を介して小型decoderへ渡すことで、学習対象のパラメータ数と推論時の計算・メモリを削減する。

BART-baseを用いた要約では、decoderパラメータを約96Mから40Mへ削減した条件で、ROUGE-1が相対4.5%低下する一方、推論時間は5時間9分から2時間20分へ短縮した。著者は推論時間54%減、約2.2倍の速度改善を報告する。ただし翻訳では推論速度改善が約9%にとどまり、分類では改善がほぼない。これは「どのTransformerにも2倍速い」方式ではなく、自己回帰的なdecoderが実行時間の大部分を占めるseq2seqタスクで有利になる手法である。

## 問題設定と関連方式との差

通常の剪定は重みや注意ヘッドを取り除き、量子化は各重み・活性値のビット数を下げる。本研究はencoderの出力次元そのものを減らし、後段decoderを小さくする。低ランク分解や蒸留と組み合わせられるが、それらを同時に評価したわけではない。対象はBARTなどのencoder-decoderであり、decoder-only LLMのKVキャッシュ圧縮とは機構が異なる。encoderが生成した系列長Sの隠れ状態は通常S×Dで、D=768の次元をCへ圧縮する。系列長Sはそのまま残すため、長文脈のトークン数そのものが減るわけではない。

事前学習済みencoderの出力をPCAや単一の線形層で圧縮する方法も考えられる。しかし著者の比較では、複数層の線形autoencoderを先に学習し、圧縮部分を凍結してから小型decoderを学習する方が良かった。autoencoderを同時にゼロから学習するAE-Sや、単純なlearnable linear projection（LL）も比較対象に含めている。入力表現の再構成を事前に学習しておくことが、decoderの小型化による品質低下を抑えるための重要な工程となる。

## 手法

### 1. Encoder、autoencoder、小型decoderの接続

原著Figure 1では、事前学習済みTransformer encoderの出力Xを、autoencoderの圧縮器AE_encでZへ写像し、小型decoderに渡す。Xの形状はS×D、ZはS×Cで、Sは系列長、Dは元の隠れ次元、Cは圧縮後の隠れ次元である。検証ではS=512、D=768を主に用い、Cを32、128、384、512などに変えて容量と品質の関係を測る。Cを小さくすると後段decoderの内部行列も小さくできる一方、encoderが保持していた意味情報が失われる危険が増える。

autoencoderは圧縮器3層と復元器3層の計6層の線形ネットワークを採用する。まずencoderの出力を入力として、AE_dec(AE_enc(X))がXを再構成するように学習する。原著Table 1では、潜在次元64で6層の線形autoencoderのMSEが0.0766であり、6層LSTMの0.0810、6層CNNの0.2659より低い。4層・8層の線形構成よりも6層が良いというアブレーションもある。autoencoderを学習した後は復元器を推論経路から外し、圧縮器だけをencoderとdecoderの間に挿入する。

### 2. 学習する部分と圧縮率の決定

encoderとAE_encを凍結し、後段のdecoderをタスクに合わせて学習する。したがってautoencoder自体のパラメータが存在しても、下流タスクで更新する重みは主にdecoderとなる。圧縮次元C=384では元の768次元から半分になり、検証用の3層decoderではBART encoderとの組合せで約48Mから24Mへ減る。実運用に近いBART-base構成ではdecoder約96Mから40Mへ縮小する条件を評価した。単に潜在表現を圧縮しただけではなく、圧縮後の次元に対応する新しいdecoderを学習する点が重要である。

圧縮率はタスクの許容品質低下とハードウェアの制約で選ぶ。Cを32のように極端に下げると再構成誤差が増え、要約品質も大きく悪化する。C=384では要約品質が比較的維持され、パラメータ削減の効果が大きい。autoencoderを学習したデータと下流タスクのデータが異なっても一定の転移性が示されるが、あらゆるドメインで成立する保証ではない。凍結するencoderの品質、語彙、タスクが変われば最適なCも変わる。

### 3. 学習・評価パイプライン

原著はCNN/DailyMailとNewsroomの訓練集合を組み合わせ、その一部でautoencoderを事前学習する。要約はCNN/DailyMail、翻訳はWMT16ルーマニア語→英語、分類はSentiment140を使う。学習にはAdamと1cycle学習率スケジュールを使い、要約・翻訳はROUGEやBLEU、分類はaccuracyで評価する。GPUはV100 32GBで、タスクごとにバッチサイズが異なる。原著の速度値はこれらの実装とデータ長に依存するため、異なるバッチの単純な相互比較は適切でない。

## 評価結果

### 要約：decoder削減と時間・メモリの関係

| 指標 | BART-base基準 | BART+AE（C=384） | 解釈 |
|---|---:|---:|---|
| decoderパラメータ | 約96M | 約40M | 約60%削減 |
| ROUGE-1 | 基準100% | 基準の約95.5% | 相対約4.5%低下 |
| 要約推論時間（テスト集合） | 5時間9分 | 2時間20分 | 約54%短縮、約2.2倍高速 |
| fine-tuning時間 | 基準 | 約45%短縮 | 一度の下流学習が軽い |
| fine-tuning GPUメモリ | 基準 | 約57%削減 | 凍結と小型decoderの効果 |
| 推論GPUメモリ | 基準 | 約20%削減 | モデル全体のメモリは60%減ではない |

この表のパラメータ削減はdecoderに関する値で、encoderやautoencoderを含むモデル全体のパラメータが60%減ったことを意味しない。GPUメモリも学習時57%減に対し推論時20%減であり、別の尺度である。ROUGE-1の4.5%低下は相対的な値で、絶対4.5ポイントの低下ではない。著者は生成例の見た目では品質劣化が小さいと説明するが、ROUGEが示すn-gram重複の低下自体は残る。学習時のバッチ16、推論時のバッチ32など条件を固定して比較している。

### 翻訳と分類：利得が縮む負の結果

WMT16ルーマニア語→英語翻訳では、C=384に圧縮した場合、BLEUが約10%低下し、fine-tuning時間は約55%短縮、推論速度の改善は約9%にとどまる。推論時GPUメモリ削減は約14%、学習時は約37%である。著者は翻訳の出力系列が平均約25語で、要約の約50語より短いことを一因として挙げる。decoderを小型化しても逐次生成するトークン数が少なければ、encoderや固定オーバーヘッドの比率が大きくなり、速度改善が小さくなる。

分類ではdecoderの代わりに小さい分類ヘッドを使うため、潜在表現を圧縮しても計算を削る余地が少ない。Sentiment140でC=504の条件は分類ヘッドを約55%小さくするが、accuracyは約8%低下し、予測時間はほとんど改善しない。凍結encoderだけを使う方が品質面で有利な条件もあり、autoencoderを追加するとむしろわずかな実行費用が増える。これは本方式が万能のモデル圧縮ではなく、重い自己回帰decoderを持つモデル向けの構造的な軽量化であることを示す。

### アブレーションと再現上の注意

線形autoencoderの6層構成が、比較したLSTMやCNN、異なる層数より再構成MSEが低い。事前学習済みAEを凍結する方式は、AE-S（同時学習）、単一線形射影、PCAと比較して要約品質が高い。小さいCでは表現力の損失が大きくなるため、圧縮率を上げるほど必ず良くなるわけではない。元のencoderの種類をBERT、DistilBERT、BART encoderへ変えた場合にも傾向が変わる。例えばC=384はBART encoderと組み合わせた小型decoderで48M→24Mの削減を示すが、BART-base実験の96M→40Mと混同しない。

## 限界と既存研究との差

この方法は事前学習済みencoderの出力次元を削り、decoderの行列サイズを減らす。モデルの層を取り除く剪定や低ビット量子化と異なり、内部表現を再構成するautoencoderの事前学習が必要である。学習済みAEのドメイン転移性は一定程度示されるが、対象はBARTを中心とするseq2seqであり、decoder-onlyのLLMやMoE、KVキャッシュの長文脈推論を直接評価していない。速度はV100上のタスク別実測であり、最新GPUのカーネル、バッチサイズ、入力長で同じ倍率になるとは限らない。

分類で改善がないこと、翻訳では品質低下の割に速度利得が小さいこと、要約でもROUGEが低下することを主要な負の結果として扱う。論文はautoencoderと他の圧縮手法の組合せを将来課題として述べるが、剪定・蒸留・量子化を同時に適用した実測値を本論文の成果として扱わない。著者の公式GitHubは実装とチェックポイントの参照先であり、今回の調査でコードを再実行したわけではない。

## 一次資料と実装

- Falaki and Gras, *Efficient Latent Space Compression for Lightning-Fast Fine-Tuning and Inference of Transformer-Based Models*, Machine Learning and Knowledge Extraction 5(3), 847–867 (2023), https://www.mdpi.com/2504-4990/5/3/45
- DOI：https://doi.org/10.3390/make5030045
- 公式コード：https://github.com/AlaFalaki/compressedBART
- 確認箇所：§3（encoder/AE/decoder）、§4（学習と評価）、§5.1（AEアブレーション）、§5.2（要約）、§5.3（翻訳）、§5.4（分類）、§6（結論）。
