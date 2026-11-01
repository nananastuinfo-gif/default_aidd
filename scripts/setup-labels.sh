#!/usr/bin/env bash
# 改善ループ用のラベルを作成・更新する。何度実行しても同じ結果になる。
# 既存のラベル(GitHub の既定ラベルを含む)は削除しない。
#
# 使い方: scripts/setup-labels.sh [OWNER/REPO]
#   OWNER/REPO を省略すると、カレントディレクトリのリポジトリを対象にする。
# 必要なもの: GitHub CLI (gh) とリポジトリへの書き込み権限
set -euo pipefail

repo_args=()
if [[ $# -ge 1 ]]; then
  repo_args=(--repo "$1")
fi

# 名前|色|説明(specs/001-improvement-loop/contracts/labels.md と一致させる)
labels=(
  "improvement|0E8A16|AIDD 標準への改善提案"
  "target:constitution|5319E7|対象: 憲章"
  "target:template|1D76DB|対象: テンプレート"
  "target:process|0052CC|対象: 手順"
  "status:triage|FBCA04|未判断"
  "status:needs-info|F9D0C4|追加情報待ち"
  "decision:constitution|B60205|判断: 憲章の改定"
  "decision:template-process|D93F0B|判断: テンプレート・手順の修正"
  "decision:wontfix|CCCCCC|判断: 見送り"
)

for entry in "${labels[@]}"; do
  IFS='|' read -r name color description <<<"$entry"
  gh label create "$name" --color "$color" --description "$description" --force "${repo_args[@]}"
done

echo "ラベルを ${#labels[@]} 件作成・更新しました。"
