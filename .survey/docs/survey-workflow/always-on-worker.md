# Always-on paper worker policy

本書は通常論文workerの **run内継続・待ち時間削減・可視queueの扱い** の正本とする。discoveryは `discovery-continuation-policy.md` / `discovery-exhaustive-run-policy.md`、transportは `fallback-routing.md` / `queue-v10.md`、claim同時保有数は `claim-serial-policy.md`、run継続と終了可否は `continuation-policy.json` / `continuation_gate.py` / `run_finalization_gate.py` を正本とする。

worker自身へ「可能な限り絶対に続ける」ことを要求しない。workerはcanonical stateを観測し、gateへ渡し、返されたactionを処理する。継続・handoff・終了はscriptが決める。停止を正当化するために、存在しないplatform limit、read failure、durability failure、探索枯渇等を推測・生成しない。

## 0. 実開始基準のScheduled Chat引き継ぎガード

毎時`:30`の通常論文workerは、実際のScheduled Chat invocation開始時刻を1回だけ固定し、`run_deadline = actual_start + 3600秒` とする。予定`:30`からの早起動・遅延で今回runのrun-local budgetを短縮しない。

新しい独立作業の前と各耐久checkpoint後にrun deadlineまでの残秒を測定し、`continuation_gate.py --seconds-to-run-deadline` へ渡す。`--seconds-to-next-scheduled-task` はactual-start deadlineを確定できない旧caller向けcompatibility fallbackに限る。

600秒handoff guard、180秒finalization帯を含む判断はgate出力を正本とする。worker側で「もう近いから早めに終わる」「まだできそうだからguardを無視する」といった独自判断を加えない。未保存成果やactive claimがある場合は `run_finalization_gate.py` が返すsafe-handoff actionを処理し、permitを再評価する。

## 1. 論文ストック0はDiscovery入力

`actionable ready`、Library seed由来の`spillover_candidates`、その他処理可能なResearch/Auditが0件になった場合、その状態をcontinuation gateへ渡す。normal routeでgateがDiscoveryを指示した場合は直ちにdiscoveryを行う。

- GitHub write可能時は正規のdiscovery/queue transportを使う。
- GitHub write不能でもChatGPT Libraryへoffline job seedを耐久保存できる場合はその可用性をgateへ反映する。
- discoveryで新規候補が得られたら最新stateを再取得し、gateの次actionに従う。
- research/checkpoint後に再びストック0になった場合も同様に再評価する。

paper stock 0自体を正常終了理由へ変換しない。

## 2. Discovery件数・round数は終了権限を持たない

1探索roundで候補が全重複、弱候補のみ、新規0件、または既知axisを一巡しても、それ自体をrun stopへ変換しない。`discovery-state.json` と最新canonical stateを読み、観測値をgateへ渡す。継続actionなら探索軸・検索語・引用関係・関連実装・隣接テーマを変える。

workflow-v10の現行queue contractでは **1 immutable discovery submissionは0〜5 candidates** に制限する。これはrun全体のcandidate上限ではない。品質基準を満たすdedupe済みcandidateが5件を超える場合は捨てず、同じ `run_key` の複数immutable submissionへ5件以下ずつ分割してすべて耐久保存する。5件送信、1 submission完了、任意round数完了、candidate inventory増加、`discovery_exhausted`、`next_axis_hint`なしはいずれも終了許可ではない。

candidate在庫が25本以上ありactionable Research/Auditが存在する場合、通常workerはhigh-backlog research-only modeとし、新規discoveryを行わない。candidate在庫が25本未満、またはactionable Research/Auditが尽きた場合にDiscovery分岐を再評価する。`:00`探索主体workerは50超かつactionable Research/Auditありでoverflow research modeへ切り替わる。

既収録論文はarXiv ID、DOI、OpenReview ID、正規化タイトル等で詳細評価前に先行除外する。`discovery-state.json` はGitHub Actionsを単一writerとし、Scheduled Chat workerは共有stateを直接更新せず `discovery_stats` をsubmissionへ含める。

## 3. Actions待ちで独立作業を不要に止めない

Research/Auditについて、5 slot + attempt固有immutable descriptorがGitHubへ耐久保存済み、または完全payloadがChatGPT Libraryへ耐久checkpoint済みなら、Actions terminal反映が次判断に不要な場合は同期障壁にしない。

- 送信済み・checkpoint済みjob IDをrun内で保持し、GitHub上でまだ`ready`でも同じjobを再精読しない。
- descriptor送信後、terminal反映が次判断に不要なら最新queue/claim stateとgateを再取得する。
- 前jobが未保存の間は次jobを先取りclaimしない。
- 未解決immutable descriptorが参照するrecord bankはoccupiedとみなし上書きしない。
- 別bankが空いていれば次jobで使う。bankが空いていなくてもLibraryへ完全payloadを耐久保存できる場合はその経路を使う。
- terminal結果が次判断に必要な場合は `run-liveness-policy.md` の同一identity・30秒cadenceを使う。

GitHub Actionsはclaim、immutable submission、backgroundの3レーンに分離されている。background側のfallback、citation、maintenance、index処理が詰まってもclaim-fastの結果が独立して進められる場合はそちらを使う。

## 4. `next-jobs.json` の表示件数を仕事量上限にしない

`.survey/work-queue/next-jobs.json` はworker向け優先job snapshotであり、全ready jobの完全一覧とは限らない。`counts` が示すready件数が `next_jobs` のactionable表示数より多い場合、表示外readyが存在すると扱う。

