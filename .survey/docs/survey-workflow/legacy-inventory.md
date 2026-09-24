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
|`.survey/scripts/list_summary.py`|旧 `## 一文要約` と `fallback_summary` を読む処理、`_compact_legacy` がある。|旧論文救済reader候補（E）。ただし旧論文データが残る限り削除不可。|全公開論文の明示 `list_summary` と品質監査PASSを確認。|
|`.survey/scripts/replay_record_fallback.py`|5スロットResearch/Audit fallbackを現行不変提出へ変換する。旧 `chat-inbox.json` payloadを読む分岐もある。|現行Library退避・再生は保持対象（A）。chat-inbox読取だけ旧互換（E）。|fallback-inbox/archive/failedの全件分類と再生・終端確定後、旧分岐のみ除去。|
|`.survey/scripts/dispatch_fallback_inbox.py`|現行fallback dispatchのほか、旧chat-inbox bundleと `writes` wrapperなしDiscovery payloadを扱う分岐がある。|現行dispatchは保持（A）。旧envelope救済はE候補。|全inbox実データをreader単位で照合し、正常変換/終端/記録付き破棄を確定。|
|`.survey/scripts/record_bank_config.py`|現行bank設定に加え、旧bank root alias `a` と旧slot path受入れ関数がある。|新規writerが旧pathを出さないことを確認したうえでreader部分はE候補。|全records/claims/descriptor参照先を棚卸しし、旧path参照0を確認。|
|`.survey/scripts/claim_worker.py`|旧Scheduled Chat長時間leaseを正規化/無効化する処理を含む。|旧lease normalizerはE候補。|ライブclaimを凍結中に分類し、期限切れ・完了・handoffのいずれかを全件確定。|
|`.survey/scripts/claim_worker_with_banks.py`|現行bank割当とLibrary fallbackを維持しつつ、旧unbanked claimをLibraryへ移行した印 `legacy-unbanked-to-library` を書く処理がある。|Library fallbackは現行・障害復旧系として保持（A）。旧移行能力/移行markerはC/E候補。|全claim・Library checkpointを照合し、markerが不要か、データ移行が完了しているかを証明。|
|`.survey/scripts/process_discovery_precheck.py`|入力requestはschema v3のみを受け付ける。|現行producer/strict reader（A）。|resultの旧schema readerは別コード（queue_worker等）を追跡し、requestとresult契約を混同しない。|
|`.survey/scripts/queue_worker.py`|Discovery submission/job化の経路。現行precheck request制約とは別に旧precheck result読取の記載がある。|旧result reader候補（E）。|現存resultの参照・終端状態を全件特定し、旧resultが0になるまで保持。|
|`.survey/scripts/process_immutable_submission.py`|現行immutable descriptorと5スロットから論文更新を行う。|現行reader/writer（A）。|旧形式除去後もimmutable submissionの正常系・防御検査を回帰確認。|

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
