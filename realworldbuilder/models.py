from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal
from pydantic import BaseModel, Field
from .constants import SCHEMA_VERSION, TOOL_NAME, TOOL_VERSION

Status = Literal["detected", "missing", "unconfirmed", "planned"]
Confidence = Literal["high", "medium", "low"]

class Finding(BaseModel):
    category: str
    path: str
    status: Status = "detected"
    confidence: Confidence = "low"
    evidence_strength: int = 1
    control_maturity: int = 1
    reason: str = "path indicator"
    manual_review: list[str] = Field(default_factory=lambda: ["needs_manual_review"])

class ScanFile(BaseModel):
    path: str
    size: int
    kind: str
    text_sample: str = ""

class ScanResult(BaseModel):
    target_path: str
    files: list[ScanFile]
    ignored_count: int
    findings: list[Finding]

class ReportEnvelope(BaseModel):
    schema_version: str = SCHEMA_VERSION
    tool_name: str = TOOL_NAME
    tool_version: str = TOOL_VERSION
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    target_repo_fingerprint_id: str
    data: dict[str, Any]
