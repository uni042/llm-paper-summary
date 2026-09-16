# Run liveness, asynchronous waits, and finalization permit

本書はScheduled Chat / Work系workerの **run継続、非同期結果待機のcadence、final responseを出してよい条件** の正本とする。実際の作業内容・queue semantics・claim ownership・fallback semanticsは `worker-router.md`、`always-on-worker.md`、`claim-serial-policy.md`、`fallback-routing.md`、`library-publication-ack.md` 等の専門正本を使う。本書はそれらの処理中に「待つか・続けるか・終了してよいか」を機械的に決める。

## 0. Decision authority

worker自身に「時間まで絶対に終わるな」という主観的な継続判断は要求しない。終了可否は `.survey/scripts/continuation_gate.py` と `.survey/scripts/run_finalization_gate.py` が決める。workerの役割は、観測可能なcanonical stateを正確に取得してscriptへ渡し、返された `decision` / `required_action` / `next_action` / `finalization_permit` をそのまま実行することである。

したがって、停止を正当化するために存在しないエラー、platform/runtime limit、canonical read failure、durable-save failure、探索枯渇などを推測・生成する必要はない。終了報告には実際に観測できたstate/errorとgate出力だけを使う。外部プラットフォームがinvocationを強制終了した場合はfinal response自体が出ないので、workerが事前にそれを予測してstop理由へ変換しない。

重要な原則は2つである。

1. 結果待ちが必要な箇所では、短い任意間隔のpollや「少し待った」判断を使わず、**30秒待機 → 同じ結果対象を再取得 → 未確定なら再び30秒待機**を結果が出るまで繰り返す。
2. normal final responseは `.survey/scripts/run_finalization_gate.py` が `MAY_FINALIZE` かつ `finalization_permit.issued=true` を返した場合に行う。それ以外ではscriptが返す次のactionを処理する。

ただし、既存契約上「結果を待たず別の独立作業へ進める」箇所では待機を新しい同期障壁にしない。例えばResearch/Auditのimmutable descriptorを耐久保存した後、前jobのsubmission-fast terminal反映を待つ必要がなければ、30秒sleepせず次の独立作業へ進む。30秒ループは、次の判断または安全な状態遷移にその非同期結果が実際に必要な場合だけ使う。

## 1. Finalization permit

final response候補地点では次の順で判定する。

1. 最新canonical stateを再取得し、`continuation-policy.json` / `.survey/scripts/continuation_gate.py` を評価する。
2. continuation result、active assignment、claim/submission/ACK pending、observed stop state、safe handoff状態を `.survey/scripts/run_finalization_gate.py` へ渡す。
3. `decision=MUST_CONTINUE` または `finalization_permit.issued=false` なら、返された `next_action` を同じinvocation内で実行する。
4. `decision=MAY_FINALIZE` かつ `finalization_permit.issued=true` ならnormal final responseを出す。

`continuation_gate.py` が `CONTINUE` の間はfinalization permitは発行されない。有効なResearch/Audit assignmentが未処理の場合や、次の安全な状態遷移に必要なclaim result、submission result、Library ACK等がpendingの場合もfinalization gateが次のactionを返す。

run deadline handoff guard、canonical read不能、必要成果をどの承認済み経路にも耐久保存できない等の明示的状態では、現在の成果・assignment・pending transportを安全な耐久状態へhandoffした上でgateを再評価する。外部からinvocationが強制終了されpermitを取得できなかった場合、そのrunをcanonicalな正常終了とはみなさず、次runはactive claim / checkpoint / pending resultから回復する。

`platform_limit` のような入力は、実際に観測可能な具体的状態がある場合だけ渡す。「長く動いている」「ツール回数が多い」「そろそろ切れそう」といった予測や感覚はその入力へ変換しない。

## 2. Claim result待機

claim requestを `.survey/work-queue/claim-requests/<request_id>.json` へ耐久保存した後、対応する `.survey/work-queue/claim-results/<request_id>.json` がまだ無い場合は、**同じrequest_idを保持したまま30秒待機する。** 待機後に最新HEADと同じclaim resultを再取得する。まだ結果が無ければ、**再び30秒待機して同じrequest_idの確認を繰り返す。** resultが出るか、対応Actionsがterminal failureになるか、gateが別actionを返す状態になるまで繰り返す。

pending中に別request_idを発行しない。queued / in_progress / 404 / not foundは単独では失敗でもSTOP_RUNでもない。Actions runを確認できる場合も、同じpush/runを対象に30秒待機と再確認を繰り返す。assignmentが得られたら待機を終え、そのResearch/Audit実作業へ進む。

