import hashlib
import inspect
import io
import json
import re
import sys
import tempfile
import unittest
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import identity_delta  # noqa: E402
import paper_lineage_migration as migration  # noqa: E402
import survey  # noqa: E402


SOURCE_MAIN = "b74bf705735f43dd362706621ff9f6cc61bdc538"
DURABLE_PHASES = (
    "prepared", "target-installed:0", "target-installed:1", "targets-installed",
    "old-stubbed:0", "old-stubbed:1", "snapshot-replaced", "complete",
)
CID = "arXiv:2401.00001"
OLD = "papers/inference/old/paper.md"
NEW = "papers/inference/new/paper.md"
RAW = b"---\ncanonical_id: arXiv:2401.00001\narxiv_id: 2401.00001\ndoi: 10.1000/sample\ntitle: Sample\n---\nBody bytes stay exact.\n"


def world(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    (root / OLD).parent.mkdir(parents=True)
    (root / NEW).parent.mkdir(parents=True)
    (root / OLD).write_bytes(RAW)
    state = root / "survey-state"
    state.mkdir()
    survey.ROOT = root
    identity_delta.ROOT = root
    monkeypatch.setattr(migration, "current_worktree_sha", lambda: SOURCE_MAIN)
    monkeypatch.setattr(migration, "_after_phase", lambda _phase: None)
    aliases = [CID, "DOI:10.1000/sample"]
    snapshot = {
        "schema_version": 3,
        "active_count": 1,
        "papers": {CID: {"path": OLD, "identifiers": aliases, "source_hash": hashlib.sha256(RAW).hexdigest()}},
        "identifier_to_canonical": {alias: CID for alias in aliases},
        "ignored_moved_stubs": [],
    }
    index = state / "paper-identity-index.json"
    index.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "source_main_sha": SOURCE_MAIN,
        "entries": [{
            "old_path": OLD,
            "new_path": NEW,
            "canonical_id": CID,
            "aliases": aliases,
            "expected_sha256": hashlib.sha256(RAW).hexdigest(),
        }],
    }
    manifest_path = root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return root, manifest, manifest_path, index


def cli(args, capsys):
    stdout, stderr = io.StringIO(), io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        code = migration.main(args)
    return code, stdout.getvalue(), stderr.getvalue()


@contextmanager
def raises(expected, match=None):
    try:
        yield
    except expected as exc:
        if match and not re.search(match, str(exc)):
            raise AssertionError(f"{str(exc)!r} does not match {match!r}") from exc
    else:
        raise AssertionError(f"expected {expected.__name__} to be raised")


class MonkeyPatch:
    def __init__(self):
        self._changes = []

    def setattr(self, target, name, value):
        self._changes.append((target, name, getattr(target, name)))
        setattr(target, name, value)

    def undo(self):
        for target, name, old_value in reversed(self._changes):
            setattr(target, name, old_value)
        self._changes.clear()


def add_second_entry(root, manifest, manifest_path, index):
    old2, new2 = "papers/training/old/second.md", "papers/training/new/second.md"
    (root / old2).parent.mkdir(parents=True); (root / new2).parent.mkdir(parents=True)
    raw2 = RAW.replace(b"2401.00001", b"2401.00002").replace(b"10.1000/sample", b"10.1000/second")
    cid2 = "arXiv:2401.00002"
    (root / old2).write_bytes(raw2)
    snapshot = json.loads(index.read_text(encoding="utf-8"))
    aliases2 = sorted([cid2, "DOI:10.1000/second"])
    snapshot["papers"][cid2] = {"path": old2, "identifiers": aliases2, "source_hash": hashlib.sha256(raw2).hexdigest()}
    snapshot["identifier_to_canonical"].update({alias: cid2 for alias in aliases2})
    snapshot["active_count"] = 2
    index.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    manifest["entries"].append({"old_path": old2, "new_path": new2, "canonical_id": cid2,
        "aliases": aliases2, "expected_sha256": hashlib.sha256(raw2).hexdigest()})
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return old2, new2, raw2, cid2


