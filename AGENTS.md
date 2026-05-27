# Agent Operating Charter

This repo is intentionally AI-native. Agents can research, draft, review, test,
and propose changes. Ram owns final judgment.

## Mission

Build a public field manual for platform engineers deploying LLM agents into
production. The manual should make agent identity, authorization, least
privilege, and auditability concrete enough to apply.

## Default Workflow

1. Read `README.md`, `DESIGN.md`, and the target chapter before editing.
2. Keep public claims grounded in primary sources when possible.
3. Prefer small pull requests: one chapter, one demo, or one matrix update.
4. Put research notes in `notes/` when adding non-trivial source material.
5. Add runnable examples under `demos/` only when they can be tested locally.
6. Update `landscape/vendors.md` when vendor claims affect the manual.
7. Leave private planning under `.private/`; do not reference it from public docs.

## Quality Bar

- Be precise about identity, authorization, trust boundaries, and audit logs.
- Do not treat prompt injection as the whole problem.
- Do not overstate vendor capabilities.
- Do not invent citations or imply a source says more than it says.
- Prefer practical platform-engineering guidance over abstract security prose.
- Keep examples minimal enough to inspect.

## Agent Roles

- Research agents produce notes and source maps.
- Writer agents draft chapters from approved outlines and research.
- Critic agents challenge IAM accuracy, missing controls, and unsupported claims.
- Demo agents build PoCs and tests.
- Distribution agents draft launch copy only; humans publish.

## Human Gates

Ram must approve:

- chapter thesis and angle
- merged chapter text
- demo behavior and security framing
- vendor claims
- public social posts
- conference submissions

Agents should make the work legible enough for fast human review.

## gstack

Use gstack skills when they match the task. For web browsing in Claude, use
gstack `/browse`. Do not use `mcp__claude-in-chrome__*` tools.

For Codex agents, use the global Codex bridge skill at
`~/.codex/skills/gstack`. It resolves requests like `/office-hours`,
`/review`, or `/browse` to the matching Claude gstack skill under
`~/.claude/skills/gstack/<skill>/SKILL.md` and applies the playbook with Codex
tools.

## Acceptance Criteria

Binary checklists. Each item is yes/no, not vibes. A chapter does not ship if
any required box is unchecked.

### A chapter is "done" and ready for PR

- [ ] Thesis approved by Ram in writing (commit message or PR comment)
- [ ] `notes/research-NN.md` exists with ≥5 primary-source citations
- [ ] Every vendor/standards claim links to primary doc, not a blog
- [ ] Critic-agent review in PR thread (or `.private/critic-NN.md`); each
      finding resolved or marked won't-fix with reason
- [ ] No claim states more than its primary source supports
- [ ] At least one diagram or code snippet
- [ ] Word count 1,500–3,500
- [ ] Ram has read end-to-end in one sitting and approved
- [ ] CI green: links, markdown, spelling

### A demo is "ready to merge"

- [ ] Runs from a clean checkout with one documented command
- [ ] No paid external services (or local mock provided)
- [ ] README explains: what it shows, how to run, expected output
- [ ] Failure mode reproducible and visible in stdout
- [ ] Mitigated/fixed version included; both states demonstrated
- [ ] ≤500 LOC total (or stated exception with reason in PR)
- [ ] CI executes the demo end-to-end (or has a passing smoke test)
- [ ] Security framing reviewed by Ram: does the demo model a real threat

### The vendor matrix is "fresh"

- [ ] Every row has last-verified date within 35 days
- [ ] Every entry links to current primary doc
- [ ] Sunset/rebrand events flagged in a changelog row
- [ ] New entrants since last update explicitly considered
      (evaluated, added/not added)
- [ ] Diff posted as a monthly note

### Week 1 public push is "ready to make the repo public"

- [ ] Ch 1 draft merged with demo working
- [ ] README leads with Ch 1, not the outline
- [ ] LICENSE present (content CC BY 4.0, code MIT)
- [ ] AGENTS.md present
- [ ] Empty chapter stubs either removed from public view or have ≥1
      paragraph + thesis statement
- [ ] No `.private/` paths referenced in public files
- [ ] CI passing
- [ ] One-paragraph "who this is for" at top of README
- [ ] README read on mobile and renders cleanly

### The AI-native workflow is "working"

- [ ] Ram review time per chapter ≤4 hours total across all gates
- [ ] No chapter shipped requiring >1 post-merge IAM-accuracy correction
- [ ] Research-note → draft → revision turnaround ≤2 weeks per chapter
- [ ] Distribution drafts require ≤30 min Ram edit time
- [ ] At least 1 chapter shipped before grading the workflow as successful
- [ ] Critic-agent prompt includes a per-claim verification checklist,
      not generic "review for accuracy"
