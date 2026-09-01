import os

from google import genai
from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_FILE)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY was not found.\n"
        f"Expected .env file at: {ENV_FILE}"
    )


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# GEMINI MEDICAL EXPLANATION
# =========================================================

def generate_medical_explanation(
    age,
    symptoms,
    severity,
    duration,
    medical_history,
    risk_level,
    risk_score,
    specialty,
    possible_conditions,
    recommended_tests,
):

    prompt = f"""
You are an AI assistant supporting a prototype medical
risk-assessment application called FirstDoor.

IMPORTANT:
- Do not diagnose the patient.
- Do not claim certainty.
- Do not prescribe medication.
- Do not replace a healthcare professional.
- Base your response only on the information provided.
- Clearly state that this is a prototype assessment.

Patient information:

Age: {age}

Symptoms:
{symptoms}

Severity:
{severity}/10

Duration:
{duration}

Medical history:
{medical_history}

Prototype risk level:
{risk_level}

Prototype risk score:
{risk_score}/100

Suggested specialty:
{specialty}

Possible conditions from the knowledge base:
{possible_conditions}

Recommended tests from the knowledge base:
{recommended_tests}

Write a short, clear explanation for the user.

Explain:
1. What the reported symptoms may indicate in general.
2. Why the prototype assigned this risk level.
3. Why the suggested specialty may be relevant.
4. Why the listed tests may be considered by a healthcare professional.
5. When the patient should seek medical attention.

Do not introduce a new diagnosis that is not supported
by the supplied information.

End with:
"This is not a medical diagnosis. Please consult a qualified healthcare professional."
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        if not response or not response.text:
            print("Gemini returned an empty response.")

            return (
                "The AI explanation could not be generated. "
                "Please consult a qualified healthcare professional."
            )

        return response.text.strip()

    except Exception as exc:

        print("")
        print("=" * 60)
        print("GEMINI API ERROR")
        print("=" * 60)
        print(repr(exc))
        print("=" * 60)
        print("")

        return (
            "The AI explanation could not be generated. "
            "Please consult a qualified healthcare professional."
        )