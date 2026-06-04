from .base import KeywordDetector
class SupplyChainDetector(KeywordDetector):
    name = "supply_chain"
    categories = tuple("supply_chain".split(","))
