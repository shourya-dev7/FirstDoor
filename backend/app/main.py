from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Any, Dict, List, Optional
import json
from pathlib import Path

from .knowledge_base import (
    KNOWLEDGE_BASE,
    MEDICAL_HISTORY,
    SPECIALTY_PRIORITY,
    get_symptom_information,
    get_history_information,
)

from .llm_service import generate_medical_explanation

from .services.psychological import (
    run_psychological_screening,
)


# =========================================================
# PATHS / DATASET
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "medical_knowledge.json"

try:
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        MEDICAL_DATA = json.load(file)

except FileNotFoundError:
    raise RuntimeError(
        f"Medical dataset not found at: {DATA_FILE}"
    )

except json.JSONDecodeError as exc:
    raise RuntimeError(
        f"Medical dataset contains invalid JSON: {exc}"
    )


CONDITIONS_DATA = MEDICAL_DATA.get("conditions", [])
TREATMENTS_DATA = MEDICAL_DATA.get("treatments", [])
LABORATORY_TESTS_DATA = MEDICAL_DATA.get("laboratory_tests", [])


if not isinstance(CONDITIONS_DATA, list):
    CONDITIONS_DATA = []

if not isinstance(TREATMENTS_DATA, list):
    TREATMENTS_DATA = []

if not isinstance(LABORATORY_TESTS_DATA, list):
    LABORATORY_TESTS_DATA = []


# =========================================================
# FIRSTDOOR API
# =========================================================

app = FastAPI(
    title="FirstDoor API",
    description=(
        "FirstDoor clinical decision-support prototype "
        "for early health risk assessment."
    ),
    version="1.0.0",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5176",
        "http://127.0.0.1:5176",
        "http://localhost:3000",
        "http://127.0.0.1:3000",

        # FirstDoor live frontend
        "https://first-door-gamma.vercel.app",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def clean_list(value):
    """
    Safely convert a value into a clean list of strings.
    """

    if not isinstance(value, list):
        return []

    return [
        str(item).strip()
        for item in value
        if str(item).strip()
    ]


def unique_list(items):
    """
    Remove duplicates while preserving order.
    """

    result = []

    for item in items:
        if item not in result:
            result.append(item)

    return result


# =========================================================
# PATIENT ASSESSMENT MODEL
# =========================================================

class PatientAssessment(BaseModel):

    age: int = Field(
        ...,
        ge=1,
        le=120,
        description="Patient age",
    )

    symptoms: List[str] = Field(
        ...,
        min_length=1,
        description="Reported symptoms",
    )

    severity: int = Field(
        ...,
        ge=1,
        le=10,
        description="Symptom severity from 1 to 10",
    )

    duration: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Duration of symptoms",
    )

    medical_history: List[str] = Field(
        default_factory=list,
        description="Relevant medical history",
    )


    @field_validator("symptoms")
    @classmethod
    def validate_symptoms(cls, value):

        cleaned = [
            str(item).strip().lower()
            for item in value
            if str(item).strip()
        ]

        if not cleaned:
            raise ValueError(
                "At least one symptom is required."
            )

        return list(dict.fromkeys(cleaned))


    @field_validator("medical_history")
    @classmethod
    def validate_history(cls, value):

        cleaned = [
            str(item).strip().lower()
            for item in value
            if str(item).strip()
        ]

        return list(dict.fromkeys(cleaned))


    @field_validator("duration")
    @classmethod
    def validate_duration(cls, value):

        value = str(value).strip()

        if not value:
            raise ValueError(
                "Symptom duration is required."
            )

        return value


# =========================================================
# TRIAGE REQUEST MODEL
# =========================================================

class TriageRequest(BaseModel):
    """
    Frontend contract for psychological / emotional triage.

    IMPORTANT:
    The field names are part of the frontend contract.
    """

    answers: Dict[str, Any] = Field(
        default_factory=dict
    )

    instrument: Optional[str] = Field(
        default=None
    )


# =========================================================
# TRIAGE RESPONSE HELPERS
# =========================================================

