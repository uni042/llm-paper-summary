---
canonical_id: arXiv:2403.01632
arxiv_id: '2403.01632'
arxiv_categories:
  primary: cs.LG
  cross_list:
    - cs.FL
    - cs.PL
    - cs.SE
title: 'SynCode: LLM Generation with Grammar Augmentation'
summary: 文脈自由文法の逐次解析から許容終端列と未確定末尾を求め、決定性有限オートマトンの事前計算マスク表からLLM語彙の許可集合を高速に生成するSynCode。JSONの構文エラー0件、Python・Goの平均構文エラー96.07%減を報告するが、文法マスクは意味的正しさを保証せず、マスク表の構築に最大約10分・2GB弱を要する。
list_summary: 逐次構文解析とDFA語彙マスク表による制約付き復号。JSON構文違反をゼロ、Python・Goの構文違反を平均96.07%減。
authors:
  - Shubham Ugare
  - Tarun Suresh
  - Hangoo Kang
  - Sasa Misailovic
  - Gagandeep Singh
published: '2024-03-03'
publication: Transactions on Machine Learning Research (2025); arXiv:2403.01632v4
publication_type: journal
publication_status: published
source: https://arxiv.org/pdf/2403.01632
sources:
  - https://arxiv.org/abs/2403.01632
  - https://arxiv.org/pdf/2403.01632
  - https://mlanthology.org/tmlr/2025/ugare2025tmlr-syncode/
  - https://github.com/structuredllm/syncode
implementation: PyTorch・Transformers・Larkで文法終端のDFAマスク表を事前構築し、生成時は部分構文解析で得た許容終端からLLM語彙のマスクを計算。公式実装はstructuredllm/syncodeで公開。
code: https://github.com/structuredllm/syncode
references:
  - canonical_id: arXiv:2306.10763
  - canonical_id: DOI:10.1145/356628.356629
  - canonical_id: arXiv:2210.14868
  - canonical_id: arXiv:2108.07732
  - canonical_id: arXiv:2407.02742
  - canonical_id: DOI:10.1145/3591300
  - canonical_id: arXiv:2403.06988
  - canonical_id: DOI:10.18653/v1/2020.emnlp-main.576
  - canonical_id: arXiv:2005.14165
  - canonical_id: DOI:10.48550/arxiv.2302.01318
  - canonical_id: arXiv:2107.03374
  - canonical_id: arXiv:2207.02098
  - canonical_id: DOI:10.1145/3597926.3598048
  - canonical_id: DOI:10.1145/362007.362035
  - canonical_id: DOI:10.18653/v1/2020.findings-emnlp.384
  - canonical_id: DOI:10.1162/tacl_a_00306
  - canonical_id: arXiv:2211.17192
  - canonical_id: arXiv:2211.09110
  - canonical_id: arXiv:2306.08568
  - canonical_id: arXiv:2402.17988
  - canonical_id: arXiv:2302.07842
  - canonical_id: OpenReview:nRB8VpeM7b
  - canonical_id: arXiv:2203.13474
  - canonical_id: DOI:10.18653/v1/2023.emnlp-main.313
  - canonical_id: arXiv:2305.12295
  - canonical_id: arXiv:1912.01703
  - canonical_id: OpenReview:KmtVD97J43e
  - canonical_id: arXiv:1803.00676
  - canonical_id: DOI:10.18653/v1/2021.emnlp-main.779
  - canonical_id: arXiv:2408.00118
  - canonical_id: arXiv:2302.13971
  - canonical_id: arXiv:2307.09288
  - canonical_id: DOI:10.1145/3611643.3616271
  - canonical_id: arXiv:2308.10462
  - canonical_id: arXiv:2307.09702
  - canonical_id: DOI:10.18653/v1/2020.emnlp-demos.6
  - canonical_id: OpenReview:IUikebJ1Bf0
  - canonical_id: arXiv:2310.13897
  - canonical_id: arXiv:2306.15626
  - canonical_id: DOI:10.18653/v1/d18-1425
  - canonical_id: arXiv:2312.07104
  - canonical_id: DOI:10.1145/3597503.3639125
