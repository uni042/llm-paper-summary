# LLM論文サーベイ STATUS

> 再構成: **2026-09-29 JST**

現行のLibrary-first手順で継続的に得られる成果情報だけを表示します。旧claim / heartbeat / run-ledger / queue snapshot / maintenance内部状態はSTATUSの表示対象にしません。

## サマリー

| 指標 | 現在値 |
|---|---:|
| 収録論文 | **1312** |
| 直近24時間のResearch完了 | **次回GitHub自動生成で再計算** |
| 直近24時間のDiscovery本文確認・分類 | **次回GitHub自動生成で再計算** |
| 最終Research完了 | **09-25 11:14:16 JST** |
| 最終Discovery完了 | **09-26 04:45:42 JST** |

Researchは完成成果がGitHubへ正規収録され、現行の耐久証拠で照合できる論文を数えます。Discoveryはimmutable成果に記録された本文確認・最終分類済み候補数を数えます。

## 直近7日の日次進捗

今後はSTATUS生成時に、JSTの日付ごとに **Research完了論文数** と **Discovery本文確認・分類数** を7日分ゼロベース集計して表示します。過去の旧方式の集計値を補間・推定して埋めません。

| 日付 (JST) | Research完了 | Discovery本文確認・分類 |
|---|---:|---:|
| 2026-09-29 | **次回再計算** | **次回再計算** |
| 2026-09-28 | **0** | **0** |
| 2026-09-27 | **0** | **0** |

9月29日の旧手動値はLibrary未転送分を混ぜていたため撤回しました。次回生成からGitHubへ到達済みのImport成果だけで再計算します。

## 収録論文

- 現在の論文Markdown実体: **1312件**
- 対象: `papers/inference/**`、`papers/training/**`、`papers/survey/**`
- README、comparison系、Movedスタブは除外します。

## 構造化references探索状況

| 指標 | 件数 |
|---|---:|
| 構造化references総候補 | **7444** |
| 処理済み | **1392** |
| 未処理 | **6052** |
| 収録済みとして除外 | **795** |
| 無関係として除外 | **296** |
| 微妙として除外 | **301** |

- 消化率: **18.7%**
- 処理済み = 収録済み + 無関係 + 微妙。
- STATUS生成時にpaper実体と無関係/微妙台帳からゼロベースで再計算します。

## 速度指標

次回自動生成から以下を常時表示します。

- **Research 7日平均（件/日）**
- **Discovery 7日平均（件/日）**
- **構造化references推定残日数** = 未処理references ÷ Discovery 7日平均

推定残日数は現在ペースが続くと仮定した参考値で、期限予測ではありません。

## 集計方針

- STATUSは表示のたびに現在の正規paper実体・Discovery耐久成果・構造化referencesから再計算します。
- Libraryに未転送の成果はGitHub側STATUSにはまだ現れません。Survey GitHub Import後に反映されます。
- Scheduled workerの生存推定、claim数、heartbeat、旧queue内部状態など、現行Library-first手順の進捗判断に不要な値は表示しません。

---

表示生成: `.survey/scripts/render_status_dashboard.py`
