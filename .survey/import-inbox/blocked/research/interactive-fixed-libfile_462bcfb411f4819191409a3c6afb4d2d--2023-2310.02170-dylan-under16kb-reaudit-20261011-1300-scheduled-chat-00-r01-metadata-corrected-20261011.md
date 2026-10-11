---
canonical_id: arXiv:2310.02170
arxiv_id: '2310.02170'
arxiv_categories:
  primary: cs.CL
  cross_list:
- cs.AI
- cs.MA
title: A Dynamic LLM-Powered Agent Network for Task-Oriented Agent Collaboration
summary: 動的な大規模言語モデルのエージェント協調を時間展開グラフで表し、予備協調からの寄与度伝播によるチーム選抜と、実行中のランカーによる再編成・早期終了を組み合わせる。HumanEval、WebShop、MMLU、MATHで正答品質とAPI呼出し数の交換条件を測定した。
list_summary: 予備協調の寄与度伝播で役割を選び、実行中も低寄与エージェントを除外する動的協調方式。品質向上の対価をAPI呼出し数で評価し、GPU遅延改善とは区別する。
authors:
- Zijun Liu
- Yanzhe Zhang
- Peng Li
- Yang Liu
- Diyi Yang
published: '2023-10-03'
publication: COLM 2024
publication_type: 査読付き国際会議
publication_status: COLM 2024掲載版（arXiv v2は2024-11-15）
source: https://openreview.net/pdf?id=XII0Wp1XA9
sources:
- https://openreview.net/forum?id=XII0Wp1XA9
- https://openreview.net/pdf?id=XII0Wp1XA9
- https://arxiv.org/abs/2310.02170
- https://www.scribd.com/document/856503167/LLM-Research-Paper
code: https://github.com/SALT-NLP/DyLAN
implementation: 著者公式コードはSALT-NLP/DyLAN。GPUカーネルではなく、LLM呼出し、順位付け、エージェント間メッセージ伝播を実装する。
last_checked: '2026-10-11'
worker_id: scheduled-chat-00
worker_completed_at: '2026-10-11T13:06:06+09:00'
worker_kind: scheduled_chat
scheduled_slot: '00'
worker_run_key: 20261011-1300-scheduled-chat-00/r01
reference_main_sha: f7f05c987ec5bfb49c550845fd23884cb2d9c89a
under16kb_reaudit_target_path: papers/inference/99-other-inference-systems/2023-2310.02170-a-dynamic-llm-powered-agent-network-for-task-oriented-agent-collaboratio.md
under16kb_reaudit_source_git_blob_sha: ab802dd006e0a9668e804e3ecc66a767f0cebe65
under16kb_reaudit_version: 2026-10-07-v1
under16kb_reaudit_passed: true
quality_body_chars: 6314
quality_method_chars: 1603
quality_eval_chars: 2920
quality_limitation_chars: 324
quality_self_review_passed: true
quality_self_review_version: 2026-10-07-v1
references:
- canonical_id: arXiv:2305.11860
  arxiv_id: '2305.11860'
- canonical_id: OpenReview:FQepisCUWu
  openreview_id: FQepisCUWu
- canonical_id: OpenReview:ktrw68Cmu9c
  openreview_id: ktrw68Cmu9c
- canonical_id: arXiv:2309.17288
  arxiv_id: '2309.17288'
- canonical_id: arXiv:2107.03374
  arxiv_id: '2107.03374'
- canonical_id: OpenReview:EHg5GDnyq1
  openreview_id: EHg5GDnyq1
- canonical_id: arXiv:2312.14878
  arxiv_id: '2312.14878'
- canonical_id: arXiv:2304.07590
  arxiv_id: '2304.07590'
- canonical_id: arXiv:2305.14325
  arxiv_id: '2305.14325'
- canonical_id: arXiv:2304.12998
  arxiv_id: '2304.12998'
