<div align="center">

# Decision Kernel

**A judgment gate for coding agents.**

Decision Kernel is four local Claude/Codex skills that make agent decisions
inspectable before large diffs land. It is built for Claude Code and Codex
users who want agent decision-making, drift audits, evidence-gated technical
decisions, and an honest "is this really done?" gate to happen inside the repo
instead of in vague chat.

<img src="assets/decision-kernel-mobile-card.png" alt="Decision Kernel compact card" width="340">

</div>

## Why This Exists

Agents fail most often at judgment boundaries: committing to the wrong direction,
continuing after drift, or deciding from weak evidence. Decision Kernel gives
those moments a short local protocol:

1. **Decide with evidence** instead of confident guesswork.
2. **Measure the fork** before building the wrong thing.
3. **Audit drift and rot** before a long session compounds mistakes.
4. **Gate "done"** so finished means useful-done, not just tests-pass.

This repository packages those protocols as local Claude/Codex skills. It does
not replace engineering judgment; it makes that judgment inspectable. Search
terms that describe the project plainly: agent skills, Claude Code skills,
Codex skills, coding-agent workflows, decision gates, drift audits, and
evidence-backed technical choices.

| Moment | Skill | Product Job |
| --- | --- | --- |
| "What is the right technical choice?" | [`decide`](skills/decide) | Combine local project context with current source-backed evidence. |
| "Which direction should we build?" | [`anneal`](skills/anneal) | Turn alternatives into a cheap measurable comparison. |
| "Has this session gone off-track?" | [`compass`](skills/compass) | Check drift, accumulated work, stale evidence, and codebase rot. |
| "Is this actually done?" | [`done-gate`](skills/done-gate) | Check built-done vs useful-done; refuse a verdict without signal. |

## Quick Start

Install both Claude Code and Codex skill copies:

```bash
git clone https://github.com/moonweave/decision-kernel.git
cd decision-kernel
python3 scripts/install.py --target all --apply
```

Then invoke the protocols when an agent is about to make a judgment-heavy move:

```text
/decide should this project use a src layout?
/anneal choose between table, graph, and cards for an inventory dashboard
/compass audit this session against the original goal
/done-gate is the MCP server I just finished actually usable?
```

## Example Workflow

A coding agent is about to build an inventory dashboard and must pick between a
table, graph, or card layout.

```text
/anneal choose the primary UI direction for a developer inventory dashboard:
table vs graph vs cards
```

The protocol forces the agent to define a task-based fitness sheet before
building: time to find an owner, steps to spot risky inventory, and coverage of
relationship questions. If the rough table scores highest, the agent builds the
table first instead of spending the session polishing a graph that fails the
actual task.

Later in the same session:

```text
/compass harden local Claude/Codex skills
/decide should this stale spec file be deleted?
/done-gate I said the dashboard is done — is it?
```

`compass` checks whether the work still matches the session intent. `decide`
requires local repo context plus current sources before making the deletion call.
`done-gate` runs at the finish line: it separates built-done (tests pass) from
useful-done (a real consumer gets value), and reports a stale ROADMAP claim or a
README that contradicts its own scorecard rather than rubber-stamping "done."

See [docs/examples](docs/examples) for concrete representative runs covering
the protocols: evidence-gated choice, measurable direction fork, session drift
audit, and the useful-done gate at the finish line.

## Visual Model

![Decision Kernel protocol strip](assets/decision-kernel-protocol-strip.png)

![Decision Kernel annotated hero](assets/decision-kernel-annotated-hero.png)

## The Four Protocols

### `anneal` - Measure Before You Commit

Use when the agent is about to choose between competing approaches. `anneal`
forces the choice into a measurable fitness sheet, scores rough candidates, and
stops before expensive implementation.

Best for:

- UI direction choices
- architecture alternatives
- data model tradeoffs
- "graph vs table vs cards" style forks

### `compass` - Audit Drift And Rot

Use during long sessions when the agent may be optimizing for the wrong task or
carrying too much unverified work. `compass` compares the current work against a
baseline intent and checks local repo health signals.

Best for:

