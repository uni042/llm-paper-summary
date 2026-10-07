---
canonical_id: arXiv:2402.16775
title: A Comprehensive Evaluation of Quantization Strategies for Large Language Models
summary: Qwen-Chat 7B・14B・72Bの量子化を知識・能力、整合性、効率の3軸と10課題で評価する。7Bの4ビットGPTQでは平均正答率57.10から54.86、メモリ15.14GBから7.83GBへ変わる一方、8ビットLLM.int8()は生成速度37.67から7.19トークン/秒へ低下し、量子化と高速化が同義でないことを示す。
list_summary: Qwen-Chat 7B/14B/72Bの10課題評価により、4ビット量子化の品質維持と省メモリ効果、2ビットでの外れ値保護の重要性、実装による生成速度低下を示す。
authors:
- Renren Jin
- Jiangcun Du
- Wuwei Huang
- Wei Liu
- Jian Luan
- Bin Wang
- Deyi Xiong
published: '2024-02-26'
publication: 'Findings of the Association for Computational Linguistics: ACL 2024'
publication_type: conference
publication_status: published
source: https://aclanthology.org/2024.findings-acl.726/
sources:
- https://aclanthology.org/2024.findings-acl.726/
- https://aclanthology.org/2024.findings-acl.726.pdf
- https://arxiv.org/abs/2402.16775
- https://arxiv.org/pdf/2402.16775
implementation: Qwen-Chat 7B/14B/72BのGPTQ・LLM.int8()・SpQRを評価。論文脚注記載の公式評価コードは https://github.com/cordercorder/quant_eval 。速度とメモリはA100 80GB SXM上で入力256・出力512トークンを用いた。
code: https://github.com/cordercorder/quant_eval
last_checked: '2026-10-08'
arxiv_id: '2402.16775'
arxiv_categories:
  primary: cs.CL
  cross_list: []
worker_completed_at: '2026-10-07T22:52:00+09:00'
worker_run_key: 20261007-interactive-repair-v3
quality_self_review_passed: true
quality_self_review_version: 2026-10-07-v1
quality_body_chars: 3111
quality_method_chars: 764
quality_evaluation_chars: 1050
quality_limitation_chars: 223
reference_main_sha: 2bdbc19fb4e7b184d066c9e5240fb1d9707db023
last_audited: '2026-10-08'
audit_version: 1
references:
- canonical_id: arXiv:2112.00861
  arxiv_id: '2112.00861'
- canonical_id: DOI:10.48550/arxiv.2309.16609
  doi: 10.48550/arxiv.2309.16609
- canonical_id: DOI:10.48550/arxiv.2204.05862
  doi: 10.48550/arxiv.2204.05862
- canonical_id: DOI:10.48550/arxiv.2302.04023
  doi: 10.48550/arxiv.2302.04023
- canonical_id: DOI:10.18653/v1/d15-1075
  doi: 10.18653/v1/d15-1075
- canonical_id: DOI:10.1145/3641289
  doi: 10.1145/3641289
- canonical_id: arXiv:2110.14168
  arxiv_id: '2110.14168'
- canonical_id: DOI:10.48550/arxiv.2207.04672
  doi: 10.48550/arxiv.2207.04672
- canonical_id: DOI:10.48550/arxiv.2305.14314
  doi: 10.48550/arxiv.2305.14314
- canonical_id: arXiv:2306.03078
  doi: 10.48550/arxiv.2306.03078
- canonical_id: arXiv:2112.06905
- canonical_id: arXiv:2210.17323
  doi: 10.48550/arxiv.2210.17323
- canonical_id: OpenReview:tcbBPnfwxS
  openreview_id: tcbBPnfwxS
- canonical_id: DOI:10.18653/v1/2020.findings-emnlp.301
  doi: 10.18653/v1/2020.findings-emnlp.301
- canonical_id: arXiv:2103.13630
  arxiv_id: '2103.13630'
- canonical_id: DOI:10.1162/tacl_a_00474
  doi: 10.1162/tacl_a_00474
- canonical_id: DOI:10.48550/arxiv.2310.19736
  doi: 10.48550/arxiv.2310.19736
