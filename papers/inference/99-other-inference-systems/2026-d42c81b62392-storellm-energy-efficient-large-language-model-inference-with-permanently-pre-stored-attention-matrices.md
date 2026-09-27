---
canonical_id: "DOI:10.1145/3679240.3734604"
arxiv_id: null
doi: "10.1145/3679240.3734604"
openreview_id: null
arxiv_categories:
  primary: null
  cross_list: []
last_audited: "2026-09-27"
audit_version: 0
storage_targets:
  - "papers/inference/99-other-inference-systems/2026-d42c81b62392-storellm-energy-efficient-large-language-model-inference-with-permanently-pre-stored-attention-matrices.md"
bottlenecks:
  - "同じ語彙トークンに対するKVQ射影の繰返し計算"
  - "全トークンのKVQをSSDから読む場合の先頭応答遅延"
  - "ストレージ読出しとGPU再計算のエネルギー・遅延トレードオフ"
hardware_details: "NVIDIA RTX 3090、最大2.13 GHz、32 GB DRAM、Samsung 980 Pro PCIe 4.0 SSD 2 TBのサーバで実装。GPU側エネルギーはAccelWattchモデルとPowenetics v2測定器による校正、ストレージアクセスは既報のモデルを使用。"
quality_effect: "StoreLLMはKVQを元の値のまま再利用する設計で、論文は比較精度を約96.87%と報告。FFN圧縮のPTQではINT8/INT4の精度がそれぞれ86.27%/81.23%。MoE版の精度は再学習を要するため未評価。"
evidence_locations:
  - "Primary conference PDF: Abstract and bibliographic details, PDF lines 0-55"
  - "Primary conference PDF: Motivation and system overview, PDF lines 56-183"
  - "Primary conference PDF: Cache, profiling, scheduler and FFN compression, PDF lines 184-367"
  - "Primary conference PDF: Implementation, evaluation setup, energy/latency/accuracy results, PDF lines 369-439"
  - "Primary conference PDF: Complete references [1]-[37], PDF lines 444-545"
  - "Primary conference PDF: Profiling details, scheduler algorithm, ablations, discussion and limits, PDF lines 546-1005"
references:
  - "arXiv:2407.14057"
  - "arXiv:1609.07843"
  - "arXiv:2205.13792"
  - "arXiv:2403.20306"
  - "arXiv:2302.13971"
  - "arXiv:2205.01068"
references_checked_at: "2026-09-27"
references_source: "primary-reference-section"
references_total: 37
title: "StoreLLM: Energy Efficient Large Language Model Inference with Permanently Pre-stored Attention Matrices"
summary: "StoreLLMは、同じ語彙トークンのKVQ射影は異なるプロンプトでも大きく変わらないという観察に基づき、全トークンの行列を事前計算してSSDに置き、語彙頻度の高いものだけをDRAMへキャッシュする。要求時はまずDRAMを調べ、ミスした低頻度トークンごとに、GPU再計算とSSD読出しのどちらを選ぶかを計算・ストレージのエネルギー、遅延プロファイルとTTFT制約から動的計画法で決める。GPU計算の一部を低エネルギーの記憶読出しへ置き換え、遅延制約を守りながらエネルギー/トークンを減らす。RTX 3090・32 GB DRAM・PCIe 4.0 SSD上でOPT-6.7B、Llama-7B、StableLM-7Bを評価し、WikiText-103とBookCorpusではLazyLLM比最大1.45倍の省エネルギーを報告する一方、BookCorpusの先頭応答遅延はLazyLLMより5.05%増える。これは英語コーパスで上位頻度トークンを固定キャッシュする実装であり、語彙分布が異なる領域では再配置が必要と論じる。"
list_summary: "頻出語のKVQ行列をDRAMへ置き、残りをSSDに事前格納して、遅延制約下でSSD読出しかGPU再計算かを選ぶ。英語コーパス評価でLazyLLM比1.45倍の省エネルギーと5.05%のTTFT増を報告する。"
authors:
  - "Dan Wang"
  - "Boan Liu"
  - "Rui Lu"
  - "Shuntao Zhu"
  - "Zhaorui Zhang"
