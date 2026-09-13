import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import reusable_transport_baseline as baseline  # noqa: E402


INBOX = Path(".survey/work-queue/submissions/chat-inbox.json")
RESULT = Path(".survey/work-queue/results/chat-inbox.json")
PAYLOAD = Path(".survey/work-queue/payloads/chat-payload.md")


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class ReusableTransportBaselineTests(unittest.TestCase):
    def test_fallback_dispatch_restores_original_inbox_result_pair(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as sd:
            root = Path(td)
            snapshot = Path(sd)
            write(root / INBOX, '{"job_id":"job-evicpress"}\n')
            write(root / RESULT, '{"job_id":"job-evicpress","repair_required":true}\n')
            write(root / PAYLOAD, "original payload\n")

            baseline.snapshot(root, snapshot)

            write(root / INBOX, '{"job_id":"job-fallback"}\n')
            write(root / RESULT, '{"job_id":"job-fallback","ok":true}\n')
            write(root / PAYLOAD, "temporary fallback payload\n")
            report = root / "fallback-report.json"
            write(report, json.dumps({"action": "dispatched"}) + "\n")

            baseline.restore(root, snapshot, report)

            self.assertEqual((root / INBOX).read_text(), '{"job_id":"job-evicpress"}\n')
            self.assertEqual((root / RESULT).read_text(), '{"job_id":"job-evicpress","repair_required":true}\n')
            self.assertEqual((root / PAYLOAD).read_text(), "original payload\n")

    def test_non_fallback_run_keeps_new_result_but_restores_fixed_input_files(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as sd:
            root = Path(td)
            snapshot = Path(sd)
            write(root / INBOX, '{"job_id":"job-direct"}\n')
            write(root / PAYLOAD, "original payload\n")

            baseline.snapshot(root, snapshot)

            write(root / RESULT, '{"job_id":"job-direct","ok":true}\n')
            write(root / INBOX, '{"job_id":"temporary"}\n')
            write(root / PAYLOAD, "temporary payload\n")
            report = root / "fallback-report.json"
            write(report, json.dumps({"action": "idle"}) + "\n")

            baseline.restore(root, snapshot, report)

            self.assertEqual((root / INBOX).read_text(), '{"job_id":"job-direct"}\n')
            self.assertEqual((root / RESULT).read_text(), '{"job_id":"job-direct","ok":true}\n')
            self.assertEqual((root / PAYLOAD).read_text(), "original payload\n")

    def test_fallback_restores_absent_baseline_result_as_absent(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as sd:
            root = Path(td)
            snapshot = Path(sd)
            write(root / INBOX, '{"job_id":"job-direct"}\n')
            write(root / PAYLOAD, "original payload\n")

            baseline.snapshot(root, snapshot)
            write(root / RESULT, '{"job_id":"job-fallback","ok":true}\n')
            report = root / "fallback-report.json"
            write(report, json.dumps({"action": "dispatched"}) + "\n")

            baseline.restore(root, snapshot, report)

            self.assertFalse((root / RESULT).exists())

    def test_mismatched_baseline_result_is_treated_as_absent(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as sd:
            root = Path(td)
            snapshot = Path(sd)
            write(root / INBOX, '{"job_id":"job-evicpress"}\n')
            write(root / RESULT, '{"job_id":"job-other","ok":false}\n')
            write(root / PAYLOAD, "original payload\n")

            baseline.snapshot(root, snapshot)

            write(root / INBOX, '{"job_id":"job-fallback"}\n')
            write(root / RESULT, '{"job_id":"job-fallback","ok":true}\n')
            report = root / "fallback-report.json"
            write(report, json.dumps({"action": "dispatched"}) + "\n")

            baseline.restore(root, snapshot, report)

            self.assertEqual((root / INBOX).read_text(), '{"job_id":"job-evicpress"}\n')
            self.assertFalse((root / RESULT).exists())


if __name__ == "__main__":
    unittest.main()
