# 🩺 FirstDoor

### AI-Assisted Early Health Risk Assessment & Clinical Decision Support

<p align="center">
  <strong>🚪 Your First Door to Smarter Healthcare Guidance</strong>
</p>

<p align="center">
  FirstDoor is an AI-assisted clinical decision-support prototype that helps users perform an early health-risk assessment, identify potentially urgent situations, receive specialty guidance, undergo psychological screening, analyze laboratory and imaging information, and find suitable hospital referrals.
</p>

<p align="center">
  <a href="https://first-door-gamma.vercel.app">🌐 Live Website</a> •
  <a href="https://firstdoor.onrender.com/docs">📚 API Documentation</a> •
  <a href="https://firstdoor.onrender.com/health">💚 Backend Health</a>
</p>

---

## ⚠️ Medical Disclaimer

> **FirstDoor is an educational and hackathon prototype.**
>
> It is **not a medical diagnostic system** and does not replace qualified doctors, professional medical advice, diagnosis, treatment, or emergency medical care.
>
> If someone is experiencing a medical emergency, they should contact their local emergency services or seek immediate professional medical attention.

---

# 🌟 What is FirstDoor?

Healthcare decisions can sometimes begin with uncertainty:

* *Is this symptom serious?*
* *Which medical specialist should I consult?*
* *Should I seek immediate medical attention?*
* *What could my laboratory results indicate?*
* *Where can I find an appropriate hospital?*

**FirstDoor** aims to provide an intelligent first layer of healthcare guidance.

Instead of treating every user query identically, the system combines **rule-based safety detection, clinical risk assessment, psychological screening, specialty routing, laboratory analysis, imaging analysis, and hospital referral**.

The goal is to help users understand their situation and identify an appropriate **next step** while keeping safety as a priority.

---

# ✨ Key Features

## 🩺 1. General Health Assessment

Users can provide information such as:

* Symptoms
* Age
* Medical history
* Symptom severity
* Duration

The system processes this information and provides:

* 📊 Risk assessment
* 🧠 Possible health conditions
* 👨‍⚕️ Recommended medical specialty
* 🗺️ Suggested next steps
* 💡 Medical explanations

### API

```http
POST /api/assess
```

---

## 🚨 2. Emergency & Safety Detection

FirstDoor includes a dedicated safety layer designed to identify potentially urgent situations.

Examples include symptoms such as:

* Chest pain
* Difficulty breathing
* Severe shortness of breath
* Sudden weakness
* Slurred speech
* Seizures

When a potentially urgent situation is detected, the system can **prioritize an emergency recommendation instead of continuing through the normal decision flow**.

### Safety Flow

```text
User Symptoms
      ↓
Safety Detection
      ↓
 ┌───────────────┐
 │ Emergency?    │
 └───────┬───────┘
      YES│       │NO
         ↓       ↓
 Emergency     Continue
 Guidance      Assessment
```

---

# 🧠 3. Psychological Screening

FirstDoor supports structured psychological screening using:

### PHQ-9

Used as a structured screening questionnaire for depressive symptoms.

### GAD-7

Used as a structured screening questionnaire for anxiety symptoms.

The psychological module includes:

* Crisis/safety detection
* Screening-score calculation
* Risk-band classification
* Safety protections for minors
* Mental-health referral guidance

### API

```http
POST /triage
```

---

# 🧪 4. Laboratory Analysis

FirstDoor provides a dedicated API for laboratory information.

Users/services can submit laboratory tests and corresponding values for analysis.

### Supported Input

```text
Test → Value
```

### API

```http
POST /labs/analyze
```

This module is designed to provide structured interpretation and guidance around submitted laboratory information.

---

# 🩻 5. Imaging Analysis

FirstDoor also supports basic structured imaging analysis.

Information can include:

* Imaging modality
* Body part
* Findings
* Urgency

### API

```http
POST /imaging/analyze
```

The module can help organize imaging findings and determine an appropriate level of attention or follow-up.

---

# 🏥 6. Hospital Referral

The hospital referral module can recommend hospitals based on:

* 🩺 Medical specialty
* 📍 City
* 🚨 Emergency status

### API

```http
POST /hospitals/referral
```

The hospital information is maintained in:

