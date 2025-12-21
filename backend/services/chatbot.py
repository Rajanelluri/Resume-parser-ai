# backend/services/chatbot.py
import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "llama3.1"   # change to "mistral" if you pulled mistral


def build_prompt(session: dict, user_question: str) -> str:
    resume = (session.get("resume_text") or "")[:3000]
    jd = (session.get("job_description") or "")[:3000]
    role = session.get("job_role", "unknown")
    score = session.get("score", 0)
    required_skills = session.get("required_skills", [])

    skills_str = ", ".join(required_skills) if required_skills else "N/A"

    return f"""
You are a Resume ATS Assistant chatbot.

Context:
- Job Role: {role}
- ATS Score: {score}/10
- Required Skills: {skills_str}

Job Description:
{jd}

Resume:
{resume}

User Question:
{user_question}

Instructions:
- Answer in a clear, practical way.
- Give bullet points if helpful.
- If user asks how to improve score, list missing skills + specific edits.
- Do not hallucinate experience; suggest wording improvements instead.
"""


def ollama_answer(prompt: str) -> str:
    print(" ollama_answer() is running")
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }


    r = requests.post(OLLAMA_URL, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    return (data.get("response") or "").strip()
