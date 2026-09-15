# Discovery specialist worker

この文書は、既存の論文workerとは別に毎時実行する **探索主体のScheduled Chat worker** の正本とする。平常時はcandidate在庫を継続的に積み上げる。一方、research backlogが十分に大きいときは追加readerとして働き、既存の論文workerと並列にresearchを消化する。

## 役割

- 探索専用worker: 通常はdiscovery、軽量重複判定、候補評価、priority付与、candidate投入を担当する。
- `candidate_inventory > 50` かつactionable researchがある場合: **overflow research mode** へ切り替え、そのrunでは通常論文workerと同じresearch / audit契約、claim直列契約、品質基準、耐久保存契約に従う。
- 既存の論文worker: 従来どおりresearch / audit / discoveryを行う。探索機能を削除・停止しない。
- GitHub Actions: queue/state/identityの最終整合、重複抑止、job materialization、および `discovery-state.json` の統計更新を担当する。

通常探索モードではresearch、audit、5-slot structured research record作成、論文Markdown生成を行わない。候補発見後に全文精読へ進まず、candidate poolへ安全に投入して次の探索軸へ進む。overflow research modeではこの制約を解除し、`always-on-worker.md` / `claim-serial-policy.md` / `candidate-buffer-policy.md` に従ってpriority上位のresearch / auditを処理する。

## 同一run内の継続不変条件

**1 discovery round / 1 discovery submission の完了はScheduled Chat runの完了ではない。** roundごとの耐久保存は中間checkpointとして扱い、その直後に最新HEAD、queue、`discovery-state.json`、candidate inventoryを再取得して、同じrun内の次の行動を必ず決める。

Discovery modeのままで、次回同一`:00` Scheduled Chat枠まで600秒より多く残り、正本読取と耐久保存が可能で、`next_axis_hint` または他の独立した有望探索軸が残る場合は、**同じrun内で直ちに次の異なるdiscovery roundへ進む**。`next_axis_hint` を書いたこと自体は終了理由ではなく、原則として同一runで次に試す候補軸を示す。

次は単独ではrun停止条件にしない。

- 1 round / 1 submissionを完了した。
- candidateを5本送信した。
- acceptedが0件だった。
- 全候補が重複だった、または採用率が低かった。
- Actionsが次jobをmaterializeするのを待っている。
- 1 discovery jobがcompletedになった。
- 1 Research/Auditを完了した。

runを終了する直前には必ず **終了監査** を行い、`discovery-exhaustive-run-policy.md` のRun-level stop conditionsのいずれかに明確に一致することを確認する。一致しない場合は終了禁止で、次のdiscovery roundまたはoverflow research modeへ進む。特に、次回`:00`まで600秒より多く残り、未試行の有望な`next_axis_hint`があるのにDiscoveryを1 roundだけで終了してはならない。

探索空間枯渇を終了理由にできるのは、`discovery-exhaustive-run-policy.md` の独立探索経路の一巡条件を満たした場合だけとする。1 round終了直後や、未試行の有望軸が明示されている状態を「枯渇」とみなしてはならない。

## 実行時刻

探索主体workerは毎時 `:00` JSTに実行する。既存の論文workerは従来どおり毎時 `:30` JSTで動作する。平常時は30分ずらすことでdiscoveryとpaper workerのqueue/state write競合を減らす。overflow research modeでは`:00` workerが長く動けば`:30` workerと自然に重なり、異なるworker IDで別jobをclaimして並列readerとして動く。

探索主体workerは既存の24-run maintenance counterへ加算しない。overflow research modeへ切り替わってもこの扱いは変えない。maintenance gateは既存の論文worker側の正本に従う。

## 必読正本

毎回default branch最新HEADを取得し、同じHEADから最低限以下を読む。

1. `candidate-buffer-policy.md`
2. `always-on-worker.md`
3. `claim-serial-policy.md`
4. `queue-v10.md`
5. `fallback-routing.md`
6. `continuation-policy.json`
7. `.survey/work-queue/next-jobs.json`
8. `.survey/work-queue/discovery-state.json`
9. `.survey/survey-state/paper-identity-index.json`
10. 必要に応じて `.survey/survey-state/identity-deltas/**` と既存job

