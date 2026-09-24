---
canonical_id: DOI:10.18653/v1/2025.naacl-long.601
doi: 10.18653/v1/2025.naacl-long.601
arxiv_categories:
  primary: null
  cross_list: []
title: 'Speculative Diffusion Decoding: Accelerating Language Generation through Diffusion'
summary: 通常の投機的復号は小型自己回帰draft modelがγ個の候補トークンを逐次生成するため、target側の並列検証は速くてもdraft段階に直列依存が残る。SpecDiffはdraft modelを離散拡散言語モデルへ置換し、候補列全体をT回の拡散stepで並列生成する。draft長γを増やしても評価回数はγではなくTに依存するため、長い候補を低depthで生成できる。候補は標準投機的復号と同じtarget確率によるaccept/rejectで検証するのでtarget modelの出力品質を保持する。CNN/DM、OpenWebText、MT-Benchで最大7.23倍の自己回帰生成比高速化、標準投機的復号比1.45〜1.75倍改善を示す。
list_summary: 自己回帰型の下書き器を離散拡散型へ置換し、候補列の生成と目標モデルによる検証の双方を並列化して投機的復号を高速化する方式。
authors:
- Jacob K. Christopher
- Brian R. Bartoldson
- Tal Ben-Nun
- Michael Cardei
- Bhavya Kailkhura
- Ferdinando Fioretto
authors_affiliations: University of Virginia; Lawrence Livermore National Laboratory
published: '2025-04-29'
publication: NAACL 2025 Long Papers
publication_type: Conference paper
publication_status: Published
lineage: 投機的復号・非自己回帰draft
topics:
- speculative デコード
- discrete diffusion
- parallel drafting
- LLM inference
importance: 投機的復号のdraft側に残る自己回帰直列性を離散拡散で除き、draft長とnetwork evaluation数を分離した。
hardware_evaluation: 2×NVIDIA A100 80GB、CUDA 12.2、FlashAttention。
hardware_details: 全主要評価を2台のA100 80GBで実施。
quality_effect: target modelの標準投機的accept/reject補正を維持するため、target分布の品質を保持する設計。評価はtemperature 0。
references:
- canonical_id: arXiv:2211.17192
  arxiv_id: '2211.17192'
- canonical_id: arXiv:2401.10774
  arxiv_id: '2401.10774'
- canonical_id: arXiv:2402.05109
  arxiv_id: '2402.05109'
- canonical_id: arXiv:2406.16858
  arxiv_id: '2406.16858'
references_checked_at: '2026-09-20'
references_source: primary-reference-section
references_total: 4
source: https://aclanthology.org/2025.naacl-long.601/
sources:
- https://aclanthology.org/2025.naacl-long.601/
- https://aclanthology.org/2025.naacl-long.601.pdf
implementation: Masked Diffusion Language Modelをdraftとして用い、既存speculative デコードのdraft部分だけを置換。初期トークンでは必要に応じ標準speculative デコードでdistribution alignmentを改善。
last_checked: '2026-09-20'
code: null
last_audited: null
audit_version: 0
---

# Speculative Diffusion Decoding: Accelerating Language Generation through Diffusion

> 自己回帰型の下書き器を離散拡散型へ置換し、候補列の生成と目標モデルによる検証の双方を並列化して投機的復号を高速化する方式。
## 書誌情報
- **著者**: Jacob K. Christopher, Brian R. Bartoldson, Tal Ben-Nun, Michael Cardei, Bhavya Kailkhura, Ferdinando Fioretto
- **著者・所属**: University of Virginia; Lawrence Livermore National Laboratory
- **公開**: NAACL 2025 Long Papers
- **種別**: Conference paper
- **対象**: speculative デコード、discrete diffusion、parallel drafting、LLM inference
- **実装**: Masked Diffusion Language Modelをdraftとして用い、既存speculative デコードのdraft部分だけを置換。初期トークンでは必要に応じ標準speculative デコードでdistribution alignmentを改善。
## 概要
通常の投機的復号は小型自己回帰draft modelがγ個の候補トークンを逐次生成するため、target側の並列検証は速くてもdraft段階に直列依存が残る。SpecDiffはdraft modelを離散拡散言語モデルへ置換し、候補列全体をT回の拡散stepで並列生成する。draft長γを増やしても評価回数はγではなくTに依存するため、長い候補を低depthで生成できる。候補は標準投機的復号と同じtarget確率によるaccept/rejectで検証するのでtarget modelの出力品質を保持する。CNN/DM、OpenWebText、MT-Benchで最大7.23倍の自己回帰生成比高速化、標準投機的復号比1.45〜1.75倍改善を示す。

