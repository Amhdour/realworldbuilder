from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime, timezone
from .constants import SCHEMA_VERSION, TOOL_NAME, TOOL_VERSION, UNCONFIRMED
from .privacy import redact_text
from .report_safety_validator import sanitize_report_text

MD_REPORTS=["index","repo_fingerprint","architecture_map","patch_points","threat_control_matrix","security_gap_report","readiness_score","launch_gate_checklist","evidence_index","safe_public_claims","public_portfolio_summary","codex_next_tasks","read_only_verification","supply_chain_indicators","known_limitations"]
JSON_REPORTS=["repo_fingerprint","architecture_map","patch_points","threat_control_matrix","security_gap_report","readiness_score","launch_gate_checklist","evidence_index","safe_public_claims","codex_next_tasks","read_only_verification","supply_chain_indicators","known_limitations"]

def envelope(fid: str, data: dict) -> dict:
    return {"schema_version":SCHEMA_VERSION,"tool_name":TOOL_NAME,"tool_version":TOOL_VERSION,"generated_at":datetime.now(timezone.utc).isoformat(),"target_repo_fingerprint_id":fid,"data":data}

def _md(title: str, data) -> str:
    return f"# {title}\n\n" + json.dumps(data, indent=2, sort_keys=True) + "\n\n## MVP / production-style portfolio work\nLocal tests, demo attacks, CI gates, evidence reports, and safe public claims.\n\n## Later enterprise work\nStaging validation, monitoring stack, backup/restore validation, rollback drills, SSO/SCIM integration, external audit, compliance certification, and customer-specific deployment hardening.\n"

def _index() -> str:
    links="\n".join(f"- [{r}.md]({r}.md)" for r in MD_REPORTS if r != 'index')
    return f"# RealWorldBuilder Report Index\n\nThis report is evidence-first and does not prove enterprise readiness.\n\n{links}\n\n## MVP / production-style portfolio work\nLocal tests, demo attacks, CI gates, evidence reports, and safe public claims.\n\n## Later enterprise work\nStaging validation, monitoring stack, rollback drills, SSO/SCIM integration, external audit.\n"

def write_reports(output: Path, context: dict, privacy: str) -> list[str]:
    output.mkdir(parents=True, exist_ok=True)
    rewrites=[]; fid=context['repo_fingerprint']['fingerprint_id']
    for name in MD_REPORTS:
        text=_index() if name=='index' else _md(name.replace('_',' ').title(), context[name])
        if name=='public_portfolio_summary': text += "\n## What is not claimed\nNo enterprise readiness, production readiness, compliance, certification, or comprehensive security is claimed.\n"
        if privacy == "public": text=redact_text(text, True)
        text, r=sanitize_report_text(text); rewrites.extend(r)
        (output/f"{name}.md").write_text(text)
    context['known_limitations']['safety_rewrites']=sorted(set(rewrites))
    for name in JSON_REPORTS:
        payload=envelope(fid, context[name])
        text=json.dumps(payload, indent=2, sort_keys=True)
        if privacy == "public": text=redact_text(text, True)
        (output/f"{name}.json").write_text(text)
    (output/"known_limitations.md").write_text(_md("Known Limitations", context['known_limitations']))
    return sorted(set(rewrites))
