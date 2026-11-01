# Contract: 改善提案の Issue フォーム

配置: `.github/ISSUE_TEMPLATE/`。GitHub Issue フォーム(YAML)の構文に従う。

## フォーム一覧

| ファイル | `name`(選択画面の表示) | 自動で付くラベル | タイトルの接頭辞 |
|----------|-------------------------|------------------|------------------|
| `improvement-constitution.yml` | 改善提案: 憲章 | `improvement`, `status:triage`, `target:constitution` | `[改善][憲章] ` |
| `improvement-template.yml` | 改善提案: テンプレート | `improvement`, `status:triage`, `target:template` | `[改善][テンプレート] ` |
| `improvement-process.yml` | 改善提案: 手順 | `improvement`, `status:triage`, `target:process` | `[改善][手順] ` |

各フォームの `description` には、その区分が対象とする範囲を 1 文で書く。

- 憲章: `.specify/memory/constitution.md` の原則・標準プロセス・品質ゲート・Governance
- テンプレート: Spec Kit のテンプレート、Issue/PR テンプレート、種別ごとの文書テンプレート
- 手順: 手順書(`docs/` 配下)、作業の進め方、ツールの使い方

## 入力欄(3 フォームで共通・同じ順序)

先頭に `type: markdown` の案内を置き、続けて次の入力欄を置く。`id` と `required` は 3 フォームで一致させる。

| 順 | `id` | `type` | ラベル | `required` | 補足 |
|----|------|--------|--------|------------|------|
| 0 | — | markdown | (案内) | — | 「標準(AIDD)そのものへの提案で、このリポジトリが default_aidd でない場合は、default_aidd の同じフォームから登録してください」と、default_aidd の該当フォームへのリンク。手順書へのリンク |
| 1 | `context` | textarea | 気づいた作業 | true | どの作業中に気づいたか。関連する Issue/PR 番号 |
| 2 | `problem` | textarea | 問題点 | true | 何が困ったか、何が不足しているか |
| 3 | `proposal` | textarea | 改善案 | true | 案がなければ「未定(判断時に検討)」 |
| 4 | `source` | input | 出典 | true | 既定値 `default_aidd`。派生プロジェクトからの場合はそのリポジトリ名 |

## 検証ルール(`scripts/check-issue-forms.py`)

- 各ファイルが YAML として読み込めること
- トップレベルに `name`, `description`, `title`, `labels`, `body` があること
- `labels` が上表と一致すること
- `body` の入力欄(markdown 以外)の `id`・`type`・`required` の並びが 3 フォームで一致すること
- 必須の入力欄に `validations.required: true` が設定されていること

## `config.yml`

- `blank_issues_enabled: true`(改善提案以外の Issue も作れるようにする)
- `contact_links` に、手順書(`docs/improvement-loop.md`)へのリンクを 1 件置く
