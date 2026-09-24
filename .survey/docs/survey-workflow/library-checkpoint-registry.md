# ChatGPT Library checkpoint registry

この文書は、Research/Audit の全文精読が ChatGPT Library に耐久保存された後、GitHub 反映前に同じ論文を再精読しないための正本である。GitHub queue / paper の正本性は変更しない。Library registry は **「全文精読済みだが GitHub publication が未完了」** を表す耐久barrierである。

publication後のLibrary dispositionは `.survey/docs/survey-workflow/library-publication-ack.md` と `.survey/work-queue/library-ack-manifest.json` を正本とする。本書だけから `processed/` / `superseded/` への移動を推測してはならない。

## 1. Library layout

Research/Audit fallback は次の領域を使う。

- payload待機: `/LLM-survey-outbox/pending/<envelope-id>.json`
- registry: `/LLM-survey-outbox/checkpoints/<job-id>.json`
- このpayloadがpublicationへ反映済み: `/LLM-survey-outbox/processed/<envelope-id>.json`
- 同jobの別attemptがpublicationを完了しこのpayloadが不要: `/LLM-survey-outbox/superseded/<envelope-id>.json`
- 不正・回復不能: `/LLM-survey-outbox/failed/<envelope-id>.json`

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

処理中markerの `status` は主に次を使う。

- `checkpointed`: 完全な5-slot payloadがLibraryに耐久保存済み。GitHub intake未確認。
- `transported`: 同じenvelopeがGitHub `fallback-inbox` または `fallback-archive` に耐久保存されたことを確認済み。publication未確認。
- `reflected`: ACK manifestにより、このpayload自身または明示的provenance reboundのcanonical publication反映を確認済み。
- `superseded`: ACK manifestにより、同jobの別attemptがcanonical publicationを完了し、このmarkerの元payloadが不要になったことを確認済み。

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

markerの `payload_ref` が `processed/` を指しているlegacy/不整合状態では、最新ACK manifestとpayload identityを確認し、ACKされていないなら必要に応じて `pending/` へ戻してから回復する。

GitHub側では `.survey/scripts/apply_library_checkpoint_barriers.py` が、GitHub claimに既に残っている `checkpoint_ref` を未処理claim requestへ自動マージする。したがってbarrierは二重化される。

1. Library marker: GitHub write障害中でも再精読を防ぐ。
2. GitHub persisted `checkpoint_ref`: workerがLibrary markerを読み落としても再claimを防ぐ。

どちらか一方でも精読済みを示す限り、新規全文精読を開始しない。`reflected` / `superseded` はcanonical jobがterminalであることをmanifestにより確認した後の状態なので、新規claim barrierへ投入する必要はない。

## 4. Checkpoint creation

Library fallbackが必要になったResearch/Auditについては次の順序を守る。

1. 完全な5-slot envelopeを `pending/<envelope-id>.json` へ保存する。
2. 保存したpayloadを再読して `job_id` / `claim_id` / `attempt_id` / envelope `id` が期待値と一致することを確認する。
3. `checkpoints/<job-id>.json` を `checkpointed` として作成または更新する。
4. GitHub writeが可能ならclaim requestの `checkpointed_jobs` を使って現在claimを解放する。
5. 次の独立jobへ進む。

GitHub writeが利用不能でも1〜3まで完了すれば全文精読成果は失われない。GitHubが復旧するまで同jobを再精読せず、既に安全に取得済みの別作業だけ継続する。

## 5. Recovery transport

GitHub read/writeが復旧したら、新規claim/discoveryより先に **`checkpoints/` と `pending/` の両方** を走査する。

### 5.1 Marker付きpayload

`checkpointed` markerごとに:

1. `payload_ref` を読み、markerのjob/claim/attemptと一致することを確認する。
2. GitHub `fallback-inbox/<envelope-id>.json`、`fallback-archive/<envelope-id>.json`、`fallback-failed/<envelope-id>.json` を確認する。
3. inbox/archiveに同一内容が無ければfallback-inboxへimmutableに保存する。同じidで別内容なら上書きせず衝突として扱う。
4. GitHub側に同一envelopeがdurableに存在することを再取得して確認する。
5. markerを `transported` に更新し、`github_intake_path` と `transported_at` を記録する。

### 5.2 Markerのないorphan pending payload

