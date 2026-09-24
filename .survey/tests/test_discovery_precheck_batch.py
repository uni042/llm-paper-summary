import threading
import time
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import sys

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / ".survey" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import process_discovery_precheck_batch as batch


class DiscoveryPrecheckBatchTests(unittest.TestCase):
    def test_parallelism_is_bounded(self):
        self.assertEqual(1, batch.bounded_parallelism(0))
        self.assertEqual(4, batch.bounded_parallelism(4))
        self.assertEqual(8, batch.bounded_parallelism(99))

    def test_parallel_runner_reaches_four_workers_but_not_more(self):
        lock = threading.Lock()
        active = 0
        peak = 0

        def worker(path):
            nonlocal active, peak
            with lock:
                active += 1
                peak = max(peak, active)
            time.sleep(0.05)
            with lock:
                active -= 1
            return path.name

        paths = [Path(f"request-{index}.json") for index in range(8)]
        rows = batch.run_parallel_requests(paths, worker=worker, parallelism=4)
        self.assertEqual([path.name for path in paths], rows)
        self.assertGreaterEqual(peak, 2)
        self.assertLessEqual(peak, 4)

    def test_batch_persists_individual_failures_without_aborting_other_requests(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            requests = root / batch.REQUEST_ROOT
            results = root / batch.RESULT_ROOT
            requests.mkdir(parents=True)
            results.mkdir(parents=True)
            snapshot = root / "snapshot"
            snapshot.mkdir()
            ledger = root / "rejections.json"
            ledger.write_text("{}\n", encoding="utf-8")

            good = requests / "good.json"
            bad = requests / "bad.json"
            good.write_text("{}\n", encoding="utf-8")
            bad.write_text("{}\n", encoding="utf-8")

            def fake_process(path, **kwargs):
                if Path(path).name == "bad.json":
                    raise ValueError("boom")
                return {"ok": True, "request_id": "good"}

            with mock.patch.object(batch.process_discovery_precheck, "process_request", side_effect=fake_process):
                with mock.patch.object(
                    batch.process_discovery_precheck,
                    "failure_result",
                    return_value={"ok": False, "error": "ValueError: boom"},
                ):
                    summary = batch.process_batch(
                        root,
                        [good, bad],
                        snapshot_dir=snapshot,
                        rejection_ledger_path=ledger,
                        parallelism=4,
                    )

            self.assertEqual(2, summary["requests"])
            self.assertEqual(1, summary["failures"])
            self.assertTrue((results / "good.json").is_file())
            self.assertTrue((results / "bad.json").is_file())


if __name__ == "__main__":
    unittest.main()