def batch_world(tmp_path, monkeypatch, count, *, extra_body_bytes=0):
    root = tmp_path / "batch-repo"
    state = root / "survey-state"
    state.mkdir(parents=True)
    survey.ROOT = root
    identity_delta.ROOT = root
    monkeypatch.setattr(migration, "current_worktree_sha", lambda: SOURCE_MAIN)
    monkeypatch.setattr(migration, "_after_phase", lambda _phase: None)
    papers = {}
    identifier_to_canonical = {}
    entries = []
    original_bytes = {}
    for index in range(count):
        suffix = f"{index:03d}"
        arxiv = f"2401.{index + 1:05d}"
        cid = f"arXiv:{arxiv}"
        doi = f"DOI:10.1000/migration-{suffix}"
        aliases = sorted([cid, doi])
        old_path = f"papers/inference/old/{suffix}-paper.md"
        new_path = f"papers/inference/new/{suffix}-paper.md"
        raw = (
            f"---\ncanonical_id: {cid}\narxiv_id: '{arxiv}'\n"
            f"doi: 10.1000/migration-{suffix}\ntitle: Synthetic {suffix}\n---\n"
            "Synthetic body bytes stay exact.\n"
        ).encode("utf-8")
        if extra_body_bytes:
            raw += b"x" * extra_body_bytes
        old_file = root / old_path
        old_file.parent.mkdir(parents=True, exist_ok=True)
        (root / new_path).parent.mkdir(parents=True, exist_ok=True)
        old_file.write_bytes(raw)
        source_hash = hashlib.sha256(raw).hexdigest()
        original_bytes[old_path] = raw
        papers[cid] = {"path": old_path, "identifiers": aliases, "source_hash": source_hash}
        identifier_to_canonical.update({alias: cid for alias in aliases})
        entries.append({"old_path": old_path, "new_path": new_path, "canonical_id": cid,
                        "aliases": aliases, "expected_sha256": source_hash})
    snapshot = {"schema_version": 3, "active_count": count, "papers": papers,
                "identifier_to_canonical": identifier_to_canonical, "ignored_moved_stubs": []}
    index = state / "paper-identity-index.json"
    index.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    manifest_path = root / "batch-manifest.json"
    manifest_path.write_text(json.dumps({"source_main_sha": SOURCE_MAIN, "entries": entries}, indent=2),
                             encoding="utf-8")
    return root, manifest_path, index, original_bytes


def test_dry_run_is_read_only(world, capsys):
    root, _manifest, manifest_path, index = world
    before = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}
    code, out, _ = cli(["dry-run", "--manifest", str(manifest_path)], capsys)
    after = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}
    assert code == 0
    assert json.loads(out)["valid"] is True
    assert before == after
    assert index.exists()


def test_valid_apply_preserves_bytes_stub_and_alias_lookup(world, capsys):
    root, _manifest, manifest_path, index = world
    code, out, _ = cli(["apply", "--manifest", str(manifest_path)], capsys)
    result = json.loads(out)
    assert code == 0
    assert (root / NEW).read_bytes() == RAW
    stub = (root / OLD).read_text(encoding="utf-8")
    assert next(line for line in stub.splitlines() if line.strip()) == "# Moved"
    assert not stub.startswith("---")
    snapshot = json.loads(index.read_text(encoding="utf-8"))
    assert OLD.split("/", 2)[-1] in snapshot["ignored_moved_stubs"]
    assert snapshot["papers"][CID]["path"] == NEW
    assert snapshot["papers"][CID]["source_hash"] == hashlib.sha256(RAW).hexdigest()
    assert identity_delta.logical_lookup("DOI:10.1000/sample")[0] == CID
    assert result["transaction_id"]


