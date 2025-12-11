from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.services.mock_data import mock_db
from app.models.core import Threat, Status

router = APIRouter(prefix="/threats", tags=["Threats"])

@router.get("/", response_model=List[Threat])
def list_threats(cluster_id: Optional[str] = None):
    threats = mock_db.threats
    if cluster_id:
        threats = [t for t in threats if t.cluster_id == cluster_id]
    return threats

@router.get("/{threat_id}", response_model=Threat)
def get_threat(threat_id: str):
    threat = next((t for t in mock_db.threats if t.id == threat_id), None)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    return threat

@router.post("/{threat_id}/fix")
def generate_fix(threat_id: str):
    threat = next((t for t in mock_db.threats if t.id == threat_id), None)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    
    # Mock fix generation
    fix_type = threat.fix_options[0]["type"] if threat.fix_options else "generic"
    
    return {
        "success": True,
        "pr_url": f"https://github.com/org/repo/pull/123",
        "fix_type": fix_type,
        "message": f"Generated {fix_type} fix for {threat.title}"
    }

@router.post("/{threat_id}/snooze")
def snooze_threat(threat_id: str):
    threat = next((t for t in mock_db.threats if t.id == threat_id), None)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    
    # In a real app we'd update DB
    return {"success": True, "message": "Threat snoozed for 24h"}
