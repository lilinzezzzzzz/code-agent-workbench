from __future__ import annotations

import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import merge_codex_config  # noqa: E402


class MergeCodexConfigTest(unittest.TestCase):
    def test_merge_updates_managed_keys_and_preserves_target_only_content(self) -> None:
        source_text = """\
# 源配置注释
model = "gpt-5.6-terra"

[sandbox_workspace_write]
writable_roots = ["/tmp"]

[features]
memories = false
"""
        target_text = """\
# 目标配置注释
model = "gpt-5.6-sol"
service_tier = "default"

[sandbox_workspace_write]
writable_roots = [
  "/workspace",
]
network_access = false

[features]
memories = true
desktop_state = true

[desktop]
localeOverride = "zh-CN"

[projects."/Users/example/project"]
trust_level = "trusted"
"""

        merged_text = merge_codex_config.merge_text(source_text, target_text)
        merged = merge_codex_config.tomllib.loads(merged_text)

        self.assertEqual(merged["model"], "gpt-5.6-terra")
        self.assertEqual(merged["service_tier"], "default")
        self.assertEqual(
            merged["sandbox_workspace_write"]["writable_roots"], ["/tmp"]
        )
        self.assertFalse(merged["features"]["memories"])
        self.assertTrue(merged["features"]["desktop_state"])
        self.assertEqual(merged["desktop"]["localeOverride"], "zh-CN")
        self.assertEqual(
            merged["projects"]["/Users/example/project"]["trust_level"],
            "trusted",
        )
        self.assertIn("# 目标配置注释", merged_text)

    def test_merge_creates_backup_and_keeps_private_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            source = directory / "source.toml"
            target = directory / "config.toml"
            source.write_text('model = "gpt-5.6-terra"\n', encoding="utf-8")
            original = 'model = "gpt-5.6-sol"\nlocal_only = true\n'
            target.write_text(original, encoding="utf-8")
            target.chmod(0o644)

            backup = merge_codex_config.merge_config(source, target)

            self.assertEqual(backup, directory / "config.toml.backup")
            self.assertEqual(backup.read_text(encoding="utf-8"), original)
            self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(backup.stat().st_mode), 0o600)
            merged = merge_codex_config.tomllib.loads(
                target.read_text(encoding="utf-8")
            )
            self.assertEqual(merged["model"], "gpt-5.6-terra")
            self.assertTrue(merged["local_only"])

    def test_merge_adds_missing_keys_and_tables(self) -> None:
        source_text = """\
model = "gpt-5.6-terra"

[features]
memories = false
# 新增受管键
chronicle = false

[agents]
max_threads = 3
"""
        target_text = """\
model = "gpt-5.6-sol"

[features]
memories = true

[desktop]
local_marker = "keep-me"
"""

        merged_text = merge_codex_config.merge_text(source_text, target_text)
        merged = merge_codex_config.tomllib.loads(merged_text)

        self.assertFalse(merged["features"]["chronicle"])
        self.assertEqual(merged["agents"]["max_threads"], 3)
        self.assertEqual(merged["desktop"]["local_marker"], "keep-me")
        self.assertIn("# 新增受管键", merged_text)

    def test_missing_target_is_created_without_backup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            source = directory / "source.toml"
            target = directory / "config.toml"
            source_text = 'model = "gpt-5.6-terra"\n'
            source.write_text(source_text, encoding="utf-8")

            backup = merge_codex_config.merge_config(source, target)

            self.assertIsNone(backup)
            self.assertEqual(target.read_text(encoding="utf-8"), source_text)
            self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)
            self.assertFalse((directory / "config.toml.backup").exists())

    def test_invalid_source_does_not_touch_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            source = directory / "source.toml"
            target = directory / "config.toml"
            source.write_text("model = [\n", encoding="utf-8")
            original = 'model = "gpt-5.6-sol"\n'
            target.write_text(original, encoding="utf-8")

            with self.assertRaises(ValueError):
                merge_codex_config.merge_config(source, target)

            self.assertEqual(target.read_text(encoding="utf-8"), original)
            self.assertFalse((directory / "config.toml.backup").exists())

    def test_invalid_target_does_not_create_backup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            source = directory / "source.toml"
            target = directory / "config.toml"
            source.write_text('model = "gpt-5.6-terra"\n', encoding="utf-8")
            original = "model = [\n"
            target.write_text(original, encoding="utf-8")

            with self.assertRaises(ValueError):
                merge_codex_config.merge_config(source, target)

            self.assertEqual(target.read_text(encoding="utf-8"), original)
            self.assertFalse((directory / "config.toml.backup").exists())

    def test_sync_agents_config_flow_preserves_local_sections(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            codex_root = Path(temporary_directory) / ".codex"
            codex_root.mkdir()
            target = codex_root / "config.toml"
            original = """\
model = "gpt-5.6-sol"

[desktop]
local_marker = "keep-me"
"""
            target.write_text(original, encoding="utf-8")
            environment = os.environ.copy()
            environment["CODEX_ROOT"] = str(codex_root)
            environment["PYTHONDONTWRITEBYTECODE"] = "1"

            result = subprocess.run(
                ["bash", str(ROOT / "sync-agents.sh")],
                input="3\n",
                text=True,
                capture_output=True,
                check=False,
                cwd=ROOT,
                env=environment,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            merged = merge_codex_config.tomllib.loads(
                target.read_text(encoding="utf-8")
            )
            self.assertEqual(merged["model"], "gpt-5.6-terra")
            self.assertEqual(merged["desktop"]["local_marker"], "keep-me")
            self.assertEqual(
                (codex_root / "config.toml.backup").read_text(encoding="utf-8"),
                original,
            )
            self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)


if __name__ == "__main__":
    unittest.main()
