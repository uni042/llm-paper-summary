---
canonical_id: DOI:10.18653/v1/2026.acl-long.1683
doi: 10.18653/v1/2026.acl-long.1683
arxiv_categories:
  primary: null
  cross_list: []
title: 'LazyEviction: Lagged KV Eviction with Attention Pattern Observation for Efficient Long Reasoning'
summary: 長い思考連鎖では生成トークンが数千〜16kへ伸び、KVキャッシュがGPUメモリを圧迫する。従来の現在注意値や累積注意値による貪欲削除は、一時的に注意が低くても後で再び重要になるトークンを早期削除する。LazyEvictionはトークン重要度再帰現象を観測し、重要になった時刻間の最大再帰間隔を追跡する。W復号stepごとの観測窓で削除を遅延し、最終重要時刻からの経過と最大再帰間隔から将来重要度を予測してKVを保持する。4B〜32Bの推論モデルと数学・科学QA・コード生成で、FullKVの30〜50%予算でも近い精度を保ち、従来KV圧縮を上回る。
list_summary: 一時的に注意が下がって後で再重要化するトークンを最大再帰間隔で予測し、観測窓ごとの遅延削除で長い推論のKVキャッシュを圧縮する方式。
authors:
- Haoyue Zhang
- Hualei Zhang
- Xiaosong Ma
- Jie Zhang
- Song Guo
authors_affiliations: The Hong Kong University of Science and Technology; The Hong Kong Polytechnic University
published: '2026-07-02'
publication: ACL 2026 Long Papers
publication_type: Conference paper
publication_status: Published
lineage: 長時間推論向けKVキャッシュ削除
topics:
- KV キャッシュ 追い出し
- long reasoning
- トークン importance recurrence
- attention sparsity
importance: 長い推論ではトークン重要度が時間を置いて再発することを実測し、単step貪欲削除ではなく将来の再重要化を予測するKV保持へ転換した。
hardware_evaluation: 本文主要節では評価GPU型を明示していない。4B〜32B推論モデルを評価。100B級評価の資源例として8×A100でMATH-500 500問に数日を要すると記載。
hardware_details: 主要評価ハードウェアの型番は本文から確認できず。
quality_effect: FullKVの30〜50% KV予算で数学・科学QA・コード生成の精度を概ね維持し、複数条件で既存削除法を上回る。
references:
- canonical_id: arXiv:2309.17453
  arxiv_id: '2309.17453'
- canonical_id: arXiv:2401.06104
  arxiv_id: '2401.06104'
- canonical_id: arXiv:2408.03675
  arxiv_id: '2408.03675'
- canonical_id: arXiv:2502.11147
  arxiv_id: '2502.11147'
references_checked_at: '2026-09-20'
references_source: primary-reference-section
references_total: 4
source: https://aclanthology.org/2026.acl-long.1683/
sources:
- https://aclanthology.org/2026.acl-long.1683/
- https://aclanthology.org/2026.acl-long.1683.pdf
code: https://github.com/Halo-949/LazyEviction
implementation: 復号時にattention threshold超過時刻と最大再帰間隔をトークンごとに更新し、W step間隔で最新W トークンを常時保持した上で残りをMRI中心scoreで選別する。
last_checked: '2026-09-20'
last_audited: null
audit_version: 0
---

# LazyEviction: Lagged KV Eviction with Attention Pattern Observation for Efficient Long Reasoning

> 一時的に注意が下がって後で再重要化するトークンを最大再帰間隔で予測し、観測窓ごとの遅延削除で長い推論のKVキャッシュを圧縮する方式。
## 書誌情報
- **著者**: Haoyue Zhang, Hualei Zhang, Xiaosong Ma, Jie Zhang, Song Guo
- **著者・所属**: The Hong Kong University of Science and Technology; The Hong Kong Polytechnic University
- **公開**: ACL 2026 Long Papers
- **種別**: Conference paper
- **対象**: KV キャッシュ 追い出し、long reasoning、トークン importance recurrence、attention sparsity
- **実装**: 復号時にattention threshold超過時刻と最大再帰間隔をトークンごとに更新し、W step間隔で最新W トークンを常時保持した上で残りをMRI中心scoreで選別する。
## 概要
長い思考連鎖では生成トークンが数千〜16kへ伸び、KVキャッシュがGPUメモリを圧迫する。従来の現在注意値や累積注意値による貪欲削除は、一時的に注意が低くても後で再び重要になるトークンを早期削除する。LazyEvictionはトークン重要度再帰現象を観測し、重要になった時刻間の最大再帰間隔を追跡する。W復号stepごとの観測窓で削除を遅延し、最終重要時刻からの経過と最大再帰間隔から将来重要度を予測してKVを保持する。4B〜32Bの推論モデルと数学・科学QA・コード生成で、FullKVの30〜50%予算でも近い精度を保ち、従来KV圧縮を上回る。

