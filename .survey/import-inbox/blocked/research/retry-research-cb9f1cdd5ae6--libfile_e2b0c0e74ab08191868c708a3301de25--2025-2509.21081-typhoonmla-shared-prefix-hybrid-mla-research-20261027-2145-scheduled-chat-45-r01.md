---
canonical_id: "arXiv:2509.21081"
arxiv_id: "2509.21081"
arxiv_categories:
  primary: "cs.LG"
  cross_list:
    - "cs.AI"
title: "TyphoonMLA: A Mixed Naive-Absorb MLA Kernel For Shared Prefix"
authors:
  - "Ahmet Caner Yüzügüler"
  - "Ahmet Çelik"
  - "Jiawei Zhuang"
  - "Lukas Cavigelli"
published: "2025-09-25"
publication: "ICLR 2026 (arXiv v2)"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/pdf/2509.21081v2"
sources:
  - "https://arxiv.org/abs/2509.21081"
  - "https://arxiv.org/pdf/2509.21081v2"
implementation: "Huawei Ascend NPU上のCANN/CATLASS/TorchNPU実装とGPU上のFlashInfer/FlashMLA比較。共有prefixのnaive計算と非共有部分のabsorb計算を統合。公式コミュニティ実装あり。"
code: "https://github.com/huawei-csl/TyphoonMLA-community"
summary: "TyphoonMLAはMLAの共有prefix部分だけを非圧縮naive注意で計算し、各要求固有部分を圧縮absorb注意で計算してLSEで正確に結合する。DeepSeek-v3/Kimi K2の注意カーネルはNPU最大3.0倍、GPU最大3.24倍。DeepSeek-v3の全体TGR最大1.48倍は実測カーネル時間と公開プロファイルを合成した推定であり、128 GPU全体の実測ではない。共有prefix展開によるHBM増分は想定クラスタ条件で約3%。"
list_summary: "MLAの共有prefixをnaive、非共有部分をabsorbで処理しLSEで結合。注意カーネル最大3.24倍、全体TGR最大1.48倍はプロファイル合成推定。共有prefixが短い/小バッチではabsorbへfallback。"
last_checked: "2026-10-27"
worker_id: "scheduled-chat-45"
worker_completed_at: "2026-10-27T21:47:00+09:00"
worker_run_key: "20261027-2145-scheduled-chat-45/r01"
reference_main_sha: "27159e9e4fcd1b88e392adae30ad9781d8b98e7b"
quality_self_review_passed: true
quality_self_review_version: "PAPER-QUALITY-GUIDE-2026-10-07"
worklist_rank: 62
last_audited: null
audit_version: 0
---

# TyphoonMLA：共有prefixだけをnaive展開し、非共有KVをabsorbで保持するMLA推論カーネル

## 概要

DeepSeek-v3やKimi K2で使われるMulti-Head Latent Attention（MLA）は、Key/Valueを低ランク潜在空間に圧縮して保持する。デコード時には、低ランクのまま注意を計算する**absorb**方式がKVのHBM転送量を減らせる。しかしabsorbはQuery側の射影を吸収した計算により、共有prefixを複数要求が再利用する状況でも算術演算が多く、演算性能が律速になりやすい。

TyphoonMLAは、同じMLAを二通りの代数的に等価な計算経路へ分ける。多数の要求が参照する**共有prefix**は、Key/Valueを展開した**naive**注意としてまとめて処理し、各要求だけの**非共有suffix**は圧縮状態を使う**absorb**注意で処理する。両方の部分softmaxをlog-sum-exp（LSE）で結合することで、通常のMLAと同じ注意出力を再構成する。モデル重みの変更・追加学習・近似的なKV削除を必要としない。

原著v2はDeepSeek-v3とKimi K2を用い、Ascend NPUで注意演算の生成token/sを最大3.0倍、GPUで最大3.24倍に改善したと報告する。ただし、**全モデルの生成速度最大1.48倍は、GPU上の注意カーネル実測とDeepSeek公開プロファイルを合成した推定値**であり、128 GPUの本番システム全体を直接計測した値ではない。メモリの増分約3%も特定の並列化・バッチ・文脈長を仮定したモデル上の結果である。カーネル改善、全体性能推定、メモリ見積りを分けて読む必要がある。

## 問題設定：MLAの吸収計算はprefix共有の利得を十分に利用できない

