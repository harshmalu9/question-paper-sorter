# Question Paper Sorter

Automatically sort scanned question papers into individual grouped PDFs using OCR and document boundary detection.

---

## Description

A mixed collection of scanned question paper pages (PDF or ZIP of images) is processed through an OCR pipeline that detects boundaries between separate papers. Each group is exported as a separate PDF with metadata.

The system works as both a CLI tool and a web service with a FastAPI backend.

---

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│   Frontend   │────▶│  FastAPI Backend │────▶│  Processing  │
│  (React)     │     │   /api/v1        │     │    Engine    │
└─────────────┘     └─────────────────┘     └──────────────┘
                           │                       │
                     Upload & Jobs           OCR + Grouping
                     Result Retrieval        PDF Export
                     File Download           Metadata
```

### Engine (`engine/`)

Self-contained processing pipeline with no backend dependencies.

- `ocr/` — EasyOCR wrapper with rotation detection and caching
- `product/` — Ingestion, group detection (TF-IDF + keywords), ordering, and export
- `models/` — Data models for pages, groups, and documents

### Backend (`backend/app/`)

FastAPI service exposing the engine over HTTP.

- `api/v1/` — Versioned REST endpoints
- `jobs/` — In-memory job manager and status tracking
- `services/` — Single bridge to the engine (`pipeline.py`)
- `core/` — Configuration via pydantic-settings

### Data (`data/`)

Runtime directories (not committed). Created automatically.

- `data/input/` — User-supplied input files
- `data/temp/` — Temporary images from PDF conversion
- `data/cache/` — OCR text cache
- `data/output/` — CLI output directory

---

## Current Status

### Implemented

- PDF and ZIP input processing
- GPU-accelerated OCR with rotation detection
- OCR result caching to disk
- Group detection via TF-IDF cosine similarity and keyword boundary scoring
- Per-group confidence metrics
- PDF export (one file per detected group)
- Metadata JSON generation
- CLI interface (`python main.py`)

### Backend API

- File upload (PDF/ZIP)
- Background job processing with progress tracking
- Job status polling
- Result retrieval (generated file list)
- File download with path traversal protection

### In Progress

- React frontend

See `PROJECT_ROADMAP.md` for full roadmap.

---

## Local Setup

```bash
git clone https://github.com/harshmalu9/question-paper-sorter.git
cd question-paper-sorter

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

## Running

### CLI

```bash
python main.py data/input/sample.pdf
```

Options:

- `--output-dir DIR` — Output directory (default: `output/`)
- `--temp-dir DIR` — Temporary image directory (default: `data/temp/`)
- `--quiet` — Suppress verbose output

### Backend API

Must be started from the repository root:

```bash
uvicorn backend.app.main:app --reload
```

API base: `http://localhost:8000/api/v1`

#### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/health` | Health check |
| `POST` | `/api/v1/jobs` | Upload file and create processing job |
| `GET` | `/api/v1/jobs` | List all jobs |
| `GET` | `/api/v1/jobs/{job_id}` | Get job status |
| `GET` | `/api/v1/jobs/{job_id}/results` | Get result file list |
| `GET` | `/api/v1/download/{job_id}/{filename}` | Download a generated file |

---

## Technologies

- Python, FastAPI
- EasyOCR, PyTorch
- OpenCV, Pillow
- TF-IDF, scikit-learn
- pdf2image

---

## Author

Harsh Malu — MIT-WPU, Computer Science Engineering
