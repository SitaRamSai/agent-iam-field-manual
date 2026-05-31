# Chapter 2: Why Prompt-Injection Defenses Aren't Enough

> Prompt-injection defenses are necessary but architecturally
> insufficient. They try to make an unsolved detection problem
> reliable; the durable control is bounding what a compromised agent is
> authorized to do.

Chapter 1 argued that an LLM agent is a confused deputy by
construction: it reads low-trust content, it requests tool calls, and a
runtime executes those calls under authority the original requester
never held. The natural reaction from an engineer who has just
internalized that is reasonable and almost universal: *fine, so the
problem is the malicious instruction reaching the model — let's stop it
from getting in.* Filter the input. Harden the system prompt. Train a
classifier to flag injected instructions. Wrap the whole thing in
guardrails.

This chapter is about why that instinct, pursued on its own, does not
close the hole. Not because input defenses are worthless — they reduce
risk and you should run them — but because they are aimed at the wrong
layer. The confused-deputy problem is an *authorization* problem, and
no amount of input hardening converts a detection control into an
authorization boundary.

## Prompt injection is an unsolved problem, not a pending patch

Start with the most honest statement a major lab has published on the
subject. Meta's 2025 *Agents Rule of Two* guidance opens by calling
prompt injection "a fundamental, unsolved weakness in all LLMs."[^meta]
That is not hedging. It is a vendor with enormous incentive to claim a
fix declining to claim one.

OWASP's 2025 LLM Top 10 ranks prompt injection as the number-one risk
for LLM applications and is explicit that it includes *indirect*
injection — instructions arriving through documents, web pages,
retrieved context, and other external sources the model is asked to
process.[^owasp01] The danger is not a user typing "ignore your
instructions." It is that any text an agent ingests is, from the
model's perspective, potentially instructions. That is a property of
how language models consume their context window, not a bug with a
patch number.

If the input channel cannot be made trustworthy, the question becomes:
how reliable are the defenses that try to catch the bad input anyway?

## The defenses do not hold against an adaptive attacker

This is where the empirical record matters, because it is easy to build
a prompt-injection defense that looks excellent and is, in fact,
brittle.

AgentDojo, introduced in 2024 by E. Debenedetti and colleagues, was
built precisely to measure this. It is a dynamic benchmark of 97
realistic agent tasks — managing an email client, navigating an
e-banking site, booking travel — wired with 629 security test cases
that inject attacker instructions into the data an agent retrieves. Its
designers found that existing prompt-injection attacks break some of
the security properties of current agents, and, just as tellingly, that
the benchmark is hard for *defenses* too: it is not solved.[^agentdojo]

The sharper result came in 2025. A team spanning OpenAI, Anthropic, and
Google DeepMind published *The Attacker Moves Second*, which took 12
recently published defenses against jailbreaks and prompt injection —
most of which had reported near-zero attack success rates in their
original papers — and subjected them to *adaptive* attacks: gradient
descent, reinforcement learning, random search, and human-guided
exploration that deliberately targets each defense's design. The result
was a bypass rate above 90% for most of the defenses tested.[^attacker]

Sit with the gap. The same defense reports near-zero attack success
when evaluated against a fixed set of attack strings, and over 90% when
the attacker is allowed to adapt. The defenses did not get worse
between the two evaluations; the evaluation got honest. A real attacker
does not throw a static payload and give up. They tune the payload
against your filter until it passes. The cross-lab author list matters
here: this is not one vendor disparaging a competitor's approach. It is
the people building the frontier models reporting that input-side
detection, as a category, does not hold under adaptive pressure.

The conclusion is not "stop filtering." It is "do not treat filtering
as a boundary." A control that fails most of the time against a
motivated attacker can be a useful speed bump. It cannot be the thing
standing between an injected instruction and your customer database.

## Stop trying to keep the instruction out; bound what it can do

