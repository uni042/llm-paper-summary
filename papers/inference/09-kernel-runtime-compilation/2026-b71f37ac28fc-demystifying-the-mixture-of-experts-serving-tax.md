---
canonical_id: SemanticScholar:929a6dad9869799e02c60c0fc959d2fd41de8cb2
title: Demystifying the Mixture of Experts Serving Tax
authors:
- Pratyush Patel
- Dayeol Lee
- Shintaro Iwasaki
- Arvind Krishnamurthy
published: 2026-05
publication: Proceedings of Machine Learning and Systems 8 (MLSys 2026)
publication_type: conference
publication_status: published
source: https://proceedings.mlsys.org/paper_files/paper/2026/file/42a452cbafa9dd64e9ba4aa95cc1ef21-Paper-Conference.pdf
sources:
- https://proceedings.mlsys.org/paper_files/paper/2026/hash/42a452cbafa9dd64e9ba4aa95cc1ef21-Abstract-Conference.html
- https://proceedings.mlsys.org/paper_files/paper/2026/file/42a452cbafa9dd64e9ba4aa95cc1ef21-Paper-Conference.pdf
code: null
implementation: Mixtral-8x7B、Qwen2-MoE、DeepSeek-V3をvLLM、Triton FusedMoE、DeepGEMM、DeepEP等で実行し、A100/B200/H200 GPU上のエンドツーエンド反復レイテンシ、NsightによるGroupGEMM・通信マイクロベンチマーク、解析モデルとMonte Carloを組み合わせたシステム特性評価。新規サービングランタイムの実装・優位性を実証する論文ではなく、公式コード公開URLは一次資料から確認できない。
summary: MoEは1トークン当たりの活性化FLOPsが同じdenseモデルよりサービングが2〜3倍遅くなり得る。著者らは同一活性化計算量のDenseFAと同一総パラメータ量のDensePAを区別し、MoE taxを反復レイテンシ比として定義。prefillでは専門家ごとの小バッチ化・padding・EPのstraggler、decodeでは活性化expert重みの広範なHBMロードが主因であることを、Mixtral/Qwen2-MoE/DeepSeek-V3、A100/B200/H200、vLLMの実測と解析で示す。decodeのtaxは中程度のbatchで最大化し、routing偏りがむしろ有利になる場合がある。解析モデルは大半の条件で実測から10〜30%以内だが、長文脈、multi-node end-to-end、精度比較、JITを対象外とする。
list_summary: "MoEの同一FLOPs 密比2〜3倍の推論負担をプリフィル/デコード・TP/EP・ルーティング分布別に分解。デコードは重み読出し、プリフィルは小バッチ・padding・stragglerが主因。"
last_checked: '2026-10-29'
worker_id: scheduled-chat-00
worker_run_key: 20261029-0100-scheduled-chat-00/r01
worker_completed_at: '2026-10-29T01:00:00+09:00'
reference_main_sha: 64e4dde3d3f3931dcff3f587d1e0cd47e9d7b03e
quality_self_review_passed: true
quality_self_review_version: PAPER-QUALITY-GUIDE-2026-10-07
last_audited: null
audit_version: 0
references:
- canonical_id: arXiv:2107.03374
  arxiv_id: '2107.03374'
- canonical_id: arXiv:2407.00945
- canonical_id: arXiv:2401.09670
- canonical_id: arXiv:2308.12066
- canonical_id: arXiv:2504.02263
- canonical_id: arXiv:2303.06182
- canonical_id: arXiv:2512.09277
- canonical_id: arXiv:2411.08982
- canonical_id: DOI:10.1145/3600006.3613165
- canonical_id: DOI:10.48550/arxiv.2405.04434
- canonical_id: arXiv:1701.06538
- canonical_id: arXiv:2311.18677
- canonical_id: arXiv:2410.12247
- canonical_id: arXiv:2210.17223
- canonical_id: arXiv:2202.08906
- canonical_id: arXiv:2506.05508
- canonical_id: SemanticScholar:929a6dad9869799e02c60c0fc959d2fd41de8cb2
- canonical_id: arXiv:2206.03382
references_checked_at: '2026-10-28'
references_source: primary-pdf-reference-section
references_total: 1
---

