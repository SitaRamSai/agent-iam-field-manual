# Chapter 3: Who's Solving What

> There is no single "agent IAM" product. The market splits by layer —
> identity, authorization, audit — and by buyer mode — build-side
> primitives versus govern-side suites. Your job is composition, not
> procurement.

Chapter 2 ended at the authorization layer and called it a market. This
chapter is the map of that market. The reader arriving here is convinced:
prompt injection is unsolved, input filters do not hold, and the durable
control is bounding what a compromised agent is *authorized* to do. So you
go looking for the product that does that — and you find chaos. Dozens of
vendors, three different definitions of "agent identity," cloud providers
and identity incumbents and open-source policy engines all using the word
"agent" in their headlines, and not one box on a pricing page labeled the
thing you actually want.

The chaos is navigable once you see that it is organized along two axes.
This chapter draws both, places the current field on them, and shows how to
read the landscape as a composition problem. The exhaustive, dated,
primary-sourced detail lives in the companion vendor matrix
(`landscape/vendors.md`); the chapter teaches you how to use it.

## No one sells "agent IAM" — the market is layered

The first axis is the one Chapter 1 already gave you. IAM for any principal
decomposes into three questions: *who is this principal* (identity), *what
may it do* (authorization), and *what did it do* (audit). The agent market
maps onto exactly those three layers, and — crucially — the foundational,
single-purpose tools each answer only one of them. (The larger suites later
in this chapter span two or three; the buyer's trap is the pure-play
primitive that looks like it does more than it does.)

That is not a criticism. It is the single most important fact for a buyer.
SPIFFE issues a workload an identity and has no opinion about what that
workload may do. AWS Verified Permissions decides whether an action is
allowed and explicitly "presumes that the principal has been previously
identified and authenticated through other means."[^avp] One proves who;
the other decides what; neither does the other's job. If you buy an
identity product expecting authorization, or a policy engine expecting it
to know who the agent is, you will ship a gap.

OWASP's Agentic Security Initiative threat taxonomy is a useful spine for
why all three matter: its threats run from identity spoofing through
privilege compromise to tool misuse, and the mitigations are different
controls at different layers.[^owasp] Keep that taxonomy in view as a
checklist, not as a shopping list — no vendor "covers" an OWASP threat the
way a feature ticks a box.

## The identity layer: what principal is the agent?

Three things live here, and they answer the identity question in two
genuinely different ways.

**SPIFFE and SPIRE** issue *workload* identity. A SPIFFE ID is a URI like
`spiffe://trust-domain/path`; the agent process calls the Workload API,
proves itself through platform attestation, and receives a short-lived,
automatically rotated SVID — an X.509 certificate or JWT — with no secret
co-deployed.[^spiffe] This is identity for the agent *as a running thing*.
It is also identity-only: SPIFFE has no policy engine, and "agent identity"
is your modeling convention layered on top of workload identity.

**Cloudflare and WorkOS** answer a different question: who is the *user or
client* on whose behalf the agent acts. Both implement OAuth for the Model
Context Protocol. Cloudflare's Workers OAuth Provider lets an MCP server
issue its own scoped, bound access token to an MCP client and federate to
Cloudflare Access or a third-party IdP.[^cf] (Note: despite the placeholder
name some roadmaps carry, Cloudflare ships no product called "Agent Tokens"
— the documented primitive is OAuth for MCP.) WorkOS AuthKit plays the
spec's authorization-server role in front of your MCP server, supplying the
authorize, token, and registration endpoints so your server only verifies
issued JWTs.[^workos]

The distinction is load-bearing and easy to miss: OAuth-for-MCP proves the
human or app behind the agent; SPIFFE proves the agent process itself. They
are not interchangeable, and a production agent often needs both — a
workload identity to run and a delegated user token to act on someone's
behalf.

## The authorization layer: what may it do?

This is the layer Chapter 2 pointed at, and it is not one thing. Four
vendors here make three different bets on how you express policy.

