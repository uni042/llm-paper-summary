#!/usr/bin/env python3
"""Fourth content-only quality batch: oldest remaining 2024 papers first."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PATCHES: dict[str, list[tuple[str, str]]] = {
    "papers/inference/07-kv-cache-optimization-compression/2024-2402.05099-hydragen-high-throughput-llm-inference-shared-prefixes.md": [
        (
            "論文ではこの系列間のまとめ処理を `inter-sequence batching` と呼ぶ。",
            "この変換が効く理由は、デコード時の共有接頭部Attentionが演算量よりHBMからのKV読出しに支配されやすいからである。系列を1本ずつ処理すると同じ共有KVを系列数だけ読み直すが、複数クエリを一度に当てれば、読み込んだ共有KVをGPU上で複数クエリへ使い回せる。したがって削減対象はKV容量そのものではなく、同じバイト列をHBMから繰り返し運ぶ回数である。共有系列数が増えるほど1回のKV読出しを多くのクエリで償却できるため、長い共有接頭部と大きなバッチほど利得が大きい。",
        ),
        (
            "最後に共有 接頭辞側とsuffix側の注意機構結果を、softmaxの正規化を崩さないように結合する。",
            "単純に共有側と固有側のAttention出力を足すだけでは正しい結果にならない。それぞれは別々のキー集合に対してsoftmax正規化されているため、各部分で得たlog-sum-expを使って『全キーを一度にsoftmaxした場合の重み』へ戻してから合成する必要がある。この再正規化があるため、Hydragenは近似的な接頭部圧縮ではなく通常Attentionと同じ出力を保てる。",
        ),
    ],
    "papers/inference/11-llm-serving-scheduling-disaggregation/2024-2403.19708-cachedattention-multi-turn-conversation-serving.md": [
        (
            "論文の層ごとの事前読み込みはこの先読みを指す。記憶装置からの転送をGPU計算の裏へ隠すことで、低速階層を使ったときの追加遅延を減らす。",
            "層単位にするのは、全KVを一括で戻すより必要な先行量を小さくできるためである。層 `l` を計算している間に層 `l+1` のKVだけを転送できれば、GPUには次に使う分だけを用意すればよく、セッション全体のKVがGPUへ揃うまで開始を待つ必要がない。逆に記憶装置帯域が遅すぎて1層の計算時間内に次層KVを供給できない場合は転送待ちが表面化するため、保存階層を選ぶ際には再計算時間だけでなく層ごとの供給速度も見る必要がある。",
        ),
    ],
    "papers/inference/11-llm-serving-scheduling-disaggregation/2024-2404.16283-andes-qoe-text-streaming-serving.md": [
        (
            "すでにユーザーが消費できる量より十分先までトークンを生成済みの要求は一時的に優先度を下げ、そのGPU時間を**最初のトークン待ちや、まもなく表示トークンが尽きる要求**へ回す。",
            "ここで重要なのは、停止対象が『遅い要求』ではなく『今は急いで進めなくても利用者側バッファが尽きない要求』である点である。例えば利用者が毎秒10トークン読む一方、すでに50トークン未読なら数秒分の余裕がある。その要求を一時停止しても直ちに体感品質は下がらないため、その間に初回トークン待ちの別要求を処理できる。GPU処理量そのものを減らすのではなく、同じ処理量を体感効果の大きい時刻へ再配置する考え方である。",
        ),
    ],
    "papers/inference/11-llm-serving-scheduling-disaggregation/2024-2407.00023-preble-efficient-distributed-prompt-scheduling.md": [
        (
            "これは厳密なclient-level fairness保証が主目的ではなく、**cache reuseを増やしてもcache miss requestを永久に後回しにしないための安全策**である。",
            "この安全策が必要なのは、接頭部ヒットを優先する方策が自己強化しやすいためである。あるGPUに人気接頭部が残っていると、その接頭部を持つ要求がさらに同GPUへ集まり、キャッシュ命中は高まる一方で、共有接頭部を持たない要求は相対的に処理機会を失う。待機要求を複数の優先度群へ分けて各群へ処理枠を残すことで、局所性の利得を取りつつ飢餓を防ぐ。したがってPrebleのローカル実行順は、単なる命中率最大化ではなくクラスタ配置の偏りを補正する役割も持つ。",
        ),
    ],
    "papers/inference/11-llm-serving-scheduling-disaggregation/2024-2405.19888-parrot-efficient-serving-llm-applications-semantic-variable.md": [
        (
            "各エンジンは通常のモデル推論提供バックエンドとして動作するが、ServeCoreから\n\n- どの要求を先に処理するか\n- どの文脈を再利用できるか\n- どの要求を同じエンジンへ寄せるか\n\nという情報を受け取る。",
            "この情報があると、個々の要求だけを見た最短処理順と、アプリケーション全体の最短完了順が異なる場合を扱える。例えば後続の多数要求を解放する前段要求は、その要求単体の生成長が多少長くても早く完了させる価値が高い。一方、互いに独立な枝は同時に実行できる。Parrotは依存グラフからこの違いを把握し、重要な依存経路を詰まらせないことと、独立枝をまとめて高効率に実行することを両立させる。",
        ),
        (
            "スケジューラはその共有KVをすでに持つエンジンへ要求を寄せ、再プリフィルを減らす。",
            "ただし共有KVを持つエンジンへ常に寄せれば、そのエンジンだけ待ち行列が伸びる可能性がある。そのため共有接頭部の再利用価値は、アプリケーション依存関係や実行単位の混雑と一緒に判断する必要がある。Parrotの利点はキャッシュ機構単体ではなく、データフロー情報を同じ制御器が持つことで『再計算を省く配置』と『アプリケーションを早く進める配置』を同じ判断に含められる点にある。",
        ),
    ],
    "papers/inference/11-llm-serving-scheduling-disaggregation/2024-2407.00047-qlm-queue-management-slo-oriented-llm-serving.md": [
        (
            "予測には不確実性も含め、単一の決め打ち時間ではなく「この順ならSLOを守れる可能性がどの程度あるか」をスケジューラへ渡す。",
            "この不確実性を入れる理由は、LLMの出力長が要求開始前には分からず、同じモデル・同じ入力長でも完了時刻がばらつくためである。平均実行時間だけで締切ぎりぎりに詰めると、少し長い生成が出た時点で後続要求まで連鎖的にSLOを破る。そこで待ち時間の分布や安全余裕を考慮し、残りSLO余裕が小さいグループほど予測誤差に耐えられる位置へ移す。これは最短ジョブ優先ではなく、違反リスクを待ち行列全体で抑える考え方である。",
        ),
        (
            "QLMの考え方は、これらを個別経験則で別々に判断するのではなく、**「この順でこの実行単位へ要求を流したい」という最終待ち行列計画を先に作り、必要な処理をそこから導く**ことである。",
            "この順序付けにより、モデル局所性とSLOを同じ計画へ入れられる。目的モデルがすでにGPUへ常駐している実行単位は交換費用を避けられるが、そこへ急ぎ要求が集中して待ち時間が伸びるなら別GPUへ載せ替える方がSLO達成数は増える場合がある。逆に締切に余裕がある要求はモデル交換を避けられる位置まで待たせられる。つまりモデル交換を最小化すること自体ではなく、交換費用を払ってでも救うべき要求かを残りSLO余裕から判断する。",
        ),
    ],
    "papers/inference/11-llm-serving-scheduling-disaggregation/2024-2406.17565-memserve-context-caching-disaggregated-serving.md": [
        (
            "論文の全体プロンプト木構造は、この**クラスタ全体の接頭部→KV所在地索引**を指す。",
            "この索引が必要なのは、P/D分離後は『同じ要求のKVがどこにあるか』だけでなく『別要求が再利用できるKVがどこに残っているか』まで探索対象になるからである。要求到着時に各実行単位へ問い合わせていては制御遅延が増えるため、全体スケジューラが接頭部と所在地をまとめて把握し、最長一致するキャッシュ候補を先に特定する。これにより、再プリフィルで節約できる計算量と遠隔転送量を要求振り分け前に比較できる。",
        ),
        (
            "論文のブロック集約 / huge-ページ的な設計は、**論理的には小ブロック管理を保ちつつ、物理的転送だけ大きくする**工夫を指す。",
            "小ブロック管理はPagedAttentionとの互換性や細かな解放には有利だが、ネットワーク転送では1回ごとのAPI発行・同期・メタデータ処理が固定費になる。そこで送信時だけ連続した大きな単位へ束ねることで、固定費を多数ブロックへ償却し、リンク帯域を使いやすくする。受信後は再び実行エンジンのブロック配置へ対応付けるため、メモリ管理粒度を粗くすることなく転送粒度だけを最適化できる。",
        ),
    ],
    "papers/inference/04-conditional-computation/2024-2407.14057-lazyllm-dynamic-token-pruning-for-efficient-long-context-llm-inference.md": [
        (
            "主な効果は長文prefillのTTFT削減で、A100実測では多文書QAでLlama 2 7Bが2.34倍、XGen 7Bが2.65倍のTTFT改善を示す。一方、decode支配のtaskでは全生成時間への効果は小さい。",
            "したがってLazyLLMが最も有利なのは、長い入力を一度に読む時間が応答遅延の大部分を占める処理である。出力が非常に長い場合は、最初の入力処理を短縮してもその後のデコード時間が支配的になり、エンドツーエンドの改善率は小さくなる。逆に検索結果や長文書を大量に与えて短い答えを返す用途では、削減した入力トークン計算がそのまま最初の応答待ち短縮へつながりやすい。",
        ),
    ],
    "papers/inference/06-moe-quantization-compression/2024-2407.14417-mixture-of-experts-with-mixture-of-precisions-for-tuning-quality-of-service.md": [
        (
            "これはMixtralが比較的load-balancedに学習され、expert間の重要度差が小さいという前提に立つ。そのため、routingが偏るDeepSeek系などへそのまま一般化できるとは限らない。",
            "この前提が崩れると、ランダムに4ビット化する方式は頻繁に使われるエキスパートまで低精度化し、同じ平均ビット数でも品質損失が大きくなり得る。またCPU配置も利用頻度を見ないため、高頻度エキスパートがCPU側へ残るとPCIe転送が反復してスループットが落ちる。したがって本手法は『精度と配置を共同で調整する枠組み』が重要であり、後続研究ではそこへエキスパート重要度・利用頻度を加える余地がある。",
        ),
        (
            "そのためこの論文は、**量子化・resident率・PCIe転送を一緒に見ないと実速度は評価できない**ことを示す早期のserving研究として読むのが適切である。",
            "特に4ビット化でGPU常駐数を増やした効果と、4ビット行列積自体の実装効率は分けて考える必要がある。低ビット演算カーネルが遅くても、CPUから大きな重みを毎回運ぶ時間を省ければ全体は速くなる一方、すべての対象エキスパートがすでにGPUへ載る条件では転送削減の利得が消え、低ビットカーネルの性能が前面に出る。したがって最適精度はGPUメモリ容量だけでなく、PCIe帯域と利用する量子化カーネルにも依存する。",
        ),
    ],
    "papers/inference/04-conditional-computation/2024-layerskip-enabling-early-exit-inference-and-self-speculative-decoding.md": [
        (
            "H100実機でtoken/sまで測定しており、taskにより約1.3〜2.16倍のspeedupを示す。単純なlayer skipではなく、**浅い予測を後段で検証して誤りを修正するため品質を守りやすい**のが特徴である。",
            "この検証は最終モデルの出力分布に従って下書きトークンを受理するため、単純な早期終了のように浅い層の誤りをそのまま確定させない。下書きが外れた位置では後段層の結果へ戻り、それ以降を改めて生成する。そのため速度は受理率に依存するが、受理されたトークンについては完全モデルで検証済みの経路を使える。LayerSkipの品質保持は『浅い層が常に正しい』ことではなく、『浅い層を安い候補生成器として使い、間違いを後段で検出する』構造から生じる。",
        ),
    ],
    "papers/inference/04-conditional-computation/2024-d-llm-a-token-adaptive-computing-resource-allocation-strategy-for-large-language.md": [
        (
            "そのため `FLOPs 0.55` を「1.82倍高速」と読み替えることはできない。大規模batchのwall-clock speedupは主評価ではない。",
            "実際のランタイムで速度へ変換するには、同じ層を実行するトークンをまとめ直して十分大きなGPU処理単位を作り、スキップしたトークンはそのカーネルへ投入しない仕組みが必要になる。分岐ごとに小さな処理を個別発行すると、FLOPsを減らしてもカーネル起動やトークン再配置の固定費が増える。したがってD-LLMは『どの計算を省けるか』を示すモデル側手法であり、その省略可能性を壁時計時間へ変える実行系最適化は別の重要課題である。",
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
    print(f"content-quality batch4: {changed} paper(s) changed")


if __name__ == "__main__":
    main()