def test_stale_hash_id_snapshot_and_alias_fail_closed(world, mutation, expected, capsys):
    root, manifest, manifest_path, index = world
    if mutation == "pin":
        manifest["source_main_sha"] = "0" * 40
    elif mutation == "hash":
        manifest["entries"][0]["expected_sha256"] = "0" * 64
    elif mutation == "id":
        manifest["entries"][0]["canonical_id"] = "arXiv:2401.00002"
    elif mutation == "snapshot":
        data = json.loads(index.read_text(encoding="utf-8")); data["papers"][CID]["path"] = NEW
        index.write_text(json.dumps(data), encoding="utf-8")
    else:
        manifest["entries"][0]["aliases"] = [CID]
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    before = (root / OLD).read_bytes()
    code, out, err = cli(["apply", "--manifest", str(manifest_path)], capsys)
    assert code != 0
    assert expected in (out + err).lower()
    assert (root / OLD).read_bytes() == before
    assert not (root / NEW).exists()


def test_target_collision_and_traversal_fail_before_mutation(world, capsys):
    root, manifest, manifest_path, _index = world
    (root / NEW).write_bytes(b"occupied")
    code, out, err = cli(["apply", "--manifest", str(manifest_path)], capsys)
    assert code != 0 and "target" in (out + err).lower()
    (root / NEW).unlink()
    manifest["entries"][0]["new_path"] = "papers/../outside.md"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    code, out, err = cli(["apply", "--manifest", str(manifest_path)], capsys)
    assert code != 0 and "path" in (out + err).lower()
    assert (root / OLD).read_bytes() == RAW


def test_dry_run_rejects_moved_stub_suffix_collision(world, collision, capsys):
    root, _manifest, manifest_path, index = world
    suffix = OLD.split("/", 2)[-1]
    if collision == "other-family-paper":
        other = root / "papers/training/old/paper.md"
        other.parent.mkdir(parents=True)
        other.write_text(
            "---\ncanonical_id: arXiv:2401.00099\narxiv_id: 2401.00099\ntitle: Other\n---\nBody\n",
            encoding="utf-8",
        )
    else:
        snapshot = json.loads(index.read_text(encoding="utf-8"))
        snapshot["ignored_moved_stubs"] = [suffix]
        index.write_text(json.dumps(snapshot), encoding="utf-8")
    code, out, err = cli(["dry-run", "--manifest", str(manifest_path)], capsys)
    assert code != 0
    assert "moved-stub registration" in (out + err).lower()
    assert (root / OLD).read_bytes() == RAW
    assert not (root / NEW).exists()


def test_dry_run_rejects_target_suffix_already_ignored(world, capsys):
    root, _manifest, manifest_path, index = world
    snapshot = json.loads(index.read_text(encoding="utf-8"))
    snapshot["ignored_moved_stubs"] = [NEW.split("/", 2)[-1]]
    index.write_text(json.dumps(snapshot), encoding="utf-8")
    code, out, err = cli(["dry-run", "--manifest", str(manifest_path)], capsys)
    assert code != 0
    assert "target suffix conflicts with moved-stub registration" in (out + err).lower()
    assert (root / OLD).read_bytes() == RAW
    assert not (root / NEW).exists()


def test_dry_run_rejects_target_suffix_matching_another_entry_old_path(world, capsys):
    root, manifest, manifest_path, index = world
    old2, new2 = "papers/training/new/paper.md", "papers/training/dest/second.md"
    (root / old2).parent.mkdir(parents=True)
    (root / new2).parent.mkdir(parents=True)
    raw2 = RAW.replace(b"2401.00001", b"2401.00002").replace(b"10.1000/sample", b"10.1000/second")
    cid2 = "arXiv:2401.00002"
    (root / old2).write_bytes(raw2)
    aliases2 = [cid2, "DOI:10.1000/second"]
    snapshot = json.loads(index.read_text(encoding="utf-8"))
    snapshot["papers"][cid2] = {"path": old2, "identifiers": aliases2,
                                "source_hash": hashlib.sha256(raw2).hexdigest()}
    snapshot["identifier_to_canonical"].update({alias: cid2 for alias in aliases2})
    snapshot["active_count"] = 2
    index.write_text(json.dumps(snapshot), encoding="utf-8")
    manifest["entries"].append({"old_path": old2, "new_path": new2, "canonical_id": cid2,
                                "aliases": aliases2, "expected_sha256": hashlib.sha256(raw2).hexdigest()})
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    code, out, err = cli(["dry-run", "--manifest", str(manifest_path)], capsys)
    assert code != 0
    assert "target suffix conflicts with moved-stub registration" in (out + err).lower()
    assert (root / OLD).read_bytes() == RAW
    assert (root / old2).read_bytes() == raw2
    assert not (root / NEW).exists() and not (root / new2).exists()


