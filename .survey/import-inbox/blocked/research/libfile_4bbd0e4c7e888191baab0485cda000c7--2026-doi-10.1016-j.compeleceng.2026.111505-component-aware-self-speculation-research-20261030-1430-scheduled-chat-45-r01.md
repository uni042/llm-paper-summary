---
canonical_id: "DOI:10.1016/j.compeleceng.2026.111505"
arxiv_id: "2605.01106"
arxiv_categories:
  primary: "cs.CL"
  cross_list: ["cs.AI"]
title: "Component-aware self-speculative decoding for hybrid language models: An architectural viability study"
summary: "ハイブリッドLLMのSSM/linear-attention成分だけを内部draftとして用いる自己投機復号を検証。Falcon-H1の並列構成では2-token draftの全採択率0.680、Qwen3.5の逐次構成では0.038と18倍差。だがPython prototypeは全条件で実測1倍未満、Falconでも理論0.92倍・実測0.342倍で高速化を実証しない。モデル成分の構成方式と注意削除時のPPL悪化が適用可能性を左右する。"
list_summary: "並列SSM+注意機構のFalcon-H1では内部SSM ドラフトの採択率が高いが、逐次Qwen3.5ではほぼ失敗。現行prototypeは全条件で減速。"
authors:
  - "Hector Borobia"
  - "Elies Seguí-Mas"
  - "Guillermina Tormo-Carbó"
published: "2026-05-01"
publication: "Computers & Electrical Engineering, DOI:10.1016/j.compeleceng.2026.111505（関連正式版）。本文数値の照合対象はarXiv:2605.01106v1"
publication_type: "journal / preprint-version analysis"
publication_status: "published"
source: "https://arxiv.org/pdf/2605.01106"
sources:
  - "https://arxiv.org/pdf/2605.01106"
  - "https://arxiv.org/abs/2605.01106"
  - "https://doi.org/10.1016/j.compeleceng.2026.111505"
implementation: "Falcon-H1では各層のattention出力をforward hookでゼロ化、Qwen3.5ではattention層をidentity skipし、残るSSM/linear-attention成分を内部draftにする。標準rejection samplingで検証。Python hooksと非共有KVを使う研究prototype。"
code: null
last_checked: "2026-10-30"
worker_id: "scheduled-chat-45"
worker_completed_at: "2026-10-30T14:26:00+09:00"
worker_run_key: "20261030-1408-scheduled-chat-45/r01"
reference_main_sha: "8a4c43d4d90ff181c263ce52251dd48734928dda"
quality_self_review_passed: true
quality_self_review_version: "PAPER-QUALITY-GUIDE-2026-10-07"
research_job_source: "WORKLIST-45.md rank 46"
version_scope: "arXiv:2605.01106v1; journal full-text differences unverified"
last_audited: null
audit_version: 0
---
# Component-aware self-speculative decoding：ハイブリッドLLMの内部成分をdraftに使える条件

## 概要

投機的復号は、軽い下書きモデルが複数トークンを先読みし、重い対象モデルがまとめて検証することで、対象の出力分布を変えずに生成を速める。従来の自己投機はTransformerの一部層をスキップしたり早期出口したりするが、Mamba/SSMや線形 注意機構を混ぜたハイブリッドLLMでは、そもそも**別の計算成分をモデル内部から切り出す**という選択肢がある。外部drafterを保存・学習しなくても、SSM側だけで候補を作れるのではないか、というのが本論文の問いである。

著者らはFalcon-H1とQwen3.5を比較し、成分が**各層内で並列に加算される**場合と、**異なる種類の層が逐次的に交互配置される**場合で結果が大きく変わることを示した。Falcon-H1のSSM-only ドラフトは比較的対象に近い分布を出す一方、Qwen3.5の線形-only ドラフトは注意機構層を全削除すると情報の流れが破綻する。重要なのは、採択率が高いことと実際の推論が速いことは別だという点である。原著のPython prototypeは全条件で**実測速度が通常のautoregressive 復号より遅い**。理論上の高速化可能性と実装実測を分離する必要がある。

## アーキテクチャと手法

### 並列ハイブリッドと逐次ハイブリッド

Falcon-H1の各層は、同じ隠れ状態をMamba-2のSSM成分とsoftmax 注意機構成分に並列投入し、その出力を加算する。通常の層出力は`h_l = f_SSM(h_{l-1}) + f_attn(h_{l-1})`と近似できる。ここで注意機構出力をゼロにしても、SSM成分が各層を通じて連続的な計算経路を形成する。ドラフト時はSSMのみを計算し、対象検証時は元の両成分を計算する。Falcon-H1-0.5Bでは36層、3Bでは32層のSSMと注意機構の並列ペアを用いる。

