# 補助プログラムと共通形式

## 実行環境

Python 3.10以上と `scripts/requirements.txt` の依存を使う。実行前にPython・依存・ファイル取得・書込み可否を個別に確認する。通常チャットにデータ分析機能があっても、予定タスクでPython・通信・永続ファイル・任意の追加ライブラリを使えるとは仮定しない。

使える場合は、同じ版のプログラムと対象ファイルを実行環境へ渡す。Pythonの実行とGitHubへの読み書きは別の能力であり、保存には接続機能を使ってよい。依存を追加できなければ接続機能による確認へ切り替え、未実行の検査を明示する。

## コマンド一覧

リポジトリ直下で実行する。必要な場合だけ依存を導入する。

```bash
python -m pip install -r scripts/requirements.txt
python scripts/survey.py build
python scripts/survey.py validate
python scripts/check_repository.py --inventory /tmp/repository-inventory.json --report /tmp/integrity.json
python -m unittest discover -s tests
```

| コマンド | 役割 |
|---|---|
| `build` | 識別索引、系統一覧、上位件数、比較表、進捗を決定的に生成 |
| `validate` | 推論索引、必須属性、現在計画、未完了一覧、除外・再確認を検査 |
| `check_repository.py` | 全ファイルの構造・参照・状態・凍結・生成差分を読取り専用で検査 |
| `select-mode` | 予定枠と起動元の時刻指定から夜間・朝・選定・精読を判定 |
| `route` | 精読時の当日計画欠落・選定途中・旧期間を検出 |
| `closing-result` | 前計画の次目標と繰越を計算。履歴と新計画の保存は別工程 |
| `lease acquire/renew/release` | ローカルの作業権更新。リモート確認まで取得成功ではない |
| `run start/progress/finish` | 観測記録の開始・更新・終了 |
| `retry-failure`、`due` | 7日間隔の再確認履歴と期限到来候補 |
| `cleanup` | 終了済み詳細記録の24時間整理。夜間だけ実施 |

`build` と `validate` の全件実行は夜間または明示的な保守で使う。通常の論文保存時は当該論文・関連状態・索引差分を検査する。`scripts/migrate_v5.py` は旧形式からの移行専用で、通常実行で呼ばない。

## 論文属性と識別索引

[論文ひな型](../../templates/paper.md)を共通形式とする。必須キーは `canonical_id`, `title`, `summary`, `source`, `last_audited`, `audit_version`。監査未実施は `last_audited: null`, `audit_version: 0`。形式移行だけでは監査済みにしない。

確認済みの `arxiv_id`, `doi`, `openreview_id` を同じページに保存する。改題・会議版の追加でも既存の `canonical_id` は維持する。新規識別子の優先順はarXiv、DOI、OpenReview、その他安定識別子。題名類似だけで同一研究と断定しない。

索引形式3の `papers[canonical_id].path` から直接保存先を解決し、`identifier_to_canonical` で別識別子を照合する。`source_hash` はローカル論文ファイルとの照合用で、一次資料の確認証拠ではない。`ignored_moved_stubs` の移動案内は件数から除く。

## 比較属性

`storage_targets`, `bottlenecks`, `hardware_details`, `quality_effect`, `evidence_locations` を使う。既存の `summary`, `topics`, `hardware_evaluation`, `code` も表示する。未確認は空配列またはnullとし、非対応や実装なしと解釈しない。

出典属性は一次資料URL・版・節/表/図・裏付ける主張を含める。次の通常監査で確認できた分を補い、比較表のためだけに全論文を再精読しない。自動生成範囲を手で編集しない。

作業権と観測記録は[state.md](state.md)、取得再確認は[retries.md](retries.md)、夜間の実行手順は[nightly.md](nightly.md)を正本とする。
