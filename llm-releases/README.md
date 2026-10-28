# 新LLMリリース一覧

主要LLMの新規公開・一般提供を**model family別**に整理する。

- 初回バックフィル対象: **2026-03-04〜2026-09-05**
- リリース情報の最終確認: **2026-10-22**
- 用語・可読性の最終監査: **2026-09-07**

2026-09-24に主要提供元の公式公開を再確認し、OpenAIのGPT-6 Sol / LunaとAnthropicのClaude Opus 5.5を追加した。GPT-6 Sol / LunaはAstra世代の能力をより低cost帯へ展開し、Claude Opus 5.5はOpus 5比の性能・効率・安全性を更新する。トップ表は各model familyの最新リリースを示す。

噂・リーク・単なる軽微variantは原則含めない。著名なmodel familyで直近半年に主要リリースがない場合は、その系統自体が一覧から消えないよう**直近の主要モデル1件だけ**を期間外として残す。

2026-10-22の確認でRecursive Flint 40B-A2.5Bを追加した。公式BF16配布、Apache-2.0、モデル規模とcontext設定、Ollama v0.40.8のmacOS限定対応を分けて記録する。

## この一覧の読み方

modelを比較するときは「flagship」「frontier」のような宣伝上の呼称だけでなく、以下を分けて見る。

- **API modelか重み公開（open-weight）か**: 自前hardwareへdownloadできるか
- **denseかMoEか**: 全weightを毎token使うか、一部expertだけ使うか
- **総パラメータ数（total parameters） / 有効パラメータ数（active parameters）**: 保存容量とtokenごとの主な演算量を分ける
- **文脈長（context length）**: 1 requestで参照できるtoken履歴の上限
- **マルチモーダル（multimodal）**: text以外にimage / audio / video等を扱えるか
- **提供段階**: 正式提供、preview、public beta、experimentalを区別する
- **tool / agent用途**: code生成だけか、browser・terminal・file等を使うmulti-step taskまで想定するか

## 各系統の最新リリース

