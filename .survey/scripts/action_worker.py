#!/usr/bin/env python3
"""GitHub Actions worker for survey helper operations.

Requests are JSON files under .survey/requests/. Results are written to
.survey/results/<request-name>.json. Only a small whitelist of operations is
accepted; arbitrary shell execution is intentionally unsupported.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MGMT = REPO / ".survey"
REQUESTS = MGMT / "requests"
RESULTS = MGMT / "results"
ALLOWED = {"status", "validate", "prepare_result"}


def run_json(cmd: list[str]) -> dict:
    p = subprocess.run(cmd, cwd=REPO, text=True, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f"command failed ({p.returncode}): {' '.join(cmd)}\n{p.stdout}\n{p.stderr}")
    out = p.stdout.strip()
    return json.loads(out) if out else {}


def run_text(cmd: list[str]) -> dict:
    p = subprocess.run(cmd, cwd=REPO, text=True, capture_output=True)
    return {
        "returncode": p.returncode,
        "stdout": p.stdout[-12000:],
        "stderr": p.stderr[-12000:],
    }


def handle(req: dict) -> dict:
    op = req.get("operation")
    if op not in ALLOWED:
        raise ValueError(f"unsupported operation: {op!r}")

    py = sys.executable
    if op == "status":
        payload = run_json([py, ".survey/scripts/next_work.py", "--root", ".survey"])
        return {"operation": op, "ok": True, "payload": payload}

    if op == "validate":
        checks = {
            "identity_delta": run_text([py, ".survey/scripts/identity_delta.py", "validate"]),
            "survey": run_text([py, ".survey/scripts/survey_v8.py", "validate"]),
            "tests": run_text([py, "-m", "unittest", "discover", "-s", ".survey/tests"]),
        }
        ok = all(v["returncode"] == 0 for v in checks.values())
        return {"operation": op, "ok": ok, "checks": checks}

    side = req.get("side")
    paper = req.get("paper")
    if side not in {"research", "audit"}:
        raise ValueError("prepare_result requires side=research|audit")
    if not isinstance(paper, str) or not paper.startswith("papers/") or ".." in Path(paper).parts:
        raise ValueError("prepare_result requires a safe repo-relative papers/... path")
    cmd = [
        py,
        ".survey/scripts/prepare_result.py",
        "--root", ".survey",
        "--side", side,
        "--paper", paper,
        "--apply",
    ]
    if req.get("status"):
        cmd += ["--status", str(req["status"])]
    if req.get("result"):
        cmd += ["--result", str(req["result"])]
    if req.get("note"):
        cmd += ["--note", str(req["note"])]
    payload = run_json(cmd)
    return {"operation": op, "ok": True, "payload": payload}


def process_one(path: Path) -> Path:
    result_path = RESULTS / path.name
    if result_path.exists():
        return result_path
    req = json.loads(path.read_text(encoding="utf-8"))
    result = {
        "schema_version": 1,
        "request_file": str(path.relative_to(REPO)),
        "request": req,
    }
    try:
        result.update(handle(req))
    except Exception as exc:
        result.update({"ok": False, "error": f"{type(exc).__name__}: {exc}"})
    RESULTS.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result_path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--request", help="process one request path; defaults to all unprocessed requests")
    args = p.parse_args()
    if args.request:
        path = (REPO / args.request).resolve()
        if REQUESTS.resolve() not in path.parents:
            raise SystemExit("request must be under .survey/requests")
        print(process_one(path))
        return
    for path in sorted(REQUESTS.glob("*.json")):
        if not (RESULTS / path.name).exists():
            print(process_one(path))


if __name__ == "__main__":
    main()
