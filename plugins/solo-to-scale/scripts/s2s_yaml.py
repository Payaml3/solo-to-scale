"""A tiny YAML-subset reader (standard library only) for the plugin's own files.

Supported: `key: scalar`, `key: |` block text, and `key:` followed by an indented list (`- item`)
or an indented one-level map (`sub: value`). Whole-line comments start with `#`.
It is not a general YAML parser: the plugin's files are written to fit it, and tests hold them to it.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def _scalar(text: str) -> Any:
    t = text.strip()
    if len(t) >= 2 and t[0] == t[-1] and t[0] in "\"'":
        return t[1:-1]
    if t in ("true", "false"):
        return t == "true"
    if t in ("null", "~", ""):
        return None
    try:
        return int(t)
    except ValueError:
        return t


def loads(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    out: dict[str, Any] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if line[0] in " \t":
            raise ValueError(f"line {i + 1}: unexpected indentation: {line!r}")
        key, sep, rest = line.partition(":")
        if not sep:
            raise ValueError(f"line {i + 1}: expected 'key: value': {line!r}")
        key, rest = key.strip(), rest.strip()
        if key in out:
            raise ValueError(f"line {i + 1}: duplicate key {key!r}")
        i += 1
        if rest in ("|", "|-"):
            block: list[str] = []
            while i < len(lines) and (not lines[i].strip() or lines[i].startswith("  ")):
                block.append(lines[i][2:] if lines[i].startswith("  ") else "")
                i += 1
            out[key] = "\n".join(block).strip("\n")
            continue
        if rest:
            out[key] = _scalar(rest)
            continue
        items: list[Any] = []
        mapping: dict[str, Any] = {}
        while i < len(lines) and (not lines[i].strip() or lines[i].startswith((" ", "\t"))):
            sub = lines[i].strip()
            i += 1
            if not sub or sub.startswith("#"):
                continue
            if sub.startswith("- "):
                items.append(_scalar(sub[2:]))
            else:
                k, s, v = sub.partition(":")
                if not s:
                    raise ValueError(f"line {i}: expected '- item' or 'key: value': {sub!r}")
                mapping[k.strip()] = _scalar(v)
        if items and mapping:
            raise ValueError(f"key {key!r} mixes a list and a map")
        out[key] = items or mapping or None
    return out


def load(path: Path) -> dict[str, Any]:
    return loads(Path(path).read_text(encoding="utf-8"))
