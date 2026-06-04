from realworldbuilder.classify_files import classify_path

def test_classifies_core_files():
    assert "backend" in classify_path("backend/api/routes.py", "")
    assert "frontend" in classify_path("frontend/app.tsx", "")
    assert "tests" in classify_path("tests/test_api.py", "")
    assert "ci_cd" in classify_path(".github/workflows/ci.yml", "")
