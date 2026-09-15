# Discovery exhaustive-run policy

この文書は毎時`:00` JSTの **探索主体Scheduled Chat worker** が1回の実行枠をどう使うかを定める。役割分離は `discovery-specialist-worker.md`、candidate水位とoverflow切替は `candidate-buffer-policy.md`、一般的な継続条件は `discovery-continuation-policy.md` を正本とする。

## 次回Scheduled Chat枠への引き継ぎガード

探索主体workerは、同じScheduled Chatの次回`:00`実行と重ならないことを優先する。overflow research modeへ切り替わった場合も同じルールを使う。

- 新しいdiscovery round、新しい探索軸、新しいsubmission作成単位、または新しいResearch/Audit claimを開始する直前に、JSTで同じScheduled Chatの次回`:00`予定枠までの残り時間を確認する。
- 次回`:00`予定枠まで **600秒以下** なら新しい独立作業を開始しない。現在までの成果・観測値・次探索軸ヒントを耐久保存し、新しいclaimを発行せずrunを終了する。
- 次回`:00`予定枠まで **180秒以下** なら、未保存成果の耐久保存、既存claimの安全な着地、必要な継続情報の記録など最低限の終了処理だけを行う。
- この600秒ガードは、固定上限を設けないという通常の継続原則、overflow research modeの処理継続、探索空間を回し続ける規則より優先する。
- すでに進行中で未保存の作業を捨てるための規則ではない。まず安全な耐久保存地点まで進め、その後は次の独立作業を開始しない。
- `continuation_gate.py` を使う場合、同じScheduled Chatの次回`:00`予定枠までの秒数を `--seconds-to-next-scheduled-task` に渡す。既定ガードは600秒である。

## 最重要原則

**5本は1 runの上限ではない。1探索軸・1 discovery submissionのcandidate送信上限である。**

ただし探索主体workerは常にdiscoveryだけを行うわけではない。各round開始前に `candidate_inventory` とactionable Research/Auditを確認し、**`candidate_inventory > 50` かつactionable Research/Auditがある場合はoverflow research modeへ切り替える。** この場合、探索ループを一時停止し、通常論文workerと同じ全文精読・5-slot structured record・不変提出（immutable submission）契約でbacklogを処理する。

candidate在庫が50以下へ戻るかactionable Research/AuditがなくなればDiscovery modeへ戻る。candidate在庫の多さはrun終了条件ではなくモード切替条件である。

## Discovery mode loop

Discovery modeでは次をループする。

1. 最新HEAD、identity、queue、existing jobs、`discovery-state.json`、candidate在庫を確認する。
2. 次の独立作業を始める前に引き継ぎガードを評価する。ガード内なら耐久保存と終了処理を行って終了する。
3. `candidate_inventory > 50` かつactionable Research/AuditありならOverflow research modeへ移る。
4. 直近roundと重複しない探索軸を1つ選ぶ。
5. title、abstract、書誌情報、一次資料の存在、テーマ適合性だけを軽量評価する。Research modeではない間は全文精読・5-slot作成を行わない。
6. canonical ID / arXiv ID / DOI / OpenReview ID / normalized titleで重複除外する。
7. その軸から強いcandidateを最大5本だけ1 submissionとして送る。弱い候補で5本を埋めない。
8. `discovery_stats` にrun_key、round、axis、query summary、candidate数、重複数、next-axis hintを残す。
9. 最新stateを再取得し、overflow条件を満たせばResearch modeへ、満たさなければ引き継ぎガードを再評価して別探索軸へ進む。

固定round数、固定総candidate数、固定submission数は設けない。ただし同じScheduled Chatの次回`:00`予定枠まで600秒以下になった場合は引き継ぎガードを優先する。

## 耐久実行記録の不変条件

Discovery modeへ1回でも入った`:00` Scheduled Chat runは、**正常終了する前に、そのrunで固定した `run_key` を持つdiscovery submissionを少なくとも1件、正規の耐久経路へ保存しなければならない。** 探索を実行した事実だけ、候補0件という判断だけ、ローカルな一時状態だけを残して終了してはならない。