- canonical_id: OpenReview:d7KBjmI3GmQ
  openreview_id: d7KBjmI3GmQ
- canonical_id: DOI:10.48550/arxiv.2310.03262
  doi: 10.48550/arxiv.2310.03262
- canonical_id: DOI:10.48550/arxiv.2306.16244
  doi: 10.48550/arxiv.2306.16244
- canonical_id: OpenReview:fOrm2rGX2r
  openreview_id: fOrm2rGX2r
- canonical_id: DOI:10.1109/cvpr.2018.00286
  doi: 10.1109/cvpr.2018.00286
- canonical_id: DOI:10.48550/arxiv.2310.20410
  doi: 10.48550/arxiv.2310.20410
- canonical_id: DOI:10.48550/arxiv.2305.14152
  doi: 10.48550/arxiv.2305.14152
- canonical_id: DOI:10.18653/v1/2023.findings-acl.29
  doi: 10.18653/v1/2023.findings-acl.29
- canonical_id: arXiv:2306.02272
  doi: 10.48550/arxiv.2306.02272
- canonical_id: DOI:10.48550/arxiv.2306.09212
  doi: 10.48550/arxiv.2306.09212
- canonical_id: DOI:10.48550/arxiv.2309.10677
  doi: 10.48550/arxiv.2309.10677
- canonical_id: DOI:10.48550/arxiv.2211.09110
  doi: 10.48550/arxiv.2211.09110
- canonical_id: arXiv:2306.00978
  doi: 10.48550/arxiv.2306.00978
- canonical_id: DOI:10.18653/v1/2022.acl-long.229
  doi: 10.18653/v1/2022.acl-long.229
- canonical_id: DOI:10.48550/arxiv.2305.10263
  doi: 10.48550/arxiv.2305.10263
- canonical_id: DOI:10.48550/arxiv.2307.08072
  doi: 10.48550/arxiv.2307.08072
- canonical_id: DOI:10.48550/arxiv.2311.18743
  doi: 10.48550/arxiv.2311.18743
- canonical_id: DOI:10.48550/arxiv.2403.07747
  doi: 10.48550/arxiv.2403.07747
- canonical_id: DOI:10.48550/arxiv.2308.05374
  doi: 10.48550/arxiv.2308.05374
- canonical_id: arXiv:2305.17888
  doi: 10.48550/arxiv.2305.17888
- canonical_id: DOI:10.48550/arxiv.2309.01809
  doi: 10.48550/arxiv.2309.01809
- canonical_id: DOI:10.48550/arxiv.2308.12488
  doi: 10.48550/arxiv.2308.12488
- canonical_id: OpenReview:Byj72udxe
  openreview_id: Byj72udxe
- canonical_id: DOI:10.18653/v1/k16-1028
  doi: 10.18653/v1/k16-1028
- canonical_id: DOI:10.18653/v1/d18-1206
  doi: 10.18653/v1/d18-1206
- canonical_id: DOI:10.48550/arxiv.2310.17623
  doi: 10.48550/arxiv.2310.17623
- canonical_id: DOI:10.18653/v1/2022.findings-acl.165
  doi: 10.18653/v1/2022.findings-acl.165
- canonical_id: DOI:10.48550/arxiv.2304.03277
  doi: 10.48550/arxiv.2304.03277
- canonical_id: DOI:10.48550/arxiv.2307.16789
  doi: 10.48550/arxiv.2307.16789
- canonical_id: DOI:10.48550/arxiv.2303.10845
  doi: 10.48550/arxiv.2303.10845
- canonical_id: DOI:10.48550/arxiv.2211.05100
  doi: 10.48550/arxiv.2211.05100
- canonical_id: OpenReview:ITw9edRDlD
  openreview_id: ITw9edRDlD
- canonical_id: DOI:10.18653/v1/p17-1099
  doi: 10.18653/v1/p17-1099
- canonical_id: arXiv:1911.02150
  arxiv_id: '1911.02150'
- canonical_id: DOI:10.48550/arxiv.2312.16132
  doi: 10.48550/arxiv.2312.16132
