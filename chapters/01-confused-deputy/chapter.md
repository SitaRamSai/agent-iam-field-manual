# Chapter 1: The Confused Deputy Comes for Agents

> LLM agents are the textbook confused-deputy problem, given a fresh
> attack surface and a louder operational failure mode.

An LLM agent reads a customer support email. The email contains a
sentence that was not written by your customer: it was written by an
attacker who knew the agent would read it. A few tool calls later, the
agent has used the support runtime's credentials to email a confidential
record to an address the attacker controls. No password was stolen. No
software bug was exploited. The agent did exactly what a literal reading
of the email told it to do, and the runtime that executed the agent's
tool calls had the authority to do it.

This pattern is not new. It is a thirty-eight-year-old problem dressed
in 2026 vocabulary. The label for it is the **confused deputy**, and
once you see it inside an LLM agent, the entire industry conversation
about prompt injection starts to look like a debate about symptoms.

## The original confused deputy

In a 1988 SIGOPS Operating Systems Review note titled *The Confused
Deputy*, Norm Hardy described a compiler running on a shared mainframe.
The compiler had been granted write access to a billing file so that it
could record usage. It also accepted, as a command-line argument, the
path to an output file for the compiled program. A user could ask the
compiler to write its output to the billing file. The compiler, holding
both authorities at once, would happily overwrite the billing record
with compiled object code.[^hardy]

The compiler is a deputy. It is acting on behalf of a user. The trouble
is that it holds two distinct authorities — its own ambient permission
on the billing file, and the user's much narrower permission — and it
cannot tell which authority a particular request is asking it to use.
When the user asks the deputy to act, the deputy uses whichever
authority gets the job done. Hardy's point is structural: a program
that holds authority granted for one purpose can be induced to use that
authority while acting on a different party's request.

The 1988 paper does not use modern LLM vocabulary. Throughout this
chapter, "ambient authority" is used in its plain-language sense — the
authority a process holds by virtue of running, rather than the
authority a request explicitly carries. Hardy was diagnosing an
access-control failure mode that the operating systems community has
rediscovered, in new clothing, every decade since. The 2026 clothing
is agent runtimes.

## Why agents are confused deputies by construction

A modern LLM agent has three properties that, taken together, recreate
Hardy's compiler:

1. **It accepts instructions from low-trust input.** OWASP's 2025 LLM
   Top 10 lists *indirect prompt injection* — instructions reaching the
   model through documents, web pages, retrieved context, or other
   external sources — as a primary risk for LLM applications.[^owasp01]
2. **It requests tool execution.** OpenAI's function-calling
   documentation describes the pattern: function definitions let the
   model pass data to application code, where the application code can
   access data or take actions suggested by the model. Anthropic's MCP
   connector lets Claude reach a configured set of remote tool servers
   through the Messages API and use OAuth bearer tokens to authenticate
   against them.[^openai] [^anthropic]
3. **The runtime executes those calls under its own authority.** The
   model itself does not have credentials at the resource layer. The
   process that runs the agent — the API gateway, the tool runner, the
   MCP connector — holds the database connection, the cloud role, the
   service account, the OAuth refresh token. When the model emits a
   tool call, that process executes it.

Put the three together and the structural shape is identical to Hardy's
compiler. The agent is a deputy. It acts on requests that arrive partly
from a trusted user and partly from untrusted content in the model's
context window. It holds authority that the original requester never
had and could not have been granted by name. And it cannot, on its own,
distinguish which authority any given tool call is meant to invoke.

To be precise about the threat: the model does not "execute" anything
at the resource layer. The model emits or suggests tool calls;
application code, the agent runtime, or a connected tool server is what
actually touches the database, the file system, or the outbound HTTP
call. The confused-deputy failure is not the model misbehaving in
isolation. It is the runtime obediently executing a tool call whose
intent came from a less-trusted source than the runtime's authority
implies.

## Why prompt-injection defenses miss this

Most public guidance on LLM application security still centers prompt
injection. OWASP LLM01:2025 catalogues mitigations: constraining model
behavior, validating output, filtering, limiting privileges, requiring
human approval for high-impact actions, and segregating external
content from trusted prompts.[^owasp01] These are useful. None of them
are authorization boundaries.

