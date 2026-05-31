# Compass Example: Long Session Drift Audit

This is a representative `/compass` run for a coding agent that has been
editing a skill repository for several hours.

## Prompt

```text
/compass polish the Decision Kernel repo for public release
```

## Baseline Intent

Prepare a public-facing repository that helps people understand, install, and
evaluate the three decision protocols.

## Audit Output

| Axis | Status | Evidence |
| --- | --- | --- |
| Intent drift | SAFE | Recent edits still target README clarity, install safety, examples, and release readiness. |
| Git accumulation | CONSIDER | 9 files changed, including generated images and docs. Commit boundary is getting large. |
| Verification freshness | CONSIDER | Local smoke ran before README changes, but not after the final docs patch. |
| File bloat | SAFE | Skill files remain stable; public docs changed more than protocol internals. |
| TODO debt | SAFE | No new TODO markers in edited files. |

## Verdict

```text
CONSIDER
```

The session is still on-goal, but the next action should be a checkpoint:
review the diff, run validation, commit the public docs, and only then continue
with marketplace submission.

## Top Action

```text
Run validate + local smoke + installer tests, then commit the docs/release boundary.
```

## Why This Matters

Without the audit, the agent may keep polishing visible assets while carrying a
large unverified diff. `compass` does not say the work is wrong; it identifies
the point where continuing without a checkpoint becomes risky.