LazyEvictionは毎step即時削除をやめ、W stepの観測窓ごとに削除判断を遅延する。各トークンについてattentionが閾値を超えた最終時刻と、過去の重要化間隔の最大値である最大再帰間隔（Maximum Recurrence Interval: MRI）を追跡する。最終重要時刻からの経過時間がMRIへ近づくほど再重要化の見込みが下がるという生存確率と、MRIが短いトークンほど頻繁に再帰するという頻度事前分布を組み合わせて将来重要度を推定する。これにより低注意区間にいる再帰トークンを保持し、将来必要になる前の早期削除を避ける。

代表結果として、GSM8K accuracy at 50% KV budgetはKV budget ratio 50%でFullKV 81.73/89.92/93.32/95.61に対してDS-Llama 80.06、DS-Qwen 88.40、Qwen3 91.50、QwQ 93.48。半分のKVでもFullKVに近い数学推論精度を維持。
## 問題設定
長い思考連鎖では復号が数千から16k語へ伸び、過去トークンの鍵・値を保持するKVキャッシュが系列長に比例して増える。バッチ 32の16k推論では100GB超になり得る。既存削除法は現在attention値、累積attention値、直近/先頭位置などから各stepで不要トークンを貪欲に捨てる。しかし推論中のトークンは、一度重要になった後しばらく注意が低下し、検証・逆戻り・要約時に再び強く参照される。論文は95%超のトークンでこの重要度再帰を観測し、GSM8Kでは同じ50%圧縮でH2O/TOVAが一般長文より約20%精度を落とすことを示す。したがって現在や累積の低注意だけで削除せず、将来再び重要になる可能性を時間パターンから判断する必要がある。
## 新規性
LazyEvictionは毎step即時削除をやめ、W stepの観測窓ごとに削除判断を遅延する。各トークンについてattentionが閾値を超えた最終時刻と、過去の重要化間隔の最大値である最大再帰間隔（Maximum Recurrence Interval: MRI）を追跡する。最終重要時刻からの経過時間がMRIへ近づくほど再重要化の見込みが下がるという生存確率と、MRIが短いトークンほど頻繁に再帰するという頻度事前分布を組み合わせて将来重要度を推定する。これにより低注意区間にいる再帰トークンを保持し、将来必要になる前の早期削除を避ける。
## 手法
### 手法のあらまし
入力は自己回帰復号中に各層から得られるトークン別attention値、現在GPU上に保持するKV集合S、最終的に残したい容量上限B、削除判断間隔となる観測窓W、重要attentionを判定する閾値αである。新しいトークンを一つ生成するたび、まず通常のattentionを実行してそのトークンのKVを追加する。同時に、既存トークンのattentionがαを超えた場合は、そのトークンが再び重要化したと判定する。前回重要時刻と現在時刻の差を求め、それが過去最大より長ければ最大再帰間隔MRIを更新し、最新重要時刻TSを現在stepへ進める。この追跡は毎step行うが、KV削除そのものはt=kWとなる観測窓境界だけで実行する。境界に到達して保持数がBを超えたら、最新W個のKVを局所一貫性のため無条件に保護する。それより古いトークンについて、現在時刻からTSまでの経過時間をMRIで正規化した生存確率項と、MRIが短いほど高くなる再帰頻度項を計算し、両者を足した将来重要度scoreを作る。MRIが0で再重要化実績のないトークンは生存確率項だけで扱う。古いKVをscore順に並べ、上位B-W個を最新W個と結合して次の保持集合S'とし、残りのKVをGPUメモリから削除する。次のW stepではこの圧縮済み集合へ新規KVを足しながらTS/MRI追跡を続け、次の境界で同じ選別を反復する。最終的にモデルが出すトークン列は通常の自己回帰復号と同じ手順で生成されるが、attentionが参照できる過去KVだけが将来重要度予測によって動的に制限される。

### 重要度再帰の時刻追跡
各トークンに最新重要時刻TSと最大再帰間隔MRIを持たせる。attention scoreが閾値αを超えたときだけ重要化とみなし、前回TSとの差を計算してMRI=max(旧MRI, 今回間隔)へ更新した後、TSを現在stepへ進める。新規トークンのMRIは0から始まる。これによりattention値そのものを長期累積する代わりに、『最後にいつ重要だったか』『これまで最長で何step休眠してから再重要化したか』という時間構造を小さい状態で保持する。入力はstepごとのattention、出力はトークンごとのTS/MRIで、削除判断の将来予測へ渡される。

