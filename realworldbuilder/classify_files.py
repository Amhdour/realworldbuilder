from __future__ import annotations
from pathlib import Path

CATEGORY_KEYWORDS = {
    "backend": ["backend", "server", "api", "app.py", "main.py"],
    "frontend": ["frontend", "web", "ui", "components", "pages"],
    "tests": ["test", "tests", "spec"],
    "ci_cd": [".github/workflows", ".gitlab-ci", "circleci"],
    "deployment": ["dockerfile", "docker-compose", "k8s", "deploy", "helm"],
    "docs": ["docs", "readme"],
    "api_route": ["api", "route", "router", "endpoint"],
    "auth": ["auth", "login", "jwt", "session"],
    "authorization": ["acl", "permission", "role", "rbac", "authorize", "tenant"],
    "database_model": ["model", "schema", "migration", "db", "database"],
    "worker": ["worker", "queue", "job", "task"],
    "rag_retrieval": ["rag", "retriev", "document", "chunk", "vector", "embedding", "index"],
    "agent_tool": ["agent", "tool_call", "tool", "function_call"],
    "mcp": ["mcp", "modelcontextprotocol"],
    "artifact_sandbox": ["upload", "download", "artifact", "sandbox", "subprocess", "exec", "command"],
    "audit_telemetry": ["audit", "log", "telemetry", "monitor", "metric", "observability"],
    "policy": ["policy", "guardrail", "opa", "rego"],
    "security_test": ["attack", "redteam", "security", "exploit", "negative"],
    "evidence": ["evidence", "report", "attestation"],
    "supply_chain": ["license", "pyproject.toml", "requirements.txt", "package.json", "lock", "sbom", "cyclonedx", "dockerfile"],
}

def classify_path(path: str, text: str = "") -> list[str]:
    hay = f"{path.lower()} {text.lower()[:2000]}"
    found = [cat for cat, words in CATEGORY_KEYWORDS.items() if any(w in hay for w in words)]
    return sorted(set(found))

def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in {".py", ".js", ".ts", ".tsx", ".jsx", ".md", ".txt", ".yml", ".yaml", ".toml", ".json", ".env", ".ini", ".cfg", ".html", ".css"} or path.name.lower() in {"dockerfile", "license", "readme"}
