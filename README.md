# Agent Identity — A Field Manual for Platform Engineers

## Who this is for

You run agents in production. Or you're about to. You already know IAM —
principals, scopes, capabilities, delegation, audit logs — and you know how
to wire authn/authz for human users and for services. What you don't have is
a single practical map for the new principal class showing up in your
infrastructure: the LLM agent that calls tools, touches tenant data, and
reasons across trust boundaries.

This manual treats the agent as a first-class principal and walks through
identity, authorization, least privilege, and audit patterns that apply to
it. The audience is platform, infra, and SRE engineers. The cadence is one
chapter at a time, shipped with a runnable demo where the principle benefits
from code.

## Start here: Chapter 1 — The Confused Deputy Comes for Agents

LLM agents are the textbook 1988 confused-deputy problem, given a fresh
attack surface and a much louder failure mode. The chapter walks the
classic compiler example, shows why agents are confused deputies by
construction, and ships a small, dependency-free Python PoC that
demonstrates the failure AND the IAM-shaped mitigation.

- Chapter: [`chapters/01-confused-deputy/chapter.md`](./chapters/01-confused-deputy/chapter.md)
- Demo: [`demos/01-confused-deputy/`](./demos/01-confused-deputy/)
  — runs in mock mode without an API key, or with a real LLM for a
  visceral version

## Outline (roadmap, not calendar)

Cadence is 1–2 chapters per month, evenings/weekends. Chapter folders are
created as each chapter enters the writer-agent pipeline; the roadmap below
is intentionally aspirational.

### Part I — Why Agent Identity

- **Ch 1: The Confused Deputy Comes for Agents** ✅ *(this is the launch)*
- **Ch 2: Why Prompt-Injection Defenses Aren't Enough** — the lethal-trifecta
  gap that IAM fills; Meta's Agents Rule of Two as context

### Part II — The Landscape

- **Ch 3: Who's Solving What** — Cloudflare Agent Tokens, AWS Verified
  Permissions, Auth0 FGA, Permit.io, Cerbos, WorkOS, SPIFFE-derived
  patterns, OWASP Agentic Top 10 mapping (ships with the live vendor
  matrix populated)
- **Ch 4: MCP and Tool Identity** — tool-poisoning + identity-aware tool
  gating

### Part III — Patterns

- **Ch 5: Least Privilege for Agents** — the OG IAM pattern re-applied
- **Ch 6: Identity-Aware Memory & Retrieval** — multi-tenant agent
  isolation, retrieval poisoning detection
- **Ch 7: Auditability & the Agent as a Principal**

### Part IV — Future

- **Ch 8: What Agent IAM Looks Like in 2028**

## How this manual is made

This repo is AI-native. Research, drafting, critic review, demo code, and
distribution copy go through agent pipelines; IAM judgment and final
approval are human gates. See [`DESIGN.md`](./DESIGN.md) for the production
workflow and [`AGENTS.md`](./AGENTS.md) for the operating charter and
acceptance criteria.

## Author

[SitaRam](https://github.com/SitaRamSai) — IAM background, currently writing
this manual chapter by chapter in public.

## License

Content under `chapters/` and `landscape/`: CC BY 4.0.
Code under `demos/`: MIT.
See [`LICENSE`](./LICENSE).
