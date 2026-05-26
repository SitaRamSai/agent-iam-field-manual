# MCP and Tool Identity

## Thesis

Tool protocols make agent systems composable, but composability without
identity-aware gating creates a new authorization problem: which agent is using
which tool, on whose behalf, under which policy?

## Reader Promise

By the end of this chapter, a platform engineer should understand the difference
between connecting a tool server and authorizing a specific tool invocation.

## Draft Outline

1. Explain why tool identity matters once agents can discover and call tools.
2. Describe tool poisoning and over-broad tool exposure.
3. Separate server authentication from per-action authorization.
4. Sketch identity-aware tool discovery and policy-enforced tool calls.
5. Define operational questions teams should ask before enabling an MCP server.

