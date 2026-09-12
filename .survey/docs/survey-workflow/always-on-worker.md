# Always-on paper worker policy

通常の論文workerは、maintenance runや08:30 JSTのその他更新workerなど明示的な特殊runを除き、実行環境と耐久保存経路が許す限り処理を継続する。

本書は通常論文workerの **run内継続・待ち時間削減・可視queueの扱い** の正本とする。discoveryの詳細な継続・停止判断は `discovery-continuation-policy.md` と `discovery-exhaustive-run-policy.md`、transportは `fallback-routing.md` / `queue-v10.md`、全体STOP判定は `continuation-policy.json` を併用する。

## 1. 論文ストック0は停止条件ではない

`actionable ready`、Library seed由来の`spillover_candidates`、その他処理可能なresearch/audit jobを合わせた論文ストックが0件になった場合、通常論文workerはアイドル終了してはならない。ストック0を新規discovery開始条件として扱い、直ちにdiscoveryを実行する。

- GitHub write可能時は正規のdiscovery/queue transportを使う。
- GitHub write不能でもChatGPT Libraryへoffline job seedを耐久保存できる場合はoffline discoveryを行う。
- discoveryで新規候補が得られたら、可能なら同じrun内でresearchまで進む。
- researchまたはcheckpoint後に再びストック0になったら、再度discoveryへ戻る。

## 2. discovery新規0・5件到達は停止条件ではない

1探索ラウンドで候補が全重複、弱候補のみ、または新規0件でも通常runを終了しない。`discovery-state.json`を参照し、直前と異なる探索軸・検索語・引用関係・関連実装・隣接テーマへ切り替えて次の探索ラウンドを行う。

1 discovery submissionのcandidate上限5本は **transport上の1バッチ上限** であり、通常run全体のdiscovery上限ではない。5本送ったこと、1 discovery jobがcompletedになったこと、candidate inventoryがsoft target 50へ到達したことだけを理由に探索を終了しない。探索専用workerと同様、利用可能な実行時間の中で有望な独立探索軸が残る限り別roundへ進む。

既収録論文はarXiv ID、DOI、OpenReview ID、正規化タイトル等で詳細評価前に先行除外する。検索側で除外できない場合は広めに候補を取得して軽量重複除去し、未収録候補だけを詳細評価する。

`discovery-state.json` はGitHub Actionsを単一writerとする。通常Scheduled Chat workerはこの共有stateを直接更新せず、各discovery submissionの `discovery_stats` として観測値を渡す。Actions処理待ちの間は別の探索軸の検索・軽量評価を先行してよいが、次のcandidate送信直前には最新HEAD / identity / queueを再確認する。

## 3. Actions待ちでアイドルにしない

research / audit / discoveryの完全なlogical payloadをGitHubへ送信済み、またはChatGPT Libraryへ耐久checkpoint済みなら、**Actionsがそのjobをterminalへ反映するまで待つことをrun内の同期障壁にしない**。

- 送信済み・checkpoint済みjob IDをrun内で保持し、GitHub上でまだ`ready`でも同じjobを再精読しない。
- 別のactionable research/audit、spillover candidate、またはdiscoveryがあるなら直ちに次へ進む。
- GitHub direct transportのrecord bankが別に空いていれば別bankを使う。bankが空いていなくてもLibraryへ完全payloadを耐久保存できるなら研究を続ける。
- Actions resultのterminal確認は必要だが、独立作業を開始する前提条件にはしない。
- 前jobのActions処理中に次論文の一次資料取得・精読や別探索軸の探索を進め、送信直前だけ最新queue/identityと競合を再確認する。

これによりGitHub Actionsの処理時間をScheduled Chatのアイドル時間へ変換しない。

## 4. `next-jobs.json` の表示件数を仕事量上限にしない

`.survey/work-queue/next-jobs.json` はworker向けの優先jobスナップショットであり、全ready jobの完全一覧とは限らない。`counts` が示すready件数が `next_jobs` に見えているactionable job数より多い場合、表示外readyが存在すると扱う。

特に、表示上位jobがすべてcheckpoint済み・処理中・局所blockedである一方、`counts` に未処理readyが残る場合は、「actionable jobなし」と判断して終了してはならない。必要に応じて `.survey/work-queue/jobs/` のjob実体、GitHub上のready job検索、最新Actions反映後のsnapshotを確認し、checkpoint済みjobを除いたpriority最上位の未処理jobを選ぶ。

`next_jobs` の表示枠、record bank数、Library pending件数、fallback-inbox件数はrun当たりの研究上限ではない。

## 5. 通常runの継続ループ

通常論文workerは原則として次を繰り返す。

1. candidate在庫水位と最新queue/backlogを確認する。
2. actionable readyをpriority順に処理する。表示上位がcheckpoint済みなら表示外readyも確認する。
3. 完全payloadを送信またはcheckpointしたら、Actions terminal待ちをせず次の独立jobへ進む。
4. actionable readyがなければspillover candidateを処理する。
5. 論文ストックが0、またはcandidate補充が必要ならdiscoveryする。
6. discoveryで候補を得たらresearchし、必要ならauditする。1 submission 5件はbatch上限として扱い、必要なら別探索軸で続ける。
7. job完了、blocked化、checkpoint、discovery各ラウンド後にqueue/backlog/discovery stateを再取得する。
8. 次の独立作業があれば1へ戻る。
9. ストック0なら5へ戻る。

「readyが空」「候補が0」「1本完了」「1探索ラウンド完了」「discoveryで5本送信」「固定bankが埋まった」「fallback backlogがある」「Actionsのterminal反映待ち」「`next_jobs`表示枠を処理し切った」は終了理由ではない。

## 6. 通常runを終了してよい条件

通常論文workerが自発的に終了してよいのは、原則として以下だけ。

- platform time/context/execution limitに到達した。
- GitHub read不能で正本状態を安全に判断できない。
- GitHub direct writeとChatGPT Libraryの両方で、必要な成果またはoffline seedを耐久保存できない。
- `discovery-exhaustive-run-policy.md` に従って materially distinct な探索軸・source・citation方向・隣接テーマを十分に回しても、利用可能な探索手段・一次資料アクセスの範囲で独立作業を合理的に生成できない。

最後の条件は単一ラウンドの新規0件、全重複、低採用率、5件送信、soft target到達では満たさない。探索軸変更・引用展開・隣接テーマ展開を試した後にのみ検討する。

終了直前には `continuation-policy.json` を評価し、可能なら `.survey/scripts/continuation_gate.py` を使う。`CONTINUE` なら最終応答だけを出して終了せず、同じrunで次の独立作業へ進む。

## 7. 特殊run

maintenance runは通常処理へ戻らず、maintenance要求発行後に終了する。08:30 JSTのその他更新workerは論文workerを同じ枠で実行しない。これは通常runの早期終了ではなく、明示的に別目的へ割り当てた特殊runである。将来repoで追加される明示的な特殊runも、その正本指示を優先する。
