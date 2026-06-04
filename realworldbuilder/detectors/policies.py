from .base import KeywordDetector
class PoliciesDetector(KeywordDetector):
    name = "policies"
    categories = tuple("policy".split(","))