def test_dry_run_rejects_duplicate_target_suffixes_in_batch(world, capsys):
    root, manifest, manifest_path, index = world
    _old2, _new2, _raw2, _cid2 = add_second_entry(root, manifest, manifest_path, index)
    manifest["entries"][1]["new_path"] = "papers/training/new/paper.md"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    code, out, err = cli(["dry-run", "--manifest", str(manifest_path)], capsys)
    assert code != 0
    assert "batch target suffix is duplicated" in (out + err).lower()
    assert (root / OLD).read_bytes() == RAW
    assert not (root / NEW).exists()


def test_pending_delta_for_moving_identity_is_rejected(world, capsys):
    _root, _manifest, manifest_path, _index = world
    identity_delta.prepare(OLD)
    code, out, err = cli(["apply", "--manifest", str(manifest_path)], capsys)
    assert code != 0 and "pending identity delta" in (out + err).lower()


def test_symlink_path_refused(world, capsys, monkeypatch):
    root, manifest, manifest_path, _index = world
    outside = root.parent / "outside"
    outside.mkdir()
    link = root / "papers/inference/link"
    original_is_symlink = Path.is_symlink
    monkeypatch.setattr(Path, "is_symlink", lambda self: self == link or original_is_symlink(self))
    manifest["entries"][0]["new_path"] = "papers/inference/link/paper.md"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    code, out, err = cli(["dry-run", "--manifest", str(manifest_path)], capsys)
    assert code != 0 and "symlink" in (out + err).lower()


