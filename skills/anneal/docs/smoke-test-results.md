# Smoke Test Results

## 2026-05-31 — Codex hardening pass

### Scope

Verify the `anneal` source skill and installed copies after adding Claude Code manual-only metadata and syncing the Codex copy with the latest measurement-sheet workflow.

### Static Verification

Command:

```bash
python3 - <<'PY'
from pathlib import Path
import yaml
for path in [
    Path('/Users/choemun-yeong/ai-skills-dev/my-skills/anneal-skill/SKILL.md'),
    Path('/Users/choemun-yeong/.claude/skills/anneal/SKILL.md'),
    Path('/Users/choemun-yeong/.codex/skills/anneal/SKILL.md'),
]:
    text = path.read_text()
    fm = yaml.safe_load(text.split('---', 2)[1])
    assert fm['name'] == 'anneal'
    assert 'description' in fm
    if '.codex' not in str(path):
        assert fm.get('disable-model-invocation') is True
        assert 'argument-hint' in fm
    assert 'Bound "fixable"' in text
    assert 'Stop rule' in text
    print('ok', path)
PY
```

Result: passed.

### Fixture Verification

Command:

```bash
python3 /Users/choemun-yeong/ai-skills-dev/my-skills/anneal-skill/eval/dup-finder/target.py
```

Result:

```text
input size: 9000
duplicate values found: 148
elapsed: 1.2895s
```

### Fresh Claude Code Invocation

Command:

```bash
claude --print --no-session-persistence --max-budget-usd 0.20 --allowedTools Read,Bash --permission-mode bypassPermissions '/anneal choose the primary UI direction for a developer inventory dashboard: table vs graph vs cards. Run only the measurement-sheet drafting step, then stop. Do not edit files.'
```

Result: blocked by Claude CLI organization policy, before skill execution:

```text
Your organization has disabled Claude subscription access for Claude Code · Use an Anthropic API key instead, or ask your admin to enable access
```

### Verdict

Local file and fixture verification passed. True fresh Claude Code invocation remains blocked by account/organization policy. This is not a skill-file failure.
