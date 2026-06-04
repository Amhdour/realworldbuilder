from __future__ import annotations
from pathlib import Path
from collections import defaultdict
from .config import AppConfig
from .classify_files import classify_path, is_text_file
from .models import ScanFile, ScanResult
from .detectors import all_detectors
from .detect_architecture import architecture_map
from .detect_patch_points import patch_points
from .gap_analysis import build_gaps
from .readiness_score import calculate_scores
from .fingerprint import build_fingerprint
from .read_only_verifier import snapshot, verify
from .safe_claims import generate_safe_claims
from .supply_chain import indicators
from .codex_tasks import generate_tasks
from .privacy import detect_secret_lines
from .evidence_writer import write_reports

def scan_files(target: Path, cfg: AppConfig) -> ScanResult:
    files=[]; ignored=0
    for p in sorted(target.rglob("*")):
        rel=p.relative_to(target).as_posix()
        if any(part in set(cfg.ignored_paths) for part in p.relative_to(target).parts): ignored+=1; continue
        if not cfg.include_hidden and any(part.startswith('.') and part != '.github' for part in p.relative_to(target).parts): ignored+=1; continue
        if p.is_dir(): continue
        if len(files) >= cfg.max_files: ignored+=1; continue
        size=p.stat().st_size
        sample=""
        if is_text_file(p) and size <= cfg.max_file_size_kb*1024:
            try: sample=p.read_text(errors='ignore')[:4000]
            except Exception: sample=""
        kind=",".join(classify_path(rel, sample))
        files.append(ScanFile(path=rel,size=size,kind=kind,text_sample=sample))
    scan=ScanResult(target_path=str(target), files=files, ignored_count=ignored, findings=[])
    findings=[]
    for det in all_detectors(): findings.extend(det.detect(files))
    scan.findings=sorted(findings, key=lambda f:(f.category,f.path))
    return scan

def threat_matrix(patches):
    return [{"threat":p['threat_addressed'],"required_control":p['control_name'],"candidate_patch_point":p['candidate_files_or_folders'],"required_policy_rule":p['control_name'].lower().replace(' ','_'),"required_test":p['required_tests'],"required_demo_attack":p['required_demo_attack'],"required_audit_event":p['required_audit_event'],"required_telemetry_metric":p['required_telemetry_metric'],"required_evidence_file":p['required_evidence_file'],"current_status":p['implementation_status'],"evidence_strength_level":p['evidence_strength_level'],"control_maturity_level":p['control_maturity_level'],"safe_public_claim":p['safe_public_claim']} for p in patches]

def build_context(target: Path, cfg: AppConfig, before: dict, after: dict) -> dict:
    scan=scan_files(target,cfg); arch=architecture_map(scan); patches=patch_points(arch); gaps=build_gaps(patches); scores=calculate_scores(arch,patches,gaps); fp=build_fingerprint(target,scan,cfg.profile,cfg.privacy)
    secrets=[]
    for f in scan.files: secrets.extend(detect_secret_lines(f.path, f.text_sample))
    evidence=[{"evidence_file":p,"claim_supported":"supply-chain indicator present","control_supported":"supply-chain evidence","source_of_evidence":p,"reproducibility_status":"file/path indicator only","limitations":"No vulnerability scan performed in Phase 1.","safe_public_wording":"Supply-chain evidence indicators were found.","public_private_classification":"public_safe","reasons":["contains safe synthetic demo only"],"evidence_strength_level":1,"manual_review_marker":["needs_manual_review"]} for p in indicators(scan.files)]
    if secrets:
        evidence += [{"evidence_file":s['file_path'],"claim_supported":"potential secret indicator","control_supported":"Secret/PII detection","source_of_evidence":s['redacted_preview'],"reproducibility_status":"heuristic indicator","limitations":"Secret value is redacted and requires manual review.","safe_public_wording":"A redacted possible secret indicator was found and requires review.","public_private_classification":"sensitive_do_not_publish","reasons":["contains secrets"],"evidence_strength_level":1,"manual_review_marker":["needs_manual_review"]} for s in secrets]
    launch={"gates":[{"name":n,"status":"unconfirmed","mvp_work":"local tests, demo attacks, CI gates, evidence reports, safe public claims","later_enterprise_work":"staging validation, monitoring stack, rollback drills, external audit","safe_claim":"Not yet proven."} for n in ["Local development readiness","Test readiness","Demo attack readiness","CI readiness","Staging readiness","Production-style portfolio readiness","Enterprise production-candidate readiness","External validation readiness","Compliance-readiness","Public claim readiness"]]}
    known={"cannot_confirm":["I cannot confirm this from the provided project."],"manual_code_review":["All heuristic findings require review."],"requires_running_tests":["Control behavior and negative tests."],"requires_ci_logs":["CI gate execution evidence."],"requires_staging_validation":["Runtime deployment behavior."],"requires_external_validation":["External audit or assessment."],"must_not_claim_yet":["readiness for production use","readiness for enterprise use","compliance, certification, or comprehensive security"],"phase_1_intentionally_does_not_do":["modify target repo","full vulnerability scanning","SARIF export","auto-patching"],"safety_rewrites":[]}
    return {"scan":scan.model_dump(),"repo_fingerprint":fp,"architecture_map":arch,"patch_points":{"patch_points":patches,"mvp_production_style_portfolio_work":["local tests","demo attacks","CI gates","evidence reports","safe public claims"],"later_enterprise_work":["staging validation","monitoring stack","rollback drills","SSO/SCIM","external audit","certification"]},"threat_control_matrix":{"items":threat_matrix(patches)},"security_gap_report":{"gaps":gaps},"readiness_score":{"scores":scores},"launch_gate_checklist":launch,"evidence_index":{"evidence_items":evidence,"secret_indicators":secrets},"safe_public_claims":{"claims":generate_safe_claims()},"public_portfolio_summary":{"summary":"This public summary only states that a local heuristic readiness scan was run and that evidence gaps remain.","safe_claims":[c['safer_claim'] for c in generate_safe_claims()],"public_safe_evidence":[e for e in evidence if e['public_private_classification']=='public_safe']},"codex_next_tasks":{"tasks":generate_tasks(patches,gaps)},"read_only_verification":verify(before,after),"supply_chain_indicators":{"indicators":indicators(scan.files),"phase_1_limitation":"No full vulnerability scanning is performed."},"known_limitations":known}

def run_scan(target: Path, output: Path, cfg: AppConfig) -> tuple[dict, bool]:
    before=snapshot(target)
    scan=scan_files(target,cfg)
    after=snapshot(target)
    # rebuild context uses read-only scan again, snapshots still compare target state around first scan
    context=build_context(target,cfg,before,after)
    write_reports(output,context,cfg.privacy)
    critical=any(g['severity']=='critical' for g in context['security_gap_report']['gaps'])
    return context, critical
