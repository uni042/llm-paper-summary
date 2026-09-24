# レガシー棚卸し — コード経路とデータの初回確認

## 初回コード経路調査の対象と状態

- 対象commit: `5cccd8347ae6ce2c14129c73b48643aad1005469`（初回調査時点）
- 調査日: 2026-09-24
- 種別: 静的コード経路の一次確認。**ファイル全件のデータ分類は未実施**。
- 判定: この文書の確認だけでreader削除・データ削除へ進んではならない。
- 現行mainは調査中にも進行している。work-queueのライブデータを扱う前に、最新mainへの追随、書込凍結、active claim/result待ちの確認、全件台帳の再生成が必要。

## 最新固定スナップショットの棚卸し（2026-09-24）

- 対象commit: `62401ab310da02b472d31715e3c4b3b6364a9bbc`
- 機械可読台帳: `.survey/reports/legacy-inventory.json`（`source_commit` を確認すること）
- 論文監査: `.survey/reports/legacy-paper-audit.json`（同じ `source_commit` を確認すること）
- 走査対象ファイル: 10,902。UTF-8走査不能0。
- 分類: A〜Eのレビュー済み分類0。未レビュー10,902。したがって `legacy_remaining=10,902` は「旧形式の実データ件数」ではなく、未分類・未決のゲート値である。
- 旧形式marker候補ヒット: 1,320（`chat-inbox.json` 105、旧Scheduled Chat名1,193、旧unbanked marker 2、旧record bank root 10、旧要約heading 10）。文字列一致であり、ライブ/履歴や旧reader依存を個別判定した件数ではない。
- 論文監査対象: 1,026。本文品質 PASS 243 / WARN 49 / FAIL 734、明示 `list_summary` 欠落0（一覧品質 PASS 1,017 / WARN 9 / FAIL 0）、代表結果監査 PASS 1,000 / FAIL 26。
- この状態では旧reader削除、履歴削除、ライブ移行を開始しない。紙面FAILは一次資料を読んで修正し、状態ファイルは参照・終端・writer契約を個別に確認する。
- 作業ブランチで一次資料を再確認したMixtral offloading論文（`2312.17238`）の評価説明を日本語化し、本文・一覧・代表結果の3監査がPASS。変更後も全論文FAIL件数の大勢は変わらず、全件合格の条件には未到達。

## コード経路の暫定分類

|経路|確認できた実装|暫定分類|次のゲート|
|---|---|---|---|
|`.survey/scripts/list_summary.py`|明示 `list_summary` の品質監査のみ。本文・`summary` からの生成関数は除去済み。|品質監査は現行reader（A）。旧生成互換は撤去済み。|明示値の欠落は構造検査と監査で拒否。本文品質のPASSはreader撤去条件と分離。|
|`.survey/scripts/replay_record_fallback.py`|5スロットResearch/Audit fallbackを現行不変提出へ変換する。旧 `chat-inbox.json` payloadを読む分岐もある。|現行Library退避・再生は保持対象（A）。chat-inbox読取だけ旧互換（E）。|fallback-inbox/archive/failedの全件分類と再生・終端確定後、旧分岐のみ除去。|
|`.survey/scripts/dispatch_fallback_inbox.py`|現行fallback dispatchのほか、旧chat-inbox bundleと `writes` wrapperなしDiscovery payloadを扱う分岐がある。|現行dispatchは保持（A）。旧envelope救済はE候補。|全inbox実データをreader単位で照合し、正常変換/終端/記録付き破棄を確定。|
|`.survey/scripts/record_bank_config.py`|現行bank設定に加え、旧bank root alias `a` と旧slot path受入れ関数がある。|新規writerが旧pathを出さないことを確認したうえでreader部分はE候補。|全records/claims/descriptor参照先を棚卸しし、旧path参照0を確認。|
|`.survey/scripts/claim_worker.py`|旧Scheduled Chat長時間leaseを正規化/無効化する処理を含む。|旧lease normalizerはE候補。|ライブclaimを凍結中に分類し、期限切れ・完了・handoffのいずれかを全件確定。|
|`.survey/scripts/claim_worker_with_banks.py`|現行bank割当とLibrary fallbackを維持しつつ、旧unbanked claimをLibraryへ移行した印 `legacy-unbanked-to-library` を書く処理がある。|Library fallbackは現行・障害復旧系として保持（A）。旧移行能力/移行markerはC/E候補。|全claim・Library checkpointを照合し、markerが不要か、データ移行が完了しているかを証明。|
|`.survey/scripts/process_discovery_precheck.py`|入力requestはschema v3のみを受け付ける。|現行producer/strict reader（A）。|resultの旧schema readerは別コード（queue_worker等）を追跡し、requestとresult契約を混同しない。|
|`.survey/scripts/queue_worker.py`|Discovery submission/job化の経路。現行precheck request制約とは別に旧precheck result読取の記載がある。|旧result reader候補（E）。|現存resultの参照・終端状態を全件特定し、旧resultが0になるまで保持。|
|`.survey/scripts/process_immutable_submission.py`|現行immutable descriptorと5スロットから論文更新を行う。|現行reader/writer（A）。|旧形式除去後もimmutable submissionの正常系・防御検査を回帰確認。|

