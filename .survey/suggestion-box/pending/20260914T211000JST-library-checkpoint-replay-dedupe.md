type: improvement
observed_at: 2026-09-14T21:10:00+09:00
run_key: unknown
component: fallback / queue
observation: >50候補時の通常research経路で、GitHub上はreadyのままなのにChatGPT Library `/LLM-survey-outbox/pending/` には完全5-slot payloadが複数世代存在するjobが連続してclaimされた。今回だけでもFlowKV、Sparse inference、BlockServe、Autellix、AgentCgroup、MorphServe、OrderMoE、StreamServe、persistent Q4 agent KV、BanaServe等で確認した。`checkpointed_jobs` はworker-local除外なので、別workerは同じready jobを再claim・再精読し、同じ論文のpending envelopeが増え続ける。Library replayがimmutable resultへ収束するまでrepository-wide completionにはできないという安全条件は正しいが、pending checkpointの存在を他workerの再精読抑止に利用できていない。
suggestion: claim-fast/queue snapshot側に、検証済みLibrary pendingまたはGitHub fallback-inbox/archiveから構築するrepository-wideな `durable_checkpoint_pending` 指標を導入し、内容自体をcompleted扱いにはしないまま、新規research claimの選択対象から一時除外する。併せてGitHub write可能なworkerはresearch loop開始時またはclaim待ち中にpending envelopeをfallback-inboxへ優先replayし、stale claimでreplay不能なpayloadは明示的にrepair/reclaim対象へ昇格させる。少なくとも同一jobのpending envelopeが一定数以上ある場合は、再精読よりreplay/reconciliationを優先する。
expected_benefit: 同じ論文の重複全文精読と重複Library payload生成を大幅に減らし、ready backlogを実際の未読論文へ向けられる。fallback復旧が滞った際も、研究workerの処理量を未処理jobへ集中できる。
risk_or_tradeoff: Library checkpointの存在だけでglobal completionにすると偽checkpointやstale claimでjobを隠す危険があるため、あくまで一時claim抑止とreplay優先度に限定し、最終completed判定は既存どおりimmutable GitHub resultに限定する必要がある。Library一覧取得失敗時は通常queueへフォールバックする。
confidence: high
evidence: 本runのclaim requests `claim-20260914T115900Z-scheduled-chat-discovery-overflow-11` から `claim-20260914T124200Z-scheduled-chat-discovery-overflow-11-next11`、対応claim-results、および `/LLM-survey-outbox/pending/` の各job複数envelope。
