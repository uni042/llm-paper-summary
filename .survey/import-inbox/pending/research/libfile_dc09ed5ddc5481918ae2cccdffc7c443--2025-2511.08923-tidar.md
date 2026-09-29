---
canonical_id: "arXiv:2511.08923"
title: "TiDAR: Think in Diffusion, Talk in Autoregression"
summary: "TiDARは1つのモデル内でdiffusionによる並列draftとautoregressiveな確定生成を同一forward passに組み込み、structured attention maskで両者を接続するsequence-level hybrid architectureである。正確なKV cacheを維持しつつdraft用のGPU計算密度を高め、1.5B/8B評価でAR品質とのgapを閉じながらtokens/sを4.71〜5.91倍へ高める。"
list_summary: "拡散型の並列draftと自己回帰の確定生成をstructured attention maskで同一forwardへ統合し、正確なKV cacheを保ったままAR品質と高throughputを両立する。"
source: "https://arxiv.org/abs/2511.08923"
worker_completed_at: "2026-09-30T03:03:23+09:00"
worker_run_key: "20260930-0303-scheduled-chat-00"
reference_main_sha: "0f2cea8f5102b76f85583e41068ab8e20c7bf17a"
---

# TiDAR: Think in Diffusion, Talk in Autoregression

## 概要
拡散言語モデルは複数tokenを並列更新できるが、左から右へ条件付ける自己回帰（AR）モデルに比べ品質が落ちやすい。投機的復号はAR品質を保つ一方、小型draft modelが逐次tokenを作るためGPU計算密度が低く、draft自体が新たなserial pathになる。TiDARはこの二択をarchitecture内部で統合し、「考える」draft部分をdiffusion、「話す」確定部分をARとして一つのforward passで処理する。

structured attention maskにより、未確定領域は並列にdraftしながら、確定tokenは因果的に生成する。別draft modelを起動するのではなく同じモデル内の計算を密に使い、正確なKV cacheも保持する。1.5Bと8B規模でAR model、speculative decoding、Dream/LLaDA等のdiffusion modelと比較し、AR品質との差を閉じながら4.71〜5.91倍のtokens/sを報告する。

## 問題設定
純粋diffusionはmaskされた複数位置を並列復元できるが、どのtokenが先に確定するかや条件付けがARと異なり、likelihoodとgeneration qualityで不利になり得る。逆に通常のspeculative decodingではdraft modelが左から右へ候補を作るので、target GPUが余っていてもdraftのsequential latencyに待たされる。

TiDARはdraftを「小さいARモデル」に任せるのではなく、同一モデルの未確定位置をdiffusion的に並列更新し、その結果を同じforward内のAR samplingへ渡す。これによりverification capacityとdraft capacityを別モデルへ固定分割しない。

## 手法
### sequence-level hybrid
sequenceを確定済みAR領域と、並列に候補を作るdiffusion領域へ分ける。diffusion領域は複数位置を同時に更新し、AR領域は左から右の厳密な条件付けで最終tokenをsampleする。二つのmodeをstepごとに別modelとして切り替えるのではなく、一つのTransformer forwardに同居させる。

### structured attention mask
attention maskは確定prefixからdraft領域への情報伝播を許しつつ、最終AR tokenが未来の未確定情報を不正に参照しないよう依存関係を制御する。これにより並列draftの計算密度を上げても、AR側の因果性を維持する。

### exact KV cache
確定したAR tokenについて通常のKV cacheを形成できるよう設計されている。diffusion modelで問題になりやすい「複数位置を更新するたびに全sequenceを再計算する」費用を避け、serving runtimeでincremental decodeを継続できる。論文がstandalone serving-friendlyを強調する理由はここにある。

## 評価条件
|項目|内容|
|---|---|
|規模|1.5B、8B|
|比較|対応AR model、通常speculative decoding、Dream、LLaDA等diffusion LM|
|task|生成taskとlikelihood task|
|指標|tokens/s、生成品質、likelihood、KV cache適合性|
|実行|並列draft + AR samplingを同一forwardで実行|

## 主要結果
|結果|意味|
|---|---|
|AR比4.71〜5.91倍 tokens/s|並列draftが実測throughputへつながる|
|AR modelとの品質gapを閉じる|高速化を純diffusionの品質低下で得ていない|
|Dream/LLaDAより効率・品質で優位|単純なdiffusion decodeとの差を確認|
|speculative decodingより高throughput|sequential draft modelのcritical pathを削減|
|exact KV cache対応|長いserving decodeでprefix再計算を避けられる|

## 既存研究との差
通常の投機的復号はdraft modelとtarget modelを別々に走らせ、候補生成と検証を二段にする。TiDARはdraft/verificationの役割をsequence内のattention構造として一モデルへ埋め込む。純diffusion LMは全tokenを反復更新するが、TiDARは確定出力をARで生成して品質とKV cache互換性を得る。

## 限界
既存AR checkpointへ推論時だけ追加できるdecoderではなく、hybrid architectureとしての学習が必要である。4.71〜5.91倍は評価した1.5B/8Bとhardware/runtime条件での結果で、batch sizeやsequence長で変わる。structured maskとhybrid trainingを既存serving stackへ統合する実装負担も残る。

## 一次資料
- https://arxiv.org/abs/2511.08923
