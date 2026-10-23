# Static Structured Model Pruning

事前学習済みdense Transformerから入力に依存しない固定のchannel/neuron、attention head、layerなどの構造単位を削除し、推論時のparameter・演算量を小さくする研究をまとめる。importance推定、mask学習、calibration、LoRA/fine-tuning/continued-pretraining/distillationによる削除後の回復工程を許容する。

## 分類境界

推論時の主要ボトルネック削減を目的に、事前学習済みdense Transformerから固定のchannel/neuron、attention head、layerなどを物理削除し、requestごとに変わらない小型dense architectureを作る研究を含める。入力token依存のpruning/skip/early exit、unstructured/N:M/block weight sparsity、quantization/encodingだけ、MoE expertだけのpruning、model topologyを変えないkernel/compiler最適化は除く。

### 含める研究

- 固定channel/neuron/hidden-dimension pruning
- 固定attention-head pruning
- 固定layer/depth pruning
- 削除後modelを作るためのcalibration、mask learning、軽量な回復学習

### 含めない研究

- input/token依存のtoken pruning、layer skipping、early exit（04）
- unstructured/N:M/block weight sparsity、weight quantization、encoding（16または別該当family）
- MoE expert固有のpruning（02/06）
- parameter topologyを変えないkernel/compiler最適化

## 近傍系統

- [04-conditional-computation](../04-conditional-computation/)
- [16-weight-quantization-compression](../16-weight-quantization-compression/)

この系統は複数論文からなる明確な近傍クラスタとしてDiscoveryの昇格ゲートを通過した。単一論文だけを理由に細分化せず、上記の分類境界を維持する。