- canonical_id: OpenReview:VtmBAGCN7o
  openreview_id: VtmBAGCN7o
- canonical_id: arXiv:2309.13193
  arxiv_id: '2309.13193'
- canonical_id: OpenReview:3IyL2XWDkG
  openreview_id: 3IyL2XWDkG
- canonical_id: arXiv:2305.19118
  arxiv_id: '2305.19118'
- canonical_id: OpenReview:zAdUB0aCTQ
  openreview_id: zAdUB0aCTQ
- canonical_id: arXiv:2308.05960
  arxiv_id: '2308.05960'
- canonical_id: OpenReview:HtqnVSCj3q
  openreview_id: HtqnVSCj3q
- canonical_id: arXiv:2309.08172
  arxiv_id: '2309.08172'
- canonical_id: arXiv:2308.10435
  arxiv_id: '2308.10435'
- canonical_id: OpenReview:mqVgBbNCm9
  openreview_id: mqVgBbNCm9
- canonical_id: arXiv:2303.08774
  arxiv_id: '2303.08774'
- canonical_id: arXiv:2307.07924
  arxiv_id: '2307.07924'
- canonical_id: arXiv:2312.17025
  arxiv_id: '2312.17025'
- canonical_id: arXiv:2401.05268
  arxiv_id: '2401.05268'
- canonical_id: arXiv:2306.17563
  arxiv_id: '2306.17563'
- canonical_id: arXiv:2009.10297
  arxiv_id: '2009.10297'
- canonical_id: OpenReview:GrkgKtOjaH
  openreview_id: GrkgKtOjaH
- canonical_id: OpenReview:vAElhFcKW6
  openreview_id: vAElhFcKW6
- canonical_id: arXiv:2401.12954
  arxiv_id: '2401.12954'
- canonical_id: OpenReview:pAMNKGwja6
  openreview_id: pAMNKGwja6
- canonical_id: OpenReview:1PL1NIMMrw
  openreview_id: 1PL1NIMMrw
- canonical_id: arXiv:2307.05300
  arxiv_id: '2307.05300'
- canonical_id: OpenReview:_VjQlMeSB_J
  openreview_id: _VjQlMeSB_J
- canonical_id: arXiv:2308.08155
  arxiv_id: '2308.08155'
- canonical_id: DOI:10.18653/v1/2023.findings-emnlp.508
  doi: 10.18653/v1/2023.findings-emnlp.508
- canonical_id: OpenReview:gjeQKFxFpZ
  openreview_id: gjeQKFxFpZ
- canonical_id: OpenReview:WE_vluYUL-X
  openreview_id: WE_vluYUL-X
- canonical_id: DOI:10.18653/v1/2023.emnlp-main.936
  doi: 10.18653/v1/2023.emnlp-main.936
- canonical_id: arXiv:2310.02124
  arxiv_id: '2310.02124'
- canonical_id: arXiv:2308.01862
  arxiv_id: '2308.01862'
- canonical_id: arXiv:2308.04371
  arxiv_id: '2308.04371'
- canonical_id: arXiv:2304.09797
  arxiv_id: '2304.09797'
- canonical_id: arXiv:2310.04406
  arxiv_id: '2310.04406'
- canonical_id: arXiv:2308.05481
  arxiv_id: '2308.05481'
- canonical_id: arXiv:2305.17144
  arxiv_id: '2305.17144'
- canonical_id: arXiv:2402.16823
  arxiv_id: '2402.16823'
references_total: 46
references_checked_at: '2026-10-07'
references_source: 修復元の構造化参考文献46件を識別子として継承。全引用論文の本文再検証を意味しない。
---

# A Dynamic LLM-Powered Agent Network for Task-Oriented Agent Collaboration

## 一文解説

動的エージェント協調網（DyLAN）は、複数の大規模言語モデル（LLM）を単純に増やすのではなく、予備実行から参加者の寄与を推定してチームを選び、解答中にも参加者を再編成することで、正答品質と呼出し費用の交換条件を改善する方式である。