旧worker・移行途中・過去の障害では、完全なResearch/Audit envelopeが `pending/` に存在するのに `checkpoints/<job-id>.json` が無いことがある。**markerが無いことを理由にpending payloadを無視してはならない。**

新規claim/discoveryより先に `pending/*.json` を全件sweepし、markerで参照されていないpayloadについて次を行う。

1. payloadを再読し、JSON object、`id`、`kind`、`job_id`、`attempt_id`、完全な5-slot writes等のtransport identityを検証する。
2. GitHub canonical job/claim/fallback stateと照合する。ここでpaper内容を再生成・再精読しない。
3. GitHub fallback-inbox/archive/failedにexact envelope idがあるか確認し、同一id・同一payloadならその状態を採用する。同一id・別内容ならLibrary原本を保持してconflict隔離する。
4. GitHub側に未存在で、payloadが完全かつ安全にreplay可能ならexact payloadをfallback-inboxへimmutableに搬送する。
5. Research/Audit jobが非terminalで、同payloadを精読済みbarrierとして保持すべきならmarkerを `checkpointed` または `transported` として再構築する。
6. GitHub intake確認後もLibrary payloadを独自判断でterminal folderへ移さない。次節のACK manifest更新を待つ。

1 runで件数が多くても、pending件数自体を停止理由にしない。handoff guardまで安全にsweepを継続し、残件は次runへ持ち越す。1件の異常で他の独立payloadの搬送を止めない。

**この段階ではLibrary payloadを `processed/` / `superseded/` へ移さない。** GitHub intakeはtransport receiptでありpublication/disposition完了ではない。

## 6. Publication acknowledgement and disposition

Libraryのterminal移動は最新mainの `.survey/work-queue/library-ack-manifest.json` だけを正本にする。

- `acknowledgements[]`: payload identityをexact照合できた場合だけ `processed/` へ移し、対応markerを `reflected` にする。
- `superseded[]`: payload identityをexact照合できた場合だけ `superseded/` へ移し、対応markerが同じ元attemptなら `superseded` にする。
- `waiting[]`: `pending/` から移動しない。再精読せず既存recovery/repair経路を使う。
- manifestに無いpayload: terminal folderへ移動しない。

fallback archive、canonical job status、paperの存在などをworker側で個別に組み合わせてACKを推測してはならない。詳細な判定条件は `library-publication-ack.md` を参照する。

従来 `processed/ = GitHub intake受領済み` としていた運用は廃止する。`processed/` は **このpayload自身または明示的provenance reboundがGitHub publicationへ反映済み**、`superseded/` は **別attemptが同jobを正常完了したため元payloadが不要** を意味する。

## 7. Reconciliation of historical state

旧運用のLibrary状態は新規claimより先に段階的に整合させる。

- `processed/` にあるのにmanifest ACKされないpayloadはpublication完了とみなさない。job/claim/attemptを照合し、必要ならpendingへ戻してreplayする。
- `pending/` にある完全payloadはmarkerの有無にかかわらず5.2のorphan sweep対象とする。
- `pending/` のpayloadがmanifest `acknowledgements[]` とexact一致すればprocessedへ、`superseded[]` とexact一致すればsupersededへ移す。
- terminal jobでもmanifest `waiting[]` またはmanifest外なら独自判断で移動しない。
- 同jobの複数attemptではcanonical current claimとGitHub `checkpoint_ref`、ACK manifestのprovenanceを優先して回復対象を決める。

historical payloadの整理は再精読ではない。既存の完全payloadを失わず、GitHub transport / deterministic repair / manifest dispositionだけで回復する。

## 8. Failure policy

単一marker/payloadの異常でrun全体を止めない。異常jobだけ隔離し、独立作業を続行する。

ただし次は安全側へ倒す。

- markerはあるがpayloadが見つからない: 自動再精読しない。まずLibraryのpending/processed/supersededとGitHub fallback stateを探索する。
- payload identityがmarkerと不一致: 上書きせず隔離する。
- GitHubに同じenvelope idで別内容: conflict。Library原本を保持する。
- orphan pendingが不完全: terminal folderへ動かさず、可能な限りidentity/evidenceを保持して隔離・修復する。
- LibraryにもGitHubにも完全payloadが無いことを確認できた場合だけ、checkpoint barrierを明示的に解除して再精読候補へ戻してよい。