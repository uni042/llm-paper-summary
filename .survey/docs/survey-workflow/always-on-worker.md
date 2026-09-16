# Always-on paper worker policy

通常の論文workerは、maintenance runや08:30 JSTのその他更新workerなど明示的な特殊runを除き、実行環境と耐久保存経路が許す限り処理を継続する。本書は通常論文workerのrun内継続の正本とする。全体の終了判定は `continuation-policy.json` と `.survey/scripts/continuation_gate.py` を優先する。

## Run-local time window

毎時`:30`の通常論文workerは、実際のScheduled Chat invocation開始時刻を1回だけ固定し、`run_deadline = actual_start + 3600 seconds` とする。

- run deadlineまで600秒以下: 新しい独立作業を開始せず、現在までの成果とclaimを安全に耐久handoffする。
- run deadlineまで180秒以下: 未保存成果、claim、継続情報の最低限の着地だけを行う。
- 600秒より多く残る: 件数・在庫・job完了数・探索枯渇を理由に正常終了しない。

予定`:30`は起動・集計識別に使うだけで、run-local deadlineを短縮しない。`--seconds-to-next-scheduled-task` はactual-start deadlineを確定できない古いcaller向けの互換フォールバック（compatibility fallback）に限る。

## 件数ノルマを使わない

通常workerにも1run最低3件などのResearch/Audit処理ノルマを設けない。また「3件完了」「5件candidate送信」「4 round完了」等を終了条件にしない。

処理件数、candidate数、round数、submission数はすべて観測値（telemetry）である。時間と耐久保存が許す限り、1件でも100件でも次の独立作業へ進む。

## 論文ストック0はDiscovery開始条件

`actionable ready`、Library seed由来のspillover candidate、その他処理可能なResearch/Auditが0件になった場合、アイドル終了せずDiscoveryへ進む。

- GitHub write可能時は正規のworkflow-v10 discovery transportを使う。
- GitHub write不能でもChatGPT Libraryへoffline seedを耐久保存できる場合はoffline discoveryを行う。
- discoveryで候補が得られたら同じrun内でResearchへ進んでよい。
- 空round・全重複roundでも、handoff guard外なら別探索軸を生成して継続する。

探索空間を「使い切った」という判断は正常終了理由にせず、検索語・source・引用方向・隣接分野を再生成するトリガーとして扱う。

## Candidate受入

Discovery submissionのcandidate配列に固定件数上限を設けない。強いcandidateを5件などに切り詰めない。弱い候補で件数を埋めず、quality基準を満たす候補はすべて受け入れる。

外部transportの実payload制約で単一submissionが保存不能な場合だけ複数immutable submissionへ分割し、総candidateを失わない。

## High-backlog research mode

candidate在庫が25本以上あり、actionable Research/Auditが存在する間、通常workerはhigh-backlog research-only modeとしてpriority順の全文精読・5-slot structured research record作成・必要なauditを優先する。

このmodeでも最低完了件数は設けない。handoff guard外でactionable workが残る限り、1件の完全payloadをGitHubまたはLibraryへ耐久保存した後で次の1件をclaimする。

## Claim-first execution

`claim-serial-policy.md` に従う。

- 同一workerの未完了claimは1件だけ。
- claim requestは `.survey/work-queue/claim-requests/<request-id>.json` へ送る。
- 完全payloadが耐久保存される前に次jobを先取りclaimしない。
- descriptor/checkpointが耐久保存できたらActions terminal反映を同期障壁にせず、最新queue / claim stateを取得して次のclaimへ進む。
- pending claim resultは同一request IDを維持して待機・再読し、別requestを重ねない。

## next-jobs.jsonは上限ではない

`.survey/work-queue/next-jobs.json` は優先jobスナップショットであり、全ready jobの完全一覧とは限らない。表示枠、record bank数、Library pending件数、fallback inbox件数をrunの処理上限にしない。

表示上位がcheckpoint済み・processing・局所blockedでも、countsやjob実体に未処理readyが残るなら継続する。

## 通常runの継続ループ

1. 最新HEAD、candidate inventory、queue/backlog、claim stateを確認する。
2. actionable Research/Auditがあればpriority最上位を1件claimする。
3. 一次資料全文を精読し、5-slot recordを作成・preflightする。
4. GitHub正常時はimmutable descriptor、GitHub write不能時はLibrary checkpointへ完全payloadを耐久保存する。
5. 最新stateを再取得する。
6. actionable workがなければspillover、次にDiscoveryへ進む。
7. Discoveryが空・全重複・低採用でも別軸へ切り替える。
8. 新しい独立作業の直前にrun-local handoff guardを評価する。
9. guard外なら1へ戻る。guard内なら安全なhandoffを行って終了する。

## 正常終了と異常blocker

通常runを正常終了してよいのは、run-local handoff guardが成立し、成果とclaimが安全に耐久handoffされた場合だけである。

以下は異常blockerであり、正常成功のfinalization理由ではない。

- GitHub read不能で正本状態を安全に判断できない。
- GitHub direct writeとChatGPT Libraryの両方で必要な成果・seedを耐久保存できない。
- platform/context/tool hard limitで継続不能。

回復可能なら回復して継続する。回復不能でも「仕事を使い切って正常終了」とは扱わない。

## 特殊run

maintenance run、08:30 JSTのframework/model update worker、その他repoで明示された特殊runは各専用ルールに従う。通常paper workerの件数ノルマ・探索枯渇による終了規則は適用しない。
