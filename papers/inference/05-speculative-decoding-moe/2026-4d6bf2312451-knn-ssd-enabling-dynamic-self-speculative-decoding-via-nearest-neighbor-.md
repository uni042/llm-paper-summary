---
canonical_id: "DOI:10.18653/v1/2026.findings-eacl.31"
title: "KNN-SSD: Enabling Dynamic Self-Speculative Decoding via Nearest Neighbor Layer Set Optimization"
authors:
  - "Mingbo Song"
  - "Heming Xia"
  - "Jun Zhang"
  - "Chak Tou Leong"
  - "Qiancheng Xu"
  - "Wenjie Li"
  - "Sujian Li"
published: "2026-03-24"
publication: "Findings of the Association for Computational Linguistics: EACL 2026, pp. 641–655"
publication_type: "査読付き国際会議論文"
publication_status: "published"
doi: "10.18653/v1/2026.findings-eacl.31"
source: "https://aclanthology.org/2026.findings-eacl.31.pdf"
sources:
  - "https://aclanthology.org/2026.findings-eacl.31.pdf"
  - "https://aclanthology.org/2026.findings-eacl.31/"
  - "https://github.com/mbsong/KNN-SSD"
summary: "KNN-SSDは、同一LLMの一部層を飛ばすSelf-Speculative Decodingで、入力ドメインが変わると固定skip-layer集合の受理率・速度が悪化する問題を扱う。ドメイン別の最適skip集合をBayesian Optimizationで事前探索し、最後の隠れ状態をK-meansで代表化したアンカーへのKNN類似度から入力ごとに集合を選ぶ。LLaMA-2-13Bの混合タスク平均はvanilla 13.62 tokens/s、固定Self-SD 16.34、KNN-SSD 19.61（1.44倍）、Qwen2.5-14Bでは11.16→18.08 tokens/s（1.62倍）。ただしドメイン別1000回の事前探索、推論時の隠れ状態抽出とKNN探索、評価対象モデルが最大14Bという制約がある。"
list_summary: "Self-SDのskip-layer集合をドメイン別に事前最適化し、入力の最終隠れ状態からKNNで動的選択。LLaMA-2-13Bで1.44倍、Qwen2.5-14Bで1.62倍だが事前探索と分類費用が必要。"
implementation: "著者公式コード https://github.com/mbsong/KNN-SSD 。PyTorch/Transformers、CUDA 12.0、RTX 3090×8およびRTX A6000×4で検証。ドメインごと1000回のBayesian Optimizationと代表アンカー選択を実施。"
implementation_status: "official-code-public; evaluated-on-multi-gpu-workstations"
code: "https://github.com/mbsong/KNN-SSD"
last_checked: "2026-10-27"
worker_id: "scheduled-chat-45"
scheduled_slot: "45"
worker_run_key: "20261027-1645-scheduled-chat-45/r01"
reference_main_sha: "f394e5556881587d1fbd29e587b1462f47a1cc13"
worker_completed_at: "2026-10-27T16:51:00+09:00"
quality_self_review_passed: true
quality_self_review_version: "PAPER-QUALITY-GUIDE-2026-10-07"
research_scope: "domain-adaptive-speculative-decoding-layer-skipping-routing"
last_audited: null
audit_version: 0
---

# KNN-SSD：入力ドメインに応じて層スキップ集合を切り替える自己投機的デコード

## 書誌と概要

Mingbo Songほか、*KNN-SSD: Enabling Dynamic Self-Speculative Decoding via Nearest Neighbor Layer Set Optimization*、Findings of EACL 2026、641–655ページ、2026年3月24–29日開催。DOI:10.18653/v1/2026.findings-eacl.31。著者公開実装あり。投機的デコードは、小型ドラフトで複数トークンを先読みし、ターゲットLLMでまとめて検証することで、元のターゲット分布を維持しつつ逐次生成の回数を減らす。Self-Speculative Decoding（Self-SD）は別のドラフトモデルを持たず、同じLLMの一部のattention/MLP層を飛ばした経路をドラフトとして使う。

