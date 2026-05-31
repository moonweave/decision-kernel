# Architecture

## Source Of Truth

This repository owns the editable source for:

- `skills/anneal`
- `skills/compass`
- `skills/decide`

Do not edit installed copies directly. Local installs are generated from this
repository.

## Install Policy

Claude installs prefer symlinks:

```text
~/.claude/skills/<name> -> <repo>/skills/<name>
```

This keeps Claude Code pointed at the editable source.

Codex installs are sanitized copies:

```text
~/.codex/skills/<name>
```

Codex skill metadata support differs from Claude Code metadata support, so
`scripts/install.py --target codex` rewrites `SKILL.md` frontmatter to keep only
`name` and `description` while preserving the body unchanged.

## Shared Logic

Common behavior belongs in repository scripts, not in runtime dependencies
between skill folders. A skill folder should remain installable by itself.

Use `scripts/validate.py` for structural checks, `scripts/install.py` for local
deployment, and `scripts/smoke.py` for repeatable smoke verification.

## Migration Policy

The original individual repos remain preserved as rollback points. Once this
monorepo has been used for multiple successful changes, they can be archived
manually.
