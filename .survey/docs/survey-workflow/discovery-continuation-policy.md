# Discovery continuation policy

この文書は通常論文workerと毎時`:00` JSTの探索主体workerが、探索（discovery）をいつ継続し、いつ研究消化へ切り替えるかを定める。candidate水位とモード切替の正本は `candidate-buffer-policy.md`、探索主体worker固有の動作は `discovery-specialist-worker.md` とする。

## 基本原則

探索は、有望な候補を供給できる限り1回の空振りや重複だけで終了しない。ただし **candidate在庫が十分に積み上がった場合は探索を続けること自体が目的ではない。** `candidate_inventory > 50` かつactionable Research/Auditがある場合、探索主体workerはoverflow research modeへ切り替え、discoveryを一時停止して追加readerとしてbacklog消化に加勢する。

candidate在庫が50以下へ戻る、またはactionable Research/Auditがなくなった場合は、探索主体workerは通常探索モードへ戻る。candidate在庫の多さはrun終了条件ではなく、**discoveryからresearchへのモード切替条件**である。

## Discovery modeでの非停止条件

通常探索モード中、次のいずれも単独ではrun終了条件ではない。

- 1探索軸で有力候補が0件だった。
- 1探索軸の候補が全て重複だった。
- 1探索軸の採用率が低い、または重複率が高い。
- 1 source / API / queryが失敗した。
- 1候補の全文取得や証拠が不足していた。
- 1候補を弱い・対象外として見送った。
- 1回のGitHub writeが競合した。
- 1回のfallback保存・replayが失敗したが別の耐久経路が残っている。
- 1 discovery submissionが候補上限5本に達した。

この場合は有用な状態を保存し、探索軸、query family、source、引用方向、隣接分野を変えて継続する。

ただし各round開始前とcandidate投入前に `candidate_inventory` とactionable Research/Auditを再評価し、overflow条件を満たした時点で探索ループを中断してResearch modeへ切り替える。

## 探索空間のローテーション

同じ検索式を機械的に繰り返さず、次を独立経路として回す。

1. 新着・recent revision
2. 収録済み重要論文のforward citation
3. 重要論文のbackward reference
4. DBMS / OS / storage / distributed systems / HPC / GPU runtime / networking / memory systems等の隣接分野
5. 直近で採用されたcandidateのtitle / abstract / keywordからのquery expansion
6. offload / hierarchical memory / SSD/NVMe / MoE expert placement・cache・prefetch / KV cache / scheduling / disaggregation / inference framework等の重点テーマ

`discovery-state.json` を読み、採用実績のある軸を利用しつつ未探索軸も残す。少数sampleの0% / 100%だけで軸を恒久的に切らない。

## Candidate quality

候補件数のquotaやhard capは設けない。件数維持のために品質基準を下げない。

Discoveryは軽量段階であり、title、abstract、書誌情報、一次資料の存在、重複状態、テーマ適合性、新規性の見込みを確認する。全文精読、詳細な科学的判断、5-slot structured record作成はResearch段階で行う。検索snippetやabstractだけからresearch内容を推測しない。

## Overflow research mode

`candidate_inventory > 50` かつactionable Research/Auditが存在する場合、探索主体workerは通常論文workerと同じResearch/Audit契約へ切り替える。

1. 最新queue / identity / claim stateを再取得する。
2. priority最上位のeligible Research/Auditを1件だけclaimする。
3. 一次資料全文を精読する。
4. claim resultで予約されたrecord bankへ5-slot structured research recordを書く。
5. 事前検査（preflight）後、attempt固有の不変提出（immutable submission）またはLibrary checkpointへ完全payloadを耐久保存する。
6. Actions terminal反映を同期的に待たず最新状態を取り直し、overflow条件が続く限り次の独立jobを処理する。
7. `candidate_inventory <= 50` またはactionable Research/AuditなしになったらDiscovery modeへ戻る。

1 workerが同時に保持する未完了claimは1件だけとする。探索主体workerのoverflow runも通常論文workerの24-run maintenance counterには加算しない。

## Durability and concurrency

candidate submission前には最新canonical identity / queue / job stateを再確認する。複数workerが同じ論文を発見してもcanonical ID / arXiv ID / DOI / OpenReview ID / normalized titleで1候補へ収束させる。

GitHub direct persistenceを優先し、GitHub write不能でもChatGPT Library `/LLM-survey-outbox/pending/` へ完全なseed / envelopeを耐久保存できるなら継続する。Google Drive、Notion、旧Library fallbackは現行経路ではない。

Discovery roundでは `discovery_stats` を送り、評価候補数、事前重複数、最終採用数、探索軸、query概要、next-axis hintをActions側で記録する。

## Run-level stop conditions

runを終了してよいのは次の場合だけである。

1. canonical repository / rulesを十分読めず、安全な重複判定やclaimができない。
2. GitHubと承認済みLibrary fallbackの両方で必要な状態・成果を耐久保存できない。
3. 実行環境のhard platform/runtime/tool limitに達し、追加の有用作業ができない。
4. Discovery modeで、利用可能な互いに独立した探索軸を合理的に使い切り、未試行の有望軸も残っていない。
5. Overflow research modeでactionable Research/Auditが尽き、Discovery modeへ戻っても条件4を満たす。

単一の空round、全重複round、大きなcandidate在庫、単一source障害はrun停止条件ではない。大きなcandidate在庫はoverflow research modeへの切替理由として扱う。