投機的拡散復号（Speculative Diffusion デコード: SpecDiff）は、投機的復号の下書きモデルを自己回帰型から離散拡散言語モデルへ置換する。離散拡散器は次のγ位置を一つずつ生成せず、全位置を同じ拡散段階で並列更新するため、下書きに必要なネットワーク評価回数は候補長γではなく逆拡散段階数Tで決まる。通常Tをγより小さくできるので、10〜20語程度の長い候補を提案しても直列深さを抑えられる。下書き器が生成した各位置の確率分布は捨てずに保持し、大型目標モデルの確率分布と標準投機的samplingの受理・棄却規則で補正する。したがって離散拡散器単独の困惑度が高くても、その高速な並列生成だけを利用し、最終出力の分布は目標モデルへ整合させる。

代表結果として、OpenWebText 高速化倍率はMDLM draft、temperature 0、2×A100でautoregressive target デコードに対して7.23倍 GPT-NEO、5.38倍 GPT-2 XL。長い並列diffusion draftで最大高速化を達成。
## 問題設定
通常の自己回帰生成では、次の語を決めるには直前までに確定した語列が必要なので、出力位置を時間方向へ順番に処理するしかない。標準的な投機的復号は、小型の下書き器が複数候補を先に作り、大型の目標モデルがそれらを一括検証することで大型モデル側の呼び出し回数を減らす。しかし従来の下書き器も自己回帰型なので、候補長γを伸ばすほどγ回の逐次ネットワーク評価が必要になる。候補を短くすれば一回の検証で確定できる語数が少なく、長くすれば下書き時間が増えて高速化を失う。このため目標モデルの検証は並列化できても下書き段階に直列依存が残る。木構造や複数headによる方式は候補並列性を増やせるが、候補木の追加計算、メモリ、専用学習を要する。そこで候補列そのものを非自己回帰的に同時生成し、候補長を増やしても下書きの直列深さが比例増加しない方式が必要になる。
## 新規性
投機的拡散復号（Speculative Diffusion デコード: SpecDiff）は、投機的復号の下書きモデルを自己回帰型から離散拡散言語モデルへ置換する。離散拡散器は次のγ位置を一つずつ生成せず、全位置を同じ拡散段階で並列更新するため、下書きに必要なネットワーク評価回数は候補長γではなく逆拡散段階数Tで決まる。通常Tをγより小さくできるので、10〜20語程度の長い候補を提案しても直列深さを抑えられる。下書き器が生成した各位置の確率分布は捨てずに保持し、大型目標モデルの確率分布と標準投機的samplingの受理・棄却規則で補正する。したがって離散拡散器単独の困惑度が高くても、その高速な並列生成だけを利用し、最終出力の分布は目標モデルへ整合させる。
## 手法
### 手法のあらまし
入力は、すでに確定した接頭辞、自己回帰型の大型目標モデルMp、離散拡散型の小型下書きモデルMq、一回に提案する候補長γ、逆拡散段階数Tである。各反復の開始時に、接頭辞の直後へγ個の未確定位置を用意し、それらをmaskまたは雑音状態として初期化する。次にMqをT回呼び出す。各呼び出しではγ位置を同時に処理して各位置の語彙確率を更新し、最終段階でγ個の候補語と、それぞれを生成した下書き確率qを得る。ここまでの直列回数はγではなくTである。続いて接頭辞と候補列をまとめてMpへ一度入力し、候補γ位置とその直後の位置について目標確率pを並列計算する。検証は左端から順に行い、各候補についてpとqの比に基づく標準投機的受理試験を適用する。受理された候補は確定接頭辞へ追加し、最初の棄却位置が現れたらそれ以降の候補は捨てる。棄却位置ではp-qの正部分を正規化した補正分布から一語を目標側として生成する。γ個すべてが受理された場合もMpの次位置分布から一語を追加する。こうして少なくとも一語、しばしば複数語を確定し、その新しい接頭辞を次反復の入力として同じ処理を繰り返す。事前学習済み拡散器と目標モデルの分布が生成冒頭でずれる場合、最初の100語だけ通常の投機的復号で作って接頭辞を目標分布へ寄せ、その後SpecDiffへ切り替える。指示追従用に拡散器を目標へ調整した場合はこの初期化を省ける。最終的に出力される文章は目標モデルの受理・補正規則を通過した語だけで構成され、拡散器は高速な候補提案器として機能する。

