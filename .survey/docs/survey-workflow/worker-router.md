# Chat worker router

Chatの予定タスクは、実行時刻を見て**論文worker**か**その他更新worker**のどちらか一方だけを選ぶ。

## ルーティング

- **08:30 JST** → その他更新workerだけを使う。論文queueの research / audit / discovery は処理しない。
- **それ以外の毎時 :30** → 論文workerだけを使う。フレームワーク／新規LLM更新は行わない。

同じ実行枠で両方を叩かない。

---

## A. 論文worker

正本: [README.md](README.md) と [queue-v9.md](queue-v9.md)

Chat側の固定入口:

- 本文: `.survey/work-queue/payloads/chat-payload.md`
- trigger: `.survey/work-queue/submissions/chat-inbox.json`
- result: `.survey/work-queue/results/chat-inbox.json`

Chatは新規payload/submissionを作らず、既存固定ファイルを現在blob SHA付きでupdateする。trigger push後は `Survey helper worker` が論文本体反映、job/state遷移、派生view更新、ready=0時のdiscovery補充を行う。

---

## B. その他更新worker（08:30専用）

対象は以下だけ。

1. `framework-updates/**` — LLM推論・serving・runtime等の本質的な更新
2. `llm-releases/**` — 新規LLMの正式公開・一般提供・主要モデル更新

論文、paper queue、survey stateはこのworkerから変更できない。

Chat側の固定入口:

- payload: `.survey/update-worker/update-payload.json`
- trigger: `.survey/update-worker/update-inbox.json`
- result: `.survey/update-worker/result.json`
- Actions: `Framework and LLM update worker`

### 08:30の調査対象

フレームワークは vLLM、SGLang、TensorRT-LLM、llama.cpp、Ollama、ExLlama、LightLLM 等を中心に、性能、memory、KV cache、MoE、offload、I/O、分散、kernel、schedulingなど能力・性能特性を実質的に変える更新を確認する。軽微なbug修正、allowlist追加、chat template追加、単なる対応model/device追加だけの変更は原則除外する。

新規LLMは公式公開・一般提供された主要modelを対象にする。噂、リーク、ティザーだけでは登録しない。Qwen系MoE、小型高性能model、推論効率に大きく関わるmodelは重点確認する。

一次資料は公式release、公式repository / PR、公式blog、公式model配布ページを優先する。

### update payload schema

Chatは対象ファイルを直接編集しない。最新HEADから対象ファイルのblob SHAを取得し、固定payloadをupdateした後、固定inboxをupdateしてActionsへ処理を渡す。

```json
{
  "schema_version": 1,
  "attempt_id": "update-<unique>",
  "kind": "framework_llm_update",
  "artifacts": [
    {
      "path": "framework-updates/README.md",
      "expected_blob_sha": "<current blob sha>",
      "edits": [
        {
          "op": "replace_once",
          "old": "<exact old text>",
          "new": "<replacement>"
        },
        {
          "op": "insert_after_once",
          "anchor": "<unique exact anchor>",
          "text": "<new text>"
        }
      ]
    }
  ],
  "summary": "<short summary>"
}
```

既存ファイルでは `expected_blob_sha` が必須。新規ファイルの場合だけ `expected_blob_sha` を省略し、`content` に完成内容を入れる。既存ファイルも必要なら `content` による全文置換を使えるが、通常はpayloadを小さくするため `edits` を優先する。

対応edit:

- `replace_once`: exact `old` を1箇所だけ `new` に置換
- `insert_after_once`: exact `anchor` が1箇所だけ存在する場合、その直後へ `text` を挿入
- `insert_before_once`: exact `anchor` が1箇所だけ存在する場合、その直前へ `text` を挿入

match数が0または2以上ならworkerは失敗扱いにして対象ファイルを変更しない。すべてのartifactを検証してから書き込む。

固定inboxは次の形で、payloadと同じ一意な `attempt_id` を使う。

```json
{
  "schema_version": 1,
  "attempt_id": "update-<unique>",
  "payload_path": ".survey/update-worker/update-payload.json"
}
```

固定payloadのupdateだけ成功してtrigger updateが失敗した場合、対象更新は未反映なので完了扱いにしない。次回、対象blob SHAとpayload内容がまだ有効ならtriggerだけ再送してよい。

Actions実行後は `.survey/update-worker/result.json` を確認する。`ok: true` と同じ `attempt_id` を確認して初めて完了とする。`ok: false` の場合は対象ファイルへ反映済みとみなさない。

### 安全境界

その他更新workerは `framework-updates/**` と `llm-releases/**` 以外を拒否する。2つのGitHub Actions workerは同じconcurrency groupを使い、mainへのcommitを同時実行しない。
