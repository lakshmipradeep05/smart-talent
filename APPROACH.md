# Smart Talent Selection Engine
**Approach Document**

Lakshmi Pradeep | B.Tech CSE | Govt. Model Engineering College, Kochi

---

## 1. Problem Understanding

Traditional Applicant Tracking Systems rely on exact keyword matching. When a job description asks for a 'Java Developer' and a candidate writes 'Backend Specialist with JVM expertise', the system rejects them — even though they are qualified. With 1,000+ applicants per role and recruiters spending just 6 seconds per resume, this creates two critical failures: qualified candidates are accidentally rejected, and unqualified candidates who 'keyword stuff' rank higher than genuinely skilled ones.

The goal was to build a system that understands the meaning and intent behind a resume — not just keywords.

---

## 2. Solution Design

### 2.1 Architecture Overview

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Backend API | Python, FastAPI | REST endpoints for upload, parse, rank |
| Resume Parser | pdfplumber, python-docx | Extract text from PDF and DOCX files |
| Skill Extractor | Rule-based taxonomy | Map skill synonyms to canonical names |
| ML Scorer | scikit-learn TF-IDF | Semantic similarity scoring |
| Frontend | React, Vite, Axios | Recruiter dashboard and UI |
| Data Store | In-memory (Python dict) | Fast prototype storage |

### 2.2 Resume Parsing Pipeline

- **Raw Text Extraction** — pdfplumber reads PDFs with x/y tolerance to handle two-column and table-based layouts. python-docx handles DOCX files including tables.
- **Section Detection** — splits text into labelled sections (Experience, Education, Skills, Projects, Certifications) using keyword-based heuristics.
- **Entity Extraction** — regex patterns extract name, email, phone, years of experience, and education entries.
- **Skill Extraction** — scans against a taxonomy of 60+ skills with synonym aliases. 'scikit-learn', 'sklearn', and 'scikit learn' all map to 'machine_learning'.

### 2.3 ML-Powered Scoring Engine

| Signal | Weight | Method |
|--------|--------|--------|
| TF-IDF Semantic Similarity | 45% | Cosine similarity between JD and resume vectors |
| Skill Match Score | 30% | Canonical skill overlap with parent-category expansion |
| Experience Score | 20% | Candidate years vs. required years ratio |
| Education Score | 5% | Presence of a degree |

### 2.4 AI Justification

For the top 5 ranked candidates, a rule-based 2-sentence justification is generated referencing semantic alignment, experience, top matched skills, and skill gaps — without requiring a language model API.

---

## 3. Key Design Decisions

- **Rule-based NLP over pre-trained model** — precise, explainable results with no API cost or latency.
- **TF-IDF over embeddings** — fast, transparent, sufficient for domain-specific technical vocabulary.
- **FastAPI over Flask/Django** — Pydantic validation, auto Swagger docs, native async support.
- **In-memory store over database** — removes infrastructure complexity; swap in PostgreSQL by changing only `store.py`.

---

## 4. What I Would Improve With More Time

| Improvement | Impact |
|-------------|--------|
| Replace in-memory store with SQLite/PostgreSQL | Data persists across restarts |
| Add sentence-transformer embeddings (MiniLM) | Better semantic understanding |
| OCR support for image resumes (pytesseract) | Handle scanned PDFs |
| Batch upload progress bar in UI | Better recruiter UX |
| Authentication + multi-recruiter support | Production readiness |
| Deploy to cloud (Railway / Render) | Accessible without local setup |

---

## 5. How to Run the Project

**Backend:**
```bash
cd backend
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.
EOF

