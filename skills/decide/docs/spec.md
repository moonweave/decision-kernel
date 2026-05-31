# Skill Design: `/decide`

**Date**: 2026-05-03  
**Status**: Approved for implementation

## 1. Identity & Trigger

- **Skill Name**: `decide`
- **Invocation**: `/decide` (user-triggered manual-only)
- **Location**: `~/.claude/skills/decide/SKILL.md`
- **Invocation Gate Description**: "User-invoked research skill. Investigates current industry best practice via WebSearch + docs APIs + GitHub adoption signals, then either decides autonomously (reversible actions) or escalates with user context (contested or information-requiring decisions). Manually triggered via `/decide` only."

This description prevents accidental auto-invocation. The skill fires only when user explicitly types `/decide`.

## 2. Input Resolution

### Syntax

```
/decide                    → Auto-extract pending question from prior assistant message
/decide <question text>    → Use explicit question as-is
```

### Auto-Extraction Logic (no args)

1. Search prior assistant message for question patterns:
   - Sentences ending with `?` + choice indicators (`A) ... B) ...`, `X vs Y`, "which", "어느", "어디")
   - If multiple candidates, use most recent one
   - If none found, respond with single line: `What should I research? Give me the question.` and exit (no research)

2. On successful extraction, output: `Researching: <extracted question>. If wrong, re-run with `/decide <your question>`.`

## 3. Research Pipeline

### Multi-Source Parallel Investigation

When question is resolved, execute 3 research tools in parallel (single tool call block):

1. **WebSearch** (always)
   - Patterns: `{question} best practice 2026`, `{X} vs {Y} which to use`, `{library} current standard`
   - 1-2 queries, aggregate results

2. **context7 (context7:query-docs)** (conditional)
   - Trigger: If question mentions a named library/framework (Next.js, PostgreSQL, FastAPI, etc.)
   - First resolve library via `context7:resolve-library-id`, then query latest docs for best practices
   - If no library noun detected, skip this tool
   - Goal: Official team guidance + recent version-specific advice

3. **GitHub adoption signals** (conditional)
   - Trigger: Only if WebSearch results show disagreement (see Synthesis)
   - Use `mcp__github__search_code` or similar to find: which projects are actually using X vs Y
   - Look for: recent activity (commits < 6 months), contributor count, adoption by flagship projects
   - **Constraint**: Stars are tiebreaker only, not primary signal. Flagship adoption (major companies, well-known orgs) matters more.

### Synthesis Rules

- **All 3 sources converge on same answer** → `clear standard` → Decide autonomously (Section 4)
- **Sources diverge** (e.g., WebSearch says X, GitHub shows Y popular) → `contested` → Escalate (Section 5)
- **GitHub search not needed** if WebSearch + context7 already converge → Skip tool 3, save tokens

## 4. Clear Standard Output (Reversible Path)

When sources converge, output:

```
**Decision: <X>**

<2-3 sentence explanation of why X is current industry standard, explicitly citing which source backed this (official docs, serverey data, expert consensus)>

Sources:
- <url1>
- <url2>
- <url3>

Considered: <alternative>, reason: <1 line why it lost>
```

**Example**:
```
**Decision: NextAuth.js**

NextAuth is the dominant choice for full-stack Next.js projects in 2026 (State of JS, Vercel docs). It's maintained by Vercel core, widely adopted across flagship Next.js projects, and the most recent releases (5.x) resolve prior pain points around session handling. Clerk is the managed alternative for teams that want to outsource auth infrastructure.

Sources:
- https://vercel.com/blog/nextauth-5
- https://2024.stateofjs.com/en-US/libraries/backend-frameworks/
- https://github.com/nextauthjs/next-auth (1.8K commits last 6 months)

Considered: Clerk, reason: managed service, not full-stack control
```

Then proceed to **Action Gate** (Section 6).

## 5. Contested/Context-Requiring Escalation

When sources diverge OR decision depends on user's project context:

**Output**:
```
**No clear standard — your context needed.**

Industry opinion splits:
- <Option X>: <1-line rationale> (<url>)
- <Option Y>: <1-line rationale> (<url>)

**The real question for your case:**
What is your answer to (a) <context fact 1> / (b) <context fact 2>?

Once I know that, I'll decide. [Wait for user response]
```

**Critical**: Do NOT ask "which do you prefer?" Ask for **factual project context** that determines the choice, so AI can map context → decision.

**Example**:
```
**No clear standard — deployment model differs.**

- NextAuth.js: full-stack, self-hosted infrastructure
- Clerk: managed SaaS, vendor-hosted

**For your case:**
Is this project (a) hosted on your own infrastructure / (b) delegated to a managed platform?

Once you answer, the choice is clear.
```

Wait for user's answer. Map answer to decision, then proceed to Action Gate.

## 6. Action Gate (Reversibility-Conditional)

After decision is made (Section 4 or 5), check if follow-up actions exist.

### Reversible Actions (proceed autonomously)

- Library/package install (`npm install`, `uv add`, `pip install`)
- File/folder creation (new files, new directories)
- Code writing/modification (new functions, new classes)
- Config file edits (before git commit)
- Documentation/comments

**Proceed with**: `Installing/Creating/Implementing <X>. Decision made; this is reversible.`

### Irreversible Actions (request confirmation)

- Database schema changes / migrations (even local)
- External service signup / API key generation
- Git destructive ops (`git reset --hard`, `git push --force`)
- Publishing / deployment (npm publish, GitHub Pages, staging/prod deploy)
- Payment / subscription changes
- External messaging (PR creation, issue comments, Slack messages)
- File deletion (multiple files, important history)

**Request confirmation with**: 
```
Next step requires: <action description>. This is hard to undo.
Proceed? [y/n]
```

Wait for explicit `y`/yes. Do NOT proceed without.

### Edge Case: "File creation after decision"

If decision is "use X", and follow-up involves **deleting old code** (e.g., "remove Y from codebase"), treat as reversible if < 5 files, irreversible if ≥ 5 files or core logic.

## 7. Error Handling

**WebSearch returns no useful results**:
- Output: `No clear guidance found for <question>. Asking you.` Then escalate (Section 5) with "expert consensus unclear" disclaimer.

**Question too vague** (e.g., `/decide should I learn programming?`):
- Output: `Too broad. Pick a specific technical decision: library choice, architecture pattern, tooling, workflow order, etc.`

**User escalation answer is ambiguous**:
- Ask for clarification: `I need more detail on <fact>. You said <X>, but does that mean <a> or <b>?`

## 8. Token Efficiency

- Parallel tool calls (all 3 in one block if needed)
- context7: only if library noun present
- GitHub: only if WebSearch diverges
- Synthesis: don't repeat sources verbatim, synthesize
- Output length: compact (100-200 words for decision, 150-250 for escalation)

## 9. Implementation Checklist

- [ ] Create skill file `~/.claude/skills/decide/SKILL.md`
- [ ] Implement auto-extraction regex for question patterns
- [ ] Parallel tool invocation for WebSearch + context7 + GitHub
- [ ] Synthesis logic (converge → decide, diverge → escalate)
- [ ] Output formatting per Section 4 & 5
- [ ] Reversibility gate (Section 6) with confirmaton patterns
- [ ] Error handling (Section 7)
- [ ] Test with 3-5 sample questions (library choice, architecture, tooling)
- [ ] Document invocation gate in skills index
