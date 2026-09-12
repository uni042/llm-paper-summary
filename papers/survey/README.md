# Survey / サーベイ

LLMシステム研究を横断的に整理する **survey / review 論文** を置く独立カテゴリ。Inference / Training の個別手法論文とは分け、複数の研究系統を俯瞰する文献をここへ収録する。

新規収録時は、対象が主に推論システムを扱うか、学習システムを扱うか、両方を横断するかに応じて適切な下位系統ディレクトリを作る。個別の新規手法を主題とする原著論文は従来どおり Inference / Training 側へ置く。

各下位系統の論文一覧は自動生成し、次の順に相互排他的に分類する。

1. 公開年月が直近12か月の論文
2. それ以前で、リポジトリ内の別論文から arXiv ID / DOI が明示参照されている論文
3. その他

実装情報が論文メタデータまたは構造化本文で明示されている場合は一覧に `✓` を表示する。

<!-- survey:auto:start -->
## 自動生成の収録状況

サーベイ論文：**6本**。

| 系統 | 本数 |
|---|---:|
| [01-kv-cache-optimization](01-kv-cache-optimization/README.md) | 1 |
| [01-kv-cache-systems](01-kv-cache-systems/README.md) | 1 |
| [02-diffusion-llm-inference](02-diffusion-llm-inference/README.md) | 1 |
| [03-inference-engines](03-inference-engines/README.md) | 2 |
| [llm-serving-systems](llm-serving-systems/README.md) | 1 |
<!-- survey:auto:end -->
