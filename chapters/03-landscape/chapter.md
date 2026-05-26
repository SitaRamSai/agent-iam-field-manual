# Chapter 3: Who's Solving What

**Status:** outlined — target ship: week 8.
**Length target:** ~2500 words + vendor matrix.

## Thesis (one sentence)

The agent-IAM market in 2026 has 7+ serious players solving overlapping
slices; here is the canonical map and where the gaps are.

## Outline

1. Why this chapter exists: a platform engineer cannot evaluate 7 vendors
   in a week. This is the week of work, compressed.
2. The taxonomy (3 axes):
   - **Identity layer**: who is the agent? (Cloudflare Agent Tokens,
     SPIFFE-derived, WorkOS)
   - **Authorization layer**: what can the agent do? (AWS Verified
     Permissions, Auth0 FGA, Permit.io, Cerbos)
   - **Audit layer**: what did the agent actually do? (mostly absent —
     gap callout)
3. Per-vendor 1-page brief: positioning, primitives, gaps, when to pick.
4. OWASP Agentic Top 10 mapping: which vendor addresses which risk.
5. The gaps: what no one is solving yet.

## Living vendor matrix

The actual matrix lives in `../../landscape/vendors.md` and updates
monthly. This chapter freezes a snapshot at ship time.

## Scope-cut rule (from PLAN.md)

If not drafted by end of week 7: ship with top-5 vendors only + "more
coming" placeholder. Do not slip.

## Distribution checklist

- [ ] chapter.md committed
- [ ] `landscape/vendors.md` complete for the chapter's vendor set
- [ ] LinkedIn long-form rewrite
- [ ] X thread
- [ ] `git tag ch3`
