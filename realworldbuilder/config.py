from __future__ import annotations
from pathlib import Path
from pydantic import BaseModel, Field
from .constants import DEFAULT_IGNORED_PATHS

class AppConfig(BaseModel):
    profile: str = "rag-agent"
    output_dir: str = "realworldbuilder_output"
    max_files: int = 10000
    max_file_size_kb: int = 512
    include_hidden: bool = False
    ignored_paths: list[str] = Field(default_factory=lambda: sorted(DEFAULT_IGNORED_PATHS))
    required_controls: list[str] = Field(default_factory=lambda: ["retrieval_acl", "tenant_isolation", "tool_authorization", "audit_logging", "telemetry"])
    claim_mode: str = "conservative"
    privacy: str = "internal"

def load_config(target: Path) -> AppConfig:
    p = target / "realworldbuilder.yaml"
    if p.exists():
        data = {}
        current = None
        for line in p.read_text().splitlines():
            if not line.strip() or line.strip().startswith("#"): continue
            if ":" in line and not line.startswith("  -"):
                k,v=line.split(":",1); current=k.strip(); v=v.strip()
                data[current] = [] if v == "" else v
            elif line.strip().startswith("-") and current:
                data.setdefault(current, []).append(line.strip()[1:].strip())
        return AppConfig(**data)
    return AppConfig()
