# Project Roadmap

---

## Project Vision

The goal is to build a production-ready Question Paper Sorter.

The product accepts either:

- A PDF
- A ZIP of images
- (future) Multiple uploaded images

The output is multiple grouped PDFs representing individual papers.

The grouping accuracy is the highest priority.

Page ordering is secondary.

The product must be useful even without AI.

---

## Product Philosophy

The product should solve one problem extremely well:

Convert a mixed collection of question paper pages into correctly grouped PDFs.

AI is an enhancement, not the product.

---

## Current MVP

The following functionality is implemented and operational:

### PDF Input

- Accepts a single PDF file containing multiple question papers
- Converts all pages to images for downstream processing
- Preserves original image quality throughout the pipeline

### ZIP Input

- Accepts a ZIP archive containing image files (JPG, PNG)
- Extracts and flattens images into a processing directory
- Warns users about page ordering limitations with ZIP input

### OCR

- Uses EasyOCR for local text extraction
- Performs automatic rotation detection (0, 90, 180, 270 degrees)
- Scores OCR quality and selects the best rotation for each page
- Applies image preprocessing before OCR for improved accuracy

### Group Detection

- Identifies boundaries between separate question papers
- Uses keyword-based boundary scoring (university headers, exam titles, department names)
- Uses TF-IDF cosine similarity to measure adjacent page similarity
- Merges low-similarity regions into groups with computed confidence scores
- Generates per-group confidence metrics

### PDF Export

- Exports each detected group as a separate PDF file
- Preserves image quality (95% JPEG quality)
- Outputs files as `group_1.pdf`, `group_2.pdf`, etc.

### Metadata Generation

- Produces a `metadata.json` file alongside exported PDFs
- Includes group ID, page count, grouping confidence, and ordering confidence
- Lists all pages within each group with their original indices and image paths

### CLI Interface

- Full command-line interface via `python main.py`
- Accepts input path (PDF or ZIP)
- Supports `--output-dir`, `--temp-dir`, and `--quiet` flags
- Provides verbose progress logging by default

---

## Planned Architecture

```
React Frontend
        |
        v
FastAPI Backend
        |
        v
OCR Provider Interface
        |
        v
Grouping Engine
        |
        v
Export Engine
        |
        v
Download
```

Every layer should be independently replaceable.

The OCR provider, grouping algorithm, and export format can each be swapped without affecting other layers. The frontend communicates only with the backend API. The backend delegates OCR, grouping, and export through clearly defined interfaces.

---

## OCR Strategy

OCR must be pluggable. The grouping pipeline must never depend on the OCR implementation.

### Initially Supported

| Provider | Type | Notes |
|----------|------|-------|
| EasyOCR | Local | Current default. Requires PyTorch. GPU optional. |
| OCR.space | Cloud | Free tier available. No local dependencies. |

### Future Support

- Google Cloud Vision
- PaddleOCR
- Azure Computer Vision

The OCR layer exposes a single interface: `image path -> text`. All downstream logic consumes only the extracted text.

---

## Deployment Strategy

### Local Mode

- EasyOCR with PyTorch
- Fully offline processing
- No usage limits
- Requires GPU for acceptable speed
- Best for batch processing large collections

### Cloud Mode

- OCR.space as the OCR provider
- Lightweight backend with no GPU dependency
- Suitable for free-tier hosting
- Ideal for small to medium workloads

Future versions should allow selecting the OCR provider through configuration. The same codebase must support both modes with zero code changes.

---

## Tech Stack

### Frontend

- React
- Responsive UI
- Mobile-first design

### Backend

- FastAPI

### Processing

- Python

### OCR

- Pluggable providers (EasyOCR, OCR.space, future providers)

### Deployment

- Docker
- Render / Railway / Fly.io for backend
- Vercel for frontend (if feasible)
- Prefer zero-cost infrastructure where practical

---

## Product Roadmap

### Phase 1: Core MVP

- PDF input
- ZIP input
- OCR with EasyOCR
- Group detection (keyword + similarity)
- PDF export
- Metadata generation
- CLI interface
- Confidence scoring

**Status: Implemented**

### Phase 2: Backend API

- FastAPI server wrapping the existing pipeline
- Upload endpoint for PDF and ZIP files
- Processing status and result retrieval
- Error handling and validation

### Phase 3: React Frontend

- File upload interface
- Processing status display
- Result preview and download
- Responsive and mobile-friendly layout

### Phase 4: Deployment

- Docker containerization
- Backend deployment (Render, Railway, or Fly.io)
- Frontend deployment (Vercel)
- End-to-end deployment verification

### Phase 5: OCR Abstraction

- Define a provider-agnostic OCR interface
- Implement OCR.space adapter
- Configuration-driven provider selection
- Fallback logic between providers

### Phase 6: AI Enhancements

- AI-generated document titles
- AI-generated subject/category
- AI-generated summary for each grouped paper
- AI-assisted page ordering (future research)

These features enhance the product but are not required for the core workflow.

Semantic search, RAG, chatbots, vector databases, and large LLM features are intentionally postponed until after the production product is complete.
---

## Future Features

- Drag-and-drop upload
- Upload multiple individual images (backend creates ZIP automatically)
- Upload history
- Re-download previous jobs
- Progress bar with live updates
- Cancel processing
- Multiple OCR providers
- User accounts (optional)
- Admin dashboard (optional)

## Engineering Rules

- Keep the project deployable at all times.
- Never tightly couple OCR providers to the grouping or export logic.
- Prefer clean architecture over clever code.
- Every module should have a single responsibility.
- Finish one feature completely before starting another.
- Every completed milestone should end with testing and a git checkpoint.
