from __future__ import annotations
from abc import ABC, abstractmethod
from ..models import Finding, ScanFile

class BaseDetector(ABC):
    name: str
    categories: tuple[str, ...]
    @abstractmethod
    def detect(self, files: list[ScanFile]) -> list[Finding]: ...

class KeywordDetector(BaseDetector):
    name = "keyword"
    categories: tuple[str, ...] = ()
    def detect(self, files: list[ScanFile]) -> list[Finding]:
        out: list[Finding] = []
        for f in files:
            hay = f"{f.path.lower()} {f.text_sample.lower()}"
            for cat in self.categories:
                if cat in f.kind.split(","):
                    content_hit = any(k in f.text_sample.lower() for k in cat.split("_"))
                    out.append(Finding(category=cat, path=f.path, confidence="high" if content_hit else "medium", evidence_strength=2 if content_hit else 1, reason="conservative path/content heuristic"))
        return out
