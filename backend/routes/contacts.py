from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.database import execute_query
from datetime import datetime

router = APIRouter(prefix="/contacts", tags=["Contacts"])


class ContactCreate(BaseModel):
    name: str
    email: str
    phone: str | None = None
    subject: str | None = None
    message: str


@router.post("")
async def submit_contact(data: ContactCreate):
    result = execute_query(
        """
        INSERT INTO contacts (name, email, subject, message, status) 
        VALUES (%s, %s, %s, %s, 'New') 
        RETURNING *
        """,
        (data.name, data.email, data.subject, data.message),
        fetch_one=True
    )

    # Log the contact in system_logs
    execute_query(
        "INSERT INTO system_logs (event_type, description) VALUES (%s, %s)",
        ("info", f"New contact from {data.name} ({data.email})")
    )

    return {
        "message": "Message sent successfully", 
        "contact": result
    }


@router.get("")
async def get_contacts():
    contacts = execute_query("SELECT * FROM contacts ORDER BY created_at DESC", fetch_all=True)
    return {"contacts": contacts}
