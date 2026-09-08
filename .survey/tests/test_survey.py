import copy
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('survey', Path(__file__).resolve().parents[1] / 'scripts/survey.py')
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)

AT = '2026-09-08T09:30:00+09:00'


class SafetyTests(unittest.TestCase):
    def test_competing_claim(self):
        data = s.lease({}, 'paper:x', 'one', AT, 'acquire')
        with self.assertRaises(ValueError):
            s.lease(data, 'paper:x', 'two', AT, 'acquire')

    def test_expired_owner_cannot_release_successor(self):
        data = s.lease({}, 'paper:x', 'one', AT, 'acquire')
        later = '2026-09-08T10:16:00+09:00'
        s.lease(data, 'paper:x', 'two', later, 'acquire')
        with self.assertRaises(ValueError):
            s.lease(data, 'paper:x', 'one', later, 'release')

    def test_expired_owner_cannot_renew(self):
        data = s.lease({}, 'paper:x', 'one', AT, 'acquire')
        with self.assertRaises(ValueError):
            s.lease(data, 'paper:x', 'one', '2026-09-08T10:15:00+09:00', 'renew')

    def test_independent_resources(self):
        data = s.lease({}, 'paper:x', 'one', AT, 'acquire')
        s.lease(data, 'paper:y', 'two', AT, 'acquire')
        self.assertEqual(len(data['items']), 2)

    def test_retry_exactly_one_week(self):
        data = s.retry_failure({}, 'arXiv:2609.03949', AT, ['official'], 'unavailable')
        self.assertEqual(data['items'][0]['retry_after'], '2026-09-15T09:30:00+09:00')
        with self.assertRaises(ValueError):
            s.retry_failure(data, 'arXiv:2609.03949', '2026-09-15T09:29:59+09:00', ['official'], 'unavailable')

    def test_five_weekly_failures_suspend_not_reject(self):
        data = {}
        for week in range(5):
            at = (s.timestamp(AT) + dt.timedelta(days=7 * week)).isoformat()
            data = s.retry_failure(data, 'arXiv:2609.03949', at, ['official'], 'unavailable')
        self.assertEqual(data['items'][0]['status'], 'dormant')
        self.assertIsNone(data['items'][0]['retry_after'])
        with self.assertRaises(ValueError):
            s.retry_failure(data, 'arXiv:2609.03949', '2026-11-01T00:00:00+09:00', ['official'], 'unavailable')

    def test_missing_or_partial_plan_recovers(self):
        self.assertEqual(s.route({}, AT, AT), 'recover_planning')
        self.assertEqual(s.route({'period_start': AT, 'status': 'selecting'}, AT, AT), 'recover_planning')

    def test_delayed_old_slot_cannot_rewind_new_plan(self):
        plan = {'period_start': '2026-09-09T09:30:00+09:00', 'status': 'ready'}
        self.assertEqual(s.route(plan, AT, AT), 'stale_slot')

    def test_equivalent_timezone(self):
        plan = {'period_start': '2026-09-08T00:30:00+00:00', 'status': 'ready'}
        self.assertEqual(s.route(plan, AT, AT), 'reading')

    def test_outside_slot_rejected(self):
        with self.assertRaises(ValueError):
            s.route({}, '2026-09-09T09:30:00+09:00', AT)

    def test_midnight_hour_is_dedicated_to_integrity(self):
        for minute in ['00', '30', '59']:
            self.assertEqual(s.select_mode('2026-09-09T00:' + minute + ':00+09:00', 0, 8, 30, 9, 30), 'nightly')

    def test_midnight_takes_precedence_over_other_modes(self):
        self.assertEqual(s.select_mode('2026-09-09T00:30:00+09:00', 0, 0, 30, 0, 30), 'nightly')

    def test_non_midnight_slots_keep_their_roles(self):
        for hour, expected in [('08', 'morning'), ('09', 'planning'), ('10', 'reading')]:
            self.assertEqual(s.select_mode('2026-09-09T' + hour + ':30:00+09:00', 0, 8, 30, 9, 30), expected)

    def test_timezone_required(self):
        with self.assertRaises(ValueError):
            s.timestamp('2026-09-08T09:30:00')

    def test_duplicate_canonical_id_rejected(self):
        r = {'canonical_id': 'arXiv:2609.03949', 'identifiers': ['arXiv:2609.03949'], 'path': 'x'}
        with self.assertRaises(ValueError):
            s.identity([r, dict(r, path='y')])

    def test_duplicate_alias_rejected(self):
        with self.assertRaises(ValueError):
            s.identity([{'canonical_id': 'x', 'identifiers': ['DOI:one']}, {'canonical_id': 'y', 'identifiers': ['DOI:one']}])

    def test_identifier_normalization(self):
        self.assertEqual(s.norm_id('arxiv:2609.03949v2'), 'arXiv:2609.03949')
        self.assertEqual(s.norm_id('https://doi.org/10.1234/ABC'), 'DOI:10.1234/abc')

    def test_daily_adjustment_independent_and_idempotent(self):
        plan = {'plan_id': 'd', 'target': 2, 'audit_target': 1,
                'selected_papers': [{'canonical_id': 'a', 'status': 'completed'}, {'canonical_id': 'b', 'status': 'pending'}],
                'selected_audits': [{'canonical_id': 'c', 'status': 'completed'}]}
        result = s.closing_result(plan, {'entries': []})
        self.assertEqual(result['research']['next_target'], 1)
        self.assertEqual(result['research']['carry_ids'], ['b'])
        self.assertEqual(result['audit']['next_target'], 2)
        plan['target'] = 10
        self.assertEqual(s.closing_result(plan, {'entries': [result]}), result)

    def test_unavailable_or_shortfall_does_not_raise_target(self):
        plan = {'plan_id': 'd', 'target': 1, 'audit_target': 1,
                'selected_papers': [{'canonical_id': 'a', 'status': 'completed', 'reason_code': 'insufficient_primary_source'}],
                'selected_audits': []}
        result = s.closing_result(plan, {'entries': []})
        self.assertEqual(result['research']['next_target'], 1)
        self.assertEqual(result['audit']['next_target'], 1)

    def test_cleanup_keeps_interrupted_runs(self):
        root = s.ROOT
        with tempfile.TemporaryDirectory() as tmp:
            try:
                s.ROOT = Path(tmp)
                s.write('survey-state/runs/interrupted.json', {'status': 'running', 'started_at': AT})
                s.write('survey-state/runs/done.json', {'status': 'completed', 'finished_at': AT})
                removed = s.cleanup('2026-09-10T09:30:00+09:00')
                self.assertEqual(removed, ['survey-state/runs/done.json'])
                self.assertTrue((s.ROOT / 'survey-state/runs/interrupted.json').exists())
            finally:
                s.ROOT = root

    def test_completed_without_artifact_detected(self):
        root = s.ROOT
        with tempfile.TemporaryDirectory() as tmp:
            try:
                s.ROOT = Path(tmp)
                s.write('survey-state/paper-identity-index.json', s.identity([]))
                s.write('survey-state/runtime.json', {'current_plan_id': 'day', 'current_plan_path': 'plan.json'})
                s.write('plan.json', {'plan_id': 'day', 'target': 1, 'audit_target': 0, 'selected_papers': [{'canonical_id': 'missing', 'status': 'completed', 'result': 'added'}]})
                for path in ['README.md', 'papers/README.md', 'papers/inference/README.md', 'papers/inference/comparison.md', 'survey-state/STATUS.md']:
                    s.put_text(path, '')
                with self.assertRaisesRegex(ValueError, 'Completed paper missing artifact'):
                    s.validate()
            finally:
                s.ROOT = root


if __name__ == '__main__':
    unittest.main()
