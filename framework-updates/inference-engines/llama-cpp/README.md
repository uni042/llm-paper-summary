# llama.cpp

llama.cppの主要な機能・性能更新を継続的に記録する集約ページ。メモリ管理（memory management）、MoE、投機的デコード（speculative decoding）、GPUカーネル（kernel）、CPU/GPU間転送、同期削減など、実際の推論速度・必要メモリ・対応できるモデル規模へ影響する変更を扱う。

## 現在できること

- **CPU・GPUをまたぐローカル推論**: CPUのみ、GPUのみ、またはCPU+GPU混在でmodelを実行できる。全layerをGPUへ載せる必要はなく、一部layerやFFNをCPU DRAMへ置いて、VRAM容量を超えるmodelも実行できる。代わりにCPU memory帯域とPCIe転送が性能へ効く。
- **広範なweight量子化**: GGUFと各種低bit量子化を使い、model weightの保存量・RAM/VRAM使用量・memory bandwidthを削減できる。CPU向けとGPU向けの専用kernelを使い、単なる保存圧縮ではなく実行時の低bit計算まで行う。
- **複数GPU配置**: tensor / pipeline型の分割でmodelを複数GPUへ配置できる。GPUごとのVRAM容量に応じてlayerやtensorを分担し、単一GPUに収まらないmodelを複数GPUで実行できる。
- **KV cache管理**: KV cacheの型・量子化・保持方法を調整し、長context時のmemory量を削減できる。recurrent / hybrid modelではKV以外のstateもcacheとして扱い、次tokenへ状態を持ち越せる。
- **MoE実行とexpert offload**: routed expert計算を専用GPU kernelでまとめて実行し、一部expertをCPUへ退避する構成も取れる。巨大MoEではVRAM節約とhost memory帯域のtrade-offを調整できる。
- **投機的デコードとMTP**: draft model、n-gram、MTP等で複数token候補を先に作り、target modelでまとめて検証できる。target forward回数を減らしてdecodeを高速化する。
- **GPU launch overhead削減**: CUDA Graphやkernel fusionで、1 tokenごとに繰り返す小kernelのCPU launch回数と中間tensorのVRAM書き戻しを減らせる。
- **server / embedding / multimodal利用**: CLIだけでなくserverとしてmodelを常駐させ、chat completion、embedding、画像入力対応model等をローカルAPIとして提供できる。

以下の更新履歴は、これらの能力について**どこまでGPU外memoryを使えるか、どの計算を低bit化・fusionできるか、decode時のCPU/GPU同期や転送をどれだけ減らせるか**を追う。

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
