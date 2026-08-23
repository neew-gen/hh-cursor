from __future__ import annotations

from typing import Any


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _parse_scalar(raw: str) -> Any:
    text = raw.strip()
    if text == "null":
        return None
    if text == "true":
        return True
    if text == "false":
        return False
    if text.startswith('"') and text.endswith('"'):
        inner = text[1:-1]
        return inner.replace('\\"', '"').replace("\\\\", "\\")
    if text.isdigit():
        return int(text)
    return text


def _skip_blank(lines: list[str], index: int) -> int:
    while index < len(lines) and not lines[index].strip():
        index += 1
    return index


def _parse_block_scalar(lines: list[str], index: int, base_indent: int) -> tuple[str, int]:
    block_lines: list[str] = []
    content_indent: int | None = None
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            block_lines.append("")
            index += 1
            continue
        line_indent = _indent(line)
        if line_indent <= base_indent:
            break
        if content_indent is None:
            content_indent = line_indent
        if line_indent < content_indent:
            break
        block_lines.append(line[content_indent:])
        index += 1
    return "\n".join(block_lines), index


def _parse_list(lines: list[str], index: int, indent: int) -> tuple[list[Any], int]:
    items: list[Any] = []
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        line_indent = _indent(line)
        if line_indent < indent:
            break
        if line_indent > indent or not line.strip().startswith("- "):
            break

        item_text = line.strip()[2:]
        index += 1
        if ": " in item_text or item_text.endswith(":"):
            key, sep, rest = item_text.partition(":")
            item: dict[str, Any] = {}
            if sep:
                key = key.strip()
                rest = rest.strip()
                if rest == "|":
                    index += 1
                    value, index = _parse_block_scalar(lines, index, line_indent + 2)
                    item[key] = value
                elif rest:
                    item[key] = _parse_scalar(rest)
                else:
                    nested, index = _parse_mapping(lines, index, line_indent + 2)
                    item[key] = nested

            nested_indent = line_indent + 2
            while index < len(lines):
                next_line = lines[index]
                if not next_line.strip():
                    index += 1
                    continue
                next_indent = _indent(next_line)
                if next_indent < nested_indent:
                    break
                if next_line.strip().startswith("- "):
                    break
                nested_key, sep, nested_rest = next_line.strip().partition(":")
                if not sep:
                    index += 1
                    continue
                nested_key = nested_key.strip()
                nested_rest = nested_rest.strip()
                if nested_rest == "|":
                    index += 1
                    value, index = _parse_block_scalar(lines, index, next_indent)
                elif nested_rest == "":
                    index = _skip_blank(lines, index)
                    if index >= len(lines):
                        value = []
                    elif lines[index].strip().startswith("- "):
                        value, index = _parse_list(lines, index, _indent(lines[index]))
                    else:
                        value, index = _parse_mapping(lines, index, next_indent + 2)
                else:
                    value = _parse_scalar(nested_rest)
                    index += 1
                item[nested_key] = value
            items.append(item)
        else:
            items.append(_parse_scalar(item_text))
    return items, index


def _parse_mapping(lines: list[str], index: int, indent: int) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        line_indent = _indent(line)
        if line_indent < indent:
            break
        if line_indent > indent:
            break
        if line.strip().startswith("- "):
            break

        key, sep, rest = line.strip().partition(":")
        if not sep:
            index += 1
            continue
        key = key.strip()
        rest = rest.strip()
        if rest == "|":
            index += 1
            value, index = _parse_block_scalar(lines, index, indent)
        elif rest == "":
            index += 1
            index = _skip_blank(lines, index)
            if index >= len(lines):
                result[key] = []
                break
            next_line = lines[index]
            next_indent = _indent(next_line)
            if next_indent <= indent and not next_line.strip().startswith("- "):
                result[key] = []
                continue
            if next_line.strip().startswith("- "):
                value, index = _parse_list(lines, index, next_indent)
            else:
                value, index = _parse_mapping(lines, index, next_indent)
        else:
            value = _parse_scalar(rest)
            index += 1
        result[key] = value
    return result, index


def parse_artifact_yaml(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    data, _ = _parse_mapping(lines, 0, 0)
    return data
