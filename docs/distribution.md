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

Checked on 2026-06-01.

Priority 1: direct repository import forms.

| Target | URL | Status | Action |
| --- | --- | --- | --- |
| agentskill.sh | https://agentskill.sh/submit | Direct GitHub repository import form visible. | Submit `https://github.com/moonweave/decision-kernel`. |
| skills.re | https://skills.re/submit | Submit page available; may require sign-in before final publish. | Submit repo URL, verify scan result, finish after sign-in if prompted. |
| Agent Skills CLI | https://agentskills.in | Home page advertises repo submission and marketplace indexing. | Submit repo URL from the home page submission panel. |

Final submission may require a browser session, account sign-in, or a visible
confirmation step. Do not rely on undocumented API calls for these targets.

Priority 2: directory/indexing targets.

| Target | URL | Status | Action |
| --- | --- | --- | --- |
| AgentSkills | https://agentskills.to | Directory online; direct submit path not obvious from the public page. | Search site UI or contact maintainer if not auto-indexed. |
| Claude Code Marketplace | https://www.claudemarketplace.net/skills | Directory online and indexing thousands of skills; direct submit path not obvious from public nav. | Check whether repo appears after indexing; otherwise use contact/advertise route. |
| ClaudeSkills | https://www.claudeskills.co | Directory online. | Verify direct submission or indexing path manually. |
| PolySkill | https://polyskill.ai | Site responded during earlier availability check. | Verify whether it accepts SKILL.md repos before spending time. |
| SkillMesh | https://skillmesh.tech | Returned temporary bad gateway during earlier check. | Recheck later before submitting. |

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
