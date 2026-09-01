FirstDoor

FirstDoor is a clinical decision-support prototype designed to provide early health risk assessment, symptom-based guidance, specialty routing, psychological screening, laboratory analysis, imaging analysis, and hospital referral support.

⚠️ Disclaimer: FirstDoor is a prototype for educational and demonstration purposes. It does not replace professional medical advice, diagnosis, or emergency medical care.

Features
🩺 General Health Assessment

Users can provide:

Symptoms
Age
Medical history
Severity
Duration

The system analyzes the information and provides:

Risk assessment
Possible conditions
Recommended medical specialties
Suggested next steps
Medical explanations
🚨 Safety and Emergency Detection

The backend includes safety rules for identifying potentially urgent medical situations.

Examples include:

Chest pain
Difficulty breathing
Shortness of breath
Sudden weakness
Slurred speech
Seizures

Emergency cases stop the normal decision flow and return an emergency recommendation.

🧠 Psychological Screening

FirstDoor supports psychological screening instruments including:

PHQ-9
GAD-7

The system includes:

Crisis detection before scoring
Minor safety protection
Risk band classification
Mental-health referral guidance
🧪 Laboratory Analysis

The backend provides laboratory result analysis through:

POST /labs/analyze

Laboratory data can be submitted as test/value pairs.

🩻 Imaging Analysis

The backend supports basic imaging analysis through:

POST /imaging/analyze

Supported information includes:

Modality
Body part
Findings
Urgency
🏥 Hospital Referral

The hospital referral system can recommend hospitals based on:

Medical specialty
City
Emergency status

Endpoint:

POST /hospitals/referral
Project Structure
FirstDoor/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── knowledge_base.py
│   │   ├── llm_service.py
│   │   │
│   │   ├── safety/
│   │   │   ├── psychological.py
│   │   │   └── rules.py
│   │   │
│   │   └── services/
│   │       ├── decision_engine.py
│   │       ├── risk_engine.py
│   │       ├── routing_engine.py
│   │       ├── psychological.py
│   │       ├── labs.py
│   │       ├── imaging.py
│   │       └── hospitals.py
│   │
│   ├── data/
│   │   ├── medical_knowledge.json
│   │   └── hospitals.json
│   │
│   ├── tests/
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   └── package.json
│
└── README.md
Requirements
Backend
Python 3.10+
pip
Frontend
Node.js 18+
npm
Clone the Repository
git clone https://github.com/shourya-dev7/FirstDoor.git

Move into the project directory:

cd FirstDoor
Backend Setup
1. Create a Virtual Environment
python -m venv .venv
Windows PowerShell
.\.venv\Scripts\Activate.ps1
Windows Command Prompt
.venv\Scripts\activate
macOS / Linux
source .venv/bin/activate
2. Install Backend Dependencies

From the project root:

pip install -r backend/requirements.txt

The backend uses:

fastapi
uvicorn[standard]
pydantic
python-dotenv
google-genai
3. Configure Environment Variables

Create a file:

backend/.env

Add the required environment variables if you are using the Gemini-powered explanation service.

Example:

GEMINI_API_KEY=your_api_key_here

Do not commit API keys to GitHub.

4. Run the Backend Locally

Move into the backend folder:

cd backend

Start the FastAPI server:

python -m uvicorn app.main:app --reload

The backend should start at:

http://127.0.0.1:8000
Backend API
Root Endpoint
GET /

Example response:

{
  "message": "FirstDoor API is running!",
  "docs": "/docs",
  "health": "/health"
}
Health Check
GET /health

Example response:

{
  "status": "healthy",
  "service": "FirstDoor Backend"
}
API Documentation

FastAPI automatically provides interactive API documentation.

Open:

http://127.0.0.1:8000/docs
Main API Endpoints
General Health Assessment
POST /api/assess
Triage and Decision Engine
POST /triage

The triage system supports:

Emergency detection
Psychological screening
Crisis detection
Risk classification
Specialty routing
Clinical roadmap generation
Laboratory Analysis
POST /labs/analyze
Imaging Analysis
POST /imaging/analyze
Hospital Referral
POST /hospitals/referral
Running Backend Tests

Move into the backend directory:

cd backend

Install pytest if necessary:

pip install pytest

Run the decision-engine tests:

python -m pytest tests/test_decision_engine.py tests/test_risk.py tests/test_routing.py tests/test_safety.py tests/test_psychological.py -v

Expected result:

18 passed
Frontend Setup

Open a new terminal and move to the project root.

Then enter the frontend directory:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The terminal will display a local URL similar to:

http://localhost:5173

Open that URL in your browser.

Connecting Frontend and Backend

The frontend communicates with the backend through:

frontend/src/lib/backendTriage.js

The backend URL is configured using:

const BACKEND_URL = "https://firstdoor.onrender.com/api/assess";

For local development, it can be changed to:

const BACKEND_URL = "http://127.0.0.1:8000/api/assess";

For the deployed project, the frontend should use the public backend URL.

Deployment
Frontend

The frontend can be deployed using platforms such as Vercel.

Backend

The backend can be deployed using platforms such as Render.

The deployed backend currently uses the public API domain:

https://firstdoor.onrender.com

Useful endpoints include:

https://firstdoor.onrender.com/
https://firstdoor.onrender.com/health
https://firstdoor.onrender.com/docs
CORS Configuration

The backend must allow requests from the deployed frontend.

The FastAPI CORS configuration includes:

allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5176",
    "http://127.0.0.1:5176",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://first-door-gamma.vercel.app",
]

If the frontend is deployed to a different domain, that domain must also be added to the allowed origins.

Development Workflow

Before making changes:

git pull origin main

Check repository status:

git status

Create and commit changes:

git add .
git commit -m "Describe your changes"

Push changes:

git push origin main
Troubleshooting
Backend Does Not Start

Make sure dependencies are installed:

pip install -r backend/requirements.txt

Then run:

cd backend
python -m uvicorn app.main:app --reload
pytest Not Found

Install pytest:

pip install pytest

Then run:

python -m pytest -v
Frontend Cannot Reach Backend

Check that:

The backend is running.
The backend URL is correct.
CORS includes the frontend domain.
The frontend is using the deployed backend URL when running online.
API Documentation Shows Not Found

Make sure the correct URL is being used:

https://firstdoor.onrender.com/docs

The /docs endpoint should return the FastAPI Swagger interface when the backend is running correctly.

Team Integration

The project combines multiple backend and frontend components, including:

Medical knowledge processing
Clinical risk assessment
Decision engine
Emergency safety detection
Psychological screening
Specialty routing
Laboratory analysis
Imaging analysis
Hospital referrals
Frontend-backend API integration

All team members should pull the latest main branch before starting new work:

git pull origin main
Important Notes
Never commit .env files containing API keys.
Always test backend changes before pushing.
Always pull the latest main branch before merging new work.
Use the deployed backend URL for the deployed frontend.
Ensure CORS is configured correctly for the live frontend domain.
FirstDoor

Early health assessment and clinical decision-support prototype.

Built as a hackathon project to explore how intelligent software can assist with early symptom assessment, risk detection, specialty routing, and healthcare guidance.
