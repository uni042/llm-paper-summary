---
canonical_id: "arXiv:2402.10517"
title: "Any-Precision LLM: Low-Cost Deployment of Multiple, Different-Sized LLMs"
summary: "Any-Precision LLMは3、4、…、nビットの複数量子化モデルを別々に保存せず、最上位nビット表現のビットプレーンを共有して低精度版を切り出す配置方式である。学習不要の段階的アップスケール量子化と、必要ビットだけを読み込むGPU行列ベクトル積カーネルを組み合わせる。Llama-2-7Bでは複数精度を単一最大精度モデル相当のメモリへ重ね、個別配置比で最大数倍のメモリ節約を示す。"
list_summary: "1つのビットプレーン表現から複数精度LLMを切り出し、モデル切替・投機的復号向けの複数サイズ配置を低メモリ化する。"
authors: ["Yeonhong Park","Jake Hyun","SangLyul Cho","Bonggeun Sim","Jae W. Lee"]
published: "2024-02-16"
publication: "International Conference on Machine Learning (ICML 2024)"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/2402.10517"
sources: ["https://arxiv.org/abs/2402.10517","https://github.com/SNU-ARC/any-precision-llm"]
implementation: "重みのみ事後量子化で最低精度から段階的にクラスタを分割して上位ビットを追加し、ビットプレーン配置から要求精度分だけを読む専用GPU行列ベクトル積カーネルを実装。Llama-2等をデスクトップ/エッジGPUで評価。"
code: "https://github.com/SNU-ARC/any-precision-llm"
last_checked: "2026-10-04"
arxiv_id: "2402.10517"
arxiv_categories:
  primary: "cs.LG"
  cross_list: []
worker_completed_at: "2026-10-04T08:23:00+09:00"
worker_run_key: "20261004-0800-scheduled-chat-00/r01"
---
# Any-Precision LLM: Low-Cost Deployment of Multiple, Different-Sized LLMs

## 概要
実運用では、同じ能力系列でも低遅延用・高品質用の複数モデルを切り替えたり、投機的復号で小型ドラフトと大型対象モデルを同時常駐させたりする。通常は各モデルの重みを別々に保持するため、モデル数を増やすほどGPUメモリやストレージが増える。Any-Precision LLMは「モデル幅を別々に作る」のではなく、同じ重みを3、4、…、nビットの量子化精度として入れ子にする。

最上位nビット表現をビットプレーンとして保存し、低精度版はその上位ビットだけを読む。これを成立させるため、最低精度モデルを事後量子化で作った後、クラスタを段階的に二分して1ビットずつ精度を上げる。さらに通常の量子化カーネルでは全ビットを読み込んでしまう問題に対し、要求精度のビットプレーンだけをメモリから取得する専用行列ベクトル積を実装する。

## 問題設定
複数サイズのLLMは、要求ごとの品質・遅延制約への適応や投機的復号に有用だが、別checkpointとして持つと容量が加算される。論文のLlama-2-7B例では3ビット版と6ビット版を別々に置くと8.3 GBなのに対し、入れ子表現なら5.6 GBで済む。3/4/6ビットを別々に持つ12.1 GBに対しても5.6 GBであり、モデル数が増えるほど共有の価値が増える。

従来の任意精度ニューラルネットワークは学習段階から複数ビットを考慮するため、巨大LLMへ適用するには再学習費用が大きい。また既存GPUカーネルは量子化値の一部ビットだけを選択的に読む設計ではないため、低精度を選んでもHBMからnビット全体を転送するとdecodeのメモリ帯域を節約できない。

## 手法

### 段階的アップスケール量子化
最初にSqueezeLLM型の非一様な重みのみ事後量子化を使って最低ビット幅のseedを作る。各量子化クラスタは重み感度を考慮した代表値を持つ。次の精度へ上げる際、各クラスタを重み付きk-meansで2つへ分割し、元のインデックスへ1ビットを追加する。この操作を繰り返すと、低精度コードが高精度コードの上位ビットとして保存される。

