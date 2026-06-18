# FastAPI application entry point.
# Includes routers and defines the root health-check endpoint.

from fastapi import FastAPI

from app.routes.upload import router as upload_router

app = FastAPI(
    title="Question Paper Sorter API",
)

app.include_router(upload_router)


@app.get("/")
async def root():
    """Health-check endpoint."""
    return {
        "status": "alive",
        "service": "question-paper-sorter-backend",
    }
