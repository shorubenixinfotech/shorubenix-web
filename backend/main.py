import logging
import sys
import os

# Ensure backend directory is in path
sys.path.insert(0, os.path.dirname(__file__))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from config.settings import settings
from config.database import init_database
from routes.auth import router as auth_router
from routes.projects import router as projects_router
from routes.payments import router as payments_router
from routes.contacts import router as contacts_router
from routes.blog import router as blog_router
from routes.services import router as services_router
from routes.admin import router as admin_router


# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("ShoRubenix Backend Starting...")
    try:
        init_database()
        logger.info("Database initialized successfully")
        
        # Seed default admin if none exists
        from config.database import execute_query
        from middleware.auth import hash_password
        
        admin_count = execute_query("SELECT COUNT(*) as count FROM admin_users", fetch_one=True)['count']
        if admin_count == 0:
            logger.info("Seeding default admin...")
            pwd_hash = hash_password("admin123")
            execute_query(
                "INSERT INTO admin_users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                ("Admin", "admin@shorubenix.com", pwd_hash, "admin")
            )
            logger.info("Default admin created: admin@shorubenix.com / admin123")
            
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        logger.warning("Server will continue without database. Some features may be limited.")
    yield
    # Shutdown
    logger.info("ShoRubenix Backend Shutting Down...")


app = FastAPI(
    title="ShoRubenix Infotech API",
    description="Backend API for ShoRubenix Freelancer IT Website",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Configuration
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "https://planning-with-ai-fea7d.web.app",
    "https://planning-with-ai-fea7d.firebaseapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    logger.error(f"Internal server error: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    import time
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - {response.status_code} ({duration:.2f}s)")
    return response

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(projects_router, prefix="/api")
app.include_router(payments_router, prefix="/api")
app.include_router(contacts_router, prefix="/api")
app.include_router(blog_router, prefix="/api")
app.include_router(services_router, prefix="/api")
app.include_router(admin_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "name": "ShoRubenix Infotech API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "ShoRubenix Backend"}


# Analytics tracking endpoint
@app.post("/api/analytics/track")
async def track_event(request: Request):
    try:
        body = await request.json()
        from config.database import execute_query
        execute_query(
            "INSERT INTO analytics (event_type, description, user_id) VALUES (%s, %s, %s)",
            (body.get("event_type", "page_view"), body.get("page", "/"), body.get("user_id"))
        )
        return {"message": "Event tracked"}
    except Exception:
        return {"message": "Tracking skipped"}


# Newsletter subscription
@app.post("/api/newsletter/subscribe")
async def subscribe_newsletter(request: Request):
    try:
        body = await request.json()
        email = body.get("email")
        if not email:
            return JSONResponse(status_code=400, content={"detail": "Email is required"})

        from config.database import execute_query
        # Insert or ignore if duplicate
        execute_query(
            "INSERT INTO newsletter_subscribers (email) VALUES (%s) ON CONFLICT (email) DO UPDATE SET is_active = TRUE",
            (email,)
        )
        return {"message": "Subscribed successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})


if __name__ == "__main__":
    import uvicorn
    # Use 0.0.0.0 for containerized environments like Railway
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