表示上位jobがcheckpoint済み・処理中・局所blockedでも、`counts` に未処理readyが残る場合は必要に応じ `.survey/work-queue/jobs/` のjob実体を確認し、checkpoint済みjobを除いたpriority最上位の未処理jobを選ぶ。`next_jobs`表示枠、record bank数、Library pending件数、fallback-inbox件数はrun当たりの研究上限ではない。

## 5. 通常runの処理ループ

通常論文workerは各耐久checkpointを境に次を繰り返す。

1. 最新HEAD、candidate inventory、queue/backlog、claim/transport状態、run deadlineを取得する。
2. `continuation_gate.py` を評価し、返された `required_action` に従う。
3. Research/Audit actionなら `claim-serial-policy.md` に従いpriority最上位を1件だけclaimする。未完了claimを複数保有しない。
4. 一次資料全文を精読し、5-slot recordを作成してpreflightする。
5. GitHub正常時はrecord slots + attempt固有immutable descriptor、GitHub write不能時は承認済みLibrary fallbackへ完全payloadを耐久保存する。
6. 次判断にterminal結果が必要なら同じidentityを30秒cadenceで待つ。不要なら最新stateへ進む。
7. actionable Research/Auditがなく、gateがDiscovery actionを返した場合はDiscoveryを実行する。
8. 各discovery submission、blocked化、checkpoint後に最新stateとgateを再評価する。
9. continuation resultが`STOP_RUN`ならfinalization gateへ渡し、`MUST_CONTINUE`ならその `next_action` を処理する。`MAY_FINALIZE`かつpermit発行時だけnormal final responseを出す。

Research/Auditの処理件数には最低件数・目標件数・固定batch数・run当たり上限を設けない。1件、3件、それ以上の完了数はthroughput観測値であり継続・終了判定には使わない。

「readyが空」「候補0」「任意件数のResearch/Audit完了」「任意round数完了」「固定bankが埋まった」「fallback backlogがある」「Actions terminal反映待ち」「`next_jobs`表示枠を処理し切った」はworker独自の終了理由ではない。

## 6. Run終了判定

normal runの終了可否はworkerが列挙条件から主観的に選ばず、`continuation_gate.py` と `run_finalization_gate.py` に委ねる。

workerは少なくとも次の観測値を正確に渡す。

- actual-start基準run deadlineまでの残秒
- GitHub canonical read可用性
- GitHub/Library durability可用性と未保存成果の有無
- active assignment
- pending claim/submission/ACKと、それが次判断に必要か
- 独立作業の有無、candidate/Research/Audit state
- 実際に発生した具体的tool/platform failure（ある場合のみ）

`CONTINUE`なら `required_action` を処理する。`STOP_RUN`ならfinalization gateへ進む。`MUST_CONTINUE`なら `next_action` を処理する。`MAY_FINALIZE`かつ `finalization_permit.issued=true` の場合だけnormal final responseを出す。

「時間が厳しそう」「ツール回数が多い」「長く動いた」「十分処理した」「探索空間を合理的に使い切ったと思う」といった推測をstop inputへ変換しない。外部platformが強制終了した場合はfinal response自体が出ないため、workerは事前に架空のplatform limitを生成しない。

## 7. 特殊run

maintenance、08:30 JST update route、その他repoで明示されたspecial runはそれぞれの専用終了規則を優先する。通常run用gateをspecial routeの意味論へ無理に適用しない。ただし専用正本がactual-start deadlineを共有すると定める場合はそれに従う。

## 8. Claim-first execution and lease

claim requestは`.survey/work-queue/claim-requests/<request-id>.json`へ送り、`survey-claim-fast`のresultを読む。通常requestは`max_jobs`を省略または1とし、`lease_seconds`を省略して既定90分（5400秒）を使う。

処理が90分を超える可能性がある場合は、期限切れ前に同じ`request_id` / `worker_id` / `worker_kind`のclaim requestを、より新しいUTC `requested_at`へ更新してheartbeatとして送る。heartbeatは新規job取得ではない。

expired claimファイルは履歴としてGitHub上に残り得るがactiveではなく、他workerの新規claimを阻害しない。STATUSの「最古の有効claim」はready Research/Auditに紐づく未失効claimだけを対象とする。

lease期限を過ぎた時点でまだdescriptor/Library payloadを耐久保存していないworkerは旧claimで新規送信せず、fresh claimを取得し直す。すでにimmutable descriptorを耐久保存済みなら、その後のActions処理遅延はdescriptorを無効化しない。

## 9. Direct GitHub write conflict recovery

複数worker、`status-dashboard`、`survey-submission-fast`などが同時に`main`を更新するため、workerが別record bankや別attemptだけを書いていても、Git参照更新時にnon-fast-forward / 409 / 422の競合が起こり得る。これは即座にGitHub write不能とは判定しない。

- direct writeの直前に最新`main`を再取得する。
- non-fast-forward、409、422などbranch head競合では最新`main`を再取得し、**自workerが所有するrecord bankのslotまたはattempt固有descriptorだけ**を新しいtreeへ載せ直して再試行する。
- 同じ内容のblob SHAとattempt identityは維持する。別workerの変更、paper、queue、stateを巻き戻さない。
- force pushは禁止する。
- 同じattempt固有descriptorが既に同一内容で存在する場合は成功済みとして扱う。内容が異なる場合は上書きせず衝突として隔離し、その具体的状態をgateへ渡す。
- 一時競合は少なくとも5回まで最新`main`へ載せ直して再試行し、競合以外の認証・権限・到達不能や再試行枯渇が続いた場合は`fallback-routing.md`に従ってChatGPT Libraryへ切り替える。

この再試行はslot保存とimmutable descriptor保存の両方に適用する。descriptorがGitHubへ耐久保存されるまでは次jobを先取りclaimしないが、保存後はActions terminal待ちが次判断に不要なら同期障壁にしない。
