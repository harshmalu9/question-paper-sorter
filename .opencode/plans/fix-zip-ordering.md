# Fix ZIP Ordering Behavior

## Changes

### 1. `src/product/ingest.py` — Add debug logging

After line 39 (`members = zf.namelist()`), insert:

```python
print("[ZIP ORDER]")
for i, m in enumerate(
    members[:15], 1
):
    print(f"{i}: {m}")
```

### 2. `src/product/pipeline.py` — Clear OCR cache + add import

At top of file, add `import shutil` (after existing imports):

```python
import shutil
from pathlib import Path
```

At start of `process()`, before any processing, insert cache-clearing:

```python
cache_dir = Path("data/cache/ocr")
if cache_dir.exists():
    shutil.rmtree(cache_dir)
```

## Rationale

- `sorted()` was already removed in previous session — `members = zf.namelist()` preserves ZIP insertion order.
- OCR cache in `src/ocr/ocr_processor.py` uses `image_path.stem` as cache key. When both ordered and shuffled ZIPs contain identically-named files (e.g. `page_001.jpg`..`page_069.jpg`), the second run reads cached results from the first run, producing identical `PageMetadata` regardless of actual file order.
- Cache clearing ensures every `process()` call does fresh OCR in the actual on-disk file order, revealing real ordering differences.
- Debug logging makes ZIP order visible in stdout for verification.
