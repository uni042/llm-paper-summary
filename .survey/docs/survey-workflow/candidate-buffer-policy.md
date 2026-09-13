# Candidate buffer policy

この文書は論文survey workerの **candidate供給・discovery水位制御** の正本とする。既存の `queue-v10.md` にある「actionable readyが尽きたらdiscovery」という受動的な記述より、本書の水位制御を優先する。research品質、transport、fallback、maintenance、08:30 routing等は従来の正本に従う。

探索ラウンドの継続・停止判断は `.survey/docs/survey-workflow/discovery-continuation-policy.md` を正本とし、通常論文worker（毎時:30）と探索主体worker（毎時:00）は毎run本書と併読する。0件、全重複、低採用率、単一sourceの一時障害だけを理由にdiscoveryを停止せず、同ポリシーに従って探索軸・source・query familyを切り替える。ただし `candidate_inventory > 50` かつactionable researchがある場合、探索主体workerはoverflow research modeへ切り替え、discoveryよりbacklog消化を優先する。

## 目的

research workerが候補枯渇で停止しないよう、discoveryをresearch開始の前処理ではなく独立した在庫補充工程として扱う。弱い論文で件数を埋めず、有望候補を先に広く集め、researchはその候補群から優先度順に全文精読する。同時に、候補供給が消化速度を大きく上回った場合は探索workerの計算資源を追加readerへ転用し、backlogを無制限に積み増さない。

## 水位

重複排除後の未処理research候補を `candidate_inventory` とする。

- `low_watermark = 25`
- `critical_watermark = 15`
- `overflow_research_threshold = 50`。切替条件は **`candidate_inventory > 50`**。

25本以上の候補がある状態は、通常論文workerがresearchへ十分に注力できる在庫水準とみなす。25本未満になった時点でdiscovery補充をresearchと並行して加速し、15本未満では候補枯渇防止を優先してdiscovery比重をさらに上げる。0本になるまで待ってから探索を始めてはならない。

`candidate_inventory` にhard capは設けない。ただし50本を超え、かつ処理可能なresearch jobがある間は、毎時`:00`の探索主体workerもoverflow research modeへ入り、通常論文workerと同じhigh-backlog research-only動作で全文精読に加勢する。50以下へ戻るかactionable researchが尽きたら、`:00` workerは通常探索モードへ戻る。件数維持のために弱い候補を採用しない。

`candidate_inventory` はGitHub queueの未処理research候補、Library/GitHub fallback由来の未checkpoint spillover、candidate pool相当の未処理候補をcanonical ID / arXiv ID / DOI / normalized titleで重複排除して数える。blocked/deferredで現在research不能な論文は通常在庫に含めない。

## DiscoveryとResearchの分離

Discovery段階では原則として全文精読しない。タイトル、abstract、書誌情報、一次資料の存在、既収録identityとの重複、テーマ適合性、新規性の見込みを軽量評価し、「全文を読む価値がある候補」をcandidate poolへ積む。

Research段階で初めて一次資料全文を取得・精読し、repository-qualityの5-slot structured recordを作る。Discoveryで得たabstractや検索snippetだけからresearch内容を推測しない。

この分離により、1回のdiscoveryで1本だけ見つけて即researchする方式に固定せず、先に複数候補を蓄積できる。overflow research modeはこの段階分離を崩さず、探索主体workerの役割そのものをrun単位でResearchへ切り替える。

## 複数worker協調

candidate供給とresearch消化は2つのScheduled Chat workerが共有する。

1. **通常論文worker（毎時:30）**: research / auditを主担当とする。candidate在庫が25本未満、またはactionable researchが尽きた場合にdiscoveryも行う。25本以上かつactionable researchありの間はdiscoveryを行わない。
2. **探索主体worker（毎時:00）**: `candidate_inventory <= 50` またはactionable researchなしならdiscovery、軽量候補評価、priority付与、candidate投入を行う。`candidate_inventory > 50` かつactionable researchありなら **overflow research mode** に切り替え、通常論文workerと同じresearch / audit処理へ加勢する。

両workerがresearchを行う場合、それぞれ固有の `worker_id` を使う。各worker内では未完了claimは1件だけだが、異なるworkerが別jobを同時にclaim・精読することは許可する。record bank予約と同一job排他はclaim-fastの直列化された割当に任せ、worker側でpriority上位jobをまとめて先取りしない。

通常論文workerはcandidate在庫が25本以上あり、処理可能なresearch jobが存在する場合、high-backlog research-only modeとして新規discovery・低コスト新着確認・candidate投入を停止する。探索主体workerも50超では同じ動作を行う。探索主体workerの存在を理由に通常論文workerのdiscovery機能自体は削除せず、在庫が25本未満になった場合やactionable researchが尽きた場合に再度有効化する。

二重投入を防ぐため、discoveryを行うworkerは探索開始前とcandidate投入直前に最新HEADを再確認し、canonical ID / arXiv ID / DOI / OpenReview ID / normalized titleで再重複判定する。片方が探索中にもう片方やActionsが同じ候補を先に登録した場合、後発workerはその候補を送らない。競合が残る場合も正本側のdedupeで1候補へ収束させる。

`discovery-state.json` はGitHub Actionsを単一writerとする。Scheduled Chatはこの共有stateを直接更新せず、各discovery submissionへトップレベル `discovery_stats` を添付する。Actionsは直列化されたqueue処理の中で最終dedupe後の実採用数を確定してから、探索軸ごとの統計を1回だけ加算する。同一submission pathは二重計上しない。

