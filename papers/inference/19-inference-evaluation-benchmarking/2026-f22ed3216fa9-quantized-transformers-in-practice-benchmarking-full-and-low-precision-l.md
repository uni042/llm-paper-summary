---
canonical_id: DOI:10.32604/cmc.2026.078985
doi: 10.32604/cmc.2026.078985
title: 'Quantized Transformers in Practice: Benchmarking Full- and Low-Precision LLMs across Two Processors'
summary: RTX4070/4080 Laptop GPUでGPT-2、LLaMA-2-7B-Chat、Qwen1.5-1.8B-ChatのFP16とINT8学習後量子化を比較した実証研究。表3では4070のLLaMA-2 FP16がCPUオフロードで1244.29秒、INT8が18.63秒となる一方、4080のGPT-2はINT8で1.10秒から2.01秒へ悪化する。50プロンプトの語彙一致指標と人手参照文、GPT-4o/Geminiによる定性評価を区別し、速度と文章品質の交換条件を検討する。
list_summary: ノートPC向けRTX4070/4080で3系列のFP16/INT8生成速度と品質を比較し、CPUオフロードによる巨大な見かけの高速化とINT8逆転例を分離する。
authors:
- Simona-Vasilica Oprea
- Adela Bâra
published: '2026-04-09'
publication: Computers, Materials & Continua 87(3), article 91 (2026)
publication_type: peer-reviewed journal article
publication_status: published
source: https://www.techscience.com/cmc/v87n3/66994/html
sources:
- https://www.techscience.com/cmc/v87n3/66994/html
- https://cdn.techscience.cn/files/cmc/2026/TSP_CMC-87-3/TSP_CMC_78985/TSP_CMC_78985.pdf
- https://doi.org/10.32604/cmc.2026.078985
implementation: Hugging Face Transformers 4.38.2、PyTorch 2.1.2、BitsAndBytes 0.42.0、CUDA 12.1でFP16ロードとload_in_8bit=Trueを比較。device_map=auto、greedy、batch 1、最大256新規トークン。コード公開URLは未確認。
code: null
last_checked: '2026-10-30'
worker_id: scheduled-chat-45
worker_completed_at: '2026-10-30T00:50:08+09:00'
worker_run_key: 20261030-0045-scheduled-chat-45/r01
reference_main_sha: 6154f06fa0cb837ccdc94a428400254f097d2e47
quality_self_review_passed: true
quality_self_review_version: PAPER-QUALITY-GUIDE-2026-10-07
returned_research_repair: true
returned_research_reason: 'blocked_quality: method/evaluation sections were not recognized because headings did not match; independent rewrite and primary-PDF recheck'
returned_research_blocked_git_blob_sha: aae9e62a1470dfab0d9f15548d1fa932a87a39a2
last_audited: null
audit_version: 0
references:
- canonical_id: DOI:10.18653/v1/2021.acl-long.334
  doi: 10.18653/v1/2021.acl-long.334
- canonical_id: arXiv:2208.07339
- canonical_id: arXiv:2310.16836
- canonical_id: DOI:10.18653/v1/2023
  doi: 10.18653/v1/2023
- canonical_id: DOI:10.3390/ai4040047
  doi: 10.3390/ai4040047
- canonical_id: DOI:10.53469/jtpes.2024.04(02).08
  doi: 10.53469/jtpes.2024.04(02).08
- canonical_id: DOI:10.1145/3486618
  doi: 10.1145/3486618
- canonical_id: DOI:10.13374/j.issn2095-9389.2022.12.27.004
  doi: 10.13374/j.issn2095-9389.2022.12.27.004
- canonical_id: DOI:10.1145/3487045
  doi: 10.1145/3487045
- canonical_id: DOI:10.18653/v1/2023.emnlp-main.102
  doi: 10.18653/v1/2023.emnlp-main.102
- canonical_id: arXiv:2211.10438
- canonical_id: DOI:10.18653/v1/2023.emnlp-main.910
  doi: 10.18653/v1/2023.emnlp-main.910
- canonical_id: DOI:10.1109/tcsi.2024.3350661
  doi: 10.1109/tcsi.2024.3350661
- canonical_id: DOI:10.18653/v1/2022.findings-emnlp.240
  doi: 10.18653/v1/2022.findings-emnlp.240
- canonical_id: DOI:10.21437/interspeech.2022-413
  doi: 10.21437/interspeech.2022-413
- canonical_id: DOI:10.18653/v1/2022
  doi: 10.18653/v1/2022
- canonical_id: DOI:10.1371/journal.pone.0265621
  doi: 10.1371/journal.pone.0265621
