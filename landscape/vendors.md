<!-- markdownlint-disable MD013 -->

# Agent IAM Vendor Landscape

Living document. Updates monthly. Last updated: 2026-05-30.

Format: one entry per vendor. Keep entries 100-200 words. Cite primary
sources (vendor docs, blog posts) over secondary coverage. Every entry was
re-verified against its primary source on the **last-verified** date shown.

> Scope note: this matrix maps the IAM control plane for agents — identity,
> authorization, and audit. It does not rank prompt-injection or content-safety
> tooling (see Chapter 2). "Agent identity" below means treating the agent as a
> first-class principal; several vendors authenticate the *user or client behind*
> the agent rather than the agent process itself, and that distinction is called
> out per entry. The market also splits by **buyer mode**: *build-side* primitives
> a developer wires into an agent they ship (Identity and Authorization layers
> below), versus *govern-side* suites the IAM incumbents use to govern a fleet of
> already-deployed agents (the Enterprise agent identity & governance section).

## Identity layer

### Cloudflare Agents (Workers OAuth Provider + Access)

- **What it does:** Cloudflare's Agents SDK runs each agent as a named Durable
  Object. For access, Cloudflare ships the Workers OAuth Provider library, which
  implements the provider side of the OAuth 2.1 subset that MCP uses: an MCP
  server on Workers issues its own scoped access token to the MCP client, and can
  federate to Cloudflare Access SSO or a third-party IdP (GitHub, Google, Auth0,
  WorkOS, Stytch).
- **Primitives:** OAuth 2.1 authorization-code flow; server-issued bound access
  tokens; Cloudflare Access policies/SSO; Durable Object stable names as agent
  instance identity.
- **Gaps:** No product literally named "Agent Tokens"; the shipped primitive is
  OAuth for MCP. Identity is the OAuth user/client, not a distinct agent
  principal; least privilege is per-token scope you define. Tied to the
  Workers/Durable Objects runtime.
- **When to pick:** You build or host MCP servers/agents on Cloudflare Workers and
  want spec-compliant OAuth + SSO without running your own authorization server.
