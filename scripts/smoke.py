#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ("anneal", "compass", "decide")
ORG_POLICY_MARKER = "Your organization has disabled Claude subscription access for Claude Code"


def run_validate() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate.py")],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(result.stdout, end="")
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def run_claude_prompt(claude: str, prompt_path: Path) -> int:
    prompt = prompt_path.read_text().strip()
    result = subprocess.run(
        [
            claude,
            "--print",
            "--no-session-persistence",
            "--max-budget-usd",
            "0.20",
            prompt,
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )
    print(f"--- {prompt_path.name} exit={result.returncode} ---")
    print(result.stdout)
    if ORG_POLICY_MARKER in result.stdout:
        return 2
    return result.returncode


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local-only", action="store_true")
    args = parser.parse_args()

    run_validate()
    if args.local_only:
        print("smoke local ok")
        return

    claude = shutil.which("claude")
    if not claude:
        print("claude CLI not found")
        raise SystemExit(2)

    blocked = False
    failed = False
    for name in PROMPTS:
        code = run_claude_prompt(claude, ROOT / "tests" / "smoke" / f"{name}.md")
        if code == 2:
            blocked = True
        elif code != 0:
            failed = True

    if blocked:
        raise SystemExit(2)
    if failed:
        raise SystemExit(1)
    print("smoke live ok")


if __name__ == "__main__":
    main()