references_checked_at: '2026-10-15'
references_source: arxiv-pdf-reference-section
references_total: 54
last_checked: '2026-10-15'
worker_completed_at: '2026-10-15T12:33:12+09:00'
worker_run_key: 20261015-1233-scheduled-chat-30/r01
last_audited: '2026-10-15'
audit_version: 1
under16kb_reaudit_target_path: papers/inference/99-other-inference-systems/2024-2403.01632-syncode-llm-generation-with-grammar-augmentation.md
under16kb_reaudit_source_git_blob_sha: 'd1626714e89bd2ac599c05e89d744f1e31d0e42b'
under16kb_reaudit_source_sha256: 'ed930b210b8bd3d80f89f229fe144f3a065123397bd5a20709a4a99a7dca6b84'
under16kb_reaudit_version: '2026-10-07-v1'
under16kb_reaudit_passed: true
quality_body_chars: 6590
quality_method_chars: 1722
quality_eval_chars: 2743
quality_limitation_chars: 523
quality_self_review_passed: true
quality_self_review_version: '2026-10-07-v1'
---

# SynCode：文脈自由文法を使う構文保証と語彙マスクの高速化

## 概要

SynCodeは、言語モデルがJSON、SQL、Python、Goなどの形式言語を生成する際に、文脈自由文法（CFG）を満たすトークンだけを次の候補として残す制約付き復号方式である。出力済み文字列を逐次解析し、文法上続けられる終端記号列を求めた後、決定性有限オートマトン（DFA）に基づく事前計算の語彙マスク表を参照する。LLMのトークンと文法の終端記号が一致しない場合でも、合法な続きを誤って消さないようにすることが技術的な中心である。

原著のJSON生成実験では、Llama-2-7B-chatとGemma2-2B-itの両方で構文エラーを0件とし、Gemma2-2B-itの明示的なJSON指示ではスキーマ適合率100%を得た。PythonとGoのコード生成では、無制約生成と比べて構文エラーを平均96.07%削減した。一方、構文的に正しいプログラムでも意味的に正しいとは限らず、コードの機能正答率の改善は小さい条件がある。また、DFAマスク表の構築には、文法と語彙の組合せによって数分から約10分、最大2GB弱のメモリを要する。

## 問題設定：文法終端とLLM語彙のずれ

文脈自由文法は、識別子や数値、演算子、括弧といった終端記号の並びを非終端規則で制約する。一方、言語モデルのトークナイザは学習時に固定したサブワード語彙を使うため、一つのモデル語彙トークンが複数の文法終端をまたぐ場合がある。例えば整数に見える末尾文字列が、次の小数点や数字によって浮動小数点数の字句へ変わることがある。字句境界を早く確定しすぎると、文法上は有効な次トークンを誤って除外してしまう。

SynCodeは、生成途中の文字列C_kが文法Gの有効な完成文字列の接頭辞集合L_p(G)に属し続けることを目標とする。現在のC_kから、次に連結しても有効な接頭辞を保つ語彙集合V_kを求め、他のトークンを復号時にマスクする。モデルの重みや学習データを変えず、貪欲生成、確率標本化、ビーム探索などのトークン選択直前へ組み込める点が利点である。

## 手法

### 1. 逐次字句解析と未確定の末尾文字列

生成済みの文字列を、字句解析によって確定した終端記号列と、後続文字によって字句の種類が変わり得る末尾文字列rへ分ける。原著は1文字先読み・バックトラックなしの字句解析器を仮定する。確定済み部分は次の生成ステップでも字句の種類が変わらず、rだけを再検討すればよいため、全文を毎回先頭から解析する必要がない。

