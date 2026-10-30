---
canonical_id: "arXiv:2510.11602"
arxiv_id: "2510.11602"
arxiv_categories:
  primary: "cs.CL"
  cross_list:
    - "cs.LG"
title: "Deconstructing Attention: Investigating Design Principles for Effective Language Modeling"
summary: "Transformerの注意機構をトークン混合、QK-softmaxの数学的形式、入力系列依存性、現在層QK依存性へ分解し、同規模のUniformとHybridモデルで比較する。500M級ではUniform Non-approximateのWikiText PPLが9025.9に悪化する一方、標準attentionを半数残すHybridは39.4で標準38.1に近い。単独では弱い機構も標準層と相補的に機能するが、推論速度の実測優位は未検証。"
list_summary: "attentionの四原理を制御実験で分離。トークン混合は不可欠だが標準層とのHybridではsoftmaxやQK依存を緩和可能。"
authors:
  - "Huiyin Xue"
  - "Nafise Sadat Moosavi"
  - "Nikolaos Aletras"
published: "2025-10-13"
publication: "arXiv:2510.11602v1 (2025-10-13)"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/pdf/2510.11602"
sources:
  - "https://arxiv.org/pdf/2510.11602"
  - "https://arxiv.org/abs/2510.11602"
implementation: "同じパラメータ規模の70M/160M/500MモデルをSlimPajama最大15Bトークンで学習し、Uniform、Hybrid、Skip構成でPPL・NLU・注意パターンを比較。単一MI300Xで学習・評価。"
code: null
last_checked: "2026-10-30"
worker_id: "scheduled-chat-45"
worker_completed_at: "2026-10-30T16:32:25+09:00"
worker_run_key: "20261030-1616-scheduled-chat-45/r02"
reference_main_sha: "dcd875600edd459637c98aa8eb1f739b68d7633f"
quality_self_review_passed: true
quality_self_review_version: "PAPER-QUALITY-GUIDE-2026-10-07"
---

# Deconstructing Attention：言語モデルに必要な注意機構の設計原理を分解する

## 概要

本論文は、Transformerの標準的なdot-product attentionが備える性質を四つに分け、それぞれを緩和した代替機構を同じパラメータ規模で事前学習することにより、何が言語モデルの予測性能に不可欠かを検証する。四つの性質は、(1)異なるトークン位置間で情報を混合すること、(2)QK内積とsoftmaxに基づく数学的形式、(3)注意重みが入力系列に依存すること、(4)QueryとKeyが現在層の隠れ状態に結び付くことである。

結果は、トークン混合そのものをなくすと性能がほぼランダムに崩壊する一方、softmaxや入力依存性、現在層QKへの依存は一定範囲で緩和できるというものだった。特に、奇数層に簡易機構、偶数層に標準attentionを置くhybrid構成では、単独で学習が破綻する機構でも良好な性能を示す。500M級モデルのWikiText困惑度（文脈長2048）は標準attention 38.1に対し、hybridのNon-approximateが39.4、FixedSeqQKが38.5、StaticEmbQKが38.7である。逆に全層をNon-approximateへ置き換えるuniform構成では9025.9へ悪化する。したがって、注意機構の性質を単独層の強さだけで評価せず、標準層との相補性を考慮する必要がある。

これは言語モデルの設計原理を調べる制御実験であり、実運用GPUでの推論スループットが何倍になるかを示した研究ではない。FLOPs、KVキャッシュ、計算量の解析はあるが、理論計算量の改善とエンドツーエンドの速度を混同してはならない。

## 問題設定と四つの設計原理

標準attentionは、各位置のQueryとKeyの内積を計算し、softmaxで正規化してValueの重み付き和を作る。この仕組みには複数の性質が同時に含まれるため、性能の源泉が何かを切り分けにくい。著者らは、次の四つを独立した設計要素として扱う。

**Token Mixing**は異なる位置の表現を混ぜ、単一トークンだけでは得られない文脈情報を伝える性質である。**Mathematical Form**はQK内積・softmaxという標準attentionの数式を保つ性質である。**Sequence-Dependency**は入力系列が変われば注意行列も変わる性質である。**Current QK**は現在の層の隠れ状態からQとKを計算する性質である。

