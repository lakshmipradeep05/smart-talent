import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.schemas import JobDescription, RankingResult
from app.services import store
from app.services.scoring import rank_candidates

router = APIRouter(prefix="/jobs", tags=["jobs"])


class CreateJobRequest(BaseModel):
    title: str
    description: str
    required_skills: list[str] = []
    preferred_skills: list[str] = []
    min_experience_years: float = 0.0


@router.post("/", response_model=JobDescription)
def create_job(req: CreateJobRequest):
    jd = JobDescription(
        id=str(uuid.uuid4()),
        title=req.title,
        description=req.description,
        required_skills=req.required_skills,
        preferred_skills=req.preferred_skills,
        min_experience_years=req.min_experience_years,
    )
    store.save_job(jd)
    return jd


@router.get("/", response_model=list[JobDescription])
def list_jobs():
    return store.get_all_jobs()


@router.post("/{job_id}/rank", response_model=RankingResult)
def rank_for_job(job_id: str):
    jd = store.get_job(job_id)
    if not jd:
        raise HTTPException(status_code=404, detail="Job not found")

    profiles = store.get_all_resumes()
    if not profiles:
        raise HTTPException(status_code=404, detail="No resumes uploaded yet")

    valid = [p for p in profiles if p.parse_status == "success"]
    if not valid:
        raise HTTPException(status_code=422, detail="No successfully parsed resumes")

    return rank_candidates(valid, jd)