# Always-on paper worker policy

通常の論文workerは、maintenance runや08:30 JSTのその他更新workerなど明示的な特殊runを除き、実行環境と耐久保存経路が許す限り処理を継続する。

本書は通常論文workerの **run内継続・待ち時間削減・可視queueの扱い** の正本とする。discoveryの詳細な継続・停止判断は `discovery-continuation-policy.md` と `discovery-exhaustive-run-policy.md`、transportは `fallback-routing.md` / `queue-v10.md`、claim同時保有数は `claim-serial-policy.md`、全体STOP判定は `continuation-policy.json` を併用する。

## 0. 実開始基準のScheduled Chat引き継ぎガード

毎時`:30`の通常論文workerは、**実際にそのScheduled Chat invocationが開始した時刻をrun開始時刻として1回だけ固定し、run開始時刻 + 3600秒をrun deadlineとする。** プラットフォーム都合で予定`:30`より数分早く、または遅く起動しても、そのずれで今回runの持ち時間を削らない。

各runは新しい独立作業（Research/Auditのclaim、新しいdiscovery round、maintenanceの新しい独立単位など）を開始する直前に、予定`:30`までではなく **run deadlineまでの残り時間** を確認する。

- run deadlineまで **600秒以下** なら、新しい独立作業を開始せず、現在までの成果を耐久保存し、新しいclaimを発行せず、安全な継続情報だけを残してrunを終了する。
- run deadlineまで **180秒以下** なら、未保存成果の耐久保存、既存claimの安全な着地、必要な継続情報の記録など、孤立状態を残さないための最低限の終了処理だけを行う。
- 予定`:30`が近い、または既に通過していること自体は、run-local deadlineがまだ十分先なら停止理由にしない。これにより早起動・遅延起動のどちらでも概ね1時間の処理枠を使える。
- 600秒の引き継ぎガードは、high-backlog時の最低3件目標、通常のwork-conserving継続、`CONTINUE`既定値より優先する。ガード内に入ったことを理由に新しい3件目・次job・次探索軸を開始してはならない。
- すでに処理中で未保存のjobを乱暴に中断して成果を失うことはしない。まず現在の論理成果をGitHubまたはChatGPT Libraryへ耐久保存できる安全地点まで進め、その後は次の独立作業を開始しない。
- `continuation_gate.py` を使う場合は、実開始時に確定したrun deadlineまでの秒数を `--seconds-to-run-deadline` へ渡す。既定の `--scheduled-handoff-guard-seconds` は600秒とする。`--seconds-to-next-scheduled-task` はrun deadlineを確定できない古いcaller向けのcompatibility fallbackに限る。

この引き継ぎガードは通常runだけでなく、この毎時`:30` Scheduled Chatから起動する特殊runにも適用する。ただし特殊run固有の終了条件がさらに早く成立する場合は、そちらで終了してよい。

## 1. 論文ストック0は停止条件ではない

`actionable ready`、Library seed由来の`spillover_candidates`、その他処理可能なresearch/audit jobを合わせた論文ストックが0件になった場合、通常論文workerはアイドル終了してはならない。ストック0を新規discovery開始条件として扱い、直ちにdiscoveryを実行する。

- GitHub write可能時は正規のdiscovery/queue transportを使う。
- GitHub write不能でもChatGPT Libraryへoffline job seedを耐久保存できる場合はoffline discoveryを行う。
- discoveryで新規候補が得られたら、可能なら同じrun内でresearchまで進む。
- researchまたはcheckpoint後に再びストック0になったら、再度discoveryへ戻る。

## 2. discovery新規0・5件到達・在庫増加は停止条件ではない

1探索ラウンドで候補が全重複、弱候補のみ、または新規0件でも通常runを終了しない。`discovery-state.json`を参照し、直前と異なる探索軸・検索語・引用関係・関連実装・隣接テーマへ切り替えて次の探索ラウンドを行う。

1 discovery submissionのcandidate上限5本は **transport上の1バッチ上限** であり、通常run全体のdiscovery上限ではない。5本送ったこと、1 discovery jobがcompletedになったこと、candidate inventoryが多いことだけを理由に探索を終了しない。