## 概要

複数のLLMエージェントを協調させる従来の設計では、参加人数、役割、通信相手、反復回数を固定することが多い。ところが、数学とコード生成では必要な役割が異なり、途中で誤った説明を繰り返すエージェントが残ると、余分な推論呼出しだけでなく回答品質の低下も起きる。DyLANは時間展開型の順伝播網（Temporal Feed-Forward Network; T-FFN）として協調の経路を表し、予備試行からエージェント重要度（Agent Importance Score）を推定する。正式実行では選抜した参加者が各時点で回答を交換し、順位付け器が低評価の枝を外す。回答一致による早期終了も組み合わせる。

査読付きCOLM 2024掲載版の表2～6では、HumanEvalの単一実行73.2から82.9への正解率向上、MMLUの66.4から70.5への改善、WebShopの報酬50.6から68.3への改善を示す。一方、HumanEvalのAPI呼出しは単一実行の1回から16.85回へ増えるため、単一実行より低費用という結果ではない。比較対象となる多段方式より少ない呼出しで品質を得ることが中心的な主張であり、GPUのカーネル実行時間を短縮する研究とは区別する。

## 背景・問題設定

固定チームの討論では、初期の参加者を最後まで残すため、特定課題に不適切な役割や誤答が次段へ伝わる。固定した通信構造を持つ複数エージェントの計算は、回答が一致していても所定のラウンド数だけ実行される場合がある。したがって、誰を参加させるか、各段階で誰を残すか、いつ終了するかという三つの選択が重要になる。

ただし、エージェントの寄与は個別の正答率だけでは決まらない。ある参加者が直接最終回答を出さなくても、その説明が次の参加者の誤り訂正に役立つことがある。DyLANは各時点のエージェントを別ノードとする時間展開グラフを用いて、間接寄与を後ろから伝播させる。初期の役割説明だけで選ぶ方法より、実際の協調過程に基づいて選抜できることを狙う。

この設計では、予備試行に追加のAPI費用が発生し、重要度の推定には別のLLMによる相互評価が必要となる。さらに、最終回答の一致が必ず正しさを保証するわけではない。論文が報告する効率指標は主にAPI呼出し回数であり、料金、トークン長、実行待ち時間、並列化した際の壁時計時間を直接測った値ではない。

## 手法

### 1. 時間展開順伝播網による協調の表現

エージェント集合を $A=\{a_1,\ldots,a_N\}$、時刻 $t$ のノード集合を $V_t$、時刻間の通信辺を $E_{t-1,t}$ とする。各ノードはその時刻における一つのエージェントを表し、同じエージェントでも時刻が違えば別ノードである。通信は原則として隣接時刻の間に向かう。前時刻の回答集合を受け取ったノードは、質問と回答をプロンプトへ組み込み、修正案、批評、コード、ツール実行結果などを次時刻へ渡す。入力は質問と前段のメッセージ、出力は当該ノードの新しいメッセージである。

この表現により、固定討論、直列的な自己修正、並列候補生成などを同じグラフとして扱える。重要なのは、計算途中で辺集合を変えることができる点である。すべての参加者を次時刻へ接続するのではなく、残す参加者だけを次段へ結ぶことで、無駄な回答生成と誤答の伝播を抑える。グラフはモデルの重みを更新するニューラルネットワークではなく、LLM呼出しを編成する実行時の論理構造である。

### 2. 実行中の順位付けとチーム再編成

各時刻の参加者が出した回答を、追加のLLM順位付け器（LLM Ranker）が比較する。順位が高いエージェントだけを次時刻の参加者集合へ残し、残したノードから次時刻のノードへの通信辺を作る。入力は同じ質問に対する各回答、処理は順位付け、出力は次段に残す参加者と接続辺である。これは役割を固定して全員を反復させる方式と異なり、誤った中間回答の影響を局所的に切ることを意図する。

