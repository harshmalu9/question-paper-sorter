# Question Paper Sorter

Automatically classify, organize, and generate subject-wise PDFs from scanned medical question papers using OCR, NLP embeddings, and document classification.

---

## Features

* GPU-accelerated OCR using EasyOCR
* Automatic page rotation detection
* OCR result caching
* Medical subject classification using sentence embeddings
* Rule-based subject overrides
* Document type classification
* Automatic page organization
* PDF generation from classified pages
* Single-command execution

---

## Supported Subjects

* Pharmacology
* Pathology
* Microbiology
* Forensic Medicine
* Community Medicine

---

## Supported Document Types

* Theory
* Practical
* MCQ
* Communication
* Unknown

---

## Pipeline

```text
PDF
 │
 ▼
PDF → Images
 │
 ▼
OCR (EasyOCR + GPU)
 │
 ▼
Rotation Detection
 │
 ▼
Text Extraction
 │
 ▼
Subject Classification
 │
 ▼
Document Type Classification
 │
 ▼
Page Organization
 │
 ▼
PDF Generation
```

---

## Project Structure

```text
question-paper-sorter/

├── data/
│   ├── input/
│   ├── temp/
│   ├── cache/
│   └── output/
│
├── src/
│   ├── ocr/
│   ├── classification/
│   ├── preprocessing/
│   ├── organizer/
│   ├── pdf/
│   ├── reporting/
│   ├── models/
│   └── exporters/
│
├── run.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/harshmalu9/question-paper-sorter.git

cd question-paper-sorter
```

Create virtual environment:

```bash
python -m venv venv
```

Activate:

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running

Place a PDF inside:

```text
data/input/
```

Run:

```bash
python run.py data/input/sample.pdf
```

---

## Outputs

### Metadata

```text
data/output/pages.json
```

Contains:

* Page number
* OCR text
* Subject
* Subject confidence
* Document type
* Document type confidence

### Sorted Pages

```text
data/output/sorted/
```

Example:

```text
Pharmacology/
├── Theory/
├── Practical/
├── MCQ/
└── Communication/
```

### Generated PDFs

```text
data/output/pdfs/
```

Example:

```text
Pharmacology_Theory.pdf
Microbiology_Practical.pdf
Community_Medicine_Theory.pdf
```

---

## OCR Optimizations

The OCR engine includes:

### GPU Acceleration

Uses CUDA-enabled EasyOCR.

### Rotation Detection

Each page is checked for orientation and corrected automatically.

### OCR Cache

Previously processed pages are loaded directly from cache.

### Early Exit Optimization

Pages that already produce high-quality OCR at 0° rotation skip additional rotation checks.

---

## Technologies Used

* Python
* EasyOCR
* OpenCV
* Sentence Transformers
* PyTorch
* PDF2Image
* Scikit-Learn

---

## Example Workflow

```text
69-page scanned PDF

        ↓

OCR + Rotation Correction

        ↓

Subject Classification

        ↓

Document Type Classification

        ↓

Automatic Sorting

        ↓

15+ Organized PDFs
```

---

## Future Improvements

* Additional medical subjects
* Better unknown-page classification
* Batch PDF processing
* Web interface
* Desktop GUI
* Analytics dashboard
* Confidence-based human review

---

## Author

Harsh Malu

MIT-WPU

Computer Science Engineering

```
```
