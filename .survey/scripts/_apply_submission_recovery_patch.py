from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected exactly one match in {path}, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


process = Path(".survey/scripts/process_immutable_submission.py")
replace_once(
    process,
    '''def _precheck_paper(repo_root: Path, descriptor: dict[str, Any]) -> None:\n    paper = repo_root / descriptor["paper_path"]\n    expected = descriptor.get("expected_blob_sha")\n    if not paper.exists():\n        return\n    if not expected:\n        raise ValueError("expected_blob_sha is required when updating an existing paper")\n    current = immutable_submission.git_blob_sha(paper.read_bytes())\n    if current != expected:\n        raise ValueError(f"paper blob changed: expected {expected}, current {current}")\n''',
    '''def _precheck_paper(\n    repo_root: Path,\n    descriptor: dict[str, Any],\n    *,\n    rendered_content: str | None = None,\n) -> None:\n    paper = repo_root / descriptor["paper_path"]\n    expected = descriptor.get("expected_blob_sha")\n    if not paper.exists():\n        return\n    if not expected:\n        raise ValueError("expected_blob_sha is required when updating an existing paper")\n    current_bytes = paper.read_bytes()\n    current = immutable_submission.git_blob_sha(current_bytes)\n    if current != expected:\n        desired_bytes = None\n        if rendered_content is not None:\n            desired_bytes = (rendered_content.rstrip() + "\\n").encode("utf-8")\n        if desired_bytes is not None and current_bytes == desired_bytes:\n            return\n        raise ValueError(f"paper blob changed: expected {expected}, current {current}")\n''',
)
replace_once(
    process,
    '''    if status == "completed":\n        _precheck_paper(repo_root, descriptor)\n        sub["content"] = render_descriptor(repo_root, descriptor)\n''',
    '''    if status == "completed":\n        rendered_content = render_descriptor(repo_root, descriptor)\n        _precheck_paper(repo_root, descriptor, rendered_content=rendered_content)\n        sub["content"] = rendered_content\n''',
)

queue_worker = Path(".survey/scripts/queue_worker.py")
replace_once(
    queue_worker,
    '''        current = p.stdout.strip() if p.returncode == 0 else None\n        if current != expected_sha:\n            raise ValueError(f"paper blob changed: expected {expected_sha}, current {current}")\n''',
    '''        current = p.stdout.strip() if p.returncode == 0 else None\n        if current != expected_sha:\n            if target.read_bytes() != content.encode("utf-8"):\n                raise ValueError(f"paper blob changed: expected {expected_sha}, current {current}")\n''',
)

workflow = Path(".github/workflows/survey-submission-fast.yml")
replace_once(
    workflow,
    '''        required: true\n        type: string\n\npermissions:\n''',
    '''        required: true\n        type: string\n  schedule:\n    - cron: '7/10 * * * *'\n\npermissions:\n''',
)
replace_once(
    workflow,
    '''                echo 'Immutable submission failure result was persisted to main.' >&2\n                exit 1\n''',
    '''                echo 'Immutable submission failure result was persisted to main.' >&2\n                echo 'Periodic drain will retry it only when explicitly classified retryable.' >&2\n                exit 1\n''',
)
