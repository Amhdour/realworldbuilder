from __future__ import annotations
from pathlib import Path
import hashlib
from .classify_files import is_text_file

def snapshot(target: Path) -> dict:
    files=[]; dirs=[]; mtimes=[]
    for p in sorted(target.rglob("*")):
        if ".git" in p.parts: continue
        st=p.stat(); mtimes.append(st.st_mtime)
        if p.is_dir(): dirs.append(str(p.relative_to(target)))
        else: files.append(p)
    hashes={}
    for p in files[:200]:
        try:
            if is_text_file(p) and p.stat().st_size <= 64*1024:
                hashes[str(p.relative_to(target))]=hashlib.sha256(p.read_bytes()).hexdigest()
        except Exception: pass
    return {"file_count": len(files), "directory_count": len(dirs), "selected_file_hashes": hashes, "latest_mtime": max(mtimes) if mtimes else None}

def verify(before: dict, after: dict) -> dict:
    return {"changed_during_scan": before != after, "before": before, "after": after, "statement": "The target repository changed during the scan." if before != after else "The target repository did not change during the scan."}
