 Resume Parser AI
An AI-powered web application that analyzes resumes against job descriptions, computes ATS match scores, and provides chatbot-based feedback using a locally hosted LLM via Ollama.

🚀 Features
- Upload resumes (PDF/DOCX) and job descriptions
- Get ATS match score and skill gap analysis
- Preview extracted resume content
- Ask follow-up questions via integrated chatbot
- Powered by FastAPI backend and Ollama LLM
- Frontend built with vanilla HTML/CSS/JS

🧱 Architecture
Frontend (HTML/CSS/JS)
│
├── Resume upload + job description
│
├── Chat Assistant (calls /chat endpoint)
│
└──→ FastAPI Backend
     ├── /upload-resume → parses resume, scores match
     ├── /chat → sends prompt to Ollama
     └── Ollama (localhost:11434) → responds with AI feedback



🛠 Setup Instructions
1. Clone the repo
git clone https://github.com/your-username/resume-parser-ai.git
cd resume-parser-ai


2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows


3. Install dependencies
pip install -r requirements.txt


4. Start Ollama locally
Install Ollama and run:
ollama serve
ollama run llama3.1  # or mistral / phi3


5. Start FastAPI backend
uvicorn app:app --reload


6. Open frontend
Open frontend/index.html in your browser (served via Live Server or manually).

💬 Chatbot Integration
- The chatbot sends user questions to /chat
- Backend formats the prompt and sends it to Ollama
- Ollama responds with resume improvement suggestions
- Response is displayed in the chat log

📦 API Endpoints
|  |  |  | 
|  | /upload-resume |  | 
|  | /chat |  | 
|  | /roles |  | 
|  | /health |  | 



🧠 Models Supported
- llama3.1
- mistral:7b-instruct
- phi3 (fastest for local use)
Set model in app.py:
OLLAMA_MODEL = "phi3"



🧪 Sample Prompts
- “How can I improve my ATS score?”
- “Which skills are missing for Cloud Engineer?”
- “Rewrite my resume summary for better impact”
OUTPUTS:
<img width="1920" height="1200" alt="OUTPUT1" src="https://github.com/user-attachments/assets/ed5efaec-13af-4a44-b1f3-dfe62b99f903" />

<img width="1920" height="1200" alt="OUTPUT2" src="https://github.com/user-attachments/assets/4143ebe1-8f77-4106-95fe-4a2296ef5619" />

<img width="1920" height="1200" alt="Screenshot (107)" src="https://github.com/user-attachments/assets/4639a903-ddda-4041-aa8c-f360a537ebcf" />

<img width="1920" height="1200" alt="CHATBOT WITH OUTPUT" src="https://github.com/user-attachments/assets/fb400521-ddfa-4ce6-b08e-8b32ed0a61ba" />
