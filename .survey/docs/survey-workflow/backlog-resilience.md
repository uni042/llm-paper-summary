# 未送信バックログ非阻害ポリシー

この文書は、GitHubへ未反映の研究成果やoffline job seedが一時配送先へ蓄積しても、新しい論文サーベイを止めないための正本である。

## 最重要原則

完成済みだが未反映の研究成果は**配送待ちバックログ**であり、研究停止理由ではない。record bankはGitHubへ直接送る際の一時ステージであり、未送信論文を保存し続けるキューではない。

耐久経路は **GitHub direct** と **ChatGPT Library fallback** の2つだけ。完成logical payloadまたは継続に必要なoffline job seedをどちらかへ耐久保存できた時点で後続作業へ進める。GitHub上のjob自体はActionsで最終反映されるまで未完了のまま残す。

Google Drive fallbackは廃止済みであり、新規保存・replay・backlog判定には使わない。旧実装は `archive/drive-fallback-before-removal-20260910` ブランチに保存している。

## 1. record bank

利用可能bankの正本は `.survey/work-queue/records/bank-registry.json`。GitHubへ直接送る前は可能なら:

```bash
python .survey/scripts/select_record_bank.py --repo-root .
```

を実行し、`selected_bank`を使う。

A〜Hがすべて使用中・dirtyでも、Libraryへ完全payloadを保存できればrunを止めない。fallback backlogはbank数に拘束されない。

## 2. backlog

複数件が蓄積してよい場所は:

- ChatGPT Library: `/LLM-survey-outbox/pending/`
- GitHub intake: `.survey/work-queue/fallback-inbox/`

pending件数は、そのrunで新しく精読できる論文数を減らす条件にしない。

research/auditは1論文につき1 envelopeとし、5 slot + `chat-inbox.json`を完全に含める。1論文を複数fragmentへ分割しない。完成Markdownはfallbackへ保存しない。

## 3. Library障害

Library保存失敗だけをSTOP_RUNにしない。GitHub direct writeが利用可能ならGitHubへ保存して研究を継続する。

GitHub writeもrun-wideで利用不能かつLibraryにも必要な完全payload/offline seedを保存できない場合だけ、未checkpoint成果を増やす前にSTOP_RUNする。

Library pending増加や単一payloadのreplay失敗はrun停止理由ではない。

## 4. recovery

Libraryは固定record bankへ直接replayしない。まずGitHubの不変受信箱へ送る。

`.survey/work-queue/fallback-inbox/<envelope-id>.json`

`.survey/scripts/dispatch_fallback_inbox.py` がsurvey-helperの共通concurrency group内で1件ずつ固定transportへ展開する。処理済みenvelopeは `.survey/work-queue/fallback-archive/` へ移る。

同じ`id`のpayloadを再発見した場合:

1. GitHub fallback-inbox/archiveに同じ`id`があるか確認する。
2. 内容一致ならLibrary copyを再展開せずprocessedへ移す。
3. 内容不一致ならID衝突としてfailedへ隔離する。

## 5. dependency待ち

GitHub write不能中にoffline seedをLibraryへ保存し、その候補を同じrunで先に精読してresearch payloadも保存してよい。

復旧時にresearch payloadがseedより先にGitHub intakeへ入っても、対応jobがまだ存在しない間は `fallback-inbox` に残す。後続seedがdispatchされjobが実体化した後にeligibleになる。

## 6. actionable work

workerは可能な範囲で次を統合して判断する。

- GitHub ready jobs
- Library/GitHub intake上のcheckpoint済みjob
- Library seed由来のspillover candidates

GitHub readyでも完全payloadがcheckpoint済みのjobは再精読しない。checkpoint済みreadyだけがGitHub queueを塞ぐ場合は `.survey/work-queue/transport/request-jobs.json` でそれらを一時除外して新しいdiscovery jobを発行する。元jobのstatusは変更しない。

GitHub write不能時にactionable readyとspillover candidateが尽きても、Libraryへoffline seedを保存可能なら新規discoveryを続ける。

## 7. replay fairness

Library replayだけでScheduled Chat runを恒常的に使い切らない。

- Library replayはGitHub immutable intakeへ渡すだけに留める。
- 固定transport処理はActionsへ任せる。
- 複数pendingをintakeできても、replayだけをrun終了理由にせずactionable researchを再評価する。
- GitHub fallback dispatcherは1 Actions runにつき最大1 logical envelopeを展開する。

## 8. 回復完了の意味

- Library `processed`: GitHub immutable intakeへ受領済み。
- GitHub `fallback-archive`: fallback envelopeのdispatchまたはterminal確認済み。
- 論文job完了: Actions result + latest queueでterminal確認済み。

Libraryの`processed`をpaper publication完了と混同しない。

## 9. STOP_RUN

停止条件は `continuation-policy.json` のみを使う。

Library pending数、GitHub fallback-inbox件数、未送信論文数、record bank exhaustion、単一payload障害、dependency待ち1件だけでは停止しない。

完成成果または必要なoffline seedをGitHubにもLibraryにも耐久保存できない、GitHub readが不能、プラットフォーム上限到達、fallback spilloverを含めても独立作業が残らない場合など、正本条件だけで停止する。
