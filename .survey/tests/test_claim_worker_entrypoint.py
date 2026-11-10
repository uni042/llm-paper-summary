from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".survey" / "scripts" / "claim_worker.py"


class ClaimWorkerEntrypointTest(unittest.TestCase):
    def test_direct_cli_is_retired_in_favor_of_banked_entrypoint(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(proc.returncode, 0)
        combined = proc.stdout + proc.stderr
        self.assertIn("internal claim-allocation core", combined)
        self.assertIn("claim_worker_with_banks.py", combined)


if __name__ == "__main__":
    unittest.main()
