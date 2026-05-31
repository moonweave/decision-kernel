# Fixture: doc-drift — canonical-sync mismatch and cross-file drift

This fixture packages two real gap patterns — a ROADMAP claiming a phase is
DEFERRED when the work has already landed, and a status summary whose headline
score contradicts the linked scorecard — into a small, inspectable worked example.
It exercises Checks 2 and 3 of the done-gate protocol.

## Files

- `ROADMAP.md` — project roadmap. Phase 3 is marked DEFERRED.
- `status-claim.md` — project status summary. Claims "6 / 8 integration tests
  passing" and "Overall health score: 92 / 100." Links to `status-detail.md`.
- `status-detail.md` — the full scorecard. Shows 5 / 8 integration tests passing
  and a total score of 82 / 100.
- `expected.md` — this walkthrough.

## The declared-done state

An engineer completes a multi-phase feature project and declares it done after
merging a batch of commits. done-gate is triggered at that boundary.

## Step 0 — Artifact-type gate (runs first)

The primary deliverable described in this fixture is **documentation** (a roadmap
and status files). The consumer is a human reader.

Classification: **figure / manuscript / doc** → useful-done is NOT mechanically
assessable. done-gate states plainly: "useful-done is not mechanically assessable
for a doc; consumer is a human reader." Check 1 does not run.

Checks 2 and 3 are baseline-independent and run for every artifact type.

## Check 2 — canonical-sync

**What done-gate does:** diff *claims* in the ROADMAP against repo reality —
specifically against `git log` for the branch.

**The claim:** `ROADMAP.md` line 13: `## Phase 3 — Multi-host aggregation (DEFERRED)`

**Repo reality:** the `git log` for this branch includes the following commits
(representative excerpt — shown here as inspectable evidence since this is a
prose fixture without a live repo):

```
c3f9a12  feat: implement multi-host aggregation endpoint
b7e2041  test: add multi_host_merge integration test skeleton
a1d55e8  feat: unified registry view — Phase 3 core
```

Commits referencing Phase 3 / multi-host / unified registry have landed on the
branch. The claim "DEFERRED" contradicts repo reality.

**Date-noise guard:** `ROADMAP.md` carries no timestamp, and `status-detail.md`
says "Last updated after Phase 2 merge." A doc being *older* than the latest
commit is not itself a finding — done-gate only flags a *contradicted claim*.
The contradiction here is the word "DEFERRED" standing next to landed commits,
not the document's age.

**Finding (Check 2, severity HIGH):**

> `ROADMAP.md` claims Phase 3 is DEFERRED, but commits for Phase 3 (multi-host
> aggregation) are present on the branch. Canonical doc does not reflect repo
> reality. Update the ROADMAP or confirm the commits were reverted.

## Check 3 — artifact-consistency / drift

**What done-gate does:** scan for numeric, term, or dimension contradictions
across files.

**Cross-file contradiction A — integration test count:**

- `status-claim.md`: "Integration tests passing: 6 / 8"
- `status-detail.md`: "Integration tests: 5 / 8 passing"

These are contradictory claims about the same metric. Neither file is "wrong" by
age; they simply disagree on the number.

**Cross-file contradiction B — overall health score:**

- `status-claim.md`: "Overall health score: 92 / 100"
- `status-detail.md` score breakdown: Total = 82 / 100

A 10-point gap between the summary headline and the linked scorecard. The summary
claims 92; the detail that the summary explicitly links to shows 82.

**Finding (Check 3, severity HIGH):**

> `status-claim.md` reports 6 / 8 integration tests passing and a score of 92 /
> 100. `status-detail.md` (the file it links to) shows 5 / 8 passing and 82 / 100.
> Two concrete numeric contradictions between the summary and its authoritative
> source. The summary was likely written before the scorecard was finalized or
> vice versa.

## Verdict

One-line verdict: **cannot-judge (doc type — useful-done not mechanically
assessable)**

Severity-ranked findings:

1. **[HIGH] Check 2 — canonical-sync:** ROADMAP Phase 3 marked DEFERRED;
   Phase 3 commits landed on branch.
2. **[HIGH] Check 3 — cross-file drift:** status-claim.md score (92/100, 6/8
   integration) contradicts status-detail.md (82/100, 5/8 integration).

These are drift/stale-claim findings. done-gate reports them as observations;
fixing is the user's job.

## What this fixture proves

done-gate catches two gap patterns that green tests do not reach:

- A canonical doc can contradict repo reality (Check 2) without any code being
  broken. The only signal is comparing a written claim against `git log`.
- Cross-file numeric drift (Check 3) survives heavy churn invisibly — the README
  and its linked scorecard diverge when one is updated and the other is not.

The date-noise guard is explicit: `status-detail.md` being older than the ROADMAP
is not flagged. Only the *contradicted claim* (DEFERRED vs landed commits,
92 vs 82) is reported.
