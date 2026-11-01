---

description: "Task list for 改善ループの整備"
---

# Tasks: 改善ループの整備

**Input**: Design documents from `/specs/001-improvement-loop/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: 憲章 V と plan.md の Constitution Check に従い、検証スクリプト(`scripts/check-issue-forms.py`)を
Issue フォームより先に作り、失敗することを確認してからフォームを作る。GitHub 上の動作は quickstart.md の
受け入れシナリオで確認する。

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

plan.md の構成に従う。GitHub 設定は `.github/`、手順書は `docs/`、スクリプトは `scripts/`、
Claude Code 向けルールはリポジトリ直下の `CLAUDE.md`。いずれも `kit-dev/` の外に置く(FR-017)。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: ディレクトリの用意

- [X] T001 リポジトリ直下に `.github/ISSUE_TEMPLATE/`、`docs/`、`scripts/` ディレクトリを作成する

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: すべてのユーザーストーリーが前提とするラベルと手順書の骨組み

**⚠️ CRITICAL**: ラベルが存在しないと、Issue フォームで登録してもラベルが付かない。

- [X] T002 [P] `scripts/setup-labels.sh` を作成する。contracts/labels.md の 9 ラベル(`improvement` `0E8A16`「AIDD 標準への改善提案」、`target:constitution` `5319E7`「対象: 憲章」、`target:template` `1D76DB`「対象: テンプレート」、`target:process` `0052CC`「対象: 手順」、`status:triage` `FBCA04`「未判断」、`status:needs-info` `F9D0C4`「追加情報待ち」、`decision:constitution` `B60205`「判断: 憲章の改定」、`decision:template-process` `D93F0B`「判断: テンプレート・手順の修正」、`decision:wontfix` `CCCCCC`「判断: 見送り」)を `gh label create <name> --color --description --force` で作成・更新する。第 1 引数 `OWNER/REPO` を `--repo` に渡し、省略時はカレントのリポジトリを対象にする。`set -euo pipefail` を使い、既存ラベルは削除しない。実行権限を付ける
- [X] T003 [P] `docs/improvement-loop.md` の骨組みを作成する。見出しは「概要(改善ループの全体像と状態遷移の図)」「1. 改善提案を登録する」「2. 判断する」「3. 反映する」「4. 振り返る」「5. 定期的に見直す」「6. 派生プロジェクトから提案する」「付録: 検索条件」「付録: 初期設定(ラベルの作成)」とし、概要には data-model.md の状態遷移を手順書向けに簡潔に書き、各節の本文は後続タスクで埋める
- [X] T004 運用者の確認を得てから `scripts/setup-labels.sh nananastuinfo-gif/default_aidd` を 2 回実行し、`gh label list` で 9 ラベルの色と説明が contracts/labels.md と一致することを確認する(quickstart.md 手順 2)。`docs/improvement-loop.md` の「付録: 初期設定」に実行方法を書く

**Checkpoint**: ラベルが作成され、手順書の骨組みがある

---

## Phase 3: User Story 1 - 改善提案を手間なく登録する (Priority: P1) 🎯 MVP

**Goal**: 対象区分ごとの Issue フォームから、必須項目が揃った改善提案を「未判断」で登録できる

**Independent Test**: 手順書だけを見て気づき 1 件を登録し、対象区分・発生状況・問題点・改善案・出典が揃い、「未判断」の検索結果に表示される(quickstart.md 手順 3)

### Tests for User Story 1 ⚠️

> **NOTE: 検証スクリプトを先に作り、フォームがない状態で失敗することを確認する**

- [X] T005 [US1] `scripts/check-issue-forms.py` を作成する。contracts/issue-forms.md の検証ルールを実装する: 3 ファイル(`improvement-constitution.yml`、`improvement-template.yml`、`improvement-process.yml`)が存在し YAML として読めること、トップレベルに `name` `description` `title` `labels` `body` があること、`labels` が契約の表と一致すること、markdown 以外の入力欄の `id`・`type`・`required` の並びが `context`(textarea)→`problem`(textarea)→`proposal`(textarea)→`source`(input)で 3 フォーム一致し、すべて `validations.required: true` であること、`source` に `value`(既定値)がないこと、`config.yml` が存在し `blank_issues_enabled: true` かつ `contact_links` が 1 件であること。依存は PyYAML のみ。ファイルごとに `OK` / `NG: 理由` を表示し、1 件でも NG なら終了コード 1。実行して、フォームがないため失敗することを確認する

### Implementation for User Story 1

- [X] T006 [P] [US1] `.github/ISSUE_TEMPLATE/improvement-constitution.yml` を作成する。`name: 改善提案: 憲章`、`title: "[改善][憲章] "`、`labels: [improvement, status:triage, target:constitution]`、`description` は「`.specify/memory/constitution.md` の原則・標準プロセス・品質ゲート・Governance への改善提案」。`body` は contracts/issue-forms.md の順で、先頭の markdown に「標準(AIDD)そのものへの提案で、このリポジトリが default_aidd でない場合は https://github.com/nananastuinfo-gif/default_aidd/issues/new?template=improvement-constitution.yml から登録する」旨と手順書 `docs/improvement-loop.md` への案内を書き、続けて `context`「気づいた作業」、`problem`「問題点」、`proposal`「改善案」(説明に「案がなければ『未定(判断時に検討)』」)、`source`「出典」(input、既定値なし、`placeholder: default_aidd または派生プロジェクトのリポジトリ名`)をすべて必須で置く
- [X] T007 [P] [US1] `.github/ISSUE_TEMPLATE/improvement-template.yml` を T006 と同じ構成で作成する。`name: 改善提案: テンプレート`、`title: "[改善][テンプレート] "`、`labels: [improvement, status:triage, target:template]`、`description` は「Spec Kit のテンプレート、Issue/PR テンプレート、種別ごとの文書テンプレートへの改善提案」、案内のリンク先は `?template=improvement-template.yml`
- [X] T008 [P] [US1] `.github/ISSUE_TEMPLATE/improvement-process.yml` を T006 と同じ構成で作成する。`name: 改善提案: 手順`、`title: "[改善][手順] "`、`labels: [improvement, status:triage, target:process]`、`description` は「手順書(`docs/` 配下)、作業の進め方、ツールの使い方への改善提案」、案内のリンク先は `?template=improvement-process.yml`
- [X] T009 [P] [US1] `.github/ISSUE_TEMPLATE/config.yml` を作成する。`blank_issues_enabled: true`、`contact_links` に「改善ループの手順書」として https://github.com/nananastuinfo-gif/default_aidd/blob/main/docs/improvement-loop.md を 1 件置く
- [X] T010 [US1] `python3 scripts/check-issue-forms.py` を実行し、3 フォームすべて `OK`・終了コード 0 になることを確認する(T006〜T008 に依存)
- [X] T011 [US1] `docs/improvement-loop.md` の「1. 改善提案を登録する」を書く: 3 フォームの使い分け(対象区分の範囲)、複数区分にまたがる場合は主な区分を 1 つ選ぶこと、各入力欄の書き方、Claude Code が登録する場合は内容を提示して運用者の承認を得てから `gh issue create --label improvement,status:triage,target:<区分>` で登録すること(FR-005)。あわせて「付録: 検索条件」に data-model.md の検索条件の表(未判断・30 日超・対応予定・見送り・反映済み・対象区分)を、`https://github.com/nananastuinfo-gif/default_aidd/issues?q=...` の形のリンク付きで書く
- [X] T012 [P] [US1] リポジトリ直下に `CLAUDE.md` を作成する。内容は「改善提案」の節のみ: 作業中に標準(憲章・テンプレート・手順)の改善点に気づいたら、登録内容(対象区分・気づいた作業・問題点・改善案・出典)を運用者に提示し、承認を得てから登録すること。登録方法と書式は `docs/improvement-loop.md` に従うこと。全体の整備はフェーズ 2 で行う旨を 1 行書く

