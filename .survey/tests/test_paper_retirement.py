from __future__ import annotations

import json
import hashlib
import subprocess
import threading
from unittest.mock import patch
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import resolve_paper_identity  # noqa: E402
import paper_retirement_registry  # noqa: E402
import represented_paper_index  # noqa: E402
import research_job_reconciliation  # noqa: E402
import paper_retirement  # noqa: E402
import library_ack_manifest  # noqa: E402


class PaperRetirementResolverTests(unittest.TestCase):
    def _synthetic_repo(self, root: Path, *, cross_delta: bool = False, exact_delta: bool = False, reference_link: bool = False) -> tuple[Path, Path]:
        paper = root / "papers/inference/test/2026-2609.99993-retired.md"
        paper.parent.mkdir(parents=True)
        paper.write_bytes(
            b'---\ncanonical_id: "arXiv:2609.99993"\narxiv_id: "2609.99993"\ntitle: "Retired test"\n---\n\n# Retired test\n'
        )
        if cross_delta:
            owner = root / "papers/inference/test/owner.md"
            owner.write_bytes(b'---\ncanonical_id: "arXiv:2609.99994"\ndoi: "10.1000/owner"\ntitle: "Owner"\n---\n\n# Owner\n')
            delta = root / ".survey/survey-state/identity-deltas/arxiv/2609.99993.json"
            delta.parent.mkdir(parents=True)
            delta.write_text(json.dumps({
                "canonical_id": "arXiv:2609.99993", "path": "papers/inference/test/2026-2609.99993-retired.md",
                "identifiers": ["arXiv:2609.99993", "DOI:10.1000/owner"],
            }), encoding="utf-8")
        if exact_delta:
            delta = root / ".survey/survey-state/identity-deltas/arxiv/2609.99993.json"
            delta.parent.mkdir(parents=True, exist_ok=True)
            delta.write_text(json.dumps({
                "canonical_id": "arXiv:2609.99993", "path": "papers/inference/test/2026-2609.99993-retired.md",
                "identifiers": ["arXiv:2609.99993"],
            }, indent=2) + "\n", encoding="utf-8")
        if reference_link:
            readme = root / "papers/inference/test/README.md"
            readme.write_text("[retired paper][retired]\n\n[retired]: ./2026-2609.99993-retired.md\n", encoding="utf-8")
        index = root / ".survey/survey-state/paper-identity-index.json"
        index.parent.mkdir(parents=True, exist_ok=True)
        index.write_text('{"schema_version":3,"papers":{},"identifier_to_canonical":{}}\n', encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Synthetic Test"], cwd=root, check=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "synthetic paper"], cwd=root, check=True)
        return paper, root / ".survey/survey-state/paper-retirements.json"

    def test_verified_alias_resolves_to_retirement_without_active_paper_path(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            registry_path = root / ".survey/survey-state/paper-retirements.json"
            registry_path.parent.mkdir(parents=True)
            registry_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "records": {
                            "arXiv:2609.99993": {
                                "retirement_id": "ret-7b3e",
                                "canonical_id": "arXiv:2609.99993",
                                "verified_aliases": [
                                    "arXiv:2609.99993",
                                    "DOI:10.1000/retired-paper",
                                ],
                                "original_path": "papers/inference/test/retired-paper.md",
                                "source_sha256": "a" * 64,
                                "source_git_blob_sha": "b" * 40,
                                "source_commit": "c" * 40,
                                "classification": "unrelated",
                                "reason": "Outside inference systems scope.",
                                "evidence": "Independent primary-text review",
                                "relevance_request_id": "retire-7b3e-unrelated",
                                "relevance_result_id": "retire-7b3e-unrelated",
                            }
                        },
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            resolved = resolve_paper_identity.resolve(
                root,
                {"doi": "10.1000/retired-paper"},
            )

            self.assertEqual(resolved["status"], "retired")
            self.assertEqual(resolved["canonical_id"], "arXiv:2609.99993")
            self.assertEqual(resolved["retirement_id"], "ret-7b3e")
            self.assertEqual(resolved["retired_path"], "papers/inference/test/retired-paper.md")
            self.assertIsNone(resolved["paper_path"])

    def test_missing_registry_preserves_normal_not_found_behavior(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            resolved = resolve_paper_identity.resolve(Path(td), {"doi": "10.1000/ordinary"})
            self.assertEqual(resolved["status"], "not_found")
            self.assertIsNone(resolved["paper_path"])

    def test_conflicting_registry_alias_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / ".survey/survey-state/paper-retirements.json"
            path.parent.mkdir(parents=True)
            record = {
                "retirement_id": "ret-one", "canonical_id": "arXiv:2609.99991",
                "verified_aliases": ["arXiv:2609.99991", "DOI:10.1000/shared"],
                "original_path": "papers/inference/test/a.md", "classification": "unrelated",
                "source_sha256": "a" * 64, "source_git_blob_sha": "b" * 40, "source_commit": "c" * 40,
                "reason": "unrelated", "evidence": "source review",
                "relevance_request_id": "req-one", "relevance_result_id": "req-one",
            }
            conflicting = dict(record, retirement_id="ret-two", canonical_id="arXiv:2609.99992")
            conflicting["verified_aliases"] = ["arXiv:2609.99992", "DOI:10.1000/shared"]
            path.write_text(json.dumps({"schema_version": 1, "records": {record["canonical_id"]: record, conflicting["canonical_id"]: conflicting}}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "conflicting retired identity alias"):
                paper_retirement_registry.load_registry(root)

    def test_retired_alias_is_in_duplicate_prevention_records(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            state = root / ".survey/survey-state/paper-retirements.json"
            state.parent.mkdir(parents=True)
            state.write_text(json.dumps({"schema_version": 1, "records": {"arXiv:2609.99993": {
                "retirement_id": "ret-7b3e", "canonical_id": "arXiv:2609.99993",
                "verified_aliases": ["arXiv:2609.99993", "DOI:10.1000/retired-paper"],
                "original_path": "papers/inference/test/retired-paper.md", "classification": "unrelated",
                "source_sha256": "a" * 64, "source_git_blob_sha": "b" * 40, "source_commit": "c" * 40,
                "reason": "unrelated", "evidence": "source review",
                "relevance_request_id": "req-ret", "relevance_result_id": "req-ret",
            }}}), encoding="utf-8")
            records = represented_paper_index.collect_represented_records(root)
            self.assertTrue(any(row.get("retirement_id") == "ret-7b3e" for row in records))

    def test_ready_research_job_matching_retired_alias_is_superseded(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            state = root / ".survey/survey-state/paper-retirements.json"
            state.parent.mkdir(parents=True)
            state.write_text(json.dumps({"schema_version": 1, "records": {"arXiv:2609.99993": {
                "retirement_id": "ret-7b3e", "canonical_id": "arXiv:2609.99993",
                "verified_aliases": ["arXiv:2609.99993", "DOI:10.1000/retired-paper"],
                "original_path": "papers/inference/test/retired-paper.md", "classification": "unrelated",
                "source_sha256": "a" * 64, "source_git_blob_sha": "b" * 40, "source_commit": "c" * 40,
                "reason": "unrelated", "evidence": "source review",
                "relevance_request_id": "req-ret", "relevance_result_id": "req-ret",
            }}}), encoding="utf-8")
            job = {"type": "research", "status": "ready", "doi": "10.1000/retired-paper"}
            index = research_job_reconciliation.build_paper_index(root)
            self.assertEqual(research_job_reconciliation.effective_status(job, index), "superseded")
            matched = research_job_reconciliation.match_represented_research_job(job, index)
            self.assertEqual(matched["identity_disposition"], "retired")

    def test_dry_run_is_read_only_and_apply_can_restore_synthetic_source(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            root = base / "repo"
            root.mkdir()
            paper, registry_path = self._synthetic_repo(root)
            content = paper.read_bytes()
            commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True).stdout.strip()
            blob = subprocess.run(["git", "rev-parse", f"HEAD:{paper.relative_to(root).as_posix()}"], cwd=root, check=True, capture_output=True, text=True).stdout.strip()
            manifest = base / "manifest.json"
            manifest.write_text(json.dumps({
                "schema_version": 1, "transaction_id": "synthetic-retire-1", "source_commit": commit,
                "entries": [{
                    "path": paper.relative_to(root).as_posix(), "canonical_id": "arXiv:2609.99993",
                    "verified_aliases": ["arXiv:2609.99993"], "source_sha256": hashlib.sha256(content).hexdigest(),
                    "source_git_blob_sha": blob, "retirement_id": "ret-synthetic-1", "classification": "unrelated",
                    "reason": "Synthetic unrelated test", "evidence": "Synthetic fixture only",
                }],
            }), encoding="utf-8")
            before_status = subprocess.run(["git", "status", "--porcelain"], cwd=root, check=True, capture_output=True, text=True).stdout
            plan = paper_retirement.preflight(root, manifest)
            self.assertEqual(plan["entry_count"], 1)
            self.assertEqual(before_status, subprocess.run(["git", "status", "--porcelain"], cwd=root, check=True, capture_output=True, text=True).stdout)
            self.assertFalse(registry_path.exists())
            applied = paper_retirement.apply(root, manifest)
            self.assertTrue(applied["ok"])
            self.assertFalse(paper.exists())
            self.assertTrue(registry_path.exists())
            repeated = paper_retirement.apply(root, manifest)
            self.assertTrue(repeated["already_applied"])
            restored = paper_retirement.recover(root, "synthetic-retire-1", "restore")
            self.assertEqual(restored["phase"], "rolled_back")
            self.assertEqual(paper.read_bytes(), content)
            self.assertFalse(registry_path.exists())

    def test_exact_retirement_proof_uses_existing_superseded_ack_section(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper_path = "papers/inference/test/retired.md"
            source_file = root / paper_path
            source_file.parent.mkdir(parents=True, exist_ok=True)
            source_bytes = b"# exact pinned retired source\n"
            source_file.write_bytes(source_bytes)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Synthetic Test"], cwd=root, check=True)
            subprocess.run(["git", "add", "papers"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "retired source"], cwd=root, check=True)
            source_commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True).stdout.strip()
            source_blob = subprocess.run(["git", "rev-parse", f"HEAD:{paper_path}"], cwd=root, check=True, capture_output=True, text=True).stdout.strip()
            source_file.unlink()
            job_id, attempt_id, envelope_id = "job-retired", "attempt-retired", "env-retired"
            submission = f".survey/work-queue/submissions/research/{attempt_id}.json"
            self._write_json(root, f".survey/work-queue/fallback-archive/{envelope_id}.json", {
                "schema_version": 1, "id": envelope_id, "kind": "research", "job_id": job_id,
                "attempt_id": attempt_id, "paper_path": paper_path, "canonical_id": "arXiv:2609.99993",
            })
            self._write_json(root, submission, {
                "schema_version": 1, "transport_version": 10, "kind": "research", "job_id": job_id,
                "attempt_id": attempt_id, "paper_path": paper_path, "canonical_id": "arXiv:2609.99993",
            })
            self._write_json(root, f".survey/work-queue/results/research/{attempt_id}.json", {
                "schema_version": 1, "workflow_version": 10, "ok": True, "job_id": job_id,
                "attempt_id": attempt_id, "job_type": "research", "job_status": "completed",
                "artifact": {"paper": paper_path}, "submission": submission,
            })
            self._write_json(root, f".survey/work-queue/jobs/{job_id}.json", {
                "job_id": job_id, "type": "research", "status": "completed", "paper_path": paper_path,
                "canonical_id": "arXiv:2609.99993", "artifact_submission": submission,
            })
            self._write_json(root, ".survey/survey-state/paper-retirements.json", {
                "schema_version": 1, "records": {"arXiv:2609.99993": {
                    "retirement_id": "ret-ack-1", "canonical_id": "arXiv:2609.99993",
                    "verified_aliases": ["arXiv:2609.99993"], "original_path": paper_path,
                    "source_sha256": hashlib.sha256(source_bytes).hexdigest(), "source_git_blob_sha": source_blob,
                    "source_commit": source_commit, "classification": "unrelated", "reason": "unrelated",
                    "evidence": "primary source review", "relevance_request_id": "req-ack-1",
                    "relevance_result_id": "req-ack-1",
                }},
            })
            manifest = library_ack_manifest.build_manifest(root)
            self.assertEqual(manifest["acknowledgements"], [])
            self.assertEqual(manifest["waiting"], [])
            self.assertEqual(len(manifest["superseded"]), 1)
            row = manifest["superseded"][0]
            self.assertEqual(row["reason"], "paper_retired")
            self.assertEqual(row["retirement_id"], "ret-ack-1")
            self.assertEqual(row["paper_path"], paper_path)
            registry = json.loads((root / ".survey/survey-state/paper-retirements.json").read_text(encoding="utf-8"))
            registry["records"]["arXiv:2609.99993"]["source_sha256"] = "0" * 64
            self._write_json(root, ".survey/survey-state/paper-retirements.json", registry)
            invalid = library_ack_manifest.build_manifest(root)
            self.assertEqual(invalid["superseded"], [])
            self.assertEqual(invalid["waiting"][0]["reason"], "paper_missing")

    def test_foreign_alias_delta_rejects_before_any_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            root = base / "repo"
            root.mkdir()
            paper, registry = self._synthetic_repo(root, cross_delta=True)
            original_delta = root / ".survey/survey-state/identity-deltas/arxiv/2609.99993.json"
            before = original_delta.read_bytes()
            manifest = self._manifest(root, base, paper)
            with self.assertRaisesRegex(ValueError, "delta.*alias|alias.*delta"):
                paper_retirement.apply(root, manifest)
            self.assertTrue(paper.exists())
            self.assertFalse(registry.exists())
            self.assertEqual(original_delta.read_bytes(), before)
            self.assertFalse((root / ".survey/work-queue/reference-curation/requests").exists())

    def test_reference_style_link_blocks_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            root = base / "repo"
            root.mkdir()
            paper, _ = self._synthetic_repo(root, reference_link=True)
            manifest = self._manifest(root, base, paper)
            with self.assertRaisesRegex(ValueError, "inbound local markdown link"):
                paper_retirement.preflight(root, manifest)
            self.assertTrue(paper.exists())

    def test_recovery_rejects_tampered_prior_registry_without_changes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            root = base / "repo"
            root.mkdir()
            paper, registry_path = self._synthetic_repo(root)
            manifest = self._manifest(root, base, paper)
            paper_retirement.apply(root, manifest)
            journal_path = root / ".survey/survey-state/paper-retirement-journals/synthetic-retire-1.json"
            journal = json.loads(journal_path.read_text(encoding="utf-8"))
            journal["prior_registry"] = {"schema_version": 999, "records": {}}
            journal_path.write_text(json.dumps(journal), encoding="utf-8")
            registry_before = registry_path.read_bytes()
            with self.assertRaises(ValueError):
                paper_retirement.recover(root, "synthetic-retire-1", "restore")
            self.assertFalse(paper.exists())
            self.assertEqual(registry_path.read_bytes(), registry_before)

    def test_recovery_rejects_delta_traversal_before_any_restore_write(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            root = base / "repo"
            root.mkdir()
            paper, _ = self._synthetic_repo(root)
            manifest = self._manifest(root, base, paper)
            paper_retirement.apply(root, manifest)
            journal_path = root / ".survey/survey-state/paper-retirement-journals/synthetic-retire-1.json"
            journal = json.loads(journal_path.read_text(encoding="utf-8"))
            journal["prior_deltas"] = [{"path": "../../escaped.json", "record": {"canonical_id": "arXiv:2609.99993", "path": "papers/x.md", "identifiers": []}}]
            journal_path.write_text(json.dumps(journal), encoding="utf-8")
            escaped = base / "escaped.json"
            with self.assertRaises(ValueError):
                paper_retirement.recover(root, "synthetic-retire-1", "restore")
            self.assertFalse(escaped.exists())
            self.assertFalse(paper.exists())

    def test_recovery_rejects_symlink_parent_before_restore(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            root = base / "repo"
            root.mkdir()
            paper, _ = self._synthetic_repo(root)
            manifest = self._manifest(root, base, paper)
            paper_retirement.apply(root, manifest)
            paper.parent.rmdir()
            outside = base / "outside"
            outside.mkdir()
            try:
                paper.parent.symlink_to(outside, target_is_directory=True)
            except OSError:
                junction = subprocess.run(
                    ["powershell", "-NoProfile", "-Command", "New-Item -ItemType Junction -Path $args[0] -Target $args[1] | Out-Null", str(paper.parent), str(outside)],
                    capture_output=True,
                    text=True,
                )
                if junction.returncode != 0:
                    self.skipTest("symlink/junction creation unavailable in this Windows environment")
            with self.assertRaisesRegex(ValueError, "symlink|escapes"):
                paper_retirement.recover(root, "synthetic-retire-1", "restore")
            self.assertFalse((outside / paper.name).exists())
            self.assertFalse(paper.exists())

    def test_recovery_junction_guard_rejects_redirected_parent_before_write(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            root = base / "repo"
            root.mkdir()
            paper, registry_path = self._synthetic_repo(root)
            manifest = self._manifest(root, base, paper)
            paper_retirement.apply(root, manifest)
            registry_before = registry_path.read_bytes()
            outside = base / "outside"
            outside.mkdir()
            actual_is_link = paper_retirement._is_link

            def simulated_junction(path: Path) -> bool:
                return path == paper.parent or actual_is_link(path)

            with patch.object(paper_retirement, "_is_link", side_effect=simulated_junction):
                with self.assertRaisesRegex(ValueError, "symlink ancestry"):
                    paper_retirement.recover(root, "synthetic-retire-1", "restore")
            self.assertFalse(paper.exists())
            self.assertEqual(registry_path.read_bytes(), registry_before)
            self.assertFalse((outside / paper.name).exists())

    def test_apply_serializes_competing_transactions_before_side_effects(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            root = base / "repo"
            root.mkdir()
            paper, registry = self._synthetic_repo(root)
            first_manifest = self._manifest(root, base, paper)
            second_data = json.loads(first_manifest.read_text(encoding="utf-8"))
            second_data["transaction_id"] = "synthetic-retire-2"
            second_manifest = base / "manifest-second.json"
            second_manifest.write_text(json.dumps(second_data), encoding="utf-8")
            first_entered = threading.Event()
            second_refused = threading.Event()
            outcomes: list[Any] = []

            def checkpoint(phase: str) -> None:
                if phase == "prepared" and threading.current_thread().name == "retirement-first":
                    first_entered.set()
                    if not second_refused.wait(5):
                        raise RuntimeError("second contender did not reach lock")

            def first() -> None:
                try:
                    outcomes.append(paper_retirement.apply(root, first_manifest))
                except Exception as exc:
                    outcomes.append(exc)

            def second() -> None:
                if not first_entered.wait(5):
                    outcomes.append(AssertionError("first transaction did not reach prepared phase"))
                    second_refused.set()
                    return
                try:
                    paper_retirement.apply(root, second_manifest)
                    outcomes.append(AssertionError("competing transaction unexpectedly proceeded"))
                except ValueError as exc:
                    outcomes.append(exc)
                finally:
                    second_refused.set()

            with patch.object(paper_retirement, "_phase_checkpoint", side_effect=checkpoint):
                t1 = threading.Thread(target=first, name="retirement-first")
                t2 = threading.Thread(target=second, name="retirement-second")
                t1.start()
                t2.start()
                t1.join(10)
                t2.join(10)
            self.assertFalse(t1.is_alive() or t2.is_alive())
            self.assertEqual(len(outcomes), 2)
            self.assertTrue(any(isinstance(value, ValueError) and "transaction is active" in str(value) for value in outcomes))
            self.assertTrue(any(isinstance(value, dict) and value.get("phase") == "complete" for value in outcomes))
            self.assertFalse(paper.exists())
            self.assertTrue(registry.exists())
            self.assertFalse((root / ".survey/survey-state/paper-retirement-journals/synthetic-retire-2.json").exists())

    def test_recover_restores_exact_bytes_after_each_durable_apply_phase(self) -> None:
        phases = ("prepared", "requests_written", "registry_written", "papers_deleted", "index_rebuilt")
        for phase in phases:
            with self.subTest(phase=phase), tempfile.TemporaryDirectory() as td:
                base = Path(td)
                root = base / "repo"
                root.mkdir()
                paper, registry_path = self._synthetic_repo(root)
                source_bytes = paper.read_bytes()
                manifest = self._manifest(root, base, paper)

                def failpoint(current: str) -> None:
                    if current == phase:
                        raise RuntimeError("synthetic crash after durable phase")

                with patch.object(paper_retirement, "_phase_checkpoint", side_effect=failpoint):
                    with self.assertRaisesRegex(RuntimeError, "synthetic crash"):
                        paper_retirement.apply(root, manifest)
                recovered = paper_retirement.recover(root, "synthetic-retire-1", "restore")
                self.assertEqual(recovered["phase"], "rolled_back")
                self.assertEqual(paper.read_bytes(), source_bytes)
                self.assertFalse(registry_path.exists())

    def test_exactly_owned_delta_is_removed_and_restored(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            root = base / "repo"
            root.mkdir()
            paper, _ = self._synthetic_repo(root, exact_delta=True)
            delta = root / ".survey/survey-state/identity-deltas/arxiv/2609.99993.json"
            delta_bytes = delta.read_bytes()
            index = root / ".survey/survey-state/paper-identity-index.json"
            index_bytes = index.read_bytes()
            manifest = self._manifest(root, base, paper)
            paper_retirement.apply(root, manifest)
            self.assertFalse(delta.exists())
            self.assertFalse(paper.exists())
            self.assertNotEqual(index.read_bytes(), index_bytes)
            paper_retirement.recover(root, "synthetic-retire-1", "restore")
            self.assertEqual(delta.read_bytes(), delta_bytes)
            self.assertEqual(index.read_bytes(), index_bytes)
            self.assertTrue(paper.exists())

    def test_failpoint_after_exact_delta_deletion_restores_it(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            root = base / "repo"
            root.mkdir()
            paper, _ = self._synthetic_repo(root, exact_delta=True)
            delta = root / ".survey/survey-state/identity-deltas/arxiv/2609.99993.json"
            original_delta = delta.read_bytes()
            manifest = self._manifest(root, base, paper)
            with patch.object(paper_retirement, "_phase_checkpoint", side_effect=lambda phase: (_ for _ in ()).throw(RuntimeError("synthetic delta crash")) if phase.startswith("delta_deleted:") else None):
                with self.assertRaisesRegex(RuntimeError, "synthetic delta crash"):
                    paper_retirement.apply(root, manifest)
            paper_retirement.recover(root, "synthetic-retire-1", "restore")
            self.assertEqual(delta.read_bytes(), original_delta)
            self.assertTrue(paper.exists())

    def _manifest(self, root: Path, base: Path, paper: Path) -> Path:
        content = paper.read_bytes()
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True).stdout.strip()
        blob = subprocess.run(["git", "rev-parse", f"HEAD:{paper.relative_to(root).as_posix()}"], cwd=root, check=True, capture_output=True, text=True).stdout.strip()
        value = {
            "schema_version": 1, "transaction_id": "synthetic-retire-1", "source_commit": commit,
            "entries": [{
                "path": paper.relative_to(root).as_posix(), "canonical_id": "arXiv:2609.99993",
                "verified_aliases": ["arXiv:2609.99993"], "source_sha256": hashlib.sha256(content).hexdigest(),
                "source_git_blob_sha": blob, "retirement_id": "ret-synthetic-1", "classification": "unrelated",
                "reason": "Synthetic unrelated test", "evidence": "Synthetic fixture only",
            }],
        }
        path = base / "manifest.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def _write_json(self, root: Path, relative: str, value: dict) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
