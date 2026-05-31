# done-gate

> A read-only completion-boundary gate. After you declare work "done," it checks whether it is **built-done** (tests pass) or **useful-done** (a real consumer gets real value) — and refuses to judge rather than guess when the signal is absent.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Claude Code skill](https://img.shields.io/badge/Claude%20Code-skill-8A63D2)
![status: early](https://img.shields.io/badge/status-early-orange)

```
/done-gate                                    # at the completion boundary
/done-gate <what this work was to deliver>    # seed the baseline explicitly
```

---

## The problem

Green tests can hide gaps no automated reviewer catches:

- An MCP server passes all tests but no host config registers it — built, tested, and functionally inert.
- A ROADMAP says a phase is `DEFERRED` while the work for it had already landed — canonical doc contradicting repo reality.
- A README score table disagrees with the scorecard file it tells readers to audit — numeric drift after heavy churn.

None are bugs a test suite checks. The finish line gets drawn at *build-correctness* instead of *usefulness*. done-gate encodes the by-hand pass that catches these as a repeatable gate.

## What it does

**Step 0 — Artifact-type gate (runs first).** Classify the declared deliverable before any check:

| Type | useful-done assessable? |
|---|---|
| runnable-deliverable (server, CLI, service, wired entry point) | Yes |
| library / skill (consumer is a future caller or session) | Partial — reachability only |
| figure / manuscript / doc | No — says so; check 1 skipped, checks 2-3 still run |
| throwaway / one-off (ran once, intentionally not wired) | No — "ran-once-and-parked is its done state" |

**Three checks:**

1. **useful-done** (gated to runnable-deliverable) — can a real consumer invoke this against real input? Non-mutating probe only (grep host configs, check an importable path, `--help`). If confirming would require a mutating run, reports it as a limit and defers to the user. DONE-but-inert is surfaced as a state, not auto-classified as broken.
2. **canonical-sync** — do canonical docs match repo reality? Diffs *claims*, not timestamps. ROADMAP says `DEFERRED` but commits for that phase are on the branch? That's a contradicted claim. A doc dated older than HEAD is not stale by itself. This is the one check compass does not do and that is fully mechanizable.
3. **artifact-consistency / drift** — cross-file numeric, term, or dimension disagreements, plus `git status` scoped to the declared change. Untracked files are listed and the user is asked about each — never auto-classified as debris.

**Baseline (draft → confirm) with a refusal floor.** Infers what this work was supposed to deliver from recent `git diff`/commits plus any spec or plan file, drafts it, then asks the user to confirm or correct. For large or squashed diffs, requires the user to name the subtree before inferring. If no baseline is inferable and the user cannot confirm one: **refuses to emit a verdict** and outputs `cannot judge useful-done here; missing signal: <what>`. That is the correct, valuable output.

**Advisory (not a verdict).** Optionally lists ≤3 unranked candidate next steps (may be wrong — you judge cost/value). Never "the cheapest next step is X." If nothing is confidently identifiable, the section is omitted.

## vs. compass

compass and done-gate are siblings in the same family; conflating them removes the value of both.

| | compass | done-gate |
|---|---|---|
| **Trigger moment** | Mid-session, during work | Completion boundary — after "done" is declared |
| **Question** | Have I drifted from intent? Is the codebase rotting? | Is this built-done or useful-done? |
| **Baseline** | Original session intent | What this specific piece of work was to deliver |
| **Git scope** | General repo health sweep | Declared change only — not a whole-repo sweep |

done-gate must not re-implement compass's rot scan. Its git read is scoped to the declared change and used only to distinguish built-done from useful-done.

## Install

done-gate ships a single runtime artifact — `SKILL.md`:

```bash
mkdir -p ~/.claude/skills/done-gate
cp SKILL.md ~/.claude/skills/done-gate/
```

It auto-loads in any new Claude Code session; verify it appears in `/help`.

## Usage

```
/done-gate
```

Invoke at the completion boundary — right after declaring work done. Not during work, not on a hunch, not on a timer.

```
/done-gate <what this work was supposed to deliver>
```

Seed the baseline explicitly to skip the draft-and-confirm round, or when the diff is too large to infer from.

done-gate is read-only: it diagnoses, never fixes.

## Honest positioning

**It is a forcing-function checklist, not a novel engine.** The value is reproducing the by-hand pass at the finish line so it is not skipped. The one genuinely new mechanizable signal is canonical-sync (check 2) — everything else encodes judgment that already existed, made repeatable.

## Honest limits

- Does not judge honesty — out of scope.
- Cannot assess useful-done for non-runnable artifact types (figures, manuscripts, docs) — says so plainly, does not fake it.
- Refuses a verdict without a measurable baseline rather than guessing.
- Where a check requires human judgment (intentional vs accidental, is inert acceptable), it surfaces and asks; it never auto-concludes.
- The gate stays read-only: if confirming useful-done would require a side-effecting run, it defers to the user rather than executing.

## Status

Early, and honest about it. The three checks and the refusal floor are the stable core. It is a checklist discipline, not a measured win over careful by-hand review — use it as a forcing function at the finish line, not a guarantee.

**Why a skill and not just a tip?** Because the by-hand pass gets skipped. The cases in the problem section above all passed automated review and were flagged only by manual audit. Packaging the pass as `/done-gate` gives it a trigger moment, a scope, and a refusal floor — making it harder to skip than a note in a CLAUDE.md.

## License

MIT — see [LICENSE](LICENSE).

## Author

[@moonweave](https://github.com/moonweave)