def test_delta_validation_uses_repo_root_when_survey_root_is_dot_survey(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    survey_root = repo / ".survey"
    paper = repo / "papers/inference/old/paper.md"
    paper.parent.mkdir(parents=True)
    paper.write_bytes(RAW)
    delta_path = survey_root / "survey-state/identity-deltas/arxiv/2401.00001.json"
    delta_path.parent.mkdir(parents=True)
    snapshot = survey_root / "survey-state/paper-identity-index.json"
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    snapshot.write_text(json.dumps({"schema_version": 3, "papers": {}, "identifier_to_canonical": {}}), encoding="utf-8")
    delta_path.write_text(json.dumps({"schema_version": 1, "canonical_id": CID, "path": "papers/inference/old/paper.md",
        "identifiers": sorted([CID, "DOI:10.1000/sample"])}), encoding="utf-8")
    monkeypatch.setattr(survey, "ROOT", survey_root)
    monkeypatch.setattr(identity_delta, "ROOT", survey_root)
    assert migration._validate_deltas() == 1


def test_batch_apply_failure_rolls_back_every_entry(world, capsys, monkeypatch):
    root, manifest, manifest_path, index = world
    old2, new2, raw2, _cid2 = add_second_entry(root, manifest, manifest_path, index)
    before_index = index.read_bytes()
    def fail(phase):
        if phase == "target-installed:1": raise OSError("injected phase failure")
    monkeypatch.setattr(migration, "_after_phase", fail)
    code, out, err = cli(["apply", "--manifest", str(manifest_path)], capsys)
    assert code != 0
    assert (root / OLD).read_bytes() == RAW
    assert (root / old2).read_bytes() == raw2
    assert not (root / NEW).exists() and not (root / new2).exists()
    assert index.read_bytes() == before_index


def test_batch_apply_moves_all_entries(world, capsys):
    root, manifest, manifest_path, index = world
    old2, new2, raw2, cid2 = add_second_entry(root, manifest, manifest_path, index)
    # Move the second paper ahead of the first in filesystem path order. The
    # planned snapshot must use the same insertion order as survey.papers() after
    # the moves have been applied.
    new2 = "papers/inference/00-first/second.md"
    (root / new2).parent.mkdir(parents=True)
    manifest["entries"][1]["new_path"] = new2
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    code, out, err = cli(["apply", "--manifest", str(manifest_path)], capsys)
    assert code == 0, err
    assert json.loads(out)["entry_count"] == 2
    assert (root / NEW).read_bytes() == RAW and (root / new2).read_bytes() == raw2
    snapshot = json.loads(index.read_text(encoding="utf-8"))
    assert snapshot["papers"][CID]["path"] == NEW
    assert snapshot["papers"][cid2]["path"] == new2


def test_apply_accepts_100_entries_and_moves_all_original_bytes(tmp_path, monkeypatch, capsys):
    root, manifest_path, index, original_bytes = batch_world(tmp_path, monkeypatch, 100)
    before_index = index.read_bytes()
    code, out, err = cli(["dry-run", "--manifest", str(manifest_path)], capsys)
    assert code == 0, err
    assert json.loads(out)["entry_count"] == 100
    assert index.read_bytes() == before_index
    code, out, err = cli(["apply", "--manifest", str(manifest_path)], capsys)
    assert code == 0, err
    assert json.loads(out)["entry_count"] == 100
    snapshot = json.loads(index.read_text(encoding="utf-8"))
    for entry in json.loads(manifest_path.read_text(encoding="utf-8"))["entries"]:
        old_path, new_path = entry["old_path"], entry["new_path"]
        assert (root / new_path).read_bytes() == original_bytes[old_path]
        assert next(line for line in (root / old_path).read_text(encoding="utf-8").splitlines()
                    if line.strip()) == "# Moved"
        assert snapshot["papers"][entry["canonical_id"]]["path"] == new_path
        assert all(snapshot["identifier_to_canonical"][alias] == entry["canonical_id"]
                   for alias in entry["aliases"])
    assert len(snapshot["papers"]) == len(snapshot["identifier_to_canonical"]) // 2 == 100


def test_101_entries_rejected_before_any_mutation(tmp_path, monkeypatch, capsys):
    root, manifest_path, index, original_bytes = batch_world(tmp_path, monkeypatch, 101)
    before_index = index.read_bytes()
    code, out, err = cli(["apply", "--manifest", str(manifest_path)], capsys)
    assert code != 0 and "100 entries" in (out + err)
    assert index.read_bytes() == before_index
    assert all((root / path).read_bytes() == raw for path, raw in original_bytes.items())
    assert not any((root / entry["new_path"]).exists()
                   for entry in json.loads(manifest_path.read_text(encoding="utf-8"))["entries"])
    assert not (root / "survey-state/lineage-migrations").exists()


def test_source_bytes_above_64_mib_rejected_before_any_mutation(tmp_path, monkeypatch, capsys):
    root, manifest_path, index, original_bytes = batch_world(
        tmp_path, monkeypatch, 1, extra_body_bytes=64 * 1024 * 1024 + 1
    )
    old_path, raw = next(iter(original_bytes.items()))
    before_index = index.read_bytes()
    code, out, err = cli(["apply", "--manifest", str(manifest_path)], capsys)
    assert code != 0 and "source bytes" in (out + err).lower()
    assert index.read_bytes() == before_index
    assert (root / old_path).read_bytes() == raw
    assert not (root / "papers/inference/new/000-paper.md").exists()
    assert not (root / "survey-state/lineage-migrations").exists()


def test_late_batch_failure_after_entry_25_recovers_exact_original_state(
        tmp_path, monkeypatch, capsys):
    root, manifest_path, index, original_bytes = batch_world(tmp_path, monkeypatch, 30)
    before_index = index.read_bytes()
    def crash(phase):
        if phase == "target-installed:25":
            raise SimulatedCrash(phase)
    monkeypatch.setattr(migration, "_after_phase", crash)
    with raises(SimulatedCrash, match="target-installed:25"):
        migration.apply_manifest(manifest_path)
    monkeypatch.setattr(migration, "_after_phase", lambda _phase: None)
    journals = list((root / "survey-state/lineage-migrations").glob("*.json"))
    assert len(journals) == 1
    txid = journals[0].stem
    code, out, err = cli(["recover", "--transaction", txid, "--action", "rollback"], capsys)
    assert code == 0, err
    assert json.loads(out)["status"] == "rolled_back"
    assert index.read_bytes() == before_index
    for entry in json.loads(manifest_path.read_text(encoding="utf-8"))["entries"]:
        old_path, new_path = entry["old_path"], entry["new_path"]
        assert (root / old_path).read_bytes() == original_bytes[old_path]
        assert not (root / new_path).exists()
    journal = json.loads(journals[0].read_text(encoding="utf-8"))
    assert journal["source_main_sha"] == SOURCE_MAIN
    assert journal["status"] == "rolled_back"


class SimulatedCrash(BaseException):
    pass


def test_recover_rollback_after_crash_at_each_phase(world, capsys, monkeypatch, phase):
    root, manifest, manifest_path, index = world
    old2, new2, raw2, _cid2 = add_second_entry(root, manifest, manifest_path, index)
    before_index = index.read_bytes()
    def crash(current):
        if current == phase: raise SimulatedCrash(current)
    monkeypatch.setattr(migration, "_after_phase", crash)
    with raises(SimulatedCrash):
        migration.apply_manifest(manifest_path)
    monkeypatch.setattr(migration, "_after_phase", lambda _phase: None)
    journals = list((root / "survey-state/lineage-migrations").glob("*.json"))
    assert len(journals) == 1
    txid = journals[0].stem
    code, out, _ = cli(["recover", "--transaction", txid, "--action", "rollback"], capsys)
    assert code == 0 and json.loads(out)["status"] == "rolled_back"
    assert (root / OLD).read_bytes() == RAW
    assert not (root / NEW).exists()
    assert (root / old2).read_bytes() == raw2
    assert not (root / new2).exists()
    assert index.read_bytes() == before_index
    assert migration.recover(root, txid, "rollback")["status"] == "rolled_back"


def test_recovery_refuses_ambiguous_bytes_without_deleting_source(world, monkeypatch):
    root, _manifest, manifest_path, _index = world
    def crash(phase):
        if phase == "target-installed:0": raise SimulatedCrash(phase)
    monkeypatch.setattr(migration, "_after_phase", crash)
    with raises(SimulatedCrash): migration.apply_manifest(manifest_path)
    monkeypatch.setattr(migration, "_after_phase", lambda _phase: None)
    txid = migration.find_active_transaction(root)
    (root / NEW).write_bytes(b"ambiguous")
    with raises(migration.RecoveryConflict): migration.recover(root, txid, "rollback")
    assert (root / OLD).read_bytes() == RAW
    assert (root / NEW).read_bytes() == b"ambiguous"


def test_recovery_journal_sha_must_match_current_worktree(world, monkeypatch):
    root, _manifest, manifest_path, _index = world
    def crash(phase):
        if phase == "target-installed:0": raise SimulatedCrash(phase)
    monkeypatch.setattr(migration, "_after_phase", crash)
    with raises(SimulatedCrash): migration.apply_manifest(manifest_path)
    monkeypatch.setattr(migration, "_after_phase", lambda _phase: None)
    txid = migration.find_active_transaction(root)
    monkeypatch.setattr(migration, "current_worktree_sha", lambda: "f" * 40)
    with raises(migration.RecoveryConflict, match="source pin mismatch"):
        migration.recover(root, txid, "rollback")
    assert (root / OLD).read_bytes() == RAW
    assert (root / NEW).read_bytes() == RAW


def test_recovery_rejects_tampered_journal_paths_before_mutation(world, monkeypatch, field, value):
    root, _manifest, manifest_path, index = world
    before_index = index.read_bytes()
    def crash(phase):
        if phase == "target-installed:0": raise SimulatedCrash(phase)
    monkeypatch.setattr(migration, "_after_phase", crash)
    with raises(SimulatedCrash): migration.apply_manifest(manifest_path)
    monkeypatch.setattr(migration, "_after_phase", lambda _phase: None)
    txid = migration.find_active_transaction(root)
    journal_path = next((root / "survey-state/lineage-migrations").glob("*.json"))
    journal = json.loads(journal_path.read_text(encoding="utf-8"))
    if field in ("snapshot_path", "snapshot_temp"):
        journal[field] = value
    else:
        journal["entries"][0][field] = value
    journal_path.write_text(json.dumps(journal), encoding="utf-8")
    with raises(migration.RecoveryConflict, match="journal .* path"):
        migration.recover(root, txid, "rollback")
    assert (root / OLD).read_bytes() == RAW
    assert (root / NEW).read_bytes() == RAW
    assert index.read_bytes() == before_index


def test_recovery_refuses_symlink_staging_path_before_mutation(world, monkeypatch):
    root, _manifest, manifest_path, index = world
    before_index = index.read_bytes()
    def crash(phase):
        if phase == "target-installed:0": raise SimulatedCrash(phase)
    monkeypatch.setattr(migration, "_after_phase", crash)
    with raises(SimulatedCrash): migration.apply_manifest(manifest_path)
    monkeypatch.setattr(migration, "_after_phase", lambda _phase: None)
    txid = migration.find_active_transaction(root)
    target_temp = root / f"{NEW.rsplit('/', 1)[0]}/.{NEW.rsplit('/', 1)[1]}.{txid}.target.tmp"
    original_is_symlink = Path.is_symlink
    monkeypatch.setattr(Path, "is_symlink", lambda self: self == target_temp or original_is_symlink(self))
    with raises(migration.RecoveryConflict, match="staging path is a symlink"):
        migration.recover(root, txid, "rollback")
    assert (root / OLD).read_bytes() == RAW
    assert (root / NEW).read_bytes() == RAW
    assert index.read_bytes() == before_index


PARAMETER_CASES = [
    (test_stale_hash_id_snapshot_and_alias_fail_closed, [
        ("pin", "source_main_sha"), ("hash", "hash"), ("id", "canonical"),
        ("snapshot", "snapshot"), ("alias", "alias"),
    ]),
    (test_dry_run_rejects_moved_stub_suffix_collision, [
        ("other-family-paper",), ("registered-stub",),
    ]),
    (test_recover_rollback_after_crash_at_each_phase, [(phase,) for phase in DURABLE_PHASES]),
    (test_recovery_rejects_tampered_journal_paths_before_mutation, [
        ("snapshot_path", "../../outside.json"),
        ("snapshot_temp", "../outside.tmp"),
        ("target_temp", "../../outside.tmp"),
        ("stub_temp", "C:/outside.tmp"),
    ]),
]


def _run_unittest_case(function, parameter_values):
    temporary = tempfile.TemporaryDirectory(prefix="lineage-migration-")
    tmp_path = Path(temporary.name)
    monkeypatch = MonkeyPatch()
    old_survey_root, old_delta_root = survey.ROOT, identity_delta.ROOT
    try:
        args = []
        for parameter in inspect.signature(function).parameters:
            if parameter == "world":
                args.append(world(tmp_path, monkeypatch))
            elif parameter == "tmp_path":
                args.append(tmp_path)
            elif parameter == "monkeypatch":
                args.append(monkeypatch)
            elif parameter == "capsys":
                args.append(None)
            else:
                args.append(parameter_values.pop(0))
        function(*args)
    finally:
        monkeypatch.undo()
        survey.ROOT = old_survey_root
        identity_delta.ROOT = old_delta_root
        temporary.cleanup()


class TestPaperLineageMigration(unittest.TestCase):
    pass


_parameterized_functions = {function for function, _values in PARAMETER_CASES}
_parameter_values = {function: values for function, values in PARAMETER_CASES}
for _function in [value for value in globals().values()
                  if inspect.isfunction(value) and value.__name__.startswith("test_")]:
    if _function in _parameterized_functions:
        for _index, _values in enumerate(_parameter_values[_function]):
            def _test(self, function=_function, values=_values):
                _run_unittest_case(function, list(values))
            setattr(TestPaperLineageMigration, f"{_function.__name__}_{_index:02d}", _test)
    else:
        def _test(self, function=_function):
            _run_unittest_case(function, [])
        setattr(TestPaperLineageMigration, _function.__name__, _test)