- canonical_id: DOI:10.1007/s00530-023-01065-2
  doi: 10.1007/s00530-023-01065-2
- canonical_id: arXiv:2206.01861
- canonical_id: DOI:10.1016/j.neunet.2023.12.001
  doi: 10.1016/j.neunet.2023.12.001
- canonical_id: arXiv:2212.09720
- canonical_id: DOI:10.18653/v1/2023.emnlp-main.161
  doi: 10.18653/v1/2023.emnlp-main.161
- canonical_id: DOI:10.18653/v1/2023.findings-acl.511
  doi: 10.18653/v1/2023.findings-acl.511
- canonical_id: DOI:10.24818/18423264/59.3.25.06
  doi: 10.24818/18423264/59.3.25.06
- canonical_id: DOI:10.1016/j.neucom.2020.12.035
  doi: 10.1016/j.neucom.2020.12.035
- canonical_id: DOI:10.18653/v1/2023.emnlp-main.565
  doi: 10.18653/v1/2023.emnlp-main.565
- canonical_id: DOI:10.1109/lca.2024
  doi: 10.1109/lca.2024
- canonical_id: arXiv:2101.01321
- canonical_id: DOI:10.18653/v1/2023.sustainlp-1.3
  doi: 10.18653/v1/2023.sustainlp-1.3
- canonical_id: DOI:10.18653/v1/2023.emnlp-main.617
  doi: 10.18653/v1/2023.emnlp-main.617
- canonical_id: DOI:10.1109/cvpr52729.2023.02170
  doi: 10.1109/cvpr52729.2023.02170
- canonical_id: DOI:10.1145/3579371.3589038
references_checked_at: '2026-10-29'
references_source: primary-pdf-reference-section
references_total: 33
---

# ノートPC向けRTX 4070/4080でのFP16・INT8推論比較：速度と品質の分母をそろえる

## 概要

この論文は新しい量子化器や専用カーネルの提案ではない。著者の関心は、既存の8ビット学習後量子化を実務環境へ適用したとき、モデルの収容可否、生成時間、文章の語彙・構造がどう変わるかを測定することにある。対象はGPT-2、LLaMA-2-7B-Chat、Qwen1.5-1.8B-Chatの3系列、GPUはRTX 4070 LaptopとRTX 4080 Laptopの2機種である。比較精度はFP16とINT8で、主な測定対象は単一要求の生成時間、トークン毎秒、50件の文章生成に対する語彙一致、少数の人手参照文および自動評価者による品質評価となる。

著者はCPUオフロードの影響を受けた構成を除いた平均高速化を3.4倍と総括する。しかし表3の個別値には、4070上の7BモデルでFP16の一部がCPUへ退避して約67倍の時間差を生じる例と、4080上のGPT-2でINT8がむしろ遅くなる例が共存する。したがって、この論文を「8ビット整数演算は常に3.4倍速い」と読むのは不正確である。モデルのメモリ常駐、カーネル処理、出力品質という異なる軸を分離して解釈する必要がある。

## 問題設定と比較対象

低ビット化によって重みの保存量は減るが、実行時の速度は重み容量だけで決まらない。FP16がVRAMへ収まらなければ、推論時にCPUメモリとGPUの間で重みや中間データの移動が発生する。反対に、既にFP16で全て収まる小型モデルでは、量子化した重みの復元、尺度係数、整数演算の起動・実装効率が速度を制限する。CPUオフロード回避による利益と、GPU内の低精度カーネル自体の利益は別の因果要因である。

本研究はINT4、GPTQ、AWQ、QAT等の最適手法を競わせるものではない。一般的なINT8 PTQを、入手しやすいノートPC GPUで運用した際の基準点として測る。比較するFP16生成文も真の正解ではなく、同一モデルの異なる数値精度から得られた出力である。したがってBLEUやROUGEは出力の一致度を測るが、事実正確性や推論問題の正答率を測るわけではない。

## 手法

### 1. モデルと量子化設定の作成

原著Algorithm 1は、モデル名を受け取ってトークナイザを読み込み、まず`torch_dtype=float16`でFP16モデルをロードする。次に`load_in_8bit=True`を指定したINT8モデルを別にロードする。両者とも`device_map=auto`を使用するため、GPUメモリ容量を超える場合にはCPUへの自動配置が入り得る。ここで重要なのは、量子化前後で「同じGPU上で全層が動く」とは保証されない点である。FP16でオフロードが生じた場合、その速度はGPU内のFP16演算の純粋な性能ではない。

