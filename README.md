# ⚖️ Case Grinder

An AI-powered legal case digest generator focused on fast, structured outputs from raw case documents (PDF or text). Built as a simple MVP to transform lengthy legal decisions into clear, digestible summaries.

---

## 🧠 Overview

**Case Grinder** allows users to:

* Upload a PDF of a legal case OR paste raw text
* Automatically extract and clean the content
* Generate a structured legal digest using AI

### Output includes:

* Facts
* Issues
* Ruling
* Ratio Decidendi
* Summary

---

## 🚀 Tech Stack

### Frontend

* Next.js
* shadcn/ui

### Backend

* FastAPI
* pdfminer.six (PDF parsing)

### AI

* OpenAI API (or compatible LLM)

### Storage (MVP)

* In-memory / SQLite (upgrade later)

---

## 🧱 Architecture

```
Client (Next.js)
   ↓
FastAPI Backend (rate-limited)
   ↓
PDF/Text Processing
   ↓
AI Processing Pipeline
   ↓
Structured Digest Output
```

---

## 📦 API Endpoints

### 1. Generate Digest

**POST** `/digest`

Accepts:

* `multipart/form-data` (PDF upload)
* OR `text` input

#### Request (PDF)

```
file: <uploaded_pdf>
```

#### Request (Text)

```json
{
  "text": "Full case text..."
}
```

#### Response

```json
{
  "id": "case_123",
  "status": "processing"
}
```

---

### 2. Get Digest Result

**GET** `/digest/:id`

#### Response

```json
{
  "status": "done",
  "data": {
    "facts": "...",
    "issues": "...",
    "ruling": "...",
    "ratio": "...",
    "summary": "..."
  }
}
```

---

## ⚙️ Processing Pipeline

```
PDF Upload / Text Input
        ↓
Extract Text (pdfminer)
        ↓
Clean Text
        ↓
Chunk Text
        ↓
AI Extraction (per chunk)
        ↓
Merge Results
        ↓
Final Structured Digest
```

---

## 📄 PDF Extraction

Install dependency:

```bash
pip install pdfminer.six
```

Example:

```python
from io import BytesIO
from pdfminer.high_level import extract_text

def extract_pdf_text(file_bytes: bytes) -> str:
    return extract_text(BytesIO(file_bytes))
```

---

## ✂️ Text Chunking

```python
def chunk_text(text, size=2000):
    return [text[i:i+size] for i in range(0, len(text), size)]
```

---

## 🧹 Text Cleaning

```python
import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
```

---

## 🔐 Rate Limiting (No Auth MVP)

Implemented using IP-based limiting.

Example:

```python
@limiter.limit("2/minute")
```

Purpose:

* Prevent abuse
* Control AI costs
* Ensure system stability

---

## 🧠 AI Output Format

All responses are structured as:

```json
{
  "facts": "",
  "issues": "",
  "ruling": "",
  "ratio": "",
  "summary": ""
}
```

---

## ⚡ Background Processing (Recommended)

Use FastAPI BackgroundTasks:

```python
from fastapi import BackgroundTasks

@router.post("/digest")
async def generate_digest(background_tasks: BackgroundTasks, file: UploadFile):
    case_id = create_case()
    background_tasks.add_task(process_pdf, case_id, file)
    return {"id": case_id, "status": "processing"}
```

---

## 📏 Constraints (MVP Safety)

* Max file size: **5MB**
* Rate limit: **2 requests/minute per IP**
* No authentication (yet)

---

## 🧩 Project Structure

```
app/
 ├── main.py
 ├── routes/
 │    └── digest.py
 ├── services/
 │    ├── ai.py
 │    └── pdf.py
 ├── utils/
 │    ├── chunk.py
 │    └── clean.py
 ├── core/
 │    └── rate_limit.py
```

---

## 🎯 MVP Roadmap

### Phase 1

* Text input → AI digest
* Basic UI

### Phase 2

* PDF upload
* Chunking + structured output

### Phase 3

* Background processing
* Improved prompts

### Phase 4

* Queue system (Redis)
* File storage (S3)

### Phase 5

* Authentication
* Search & bookmarks

---

## 🚨 Notes

* Focus on **accuracy over features**
* Legal text is long → chunking is essential
* PDF parsing is imperfect → always clean text
* AI cost grows fast → enforce limits early

---

## 💡 Future Improvements

* Citation extraction
* Case law linking
* Search engine
* Export to PDF
* User accounts

---

## 🧪 Quick Start (Backend)

```bash
pip install fastapi uvicorn pdfminer.six slowapi
uvicorn app.main:app --reload
```

---

## ✨ Summary

**Case Grinder** is a lightweight AI tool designed to turn complex legal cases into structured, readable digests with minimal friction—no login required, just upload and generate.

---