しかし固定した層スキップ構成は入力ドメインに敏感である。要約で良い層集合が数学推論や翻訳では受理率を落とし、速度向上が消えることがある。KNN-SSDは、ドメインごとにskip-layer集合を事前最適化し、推論入力の最後の隠れ状態からKNNでドメインを推定して適切な集合を選ぶ。5タスクを混合した評価でLLaMA-2-13Bは13.62→19.61 tokens/s（1.44倍）、Qwen2.5-14Bは11.16→18.08 tokens/s（1.62倍）と報告する。これらは単純なモデル圧縮の速度ではなく、ドラフト生成とターゲット検証を含むSelf-SD経路の改善である。

## 問題設定

### 固定skip-layer集合のドメイン依存性

層スキップは計算を減らす一方、飛ばした層が重要なタスクではドラフト分布がターゲットから離れる。ターゲットが候補を棄却すると、先読みした計算は無駄になり、検証回数も減らない。従来のSelf-SDは代表入力に対してBayesian Optimization（BO）でスキップの有無を表す二値マスクzを探索し、その後は同じマスクを使う。しかし要約・推論・翻訳・物語生成・Text-to-SQLでは最適マスクが異なる。

原著Figure 2では、要約用に選んだマスクは要約で1.41倍でも、他タスクでは0.97倍など1倍未満の例がある。これはモデルが小さくなれば必ず速いわけではなく、**ドラフトの受理率と層削減量の積**で最終速度が決まることを示す。対象は異なる入力が到着するサーバの生成負荷であり、静的な一ドメインのベンチマークだけでは十分に評価できない。

### 追加学習と追加モデルを避ける

別モデル型の投機的デコードではドラフトを訓練・保持する費用が必要になる。KNN-SSDは元のLLMを共有し、層を飛ばすマスクだけを切り替える。ドメイン別マスクの探索とKNNの学習・保持は必要だが、新しい大規模なドラフト重みを追加しない。最終的な検証は全層のターゲットが行うため、原著はターゲット分布を変えないlosslessな復号として扱う。ただしこれは正しい検証・補正実装が前提であり、単なる層スキップ生成をそのまま出力すればlosslessになるわけではない。

## 手法

### 1. ドメインごとのskip-layer集合を探索

ドメインD_iごとにサンプルを取り、LLMの最後の隠れ状態ベクトルを抽出する。K-meansで特徴空間をクラスタ化し、重心に近い代表アンカーを選ぶ。各ドメインのアンカーを使って、各Transformer層のattention/MLPをスキップするかを示す二値マスクz_iをBOで探索する。目的関数は、代表サンプル上の**検証済み1トークン当たり平均推論時間**である（原著式1・3）。単にスキップする層数を最大化するのではなく、受理率低下まで含めて最小時間となるマスクを選ぶ。

原著の主要実験では各ドメインで代表8サンプルを用い、BOを1000反復実施する。したがってオフラインの探索費用は小さくない。モデルやタスクが変わると最適マスクが変わるため、既存の設定を別モデルへそのまま転用できない。探索したマスクは設定ファイルへ保存し、推論時にはBOを毎回実行しない。

### 2. 最終隠れ状態からKNNドメイン判定

各ドメインの入力について最後の隠れ状態を収集し、代表アンカーを保存する。付録C.1では各データセットから1000ベクトルを選び、K-meansを用いて10個の代表を抽出する。新しい入力が来たらLLMからその入力の最後の隠れ状態vを得て、保存済みアンカーとのcosine類似度が最大のものを探し、そのアンカーが属するドメインのskip-layerマスクを選択する（原著式4–6）。

この方式は入力文の表面的な単語ではなく、LLMの内部表現でドメインを近似する。原著の5タスクではドメイン分類精度100%と報告されるが、学習・評価のタスク集合が明確で、表現が分離した条件での結果である。未知の新規ドメイン、類似ドメインの境界、分布が連続的に変わる実運用での100%精度を保証しない。

### 3. 自己投機的デコードの実行