INT8側は既存ライブラリが提供する学習後量子化経路を利用する。論文は新規の尺度最適化、混合精度の層割当、低ビット学習を実装していない。処理の入口は既存checkpointで、出口はFP16とINT8の生成文、生成に要した壁時計時間、語彙一致指標である。量子化によるモデルの軽量化が配置を変える可能性も含め、実配備に近い比較として位置付けられている。

### 2. 生成条件を統一する

同一プロンプトを両精度のモデルへ入力し、greedy decodingで最大256個の新規トークンを生成する。batch sizeは1、top-kとtop-pは無効、repetition penaltyは1.0、温度は1.0でサンプリングを行わない。乱数seedは固定し、1回のウォームアップを計測から除外する。時間はモデルロード時間ではなく生成フェーズの壁時計時間である。入力はモデルのコンテキスト内に収め、padding/truncationは行わない。

この条件統一は、サンプリングの偶然による出力差を抑える。ただしGPUのTGP、メモリ構成、driver、実行時のクロック、実際に生成されたトークン数などは結果の外挿に関わる。特に壁時計時間は最大256トークンという上限を持つ一例であり、厳密な同一出力長でのkernel-only latencyではない。表3は同じモデル・同じGPU・異なる精度という組合せ内で読むのが適切である。

### 3. 語彙指標と意味評価を分ける

生成後は、INT8の出力を同一モデルのFP16出力と比較し、BLEU、ROUGE-1、ROUGE-Lを計算する。BLEUはn-gramの一致、ROUGE-1は単語の重複、ROUGE-Lは最長共通部分列に依存するため、同じ意味を言い換えた文章でも低下し得る。50プロンプトの集計と、20プロンプトの人手作成参照文との比較は、参照先が異なるため同じ指標名でも単純に差し引けない。

補完的にGPT-4oとGemini 2.5 Flashで、関連性、流暢さ、構成、説明の深さを定性的に評価する。これらの評価は人間による盲検・大規模採点ではなく、評価者モデルの傾向を含む。主題に沿っていても説明が断片的になるという観察は、語彙一致指標と独立の観測として読むべきである。

## 評価

### 実行環境と表3の速度結果

著者が明記した環境はPyTorch 2.1.2、Transformers 4.38.2、BitsAndBytes 0.42.0、CUDA 12.1である。GPUはデスクトップのRTX 4070/4080ではなく、Laptop版である。以下は原著Table 3の値で、時間比は同一モデル・同一GPUのFP16秒をINT8秒で割った値である。

| GPU | モデル | FP16秒 | INT8秒 | FP16 token/s | INT8 token/s | 時間比 |
|---|---|---:|---:|---:|---:|---:|
| RTX4070 Laptop | GPT-2 | 23.21 | 17.37 | 11.03 | 14.74 | 1.34倍 |
| RTX4080 Laptop | GPT-2 | 1.10 | 2.01 | 231.73 | 127.36 | 0.55倍 |
| RTX4070 Laptop | LLaMA-2-7B-Chat | 1244.29 | 18.63 | 0.21 | 13.74 | 66.79倍 |
| RTX4080 Laptop | LLaMA-2-7B-Chat | 50.04 | 26.64 | 5.12 | 9.61 | 1.88倍 |
| RTX4070 Laptop | Qwen1.5-1.8B-Chat | 12.66 | 11.78 | 20.22 | 21.73 | 1.07倍 |
| RTX4080 Laptop | Qwen1.5-1.8B-Chat | 13.61 | 11.08 | 18.81 | 23.10 | 1.23倍 |

4070上のLLaMA-2ではFP16の0.21 token/sが異常に低い。論文は`device_map=auto`による暗黙のCPUオフロードを明示し、GPU-only FP16の性能値と区別する。INT8がGPU内へ収まったためにホスト・デバイス転送を回避した効果が大きいので、66.79倍を整数演算器の倍率として扱うことはできない。実際、4080上の同モデルでは比較は1.88倍へ縮む。

逆に4080上のGPT-2では、FP16が1.10秒でINT8が2.01秒と、量子化で約83%時間が増える。小型モデルの行列サイズや量子化処理費用では、重み容量削減が実行時間の利益へ変わらないことを示す重要な負の結果である。4070のQwenも1.07倍にとどまり、どの構成でも一律に3.4倍改善するという主張は支持されない。平均3.4倍は著者が定めた除外条件を含む総括値であり、表3の各行を置き換えるものではない。

### 文章品質と参照の違い

