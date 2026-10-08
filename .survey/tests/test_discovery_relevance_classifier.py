"""Bounded, resumable, fail-open classifier regression tests."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import discovery_relevance_classifier as ml
import discovery_relevance_prefilter as rule

spec = importlib.util.spec_from_file_location("discovery_relevance_batch_test", SCRIPTS / "discovery_relevance_batch.py")
batch = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(batch)


class ClassifierTests(unittest.TestCase):
    def test_features_deterministic(self):
        self.assertEqual(ml.features("GPU Memory Inference"), ml.features("gpu memory inference"))
        self.assertIn("b:gpu_memory", ml.features("GPU Memory Inference"))

    def test_training_has_validated_threshold(self):
        pos = [f"efficient gpu inference offloading optimization architecture token{i:03d}" for i in range(100)]
        neg = [f"agriculture tomato crop phenotyping detection field{i:03d}" for i in range(100)]
        with mock.patch.object(ml, "_paper_labels", return_value=(pos, neg)):
            model = ml.train(Path("/no-repo"))
        self.assertTrue(model["approved"])
        self.assertEqual(model["validation_positive_recall"], 1.0)
        self.assertTrue(model["model_id"])

    def test_too_few_labels_fail_open(self):
        with mock.patch.object(ml, "_paper_labels", return_value=(["one"], ["two"])):
            model = ml.train(Path("/no-repo"))
        self.assertFalse(model["approved"])
        self.assertFalse(ml.predict("tomato crop", model))

    def test_title_edit_invalidates_key(self):
        a = {"canonical_id": "arXiv:2601.01234", "title": "First title"}
        self.assertNotEqual(ml.identity_key(a), ml.identity_key({**a, "title": "Second title"}))

    def test_durable_shards_are_model_specific(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            key = ml.identity_key({"canonical_id": "a", "title": "one"})
            ml.save_shard(root, ml.shard_for(key), "model-1", {key: "q"})
            self.assertEqual(ml.load_decisions(root, "model-1")[key], "q")
            self.assertEqual(ml.load_decisions(root, "model-2"), {})

    def test_two_batches_dont_repeat_scanned_candidates(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            cfg = root / ".survey/config/discovery-relevance-prefilter.json"
            cfg.parent.mkdir(parents=True)
            cfg.write_text(json.dumps({
                "schema_version": 1, "enabled": True, "mode": "quarantine",
                "classifier": {"enabled": True, "mode": "quarantine"},
            }), encoding="utf-8")
            model = {
                "schema_version": 1, "approved": True, "model_id": "demo",
                "weights": {"u:tomato": -3.0}, "threshold": -0.1,
            }
            source = [
                {"canonical_id": f"arXiv:2601.{i:05d}", "title": "Tomato phenotyping"}
                for i in range(8)
            ]
            with mock.patch.object(batch.ml, "load_model", return_value=model), mock.patch.object(
                batch.worklist, "_discovery_candidates", return_value=(source, len(source))
            ), mock.patch.object(batch.worklist, "_current_research_reservations", return_value=[]):
                first = batch.run(root, batch_size=2)
                second = batch.run(root, batch_size=2)
            self.assertEqual(first["processed_this_batch"], 2)
            self.assertEqual(second["processed_this_batch"], 2)
            self.assertEqual(len(ml.load_decisions(root, "demo")), 4)

    def test_worklist_cached_model_predictions_are_reversible(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            model = {
                "schema_version": 1, "approved": True, "model_id": "demo",
                "weights": {"u:tomato": -3.0}, "threshold": -0.1,
            }
            model_path = root / ml.MODEL_PATH
            model_path.parent.mkdir(parents=True)
            model_path.write_text(json.dumps(model), encoding="utf-8")
            rows = [{"canonical_id": "x", "title": "Model applications in literature"}]
            key = ml.identity_key(rows[0])
            ml.save_shard(root, ml.shard_for(key), "demo", {key: "q"})
            policy = {"enabled": True, "mode": "quarantine", "classifier": {"enabled": True, "mode": "quarantine"}, "max_audit_per_build": 0}
            selected, stats = rule.triage_worklist(rows, policy, root=root)
            self.assertEqual(stats["classifier_scanned_count"], 1)
            self.assertEqual(stats["classifier_quarantine_count"], 1)
            self.assertEqual(selected, [])
            restored, _ = rule.triage_worklist(rows, {**policy, "enabled": False}, root=root)
            self.assertEqual(restored, rows)


if __name__ == "__main__":
    unittest.main()
