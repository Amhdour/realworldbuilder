from realworldbuilder.privacy import redact_text, detect_secret_lines

def test_redacts_public_data():
    t=redact_text("/home/alice/proj a@b.com api_key=abcdefghi", True)
    assert "alice" not in t and "a@b.com" not in t and "abcdefghi" not in t
    assert detect_secret_lines("x.env", "TOKEN=abcdefghijkl")