MLAは、各トークンのKVを低ランク潜在ベクトル（位置埋め込みに対応する成分を含む）として保持し、デコード時のHBM読み出し量を減らす。通常のMHAやGQAと比べてキャッシュを小さくできるため、長文脈・大バッチの推論に有利である。一方で、Queryに吸収した射影を用いるabsorb形式では、注意計算のヘッド次元が大きくなり、単純なHBM削減だけでは算術負荷が支配的となる。

多くのLLMサービスでは、共通のシステム指示や長いツール仕様を多数の要求が共有する。さらにTree-of-Thoughtや投機的デコードなど、複数の候補系列が同じ過去トークン列を参照する場合がある。共有prefixに対するKVの読み出しを複数要求で再利用できれば、通常のMHA/GQAではメモリ転送を減らせる。しかしMLAのabsorb注意はもともと転送より演算が律速になりやすく、**同じKVを一度読むだけでは計算量が減らない**。

対照的に、naive形式は低ランクKVを各ヘッドのK/Vへ展開するため、通常のattention行列積に近い演算量で済むが、展開済みKVが大きい。要求固有のKVまで全部naive形式にすると、長いsuffixと大バッチでHBM帯域とキャッシュ容量が問題になる。そこで「共有部分は演算削減を優先」「非共有部分は帯域削減を優先」という異なる目的で実装を切り替える。

## 手法：naive/absorbの二経路と正確なsoftmax結合

### 1. Naiveとabsorbの数学的な違い

naive形式ではMLAの低ランクKVをup-projection行列で展開し、各ヘッドのK/Vを用いて標準的な`softmax(QKᵀ)V`を計算する。Query/Keyのヘッド次元を小さく保てるので算術演算数は少ないが、展開後のK/VをHBMへ保存・読込すると帯域が増える。

absorb形式では、低ランクKVを展開する射影行列をQuery側と出力側へ移動させる。Key/Valueは位置埋め込み成分（PE）と非位置埋め込み成分（noPE）の圧縮表現で保持し、Key/ValueのHBM転送を削減する。代わりにQuery側の次元が拡張され、同じprefixに対して多数のQueryを処理する場合は演算量が増える。

両方式は、MLAの射影行列の結合順序を変えた**数学的に等価な実装**である。softmaxを線形近似したり重要トークンを削除したりする方式ではない。実機の有限精度では演算順序による丸め差が生じ得るため、完全なbitwise一致を保証するという意味ではないが、モデルを再学習して精度を補償する必要はない。

### 2. Prefillで共有prefixのKVを展開しておく

TyphoonMLAはprefillで共有prefixと個別suffixを含む木状の要求集合を処理する。通常のprefix-aware naiveカーネルを用いて低ランクのPE/noPEキャッシュを生成し、共有prefixに対応する部分だけをup-projectionで展開して、共有のK/Vキャッシュとして保存する。要求固有のsuffixは引き続き低ランクのPE/noPE形式で保存する。

共有prefixのup-projectionはprefillのnaive処理で既に必要な計算と重なるため、著者は追加の計算オーバーヘッドがないと説明する。ただし**展開済みの共有K/Vを保持するメモリ費用は残る**。共有prefixが長い場合にHBM使用量が増えるのはこのためである。prefixキャッシュを要求間で一度だけ保存し、個別suffixと別々の物理形式を持たせる設計が前提となる。

### 3. Decodeの二経路

デコードではQueryを位置埋め込みあり/なしの成分に分割し、共有prefixに対しては展開済みのK/Vを読み出してnaive注意を計算する。一方、各要求の非共有suffixに対しては、Queryへ吸収済み射影を適用して圧縮PE/noPEキャッシュを読むabsorb注意を計算する。後者の出力には必要な出力射影を戻す。

原著Algorithm 1では、共有部分の部分出力を`O_N`、正規化用LSEを`l_N`、非共有部分の出力を`O_A`、LSEを`l_A`とする。二つの部分softmaxの正規化分母を利用して、全prefix+suffixを一度にsoftmaxした場合と同じ重み付き平均へ統合する。単純に`O_N+O_A`と足すだけでは、共有部分と非共有部分のsoftmax分母が別々なので正しくない。**LSEによる正規化重み付き結合**が厳密性の要である。

結合は各Queryとヘッドの出力ベクトルに対する演算であり、長いKV系列長に比例する主要なQK/V演算より小さい。原著は結合のHBM読込と演算量が系列長には依存しないと整理する。ただし短い文脈では固定的な結合オーバーヘッドが相対的に目立つ可能性がある。

### 4. 小バッチではabsorbのみへfallback

