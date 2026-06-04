from .base import KeywordDetector
class AuditTelemetryDetector(KeywordDetector):
    name = "audit_telemetry"
    categories = tuple("audit_telemetry".split(","))
