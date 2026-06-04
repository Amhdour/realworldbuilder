from .base import KeywordDetector
class BackendDetector(KeywordDetector):
    name = "backend"
    categories = tuple("backend".split(","))
