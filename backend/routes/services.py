from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from config.database import execute_query
from middleware.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("")
async def get_services():
    services = execute_query("SELECT * FROM services WHERE is_active = TRUE ORDER BY sort_order ASC, created_at DESC", fetch_all=True)
    return {"services": services}


class ServiceCreate(BaseModel):
    title: str
    description: str | None = None
    icon: str | None = None
    price: float | None = None
    category: str | None = None
    features: list[str] = []


@router.post("")
async def create_service(data: ServiceCreate, current_user=Depends(get_current_user)):
    import json
    result = execute_query(
        """
        INSERT INTO services 
        (title, description, icon, features, price_value) 
        VALUES (%s, %s, %s, %s, %s) 
        RETURNING *
        """,
        (data.title, data.description, data.icon, json.dumps(data.features), data.price),
        fetch_one=True
    )
    
    return {
        "message": "Service created", 
        "service": result
    }
