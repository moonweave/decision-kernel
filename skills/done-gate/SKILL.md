---
name: done-gate
description: |
  A completion-boundary gate that distinguishes built-done (tests pass) from
  useful-done (a real consumer gets real value) at the moment work is declared
  finished. Manually triggered via `/done-gate` only — never auto-invoked. Use
  when the user types `/done-gate` after declaring work done.
disable-model-invocation: true
argument-hint: "[what this work was supposed to deliver]"
allowed-tools:
  - Read
  - Bash
  - AskUserQuestion
---

# /done-gate — Built-Done vs Useful-Done

A read-only gate for the completion boundary: "I just said this is done — is it built-done or useful-done?" Diagnosis only; it never fixes.

## 1. When to run

Only when the user types `/done-gate`. Never auto-invoke.

Run it at the completion boundary — right after the user declares work "done." Not during work, not on a hunch, not on a timer. The trigger is the user's own declaration.

## 2. Separation from compass

compass and done-gate are siblings, not duplicates. Conflating them removes the value of both.

- **compass** = mid-session audit: "have I drifted from intent? is the codebase rotting?" Backward/sideways during work. Baseline = original session intent. General repo health sweep.
- **done-gate** = completion-boundary gate: "I just said this is done — is it built-done or useful-done?" Forward at the finish line. Baseline = what this specific piece of work was supposed to deliver. Git read scoped to the declared change only — NOT a whole-repo health sweep.

Different trigger moment, different question, different baseline. done-gate must not re-implement compass's rot scan.

## 3. Baseline (draft → confirm) + refusal floor

Before any check, establish what this work was supposed to deliver.

**Draft the baseline** from recent `git diff`/commits plus any spec or plan file present. Show the inferred baseline to the user; ask them to confirm, correct, or narrow it. Do not silently lock in a model-drafted scope.

**Mandatory scope-confirm** above a size threshold: for large, multi-session, or squashed diffs (many dozens of files), require the user to name the subtree or intended change before inferring — a giant diff contains no usable "should-have" signal.

**Refusal floor:** if no baseline is inferable AND the user cannot confirm a concrete one, refuse to emit a verdict. Output exactly:

> cannot judge useful-done here; missing signal: `<what is missing>`

That is the correct, valuable output. A confident verdict without signal is the bug, not the feature. On refusal, emit no verdict; checks 2-3 (canonical-sync, drift) are baseline-independent and may still be reported as observations.

## 4. Step 0 — Artifact-type gate (run FIRST)

Classify the declared deliverable before running any check. This prevents false-red on shelved work and false-green on figures.

| Type | useful-done assessable? |
|---|---|
| **runnable-deliverable** (server, CLI, service, wired entry point) | Yes — check 1 runs |
| **library / skill** (consumer is a future caller or session) | Partial — "reachable / importable / registered?" only; never "inert" as a defect if deferral was intended |
| **figure / manuscript / doc** | No — state "useful-done is not mechanically assessable for a `<type>`; consumer is a human reader." Check 1 is skipped; checks 2-3 (canonical-sync, drift) still run — they are baseline-independent (§3). |
| **throwaway / one-off** (ran once, intentionally not wired) | No — "ran-once-and-parked is its done state"; do not flag as inert |

If a deliverable matches more than one row, classify by how its *primary declared consumer* (from the baseline, §3) reaches it — a future caller/session ⇒ library/skill; an end user invoking it now ⇒ runnable-deliverable. When intent (wired vs parked) isn't observable, ask the user rather than assuming.

For any non-runnable type, state plainly that useful-done is out of scope rather than faking it.

## 5. The three checks

### Check 1 — useful-done (gated to runnable-deliverable)

Can a real consumer invoke this against real (not fixture) data or path?

Mechanically decidable cases:
- MCP server → grep host configs for a registration entry.
- Package → published / imported / has a runnable example.
- Entry point → wired into a caller.

Prefer a non-mutating probe of reachability: grep host/registry configs, check the entry point is wired, confirm an importable/published path, or invoke a dry-run / `--help` / read-only subcommand. If confirming useful-done would require a mutating run (a CLI that writes, a migration, a network call), do NOT execute it — report "useful-done not verifiable without a side-effecting run" as a limit and let the user run it. The gate stays read-only.

**DONE-but-inert is a STATE, not always a defect.** If the human intended "inert pending Phase 2 registration," that is a legitimate landing. Surface it ("built-done; not yet useful-done because no host registers it") and let the user judge. Do not auto-conclude it is broken.

### Check 2 — canonical-sync

Do the canonical docs match repo reality? Diff *claims*, not timestamps:
- ROADMAP / STATUS / README claims (e.g. "Phase X DEFERRED") vs `git log` reality (commits for Phase X already on the branch).
- A doc dated older than HEAD is **not** stale by itself — only a contradicted *claim* is. Guard against date-noise false positives.

This is the one check compass does not do and that is fully mechanizable.

### Check 3 — artifact-consistency / drift

Cross-file numeric, term, or dimension drift plus declared-change tree state.

**Cross-file:** a number, term, or dimension stated in file A contradicts file B (README score table differs from the linked scorecard; a dimension named in the task spec absent from the rubric). Applicable to every artifact type, including figures.

**Tree state:** `git status` scoped to the declared change. "Just declared done" inverts the prior — a dirty tree defaults to legit WIP, not debris. Untracked files are listed and the user is asked about each (intentional-will-gitignore vs stray). Never auto-classify as debris.

## 6. Advisory (not a verdict)

Optionally list at most three unranked candidate next steps. Prefix them explicitly: "You judge cost/value — these are not ranked and may be wrong."

Never write "the cheapest next step is X." If nothing is confidently identifiable, omit this section entirely.

## 7. Output

Emit a severity-ranked report followed by a single-line verdict:

- **built-done** — artifact is correct and complete but not yet reachable by a real consumer.
- **useful-done** — a real consumer can invoke it against real input now.
- **cannot-judge (`<reason>`)** — baseline missing, artifact type not assessable, or signal absent.

Diagnosis only, read-only. Fixing is the user's or `/team`'s job.

## 8. Honest limits

- Does not judge honesty — out of scope; the author is already strong there.
- Cannot assess useful-done for non-runnable artifact types — says so, does not fake it.
- Refuses a verdict without a measurable baseline rather than guessing.
- It is a forcing-function checklist, not a novel engine. Value is reproducing the by-hand pass at the finish line so it is not skipped, plus the one new mechanizable signal (canonical-sync). Where a check needs human judgment (intentional vs accidental, is inert OK), it surfaces and asks; it never auto-concludes.
