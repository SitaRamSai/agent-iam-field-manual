<!-- markdownlint-disable MD013 -->

# Research 02: Why Prompt-Injection Defenses Aren't Enough

**Status:** source map filled; **thesis gate not yet cleared** — awaiting Ram's
written approval of the angle before the writer-agent draft begins.
**Chapter (planned):** `chapters/02-prompt-injection-isnt-enough/chapter.md`
**Last updated:** 2026-05-30

## Working Thesis

Prompt-injection defenses are necessary but architecturally insufficient. They
try to make an *unsolved detection problem* reliable at the input boundary —
and the empirical record shows that adaptive attackers break those defenses at
will. The durable control is not "detect the malicious instruction" but "bound
what a compromised agent is *authorized* to do." Two 2025 framings of that
boundary — Simon Willison's **lethal trifecta** and Meta's **Agents Rule of
Two** — are, read carefully, capability/least-privilege controls. They are the
same IAM layer Chapter 1 introduced (principal separation, scoped delegation,
complete mediation, audit), now expressed as a rule for which combinations of
capability an agent may hold in a single session. Chapter 2's job is to move
the reader from "harden the prompt" to "shrink the blast radius by design."

## Source Map

Primary sources only for chapter-facing claims. The lethal-trifecta and
Rule-of-Two entries are coined-concept sources (the author/vendor is the
authority for their own term); the AgentDojo, CaMeL, and Attacker-Moves-Second
entries are peer-style primary research with reproducible code/benchmarks.

### S1: Willison 2025, The Lethal Trifecta

