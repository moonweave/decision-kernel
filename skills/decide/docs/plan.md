# `/decide` Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a user-invoked `/decide` skill that researches current industry best practice (WebSearch + context7 + GitHub) and either decides autonomously for reversible actions or escalates with factual-context questions for contested ones.

**Architecture:** Single `SKILL.md` file at `~/.claude/skills/decide/SKILL.md`. The "code" is structured markdown instructions that Claude reads at invocation time. No external dependencies, no Python/TS, no traditional test framework — validation is performed by invoking `/decide <sample-question>` and checking that the output conforms to spec sections.

**Tech Stack:** Claude Code skill (YAML frontmatter + markdown), git versioning under `~/.claude/skills/.git`. Tools used at runtime: WebSearch, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__github__search_code, mcp__github__search_repositories.

**Spec reference:** `~/docs/superpowers/specs/2026-05-03-decide-skill-design.md`

---

## File Structure

- Create: `~/.claude/skills/decide/SKILL.md` — the entire skill (frontmatter + body)
- Modify: none
- Test: smoke tests via interactive `/decide` invocation in a fresh Claude Code session

Single-file skill. No supporting scripts, no helpers, no tests directory. The spec sections map 1:1 onto SKILL.md sections.

Working directory for git operations: `~/.claude/skills/` (separate git repo, confirmed via `ls -la` showing `.git/`).

---

## Task 1: Scaffold skill directory and frontmatter

**Files:**
- Create: `~/.claude/skills/decide/SKILL.md`

- [ ] **Step 1: Verify the parent directory and confirm no name collision**

Run:
```bash
ls -la ~/.claude/skills/decide 2>&1
```
Expected: `No such file or directory` (skill does not yet exist).

If the directory already exists, STOP and inspect — do not overwrite.

- [ ] **Step 2: Create the directory**

Run:
```bash
mkdir -p ~/.claude/skills/decide
```
Expected: silent success.

- [ ] **Step 3: Write frontmatter-only SKILL.md**

Write to `~/.claude/skills/decide/SKILL.md`:

```markdown
---
name: decide
description: |
  User-invoked research skill. Investigates current industry best practice via
  parallel WebSearch + context7 + GitHub adoption signals, then either decides
  autonomously (reversible actions) or escalates with factual-context questions
  (contested or information-requiring decisions). Manually triggered via
  `/decide` only — never auto-invoked. Use when the user types `/decide`
  optionally followed by a question. Without arguments, extract the pending
  decision from the prior assistant message.
allowed-tools:
  - WebSearch
  - WebFetch
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
  - mcp__github__search_code
  - mcp__github__search_repositories
  - mcp__github__list_commits
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
---

# /decide — Best Practice Research & Autonomous Decision

(body to be filled in subsequent tasks)
```

- [ ] **Step 4: Verify YAML frontmatter parses**

Run:
```bash
python3 -c "import yaml,sys; doc=open('$HOME/.claude/skills/decide/SKILL.md').read().split('---')[1]; yaml.safe_load(doc); print('YAML OK')"
```
Expected: `YAML OK`

If this fails, inspect for indentation or quoting errors and re-run before proceeding.

- [ ] **Step 5: Commit scaffold**

Run:
```bash
cd ~/.claude/skills && git add decide/SKILL.md && git commit -m "feat(decide): scaffold skill directory and frontmatter"
```
Expected: 1 file changed.

---

## Task 2: Write trigger and input resolution sections

**Files:**
- Modify: `~/.claude/skills/decide/SKILL.md` (append to body)

- [ ] **Step 1: Append Trigger and Input Resolution sections**

Use Edit to replace the placeholder line `(body to be filled in subsequent tasks)` with the following content:

````markdown
## When to Run

Only when the user types `/decide`, optionally followed by a question. Never auto-invoke. The description gate above explicitly forbids automatic firing.

## 1. Input Resolution

Resolve the question to research using these rules in order:

1. **If `/decide` is followed by text** → use the text verbatim as the question. Do not paraphrase.

2. **If `/decide` has no arguments** → scan the most recent assistant message in this conversation for a pending decision. Look for:
   - Sentences ending with `?` that contain choice indicators: `A) ... B) ...`, `X vs Y`, the words `which`, `어느`, `어디`, `뭐가`
   - If exactly one candidate is found, use it
   - If multiple candidates, use the most recent one and announce: `Researching: <question>. If wrong, re-run with /decide <your question>.`
   - If none found, output exactly: `What should I research? Give me the question.` and STOP. Do not call any research tool.

3. **Once resolved**, announce: `Researching: <question>` (one line, then proceed).
````

