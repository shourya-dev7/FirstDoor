from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import List

from .knowledge_base import (
    KNOWLEDGE_BASE,
    MEDICAL_HISTORY,
    SPECIALTY_PRIORITY,
    CONDITIONS_DATA,
    TREATMENTS_DATA,
    LABORATORY_TESTS_DATA,
    get_symptom_information,
    get_history_information,
)

from .llm_service import generate_medical_explanation
<<<<<<< ours

from .services.psychological import (
    run_psychological_screening,
)
from .services.labs import analyze_labs
from .services.imaging import analyze_imaging
from .services.hospitals import get_hospital_referral

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
=======
from ..rag.retrieve import retrieve
>>>>>>> theirs


# =========================================================
# FIRSTDOOR API
# =========================================================

app = FastAPI(
    title="FirstDoor API",
    description=(
        "FirstDoor prototype API for symptom-based "
        "early health risk assessment."
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
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# PATIENT INPUT
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

    # -----------------------------------------------------
    # USER-SELECTED RED FLAGS
    # -----------------------------------------------------

    red_flags: List[str] = Field(
        default_factory=list,
        description="Warning signs selected by the patient",
    )

    # -----------------------------------------------------
    # VALIDATE SYMPTOMS
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # VALIDATE MEDICAL HISTORY
    # -----------------------------------------------------

    @field_validator("medical_history")
    @classmethod
    def validate_history(cls, value):

        cleaned = [
            str(item).strip().lower()
            for item in value
            if str(item).strip()
        ]

        return list(dict.fromkeys(cleaned))

    # -----------------------------------------------------
    # VALIDATE RED FLAGS
    # -----------------------------------------------------

    @field_validator("red_flags")
    @classmethod
    def validate_red_flags(cls, value):

        cleaned = [
            str(item).strip().lower()
            for item in value
            if str(item).strip()
        ]

        return list(dict.fromkeys(cleaned))

    # -----------------------------------------------------
    # VALIDATE DURATION
    # -----------------------------------------------------

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
<<<<<<< ours
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
# MEMBER 5 REQUEST MODELS
# =========================================================

class LabItem(BaseModel):
    test: str
    value: Any


class LabsRequest(BaseModel):
    labs: List[LabItem]


class ImagingRequest(BaseModel):
    modality: Optional[str] = ""
    body_part: Optional[str] = ""
    findings: Optional[str] = ""
    urgency: Optional[str] = ""


class HospitalReferralRequest(BaseModel):
    specialty: str
    city: Optional[str] = "Chennai"
    emergency: Optional[bool] = False

# =========================================================
# TRIAGE RESPONSE HELPERS
=======
# HELPER FUNCTIONS
>>>>>>> theirs
# =========================================================

def clean_list(value):
    """
    Safely convert a value into a clean list.
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
# MEMBER 5 — LABORATORY ANALYSIS
# =========================================================

@app.post("/labs/analyze")
def laboratory_analysis(request: LabsRequest):
    labs = [
        {
            "test": lab.test,
            "value": lab.value,
        }
        for lab in request.labs
    ]

    return analyze_labs(labs)


# =========================================================
# MEMBER 5 — IMAGING ANALYSIS
# =========================================================

@app.post("/imaging/analyze")
def imaging_analysis(request: ImagingRequest):

    data = {
        "modality": request.modality,
        "body_part": request.body_part,
        "findings": request.findings,
        "urgency": request.urgency,
    }

    return analyze_imaging(data)


# =========================================================
# MEMBER 5 — HOSPITAL REFERRAL
# =========================================================

@app.post("/hospitals/referral")
def hospital_referral(request: HospitalReferralRequest):

    return get_hospital_referral(
        specialty=request.specialty,
        city=request.city or "Chennai",
        emergency=request.emergency or False,
    )

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
# ASSESSMENT
# =========================================================

@app.post("/api/assess")
def assess_patient(patient: PatientAssessment):

    # -----------------------------------------------------
    # NORMALIZE INPUT
    # -----------------------------------------------------

    symptoms = [
        str(symptom).strip().lower()
        for symptom in patient.symptoms
        if str(symptom).strip()
    ]

    symptoms = unique_list(symptoms)

    medical_history = [
        str(item).strip().lower()
        for item in patient.medical_history
        if str(item).strip()
    ]

    medical_history = unique_list(
        medical_history
    )

    # -----------------------------------------------------
    # NORMALIZE USER-SELECTED RED FLAGS
    # -----------------------------------------------------

    selected_red_flags = [
        str(item).strip().lower()
        for item in patient.red_flags
        if str(item).strip()
    ]

    selected_red_flags = unique_list(
        selected_red_flags
    )

    severity = max(
        1,
        min(10, int(patient.severity))
    )

    age = max(
        1,
        min(120, int(patient.age))
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


    # =====================================================
    # USER-SELECTED RED FLAG SCORE
    # =====================================================

    # A red flag explicitly selected by the patient is
    # treated as an urgent warning signal.
    #
    # We add 50 points for each selected warning sign,
    # while the final score is still capped at 100.
    #
    # The risk-level logic below additionally makes any
    # selected red flag HIGH risk.

    if selected_red_flags:

        risk_score += (
            len(selected_red_flags) * 50
        )


    # -----------------------------------------------------
    # LIMIT SCORE
    # -----------------------------------------------------

    risk_score = min(
        max(risk_score, 0),
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
    # RAG RETRIEVAL
    # =====================================================

    rag_results = []

    try:

        rag_query = " ".join(symptoms)

        rag_results = retrieve(
            rag_query
        )

    except Exception as exc:

        print(
            f"RAG retrieval failed: {exc}"
        )

        rag_results = []


    # -----------------------------------------------------
    # EXTRACT USEFUL INFORMATION FROM RAG
    # -----------------------------------------------------

    for result in rag_results:

        if not isinstance(
            result,
            dict
        ):
            continue

        result_type = result.get(
            "type"
        )

        # -------------------------------------------------
        # DISEASE RESULT
        # -------------------------------------------------

        if result_type == "disease":

            condition_name = result.get(
                "name"
            )

            if condition_name:

                possible_conditions.append(
                    condition_name
                )

            result_specialty = result.get(
                "specialty"
            )

            if result_specialty:

                specialty_scores[
                    result_specialty
                ] = (
                    specialty_scores.get(
                        result_specialty,
                        0
                    ) + 1
                )

            tests = clean_list(
                result.get(
                    "tests",
                    []
                )
            )

            recommended_tests.extend(
                tests
            )

        # -------------------------------------------------
        # RELATIONSHIP RESULT
        # -------------------------------------------------

        elif result_type == "relationship":

            relationship = result.get(
                "relationship"
            )

            target = result.get(
                "target"
            )

            if (
                relationship == "evaluated_by"
                and target
            ):

                recommended_tests.append(
                    str(target)
                )

            elif (
                relationship == "routes_to"
                and target
            ):

                specialty_scores[
                    str(target)
                ] = (
                    specialty_scores.get(
                        str(target),
                        0
                    ) + 1
                )


    # -----------------------------------------------------
    # REMOVE RAG DUPLICATES
    # -----------------------------------------------------

    possible_conditions = unique_list(
        possible_conditions
    )

    recommended_tests = unique_list(
        recommended_tests
    )


    # =====================================================
    # SYMPTOM KNOWLEDGE
    # =====================================================

    for symptom in symptoms:

        try:

            information = get_symptom_information(
                symptom
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
        # KNOWLEDGE BASE RED FLAGS
        # -------------------------------------------------

        kb_red_flags = clean_list(
            information.get(
                "red_flags",
                []
            )
        )

        knowledge_red_flags.extend(
            kb_red_flags
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

            information = get_history_information(
                condition
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


        # -------------------------------------------------
        # ASSOCIATED CONDITIONS
        # -------------------------------------------------

        associated_conditions = clean_list(
            information.get(
                "associated_conditions",
                []
            )
        )

        possible_conditions.extend(
            associated_conditions
        )


        # -------------------------------------------------
        # HISTORY TESTS
        # -------------------------------------------------

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
    # EMERGENCY SYMPTOMS
    # =====================================================

    emergency_symptoms = {
        "chest pain",
        "difficulty breathing",
        "shortness of breath",
        "slurred speech",
        "sudden weakness",
        "seizure",
    }


    symptom_red_flags = [
        symptom
        for symptom in symptoms
        if symptom in emergency_symptoms
    ]

    symptom_red_flags = unique_list(
        symptom_red_flags
    )


    # =====================================================
    # COMBINE RED FLAGS
    # =====================================================

    # Keep both:
    # 1. red flags explicitly selected by the user
    # 2. emergency symptoms detected from symptoms

    red_flags = unique_list(
        selected_red_flags
        + symptom_red_flags
    )


    # =====================================================
    # RISK LEVEL
    # =====================================================

    # IMPORTANT:
    # A user-selected red flag or an emergency symptom
    # makes this HIGH risk.

    if (
        len(selected_red_flags) > 0
        or risk_score >= 70
        or len(symptom_red_flags) >= 2
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

        # -------------------------------------------------
        # RISK
        # -------------------------------------------------

        "risk_level": risk_level,

        "risk_score": risk_score,

        "urgency": urgency,


        # -------------------------------------------------
        # SPECIALIST
        # -------------------------------------------------

        "specialty": specialty,


        # -------------------------------------------------
        # POSSIBLE CONDITIONS
        # -------------------------------------------------

        "possible_conditions": (
            possible_conditions
        ),


        # -------------------------------------------------
        # RECOMMENDED TESTS
        # -------------------------------------------------

        "recommended_tests": (
            recommended_tests
        ),


        # -------------------------------------------------
        # RED FLAGS
        # -------------------------------------------------

        "red_flags": red_flags,

        "selected_red_flags": (
            selected_red_flags
        ),

        "symptom_red_flags": (
            symptom_red_flags
        ),

        "knowledge_base_red_flags": (
            knowledge_red_flags
        ),


        # -------------------------------------------------
        # AI EXPLANATION
        # -------------------------------------------------

        "ai_explanation": (
            ai_explanation
        ),


        # -------------------------------------------------
        # PATIENT SUMMARY
        # -------------------------------------------------

        "patient_summary": {

            "age": age,

            "symptoms": symptoms,

            "severity": severity,

            "duration": duration,

            "medical_history": medical_history,

            "red_flags": selected_red_flags,
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