- canonical_id: DOI:10.1609/aaai.v38i17.29861
  doi: 10.1609/aaai.v38i17.29861
- canonical_id: DOI:10.48550/arxiv.2206.04615
  doi: 10.48550/arxiv.2206.04615
- canonical_id: DOI:10.48550/arxiv.2302.13971
  doi: 10.48550/arxiv.2302.13971
- canonical_id: DOI:10.48550/arxiv.2307.09288
  doi: 10.48550/arxiv.2307.09288
- canonical_id: OpenReview:yzkSU5zdwD
  openreview_id: yzkSU5zdwD
- canonical_id: DOI:10.18653/v1/2020.emnlp-demos.6
  doi: 10.18653/v1/2020.emnlp-demos.6
- canonical_id: DOI:10.18653/v1/2023.acl-long.767
  doi: 10.18653/v1/2023.acl-long.767
- canonical_id: arXiv:2211.10438
- canonical_id: DOI:10.48550/arxiv.2311.04850
  doi: 10.48550/arxiv.2311.04850
- canonical_id: arXiv:2206.01861
- canonical_id: DOI:10.18653/v1/2023.findings-acl.551
  doi: 10.18653/v1/2023.findings-acl.551
- canonical_id: DOI:10.48550/arxiv.2304.12986
  doi: 10.48550/arxiv.2304.12986
- canonical_id: DOI:10.48550/arxiv.2303.18223
  doi: 10.48550/arxiv.2303.18223
- canonical_id: DOI:10.48550/arxiv.2311.07911
  doi: 10.48550/arxiv.2311.07911
- canonical_id: DOI:10.48550/arxiv.2308.07633
  doi: 10.48550/arxiv.2308.07633
- canonical_id: DOI:10.48550/arxiv.2310.01405
  doi: 10.48550/arxiv.2310.01405
references_checked_at: '2026-10-07'
references_source: arxiv-html-reference-section
references_total: 81
under16kb_reaudit_target_path: papers/inference/19-inference-evaluation-benchmarking/2024-2402.16775-a-comprehensive-evaluation-of-quantization-strategies-for-large-language.md
under16kb_reaudit_source_git_blob_sha: '4efd705320e40c3f9fe8fe5e9067c0196277dc84'
under16kb_reaudit_version: '2026-10-07-v1'
under16kb_reaudit_passed: true
quality_body_chars: 5857
quality_method_chars: 1703
quality_evaluation_chars: 2366
quality_limitation_chars: 221
quality_self_review_passed: true
quality_self_review_version: '2026-10-07-v1'
worker_completed_at: '2026-10-07T21:38:06.922Z'
worker_run_key: 'interactive-20261008-bottom-up-reaudit-2402.16775'

---

## 概要

量子化は重みや活性値を少ないビット数で表し、GPUメモリ容量とデータ転送量を減らす代表的なLLM圧縮手法である。しかし、従来の評価はパープレキシティや少数の知識課題へ偏り、指示調整済みモデルの振る舞い、整合性、実際の推論効率まで同じ枠組みで比較されていなかった。本研究はこの不足を埋める評価研究である。

著者らは評価を「知識・能力」「整合性」「効率」の3軸へ整理し、10種類のベンチマークを使って量子化前後を比較する。結果として、4ビット量子化は多くの条件で非量子化モデルに近い下流性能を維持する。また、量子化モデルのパープレキシティは多くのベンチマーク性能と相関し、安価な代理指標として使える可能性を示す。

一方で、メモリ使用量が減ることと生成速度が上がることは同義ではない。低ビット演算を高速に実行するカーネルやハードウェア支援が不十分な場合、逆量子化や型変換の追加処理によって量子化モデルの推論が遅くなる。この負の結果は、量子化方式を「モデルサイズだけ」で選ぶ危険を示す。

## 問題設定

量子化の目的は、元の浮動小数点モデルが持つ能力をできるだけ保ちながら、重みや活性値の保存・転送コストを減らすことである。ビット幅を下げるほど同じGPUメモリへ大きなモデルを載せられるが、丸め誤差や外れ値の影響が増え、出力品質が悪化しやすい。