- [ ] **Step 2: Read the file back and verify structure**

Run:
```bash
grep -c "^## " ~/.claude/skills/decide/SKILL.md
```
Expected: `2` (the `## When to Run` and `## 1. Input Resolution` headers).

- [ ] **Step 3: Commit**

Run:
```bash
cd ~/.claude/skills && git add decide/SKILL.md && git commit -m "feat(decide): add trigger and input resolution sections"
```

---

## Task 3: Write research pipeline section

**Files:**
- Modify: `~/.claude/skills/decide/SKILL.md` (append)

- [ ] **Step 1: Append Research Pipeline section**

Use Edit to add to the end of the file:

````markdown

## 2. Research Pipeline

Once the question is resolved, run research tools. **WebSearch is always called.** The other two are conditional.

### Step 2a — Always call WebSearch (1-2 queries)

Choose query patterns matching the question type:
- Comparison: `<X> vs <Y> 2026 best practice`
- Standard lookup: `<library or topic> current standard 2026 recommended`
- Workflow: `<domain> recommended workflow order 2026`

Prefer recent (≤ 18 months) sources. Prioritize:
- Official framework/library team docs and blog posts (e.g., Vercel, Anthropic, Postgres team)
- Industry surveys: State of JS, Stack Overflow Developer Survey, JetBrains Developer Ecosystem
- Named expert blogs and conference talks

**Stars and follower counts are not best-practice signals.** They correlate with hype and age, not technical correctness.

### Step 2b — Conditionally call context7

**Trigger:** the question mentions a named library, framework, or tool (Next.js, PostgreSQL, FastAPI, React, Pydantic, etc.).

If triggered:
1. `mcp__context7__resolve-library-id` with the library name
2. `mcp__context7__query-docs` with the resolved ID and a topic-focused query (e.g., `"authentication recommended approach"`)

If no library noun is detected in the question, skip this step.

### Step 2c — Conditionally call GitHub MCP (tiebreaker only)

**Trigger:** Step 2a results show genuine disagreement between sources, OR Step 2a + 2b return no clear consensus.

If triggered, use `mcp__github__search_code` or `mcp__github__search_repositories` to check **flagship adoption signals**, in this priority:
1. Adoption by major orgs / well-known production projects
2. Recent commit activity (last 6 months) and active contributor count
3. Star count is the weakest signal — use only as a final tiebreaker

If Step 2a + 2b already converge, skip this step.

### Synthesis

After tools return:
- **All called sources point to the same answer** → "clear standard" → proceed to Section 3
- **Sources disagree, but the disagreement is explained by a project-context variable** (e.g., self-hosted vs managed, team size, scale) → proceed to Section 4 (escalate with factual-context question)
- **Sources disagree without a clear discriminating variable** → proceed to Section 4 with the explanation that expert consensus is unclear
````

- [ ] **Step 2: Verify section count**

Run:
```bash
grep -c "^## " ~/.claude/skills/decide/SKILL.md
```
Expected: `3`.

- [ ] **Step 3: Commit**

Run:
```bash
cd ~/.claude/skills && git add decide/SKILL.md && git commit -m "feat(decide): add research pipeline with conditional tool routing"
```

---

## Task 4: Write clear-standard output format

**Files:**
- Modify: `~/.claude/skills/decide/SKILL.md` (append)

- [ ] **Step 1: Append clear-standard output section**

Use Edit to add to the end of the file:

````markdown

## 3. Output — Clear Standard Path

When synthesis yields a clear standard, output exactly this structure:

```
**Decision: <X>**

<2-3 sentences explaining why X is the current industry standard. Cite explicitly which type of source backed this: official docs, industry survey, expert consensus.>

Sources:
- <url1>
- <url2>
- <url3 if used>

Considered: <alternative>, reason: <one line why it lost>
```

**Rules:**
- Source URLs are mandatory. Never omit them — the user's global `<communication>` rule requires it.
- Keep the explanation to 2-3 sentences total. Compact decision text, not a research summary.
- The "Considered" line is mandatory whenever a real alternative exists. Naming the loser builds trust that the search was thorough.

After this output block, proceed to Section 5 (Action Gate).
````

- [ ] **Step 2: Commit**

Run:
```bash
cd ~/.claude/skills && git add decide/SKILL.md && git commit -m "feat(decide): add clear-standard output format"
```

---

## Task 5: Write contested escalation section

**Files:**
- Modify: `~/.claude/skills/decide/SKILL.md` (append)

- [ ] **Step 1: Append contested escalation section**

Use Edit to add to the end of the file:

````markdown

## 4. Output — Contested / Context-Required Path