authors_affiliations: "The Hong Kong Polytechnic University"
published: "2025-06-17"
publication: "The 16th ACM International Conference on Future and Sustainable Energy Systems (E-ENERGY '25), Rotterdam, June 17-20, 2025"
publication_type: "conference paper"
publication_status: "Published"
lineage: "推論中のKVQ再計算をストレージ読出しへ置換し、階層キャッシュと遅延制約付きスケジューラを組み合わせるLLM推論省エネルギー化。"
topics:
  - "LLM推論の省エネルギー化"
  - "KVキャッシュ"
  - "階層ストレージ"
  - "計算とストレージのスケジューリング"
importance: "モデル内部の計算を減らす既存手法と別の軸として、繰返し現れる語彙トークンの射影行列を永続ストレージから再利用する。DRAM頻度キャッシュと、SSD読出し・GPU再計算を使い分ける最適化を一つの実装へまとめ、エネルギー削減と先頭応答時間の競合を定量化する。"
hardware_evaluation: "OPT-6.7B、Llama-7B、StableLM-7BをNVIDIA RTX 3090上で実装。最大GPU周波数2.13 GHz、DRAM 32 GB、Samsung 980 Pro PCIe 4.0 SSD 2 TB。Wikitext-103とBookCorpusを使用し、既定プロンプト長100、DRAMの10%をKVQ格納へ割当。エネルギー/トークン、先頭トークンまでの時間（TTFT）、Vanilla比の精度指標を測定。"
source: "https://wangdan.people.ust.hk/Publication/eEnergy25-StoreLLM-final.pdf"
sources:
  - "https://wangdan.people.ust.hk/Publication/eEnergy25-StoreLLM-final.pdf"
  - "https://doi.org/10.1145/3679240.3734604"
code: "https://github.com/StoreLLM/StoreLLM/"
implementation: "一次資料の脚注にソースコードURLの記載あり: https://github.com/StoreLLM/StoreLLM/"
last_checked: "2026-09-27"
---

# StoreLLM: Energy Efficient Large Language Model Inference with Permanently Pre-stored Attention Matrices

> 語彙トークンの注意行列を先に計算してSSDへ蓄え、頻出分だけDRAMへ置き、要求ごとに遅延を守りながら読出しか再計算かを選ぶ方式である。

## 概要

StoreLLMは、同じトークンに対応する鍵・値・問い合わせの射影行列（KVQ行列）がプロンプトをまたいで大きくは変わらないという著者らの観察を利用し、これらを事前計算してSSDに永続保管するLLM推論システムである。毎回の入力処理でGPUが再計算する代わりに、ストレージから既計算値を読み込む。語彙頻度の高いトークンはDRAMキャッシュへ置き、低頻度トークンはSSDから読むか、遅延が厳しければGPUで再計算する。

中核は、ハードウェア上の計算時間・ストレージ時間・エネルギーをオフライン計測しておき、要求の先頭トークン応答時間（TTFT）制約内でエネルギー/トークンを小さくする計算・ストレージスケジューラである。RTX 3090、32 GB DRAM、PCIe 4.0 SSDを用いた評価で、OPT-6.7B、Llama-7B、StableLM-7BのエネルギーをLazyLLM比約1.45倍効率化し、BookCorpusでTTFTはLazyLLMより5.05%増えた。著者らはFFNをMoE化・量子化した変種も示すが、MoE版の精度は再学習が必要なため測定していない。また語彙の頻度順位は一般英語コーパスに基づき、専門・多言語領域へは動的適応が今後の課題である。

## 書誌情報

- 著者: Dan Wang、Boan Liu、Rui Lu、Shuntao Zhu、Zhaorui Zhang。全員の所属はThe Hong Kong Polytechnic University。
- 発表: E-ENERGY '25（The 16th ACM International Conference on Future and Sustainable Energy Systems）、2025年6月17〜20日、オランダ・ロッテルダム。DOI: 10.1145/3679240.3734604。
- 実装: 論文脚注に https://github.com/StoreLLM/StoreLLM/ を記載。
- 参考文献: 一次資料の参考文献は[1]〜[37]の37件。metadataには本文の参考文献節にarXiv識別子が明記された6件のみを記録し、残りの識別子を題名から推定していない。

