---
canonical_id: DOI:10.18653/v1/2026.findings-acl.1655
arxiv_id: null
arxiv_categories: null
title: 'LogitSpec: Accelerating Retrieval-based Speculative Decoding via Next Next Token Speculation'
summary: 検索ベースの投機的生成は追加draftモデルを不要にするが、prompt中のn-gramが一致しないと候補を得られない。LogitSpecはtarget LLMの直近logit上位kに次々トークンが含まれやすい経験的性質を使い、次トークンと次々トークンの両方を鍵にprompt・生成済み文脈から後続列を検索する。候補木を作りtargetモデルで並列検証する。Vicuna 7B・CNN/DMで平均受理長3.28、自己回帰比2.61倍、4課題平均2.26倍。A100上のbatch1・greedyを中心に評価し、検索対象が少ない短いpromptや実運用のcontinuous batchingで同じ利得を保証しない。
list_summary: "LogitSpecは対象の直近logitから次々トークン候補を推定し、プロンプト内n-gram検索の照合範囲を広げる学習不要の投機的生成。Vicuna 7B/CNN-DMで2.61倍、平均受理3.28。"
authors:
- Tianyu Liu
- Qitan Lv
- Hao Li
- Xing Gao
- Xiao Sun
- Xiaoyan Sun
published: '2026-07-02'
publication: Findings of ACL 2026, pp. 33070–33092
publication_type: conference
publication_status: published
source: https://aclanthology.org/2026.findings-acl.1655.pdf
sources:
- https://aclanthology.org/2026.findings-acl.1655.pdf
- https://aclanthology.org/2026.findings-acl.1655/
implementation: PyTorch 2.6.0、CUDA 12.4、Transformers 4.37.1（Vicuna/Llama2）および4.57.1（Llama3.1/Qwen3）。7～33BはA100 SXM 80GB×1、70Bは×2。prompt由来n-gramをhash索引へ格納し、候補木をtree attentionで検証。原著が実装URLを明示する。
code: https://github.com/smart-lty/LogitSpec
last_checked: '2026-10-26'
worker_id: scheduled-chat-45
worker_completed_at: '2026-10-26T22:56:50+09:00'
worker_run_key: 20261026-2245-scheduled-chat-45/r01
reference_main_sha: 4bc39e85c86cd398a0c6f441df3c7789a7f22785
quality_self_review_passed: true
quality_self_review_version: PAPER-QUALITY-GUIDE-2026-10-07
last_audited: null
audit_version: 0
references:
- canonical_id: arXiv:2502.17421
- canonical_id: arXiv:2503.01840
- canonical_id: arXiv:2309.08168
- canonical_id: arXiv:2501.19309
- canonical_id: arXiv:2401.10774
- canonical_id: arXiv:2405.00263
- canonical_id: arXiv:2503.10135
- canonical_id: arXiv:2402.02057
- canonical_id: arXiv:2410.06916
- canonical_id: ACL:2024.acl-long.681
- canonical_id: DOI:10.48550/arxiv.2302.01318
- canonical_id: arXiv:2405.19715
- canonical_id: arXiv:2402.02082
- canonical_id: arXiv:2401.15077
- canonical_id: arXiv:2406.16858
- canonical_id: arXiv:2406.17276
- canonical_id: arXiv:2408.11850
- canonical_id: arXiv:2408.15766
- canonical_id: arXiv:2310.12072
- canonical_id: arXiv:2404.19737
- canonical_id: arXiv:2402.05109
- canonical_id: arXiv:2211.17192
- canonical_id: arXiv:2311.08252
- canonical_id: arXiv:2402.01528
references_checked_at: '2026-10-26'
references_source: primary-pdf-reference-section
references_total: 4
---

# LogitSpec：次々トークン予測を検索キーに加える投機的デコード

## 概要