原著の50プロンプト集計では、LLaMA-2-7B-Chatの4070上のINT8対FP16 BLEU平均は0.180±0.007、Qwen1.5の4080上では0.113±0.004である。これは生成したINT8文章がFP16文章とどの程度語彙・語順を共有するかの指標であり、FP16が正しいことの証明ではない。人手参照文を使う20プロンプトの比較では、LLaMA-2の4070でBLEUが0.10±0.02、Qwen1.5の4080で0.10±0.02となる。参照文の書き方が変わるため、単純に「量子化が追加で0.08悪化した」と読むのは誤りである。

単一プロンプトのQwen1.5・4070でのINT8対FP16はBLEU 0.1327、ROUGE-1 0.4896、ROUGE-L 0.3021と報告される。50件平均とは標本が違う。GPT-4o/Geminiによる評価では、量子化後の文章は主題との関連性を保ちながら、説明の構成・語彙の豊かさ・段落間の流れが劣化する場合がある。一方、4070のQwenではINT8がより技術的に具体的な出力を示す個別例もあり、FP16があらゆる出力で常に良いわけではない。

### 評価の強みと不足

本研究の長所は、量子化後のトークン毎秒だけでなく、同じGPUのFP16基準、CPUオフロードの影響、文章品質の参照先を並べたことである。数値の見かけの改善を生む配置変更と、実際に生成される内容の変化を一つの論文で検討できる。ただしこの比較はバッチ1・単一要求のデコードであり、並列リクエスト、連続バッチング、KVキャッシュの長期保持、prefix caching、分散サービングの性能を直接測らない。

## 既存研究との差と実務的示唆

AWQやGPTQは重みの量子化誤差を減らす独自アルゴリズムを持ち、QATは学習時に低精度の影響を取り込む。これに対して本研究は既存のINT8 PTQを使うため、最先端の圧縮率や低ビット精度の競争ではなく、比較的標準的な実装を選んだ場合の配備特性を測る。既存GPUのメモリ容量を超えるモデルで量子化が劇的に効くという観察は、VRAM制約のある環境で方式を選ぶ際に有用である。

実務では、まずFP16モデルがGPUへ完全常駐しているかを確認し、次にINT8でCPUオフロードが消えるかを調べる。そのうえで同じ入力長・出力長・batch・モデル・GPUでTTFT、TPOT、メモリ使用量、品質を測り直す必要がある。小型モデルでINT8の方が遅い例を無視して、ビット幅だけで高速化を保証するのは危険である。コード生成のように構文と論理的一貫性が重要な用途では、単語一致よりもテスト実行や課題正答率の測定を追加すべきである。

## 限界

評価モデルはGPT-2、LLaMA-2-7B-Chat、Qwen1.5-1.8B-Chatに限られ、MoE、現行の巨大推論モデル、長文コンテキスト、画像入力、複数GPUの性能へ一般化できない。Laptop GPUのTGPやVRAMは機種ごとに異なり、RTX4070/4080という型番だけで再現性が確保されるわけではない。使用ソフトウェアの版も固定されており、後続の量子化カーネルやドライバ更新による差は未評価である。

INT8以外のINT4/FP8/BF16や混合精度、層別量子化の切除実験はなく、どの層の誤差が文章品質低下を生むかも特定できない。CPUオフロードを含む比較は実運用上の重要な事例だが、演算方式だけの厳密な対照実験ではない。RTX4080のGPT-2ではINT8が悪化し、4070のLLaMA-2の極端な高速化はメモリ配置差に依存する。この両方を報告することが、定量結果を過大に一般化しないための必須条件となる。

BLEU/ROUGEは語彙重複を測るため、正答性、事実性、推論能力、コード実行の正しさを直接保証しない。GPT-4oとGeminiの評価も評価者依存である。50プロンプトという限定的な分布では、P95/P99遅延や本番サービスの負荷条件、量子化誤差に対する長期安定性を示せない。著者の結論を採用する際には、用途別の品質試験を追加する必要がある。

## 一次資料と検証範囲

- 出版社HTML全文: https://www.techscience.com/cmc/v87n3/66994/html
- 正式PDF（28ページ）: https://cdn.techscience.cn/files/cmc/2026/TSP_CMC-87-3/TSP_CMC_78985/TSP_CMC_78985.pdf
- DOI: https://doi.org/10.32604/cmc.2026.078985
- 本稿はPDF Algorithm 1、Table 1・3・9・10・12、§4・§5とAppendix Aの比較条件を確認した。旧blocked稿の見出し認識失敗を修復するため、手法と評価を明示節に再構成した。未測定のGPUや別の量子化方式について性能値を推測していない。
