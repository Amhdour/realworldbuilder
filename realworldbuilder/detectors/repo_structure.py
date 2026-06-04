from .base import KeywordDetector
class RepoStructureDetector(KeywordDetector):
    name = "repo_structure"
    categories = tuple("docs,backend,frontend".split(","))
