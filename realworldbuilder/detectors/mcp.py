from .base import KeywordDetector
class McpDetector(KeywordDetector):
    name = "mcp"
    categories = tuple("mcp".split(","))
