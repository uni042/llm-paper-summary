---
canonical_id: "arXiv:2503.20215"
title: "Qwen2.5-Omni Technical Report"
summary: "Qwen2.5-Omniはtext・image・audio・videoを逐次入力しtextとspeechを同時生成する7B級end-to-end multimodal modelで、block-wise audio/vision encoder、時間整合TMRoPE、Thinker-Talker分離、sliding-window DiTを組み合わせてstreaming入出力を実現する。推論効率の主眼は初回音声packet遅延を抑えるstreaming設計であり、論文は包括的なGPU latency/throughput benchmarkは提示しない。"
list_summary: "ブロック-wise マルチモーダル入力とThinker-Talker、sliding-window音声decoderを組み合わせ、テキスト理解とspeech生成を同時streamingするエンドツーエンド omni モデル。"
authors: ["Jin Xu","Zhifang Guo","Jinzheng He","Hangrui Hu","Ting He","Shuai Bai","Keqin Chen","Jialin Wang","Yang Fan","Kai Dang","Bin Zhang","Xiong Wang","Yunfei Chu","Junyang Lin"]
published: "2025-03-26"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2503.20215"
sources: ["https://arxiv.org/abs/2503.20215", "https://github.com/QwenLM/Qwen2.5-Omni"]
implementation: "Qwen2.5-Omni-7Bをtext/image/audio/video理解とstreaming speech generationで評価し、公式model・推論実装をQwenLMから公開。"
code: "https://github.com/QwenLM/Qwen2.5-Omni"
last_checked: "2026-10-06"
arxiv_id: "2503.20215"
arxiv_categories: {primary: "cs.CL", cross_list: ["cs.CV","cs.SD","eess.AS"]}
worker_completed_at: "2026-10-06T07:50:00+09:00"
worker_run_key: "20261006-0730-scheduled-chat-30/r01"
last_audited: null
audit_version: 0
---
## 概要
Qwen2.5-Omniは、テキスト、image、audio、videoを同一モデルで理解し、テキストと自然音声をstreaming生成するエンドツーエンド マルチモーダル モデルである。単に複数modal encoderをLLMへ接続するだけでなく、入力ストリームの時間関係を保ちながら、理解用のThinkerと音声生成用のTalkerを同時進行させることを狙う。

推論効率の観点では、audio/vision encoderをブロック-wise処理して入力完了を待たずプリフィルを進め、speech decoderにはsliding-window Diffusion Transformer（DiT）を用いて初回packet遅延を抑える。したがって本論文の効率性は最大スループットより「リアルタイムに近い逐次入出力を成立させる構成」にある。

## 問題設定
offline マルチモーダル モデルではvideo/audio全体を受信してからencode・推論を始められるが、会話では入力が継続到着する。全入力待ちでは応答開始が遅れ、audioとvideoを別々の位置系列として扱うと同じ実時間に起きた事象の整合も崩れる。

またテキスト reasoningとspeech generationを1本の自己回帰列へ混在させると、音声トークン生成がlanguage reasoningを圧迫し得る。高品質な音声生成に拡散モデルを使う場合も、全履歴へ広いreceptive fieldを持たせるとstreamingの最初のpacketが遅くなる。

## 手法
入力側ではaudio encoderとvision encoderをブロック-wiseに動かす。audioは一定時間ブロックで処理し、video frameも逐次特徴化するため、長いストリームの終端を待たずにThinkerへトークンを送り込める。これはoffline一括encodeに対する待ち時間を減らす。

Time-aligned Multimodal Rotary Position Embedding（TMRoPE）は、audioとvideoの位置を単なるトークン indexではなく時間軸で整合させる。audio/videoをinterleaveして同じ実時間の情報が対応する位置表現を持つため、長いストリームでmodalities間の同期を保持する。

Thinker-Talker 構成では、Thinkerがマルチモーダル理解とテキスト generationを担い、TalkerはThinkerの隠れ 表現を直接受け取ってaudio codec トークンを生成する。Talkerはdual-track autoregressive構造で、テキスト reasoningとspeech generationを分離しつつ共有表現で同期する。

speech waveform側ではsliding-window DiTを使い、拡散decoderのreceptive fieldを局所windowへ制限する。全過去audio トークンを毎回広く参照しないため、streaming デコードで最初の音声packetを出すまでの待ちを減らす設計になっている。

## 評価条件
|観点|内容|
|---|---|
|モデル|Qwen2.5-Omni-7B|
|入力|テキスト、image、audio、video|
|出力|テキスト + streaming speech|
|理解評価|OmniBench、MMLU、GSM8K等|
|音声評価|自然性・robustnessを既存streaming/non-streaming方式と比較|
|効率評価|streaming設計を提示するが包括的なGPU TTFT/スループット表はなし|

## 主要結果
OmniBenchではQwen2.5-Omni-7BがSpeech 55.25%、Sound Event 60.00%、Music 52.83%、aggregate 56.13%を報告し、表中の他omni モデルより高いaggregateを示す。speech instruction followingでもテキスト入力時に近いMMLU/GSM8K能力を保つ。

一方、推論効率について論文はブロック-wise encoderとsliding-window DiTがstreamingを可能にし初回packet遅延を減らす設計意図を説明するが、初回packet 遅延の絶対値や通常decoderとの速度倍率を主要表としては報告していない。したがって本サーベイでは「streaming inference 構成」の事例として扱い、未報告の速度値を補わない。

## 既存研究との差
従来のaudio/video LLMが特定modalitiesやテキスト出力へ分かれるのに対し、Qwen2.5-Omniは同一モデルで時間同期したマルチモーダル 入力とテキスト/speech同時出力をエンドツーエンド化する。Thinker-Talker分離により、language reasoningとaudio トークン generationの役割を明確に分ける。

## 限界
論文の主眼はマルチモーダル能力で、LLM 推論提供 システムとしてのGPU メモリ、バッチ スループット、TTFT、TPOT、同時セッション数は詳細評価していない。streaming部品の個別ablationも限定的で、sliding-window DiTが遅延をどれだけ削減したかを単独の定量値として切り出せない。