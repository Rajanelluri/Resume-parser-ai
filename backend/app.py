from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uuid

from services.extract_text import extract_text
from services.preprocess import clean_text
from services.scoring import compute_final_score
from services.skills_config import ROLE_SKILLS

# Chatbot (Ollama)
from services.chatbot import build_prompt, ollama_answer

app = FastAPI(
    title="Resume Parser AI",
    version="1.0.0",
    description="AI-powered resume parsing, scoring, and chatbot API"
)

# -----------------------------
# CORS (Frontend -> Backend)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Upload directory
# -----------------------------
UPLOAD_DIR = Path(__file__).resolve().parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# -----------------------------
# Simple in-memory session store
# (For demo: one user on local machine)
# -----------------------------
LAST_SESSION = {
    "resume_text": "",
    "job_description": "",
    "job_role": "",
    "score": 0,
    "required_skills": []
}


@app.get("/")
def home():
    return {"message": "Resume Parser API is running. Go to /docs for Swagger UI."}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    job_role: str = Form(...),
    job_description: str = Form(...)
):
    # Validate role
    if job_role not in ROLE_SKILLS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid job role. Choose from: {list(ROLE_SKILLS.keys())}"
        )

    # Validate file type
    if not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF or DOCX files are supported."
        )

    temp_path = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"

    try:
        # Save uploaded file
        contents = await file.read()
        temp_path.write_bytes(contents)

        # Extract resume text (path-based)
        resume_text = extract_text(str(temp_path))
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from resume.")

        # Clean text for scoring model
        resume_clean = clean_text(resume_text)
        jd_clean = clean_text(job_description)

        # Compute ATS score
        score = compute_final_score(resume_clean, jd_clean, job_role)

        # Store session for chatbot
        LAST_SESSION["resume_text"] = resume_text
        LAST_SESSION["job_description"] = job_description
        LAST_SESSION["job_role"] = job_role
        LAST_SESSION["score"] = round(float(score), 2)
        LAST_SESSION["required_skills"] = ROLE_SKILLS.get(job_role, [])

        return {
            "job_role": job_role,
            "score": round(float(score), 2),
            "required_skills": ROLE_SKILLS[job_role],
            "resume_preview": resume_text[:1200]
        }

    finally:
        # Cleanup uploaded temp file
        try:
            if temp_path.exists():
                temp_path.unlink()
        except Exception:
            pass


@app.post("/chat")
async def chat(message: str = Form(...)):
    # Must analyze first
    if not LAST_SESSION.get("resume_text") or not LAST_SESSION.get("job_description"):
        raise HTTPException(
            status_code=400,
            detail="Please analyze a resume first, then use the chatbot."
        )

    user_question = (message or "").strip()
    if not user_question:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    prompt = build_prompt(LAST_SESSION, user_question)

    try:
        reply = ollama_answer(prompt)
        if not reply:
            raise HTTPException(status_code=500, detail="Empty response from Ollama.")
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")
