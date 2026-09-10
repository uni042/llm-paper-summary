#!/usr/bin/env python3
"""Tenth content-only batch: finish remaining 2025 content gaps."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PATCHES: dict[str, list[tuple[str, str]]] = {
    "papers/inference/05-speculative-decoding-moe/2025-2510.10302-sp-moe-speculative-decoding-and-prefetching-for-accelerating-moe-based-model-inf.md": [
        (
            "別の専用predictorを学習するのではなく、**draft modelの中間表現＋target gateを組み合わせてroutingを先読みする**点が特徴である。",
            "この方法が成立するには、draftが作る中間表現とtarget側のrouting判断に十分な相関が必要になる。token自体のdraft accuracyだけが高くても、target gateへ入れたときのexpert rankingが外れればprefetchには使えない。逆にtokenが最終的にrejectされても、routing候補が似ていれば先読みしたexpertをverificationで再利用できる場合がある。SP-MoEではtoken受理率とexpert予測精度を別の性能要因として見る必要がある。",
        ),
        (
            "つまり「予測できるだけ先まで読む」のではなく、**今の帯域とcache容量で得になる範囲だけ読む**。",
            "cutoffが必要なのは、prefetch depthを深くするほどfuture expert候補が指数的ではないにせよ広がり、まだ使うか分からないweightがGPU cacheを占有するからである。深いlayerの候補を早く載せることで後のI/Oは減らせる一方、近いlayerで確実に必要なexpertを追い出せば逆にmissが増える。profilingとlatency modelは、先読みで隠せる転送時間とcache pollutionによる追加転送を比較し、利益が正になる深さで止める。",
        ),
        (
            "これにより、今すぐ必要な正しいexpertの転送と、まだ必要か確定していない先読み転送が同じPCIe帯域を奪い合うのを抑える。",
            "3段階に分けることでprefetchの確信度とdeadlineを対応付けられる。Phase Iはdraft中でも高確率で必要と見込めるexpertを早く流し、Phase IIはGPU計算中の余剰帯域だけを使って候補を追加する。Phase IIIはtarget verificationが迫った時点で、まだ到着していない高確率expertを優先する。単一FIFOへ全prefetchを投入するより、緊急度の高いtransferが低価値な先読みの後ろへ詰まるのを防ぎやすい。",
        ),
        (
            "GPUにあるexpertを計算している間に転送中expertを到着させ、I/O待ちを隠す。",
            "この並べ替えはtokenの意味的な処理順を変えるのではなく、同じMoE layer内で独立に計算できるexpert branchの実行順だけを変える。各expert出力は最後に元router weightでcombineされるため、先に計算したresident expertと後から到着したexpertを最終的に同じ位置へ合成できる。したがってreordered inferenceは結果を近似せず、I/O arrival orderへGPU計算順を合わせるsystem最適化である。",
        ),
    ],
    "papers/inference/06-moe-quantization-compression/2025-2510.10962-mc-mixture-compressor-for-mixture-of-experts-large-models.md": [
        (
            "旧MC-MoEと同じく、ここで減るのは**保存しておくweight量**である。",
            "PMQはexpertを丸ごと同じbitへ落とすのではなく、重要度と量子化誤差からexpertごとのprecision価値を見積もる。頻繁に強く選ばれるexpertは低bit化の誤差が多くのtokenへ波及しやすいため高bitを残す価値が高い。一方、利用頻度が低く低bitでも出力再構成誤差が小さいexpertは容量削減への貢献が大きい。線形計画は総bit予算を超えない範囲で、この品質損失と保存byteのtrade-offを全expert横断で解く。",
        ),
        (
            "論文の `Top-any` という名前は、実行expert数を固定のkへ縛らないことを指す。",
            "OTPはPMQとは異なりweight自体を消さない。あるtokenでexpertをpruneしても別tokenでは同じexpertを再び実行できるため、入力依存の計算削減になる。画像tokenとtext token、簡単なtokenと難しいtokenで必要expert数が違うVLMでは、このtoken-adaptive性が特に重要になる。固定Top-1/Top-2へ一律削減すると、必要計算量の多いtokenまで同じbudgetへ押し込めるからである。",
        ),
        (
            "学習では16-bit teacherとのdistillation lossと、expertを使いすぎないようにする制約を同時に最適化するため、**単なるrouting score下位切り捨てより品質を保ちやすい**。",
            "distillationは、prune後のMoE出力や最終予測が元modelから離れないようにする役割を持つ。計算量制約だけを強くするとrouterは多くのexpertを切って速度を上げられるが品質が崩れ、teacher一致だけを重くするとほぼ全expertを残してしまう。二つを同時に最適化して、どのtokenで何個までexpertを省いてよいかを学習する。したがってOTPのpruning率は無料の冗長性除去ではなく、明示的に学習された品質・計算量のoperating pointである。",
        ),
        (
            "したがってMC#は、旧MC-MoEのrule-based pruningを、**学習可能なtoken-adaptive pruningへ置き換えた拡張**と見ると分かりやすい。",
            "PMQとOTPを分ける理由は、解いている資源制約が異なるためである。PMQはmodelをstorage/GPU memoryへ収めるための静的容量削減で、request開始前にbit配置が決まる。OTPはmodelが載った後のtokenごとのFLOPs削減で、入力に応じて実行集合が変わる。両者を同時に強くすると量子化誤差とexpert pruning誤差が重なるため、平均bitとactivation削減率を別々のつまみとして評価する必要がある。",
        ),
    ],
    "papers/inference/02-adaptive-expert-computation-compression/2025-2511.10054-buddymoe-exploiting-expert-redundancy-to-accelerate-memory-constrained-mixture-o.md": [
        (
            "各native expertに対しbuddy候補の順位表を作り、cache miss時の代替検索へ使う。",
            "共活性を使う利点は、expert weight同士の距離を直接計算せず、実際のrouterが『同じ入力に対して同時に必要と判断した』というmodel内部の利用関係を利用できる点である。ただし共活性は機能同値を保証しない。同時選択される2 expertが補完的な役割を持つ可能性もあるため、buddy relationは安全な置換証明ではなく、Random replacementより良い候補を作る経験的heuristicとして扱う。",
        ),
        (
            "つまりcache hit時は元modelと同一で、**近似が起きるのはGPUにないexpertだけ**である。",
            "この条件付き近似により、cache容量が大きい環境ではnative pathを通るtokenが増え品質差が小さくなる。一方、memory budgetが厳しくcache missが増えるほどbuddy substitutionの発生率が上がり、PCIe節約量と品質誤差の両方が大きくなる。したがって同じτ・ρでもcache率によって実際の近似強度が変わるため、quality設定はmemory budgetとセットで決める必要がある。",
        ),
        (
            "この重複回避が、単純に最も似たexpertへ置換する方式との差になる。",
            "Top-k MoEは複数expert出力を組み合わせることで1 tokenの表現を作るため、異なるnative expertを同じbuddyへ潰すと本来のensemble幅まで減ってしまう。duplicate avoidanceは、置換を行ってもできるだけ異なるresident expertを使い、元のTop-kが持つ多様性を残す安全策である。これにより『転送を避ける』ことと『実行expert数そのものを減らす』ことを区別できる。",
        ),
        (
            "BuddyMoEはその中間で、**似た役割を持つ可能性が高い常駐expertだけを使い、Randomより品質を守る**ことを狙う。",
            "OriginalとRandomを両端に置くと、BuddyMoEの設計意図が明確になる。Originalは正しいexpert到着まで待つためqualityは変えないがPCIe stallを受ける。Randomはstallをほぼ避けられるがrouterの意味を無視するため品質が急落する。BuddyMoEはcache miss時だけ意味的に近い可能性のあるresident expertへ置換し、一定のquality costを払ってI/O待ちを減らす。したがってprefetch missをlosslessに隠す方式ではなく、明示的なquality–latency trade-offである。",
        ),
    ],
    "papers/inference/05-speculative-decoding-moe/2025-2511.14102-moe-speq-speculative-quantized-decoding-with-proactive-expert-prefetching-and-of.md": [
        (
            "別の小型routing predictorを学習するのではなく、**量子化した同一系統modelそのものをpredictorにする**。",
            "同一構造を使うことでlayer対応が明確になり、draft layer `l` のrouting結果をtarget layer `l` のprefetch hintとして直接利用できる。別architectureの小型draftではtoken予測が当たってもexpert構造が一致せず、この対応付けが難しい。代わりにMoE-SpeQはtargetと似たmodelをINT4で持つため、一般的なtiny draftよりdraft計算とmemoryが重くなりやすく、後述のparameter共有と低bit kernelが重要になる。",
        ),
        (
            "routerまで低bit化するとexpert ID自体が変わり、先読み対象まで外れやすくなる。そのため**どのexpertを選ぶかに直接効く部分を高精度に残す**ことが成立条件になる。",
            "これは量子化誤差の影響箇所によって重要度が違うためである。routed expert MLPのweight誤差はdraft側のhidden stateを多少変えるが、最終tokenはtargetが検証する。一方gateのscore順位が変わると、draftが報告するexpert IDそのものが外れてprefetch対象が間違い、I/O隠蔽能力が直接落ちる。そこで容量の大きいexpert MLPを主にINT4化し、routing決定や共有計算に効く部分をFP16で保護する。",
        ),
        (
            "長いdraftはexpertを早く先読みできる一方、draft計算そのものと不要な候補も増える。Governorは**先読みで得られる時間短縮がdraft追加計算を上回る範囲**を選ぶ。",
            "最適なspeculation長はhardware依存でもある。PCIeが遅い環境ではexpert transferを隠すため長いlookaheadに価値があるが、GPU computeが遅くdraft自体が重い環境では先読み時間を得るための追加計算costが大きい。Amortization Roofline Modelはdraft compute、転送帯域、target verificationの比率から、1 token追加speculationしたときに隠せるI/Oと増える計算のどちらが大きいかを見積もり、実行環境ごとにGovernorの設定を変える。",
        ),
        (
            "これにより別draft modelを丸ごと持つ場合よりVRAM overheadを小さくする。",
            "共有できる部分を二重保持しないことは、そもそもmemory-constrained MoEでspeculative decodingを成立させるために重要である。target expertをCPUへoffloadしてHBMを節約しているのに、独立draftのattention weightやKVを追加常駐させてHBMを消費すれば、expert cache容量がさらに減ってmissが増える。MoE-SpeQは同系統modelという制約を利用して共有領域を増やし、draft導入がoffload pressureを悪化させるのを抑える。",
        ),
    ],
    "papers/inference/06-moe-quantization-compression/2025-2511.15015-dynamic-expert-quantization-for-scalable-mixture-of-experts-inference.md": [
        (
            "論文ではこの値を `hotness` と呼ぶ。",
            "hotnessを長期統計に寄せるのは、precision切替自体がhost→GPU transferを伴うためである。requestごとの瞬間routingへ追従して毎回promotionすると、品質改善よりcopy trafficの方が大きくなり得る。指数的に古い履歴を減衰させれば、持続的な人気expertは高bitへ上げつつ一時的なburstには過敏に反応しない。workload shiftが続けば新expertのhotnessが徐々に上がり、配置も追従する。",
        ),
        (
            "これにより**precision変更の転送をbackgroundで進めてもforwardを止めにくい**。",
            "forward側から見ると、precision switchはatomicなversion切替として見える。新しいhigh-bit bufferへcopy中でも旧low-bit bufferは有効なままなので、現在batchは旧versionで計算できる。copy完了後にpointer/metadataだけを新versionへ切り替え、不要になった旧bufferを後で解放する。この二重化期間を明示管理することで、async copyとcomputeを重ねてもpartially copied weightを読むraceを避ける。",
        ),
        (
            "論文ではこの往復防止を `hysteresis` と呼ぶ。",
            "例えばpromotion thresholdよりdemotion thresholdを低く置けば、一度hotと判定したexpertは明確にcoldになるまでhigh-bitを維持する。これによりthreshold付近のnoiseでprecisionが毎iteration反転するthrashingを防ぐ。代わりに一時的にhigh-bit expertを余分に保持するため、hysteresis幅を広げすぎるとHBM budgetの柔軟性が下がる。precision stabilityとmemory responsivenessのtrade-offになる。",
        ),
        (
            "モデル本体やrouterの再学習は不要。一方でhost側には複数precision copyを準備するため、**GPU HBMを節約する代わりにCPU RAM使用量とscheduler複雑性が増える**。",
            "hostに複数precisionを置くのは、promotion時にGPU上で元weightから再量子化・逆量子化する待ち時間を避けるためでもある。必要versionをあらかじめhost側へ用意しておけばprecision controllerはcopy先を選ぶだけでよく、switchをcomputeと非同期化しやすい。ただし80B級MoEではhost copyの総容量も大きくなるため、GPU memory削減だけを見てsystem全体のmemory costが減ったと解釈してはいけない。",
        ),
    ],
    "papers/inference/03-expert-prefetch/2025-2512.03927-od-moe-on-demand-expert-loading-for-cacheless-edge-distributed-moe-inference.md": [
        (
            "論文では`Shadow-Emulative Predictor (SEP)`と呼ぶ。単純classifierでexpert IDだけを当てるのではなく、**元modelのtoken処理を軽量modelで少し先まで追跡し、そのrouter出力を将来予測として使う**方式である。",
            "emulative predictorの利点は、layerをまたいだhidden-state変化まで軽量model自身が追跡するため、next-layerだけの局所classifierより遠いlayerを予測しやすい点にある。代わりにshadow modelはtoken generation状態を持つため、main modelとの差が累積するとroutingもずれる。OD-MoEでは高いlookahead精度とshadow計算costを交換して、数layer分のexpert load時間を前倒しする。",
        ),
        (
            "この同期を省くと長いgenerationでrouting recallが急落する。",
            "同期は毎step全状態を丸ごとcopyする必要はないが、mainが実際に確定したtokenと、将来routingへ効くKV/hidden-stateの整合を定期的に回復する必要がある。shadowが誤tokenを1つ生成すると次stepの入力が変わり、その差がさらに後段layerのexpert選択へ伝播するためである。したがってstate alignmentはprediction accuracyを長いsequenceで維持するためのfeedback correctionとして働く。",
        ),
        (
            "layerが進むたびに「今計算するgroup」と「先のexpertをloadするgroup」を順番に交代し、network / storageからのloadをexpert computeと同時に進める。",
            "このround-robin配置では1 groupが現在layerを計算する間、他groupのGPU memoryは将来layer expertのstagingへ使える。計算終了後には現在expertを解放し、そのgroupが今度は先読み担当へ回る。固定cacheを持たない代わりに、複数nodeを時間的なpipeline bufferとして使い、expert residencyをlayer進行と一緒に循環させる設計である。",
        ),
        (
            "hot expert用にGPU memoryを固定予約しないため、layerごとのexpert需要が大きく変わっても、その時必要なexpertへmemoryを使える。",
            "cacheless化の効果は特に各workerのVRAMが1GB未満のように小さい場合に大きい。通常cacheでは将来使うか分からないpopular expertへ常時領域を予約するため、現在必要なexpertを同時に置けない可能性がある。OD-MoEは予測精度と分散node数を使って常設capacityを時間方向のprefetchへ置き換える。一方、network障害やprediction missが増えると待避cacheがないため即座にload stallへ現れる。",
        ),
    ],
    "papers/inference/04-conditional-computation/2025-diffskip-differential-layer-skipping-in-large-language-models.md": [
        (
            "論文名の`Differential`はこの**layer変換前後の差分**を利用することに由来する。",
            "論文が利用するもう一つの観察は、同じlayer内でself-attentionによる変化量と後続FFNによる変化量に強い相関があることである。FFNを実際に計算してから『変化が小さかったのでskipすべきだった』と判断しても計算削減にならないため、先に得られるattention側の差分をrouter signalとして使い、これから来るFFNの必要性を予測する。つまり安い前段情報から高価な後段変換の価値を推定する構造になっている。",
        ),
        (
            "このためDiffSkipは「FFNをゼロコストで飛ばす」というより、**大きいFFNを小さい近似変換へ置き換える**方式と見る方が正確である。",
            "adapterが必要なのは、residual connectionがあってもFFNを完全identityにすると、後続layerが学習時に見てきたhidden-state分布からずれるためである。元LLMはfreezeしているので後続weight側をskip入力へ適応させられない。小型adapterだけをfine-tuneして、FFNを省いたtokenを元modelの表現空間へ近づけることで、dynamic routeを追加しても既存checkpointの大部分を変更せずに済む。",
        ),
        (
            "つまり実行時に自由に任意kへ変える方式ではなく、**学習したbudget付近で使う**。",
            "budget penaltyはrouterが全tokenをexecuteして品質だけを最大化する退化解と、逆に全tokenをskipして計算だけを最小化する退化解の間へ誘導する。各token・layerの局所判断は自由でもbatch全体では平均skip数をk付近へ保つため、品質比較を同程度のcompute budgetで行える。kを変えるとrouterが学ぶ境界自体も変わるので、単一checkpointで連続的に任意のspeed-quality点を選べるわけではない。",
        ),
    ],
    "papers/inference/06-moe-quantization-compression/2025-eac-moe-expert-selection-aware-compressor-for-mixture-of-experts-large-language-.md": [
        (
            "つまり量子化誤差は、単にexpert出力の近似誤差として終わらず、**routing経路そのものを変えて後段へ増幅する**。",
            "この増幅がMoE量子化をdense FFN量子化より難しくする。dense modelならあるlayerの小さい出力誤差は次layerへ連続値として伝わるが、MoE routerにはTop-kという離散境界がある。2 expertのscoreが近いtokenでは小さなhidden-state誤差でも順位が反転し、その後は全く別のexpert weightを通るため誤差が不連続に大きくなる。EAC-MoEはこの選択境界を守ることを量子化目的へ直接入れる。",
        ),
        (
            "狙いは「全出力を平均的に近づける」よりも、**元モデルと同じexpert rankingを維持すること**にある。",
            "TopK-MSEで上位候補を重視するのは、router下位expertのscoreを多少誤っても実際のforwardには選ばれず影響しない一方、Top-k境界付近の誤差はexpert-shiftを起こすためである。限られた量子化補正budgetをrouting decisionへ効く部分へ集中し、同じbit幅でもnative execution pathを維持しやすくする。したがってQESCは単なる低bit weight再構成ではなく、MoEの離散expert-selectionを保護するcalibrationである。",
        ),
        (
            "ただしfrequencyを集めるには複数tokenが必要なので、1 tokenずつ進むdecodeへそのまま適用する方式ではない。",
            "PESFはprefill中に同じsequenceの多数tokenを観測できることを利用する。長いprompt内で一度も、あるいはほとんど選ばれなかったexpertはその入力domainでは重要度が低い可能性が高く、後続prefill処理から外すことで実GEMM数を減らせる。ただしdecodeでは将来tokenのroutingが変わる可能性があり、prefill頻度だけを根拠にexpertを恒久削除すると必要expertを失う危険がある。このため適用phaseを分けている。",
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
        paper_changed = False
        for anchor, addition in patches:
            paper_changed |= apply_patch(path, anchor, addition)
        if paper_changed:
            mark_audited(path)
            changed += 1
    print(f"content-quality batch10: {changed} paper(s) changed")


if __name__ == "__main__":
    main()
