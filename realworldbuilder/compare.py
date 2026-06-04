from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime, timezone
from .constants import SCHEMA_VERSION, TOOL_NAME, TOOL_VERSION

def _load(p: Path, name: str):
    f=p/name
    return json.loads(f.read_text()) if f.exists() else {"data":{}}
def compare_outputs(before: Path, after: Path, output: Path|None=None) -> dict:
    barch=_load(before,"architecture_map.json").get("data",{})
    aarch=_load(after,"architecture_map.json").get("data",{})
    bs=_load(before,"readiness_score.json").get("data",{}).get("scores",{})
    as_=_load(after,"readiness_score.json").get("data",{}).get("scores",{})
    bfiles=set(sum([v for v in barch.values() if isinstance(v,list)], [])); afiles=set(sum([v for v in aarch.values() if isinstance(v,list)], []))
    delta={"new_detected_files":sorted(afiles-bfiles),"new_evidence":sorted(set(aarch.get('evidence',[]))-set(barch.get('evidence',[]))),"improved_scores":{k:{"before":bs.get(k,0),"after":as_.get(k,0)} for k in sorted(as_) if as_.get(k,0)>bs.get(k,0)},"unchanged_gaps":[],"newly_introduced_gaps":[],"claims_now_better_supported":[],"claims_still_unsupported":["Enterprise readiness is not proven."]}
    env={"schema_version":SCHEMA_VERSION,"tool_name":TOOL_NAME,"tool_version":TOOL_VERSION,"generated_at":datetime.now(timezone.utc).isoformat(),"target_repo_fingerprint_id":_load(after,'repo_fingerprint.json').get('target_repo_fingerprint_id','comparison'),"data":delta}
    out=output or after
    out.mkdir(parents=True, exist_ok=True)
    (out/"readiness_delta.json").write_text(json.dumps(env, indent=2, sort_keys=True))
    (out/"readiness_delta.md").write_text("# Readiness Delta\n\n"+json.dumps(delta, indent=2, sort_keys=True)+"\n")
    return env
