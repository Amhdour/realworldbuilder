from realworldbuilder.report_safety_validator import sanitize_report_text, validate_no_forbidden

def test_forbidden_claims_rewritten():
    text, rewrites=sanitize_report_text("This repo is enterprise-ready and production-ready.")
    assert rewrites
    assert validate_no_forbidden(text)
