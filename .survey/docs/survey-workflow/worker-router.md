# Chat worker router — workflow v10

このrouterはScheduled Chat / Work系workerの最上位routing正本とする。毎回default branch最新HEADを取得し、同じHEADの `README.md`、`queue-v10.md`、`candidate-buffer-policy.md`、`claim-serial-policy.md`、`continuation-policy.json`、`run-liveness-policy.md`、`fallback-routing.md`、`backlog-resilience.md`、`suggestion-box.md` と必要なqueue/state/job/identity正本を読む。

通常論文workerは毎時`:30`、探索主体workerは毎時`:00`に動く。探索主体workerは通常Discoveryを担当するが、`candidate_inventory > 50` かつactionable Research/Auditがある場合は **overflow research mode** へ切り替え、追加readerとしてResearch/Audit backlogを処理する。

Google Drive fallback、Notion、旧 `/LLM-survey-fallback/` は現行transportではない。外部fallbackはChatGPT Library `/LLM-survey-outbox/pending/` とする。

## 0. 時刻routingとmaintenance gate

通常論文workerでは `.survey/work-queue/maintenance-cycle.json` を確認する。

- 24回目のcounted run → maintenance専用run
- 08:30 JST → その他更新worker
- それ以外の毎時`:30` → 通常論文worker
- 毎時`:00` → 探索主体worker

探索主体workerはDiscovery mode / overflow research modeのどちらでも通常workerの24-run maintenance counterへ加算しない。

maintenance runは専用契約に従い、Research/Audit/Discoveryと混在させない。08:30 update workerも専用契約に従う。以下のtime-only livenessは通常`:00`/`:30` paper worker runを対象とする。

## 1. 通常runのliveness

通常paper workerはScheduled Chat invocationの実開始時刻を1回固定し、`run_deadline = actual_invocation_start + 3600 seconds` とする。新しい独立作業を始める直前と各耐久保存後に `seconds_to_run_deadline` を再計算する。

- `seconds_to_run_deadline > 600`: 件数・在庫・探索枯渇を理由に正常終了せず、次の独立作業へ進む。
- `seconds_to_run_deadline <= 600`: 新しい独立作業を始めず、成果とclaimを安全に耐久handoffし、continuation/finalization gateを評価する。
- `seconds_to_run_deadline <= 180`: finalizationに必要な最低限の耐久着地だけを行う。

正常runの `STOP_RUN` / finalizationを許可するのはrun-local handoff guardだけである。candidate数、Discovery round数、submission数、Research/Audit完了数、candidate inventory、空round、全重複、探索枯渇、Actions待ちは正常終了理由にしない。

canonical read不能、GitHub/Library双方のdurability failure、tool/platform異常等は **異常blocker** として扱う。回復可能なら回復し、回復不能でもnormal successのfinalization理由へ変換しない。外部platformがinvocationを強制終了した場合は、次runがcanonical stateから回復する。

normal final responseは `run_finalization_gate.py` が `MAY_FINALIZE` かつ `finalization_permit.issued=true` を返した場合だけ許可する。

## 2. Run開始時の回復

最新queue / identityに加えて、必要な範囲で次を確認する。

- ChatGPT Library `/LLM-survey-outbox/pending/`
- `.survey/work-queue/fallback-inbox/*.json`
- `.survey/work-queue/fallback-archive/*.json`
- active claim / claim result
- immutable Research/Audit descriptor / result
- Library ACK manifest

完全payloadが既にGitHubまたはLibraryへ耐久保存済みのjobを同じrunで再精読しない。pending orphanは既存payloadのvalidation/replay/recoveryを優先する。

## 3. GitHub write failure

対象writeが失敗した場合は、最新SHA/stateを取得してその対象だけ1回再試行し、必要ならcanonical health probeでtarget-specificかrun-wideかを分類する。

GitHub write不能でもLibraryへ完全payloadを耐久保存できるなら独立作業を継続する。GitHub directとLibrary fallbackの双方で必要な状態を保存できない場合は異常blockerとして成果を増やさず、normal success finalizationとは扱わない。

## 4. 通常論文worker（毎時:30）

candidate水位は処理モードの選択に使う。

- `candidate_inventory > 50`: actionable Research/Auditがある間はhigh-backlog research-only。
- 25〜50: actionable Research/Auditを優先する。
- 15〜24: Researchを進めながらDiscovery補充を積極化する。
- 0〜14: Discovery補充の比重を上げる。
- actionable Research/Auditがない: Discoveryへ進む。

通常workerのDiscovery機能は探索主体workerの存在を理由に削除しない。

### Research / Audit loop

1. 最新queue / checkpointed stateを取得する。
2. actionable readyをpriority順に1件claimする。同一workerが保持する未完了claimは1件だけ。
3. claim resultの `record_bank` / `record_bank_fallback` を正本とする。
4. 一次資料本文を最後まで読み、5-slot structured research recordを作る。
5. validator基準でpreflightする。
6. immutable descriptorまたはLibrary checkpointへ完全payloadを耐久保存する。
7. Actions terminal反映を同期障壁にせず、最新stateとrun deadlineを再取得する。
8. handoff guard外なら次のactionable workへ進む。

