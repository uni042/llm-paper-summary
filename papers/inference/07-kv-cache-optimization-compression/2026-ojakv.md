---
canonical_id: DOI:10.18653/v1/2026.findings-acl.494
doi: 10.18653/v1/2026.findings-acl.494
arxiv_categories:
  primary: null
  cross_list: []
title: 'OjaKV: Context-Aware Online Low-Rank KV Cache Compression'
summary: OjaKVは長文LLM推論のKVキャッシュを低ランク圧縮する際、静的な校正データ由来部分空間が会話・コード・長期推論などの分布変化で崩れる問題を扱う。再構成誤差と直近注意を用いて圧縮に弱い重要トークンだけをフルランク保持し、大多数の中間トークンは低ランク表現で保存する。射影基底はプリフィルでまとめて更新し、デコード中は一定間隔でバッファをOja則により軽量更新して現在文脈の主成分へ追随する。FlashAttention互換の再構成経路を持ち、RULER・LongBench・AIME2025で静的低ランク法を上回る。
list_summary: 重要トークンをフルランク保持し、残りのKVキャッシュをOja則で文脈適応する低ランク部分空間へ圧縮して長文生成時の分布変化へ追随する。
authors:
- Yuxuan Zhu
- David H. Yang
- Mohammad Mohammadi Amiri
- Keerthiram Murugesan
- Tejaswini Pedapati
- Pin-Yu Chen
published: '2026-07-02'
publication: Findings of ACL 2026
publication_type: conference
publication_status: published
topics:
- KVキャッシュ圧縮
- 低ランク近似
- オンラインPCA
- 長文推論
- FlashAttention
hardware_evaluation: NVIDIA H100 GPU上でLlama-2-7B、Llama-3.1-8B、LongChat-7b-v1.5-32k、DeepSeek-R1-Distill-Llama3-8B等を評価。
quality_effect: 0.8x/0.6xキャッシュ予算で静的PCAより長文検索・生成・推論精度を大幅に維持。lm-evalでは0.6xでもLlama-3.1-8B平均69.18%でFull KV 69.34%に近い。
references:
- canonical_id: arXiv:2402.14261
  arxiv_id: '2402.14261'
references_checked_at: '2026-09-20'
references_source: ACL Anthology PDF reference section; normalized subset recorded
references_total: 1
source: https://aclanthology.org/2026.findings-acl.494/
sources:
- https://aclanthology.org/2026.findings-acl.494/
- https://aclanthology.org/2026.findings-acl.494.pdf
code: https://github.com/zzbright1998/OjaKV
implementation: 著者コード公開。圧縮KVを注意計算直前にフル次元へ再構成してFlashAttentionへ渡し、プリフィルとデコードでOja則による基底更新を行う。
last_checked: '2026-09-20'
last_audited: null
audit_version: 0
---

# OjaKV: Context-Aware Online Low-Rank KV Cache Compression

> 重要トークンをフルランク保持し、残りのKVキャッシュをOja則で文脈適応する低ランク部分空間へ圧縮して長文生成時の分布変化へ追随する。
## 書誌情報
- **著者**: Yuxuan Zhu, David H. Yang, Mohammad Mohammadi Amiri, Keerthiram Murugesan, Tejaswini Pedapati, Pin-Yu Chen
- **公開**: Findings of ACL 2026
- **種別**: conference
- **対象**: KVキャッシュ圧縮、低ランク近似、オンラインPCA、長文推論、FlashAttention
- **実装**: 著者コード公開。圧縮KVを注意計算直前にフル次元へ再構成してFlashAttentionへ渡し、プリフィルとデコードでOja則による基底更新を行う。
## 概要
OjaKVは長文LLM推論のKVキャッシュを低ランク圧縮する際、静的な校正データ由来部分空間が会話・コード・長期推論などの分布変化で崩れる問題を扱う。再構成誤差と直近注意を用いて圧縮に弱い重要トークンだけをフルランク保持し、大多数の中間トークンは低ランク表現で保存する。射影基底はプリフィルでまとめて更新し、デコード中は一定間隔でバッファをOja則により軽量更新して現在文脈の主成分へ追随する。FlashAttention互換の再構成経路を持ち、RULER・LongBench・AIME2025で静的低ランク法を上回る。

