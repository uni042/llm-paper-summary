#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / ".survey" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import refresh_under16kb_reaudit_queue as reaud


def paper_text(*, attested: bool, english_heavy: bool = False) -> str:
    marker = ""
    if attested:
        marker = (
            f'under16kb_reaudit_version: "{reaud.REAUDIT_VERSION}"\n'
            "under16kb_reaudit_passed: true\n"
        )
    overview = ("system serving cache " * 220) if english_heavy else ("概要の日本語説明。" * 180)
    method = "入力を観測して内部状態を更新し、出力を選択する手法の説明。" * 55
    evaluation = "比較条件と指標と結果を対応付けて評価する説明。" * 45
    limitation = "適用範囲と失敗条件を明示する。" * 15
    return f"""---
canonical_id: arXiv:2601.00001
title: Example
source: https://arxiv.org/abs/2601.00001
summary: 日本語の概要。
list_summary: 日本語の一覧要約。
{marker}---
# Example

## 概要
{overview}

## 手法
{method}

## 評価
{evaluation}

## 限界
{limitation}
"""


class Under16KbReauditTests(unittest.TestCase):
    def test_blob_sha_matches_git_hash_object(self) -> None:
        # Git object headers end with a NUL byte, not literal backslash-zero.
        for payload in (b"", b"hello\n", "日本語の論文解説".encode("utf-8"), b"\x00" * 512):
            with self.subTest(payload_len=len(payload)):
                actual = subprocess.run(
                    ["git", "hash-object", "--stdin"],
                    input=payload,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True,
                ).stdout.decode("ascii").strip()
                self.assertEqual(reaud.git_blob_sha(payload), actual)

    def test_assignment_is_stable(self) -> None:
        path = "papers/inference/01-offload-hierarchical-memory/example.md"
        self.assertEqual(reaud.assigned_worker(path), reaud.assigned_worker(path))
        self.assertIn(reaud.assigned_worker(path), reaud.WORKERS)

    def test_balancing_skewed_existing_assignments_and_preserving_live_edges(self) -> None:
        # The last worker may accumulate far more *remaining* papers as other
        # workers finish; the regenerated queue must balance what is left.
        workers = reaud.WORKERS
        rows = [
            {"path": f"papers/inference/paper-{n:03d}.md", "assigned_worker": owner}
            for owner, length in zip(workers, (76, 76, 145))
            for n in range(length)
        ]
        # Paths must be unique across workers, as in a real paper queue.
        for i, row in enumerate(rows):
            row["path"] = f"papers/inference/paper-{i:03d}.md"
        before = {r["path"]: r["assigned_worker"] for r in rows}
        edges = {
            r["path"]
            for owner in workers
            for r in (
                [row for row in rows if row["assigned_worker"] == owner][:5]
                + [row for row in rows if row["assigned_worker"] == owner][-5:]
            )
        }
        reaud.rebalance_workers(rows, before)
        counts = [sum(r["assigned_worker"] == owner for r in rows) for owner in workers]
        self.assertEqual(counts, [99, 99, 99])
        self.assertEqual(sum(r["assigned_worker"] != before[r["path"]] for r in rows), 46)
        self.assertTrue(all(r["assigned_worker"] == before[r["path"]] for r in rows if r["path"] in edges))
        balanced = {r["path"]: r["assigned_worker"] for r in rows}
        reaud.rebalance_workers(rows, balanced)
        self.assertEqual(balanced, {r["path"]: r["assigned_worker"] for r in rows})

    def test_balancer_handles_new_and_completed_papers_without_mass_rotation(self) -> None:
        workers = reaud.WORKERS
        rows = [
            {"path": f"papers/inference/{i:03d}.md", "assigned_worker": workers[i % 3]}
            for i in range(90)
        ]
        previous = {r["path"]: r["assigned_worker"] for r in rows}
        rows.pop(0)  # completed job should not rotate the rest
        reaud.rebalance_workers(rows, previous)
        self.assertEqual(sum(r["assigned_worker"] != previous[r["path"]] for r in rows), 0)
        self.assertLessEqual(
            max(sum(r["assigned_worker"] == w for r in rows) for w in workers)
            - min(sum(r["assigned_worker"] == w for r in rows) for w in workers),
            1,
        )
        # A new paper can be assigned without reshuffling all old ownership.
        new_path = "papers/inference/new-paper.md"
        rows.append({"path": new_path, "assigned_worker": reaud.assigned_worker(new_path)})
        reaud.rebalance_workers(rows, previous)
        self.assertLessEqual(
            max(sum(r["assigned_worker"] == w for r in rows) for w in workers)
            - min(sum(r["assigned_worker"] == w for r in rows) for w in workers),
            1,
        )
        self.assertLessEqual(
            sum(r["assigned_worker"] != previous[r["path"]] for r in rows if r["path"] in previous),
            1,
        )

    def test_attested_mechanical_pass_is_removed_from_queue(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper = root / "papers/inference/01-offload-hierarchical-memory/example.md"
            paper.parent.mkdir(parents=True)
            paper.write_text(paper_text(attested=True), encoding="utf-8")

            queue = reaud.build_queue(root)
            self.assertEqual(queue["count"], 0)

    def test_unattested_paper_stays_in_queue(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper = root / "papers/inference/01-offload-hierarchical-memory/example.md"
            paper.parent.mkdir(parents=True)
            paper.write_text(paper_text(attested=False), encoding="utf-8")

            queue = reaud.build_queue(root)
            self.assertEqual(queue["count"], 1)
            entry = queue["entries"][0]
            self.assertEqual(entry["semantic_status"], "pending")
            self.assertGreaterEqual(entry["japanese_ratio"], reaud.MIN_JAPANESE_RATIO)

    def test_pending_candidate_does_not_escape_by_growing_above_16kb(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper = root / "papers/inference/01-offload-hierarchical-memory/example.md"
            paper.parent.mkdir(parents=True)
            paper.write_text(paper_text(attested=False), encoding="utf-8")

            first = reaud.build_queue(root)
            self.assertEqual(first["count"], 1)
            self.assertTrue(reaud.write_queue(root, first))

            paper.write_text(
                paper_text(attested=False) + ("追加の日本語説明。" * 2500),
                encoding="utf-8",
            )
            self.assertGreaterEqual(
                len(paper.read_bytes()),
                reaud.MAX_FILE_BYTES,
            )

            second = reaud.build_queue(root)
            self.assertEqual(second["count"], 1)
            self.assertEqual(second["entries"][0]["path"], paper.relative_to(root).as_posix())

    def test_attested_candidate_can_leave_after_growing_above_16kb(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper = root / "papers/inference/01-offload-hierarchical-memory/example.md"
            paper.parent.mkdir(parents=True)
            paper.write_text(paper_text(attested=False), encoding="utf-8")

            first = reaud.build_queue(root)
            self.assertEqual(first["count"], 1)
            self.assertTrue(reaud.write_queue(root, first))

            paper.write_text(
                paper_text(attested=True) + ("追加の日本語説明。" * 2500),
                encoding="utf-8",
            )
            self.assertGreaterEqual(
                len(paper.read_bytes()),
                reaud.MAX_FILE_BYTES,
            )

            second = reaud.build_queue(root)
            self.assertEqual(second["count"], 0)

    def test_japanese_ratio_below_80_percent_is_a_reaudit_failure(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper = root / "papers/inference/01-offload-hierarchical-memory/example.md"
            paper.parent.mkdir(parents=True)
            paper.write_text(
                paper_text(attested=True, english_heavy=True),
                encoding="utf-8",
            )

            queue = reaud.build_queue(root)
            self.assertEqual(queue["count"], 1)
            self.assertTrue(
                any(
                    "日本語比率" in reason
                    for reason in queue["entries"][0]["mechanical_failures"]
                )
            )

    def test_survey_does_not_require_experimental_evaluation_floor(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper = root / "papers/survey/example.md"
            paper.parent.mkdir(parents=True)
            text = paper_text(attested=True).replace(
                "比較条件と指標と結果を対応付けて評価する説明。" * 45,
                "評価軸の整理。",
            )
            paper.write_text(text, encoding="utf-8")
            audit, meta = reaud.audit_one(paper, root)
            failures = reaud.reaudit_failures(audit, "papers/survey/example.md")
            self.assertFalse(any("評価説明量" in reason for reason in failures))
            self.assertTrue(reaud.semantic_attestation_present(meta))


if __name__ == "__main__":
    unittest.main()
