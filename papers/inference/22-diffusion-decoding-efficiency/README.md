# Diffusion Language Model Decoding Efficiency

離散・masked diffusion言語モデルの生成token commit順序・並列幅、denoising回数、単一request内のrefinement/advancement依存、候補軌道の分岐・剪定・計算配分を制御し、NFEやlatency/throughputと品質の関係を改善する研究をまとめる。

## 分類境界

Include inference-time methods whose primary mechanism schedules, selects, branches, prunes, or verifies denoising states or token commitments within a discrete/masked diffusion-LM request, with direct evidence on denoising rounds/NFE, latency/throughput, or quality-efficiency. Include per-request lane scheduling only when it changes diffusion refinement/advancement dependency. Exclude new model/backbone architecture or training-only gains; general conditional layer/token skipping independent of the diffusion denoising process; external target-model draft verification (05); primary KV/cache management (07); primary kernel/runtime work (09); cross-request admission/batching/resource scheduling (11); sparse query-key computation (13); and methods whose primary evidence shows quality gains without inference-efficiency evidence.

### 含める研究

- masked位置のunmask/commit順序と同時更新幅の制御
- denoising round/NFE予算の適応的配分
- diffusion refinement/advancementを分離する単一request内の依存制御
- denoising軌道の探索・remask・剪定による品質対計算量改善

### 含めない研究

- 一般model/backbone設計、training-only、効率評価のない品質改善
- 通常の入力token/layer skipping04、外部target-modelによるdraft verification05
- 主貢献がKV/cache07またはkernel/runtime09の研究
- cross-request admission/batching/resource scheduling11、sparse query-key13

## 近傍系統

- [04-conditional-computation](../04-conditional-computation/)
- [05-speculative-decoding-moe](../05-speculative-decoding-moe/)
- [11-llm-serving-scheduling-disaggregation](../11-llm-serving-scheduling-disaggregation/)

この系統は複数論文からなる明確な近傍クラスタとしてDiscoveryの昇格ゲートを通過した。単一論文だけを理由に細分化せず、上記の分類境界を維持する。