- long agent sessions
- repo cleanup before continuing
- catching stale test/lint assumptions
- identifying drift between requested work and current edits

### `decide` - Evidence-Gated Technical Decisions

Use when the agent must make or escalate a technical decision. `decide` starts
with local repo context, then requires credible current evidence before calling
anything a clear standard.

Best for:

- library/framework choices
- migration decisions
- deletion or deprecation calls
- contested engineering practices

### `done-gate` - Built-Done vs Useful-Done

Use at the completion boundary, right after the agent declares work "done."
`done-gate` checks whether it is built-done (tests pass) or useful-done (a real
consumer gets real value), and refuses to emit a verdict when there is no
measurable signal rather than rubber-stamping it. Read-only — it diagnoses,
never fixes.

Best for:

- a server/CLI that passes tests but no host is wired to call it
- a ROADMAP or README whose claims drifted from what actually landed
- score/number contradictions across files after heavy churn
- telling "shelved on purpose" apart from "silently unfinished"

It is distinct from `compass`: compass audits mid-session drift against the
original intent; done-gate runs at the finish line against what this specific
piece of work was supposed to deliver.

## Install

Clone the repo:

```bash
git clone https://github.com/moonweave/decision-kernel.git
cd decision-kernel
```

Preview Claude Code install:

```bash
python3 scripts/install.py --target claude
```

Apply Claude Code install:

```bash
python3 scripts/install.py --target claude --apply
```

Preview Codex install:

```bash
python3 scripts/install.py --target codex
```

Apply Codex install:

```bash
python3 scripts/install.py --target codex --apply
```

Preview both:

```bash
python3 scripts/install.py --target all
```

Apply both:

```bash
python3 scripts/install.py --target all --apply
```

Without `--apply`, the installer only prints the planned changes. Claude installs
are symlinks to this repository. Codex installs are generated copies with
Codex-compatible frontmatter.

## Validate

Run local structural checks:

```bash
python3 scripts/validate.py
```

Run local smoke checks:

```bash
python3 scripts/smoke.py --local-only
```

Run installer behavior tests:

```bash
python3 -m unittest tests/test_install.py -v
```

Attempt live Claude Code smoke checks:

```bash
python3 scripts/smoke.py
```

If Claude Code is blocked by account or organization policy, live smoke returns
exit code `2` and prints the blocker. Local validation still verifies the repo
structure and installable skill files.

## Repository Layout

![Decision Kernel architecture](assets/decision-kernel-architecture.png)

```text
skills/
  decide/      # evidence-gated technical decisions
  anneal/      # measurable fork comparison
  compass/     # session drift and repo rot audit
  done-gate/   # completion-boundary built-done vs useful-done gate
scripts/
  install.py   # Claude symlink install + Codex sanitized copy install
  smoke.py     # local and live smoke checks
  validate.py  # frontmatter, marker, and hygiene validation
tests/smoke/
  anneal.md
  compass.md
  decide.md
  done-gate.md
docs/
  architecture.md
  distribution.md
  examples/
  launch-copy.md
  product-brief.md
  skill-catalog.md
```

## Status

Decision Kernel is currently a local-first toolkit for Claude Code and Codex
users. The core protocols are usable, but the public-facing product surface is
still early:

- no hosted UI
- no marketplace package
- no automated release channel
- live Claude Code smoke depends on the local account policy

The source of truth is this monorepo. Older standalone skill repos are legacy
mirrors and should not receive new development.

For public listing and discovery work, see
[docs/distribution.md](docs/distribution.md).

## Development

Edit skills only inside this repository:

```text
skills/anneal/SKILL.md
skills/compass/SKILL.md
skills/decide/SKILL.md
skills/done-gate/SKILL.md
```

Before committing:

```bash
python3 scripts/validate.py
python3 scripts/smoke.py --local-only
```

Then reinstall locally:

```bash
python3 scripts/install.py --target all --apply
```

See [docs/architecture.md](docs/architecture.md) for the source-of-truth and
install model. See [docs/product-brief.md](docs/product-brief.md) for the PRD
framing behind the public positioning.