When synthesis is contested or the decision depends on a project-context variable, output exactly this structure:

```
**No clear standard — your context decides.**

업계 의견 분기:
- <Option X>: <one-line rationale> (<url>)
- <Option Y>: <one-line rationale> (<url>)

너의 답에 따라 자동 결정됨:
"<one factual question about user's project context>"
```

**Critical rules — the entire skill premise depends on these:**

1. **Never ask "X or Y?" or "어느 쪽?"** — that bounces the decision back to the user, which defeats the skill's purpose. The user triggered `/decide` because they cannot intelligently pick between X and Y.

2. **Always ask for a factual project context variable**, never a technical preference. Good question patterns:
   - "이 프로젝트는 자체호스팅이야 관리형이야?"
   - "예상 동시 사용자 수가 1k 이하야 그 이상이야?"
   - "팀이 너 혼자야 여러 명이야?"
   - "데이터 일관성과 가용성 중 더 중요한 게 뭐야?" (when both are valid technical contexts, not preferences)

3. **After the user answers**, map the answer to one of the options and output the Section 3 (Clear Standard) format with the chosen option, then proceed to Section 5 (Action Gate). Do not re-research.

4. **If the user's answer is ambiguous**, ask one clarifying factual question. Never ask the user to pick the technical option directly.
````

- [ ] **Step 2: Commit**

Run:
```bash
cd ~/.claude/skills && git add decide/SKILL.md && git commit -m "feat(decide): add contested escalation with factual-context rule"
```

---

## Task 6: Write action gate (reversibility) section

**Files:**
- Modify: `~/.claude/skills/decide/SKILL.md` (append)

- [ ] **Step 1: Append action gate section**

Use Edit to add to the end of the file:

````markdown

## 5. Action Gate — Reversibility Rule

After the decision is announced (Section 3 or 4), check whether follow-up actions are required.

### Reversible — proceed autonomously, no confirmation

- Library/package install (`npm install`, `uv add`, `pip install`, `cargo add`)
- New file or directory creation
- New function/class/module written from scratch
- Config file edits **before** the first git commit of those edits
- Documentation, comments, README changes
- Code modification touching **fewer than 5 files**

When proceeding: announce in one line: `Installing/Creating/Implementing <X>. Reversible — proceeding.`

### Irreversible — request explicit confirmation

- Database schema changes or migrations (even on local databases)
- External service signup, API key generation, OAuth setup
- Git destructive ops: `git reset --hard`, `git push --force`, `git branch -D`
- Publishing or deployment: `npm publish`, GitHub Pages publish, staging/prod deploy
- Payment, subscription, or billing changes
- External messaging: PR creation, issue comments, Slack/email send
- File or directory deletion (any number of files)
- Code modification touching **5 or more files** OR rewriting core/load-bearing logic
- Removal of existing functionality (delete a function, drop a feature)

When confirmation is needed, output exactly:

```
다음 액션은 되돌리기 어려워: <action description>.
진행할까? (y/n)
```

Wait for an explicit `y` or `yes` (English or Korean equivalent). Do not proceed on silence, "ok", or ambiguous responses.

### Edge case — borderline scope

If you are unsure whether a planned action crosses the 5-file threshold or touches load-bearing logic, treat it as irreversible and confirm. False negatives are cheap (one extra question); false positives can cause real damage.
````

- [ ] **Step 2: Commit**

Run:
```bash
cd ~/.claude/skills && git add decide/SKILL.md && git commit -m "feat(decide): add reversibility-based action gate"
```

---

## Task 7: Write error handling section

**Files:**
- Modify: `~/.claude/skills/decide/SKILL.md` (append)

- [ ] **Step 1: Append error handling section**

Use Edit to add to the end of the file:

````markdown

## 6. Error Handling

### WebSearch returns no useful results

Output: `No clear guidance found for "<question>". Falling back to escalation with explicit "expert consensus unclear" disclaimer.`

Then run Section 4 with this acknowledgment in place of the source URLs.

### Question is too vague

Examples: `/decide should I learn programming?`, `/decide what should I do?`

Output: `Too broad. /decide is for specific technical decisions: library choice, architecture pattern, tooling, workflow order. Re-run with a concrete question.` Then STOP.

### Library lookup fails (context7 returns nothing)

Skip context7 silently. Continue with WebSearch + GitHub. Do not retry.

### Tool failure during research

If a tool errors, log it as one line in the final output (`Note: <tool> errored, decided based on remaining sources`) but do not abort. Use whatever sources succeeded.

### User's escalation answer is ambiguous