これらの性質は相互に関連するが、必ずしも全てを同時に保持する必要はない。例えば固定されたQK表現を使ってもトークン位置間の混合はできるし、softmaxを別の正規化へ置き換えても系列間情報の伝達は可能である。逆に、層内のMLPだけを残してトークン間混合をなくすと、文脈を利用した次トークン予測が困難になる。著者らはこの違いを同一規模の事前学習実験で分離する。

## 比較する注意機構

### 標準attentionとToken Mixingを除いたMLP

標準attentionは、入力からQ/K/Vを計算し、因果マスク付きの内積softmaxで過去位置を参照する。比較用のMLP変種は位置ごとの写像だけを使い、系列内の他トークンを混合しない。これは「attentionの代わりに単純なMLPを置くとどうなるか」という対照条件であり、MLP-Mixerのような位置方向混合を持つ別アーキテクチャと同一ではない。

uniformのMLPでは文脈長を128から2048へ増やしてもWikiText PPLが993.5のままで、文脈を利用できない。hybridでは81.3から45.8へ改善するが、標準38.1には届かない。標準attention層を半分残すことで文脈情報を利用できるが、簡易層の性能は混合を行う代替機構より低い。

### ApproximateとNon-approximate：標準softmax形式を緩和

ApproximateとNon-approximateは、QK内積とsoftmaxに忠実な標準attentionの数学的形式を緩和し、系列長に線形な計算を目指す機構である。両者には再帰的な計算形があり、原著Appendix Iで詳述される。Non-approximateはApproximateよりdecode時の活性メモリ、KVキャッシュ、FLOPs/iterationを削減できる可能性がある。一方、uniformでNon-approximateを全層へ適用すると、500M級モデルの学習は不安定でPPLが約9000へ悪化する。hybridで半分の層に標準attentionを残すと39.4まで回復する。

これは線形attentionが単独では常に失敗するという意味ではない。論文ではQwen3のQ/K正規化を備えたモデルではuniform Non-approximateが収束する例も確認している。正規化の配置、モデル構造、学習設定に依存するため、同じ代替機構でもホストアーキテクチャによって結果が変わる。

### RndEmbQKとFixedSeqQK：入力系列への依存を緩和

RndEmbQKは入力内容に依存しないランダムな埋め込みからQ/Kを構成し、FixedSeqQKは固定された事前定義系列に基づいてQ/Kを構成する。いずれも注意スコアを入力内容から独立させるため、共通の注意行列を前計算・キャッシュできる可能性がある。計算が入力ごとに変わらないからといってトークン混合がなくなるわけではなく、Value側を通じて系列の情報は伝わる。

ただし固定パターンだけでは実際の語順・構文・意味に適応しにくい。uniformの文脈長2048でRndEmbQKは84.8、FixedSeqQKは79.1のPPLとなり、標準38.1から大きく悪化する。hybridではそれぞれ39.3、38.5へ改善する。固定QKは事前計算に向くが、前計算可能性がそのまま高速化を保証するわけではない。行列のロード・キャッシュ・バッチ共有・メモリ階層まで含めた実装が必要である。

### StaticEmbQK：現在層の隠れ状態からQKを切り離す

StaticEmbQKは、現在層の文脈化済み表現ではなく静的なトークン埋め込みからQ/Kを計算する。現在層に依存しない注意行列を用意できるため、層をまたぐ事前計算やprefetchの余地がある。しかし標準attentionと同じ二乗の計算構造を残すため、単独では計算量の次数を下げない。

uniformでは文脈長2048のPPLが79.9と標準38.1より悪いが、hybridでは38.7となる。入力内容に応じた注意の柔軟性を制限しても、標準層が一部に残れば他の層が補助的な情報混合を担える。これはCurrent QKの性質が各層で絶対必要というわけではないことを示すが、全層で不要だと主張するものではない。

## 実験設計

著者らはSlimPajamaで約500Mパラメータのモデルを最大150億トークン事前学習し、バッチ当たり約50万トークン、系列長2048、Pythiaの英語中心50K BPEトークナイザを用いる。主実験は単一AMD Instinct MI300Xで行う。異なる注意機構のパラメータ数を揃え、単純にモデルを小さくした効果を除外する。70Mと160Mのモデルでも同様の比較を行い、モデルサイズ依存性を調べる。

