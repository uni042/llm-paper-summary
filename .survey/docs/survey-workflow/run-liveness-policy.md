# Run liveness, asynchronous waits, and finalization permit

本書はScheduled Chat / Work系workerのrun継続、非同期結果待機、normal final responseを出してよい条件の正本とする。実作業内容とqueue/claim/fallback semanticsは `worker-router.md`、`always-on-worker.md`、`claim-serial-policy.md`、`fallback-routing.md`、`library-publication-ack.md` 等の専門正本を使う。

重要原則は次である。

1. 通常runの正常終了は実開始基準のrun-local handoff guardだけで決める。`run_deadline = actual_invocation_start + 3600 seconds` とし、600秒以下で新規独立作業を止め、安全なhandoffへ移る。
2. round数、candidate数、submission数、Research/Audit完了数、探索枯渇、在庫状態はnormal finalizationを許可しない。
3. canonical read不能、GitHub/Library双方のdurability failure、tool/platform側の異常等はnormal successの停止理由ではなく異常blockerとして扱う。回復可能なら回復し、回復不能でも正常完了へ変換しない。
4. 結果待ちが必要な箇所では **30秒待機 → 同じ結果対象を再取得 → 未確定なら再び30秒待機** を繰り返す。
5. normal final responseは `.survey/scripts/run_finalization_gate.py` が `MAY_FINALIZE` かつ `finalization_permit.issued=true` を返した場合だけ許可する。**許可なしにfinal responseを出してはならない。**

既存契約上、結果を待たず別の独立作業へ進める箇所では待機を新しい同期障壁にしない。Research/Audit descriptorを耐久保存済みで前jobのterminal反映が次判断に不要なら、30秒sleepせず次の独立作業へ進む。**30秒待機を新しい同期障壁にしない。**

## 1. Finalization permit

run終了前は必ず次の順で判定する。

1. 最新canonical stateを再取得し、`continuation-policy.json` / `.survey/scripts/continuation_gate.py` を評価する。
2. continuation result、active assignment、claim/submission/ACK pending、異常blocker、安全なhandoff状態を `.survey/scripts/run_finalization_gate.py` へ渡す。
3. `decision=MUST_CONTINUE` または `finalization_permit.issued=false` ならnormal final responseは禁止し、返された `next_action` に従う。
4. `decision=MAY_FINALIZE` かつ `finalization_permit.issued=true` の場合だけnormal final responseを出せる。

通常runで `STOP_RUN` とnormal finalizationを生むのは、実開始基準run deadlineがhandoff guard内へ入った場合だけである。予定`:00`/`:30`境界はactual-start deadlineを得られないlegacy caller向け互換フォールバック（compatibility fallback）に限る。

canonical read不能、耐久保存不能、platform/tool異常等の非時間blockerは、safe handoff済みであってもnormal finalization permitを発行する根拠にはしない。回復可能なら同一invocation内で回復を試みる。外部要因でinvocation自体が強制終了した場合、そのrunをcanonicalな正常終了とはみなさず、次runがactive claim / checkpoint / pending resultから回復する。

## 2. Claim result待機

claim requestを `.survey/work-queue/claim-requests/<request_id>.json` へ耐久保存した後、対応resultがまだ無い場合は、**同じrequest_idを保持したまま30秒待機**する。待機後に最新HEADと同じclaim resultを再取得する。未確定なら **再び30秒待機して同じrequest_idの確認を繰り返す**。

結果が出るか、run-local handoff guardへ入るまで同じ対象を追う。pending中に別request_idを発行しない。queued / in_progress / 404 / not foundだけを正常終了理由にしない。assignmentが得られたら直ちにResearch/Audit実作業へ進む。

異常failureが確定した場合は専門正本のrecoveryへ進むが、それ自体をnormal success finalizationへ変換しない。

## 3. Research / Audit submission result待機

