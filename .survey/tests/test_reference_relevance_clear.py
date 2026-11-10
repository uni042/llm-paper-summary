from __future__ import annotations

import json
import hashlib
import os
import subprocess
import sys
import tempfile
import time
import textwrap
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import process_reference_relevance_requests as processor  # noqa: E402
import reference_relevance_ledger as ledger  # noqa: E402


class ReferenceRelevanceClearTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.request_dir = self.root / ".survey/work-queue/reference-curation/requests"
        self.result_dir = self.root / ".survey/work-queue/reference-curation/results"
        self.request_dir.mkdir(parents=True)
        self.unrelated = self.root / ".survey/work-queue/reference-curation/unrelated-papers.json"
        self.borderline = self.root / ".survey/work-queue/reference-curation/borderline-papers.json"
        self.reviews = self.root / ".survey/work-queue/reference-curation/reviews"
        self.canonical = "arXiv:2609.90001"
        self.alias = "DOI:10.48550/arXiv.2609.90001"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _request(self, request_id: str = "clear-1", **overrides: object) -> Path:
        proof = overrides.pop("root_review_proof", None)
        if proof is None and overrides.get("operation", "clear_relevance") == "clear_relevance":
            proof = self._review_proof()
        payload: dict[str, object] = {
            "schema_version": 1,
            "request_id": request_id,
            "operation": "clear_relevance",
            "canonical_id": self.canonical,
            "reason": "Root review reclassified this paper as relevant to inference efficiency.",
            "identity_tokens": [self.alias],
            "root_review_proof": proof,
        }
        payload.update(overrides)
        path = self.request_dir / f"{request_id}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def _review_proof(
        self,
        review_id: str = "root-review-20261024-01",
        *,
        canonical_id: str | None = None,
        aliases: list[str] | None = None,
        action: str = "clear_relevance",
        root_decision: str = "move",
        filename: str | None = None,
    ) -> dict[str, str]:
        canonical = canonical_id or self.canonical
        verified_aliases = aliases or [canonical, self.alias]
        self.reviews.mkdir(parents=True, exist_ok=True)
        review_path = self.reviews / (filename or f"{review_id}.json")
        artifact = {
            "schema_version": 1,
            "record_type": "reference_relevance_clear_review",
            "review_id": review_id,
            "action": action,
            "root_decision": root_decision,
            "canonical_id": canonical,
            "verified_aliases": verified_aliases,
        }
        data = json.dumps(artifact, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
        review_path.write_bytes(data)
        return {
            "review_id": review_id,
            "review_path": review_path.relative_to(self.root).as_posix(),
            "review_sha256": hashlib.sha256(data).hexdigest(),
        }

    def _run_concurrent(self, scripts: list[str]) -> list[subprocess.CompletedProcess[str]]:
        gate = self.root / "start-workers"
        processes = [
            subprocess.Popen(
                [sys.executable, "-c", textwrap.dedent(script), str(self.root), str(gate), str(SCRIPTS)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            for script in scripts
        ]
        gate.write_text("go", encoding="utf-8")
        completed = []
        for process in processes:
            stdout, stderr = process.communicate(timeout=20)
            completed.append(subprocess.CompletedProcess(process.args, process.returncode, stdout, stderr))
        return completed

    def _write_ledger(self, path: Path, classification: str, records: dict[str, object]) -> bytes:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": 1,
            "classification": classification,
            "purpose": f"synthetic {classification}",
            "records": records,
        }
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path.read_bytes()

    def _read(self, path: Path) -> dict[str, object]:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_clear_removes_only_reviewed_canonical_and_alias_rows_from_both_ledgers(self) -> None:
        unrelated_row = {"classification": "unrelated", "canonical_id": self.canonical, "identity_tokens": [self.canonical, self.alias], "reason": "old ruling"}
        borderline_row = {"classification": "borderline", "canonical_id": self.canonical, "identity_tokens": [self.canonical, self.alias], "reason": "old uncertainty"}
        other_unrelated = {"classification": "unrelated", "canonical_id": "arXiv:2609.90002", "identity_tokens": ["arXiv:2609.90002"], "reason": "keep"}
        other_borderline = {"classification": "borderline", "canonical_id": "arXiv:2609.90003", "identity_tokens": ["arXiv:2609.90003"], "reason": "keep"}
        self._write_ledger(self.unrelated, "unrelated", {self.canonical: unrelated_row, "arXiv:2609.90002": other_unrelated})
        self._write_ledger(self.borderline, "borderline", {self.alias: borderline_row, "arXiv:2609.90003": other_borderline})
        self._request()

        summary = processor.process_pending(self.root)

        self.assertTrue(summary["ok"])
        self.assertEqual(summary["processed_count"], 1)
        self.assertEqual(self._read(self.unrelated)["records"], {"arXiv:2609.90002": other_unrelated})
        self.assertEqual(self._read(self.borderline)["records"], {"arXiv:2609.90003": other_borderline})
        result = self._read(self.result_dir / "clear-1.json")
        self.assertTrue(result["ok"])
        self.assertEqual(result["request_operation"], "clear_relevance")
        self.assertNotIn("classification", result)
        self.assertEqual(result["reason"], "Root review reclassified this paper as relevant to inference efficiency.")
        self.assertEqual(set(result["identity_tokens"]), {self.canonical, "DOI:10.48550/arxiv.2609.90001"})
        self.assertEqual({(row["ledger"], row["key"]) for row in result["removed_rows"]}, {
            ("unrelated", self.canonical), ("borderline", self.alias)
        })
        self.assertEqual(result["root_review_proof"]["review_id"], "root-review-20261024-01")

    def test_missing_target_is_a_noop_with_review_proof_and_no_positive_classification(self) -> None:
        self._request("clear-noop")
        summary = processor.process_pending(self.root)
        self.assertTrue(summary["ok"])
        result = self._read(self.result_dir / "clear-noop.json")
        self.assertEqual(result["removed_rows"], [])
        self.assertEqual(set(result["identity_tokens"]), {self.canonical, "DOI:10.48550/arxiv.2609.90001"})
        self.assertNotIn("classification", result)
        self.assertFalse(self.unrelated.exists())
        self.assertFalse(self.borderline.exists())

    def test_existing_result_makes_clear_request_idempotent_and_preserves_immutable_history(self) -> None:
        self._write_ledger(self.unrelated, "unrelated", {self.canonical: {"classification": "unrelated", "canonical_id": self.canonical, "identity_tokens": [self.canonical], "reason": "old"}})
        self._request("clear-idempotent")
        first = processor.process_pending(self.root)
        result_path = self.result_dir / "clear-idempotent.json"
        result_bytes = result_path.read_bytes()
        # A replay must not clear a newly re-added row or mutate the original result.
        self._write_ledger(self.unrelated, "unrelated", {self.canonical: {"classification": "unrelated", "canonical_id": self.canonical, "identity_tokens": [self.canonical], "reason": "later event"}})
        second = processor.process_pending(self.root)
        self.assertEqual(first["processed_count"], 1)
        self.assertEqual(second["already_processed_count"], 1)
        self.assertEqual(result_path.read_bytes(), result_bytes)
        self.assertIn(self.canonical, self._read(self.unrelated)["records"])
        self.assertTrue((self.request_dir / "clear-idempotent.json").exists())

    def test_cross_canonical_alias_collision_fails_closed_without_writes(self) -> None:
        self._write_ledger(self.unrelated, "unrelated", {self.canonical: {"classification": "unrelated", "canonical_id": self.canonical, "identity_tokens": [self.canonical, self.alias], "reason": "target"}})
        before_borderline = self._write_ledger(self.borderline, "borderline", {"arXiv:2609.90002": {"classification": "borderline", "canonical_id": "arXiv:2609.90002", "identity_tokens": ["arXiv:2609.90002", self.alias], "reason": "different owner"}})
        before_unrelated = self.unrelated.read_bytes()
        self._request("clear-collision")

        summary = processor.process_pending(self.root)

        self.assertFalse(summary["ok"])
        self.assertEqual(summary["retryable_error_count"], 1)
        self.assertEqual(self.unrelated.read_bytes(), before_unrelated)
        self.assertEqual(self.borderline.read_bytes(), before_borderline)
        self.assertTrue((self.request_dir / "clear-collision.json").exists())
        self.assertFalse((self.result_dir / "clear-collision.json").exists())

    def test_root_review_alias_tamper_is_invalid_and_does_not_change_ledgers(self) -> None:
        before_unrelated = self._write_ledger(self.unrelated, "unrelated", {self.canonical: {"classification": "unrelated", "canonical_id": self.canonical, "identity_tokens": [self.canonical], "reason": "old"}})
        before_borderline = self._write_ledger(self.borderline, "borderline", {"arXiv:2609.90002": {"classification": "borderline", "canonical_id": "arXiv:2609.90002", "identity_tokens": ["arXiv:2609.90002"], "reason": "keep"}})
        proof = self._review_proof(
            "root-review-1",
            aliases=[self.canonical, "DOI:10.1234/not-the-reviewed-alias"],
        )
        self._request("clear-tampered", root_review_proof=proof)

        summary = processor.process_pending(self.root)

        self.assertTrue(summary["ok"])
        self.assertEqual(summary["invalid_request_count"], 1)
        self.assertEqual(self.unrelated.read_bytes(), before_unrelated)
        self.assertEqual(self.borderline.read_bytes(), before_borderline)
        failure = self._read(self.result_dir / "clear-tampered.json")
        self.assertEqual(failure["failure_class"], "invalid_request")

    def test_root_review_proof_requires_real_confined_untampered_json_artifact(self) -> None:
        before_unrelated = self._write_ledger(self.unrelated, "unrelated", {self.canonical: {"classification": "unrelated", "canonical_id": self.canonical, "identity_tokens": [self.canonical], "reason": "old"}})
        before_borderline = self._write_ledger(self.borderline, "borderline", {})
        cases: list[tuple[str, dict[str, object]]] = []

        missing = self._review_proof("review-missing")
        (self.root / missing["review_path"]).unlink()
        cases.append(("missing", missing))

        tampered = self._review_proof("review-tampered")
        artifact_path = self.root / tampered["review_path"]
        artifact = self._read(artifact_path)
        artifact["root_decision"] = "unrelated"
        artifact_path.write_text(json.dumps(artifact), encoding="utf-8")
        cases.append(("tampered", tampered))

        outside = self._review_proof("review-outside")
        outside["review_path"] = "reports/outside.json"
        cases.append(("outside", outside))

        wrong_canonical = self._review_proof(
            "review-wrong-canonical",
            canonical_id="arXiv:2609.90099",
            aliases=["arXiv:2609.90099", "DOI:10.1234/other"],
        )
        cases.append(("wrong-canonical", wrong_canonical))

        wrong_decision = self._review_proof("review-wrong-decision", root_decision="unrelated")
        cases.append(("wrong-decision", wrong_decision))

        for suffix, proof in cases:
            request_id = f"clear-proof-{suffix}"
            self._request(request_id, root_review_proof=proof)

        for field in ("review_id", "review_path", "review_sha256"):
            proof = self._review_proof(f"review-nonstring-{field}")
            proof[field] = 7
            self._request(f"clear-nonstring-{field}", root_review_proof=proof)
        self._request("clear-nonstring-object", root_review_proof=["not", "an", "object"])

        summary = processor.process_pending(self.root)

        self.assertEqual(summary["invalid_request_count"], len(cases) + 4)
        self.assertEqual(self.unrelated.read_bytes(), before_unrelated)
        self.assertEqual(self.borderline.read_bytes(), before_borderline)
        for suffix, _proof in cases:
            self.assertFalse(self._read(self.result_dir / f"clear-proof-{suffix}.json")["ok"])

    def test_review_artifact_symlink_is_rejected_when_supported(self) -> None:
        proof = self._review_proof("review-symlink")
        target = self.root / proof["review_path"]
        link = target.with_name("linked-review.json")
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlinks unavailable: {exc}")
        proof["review_path"] = link.relative_to(self.root).as_posix()
        request = self._request("clear-symlink", root_review_proof=proof)
        summary = processor.process_pending(self.root)
        self.assertEqual(summary["invalid_request_count"], 1)
        self.assertFalse(self._read(self.result_dir / request.name)["ok"])

    def test_review_id_must_be_unique_in_the_review_directory(self) -> None:
        proof = self._review_proof("review-duplicate")
        duplicate = self._review_proof("review-duplicate", filename="second-file.json")
        self._request("clear-duplicate-review", root_review_proof=proof)
        summary = processor.process_pending(self.root)
        self.assertEqual(summary["invalid_request_count"], 1)
        self.assertEqual(self._read(self.result_dir / "clear-duplicate-review.json")["failure_class"], "invalid_request")

    def test_concurrent_mark_and_clear_preserve_both_updates(self) -> None:
        target_row = {"classification": "unrelated", "canonical_id": self.canonical, "identity_tokens": [self.canonical, self.alias], "reason": "old"}
        keep_row = {"classification": "unrelated", "canonical_id": "arXiv:2609.90002", "identity_tokens": ["arXiv:2609.90002"], "reason": "keep"}
        self._write_ledger(self.unrelated, "unrelated", {self.canonical: target_row, "arXiv:2609.90002": keep_row})
        self._write_ledger(self.borderline, "borderline", {self.canonical: {"classification": "borderline", "canonical_id": self.canonical, "identity_tokens": [self.canonical, self.alias], "reason": "old"}})
        self._request("clear-concurrent-mark")
        mark_script = """
            import sys, time
            from pathlib import Path
            root, gate, scripts = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
            sys.path.insert(0, str(scripts))
            import reference_relevance_ledger as ledger
            while not gate.exists(): time.sleep(0.01)
            ledger.mark_unrelated(root / '.survey/work-queue/reference-curation/unrelated-papers.json', canonical_id='arXiv:2609.90010', reason='concurrent independent mark', identity_tokens=['arXiv:2609.90010'])
        """
        clear_script = """
            import sys, time
            from pathlib import Path
            root, gate, scripts = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
            sys.path.insert(0, str(scripts))
            import process_reference_relevance_requests as processor
            while not gate.exists(): time.sleep(0.01)
            processor.process_request(root, root / '.survey/work-queue/reference-curation/requests/clear-concurrent-mark.json')
        """
        results = self._run_concurrent([mark_script, clear_script])
        self.assertEqual([result.returncode for result in results], [0, 0], [result.stderr for result in results])
        unrelated = self._read(self.unrelated)["records"]
        borderline = self._read(self.borderline)["records"]
        self.assertEqual(set(unrelated), {"arXiv:2609.90002", "arXiv:2609.90010"})
        self.assertEqual(borderline, {})

    def test_concurrent_distinct_clears_preserve_both_targets_and_other_rows(self) -> None:
        canonical_b = "arXiv:2609.90004"
        alias_b = "DOI:10.48550/arXiv.2609.90004"
        rows = {
            self.canonical: {"classification": "unrelated", "canonical_id": self.canonical, "identity_tokens": [self.canonical, self.alias], "reason": "old"},
            canonical_b: {"classification": "unrelated", "canonical_id": canonical_b, "identity_tokens": [canonical_b, alias_b], "reason": "old"},
            "arXiv:2609.90005": {"classification": "unrelated", "canonical_id": "arXiv:2609.90005", "identity_tokens": ["arXiv:2609.90005"], "reason": "keep"},
        }
        self._write_ledger(self.unrelated, "unrelated", rows)
        self._write_ledger(self.borderline, "borderline", {
            key: {**row, "classification": "borderline"} for key, row in rows.items()
        })
        proof_a = self._review_proof("review-clear-a")
        proof_b = self._review_proof("review-clear-b", canonical_id=canonical_b, aliases=[canonical_b, alias_b])
        self._request("clear-a", root_review_proof=proof_a)
        self._request("clear-b", canonical_id=canonical_b, identity_tokens=[alias_b], root_review_proof=proof_b)
        scripts = [f"""
            import sys, time
            from pathlib import Path
            root, gate, scripts = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
            sys.path.insert(0, str(scripts))
            import process_reference_relevance_requests as processor
            while not gate.exists(): time.sleep(0.01)
            processor.process_request(root, root / '.survey/work-queue/reference-curation/requests/{request_id}.json')
        """ for request_id in ("clear-a", "clear-b")]
        results = self._run_concurrent(scripts)
        self.assertEqual([result.returncode for result in results], [0, 0], [result.stderr for result in results])
        self.assertEqual(set(self._read(self.unrelated)["records"]), {"arXiv:2609.90005"})
        self.assertEqual(set(self._read(self.borderline)["records"]), {"arXiv:2609.90005"})
        self.assertEqual(len(self._read(self.result_dir / "clear-a.json")["removed_rows"]), 2)
        self.assertEqual(len(self._read(self.result_dir / "clear-b.json")["removed_rows"]), 2)

    def test_concurrent_identical_request_preserves_first_immutable_result(self) -> None:
        self._write_ledger(self.unrelated, "unrelated", {self.canonical: {"classification": "unrelated", "canonical_id": self.canonical, "identity_tokens": [self.canonical, self.alias], "reason": "old"}})
        self._write_ledger(self.borderline, "borderline", {self.canonical: {"classification": "borderline", "canonical_id": self.canonical, "identity_tokens": [self.canonical, self.alias], "reason": "old"}})
        self._request("clear-identical")
        script = """
            import sys, time
            from pathlib import Path
            root, gate, scripts = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
            sys.path.insert(0, str(scripts))
            import process_reference_relevance_requests as processor
            while not gate.exists(): time.sleep(0.01)
            processor.process_request(root, root / '.survey/work-queue/reference-curation/requests/clear-identical.json')
        """
        results = self._run_concurrent([script, script])
        self.assertEqual([result.returncode for result in results], [0, 0], [result.stderr for result in results])
        result_path = self.result_dir / "clear-identical.json"
        result_bytes = result_path.read_bytes()
        result = self._read(result_path)
        self.assertEqual(len(result["removed_rows"]), 2)
        self.assertFalse((self.root / ".survey/work-queue/reference-curation/clear-transactions/clear-identical.json").exists())
        processor.process_request(self.root, self.request_dir / "clear-identical.json")
        self.assertEqual(result_path.read_bytes(), result_bytes)

    def test_result_written_before_crash_finalizes_journal_on_idempotent_retry(self) -> None:
        self._write_ledger(self.unrelated, "unrelated", {self.canonical: {"classification": "unrelated", "canonical_id": self.canonical, "identity_tokens": [self.canonical], "reason": "old"}})
        self._write_ledger(self.borderline, "borderline", {})
        request = self._request("clear-result-crash")
        original_write = processor._write_json

        def write_then_interrupt(path: Path, payload: dict[str, object]) -> None:
            original_write(path, payload)
            if path == self.result_dir / "clear-result-crash.json":
                raise SystemExit("synthetic interruption after durable result")

        with mock.patch.object(processor, "_write_json", side_effect=write_then_interrupt):
            with self.assertRaises(SystemExit):
                processor.process_request(self.root, request)
        result_path = self.result_dir / "clear-result-crash.json"
        journal = self.root / ".survey/work-queue/reference-curation/clear-transactions/clear-result-crash.json"
        self.assertTrue(result_path.exists())
        self.assertTrue(journal.exists())
        result_bytes = result_path.read_bytes()

        retry = processor.process_request(self.root, request)

        self.assertEqual(retry["status"], "already_processed")
        self.assertEqual(result_path.read_bytes(), result_bytes)
        self.assertFalse(journal.exists())

    def test_partial_two_ledger_write_rolls_back_both_exact_bytes(self) -> None:
        before_unrelated = self._write_ledger(self.unrelated, "unrelated", {self.canonical: {"classification": "unrelated", "canonical_id": self.canonical, "identity_tokens": [self.canonical], "reason": "old"}})
        before_borderline = self._write_ledger(self.borderline, "borderline", {self.canonical: {"classification": "borderline", "canonical_id": self.canonical, "identity_tokens": [self.canonical], "reason": "old"}})
        self._request("clear-rollback")
        original = ledger._atomic_write_bytes
        writes = 0

        def fail_second_write(path: Path, data: bytes) -> None:
            nonlocal writes
            writes += 1
            if writes == 2:
                raise OSError("synthetic second-ledger failure")
            original(path, data)

        with mock.patch.object(ledger, "_atomic_write_bytes", side_effect=fail_second_write):
            summary = processor.process_pending(self.root)

        self.assertFalse(summary["ok"])
        self.assertEqual(summary["retryable_error_count"], 1)
        self.assertEqual(self.unrelated.read_bytes(), before_unrelated)
        self.assertEqual(self.borderline.read_bytes(), before_borderline)
        self.assertTrue((self.request_dir / "clear-rollback.json").exists())
        self.assertFalse((self.result_dir / "clear-rollback.json").exists())

    def test_orphaned_clear_journal_restores_partial_write_before_retry(self) -> None:
        before_unrelated = self._write_ledger(self.unrelated, "unrelated", {self.canonical: {"classification": "unrelated", "canonical_id": self.canonical, "identity_tokens": [self.canonical], "reason": "old"}})
        before_borderline = self._write_ledger(self.borderline, "borderline", {self.canonical: {"classification": "borderline", "canonical_id": self.canonical, "identity_tokens": [self.canonical], "reason": "old"}})
        request = self._request("clear-crash-recovery")
        original = ledger._atomic_write_bytes
        ledger_writes = 0

        def fail_like_process_crash(path: Path, data: bytes) -> None:
            nonlocal ledger_writes
            if path in (self.unrelated, self.borderline):
                ledger_writes += 1
                if ledger_writes == 2:
                    raise SystemExit("synthetic process interruption")
            original(path, data)

        with mock.patch.object(ledger, "_atomic_write_bytes", side_effect=fail_like_process_crash):
            with self.assertRaises(SystemExit):
                processor.process_request(self.root, request)

        journal = self.root / ".survey/work-queue/reference-curation/clear-transactions/clear-crash-recovery.json"
        self.assertTrue(journal.exists())
        self.assertTrue(request.exists())
        self.assertFalse((self.result_dir / "clear-crash-recovery.json").exists())

        original_request = request.read_bytes()
        tampered = json.loads(original_request.decode("utf-8"))
        tampered["reason"] = "A changed request must not reuse the interrupted transaction."
        request.write_text(json.dumps(tampered), encoding="utf-8")
        partial_unrelated = self.unrelated.read_bytes()
        partial_borderline = self.borderline.read_bytes()
        tampered_summary = processor.process_pending(self.root)
        self.assertFalse(tampered_summary["ok"])
        self.assertEqual(tampered_summary["retryable_error_count"], 1)
        self.assertEqual(self.unrelated.read_bytes(), partial_unrelated)
        self.assertEqual(self.borderline.read_bytes(), partial_borderline)
        self.assertTrue(journal.exists())
        request.write_bytes(original_request)

        summary = processor.process_pending(self.root)

        self.assertTrue(summary["ok"])
        self.assertEqual(summary["processed_count"], 1)
        self.assertNotIn(self.canonical, self._read(self.unrelated)["records"])
        self.assertNotIn(self.canonical, self._read(self.borderline)["records"])
        self.assertTrue((self.result_dir / "clear-crash-recovery.json").exists())
        self.assertFalse(journal.exists())
        self.assertNotEqual(self.unrelated.read_bytes(), before_unrelated)
        self.assertNotEqual(self.borderline.read_bytes(), before_borderline)

    def test_clear_rejects_invalid_schema_and_unknown_operation(self) -> None:
        self._request("clear-bad-schema", schema_version=2)
        self._request("clear-bad-operation", operation="erase-ledgers")
        summary = processor.process_pending(self.root)
        self.assertEqual(summary["invalid_request_count"], 2)
        self.assertFalse(self._read(self.result_dir / "clear-bad-schema.json")["ok"])
        self.assertFalse(self._read(self.result_dir / "clear-bad-operation.json")["ok"])

    def test_existing_mark_operations_remain_supported(self) -> None:
        self._request("mark-unrelated-regression", operation="mark_unrelated", root_review_proof=None)
        summary = processor.process_pending(self.root)
        self.assertTrue(summary["ok"])
        self.assertEqual(summary["processed_count"], 1)
        self.assertIn(self.canonical, self._read(self.unrelated)["records"])
        result = self._read(self.result_dir / "mark-unrelated-regression.json")
        self.assertEqual(result["classification"], "unrelated")
        self.assertEqual(result["request_operation"], "mark_unrelated")


if __name__ == "__main__":
    unittest.main()
