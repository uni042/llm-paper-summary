# Scheduled task / GitHub connector reliability references

workflow v10のtransport設計判断を再現できるよう、参照した公式資料・公開検証/不具合報告を固定URLで残す。GitHub Issuesはコミュニティ/利用者による再現報告であり、OpenAI公式仕様ではない。仕様判断はHelp Center等の公式資料を優先し、Issuesはfailure modeの実例として扱う。

## OpenAI official

### Agent mode / scheduled tasks

- https://help.openai.com/en/articles/10291617-what-is-agent-mode

Scheduled taskがconnected appを利用できること、外部データを変更する操作では承認が必要になる場合があり、承認が必要ならscheduled executionが停止し得ることを確認するための一次資料。

### Apps in ChatGPT

- https://help.openai.com/en/articles/11487775-connectors-in-chatgpt

接続アプリのpermission、action approval、workspace/app側権限との関係を確認するための一次資料。

## Public reproduction / bug reports

### Connector authority/tool namespaceが途中で失われる

- https://github.com/openai/codex/issues/42687

同一環境でGitHub CLI経路は機能している一方、connector側でread/write後にGitHub tool namespaceがunavailable/disabledになる再現報告。workflow v10で「単一run中のconnector能力を永続と仮定しない」理由。

### Reconnect成功に見えてcreate-fileが403

- https://github.com/openai/codex/issues/37330

再接続後もrepository discoveryが0件、create-fileで `403 Resource not accessible by integration` となる報告。GitHub App installation/対象repo authorizationがUI上の接続状態と別レイヤーである例。

### User権限とconnector App権限の不一致

- https://github.com/openai/codex/issues/38146

ユーザー自身はpush/admin可能でも、connector Appが実際のrepo owner側へinstallされておらずwriteが403となる報告。read成功だけでwrite権限を推定しない理由。

### Endpoint単位の403

- https://github.com/openai/codex/issues/39018

repository/PR/default-branch fileのreadは成功する一方、refs/commits/compare/workflow run等が403となる報告。GitHub accessを単純なread/write二値として扱わない理由。

### Capability surfaceの非対称

- https://github.com/openai/codex/issues/41863

file write/delete、branch/PR操作など一部操作は可能でも、branch listing/deletion等の専用toolがないというcapability gap報告。通常経路を少数の既知operationへ絞る理由。

### Private repo access変更後にGitHub toolsが消える

- https://github.com/openai/codex/issues/40729

private repository access設定後にtool availabilityが失われた報告。connector failureをjob failureと同一視せずtransport failureとして分離する理由。

### Connector create/writeは403だが別GitHub認証経路は成功

- https://github.com/openai/codex/issues/21387

connectorでwrite operationが403となる一方、別の認証済みGitHub CLI経路では成功する報告。repo自体やユーザー権限だけでなくconnector-specific authorityを独立したfailure domainとして扱う理由。

## workflow v10への反映

以上から、予定Chat workerのGitHub操作を次に限定する。

1. 既存・事前作成済み固定JSON slotの小さいupdate。
2. 既存・固定inboxの小さいupdate。
3. 08:30 workerも既存固定payload/inboxのみ。
4. paper/state/README/queueの変更はGitHub Actionsへ委譲。
5. write不能はresearch failureではなくtransport failureとしてNotion temporary fallbackへ退避。
6. 成功判定は「writeを試みた」ではなくActions resultと最新queueで行う。
7. 構造化方式は安全検査回避ではなく、payload size、validation、partial retry、idempotencyを改善するために使う。

この文書のリンク切れや仕様変更は、必要に応じて更新する。