例えば数値の末尾が「2」で終わっていても、次に「.」が来れば浮動小数点数になる可能性があるため、最後の字句をrとして扱う。未解析の接尾辞「2.」がある場合も同様にrへ入れる。部分構文解析器は確定した終端列から、次に続けられる終端記号列の集合Aを計算する。ここでのAは文法上の終端記号の候補であり、LLMの語彙トークンIDの集合とは異なる。

### 2. DFAマスク表の事前計算

各終端記号を定義する正規表現から決定性有限オートマトンを作り、DFAの状態qと、先に続く終端記号列に応じて、LLM語彙Vの各トークンが許容されるかを真偽値マスクとして事前計算する。このDFAマスク表は、文法とトークナイザ語彙の組合せに対して一度構築すれば繰り返し利用できる。推論中に毎ステップすべての語彙文字列を正規表現へ照合する方式より、表参照で許容候補を高速に得られる。

原著では先読みする終端数を制御するパラメータαを導入し、主にα=0、1の構成を用いる。先読みを増やすと候補をより細かく判定できるが、終端記号の種類数が増えるとマスク表の組合せも増える。表はCPU上の逐次処理を減らし、GPUでのマスク統合を利用できる一方、異なる語彙・文法の組合せへ同じ表を無条件に再利用できない。

### 3. 部分構文解析から許容語彙を計算

各生成ステップで、構文解析器が得た許容終端列Aと未確定末尾rをDFAマスク表へ渡す。まずrを候補終端のDFAへ入力して到達状態を求め、次に続けられる終端列のマスクを表から取得する。複数の許容終端列がある場合はマスクの論理和をとり、最終的な許容語彙集合V_kを構成する。LLMが出力した次トークンの確率分布からV_k以外を除外し、残りの確率を正規化して通常の復号へ戻す。

この処理は、出力をすべて生成した後に構文検査する方式とは異なる。各トークン選択の時点で不正な続きが排除されるため、後段の構文エラーによる再生成を減らせる。文法上の許容終端列を正しく計算することと、LLM語彙へ安全に写像することが両方必要であり、単なる固定文字列のブラックリストでは代替できない。

### 4. 健全性・完全性の条件

原著が論じる健全性は、文法上有効な次トークンを不当に除外しないことを意味する。完全性は、指定された条件下で不正な次トークンを排除できることを指す。これらはプログラムの意味や業務ルールが正しいという保証ではない。例えば構文的に有効なJSONでも必須キーが欠けたり、値の型が要求と異なったりする場合がある。

また、生成が最大トークン長で打ち切られた場合、途中まで有効な接頭辞であっても完成したプログラムにならない。原著のPython・Go実験で構文エラーが完全にはゼロにならない主要な理由は、この生成長制限である。字下げや改行時の字句規則など、言語固有の構文要素に対する追加処理も必要になる。

### 5. 生成時間と表構築費用の分離

SynCodeの実行時は、部分解析、DFA状態遷移、表参照、語彙マスクの統合という追加処理が必要である。ただし表は事前計算でき、許容候補のマスクをGPU上で処理できる。構文制約によって余計な自然言語説明が減れば、生成トークン数自体が短くなり、総生成時間が無制約より小さくなる場合もある。これはマスク処理が負の費用を持つという意味ではない。

構築時間は文法の終端数やモデル語彙数に依存し、数百秒とGB級のメモリを要する条件がある。多くの要求で同じ文法を使う場合は構築費用を償却できるが、利用者ごとに新しい文法を作る用途では初期費用が無視できない。モデルのトークナイザが変わった場合も表の再構築が必要である。

## 評価

### ハードウェア・モデル・比較対象

原著は48コアのIntel Xeon Silver 4214RとNVIDIA RTX A5000 GPU 2基を使用し、PyTorch、Transformers、Larkで実装した。JSON生成はJSON-Mode-Evalの100問題をLlama-2-7B-chatとGemma2-2B-itで評価する。SQLはSpiderの1,034問題でLlama-2、Llama-3.2-1B/3B、Gemma2を比較する。Python・Goのコード生成はHumanEvalとMBXPを用い、CodeGen-350M、WizardCoder-1B、LLaMA-7Bで評価した。

