# 改善ループの手順書

AIDD 標準(憲章・テンプレート・手順)を使う中で気づいた問題や改善案を、標準に反映するための手順です。
この手順書だけで、登録から反映までを一人で行えるように書いています。

- 開発用リポジトリ: https://github.com/nananastuinfo-gif/default_aidd
- 憲章: [`.specify/memory/constitution.md`](../.specify/memory/constitution.md)

## 概要

改善提案は GitHub Issue として登録し、判断を経て、PR で標準に反映します。

```text
 気づき ─► 1. 登録 ─► 未判断 ─► 2. 判断 ─┬─► 対応予定 ─► 3. 反映(PR のマージ) ─► 反映済み
   ▲                                      ├─► 見送り(理由を残して閉じる)
   │                                      ├─► 重複(統合先を残して閉じる)
   │                                      └─► 保留(追加情報待ち)─► 再び判断
   │
   └──── 4. 振り返り(PR ごと) / 5. 定期的な見直し
```

| 状態 | Issue | ラベル |
|------|-------|--------|
| 未判断 | open | `improvement` `status:triage` `target:*` |
| 追加情報待ち | open | 上記 + `status:needs-info` |
| 対応予定(憲章の改定) | open | `improvement` `decision:constitution` `target:*` |
| 対応予定(テンプレート・手順の修正) | open | `improvement` `decision:template-process` `target:*` |
| 見送り | closed(not planned) | `improvement` `decision:wontfix` `target:*` |
| 重複 | closed(duplicate) | `improvement` `target:*` |
| 反映済み | closed(completed) | `improvement` `decision:constitution` または `decision:template-process` `target:*` |

## 1. 改善提案を登録する

作業の流れを止めないよう、気づいたらすぐに登録します。内容が粗くても構いません(判断時に補えます)。

### フォームを選ぶ

「New issue」から、対象区分に合うフォームを選びます。

| フォーム | 対象 |
|----------|------|
| 改善提案: 憲章 | 憲章の原則・タスク種別ごとの標準プロセス・品質ゲート・Governance |
| 改善提案: テンプレート | Spec Kit のテンプレート、Issue/PR テンプレート、種別ごとの文書テンプレート |
| 改善提案: 手順 | 手順書(`docs/` 配下)、作業の進め方、ツールの使い方 |

複数の区分にまたがる場合は、主な区分を 1 つ選び、他の区分は「問題点」に書きます。必要なら判断時に分割します。

### 入力欄を書く

| 入力欄 | 書き方 |
|--------|--------|
| タイトル | `[改善][区分] ` の後に、問題を 1 行で書く |
| 気づいた作業 | どの作業中に気づいたか。関連する Issue/PR 番号(例: `#3 の /speckit-plan 実行中`) |
| 問題点 | 何が困ったか、何が不足しているか |
| 改善案 | 思いつく案。なければ「未定(判断時に検討)」 |
| 出典 | `default_aidd`、または派生プロジェクトのリポジトリ名 |

登録すると `improvement`・`status:triage`・対象区分のラベルが自動で付き、「未判断」になります。

### Claude Code が登録する場合

Claude Code は、標準の改善点に気づいても**勝手に登録しません**。次の手順で登録します(憲章 VI)。

1. 対象区分・気づいた作業・問題点・改善案・出典を運用者に提示する。
2. 運用者の承認を得る。
3. 次のコマンドで登録する。

```bash
gh issue create \
  --title "[改善][手順] <問題を 1 行で>" \
  --label improvement,status:triage,target:process \
  --body "$(cat <<'BODY'
### 気づいた作業
...
### 問題点
...
### 改善案
...
### 出典
default_aidd
BODY
)"
```

対象区分に応じて `--label` の `target:` を `constitution` / `template` / `process` に変えます。

## 2. 判断する

未判断の提案を見て、次のいずれかに振り分けます。

| 判断 | 選ぶとき |
|------|----------|
| 憲章の改定 | 原則・標準プロセス・品質ゲート・Governance を変える必要がある |
| テンプレート・手順の修正 | 憲章は変えず、テンプレートや手順書を直せば解決する |
| 見送り | 今は対応しない(効果が小さい、前提が合わない、他の方法で解決済みなど) |
| 重複 | 同じ内容の提案がすでにある |
| 保留(追加情報待ち) | 判断に必要な情報が足りない |

### 判断記録を投稿する

提案 Issue に、次の書式でコメントします。判断のたびに投稿し、最新のものが有効です。

