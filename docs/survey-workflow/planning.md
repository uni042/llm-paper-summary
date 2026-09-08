# 周の精読・監査対象の選定

run 1だけが選定を担当する。時刻や日付で新しいplanを作らない。

## 前周からの引継ぎ

1. 前周planとprogress deltaを統合し、未完了の精読・監査を抽出する。
2. queueに以前から残る繰越も重複除去して加える。
3. 現在の `targets.research` / `targets.audit` をNとする。
4. 古い繰越から優先し、繰越＋新規候補の合計が各N本になるように選ぶ。
5. 繰越がN本以上なら新規探索は行わず、古い繰越からN本だけ当周へ割り当てる。余剰繰越はqueueに残す。
6. 繰越がN本未満なら不足分だけ新規探索・監査選定を行う。

移行だけで完了数や目標を変えない。前周の締め結果は `cycle-history/<cycle_id>.json` を正本とし、同じcycleを二度締めない。

## 精読候補

新規候補は以下を確認・記録する。
`publication_date`, `last_revision_date`, `venue`, `venue_status`, `venue_verified_url`, `priority_tier`, `priority_reason`.

優先度:
- A: 直近180日以内の公開/大幅改訂 + 主要査読会議/誌で公式採択確認
- B: 直近90日以内 + 推論システム上の新規性が高いpreprint等
- C: 主要会議/誌採択済みで重要な既存空白を埋める
- D: その他の重要候補

tier内は新しい改訂/公開を優先し、同条件では推論システムへの直接性、既存との差、実機評価を比較する。採択は会議公式/OpenReview/出版社等で確認する。

## 一次資料preflight

当周planへ新規採用する前に、通常の一次資料本文経路を実際に確認し、失敗時は同一研究の別公式経路を1つ確認する。双方取れなければplan枠を消費せず `retry-papers.json` へ記録し、別候補を探す。取得失敗だけで永久除外しない。

preflightは全文精読ではない。

## 監査候補

繰越を優先し、不足分を既存推論論文から選ぶ。監査形式の欠落、旧版、採択/実装/評価情報の未確認、監査日の古さを優先する。同一系統へ偏りすぎない。

## plan保存

新規cycleのplanは `survey-state/cycle-plans/<cycle_id>.json` に保存する。選定項目は初期状態 `pending` とし、その後の完了はprogress deltaへ書く。plan保存と `cycle-state.current_plan_id/current_plan_path` の設定を同一変更にできる場合はまとめる。できない場合はplanを先に保存し、次runが存在を照合してcycle stateをreconcileする。

早期繰上げで同じ予定実行内に新cycleへ移った場合は、その場でrun 1をclaimして可能な範囲までこの選定を行う。