ドメインを判定した後、選んだz_iで層をスキップした同一LLMをドラフトとして先読みトークンを生成する。全層のターゲットモデルがそれらを一括検証し、受理・補正する。ターゲットの検証を残すことで、ドラフトの誤りを最終出力へ直接通さない。したがってドメイン分類が外れても原理的には生成品質よりも**速度・受理率**に影響する。

推論時に追加するのは特徴抽出・KNN探索とマスク選択である。通常のTransformer推論で得られる隠れ状態を再利用できる構成でも、分類に要するGPU/CPU時間はゼロではない。入力ごとの分類が遅い場合、短い生成では層スキップの利益を相殺する。

### 4. ドメイン切替頻度を制御した入力列

原著はmix ratio rを、次の要求が現在と異なるタスクになる確率として定義する。r=0は同じタスクが連続する入力列、r=1は隣接する要求が必ず異なるタスクになる列である。r=0/0.3/0.7/1.0の4条件を作り、単一ドメインで最適化したマスクが分布変化にどの程度弱いかを検証する。固定マスクのSelf-SDと、混合入力に対して単一マスクを再最適化したSelf-SDの双方を比較するため、ドメイン適応そのものの効果を切り出せる。

## 評価

### 環境・データ・比較

原著§5・付録C.1では、LLaMA-2-13B、LLaMA-2-13B-Chat、Qwen2.5-14B、Qwen2.5-14B-Instructを用いる。実験機材はRTX 3090 24GB×8とRTX A6000 40GB×4、CUDA 12.0、Xeon Gold 5117、PyTorch/Transformers。これは複数GPU搭載のワークステーション環境であり、12GB VRAM単体GPUの実測ではない。KV cacheは有効。タスクはCNN/DailyMail（要約）、GSM8K（数学推論）、WMT16独英翻訳、TinyStories（物語生成）、Spider2（Text-to-SQL）で、各40件・合計200件の混合列を評価する。

比較はvanilla逐次デコード、最初のタスクに合わせた固定マスクSSD_F、混合分布に対し単一マスクを再探索したSSD_M、入力ごとにKNNで切り替えるKNN-SSD。論文はtokens/sとspeedupのほか、ターゲット一回当たりの平均受理長Mとドラフトトークン受理率αを報告する。速度は実測tokens/sの表と、M・α・スキップ率から計算する期待speedupの表があり、**両者を同一指標として混同しない**。

### 主要結果：生成速度

| モデル | Vanilla | SSD_F | SSD_M | KNN-SSD | KNN-SSD / Vanilla |
|---|---:|---:|---:|---:|---:|
| LLaMA-2-13B | 13.62 tok/s | 16.34 | 16.88 | 19.61 | 1.44倍 |
| LLaMA-2-13B-Chat | 13.22 | 14.67 | 15.33 | 17.85 | 1.35倍 |
| Qwen2.5-14B | 11.16 | 14.06 | 15.40 | 18.08 | 1.62倍 |
| Qwen2.5-14B-Instruct | 10.79 | 12.84 | 13.49 | 16.30 | 1.51倍 |

原著Table 1のgreedy decoding・4つのmix ratio平均に基づく。たとえばLLaMA-2-13BでSSD_Fの16.34に対してKNN-SSDは19.61 tok/sで、既存Self-SD比では約1.20倍である。**1.44倍はvanilla比**であり、固定Self-SD比1.44倍という意味ではない。モデルにより改善幅は変わる。

### ドメイン混合と受理率

原著Table 2の期待speedupでは、LLaMA-2-13BのKNN-SSDはr=0/0.3/0.7/1.0で1.42/1.45/1.43/1.45倍。SSD_Fは1.24/1.21/1.19/1.17倍へ悪化する。Qwen2.5-14BのKNN-SSDは1.60/1.64/1.63/1.61倍で、ドメイン切替に対して比較的安定している。固定マスクの劣化が実験の主な対照結果である。

原著Table 3のr=1.0・5タスク混合では、LLaMA-2-13Bの平均受理長MがSSD_F 2.17、SSD_M 2.53、KNN-SSD 3.12、受理率αが0.62/0.68/0.88。実測speedupは1.10/1.14/1.34倍だった。LLaMA-2-13B-Chatでは受理率0.57/0.59/0.85、実測speedup1.04/1.09/1.28倍。これらの実測speedupはTable 2の期待値と一致しないため、異なる指標を同じ表へ無説明で混ぜない。