If you cannot reliably keep the malicious instruction out of the
model's context, the durable move is to design the system so that a
compromised agent cannot do much damage. That reframing — from "detect
the bad input" to "limit the blast radius" — is the whole game, and two
widely cited 2025 framings express it.

The first is Simon Willison's **lethal trifecta**.[^trifecta] Willison,
who coined the term "prompt injection," observed that data theft
requires an agent to combine three capabilities:

1. **Access to private data** — the customer records, internal
   documents, or credentials that make the agent useful.
2. **Exposure to untrusted content** — any text from outside the trust
   boundary: a web page, an email, a retrieved file.
3. **The ability to communicate externally** — any path that can carry
   data out, from an outbound HTTP request to a rendered image URL to a
   link the agent hands a user to click.

The point is that the danger lives in the *combination*. An agent with
private data and untrusted input but no egress cannot exfiltrate. An
agent with untrusted input and egress but no private data has nothing
worth stealing. Remove any one leg and the exfiltration path closes —
regardless of whether the injection succeeded. That is an
access-control statement, not a prompt-engineering one.

The second framing operationalizes the first. Meta's **Agents Rule of
Two** states that, until robustness research can reliably detect and
refuse prompt injection, an agent should satisfy "no more than two of
the following three properties within a session": [A] processing
untrustworthy inputs, [B] accessing sensitive systems or private data,
and [C] changing state or communicating externally. If an agent needs
all three in one session without a fresh context, Meta's guidance is
that it "should not be permitted to operate autonomously and at a
minimum requires supervision — via human-in-the-loop approval or
another reliable means of validation."[^meta] The framework credits
both Chromium's security model and Willison's lethal trifecta as
inspiration.

Read the Rule of Two for what it actually is: a per-session
least-privilege policy with a human-approval escape hatch. It says
nothing about how to phrase a prompt. It is a rule about which
*capabilities* an agent is allowed to hold at once — which is the
language of authorization, not the language of input sanitization.

## The most promising research defense is capability-based access control

The strongest evidence that this is the right layer comes from the most
promising design-level defense. In 2025, researchers at Google DeepMind
and ETH Zürich published CaMeL — short for *Capabilities for Machine
Learning* — described in the paper *Defeating Prompt Injections by
Design*.[^camel]

CaMeL is worth understanding because of what it refuses to do. It does
not modify the model or try to make it harder to fool. Instead it
builds a protective layer *around* the LLM. It extracts the control and
data flow from the trusted user query, so that untrusted data the model
retrieves can never alter the program's control flow. It attaches
capability metadata to values and enforces security policies in a
custom interpreter at the moment a tool is called, blocking
exfiltration over unauthorized data flows. On AgentDojo it solves 77%
of tasks *with provable security*, against 84% for an undefended system
that offers no security at all.[^camel]

Notice the shape of that result. One of the most promising research
defenses against prompt injection is not a better classifier or a more
cleverly worded system prompt. It is capability-based access control —
tracking where data is allowed to flow and mediating every tool call
against a policy — applied to the agent's data and control flow. That is the
authorization layer from Chapter 1, generalized from "who may call this
tool" to "where may this value travel." CaMeL pays for its guarantees
in coverage; it cannot run every agent task. But it demonstrates the
direction: security that comes from *design and mediation*, independent
of whether the model was fooled.

## The IAM reading

Line the three framings up and they say one thing. The lethal trifecta
names the dangerous combination of capabilities. The Rule of Two turns
that into an enforceable per-session privilege limit. CaMeL enforces a
capability policy on data flow at the tool boundary. None of them is a
prompt-hardening technique. All of them are access-control techniques:
they decide what authority an agent holds and what its actions are
permitted to reach.

That is the same mitigation shape Chapter 1 sketched, viewed from a
different angle:

- **Principal separation and least privilege** decide whether an agent
  holds all three trifecta legs at once. An agent that reads untrusted
  email should not also carry the credential that can send mail to
  arbitrary external addresses *and* read the full customer database in
  the same session.
