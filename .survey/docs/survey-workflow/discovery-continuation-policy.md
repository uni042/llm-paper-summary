# Discovery continuation policy

この文書は通常論文workerと毎時`:00` JSTの探索主体workerが、探索（discovery）をいつ継続し、いつresearchへ切り替えるかを定める。candidate水位とモード切替は `candidate-buffer-policy.md`、探索主体workerの詳細は `discovery-specialist-worker.md`、run終了判定は `continuation-policy.json` を正本とする。

## 基本原則

Discoveryの継続・終了を件数で決めない。round数、candidate数、submission数、Research/Audit完了数、candidate在庫は観測値であり、runの正常終了許可ではない。

通常runの正常終了は、実開始時刻 + 3600秒で定義したrun deadlineのhandoff guardだけで決める。guard外では、現在の探索軸が空・全重複・低採用・枯渇でも探索軸を再生成して継続する。

## Candidate quality and intake

候補件数のquota（ノルマ）やhard cap（固定上限）は設けない。弱い候補で件数を埋めない一方、強い候補を5件などへ切り詰めてもならない。

1 roundで得られた強い候補は、重複除外後にすべて `candidates` 配列へ含めてよい。queue/backendはcandidate配列を固定件数で拒否しない。外部transportの実payload制約がある場合だけ複数submissionへ分割し、総候補を失わない。

## Discovery mode

handoff guard外では次を繰り返す。

1. 最新identity / queue / discovery stateを読む。
2. candidate inventoryとactionable Research/Auditを確認する。
3. `candidate_inventory > 50` かつactionable Research/AuditありならOverflow research modeへ切り替える。
4. そうでなければ、前roundと異なる検索語・source・引用方向・隣接分野から探索軸を作る。
5. 軽量quality判定と重複除外を行い、強いcandidateを件数制限なしで耐久保存する。
6. 最新stateを取り直し、handoff guard外なら次の独立作業へ進む。

空round、全重複round、低採用率、1 source/APIの失敗、`next_axis_hint` 不在、既知軸の一巡はrun停止条件ではない。

## 探索空間の再生成

同じ検索式を機械的に繰り返さず、次を組み替える。

- 新着・recent revision
- forward citation
- backward reference
- 関連実装・同一著者・同一研究グループ
- DBMS / OS / storage / distributed systems / HPC / GPU runtime / networking / memory systems等の隣接分野
- 直近candidateからのkeyword / title / citation cluster拡張
- offload / hierarchical memory / SSD/NVMe / MoE expert placement・cache・prefetch / KV cache / scheduling / disaggregation / inference framework等の重点テーマ

現在の探索空間が枯れたという判断は、新しい探索空間を生成するトリガーであり、正常終了理由ではない。

## Overflow research mode

`candidate_inventory > 50` かつactionable Research/Auditがある場合、探索主体workerは通常論文workerと同じResearch/Audit契約へ切り替える。

- 1 workerが同時に保持する未完了claimは1件だけ。
- 完全payloadを耐久保存したらterminal反映を同期障壁にせず次stateを取得する。
- handoff guard外でactionable workが残る限り次jobへ進む。
- candidate inventoryが50以下、またはactionable Research/AuditなしになったらDiscovery modeへ戻る。

1run最低3件などの処理件数ノルマは設けない。

## Durability and abnormal blockers

GitHub direct persistenceを優先し、GitHub write不能でもChatGPT Library `/LLM-survey-outbox/pending/` へ完全payloadを耐久保存できるなら継続する。

canonical repositoryを読めない、GitHub/Library双方で必要状態を耐久保存できない、platform/tool hard limitに達した、などは異常blockerである。正常成功としてfinalizeする理由にはしない。

## Normal run finalization

正常runを終了してよいのは、run-local handoff guardが成立し、現在の成果とclaimが安全に耐久handoffされた場合だけである。

探索枯渇、candidate数、round数、submission数、job完了数、在庫状態は正常finalizationを許可しない。