OjaKVの核は、低ランクKV圧縮を一様な静的射影ではなく『重要トークンだけフルランクで残す混合保存』と『推論中に基底を追随させるオンライン部分空間更新』の二つに分けた点である。各keyの低ランク再構成残差が注意logit摂動の上界を直接決めることを利用し、直近queryで重み付けした再構成誤差が大きいトークンをフルランクのアンカーとして選ぶ。残りの多数トークンだけを圧縮し、そのkey/value射影基底をOjaのオンラインPCA則で更新する。プリフィルではprompt全体を平均プーリングして包括的に更新し、デコードでは新規KVをバッファしてTトークンごとに小さな学習率で更新するため、毎回SVDを解かず非定常な文脈へ追随できる。圧縮表現を注意直前に再構成する経路を採用してFlashAttentionとの互換性も維持する。

代表結果として、RULER平均精度はLongChat-7b-v1.5-32k、16K入力、0.6x キャッシュでStaticPCA 23.44%、Full KV 74%に対して39.99%（OjaKV）、50.7%（OjaKV-PF）。長文検索では混合保存と適応基底が静的低ランクより大幅に情報保持を改善する。
## 問題設定
長文LLMでは自己回帰生成の全過去トークンに対するkey/valueを保持するKVキャッシュが入力長・バッチに比例して増え、Llama-3.1-8Bの32Kトークン・バッチ 4では約16GBとモデル重み自体に匹敵する。低ランク射影は各KVベクトルをd次元からr次元へ落として保存量を減らせるが、既存のEigenAttentionやStaticPCAは小さな校正データで一度学習した固定部分空間を推論中ずっと使うため、対話からコード、promptから長いchain-of-thoughtへと活性分布が移ると射影誤差が増える。重み分解型は精度劣化やモデル変更を伴い、全履歴でSVDを再計算する動的方式は高価である。さらに全トークンを同じ比率で圧縮すると、現在の基底で表現しにくい重要トークンまで壊し、長文検索や生成品質が急落する。
## 新規性
OjaKVの核は、低ランクKV圧縮を一様な静的射影ではなく『重要トークンだけフルランクで残す混合保存』と『推論中に基底を追随させるオンライン部分空間更新』の二つに分けた点である。各keyの低ランク再構成残差が注意logit摂動の上界を直接決めることを利用し、直近queryで重み付けした再構成誤差が大きいトークンをフルランクのアンカーとして選ぶ。残りの多数トークンだけを圧縮し、そのkey/value射影基底をOjaのオンラインPCA則で更新する。プリフィルではprompt全体を平均プーリングして包括的に更新し、デコードでは新規KVをバッファしてTトークンごとに小さな学習率で更新するため、毎回SVDを解かず非定常な文脈へ追随できる。圧縮表現を注意直前に再構成する経路を採用してFlashAttentionとの互換性も維持する。
## 手法
### 手法のあらまし
初期基底は小さな校正集合のquery/keyを結合し、valueは別にSVDしてエネルギー閾値を満たすrankを選ぶ。推論開始後、各headのkey/valueをUk、Uvへ射影して低次元K̃、Ṽとして保存する。ただし各keyについて残差rt=kt-UkUk^Tktを計算し、最近のquery窓から得る注意影響で重み付けした誤差スコアを求める。上位k個の高誤差トークンは圧縮せずフルランク保持し、その他を低ランク化するため、最悪再構成誤差を直接抑える。プリフィルではpromptのKVを局所平均プーリングして共分散を作り、Oja更新U←U+η(CU-UU^TCU)を適用後QRで再直交化する。デコードでは新規KVをバッファBへ蓄積し、Tステップごとに同じ更新を小さいηで行い、基底を現在の生成分布へ追随させる。注意計算では圧縮K̃/ṼをUk^T/Uv^Tで元次元へ再構成し、フルランク保持トークンと合わせて標準FlashAttentionへ渡す。実用版OjaKV-PFはプリフィル注意自体は元のフルランクKVで行い、prompt特徴を基底更新と圧縮キャッシュ構築だけに使い、デコードから低ランク再構成を使う。

### 再構成誤差ベース混合保存
低ランク基底で表現しにくいトークンを一律圧縮から除外する。key ktの再構成残差rtを計算すると、query qに対する注意logit誤差はCauchy-Schwarzにより||q||||rt||/√dで上界付けできる。そこで直近query窓から実際の注意影響を集約したスコアを作り、上位k個の高誤差トークンをフルランクで保持する。残りだけを低ランク化することで、位置固定のattention sink保持より現在基底の弱点を直接検出し、圧縮トークンの最大残差を抑える。論文はsoftmax安定性と後段ネットワークのLipschitz性から最終logit摂動まで残差に比例する上界を導き、この選択が生成品質保全につながる根拠を与える。

