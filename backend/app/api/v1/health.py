# Health check endpoint for API v1.

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Returns service health status."""
    return {"status": "healthy"}
