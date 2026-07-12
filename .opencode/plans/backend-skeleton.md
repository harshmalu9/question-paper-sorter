# FastAPI Backend Skeleton

## Files to create

### `backend/requirements.txt`
```
fastapi>=0.115.0
uvicorn>=0.30.0
python-multipart>=0.0.9
```

### `backend/app/__init__.py` — empty

### `backend/app/routes/__init__.py` — empty

### `backend/app/routes/upload.py`
```python
# Upload route — accepts .pdf / .zip files,
# saves them to backend/uploads/, returns filename + size.
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".zip"}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Only {', '.join(ALLOWED_EXTENSIONS)} files are allowed.",
        )
    dest = UPLOAD_DIR / file.filename
    content = await file.read()
    dest.write_bytes(content)
    return {
        "filename": file.filename,
        "size_bytes": len(content),
    }
```

### `backend/app/main.py`
```python
# FastAPI application entry point.
# Includes routers and defines the root health-check endpoint.
from pathlib import Path
from fastapi import FastAPI

from app.routes.upload import router as upload_router

app = FastAPI(
    title="Question Paper Sorter API",
)

app.include_router(upload_router)


@app.get("/")
async def root():
    return {
        "status": "alive",
        "service": "question-paper-sorter-backend",
    }
```

## Run commands

```bash
# Install deps into existing root venv (~/proj/question-paper-sorter/venv/)
source venv/bin/activate
pip install fastapi uvicorn python-multipart

# Start dev server from project root
uvicorn backend.app.main:app --reload --port 8000
```

## Verify

```bash
curl http://localhost:8000/
# {"status":"alive","service":"question-paper-sorter-backend"}

curl -F "file=@test.pdf" http://localhost:8000/upload
# {"filename":"test.pdf","size_bytes":12345}
```
