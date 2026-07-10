#!/usr/bin/env python3
"""安全合并 Codex 用户配置，并保留目标中的非受管键。"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomllib

MARKER_VALUE = "__CODEX_CONFIG_SYNC_MARKER__"


@dataclass(frozen=True)
class Assignment:
    """记录一条 TOML 赋值语句及其文本范围。"""

    path: tuple[str, ...]
    table_path: tuple[str, ...]
    start: int
    end: int
    prefix_start: int
    statement: tuple[str, ...]


@dataclass
class Section:
    """记录标准 TOML table 在原文中的范围。"""

    path: tuple[str, ...]
    header: str | None
    content_start: int
    end: int


@dataclass(frozen=True)
class Document:
    """保存 TOML 语义数据与受管键定位信息。"""

    text: str
    lines: tuple[str, ...]
    data: dict[str, Any]
    assignments: tuple[Assignment, ...]
    sections: dict[tuple[str, ...], Section]


def _find_marker(value: Any, path: tuple[str, ...] = ()) -> tuple[str, ...] | None:
    if value == MARKER_VALUE:
        return path
    if isinstance(value, dict):
        for key, child in value.items():
            result = _find_marker(child, (*path, key))
            if result is not None:
                return result
    return None


def _parse_table_path(header: str) -> tuple[str, ...]:
    parsed = tomllib.loads(f"{header}\n__sync_marker__ = {MARKER_VALUE!r}\n")
    marker_path = _find_marker(parsed)
    if marker_path is None or marker_path[-1] != "__sync_marker__":
        raise ValueError(f"无法解析 TOML table: {header}")
    return marker_path[:-1]


def _find_assignment_equals(line: str) -> int | None:
    quote: str | None = None
    escaped = False

    for index, char in enumerate(line):
        if quote is not None:
            if quote == '"' and char == "\\" and not escaped:
                escaped = True
                continue
            if char == quote and not escaped:
                quote = None
            escaped = False
            continue
        if char in {'"', "'"}:
            quote = char
        elif char == "=":
            return index
        elif char == "#":
            return None
    return None


def _parse_assignment_path(header: str | None, lhs: str) -> tuple[str, ...]:
    prefix = f"{header}\n" if header else ""
    parsed = tomllib.loads(f"{prefix}{lhs} = {MARKER_VALUE!r}\n")
    marker_path = _find_marker(parsed)
    if marker_path is None:
        raise ValueError(f"无法解析 TOML key: {lhs}")
    return marker_path


def _statement_end(
    lines: tuple[str, ...], start: int, header: str | None
) -> int:
    prefix = f"{header}\n" if header else ""
    for end in range(start + 1, len(lines) + 1):
        candidate = "".join(lines[start:end])
        try:
            tomllib.loads(f"{prefix}{candidate}")
        except tomllib.TOMLDecodeError:
            continue
        return end
    raise ValueError(f"无法定位第 {start + 1} 行 TOML 赋值语句的结尾")


def _leading_comment_start(
    lines: tuple[str, ...], assignment_start: int, section_start: int
) -> int:
    start = assignment_start
    while start > section_start:
        previous = lines[start - 1].strip()
        if previous and not previous.startswith("#"):
            break
        start -= 1
    return start


def parse_document(text: str, *, description: str) -> Document:
    """解析 TOML，并定位可由模板管理的赋值语句。"""

    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as error:
        raise ValueError(f"{description} 不是有效 TOML: {error}") from error

    lines = tuple(text.splitlines(keepends=True))
    sections: dict[tuple[str, ...], Section] = {
        (): Section(path=(), header=None, content_start=0, end=len(lines))
    }
    assignments: list[Assignment] = []
    current_path: tuple[str, ...] | None = ()
    current_header: str | None = None
    current_section: Section | None = sections[()]
    index = 0

    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith("[[") and stripped.endswith("]]"):
            if current_section is not None:
                current_section.end = index
            current_path = None
            current_header = None
            current_section = None
            index += 1
            continue
        if stripped.startswith("[") and stripped.endswith("]"):
            if current_section is not None:
                current_section.end = index
            current_path = _parse_table_path(stripped)
            current_header = stripped
            current_section = Section(
                path=current_path,
                header=stripped,
                content_start=index + 1,
                end=len(lines),
            )
            sections[current_path] = current_section
            index += 1
            continue
        if (
            not stripped
            or stripped.startswith("#")
            or current_path is None
            or current_section is None
        ):
            index += 1
            continue

        equals_index = _find_assignment_equals(lines[index])
        if equals_index is None:
            index += 1
            continue

        lhs = lines[index][:equals_index].strip()
        end = _statement_end(lines, index, current_header)
        path = _parse_assignment_path(current_header, lhs)
        prefix_start = _leading_comment_start(
            lines, index, section_start=current_section.content_start
        )
        assignments.append(
            Assignment(
                path=path,
                table_path=current_path,
                start=index,
                end=end,
                prefix_start=prefix_start,
                statement=lines[index:end],
            )
        )
        index = end

    if current_section is not None:
        current_section.end = len(lines)
    return Document(
        text=text,
        lines=lines,
        data=data,
        assignments=tuple(assignments),
        sections=sections,
    )


def _deep_merge(base: dict[str, Any], managed: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = dict(base)
    for key, managed_value in managed.items():
        base_value = result.get(key)
        if isinstance(base_value, dict) and isinstance(managed_value, dict):
            result[key] = _deep_merge(base_value, managed_value)
        else:
            result[key] = managed_value
    return result


def _ensure_separated(chunk: str) -> str:
    if not chunk:
        return chunk
    return chunk if chunk.startswith("\n") else f"\n{chunk}"


def merge_text(source_text: str, target_text: str) -> str:
    """用 source 中出现的键覆盖 target，并保留 target 的其他内容。"""

    source = parse_document(source_text, description="源配置")
    target = parse_document(target_text, description="目标配置")
    target_assignments = {item.path: item for item in target.assignments}
    replacements: list[tuple[int, int, tuple[str, ...]]] = []
    missing_by_table: dict[tuple[str, ...], list[Assignment]] = {}

    for managed in source.assignments:
        existing = target_assignments.get(managed.path)
        if existing is not None:
            replacements.append((existing.start, existing.end, managed.statement))
        else:
            missing_by_table.setdefault(managed.table_path, []).append(managed)

    insertions: dict[int, list[str]] = {}
    for table_path, assignments in missing_by_table.items():
        blocks = [
            "".join(source.lines[item.prefix_start : item.end])
            for item in assignments
        ]
        section = target.sections.get(table_path)
        if section is not None:
            chunk = _ensure_separated("".join(blocks))
            insertions.setdefault(section.end, []).append(chunk)
            continue

        source_section = source.sections.get(table_path)
        if source_section is None or source_section.header is None:
            raise ValueError(f"找不到受管 table: {'.'.join(table_path)}")
        chunk = _ensure_separated(
            f"{source_section.header}\n{''.join(blocks).lstrip()}"
        )
        insertions.setdefault(len(target.lines), []).append(chunk)

    edits: list[tuple[int, int, tuple[str, ...]]] = replacements
    for position, chunks in insertions.items():
        edits.append((position, position, ("".join(chunks),)))

    merged_lines = list(target.lines)
    sorted_edits = sorted(edits, key=lambda item: item[0], reverse=True)
    for start, end, replacement in sorted_edits:
        merged_lines[start:end] = replacement
    merged_text = "".join(merged_lines)

    merged = parse_document(merged_text, description="合并结果")
    expected = _deep_merge(target.data, source.data)
    if merged.data != expected:
        raise ValueError(
            "合并结果未完整保留目标配置或未正确覆盖受管键"
        )
    return merged_text


def _atomic_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", dir=destination.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(file_descriptor, "wb") as temporary_file:
            with source.open("rb") as source_file:
                shutil.copyfileobj(source_file, temporary_file)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        temporary_path.chmod(0o600)
        os.replace(temporary_path, destination)
    finally:
        temporary_path.unlink(missing_ok=True)


def _atomic_write(content: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", dir=destination.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8", newline="") as file:
            file.write(content)
            file.flush()
            os.fsync(file.fileno())
        temporary_path.chmod(0o600)
        os.replace(temporary_path, destination)
    finally:
        temporary_path.unlink(missing_ok=True)


def merge_config(source: Path, target: Path) -> Path | None:
    """合并配置到 target，返回生成的备份路径。"""

    if source.resolve() == target.resolve():
        raise ValueError("源配置和目标配置不能是同一个文件")
    if target.is_symlink():
        raise ValueError(f"拒绝覆盖符号链接目标: {target}")

    source_text = source.read_text(encoding="utf-8")
    parse_document(source_text, description=str(source))

    if not target.exists():
        _atomic_write(source_text, target)
        return None

    target_text = target.read_text(encoding="utf-8")
    merged_text = merge_text(source_text, target_text)
    backup = target.with_name(f"{target.name}.backup")
    _atomic_copy(target, backup)
    _atomic_write(merged_text, target)
    return backup


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "合并 Codex 受管配置键，同时保留目标中的本机配置"
        )
    )
    parser.add_argument("source", type=Path, help="受 Git 管理的源配置")
    parser.add_argument("target", type=Path, help="Codex 用户配置目标")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        backup = merge_config(args.source, args.target)
    except (OSError, ValueError) as error:
        print(f"Codex config sync failed: {error}", file=sys.stderr)
        return 1

    if backup is not None:
        print(f"Backed up file -> {backup}")
    print(f"Merged managed config -> {args.target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