「1件」「3件」等の最低処理件数や完了件数停止条件は設けない。

## 5. Discovery

Discoveryはtitle、abstract、書誌、一次資料の存在、identity重複、テーマ適合性、新規性見込みを軽量評価する。全文精読と5-slot作成はResearch段階で行う。

探索開始前とcandidate投入直前に最新HEAD / identity / queueを再確認し、canonical ID / arXiv ID / DOI / OpenReview ID / normalized titleで重複除外する。

**Discovery candidate配列にアプリケーション上の固定件数上限を設けない。** 1 roundで強いcandidateが12件、50件、100件得られた場合も、重複除外後の候補をすべて保存する。弱いcandidateで件数を埋めず、固定5件等へ強いcandidateを切り捨てない。

外部transportの実payloadサイズ制約で単一submissionが保存不能な場合だけ複数immutable submissionへ分割し、総candidateを失わない。

1探索軸が0件、全重複、低採用、または枯渇しても正常終了せず、handoff guard外では検索語、source、引用方向、関連実装、隣接分野等から次軸を生成する。

`discovery-state.json` はGitHub Actionsを単一writerとし、Scheduled Chatは各submissionへ `discovery_stats` を添付する。

## 6. 探索主体worker（毎時:00）

正本は `discovery-specialist-worker.md`、`candidate-buffer-policy.md`、`discovery-continuation-policy.md`、`discovery-exhaustive-run-policy.md`。

- `candidate_inventory <= 50` またはactionable Research/Auditなし → Discovery mode。
- `candidate_inventory > 50` かつactionable Research/Auditあり → **overflow research mode**。

Discovery modeでは最低4 round等のroundノルマを設けない。round数が0、1、4、100でもnormal finalization可否は変わらず、handoff guard外なら次の探索軸を生成して続ける。

overflow research modeでは通常論文workerと同じclaim / full-text / 5-slot / preflight / immutable descriptorまたはLibrary checkpoint契約を使う。最低3件等のResearch件数ノルマは設けない。50以下へ戻るかactionable Research/Auditが尽きたらDiscovery modeへ戻る。

## 7. GitHub write不能中のoffline Discovery / Research

GitHub writeがrun-wideで停止してもLibraryへ保存可能なら停止しない。

Discovery mode:

1. identity、既存jobs、Library pending、GitHub fallbackと重複確認する。
2. 強いcandidateを **固定件数上限なし** で選ぶ。
3. offline seed envelopeをLibraryへ完全保存する。
4. seedのGitHub materializationを同期的に待たず、必要なら同runでcandidateをResearchへ進める。
5. 完成Research fallbackはroot-level identity + 完全5 slotを1 envelopeへ保存する。

Library/APIの実payload上限に当たる場合は複数seed envelopeへ分割してよいが、candidateを切り捨てない。

overflow research modeでは既存priority上位Research/Auditの完全payloadをLibraryへcheckpointする。

## 8. Record bankと品質

通常Research/Auditではclaim resultの予約bankが正本であり、`select_record_bank.py` は診断・maintenance・fallback replay用途とする。

record bank枯渇はrun終了理由ではない。Libraryへ完全payloadを保存できれば継続する。structured recordはrendererが後で内容を補う前提で短縮せず `.survey/templates/paper.md` の品質基準を満たす。

## 9. 非同期結果待機

次判断に特定結果が必要な場合は、request_id / attempt_id / envelope_id等を固定し、**30秒待機 → 最新canonical state取得 → 同じ対象再取得**を繰り返す。pending中に別identityで重複投入しない。

専門正本が結果を待たず独立作業へ進めると定める場合は30秒待機を同期障壁にせず、その作業を先に進める。待機は結果が出るかrun-local handoff guardへ入るまで行う。非時間failureはrecovery対象でありnormal finalization理由ではない。

## 10. その他更新worker（08:30専用）

08:30はframework / LLM release更新workerの専用routeとする。論文queue処理とは分離し、最新mainに定義されたupdate transportと報告契約に従う。

## 11. Maintenance

maintenance runは `.survey/work-queue/maintenance-cycle.json` と `.github/workflows/maintenance.yml` を正本とし、GC、derived view再構築、品質監査、metadata coverage、health、repository-wide consistency等を専用runで実施する。通常Research/Audit/Discoveryを同じmaintenance runへ混在させない。

## 12. 改善知見

maintenance以外のworkerは、実作業中に具体的な摩擦・重複・失敗・復旧コスト・品質低下リスクを観測し、実行可能な改善案がある場合だけ `suggestion-box.md` の契約に従って記録する。改善案作成そのものをrun終了理由にしない。
