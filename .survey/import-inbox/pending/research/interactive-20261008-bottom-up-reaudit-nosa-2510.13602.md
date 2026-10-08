---
under16kb_reaudit_target_path: papers/inference/13-sparse-attention/2025-2510.13602-nosa-native-and-offloadable-sparse-attention.md
under16kb_reaudit_source_git_blob_sha: a2c962ff25c986bed4a6a0309b2276fb27041ba9
under16kb_reaudit_version: "2026-10-07-v1"
under16kb_reaudit_passed: true
quality_eval_chars: 1419
worker_id: interactive-chat
worker_completed_at: "2026-10-08T15:00:31.083Z"
last_audited: "2026-10-08"
audit_version: 1
canonical_id: arXiv:2510.13602
title: 'NOSA: Native and Offloadable Sparse Attention'
summary: 学習可能な疎注意は品質を保ちやすい一方、選択されるKVブロックが毎ステップ変化するとCPUからGPUへの転送が律速になる。NOSAは問い合わせ依存選択と非依存選択を分離して最低局所性を保証し、NOSIはブロック配置・カーネル融合・PCIe転送を最適化する。1B/3B/8Bモデルで長文品質を維持しつつ復号スループットを全注意比最大5.04倍に改善する。
list_summary: 学習時からKV選択の局所性を保証する疎注意NOSAとCPU退避推論基盤NOSIにより、長文品質を保ちつつGPU容量とPCIe転送の制約を緩和する。
authors:
- Yuxiang Huang
- Pengjie Wang
- Jicheng Han
- Weilin Zhao
- Zhou Su
- Ao Sun
- Hongya Lyu
- Hengyu Zhao
- Yudong Wang
- Chaojun Xiao
- Xu Han
- Zhiyuan Liu
published: '2025-10-15'
publication: EMNLP 2026 main conference
publication_type: conference
publication_status: accepted
source: https://arxiv.org/abs/2510.13602
sources:
- https://arxiv.org/abs/2510.13602
- https://arxiv.org/html/2510.13602v3
implementation: NOSAモデルとCPU-GPU間KV退避推論基盤NOSIを実装。Tritonの融合・UVA転送カーネル、FlashInfer、CUDA Graphs、専用CUDA集合差分カーネルを使用。著者らがthunlp/NOSAで公式コードを公開。
code: https://github.com/thunlp/NOSA
last_checked: '2026-10-08'
arxiv_id: '2510.13602'
arxiv_categories:
  primary: cs.CL
  cross_list:
  - cs.AI
  - cs.LG
worker_run_key: 20261008-0428-scheduled-chat-30/r01
reference_main_sha: 55fc170f98736092545d48085ae4b4f60a3bb2bc
quality_self_review_passed: true
quality_self_review_version: 2026-10-07-v1
quality_body_chars: 5021
quality_method_chars: 1665
quality_evaluation_chars: 1419
quality_limitation_chars: 372
references:
- canonical_id: arXiv:2108.07732
  arxiv_id: '2108.07732'
- canonical_id: arXiv:2506.17121
  arxiv_id: '2506.17121'
- canonical_id: arXiv:2508.11661
  arxiv_id: '2508.11661'
- canonical_id: arXiv:2107.03374
  arxiv_id: '2107.03374'
- canonical_id: arXiv:2512.10576
  arxiv_id: '2512.10576'
- canonical_id: arXiv:2410.16179
- canonical_id: arXiv:2601.02872
  arxiv_id: '2601.02872'
- canonical_id: arXiv:2110.14168
  arxiv_id: '2110.14168'
- canonical_id: DOI:10.5281/zenodo.12608602
  doi: 10.5281/zenodo.12608602
- canonical_id: arXiv:2410.13276
- canonical_id: arXiv:2310.01801
- canonical_id: arXiv:2407.21783
  arxiv_id: '2407.21783'
- canonical_id: arXiv:2308.16137
- canonical_id: arXiv:2501.15113
  arxiv_id: '2501.15113'
- canonical_id: arXiv:2401.18079
- canonical_id: arXiv:2411.09688
- canonical_id: arXiv:2410.21276
  arxiv_id: '2410.21276'
- canonical_id: arXiv:2407.02490
- canonical_id: arXiv:2510.25600
  arxiv_id: '2510.25600'
- canonical_id: arXiv:2410.01518
- canonical_id: DOI:10.1145/3600006.3613165
- canonical_id: arXiv:2504.16083
- canonical_id: arXiv:2404.14469
- canonical_id: DOI:10.48550/arxiv.2405.04434
  arxiv_id: '2405.04434'
- canonical_id: arXiv:2405.14366
- canonical_id: arXiv:2412.03213
- canonical_id: arXiv:2305.17118
- canonical_id: arXiv:2402.02750
- canonical_id: arXiv:2502.13189
- canonical_id: arXiv:2503.21460
  arxiv_id: '2503.21460'
