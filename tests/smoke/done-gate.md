# done-gate smoke test

Manual smoke checklist for the `done-gate` skill.

1. Run `/done-gate` right after declaring some work "done."
2. Confirm it classifies the artifact type first, then runs the gated checks (useful-done, canonical-sync, drift).
3. Confirm it reports a one-line verdict — built-done, useful-done, or cannot-judge — and never edits files (read-only diagnosis).
4. Confirm it refuses a verdict when no measurable baseline is available instead of guessing.
5. Confirm it does not auto-fire without the `/done-gate` command.
