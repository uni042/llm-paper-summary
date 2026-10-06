---
canonical_id: "arXiv:2601.19139"
title: "Native LLM and MLLM Inference at Scale on Apple Silicon"
summary: "本論文はApple Siliconの統合メモリとMLXを直接利用するvllm-mlxを提案し、text LLMとmultimodal LLMを単一のnative runtimeでservingする。continuous batchingで16並列時にaggregate throughputを最大4.3倍へ拡大し、M4 Max上でllama.cpp比21〜87%高いtext throughput、最大525 token/sを示す。画像content hashに基づくmultimodal prefix cacheでは反復画像queryを最大28倍高速化し、21.7秒から1秒未満へ短縮する。"
list_summary: "Apple Silicon向けMLX native 推論提供にcontinuous batchingとマルチモーダル 接頭辞 キャッシュを組み込み、テキストと画像・動画LLM推論を統合メモリ上で高速化する。"
authors: ["Wayner Barrios"]
published: "2026-01-27"
publication: "arXiv"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2601.19139"
sources: ["https://arxiv.org/abs/2601.19139","https://github.com/waybarrios/vllm-mlx"]
implementation: "MLX nativeのvllm-mlxを公開し、Apple M4 MaxでQwen3-0.6BからNemotron-30Bまでのtext model、画像・動画multimodal modelを評価。continuous batching、content-based prefix cacheを実装する。"
code: "https://github.com/waybarrios/vllm-mlx"
last_checked: "2026-10-06"
arxiv_id: "2601.19139"
arxiv_categories:
  primary: "cs.LG"
  cross_list: ["cs.DC","cs.ET"]
worker_completed_at: "2026-10-06T14:31:00+09:00"
worker_run_key: "20261006-1400-scheduled-chat-00/r02"
reference_main_sha: "b00f07437b5d8606a5147906940d55cd23760a82"
last_audited: null
audit_version: 0
---

## 概要

Apple SiliconはCPU/GPUが同じ統合メモリを共有し、大容量MacではGPU専用VRAMを超えるモデルも局所実行できる。一方、PyTorch MPSはApple GPU専用の推論ランタイムではなく、llama.cppはテキスト中心で、複数リクエストをまとめるcontinuous batchingやマルチモーダル 接頭辞 再利用を一体化した推論提供機能が不足していた。

vllm-mlxはAppleのMLX上へLLM/MLLM 推論提供をnative実装し、テキストではcontinuous batching、マルチモーダルでは画像内容のhashに基づく接頭辞 キャッシュを導入する。M4 Max実測でテキストはllama.cppより21〜87%高いスループット、最大525 トークン/s、16 concurrent リクエストでaggregate スループット最大4.3倍を報告する。

## 問題設定

統合メモリは重みコピーを減らせても、1 リクエストずつデコードすればGPU 並列化を十分使えない。マルチモーダル モデルでは同じ画像をmulti-turnで再利用してもvision encoderを毎回実行すると、テキスト KV キャッシュだけを再利用しても前処理遅延が残る。

## 手法

### MLX native runtime

Metal向けに設計されたMLX テンソル/カーネル経路を使い、PyTorch→MPS変換層を避ける。Apple Siliconの統合メモリ上でモデル 重みとランタイム 状態を扱い、テキストとvision-language モデルを同じserverへ載せる。

### continuous batching

複数リクエストのデコードをiteration単位で同じバッチへ出し入れし、終了リクエストを待たず新しいリクエストを追加する。単一ストリームでは小さいmatrix-vector処理になりやすいデコードを、複数リクエストでまとめてGPU利用率を上げる。

### content-based multimodal prefix cache

画像の入力formatやpathではなく内容hashで同一画像を識別し、vision encoderのembeddingと関連接頭辞 状態をキャッシュする。同じ画像を再質問するmulti-turn ワークロードでは高価なvision encodingをスキップできる。動画でもframe由来の再利用を行う。

## 評価条件

|項目|条件|
|---|---|
|ハードウェア|Apple M4 Max|
|ランタイム|MLX native vllm-mlx|
|テキスト モデル|Qwen3-0.6B〜Nemotron-30B|
|比較|llama.cpp等|
|concurrency|最大16 リクエスト|
|マルチモーダル|反復画像問い合わせ、最大64 frame動画|
|指標|トークン/s、aggregate スループット、エンドツーエンド 遅延、キャッシュ 高速化倍率|

## 主要結果

テキスト モデルではllama.cpp比21〜87%高いスループットを示し、条件によって最大525 トークン/sへ達する。16 concurrent リクエストではcontinuous batchingによりaggregate スループットが最大4.3倍へ増える。

マルチモーダル 接頭辞 キャッシュは反復画像問い合わせを最大28倍高速化し、遅延を21.7秒から1秒未満へ短縮する。最大64 frameの動画解析でもキャッシュ利用時に24.7倍の高速化倍率を報告する。これはテキスト KVだけでなくvision encoder結果を再利用する効果を測ったものになる。

## 既存研究との差

llama.cppはApple Siliconを広く支援するが、論文時点の比較ではテキスト中心である。vllm-mlxはvLLM型のcontinuous batchingと接頭辞 キャッシュという推論提供機能をMLXへ移し、さらにimage/video encoder結果までキャッシュ対象へ拡張する。

## 限界

評価ハードウェアはM4 Max中心で、M1〜M5の全SoCやメモリ構成で同じ倍率を保証しない。llama.cpp比21〜87%はモデル依存で、現在のランタイム version間でも変化し得る。content キャッシュは同一画像の反復がないワークロードでは命中せず、hash管理分だけオーバーヘッドが残る。

## 一次資料

- https://arxiv.org/abs/2601.19139
- https://github.com/waybarrios/vllm-mlx