| リリース日 | モデル | 系統 | 概要 | 詳細 |
|---|---|---|---|---|
| 2026-10-27 | Liquid AI LFM3 / d1 | Liquid AI | 1.73B text tri-hybridを含む用途別6派生とbase。text modelは256K context、LFM Open License v1.0。Ollama v0.40.12のLFM3/d1 2B対応はApple hardware限定。 | [Liquid AI系](liquid-ai.md) |
| 2026-10-21 | Recursive Flint 40B-A2.5B | Recursive | 総39.8B / 有効約2.5BのApache-2.0 MoE。公式BF16 checkpointは約80GB、設定上の最大262K context。Ollama対応はmacOS限定。 | [Recursive系](recursive.md) |
| 2026-10-15 | Nemotron 3.5 Super VL | NVIDIA Nemotron | 総120B / 有効12Bのopen-weight視覚言語MoE。Mamba-2 / TransformerとC-RADIOを組み合わせ、最大1M context。 | [NVIDIA Nemotron系](nvidia.md) |
| 2026-10-15 | Nemotron 3.5 Bolt 74B-A9B 24GB | NVIDIA Nemotron | 総74B / 有効9Bの視覚言語MoE。24GB GPU向け設計値と約25GBの配布ファイル表示を区別する。 | [NVIDIA Nemotron系](nvidia.md) |
| 2026-09-23 | GPT-6 Sol / Luna | OpenAI GPT | GPT-6 Astraで導入したprofessional work、factuality、coding、computer use等の改善を高速・低cost帯へ展開。API IDは`gpt-6-sol` / `gpt-6-luna`。GPT-5.6のpromotional pricing比でSol / Lunaとも大幅に低価格化。 | [OpenAI GPT系](openai-gpt.md) |
| 2026-09-02 | Qwen3.8-Max-0902 | Qwen | 2.4T級MoEを基盤とするQwen3.8-MaxのAPI snapshot。1M contextとtext / image / video入力を維持し、coding・長時間tool taskを更新。0902自体のopen-weight checkpointとは区別。 | [Qwen系](qwen.md) |
| 2026-09-20 | Step 5 Preview | StepFun | 総600B / 有効27Bの疎MoE。公式BF16重みのrepo commitは2026-09-20、最大1M context。画像入力は仕様表に記載。 | [StepFun系](stepfun.md) |
| 2026-09-15 | Gemini 3.8 Live / Live Extended Thinking | Gemini | Live API向けaudio-to-audioモデル。標準Liveは低latencyのreal-time dialogue、Extended Thinkingはlive audio中のbackground reasoningを重視する。両方とも一般提供（GA）。 | [Gemini系](gemini.md) |
| 2026-10-15 | Muse Spark Open | Meta Muse | 総816B / 有効42B、256 expertsから8を選ぶopen-weight multimodal MoE。最大1M context。NVFP4/BF16重みのGPU memory要件は700GB / 2TBと公式案内。 | [Meta Muse系](meta-muse.md) |
| 2026-08-26 | GLM-5.3-Flash | GLM | 総320B / 約18B activeのnative multimodal MoE。sparse / linear attentionを組み合わせ、長context時のattention計算とKV増加を抑える設計。 | [GLM系](glm.md) |
| 2026-09-22 | Claude Opus 5.5 | Claude | Claude 5.5 familyの最初のmodel。Opus 5からagentic coding、computer use、knowledge work、効率、安全性を更新し、通常workloadで約40%低cost、出力速度も30%以上高速化とAnthropicが報告。 | [Claude系](claude.md) |
| 2026-10-17 | DeepSeek-V4.1-Flash-1017 | DeepSeek | 10月17日に公式更新されたAPI snapshot。APIのmodel IDは`deepseek-flash`のまま。公式公表ベンチマークはタスクごとの条件付き比較で、hardware実測tokens/sの倍率とは区別する。 | [DeepSeek系](deepseek.md) |
| 2026-08-12 | Grok 4.6 | Grok | 長時間agent、coding、visual / interactive taskを重点にした上位model。最大500K-token context。 | [Grok系](grok.md) |
| 2026-07-16 | Kimi K3 | Kimi | 総2.8T、896 routed experts、16 experts/tokenのopen-weight native multimodal MoE。1M contextでimage / videoと長時間coding taskを対象。 | [Kimi系](kimi.md) |
| 2026-06-03 | Gemma 4 12B Unified | Gemma | Gemma 4世代の12B級open-weight Unified model。大規模MoEよりweight規模が小さく、量子化時のローカル利用も検討しやすい帯域。 | [Gemma系](gemma.md) |
| 2026-06-01 | MiniMax M3 | MiniMax | 1M contextとimage / video入力を持つopen-weight multimodal model。coding・multi-step agent workを対象。 | [MiniMax系](minimax.md) |
| 2026-10-06 | Mistral Large 4 | Mistral | 1T total / 49B activeのnative multimodal flagship。APIはpublic preview、weightsは2026年10月末公開予定で、現時点ではopen-weight配布済みではない。 | [Mistral系](mistral.md) |
| 2026-03-04 | Phi-4-reasoning-vision-15B | Phi | 約15B parameterのopen-weight multimodal reasoning model。math / science、UI・image理解を重点対象。 | [Phi系](phi.md) |
| 2025-04-05 | Llama 4 Scout / Maverick | Llama | **期間外最新**。Meta Llama初のnative multimodal MoE世代。Scout / Maverickとも約17B activeでopen weights。 | [Llama系](llama.md) |

## 系統別ページ

- [Liquid AI系](liquid-ai.md)
- [Recursive系](recursive.md)
- [Qwen系](qwen.md)
- [Llama系](llama.md)
- [OpenAI GPT系](openai-gpt.md)
- [Claude系](claude.md)
- [Gemini系](gemini.md)
- [Gemma系](gemma.md)
- [DeepSeek系](deepseek.md)
- [Mistral系](mistral.md)
- [Grok系](grok.md)
- [Kimi系](kimi.md)
- [GLM系](glm.md)
- [MiniMax系](minimax.md)
- [Phi系](phi.md)
- [Meta Muse系](meta-muse.md)
- [StepFun系](stepfun.md)
- [NVIDIA Nemotron系](nvidia.md)

## 更新ルール

各modelについて最低限、**model名 / release日 / 何が変わったか / 提供形態 / 公式link**を記録する。各系統ページは新しい順に並べ、新規model追加時はこのトップページの「各系統の最新リリース」も必ず更新する。

重み公開（open-weight）modelでは、重要な場合に以下も追記する。

- 総parameter数とactive parameters
- expert数 / Top-k routingなどMoE構造
- context length
- vision / audio / video対応
- license
- Hugging Face / ModelScope等の入手先
- llama.cpp / Ollama / vLLM等の主要runtime対応状況
- 量子化時のRAM / VRAM目安

### 用語上の方針

- **open-weight** と **open source** を同義にしない。
- **total parameters** と **active parameters** を混同しない。
- 「agentic」「frontier」「workhorse」だけで説明を終えず、何をするmodelなのかを具体化する。
- preview / beta / experimentalの性能値や提供条件をstable releaseと混同しない。
- context lengthが大きくても、実際に長contextを高速に動かせるかはKV cache、runtime、hardware memoryに依存することを必要に応じて明記する。
