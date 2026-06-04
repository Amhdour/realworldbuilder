from __future__ import annotations
import re
from .constants import FORBIDDEN_CLAIMS
REWRITES={"production-ready":"production-style portfolio readiness is not proven","enterprise-ready":"enterprise readiness is not proven","secure":"has security-related indicators","compliant":"compliance is not proven","certified":"certification is not proven","fully protected":"protection is not proven","complete security":"complete security is not proven","guaranteed":"not guaranteed","all risks covered":"not all risks are covered"}
def sanitize_report_text(text: str) -> tuple[str,list[str]]:
    rewrites=[]
    for phrase in FORBIDDEN_CLAIMS + ["secure"]:
        pat=re.compile(re.escape(phrase), re.I)
        if pat.search(text):
            text=pat.sub(REWRITES.get(phrase, phrase), text)
            rewrites.append("Rewrote unsupported claim wording during safety validation")
    return text, sorted(set(rewrites))
def validate_no_forbidden(text: str) -> bool:
    return not any(re.search(re.escape(p), text, re.I) for p in FORBIDDEN_CLAIMS)
