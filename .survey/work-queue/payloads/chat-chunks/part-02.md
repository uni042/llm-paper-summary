## Fused-Fit
Head-Localでもtarget layerごとに選択source layer集合が異なるため、素朴な実装では非連続gather、centering、weighting用tensorのmaterializeが大量に発生する。Fused-Fitはridge solverが必要とするweighted mean、covariance、cross-covarianceという十分統計だけを構築する。

2-passの新しいGPU kernelで、最初にweighted meanを求め、2回目に観測をbounded chunkで走査する。kernel内で選択されたhead-local blockのgather・center・weightを行い、連続したper-head panelへ出力してhead-batched matrix multiplicationで統計量を蓄積する。したがってfull observation tensorを保持せず、scratch memoryはchunk sizeに対してboundedになる。ridge solver、regularization、serialized mapper schema、online affine interfaceは維持される。

## 評価条件
- **Transfer directions**:
  - Ministral 3 3B → 14B
  - Ministral 3 8B → 14B
  - Qwen3 14B → 32B
- **Attention**: すべてdense GQA、source/targetとも8 KV heads
- **Calibration**: FineWeb-Edu、長さ1,024 token。主要比較は500 sequence、4 tokenごとにsampleして128,000 token position
- **Selected source layers**: 3B→14Bで20、8B→14Bで12、Qwen3で8
- **Ridge**: `lambda=0.01`。比較法でcalibration row、layer selection、ridge strength、token sampling、evaluation exampleを固定
- **Quality**: HellaSwagを含むtask accuracy、target standaloneに対するmean target retention、NLL、KV reconstruction R²
- **System metrics**: serialized mapper storage、1,024-token prefixのmapper application latency、offline mapper construction time
- **Construction timing**: Qwen3の500-sequence構築は4×NVIDIA H800で測定。trace collection、layer selection、attention-weight生成、evaluation、scheduler delayは除外し、mapper construction部分のみを測る

## 主要結果

### Quality recovery
Full-Head Mappingは同じ8-head KV interfaceでもMinistral 3で大きく崩れる。HellaSwagでは、
- Ministral 3 3B→14B: **52.2% → 72.6%**（CacheBridge、+20.4 pt）
- Ministral 3 8B→14B: **44.4% → 76.0%**（+31.6 pt）

mean target retentionはそれぞれ **65.89% → 88.23%**、**59.43% → 97.57%**へ改善する。一方Qwen3 14B→32Bでは既存full-headも比較的良好で、CacheBridgeは**99.83%**を維持し、Full-Head Mappingの99.72%と同等以上だった。

### Mapper容量とonline cost
Qwen3 14B→32Bではserialized mapper storageを **4.296 GB → 0.538 GB**へ削減し、理論どおり約8分の1になった。1,024-token prefixでのapplication latencyは **65.12 ms → 21.66 ms**で、最大**3.0×高速**。target側re-prefillを避ける目的に対して、mapper自体のsupport幅がhandoff costを食い潰す問題を抑えている。

### Calibration効率とAttn-Repair
Qwen3では50 calibration sequencesでもCacheBridgeは**99.89% mean retention**を得て、Full-Head Mappingの500 sequencesでの99.44%を上回るbudget sweep結果を報告する。attention weightingはKV R²自体をほぼ改善しない一方、continuation retentionやlong-prefix NLLを改善しており、「coordinate reconstructionが良いこと」と「receiverの生成品質が良いこと」を分離して示している。

具体例としてQwen3でK/V R²はおおむね **0.678/0.655 → 0.672/0.654**と変わらないが、4KでのNLLは **2.446 → 2.350**へ低下した。
