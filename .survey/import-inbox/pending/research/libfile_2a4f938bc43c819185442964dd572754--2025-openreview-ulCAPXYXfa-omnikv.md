---
canonical_id: "OpenReview:ulCAPXYXfa"
title: "OmniKV: Dynamic Context Selection for Efficient Long-Context LLMs"
authors: ["Jitai Hao", "Yuke Zhu", "Tian Wang", "Jun Yu", "Xin Xin", "Bo Zheng", "Zhaochun Ren", "Sheng Guo"]
published: 2025
publication_status: "ICLR 2025"
summary: "OmniKVは長文脈推論で現在stepのattention scoreに基づきKVを永久削除すると、後続stepで重要になるtokenを失う問題を避けるため、全KVをCPU側へ保持したままGPU上では動的に選択したcontextだけを使う。少数のfilter layerがfull attentionからTop-K tokenを選び、連続する非filter layerは層間attention類似性を利用して同じindexを再利用し、packed loadと非同期転送でCPU→GPU通信を隠蔽する。Llama-3-8Bの単一A100最大contextを128Kから450Kへ拡張し、性能損失なしで1.68倍高速化、offload時GPU KVメモリ最大75%削減を報告する。"
list_summary: "全KVをCPUに残し、少数filter layerが選んだ重要token indexを後続層で共有してGPUへ必要KVだけ転送する、token非破棄型の長文脈推論。"
source: "https://openreview.net/forum?id=ulCAPXYXfa"
worker_completed_at: "2026-09-30T06:00:15+09:00"
worker_run_key: "20260930-0600-scheduled-chat-00"
reference_main_sha: "8809ea0a9d371b2eb0779d7d488085499bcb601b"
---

# OmniKV: Dynamic Context Selection for Efficient Long-Context LLMs

## 概要
長文脈LLMではKVキャッシュがGPUメモリを占有する。H2O系の削除方式は現在のattentionから不要tokenを捨てるが、現在重要でないtokenが将来の生成stepで重要になる可能性があり、一度捨てると回復できない。OmniKVはtokenを永久削除せず、全KVをCPU側に保持しながら、そのstepで必要な部分だけをGPUへ動的に読み込む。

鍵となる観測は、同一生成step内の連続Transformer層で高attention tokenの集合が似ることにある。そこで一部のfilter layerだけがfull attentionを計算してTop-K indexを選び、後続の複数層は同じindexを再利用する。これにより各層で選択処理を繰り返さず、KV転送も層を跨いでまとめられる。

## 問題設定
CPU offloadはGPU容量を節約できる一方、各層が異なるtokenを要求するとPCIe上の小さな不規則転送が増える。KV evictionは転送を減らせるが情報を不可逆に失う。OmniKVは「保持」と「そのstepで計算に使う集合」を分離し、将来必要になったtokenを再び選択可能にする。

## 手法
プリフィルでは完全なKVを生成し、filter layer等の必要部分を除いてCPUへoffloadする。デコードではfilter layerがfull attentionを行い、現在stepで重要なTop-K token indexをContext Selectorが抽出する。

後続の非filter layerは層間類似性を前提に同じindexのKVだけをCPUから読み、疎attentionを計算する。複数層が同じindexを共有するため、packed loadでまとめて転送できる。さらにGPU計算と次層KV転送を非同期に重ね、PCIe待ちを隠す。待ち時間が大きい箇所では一部層をGPUに完全保持して転送完了までのbufferとして使う。

## 評価条件
|項目|内容|
|---|---|
|代表モデル|Llama-3-8B / 70B系|
|GPU|単一NVIDIA A100を含む評価|
|ランタイム|Hugging Face Transformers、LightLLM実装|
|ベンチマーク|LongBench、InfiniteBench、CoT系評価|
|比較観点|品質、context上限、KV GPUメモリ、推論速度|
|学習|追加訓練なし|

## 主要結果
ICLR 2025論文は、性能損失なしの条件で最大1.68倍の推論高速化を報告する。offloadと組み合わせたGPU上KVメモリは最大75%削減された。単一A100上のLlama-3-8Bでは最大context長が128Kから450Kへ伸び、約3.5倍のcontextを扱える。

特にCoTのように生成途中で過去tokenの重要度が変化しやすい条件で、永久evictionしない設計が有利になる。実装はLightLLMのtensor parallelにも対応し、単一の研究用attention関数だけでなくserving runtime上でも評価されている。

## 既存研究との差
H2O等は重要度の低いKVを破棄して物理キャッシュ自体を縮小する。OmniKVは全tokenのKVを低速側に保持し、計算対象だけを毎step変えるため情報損失を回避する。各層独立のsparse attentionとも異なり、filter layerで得たindexを連続層へ共有し、選択overheadとPCIe転送を同時に減らす。

## 限界
CPU側には完全KVを保持するため、総メモリ量そのものを4分の1にする方式ではなく、主にGPU常駐量を削る。性能は層間attention類似性とPCIe転送を計算で隠せることに依存する。公開実装では対応モデルやfilter layer設定が限定され、別アーキテクチャでは選択層・Top-K率・待機層数などの再調整が必要になる。

## 一次資料
- https://openreview.net/forum?id=ulCAPXYXfa
- https://proceedings.iclr.cc/paper_files/paper/2025/hash/da1131a86ac3c70e0b7cae89c3d4df22-Abstract-Conference.html