# llama.cpp

llama.cppの主要な機能・性能更新を継続的に記録する集約ページ。メモリ管理（memory management）、MoE、投機的デコード（speculative decoding）、GPUカーネル（kernel）、CPU/GPU間転送、同期削減など、実際の推論速度・必要メモリ・対応できるモデル規模へ影響する変更を扱う。

## 現在できること

- **CPU中心のローカル推論**: x86 / ARM CPU上でGGUF modelを実行でき、GPUを持たないPCや大容量RAMを優先する環境でもLLMを動かせる。低bit weightとCPU向けSIMD / matrix kernelを使い、memory bandwidth律速になりやすいdecodeをできるだけ効率化する。
- **GPU推論とCPU/GPU混在配置**: CUDA、Metal等のbackendで一部または全部のlayerをGPUへ載せられる。全layerをVRAMへ置けない場合は残りをCPU DRAMへ置き、VRAM容量とCPU RAM容量を合わせてmodelを実行できる。
- **細粒度weight offload**: layer単位だけでなくFFN等の特定部分をCPU側へ置ける構成があり、attentionはGPU、容量の大きいFFNはCPUといった配置を取れる。VRAM節約とPCIe / CPU memory帯域のtrade-offを細かく調整できる。
- **GGUFと広範なweight量子化**: 2〜8 bit級を含む多数の量子化形式を使い、model file、RAM / VRAM使用量、weight読出し量を削減できる。単なるstorage圧縮ではなく、量子化weightを直接扱うCPU / GPU kernelを持つためdecodeのmemory traffic削減にもつながる。
- **複数GPUへのmodel分割**: modelをtensor / pipeline型に複数GPUへ配置し、単一GPUに収まらないmodelを実行できる。GPUごとのVRAM量に合わせてsplit比率を変えられ、multi-GPU streamを重ねて通信・計算の直列待ちを減らす方向の最適化も利用できる。
- **KV cacheの型・精度・容量制御**: K/Vを低bit化し、長contextで線形に増えるcache memoryを削減できる。cache領域を起動時のmemory planningへ含め、model load後にKV確保でVRAM不足になる問題を避けやすくする。
- **recurrent / hybrid state管理**: TransformerのKVだけでなく、GDN等のrecurrent architectureがtoken間で持ち越すstateもruntime cacheとして管理できる。MTPや投機的デコードで候補を巻き戻す際にもstate整合性が必要になる。
- **MoE実行**: routingされたexpertだけを計算し、Top-k選択、expert projection、weighted reduction等を専用kernelで処理できる。細かいMoE処理をfusionし、中間tensorのVRAM書き戻しとkernel launchを減らせる。
- **MoE expertのCPU offload**: 全expertをGPUへ常駐させず、一部をCPU RAMへ置くことで巨大MoEを少ないVRAMで実行できる。tokenごとに選ばれたexpertをCPU側から読むためhost memory bandwidthが律速になりやすく、hot expertだけGPUへcacheする方式も検討されている。
- **投機的デコード**: draft model、n-gram、DSpark、MTP等で複数token候補を先に作り、target modelでまとめて検証できる。候補受理率が高いほどtarget forward回数を減らせる。
- **MTP対応**: model自身の複数token予測headをdraftとして使い、別draft modelをloadせず投機的デコードできる構成を取れる。追加model memoryを抑えつつdecodeを高速化できる可能性がある。
- **CUDA Graph / kernel fusion**: decodeで繰り返すkernel列をGraphとして再利用し、CPU launch overheadを下げられる。MoEやactivation処理をfused kernelへまとめ、中間memory trafficも減らせる。
- **非同期copy / concurrent stream**: CPU→GPU copyやmulti-GPU処理を別streamへ載せ、copy・通信・計算を可能な範囲で同時進行できる。GPUがCPU側のcopy完了を待つidle時間を減らす。
- **server運用**: modelを常駐させてHTTP serverとして提供し、chat completion、text generation、embedding等をlocal / LAN applicationから利用できる。単発CLI実行だけでなく長時間常駐runtimeとして使える。
- **embedding / reranking等の非生成用途**: generationだけでなくembeddingやmodelによってはreranking系のforwardにも使え、RAG pipelineのlocal backendとして利用できる。
- **multimodal model**: 対応modelでは画像入力等をtext promptと組み合わせて処理できる。vision encoderとLLM部分のmemory配置が異なるため、CPU/GPU splitの調整が重要になる。
- **grammar / structured generation**: grammarやschemaに沿って生成token候補を制約し、JSON等の構造化出力を作りやすくできる。自由生成後のparse failureを減らせる。
- **広いplatform対応**: desktop、server、Apple Silicon、consumer NVIDIA GPU等で同じGGUF ecosystemを利用できるため、model配布形式とlocal inference runtimeの事実上の共通基盤の1つになっている。

以下の更新履歴は、これらの主要能力について**GPU外memoryをどこまで使えるか、低bit / fusionでmemory trafficをどこまで減らせるか、投機的デコードとmulti-GPUでtokenごとの待ち時間をどこまで削減できるか**を追う。

## 2026-09-05

