# LLM Survey Suggestion Box

このフォルダは、LLM研究サーベイの実行中に得た運用知見を、研究成果やfallbackとは分離して一時保管するための目安箱です。

対象は2種類です。

1. `improvement`: 「ここをこう変えると手間・失敗・無駄・復旧コストを減らせる」という具体的な改善案。
2. `continuation_obstacle`: 「この制約・確認・失敗・待ちがなければ、そのrunで本来はさらに処理を続けていた」という実行阻害の観測。改善策がまだ確定していなくても記録してよい。

## ディレクトリ

- `pending/`: まだユーザーへ報告していない提案・阻害要因
- `reported/`: 08:30 JSTの報告後に移動した直近の項目。個別ファイルは最大30件
- `archive/`: 古いreportedを圧縮した月次ダイジェストと長期要約

## 登録基準

実際の作業中に観測したものだけ登録する。目安箱を埋めるために作業を中断したり、無理に件数を増やしたりしない。

`improvement` は次を満たすものを登録する。

1. 実際に観測した摩擦、失敗、重複作業、無駄、復旧コスト、品質低下リスクに根拠がある。
2. 改善案が具体的で、どのコンポーネントをどう変えるか説明できる。
3. 既存の `pending/` および最近の `reported/` と実質重複していない。
4. 研究queueを止めてまで即時対応する重大障害ではない。重大障害は通常の問題報告・修復経路を使う。
5. 単なる好みや未検証の大規模再設計ではなく、期待効果と副作用を比較できる。

`continuation_obstacle` は、次の条件を満たす場合に登録する。

1. そのrunで、特定の仕組み・制約・エラー・確認作業・待ち・安全側判断などが原因で、本来続ける予定だった独立作業を開始または継続できなかった、あるいは明確に処理量が減った。
2. 「これがなければ何を続けていたか」を具体的に説明できる。
3. 単なるプラットフォーム上限そのものを毎回記録するのではなく、回避・短縮・先送り・自動化の余地がありそうな場合、または同種の阻害が再発している場合を優先する。
4. 改善策がまだ分からなくてもよい。その場合は `suggestion: unknown` とし、観測事実と失われた作業機会を残す。
5. 同じ原因・同じ対処候補の項目を毎run重複登録しない。既存項目へ統合できるなら新規作成しない。

## 1項目1ファイル

推奨ファイル名: `YYYYMMDDTHHMMSSJST-<short-slug>.md`

本文には最低限、次を含める。

- `type`: `improvement` / `continuation_obstacle`
- `observed_at`: 観測時刻
- `run_key`: 分かる場合はScheduled Chat run key
- `component`: queue / discovery / research / GitHub write / fallback / Actions / maintenance / notification / other
- `observation`: 実際に起きた手間・失敗・無駄・阻害
- `suggestion`: 変更案。未確定なら `unknown`
- `expected_benefit`: 改善時に何が良くなるか。未確定なら推定でよい
- `risk_or_tradeoff`: 副作用、複雑化、回帰リスク。未確定なら `unknown`
- `confidence`: high / medium / low
- `evidence`: 関連job、commit、ログ、状態ファイル等。なければ `none`

`continuation_obstacle` ではさらに次を必須とする。

- `would_have_continued_with`: 阻害がなければ次に実行していた具体的な作業
- `estimated_impact`: 失われた論文本数・探索ラウンド・write回数・時間等。正確に分からなければ定性的記述でよい
- `obstacle_class`: platform_limit / tool_or_connector / repository_design / workflow_rule / waiting_or_retry / validation / other

目安箱への保存失敗は研究runの停止条件にしない。研究成果・queue状態・fallback checkpointの保存を常に優先する。

## 08:30 JSTの扱い

08:30のその他更新workerは通常のframework / LLM release報告に加え、`pending/` を確認する。

- pendingが0件なら目安箱について余分な通知はしない。
- pendingがある場合、重複をまとめ、重要度の高い順に短く報告する。
- `improvement` と `continuation_obstacle` は分けて報告する。
- `improvement` は「観測された問題」「提案」「期待効果」「リスク」を含める。
- `continuation_obstacle` は「何が処理を止めた/遅らせたか」「それがなければ何を続けていたか」「影響」「考えられる対策（あれば）」を含める。
- 自動実装はしない。ユーザーが明示的に採用を指示した案だけ実装する。
- ユーザーへの報告を生成した後でのみ、その日に報告したファイルを `reported/` へ移す。先に移動しない。
- 報告後の移動に失敗した場合はpendingに残し、次回重複報告の可能性を許容する。未報告のまま失うより安全側を優先する。

## reported / archive の肥大化防止

08:30の報告処理後にbest-effortで整理する。

1. `reported/` は新しい個別項目30件だけを保持する。
2. 30件を超えた古い個別項目は、対象月ごとに `archive/YYYY-MM.md` へ要点を統合する。
3. 月次ダイジェストには日付、type、component、観測問題、提案、期待効果、リスク、`would_have_continued_with`（該当時）、分かる場合は採否だけを残し、重複内容は統合する。
4. ダイジェストの保存成功を確認してから、対応する古い個別ファイルを削除する。保存失敗時は原本を残す。
5. 月次ダイジェストは直近12か月分まで保持する。12か月を超えたものは `archive/history-summary.md` へ再要約した後、元の月次ファイルを削除する。
6. `history-summary.md` は再発しやすい失敗、繰り返し処理量を落とす阻害要因、採用済みで有効だった改善、避けるべき設計だけを簡潔に残し、同じ知見を重複追記しない。
7. 整理失敗は研究や更新workerの停止理由にしない。

## 非目標

- 論文候補や研究成果の保存先にはしない。
- GitHub/Library fallbackの代替にしない。
- workerの停止条件に使わない。
- pending件数を研究処理能力の上限にしない。
- `continuation_obstacle` を「停止してよい理由」の記録として使わない。可能なら通常のcontinuation policyに従って同じrun内で処理を続け、実際に阻害された場合だけ観測として残す。