独立に3/4/5…ビットを量子化するのと異なり、各段階が前段のコードを継承するため、単一nビット表現から任意の対応精度を復元できる。追加学習は不要で、既存FP16 checkpointから後処理として作れる。

### ビットプレーン配置
通常のpacked integer配置では1つの重みの全ビットが隣接するため、3ビットだけ使いたくてもメモリtransactionが不要な下位ビットを含みやすい。提案エンジンは同じ桁のビットをまとめるビットプレーン配置へ変換し、要求された精度までのplaneだけをGPUへ読み込む。

decodeの行列ベクトル積はしばしば演算よりweight読み出しが律速なので、3ビット選択時に8ビット分を読まないことが実時間短縮へ直結する。論文はweight layout optimization、index bit transformation、table lookup関連のカーネル最適化を組み合わせ、任意精度の柔軟性による追加費用を抑える。

### 実行時精度切替
同じ常駐表現から要求ごとにビット幅を選択できるため、品質優先requestは高精度、遅延優先requestは低精度を利用できる。投機的復号なら低ビット版をドラフト、高ビット版を対象として、別checkpointを常駐させず同一weight表現を共有できる。

この設計はパラメータ数を変える「小型モデル」とは異なり、同じarchitectureの量子化精度を変える。したがってメモリ共有性は高い一方、低精度版の計算グラフや層数は変わらない。

## 評価条件
|項目|条件|
|---|---|
|モデル|Llama-2系列などdecoder-only LLM|
|量子化|重みのみ事後量子化、3ビット以上の複数精度|
|実装|専用CUDA行列ベクトル積、TensorRT-LLM統合を含む|
|hardware|デスクトップGPUおよびエッジGPU|
|比較|精度ごとの独立量子化、既存weight-only量子化engine|
|指標|メモリ容量、perplexity/zero-shot品質、kernel・end-to-end throughput|

## 主要結果
|条件|結果|読み取れること|
|---|---:|---|
|Llama-2-7B、3/6 bit|5.6 GB対別配置8.3 GB、1.49倍節約|2精度でもweight共有が効く|
|Llama-2-7B、3/4/6 bit|5.6 GB対12.1 GB、2.15倍節約|対応精度数が増えるほど別checkpoint方式との差が広がる|
|Llama-2-7B、3/4/8 bit|7.7 GB対13.7 GB、1.76倍節約|最大精度モデル相当の容量で複数精度を保持できる|
|複数モデル・bit幅|独立量子化手法に近い品質|入れ子制約による品質損失を小さく抑える|
|専用kernel|低bitほどweight trafficを削減|任意精度表現を容量節約だけでなく推論速度へ結び付ける|

論文の重要な点は「低ビット量子化そのもの」の最高精度ではなく、複数の量子化モデルを同時配備する際の総メモリを、最大ビット幅モデル1つに近い水準へ抑えることにある。個別量子化モデルを複数ロードする場合と比べ、精度候補が増えても重み容量がほぼ最大精度側で頭打ちになる。

## 既存研究との差
GPTQ、AWQ、SqueezeLLM等は通常、1つの目標bit幅に対して高品質な量子化モデルを作る。Any-Precision LLMは複数bit幅のコードを入れ子にすることを第一目的にし、単一weight表現から複数deployment pointを作る。従来のany-precision DNNに対しては、LLMを再学習せず事後量子化だけで構築し、decodeのweight bandwidthを実際に減らす専用GPUカーネルまで用意する点が異なる。

## 限界
低精度版は同一パラメータ数の量子化モデルなので、層削減や蒸留モデルほど演算数そのものは減らない。速度利得はdecodeがweight bandwidth律速である条件ほど大きく、prefillの大きなGEMMでは同じ比率にならない。また任意精度の入れ子制約により、各bit幅を完全独立に最適化した場合より量子化自由度は狭い。

## 一次資料
- https://arxiv.org/abs/2402.10517
- https://github.com/SNU-ARC/any-precision-llm