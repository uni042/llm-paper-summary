# 新LLMリリース一覧

主要LLMの新規公開・一般提供を**系統別**に整理する。原則として直近約半年（初回バックフィル: **2026-03-04〜2026-09-05**）の主要リリースを収録する。噂・リーク・単なる軽微variantは含めない。

著名なモデル系統で直近半年に主要リリースがない場合は、その系統が一覧から消えないよう**最新の主要モデル1件だけ**を掲載する。

## 各系統の最新リリース

| リリース日 | モデル | 系統 | 概要 | 詳細 |
|---|---|---|---|---|
| 2026-09-03 | GPT-6 Astra | OpenAI GPT | GPT-6世代flagship。computer use・coding・research・science・professional workを強化し、API modelは`gpt-6-astra`。 | [OpenAI GPT系](openai-gpt.md) |
| 2026-09-02 | Qwen3.8-Max-0902 | Qwen | 2.4T級Qwen3.8-Maxの重要snapshot。coding / cowork / long-horizon agent / multimodal understandingを強化し、1M contextを維持。 | [Qwen系](qwen.md) |
| 2026-09-02 | Gemini 3.8 Flash | Gemini | coding、agentic tasks、multi-step reasoningを強化した1M-context multimodal workhorse。 | [Gemini系](gemini.md) |
| 2026-09-02 | Muse Spark 1.3 | Meta Muse | coding・agentic tasksを強化したMuse Spark更新。Muse CodeとMeta APIへ展開。 | [Meta Muse系](meta-muse.md) |
| 2026-09-02 | GLM-5.3-Flash | GLM | 320B total / 18B activeのnative multimodal MoE。efficient long-context / agent用途。 | [GLM系](glm.md) |
| 2026-09-01 | Claude Fable 5.1 / Mythos 5.1 | Claude | coding・knowledge work・科学研究を中心に更新されたAnthropic上位モデル。 | [Claude系](claude.md) |
| 2026-08-21 | DeepSeek-V4-Flash-Vision-Exp | DeepSeek | V4-Flashへvision inputを統合したexperimental multimodal model。 | [DeepSeek系](deepseek.md) |
| 2026-08-12 | Grok 4.6 | Grok | long-running agents、coding、visual workを強化した最新flagship。 | [Grok系](grok.md) |
| 2026-07-16 | Kimi K3 | Kimi | 2.8T open-weight native multimodal MoE、1M context。 | [Kimi系](kimi.md) |
| 2026-06-03 | Gemma 4 12B Unified | Gemma | Gemma 4世代の12B級Unified open model。 | [Gemma系](gemma.md) |
| 2026-06-01 | MiniMax M3 | MiniMax | coding・agentic work・1M context・native multimodalityを統合したopen-weight model。 | [MiniMax系](minimax.md) |
| 2026-04-28 | Mistral Medium 3.5 | Mistral | agentic / coding向けfrontier-class multimodal open-weight model。 | [Mistral系](mistral.md) |
| 2026-03-04 | Phi-4-reasoning-vision-15B | Phi | 15B open-weight multimodal reasoning model。 | [Phi系](phi.md) |
| 2025-04-05 | Llama 4 Scout / Maverick | Llama | **期間外最新**。Metaのnative multimodal MoE Llama。 | [Llama系](llama.md) |

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

各モデルについて最低限、**モデル名 / リリース日 / 簡単な説明 / 公式リンク**を記録する。各系統ページは新しい順に並べ、新規モデル追加時はこのトップページの「各系統の最新リリース」も必ず更新する。

open-weightモデルでは、重要な場合に総パラメータ数、active parameters、context length、modal対応、ライセンス、入手方法、llama.cpp / Ollama / vLLM対応状況、量子化時のメモリ目安も追記する。
