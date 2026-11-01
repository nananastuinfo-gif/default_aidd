# Research: 改善ループの整備

Technical Context に `NEEDS CLARIFICATION` は残っていない。以下は設計上の選択肢を比較した記録である。
GitHub の機能に関する記述は、GitHub 公式ドキュメント(Issue フォームの構文、PR テンプレート、
Issue のクローズ理由)の仕様に基づく。

## R1: 改善提案の登録方法

- **Decision**: 対象区分(憲章/テンプレート/手順)ごとに 3 つの Issue フォームを用意し、
  フォームごとに `improvement`・`status:triage`・対象区分ラベルを自動で付ける。
- **Rationale**: Issue フォームが自動で付けられるラベルは固定値で、ドロップダウンの選択値に
  応じたラベル付けはできない。フォームを分ければ、独自コードなしで登録直後から対象区分で
  絞り込める(FR-003)。また入力欄が 1 つ減り、登録が速くなる(SC-001)。
- **Alternatives considered**:
  - 1 つのフォーム + ドロップダウン + 判断時に手動でラベル付け: 判断前は対象区分で絞り込めない。
  - 1 つのフォーム + GitHub Actions で選択値からラベル付け: 自動化はフェーズ 2 の範囲であり、
    コードとテストが増える(原則 IV)。
  - Markdown の Issue テンプレート: 必須項目を強制できない(FR-001)。
- **Trade-off**: 3 フォームの入力欄が重複する。入力欄の変更時は 3 ファイルを揃える必要があるため、
  `scripts/check-issue-forms.py` で 3 フォームの入力欄の一致を検証する。

## R2: 状態の表し方

- **Decision**: ラベルと Issue のクローズ理由を組み合わせる([data-model.md](data-model.md) の状態遷移)。
  - 未判断: open + `status:triage`
  - 追加情報待ち: open + `status:triage` + `status:needs-info`
  - 対応予定(憲章の改定): open + `decision:constitution`
  - 対応予定(テンプレート・手順の修正): open + `decision:template-process`
  - 見送り: closed(not planned)+ `decision:wontfix`
  - 重複: closed(duplicate)
  - 反映済み: closed(completed)+ `decision:constitution` または `decision:template-process`
- **Rationale**: GitHub の検索だけで各状態を一覧できる(例: `is:open label:status:triage`)。
  反映済みは PR の `Closes #N` によるクローズで自動的に「completed」になる(FR-011)。
- **Alternatives considered**: GitHub Projects のステータス列(設定の手間が増え、派生プロジェクトでの
  再現が難しい)、状態ごとのラベル(反映済みラベルの付け忘れが起きる)。

## R3: ラベルの管理方法

- **Decision**: `scripts/setup-labels.sh` に全ラベルの定義を書き、`gh label create --force` で
  作成・更新する。何度実行しても同じ結果になる。
- **Rationale**: ラベル定義が Git で管理され(原則 VII)、派生プロジェクトでも同じスクリプトで
  再現できる。依存は `gh` だけ。
- **Alternatives considered**: GitHub の画面で手動作成(再現できない)、ラベル同期用の Actions
  (自動化はフェーズ 2)。

## R4: 判断結果と理由の記録場所

- **Decision**: 判断時に、決まった書式のコメント([contracts/decision-record.md](contracts/decision-record.md))
  を提案 Issue に投稿し、ラベルを付け替える。
- **Rationale**: 判断の経緯が提案 Issue に時系列で残り、本文の書き換えによる情報の消失がない。
  書式の見出し(`## 判断記録`)で検索できる(SC-003)。
- **Alternatives considered**: Issue 本文の追記(履歴が追いにくい)、リポジトリ内の判断ログファイル
  (提案ごとに PR が必要になり、登録の手間が増える)。

## R5: 振り返りの記録場所

- **Decision**: PR テンプレートに「振り返り」欄(うまくいった点・問題点・改善提案)を設け、
  PR の説明に記入する。改善提案は Issue 番号で参照する。
- **Rationale**: PR の作成時に必ず目に入り、記入漏れが起きにくい(SC-005)。PR と同じ場所に残るので、
  どの作業の振り返りかが明確になる。
- **Alternatives considered**: `specs/` 配下の振り返りファイル(仕様駆動でない小さな PR に置き場がない)、
  PR のコメント(テンプレート化できない)。

## R6: 派生プロジェクトからの還元経路

- **Decision**: 各 Issue フォームの冒頭に「標準そのものへの提案は default_aidd に登録する」旨の案内と、
  default_aidd のフォームへの直接リンクを置く。手順書にも同じリンクと、還元対象かどうかの判別基準を書く。
- **Rationale**: 派生プロジェクトには同じフォームがコピーされる。派生プロジェクト内の提案(固有の改善)は
  そのまま派生プロジェクトに登録し、標準への提案はリンクから開発用リポジトリに登録できるため、
  フォームを 1 種類のまま両方の用途に使える(FR-016, FR-017)。
- **Alternatives considered**: リリース時に派生先用のフォームへ差し替える(フェーズ 4 の範囲で、
  今は配布物がない)。`config.yml` の連絡先リンク(開発用リポジトリでは自分自身を指して紛らわしい)。
- **Follow-up**: フェーズ 4 で、派生先での表示を確認し必要なら調整する(ロードマップに記録)。

## R7: 手順書の置き場所と構成

- **Decision**: `docs/improvement-loop.md` に、登録・判断・反映・振り返り・還元を 1 本にまとめる(FR-018)。
  よく使う検索条件は、そのまま開ける URL として載せる。
- **Rationale**: `kit-dev/` の外にあり配布対象になる。1 ファイルで完結し、手順書だけで実施できる(SC-002)。
- **Alternatives considered**: GitHub Wiki(Git 管理の対象外になり、派生プロジェクトにコピーされない)。

## R8: 見直しのタイミング

- **Decision**: 随時に加え、各機能(PR)の完了時に未判断の提案を確認する。さらに少なくとも月 1 回、
  登録から 30 日に近い未判断の提案を確認する。四半期ごとの憲章の見直しでも全件を確認する。
- **Rationale**: FR-007 の「各フェーズの完了時」「四半期ごと」だけでは、フェーズが長引いた場合に
  SC-004(30 日超の放置 0 件)を守れない。月 1 回の確認を加えることで SC-004 を満たす。
- **Alternatives considered**: 毎週の確認(個人運用には負担が大きい)。

## R9: Claude Code への起票ルールの伝え方

- **Decision**: ルートに最小限の `CLAUDE.md` を置き、「標準の改善点に気づいたら、内容を提示して
  運用者の承認を得てから `gh issue create` で登録する」ルールと手順書へのリンクだけを書く。
- **Rationale**: Claude Code はセッション開始時に `CLAUDE.md` を読むため、FR-005 を確実に守れる。
  `CLAUDE.md` 全体の整備はフェーズ 2 で行う。
- **Alternatives considered**: 手順書だけに記載(Claude Code が毎回読むとは限らない)。

## R10: 検証方法(原則 V の適用)

- **Decision**: `scripts/check-issue-forms.py` で Issue フォームの YAML 構文、必須キー、3 フォームの
  入力欄の一致を検証する。加えて quickstart.md の受け入れシナリオを実施する。
- **Rationale**: 成果物の大半は文書と設定であり、動作の正しさは GitHub 上で実際に使って確かめるのが
  最も確実である。機械的に検証できる部分(YAML)は自動で検証する。
- **Alternatives considered**: シェルスクリプトの静的解析(shellcheck は環境にないため、導入は
  フェーズ 2 の品質チェックで検討する)。
