from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum
from sqlmodel import SQLModel, Field, JSON

class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Status(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    FIX_READY = "fix_ready"
    RESOLVED = "resolved"
    IGNORED = "ignored"

class Cluster(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    provider: str  # AWS, GKE, On-Prem
    namespace_count: int
    pod_count: int
    risk_score: int
    status: str # connected, degraded, disconnected
    last_scan: datetime

class Threat(SQLModel, table=True):
    id: str = Field(primary_key=True)
    cluster_id: str = Field(foreign_key="cluster.id")
    title: str
    cwe_id: str
    cve_id: Optional[str] = None
    severity: Severity
    target_namespace: str
    target_kind: str # valid: deployment, service, ingress
    target_name: str
    zap_risk_score: int
    status: Status
    created_at: datetime = Field(default_factory=datetime.now)
    description: str
    
    # Detailed fields stored as JSON
    ai_summary: str
    attack_path_steps: List[str] = Field(default=[], sa_type=JSON) 
    zap_raw_output: Dict = Field(default={}, sa_type=JSON)
    fix_options: List[Dict] = Field(default=[], sa_type=JSON) # List of proposed fixes

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cluster_id: str
    type: str # SCAN_COMPLETED, DEPLOY_BLOCKED, etc.
    description: str
    timestamp: datetime = Field(default_factory=datetime.now)
    severity: str = "info" # info, warning, error, success

class DashboardStats(SQLModel):
    zap_risk_global: int
    blocked_today: int
    mttr_hours: float
    active_threats_count: int