**Checkpoint**: User Story 1 が単独で使える(マージ後に quickstart.md 手順 3 で確認)

---

## Phase 4: User Story 2 - 改善提案を判断し、標準に反映する (Priority: P2)

**Goal**: 提案を 3 区分に振り分けて理由を記録し、反映 PR のマージで「反映済み」にできる

**Independent Test**: US1 で登録した提案 1 件を、手順書だけを見て判断・反映し、提案から判断記録と反映 PR を辿れる(quickstart.md 手順 4)

### Implementation for User Story 2

- [X] T013 [US2] `docs/improvement-loop.md` の「2. 判断する」を書く: contracts/decision-record.md の判断記録コメントの書式(`## 判断記録` / 判断 / 理由 / 反映先 / 判断日)、「`理由` は空欄にしない」「見送りの場合は、どんな前提が変われば再検討するかも書く」こと、判断ごとのラベルとクローズ操作の表(data-model.md の状態の表: 対応予定は `status:*` を外して `decision:*` を付ける、見送りは `status:*` を外し `decision:wontfix` を付けて「not planned」でクローズ、重複は `status:*` を外し統合先を書いて「duplicate」でクローズ、保留は `status:needs-info` を追加)、判断記録コメントは「判断の経過」であり、標準を変更する判断は反映コミットに残すこと(contracts/decision-record.md「憲章 VII との関係」)、過去に見送った提案と同種の場合の扱い
- [X] T014 [US2] `docs/improvement-loop.md` の「3. 反映する」を書く: 対応予定の提案ごとに Issue → ブランチ → PR で進めること、PR 本文に提案ごとの `Closes #N` を書くこと、反映コミットのメッセージに contracts/decision-record.md の書式で背景・判断理由・`Refs #N` を必ず書くこと(憲章 VII の決定記録として Git に残すため)、「憲章の改定」は `/speckit-constitution` で行い、Sync Impact Report を確認・承認後に削除してコミットし、PR タイトルに新しいバージョンを書くこと(FR-012)、反映 PR を中止した場合は新しい判断記録を投稿し、`decision:*` を外して `status:triage` を付け直し、未判断に戻すこと
- [X] T015 [US2] `docs/improvement-loop.md` の「5. 定期的に見直す」を書く: 見直しのタイミング(随時、各機能(フェーズ)の完了時、少なくとも月 1 回、四半期ごとの憲章の見直し)、月 1 回の確認では 30 日を超えそうな未判断の提案を優先すること(SC-004)、使う検索条件(付録へのリンク)

