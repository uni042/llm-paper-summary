# フレームワーク更新

主要フレームワークの、本質的な機能・性能更新だけを記録します。

## 掲載対象

offload、MoE、expert cache／prefetch、dynamic routing、speculative decoding、quantization、kernel、parallelism、memory management、I/O方式、実質的なhardware性能改善。

## 除外

単なる新モデル対応、allowlist・chat template追加、軽微な互換性変更、bug／crash／correctness／security fixのみの変更。

## 期間別まとめ

- [2026-06-03〜2026-09-03](2026-06-03_to_2026-09-03.md)

## inference engines

- [llama.cpp](inference-engines/llama-cpp/)
- [vLLM](inference-engines/vllm/)
- [SGLang](inference-engines/sglang/)
- [TensorRT-LLM](inference-engines/tensorrt-llm/)
- [KTransformers](inference-engines/ktransformers/)
- [Hugging Face Transformers](inference-engines/hugging-face-transformers/)
- [Accelerate](inference-engines/accelerate/)
- [MLX](inference-engines/mlx/)
- [MLX LM](inference-engines/mlx-lm/)
- [Ollama](inference-engines/ollama/)
- [ExLlama](inference-engines/exllama/)
- [Mistral.rs](inference-engines/mistral-rs/)
- [ONNX Runtime GenAI](inference-engines/onnx-runtime-genai/)
- [OpenVINO GenAI](inference-engines/openvino-genai/)
- [TGI](inference-engines/tgi/)
- [LMDeploy](inference-engines/lmdeploy/)
- [LightLLM](inference-engines/lightllm/)
- [FlexFlow Serve](inference-engines/flexflow-serve/)
- [Modular MAX](inference-engines/modular-max/)

## training frameworks

- [DeepSpeed](training-frameworks/deepspeed/)
- [Megatron-LM](training-frameworks/megatron-lm/)
- [Megatron-Core](training-frameworks/megatron-core/)
- [TorchTitan](training-frameworks/torchtitan/)

## hardware runtimes

- [ROCm](hardware-runtimes/rocm/)


