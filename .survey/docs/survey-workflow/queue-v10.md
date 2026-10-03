# 保守者向け実装索引 — Library-first workflow v11

> **これはワーカー実行手順ではない。** Scheduled Chat / Workの実行判断は [`worker-router.md`](worker-router.md) を唯一のGitHub側人間向け正本とする。ここから閾値、ノルマ、停止条件、探索順序、保存先を再構成しない。

ファイル名 `queue-v10.md` は既存リンクとの互換性のため維持する。旧direct-GitHub運用時の内容は [`queue-v10-legacy-direct-github.md`](queue-v10-legacy-direct-github.md) へ退避した。

## 現行の運用境界

現在のScheduled workerはGitHub `main` を読み取り専用（read-only）で参照し、成果をChatGPTライブラリ（Library）へ保存する。GitHub反映はSurvey GitHub Importのワーク（Work）タスクが担当する。

したがって、以下のGitHub内部機構はScheduled workerの通常runの実行入口ではない。

- claim / reservation
- record bank
- research quality preflight fast lane
- immutable submission / result
- run-state / continuation / finalization
- worker-control / health-probe
- fallback-inbox / checkpoint transport

これらは、既存GitHub状態の解釈、過去成果の回収、リポジトリ内部自動化、回帰互換のため残る場合がある。存在することを理由にScheduled workerから新規生成・新規投入しない。

## 現行運用で参照する主な実装

Survey GitHub ImportのWorkタスクやリポジトリ保守では、必要に応じて次を使う。

- 論文identity解決: `.survey/scripts/resolve_paper_identity.py`
- 論文テンプレート: `.survey/templates/paper.md`
- 論文品質監査: `.survey/scripts/audit_paper_quality.py`
- 日本語文体検査: `.survey/scripts/japanese_style.py`
- 引用・候補pool: `.survey/scripts/reference_pool.py`
- 候補重要度設定: `.survey/config/candidate-priority.json`
- 候補重要度計算: `.survey/scripts/candidate_priority.py`
- venue / 被引用数cache更新: `.survey/scripts/refresh_candidate_priority.py`
- 全収録論文の前方引用巡回設定: `.survey/config/forward-citation-sweep.json`
- 全収録論文の前方引用巡回: `.survey/scripts/forward_citation_sweep.py`
- 前方引用巡回workflow: `.github/workflows/forward-citation-sweep.yml`
- relevance分類台帳: `.survey/scripts/reference_relevance_ledger.py`
- relevance request処理: `.survey/scripts/process_reference_relevance_requests.py`
- Discovery事前検査: `.survey/scripts/process_discovery_precheck.py`
- Discovery候補の正規queue反映: `.survey/scripts/queue_worker.py`
- repository整合性検査: `.survey/scripts/check_repository.py`
- repository inventory: `.survey/scripts/build_repository_inventory.py`
- 日次maintenance: `.github/workflows/maintenance.yml`
- STATUS表示生成: `.survey/scripts/render_status_dashboard.py`

上記のうちDiscovery事前検査やqueue反映は**Work側のGitHub取り込み**で使う。Scheduled workerがLibraryへ保存する前段でGitHubへrequest/submissionを書くためのものではない。

## Library側の実行手順

Scheduled workerの詳細HOWは次を参照する。

- `/LLM-paper-summary-library-first/WORKER-LIBRARY-PROCEDURES.md`
- Research作成時: `/LLM-paper-summary-library-first/PAPER-QUALITY-GUIDE.md`

Survey GitHub ImportのWorkタスクは次を参照する。

- Libraryの `github-import-procedure.md`
- 最新mainの `worker-router.md`

現行の主要値は`worker-router.md`にのみ置く。この索引へ数値を複製しない。

## 旧実装の扱い

旧direct-GitHub運用の詳細は次へ退避済み。

- `worker-router-legacy-v10.22-direct-github.md`
- `queue-v10-legacy-direct-github.md`

また、`library-checkpoint-registry.md`、`library-publication-ack.md`、`library-superseded-cleanup.md` は過去の `/LLM-survey-outbox/` 成果を回収するための互換・保守資料として扱う。新規Scheduled workerの保存方式ではない。

旧claim、run-state、fallback、submission等を扱うスクリプトやワークフローが残っていても、新規worker運用へ戻す根拠にはしない。削除可否は過去成果の回収依存と回帰テストを確認して別途判断する。

## STATUSと派生状態

`STATUS.md` は観測・表示面であり、Scheduled workerの現在のLibrary未反映成果を完全には表さない。モード判定は`worker-router.md`で定義するGitHub値とLibrary未反映分の補正を使う。

STATUSやqueueの派生ファイルを手で編集してLibrary成果を「反映済み」に見せない。GitHub反映はWorkタスクの正規identity照合・書込み・再取得確認を通す。

## 変更時の原則

運用を変更するときは次の順序を守る。

1. ユーザーの現行指示を確認する。
2. `worker-router.md`の責務分離を更新する。
3. Libraryのworker手順書 / GitHub取込手順書を整合させる。
4. 必要な実装と回帰テストだけを更新する。
5. 旧手順を現行文書内に併記せず、履歴資料へ退避する。
6. GitHub `main`から再取得し、現行正本に旧閾値・旧transportが混入していないことを確認する。

**実装の所在だけ**をこのファイルに残し、ワーカー実行手順の第二の正本を作らない。
