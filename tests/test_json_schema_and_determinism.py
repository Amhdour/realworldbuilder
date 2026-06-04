import json
from typer.testing import CliRunner
from realworldbuilder.cli import app
runner=CliRunner()

def test_schema_and_deterministic_ordering(tmp_path):
    out1=tmp_path/"o1"; out2=tmp_path/"o2"
    for out in [out1,out2]:
        res=runner.invoke(app,["scan","tests/fixtures/sample_repo","--output",str(out)])
        assert res.exit_code==0, res.output
    a=json.loads((out1/"architecture_map.json").read_text())["data"]
    b=json.loads((out2/"architecture_map.json").read_text())["data"]
    assert a == b
    for jf in out1.glob("*.json"):
        data=json.loads(jf.read_text())
        assert data["schema_version"] == "1.0.0"
        assert data["tool_version"] == "0.1.0"
        assert "generated_at" in data
