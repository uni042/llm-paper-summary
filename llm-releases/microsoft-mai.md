# Microsoft MAI系モデル

Microsoft AI（MAI）が開発するタスク特化型モデル系列の主要リリースを新しい順に記録する。いずれも重み非公開のhostedモデルであり、価格・性能の数値はMicrosoft報告値で独立検証ではない。

## MAIモデル群（2026-11-17、Ignite 2026）

Microsoft Ignite 2026で7モデルを同時発表した。

- **MAI Code 2 / Code 2 Flash**: agentic coding向けのflagship系列。GitHub Copilotで一般提供され、Foundryでも提供（Code 2 FlashのFoundry提供は限定preview）。Microsoftによれば、日常的なenterprise codingのbenchmark平均でCode 2はGPT-6.1 Solの98%の性能を40%のコストで、Claude Opus 5.5比では96%の性能を5%のコストで達成する（同社報告値）。基礎科学や長時間のagent作業には未調整と明記されている。
- **Microsoft-Decision-1.1**: routing・分類・優先順位付けなどの判断向け小型モデル。Foundryで一般提供。Artificial Analysis Decision Indexで競合を上回るとMicrosoftは主張する。入力価格は一次資料で未確認のため記載しない。
- **MAI Cyber 2 Flash**: cybersecurity向け。CyberGym-E2EでGPT-6 Astraを上回り、taskあたりコストは2%未満とされる（同社報告値）。
- **MAI Image 2.7**: 画像生成・編集向け。画像編集で世界1位と主張する（同社報告値）。
- **MAI Realtime 1**: speech-to-speech向け。
- **MAI Transcribe 2**: 文字起こし向け。Dragon Copilotで月1,000万件の診療encounterへ展開済みで、error rateが半減したとされる（同社報告値）。
- あわせて **MAI Licensed Weights**（信頼済み顧客がFrontier Co.経由でMAIモデルの重みライセンスを受け、自社Azure環境でカスタマイズ・運用する仕組み）を発表した。

## 一次資料

- [Microsoft公式ブログ: Ignite 2026: Building the frontier ecosystem](https://blogs.microsoft.com/blog/2026/11/17/ignite-2026-building-the-frontier-ecosystem/?ocid=FY27_soc_omc_br_LI_OMB)
- [Microsoft AI: MAI keynote transcript](https://microsoft.ai/news/microsoft-ignite-2026-mai-keynote/?ref=creativestrategies.com)
