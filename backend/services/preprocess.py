# backend/services/preprocess.py

import re

def clean_text(text: str) -> str:
    """
    Safe text cleaner (no NLTK). This avoids NLTK download issues inside Uvicorn.
    Later we can upgrade to NLTK after backend works.
    """
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
