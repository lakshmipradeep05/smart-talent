from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services import store
from app.routers import resumes, jobs    # ← make sure jobs is here

app = FastAPI(title="Smart Talent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resumes.router)
app.include_router(jobs.router)          # ← and this line exists

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/dashboard")
def dashboard():
    stats = store.get_dashboard_stats()
    resumes_list = store.get_all_resumes()
    top_talent = sorted(resumes_list, key=lambda r: r.total_experience_years, reverse=True)[:3]
    return {
        **stats,
        "top_talent": [
            {
                "name": r.candidate_name,
                "role": r.job_role,
                "experience_years": r.total_experience_years,
                "top_skills": [s.canonical for s in r.skills[:5]],
            }
            for r in top_talent
        ]
    }