この文書と他文書が競合する場合、探索主体workerのモード切替については本書と `candidate-buffer-policy.md`、research実行時の継続・claim・transportについては `always-on-worker.md` / `claim-serial-policy.md`、transportについては `fallback-routing.md` / `continuation-policy.json` を優先する。

## candidate在庫とモード切替

`candidate-buffer-policy.md` の水位を共有する。

- low watermark: 25
- critical watermark: 15
- overflow research threshold: `candidate_inventory > 50`
- target / upper cap: なし

run開始時と、discovery submissionまたはresearch/auditの耐久保存後にcandidate在庫とactionable researchを再評価する。

- `candidate_inventory > 50` かつactionable researchあり: overflow research mode。新規discoveryを停止し、通常論文workerと同じhigh-backlog research-only動作へ切り替える。
- `candidate_inventory <= 50`、またはactionable researchなし: 通常探索モード。高価値候補のdiscoveryを継続する。

overflow research modeではworker IDを通常論文workerと共有しない。同じScheduled Chat worker内でも未完了claimは1件だけ保持し、1件の完全payloadをGitHubまたはLibraryへ耐久保存した後で次の1件をclaimする。別workerが同時に別claimを持つことは許可される。

## overflow research mode

overflow research modeへ入ったrunでは、通常論文workerのhigh-backlog research-only契約をそのまま適用する。

1. `checkpointed_job_ids` を除いたactionable readyからpriority順に1件claimする。
2. 一次資料全文を取得・精読し、repository-qualityの5-slot structured research recordを作る。
3. preflight後、immutable descriptorまたはLibrary checkpointへ完全payloadを耐久保存する。
4. Actionsのterminal反映を待たず、最新HEAD / queue / claim stateを再取得して次の1件をclaimする。
5. 一次資料取得・耐久保存・claimが利用可能でbacklogが十分なら、1runにつき最低3件を下限目標とし、3件を停止条件にしない。
6. 各job保存後に `candidate_inventory` を再評価し、50以下まで減った場合は通常探索モードへ戻る。

通常論文workerと同時に動く場合も、各workerは固有の `worker_id` を使い、同じjobの二重claimやrecord bankの二重予約はclaim-fastの直列化に任せる。

## 探索経路

通常探索モードでは直近の `discovery-state.json` を読み、直前の高重複軸を機械的に繰り返さない。候補経路は少なくとも以下から選ぶ。

- 新着論文
- 収録済み重要論文の被引用
- 重要論文の参考文献
- DBMS / OS / storage / distributed systems / HPC / GPU runtime / networking等の隣接分野
- 直近採用候補からの検索語拡張
- offload / hierarchical memory / MoE / expert cache・placement・prefetch / KV cache / scheduling / disaggregation / inference framework等の重点テーマ

固定件数で埋めない。1軸が0件または全重複なら別軸へ切り替える。

## 二重探索・二重投入の防止

探索開始前とcandidate投入直前の **2段階** で重複判定する。

照合対象:

1. paper identity index
2. identity deltas
3. 既収録paper
4. 既存research / discovery jobs
5. GitHub fallback inbox/archive
6. 可能な範囲でLibrary pending/offline seed

同一性判定はcanonical ID、arXiv ID、DOI、OpenReview IDを優先し、最後にnormalized titleを使う。

探索開始後に既存workerやActionsが同じ候補を先に投入する可能性があるため、write直前に最新HEAD / queue / identityを再取得する。そこで既存化していた候補は送らない。

両workerが同じ論文を同時に発見した場合も、同じcanonical IDから同一candidateとして扱い、Actions側の重複抑止で1件へ収束させる。重複候補を別jobとして意図的に作らない。

## candidate priority

priorityは少なくとも以下を考慮する。

- 重点テーマとの関連度
- 新規性と既存収録との差分
- 実測評価の有無
- 公式実装・コード公開の有無
- 引用関係上の重要度
- SSD/NVMe、MoE、階層メモリ、serving基盤への研究価値

