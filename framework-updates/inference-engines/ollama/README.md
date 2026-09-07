# Ollama

Ollamaの主要な機能・性能更新を継続的に記録する集約ページ。Apple Silicon向け投機的デコード（speculative decoding）、MoE kernel、低bit model、model metadata cache、prefill cacheなど、ローカルLLM実行時の速度・memory・再試行costへ影響する変更を扱う。

## 初期収録期間

2026-06-03〜2026-09-03

## 主要更新

### 2026-06-30 — v0.31.1（released）

- **Apple SiliconでMTP draft token数を自動調整**: MTP（Multi-Token Prediction; 複数token予測）headが一度に何token候補を先読みするかを固定せず、実行状況に応じて調整する。

  draft tokenを増やせば本体modelを呼ぶ回数を減らせる可能性がある一方、外れ候補が多ければ無駄な検証が増える。そのため「多いほどよい」のではなく、受理されやすさとdraft costのbalanceを取る。

  coding-agent benchmark平均で約 **90%高速化**を報告。[release](https://github.com/ollama/ollama/releases/tag/v0.31.1)

### 2026-07-25 — v0.32.4（released）

- **MoE gate/up projection高速化**: MoE expert内で並行して計算するgate projectionとup projectionのweight配置・matrix処理をpacked化し、memory accessとkernel overheadを削減。M5 Maxで **4〜9%改善**。[release](https://github.com/ollama/ollama/releases/tag/v0.32.4)

### 2026-08-04 — v0.32.6（released）

- **MLX engineがMTP headを自動利用**: modelにMTP headが含まれている場合、Apple GPU上で投機的デコードを自動有効化する。利用者がdraft modelを別途指定しなくても、model自身の複数token予測headをdraftとして使える。公式速度値なし。[release](https://github.com/ollama/ollama/releases/tag/v0.32.6)

### 2026-08-12 — v0.32.10（released）

- **NVFP4 modelのprefill高速化**: NVIDIAの4-bit浮動小数点形式NVFP4で、weight全体に共通するglobal scaleを持つmodelのprefill pathを最適化。prompt処理を **7〜8%改善**。[release](https://github.com/ollama/ollama/releases/tag/v0.32.10)

### 2026-08-19 — v0.32.15（released）

- **resolved model metadataのrequest間cache**: model fileやtemplate、parameter設定など、requestごとに同じmodelについて繰り返し解決していたmetadataをcacheする。

  GPU推論そのものを速くする変更ではないが、request開始前の準備時間を減らし、TTFT（Time To First Token; 最初のtokenが返るまでの時間）を約 **995 → 524 ms**へ短縮。[release](https://github.com/ollama/ollama/releases/tag/v0.32.15)

### 2026-08-21 — v0.33.0（released）

- **cancel後のprefill restore point保持**: 長いpromptをprefill中にrequestがcancelされても、すでに計算済みの地点をcacheとして残す。

  同じpromptでretryした場合、最初のtokenからKVを作り直さず、保存済み地点から再開できる。coding agentやtool loopのように同じ長いcontextを再送しやすいworkloadで再計算を減らす。[release](https://github.com/ollama/ollama/releases/tag/v0.33.0)

### 用語メモ

- **MTP（Multi-Token Prediction; 複数token予測）**: 現在位置から次の1 tokenだけでなく複数token先まで候補を予測するhead / 学習方式。
- **prefill**: prompt全体を一括処理してKV cacheを作る段階。長いpromptではdecode開始前の大きなcostになる。
- **restore point**: 途中まで計算済みのcache状態を保存し、次回その地点から再開するためのcheckpoint。
- **metadata cache**: model weightそのものではなく、modelをどう読み込むか・どのtemplateや設定を使うかといった付随情報を再利用するcache。
