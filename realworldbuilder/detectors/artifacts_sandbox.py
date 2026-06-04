from .base import KeywordDetector
class ArtifactsSandboxDetector(KeywordDetector):
    name = "artifacts_sandbox"
    categories = tuple("artifacts_sandbox".split(","))
