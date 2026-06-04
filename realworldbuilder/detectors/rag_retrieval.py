from .base import KeywordDetector
class RagRetrievalDetector(KeywordDetector):
    name = "rag_retrieval"
    categories = tuple("rag_retrieval".split(","))
