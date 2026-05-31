# Decide Example: Python Package Layout

This is a representative `/decide` run for a coding agent choosing between a
flat Python package layout and a `src/` layout.

## Prompt

```text
/decide should this Python library use a src layout or a flat layout?
```

## Local Context

The repository is intended to be installed by users and tested against the
installed package, not only run in-place from the checkout.

## Evidence Check

| Source Type | Signal |
| --- | --- |
| Official packaging guidance | `src/` layout reduces accidental imports from the working tree during tests. |
| Project intent | The package is meant for installation and reuse outside the repo. |
| Cost | `src/` layout adds a small amount of scaffolding but avoids a common test/import trap. |

## Decision

```text
Use a src layout.
```

## Rationale

For an installable Python library, `src/` is the safer default because tests are
less likely to pass by accidentally importing the local working tree instead of
the installed distribution. A flat layout is still reasonable for tiny scripts,
single-use internal tools, or repositories that are not intended to be packaged.

## Action

Create:

```text
src/<package_name>/
tests/
pyproject.toml
```

Then run the test suite through the installed package path before publishing.

## Why This Matters

The value of `decide` is not that it always picks the more complex option. It
checks whether the choice is governed by a clear standard, explains the boundary
conditions, and escalates only when project facts would change the answer.

