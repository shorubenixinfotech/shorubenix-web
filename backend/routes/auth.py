from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from config.database import execute_query
from middleware.auth import hash_password, verify_password, create_access_token, get_current_user
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str


class UpdateProfileRequest(BaseModel):
    name: str | None = None
    phone: str | None = None


@router.post("/register")
async def register(data: RegisterRequest):
    # Check if email exists
    existing = execute_query("SELECT id FROM users WHERE email = %s", (data.email,), fetch_one=True)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    password_hash = hash_password(data.password)
    
    result = execute_query(
        "INSERT INTO users (name, email, password_hash, phone) VALUES (%s, %s, %s, %s) RETURNING id",
        (data.name, data.email, password_hash, data.phone),
        fetch_one=True
    )
    user_id = result['id']

    token = create_access_token({"sub": str(user_id), "email": data.email, "role": "user"})

    return {
        "message": "Registration successful",
        "token": token,
        "user": {
            "id": user_id,
            "name": data.name,
            "email": data.email,
            "phone": data.phone,
            "role": "user",
        }
    }


@router.post("/login")
async def login(data: LoginRequest):
    user = execute_query("SELECT * FROM users WHERE email = %s AND is_active = TRUE", (data.email,), fetch_one=True)
    
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user_id = user["id"]
    token = create_access_token({"sub": str(user_id), "email": user["email"], "role": user["role"]})

    return {
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user_id,
            "name": user["name"],
            "email": user["email"],
            "phone": user.get("phone"),
            "role": user["role"],
        }
    }


@router.post("/admin-login")
async def admin_login(data: LoginRequest):
    # Check admin_users table
    admin = execute_query("SELECT * FROM admin_users WHERE email = %s AND is_active = TRUE", (data.email,), fetch_one=True)
    
    if not admin:
        # Also allow users with role='admin' in users table
        admin = execute_query("SELECT * FROM users WHERE email = %s AND role = 'admin' AND is_active = TRUE", (data.email,), fetch_one=True)
    
    if not admin or not verify_password(data.password, admin["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid admin credentials")

    admin_id = admin["id"]
    token = create_access_token({"sub": str(admin_id), "email": admin["email"], "role": "admin"})

    return {
        "message": "Admin login successful",
        "token": token,
        "user": {
            "id": admin_id,
            "name": admin.get("username", admin.get("name", "Admin")),
            "email": admin["email"],
            "role": "admin",
        }
    }


@router.post("/setup-admin")
async def setup_admin(data: RegisterRequest):
    """Create an admin user (first-time setup only)."""
    admin_count = execute_query("SELECT COUNT(*) as count FROM admin_users", fetch_one=True)['count']
    if admin_count > 0:
        raise HTTPException(status_code=400, detail="Admin already exists. Use admin-login.")

    password_hash = hash_password(data.password)
    
    result = execute_query(
        "INSERT INTO admin_users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id",
        (data.name, data.email, password_hash),
        fetch_one=True
    )
    admin_id = result['id']

    token = create_access_token({"sub": str(admin_id), "email": data.email, "role": "admin"})

    return {
        "message": "Admin account created",
        "token": token,
        "user": {
            "id": admin_id,
            "name": data.name,
            "email": data.email,
            "role": "admin",
        }
    }


@router.get("/profile")
async def get_profile(current_user=Depends(get_current_user)):
    user_id = current_user["id"]

    # Check users table
    user = execute_query("SELECT * FROM users WHERE id = %s", (user_id,), fetch_one=True)
    if not user:
        # Check admin_users table
        user = execute_query("SELECT * FROM admin_users WHERE id = %s", (user_id,), fetch_one=True)
        if not user:
            raise HTTPException(status_code=404, detail="User or Admin not found")
    
    user_data = dict(user)
    user_data.pop("password_hash", None)
    
    # Format dates if needed
    for key in ["created_at", "updated_at", "published_at"]:
        if key in user_data and isinstance(user_data[key], datetime):
            user_data[key] = user_data[key].isoformat()

    return {"user": user_data}


@router.put("/profile")
async def update_profile(data: UpdateProfileRequest, current_user=Depends(get_current_user)):
    user_id = current_user["id"]

    updates = []
    params = []
    if data.name is not None:
        updates.append("name = %s")
        params.append(data.name)
    if data.phone is not None:
        updates.append("phone = %s")
        params.append(data.phone)

    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    updates.append("updated_at = CURRENT_TIMESTAMP")
    
    query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s RETURNING *"
    params.append(user_id)
    
    result = execute_query(query, tuple(params), fetch_one=True)

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = dict(result)
    user_data.pop("password_hash", None)

    return {"message": "Profile updated", "user": user_data}
