#!/usr/bin/env python3
"""Repository-wide audit for compact one-line paper-list summaries."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import yaml

from list_summary import (
    DEFAULT_MAX_CHARS,
    DEFAULT_MIN_CHARS,
    audit_list_summary,
)
from paper_audit_scope import PAPER_AUDIT_BASELINE, added_paper_paths

PAPER_FAMILIES = ("inference", "training", "survey")
MOVED_RE = re.compile(r"^#\s+Moved(?:\s|$)", re.I | re.M)


@dataclass
class Result:
    path: str
    status: str
    summary: str
    char_count: int
    japanese_ratio: float
    failures: list[str]
    warnings: list[str]


def front(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    return yaml.safe_load(parts[1]) or {}, parts[2]


def is_paper(path: Path, body: str) -> bool:
    if path.name.casefold() in {"readme.md", "comparison.md"}:
        return False
    return not bool(MOVED_RE.search(body))


def audit_file(path: Path, repo_root: Path) -> Result:
    meta, _ = front(path)
    value = meta.get("list_summary")
    summary = value.strip() if isinstance(value, str) else ""
    quality = audit_list_summary(summary)
    failures = list(quality.failures)
    if not summary:
        failures.insert(0, "frontmatter list_summary is required")
    return Result(
        path=path.relative_to(repo_root).as_posix(),
        status="FAIL" if failures else quality.status,
        summary=summary,
        char_count=quality.char_count,
        japanese_ratio=quality.japanese_ratio,
        failures=failures,
        warnings=quality.warnings,
    )


def markdown_report(results: list[Result]) -> str:
    failed = [r for r in results if r.status == "FAIL"]
    warned = [r for r in results if r.status == "WARN"]
    passed = [r for r in results if r.status == "PASS"]
    lines = [
        "# 論文一覧・一文要約の品質監査",
        "",
        f"- 生成日時: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"- 対象: {len(results)}件（Inference / Training / Survey）",
        f"- 合格: {len(passed)}件 / 警告: {len(warned)}件 / 不合格: {len(failed)}件",
        f"- 長さ: {DEFAULT_MIN_CHARS}〜{DEFAULT_MAX_CHARS}文字",
        "- 日本語比率: 70%未満は不合格、80%未満は警告",
        "- 日本語化できる英語専門語、改行、URL、Markdown断片は不合格",
        "- frontmatterの明示的なlist_summaryだけを監査し、本文・summaryから生成しない",
        "",
        "## 基準未達",
        "",
    ]
    if not failed:
        lines.append("なし")
    for r in failed:
        lines += [
            f"### `{r.path}`",
            "",
            f"- 一文要約: {r.summary}",
            f"- 文字数: {r.char_count} / 日本語比率: {r.japanese_ratio:.1%}",
        ]
        lines.extend(f"- **不合格理由:** {reason}" for reason in r.failures)
        lines.append("")
    if warned:
        lines += ["## 警告のみ", ""]
        for r in warned:
            lines.append(f"- `{r.path}` — " + "; ".join(r.warnings))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--baseline-commit", default=PAPER_AUDIT_BASELINE)
    ap.add_argument("--markdown-out")
    ap.add_argument("--json-out")
    ap.add_argument("--no-fail-exit", action="store_true")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    results: list[Result] = []
    added = added_paper_paths(repo_root, args.baseline_commit)
    for relative in sorted(added):
        path = repo_root / relative
        if not path.exists():
            continue
        meta, body = front(path)
        if is_paper(path, body):
            results.append(audit_file(path, repo_root))

    report = markdown_report(results)
    if args.markdown_out:
        out = repo_root / args.markdown_out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    if args.json_out:
        out = repo_root / args.json_out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "criteria": {
                        "min_chars": DEFAULT_MIN_CHARS,
                        "max_chars": DEFAULT_MAX_CHARS,
                        "families": list(PAPER_FAMILIES),
                        "min_japanese_ratio": 0.70,
                        "warn_japanese_ratio": 0.80,
                        "bare_english_terms_allowed": 0,
                        "worker_authored_preferred": True,
                        "legacy_overview_fallback": False,
                        "baseline_commit": args.baseline_commit,
                    },
                    "results": [asdict(r) for r in results],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    failed = any(r.status == "FAIL" for r in results)
    return 0 if args.no_fail_exit or not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
