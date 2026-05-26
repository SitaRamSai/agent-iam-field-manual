# Chapter 2: Why Prompt-Injection Defenses Aren't Enough

**Status:** outlined — target ship: week 5.
**Length target:** ~1800 words + lethal-trifecta diagram.

## Thesis (one sentence)

Every prompt-injection defense narrows the attack surface; IAM is what
makes the surviving attacks survivable.

## Outline

1. The lethal trifecta (Simon Willison's framing): private data + untrusted
   content + external comms. Prompt-injection defenses chip at the
   "untrusted content" leg; IAM chips at the "external comms" leg.
2. Meta's "Agents Rule of Two" as context — never let two of the three
   coexist for an unrestricted agent.
3. Walk through 3 prompt-injection defenses (input filtering, structured
   prompting, output filtering) and where each fails open.
4. The IAM completion: scope each agent action to a capability the user
   has explicitly delegated. Failed-open prompts become failed-closed
   authorizations.
5. Pointer to Ch 5 (least privilege) and Ch 7 (auditability) for the
   pattern catalog.

## Distribution checklist

- [ ] chapter.md committed
- [ ] Diagram: lethal-trifecta Venn with IAM overlay
- [ ] LinkedIn long-form rewrite
- [ ] X thread (chapter-launch pattern)
- [ ] `git tag ch2`
