# FlexFlow Serve

FlexFlow Serveの主要な機能・性能更新を継続的に記録する集約ページ。投機的デコード（speculative decoding）、複数GPU配置、serving scheduler、memory管理など、推論性能へ直接影響する更新があった場合に記録する。

## 現在できること

- LLM servingで複数GPUへmodel計算を配置し、requestをbatch化して実行できる。
- speculative inferenceでは、小さいdraft model等から複数候補を作り、target modelで木構造の候補をまとめて検証することで逐次decode回数を減らせる。
- model parallelismや実行配置をruntime側で管理し、単純な1 GPU / 1 request実行より大きなmodel・高い並列度を扱うことを目的とする。
- FlexFlow runtimeのoperator graph / task parallelismを使い、GPU間の計算・通信をまとめてscheduleできる。

現在は活発な機能追加が止まっているため、以下では**現行の主要能力**と、追跡期間内に本質的な新機能がなかったことを分けて記録する。

## 初期収録期間

2026-06-03〜2026-09-03

## 掲載対象となる更新なし

対象期間内のrelease、tag、commit、PRを確認した範囲では、性能・memory architecture・serving方式を大きく変える新規更新は確認できなかった。

確認時点で最新tagは対象期間より前のv25.2.1で、default branchの最新commitも2025-04-12だったため、この期間は「更新なし」として残す。

これはproject自体に価値がないという意味ではなく、**このrepositoryが追跡対象としている期間内に、新たに記録すべき本質的差分がなかった**という意味である。

- [repository](https://github.com/flexflow/flexflow-serve)
- [tags](https://github.com/flexflow/flexflow-serve/tags)
