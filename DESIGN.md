# Design: Agent Identity Field Manual

Status: v0.2, AI-native workflow approved on 2026-05-26.

## Problem

Platform, infra, and SRE engineers are starting to deploy LLM agents into
production, but there is no canonical guide for agent identity, authorization,
least privilege, and auditability. Most public AI security writing focuses on
prompt injection and red-team tooling. Most agent tutorials focus on app
developers. The IAM layer for agents is still scattered across vendor docs,
classic workload-identity patterns, and emerging authorization products.

This project is a public field manual for that gap.

## Audience

The primary reader is a platform engineer responsible for running agents in
production. They need practical patterns, vendor context, and runnable examples,
not a research survey or a vendor pitch.

Secondary readers include AI security engineers, IAM practitioners, SREs,
security architects, and vendor engineers building the primitives.

## Premises

1. Agent identity becomes a platform concern once agents call tools, touch
   tenant data, and operate across trust boundaries.
2. Prompt-injection defenses are necessary but insufficient; the durable control
   plane is identity, authorization, least privilege, and audit.
3. The useful artifact is a book-shaped manual, shipped chapter by chapter, with
   demos and a maintained vendor matrix.
4. The project should be transparent about how it is made: agents can draft,
   research, review, and test, while Ramsai owns IAM judgment and final approval.

## AI-Native Pivot

The original plan assumed Ramsai would be the primary writer, with AI assisting.
The approved pivot is stronger: the field manual is produced by an agentic
workflow, and the workflow itself is part of the story.

New operating premise:

> Ramsai is the curator and IAM judgment layer for AI-produced research,
> explanation, demos, and distribution drafts.

That changes the moat. The credibility is not "AI wrote this for me." The
credibility is "I designed and oversee the agent system that produces this, and
I review it with IAM taste and domain judgment."

## Production Workflow

Each chapter should move through the same pipeline:

1. Ramsai provides a one-sentence chapter intent.
2. A research agent writes `notes/research-NN.md` from primary sources, vendor
   docs, standards, and prior art.
3. Ramsai confirms the thesis and angle.
4. A writer agent drafts `chapters/NN-slug/chapter.md`.
5. A critic agent reviews the draft for IAM accuracy, missing threat models,
   weak claims, and unsupported vendor statements.
6. The writer agent revises the chapter.
7. A demo agent builds runnable code when the chapter needs a PoC.
8. CI checks links, markdown, and demo execution.
9. Ramsai reviews the pull request and approves the public version.
10. A distribution agent drafts LinkedIn and X copy from the merged chapter.
11. Ramsai approves voice and posts manually.

Execution model: use one workspace or branch per chapter so agents can work in
parallel without mixing chapter drafts, demos, and review notes.

## Agent Roles

- Research agent: source gathering, summaries, and citations.
- Writer agent: chapter drafts from approved research and outline.
- Critic agent: adversarial IAM review and claim checking.
- Demo agent: runnable PoCs and tests for demo chapters.
- Distribution agent: launch posts, threads, and repurposed summaries.
- Landscape agent: recurring vendor-matrix updates.

Agents may draft and propose. They do not approve final claims, publish social
posts, DM people, or merge without human review.

## Oversight Gates

- Thesis gate: Ramsai confirms the chapter angle before drafting.
- PR gate: Ramsai checks IAM truth, tone, and risk before merge.
- Distribution gate: Ramsai approves public posts before publishing.
- Monthly landscape gate: Ramsai decides which vendor updates are real product
  signal versus marketing copy.

## Public And Private Files

Public files should explain the manual and show the agentic workflow:

- `README.md`
- `DESIGN.md`
- `AGENTS.md`
- `CLAUDE.md`
- `chapters/`
- `demos/`
- `landscape/`
- `LICENSE`

Private files belong under `.private/` and should not be pushed:

- engagement target lists
- CFP strategy and abstract drafts
- commitment-tweet drafts
- detailed cadence, kill criteria, and personal operating notes

## Week 1 Public Bar

Week 1 should only push what supports the public artifact:

- outline and repo structure
- chapter stubs
- demo placeholder
- vendor-matrix skeleton
- agent operating charter
- license
- project-level AI/gstack instructions

Everything that looks like personal strategy, relationship targeting, or
pre-announcement copy stays private.
