"""
ML-based semantic matcher using TF-IDF + Cosine Similarity.

Instead of just counting keyword matches, this converts the full text
of both the JD and resume into vectors and measures how similar they are.
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline
import re
import string


# ─────────────────────────────────────────────────────────────────────────────
# Text Cleaning
# ─────────────────────────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    """
    Normalise text before feeding into TF-IDF.
    - lowercase everything
    - remove punctuation
    - collapse extra spaces
    """
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ─────────────────────────────────────────────────────────────────────────────
# The Matcher Class
# ─────────────────────────────────────────────────────────────────────────────

class TFIDFMatcher:
    """
    Computes semantic similarity between a Job Description and a Resume
    using TF-IDF vectorisation and cosine similarity.

    How it works:
    1. Collect all resume texts + JD text into one corpus
    2. Fit TF-IDF on the whole corpus (so vocabulary is shared)
    3. Transform each text into a vector
    4. Compute cosine similarity between JD vector and each resume vector
    """

    def __init__(self):
        # ngram_range=(1,2) means we look at single words AND pairs
        # e.g. "machine learning" is treated as one unit, not just "machine" + "learning"
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=8000,
            stop_words='english',  # ignore "the", "and", "is" etc.
            min_df=1,              # include even rare terms (small corpus)
            sublinear_tf=True,     # dampens very high frequency words
        )
        self._fitted = False

    def _build_resume_text(self, profile) -> str:
        """
        Combine all the useful text from a resume into one string.
        We weight skills and experience sections more by repeating them.
        """
        parts = []

        # Add candidate summary
        if profile.summary:
            parts.append(profile.summary)

        # Add skills — repeated twice to give them more weight
        skill_text = " ".join(s.canonical for s in profile.skills)
        parts.append(skill_text)
        parts.append(skill_text)  # repeated for emphasis

        # Add experience text from raw sections
        if "experience" in profile.raw_sections:
            parts.append(profile.raw_sections["experience"])

        # Add project text
        if "projects" in profile.raw_sections:
            parts.append(profile.raw_sections["projects"])

        # Add skills section raw text
        if "skills" in profile.raw_sections:
            parts.append(profile.raw_sections["skills"])

        return clean_text(" ".join(parts))

    def _build_jd_text(self, jd) -> str:
        """Combine JD description + required skills into one string."""
        parts = [jd.description]
        parts.extend(jd.required_skills)
        parts.extend(jd.preferred_skills)
        return clean_text(" ".join(parts))

    def fit_and_score(
        self,
        jd,
        profiles: list,
    ) -> dict[str, float]:
        """
        Main method — given a JD and list of resume profiles,
        return a dict of { resume_id → similarity_score (0.0 to 1.0) }
        """
        if not profiles:
            return {}

        # Step 1: Build text representations
        jd_text = self._build_jd_text(jd)
        resume_texts = [self._build_resume_text(p) for p in profiles]

        # Step 2: Fit TF-IDF on ALL texts together (JD + all resumes)
        # This ensures everyone shares the same vocabulary
        all_texts = [jd_text] + resume_texts
        self.vectorizer.fit(all_texts)
        self._fitted = True

        # Step 3: Transform each text into a vector
        jd_vector = self.vectorizer.transform([jd_text])           # shape: (1, n_features)
        resume_vectors = self.vectorizer.transform(resume_texts)   # shape: (n_resumes, n_features)

        # Step 4: Compute cosine similarity
        # Returns a matrix of shape (1, n_resumes)
        # Each value is how similar that resume is to the JD
        similarities = cosine_similarity(jd_vector, resume_vectors)[0]
        # similarities[0] is the score for profiles[0], etc.

        # Step 5: Return as dict { resume_id → score }
        return {
            profile.id: float(round(score, 4))
            for profile, score in zip(profiles, similarities)
        }


# ─────────────────────────────────────────────────────────────────────────────
# Explain the match (so we can show it in the UI)
# ─────────────────────────────────────────────────────────────────────────────

def get_matching_terms(jd_text: str, resume_text: str, top_n: int = 8) -> list[str]:
    """
    Find the most important words that appear in BOTH the JD and resume.
    These are the terms driving the similarity score.
    """
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words='english',
        max_features=5000,
    )

    cleaned_jd = clean_text(jd_text)
    cleaned_resume = clean_text(resume_text)

    try:
        tfidf_matrix = vectorizer.fit_transform([cleaned_jd, cleaned_resume])
        feature_names = vectorizer.get_feature_names_out()

        jd_scores     = tfidf_matrix[0].toarray()[0]
        resume_scores = tfidf_matrix[1].toarray()[0]

        # A term matters if it scores high in BOTH documents
        combined = jd_scores * resume_scores
        top_indices = combined.argsort()[-top_n:][::-1]

        return [feature_names[i] for i in top_indices if combined[i] > 0]
    except Exception:
        return []