# Discovery exhaustive-run policy

この文書は毎時`:00` JSTの探索主体Scheduled Chat workerが1回の実行枠をどう使うかを定める。役割分離は `discovery-specialist-worker.md`、candidate水位とoverflow切替は `candidate-buffer-policy.md`、run終了可否は `continuation-policy.json` / `continuation_gate.py` / `run_finalization_gate.py` を正本とする。

## 終了判断はgateへ委譲する

worker自身が「時間まで絶対に働き続ける」「探索空間を使い切ったから終わる」のどちらかを主観で選ぶ設計にはしない。workerは最新canonical stateと実測時間を取得し、gateへ渡して返されたactionに従う。

停止を正当化するために、存在しないplatform/runtime/tool limit、canonical read failure、durable-save failure、探索枯渇を推測・生成しない。観測できた具体的state/errorだけを入力する。外部プラットフォームが強制終了する場合はworkerが事前にそれをstop理由として予測しない。

## 実開始基準のScheduled Chat引き継ぎガード

探索主体workerは実際のScheduled Chat invocation開始時刻を1回だけ固定し、`run_deadline = actual_start + 3600s` とする。overflow research modeへ切り替わっても同じdeadlineを使う。

新しいdiscovery round、探索軸、submission作成単位、Research/Audit claimを始める前、および各耐久checkpoint後にrun deadlineまでの残秒を再計算し `continuation_gate.py --seconds-to-run-deadline` へ渡す。予定`:00`までの残り時間はactual-start deadlineを確定できない旧caller向けcompatibility fallbackに限る。

600秒handoff guardや180秒finalization帯の扱いはscript出力を正本とし、worker側で独自に前倒し・延長しない。

## Candidate件数とtransport chunk

run全体のcandidate件数に最低quotaやhard capは設けない。弱いcandidateで件数を埋めず、品質基準を満たす候補を保存する。

workflow-v10の現行queue contractでは1 immutable discovery submissionを **0〜5 candidates** に制限する。5件はtransport chunkの上限であり、1 round/runの探索上限ではない。強いdedupe済みcandidateが6件以上ある場合は、同じrun_keyの複数immutable submissionへ5件以下ずつ分割し、候補を捨てずに送る。5件到達やsubmission分割をrun終了理由にしない。

## Discovery mode loop

Discovery modeでは次を1単位として処理する。

1. 最新HEAD、identity、queue、existing jobs、`discovery-state.json`、candidate inventory、actionable Research/Auditを取得する。
2. run deadline等の観測値をcontinuation gateへ渡し、返されたactionを確認する。
3. `candidate_inventory > 50` かつactionable Research/Auditありならoverflow research modeへ切り替える。
4. Discovery継続actionなら、直近roundと実質的に異なる探索軸を選ぶ。
5. title、abstract、書誌情報、一次資料の存在、テーマ適合性を軽量評価する。通常Discovery中は全文精読や5-slot作成を行わない。
6. canonical ID / arXiv ID / DOI / OpenReview ID / normalized titleで重複除外する。
7. 強いcandidateを1 payload最大5件のimmutable discovery submissionへ必要数だけ分割して耐久保存する。0件の場合も観測可能性のため空submissionを保存する。
8. `discovery_stats` にrun_key、round、axis、query summary、candidate数、重複数、empty reason、next-axis hintを残す。
9. 最新canonical stateを再取得し、gateへ戻る。

round数・submission数・candidate数には終了ノルマを置かない。0件round、全重複round、同じrun内で多数roundを完了したこと、現在のnext-axis hintが空であることも、それ自体を正常終了許可には変換しない。

## 耐久実行記録

Discovery modeへ1回でも入った`:00` runでは、そのrunで固定した `run_key` を持つdiscovery submissionを正規の耐久経路へ残す。

GitHub write可能時はworkflow-v10 discovery submissionを使用する。強い新規candidateが0件、全候補が重複、最終dedupeで0件になった場合も `candidates: []` と実際の `candidate_count`、`duplicate_filtered_count`、`duplicate_canonical_ids`、`next_axis_hint`、具体的な `empty_round_reason` を保存する。候補が5件を超える場合は同一run_keyの複数submissionへ分割する。

GitHub directが使えない場合は `fallback-routing.md` が認めるChatGPT Library経路を使用する。GitHub directと承認済みLibrary fallbackの両方で必要状態を保存できないことが実際に確認された場合、その事実をcontinuation gateへ渡す。

run開始から最後までoverflow research modeだけでDiscovery modeへ入らなかった場合、空discovery submissionは不要で、Research/Auditの完全payloadの耐久保存を成果証跡とする。

## Overflow research mode loop

Overflow research modeでは `always-on-worker.md` / `claim-serial-policy.md` / `run-liveness-policy.md` を適用する。

1. 最新queue / claim / checkpoint stateを取得しgateを評価する。
2. actionable Research/Auditがありgateが継続actionを返した場合、eligible jobをpriority順に1件claimする。
3. 一次資料全文を取得・精読し、repository-qualityの5-slot structured recordを作る。
4. claim resultで予約されたrecord bankへ保存し、preflightを通す。
5. attempt固有immutable descriptorまたはLibrary checkpointへ完全payloadを耐久保存する。
6. 次の判断にterminal結果が不要なら待たず、最新stateとgateを再評価する。必要なら同一対象を30秒cadenceで再取得する。
7. `candidate_inventory <= 50` またはactionable Research/AuditなしならDiscovery modeへ戻る。

1 workerが同時に保持する未完了claimは1件だけ。完了件数に「最低3件」等のノルマも「3件で終了」等の終了条件も置かない。件数はthroughput指標として記録し、終了可否はgateが決める。

## 探索空間の回し方

候補軸には新着・revision、forward citation、backward reference、DBMS/OS/storage/distributed systems/HPC/GPU runtime/networking/memory systems等の隣接分野、直近採用candidateからのquery expansion、offload/hierarchical memory/SSD/NVMe/MoE expert placement・cache・prefetch/KV cache/scheduling/disaggregation/inference framework等を含める。

高重複・低採用率の軸は機械的に直後反復せず、別軸へ移る。ここでいう「探索空間の枯渇」は検索戦略の診断値として記録できるが、正常終了許可には使わない。`discovery_exhausted`、round数、最後のnovel candidateからのround数はcontinuation gateではtelemetryでありstop権限を持たない。

## 非同期結果

claim result、submission result、Library ACK等が次の判断に必要なら `run-liveness-policy.md` に従い対象identityを固定して30秒待機・再取得を繰り返す。別の独立作業が可能なら待機を同期障壁にしない。queued / in_progress / 404 / result未生成をworker独自のstop理由へ変換しない。

## Finalization flow

final response候補地点では必ず最新stateを取得し、まず `continuation_gate.py`、次に `run_finalization_gate.py` を評価する。

`CONTINUE` / `MUST_CONTINUE` の場合はscriptが返したactionを処理する。`STOP_RUN` はそれだけでnormal final responseの許可ではなく、active assignment・pending transport・safe handoffを含めたfinalization gateが `MAY_FINALIZE` かつ `finalization_permit.issued=true` を返した場合に正常終了する。

終了報告にstop reasonを記す場合はscript出力と、その根拠になった具体的canonical state/errorを使う。workerが曖昧な停止理由を創作しない。
