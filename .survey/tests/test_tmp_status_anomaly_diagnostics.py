import json
from pathlib import Path
import importlib.util

ROOT = Path(__file__).parents[2]
RENDERER = ROOT / '.survey' / 'scripts' / 'render_status_dashboard.py'


def _load_renderer():
    spec = importlib.util.spec_from_file_location('render_status_dashboard_tmpdiag', RENDERER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_dump_status_anomalies():
    mod = _load_renderer()
    evidence = mod.evidence
    jobs = evidence._collect_jobs(ROOT)
    submissions = evidence._collect_submissions(ROOT)

    print('\n=== MISSING_PAPER_JOBS ===')
    for job_id, job in sorted(jobs.items()):
        if job['kind'] != 'research':
            continue
        payload = job['payload']
        if str(payload.get('status') or '').strip().lower() != 'completed':
            continue
        paper_value = payload.get('paper_path')
        if not isinstance(paper_value, str) or not paper_value.strip():
            continue
        resolved = evidence._resolve_repo_path(ROOT, paper_value)
        if resolved is not None and resolved.is_file():
            continue
        print(json.dumps({
            'job_id': job_id,
            'job_path': str(job['path'].relative_to(ROOT)),
            'canonical_id': payload.get('canonical_id'),
            'title': payload.get('title'),
            'paper_path': paper_value,
        }, ensure_ascii=False, sort_keys=True))

    print('=== ORPHAN_SUBMISSIONS ===')
    for row in sorted(submissions, key=lambda r: str(r['path'])):
        if row['job_id'] and row['job_id'] in jobs:
            continue
        p = row['payload']
        print(json.dumps({
            'submission_path': str(row['path'].relative_to(ROOT)),
            'job_id': row['job_id'],
            'kind': row['kind'],
            'attempt_id': p.get('attempt_id'),
            'canonical_id': p.get('canonical_id'),
            'paper_path': p.get('paper_path'),
            'worker_id': p.get('worker_id'),
        }, ensure_ascii=False, sort_keys=True))

    print('=== END_STATUS_ANOMALIES ===')