## 3. Research / Audit submission result待機

5-slot + immutable descriptorをGitHubへ耐久保存済みなら、通常throughputでは前jobのsubmission terminal結果を待たず次の独立作業へ進む。これは `always-on-worker.md` のwork-conserving契約を維持するためであり、30秒待機を新しい同期障壁にしない。

一方、recovery、result validation、terminal ownership確認などで **同じsubmission resultが次の判断に必須** になった場合は、その同じjob / attempt / descriptorを対象に **30秒待機 → 同じsubmission resultまたは対応Actionsを再取得** する。未確定なら再び30秒待機し、結果が出るまで繰り返す。pendingだからという理由で同一descriptorを重複submitしない。別attemptを勝手に作らない。

terminal failureが確定した場合は専門正本のrecoveryへ移る。failure確定前のqueued / in_progressを理由にretry payloadを増やさない。

## 4. Library publication ACK待機

Library `/LLM-survey-outbox/pending/` のpayloadについてpublication ACKまたはdispositionが必要な場合、**同じenvelope / checkpoint / `library-ack-manifest.json` の対象行を保持して30秒待機**し、その後に同じ対象を再取得する。まだ `waiting[]` など未確定なら、再び30秒待機して同じ対象の確認を繰り返す。`acknowledgements[]` / `superseded[]` / 明示的失敗のいずれかへ確定するまで繰り返す。ただし別の独立作業を安全に進められる契約なら、ACK待ちを同期障壁にせずその作業を先に進めてよい。

ACK未確定中にLibrary payloadを`processed/`や`superseded/`へ推測移動しない。同じpayloadを重複checkpointしない。再送はcanonical recovery契約がconfirmed failure / orphan等を根拠に要求した場合だけ行う。

## 5. Fallback replay / materialization待機

fallback-inboxへ送ったenvelopeのreplay、record bank materialization、archive/result反映などが次の判断に必要な場合、**同じenvelope ID / replay対象を保持して30秒待機**し、最新canonical stateから同じresult / inbox / archive状態を再取得する。未確定なら再び30秒待機し、同じ対象の確認を結果が出るまで繰り返す。

pending replay中に同じenvelopeを別IDで再投入しない。同じIDの内容を変更して上書きしない。安全なbankが無くdeferredになった場合は専門正本に従いdeferred状態を維持し、単なる待機時間経過をfailure扱いしない。

## 6. GitHub Actions / その他の非同期結果待機

GitHub Actions、background dispatcher、maintenance result等、特定の非同期結果を **その場で待つ必要がある場合** は、対象run / request / descriptor / result identityを固定し、**30秒待機 → 同じ対象を再取得**する。queued / in_progress / result未生成なら、再び30秒待機して同じ対象の確認を繰り返す。結果またはterminal stateが出るまで繰り返す。

pollのたびに新しいActions runを起動したり、同じrequest/submissionを複製したりしない。結果を待つ必要がなく独立作業へ進める場合は、sleepでworkerをidleにせず独立作業を続ける。

## 7. 30秒wait loopの共通形

結果待機が必要なすべての箇所は次の形に統一する。

```text
while required_result_is_pending:
    refresh_observable_state_for_gate()
    gate = evaluate_continuation_and_finalization()
    if gate selects a safe-handoff/finalization action:
        durably_save_or_handoff_current_state()
        reevaluate_gate()
        break
    wait 30 seconds
    refresh_latest_canonical_state()
    reread_the_same_result_target()
```

「30秒を1回待った」「Actionsがまだin_progressだった」「結果ファイルがまだ404だった」は、それ自体をstop理由へ変換しない。必要な結果がpendingなら同じ対象で30秒cadenceを続け、別の独立作業を進められる場合はそちらを進める。終了判断はその都度gateへ戻す。

## 8. 次runでの回復

finalization permitなしにinvocationが外部要因で途切れた場合、次runは前runのfinal textを完了証拠に使わない。GitHub canonical state、active claim、claim result、immutable descriptor、Library checkpoint/pending、ACK manifestから未完了状態を復元する。

- active assignmentがあり成果未保存なら、そのassignmentを再開する。
- 完全payloadが既にdurableなら再精読せずsubmission/ACK/recoveryを再開する。
- claim requestだけ存在しresult待ちなら同じrequest_idを再確認する。
- 必要な非同期結果がpendingなら本書の30秒wait loopへ戻る。

この構造ではworkerが「続けるべきか」を心理的に判断する必要がない。canonical stateとgate出力がrunの継続・handoff・finalizationを一貫して決める。