ただしcandidate在庫が25本以上あり、処理可能なresearch jobが存在する間は **high-backlog research-only mode** とする。この条件中、通常workerは新規discoveryを行わず、priority順の全文精読、5-slot structured record作成、必要なauditだけに処理時間を使う。discoveryは毎時`:00`側へ任せる。candidate在庫が25本未満、またはactionable researchが尽きた場合に通常workerのdiscoveryを再開する。

既収録論文はarXiv ID、DOI、OpenReview ID、正規化タイトル等で詳細評価前に先行除外する。

`discovery-state.json` はGitHub Actionsを単一writerとする。Scheduled Chat workerは共有stateを直接更新せず、各discovery submissionの `discovery_stats` として観測値を渡す。

## 3. Actions待ちでアイドルにしない

Research/Auditについて、5 slot + attempt固有immutable descriptorがGitHubへ耐久保存済み、または完全payloadがChatGPT Libraryへ耐久checkpoint済みなら、**Actionsがそのjobをterminalへ反映するまで待つことをrun内の同期障壁にしない**。

- 送信済み・checkpoint済みjob IDをrun内で保持し、GitHub上でまだ`ready`でも同じjobを再精読しない。
- descriptor送信後は`survey-submission-fast`の完了を待たず、最新queue/claim stateを再取得して次の1件だけclaimする。
- 前jobが未保存の間は次jobを先取りclaimしない。
- 未解決immutable descriptorが参照しているrecord bankはoccupiedとみなし上書きしない。
- 別bankが空いていれば次jobでは別bankを使う。bankが空いていなくてもLibraryへ完全payloadを耐久保存できるなら研究を続ける。
- Actions resultのterminal確認は必要だが、独立作業開始の前提条件にはしない。
- high-backlog research-only mode中はActions待ちをdiscoveryで埋めず、次Research/Auditを優先する。

GitHub Actionsはclaim、immutable submission、backgroundの3レーンに分離されている。background側のfallback、citation、maintenance、index処理が詰まってもclaim-fastを待たせない。

## 4. `next-jobs.json` の表示件数を仕事量上限にしない

`.survey/work-queue/next-jobs.json` はworker向けの優先jobスナップショットであり、全ready jobの完全一覧とは限らない。`counts` が示すready件数が `next_jobs` に見えているactionable job数より多い場合、表示外readyが存在すると扱う。

表示上位jobがすべてcheckpoint済み・処理中・局所blockedでも、`counts` に未処理readyが残る場合は終了しない。必要に応じて `.survey/work-queue/jobs/` のjob実体を確認し、checkpoint済みjobを除いたpriority最上位の未処理jobを選ぶ。

`next_jobs` の表示枠、record bank数、Library pending件数、fallback-inbox件数はrun当たりの研究上限ではない。

## 5. 通常runの継続ループ

通常論文workerは原則として次を繰り返す。

1. candidate在庫水位と最新queue/backlogを確認する。25本以上でactionable researchがある場合はhigh-backlog research-only modeへ入る。
2. `claim-serial-policy.md`に従い、priority最上位のResearch/Auditを**1件だけclaim**する。未完了claimを複数保有しない。
3. 一次資料を全文精読し、5-slot recordを作成してpreflightする。
4. GitHub正常時は5 slotを書いた後、attempt固有immutable descriptorを作成する。GitHub write不能時はLibraryへ完全payloadをcheckpointする。
5. descriptor/checkpointが耐久保存できたら前jobのActions terminal待ちをせず、最新queue/claim stateを再取得して次の1件をclaimする。
6. actionable readyがなければspillover candidateを処理する。
7. 論文ストック0、candidate在庫low watermark未満、またはactionable researchが尽きた場合だけdiscoveryする。25本以上かつactionable researchありならdiscovery分岐へ入らない。
8. discovery各ラウンド、blocked化、checkpoint後にもqueue/backlog/discovery stateを再取得する。
9. 次の独立作業を始める前に§0の引き継ぎガードを評価する。ガード外で次の独立作業があれば1へ戻る。ガード内なら耐久保存と終了処理を行って終了する。

high-backlog research-only modeでは、一次資料取得と耐久保存経路が利用可能でactionable researchが十分ある限り、**1通常runにつき最低3件の異なるresearch jobを完全payloadとして送信または耐久checkpointすることを下限目標**とする。3件はrun終了条件でも上限でもない。§0の引き継ぎガードが成立した場合は、3件未満でもガードを優先して終了する。