### 二段階Ojaオンライン更新
静的校正基底の分布ずれを、ストリーミングPCAであるOja則を使って推論中に修正する。プリフィルではprompt全体のkey/value特徴を局所平均プーリングして冗長性を減らし、経験共分散に対するOja更新をまとめて適用してQR再直交化する。デコードでは各生成トークンの新規key/valueを小さなバッファへ蓄積し、固定間隔Tごとに保守的な学習率で基底を更新してバッファを消去する。全履歴SVDを繰り返さず、現在文脈の主成分方向へ少しずつ回転するため、長い生成で意味分布が変化しても射影誤差の累積を抑えられる。WikiText校正からMultiNewsへ移した実験では残差エネルギー比を0.255から0.097へ下げ、oracle基底との重なりを0.597から0.653へ改善する。

### FlashAttention互換再構成経路
FlashAttentionは通常n×dhのフル次元K/Vを受け取るため、圧縮特徴を直接処理する専用低ランクカーネルは既存実行系との互換性を失いやすい。OjaKVはキャッシュ上ではK̃=KUk、Ṽ=VUvだけを保持してメモリを節約し、注意計算直前にK̂=K̃Uk^T、V̂=ṼUv^Tへ再構成して標準FlashAttentionへ渡す。QもUkへ射影して低ランク空間で計算した場合と、再構成K̂を使う場合のlogitが数学的に等価であることを示し、同じ1/√dhスケールなら出力も一致する。これにより既存の高速attention カーネルを変更せず導入でき、OjaKV-PFではプリフィルを完全フルランクのまま実行してデコード時のメモリ削減だけを得る選択肢も持つ。

### 全体のデータ／制御の流れ
圧縮キャッシュ、フルランクアンカー、key/value別の適応基底、デコード更新バッファをhead単位で管理する。オンライン更新間隔T、学習率、バッファ長、フルランク保持数top-kが主な実行時調整値で、トークン 追い出しとは直交するため併用してメモリ削減を乗算できる。
## 評価条件
- **ハードウェア**: 主要実験はNVIDIA H100 GPU。Llama-3.1-8B-Instructの8K～32K効率測定ではKVメモリと最初のトークンまでの時間（TTFT）、デコード ms/トークンを測定する。
- **ソフトウェア**: Llama-2-7B、Llama-3.1-8B、RULER用LongChat-7b-v1.5-32k、AIME2025用DeepSeek-R1-Distill-Llama3-8Bを使用。比較対象はFull KV、Eigen-N、StaticPCA、Palu。OjaKVとプリフィルをフルランク化したOjaKV-PFを評価し、FlashAttention互換再構成を使う。
RULERでは16K入力でFull、0.8x、0.6xのキャッシュ予算を比較する。LongBenchでは単一/複数文書QA、few-shot、合成、codeなどをLlama-2-7BとLlama-3.1-8Bで評価する。AIME2025では長い推論生成を伴う蒸留R1モデルを用い、promptはフルランク保持しデコード生成の大半を圧縮する。補助的にlm-eval-harnessのWinoGrande、PiQA、HellaSwag、ARC-easy/challengeを測る。効率では32KまでのTTFT・GPUメモリ、更新間隔T=64/128/256のデコード遅延を測り、アブレーションでStaticPCA→Hybrid Storage→Hybrid+Onlineの寄与を分離する。
長文検索、長文理解、数学推論、一般多肢選択まで広く評価する一方、GPUはH100中心であり、低帯域GPUやCPUオフロード環境は対象外。0.8x/0.6xという低ランクキャッシュ比率が中心で、量子化との統合性能は主要表で測らない。実装は固定学習率、更新間隔、バッファ長、top-kを使い、モデルやタスクごとの自動調整は今後の課題とされる。
## 主要結果
OjaKVは静的低ランク基底が崩れやすい長文・非定常生成ほど効果が大きい。RULER 16Kでは0.6x キャッシュでStaticPCA平均23.44%に対し39.99%、プリフィルフルランク版は50.7%。AIME2025では静的圧縮群が0%になる中で13%を維持する。一般多肢選択では0.6xでもFull KVとほぼ同等の平均精度を保つ一方、オンライン更新によりデコード遅延は約10.9～13.4%増える。

- RULER平均精度 / 39.99%（OjaKV）、50.7%（OjaKV-PF） (比較対象: StaticPCA 23.44%、Full KV 74%; 条件: LongChat-7b-v1.5-32k、16K入力、0.6x キャッシュ) — 長文検索では混合保存と適応基底が静的低ランクより大幅に情報保持を改善する。

- AIME2025精度 / 13.0% (比較対象: Eigen-N/StaticPCA/Paluはいずれも0%、Vanilla 43.3%; 条件: DeepSeek-R1-Distill-Llama3-8B、長いデコード推論) — 生成中に意味分布が継続変化する推論では静的基底が完全崩壊する一方、オンライン追随は意味のある推論能力を残す。

