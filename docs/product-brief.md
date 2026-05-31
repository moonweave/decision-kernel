# Product Brief

## Product

Decision Kernel is a local decision layer for agentic coding workflows. It
packages three operational protocols as Claude/Codex skills: `anneal`,
`compass`, and `decide`.

## Target User

- Developers using coding agents for multi-step local implementation.
- Agent workflow builders who need repeatable decision gates.
- Researchers and technical leads who want evidence-backed agent decisions
  without adding a heavyweight process.

## Problem

Agent workflows often fail at judgment boundaries rather than raw execution:

- they commit too early to one implementation direction
- they continue after session drift
- they treat stale local evidence as healthy
- they decide from a single weak source

These failures are hard to see until after the agent has produced a large diff.

## Value Proposition

Decision Kernel keeps agents autonomous while making their judgment auditable.
It turns ambiguous decision moments into short protocols with explicit inputs,
evidence, and stop conditions.

## Core Use Cases

1. Choose between implementation directions before building.
2. Audit long sessions for drift and accumulated repo risk.
3. Make or escalate technical decisions using local context and current sources.

## Differentiation

Decision Kernel is not another prompt pack. It is organized around decision
failure modes:

- `anneal` handles premature commitment.
- `compass` handles drift and local rot.
- `decide` handles weak-evidence technical calls.

## Current Scope

In scope:

- local Claude Code skill installs
- local Codex skill installs
- repeatable validation and smoke scripts
- source-of-truth monorepo layout

Out of scope for the current version:

- hosted UI
- marketplace publishing
- automated release distribution
- cross-agent telemetry

## Success Criteria

- A first-time visitor understands the repo purpose within 30 seconds.
- A local user can install and validate the skills with two commands.
- Future skill edits happen in this monorepo, not in standalone legacy repos.
- The repo reads as an agent judgment product, not a loose collection of skills.
