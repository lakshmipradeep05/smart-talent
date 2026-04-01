"""
Scoring engine — blends rule-based skill matching with TF-IDF ML similarity.
"""
from app.models.schemas import ResumeProfile, JobDescription, CandidateScore, RankingResult
from app.services.skill_extractor import (
    extract_skills, skills_to_set, expand_with_parents, get_top_skills
)
from app.services.ml_matcher import TFIDFMatcher, get_matching_terms

# ── Weights ───────────────────────────────────────────────────────────────────
W_TFIDF      = 0.45   # ML semantic similarity  ← new!
W_SKILL      = 0.30   # rule-based skill overlap
W_EXPERIENCE = 0.20   # years of experience
W_EDUCATION  = 0.05   # has a degree


def _parse_jd_skills(jd: JobDescription) -> set[str]:
    text_skills = skills_to_set(extract_skills(jd.description, "jd"))
    explicit = {s.lower().strip() for s in jd.required_skills + jd.preferred_skills}
    return expand_with_parents(text_skills | explicit)


def _score_skills(candidate_skills: set[str], jd_skills: set[str]):
    if not jd_skills:
        return 1.0, [], []
    candidate_expanded = expand_with_parents(candidate_skills)
    matched = sorted(jd_skills & candidate_expanded)
    missing = sorted(jd_skills - candidate_expanded)
    direct  = jd_skills & candidate_skills
    parent_only = set(matched) - direct
    score = (len(direct) + 0.5 * len(parent_only)) / len(jd_skills)
    return min(score, 1.0), matched, missing


def _score_experience(candidate_years: float, required_years: float) -> float:
    if required_years <= 0:
        return 1.0 if candidate_years > 0 else 0.5
    ratio = candidate_years / required_years
    if ratio >= 1.5: return 1.0
    if ratio >= 1.0: return 0.9
    if ratio >= 0.75: return 0.7
    if ratio >= 0.5: return 0.5
    return max(0.1, ratio)


def _score_education(profile: ResumeProfile) -> float:
    return 1.0 if profile.education_entries else 0.5


def _generate_justification(
    profile, matched, missing, tfidf_score, compatibility_score
) -> str:
    exp_note = (f"{profile.total_experience_years} years of experience"
                if profile.total_experience_years > 0
                else "project-based experience")

    top_matched = matched[:3]
    skills_str  = ", ".join(top_matched) if top_matched else "relevant skills"

    # Use TF-IDF score to describe semantic alignment
    if tfidf_score >= 0.7:
        semantic_note = "strong semantic alignment with the job description"
    elif tfidf_score >= 0.4:
        semantic_note = "moderate alignment with the job requirements"
    else:
        semantic_note = "partial match with the job description"

    s1 = (f"Demonstrates {semantic_note} — brings {exp_note} "
          f"with expertise in {skills_str}.")

    if not missing:
        s2 = "Covers all detected technical requirements in the job description."
    elif len(missing) <= 3:
        s2 = f"Gaps identified in {', '.join(missing[:3])}; otherwise a strong profile."
    else:
        s2 = f"Matches {len(matched)} of {len(matched)+len(missing)} required skill areas."

    return f"{s1} {s2}"


def rank_candidates(
    profiles: list[ResumeProfile],
    jd: JobDescription
) -> RankingResult:

    # ── Step 1: Run TF-IDF ML scoring on all candidates at once ──────────────
    matcher = TFIDFMatcher()
    tfidf_scores = matcher.fit_and_score(jd, profiles)
    # tfidf_scores = { resume_id: 0.0–1.0 }

    # ── Step 2: Score each candidate ─────────────────────────────────────────
    jd_skills = _parse_jd_skills(jd)
    scored: list[CandidateScore] = []

    for profile in profiles:
        candidate_skills = skills_to_set(profile.skills)
        skill_score, matched, missing = _score_skills(candidate_skills, jd_skills)
        exp_score = _score_experience(profile.total_experience_years, jd.min_experience_years)
        edu_score = _score_education(profile)
        tfidf_score = tfidf_scores.get(profile.id, 0.0)

        # ── Blend ML + rule-based scores ─────────────────────────────────────
        composite = (
            tfidf_score  * W_TFIDF      +
            skill_score  * W_SKILL      +
            exp_score    * W_EXPERIENCE +
            edu_score    * W_EDUCATION
        )
        compatibility_pct = round(composite * 100, 1)

        scored.append(CandidateScore(
            resume_id=profile.id,
            candidate_name=profile.candidate_name,
            filename=profile.filename,
            compatibility_score=compatibility_pct,
            skill_match_score=round(skill_score * 100, 1),
            experience_score=round(exp_score * 100, 1),
            matched_skills=matched,
            missing_skills=missing,
            total_experience_years=profile.total_experience_years,
            top_skills=get_top_skills(profile.skills),
        ))

    # ── Step 3: Sort by score ─────────────────────────────────────────────────
    scored.sort(key=lambda s: s.compatibility_score, reverse=True)

    # ── Step 4: Generate justification for top 5 only ────────────────────────
    for i, candidate_score in enumerate(scored[:5]):
        profile = next(p for p in profiles if p.id == candidate_score.resume_id)
        candidate_score.ai_justification = _generate_justification(
            profile,
            candidate_score.matched_skills,
            candidate_score.missing_skills,
            tfidf_scores.get(profile.id, 0.0),
            candidate_score.compatibility_score,
        )

    for rank, s in enumerate(scored, start=1):
        s.rank = rank

    return RankingResult(
        job_id=jd.id,
        job_title=jd.title,
        total_candidates=len(scored),
        ranked_candidates=scored,
    )