from .base import KeywordDetector
class TestsDetector(KeywordDetector):
    name = "tests"
    categories = tuple("tests,security_test".split(","))