### 離散拡散による候補列の並列生成
次のγ位置を一つずつ自己回帰生成する代わりに、全位置を未確定状態として同時に初期化する。入力は確定済み接頭辞とγ位置の雑音・mask状態である。各逆拡散段階で小型モデルMqはγ位置すべての語彙分布を一度に予測し、その予測を使って次のより低雑音な状態へ更新する。この処理をT回繰り返し、最終的な候補語列と各位置の確率qを出力する。従来の自己回帰下書きではγ語を得るため計算依存の深さが概ねγ×Dqになるのに対し、ここではT×Dqで済む。γを増やしても各段階内の位置は並列なので、Tを固定できる範囲では直列時間の増加が小さい。これが長い候補列を一度に提案できる主因であり、後段の目標モデル検証へ候補語とq分布の両方を渡す。

### 目標モデルによる一括検証と確率補正
離散拡散器が出したγ個の候補と各下書き確率qを、確定接頭辞と連結して大型目標モデルMpへまとめて入力する。Mpは自己回帰modelだが、候補語が既知なので各候補位置のlogitを一回のforwardで並列計算できる。検証では左から順に目標確率pと下書き確率qを比較し、標準投機的復号の受理確率で候補を確定する。最初に棄却された位置より後ろは条件付き文脈が変わるため破棄する。棄却位置ではp-qの正部分を正規化した補正分布から一語を生成し、全候補が通れば目標モデルの次位置分布から追加の一語を生成する。この補正により、拡散器の確率が目標と完全一致していなくても最終出力を目標モデルの分布へ戻せる。したがって下書き器には最終品質ではなく速度と十分な受理率を要求すればよい。

### 候補長と拡散段階数の分離
自己回帰下書きでは候補長γを増やすと下書き器の呼び出し回数も増えるため、速度はγの選択に非常に敏感である。SpecDiffではγ位置を同時更新するため、γを10から20程度へ変えても各逆拡散段階の並列幅が変わるだけで直列段階数はTのままである。一方、Tを増やすと拡散器が候補分布をより丁寧に復元でき、目標モデルに受理される割合は上がるが、Mqのforward回数も増える。したがって設計上はγを比較的長くして一回に進める最大語数を確保し、Tを『候補品質による受理語数』と『下書き計算時間』の交換として調整する。実験でもγ=10〜20は広く機能し、速度はγよりTへ敏感だった。これにより従来のγ調整問題を、より直接的な拡散品質・計算量の調整へ置き換える。

### 生成冒頭の分布整合と指示調整
異なるarchitectureと学習データを持つ事前学習済み拡散器は、接頭辞が短い生成冒頭では目標モデルの分布とずれ、候補受理率が低くなりやすい。未調整条件では最初の100語を標準投機的復号で生成し、目標モデルらしい十分な接頭辞が形成されてからSpecDiffへ切り替える。この接頭辞を条件として与えると拡散器の候補も目標分布へ近づき受理率が上がる。Vicuna 33B評価ではLlama系tokenizerへ合わせたMDLMを用意し、teacher-student型の指示調整で目標の出力分布へ近づけたため、この冒頭初期化を不要にした。つまり運用時には『既存拡散器＋短い標準初期化』と『target向け調整済み拡散器』の二経路を選べる。

### 全体のデータ／制御の流れ
既存の投機的復号実装に対して、候補生成部だけを離散拡散器へ置換し、目標モデルの並列検証、受理・棄却、補正samplingはそのまま再利用する。実験は2台のNVIDIA A100 80GBで行い、CUDA 12.2とFlashAttentionを全比較条件へ適用した。
## 評価条件
- **ハードウェア**: 2×NVIDIA A100 80GB。
- **ソフトウェア**: CUDA 12.2、FlashAttention。Masked Diffusion Language Modelをdraftとして使用。
- **比較対象**: autoregressive デコード、standard speculative デコード、EAGLE、EAGLE-2
CNN/DailyMail要約、OpenWebText生成、MT-Bench、およびSpecBenchで評価。CNN/DMとOpenWebTextは1024 トークンをtemperature 0で生成し、targetにGPT-2 XL 1.5B/GPT-NEO 2.7B、draftにMDLM 110Mを使用。標準投機的復号はGPT-2 86M draft。MT-BenchではVicuna 33B target、MDLM 141M draftを用いEAGLE/EAGLE-2と比較。walltime 高速化倍率、acceptance rate、FLOPs/draft、メモリ/depthを測定し、γとT、標準投機的初期化の有無もablation。
自己回帰target modelの出力品質を保った投機的復号高速化。主に長いgreedy generationを対象とし、temperature>0の確率的生成は未評価。
## 主要結果
CNN/DMではGPT-2 XL targetで4.80倍、GPT-NEOで6.63倍の自己回帰生成比高速化を達成し、標準投機的復号の3.58倍/5.45倍を上回った。OpenWebTextでは5.38倍/7.23倍で、標準投機的復号3.66倍/4.12倍に対して最大約1.75倍改善した。MT-BenchのVicuna 33Bでは2.61倍で、EAGLE 2.41倍、EAGLE-2 2.60倍と同等以上のoverall 高速化倍率を、EAGLE-2より33%以上少ないdraft FLOPsで得た。