- **Scoped delegation** is how you give an agent capability [B] —
  access to private data — narrowed to the one record the user actually
  asked about, so that holding it is not the same as holding the whole
  store.
- **Complete mediation at the tool boundary** is the enforcement point
  the Rule of Two and CaMeL both rely on: the place where capability
  [C], the outbound action, is checked against policy before it
  executes.
- **Audit** is what tells you, after the fact, which leg was present and
  which boundary said yes.

Prompt-injection defenses sit *in front of* this layer. They lower the
probability that an instruction is injected in the first place, which
is genuinely worth doing. They do not change what happens when one gets
through. The authority behind the agent's tool calls is what determines
whether a successful injection is a logged non-event or a breach.

## A picture of the two layers

The failure mode is an attacker tuning input until it slips past the
detector, behind which the agent still holds full authority:

```text
Input-side defense (necessary, not sufficient)

untrusted content --> [ filter / classifier ] --> agent --> tool call
                              ^                                  |
   adaptive attacker tunes    |                                  | full runtime
   the payload until it       |                                  | authority
   passes the filter ---------+                                  v
                                                      private resource (exfiltrated)
```

The containment layer does not depend on the detector being right. Even
when the injected instruction reaches the model and the model emits the
malicious tool call, the boundary refuses it because the agent's
authority for that session does not span all three trifecta legs:

```text
Authorization-side containment (the IAM layer)

untrusted content --> agent --> requested tool call
                                      |
                                      v
                          [ authorization boundary ]
                           - all three trifecta legs present this session?
                           - rule of two: >2 capabilities -> require human
                           - scoped delegation + complete mediation (Ch1)
                                      |
                       allow only if scope and intent match; else REFUSED + audit
```

The components are not exotic — they are the access-control primitives
platform engineers already operate. What is new is the discipline of
wiring them around the agent's tool surface instead of trusting the
model to police its own input.

## What's next

If prompt injection is unsolved and input defenses do not hold, the
work moves to the authorization layer — and that layer is now a market.
Part II of this manual surveys who is building the primitives this
chapter named: agent identity issuers, scoped-delegation services,
policy engines that can sit at the tool boundary, and the standards
they lean on. The next chapter populates that landscape with primary
sources and a maintained vendor matrix.

If you take one thing from this chapter, take this: a defense you
evaluate against your own fixed test cases will look far stronger than
it is. Assume the attacker adapts, assume the injection sometimes
succeeds, and put your real control where it cannot be talked out of
doing its job — at the boundary that decides what the agent's tool
calls are authorized to reach.

[^meta]: Meta, "Agents Rule of Two: A Practical Approach to AI Agent
    Security," Meta AI blog (October 31, 2025).
    <https://ai.meta.com/blog/practical-ai-agent-security/>.

[^owasp01]: OWASP, "LLM01:2025 Prompt Injection," *OWASP Top 10 for LLM
    Applications 2025*.
    <https://genai.owasp.org/llmrisk/llm01-prompt-injection/>.

[^trifecta]: Simon Willison, "The lethal trifecta for AI agents: private
    data, untrusted content, and external communication" (June 16,
    2025). <https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/>.

[^agentdojo]: E. Debenedetti et al., "AgentDojo: A Dynamic Environment
    to Evaluate Prompt Injection Attacks and Defenses for LLM Agents,"
    arXiv:2406.13352. <https://arxiv.org/abs/2406.13352>. Code:
    <https://github.com/ethz-spylab/agentdojo>.

[^attacker]: M. Nasr, N. Carlini, et al., "The Attacker Moves Second:
    Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and
    Prompt Injections," arXiv:2510.09023.
    <https://arxiv.org/abs/2510.09023>.

[^camel]: E. Debenedetti et al., "Defeating Prompt Injections by
    Design," arXiv:2503.18813. <https://arxiv.org/abs/2503.18813>. Code:
    <https://github.com/google-research/camel-prompt-injection>.
