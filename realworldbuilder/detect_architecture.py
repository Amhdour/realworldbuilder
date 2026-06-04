from __future__ import annotations
from collections import defaultdict
from .models import ScanResult
SECTIONS=["root_files","backend","frontend","worker","api_route","auth","authorization","rag_retrieval","agent_tool","mcp","artifact_sandbox","policy","audit_telemetry","tests","ci_cd","deployment","evidence","supply_chain"]
def architecture_map(scan: ScanResult) -> dict:
    m=defaultdict(list)
    for f in scan.files:
        if "/" not in f.path: m["root_files"].append(f.path)
        for k in f.kind.split(','):
            if k: m[k].append(f.path)
    return {s: sorted(set(m.get(s, []))) for s in SECTIONS} | {"unknowns_and_limitations":["I cannot confirm this from the provided project."]}