# Demystifying the Mixture of Experts Serving Tax — MoE推論の計算・通信・ルーティング由来の費用を分解する

## 概要

本論文は、Mixture-of-Experts（MoE）が「1トークン当たりに実行する演算量を減らせる」という設計上の利点と、実際のGPUサービングで低遅延・高スループットを得られることの間にある差を調べる**システム特性分析研究**である。MoEではrouterが各トークンを複数のFFN専門家へ割り当て、全パラメータの一部しか計算しない。しかし実際には、expertごとに計算が分割され、GPU間でトークンを転送し、必要なexpert重みを読み込み、ばらばらなトークン数を行列積のブロックサイズへ合わせる必要がある。この費用を論文はMoE taxと呼ぶ。

重要なのは、MoE taxが単一の固定倍率ではないことである。入力プロンプトを一括処理するprefillでは、expert単位のバッチが小さくなって演算器を使い切れないこと、GPU間で仕事量が偏ること、paddingによる空計算が問題となる。生成中に1トークンずつ進めるdecodeでは、実際の計算に使うトークン数が少なくても、活性化された多数のexpert重みをGPUのHBMから読み出すため、**演算量ではなく重み転送量**が支配的となる。Mixtral-8x7B、Qwen2-MoE、DeepSeek-V3で、同じ活性化FLOPsのdense相当モデルに対し概ね2〜3倍の遅延税が発生する条件を実測する。

この論文の主たる貢献は新しい高速化アルゴリズムの導入ではなく、比較基準、内訳、推論フェーズごとの逆転条件、解析モデル、運用上の最適化指針を統一的に提示した点にある。例えばexpert負荷を均すことはprefillのEPでは有効でも、decodeでは活性化expertの種類を増やして重み読出しを増やし、かえって遅くする場合がある。従って「expert負荷を均せば常に速い」とは結論できない。

## 問題設定と比較基準

### 同じFLOPsでも同じGPU時間にならない理由

通常のdense FFNでは、同一の重み行列へ多くのトークンをまとめて通す。GPUは一度読み込んだ重みを複数トークンに再利用でき、大きな行列積としてTensor Coreの演算性能を活用できる。対してMoEのGroupGEMM（expertごとの異なる行列積をまとめて実行するカーネル）では、総トークン数が同じでもrouterが複数expertへ分配するため、各expertに割り当てられるトークン数は少ない。演算量だけが同じでも、重みの再利用と行列積の効率は一致しない。

さらにExpert Parallelism（EP）はexpert重みを複数GPUへ配置するので、トークンのdispatch（担当expertのGPUへの送信）とcombine（結果の返送）にAllToAll通信を要する。Tensor Parallelism（TP）は同じ行列をGPU間で分割して部分結果をAllReduceで統合する。どちらも複数GPUを使うが、通信パターンと偏りの影響が異なる。Data Parallelism（DP）でattentionを複製しEPでexpertを分配する構成では、attentionとMoE層の並列化方式が異なるため、単純なFFN時間だけでは全体差を説明できない。

### 二種類のdense比較対象とMoE taxの定義

著者は比較基準を明確に分ける。**DenseFA（FLOP-aligned dense）**は、各MoE層を「1トークンがtop-K個のexpertで行うのと同程度のFLOPsを使う」dense FFNへ置き換えたもの。これはMoE固有のdispatch、padding、重みの分散ロードなどを除いた理想的な比較基準であり、品質が同じことを意味しない。**DensePA（parameter-aligned dense）**は、全expertの総重み量に合わせた巨大なdense FFNであり、計算量も大きい。MoEのdecodeがこのDensePAに近づくなら、疎な計算の利点がメモリ転送面で失われていると解釈できる。