投機的デコードは、軽いdraft側が将来トークン候補を提案し、大きなtargetモデルが複数候補を一度のforwardで検証する。target分布を保つ検証規則を使えば、逐次生成と同じ出力分布を維持したまま1回のtarget forwardで複数トークンを確定できる。ただし専用draftモデルを訓練・常駐させる方式は、追加の重み、KVキャッシュ、モデル更新への追随、複数モデルの配信管理が必要になる。

Prompt Lookup Decoding（PLD）やRESTなどの検索ベース方式は、入力promptや過去の生成文、外部コーパスに現れたn-gramの後続列をdraftとして再利用する。追加モデルは不要だが、直近トークン列が参照文と一致しないと候補を得られない。LogitSpecは、**targetモデルの直近logitには次トークンだけでなく、そのさらに次のトークンを予測する情報も残っている**という経験的観察を利用する。直近logitの上位候補から「次々トークン」を推定し、そのトークンを手掛かりに検索対象を増やす。

具体的には、次トークンを決めた後、直近logit上位k個から次々トークン候補を列挙し、両者を起点にprompt・生成済み文脈のn-gramを検索する。取得した複数の後続列を木へ組み立て、targetモデルがtree attentionで一括検証する。専用draft重みを持たず、学習不要で実装できる点が特徴である。

Vicuna 7B・CNN/DailyMailでは、平均受理トークン数（MAT）3.28、逐次自己回帰デコード比2.61倍の速度を報告する。Vicuna 7Bの4評価集合平均はMAT 2.76、速度2.26倍であり、最大値2.61倍と平均2.26倍は異なる集計である。**追加draftモデルを使わないことと、検索や木マスクの費用がゼロであることは同義ではない。**

## 問題設定と既存研究との差

### 検索ベースのdraftが外れる理由

検索ベース投機では、現在のprefix末尾m個のトークン列を検索キーとして、同じ列が現れた参照テキストから後続n個を取り出す。mを長くすると一致した候補の信頼性は上がるが、そもそも一致する参照が少なくなる。mを短くすると一致件数は増えるが、文脈に合わない後続列が混ざりやすい。

PLDはpromptと生成済みテキストから参照を構築する。RESTは外部の参照集合を使う。Lookaheadは過去に破棄した候補列を参照する。これらはいずれも、検索の入口となるトークン列の一致条件に依存する。原著はPLDで3割超のdecode stepに一致候補がない場合があると述べる。たとえば「What is the area of the triangle?」の回答で「the」の後続を探すと、参照文中の「the triangle」が誤って強く一致し、本当に続けたい「area」を見落とす。

LogitSpecは「次トークンがtheである」と決まったとき、直近logit上位候補に含まれる「area」を次々トークン候補として追加し、「the area」に一致する参照を探す。つまり、検索の前に小さなモデルを追加するのではなく、**targetがすでに計算したlogitを検索ヒントとして再利用する**。

### 次々トークンをlogitから推定できるという観察

通常の次トークン分布は、厳密には次々トークンの条件付き分布そのものではない。しかしtargetの最終hidden stateは文脈全体を表現しており、logit上位語にはさらに先の文脈に現れやすい語も含まれる。原著はVicuna 7B/13B/33B、Llama 3.1 8B、Qwen2.5 0.5B/7Bの計6モデルと13タスクで、真の次々トークンが直近logitの上位60語に入る割合を測った。

結果は多くの条件で50%超、Llama 3.1 8Bでは約64%だった。ただしこれは「次々トークンを64%の確率で確定できる」ことではなく、**候補集合60個の中に真のトークンが含まれる割合**である。top-1予測の正解率や、実際のdraft列の受理率とは異なる。著者らはこの性質の形式的理論説明を今後の課題としている。

## 手法

### 1. targetの直近logitから次々トークン候補を列挙する

prefixをx、targetの最後のlogitをpとする。まず通常どおり次トークンx_{i+1}をpから得る。次に同じpの上位k個を取り、x_{i+1}自体を除いた集合Lを次々トークン候補とする。追加のモデルforwardを行わず、既存logitの順位を読むだけで検索キー候補を得る。