順位付けは無料ではない。比較器の追加呼出しが発生し、評価器が誤った回答を高く順位付けする場合は有用な枝を捨てる。論文付録C.5では、一覧順位付けがMMLU正答率70.5・4.39呼出しなのに対し、対比較方式は70.1～70.3程度の正答率で11.40～19.55呼出しを要する。精度差が小さくても、順位付け方法による呼出し費用差は大きい。

### 3. 早期終了の条件

一時刻の参加者のうち、回答が一致する者が3分の2を超えたとき、または最大時刻へ達したときに実行を終える。回答の一致は誤りが少ないことの代理として用いられるが、全員が同じ誤答に合意する可能性もある。コード生成のような自由記述課題では、意味が同じでも表記が異なるため一致判定が難しい。論文はBLEUの閾値0.9を使い、形式の異なる正しいコードが一致と見なされず、早期終了の効果が小さくなることを報告する。

早期終了は主として呼出し数を減らす機構である。参加者の再編成は品質の改善にも寄与するが、終了判定は必ずしも精度を改善するとは限らない。両者を一つの「効率化」機能とみなさず、どの費用と品質に効くかを分けて評価する必要がある。

### 4. 予備協調による重要度の後方伝播

正式な質問解決に先立ち、候補チームで予備的な協調を実行する。各ノードは前時刻の参加者の回答を評価し、その評点を辺の重み $w_{t-1,i,j}$ として記録する。最後の時刻から始めて、次時刻のノードの重要度 $I_{t,j}$ を評点で重み付けし、$I_{t-1,i}=\sum_j I_{t,j}w_{t-1,i,j}$ により一段前へ戻す。各エージェントの全時刻にわたる重要度を合計して、候補の中から上位の参加者を選ぶ。

この後方伝播はモデルの勾配計算ではない。予備試行で生成された回答の相互評価を使い、最終段へつながる間接的な貢献を割り当てる処理である。選抜結果を次の本番実行へ渡すことで、課題別に必要な役割を絞り込める。一方、予備試行のコストは発生し、重要度はLLM評価の偏りや候補役割の分布に影響される。候補の中に課題へ適したエージェントが一人もいない場合は、選抜しても大きな利得が得られない。

## 評価

### 条件・指標と比較対象

| 対象 | 評価条件 | 主指標 | 注意点 |
|---|---|---|---|
| HumanEval | 164問のコード生成、単一実行、CodeT、Reflexion、LATS、CAMEL、AgentVerse等 | Pass@1、API呼出し数 | コード生成器とコード検査器を使う構成 |
| WebShop | テスト集合から50環境、ReAct、Reflexion、LATS、BOLAA等 | 報酬、成功率、API呼出し数 | 対話操作の費用はコード生成と異なる |
| MMLU | 57科目、テスト問題を5分の1に標本抽出 | 正答率、API呼出し数 | 科目ごとに役割を選抜 |
| MATH | 5,000問、標準・複雑な思考連鎖の別条件 | 正答率、API呼出し数 | 比較はプロンプト条件ごとに行う |
| 構成要素除去 | 早期終了と再編成を別々に無効化 | 品質、呼出し数 | 機構ごとの寄与を分離 |

主実験の基盤モデルはGPT-3.5系であり、一部コード生成ではGPT-4-0613も追加検証する。表のAPI呼出し数は主に予備試行後の「課題解決」段階を対象とし、チーム最適化の準備費用を全面的に加算した総費用ではない。したがって、本番段階での呼出し削減を単発要求の総コスト削減へ直結させてはならない。性能は主に正答品質と呼出し数の比較であり、GPU推論速度や初回トークン遅延は測定対象ではない。

### 主要結果：品質と費用の両面