- **CPUへ退避したMoE expert向けGPU常駐LRU cache — Draft / Open**: CPUメモリへ置いたMoE expertのうち、直近で使われたexpertだけをVRAMにも一時保持する提案。2026-09-07時点でもDraft / Open。`--moe-expert-cache N`で有効化し、現在は1 tokenずつ生成する通常decodeだけに適用される。

  MoE expertをCPUへ退避するとVRAM使用量は減る一方、tokenを生成するたびに選ばれたexpert weightをCPU RAMから読むため、host memory bandwidthが律速になりやすい。このPRは、**最近使ったexpertは近いtokenでも再利用されやすいという時間局所性（temporal locality）**を利用する。

  **LRU（Least Recently Used）cache**は、cacheが満杯になったとき「最も長く使われていない項目」から追い出す方式である。routing traceでは、常に人気なexpertを固定して置く静的cacheには強い偏りがなかった一方、直近利用expertには強い再利用傾向があり、推定cache hit率は64 slotsで約67%、128 slotsで約81%。

  Qwen3.8-Flash-Next UD-Q4_K_XL、2×RTX 3090では **18.4 → 24.2 tok/s（+31%）**。48 slots/layerで約4.1 GiBの追加VRAMを使う。multi-token decode、投機的デコード、MTP（Multi-Token Prediction; 複数token予測）は現状cacheを使わず従来経路へ戻る。[PR #27861](https://github.com/ggml-org/llama.cpp/pull/27861)

## 初期収録期間

2026-06-03〜2026-09-03

対象期間のmerged PRのうち、メモリ管理、MoE、投機的デコード、GPUカーネル、CPU/GPU offload、同期削減に関する本質的更新だけを掲載する。

## 要点

この期間の主な前進は、**GPUを待たせる同期やコピーを減らすこと、複数処理を1つのGPUカーネルへまとめること、将来tokenを予測して1回のforwardで複数tokenを進めること、モデル重みをCPUへ逃がしてVRAM制約を緩めること**に整理できる。

具体的には、CUDA Graphの適用範囲拡大、MoE kernel fusion、DSpark投機的デコード、dense FFNのCPU offloadが入った。さらに2026-09-05には、CPUへ退避したMoE expertを時間局所性に基づいてVRAMへcacheするDraft PRが公開された。

## 主要更新

- **2026-06-26 — token間同期の削減（merged）**: パイプライン並列（pipeline parallelism）でCPU→CUDA copyを非同期化し、copy完了確認とCUDA Graph実行の間にあった同期点を1回へ削減。GPUがCPU側処理を待つ時間を減らす。[PR #20793](https://github.com/ggml-org/llama.cpp/pull/20793)

- **2026-07-03 — GDNの冗長CUDA copy削除（merged）**: recurrent modelで次tokenへ持ち越す状態を、一時領域を何度も経由せずcacheへ直接書くよう変更し、4回のcopyを除去。DGX Sparkで通常decode約3%、MTP平均約4%向上。[PR #23940](https://github.com/ggml-org/llama.cpp/pull/23940)

- **2026-07-03〜09-01 — MoE fusion群（merged）**: routing後のexpert処理で別々に実行していた小さな演算をまとめ、GPU kernel起動回数や中間memory trafficを削減。
  - 288-expert Top-k処理のfusion: Step-3.7-Flash decode **2.4%向上**
  - 活性値量子化（activation quantization）の重複処理削除: RTX 5090 prefill **3.4〜5.9%**、end-to-end **2.8〜3.1%向上**
  - expert出力の重み付き加算（weighted reduction）をfusion: prefill **3.6〜7.1%向上**
  [#25267](https://github.com/ggml-org/llama.cpp/pull/25267) [#25441](https://github.com/ggml-org/llama.cpp/pull/25441) [#25952](https://github.com/ggml-org/llama.cpp/pull/25952)

- **2026-07-28 — DSpark投機的デコード（merged）**: 本体modelの次tokenをそのまま1個ずつ確定する代わりに、軽量な予測headで複数候補を先に作り、本体modelでまとめて検証する方式を追加。低rank Markov head、anchor-first drafting、信頼度による候補削減（confidence pruning）を使い、RTX 4090／Qwen3-8Bで **1.88倍**。[PR #25173](https://github.com/ggml-org/llama.cpp/pull/25173)

- **2026-08-11 — CUDA Graph適用範囲拡大（merged）**: CUDA GraphはGPU kernel群の起動手順を事前記録してCPU側launch overheadを減らす仕組み。同期が必要な経路だけGraph対象外にし、それ以外へ適用範囲を広げた。RTX 5090 parallel decodeでnpl16 **13%**、npl32 **8%**、BF16 decode **4.8%向上**。[PR #26802](https://github.com/ggml-org/llama.cpp/pull/26802)

- **2026-09-03 — multi-GPU concurrent streams（merged）**: 複数GPUへmodelを分割したとき、各splitのCUDA Graph最適化とCUDA streamを独立化し、GPU間で処理をより重ねられるようにした。MoE decode **3.7%向上**。[PR #28198](https://github.com/ggml-org/llama.cpp/pull/28198)

- **期間内 — `--n-cpu-ffn`（merged）**: dense modelのFFN（Feed-Forward Network; 全結合層部分）の一部をCPUへ置けるweight offloadを追加。VRAM不足を緩和できるが、CPU RAM bandwidthとPCIe転送が新しい律速になり得る。公式性能値なし。[PR #26622](https://github.com/ggml-org/llama.cpp/pull/26622)

KV cacheの量子化領域を起動時に予約し`--fit`へ反映する変更も入った。これは主に「実行途中で予想外にVRAM不足になる」ことを防ぐメモリ計画（memory planning）の改善で、速度向上を主目的とする変更ではない。[PR #23907](https://github.com/ggml-org/llama.cpp/pull/23907)