ここでLの要素は「次々トークンの真の分布からサンプルしたもの」ではない。あくまで検索を広げるヒントであり、最終出力へそのまま確定することはない。候補木をtargetで検証するため、誤ったヒントが混ざってもtargetの出力分布を守る仕組みを適用できる。

### 2. 次トークンと次々トークンの両方でn-gramを検索する

検索対象Rは、ユーザーの入力promptと、それまでに生成したトークン列から構築する。原著の基本実装では外部データベースを使わないため、異なるユーザーの検索履歴や外部文書に依存しない。各n-gramから後続列を得る索引を作り、次トークンx_{i+1}を末尾に持つm-gramと、次々候補x̃_{i+2}を末尾に持つm-gramの双方で照合する。

検索はm=3から試し、一致がなければm=2などへ短縮する。次々候補は複数あるため、同じpromptでも複数の検索経路が生まれる。これにより単一の直近m-gramでは見つからなかった参照へ到達しやすくなる。ただしmを短くすると誤一致も増えるため、取得した後続列は後段のtarget検証で選別する。

原著は素朴な全走査だと候補kとprompt長Lに比例する費用が大きいとして、promptを一度走査してn-gram→後続列のhash索引を構築する。構築はO(L)、各候補のhash照合は概ね定数時間、後続列のコピーは長さに依存する。本文の「O(n+k)」という簡略表記だけで候補数kとコピー長nの積を無視せず、Appendix D.3が記す `O(k×(1+n))` も考慮する。

### 3. draft木の容量を制限する

検索から得た後続列を無制限に並べると、target検証の注意計算が膨張する。LogitSpecは次々候補のlogit順位で保持長を変える。原著では順位8以内の候補は後続4トークン、順位32以内は3トークン、それより下位は次々候補自身だけを保持するという簡単な規則を採用する。draft木の総トークン数が容量Kを超えたら検索を打ち切る。

この割当は確信度の高い候補へ長い参照列を配り、低い候補へ短い枝を配る設計である。原著の主要設定ではK=64が用いられる。木容量を大きくすると候補の網羅性は増すが、target forwardで検証するトークン数も増える。Appendixでは64～128を超えると検証費用による収益逓減が起きると報告される。

### 4. tree attentionでtarget検証し、正しい分布を保つ

複数の候補列を一本の連結列としてtargetへ与える場合、別枝の候補同士が相互に注意してはいけない。LogitSpecは共通prefixと確定済み次トークンを全枝から見えるようにし、各枝の内部だけで因果注意を許可するブロック対角的なマスクを作る。位置IDも各枝の深さに合わせる。これにより各枝が独立に生成された場合と同じ条件でtargetのlogitを計算できる。

検証では、targetの確率分布に従う受理・棄却処理を行う。通常のspeculative samplingでは、draft分布qに対してtarget分布pを使い `min(1,p(token)/q(token))` で受理し、棄却時は正規化した正の残差から再サンプリングする。原著の主要実験は温度0のgreedyであり、非ゼロ温度の追加実験は附録で扱う。出力品質を保持するという主張は、この検証処理が正しく実装されることに依存し、検索候補が常に正しいことを意味しない。

## 評価条件と主要結果

### 実装・データセット

| 項目 | 原著の設定 |
|---|---|
| 主なtargetモデル | Vicuna 7B/13B/33B、Llama-2系列、附録でLlama 3.1 8BとQwen3 8B |
| GPU | 7～33BはNVIDIA SXM A100 80GB×1、70Bは×2 |
| ソフトウェア | PyTorch 2.6.0、CUDA 12.4、Transformers 4.37.1（新モデル追加実験は4.57.1） |
| 精度・生成 | FP16、温度0、batch=1、最大1024生成トークン |
| データ | Spec-Bench（対話・翻訳・要約・QA・数学・RAG）、CNN/DM、GSM8K、HumanEval、附録でMATH/AIME/LongBench |
| 比較 | 自己回帰、Lookahead、REST、PLD、SpS（Vicuna-68M draft）、附録でSAM Decoding/Token Recycling等 |
| 指標 | MAT（1 decode step当たりの平均確定トークン数）、自己回帰比のwall-clock速度 |

