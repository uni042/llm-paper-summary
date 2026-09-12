# Discovery exhaustive-run policy

この文書は、毎時 `:00` JST の **探索専用Scheduled Chat worker** が1回の実行枠をどこまで使って探索を継続するかを定める実行契約である。役割分離は `discovery-specialist-worker.md`、candidate水位は `candidate-buffer-policy.md`、一般的な継続条件は `discovery-continuation-policy.md` を正本とし、本書は探索専用workerの run 内ループをより具体化する。

## 最重要原則

**5本は1 run の上限ではない。1探索軸・1 discovery submission のcandidate送信上限である。**

1つの探索軸で最大5本の強い候補を送信したら、その時点でScheduled Chat runを終了せず、別の探索軸へ移って次のroundを続ける。候補が5本未満でも、その軸で追加の強候補が見込めないなら無理に埋めず、次の軸へ移る。

探索専用workerには固定のround数、固定の総candidate数、固定のsubmission数を設けない。プラットフォーム上限等のrun-level stop条件に達するまで、強い候補を探せる限り探索を続ける。

## Mandatory run loop

探索専用workerは以下を1回だけではなくループとして実行する。

1. 最新HEAD、identity、queue、existing jobs、`discovery-state.json` を確認する。
2. 直近roundと重複しない探索軸を1つ選ぶ。
3. Discoveryの軽量評価だけで候補を集める。全文精読・researchは行わない。
4. canonical ID / arXiv ID / DOI / OpenReview ID / normalized titleで重複除外する。
5. その軸から強いcandidateを **最大5本** だけ1 submissionとして送る。弱い候補で5本を埋めない。
6. `discovery_stats` にrun_key、round、axis、query summary、candidate数、重複数、next-axis hintを残す。
7. submissionが5本に達したこと、candidateを1本以上送れたこと、candidate inventoryが50以上になったことをrun終了理由にしない。
8. 次の探索軸へ直ちに移り、2へ戻る。

## GitHub Actions待ちのパイプライン

queueは重複競合を抑えるためactive discovery jobを原則1件に直列化している。そのため、前roundのsubmission後、新しいdiscovery jobがActionsでmaterializeされるまで短い待ちが発生し得る。

この待ち時間を探索停止・run終了・アイドル待機に使わない。前roundのsubmissionを送ったら、Actions処理と並行して次の探索軸の検索・軽量candidate評価を進める。次のcandidate batchを送る直前に最新HEAD / identity / queue / next discovery jobを再取得し、競合で既存化した候補を除外してから送信する。

次のjobがまだmaterializeされていない場合も、別軸の探索自体は先行してよい。jobが利用可能になり次第、最新状態で再dedupeしてsubmissionする。

## 探索空間の回し方

1つのquery familyだけを深掘りして終了しない。少なくとも次の独立経路をローテーション候補として扱う。

1. 新着・recent revision
2. 収録済み重要論文のforward citation
3. 重要論文のbackward reference
4. DBMS / OS / storage / distributed systems / HPC / GPU runtime / networking / memory systems等の隣接分野
5. 直近で採用率が高かったcandidateからのquery expansion
6. offload / hierarchical memory / SSD/NVMe / MoE expert placement・cache・prefetch / KV cache / scheduling / disaggregation / inference framework等の重点テーマ

高重複・低採用率の軸は同一run内で機械的に反復せず、別経路へ切り替える。強い候補が見つかった軸は将来再利用してよいが、同じ検索式を直後にそのまま再実行しない。

## 「探索空間を使い切った」の判定

`reasonably exhausted` を安易な早期終了理由にしない。

探索空間枯渇を理由にrunを終了してよいのは、**最後に強いcandidateを得たround以降**、現在利用可能で互いに独立な探索経路を一巡し、各経路で少なくとも1つは実質的に異なるaxis / query family / source方向を試し、それでも強い新規candidateが得られず、`discovery-state.json` のnext-axis hintにも有望な未試行方向が残っていない場合だけとする。

途中で1本でも強いcandidateを得た場合、枯渇判定用の一巡はリセットし、新たなcandidateや用語から探索空間を再展開する。

利用不能な探索経路がある場合は、それを試したことにせず、source/API/tool unavailable等の理由を記録する。他の利用可能経路が残っていれば探索を続ける。

## Run-level stop conditions

探索専用runを終了してよいのは次だけである。

1. 最新の正本・identity・queueを十分読めず、安全な重複判定ができない。
2. GitHub directと承認済みLibrary fallbackの両方でcandidate状態を耐久保存できない。
3. 実行環境のhard platform/runtime/tool limitに達し、追加の有用作業を実行できない。
4. 上記の「探索空間を使い切った」の条件を満たした。

以下は単独ではstop条件ではない。

- 1軸で0件
- 全候補が重複
- 低採用率
- 1 source/APIの失敗
- candidate inventoryが50以上
- 1 submissionで5本送信した
- 1 discovery jobをcompletedにした
- Actionsの次job materialization待ち

## Run終了時の記録

hard limitまたは探索空間枯渇で終了する場合、可能な範囲で最後の`discovery_stats` / next-axis hintに、最後に成功した軸、成功後に試した独立経路、未試行だが有望な軸が残っているかを反映する。未試行の有望軸が残っているのに「枯渇」として終了してはならない。
