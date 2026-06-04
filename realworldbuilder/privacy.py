from __future__ import annotations
import re
SECRET_PATTERNS=[(re.compile(r'(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*["\']?([A-Za-z0-9_./+=-]{8,})'), "likely_secret")]
def redact_text(text: str, public: bool = True) -> str:
    if not public: return text
    text=re.sub(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', '[REDACTED_EMAIL]', text)
    text=re.sub(r'/Users/[^/\s]+|/home/[^/\s]+', '[REDACTED_LOCAL_PATH]', text)
    for pat,_ in SECRET_PATTERNS:
        text=pat.sub(lambda m: f"{m.group(1)}=[REDACTED_SECRET]", text)
    return text
def detect_secret_lines(path: str, text: str) -> list[dict]:
    out=[]
    for i,line in enumerate(text.splitlines(),1):
        for pat,typ in SECRET_PATTERNS:
            m=pat.search(line)
            if m:
                out.append({"file_path": path, "line_number": i, "secret_type_guess": typ, "redacted_preview": pat.sub(lambda x: f"{x.group(1)}=[REDACTED_SECRET]", line), "severity":"high", "recommended_action":"Remove secret and rotate it."})
    return out
