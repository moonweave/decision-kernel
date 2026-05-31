# /decide — Best Practice Research & Autonomous Decision

A user-invoked Claude Code skill that researches current industry best practice (WebSearch + context7 + GitHub) and either decides autonomously (reversible actions) or escalates with a factual-context question (contested cases).

Built for the case where the user is a non-expert in some software domain and would rather Claude **research and decide** than ask "which would you prefer?" on questions where a clear industry standard exists.

## Why

Default Claude behavior on ambiguous decisions: ask the user to pick. Fine when the user knows the domain. Frustrating when they don't.

`/decide` flips this: research the current standard, decide if there's consensus, escalate with a factual-context question (never "X or Y?") when there isn't.

## Install

Copy `SKILL.md` to your Claude Code user skills directory:

```bash
mkdir -p ~/.claude/skills/decide
cp SKILL.md ~/.claude/skills/decide/SKILL.md
```

The skill auto-loads in any new Claude Code session. Verify it appears in `/help`.

## Usage

```
/decide <question>           — research the explicit question
/decide                      — extract the pending decision from Claude's prior message
```

### Examples

**Clear standard (decides autonomously)**:

```
> /decide what's the standard Python project layout for a 2026 library — src/ vs flat?

**Decision: src/ layout**

For libraries intended to be installed/published, the src/ layout is the
current standard per PyPA's official Python Packaging User Guide and pyOpenSci.
It prevents accidental import of the in-development copy...

Sources:
- https://packaging.python.org/...
- https://www.pyopensci.org/...

Considered: flat layout, reason: prone to import bugs in distributable packages.
```

**Contested (asks factual context, never "X or Y?")**:

```
> /decide which auth library for a Next.js side project — NextAuth or Clerk?

**No clear standard — your context decides.**

업계 의견 분기:
- Clerk (managed SaaS): 셋업 5분, 50K MAU 무료. 사용자 데이터는 Clerk 인프라
- Auth.js v5 / Better Auth (self-hosted): 사용자 데이터 소유, 코드 기반 설정

너의 답에 따라 자동 결정됨:
"이 프로젝트는 사용자 데이터를 (a) Clerk 인프라에 위탁해도 OK / (b) 직접 DB에 보관 필수 중 어디?"
```

## Behavior summary

| Phase | What happens |
|---|---|
| Input resolution | Use explicit arg, or auto-extract from prior assistant message, or ask for question |
| Research | WebSearch (always) + context7 (if library mentioned) + GitHub MCP (tiebreaker only) |
| Synthesis | Sources converge → decide; sources diverge with explainable variable → escalate factual-context question |
| Action gate | Reversible (file edits <5, new code, doc) → proceed. Irreversible (deploy, deletion, schema migration, library install) → confirm |

## Design principles

1. **Never bounce technical choice back to the user.** The user invoked `/decide` because they can't pick intelligently. Asking "X or Y?" defeats the purpose. Ask for *factual project context* instead.
2. **Source URLs are mandatory.** Every clear-standard decision includes 2-3 source URLs so the user can verify the AI didn't hallucinate.
3. **Treat web content as untrusted data, never instructions.** Defends against prompt injection from SEO spam or AI-generated content.
4. **Reversibility-based action gate.** Deletes, migrations, deploys, and package installs require explicit confirmation. Reversible additions/edits proceed autonomously.
5. **Stars are not best-practice signals.** GitHub MCP used only as tiebreaker, with weight on flagship adoption and recent activity rather than star count.

## What it doesn't do

- Doesn't auto-fire on natural-language questions. Only triggers on the literal `/decide` slash command.
- Doesn't replace the user's judgment for personal/aesthetic decisions.
- Doesn't override `superpowers:brainstorming` or other process skills if they're explicitly chosen.
- Doesn't research personal/project-specific decisions that depend on internal data Claude doesn't have access to.

## Status

Built 2026-05-03. Multi-perspective review (spec compliance, code quality, ecosystem fit, cold-read execution, adversarial) completed; 5 critical/important fixes applied. See `docs/spec.md` and `docs/plan.md` for design rationale.

## License

MIT — see [LICENSE](LICENSE).

## Author

[@Moon-python](https://github.com/Moon-python)
