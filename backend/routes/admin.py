from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from config.database import execute_query
from middleware.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/analytics")
async def get_analytics(current_user=Depends(get_current_user)):
    # Get user count
    user_count = execute_query("SELECT COUNT(*) as count FROM users", fetch_one=True)['count']
    
    # Get payment stats
    payment_stats = execute_query("SELECT COUNT(*) as count, COALESCE(SUM(amount), 0) as total FROM payments WHERE status = 'completed'", fetch_one=True)
    
    # Get contact count
    contact_count = execute_query("SELECT COUNT(*) as count FROM contacts", fetch_one=True)['count']
    
    # Get project count
    project_count = execute_query("SELECT COUNT(*) as count FROM projects WHERE status = 'active'", fetch_one=True)['count']
    
    # Recent analytics events
    recent_events = execute_query("SELECT * FROM analytics ORDER BY created_at DESC LIMIT 20", fetch_all=True)

    return {
        "analytics": {
            "total_users": user_count,
            "total_revenue": float(payment_stats["total"]),
            "total_payments": payment_stats["count"],
            "total_contacts": contact_count,
            "total_projects": project_count,
            "recent_events": recent_events,
        }
    }


@router.get("/users")
async def get_users(current_user=Depends(get_current_user)):
    users = execute_query("SELECT * FROM users ORDER BY created_at DESC", fetch_all=True)
    for u in users:
        u.pop("password_hash", None)
    return {"users": users}


@router.get("/user-projects")
async def get_all_user_projects(current_user=Depends(get_current_user)):
    results = execute_query("""
        SELECT 
            u.id as user_id, 
            u.name as user_name, 
            u.email as user_email, 
            u.phone as user_phone,
            p.id as project_id, 
            p.title as project_title, 
            p.category as project_category,
            up.purchased_at
        FROM users u
        JOIN user_projects up ON u.id = up.user_id
        JOIN projects p ON up.project_id = p.id
        ORDER BY up.purchased_at DESC, u.id ASC
    """, fetch_all=True)
    return {"user_projects": results}


class NotificationCreate(BaseModel):
    user_id: str | None = None
    title: str
    message: str | None = None
    type: str = "info"


@router.post("/notifications")
async def send_notification(data: NotificationCreate, current_user=Depends(get_current_user)):
    if data.user_id:
        execute_query(
            "INSERT INTO notifications (user_id, title, message, type) VALUES (%s, %s, %s, %s)",
            (data.user_id, data.title, data.message, data.type)
        )
    else:
        # Send to all active users
        users = execute_query("SELECT id FROM users WHERE is_active = TRUE", fetch_all=True)
        for user in users:
            execute_query(
                "INSERT INTO notifications (user_id, title, message, type) VALUES (%s, %s, %s, %s)",
                (user['id'], data.title, data.message, data.type)
            )
            
    return {"message": "Notification sent successfully"}


@router.get("/complaints")
async def get_complaints(current_user=Depends(get_current_user)):
    complaints = execute_query("SELECT * FROM complaints ORDER BY created_at DESC", fetch_all=True)
    return {"complaints": complaints}


@router.get("/logs")
async def get_system_logs(current_user=Depends(get_current_user)):
    logs = execute_query("SELECT * FROM system_logs ORDER BY created_at DESC LIMIT 100", fetch_all=True)
    return {"logs": logs}


@router.get("/newsletter")
async def get_subscribers(current_user=Depends(get_current_user)):
    subscribers = execute_query("SELECT * FROM newsletter_subscribers WHERE is_active = TRUE ORDER BY created_at DESC", fetch_all=True)
    return {"subscribers": subscribers}
