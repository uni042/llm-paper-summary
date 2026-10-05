---
canonical_id: "arXiv:2006.02464"
title: "Serving DNNs like Clockwork: Performance Predictability from the Bottom Up"
summary: "ClockworkはGPU推論を予測不能な共有resourceとして扱うのではなく、model load・kernel execution等を制御可能なactionへ分解し、実測execution profileとdeadlineから中央schedulerが実行時刻を決めるmodel serving systemである。production traceで数千modelを扱い、100 ms latency targetを99.9999%のrequestで満たす。"
list_summary: "GPU推論を予測可能なactionへ分解し、deadline-aware中央scheduleで数千モデルのtail 遅延とリクエスト-level isolationを制御する推論提供 システム。"
authors: ["Arpan Gujarati","Reza Karimi","Safya Alzayat","Wei Hao","Antoine Kaufmann","Ymir Vigfusson","Jonathan Mace"]
published: "2020-06-03"
publication: "OSDI"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/2006.02464"
sources: ["https://arxiv.org/abs/2006.02464"]
implementation: "GPU model serving system Clockworkを実装し、production trace由来workloadでtail latency、SLO達成率、model数scale、performance isolationを評価。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2006.02464"
arxiv_categories:
  primary: "cs.DC"
  cross_list: []
worker_completed_at: "2026-10-06T07:00:00+09:00"
worker_run_key: "20261006-0700-scheduled-chat-00/r01"
reference_main_sha: "b66aec387fad5bd8e23d8ba03ddab4b574484e1b"
last_audited: null
audit_version: 0
---

## 概要
モデル 推論提供では平均遅延が低くても、モデル 読み込み、GPU queue、バッチ競合などの稀な遅延がtailを悪化させる。従来システムはtimeoutやreactive 読み込み balancingで後から混雑へ対処するが、deadline直前のリクエストを救えない。ClockworkはDNN inference カーネル自体のexecution timeが同一GPU・形状なら高い再現性を持つ点から出発し、ランタイムの自由度を減らして予測可能性を上位スケジューラへ伝播させる。

workerはモデル 読み込み、入力 transfer、inference等を明示actionとして受け取り、中央controllerがprofile済み時間とdeadlineからいつ・どのGPUで実行するかを決める。production トレース ワークロードで数千モデルを同時serveしながら100 ms 対象を99.9999%のリクエストで満たした。

## 問題設定
一般的な推論提供 ランタイムはGPU driver queue、background モデル 読み込み、動的 batchingなど複数の独立queueを持つ。個々の平均時間が短くても、queue順序と資源 contentionが見えなければcontrollerはリクエスト completionを予測できない。Clockworkはスループット最大化より、まず「何がいつ終わるか」を予測可能にする。

## 手法
### predictable worker
worker内部の自律スケジューラを排し、controllerから指定されたactionを実行する。モデル 重み 読み込みとinferenceを分離し、各actionの実行時間をprofileする。GPU上で同時に多数カーネルを競合させず、予測誤差源を減らす。

### centralized scheduling
controllerはリクエスト deadline、モデル residency、profiled execution timeを使ってactionを選ぶ。deadlineへ間に合わない仕事を無制限にqueueへ積まず、モデル 読み込みも将来リクエストを見越してscheduleする。

### model cache管理
GPU メモリに常駐なモデルと読み込み予定をcontrollerが把握し、必要モデルの読み込みがinference deadlineと衝突しないよう調整する。キャッシュ replacementをworker任せにしないため、読み込み 遅延をリクエスト pathへ明示的に組み込める。

### admissionとisolation
資源 budgetを超えるリクエストは他tenantのdeadlineを壊す前に制御する。リクエスト-level SLOをスケジューラ 目的関数にすることで、特定モデルのburstが別モデルのtail 遅延へ波及するのを抑える。

## 評価条件
| 観点 | 内容 |
|---|---|
| ワークロード | production トレース由来multi-モデル 推論提供 |
| scale | 数千モデル |
| 遅延 対象 | 代表条件100 ms |
| 指標 | deadline/SLO達成率、tail 遅延、isolation |
| 構成 | centralized controller + predictable GPU workers |

## 主要結果
代表評価では数千モデルをserveしながら100 ms 遅延 対象を99.9999%のリクエストで満たした。重要なのは平均遅延だけでなく極端なtailまでdeadline内へ収めた点である。predictabilityを犠牲にするopportunisticな同時実行を減らしても、deadline-aware batchingとモデル キャッシュ管理で高い資源利用を維持する。

## 既存研究との差
reactive システムはqueueが遅れた後に読み込み balancingやバッチ変更を行う。Clockworkは低level executionを決定論的に近づけ、上位スケジューラが未来のcompletion timeを使えるようにする。LLM専用ではないが、後のLLM 推論提供でSLO-aware スケジューラを考える際の基礎的設計点になる。

## 限界
評価はDNN inference一般で、KV キャッシュやautoregressive デコード、プリフィル/デコード分離など現代LLM固有状態を持たない。中央controllerはprofileの安定性を前提とし、カーネル時間が入力依存で大きく変わるワークロードでは予測誤差が増える。100 ms/99.9999%は評価条件の結果で任意ハードウェアへ保証されない。

## 一次資料
- https://arxiv.org/abs/2006.02464