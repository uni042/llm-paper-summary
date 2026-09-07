# FlexFlow Serve

FlexFlow Serveの主要な機能・性能更新を継続的に記録する集約ページ。投機的デコード（speculative decoding）、複数GPU配置、serving scheduler、memory管理など、推論性能へ直接影響する更新があった場合に記録する。

## 現在できること

- **複数GPUへLLM実行を配置**: modelのoperator graphを複数GPUへ分割し、単一GPUに収まらないmodelや高い同時実行数を扱える。単純なlayer分割だけでなく、runtimeがoperatorと通信を含む実行graphとして扱う。
- **request batchingとserving scheduling**: 複数requestをまとめてGPUへ流し、GPUが小さいrequestを1件ずつ処理して空く時間を減らす。request長や実行段階に応じてruntime側で処理順を管理する。
- **tree-based speculative inference**: 小さいdraft model等で次token候補を1本だけでなくtree状に複数生成し、target modelで候補群をまとめて検証できる。候補が受理されればtarget modelを1 tokenごとに逐次実行する回数を減らせる。
- **複数draft / targetの組合せ**: 投機的推論では候補生成側と検証側を別modelとして構成でき、draftの軽さと候補受理率のtrade-offを調整できる。単純なgreedy draftより候補幅を広げることで、target forward 1回あたりに確定できるtoken数を増やす狙いがある。
- **model parallel execution**: FlexFlow runtimeのtask parallelismを使い、operator計算とGPU間通信を同じ実行計画の中でscheduleできる。計算だけを分割して通信を後付けするより、device配置と通信costをまとめて考えられる。
- **memoryを含む実行計画**: 大きいmodelのweight、activation、KV等を複数device上で扱い、device memory制約の中で実行可能な配置を作ることを目的とする。実際の利得はGPU間接続やmodel shapeに強く依存する。
- **research-oriented serving runtime**: vLLMやSGLangのような現在活発な汎用serving基盤と比べると更新頻度は低いが、複数GPU配置とtree型speculative inferenceを一体で扱う研究実装として位置づけられる。

現在は活発な機能追加が止まっているため、以下では**現行の主要能力**と、追跡期間内に本質的な新機能がなかったことを分けて記録する。

## 初期収録期間

2026-06-03〜2026-09-03

## 掲載対象となる更新なし

対象期間内のrelease、tag、commit、PRを確認した範囲では、性能・memory architecture・serving方式を大きく変える新規更新は確認できなかった。

確認時点で最新tagは対象期間より前のv25.2.1で、default branchの最新commitも2025-04-12だったため、この期間は「更新なし」として残す。

これはproject自体に価値がないという意味ではなく、**このrepositoryが追跡対象としている期間内に、新たに記録すべき本質的差分がなかった**という意味である。

- [repository](https://github.com/flexflow/flexflow-serve)
- [tags](https://github.com/flexflow/flexflow-serve/tags)