def crisis_response(
    question_id: Optional[str],
    answer: Optional[str],
    reason: str,
):
    """
    Crisis response.

    IMPORTANT:
    No score is returned.

    drivers, referrals and roadmap are ALWAYS arrays.
    """

    drivers = []

    if question_id is not None:
        drivers.append(
            {
                "question_id": str(question_id),
                "answer": str(answer) if answer is not None else "",
            }
        )

    return {
        "risk_band": "crisis",

        "headline": (
            "Your responses indicate that immediate "
            "support may be needed."
        ),

        "drivers": drivers,

        "referrals": [],

        "roadmap": [],

        "crisis_support": {
            "name": "Emergency and crisis support",
            "numbers": [
                "Contact your local emergency services.",
                "If you are in immediate danger, go to the nearest emergency department.",
                "Reach out to a trusted person who can stay with you.",
            ],
        },
    }


def minor_support_response():
    """
    Response for users under 18 on the emotional /
    mental-health pathway.

    Psychological scoring must NOT happen.
    """

    return {
        "risk_band": "minor_support",

        "headline": (
            "Because you are under 18, this mental-health "
            "screening flow will not calculate a psychological "
            "score. Please involve a trusted adult or qualified "
            "health professional for support."
        ),

        "drivers": [],

        "referrals": [],

        "roadmap": [],

        "crisis_support": {
            "name": "Support for young people",
            "numbers": [
                "Contact a parent, guardian, school counselor, or another trusted adult.",
                "If you are in immediate danger, contact your local emergency services.",
                "Go to the nearest emergency department if urgent help is needed.",
            ],
        },
    }


# =========================================================
# TRIAGE ENDPOINT
# =========================================================

@app.post("/triage")
def triage(request: TriageRequest):

    answers = request.answers or {}
    instrument = request.instrument

    print("====================================")
    print("TRIAGE REQUEST RECEIVED")
    print("Instrument:", instrument)
    print("Answers:", answers)
    print("====================================")

    # -----------------------------------------------------
    # NORMALIZE INSTRUMENT
    # -----------------------------------------------------

    if instrument is not None:
        instrument = str(
            instrument
        ).strip().lower()

    # -----------------------------------------------------
    # BASIC ANSWER INFORMATION
    #
    # We intentionally look for age using several common
    # frontend keys so the endpoint is tolerant of the
    # existing UI.
    # -----------------------------------------------------

    age = None

    possible_age_keys = [
        "age",
        "patient_age",
        "user_age",
    ]

    for key in possible_age_keys:

        if key in answers:

            try:
                age = int(
                    answers[key]
                )
                break

            except (TypeError, ValueError):
                pass


    # =====================================================
    # MINOR SAFETY GATE
    # =====================================================
    #
    # For an under-18 user on the emotional / mental-health
    # pathway:
    #
    # STOP before psychological screening/scoring.
    #
    # No score.
    # No referrals.
    # Support contacts only.
    #
    # =====================================================

    if (
        age is not None
        and age < 18
        and instrument in {"phq9", "gad7"}
    ):

        return minor_support_response()


    # =====================================================
    # PSYCHOLOGICAL SCREENING
    # =====================================================

    if instrument in {"phq9", "gad7"}:

        try:

            screening_result = (
                run_psychological_screening(
                    answers=answers,
                    instrument=instrument,
                )
            )

        except ValueError as exc:

            # Keep the API safe and predictable.
            return {
                "risk_band": "urgent",

                "headline": (
                    "The psychological screening could not "
                    "be completed safely."
                ),

                "drivers": [],

                "referrals": [],

                "roadmap": [],

                "crisis_support": {
                    "name": "Clinical support",
                    "numbers": [
                        "Please contact a qualified healthcare professional.",
                    ],
                },
            }

        # -------------------------------------------------
        # CRISIS
        #
        # CRITICAL:
        # psychological.py performs the crisis gate BEFORE
        # scoring.
        #
        # If crisis is detected, the screening service returns
        # score=None.
        #
        # We NEVER expose a score here.
        # -------------------------------------------------

        if screening_result.get("is_crisis"):

            return crisis_response(
                question_id=screening_result.get(
                    "crisis_question_id"
                ),
                answer=screening_result.get(
                    "crisis_answer"
                ),
                reason=screening_result.get(
                    "reason",
                    "Crisis detected.",
                ),
            )


        # -------------------------------------------------
        # SAFE PSYCHOLOGICAL SCREENING
        # -------------------------------------------------

        severity = screening_result.get(
            "severity"
        )

        question_id = screening_result.get(
            "crisis_question_id"
        )

        crisis_answer = screening_result.get(
            "crisis_answer"
        )


        drivers = []

        if question_id is not None:

            drivers.append(
                {
                    "question_id": str(
                        question_id
                    ),
                    "answer": (
                        str(crisis_answer)
                        if crisis_answer is not None
                        else ""
                    ),
                }
            )


        # -------------------------------------------------
        # DETERMINE PSYCHOLOGICAL RISK BAND
        # -------------------------------------------------

        if severity == "severe":

            risk_band = "urgent"

            headline = (
                "Your screening responses suggest that "
                "professional mental-health support should "
                "be arranged promptly."
            )

        elif severity in {
            "moderately_severe",
            "moderate",
        }:

            risk_band = "soon"

            headline = (
                "Your responses suggest that speaking with "
                "a mental-health professional soon may be helpful."
            )

        elif severity == "mild":

            risk_band = "soon"

            headline = (
                "Your responses suggest some symptoms that "
                "may benefit from professional support."
            )

        else:

            risk_band = "routine"

            headline = (
                "Your responses do not indicate an immediate "
                "mental-health crisis. Continue monitoring "
                "your wellbeing and seek support if symptoms "
                "persist or worsen."
            )


        # -------------------------------------------------
        # REFERRAL
        # -------------------------------------------------

        referrals = [
            {
                "specialty": "Mental Health Professional",
                "rank": 1,
                "rationale": (
                    "A mental-health professional can review "
                    "your symptoms and provide appropriate support."
                ),
            }
        ]


        # -------------------------------------------------
        # ROADMAP
        # -------------------------------------------------

        roadmap = [
            {
                "stage": "Next step",
                "actions": [
                    "Discuss your concerns with a qualified healthcare professional.",
                    "Monitor changes in your symptoms and wellbeing.",
                ],
            }
        ]


        # -------------------------------------------------
        # CRISIS SUPPORT
        #
        # For non-crisis screening this is null.
        # -------------------------------------------------

        return {
            "risk_band": risk_band,

            "headline": headline,

            "drivers": drivers,

            "referrals": referrals,

            "roadmap": roadmap,

            "crisis_support": None,
        }


    # =====================================================
    # NO PSYCHOLOGICAL INSTRUMENT
    # =====================================================

    return {
        "risk_band": "routine",

        "headline": (
            "No psychological screening instrument was selected."
        ),

        "drivers": [],

        "referrals": [],

        "roadmap": [
            {
                "stage": "Next step",
                "actions": [
                    "Continue with the general FirstDoor health assessment.",
                ],
            }
        ],

        "crisis_support": None,
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "FirstDoor Backend",
    }


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "message": "FirstDoor API is running!",
        "docs": "/docs",
        "health": "/health",
    }


