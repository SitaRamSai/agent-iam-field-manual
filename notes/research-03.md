<!-- markdownlint-disable MD013 -->

# Research 03: Who's Solving What

**Status:** source map filled; **thesis gate not yet cleared** — awaiting Ram's
written approval of the angle before the writer-agent draft begins.
**Chapter (planned):** `chapters/03-whos-solving-what/chapter.md`
**Companion artifact:** `landscape/vendors.md` (populated 2026-05-30, same cycle).
**Last updated:** 2026-05-30

## Working Thesis

As of mid-2026 there is no single "agent IAM" product. The market splits cleanly
into the two layers this manual already named. An **identity layer** answers
*what principal is this agent* — SPIFFE/SPIRE workload identity, and OAuth-for-MCP
from Cloudflare and WorkOS. An **authorization layer** answers *what is it allowed
to do* — Cedar/AWS Verified Permissions, Cerbos, Zanzibar-style Auth0 FGA, and
Permit.io. The **audit layer** is still mostly per-decision PDP logs, not
agent-session audit, and that gap is real (forward reference to Chapter 7).

There is a second axis, surfaced by reviewing the IAM incumbents: **buyer mode**.
The layers above are mostly *build-side* — primitives a developer wires into an
agent they ship. But the established IAM leaders (Okta, Microsoft Entra, AWS,
CyberArk, SailPoint, Ping) are entering from the *govern-side*: extending workforce
identity, IGA, and PAM to discover, govern, and **audit a fleet of already-deployed
agents** as a managed identity type, the way they manage employees. Notably, this
govern-side is where agent audit is *first actually shipping* (Okta streams tool
calls + authz decisions to a SIEM; CyberArk logs agent actions; SailPoint gives one
governed view) — so the "audit gap" is real for build-side tools but being closed
from the governance side. The chapter should present both axes: layer (identity /
authz / audit) and buyer mode (build vs govern).

The two 2025 framings from Chapter 2 — the lethal trifecta and the Rule of Two —
require *both* layers at once: you cannot bound a compromised agent's blast radius
with identity alone or authorization alone. So the platform engineer's job here is
**composition, not procurement**: choose an identity substrate, choose a policy
decision point, and wire least privilege between them. Chapter 3 maps each vendor
to the Chapter 1 primitives (principal, scoped delegation, complete mediation,
audit) and to which leg of the trifecta its control actually cuts — turning the
populated vendor matrix into a composition guide rather than a feature list.

This earns its place in the arc: Chapter 1 said treat the agent as a principal;
Chapter 2 said bound its authority; Chapter 3 says here is who sells the pieces,
how they fit, and — honestly — that nobody sells the whole thing and audit is the
hole.

## Source Map

Primary sources only. For a vendor's own product, the vendor's documentation *is*
the primary source (per `AGENTS.md`: link to primary doc, not third-party blog).
Every vendor doc below was re-verified on 2026-05-30 and is the same source backing
the matching row in `landscape/vendors.md`.

### S1: OWASP Agentic Security Initiative — Threats and Mitigations

