# Library publication acknowledgement contract

`/LLM-survey-outbox/pending/` から `/LLM-survey-outbox/processed/` へpayloadを移すためのGitHub側の判定契約を定義する。

## Authoritative manifest

GitHub Actionsは `.survey/scripts/library_ack_manifest.py` を実行し、派生ファイル `.survey/work-queue/library-ack-manifest.json` を生成する。

Scheduled ChatはLibrary payloadを `processed/` へ移す前に、必ずこのmanifestの `acknowledgements` を確認する。`fallback-archive` にあること、paperが存在すること、jobがterminalに見えること等をScheduled Chat側で個別推測して代用してはならない。

## Direct acknowledgement

通常はexact attempt単位で判定する。次のすべてを満たす場合だけ `status=reflected` としてmanifestへ載る。

1. `fallback-archive/<envelope-id>.json` が存在し、job / attempt / kindを持つ。
2. `submissions/<kind>/<attempt-id>.json` のidentityがarchive envelopeと一致する。
3. `results/<kind>/<attempt-id>.json` が同じjob / attemptを持ち、`ok: true` である。
4. resultの `submission` がexact descriptor pathと一致する。
5. canonical jobがterminalで、resultの `job_status` と一致する。
6. completed attemptではcanonical jobの `artifact_submission` がexact descriptorを指す。
7. completed Researchではresult artifactのpaper path、job/envelope/descriptorのpaper path、実際のpaper artifactが一致する。

## Checkpoint-adopted rebound

旧attemptがstale-claim fencingで失敗した後、より新しいreleased claimがそのLibrary payloadを `checkpoint_ref` として明示的に採用している場合だけ、`.survey/scripts/retry_adopted_checkpoint_submissions.py` が再精読なしでtransport identityを新claimへrebindできる。

rebindは元の5-slot `data` を変更せず、job / attempt / claim / workerのtransport identityだけを新claimへ置き換える。新descriptorには必ず次のprovenanceを記録する。

- `source_fallback_envelope_id`: 元Library envelope id
- `source_attempt_id`: 元attempt id
- `source_claim_id`: 元claim id（存在する場合）

同じadopting attemptのdescriptorが既に存在する場合は再rebindしない。そこでvalidation failure等が発生している場合は通常のrepair経路が所有する。

reboundされたpayloadをACKする場合は、canonical completed jobの `artifact_submission` が新descriptorを指し、その新descriptorのprovenanceが元envelope id / 元attempt idと完全一致し、新attemptのdurable resultが `ok: true`、paper artifactまで一致することを要求する。manifest行には元 `attempt_id` に加えて `published_attempt_id` と `rebound: true` を記録する。

したがって、単なるstale claim、任意の別attemptによるterminal化、provenanceのない別submission、validation failure、paper未生成はACKされない。

## Library worker behavior

各 `acknowledgements[]` について:

1. `pending_path` に同じenvelope idのLibrary payloadが存在するか確認する。
2. payload内のjob / 元attempt / envelope id / kindがmanifest行と一致することを確認する。
3. 一致したpayloadだけ `processed_path` へmoveする。`published_attempt_id` がある場合でもLibrary payload側の元attempt identityを書き換えない。
4. 対応する `/LLM-survey-outbox/checkpoints/<job-id>.json` markerを `reflected` に更新し、`reflected_at` を記録する。
5. pendingに存在しない場合はprocessed側を確認し、既に同一payloadがあるならidempotent successとして扱う。

manifestの `waiting[]` は移動禁止である。理由が `result_not_successful`、`job_not_terminal`、`job_owned_by_different_submission` 等の場合、再精読せず既存checkpoint/recovery経路で処理する。

## Safety rule

`processed/` は publication ACK 済みを意味する。GitHub intake、fallback archive、descriptor生成、またはprovenanceのない別attemptの成功だけでは `processed/` へ移してはならない。