Qwen3.5-0.8Bは24層のうち18層がGated DeltaNet型線形 注意機構、6層がsoftmax 注意機構という**逐次インターリーブ**である。注意機構層を識別子としてスキップすると、線形層は学習時とは異なる隠れ状態を受け取り、途中の大域情報統合が失われる。したがって線形-only経路が完全な言語モデルとして機能するとは限らない。Qwen2.5-0.5Bは純Transformerの比較対象で、24層の約33%をLayerSkipする。

### 内部draft抽出と分布保存検証

実装は順伝播 hookで、Falcon-H1では注意機構成分の出力をゼロ化、Qwen3.5では注意機構層の計算をスキップする。追加の学習・別重みは不要で、元のembedding、正規化、LM ヘッドを共有する。各ラウンドでは内部ドラフトがk個のトークンを逐次生成し、完全な対象がその候補列をまとめて検証する。サンプリング時には`min(1, p_target(token)/p_draft(token))`の確率で受理し、棄却位置では両分布の正の差分から補正トークンを引く標準のrejection samplingを使う。この規則が正しく実装されれば、厳密演算では対象分布を保持する。

greedy 復号ではドラフトと対象のargmaxが一致したときに受理する。論文の主指標`α(k)`は、kトークンのドラフト列が**全トークン採択された割合**であり、単一トークン平均採択率や一回の検証で生成できる期待トークン数と同じではない。`α(k)`がkとともに下がるのは、全ての位置で一致する必要があるためである。

### 理論的な速度見積もり

論文の式(1)は、kトークンドラフトの期待生成トークン数を`(1−α^(k+1))/(1−α)`で近似し、検証1回とドラフト k回の合計費用で割って理論速度倍率を求める。Falcon-H1-0.5BのSSM-only ドラフトは元モデルのFLOPsの**78.4%**、Qwen3.5-0.8Bの線形-onlyは**77.3%**を使う。追加パラメータがゼロという意味で「zero-コスト internal ドラフト」と呼んでいるが、**ドラフト計算が無料という意味ではない**。この高いFLOP比率は採択率が高くても速度倍率が1未満になり得る原因である。

SSMはrecurrent 状態を使い、過去系列長に対するKV参照が少ないので、長文ではFLOP比だけでは表せないメモリ帯域上の利点があり得る。ただし原著のprototypeは共有KV、fused カーネル、バッチ検証の最適化を実装していないため、長文での実機高速化を検証したものではない。

## 評価条件

| 項目 | 原著の設定 |
|---|---|
| モデル | Falcon-H1-0.5B-Base（521M）、Falcon-H1-3B-Base（3.15B）、Qwen3.5-0.8B-Base（752M）、Qwen2.5-0.5B（494M） |
| モデルの状態 | instruction-tunedではないbase モデル。Falconは並列、Qwen3.5は逐次、Qwen2.5は純Transformer |
| データ | WikiText-2 検証 200 prompts/条件（最大512 トークン）、MMLU、GSM8K、Alpaca形式プロンプト |
| ドラフト長 | k=2,4,8。greedy T=0.0、サンプリングT=0.6 |
| 指標 | 全トークン採択率α(k)、top-100 logitsのtotal variation、top-1一致、実測実時間速度倍率、PPL 構成要素除去 |
| 統計 | 採択率の95% bootstrap CI、10,000 resamples |
| ハードウェア | NVIDIA L4 24GB 1枚、PyTorch 2.x、HuggingFace Transformers。GPU-side timingにCUDA Event |
| 実装 | Python 順伝播 hook、ドラフトとverifyの逐次順伝播、KV キャッシュ非共有 |

## 主要評価結果

| 出典 | Falcon-H1-0.5B | Qwen3.5-0.8B | 読み取り |
|---|---:|---:|---|
| Table 2、total variation | 0.302 | 0.803 | 低いほどドラフト分布が対象に近い。Qwen3.5は大きく乖離 |
| Table 2、top-1一致率 | 0.658 | 0.203 | 成分を切り出した時点の分布品質に差がある |
| Table 3、greedy k=2 | **0.680** | **0.038** | 全採択率は約18倍差。Qwen2.5 LayerSkipは0.520 |
| Table 3、greedy k=4 | 0.370 | 0.019 | ドラフト長が増えると両者とも全採択率は低下 |
| Table 3、greedy k=8 | 0.186 | 0.009 | k=8ではQwen3.5の採択はほぼ起きない |
| Table 4、sampling T=0.6, k=2 | 0.560 | 0.073 | samplingでもアーキテクチャ差は残る |
| Table 5、k=4 GSM8K | 0.495 | 0.001 | 数学系プロンプトでFalconは比較的有利、Qwen3.5は失敗 |
| Table 5、k=4 MMLU | 0.208 | 0.013 | Falconも事実想起では採択率が低い |
| Table 6、注意機構削除時PPL比 | 3.15倍 | 81.96倍 | 注意成分への依存度と採択率の関係を示す |
| Table 7、**実測速度倍率 k=2** | **0.342倍** | **0.026倍** | いずれも通常デコードより遅い。高速化実証ではない |
| Table 7、実測速度倍率 k=4 | 0.311倍 | 0.016倍 | k増でPython実装のオーバーヘッドが増える |

