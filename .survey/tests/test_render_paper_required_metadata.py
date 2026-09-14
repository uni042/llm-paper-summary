import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

spec = importlib.util.spec_from_file_location("render_paper", SCRIPTS / "render_paper.py")
render_paper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render_paper)


class RenderPaperRequiredMetadataTests(unittest.TestCase):
    def test_renderer_preserves_nullable_code_key(self):
        record = {
            "metadata": {
                "canonical_id": "arXiv:2609.99999",
                "title": "Synthetic Paper",
                "summary": "動作確認用の十分な長さを持つ概要。システムの構成と評価方法を説明し、レンダリング時の必須メタデータ保持を確認する。",
                "list_summary": "必須メタデータの保持を確認するため、コード未公開の論文を模した入力から前文のnullableキーを検証するテスト。",
                "source": "https://arxiv.org/abs/2609.99999",
                "sources": ["https://arxiv.org/abs/2609.99999"],
                "authors": ["A. Researcher"],
                "published": "2026-09-01",
                "publication": "arXiv",
                "publication_type": "Preprint",
                "publication_status": "Preprint",
                "implementation": "公式コードは未公開。",
                "code": None,
                "last_checked": "2026-09-14",
            },
            "problem_method": {
                "problem": "既存方式では必須nullableフィールドが出力時に欠落する。",
                "novelty": "nullableなcodeキーを明示的に保持する。",
                "method_overview": "入力メタデータを前文へ変換し、codeがNoneでもcode: nullとして保持する。",
            },
            "evaluation": {"methodology": "生成されたMarkdown前文を確認する。"},
            "results": {
                "overview": "必須キーが保持されることを確認する。",
                "key_results": [{"metric": "code key", "value": "preserved"}],
            },
            "positioning": {"limitations": ["合成入力による回帰テストである。"]},
        }
        rendered = render_paper.render_paper(record)
        frontmatter = rendered.split("---", 2)[1]
        self.assertIn("code: null", frontmatter)


if __name__ == "__main__":
    unittest.main()
