# Cleanup Report

## A. Required for MVP (kept — 8 shared infra + 7 product)

### Shared infrastructure (used by both MVP and legacy)
| File | Reason |
|------|--------|
| `src/ocr/__init__.py` | Package marker |
| `src/ocr/pdf_loader.py` | PDF → images (pdf2image) |
| `src/ocr/ocr_processor.py` | Directory OCR orchestration |
| `src/ocr/ocr_engine.py` | EasyOCR engine with rotation |
| `src/models/__init__.py` | Package marker |
| `src/models/page_metadata.py` | PageMetadata dataclass |
| `src/preprocessing/__init__.py` | Package marker |
| `src/preprocessing/image_preprocessor.py` | Rotation generation |

### Product package (new — self-contained)
| File | Reason |
|------|--------|
| `src/product/__init__.py` | Package marker |
| `src/product/models.py` | MVPPPage / MVPPGroup dataclasses |
| `src/product/ingest.py` | PDF + ZIP ingestion |
| `src/product/group_detector.py` | TF-IDF + keyword boundary detection |
| `src/product/page_orderer.py` | Static ordering confidence |
| `src/product/exporter.py` | Pillow PDF + metadata JSON |
| `src/product/pipeline.py` | Orchestrator |
| `main.py` | Production entrypoint |

---

## B. Legacy-Only Code (safe to delete — 21 files, ~2000 lines)

These are used ONLY by `src/main.py` (legacy) and have zero impact on the MVP.

| Module | Files | Dependency Chain |
|--------|-------|-----------------|
| `src/classification/` | `embedding_classifier.py`, `document_type_classifier.py`, `subject_loader.py` | Uses `sentence-transformers`, `torch` |
| `src/clustering/` | `document_clusterer.py`, `cluster_namer.py` | Uses `sklearn.cluster`, `numpy` |
| `src/embeddings/` | `document_embedding_generator.py`, `similarity.py` | Standalone |
| `src/topicing/` | `semantic_topic_extractor.py` | Uses `sklearn`, `numpy` |
| `src/segmentation/` | `document_boundary_detector.py` | Uses `sentence-transformers` |
| `src/organizer/` | `page_organizer.py` | Standalone |
| `src/pdf/` | `pdf_batch_generator.py`, `pdf_generator.py` | Standalone |
| `src/exporters/` | `metadata_exporter.py` | Depends on `models.page_metadata` |
| `src/reporting/` | `report_generator.py` | Standalone |
| `src/main.py` | — | Orchestrator; imports all above |
| `run.py` | — | Entrypoint for legacy |

**Dependency impact**: Deleting these has zero impact on `main.py` or `src/product/`. The legacy `src/main.py` would stop working, but that's expected — it's being replaced by `main.py` (the new entrypoint).

---

## C. Already-Dead Code (safe to delete — 10 files, ~300 lines)

Completely unreachable from ANY entrypoint:

| File | Notes |
|------|-------|
| `src/classification/subject_classifier.py` | Orphaned; never imported |
| `src/classification/subject_override.py` | Orphaned; never imported |
| `src/segmentation/paper_segmenter.py` | Orphaned; only uses orphaned `models/paper.py` |
| `src/segmentation/paper_boundary_detector.py` | Empty stub |
| `src/models/paper.py` | Only reachable via orphaned `paper_segmenter.py` |
| `src/models/paper_segment.py` | Never imported |
| `src/analysis/ocr_quality_analyzer.py` | Standalone `__main__` script |
| `src/discovery/topic_extractor.py` | Only reachable via orphaned `keyphrase_extractor.py` |
| `src/discovery/keyphrase_extractor.py` | Orphaned; never imported |
| `src/preprocessing/text_cleaner.py` | Empty stub |
| `src/discovery/__init__.py` | Package marker for orphaned package |
| `src/utils/__init__.py` | Package marker for empty package |
| `regenerate_images.py` | Utility script, not part of any pipeline |
| `mvp_run.py` | Being replaced by `main.py` |

---

## Summary

| Category | Count | Lines |
|----------|-------|-------|
| A. Keep (required) | 16 | ~850 |
| B. Legacy-only (safe to delete) | 21 | ~2000 |
| C. Already-dead (safe to delete) | 14 | ~300 |
| **Total deletable (B + C)** | **35 files** | **~2300 lines** |
