# 🎯 Smart Talent Selection Engine

A full-stack AI-powered recruitment tool that semantically parses resumes and ranks candidates against a Job Description — going beyond keyword matching to understand intent and meaning.

---

## 🚀 Features

- **Multi-format Resume Upload** — supports PDF and DOCX
- **Intelligent Resume Parser** — extracts name, email, phone, skills, education, projects
- **Semantic Skill Matching** — understands synonyms (e.g. "PyTorch" counts as "Machine Learning")
- **TF-IDF ML Scorer** — measures semantic similarity between resume and JD
- **Candidate Ranking** — blended ML + rule-based compatibility score (0–100%)
- **AI Justification** — 2-sentence "Summary of Fit" for top 5 candidates
- **Recruiter Dashboard** — live stats, top talent preview, active roles

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Resume Parsing | pdfplumber, python-docx |
| ML Scoring | scikit-learn (TF-IDF + Cosine Similarity) |
| Frontend | React, Vite, Axios |
| Routing | React Router DOM |

---

## 📁 Project Structure

```
smart-talent/
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── routers/
│   │   │   ├── resumes.py        # Upload, list, delete resumes
│   │   │   └── jobs.py           # Create JD, rank candidates
│   │   ├── services/
│   │   │   ├── resume_parser.py  # PDF/DOCX text extraction
│   │   │   ├── skill_extractor.py# Rule-based skill detection
│   │   │   ├── ml_matcher.py     # TF-IDF semantic similarity
│   │   │   ├── scoring.py        # Blended ranking engine
│   │   │   └── store.py          # In-memory data store
│   │   ├── models/
│   │   │   └── schemas.py        # Pydantic data models
│   │   └── utils/
│   │       └── taxonomy.py       # Skill synonym taxonomy
│   └── requirements.txt
└── frontend/
    └── src/
        ├── App.jsx               # Routing + layout
        ├── api.js                # API calls to backend
        └── pages/
            ├── Dashboard.jsx     # Stats + top talent
            ├── Upload.jsx        # Resume upload form
            └── Ranking.jsx       # JD input + results table
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+

---

### Backend Setup

```bash
# 1. Navigate to backend
cd smart-talent/backend

# 2. Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install fastapi uvicorn python-multipart pdfplumber python-docx scikit-learn numpy

# 4. Start the server
uvicorn app.main:app --reload
```

Backend runs at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

---

### Frontend Setup

```bash
# 1. Navigate to frontend
cd smart-talent/frontend

# 2. Install dependencies
npm install

# 3. Start the dev server
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 🧪 How to Use

1. **Open** `http://localhost:5173` in your browser
2. **Upload Resumes** — go to Upload page, select job role, upload PDF/DOCX files
3. **Rank Candidates** — go to Rank page, enter a job title and description, click Rank
4. **View Results** — see ranked candidates with scores, skills, and AI justification
5. **Dashboard** — view total resumes, active jobs, and top talent preview

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/dashboard` | Stats + top talent |
| POST | `/resumes/upload` | Upload resume files |
| GET | `/resumes/` | List all resumes |
| POST | `/jobs/` | Create a job description |
| POST | `/jobs/{id}/rank` | Rank candidates for a job |

---

## 👩‍💻 Author

**Lakshmi Pradeep**
B.Tech Computer Science Engineering — Govt. Model Engineering College, Kochi