- Primary source:
  [Agentic AI — Threats and Mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
  (OWASP GenAI Security Project). The Agentic Top 10 (AT01–AT10) taxonomy.
- Use for: the risk spine of the chapter and the matrix's OWASP→vendor mapping.
- Supported claim: OWASP enumerates agent-specific risks (memory poisoning, tool
  misuse, privilege compromise, identity spoofing, etc.) distinct from the LLM Top
  10.
- Safe limitation: it is a community taxonomy and mitigation catalog, not a
  benchmark or certification. Map vendors to risks only where access control
  *meaningfully* reduces the risk; do not imply OWASP endorses any vendor.

### S2: Cloudflare — MCP Authorization (Workers OAuth Provider + Access)

- Primary source:
  [Authorization](https://developers.cloudflare.com/agents/model-context-protocol/authorization/)
  (Cloudflare Agents docs) + library
  [workers-oauth-provider](https://github.com/cloudflare/workers-oauth-provider).
- Use for: how an MCP server on Workers issues its own OAuth 2.1 access token to
  the MCP client, federating to Cloudflare Access or a third-party IdP.
- Supported claim: Cloudflare implements the provider side of the OAuth 2.1 subset
  MCP uses; the Worker (MCP server) generates and issues a bound token to the
  client.
- Safe limitation: **no Cloudflare product ships as "Agent Tokens"** — that stub
  name was a placeholder. The documented primitive is OAuth for MCP. Identity here
  is the OAuth user/client, not a distinct agent workload identity.

### S3: WorkOS — AuthKit as the MCP authorization server

- Primary source:
  [Model Context Protocol](https://workos.com/docs/authkit/mcp) (WorkOS AuthKit
  docs) + [Connect](https://workos.com/docs/authkit/connect).
- Use for: AuthKit as a spec-compatible OAuth 2.0 authorization server fronting an
  MCP resource server; CIMD (added to the MCP spec Nov 2025) and DCR for client
  identification.
- Supported claim: AuthKit supplies the OAuth endpoints (authorize, token,
  introspection, JWKS, register); the MCP server only verifies AuthKit-issued JWTs
  and advertises protected-resource metadata.
- Safe limitation: this authenticates the user/client behind the agent and gives
  coarse OAuth-scope authorization; fine-grained per-resource decisions need a
  separate PDP (WorkOS FGA or other). Not workload identity for the agent process.

### S4: SPIFFE / SPIRE — workload identity

- Primary source:
  [SPIFFE Concepts](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/)
  (spiffe.io) and the SPIFFE specifications referenced there.
- Use for: cryptographic, secretless workload identity as the substrate beneath
  higher-level auth — SPIFFE ID, SVID (short-lived X.509 or JWT), trust domain,
  Workload API, attestation, automatic rotation.
- Supported claim: a workload (which can be an agent process) obtains an SVID via
  the Workload API after platform attestation, with no co-deployed secret, and
  keys are short-lived and rotated.
- Safe limitation: SPIFFE is **identity/authentication only** — it has no
  authorization policy engine, and no agent- or LLM-specific concept. "Agent
  identity" is a modeling convention on top of workload identity.

### S5: AWS Verified Permissions — Cedar PDP

- Primary source:
  [What is Amazon Verified Permissions?](https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/what-is-avp.html)
  (AWS docs). Cedar v4.7.
- Use for: externalized, policy-as-code authorization — `IsAuthorized` over
  principal/action/resource/context returns allow or deny.
- Supported claim: AVP evaluates Cedar policies and returns an access decision; it
  **presumes the principal was already identified and authenticated** by other
  means (Cognito, OIDC).
- Safe limitation: authorization only; no identity, delegation, or human-in-the-
  loop. The agent is modeled as a Cedar principal by you. Cedar's value is
  analyzable, decoupled policy — do not claim AVP provides agent identity.

### S6: Auth0 — Auth0 for AI Agents + Auth0 FGA (Zanzibar lineage)

- Primary source:
  [Auth0 for AI Agents — Overview](https://auth0.com/ai/docs/intro/overview) and
  [Auth0 FGA docs](https://docs.fga.dev/).
- Use for: the most complete agent-on-behalf-of-user story — user auth, **Token
  Vault** (third-party API tokens), **asynchronous authorization** (CIBA
  human-in-the-loop), and **FGA document-level filtering for RAG** (ReBAC,
  relationship tuples + Check API).
- Supported claim: Auth0 lets an agent call third-party APIs without holding the
  credentials (Token Vault), request human approval out-of-band (CIBA), and filter
  RAG retrieval by the user's FGA permissions.
- Safe limitation: several AI features are recent/preview; RAG filtering secures
  retrieval, not the model's reasoning; FGA carries a Zanzibar modeling learning
  curve. Vendor-managed SaaS.

### S7: Permit.io — Four-Perimeter Framework + MCP Gateway

- Primary source:
  [The 4-Perimeter Framework](https://docs.permit.io/ai-security/framework) and
  [Permit MCP Gateway](https://docs.permit.io/permit-mcp-gateway/).
- Use for: a single authorization layer spanning app and agent perimeters (prompt
  filtering, RAG data protection, secure external access, response enforcement),
  plus MCP gating with consent/audit and human-approval via Access Request MCP.
- Supported claim: Permit pairs an RBAC/ABAC/ReBAC PDP with AI-specific perimeters
  and an MCP Gateway that adds auth/consent/audit to MCP servers.
- Safe limitation: several AI components are framework integrations/guides/SDKs,
  not a single turnkey managed product; **prompt/response filtering is not a hard
  security boundary** (overlaps content safety). Newer, smaller vendor — do not
  overstate maturity.

### S8: Cerbos — stateless policy-as-code PDP

- Primary source: [Cerbos documentation](https://docs.cerbos.dev/cerbos/latest/).
- Use for: self-hostable, low-latency authorization decoupled from app code — YAML
  resource/principal policies, derived roles, conditions, a policy test framework.
- Supported claim: Cerbos is a stateless PDP that evaluates policies per request
  and returns allow/deny; it stores no data and runs anywhere.
- Safe limitation: authorization only, like AVP — assumes an authenticated
  principal; no agent identity or delegation primitives; ReBAC is less native than
  Zanzibar-style tools.

### S9 (supporting): MCP authorization spec + Zanzibar (foundations)

- Primary sources:
  [MCP Authorization specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)
  and Google's
  [Zanzibar paper](https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/).
- Use for: the standards both the Cloudflare/WorkOS OAuth story (MCP spec) and the
  Auth0 FGA model (Zanzibar) descend from — so the chapter explains the lineage,
  not just the brands.
- Safe limitation: cite these as the origin of the pattern; do not attribute
  vendor-specific behavior to the spec/paper.

### S10: Okta for AI Agents (govern-side, vendor-neutral)

- Primary source:
  [Okta for AI Agents](https://www.okta.com/products/govern-ai-agent-identity/) and
  newsroom
  [Okta expands AI agent security to any IdP](https://www.okta.com/newsroom/articles/okta-expands-ai-agent-security-to-any-idp/).
- Use for: the clearest example of the govern-side — discover, import/register
  (agents as identities with a human owner), resource connections, access
  certifications, single-action deactivation, and SIEM telemetry of tool calls +
  authz decisions; vendor-neutral (works with any IdP); integrates AWS Bedrock
  AgentCore.
- Supported claim: Okta governs deployed agents as a managed identity type across
  platforms without replacing existing human IAM, and streams agent action audit
  to a SIEM.
- Safe limitation: distinct from Auth0 for AI Agents (S6, build/CIAM side). A
  governance/lifecycle layer, not a runtime auth library; some capabilities only
  recently GA and some builder integrations are "coming soon."

### S11: Microsoft Entra Agent ID

- Primary source:
  [Microsoft Entra Agent ID](https://www.microsoft.com/en-us/security/business/identity-access/microsoft-entra-agent-id).
- Use for: incumbent (Microsoft) extending Entra — Conditional Access, identity
  governance, identity protection — to agent identities, included with Microsoft
  Agent 365.
- Supported claim: Entra assigns agents a built-in identity for authentication and
  policy enforcement and governs their lifecycle with familiar Entra controls.
- Safe limitation: Microsoft-ecosystem-centric; several capabilities are preview /
  rolling out. Authorization is Conditional Access policy, not a fine-grained
  external PDP. Word as "preview/early," not GA depth.

### S12: AWS — Amazon Bedrock AgentCore Identity

- Primary source:
  [AgentCore Identity](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html).
- Use for: an incumbent cloud identity service purpose-built for agents — agent
  identities as workload identities, inbound JWT authorizer, outbound credential
  providers for third-party APIs, audit trails; integrates AgentCore Runtime and
  Gateway.
- Supported claim: AgentCore Identity provides managed agent identity + credential
  management so agents access AWS and third-party services on a user's behalf.
- Safe limitation: Bedrock AgentCore-centric; pairs with (does not replace) Cedar /
  Verified Permissions for fine-grained policy. New service.

### S13: CyberArk Secure AI Agents

- Primary source:
  [Secure AI Agents](https://www.cyberark.com/solutions/secure-agentic-ai/).
- Use for: the PAM framing — agents as privileged identities; discovery + context
  enrichment; an AI Agent Gateway granting just-in-time, task-scoped privilege with
  automatic revocation toward zero standing privileges; action/communication
  logging.
- Supported claim: CyberArk applies least privilege, zero standing privilege, and
  audit to autonomous agents via an enforcement Gateway.
- Safe limitation: PAM/privilege framing; newer offering. Do not imply it is a
  general-purpose agent build-side auth library.

### S14: SailPoint Agent Identity Security (Agentic Fabric)

- Primary source:
  [Agent Identity Security](https://www.sailpoint.com/products/agent-identity-security)
  and [Agentic Fabric](https://www.sailpoint.com/products/agentic-fabric).
- Use for: the IGA incumbent extending governance to agents — one governed view of
  agents, their users, and the tools they access; aggregates agents from AWS,
  Azure, GCP, Salesforce.
- Supported claim: SailPoint brings agents into its identity-governance platform
  with ownership, access governance, and certification.
- Safe limitation: governance/IGA layer, enterprise-suite oriented; capabilities
  maturing. Keep claims at the level the product page supports (some detail did not
  render for extraction; do not over-specify).

### S15: Ping Identity — Identity for AI (Agentic AI Identity)

- Primary source:
  [Agentic AI Identity](https://www.pingidentity.com/en/solution/agentic-ai-identity.html)
  and press release
  [Redefines the Identity Control Plane for the Agentic Enterprise](https://press.pingidentity.com/2026-05-27-Ping-Identity-Redefines-the-Identity-Control-Plane-for-the-Agentic-Enterprise)
  (2026-05-27).
- Use for: another incumbent repositioning around an identity control plane for
  agents — trusted identities, real-time authorization, human oversight, bot/agent
  differentiation.
- Supported claim: Ping is extending its identity platform to agentic users with
  discovery, agent identity, and human-in-the-loop oversight.
- Safe limitation: early/announced (May 2026); shipped depth still emerging.
  Present as direction-of-travel, not mature product.

## Claim Checklist

### Claim 1 — There is no end-to-end "agent IAM" product yet; the market is layered

- Source IDs: S2–S8 (synthesis), S1.
- Evidence note: identity-layer vendors (S2, S3, S4) and authorization-layer
  vendors (S5, S6, S7, S8) are distinct products; no single doc describes one
  product covering identity + authorization + agent-session audit.
- Safe wording: "As of this writing, no vendor sells a complete agent IAM stack.
  You compose one — an identity substrate plus a policy decision point — and the
  audit layer is still mostly decision logs."

### Claim 2 — Identity tools and authorization tools answer different questions

- Source IDs: S4, S5, S8.
- Evidence note: SPIFFE is identity with no authz engine; AVP "presumes the
  principal has been previously identified and authenticated"; Cerbos likewise
  assumes an authenticated principal.
- Safe wording: "Identity-layer tools say *who the agent is*; authorization-layer
  tools say *what it may do* and assume identity is already established. Buying one
  does not get you the other."

### Claim 3 — OAuth-for-MCP authenticates the user/client behind the agent, not the agent as a workload

- Source IDs: S2, S3, S4.
- Evidence note: Cloudflare/WorkOS issue OAuth tokens tied to a user or client;
  SPIFFE issues an SVID to the workload itself after attestation.
- Safe wording: "OAuth-for-MCP (Cloudflare, WorkOS) proves *the human or app on
  whose behalf the agent acts*. Workload identity (SPIFFE) proves *the agent
  process*. They are not interchangeable; production agents often need both."

### Claim 4 — Policy model is a real choice: Cedar vs Zanzibar-ReBAC vs YAML PDP

- Source IDs: S5, S6, S8.
- Evidence note: AVP uses Cedar; Auth0 FGA uses Zanzibar-style relationship
  tuples; Cerbos uses YAML resource/principal policies. RAG and relationship-heavy
  cases favor ReBAC.
- Safe wording: "The authorization layer is not one thing. Cedar (AVP) is
  analyzable policy-as-code, Zanzibar-style ReBAC (Auth0 FGA) shines for
  relationship and per-document RAG checks, and Cerbos is git-managed YAML with no
  central data store. Pick for your data shape."

### Claim 5 — Human-in-the-loop approval is the concrete enforcement of Rule-of-Two "supervision"

- Source IDs: S6, S7, and Chapter 2's Meta Rule of Two (carried).
- Evidence note: Auth0 CIBA and Permit Access Request MCP implement out-of-band
  approval; Meta's Rule of Two requires supervision when an agent needs all three
  trifecta legs in one session.
- Safe wording: "When an agent genuinely needs untrusted input, sensitive access,
  and external action together, the Rule of Two says require human approval.
  Auth0's CIBA flow and Permit's Access Request MCP are where that rule becomes a
  shipped control."

### Claim 6 — Audit is the build-side gap, closing from the govern-side

- Source IDs: S5–S8 (decision logs); S10, S13, S14 (govern-side telemetry);
  absence of any standalone agent-session audit product.
- Evidence note: build-side PDPs (AVP, Auth0 FGA, Permit, Cerbos) emit per-decision
  logs; govern-side incumbents ship agent-action audit as a feature (Okta → SIEM,
  CyberArk action logs, SailPoint governed view). Neither yet sells standalone
  agent-session audit (identity → tool call → data touched → external action).
- Safe wording: "Every PDP logs its decisions, and the IAM incumbents now stream
  agent actions into governance suites — real audit primitives both. What no one
  sells yet as a standalone product is *agent-session* audit, the full chain from
  identity through tool call to external effect. Chapter 7 takes this up."

### Claim 7 — Overstatement guards (for the critic pass)

- The following must not be overstated in the draft:
  - "Cloudflare Agent Tokens" is **not** a shipped product name (S2).
  - Permit's prompt/response filtering is **not** a hard security boundary (S7).
  - Several Auth0 "for AI Agents" features are recent/preview, not mature GA (S6).
  - The OWASP→vendor mapping is *where access control helps*, not an OWASP
    endorsement (S1).
  - Microsoft Entra Agent ID (S11) and Ping (S15) are partly **preview / announced**,
    not full GA depth — present as direction-of-travel.
  - Okta for AI Agents (S10) is the **govern-side**, distinct from Auth0 for AI
    Agents (build/CIAM); do not conflate the two Okta-owned products.
  - SailPoint detail (S14) is limited to what the product page supports; do not
    over-specify capabilities that did not render for verification.
- Safe wording: prefer "documents", "as of mid-2026", and "reduces" over
  "guarantees", "solves", or "the best".

### Claim 8 — Two buyer modes: build-side primitives vs govern-side incumbents

- Source IDs: S2–S8 (build-side) vs S10–S15 (govern-side).
- Evidence note: build-side vendors expose primitives a developer wires into an
  agent they ship; the IAM incumbents (Okta, Entra, AWS AgentCore, CyberArk,
  SailPoint, Ping) extend workforce identity / IGA / PAM to discover, govern, and
  audit fleets of already-deployed agents as a managed identity type.
- Safe wording: "There are two ways to buy agent IAM. If you're *building* an
  agent, you compose build-side primitives (identity + a PDP). If you're an
  enterprise *running* many agents, the IAM incumbents now extend the governance
  and PAM tooling you already own to treat agents like a new class of workforce
  identity — discovered, owned, certified, and deactivatable."

## Open Questions For Ram (thesis gate)

1. **Angle:** approve "composition, not procurement — map vendors to Ch1 primitives
   and trifecta legs," now with the added **build-side vs govern-side** axis the
   incumbent review surfaced? Or steer toward a different cut (e.g. a decision-tree
   buyer's-guide, or a deeper single-vendor walkthrough)?
2. **Scope:** the matrix now holds **13 vendors** — 7 build-side (Cloudflare,
   WorkOS, SPIFFE, AVP, Auth0 FGA, Permit, Cerbos) + 6 govern-side incumbents
   (Okta for AI Agents, Entra Agent ID, AWS AgentCore Identity, CyberArk,
   SailPoint, Ping). Cover all 13 in the chapter body, or feature a subset and
   table the rest? Pull any "considered" vendor (Saviynt, Aembit/Astrix,
   Oso/OpenFGA, Stytch/Descope, Google Vertex AI) up now?
3. **Diagram:** the stronger hero figure is now a **2×2** — layer (identity /
   authz / audit) × buyer mode (build / govern) — placing each vendor. OK, or
   prefer the OWASP→vendor grid, or the original identity×authz map?
