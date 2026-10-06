---
canonical_id: "arXiv:2406.11816"
title: "VideoLLM-online: Online Video Large Language Model for Streaming Video"
summary: "VideoLLM-onlineは連続video streamを時間整合した対話へ変えるLIVE frameworkを提案し、frame入力の継続KV cache、視覚encoder・LLM frame forwarding・応答生成の非同期並列化で再計算と待ちを減らす。Llama-2/3系でA100 10–15 FPS、RTX 3090 5–10 FPSのreal-time streamingを報告する。"
list_summary: "連続frameのKV キャッシュと視覚encode・LLM処理・応答生成の非同期パイプラインにより、VideoLLMをoffline clip処理からreal-time ストリーム対話へ変える。"
authors: ["Joya Chen","Zhaoyang Lv","Shiwei Wu","Kevin Qinghong Lin","Chenan Song","Difei Gao","Jia-Wei Liu","Ziteng Gao","Dongxing Mao","Mike Zheng Shou"]
published: "2024-06-17"
publication: "IEEE/CVF Conference on Computer Vision and Pattern Recognition 2024"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/2406.11816"
sources: ["https://arxiv.org/abs/2406.11816","https://showlab.github.io/videollm-online/"]
implementation: "Llama-2/Llama-3を基盤にLIVE streaming modelを実装し、A100/RTX3090でFPS・memoryとoffline video benchmarkを評価。公式code/model/data/demo公開。"
code: "https://github.com/showlab/videollm-online"
last_checked: "2026-10-06"
arxiv_id: "2406.11816"
arxiv_categories: {primary: "cs.CV", cross_list: ["cs.CL"]}
worker_completed_at: "2026-10-06T06:51:00+09:00"
worker_run_key: "20261006-0630-scheduled-chat-30/r01"
last_audited: null
audit_version: 0
---
## 概要
従来のVideoLLMは完成済みclip全体を一括入力するoffline方式が中心で、camera ストリームへ逐次反応するには過去frameの再処理や、視覚encoderとLLM生成の速度差が問題になる。VideoLLM-onlineはLearning-In-Video-Stream（LIVE）として、入力中の時間位置に合わせて発話または沈黙を生成する学習形式とreal-time inference パイプラインを組み合わせる。

## 手法
学習dataは既存offline annotationをstreaming dialogueへ変換する。モデルはframe トークンが逐次到着する系列上でlanguage modelingを行い、イベントに対応する時点で応答し、発話すべきでない期間はsilenceを学ぶ。

推論では過去frameを毎回再順伝播せず、継続的なKey-Value（KV）キャッシュへ状態を保持する。frame トークン上でEOSを過剰予測するbiasを閾値で補正し、ストリームが進んでも不要な応答終了を抑える。

さらにvideo encoding、LLMによるframe forwarding、LLM response generationを非同期に並列化する。高速なvision側が低速なlanguage デコードを待って入力ストリームを止めない構成にすることで、実時間のframe処理率を上げる。

## 評価条件
|項目|条件|
|---|---|
|基盤モデル|Llama-2 / Llama-3系|
|GPU|NVIDIA A100、RTX 3090|
|ストリーム例|5分video|
|offline タスク|COIN、Ego4D LTA等|
|指標|FPS、メモリ、recognition/captioning/forecasting、streaming dialogue品質|

## 主要結果
公式projectではA100で10–15 FPS、RTX 3090で5–10 FPSを報告し、5分videoのstreaming dialogueをA100で平均10 FPS超で処理する。報告メモリは20GB未満である。offline ベンチマークでもrecognition、captioning、forecastingで競争力ある結果を維持する。

この速度は単一LLMのトークン/sではなく、video ストリームを何frame/sで取り込んで対話状態を更新できるかというシステム指標である。継続KV キャッシュと非同期パイプラインが、offline clip再処理との差を作る。

## 既存研究との差
offline VideoLLMが「clipを見終えてから質問に答える」のに対し、LIVEはストリーム中に時間整合した発話を生成する。単にframe数を減らすのではなく、学習 formatとinference パイプラインの双方をonline化する。

## 限界
視覚情報を強く圧縮するため細粒度の空間認識との交換条件がある。streaming dataの多くを既存annotationから合成しており、自然な長時間対話への一般化には追加検証が必要である。純テキスト LLM 推論提供のスループット最適化ではなく、video ストリーム固有のパイプライン研究である。