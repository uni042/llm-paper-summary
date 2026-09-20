# 保守者向け実装索引 — workflow v10

> **これはワーカー実行手順ではない。** Scheduled Chat / Work のワーカーは [`worker-router.md`](worker-router.md) だけを人間向け手順正本として読む。ここから閾値、ノルマ、停止条件、探索順序、保存手順を再構成しない。

このファイル名は既存リンクとの互換性のため残している。重複した運用手順は削除し、実装の所在だけを示す。

## 現行の実装境界

- ルーティング・継続判定: `.survey/scripts/continuation_gate.py`
- 最終化判定: `.survey/scripts/run_finalization_gate.py`
- Research / Audit の担当確保: `.survey/scripts/claim_worker_with_banks.py`
- Discovery の固定ソース事前検査: `.survey/scripts/process_discovery_precheck.py`
- 固定ソースのページ送り・重複排除: `.survey/scripts/discovery_search_filter.py`
- Discovery submission の検証・Research job 化: `.survey/scripts/queue_worker.py`
- immutable submission 処理: `.survey/scripts/process_immutable_submission.py`
- Library fallback の復旧: `.survey/scripts/replay_record_fallback.py`
- ワーカー向け案内: `.survey/scripts/worker_guidance.py`
- 日次 maintenance: `.github/workflows/maintenance.yml`

## 正本関係

ワーカー行動は `worker-router.md` と上記正規スクリプトが返す `[WORKER-GUIDE]` / `next_action` / `recovery_steps` に従う。実装契約は対応するテストで固定する。

過去のschema、固定 `chat-inbox.json`、旧fallback、旧claim/record-bank形式などのコードが残る場合は**既存履歴の読取・救済専用**である。新規生成、新規分岐、エラー回避経路として使わない。

## 変更時の原則

現行経路を変更するときは、先に実行コードと回帰テストを更新し、その後 `worker-router.md` の人間向け説明だけを同期する。同じ数値条件やHOWをこの索引へ複製しない。
