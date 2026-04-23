# Case Grinder

An AI-powered legal case digest generator focused on fast, structured outputs from raw case documents.

---

## Overview

**Case Grinder** allows users to:

- Upload a PDF of a legal case
- Extract and clean text automatically
- Generate structured legal digests using AI

Current digest output includes:

- Standard and Detailed versions
- Title
- Case Number
- Decision Date
- Abstract
- Facts
- Issues
- Ruling
- Ratio
- Summary

---

## Tech Stack

### Frontend

- Next.js
- TypeScript

### Backend

- FastAPI
- pdfminer.six

### AI

- Groq API (`llama-3.1-8b-instant`)

### Deployment

- Frontend: Vercel
- Backend: Render (Docker)

---

## Project Structure

```text
Case-Grinder/
├── backend/
│   ├── index.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── service/
│   │   └── generate_digest.py
│   └── utils/
│       ├── extract_text_from_pdf.py
│       ├── clean_text.py
│       └── validate_digest.py
└── frontend/
    └── case-grinder/
        ├── app/
        │   ├── layout.tsx
        │   └── page.tsx
        └── components/
```

---

## MVP Roadmap

### Phase 1

- Upload and process PDF cases
- Generate structured digest output

### Phase 2

- Improve prompt quality and output consistency
- Better error handling and validation

### Phase 3

- Improve UI readability and filtering
- Add result export options

### Phase 4

- Add authentication and saved digests
- Add search and bookmarks

---

## Contributing

Contributions are welcome.

Simple flow:

1. Fork the repository
2. Create your branch from `dev`
3. Make your changes
4. Open a Pull Request to `dev`

Branch naming:

- `fix/<short-description>` for bug fixes
- `add/<short-description>` for additions

Example:

```bash
git checkout dev
git pull origin dev
git checkout -b add/case-filter-ui
```

---

## Issues

If you find a bug, open an issue and include:

- What happened
- Expected behavior
- Steps to reproduce
- Screenshots/logs (if available)
- Environment details (OS, browser, Python/Node versions)

---

## Suggestions

For ideas or feature requests, open an issue and label it as a suggestion.

Please include:

- Problem you are trying to solve
- Proposed change
- Why it helps users/developers
- Optional mockups or examples

---
