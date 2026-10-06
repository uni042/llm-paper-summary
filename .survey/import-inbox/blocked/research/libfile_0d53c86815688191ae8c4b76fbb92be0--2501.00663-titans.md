---
canonical_id: "arXiv:2501.00663"
title: "Titans: Learning to Memorize at Test Time"
summary: "Titansはattentionを短期記憶、入力に応じて推論時にも更新される深いニューラルmemoryを長期記憶として組み合わせる。surpriseに基づくmemory update、momentum、forgettingを導入し、Memory as Context/Gate/Layerの3構成を提示する。言語モデル等でTransformerや線形再帰モデルを上回り、needle-in-haystackでは2M token超へscaleする。"
list_summary: "入力のsurpriseを用いて推論中に更新するニューラル長期メモリを注意機構と統合し、固定window外の情報をparameterized メモリへ記憶・検索する。"
authors: ["Ali Behrouz","Peilin Zhong","Vahab Mirrokni"]
published: "2024-12-31"
publication: "NeurIPS 2025"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/2501.00663"
sources: ["https://arxiv.org/abs/2501.00663"]
implementation: "340M～760M級を含む複数規模でlanguage modeling、common-sense reasoning、genomics、time series、long-context retrievalを評価。一次資料から公式コードURLは確認できず。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2501.00663"
arxiv_categories: {primary: "cs.LG", cross_list: ["cs.AI","cs.CL"]}
worker_completed_at: "2026-10-06T15:45:00+09:00"
worker_run_key: "20261006-1530-scheduled-chat-30/r01"
reference_main_sha: "0bbe57b3f448170074d516761dd9f8c955981e5e"
last_audited: null
audit_version: 0
---
## 概要
Transformerの注意機構は過去トークンを直接参照できるため正確だが、文脈を保持するほどKV メモリと注意機構計算が増える。RNNや状態-space モデルは履歴を固定状態へ圧縮できる一方、何を忘れるべきかを固定更新則で決める。Titansは長期メモリ自体を小さなneural ネットワークとし、現在入力から得た驚き（surprise）を使って推論中にもそのパラメータを更新する。

## 問題設定
長い文脈を全て注意機構へ置く方式では二乗計算または巨大KV キャッシュが必要になる。一方、固定サイズ状態は古い情報を不可逆に混ぜやすい。Titansは短期の精密参照を注意機構へ任せ、長期情報を別メモリへ圧縮し、必要時に問い合わせで取り出す役割分担を行う。

## 手法
ニューラルメモリはkey/valueを受け取り、現在メモリがvalueをどれだけ予測できなかったかをloss 勾配で測る。この勾配 magnitudeをsurprise signalとして、予測しにくい情報ほど強くメモリへ書き込む。単純な1-段階 勾配 descentではなく、過去のsurpriseを蓄積するモーメンタムと、古いメモリを減衰させるforgetting ゲートを持つ。

Memory as Context（MAC）は長期メモリから取り出した表現をpersistent メモリ トークンと現在segmentへ連結し、注意機構の文脈として使う。Memory as Gate（MAG）は注意機構 分岐とメモリ 分岐を並列に計算し、ゲートで混合する。Memory as Layer（MAL）はneural メモリを注意機構とは別層として直列に配置する。

推論時更新をトークン単位で完全逐次実行すると遅いため、メモリ 更新をchunk単位で並列化できる定式化を用いる。これにより「推論中に学習するメモリ」でありながらGPU並列性を残す。

## 評価条件
|項目|内容|
|---|---|
|構成|MAC / MAG / MAL + neural long-term メモリ|
|規模|約340M、760M等|
|比較|Transformer、Mamba等のmodern linear recurrent モデル|
|タスク|language modeling、common-sense reasoning、genomics、time series、探索対象-in-haystack|
|長文脈|2M トークン超まで評価|

## 主要結果
language modelingとcommon-sense reasoningでは複数のTransformer/linear recurrent 比較対象を上回り、340M級の代表値ではMAC パープレキシティ 25.43、平均accuracy 47.36、MAG 25.07/47.54、MAL 24.69/46.55を報告する。

長文脈では探索対象-in-haystack型タスクを2M トークン超へscaleし、比較対象より高い検索 accuracyを維持する。これは全履歴を注意機構 KVとして残すのではなく、長期メモリ パラメータへ圧縮して参照する設計が長さ拡張へ寄与することを示す。

## 既存研究との差
Mamba等は固定形式のrecurrent 状態を更新するのに対し、Titansはmulti-層 neural ネットワーク自体をtest timeに学習する。RAGのように外部vector databaseへ文書を保存する方式とも異なり、系列処理中のinternal メモリ パラメータへ情報を圧縮する。

## 限界
メモリ 更新にも計算コストがあり、長文脈で常に通常注意機構より実時間で速いことを保証する研究ではない。2M トークン結果は主に検索能力のscale評価で、production 推論提供の同時要求・TTFT・TPOT評価ではない。メモリを推論中に更新するため、通常のstateless 推論提供よりリクエスト 状態管理も複雑になる。