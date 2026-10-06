---
canonical_id: "arXiv:2603.24517"
title: "AVO: Agentic Variation Operators for Autonomous Evolutionary Search"
summary: "AVOは進化探索のmutation/crossoverを固定演算ではなく自律coding agentへ置換し、系譜・CUDA/PTX知識・実行feedbackを参照しながらGPU kernelを反復修正する。B200上で7日間のmulti-head attention探索によりcuDNN比最大3.5%、FlashAttention-4比最大10.5%高速なkernelを発見し、30分の追加適応でgrouped-query attentionでも最大7.0%/9.3%上回る。"
list_summary: "進化探索のvariation 演算子自体をcoding agent化し、プロファイリング・修正・検証ループからBlackwell向け注意機構 カーネルを自律探索する。"
authors: ["Terry Chen","Zhifan Ye","Bing Xu","Zihao Ye","Timmy Liu","Ali Hassani","Tianqi Chen","Andrew Kerr","Haicheng Wu","Yang Xu","Yu-Jung Chen","Hanfeng Chen","Aditya Kane","Ronny Krashinsky","Ming-Yu Liu","Vinod Grover","Luis Ceze","Roger Bringmann","John Tran","Wei Liu","Fung Xie","Michael Lightstone","Humphrey Shi"]
published: "2026-03-25"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2603.24517"
sources: ["https://arxiv.org/abs/2603.24517"]
implementation: "NVIDIA B200上のBF16 attention forward kernelを対象に7日間の自律進化を行い、cuDNN/FlashAttention-4とthroughput比較。"
code: "https://github.com/coder-2011/avo"
last_checked: "2026-10-06"
arxiv_id: "2603.24517"
arxiv_categories: {primary: "cs.LG", cross_list: []}
worker_completed_at: "2026-10-06T20:52:00+09:00"
worker_run_key: "20261006-2030-scheduled-chat-30/r01"
reference_main_sha: "a25363d27abaad5f4abefbac377726381dff8648"
last_audited: null
audit_version: 0
---
## 概要
GPU カーネル最適化はハードウェア document、profiler、correctness test、microarchitecture理解を何度も往復する。従来のLLM-in-the-loop進化探索ではLLMは候補生成の一工程に留まり、外側のフレームワークがmutation、評価、選択を固定手順で制御する。AVOはvariation 演算子そのものを自律coding agentへ置換する。

## 問題設定
FlashAttention-4やcuDNNのような成熟カーネルを超えるには、単発のコード生成ではなく、失敗を診断してPTX/CUDA実装を何度も修正する必要がある。固定mutation 演算子はこの意味的・ハードウェア依存の探索を表現しにくい。

## 手法
AVO agentは現在のcandidate lineage、CUDA/PTXやBlackwellに関するdomain-specific knowledge base、コンパイラ/error/profiler/スループット feedbackへアクセスする。過去候補を調べ、変更を計画し、実装し、correctnessと速度を測り、失敗やregressionなら自分で修正する。

進化フレームワークは候補集団とスコアを管理するが、親から次候補をどう変えるかというvariationはagentへ委ねる。これにより複数段階のdebuggingや複数ファイルに跨る最適化を一つのvariationとして実行できる。

## 評価条件
|項目|内容|
|---|---|
|GPU|NVIDIA Blackwell B200|
|カーネル|multi-ヘッド 注意機構 順伝播、grouped-問い合わせ 注意機構|
|datatype|BF16|
|比較|cuDNN、FlashAttention-4|
|探索時間|MHA 7日、GQA追加適応約30分|
|指標|TFLOPS/スループット、correctness|

## 主要結果
multi-ヘッド 注意機構では評価構成全体でcuDNNを最大3.5%、FlashAttention-4を最大10.5%上回る。代表的なcausal プリフィルでは16 heads、ヘッド dimension 128、総32K トークンの条件で4K 系列時に1392 TFLOPSに達し、cuDNN 1344、FA4 1259を上回る。

得られた最適化をgrouped-問い合わせ 注意機構へ移す際は約30分の追加自律適応で、cuDNN比最大7.0%、FlashAttention-4比最大9.3%の改善を報告する。

## 既存研究との差
AlphaEvolve型のLLM利用ではホスト側がvariation workflowを強く規定する。AVOは候補の調査、実装、プロファイリング、修正、検証までをagent内部loopへ入れ、LLMを「候補generator」から「variation 演算子」へ昇格させる。

## 限界
主要結果は単一lineage・7日間のB200 注意機構 順伝播探索で、エンドツーエンド LLM 推論提供速度ではない。比較は同一カーネル ベンチマーク上のcuDNN/FA4であり、他のagentic search手法との同条件比較は限定的である。発見した最適化の個別寄与も完全には分離されていない。