#!/usr/bin/env python3
"""Third content-only quality batch: residual 2024 gaps and four older papers."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PATCHES: dict[str, list[tuple[str, str]]] = {
    "papers/inference/02-adaptive-expert-computation-compression/2024-2402.14800-not-all-experts-are-equal-efficient-expert-pruning-and-skipping-for-mixture-of-e.md": [
        (
            "速度だけでなく、削除率・スキップ閾値・較正領域を一組の運用設定として評価する必要がある。",
            "特に恒久削除の安全性は、較正データが実運用のルーティング分布をどこまで代表しているかに依存する。較正時にほとんど使われなかったエキスパートでも、別ドメインでは重要になる可能性があるため、削除後に入力分布が変わる用途では再較正または元モデルへの復帰手段を用意する必要がある。",
        ),
    ],
    "papers/inference/02-adaptive-expert-computation-compression/2024-2403.18926-xmoe-sparse-models-with-fine-grained-and-adaptive-expert-selection.md": [
        (
            "したがってXMoEの計算量削減は、細かい計算単位を効率よく束ねる実行系と組み合わせて初めて、同程度の壁時計時間（wall-clock time）削減として現れる。",
            "実装時には、同じ小エキスパートを選んだトークンを一度集約してから行列積へ渡し、処理後に元のトークン位置へ戻すような振り分け処理が必要になる。この振り分け費用が大きい場合、理論上の動的計算量削減がそのまま実時間の短縮にはならない。",
        ),
    ],
    "papers/inference/02-adaptive-expert-computation-compression/2024-2406.13233-adamoe-token-adaptive-routing-with-null-experts-for-mixture-of-experts-language-.md": [
        (
            "逆に補助損失が強すぎれば全トークンの構成が似通い、弱すぎればnullへ過度に集中し得るため、計算予算と品質の両方を学習時に調整する必要がある。",
            "またnullエキスパートを選ぶとFFN計算は消えるが、ルータ判定そのものやトークンの振り分け管理まで完全に消えるわけではない。したがって実機での高速化は、削減したFFN演算量がランタイムの分岐・通信・小バッチ化の固定費を十分上回る条件で大きくなる。",
        ),
    ],
    "papers/inference/02-adaptive-expert-computation-compression/2024-2410.17954-expertflow-efficient-mixture-of-experts-inference-via-predictive-expert-caching-.md": [
        (
            "このため三者を直列の独立最適化ではなく、同じ将来ルーティング情報を共有する一つの制御系として扱うことが性能向上の中心になる。",
            "予測距離を長くすると転送を始める猶予は増えるが、誤予測による不要なキャッシュ占有とPCIe転送も増えやすい。したがって予測器は単純に最長距離を選ぶのではなく、転送を隠せる時間と予測精度の両方が有利になる範囲で使う必要がある。",
        ),
    ],
    "papers/inference/03-expert-prefetch/2024-2501.10375-daop-data-aware-offloading-and-predictive-pre-calculation-for-efficient-moe-infe.md": [
        (
            "したがってDAOPでは通常時の先行計算による無損失な待ち時間削減と、混雑時の品質・遅延交換を分けて評価する必要がある。",
            "この設計はCPU側に十分な演算余力があることも前提にする。CPUが他処理で飽和していたり、複数のCPUエキスパート計算が競合したりすると、先行計算を始めても次層までに結果が間に合わずGPU待ちが残るため、CPU負荷も配置判断の重要な条件になる。",
        ),
    ],
    "papers/inference/04-conditional-computation/2024-2407.14057-lazyllm-dynamic-token-pruning-for-efficient-long-context-llm-inference.md": [
        (
            "これにより「一度外したtokenを復帰できる」柔軟性を保ちつつ、同じtoken×layerの計算を何度も繰り返すことを避ける。",
            "復帰が必要になるのは、ある生成ステップでは重要度が低かった入力トークンが、後続の生成内容によって再び高いAttentionを受ける場合である。静的なプロンプト圧縮ではこのトークンは永久に失われるが、LazyLLMは途中層の隠れ状態を補助キャッシュ（Aux Cache）へ残すため、必要になった層から後段計算へ再参加させられる。これにより『現在は不要』という判断を『会話全体で不要』という不可逆な判断へ変えずに済む。",
        ),
        (
            "その代わり、layerごとに異なるtoken集合を管理し、外したtokenを後で復帰させるindex管理自体がruntime overheadになる。",
            "実行時には、各層で残ったトークンを連続したテンソルへ詰め直し、AttentionとFFNを計算した後に元の系列位置との対応を維持する必要がある。保持トークン数が減っても、この収集・索引管理・補助キャッシュ参照が大きいとGPUの密な行列演算効率を失うため、削減率と実時間短縮は一致しない。特に少数トークンだけを不規則に残す強い枝刈りでは、演算量の削減より小さなカーネル起動やメモリアクセスの固定費が目立ちやすい。",
        ),
        (
            "どのlayerから削り始めるか、各段階で何割残すか、何layerを対象にするかが品質とlatencyの主な調整parameterになる。",
            "浅い層で残す割合を高くする理由は、初期表現を早く捨てると後段の重要度判定そのものが不安定になりやすいためである。後段ほど文脈表現が整理された後なので選択を強くできるが、長距離依存を必要とするタスクでは後半でも遠い入力トークンが再び重要になる。このため保持率は単なる速度つまみではなく、情報をいつまで候補として残すかを決める品質制約でもある。",
        ),
    ],
    "papers/inference/04-conditional-computation/2024-d-llm-a-token-adaptive-computing-resource-allocation-strategy-for-large-language.md": [
        (
            "ただし長距離文脈を失いやすくなるため、文頭の最初 `m` tokenは必ずKVを残す。本実験では `m=2` が最良だった。",
            "このKV除外が必要なのは、あるトークンが層を飛ばした場合、その層にはそのトークンのK/Vが存在しないからである。後続トークンだけが同じ層を実行して欠損した位置を通常のAttention対象に含めると、系列内で参照可能な状態が不整合になる。D-LLMは欠損位置を明示的にAttention対象から外し、『計算しなかった状態を存在するものとして扱わない』ことで動的深度とKVキャッシュを整合させる。",
        ),
        (
            "全32 layerを完全自由にrouteしているわけではない。",
            "先頭層を固定することは学習安定性だけでなく、すべてのトークンが共有する最低限の表現基盤を確保する役割も持つ。各トークンが最初から別経路へ分かれると、後段の決定モジュールが受け取る隠れ状態の分布まで大きくばらつくため、実行／スキップ判断の学習が難しくなる。固定前段を置くことで、動的分岐を後半の冗長性が大きい領域へ限定している。",
        ),
        (
            "元checkpointへ推論時だけ差し込むtraining-free手法ではない。",
            "決定モジュールの判断は、その判断によって途中層を飛ばした状態でも最終タスクを解けるようにモデル本体と共同で適応する必要がある。したがって既存チェックポイントへ未学習の判定器だけを追加しても、スキップ後の表現変化やKV除外に本体が適応しておらず、論文と同じ品質・計算量交換は期待できない。",
        ),
    ],
    "papers/inference/04-conditional-computation/2024-layerskip-enabling-early-exit-inference-and-self-speculative-decoding.md": [
        (
            "最適点は単なる「浅いほど速い」ではなく、draft acceptanceとのバランスで決まる。",
            "例えば終了層を浅くすると1個の下書きトークンを作る費用は小さくなるが、後段層で否認される割合が増えれば、まとめて作った後続下書きも無駄になる。逆に終了層を深くすると受理率は上がるが、下書き生成そのものが完全モデルに近い費用へ戻る。したがって最適な終了層と下書き長は、下書き1トークンの費用、受理される連続長、検証を一括実行する効率の積で決まる。",
        ),
        (
            "またdraft時に作った前半layerのactivation/KVをverificationでも再利用できる。",
            "同一モデルを使う利点は、重みの共有だけではない。下書き段階で終了層まで計算済みの各トークンについて、検証時は同じ前半層をもう一度通さず、その中間表現から残りの層だけをまとめて実行できる。別の小型下書きモデルを使う方式では下書き側の計算結果を標的モデルの途中状態として直接再利用できないため、この共有計算がLayerSkip固有の速度・メモリ利点になる。",
        ),
        (
            "既存Llama checkpointへruntimeだけ追加して同じ結果が出るわけではない。",
            "学習時の層ドロップアウト（layer dropout）は複数の深さで残る層を使う経験を与え、途中終了損失（early-exit loss）は各中間表現を同じ語彙出力へ読み出せるようにする。前者だけでは浅い表現が次トークン予測へ十分整列する保証がなく、後者だけでは後半層を抜いた経路に本体が慣れない。二つを組み合わせることで、前半層を独立した下書き器として使える状態を作る。",
        ),
    ],
    "papers/inference/06-moe-quantization-compression/2024-2406.08155-examining-post-training-quantization-for-mixture-of-experts-a-benchmark.md": [
        (
            "評価粒度は主に次の4段階である。",
            "比較を同じ平均ビット予算に揃えることが重要である。高精度に残す部分を増やせば単純に品質が上がるため、配置戦略の良し悪しを調べるには、全体の平均ビット数をほぼ同じにした上で『どこへ高ビットを使ったか』だけを変える必要がある。この設計により、品質差を容量差ではなくMoE構造に沿ったビット配分の効果として読みやすくしている。",
        ),
        (
            "つまり結果は特定の1つの量子化アルゴリズムだけに依存するというより、**MoE構造を考慮したbit配置そのものが有効か**を確認する設計になっている。",
            "重みのみ量子化と重み・活性値量子化の両方で同じ傾向を確認する理由は、低精度化の誤差源が異なっても『どのMoE構造が敏感か』という順位が利用できるかを確かめるためである。もし特定の量子化器だけでしか成立しないなら一般的な配置指針にはしにくい。複数方式で再確認することで、ブロック・エキスパート・線形層の感度差を量子化器固有の偶然から切り離そうとしている。",
        ),
        (
            "上位25%や50%のlinearだけ4 bitへ戻し、それ以外を2 bitにすることで、**同じ平均bitでも感度の高い場所へ精度を集中させる**。",
            "外れ値スコアは『その線形層が実際のタスク損失へ何点寄与するか』を直接測るものではなく、低ビット丸めで大きな誤差を生みやすい重み分布の代理指標である。したがって高スコア部分を保護する方式は、全候補をタスク評価して探索するより安価だが、入力分布や較正データが変われば感度順位も変わり得る。この点で、配置は一度決めれば普遍的に最適なものではない。",
        ),
        (
            "したがって後続のMxMoEのような「kernel実時間まで含めてbit allocationを決める研究」とは役割が異なり、こちらは **MoE量子化の感度マップを作ったbenchmark** と位置付けるのが適切である。",
            "このため本論文の高精度なビット配置を、そのまま『最速の実装』と解釈してはいけない。低ビット重みを実時間短縮へ変換するには、対象GPUでそのビット幅を直接処理できるカーネル、復号費用、メモリアクセス量まで含めた実行系が必要になる。本論文はその前段として、限られた精度予算をどの構造へ配るべきかを明らかにする役割を持つ。",
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
    print(f"content-quality batch3: {changed} paper(s) changed")


if __name__ == "__main__":
    main()