## 問題設定

LLM推論の入力処理（プリフィル）では、プロンプトの各トークンをモデルへ通し、注意機構で使うKVQ行列を計算する。逐次生成（デコード）では計算済みKVをキャッシュから再利用するが、新しいプロンプトの各トークンに対しては、プリフィル時にKVQを再び計算する。著者らは、同じ語彙トークンの埋め込みが同一であることから、そのトークンのKVQ行列は異なるプロンプトでも大部分が同じになり、繰り返し計算されていると仮定する。

この仮定に立つと、GPU演算をストレージ読出しで置き換えることに省エネルギーの余地がある。論文は計算一回のエネルギーがストレージアクセス一回より20〜100倍大きいという先行研究に基づく。ただし、全語彙の行列を保存すると容量が大きく、SSD読出しはGPU計算より遅い。全てを保存して毎回読むだけではTTFT制約を満たせないことがある。

Wikitext-103では267,735種類の異なるトークン行列に約257 GB、BookCorpusでは1,316,420種類に約1.263 TBが必要と推定される。そこで、全トークンの行列はSSDへ事前保存しつつ、COCAの頻度上位語彙だけをDRAMへ置く。残る低頻度トークンは、要求ごとの時間制約とエネルギーに基づいてGPU再計算かSSD読出しかを選ぶ。目的はモデル精度を変えずに計算エネルギーを減らすことと、許容可能な先頭応答遅延を維持することである。

## 手法

### KVQ行列の事前保存と頻度キャッシュ

StoreLLMは各LLMトークンのKVQ行列をあらかじめ計算し、SSDへ保存する。トークン行列はモデル固有なので、同じモデルの推論要求が複数来るほど事前計算エネルギーを多数の要求へ償却できる。論文の例ではWikitext-103の1億トークンに対して異なるトークンは267,735種類で、平均再出現回数は380.53回である。BookCorpusには約131万種類あり、想定保存量は約1.263 TBになる。

SSDの大容量だけでは応答速度が足りないため、頻出トークンのKVQ行列をDRAMへキャッシュする。対象頻度表には英語コーパスCOCAを使い、要求プロンプトに依存しない固定の上位K語彙を選ぶ。既定設定は32 GB DRAMの10%をKVQ用に割り当て、上位3,495トークンを保存する。この集合はWikitext-103では全語彙の1.30%、BookCorpusでは0.26%だが、それぞれ全アクセスの81.26%、90.18%を占めると論文は報告する。

要求処理では、まずDRAMキャッシュからKVQを取得する。ヒットすればSSDにもGPUにも行かない。ミスしたトークンは低頻度で、SSDから読むときの時間とエネルギー、GPUで再計算した場合の時間とエネルギーを比較し、そのプロンプト全体のTTFT上限を満たす範囲で選択する。

### オフライン計測で実行コストをモデル化する

実行時の選択には、LLM内部の各計算とストレージ読出しのコストが必要になる。オフライン段階で、KVQ線形層、FFN、埋め込みなどの計算時間と電力をGPU・モデル別に測り、行列サイズや演算量から各層の時間を見積もる。GPUエネルギーはAccelWattchの電力モデルを使い、Powenetics v2電力測定器の結果で校正する。ストレージは読出しバイト数に比例するエネルギーと、実機SSDの帯域・レイテンシモデルを使う。

このプロファイルはGPUの型、モデル、ストレージ構成に依存する。論文はRTX 3090、RTX 4090、RTX 4070 Tiについて効率や計算時間・エネルギーを表にし、これらの構成に応じてKVQ計算とSSD読出しの相対コストが変わることを示す。DVFSを含めた動的GPU周波数制御は今後の課題としている。

### TTFT制約下で計算とSSD読出しを選ぶ

