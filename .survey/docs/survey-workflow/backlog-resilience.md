# 未送信バックログ非阻害ポリシー

この文書は、GitHubへ未反映の研究成果やoffline job seedが一時配送先へ蓄積しても、新しい論文サーベイを止めないための正本である。

## 最重要原則

完成済みだが未反映の研究成果は**配送待ちバックログ**であり、研究停止理由ではない。record bankはGitHubへ直接送る際の一時ステージであり、未送信論文を保存し続けるキューではない。

耐久経路は **GitHub direct** と **ChatGPT Library fallback** の2つだけ。完成logical payloadまたは継続に必要なoffline job seedをどちらかへ耐久保存できた時点で後続作業へ進める。GitHub上のjob自体はActionsで最終反映されるまで未完了のまま残す。

Google Drive fallbackは廃止済みであり、新規保存・replay・backlog判定には使わない。

## 1. Record bank

通常Research/Auditではclaim resultの `record_bank` が正本である。workerは `select_record_bank.py` で別bankを選び直さない。`record_bank_fallback: "library"` の場合は完全payloadをLibraryへcheckpointする。

`select_record_bank.py` は診断・maintenance・fallback replayでbank状態を確認するために使う。

A〜Hがすべて使用中・dirtyでも、Libraryへ完全payloadを保存できればrunを止めない。fallback backlogはbank数に拘束されない。

## 2. Backlog

複数件が蓄積してよい場所は次である。

- ChatGPT Library: `/LLM-survey-outbox/pending/`
- GitHub intake: `.survey/work-queue/fallback-inbox/`

pending件数は、そのrunで新しく精読できる論文数を減らす条件にしない。

新規Research/Audit fallbackは1論文につき1 envelopeとし、root-levelのjob/claim/attempt/paper identityと完全な5 record slotを含める。固定 `chat-inbox.json` と完成Markdownは新規fallbackへ保存しない。

2026-09-14以前に保存済みの「5 slot + `chat-inbox.json`」形式は既存pending救済のため読込互換だけ残し、replay時に現行のattempt固有不変descriptorへ変換する。

## 3. Library / durability障害

Library保存失敗だけをnormal STOP_RUNにしない。GitHub direct writeが利用可能ならGitHubへ保存して研究を継続する。

GitHub writeもrun-wideで利用不能かつLibraryにも必要な完全payload / offline seedを保存できない場合は **異常blocker** として扱う。未checkpoint成果を増やさず、回復または証拠保存を行うが、これをnormal success finalizationへ変換しない。

Library pending増加や単一payloadのreplay失敗はrun停止理由ではない。

## 4. Recovery

Libraryからrecord bankへ直接replayしない。まずGitHubの不変受信箱へ送る。

`.survey/work-queue/fallback-inbox/<envelope-id>.json`

Research/Audit record bundleは `dispatch_fallback_inbox.py` から `replay_record_fallback.py` へ渡し、安全なbankへ5 slotをmaterializeした後、attempt固有descriptorを `.survey/work-queue/submissions/research/` または `audit/` に生成する。固定Chat transportは再生成しない。

Discovery seed、job request、framework / LLM update等の非record envelopeはgeneric fallback transportでallowlistされたJSON pathへ展開する。

処理済みenvelopeは `.survey/work-queue/fallback-archive/` へ移す。同じ`id`を再発見した場合、内容一致なら再展開せずprocessed扱いとし、内容不一致なら衝突としてfailedへ隔離する。

## 5. Dependency待ち

GitHub write不能中にoffline seedをLibraryへ保存し、そのcandidateを同じrunで先に精読してResearch fallbackも保存してよい。

復旧時にResearch fallbackがseedより先にGitHub intakeへ入っても、対応canonical jobがまだ存在しない間は隔離せず `fallback-inbox` に残す。後続seedがdispatchされjobが実体化した後にeligibleになる。

## 6. Actionable work

workerは可能な範囲で次を統合して判断する。

- GitHub ready jobs
- Library / GitHub intake上のcheckpoint済みjob
- Library seed由来のspillover candidates

GitHub readyでも完全payloadがcheckpoint済みのjobは再精読しない。checkpoint済みreadyだけがqueueを塞ぐ場合は `.survey/work-queue/transport/request-jobs.json` でそれらを一時除外して新しいDiscovery jobを発行する。元jobのstatusは変更しない。

GitHub write不能時にactionable readyとspillover candidateが尽きても、Libraryへoffline seedを保存可能なら新規Discoveryを続ける。現在の探索軸が空・全重複・枯渇なら、handoff guard外では別軸を生成する。

Discovery seedのcandidate配列に固定件数上限は設けない。外部transportの実payload制約に当たる場合だけ複数immutable seedへ分割し、総candidateを切り捨てない。

## 7. Replay fairness

Library replayだけでScheduled Chat / Work runを恒常的に使い切らない。

- Library replayはGitHub fallback-inboxへのintakeまでをworkerが行う。
- GitHub側のrecord replay / generic dispatchはActionsへ任せる。
- 複数pendingをintakeできても、replayだけをrun終了理由にせずactionable Research/Auditとcandidate水位を再評価する。
- GitHub fallback dispatcherの内部batch制御はtransport実装上の処理単位であり、Scheduled Chat runのresearch/candidate上限ではない。

## 8. 回復完了の意味

- Library `processed`: GitHub immutable intakeへ受領済み。
- GitHub `fallback-archive`: fallback envelopeが現行transportへ変換・dispatchされた、またはterminal jobとしてacknowledgeされた。
- 論文job完了: immutable result + latest queueでterminal確認済み。

Library `processed` やfallback archiveをpaper publication完了と混同しない。

## 9. Normal finalization

通常runの終了条件は `continuation-policy.json` と `run-liveness-policy.md` のtime-only semanticsを使う。

Library pending数、GitHub fallback-inbox件数、未送信論文数、record bank exhaustion、単一payload障害、dependency待ち、GitHub read不能、durability failure、platform/tool異常、現在の探索軸の枯渇はnormal successのSTOP_RUN条件ではない。

normal finalizationを許可するのは、実開始基準のrun-local handoff guardが成立し、現在の成果とclaimが安全に耐久handoffされ、`run_finalization_gate.py` がpermitを発行した場合だけである。非時間failureは異常blockerとして回復または次runへのcanonical stateを残す。

Claim request/result/current-claim filesはdurable queue stateである。maintenanceはready jobに対応するactive/expired claim、未処理request/result、非terminalまたは未知jobをassignmentに含む履歴を保護する。GC可能なのは、live参照がなく保持期間を満たしたterminal history等に限る。