比較には無制約生成、Outlines、guidance、llama.cpp、GCDを含む。llama.cppの比較は実験機とのCUDA互換性のためCPU上で実行されており、GPU上のSynCodeと同一条件でのカーネル性能比較ではない。マスク表の構築時間は生成時間から除外して別に測定する。構文エラー、JSONスキーマ適合率、SQLの実行成功率と正答率、コードのpass@1、平均生成時間は、それぞれ別の指標である。

### JSON構文・スキーマ適合（原著表1）

| モデル・指示 | 方式 | 構文エラー（100件中） | スキーマ適合率 | 平均生成時間 |
|---|---|---:|---:|---:|
| Llama-2-7B、通常 | 無制約 | 98 | 2% | 3.58秒 |
| Llama-2-7B、通常 | SynCode | 0 | 66% | 3.07秒 |
| Llama-2-7B、明示 | 無制約 | 41 | 58% | 3.11秒 |
| Llama-2-7B、明示 | SynCode | 0 | 84% | 3.02秒 |
| Gemma2-2B、通常 | 無制約 | 59 | 41% | 4.32秒 |
| Gemma2-2B、通常 | SynCode | 0 | 99% | 4.82秒 |
| Gemma2-2B、明示 | 無制約 | 59 | 41% | 5.82秒 |
| Gemma2-2B、明示 | SynCode | 0 | 100% | 4.74秒 |

Llama-2の通常指示では、無制約生成の98件が構文不正であったが、SynCodeでは0件になった。一方、SynCodeのスキーマ適合率は66%で、構文が正しいことと要求されたキー・型が正しいことは一致しない。Gemma2の通常指示では構文エラーを59件から0件へ減らしたが、生成時間は4.32秒から4.82秒へ増えた。すべての条件で速度が向上するわけではない。

### SQLの正答率・実行成功率（原著表2）

| モデル | 方式 | 正答率 | 実行成功率 | 平均生成時間 |
|---|---|---:|---:|---:|
| Gemma2-2B | 無制約＋SQL抽出 | 25.4% | 77.6% | 9.893秒 |
| Gemma2-2B | SynCode | 26.3% | 78.2% | 5.876秒 |
| Llama-2-7B | 無制約 | 20.4% | 32.6% | 1.148秒 |
| Llama-2-7B | SynCode | 24.6% | 41.6% | 1.483秒 |
| Llama-3.2-1B | 無制約 | 25.6% | 51.1% | 0.509秒 |
| Llama-3.2-1B | SynCode | 28.8% | 59.0% | 0.916秒 |
| Llama-3.2-3B | 無制約 | 28.6% | 67.4% | 0.846秒 |
| Llama-3.2-3B | SynCode | 34.9% | 81.4% | 1.164秒 |

SQLの実行成功率はSQLiteで実行時エラーなく動く割合で、正答率は質問の意味に合うSQLを生成できた割合である。Llama-3.2-3Bは実行成功率67.4→81.4%、正答率28.6→34.9%へ改善したが、生成時間は0.846→1.164秒へ増えた。Gemma2では不要なマークアップや説明文を抑えて生成時間が9.893→5.876秒となったが、この差を全モデルへ一般化できない。

### Python・Goの構文エラーと機能正答率（原著表3・4）

HumanEvalのCodeGen-350MではPythonの構文エラーが271件から15件、Goが573件から49件に減った。WizardCoder-1BではPythonが36件から3件、Goが1,031件から50件に減った。MBXPのLLaMA-7BではPythonが148件から5件、Goが414件から1件に減った。原著の平均96.07%削減という総括は、すべての条件で構文エラーがゼロになるという意味ではない。

