from fastapi import APIRouter
from app.services.mock_data import mock_db
from app.models.core import DashboardStats, Threat, Status

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/", response_model=DashboardStats)
def get_dashboard_stats():
    # Calculate stats from mock data
    active_threats = [t for t in mock_db.threats if t.status not in [Status.RESOLVED, Status.IGNORED]]
    active_count = len(active_threats)
    
    blocked_count = sum(1 for e in mock_db.events if e.type == "DEPLOY_BLOCKED")
    
    # Mocked complex calculation
    zap_risk_global = 73
    mttr_hours = 2.3
    
    return DashboardStats(
        zap_risk_global=zap_risk_global,
        blocked_today=blocked_count,
        mttr_hours=mttr_hours,
        active_threats_count=active_count
    )

@router.get("/activity")
def get_recent_activity():
    return mock_db.events[:10]

@router.get("/trends")
def get_risk_trends():
    """Return last 30 days of risk trends"""
    return mock_db.scan_history

@router.get("/notifications")
def get_notifications():
    """Return unread notifications"""
    return mock_db.notifications

@router.post("/notifications/{notification_id}/read")
def mark_notification_read(notification_id: int):
    """Mark a notification as read"""
    for notif in mock_db.notifications:
        if notif["id"] == notification_id:
            notif["read"] = True
            return {"success": True}
    return {"success": False}
