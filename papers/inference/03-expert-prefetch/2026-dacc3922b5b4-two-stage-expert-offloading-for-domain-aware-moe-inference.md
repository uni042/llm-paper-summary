---
canonical_id: DOI:10.1109/ACCESS.2026.3665697
doi: 10.1109/ACCESS.2026.3665697
arxiv_categories:
  primary: null
  cross_list: []
title: Two-Stage Expert Offloading for Domain-Aware MoE Inference
summary: GPUメモリに全MoEエキスパートを常駐させる高メモリ費用と、CPUへ退避して必要時に転送するI/O待ちの両方を抑えるADEPTを提案する。プリフィルではプロンプトの意味領域を軽量埋込みで同定し、領域別に事前集計したエキスパート短縮リストだけを階層的にGPUへ読み込む。デコードでは直近利用、層間相関、領域情報をランダムフォレストへ入力して次に必要なエキスパートを予測し、現在層の計算とCPU→GPU転送を非同期に重ねる。DeepSeek-MoE-16B、RTX A6000、20GB制約で、シミュレーションI/O待ちを50%削減し、HF Accelerateのオンデマンド退避基準に対する投影TPOTを3797msから1100msへ短縮して3.45倍、全常駐比のピークメモリを33%削減した。
list_summary: 領域別プリフィル事前読込と時間・層間・領域局所性によるデコード先読みを組み合わせ、MoEのCPU退避でI/O待ち50%削減、投影TPOT 3.45倍高速化、全常駐比33%メモリ削減を狙う。
authors:
- Hangyeol Kim
- Honguk Woo
- Younghwan Kim
authors_affiliations: Sungkyunkwan University; Korea Electronics Technology Institute
published: '2026-02-17'
publication: IEEE Access, vol.14, pp.33610-33624, 2026
publication_type: Journal article
publication_status: Received 2026-01-19, accepted 2026-02-03, published 2026-02-17, current version 2026-03-05.
lineage: MoE expert offloading、expert caching、prefetch、domain-aware routing
topics:
- MoE推論
- エキスパート退避
- GPUメモリ
- 先読み
- キャッシュ
- 領域適応
importance: プリフィルのピークメモリとデコードの反復I/Oを別々の局所性で最適化し、領域事前知識とトークン時系列予測を一つの退避パイプラインに統合した点が重要。
hardware_evaluation: NVIDIA RTX A6000単一GPU。実世界基準検証では20GB GPUメモリ制約。DeepSeek-MoE-16B、27 エキスパート 層、各64 エキスパート、ルーティング top-k=6。
quality_effect: K=32のプリフィル予算では全64 エキスパート容量の63%の精度を保持する一方、K=16では大幅な精度低下。最終TPOT比較ではモデル出力品質は基準と同一と報告。
references:
- canonical_id: arXiv:1810.04805
  title: BERT
- canonical_id: arXiv:1701.06538
  title: Sparsely-Gated Mixture-of-Experts
- canonical_id: arXiv:2006.16668
  title: GShard
- canonical_id: arXiv:2202.08906
  title: ST-MoE
- canonical_id: arXiv:2112.06905
  title: GLaM
- canonical_id: arXiv:1910.02054
  title: ZeRO
references_checked_at: '2026-09-23'
references_source: IEEE Access CC BY 4.0全文の参考文献節
references_total: 37
source: https://doi.org/10.1109/ACCESS.2026.3665697
sources:
- https://doi.org/10.1109/ACCESS.2026.3665697
- https://www.researchgate.net/publication/400888358_Two-Stage_Expert_Offloading_for_Domain-Aware_MoE_Inference
implementation: コアアルゴリズムとシミュレータ設定は論文中に記載。ソフトウェア登録手続中のため完全な公開コードは未公開。GPU キャッシュはPython OrderedDict、予測器はRandom Forest。
last_checked: '2026-09-23'
code: null
last_audited: null
audit_version: 0
---

# Two-Stage Expert Offloading for Domain-Aware MoE Inference