- GitHub write可能時は `.survey/work-queue/submissions/<unique-id>.json` へ通常のworkflow-v10 discovery submissionを直接保存する。
- 強い新規candidateが0件、全候補が重複、または最終dedupeで0件になった場合も `candidates: []` のsubmissionを保存し、`discovery_stats` に実際の `candidate_count`、`duplicate_filtered_count`、`duplicate_canonical_ids`、`next_axis_hint` と、具体的な非nullの `empty_round_reason` を残す。
- GitHub write可能なのに、`kind: discovery` の生payloadを `.survey/work-queue/fallback-inbox/` へ直接置いてはならない。generic fallbackを使う経路では `fallback-routing.md` と `fallback_transport.py` の完全な `writes[]` envelope契約に従い、通常のDiscovery fallbackは `fallback-routing.md` が指定するLibrary経路を優先する。
- run終了監査では、今回の `run_key` を持つ正規submissionまたは承認済みLibrary fallbackが実際に耐久保存されていることを再確認する。見つからなければ、候補0件でも空submissionを作成してから終了する。
- GitHub directと承認済みLibrary fallbackの両方へ保存できない場合だけ、下記Run-level stop condition 3として異常終了してよい。正常終了扱いにはしない。
- run開始直後から最後までoverflow research modeだけで、Discovery modeへ一度も入らなかった場合は空discovery submissionを作る必要はない。その場合はResearch/Auditの完全payloadの耐久保存をそのrunの成果証跡とする。

これにより、各通常Discovery runは候補採用数にかかわらず `run_key` 単位で観測可能になり、`STATUS.md` / `discovery-state.json` が「探索したが0件」と「探索runの耐久記録が欠落した」を区別できる。

## Overflow research mode loop

Overflow research modeでは新規discoveryを一時停止し、次を繰り返す。

1. 最新queue / claim state / checkpointed jobを確認する。
2. 次のResearch/Auditをclaimする前に引き継ぎガードを評価する。ガード内なら新しいclaimを出さず終了処理へ進む。
3. eligibleなResearch/Auditをpriority順に1件だけclaimする。
4. 一次資料全文を取得・精読し、科学的判断を行う。
5. claim resultで予約されたrecord bankへ5 slotを書く。別bankを独自選択しない。
6. preflight後、attempt固有descriptorをGitHubへ保存するか、GitHub write不能なら完全payloadをChatGPT Libraryへcheckpointする。
7. 完全payloadが耐久保存された時点でActions terminal反映を待たず、最新stateを取得する。
8. 引き継ぎガード外で `candidate_inventory > 50` かつactionable Research/Auditが残るなら次jobへ進む。
9. candidate在庫が50以下、またはactionable Research/AuditなしならDiscovery modeへ戻る。

1 workerが同時に保持する未完了claimは1件だけ。1本処理完了、bank枯渇、Actions待ちはrun停止理由ではない。ただし引き継ぎガード成立時は新しいclaimを発行せず終了する。

## GitHub Actions待ちのパイプライン

Discovery submission後、新しいdiscovery jobがActionsでmaterializeされるまで短い待ちが発生し得る。この待ちをrun終了理由にしない。別探索軸の検索・軽量評価を先行してよいが、次submission直前には最新HEAD / identity / queueを再取得して再dedupeする。ただし同じScheduled Chatの次回`:00`予定枠まで600秒以下なら別探索軸を新しく開始せず、引き継ぎガードに従って終了する。

一方、overflow条件を満たした場合は次のdiscovery job materializationを待たずResearch modeへ切り替える。ただし新しいResearch/Audit claimの直前にも引き継ぎガードを評価する。

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

引き継ぎガードによる終了は探索空間枯渇とは別理由であり、有望な未試行軸が残っていてもよい。その場合はnext-axis hintへ残し、次runで再開する。

## Run-level stop conditions

runを終了してよいのは次だけである。

1. 同じ探索Scheduled Chatの次回`:00`予定枠まで600秒以下となり、引き継ぎガードが成立した。
2. 最新の正本・identity・queueを十分読めず、安全な重複判定やclaimができない。
3. GitHub directと承認済みLibrary fallbackの両方で必要な状態・成果を耐久保存できない。
4. hard platform/runtime/tool limitに達し、追加の有用作業を実行できない。
5. Discovery modeで上記の探索空間枯渇条件を満たし、overflow research modeへ移れるactionable Research/Auditもない。

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

hard limit、探索空間枯渇、または引き継ぎガードで終了する場合、最後の`discovery_stats` / next-axis hintに、最後に成功した軸、成功後に試した独立経路、未試行の有望軸が残るかを可能な範囲で記録する。引き継ぎガード以外の理由で、未試行の有望軸が残る、またはoverflow research modeで処理可能なjobが残るのに「枯渇」として終了してはならない。

探索主体workerのrunはDiscovery mode / Overflow research modeのどちらでも通常論文workerの24-run maintenance counterへ加算しない。