### 観測窓による遅延削除
従来法のように各復号stepで即座にKVを削除せず、W stepごとの判断時点だけで削除する。窓の開始後は通常どおり新規トークンのKVを追加し、保持数が一時的にBを超えても境界までは削除せず、その間のattention変化を観測する。これにより、あるトークンが数stepだけ低注意になった直後に再び重要化する場合、その再帰を確認する前に捨てる危険を減らす。境界t=kWで選別を始める際には最新W個を無条件に保護し、局所的な言語一貫性を維持する。残りの古いトークンにだけMRI中心scoreを適用し、B-W枠を配分する。Wは再帰トークンの休眠期間を覆う安全バッファであり、論文では各model/taskについてtest sampleの1%からMRI分布を事前測定し、80%のトークンのMRIを覆う値をWとして選ぶ。たとえばQwenのMATH-500では出力が8kに達しても80%のトークンのMRIが175未満であり、W=175程度の観測で多数の再帰を捕捉できる。出力は『最新W個＋予測重要度の高い古いB-W個』からなる次窓のKV集合である。

### MRI中心の将来重要度score
古いトークン iについて二つの項を計算する。第一項は最終重要時刻からの経過ΔTをMRIで割り、ΔTがMRIへ近づくほどsigmoidで値を下げる生存確率である。第二項はMRI自体が短いトークンほど頻繁に再重要化するとみなして高得点にする頻度事前分布である。MRIが0なら第二項は使わない。二項を足したscoreで古いKVを順位付けし、上位B-Wだけを保持する。これにより単なる累積attentionが低いトークンでも、再帰周期から近い将来の重要化が期待されれば残せる。ablationでは第一項を外すとGSM8K精度がDS-Llamaで3.95点、DS-Qwenで5.62点低下した。

### 予算制約付き反復復号
KV数が予算Bを超えた観測窓境界でだけscore計算と選別を行い、保持集合をB程度へ戻す。その後も通常の自己回帰復号を続け、新しいKVを追加しながら次の窓までTS/MRIを更新する。削除計算をW stepに一度へ間引くため、毎step圧縮より管理オーバーヘッドを抑える。長い生成ではFullKVのattention計算量がトークン数とともに増え続ける一方、LazyEvictionはKV budgetを制限するため、論文では16k生成付近で追加score計算を含めてもFullKVより推論効率が高くなると報告する。

### 全体のデータ／制御の流れ
既存推論モデルを再学習せず、復号時のKV管理層へ追加できる。attention値からTS/MRIを更新し、W stepごとに最新W個＋将来重要度上位B-W個だけをGPU上のKVとして残す。コードは著者GitHubで公開され、4B〜32Bの推論モデルで評価されている。
## 評価条件
- **ハードウェア**: 主要評価のGPU型番は本文主要節で明示されない。制約説明では100B級DeepSeek-R1のMATH-500 500問評価に8×A100で数日必要と記載。
- **ソフトウェア**: 著者実装を公開。復号attention値からトークンごとの最新重要時刻と最大再帰間隔を追跡し、観測窓ごとにKVを削除。
- **比較対象**: FullKV、RaaS、H2O、TOVA、CAKE、R-KV
DeepSeek-R1-Distill-Llama-8B、DeepSeek-R1-Distill-Qwen-7B、Qwen3-4B、QwQ-32Bを数学GSM8K/MATH-500/AIME、科学QAのGPQA Diamond、コードのLiveCodeBenchで評価する。FullKV、RaaS、H2O、TOVA、CAKE、R-KVと同じKV予算比で精度を比較する。主要条件はGSM8K/MATH-500が50%、AIMEが30%、GPQAが50%、LiveCodeBenchが40%。さらにLlama-3.1-8B-Instructで一般長文QA/要約も検証し、観測窓・score項・閾値のablation、0〜8k生成でのKVメモリ変化と長生成時オーバーヘッドを測る。
長い思考連鎖を生成する復号段階のKV削除が中心。再学習なしの推論時圧縮で、4B〜32B reasoning modelと一部一般長文生成を対象にする。
## 主要結果
LazyEvictionはFullKVの30〜50%だけを保持する厳しい予算でも、4種類のreasoning modelと複数領域で既存KV削除法より高い精度を示した。GSM8K 50%予算ではDS-Llama 80.06対FullKV 81.73、DS-Qwen 88.40対89.92。MATH-500 50%ではDS-Llamaが75.2でFullKV 74.8を上回り、DS-Qwenも85.4対86.0に近い。AIME 30%ではDS-Llama 30.0でFullKVと同値、QwQ-32B 66.7対73.3。GPQA 50%では36.9/54.6でFullKV 37.4/55.7に近く、LiveCodeBench 40%でも56.90/51.72で既存圧縮を上回る。