> 領域別プリフィル事前読込と時間・層間・領域局所性によるデコード先読みを組み合わせ、MoEのCPU退避でI/O待ち50%削減、投影TPOT 3.45倍高速化、全常駐比33%メモリ削減を狙う。
## 書誌情報
- **著者**: Hangyeol Kim, Honguk Woo, Younghwan Kim
- **著者・所属**: Sungkyunkwan University; Korea Electronics Technology Institute
- **公開**: IEEE Access, vol.14, pp.33610-33624, 2026
- **種別**: Journal article
- **対象**: MoE推論、エキスパート退避、GPUメモリ、先読み、キャッシュ、領域適応
- **実装**: コアアルゴリズムとシミュレータ設定は論文中に記載。ソフトウェア登録手続中のため完全な公開コードは未公開。GPU キャッシュはPython OrderedDict、予測器はRandom Forest。
## 概要
GPUメモリに全MoEエキスパートを常駐させる高メモリ費用と、CPUへ退避して必要時に転送するI/O待ちの両方を抑えるADEPTを提案する。プリフィルではプロンプトの意味領域を軽量埋込みで同定し、領域別に事前集計したエキスパート短縮リストだけを階層的にGPUへ読み込む。デコードでは直近利用、層間相関、領域情報をランダムフォレストへ入力して次に必要なエキスパートを予測し、現在層の計算とCPU→GPU転送を非同期に重ねる。DeepSeek-MoE-16B、RTX A6000、20GB制約で、シミュレーションI/O待ちを50%削減し、HF Accelerateのオンデマンド退避基準に対する投影TPOTを3797msから1100msへ短縮して3.45倍、全常駐比のピークメモリを33%削減した。

ADEPTはプリフィルとデコードを同じキャッシュ規則で処理せず、プリフィルにはプロンプト意味領域と事前計測した領域別エキスパート分布、デコードには時間局所性・層間相関・領域を使う。領域判定は専用分類器を学習せずGTE-base等の埋込みと領域medoidで行い、各領域・各MoE層について累積ゲート確率95%を覆う最大8 エキスパートの短縮リストを作る。デコード側はRandom Forestで次エキスパート集合を予測し、現在計算中に非同期先読みする。段階ごとのボトルネックを分離しつつ同じGPU エキスパート キャッシュへ接続する二段構成が中心的差分である。
## 問題設定
MoEは各トークンで少数エキスパートしか使わないが、全エキスパート重みをGPUへ常駐させればメモリが大きく、CPUへ退避すればルータ判定後のPCIe転送が逐次推論を停止させる。プリフィルでは多数トークンを同時処理するため必要エキスパート集合が広がりピークVRAMが問題になり、デコードでは各トークンの活性数は少ないが同じ転送待ちが数百回累積する。従来の量子化や単純LRU、オンデマンド退避はメモリか遅延の片方へ寄りやすい。論文は二つの推論段階で異なる予測可能性を利用し、最初に必要集合を絞り、その後は次トークンを先読みすることでメモリとI/O待ちを同時に下げる。
## 新規性
ADEPTはプリフィルとデコードを同じキャッシュ規則で処理せず、プリフィルにはプロンプト意味領域と事前計測した領域別エキスパート分布、デコードには時間局所性・層間相関・領域を使う。領域判定は専用分類器を学習せずGTE-base等の埋込みと領域medoidで行い、各領域・各MoE層について累積ゲート確率95%を覆う最大8 エキスパートの短縮リストを作る。デコード側はRandom Forestで次エキスパート集合を予測し、現在計算中に非同期先読みする。段階ごとのボトルネックを分離しつつ同じGPU エキスパート キャッシュへ接続する二段構成が中心的差分である。
## 手法
### 手法のあらまし
オフラインではCode、Math、Science、Creative、Businessの各領域から埋込み代表を作る。各領域でk-meansにより50クラスタを作り、中心に最も近いmedoidを代表ベクトルとして保持する。同時に全エキスパート常駐状態で各領域・各MoE層について10,000トークンのゲート確率を記録し、累積確率95%を覆う上位エキスパートを最大8件までH[domain][層]へ保存する。デコード予測器用にはDeepSeek-MoE-16Bのエキスパート 活性値 トレースを収集し、層 index、time since last use、previous エキスパート、domain等からRandom Forestを学習する。

