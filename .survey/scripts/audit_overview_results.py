#!/usr/bin/env python3
"""Audit whether each paper overview states a representative research result."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

PAPER_FAMILIES = ("inference", "training", "survey")
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
MOVED_RE = re.compile(r"^#\s+Moved(?:\s|$)", re.I | re.M)
MARKDOWN_RE = re.compile(r"!?\[([^\]]*)\]\([^)]+\)|`([^`]*)`|[*_~]")
HTML_RE = re.compile(r"<[^>]+>")
URL_RE = re.compile(r"https?://\S+")

# A number alone is not enough; these units/expressions indicate an empirical
# or analytical outcome rather than a year, model size, or section number.
QUANTITATIVE_RESULT_RE = re.compile(
    r"(?:\d+(?:\.\d+)?\s*(?:%|％|倍|x|×|ms|s|秒|ミリ秒|GB|MB|TB|W|J|tokens?/s|tok/s|トークン/秒|件/秒))"
    r"|(?:\d+(?:\.\d+)?\s*(?:ポイント|pt))",
    re.I,
)

# Qualitative papers and surveys may not have one natural headline number.
# In those cases the overview must explicitly state what evaluation/analysis
# established, not merely what the method intends to improve.
RESULT_CONTEXT_RE = re.compile(
    r"(?:評価|実験|測定|比較|解析|分析|検証|ベンチマーク|代表結果|主要結果|結果)"
    r"(?:では|から|により|として|の結果|で)?[^。！？]{0,100}"
    r"(?:示した|示す|確認した|確認できた|分かった|明らかになった|達成した|達成|"
    r"短縮した|削減した|低減した|改善した|向上した|高速化した|上回った|抑えた|"
    r"維持した|同等だった|優位だった|支配的|逆転する|有効だった)",
)
DIRECT_RESULT_RE = re.compile(
    r"(?:ことを示した|ことが分かった|ことを確認した|結果を得た|"
    r"既存方式(?:より|に比べて|と比べて)[^。！？]{0,80}(?:高速|短縮|削減|改善|向上|低減|上回))"
)


@dataclass
class OverviewAudit:
    status: str
    overview: str
    has_result_signal: bool
    has_quantitative_signal: bool
    failures: list[str]


@dataclass
class FileAudit:
    path: str
    status: str
    has_overview: bool
    has_result_signal: bool
    has_quantitative_signal: bool
    overview_chars: int
    failures: list[str]


def _clean(text: str) -> str:
    text = URL_RE.sub(" ", text)
    text = HTML_RE.sub(" ", text)

    def repl(match: re.Match[str]) -> str:
        return match.group(1) or match.group(2) or ""

    text = MARKDOWN_RE.sub(repl, text)
    text = re.sub(r"^\s*>\s?", "", text, flags=re.M)
    text = re.sub(r"^\s*(?:[-*+] |\d+[.)] )", "", text, flags=re.M)
    return re.sub(r"\s+", " ", text).strip()


def extract_overview(body: str) -> str:
    collecting = False
    lines: list[str] = []
    for line in body.splitlines():
        match = H2_RE.match(line)
        if match:
            title = re.sub(r"[`*_~]", "", match.group(1)).strip()
            if collecting:
                break
            collecting = title == "概要" or title.startswith("概要 ")
            continue
        if collecting:
            lines.append(line)
    return _clean("\n".join(lines))


def audit_overview_text(overview: str) -> OverviewAudit:
    overview = _clean(overview)
    quantitative = bool(QUANTITATIVE_RESULT_RE.search(overview))
    contextual = bool(RESULT_CONTEXT_RE.search(overview) or DIRECT_RESULT_RE.search(overview))
    has_result = quantitative or contextual
    failures: list[str] = []
    if not overview:
        failures.append("概要節がない、または概要が空")
    elif not has_result:
        failures.append(
            "概要に代表結果がない。最もアピールしたい定量結果、または論文を象徴する定性的結果を1〜2文で明示する"
        )
    return OverviewAudit(
        status="PASS" if not failures else "FAIL",
        overview=overview,
        has_result_signal=has_result,
        has_quantitative_signal=quantitative,
        failures=failures,
    )


def _body_without_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    parts = text.split("---", 2)
    return parts[2] if len(parts) >= 3 else text


def is_paper(path: Path, body: str) -> bool:
    if path.name.casefold() in {"readme.md", "comparison.md"}:
        return False
    return not bool(MOVED_RE.search(body))


def audit_file(path: Path, repo_root: Path) -> FileAudit:
    text = path.read_text(encoding="utf-8", errors="ignore")
    body = _body_without_frontmatter(text)
    overview = extract_overview(body)
    result = audit_overview_text(overview)
    return FileAudit(
        path=path.relative_to(repo_root).as_posix(),
        status=result.status,
        has_overview=bool(overview),
        has_result_signal=result.has_result_signal,
        has_quantitative_signal=result.has_quantitative_signal,
        overview_chars=len(overview),
        failures=result.failures,
    )


def markdown_report(results: list[FileAudit]) -> str:
    failed = [r for r in results if r.status == "FAIL"]
    quantitative = [r for r in results if r.has_quantitative_signal]
    qualitative = [r for r in results if r.has_result_signal and not r.has_quantitative_signal]
    lines = [
        "# 概要・代表結果の品質監査",
        "",
        f"- 生成日時: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"- 対象: {len(results)}件（Inference / Training / Survey）",
        f"- 代表結果あり: {len(results) - len(failed)}件",
        f"- 定量結果を検出: {len(quantitative)}件",
        f"- 明示的な定性的結果を検出: {len(qualitative)}件",
        f"- 基準未達: {len(failed)}件",
        "- 基準: 概要だけを読んでも、論文の代表的な結果が少なくとも1つ分かること",
        "- 優先順位: 論文が最もアピールする主要な定量結果 > その他の象徴的な定量結果 > 明示的な定性的結論",
        "- 数値を書く場合は比較対象・条件・指標が分かる文にし、単独の倍率や百分率だけを置かない",
        "",
        "## 基準未達",
        "",
    ]
    if not failed:
        lines.append("なし")
    for item in failed:
        lines.append(f"- `{item.path}` — " + "; ".join(item.failures))
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--markdown-out")
    parser.add_argument("--json-out")
    parser.add_argument("--no-fail-exit", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    results: list[FileAudit] = []
    for family in PAPER_FAMILIES:
        root = repo_root / "papers" / family
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            text = path.read_text(encoding="utf-8", errors="ignore")
            body = _body_without_frontmatter(text)
            if is_paper(path, body):
                results.append(audit_file(path, repo_root))

    report = markdown_report(results)
    if args.markdown_out:
        output = repo_root / args.markdown_out
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")

    if args.json_out:
        output = repo_root / args.json_out
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "criteria": {
                        "families": list(PAPER_FAMILIES),
                        "overview_must_include_representative_result": True,
                        "result_preference": [
                            "headline quantitative result",
                            "representative quantitative result",
                            "explicit qualitative finding",
                        ],
                    },
                    "results": [asdict(item) for item in results],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    failed = any(item.status == "FAIL" for item in results)
    return 0 if args.no_fail_exit or not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
