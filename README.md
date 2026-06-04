# RealWorldBuilder

RealWorldBuilder is a local, evidence-first readiness builder that helps move a RAG/agent repository toward production-style portfolio readiness by mapping architecture, security gaps, patch points, tests, demo attacks, CI gates, evidence, and safe public claims.

## What RealWorldBuilder does
- Scans a target repository using conservative path, filename, and limited text heuristics.
- Fingerprints the scanned state and produces Markdown and JSON reports.
- Detects likely backend, frontend, tests, CI/CD, deployment, RAG, agent, MCP, artifact, sandbox, audit, telemetry, policy, evidence, and supply-chain indicators.
- Maps likely patch points and threat-control relationships.
- Generates conservative readiness scores, public/private evidence classification, safe public claims, known limitations, and Codex-ready next tasks.
- Verifies read-only behavior with before/after snapshots.

## What RealWorldBuilder does not do
- It does not modify the target repository in Phase 1.
- It does not auto-patch, delete, or rewrite target files.
- It does not perform full vulnerability scanning.
- It does not implement SARIF export in Phase 1.
- It does not prove control effectiveness from keyword matches.

## Why it does not claim enterprise readiness
Enterprise readiness requires evidence beyond a local heuristic scan: staging validation, monitoring, rollback drills, operational runbooks, CI logs, and external validation. RealWorldBuilder separates MVP / production-style portfolio work from later enterprise work so public claims remain conservative.

## Installation
```bash
python -m pip install -e ".[dev]"
```

## Usage
```bash
python -m realworldbuilder scan /path/to/target/repo
python -m realworldbuilder scan /path/to/target/repo --output /path/to/output
python -m realworldbuilder scan /path/to/repo --ci --fail-on-critical
python -m realworldbuilder compare --before /path/to/old/output --after /path/to/new/output
```

Default output folder:
```text
./realworldbuilder_output/<target_repo_name>/
```

Profiles: `rag`, `agent`, `rag-agent`, `mcp`, `general-ai-app`. Default: `rag-agent`.
Privacy modes: `internal` and `public`. Public mode redacts local paths, usernames, email addresses, and likely secrets, and limits exploit detail.

## Claim rules
Do not claim production readiness, enterprise readiness, compliance, certification, complete security, or that controls work unless evidence supports the exact claim. If RealWorldBuilder cannot confirm something, reports use: “I cannot confirm this from the provided project.”

## Readiness scoring model
Scores are conservative and separated into repository visibility, architecture understanding, patch-point readiness, control implementation, tests, demo attacks, CI, evidence, staging, production-style portfolio readiness, and enterprise production-candidate readiness. Scores never output 100%, and enterprise production-candidate readiness remains low without staging, monitoring, rollback, CI, and external validation indicators.

## Evidence strength model
0 not found; 1 file/path indicator; 2 code indicator; 3 test indicator; 4 negative/security test; 5 demo attack; 6 CI evidence; 7 staging/deployment evidence; 8 telemetry/audit evidence; 9 external validation.

## Control maturity model
0 not identified; 1 patch point; 2 policy; 3 enforcement; 4 unit tested; 5 negative/security tested; 6 demo attack; 7 CI gated; 8 staging validated; 9 monitored; 10 externally validated.

## Public/private evidence rules
Evidence is classified as `public_safe`, `private_internal`, or `sensitive_do_not_publish` with reasons such as secrets, PII, internal paths, customer data, exploit details, or safe synthetic demo only.

## CI mode
`--ci --fail-on-critical` returns exit code 1 if critical gaps are present. Phase 1 does not fail solely because gaps exist unless `--fail-on-critical` is passed.

## Portfolio usage
Use the reports to demonstrate disciplined security-readiness engineering: patch-point mapping, gaps, safe claims, evidence separation, and next tasks. Do not present heuristic reports as final proof.

## Known limitations
Phase 1 requires manual review, tests, CI logs, staging validation, and external validation for stronger claims. It intentionally avoids target modification, full vulnerability scanning, auto-patching, and SARIF export.

## Roadmap
See `docs/roadmap.md` for Phase 1 through Phase 4 and backlog SARIF notes.
