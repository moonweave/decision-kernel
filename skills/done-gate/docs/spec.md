# done-gate — design spec

> A user-invoked, read-only gate that runs when you *declare work "done"*. It
> actively checks whether the work is **useful-done** (a real consumer gets real
> value) or merely **built-done** (tests pass) — and refuses to judge rather than
> emit a confident-wrong verdict where the signal isn't there.

## Name & family

`done-gate`. A sibling of the author's `anneal` / `decide` / `compass` skills:
a single rich `SKILL.md`, `disable-model-invocation: true`, manual `/done-gate`
trigger only, read-only diagnosis. Published to
`github.com/moonweave/done-gate-skill`.

## The problem (measured, not hypothesized)

In one session, two artifacts were declared "done" with green tests, then a
by-hand audit found gaps every automated pass (reviewer, debugger, adversarial
review) had missed:

- An MCP server passed all tests but **no host was registered to call it** — built,
  tested, and functionally inert.
- A ROADMAP said a phase was `DEFERRED` while three commits for it were on `main`
  — canonical docs contradicting repo reality.
- A README's score table didn't match the scorecard file it told readers to audit
  — numeric drift across files after heavy churn.

None are bugs a test suite checks. The finish line was drawn at *build-correctness*
instead of *usefulness*. done-gate encodes that by-hand pass as a repeatable gate.

## The load-bearing lesson from the adversarial design review

A two-lens adversarial review of *this design* (before building) found that the
three catches that make done-gate valuable — "DONE-but-inert", "intentional vs
accidental debris", "name the cheap next step" — are exactly the ones that
**resist mechanization**; in the gold-standard by-hand pass they were all *human*
judgments. Therefore:

