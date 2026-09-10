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

    def test_rules_mirror_references_without_removing_sibling_content(self) -> None:
        targets = (
            ("CODEX_ROOT", "1"),
            ("WORKBUDDY_ROOT", "2"),
            ("OPENCODE_ROOT", "3"),
            ("ZCODE_ROOT", "4"),
            ("QODER_CN_ROOT", "5"),
        )
        for variable, selection in targets:
            with self.subTest(target=variable), tempfile.TemporaryDirectory() as temporary_directory:
                target = Path(temporary_directory) / "assistant root"
                references = target / "references"
                obsolete = references / "obsolete"
                obsolete.mkdir(parents=True)
                (obsolete / "nested.md").write_text("obsolete", encoding="utf-8")
                (references / "ai-rag.md").write_text("legacy", encoding="utf-8")
                (references / ".custom").write_text("hidden", encoding="utf-8")
                (references / "python.md").write_text("modified", encoding="utf-8")
                skill = target / "skills" / "personal" / "SKILL.md"
                skill.parent.mkdir(parents=True)
                skill.write_text("personal skill", encoding="utf-8")
                config = target / "config.toml"
                config.write_text("# personal config", encoding="utf-8")
                environment = os.environ.copy()
                environment[variable] = str(target)

                result = subprocess.run(
                    ["bash", str(SYNC_SCRIPT)],
                    input=f"1\n{selection}\n",
                    text=True,
                    capture_output=True,
                    check=False,
                    cwd=ROOT,
                    env=environment,
                )

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assert_directory_equal(ROOT / "rules" / "references", references)
                self.assertEqual(skill.read_text(encoding="utf-8"), "personal skill")
                self.assertEqual(config.read_text(encoding="utf-8"), "# personal config")

    def test_qoder_cn_defaults_to_home_dot_qoder_cn(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            environment = os.environ.copy()
            environment["HOME"] = str(directory)
            environment.pop("QODER_CN_ROOT", None)

            result = subprocess.run(
                ["bash", str(SYNC_SCRIPT)],
                input="rules\nqoder-cn\n",
                text=True,
                capture_output=True,
                check=False,
                cwd=ROOT,
                env=environment,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            target = directory / ".qoder-cn"
            self.assertEqual(
                (target / "AGENTS.md").read_bytes(),
                (ROOT / "rules" / "agents.md").read_bytes(),
            )
            self.assert_directory_equal(
                ROOT / "rules" / "references", target / "references"
            )
            self.assertEqual(list(directory.iterdir()), [target])

    def test_rejects_blank_qoder_cn_root(self) -> None:
        environment = os.environ.copy()
        environment["QODER_CN_ROOT"] = "   "

        result = subprocess.run(
            ["bash", str(SYNC_SCRIPT)],
            input="1\n5\n",
            text=True,
            capture_output=True,
            check=False,
            cwd=ROOT,
            env=environment,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("QODER_CN_ROOT cannot be empty.", result.stderr)

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

    def test_syncs_all_skills_to_qoder_cn_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            qoder_cn_root = directory / ".qoder-cn"
            codex_root = directory / ".codex"
            environment = os.environ.copy()
            environment["QODER_CN_ROOT"] = str(qoder_cn_root)
            environment["CODEX_ROOT"] = str(codex_root)

            result = subprocess.run(
                ["bash", str(SYNC_SCRIPT)],
                input="2\n1\n5\n",
                text=True,
                capture_output=True,
                check=False,
                cwd=ROOT,
                env=environment,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("5) qoder-cn", result.stderr)
            source_skills = ROOT / "skills"
            target_skills = qoder_cn_root / "skills"
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

    def test_syncs_rules_to_opencode_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            opencode_root = directory / ".config" / "opencode"
            codex_root = directory / ".codex"
            workbuddy_root = directory / ".workbuddy"
            environment = os.environ.copy()
            environment["OPENCODE_ROOT"] = str(opencode_root)
            environment["CODEX_ROOT"] = str(codex_root)
            environment["WORKBUDDY_ROOT"] = str(workbuddy_root)

            result = subprocess.run(
                ["bash", str(SYNC_SCRIPT)],
                input="1\n3\n",
                text=True,
                capture_output=True,
                check=False,
                cwd=ROOT,
                env=environment,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(
                "3) opencode -> AGENTS.md + references", result.stderr
            )
            self.assertEqual(
                (opencode_root / "AGENTS.md").read_bytes(),
                (ROOT / "rules" / "agents.md").read_bytes(),
            )

            source_references = ROOT / "rules" / "references"
            target_references = opencode_root / "references"
            self.assert_directory_equal(source_references, target_references)

            self.assertFalse(codex_root.exists())
            self.assertFalse(workbuddy_root.exists())

    def test_syncs_opencode_config_to_opencode_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            opencode_root = directory / ".config" / "opencode"
            environment = os.environ.copy()
            environment["OPENCODE_ROOT"] = str(opencode_root)

            result = subprocess.run(
                ["bash", str(SYNC_SCRIPT)],
                input="3\n2\n",
                text=True,
                capture_output=True,
                check=False,
                cwd=ROOT,
                env=environment,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("2) opencode -> opencode.json", result.stderr)
            self.assertEqual(
                (opencode_root / "opencode.json").read_bytes(),
                (ROOT / "assistants-configs" / "opencode" / "opencode.json").read_bytes(),
            )

    def test_rejects_empty_opencode_root_for_config(self) -> None:
        environment = os.environ.copy()
        environment["OPENCODE_ROOT"] = "   "

        result = subprocess.run(
            ["bash", str(SYNC_SCRIPT)],
            input="3\n2\n",
            text=True,
            capture_output=True,
            check=False,
            cwd=ROOT,
            env=environment,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("OPENCODE_ROOT cannot be empty.", result.stderr)

    def test_syncs_skills_to_opencode_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            opencode_root = directory / ".config" / "opencode"
            codex_root = directory / ".codex"
            workbuddy_root = directory / ".workbuddy"
            environment = os.environ.copy()
            environment["OPENCODE_ROOT"] = str(opencode_root)
            environment["CODEX_ROOT"] = str(codex_root)
            environment["WORKBUDDY_ROOT"] = str(workbuddy_root)

            result = subprocess.run(
                ["bash", str(SYNC_SCRIPT)],
                input="2\n1\n3\n",
                text=True,
                capture_output=True,
                check=False,
                cwd=ROOT,
                env=environment,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            source_skills = ROOT / "skills"
            target_skills = opencode_root / "skills"
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
            self.assertFalse(workbuddy_root.exists())

    def test_syncs_all_skills_to_workbuddy_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            codex_root = directory / ".codex"
            workbuddy_root = directory / ".workbuddy"
            environment = os.environ.copy()
            environment["CODEX_ROOT"] = str(codex_root)
            environment["WORKBUDDY_ROOT"] = str(workbuddy_root)

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


if __name__ == "__main__":
    unittest.main()
