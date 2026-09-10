#!/usr/bin/env python3
"""Thirteenth content-only batch: finish remaining paper quality gaps."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PATCHES: dict[str, list[tuple[str, str]]] = {
    "papers/inference/07-kv-cache-optimization-compression/2026-2606.06302-tangram-non-uniform-kv-cache.md": [
        (
            "runtimeではこのmapを読むだけでper-layer re-planningを行わない。context lengthが変わっても各group長は同じ比率で伸びるためrelative workloadはほぼ不変で、batchingしてもstatic planを再利用できる。",
            "この一連の流れで重要なのは、保持率の予測を単なる圧縮設定で終わらせず、メモリ予約・ページ配置・GPU仕事量の三つへ同じ設計値として伝播させる点である。保持量だけを固定しても実行側が不均一長を知らなければ待ち時間が残り、実行側だけを最適化してもページを返却できなければ同時処理数は増えない。Tangramは一つの較正結果を複数層の制御へ共有することで、圧縮で生じた不均一性を実際の処理量向上へ変換する。"
        ),
    ],
    "papers/inference/05-speculative-decoding-moe/2026-2607.12696-less-experts-faster-decoding-cost-aware-speculative-decoding-for-mixture-of-expe.md": [
        (
            "branchを優先する。",
            "ここで使う費用は、その候補単独が使うexpert総数ではなく、現在選択済みの検証集合へ追加したときに新たに増えるexpert数である。同じexpertを既存候補がすでに使うなら追加の重み読出しは小さく、受理確率が少し低くても費用対効果が高くなる場合がある。逆に高確率候補でも新しいexpert群を多数開くなら、検証集合全体のHBM読出しを急増させるため優先度が下がる。"
        ),
        (
            "影響は、expertを再利用しにくいtreeを選んでしまいspeedupが縮むこと。",
            "したがって予測器の役割は正しいroutingを代行することではなく、候補追加の限界費用を概算することである。予測が外れてもtarget側の検証規則は変わらないので生成結果は維持される一方、実際には共有できないexpertを共有可能と見積もれば重み再利用が減り、逆に共有可能な候補を高費用と見積もれば受理長を不必要に犠牲にする。性能は受理率だけでなく、この費用順位の精度にも依存する。"
        ),
    ],
    "papers/inference/06-moe-quantization-compression/2026-2607.16184-pagedweight-efficient-moe-llm-serving-with-dynamic-quality-aware-weight-quantiza.md": [
        (
            "VRAMが足りなくなれば低影響blockからprecisionを下げ、request終了などで余裕が戻れば重要blockへbitを戻す。",
            "この制御の狙いは、最大同時request数を守るためにKV cacheを追い出すのではなく、時間とともに変動するweight側の占有量を調整弁にすることである。長いrequestが増えた瞬間だけ一部weightを低精度化し、queueが軽くなれば高精度へ戻せるため、最悪時のKV量に合わせて全expertを恒久的に低bit化する必要がない。したがって同じ平均memory budgetでも、静的量子化より品質を高く保てる余地が生まれる。"
        ),
        (
            "さらにmixed-precision CUDA kernelが必要なbitだけを直接読み、異なるprecisionのexpert blockをまとめて実行する。",
            "実装上はprecision変更そのものが新しい待ち時間にならないことも重要である。memory pressureが短時間で上下するたびに大きなweight tensorを作り直す設計では、量子化・復元のcostがserving利得を相殺する。page単位のbit追加・除去と安全な参照先切替を使うことで、変更粒度を必要量へ限定し、推論中のweight表現を段階的に更新できるようにしている。"
        ),
    ],
    "papers/inference/03-expert-prefetch/2026-2607.24787-specprefetch-parameter-efficient-expert-prefetching-for-sparse-moe-foundation-mo.md": [
        (
            "候補数を固定しないため、storageが遅いときは少数、速いときは多めに先読みできる。",
            "この上限は『予測上位を何個読むか』と『期限までに何個読み終えられるか』を分離する。予測精度だけを重視して多数候補を発行すると、低速storageでは未完了転送が列を作り、native router確定後の本当に必要なloadまで同じ帯域で待たされる。M_maxで発行数を実行可能な範囲へ抑えることで、先読みは需要loadを妨害しない余剰I/Oとして機能しやすくなる。"
        ),
        (
            "これによりpredictorの正しさとI/O schedulingの実用性を一つの指標で評価できる。",
            "例えば候補集合に正解expertが含まれていても、その転送が対象layer到達後まで続いていれば実行時にはcache missと同じである。ReadyRecallはこのケースを失敗として数えるため、単なる分類精度の高いpredictorと、serving上本当に待ち時間を隠せるprefetcherを区別できる。特にmobile storageでは帯域変動と転送粒度の影響が大きいため、この区別がend-to-end速度の説明に直結する。"
        ),
    ],
    "papers/inference/05-speculative-decoding-moe/2026-2608.02989-acceptmoe-commitment-weighted-self-sizing-verifier-expert-sets-for-efficient-moe.md": [
        (
            "この違いが最も重要である。",
            "EcoSpecやEVICTでは候補nodeを捨てても、残したnodeについてtargetが要求するexpert計算は完全に実行される。そのため誤った選択は主に速度へ響く。AcceptMoEは逆に、残したnodeの内部でも低寄与と判断したexpertを実行しないため、削減したHost→GPU転送量の一部は本来のmodel計算そのものを省いた結果である。したがって同じ『speculative decoding高速化』でも、速度比較では無損失方式と近似方式を分けて読む必要がある。",
        ),
        (
            "この違いが最も重要である。\n\nEcoSpecやEVICTでは候補nodeを捨てても、残したnodeについてtargetが要求するexpert計算は完全に実行される。そのため誤った選択は主に速度へ響く。AcceptMoEは逆に、残したnodeの内部でも低寄与と判断したexpertを実行しないため、削減したHost→GPU転送量の一部は本来のmodel計算そのものを省いた結果である。したがって同じ『speculative decoding高速化』でも、速度比較では無損失方式と近似方式を分けて読む必要がある。",
            "もう一つの差は、誤差がdraftの不採用で打ち消されるとは限らない点である。省いたexpertが最終的にcommitされるtokenのverificationへ寄与していれば、その近似はtarget logitsへ直接入る。Commitment Weightはrejectされやすいbranchのexpertを優先的に省くことでこの確率を下げるが、受理確率推定やrouter重要度が外れた場合の品質誤差をゼロにはできない。平均score低下が小さくても、長い生成や分布外promptでは累積誤差を別途見る必要がある。",
        ),
    ],
    "papers/inference/11-llm-serving-scheduling-disaggregation/2026-2608.06557-cascade-slo-aware-latency-budget-serving.md": [
        (
            "requestが待機・実行し、cache状態やsystem loadが変わるたびにbudgetを更新する。",
            "budgetはdeadlineそのものではなく、残り仕事を終えるための推定時間を差し引いた余白である。そのため同じSLO期限を持つ2 requestでも、短い残作業しかないものは余裕が大きく、長い生成や深いtierからのKV復元を抱えるものは余裕が小さくなる。実行が進んだりcache hit状況が変われば残りservice timeも変わるので、固定priorityではなく継続更新する必要がある。",
        ),
        (
            "長context requestを系統的にstarvationさせにくい。",
            "このpriorityは短いrequestを常に先にする最短仕事優先とは異なる。長contextでも早く到着してbudgetを消費し続ければ緊急度が上がり、後から来た短requestより先に選ばれる場合がある。つまり公平性はrequest長を同一視することでなく、『これ以上待たせられる余裕』を共通尺度へ変換することで実現する。",
        ),
        (
            "queueへ戻した後にbudgetを再計算する。",
            "preemption victimを選ぶ際にも同じ尺度を使うことで、schedulerとmemory managerが逆向きの判断をするのを防ぐ。例えば実行priorityが高いrequestをKV容量だけの都合で退避すると、直後にSLO違反へ近づき再度swap-inする無駄が起きる。余裕の大きいrequestから退避すれば、spillや再計算の時間を吸収できる可能性が高く、preemption自体がcritical pathへ入りにくい。",
        ),
    ],
    "papers/inference/05-speculative-decoding-moe/2026-2609.00355-glance-vlm-speculative-decoding.md": [
        (
            "trainingはtarget/vision towerをfreezeし、target自身のgreedy generations 16K rowsでheadだけ1 epoch学習する。",
            "この設計では視覚特徴をdraft側で再計算しない点が重要である。targetがprefillで作った融合済みstateには画像情報とテキスト履歴がすでに統合されているため、補助headはそのstateを条件として将来tokenをまとめて予測できる。追加のvision encoderを持つ方式よりparameterと実行経路を減らしつつ、画像に強く拘束されたtoken列では視覚条件を失わずにdraftできる。",
        ),
        (
            "targetのvision-language fusion済みhidden statesを再利用しraw image encodingなしで16-token blockをparallel draftする。",
            "特に文書読取やchart回答のように次tokenが画像中の文字列へ強く固定される場面では、融合stateが将来複数位置を同時に予測する強い手掛かりになる。一方、自由記述では直前に生成したtokenが次tokenへ与える依存が強く、各offsetを同時推定するblock headは自己回帰drafterより深い位置でずれやすい。これがtaskごとの速度逆転につながる。",
        ),
        (
            "offset-wise marginalsのproduct scoreからprefix-closed treeを作り、one-pass draftのwidthをaccepted lengthへ変換する。",
            "block headは各位置の候補を一度に出すため、そのまま1本のchainだけ選ぶと位置間の不確実性を十分活用できない。複数prefixへ幅を使えば、少し先の位置で第一候補が外れても別branchがtargetのgreedy pathを含む可能性を残せる。ただしtreeを広げすぎるとtarget verificationのtoken数が増えるため、固定node budget内で確率の高いprefixを優先する。",
        ),
        (
            "tree nodeを1 target forwardへpackし各nodeでexact autoregressive conditionalを再現、target greedy pathだけをcommitする。",
            "ancestor-only maskにより各nodeは自分の祖先tokenだけを参照し、別branchの候補を見ない。したがって多数nodeを同じtensorへ詰めても、各nodeのlogitはそのprefixを通常の自己回帰順で実行した場合と同じ条件で計算される。速度は複数branchを一度に検証する並列性から得て、受理判定の意味はtarget本来のgreedy decodingから変えない。",
        ),
        (
            "fp32ではargmax margin条件下でbitwise greedy equivalence、production bf16ではtie近傍をtarget tokenへdeferしてbyte identityを守る。",
            "低精度ではほぼ同点のlogit順位が丸め誤差で入れ替わると、理論上同じgreedy規則でもbyte単位の出力が分岐し得る。そこでmarginが小さい境界例を補助head側で強引に確定せずtarget判断へ戻す。これは平均精度を合わせるためではなく、production精度形式でも『弱いdraftは受理長だけを悪化させ、最終greedy出力は変えない』という性質を守るための安全策である。",
        ),
        (
            "accepted lengthがtarget next-token entropyに強く支配され、grounded/copied spansほど長くなることをtask横断で定量化する。",
            "entropyが低い区間ではtarget自身が次tokenへ強く確信しているため、各offsetの周辺分布も尖りやすく、block headが深い位置まで正しいprefixを含めやすい。逆に会話やcaptionのような高entropy区間では少しの誤差でbranchが急増し、固定tree budgetではtarget pathを覆い切れない。この分析はGLANCEが常にchain drafterより優れるのではなく、視覚groundingが予測可能性を下げるtaskで特に有利になる理由を説明する。",
        ),
        (
            "prefillでtarget vision encoderとdecoder fusion→decode round root→block head 1 pass→candidate tree構築→target tree verification 1 pass→longest target-greedy prefix+bonus token commit→次round。autoregressive drafterのdepth分passを除去しつつtargetは無改造。",
            "1 roundのcritical pathを見ると、従来chain drafterはdraft depthに比例して補助model forwardを直列実行するのに対し、GLANCEはblock headを1回だけ実行する。その代わりtarget側ではwide treeを一括検証するため、利得は『省けたdraft pass時間』が『増えたtree verification量』を上回る範囲で生じる。短出力や長contextでこの差が小さくなるという負の結果も、このround-level cost構造から理解できる。",
        ),
    ],
    "papers/inference/08-edge-on-device-llm-systems/2026-2609.01338-mzcache-on-device-llm-memory-management-under-multitasking.md": [
        (
            "細分化されたKVを毎回1つの連続bufferへ詰め直すとcopy costが増えるため、GPU attention kernelはshared buffer上の非連続KV chunkをpointer array経由で直接streamingする。online softmaxを使い、chunkを統合せず1 passでattentionを計算する。",
            "このkernel変更がないと、fine-grained evictionで得た弾力性を推論再開時の再packing costが打ち消してしまう。退避と復元の結果として物理配置がばらばらでも、そのままattentionへ渡せれば『必要量だけ戻す』方針を維持できる。つまりmemory managerが作る非連続layoutをcompute kernel側も受け入れることで、partial restorationとzero-copy unified memoryの利点をend-to-endで残している。",
        ),
    ],
    "papers/inference/02-adaptive-expert-computation-compression/2026-2609.04575-training-free-halving-activated-experts.md": [
        (
            "結果として、半数のexpertしか実行しなくても、適切なk2なら標準reduced-kより大幅に品質を回復できる一方、k2を大きくしすぎて再正規化を実質的に外すと品質が壊れるため、gainそのものは不可欠である。",
            "この分離によって、post-trainingでexpert数を減らしたときの劣化を二種類に切り分けられる。k1を小さくしたことで本当に計算しなくなったexpertの表現能力は戻せないが、survivorへ掛かる振幅だけが訓練時とずれた部分はk2で補正できる。したがって改善分は『削ったexpertを復元した』のではなく、削減とは無関係な正規化ずれを除去したものと解釈する必要がある。",
        ),
        (
            "expert identityは元routerのtop-k順位をそのまま使うため、別の選択器を学習する方式ではない。",
            "このためk1は計算予算を直接決める一方、どのexpertを残すかというranking品質には手を加えない。元routerが上位expertを適切に並べられていることが成立条件であり、ranking自体が不安定なmodelではk2だけ調整してもcapacity lossは回復しにくい。逆に細粒度routerで上位順位が安定しているなら、追加predictorなしで実行数だけを減らせる。",
        ),
        (
            "k2=Eは再正規化をほぼ外す端点として解釈できる。",
            "k2を増やすほど分母の確率質量が大きくなり、実行するk1 expertのweight合計は小さくなる。したがってk2は単なる候補数ではなくexpert branch全体のgain knobとして働く。訓練時より小さすぎればsurvivorを過大増幅し、大きすぎればexpert branchを弱めすぎるため、両端では品質が悪化し、中間に適切な基準集合が現れる。",
        ),
        (
            "Qwen系ではこれにより半数expert時のMMLU低下が標準reduced-kより大幅に縮小したが、k2=Eのようにgainを落としすぎると逆に大幅劣化する。",
            "この結果は、単純なreduced-k実験をexpert capacityの評価として読む際の注意点にもなる。標準実装でkを変えるとexpert identityと同時に正規化gainも変わるため、観測された精度低下をすべて『expertを減らしたから』と帰属すると過大評価になる。k1/k2分離は、compute削減と振幅較正を別々に操作してこの交絡を測るための診断手段でもある。",
        ),
        (
            "これは追加学習ではないが、deployment時の設定選択という実務上の境界条件になる。",
            "perplexityだけでk2を選ぶと、language modeling上は良くても下流推論taskで最適とは限らない。k2はbranch gainを全tokenへ系統的に変えるため、評価指標ごとに許容される振幅ずれが異なる可能性がある。少数候補をpaired downstream評価するという推奨は、training-freeであっても設定較正が完全に不要ではないことを明示している。",
        ),
        (
            "coarse routerや異なるarchitectureへ同じk2規則がそのまま一般化する保証はない。",
            "実行時に追加されるのは、すでに計算したrouter probabilityからtop-k2 massを集計する処理だけである。そのためFFNを半減して得る計算削減に対して制御overheadは小さいが、resident expert weight総量は変わらない。従って本手法はcapacity不足を解決するcompressionではなく、HBMにmodelが載る環境でtoken当たりのexpert computeとweight readを減らす実行時最適化として位置付けるのが正確である。",
        ),
    ],
    "papers/inference/02-adaptive-expert-computation-compression/2026-2609.05228-ace.md": [
        (
            "残存expertだけFFNを実行し、gateを再正規化してMoE出力を合成する。",
            "ACEが直接変更するのはnative routerが選んだtop-k候補の内部だけで、候補外expertを新たに探索するわけではない。したがって元routerの大まかな専門化構造は維持しつつ、第二位以下のslotに本当に計算を使う価値があるかを追加評価する。これはroutingを置き換える新routerではなく、既存routing後段に置く実行抑制器として理解すると分かりやすい。",
        ),
        (
            "SwiGLUの三投影の結合を保つbranch-symmetric spectral surrogateとRMSNorm scalingから、real sampleなしでglobal amplificationを推定しlayer内正規化する。",
            "GSPだけを見ると入力方向を区別せず、そのexpertが全体としてどの程度大きな変換を作り得るかをweight geometryから測る。したがって平均的には強いexpertを保護しやすい一方、特定のrouting方向だけで重要になるexpertは見落とし得る。この方向盲性を補うためにRCRが別視点として必要になる。",
        ),
        (
            "centered router weightからexpert固有routing方向を作り、そのprototypeに対するexpert応答増幅をoffline評価してGSPの方向盲性を補う。",
            "router weightをlayer平均から引くことで、全expertに共通する成分ではなく『このexpertが相対的に好む方向』をprototypeへ残す。その方向をexpertへ通したときの応答が大きければ、global proxyが低くても特定token群では重要な可能性がある。ただし一方向のprototypeで実入力分布すべてを代表できないため、RCR単独では高skip率で不安定になり得る。",
        ),
        (
            "GSP/RCR寄与分布のmaxを使うため、skip setは両低寄与集合のintersectionとなる。片方が重要とみなしたexpertは保持する。",
            "max融合は平均融合より保守的で、どちらか一方のproxyが高いslotを削除しない。これは2つのproxyが互いの失敗様式を補う設計である。GSPは方向特化を見落とし、RCRはprototypeが実入力を代表しない可能性があるため、両方が同時に低いときだけ省くことで偽陰性による重要expert削除を減らす。",
        ),
        (
            "estimatorはdata-freeだが、報告された10–60%のbudgetをthresholdへ変換する際はunlabeled full-model passでcandidate scoreを集めquantile mappingする。",
            "したがって『calibration-free』はexpert重要度tableを作るためにtask calibration dataを必要としないという意味で、所望skip率のthresholdまで完全にworkload非依存という意味ではない。実験では無label入力上のscore分布から分位点を求めるため、未知domainへ同じthresholdを持ち出すと実現skip率や品質がずれる可能性がある。この境界はdeployment時の再設定costとして扱う必要がある。",
        ),
        (
            "top-1を常時保持し、必要ならminimum-active数を課し、surviving gateを再正規化する。",
            "top-1保持はrouterが最も強く選んだ主経路を必ず残すための下限保証である。minimum-activeを追加すれば、proxyが多数slotを低寄与と判定したtokenでも計算量が極端に落ちるのを防げる。一方、残存gate再正規化は出力scaleを保つが、省いたexpertの方向成分そのものは復元できないため、これらは安全策であってlossless保証ではない。",
        ),
        (
            "offline tableはcheckpointごとに再利用できるが、所定skip率のthresholdは報告実験ではworkload score分布に対応付けている。",
            "online hot pathでは新しいneural predictorを動かさず、router gateと2種類のtable値をscalar演算するだけなので、expert FFNを省いた利得を制御overheadが食いにくい。反面、分散expert parallel環境ではslotを減らすことがall-to-all trafficやdevice間load balanceへどう波及するかは別問題であり、単一GPUでのFFN削減率がそのままcluster speedupになるとは限らない。",
        ),
    ],
    "papers/inference/03-expert-prefetch/2026-casmoe-a-cascaded-framework-for-efficient-moe-inference-on-resource-constrained-.md": [
        (
            "native router / Top-kは変更せず、予測はcache warming専用なのでlossless型である。",
            "二段構成の意味は、検索と学習予測を精度競争させるのではなくcostの違うfallbackとして使うことにある。既知workloadでは履歴検索だけで全layer候補を得られるため追加model実行を避けられ、未知promptだけ高costなEAPへ送る。database coverageが高まるほどonline predictor利用率を下げられる一方、workload shiftが大きい環境では検索hitを過信すると誤prefetchが増える。",
        ),
        (
            "CPU DRAMからGPUへcandidate expertを非同期transferし、native gate到達時に必要expertがすでにGPUへある割合を高める。",
            "全layerをprompt時点で予測する利点は、深いlayerほど長い先読み窓を確保できることである。ただし早く予測するほど実際のdecode hidden stateをまだ観測していないため、将来routingの不確実性も高い。CasMoEはprompt-level履歴やpredictorへ依存する代わりに、転送開始を大幅に前倒ししてPCIe latencyを多くの前段計算へ隠す設計といえる。",
        ),
        (
            "workloadが大きく変わる場合、古いrouting履歴の価値は低下する。",
            "そのためdatabaseは単なるcacheではなく、予測精度と検索costを同時に決める状態になる。小さすぎればEAP呼出しが増え、大きすぎれば近傍検索と更新の管理costが増える。また意味的に似ていてもroutingが異なるpromptを再利用すると不要expertを先読みするため、EAM表現はsemantic similarityだけでなくexpert activation similarityを反映する必要がある。",
        ),
    ],
    "papers/inference/03-expert-prefetch/2026-commitmoe-efficient-fallback-free-moe-inference-with-offloading-under-gpu-memory.md": [
        (
            "この経験則を、fallbackを捨てる根拠に使う。ただし一般的な品質保証ではない。",
            "逆にrouter certaintyが高いtokenで予測を外すと、native modelが強く必要としていたexpertを置換するため影響が大きくなり得る。Commit Routerの予測精度だけでなく、native routerがどれだけ一つの選択へ集中しているかを品質riskの手掛かりとして見る理由はここにある。fallback-free化はすべてのmissを同価値として扱うのではなく、missが許容されやすい領域が存在するという経験的性質へ依存している。",
        ),
        (
            "CommitMoEの大きなspeedupは、このfallback elimination込みで解釈する必要がある。",
            "lossless prefetchではprediction missのたびに正しいexpertを追加loadするため、最悪時には予測transferとdemand transferの両方を支払う。CommitMoEは後者を完全に削るので、PCIeが遅いlegacy環境ほど相対利得が大きくなる。一方その速度は『予測をより早くした』だけでなく『正しいnative expertを待つことをやめた』結果でもあり、quality-preserving system optimizationと同じ条件で比較してはいけない。",
        ),
        (
            "CommitMoEの大きなspeedupは、このfallback elimination込みで解釈する必要がある。\n\nlossless prefetchではprediction missのたびに正しいexpertを追加loadするため、最悪時には予測transferとdemand transferの両方を支払う。CommitMoEは後者を完全に削るので、PCIeが遅いlegacy環境ほど相対利得が大きくなる。一方その速度は『予測をより早くした』だけでなく『正しいnative expertを待つことをやめた』結果でもあり、quality-preserving system optimizationと同じ条件で比較してはいけない。",
            "さらにOWAはmissしたnative expertの関数を再現するものではなく、利用可能なexpertの混合係数を調整して出力scaleやrouter preferenceの一部を残す補正である。準備済みexpertがnative集合と大きく異なれば、weightを再配分しても失われた非線形変換は戻らない。平均benchmarkが維持される結果はこの近似が多くの入力で許容されたことを示すが、token-level equivalenceや長期誤差の不存在を示すものではない。",
        ),
    ],
    "papers/inference/03-expert-prefetch/2026-firm-moe-fine-grained-expert-decomposition-for-resource-adaptive-moe-inference.md": [
        (
            "expert丸ごとloadする方式よりGPU cache容量を細かく使え、不要なweight transferを減らせる。",
            "細粒度化の利点は、予測が部分的に当たった場合にも転送済みbyteを無駄にしにくいことにある。expert全体を一単位にすると一部projectionだけ先に必要でも全weightを運ぶが、分解後は実行順や残りmemoryに合わせて必要部分から配置できる。ただし単位を小さくしすぎるとmetadataとDMA発行回数が増えるため、分解粒度自体にもhardware依存の最適点がある。",
        ),
        (
            "cache missでもexpert全体を移す必要がなく、必要なweight部分だけをCPU DRAMから送る。",
            "この性質はVRAMが数expert分しか空いていない状況で特に効く。丸ごとcacheでは空き容量より少し大きいexpertを全く置けないが、projection単位なら一部だけresidentにして残りを後続計算と重ねて送れる。その結果、capacity制約を『何expert置けるか』という離散問題から『何byteのsub-expertを先に置くか』という連続に近い配分問題へ細かくできる。",
        ),
        (
            "GPU memoryが小さい環境ではweightを細かく保持する利点を重視し、PCIe帯域に余裕があればprefetchを増やす、といった適応を行う。",
            "同じmodelでも最適な予測距離はdeviceによって変わる。遠いlayerを早く予測すればtransfer時間は長く確保できるが、routing相関が弱まり誤prefetchも増える。近いlayerだけなら予測は当たりやすいが転送を隠す時間が不足する。HEOPはこのaccuracy-versus-lookaheadのtrade-offをVRAMとPCIeの実測costへ結びつけ、固定の『n layer ahead』設定を全deviceへ押し付けない。",
        ),
    ],
    "papers/inference/10-kv-cache-offload-recomputation/2026-vldb-retroinfer-vector-storage-engine-scalable-long-context-llm-inference.md": [
        (
            "token生成に伴う新しいKVも局所的に追加できるため、巨大なglobal indexを繰り返し作り直す必要を減らす。",
            "segment単位に分けるもう一つの利点は、検索indexの更新costと検索精度を局所化できることである。長context全体を一つのcluster空間として再最適化すると、新token追加のたびに広い範囲のcentroidや割当が変化し得る。既存segmentを固定したまま末尾側だけ更新できれば、decodeのcritical pathで行うindex maintenanceを小さく保ち、CPU検索をGPU attentionと重ねやすくなる。",
        ),
    ],
}


def insert_after(text: str, anchor: str, addition: str, path: str) -> str:
    if addition in text:
        return text
    if anchor not in text:
        raise RuntimeError(f"anchor not found in {path}: {anchor[:100]!r}")
    return text.replace(anchor, anchor + "\n\n" + addition, 1)


def update_audit_metadata(text: str) -> str:
    if 'last_audited: null' in text:
        text = text.replace('last_audited: null', 'last_audited: "2026-09-10"', 1)
    if 'audit_version: 0' in text:
        text = text.replace('audit_version: 0', 'audit_version: 1', 1)
    return text


def main() -> None:
    changed = 0
    for relpath, patches in PATCHES.items():
        path = ROOT / relpath
        text = path.read_text(encoding="utf-8")
        original = text
        for anchor, addition in patches:
            text = insert_after(text, anchor, addition, relpath)
        text = update_audit_metadata(text)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(f"updated {relpath}")
        else:
            print(f"unchanged {relpath}")
    print(f"changed files: {changed}")


if __name__ == "__main__":
    main()
