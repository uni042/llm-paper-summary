# Discovery specialist worker

この文書は、既存の論文workerとは別に毎時`:00` JSTで実行する **探索専用Scheduled Chat workerの役割分離** の正本とする。目的はcandidate在庫を継続的に積み上げることであり、既存の論文workerからdiscovery責務を取り上げない。

## 1. 役割

- **探索専用worker**: discovery、軽量重複判定、候補評価、priority付与、candidate投入だけを担当する。
- **通常論文worker**: research / audit / discoveryを引き続き担当する。
- **GitHub Actions**: queue/state/identityの最終整合、重複抑止、job materialization、`discovery-state.json` の単一writerを担当する。

探索専用workerはresearch、audit、全文精読、5-slot structured research record作成、論文Markdown生成を行わない。候補を安全にcandidate poolへ投入したら次の探索軸へ進む。

## 2. 実行時刻とmaintenance

探索専用workerは毎時`:00` JST、通常論文workerは毎時`:30` JSTで動作する。探索専用workerのrunは通常workerの24-run maintenance counterへ加算しない。

## 3. 必読正本

毎回default branch最新HEADを取得し、同じHEADから最低限次を読む。

1. 本書
2. `discovery-exhaustive-run-policy.md`
3. `discovery-continuation-policy.md`
4. `candidate-buffer-policy.md`
5. `queue-v10.md`
6. `fallback-routing.md`
7. `continuation-policy.json`
8. `.survey/work-queue/next-jobs.json`
9. `.survey/work-queue/discovery-state.json`
10. `.survey/survey-state/paper-identity-index.json`
11. 必要に応じてidentity delta、existing jobs、fallback ledger

事項ごとの優先関係は次とする。

- **探索専用という役割境界**: 本書
- **run内で何ラウンド続けるか / 5件上限の意味 / 探索空間枯渇**: `discovery-exhaustive-run-policy.md`
- **一般的なdiscovery継続条件**: `discovery-continuation-policy.md`
- **candidate水位**: `candidate-buffer-policy.md`
- **transport / replay**: `queue-v10.md` / `fallback-routing.md`
- **run全体のSTOP**: `continuation-policy.json`

## 4. candidate在庫

`candidate-buffer-policy.md` のsoft水位を共有する。

- target: 50
- low watermark: 25
- critical watermark: 15

50はhard capではない。在庫が50以上でも低コスト探索で高価値候補が見つかるなら追加してよい。弱い候補で件数を埋めない。

## 5. run内ループ

探索専用runは `discovery-exhaustive-run-policy.md` に従い、固定round数・固定総candidate数・固定submission数を設けない。

1探索軸・1 submissionで送れるcandidateは最大5本。これはtransport batch上限だけであり、run全体の上限ではない。5本送信、1 discovery job完了、candidate inventory 50以上、1軸0件・全重複・低採用率を単独の終了理由にしない。

前roundを送信した後、Actionsが次のdiscovery jobをmaterializeするまでアイドル待機しない。別軸の検索・軽量候補評価を先行し、次batch送信直前に最新HEAD / identity / queue / existing jobsを再取得して再dedupeする。

強いcandidateを1本でも得た場合は、探索空間枯渇判定用の「最後の成功以降の一巡」をリセットし、そのcandidate由来の用語・引用関係も新しい探索軸候補として展開する。

## 6. 探索経路

直近の`discovery-state.json`を読み、高重複・低採用率の軸を機械的に直後反復しない。少なくとも次を独立経路としてローテーションする。

- 新着・recent revision
- 収録済み重要論文のforward citation
- 重要論文のbackward reference
- DBMS / OS / storage / distributed systems / HPC / GPU runtime / networking / memory systems等の隣接分野
- 直近採用候補からのquery expansion
- offload / hierarchical memory / SSD/NVMe / MoE expert placement・cache・prefetch / KV cache / scheduling / disaggregation / inference framework等の重点テーマ

Discoveryは軽量段階に留める。title / abstract / 書誌情報 / 一次資料の存在 / 重複 / テーマ適合性 / 新規性の見込みを確認し、全文精読や検索snippetからの研究内容推測は行わない。

## 7. 二重探索・二重投入の防止

探索開始前とcandidate投入直前の2段階で重複判定する。照合対象はpaper identity index、identity delta、既収録paper、既存research/discovery jobs、GitHub fallback ledger、可能な範囲でLibrary pending/offline seed。

canonical ID、arXiv ID、DOI、OpenReview IDを優先し、最後にnormalized titleを使う。探索中に通常workerまたはActionsが同じ候補を先に登録した場合、後発workerはその候補を送らない。競合が残ってもActions側の最終dedupeで1候補へ収束させ、意図的な重複jobを作らない。

## 8. candidate priority

priorityは少なくとも次を考慮する。

- 重点テーマとの関連度
- 新規性と既存収録との差分
- 実測評価の有無
- 公式実装・コード公開の有無
- 引用関係上の重要度
- SSD/NVMe、MoE、階層メモリ、serving基盤への研究価値

FIFO固定にしない。

## 9. transportとdiscovery-state

GitHub write可能時はworkflow v10のdiscovery transportを使い、paper / queue / state / READMEをScheduled Chatから直接編集しない。

各discovery submissionには通常の`job_id`と`candidates`に加え、トップレベル`discovery_stats`を含める。少なくとも次を保持する。

```json
{
  "discovery_stats": {
    "run_key": "2026-09-12T15:00:00+09:00",
    "round": "specialist-new-arrivals-1",
    "axis": "2609新着・分離サービング",
    "query_summary": "今回実際に使った探索軸と範囲の短い説明",
    "candidate_count": 5,
    "duplicate_filtered_count": 2,
    "duplicate_canonical_ids": ["arxiv:..."],
    "next_axis_hint": "次に優先する異なる探索軸",
    "empty_round_reason": null
  }
}
```

`candidate_count`は検索結果の生hit数ではなく、テーマ適合性等を確認して実質的に評価した候補数。`candidates`にはScheduled Chat側の重複除外後にActionsへ投入する候補だけを入れる。`accepted_count`はScheduled Chat側で確定せず、Actionsが最終dedupe後のresearch job生成数から確定する。

`.survey/work-queue/discovery-state.json` は **GitHub Actions単一writer**。探索専用Scheduled Chatも通常論文Scheduled Chatも直接更新しない。各workerは`discovery_stats`を渡し、Actionsがsubmission単位の冪等性を保って共有stateへ反映する。

GitHub write不能時は `fallback-routing.md` に従い、ChatGPT Library `/LLM-survey-outbox/pending/` へoffline job seedを完全envelopeとして耐久保存する。envelopeにも同じ`discovery_stats`を保持する。探索専用workerはresearch envelopeを作らない。

## 10. 停止と通知

停止条件は`discovery-exhaustive-run-policy.md`と`continuation-policy.json`を正本とする。単一空round、全重複、5件送信、soft target到達、source 1件の障害、Actions次job待ちはstop条件ではない。

通常成功時はユーザーへ通知しない。GitHubとLibraryの両方へ候補状態を耐久保存できない、正本が読めず安全に探索できない、または継続的競合でcandidate投入が実質不能な場合だけ問題として通知する。
