# MLX LM

MLX LMの主要な機能・性能更新を継続的に記録する集約ページです。未リリースPRは正式releaseと区別して記録します。

## 初期収録期間

2026-06-03〜2026-09-03

対象期間内のstable releaseはない。以下は未リリースPRとして分離して記録する。

## 注視すべきPR

- **2026-09-02 — #1817（Open）**: multi-token decodeでabsorbed MLAとmaterialized経路をcache長から動的選択。GLM-4.7-Flash draft modelで2.8→14.7 tok/s、8,192 cacheのverify stepは363.7→3.3 ms。[PR #1817](https://github.com/ml-explore/mlx-lm/pull/1817)
- **2026-08-29 — #1804（Open）**: serverへKV cache量子化設定を公開し、長文cacheのmemory増加を抑える。性能値なし。[PR #1804](https://github.com/ml-explore/mlx-lm/pull/1804)
- **2026-09-02 — #1821（Draft）**: speculative decoding／MTP rollback用のtrimmable RecurrentCache案。profiling未実施で、RAM増加とのtrade-offが残る。[PR #1821](https://github.com/ml-explore/mlx-lm/pull/1821)

[公式releases](https://github.com/ml-explore/mlx-lm/releases)の最新stableは期間前のv0.31.3。
