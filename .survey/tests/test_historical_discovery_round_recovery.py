# Regression coverage for immutable replay of the malformed 21:00/22:00 Discovery shape.
import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import recover_discovery_submissions as recovery  # noqa: E402


RENDERER = SCRIPTS / "render_status_dashboard.py"


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_renderer():
    spec = importlib.util.spec_from_file_location("historical_discovery_renderer", RENDERER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class HistoricalDiscoveryRoundRecoveryTests(unittest.TestCase):
    def _write_historical_failure(self, root: Path, *, axis: str = "legacy-axis") -> tuple[Path, Path, dict, dict]:
        sr = root / ".survey"
        submission_path = sr / "work-queue/submissions/discovery-specialist-legacy-r01.json"
        result_path = sr / "work-queue/results/discovery-specialist-legacy-r01.json"
        submission = {
            "operation": "submit_discovery_round",
            "run_key": "2026-09-16T21:00:00+09:00",
            "candidates": [],
            "discovery_stats": {
                "round": 1,
                "axis": axis,
                "candidate_count": 0,
            },
        }
        result = {
            "schema_version": 1,
            "workflow_version": 10,
            "submission": "work-queue/submissions/discovery-specialist-legacy-r01.json",
            "ok": False,
            "error": "ValueError: invalid submit_discovery_round payload",
        }
        write_json(submission_path, submission)
        write_json(result_path, result)
        return submission_path, result_path, submission, result

    def test_malformed_historical_round_is_replayed_without_rewriting_original_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            submission_path, result_path, original_submission, original_result = self._write_historical_failure(root)

            summary = recovery.recover(root / ".survey")

            self.assertEqual(summary["recovered_count"], 1)
            self.assertEqual(json.loads(submission_path.read_text(encoding="utf-8")), original_submission)
            self.assertEqual(json.loads(result_path.read_text(encoding="utf-8")), original_result)

            replay_path = submission_path.with_name("discovery-specialist-legacy-r01.recovered-v1.json")
            replay_result_path = result_path.with_name("discovery-specialist-legacy-r01.recovered-v1.json")
            replay = json.loads(replay_path.read_text(encoding="utf-8"))
            replay_result = json.loads(replay_result_path.read_text(encoding="utf-8"))
            self.assertNotIn("run_key", replay)
            self.assertEqual(replay["discovery_stats"]["run_key"], "2026-09-16T21:00:00+09:00")
            self.assertEqual(replay["discovery_stats"]["round"], "1")
            self.assertEqual(
                replay["recovered_from_submission"],
                "work-queue/submissions/discovery-specialist-legacy-r01.json",
            )
            self.assertTrue(replay_result["ok"])
            self.assertEqual(
                replay_result["submission"],
                "work-queue/submissions/discovery-specialist-legacy-r01.recovered-v1.json",
            )

            second = recovery.recover(root / ".survey")
            self.assertEqual(second["recovered_count"], 0)
            self.assertEqual(json.loads(result_path.read_text(encoding="utf-8")), original_result)
            self.assertEqual(
                len(list(submission_path.parent.glob("discovery-specialist-legacy-r01.recovered-*.json"))),
                1,
            )

    def test_verified_replay_resolves_original_status_orphan_without_deleting_history(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            submission_path, result_path, _, _ = self._write_historical_failure(root)
            recovery.recover(root / ".survey")

            text = load_renderer().build_dashboard(
                root,
                now=datetime(2026, 9, 16, 13, 10, tzinfo=timezone.utc),
            )

            self.assertTrue(submission_path.is_file())
            self.assertTrue(result_path.is_file())
            self.assertIn("| 整合性異常 | **0** |", text)
            self.assertIn("| 対応jobなしsubmission（有効Discovery round除外） | **0** |", text)

    def test_unrelated_invalid_payload_is_not_normalized(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            submission_path, result_path, original_submission, original_result = self._write_historical_failure(
                root,
                axis="",
            )

            summary = recovery.recover(root / ".survey")

            self.assertEqual(summary["recovered_count"], 0)
            self.assertEqual(json.loads(submission_path.read_text(encoding="utf-8")), original_submission)
            self.assertEqual(json.loads(result_path.read_text(encoding="utf-8")), original_result)
            self.assertFalse(
                submission_path.with_name("discovery-specialist-legacy-r01.recovered-v1.json").exists()
            )


if __name__ == "__main__":
    unittest.main()