```text
backend/data/hospitals.json
```

---

# 🤖 7. AI-Powered Medical Explanations

FirstDoor can integrate **Google Gemini** to provide natural-language explanations.

The architecture separates the decision-making logic from the explanation layer.

```text
Clinical Input
      ↓
Safety Rules
      ↓
Risk Engine
      ↓
Decision Engine
      ↓
Structured Result
      ↓
Gemini Explanation
      ↓
User-Friendly Guidance
```

This approach helps prevent the LLM from being the only mechanism responsible for safety-critical decisions.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │      USER           │
                         │  Web Application    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     FRONTEND        │
                         │ React / Node.js     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FASTAPI        │
                         │       Backend       │
                         └──────────┬──────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
        ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
        │ Safety Rules │    │ Risk Engine  │    │   Routing    │
        │              │    │              │    │   Engine     │
        └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
               │                   │                   │
               └───────────────────┼───────────────────┘
                                   ▼
                         ┌─────────────────────┐
                         │  Decision Engine    │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌────────────┐        ┌────────────┐        ┌────────────┐
       │Psychology  │        │    Labs    │        │  Imaging   │
       └────────────┘        └────────────┘        └────────────┘
              │                     │                     │
              └─────────────────────┼─────────────────────┘
                                    ▼
                         ┌─────────────────────┐
                         │ Hospital Referral   │
                         └─────────────────────┘

                         ┌─────────────────────┐
                         │   Gemini / LLM      │
                         │ Explanation Layer   │
                         └─────────────────────┘
```

---

# 📂 Project Structure

```text
FirstDoor/
│
├── backend/
│   │
│   ├── app/
│   │   ├── main.py
│   │   ├── knowledge_base.py
│   │   └── llm_service.py
│   │
│   ├── safety/
│   │   ├── psychological.py
│   │   └── rules.py
│   │
│   ├── services/
│   │   ├── decision_engine.py
│   │   ├── risk_engine.py
│   │   ├── routing_engine.py
│   │   ├── psychological.py
│   │   ├── labs.py
│   │   ├── imaging.py
│   │   └── hospitals.py
│   │
│   ├── data/
│   │   ├── medical_knowledge.json
│   │   └── hospitals.json
│   │
│   ├── tests/
│   │   ├── test_decision_engine.py
│   │   ├── test_risk.py
│   │   ├── test_routing.py
│   │   ├── test_safety.py
│   │   └── test_psychological.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   └── package.json
│
├── .gitignore
└── README.md
```

---

# 🛠️ Technology Stack

## Frontend

* ⚛️ React
* 🟢 Node.js
* 📦 npm
* 🌐 REST API integration

## Backend

* 🐍 Python 3.10+
* ⚡ FastAPI
* 🚀 Uvicorn
* 📋 Pydantic
* 🔐 python-dotenv

## AI

* 🤖 Google Gemini
* 🧠 Rule-based clinical decision logic
* 📊 Risk assessment engine

## Deployment

* ▲ Vercel — Frontend
* ☁️ Render — Backend

---

# 🌐 Access the Live Website

## Step 1 — Open the FirstDoor Website

Visit:

### 👉 https://first-door-gamma.vercel.app

This opens the deployed FirstDoor frontend.

---

## Step 2 — Navigate Through the Website

The general user journey is:

```text
Open FirstDoor
      ↓
Enter Health Information
      ↓
Provide Symptoms
      ↓
Enter Age / Medical History
      ↓
Specify Severity & Duration
      ↓
Submit Assessment
      ↓
Safety Check
      ↓
Risk Assessment
      ↓
Possible Conditions
      ↓
Recommended Specialty
      ↓
Suggested Next Steps
```

Depending on the functionality exposed by the frontend, users can also interact with the corresponding health-analysis modules.

---

# 🔗 Backend URLs

The deployed backend is available at:

### 🏠 API Root

https://firstdoor.onrender.com/

### 💚 Health Check

https://firstdoor.onrender.com/health

### 📚 Swagger API Documentation

https://firstdoor.onrender.com/docs

The `/docs` page provides an interactive **Swagger UI** where API endpoints can be explored and tested.

---

# 🧭 How to Explore the API

Open:

**https://firstdoor.onrender.com/docs**

You will see the available API endpoints.

Typical endpoints include:

```text
GET  /
GET  /health

