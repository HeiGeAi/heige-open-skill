import importlib.util
import os
import subprocess
import sys
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

    def test_skill_frontmatter_tolerates_utf8_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "SKILL.md").write_text(
                f"\ufeff---\nname: {root.name}\ndescription: test\n---\n\n# Test\n",
                encoding="utf-8",
            )

            preflight.check_skill_frontmatter(root)

        self.assertEqual(preflight.errors, [])

    def test_skill_frontmatter_requires_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "SKILL.md").write_text(
                "---\ndescription: missing name\n---\n\n# Test\n",
                encoding="utf-8",
            )

            preflight.check_skill_frontmatter(root)

        self.assertIn("SKILL.md frontmatter 缺 name", preflight.errors)

    def _git(self, root, *args, check=True):
        return subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            check=check,
        )

    def _commit(self, root, email, subject, body=None):
        self._git(root, "add", ".")
        command = [
            "-c", "user.name=Test Author",
            "-c", f"user.email={email}",
            "-c", "commit.gpgsign=false",
            "commit", "-m", subject,
        ]
        if body:
            command.extend(["-m", body])
        self._git(root, *command)
        return self._git(root, "rev-parse", "HEAD").stdout.strip()

    def _create_repo(self, root, first_email, first_body=None):
        (root / "README.md").write_text("# Test\n", encoding="utf-8")
        (root / "LICENSE").write_text(
            "MIT License\n\nCopyright 2026 HeiGeAi\n",
            encoding="utf-8",
        )
        (root / ".gitignore").write_text("*.pyc\n", encoding="utf-8")
        (root / "SKILL.md").write_text(
            f"---\nname: {root.name}\ndescription: test\n---\n\n# Test\n",
            encoding="utf-8",
        )
        self._git(root, "init", "-b", "main")
        return self._commit(root, first_email, "initial", first_body)

    def _run_preflight(self, root, *args):
        return subprocess.run(
            [sys.executable, str(MODULE_PATH), str(root), *args],
            capture_output=True,
            text=True,
        )

    def test_git_range_excludes_legacy_identity_and_commit_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            legacy_sha = self._create_repo(
                root,
                "legacy@example.com",
                "Co-Authored-By: Legacy <legacy@example.com>",
            )
            (root / "README.md").write_text("# Test\n\nCurrent.\n", encoding="utf-8")
            self._commit(
                root,
                "12345+test@users.noreply.github.com",
                "current",
            )

            result = self._run_preflight(root, "--git-range", f"{legacy_sha}..HEAD")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_git_range_still_rejects_new_private_email(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base_sha = self._create_repo(
                root,
                "12345+test@users.noreply.github.com",
            )
            (root / "README.md").write_text("# Test\n\nPrivate.\n", encoding="utf-8")
            self._commit(root, "private@example.com", "current")

            result = self._run_preflight(root, "--git-range", f"{base_sha}..HEAD")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("private@example.com", result.stdout)

    def test_invalid_git_range_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._create_repo(root, "12345+test@users.noreply.github.com")

            result = self._run_preflight(root, "--git-range", "missing..HEAD")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("missing..HEAD", result.stdout)

    def test_three_dot_git_range_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base_sha = self._create_repo(
                root,
                "12345+test@users.noreply.github.com",
            )
            (root / "README.md").write_text("# Test\n\nCurrent.\n", encoding="utf-8")
            self._commit(
                root,
                "12345+test@users.noreply.github.com",
                "current",
            )

            result = self._run_preflight(root, "--git-range", f"{base_sha}...HEAD")

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("格式无效", result.stdout)

    def test_committer_private_email_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._create_repo(root, "12345+test@users.noreply.github.com")
            (root / "README.md").write_text("# Test\n\nLeaky.\n", encoding="utf-8")
            self._git(root, "add", ".")
            env = dict(
                os.environ,
                GIT_COMMITTER_NAME="Leaky Committer",
                GIT_COMMITTER_EMAIL="leaky@gmail.com",
            )
            subprocess.run(
                [
                    "git", "-C", str(root),
                    "-c", "user.name=Test Author",
                    "-c", "user.email=12345+test@users.noreply.github.com",
                    "-c", "commit.gpgsign=false",
                    "commit", "-m", "committer leak",
                ],
                capture_output=True,
                text=True,
                check=True,
                env=env,
            )

            result = self._run_preflight(root)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("leaky@gmail.com", result.stdout)

    def test_empty_repo_still_skips_history_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Test\n", encoding="utf-8")
            (root / "LICENSE").write_text(
                "MIT License\n\nCopyright 2026 HeiGeAi\n", encoding="utf-8"
            )
            (root / ".gitignore").write_text("*.pyc\n", encoding="utf-8")
            (root / "SKILL.md").write_text(
                f"---\nname: {root.name}\ndescription: test\n---\n\n# Test\n",
                encoding="utf-8",
            )
            self._git(root, "init", "-b", "main")

            result = self._run_preflight(root)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("git 历史为空", result.stdout)

    def test_broken_git_repo_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._create_repo(root, "12345+test@users.noreply.github.com")
            # 模拟 .git 损坏: HEAD 内容非法, git log 直接报错
            (root / ".git" / "HEAD").write_text("garbage-not-a-ref\n", encoding="utf-8")

            result = self._run_preflight(root)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("git 历史检查失败", result.stdout)

    def test_default_preflight_keeps_full_history_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._create_repo(root, "legacy@example.com")

            result = self._run_preflight(root)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("legacy@example.com", result.stdout)

    def test_ci_uses_auditable_ranges_and_keeps_full_history_dispatch(self):
        workflow = (MODULE_PATH.parents[1] / ".github" / "workflows" / "ci.yml").read_text(
            encoding="utf-8",
        )

        self.assertIn("fetch-depth: 0", workflow)
        self.assertIn(
            "github.event.pull_request.base.sha }}..${{ github.event.pull_request.head.sha",
            workflow,
        )
        self.assertIn("github.event.before }}..${{ github.sha", workflow)
        self.assertRegex(
            workflow,
            r"if: github\.event_name == 'workflow_dispatch'\s+run: python scripts/preflight\.py \.\s",
        )


if __name__ == "__main__":
    unittest.main()