オンラインのプリフィルでは入力promptを埋込み、領域medoidとのcosine類似度を集約して温度0.05のsoftmaxで領域重みを得る。対応する層別短縮リストをanchor エキスパートとしてGPUへ優先ロードし、その集合でプリフィルを実行する。これにより全64 エキスパートを各層で常駐させず、領域に高確率で必要な集合から開始する。

デコードへ移ると、各層で現在の履歴から局所性特徴を抽出しRandom Forestが次トークン/次層で必要なエキスパート確率を出す。上位Kを選び、現在層のMoE計算と並行してCPUからGPUへ非同期転送する。GPU キャッシュはLRUを用いて不要エキスパートを退避する。次のルータ要求時に予測が当たればエキスパートは既にGPUにありI/O待ちが隠れる。この流れを終了トークンまで反復する。

### 領域medoidによる軽量prompt分類
専用分類器を追加学習せず、各領域のprompt埋込みを50クラスタへ分けてmedoidを保存する。新promptは同じ埋込み器でベクトル化し、各領域medoidとのcosine類似度を集約して領域を決める。

温度0.05のsoftmaxは明瞭なpromptではほぼone-hot、混合promptではsoft mixtureを許す。5領域のmacro Top-1領域精度は97.2%、これが95.9%のプリフィルエキスパート hit rateにつながり、分類自体の追加学習費を避ける。

### 領域別エキスパート heatmapと階層読込
各領域・各MoE層で10,000トークンのルーティング確率を全エキスパート常駐状態で記録し、エキスパートごとの平均活性頻度を計算する。頻度順に並べ、累積質量95%を覆う最大8 エキスパートを層別short-listとして三次元表Hへ保存する。

プリフィル開始時は推定領域のshort-listをanchor エキスパートとして先にGPUへ置き、必要に応じて層単位で読み込む。技術領域同士はTop-16 エキスパートの60%以上を共有する一方、Creativeとの重なりは25%未満であり、意味領域がエキスパート集合を絞る根拠になる。

### 局所性認識Random Forest先読み
デコードでは直前エキスパートなどの時間局所性、層 indexによる層間相関、domain idを特徴にRandom Forestが各エキスパートの次回活性確率を推定する。既定K=6で上位集合を選び、現在のGPU計算と並行してCPU→GPU DMAを開始する。

平均Top-6予測精度は単純基準48.8%から83.3%へ上がり、Mathでは52.92%から89.76%、Scienceでも約84.22%となる。予測器は約10マイクロ秒/トークンで、10〜100ms級MoE層計算より十分小さいため先読み判断自体が新たなボトルネックになりにくい。

### GPU エキスパート キャッシュと非同期I/O重畳
GPU キャッシュはPython OrderedDictによるLRU管理で、キャッシュ hit/insert/追い出しをO(1)で扱う。予測されたエキスパートを現在層の計算中に非同期転送し、次のルーティング要求までにGPU常駐させることでPCIe待ちを臨界経路から外す。

各層64 エキスパートのうちピーク約43を同時常駐させる設定ではエキスパート メモリは全常駐の約67%となる。キャッシュ操作と予測を含む層当たり費用は約20マイクロ秒で、単純オンデマンドの最小メモリより多少VRAMを使う代わりに転送待ちを大きく削る設計である。

### 全体のデータ／制御の流れ
Stage 1はprompt embedding→domain identification→Hからshort-list取得→GPU優先ロード→プリフィル forward、Stage 2は各生成step・各層で特徴抽出→エキスパート予測→AsyncPrefetch→現在MoE 層 forwardという一本道で接続する。