| 条件 | 比較基準 | DyLAN | 解釈 |
|---|---|---|---|
| HumanEval Pass@1 | 単一実行73.2・1呼出し、LATS 81.1・48呼出し | 82.9・16.85呼出し | 単一実行より呼出しは増えるが、多段LATSより少ない呼出しで高品質 |
| WebShop報酬・成功率 | 直接実行50.6・28.0%、LATS 64.5・38.0% | 68.3・42.0%、24.85呼出し | LATSの400呼出し超より少ないが、直接実行の14.52より多い |
| MMLU平均正答率 | 単一実行66.4・1呼出し、LLM Debate 69.3・12呼出し | 70.5・4.39呼出し | 固定討論より品質・呼出し数が有利 |
| MATH標準思考連鎖 | 単一実行31.6・1呼出し、LLM Debate 32.4・8呼出し | 35.7・7.15呼出し | 単一実行との差は+4.1ポイント |
| MATH複雑思考連鎖 | 単一実行34.1・1呼出し、PHP 36.5・3.67呼出し | 37.6・6.21呼出し | 精度は上回るがPHPより呼出しは多い |

HumanEvalの82.9と単一実行73.2の差は9.7ポイントであり、呼出し数は1回から16.85回へ増えている。DyLANが「単一LLMより安い」と読むのは誤りである。一方、LATSの81.1・48回と比べると品質と呼出し数の双方が改善している。MMLUでも70.5対69.3という1.2ポイント差を得ながら、呼出し数は4.39対12であり、複数エージェント方式同士の比較としては効率が良い。

MATHの標準思考連鎖では、35.7と31.6の差は4.1ポイントである。原著の「特定MMLU科目で最大25.0ポイント」は科目別選抜の結果であり、MATH全体の改善でもMMLU全科目の平均改善でもない。指標と分母を取り違えないよう、個別課題と全体平均を分けて読む必要がある。

### チーム最適化と構成要素除去

| 設定 | 最適化前 | 最適化後 | 機構の意味 |
|---|---|---|---|
| HumanEval候補12→8人 | Pass@1 76.2・23.04呼出し | 82.9・16.85呼出し | 役割選抜が品質と費用の両方に寄与 |
| WebShop候補8→4人 | 報酬53.0・32.03呼出し | 68.3・24.85呼出し | 不適切な参加者の干渉を減らす |
| MMLU候補7→4人 | 正答率69.5・8.30呼出し | 70.5・4.39呼出し | 科目別の適応で呼出しを減らす |
| MATHで早期終了を除去 | 35.7・7.15呼出し | 35.0・13.00呼出し | 早期終了は主として呼出し削減 |
| MMLUで早期終了を除去 | 70.5・4.39呼出し | 70.1・13.00呼出し | 終了条件なしでは費用が急増 |
| HumanEvalで再編成を除去 | 82.9・16.85呼出し | 76.2・17.98呼出し | 再編成が品質に寄与 |
| WebShopで再編成を除去 | 報酬68.3・24.85呼出し | 66.0・48.90呼出し | 再編成なしでは品質と費用が悪化 |

ここで構成要素除去の行は「最適化前・後」の時間順ではなく、左が完全版、右が該当機構を外した版である。MATHの早期終了を外すとAPI呼出しが7.15から13.00へ増え、品質は35.7から35.0へわずかに下がる。これに対して再編成を外すとHumanEvalの82.9が76.2まで落ちる。したがって、早期終了と再編成を別々に設計する根拠がある。

MMLUのcollege mathematicsでは正答率40.0から65.0へ改善するが、候補の中に関連役割がないpublic relationsでは54.5から59.1への小さな改善にとどまる。役割選抜は、必要な能力が候補に存在して初めて効果を発揮する。付録C.3では人間の事前判断による役割選抜より、実際の協調から得た重要度を使う方式が有利な例を示す。5科目平均では事前選抜66.7に対し重要度選抜73.6であり、説明文だけから役割を推定する限界を示している。

### 負の結果・感度・再現上の注意

