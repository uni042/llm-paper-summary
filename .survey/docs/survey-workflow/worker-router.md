# Chat worker router — workflow v10

予定されたChat workerは**1つだけ**。実行時刻で次のどちらか一方を選び、同じ枠で両方を処理しない。

- **08:30 JST** → その他更新worker
- **それ以外の毎時 :30** → 論文worker

毎回default branch最新HEADを取得し、このrouter、[queue-v10.md](queue-v10.md)、[continuation-policy.json](continuation-policy.json) を同じHEADから読む。stop / continue判断は `continuation-policy.json` を正本とし、可能なら `.survey/scripts/continuation_gate.py` の判定に従う。

## 最重要: 問題が起きてもrun全体を止めない

**個別jobの失敗・保留はrun全体の停止理由ではない。** 問題が起きたjobだけをblocked/pending/checkpoint扱いにし、独立して処理できるready jobがあれば必ず続行する。

run全体を停止してよいのは、次のいずれかだけ。

1. GitHub read自体が利用できず、最新queue/identity/repo状態を確認できない。
2. 完成済み成果があり、それをGitHubまたはGoogle Drive outboxのどちらにも耐久保存できない。
3. 明確な時間・実行回数・コンテキスト等のプラットフォーム上限に達した。
4. 独立して処理できる作業が残っておらず、残作業すべてが同じ未解決の全体依存でblockedになっている。

全文取得不能、論文固有の依存不足、単一payloadのGitHub write失敗、Drive保存失敗、pending replay失敗は**そのjobまたは経路だけの問題**として扱う。別のready jobまで止めない。

### End-of-run Stop Gate

ユーザーへ最終報告を出す前、またはworkerが自発的に終了しようとする前に、必ず [continuation-policy.json](continuation-policy.json) を評価する。Python実行が利用可能なら `.survey/scripts/continuation_gate.py` を使う。

`STOP_RUN` 条件が1つも成立せず、独立したready jobがある場合は、**最終報告を出して終了してはならない。処理を続ける。** 問題の通知はrun終了命令ではない。

## 実行前の共通回復

GitHubへの反映が利用可能な場合、Google Drive outboxの `pending` は [drive-outbox.md](drive-outbox.md) と `.github/workflows/drive-outbox-import.yml` に従ってGitHub Actions側が回収する。Chat workerは同じpayloadをGitHubへ手動で二重投入しない。開始時は最新queue/identity/対象blobを読み、Driveからすでに再投入済みの成果が反映されていれば、その状態を正として新規作業へ進む。

Drive pendingの回収失敗は新規研究を飢餓させない。GitHub readが可能で、完成payloadがDriveへ耐久保存済みなら通常のready job処理へ進む。同じ `Failure Class` の共通障害が確認されたrunでは、同原因の保存・再投入を各jobごとに繰り返さない。

GitHub readができない場合はrepo状態に依存する新規処理を開始しない。

## GitHub write失敗の診断プロトコル

GitHub writeが失敗した場合は、失敗しただけでrunを終了しない。次を**機械的な順序**で行う。

1. 失敗対象の最新blob SHA / repo状態を再取得し、その対象だけ1回再試行する。
2. それでも失敗した場合、そのrunで最初のwrite失敗に限り、固定診断先 `.survey/work-queue/transport/health-probe.json` を最新SHA付きで1回だけ更新する。`probe_id` はrun/attemptを識別できる短い値に変え、元の論文payloadは書かない。
3. 診断writeが成功した場合は `target_or_payload_specific` と分類する。GitHub write能力全体は生きているため、影響を受けたjobだけを一時保管し、後続の独立したGitHub writeは許可する。
4. 診断writeも失敗した場合は `run_wide_github_write_unavailable` と分類する。そのrunでは以後GitHub writeを試さない。同じ失敗を各slot/jobで繰り返さない。
5. GitHub writeを使えないrunでも、GitHub readが可能で、成果をGoogle Drive outboxへ耐久保存できる限り、既知のready research/auditを読み進めて一時保管し、次の独立jobへ進む。
6. GitHub write不能のため新しいqueue遷移が必要な作業しか残っていない場合は、それを全体依存としてStop Gateで判定する。

診断用固定ファイルは接続状態の切り分け専用であり、安全検査回避やpayload分割回避には使わない。

## A. 論文worker

正本: [README.md](README.md)、[queue-v10.md](queue-v10.md)、[paper template](../../templates/paper.md)、`.survey/work-queue/next-jobs.json`。

**research / auditに着手する前に `.survey/templates/paper.md` を必ず読む。** 新しい実行環境・新しい会話では、テンプレートが基準に指定する [MoE-Infinity のまとめ](../../../papers/inference/01-offload-hierarchical-memory/2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md) も確認する。

