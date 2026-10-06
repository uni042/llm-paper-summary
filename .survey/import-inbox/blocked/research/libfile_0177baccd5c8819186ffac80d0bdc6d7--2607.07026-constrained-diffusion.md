---
canonical_id: "arXiv:2607.07026"
title: "Constrained Decoding for Diffusion Language Models via Efficient Inference over Finite Automata"
summary: "本論文は有限オートマトンで表現できる制約の下で、拡散言語モデルのmean-field分布を厳密に条件付けしてsamplingするアルゴリズムを提案する。automatonをgraphical modelとして扱い、parallel/block-wise decodingや任意remasking scheduleと両立し、回路深さ削減でsampling depthを系列長の線形から対数へ短縮する。Dream-7BのBFCL-Liveではgreedy accuracyを63.9%から71.5%、stochastic samplingを22.3%から69.0%へ改善し、wall-clock overheadは5%未満である。"
list_summary: "有限オートマトン制約を拡散言語モデルのmean-field posteriorへ厳密に組み込み、並列復号を保ったままJSON等の構造制約を保証する。"
authors: ['Meihua Dang', 'Stefano Ermon']
published: "2026-07-08"
publication: "arXiv"
publication_type: "preprint"
publication_status: "preprint"
source: "https://arxiv.org/abs/2607.07026"
sources: ["https://arxiv.org/abs/2607.07026"]
implementation: "一次資料本文に基づき提案手法と評価を整理。 確認した一次資料から公式コードURLは特定できなかった。"
code: null
last_checked: "2026-10-06"
arxiv_id: "2607.07026"
arxiv_categories:
  primary: "cs.LG"
  cross_list: []
worker_completed_at: "2026-10-06T19:35:00+09:00"
worker_run_key: "20261006-1900-scheduled-chat-00/r01"
reference_main_sha: "174b4002a423363e19f2224834cbb596437d38d6"
last_audited: null
audit_version: 0
---

## 概要

構造化出力、function calling、SQL生成では、生成文字列がJSON schemaや文法上の制約を必ず満たす必要がある。自己回帰モデルでは次トークン候補を左から右へmaskすればよいが、拡散言語モデルは複数位置を同時標本するため、各位置を独立にmaskすると位置間依存を満たせない。

本論文は有限オートマトン（finite automaton）で表現できる任意制約について、拡散モデルが各位置へ与えるfactorized分布を制約条件で厳密に条件付けする。automatonをgraphical モデルとして動的計画法で推論し、greedyとsamplingの双方、並列/ブロック-wise 復号、任意remasking scheduleへ適用する。Dream-7BのBFCL-Liveではgreedy accuracy 63.9%→71.5%、stochastic 22.3%→69.0%で、実時間 オーバーヘッドは5%未満である。

## 問題設定

自己回帰制約復号は接頭辞状態から「次に許されるトークン集合」を計算できる。しかしDLMの1 段階では複数位置が同時に変わり、それぞれを独立に許可しても、全系列としてautomatonがacceptする保証はない。全候補系列を列挙すれば指数的になる。

必要なのは、各位置のmean-field probabilityを保ちながら、系列全体がautomatonを通過する条件付き分布から効率よく標本する方法である。

## 手法

### automatonをgraphical model化

制約automatonの状態を隣接位置間の潜在状態として置き、各トークンが状態 transitionを表すfactorになる。これにより「系列がaccept 状態へ到達する」という大域制約をchain構造のメッセージ passingとして計算できる。

### constrained mean-field posterior

DLMが各位置へ出す独立トークン確率とautomaton transitionを掛け合わせ、順伝播/逆伝播 メッセージで各位置・遷移の条件付き分布を求める。単なるinvalid トークン maskではなく、後続位置で制約を完了できるかまで含めた厳密posteriorとなる。

### 並列sampling

素朴には左から右にautomaton 状態を標本するため深さが系列長に比例する。論文は算術回路の深さ reductionを応用し、積の結合順序を木構造化してsampling 深さを対数へ短縮する。これによりDLM本来の並列復号を大きく壊さない。

### remaskingとの互換性

各denoising 段階で確定・再maskされる位置集合が変わっても、残る未知位置に対してautomaton推論を再構成できるため、ブロック-wiseや任意remasking scheduleへ適用できる。

## 評価条件

| 項目 | 内容 |
|---|---|
| モデル | Dream-7B、LLaDA-8B |
| タスク | xLAM/BFCL function calling、Sudoku/Countdown、Spider、GSM-Symbolic |
| 制約 | 有限オートマトンで表現可能な構造 |
| 指標 | タスク accuracy、constraint satisfaction、実時間 オーバーヘッド |
| 復号 | greedy / stochastic、並列 / ブロック-wise |

## 主要結果

BFCL-LiveのDream-7Bではgreedy accuracyが63.9%から71.5%、stochastic samplingが22.3%から69.0%へ上がる。特にunconstrained stochastic samplingが構造違反で崩れる条件で差が大きい。実時間 オーバーヘッドは5%未満と報告され、制約保証のために自己回帰化する方式よりDLMの並列性を維持する。

## 既存研究との差

従来のguided generationは自己回帰接頭辞に対するnext-トークン maskが中心である。本方式は複数位置の共同 constraintをautomaton 状態で結び、factorized DLM proposalを厳密な制約posteriorへ変換する。heuristicなrepairではなく、有限オートマトン範囲では制約充足を構成上保証する。

## 限界

扱える制約は有限オートマトンで表現できる範囲が中心で、一般の文脈自由文法をそのまま扱う結果ではない。automaton 状態数が大きい複雑schemaではメッセージ passing コストが増える。5%未満のオーバーヘッドは評価したモデル/タスク条件での値である。

## 一次資料

- https://arxiv.org/abs/2607.07026