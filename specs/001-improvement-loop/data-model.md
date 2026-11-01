# Data Model: 改善ループの整備

データはすべて GitHub(Issue、PR、ラベル)とリポジトリ内のファイルに保存される。独自のデータストアは持たない。

## エンティティ

### 改善提案(Improvement Proposal)

GitHub Issue として表す。登録は [contracts/issue-forms.md](contracts/issue-forms.md) のフォームで行う。

| 属性 | 表現 | 必須 | 検証ルール |
|------|------|------|------------|
| 対象区分 | ラベル `target:constitution` / `target:template` / `target:process` | ○ | ちょうど 1 つ(FR-002)。フォームで自動付与 |
| 発生状況 | フォームの入力欄「気づいた作業」 | ○ | 空欄不可。関連する Issue/PR 番号があれば記載 |
| 問題点 | フォームの入力欄「問題点」 | ○ | 空欄不可 |
| 改善案 | フォームの入力欄「改善案」 | ○ | 空欄不可。案がなければ「未定(判断時に検討)」と書く |
| 出典 | フォームの入力欄「出典」 | ○ | `default_aidd` または派生プロジェクトのリポジトリ名 |
| 状態 | ラベル + open/closed + クローズ理由 | ○ | 下記の状態遷移に従う(FR-004) |
| 判断記録 | Issue コメント | 判断後は○ | [contracts/decision-record.md](contracts/decision-record.md) の書式(FR-006) |
| 反映 PR | PR 本文の `Closes #N` | 反映時は○ | 反映済みの提案は、必ず反映 PR からクローズされている(FR-010, FR-011) |

### 振り返り(Retrospective)

PR の説明欄の「振り返り」セクションとして表す([contracts/pr-template.md](contracts/pr-template.md))。

| 属性 | 必須 | 検証ルール |
|------|------|------------|
| うまくいった点 | ○ | 空欄不可(「特になし」可、FR-015) |
| 問題点 | ○ | 同上 |
| 改善提案 | ○ | 「特になし」または改善提案の Issue 番号(`#N`)。マージ前に登録済みであること(FR-014) |

### 判断記録(Decision Record)

改善提案 Issue へのコメントとして表す。1 件の提案に複数あってよい(保留 → 判断、見直しなど)。
最新のものが有効。書式は [contracts/decision-record.md](contracts/decision-record.md)。

### 反映(Amendment)

採用された提案を標準に適用する PR。

| 属性 | 検証ルール |
|------|------------|
| 対象の提案 | PR 本文に `Closes #N`(提案ごと)。コミットメッセージに `Refs #N` |
| 憲章のバージョン | 憲章の改定の場合、PR タイトルに新しいバージョン(例: `憲章 v1.2.0: ...`)を含める(FR-012) |
| 振り返り | 他の PR と同じく振り返り欄を記入する |

## 関係

```text
改善提案 1 ── * 判断記録
改善提案 * ── 0..1 反映(PR)        # 1 つの PR で複数の提案を反映してよい
振り返り(PR)1 ── * 改善提案        # 振り返りから新しい提案が生まれる
改善提案 0..1 ── 改善提案(重複先)
```

## 状態遷移

```text
                    ┌──────────────── 追加情報待ち ◄──┐
                    ▼                                  │
 [登録] ──► 未判断 ─────────────────────────────────────┘
              │
              ├──► 対応予定(憲章の改定) ──────────┐
              ├──► 対応予定(テンプレート・手順の修正) ─┼──► 反映済み(closed: completed)
              │                                    │
              │       反映 PR が中止された場合 ◄────┘──► 未判断に戻す(判断記録で理由を残す)
              ├──► 見送り(closed: not planned)
              └──► 重複(closed: duplicate、統合先を記録)
```

| 状態 | open/closed | ラベル | 遷移の操作 |
|------|-------------|--------|------------|
| 未判断 | open | `improvement` `status:triage` `target:*` | フォームで登録すると自動でこの状態になる |
| 追加情報待ち | open | 上記 + `status:needs-info` | 判断記録で依頼内容を残し、ラベルを追加 |
| 対応予定(憲章の改定) | open | `improvement` `decision:constitution` `target:*` | 判断記録を投稿し、`status:*` を外して `decision:*` を付ける |
| 対応予定(テンプレート・手順の修正) | open | `improvement` `decision:template-process` `target:*` | 同上 |
| 見送り | closed(not planned) | `improvement` `decision:wontfix` `target:*` | 判断記録を投稿し、ラベルを付けて「not planned」でクローズ |
| 重複 | closed(duplicate) | `improvement` `target:*` | 統合先を判断記録に書き、「duplicate」でクローズ |
| 反映済み | closed(completed) | `improvement` `decision:constitution` または `decision:template-process` | 反映 PR のマージで自動クローズ |

## 一覧の取得(検索条件)

| 目的 | 検索条件 |
|------|----------|
| 改善提案すべて | `is:issue label:improvement` |
| 未判断 | `is:issue is:open label:improvement label:status:triage` |
| 30 日を超えた未判断 | `is:issue is:open label:status:triage created:<YYYY-MM-DD`(30 日前の日付) |
| 対応予定 | `is:issue is:open label:improvement -label:status:triage` |
| 見送り | `is:issue is:closed label:decision:wontfix` |
| 対象区分で絞り込み | 上記に `label:target:constitution` などを追加 |