- OpenWebText 高速化倍率 / 7.23倍 GPT-NEO、5.38倍 GPT-2 XL (比較対象: autoregressive target デコード; 条件: MDLM draft、temperature 0、2×A100) — 長い並列diffusion draftで最大高速化を達成。

- standard speculative デコード比 / 最大約1.75倍、範囲1.45〜1.75倍 (比較対象: GPT-2 autoregressive drafter; 条件: CNN/DM/OpenWebText) — draft側の直列生成を並列化する利得を確認。

- CNN/DM 高速化倍率 / 4.80倍 GPT-2 XL、6.63倍 GPT-NEO (比較対象: autoregressive デコード; 条件: 1024 トークン generation) — 要約でも標準投機的復号を上回る。

- MT-Bench overall 高速化倍率 / 2.61倍 (比較対象: EAGLE 2.41倍、EAGLE-2 2.60倍; 条件: Vicuna 33B target、MDLM 141M) — SOTA級速度をより小さいdiffusion draftで達成。

- draft FLOPs / 5.53×10^10 FLOPs/draft (比較対象: EAGLE-2 8.35×10^10; 条件: MT-Bench Vicuna 33B) — EAGLE-2より33%以上少ないdraft計算で同等overall 高速化倍率。

### 負の結果・境界条件
- diffusion drafterの確率はtargetと十分calibrateされず、特にtemperature>0ではtop-1へ過度に集中するため確率的samplingの有効性は未検証。利用可能なdiffusion modelのtokenizerがGPT-2系に偏り、Vicuna用には別tokenizerで新規学習が必要だった。短い生成では並列化利得が小さく、fine-tuningなしでは初期acceptance率が低い。性能はγより拡散step数Tの調整に敏感。

### 結果の読み方
投機的復号の速度上限はtarget検証だけでなくdraftの直列depthにも依存する。diffusion draftでは候補長γとnetwork evaluation数Tを分離でき、より長い候補を低depthで提案できるため、acceptance率が標準draftより少し低くてもwalltimeでは速くなる。
## 品質への影響
標準speculative samplingのaccept/reject補正を維持するためtarget modelのgreedy出力品質を保持する。実験はtemperature 0であり、多様な確率的samplingでの同等性は今後の課題。
## 既存研究との差
標準speculative デコードは小型自己回帰drafterがγ トークンを逐次生成するためdraft depthがγに比例する。SpecDiffは離散拡散でγ位置を同時生成しdepthをTへ置換する。Medusa/Hydra/EAGLE系はtarget由来の追加headやtreeを使い、target architectureとの強い結合や追加trainingを伴う。SpecDiffは異種architectureの独立diffusion drafterを利用でき、既存targetの検証規則を変更しない。tree方式より候補長拡大時のメモリ/FLOPs増加を抑えやすい。
## 限界
離散拡散draftと自己回帰targetの確率分布calibrationが弱く、temperature>0ではdiffusion側がtop-1へ過信しやすい。主要実験はtemperature 0なのでstochastic samplingは未実証。利用可能な離散拡散modelはtokenizer互換性が限られ、異なるtarget用には新規pretraining/fine-tuningが必要になり得る。短い生成では長い候補列を並列化する利得が小さく、targetとのalignment不足も相対的に大きい。最適速度は拡散step Tに敏感で調整が必要。
## 実装状態
2×A100上でMDLM drafterと複数targetを組み合わせて実測。既存speculative デコード codeのdraft生成を置換する形で実装可能。論文ではmodelをHuggingFace公開予定と記載するが、本文から独立code repository URLは確認できない。
## 研究上の位置づけ
投機的復号の研究を『targetの並列検証』から『draft生成自体の並列化』へ拡張する方式。非自己回帰modelの品質不足をそのまま最終生成へ使わず、target modelのaccept/reject補正の内側に閉じ込めることで、diffusionの速度と自己回帰LLMの品質を分業させる。将来diffusion modelのcalibrationと速度が改善すると、draft長をさらに伸ばして利得を拡大できる。
## 一次資料
- https://aclanthology.org/2025.naacl-long.601/
- https://aclanthology.org/2025.naacl-long.601.pdf
