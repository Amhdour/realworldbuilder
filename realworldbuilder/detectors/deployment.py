from .base import KeywordDetector
class DeploymentDetector(KeywordDetector):
    name = "deployment"
    categories = tuple("deployment".split(","))
