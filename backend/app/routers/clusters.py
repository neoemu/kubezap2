from fastapi import APIRouter, HTTPException
from typing import List
from app.services.mock_data import mock_db
from app.models.core import Cluster

router = APIRouter(prefix="/clusters", tags=["Clusters"])

@router.get("/", response_model=List[Cluster])
def list_clusters():
    return mock_db.clusters

@router.get("/{cluster_id}", response_model=Cluster)
def get_cluster(cluster_id: str):
    cluster = next((c for c in mock_db.clusters if c.id == cluster_id), None)
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    return cluster

@router.post("/{cluster_id}/scan")
def trigger_scan(cluster_id: str):
    return {"success": True, "message": f"Scan triggered for {cluster_id}"}
