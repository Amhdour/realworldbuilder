from realworldbuilder.detect_patch_points import patch_points
from realworldbuilder.gap_analysis import build_gaps

def test_patch_points_and_gaps():
    patches=patch_points({"rag_retrieval":["backend/rag/retriever.py"],"agent_tool":[]})
    assert any(p["control_name"] == "Retrieval ACL enforcement" for p in patches)
    gaps=build_gaps(patches)
    assert any(g["severity"] in {"critical","medium"} for g in gaps)