さらにLLMでは、パープレキシティが低いことと、指示追従、知識質問、推論、生成品質が同じように保たれることは保証されない。事前学習モデルで成立した評価傾向が、指示調整済みモデルにもそのまま当てはまるかを確かめる必要がある。

## 評価枠組み

### 知識・能力

知識・能力軸では、言語モデルとしての予測性能だけでなく、複数の下流課題で量子化による能力低下を測る。これにより「パープレキシティはほぼ同じだが特定能力だけ大きく落ちる」ケースを検出できる。

著者らはモデル規模も比較し、同程度のメモリ予算なら、小さい高精度モデルと大きい低ビットモデルのどちらが有利かを見る。結果は、大規模モデルを量子化して使う方が小規模モデルより高い能力を保つ条件があることを示す。

### 整合性

指示調整済みLLMでは、ユーザー指示への従い方や会話品質が重要である。量子化誤差が次トークン確率へ小さく見えても、長い生成の途中で誤差が累積し、指示追従や応答傾向が変わる可能性がある。そのため本研究は知識問題だけでなく、整合性に関係する評価も独立軸として扱う。

### 効率

効率軸では、モデルサイズとメモリ節約だけでなく実際の推論速度を確認する。理論上、低ビット重みはメモリ帯域を節約できる。しかしGPUが対象ビット幅の行列積を効率よく実行できない場合、低ビット表現を高精度へ戻す処理や専用カーネルの不足が律速になる。

このため、量子化は「ビット数を半分にしたので速度も倍になる」という単純な関係ではない。論文は、メモリ削減を達成していても生成速度が悪化する条件を報告し、ハードウェアとソフトウェア実装を含めて評価する必要性を示す。

## 手法

### 評価方法の再現可能な説明

本論文は新しい量子化器を作る研究ではない。事後量子化の実装を同一モデルで横断比較する研究である。対象となる指示調整済みのQwen-7B-Chat、Qwen-14B-Chat、Qwen-72B-Chatについて、BFloat16版を基準として8・4・3・2ビットの設定を測定する。GPTQは校正データを利用して量子化の重み誤差を補正し、LLM.int8()は大きな値を持つ成分を保護して8ビット演算へ移す。SpQRは外れ値重みを高精度の疎な経路に分離するため、同じ2ビットでもGPTQと保存・演算条件が異なる。

入力となる各モデル・量子化設定をMMLU、C-EVAL、FLORES-200、CNN/DailyMail、XSum、GSM8K、SNLI、FollowBench、TruthfulQA、BBQに適用する。評価指標は正答率、翻訳のBLEU、要約のROUGE、指示追従の満足率、社会的偏りの得点、言語モデルの困惑度などであり、一つの総合得点には統合しない。表2の「平均正答率」は10種類全部の平均ではなく、MMLU、C-EVAL、GSM8K、SNLI、TruthfulQAという五つの正答率の平均なので、翻訳・要約・指示遵守の劣化を見落とさないためには個別指標も必要になる。

実装面では低ビット表現に対応する高速カーネルがあるかが大きな交絡要因となる。SpQRは高精度による模擬量子化の部分を持つため、重みの理論上のビット幅から実測GPUメモリや高速化率を推定できない。定量表から言えることと、将来カーネルが整えば期待できることを分離する。

### 外れ値保護の構成要素除去

SpQRの性能理由を確かめるため、外れ値隔離を維持したまま重みグループ長を16から128へ増やす条件と、グループ長16のまま外れ値隔離を外す条件を比較している。Qwen-14Bの2ビット量子化では、外れ値隔離を外すとWikiTextの困惑度が140.22まで悪化する一方、隔離を残した条件は10未満程度である。グループ長の変更による悪化は比較的小さいため、主に外れ値の保護が極低ビット量子化の品質保持を支えている。この主張は論文表4の比較に対応する。