`discovery_stats` には少なくとも `run_key`, `round`, `axis`, `query_summary`, `candidate_count`, `duplicate_filtered_count`, `duplicate_canonical_ids`, `next_axis_hint` を含める。`candidate_count` は検索エンジンの生hit数ではなく、テーマ適合性を確認して実質的に評価した候補数とする。`candidates` 本体にはScheduled Chat側の重複除外後にActionsへ渡す候補だけを入れる。実際の `accepted_count` はActions側の最終dedupe結果から算出する。

探索主体workerの毎時runは、overflow research modeへ切り替わった場合も通常論文workerの24-run maintenance counterへ加算しない。詳細契約は `discovery-specialist-worker.md` を正本とする。

## 探索経路

在庫補充では同じ検索語を反復せず、以下を独立した探索経路として組み合わせる。

1. **新着探索**: arXiv、OpenReview、会議等から重点テーマの新規論文を広めに拾う。
2. **被引用探索**: 収録済み重要論文を引用する新しい論文を追う。
3. **参考文献探索**: 重要論文のreferenceから未収録の基礎・過去研究を拾う。
4. **隣接分野探索**: DBMS、OS、storage、distributed systems、HPC、GPU runtime、networking等からLLM serving / inferenceへ接続する研究を探す。
5. **検索語自動拡張**: 直近で採用率が高かった候補のtitle / abstract / keywordから新しい検索語を抽出し、次の探索軸に使う。
6. **既存の重点テーマ探索**: offload / hierarchical memory / MoE / expert placement・cache・prefetch / KV cache / scheduling / disaggregation / inference framework等を継続する。

探索ラウンドごとに、取得候補数、重複除外数、新規候補数、candidate採用数、採用率、探索軸を記録する。高重複・低採用率の軸は直後に繰り返さず、別経路へ切り替える。採用率の高い探索語・探索経路は次回の候補生成へ再利用する。

統計の意味は以下で固定する。

- `candidate_count`: 軽量評価後に実質的な候補として検討した件数。
- `duplicate_filtered_count`: Scheduled Chat側のidentity/queue再確認で既存と判定し除外した件数。
- `novel_candidate_count`: `candidate_count - duplicate_filtered_count`。
- `accepted_count`: Actionsの最終dedupeを通過してresearch job化された件数。
- `duplicate_ratio`: `duplicate_filtered_count / candidate_count`。candidateが0なら0。

したがって、Scheduled Chat側で新規に見えても投入までの間に他workerが同じ論文を登録した場合、`novel_candidate_count` と `accepted_count` は異なり得る。この差は並行探索時の競合として正常であり、採用数をScheduled Chat側で推測して補正しない。

## 優先順位

candidateにはresearch priorityを付ける。少なくとも以下を考慮する。

- repoの重点テーマとの関連度
- 手法・システムとしての新規性
- 既存収録論文との差分
- 実測評価・実装公開の有無
- SSD/NVMe、MoE、階層メモリ、serving基盤等への研究価値
- 新しさだけでなく、重要な基礎研究・引用関係上の価値

research workerは原則としてpriorityの高い候補から処理する。candidate poolが大きくなった場合もFIFOだけで消化しない。

## Run内の制御

maintenance runと08:30 other-update runを除くpaper workerでは、run開始時とjob処理後にcandidate_inventoryを再評価する。

- `candidate_inventory > 50`: actionable researchがある間、通常論文workerと探索主体workerの双方をhigh-backlog research-only modeにする。両者は固有worker IDで別jobをclaimし、全文精読・structured record作成・必要なauditに専念する。
- 25〜50: 通常論文workerはactionable researchがある間research-only。探索主体workerはdiscoveryを継続して高価値候補を供給する。
- 15〜24: 通常論文workerはresearchを継続しながらdiscovery補充を積極化する。探索主体workerもdiscoveryを行う。
- 0〜14: discovery補充を優先し、複数の探索経路を使って在庫回復を図る。見つかった高priority候補のresearchを通常論文workerが同一runで進めてもよい。

high-backlog research-only mode中は、一次資料取得と耐久保存経路が利用可能でactionable researchが十分ある限り、researchを担当する各workerは1runにつき最低3件の異なるresearch jobを完全payloadとして送信または耐久checkpointすることを処理量の下限目標とする。3件は上限でも停止条件でもなく、3件後も処理可能なら継続する。platform limit、正本read不能、耐久保存不能、一次資料取得不能、claim不能等のhard conditionはこの目標より優先する。

固定上限件数・固定batch数は設けない。候補が0件の探索ラウンドがあっても別軸へ切り替える。プラットフォーム上限、耐久保存不能、または合理的に有望探索軸を使い切った場合のみそのrunのdiscoveryを終了する。

## GitHub write不能時

GitHub write不能でもLibrary `/LLM-survey-outbox/pending/` へ保存可能ならworkerを止めない。high-backlog research-only / overflow research modeでは新規candidate seedを作らず、priority上位researchの完成payloadをLibraryへcheckpointする。candidate在庫が50以下で探索主体workerが通常探索モードの場合、または通常論文worker側でdiscoveryが許可される場合はcandidate seedを保存する。transport envelope、job ID、replayは `fallback-routing.md` と `continuation-policy.json` を正本とする。

fallback envelopeにも探索時点の `discovery_stats` を保持し、GitHub復旧後のreplayでActionsが通常submissionと同じ統計処理を行えるようにする。overflow research modeの探索主体workerは通常論文workerと同じresearch fallback契約を使う。

## 08:30 reporting

08:30 JSTの報告では従来どおり「直近24時間の発見数・追加数・残候補数」を示す。在庫がlow watermark未満ならその旨を短く示す。target inventoryは設けないため、`candidate_inventory / target_inventory` の比率表示は行わない。集計できない場合は推測値で埋めない。

Claims do not change candidate-buffer or discovery visibility. They hide only
actively claimed ready research/audit jobs from `next-jobs.json`; discovery stays
visible under the existing priority-window policy.
