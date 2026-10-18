# NVIDIA Nemotron系 LLMリリース

NVIDIAが公開するNemotron系モデルを記録する。総パラメータ数とtokenごとの有効パラメータ数、配布サイズと推論時メモリ、公式ベンチマークの条件を分けて読む。

| 公開日 | モデル | 構成・用途 | 提供・ライセンス |
|---|---|---|---|
| 2026-10-15 | Nemotron 3.5 Super VL | 総120B / 有効12B。Mamba-2とTransformerを組み合わせたMoEにC-RADIO視覚encoderを接続。最大1M context。画像・文書・表・図表・動画の理解、tool calling、reasoning mode、MTPに対応。 | BF16 / NVFP4 checkpoint、LiLiCorr draft model。OpenMDW v1.1。公式資料：[発表](https://blogs.nvidia.com/blog/nemotron-3-5-super-vl/)、[技術概要](https://developer.nvidia.com/blog/nvidia-nemotron-3-5-super-vl-powers-specialized-agents-with-multimodal-reasoning/)、[BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-BF16)、[NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-NVFP4)。
| 2026-10-15 | Nemotron 3.5 Bolt 74B-A9B 24GB | 総74B / 有効9Bの圧縮・追加学習版視覚言語MoE。公式GGUFはexpert重みにIQ2_XXS、他層にNVFP4 / Q8_0を組み合わせる。最大256K context。 | 24GB GPU向けは設計目標であり、Ollama配布ファイル表示は約25GB。長文脈・画像・draftの追加memoryを含む実測ではない。Apple Silicon / Metal非対応の案内あり。12GB VRAMへ全weightは載らず、CPU RAM退避を含む構成検討が必要。[公式発表](https://blogs.nvidia.com/blog/nemotron-3-5-super-vl/)、[Ollama](https://ollama.com/library/nemotron-3.5-bolt)、[GGUF](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-24GB-GGUF)。

## 性能値の読み方

NVIDIAはSuper VLについて同規模open-weight modelとの比較でagentic処理throughput最大5倍、LiLiCorrをDGX Sparkで使う場合に投機なしdecode比で最大2.3倍を報告する。別のDynamo評価は16基のB200と利用者当たり50 token/sの条件で同時利用者最大8倍、TTFT 85%減を報告する。これらは別々の特定条件であり、Windows / RTX 4070 SUPER 12GBの性能値や同一構成で同時に得られる倍率ではない。

重み公開（open-weight）はopen sourceと同じ意味ではない。利用前に個別licenseを確認する。context上限だけから実利用可能なsequence長や速度を判断せず、KV cache、GPU memory、runtime設定を含めて測定する。
