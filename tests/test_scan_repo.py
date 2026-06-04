import json
from pathlib import Path
from typer.testing import CliRunner
from realworldbuilder.cli import app
from realworldbuilder.read_only_verifier import snapshot

runner=CliRunner()
FIX=Path("tests/fixtures/sample_repo")

def test_scan_generates_reports_and_is_read_only(tmp_path):
    before=snapshot(FIX)
    out=tmp_path/"out"
    res=runner.invoke(app, ["scan", str(FIX), "--output", str(out)])
    assert res.exit_code == 0, res.output
    after=snapshot(FIX)
    assert before == after
    for name in ["index.md","repo_fingerprint.json","architecture_map.json","patch_points.json","threat_control_matrix.json","security_gap_report.json","readiness_score.json","read_only_verification.json","supply_chain_indicators.json","safe_public_claims.json","codex_next_tasks.json","known_limitations.md"]:
        assert (out/name).exists(), name
    ro=json.loads((out/"read_only_verification.json").read_text())
    assert ro["data"]["changed_during_scan"] is False
    fp=json.loads((out/"repo_fingerprint.json").read_text())
    assert fp["schema_version"] == "1.0.0"
    assert fp["tool_name"] == "RealWorldBuilder"
    assert "fingerprint_id" in fp["data"]

def test_public_scan_redacts_and_has_summary(tmp_path):
    out=tmp_path/"public"
    res=runner.invoke(app, ["scan", str(FIX), "--output", str(out), "--privacy", "public"])
    assert res.exit_code == 0
    assert (out/"public_portfolio_summary.md").exists()
