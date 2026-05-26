# Auditability and the Agent as a Principal

## Thesis

An agent that can act in production needs an audit trail that distinguishes the
human requester, the agent principal, the tool identity, the policy decision,
and the resulting state change.

## Reader Promise

By the end of this chapter, a platform engineer should be able to design an
audit event shape for agent workflows that an incident reviewer can actually
use.

## Draft Outline

1. Define why normal application logs are insufficient.
2. Separate requester, agent, tool, resource, and policy decision.
3. Cover trace correlation across planning and execution.
4. Show examples of useful and useless audit records.
5. Connect auditability to incident response and compliance.

