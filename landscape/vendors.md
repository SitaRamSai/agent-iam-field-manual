# Agent IAM Landscape

This is the living research matrix for Chapter 3. Keep notes factual and link
claims to primary sources when possible.

| Project / Vendor | Category | What It Appears To Solve | Open Questions |
| --- | --- | --- | --- |
| Cloudflare Agent Tokens | Agent / edge identity | Scoped credentials for agent access to services | How delegation and audit are represented across external tools |
| AWS Verified Permissions | Fine-grained authorization | Policy decisions for application actions | How much agent-specific context teams model in policy |
| Auth0 FGA | Fine-grained authorization | Relationship-based authorization for app resources | How it composes with tool invocation and agent principals |
| Permit.io | Authorization platform | Policy and permission management for applications | Agent-specific primitives and operational patterns |
| Cerbos | Policy engine | Externalized authorization checks | How teams model agent context and delegated authority |
| WorkOS | Enterprise identity platform | Authn, directory sync, and enterprise access foundations | Where agent identity fits in the product surface |
| SPIFFE / SPIRE patterns | Workload identity | Verifiable workload identity and short-lived credentials | How agent principals map onto workload identity conventions |
| OWASP Agentic guidance | Security taxonomy | Shared vocabulary for agent risks | How guidance maps to concrete IAM controls |

## Research Rules

- Prefer primary docs, product announcements, specs, and code.
- Separate what exists today from inferred roadmap direction.
- Track capabilities, not marketing categories.
- Update monthly after Chapter 3 ships.

