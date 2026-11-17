# MiniCPM系モデルの公開情報

公式チェックポイントと推論器の先行対応を区別して記録する。

| 確認日 | モデル | 公開状況・留保 | 公式リンク |
|---|---|---|---|
| 2026-10-31 | MiniCPM-OCR 1.0 / MiniCPM-OCR Jev | OCR特化モデル群を共同発表・open source化。MiniCPM-OCR 1.0は1.3Bの文書解析モデル（MiniCPM-V 4.6ベース、SigLIP encoder + Qwen3.5 LM）で、text・表・数式・印影等の構造化抽出を対象とする。Jevは2BのOCR出力品質スコアラ（自動承認 / 人手レビュー振り分け用）。licenseはApache-2.0。GGUF / AWQ / GPTQ版とDSpark draftも配布され、vLLM、SGLang、llama.cpp、Ollamaへ初日から対応。著者評価ではReal5-OmniDocBench 93.68、OCRBench v2 54.7、RTX 5090の明記条件下で1.2 pages/s（いずれもOpenBMB報告値）。context lengthはmodel cardに明記なし。 | https://huggingface.co/openbmb/MiniCPM-OCR-1.0 |
| 2026-10-12 | MiniCPM-V 4.7 35B-A3B | OpenBMBの公式BF16チェックポイントを確認。モデルカード未掲載のためライセンス・性能・文脈長・厳密な有効パラメータ数は未検証。**確認日は公開日を意味しない**。llama.cpp b11551の対応を全形式の完全動作保証と扱わない。 | https://huggingface.co/openbmb/MiniCPM-V-4.7-35B-A3B |
