# backend/services/scoring.py

from pathlib import Path
import pickle
from sklearn.metrics.pairwise import cosine_similarity

from .preprocess import clean_text
from .skills_config import ROLE_SKILLS

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"

def _load_models():
    tfidf_path = MODELS_DIR / "tfidf_vectorizer.pkl"
    kmeans_path = MODELS_DIR / "skill_clusters.pkl"

    if not tfidf_path.exists() or not kmeans_path.exists():
        raise FileNotFoundError(
            "Model files not found. Run notebooks/01_build_tfidf_and_clusters.ipynb first "
            "to create backend/models/tfidf_vectorizer.pkl and backend/models/skill_clusters.pkl"
        )

    with open(tfidf_path, "rb") as f:
        tfidf_vectorizer = pickle.load(f)

    with open(kmeans_path, "rb") as f:
        kmeans = pickle.load(f)

    return tfidf_vectorizer, kmeans

# Load once when module imports
tfidf_vectorizer, kmeans = _load_models()


def compute_similarity(resume_text: str, job_desc: str) -> float:
    docs = [clean_text(resume_text), clean_text(job_desc)]
    X = tfidf_vectorizer.transform(docs)
    sim = cosine_similarity(X[0], X[1])[0][0]
    return float(sim)


def compute_skill_coverage(resume_text: str, job_role: str) -> float:
    required_skills = ROLE_SKILLS.get(job_role, [])
    if not required_skills:
        return 0.0

    resume_clean = clean_text(resume_text)

    present = 0
    for skill in required_skills:
        s = clean_text(skill)
        if s and s in resume_clean:
            present += 1

    return present / len(required_skills)


def compute_final_score(resume_text: str, job_desc: str, job_role: str) -> float:
    sim = compute_similarity(resume_text, job_desc)
    coverage = compute_skill_coverage(resume_text, job_role)

    raw = 0.6 * sim + 0.4 * coverage
    return round(raw * 10, 2)
