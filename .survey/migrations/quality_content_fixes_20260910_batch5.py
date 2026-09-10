#!/usr/bin/env python3
"""Fifth content-only quality batch: finish remaining 2024 content gaps."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PATCHES: dict[str, list[tuple[str, str]]] = {
    "papers/inference/06-moe-quantization-compression/2024-2407.14417-mixture-of-experts-with-mixture-of-precisions-for-tuning-quality-of-service.md": [
        (
            "つまり4 bit化は圧縮そのものが目的ではなく、**より多くのexpertをGPUへ常駐させてcache miss / PCIe transferを減らすためにも使われる**。",
            "同じVRAM予算で16 bitへ戻すexpertを1個増やすと、その分だけ複数の4 bit expertをGPUへ置けなくなる可能性がある。quality優先では、その精度改善で得られる品質利得がresident expert減少によるPCIe転送増加を上回る範囲まで16 bit化する。一方throughput優先では、まず実行時に選ばれるexpertをできるだけGPUへ常駐させ、CPUからのweight transferを減らすことを優先し、残った容量だけを高精度化へ使う。したがって最適点は固定の量子化率ではなく、利用可能VRAM、expert利用分布、PCIe帯域、要求負荷によって変わる運用上の設定である。",
        ),
        (
            "本研究の価値は、expertの意味的重要度を学習することではなく、変動するGPUメモリを前提に精度・配置・転送を一つのサービス設定として扱う点にある。Mixtral 8x7Bのexpertを4 bitまたは16 bitで保持し、GPUに載らないものはCPUへ置くことで、VRAM予算に応じて品質とthroughputを切り替える。",
            "ここでは『低bitにすれば速い』と『GPUへ多く常駐できれば速い』を分けて考える必要がある。量子化で直接変わるのは1 expertあたりの保存容量と演算形式だが、serving全体では容量削減によってGPU resident expert数が増え、CPUからのweight転送回数が減る効果の方が大きい場合がある。逆に全expertがGPUへ収まる条件ではresident率改善の余地がなくなり、低bit kernel自体の実行効率と品質差が主要な判断材料になる。",
        ),
    ],
    "papers/inference/06-moe-quantization-compression/2024-2410.06270-mixture-compressor-for-mixture-of-experts-llms-gains-more.md": [
        (
            "単に「よく使われるexpertを高bitにする」だけではなく、**量子化すると壊れやすいexpertにも高bitを残す**のがポイントである。",
            "3種類の指標は異なる失敗を捉える。routing頻度はそのexpertの量子化誤差が何回繰り返し出力へ混ざるかを示し、routing scoreは選ばれたときにそのexpertの寄与がどの程度大きいかを示す。再構成誤差は、その重みを低bitへ落としたときに元のexpert出力をどれだけ再現しにくいかを表す。頻繁に使われても寄与が小さいexpert、利用頻度は低くても選ばれたときの寄与が大きいexpert、利用頻度とは無関係に量子化へ弱いexpertがあり得るため、どれか1指標だけでbit幅を決めると容量配分を誤りやすい。PMQはこれらをまとめて、限られた総bit予算を『高精度を残す価値が高いexpert』へ優先配分する。",
        ),
        (
            "各expertに1.5〜2.5 bit程度の候補を持たせ、**モデル全体で使える保存容量を超えない範囲で、どのexpertへ何bitを割り当てるかを組み合わせ最適化**して最終配置を決める。non-expert部分は4 bit固定である。",
            "PMQの判断は推論前に一度行う静的な圧縮であり、tokenごとにbit幅を切り替える方式ではない。したがって実行時には各expertの保存形式が確定しており、低bit化したexpertはモデル保存容量だけでなくGPUへ読み込む必要がある場合の転送byteも小さくなる。一方、そのexpertが選ばれるたびに同じ量子化誤差が影響するため、calibration dataが本番routing分布を代表していない場合は、高精度を残すべきexpertを誤る可能性がある。",
        ),
        (
            "ODPはrouting weightだけでなく、attention scoreやfeature magnitudeも見て、重要tokenではpruningを弱める。論文中の「重要token保護」は、**tokenによってexpert削減率を変える安全策**と理解するとよい。",
            "ODPがtoken単位であることもPMQとの大きな違いである。あるtokenで第2・第3候補expertの寄与が小さいと判断して実行を省いても、そのexpertのweight自体を削除するわけではないため、次のtokenでは通常どおり再び選択できる。特にattentionやfeatureから重要と判断されたtokenではnative routingに近いexpert数を維持し、重要度が低いtokenだけ積極的に削ることで、すべてのtokenへ同じpruning率を適用する方式より品質劣化を抑える。つまりODPは『どのexpertをモデルから消すか』ではなく、『このtokenで今どこまで計算するか』を動的に決める。",
        ),
        (
            "したがって「2.54 bit」だけを見てもruntimeの計算量は分からず、「activated parameters」がどこまで減ったかも別に見る必要がある。",
            "二つの圧縮は品質への誤差の入り方も異なる。PMQの量子化誤差は、その低bit expertが実行されるすべてのtokenへ継続的に入る。一方ODPは特定tokenとexpertの組合せだけを省く近似なので、別tokenでは元の計算経路を使える。そのため同じ保存容量でもODP設定によって実行FLOPsは変わり、同じactivated parameter数でもPMQのbit配分によってモデル容量と品質は変わる。運用上は『保存容量の予算』と『tokenあたり計算量の予算』を独立したつまみとして調整し、両者を同時に強くしすぎたときの誤差の重なりを評価する必要がある。",
        ),
        (
            "前者をPre-Loading Mixed-Precision Quantization（PMQ）、後者をOnline Dynamic Pruning（ODP）が担当する。",
            "この分離により、モデルがGPUへ載るかという容量問題と、載った後に1 token生成するのに何個のexpertを動かすかという計算問題を混同せず最適化できる。均一な低bit化だけでは保存量は減っても全expertを毎回native routingどおり実行するためFLOPsは残り、pruningだけでは計算量は減っても全expert weightを保存する容量問題は残る。MC-MoEはこの二つの独立した冗長性を別機構で削る。",
        ),
        (
            "### 3. 二つの圧縮率は意味が違う",
            "### 3. 二つの圧縮率は意味が違う\n\nPMQとODPは同時に使えるが、一方の設定値から他方の効果を推測することはできない。平均bitは『保存している重み1要素あたり何bit使うか』を表し、activated parameterは『そのtokenで何個分のparameterを実際の演算へ通したか』を表す。前者は主に容量・weight load帯域へ、後者は主に演算量へ効くため、評価でも別々の指標として追う必要がある。",
        ),
    ],
    "papers/inference/10-kv-cache-offload-recomputation/2024-2411.01142-neo-saving-gpu-memory-crisis-with-cpu-offloading-for-online-llm-inference.md": [
        (
            "CPU側requestでもQ/K/V projectionやMLPなどの大きなlinear計算はGPUで行う。CPUへ移すのは主に**KVを大量に読むdecode attention**であり、model weight全体をCPUへ移すわけではない。",
            "データ経路としては、GPUが現在tokenのprojectionなどを計算した後、CPU担当requestについては現在token側の小さいquery / activationだけをhostへ渡す。CPUはDRAMに残してある長い過去KVをその場で読み、decode attentionを計算して小さいattention出力をGPUへ返す。これによりcontext長に比例して増える過去KVを毎token PCIeでGPUへ戻す代わりに、tokenごとの小さなactivationだけを往復させられる。したがって長いcontextほど転送削減の価値が増える一方、短いrequestではCPU起動・同期・小転送の固定費が相対的に大きくなりやすい。",
        ),
    ],
    "papers/inference/10-kv-cache-offload-recomputation/2024-2411.17089-kvpr-efficient-llm-inference-with-io-aware-kv-cache-partial-recomputation.md": [
        (
            "論文では、複数要素をまとめた単位ごとにscaleを持たせるgroup-wise 4-bit KV cache compressionも評価している。KVを圧縮すればtransfer量そのものが減るが、KVPRはその上で残ったI/Oとrecomputationを重ねられるため、両者は競合する手法ではなく併用可能である。",
            "量子化を併用すると最適な再計算比率も変わる。KVを4 bitへ圧縮すればCPU→GPUで運ぶbyteが減るため、full-precision KVを前提にしたときより転送側が早く終わり、再計算へ回す割合を小さくした方がよい場合がある。一方で転送したKVにはdequantizationの費用も加わるため、profilerは圧縮後の実測転送時間と復号費用を含めて再び分担を決める必要がある。つまりKV量子化はI/Oそのものを小さくするつまみ、KVPRは残ったI/OをGPU計算へ置き換えて同時進行させるつまみであり、両方を使う場合もhardwareごとにbalance pointを測ることが重要になる。",
        ),
    ],
    "papers/inference/11-llm-serving-scheduling-disaggregation/2024-2406.17565-memserve-context-caching-disaggregated-serving.md": [
        (
            "一方、キャッシュ局所性を優先しすぎれば特定実行単位へ要求が集中するため、実運用では接頭部ヒットで節約できる計算量と待ち行列化遅延、KV転送コストを同じコストモデルで比較する必要がある。",
            "例えば遠隔GPUに非常に長い接頭部KVが残っていれば、それをnetwork経由で取得して再利用する方がローカルで全接頭部を再プリフィルするより安い場合がある。逆に共有部分が短い、networkが混雑している、転送先の待ち行列が長い場合は、キャッシュを捨てて空いた実行単位で再計算した方が早い。分散KVキャッシュでは『ヒットするか』だけでなく、ヒットを使う実コストまで比較する必要がある。",
        ),
    ],
    "papers/inference/11-llm-serving-scheduling-disaggregation/2024-2407.00023-preble-efficient-distributed-prompt-scheduling.md": [
        (
            "この2段構成により、cluster-level routingの判断を各GPUの細かいtoken schedulingから分離する。",
            "全体スケジューラはrequest到着時の比較的粗い粒度で『どのGPUへ所属させるか』を決め、ローカルスケジューラはそのGPU内でiterationごとの実際のbatchを組み直す。これにより全体制御器が全GPUのtoken単位状態を常時追わなくても、接頭部局所性と大まかな負荷を見て配置できる。一方、生成長やKV使用量が実行中に予想から外れても、各GPU側は現在のmemory / queue状態を見ながら短い周期で実行順を調整できる。二つの時間尺度を分けることで、cluster-level配置の制御費用を抑えつつ、実行中の変動へ局所的に追従する。",
        ),
    ],
    "papers/inference/11-llm-serving-scheduling-disaggregation/2024-2407.00047-qlm-queue-management-slo-oriented-llm-serving.md": [
        (
            "特に複数モデル環境では、モデル局所性だけを優先すると急ぎ要求が詰まり、逆にSLOだけを見るとモデル再読み込みが増える。",
            "QLMの自由度が大きいのは、SLOの緩いbatch要求と急ぎのinteractive要求、複数modelが同時に存在するときである。要求ごとの残り余裕が違えば、急ぎを前へ出す代わりに余裕のある要求をmodel localityの良い位置まで待たせられる。逆に全要求が同じmodel・同じ厳しいSLOで到着する場合は並べ替え余地が小さく、QLM固有の利得も通常のload balancingに近づく。",
        ),
    ],
    "papers/inference/11-llm-serving-scheduling-disaggregation/2024-2408.15792-efficient-llm-scheduling-learning-to-rank.md": [
        (
            "論文でいうstarvation対策は、この**長いrequestを永久待ちにしないpriority補正**を指す。",
            "この補正は、理想的なShortest Job Firstを厳密に守ることより、長いrequestにも時間経過とともに処理機会を与えることを優先する。新しい短requestが継続的に到着する高負荷状態では、ranking scoreだけなら長requestが何度でも追い越され得るが、待機時間をpriorityへ足すことで一定時間後には順位が上がる。その代わり平均latencyだけを最小化する理想順からは少し外れるため、性能とstarvation回避のtrade-offになる。",
        ),
        (
            "重要なのは「length predictorの絶対誤差を小さくする」こと自体ではなく、**最終的にschedulerが必要とする順位を直接学習した**点にある。",
            "この利得はqueueに複数requestが並び、どれを先に実行するか選べるときに最も大きい。到着率が低く、GPUがほぼ空いていてrequestが来たらすぐ実行できる状態では、順位を予測しても待ち時間を短縮する余地が小さく、predictorの追加costだけが残り得る。逆に高負荷で短いrequestが長いgenerationの後ろへ多数並ぶほどHead-of-Line blockingが大きくなり、正確なtoken数でなくても短い順を当てる価値が高くなる。",
        ),
    ],
}


def apply_patch(path: Path, anchor: str, addition: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if addition in text:
        return False
    if anchor not in text:
        raise RuntimeError(f"anchor not found: {path}\n{anchor}")
    path.write_text(text.replace(anchor, anchor + "\n\n" + addition, 1), encoding="utf-8")
    return True


def mark_audited(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace('last_audited: null', 'last_audited: "2026-09-10"', 1)
    text = text.replace('audit_version: 0', 'audit_version: 1', 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    changed = 0
    for rel, patches in PATCHES.items():
        path = ROOT / rel
        if not path.exists():
            raise FileNotFoundError(path)
        paper_changed = False
        for anchor, addition in patches:
            paper_changed |= apply_patch(path, anchor, addition)
        if paper_changed:
            mark_audited(path)
            changed += 1
    print(f"content-quality batch5: {changed} paper(s) changed")


if __name__ == "__main__":
    main()
