---
canonical_id: "title:Efficient LLM Pruning with Global Token-Dependency Awareness and Hardware-Adapted Inference"
title: "Efficient LLM Pruning with Global Token-Dependency Awareness and Hardware-Adapted Inference"
summary: "TVA-Pruneは全先行層への依存を考慮した変分情報ボトルネックのマスクで隠れ次元、FFN、注意ヘッドを構造的に削減し、GQAの共有関係を保ったままGPU Tensor Coreに適した行列寸法へ調整する。A100でLLaMA-2-7Bの困惑度5.11→14.15と品質が低下する一方、推論速度は1.8倍となる。LoRA後は困惑度9.58。"
list_summary: "前層全体の情報を利用する変分マスクでLLMの構造を削減し、GQAの共有ヘッドとGPUの演算ブロックに合わせた調整によって実測速度を改善する。"
authors:
  - "Oshin Dutta"
  - "Ritvik Gupta"
  - "Sumeet Agarwal"
published: "2024-07-01"
publication: "ICML 2024 Workshop on Efficient Systems for Foundation Models II"
publication_type: "workshop"
publication_status: "published"
source: "https://raw.githubusercontent.com/oshindutta/TVAprune/main/Es_fomo__ICML__camera_ready.pdf"
sources:
  - "https://raw.githubusercontent.com/oshindutta/TVAprune/main/Es_fomo__ICML__camera_ready.pdf"
  - "https://github.com/oshindutta/TVAprune"
  - "https://www.researchgate.net/publication/383218239_Efficient_LLM_Pruning_with_Global_Token-Dependency_Awareness_and_Hardware-Adapted_Inference"
code: "https://github.com/oshindutta/TVAprune"
implementation: "C4から5000サンプル、長さ512の校正データでVIBマスクを学習。A100 40GB上でLLaMA、LLaMA-2、Mistral、LLaMA-3の枝刈り、追加LoRA学習、WikiText2と6ゼロショット課題を評価する。"
last_checked: "2026-10-30"
worker_id: "scheduled-chat-00"
scheduled_slot: "00"
worker_run_key: "20261030-1803-scheduled-chat-00/r01"
reference_main_sha: "36e5083fe7d51557a86aa77d397cd66820ac7f33"
quality_self_review_passed: true
quality_self_review_version: "PAPER-QUALITY-GUIDE-2026-10-07"
under16kb_reaudit_target_path: "papers/inference/99-other-inference-systems/2024-614ce03da14c-efficient-llm-pruning-with-global-token-dependency-awareness-and-hardwar.md"
under16kb_reaudit_source_git_blob_sha: "6ecb1314bea0bd1ad51cf06808c0882bfc0b10ff"
under16kb_reaudit_source_sha256: "46c5d1e13cf56e49024efd99078bc69dfbe9c9be4c8303a269fe039692f1049c"
under16kb_reaudit_version: "2026-10-07-v1"
under16kb_reaudit_passed: true
last_audited: "2026-10-30"
audit_version: 1
worker_completed_at: 2026-10-30T19:50:10+09:00
metadata_repair_worker_id: scheduled-chat-45
metadata_repair_run_key: 20261030-1943-scheduled-chat-45/r01
metadata_repair_checked_at: 2026-10-30T19:50:10+09:00
---

# TVA-Prune：トークン依存とGPUの行列形状を考慮した構造的枝刈り

## 概要

TVA-Pruneは、大規模言語モデルの注意ヘッド、フィードフォワード層の中間次元、トークン表現の隠れ次元を構造的に削除する圧縮方式である。通常の重み単位の非構造的枝刈りでは、ゼロ重みを増やしても一般的な密行列演算がそのまま残るため、計算時間が減るとは限らない。構造的枝刈りなら、行列そのものの縦横の大きさを縮められる。しかし削除する次元の選択を誤ると、後段層の表現が崩れ、推論品質が大きく落ちる。

本研究は変分情報ボトルネックのマスクを利用し、各層がその直前だけでなく先行する全層から受け取る情報を考慮して削除候補を選ぶ。さらに、複数のクエリヘッドが一つのキー・値ヘッドを共有するGQAの構造を保ち、枝刈り後の行列寸法をGPUの行列演算器に合わせる。削除率だけでなく、削除後の密なモデルが実際に効率よく動くかを設計に組み込む点が重要である。

A100 40GBでLLaMA-2-7Bを枝刈りした条件では、無圧縮のWikiText2困惑度5.11に対し、TVA-Pruneの困惑度は14.15へ悪化するが、推論速度は1.8倍となる。LoRAによる追加学習後は困惑度9.58まで回復する。行列寸法の調整なしでは同じ品質でも速度改善が約1.1倍にとどまるという結果は、理論的なパラメータ削減とGPU上の実測速度を区別すべきことを示す。