# =========================================================
# GENERAL HEALTH ASSESSMENT
# =========================================================

@app.post("/api/assess")
def assess_patient(
    patient: PatientAssessment
):

    # -----------------------------------------------------
    # NORMALIZE INPUT
    # -----------------------------------------------------

    symptoms = [
        str(symptom).strip().lower()
        for symptom in patient.symptoms
        if str(symptom).strip()
    ]

    symptoms = unique_list(
        symptoms
    )


    medical_history = [
        str(item).strip().lower()
        for item in patient.medical_history
        if str(item).strip()
    ]

    medical_history = unique_list(
        medical_history
    )


    severity = max(
        1,
        min(
            10,
            int(patient.severity)
        )
    )


    age = max(
        1,
        min(
            120,
            int(patient.age)
        )
    )


    duration = str(
        patient.duration
    ).strip()


    # =====================================================
    # RISK SCORE
    # =====================================================

    risk_score = 0


    symptom_weights = {

        "chest pain": 35,

        "difficulty breathing": 30,

        "shortness of breath": 30,

        "slurred speech": 40,

        "sudden weakness": 40,

        "seizure": 40,

        "palpitations": 20,

        "dizziness": 15,

        "vomiting": 10,

        "severe headache": 25,

        "headache": 10,

        "stomach pain": 10,

        "abdominal pain": 10,
    }


    # -----------------------------------------------------
    # SYMPTOM SCORE
    # -----------------------------------------------------

    for symptom in symptoms:

        risk_score += symptom_weights.get(
            symptom,
            0
        )


    # -----------------------------------------------------
    # SEVERITY SCORE
    # -----------------------------------------------------

    risk_score += severity * 3


    # =====================================================
    # MEDICAL HISTORY
    # =====================================================

    history_weights = {

        "diabetes": 8,

        "high blood pressure": 10,

        "heart disease": 15,

        "asthma": 5,

        "previous stroke": 20,
    }


    for condition in medical_history:

        risk_score += history_weights.get(
            condition,
            0
        )


    # -----------------------------------------------------
    # LIMIT SCORE
    # -----------------------------------------------------

    risk_score = min(
        max(
            risk_score,
            0
        ),
        100
    )


    # =====================================================
    # KNOWLEDGE BASE
    # =====================================================

    possible_conditions = []

    recommended_tests = []

    knowledge_red_flags = []

    specialty_scores = {}


    # =====================================================
    # SYMPTOM KNOWLEDGE
    # =====================================================

    for symptom in symptoms:

        try:

            information = (
                get_symptom_information(
                    symptom
                )
            )

        except Exception as exc:

            print(
                f"Knowledge lookup failed "
                f"for '{symptom}': {exc}"
            )

            information = {}


        if not isinstance(
            information,
            dict
        ):

            information = {}


        # -------------------------------------------------
        # CONDITIONS
        # -------------------------------------------------

        conditions = clean_list(
            information.get(
                "conditions",
                []
            )
        )

        possible_conditions.extend(
            conditions
        )


        # -------------------------------------------------
        # TESTS
        # -------------------------------------------------

        tests = clean_list(
            information.get(
                "tests",
                []
            )
        )

        recommended_tests.extend(
            tests
        )


        # -------------------------------------------------
        # RED FLAGS
        # -------------------------------------------------

        red_flags = clean_list(
            information.get(
                "red_flags",
                []
            )
        )

        knowledge_red_flags.extend(
            red_flags
        )


        # -------------------------------------------------
        # SPECIALTY
        # -------------------------------------------------

        symptom_specialty = information.get(
            "specialty"
        )


        if symptom_specialty:

            specialty_name = str(
                symptom_specialty
            ).strip()

            specialty_scores[
                specialty_name
            ] = (
                specialty_scores.get(
                    specialty_name,
                    0
                ) + 1
            )


    # =====================================================
    # MEDICAL HISTORY KNOWLEDGE
    # =====================================================

    for condition in medical_history:

        try:

            information = (
                get_history_information(
                    condition
                )
            )

        except Exception as exc:

            print(
                f"History lookup failed "
                f"for '{condition}': {exc}"
            )

            information = {}


        if not isinstance(
            information,
            dict
        ):

            information = {}


        associated_conditions = clean_list(
            information.get(
                "associated_conditions",
                []
            )
        )

        possible_conditions.extend(
            associated_conditions
        )


        history_tests = clean_list(
            information.get(
                "recommended_tests",
                []
            )
        )

        recommended_tests.extend(
            history_tests
        )


    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    possible_conditions = unique_list(
        possible_conditions
    )

    recommended_tests = unique_list(
        recommended_tests
    )

    knowledge_red_flags = unique_list(
        knowledge_red_flags
    )


    # =====================================================
    # SPECIALTY SELECTION
    # =====================================================

    specialty = "General Medicine"


    if specialty_scores:

        def specialty_sort_key(item):

            name, count = item

            priority = SPECIALTY_PRIORITY.get(
                name,
                0
            )

            return (
                count,
                priority
            )


        specialty = max(
            specialty_scores.items(),
            key=specialty_sort_key
        )[0]


    # -----------------------------------------------------
    # CHEST PAIN OVERRIDE
    # -----------------------------------------------------

    if (
        "chest pain" in symptoms
        and "Cardiology" in specialty_scores
    ):

        specialty = "Cardiology"


    # =====================================================
    # EMERGENCY RED FLAGS
    # =====================================================

    emergency_symptoms = {

        "chest pain",

        "difficulty breathing",

        "shortness of breath",

        "slurred speech",

        "sudden weakness",

        "seizure",
    }


    red_flags = [

        symptom

        for symptom in symptoms

        if symptom in emergency_symptoms
    ]


    red_flags = unique_list(
        red_flags
    )


    # =====================================================
    # RISK LEVEL
    # =====================================================

    if (
        risk_score >= 70
        or len(red_flags) >= 2
    ):

        risk_level = "HIGH"

        urgency = (
            "Urgent medical evaluation recommended."
        )


    elif risk_score >= 40:

        risk_level = "MEDIUM"

        urgency = (
            "Medical consultation recommended soon."
        )


    else:

        risk_level = "LOW"

        urgency = (
            "Routine medical consultation recommended."
        )


    # =====================================================
    # AI EXPLANATION
    # =====================================================

    ai_explanation = None


    try:

        ai_explanation = (
            generate_medical_explanation(

                age=age,

                symptoms=symptoms,

                severity=severity,

                duration=duration,

                medical_history=medical_history,

                risk_level=risk_level,

                risk_score=risk_score,

                specialty=specialty,

                possible_conditions=possible_conditions,

                recommended_tests=recommended_tests,
            )
        )


    except Exception as exc:

        print(
            "AI explanation failed:"
        )

        print(exc)


        ai_explanation = (
            "The AI explanation could not be generated. "
            "This assessment is based on the FirstDoor "
            "prototype rules and knowledge base. "
            "Please consult a qualified healthcare "
            "professional for medical advice."
        )


    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    return {

        "risk_level": risk_level,

        "risk_score": risk_score,

        "urgency": urgency,

        "specialty": specialty,

        "possible_conditions": (
            possible_conditions
        ),

        "recommended_tests": (
            recommended_tests
        ),

        "red_flags": red_flags,

        "knowledge_base_red_flags": (
            knowledge_red_flags
        ),

        "ai_explanation": (
            ai_explanation
        ),

        "patient_summary": {

            "age": age,

            "symptoms": symptoms,

            "severity": severity,

            "duration": duration,

            "medical_history": medical_history,
        },
    }


