# Library publication acknowledgement contract

`/LLM-survey-outbox/pending/` から `/LLM-survey-outbox/processed/` へpayloadを移すためのGitHub側の判定契約を定義する。

## Authoritative manifest

GitHub Actionsは `.survey/scripts/library_ack_manifest.py` を実行し、派生ファイル `.survey/work-queue/library-ack-manifest.json` を生成する。

Scheduled ChatはLibrary payloadを `processed/` へ移す前に、必ずこのmanifestの `acknowledgements` を確認する。`fallback-archive` にあること、paperが存在すること、jobがterminalに見えること等をScheduled Chat側で個別推測して代用してはならない。

ACK対象はexact attempt単位で判定する。次のすべてを満たす場合だけ `status=reflected` としてmanifestへ載る。

1. `fallback-archive/<envelope-id>.json` が存在し、job / attempt / kindを持つ。
2. `submissions/<kind>/<attempt-id>.json` のidentityがarchive envelopeと一致する。
3. `results/<kind>/<attempt-id>.json` が同じjob / attemptを持ち、`ok: true` である。
4. resultの `submission` がexact descriptor pathと一致する。
5. canonical jobがterminalで、resultの `job_status` と一致する。
6. completed attemptではcanonical jobの `artifact_submission` がexact descriptorを指す。
7. completed Researchではresult artifactのpaper path、job/envelope/descriptorのpaper path、実際のpaper artifactが一致する。

したがって、stale claim、validation failure、別attemptによるterminal化、paper未生成はACKされない。

## Library worker behavior

各 `acknowledgements[]` について:

1. `pending_path` に同じenvelope idのLibrary payloadが存在するか確認する。
2. payload内のjob / attempt / envelope idがmanifest行と一致することを確認する。
3. 一致したpayloadだけ `processed_path` へmoveする。
4. 対応する `/LLM-survey-outbox/checkpoints/<job-id>.json` markerを `reflected` に更新し、`reflected_at` を記録する。
5. pendingに存在しない場合はprocessed側を確認し、既に同一payloadがあるならidempotent successとして扱う。

manifestの `waiting[]` は移動禁止である。理由が `result_not_successful`、`job_not_terminal`、`job_owned_by_different_submission` 等の場合、再精読せず既存checkpoint/recovery経路で処理する。

## Safety rule

`processed/` は publication ACK 済みを意味する。GitHub intake、fallback archive、descriptor生成だけでは `processed/` へ移してはならない。