共有prefixをnaive形式で計算する利点は、同じ展開済みK/Vを十分な数のQueryが共有して初めて現れる。小バッチでは、naiveの大きなHBM読み出し量が演算削減の利点を上回る。そこでハードウェアの計算性能`T`とHBM帯域`M`、ヘッド次元、Query長を使って損益分岐バッチ数`Bθ`を見積もり、それより小さいバッチではabsorb-onlyへ自動で切り替える。

原著式(1)は概念的に`Bθ = ((Dqk+Dv)/(Sq(2Dl+Dr))) × (T/M)`である。DeepSeek-v3とAscend NPU（376 TOPS/s、1.8TB/s）を代入すると閾値は約61となる。実装の閾値はモデル・精度・GPU/NPUの計算/帯域比によって変わる。**小バッチでも常にnaiveを使う設計ではない**ため、少数同時要求のサービスでは実質的に既存absorbと同じ挙動となる。

## 演算量とHBM転送量：共有prefixと非共有suffixの分離

共有長`Ls`、非共有長`Ln`、バッチ`B`、Query長`Sq`、ヘッド数`H`、ヘッド次元`Dqk`/`Dv`、低ランク次元`Dl`、非RoPE/ RoPE次元`Dn`/`Dr`とする。原著Table 1は、naiveが共有・非共有とも展開済みK/Vを読むのに対し、absorbは両方を低ランクのまま読み、TyphoonMLAは共有側だけnaiveへ置き換える構造を示す。

| 方式 | 共有prefix側の主要MAC | 非共有suffix側の主要MAC | 非共有側HBMの傾向 |
|---|---|---|---|
| Naive | `B Sq Ls H (Dqk+Dv)` | `B Sq Ln H (Dqk+Dv)` | 展開K/Vのため大きい |
| Absorb | `B Sq Ls H (2Dl+Dr)` | `B Sq Ln H (2Dl+Dr)` | 低ランクKVで小さい |
| TyphoonMLA | `B Sq Ls H (Dqk+Dv)` | `B Sq Ln H (2Dl+Dr)` | Absorbと同じ低ランクKV |

DeepSeek-v3の次元を代入したTable 1の1024単位のMAC係数では、naiveが共有/非共有とも40、absorbが136、TyphoonMLAが共有40・非共有136となる。したがって**共有部分の演算はabsorb比約3.4分の1**に減り、非共有部分の演算は増えない。HBM読み出しの係数は、naiveの非共有40に対しabsorb/TyphoonMLAの非共有0.56で、**非共有部分では約70倍の転送係数差**がある。これは解析上の係数であり、全モデルの実測速度が3.4倍/70倍になるという意味ではない。

このトレードオフは、長い共通システムプロンプトを大バッチで処理する条件ほど有利である。共通prefixが短い、suffixが長い、同時要求が少ない場合には、共有側の演算削減が全体時間に占める割合が小さくなる。大バッチ化によるHBM容量・スケジューリングの制約も残る。

## 評価条件

| 項目 | 原著v2の条件 |
|---|---|
| モデル | DeepSeek-v3、Kimi K2。MLAの注意演算を評価 |
| データ | MMLU、GSM8K、SimpleQAの質問をサンプリング。完了要求を新しい質問に置換するcontinuous batching |
| 共通prefix | Prompt A 26,472 tokens、Prompt B 7,069、Prompt C 4,759（原著Table 2） |
| バッチ | 64、128、256、512、1024。paged KV-cacheのブロック長128 |
| NPU | Ascend、24 DaVinci cores、HBM64GB、FP16 376 TOPS/s、帯域1.8TB/s |
| NPU比較 | TorchNPU PagedAttentionMLA、CATLASS Absorb-only |
| GPU | 理論FP16 1 PFLOPS/s、HBM帯域3.3TB/sのGPU。FlashMLA、FlashInfer absorb-onlyとの比較 |
| 測定 | 注意カーネルのgenerated tokens/s per layerを実測。全体TGRは別のプロファイル合成推定 |
| メモリ解析 | DeepSeek-v3を384 NPUへ配置し、EP/DP/TP/SPを仮定したHBM footprintモデル |

生成token/s per layerは、注意層を独立に実行したときの処理量である。GPU実験はFlashInferのnaive/absorb実装を組み合わせているため、NPU実装のカーネルと完全に同じコードではない。GPU機種を論文にない型番へ推測して置き換えない。学習済みモデルの重み・データを変更しないため、品質ベンチマークの再学習比較ではなく、計算経路の性能評価が中心となる。

## 定量評価：カーネル・全体推定・HBMを分ける