WizardCoder-1BのHumanEvalではPythonのpass@1が20.0%から20.0%で変化せず、Goは9.3%から9.5%への小幅改善だった。Pythonのpass@10は27.6%から28.4%、Goは12.5%から13.7%である。構文エラーの大幅削減が機能的な正しさの同程度の改善を保証しないことを示す。最大生成長に達して終了記号が出ない場合、合法な接頭辞のまま生成が打ち切られ、不完全なコードが残る。

### DFAマスク表の構築費用（原著表5）

| モデル・文法 | 構築時間 | マスク表のメモリ |
|---|---:|---:|
| Llama-2-7B・JSON | 113.72秒 | 181MB |
| CodeGen-350M・Python | 602.26秒 | 1.87GB |
| CodeGen-350M・Go | 603.03秒 | 1.58GB |
| WizardCoder-1B・Python | 588.28秒 | 1.83GB |
| LLaMA-7B・Python | 382.26秒 | 1.17GB |

JSON文法の表は比較的小さいが、Python・Goでは終端記号数が多く、表構築に数百秒とGB級のメモリが必要となる。同じ文法と語彙を使うサーバーでは一度の構築を多数の要求で償却できる。一方、ユーザー定義文法を頻繁に変更する用途や、複数モデルで異なるトークナイザを扱う用途では、事前計算の費用と表のキャッシュ管理が支配的になる可能性がある。

## 限界と負の結果

第一に、文法制約は構文を保証するだけで、JSONスキーマのキー・型、SQLの意味、プログラムの単体テスト合格を保証しない。第二に、最大生成長で打ち切られた場合、完成したコードとして構文が不正になることがある。第三に、PythonやGoの全言語仕様を完全に網羅した評価ではなく、実験に用いた文法と字句解析器の前提を満たす範囲での結果である。

第四に、マスク表は語彙と文法に依存するため、別モデルや別文法への流用が難しい。第五に、表の構築には最大約10分、2GB弱のメモリが必要であり、文法が頻繁に変わるアプリケーションでは負担になる。第六に、制約付き復号は必ずしも高速ではなく、Gemma2のJSONやLlama-3.2のSQLでは平均生成時間が増加した。第七に、論文のllama.cpp比較はCPU上で行われたため、同一GPU条件での優劣は結論できない。

さらに、部分構文解析には1文字先読み・バックトラックなし等の仮定があり、任意の曖昧な文法へ形式的な保証をそのまま拡張できるわけではない。生成内容の意味的妥当性を確かめるには、JSONスキーマ検査、SQL実行・権限検査、コードの単体テストなど、別の検証機構が必要となる。

## 既存研究との差と実装上の示唆

SynCodeは、逐次構文解析から許容終端列を求め、DFA状態とLLM語彙の事前計算マスク表を組み合わせる。Outlinesやguidanceなどの制約付き復号と同じ課題を扱うが、末尾の未確定字句r、許容終端列A、DFAマスク表の連結により、サブワード語彙と文法終端の不一致を扱う点が中心である。文法制約を事後検査へ回す方式と異なり、不正な次トークンを生成時に除外する。

推論基盤への組み込みでは、トークナイザごとのマスク表生成とキャッシュ、逐次解析状態のセッション別保持、GPUへのマスク転送・統合、生成停止条件の設計が必要となる。構文的に正しい結果を得るための制御費用と、不要な生成トークンが減る効果を別々に測ることが重要である。原著の構築時間とメモリをそのまま別のGPU・別の語彙・別の文法へ適用することはできない。

## 一次資料・照合箇所

- 原著第4版：https://arxiv.org/pdf/2403.01632
- 書誌：https://arxiv.org/abs/2403.01632
- 掲載版：https://mlanthology.org/tmlr/2025/ugare2025tmlr-syncode/
- 公式実装：https://github.com/structuredllm/syncode
- 手法：原著§3.2〜§4（部分解析、DFAマスク表、健全性・完全性）。
- 評価：原著表1（JSON）、表2（SQL）、表3・4（Python・Go）、表5（マスク表構築）。
