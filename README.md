# Agent Identity: A Field Manual for Platform Engineers

This is a practical field manual for platform, infrastructure, and SRE teams
deploying LLM agents into production.

The core claim is simple: once agents can call tools, read data, and act across
systems, they need identity and authorization boundaries that look more like
workload IAM than chatbot safety filters. Prompt-injection defenses matter, but
they are not enough to answer platform questions like: who is the agent acting
as, which tools can it call, what data can it retrieve, and how do we audit what
happened?

Status: **Chapter 1 first draft in progress**. The first demo is runnable; the
next pass is editorial tightening and source review.

## Who this is for

- Platform engineers building internal agent platforms
- SREs and infra engineers asked to put agent systems into production
- Security engineers mapping classic IAM controls onto agent workflows
- AI application teams that need a deployable authorization model

This is not a red-team catalog, a prompt-engineering guide, or a vendor-neutral
replacement for product docs. It is a map of the operating model: principles,
failure modes, patterns, and tradeoffs.

## Table of Contents

### Part I: Why Agent Identity

1. [The Confused Deputy Comes for Agents](./chapters/01-confused-deputy/chapter.md)

   A classic IAM failure mode becomes easier to trigger when an agent can read
   untrusted content and call privileged tools in the same workflow. This chapter
   introduces the problem with a small runnable demo: an agent is tricked into
   using its own authority for someone else's goal.

2. [Why Prompt-Injection Defenses Are Not Enough](./chapters/02-prompt-injection-gap/chapter.md)

   Prompt-injection mitigations reduce risk, but they do not define authority.
   This chapter explains the gap between content filtering, instruction
   hierarchy, and durable authorization controls, then shows where IAM belongs in
   the agent threat model.

### Part II: The Landscape

3. [Who Is Solving What](./chapters/03-landscape/chapter.md)

   Agent IAM is emerging across several product categories: edge tokens, fine
   grained authorization, workload identity, policy engines, audit systems, and
   AI security tools. This chapter maps the current vendor and open source
   landscape without pretending one category solves the whole problem.

4. [MCP and Tool Identity](./chapters/04-mcp-tool-identity/chapter.md)

   Tool protocols make agents useful, but they also create a new control plane.
   This chapter covers tool identity, tool poisoning, authorization-aware tool
   discovery, and the difference between authenticating a server and authorizing
   a specific agent action.

### Part III: Patterns

5. [Least Privilege for Agents](./chapters/05-least-privilege/chapter.md)

   Least privilege still works, but the subject, resource, and request context
   are different. This chapter translates familiar IAM patterns into scoped
   tools, delegated user authority, policy checks, and just-in-time access for
   agent workflows.

6. [Identity-Aware Memory and Retrieval](./chapters/06-identity-aware-memory/chapter.md)

   Memory and retrieval systems are authorization surfaces. This chapter covers
   tenant isolation, document-level permissions, retrieval poisoning, and why
   "the model saw it" must not become an implicit access grant.

7. [Auditability and the Agent as a Principal](./chapters/07-auditability/chapter.md)

   Production agents need accountable traces: which principal initiated the
   task, which agent executed it, which tools were called, which policy decisions
   were made, and what changed. This chapter defines an audit shape that infra
   teams can operate.

### Part IV: Future

8. [What Agent IAM Looks Like in 2028](./chapters/08-future/chapter.md)

   The end state is not every agent holding a god token or every action routed
   through human approval. This chapter sketches the likely shape of mature
   agent IAM: agent principals, short-lived credentials, policy-rich tools,
   auditable delegation, and platform-level guardrails.

## Working Artifacts

- [Project plan](./PLAN.md)
- [Vendor landscape](./landscape/vendors.md)
- [Chapter 1 demo](./demos/01-confused-deputy/)

## Shipping cadence

The first phase targets four shipped chapters in roughly 90 days, with Chapter 5
in flight by the end of that window. The default weekly budget is 10 hours:
chapter work comes first, distribution and engagement absorb variance.