## 問題設定

一般の構造的枝刈りでは、ある層の重要度をその層だけの活性や重みで判断する場合がある。しかしTransformerでは、残差接続を通じて前段から情報が伝わり、同じ隠れ次元が複数の層で異なる役割を担う。ある層で不要に見えた次元が、後続層の予測に不可欠なこともある。TVA-Pruneは、局所統計だけでは全体の情報の流れを適切に扱えない点を問題とする。

もう一つの問題は、注意ヘッドの共有構造である。GQAでは複数のクエリヘッドが同じキー・値ヘッドを参照するため、共有先を削除するなら対応するクエリヘッドも整合するように削除しなければならない。単純に各ヘッドを独立して消すと、残存行列の形状が合わず、注意演算を実行できない。さらに、削除後の行列寸法がGPUのタイル幅に合わないと、演算器の一部が空転し、パラメータ数の減少が速度へ比例しない。

## 手法

### 全層依存を考慮した変分マスク

各層の隠れ表現へ学習可能な確率的マスクを掛け、予測に必要な情報を残しながら不要な次元を抑える。マスクは平均と分散で表され、再パラメータ化した乱数を用いて学習する。目的関数は、元のモデルの予測を維持する損失と、圧縮表現の情報量を抑える正則化を組み合わせる。単に活性値が小さい次元を削除するのではなく、各層が先行する複数の層から受け取る依存を含めて重要度を評価する。

原著§2の定式化では、層ごとのマスクが全先行層の情報を保持する必要性を考慮する。これにより、トークン表現の隠れ次元を削除しても、予測に必要な経路をできるだけ残すことを狙う。元のモデル重みは固定し、主にマスクと疎性制約を最適化するため、重み全体を再訓練する方式より圧縮準備の費用を抑えられる。ただしマスクの学習にはデータとGPU時間が必要であり、完全に学習不要な方式ではない。

### 注意ヘッドとGQAの共有関係

通常の多頭注意では、独立したヘッドを削除すると対応するクエリ・キー・値の射影次元をまとめて縮められる。GQAではキー・値ヘッドが複数のクエリヘッドに共有されるため、一つの共有ヘッドを削除する際には関連するクエリヘッド群も同時に調整する。TVA-Pruneはこの共有関係をマスクの削除操作に組み込み、残った注意構造の実行可能性を維持する。

ヘッド削除に加えて、フィードフォワード層の中間次元と隠れ表現の次元を圧縮する。どの部分を多く削るかによって、同じ総パラメータ削減率でも実際の速度が異なる。注意部分の計算やメモリ移動が律速なら、その部分を減らす方が有利になるが、特定層だけを極端に削ると精度の低下を招く。このため、全体の予測損失と削除率の制約を組み合わせて配分を決める。

### マスク二値化とGPU向け寸法調整

学習中の連続的なマスクは、最終的には残すか削除するかの二値マスクに変換する。これによって行列の行・列やヘッドを実際に取り除き、小さな密行列モデルを構成する。枝刈り後の行列寸法をそのままにせず、GPUのTensor Coreが扱いやすい64、128、256などの倍数へ調整する後処理を行う。原著はタイルの端数による無駄な計算と、GPUの演算ユニット数に合わないタイル配分による利用率低下を説明している。

この後処理はパラメータ削減率を少し変えてでも、実行速度を改善するためのものである。行列が小さくなっただけでは、GPUの演算器を効率よく埋められるとは限らない。対象GPU、行列の縦横、バッチ、カーネルに応じて最適な倍数が変わるため、著者が示した値をすべての環境で固定的に最良と解釈してはならない。

### 圧縮後の追加学習

枝刈りによる予測品質の低下を回復するため、著者はLoRAによる追加学習も評価する。これは削除する構造を選ぶマスク学習とは別の工程であり、追加学習なしの結果と混同してはいけない。圧縮時間の比較では、マスク学習に要する時間と、精度回復の追加学習時間を区別して読む必要がある。LoRA後の高い品質だけを使って、枝刈り単独の精度損失が小さいと主張することはできない。

## 評価環境と主要結果

| 項目 | 原著の条件 |
|---|---|
| GPU | NVIDIA A100 40GB、単一GPUで枝刈りと推論評価 |
| モデル | LLaMA-7B、LLaMA-2-7B、Mistral-7B、LLaMA-3-8B |
| 校正 | C4の5000サンプル、長さ512。学習するのは主に変分マスク |
| 比較方式 | Wanda、LLM-Pruner、FLAP、Bonsai、LoRAPrune等 |
| 評価指標 | WikiText2困惑度、推論速度、トークン毎秒、6課題ゼロショット正答率、圧縮所要時間 |