本研究の「手法」は新しい量子化器ではなく、既存量子化方式を同じ観点で比較する評価設計である。まず非量子化モデルを基準に置き、量子化後モデルについて言語モデルとしての予測誤差、複数の下流能力、指示調整後の振る舞い、実際の資源効率を分離して測る。これにより、ある方式がパープレキシティだけを保っているのか、下流課題まで保っているのか、さらに実行時間まで改善しているのかを切り分ける。

入力は同一系列のLLMと量子化設定で、出力は10ベンチマークにまたがる品質指標と効率指標である。モデル規模とビット幅も交差させるため、「小さい高精度モデル」と「大きい低ビットモデル」を近いメモリ予算で比較できる。量子化誤差だけでなく、元モデル容量が持つ知識・能力の差を含めて配置判断を行える点が重要である。

さらにパープレキシティと各下流指標の関係を比較し、安価に測れる言語モデル指標が高価なベンチマーク群の代理になり得る範囲を調べる。ただし整合性や生成挙動を単一指標へ還元せず、3軸を残す。効率評価では圧縮後のファイルサイズだけでなく推論速度も測り、低ビット表現の理論的な転送量削減と実装上のカーネル効率を区別する。

この設計の出力は単一の総合点ではない。品質を保てても実行が遅い構成、メモリは大きく減るが特定能力が落ちる構成を別々に識別する。したがって利用者は、搭載可能容量、必要な下流能力、対象ハードウェアの低ビット実行性能という配置条件に合わせて量子化方式を選べる。


評価時には、量子化方式ごとの前処理や実行経路の違いも結果へ混ざるため、ビット幅だけを原因とみなさない。特に速度結果は量子化表現を直接演算できるか、途中で高精度へ戻すかで変わる。この観点を効率軸へ残すことで、アルゴリズム上の圧縮率と実装上の高速化を分離する。

## 評価

### 元論文表2と図8に戻った代表値

次の生成速度とメモリは、A100 80GB SXMで入力256トークン、出力512トークンという測定条件である。平均正答率は五つの正答率ベンチマークの平均であり、翻訳や指示追従は別指標で測る。

| モデル・量子化条件 | 平均正答率 | 推論時メモリ | 生成速度 |
|---|---:|---:|---:|
| Qwen-7B-Chat 非量子化（BFloat16） | 57.10 | 15.14 GB | 37.67 トークン/秒 |
| Qwen-7B-Chat GPTQ 4ビット | 54.86 | 7.83 GB | 37.43 トークン/秒 |
| Qwen-7B-Chat LLM.int8() 8ビット | 56.67 | 9.23 GB | 7.19 トークン/秒 |
| Qwen-7B-Chat GPTQ 2ビット | 16.52 | 6.26 GB | 19.36 トークン/秒 |
| Qwen-7B-Chat SpQR 2ビット | 53.18 | 15.66 GB | 37.51 トークン/秒 |
| Qwen-72B-Chat 非量子化（BFloat16） | 71.76 | 138.44 GB | 8.97 トークン/秒 |
| Qwen-72B-Chat GPTQ 4ビット | 71.38 | 44.11 GB | 14.88 トークン/秒 |

7Bの4ビットGPTQではメモリ使用量を約半減させながら生成速度は37.67から37.43トークン/秒とほぼ変わらず、平均正答率は2.24ポイント低下する。一方、同じ7BのLLM.int8()はメモリこそ15.14から9.23GBへ下がるものの、生成速度は37.67から7.19トークン/秒へ大きく低下する。論文は量子化重みと高精度活性を混ぜた演算を十分加速できない当該ハードウェア・実装の制約を理由に挙げている。したがって省メモリをそのまま高速化と同一視できない。

極端な2ビット化では方式差がさらに大きい。7BでGPTQの平均正答率は16.52へ崩壊し、困惑度も84396.73まで悪化する。しかし外れ値重みを保護するSpQRは平均正答率53.18を保つ。ただし、このSpQR構成では推論時のメモリが15.66GBと非量子化の15.14GBを上回り、実装の高精度模擬演算が理論的な圧縮効果を実機で生んだとは言えない。品質維持と実装コストは別の評価軸である。