## 互換コードを外す前に現行経路へ残す機能

2026-09-24の `62401ab` を基準に現行コードとデータの両方を照合した。削除時に必要な機能と、除去を止める実データは次の通り。

|旧分岐・場所|現行でも必要な機能|現行経路／置換条件|削除可否|
|---|---|---|---|
|Library退避の再生（`.survey/scripts/replay_record_fallback.py`）|失敗時にLibrary退避を回収し、Research/Auditの5スロットから復旧する。|現行fallback-inboxから、bankまたはLibraryへ安全に保存し、試行ごとの不変submissionへ変換する。これは現行障害復旧経路なので維持する。|現行部分は削除しない。|
|固定 `chat-inbox.json` 読取（同上）|旧固定輸送にしか残っていない内容を救済する。固定ファイルを再生成しない。|旧bundleを現行の不変submissionへ変換、終端状態として確定、または根拠付きで破棄する。台帳上の固定輸送markerは105件あり、そのうちfallback-archive 84、fallback-failed 10、fallback-inbox 1ファイルに検出。これは文字列ヒット数でありpayload実数ではない。|データ処理とblob照合が完了するまでreaderを維持。|
|旧Discovery envelope救済（`.survey/scripts/dispatch_fallback_inbox.py`）|正規wrapperのない旧payloadに残るDiscovery結果を拾う。|現行writerの `writes` wrapperから現行immutable submissionを作る。受信箱と退避履歴の旧payloadを移行・終端・記録付き破棄してから、旧分岐を外す。|受信箱・退避履歴の照合前は維持。|
|旧bank alias/path（`.survey/scripts/record_bank_config.py` 等）|旧rootに残る5スロットrecordと、そのclaim/submission参照を救済する。|現行のbank IDと正規slot pathへデータ・参照を移し、readerを正規path限定にする。marker hitはコード/試験/退避データを含め10ファイル。|参照closure確認前は維持。|
|bank未割当claim移行（`.survey/scripts/claim_worker_with_banks.py`）|すでに開始した非Scheduled Chat claimがbankなしでも処理を続けられるようLibraryへ経路を付ける。|新しいclaimの通常割当ではbank予約を行い、bankを使えない場合の現行Library fallbackは保持する。残るactive claimのrouteを全件検証し、migration markerなしでも同じ経路が成立した後にだけ旧claim移行分岐を外す。|ライブclaimの書込凍結・route照合前は維持。|
|論文の旧要約読取（`.survey/scripts/list_summary.py`）|公開一覧で明示要約のない旧ページを表示する。|現行producerは `list_summary` を明示生成する。旧heading markerは論文10件に残るため、当該ページを通常の本文監査で直した後にのみ旧heading/fallback readerを外す。|論文移行完了まで維持。品質修正は現在の作業優先対象から外す。|

この表は機能移管と削除ゲートを特定するもの。列挙件数はmarker hitであり、個々の旧payloadが有効・未処理・ライブであるとの判定ではない。個別レコードの移行結果は機械可読台帳へ記録する。

## 旧互換専用試験候補

次のテストは名称または実体に旧データ受入れ・正規化を含む。最終的には削除、または旧形式を明示拒否する試験へ置換する。移行完了前に削除しない。

- `.survey/tests/test_claim_and_legacy_transport_state.py`: lease失効状態と重複lease policyの撤去を検査。
- `.survey/tests/test_legacy_record_bank_alias.py`: 終端済み旧chat record bundleをack/archiveする経路を検査。
- `.survey/tests/test_legacy_scheduled_chat_lease_cap.py`: 旧8時間claimの正規化や長いleaseの短縮を検査。

