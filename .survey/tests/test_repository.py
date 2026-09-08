import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import check_repository as checker
import survey


class RepositoryChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.previous = survey.ROOT
        survey.ROOT = self.root
        for path in ['README.md', 'papers/README.md', 'papers/inference/README.md', 'papers/training/README.md']:
            survey.put_text(path, '# Example\n')
        survey.write('survey-state/runtime.json', {'current_plan_id': 'day', 'current_plan_path': 'survey-state/daily-plans/day.json'})
        survey.write('survey-state/daily-plans/day.json', {'plan_id': 'day', 'target': 1, 'audit_target': 1,
                     'period_start': '2026-09-08T09:30:00+09:00', 'period_end': '2026-09-09T09:30:00+09:00',
                     'selected_papers': [], 'selected_audits': []})
        survey.write('survey-state/frozen-training.json', {'source_commit': 'baseline', 'files': {'papers/training/README.md': checker.blob_hash(self.root / 'papers/training/README.md')}})
        survey.render()
        self.inventory = {'source_commit': 'fixture', 'files': [{'path': n, 'sha': checker.blob_hash(p)} for n, p in checker.local_files(self.root).items()]}

    def tearDown(self):
        survey.ROOT = self.previous
        self.tmp.cleanup()

    def codes(self):
        return [x['code'] for x in checker.check(self.root, self.inventory)['findings']]

    def test_complete_repository_is_read_only(self):
        before = {n: p.read_bytes() for n, p in checker.local_files(self.root).items()}
        result = checker.check(self.root, self.inventory)
        self.assertEqual(result['status'], 'passed')
        self.assertEqual(before, {n: p.read_bytes() for n, p in checker.local_files(self.root).items()})

    def test_missing_inventory_file_is_not_passed(self):
        self.inventory['files'].append({'path': 'framework-updates/missing.md', 'sha': 'unknown'})
        self.assertIn('missing_file', self.codes())

    def test_links_outside_inference_are_checked(self):
        survey.put_text('framework-updates/example.md', '[missing](missing.md)\n')
        self.assertIn('broken_local_link', self.codes())

    def test_frozen_training_change_is_detected(self):
        survey.put_text('papers/training/README.md', '# Changed\n')
        self.assertIn('frozen_training_changed', self.codes())

    def test_generated_drift_is_detected_without_repair(self):
        survey.put_text('papers/inference/comparison.md', '# Stale\n')
        self.assertIn('stale_generated_file', self.codes())
        self.assertEqual((self.root / 'papers/inference/comparison.md').read_text(), '# Stale\n')

    def test_invalid_json_in_unrelated_directory_is_detected(self):
        survey.put_text('llm-releases/bad.json', '{')
        self.assertIn('invalid_json', self.codes())


if __name__ == '__main__':
    unittest.main()
