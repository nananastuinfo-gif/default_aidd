# Contract: ラベル

定義と作成は `scripts/setup-labels.sh` で行う。スクリプトは `gh label create <name> --color --description --force`
を使い、何度実行しても同じ結果になる。対象リポジトリは引数(`OWNER/REPO`)で指定でき、省略時は
カレントディレクトリのリポジトリとする。既存のラベル(GitHub の既定ラベルを含む)は削除しない。

| ラベル | 色 | 説明 | 用途 |
|--------|----|------|------|
| `improvement` | `0E8A16` | AIDD 標準への改善提案 | 改善提案の識別(FR-003) |
| `target:constitution` | `5319E7` | 対象: 憲章 | 対象区分 |
| `target:template` | `1D76DB` | 対象: テンプレート | 対象区分 |
| `target:process` | `0052CC` | 対象: 手順 | 対象区分 |
| `status:triage` | `FBCA04` | 未判断 | 状態 |
| `status:needs-info` | `F9D0C4` | 追加情報待ち | 状態(`status:triage` と併用) |
| `decision:constitution` | `B60205` | 判断: 憲章の改定 | 判断結果 |
| `decision:template-process` | `D93F0B` | 判断: テンプレート・手順の修正 | 判断結果 |
| `decision:wontfix` | `CCCCCC` | 判断: 見送り | 判断結果 |

## 検証

- スクリプト実行後、`gh label list` に上表の 9 件がすべて表示され、色と説明が一致すること
- 2 回続けて実行してもエラーにならず、結果が変わらないこと
