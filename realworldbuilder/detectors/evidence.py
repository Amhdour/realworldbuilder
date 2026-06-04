from .base import KeywordDetector
class EvidenceDetector(KeywordDetector):
    name = "evidence"
    categories = tuple("evidence".split(","))