- canonical_id: arXiv:2506.07900
  arxiv_id: '2506.07900'
- canonical_id: arXiv:2408.05646
- canonical_id: arXiv:2303.06865
- canonical_id: arXiv:2508.02124
  arxiv_id: '2508.02124'
- canonical_id: arXiv:1909.08053
  arxiv_id: '1909.08053'
- canonical_id: arXiv:2406.02542
- canonical_id: arXiv:2312.12456
- canonical_id: arXiv:2410.21465
- canonical_id: arXiv:2406.10774
- canonical_id: arXiv:2506.16640
  arxiv_id: '2506.16640'
- canonical_id: arXiv:2510.11292
  arxiv_id: '2510.11292'
- canonical_id: arXiv:2402.04617
- canonical_id: arXiv:2410.10819
- canonical_id: arXiv:2309.17453
- canonical_id: arXiv:2503.16428
- canonical_id: arXiv:2502.14866
- canonical_id: arXiv:2408.07092
  arxiv_id: '2408.07092'
- canonical_id: arXiv:2501.01005
- canonical_id: arXiv:2505.07661
  arxiv_id: '2505.07661'
- canonical_id: arXiv:2502.11089
- canonical_id: arXiv:2402.16363
  arxiv_id: '2402.16363'
- canonical_id: arXiv:2505.21136
  arxiv_id: '2505.21136'
- canonical_id: arXiv:2305.12474
  arxiv_id: '2305.12474'
- canonical_id: arXiv:2306.14048
- canonical_id: arXiv:2509.24663
  arxiv_id: '2509.24663'
- canonical_id: arXiv:2312.07104
- canonical_id: arXiv:2509.24626
  arxiv_id: '2509.24626'
references_checked_at: '2026-10-08'
references_source: arxiv-html-reference-section
references_total: 99
---

## 概要

NOSAは、学習可能な疎注意（trainable sparse attention）とCPUへのKVキャッシュ退避を両立させるために、注意先の選択パターンを学習段階から転送局所性の高いものへ制約する手法である。長い文脈を持つ言語モデルでは、各要求のキー・値（KV）キャッシュがGPUメモリを占有し、バッチを増やせなくなる。不要なKVをCPUへ退避し、必要な一部だけGPUへ戻せばメモリ容量は節約できるが、必要なブロックが毎トークン変わるとPCIe転送が律速になり、バッチ拡大の利得が失われる。

従来の学習不要の疎注意・退避方式は、学習時に見ていない選択パターンを推論で使うため、長い出力を生成すると誤差が蓄積しやすい。逆に学習可能な疎注意は生成品質を保ちやすいが、GPUに必要なKVブロックを毎回自由に選ぶとCPU転送が大きくなり、実用的な退避が難しい。NOSAは問い合わせ依存の選択と問い合わせ非依存の選択を組み合わせ、前後ステップで再利用されるKVの割合に下限を与える。専用推論基盤NOSIはこの局所性を生かして転送、索引、カーネル起動を削減する。

1B、3B、8Bの言語モデルで一般課題、長入力、長出力の能力を測り、復号スループットは全注意比最大5.04倍、InfLLMv2比最大1.92倍、ShadowKV比最大1.83倍と報告する。論文の最新版は2026年9月28日のv3で、EMNLP 2026本会議採択と明記されている。

## 問題設定と観察

通常の全注意では入力長に比例してKVキャッシュが増える。復号段階では毎トークン、現在の問い合わせと過去KVを照合するため、長い文脈ほどGPUメモリ容量と帯域が問題になる。InfLLMv2のような学習可能な疎注意は重要ブロックだけを選ぶが、選択され得るKVは全履歴に広がるため、CPUへ退避した場合の転送量を明示的に抑えられない。

著者らは連続する復号ステップで選択されるKV集合の重複率を局所性γ(t)と定義する。前ステップで選んだ集合と現在選ぶ集合の共通要素数を、現在選ぶ集合の大きさで割った値である。16Kトークンから4Kトークンを選ぶInfLLMv2の測定では、多くの層でγ(t)が0.8以上となり、少なくとも80%は再利用できる。しかし残り20%を毎ステップPCIeで転送すると、注意処理が復号時間の80%以上を占める条件があり、まだ通信律速である。局所性が自然に高いだけでは不十分で、最低限の再利用率を設計上保証する必要がある。

## 手法

### 問い合わせ依存・非依存選択の分離

NOSAは選択するKVの予算kを、現在の問い合わせベクトルで重要度を決めるk_qと、過去のKVの内容だけで重要度を決めるk_eに分ける。問い合わせ依存側はqと過去のkの内積に基づいて上位候補を選び、古い重要情報を再発見する能力を残す。問い合わせ非依存側は、値ベクトルから小さな学習可能な退避ヘッドが重要度を算出し、上位候補を保持する。