自由形式のコードでは意味が同じでも表現が異なり、BLEUによる一致判定では早期終了が効きにくい。候補エージェントがすべて対象分野に不適切なら、重要度の順位を付けても適切な能力を新規に生み出せない。付録C.4では生成温度を高くすると多様性の利点を得る条件がある一方、算術推論のAPI呼出しは温度0.2から1.0で平均約0.98回増える。品質だけでなく費用側の感度もある。

付録C.5の順位付け比較では、一覧順位付け70.5・4.39呼出しに対し、対比較のLLM-Blenderは70.1・19.27呼出し、Eloは70.3・19.55呼出しである。順位付け方式の変更が性能差より大きな呼出し差を生む。付録C.6ではエージェント重要度とシャープレイ値（Shapley Value）の関連を評価するが、シャープレイ値は多数の部分集合を評価するため、実行時の低費用な代替としてそのまま使えない。重要度推定は無監督であっても、LLM相互評価に由来する偏りを持つ可能性がある。

## 既存研究との差

固定した役割と通信路で討論する方式、候補を一度だけ選んで並列実行する方式、単一エージェントが逐次自己修正する方式と異なり、DyLANは「予備試行による選抜」と「本番中の枝の除去」を同一の時間展開グラフ上で扱う。間接的な貢献を後方伝播で集計するため、最終回答を直接出した参加者だけを評価する単純な投票とは異なる。評価表では役割の選抜が品質に、早期終了が呼出し数に、再編成が両者に異なる程度で寄与することが示される。

ただし、推論システムとしての階層は高い。KVキャッシュの圧縮、重み量子化、演算子融合、GPU配置、バッチ化などを直接最適化するものではなく、複数のLLM呼出しをどの順序・構造で実施するかを扱う。したがって、他の推論基盤研究と比較するときは、API呼出し削減をGPU処理率の改善と混同しない。

## 限界・未評価事項

予備協調を含めた全体費用は、主要表に示す本番段階のAPI呼出しだけでは表現できない。単発の要求では選抜準備の費用を回収できない可能性がある。呼出し数はトークン長、入力文脈、価格、並列実行、待ち時間、GPU資源を反映しないため、課金額や壁時計遅延を同じ比率で削減するという結論は導けない。

重要度の教師は人手で付けないが、エージェント同士のLLM評点に依存する。誤った回答を全員が支持した場合には早期終了が品質を保証しない。特定の課題で必要な役割が候補にない場合、選抜で能力を補えない。論文の主な実験はGPT-3.5系を用い、異なるオープンモデル、数百エージェントの大規模構成、厳格な応答時間目標、複数要求の同時実行などについて一般的な保証はない。

## 一次資料・監査履歴

- COLM 2024公式掲載情報とPDF： https://openreview.net/forum?id=XII0Wp1XA9 、 https://openreview.net/pdf?id=XII0Wp1XA9
- 論文本文の閲覧可能な再掲（COLM 2024版30ページ）： https://www.scribd.com/document/856503167/LLM-Research-Paper
- 書誌・版履歴： https://arxiv.org/abs/2310.02170
- 著者公式実装： https://github.com/SALT-NLP/DyLAN
- 照合箇所：本文§3.2～3.4、表2～6、§4.3、付録C.3～C.6。主な表の数値、負の結果、費用指標の対象範囲を確認した。
- 2026-10-11 13:00 JST：固定mainの原稿と、GitHub差し戻し原稿を参照して再監査。差し戻しの「評価説明量277文字」判定に対処するため、評価の条件・結果・構成要素除去・限界を単一の「評価」節とその下位見出しに統合した。既存原稿の構造化参考文献46件を保持。一次資料の原著テキストを照合し、差し戻し原稿を単純に合格扱いしなかった。
- 2026-10-11: 形式監査で欠けていた分類、説明量測定、完了日時を補完。完了日時はLibrary原稿の初回保存時刻とし、元の論文解説と構造化参考文献を保持。