```markdown
## 判断記録
- 判断: 憲章の改定 / テンプレート・手順の修正 / 見送り / 重複 / 保留(追加情報待ち)
- 理由:
- 反映先: <!-- 対応予定: 反映する Issue/PR か「未着手」。重複: 統合先 #N。見送り: なし -->
- 判断日: YYYY-MM-DD
```

- `判断` は 5 つのうち 1 つだけを書きます。
- `理由` は空欄にしません。見送りの場合は、**どんな前提が変われば再検討するか**も書きます。
- 過去に見送った提案と同種の場合は、理由に過去の提案番号と、前提が変わったかどうかを書きます。

### ラベルと Issue を操作する

判断記録の投稿と同時に、次の操作をします。

| 判断 | 操作 |
|------|------|
| 憲章の改定 | `status:*` を外し、`decision:constitution` を付ける(open のまま) |
| テンプレート・手順の修正 | `status:*` を外し、`decision:template-process` を付ける(open のまま) |
| 見送り | `status:*` を外し、`decision:wontfix` を付けて「Close as not planned」で閉じる |
| 重複 | `status:*` を外し、統合先の Issue にも相互参照を書いて「Close as duplicate」で閉じる |
| 保留 | `status:needs-info` を追加する(`status:triage` は残す)。依頼内容は判断記録の理由に書く |

```bash
# 例: テンプレート・手順の修正と判断した場合
gh issue edit <番号> --remove-label status:triage --add-label decision:template-process
# 例: 見送りと判断した場合
gh issue edit <番号> --remove-label status:triage,status:needs-info --add-label decision:wontfix
gh issue close <番号> --reason "not planned"
```

### 判断記録と憲章 VII の関係

- Issue の判断記録は、提案ごとの採否の「判断の経過」です。憲章 VII の「決定記録」には当たりません。
- 標準を変更する判断(憲章の改定、テンプレート・手順の修正)は、憲章 VII の決定記録として
  **反映コミットのメッセージ**に残します(「3. 反映する」を参照)。

## 3. 反映する

対応予定の提案は、通常の作業と同じく Issue → ブランチ → PR で反映します。

1. 提案 Issue をそのまま作業の Issue として使います(大きな変更なら別の Issue を作り、提案から参照します)。
2. `main` から作業ブランチを作ります。
3. 変更をコミットします。**反映コミットのメッセージ**には、次の書式で背景・判断理由・提案番号を必ず書きます。

   ```text
   <type>: <変更の要約>

   背景: <提案の問題点の要約>
   判断理由: <判断記録の「理由」の要約>

   Refs #N
   ```

4. PR を作ります。本文の「関連 Issue」に、反映する提案ごとに `Closes #N` を書きます。
5. 振り返りを記入し(「4. 振り返る」)、レビューしてマージします。マージすると提案は自動で
   「completed」として閉じ、反映済みになります。

### 憲章の改定の場合

1. `/speckit-constitution` を実行し、改定内容を伝えます。
2. 生成された Sync Impact Report(ファイル先頭のコメント)で、バージョンの上げ方と影響範囲を確認し、
   承認します。
3. Sync Impact Report を削除してからコミットします。
4. PR タイトルに新しいバージョンを書きます(例: `憲章 v1.2.0: ...`)。

### 反映をやめた場合

反映 PR を中止したときは、PR を閉じたうえで、提案に新しい判断記録を投稿します。

```bash
gh issue edit <番号> --remove-label decision:constitution,decision:template-process --add-label status:triage
```

これで未判断に戻り、次の見直しで改めて判断します。

## 4. 振り返る

すべての PR で、説明欄の「振り返り」に次の 3 項目を書きます(PR テンプレートに欄があります)。

| 項目 | 書くこと |
|------|----------|
| うまくいった点 | 次も続けたい進め方 |
| 問題点 | 困ったこと、手戻り、時間がかかったこと |
| 改善提案 | 標準を変えたほうがよい点。`特になし` または `#N` |

- 小さな変更で特に書くことがなければ、各項目に「特になし」と書けば完了です。
- 改善提案が出たら、**マージ前に**「1. 改善提案を登録する」の手順で登録し、番号を書きます。
- 機能(フェーズ)を完了する PR では、あわせて「5. 定期的に見直す」も行います。

## 5. 定期的に見直す

未判断の提案が溜まりすぎないよう、次のタイミングで見直します。