バッチ内のトークン数を`b`、1回のモデルforwardにかかるレイテンシを`T`とすると、MoE taxは `τ_b = T(MoE,b) / T(DenseFA,b)` である。`τ=1`なら同一条件のDenseFAと同等、`τ=2`なら同じFLOPsのdense比較対象より2倍遅い。**推論コストのドル比、モデル品質、理論演算量比、生成トークン/秒の単純な逆数と同一視してはいけない。** 比較は同じ並列度・同じGPU資源で行い、単一GPUで動かせる小さなDenseFAを敢えて少ないGPUへ置き直す比較は対象外である。

## 手法：計測から内訳モデルへ

### 1. 実モデルのforward stepをprefillとdecodeに分けて測る

入力として3種のMoEモデル、複数のバッチサイズ、attention/FFNの並列化構成、MMLU・HumanEval・ランダムトークンから得たルーティング分布を用いる。vLLM上でモデル全体のforward step latencyを測り、同じ並列度のDenseFAとDensePAを実行してtaxを算出する。prefillは多数のプロンプトトークンをまとめて処理する段階であり、decodeは各要求について新しいトークンを繰り返し生成する段階である。両者は演算強度が異なるため、1つの平均値へ混ぜず別々に測る。

さらに各層・各トークンが選んだexpertのIDを記録する。これにより「uniform routingならどれほど速いか」と「実際のテキストでrouterが選んだときにどれほど遅いか」を同じカーネルへ入力して比較できる。end-to-endの差を測るだけでは、計算効率、padding、通信、expertの偏りのどれが原因か分からないので、後段で個別に切り分ける。

### 2. GroupGEMMの算術強度と重み増幅を分離する

総expert数を`E`、トークン当たりの選択expert数を`K`、1反復で実際に活性化したexpert数を`E_active`、トークン数を`m`とする。平均的には各活性化expertへ`mK/E_active`個のトークンが入る。DenseFAは同じ`m`トークンを単一の大きなFFNへ通すため、MoEの算術強度は理想化するとDenseFAの`K/E_active`程度まで下がる。算術強度とは、メモリから1バイト読み込む間に何FLOPsの計算を実行できるかを表す指標である。

prefillではこの小バッチ化がTensor Coreの演算利用率を落とす。decodeでは演算器を使い切る以前にHBM帯域が律速となり、DenseFA比で`E_active/K`倍のexpert重みをロードする。例えば選択expertが少なくても、バッチ全体ではほぼ全expertが一度は使われると、MoEは総パラメータ量が同じDensePAのように重みを読み込む。ここが「活性化FLOPsが少ないのにdecodeが速くない」主要な因果関係である。`E_active`は1トークンのKではなく**バッチ全体で重複を除いたexpert数**なので、バッチ増大とともに飽和し得る。

### 3. padding、straggler、AllToAllの影響を切り分ける

expertに届くトークン数は不規則で、行列積カーネルのブロック幅`B`に合わせるため、空スロットを補うpaddingが必要になる。**blockwise padding**ではexpertごとに`ceil(N_i/B)B`へ切り上げる。expertが多数あり各expertに少数のトークンが散ると、無駄が増える。**max padding**では最大トークン数のexpertに合わせて全expertの次元を揃えるため、一部expertにトークンが集中する分布が悪い。したがって「ルーティングが均一ならpaddingもゼロ」とはならず、均一でもブロック境界と一致しなければ無駄が生じる。

EPでは各GPUに割り当てられたexpertが処理するトークン数が異なる。最も遅いGPUが同期点を決めるので、平均仕事量ではなく**最大仕事量**が全体レイテンシを左右する。これはstraggler taxであり、特に計算主体のprefillで顕著となる。paddingを含む実際の仕事量を均す必要があり、単に生トークン数だけを均等にしても最適とは限らない。decodeでは各GPUがロードするexpert重み数の方が支配的なので、同じルーティング偏りがむしろ活性化expert種類数を減らして有利に働くことがある。

通信についてはTPのAllReduceとDP+EPのAllToAllを区別する。TP同士のMoE/DenseFA比較では、attentionとFFNの後に必要なAllReduceは同じため、**追加の通信taxは定義上ほぼ生じない**。一方DP+EPではトークンを各expertのGPUへ送って戻すため、送受信量はtop-Kのfan-outに応じて増える。AllToAllのAPIレベルの送信量をそのまま物理リンク転送量と見なすと、同一GPU宛のローカル割当てやAllReduceの実装による差を見落とす。論文は8 GPU時のDeepSeek-V3（K=8）で、APIレベルの8倍という差が実ネットワーク転送量の近似では約4.6倍になると整理している。

