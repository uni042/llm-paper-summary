---
canonical_id: "arXiv:2306.09539"
summary: "Block-State Transformerは長系列をブロック並列Transformerで処理し、ブロック間の長距離状態をS4等の状態空間モデルへ分離する。再帰ブロック間依存を外すことで層単体をBlock-Recurrent Transformer比6〜11倍高速化し、構造化S4版は65k系列へ長さ一般化する。"
list_summary: "ブロック内注意と並列計算可能なSSM長距離状態を組み合わせ、再帰Transformerの逐次ブロック依存を除去して長系列層を6〜11倍高速化する。"
worker_id: "scheduled-chat-30"
worker_completed_at: "2026-10-03T09:34:23+09:00"
worker_run_key: "20261003-0934-scheduled-chat-30"
reference_main_sha: "6b02faee2b755ab277a4737be7abbab1fc431249"
---
# Block-State Transformers

## 書誌
- 著者: Mahan Fathi, Jonathan Pilault, Orhan Firat, Christopher Pal, Pierre-Luc Bacon, Ross Goroshin
- 正規識別子: `arXiv:2306.09539`
- 一次資料: https://arxiv.org/abs/2306.09539

## 概要
Block-State Transformer（BST）は、長系列を固定長ブロックへ分けて各ブロックのTransformer計算を並列化し、ブロック間の長距離情報だけを状態空間モデル（state space model; SSM）の状態として伝えるハイブリッド構造である。Block-Recurrent Transformerのように前ブロックの再帰状態を逐次待つ必要がなく、長文脈を持ちながらGPU並列性を回復する。

BSTはSSM状態を注意へ入れる位置により単一ヘッド（single-head; SH）、多ヘッド（multi-head; MH）、多フィルタ（multi-filter; MF）などを構成する。構造化S4カーネルを使う版では、学習時より長い系列へカーネルを延長でき、65kトークンまでの長さ一般化を評価している。

GPU上の層単体前向き計算ではBST:SHがBlock-Recurrent Transformerより6〜11倍、BST:MHが3〜4倍高速。65k系列でも最大約6倍の改善が残る。品質面ではPG19、arXiv、GitHubの自己回帰言語モデル評価とLong Range Arenaで、再帰型・局所型基準と比較する。

## 問題設定
局所窓Transformerはブロック内部を並列化できるが、窓外情報を失う。再帰型Transformerはブロック間状態を保持できるが、次ブロックが前ブロック状態に依存するため、系列方向に逐次依存が生じGPUを十分並列利用できない。

BSTは長距離記憶をSSMへ分離する。SSMは系列全体の状態を畳み込みとして並列計算でき、各ブロックのTransformerはその状態を参照しながら同時実行できる。

## 手法
### ブロック並列化
系列を幅Wのブロックへ分け、ブロック内は通常のTransformer注意で局所関係を処理する。従来のブロック再帰方式のようにブロックiの出力を待ってi+1を始めるのではなく、SSMが提供する長距離状態を介して複数ブロックを並列処理する。

### SSM状態の注入
S4などのSSMが系列全体から長距離状態を生成する。SH版は共有状態を注意へ与え、MH版はヘッドごと、MF版は複数フィルタでより豊かな状態を作る。MFはパラメータが増えるがarXiv/GitHubで良いPPLを示し、局所性の強いPG19ではSHが有利という差も観測される。

### 構造化・非構造化カーネル
S4の構造化カーネルはA/B/C行列から任意系列長Lへ再構成できるため、学習窓を超える長さへ一般化できる。非構造化畳み込み版は自由度が高く学習長付近では強いが、16k/65kへ外挿するとPPLが悪化する。

## 評価条件
|項目|内容|
|---|---|
|言語データ|PG19、arXiv、GitHub|
|規模|約200M/400M中心、付録で1.3Bまでスケーリング|
|学習窓|512または2048/4096等|
|長さ一般化|512、16k、65k|
|効率層測定|GPU、window 128、SSM state 16、16 heads、embedding 512|
|比較|Block-Recurrent Transformer、Transformer-XL、GSS-Hybrid、Sliding Transformer等|

## 主要結果
BST:SH層はBlock-Recurrent Transformerより6〜11倍、BST:MHは3〜4倍高速。65kトークンでもハードウェア飽和が始まるまで最大約6倍の差が残る。4k付近でBlock-Recurrent層と単純Sliding層の差が約15倍ある条件でも、BSTはその差を2倍未満へ縮める。

長さ一般化ではBST:SH:S4-Lが65kでPG19、GitHub、arXivの三データセットすべてで最良PPLを示す。非構造化MF版は学習長4kで強いが、未学習の16k/65kで悪化する。Long Range ArenaではBST:SH:S4が平均86.96で、S4の86.09やBlock-Recurrent Transformerの60.80を上回る。

## 既存研究との差
Block-Recurrent Transformerは長距離状態を再帰的に更新するためブロック間逐次依存がある。BSTは状態更新をSSMへ置き換え、畳み込みとして並列化することでこの依存を外す。純粋SSMと異なり、局所ブロック内ではTransformer注意を残すため、局所的な内容ベース検索を維持する。

## 限界
層単体の高速化は完全なLLMサービングのtoken/sではない。主要モデル規模は200M〜400Mで、付録のスケーリングも1.3Bまでである。S4版の計算量はSSM内部状態サイズNにも依存し、報告性能はN=16。65k付近ではハードウェア飽和で利得が縮む。

## 一次資料
- https://arxiv.org/abs/2306.09539