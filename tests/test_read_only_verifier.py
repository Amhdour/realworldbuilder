from pathlib import Path
from realworldbuilder.read_only_verifier import snapshot, verify

def test_snapshot_verify(tmp_path):
    (tmp_path/"a.txt").write_text("x")
    before=snapshot(tmp_path); after=snapshot(tmp_path)
    assert verify(before, after)["changed_during_scan"] is False