Falcon-H1-3Bのgreedy全採択率はk=2で0.590、k=4で0.351、k=8で0.186で、0.5Bと近い。ただし0.5Bのk=2は0.680なので「完全に同じ」ではない。95% CIが重なるk=4/8ではモデル規模の増大だけでは採択率を改善しないという傾向を示すが、**他のモデル系列や10B以上まで一般化できる厳密なスケール不変則ではない**。

### 実測速度の負の結果を隠さない

Table 7では、Qwen2.5 LayerSkipもk=2で0.496倍、Falcon-H1-3Bは0.148倍と、**すべてのモデル・ドラフト長で速度倍率が1.0未満**だった。Falcon-H1-0.5Bのk=2について、採択率0.680とFLOP比0.784から式(1)が予測する理論速度倍率は**0.92倍**であり、理想的にPythonオーバーヘッドを取り除いても、この条件では高速化を保証しない。実測は0.342倍で、理論値からさらに2.7倍の乖離がある。著者はPython hook、別々の順伝播、KV非共有が主因と説明するが、最適化後の実時間倍率を測っていない。

Qwen3.5での代替戦略を比べたTable 8では、線形-onlyのk=4全採択率0.019に対し、**LayerSkip 33%が0.233**、早期出口 50%は0.000だった。逐次ハイブリッドでは特定成分を丸ごと抜くより、注意機構/線形の交互配置をある程度残すLayerSkipの方が適する。これは「Qwen3.5では投機復号が不可能」という結論ではなく、**この内部成分切り出し戦略が不適切**という結論である。

### 分布保存の確認と数値上の留保

Table 9のgreedy出力一致率はFalcon-H1 96%、Qwen3.5 96%、Qwen2.5 90%で100%ではない。論文はbf16で上位logit差が小さい場合のargmax反転を原因と説明し、厳密演算におけるrejection samplingの分布保存とは区別する。実装の一致率90〜96%を「出力分布の完全一致を実験で証明した」と表現すべきではない。

また、Table 6の「PPL比と採択率の完全な逆相関」は実質的にFalcon-H1とQwen3.5の2モデル間の比較である。PPL比が5未満なら有望、20超なら不適という実務上の目安を著者は提案するが、独立モデル群で校正された汎用分類器ではない。

## 限界・適用可能性

本論文はアーキテクチャの**適合性診断**として有用だが、完成した高速推論エンジンではない。GPU上での実測速度はすべて低下し、外部drafterを持たないことによるメモリ節約と、実際のトークン/sの改善を混同できない。SSM recurrent 状態と注意機構 KVの状態同期、accept/reject時の状態 rollback、共有KV、fused カーネル、CUDA グラフ、batching、長文でのメモリ 帯域優位を本番レベルで統合する必要がある。

評価はbase モデルの小型構成中心で、instruction-tuned Qwen3.5やFalcon-H1の大規模MoE版、Jamba、Sambaなどの別系列へ直接外挿できない。プロンプトはWikiText-2 200件/条件を主軸とし、実サーバーの混合長・混合バッチ・arrival rate・tail 遅延を測っていない。採択率もMMLUとGSM8Kで大きく変わるため、固定kが最適とは限らない。

特に、**正式出版版とarXiv v1の版差**には留保が必要である。DOI:10.1016/j.compeleceng.2026.111505の関連正式版が確認できるが、今回詳細な表・数値を直接照合した一次本文はarXiv:2605.01106v1である。正式版の全文表を取得できなかったため、正式版に同じ数値がすべて残っているとは断定しない。サーベイの後続監査ではDOI正式版を入手し、評価表・限界の差分を確認する必要がある。

サーベイ上は、投機的復号における「**内部ドラフトの成立条件をアーキテクチャで判定する研究**」として、LayerSkip/CLaSp/SWIFTと、SSM/線形 注意機構のハイブリッド設計の交差領域に配置する。高い採択率が必ずしも高速化を意味しないという負の結果は、ドラフトモデル選択の評価基準として特に重要である。

## 一次資料・書誌

- [arXiv:2605.01106v1 PDF（29ページ）](https://arxiv.org/pdf/2605.01106)：§3〜5、Table 1〜9、rejection sampling、理論FLOP比、実測負の結果を確認。
- [arXiv公式書誌](https://arxiv.org/abs/2605.01106)：初稿2026-05-01、著者3名、cs.CL / cs.AI。
- [関連正式版DOI](https://doi.org/10.1016/j.compeleceng.2026.111505)：Computers & Electrical Engineeringの正式版。今回の数値出典はarXiv v1であり正式版の表との同一性は未検証。
