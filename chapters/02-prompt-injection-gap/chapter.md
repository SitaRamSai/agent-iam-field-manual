# Why Prompt-Injection Defenses Are Not Enough

## Thesis

Prompt-injection defenses help agents decide what to trust, but IAM decides what
they are allowed to do. Treating prompt safety as the whole control plane leaves
tool use, data access, and delegated authority under-specified.

## Reader Promise

By the end of this chapter, a platform engineer should be able to separate model
behavior controls from authorization controls and explain why production agent
platforms need both.

## Draft Outline

1. Define the common prompt-injection framing.
2. Explain what instruction hierarchy and content filtering can reduce.
3. Identify the gap: authority is still ambient unless tools enforce policy.
4. Connect the gap to the lethal-trifecta shape: private data, untrusted
   content, and external action.
5. Introduce the control-plane split used in the rest of the manual.