問い合わせ非依存側では一度捨てた古い要素が後から突然復活しないという性質がある。新しいトークンの追加を除けば、選択集合が安定するため、前ステップでGPUに載せたブロックを再利用できる。両者を組み合わせると局所性にγ(t)≧k_e/kという下限を与えられる。論文の主要設定はk=4096、k_q=1024、k_e=3072で、最低局所性0.75を保証する。問い合わせ依存側の比率を増やすと検索品質は上がり得るが、転送量も増えるという明確な交換条件がある。

### ブロック単位の選択と学習

トークン単位の細かい選択では、CPUからGPUへの転送が小さい不連続領域に分かれ、PCIeの帯域を使い切れない。NOSAはInfLLMv2のブロック疎注意を基盤とし、サブブロックで平均プーリングした重要度をブロック内で最大プーリングして選択スコアを作る。先に問い合わせ依存側の上位ブロックを選び、その位置を確保したうえで問い合わせ非依存側の上位ブロックを埋める。これにより総選択数kを保ち、ブロック転送と局所性保証を両立する。

退避ヘッドは値ベクトルvを学習可能な二層の小さな変換へ通し、重要度を出す。注意の重みにもこのスコアをバイアスとして加えるため、単なる推論時の後付け選択ではなく、学習中から退避選択に合わせてモデルを適応させられる。重要度の指数関数を選択前に計算すると数値精度の問題が起こるため、指数計算を注意の最終重み計算へ遅らせるED-DMA方式を採用する。1BモデルのRULER-16Kでは、この退避ヘッド実装が61.9%で、比較するInfLLMv2の60.3%、通常DMAの56.2%より高い。

学習は短い文脈で通常の全注意を用いて事前学習し、長文への継続事前学習からNOSAへ切り替え、指示調整でもNOSAを使う。評価した1B/3B/8Bモデルはいずれも4Kの元の文脈長から16Kへ拡張しており、同じ学習経路を持つInfLLMv2やDMAと比較する。推論時だけ疎性を導入する方式と異なり、訓練と推論で注意パターンを一致させることが長出力の品質維持につながる。

### NOSI：退避を実際に速くする推論基盤

素朴なHugging Face Transformers上の実装では、退避ヘッドや索引生成の小カーネルが多く、起動費用が支配的になる。NOSIは退避ヘッドとQKV分割を一つのTritonカーネルへ融合し、問い合わせ依存・非依存のプーリングもまとめる。LayerNorm、RoPE、FFNにはFlashInferの実装を使い、索引生成などの起動列をCUDA Graphsでまとめる。

GPUとCPUにはKVをブロック単位で配置し、前ステップの選択集合と新しい集合の差分だけを交換する。GPU側のブロックは連続して並ぶ必要がないため、不要になった位置へ新しいブロックを上書きする。集合差分と置換先の対応付けを専用CUDAカーネルで処理し、Python側の逐次索引操作を避ける。

選択ブロックは実験設定で約16KiBと小さく、普通のホストから装置へのコピーを多数呼ぶと帯域効率が悪い。NOSIは統合仮想アドレス（UVA）でCPUメモリを直接参照するTriton転送カーネルを実装する。PCIe 4.0上の8Bモデルで、バッチ16/32/64の転送帯域はそれぞれ17.04/20.36/22.35GB/sと報告する。NOSAの選択局所性だけではなく、この実行基盤の最適化が高い復号スループットを得るために不可欠である。

## 評価条件と結果

| 評価軸 | 条件・比較 | 結果 | 解釈 |
|---|---|---|---|
| 長文理解 | 1B/3B/8B、LongBenchとHELMET、InfLLMv2・ShadowKV・DMA等 | 表2の12設定中9設定でNOSAが最高 | 学習可能な疎性と退避適性を両立 |
| 長出力推論 | 8B、Math-500・Gaokao等の推論課題 | 平均正解率：全注意51.6%、NOSA49.6%、ShadowKV12.5% | 学習不要の退避方式で生じる長生成劣化を抑制 |
| 一般課題 | 1B/3B/8B、複数の短文課題 | 8Bの平均は全注意52.9%、NOSA53.6% | 短文一般能力は概ね維持 |
| 退避による復号 | 8B、96K入力、等価バッチ64、全注意と比較 | 最大5.04倍の復号スループット | GPUに保持するKV量を揃えると実バッチを増やせる |
| 学習可能な疎注意との比較 | NOSA+NOSIとInfLLMv2+NOSI、CPU退避あり | 最大1.92倍の復号スループット | 最低局所性がPCIe転送を減らす |
| 学習不要の退避方式との比較 | NOSA+NOSIとShadowKV | 最大1.83倍の復号スループット | 選択局所性と実装効率の両方が寄与 |
| PCIe転送 | 8B、PCIe 4.0、バッチ16/32/64 | 17.04/20.36/22.35GB/s | 細粒度ブロックをまとめて高帯域で取得 |
| 最新GPU条件 | H100、PCIe 5.0、入力16K、等価バッチ16 | NOSA+NOSI 2551.66 tok/s、InfLLMv2+NOSI 1762.16 tok/s | PCIeが速くなっても局所性制約の利得が残る |

