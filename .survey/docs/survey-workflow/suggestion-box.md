# Scheduled Chat suggestion box

目的: 研究・探索・queue・fallback・Actions・maintenance・通知などの実作業中に得た「ここをこう変えると手間、失敗、重複作業、復旧コストを減らせる」という運用知見を、研究成果や障害処理とは分離して保存し、08:30 JSTにユーザーへまとめて報告する。

Library上の正本:

- `/LLM-survey-suggestion-box/README.md`
- `/LLM-survey-suggestion-box/pending/`
- `/LLM-survey-suggestion-box/reported/`

## 通常runでの登録

実際の作業中に具体的な改善知見を得た場合だけ、`pending/` に1提案1ファイルで保存する。提案作成そのものを目的に探索したり、無理に件数を増やしたりしない。

登録対象は次を満たすものに限る。

1. 実際に観測した摩擦、失敗、重複作業、無駄、復旧コスト、品質低下リスクに根拠がある。
2. 改善案が具体的で、どこをどう変えるか説明できる。
3. `pending/` と最近の `reported/` に実質同一の提案がない。
4. 即時修復すべき重大障害ではない。重大障害は通常の問題報告・修復経路を使う。
5. 大規模再設計を思いつきだけで提案せず、期待効果と副作用を比較できる。

推奨ファイル名は `YYYYMMDDTHHMMSSJST-<short-slug>.md`。最低限、次を記録する。

- `observed_at`
- `run_key`（分かる場合）
- `component`
- `observation`
- `suggestion`
- `expected_benefit`
- `risk_or_tradeoff`
- `confidence`: `high` / `medium` / `low`
- `evidence`: 関連job、commit、ログ、状態ファイル等。なければ `none`

目安箱への保存失敗は研究runの停止条件にしない。研究成果・queue状態・fallback checkpointの保存を常に優先する。

## 08:30 JSTの報告

08:30のその他更新workerではframework / LLM release更新の確認に加え、Libraryの `pending/` を読む。

- pendingが0件なら、目安箱について余分な通知は出さない。
- pendingがある場合、実質重複をまとめ、重要度の高い順に簡潔に報告する。
- 各項目は少なくとも「観測された問題」「提案」「期待効果」「リスク」を含める。
- 目安箱の案は08:30 workerが自動実装しない。ユーザーが明示的に採用した案だけ別run/対話で実装する。
- **ユーザーへの報告を生成した後でのみ**、その日に報告したファイルを `reported/` へ移す。報告前に移動しない。
- 報告後の移動に失敗した場合はpendingに残す。重複報告の可能性より、未報告の提案を失うリスクを避ける。

## 非目標

目安箱は論文候補、research record、fallback、queue、run ledgerの代替ではない。pending件数を研究容量やrun停止判断に使わない。
