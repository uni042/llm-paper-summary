# 新LLMリリース一覧

主要LLMの新規公開・一般提供を**model family別**に整理する。

- 初回バックフィル対象: **2026-03-04〜2026-09-05**
- リリース情報の最終確認: **2026-09-08**
- 用語・可読性の最終監査: **2026-09-07**

2026-09-08に主要公式公開を再確認し、既存のQwen3.8-Flash-Nextについてopen-weight構成と主要runtime対応の詳細を補完した。トップ表は各model familyの最新リリースを示すため、Qwen行はより新しいQwen3.8-Max-0902のままとする。

噂・リーク・単なる軽微variantは原則含めない。著名なmodel familyで直近半年に主要リリースがない場合は、その系統自体が一覧から消えないよう**直近の主要モデル1件だけ**を期間外として残す。

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
| 2026-09-03 | GPT-6 Astra | OpenAI GPT | toolを使う長時間task、coding、research、science等を重点にしたGPT-6世代上位APIモデルとして記録。API ID `gpt-6-astra`、最大1.05M-token context / 128K output。 | [OpenAI GPT系](openai-gpt.md) |
| 2026-09-02 | Qwen3.8-Max-0902 | Qwen | 2.4T級MoEを基盤とするQwen3.8-MaxのAPI snapshot。1M contextとtext / image / video入力を維持し、coding・長時間tool taskを更新。0902自体のopen-weight checkpointとは区別。 | [Qwen系](qwen.md) |
| 2026-09-02 | Gemini 3.8 Flash | Gemini | text / image / audio / video入力、1M input context、64K outputを持つ高速汎用APIモデル。coding・agent task・multi-step reasoningを更新。 | [Gemini系](gemini.md) |
| 2026-09-02 | Muse Spark 1.3 | Meta Muse | codingとエージェント型タスク（agentic tasks）を更新し、Muse Code / Meta APIへ展開されたMuse Spark系モデル。 | [Meta Muse系](meta-muse.md) |
| 2026-08-26 | GLM-5.3-Flash | GLM | 総320B / 約18B activeのnative multimodal MoE。sparse / linear attentionを組み合わせ、長context時のattention計算とKV増加を抑える設計。 | [GLM系](glm.md) |
| 2026-09-01 | Claude Fable 5.1 / Mythos 5.1 | Claude | coding・knowledge work・scienceなど長いmulti-step task向けの上位model群。Mythosはcybersecurity / biology等の専門領域を重点化。 | [Claude系](claude.md) |
| 2026-08-21 | DeepSeek-V4-Flash-Vision-Exp | DeepSeek | V4-Flash系へimage入力を統合した**experimental** multimodal model。production modelとは分けて記録。 | [DeepSeek系](deepseek.md) |
| 2026-08-12 | Grok 4.6 | Grok | 長時間agent、coding、visual / interactive taskを重点にした上位model。最大500K-token context。 | [Grok系](grok.md) |
| 2026-07-16 | Kimi K3 | Kimi | 総2.8T、896 routed experts、16 experts/tokenのopen-weight native multimodal MoE。1M contextでimage / videoと長時間coding taskを対象。 | [Kimi系](kimi.md) |
| 2026-06-03 | Gemma 4 12B Unified | Gemma | Gemma 4世代の12B級open-weight Unified model。大規模MoEよりweight規模が小さく、量子化時のローカル利用も検討しやすい帯域。 | [Gemma系](gemma.md) |
| 2026-06-01 | MiniMax M3 | MiniMax | 1M contextとimage / video入力を持つopen-weight multimodal model。coding・multi-step agent workを対象。 | [MiniMax系](minimax.md) |
| 2026-04-28 | Mistral Medium 3.5 | Mistral | 256K context、multimodal対応、open weightsを持ち、coding / tool利用を主対象とするMistral系モデル。 | [Mistral系](mistral.md) |
| 2026-03-04 | Phi-4-reasoning-vision-15B | Phi | 約15B parameterのopen-weight multimodal reasoning model。math / science、UI・image理解を重点対象。 | [Phi系](phi.md) |
| 2025-04-05 | Llama 4 Scout / Maverick | Llama | **期間外最新**。Meta Llama初のnative multimodal MoE世代。Scout / Maverickとも約17B activeでopen weights。 | [Llama系](llama.md) |

## 系統別ページ

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
