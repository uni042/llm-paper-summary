# LLM論文サーベイ STATUS

> 自動生成: **2026-09-30 16:39:51 JST**

GitHubへ到達済みのLibrary-first成果だけから再構成します。ChatGPT Libraryへはアクセスしません。

## サマリー

| 指標 | 現在値 |
|---|---:|
| 収録論文 | **1361** |
| 直近24時間のResearch完了 | **86** |
| 直近24時間のDiscovery本文確認・分類 | **200** |
| 最終Research完了 | **09-30 16:08:32 JST** |
| 最終Discovery完了 | **09-30 13:18:24 JST** |
| Research 7日平均 | **12.3件/日** |
| Discovery 7日平均 | **28.6件/日** |
| references推定残日数 | **207.5日** |

日次進捗はImport日時ではなく元worker実行日時を優先します。旧Research成果にworker時刻がない場合だけImport処理日時へフォールバックします。

## 直近7日の日次進捗

| 日付 (JST) | Research完了 | Discovery本文確認・分類 |
|---|---:|---:|
| 2026-09-24 | **0** | **0** |
| 2026-09-25 | **0** | **0** |
| 2026-09-26 | **0** | **0** |
| 2026-09-27 | **0** | **0** |
| 2026-09-28 | **0** | **0** |
| 2026-09-29 | **5** | **0** |
| 2026-09-30 | **81** | **200** |

## 収録論文

- 現在の論文Markdown実体: **1361件**
- 対象: `papers/inference/**`、`papers/training/**`、`papers/survey/**`。
- README、comparison系、Movedスタブは除外します。

## 構造化references探索状況

| 指標 | 件数 |
|---|---:|
| 構造化references総候補 | **7444** |
| 処理済み | **1515** |
| 未処理 | **5929** |
| 収録済みとして除外 | **841** |
| 無関係として除外 | **352** |
| 微妙として除外 | **322** |

- 消化率: **20.4%**
- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。
- STATUS生成時にpaper実体と無関係/微妙台帳からゼロベースで再計算します。過去のschema-v3 precheck snapshotは表示値の根拠にしません。

## 集計方針

- GitHub checkoutだけを入力にし、ChatGPT Library未転送成果は数えません。
- Discoveryはimmutable runの `run_key` と `record_count` を使用し、同一run_keyを一度だけ数えます。
- Researchはimport resultの `worker_completed_at` を使用します。旧成果だけ `processed_at` を代用します。
- Library未転送分は次回Survey GitHub Import後に反映されます。
- references推定残日数は未処理references ÷ Discovery 7日平均です。

---

表示生成: `.survey/scripts/render_status_dashboard.py`