- lm-eval平均精度 / Llama-3.1-8Bで69.18% (比較対象: Full KV 69.34%、StaticPCA 66.18%; 条件: 0.6x圧縮、WinoG/PiQA/HellaS/ARC-e/ARC-c) — 一般タスクでは40%のキャッシュ削減でもほぼ非圧縮精度を維持できる。

- 32K KVメモリ / 11.6GB (比較対象: Full KV 16GB; 条件: Llama-3.1-8B-Instruct、32K、論文表記60% compression設定) — 長文入力で主要ボトルネックとなるKV容量を4.4GB削減する。

- デコード遅延 / 40.44～41.38 ms/トークン (比較対象: Full KV 36.48、StaticPCA 36.60 ms/トークン; 条件: Oja更新間隔T=64～256) — オンライン適応は10.9～13.4%の計算オーバーヘッドを持ち、Tを広げるほど軽くなる。

### 負の結果・境界条件
- OjaKVはメモリ削減と品質を改善するが、32KのTTFTはFull KV 2102msから2801msへ増える。AIME2025も13%でVanilla 43.3%には大きく届かず、低ランク圧縮自体の限界は残る。LongBenchではRULERほど差が大きくなく、安定した長文理解では静的基底でも相対的に崩れにくい。固定間隔Oja更新は不要な位置でも計算する可能性があり、著者も再構成誤差スパイクに基づく動的更新を今後の課題とする。

### 結果の読み方
アブレーションではStaticPCA平均38.9%からHybrid Storageだけで57%、さらにOnline Ojaを加えると60%となり、最大の寄与は高誤差トークンをフルランク保持する混合保存にある。その上でオンライン更新が分布変化の大きい長期デコードで追加効果を与える。したがってOjaKVの強みは単なるオンラインPCAではなく、圧縮に不向きな外れトークンをアンカーとして残し、残りの低ランク部分だけを適応させる分業にある。
## 品質への影響
0.6x圧縮でもLlama-3.1-8Bのlm-eval平均69.18%はFull KV 69.34%に近い。LongBenchではLlama-3.1-8B 0.6xでStaticPCA 15.70に対しOjaKV 20.66、OjaKV-PF 28.46。RULERとAIMEのような長期・非定常文脈で改善幅が特に大きい。
## 既存研究との差
EigenAttention/StaticPCAは校正データから作った固定基底を全入力へ適用するが、OjaKVはプリフィルとデコードの現在活性から基底を継続更新する。Palu/ReCalKVのような重み分解型と違い、モデル重みや学習済み構造を変更せずKV表現側だけで導入できる。StreamingLLM/SnapKV等のトークン selectionはトークンを捨てるのに対し、OjaKVは大多数を低ランクで残し、高誤差トークンをフルランク保持するため情報削除の軸が異なる。論文は両者が直交し、トークン 追い出しとの併用でメモリ削減を乗算できると位置付ける。
## 限界
OjaKVは学習率、デコード更新間隔T、更新バッファ長、フルランク保持top-kなど固定ハイパーパラメータを持ち、モデルやタスクごとに調整が必要になり得る。Oja更新はSVD再計算より軽いが静的圧縮より計算負荷があり、実測デコード遅延は10.9～13.4%増える。再構成誤差は注意摂動と理論的関係を持つものの、全下流タスクでの意味的重要度を完全には表さない。主要ハードウェアはH100で、帯域・演算比の異なるGPUでの損益分岐は未評価である。
## 実装状態
Findings of ACL 2026採択済みで、著者公式GitHub実装が公開されている。標準FlashAttentionへ再構成K/Vを渡す経路を実装し、専用低ランクattention カーネルを必須としない。H100上で実際のTTFT、デコード 遅延、GPU メモリまで測定しており、精度だけのシミュレーションではない。
## 研究上の位置づけ
KVキャッシュ最適化系統では、OjaKVは『どのトークンを残すか』と『どの部分空間で圧縮するか』を同時に文脈適応させる低ランク圧縮研究である。特に静的校正基底が長いデコード中の分布移動へ追随できない点をオンラインPCAで解決し、長期推論やRULERのような動的文脈で改善幅が大きい。オフロードとは異なり転送先メモリを増やさずGPU上の表現次元を縮めるため、量子化・トークン 追い出し・CPUオフロードと組み合わせられる補完的な手法として位置付けられる。
## 一次資料
- https://aclanthology.org/2026.findings-acl.494/
- https://aclanthology.org/2026.findings-acl.494.pdf
