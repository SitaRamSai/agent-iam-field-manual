# Design: Agent Identity Field Manual

Status: v0.2.1, Ch1-first launch confirmed on 2026-05-26 (revised after
/office-hours pressure-test). Throughput target: 1–2 chapters/month
steady-state, evenings/weekends.

## Problem

Platform, infra, and SRE engineers are starting to deploy LLM agents into
production, but practical guidance for agent identity, authorization, least
privilege, and auditability is still fragmented. Much public AI security writing
focuses on prompt injection and red-team tooling. Many agent tutorials focus on
app developers. The IAM layer for agents is scattered across vendor docs,
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

## AI-Native Workflow

The field manual is produced through an agentic workflow. Agents can research,
draft, review, test, and prepare distribution copy, but Ramsai owns the IAM
judgment and final approval.

Operating premise:

> Ramsai is the curator and IAM judgment layer for AI-produced research,
> explanation, demos, and distribution drafts.

The workflow is public because it affects the artifact: every chapter should
make the research trail, review path, demo behavior, and human approval gates
legible.

### Critic-agent prompt is versioned

The critic agent is the load-bearing AI role: it verifies IAM-truth before a
chapter ships. Generic "review for accuracy" prompts produce confident,
plausibly-wrong feedback. The critic prompt for this project is a
**per-claim verification checklist** that requires the critic to output a
structured table (one row per factual claim) with primary-source URL,
exact-match verdict, and IAM/threat/overstatement checks.

The prompt lives in `.private/critic-prompt-vN.md` and is **versioned**.
A chapter is critiqued under one frozen version. The prompt may evolve
between chapters but never mid-chapter.

### Throughput

Realistic steady-state: **1–2 chapters per month**, evenings/weekends. The
first chapter is slower (~4–6 weeks) because the workflow itself is being
debugged through it. The 8-chapter outline is a roadmap, not a calendar.

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
8. CI or local checks validate links, markdown, and demo execution.
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
- `notes/`
- `LICENSE`

Private files belong under `.private/` and should not be pushed:

- engagement target lists
- CFP strategy and abstract drafts
- commitment-tweet drafts
- detailed cadence, kill criteria, and personal operating notes

## Week 1 Public Bar

Week 1 launches with **Chapter 1 done**, not eight empty stubs. The bar is a
single finished artifact a platform engineer can read in 20 minutes and act on
tomorrow.

Ship at launch:

- Chapter 1 (`chapters/01-confused-deputy/chapter.md`), ~2,000 words, sourced
- Runnable PoC (`demos/01-confused-deputy/`), ≤200 LOC per file, framework-less
  Python, with both attack and mitigated versions
- `README.md` that leads with "who this is for" + Ch 1, not an outline
- `AGENTS.md` operating charter with acceptance criteria
- `DESIGN.md` (this file)
- `LICENSE` (CC BY 4.0 content + MIT code)
- `CLAUDE.md` project-level skill routing
- Minimal CI (`.github/workflows/ci.yml`) — markdown lint, link check, spell
  check, demo execution with assertions

Cut from the Week 1 surface:

- Empty chapter folders for Ch 2–8 (the README outline still references them
  as roadmap, but no empty `chapter.md` files ship publicly)
- `landscape/vendors.md` (skeleton stays, but not headlined; ships populated
  with Ch 3)
- Public framing of `notes/` (process directory, not reader-facing on launch)

Everything that looks like personal strategy, relationship targeting,
audience-fit validation, or pre-announcement copy stays private under
`.private/`.
