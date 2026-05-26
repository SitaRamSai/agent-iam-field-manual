# Agent Identity — A Field Manual for Platform Engineers

A working manual for platform, infra, and SRE engineers deploying LLM agents
into production. Identity, authorization, and least-privilege patterns
applied to a new kind of principal.

Status: **v0.2 — outline locked, AI-native workflow defined, Chapter 1 in flight.**

## What this is

Much AI security writing in 2026 focuses on red-team tooling aimed at
researchers (PyRIT, Garak, HackAPrompt), while many agent-app tutorials are
aimed at developers (awesome-llm-apps). Meanwhile, vendors — Cloudflare Agent
Tokens, AWS Verified Permissions for agents, Auth0 FGA, Permit.io, Cerbos,
WorkOS, SPIFFE-derived patterns — are shipping agent-IAM features. The field
still lacks a single practical map a platform engineer can read in an afternoon
and act on tomorrow.

This is that map.

## Outline

### Part I — Why Agent Identity
- **Ch 1: The Confused Deputy Comes for Agents** *(with PoC demo)*
- **Ch 2: Why Prompt-Injection Defenses Aren't Enough** *(the lethal-trifecta gap that IAM fills; Meta's Agents Rule of Two as context)*

### Part II — The Landscape
- **Ch 3: Who's Solving What** *(Cloudflare Agent Tokens, AWS Verified Permissions, Auth0 FGA, Permit.io, Cerbos, WorkOS, OWASP Agentic Top 10 mapping)*
- **Ch 4: MCP and Tool Identity** *(tool-poisoning + identity-aware tool gating)*

### Part III — Patterns
- **Ch 5: Least Privilege for Agents** *(the OG IAM pattern re-applied)*
- **Ch 6: Identity-Aware Memory & Retrieval** *(multi-tenant agent isolation, retrieval poisoning detection)*
- **Ch 7: Auditability & the Agent as a Principal**

### Part IV — Future
- **Ch 8: What Agent IAM Looks Like in 2028**

## Cadence

Chapters ship as `chapter.md` in `chapters/NN-slug/`, mirrored to LinkedIn
long-form and X threads on launch. Vendor matrix in `landscape/vendors.md`
is a living document, updated monthly. Demo code in `demos/`.

See [`DESIGN.md`](./DESIGN.md) for the public design doc and AI-native
production workflow.

## Repo layout

```
.
├── README.md                    ← you are here
├── DESIGN.md                    ← public design doc + agent workflow
├── AGENTS.md                    ← operating charter for coding agents
├── CLAUDE.md                    ← project-level gstack skill routing
├── chapters/
│   ├── 01-confused-deputy/      ← chapter.md + diagrams (PoC links to /demos)
│   ├── 02-prompt-injection-gap/
│   ├── 03-landscape/
│   ├── 04-mcp-tool-identity/
│   ├── 05-least-privilege/
│   ├── 06-identity-aware-memory/
│   ├── 07-auditability/
│   └── 08-future/
├── demos/
│   └── 01-confused-deputy/      ← runnable PoC for Ch 1 (framework-less, ≤200 LOC)
├── landscape/
│   └── vendors.md               ← living vendor matrix, monthly updates
├── notes/
│   └── README.md                 ← public research-note conventions
└── .private/                    ← local strategy files, ignored by git
```

## Author

[Ramsai Goddu](https://github.com/) — IAM background, currently writing this
manual chapter by chapter in public.

## License

Content: CC BY 4.0. Code in `demos/`: MIT. See `LICENSE`.
