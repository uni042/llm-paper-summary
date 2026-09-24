# MoE Parallelism / Communication

MoEの専門家並列、テンソル並列との混成、all-to-all通信、専門家配置、負荷分散、ネットワークトポロジーを共同最適化し、複数GPU・複数ノード間の通信待ちと偏りを減らす研究をまとめる。

## 分類境界

主要貢献がMoEのexpert parallelism、all-to-all通信、分散expert配置、通信と計算の重畳、ネットワークトポロジーまたは分散負荷分散である論文を含め、単一GPU内のexpert offloadやexpert数削減だけの研究は含めない。

### 含める研究

- expert parallelismとall-to-all通信最適化
- 複数GPU／複数ノードのexpert配置と負荷分散
- MoE通信と計算の重畳・ネットワーク最適化

### 含めない研究

- 単一GPU向けexpert offload
- expert pruning・mergingだけを主題とする研究

## 近傍系統

- [11-llm-serving-scheduling-disaggregation](../11-llm-serving-scheduling-disaggregation/)
- [01-offload-hierarchical-memory](../01-offload-hierarchical-memory/)
- [02-adaptive-expert-computation-compression](../02-adaptive-expert-computation-compression/)
