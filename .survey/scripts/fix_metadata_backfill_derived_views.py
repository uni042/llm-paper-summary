#!/usr/bin/env python3
"""One-shot fixes uncovered by metadata-backfill repository validation."""
from __future__ import annotations

from pathlib import Path


def patch_survey_generator() -> None:
    path = Path('.survey/scripts/survey.py')
    text = path.read_text(encoding='utf-8')

    old_expr = 'r["path"].removeprefix("papers/inference/")'
    new_expr = '_comparison_link(r["path"])'
    if old_expr in text:
        text = text.replace(old_expr, new_expr)

    marker = '\ndef render_comparison(records):\n'
    helper = '''\ndef _comparison_link(path):
    if path.startswith("papers/inference/"):
        return path.removeprefix("papers/inference/")
    if path.startswith("papers/"):
        return "../" + path.removeprefix("papers/")
    return path


def render_comparison(records):
'''
    if 'def _comparison_link(path):' not in text:
        if marker not in text:
            raise SystemExit('render_comparison marker not found')
        text = text.replace(marker, helper, 1)

    root_write = '        root.write_text(content, encoding="utf-8")\n'
    root_update = '''        content = re.sub(r"- \\[Inference / 推論\\]\\(papers/inference/\\) — \\*\\*\\d+本\\*\\*", f"- [Inference / 推論](papers/inference/) — **{counts['inference']}本**", content)
        content = re.sub(r"- \\[Training / 学習\\]\\(papers/training/\\) — \\*\\*\\d+本（凍結）\\*\\*", f"- [Training / 学習](papers/training/) — **{counts['training']}本（凍結）**", content)
        survey_line = f"  - [Survey / サーベイ](papers/survey/) — **{counts['survey']}本**"
        if "[Survey / サーベイ](papers/survey/)" not in content:
            training_line = re.search(r"^  - \\[Training / 学習\\].*$", content, flags=re.M)
            if training_line:
                content = content[:training_line.end()] + "\\n" + survey_line + content[training_line.end():]
        else:
            content = re.sub(r"^  - \\[Survey / サーベイ\\]\\(papers/survey/\\) — \\*\\*\\d+本\\*\\*$", survey_line, content, flags=re.M)
        root.write_text(content, encoding="utf-8")
        block("README.md", f"推論：**{counts['inference']}本** ／ 学習：**{counts['training']}本** ／ サーベイ：**{counts['survey']}本**。 [推論一覧](papers/inference/README.md) ／ [学習一覧](papers/training/README.md) ／ [サーベイ一覧](papers/survey/README.md) ／ [研究比較](papers/inference/comparison.md)")
'''
    if 'block("README.md", f"推論：**{counts[\'inference\']}本**' not in text:
        if root_write not in text:
            raise SystemExit('root README write marker not found')
        text = text.replace(root_write, root_update, 1)

    path.write_text(text, encoding='utf-8')


def patch_root_readme_links() -> None:
    path = Path('README.md')
    text = path.read_text(encoding='utf-8')
    text = text.replace('.survey/survey-state/STATUS.md', '.survey/reports/metadata-coverage-latest.json')
    text = text.replace('.survey/survey-state/integrity/README.md', '.survey/reports/consistency-latest.json')
    path.write_text(text, encoding='utf-8')


def main() -> int:
    patch_survey_generator()
    patch_root_readme_links()
    print('derived_view_consistency_fix=applied')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
