# Library publication acknowledgement contract

`/LLM-survey-outbox/pending/` のpayloadについて、GitHub canonical stateを根拠に「publication済み」「別attemptにより不要」「まだ回復が必要」を判定する契約を定義する。

## Authoritative manifest

GitHub Actionsは `.survey/scripts/library_ack_manifest.py` を実行し、派生ファイル `.survey/work-queue/library-ack-manifest.json` を生成する。

Scheduled ChatはLibrary payloadを移動する前に必ずこのmanifestを確認する。`fallback-archive` にあること、paperが存在すること、jobがterminalに見えること等をScheduled Chat側で個別推測して代用してはならない。

manifestは相互排他的な3分類を持つ。

- `acknowledgements[]`: このpayload自身、または明示的provenanceを持つreboundがcanonical publicationへ反映済み。`processed/`へ移動可能。
- `superseded[]`: 同じcanonical jobが別のimmutable attemptで正常publication済み。この古いpayloadは不要なので`superseded/`へ移動可能。
- `waiting[]`: publication/recovery未確定。`pending/`から移動禁止。

## Direct acknowledgement

通常はexact attempt単位で判定する。次のすべてを満たす場合だけ `status=reflected` として `acknowledgements[]` へ載る。

1. `fallback-archive/<envelope-id>.json` が存在し、job / attempt / kindを持つ。
2. `submissions/<kind>/<attempt-id>.json` のidentityがarchive envelopeと一致する。
3. `results/<kind>/<attempt-id>.json` が同じjob / attemptを持ち、`ok: true` である。
4. resultの `submission` がexact descriptor pathと一致する。
5. canonical jobがterminalで、resultの `job_status` と一致する。
6. completed attemptではcanonical jobの `artifact_submission` がexact descriptorを指す。
7. completed Researchではresult artifactのpaper path、job/envelope/descriptorのpaper path、実際のpaper artifactが一致する。

## Checkpoint-adopted rebound

旧attemptがstale-claim fencingで失敗した後、より新しいreleased claimがそのLibrary payloadを `checkpoint_ref` として明示的に採用している場合だけ、`.survey/scripts/retry_adopted_checkpoint_submissions.py` が再精読なしでtransport identityを新claimへrebindできる。

新descriptorは元payloadとのprovenanceとして少なくとも `source_fallback_envelope_id` と `source_attempt_id` を持つ。canonical completed jobの `artifact_submission` がこのdescriptorを指し、新attemptのdurable resultが `ok: true`、Researchならpaper artifactも一致する場合だけ元payloadを `acknowledgements[]` に載せる。manifest行には `published_attempt_id` と `rebound: true` を付ける。

## Superseded disposition

元payload自身がpublicationに使われていなくても、同じcanonical jobが**別attemptで完全に正常完了**したことを機械的に証明できれば、元payloadを `superseded[]` に載せる。

completed jobでは次をすべて要求する。

1. canonical jobの `artifact_submission` が同じkind/jobの別attempt descriptorを指す。
2. その別attemptのdurable resultが同じjob/attempt/submissionを持ち `ok: true`、`job_status: completed` である。
3. resultとcanonical jobの所有関係が一致する。
4. completed Researchではresult artifactのpaper pathとcanonical paper pathが一致し、実際のpaper artifactが存在する。

rejected jobについても `status_submission` が別attemptのsuccessful resultによりcanonical ownershipを持つ場合に限り同様に扱う。

`superseded` は「元payloadがpublicationされた」という意味ではない。そのため `processed/` へは入れず、次へ移す。

`/LLM-survey-outbox/superseded/<envelope-id>.json`

jobがready/nonterminal、canonical resultが成功していない、所有submissionが不明、Research paperが無い等の場合はsuperseded判定しない。

## Library worker behavior

`acknowledgements[]` について:

1. `pending_path` のLibrary payloadを読み、envelope id / job id / 元attempt id / kindがmanifest行と一致することを確認する。
2. 一致したpayloadだけ `processed_path` へmoveする。
3. checkpoint markerを `reflected` に更新する。
4. pendingに無い場合はprocessed側の同一payloadを確認し、既に移動済みならidempotent successとする。

`superseded[]` について:

1. `pending_path` のLibrary payload identityをmanifest行と照合する。
2. 一致したpayloadだけ `superseded_path` へmoveする。
3. checkpoint markerが同じ元attemptを指す場合は `superseded` として記録し、claim barrier用途から外す。canonical jobは既にterminalなので再精読しない。
4. pendingに無い場合はsuperseded側を確認し、同一payloadならidempotent successとする。

`waiting[]` は移動禁止である。`result_not_successful`、`job_not_terminal`、`descriptor_missing` 等でも、canonical別attemptの成功が証明されない限り再精読せず既存checkpoint/recovery経路で処理する。

## Safety rule

- `processed/`: このLibrary payloadの内容がcanonical publicationへ反映済み。
- `superseded/`: 同じjobの別attemptがcanonical publicationを完了し、このpayloadは不要。
- `pending/`: まだpublication/recovery上の意味を持つ。

GitHub intake、fallback archive、descriptor生成、単なる別attemptの存在だけでは、どのterminal分類にも移してはならない。
