import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "preflight.py"
SPEC = importlib.util.spec_from_file_location("preflight", MODULE_PATH)
preflight = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(preflight)


class PreflightTests(unittest.TestCase):
    def setUp(self):
        preflight.errors.clear()
        preflight.warns.clear()
        preflight.infos.clear()

    def test_allowlisted_domains_require_a_label_boundary(self):
        self.assertTrue(preflight.domain_allowed("github.com"))
        self.assertTrue(preflight.domain_allowed("docs.github.com"))
        self.assertFalse(preflight.domain_allowed("evilgithub.com"))

    def test_skill_frontmatter_requires_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "SKILL.md").write_text(
                "---\ndescription: missing name\n---\n\n# Test\n",
                encoding="utf-8",
            )

            preflight.check_skill_frontmatter(root)

        self.assertIn("SKILL.md frontmatter 缺 name", preflight.errors)


if __name__ == "__main__":
    unittest.main()
