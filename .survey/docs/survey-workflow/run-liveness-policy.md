# Run liveness, asynchronous waits, and finalization permit

本書はScheduled Chat / Work系workerの **run継続、非同期結果待機の正確なcadence、final responseを出してよい条件** の正本とする。実際の作業内容・queue semantics・claim ownership・fallback semanticsは `worker-router.md`、`always-on-worker.md`、`claim-serial-policy.md`、`fallback-routing.md`、`library-publication-ack.md` 等の専門正本を使う。本書はそれらの処理中に「待つか・続けるか・終了してよいか」を機械的に固定する。

重要な原則は2つだけである。

1. 次の判断または安全な状態遷移に非同期結果が必要な場合は、**必要結果がterminalになるまで待機する**。確認間隔は **10秒の実時間polling** とし、同じresult target identityを保持したまま `10秒実時間待機 → 同じ対象を再取得 → pendingなら再び10秒実時間待機` を繰り返す。
2. normal final responseは `.survey/scripts/run_finalization_gate.py` が `MAY_FINALIZE` かつ `finalization_permit.issued=true` を返した場合だけ許可する。許可なしにfinal responseを出してはならない。

ただし、既存契約上「結果を待たず別の独立作業へ進める」箇所では待機を新しい同期障壁にしない。例えばResearch/Auditのimmutable descriptorを耐久保存した後、前jobのsubmission-fast terminal反映を待つ必要がなければ、10秒pollingを開始せず次の独立作業へ進む。**10秒pollingを新しい同期障壁にしない。10秒wait loopは、次の判断または安全な状態遷移にその非同期結果が実際に必要な場合にだけ使う。**

## 1. Finalization permit

run終了前は必ず次の順で判定する。

1. 最新canonical stateを再取得し、`continuation-policy.json` / `.survey/scripts/continuation_gate.py` を評価する。
2. continuation result、active assignment、claim/submission/ACK pending、hard stop、safe handoff状態を `.survey/scripts/run_finalization_gate.py` へ渡す。
3. `decision=MUST_CONTINUE` または `finalization_permit.issued=false` ならfinal responseは禁止し、返された `next_action` を同じinvocation内で実行する。
4. 通常workerはgate呼び出し直前に最新のclaim request/result対応を実際に確認する。確認済みの場合だけ `--claim-state-checked yes` を渡す。最新requestのresultが未生成・queued・in_progressなら `--claim-result-pending yes` も渡す。状態確認を省略するとgateは `CHECK_CLAIM_STATE` を返し、finalization permitを発行しない。
5. `decision=MAY_FINALIZE` かつ `finalization_permit.issued=true` の場合だけnormal final responseを出せる。

`continuation_gate.py` が `CONTINUE` の間はfinalization permitを発行しない。有効なResearch/Audit assignmentが未処理の間もpermitを発行しない。claim result、submission result、Library ACK等の必要結果がpendingならpermitを発行しない。

hard platform/runtime limit、run deadline handoff guard、canonical read不能等の明示的hard stopでは、未保存成果・active assignment・pending transportを安全な耐久状態へhandoffしたことを確認した後だけhard-stop finalizationを許す。プラットフォームが外部からinvocationを強制終了しpermitを取得できなかった場合、そのrunをcanonicalな正常終了とはみなさず、次runはactive claim / checkpoint / pending resultから回復する。

## 2. Claim result待機

claim requestを `.survey/work-queue/claim-requests/<request_id>.json` へ耐久保存した後、対応する `.survey/work-queue/claim-results/<request_id>.json` がまだ無い場合は、**同じrequest_idを保持したまま10秒の実時間待機を行う。** この待機は文言上の待機ではなく、利用可能なruntime wait機構（例: Pythonの `time.sleep(10)` 相当）を実際に呼び出し、10秒の実時間を経過させることを意味する。実時間待機の代わりに即時再取得を連続実行したり、「待った」と記述するだけで代替してはならない。

10秒の実時間待機が完了した後でのみ、最新HEADと同じclaim resultを再取得する。まだ結果がpendingなら、**同じrequest_idを保持したまま再び10秒の実時間待機を実行し、同じclaim resultを再取得する。** claim resultまたは対応Actionsがterminalになるか、明示的hard stopが成立するまでこのruntime wait loopを繰り返す。

pending中に別request_idを発行しない。queued / in_progress / 404 / not foundは単独では失敗でもSTOP_RUNでもない。Actions runを確認できる場合も、同じpush/runを対象に10秒の実時間待機と再確認を繰り返す。assignmentが得られたら待機を終え、直ちにそのResearch/Audit実作業へ進む。

run deadlineのhandoff guardに入るまでは、pendingが続くこと自体を理由にloopを抜けない。handoff guard、明示的platform/tool failure、canonical read不能など正本所定のhard stopへ到達した場合だけ、安全な耐久handoffを行った後にfinalization gateを再評価する。

## 3. Research / Audit submission result待機

5-slot + immutable descriptorをGitHubへ耐久保存済みなら、通常throughputでは前jobのsubmission terminal結果を待たず次の独立作業へ進む。これは `always-on-worker.md` のwork-conserving契約を維持するためであり、10秒pollingを新しい同期障壁にしない。

