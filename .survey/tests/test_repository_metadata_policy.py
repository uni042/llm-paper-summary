from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_repository  # noqa: E402


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


class RepositoryMetadataPolicyTests(unittest.TestCase):
    def test_month_precision_publication_date_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            frozen = root / ".survey/survey-state/frozen-training.json"
            frozen.parent.mkdir(parents=True, exist_ok=True)
            frozen.write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "policy": "No new training paper entries; existing files may be edited.",
                        "files": {"papers/training/README.md": "historical"},
                    }
                ),
                encoding="utf-8",
            )

            paper = root / "papers/inference/test/month-precision.md"
            paper.parent.mkdir(parents=True, exist_ok=True)
            paper.write_text(
                """---
canonical_id: DOI:10.0000/example
title: Month Precision Example
summary: Month-precision proceedings metadata must remain valid when the primary source exposes no day.
authors:
- Example Author
published: 2025-11
publication: Example Proceedings
publication_type: conference
publication_status: published
source: https://example.com/paper
sources:
- https://example.com/paper
implementation: null
code: null
last_checked: '2026-09-20'
last_audited: null
audit_version: 0
---
# Month Precision Example
""",
                encoding="utf-8",
            )

            files = []
            for current in sorted(root.rglob("*")):
                if current.is_file():
                    data = current.read_bytes()
                    files.append(
                        {
                            "path": current.relative_to(root).as_posix(),
                            "sha": blob_sha(data),
                        }
                    )
            inventory = {"source_commit": "test", "files": files}

            with patch.object(check_repository, "REQUIRED_V10_PATHS", ()):
                result = check_repository.check(root, inventory)

            invalid = [
                finding
                for finding in result["findings"]
                if finding["code"] == "paper_invalid_metadata"
                and finding["path"] == paper.relative_to(root).as_posix()
            ]
            self.assertEqual(invalid, [])


if __name__ == "__main__":
    unittest.main()
