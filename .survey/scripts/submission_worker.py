#!/usr/bin/env python3
"""Apply small survey submissions produced by Chat/Scheduled Task.

Each submission is an immutable JSON file under .survey/submissions/.
Processed results are written under .survey/submission-results/ with the same name.
Only validated, claim-bound paper publications are allowed.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MGMT = REPO / ".survey"
SUBMISSIONS = MGMT / "submissions"
RESULTS = MGMT / "submission-results"
CYCLE_STATE = MGMT / "survey-state" / "cycle-state.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: str) -> str | None:
    p = subprocess.run(
        ["git", "rev-parse", f"HEAD:{path}"],
        cwd=REPO, text=True, capture_output=True
    )
    return p.stdout.strip() if p.returncode == 0 else None


def run_json(cmd: list[str]) -> dict:
    p = subprocess.run(cmd, cwd=REPO, text=True, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(
            f"command failed ({p.returncode}): {' '.join(cmd)}\n{p.stdout}\n{p.stderr}"
        )
    out = p.stdout.strip()
    return json.loads(out) if out else {}


def validate_common(sub: dict) -> tuple[str, str, str, str]:
    if sub.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    if sub.get("operation") != "publish_result":
        raise ValueError("operation is not publish_result")

    side = sub.get("side")
    if side not in {"research", "audit"}:
        raise ValueError("side must be research|audit")

    paper = sub.get("paper")
    if not isinstance(paper, str) or not paper.startswith("papers/"):
        raise ValueError("paper must be a repo-relative papers/... path")
    pp = Path(paper)
    if ".." in pp.parts or pp.suffix.lower() != ".md":
        raise ValueError("unsafe paper path")

    claim_token = sub.get("claim_token")
    if not isinstance(claim_token, str) or not claim_token:
        raise ValueError("claim_token is required")

    content = sub.get("content")
    if not isinstance(content, str) or len(content.strip()) < 200:
        raise ValueError("content must contain the complete paper markdown")
    if len(content.encode("utf-8")) > 512_000:
        raise ValueError("content exceeds 512 KiB submission limit")

    return side, paper, claim_token, content


def apply_submission(path: Path) -> Path:
    result_path = RESULTS / path.name
    if result_path.exists():
        return result_path

    sub = load_json(path)
    result = {
        "schema_version": 1,
        "submission_file": str(path.relative_to(REPO)),
        "ok": False,
    }
    try:
        if sub.get("schema_version") != 1:
            raise ValueError("schema_version must be 1")
        if sub.get("operation") == "probe":
            result.update({
                "ok": True,
                "operation": "probe",
                "payload": sub.get("payload"),
            })
            RESULTS.mkdir(parents=True, exist_ok=True)
            result_path.write_text(
                json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            return result_path

        side, paper, claim_token, content = validate_common(sub)

        state = load_json(CYCLE_STATE)
        active = state.get("active_claim") or {}
        if active.get("claim_token") != claim_token:
            raise ValueError("stale or mismatched claim_token")

        expected_cycle = sub.get("cycle_id")
        if expected_cycle and active.get("cycle_id") != expected_cycle:
            raise ValueError("cycle_id does not match active claim")
        expected_run = sub.get("run_id")
        if expected_run and active.get("run_id") != expected_run:
            raise ValueError("run_id does not match active claim")

        current_sha = git_blob_sha(paper)
        expected_sha = sub.get("expected_blob_sha")
        if expected_sha is not None:
            if not isinstance(expected_sha, str):
                raise ValueError("expected_blob_sha must be string or null")
            if current_sha != expected_sha:
                raise ValueError(
                    f"paper blob changed: expected {expected_sha}, current {current_sha}"
                )
        elif current_sha is not None and not sub.get("allow_existing_without_sha", False):
            raise ValueError("existing paper requires expected_blob_sha")

        target = REPO / paper
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content.rstrip() + "\n", encoding="utf-8")

        py = sys.executable
        cmd = [
            py, ".survey/scripts/prepare_result.py",
            "--root", ".survey",
            "--side", side,
            "--paper", paper,
            "--apply",
        ]
        if sub.get("status"):
            cmd += ["--status", str(sub["status"])]
        if sub.get("result"):
            cmd += ["--result", str(sub["result"])]
        if sub.get("note"):
            cmd += ["--note", str(sub["note"])]
        prepared = run_json(cmd)

        result.update({
            "ok": True,
            "operation": "publish_result",
            "side": side,
            "paper": paper,
            "claim_token": claim_token,
            "previous_blob_sha": current_sha,
            "prepared": prepared,
        })
    except Exception as exc:
        result.update({"error": f"{type(exc).__name__}: {exc}"})

    RESULTS.mkdir(parents=True, exist_ok=True)
    result_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return result_path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--submission")
    args = p.parse_args()
    SUBMISSIONS.mkdir(parents=True, exist_ok=True)

    if args.submission:
        path = (REPO / args.submission).resolve()
        if SUBMISSIONS.resolve() not in path.parents:
            raise SystemExit("submission must be under .survey/submissions")
        print(apply_submission(path))
        return

    for path in sorted(SUBMISSIONS.glob("*.json")):
        if not (RESULTS / path.name).exists():
            print(apply_submission(path))


if __name__ == "__main__":
    main()
