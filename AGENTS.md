# リポジトリ固有の協調規約

- 最新の `main` を正本とする。dirtyな変更や無関係な変更は保持し、勝手に戻さない。
- Solはdispatch前に `objective`、`write_set`、`read_set`、禁止範囲、不変条件、受入コマンド、統合順序を凍結する。
- 通常の並列実装は適応型 `3+1`（独立実装Luna最大3人、read-onlyレビューまたは隔離blocker調査用Luna 1人を常に予約）とする。
- `fork_turns="none"` を使い、会話履歴全体を貼り付けない。完全な要件は1つのfile-backed briefに置く。
- Lunaは他のLunaへ委譲せず、重複しない所有範囲で inspect → implement → focused test → fix → retest → local verification を、可能な限り1 turnで完了する。定例の進捗pollingや同じ内容の反復要約はしない。
- report pathが指定された場合、Lunaは詳細な証跡をそこへ書き、chatには状態、commit/change files、1行のテスト結果、懸念だけを返す。状態は `EVIDENCE_READY`、`BLOCKED_EVIDENCE`、`CONFLICT` のいずれかとする。
- blocker reportには stage、class、exact error、再現コマンド、exit code、expected/actual、files、試行、未達の受入条件、次に調査すべきproblem domainを含める。同一root causeに対する総試行は初回を含め最大2回とし、その後は停止またはglobal Astra条件に従ってescalateする。
- Lunasに重複するfile ownershipや未凍結interfaceを割り当てない。claim allocator/state、dispatcher/record bank、queue/discovery、GC/maintenanceはwrite setとinterfaceが凍結されている場合だけ別unitに分ける。workflow filesとcanonical docsは直列化する。
- canonical repository writers、workflow定義、paper/index/state更新、shared generated outputsは直列化する。`survey-helper-main` はcanonical GitHub Actions writer groupであり、別名のconcurrency groupだけを根拠に安全とみなさない。
- commit、push、PR/merge、GitHub settings、Actions dispatch/rerun、credential変更、dependency install、destructive/live operationはSol所有とする。Solは初期partition、blocker triage、最終acceptance、external effectsに介入する。
- focused test、関連regression、`git diff --check` の順に確認する。local test、CI、pushの結果を区別する。
