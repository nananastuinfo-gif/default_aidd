#!/usr/bin/env python3
"""改善提案の Issue フォームを検証する。

検証ルールは specs/001-improvement-loop/contracts/issue-forms.md に従う。
使い方: python3 scripts/check-issue-forms.py
すべて OK なら終了コード 0、1 件でも NG があれば 1 を返す。
依存: PyYAML
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / ".github" / "ISSUE_TEMPLATE"

FORMS = {
    "improvement-constitution.yml": ["improvement", "status:triage", "target:constitution"],
    "improvement-template.yml": ["improvement", "status:triage", "target:template"],
    "improvement-process.yml": ["improvement", "status:triage", "target:process"],
}

REQUIRED_TOP_KEYS = ["name", "description", "title", "labels", "body"]

# markdown 以外の入力欄の並び: (id, type, required)
EXPECTED_FIELDS = [
    ("context", "textarea", True),
    ("problem", "textarea", True),
    ("proposal", "textarea", True),
    ("source", "input", True),
]


def load_yaml(path: Path) -> tuple[object, str | None]:
    if not path.is_file():
        return None, "ファイルがありません"
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")), None
    except yaml.YAMLError as exc:
        return None, f"YAML として読み込めません: {exc}"


def check_form(path: Path, expected_labels: list[str]) -> list[str]:
    data, error = load_yaml(path)
    if error:
        return [error]
    if not isinstance(data, dict):
        return ["トップレベルがマッピングではありません"]

    errors = [f"トップレベルに `{key}` がありません" for key in REQUIRED_TOP_KEYS if key not in data]
    if errors:
        return errors

    if data["labels"] != expected_labels:
        errors.append(f"labels が {expected_labels} ではありません: {data['labels']}")

    fields = [item for item in data["body"] if item.get("type") != "markdown"]
    actual = [
        (item.get("id"), item.get("type"), bool((item.get("validations") or {}).get("required")))
        for item in fields
    ]
    if actual != EXPECTED_FIELDS:
        errors.append(f"入力欄の並び (id, type, required) が契約と一致しません: {actual}")

    for item in fields:
        if item.get("id") == "source" and "value" in (item.get("attributes") or {}):
            errors.append("source に既定値 (value) が設定されています")

    return errors


def check_config(path: Path) -> list[str]:
    data, error = load_yaml(path)
    if error:
        return [error]
    if not isinstance(data, dict):
        return ["トップレベルがマッピングではありません"]
    errors = []
    if data.get("blank_issues_enabled") is not True:
        errors.append("blank_issues_enabled が true ではありません")
    links = data.get("contact_links") or []
    if len(links) != 1:
        errors.append(f"contact_links が 1 件ではありません: {len(links)} 件")
    return errors


def main() -> int:
    results = {name: check_form(TEMPLATE_DIR / name, labels) for name, labels in FORMS.items()}
    results["config.yml"] = check_config(TEMPLATE_DIR / "config.yml")

    failed = False
    for name, errors in results.items():
        if errors:
            failed = True
            for message in errors:
                print(f"NG: {name}: {message}")
        else:
            print(f"OK: {name}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