| LLaMA-2-7B | WikiText2困惑度（低いほど良い） | 推論速度比 |
|---|---:|---:|
| 無圧縮 | 5.11 | 1.00倍 |
| TVA-Prune | 14.15 | 1.80倍 |
| TVA-Prune＋LoRA | 9.58 | 1.80倍 |
| Bonsai | 19.24 | 1.28倍 |

著者公開実装のREADMEと原著Table 1に対応する。TVA-Pruneは無圧縮より困惑度が大幅に悪化しており、速度の利得と品質低下を同時に見る必要がある。LoRAを追加すれば一部の品質を回復できるが、そのための学習費用は別途発生する。行列寸法調整の効果は、調整なし約1.1倍に対して調整後1.8倍という対比から読み取れる。

| GQAモデル | 無圧縮PPL | TVA-Prune PPL | 無圧縮トークン/秒 | TVA-Pruneトークン/秒 |
|---|---:|---:|---:|---:|
| Mistral-7B | 4.77 | 18.37 | 24.78 | 41.39 |
| LLaMA-3-8B | 5.57 | 27.50 | 25.13 | 40.94 |

GQAモデルでも速度は改善するが、困惑度は大きく悪化する。Mistral-7BはLoRA後に困惑度10.12へ回復する一方、LLaMA-3-8Bでは同条件の追加学習結果が表で示されていない。欠けている値を推定して補ってはいけない。GQAの共有ヘッドを壊さずに圧縮できることと、圧縮後の品質が十分であることは別の評価軸である。

### ゼロショット評価と圧縮費用

LLaMA-7Bを約50%圧縮したゼロショット6課題の平均正答率は、無圧縮70.48に対してTVA-Prune＋LoRAが52.44となる。Bonsai＋LoRAは52.33で近いが、枝刈り時間はTVA-Pruneの約2 GPU時間に対してBonsaiは約40 GPU時間と報告される。TVA-Pruneは圧縮準備を短縮する一方、元モデルの正答率からは大きく低下する。原著Table 4ではBoolQ、PIQA、HellaSwag、WinoGrande、ARC-e、ARC-cを個別に示し、特にARC-cではTVA-Prune＋LoRAが26.46と無圧縮47.6を大きく下回る。

圧縮時間が短い方式は実装や条件によって品質が低くなる場合があり、逆に追加学習の時間をかければ性能を回復できる。比較方式ごとに追加学習の有無が異なるため、圧縮時間・推論速度・精度を単一の順位にまとめるのは不適切である。また、Tensor Coreに合わせた寸法調整の利得はA100上の結果であり、他GPU世代や異なるバッチで同じ倍率になる保証はない。

## 限界と実用上の含意

本研究は、モデルの構造を削減して密な行列として実行する方式であり、疎な重みを扱う専用カーネルを必要としない点に利点がある。ただし、枝刈り率を上げるほど言語モデルの品質が低下しやすく、長文脈検索や複雑な推論での影響を十分に評価していない。実測は特定のGPUとモデル規模に依存し、削除後の行列寸法の最適値も装置ごとに変わり得る。

さらに、マスク学習にC4データを使い、品質回復にはLoRA学習を行うため、完全にデータ不要な圧縮ではない。GQAの共有構造を保つ削除方法は技術的に重要だが、共有ヘッドを大幅に減らしたときの長文脈性能は別途確認する必要がある。評価で用いられたLLaMAやMistralの条件を、より大きなMoEモデルや別の注意構造へそのまま適用できるとは限らない。

既存方式との差は、全層にわたる情報依存を使うマスク、GQAの共有関係を守るヘッド削除、GPUの演算タイルに合わせる寸法調整を一連の処理にしたことである。実際の運用では、同じ圧縮率だけで方式を比較せず、同じ品質条件を満たすモデル同士で、生成速度、GPUメモリ、校正費用を測ることが必要である。品質の大きな低下を許容できない用途では、速度改善が大きくても採用を見送る合理的な理由になる。

## 一次資料と再監査

- [著者公開論文と実装](https://github.com/oshindutta/TVAprune) の原稿、表1〜5、図2〜3、実装READMEの再掲数値を照合した。
- [著者アップロードの全文](https://www.researchgate.net/publication/383218239_Efficient_LLM_Pruning_with_Global_Token-Dependency_Awareness_and_Hardware-Adapted_Inference) の手法・評価・追加資料を確認した。
- 固定HEADの既存paper Git blob `6ecb1314bea0bd1ad51cf06808c0882bfc0b10ff` を対象にした再監査修復稿である。元原稿は直接変更せず、GitHub側のsource SHA検査と取り込み判定へ委ねる。
