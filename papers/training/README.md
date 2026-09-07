# 学習システム研究

収録論文: **18本**。

事前学習（pre-training）、追加学習（fine-tuning）、分散学習、最適化状態（optimizer state）・活性値（activation）・パラメータ（parameter）のメモリ管理など、**モデルを学習・更新する工程そのものを高速化したり、必要なGPUメモリを減らしたりする研究**を収録する。

推論を速くするための補助モデルや予測器を途中で学習する研究は、学習工程そのものの効率化が目的ではないためここには置かない。最終目的が推論なら `inference/` に分類する。

各系統READMEには、その系統が「何を動かす・分ける・省く・重ねる研究なのか」と、収録する全論文の一文説明を掲載する。TransformerやMoEのような基礎概念以外は、個別論文の名称だけに頼らず、初見でも処理内容が追える表現にする。

## 系統

- [Training Offload / Memory Systems](01-training-offload-memory-systems/) — 13本
  - 学習中にGPUへ置ききれない活性値、最適化状態、パラメータなどをCPUメモリやSSDへ一時退避する方式に加え、CPU DRAMをモデル状態の正本として必要な層だけGPUへ送る方式も扱う。データ転送や最適化器更新をGPU計算と同時進行させ、限られたGPUメモリで大規模モデルを学習する研究を含む。
- [Distributed / Heterogeneous MoE Training](02-distributed-heterogeneous-moe-training/) — 5本
  - MoEのエキスパート（expert）をどのGPUへ置くか、人気expertを何個複製するか、tokenをGPU間でどう通信するか、性能の異なるGPUへどう役割分担させるかを調整し、大規模MoE学習の待ち時間を減らす研究を含む。