| タイミング | すること |
|------------|----------|
| 随時 | 気が向いたときに未判断の提案を判断する |
| 各機能(フェーズ)の完了時 | 未判断の提案をすべて確認する |
| 少なくとも月 1 回 | 登録から 30 日に近い未判断の提案を優先して判断する(30 日を超えて放置しない) |
| 四半期ごと | 憲章の定期見直しとあわせて、未判断・対応予定の提案をすべて確認する |

見直しには「付録: 検索条件」のリンクを使います。30 日を超えた提案は、`created:<YYYY-MM-DD` に
30 日前の日付を入れて検索します。

## 6. 派生プロジェクトから提案する

配布用リポジトリ(aidd-template)から作ったプロジェクトで気づいたことは、内容に応じて登録先を変えます。

### 登録先の判別

| 内容 | 登録先 | 例 |
|------|--------|----|
| 標準そのもの(憲章・テンプレート・手順)の不備や改善 | **default_aidd** | 原則の書き方が曖昧、テンプレートに必要な欄がない、手順書が分かりにくい |
| 派生プロジェクト固有の運用 | 派生プロジェクト自身 | そのプロジェクトだけのレビュー観点、固有のツールの使い方 |

迷った場合は「他の派生プロジェクトでも同じことが起きるか」で判断します。起きるなら標準への提案です。

### default_aidd に登録する

1. 対象区分に合うフォームを開きます。
   - 憲章: https://github.com/nananastuinfo-gif/default_aidd/issues/new?template=improvement-constitution.yml
   - テンプレート: https://github.com/nananastuinfo-gif/default_aidd/issues/new?template=improvement-template.yml
   - 手順: https://github.com/nananastuinfo-gif/default_aidd/issues/new?template=improvement-process.yml
   (派生プロジェクトのフォーム冒頭にも同じリンクがあります)
2. 「出典」に派生プロジェクトのリポジトリ名を書きます。
3. 「気づいた作業」は、default_aidd の運用者が文脈を知らなくても分かるよう具体的に書きます
   (派生プロジェクトの Issue/PR への URL があれば貼ります)。

派生プロジェクト固有の改善は、派生プロジェクト内の同じフォームで登録して構いません。

## 付録: 検索条件

| 目的 | 検索条件 |
|------|----------|
| 改善提案すべて | [`is:issue label:improvement`](https://github.com/nananastuinfo-gif/default_aidd/issues?q=is:issue%20label:improvement) |
| 未判断 | [`is:issue is:open label:improvement label:status:triage`](https://github.com/nananastuinfo-gif/default_aidd/issues?q=is:issue%20is:open%20label:improvement%20label:status:triage) |
| 30 日を超えた未判断 | `is:issue is:open label:status:triage created:<YYYY-MM-DD`(30 日前の日付を入れる) |
| 対応予定 | [`is:issue is:open label:improvement -label:status:triage`](https://github.com/nananastuinfo-gif/default_aidd/issues?q=is:issue%20is:open%20label:improvement%20-label:status:triage) |
| 見送り | [`is:issue is:closed label:decision:wontfix`](https://github.com/nananastuinfo-gif/default_aidd/issues?q=is:issue%20is:closed%20label:decision:wontfix) |
| 反映済み | [`is:issue is:closed reason:completed label:improvement`](https://github.com/nananastuinfo-gif/default_aidd/issues?q=is:issue%20is:closed%20reason:completed%20label:improvement) |
| 判断記録のある提案 | [`is:issue label:improvement "判断記録" in:comments`](https://github.com/nananastuinfo-gif/default_aidd/issues?q=is:issue%20label:improvement%20%22%E5%88%A4%E6%96%AD%E8%A8%98%E9%8C%B2%22%20in:comments) |

対象区分で絞り込むときは、検索条件に `label:target:constitution`・`label:target:template`・
`label:target:process` を加えます。

## 付録: 初期設定(ラベルの作成)

改善ループのラベルは `scripts/setup-labels.sh` で作成します。何度実行しても同じ結果になり、
既存のラベルは削除しません。新しいリポジトリ(派生プロジェクトを含む)を作ったら一度実行します。

```bash
gh auth status                              # 書き込み権限があることを確認
scripts/setup-labels.sh OWNER/REPO          # 省略するとカレントのリポジトリ
gh label list --search "improvement"        # 作成結果の確認
```

作成されるラベルは 9 件です: `improvement`、`target:constitution`、`target:template`、
`target:process`、`status:triage`、`status:needs-info`、`decision:constitution`、
`decision:template-process`、`decision:wontfix`。