DeepSeek-MoE-16Bの27 エキスパート 層×64 エキスパート、top-k=6を対象に、CPU側エキスパート storageと単一A6000のGPU キャッシュを管理する。領域事前知識はプリフィルの初期常駐 setを決め、デコード予測器はその後の動的常駐 setを更新するため、二段階が独立最適化ではなく同じキャッシュ状態を引き継ぐ。
## 評価条件
- **ハードウェア**: 単一NVIDIA RTX A6000。実世界基準検証では20GB GPU メモリ limitを課してheavy オフロードを強制。エキスパート 重みはCPU側からGPUへ転送する。
- **ソフトウェア**: DeepSeek-MoE-16B。GPU キャッシュはPython OrderedDict、Random Forest predictor。実世界の標準オフロード基準にHuggingFace Accelerateを使用し、LRU、LFU、On-Demand、MoE-Infinity-style lookaheadとも比較。コア実装の完全公開コードはソフトウェア登録手続中のため未公開。
Code Alpaca、MathQA、Financial PhraseBank等からCode、Math、Science、Creative、Businessの5領域を構成し、DeepSeek-MoE-16Bのトークン エキスパート 活性値 トレースを収集する。訓練ログは合計830万超で、27 エキスパート 層、各64 エキスパート、ルーティング top-k=6。プリフィルではdomain Top-1 accuracy、エキスパート hit rate、active エキスパート budget Kを変えた下流精度を評価する。デコードではFrequency、temporal、spatial、domain signalの段階的ablationとTop-k予測精度・hit rateを測る。主要I/O結果はA6000特性を反映したevent-driven simulatorで評価し、20GB制約のHF Accelerate実測比較対象を用いてADEPTの投影TPOTと比較する。Full エキスパート Loading、On-Demand オフロード、Locality-Aware キャッシュのメモリ・遅延も比較する。
単一GPUのDeepSeek-MoE-16Bが中心で、領域分布を事前構築できる推論を対象とする。主要3.45倍値のADEPT側TPOTはシミュレーション projectionであり、HF Accelerate基準自体は実測。複数GPU/モデル並列、非定常な未知領域、より大規模な別MoEでの一般化は未検証。
## 主要結果
ADEPTはプリフィル領域分類でmacro Top-1 97.2%、エキスパート hit rate 95.9%を得て、デコードのRandom Forest予測ではTop-6平均83.3%（単純基準48.8%）へ改善する。イベント駆動シミュレーションではI/O waitを50%削減し、20GB A6000上の実測HF Accelerateオンデマンド基準TPOT約3797msに対しADEPTの投影TPOTは1100msで3.45倍。全エキスパート常駐約38GBに対しピーク常駐 エキスパートは各層約43/64で約67%、すなわち33%ピークメモリ削減。予測・キャッシュ管理の層当たり費用は約20マイクロ秒である。

- I/O wait / 50%削減 (比較対象: On-Demand オフロード; 条件: A6000特性のevent-driven シミュレーション) — 次エキスパートを計算と重ねて先読みすることでPCIe待ちを半減。

- TPOT / 3797ms → 1100ms、3.45倍 (比較対象: 20GB A6000のHF Accelerate標準オフロード実測比較対象に対するADEPT シミュレーション projection; 条件: DeepSeek-MoE-16B) — 主要速度値は実測対実測ではなく実測比較対象と投影ADEPTの比較である点に注意。

- ピークエキスパート メモリ / 全常駐比67%、33%削減 (比較対象: 全64 エキスパート 常駐 ≈38GB; 条件: peak ≈43 エキスパート/層) — オンデマンドより多くキャッシュする代わりに全常駐より大幅にVRAMを削減。

- デコードTop-6予測精度 / 48.8% → 83.3% (比較対象: naive frequency/recent 比較対象; 条件: 5 domains、K=6) — 時間・層間・領域信号の統合で先読みhit率を大幅改善。

- プリフィルdomain分類/hit / Top-1 97.2%、hit 95.9% (比較対象: 5-domain macro average; 条件: medoid similarity) — 軽量なprompt領域推定でも初期常駐 エキスパート集合を高精度に絞れる。

- 予測器・キャッシュ オーバーヘッド / 約20µs/層、RF約10µs/トークン (比較対象: MoE 層 compute 10〜100ms; 条件: 実装複雑度評価) — 先読み判断費は層計算より三桁小さい。

