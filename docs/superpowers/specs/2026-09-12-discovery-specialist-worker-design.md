# Discovery Specialist Worker Design

## Goal

既存の毎時`:30` LLM研究サーベイworkerからdiscovery機能を取り上げず、そのまま維持した上で、毎時`:00`に動く探索専用Scheduled Chat workerを追加し、research候補在庫を継続的に補充する。

## Architecture

探索専用workerは既存のcandidate bufferとidentity/重複判定を共有する追加producerとして扱う。新しい独立queue体系は作らず、既存workerと同じcanonical candidate pool / queueへ候補を投入する。既存`:30` workerは従来どおり水位に応じてdiscovery / research / auditを実行できる。

`:00`と`:30`へ時間をずらし、同時実行確率を下げる。ただし時刻分離だけを排他制御として信用せず、candidate投入はcanonical ID、arXiv ID、DOI、normalized titleによる重複排除を必須にする。同じ論文を両workerが発見した場合は1候補へ収束させる。

## Discovery-only worker responsibilities

探索専用workerは次だけを担当する。

1. 最新mainとcandidate-buffer-policy、worker-router、queue/identity/discovery-stateを読む。
2. candidate inventoryと最近の探索履歴を確認する。
3. 新着、被引用、参考文献、隣接分野、検索語拡張、重点テーマの複数探索経路を回す。
4. Discovery段階の軽量評価だけを行い、原則として全文精読・5-slot research record作成・paper Markdown生成をしない。
5. 重複排除した有望候補へpriorityを付け、既存candidate pool / research queueへ耐久投入する。
6. 各探索軸の取得数、重複数、新規候補数、採用数/率をdiscovery stateへ記録する。
7. GitHub write不能時は既存fallback-routingに従いLibrary `/LLM-survey-outbox/pending/` へoffline job seedを保存する。

探索専用workerはresearch、audit、08:30 other-update、maintenance counterの加算を行わない。maintenance-cycleは参照してもよいが、既存`:30` workerの24-run maintenance cadenceを二重計上しない。

## Candidate buffer behavior

`target_inventory=50`、`low_watermark=25`、`critical_watermark=15`を共有する。

探索専用workerは在庫50以上でもhard stopせず、新着確認や引用追跡など低コスト探索で高価値候補を追加してよい。在庫25未満では探索幅を広げ、15未満では複数経路を積極的に使う。件数のために弱い候補を採用しない。

既存`:30` workerも同じ規則でdiscoveryを継続できる。探索専用worker追加を理由に既存workerから探索を削除・無効化・抑制しない。

## Concurrency and idempotency

候補の同一性は可能な順にarXiv ID、DOI、canonical URL、normalized titleで判定する。投入直前に最新queue/identityを再取得し、既収録、既candidate、ready/research中、checkpoint済みfallback候補との重複を再確認する。

同一候補が既に存在する場合は新規jobを増やさず、必要なら既存candidateのpriority/evidenceだけを安全に補強する。異なるworker由来であることを理由に別jobを作らない。

GitHub SHA競合時は最新状態を再取得して重複判定からやり直す。盲目的な上書きはしない。

## Scheduling

- 探索専用worker: 毎時`:00` JST
- 既存survey worker: 現状どおり毎時`:30` JST

探索専用workerは通常成功時に通知しない。GitHub/Library双方へ耐久保存できない、identity/queue破損など継続不能な問題がある場合のみ通知する。

## Reporting

08:30報告の24時間集計は両worker由来のdiscoveryを合わせて数える。同じcandidateは重複排除して1件とする。既存の「発見数・追加数・残候補数・candidate_inventory/50」の定義は維持する。

## Failure handling

GitHub direct write失敗時は既存continuation-policyとfallback-routingを使用する。単一候補の競合・重複・取得失敗でrun全体を止めない。GitHub directとLibrary durable fallbackの両方が使えず状態保存不能な場合のみrun停止を検討する。

## Success criteria

- 毎時`:00`の探索専用workerが候補を補充する。
- 既存`:30` workerは引き続きdiscovery可能。
- 両workerが同じ論文を発見しても候補/jobが二重化しない。
- maintenance cadenceは既存workerだけで数え、探索専用workerで加速しない。
- 08:30の24h discovery集計は両workerの成果を重複なしで反映する。