OWASP LLM06:2025, *Excessive Agency*, is the more pointed source. It
warns that the root cause of agentic-system damage is not the prompt
injection itself but the combination of excessive functionality,
excessive permissions, and excessive autonomy granted to extensions
that the model can invoke. It is also explicit about a control that
practitioners frequently overrate: logging and rate-limiting do not
*prevent* excessive agency, though they can detect or limit
damage.[^owasp06]

The practical reading is that input filtering and prompt hardening can
reduce the rate of successful injections, but they are not the
authorization layer. Downstream systems still need complete mediation
for tool and resource access. Even if every model invocation were
hardened against injection — a target nobody has hit — the structural
problem would remain. A deputy with broad authority and ambient
credentials is a deputy with broad authority and ambient credentials.

## The IAM lens

If prompt-injection defense is necessary but insufficient, what is the
durable shape of the fix? The 1975 Saltzer and Schroeder paper, *The
Protection of Information in Computer Systems*, gives the two
principles agent designers should care about most: **least privilege**
— each program and user should operate with only the privileges needed
for the job — and **complete mediation** — every access to every object
should be checked for authority.[^saltzer] The paper predates LLMs by
half a century and does not discuss them. The principles are still the
ones to apply.

A durable mitigation shape for agentic systems looks like this:

- **Principal separation.** The user's identity is one principal. The
  agent runtime is a different principal. The tool server is a third.
  Each holds distinct credentials with distinct scopes.
- **Scoped delegation.** When the agent acts for a user, it should act
  with a token that names the user, names the agent as the actor, and
  is scoped to the resource and action the user actually intended.
  OAuth 2.0 Token Exchange (RFC 8693) is one useful primitive here. It
  supports exchanging one token for another with explicit `resource`
  and `audience` targeting, and it supports an `act` claim that
  represents the acting party in delegation chains.[^rfc8693]
- **Least privilege at the tool boundary.** The agent's tool surface
  should be the narrowest set that the chapter, workflow, or session
  actually requires. The OWASP LLM06 guidance on functionality,
  permissions, and autonomy applies directly.[^owasp06]
- **Complete mediation downstream.** Every tool invocation should hit
  an authorization decision that re-checks the user, the agent, the
  resource, and the requested action against policy. This is Saltzer
  and Schroeder's complete mediation, restated in tool-runner
  terms.[^saltzer]
- **Audit that preserves the chain.** Logs should record the user
  principal, the agent or runtime principal, any actor or delegation
  chain present, the tool invoked, the resource touched, the
  authorization decision, the policy reason, the timestamp, and a
  request identifier. RFC 8693 supports representing the actor chain;
  the audit layer is what makes it useful after the fact.[^rfc8693]

The IETF Workload Identity in Multi-System Environments (WIMSE)
working group's *Workload Identity Practices* draft is the right place
to follow how the workload-identity side of this story is evolving:
how to issue, scope, and rotate the credentials the agent runtime and
tool servers themselves hold.[^wimse]

None of these primitives, on their own, is an "agent IAM" product.
RFC 8693 is a protocol primitive — it does not, by itself, guarantee
auditability, least privilege, or correct per-request policy. Cloud
providers expose useful narrowing controls — AWS, for one, documents
condition keys such as `aws:SourceArn` and `aws:SourceAccount` in
resource policies to defeat cross-service confused-deputy attacks on
AWS service principals — but that is cross-service IAM guidance, not
an end-to-end agent IAM architecture.[^aws] Vendor tooling for LLM
agents — OpenAI's function definitions and allowed-tool controls,
Anthropic's MCP connector with its allowlist/denylist and OAuth bearer
support — describes useful controls for narrowing tool or service
authority. None of them, in their own documentation, claims to solve
end-to-end agent IAM, and this manual will not imply they do.[^openai]
[^anthropic]

## A picture of the failure, and the fix

The structural picture of the failure is simple enough to draw with
two diagrams. The first shows the failure mode this chapter is about:

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

The deputy holds runtime or tool authority. It reads content the
attacker controls. It emits a tool call. The runtime executes it.
Nothing in this pipeline is a malfunction; every layer is doing what
it was built to do. The exfiltration happens because the authority
that backs the tool call was never bound to the user's actual intent.

The second shows the mitigation shape:

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

