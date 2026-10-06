---
canonical_id: "arXiv:2601.05109"
title: "Nalar: Workflow-Aware Management of Agentic Applications"
summary: "NalarはエージェントのPython制御フローを保ったまま、agent/tool呼出しを依存関係付きfutureへ変換し、workflow全体をruntimeから観測・制御できるserving基盤である。管理state層、workflow-aware KV cache、global/local二段制御を組み合わせ、3 workloadでtail latencyを34～74%削減し、最大3.38倍の高速化を示す。"
list_summary: "エージェントworkflowを依存関係付きfutureとして可視化し、KV配置・ルーティング・スケジューラ・状態管理をworkflow単位で協調制御する推論提供基盤。"
authors: ["Saurabh Agarwal","Marco Laju","Donghyun Son","Nitin Kedia","Myungjin Lee","Jayanth Srinivasa","Aditya Akella"]
published: "2026-01"
publication: "arXiv preprint"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2601.05109"
sources: ["https://arxiv.org/abs/2601.05109"]
implementation: "3種類のagentic workloadでtail latency、throughput、control-plane scalabilityを評価。workflow-aware KV-cacheと二段制御を含むserving runtime。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2601.05109"
arxiv_categories: {primary: "cs.DC", cross_list: ["cs.MA"]}
worker_completed_at: "2026-10-06T12:42:00+09:00"
worker_run_key: "20261006-1230-scheduled-chat-30/r01"
last_audited: null
audit_version: 0
---
## 概要
LLMエージェントは一つのリクエストが複数のモデル call、tool、分岐、retry、長寿命状態をまたぐ。通常のLLM 推論提供は個々のモデル リクエストだけを見て最適化するため、次にどのagentが動くか、どのKV キャッシュやtool 状態が再利用されるかをworkflow全体から判断できない。Nalarはアプリ記述とランタイム実行を分離しつつ、通常のPython制御フローを保ったままworkflow情報を推論提供側へ露出する。

## 手法
開発者が呼ぶagent/tool interfaceは自動生成stubへ置換され、実呼出しではなくfutureを返す。futureは依存関係とexecution 文脈を持つため、ランタイムはDAGを事前に固定しなくても、実行中に現れたworkflow構造を追跡できる。モデル-drivenな条件分岐やtool結果依存の経路もPython側に残せる。

管理状態層はlogical 状態と物理配置を分離する。これによりretry時の整合性を保ちながら状態の再利用・migrationを行える。KV キャッシュについてもworkflow-awareな管理を行い、単一リクエストのLRUだけでなく将来のworkflow利用を考慮して配置とlifetimeを扱う。

制御は大域 policy computationと局所 event-driven enforcementの二段構成である。大域側はworkflowを横断してルーティング・スケジューラ・資源 policyを決め、局所側はfuture完了などのeventに応じて低遅延で適用する。中央制御を全eventのcritical pathへ置かずに、workflow-level情報を使う狙いである。

## 評価条件
|項目|条件|
|---|---|
|ワークロード|3種類のagentic application|
|比較軸|tail 遅延、高速化倍率、持続リクエスト rate、制御 scalability|
|対象資源|LLM、tool、状態、KV キャッシュ|
|制御|大域 policy + 局所 event-driven enforcement|

## 主要結果
3 ワークロードでtail 遅延を34～74%削減し、最大3.38倍の高速化倍率を報告する。比較対象が維持できない80 リクエスト/sの負荷を持続でき、制御 planeは約130K futuresまで拡張しつつ制御オーバーヘッドを500ms未満に保つ。

これらは単一LLM カーネルの高速化ではなく、workflow全体の依存関係と再利用可能状態をランタイムが把握することで、待ち時間と資源 mismatchを減らしたシステム-level結果である。

## 既存研究との差・限界
静的DAGを前提とするworkflow engineやリクエスト単位のLLM スケジューラと異なり、Pythonの動的制御を維持したままfuture metadataでworkflowをランタイムへ伝える。性能はagent workflowの再利用性・並行性・分岐構造に依存し、単発の独立LLM リクエストではworkflow-aware制御の利得は小さい。評価は3 ワークロードであり、あらゆるtool ecosystemや障害 modeを網羅するものではない。