## 再現用source blob SHA

|ファイル|blob SHA|
|---|---|
|`.survey/scripts/list_summary.py`|`a52d78a005bca93626363cfd2c73a6974545edc8`|
|`.survey/scripts/replay_record_fallback.py`|`cac704240af20618d4f3efa06ee806c7a6716b4b`|
|`.survey/scripts/dispatch_fallback_inbox.py`|`3daf70ec3c10f0263ab35a6e5eb535f3261f4012`|
|`.survey/scripts/record_bank_config.py`|`94d30b0937a947760296eea4670f58b3fd04897a`|
|`.survey/scripts/claim_worker.py`|`571c1bedb1668b7144753f67d15808d8a899fd0e`|
|`.survey/scripts/claim_worker_with_banks.py`|`7e59f4e77d39b23482a0e3a2f2e56bcb82ecdfd5`|
|`.survey/scripts/process_discovery_precheck.py`|`660100e816978f2c3c6d570db5285a44e8e8323d`|
|`.survey/scripts/queue_worker.py`|`628ca4004475fab597a2383591d0059beaa40d94`|
|`.survey/scripts/process_immutable_submission.py`|`b59b6ac0e3f6136df55d8d1f749e8fd1a9c34bd2`|
|`.survey/scripts/fallback_transport.py`|`63374c9dce8c266a393eb059fc8fa7ac9cb55368`|
|`.survey/tests/test_claim_and_legacy_transport_state.py`|`a4a5c3cc3ddc90ea95b356f38e0471ccdce45f79`|
|`.survey/tests/test_legacy_record_bank_alias.py`|`6dd752c462e6847617e73d3fcce904479983fe28`|
|`.survey/tests/test_legacy_scheduled_chat_lease_cap.py`|`be8d9be091febacafd1d46a2d4f4f9ad7bfbe1cc`|

As of `12cc4e657bdcd1badc924858dec27f9dadc77af0`, `.survey/tests/test_legacy_scheduled_chat_lease_cap.py` was removed from `main`; the earlier test path is retained here only as evidence of the initial snapshot. No deletion is needed for that already-removed file.\n\n
## 固定スナップショットでの論文監査

- 対象commit: `3139b5a59501dee401bae94b9419d5d68b2e3250`
- レポート: `.survey/reports/legacy-paper-audit.json`
- 対象論文: 1,026件（inference / training / survey。本文品質監査で inference+survey と training に分けて全件処理）
- 本文品質: PASS 243 / WARN 49 / FAIL 734
- 一覧用 `list_summary`: PASS 1,017 / WARN 9 / FAIL 0。明示値の欠落0件
- 概要の代表結果: PASS 1,000 / FAIL 26
- 本文FAIL理由の出現数（同一論文内で重複あり）: 手法構成要素の段落不足3,708、英語専門語75、日本語比率11、説明文量12。これは監査失敗レコードの分類であり、単純な論文件数ではない。
- 26件の代表結果FAILと734件の本文FAILは科学的内容の再読解が要る。監査文言から自動で結果を補完しない。個別の一次資料確認を伴う修正後、全監査を再実行する。
- この節の数値は `3139...` を固定した時点の監査結果である。以後の最新実行結果は `legacy-paper-audit.json` と `legacy-inventory.json` 内の `source_commit` を基準にし、各レポートのblob SHAで入力を照合する。先行の `df7386...` は初回実行履歴として保持する。

## 残作業

1. 現行mainの安定した移行基準点を定める。ワーカーが書込中のHEADを固定したままライブ移行を開始しない。
2. 論文frontmatter/bodyを全件走査し、旧一覧形式の件数と要人手読解件数を確定する。
3. claims、record banks、fallback、precheck、submission/result間の実参照を解決し、A〜Eの全件JSON台帳を生成する。
4. 現行producer側の旧形式生成能力を別途検索し、この静的確認に含まれていないpath/field/worker aliasを追加する。
5. 台帳に未分類・未決・active itemが残る間は移行・削除へ進まない。

## 進捗追記 — 2026-09-24

一覧用説明の旧生成readerを削除した。`survey.py` はfrontmatterの `list_summary` だけを公開一覧に使い、欠落・空値は例外とする。`check_repository.py` でも必須項目として検査する。`audit_list_summary_quality.py` は明示値を監査し、旧要約生成関数を呼ばない。論文本文の品質監査FAILは残存し得るが、旧本文形式readerを維持する理由にはしない。