72BのGPTQ 4ビットはメモリ138.44GBから44.11GB、速度8.97から14.88トークン/秒へ改善する。7Bの場合と違って生成速度にも利得があるため、同じビット幅でもモデル規模やメモリ帯域律速の程度で効果が異なる。特定GPUでの結果をCPU・別世代GPU・別カーネルへ転用する場合は、演算形式と実測条件を再確認する必要がある。


| 観点 | 内容 |
|---|---|
| 評価軸 | 知識・能力、整合性、効率 |
| ベンチマーク | 合計10種類 |
| 比較 | 非量子化モデルと複数の量子化条件 |
| 主な品質指標 | パープレキシティと下流課題性能 |
| 資源指標 | モデル／メモリ規模、推論速度 |
| 重要な負の結果 | 量子化でメモリを減らしても推論が遅くなる場合がある |

この評価の読み方で重要なのは、4ビット量子化の「ほぼ同等」という結論を単一ベンチマークの平均だけで一般化していない点である。著者らは知識・能力、整合性、効率を分け、合計10ベンチマークで非量子化モデルとのずれを見る。その結果、多くの条件では4ビットでも元モデルに近い性能を保つ一方、タスクやモデルによって差が残るため、4ビットなら常に無損失という意味ではない。

モデル規模との交差比較では、大きなモデルを低ビット化した方が、小さいモデルを高精度のまま使うより高い性能を示す条件がある。これは同じメモリ予算で「パラメータ数」と「数値精度」のどちらへ容量を使うかという配置判断に直結する。また、パープレキシティは多くのベンチマークで下流性能の代理になり得るが、論文は整合性を独立軸として残しており、会話品質や指示追従まで単一の言語モデル指標だけで保証できるとはしていない。

効率評価では最も実運用上重要な負の結果が出る。量子化によってメモリ使用量が減っても、対象GPUや実装がそのビット幅を直接高速に処理できなければ、逆量子化や型変換の費用が加わり、生成速度が非量子化モデルより遅くなる場合がある。したがって「4ビットで容量が半減したから速度も比例して上がる」という推論は成立せず、モデル品質、実メモリ、対象ハードウェア上の実測速度を同時に見る必要がある。

代表的な結論は、4ビット量子化が多くの条件で非量子化モデルに近い性能を維持することである。さらにパープレキシティと多くの下流課題性能の関係が観測され、量子化候補を大量に比較する際の一次スクリーニング指標として利用できる可能性がある。

ただしパープレキシティだけで全能力を保証できるという主張ではない。評価枠組みが複数軸を採用していること自体が、単一指標では指示調整済みLLMの品質を十分に表せないという問題意識を反映している。


評価結果を配置判断へ使う場合は、同じメモリ削減率でも方式ごとに品質と速度の位置が異なる点を見る必要がある。4ビットで非量子化に近い品質を保てるという総括は有力だが、個々の課題では差が残る。したがって、まず容量制約を満たす候補を絞り、その後に対象課題の品質と実機速度を確認するという二段階の選択が妥当である。

## なぜ重要か

量子化論文では、圧縮率やパープレキシティ改善だけが強調されやすい。本研究は、実運用で必要な「そのモデルが何をできるか」「指示にどう従うか」「実際に速いか」を同時に見ることで、量子化方式の選択を配置条件へ結び付ける。

特に推論速度の負の結果は重要である。低ビット表現は容量問題を解決しても、対象GPUに高速カーネルがなければ計算経路が非効率になる。したがって、モデル形式、カーネル、アクセラレータ命令、バッチ条件を含む実測なしに、ビット幅だけから速度を推定すべきではない。

## 限界

評価結果は使用したモデル、量子化実装、ハードウェア、ベンチマークに依存する。後発の専用低ビットカーネルや新GPUでは、論文時点で観測された速度低下が解消される可能性がある。

4ビットで品質を保てるという総括も、全モデル・全課題・全量子化方式へ無条件に一般化できない。外れ値分布、モデル規模、指示調整方法によって感度は変わる。また、パープレキシティを代理指標として使える傾向があっても、安全性や長文生成など別の性質まで代表するとは限らない。