5-slot + immutable descriptorをGitHubへ耐久保存済みなら、通常throughputでは前jobのterminal結果を待たず次の独立作業へ進む。

recovery、validation、ownership確認等で **同じsubmission resultが次判断に必須** になった場合は、同じjob / attempt / descriptorを対象に **30秒待機 → 同じsubmission resultまたは対応Actionsを再取得** する。未確定なら **再び30秒待機して同じ対象の確認を繰り返す**。

pendingだからという理由で同一descriptorを重複submitしない。別attemptを勝手に作らない。terminal failureが確定した場合だけ専門recoveryへ移る。queued / in_progressだけでnormal finalizationしない。

## 4. Library publication ACK待機

Library `/LLM-survey-outbox/pending/` のpayloadについてACK/dispositionが次判断に必要な場合、**同じenvelope / checkpoint / `library-ack-manifest.json` の対象を保持して30秒待機**し、その後に同じ対象を再取得する。未確定なら **再び30秒待機して同じ対象の確認を繰り返す**。

ただし別の独立作業を安全に進められる契約なら、ACK待ちを同期障壁にせずその作業を先に進める。ACK未確定中にLibrary payloadを推測でprocessed/supersededへ移さず、重複checkpointしない。

## 5. Fallback replay / materialization待機

fallback-inboxへ送ったenvelopeのreplay、record bank materialization、archive/result反映が次判断に必要な場合、**同じenvelope ID / replay対象を保持して30秒待機**し、最新canonical stateから同じresult / inbox / archive状態を再取得する。未確定なら **再び30秒待機して同じ対象の確認を繰り返す**。

pending replay中に同じenvelopeを別IDで再投入しない。同じIDの内容を変更して上書きしない。deferredになった場合は専門正本に従い状態を維持し、待機時間経過だけをfailure扱いしない。

## 6. GitHub Actions / その他の非同期結果待機

GitHub Actions、background dispatcher、maintenance result等、特定の非同期結果をその場で待つ必要がある場合は、対象run / request / descriptor / result identityを固定し、**30秒待機 → 同じ対象を再取得**する。queued / in_progress / result未生成なら、**再び30秒待機して同じ対象の確認を繰り返す**。

pollごとに新しいActions runを起動したり、同じrequest/submissionを複製したりしない。結果を待つ必要がなく独立作業へ進める場合はsleepでidleにせず独立作業を続ける。

## 7. 30秒wait loopの共通形

結果待機が必要な箇所は次の形に統一する。

```text
while required_result_is_pending:
    if run_deadline_handoff_guard_is_active:
        durably_save_or_handoff_current_state()
        recheck_finalization_gate()
        break
    if abnormal_blocker_is_confirmed:
        attempt_canonical_recovery_or_preserve_evidence()
        continue_or_leave_state_for_next_run_without_normal_success()
    wait 30 seconds
    refresh_latest_canonical_state()
    reread_the_same_result_target()
```

「30秒を1回待った」「Actionsがまだin_progress」「結果ファイルが404」は正常終了条件ではない。30秒待機を結果が出るまで繰り返す。normal finalizationへ移るのはrun-local handoff guardが成立し、finalization permitが発行された場合だけである。

## 8. 次runでの強制回復

finalization permitなしにinvocationが外部要因で途切れた場合、次runは前runのfinal textを完了証拠に使わない。GitHub canonical state、active claim、claim result、immutable descriptor、Library checkpoint/pending、ACK manifestから未完了状態を復元する。

- active assignmentがあり成果未保存なら、そのassignmentを再開する。
- 完全payloadがdurableなら再精読せずsubmission/ACK/recoveryを再開する。
- claim requestだけ存在しresult待ちなら同じrequest_idを再確認する。
- 必要な非同期結果がpendingなら本書の30秒wait loopへ戻る。

これにより、モデルの一区切り判断、探索枯渇判断、非時間blocker、または外部platform終了がnormal completionとして固定されない。
