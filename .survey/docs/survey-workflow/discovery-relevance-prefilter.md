# Discovery関連性事前フィルタ（2026-10-08 試験運用）

この機能は候補を削除せず、専用ワーカーの探索候補表示だけを調整します。参考文献・前方引用候補プール、既存の採否台帳、収録・Researchジョブは変更しません。

## 設定と復旧

- 設定: .survey/config/discovery-relevance-prefilter.json
- 実装: .survey/scripts/discovery_relevance_prefilter.py
- enabled=true, mode=quarantine: 明確な異分野応用でシステム技術の証拠が見つからない候補を一時隔離
- mode=shadow: 全候補を通常どおり表示し、隔離見込み件数だけ集計
- enabled=false または mode=off: 次回のワーカー一覧再生成で従来の並びへ戻す
- allow_canonical_ids: 機械誤判定から復活させる論文ID一覧
- audit_stride=50, max_audit_per_build=30: 隔離候補から決定論的に小標本を抽出して通常一覧に再投入

## 境界と確認方法

初期版はタイトルに明確な異分野の応用が書かれているものだけを候補とし、概要中にKVキャッシュ・オフロード・量子化などのシステム機構が見つかれば救済します。自動的な unrelated 判定は絶対に作りません。件数は分類済み論文数ではなくワーカー一覧の表示抑制数です。

導入後は Repository regression tests と Survey status dashboard の両ワークフローを確認してください。隔離されたサンプルの採用率と前方・後方参照別の流入率を測定し、再現率を検証するまではルールを強化しないでください。

## 教師あり分類器と分割進捗（2026-10-08）

既存の収録論文タイトルを正例、確定済みunrelatedタイトルを負例に学習する、多項ナイーブベイズ分類器（Python標準ライブラリのみ）を追加。正例の独立検証セットで誤隔離が0件となる閾値より厳しい条件でのみ暫定隔離。実データの検証性能は誤判定ゼロを保証しないため、従来の監査再投入は維持する。

- 毎回最大2,000件を分類し、判定したidentityとタイトルのハッシュを16分割でGitHub保存。失敗時も保存済みの先行バッチを再利用する。
- モデルは最初のrunで一度訓練してGitHubに固定保存する。異なるモデルIDで過去の判定を流用しない。
- 新着候補とタイトル変更は未処理として後続バッチへ戻る。未処理を自動的に無関係判定しない。
- status-dashboardは同一の現在候補集合に対してフィルタ前件数、規則隔離、分類器追加隔離、監査復活、最終読解可能件数、分類器処理済・未処理を直接再計算してSTATUSに表示する。
- 再実行はGitHub Actionsの Incremental Discovery relevance classifier を使用する。30分ごとに1バッチを試みるがGitHubスケジューラはbest-effortであり遅延・欠落があり得る。
- 緊急復旧は設定 enabled=false。分類器のみ無効化したければ classifier.enabled=false。
