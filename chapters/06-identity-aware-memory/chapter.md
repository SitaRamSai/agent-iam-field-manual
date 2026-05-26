# Chapter 6: Identity-Aware Memory & Retrieval

**Status:** outlined — target ship: Phase 2 (post week 12).
**Length target:** ~2000 words.

## Thesis (one sentence)

Multi-tenant agent memory is the new multi-tenant database, with worse
defaults and no DBA culture yet.

## Outline

1. The leak surface: shared vector store + per-user prompts.
2. Retrieval poisoning: attacker inserts a document only the agent will
   see, that steers later queries.
3. Identity-aware retrieval: ACL on chunks, per-user index partitioning,
   row-level security analogues.
4. Audit pattern: every retrieval call carries the principal.

## Distribution checklist

- [ ] chapter.md committed
- [ ] LinkedIn long-form rewrite
- [ ] X thread
- [ ] `git tag ch6`