The difference is the authorization boundary in front of every tool
invocation: a place where the user principal, the agent principal,
the action, and the resource are checked together against policy, and
the decision is logged with enough fidelity to reconstruct who asked,
who acted, and why the system said yes or no.

The point of drawing it this plainly is that there is no exotic
component here. There is no new cryptographic protocol, no
unannounced standard, no model-side breakthrough. The components are
ones platform engineers already operate. They are simply not, in most
agent deployments today, wired up around the tool surface.

## The proof of concept

The companion PoC under [`demos/01-confused-deputy/`](../../demos/01-confused-deputy/)
is framework-less Python in a single file under 200 lines. It models a
support agent reading an inbox. One of the messages is from an
attacker who embedded an instruction in the email body. The agent
follows the instruction and uses the runtime's ambient credentials to
emit a record to an attacker-controlled destination. The terminal
prints `EXFILTRATED` so the failure mode is visible at a glance.

A second file, `demo_fixed.py`, runs the same scenario through a
scoped-delegation path. The agent must request a token bound to the
user's actual intent, and the tool runner re-checks the user, the
actor, the resource, and the action against policy before executing.
The attacker's instruction reaches the model. The model emits a tool
call. The authorization boundary refuses it. The terminal prints
`REFUSED`. Both runs use the same fixtures.

The demo defaults to a mock model so it runs with zero dependencies
and so CI can execute it deterministically. Flags exist to run against
a real provider or a local model for the more visceral demo, but the
chapter's argument does not depend on any of that. The structural
failure shows up against a mock just as well as it does against a
frontier model.

## What's next

The rest of the manual is about turning the mitigation shape sketched
above into something a platform engineer can actually wire up. The
next chapters cover the IAM mental model in more depth, survey the
vendor landscape for the primitives this chapter named, and walk
through least-privilege patterns for tool surfaces in detail.

If you take only one thing from this chapter, take this: an agent is
not safe because its prompt is hard to inject. An agent is safe when
the authority behind its tool calls cannot exceed the authority the
user intended to delegate, and when every exception to that rule is
recorded.

The compiler in Hardy's paper was not malicious. It was confused. So
is your agent, by construction, unless something downstream of the
model is doing the work of distinguishing whose authority a given
tool call is meant to invoke.

[^hardy]: Norm Hardy, "The Confused Deputy: (or why capabilities might
    have been invented)," *ACM SIGOPS Operating Systems Review* 22, no.
    4 (October 1988): 36–38, doi:10.1145/54289.871709. Open copy:
    <https://www.cs.utexas.edu/~witchel/S25-380L/papers/hardy88confused.pdf>.

[^saltzer]: Jerome H. Saltzer and Michael D. Schroeder, "The Protection
    of Information in Computer Systems," *Proceedings of the IEEE* 63,
    no. 9 (September 1975).
    <https://www.cs.virginia.edu/~evans/cs551/saltzer/>.

[^owasp01]: OWASP, "LLM01:2025 Prompt Injection," *OWASP Top 10 for LLM
    Applications 2025*.
    <https://genai.owasp.org/llmrisk/llm01-prompt-injection/>.

[^owasp06]: OWASP, "LLM06:2025 Excessive Agency," *OWASP Top 10 for LLM
    Applications 2025*.
    <https://genai.owasp.org/llmrisk/llm062025-excessive-agency/>.

[^openai]: OpenAI, "Function Calling," API documentation.
    <https://developers.openai.com/api/docs/guides/function-calling>.

[^anthropic]: Anthropic, "MCP Connector," Claude platform documentation.
    <https://platform.claude.com/docs/en/agents-and-tools/mcp-connector>.

[^rfc8693]: M. Jones, A. Nadalin, B. Campbell, J. Bradley, and C.
    Mortimore, *OAuth 2.0 Token Exchange*, RFC 8693 (January 2020).
    <https://datatracker.ietf.org/doc/html/rfc8693>.

[^wimse]: IETF WIMSE Working Group, *Workload Identity Practices*,
    Internet-Draft draft-ietf-wimse-workload-identity-practices-00.
    <https://www.ietf.org/archive/id/draft-ietf-wimse-workload-identity-practices-00.html>.

[^aws]: AWS, "The confused deputy problem," IAM User Guide.
    <https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html>.
