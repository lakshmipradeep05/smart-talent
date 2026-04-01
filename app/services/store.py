"""
In-memory store — acts as our database for now.
In production, replace with PostgreSQL + SQLAlchemy.
"""
from app.models.schemas import ResumeProfile, JobDescription

# These are just Python dicts: { id → object }
_resumes: dict[str, ResumeProfile] = {}
_jobs: dict[str, JobDescription] = {}


# ── Resume functions ──────────────────────────────────────────────────────────

def save_resume(profile: ResumeProfile) -> None:
    _resumes[profile.id] = profile

def get_resume(resume_id: str) -> ResumeProfile | None:
    return _resumes.get(resume_id)

def get_all_resumes() -> list[ResumeProfile]:
    return list(_resumes.values())

def get_resumes_by_role(job_role: str) -> list[ResumeProfile]:
    return [r for r in _resumes.values()
            if r.job_role.lower() == job_role.lower()]

def delete_resume(resume_id: str) -> bool:
    if resume_id in _resumes:
        del _resumes[resume_id]
        return True
    return False


# ── Job functions ─────────────────────────────────────────────────────────────

def save_job(jd: JobDescription) -> None:
    _jobs[jd.id] = jd

def get_job(job_id: str) -> JobDescription | None:
    return _jobs.get(job_id)

def get_all_jobs() -> list[JobDescription]:
    return list(_jobs.values())

def delete_job(job_id: str) -> bool:
    if job_id in _jobs:
        del _jobs[job_id]
        return True
    return False


# ── Dashboard stats ───────────────────────────────────────────────────────────

def get_dashboard_stats() -> dict:
    resumes = get_all_resumes()
    role_counts: dict[str, int] = {}

    for r in resumes:
        role = r.job_role or "Unassigned"
        role_counts[role] = role_counts.get(role, 0) + 1

    return {
        "total_resumes": len(resumes),
        "total_jobs": len(_jobs),
        "resumes_by_role": role_counts,
    }