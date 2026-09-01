# =========================================================
# FIRSTDOOR MEDICAL KNOWLEDGE BASE
# =========================================================

import json
from pathlib import Path


# =========================================================
# LOAD MEDICAL DATASET
# =========================================================

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "medical_knowledge.json"
)


with open(
    DATA_FILE,
    "r",
    encoding="utf-8"
) as file:

    MEDICAL_DATA = json.load(file)


# =========================================================
# DATA SECTIONS
# =========================================================

CONDITIONS_DATA = MEDICAL_DATA.get(
    "conditions",
    []
)

TREATMENTS_DATA = MEDICAL_DATA.get(
    "treatments",
    []
)

LABORATORY_TESTS_DATA = MEDICAL_DATA.get(
    "laboratory_tests",
    []
)


if not isinstance(
    CONDITIONS_DATA,
    list
):
    CONDITIONS_DATA = []


if not isinstance(
    TREATMENTS_DATA,
    list
):
    TREATMENTS_DATA = []


if not isinstance(
    LABORATORY_TESTS_DATA,
    list
):
    LABORATORY_TESTS_DATA = []


# =========================================================
# BUILD SYMPTOM KNOWLEDGE BASE
# =========================================================

KNOWLEDGE_BASE = {}


for condition in CONDITIONS_DATA:

    if not isinstance(
        condition,
        dict
    ):
        continue


    condition_name = str(
        condition.get(
            "name",
            ""
        )
    ).strip()


    condition_symptoms = condition.get(
        "symptoms",
        []
    )


    specialty = condition.get(
        "specialty"
    )


    common_tests = condition.get(
        "common_tests",
        []
    )


    if not isinstance(
        condition_symptoms,
        list
    ):
        continue


    if not isinstance(
        common_tests,
        list
    ):
        common_tests = []


    for symptom in condition_symptoms:

        symptom = str(
            symptom
        ).strip().lower()


        if not symptom:
            continue


        if symptom not in KNOWLEDGE_BASE:

            KNOWLEDGE_BASE[symptom] = {

                "conditions": [],

                "tests": [],

                "specialty": specialty,

                "red_flags": [],
            }


        # -------------------------------------------------
        # CONDITION
        # -------------------------------------------------

        if (
            condition_name
            and condition_name
            not in KNOWLEDGE_BASE[
                symptom
            ]["conditions"]
        ):

            KNOWLEDGE_BASE[
                symptom
            ]["conditions"].append(
                condition_name
            )


        # -------------------------------------------------
        # TESTS
        # -------------------------------------------------

        for test in common_tests:

            test = str(
                test
            ).strip()


            if (
                test
                and test
                not in KNOWLEDGE_BASE[
                    symptom
                ]["tests"]
            ):

                KNOWLEDGE_BASE[
                    symptom
                ]["tests"].append(
                    test
                )


        # -------------------------------------------------
        # SPECIALTY
        # -------------------------------------------------

        if (
            not KNOWLEDGE_BASE[
                symptom
            ].get("specialty")
            and specialty
        ):

            KNOWLEDGE_BASE[
                symptom
            ]["specialty"] = specialty


# =========================================================
# SPECIALTY PRIORITY
# =========================================================

SPECIALTY_PRIORITY = {

    "Cardiology": 5,

    "Neurology": 5,

    "Pulmonology": 5,

    "Gastroenterology": 4,

    "Endocrinology": 4,

    "General Medicine": 1,
}


# =========================================================
# MEDICAL HISTORY
# =========================================================

MEDICAL_HISTORY = {

    "diabetes": {

        "associated_conditions": [
            "Diabetes mellitus",
            "Diabetes-related complications",
        ],

        "recommended_tests": [
            "Blood glucose",
            "HbA1c",
        ],
    },


    "high blood pressure": {

        "associated_conditions": [
            "Hypertension",
            "Cardiovascular risk",
            "Cerebrovascular risk",
        ],

        "recommended_tests": [
            "Blood pressure measurement",
            "Blood tests",
            "ECG",
        ],
    },


    "heart disease": {

        "associated_conditions": [
            "Cardiovascular disease",
            "Cardiovascular condition",
        ],

        "recommended_tests": [
            "ECG",
            "Blood tests",
            "Cardiac evaluation",
        ],
    },


    "asthma": {

        "associated_conditions": [
            "Asthma",
            "Asthma-related condition",
            "Respiratory condition",
        ],

        "recommended_tests": [
            "Pulmonary function testing",
            "Spirometry",
            "Pulse oximetry",
        ],
    },


    "previous stroke": {

        "associated_conditions": [
            "Neurological disorder",
            "Cerebrovascular risk",
            "Neurological condition",
        ],

        "recommended_tests": [
            "Neurological examination",
            "Brain imaging",
        ],
    },
}


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_symptom_information(
    symptom: str
):

    symptom = str(
        symptom
    ).lower().strip()


    return KNOWLEDGE_BASE.get(
        symptom,
        {
            "conditions": [],
            "tests": [],
            "specialty": None,
            "red_flags": [],
        },
    )


def get_history_information(
    history: str
):

    history = str(
        history
    ).lower().strip()


    return MEDICAL_HISTORY.get(
        history,
        {
            "associated_conditions": [],
            "recommended_tests": [],
        },
    )