# Discovery continuation policy

この文書は通常論文workerと毎時`:00` JSTの探索主体workerが、探索（discovery）をいつ継続し、いつ研究消化へ切り替えるかを定める。candidate水位とモード切替の正本は `candidate-buffer-policy.md`、探索主体worker固有の動作は `discovery-specialist-worker.md`、run終了判定の正本は `continuation-policy.json` / `continuation_gate.py` / `run_finalization_gate.py` とする。

## 終了判断の責務

worker自身が「十分探索した」「もう枯渇した」「長く動いた」「時間が厳しそう」といった主観でrun終了を決める必要はない。workerの責務は、最新HEAD・queue・candidate inventory・claim/transport状態・実開始基準のrun deadlineなど、観測可能な正本状態を正確に取得してgateへ渡し、返された `decision` / `required_action` / `next_action` / `finalization_permit` に従うことである。

停止を正当化するために、存在しないエラー、platform limit、読取失敗、耐久保存失敗、探索枯渇を推測・生成してはならない。実際に観測した事実だけをgate入力と終了報告へ使う。

`continuation_gate.py` が `CONTINUE` を返した場合は返された行動を実行する。`run_finalization_gate.py` が `MUST_CONTINUE` を返した場合も同様に `next_action` を実行する。正常な最終応答は `MAY_FINALIZE` かつ `finalization_permit.issued=true` の場合だけ行う。この規則は「workerを無理に働かせる」ためではなく、終了可否の判断を決定論的なscriptへ集約するためのものである。

## 基本原則

探索は、有望な候補を供給できる限り1回の空振りや重複だけで終了しない。ただし **candidate在庫が十分に積み上がった場合は探索を続けること自体が目的ではない。** `candidate_inventory > 50` かつactionable Research/Auditがある場合、探索主体workerはoverflow research modeへ切り替え、discoveryを一時停止して追加readerとしてbacklog消化に加勢する。

candidate在庫が50以下へ戻る、またはactionable Research/Auditがなくなった場合は、探索主体workerは通常探索モードへ戻る。candidate在庫の多さはrun終了条件ではなく、**discoveryからresearchへのモード切替条件**である。

## Discovery modeでの継続判断

通常探索モードでは、次の値は探索戦略・統計のための入力であり、単独でも組み合わせても正常終了の許可には使わない。

- discovery round数、submission数、candidate数
- 0件round、全重複round、低採用率round
- `discovery_exhausted` の自己評価
- 現在の `next_axis_hint` が空であること
- 1 source / API / queryの失敗
- 1候補の全文取得や証拠不足
- 1回のGitHub write競合や、代替経路が残る局所的fallback失敗
- 1件または複数件のResearch/Audit完了数

これらは `discovery_stats` へ記録し、必要なら探索軸、query family、source、引用方向、隣接分野を変える。次に何をするかは最新状態を渡した `continuation_gate.py` の `required_action` に従う。

各round開始前とcandidate投入前に `candidate_inventory` とactionable Research/Auditを再評価し、overflow条件を満たした時点でResearch modeへ切り替える。

## 探索空間のローテーション

同じ検索式を機械的に繰り返さず、次を独立経路として回す。

1. 新着・recent revision
2. 収録済み重要論文のforward citation
3. 重要論文のbackward reference
4. DBMS / OS / storage / distributed systems / HPC / GPU runtime / networking / memory systems等の隣接分野
5. 直近で採用されたcandidateのtitle / abstract / keywordからのquery expansion
6. offload / hierarchical memory / SSD/NVMe / MoE expert placement・cache・prefetch / KV cache / scheduling / disaggregation / inference framework等の重点テーマ

`discovery-state.json` を読み、採用実績のある軸を利用しつつ未探索軸も残す。少数sampleの0% / 100%だけで軸を恒久的に切らない。「現在思いつく未試行軸がない」という状態も終了許可ではなく、gateへ渡す観測値として扱う。

## Candidate quality and bounded transport

run全体のcandidate件数にquotaやhard capは設けない。件数維持のために品質基準を下げない。

Discoveryは軽量段階であり、title、abstract、書誌情報、一次資料の存在、重複状態、テーマ適合性、新規性の見込みを確認する。全文精読、詳細な科学的判断、5-slot structured record作成はResearch段階で行う。検索snippetやabstractだけからresearch内容を推測しない。

workflow-v10の現行queue contractでは **1 immutable discovery submissionは最大5 candidates** のbounded transportとする。これはrun全体の候補上限ではない。強いdedupe済みcandidateが5件を超える場合は捨てず、同じ `run_key` の複数immutable submissionへ5件以下ずつ分割してすべて耐久保存する。5件到達をround/run終了理由に使わない。

## Overflow research mode

`candidate_inventory > 50` かつactionable Research/Auditが存在する場合、探索主体workerは通常論文workerと同じResearch/Audit契約へ切り替える。

1. 最新queue / identity / claim stateを再取得する。
2. priority最上位のeligible Research/Auditを1件だけclaimする。
3. 一次資料全文を精読する。
4. claim resultで予約されたrecord bankへ5-slot structured research recordを書く。
5. 事前検査（preflight）後、attempt固有の不変提出（immutable submission）またはLibrary checkpointへ完全payloadを耐久保存する。
6. Actions terminal反映が次の判断に必要なら同じ対象を30秒間隔で再取得し、独立作業が可能なら同期障壁にしない。
7. 各耐久checkpoint後に最新状態とgateを再評価し、返されたactionに従う。
8. `candidate_inventory <= 50` またはactionable Research/AuditなしになったらDiscovery modeへ戻る。

完了件数に最低ノルマ・終了ノルマは置かない。1件、3件、それ以上という件数はthroughput指標にすぎず、run終了可否はgateが決める。1 workerが同時に保持する未完了claimは1件だけとする。探索主体workerのoverflow runも通常論文workerの24-run maintenance counterには加算しない。

## Durability and concurrency

candidate submission前には最新canonical identity / queue / job stateを再確認する。複数workerが同じ論文を発見してもcanonical ID / arXiv ID / DOI / OpenReview ID / normalized titleで1候補へ収束させる。

GitHub direct persistenceを優先し、GitHub write不能でもChatGPT Library `/LLM-survey-outbox/pending/` へ完全なseed / envelopeを耐久保存できるなら、その観測値をgateへ反映する。Google Drive、Notion、旧Library fallbackは現行経路ではない。

Discovery roundでは `discovery_stats` を送り、評価候補数、事前重複数、最終採用数、探索軸、query概要、next-axis hintをActions側で記録する。複数submissionへ分割した場合も同一run_keyで識別し、各payloadはqueue contract上の最大5 candidatesを守る。

## Run-level decision flow

毎回の耐久checkpoint後と最終応答前に次の順で処理する。

1. 実際のScheduled Chat invocation開始時刻から固定した `run_deadline = actual_start + 3600s` までの残り時間を再計算する。
2. 最新canonical state、assignment、pending claim/submission/ACK、transport可用性を再取得する。
3. 観測した値を `continuation_gate.py` に渡す。
4. `CONTINUE` なら `required_action` を実行する。worker独自の追加停止判定は挟まない。
5. `STOP_RUN` なら、その結果とassignment/pending状態を `run_finalization_gate.py` へ渡す。
6. `MUST_CONTINUE` なら `next_action` を実行する。`MAY_FINALIZE` かつpermit発行時だけ正常終了する。

外部プラットフォームがworkerを強制終了した場合は、その時点でworkerが正常なstop理由を生成する必要はない。次runが耐久状態から回復する。workerが事前に強制終了を予測して架空の `platform_limit` を報告することはしない。
