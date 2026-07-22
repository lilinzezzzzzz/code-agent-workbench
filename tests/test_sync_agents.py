from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SYNC_SCRIPT = ROOT / "sync-agents.sh"


class SyncAgentRulesTest(unittest.TestCase):
    def assert_directory_equal(self, source: Path, target: Path) -> None:
        source_entries = sorted(
            path.relative_to(source) for path in source.rglob("*")
        )
        target_entries = sorted(
            path.relative_to(target) for path in target.rglob("*")
        )
        self.assertEqual(target_entries, source_entries)

        for relative_path in source_entries:
            source_entry = source / relative_path
            target_entry = target / relative_path
            self.assertEqual(target_entry.is_dir(), source_entry.is_dir())
            if source_entry.is_file():
                self.assertEqual(
                    target_entry.read_bytes(), source_entry.read_bytes()
                )

    def test_syncs_rules_to_workbuddy_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            workbuddy_root = directory / ".workbuddy"
            codex_root = directory / ".codex"
            environment = os.environ.copy()
            environment["WORKBUDDY_ROOT"] = str(workbuddy_root)
            environment["CODEX_ROOT"] = str(codex_root)

            result = subprocess.run(
                ["bash", str(SYNC_SCRIPT)],
                input="1\n2\n",
                text=True,
                capture_output=True,
                check=False,
                cwd=ROOT,
                env=environment,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(
                "2) workbuddy -> AGENTS.md + references", result.stderr
            )
            self.assertEqual(
                (workbuddy_root / "AGENTS.md").read_bytes(),
                (ROOT / "rules" / "agents.md").read_bytes(),
            )

            source_references = ROOT / "rules" / "references"
            target_references = workbuddy_root / "references"
            self.assert_directory_equal(source_references, target_references)

            self.assertFalse(codex_root.exists())

    def test_codex_and_workbuddy_use_the_same_rules_layout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            codex_root = directory / ".codex"
            workbuddy_root = directory / ".workbuddy"
            environment = os.environ.copy()
            environment["CODEX_ROOT"] = str(codex_root)
            environment["WORKBUDDY_ROOT"] = str(workbuddy_root)

            codex_result = subprocess.run(
                ["bash", str(SYNC_SCRIPT)],
                input="1\n1\n",
                text=True,
                capture_output=True,
                check=False,
                cwd=ROOT,
                env=environment,
            )
            workbuddy_result = subprocess.run(
                ["bash", str(SYNC_SCRIPT)],
                input="1\n2\n",
                text=True,
                capture_output=True,
                check=False,
                cwd=ROOT,
                env=environment,
            )

            self.assertEqual(codex_result.returncode, 0, codex_result.stderr)
            self.assertEqual(
                workbuddy_result.returncode, 0, workbuddy_result.stderr
            )
            self.assert_directory_equal(codex_root, workbuddy_root)

    def test_workbuddy_defaults_to_home_dot_workbuddy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            environment = os.environ.copy()
            environment["HOME"] = str(directory)
            environment.pop("WORKBUDDY_ROOT", None)

            result = subprocess.run(
                ["bash", str(SYNC_SCRIPT)],
                input="1\n2\n",
                text=True,
                capture_output=True,
                check=False,
                cwd=ROOT,
                env=environment,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            workbuddy_root = directory / ".workbuddy"
            self.assertTrue((workbuddy_root / "AGENTS.md").is_file())
            self.assertTrue((workbuddy_root / "references").is_dir())

    def test_rejects_empty_workbuddy_root(self) -> None:
        environment = os.environ.copy()
        environment["WORKBUDDY_ROOT"] = "   "

        result = subprocess.run(
            ["bash", str(SYNC_SCRIPT)],
            input="1\n2\n",
            text=True,
            capture_output=True,
            check=False,
            cwd=ROOT,
            env=environment,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("WORKBUDDY_ROOT cannot be empty.", result.stderr)

    def test_syncs_all_skills_to_workbuddy_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            codex_root = directory / ".codex"
            workbuddy_root = directory / ".workbuddy"
            qoder_root = directory / ".qoder"
            environment = os.environ.copy()
            environment["CODEX_ROOT"] = str(codex_root)
            environment["WORKBUDDY_ROOT"] = str(workbuddy_root)
            environment["QODER_ROOT"] = str(qoder_root)

            result = subprocess.run(
                ["bash", str(SYNC_SCRIPT)],
                input="2\n1\n2\n",
                text=True,
                capture_output=True,
                check=False,
                cwd=ROOT,
                env=environment,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("2) workbuddy", result.stderr)
            source_skills = ROOT / "skills"
            target_skills = workbuddy_root / "skills"
            expected_directories = [source_skills / "_shared"]
            expected_directories.extend(
                sorted(
                    path
                    for path in source_skills.iterdir()
                    if path.is_dir() and (path / "SKILL.md").is_file()
                )
            )
            self.assertEqual(
                sorted(path.name for path in target_skills.iterdir()),
                sorted(path.name for path in expected_directories),
            )
            for source_directory in expected_directories:
                self.assert_directory_equal(
                    source_directory, target_skills / source_directory.name
                )
            self.assertFalse(codex_root.exists())
            self.assertFalse(qoder_root.exists())


if __name__ == "__main__":
    unittest.main()
