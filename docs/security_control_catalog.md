# Security Control Catalog

## RAG security controls
Context construction checks, retrieval filtering, source provenance, citation integrity, and prompt-injection handling.
## Retrieval security controls
Query authorization, result filtering, source allowlists, and result consistency checks.
## ACL-aware retrieval controls
Tenant/user/role/permission predicates enforced before retrieved content reaches prompts.
## Tenant isolation controls
Tenant-bound storage, indexes, caches, sessions, tools, and audit context.
## Source provenance controls
Document origin, connector identity, ingestion timestamp, and version metadata.
## Prompt-injection defense controls
Retrieved-context classification, instruction stripping, allowlisted tool routing, and negative tests.
## Agent runtime controls
Loop limits, step budgets, memory boundaries, and high-risk action approvals.
## Tool authorization controls
Policy checks before tool execution and validation after tool output.
## MCP hardening controls
Identity binding, scope validation, tenant context, and confused-deputy defense.
## Artifact security controls
Upload/download validation, malware/secret/PII scanning hooks, and safe storage.
## Sandbox security controls
Command restrictions, egress controls, resource limits, and audit events.
## Audit logging controls
Decision events, actor identity, tenant context, denied actions, and evidence retention.
## Telemetry controls
Control metrics, failure rates, policy decisions, latency, and anomaly counters.
## CI/CD gate controls
Unit tests, negative/security tests, demo attacks, evidence generation, and scan gates.
## Evidence lifecycle controls
Reproducible reports, public/private classification, safe claims, and limitations.
