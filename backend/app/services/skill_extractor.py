"""
Skill Extractor — scans text and returns matched SkillEntry objects.
Uses the taxonomy for synonym matching and the hierarchy for parent lookup.
"""
import re
from app.utils.taxonomy import SKILL_TAXONOMY, SKILL_HIERARCHY
from app.models.schemas import SkillEntry


def extract_skills(text: str, source_section: str = "unknown") -> list[SkillEntry]:
    """
    Scan a block of text and return every skill found in the taxonomy.

    Example:
        text = "Built ML models using PyTorch and deployed on AWS"
        returns → [SkillEntry("pytorch"), SkillEntry("machine_learning"), SkillEntry("aws")]
    """
    norm_text = text.lower()
    found: list[SkillEntry] = []
    seen: set[str] = set()   # avoid duplicates

    for canonical, aliases in SKILL_TAXONOMY.items():
        for alias in aliases:
            # \b = word boundary — prevents "r" matching inside "her" or "for"
            pattern = r"\b" + re.escape(alias.lower()) + r"\b"
            if re.search(pattern, norm_text):
                if canonical not in seen:
                    seen.add(canonical)
                    category = _get_category(canonical)
                    found.append(SkillEntry(
                        name=alias,
                        canonical=canonical,
                        category=category,
                        source_section=source_section,
                    ))
                break   # found this skill, no need to check other aliases

    return found


def _get_category(canonical: str) -> str:
    """Look up category from hierarchy, or infer from canonical name."""
    parent = SKILL_HIERARCHY.get(canonical)
    if parent:
        return parent

    # Fallback inference
    if canonical in {"react", "vue", "angular", "html", "css", "svelte"}:
        return "frontend"
    if canonical in {"django", "flask", "fastapi", "express", "spring"}:
        return "backend"
    if canonical in {"sql", "nosql", "redis"}:
        return "database"
    if canonical in {"docker", "kubernetes"}:
        return "devops"
    if canonical in {"aws", "azure", "gcp"}:
        return "cloud"
    if canonical in {"machine_learning", "deep_learning", "nlp", "data_science"}:
        return "ml_ai"
    if canonical in {"python", "javascript", "java", "typescript", "go"}:
        return "language"
    return "other"


def get_top_skills(skills: list[SkillEntry], n: int = 6) -> list[str]:
    """Return the top-n most important skill names."""
    priority = ["language", "ml_ai", "frontend", "backend", "database", "devops", "cloud", "other"]
    sorted_skills = sorted(
        skills,
        key=lambda s: priority.index(s.category) if s.category in priority else 99
    )
    return [s.canonical for s in sorted_skills[:n]]


def skills_to_set(skills: list[SkillEntry]) -> set[str]:
    """Convert list of SkillEntry to a plain set of canonical names."""
    return {s.canonical for s in skills}


def expand_with_parents(skill_set: set[str]) -> set[str]:
    """
    Add parent categories to the skill set.
    e.g. {"pytorch"} → {"pytorch", "machine_learning"}
    This helps matching: JD needs "machine_learning", candidate has "pytorch" → match!
    """
    expanded = set(skill_set)
    for skill in skill_set:
        parent = SKILL_HIERARCHY.get(skill)
        if parent:
            expanded.add(parent)
    return expanded