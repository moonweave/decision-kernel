# Decision Kernel

Measure forks. Audit drift. Decide with evidence.

Decision Kernel is a compact operating layer for agent judgment. It gives
agents three disciplined moves before they commit work:

- `anneal`: compare candidate approaches with cheap measurable fitness before committing.
- `compass`: audit session drift and codebase rot against local evidence.
- `decide`: make or escalate technical decisions with local preflight and source-backed evidence.

The implementation is still a set of Claude/Codex skill folders, but the repo is
positioned as a decision protocol kernel rather than a loose skill collection.

## Commands

```bash
python3 scripts/validate.py
python3 scripts/install.py --target claude
python3 scripts/install.py --target codex
python3 scripts/smoke.py --local-only
```

## Layout

```text
skills/
  anneal/
  compass/
  decide/
scripts/
  validate.py
  install.py
  smoke.py
tests/smoke/
  anneal.md
  compass.md
  decide.md
```

Edit `skills/<name>/SKILL.md` in this repository. Installed copies under
`~/.claude/skills` and `~/.codex/skills` are managed by `scripts/install.py`.