**Uniform**は全Transformer層に同じ簡易注意機構を置く。**Hybrid**は奇数層に簡易機構、偶数層に標準attentionを置く。**Skip**はhybridとして学習したモデルから簡易機構を持つ奇数層を学習なしで取り除き、残差経路だけで同じ効果が得られるかを調べる。これらは同じパラメータ規模を揃えて学習したモデルと、学習後に層を削除した対照を区別するための実験設計である。

評価はWikiTextやLAMBADAの言語モデリング、SciQ、RTE、HellaSwagなどのNLU課題、文脈長128～2048でのPPLを含む。さらにattention行列のentropy、concentration、head diversity、初期トークンへのattention sink、近傍位置へのlocal focusを解析し、性能が近い構成でも内部の注意パターンがどう異なるかを調べる。

## 主要な結果

### 文脈長別のWikiText PPL（原著Table 3、低いほど良い）

| 機構 | Uniform 128 | Uniform 2048 | Hybrid 128 | Hybrid 2048 |
|---|---:|---:|---:|---:|
| Standard | 69.9 | 38.1 | ― | ― |
| MLP | 993.5 | 993.5 | 81.3 | 45.8 |
| Approximate | 81.7 | 47.9 | 71.8 | 39.4 |
| Non-approximate | 10023.7 | 9025.9 | 69.0 | 39.4 |
| RndEmbQK | 107.1 | 84.8 | 72.4 | 39.3 |
| FixedSeqQK | 100.5 | 79.1 | 69.0 | 38.5 |
| StaticEmbQK | 104.8 | 79.9 | 70.1 | 38.7 |

StandardのPPLは文脈を128から2048へ伸ばすと69.9から38.1へ改善する。トークン混合のないMLPは文脈長を伸ばしても993.5のまま変わらない。Uniform Non-approximateは約9000とほぼ破綻するが、Hybrid Non-approximateは39.4へ回復する。Hybrid FixedSeqQKは38.5、StaticEmbQKは38.7で標準38.1に近い。ここから、標準attentionの数学的形式・入力依存・現在層QKの全てを各層で維持する必要はないが、適切な混合経路が全体として必要だと読める。

### NLUタスクと相補性（Table 1～2、Figure 4）

500M級の標準attentionモデルはWikiText PPL 38.1、SciQ正答率60.2%、HellaSwag28.3%程度を示す。Hybrid Non-approximateやRndEmbQKはWikiText PPLで標準に近く、SciQなどのNLU課題でも近い範囲に収まる。Uniform MLPやUniform Non-approximateは多くの課題でランダム推測に近い。70M・160M・500Mへサイズを変えた実験では、Hybridの性能が規模とともに改善する。例えばNon-approximateのARC-E正答率は70Mの34.3%から500Mの42.3%へ上がる。

一方、Hybridモデルから簡易層を削除するSkip実験では、残った標準層だけで性能が維持されるわけではなく、NLU平均がランダム推測以下へ落ち、PPLも爆発する。これは簡易層が単なる不要な残差通路ではなく、標準層と共同して情報変換に寄与していることを示す。したがってHybridの成功を「標準attention層だけが全ての仕事をしている」と解釈するのは誤りである。

### 注意パターンの違い（Figure 1、7～8）

Uniformの標準attentionやRndEmbQKでは上位層が特定の位置へ強く集中する場合がある。Hybridでは同じ上位層でもentropyが増え、初期トークンへのattention sinkが弱まる。Non-approximateのHybridでは、偶数の標準層が広い情報混合と集中を担い、奇数の簡易層がattention sinkや平均poolingに似た役割へ分化する。個々の簡易層が単独では弱くても、標準層との組合せで有用な役割を獲得する可能性がある。

FixedSeqQKは固定された系列に対する適応を学んでしまい、入力系列への一般化を損ねる可能性がある。RndEmbQKは構文情報を十分に表現できない可能性がある。StaticEmbQKは層ごとの適応性が低い。これらは著者らの観測からの機構的解釈であり、各headの役割が厳密に因果的に証明されたわけではない。