Ask exactly one clarifying factual question. Never re-ask the technical X-vs-Y question. If still ambiguous after the second exchange, output: `Need clearer context. Could you describe <variable> in one sentence?`
````

- [ ] **Step 2: Final structural check**

Run:
```bash
grep "^## " ~/.claude/skills/decide/SKILL.md
```
Expected output (in order):
```
## When to Run
## 1. Input Resolution
## 2. Research Pipeline
## 3. Output — Clear Standard Path
## 4. Output — Contested / Context-Required Path
## 5. Action Gate — Reversibility Rule
## 6. Error Handling
```

- [ ] **Step 3: Commit**

Run:
```bash
cd ~/.claude/skills && git add decide/SKILL.md && git commit -m "feat(decide): add error handling section"
```

---

## Task 8: Smoke test — clear-standard case

**Files:**
- Test: interactive Claude Code session (no file)

This task validates the skill end-to-end on a question with a known clear standard.

- [ ] **Step 1: Open a fresh Claude Code session in any directory**

Open a new terminal, run `claude` (or your alias). This loads the skill list fresh.

- [ ] **Step 2: Verify the skill is discoverable**

In the new session, type `/help` (or check the skills list). Expected: `decide` appears with the description from the frontmatter.

If it does not appear, check:
- File path: `~/.claude/skills/decide/SKILL.md` exists
- YAML frontmatter parses without error (re-run Task 1 Step 4)

- [ ] **Step 3: Run the clear-standard smoke test**

In the session, type:
```
/decide what's the standard Python project layout for a 2026 library — src/ vs flat?
```

Expected output structure (per spec Section 4):
- `**Decision: <X>**` line
- 2-3 sentences citing official source type
- `Sources:` with 2-3 URLs
- `Considered: <alt>, reason: ...` line
- A reversible-action announcement OR no further action

If the output omits sources, names X without explanation, or asks "which do you prefer?", the skill failed this test. Note the failure and proceed to Task 10 for fixes.

- [ ] **Step 4: Record result**

Append to `~/docs/superpowers/plans/2026-05-03-decide-skill.md` under a new heading `## Smoke Test Results` (create if missing): one line with the date, question, and pass/fail.

---

## Task 9: Smoke test — contested case

**Files:**
- Test: interactive Claude Code session

- [ ] **Step 1: In the same session, run a contested question**

Type:
```
/decide which auth library for a Next.js side project — NextAuth or Clerk?
```

Expected output structure (per spec Section 5):
- `**No clear standard — your context decides.**` header
- Two options listed with one-line rationale + URL each
- A factual context question (e.g., "self-hosted vs managed?")
- **NOT** a "which do you prefer?" question

If the skill asks the user to pick X or Y directly, the Issue 1 fix did not stick. Note the failure for Task 10.

- [ ] **Step 2: Answer the factual question**

Reply with one of the two valid context answers. Expected: skill maps the answer to one option and outputs the Section 4 (Clear Standard) format. Then either reversible-proceed or irreversible-confirm.

- [ ] **Step 3: Record result**

Append a one-line entry to the smoke test results section in this plan file.

---

## Task 10: Smoke test — irreversible action gate

**Files:**
- Test: interactive Claude Code session

- [ ] **Step 1: Run a question that implies an irreversible follow-up**

Type:
```
/decide should I delete the legacy auth module since we picked NextAuth?
```

Expected:
- A decision (per Section 3 or 4)
- Then a confirmation prompt matching: `다음 액션은 되돌리기 어려워: <action>. 진행할까? (y/n)`
- The skill MUST stop and wait — must not delete files autonomously

If the skill proceeds to delete files without confirmation, the action gate failed. Note for Task 11.

- [ ] **Step 2: Reply `n`**

Expected: skill acknowledges and stops. No file changes.

- [ ] **Step 3: Verify no files were modified**

Run:
```bash
cd ~/.claude/skills && git status
```
Expected: clean working tree (the smoke test should not have modified the skill repo).

- [ ] **Step 4: Record result**

Append a one-line entry.

---

## Task 11: Iterate on any smoke test failures

**Files:**
- Modify: `~/.claude/skills/decide/SKILL.md` (only sections that failed tests)

- [ ] **Step 1: Review smoke test results**

Read the `## Smoke Test Results` section appended to this plan. Identify which spec sections produced failed behavior.

If all three smoke tests passed, skip to Task 12.

- [ ] **Step 2: For each failure, edit the corresponding SKILL.md section**

