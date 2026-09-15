import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[2]
RENDERER = ROOT / '.survey' / 'scripts' / 'render_status_dashboard.py'


def _load_renderer():
    spec = importlib.util.spec_from_file_location('render_status_dashboard_tmpdiag', RENDERER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class StatusAnomalyDiagnosticTests(unittest.TestCase):
    def test_dump_status_anomalies(self):
        mod = _load_renderer()
        evidence = mod.evidence
        jobs = evidence._collect_jobs(ROOT)
        submissions = evidence._collect_submissions(ROOT)
        results = evidence._collect_results(ROOT)

        missing = []
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
            missing.append((job_id, job))

        paper_texts = []
        for path in (ROOT / 'papers').rglob('*.md'):
            try:
                text = path.read_text(encoding='utf-8', errors='ignore').casefold()
            except OSError:
                continue
            paper_texts.append((path, text))

        print('\n=== MISSING_PAPER_DETAIL ===')
        for job_id, job in missing:
            payload = job['payload']
            canonical = str(payload.get('canonical_id') or '').strip()
            arxiv_number = canonical.split(':', 1)[-1].strip().casefold() if canonical else ''
            title = str(payload.get('title') or '').strip().casefold()
            matches = []
            for path, text in paper_texts:
                rel = str(path.relative_to(ROOT))
                rel_cf = rel.casefold()
                if arxiv_number and (arxiv_number in rel_cf or arxiv_number in text):
                    matches.append(rel)
                elif canonical and canonical.casefold() in text:
                    matches.append(rel)
                elif title and len(title) >= 16 and title in text:
                    matches.append(rel)
            related_submissions = [
                {
                    'path': str(row['path'].relative_to(ROOT)),
                    'attempt_id': row['payload'].get('attempt_id'),
                    'paper_path': row['payload'].get('paper_path'),
                }
                for row in submissions if row['job_id'] == job_id
            ]
            related_results = [
                {
                    'path': str(row['path'].relative_to(ROOT)),
                    'attempt_id': row['payload'].get('attempt_id'),
                    'ok': row['payload'].get('ok'),
                    'job_status': row['payload'].get('job_status'),
                    'submission': row['payload'].get('submission'),
                    'artifact': row['payload'].get('artifact'),
                }
                for row in results if row['job_id'] == job_id
            ]
            print(json.dumps({
                'job_id': job_id,
                'job_path': str(job['path'].relative_to(ROOT)),
                'canonical_id': canonical,
                'title': payload.get('title'),
                'declared_paper_path': payload.get('paper_path'),
                'paper_matches': sorted(set(matches)),
                'submissions': related_submissions,
                'results': related_results,
            }, ensure_ascii=False, sort_keys=True))

        print('=== ORPHAN_DISCOVERY_SUBMISSIONS ===')
        for row in sorted(submissions, key=lambda r: str(r['path'])):
            if row['job_id'] and row['job_id'] in jobs:
                continue
            p = row['payload']
            if row['kind'] != 'discovery':
                continue
            print(json.dumps({
                'submission_path': str(row['path'].relative_to(ROOT)),
                'job_id': row['job_id'],
                'worker_id': p.get('worker_id'),
                'discovery_stats': p.get('discovery_stats'),
                'candidate_count': len(p.get('candidates') or []) if isinstance(p.get('candidates'), list) else None,
            }, ensure_ascii=False, sort_keys=True))
        print('=== END_STATUS_ANOMALIES ===')
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
