import json
from realworldbuilder.compare import compare_outputs

def env(data):
    return {"data": data, "target_repo_fingerprint_id":"f"}

def test_compare_outputs(tmp_path):
    b=tmp_path/"b"; a=tmp_path/"a"; b.mkdir(); a.mkdir()
    (b/"architecture_map.json").write_text(json.dumps(env({"backend":["old.py"]})))
    (a/"architecture_map.json").write_text(json.dumps(env({"backend":["old.py","new.py"],"evidence":["evidence/report.md"]})))
    (b/"readiness_score.json").write_text(json.dumps(env({"scores":{"ci_readiness":5}})))
    (a/"readiness_score.json").write_text(json.dumps(env({"scores":{"ci_readiness":45}})))
    compare_outputs(b,a)
    d=json.loads((a/"readiness_delta.json").read_text())
    assert "new.py" in d["data"]["new_detected_files"]
    assert d["data"]["improved_scores"]