「readyが空」「候補0」「1本完了」「3本完了」「1探索ラウンド完了」「discoveryで5本送信」「固定bankが埋まった」「fallback backlogがある」「Actions terminal反映待ち」「`next_jobs`表示枠を処理し切った」は終了理由ではない。

## 6. 通常runを終了してよい条件

通常論文workerが自発的に終了してよいのは原則として以下だけ。

- §0の引き継ぎガードが成立し、**今回runの実開始時刻 + 3600秒で定義したrun deadlineまで600秒以下**になった。
- platform time/context/execution limitに到達した。
- GitHub read不能で正本状態を安全に判断できない。
- GitHub direct writeとChatGPT Libraryの両方で、必要な成果またはoffline seedを耐久保存できない。
- discoveryが必要な水位で、`discovery-exhaustive-run-policy.md` に従って materially distinct な探索軸・source・citation方向・隣接テーマを十分に回しても独立作業を合理的に生成できない。

high-backlog research-only modeでは探索枯渇を終了理由に使わず、actionable researchを優先する。ただし§0の引き継ぎガードはhigh-backlog時にも優先する。

終了直前には `continuation-policy.json` を評価し、可能なら `.survey/scripts/continuation_gate.py` を使う。`CONTINUE` なら最終応答だけを出して終了せず、同じrunで次の独立作業へ進む。ただし§0の引き継ぎガードが成立している場合は `STOP_RUN` とし、次の独立作業へ進まない。

## 7. 特殊run

maintenance runは通常処理へ戻らず、maintenance要求発行後に終了する。08:30 JSTのその他更新workerは論文workerを同じ枠で実行しない。将来repoで追加される明示的な特殊runも、その正本指示を優先する。この毎時`:30` Scheduled Chatから起動した特殊runにも§0の **実開始基準のrun deadline** を適用する。

## 8. Claim-first execution and lease

claim requestは`.survey/work-queue/claim-requests/<request-id>.json`へ送り、`survey-claim-fast`のresultを読む。通常requestは`max_jobs`を省略または1とし、`lease_seconds`を省略して既定90分（5400秒）を使う。

処理が90分を超える可能性がある場合は、期限切れ前に同じ`request_id` / `worker_id` / `worker_kind`のclaim requestを、より新しいUTC `requested_at`へ更新してheartbeatとして送る。heartbeatは新規job取得ではない。

expired claimファイルは履歴としてGitHub上に残り得るがactiveではなく、他workerの新規claimを阻害しない。STATUSの「最古の有効claim」はready Research/Auditに紐づく未失効claimだけを対象とする。

lease期限を過ぎた時点でまだdescriptor/Library payloadを耐久保存していないworkerは旧claimで新規送信せず、fresh claimを取得し直す。すでにimmutable descriptorを耐久保存済みなら、その後のActions処理遅延はdescriptorを無効化しない。

## 9. Direct GitHub write conflict recovery

複数worker、`status-dashboard`、`survey-submission-fast`などが同時に`main`を更新するため、workerが別record bankや別attemptだけを書いていても、Git参照更新時にnon-fast-forward / 409 / 422の競合が起こり得る。これは即座にGitHub write不能とは判定しない。

- direct writeの直前に最新`main`を再取得する。
- non-fast-forward、409、422など「branch headが先に進んだ」競合では、最新`main`を再取得し、**自workerが所有するrecord bankのslotまたはattempt固有descriptorだけ**を新しいtreeへ載せ直して再試行する。
- 同じ内容のblob SHAとattempt identityは維持する。別workerの変更、paper、queue、stateを巻き戻さない。
- force pushは禁止する。
- 同じattempt固有descriptorが既に同一内容で存在する場合は成功済みとして扱う。内容が異なる場合は上書きせず衝突として停止・隔離する。
- 一時競合は少なくとも5回まで最新`main`へ載せ直して再試行し、競合以外の認証・権限・到達不能や再試行枯渇が続いた場合だけ`fallback-routing.md`に従ってChatGPT Libraryへ切り替える。

この再試行はslot保存とimmutable descriptor保存の両方に適用する。descriptorがGitHubへ耐久保存されるまでは次jobを先取りclaimしないが、保存後は従来どおりActions terminal待ちを同期障壁にしない。