- GSM8K accuracy at 50% KV budget / DS-Llama 80.06、DS-Qwen 88.40、Qwen3 91.50、QwQ 93.48 (比較対象: FullKV 81.73/89.92/93.32/95.61; 条件: KV budget ratio 50%) — 半分のKVでもFullKVに近い数学推論精度を維持。

- MATH-500 accuracy at 50% KV budget / 75.2/85.4/85.8/85.4 (比較対象: FullKV 74.8/86.0/87.2/87.2; 条件: 4 reasoning models) — DS-LlamaではFullKVを上回り、他モデルも小さい差に抑える。

- GPQA Diamond at 50% KV budget / 36.9 DS-Llama、54.6 DS-Qwen (比較対象: FullKV 37.4、55.7; 条件: science QA) — 数学以外の推論でも精度をほぼ維持。

- LiveCodeBench at 40% KV budget / 56.90 DS-Llama、51.72 DS-Qwen (比較対象: FullKV 58.62、55.17; 条件: code generation) — 60%削減でもH2O/TOVA/RaaS/R-KVを上回る。

- H1 score ablation / -3.95点 DS-Llama、-5.62点 DS-Qwen (比較対象: full LazyEviction; 条件: GSM8K setting) — 最終重要時刻からMRIまでの経過を使う生存確率が主要寄与。

### 負の結果・境界条件
- 観測窓Wはmodel/taskごとのMRI分布に依存し、本文実装はtest sampleの1%をoffline解析して80% トークンを覆う閾値を選ぶため実運用では非効率かつdata leakage懸念がある。一般的な非reasoning言語モデルではMRIが10未満と短く、H2O/RaaSなど累積attention法との差が小さい。100B級モデルは未評価。観測窓中はKV数が一時的にbudgetを超えるためメモリ使用量が少し変動し、score追跡の追加計算もある。

### 結果の読み方
長い推論ではトークン重要度が単調に減るのではなく、問題条件や中間結論が後段で再利用される。現在値や累積値だけでは低注意の休眠区間に重要トークンを捨てるが、MRIは再利用の時間尺度を保持するため、将来重要化の直前までKVを残せる。
## 品質への影響
30〜50% KV budgetでFullKVに近い精度を保ち、特に既存貪欲削除が崩れやすい長い推論で改善が大きい。一般長文生成では利得が小さくなる。
## 既存研究との差
TOVA/NACL/TreeKVは現在attentionで各step削除し、H2O/Scissorhands/Keyformer/RaaSは累積attentionや最終時刻を使うが、低注意区間の後に再重要化する周期を明示的に扱わない。LazyEvictionは最大再帰間隔を記録し、削除判断自体を観測窓境界まで遅らせる。R-KV/RPCはreasoning path内のトークン類似性・冗長性を利用するのに対し、本方式はattentionの時間変化を直接扱う。KV量子化とは直交し、vLLMやCPU オフロード等のsystem-level管理とも併用可能。
## 限界
観測窓Wの選択が重要で、本文はmodel/taskごとに1% sampleからMRI分布をoffline計測する。この方法は実運用では追加準備とdata leakage懸念があり、著者も動的適応をfuture workとする。非reasoning一般生成では再帰間隔が短く、累積attention削除との差が小さい。評価は4B〜32Bで、100B級は資源制約により未検証。観測窓の間は新規KVを蓄えるため厳密な定数メモリではなくbudget周辺で小さく変動し、MRI追跡/score計算のオーバーヘッドも追加される。
## 実装状態
著者コードがGitHubで公開されている。再学習不要の復号時KV管理方式として、DeepSeek-R1 distilled系、Qwen3、QwQへ適用して評価済み。
## 研究上の位置づけ
長時間reasoning向けKV圧縮の中で、トークン重要度を静的・単調な量とみなさず時間的に再帰する状態として扱う系統。長い思考では検証、backtracking、要約により初期条件や中間結論が再参照されるため、将来重要度予測をKV 追い出しへ導入する。特に50〜70%のKV削減でもreasoning精度を保つことを狙い、単step greedy 追い出しからwindow単位のpredictive retentionへ設計を変える。
## 一次資料
- https://aclanthology.org/2026.acl-long.1683/
- https://aclanthology.org/2026.acl-long.1683.pdf