POST /api/assess
POST /triage
POST /labs/analyze
POST /imaging/analyze
POST /hospitals/referral
```

### Using Swagger

1. Open the `/docs` URL.
2. Select an endpoint.
3. Click **Try it out**.
4. Enter the required JSON request body.
5. Click **Execute**.
6. Review the API response.

This is useful for testing the backend independently from the frontend.

---

# 💻 Run FirstDoor Locally

If you want to run the complete project on your computer, follow the steps below.

---

## 📋 Prerequisites

Install the following first:

### Backend

* Python **3.10 or higher**
* pip

### Frontend

* Node.js **18 or higher**
* npm

Check your installed versions:

```bash
python --version
pip --version
node --version
npm --version
```

---

# 1️⃣ Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/shourya-dev7/FirstDoor.git
```

Enter the project:

```bash
cd FirstDoor
```

---

# 2️⃣ Set Up the Backend

Open a terminal in the project root.

Create a virtual environment:

```bash
python -m venv .venv
```

---

## 🪟 Windows PowerShell

Activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

## 🪟 Windows Command Prompt

```cmd
.venv\Scripts\activate
```

## 🍎 macOS / 🐧 Linux

```bash
source .venv/bin/activate
```

After activation, your terminal should indicate that the virtual environment is active.

---

# 3️⃣ Install Backend Dependencies

From the project root:

```bash
pip install -r backend/requirements.txt
```

The backend uses packages including:

```text
fastapi
uvicorn[standard]
pydantic
python-dotenv
google-genai
```

---

# 4️⃣ Configure Environment Variables

If you want to use the Gemini-powered explanation service, create:

```text
backend/.env
```

Add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

### 🔐 Important

Never commit your `.env` file or API keys to GitHub.

Make sure `.env` is included in `.gitignore`.

---

# 5️⃣ Start the Backend

Move into the backend directory:

```bash
cd backend
```

Start FastAPI:

```bash
python -m uvicorn app.main:app --reload
```

The local backend will normally be available at:

### http://127.0.0.1:8000

---

# 6️⃣ Check That the Backend Works

Open:

### API Root

http://127.0.0.1:8000/

You should receive a response similar to:

```json
{
  "message": "FirstDoor API is running!",
  "docs": "/docs",
  "health": "/health"
}
```

Then open:

### Health Check

http://127.0.0.1:8000/health

Expected response:

```json
{
  "status": "healthy",
  "service": "FirstDoor Backend"
}
```

---

# 7️⃣ Open Local API Documentation

Go to:

### http://127.0.0.1:8000/docs

FastAPI automatically generates an interactive Swagger interface.

From here you can test the backend APIs without using the frontend.

---

# 8️⃣ Run the Backend Tests

Keep the virtual environment activated.

From the project root or backend directory, install pytest if necessary:

```bash
pip install pytest
```

Then run:

```bash
python -m pytest tests/test_decision_engine.py tests/test_risk.py tests/test_routing.py tests/test_safety.py tests/test_psychological.py -v
```

The expected result is:

```text
18 passed
```

You can also run the complete test suite with:

```bash
python -m pytest -v
```

---

# 9️⃣ Start the Frontend

Open a **new terminal**.

Navigate to the project:

```bash
cd FirstDoor
```

Then:

```bash
cd frontend
```

Install frontend dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The terminal will display a local URL, typically similar to:

```text
http://localhost:5173
```

Open that URL in your browser.

---

# 🔌 Connecting Frontend to Backend

The frontend communicates with the backend through:

```text
frontend/src/lib/backendTriage.js
```

The deployed backend URL is configured as:

```javascript
const BACKEND_URL =
  "https://firstdoor.onrender.com/api/assess";
```

For local development, change it to:

```javascript
const BACKEND_URL =
  "http://127.0.0.1:8000/api/assess";
```

---

# 🔄 Local Application Flow

When running locally, both servers should be active.

### Terminal 1 — Backend

```bash
cd FirstDoor/backend
python -m uvicorn app.main:app --reload
```

### Terminal 2 — Frontend