### 標準層の割合と配置（Table 11、§6）

24層モデルでは偶数層だけ標準にする50%構成のほか、25%の標準層を4、8、12、16、20、24層へ配置する構成、最初・最後の層だけ標準にする構成などを比較する。標準attentionを25%程度残せる場合、残りをより単純な機構へ置き換えても比較的良い精度を保つ例がある。しかし標準層を1～2層まで減らす極端な構成では、代替機構にも重要な設計原理を保つ必要がある。標準層の配置や割合による差は、単に層数を数えるだけでは予測できない。

### 理論的な計算・キャッシュ費用（Appendix E～H）

標準attentionのprefillには系列長Lに対する二乗項があり、decodeでは過去KVの読出しが必要になる。ApproximateとNon-approximateのような線形化された機構は、系列長に線形な計算形を持ち、Non-approximateはdecodeのキャッシュ・活性メモリを減らせる可能性がある。RndEmbQKやFixedSeqQKは注意スコアが入力に依存しないため、事前計算して複数リクエストで共有する設計が考えられる。StaticEmbQKはQKが層の隠れ状態から独立するため、層をまたぐ先読みが可能だが、理論上の二乗計算自体は残る。

ただしこれらは計算量・メモリ式と設計上の可能性であり、同じGPUで実際に推論したtokens/sやTTFT、TPOTの比較ではない。前計算した行列の保存・転送、専用カーネルの実装、バッチサイズによる費用は別途必要になる。論文の目的は高速化製品の完成ではなく、attentionのどの性質を緩和できるかの制御実験である。

## 既存研究との差

Linear Transformer、RWKV、SSM、Mamba、token mixer、cross-layer attention sharingなどの既存研究は、特定の高速化機構を提案することが主眼である。本論文は標準attentionの四つの性質を明示的に切り分け、パラメータ規模と事前学習条件を揃えてUniformとHybridを比較する。ある代替機構が単独では学習失敗しても、標準attention層と組み合わせると良好になるという相補性を実験的に示す点が重要である。

この知見は、全層を一度に新機構へ置き換えるより、少数の標準attention層を残したハイブリッドアーキテクチャを探索する設計指針につながる。もっとも、Qwen3でNon-approximateがUniformでも収束するという観測があるため、正規化やモデル規模が変われば必要な原理の強さも変わる。

## 限界・負の結果

第一に、主なモデル規模は最大500M、学習トークンは最大15B、英語中心の単一トークナイザであり、数十BのMoEや長文脈の本番LLMへ同じ結論を直接外挿できない。第二に、文脈長は主に2048までで、100K級の長文脈・実際のKVオフロード・マルチGPUの挙動は未検証である。第三に、GPU推論の実測速度・消費電力・P99遅延は主要結果ではないため、理論FLOPs削減を実効性能改善と混同しない。

第四に、Uniform Non-approximateの大幅な性能崩壊は、別アーキテクチャや正規化方式では起こらない場合がある。第五に、Hybridの良好なPPLは学習済みモデルの性質であり、既存の標準Transformerから奇数層を後付けで置換しても同じ性能が得られるという意味ではない。第六に、簡易層を削除したSkipの失敗は、簡易層が役に立っていることを示すが、どの情報をどの層が伝えるかを完全に特定したものではない。

実務での含意は、注意機構を軽量化する際に「全層で同じ置換を使う」ことを当然視せず、少数の標準層と線形・固定QKなどの簡易層を組み合わせる設計を評価することにある。モデルの学習安定性、品質、理論計算量、実際の推論速度を別々に測る必要がある。標準層を残すことで学習が安定しても、実行時の専用カーネルがなければ高速化につながらない可能性がある。

## 一次資料

- Huiyin Xue、Nafise Sadat Moosavi、Nikolaos Aletras、*Deconstructing Attention: Investigating Design Principles for Effective Language Modeling*、arXiv:2510.11602v1、2025年10月。§3～6（Table 1～3、Figure 1・4）、Appendix E～H（FLOPs・キャッシュ）、Appendix P（層配置）を照合。https://arxiv.org/pdf/2510.11602
- arXiv公式書誌：https://arxiv.org/abs/2510.11602
