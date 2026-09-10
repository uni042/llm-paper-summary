# Always-on paper worker policy

通常の論文workerは、maintenance runや08:30 JSTのその他更新workerなど明示的な特殊runを除き、実行環境と耐久保存経路が許す限り処理を継続する。

## 1. 論文ストック0は停止条件ではない

`actionable ready`、Library seed由来の`spillover_candidates`、その他処理可能なresearch/audit jobを合わせた論文ストックが0件になった場合、通常論文workerはアイドル終了してはならない。ストック0を新規discovery開始条件として扱い、直ちにdiscoveryを実行する。

- GitHub write可能時は正規のdiscovery/queue transportを使う。
- GitHub write不能でもChatGPT Libraryへoffline job seedを耐久保存できる場合はoffline discoveryを行う。
- discoveryで新規候補が得られたら、可能なら同じrun内でresearchまで進む。
- researchまたはcheckpoint後に再びストック0になったら、再度discoveryへ戻る。

## 2. discovery新規0も停止条件ではない

1探索ラウンドで候補が全重複、弱候補のみ、または新規0件でも通常runを終了しない。`discovery-state.json`を参照し、直前と異なる探索軸・検索語・引用関係・関連実装・隣接テーマへ切り替えて次の探索ラウンドを行う。

既収録論文はarXiv ID、DOI、OpenReview ID、正規化タイトル等で詳細評価前に先行除外する。検索側で除外できない場合は広めに候補を取得して軽量重複除去し、未収録候補だけを詳細評価する。

## 3. 通常runの継続ループ

通常論文workerは原則として次を繰り返す。

1. actionable readyを処理する。
2. なければspillover candidateを処理する。
3. 論文ストックが0ならdiscoveryする。
4. discoveryで候補を得たらresearchし、必要ならauditする。
5. job完了、blocked化、checkpoint、discovery各ラウンド後にqueue/backlog/discovery stateを再取得する。
6. 次の独立作業があれば1へ戻る。
7. ストック0なら3へ戻る。

「readyが空」「候補が0」「1本完了」「1探索ラウンド完了」「固定bankが埋まった」「fallback backlogがある」は終了理由ではない。

## 4. 通常runを終了してよい条件

通常論文workerが自発的に終了してよいのは、原則として以下だけ。

- platform time/context/execution limitに到達した。
- GitHub read不能で正本状態を安全に判断できない。
- GitHub direct writeとChatGPT Libraryの両方で、必要な成果またはoffline seedを耐久保存できない。
- discovery-stateを踏まえて探索軸を変えても、利用可能な探索手段・一次資料アクセスの範囲で独立作業を合理的に生成できない。

最後の条件は単一ラウンドの新規0件では満たさない。探索軸変更・引用展開・隣接テーマ展開を試した後にのみ検討する。

## 5. 特殊run

maintenance runは通常処理へ戻らず、maintenance要求発行後に終了する。08:30 JSTのその他更新workerは論文workerを同じ枠で実行しない。将来repoで追加される明示的な特殊runも、その正本指示を優先する。
