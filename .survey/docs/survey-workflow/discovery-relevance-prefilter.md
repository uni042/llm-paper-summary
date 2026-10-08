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
