from __future__ import annotations
from pathlib import Path
import hashlib, subprocess
from datetime import datetime, timezone
from .models import ScanResult

def git_value(target: Path, args: list[str]) -> str | None:
    try:
        return subprocess.check_output(["git", "-C", str(target), *args], text=True, stderr=subprocess.DEVNULL).strip() or None
    except Exception:
        return None

def build_fingerprint(target: Path, scan: ScanResult, profile: str, privacy: str) -> dict:
    basis = "\n".join(f.path for f in scan.files) + str(sum(f.size for f in scan.files))
    fid = hashlib.sha256(basis.encode()).hexdigest()[:16]
    return {"fingerprint_id": fid, "target_repo_path": str(target.resolve()), "scan_timestamp": datetime.now(timezone.utc).isoformat(), "git_branch": git_value(target, ["rev-parse", "--abbrev-ref", "HEAD"]), "git_commit_sha": git_value(target, ["rev-parse", "HEAD"]), "dirty_working_tree": bool(git_value(target, ["status", "--porcelain"])), "total_files_scanned": len(scan.files), "total_files_ignored": scan.ignored_count, "scanner_version": "0.1.0", "profile": profile, "privacy": privacy, "scan_limitations": ["Phase 1 uses conservative heuristics only.", "I cannot confirm this from the provided project."]}
