# Agent IAM Vendor Landscape

Living document. Updates monthly. Last updated: 2026-05-26.

Format: one entry per vendor. Keep entries 100-200 words. Cite primary
sources (vendor docs, blog posts) over secondary coverage.

## Identity layer

### Cloudflare Agent Tokens
- **What it does:** _TODO_
- **Primitives:** _TODO_
- **Gaps:** _TODO_
- **When to pick:** _TODO_
- **Source:** _TODO_

### WorkOS (AuthKit for Agents)
- **What it does:** _TODO_
- **Primitives:** _TODO_
- **Gaps:** _TODO_
- **When to pick:** _TODO_
- **Source:** _TODO_

### SPIFFE / SPIRE (agent-adapted patterns)
- **What it does:** _TODO_
- **Primitives:** _TODO_
- **Gaps:** _TODO_
- **When to pick:** _TODO_
- **Source:** _TODO_

## Authorization layer

### AWS Verified Permissions (for agents)
- **What it does:** _TODO_
- **Primitives:** _TODO_
- **Gaps:** _TODO_
- **When to pick:** _TODO_
- **Source:** _TODO_

### Auth0 FGA (Fine-Grained Authorization)
- **What it does:** _TODO_
- **Primitives:** _TODO_
- **Gaps:** _TODO_
- **When to pick:** _TODO_
- **Source:** _TODO_

### Permit.io
- **What it does:** _TODO_
- **Primitives:** _TODO_
- **Gaps:** _TODO_
- **When to pick:** _TODO_
- **Source:** _TODO_

### Cerbos
- **What it does:** _TODO_
- **Primitives:** _TODO_
- **Gaps:** _TODO_
- **When to pick:** _TODO_
- **Source:** _TODO_

## Audit layer

(Mostly absent in 2026 — see Chapter 7. List candidates here as they emerge.)

## OWASP Agentic Top 10 → vendor mapping

| Risk | Identity | Authz | Audit |
|---|---|---|---|
| AT01 — Memory Poisoning | — | — | — |
| AT02 — Tool Misuse | — | — | — |
| AT03 — Privilege Compromise | — | — | — |
| AT04 — Resource Overload | — | — | — |
| AT05 — Cascading Hallucination | — | — | — |
| AT06 — Intent Breaking | — | — | — |
| AT07 — Misaligned Goals | — | — | — |
| AT08 — Identity Spoofing | — | — | — |
| AT09 — Overreliance | — | — | — |
| AT10 — Unexpected RCE | — | — | — |

Fill cells with vendor names as each is researched.
