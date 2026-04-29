"""Security and permission controls for TafySH."""

from tafysh.security.approval import (
    ApprovalFlow,
    ApprovalRequest,
    ApprovalResponse,
    ApprovalResult,
    AutoApprover,
)
from tafysh.security.audit import AuditAction, AuditEvent, AuditLogger
from tafysh.security.classifier import (
    CommandRiskAssessment,
    RiskClassifier,
    RiskLevel,
    RiskPattern,
)
from tafysh.security.controller import (
    SecurityContext,
    SecurityController,
    SecurityDecision,
    ValidationResult,
)
from tafysh.security.policies import (
    DevicePolicy,
    PolicyManager,
    SecurityMode,
    SecurityPolicy,
)
from tafysh.security.rbac import Permission, RBAC, Role, User

__all__ = [
    # Risk Classification
    "RiskLevel",
    "RiskPattern",
    "RiskClassifier",
    "CommandRiskAssessment",
    # Policies
    "SecurityMode",
    "SecurityPolicy",
    "DevicePolicy",
    "PolicyManager",
    # RBAC
    "Role",
    "Permission",
    "User",
    "RBAC",
    # Approval
    "ApprovalResult",
    "ApprovalRequest",
    "ApprovalResponse",
    "ApprovalFlow",
    "AutoApprover",
    # Audit
    "AuditAction",
    "AuditEvent",
    "AuditLogger",
    # Controller
    "ValidationResult",
    "SecurityContext",
    "SecurityDecision",
    "SecurityController",
]
