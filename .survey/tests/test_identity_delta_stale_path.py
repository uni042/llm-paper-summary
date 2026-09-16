import importlib.util
import json
import sys
from pathlib import Path


def load_identity_delta(repo_root: Path):
    scripts = repo_root / ".survey" / "scripts"
    sys.path.insert(0, str(scripts))
    spec = importlib.util.spec_from_file_location("identity_delta_test", scripts / "identity_delta.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prepare_replaces_stale_delta_when_old_path_no_longer_exists(tmp_path, monkeypatch):
    survey_dir = tmp_path / ".survey"
    scripts = survey_dir / "scripts"
    scripts.mkdir(parents=True)
    source_scripts = Path(__file__).resolve().parents[1] / "scripts"
    (scripts / "identity_delta.py").write_text((source_scripts / "identity_delta.py").read_text(encoding="utf-8"), encoding="utf-8")
    (scripts / "survey.py").write_text((source_scripts / "survey.py").read_text(encoding="utf-8"), encoding="utf-8")

    paper = tmp_path / "papers" / "new.md"
    paper.parent.mkdir(parents=True)
    paper.write_text("---\ncanonical_id: arXiv:2608.13127\narxiv_id: '2608.13127'\n---\n", encoding="utf-8")

    delta = survey_dir / "survey-state" / "identity-deltas" / "arxiv" / "2608.13127.json"
    delta.parent.mkdir(parents=True)
    delta.write_text(json.dumps({
        "schema_version": 1,
        "canonical_id": "arXiv:2608.13127",
        "path": "papers/old.md",
        "identifiers": ["arXiv:2608.13127"],
    }), encoding="utf-8")

    module = load_identity_delta(tmp_path)
    monkeypatch.setattr(module, "ROOT", survey_dir)
    monkeypatch.setattr(module.survey, "ROOT", survey_dir)

    output = module.prepare("papers/new.md")
    assert output == "survey-state/identity-deltas/arxiv/2608.13127.json"
    assert json.loads(delta.read_text(encoding="utf-8"))["path"] == "papers/new.md"
