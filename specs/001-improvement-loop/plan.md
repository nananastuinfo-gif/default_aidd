# Implementation Plan: 改善ループの整備

**Branch**: `001-improvement-loop` | **Date**: 2026-11-01 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-improvement-loop/spec.md`

## Summary

AIDD 標準(憲章・テンプレート・手順)への気づきを、登録 → 判断 → 反映 → 振り返りの流れで継続的に
取り込む「改善ループ」を、GitHub の標準機能(Issue フォーム、ラベル、PR テンプレート)と 1 つの
手順書で実現する。独自のコードや自動化(GitHub Actions 等)は導入せず、ラベルを作り直すための
小さなシェルスクリプト 1 本だけを追加する。自動化はフェーズ 2 で扱う。

主な設計判断(詳細は [research.md](research.md)):

- 改善提案は対象区分ごとに 3 つの Issue フォームで登録し、対象区分ラベルを自動で付ける。
- 状態はラベル(`status:` / `decision:`)と Issue のクローズ理由の組み合わせで表す。
- 判断結果と理由は、決まった書式のコメントで提案 Issue に記録する。
- 振り返りは PR テンプレートの必須欄として PR の説明に書く。
- 派生プロジェクトから標準への提案は、フォーム冒頭の案内と手順書から開発用リポジトリのフォームへ誘導する。

## Technical Context

**Language/Version**: Markdown(手順書・PR テンプレート)、YAML(GitHub Issue フォーム)、
Bash(ラベル作成スクリプト)

**Primary Dependencies**: GitHub.com(Issues、Issue フォーム、PR テンプレート、ラベル)、GitHub CLI
(`gh` 2.46 以降。ラベル作成と Claude Code からの起票に使用)

**Storage**: GitHub Issues(提案・判断記録)、PR の説明(振り返り)、リポジトリ内ファイル
(手順書・テンプレート)

**Testing**: YAML の構文検証(PyYAML)、Issue フォームの必須キー検証、quickstart.md の受け入れ
シナリオを実際に実行して確認(SC-002 の一巡を含む)

**Target Platform**: GitHub.com 上の public リポジトリ(開発用 `default_aidd`、将来の派生プロジェクト)

**Project Type**: プロセス/ドキュメントキット(GitHub 設定ファイル + 手順書)

**Performance Goals**: 改善提案の登録 3 分以内(SC-001)、派生プロジェクトからの登録 5 分以内(SC-006)

**Constraints**: GitHub Actions などの自動化は導入しない(フェーズ 2 の範囲)。運用者は 1 人。
派生プロジェクトにも配布されるファイルは `kit-dev/` の外に置く(FR-017)

**Scale/Scope**: 運用者 1 人、改善提案は四半期あたり数件〜数十件程度を想定

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

対象: 憲章 v1.1.0。本機能のタスク種別は「システム開発」(Spec Kit の流れで設定ファイルと手順書を作る)。

| 原則 | 判定 | 根拠 |
|------|------|------|
| I. 目的・成功基準の先行定義 | 合格 | 承認済みの spec に目的・スコープ・測定可能な成功基準があり、`[NEEDS CLARIFICATION]` は 0 件 |
| II. タスク種別に応じたプロセス選択 | 合格 | システム開発として Spec Kit の流れに従う。clarify は未解決事項 0 件のため省略し、理由を Issue #3 に記録済み |
| III. 根拠に基づく判断と検証可能性 | 合格 | GitHub の機能に関する判断は research.md に根拠を記録。検証手順は quickstart.md で再現可能にする |
| IV. 小さく段階的に進める | 合格 | 標準機能のみで構成し、独自コードはラベル作成スクリプトだけ。ユーザーストーリー単位で順に実装する |
| V. テストと品質ゲート | 合格(運用を明記) | 本機能の成果物はほぼ設定ファイルと文書のため、「テスト」は (1) YAML 構文と必須キーの自動検証、(2) quickstart.md の受け入れシナリオの実施、とする。実装前に検証手順を用意し、検証が通らない限りマージしない |
| VI. 人間による判断と承認 | 合格 | 仕様は承認済み。本計画も承認後に tasks へ進む。Claude Code による起票は事前確認を必須とする(FR-005)。ラベル作成は公開リポジトリへの変更のため、実行前に運用者の確認を得る |
| VII. トレーサビリティと知識の蓄積 | 合格 | 手順書・テンプレートは Git で管理。提案と判断は Issue に、反映は PR と `Refs #N` 付きのコミットに残り相互に辿れる。重要な意思決定(憲章改定)は従来どおり憲章の改定手続きで記録する |

ゲート判定: **合格**(違反なし。Complexity Tracking は不要)

### Phase 1 設計後の再確認

| 観点 | 結果 |
|------|------|
| 新たな複雑さ | なし。Issue フォーム 3 件の重複は、自動化を避けるための意図的な選択(research.md R1) |
| 原則 VI | ラベル作成スクリプトの実行と、テスト用 Issue の起票は運用者の確認後に行う手順を quickstart.md に明記 |
| 原則 VII | 判断記録コメントの書式(contracts/decision-record.md)により、採否と理由を後から検索できる |

再確認の判定: **合格**

## Project Structure

### Documentation (this feature)

```text
specs/001-improvement-loop/
├── plan.md              # このファイル
├── research.md          # Phase 0: 設計判断と根拠
├── data-model.md        # Phase 1: エンティティと状態遷移
├── quickstart.md        # Phase 1: 受け入れ検証の手順
├── contracts/           # Phase 1: Issue フォーム・ラベル・PR テンプレート・判断記録の仕様
│   ├── issue-forms.md
│   ├── labels.md
│   ├── pr-template.md
│   └── decision-record.md
├── checklists/
│   └── requirements.md
└── tasks.md             # Phase 2: /speckit-tasks で作成
```

### Source Code (repository root)

```text
.github/
├── ISSUE_TEMPLATE/
│   ├── config.yml                      # 空の Issue も許可。手順書へのリンク
│   ├── improvement-constitution.yml    # 改善提案(憲章)
│   ├── improvement-template.yml        # 改善提案(テンプレート)
│   └── improvement-process.yml         # 改善提案(手順)
└── pull_request_template.md            # 関連 Issue・変更内容・振り返り欄

docs/
└── improvement-loop.md                 # 改善ループの手順書(派生プロジェクトにも配布)

scripts/
├── setup-labels.sh                     # ラベルの作成・更新(何度実行しても同じ結果)
└── check-issue-forms.py                # Issue フォームの構文と必須キーの検証

CLAUDE.md                               # Claude Code 向け: 改善提案の起票ルール(フェーズ 2 で拡充)
```

**Structure Decision**: GitHub が自動で認識する `.github/` 配下にテンプレートを置き、手順書は
`docs/` に置く。どちらも `kit-dev/` の外にあるため、フェーズ 4 のリリースで配布用リポジトリに
含まれる(FR-017)。`CLAUDE.md` は本機能では改善提案の起票ルールだけを書き、全体の整備は
フェーズ 2 で行う。

## Complexity Tracking

憲章違反がないため記載なし。
