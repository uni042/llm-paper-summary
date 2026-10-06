---
canonical_id: "arXiv:2607.10987"
title: "[AAFLOW+] Stateful Operator Abstraction with Zero-Copy Distributed KV Cache Orchestration for Multi-Agent Workflows"
summary: "AAFLOW+はmulti-agent workflowの共有contextを各agentがtextから再prefillする無駄を、KV cacheを分散systemの第一級state objectとしてtransfer/fork/composition/evictionするstateflowへ置き換える。empirical hardware microbenchmarkでparameter化したcost modelではTTFT最大50.2倍、16-agent compute cost最大7.63倍、KV memory 1.72～6.10倍、throughput 7.74倍超の改善を示す。"
list_summary: "multi-agent workflowのKV キャッシュを明示的な分散状態 objectとしてzero-copy transfer・forkし、テキスト再プリフィルをネットワーク転送へ置換するstateful orchestration。"
authors: ["Arup Kumar Sarker","Alexander James Halpern","Mills Staylor","Aymen Alsaadi","Gregor von Laszewski","Yue Cheng","Shantenu Jha","Geoffrey Fox"]
published: "2026-07-13"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2607.10987"
sources: ["https://arxiv.org/abs/2607.10987"]
implementation: "Mistral-7B/Llama-3-8B等を想定したagent workflowを、empirical hardware microbenchmarkでparameter化したanalytical cost modelで評価。UCX/MPI型zero-copy transportとvLLM/SGLang backend integrationを設計。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2607.10987"
arxiv_categories: {primary: "cs.DC", cross_list: []}
worker_completed_at: "2026-10-06T15:57:00+09:00"
worker_run_key: "20261006-1530-scheduled-chat-30/r02"
reference_main_sha: "0bbe57b3f448170074d516761dd9f8c955981e5e"
last_audited: null
audit_version: 0
---
## 概要
複数LLM agentが同じ長いdocumentやプロンプト 接頭辞を共有しても、通常のテキスト-centric workflowではagentごとにテキストを受け取り、同じ接頭辞を再びプリフィルしてKV キャッシュを作り直す。AAFLOW+はテキストだけをworkflow edgeで渡すのではなく、既に計算したKV 状態自体を分散ノード間で再利用する「状態流（stateflow）」を導入する。

## 問題設定
局所 接頭辞 キャッシュは同一推論提供 instance内では効くが、agent graphが複数ノードへ跨がると状態の所在、互換性、転送、fork、追い出しをworkflow ランタイムが扱えない。長文脈ではプリフィル時間がTTFTを支配する一方、KV テンソル自体も大きいため、ネットワークが遅い場合は転送より再計算の方が安い。この境界をスケジューラが判断する必要がある。

## 手法
AAFLOW+のstateful 演算子は通常のdata 入力/出力に加えて入力/出力 状態と状態 policyを持つ。workflow graphにはテキスト/JSONのdata edgeとKV-状態 edgeを別に表現し、コンパイラがmaterialize、transfer、fork、composition、追い出し 演算子を挿入する。

KV 状態 objectはモデル ID、tokenizer/モデル configuration、KV ブロック、position metadata、lineage、配置/ownershipを保持する。モデルやpositionが互換でない状態を誤再利用しないcompatibility checkを行い、条件を満たさなければテキスト再プリフィルへfallbackする。

分岐workflowでは共有接頭辞を一度materializeし、copy-on-write型に複数agentへforkする。ノード間転送はCPU serializationを避けるzero-copy data pathを使い、受信側backendへKVをinjectしてプリフィルをスキップする。

スケジューラは `KV size / bandwidth + transfer overhead` と局所 プリフィル コストを比較し、transferが安い場合だけstateflowを選ぶ。したがって低帯域ネットワークで巨大KVを無条件に送る方式ではない。

## 評価条件
|項目|内容|
|---|---|
|モデル例|Mistral-7B、Llama-3-8B|
|workflow|multi-agent debate、Tree-of-Thought等のbranching agent workflow|
|比較|テキスト再プリフィル、局所 接頭辞-キャッシュ系|
|ネットワーク|10～100 Gbps級を含む帯域感度|
|評価方式|ハードウェア マイクロベンチマークでパラメータ化したanalytical コスト モデル|
|指標|TTFT、aggregate compute コスト、KV メモリ、スループット|

## 主要結果
長文脈ではTTFTを最大50.2倍短縮し、16-agent規模でaggregate compute コストを最大7.63倍削減する。共有ブロックとforkによりKV メモリ footprintは1.72～6.10倍削減し、スループットは7.74倍超改善する。

ネットワーク感度では100 Gbps以上で有意な文脈なら状態 transferがほぼ常に有利となり、10 Gbpsでも数千トークンを超えるとtransferが再計算を上回る領域が現れる。これは「KV共有は常に速い」ではなく、文脈長と帯域のcross-overをコスト モデルで選ぶ設計を裏付ける。

## 既存研究との差
vLLMのPagedAttentionやSGLangのRadixAttentionは主に局所 推論提供 scopeでKVを管理する。KVCOMMもagent間KV 通信を扱うが、AAFLOW+はworkflow コンパイラから状態 lifecycle、fork、配置、追い出しまでを演算子 abstractionへ持ち上げ、agent graph全体をoptimization対象にする。

## 限界
headline値は完全な大規模production deploymentのエンドツーエンド実測ではなく、実機マイクロベンチマークでパラメータ化したanalytical コスト モデルに基づく。この点は50.2倍等の値をproduction実測として解釈してはいけない。KV transferはネットワーク 帯域とモデル/position compatibilityに依存し、低帯域や短接頭辞では再プリフィルの方が有利になり得る。