**AWS Verified Permissions** uses Cedar — analyzable policy-as-code. You
call `IsAuthorized` with principal, action, resource, and context and get
allow or deny.[^avp] **Cerbos** makes a similar bet with a different shape:
a stateless, self-hostable PDP where policies are YAML resource and
principal definitions, evaluated per request with no central data
store.[^cerbos] Both assume the principal is already authenticated and let
you model the agent as a principal.

**Auth0 FGA** makes the Zanzibar bet: relationship-based access control,
where authorization is a graph of relationship tuples queried through a
Check API.[^fga] That model shines for the per-document filtering a
retrieval-augmented agent needs, and Auth0 packages it inside a broader
"Auth0 for AI Agents" story — Token Vault, so an agent calls Google or Slack
without holding the credentials; asynchronous (CIBA) approval for
human-in-the-loop; and FGA filtering of what a RAG pipeline is allowed to
retrieve.[^fga] Several of those AI features are recent, so treat them as
direction-of-travel with real shipping pieces rather than mature GA depth.

**Permit.io** wraps an RBAC/ABAC/ReBAC PDP in an AI-specific "Four-Perimeter
Framework" and an MCP gateway that adds auth and consent to MCP servers.
[^permit] Two of its perimeters — prompt filtering and response enforcement
— are worth a caution: they reduce risk but are not hard security
boundaries, for exactly the adaptive-attacker reason Chapter 2 laid out.
Its access-control perimeters, and its Access Request flow for human
approval, are the parts that sit on the durable layer.

The choice among these is a data-shape question. Relationship-heavy or
per-document? Lean Zanzibar (Auth0 FGA). Want analyzable policy in an
AWS-centric stack? Cedar (Verified Permissions). Want git-managed YAML with
no data store, self-hosted anywhere? Cerbos. Want one layer spanning app and
agent perimeters and willing to assemble it? Permit.io.

## The second axis: build-side versus govern-side

Everything so far is what I will call **build-side**: primitives a developer
wires into an agent they are building. But ask a different buyer — a
security leader at an enterprise that now has hundreds of agents deployed
across SaaS, clouds, and platforms they did not all build — and the
build-side answer is useless. They are not wiring auth into one agent. They
need to discover the agents that already exist, assign each an owner, decide
what each may reach, certify that access on a schedule, and kill a rogue one
fast.

That is **govern-side**, and it is where the IAM incumbents have arrived —
extending the workforce identity, governance, and privileged-access tooling
they already sell to treat agents as a new class of identity.

**Okta for AI Agents** is the clearest example, and it is deliberately
vendor-neutral: it works with any IdP, so Entra ID or Ping can stay the
system of record for humans while Okta governs the agent fleet. It
discovers agents by watching for new OAuth consent grants, imports and
registers them as identities with a human owner, defines which resources
each may reach, runs access requests and certifications, deactivates an
agent in one action, and — notably — streams the agent's tool calls and
authorization decisions to a SIEM.[^okta] (This is a distinct product from
Auth0 for AI Agents, the build-side story above; Okta owns both.)

The rest of the incumbents are arriving on the same axis from their
home turf:

- **Microsoft Entra Agent ID** gives agents a first-class identity governed
  by familiar Entra controls — Conditional Access, identity governance,
  identity protection — for agents managed in Microsoft Agent 365, with
  capabilities rolling out alongside that control plane.[^entra]
- **AWS Bedrock AgentCore Identity** implements agent identities as
  *workload* identities with credential management, an inbound JWT
  authorizer, and outbound credential providers, integrated with the
  AgentCore runtime and gateway.[^agentcore] (It is the bridge between the
  two axes: a cloud provider's build-side identity service that the
  govern-side then governs — Okta imports AgentCore agents directly.)