低頻度トークンごとに二つの選択肢がある。SSDからKVQを読むと計算エネルギーは節約できるが読出し待ちが加わる。GPUで再計算すると待ち時間は小さい場合があるが、計算エネルギーを消費する。プロンプト中の他のモデル処理やパイプライン並列で隠せる時間も考慮し、TTFTの上限から使える追加遅延を算出する。

著者らはこれを有界ナップサック問題として扱う。各トークンは「SSD読出しを選ぶことで得られるエネルギー節約量」と「増える実行時間」を持つ。プロンプトごとにコストが異なるため、オフライン計測値とプロンプトに応じた時間差分を入力し、動的計画法でエネルギーを最小化する読出し・再計算の組合せを決める。遅延上限が厳しいほど再計算を増やし、余裕があればSSD読出しへ切り替える。

ただし、あるハードウェアと制約の組合せでは問題が実行不能になることがある。著者ら自身も、遅延要求を満たせない場合があると述べ、高速SSDへの置換や別の遅延・エネルギー配分を今後検討するとしている。したがって、このスケジューラは常に省エネルギー選択を実現するものではなく、要求に使える時間枠とSSD性能が前提になる。

### FFNの圧縮を組み合わせる変種

注意行列の再利用後も、著者らのエネルギー分析ではFFNが大きな計算要因として残る。そこでStoreLLM-MoEはFFNを複数のエキスパートへ分け、トークンごとに一部だけを実行するMoEficationを組み合わせる。StoreLLM-PTQは学習後量子化でFFN重みをINT8またはINT4へ圧縮する。これらは基本StoreLLMのKVQ保存とは別の最適化軸である。

MoE版はエキスパート数を4または8にした構成を評価するが、適用モデルの再学習が必要なため、この論文では精度測定を行っていない。PTQ版では量子化ビット幅を落とすほど省エネルギーが増える一方、精度指標は低下する。基本方式の「KVQ値を変えずに読み直す」精度の議論と、FFN圧縮版の精度を混同してはならない。

## 評価

### 実装・入力・指標

実装サーバはNVIDIA RTX 3090 GPU（最大周波数2,130 MHz）、32 GB DRAM、Samsung 980 Pro PCIe 4.0 2 TB SSDを備える。モデルはOPT-6.7B、Llama 7B、StableLM-7Bで、既定はOPT-6.7B。データセットはWikitext-103とBookCorpus、既定プロンプト長は100トークンである。DRAMの10%をKVQキャッシュに用いる。

比較対象は、全層をGPUで実行するVanilla、重要でないトークンの計算を省くLazyLLM、重みの学習後量子化でモデルを圧縮するAWQである。指標はトークン当たりのエネルギー（mJ/トークン）、出力の先頭トークンまでの時間（TTFT）、Vanillaに対する精度指標である。論文は計算エネルギーを測定器で校正したモデルに基づき、ストレージも既存のエネルギーモデルに基づいて評価する。

### 基本StoreLLMの省エネルギーと遅延

OPT-6.7B、Llama-7B、StableLM-7Bの順に、Vanillaのエネルギーは72.31、75.68、86.70 mJ/トークン、LazyLLMは63.69、67.51、76.19 mJ/トークン、AWQは67.27、72.21、80.49 mJ/トークンである。StoreLLMは43.82、46.44、55.36 mJ/トークンとなり、LazyLLM比で約1.45倍のエネルギー効率を報告する。OPT-6.7BではKVQ線形層の計算が27.63 mJ/トークンに対し、保存行列のアクセスは0.30 mJ/トークンとされ、読み込みに置き換える理由を示す。

BookCorpusではStoreLLMのTTFTが8.95 msで、LazyLLMより5.05%、AWQより2.87%長い。データセットごとに頻度キャッシュへ当たるトークン割合が違い、SSDから直接読む行列が増えると遅延が増える。これはエネルギーと応答時間の交換条件を表す数値であり、全てのワークロードで一律に1.45倍の改善と5.05%の遅延増が出るわけではない。著者らは基本StoreLLMの精度指標を約96.87%と報告し、元のKVQ値を再計算せず読み出すため類似精度になると説明する。

