# Kimi系 LLMリリース

Moonshot AI Kimiファミリーの主要リリースを新しい順に記録する。初回バックフィル対象期間: **2026-03-04〜2026-09-04**。

Kimiの大規模MoEでは、model file全体の大きさと1 tokenを処理するときの計算量が大きく異なるため、**総parameter・expert数・1 tokenで選ぶexpert数**を分けて読む。

| リリース日 | モデル | 簡単な説明 | 公式リンク |
|---|---|---|---|
| 2026-07-16 | Kimi K3 | 総2.8T parameterの重み公開（open-weight）native multimodal MoE。896個のrouted expertを持ち、各tokenではそのうち16 expertを選んで実行するため、2.8T全parameterを毎token計算するわけではない。最大1M-token context、image / video理解、長時間のcoding / agent taskを対象とする。full weightは7月27日公開。 | https://github.com/MoonshotAI/Kimi-K3 |
| 2026-04-20 | Kimi K2.6 | coding、長時間実行、複数agentを並行利用するAgent Swarmを強化したKimi K2系更新。重みも公開され、自前runtimeでの実行対象にできる。 | https://github.com/MoonshotAI/kimi-help-center/blob/master/en-US/agent/overview.md |

## Kimi K3の構造を読むときの注意

- **2.8T total parameters**: checkpoint全体に含まれるparameter総量。保存storageや、全weightを置くCPU RAM / VRAM容量へ効く。
- **896 routed experts**: routerがtokenごとに選択できるexpertの総数。
- **16 experts/token**: 各tokenで実際に起動するexpert数。計算量は全896 expertを実行する場合より大幅に小さい。
- **重み公開（open-weight）**: weightをdownloadできることを意味し、training code・dataset・licenseまで完全openという意味ではない。

## 用語メモ

- **native multimodal**: textとvision等をmodel設計・training段階から統合して扱うarchitecture。
- **routed expert**: MoE routerがtokenごとに選ぶFFN expert。全tokenが同じexpertを使うわけではない。
- **Agent Swarm（複数agent協調）**: 1つのagentが全taskを順番に処理する代わりに、複数agentへsubtaskを分け、結果を統合する実行方式。
- **長時間エージェント処理（long-horizon agentic work）**: 多数のtool call、file編集、検証・再試行を複数step継続するtask。

ローカル実行を検討する場合、active parameter数だけでなく**checkpoint全体を保持するRAM / storage量**と、expertをCPUへ置く場合のmemory bandwidthも別途見る必要がある。
