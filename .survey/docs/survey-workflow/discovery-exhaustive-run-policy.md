# Discovery exhaustive-run policy

この文書は毎時`:00` JSTの **探索主体Scheduled Chat worker** が1回の実行枠をどう使うかを定める。役割分離は `discovery-specialist-worker.md`、candidate水位とoverflow切替は `candidate-buffer-policy.md`、一般的な継続条件は `discovery-continuation-policy.md` を正本とする。

## 最重要原則

**5本は1 runの上限ではない。1探索軸・1 discovery submissionのcandidate送信上限である。**

ただし探索主体workerは常にdiscoveryだけを行うわけではない。各round開始前に `candidate_inventory` とactionable Research/Auditを確認し、**`candidate_inventory > 50` かつactionable Research/Auditがある場合はoverflow research modeへ切り替える。** この場合、探索ループを一時停止し、通常論文workerと同じ全文精読・5-slot structured record・不変提出（immutable submission）契約でbacklogを処理する。

candidate在庫が50以下へ戻るかactionable Research/AuditがなくなればDiscovery modeへ戻る。candidate在庫の多さはrun終了条件ではなくモード切替条件である。

## Discovery mode loop

Discovery modeでは次をループする。

1. 最新HEAD、identity、queue、existing jobs、`discovery-state.json`、candidate在庫を確認する。
2. `candidate_inventory > 50` かつactionable Research/AuditありならOverflow research modeへ移る。
3. 直近roundと重複しない探索軸を1つ選ぶ。
4. title、abstract、書誌情報、一次資料の存在、テーマ適合性だけを軽量評価する。Research modeではない間は全文精読・5-slot作成を行わない。
5. canonical ID / arXiv ID / DOI / OpenReview ID / normalized titleで重複除外する。
6. その軸から強いcandidateを最大5本だけ1 submissionとして送る。弱い候補で5本を埋めない。
7. `discovery_stats` にrun_key、round、axis、query summary、candidate数、重複数、next-axis hintを残す。
8. 最新stateを再取得し、overflow条件を満たせばResearch modeへ、満たさなければ別探索軸へ進む。

固定round数、固定総candidate数、固定submission数は設けない。

## Overflow research mode loop

Overflow research modeでは新規discoveryを一時停止し、次を繰り返す。

1. 最新queue / claim state / checkpointed jobを確認する。
2. eligibleなResearch/Auditをpriority順に1件だけclaimする。
3. 一次資料全文を取得・精読し、科学的判断を行う。
4. claim resultで予約されたrecord bankへ5 slotを書く。別bankを独自選択しない。
5. preflight後、attempt固有descriptorをGitHubへ保存するか、GitHub write不能なら完全payloadをChatGPT Libraryへcheckpointする。
6. 完全payloadが耐久保存された時点でActions terminal反映を待たず、最新stateを取得する。
7. `candidate_inventory > 50` かつactionable Research/Auditが残るなら次jobへ進む。
8. candidate在庫が50以下、またはactionable Research/AuditなしならDiscovery modeへ戻る。

1 workerが同時に保持する未完了claimは1件だけ。1本処理完了、bank枯渇、Actions待ちはrun停止理由ではない。

## GitHub Actions待ちのパイプライン

Discovery submission後、新しいdiscovery jobがActionsでmaterializeされるまで短い待ちが発生し得る。この待ちをrun終了理由にしない。別探索軸の検索・軽量評価を先行してよいが、次submission直前には最新HEAD / identity / queueを再取得して再dedupeする。

一方、overflow条件を満たした場合は次のdiscovery job materializationを待たずResearch modeへ切り替える。

## 探索空間の回し方

同じquery familyだけを反復せず、少なくとも次をローテーション候補にする。

1. 新着・recent revision
2. 収録済み重要論文のforward citation
3. 重要論文のbackward reference
4. DBMS / OS / storage / distributed systems / HPC / GPU runtime / networking / memory systems等の隣接分野
5. 直近で採用率が高かったcandidateからのquery expansion
6. offload / hierarchical memory / SSD/NVMe / MoE expert placement・cache・prefetch / KV cache / scheduling / disaggregation / inference framework等の重点テーマ

高重複・低採用率の軸は同一run内で機械的に反復しない。強いcandidateが見つかった軸は将来再利用してよいが、直後に同一検索式を繰り返さない。

## 「探索空間を使い切った」の判定

`reasonably exhausted` を安易な早期終了理由にしない。

Discovery modeで探索空間枯渇を理由にrunを終了してよいのは、最後に強いcandidateを得たround以降、現在利用可能で互いに独立な探索経路を一巡し、各経路で実質的に異なるaxis / query family / source方向を試し、それでも強い新規candidateが得られず、`discovery-state.json` のnext-axis hintにも有望な未試行方向が残っていない場合だけとする。

途中で強いcandidateを得た場合、枯渇判定用の一巡をリセットする。利用不能な探索経路は試行済みに数えず、理由を記録する。

candidate在庫が50を超えた場合は「探索空間を使い切った」と判定せず、overflow research modeへ切り替える。

## Run-level stop conditions

runを終了してよいのは次だけである。

1. 最新の正本・identity・queueを十分読めず、安全な重複判定やclaimができない。
2. GitHub directと承認済みLibrary fallbackの両方で必要な状態・成果を耐久保存できない。
3. hard platform/runtime/tool limitに達し、追加の有用作業を実行できない。
4. Discovery modeで上記の探索空間枯渇条件を満たし、overflow research modeへ移れるactionable Research/Auditもない。

以下は単独ではstop条件ではない。

- 1軸で0件
- 全候補が重複
- 低採用率
- 1 source/APIの失敗
- candidate inventoryが多い
- 1 submissionで5本送信した
- 1 discovery jobをcompletedにした
- Actionsの次job materialization待ち
- 1 Research/Auditを完了した

## Run終了時の記録

hard limitまたは探索空間枯渇で終了する場合、最後の`discovery_stats` / next-axis hintに、最後に成功した軸、成功後に試した独立経路、未試行の有望軸が残るかを可能な範囲で記録する。未試行の有望軸が残る、またはoverflow research modeで処理可能なjobが残るのに「枯渇」として終了してはならない。

探索主体workerのrunはDiscovery mode / Overflow research modeのどちらでも通常論文workerの24-run maintenance counterへ加算しない。