Common failure modes and fixes:
- Skill asked "X or Y?" in contested case → strengthen Section 4 rule 1 with a more emphatic prohibition and an example pair (good vs bad question)
- Skill omitted source URLs → add reminder near top of Section 3: "URLs are non-negotiable per user's communication rules"
- Skill auto-executed irreversible action → re-list the irreversible category at the start of Section 5 with an explicit "STOP and confirm" header
- Skill failed to extract pending question → add more example patterns to Section 1 rule 2

Apply targeted Edits, not full rewrites.

- [ ] **Step 3: Re-run only the failed smoke test(s)** in a fresh session

- [ ] **Step 4: Commit fixes**

Run:
```bash
cd ~/.claude/skills && git add decide/SKILL.md && git commit -m "fix(decide): address smoke test failures (<one-line summary>)"
```

---

## Task 12: Save memory entry and close out

**Files:**
- Create: `~/.claude/projects/<your-project-id>/memory/project_decide_skill.md`
- Modify: `~/.claude/projects/<your-project-id>/memory/MEMORY.md`

- [ ] **Step 1: Write the memory file**

Write to `~/.claude/projects/<your-project-id>/memory/project_decide_skill.md`:

```markdown
---
name: /decide skill — research-then-decide-autonomously
description: User-invoked /decide skill researches industry standard via WebSearch+context7+GitHub, decides for reversible actions, escalates with factual-context for contested. Spec/plan completed 2026-05-03.
type: project
---

`/decide` skill at `~/.claude/skills/decide/SKILL.md`. Manual trigger only via slash command.

**Why:** User is non-expert in many software domains (web, devops, etc.) and wanted Claude to stop asking "which would you prefer?" for decisions where a clear industry standard exists. Pre-baked rules in CLAUDE.md were rejected (decay risk in long contexts); skill form chosen for stability via description-gated invocation.

**How to apply:** When the user types `/decide` (with or without an explicit question), the skill kicks in. For contested cases, the skill must NEVER ask "X or Y?" — it asks one factual project-context question and maps the answer to a decision. Irreversible actions (≥5 file edits, deletes, deploys, migrations, force-push) require explicit `y/yes` confirmation; reversible ones proceed automatically.

**Spec:** `~/docs/superpowers/specs/2026-05-03-decide-skill-design.md`
**Plan:** `~/docs/superpowers/plans/2026-05-03-decide-skill.md`

**Brainstorm note:** This brainstorm was accidentally re-done — earlier session on 2026-05-03 morning had already produced the same spec (10:09 AM file). Memory did not capture that prior work, leading to redundant Q1-Q6 walkthrough. Save brainstorm-completion checkpoints to memory in future to prevent repeats.
```

- [ ] **Step 2: Add a one-line entry to MEMORY.md**

Use Edit to append this line to `MEMORY.md` (in chronological-bottom order with other 2026-05 entries):

```
- [/decide skill](project_decide_skill.md) — 비전문가 도메인 결정 자동화 스킬. WebSearch+context7+GitHub 조사 후 reversible은 자동, contested는 factual-context 질문. (2026-05-03)
```

- [ ] **Step 3: Final verification — invoke the skill once more in a totally fresh session**

Run a new `claude` session, then `/decide what's the standard Python lockfile in 2026 — uv.lock or poetry.lock?`

Expected: full clear-standard response per Section 3, including URLs, "Considered" line, and a one-line autonomous-proceed announcement (or no follow-up action since this is a pure question).

- [ ] **Step 4: Final commit**

Run:
```bash
cd ~/.claude/skills && git log --oneline | head -10
```

Expected: 7 commits for the decide skill (Tasks 1, 2, 3, 4, 5, 6, 7) plus optionally 1 fix commit from Task 11. Total 7-8 commits, all on the `~/.claude/skills` repo.

If commits look correct, the skill is done.

---

## Self-Review Notes

This plan was reviewed against `~/docs/superpowers/specs/2026-05-03-decide-skill-design.md`:
- Spec Section 1 (Identity & Trigger) → Task 1 (frontmatter) + Task 2 (When to Run)
- Spec Section 2 (Input Resolution) → Task 2
- Spec Section 3 (Research Pipeline) → Task 3
- Spec Section 4 (Clear Standard Output) → Task 4 + smoke Task 8
- Spec Section 5 (Contested Escalation) → Task 5 + smoke Task 9
- Spec Section 6 (Action Gate) → Task 6 + smoke Task 10
- Spec Section 7 (Error Handling) → Task 7
- Spec Section 8 (Token Efficiency) → reflected as conditional logic in Task 3
- Spec Section 9 (Implementation Checklist) → mapped onto Tasks 1-12

Type/method consistency: the skill is markdown-only. No function or method names to drift.

No placeholders. Every task contains the exact content to write or the exact command to run.