### 1. NPUとGPUの注意カーネル（Figure 2、Figure 3）

NPU上のDeepSeek-v3/Kimi K2では、MMLU、GSM8K、SimpleQAと三種類のprefix長、バッチ64〜1024を組み合わせ、TyphoonMLAが比較カーネルを約1.2〜3.0倍上回った。長いPrompt Aほど共有部分の比率が大きく、改善幅が大きい。Kimi K2はDeepSeek-v3よりヘッド数が少ないため、共有K/Vの再利用が性能に効きやすいと著者は説明する。

GPUではFlashMLAおよびFlashInfer absorb-onlyと比較し、注意カーネルの最大改善が**3.24倍**となる。図3は各モデル・prefix・バッチのtoken/s per layerを示す。これはモデル全体の生成token/sではない。図から正確に読み取れない棒の値を補間して新たな絶対値として報告しない。NPUの図2では、ベースラインの一部がHBM不足で測定できないため、欠損棒を「速度0」とみなさない。

### 2. カーネル内部の遅延内訳（Figure 4）

Kimi K2相当の構成で共有prefix4096、非共有suffix512、バッチ1024の条件では、CATLASS absorb-onlyの注意部分が6.43ms、TyphoonMLAのnaive共有部分が1.63ms、absorb非共有部分が1.06msだった。共有部分のabsorb推定時間は6.43−1.06=5.37msであり、共有部分だけを比較すると5.37/1.63≈3.29倍となる。これはTable 1のMAC削減係数約3.4と整合する。

ただし、これらは注意部分の計測値であり、射影・CombineLSE・他層の総時間を同じ比率で短縮したという意味ではない。バッチ128未満はabsorbへfallbackするため、Figure 4には表示されていない。バッチが小さく共有prefixを使い回せない条件では、そもそもnaive側の利得が発生しない。

### 3. 全体生成速度の**推定**（Table 3）

原著は128 GPU上のDeepSeek-v3、GPU当たりバッチ128、MMLUについて、GPUで測った注意時間とDeepSeek-AIが公開した他層のプロファイルを合成し、全モデルのtoken generation rate（TGR）を**推定**している。Table 3の数値は次の通りである。

| 共通prefix | FlashMLA注意時間/全体時間 | TyphoonMLA注意時間/全体時間 | FlashMLA TGR | TyphoonMLA TGR | 推定速度比 |
|---|---|---|---:|---:|---:|
| Prompt A（26,472） | 99.1 / 127.2 ms | 58.1 / 86.3 ms | 1.01 kToken/s | 1.48 kToken/s | 約1.47倍 |
| Prompt B（7,069） | 34.5 / 62.6 ms | 25.9 / 54.0 ms | 2.04 kToken/s | 2.37 kToken/s | 約1.16倍 |
| Prompt C（4,759） | 26.9 / 55.0 ms | 22.0 / 50.1 ms | 2.33 kToken/s | 2.56 kToken/s | 約1.10倍 |

著者の要旨にある「end-to-end最大1.48倍」はPrompt Aに対応する**プロファイル合成のTGR推定**である。128 GPUのクラスタを実際に動かして同時要求・通信・MoE全体を測定した結果ではない。長い共通prefixほど推定利得が大きく、短い共通prefixでは約1.10倍まで縮む。注意以外のMoE・集団通信・FFN等が残るため、注意カーネル3.24倍を全体速度へそのまま外挿できない。

### 4. HBM footprintの増分（Figure 5）

共有prefixのK/Vを展開保存するため、absorb-onlyよりHBMを多く使う。著者はDeepSeek-v3を384 NPUに分散し、expert parallelismとdata/tensor/sequence parallelismを組み合わせ、バッチ4K〜32K、最大文脈32K〜256KでHBM使用量を解析した。Prompt Aを共有prefixとしたFigure 5では、例えばバッチ4K・文脈32Kがabsorb 7.80GBに対しTyphoonMLA 8.05GB、文脈256Kが13.03GBに対し13.28GBである。増分は約0.25GBで、割合は前者約3.2%、後者約1.9%となる。

最大バッチ・長文脈の条件では非共有KVとモデル重みが支配的になるため、共有prefixの展開分が総HBMに占める割合は小さくなる。原著の「約3%」はこの仮定の下での結果であり、全モデル・全prefix長・全GPUで常に3%に固定されるわけではない。共有prefixが極端に長く要求数が少ない場合や、単一GPUへ全層を置く場合には比率が変わり得る。

## 既存研究との差

