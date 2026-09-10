# 未送信バックログ非阻害ポリシー

この文書は、GitHubへ未送信の研究成果が増えても新しい論文サーベイを止めないための正本である。

## 最重要原則

完成済みだが未送信の研究成果は**配送待ちバックログ**であり、研究停止理由ではない。record bankはGitHubへ直接送る際の一時ステージであり、未送信論文を保存し続けるための待ち行列ではない。

完成したlogical payloadをGitHubへ反映できなくてもGoogle Drive outboxへ耐久保存できた時点で、その成果は後続作業へ進むためのチェックポイントを獲得する。GitHub上のjob自体はActionsで最終反映されるまで未完了のまま残すが、そのjobやbankを理由に同じrunの独立ready jobを止めない。

## record bank

利用可能な固定bankの正本は `.survey/work-queue/records/bank-registry.json`。現在はA〜Hの8 bankを用意し、各bankに同じ5 slotを持つ。

- `metadata.json`
- `problem_method.json`
- `evaluation.json`
- `results.json`
- `positioning.json`

GitHubへ直接送る前に、可能なら次を実行してbank状態を機械判定する。

```bash
python .survey/scripts/select_record_bank.py --repo-root .
```

このスクリプトは `next-jobs.json`、現在の `chat-inbox.json` / result、各bankの `attempt_id` / `job_id` を照合し、直接writeに使えるbankを `selected_bank` として返す。LLMが見た目だけでbankを再利用可能と推測しない。

完全payloadがDriveへ耐久保存済みなら、そのpayloadはbankの唯一のコピーではないため後続研究を拘束しない。A〜Hがすべて使用中・dirtyに見える場合でもDriveへ保存可能なら**runを止めない**。新しい完成成果もDrive envelopeへ保存して次の独立jobへ進む。bank exhaustionは配送経路上の状態であって研究容量上限ではない。

## Driveバックログ

`/Google Drive/llm-paper-summary-outbox/pending/` には複数の未送信論文が蓄積してよい。pending件数は、そのrunで新しく精読できる論文数を減らす条件にしない。

research/audit envelopeは1論文につき1ファイルとし、1つのbankの5 slotすべてと `chat-inbox.json` を同じenvelopeへ含める。1論文を複数envelopeへ分割しない。完成MarkdownはDriveへ保存しない。

Drive importerはChat research workerとは独立してバックログを排出する。1回のImporter実行でGitHubへ投入するlogical envelopeは最大1件とする。現在の再利用 `chat-inbox.json` に対する処理結果がまだ作られていない場合、次のresearch/audit envelopeで上書きしない。

複数pendingを一度に展開すると、同じ再利用bankと `chat-inbox.json` を後のpayloadが上書きして前の論文が失われる可能性がある。このため**1件ずつ投入 + inbox/result照合**を必須とする。

不正JSONや許可外pathのenvelopeは `failed` へ隔離し、後続の正常payloadを止めない。research transportがbusyでも、それと独立したframework/model update envelopeが後ろにあれば処理してよい。

## GitHub write失敗時

論文固有のGitHub transport失敗はその論文だけの問題として扱う。`worker-router.md` に従って再試行とhealth probeを行い、完全payloadをDriveへ保存できたら次の独立jobへ進む。

`target_or_payload_specific` の場合、影響を受けたpayloadだけDriveへ保存し、他のGitHub writeは継続してよい。

`run_wide_github_write_unavailable` の場合、そのrunでは以後GitHub writeを繰り返さない。後続jobの精読・構造化record作成は続け、完成するたびDriveへ保存する。

Drive pendingが増えていること自体は `STOP_RUN` にしない。停止条件は `continuation-policy.json` のみを使い、完成成果をGitHubにもDriveにも耐久保存できない場合や、残作業すべてが共通の全体依存で処理不能な場合などに限定する。

## 回復時

GitHub transportが利用可能になれば、Drive importerがpendingを古い順に排出する。ただし前のChat transportのresultが確認できるまで次のresearch envelopeは投入しない。

これにより、一時的なGitHub write障害が長時間続いて未送信論文が多数溜まっても、Chat workerはDriveへ完成成果を積み続けられ、A〜Hの固定bank数が論文サーベイ全体の上限になることを防ぐ。