- Primary source:
  [The lethal trifecta for AI agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
  (2025-06-16). Willison coined "prompt injection" (2022); this is the
  authoritative statement of the "lethal trifecta" term.
- Use for: the three capabilities whose *combination* enables data theft —
  (1) access to private data, (2) exposure to untrusted content,
  (3) ability to communicate externally.
- Supported claim: when an agent holds all three, an attacker who controls the
  untrusted content can exfiltrate the private data; removing any one leg
  breaks the exfiltration path.
- Safe limitation: this is a risk-framing/heuristic, not a formal proof or a
  product. It explains *why* certain capability combinations are dangerous;
  it does not by itself specify the enforcement mechanism.

### S2: Meta 2025, Agents Rule of Two

- Primary source:
  [Agents Rule of Two: A Practical Approach to AI Agent Security](https://ai.meta.com/blog/practical-ai-agent-security/)
  (2025-10-31).
- Use for: the rule that an agent should satisfy **no more than two** of three
  properties in a single session — [A] process untrustworthy inputs,
  [B] access sensitive systems or private data, [C] change state or communicate
  externally.
- Supported claims (exact-quote anchors):
  - "Prompt injection is a fundamental, unsolved weakness in all LLMs."
  - Agents "must satisfy no more than two of the following three properties
    within a session to avoid the highest impact consequences of prompt
    injection."
  - If all three are required without a fresh session, the agent "should not be
    permitted to operate autonomously and at a minimum requires supervision —
    via human-in-the-loop approval or another reliable means of validation."
- Safe limitation: Meta credits Chromium's security model and Willison's lethal
  trifecta as inspiration. Present Rule of Two as a session-scoped capability
  policy, not a complete IAM architecture; it does not specify token formats,
  delegation, or audit schema.

### S3: Debenedetti et al. 2024, AgentDojo

- Primary source:
  [AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents](https://arxiv.org/abs/2406.13352)
  (arXiv 2406.13352). Code: <https://github.com/ethz-spylab/agentdojo>.
- Use for: empirical evidence that input-side defenses are not reliable.
- Supported claim: across 97 realistic agent tasks and 629 security test cases,
  the benchmark evaluated multiple published defenses, and adaptive attacks
  bypassed them with attack success rates that remained materially high.
- Safe limitation: cite the specific numbers only from the version of the paper
  being quoted (results were updated across versions). When drafting, pull the
  exact ASR figures from the arXiv PDF rather than from secondary summaries.

### S4: Debenedetti et al. 2025, CaMeL ("Defeating Prompt Injections by Design")

- Primary source:
  [Defeating Prompt Injections by Design](https://arxiv.org/abs/2503.18813)
  (arXiv 2503.18813, v2 2025-06-24). Code:
  <https://github.com/google-research/camel-prompt-injection>.
- Use for: the strongest statement of the chapter's thesis from the research
  side — defend by *design/architecture*, not by model behavior.
- Supported claims: CaMeL does not modify the model; it attaches capability
  metadata to values and enforces control/data-flow policies in a custom
  interpreter, providing security guarantees independent of whether the model
  is fooled. It reports solving a large share of AgentDojo tasks *with provable
  security* (pull exact percentages from the PDF at draft time).
- Safe limitation: CaMeL is a research system with real usability/coverage
  costs (it cannot run arbitrary agent tasks). Use it to support "design-level
  containment beats detection," not as a turnkey recommendation.

### S5: Nasr, Carlini et al. 2025, The Attacker Moves Second

- Primary source:
  [The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections](https://arxiv.org/abs/2510.09023)
  (arXiv 2510.09023, 2025-10). Authors include researchers from OpenAI,
  Anthropic, and Google DeepMind.
- Use for: the load-bearing "detection doesn't hold up" evidence, from a
  cross-lab author list (hard to dismiss as one vendor's view).
- Supported claim: the paper subjects 12 published defenses to adaptive attacks
  (gradient, RL, random search, human-guided) and bypasses most with attack
  success rates above 90%, even though many of those defenses originally
  reported near-zero success rates.
- Safe limitation: the paper's claim is about *evaluation methodology* (static
  vs adaptive attackers) and current defenses; it is not a proof that robust
  detection is impossible in principle. Word it as "current input-side defenses
  do not hold against adaptive attackers," not "detection can never work."

### S6: OWASP LLM01:2025 Prompt Injection

- Primary source:
  [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
  (carried over from Research 01).
- Use for: the standards-body framing of prompt injection, including indirect
  injection via external content, and OWASP's own position that input filtering
  is a mitigation, not a guarantee.
- Safe limitation: OWASP lists input sanitization and constrained behavior as
  *secure-coding measures*; do not present them as worthless. The chapter's
  claim is that they are not an authorization boundary, which is consistent
  with OWASP recommending downstream privilege controls (LLM06) as well.

## Claim Checklist

### Claim 1 — Prompt injection is an unsolved, structural weakness

- Source IDs: S2, S6.
- Evidence note: Meta states plainly it is "a fundamental, unsolved weakness in
  all LLMs"; OWASP catalogs it as the #1 LLM risk including indirect injection.
- Safe wording: "Prompt injection is, as of this writing, an unsolved problem at
  the model layer; treat it as a property of how LLMs ingest text, not a bug
  that a future patch removes."

### Claim 2 — Input-side defenses do not hold against adaptive attackers

- Source IDs: S3, S5.
- Evidence note: AgentDojo bypassed multiple defenses with adaptive attacks;
  Attacker-Moves-Second bypassed 12 defenses (most >90% ASR) that had reported
  near-zero ASR under static evaluation.
- Safe wording: "Defenses that look strong against fixed test strings fall over
  when the attacker adapts to them. The empirical record across independent
  evaluations is consistent: input filtering and detection reduce risk but do
  not bound it."

### Claim 3 — The lethal trifecta names the dangerous capability combination

- Source IDs: S1.
- Evidence note: Willison's three legs — private data, untrusted content,
  external communication — and the claim that removing one breaks exfiltration.
- Safe wording: "Data theft requires three capabilities in the same agent:
  access to private data, exposure to untrusted content, and a way to send data
  out. Drop any leg and the exfiltration path closes."

### Claim 4 — Rule of Two reframes the trifecta as a session capability policy

- Source IDs: S2, S1.
- Evidence note: Meta's no-more-than-two-of-three rule, inspired by the lethal
  trifecta and Chromium, with human-in-the-loop required when all three are
  needed.
- Safe wording: "Meta's Agents Rule of Two operationalizes the same insight as
  an enforceable policy: hold at most two of {untrusted input, sensitive access,
  external action} per session, or require human approval. This is a
  least-privilege rule, not a prompt-hardening rule."

### Claim 5 — Design-level containment is where the field is heading

- Source IDs: S4.
- Evidence note: CaMeL enforces policy in an interpreter using capability
  metadata, independent of model robustness, and reports provable security on a
  large share of AgentDojo.
- Safe wording: "The most promising defenses don't try to make the model
  un-foolable; they constrain what the agent's actions are *permitted* to do
  regardless of what the model was told — which is the authorization layer from
  Chapter 1, applied to data and control flow."

### Claim 6 — Therefore the durable control is IAM, not better prompts

- Source IDs: S1, S2, S4 (synthesis); links back to Research 01 S2/S5.
- Evidence note: lethal trifecta (capability combination), Rule of Two
  (session-scoped least privilege), and CaMeL (capability-based flow control)
  are all authorization controls, not detection controls.
- Safe wording: "Every defense that actually bounds the damage works by limiting
  authority — which capabilities an agent holds, what a delegated action is
  scoped to, and whether the tool boundary mediates the call. That is identity
  and access management. Prompt-injection defenses sit *in front of* that layer;
  they do not replace it."

## Research Questions

### Does Chapter 2 risk just repeating Chapter 1?

No, if it earns the move. Ch1 argues agents *are* confused deputies. Ch2 must
answer the natural reader objection — "fine, but won't prompt-injection
defenses fix that?" — and show, with the adaptive-attack evidence (S3, S5),
that they cannot, then route the reader to the containment framings (S1, S2, S4)
as the IAM answer. The chapter is the bridge from "why it breaks" (Part I) to
"the controls" (later parts).

### How much of the lethal trifecta / Rule of Two should the chapter reproduce?

Enough to define each precisely and credit the source, then spend the chapter's
weight on the IAM *reading* of them: trifecta legs map to (data scope, input
trust boundary, egress control); Rule of Two maps to per-session least
privilege with a human-approval escape hatch. Avoid implying Meta or Willison
used the exact phrase "IAM" if they did not.

### Which numbers are safe to quote?

Quote AgentDojo (S3) and Attacker-Moves-Second (S5) attack-success figures only
from the cited arXiv version, pulled from the PDF at draft time. Do not quote
the "84% / 77%" CaMeL figures unless re-confirmed against the v2 PDF, since the
search summary may not match the final table.

### Should the chapter get its own demo?

Optional for this chapter and not required by `AGENTS.md` (demos are per-chapter
"when the chapter needs a PoC"). A natural fit would *extend* the Chapter 1
demo: add an input-side "filter" that blocks a naive injection string, then show
an adaptive variant slipping past it while the authorization boundary still
prints `REFUSED`. Propose as a stretch goal, not a gate, pending Ram's call.

## Diagram Notes

```text
Input-side defense (necessary, not sufficient)

untrusted content --> [ filter / detector ] --> agent --> tool calls
                            ^                                   |
                            |  adaptive attacker tunes          | runtime authority
                            |  the string until it passes       v
                            +---------------------------- private resource (exfiltrated)
```

```text
Authorization-side containment (the IAM layer)

untrusted content --> agent --> requested tool call
                                      |
                                      v
                         [ authorization boundary ]
                          - lethal trifecta: is data + untrusted + egress all present?
                          - rule of two: >2 capabilities this session? require human
                          - scoped delegation + complete mediation (Ch1)
                                      |
                       allow only if scope/intent match; else REFUSED + audit
```

## Do Not Ship Until

- [x] At least five primary-source citations are present (six here).
- [x] Every standards/vendor/research claim maps to a primary doc.
- [ ] **Thesis approved by Ram in writing** (commit message or PR comment).
- [ ] Exact AgentDojo / CaMeL / Attacker-Moves-Second figures re-pulled from the
      arXiv PDFs at draft time (not from search summaries).
- [ ] Chapter text uses this note for citations instead of ad hoc links.
- [ ] Critic-agent review under the frozen `critic-prompt-vN` before merge.
