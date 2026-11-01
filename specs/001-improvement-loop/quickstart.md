# Quickstart: 改善ループの受け入れ検証

実装後に、仕様の受け入れシナリオと成功基準を確かめる手順。詳細な書式は [contracts/](contracts/) を参照。

## 前提

- `gh` でリポジトリ `nananastuinfo-gif/default_aidd` に書き込み権限があること(`gh auth status`)
- 実装 PR のブランチがプッシュ済みであること
- Issue フォームと PR テンプレートは既定ブランチにある場合にのみ GitHub に反映されるため、
  GitHub 上での確認(手順 3 以降)は実装 PR のマージ後に行う

## 1. 静的検証(マージ前)

```bash
python3 scripts/check-issue-forms.py
```

期待結果: 3 フォームすべてで `OK` と表示され、終了コード 0。

## 2. ラベルの作成(マージ前、運用者の確認後)

公開リポジトリへの変更のため、実行前に運用者の確認を得る。

```bash
scripts/setup-labels.sh nananastuinfo-gif/default_aidd
scripts/setup-labels.sh nananastuinfo-gif/default_aidd   # 2 回目もエラーにならないこと
gh label list --search "improvement status: target: decision:"
```

期待結果: [contracts/labels.md](contracts/labels.md) の 9 件が表示される。

## 3. 登録(User Story 1 / SC-001)

1. GitHub の「New issue」を開き、3 つの改善提案フォームが表示されることを確認する。
2. 手順書だけを見て、実際の気づき 1 件を登録し、所要時間を測る。

期待結果: 3 分以内に登録でき、`improvement`・`status:triage`・対象区分ラベルが付いている。
`docs/improvement-loop.md` にある「未判断」の検索リンクで一覧に表示される。

## 4. 判断と反映(User Story 2 / SC-002, SC-003)

1. 手順書の「判断」に従い、手順 3 の提案に判断記録を投稿し、ラベルを付け替える。
2. 採用した場合は、手順書の「反映」に従って Issue → ブランチ → PR を作り、マージする。

期待結果: 提案が「completed」でクローズされ、提案から判断記録と反映 PR を辿れる。
手順書以外の資料を見ずに一巡できた(SC-002)。

## 5. 振り返り(User Story 3 / SC-005)

1. 手順 4 の反映 PR を作るとき、説明欄に PR テンプレートが入っていることを確認する。
2. 振り返りの 3 項目を記入する。

期待結果: 振り返り欄が初期値として表示される。改善提案があれば `#N` で参照している。

## 6. 派生プロジェクトからの還元(User Story 4 / SC-006)

派生プロジェクトはまだないため、机上で確認する。

1. 手順書の「派生プロジェクトから提案する」だけを読み、default_aidd のフォームへのリンクから
   出典を派生プロジェクト名にした提案を作成する画面まで進めることを確認する(登録はしない)。
2. 還元対象か派生プロジェクト固有かの判別基準が手順書にあることを確認する。

期待結果: 5 分以内に登録画面まで到達できる。実際の還元はフェーズ 5 で検証する。

## 7. 記録

検証結果(所要時間、つまずいた点)を実装 PR またはその後の PR の「振り返り」欄に記入する。
つまずいた点は改善提案として登録する。
