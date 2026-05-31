from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_install_module():
    spec = importlib.util.spec_from_file_location("decision_kernel_install", ROOT / "scripts" / "install.py")
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class InstallScriptTests(unittest.TestCase):
    def test_backup_existing_dry_run_preserves_directory(self) -> None:
        install = load_install_module()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "anneal"
            target.mkdir()
            (target / "SKILL.md").write_text("---\nname: old\ndescription: old\n---\n")
            install.backup_existing(target, apply=False)
            self.assertTrue(target.exists())
            self.assertFalse((Path(tmp) / ".backup").exists())

    def test_backup_existing_apply_moves_directory(self) -> None:
        install = load_install_module()
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "anneal"
            target.mkdir()
            (target / "SKILL.md").write_text("---\nname: old\ndescription: old\n---\n")
            install.backup_existing(target, apply=True)
            self.assertFalse(target.exists())
            backups = list((Path(tmp) / ".backup").glob("anneal-*"))
            self.assertEqual(len(backups), 1)

    def test_codex_frontmatter_sanitizer_keeps_only_name_and_description(self) -> None:
        install = load_install_module()
        raw = "\n".join(
            [
                "name: anneal",
                "description: |",
                "  A skill.",
                "disable-model-invocation: true",
                "argument-hint: \"[goal]\"",
            ]
        )
        sanitized = install.keep_name_description(raw)
        self.assertIn("name: anneal", sanitized)
        self.assertIn("description: |", sanitized)
        self.assertNotIn("disable-model-invocation", sanitized)
        self.assertNotIn("argument-hint", sanitized)


if __name__ == "__main__":
    unittest.main()
