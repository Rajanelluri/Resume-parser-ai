from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uuid

from services.extract_text import extract_text
from services.preprocess import clean_text
from services.scoring import compute_final_score
from services.skills_config import ROLE_SKILLS

app = FastAPI(
    title="Resume Parser AI",
    version="1.0.0",
    description="AI-powered resume parsing and scoring API"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://[::]:5500",
        "http://[::1]:5500",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).resolve().parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
def home():
    return {"message": "Resume Parser API is running. Go to /docs for Swagger UI."}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/roles")
def roles():
    return {"roles": list(ROLE_SKILLS.keys())}

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    job_role: str = Form(...),
    job_description: str = Form(...)
):
    if job_role not in ROLE_SKILLS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid job role. Choose from: {list(ROLE_SKILLS.keys())}"
        )

    if not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF or DOCX files are supported."
        )

    temp_path = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"

    try:
        contents = await file.read()
        temp_path.write_bytes(contents)

        resume_text = extract_text(str(temp_path))
        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from resume."
            )

        resume_clean = clean_text(resume_text)
        jd_clean = clean_text(job_description)

        score = compute_final_score(resume_clean, jd_clean, job_role)

        return {
            "job_role": job_role,
            "score": round(score, 2),
            "required_skills": ROLE_SKILLS[job_role],
            "matched_skills": [],
            "resume_preview": resume_text[:1200],
        }

    finally:
        try:
            if temp_path.exists():
                temp_path.unlink()
        except Exception:
            pass
