# Ollama

Ollamaの主要な機能・性能更新を継続的に記録する集約ページです。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

- **2026-06-30 — v0.31.1（released）**: Apple SiliconでMTP draft token数を自動調整。coding-agent benchmark平均で約90%高速化。[release](https://github.com/ollama/ollama/releases/tag/v0.31.1)
- **2026-07-25 — v0.32.4（released）**: MoE packed gate/up projectionを高速化し、M5 Maxで4〜9%改善。[release](https://github.com/ollama/ollama/releases/tag/v0.32.4)
- **2026-08-04 — v0.32.6（released）**: MLX engineがMTP headを自動利用し、Apple GPUでspeculative decodingを自動有効化。数値なし。[release](https://github.com/ollama/ollama/releases/tag/v0.32.6)
- **2026-08-12 — v0.32.10（released）**: global scaleを持つNVFP4 modelのprefillを7〜8%改善。[release](https://github.com/ollama/ollama/releases/tag/v0.32.10)
- **2026-08-19 — v0.32.15（released）**: resolved model metadataをrequest間でcacheし、TTFTを約995→524 msへ短縮。[release](https://github.com/ollama/ollama/releases/tag/v0.32.15)
- **2026-08-21 — v0.33.0（released）**: cancel時に通過済みprefill restore pointを保持し、retryで長いpromptを最初から再計算しないcache復元を追加。[release](https://github.com/ollama/ollama/releases/tag/v0.33.0)
