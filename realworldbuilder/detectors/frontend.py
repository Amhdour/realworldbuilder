from .base import KeywordDetector
class FrontendDetector(KeywordDetector):
    name = "frontend"
    categories = tuple("frontend".split(","))
