---
title: "LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding"
summary: "学習時のlayer dropoutとearly-exit損失により、同一モデルで早期終了とself-speculative decodingを可能にする手法。"
authors_affiliations: "Meta AIほか（ACL 2024、著者詳細は一次資料参照）"
published: "2024-08-12"
publication_status: "Published"
lineage: "Conditional computation"
topics: ["Dynamic depth","Speculative decoding","Quality-cost"]
importance: "中"
hardware_evaluation: "実機"
source: "https://aclanthology.org/2024.acl-long.681/"
code: "https://github.com/facebookresearch/LayerSkip"
last_checked: "2026-09-02"
---

# LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding

> 学習時のlayer dropoutとearly-exit損失により、同一モデルで早期終了とself-speculative decodingを可能にする手法。

## 概要
この構成は追加分類器を持たない。
通常の別モデルdraftでは、draftの重み・KV・メモリを別に持つため、速度向上と引き換えに常駐メモリが増える。LayerSkipは同じ前半層を共有するため、このコストを抑えつつ、残り層を検証器として再利用できる。さらに一つの共有LM headで全出口を採点するため、出口ごとの追加分類器を設計しなくてよい。
LayerSkipは、同じdecoderの途中層を小さいdraftモデルとして使い、早期退出（early exit）とself-speculative decodingを一体化する端到端手法である。通常のLLMは全層を通すまで各トークンの予測を確定できないが、途中層の表現が十分に読出し可能なら、そこから候補列を出し、残り層で一括検証・訂正できる。推論時に別draftモデルをロードしないため、通常のspeculative decodingよりメモリが小さく、draft/verifyで前半層の計算とactivationを共有できる。核心は学習レシピで、層dropout率を前半で低く後半で高くし、全層に同一LM headでearly-exit lossを課す。これによって途中層の出力分布を最終層へ整列させる。Llama系の複数サイズ、スクラッチ事前学習・継続事前学習・コード/タスクfine-tuningに適用し、重みを専用推論器へ変換せずに速度を上げる。論文は要約CNN/DM最大2.16倍、コード1.82倍、TOPv2 semantic parsing 2.0倍を報告する。
## 手法のあらまし
また、検証層は同一モデルの残り層であり、別モデルのロードや重み転送を要しない。この共有がメモリ削減と速度向上の根拠になる。
学習では各sampleごとにdropout maskを変えるため、同じ重みが複数の出口深度を経験する。推論時は出口層Eでd個を連続生成し、残り層を一回のparallel forwardにまとめる。受理率が十分高ければ、浅層draftの計算を低コストで再利用できる。
各層lを確率的にdropoutするが、後段ほど最大dropout率pmaxを大きくする。学習中のlayer-dropoutは異なる深さの共有重みsubmodelを同時に訓練する効果があり、early-exit lossは層lのhidden stateを共通LM headに通したcross-entropyを加える。学習は全層の能力を保ちつつ浅い層の予測精度を押し上げる。推論のearly exitではE層まで計算して候補をdトークン生成し、残りL−E層で候補をparallel verificationする。正しいprefixはそのまま受理し、最初の不一致位置は検証分布から訂正するので、理想的には完全モデルと同じ分布を保つ。前半層はdraftとverifyで同じ順に通るため、activation/KVを共有できる。出口層Eとspeculation長dは品質と速度のトレードオフを作る。layer dropout率、時間方向のcurriculum、early-exit loss重み、rotational curriculum（各層を順番に重視）を調整し、浅層が過度に弱くならないようにする。
## 評価
本実験では継続事前学習とスクラッチ学習を分け、CNN/DM・XSUM・HumanEvalでROUGE/受理率/毎秒tokenを比較する。自己推測の速度は出口層Eとdraft長dの組合せに依存し、浅すぎる出口では訂正が増え、深すぎる出口ではdraft計算が重くなる。
継続事前学習ではLlama 2 7B/13Bを52Bトークンの自然言語・コード混合コーパスで訓練し、CNN/DM、XSUM、HumanEvalをNVIDIA H100で評価。7BのCNN/DMは自己推測E=8,d=12でROUGE-2 0.078（自回帰0.079）、受理率68.9%、62.7→127.9 token/s、1.86倍。XSUMはROUGE-2 0.073を保ち1.54倍、HumanEvalは0.042で1.83倍。13BはCNN/DM1.81倍、XSUM1.34倍、HumanEval1.66倍。スクラッチ26BトークンではLlama 2 1.5BがCNN/DM 1.76倍、7Bが2.16倍で、同一トークン数の非LayerSkip学習より浅層精度が高い。論文の要約ではCNN/DM最大2.16倍、コード1.82倍、TOPv2 2.0倍。early exit単独は高速でも品質を失い、self-speculationが補正する。限界は、self-speculationには専用レシピで再学習/fine-tuningが必要（Draft&Verifyは重み変更不要）、pmax・escale・rotational間隔・出口層・dの調整が必要、スクラッチ時は学習率を上げないと精度を維持しにくいこと。受理率が低い出口やd過大では検証計算が増え、深層モデルでは速度利得が小さくなる。
## 一次資料
- [論文](https://aclanthology.org/2024.acl-long.681/)
- [公式コード](https://github.com/facebookresearch/LayerSkip)
## 更新履歴
- 2026-09-02: 概要・手法・評価を一次資料に基づき拡充。

