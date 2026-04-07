from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# A single skill found in a resume
# e.g. the word "React" → canonical name "react", category "frontend"
class SkillEntry(BaseModel):
    name: str          # how it appeared in the resume ("ReactJS", "React.js")
    canonical: str     # our standardised name ("react")
    category: str      # what type of skill ("frontend", "backend", "language")
    source_section: str = "unknown"  # which part of the resume it came from


# One job they worked at
class ExperienceEntry(BaseModel):
    title: str                        # "Senior Software Engineer"
    company: str = ""                 # "Google"
    duration_years: float = 0.0      # 3.5
    description: str = ""
    skills_mentioned: list[str] = [] # skills found inside this job entry


# One degree/diploma
class EducationEntry(BaseModel):
    degree: str          # "Bachelor of Technology"
    institution: str = ""
    year: Optional[int] = None
    field: str = ""


# The full parsed resume — this is the main object we'll work with
class ResumeProfile(BaseModel):
    id: str                                    # unique ID we generate
    filename: str                              # "john_doe_resume.pdf"
    candidate_name: str = "Unknown"
    email: str = ""
    phone: str = ""
    total_experience_years: float = 0.0
    skills: list[SkillEntry] = []
    experience_entries: list[ExperienceEntry] = []
    education_entries: list[EducationEntry] = []
    raw_sections: dict[str, str] = {}         # raw text per section
    certifications: list[str] = []
    summary: str = ""
    parse_status: str = "success"             # "success", "failed", "unsupported"
    job_role: str = ""                        # which role this resume was uploaded for
    upload_batch: str = ""                    # batch ID when uploaded together
    created_at: datetime = Field(default_factory=datetime.utcnow)


# A job description that recruiters create
class JobDescription(BaseModel):
    id: str
    title: str                          # "Senior React Developer"
    description: str                    # full JD text
    required_skills: list[str] = []    # ["react", "typescript"]
    preferred_skills: list[str] = []   # ["graphql", "aws"]
    min_experience_years: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


# The score for one candidate against one JD
class CandidateScore(BaseModel):
    resume_id: str
    candidate_name: str
    filename: str
    compatibility_score: float    # 0–100, the final score
    skill_match_score: float      # how many skills matched
    experience_score: float       # experience vs requirement
    matched_skills: list[str]
    missing_skills: list[str]
    total_experience_years: float
    top_skills: list[str]
    ai_justification: str = ""   # 2-sentence explanation for top 5
    rank: int = 0


# The full ranking result returned to the frontend
class RankingResult(BaseModel):
    job_id: str
    job_title: str
    total_candidates: int
    ranked_candidates: list[CandidateScore]


# What we return after uploading files
class UploadResult(BaseModel):
    filename: str
    status: str        # "success", "failed", "unsupported"
    resume_id: Optional[str] = None
    error: Optional[str] = None


class BatchUploadResponse(BaseModel):
    batch_id: str
    job_role: str
    total_files: int
    successful: int
    failed: int
    results: list[UploadResult]