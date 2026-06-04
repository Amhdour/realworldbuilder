AREAS=["RAG lifecycle","Retrieval security","ACL-aware retrieval","Tenant isolation","Source provenance","Permission sync","Document ingestion security","Embedding/index lifecycle security","Citation integrity","Prompt-injection defense","Context construction security","Agent runtime security","Tool authorization","MCP hardening","Policy-as-code","Runtime guardrails","Human approval workflow","Artifact security","Sandbox security","Secret/PII detection","Audit logging","Telemetry","Red-team tests","Demo attacks","CI/CD gates","Staging validation","Evidence lifecycle","Supply-chain evidence","Known limitations","Portfolio proof"]
def build_gaps(patches):
    gaps=[]
    for area in AREAS:
        related=[p for p in patches if area.lower().split()[0].replace('-','') in (p['control_name']+p['threat_addressed']).lower().replace('-','')]
        status="detected" if any(p['implementation_status']!="missing" for p in related) else "missing"
        gaps.append({"area":area,"status":status,"severity":"critical" if area in {"ACL-aware retrieval","Tenant isolation","Tool authorization","MCP hardening","Sandbox security"} and status=="missing" else "medium","exploitability":"unknown","evidence_impact":"blocks claim" if status=="missing" else "weakens claim","recommended_next_action":"Add implementation evidence, negative tests, demo attack, CI gate, and evidence report."})
    return gaps
