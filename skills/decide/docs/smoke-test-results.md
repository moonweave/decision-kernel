# Smoke Test Results

## 2026-05-31 — Codex hardening pass

### Scope

Verify the `decide` source skill after adding Claude Code manual-only metadata, a project-local preflight, and a minimum evidence rule for declaring a "clear standard."

### Static Verification

Command:

```bash
python3 - <<'PY'
from pathlib import Path
import yaml
path = Path('/Users/choemun-yeong/ai-skills-dev/my-skills/decide-skill/SKILL.md')
text = path.read_text()
fm = yaml.safe_load(text.split('---', 2)[1])
assert fm['name'] == 'decide'
assert fm.get('disable-model-invocation') is True
assert fm.get('argument-hint') == '[technical decision question]'
assert 'current repo, project, codebase' in text
assert 'A clear standard requires at least two' in text
assert 'Never ask "X or Y?"' in text
print('decide metadata and gate rules ok')
PY
```

Result: passed.

### Fresh Claude Code Invocation

Command:

```bash
claude --print --no-session-persistence --max-budget-usd 0.20 --allowedTools Read,Bash,WebSearch,WebFetch --permission-mode bypassPermissions '/decide in this current repo, should docs/spec.md be deleted now that SKILL.md is current? Answer only; do not edit files.'
```

Result: blocked by Claude CLI organization policy, before skill execution:

```text
Your organization has disabled Claude subscription access for Claude Code · Use an Anthropic API key instead, or ask your admin to enable access
```

### Verdict

Local metadata and rule verification passed. True fresh Claude Code invocation remains blocked by account/organization policy. This is not a skill-file failure.
