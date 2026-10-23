# Linear-Recurrent Language Model Architectures

生成時に文脈長へ比例しない再帰状態で履歴を表す言語モデルのSSM、retention、linear attention、動的状態更新則と有界局所attentionとの混成を扱う。モデルの状態表現・更新則自体の設計を中心に、推論メモリ、速度、想起精度の関係を比較する。

## 分類境界

主要貢献が、生成時に文脈長へ比例しない再帰状態へ履歴を集約するSSM・retention・linear attention・data-dependent recurrenceのモデル構造または状態更新則である言語モデルを含む。有界局所attentionとの混成も含む。通常TransformerのKV保持/圧縮/offload、純kernel/runtime、固定再帰decodeを主要機構としないFFT長畳み込み、test-time gradient updateによるneural memory、recurrenceを部品として使うだけの研究は除く。

### 含める研究

- Selective state-space and linear-time sequence-model architectures
- Recurrent or matrix-state linear-attention update rules
- Retention and dynamic recurrence language-model architectures
- Recurrent plus local-attention hybrids with recurrent sequence modeling as the core

### 含めない研究

- Kernel, compiler, or runtime optimization without a model-operator contribution
- KV cache, checkpoint, or recurrent-state storage/compression policy
- Request-level serving, scheduling, or disaggregation
- Speculative decoding and verification methods
- General-purpose RNN theory with no language-model architecture contribution
- Fixed-state decodingを主要機構としないFFT長畳み込み
- Test-time gradient updateを主機構とするneural memory

## 近傍系統

- [07-kv-cache-optimization-compression](../07-kv-cache-optimization-compression/)
- [09-kernel-runtime-compilation](../09-kernel-runtime-compilation/)
- [13-sparse-attention](../13-sparse-attention/)

この系統は複数論文からなる明確な近傍クラスタとしてDiscoveryの昇格ゲートを通過した。単一論文だけを理由に細分化せず、上記の分類境界を維持する。