- **Source:** <https://developers.cloudflare.com/agents/model-context-protocol/authorization/>
  (library: <https://github.com/cloudflare/workers-oauth-provider>).
  Last verified 2026-05-30.

### WorkOS AuthKit (MCP authorization)

- **What it does:** AuthKit acts as a spec-compatible OAuth 2.0 authorization
  server in front of your MCP server (the resource server). It supplies the OAuth
  endpoints MCP clients use — authorize, token, introspection, JWKS, register — so
  your MCP server only verifies AuthKit-issued JWTs and advertises protected-
  resource metadata.
- **Primitives:** OAuth 2.0 / OIDC; AuthKit Connect (OAuth + M2M
  `client_credentials` apps); Client ID Metadata Document (CIMD, added to the MCP
  spec Nov 2025) and Dynamic Client Registration; JWT verification against JWKS.
- **Gaps:** Authorization is coarse (OAuth scopes / roles); fine-grained per-
  resource decisions need WorkOS FGA or a separate PDP. It authenticates the user
  or client behind the agent, not the agent process as a workload.
- **When to pick:** A SaaS adding an authenticated MCP server that wants a managed
  OAuth server plus enterprise SSO instead of building DCR/CIMD by hand.
- **Source:** <https://workos.com/docs/authkit/mcp>. Last verified 2026-05-30.

### SPIFFE / SPIRE (agent-adapted workload identity)

- **What it does:** SPIFFE is an open standard and SPIRE its reference
  implementation for issuing cryptographic workload identity with no
  pre-provisioned secrets. A workload — which can be an agent process — calls the
  Workload API and is issued an identity document after platform attestation.
- **Primitives:** SPIFFE ID (`spiffe://trust-domain/path` URI); SVID (short-lived
  X.509 certificate or JWT); trust domain + trust bundle; Workload API with
  attestation; automatic, frequent key rotation.
- **Gaps:** Identity/authentication only — no authorization policy engine (pair
  with OPA, Cerbos, etc.). No agent- or LLM-specific concepts; "agent identity" is
  a modeling convention on top of workload identity. Operational weight (run SPIRE
  server and agents, configure attestation).
- **When to pick:** You run agents as workloads across clusters/clouds and want
  secretless, short-lived, mutually authenticated identity (mTLS) as the substrate
  beneath higher-level auth.
- **Source:** <https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/>.
  Last verified 2026-05-30.

## Authorization layer

### AWS Verified Permissions

- **What it does:** A managed, fine-grained authorization service (a PDP) built on
  the open-source Cedar policy language. The app calls `IsAuthorized` with
  principal / action / resource / context and receives an allow or deny decision.
- **Primitives:** Cedar policies (RBAC and ABAC), policy stores, schema, batch
  authorization; framework integrations (e.g. Express middleware). Cedar v4.7.
- **Gaps:** Authorization only — presumes the principal was already authenticated
  elsewhere (Cognito, OIDC). Agnostic to agents; no built-in agent identity,
  delegation, or human-in-the-loop. You model the agent as a Cedar principal and
  write the policies.
- **When to pick:** An AWS-centric stack that wants externalized, auditable,
  policy-as-code authorization for agent actions, with Cedar's analyzable
  semantics.
- **Source:** <https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/what-is-avp.html>.
  Last verified 2026-05-30.

### Auth0 FGA / Auth0 for AI Agents

- **What it does:** Auth0 FGA is a Zanzibar-style relationship-based authorization
  service. Auth0 packages it under "Auth0 for AI Agents" alongside user auth for
  agents, **Token Vault** (storing and refreshing third-party API tokens so agents
  call Google/Slack/GitHub without holding credentials), **asynchronous
  authorization** (CIBA human-in-the-loop approvals), and **FGA-based
  document-level filtering for RAG**.
- **Primitives:** relationship tuples + authorization model with a Check API
  (ReBAC); OAuth/OIDC user auth; Token Vault; CIBA async approval; RAG
  pre-filtering by permission.
- **Gaps:** Several AI features are recent/preview; ReBAC modeling has a Zanzibar
  learning curve. RAG filtering secures retrieval, not the model's reasoning.
  Vendor-managed SaaS.
- **When to pick:** You want agents acting on a user's behalf with delegated,
  revocable third-party access, human approval for sensitive actions, and
  per-document RAG authorization.
- **Source:** <https://auth0.com/ai/docs/intro/overview> ; FGA docs
  <https://docs.fga.dev/>. Last verified 2026-05-30.

### Permit.io

- **What it does:** Authorization-as-a-service (RBAC/ABAC/ReBAC over an
  OPA/Cedar-backed PDP) plus an AI-specific **Four-Perimeter Framework** and a
  **Permit MCP Gateway** that adds auth, consent, and audit to MCP servers without
  code changes.
- **Primitives:** PDP via `permit.check()`; policy models RBAC/ABAC/ReBAC/PBAC; the
  four perimeters (prompt filtering, RAG data protection, secure external access,
  response enforcement); Access Request MCP for human approval; MCP Gateway.
- **Gaps:** Several AI components are framework integrations, guides, and SDKs
  rather than a turnkey managed product; prompt/response filtering overlaps with
  content-safety tooling and is not a hard security boundary. Newer, smaller
  vendor.
- **When to pick:** You want one authorization layer spanning app and agent
  perimeters, with explicit MCP gating and human-approval flows, and will assemble
  the components.
- **Source:** <https://docs.permit.io/ai-security/framework>. Last verified
  2026-05-30.

### Cerbos

- **What it does:** An open-source, stateless authorization PDP. Policies written
  as YAML (resource policies, principal policies, derived roles) are evaluated per
  request over an API and return an allow/deny decision. Decoupled from app code;
  stores no data itself.
- **Primitives:** resource and principal policies, derived roles, conditions,
  attribute schemas; stateless PDP (self-host or Cerbos Hub); SDKs/API; a policy
  test framework.
- **Gaps:** Authorization only, like Verified Permissions — assumes an
  authenticated principal; no agent identity or delegation primitives, and no
  built-in agent/LLM features. ReBAC is less native than Zanzibar-style tools.
- **When to pick:** You want self-hostable, low-latency, git-managed policy-as-code
  for agent action authorization without a Zanzibar data store, in any cloud.
- **Source:** <https://docs.cerbos.dev/cerbos/latest/>. Last verified 2026-05-30.

## Enterprise agent identity & governance (IAM incumbents)

A second buyer mode. The vendors above are mostly **build-side** — primitives a
developer wires into an agent they ship. The vendors below are **govern-side**:
the established IAM leaders (workforce identity, IGA, PAM) extending their suites
to discover, govern, and audit a *fleet of deployed agents* as a managed identity
type, the way they already manage employees. This is where agent audit/governance
is first actually shipping.

### Okta for AI Agents

- **What it does:** Okta's workforce-side, vendor-neutral platform to discover,
  onboard, govern, and deactivate AI agents as a managed identity type — works
  with any IdP (Entra ID, Ping, etc. stay the human system of record). Distinct
  from Auth0 for AI Agents (the developer/CIAM side, listed above).
- **Primitives:** AI Agent Discovery (monitors new OAuth consent grants);
  Import/Registry (agents as identities with a human owner + baseline policy;
  imports agents built on AWS Bedrock AgentCore via the Okta Integration Network);
  Resource Connections (which resources, auth method, scopes); user access
  requests + certifications for agents; single-action deactivation; system logs
  and telemetry of tool calls + authorization decisions streamed to a SIEM.
- **Gaps:** a governance/lifecycle layer, not a runtime auth library; deepest
  support is per-builder (AgentCore, Salesforce Agentforce, ServiceNow; DataRobot,
  Boomi, Glean, Google Vertex AI, Workday "coming soon"). Some capabilities only
  recently GA.
- **When to pick:** an enterprise needing to govern a sprawling fleet of deployed
  agents across platforms without replacing its existing human IAM.
- **Source:** <https://www.okta.com/products/govern-ai-agent-identity/> ; newsroom
  <https://www.okta.com/newsroom/articles/okta-expands-ai-agent-security-to-any-idp/>.
  Last verified 2026-05-30.

### Microsoft Entra Agent ID

- **What it does:** extends Microsoft Entra to assign and govern agent identities,
  applying familiar controls — Conditional Access, identity governance, identity
  protection, network controls — to agents. Included for agents managed by
  Microsoft Agent 365 (the control plane for agents).
- **Primitives:** a built-in agent identity for authentication and policy
  enforcement; agent provisioning, metadata, and visibility (blueprints, tasks,
  logs); Conditional Access + identity governance + identity protection applied to
  agents; blocking of risky agents and access to risky resources.
- **Gaps:** Microsoft/Entra-ecosystem-centric; several capabilities are preview or
  rolling out with Agent 365. Authorization is via Conditional Access policy, not
  a fine-grained external PDP.
- **When to pick:** Microsoft/Entra shops governing agents alongside employees on
  their existing Conditional Access posture.
- **Source:** <https://www.microsoft.com/en-us/security/business/identity-access/microsoft-entra-agent-id>.
  Last verified 2026-05-30.

### AWS — Amazon Bedrock AgentCore Identity

- **What it does:** an identity and credential management service purpose-built for
  AI agents and automated workloads on AWS. Agent identities are implemented as
  workload identities with agent-specific attributes; it provides authentication,
  authorization, and credential management so agents and tools access AWS and
  third-party services on a user's behalf, with audit trails.
- **Primitives:** workload identity for agents; inbound JWT authorizer (who may
  call the agent); credential providers for outbound third-party API access (OAuth
  token handling); native integration with AgentCore Runtime and Gateway.
- **Gaps:** Bedrock AgentCore-centric; pairs with — does not replace —
  Cedar/Verified Permissions for fine-grained policy. New service.
- **When to pick:** building agents on Bedrock AgentCore and wanting managed agent
  identity plus secure third-party credential handling.
- **Source:** <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html>.
  Last verified 2026-05-30.

### CyberArk Secure AI Agents

- **What it does:** PAM-model security treating AI agents as privileged identities.
  Discovers agents across SaaS/cloud/dev environments, enriches each with context
  (owner, purpose, status, permissions), and enforces access through an AI Agent
  Gateway.
- **Primitives:** agent discovery + inventory; an AI Agent Gateway (enforcement
  point between agents and the tools they use) granting just-in-time, task-scoped
  privilege with automatic revocation toward **zero standing privileges**; logging
  of agent actions and communications for visibility and audit (what action, by
  which agent, on whose behalf).
- **Gaps:** a privilege-control / PAM framing; enforcement runs through the Gateway
  path. Newer offering on CyberArk's identity-security platform.
- **When to pick:** security teams applying least privilege, zero standing
  privilege, and audit to autonomous agents — especially where PAM already exists.
- **Source:** <https://www.cyberark.com/solutions/secure-agentic-ai/>. Last
  verified 2026-05-30.

### SailPoint Agent Identity Security (Agentic Fabric)

- **What it does:** extends SailPoint's identity governance (IGA) to AI agents,
  bringing agents, their users, and the tools they access into one governed view.
  Aggregates agents from clouds and platforms (AWS, Azure, GCP, Salesforce).
- **Primitives:** agent aggregation/discovery; governed ownership kept aligned to
  role changes; access governance and certification for agents inside the SailPoint
  identity-security platform; "Agentic Fabric" for agent-to-agent and agent-to-tool
  trust.
- **Gaps:** a governance/IGA layer, not a runtime auth library; enterprise-suite
  oriented; capabilities still maturing.
- **When to pick:** enterprises standardizing agent governance through an existing
  IGA program.
- **Source:** <https://www.sailpoint.com/products/agent-identity-security> ;
  <https://www.sailpoint.com/products/agentic-fabric>. Last verified 2026-05-30.

### Ping Identity — Identity for AI (Agentic AI Identity)

- **What it does:** positions an identity control plane for the "agentic
  enterprise" — trusted identities, real-time authorization, and human oversight
  for AI agents; discover and track agents, onboard and manage them, and
  distinguish legitimate agents from malicious bots.
- **Primitives:** agent discovery/inventory; agent identity with real-time
  authorization; human-in-the-loop oversight; bot/fraud differentiation for
  agentic users.
- **Gaps:** an early, control-plane repositioning (announced May 2026); shipped
  depth is still emerging relative to the messaging.
- **When to pick:** Ping customers extending their identity platform to agentic
  users and automated buyers.
- **Source:** <https://www.pingidentity.com/en/solution/agentic-ai-identity.html> ;
  press release 2026-05-27
  <https://press.pingidentity.com/2026-05-27-Ping-Identity-Redefines-the-Identity-Control-Plane-for-the-Agentic-Enterprise>.
  Last verified 2026-05-30.

## Audit layer

Still mostly absent as a dedicated standalone category in 2026 — see Chapter 7. Two
partial sources exist today. (1) PDP **decision logs**: Cerbos, AWS Verified
Permissions, Permit.io, and Auth0 FGA all emit per-decision authorization records
that double as an authorization audit trail. (2) **Governance-suite telemetry**:
the IAM incumbents above are the first to ship agent-action audit as a feature —
Okta streams tool calls + authorization decisions to a SIEM, CyberArk logs agent
actions and communications, and SailPoint puts agents in one governed view. What
no one yet sells as a standalone product is full agent-*session* audit (the chain
of identity → tool call → data touched → external action). List candidates here as
they emerge.

## OWASP Agentic Top 10 → vendor mapping

Mapping rule: a vendor is listed under a risk only where access control
**meaningfully reduces** that risk. A blank cell means the risk is not primarily an
IAM control (e.g. a reasoning/safety problem) — it is honest, not missing data.
Reference taxonomy: OWASP Agentic Security Initiative, *Agentic AI — Threats and
Mitigations* (<https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/>).

| Risk | Identity | Authz | Audit |
| --- | --- | --- | --- |
| AT01 — Memory Poisoning | — | Auth0 FGA, Permit.io (RAG/data filtering) | PDP logs |
| AT02 — Tool Misuse | WorkOS, Cloudflare (scoped OAuth) | AVP, Cerbos, Permit.io, Auth0 FGA | PDP logs |
| AT03 — Privilege Compromise | SPIFFE/SPIRE, Auth0 (Token Vault) | AVP, Cerbos, Permit.io | PDP logs |
| AT04 — Resource Overload | Cloudflare (platform rate limiting) | — | — |
| AT05 — Cascading Hallucination | — | — | — |
| AT06 — Intent Breaking | — | Permit.io (prompt filtering) | — |
| AT07 — Misaligned & Deceptive Goals | — | AVP, Cerbos, Permit.io (least privilege bounds blast radius) | PDP logs |
| AT08 — Identity Spoofing | SPIFFE/SPIRE, WorkOS, Cloudflare, Auth0 | AVP (verified principal) | — |
| AT09 — Overreliance | — | Auth0 (CIBA approvals), Permit.io (Access Request MCP) | — |
| AT10 — Unexpected RCE | SPIFFE/SPIRE (scoped identity) | AVP, Cerbos, Permit.io (tool gating) | PDP logs |

## Considered, not yet added

Evaluated this cycle and deferred (named for the next monthly diff, not endorsed):
**Saviynt** (IGA for agents), **Aembit** and **Astrix** (non-human / workload
identity), **Oso** and **OpenFGA** (open-source authorization), **Stytch** and
**Descope** (MCP / Connected Apps auth), **Google Vertex AI / Agentspace** agent
identity. Added next month if they carry a chapter-facing claim.

## Changelog

- **2026-05-30** — Initial population of all seven seed entries from primary
  sources; OWASP Agentic Top 10 mapping filled. Renamed the Cloudflare row from
  the placeholder "Cloudflare Agent Tokens" to "Cloudflare Agents (Workers OAuth
  Provider + Access)" — no Cloudflare product ships under the name "Agent Tokens";
  the documented primitive is OAuth for MCP. Renamed "WorkOS (AuthKit for Agents)"
  to "WorkOS AuthKit (MCP authorization)" to match the shipped doc surface.
- **2026-05-30** — Added the "Enterprise agent identity & governance (IAM
  incumbents)" section: Okta for AI Agents, Microsoft Entra Agent ID, AWS Bedrock
  AgentCore Identity, CyberArk Secure AI Agents, SailPoint Agent Identity Security,
  and Ping Identity. This introduces the build-side vs govern-side split and is
  where agent audit first ships; the Audit-layer note was updated accordingly.
  Moved Entra out of "considered" (now a full entry).
