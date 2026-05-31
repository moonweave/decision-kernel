#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "anneal": ["Bound \"fixable\"", "Stop rule"],
    "compass": ["Portable macOS/Linux", "unverified"],
    "decide": ["current repo, project, codebase", "A clear standard requires at least two"],
}
PLACEHOLDERS = [
    "T" + "BD",
    "implement " + "later",
    "fill in " + "details",
    "Add " + "appropriate",
    "Write tests " + "for the above",
    "Similar " + "to Task",
]


def fail(message: str) -> None:
    print(f"validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def split_frontmatter(path: Path) -> tuple[str, str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)} missing frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        fail(f"{path.relative_to(ROOT)} has unclosed frontmatter")
    return text[4:end], text[end + len("\n---\n") :]


def parse_scalar_keys(raw: str) -> dict[str, str]:
    values: dict[str, str] = {}
    lines = raw.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("name:"):
            values["name"] = line.split(":", 1)[1].strip().strip('"')
        if line.startswith("description:"):
            value = line.split(":", 1)[1].strip()
            if value and value != "|":
                values["description"] = value.strip('"')
            elif value == "|":
                block: list[str] = []
                for next_line in lines[i + 1 :]:
                    if next_line and not next_line.startswith((" ", "\t")):
                        break
                    block.append(next_line.strip())
                values["description"] = "\n".join(block).strip()
        if line.startswith("disable-model-invocation:"):
            values["disable-model-invocation"] = line.split(":", 1)[1].strip()
        if line.startswith("argument-hint:"):
            values["argument-hint"] = line.split(":", 1)[1].strip()
    return values


def validate_skill(name: str, markers: list[str]) -> None:
    skill_dir = ROOT / "skills" / name
    skill_path = skill_dir / "SKILL.md"
    if not skill_path.exists():
        fail(f"missing {skill_path.relative_to(ROOT)}")
    raw, body = split_frontmatter(skill_path)
    meta = parse_scalar_keys(raw)
    if not meta.get("name"):
        fail(f"{skill_path.relative_to(ROOT)} missing name")
    if not meta.get("description"):
        fail(f"{skill_path.relative_to(ROOT)} missing description")
    if meta.get("disable-model-invocation") != "true":
        fail(f"{skill_path.relative_to(ROOT)} missing disable-model-invocation: true")
    if "argument-hint" not in meta:
        fail(f"{skill_path.relative_to(ROOT)} missing argument-hint")
    text = raw + "\n" + body
    for marker in markers:
        if marker not in text:
            fail(f"{skill_path.relative_to(ROOT)} missing marker: {marker}")


def validate_placeholders() -> None:
    for path in sorted(ROOT.rglob("*")):
        if ".git" in path.parts:
            continue
        if path.suffix not in {".md", ".py"}:
            continue
        text = path.read_text(errors="ignore")
        for marker in PLACEHOLDERS:
            if marker in text:
                fail(f"{path.relative_to(ROOT)} contains placeholder marker {marker!r}")


def main() -> None:
    for name, markers in SKILLS.items():
        validate_skill(name, markers)
    validate_placeholders()
    print("validation ok")


if __name__ == "__main__":
    main()