### FFN圧縮版

OPT-6.7BとWikitext-103で、FFNを4または8エキスパートにしたMoE版は33.52、25.56 mJ/トークンである。8エキスパート版はLazyLLM比2.64倍、AWQ比2.83倍のエネルギー効率を報告する。PTQ版のINT8、INT4は37.84、27.52 mJ/トークンで、それぞれLazyLLM比1.78倍、2.45倍、AWQ比1.91倍、2.62倍となる。

INT8/INT4量子化版の精度は86.27%/81.23%で、INT4はINT8より精度が下がる代わりにエネルギー消費を27.2%減らすと記載される。MoE版はさらに低いエネルギー値を示すが、精度は再学習を要するため評価されていない。したがって、MoEの値を「精度を維持したまま得た利得」とは解釈できない。

### 感度分析から分かる範囲

付録では、プロンプト長、DRAM容量、遅延上限、頻度キャッシュ比率、語彙分布、モデル規模を変えた分析を示す。キャッシュ比率を下げるほどエネルギーは増える一方、遅延は比較的緩やかに短くなる。上位頻度の固定キャッシュは一般英語のWikitext-103とBookCorpusでは多くのアクセスを覆うが、専門用語や多言語対話では最頻語が変わる。著者らはこの分布ずれに合わせ、キャッシュ内容を実行時に動的更新することを今後の課題に挙げる。

## 既存研究との差

LazyLLMは重要度の低いトークンを計算から外し、AWQは重みを低ビット化する。従来のKVキャッシュ技術も現在のプロンプト内で計算済みの行列を再利用するが、別プロンプトでは再計算が必要になる。StoreLLMはこの計算削減や量子化とは異なり、トークン単位のKVQ行列をプロンプト間で再利用できるという仮説のもと、全トークンをSSDへ永続保存する。

容量に応じた頻度キャッシュと、SSD読み出しかGPU再計算かを遅延制約付きで選ぶスケジューラを一体化する点も特徴である。これにより、ストレージの大容量・低い読出しエネルギーを活かしつつ、SSDが遅いときは再計算へ切り替え、エネルギー削減とTTFT制約を両立させようとする。

## 限界

- 中心仮説は、同一語彙トークンに対応するKVQ行列がプロンプトをまたいで再利用できる程度に安定するというものだが、文脈に応じて層深部の表現が変わる影響を広く測る検証は限定的である。精度の維持は評価対象モデル・データセットの結果として読む必要がある。
- 頻度キャッシュはCOCAの一般英語語彙順位で固定される。論文は多言語・専門分野でアクセス分布が違うと認め、動的なキャッシュ更新を将来課題としている。
- GPUはRTX 3090、SSDはSamsung 980 Proという一つの実装が中心であり、遅延と省エネルギーはGPU計算時間、SSD性能、DRAM容量に依存する。論文は高性能SSDへの置換をまだ将来作業としている。
- スケジューラはTTFT制約を満たせない構成があり得る。とくに低頻度トークンでSSDアクセスが遅い場合は再計算に戻り、省エネルギー利得が小さくなる。
- 評価はWikitext-103・BookCorpusと100トークンの既定プロンプトを中心とする。実運用での多言語・長文・動的な複数要求、負荷変動、尾部遅延の評価は示されない。
- StoreLLM-MoEはエネルギー改善値を示す一方、再学習が必要な精度評価を行っていない。基本StoreLLMの約96.87%という精度報告と、圧縮変種の結果は分けて扱う必要がある。
- エネルギー/トークンの算出にはGPU・ストレージのモデルと一部測定器による校正が使われる。異なるハードウェアへ結果を一般化するには同じ環境での再測定が必要である。

## 一次資料

- 会議論文PDF（9ページ、全文・付録・全37参考文献）: https://wangdan.people.ust.hk/Publication/eEnergy25-StoreLLM-final.pdf
- DOI: https://doi.org/10.1145/3679240.3734604
- 著者記載のソースコードURL: https://github.com/StoreLLM/StoreLLM/