1. **done-gate measures what is mechanically measurable, and where there is no
   measurable signal it REFUSES to converge and hands the question back to the
   user** — the same floor `anneal` uses ("no measurable fitness ⇒ say so, don't
   fake it"). A confident verdict without signal is the bug, not the feature.
2. The original 4-check design was cut to **3 checks**; the 4th ("cheapest-next")
   was demoted from a verdict line to *unranked advisory candidates* because it
   structurally produces fluent-but-wrong "just do X" output — the exact
   false-authority failure the skill exists to prevent.

## Separation from compass (must stay distinct or this skill shouldn't exist)

- **compass** = *mid-session* audit: "have I drifted from intent? is the codebase
  rotting?" Looks backward/sideways during work. Baseline = original session intent.
- **done-gate** = *completion-boundary* gate: "I just said this is done — is it
  built-done or useful-done?" Looks forward at the finish line, against the work's
  own goal. Baseline = what this specific piece of work was supposed to deliver.

Different trigger moment, different question, different baseline. done-gate must
not re-implement compass's general rot scan; its git-status read is scoped to the
*declared change*, used only to distinguish built-done from useful-done — not a
"is the whole repo healthy" sweep.

## Step 0 — Artifact-type gate (run FIRST, before any check)

Classify the declared deliverable. This single gate prevents the review's two
worst failure modes (false-red on shelved work, false-green on figures):

| Type | useful-done assessable? |
|---|---|
| **runnable-deliverable** (server, CLI, service, wired entry point) | **Yes** — check #1 runs |
| **library / skill** (consumer is a future caller/session) | Partial — "reachable/importable/registered?" only; never "inert" as a defect if deferral was intended |
| **figure / manuscript / doc** | **No** — say "useful-done is not mechanically assessable for a `<type>`; consumer is a human reader." Check 1 is skipped; checks 2-3 (canonical-sync, drift) still apply — they are baseline-independent. |
| **throwaway / one-off** (ran once, intentionally not wired) | **No** — "ran-once-and-parked is its done state"; do NOT flag as inert |

For any non-runnable type, done-gate states plainly that useful-done is out of
scope rather than faking it.

## The three checks

### Check 1 — useful-done (gated to runnable-deliverable)
Can a real consumer invoke this against real (not fixture) data/path?
- Mechanically decidable cases: MCP server → grep host configs for a registration
  entry; package → published / imported / has a runnable example; entry point →
  wired into a caller. Prefer a *non-mutating* probe of reachability (grep
  host/registry configs, confirm the entry point is wired, check an
  importable/published path, or a dry-run / `--help` / read-only subcommand). If
  confirming useful-done would require a *mutating* run (a CLI that writes, a
  migration, a network call), do **not** execute it — report "useful-done not
  verifiable without a side-effecting run" as a limit and let the user run it. The
  gate stays read-only.
- **DONE-but-inert is reported as a state, not always a defect.** If the human
  intended "inert pending Phase 2 registration," that is a legitimate landing —
  done-gate surfaces it ("built-done; not yet useful-done because no host
  registers it") and lets the user judge, rather than screaming "broken."

### Check 2 — canonical-sync (the genuinely novel kernel)
Do the canonical docs match repo reality? Diff *claims*, not timestamps:
- ROADMAP/STATUS/README claims (e.g. "Phase X DEFERRED") vs `git log` reality
  (commits for Phase X on the branch).
- A doc dated older than HEAD is **not** stale by itself — only a contradicted
  *claim* is. (Guard against date-noise false positives.)
This is the one check compass does not do and that is fully mechanizable.

### Check 3 — artifact-consistency / drift (the backbone)
Numeric / term / dimension drift across files, plus declared-change tree state:
- Cross-file: a number/term/dimension stated in file A contradicts file B
  (e.g. README score table ≠ linked scorecard; a dimension named in the task
  spec but absent from the rubric).
- Tree: `git status` scoped to the declared change. **"Just declared done" inverts
  the prior — a dirty tree defaults to legit WIP, not debris.** Untracked files are
  *listed and asked about* (intentional-will-gitignore vs stray), never
  auto-classified as debris. Works across every artifact type, including figures.

## Advisory (not a verdict) — candidate next steps

Instead of the cut "cheapest-next" verdict line: optionally list **≤3 unranked
candidate next steps**, explicitly flagged "you judge cost/value — these are not
ranked and may be wrong." Never "the cheapest next step is X." If nothing is
confidently identifiable, omit the section.

## Baseline inference (draft → confirm) with a refusal floor

Infer "what this work was supposed to deliver" from recent `git diff`/commits +
any spec/plan file; draft it; ask the user to confirm/correct (the `anneal`
draft→confirm pattern).
- **Mandatory scope-confirm above a size threshold:** for large/multi-session/
  squashed diffs (e.g. ≫ a few dozen files), require the user to name the
  subtree / intended change before inferring — a giant diff has no usable
  "should-have" signal.
- **Refusal floor:** if no baseline is inferable AND the user cannot confirm a
  concrete one, **refuse to emit a verdict** — output "cannot judge useful-done
  here; missing signal: `<what>`." That is the correct, valuable output.

## Output

A severity-ranked report + a one-line verdict: **built-done** vs **useful-done**
vs **cannot-judge (<reason>)**. Diagnosis only — no fixes, read-only
(`allowed-tools`: Read, Bash, AskUserQuestion). Fixing is the user's or `/team`'s job.

## Repo layout (mirror anneal)

```
done-gate-skill/
├── SKILL.md          # the protocol (frontmatter + §0 gate + 3 checks + floor + output)
├── README.md         # public: problem → what it does → compass distinction → honest limits
├── LICENSE           # MIT, moonweave
├── .gitignore
├── docs/spec.md      # this file
└── eval/             # self-eval: the two real cases from this session as fixtures
    ├── inert-mcp/    # built-done-but-inert (useful-done check should flag "not yet useful")
    └── doc-drift/    # ROADMAP-says-deferred-but-committed (canonical-sync should flag)
```

## Honest limits (state in SKILL.md & README)

- Does **not** judge honesty (the author is already strong there; out of scope).
- Cannot assess useful-done for non-runnable artifact types — says so, doesn't fake.
- Refuses a verdict without a measurable baseline rather than guessing.
- It is a **forcing-function checklist**, not a novel engine — value is reproducing
  the by-hand pass at the finish line so it isn't skipped, plus the one new
  mechanizable signal (canonical-sync). Where a check needs human judgment
  (intentional-vs-accidental, is-inert-OK), it surfaces and asks; it never
  auto-concludes.

## Self-review notes (anti-over-engineering)

- 3 checks, not 4 — cheapest-next demoted to advisory per the review.
- No auto-fix, no hooks, no auto-invoke (the family's anti-cascade rule).
- compass-overlap addressed by the completion-boundary framing + change-scoped
  git read; if a future reader can't tell done-gate from compass, that's a defect.