長文評価では、全注意が常に全項目で負けるわけではない。1BのHELMETで全文注意の平均28.3%に対しNOSAの全文プリフィル・疎復号は24.0%という条件もある。8Bの長文では比較対象に対する改善がより安定しており、モデル容量や学習量によって疎注意の品質維持が変わる。著者らは学習長16Kを超える32K・64Kの外挿も試し、64Kでは回転位置埋め込みの尺度パラメータと選択予算を変更しているため、無調整で4倍長へ一般化したという意味ではない。

復号スループットの「等価バッチ」は、GPU上に保持するKVキャッシュ量を同じにした比較指標である。退避方式ではCPU側に残りを保持できるため、同じGPU容量で実際のバッチを大きくできる。96K・等価バッチ64での全注意比5.04倍は、この実バッチの違いを含むシステム結果であり、単一要求の1トークン遅延が5倍短くなるという意味ではない。元のHugging Face実装のNOSAはInfLLMv2より遅い条件があるため、NOSIのカーネル最適化を切り離して手法の性能を評価することはできない。

選択予算を変える実験では、問い合わせ依存比率k_q/kを小さくすると最低局所性が上がりスループットが増す一方、長距離情報の検索が弱くなる。k=2048から6144へ増やすと長文評価は改善し、特に再ランキングや再現課題は予算に敏感である。単にKVを最小化すれば良いのではなく、保持予算と問い合わせ依存選択の割合を用途に合わせて調整する必要がある。

## 既存研究との差

InfLLMv2は学習可能な疎注意で長文品質を保ちやすいが、選択ブロックの転送量を直接制約しない。ShadowKVなどの学習不要のCPU退避はGPUメモリを節約できるが、学習と推論の疎性パターンが異なり長い生成で品質が落ちる。DMAのような問い合わせ非依存の退避は選択集合が安定する一方、一度捨てた過去情報を再発見しにくい。NOSAは問い合わせ依存と非依存を混ぜて局所性の下限を保証し、学習時から同じ注意構造を使う。NOSIはその構造に合わせた転送・索引・カーネルを提供するため、アルゴリズムと推論システムの共同設計となっている。

## 限界と適用範囲

NOSAを使うには長文継続事前学習と指示調整で注意構造を組み込む必要があり、任意の既存モデルへ推論時に追加するだけでは同じ品質は保証されない。問い合わせ非依存比率を増やすほど転送は減るが、遠距離の情報を取り戻す能力が低下し得る。局所性の保証は選択ブロックの重複率に関するものであり、すべてのGPUカーネルやホストメモリ帯域の上限をなくすものではない。

実験は1B/3B/8Bモデルと対象ハードウェアに依存し、巨大な混合専門家モデルや異なるGPU接続方式へそのまま性能倍率を一般化できない。学習長16Kを超える外挿では位置埋め込み設定や選択予算を変更している。小型モデルや厳しい選択予算では全注意より長文品質が下がる条件があり、退避による大バッチ化が不要な短文・低同時実行負荷では、システム追加費用に見合う利得が小さくなる可能性がある。

## 一次資料

- Yuxiang Huang et al., *NOSA: Native and Offloadable Sparse Attention*, EMNLP 2026 main, arXiv v3 (2026-09-28), https://arxiv.org/html/2510.13602v3
- 公式実装: https://github.com/thunlp/NOSA

## 再監査記録

- 監査対象: GitHub `main` の上記同一論文、原本Git blob SHA `a2c962ff25c986bed4a6a0309b2276fb27041ba9`。
- 一次資料: 著者論文第3版（2026年9月28日、https://arxiv.org/html/2510.13602v3）の手法第3節・推論基盤第4節・評価第5節・付録Eを照合。
- 内容確認: 問い合わせ依存／非依存の選択と局所性下限 γ(t) ≥ k_e/k、ED-DMAとNOSIの機構、RULER-16K 61.9%、転送帯域17.04/20.36/22.35 GB/s、8Bの復号処理量の倍率、H100・PCIe 5.0の結果と品質低下条件が一次資料と整合。
- 判定: 本文は論文固有の手法、評価条件、主要数値、適用限界を具体的に記述しているため大幅な書換えは不要。既存解説を保存し再監査証跡だけ追加。