主表にVicunaを使う理由は、Lookahead/RESTなどの比較対象がVicuna/Llama-2系で再現しやすいためである。新しいLlama 3.1やQwen3への一般化は附録の別条件で示される。単一ユーザーのoffline decode中心であり、vLLM/SGLangのcontinuous batchingやGPU共有サービングでの実測ではない。

### VicunaでのMATと速度

| モデル | 課題 | LogitSpec MAT | LogitSpec速度比 | PLD速度比 |
|---|---|---:|---:|---:|
| Vicuna 7B | CNN/DM | **3.28** | **2.61倍** | 2.26倍 |
| Vicuna 7B | GSM8K | 2.69 | 2.20倍 | 1.62倍 |
| Vicuna 7B | HumanEval | 2.62 | 2.24倍 | 1.65倍 |
| Vicuna 7B | Spec-Bench | 2.44 | 2.01倍 | 1.59倍 |
| Vicuna 7B | 4課題平均 | 2.76 | 2.26倍 | 1.78倍 |
| Vicuna 13B | 4課題平均 | 2.67 | 2.18倍 | 1.68倍 |
| Vicuna 33B | 4課題平均 | 2.42 | 1.92倍 | 1.49倍 |

7BのCNN/DMではPLDの2.26倍に対してLogitSpecは2.61倍であり、**2.61倍は逐次生成を基準とする倍率**である。PLD比では2.61/2.26≈1.15倍となる。各課題の平均とモデル別の最大値を混同しない。MATが3.28でも速度が3.28倍ではないのは、候補検索・木マスク作成・検証・KV更新の費用があるためである。

### 検索成功率とアブレーション

原著Table 3の検索成功率は、Vicuna 7BのSpec-BenchでPLD 63.88%に対してLogitSpec 97.76%、HumanEvalでPLD 69.03%に対してLogitSpec 99.29%である。これは検索で何らかの候補を得られた割合であり、**その候補がすべてtargetに受理された割合ではない**。検索成功率が高いこととMATが高いことは関連するが、同一指標ではない。

Vicuna 7BのCNN/DMでは、完全版のMAT3.28・速度2.61倍に対し、次々logitのヒントを外した検索のみはMAT2.66・速度2.24倍、検索を外したlogitのみはMAT1.57・速度1.23倍となる。両要素の組合せで改善が大きい。Spec-Benchでも完全版MAT2.44・2.01倍に対し、検索なしはMAT1.57・1.24倍だった。単純なlogitのみ方式は1回で確定できる長さが最大2トークン程度に制約され、検索で長い後続列を得ることが重要である。

### 実行時間の内訳と追加比較

Vicuna 7B・Spec-Benchの時間内訳では、target forward 93.92%、注意マスク準備2.83%、候補検索1.17%、検証1.03%、KV更新1.05%と報告される。検索の比率は小さいが、マスク準備やtarget forwardの費用は残る。実装のhash索引が有効であることを示す一方、別のGPUやバッチサイズで同じ内訳になるわけではない。

附録Table 7のLlama-3.1-8B-Instruct、K=64、温度0のAIME/LongBench/MATH比較では、LogitSpecの速度が3.09/2.10/2.56倍、三課題平均2.58倍だった。Token Recyclingの平均2.40倍、SAM Decodingの平均2.34倍を上回る。ただしこれは主表のVicuna 7Bとは異なるモデル・課題であり、3.09倍を主表の最大2.61倍と矛盾する数値として扱わない。

## 既存方式との違いと導入上の示唆

