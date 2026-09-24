# Meta Muse系 LLMリリース

Meta Superintelligence LabsのMuse系主要モデルを新しい順に記録する。初回バックフィル対象期間: **2026-03-04〜2026-09-05**。

Muse系はmodel capabilityだけでなく、**どのproduct / APIで使えるか、public previewか一般提供か**を分けて記録する。

| リリース日 | モデル | 簡単な説明 | 公式リンク |
|---|---|---|---|
| 2026-09-02 | Muse Spark 1.3 | codingとエージェント型タスク（agentic tasks）を中心に更新したMuse Spark系モデル。Muse CodeとMeta APIへ展開され、file編集・tool利用・複数step実行を伴うpersonal-agent系productの基盤として利用される位置づけ。 | https://ai.meta.com/ |
| 2026-07-09 | Muse Spark 1.1 | tool / computer use、coding、multimodal理解を強化した更新。Meta Model APIで**公開preview（public preview）**として提供され、stable一般提供とは区別する。 | https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/ |
| 2026-04-08 | Muse Spark | Metaのpersonal superintelligence路線に向けたMuse model familyの初期モデル。単発chatだけでなく、利用者の作業を継続的に補助するagent用途を主眼として記録。 | https://ai.meta.com/blog/ |

## 用語メモ

- **エージェント型タスク（agentic tasks）**: plan作成、tool呼び出し、結果確認、再試行を複数step行うtask。
- **computer use（コンピュータ操作）**: browserやdesktop UIをmodelが操作し、click・入力・画面確認を繰り返す能力。
- **公開preview（public preview）**: 一般利用者が試せるが、正式提供までにAPI・model仕様が変わる可能性がある段階。
- **personal agent（個人向けagent）**: 利用者のcontextやtoolへ接続し、複数回の操作を通じてtaskを完了するassistant型system。

MuseのAPI提供状況とweight公開は別問題なので、open-weight提供が確認された場合は個別に明記する。