**Checkpoint**: User Story 1 と 2 で、登録から反映までの一巡ができる

---

## Phase 5: User Story 3 - PR の完了時に振り返り、改善提案につなげる (Priority: P3)

**Goal**: すべての PR に振り返り欄があり、出た改善提案がマージ前に登録される

**Independent Test**: PR を 1 件作り、説明欄に振り返り欄が初期表示され、改善提案があれば `#N` で参照している(quickstart.md 手順 5)

### Implementation for User Story 3

- [X] T016 [P] [US3] `.github/pull_request_template.md` を contracts/pr-template.md のとおりに作成する(セクション順: 関連 Issue → 変更内容 → 確認したこと → 振り返り → マージ前チェック。振り返りは「うまくいった点」「問題点」「改善提案(特になし / #N)」の 3 項目)
- [X] T017 [US3] `docs/improvement-loop.md` の「4. 振り返る」を書く: 振り返りの 3 観点と書き方、小さな変更では「特になし」でよいこと、改善提案が出たらマージ前に「1. 改善提案を登録する」の手順で登録して番号を書くこと(FR-014)、機能(フェーズ)を完了する PR では「5. 定期的に見直す」の確認も行うこと

**Checkpoint**: User Story 1〜3 がそれぞれ単独で確認できる

---

## Phase 6: User Story 4 - 派生プロジェクトから改善提案を還元する (Priority: P4)

**Goal**: 派生プロジェクトの運用者が、配布された手順書だけで default_aidd に出典付きの提案を登録できる

**Independent Test**: 手順書の該当節だけを読み、default_aidd のフォームの入力画面まで 5 分以内に到達できる(quickstart.md 手順 6)

### Implementation for User Story 4

- [X] T018 [US4] `docs/improvement-loop.md` の「6. 派生プロジェクトから提案する」を書く: 還元対象(標準そのもの: 憲章・テンプレート・手順の不備や改善)と対象外(派生プロジェクト固有の運用)の判別基準と例、還元対象は default_aidd の 3 フォーム(`https://github.com/nananastuinfo-gif/default_aidd/issues/new?template=improvement-<区分>.yml`)から登録し「出典」に派生プロジェクトのリポジトリ名を書くこと、派生プロジェクト固有の改善は派生プロジェクト内の同じフォームで登録してよいこと、判断に必要な文脈(気づいた作業)を具体的に書くこと

**Checkpoint**: すべてのユーザーストーリーの成果物が揃う

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 整合性の確認と、PR・受け入れ検証

- [X] T019 [P] `kit-dev/roadmap.md` を更新する: 「各フェーズの進め方」の手順 4 を「振り返りを PR に記録し(`docs/improvement-loop.md`)、ロードマップの状態を更新する」に変え、フェーズ 4 の注意点の表に「派生先での Issue フォームの表示確認と、`scripts/setup-labels.sh` の実行を派生時の手順に含める」を追記する
- [X] T020 `docs/improvement-loop.md` 全体を見直す: 憲章 v1.1.0 の Governance・「開発ワークフローと品質ゲート」と矛盾しないこと(FR-019)、contracts/ のラベル名・書式と表記が一致すること、手順書だけで登録から反映まで実施できること(FR-018)
- [X] T021 quickstart.md の手順 1(`python3 scripts/check-issue-forms.py`)を再実行し、結果を記録する
- [ ] T022 実装 PR を作成する。PR テンプレートはマージ前は反映されないため、contracts/pr-template.md の構成で本文を書き、`Closes #3` は付けずに `Refs #3` とする(フェーズ 1 はマージ後の受け入れ検証まで含むため)。振り返り欄を記入し、運用者のレビューとマージを依頼する
- [ ] T023 マージ後に quickstart.md の手順 3〜6 を実施する。手順 3 では実際の気づき 1 件を登録し、手順 4 でその提案を判断・反映して一巡させる(SC-002)。結果と所要時間を反映 PR の振り返りに記録し、同じ PR で `kit-dev/roadmap.md` のフェーズ 1 を「完了」にし、`Closes #3` で Issue #3 を閉じる

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 依存なし
- **Foundational (Phase 2)**: Setup に依存。T004(ラベル作成)は T002 に依存し、運用者の確認が必要
- **User Stories (Phase 3〜6)**: Foundational に依存。US2〜US4 は手順書の別の節を書くため、US1 完了前でも書けるが、受け入れ確認は US1 のフォームがある前提
- **Polish (Phase 7)**: すべてのユーザーストーリーに依存。T023 は実装 PR のマージ後

### User Story Dependencies

- **US1 (P1)**: Foundational 後に開始。他に依存しない
- **US2 (P2)**: 受け入れ確認に US1 で登録した提案を使う
- **US3 (P3)**: 独立。PR テンプレートは US1 と別ファイル
- **US4 (P4)**: 案内リンクは US1 のフォーム(T006〜T008)を指す

### Within Each User Story

- US1 は T005(検証スクリプト、失敗を確認)→ T006〜T009 → T010(成功を確認)の順
- `docs/improvement-loop.md` を編集するタスク(T003, T004, T011, T013, T014, T015, T017, T018, T020)は同じファイルのため並列にしない

### Parallel Opportunities

- T002 と T003
- T006、T007、T008、T009、T012(すべて別ファイル)
- T016 は US1・US2 の作業と並列に実施できる
- T019 は Phase 7 の他のタスクと並列に実施できる

---

## Parallel Example: User Story 1

```bash
# T005 で検証スクリプトの失敗を確認した後、フォームと CLAUDE.md を並列に作成する:
Task: "Create .github/ISSUE_TEMPLATE/improvement-constitution.yml"
Task: "Create .github/ISSUE_TEMPLATE/improvement-template.yml"
Task: "Create .github/ISSUE_TEMPLATE/improvement-process.yml"
Task: "Create .github/ISSUE_TEMPLATE/config.yml"
Task: "Create CLAUDE.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1・2 を完了する(ラベル作成は運用者の確認後)
2. Phase 3(US1)を完了し、検証スクリプトが通ることを確認する
3. この時点で「気づきを記録する受け皿」ができる

### Incremental Delivery

本フェーズは 1 つの実装 PR にまとめる。Issue フォームと PR テンプレートはマージ後にしか GitHub 上で
確認できないため、ストーリーごとに PR を分けても検証の手間が増えるだけだからである。
受け入れ検証(T023)はマージ後に行い、そこで見つかった問題は改善提案として登録して、この改善ループ自体で直す。

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- コミットメッセージには `Refs #3` を付ける
- T004(ラベル作成)と T023 の Issue 登録は公開リポジトリへの変更のため、実行前に運用者の確認を得る(憲章 VI)
