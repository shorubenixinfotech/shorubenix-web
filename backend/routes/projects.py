from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from config.database import execute_query
from middleware.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/projects", tags=["Projects"])


class ProjectCreate(BaseModel):
    title: str
    description: str | None = None
    category: str | None = None
    tech: list[str] = []
    image_url: str | None = None
    live_url: str | None = None
    github_url: str | None = None
    client_name: str | None = None


@router.get("")
async def get_projects():
    projects = execute_query("SELECT * FROM projects WHERE status = 'active' ORDER BY is_featured DESC, created_at DESC", fetch_all=True)
    return {"projects": projects}


@router.get("/my-projects")
async def get_my_projects(current_user=Depends(get_current_user)):
    projects = execute_query("""
        SELECT p.*, up.purchased_at 
        FROM user_projects up
        JOIN projects p ON up.project_id = p.id
        WHERE up.user_id = %s
    """, (current_user["id"],), fetch_all=True)
    return {"projects": projects}


@router.get("/{project_id}")
async def get_project(project_id: int):
    project = execute_query("SELECT * FROM projects WHERE id = %s", (project_id,), fetch_one=True)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"project": project}


@router.post("")
async def create_project(data: ProjectCreate, current_user=Depends(get_current_user)):
    import json
    project = execute_query(
        """
        INSERT INTO projects 
        (user_id, title, description, category, tech, image_url, live_url, github_url, client_name) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
        RETURNING *
        """,
        (current_user["id"], data.title, data.description, data.category, json.dumps(data.tech), 
         data.image_url, data.live_url, data.github_url, data.client_name),
        fetch_one=True
    )
    return {"message": "Project created", "project": project}


@router.put("/{project_id}")
async def update_project(project_id: int, data: ProjectCreate, current_user=Depends(get_current_user)):
    import json
    updates = []
    params = []
    for key, value in data.dict().items():
        if value is not None:
            updates.append(f"{key} = %s")
            if isinstance(value, list):
                params.append(json.dumps(value))
            else:
                params.append(value)
    
    if not updates:
        raise HTTPException(status_code=400, detail="No updates provided")
        
    updates.append("updated_at = CURRENT_TIMESTAMP")
    query = f"UPDATE projects SET {', '.join(updates)} WHERE id = %s RETURNING *"
    params.append(project_id)
    
    project = execute_query(query, tuple(params), fetch_one=True)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    return {"message": "Project updated", "project": project}


@router.delete("/{project_id}")
async def delete_project(project_id: int, current_user=Depends(get_current_user)):
    execute_query("UPDATE projects SET status = 'deleted' WHERE id = %s", (project_id,))
    return {"message": "Project deleted"}