単純FIFOではなく、research workerが価値の高い候補から読めるようpriorityを付ける。

## transport

通常探索モードでGitHub write可能時は既存workflow v10のdiscovery transportを使い、paper/state/READMEを直接編集しない。

各discovery submissionには、通常の `job_id` と `candidates` に加えて、トップレベルに `discovery_stats` を含める。

1回の探索主体Scheduled Chat実行では、開始時に **1つだけ** `run_key` を確定し、そのrun内の全探索round・全submissionで同じ値を使う。原則として今回の予定実行枠をJSTの `YYYY-MM-DDTHH:00:00+09:00` 形式で表す。round開始時刻、submission時刻、Actions待ち後の再開時刻を新しい `run_key` にしてはならない。予定実行枠を直接取得できない実行環境では、そのScheduled Chat実行の開始時刻をJSTで時単位に切り捨てた値を使い、その後はrun終了まで固定する。

これにより `STATUS.md` は複数の探索roundを「毎時の探索主体worker 1回がどれだけ探索したか」という単位で集計できる。旧データで同一時間帯に複数 `run_key` が残っている場合、dashboard側はJSTの毎時枠へbest-effortで集約する。

```json
{
  "discovery_stats": {
    "run_key": "2026-09-12T15:00:00+09:00",
    "round": "specialist-new-arrivals-1",
    "axis": "2609新着・分離サービング",
    "query_summary": "今回実際に使った探索軸と範囲の短い説明",
    "candidate_count": 5,
    "duplicate_filtered_count": 2,
    "duplicate_canonical_ids": ["arxiv:..."],
    "next_axis_hint": "次回に優先する異なる探索軸",
    "empty_round_reason": null
  }
}
```

`candidate_count` は検索結果の生件数ではなく、テーマ適合性等を確認して実質的に候補として評価した件数を数える。`duplicate_filtered_count` はそのうちScheduled Chat側の重複確認で除外した件数とする。`candidates` には重複除外後にActionsへ投入する候補だけを入れる。`empty_round_reason` は有効候補が残らなかった場合だけ具体的に記録すればよい。

Scheduled Chatは `accepted_count` を確定しない。最終投入直前以降にも通常workerやActionsによって同じ候補が既存化し得るため、実際の採用数はActionsが最終dedupe後の `research_jobs_added` から確定する。

GitHub write不能時は `fallback-routing.md` に従う。通常探索モードではChatGPT Library `/LLM-survey-outbox/pending/` へoffline job seedを完全envelopeとして耐久保存する。overflow research modeでは通常論文workerと同じく、完成した5-slot research/audit payloadをLibraryへcheckpointして次jobへ進む。完成Markdownは直接保存しない。

同一payloadの重複保存を避け、復旧時は既存のimmutable intake経路に従う。

## discovery-state

`discovery-state.json` は **GitHub Actionsを単一writer** とする。探索主体Scheduled Chatも通常論文Scheduled Chatも、このファイルを直接更新しない。

通常探索モードでは各workerはdiscovery submissionの `discovery_stats` として、探索軸、query概要、候補数、Scheduled Chat側で除外した重複数、重複ID、次回推奨軸を渡す。Actionsはsubmission処理時に最終dedupe後の実採用数を確定し、以下を `discovery-state.json` へ1回だけ反映する。

- candidate count
- duplicate filtered count
- novel candidate count
- accepted count
- duplicate ratio
- exploration axis aggregate
- last run / last round
- empty-round streak

submission pathを統計イベントの一意キーとして扱い、同じsubmissionをActionsが再処理しても二重加算しない。Actions workflowの直列化されたqueue処理を共有stateの競合回避点とし、Scheduled Chat側のSHA競合解消でstateを直接上書きしない。

## 通知

通常成功時はユーザーへ通知しない。GitHubとLibraryの両方へ候補またはresearch成果を耐久保存できない、継続的な重複競合でcandidate投入不能、または正本が読めず安全に探索・researchできない場合だけ問題として通知する。
