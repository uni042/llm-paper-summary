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

## 2026-10-07 — llama.cpp b11476 / b11474（開発ビルド、正式版v0.6.0とは区別）

- **b11476: Metalの少行列積（few-row MMA）対応形式拡大**: BF16、Q1_0、Q2_0、MXFP4、Q2_K、Q3_K、TQ2_0、IQ系を16重み逆量子化器で処理する汎用カーネルへ追加。M3 Ultra・`MUL_MAT`・m=4096、k=14336の測定では、各型の適用閾値から8行までの実行時間比が旧実装の0.23〜0.98倍、9〜16行では0.24〜0.33倍。1行・512行では0.99〜1.01倍で、全行数で高速化するわけではない。**Metal固有の結果でWindows CUDAには直接適用できない**。[一次資料](https://github.com/ggml-org/llama.cpp/releases/tag/b11476)
- **b11474: GLM5-Nextの複数トークン予測（MTP）グラフ**: NextN層を本体と分離したGGUFから読み込めるようにし、MTPのdraft経路で使用可能にした。出力行に合わせたグラフ縮約により、4トークンの追いつき処理（catch-up）のカーネル時間が6.9→2.9 ms（同一実装比較）となり、greedy出力ハッシュは不変。モデル全体の生成速度改善率とは解釈しない。[一次資料](https://github.com/ggml-org/llama.cpp/releases/tag/b11474)

## 2026-10-05

- **v0.6.0（released）**: 拡張batch API `llama_batch_ext` / `llama_process` を追加し、token / embedding混在入力とMTP / deepstack state embeddingを扱えるようにした。GLM-5.3-Flash（GLM5-Next）320B hybrid model、Clef decision model、Qwen4ExpのMTP speculative decodingも追加。backendではMetal tensor-APIのF16 KV Flash Attention、Vulkanの量子化K/V向けsparse Flash Attention、CUDAのNVFP4 MMQ accumulation最適化を含む。serverにはdecision model用`/v1/systemone` APIを追加し、ggmlはv0.26.0へ更新。[release](https://github.com/ggml-org/llama.cpp/releases/tag/v0.6.0)

## 2026-09-28

- **b11238 — padding処理の統合**: `ggml_pad_ext` のleft padding対応を利用し、Parakeet、LFM2-Audio、Granite Speech、Gemma 4 audio encoderの従来のright-pad + rollを単一operationへ置換。DFlash2でも先頭zero block連結を同operationへ統合し、paddingだけを読むtapをskipする。大規模end-to-end benchmarkはrelease noteにないため、速度倍率は記録しない。[release b11238](https://github.com/ggml-org/llama.cpp/releases/tag/b11238)

## 2026-09-11

- **ROCm gfx1201向けFlash Attentionを長contextで再調整 — merged**: Radeon AI PRO R9700 / Qwen3.8 27B IQ4_XSで、150k-token context付近の512-token prefillが **164.42→399.01 tok/s（約2.43倍）**、40k-token付近では **426.36→639.46 tok/s（約1.50倍）**。長contextでのkernel選択とhead-size 256周辺を調整した。[PR #28102](https://github.com/ggml-org/llama.cpp/pull/28102)

## 2026-09-10

- **SYCLでIQ量子化MoEのホスト直列化を解消 — merged 2026-09-09 / release b10868**: Qwen3.8-Flash-Next UD-IQ3_XXS、3×Intel Arc Pro B60で生成 **+48.7〜60.4%**。プリフィルはほぼ不変。[PR #28476](https://github.com/ggml-org/llama.cpp/pull/28476)

- **Intel Vulkan協調行列積を高速化 — merged 2026-09-09 / release b10870**: Windows / Xe1-ARL_Hの512トークン・プリフィルでGemma 4 31B約30%、Qwen3 8B約29%、Qwen3.8 27B約21%改善。[PR #27471](https://github.com/ggml-org/llama.cpp/pull/27471)

## 2026-09-08

- **VulkanでTQ1_0量子化weightを直接実行 — merged / release b10831**: TQ1_0について、行列積（matrix multiplication）、行列ベクトル積（matrix-vector multiplication）、MoEで使うID付き行列積、逆量子化（dequantization）、行抽出をVulkan backendへ実装した。AMD gfx1151で対象backend testが通過している。Metalには対応kernelがないため、該当演算はCPUへfallbackする。[release b10831](https://github.com/ggml-org/llama.cpp/releases/tag/b10831)

- **VulkanのRMSNorm周辺fusion拡張 — merged / release b10833**: RMSNorm後の乗算・加算・view・row書込み等を融合できるパターンを増やし、中間memory trafficとkernel launchを削減する。release記載の開発者環境ではGemma 4で約4%改善したが、単一環境の測定値として扱う。[release b10833](https://github.com/ggml-org/llama.cpp/releases/tag/b10833)

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

## 2026-10-25〜26 — llama.cpp b11870〜b11888（開発ビルド）

b11869からb11888までの確定済み開発ビルド差分を追加。これらはpre-releaseであり、正式安定版と区別する。

- b11870でDeepSeek-V4.1-Flashのmodel実装を追加。圧縮KV cache計算、Engram行のgraph内gather、sparse top-k行の並べ替えなどを含む。
- b11879、b11883、b11884ではCUDA dense FFN fusion、4D quantization accuracy修正、DRY sampling関連修正などを収録。
- b11888でgrammarの再帰深度制限と候補棄却処理を修正し、長い空白token列の誤棄却を解消。公式説明にあるsampling改善はgrammar関連の評価であり、一般のE2E生成速度倍率ではない。
- b11888の配布assetにWindows CUDA 12.4およびCUDA 13.4系x64 buildがある。Windows 11 + RTX 4070 SUPERでの実測値は未確認。

一次資料: https://github.com/ggml-org/llama.cpp/releases/tag/b11870 ; https://github.com/ggml-org/llama.cpp/releases/tag/b11879 ; https://github.com/ggml-org/llama.cpp/releases/tag/b11883 ; https://github.com/ggml-org/llama.cpp/releases/tag/b11884 ; https://github.com/ggml-org/llama.cpp/releases/tag/b11888

## 2026-10-26〜27 — llama.cpp b11889〜b11912（開発ビルド）

b11888からb11912までの差分を追加。すべてpre-release開発ビルドであり、正式安定版とは区別する。

- b11901はSYCL reorder時の一時メモリを32 MiBに制限する。Intel/SYCL backend向けでCUDAへの直接追加ではない。
- b11905はVulkan RMSNormのsubgroup reduction最適化とAMD vendor pathを追加。Vulkan固有。
- b11909はQualcomm HexagonのMUL_MAT_ID row-skip zeroingをベクトル化。Hexagon固有。
- b11910はOpenCLのKV-cache view書き込みを修正し、state restore失敗を解消。
- b11912はLagunaのMoE amax rescalingとSM tensor supportを追加。特定architecture対応で一般モデルの速度向上を示さない。
- b11912の公式Windows配布assetにCUDA 12.4および13.4系x64 buildがある。Windows 11 + RTX 4070 SUPERでの実測・互換性は未確認。

一次資料: https://github.com/ggml-org/llama.cpp/releases/tag/b11901 ; https://github.com/ggml-org/llama.cpp/releases/tag/b11905 ; https://github.com/ggml-org/llama.cpp/releases/tag/b11909 ; https://github.com/ggml-org/llama.cpp/releases/tag/b11910 ; https://github.com/ggml-org/llama.cpp/releases/tag/b11912

## 2026-11-27 — llama.cpp b12792〜b12818（開発ビルド）

b12791の続き。開発ビルドは b12818（2026-11-27 20:43 UTC）まで進んだ。いずれもpre-releaseの開発ビルドであり正式版ではない。番号の範囲であって全番号にreleaseがある意味ではない。重要変更だけを拾う（b12791→b12818の差分は27 commit）。

- **b12818: ggmlがFP8 / NVFP4向け量子化scaleに対応**（PR #28898）。tensor scale（per-tensor / per-channel / per-expert / per-expert-per-channel）とactivation scaleを `mul_mat` / `mul_mat_id` へ通し、scale付き型ではscale side-carを必須化。低bit量子化の精度基盤に関わる変更で、速度倍率は公表されていない。
- **CUDA / HIP: indexed bias付きFlash Attentionを追加**（PR #33063）。**moe-cache: 別backendで選択されたexpertに対応**（PR #33133）。**graph: recurrent stateをcopyせずin-placeで読む**よう変更し、recurrent / hybridモデルのstate転送量を削減（PR #28841 / #30139）。
- **Inkling 2向けCUDA fusion**: short conv、depth mix、loop controller、L2 clip、situ chainを融合（PR #33060）。**BailingMoE3: ssm_conv + siluを融合**し冗長なcopyを削除（PR #33081）。いずれも特定architecture向けで、一般モデルの速度向上を示さない。
- **OpenCL: Adreno A850向けMoE int8 bin kernel**（PR #33069）と**投機的検証向けmulti-token f32 GEMV**（PR #33098）を追加。**Vulkan: Inkling 2 Mini向けFA compact bias対応**（PR #32898）。**SYCL: BMG D=256の単一query decodeをFA vector kernelへ振り分け**（PR #30606）。backend別の変更であり、速度倍率は公表されていない。
- 変換ではBertForSequenceClassificationのpoolerを保持（PR #33122）。x86_64-darwinのnix supportは削除された（PR #33114、利用者影響は限定的）。

一次資料: https://github.com/ggml-org/llama.cpp/releases/tag/b12818 ; https://github.com/ggml-org/llama.cpp/compare/b12791...b12818

## 2026-11-26 — llama.cpp v1.1.0（正式版）＋ b12704〜b12791（開発ビルド）

b12703の続き。正式版 v1.1.0 が 2026-11-26 09:16 UTC に公開された（version bump は b12752）。あわせて開発ビルドは b12791（2026-11-26 22:10 UTC）まで進んだ。番号の範囲であって全番号にreleaseがある意味ではない。重要変更だけを拾う。

- **v1.1.0: 旧 `llama_batch` API を非推奨化し `llama_batch_ext` / `llama_process` へ移行**（PR #32306 / #32356）。移行先の拡張batch API自体は v0.6.0 で導入済みで、本版で旧APIが deprecated になった点が breaking に近い変更。
- **v1.1.0: DFlash投機的デコードを方式別に分割**。`llama_dflash_variant` を追加し、draft方式を `draft-dflash` / `draft-dflash2` / `draft-dspark` / `draft-lilicorr` へ分離（PR #32016 ほか）。推論時のdraft head選択が明示的になった。
- **v1.1.0: 新モデル対応**。Inkling 2 系（base / Mini / DSpark、text+vision）、Domyn Edge 4B、Zaya1 8B、RAON-1-mini（30B-A4B MoE）、Hy4 flash（220B・活性12B、DSA iSWA cache）、MiniMax-M3.1 の変換対応。いずれも他社モデルの runtime 対応であり、モデル自体の新規公開ではない。TTS・音声モデル（Kokoro、VoxCPM2、Fish S2 等）も多数追加されたが、LLM推論の主対象外のため個別には記録しない。
- **v1.1.0: 量子化の自動目標指定**。`llama_model_quantize_params` に `target_bpw` / `target_size` を追加し、目標bpw／ファイルサイズへ向けた tensor ごとの量子化型自動選択に対応（PR #15550、開発ビルド b12669 で先行導入された機能の正式版取り込み）。
- **v1.1.0: server の slot scheduling refactor と token-aware chat parsing、named `tool_choice` 対応**。ggml は v1.1.1 へ更新。一般的な生成速度の倍率は一次資料に公表されていないため記録しない。
- **b12785: Inkling-2-Mini 向け DFlash2 対応**（PR #33073）。**b12780: ggml の MUL_MAT / MUL_MAT_ID で BF16 src1 に対応（CPU / CUDA）**（PR #32533）。**b12778: CUDA で top-k MoE の weight norm と additive sum bias を融合**（PR #32943）。
- **b12722: OpenCL に coopmat MoE kernel を追加**（Q4_0 / Q4_1 / Q4_K / Q5_0 / Q5_1 / Q5_K / Q6_K / MXFP4、PR #32971、Qualcomm系経路）。**b12732: ggml で入力の非同期copyを許可**し、split ごとの blocking copy を削減（PR #30685）。**b12734: Metal で graph commit を chunk 分割**（PR #32947）。いずれも速度倍率は公表されていない。

一次資料: https://github.com/ggml-org/llama.cpp/releases/tag/v1.1.0 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12785 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12780 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12722

## 2026-11-25 — llama.cpp b12683〜b12703（開発ビルド）

b12682の続き。対象期間の開発ビルドはb12683からb12703までで、いずれもpre-releaseの開発ビルドであり正式版ではない。番号の範囲であって全番号にreleaseがある意味ではない。重要変更だけを拾う。

- **b12686: serverで skip されていた prompt cache lookup を修正**（PR #28992）。prompt cacheのlookupを slot scheduler の `select()` へ移し、cache更新の判断をplan側へ寄せた。prefix cache再利用の正確性に関わる修正で、速度倍率は公表されていない。
- **b12683: rpcで request tensor 用の context を server 側で1つに再利用**（PR #32896）。RPC経路のcontext生成 overhead削減。
- **b12690: HIPで VEGA20 向けに Q4_K（N8）と NVFP4（N7-8）で MMVQ の代わりに MMQ を使用**（PR #32805）。ROCm／旧世代AMD GPU向けのkernel選択変更。
- **b12703: CUDAで RMS_NORM・MUL・MROPE/IMROPE を融合したkernelを追加し、block sizeを自動調整**。中間memory trafficとkernel launchの削減が狙い。速度倍率は一次資料にないため記録しない。

一次資料: https://github.com/ggml-org/llama.cpp/releases/tag/b12686 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12683 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12690 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12703

## 2026-11-24 — llama.cpp b12655〜b12682（開発ビルド）

b12651の続き。対象期間の開発ビルドはb12655からb12682（2026-11-24 22:11 UTC）までで、いずれもpre-releaseの開発ビルドであり正式版ではない。なお b12652〜b12654 / b12656 / b12660 / b12661 / b12663〜b12666 / b12672 / b12673 / b12677 は Releases API の一覧にないため、この範囲表記は「番号の範囲」であって全番号にreleaseがある意味ではない。重要変更だけを拾う。

- **b12669: quantizeに、目標ファイルサイズ／bpwへ到達するための量子化型の自動選択optionを追加**（PR #15550）。低bit化の試行錯誤を自動化するもので、量子化形式そのものの追加ではない。
- **b12679: OpenCLに Q6_K coop-k c8 GEMMを追加**（最大n=8の投機的検証向け）。b12648の Q4_K 版に続くもので、対象はQualcomm系のOpenCL経路。一般的な生成速度倍率は公表されていない。
- **b12675: serverで prompt-cache entry を restore 成功まで保持**（PR #32828）。prompt cache（prefix cache相当）の復旧時の正確性・再利用に関わる修正。
- **b12676: GDNで rollback の代わりに replay を使用**（PR #31669）。recurrent stateの巻き戻し方式の変更で、投機的デコード等でのstate整合性に関わる。
- **b12670: ggmlの FLASH_ATTN_EXT で bias を compact 化**。Flash Attention経路の中間tensor削減。
- **b12668: Metalの MUL_MAT / MUL_MAT_ID で BF16 / F32 の src1 に対応**。**b12657: ggml-cudaの few-row MMQ量子化で zero blocks を処理**。いずれもbackend別の演算カバレッジ・正確性の拡張。
- **b12659: ggml-openvinoの新モデル対応・修正・改善**。**b12662: Metalで iPhone 向け Bonsai の GPU timeout を解消**。
- **b12681: Vulkanの ssm_scan で state size 96 に対応**。**b12682: ggmlの softplus に range-reduced log1p を導入**（Metal / Vulkan / OpenCL）。負入力での数値精度の修正であり、速度倍率は公表されていない。
- 小変更として扱い個別には記録しないもの: b12655（cmakeのKleidiAI vendored化）、b12658（rpcのtyped request helpers）、b12667（serverのexec_shell_command説明要求）、b12671（Metalのbatch concat）、b12674（OpenCLのAdreno binary kernel取得、Windows on Snapdragon向け）、b12678（editor config修正）、b12680（OpenCLのGDN QK offsets修正）。

一次資料: https://github.com/ggml-org/llama.cpp/releases/tag/b12682 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12679 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12669 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12675

## 2026-11-23 — llama.cpp b12635〜b12651（開発ビルド）

b12633の続き。対象期間の開発ビルドはb12635からb12651（2026-11-23 08:52 UTC）までで、いずれもpre-releaseの開発ビルドであり正式版ではない。なお b12634 / b12636 / b12637 / b12639 は GitHub Release が存在しない（Releases API の一覧になく、tag指定取得も404）ため、この範囲表記は「番号の範囲」であって全番号にreleaseがある意味ではない。重要変更だけを拾う。

- **b12648: OpenCLに投機的検証（speculative verification）向け Q4_K coop-k c8 GEMMを追加**。n>=2 で有効化され、X2向けにも有効化。対象はQualcomm系のOpenCL経路に限られ、一般的な生成速度倍率は公表されていない。
- **b12642: 複数ノードで共有されるホスト重みの全expertコピーを修正**。スケジューラがホスト重みをグラフごとに1回だけデバイスへコピーするため、最初の MUL_MAT_ID 向けの部分コピーでは他のノード分が古くなる問題（例: `--n-cpu-moe` 使用時の inkling2_loop の共有層）への正確性修正。MoEのCPU offload構成に関わる。
- **b12638: チャットのtoken-aware parsingを実装**（PR #29307）。チャット／ツール呼び出しのパース経路の変更。
- **b12650 / b12641: Inkling系の対応仕上げ**。b12650は inkling の parser / grammar を改善、b12641は inkling2 の vocab で `ignore_merges` を有効化。
- **b12644: mtmdの共有audio FFTを高速化**。再帰的な radix-2 分割を反復ステージ方式へ置換し入力バッファを縮小、`test_audio_fft` を追加。速度倍率は一次資料にないため記録しない。
- **b12643: mtmdの Qwen3-Omni / Qwen3-ASR の音声末尾（audio tail）修正**。zero-padding 由来の余分なtokenを除去する正確性修正。
- **b12649: OpenCLに XIELU 演算を追加**。**b12651: WebGPUに ROLL 対応を追加**（backend演算カバレッジの拡張）。
- **b12635: ggmlに SIGMOID の backward pass を追加**。Qwen3.5 hybrid系で使われる演算で、RPCプロトコルのパッチ版を更新。推論decode自体の高速化ではない。
- 小変更として扱い個別には記録しないもの: b12640（server の grep_search ツールへのoffset pagination）、b12645（LFM2.5-VL のtemplate検出修正）、b12646（ggml-backend の memset 汎用fallback）、b12647（GDN snapshot のテスト比較範囲の修正のみ）。

一次資料: https://github.com/ggml-org/llama.cpp/releases/tag/b12651 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12648 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12642 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12638

## 2026-11-22 — llama.cpp b12614〜b12633（開発ビルド）

b12613の続き。対象期間の開発ビルドはb12614からb12633（2026-11-22 14:53 UTC）までで、いずれもpre-releaseの開発ビルドであり正式版ではない。重要変更だけを拾う。

- **b12629: OpenCLにAdreno 850向けcoopmat GEMMを追加**。Q4_0 / Q5_0 / Q8_0 / Q4_K / Q5_K / Q6_K の量子化形式に対応する行列積で、対象はQualcomm Adreno 850のOpenCL経路に限られる。一般的な生成速度倍率は公表されていない。
- **b12615: SYCLの融合演算とRMS norm最適化**。ADD・RMS_NORM・MULのfused演算と、連続メモリ向けRMS normのベクトル化を追加。対象はIntel系のSYCL経路で、デコード幅でのテストが追加された。
- **b12621: SYCLのCONV_TRANSPOSE_1Dの入力反復に上限を設定**。出力がベースとバイト単位で一致することと test-backend-ops 116/116 が一次資料で確認されており、正確性・堅牢性の修正として扱う（速度倍率は一次資料にない）。
- **b12622: モデル読み込みで `.scale` テンソルを自動適用**し、精度ポリシー（llama_prec_policy）を導入。MoE FFN構築まわりの整理を含む。
- **b12619: mtmdがHibikiのリアルタイムduplexに対応**。音声系マルチモーダル経路の拡張であり、テキスト生成速度の改善ではない。
- **Vulkan／WebGPUの非UMA・不整合メモリまわりの修正**: b12626（Vulkanのunaligned範囲memset修正）、b12628（Vulkan SCALEの非連続src対応）、b12631（WebGPUのGDN supports_op確認更新）、b12633（ggmlのWebGPU・非UMAデバイスでのnonzero clear修正）。いずれも対象backend固有の正確性修正である。
- この範囲では新規backend追加や新規モデルアーキテクチャ対応の大きな発表はない。

一次資料: https://github.com/ggml-org/llama.cpp/releases/tag/b12633 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12629 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12615

## 2026-11-21 — llama.cpp b12591〜b12613（開発ビルド）

b12590の続き。対象期間の開発ビルドはb12591からb12613（2026-11-21 19:40 UTC）までで、いずれもpre-releaseの開発ビルドであり正式版ではない。重要変更だけを拾う。

- **b12613: Vulkan Flash Attention coopmat1のAMD Windowsドライババグ回避**。unrollの調整による回避であり、対象はAMD Windows環境のVulkan経路に限られる。
- **Vulkan RDNA4向けMMVQ性能改善**: Q3_K / Q5_K / IQ4_XS の行列ベクトル積をRDNA4向けに最適化。一般的な生成速度倍率は公表されていない。
- **tinyBLAS PPCのalignment修正**: Flint Q4_K_M / Gemma 3 27Bで起きていた文字化けを修正する正確性修正。
- **fused lightning indexerのgating撤廃**: 条件付きだった融合インデクサが常時有効化された。
- **b12602: SYCL backendのGrouped XMX GEMM性能改善**。SLM stagingによるもので、対象はIntel系のSYCL経路。
- この範囲では新規backend追加や新規モデルアーキテクチャ対応の大きな発表はない。いずれもVulkan／SYCLの性能改善と修正が中心である。

一次資料: https://github.com/ggml-org/llama.cpp/releases/tag/b12613 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12602

## 2026-11-20 — llama.cpp b12554〜b12590（開発ビルド）

b12553の続き。対象期間の開発ビルドはb12554（2026-11-19 22:19 UTC）からb12590（2026-11-20 19:02 UTC）までで、いずれもpre-releaseの開発ビルドであり正式版ではない。重要変更だけを拾う。

- **b12588: Gemma 4の複数シーケンス問い合わせでプロンプト処理を最適化**（PR #32342）。マルチシーケンス時のプリフィル経路の改善で、対象はGemma 4系の利用形態に限られる。一般の生成速度倍率は未提示。
- **b12561: Vulkanにチャンク化したGATED_DELTA_NET実装を追加**（PR #30207）。共有メモリのバンク競合対策を含むVulkan向けカーネルで、Gated DeltaNet系のハイブリッドモデルの実行経路を広げる。CUDA経路の変更ではない。
- **b12568: 新モデルDomyn Edge 4Bに対応**（PR #32559）。変換時のトークナイザハッシュ生成を含むモデル対応の追加。
- **b12590: mtmdでdrama3の音声クローニングに対応**。Fish S2のコーデックエンコーダをdrama3でも使う形で、音声系マルチモーダル経路の拡張であり、テキスト生成速度の改善ではない。
- その他はbackend別の最適化・正確性修正が中心である: GGMLのROPE／SET_ROWSへのBF16対応（b12554、CPU／CUDA）、OpenCLの分解型Flash Attentionでのdp4a（int8）KQ行列積対応（b12555）とGQAヘッド折り畳み（b12559）、CUDAのOrin向け単一列MMVQ最適化（b12564）とMUL_MAT_IDの精度保持（b12563）、VulkanのRMS_NORM_MUL_ROPEループ制御最適化（b12562）とCOL2IM_1D対応（b12589）、MoEキャッシュ向けグラフノード予約（b12569）等。一般的な生成速度倍率は公表されていない。

一次資料: https://github.com/ggml-org/llama.cpp/releases/tag/b12561 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12568 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12588 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12590

## 2026-11-19〜11-20 — llama.cpp b12528〜b12553（開発ビルド）

b12483の続き。対象期間の開発ビルドはb12528（2026-11-19）からb12553（2026-11-20）までで、いずれもpre-releaseの開発ビルドであり正式版ではない。重要変更だけを拾う。

- **b12531: VoxCPM2の音声生成（TTS）に対応**（mtmd、PR #32443）。speech runtimeへ新しい音声モデル系列を追加した。元のモデル実装の全モードを置き換えるものではなく、一部モードは未対応。一般のtext生成速度の改善ではない。
- **b12535: Vulkanにstream-k方式のMUL_MATを実装**（PR #28528）。行列積の作業量を全SMへ均等に割り振る方式で、現在はcoopmat2経路でのみ有効化される。対象はVulkan backendであり、CUDA経路の高速化を意味しない。公式のend-to-end速度倍率は未提示。
- **b12543: MetalのCONV_2Dへtensor API kernelを追加し、split-Kを全chipへ拡張**（PR #32542）。tensor API対応device（M5等）で畳み込みのreductionを分割し、threadgroup不足によるGPUの遊休を減らす。Apple Silicon向けの変更。
- その他はbackend別の正確性・互換性修正が中心である: recurrent stateのsticky NaN修正（b12529）、WASM Relaxed SIMDとq3_K / q6_K対応（b12530）、OpenCLのdecomposed Flash AttentionでのKV padding調整（b12532）、Vulkanのstorage-only FP16 zero修正（b12534）、IQ2量子化作成のcacheによる高速化（b12541、量子化作成時の処理であり推論速度ではない）、Qwen3-VLのEAGLE-3向け入力設定（b12542）、WebGPUのPOOL_2D対応（b12547）、Inkling 2のattention mask修正（b12549）、CUDAのbatched tensor write向けscatter kernel（b12551）、OpenVINO backendの修正・最適化（b12552）等。一般的な生成速度倍率は公表されていない。

一次資料: https://github.com/ggml-org/llama.cpp/releases/tag/b12531 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12535 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12543 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12553

## 2026-10-29〜11-18 — llama.cpp b11963〜b12483（開発ビルド）と v1.0.0（正式版）

b11936の続き。対象期間の開発ビルドはb11963（2026-10-29）からb12483（2026-11-18）まで。重要変更だけを拾う。

- **v1.0.0（2026-11-13、正式版）**: 初の正式版タグ。deprecated public API削除、NextN / speculative APIの `llama.h` への昇格（breaking相当）。OCP FP8 KV cache、host-memory MoE expert cache、external PLE shard読込を収録。新text architectureとしてKimi-K3.1-Pro、Ripple、xing4_0等に対応。server側はSSRF / CORS / DNS rebinding対策、MCP tool cancellation、OpenAI互換 `/v1/audio/speech` endpoint追加。対応nightlyはb12359。
- **量子化**: b12000でOCP FP8 E4M3 supportを追加（新規形式対応として最重要）。b12274でFP8 KV-cache support（`-ctk/-ctv f8_e4m3`、v1.0.0に収録）。OpenCLのq2_0 / iq3 / iq4_xs初期対応、HexagonのQ5_0 / Q5_1 / IQ2_XXS / NVFP4対応などbackend別の拡張も進んだ。
- **新モデルアーキテクチャ対応**: Nemotron 3.5 Transcribe（b12087、mtmd）、Kimi-K3.1-Pro（b12180）、Kimi K3.1 vision（b12259、mtmd）、Inkling 2（b12406）、Recursive Ripple-65B-Preview向けDFLASH2対応（b12416）、MiniMax-M3.1（b12420）等。TTS / ASR系の追加も多い。
- **backend / kernel**: host-memory MoE expert cache（b12170〜b12206、miss時はCPU実行、CPU share設定可）、CUDAのNVFP4 gate/up matmul＋GLUのMMQ融合（b12122）、CUDA MoEデータレイアウト線形化（b12144）、CUDA prefill最適化（b12329、NVFP4 checkpoint向け）、OpenCL Flash Attentionによるdecode改善（b12118）、K/V読込順rotationによるL2 cache hit率改善（b12477）等。一般的な生成速度倍率は公表されていない。
- **server**: reference-counted checkpointsの使用（b12141、deep copy置換）、OpenAI互換 `/v1/audio/speech` endpoint（b12238）。

一次資料: https://github.com/ggml-org/llama.cpp/releases/tag/v1.0.0 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12000 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12274 ; https://github.com/ggml-org/llama.cpp/releases/tag/b12483

## 2026-10-27 — llama.cpp b11913〜b11936（開発ビルド）

b11912からb11936までの増分を記録。GitHub上のpre-release開発ビルドであり、正式安定版とは区別する。b11936にはWindows x64 CUDA 12.4 / 13.4配布assetがあるが、Windows 11 + RTX 4070 SUPERでの実測性能は未確認。

- **b11930**: llama-server routerに`--models-memory-max`を追加し、device別メモリ余裕に応じてモデルロード前の使用量推定とidle model unloadを調整。複数モデルを切替えるserver運用向けで、単一モデルの生成速度向上ではない。
- **b11928**: MiniCPM-OCR-Jevの判定modelを追加。`POST /v1/systemone`で画像に対するOCR textをscoreする。通常の文章生成用LM headはない。
- **b11926 / b11927 / b11936**: GLM5-Next / QSA / DSAのsparse selectionとdense `kq_mask`依存を整理し、Metal fused top-k maskやQwen4Exp / GLM5-Nextのk-pool選択を追加。一般的な生成速度倍率は未公表。
- **b11923**: CPU / CUDA / Metalのnon-contiguous view向けSCALEを拡大し、CUDA stride-aware kernelとsoftcap fusionの正確性guardを追加。対象view patternに限る。
- **b11918**: OpenCLへQ3_K matmulとmatvecを追加。Adreno向けを含み、CUDA backendへの追加ではない。
- **b11933**: VulkanのMUL_MAT dim-3 broadcastでCPU fallbackになるケースを修正（Vulkan固有）。
- b11913 Hexagon VTCM override、b11922 replay test、b11929 CLI model指定、b11935 RPC error handlingも含まれる。テストやbackend固有変更を一般的な速度改善と扱わない。

一次資料: https://github.com/ggml-org/llama.cpp/releases/tag/b11936 ; https://github.com/ggml-org/llama.cpp/releases/tag/b11930 ; https://github.com/ggml-org/llama.cpp/releases/tag/b11928 ; https://github.com/ggml-org/llama.cpp/releases/tag/b11926 ; https://github.com/ggml-org/llama.cpp/releases/tag/b11927 ; https://github.com/ggml-org/llama.cpp/releases/tag/b11923 ; https://github.com/ggml-org/llama.cpp/releases/tag/b11918 ; https://github.com/ggml-org/llama.cpp/releases/tag/b11933

## 主要更新

### 2026-10-24 — llama.cpp b11846〜b11869（開発ビルド）\n- **b11850**: Soprano-80M / Soprano-1.1-80Mの音声生成に対応。Qwen3系backboneとVocosを使い、音声は生成後に1 chunkで返す。逐次streamingではない。\n- **b11854**: Vulkan行列演算の精度・overflow処理を調整。backend・shapeごとの検証が必要。\n- **b11861**: MiniMax M3系NVFP4/MXFP8 scaleを計算graphへ渡さない不具合を修正。対象構成では数値異常を避ける正確性修正で、一般CUDA高速化ではない。\n- **b11868**: Qualcomm Hexagonの複数core Flash Attentionを調整。Snapdragon向けでRTX CUDAの改善ではない。\n- **b11869**: Jinja templateの`select` / `selectattr`引数処理を修正し、model template互換性を改善。\n- b11869は開発build（pre-release）。Windows x64 CUDA 12系 / CUDA 13系assetの配布は確認済みだが、Windows 11 + RTX 4070 SUPERの実測性能は未確認。\n- 出典: [b11850](https://github.com/ggml-org/llama.cpp/releases/tag/b11850) / [b11854](https://github.com/ggml-org/llama.cpp/releases/tag/b11854) / [b11861](https://github.com/ggml-org/llama.cpp/releases/tag/b11861) / [b11868](https://github.com/ggml-org/llama.cpp/releases/tag/b11868) / [b11869](https://github.com/ggml-org/llama.cpp/releases/tag/b11869)\n\n### 2026-10-23 — llama.cpp b11828〜b11840（開発ビルド）\n- **b11829**: reranking用templateの置換を修正。**b11835**: SYCL/oneDNNのdevice引渡しを修正。**b11838**: `ggml_time_us`の時間overflowを修正。**b11840**: Qualcomm Hexagon NPUにCEIL演算（f32/f16）を追加。\n- いずれも開発ビルドの更新で、一般的な速度倍率は示されていない。b11840のHexagon機能をNVIDIA CUDAの改善と読み替えない。[b11829](https://github.com/ggml-org/llama.cpp/releases/tag/b11829) / [b11835](https://github.com/ggml-org/llama.cpp/releases/tag/b11835) / [b11838](https://github.com/ggml-org/llama.cpp/releases/tag/b11838) / [b11840](https://github.com/ggml-org/llama.cpp/releases/tag/b11840)\n\n### 2026-10-22 — llama.cpp b11813〜b11827（開発ビルド）
- **b11822**: Qwen4ExpでDFlash草稿を使うとhyper-connection残差の形状が合わず最初の要求が停止する問題を修正。草稿が要求する層だけ残差ストリームの平均を構築する。
- **b11823**: GLM5で不要な`sel_mask_2d`と`new_pool_flat`を渡さない入力グラフへ整理。速度倍率は示されていない。
- **b11826**: MiniCPM-OCR 1.0のマルチモーダル処理を追加。全GGUF・GPU構成の動作保証ではない。
- **b11827**: Qualcomm Adreno向けOpenCLのdepthwise 2D convolutionを追加。NVIDIA CUDA向け改善と混同しない。
- **b11819**: Nemotron系の非標準GQA、BPE tokenizer、Domyn small pre-typeへ対応。
- **b11821**: Intel XMX/SYCL量子化行列積の複数列処理を拡張。投機的検証2〜8 tokenまたは短入力9〜80 token向けの経路で、Intel XMX専用。
- **b11818**: reranking APIの型付きcontent入力と画像対応を改善し、template非対応モデルへの画像入力は黙って捨てず拒否する。
- **b11815**: SYCLの非連続入力で起きるCONV_2D誤計算を修正。対象テストは16失敗から0へ回復（速度測定ではない）。
- いずれも開発ビルドの更新で、一般的な高速化倍率はreleaseにない。b11827は2026-10-22 UTC時点の最新確認版。Windows x64 CUDA配布や12GB VRAMでの実機性能は別途確認が必要。[b11815](https://github.com/ggml-org/llama.cpp/releases/tag/b11815) / [b11818](https://github.com/ggml-org/llama.cpp/releases/tag/b11818) / [b11819](https://github.com/ggml-org/llama.cpp/releases/tag/b11819) / [b11821](https://github.com/ggml-org/llama.cpp/releases/tag/b11821) / [b11822](https://github.com/ggml-org/llama.cpp/releases/tag/b11822) / [b11823](https://github.com/ggml-org/llama.cpp/releases/tag/b11823) / [b11826](https://github.com/ggml-org/llama.cpp/releases/tag/b11826) / [b11827](https://github.com/ggml-org/llama.cpp/releases/tag/b11827)

### 2026-10-21 — llama.cpp b11800〜b11803（開発ビルド）
- **b11800**: `ggml_top_k_mask`を一般化し、Qwen4系 / GLM5.3-nextのQSAに加えてDeepSeek V4 CSA等のtop-k maskを融合。backendが演算を実装しない場合は既存経路を使う。releaseに実機速度倍率はない。
- **b11801**: SenseNova U1（NEOChatModel）のdense理解枝とvision encoderをGGUF変換・model実装へ追加。MoT生成枝は非対応。
- **b11802**: Jinja namespace属性と辞書method名が衝突する問題を修正。
- **b11803**: Recursive Flint（`FlintForCausalLM`）のmodel構造を追加。Windows x64 CUDA 12.4 / CUDA 13系buildの配布を確認。GGUF量子化版や12GB VRAMでの実用動作は別途確認が必要。
- 開発ビルドの更新として記録し、一般的な速度向上とは解釈しない。[b11800](https://github.com/ggml-org/llama.cpp/releases/tag/b11800) / [b11801](https://github.com/ggml-org/llama.cpp/releases/tag/b11801) / [b11802](https://github.com/ggml-org/llama.cpp/releases/tag/b11802) / [b11803](https://github.com/ggml-org/llama.cpp/releases/tag/b11803)

### 2026-10-20 — b11744〜b11765（開発版）

- **b11744**: `llama-server --connect`の実験的P2P接続を追加。LAN外から到達できる経路に関わるため、利用時はbind先・外部到達性・アクセス制御を確認する。
- **b11756**: Anthropic互換 `/v1/messages` から内部生成APIへ変換する際に`id_slot`を引き継ぎ、KV cacheを持つslotへのsession固定を可能にする。実測速度倍率は未公表。
- **b11757**: 旧式CUDA memory poolのflush後にCUDA Graphを破棄し、解放済みmemory参照を避ける整合性修正。
- **b11760**: HIP / CUDAのMMF reductionでtile幅が64の倍数でない形状を修正。
- **b11763**: OpenCL MXFP4 matrix-vector経路の範囲外読み取りを修正し、小batch GEMM変種を追加。OpenCL向けでCUDA性能改善とはしない。
- **b11765**: Kolibri-1 routerの冗長なprecision overrideを除去する保守。
- 端から端の速度改善率は未測定。出典: [b11744](https://github.com/ggml-org/llama.cpp/releases/tag/b11744), [b11756](https://github.com/ggml-org/llama.cpp/releases/tag/b11756), [b11757](https://github.com/ggml-org/llama.cpp/releases/tag/b11757), [b11760](https://github.com/ggml-org/llama.cpp/releases/tag/b11760), [b11763](https://github.com/ggml-org/llama.cpp/releases/tag/b11763), [b11765](https://github.com/ggml-org/llama.cpp/releases/tag/b11765)

### 2026-10-19 — b11724〜b11742（開発版）

- **b11724**: CUDA Flash Attention `flash_attn_ext_vec`のshared-memory write-after-read競合を修正。正しさ・安定性の修正で、測定済み速度向上率ではない。
- **b11727**: 分割GGUF / LoRA exportで途中切れのtensorを検知して拒否し、破損出力を避ける。
- **b11729**: Qwen3のbidirectional attentionと`dense_2`出力射影を追加。model互換性の拡張。
- **b11738**: serverのSWA checkpoint無効化条件と`n_past` / prefix境界の扱いを修正。
- **b11741**: OpenCL Q4_0 / Q4_K / Q6_K向けcooperative-K `dp4a` GEMM kernelを追加。OpenCL専用経路。
- **b11742**: Carbon-14B HybridDNAおよび旧Carbon系tokenizerの特殊token / merge変換を修正。
- 以上は対象backend / modelの修正・対応で、端から端の生成速度改善は未測定。
- 出典: [b11724](https://github.com/ggml-org/llama.cpp/releases/tag/b11724), [b11727](https://github.com/ggml-org/llama.cpp/releases/tag/b11727), [b11729](https://github.com/ggml-org/llama.cpp/releases/tag/b11729), [b11738](https://github.com/ggml-org/llama.cpp/releases/tag/b11738), [b11741](https://github.com/ggml-org/llama.cpp/releases/tag/b11741), [b11742](https://github.com/ggml-org/llama.cpp/releases/tag/b11742)

### 2026-10-18 — b11717〜b11721（開発版）

- **b11717**: Qualcomm HexagonでHadamard演算とQ1_0 / Q2_0 `GET_ROWS` を追加。Hexagon向けの対応。
- **b11718**: Intel ESIMDのFFN経路を再有効化し、Q8_0融合経路を拡張。Intel向け。
- **b11719**: CUDA Flash Attentionの境界チェック経路を修正。公開資料に速度倍率なし。
- **b11720**: 非連続tensorの `SUM` をCPU / CUDA / Vulkan / WebGPUでサポート。演算対応の追加で、性能計測結果ではない。
- **b11721**: Qwen4Exp向けCUDAで `SCALE → SIGMOID → SCALE → hc_post` を4 kernelから1 kernelへ融合。中間転送・起動費を減らす設計だが、端から端の生成速度への効果は未公表。
- 出典: [b11717](https://github.com/ggml-org/llama.cpp/releases/tag/b11717), [b11718](https://github.com/ggml-org/llama.cpp/releases/tag/b11718), [b11719](https://github.com/ggml-org/llama.cpp/releases/tag/b11719), [b11720](https://github.com/ggml-org/llama.cpp/releases/tag/b11720), [b11721](https://github.com/ggml-org/llama.cpp/releases/tag/b11721), [PR #30602](https://github.com/ggml-org/llama.cpp/pull/30602)

### 2026-10-17 — b11709 / b11710 / b11713 / b11714 / b11715（開発版）
- **b11709**：Aleph Alpha Kolibri-1のmodel構造を追加。model対応の追加であり、weightの初回公開日とは別。
- **b11710**：CUDA grouped-expertのTop-k融合を追加。MoE中間演算を減らす狙いだが端から端の速度倍率は未確認。
- **b11713**：低bit MMVQ CUDA kernelを更新。公式PRの`llama-bench`ではRTX 4090 / Qwen3.5-9B / Q3_K_S / `tg128`が162.65→174.93 tok/s（約1.08倍）、Q2_Kが181.37→186.79 tok/s（約1.03倍）。RTX 3090では同条件Q3_K_Sが81.04→126.22 tok/s（約1.56倍）。特定GPU・model・quantizationの結果でRTX 4070 SUPERや全modelへ一般化しない。
- **b11714**：model管理UIへHugging Face model発見・downloadを追加し、対応するMTP / DFlash sidecarを同時取得できる。発見機能は既定で無効。download利便性でありlocal decode高速化の保証ではない。
- **b11715**：AMD HIPのQ1_0 unpackを更新。AMD向けでNVIDIA CUDAの改善ではない。
- すべて正式版v0.7.0以後の開発用pre-release。b11713のベンチはモデル全体の一条件の測定で、他GPU・設定へ外挿しない。[b11709](https://github.com/ggml-org/llama.cpp/releases/tag/b11709) / [b11710](https://github.com/ggml-org/llama.cpp/releases/tag/b11710) / [b11713](https://github.com/ggml-org/llama.cpp/releases/tag/b11713) / [b11714](https://github.com/ggml-org/llama.cpp/releases/tag/b11714) / [b11715](https://github.com/ggml-org/llama.cpp/releases/tag/b11715)

### 2026-10-16 — b11695 / b11699 / b11700（開発版）
- **b11695**：Mellum 2.1のMTP対応とRoPE構築処理を追加。対応modelの投機的復号向けで、全model共通の高速化ではない。
- **b11699**：HTTP clientが`HTTP_PROXY` / `HTTPS_PROXY`と`NO_PROXY`、loopback例外を処理し、企業proxy下の取得互換性や子server待機の問題を修正する。
- **b11700**：IBM Granite Switch判定modelに対応。機能の追加・取り消しcommitが同じbuildに含まれるため、最終的な公開buildで挙動を確認する。
- いずれも正式版v0.7.0より新しい開発用pre-release。b11699のWindows x64 CUDA 12配布物はCUDA 12.4 DLLを参照する。これらに共通する速度倍率は報告されていない。[b11695](https://github.com/ggml-org/llama.cpp/releases/tag/b11695) / [b11699](https://github.com/ggml-org/llama.cpp/releases/tag/b11699) / [b11700](https://github.com/ggml-org/llama.cpp/releases/tag/b11700)

### 2026-10-15 — v0.7.0（正式版）
- CPU側へ退避したMoE expertをGPU LRU cacheへ載せる`--moe-cache-mib`を追加。複数GPU間のcache共有にも対応し、公式release noteは対象条件で復号速度最大約2.2倍を報告する。model、GPU、cache hit率で変わり、一般化できない。
- LiLiCorrによるDFlash draft、GLM5-NextのMTP / sparse-attention経路、draft microbatchを独立指定する`--spec-draft-n-ubatch`を追加。pooled embeddingでは不要なLM head計算とlogits bufferを省き、公式値は該当経路のVRAM最大10分の1（通常生成には適用されない）。
- 互換性注意：`llama-server`既定portを8080から9931へ変更（Docker内部portは8080のまま）。chat session APIと整形済み出力形式にも変更があるため、client・proxy・起動scriptを確認する。[正式版](https://github.com/ggml-org/llama.cpp/releases/tag/v0.7.0)。

### 2026-10-14 — b11622：Jinja JSON浮動小数点表現の精度修正（開発版）
- Jinjaの`tojson`、`string`、`safe`で浮動小数点数がC++既定の有効桁数6桁へ丸められる問題を修正し、元値へ読み戻せる短い表現を使う。ツール引数やtemplate内の数値を保つ互換性・正確性の修正で、一般的な生成速度向上ではない。
- **開発ビルド（pre-release）**であり、正式版として扱わない。[公式版](https://github.com/ggml-org/llama.cpp/releases/tag/b11622)／[PR #30362](https://github.com/ggml-org/llama.cpp/pull/30362)

### 2026-10-14 — llama.cpp b11588〜b11602：画像MTP・Vulkanホストメモリ・埋め込み・アリーナ修正
- **b11588**: Qwen3.8-Flash-Nextで画像埋め込みと複数トークン予測（MTP）を組み合わせる経路に対応。視覚入力と投機的生成の互換性改善。[公式版](https://github.com/ggml-org/llama.cpp/releases/tag/b11588)／[PR #30397](https://github.com/ggml-org/llama.cpp/pull/30397)。
- **b11594**: Vulkanで複数デバイスからGPU可視ホストメモリへのアクセスを改善。Windowsを含むVulkan経路の変更であり、**CUDA固有の改善ではない**。[公式版](https://github.com/ggml-org/llama.cpp/releases/tag/b11594)／[PR #29741](https://github.com/ggml-org/llama.cpp/pull/29741)。
- **b11597**: プーリング埋め込みで語彙logits算出に必要な不要の言語モデル出力ヘッド（LM head）計算とホストバッファを省略。**一般の生成復号の一律高速化とは異なる**。[公式版](https://github.com/ggml-org/llama.cpp/releases/tag/b11597)／[PR #30445](https://github.com/ggml-org/llama.cpp/pull/30445)。
- **b11602**: メモリアリーナ再確保後のサブグラフ再生成で整合性を修正。定量的な性能改善は未報告。[公式版](https://github.com/ggml-org/llama.cpp/releases/tag/b11602)／[PR #30453](https://github.com/ggml-org/llama.cpp/pull/30453)。

### 2026-10-13 — llama.cpp b11569〜b11577：MoE・CUDA注意・判定モデル対応
- **b11569（10/12公開）**: Metal版の専門家混合（MoE）行列積 `MUL_MAT_ID` で同一専門家IDが重複する場合の出力不整合を修正し、不要な起動タイルを削減。限定ベンチマークでは入力処理が約0.5〜2%向上、逐次生成はほぼ不変。**Metal限定でありWindows CUDAの高速化とは別**。[公式版](https://github.com/ggml-org/llama.cpp/releases/tag/b11569)
- **b11572／b11577**: vLLM D3系の判定モデル対応を追加し、後続版で複数系列の問題を修正。一般の会話モデル全体の速度改善ではない。[b11572](https://github.com/ggml-org/llama.cpp/releases/tag/b11572)／[b11577](https://github.com/ggml-org/llama.cpp/releases/tag/b11577)
- **b11576（10/13公開）**: head size 512のキャッシュなし注意機構でCUDA `FLASH_ATTN_EXT` がCPUへフォールバックすることがある不具合を、鍵・値とマスクのパディングにより修正。対象形状でのみGPU経路回復を見込める。Windows向けCUDA配布物もあるが、一般モデルの一律高速化倍率は未報告。[公式版](https://github.com/ggml-org/llama.cpp/releases/tag/b11576)
- **b11574**: Snapdragon Hexagon NPU向けコピー・連結等を最適化し、メモリ同期の問題も修正。**NVIDIA CUDAには直接適用されない**。[公式版](https://github.com/ggml-org/llama.cpp/releases/tag/b11574)

### 2026-10-12 — llama.cpp b11559 / b11558：OpenCL改善
- b11559: OpenCL版FlashAttentionがkey次元512とGQA4/GQA8に対応。gpt-oss-20b MXFP4のOpenCL限定ベンチマークでは16.59→29.01トークン/秒（1.75倍）。**NVIDIA CUDAへ同倍率を外挿しない**。[公式版](https://github.com/ggml-org/llama.cpp/releases/tag/b11559)、[PR #30266](https://github.com/ggml-org/llama.cpp/pull/30266)。
- b11558: OpenCL版の巨大量子化重み、ブロードキャストとRMSNormの不整合を修正。速度の定量値は未報告。[公式版](https://github.com/ggml-org/llama.cpp/releases/tag/b11558)、[PR #30310](https://github.com/ggml-org/llama.cpp/pull/30310)。

### 2026-10-11 — llama.cpp b11554〜b11556：新モデルとMoE
- b11556: Prism Bonsai 2 27Bの重み変換・読み込みに対応。ただし配布形式の全てで標準版完全互換を実証したものではない。[PR #29600](https://github.com/ggml-org/llama.cpp/pull/29600)。
- b11555: AVX2 CPU上のF16C命令判定修正。CUDAの速度改善とは別。[PR #30270](https://github.com/ggml-org/llama.cpp/pull/30270)。
- b11554: VulkanのMoE重複expert ID処理を効率化。報告速度改善は約1%でありCUDAに適用できない。[PR #29998](https://github.com/ggml-org/llama.cpp/pull/29998)。

### 2026-10-10〜11 — llama.cpp b11538 / b11540 / b11541 / b11551 / b11552
- b11552: 並列要求で利用中のスロットのプロンプトキャッシュを誤上書きし得る問題を修正。[PR #30295](https://github.com/ggml-org/llama.cpp/pull/30295)。
- b11551: MiniCPM-V 4.7の画像・動画入力向け3D RoPE等を先行実装。[PR #29416](https://github.com/ggml-org/llama.cpp/pull/29416)。
- b11540: Intel Arc / SYCL / MXFP4 MoEの限定条件でデコード1.91〜2.02倍。NVIDIA CUDAでの改善を意味しない。[PR #29809](https://github.com/ggml-org/llama.cpp/pull/29809)。
- b11541: OpenCL低ビットMoE行列積の更新。[公式版](https://github.com/ggml-org/llama.cpp/releases/tag/b11541)。
- b11538: Windows MSVC/CUDAで丸め一致性を修正。生成速度の向上は未検証。[PR #30229](https://github.com/ggml-org/llama.cpp/pull/30229)。
- Windows MLとllama.cpp/GGUFの実験的統合（10月7日）。既存CLIの自動置換ではない。[Microsoft公式](https://devblogs.microsoft.com/foundry-on-windows/build-on-winml-oct-7-26/)。

### 2026-10-09 — b11513：CUDAの上位k件選択（Top-k）の形状別最適化

- CUDAの上位k件選択で行数・列数に応じて複数の選択アルゴリズムを使い分ける。Qwen4Expの34,816トークン条件では演算単体の実行時間が5,761.8→941.8 ms（約6.12倍）となったが、**モデル全体が6倍高速になるわけではない**。DGX Station GB300でのQwen3.8-Flash-Nextのプリフィルは1,755.8→2,852.8 tok/s（約1.625倍）、通常生成は100.08→99.89 tok/sでほぼ不変。Windows RTX 5090での形状別正当性試験527/527通過、RTX 4070 SUPERでの実速度は未計測。
- 公式資料: [開発ビルド b11513](https://github.com/ggml-org/llama.cpp/releases/tag/b11513)、[PR #28713](https://github.com/ggml-org/llama.cpp/pull/28713)。

### 2026-10-08〜09 — b11480 / b11507：CPU退避したMoE専門家のGPUキャッシュ

- CPU RAMへ退避した混合専門家（Mixture of Experts、MoE）の重みをGPU側の最近使用順（LRU）キャッシュへ保持し、キャッシュを外れた専門家をCPUから転送する。実装フラグは `--moe-cache-mib N`（GPUごとのMiB）。b11507では層分割型の複数GPUへ拡張。小バッチ（最大32トークン）で効果がある経路であり、2026-09-05時点の**Draft PR**にあった `--moe-expert-cache` と混同しない。
- 公式の単一GPU試験（Qwen3.8-Flash-Next Q4_0、93.7GiB、CPU側に専門家65.4GiB、EPYC 7742）ではRTX 4090の生成25.0→39.4 tok/s（1.57倍、キャッシュ6,544MiB）、RTX 5090で30.8→54.5 tok/s（1.77倍）。RTX 4090×2では34.78→60.38 tok/s（1.74倍）だが、プリフィルは440.7→402.0 tok/s（約9%低下）。15,000MiB指定で生成64.39 tok/sに改善した一方、プリフィル321.5 tok/sまで低下。これらは該当モデル・接続条件での比較で、キャッシュ常駐量は他の層やKVキャッシュとGPUメモリを競合する。
- Windows 11／RTX 4070 SUPER 12GB／RAM 32GBでは同規模93.7GiBモデルを保持できないため速度倍率は外挿しない。より小型のMoEでGPU空き容量と転送条件を測定する必要がある。
- 公式資料: [b11480](https://github.com/ggml-org/llama.cpp/releases/tag/b11480)、[PR #29887](https://github.com/ggml-org/llama.cpp/pull/29887)、[b11507](https://github.com/ggml-org/llama.cpp/releases/tag/b11507)、[PR #30112](https://github.com/ggml-org/llama.cpp/pull/30112)。

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
