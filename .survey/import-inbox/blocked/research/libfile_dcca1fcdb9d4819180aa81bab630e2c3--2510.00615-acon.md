---
canonical_id: "arXiv:2510.00615"
title: "ACON: Optimizing Context Compression for Long-horizon LLM Agents"
summary: "ACONは長時間agentの観測とinteraction historyを圧縮する際、full contextでは成功したが圧縮contextでは失敗したtrajectory pairをLLMに分析させ、自然言語のcompression guideline自体を反復改善する。AppWorld、OfficeBench、Multi-objective QAでpeak token memoryを26〜54%削減しつつ性能を概ね維持し、小型compressorへ蒸留しても95%以上のaccuracyを保持する。"
list_summary: "圧縮で失敗したagent trajectoryをfeedbackとして自然言語compression guidelineを反復最適化し、長時間agentの文脈 トークンを26〜54%削減する。"
authors: ["Minki Kang","Wei-Ning Chen","Dongge Han","Huseyin A. Inan","Lukas Wutschitz","Yanzhi Chen","Robert Sim","Saravan Rajmohan"]
published: "2025-10-01"
publication: "arXiv"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2510.00615"
sources: ["https://arxiv.org/abs/2510.00615"]
implementation: "AppWorld、OfficeBench、Multi-objective QAでlong-horizon agent context compressionを評価し、large LLM compressorとdistilled small compressorを比較。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2510.00615"
arxiv_categories:
  primary: "cs.AI"
  cross_list: ["cs.CL"]
worker_completed_at: "2026-10-06T07:00:00+09:00"
worker_run_key: "20261006-0700-scheduled-chat-00/r02"
reference_main_sha: "b66aec387fad5bd8e23d8ba03ddab4b574484e1b"
last_audited: null
audit_version: 0
---

## 概要
agentがtool callとenvironment observationを繰り返すと、過去のaction、observation、reasoningが文脈へ蓄積し、毎段階のプリフィル/KV メモリ費用が増える。固定要約プロンプトはタスクごとに「残すべき情報」が異なるため、トークンを減らせても後続判定に必要な状態を落として失敗し得る。

Agent Context Optimization（ACON）は圧縮器そのものを固定せず、全体 文脈では成功したのにcompressed 文脈では失敗したtrajectory pairを強いLLMへ提示し、失敗原因から自然言語のcompression guidelineを更新する。観測とinteraction historyの両方を対象にし、最終的には最適化した圧縮方針を小型モデルへ蒸留して追加推論費用を下げる。

## 問題設定
long-horizon agentでは文脈長が段階数とともに増え、入力 トークン課金だけでなく注意機構/KV キャッシュも増加する。単純な古い履歴削除は、以前のtool resultや制約が後で必要になったとき回復できない。一般purpose summarizerは文章として自然でも、agent policyが必要とするvariable、未完タスク、environment 状態を保持する保証がない。

## 手法
### trajectory-pair feedback
同じタスクについて全体 文脈で成功したtrajectoryと、圧縮文脈で失敗したtrajectoryを収集する。強いLLMが差分を分析し、どの情報削除・言い換えが障害につながったかを言語化する。

### compression guideline optimization
失敗分析を現在のguidelineへ反映し、「何を保持し、何を統合し、何を削るか」の自然言語規則を反復更新する。パラメータ optimizationではなくinstruction spaceで圧縮policyを改善するため、観測形式が異なるタスクへも適応できる。

### observation/history compression
現在のenvironment observationだけでなく過去interaction historyもcondensationする。両方を同じトークン budget問題として扱い、long horizonで増え続ける履歴をboundedな有用情報へ変換する。

### compressor distillation
強いLLMを毎段階 compressorとして呼ぶと圧縮で節約した費用を相殺する。そこで最適化guidelineと圧縮例を小型モデルへ蒸留し、ランタイム compression オーバーヘッドを減らす。

## 評価条件
| 観点 | 内容 |
|---|---|
| ベンチマーク | AppWorld、OfficeBench、Multi-目的関数 QA |
| ワークロード | long-horizon tool-using agents |
| 指標 | タスク performance、peak 文脈 トークン、distillation quality |
| 比較対象 | 全体 文脈、既存文脈 compression |
| compressor | strong LLM → smaller distilled モデル |

## 主要結果
| 指標 | 結果 |
|---|---:|
| peak トークン メモリ削減 | 26〜54% |
| distilled compressor | 元圧縮器accuracyの95%以上を保持 |
| smaller LM agent | 最大46% performance改善 |

26〜54%はベンチマーク/settingで幅があり、固定削減率ではない。小型agentの46%改善は単なる高速化倍率ではなく、文脈整理により判定 qualityが改善したタスク性能値である。

## 既存研究との差
single-段階 プロンプト compressionは一度の質問に不要なトークンを削ることが多い。ACONはcompression後のagent行動がenvironmentを変え、その後のtrajectory全体へ影響するlong-horizon条件を対象にする。圧縮障害を次のguideline更新へ戻すclosed-loop optimizationが中心である。

## 限界
圧縮方針の最適化には全体/compressed trajectory pairと強いLLMによる障害 analysisが必要で、初期構築費用がある。タスク 分布が大きく変わるとguidelineの再最適化が必要になり得る。トークン メモリ削減が同率の実時間短縮になるとは限らず、compressor呼び出しとtool 遅延も残る。

## 一次資料
- https://arxiv.org/abs/2510.00615