**FlashMLA / ThunderMLA**はMLAのabsorb形式を効率化するが、共有prefixを使い回す際の算術演算を減らすことを主眼にしない。TyphoonMLAはabsorb形式を捨てるのではなく、非共有KVの転送効率を保ちながら共有部分だけnaive形式へ変える。したがって既存のMLA圧縮を無効にする方式ではない。

**FlashAttention / FlashInfer**は通常のMHA/GQAでのタイル化・HBM転送削減を進めてきた。共有prefixを一度読んで複数Queryへ再利用する発想もあるが、MLAのabsorb注意は演算律速のため、HBM削減だけでは十分でない。TyphoonMLAはMLAの代数的な二実装を使い分けることで、**共有部分のMACを削る**という別の律速へ働く。

**PagedAttention / RadixAttention**はKVの物理配置・共有prefixの識別・ページ管理を扱う。TyphoonMLAはそれらのキャッシュ共有が実現していることを前提に、注意計算を効率化するカーネルである。ページングやprefix treeの管理を置き換えるものではない。原著はtensor parallelismとsequence parallelismにも対応できると述べるが、通信を含む実クラスタのスケールアウト実測を網羅したものではない。

## 限界・負の結果・再現性

第一に、**十分な共有prefixと大きなバッチが必要**である。共有部分のKVを展開するため、少数要求ではHBM読込の負担が演算削減を上回る。著者はバッチ閾値未満でabsorb-onlyへfallbackする。Ascend/DeepSeek-v3の解析閾値約61を別GPU・別モデルへそのまま使えない。バッチが小さいローカル対話では利得がほぼない可能性がある。

第二に、**全体TGR最大1.48倍は推定**であり、128 GPUを用いたエンドツーエンド実測ではない。実運用ではMoE expert配置、通信、ロードバランス、scheduler、prefill/decode混合、KVキャッシュの再利用率が変わる。Table 3はそれらの全要素を同時に測定した結果ではなく、注意実測と既存プロファイルを組み合わせたモデルである。

第三に、共有prefixの展開保存はHBMを追加消費する。Figure 5の約0.25GB増分は想定クラスタとPrompt Aの条件であり、単一GPUや異なる長さの共通prefixでは増分割合が変わる。MLAの低ランクKVを完全に捨てるわけではないが、共有部分だけは大きいK/Vを持つ。

第四に、実装は特定のNPU/GPUカーネルに依存する。AscendではCATLASS/TorchNPU、GPUではFlashInferのnaive/absorb実装を用いる。GPUの実測はFP16理論1 PFLOPS/s・HBM3.3TB/sの構成であり、RTX 4070 SuperなどのコンシューマーGPUやCPU推論で同じ倍率になる証拠はない。GPU機種が明記されない場合は推測しない。

第五に、数値演算の順序が変わるため、数学的な等価性と浮動小数点でのbitwise一致は異なる。論文は近似削減を導入しないが、全モデルの下流タスク精度を大量に再評価した研究ではない。実運用では精度差の許容範囲と決定性を検証する必要がある。

第六に、prefix共有率はワークロード依存である。共通システムプロンプトが短い、各要求の固有履歴が長い、prefix cacheが頻繁に失効する、同じprefixを共有する要求が同時に集まらない場合、naive経路へ切り替える効果が小さくなる。共有prefixの存在と、実際の同時再利用率を区別して運用する必要がある。

## 一次資料・照合箇所

- [原著PDF v2](https://arxiv.org/pdf/2509.21081v2)：§2のnaive/absorb、Figure 1、§3.1 Algorithm 1とLSE結合、§3.2 Table 1のMAC/HBM係数・式(1)の閾値、§4 Figure 2/3のNPU/GPUカーネル比較、Table 2の共有prefix長、Figure 4の遅延内訳、Table 3の全体TGR**推定**、Figure 5のHBM footprintを照合。
- [arXiv書誌](https://arxiv.org/abs/2509.21081)：2025-09-25初稿、2026-02-12 v2、cs.LG/cs.AI、著者4名。
- [著者公式実装](https://github.com/huawei-csl/TyphoonMLA-community)：原著脚注の公開先。公開実装の最新バージョンによる全実験の独立再現までは確認していない。

本稿の中心的な評価軸は、MLAの**算術律速と帯域律速を共有/非共有KVで分けること**である。attention kernelの最大3.24倍、全体TGR推定最大1.48倍、HBM約3%増分を異なる測定・解析として扱い、単一の「LLM推論3倍高速化」へまとめない。
