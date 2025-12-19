Resume Parser AI 🚀

An AI-powered Resume Parser and Scoring System that analyzes resumes against job descriptions and provides a relevance score.
Built using FastAPI, NLP (NLTK), and modern frontend technologies, this project demonstrates real-world use of AI in recruitment automation.

📌 Project Overview

Recruiters often receive hundreds of resumes for a single job role. Manually reviewing them is time-consuming and inefficient.
This project automates the resume screening process by:

Extracting text from resumes (PDF / DOCX)

Cleaning and preprocessing the text using NLP

Comparing resumes with job descriptions

Generating an AI-based matching score (0–10)

The system simulates how Applicant Tracking Systems (ATS) work in real companies.

🧠 Where AI & ML Are Used
Natural Language Processing (NLP)

Text cleaning (lowercasing, punctuation removal)

Tokenization

Stop-word removal

Lemmatization

AI Logic

Skill-based semantic matching

Resume relevance scoring

Domain-specific skill evaluation (Cloud / Data roles)

This project focuses on practical AI, not just keyword matching.

🛠️ Tech Stack
Backend

Python

FastAPI

NLTK

Scikit-learn

pdfplumber

python-docx

Frontend

HTML5

CSS3

Vanilla JavaScript

Responsive modern UI

Tools

Git & GitHub

VS Code

Uvicorn (ASGI server)


📂 Project Structure
Resume-parser-ai/
│
├── backend/
│   ├── app.py
│   ├── uploads/
│   └── services/
│       ├── extract_text.py
│       ├── preprocess.py
│       ├── scoring.py
│       └── skills_config.py
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── main.js
│
├── requirements.txt
├── README.md
└── .gitignore


⚙️ How It Works (Flow)

User uploads a resume (PDF / DOCX)

User selects a job role

User pastes job description

Backend extracts resume text

NLP preprocessing is applied

Skills & relevance are analyzed

AI score is generated

Results are displayed on the UI


🚀 Getting Started
1️⃣ Clone the Repository
git clone https://github.com/Rajanelluri/Resume-parser-ai.git
cd Resume-parser-ai

2️⃣ Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app:app --reload


Backend runs at:

http://127.0.0.1:8000


Swagger API Docs:

http://127.0.0.1:8000/docs

3️⃣ Frontend Setup
cd frontend
python -m http.server 5500


Open in browser:

http://127.0.0.1:5500

Output images:
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/438d2e82-945c-4a3a-b579-7084259a63b9" />
Result:
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/fb300f60-b963-4df7-a9f1-de1b265a480f" />


📊 Supported Job Roles

Cloud Engineer

Data Analyst

Each role has predefined skill sets used during scoring.


📈 Sample Output

Resume Match Score (0–10)

Job Role

Required Skills

Resume Preview (first 1200 characters)


🔒 Security & Best Practices

CORS properly configured

No inline JavaScript

No use of eval

File cleanup after processing

Input validation on backend


🌱 Future Enhancements

TF-IDF + Cosine Similarity

Sentence embeddings (BERT)

Multi-role selection

Resume ranking (multiple uploads)

Cloud deployment (Azure / AWS)

Database integration


⭐ Why This Project Matters

This project reflects:

Real-world AI usage

ATS-style resume screening

Practical NLP implementation

Full-stack development skills


Adding features like chatbot(not fully implemented right now working on it):
chatbot is a great upgrade. You can make it answer user questions like:
“Why is my ATS score low?”
“Which skills are missing for Cloud Engineer?”
“What should I add to improve my resume for this job description?”
“Give me 5 bullet points for my experience”
“Suggest keywords for my LinkedIn”
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/b539f34e-5940-4c26-9da5-b08d3fefb67c" />


