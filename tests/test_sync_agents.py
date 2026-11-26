from __future__ import annotations

import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SYNC_SCRIPT = ROOT / "sync-agents.sh"


class SyncAgentRulesTest(unittest.TestCase):
    def test_reference_routes_resolve_to_grouped_files(self) -> None:
        agents = (ROOT / "rules" / "baseline.md").read_text(encoding="utf-8")
        routes = re.findall(r"^\| `([^`]+\.md)` \|", agents, re.MULTILINE)
        references = ROOT / "rules" / "references"
        actual = {
            path.relative_to(references).as_posix()
            for path in references.rglob("*.md")
        }
        self.assertTrue(routes)
        self.assertEqual(len(routes), len(set(routes)))
        self.assertEqual(set(routes), actual)
        for route in routes:
            self.assertEqual(len(Path(route).parts), 2, route)
        for path in references.rglob("*.md"):
            cross_references = re.findall(
                r"`([^`\n]+\.md)`", path.read_text(encoding="utf-8")
            )
            for reference in cross_references:
                self.assertIn(reference, actual, f"{path}: {reference}")

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

    def assert_agents_file(self, target_root: Path) -> None:
        contents = (target_root / "AGENTS.md").read_bytes()
        metadata, separator, body = contents.partition(b"\n\n")
        self.assertEqual(separator, b"\n\n")
        entries = re.findall(
            r"^(Instruction file|Reference root): (.+)$",
            metadata.decode("utf-8"),
            re.MULTILINE,
        )
        self.assertEqual(len(entries), 2)
        absolute_root = target_root.resolve()
        self.assertEqual(
            dict(entries),
            {
                "Instruction file": str(absolute_root / "AGENTS.md"),
                "Reference root": f"{absolute_root / 'references'}/",
            },
        )
        self.assertEqual(body, (ROOT / "rules" / "baseline.md").read_bytes())

    def test_rules_metadata_uses_absolute_paths_and_is_stable(self) -> None:
        root_names = ("relative assistant", "规则 $(touch injected) `literal` '& root")
        for root_name in root_names:
            with (
                self.subTest(root=root_name),
                tempfile.TemporaryDirectory() as temporary_directory,
            ):
                directory = Path(temporary_directory)
                target = directory / root_name
                environment = os.environ.copy()
                environment["CODEX_ROOT"] = root_name
                installed_contents = []

                for _ in range(2):
                    result = subprocess.run(
                        ["bash", str(SYNC_SCRIPT)],
                        input="rules\ncodex\n",
                        text=True,
                        capture_output=True,
                        check=False,
                        cwd=directory,
                        env=environment,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assert_agents_file(target)
                    installed_contents.append((target / "AGENTS.md").read_bytes())

                self.assertEqual(installed_contents[0], installed_contents[1])
                self.assertFalse((directory / "injected").exists())
                self.assert_directory_equal(
                    ROOT / "rules" / "references", target / "references"
                )

    def test_rules_metadata_uses_physical_installation_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            physical_root = directory / "physical root"
            physical_root.mkdir()
            linked_root = directory / "linked root"
            linked_root.symlink_to(physical_root, target_is_directory=True)
            environment = os.environ.copy()
            environment["CODEX_ROOT"] = str(linked_root)

            result = subprocess.run(
                ["bash", str(SYNC_SCRIPT)],
                input="rules\ncodex\n",
                text=True,
                capture_output=True,
                check=False,
                cwd=ROOT,
                env=environment,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assert_agents_file(linked_root)
            self.assertTrue(linked_root.is_symlink())

    def test_rules_metadata_rejects_line_breaks_in_installation_path(self) -> None:
        for root_name in ("assistant\nroot", "assistant\rroot", "assistant\n"):
            with (
                self.subTest(root=root_name),
                tempfile.TemporaryDirectory() as temporary_directory,
            ):
                directory = Path(temporary_directory)
                target = directory / root_name
                target.mkdir()
                linked_root = directory / "linked root"
                linked_root.symlink_to(target, target_is_directory=True)

                for configured_root in (target, linked_root):
                    with self.subTest(configured_root=str(configured_root)):
                        environment = os.environ.copy()
                        environment["CODEX_ROOT"] = f"{configured_root}/."
                        result = subprocess.run(
                            ["bash", str(SYNC_SCRIPT)],
                            input="rules\ncodex\n",
                            text=True,
                            capture_output=True,
                            check=False,
                            cwd=ROOT,
                            env=environment,
                        )

                        self.assertEqual(result.returncode, 1)
                        self.assertIn(
                            "Rules target path cannot contain line breaks.",
                            result.stderr,
                        )
                        self.assertFalse((target / "AGENTS.md").exists())

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
            self.assert_agents_file(workbuddy_root)

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
            self.assert_agents_file(codex_root)
            self.assert_agents_file(workbuddy_root)
            self.assert_directory_equal(
                codex_root / "references", workbuddy_root / "references"
            )

    def test_rules_mirror_references_without_removing_sibling_content(self) -> None:
        targets = (
            ("CODEX_ROOT", "1"),
            ("WORKBUDDY_ROOT", "2"),
            ("OPENCODE_ROOT", "3"),
            ("ZCODE_ROOT", "4"),
            ("QODER_CN_ROOT", "5"),
            ("HOME", "6"),
        )
        for variable, selection in targets:
            with self.subTest(target=variable), tempfile.TemporaryDirectory() as temporary_directory:
                target = Path(temporary_directory) / (".dsh" if selection == "6" else "assistant root")
                references = target / "references"
                obsolete = references / "obsolete"
                obsolete.mkdir(parents=True)
                (obsolete / "nested.md").write_text("obsolete", encoding="utf-8")
                (references / "ai-rag.md").write_text("legacy", encoding="utf-8")
                (references / ".custom").write_text("hidden", encoding="utf-8")
                for source in (ROOT / "rules" / "references").rglob("*.md"):
                    (references / source.name).write_text("legacy", encoding="utf-8")
                stale_nested = references / "languages" / "obsolete.md"
                stale_nested.parent.mkdir()
                stale_nested.write_text("obsolete", encoding="utf-8")
                legacy_git = references / "git" / "git-workflow.md"
                legacy_git.parent.mkdir()
                legacy_git.write_text("legacy grouped path", encoding="utf-8")
                (references / "git-workflow.md").write_text("legacy flat path", encoding="utf-8")
                skill = target / "skills" / "personal" / "SKILL.md"
                skill.parent.mkdir(parents=True)
                skill.write_text("personal skill", encoding="utf-8")
                config = target / "config.toml"
                config.write_text("# personal config", encoding="utf-8")
                environment = os.environ.copy()
                environment[variable] = temporary_directory if selection == "6" else str(target)

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
                self.assert_agents_file(target)
                self.assertEqual(skill.read_text(encoding="utf-8"), "personal skill")
                self.assertEqual(config.read_text(encoding="utf-8"), "# personal config")

    def test_syncs_rules_to_dsh_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            dsh_root = directory / ".dsh"
            codex_root = directory / ".codex"
            environment = os.environ.copy()
            environment["HOME"] = str(directory)
            environment["CODEX_ROOT"] = str(codex_root)

            result = subprocess.run(
                ["bash", str(SYNC_SCRIPT)],
                input="1\n6\n",
                text=True,
                capture_output=True,
                check=False,
                cwd=ROOT,
                env=environment,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("6) dsh -> AGENTS.md + references", result.stderr)
            self.assert_agents_file(dsh_root)
            self.assert_directory_equal(
                ROOT / "rules" / "references", dsh_root / "references"
            )
            self.assertFalse(codex_root.exists())

    def test_dsh_rules_aliases(self) -> None:
        for target in ("deepseek", "deepseek-harness"):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as directory:
                environment = os.environ.copy()
                environment["HOME"] = directory
                result = subprocess.run(
                    ["bash", str(SYNC_SCRIPT)],
                    input=f"rules\n{target}\n",
                    text=True,
                    capture_output=True,
                    check=False,
                    cwd=ROOT,
                    env=environment,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assert_agents_file(Path(directory) / ".dsh")

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
            self.assert_agents_file(target)
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
            self.assert_agents_file(workbuddy_root)
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

    def test_reports_empty_skill_directory_before_sync(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory).resolve()
            script = directory / "sync-agents.sh"
            script.write_bytes(SYNC_SCRIPT.read_bytes())
            for name in ("rules", "configs"):
                (directory / name).symlink_to(ROOT / name, target_is_directory=True)
            skills = directory / "skills"
            (skills / "_shared").mkdir(parents=True)
            (skills / "targets.conf").touch()
            target = directory / "target"

            result = subprocess.run(
                ["/bin/bash", str(script)],
                input="skills\n1\n1\n",
                text=True,
                capture_output=True,
                env={**os.environ, "CODEX_ROOT": str(target)},
                timeout=10,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn(
                f"No compatible skills found for codex under: {skills}", result.stderr
            )
            self.assertFalse(target.exists())

    def test_syncs_only_the_skill_selected_by_menu_number(self) -> None:
        source_skills = ROOT / "skills"
        skills = sorted(
            path for path in source_skills.iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        )
        self.assertTrue(skills)
        for menu_number, skill in enumerate(skills, start=2):
            with self.subTest(skill=skill.name), tempfile.TemporaryDirectory() as temporary_directory:
                target = Path(temporary_directory) / "assistant root"
                environment = os.environ.copy()
                environment["CODEX_ROOT"] = str(target)

                result = subprocess.run(
                    ["bash", str(SYNC_SCRIPT)],
                    input=f"2\n1\n{menu_number}\n",
                    text=True,
                    capture_output=True,
                    check=False,
                    cwd=ROOT,
                    env=environment,
                    timeout=10,
                )

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(f"{menu_number}) {skill.name}", result.stderr)
                target_skills = target / "skills"
                self.assertEqual(
                    sorted(path.name for path in target_skills.iterdir()),
                    sorted(["_shared", skill.name]),
                )
                self.assert_directory_equal(skill, target_skills / skill.name)
                self.assert_directory_equal(
                    source_skills / "_shared", target_skills / "_shared"
                )

    def test_syncs_all_compatible_skills_to_each_target(self) -> None:
        targets = {
            "codex": "CODEX_ROOT",
            "workbuddy": "WORKBUDDY_ROOT",
            "opencode": "OPENCODE_ROOT",
            "zcode": "ZCODE_ROOT",
            "qoder-cn": "QODER_CN_ROOT",
            "dsh": None,
        }
        expected_menu = "\n".join(
            f"{number}) {option}"
            for number, option in enumerate([*targets, "exit"], start=1)
        )
        source_skills = ROOT / "skills"
        skill_directories = [
            path for path in source_skills.iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        ]
        codex_only = {
            "create-project-worktree",
            "rename-worktree-chat",
            "worktree-environment-setup",
        }

        for menu_number, target in enumerate(targets, start=1):
            with (
                self.subTest(target=target),
                tempfile.TemporaryDirectory() as temporary_directory,
            ):
                directory = Path(temporary_directory)
                environment = {
                    **os.environ,
                    "HOME": str(directory),
                    "COLUMNS": "200",
                }
                target_roots = {"dsh": directory / ".dsh"}
                for name, variable in targets.items():
                    if variable:
                        target_roots[name] = directory / "configured" / name
                        environment[variable] = str(target_roots[name])

                result = subprocess.run(
                    ["bash", str(SYNC_SCRIPT)],
                    input=f"2\n{menu_number}\n1\n",
                    text=True,
                    capture_output=True,
                    env=environment,
                    timeout=10,
                )

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(expected_menu + "\n", result.stderr)
                self.assertEqual(
                    {name for name, root in target_roots.items() if root.exists()},
                    {target},
                )
                target_skills = target_roots[target] / "skills"
                compatible = [
                    path for path in skill_directories
                    if target == "codex" or path.name not in codex_only
                ]
                expected = [source_skills / "_shared", *compatible]
                self.assertEqual(
                    {path.name for path in target_skills.iterdir()},
                    {path.name for path in expected},
                )
                for skill in codex_only:
                    if target == "codex":
                        self.assertIn(skill, result.stderr)
                    else:
                        self.assertNotIn(skill, result.stderr)
                for path in expected:
                    self.assert_directory_equal(path, target_skills / path.name)

    def test_skill_target_allowlist_accepts_multiple_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            script = directory / "sync-agents.sh"
            script.write_bytes(SYNC_SCRIPT.read_bytes())
            for name in ("rules", "configs"):
                (directory / name).symlink_to(ROOT / name, target_is_directory=True)
            skills = directory / "skills"
            (skills / "_shared").mkdir(parents=True)
            (skills / "example-skill").mkdir()
            (skills / "example-skill" / "SKILL.md").touch()
            policy = skills / "targets.conf"
            policy.write_text("example-skill codex opencode\n", encoding="utf-8")
            cases = (
                (1, "CODEX_ROOT", True),
                (2, "WORKBUDDY_ROOT", False),
                (3, "OPENCODE_ROOT", True),
            )
            for menu_number, variable, allowed in cases:
                with self.subTest(variable=variable):
                    target = directory / variable
                    result = subprocess.run(
                        ["/bin/bash", str(script)],
                        input=f"skills\n{menu_number}\n1\n",
                        text=True,
                        capture_output=True,
                        env={**os.environ, variable: str(target)},
                        timeout=10,
                    )
                    self.assertEqual(
                        result.returncode, 0 if allowed else 1, result.stderr
                    )
                    if allowed:
                        installed_skill = target / "skills" / "example-skill" / "SKILL.md"
                        self.assertTrue(installed_skill.is_file())
                    else:
                        self.assertIn(
                            "No compatible skills found for workbuddy", result.stderr
                        )
                        self.assertFalse(target.exists())

            policy.write_text("example-skill codex typo\n", encoding="utf-8")
            target = directory / "invalid-target"

            result = subprocess.run(
                ["/bin/bash", str(script)],
                input="skills\n1\n1\n",
                text=True,
                capture_output=True,
                env={**os.environ, "CODEX_ROOT": str(target)},
                timeout=10,
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn(
                f"Unknown target for example-skill in {policy}: typo", result.stderr
            )
            self.assertFalse(target.exists())

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
            self.assert_agents_file(opencode_root)

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
            self.assertIn("2) opencode -> opencode.jsonc", result.stderr)
            self.assertEqual(
                (opencode_root / "opencode.jsonc").read_bytes(),
                (ROOT / "configs" / "opencode" / "opencode.jsonc").read_bytes(),
            )

    def test_aborts_when_stdin_closes_at_any_menu(self) -> None:
        cases = {
            "content": "",
            "rules target": "1\n",
            "config target": "3\n",
            "skill target": "2\n",
            "skill selection": "2\n1\n",
        }

        for label, input_text in cases.items():
            with self.subTest(menu=label), tempfile.TemporaryDirectory() as temporary_directory:
                environment = os.environ.copy()
                environment["CODEX_ROOT"] = str(Path(temporary_directory) / ".codex")
                environment["WORKBUDDY_ROOT"] = str(
                    Path(temporary_directory) / ".workbuddy"
                )
                environment["OPENCODE_ROOT"] = str(
                    Path(temporary_directory) / ".config" / "opencode"
                )
                environment["ZCODE_ROOT"] = str(Path(temporary_directory) / ".zcode")
                environment["QODER_CN_ROOT"] = str(
                    Path(temporary_directory) / ".qoder-cn"
                )

                result = subprocess.run(
                    ["bash", str(SYNC_SCRIPT)],
                    input=input_text,
                    text=True,
                    capture_output=True,
                    check=False,
                    cwd=ROOT,
                    env=environment,
                )

                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(
                    "Standard input is closed (EOF); aborting.", result.stderr
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


if __name__ == "__main__":
    unittest.main()