### 4. ハードウェア費用の解析モデルとballs-bins-buckets

モデルはexpertの重みバイト数`W_e`、1 token-expert当たりのactivation I/O、FLOPs、HBM帯域、GPU演算ピーク、ネットワーク帯域、GPU数を受け取る。expert重みのロード時間を`α = W_e/BW_HBM`、演算時間を`β = F_e/FLOPS_peak`、ネットワーク転送時間を`γ = d_model·s/BW_net`のように分解し、各並列化構成のMoE層の時間を見積もる。さらにpadding後の実効トークン数とGPU別負荷を反映する。通信と計算の重畳はモデル化しないので、実装を完全に模したシミュレータではない。

従来のballs-and-bins（球を箱へランダムに投げる確率モデル）はトークンをexpertへ割り振る偏りを表すが、MoEではexpertがさらにGPUへ格納される。著者はトークン＝balls、expert＝bins、GPU＝bucketsの三層へ拡張し、expert単位とGPU単位の最大負荷を扱う。理想的な均一ランダムルーティングなら活性化expert数の期待値は`E[ E_active ] = E·(1−(1−K/E)^m)`であり、バッチが増えるとEに近づく。実モデルのrouterは均一ランダムではないので、実測ルーティング分布も入力できるようにする。

GPU別負荷はpadding後に非線形に変わるため、Monte Carloで繰り返しルーティングを発生させて評価する。これにより、細粒度expert化がexpert単位の偏りを増やしても、GPU単位では平均化されることや、GPU数を大きくしたDP+EP構成では最も忙しいGPUの比率が悪化し得ることを示す。解析モデルはレイテンシを厳密予測することより、構成ごとにどのtaxが支配的かを説明する目的である。

## 評価条件と比較対象

| 観点 | 原著で確認できる条件 | 解釈上の注意 |
|---|---|---|
| 主モデル | Mixtral-8x7B（総47B、活性13B、8 experts/top-2）、Qwen2-MoE（総57B、活性14B、64 experts/top-8）、DeepSeek-V3（総671B、活性37B、256 experts/top-8） | モデル間でexpert粒度と総パラメータ数が大きく異なる |
| end-to-end GPU | Mixtral/Qwenは1サーバーのNVIDIA A100×8、DeepSeek-V3はNVIDIA B200×8 | 同じGPUで3モデルを横並び比較した数値ではない |
| マイクロベンチマーク | Mixtral/Qwenの計算カーネルとDeepSeek-V3の通信。通信・paddingの一部はH200、8×H200と16×H200（2ノード） | end-to-endのB200とマイクロベンチマークのH200を混同しない |
| 推論ランタイム | vLLM。Mixtral/QwenはTriton FusedMoE/AllReduce、DeepSeekはDeepGEMM/DeepEP | カーネル固有のpaddingや通信挙動が結果に影響 |
| 入力分布 | MMLU、HumanEval、ランダム語彙トークン。end-to-end結果はHumanEvalで提示 | 内容依存のroutingを分離して検討 |
| 主指標 | モデル全体の1 forward step latency（ms）とMoE/DenseFA比のtax、TFLOPS、HBM帯域、AllToAll/AllReduce比、padding、straggler | 実運用の総生成時間・SLO違反率を直接測ったものではない |
| 統計処理 | 上下各1%の外れ値を除いた平均と標準偏差 | 小さな差の過大解釈を避ける |
| 解析モデル | A100-40GB、HBM 1500 GB/s、BF16ピーク312 TFLOPS、固定padding係数prefill 1.25/decode 1.05 | 推定精度の検証は主にMixtral/QwenのTP+TP |

