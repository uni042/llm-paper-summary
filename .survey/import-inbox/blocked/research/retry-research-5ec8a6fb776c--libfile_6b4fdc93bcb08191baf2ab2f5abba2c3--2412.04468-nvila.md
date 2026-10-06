---
canonical_id: "arXiv:2412.04468"
title: "NVILA: Efficient Frontier Visual Language Models"
summary: "NVILAは高解像度画像・長時間videoを先に高い空間/時間解像度で取り込み、その後visual tokenを圧縮するscale-then-compressで精度と計算量を両立する。VILAを基盤にtrainingからdeploymentまで最適化し、training cost 1.9–5.1倍、prefill latency 1.6–2.2倍、decode latency 1.2–2.8倍の改善を報告する。"
list_summary: "画像・videoの解像度を先に拡大して情報を取り込み、その後visual トークンを空間・時間圧縮することでVLMの精度を保ちながらプリフィル/デコードを高速化する。"
authors: ["Zhijian Liu","Ligeng Zhu","Baifeng Shi","Zhuoyang Zhang","Yuming Lou","Shang Yang","Haocheng Xi","Shiyi Cao","Yuxian Gu","Dacheng Li","Xiuyu Li","Haotian Tang","Yunhao Fang","Yukang Chen","Cheng-Yu Hsieh","De-An Huang","An-Chieh Cheng","Jinyi Hu","Sifei Liu","Ranjay Krishna","Pavlo Molchanov","Jan Kautz","Hongxu Yin","Song Han","Yao Lu"]
published: "2024-12-05"
publication: "IEEE/CVF Conference on Computer Vision and Pattern Recognition 2025"
publication_type: "conference"
publication_status: "published"
source: "https://arxiv.org/abs/2412.04468"
sources: ["https://arxiv.org/abs/2412.04468","https://openaccess.thecvf.com/content/CVPR2025/html/Liu_NVILA_Efficient_Frontier_Visual_Language_Models_CVPR_2025_paper.html"]
implementation: "VILAを基盤にSigLIP vision encoder、projector、Qwen2系token processorを構成し、画像・video benchmarkとtraining/fine-tuning/deployment効率を実測。公式VILA code/modelを公開。"
code: "https://github.com/NVlabs/VILA"
last_checked: "2026-10-06"
arxiv_id: "2412.04468"
arxiv_categories: {primary: "cs.CV", cross_list: ["cs.AI","cs.CL"]}
worker_completed_at: "2026-10-06T06:58:00+09:00"
worker_run_key: "20261006-0630-scheduled-chat-30/r02"
last_audited: null
audit_version: 0
---
## 概要
視覚言語モデル（VLM）では画像解像度やvideo frame数を増やすほど細部を保持できるが、LLMへ渡すvisual トークンも増え、プリフィルとデコードの計算・メモリを圧迫する。NVILAは「最初から低解像度にして情報を捨てる」のではなく、まず解像度を上げて情報を取得し、その後トークンを圧縮するscale-then-compressを採る。

## 手法
画像側ではDynamic-S²で元aspect ratioを保ちながら複数scaleへtile化し、SigLIPで特徴を抽出する。高解像度化で増えたvisual トークンはspatial-to-経路（STC）reshapeで圧縮する。2×2だけでなく3×3圧縮も検討し、強い圧縮でaccuracyが落ちる問題に対してVisual Encoder Pre-学習（VEP）を追加し、vision encoderとprojectorを共同調整して圧縮耐性を回復する。

video側では標本 frame数を増やして時間情報を先に確保し、その後temporal averagingで複数frameのトークンをプールする。8→32 frameはVideo-MME accuracyを5ポイント超改善する一方トークン数を4倍にするが、4倍のtemporal compressionによりトークン予算を戻しつつ、元の8-frame 比較対象より高いaccuracyを保つ。

deploymentではvisual トークン削減がLLM側のプリフィル計算を直接減らす。デコードでもマルチモーダル 文脈が短くなることでメモリ アクセスと注意機構負荷が減る。論文は構成だけでなく学習/微調整/deployment全体を個別に最適化する。

## 評価条件
|項目|条件|
|---|---|
|基盤|VILA、SigLIP、2-層 MLP projector、Qwen2系LLM|
|主分析規模|8B モデル中心|
|入力|高解像度image、long video|
|比較|VILAおよび主要open/proprietary VLM|
|指標|accuracy、学習 コスト、微調整 メモリ、プリフィル/デコード 遅延|

## 主要結果
CVPR版は学習 コストを1.9–5.1倍削減し、プリフィル 遅延を1.6–2.2倍、デコード 遅延を1.2–2.8倍改善すると報告する。公式projectの代表構成では微調整 メモリ 3.4倍削減も示される。空間圧縮ではVEPを組み合わせた強いトークン compressionが学習/inference双方で約2.4倍の高速化倍率を得る設定がある。

重要なのは、単純なトークン 枝刈りではなく、先にresolutionを上げてaccuracy ceilingを高めてから圧縮する点である。これにより同程度トークン budgetの低解像度比較対象より高い画像・video理解品質を狙う。

## 既存研究との差・限界
visual トークンを最初から少なくする方式に対し、NVILAは情報取得と計算削減を順序分離する。学習効率の改善も大きいが、本サーベイ上の主な価値はプリフィル/デコードの実測遅延改善である。

効果はvisual トークンが大きな比率を占めるマルチモーダル ワークロードで特に大きく、純テキスト LLMへそのまま適用できない。強い圧縮はVEP等の追加学習なしではaccuracyを落とすため、学習不要圧縮ではない。