# =========================================================
# KNOWLEDGE BASE SEARCH
# =========================================================

@app.get("/api/search")
def search_knowledge_base(
    q: str = ""
):

    query = str(
        q
    ).lower().strip()


    if not query:

        return {
            "query": q,
            "results": [],
        }


    results = []


    # =====================================================
    # SEARCH SYMPTOMS
    # =====================================================

    for symptom, information in KNOWLEDGE_BASE.items():

        if not isinstance(
            information,
            dict
        ):

            continue


        conditions = clean_list(
            information.get(
                "conditions",
                []
            )
        )


        tests = clean_list(
            information.get(
                "tests",
                []
            )
        )


        red_flags = clean_list(
            information.get(
                "red_flags",
                []
            )
        )


        specialty = information.get(
            "specialty",
            ""
        )


        searchable_parts = (
            [symptom]
            + conditions
            + tests
            + red_flags
            + [str(specialty or "")]
        )


        searchable_text = " ".join(
            searchable_parts
        ).lower()


        if (
            query in symptom.lower()
            or query in searchable_text
        ):

            results.append({

                "type": "symptom",

                "name": symptom,

                "conditions": conditions,

                "tests": tests,

                "specialty": specialty,

                "red_flags": red_flags,
            })


    # =====================================================
    # SEARCH MEDICAL HISTORY
    # =====================================================

    for condition, information in MEDICAL_HISTORY.items():

        if not isinstance(
            information,
            dict
        ):

            continue


        associated_conditions = clean_list(
            information.get(
                "associated_conditions",
                []
            )
        )


        history_tests = clean_list(
            information.get(
                "recommended_tests",
                []
            )
        )


        searchable_text = " ".join(

            [condition]
            + associated_conditions
            + history_tests

        ).lower()


        if (
            query in condition.lower()
            or query in searchable_text
        ):

            results.append({

                "type": "medical_history",

                "name": condition,

                "conditions": associated_conditions,

                "tests": history_tests,

                "specialty": None,

                "red_flags": [],
            })


    return {

        "query": q,

        "count": len(results),

        "results": results,
    }


# =========================================================
# MEDICAL CONDITIONS DATASET
# =========================================================

@app.get("/api/conditions")
def get_conditions():

    return {

        "count": len(
            CONDITIONS_DATA
        ),

        "conditions": (
            CONDITIONS_DATA
        ),
    }


# =========================================================
# TREATMENTS
# =========================================================

@app.get("/api/treatments")
def get_treatments():

    return {

        "count": len(
            TREATMENTS_DATA
        ),

        "treatments": (
            TREATMENTS_DATA
        ),
    }


# =========================================================
# LABORATORY TESTS
# =========================================================

@app.get("/api/laboratory-tests")
def get_laboratory_tests():

    return {

        "count": len(
            LABORATORY_TESTS_DATA
        ),

        "laboratory_tests": (
            LABORATORY_TESTS_DATA
        ),
    }