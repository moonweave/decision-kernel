# AGENTS.md

- Treat `skills/<name>/SKILL.md` as the source of truth.
- Do not edit `~/.claude/skills` or `~/.codex/skills` copies directly.
- Run `python3 scripts/validate.py` before reporting completion.
- Use `python3 scripts/install.py --target claude` for Claude installs.
- Use `python3 scripts/install.py --target codex` for Codex installs.
- Do not add runtime cross-skill dependencies from one skill folder to another.
- Keep each skill self-contained so it can be installed as a standalone folder.
- Preserve existing individual repos until this monorepo has been used successfully for several changes.