### オーバーヘッド・OOD・負の結果

LLaMA-2-13B、最大生成128トークンの5タスク平均では、生成時間約7.5秒のうち隠れ状態保存とKNN検索が約0.18秒（約2.5%）を占める。生成512/1024トークンでは平均生成時間23.2/43.7秒に対して検索費用の比率0.77/0.41%へ下がる。これは**短い生成では分類費用が相対的に重い**ことを示す。事前のBO 1000反復の費用はこのオンライン0.18秒に含まれない。

MATHの7カテゴリを単一データセット内の複数ドメインとして扱ったTable 4では、LLaMA-2-13BのKNN-SSDはM=2.37、受理率0.81、speedup1.23倍。一方、固定SSD_FはM=1.54、受理率0.51、speedup0.97倍と**vanillaより遅い**。KNN-SSDが常に1.6倍というわけではなく、ドメイン構成やモデルに依存する。論文はOODデータでも約1.2倍の利得を報告するが、未知ドメインを含む全実運用負荷での保証ではない。

## 既存研究との差

従来Self-SDは一つの固定skipマスクをBOで求める。LayerSkipなども層の省略を利用するが、KNN-SSDは**入力ごとにマスクを切り替える**。別ドラフトを持つEAGLE型や小型LLM型の投機的デコードと異なり、重みの追加を抑えたままドメイン依存性を緩和する。単純なKNN分類を追加しただけではなく、ドメインごとの最適化対象が「検証済みトークン当たり時間」であること、ドメイン切替頻度を制御した混合列で比較していることが重要である。

マスクを変えても全層ターゲットによる検証は必要なので、受理率の改善が速度に結びつく。KNN自体がターゲットモデルの計算量を減らすわけではない。別のドメイン推定器、prompt埋め込み、事前分類器を使った場合の性能はこの論文では体系的に比較されていない。

## 限界と実装上の判断

第一に、BO探索はモデル×ドメインごとに必要で、1000反復×複数ドメインというオフライン費用を伴う。ドメイン集合が頻繁に増減する場合は再探索とアンカー更新が必要となる。第二に、分類にはLLMの最終隠れ状態が必要で、特徴抽出の時点で一定の前処理費用が発生する。第三に、最大14Bまでのモデルと5つの代表タスクを中心とした評価であり、70B級、MoE、長い文脈、複数要求を継続バッチ化する本番サーバでの性能は未確認である。

原著自身は、tree-based draft verificationを導入していないこと、より大規模モデルでの評価が未完了であることを限界として挙げる。さらに、表で示す期待speedupと実測speedupの差、ドメインが明瞭に分離した条件での100%分類精度、短い出力での0.18秒の検索費用を考えると、サーバへの導入前には実トレースのドメイン分布と生成長を確認すべきである。losslessという主張は検証ステップに依存し、任意のサンプリング設定や独自カーネルでの再現性は別途テストが必要である。

## 一次資料・公式実装

- EACL Findings 2026採録PDF（15ページ）：https://aclanthology.org/2026.findings-eacl.31.pdf
- 書誌ページ：https://aclanthology.org/2026.findings-eacl.31/
- 著者公開実装：https://github.com/mbsong/KNN-SSD
- 原著§3–4、式(1)–(8)：層スキップ、BO、アンカー、KNN、mix ratio。
- 原著§5、Tables 1–4、Figures 1–7：tokens/s、mix ratio、受理率、MATH、オンライン検索費用。
- 付録A–C：マスクの感度、実験GPU、代表アンカー、期待速度式と実測条件。

## 品質セルフレビュー

採録版PDF本文と付録の定量表を確認した。Table 1のtokens/sとTable 2の期待speedup、Table 3の実測speedupを区別し、vanilla比と固定Self-SD比を混同しないようにした。ドメイン切替、MATHでの固定SSDの減速、検索費用、BO事前費用、モデル規模の制約を明記した。
