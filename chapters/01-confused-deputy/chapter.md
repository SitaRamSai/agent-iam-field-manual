# Chapter 1: The Confused Deputy Comes for Agents

**Status:** in flight — target ship: week 3.
**Length target:** ~2000 words + diagram + runnable PoC link.

## Thesis (one sentence)

LLM agents are the textbook 1988 confused-deputy problem, given a fresh
attack surface and a much louder failure mode.

## Outline

1. The original confused deputy (Norm Hardy, 1988) — 200 words, with the
   classic compiler example.
2. Why agents are confused deputies by construction — the agent acts on
   behalf of user A using credentials granted to the agent itself.
3. The PoC: a minimal Python agent (≤200 LOC, no framework) that reads an
   email, follows an attacker-supplied instruction in the email body, and
   exfiltrates data the user never authorized it to share. Screenshot the
   blast radius.
4. Why prompt-injection defenses miss this — they treat the symptom (the
   injected instruction) not the cause (the agent's ambient authority).
5. The IAM lens: capability-based security, principal/agent separation,
   delegation tokens, scope narrowing.
6. What "fixing it" looks like in 2026 vocabulary — pointer to Ch 5
   (least privilege) and Ch 3 (vendor landscape).

## PoC

Code lives in `../../demos/01-confused-deputy/`. Framework-less Python,
single file, ≤200 LOC. Run `python demo.py` to see the exfiltration.
Output: screenshot-ready terminal session.

## Distribution checklist (when shipping)

- [ ] chapter.md committed
- [ ] PoC runs end-to-end on fresh `python -m venv`
- [ ] Diagram: 1 ASCII or SVG showing principal → agent → resource flow
- [ ] LinkedIn long-form rewrite (~1500 words, exec framing)
- [ ] X thread (Shubham 5-part pattern: hook → value claim → bullets → opensource close → visual)
- [ ] `git tag ch1`
- [ ] GitHub Pages site rebuild
- [ ] Reply-list seeding: 3-5 tracked accounts get the link with a
      personalized 1-line ask

## Notes / open questions

- Should the PoC use a real LLM call (OpenAI/Anthropic) or a mock? Real
  call = more visceral, costs ~$0.05 per run, requires API key. Mock = zero
  setup, less visceral. Default: real with mock fallback.
- The 1988 paper citation — link to the original PDF or a modern
  recap? Modern recap is more clickable; original is more credible.
