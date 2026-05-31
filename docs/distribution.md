# Distribution Checklist

Decision Kernel should be discoverable as a small, practical toolkit for agent
decision quality, not as three disconnected prompt snippets.

## Listing Copy

Name:

```text
Decision Kernel
```

One-line description:

```text
Claude Code and Codex skills for measurable forks, session drift audits, and evidence-gated technical decisions.
```

Short description:

```text
Decision Kernel packages three local agent skills: anneal measures competing directions before implementation, compass audits long sessions for drift and repo rot, and decide makes source-backed technical choices from local context plus current evidence.
```

Tags:

```text
Claude Code, Codex, agent skills, AI agents, coding agents, decision making, developer tools, prompt engineering
```

Primary URL:

```text
https://github.com/moonweave/decision-kernel
```

Release URL:

```text
https://github.com/moonweave/decision-kernel/releases/tag/v0.1.0
```

Primary image:

```text
assets/decision-kernel-mobile-card.png
```

## Submission Targets

These sites responded during a lightweight availability check on 2026-05-31:

- https://agentskills.to
- https://claudemarketplace.net
- https://claudeskills.co
- https://polyskill.ai

This target returned a temporary bad gateway during the same check, so verify
again before submitting:

- https://skillmesh.tech

## Submission Notes

- Submit the monorepo URL, not the old standalone skill repos.
- Use the mobile card image first; it works better in compact directory cards.
- Mention dry-run install safety: `scripts/install.py` previews changes unless
  `--apply` is passed.
- Link the concrete example:
  `docs/examples/anneal-inventory-dashboard.md`.
- Mention that the standalone `anneal-skill`, `compass-skill`, and
  `decide-skill` repos are legacy mirrors.

## Acceptance Check

Before submitting to any directory, confirm:

- GitHub description and topics match the listing copy.
- README first viewport explains the product without relying only on images.
- `python3 scripts/validate.py` passes.
- `python3 scripts/smoke.py --local-only` passes.
- The latest release exists and includes the current onboarding docs.

