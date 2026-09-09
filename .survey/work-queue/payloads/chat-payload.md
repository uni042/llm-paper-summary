# Reusable Chat payload slot — update smoke test

このファイルは予定されたChat研究workerが完成済みMarkdownを保存するための固定payloadスロットである。

## 目的

- 通常運用でGitHubの新規ファイル作成を行わない。
- 長い研究Markdownと小さいsubmission JSONを分離する。
- payload保存後にsubmission更新が失敗しても、研究成果本文を既存ファイル上に保持する。
- 次回実行時に対象jobがまだreadyなら、保存済みpayloadを検証したうえでsubmission更新だけ再試行できるようにする。

## 更新規則

予定Chat workerは毎回このファイルの最新blob SHAを取得し、そのSHAを指定した既存ファイルupdateだけを使う。新規payloadファイルは作成しない。固定inboxの処理結果を確認する前に次jobの内容で上書きしない。

この本文はtransport経路確認用のスモークテストであり、論文成果ではない。
