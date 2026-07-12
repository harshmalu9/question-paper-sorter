# FastAPI application entry point.
# Includes versioned routers, CORS, and root health-check endpoint.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.upload import router as upload_router
from app.api.v1.health import router as health_router

app = FastAPI(
    title=settings.APP_NAME,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Versioned API routes
app.include_router(health_router, prefix=settings.API_PREFIX)
app.include_router(upload_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    """Root health-check endpoint."""
    return {
        "status": "alive",
        "service": "question-paper-sorter-backend",
    }