比較対象DenseFAは同一トークン当たり演算量を揃えるようFFN中間次元を変更したdenseモデル、DensePAは総重み数を揃えたdenseモデルである。これはMoEをdenseに変換したときの**性能上の対照実験**であり、生成品質が同じ、同じ訓練予算で作れる、実際の製品料金が同じという意味ではない。DeepInfraの価格図は市場価格の参考であり、GPU測定の2〜3倍と価格差2.5〜10倍を直接同一の結果として扱わない。

## 評価結果

### 全体のtaxとフェーズ差

| 条件・指標 | DenseFAとの比較／対照 | MoE側の結果 | 読み取れること |
|---|---|---|---|
| 複数モデルの主結果 | 同じ活性化FLOPsのDenseFAを1.0とする | 代表的なMoE taxは2〜3倍（abstract・結論） | MoEの理論演算量とGPU遅延は一致しない |
| prefill・Mixtral | 大きなバッチでDenseFAへ近づく | 最小tax約1.28倍、batch 1024 | バッチが大きいと小バッチ化の損失を償却できる |
| prefill・Qwen2-MoE | 同上 | 最小tax約1.28倍、batch 2048 | 細粒度expertでも十分なバッチで改善 |
| prefill・DeepSeek-V3 | 同上 | 最小tax約1.7倍、batch 1024 | 256 experts、巨大モデル、別GPU・別カーネルの影響 |
| decode・Mixtral | DenseFA比のforward step | batch 32でtax 2.08倍、batch 1では最小約1.05倍 | 中程度のバッチで重みロード増幅が大きい |
| decode・Qwen2-MoE | 同上 | batch 32でtax 2.57倍 | expert種類数増加でメモリ律速が強い |
| decode・DeepSeek-V3 | 同上 | batch 128付近で最大約3倍 | 大規模MoEも中バッチでtaxが最大化 |
| TPの付随カーネル | MoE層計算時間に対するrouter/top-K/align/local sumの比率 | Mixtralは概ね5%未満、Qwenは8%未満 | router自体よりGroupGEMM・重みロードが主要律速 |
| TP/FusedMoE・prefill padding | 同じkernelの均一分布を基準 | 実ルーティングで約15〜25%の追加遅延 | ブロック幅に合わないトークン分割が無駄を生む |
| EP/DeepGEMM・prefill straggler | 均一なトークン分布を基準 | 40〜80%の追加kernel latency | GPU間の最大負荷が全体の遅延を決める |
| DeepSeek-V3・AllToAll/AllReduce | H200上のNCCL AllReduceを基準 | 1ノードdecode約2倍、prefill大バッチ3〜4倍、2ノード7〜15倍 | 通信方式とノード境界の差は非常に大きい |
| DeepSeek-V3・decode通信偏り | H200×8、均一分布を基準 | 128 tokens/rankでp95 combine 2.7倍、dispatch 1.9倍 | FP8送信/BF16返送の非対称性が影響 |
| 解析モデルの検証 | A100上のMixtral/Qwen実測tax | 多くのバッチで誤差10〜30%以内 | 主要傾向の説明には有効だが精密予測器ではない |

ここでprefillのbatch 1024/2048は**処理トークン数**であり、1024個の同時ユーザー要求という意味ではない。decodeのbatch 32は、1回の生成反復に参加するトークン数に近い。フェーズごとにバッチの意味と典型的な演算強度が異なるため、同じ横軸で倍率を比較して「このモデルは常に何倍遅い」と結論するのは不適切である。

### なぜdecodeは中程度のバッチで最も遅く見えるか

論文のFigure 3はdecode taxが釣鐘型になることを示す。単一要求では使われるexpertが少なく、重みをロードする量も少ないのでtaxは小さい。バッチを増やすと、一度でも選ばれたexpertの種類数が急増し、計算量に対する重みロードの割合が最大化する。さらにバッチを増やすと、今度はロード済みの重みを複数トークンで使い回せるため、相対的なtaxは低下する。つまり中程度の同時実行が、MoEの「疎な計算だがほぼ全重みを読む」という不利な領域になりやすい。

