# MiniMax系 LLMリリース

MiniMaxの主要LLMを新しい順に記録する。初回バックフィル対象期間: **2026-03-04〜2026-09-04**。

MiniMax系ではcoding benchmarkの強さだけでなく、**重み公開（open-weight）か、最大文脈長（context length）、multimodal入力、複数agent実行の有無**を分けて記録する。

| リリース日 | モデル | 簡単な説明 | 公式リンク |
|---|---|---|---|
| 2026-06-01 | MiniMax M3 | coding、エージェント型業務（agentic work）、最大1M-token context、image / video入力を統合した重み公開（open-weight）multimodalモデル。APIだけでなく自前runtimeでの実行対象にもできる一方、実際に1M contextを使う際のmemory量はruntimeとKV cache方式に依存する。 | https://www.minimax.io/blog/minimax-m3 |
| 2026-03-18 | MiniMax M2.7 | software engineering、professional work、複数agentを役割分担させるAgent Teams、実行結果を基にworkflowを改善するself-evolutionを重点にしたM2系更新。単発chatより長いmulti-step taskを主用途として記録。 | https://www.minimax.io/news/minimax-m27-en |

## 用語メモ

- **重み公開（open-weight）**: model weightをdownloadして自前hardwareで動かせる提供形態。
- **Agent Teams（複数agentチーム）**: taskを複数agentへ分割し、coding・review・researchなど異なる役割を並行または順番に処理させる方式。
- **self-evolution（自己改善型workflow）**: task実行結果・失敗・評価を次のplanningやtool使用へ反映し、複数iterationで処理方針を改善する仕組みを指す表現。
- **1M-token context**: 最大約100万tokenを1 requestの文脈として扱える仕様。実使用時にはKV cacheなどのmemory costも増える。
