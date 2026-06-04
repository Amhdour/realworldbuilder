from realworldbuilder.safe_claims import generate_safe_claims

def test_safe_claims_do_not_upgrade():
    claims=generate_safe_claims()
    assert any("not yet proven" in c["safer_claim"].lower() for c in claims)
