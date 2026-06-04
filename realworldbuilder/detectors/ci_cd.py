from .base import KeywordDetector
class CiCdDetector(KeywordDetector):
    name = "ci_cd"
    categories = tuple("ci_cd".split(","))
