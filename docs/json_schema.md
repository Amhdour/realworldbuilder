# JSON Schema Contract

Every JSON report includes:
- `schema_version`: `1.0.0`
- `tool_name`: `RealWorldBuilder`
- `tool_version`: `0.1.0`
- `generated_at`: ISO-8601 timestamp
- `target_repo_fingerprint_id`: string
- `data`: report-specific object

Field names must not change without updating `schema_version`.