一方、recovery、result validation、terminal ownership確認などで **同じsubmission resultが次の判断に必須** になった場合は、その同じjob / attempt / descriptorを保持し、**10秒の実時間待機 → 同じsubmission resultまたは対応Actionsを再取得**する。未確定なら再び10秒の実時間待機を行い、同じ対象がterminalになるまで繰り返す。実時間待機はruntime wait機構を実際に使い、即時再取得の連打で代替してはならない。pendingだからという理由で同一descriptorを重複submitせず、別attemptを勝手に作らない。

terminal failureが確定した場合だけ専門正本のrecoveryへ移る。failure確定前のqueued / in_progressを理由にretry payloadを増やさない。handoff guard等の明示的hard stopへ到達した場合だけ安全なhandoffへ移る。

## 4. Library publication ACK待機

Library `/LLM-survey-outbox/pending/` のpayloadについてpublication ACKまたはdispositionが次の判断に必要な場合、**同じenvelope / checkpoint / `library-ack-manifest.json` の対象行を保持して10秒の実時間待機**し、その後に同じ対象を再取得する。まだ `waiting[]` などpendingなら再び10秒の実時間待機を行い、`acknowledgements[]` / `superseded[]` / 明示的失敗など対象がterminalへ確定するまで繰り返す。実時間待機を即時再取得で代替してはならない。

ただし別の独立作業を安全に進められる契約なら、ACK待ちを同期障壁にせずその作業を先に進めてよい。ACK未確定中にLibrary payloadを`processed/`や`superseded/`へ推測移動せず、同じpayloadを重複checkpointしない。再送はcanonical recovery契約がconfirmed failure / orphan等を根拠に要求した場合だけ行う。

## 5. Fallback replay / materialization待機

fallback-inboxへ送ったenvelopeのreplay、record bank materialization、archive/result反映などが次の判断に必要な場合、**同じenvelope ID / replay対象を保持して10秒の実時間待機**し、最新canonical stateから同じresult / inbox / archive状態を再取得する。未確定なら再び10秒の実時間待機を行い、同じ対象がterminalになるまで確認を繰り返す。runtime waitを実際に使い、即時再取得の連打で代替してはならない。

pending replay中に同じenvelopeを別IDで再投入せず、同じIDの内容を変更して上書きしない。安全なbankが無くdeferredになった場合は専門正本に従いdeferred状態を維持し、単なる待機時間経過をfailure扱いしない。handoff guard等のhard stopに到達した場合だけ安全なhandoffへ移る。

## 6. GitHub Actions / その他の非同期結果待機

GitHub Actions、background dispatcher、maintenance result等、特定の非同期結果を **その場で待つ必要がある場合** は、対象run / request / descriptor / result identityを固定し、**10秒の実時間待機 → 同じ対象を再取得**する。queued / in_progress / result未生成なら再び10秒の実時間待機を行い、結果またはActions run等の対象がterminalになるまで同じ確認を繰り返す。runtime waitを実際に使い、即時再取得の連打で代替してはならない。

pollのたびに新しいActions runを起動したり、同じrequest/submissionを複製したりしない。結果を待つ必要がなく独立作業へ進める場合は、sleepでworkerをidleにせず独立作業を続ける。handoff guard等の明示的hard stopに到達した場合だけ安全なhandoffへ移る。

## 7. 10秒wait loopの共通形

結果待機が必要なすべての箇所は次の形に統一する。

```text
while required_result_is_pending:
    if explicit_hard_stop_is_true:
        durably_save_or_handoff_current_state()
        recheck_finalization_gate()
        break
    invoke_runtime_wait_for_10_real_seconds()
    refresh_latest_canonical_state()
    reread_the_same_result_target()
```

`invoke_runtime_wait_for_10_real_seconds()` は利用可能な実行環境のtimer/sleep機構を実際に使う。即時tool callの連打、同じ対象の即時再取得、自然言語で待機したと述べることは実時間runtime waitの代替ではない。

「10秒を1回待った」「Actionsがまだin_progressだった」「結果ファイルがまだ404だった」は終了条件ではない。**必要結果がterminalになるまで10秒実時間pollingを繰り返す。** 途中でrun deadlineのhandoff guard等のhard stopが成立した場合だけsafe handoffへ移る。

## 8. 次runでの強制回復

finalization permitなしにinvocationが外部要因で途切れた場合、次runは前runのfinal textを完了証拠に使わない。GitHub canonical state、active claim、claim result、immutable descriptor、Library checkpoint/pending、ACK manifestから未完了状態を復元する。

- active assignmentがあり成果未保存なら、そのassignmentを再開する。
- 完全payloadが既にdurableなら再精読せずsubmission/ACK/recoveryを再開する。
- claim requestだけ存在しresult待ちなら同じrequest_idを再確認する。
- 必要な非同期結果がpendingなら本書の10秒wait loopへ戻る。

これにより、モデルが誤って一区切りと判断した場合やプラットフォームがinvocationを切断した場合でも、canonical state上の未完了作業は次runへ残り、正常終了として固定されない。
