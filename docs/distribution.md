# Distribution Checklist

Decision Kernel should be discoverable as a small, practical toolkit for agent
decision quality, not as four disconnected prompt snippets.

## Listing Copy

Name:

```text
Decision Kernel
```

One-line description:

```text
Local Claude Code & Codex agent skills for evidence-gated decisions, measurable build-direction forks, mid-session drift audits, and an honest done-gate.
```

Short description:

```text
Decision Kernel packages four local agent skills: decide makes source-backed technical choices from local context plus current evidence, anneal measures competing directions before implementation, compass audits long sessions for drift and repo rot, and done-gate separates built-done (tests pass) from useful-done (a real consumer gets value) at the finish line.
```

Tags:

```text
Claude Code, Codex, Claude skills, Codex skills, agent skills, AI agents, coding agents, decision making, drift audit, done gate, developer tools, prompt engineering
```

Primary URL:

```text
https://github.com/moonweave/decision-kernel
```

Release URL:

```text
https://github.com/moonweave/decision-kernel/releases/tag/v0.1.4
```

Primary image:

```text
assets/decision-kernel-mobile-card.png
```

## Submission Queue

Verified by web search on 2026-06-01. Targets below are the ones with corroborated
public usage; earlier unverified entries (skills.re, agentskills.in, and several
Priority-2 sites) were removed because no independent reference to them was found.

> Reality check: in 2026 most skill directories **auto-index public GitHub repos**
> rather than requiring a submission portal. The repo-side work already done
> (search-friendly topics, README keywords, four valid `SKILL.md` files) is the
> bulk of "getting listed." Manual submission below is optional acceleration.

> Safety: agent-skill registries have had malicious-submission incidents (the
> ClawHub case), so reputable directories now security-scan submissions — good for
> *you as a publisher*. When any site asks to "Sign in with GitHub," read the
> OAuth scope: read-only (`read:user`, `public_repo`) is fine; decline anything
> requesting full `repo` write, delete, or org permissions. You only need to hand
> over a public repo URL.

Priority 1: submit manually (highest-traffic, security-scanned).

| Target | URL | Why | Action |
| --- | --- | --- | --- |
| agentskill.sh | https://agentskill.sh/ | Largest indexed directory (100k+ skills), 12-category security scan, Product Hunt listed. | Submit `https://github.com/moonweave/decision-kernel`; check the OAuth scope before authorizing. |
| skills.sh (Vercel) | https://skills.sh/ | Widely-referenced public skill directory. | Submit the repo URL if a submit path is offered; otherwise rely on auto-index. |
| VoltAgent/awesome-agent-skills | https://github.com/VoltAgent/awesome-agent-skills | Curated GitHub list (1000+ skills). | Open a PR adding decision-kernel under the relevant category. |

Final submission may require a browser session, account sign-in, or a visible
confirmation step. Do not rely on undocumented API calls for these targets.

Priority 2: auto-indexing directories (likely no action needed).

| Target | URL | Note |
| --- | --- | --- |
| claudemarketplaces.com | https://claudemarketplaces.com/ | Community directory, ~200k monthly visits, updated daily from GitHub — should pick the repo up automatically. |
| Agensi | https://www.agensi.io/ | Security-scanned marketplace; optional publish flow if a listing is wanted. |
| claudeskills.info / SkillsMP | https://claudeskills.info/ · https://skillsmp.com/ | Large directories that index GitHub repos; verify the listing appears after a week, submit only if a path exists. |

## Submission Notes

- Submit the monorepo URL, not the old standalone skill repos.
- Use the mobile card image first; it works better in compact directory cards.
- Mention dry-run install safety: `scripts/install.py` previews changes unless
  `--apply` is passed.
- Link the concrete example:
  `docs/examples/`.
- Mention that the standalone `anneal-skill`, `compass-skill`, and
  `decide-skill` repos are legacy mirrors. (done-gate ships only inside this
  monorepo — there is no standalone done-gate repo to confuse it with.)
- Use [launch-copy.md](launch-copy.md) for social posts and directory comments.

## Submission Payload

Repository:

```text
https://github.com/moonweave/decision-kernel
```

Direct skill URLs:

```text
https://github.com/moonweave/decision-kernel/tree/main/skills/decide
https://github.com/moonweave/decision-kernel/tree/main/skills/anneal
https://github.com/moonweave/decision-kernel/tree/main/skills/compass
https://github.com/moonweave/decision-kernel/tree/main/skills/done-gate
```

Example URL:

```text
https://github.com/moonweave/decision-kernel/tree/main/docs/examples
```

## Acceptance Check

Before submitting to any directory, confirm:

- GitHub description and topics match the listing copy.
- README first viewport explains the product without relying only on images.
- `python3 scripts/validate.py` passes.
- `python3 scripts/smoke.py --local-only` passes.
- The latest release exists and includes the current onboarding docs.
