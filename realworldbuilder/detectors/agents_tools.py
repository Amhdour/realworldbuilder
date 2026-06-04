from .base import KeywordDetector
class AgentsToolsDetector(KeywordDetector):
    name = "agents_tools"
    categories = tuple("agent_tool".split(","))
