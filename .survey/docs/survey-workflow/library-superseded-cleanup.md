# Library superseded payload disposition

`/LLM-survey-outbox/pending/` は、まだGitHub publicationへ反映する必要があるpayloadだけを保持する。

同じcanonical jobが別attemptで既に正常完了し、元fallback attemptを再実行する必要がなくなった場合、その元payloadは `processed/` へは移さない。`processed/` はそのpayload自身（または明示的なprovenance rebound）がpublicationに使われたことを意味するためである。

代わりにGitHub側ACK manifestの `superseded[]` に載せ、ChatGPT Libraryでは次へ移す。

- `/LLM-survey-outbox/superseded/<envelope-id>.json`

`superseded` と判定するには、元envelopeと同じjobについてcanonical jobがterminal/completedであり、そのjobが指す別attemptのimmutable descriptorと成功result (`ok: true`) が一致し、Researchならpublished paper artifactも存在することを機械的に確認する。

jobがまだready/nonterminal、canonical successful resultが確認できない、paperが不足する等の場合は `waiting[]` のままとし、pendingから動かさない。

この分類により、Libraryの意味は次になる。

- `pending/`: 回復・publicationがまだ必要
- `processed/`: このpayloadがpublicationに反映済み
- `superseded/`: 別attemptでcanonical jobが完了し、このpayloadは不要になった
- `failed/`: identity破損など回復不能
