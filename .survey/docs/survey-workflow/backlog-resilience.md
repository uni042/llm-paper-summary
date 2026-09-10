# 未送信バックログ非阻害ポリシー

この文書は、GitHubへ未反映の研究成果やoffline job seedが複数の一時配送先へ蓄積しても、新しい論文サーベイを止めないための正本である。

## 最重要原則

完成済みだが未反映の研究成果は**配送待ちバックログ**であり、研究停止理由ではない。record bankはGitHubへ直接送る際の一時ステージであり、未送信論文を保存し続けるキューではない。

完成logical payloadまたは継続に必要なoffline job seedをGitHub、Google Drive、ChatGPT Libraryのいずれかへ耐久保存できた時点で後続作業へ進める。GitHub上のjob自体はActionsで最終反映されるまで未完了のまま残す。

## 1. record bank

利用可能bankの正本は `.survey/work-queue/records/bank-registry.json`。現在はA〜Hの8 bankを持つ。

GitHubへ直接送る前は可能なら:

```bash
python .survey/scripts/select_record_bank.py --repo-root .
```

を実行し、`selected_bank`を使う。見た目だけで再利用可能と推測しない。

A〜Hがすべて使用中・dirtyでも、DriveまたはLibraryへ完全payloadを保存できればrunを止めない。fallback backlogはbank数に拘束されない。

## 2. 複数outbox backlog

次の全てに複数件が蓄積してよい。

- Google Drive: `/Google Drive/llm-paper-summary-outbox/pending/`
- ChatGPT Library: `/LLM-survey-outbox/pending/`
- GitHub intake: `.survey/work-queue/fallback-inbox/`

pending件数は、そのrunで新しく精読できる論文数を減らす条件にしない。

research/auditは1論文につき1 envelopeとし、5 slot + `chat-inbox.json`を完全に含める。1論文を複数fragmentへ分割しない。完成Markdownはfallbackへ保存しない。

## 3. outboxが一部死んでいる場合

DriveとLibraryは独立した耐久経路として扱う。

- Drive保存失敗 + Library保存成功 → Libraryへcheckpointして続行。
- Library保存失敗 + Drive保存成功 → Driveへcheckpointして続行。
- 両方に既存pendingがあっても新しい成果保存を止めない。
- 片方のreplayが失敗しても、他方のpendingや新規研究を止めない。
- 同一runである経路全体が利用不能と判定済みなら、各jobごとに同じ失敗を繰り返さない。

単一fallback障害やbacklog増加を `STOP_RUN` としない。

## 4. cross-outbox recovery

DriveとLibraryは固定record bankへ直接replayしない。両方ともまずGitHubの不変受信箱へ送る。

`.survey/work-queue/fallback-inbox/<envelope-id>.json`

これにより、DriveとLibraryが同時に復旧しても固定bankと`chat-inbox.json`を直接競合しない。

`.survey/scripts/dispatch_fallback_inbox.py` がsurvey-helperの共通concurrency group内で1件ずつ固定transportへ展開する。処理済みenvelopeは `.survey/work-queue/fallback-archive/` へ移る。

同じ`id`のpayloadが複数outboxに存在した場合:

1. GitHub fallback-inbox/archiveに同じ`id`があるか確認する。
2. 内容一致なら重複copyを再展開せずacknowledgeする。
3. 内容不一致ならID衝突としてfailedへ隔離する。

このglobal dedupeにより、保存結果が不明瞭だった場合の重複copyも安全に収束できる。

## 5. dependency待ちを停止理由にしない

GitHub write不能中にoffline seedをfallbackへ保存し、その候補を同じrunで先に精読してresearch payloadも保存してよい。

復旧時にresearch payloadがseedより先にGitHub intakeへ入っても、対応jobがまだ存在しない間は `fallback-inbox` に残す。failedへ送らない。後続のseed envelopeがdispatchされjobが実体化した後、research envelopeがeligibleになる。

したがって、seedとresearchが別outboxに分散しても安全である。

## 6. actionable work

workerは可能な範囲で次を統合して判断する。

- GitHub ready jobs
- Drive/Library/GitHub intake上のcheckpoint済みjob
- fallback seed由来のspillover candidates

GitHub readyでも完全payloadがcheckpoint済みのjobは再精読しない。未反映statusを理由に同じ論文を何度も読むことを避ける。

checkpoint済みreadyだけがGitHub queueを塞ぐ場合は `.survey/work-queue/transport/request-jobs.json` でそれらを一時除外して新しいdiscovery jobを発行する。元jobのstatusは変更しない。

GitHub write不能時にactionable readyとspillover candidateが尽きても、fallbackへoffline seedを保存可能なら新規discoveryを続ける。

## 7. replay fairness

backlog replayだけでScheduled Chat runを恒常的に使い切り、新規researchが飢餓する状態を避ける。

- Drive replayはGitHub Actionsが独立して進める。
- Library replayはScheduled Chatが行うが、GitHub immutable intakeへ渡すだけに留め、固定transport処理はActionsへ任せる。
- Library pendingを複数件 intakeできる場合でも、replayだけをrun終了理由にせずactionable researchを再評価する。
- GitHub fallback dispatcherは1 Actions runにつき最大1 logical envelopeを展開する。

## 8. 回復完了の意味

- Drive/Library `processed`: GitHub immutable intakeへ受領済み。
- GitHub `fallback-archive`: fallback envelopeのdispatchまたはterminal確認済み。
- 論文job完了: Actions result + latest queueでterminal確認済み。

外部outboxの`processed`をpaper publication完了と混同しない。

## 9. STOP_RUN

停止条件は `continuation-policy.json` のみを使う。

Drive pending数、Library pending数、GitHub fallback-inbox件数、未送信論文数、record bank exhaustion、単一経路の障害、dependency待ち1件だけでは停止しない。

完成成果または必要なoffline seedをGitHub・Drive・Libraryのどこにも耐久保存できない、GitHub readが不能、プラットフォーム上限到達、fallback spilloverを含めても独立作業が残らない場合など、正本条件だけで停止する。
