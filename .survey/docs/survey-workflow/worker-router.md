# Chat worker router — workflow v10

予定されたChat workerは**1つだけ**。実行時刻で次のどちらか一方を選び、同じ枠で両方を処理しない。

- **08:30 JST** → その他更新worker
- **それ以外の毎時 :30** → 論文worker

毎回default branch最新HEADを取得し、このrouterと [queue-v10.md](queue-v10.md) を同じHEADから読む。

## 実行前の共通回復

GitHubへの反映が利用可能な場合、外部設定されたNotion一時配送キューの `pending` と、private設定で指定されたChatGPT Library一時配送キューの `pending` を確認する。現在のqueue/identity/対象blobと整合する成果だけを、新規作業より先にGitHubへ再投入する。再投入中は `replaying`、Actionsの成功確認後のみ `replayed` とする。すでにterminal/supersededで適用対象外になったものは盲目的に反映せず `dead_letter` とし理由を残す。

pending再投入は新規研究を飢餓させない。各pending payloadの再投入試行は**1 runにつき最大1回**とする。さらに、権限状態・connector write不能・同種の操作検証失敗など、複数pendingに共通すると判断できる `Failure Class` で1件の再投入が失敗した場合、そのrunでは同じ `Failure Class` の残りpendingを個別に再試行しない。失敗したpayloadは `pending` のまま保持し、完全payloadが耐久保存済みでGitHub readが可能なら、直ちに通常のready job処理へ進む。再投入成功が続く場合は古いpendingから順に回復してよいが、同じ原因の失敗を反復してrun時間を消費しない。

GitHub readができない場合は、repo状態に依存する新規処理を開始しない。

## A. 論文worker

正本: [README.md](README.md)、[queue-v10.md](queue-v10.md)、[paper template](../../templates/paper.md)、`.survey/work-queue/next-jobs.json`。

**research / auditに着手する前に `.survey/templates/paper.md` を必ず読む。** テンプレート内で品質基準として指定されている [MoE-Infinity のまとめ](../../../papers/inference/01-offload-hierarchical-memory/2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md) も、少なくとも新しい実行環境・新しい会話で最初に1回は確認する。以降の論文は、論文未読者が背景・手法・データの流れ・なぜ効くか・効かない条件まで追える説明密度を基準にする。

Chatは探索・全文精読・科学的判断・監査判断と**構造化research record**作成を担当する。完成Markdownは作成・送信しない。research/auditはqueue-v10で定義されたA/B固定record bankのうち利用可能な1 bankの5 JSON slotを使い、全slot成功後のみ固定 `chat-inbox.json` をtriggerする。通常はA、Aに別jobの途中保存が残る場合だけBを使う。paper/state/README/identity/queueをChatから直接編集しない。

構造化recordは「後でMarkdown rendererが文章を補ってくれる」前提で短縮しない。特に `problem_method` は、論文固有の略語や機構名を列挙するメモではなく、**そのまま人間向け本文として読める説明文**を入れる。狭い分野の語は最初に平易な日本語で意味を説明し、手法が複数段ある場合は各段の入力・処理・出力・次段との接続・ボトルネックへの効果を書く。

**GitHubへslotを書き始める前に `.survey/templates/paper.md` に対する最終品質チェックを行う。** 複数機構を持つsystem論文では、主要機構ごとの `components[].description` を原則2〜4段落程度の説明文にし、少なくとも「何を入力・観測するか」「何を選択・移動・削除・予測するか」「前後の機構とどう接続するか」「なぜボトルネックが減るか」「追加costと失敗・資源不足時の挙動」を読者が追える状態にする。論文固有または狭い分野の用語・略語・評価指標は初出で平易に説明する。`results` は数値ごとに比較対象・条件・結果の読み方を持たせ、悪化条件・negative resultも省略しない。`metadata.overview` が使える場合は、問題・従来方式・提案・対象環境・実機/simulationの別を数段落で記述する。これらを満たさないrecordは完成扱いにせず、そのrunで本文へ戻って補強してから送信する。

**同一runで継続処理する。** 開始時に既存ready research/auditがあればpriority順に処理する。readyが尽きたらdiscoveryを実行し、Actions反映後の最新queueを読み直して、そのdiscoveryから生成されたresearch jobを同じrunで直ちに全文精読・構造化record保存・Actions結果確認まで進める。researchからauditが生成された場合も同じrunで処理する。各job完了後に必ず最新queueを再取得する。

queueが再び空になりActionsが新しいdiscovery jobを補充した場合も、そのrunを終了せず次のdiscoveryへ進む。つまり **discovery → research → 必要ならaudit → 最新queue再取得 → 次discovery** を、実行環境が許す限り繰り返す。固定件数・固定バッチ数・「1本終わったら終了」の上限は設けない。

GitHubへの成果反映を完了できなくても、完全な再送可能logical payloadをNotionまたはChatGPT Libraryの一時配送キューへ耐久保存できた時点ではrunを停止しない。そのjobはqueue上では未完了のまま残すが、一時保管を**後続jobへ進むための耐久チェックポイント**として扱い、同じrunで次のready jobへ進む。一時保管済みpayloadがそのattemptの完全な再送情報を持つなら、GitHub固定record bankに残ったpartial slotは唯一の成果コピーではないため、後続jobのためにそのbankを再利用してよい。inbox未送信のpartial slotだけを理由にA/B bankを恒久占有しない。

次回へ残してよいのは、全文取得不能、GitHub read不能、明確な時間・実行回数・コンテキスト等のプラットフォーム上限、未解決の依存、またはGitHub/Notion/Libraryのいずれにも次成果を耐久保存できない場合だけとする。単にGitHubやNotionへの反映が保留になった、pending再投入が失敗した、discoveryが終わった、1本処理した、queueへ次jobが現れた、あるいは一度queueが空になったことを終了理由にしない。停止時点でqueueに残ったjobと一時配送キューのpendingは次回runが引き継ぐ。

Discovery / blocked / deferred / rejectedは長文artifact不要なので、固定inboxだけを小さくupdateしてよい。

## B. その他更新worker（08:30専用）

対象は以下だけ。

1. `framework-updates/**` — LLM推論・serving・runtime等の本質的更新
2. `llm-releases/**` — 新規LLMの正式公開・一般提供・主要更新

論文queueには触れない。Chatは対象ファイルを直接編集せず、既存の固定 `.survey/update-worker/update-payload.json` と `.survey/update-worker/update-inbox.json` だけを使い、Actionsへ反映を委譲する。既存ファイルは現在blob SHA付きcompact editを優先する。

## GitHub反映保留時の扱い

GitHub側でwriteを完了できない場合（権限状態、接続状態、操作検証、SHA競合など）は、最新状態を取り直して対象単位を1回再試行する。それでも反映できなければ成果を完了扱いにせず、論理payloadを外部設定されたNotion一時配送キューへ `pending` として保存する。Notionにも保存できない場合は、private設定で指定されたChatGPT Library一時配送キューへ再送可能な完全payloadを `pending` 保存する。

NotionまたはLibraryへの一時保管が成功した場合、GitHub publication成功とは扱わずqueue上のjobは未完了のままにする一方、同じrunの後続job処理は継続する。3つの保存先のいずれにも成果を保持できない場合だけ、その成果を保持できないため後続処理を停止して報告する。

Notion/LibraryはGitHubの代替正本ではない。GitHub Actions内のpushが保留になった場合は入力がGitHubに届いているため外部の一時配送キューへ重複保存せず、Actions側の再処理を優先する。

単一の反映保留を理由に予定タスク自身を停止・無効化・再作成しない。