### 負の結果・境界条件
- active エキスパート budgetを64から32へ半減すると常駐 parameter poolは50%減るがfull-capacity accuracyの保持は63%にとどまり、K=16では約65 percentage-pointの大幅劣化が起きるため、メモリ削減を無制限に進められない。Creativeは領域分離が強く、分類精度95%、プリフィル hit 94%で技術領域より低い。異なる領域のエキスパート priorを誤って使うと平均でin-domain プリフィル hit rateの74%しか保持できず、domain classification errorは一次の感度要因である。

### 結果の読み方
MoE オフロードではプリフィルとデコードの統計性が違う。プリフィルはprompt全体の意味からエキスパート集合を事前に狭めることがピークメモリへ効き、デコードは直近エキスパート・層間相関・領域の短期局所性から次の転送を計算と重ねることがI/O待ちへ効く。二段を分離することで一つのキャッシュ policyへ両課題を押し込むより良いメモリ/遅延折衷を得る。
## 品質への影響
最終TPOT比較では出力品質は比較対象と同一と報告する一方、プリフィルエキスパート budgetを過度に絞ると下流精度が落ちることも明示される。したがって領域別short-listは性能だけでなくcoverageを95%質量基準で確保し、Kを極端に小さくしないことが必要。
## 既存研究との差
単純On-Demandはルーティング要求後にエキスパートを転送するためメモリ最小化と引き換えにI/O 待ちが大きい。LRU/LFUは過去利用だけで常駐 setを管理するのに対し、ADEPTはprompt domainでプリフィル開始前のエキスパート集合を決め、デコードでは次利用を明示予測して転送を計算へ重ねる。MoE-Infinity-style lookaheadのgating中心先読みと比べても、domain-aware プリフィルとtemporal/spatial localityを組み合わせることで構造化領域のhit-rate利得が大きい。FlexGen等の一般オフロードが層/テンソル配置を扱うのに対し、本手法はMoE エキスパートのルーティング sparsityとdomain specializationを直接利用する。
## 限界
主要評価は単一RTX A6000とDeepSeek-MoE-16Bに集中し、複数GPU、NVMe/SSD階層、異なるMoEアーキテクチャへの一般化は未実証。3.45倍のADEPT TPOTはイベント駆動シミュレーション投影で、比較先HF Accelerateは実機測定なので完全な実測同士ではない。領域priorは既知5領域の事前データを必要とし、誤分類時はプリフィル hit rateが平均26%相対低下する。Kを小さくしすぎるとモデル精度も大幅低下する。Random Forestは非定常ルーティングへの適応をオンライン学習せず、将来課題としてRL/NN predictorを挙げる。
## 実装状態
DeepSeek-MoE-16Bの活性値 トレース収集、domain heatmap、GTE系埋込みmedoid、Random Forest predictor、OrderedDict LRU キャッシュ、event-driven simulatorまで実装・設定が本文に記載される。論文はソフトウェア登録手続中のためcore algorithmsとsimulator configurationsを本文で詳述する代わりにfull public code releaseはまだ行わないと明記している。したがってアルゴリズムは再実装可能な程度に説明されるが、著者公式コードをそのまま再実行する再現性は現時点でない。
## 研究上の位置づけ
本リポジトリの重点であるMoE エキスパート キャッシュ/オフロード系統に直接属する。特徴は階層メモリの置換規則だけでなく、モデルルーティングの意味的・時間的予測をI/O スケジューラへ接続した点にある。CPU→GPU エキスパート transferを次トークン計算と重ねる設計は、将来CPU/DRAMだけでなくSSD/NVMeを下位階層に追加した場合にもプリフェッチ lead timeとキャッシュ admissionの問題へ一般化できる。

一方、現評価はCPU-GPU二階層でありSSD帯域・direct storage・エキスパート圧縮・複数GPU配置は扱わない。今後はdomain priorをエキスパート 配置の長期予測、Random Forestを短期プリフェッチ予測として二時間尺度に分け、NVMe→DRAM→GPUの三階層で各段階のlead timeを変える方向が既存のエキスパート キャッシュ研究との差別化候補になる。
## 一次資料
- https://doi.org/10.1109/ACCESS.2026.3665697
- https://www.researchgate.net/publication/400888358_Two-Stage_Expert_Offloading_for_Domain-Aware_MoE_Inference
