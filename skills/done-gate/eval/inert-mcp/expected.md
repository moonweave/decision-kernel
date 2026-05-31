# Fixture: inert-mcp — built-done but not yet useful-done

This fixture packages the "MCP server passed all tests, but no host registers it"
case into a small, inspectable worked example. Its job is to show what done-gate
should surface — and should *not* auto-conclude — when Check 1 finds no registration.

## Files

- `server.py` — the config-inventory MCP server stub. One read-only tool
  (`list_config_entries`), a `main()` entry point, valid Python, ruff-clean.
- `host-config.json` — a representative host MCP config registering three other
  servers (filesystem, github, brave-search). This server (`config-inventory-mcp`
  or `server.py`) is absent from it.
- `expected.md` — this walkthrough.

## The declared-done state

An engineer finishes the server, writes tests, all tests pass. They declare it done.
done-gate is triggered at that boundary.

## Step 0 — Artifact-type gate (runs first)

The deliverable is a **runnable-deliverable**: a server with a named entry point
(`main()`), designed to be called by an LLM host process. This is the type row
that makes Check 1 applicable.

Classification: **runnable-deliverable** → Check 1 runs.

(If the engineer had declared intent as "parked pending Phase 2 wiring," the
classification would shift to throwaway/one-off and Check 1 would be skipped.
Since the baseline shows no such intent, runnable-deliverable is the correct read.)

## Check 1 — useful-done

**What done-gate does:** grep `host-config.json` (and any other discovered host
config files in the standard paths) for a registration entry that references this
server. The distinctive identifier is the server name `config-inventory` or the
path to `server.py` inside a `config-inventory-mcp` directory.

**Signal:** the grep returns nothing. The three registered servers (filesystem,
github, brave-search) share no name or path with this one.

**Mechanically: absent.**

**Correct verdict:**

> **built-done; not yet useful-done** — no host config registers
> `config-inventory-mcp`. A real consumer cannot invoke `list_config_entries`
> today. This is a *state*, not a defect classification. If registration is
> deferred to a later phase, this landing is legitimate — done-gate surfaces it
> and the user decides.

**What done-gate must NOT do:** auto-conclude "broken" or "defective." The server
code is correct. Tests are green. The gap is between build-correctness and
reachability. That gap may be intentional (integration deferred) or overlooked
(engineer forgot to add the entry). done-gate names the state; it does not
adjudicate the intent.

## Checks 2 & 3 — in this fixture

No ROADMAP or cross-file status claims exist for this server stub, so Checks 2
and 3 produce no findings. The full verdict rests on Check 1 alone.

## What this fixture proves

done-gate catches a class of gap that green tests cannot: a server can be
*correct and complete* while being *unreachable*. The probe is non-mutating
(read-only grep of host configs). The verdict is a state report, not a defect
auto-classification. That distinction is the load-bearing behavior this fixture
exercises.
