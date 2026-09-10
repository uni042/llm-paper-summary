#!/usr/bin/env python3
"""Ninth content-only batch: repair D2MoE heading and expand Aug-Sep 2025 papers."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace_once(path: Path, old: str, new: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        if new in text:
            return False
        raise RuntimeError(f"anchor not found: {path}\n{old}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def append_after(path: Path, anchor: str, addition: str) -> bool:
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

    d2 = ROOT / "papers/inference/08-edge-on-device-llm-systems/2025-2504.15299-d2moe-dual-routing-and-dynamic-scheduling-for-efficient-on-device-moe-based-llm-.md"
    duplicated = "### 3. DeviceごとにSSD読込時間と計算時間を実測する\n\n### 3. DeviceごとにSSD読込時間と計算時間を実測する"
    if duplicated in d2.read_text(encoding="utf-8"):
        replace_once(d2, duplicated, "### 3. DeviceごとにSSD読込時間と計算時間を実測する")
        mark_audited(d2)
        changed += 1

    moeq = ROOT / "papers/inference/06-moe-quantization-compression/2025-2505.03804-moequant-enhancing-quantization-for-mixture-of-experts-large-language-models-via.md"
    if append_after(
        moeq,
        "MoEQuantの主貢献は速度より同bitでの品質回復**と見るのが適切である。",
        "したがって、速度比較では量子化カーネル自体の効果と、MoEQuantが較正方法を改善した効果を分離して読む必要がある。",
    ):
        mark_audited(moeq)
        changed += 1

    kv = ROOT / "papers/inference/10-kv-cache-offload-recomputation/2025-2508.13231-accelerating-llm-inference-via-dynamic-kv-cache-placement-in-heterogeneous-memory-system.md"
    if append_after(
        kv,
        "HBM容量制約の下でtotal decode latencyを最小化する。",
        "ここで単純なhot/cold分類だけでは足りない。HBMとDRAMを同時に読めるなら、全hot KVをHBMへ集めるより、両tierの読出し時間が近づくようworking setを分割した方がaggregate bandwidthを使い切れる場合がある。またDRAM→HBM昇格は将来のreadを速くする一方、その瞬間にはinterconnectと両memoryの帯域を消費する。したがって『次stepで何回読まれるか』だけでなく、移動に払うbyteと、その移動が何stepで回収できるかまで含めて配置を決める必要がある。",
    ):
        mark_audited(kv)
        changed += 1

    lexi = ROOT / "papers/inference/02-adaptive-expert-computation-compression/2025-2509.02753-lexi-layer-adaptive-active-experts-for-efficient-moe-model-inference.md"
    paper_changed = False
    paper_changed |= append_after(
        lexi,
        "目的は**同じsynthetic分布上で各layerを比較し、どのlayerがK削減へ敏感か順位付けすること**である。",
        "実データを使わない利点は、deployment taskごとにcalibration setを用意せずcheckpointだけからprofileを作れる点にある。ただしsynthetic hidden stateは実token分布そのものではないため、ここで測っているのはtask accuracyではなく『このlayerのMoE出力がexpert数削減に対してどれだけ構造的に変わりやすいか』という代理指標である。LExIは絶対値よりlayer間の相対順位として使うことでdata-free化している。",
    )
    paper_changed |= append_after(
        lexi,
        "LExIの本質は**Kを減らすこと自体ではなく、同じ総Kをlayer間で再配分すること**にある。",
        "例えば総budgetが全layer平均K=3相当でも、敏感なlayerへK=4を残す代わりに鈍感なlayerをK=1〜2へ落とせる。全layerを一律K=3にする方式では、この『余分な1 expertが品質へ効く場所』と『削ってもほぼ変わらない場所』を区別できない。総active expert数を同じに固定して比較することで、LExIの利得が単なる計算量増加ではなくlayer間の配分改善から来ることを確認できる。",
    )
    paper_changed |= append_after(
        lexi,
        "この表を一度作れば、異なる総expert実行予算に対してmodel forwardを何度も実行せず、Kの配分だけ再探索できる。",
        "またprofileは各layer・各候補Kの局所的な距離を表にしたものなので、総budgetを変えるたびにLLM全体へ大量のcalibration promptを流す必要がない。運用者は同じprofileから品質重視の大きいBとthroughput重視の小さいBを複数作り、serving要件に応じてlayer-wise K設定を切り替えられる。",
    )
    if paper_changed:
        mark_audited(lexi)
        changed += 1

    layerscope = ROOT / "papers/inference/03-expert-prefetch/2025-2509.23638-layerscope-predictive-cross-layer-scheduling-for-efficient-multi-batch-moe-infer.md"
    paper_changed = False
    paper_changed |= append_after(
        layerscope,
        "予測ではTop-kを完全一致させることだけでなく、**次layerで特に使われそうなexpertをどれだけ漏らさず含められるか**を重視する。",
        "prefetch用途では、不要expertを少し余分に予測する誤りと、実際に必要なexpertを予測から漏らす誤りのcostが非対称だからである。前者は余計なPCIe trafficを増やすが、後者はnative router確定後に緊急loadが必要になりGPUを直接待たせる。LLaPorはlayerごとのrouting傾向を学ぶことで、このmissを減らしつつpredictor自体を小さく保つ。",
    )
    paper_changed |= append_after(
        layerscope,
        "重要なのは、**先読みもPCIe帯域を消費するので無料ではない**と扱う点である。先読みを増やしたせいで緊急転送が遅くならないよう、両方を同じ計画に入れる。",
        "multi-batchではこの競合が特に強くなる。各batchが独立に『次layerのexpertを全部先読み』すると、低優先度prefetchだけでPCIe queueが埋まり、現在layerでcache missしたbatchのrequired loadが後ろへ並ぶ可能性がある。PreSchedは将来のprefetch価値と現在のstall costを同じ時間軸で比較し、先読みを抑える・CPU実行へ回す・後でloadするという選択肢まで含めてcross-layer planを作る。",
    )
    paper_changed |= append_after(
        layerscope,
        "LayerScopeはこのCPU実行も候補へ入れ、**転送待ちとCPU計算時間のどちらが短いか**で選ぶ。",
        "この判断はexpert sizeとbatch内token数で変わる。小expertや少数tokenならweight全体をPCIeで運ぶ固定costの方がCPU GEMMより大きくなり得るが、Mixtralのような大expertへ多数tokenが集まるとCPU計算が長くなりGPU実行の方が有利になりやすい。したがってCPU fallbackは一律policyではなく、各expertの転送byte・CPU compute・GPU availabilityを見たcost-based choiceになる。",
    )
    paper_changed |= append_after(
        layerscope,
        "さらに、\n\n- 将来用の低優先度prefetch\n- 今すぐ必要な高優先度transfer\n\nを分けて扱い、background prefetchのせいでGPUが正しいexpertを待たされるのを避ける。",
        "非同期化の目的は単に別threadへI/Oを移すことではなく、GPU計算のcritical pathからprefetch発行・待機を外すことである。高優先度loadはGPUが次に必要とするdeadline付きtraffic、prefetchは余剰帯域で進めるbest-effort trafficとして扱う。これによりpredictorが余分なexpertを候補へ入れても、その転送がnative routingで確定したexpertの到着を妨げにくくする。",
    )
    if paper_changed:
        mark_audited(layerscope)
        changed += 1

    print(f"content-quality batch9: {changed} paper(s) changed")


if __name__ == "__main__":
    main()
