from realworldbuilder.readiness_score import calculate_scores

def test_scores_conservative_enterprise_low():
    s=calculate_scores({"tests":[],"ci_cd":[],"deployment":[],"evidence":[],"audit_telemetry":[],"root_files":["README.md"]}, [], [])
    assert max(s.values()) < 100
    assert s["enterprise_production_candidate_readiness"] <= 40
