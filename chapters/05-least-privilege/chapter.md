# Chapter 5: Least Privilege for Agents

**Status:** outlined — target ship: week 12 (lighter pattern-recap).
**Length target:** ~1500 words.

## Thesis (one sentence)

The 1970s least-privilege principle applied to a principal that can
generate its own arguments.

## Outline

1. Least privilege recap (Saltzer & Schroeder 1975).
2. Why agents complicate it: argument generation, runtime delegation,
   capability discovery.
3. Pattern catalog: scoped delegation tokens, just-in-time elevation,
   time-bounded capabilities.
4. Anti-patterns: blanket service-account credentials, "the agent
   needs full access to be useful."

## Distribution checklist

- [ ] chapter.md committed
- [ ] LinkedIn long-form rewrite
- [ ] X thread
- [ ] `git tag ch5`
