from .repo_structure import RepoStructureDetector
from .backend import BackendDetector
from .frontend import FrontendDetector
from .tests import TestsDetector
from .ci_cd import CiCdDetector
from .deployment import DeploymentDetector
from .rag_retrieval import RagRetrievalDetector
from .agents_tools import AgentsToolsDetector
from .mcp import McpDetector
from .artifacts_sandbox import ArtifactsSandboxDetector
from .audit_telemetry import AuditTelemetryDetector
from .policies import PoliciesDetector
from .evidence import EvidenceDetector
from .supply_chain import SupplyChainDetector

def all_detectors():
    return [RepoStructureDetector(), BackendDetector(), FrontendDetector(), TestsDetector(), CiCdDetector(), DeploymentDetector(), RagRetrievalDetector(), AgentsToolsDetector(), McpDetector(), ArtifactsSandboxDetector(), AuditTelemetryDetector(), PoliciesDetector(), EvidenceDetector(), SupplyChainDetector()]