Chatは探索・全文精読・科学的判断・監査判断と**構造化research record**作成を担当する。完成Markdownは作成・送信しない。research/auditはqueue-v10で定義されたA/B固定record bankの5 JSON slotを使い、全slot成功後のみ固定 `chat-inbox.json` をtriggerする。paper/state/README/identity/queueをChatから直接編集しない。

構造化recordは「rendererが後で文章を補う」前提で短縮しない。`problem_method` は、そのまま人間向け本文として読める説明量にする。複数機構を持つsystem論文では、各主要機構を原則2〜4段落程度で説明し、入力・観測・処理・出力・前後の接続・なぜ効くか・追加コスト・失敗条件まで書く。

### 日本語優先

人間が読む説明文は可能な限り日本語または一般的なカタカナ表記で書く。`request`、`placement`、`dynamic`、`latency` のような英単語を日本語文へそのまま差し込まない。

英語を残してよいのは、固有名詞、定着した略語、コード/API/変数、または初出で日本語説明の直後に正式名称を示す括弧内に限る。初出後は日本語・カタカナまたは略語へ戻す。表のセルはこの裸英語チェック・日本語比率チェックの対象外としてよい。

`.survey/scripts/japanese_style.py` と `.survey/scripts/assemble_research_record.py` が説明文を検査する。日本語比率は80%以上を目標、70〜80%を警告、70%未満を不合格とし、日本語・カタカナへ置換できる英語専門語が本文の括弧外に残っていれば比率に関係なく不合格とする。

**GitHubへslotを書き始める前に `.survey/templates/paper.md` に対する最終品質チェックを行う。** `results` は主要数値ごとに比較対象・条件・読み方を持たせ、悪化条件・negative resultも残す。基準未達recordは完成扱いにせず、そのrunで本文へ戻って補強する。

### 同一runで継続処理

開始時に既存ready research/auditがあればpriority順に処理する。readyが尽きたらdiscoveryを実行し、Actions反映後の最新queueを読み直し、生成されたresearch jobを同じrunで全文精読・構造化record保存・Actions結果確認まで進める。researchからauditが生成された場合も同じrunで処理する。

各job完了後、blocked化後、または一時保管後に、GitHub readが可能なら最新queueを再取得する。固定件数・固定バッチ数・「1本終わったら終了」の上限は設けない。

GitHubへの成果反映を完了できなくても、完全な再送可能logical payloadをGoogle Drive outboxへ耐久保存できた時点を**後続jobへ進むためのチェックポイント**とする。元jobはGitHub上では未完了のまま残す。

全文取得不能や論文固有の依存不足が発生した場合も、対象jobだけをblocked/deferredとして、次の独立ready jobへ進む。これらをrun全体の停止理由にしない。

Discovery / blocked / deferred / rejectedは長文artifact不要なので、GitHub writeが利用可能なら固定inboxだけを小さくupdateしてよい。

## B. その他更新worker（08:30専用）

対象は以下だけ。

1. `framework-updates/**` — LLM推論・serving・runtime等の本質的更新
2. `llm-releases/**` — 新規LLMの正式公開・一般提供・主要更新

論文queueには触れない。Chatは対象ファイルを直接編集せず、既存の固定 `.survey/update-worker/update-payload.json` と `.survey/update-worker/update-inbox.json` だけを使い、Actionsへ反映を委譲する。

GitHub write失敗時は論文workerと同じhealth probe / continuation policyを使う。更新成果を一時保管できた場合は、問題を報告してもScheduled task自体を停止・無効化・再作成しない。

## 一時配送キュー

GitHub側でwriteを完了できない成果は、再投入可能な完全logical payloadとしてGoogle Drive `llm-paper-summary-outbox/pending` へ一時保管する。詳細なenvelope形式・folder ID・許可pathは [drive-outbox.md](drive-outbox.md) を正本とする。

DriveはGitHubの代替正本ではない。Drive保存成功をGitHub publication成功とは扱わず、queue上のjobは未完了のままにする。

Chat workerは完成MarkdownをDriveへ置かない。GitHubへ本来送る予定だった固定transport JSONを `schema_version: 1` のDrive envelopeに格納し、同一logical submissionの複数slotは1 envelopeにまとめる。Drive `pending` からGitHubへの回収、検証、commit、`processed` への移動はActionsに任せる。

GitHub Actions内のpushが失敗した場合は入力自体がGitHubへ届いているため、Driveへ重複保存せずActions側の再処理を優先する。

**一時保管成功後はStop Gateへ直行して終了するのではなく、次の独立ready jobを処理する。** 単一の反映保留、Drive保存失敗、pending replay失敗、1本処理完了、queueが一度空になったことをrun終了理由にしない。
