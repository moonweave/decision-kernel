#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("anneal", "compass", "decide")
CLAUDE_DIR = Path.home() / ".claude" / "skills"
CODEX_DIR = Path.home() / ".codex" / "skills"


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("unclosed frontmatter")
    return text[4:end], text[end + len("\n---\n") :]


def keep_name_description(raw: str) -> str:
    lines = raw.splitlines()
    kept: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("name:"):
            kept.append(line)
            i += 1
            continue
        if line.startswith("description:"):
            kept.append(line)
            i += 1
            while i < len(lines) and (not lines[i] or lines[i].startswith((" ", "\t"))):
                kept.append(lines[i])
                i += 1
            continue
        i += 1
    if not any(line.startswith("name:") for line in kept):
        raise ValueError("frontmatter missing name")
    if not any(line.startswith("description:") for line in kept):
        raise ValueError("frontmatter missing description")
    return "\n".join(kept)


def backup_existing(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = path.parent / ".backup"
    backup_dir.mkdir(parents=True, exist_ok=True)
    destination = backup_dir / f"{path.name}-{timestamp}"
    shutil.move(str(path), str(destination))
    print(f"backed up {path} -> {destination}")


def install_claude() -> None:
    CLAUDE_DIR.mkdir(parents=True, exist_ok=True)
    for name in SKILLS:
        source = ROOT / "skills" / name
        target = CLAUDE_DIR / name
        if not source.exists():
            raise FileNotFoundError(source)
        backup_existing(target)
        target.symlink_to(source)
        print(f"claude {name}: {target} -> {source}")


def ignore_names(_: str, names: list[str]) -> set[str]:
    return {name for name in names if name in {".git", ".ruff_cache", "__pycache__"}}


def sanitize_codex_skill(skill_dir: Path) -> None:
    skill_path = skill_dir / "SKILL.md"
    text = skill_path.read_text()
    raw, body = split_frontmatter(text)
    sanitized = f"---\n{keep_name_description(raw)}\n---\n{body}"
    skill_path.write_text(sanitized)


def install_codex() -> None:
    CODEX_DIR.mkdir(parents=True, exist_ok=True)
    for name in SKILLS:
        source = ROOT / "skills" / name
        target = CODEX_DIR / name
        if not source.exists():
            raise FileNotFoundError(source)
        backup_existing(target)
        shutil.copytree(source, target, ignore=ignore_names)
        sanitize_codex_skill(target)
        print(f"codex {name}: copied sanitized skill to {target}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=("claude", "codex", "all"), required=True)
    args = parser.parse_args()
    if args.target in {"claude", "all"}:
        install_claude()
    if args.target in {"codex", "all"}:
        install_codex()


if __name__ == "__main__":
    main()