```bash
cd FirstDoor/frontend
npm run dev
```

Then open:

```text
http://localhost:5173
```

The architecture becomes:

```text
Browser
   │
   ▼
localhost:5173
   │
   │ API Request
   ▼
localhost:8000
   │
   ▼
FastAPI Backend
   │
   ├── Safety
   ├── Risk Assessment
   ├── Decision Engine
   ├── Psychological Screening
   ├── Laboratory Analysis
   ├── Imaging Analysis
   └── Hospital Referral
```

---

# 🌍 Production Architecture

The deployed application follows this general structure:

```text
                         🌐 USER
                           │
                           ▼
              ┌─────────────────────────┐
              │        Vercel           │
              │   FirstDoor Frontend    │
              └────────────┬────────────┘
                           │
                           │ HTTPS API
                           ▼
              ┌─────────────────────────┐
              │         Render          │
              │   FirstDoor Backend     │
              │        FastAPI          │
              └────────────┬────────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Safety       Decision       Routing
          Engine        Engine         Engine
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
           Labs         Imaging       Hospitals
```

---

# 🚀 Deployment

## Frontend — Vercel

The frontend can be deployed using **Vercel**.

General workflow:

```bash
cd frontend
npm install
npm run build
```

Connect the GitHub repository to Vercel and configure the frontend project.

The current frontend deployment is:

### https://first-door-gamma.vercel.app

---

## Backend — Render

The FastAPI backend can be deployed using **Render**.

The current backend is available at:

### https://firstdoor.onrender.com

Useful production endpoints:

```text
https://firstdoor.onrender.com/
https://firstdoor.onrender.com/health
https://firstdoor.onrender.com/docs
```

---

# 🔐 CORS Configuration

The backend uses FastAPI CORS configuration to allow communication between the frontend and backend.

The configured origins include:

```text
http://localhost:5173
http://127.0.0.1:5173
http://localhost:5176
http://127.0.0.1:5176
http://localhost:3000
http://127.0.0.1:3000
https://first-door-gamma.vercel.app
```

If the frontend is deployed to another domain, that domain must also be added to the backend's allowed origins.

---

# 🧪 Testing Strategy

FirstDoor contains automated tests for important backend components.

### Decision Engine

```text
tests/test_decision_engine.py
```

### Risk Engine

```text
tests/test_risk.py
```

### Routing

```text
tests/test_routing.py
```

### Safety

```text
tests/test_safety.py
```

### Psychological Screening

```text
tests/test_psychological.py
```

Run all tests:

```bash
python -m pytest -v
```

---

# 🔧 Troubleshooting

## ❌ Backend Does Not Start

Make sure the dependencies are installed:

```bash
pip install -r backend/requirements.txt
```

Then:

```bash
cd backend
python -m uvicorn app.main:app --reload
```

---

## ❌ `pytest` Not Found

Install pytest:

```bash
pip install pytest
```

Then:

```bash
python -m pytest -v
```

---

## ❌ Frontend Cannot Reach Backend

Check the following:

1. Backend is running.
2. Correct backend URL is configured.
3. Frontend is using the correct `/api/assess` endpoint.
4. CORS allows the frontend domain.
5. For production, the frontend uses:

```text
https://firstdoor.onrender.com/api/assess
```

6. For local development, use:

```text
http://127.0.0.1:8000/api/assess
```

---

## ❌ API Documentation Shows "Not Found"

For the deployed backend, use:

```text
https://firstdoor.onrender.com/docs
```

For local development:

```text
http://127.0.0.1:8000/docs
```

Make sure the FastAPI server is running.

---

# 🔄 Development Workflow

Before starting development:

```bash
git pull origin main
```

Check the current repository state:

```bash
git status
```

After making changes:

```bash
git add .
```

Commit:

```bash
git commit -m "Describe your changes"
```

Push:

```bash
git push origin main
```

### Recommended workflow

```text
Pull latest code
      ↓
Create / modify feature
      ↓
Run backend tests
      ↓
Run frontend locally
      ↓
Test API integration
      ↓
Check git status
      ↓
Commit changes
      ↓
Push to GitHub
```

---

# 👥 Team Integration

FirstDoor combines multiple components developed as part of the project:

* 🩺 Medical knowledge processing
* 📊 Clinical risk assessment
* 🧠 Decision engine
* 🚨 Emergency safety detection
* 🧠 Psychological screening
* 👨‍⚕️ Specialty routing
* 🧪 Laboratory analysis
* 🩻 Imaging analysis
* 🏥 Hospital referrals
* 🌐 Frontend-backend API integration
* 🤖 AI-powered explanations

Before starting new work, team members should always synchronize their local repository:

```bash
git pull origin main
```

---

# 📡 API Quick Reference

| Method | Endpoint              | Purpose                    |
| ------ | --------------------- | -------------------------- |
| `GET`  | `/`                   | API status                 |
| `GET`  | `/health`             | Backend health check       |
| `POST` | `/api/assess`         | General health assessment  |
| `POST` | `/triage`             | Triage and decision engine |
| `POST` | `/labs/analyze`       | Laboratory analysis        |
| `POST` | `/imaging/analyze`    | Imaging analysis           |
| `POST` | `/hospitals/referral` | Hospital referral          |

---

# 🗺️ Quick Start

If you only want to **use the deployed application**:

### 1. Open the website

👉 **https://first-door-gamma.vercel.app**

### 2. Enter your health information

Provide the requested symptoms and relevant information.

### 3. Submit the assessment

FirstDoor processes the information through its decision-support pipeline.

### 4. Review the result

The system may provide:

* Risk information
* Possible conditions
* Recommended specialty
* Suggested next steps
* Explanations

### 5. Explore the backend API

Visit:

👉 **https://firstdoor.onrender.com/docs**

### 6. Check backend status

Visit:

👉 **https://firstdoor.onrender.com/health**

---

# 🔒 Security & Best Practices

* Never commit API keys.
* Never commit `.env` files containing secrets.
* Keep sensitive credentials in environment variables.
* Validate API inputs.
* Test backend changes before pushing.
* Keep CORS configuration updated.
* Do not treat prototype output as professional medical diagnosis.

---

# 🎯 Project Objective

The primary objective of FirstDoor is to explore how **AI, rule-based systems, and structured clinical workflows** can work together to provide accessible early-stage healthcare guidance.

Rather than attempting to replace healthcare professionals, FirstDoor focuses on supporting the **initial decision-making layer**:

```text
Symptoms
   ↓
Safety
   ↓
Risk
   ↓
Specialty
   ↓
Next Step
   ↓
Healthcare System
```

---

# 🚀 Future Scope

Potential future improvements include:

* 🔐 Secure user authentication
* 📱 Mobile application
* 🌍 Multi-language healthcare guidance
* 🗣️ Voice-based symptom input
* 📈 Long-term health tracking
* 🔬 More comprehensive laboratory interpretation
* 🩻 Advanced medical-image processing
* 🏥 Real-time hospital availability
* 👨‍⚕️ Doctor consultation integration
* 📊 Personalized health dashboards
* 🔒 Stronger privacy and security controls

---

# ❤️ Why FirstDoor?

Healthcare should not feel like a maze.

**FirstDoor aims to provide a clear starting point.**

> **Understand the symptoms.
> Detect potential risk.
> Find the right direction.
> Take the next step.**

---

# 👨‍💻 Project Information

**Project:** FirstDoor
**Category:** AI / Healthcare / Clinical Decision Support
**Type:** Hackathon Prototype
**Backend:** FastAPI + Python
**Frontend:** React + Node.js
**AI:** Google Gemini
**Deployment:** Vercel + Render

### 🔗 Important Links

| Resource             | Link                                      |
| -------------------- | ----------------------------------------- |
| 🌐 Live Website      | https://first-door-gamma.vercel.app       |
| 💻 GitHub Repository | https://github.com/shourya-dev7/FirstDoor |
| ⚡ Backend            | https://firstdoor.onrender.com            |
| 💚 Backend Health    | https://firstdoor.onrender.com/health     |
| 📚 API Documentation | https://firstdoor.onrender.com/docs       |

---

<p align="center">
  <strong>🩺 FirstDoor — Your First Door to Smarter Healthcare Guidance 🚪</strong>
</p>

<p align="center">
  Built with ❤️ for innovation in healthcare technology.
</p>
