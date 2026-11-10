type: continuation_obstacle
observed_at: 2026-09-13T18:40:00+09:00
run_key: 2026-09-13T18:30:00+09:00
component: queue
obstacle_class: repository_design
confidence: high

observation: |
  high-backlog research-only runで、開始時にChatGPT Library pendingを確認し、job-research-054d8fd9fb06ca0f（Punica）には完全な修復Research payloadが既に耐久checkpoint済みであることを確認した。しかしclaim-fastはLibrary checkpointed_job_idsを認識せず、このjobを新規claimとして割り当てた。その後、worker側では正本どおり再精読を避けてcheckpoint済みとして処理済みにしたが、次の1件claimは `worker already has an active unsubmitted claim` で拒否された。

suggestion: |
  claim-fast側でScheduled Chatが提示できるcheckpointed_job_idsを除外対象として受け取る、またはLibrary→GitHub fallback-inbox replay済みでなくてもdurable checkpointをclaim解放条件として安全に表現できるack経路を追加する。少なくともclaim requestに除外job ID一覧を渡せるようにすれば、Library backlogのために同じready jobを再claimして直列worker全体が停止する問題を回避できる。

expected_benefit: |
  Libraryへ完全payloadを保存済みのready jobを再claimしなくなり、`1件claim → 耐久保存 → 次の1件claim` のalways-on契約を実装上も満たせる。high-backlog時のResearch throughput低下と不要なreplay待ちを防げる。

risk_or_tradeoff: |
  worker申告だけで任意jobを除外できる設計は仕事の取りこぼしを生み得るため、除外はcanonical job IDとdurable envelope IDの対応を検証する、または除外をworker-local claim選択にのみ使いjob status自体は変更しない設計が必要。

would_have_continued_with: |
  priority最上位の未checkpoint Research jobを1件claimし、一次資料全文精読、5-slot structured record作成、preflight、耐久送信を最低3件まで継続する予定だった。

estimated_impact: |
  本runでは新規Research payload 3件以上の下限目標に対し、次claim取得前で停止。候補在庫169本、claimable 136本が存在するため仕事枯渇ではない。

stop_reason: |
  claim-fastがLibrary checkpoint済みの現在jobをactive unsubmitted claimとして保持し、次の直列claimを拒否したため、claim-serial-policyを守ったまま新しいResearch jobを取得できない。

last_completed_work: |
  maintenance gateを更新し、高バックログResearch専用モードを判定。Punicaの既存Library完全payloadを確認して再精読を回避し、新しいclaim requestを1件だけ発行した。

secondary_factors: |
  Library pending envelopeをGitHub fallback-inboxへreplayすれば最終的に解消可能だが、現在のGitHub connectorはLibrary fileをそのままGitHub contentとして転送するfile-to-file操作を持たず、大きな完全envelopeを手作業で再シリアライズする必要があるためrun内のResearch throughputを大きく損なう。

evidence: |
  claim result: .survey/work-queue/claim-results/sc-20260913T093500Z-run1.json
  rejected next claim: .survey/work-queue/claim-results/sc-20260913T093800Z-run1-b.json
  Library envelope: /LLM-survey-outbox/pending/20260913T141800JST-repair-research-2310.18547-punica.json
