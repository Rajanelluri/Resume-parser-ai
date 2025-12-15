from pathlib import Path
import pdfplumber
from docx import Document

def extract_text(file_path: str) -> str:
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext == ".pdf":
        text = []
        with pdfplumber.open(str(path)) as pdf:
            for page in pdf.pages:
                text.append(page.extract_text() or "")
        return "\n".join(text).strip()

    if ext == ".docx":
        doc = Document(str(path))
        return "\n".join([p.text for p in doc.paragraphs]).strip()

    return ""
