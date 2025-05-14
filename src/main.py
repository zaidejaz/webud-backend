from fastapi import FastAPI
from src.api.v1.routes import auth, template, chat, user
from fastapi.middleware.cors import CORSMiddleware
from src.database import init_db

# Create FastAPI app with enhanced documentation
app = FastAPI(
    title="Webud API",
    description="Backend API for the Webud application",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "Operations related to user authentication, login, and registration",
        },
        {
            "name": "Users",
            "description": "Operations related to user management and profiles",
        },
        {
            "name": "Templates",
            "description": "Operations related to templates",
        },
        {
            "name": "Chat",
            "description": "Operations related to chat functionality",
        },
    ]
)

# Include routers - note that auth router already has its own prefix
app.include_router(auth.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(template.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def on_startup():
    init_db()

@app.get("/")
async def root():
    """
    Root endpoint that confirms the API is running
    """
    return {"message": "Webud API is running"}

@app.get("/health")
async def health():
    """
    Health check endpoint
    """
    return {"status": "ok"}