- **CyberArk Secure AI Agents** brings the PAM playbook: treat the agent as
  a privileged identity, route it through an AI Agent Gateway that grants
  just-in-time, task-scoped privilege and revokes it toward zero standing
  privileges, and logs the agent's actions and communications.[^cyberark]
- **SailPoint Agent Identity Security** brings the IGA playbook: aggregate
  agents from AWS, Azure, GCP, and Salesforce into one governed view with
  ownership and certification.[^sailpoint]
- **Ping Identity** is repositioning its platform around an identity control
  plane for agents — trusted identities, real-time authorization, human
  oversight — though as of this writing it is more announced than
  shipped.[^ping]

The pattern is unmistakable: the established identity industry has decided
agents are a managed identity type, and they are extending IGA and PAM to
cover them.

## Audit: the gap the govern-side is starting to fill

Chapter 1 named audit as the third IAM question, and on the build-side it is
the thin layer. Every PDP — Cerbos, Verified Permissions, Permit.io, Auth0
FGA — can log its decisions, and that is a real authorization audit trail.
But no build-side product sells *agent-session* audit: the full chain from
identity, through each tool call, to the data touched and the external
action taken.

The govern-side is where that begins to close. Okta streaming tool calls and
authorization decisions to a SIEM,[^okta] CyberArk logging every agent
action through its gateway,[^cyberark] and SailPoint's single governed view
[^sailpoint] are the first agent-action audit shipping as a feature rather
than a log line. It is not yet a standalone product, and the
session-spanning view is still incomplete — Chapter 7 returns to what good
agent auditability should look like. For now, note the asymmetry: if audit
matters to you and you are build-side, you are assembling it yourself.

## How to read the map

Put the two axes together and the field stops looking like chaos:

```text
                 build-side                |        govern-side
                 (wire into one agent)     |        (govern a fleet)
   -------------+---------------------------+----------------------------
   IDENTITY     | SPIFFE/SPIRE (workload)   | Okta for AI Agents
                | Cloudflare, WorkOS (MCP)  | Entra Agent ID
                |                           | AWS AgentCore Identity
   -------------+---------------------------+----------------------------
   AUTHORIZATION| AVP/Cedar, Cerbos         | CyberArk (PAM / least priv)
                | Auth0 FGA, Permit.io      | SailPoint (IGA / certify)
   -------------+---------------------------+----------------------------
   AUDIT        | PDP decision logs only    | Okta->SIEM, CyberArk logs,
                | (assemble it yourself)    | SailPoint governed view
```

Reading it well means refusing the question "which one should I buy?" You do
not buy a box; you compose a row-and-column path. If you are *building* an
agent, you pick an identity substrate (a workload identity and/or a
delegated user token) and a policy decision point, and you wire the PDP into
your tool boundary. If you are an enterprise *running* many agents, you
extend the governance and PAM tooling you already own to treat agents like a
new class of workforce identity — discovered, owned, certified, and
deactivatable.

And you map your choices back to Chapter 1's primitives and Chapter 2's
trifecta. The identity layer establishes the **principal**. The
authorization layer is where **scoped delegation** and **complete mediation
at the tool boundary** live — the enforcement point that decides whether the
agent's session holds a dangerous combination of capabilities. The audit
layer is **accountability**. A vendor that gives you a strong principal but
no mediation has cut one trifecta leg and left two; a PDP with no identity
does not know whose authority it is checking.

## A worked composition

Concretely, a support agent that reads customer tickets (untrusted input),
looks up account data (private data), and can issue refunds (external
action) — all three trifecta legs — composes like this:

```text
SPIFFE SVID  --> support agent --> requested tool call (issue refund)
(workload ID)        |                        |
Auth0 Token Vault    |                        v
(delegated access    |            [ PDP at the tool boundary ]
 to billing API) ----+             - Cerbos/Cedar: is THIS agent allowed
                                     THIS action on THIS account, now?
                                   - rule of two: refund + private data +
                                     untrusted input -> require human approval
                                     (Auth0 CIBA)
                                          |
                       allow only if scoped + approved; else REFUSED
                                          |
                          Okta / SIEM  <-- every decision + tool call logged
```

