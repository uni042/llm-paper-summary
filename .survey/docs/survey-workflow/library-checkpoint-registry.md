# ChatGPT Library checkpoint registry

この文書は、Research/Audit の全文精読が ChatGPT Library に耐久保存された後、GitHub 反映前に同じ論文を再精読しないための正本である。GitHub queue / paper の正本性は変更しない。Library registry は **「全文精読済みだが GitHub publication が未完了」** を表す耐久barrierである。

## 1. Library layout

Research/Audit fallback は次の3領域を使う。

- payload: `/LLM-survey-outbox/pending/<envelope-id>.json`
- registry: `/LLM-survey-outbox/checkpoints/<job-id>.json`
- publication完了後: `/LLM-survey-outbox/processed/<envelope-id>.json`

不正・回復不能payloadだけ `/LLM-survey-outbox/failed/` へ隔離する。

`pending/` のファイル数そのものを精読済み判定に使わない。再精読barrierの正本は `checkpoints/<job-id>.json` とGitHub claimに残る `checkpoint_ref` の和集合である。

## 2. Marker schema

1 jobにつき1 markerを持つ。単一の共有checklistファイルは複数worker更新競合を起こすため使わない。

```json
{
  "schema_version": 1,
  "job_id": "job-research-...",
  "canonical_id": "arXiv:2607.29069",
  "claim_id": "claim-...",
  "attempt_id": "attempt-...",
  "worker_id": "scheduled-chat-...",
  "payload_ref": "/LLM-survey-outbox/pending/<envelope-id>.json",
  "status": "checkpointed",
  "checkpointed_at": "2026-09-15T00:00:00+09:00",
  "transported_at": null,
  "reflected_at": null,
  "github_intake_path": null
}
```

`status` は次だけを使う。

- `checkpointed`: 完全な5-slot payloadがLibraryに耐久保存済み。GitHub intake未確認。
- `transported`: 同じenvelopeがGitHub `fallback-inbox` または `fallback-archive` に耐久保存されたことを確認済み。publication未確認。
- `reflected`: immutable submissionが成功し、canonical jobがterminal/completedとしてGitHubへ反映済み。

markerはpayload保存より先に作らない。markerだけ存在しpayloadが無い場合は異常として扱い、新規精読を自動開始せず回復/隔離を優先する。

## 3. Claim barrier

Research/Audit claimを要求する前に、workerは必ず `checkpoints/` を読む。

`checkpointed` または `transported` markerのjobがGitHub上で非terminalなら、そのjobは**全文精読済み**として扱い、再精読しない。claim requestの `checkpointed_jobs` に次を入れる。

```json
{
  "job_id": "job-research-...",
  "checkpoint_ref": "/LLM-survey-outbox/pending/<envelope-id>.json"
}
```

markerの `payload_ref` が `processed/` を指しているlegacy/不整合状態では、同じpayloadがLibraryに存在することを確認し、必要なら `pending/` へ戻してからclaim barrierへ使う。

GitHub側では `.survey/scripts/apply_library_checkpoint_barriers.py` が、GitHub claimに既に残っている `checkpoint_ref` を未処理claim requestへ自動マージする。したがってbarrierは二重化される。

1. Library marker: GitHub write障害中でも再精読を防ぐ。
2. GitHub persisted `checkpoint_ref`: workerがLibrary markerを読み落としても再claimを防ぐ。

どちらか一方でも精読済みを示す限り、新規全文精読を開始しない。

## 4. Checkpoint creation

Library fallbackが必要になったResearch/Auditについては次の順序を守る。

1. 完全な5-slot envelopeを `pending/<envelope-id>.json` へ保存する。
2. 保存したpayloadを再読して `job_id` / `claim_id` / `attempt_id` / envelope `id` が期待値と一致することを確認する。
3. `checkpoints/<job-id>.json` を `checkpointed` として作成または更新する。
4. GitHub writeが可能ならclaim requestの `checkpointed_jobs` を使って現在claimを解放する。
5. 次の独立jobへ進む。

GitHub writeが利用不能でも1〜3まで完了すれば全文精読成果は失われない。GitHubが復旧するまで同jobを再精読せず、既に安全に取得済みの別作業だけ継続する。

## 5. Recovery transport

GitHub read/writeが復旧したら、新規claimより先にregistryを走査する。

`checkpointed` markerごとに:

1. `payload_ref` を読み、markerのjob/claim/attemptと一致することを確認する。
2. GitHub `fallback-inbox/<envelope-id>.json`、`fallback-archive/<envelope-id>.json`、`fallback-failed/<envelope-id>.json` を確認する。
3. inbox/archiveに同一内容が無ければfallback-inboxへimmutableに保存する。同じidで別内容なら上書きせず衝突として扱う。
4. GitHub側に同一envelopeがdurableに存在することを再取得して確認する。
5. markerを `transported` に更新し、`github_intake_path` と `transported_at` を記録する。

**この段階ではLibrary payloadを `processed/` へ移さない。** GitHub intakeはtransport receiptでありpublication完了ではない。

## 6. Publication acknowledgement

`transported` markerは、次を確認できた場合だけ `reflected` にする。

- canonical jobがterminalである。
- completed Research/Auditなら対応するimmutable resultが `ok: true` である。
- completed Researchならpaper artifactがcanonical job/resultと整合する。

確認後:

1. markerを `reflected` に更新し `reflected_at` を記録する。
2. payloadがまだ `pending/` にあれば `processed/` へ移す。
3. markerは監査用に `checkpoints/` に残してよい。terminal jobなのでclaim barrierには影響しない。

従来 `processed/ = GitHub intake受領済み` としていた運用は廃止する。以後 `processed/` は **GitHub publication確認済みpayload** を意味する。

## 7. Reconciliation of historical state

旧運用で `processed/` に移動済みでもcanonical jobがまだ `ready` の場合は、publication完了とみなさない。

- 対応payloadを `processed/` から特定する。
- job/claim/attemptを照合する。
- markerを `checkpointed` または `transported` として再構築する。
- 必要ならpayloadを `pending/` へ戻す。
- fallback replayを再実行する。

同jobの複数attemptがある場合、canonical current claimに一致するattemptを優先する。current claimがcheckpoint_refを保持する場合はそのpayloadを第一候補とする。terminal jobの古いpayloadは再精読せずacknowledgeだけ行う。

## 8. Failure policy

単一marker/payloadの異常でrun全体を止めない。異常jobだけ隔離し、独立作業を続行する。

ただし次は安全側へ倒す。

- markerはあるがpayloadが見つからない: 自動再精読しない。まずLibraryのpending/processedとGitHub fallback stateを探索する。
- payload identityがmarkerと不一致: 上書きせず隔離する。
- GitHubに同じenvelope idで別内容: conflict。Library原本を保持する。
- LibraryにもGitHubにも完全payloadが無いことを確認できた場合だけ、checkpoint barrierを明示的に解除して再精読候補へ戻してよい。