これは単にGPUを多く使えば解決するという話ではない。より広いEPで1GPU当たりの重み量を減らせても、AllToAll通信と同期点、空転するGPU、障害への脆弱性が増える。逆に小バッチでtaxが1.05倍に近いことも、絶対レイテンシが短いことやGPU利用率が高いことを意味しない。著者は低バッチの小さなtaxが、そもそも両モデルともメモリ律速であるため見かけ上小さい場合を限界として挙げる。

### routing分布・padding・通信の感度

Figure 7では、Mixtralのようにexpert数が少ないモデルは中程度のバッチでも活性化expert率がすぐ100%に近づく。一方、256 expertのDeepSeek-V3では学習済みrouterの選択が均一ランダムと異なり、理論式が活性化数を過大評価することがある。したがって`E_active`はモデルのEとKから機械的に決め打ちできず、実際のrouting traceを採取する価値がある。

Figure 8はTPのFusedMoEで、prefillのpaddingが大きなバッチほど約15〜25%へ増える条件を示す。EPでは、最も重いGPUに割り当てられたトークンが全体を待たせ、40〜80%のkernel遅延増が観測される。もっともdecodeで同じ偏りが起きても、負荷の大きさより読み込むexpert重みの種類が効くため、偏りが負の要因とは限らない。単一の負荷分散指標で両フェーズを最適化する設計には限界がある。

Figure 6の通信測定では、同じ8 GPUでもAllToAllがAllReduceよりdecode約2倍、prefillの大きなバッチでは3〜4倍のレイテンシを要した。2ノード16 GPUでは7〜15倍に広がる。これは**H200での通信マイクロベンチマーク**であり、B200上のDeepSeek-V3全体推論が7〜15倍遅いという意味ではない。Figure 9ではDeepSeek-V3のFP8 dispatchとBF16 combineで転送バイト数が異なるため、combineの偏りによる悪化が大きい。単純な通信呼び出し回数の削減だけでは解決しない。

### 解析モデルの精度と不一致

Figure 11では、A100-40GB、1500GB/s、BF16 312TFLOPSの条件を用い、TP+TPのMixtral/Qwenについてtaxの推定値と実測値を比較する。decodeの中バッチで高くなる釣鐘型と、prefillでバッチ増大に伴ってtaxが下がる傾向を再現するが、ほとんどの条件で誤差は10〜30%であり、厳密な性能保証ではない。一定のpadding係数、カーネル呼び出し固定費の無視、実効FLOPs/HBM帯域の差などが残差の要因である。

一方、paddingモデル単体では、実測したマイクロベンチマークに対して`R² > 0.99`を報告する。この局所的な高い当てはまりを、**MoE tax全体の予測精度が99%以上**という意味に置き換えてはいけない。前者はpadding処理の近似、後者は複数ボトルネックを統合したforward stepの相対遅延であり、測定対象が異なる。

## 既存研究との差と最適化への含意

従来のMoEサービング研究は、個々の税に対して専門化した改善を提案してきた。MegaScale-InferやDP attentionはexpertへ流れる実効バッチを大きくし、GroupGEMMの小バッチ化を緩和する。Lynxのbatch-aware expert selectionは同時に使うexpert数を減らし、decodeの重み増幅を抑える。DeepSeek-V3のExpert Parallel Load Balancer（EPLB）は人気expertを複製してGPU間の負荷を均し、prefillのstragglerを減らす。これらを「どの税を減らし、何を増やすか」で比較できる点が本論文の特徴である。

特にEPLBのexpert複製は、prefillのGPU負荷を均しても、decodeでは活性化expert重みの種類を増やすことでweight amplificationを悪化させ得る。著者は、生のトークン数`R_g`だけでなくpadding後の仕事量`P_g`、実際の活性化expert数を見て負荷分散する案を論じる。ただしこれは**解析からの設計提案**であり、新しいpadding-aware EPLBを実装してend-to-endの改善率を測定したという結果ではない。

