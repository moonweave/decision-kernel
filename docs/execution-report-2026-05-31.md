# Execution Report - 2026-05-31

## Summary

Created `decision-kernel` as the source-of-truth monorepo for `anneal`,
`compass`, and `decide`.

## Completed

- Copied current skill sources into `skills/anneal`, `skills/compass`, and `skills/decide`.
- Excluded nested `.git` directories and volatile cache directories.
- Added repository docs: `README.md`, `AGENTS.md`, `docs/architecture.md`, and `docs/skill-catalog.md`.
- Added validation, install, and smoke scripts under `scripts/`.
- Installed Claude skills as symlinks to the monorepo source.
- Installed Codex skills as sanitized copies with only `name` and `description` frontmatter.
- Preserved previous installed `anneal` directories in `.backup` folders.

## Verification

```text
python3 scripts/validate.py
validation ok

python3 scripts/smoke.py --local-only
validation ok
smoke local ok
```

Installed Claude paths:

```text
~/.claude/skills/anneal -> ~/ai-skills-dev/decision-kernel/skills/anneal
~/.claude/skills/compass -> ~/ai-skills-dev/decision-kernel/skills/compass
~/.claude/skills/decide -> ~/ai-skills-dev/decision-kernel/skills/decide
```

Installed Codex paths:

```text
~/.codex/skills/anneal
~/.codex/skills/compass
~/.codex/skills/decide
```

## Live Claude Smoke

`python3 scripts/smoke.py` attempted all three slash prompts through the local
`claude` CLI. Each prompt was blocked before skill execution:

```text
Your organization has disabled Claude subscription access for Claude Code
```

This is an account or organization policy blocker, not a monorepo validation
failure.

## Preserved Sources

The original individual repos remain in place:

```text
~/ai-skills-dev/my-skills/anneal-skill
~/ai-skills-dev/my-skills/compass-skill
~/ai-skills-dev/my-skills/decide-skill
```
