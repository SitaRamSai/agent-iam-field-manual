<!-- markdownlint-disable MD013 -->

# Research 01: The Confused Deputy Comes for Agents

**Status:** source map filled; ready to use as Chapter 1 drafting input.
**Chapter:** `chapters/01-confused-deputy/chapter.md`
**Last updated:** 2026-05-26

## Working Thesis

LLM agents are the textbook confused-deputy problem, given a fresh attack
surface and a louder operational failure mode: they act with authority granted
to the agent or tool runner while interpreting instructions from less-trusted
inputs.

## Source Map

This note uses primary sources only for chapter-facing claims. Secondary
commentary, press coverage, and summaries were intentionally omitted.

### S1: Hardy 1988, Confused Deputy

- DOI: `10.1145/54289.871709`.
- Open copy of the original paper:
  [UT Austin PDF](https://www.cs.utexas.edu/~witchel/S25-380L/papers/hardy88confused.pdf)
- Use for: the original confused-deputy framing and the compiler/billing-file
  example.
- Supported claim: a program can misuse authority granted to it when it acts on
  another party's request without distinguishing the authority source from the
  request source.

### S2: Saltzer And Schroeder 1975

- Primary source:
  [The Protection of Information in Computer Systems](https://www.cs.virginia.edu/~evans/cs551/saltzer/)
- Use for: least privilege and complete mediation.
- Supported claim: each program and user should operate with only the privileges
  needed for the job, and every access to every object should be checked for
  authority.
- Safe limitation: use this as a design-principle source. Do not claim the paper
  specifically discusses LLMs, OAuth, MCP, or modern workload identity.

### S3: OWASP LLM01 And LLM06

- Primary source:
  [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- Primary source:
  [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
- Use LLM01 for: indirect prompt injection through external sources such as
  websites or files, and the possibility that those sources alter model
  behavior.
- Use LLM06 for: excessive functionality, excessive permissions, excessive
  autonomy, least privilege for extensions, executing extensions in the user's
  context, user approval, and complete mediation in downstream systems.
- Safe limitation: LLM06 says logging and rate limiting do not prevent excessive
  agency, though they can limit or detect damage. Do not describe input
  sanitization as useless; OWASP lists it as a secure-coding measure.

### S4: Agent And Tool-Calling Documentation

- Primary source:
  [OpenAI Function Calling](https://developers.openai.com/api/docs/guides/function-calling)
- Primary source:
  [Anthropic MCP Connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector)
- Use OpenAI for: function definitions let the model pass data to application
  code, where code can access data or take actions suggested by the model.
- Use Anthropic for: Claude can connect to remote MCP servers through the
  Messages API, access MCP tools, allowlist or denylist tools, and use OAuth
  bearer tokens for authenticated MCP servers.
- Safe limitation: say the model requests, emits, or suggests tool calls.
  Application/runtime code executes them.

### S5: OAuth Token Exchange And Workload Identity

- Primary source:
  [RFC 8693, OAuth 2.0 Token Exchange](https://datatracker.ietf.org/doc/html/rfc8693)
- Primary source:
  [IETF WIMSE Workload Identity Practices draft](https://www.ietf.org/archive/id/draft-ietf-wimse-workload-identity-practices-00.html)
- Use RFC 8693 for: exchanging one token for another, resource and audience
  targeting, delegation and impersonation semantics, actor claims, and
  delegation history in JWT actor chains.
- Use WIMSE for: workload-identity practice context and the need to issue and
  scope workload credentials appropriately.
- Safe limitation: RFC 8693 is a protocol primitive. It does not by itself
  guarantee auditability, least privilege, or correct per-request policy.

### S6: AWS Confused-Deputy Guidance

- Primary source:
  [AWS IAM confused deputy](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html)
- Use for: a modern IAM example using the exact "confused deputy" term.
- Supported claim: AWS recommends condition keys such as `aws:SourceArn` and
  `aws:SourceAccount` in resource policies when an AWS service principal is
  granted access to a resource.
- Safe limitation: this is AWS cross-service confused-deputy guidance. It is
  not an end-to-end agent IAM solution.

## Claim Checklist

### Claim 1

- Source ID: S1.
- Evidence note: Hardy's paper presents a compiler that has billing-file write
  authority and can be induced to use that authority in a way the requesting
  user is not independently authorized to perform.
- Safe wording: "The confused deputy is a program that holds authority granted
  for one purpose but can be induced to use that authority while acting on a
  different party's request."

### Claim 2

- Source IDs: S1, S3, S4.
- Evidence note: S1 establishes the authority-confusion pattern. S3 establishes
  that external content can alter LLM behavior. S4 establishes that modern LLM
  systems can request tool use and that application/runtime code can use those
  tools to access data or take actions.
- Safe wording: "An LLM agent can fit the confused-deputy pattern when it reads
  attacker-controlled content and then requests tool actions that the
  application executes using the agent runtime's credentials or connected
  tool authority."

### Claim 3

- Source IDs: S2, S3.
- Evidence note: OWASP LLM01 lists prompt-injection mitigations such as
  constraining model behavior, validating output, filtering, limiting
  privileges, human approval, and segregating external content. OWASP LLM06
  separately recommends downstream authorization and complete mediation for
  tool and extension calls.
- Safe wording: "Input filtering and prompt hardening can reduce prompt
  injection risk, but they are not authorization boundaries. Downstream systems
  still need complete mediation for tool and resource access."

### Claim 4

- Source IDs: S2, S5.
- Evidence note: Saltzer and Schroeder support least privilege and complete
  mediation. RFC 8693 supports token exchange with resource and audience
  targeting, plus actor claims that can represent delegation.
- Safe wording: "A durable mitigation shape is principal separation, scoped
  delegation, least privilege, complete mediation, and logs that preserve the
  user, actor, resource, and authorization decision. OAuth token exchange is
  one useful primitive for implementing the delegation part of that pattern."

### Claim 5

- Source IDs: S4, S6.
- Evidence note: AWS documents confused-deputy controls for AWS service
  principals. Anthropic documents tool configuration and MCP authentication.
  OpenAI documents tool calling and allowed-tool controls. These are specific
  controls, not a complete agent IAM architecture.
- Safe wording: "Vendor documentation describes useful controls for narrowing
  tool or service authority, but Chapter 1 should not imply that any cited
  product solves end-to-end agent IAM unless the vendor's primary docs make
  that claim directly."

## Research Questions

### What exact wording from Hardy should define the confused deputy?

Use S1 for the original example and pull any direct quote from the PDF during
chapter drafting. Avoid paraphrases that make the paper sound like it used
modern IAM vocabulary.

### Which source best supports ambient authority?

Use S2 for the design-principle foundation and S6 as the modern platform-IAM
example. If the chapter uses the term "ambient authority," define it in plain
language and avoid implying Saltzer and Schroeder used that exact phrase.

### Which current source should support indirect prompt injection?

Use S3, specifically OWASP LLM01, for indirect prompt injection. Use OWASP
LLM06 only for the agency/permissions/complete-mediation angle.

### Should Chapter 1 cite vendor docs?

Yes, but sparingly. AWS is useful because it connects the confused-deputy term
to a modern IAM control pattern. OpenAI and Anthropic are useful only to
establish that agents can request tool execution and connect to tool servers.
Defer broader product comparison to Chapter 3.

### What minimum audit fields should the chapter name?

The minimum audit shape should be:

- user principal
- agent or runtime principal
- actor/delegation chain when present
- tool invoked
- resource touched
- authorization decision
- policy reason
- timestamp and request identifier

S2 supports complete mediation. S5 supports actor/delegation representation.
S4 and S6 support recording the tool/service surface involved in a request.

## Diagram Notes

Potential diagram shape:

```text
User A request
    |
    v
Agent runtime ---- reads ---- attacker-controlled content
    |
    | requests tool action using runtime/tool authority
    v
Private resource / tool API
    |
    v
Unauthorized disclosure or action
```

Mitigated version:

```text
User A request
    |
    v
Agent runtime
    |
    | requests scoped delegation
    v
Authorization boundary ---- logs ---- user, actor, tool, resource, decision
    |
    v
Allowed action only if user intent and resource scope match
```

## Do Not Ship Until

- [x] All placeholder URLs are replaced with primary sources.
- [x] At least five primary-source citations are present.
- [x] Every vendor or standards claim maps to a primary doc.
- [x] No claim states more than the linked source supports.
- [ ] Chapter text uses this note for citations instead of ad hoc links.