最適化の選択には交換条件がある。expert数を減らすroutingはdecodeのHBM転送を減らすが、モデル品質やrouting制約を変える可能性がある。量子化は重みロード量を直接減らせるが、低ビット演算器・dequantization・品質の問題を別途評価する必要がある。EPの並列度を上げると1GPU当たりの重みが減る反面、通信費とGPUの遊休が増える。投機的復号のverificationはdecodeをprefillに近い大きなバッチへ変える一方、通信と計算を重畳するdual-batch方式は1 microbatchのサイズを半分にし、重み増幅を増やし得る。prefill/decode分離型サービングなら、両フェーズで異なる並列化・バッチング・場合によっては異なるモデル構成を選ぶ余地がある。

本論文はこれらの手法を統一ベンチマークで再実装して順位付けした研究ではない。既存の個別最適化を同じtax分解に置き直し、**何を改善しても別の税を増やす可能性がある**ことを明示した分析である。GPU台数やネットワーク構成が違えば結論も変わり得るため、実運用では自分のモデルのrouting trace、prefill/decode構成比、HBM帯域、通信を測ることが重要となる。

## 限界・負の結果・適用範囲

1. **生成品質を比較していない。** DenseFA/DensePAはシステム性能の対照であり、同等の精度やモデル品質を実証していない。routingを偏らせたりexpert数を減らした場合の精度損失もこの研究では定量的に評価していない。
2. **end-to-endは短めの系列と単一ノード。** 長文脈ではattentionの割合が増え、全体に占めるMoE taxが相対的に小さくなる。2ノードの7〜15倍という結果は通信マイクロベンチマークであり、multi-nodeのモデル全体のtaxではない。
3. **定常時のレイテンシが中心。** 動的MoEシステムのJITコンパイル、カーネル再構成、起動直後のスパイク、expert重みの遠隔ロードや運用コストを完全には含めない。専門kernelやrouting/load balancingの保守の難しさというエンジニアリング費用も数値化していない。
4. **解析は重畳と細部を簡略化。** 通信と計算のoverlapをモデル化せず、padding係数や実効性能を単純化している。全体taxの10〜30%誤差を踏まえ、GPU台数・バッチ・routingを選ぶ厳密な最適化器として無検証に使えない。
5. **特定のGPU・kernel世代への依存。** A100/B200/H200、NVLink、Triton FusedMoE、DeepGEMM、DeepEP、NCCLの実測であり、GB200/GB300の広いNVLinkドメインや新kernelでは通信費が異なり得る。異なるデバイスへ倍率をそのまま外挿しない。
6. **MoEの高いFLOPs効率を否定する研究ではない。** 同じ活性化FLOPsでの実行時間を測るものであり、同じ品質を達成するための学習費用やモデル品質、電力当たりの有効性能を総合比較したわけではない。

## サーベイへの位置付け

本論文はMoE inference / expert parallelism / serving systemsの交点にある**定量的なボトルネック分析**として重要である。既存のMoE推論最適化を比較するとき、top-K・総expert数・実効batch・ルーティング偏り・GPU並列度・通信方式を揃えないと「同じFLOPsだから同じ速さ」という比較が成立しないことを明示する。新しいランタイムを直接提案する研究と区別し、prefillの小バッチ/straggler/padding、decodeの重み増幅、EPの通信という3軸の比較基準として利用できる。

## 一次資料・参考

- Patel, Pratyush; Lee, Dayeol; Iwasaki, Shintaro; Krishnamurthy, Arvind. *Demystifying the Mixture of Experts Serving Tax*. Proceedings of Machine Learning and Systems 8 (MLSys 2026), 2026. [出版社掲載ページ](https://proceedings.mlsys.org/paper_files/paper/2026/hash/42a452cbafa9dd64e9ba4aa95cc1ef21-Abstract-Conference.html)、[出版社PDF](https://proceedings.mlsys.org/paper_files/paper/2026/file/42a452cbafa9dd64e9ba4aa95cc1ef21-Paper-Conference.pdf)。本文のFigure 2–12、Table 1–4、§2–7を照合。
- 同論文の関連研究としてMegaScale-Infer、Lynx、DeepSeek-V3、EPLB、DeepGEMM、DeepEP、vLLM等が本文で参照されるが、ここに記した本論文の数値は上記出版社一次PDFに基づく。
