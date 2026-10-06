---
canonical_id: "arXiv:2509.17765"
title: "Qwen3-Omni Technical Report"
summary: "Qwen3-OmniはThinkerとTalkerの双方を混合専門家モデル（MoE）化し、音声・画像・動画・テキストを単一モデルで理解しつつ、multi-codebook codecと軽量Code2Wavにより低遅延のストリーミング音声生成を行う。30B-A3B Thinkerと3B-A0.3B Talkerを用い、単一同時実行の理論first-packet latencyは音声234 ms、動画547 msである。"
list_summary: "Thinker–TalkerをMoE化し、非同期chunked プリフィルとmulti-codebook音声codec、軽量ConvNetを組み合わせて高同時実行・低遅延の統合マルチモーダル推論を実現する。"
authors: ["Jin Xu","Zhifang Guo","Hangrui Hu","Yunfei Chu","Xiong Wang","Jinzheng He","Yuxuan Wang","Xian Shi","Ting He","Xinfa Zhu","Yuanjun Lv","Yongqi Wang","Dake Guo","He Wang","Linhan Ma","Pei Zhang","Xinyu Zhang","Hongkun Hao","Zishan Guo","Baosong Yang","Bin Zhang","Ziyang Ma","Xipin Wei","Shuai Bai","Keqin Chen","Xuejing Liu","Peng Wang","Mingkun Yang","Dayiheng Liu","Xingzhang Ren","Bo Zheng","Rui Men","Fan Zhou","Bowen Yu","Jianxin Yang","Le Yu","Jingren Zhou","Junyang Lin"]
published: "2025-09-22"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2509.17765"
sources: ["https://arxiv.org/abs/2509.17765"]
implementation: "Qwen3-Omni-30B-A3B系を公開し、vLLM上でtorch.compileとCUDA Graphを用いた同時ストリーミング推論を評価。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2509.17765"
arxiv_categories: {primary: "cs.CL", cross_list: ["cs.AI","cs.CV","cs.SD"]}
worker_completed_at: "2026-10-06T15:39:00+09:00"
worker_run_key: "20261006-1530-scheduled-chat-30/r01"
reference_main_sha: "0bbe57b3f448170074d516761dd9f8c955981e5e"
last_audited: null
audit_version: 0
---
## 概要
Qwen3-Omniはテキスト、画像、動画、音声の理解とリアルタイム音声生成を一つのモデル系列へ統合する。推論システム上の中心課題は、長い音声・動画を取り込むプリフィル（プリフィル）と、テキストおよび音声codecの逐次生成を同時に低遅延化し、同時要求数が増えても応答開始を極端に遅らせないことである。

## 問題設定
従来のQwen2.5-Omniでは音声生成にブロック-wise diffusionを使い、Talkerが十分なブロック 文脈を生成するまでwaveform synthesisを開始できなかった。さらにマルチモーダル入力ではencoder、Thinker、Talkerが順番に動くと最初の出力までの待ち時間が加算される。Qwen3-Omniはモデル 構成そのものを推論提供特性に合わせて変更する。

## 手法
Thinkerはテキスト生成、Talkerはストリーミング音声トークン生成を担い、双方を混合専門家モデル（Mixture-of-Experts; MoE）にする。30B-A3B Thinkerは総パラメータ約30Bのうちトークンごとに約3Bを活性にし、Talkerは3B-A0.3Bである。密 モデルより活性 重みを抑え、長系列でKVキャッシュI/Oが支配する状況でも高い同時実行性を狙う。

音声encoderのAuTは20 million hoursの教師付き音声で学習し、入力を12.5 Hzまでdownsampleする。1～8秒の動的windowを持つFlashAttentionを用いて、offline精度とreal-time プリフィル キャッシュの両立を図る。

入力側ではchunked prefillingを行う。Thinkerが現在chunkのプリフィルを終えると、その高位表現をTalkerへ渡してTalkerのプリフィルを非同期に開始し、Thinker自身は次chunkへ進む。この重なりで最初のトークンまでの時間を短縮する。

出力側ではTalkerが1 段階でcodec frameの第0 codebookを予測し、80M パラメータのmulti-トークン 予測 moduleが残りのresidual codebookを固定段階で生成する。200M パラメータのCode2Wavは従来のdiffusion vocoderではなく因果ConvNetで、1 codec frameができた時点からwaveformを生成できる。12.5 Hzなので1 frameは80 msの音声に対応する。

## 評価条件
|項目|内容|
|---|---|
|主モデル|Thinker 30B-A3B、Talker 3B-A0.3B|
|補助module|MTP 80M、Code2Wav 200M|
|ランタイム|vLLM、torch.compile、CUDA Graph|
|同時実行|1 / 4 / 6 audiovisual ストリーム|
|主要指標|first-packet 遅延、トークン/s、real-time factor、36 audio/audio-visual ベンチマーク|

## 主要結果
単一同時実行では理論エンドツーエンド first-packet 遅延が音声234 ms、動画547 msである。4同時では728/1517 ms、6同時では1172/2284 msへ増える。したがってMoE化しても同時実行増加の影響は消えず、特にThinker/Talkerの最初のトークン待ちが増える。

生成real-time factorは同時実行1/4/6で0.47/0.56/0.66と1未満を保ち、生成開始後は実時間より速く音声を供給できる。Thinkerの生成速度は75→63→53 トークン/s、Talkerは140→125→110 トークン/sへ低下する。

品質面では36のaudio/audio-visual ベンチマーク中32でopen-source SOTA、22でoverall SOTAを報告する。低遅延化だけのモデルではなく、同規模Qwen単一modality モデルに対するテキスト/vision性能低下を抑えた点も設計上重要である。

## 既存研究との差
Qwen2.5-Omniのブロック-wise DiTによるwaveform生成を、multi-codebook autoregressive codecと軽量causal ConvNetへ置換することで、ブロック完成待ちをなくした。ThinkerとTalkerを別々の密 モデルにせず双方をMoE化し、chunked プリフィルの非同期実行まで含めて推論提供向けに共同設計している。

## 限界
234 msは論文の典型計算資源を前提にした理論遅延で、ネットワークやqueueingを含む全production環境の保証値ではない。6同時ではfirst-packet 遅延が1秒を超え、concurrencyの影響は残る。音声・動画統合モデル固有の構成であり、一般的テキスト-only LLMへそのまま適用する推論ランタイム手法ではない。