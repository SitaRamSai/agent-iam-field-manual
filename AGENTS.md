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
