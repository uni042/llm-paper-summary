# 新LLMリリース一覧

主要LLMの新規公開・一般提供を**model family別**に整理する。

- 初回バックフィル対象: **2026-03-04〜2026-09-05**
- リリース情報の最終確認: **2026-11-26**
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
| 2026-11-18 | Gemini 4 Neon | Gemini | Gemini 4世代の新モデル。最大1M-token context、入力$3 / 出力$15。複雑なcoding・分析・科学workflow向けで、高速なtask完了を重視。 | [Gemini系](gemini.md) |
| 2026-11-17 | Microsoft MAIモデル群 | Microsoft MAI | Ignite 2026で7モデルを発表。MAI Code 2 / Code 2 FlashとDecision 1.1が一般提供。数値はMicrosoft報告値。 | [Microsoft MAI系](microsoft-mai.md) |
| 2026-11-17 | GPT-6.2 Astra / Sol | OpenAI GPT | GPT-6世代の更新。Astraは入力$8 / 出力$40へ20%値下げし、ChatGPT Work / CodexとAPIで提供（通常のChatには追加されない）。最大1,050,000-token context。 | [OpenAI GPT系](openai-gpt.md) |
| 2026-11-16 | Qwen4-Max | Qwen | Qwen4世代flagshipの一般提供。最大1M-token context、text / image / video入力。重み非公開・fine-tuning不可のAPI専用。 | [Qwen系](qwen.md) |
| 2026-11-16 | Liquid AI d1.2 / d1.2-ultra | Liquid AI | 判断モデルの新版。音声入力と新task 5種を追加したhostedモデル（重み非公開）。旧d1系は非推奨化。 | [Liquid AI系](liquid-ai.md) |
| 2026-11-12 | Gemini 4 Hydrogen | Gemini | 高速・実行tierの新モデル。最大1M-token context、一律価格$1.50 / $7.50。SearchのAI Modeで3.8 Flashのデフォルトを置換。 | [Gemini系](gemini.md) |
| 2026-11-09 | Claude Fable 5.2 / Mythos 5.2 | Claude | 同一基盤の2構成。Fableは一般提供、Mythosは審査済み組織向け。$8 / $40へ値下げし出力は最大30%高速（Anthropic報告）。 | [Claude系](claude.md) |
| 2026-11-09 | Muse Ember | Meta Muse | Muse系最小のclosedモデル。agentの反復作業向けで、1,048,576-token context、$0.10 / $0.50。 | [Meta Muse系](meta-muse.md) |
| 2026-11-04 | Kimi K3.1 Pro | Kimi | K3の事後学習強化版の重みを公開。総2.8T / 有効104B、MXFP4重み約1.56TB、最大1,048,576-token context。 | [Kimi系](kimi.md) |
| 2026-11-04 | Ripple-65B Preview | Recursive | Ricursive Intelligence初の汎用公開モデル。65B dense、Apache-2.0、最大1,048,576-token context。 | [Recursive系](recursive.md) |
| 2026-10-29 | Mistral Large 4（重み公開） | Mistral | previewを経て改良版checkpointの重みを公開しopen-weight化。約1.05T / 52B active、最大1M-token context。 | [Mistral系](mistral.md) |
| 2026-10-15 | Nemotron 3.5 Super VL | NVIDIA Nemotron | 総120B / 有効12Bのopen-weight視覚言語MoE。Mamba-2 / TransformerとC-RADIOを組み合わせ、最大1M context。 | [NVIDIA Nemotron系](nvidia.md) |
| 2026-10-15 | Nemotron 3.5 Bolt 74B-A9B 24GB | NVIDIA Nemotron | 総74B / 有効9Bの視覚言語MoE。24GB GPU向け設計値と約25GBの配布ファイル表示を区別する。 | [NVIDIA Nemotron系](nvidia.md) |
| 2026-09-20 | Step 5 Preview | StepFun | 総600B / 有効27Bの疎MoE。公式BF16重みのrepo commitは2026-09-20、最大1M context。画像入力は仕様表に記載。 | [StepFun系](stepfun.md) |
| 2026-11-23 | GLM-5.4 | GLM | GLM系初のLoop Transformer flagship。750B規模baseの28層を2回反復しparameter増なしで推論深度を増やす。hybrid KV cacheとsparse attention index再利用で1M context対応。GLM Coding Planで提供。 | [GLM系](glm.md) |
| 2026-10-17 | DeepSeek-V4.1-Flash-1017 | DeepSeek | 10月17日に公式更新されたAPI snapshot。APIのmodel IDは`deepseek-flash`のまま。公式公表ベンチマークはタスクごとの条件付き比較で、hardware実測tokens/sの倍率とは区別する。 | [DeepSeek系](deepseek.md) |
| 2026-08-12 | Grok 4.6 | Grok | 長時間agent、coding、visual / interactive taskを重点にした上位model。最大500K-token context。 | [Grok系](grok.md) |
| 2026-06-03 | Gemma 4 12B Unified | Gemma | Gemma 4世代の12B級open-weight Unified model。大規模MoEよりweight規模が小さく、量子化時のローカル利用も検討しやすい帯域。 | [Gemma系](gemma.md) |
| 2026-06-01 | MiniMax M3 | MiniMax | 1M contextとimage / video入力を持つopen-weight multimodal model。coding・multi-step agent workを対象。 | [MiniMax系](minimax.md) |
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