No single vendor in that diagram is doing all the work, and none of the
primitives is exotic — workload identity, delegated tokens, a policy
decision point at the boundary, human approval for the dangerous
combination, and a decision log. They are the access-control primitives
platform engineers already operate, pointed at the agent's tool surface.

The field is larger than the thirteen vendors mapped here — non-human
identity startups, open-source policy engines, and more incumbents are
entering each quarter, and the matrix tracks them as they earn a
chapter-facing claim. But the two axes are stable. New entrants land
somewhere on this grid; they do not redraw it.

## What's next

The composition above hides a hard problem inside one box: the tool
boundary. *Which* tool, invoked *how*, with *whose* identity attached? When
the agent speaks the Model Context Protocol, the tool itself becomes a
principal with an identity and a trust boundary of its own — and a new
attack surface. Chapter 4 takes up MCP and tool identity: tool poisoning,
identity-aware tool gating, and what it means to authorize not just the
agent but the tools it reaches for.

If you take one thing from this chapter, take this: stop looking for the
agent-IAM product. Learn the two axes, place your situation on the grid, and
compose the identity substrate, the policy decision point, and the audit
trail your agents actually need. The market is assembling the pieces faster
than it is assembling the whole — so assembly is the skill.

[^owasp]: OWASP, "Agentic AI — Threats and Mitigations," OWASP GenAI
    Security Project.
    <https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/>.

[^spiffe]: SPIFFE, "SPIFFE Concepts."
    <https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/>.

[^cf]: Cloudflare, "Authorization" (Agents / Model Context Protocol docs).
    <https://developers.cloudflare.com/agents/model-context-protocol/authorization/>.
    Library: <https://github.com/cloudflare/workers-oauth-provider>.

[^workos]: WorkOS, "Model Context Protocol" (AuthKit docs).
    <https://workos.com/docs/authkit/mcp>.

[^avp]: Amazon Web Services, "What is Amazon Verified Permissions?"
    <https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/what-is-avp.html>.

[^fga]: Auth0, "Auth0 for AI Agents — Overview"
    (<https://auth0.com/ai/docs/intro/overview>) and "Auth0 Fine-Grained
    Authorization" (<https://docs.fga.dev/>).

[^permit]: Permit.io, "The 4-Perimeter Framework."
    <https://docs.permit.io/ai-security/framework>.

[^cerbos]: Cerbos, "Documentation."
    <https://docs.cerbos.dev/cerbos/latest/>.

[^okta]: Okta, "Okta for AI Agents"
    (<https://www.okta.com/products/govern-ai-agent-identity/>) and
    "Okta expands AI agent security to support new agent ecosystems and any
    identity provider" (newsroom).
    <https://www.okta.com/newsroom/articles/okta-expands-ai-agent-security-to-any-idp/>.

[^entra]: Microsoft, "Microsoft Entra Agent ID."
    <https://www.microsoft.com/en-us/security/business/identity-access/microsoft-entra-agent-id>.

[^agentcore]: Amazon Web Services, "Provide identity and credential
    management for agent applications with Amazon Bedrock AgentCore
    Identity."
    <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html>.

[^cyberark]: CyberArk, "Secure AI Agents."
    <https://www.cyberark.com/solutions/secure-agentic-ai/>.

[^sailpoint]: SailPoint, "Agent Identity Security."
    <https://www.sailpoint.com/products/agent-identity-security>.

[^ping]: Ping Identity, "Identity for AI"
    (<https://www.pingidentity.com/en/solution/agentic-ai-identity.html>)
    and "Ping Identity Redefines the Identity Control Plane for the Agentic
    Enterprise" (May 27, 2026).
    <https://press.pingidentity.com/2026-05-27-Ping-Identity-Redefines-the-Identity-Control-Plane-for-the-Agentic-Enterprise>.