EAGLE系は学習済みのdraft headや専用小型モデルを使い、高い受理率を狙うが、target更新に伴うdraft再訓練や追加重みの管理が必要になる。LogitSpecはtargetのlogitと既存文脈だけで候補を作るため、追加draftモデルをロードしない。ただし検索索引、tree attention、候補木の検証カーネルは必要であり、全く改造なしで任意サービング基盤へ統合できるわけではない。

PLDは直近n-gramの一致が必要で、低反復なタスクに弱い。LogitSpecは次々トークンの複数候補を検索の入口に加え、単一キーでは見つからない参照へ到達する。RESTは外部コーパスを使えるが、その品質・更新・メモリ・情報境界が別の運用問題になる。LogitSpecの基本実装はユーザーのpromptと生成済み文脈だけを使うため、外部コーパスを必要としないが、promptが短いと検索対象が乏しい。

大きなtargetでdraft重みを別途保持しにくい環境には魅力があるが、推論エンジンにおける木マスクの効率が性能を左右する。最新のPagedAttentionやcontinuous batchingでは候補木のKVをどう割り当てるか、他要求とどのように同時実行するか、tree maskをGPUへどう転送するかが追加課題となる。原著のbatch=1・A100結果を、RTX 4070 SuperやCPUオフロードのローカルLLMで同倍率になると断定しない。

## 限界・負の結果・未検証事項

第一に、検索はpromptと生成済み文脈のn-gramを主に使うため、短いpromptや繰返しの少ない翻訳では受理長が短くなる。原著自身が翻訳で約1.4倍程度の条件を挙げ、LongBenchでは約2.01倍へ伸びる例を示す。外部参照DBを追加する方向は今後の課題であり、現行方式の測定結果ではない。

第二に、次々トークンがtop-60に入る割合は経験的観測であり、理論保証ではない。top-k候補数を増やすほど検索・候補木が増え、K=64～128を超えると検証費用が支配的になる。さらに次々々トークンまで候補を拡張すると、60×60=3600通りの組合せが生じ得るため、著者らは採用していない。

第三に、実験は主にA100・FP16・温度0・batch1のoffline生成である。非ゼロ温度では候補順位集合が同じでも、サンプリング経路が分散して受理率が変わる。連続バッチ、複数ユーザーのprompt共有、長期運用のP99、エネルギー、モデル更新時の動作、低ビット量子化モデルの実測は主表にない。

第四に、追加draftモデル不要でも、hash索引、候補列コピー、木マスク構築、targetの複数候補検証、KV更新が必要になる。原著の1.17%検索時間は一つの実装・負荷条件での観測であり、CPU↔GPU転送や小規模GPUのメモリ競合を含む一般的な上限ではない。高速化の成否は候補受理長だけでなく検証forwardの効率に依存する。

第五に、損失なしという性質は、targetの検証と再サンプリングを正しく行うことが前提である。logit上位語をそのまま確定してよいわけではない。greedyでの出力一致と非ゼロ温度での分布一致を区別し、実装の数値精度や木マスクの誤りで出力が変わる可能性を評価する必要がある。

## 一次資料と再現性

- Tianyu Liu, Qitan Lv, Hao Li, Xing Gao, Xiao Sun, Xiaoyan Sun. *LogitSpec: Accelerating Retrieval-based Speculative Decoding via Next Next Token Speculation*. Findings of ACL 2026, pp.33070–33092, 2026. https://aclanthology.org/2026.findings-acl.1655.pdf
- 公式論文ページ: https://aclanthology.org/2026.findings-acl.1655/
- 著者公開コード: https://github.com/smart-lty/LogitSpec
- 主な照合箇所: §4.1・Fig.2（次々トークンのtop-60観測）、§4.2（n-gram検索と候補順位別保持）、§4.3（tree attention検証）、Table 1（VicunaのMAT・速度）、Table 2/3（アブレーション・検索成功率）、Fig.5（実行時間内訳）、Appendix D.2～D.3（ハードウェア・索引）、Appendix E/Table 7（Llama3.1比較）、Limitations（短いprompt・実運用未検証）。
